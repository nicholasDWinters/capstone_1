from flask import Flask, render_template, request, redirect, flash, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import pdb
import requests
import os

# API key can be obtained from YouTube Data API website, and SECRET KEY is in relation to session; create both of these
from techniques import techDict
# from secrets import API_KEY, SECRET_KEY
from models import db, connect_db, User, Technique, Training_Note
from forms import UserAddForm, LoginForm, TrainingNoteForm, EditTrainingNoteForm, VideoNoteForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['API_KEY'] = os.environ.get('API_KEY')
# app.config['API_KEY'] = os.environ.get('API_KEY', API_KEY)
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL','postgresql:///jiu_jitsu_source'))
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data, password=form.password.data, email=form.email.data)
            db.session.commit()

        except IntegrityError:
            flash("Username or email already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "secondary")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    
    return redirect ('/')
    


@app.route('/')
def home():
    '''home route'''
    if CURR_USER_KEY in session:
        return redirect('/user/notes')
    else:
        return render_template('home.html')

@app.route('/user')
def go_to_notes():
    '''redirect to notes'''
    return redirect('/')


@app.route('/user/notes', methods = ['GET','POST'])
def add_note():
    '''add a training note'''

    if not g.user:
        return redirect("/")

    form = TrainingNoteForm()
    user = User.query.get_or_404(g.user.id)
    techniques = Technique.query.filter(Technique.user_id == user.id).all()
    notes = Training_Note.query.filter(Training_Note.user_id == user.id).all()
    techniques.reverse()
    notes.reverse()
    if form.validate_on_submit():
        try:
            content = form.content.data
            note = Training_Note(content = content, user_id = user.id)
            db.session.add(note)
            db.session.commit()
            flash('Added note!', 'secondary')
            return redirect('/')
        except:
            db.session.rollback()
            flash('Error adding note!', 'danger')
            return redirect('/')
   
    return render_template('show.html', user = user, form = form, techniques = techniques, notes = notes)

@app.route('/user/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    '''delete a training note from database'''
    if not g.user:
        return redirect("/")

    note = Training_Note.query.get_or_404(note_id)

    if note.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(note)
    db.session.commit()
    flash('Deleted note!', 'secondary')
    return redirect('/')

@app.route('/user/notes/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    '''edit a training note'''
    if not g.user:
        return redirect("/")
    note = Training_Note.query.get_or_404(note_id)
    form = EditTrainingNoteForm(obj = note)

    if form.validate_on_submit():
        try:
            note.content = form.content.data
            note.date = datetime.utcnow()
            db.session.commit()
            flash('Edited note!', 'secondary')
            return redirect('/')
        except:
            db.session.rollback()
            flash('Error editing note!', 'danger')
            return redirect('/')

    return render_template('editTrainingNote.html', form = form)

# ****************************************
# ROUTES FOR SHOWING TECHNIQUES, ADDING OR DELETING TECHNIQUES, ADDING TECHNIQUE NOTES


@app.route('/techniques')
def get_techniques():
    '''show the techniques page'''
    if not g.user:
        return redirect("/")

    user = User.query.get_or_404(g.user.id)
    
    return render_template('techniques.html', user = user, techDict = techDict)

@app.route('/techniques/<videoId>/<videoTitle>/<channelTitle>', methods=['POST'])
def add_technique(videoId, videoTitle, channelTitle):
    '''add technique to database'''
    if not g.user:
        return redirect("/")

    user = User.query.get_or_404(g.user.id)

    try:
        technique = Technique(user_id = user.id, video_id = videoId, video_title = videoTitle, channel_title = channelTitle)
        db.session.add(technique)
        db.session.commit()
        flash('Added technique!', 'secondary')
        return redirect('/')
    except:
        flash('Unable to add technique!', 'danger')
        return redirect('/')


@app.route('/techniques/<int:technique_id>/delete', methods=['POST'])
def delete_technique(technique_id):
    '''delete a technique from database'''
    if not g.user:
        return redirect("/")

    technique = Technique.query.get_or_404(technique_id)

    if technique.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(technique)
    db.session.commit()
    flash('Deleted technique!', 'secondary')
    return redirect('/')
    

@app.route('/techniques/<int:tech_id>/addNote', methods = ['GET', 'POST'])
def add_video_note(tech_id):
    '''add or edit a note to a technique video'''
    if not g.user:
        return redirect("/")

    technique = Technique.query.get_or_404(tech_id)
    form = VideoNoteForm(obj = technique)

    if form.validate_on_submit():
        try:
            technique.video_note = form.video_note.data
            db.session.commit()
            flash('Edited note!', 'secondary')
            return redirect('/')
        except:
            db.session.rollback()
            flash('Error editing note!', 'danger')
            return redirect('/')
    return render_template('addVideoNote.html', form = form)



# **********************************************************
# API ROUTE

@app.route('/api/search', methods=['POST'])
def search_technique():
    '''search for a technique, make a call to Youtube API'''
    errors = {}

    search = request.json['search']

    if not search:
        errors['search'] = 'Please enter a search term!'

    if errors:
        return {"errors": errors}

    search.replace(' ', '%20')

    res = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=10&q=jiu%20jitsu%20{search}&key={API_KEY}')

    
    return res.json()
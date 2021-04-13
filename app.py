from flask import Flask, render_template, request, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
import pdb
import requests
import os

# API key can be obtained from YouTube Data API website, and SECRET KEY is in relation to session; create both of these
from secrets import API_KEY, SECRET_KEY
from models import db, connect_db, User, Technique, Training_Note
from forms import UserAddForm, LoginForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL','postgresql:///jiu_jitsu_source'))
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
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
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Goodbye!", "success")
    return redirect ('/login')
    


@app.route('/')
def home():
    '''home route'''
    if CURR_USER_KEY in session:
        return render_template('show.html')
    else:
        return render_template('home.html')
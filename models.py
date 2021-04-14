from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    '''connect to database'''
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    techniques = db.relationship('Technique')
    training_notes = db.relationship('Training_Note')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(username=username, email=email, password=hashed_pwd)
        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Training_Note(db.Model):
    '''training notes for user'''
    __tablename__ = 'training_notes'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'), nullable=False)
    content = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())

    


class Technique(db.Model):
    '''techniques saved by user'''
    __tablename__ = 'techniques'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'), nullable=False)
    video_id = db.Column(db.Text, nullable = False)
    video_title = db.Column(db.Text, nullable = False)
    channel_title = db.Column(db.Text, nullable = False)
    video_note = db.Column(db.Text, nullable = True)

    
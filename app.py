from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import pdb
import requests
from secrets import API_KEY, SECRET_KEY
from models import db, connect_db

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jiu_jitsu_source'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
debug = DebugToolbarExtension(app)
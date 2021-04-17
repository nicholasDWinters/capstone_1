from models import db
from app import app

db.app = app
db.init_app(app)
db.drop_all()
db.create_all()
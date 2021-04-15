import os
from unittest import TestCase
from models import db, connect_db, User, Training_Note, Technique
from sqlalchemy import exc

os.environ['DATABASE_URL'] = "postgresql:///jiu_jitsu_source_test"


from app import app
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UserModelTestCase(TestCase):
    """Tests for user model."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()
        
        user1 = User.signup("testuser", "test@test.com", "HASHED_PASSWORD")
        user1_id = 1
        user1.id = user1_id
        
        db.session.commit()

        u1 = User.query.get(user1_id)
        
        self.u1 = u1
        
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
       

    def test_user_model(self):
        """Does basic model work?"""
       
        # User should have no techniques or training notes
        self.assertEqual(len(Technique.query.filter(Technique.user_id == self.u1.id).all()), 0)
        self.assertEqual(len(Training_Note.query.filter(Training_Note.user_id == self.u1.id).all()), 0)
        
    def test_failed_user(self):
        '''test to make sure it doesn't create a user if username, email, or password are not passed thru correctly'''
        
        user2 = User.signup(None, "test@test.com", "password")
        uid = 2
        user2.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

        db.session.rollback()

        user3 = User.signup("testtest", None, "password")
        uid = 3
        user3.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

        self.assertRaises(ValueError, User.signup, "testtest", "email@email.com", "")
        self.assertRaises(ValueError, User.signup, "testtest", "email@email.com", None)
        

    def test_authentication(self):
        '''test the authentication of an existing user, testing with a wrong username, and testing with wrong password'''
        u = User.authenticate('testuser', 'HASHED_PASSWORD')
        self.assertEqual(u.id, self.u1.id)

        self.assertFalse(User.authenticate('testuserwrong', 'HASHED_PASSWORD'))
        self.assertFalse(User.authenticate('testuser', 'WRONG_PASSWORD'))


class Training_Note_ModelTestCase(TestCase):
    """Tests for training note model."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()
        
        user1 = User.signup("testuser", "test@test.com", "HASHED_PASSWORD")
        user1_id = 1
        user1.id = user1_id
        
        db.session.commit()

        u1 = User.query.get(user1_id)

        note1 = Training_Note(id = 1, content = 'created note', user_id = 1)
        db.session.add(note1)
        db.session.commit()
        
        self.u1 = u1
        
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_check_for_note(self):
        '''does the created note exist? is it associated with our user correctly?'''
        self.assertEqual(len(Training_Note.query.filter(Training_Note.user_id == self.u1.id).all()), 1)
        self.assertEqual(len(Training_Note.query.filter(Training_Note.content == 'created note').all()), 1)


class Technique_ModelTestCase(TestCase):
    """Tests for technique model."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()
        
        user1 = User.signup("testuser", "test@test.com", "HASHED_PASSWORD")
        user1_id = 1
        user1.id = user1_id
        
        db.session.commit()

        u1 = User.query.get(user1_id)

        technique1 = Technique(id = 1, user_id = 1, video_id = 'sdkfjsdkf', video_title = 'technique title', channel_title = 'video channel', video_note = 'This is the note')
        technique2 = Technique(id = 2, user_id = 1, video_id = 'differentId', video_title = 'technique 2', channel_title = 'video channel 2', video_note = 'This is a different note')
        db.session.add(technique1)
        db.session.add(technique2)
        db.session.commit()
        
        self.u1 = u1
        
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_check_for_technique(self):
        '''does the created technique exist? is it associated with our user correctly?'''
        self.assertEqual(len(Technique.query.all()), 2)
        self.assertEqual(len(Technique.query.filter(Technique.user_id == self.u1.id).all()), 2)
        self.assertEqual(len(Technique.query.filter(Technique.video_id == 'sdkfjsdkf').all()), 1)
        self.assertEqual(len(Technique.query.filter(Technique.video_id == 'sdkkf').all()), 0)
        self.assertEqual(len(Technique.query.filter(Technique.video_title == 'technique title').all()), 1)
        self.assertEqual(len(Technique.query.filter(Technique.video_note == 'This is the note').all()), 1)
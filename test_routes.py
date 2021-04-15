import os
from unittest import TestCase
from models import db, connect_db, User, Technique, Training_Note

os.environ['DATABASE_URL'] = "postgresql:///jiu_jitsu_source_test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['TESTING'] = True

class RoutesTestCase(TestCase):
    '''test routes in app'''

    def setUp(self):
        """Create test client, add sample data."""

        Training_Note.query.delete()
        Technique.query.delete()
        User.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",email="test@test.com",password="testuser")
        
        self.testuser.id = 1
        
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_show_page(self):
        '''does the show page show redirect if not logged in? does it show details about the user if logged in?'''
        resp = self.client.get('/user/notes', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('<h1>testuser Training Notes</h1>', html)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1
            resp = c.get('/user/notes', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>testuser Training Notes</h1>', html)

    
    def test_nonUser_add_training_note(self):
        '''can a non logged in user add a training note?'''
        with self.client as c:

            resp = c.post('/user/notes', data={"content": "note content", "user_id": 1}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-1">Jiu Jitsu Source</h1>', html)


    def test_User_add_training_note(self):
        '''can a logged in user add a training note?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1

            resp = c.post('/user/notes', data={"content": "note content", "user_id": 1}, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p class="card-text">note content</p>', html)

    def test_nonUser_delete_training_note(self):
        '''can a non logged in user delete a training note?'''

        note = Training_Note(id = 1, content = 'created note', user_id = 1)
        db.session.add(note)
        db.session.commit()

        with self.client as c:
            
            resp = c.post('/user/notes/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-1">Jiu Jitsu Source</h1>', html)

    def test_User_delete_training_note(self):
        '''can a logged in user delete a training note?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1

        resp = c.post("/user/notes", data={"content": "note content", "user_id": 1}, follow_redirects=True)
        note = Training_Note.query.one()
        newResp = c.post(f'/user/notes/{note.id}/delete', follow_redirects=True)
        html = newResp.get_data(as_text=True)
        self.assertEqual(newResp.status_code, 200)
        self.assertIn('<div class="alert alert-success flashes">Deleted note!</div>', html)

    def test_nonUser_edit_training_note(self):
        '''can a non logged in user see the edit note form?'''
        note = Training_Note(id = 1, content = 'created note', user_id = 1)
        db.session.add(note)
        db.session.commit()

        resp = self.client.get('/user/notes/1/edit', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1 class="display-1">Jiu Jitsu Source</h1>', html)
    
    def test_User_edit_training_note(self):
        '''can a logged in user edit a training note?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1

        resp = c.post("/user/notes", data={"content": "note content", "user_id": 1}, follow_redirects=True)
        note = Training_Note.query.one()
        newResp = c.post(f'/user/notes/{note.id}/edit', data={"content": "edited content"}, follow_redirects=True)
        html = newResp.get_data(as_text=True)
        self.assertEqual(newResp.status_code, 200)
        self.assertIn('<div class="alert alert-success flashes">Edited note!</div>', html)
        self.assertIn('<p class="card-text">edited content</p>', html)

    def test_techniques_page(self):
        '''can a non user see the techniques page? can a user see it?'''
        resp = self.client.get('/techniques', follow_redirects=True)
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('<h2 class="mb-4">Choose a Technique</h2>', html)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1
            resp = c.get('/techniques', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2 class="mb-4">Choose a Technique</h2>', html)

    def test_nonUser_add_technique(self):
        '''can a non user add a technique?'''
        with self.client as c:

            resp = c.post('/techniques/sdfsd/videoTitle/channelTitle', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-1">Jiu Jitsu Source</h1>', html)

    def test_User_add_technique(self):
        '''can a logged in user add a technique?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1

            resp = c.post('/techniques/sdfsd/videoTitle/channelTitle', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('src="https://www.youtube.com/embed/sdfsd', html)
            self.assertIn('<p class="card-text">videoTitle</p>', html)

    def test_nonUser_delete_technique(self):
        '''can a non logged in user delete a technique?'''

        technique = Technique(id = 1, user_id = 1, video_id = 'sdkfjsdkf', video_title = 'technique title', channel_title = 'video channel')
        db.session.add(technique)
        db.session.commit()

        with self.client as c:
            
            resp = c.post('/techniques/1/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-1">Jiu Jitsu Source</h1>', html)

    def test_User_delete_technique(self):
        '''can a logged in user delete a technique?'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1

            resp = c.post('/techniques/sdfsd/videoTitle/channelTitle', follow_redirects=True)
            technique = Technique.query.one()
            resp1 = c.post(f'/techniques/{technique.id}/delete', follow_redirects=True)
            html = resp1.get_data(as_text=True)
            self.assertEqual(resp1.status_code, 200)
            self.assertIn('<div class="alert alert-success flashes">Deleted technique!</div>', html)
            self.assertNotIn('src="https://www.youtube.com/embed/sdfsd', html)

    def test_nonUser_add_technique_note(self):
        '''can a non logged in user see the form to add a technique note?'''

        technique = Technique(id = 1, user_id = 1, video_id = 'sdkfjsdkf', video_title = 'technique title', channel_title = 'video channel')
        db.session.add(technique)
        db.session.commit()

        with self.client as c:
            
            resp = c.get('/techniques/1/addNote', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="display-1">Jiu Jitsu Source</h1>', html)
            

    def test_User_add_technique_note(self):
        '''can a logged in user add a technique note'''
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1

            resp = c.post('/techniques/sdfsd/videoTitle/channelTitle', follow_redirects=True)
            technique = Technique.query.one()
            resp1 = c.post(f'/techniques/{technique.id}/addNote', data={"video_note": "great video!"}, follow_redirects=True)
            html = resp1.get_data(as_text=True)
            self.assertEqual(resp1.status_code, 200)
            self.assertIn('<div class="alert alert-success flashes">Edited note!</div>', html)
            self.assertIn('<p class="card-text">great video!</p>', html)
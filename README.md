# Capstone 1 - Jiu Jitsu Source

https://jiu-jitsu-source.herokuapp.com/


### In jiu jitsu, so much information is learned in each training session, that it can be hard to remember and keep track of it all. Keeping notes on sessions can be helpful to remember what happened on a given day. It's also a very common practice to look up technique videos on YouTube to learn about a given technique. 

**Jiu Jitsu Source** was designed to combine all of these common practices into one app, where jiu jitsu athletes can further their understanding of jiu jitsu. After registration, users are redirected to their home page, where they can take detailed notes of their training sessions, search for technique videos, and take notes on their saved videos. 

#### API Info

_The YouTube API (YouTube Data API - https://developers.google.com/youtube/v3)_ is used to search for a specified jiu jitsu technique, where the results are displayed to the user. A search is entered or selected from a list of common jiu jitsu terms, and the page is updated with 10 videos related to the specified term. Users can then add a technique video of their choosing to their techniques list. Back on the user's home page, training notes as well as their technique videos are displayed where they can edit a note associated with each technique video, or remove a technique video all together. Training notes can also be added, edited, or deleted from this page.

#### Database Models

The app uses 3 models: User, Training Note, and Technique. The User model saves the user_id, username, hashed password, and an email to the database. The Training Note model saves a foreign key to the user_id, content, and date to the database. The Technique model saves a foreign key to user_id, the video_id which is used to embed the YouTube video player to the page, video title, video channel, and a video note.

User signup, login, and logout functionality was implemented, as well as authentication and authorization. An account is required to access any of the detailed pages and search functions. Username and email must both be unique.

#### Technologies

Bootstrap was used for its minimalist design choices, easy styling of buttons and other elements, and for row/column functionality. Flash messages were implemented to help users identify when an action has worked correctly. I used WTForms for any forms in the app, mainly for easy to use validators. 

The main technologies used were Python, Flask, PostgreSQL, SQLAlchemy, and a little bit of Javascript to update the UI.

#### Installation & Testing

To run locally, clone this repo to your computer, set up a virtual environment, and install requirements. Create local database and test database in PostgreSQL, and update the app config database variables in app.py and test files. Acquire an API Key from the _The YouTube API (YouTube Data API - https://developers.google.com/youtube/v3)_ and set your key in the secrets.py file.

To run tests, use Python: Run all Tests in VSCode, or use the terminal command python -m unittest to run all tests.
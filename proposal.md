Jiu Jitsu Source is a website designed for jiu jitsu athletes to further their understanding of jiu jitsu. Users will be able to search for jiu jitsu technique videos, add videos to their 'techniques' list, take notes on those videos, and take notes in general about their recent training sessions (what went well, what to work on, setting goals, etc).

This site will use the Youtube API, to display 5-10 technique videos related to a search term input by the user. Users will be able to add them to a 'techniques' list, which will store the video details (most likely an id), to be able to display the user's favorite techniques on a seperate page.

User auth will be implemented, with registration, login, logout functionality. Session will be used to keep track of logged in users. Passwords will be hashed before storing in database. The three tables stored in a database will most likely be users, training_notes, and videos. 

The user model will have an id, username, hashed password, and email. Training_note model will have an id, user_id foreign key to users table, content, and date. The video model will have an id, user_id foreign key to users table, a youtube_id received from the Youtube API which will be used in embed codes to display videos, and a video_note.

Users will register and be redirected to their user show page, where they will be able to add/edit/remove training notes (which will also be displayed on this page), search for techniques (may include a dropdown list of potential search terms), and navigate to their 'techniques' list. 

Entering a search term will take them to a page displaying 5-10 youtube videos showing the technique they entered. Users can add these to their 'techniques' list, which will store the video id in the database, to then essentially display their favorite techniques on their individual techniques page. Users can add, edit, or remove a note to/from each of their technique videos. Functionality to remove a video from their 'techniques' list will also be added.

Bootstrap will be used for styling. Axios and javascript will be used to update pages with minimal refreshes.
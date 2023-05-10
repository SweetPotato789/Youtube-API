Youtube API

My API will show you some basic information about YouTube's attributes. It will return common basic data and even real-world data.
It gives a basic idea of how YouTube works. This will include how income works, show some popular YouTubers,
some popular videos and common user accounts to get you started. This is good for anyone new to a multipurpose platform.
It will definitely give a basic, surface-level understanding of everything. 

# API Reference Tables


# video
| HTTP Method | Endpoint | Parameters | Description |
| --- | --- | --- | --- |
| GET | /video | None | Retrieves a list of all videos in the database |
| POST | /video | title, description, author | Adds a new video to the database |
| DELETE | /video/{id} | None | Delete a specific video by ID |


# youtubers
| HTTP Method | Endpoint | Parameters | Description |
| --- | --- | --- | --- |
| GET | /youtubers | None | Retrieves a youtubers in the database |
| POST | /youtubers | name, bio | Adds new/current youtuber to the database |


# income
| HTTP Method | Endpoint | Parameters | Description |
| --- | --- | --- | --- |
| GET | /income | None | shows most popular income sources |
| POST | /income | affiliate_link, subscriptions, ads | Adds new or current ways of income on youtube |


# user_accounts
| HTTP Method | Endpoint | Parameters | Description |
| --- | --- | --- | --- |
| GET | /user_accounts | None | Retrieves a list of user_accounts from database |
| POST | /user_accounts | username, google_account, password | Adds new/current user_account to database |
| DELETE | /user_accounts/{id} | None | Delete a specific user_account by ID |


    My project evolved dramatically from taking the approach of putting everything in one file,
to dividing the files evenly in each folder and organizing them. I ended up sticking with ORM because
I discovered that using ORM resulted in fewer errors. With raw SQL, it was too complex, specifically identifying and setting
columns to a primary key or for implementing a B-tree. It was too much syntax, and I found that with ORM, it was more
readable. I found with ORM it was much easier to connect to the database. 

    In the future, I would like to improve my ER diagram planning. There were lots of attributes I had to cut out,
because I wasn't thinking of how hard it would be to implement in the code. Some of the attributes were
not the most realistic, requiring hours of syntax and some didn't make sense to include in the code. I also need to improve 
on my import and from connections. The code ran fine, but I kept getting errors because I wouldn't put my files that were imported 
in the right section (sometimes it would be indented within an if statement or, i'm suppose to put them after my models in order to run).
I would like to overall improve my ER diagram by learning everything about running a flask API, learning common issues, 
and understanding the importance of organizing the files.
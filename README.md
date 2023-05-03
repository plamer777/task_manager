# The TaskManager
The application provides functionality to manage your tasks. 
You can create new task, set its status, category and priority. Every category can be edited or removed. If you remove
a category then all tasks in it will be marked as archived and can't be shown anymore.
You also can change your task's description, priority or status. All categories have its own boards to share with 
any registered user. All users you share boards with have one of two available roles are reader and writer, all roles
can be changed at any time.
And as always every category task can be removed from list, they won't be deleted actually but marked as 'archival'.
You also can manage your goals from telegram bot

There are another functions cost to mention:
 - Registration and login by the username and password or through VK social network
 - Searching tasks by its title
 - Filtering tasks by category, status, deadline and priority
 - Filtering category by board
 - Only owner or editor can edit a board and categories with tasks into it
 - Board's owner can add, remove participant or change his role
 - Saving into CSV/JSON file
 - Creating, editing, removing and sorting comments for tasks
 - All functions also available in the mobile app
 - Get list of goals by using telegram bot
 - Create new goal or remove existing through telegram
---

**Technologies used in the project:**

 - Python 3.10
 - Django 4.1.7
 - DRF 3.14.0
 - Poetry 1.4.1
 - Gunicorn 20.1.0
 - Nginx-alpine
 - Docker
 - Docker-compose
 - Social-auth-app-django 5.2.0
 - Django-filter 23.1
---

**How to start the project:**
The project prepared for auto-deploying. So there two ways to start the project:

1. Local deployment:
 - Clone repository
 - Install docker and docker-compose packages by the command `sudo apt install docker.io docker-compose`
 - Create .env file using an example provided below
 - Prepare docker-compose.yaml file by using docker-compose.yaml or docker-compose-ci.yaml files included in the project
 - Start the app by using `sudo docker-compose up -d` command
 - Main page should be available by the ip 127.0.0.1 or localhost (if you user existing settings)
 - Telegram bot will also be available by the link provided you by the FatherBot

2. VPS deployment: 
 - Clone repository
 - Create environment variables in the 'secrets' section of your repository(all names are in the docker-compose-ci.yaml, build_deploy.yaml and .env-ci files)
 - Create new repository on the GitHub and add its url to remotes
 - Push project to your repository
 - The project should be deployed authentically if all variables are set correctly 
 - You can open main page by entering ip address of your server or domain used for it
 - Telegram bot will also be available by the link provided you by the FatherBot
---
Example of .env file:

    SECRET_KEY=your_secret_key 
    DEBUG=True
    POSTGRES_DB=postgres  # postgres db name
    POSTGRES_PASSWORD=postgres  # postgres db password
    POSTGRES_USER=postgres  # postgres db username
    POSTGRES_HOST=db
    VK_APP_ID=YOUR_VK_APP_ID
    VK_SECRET_KEY=YOUR_VK_SECRET_KEY
    TG_TOKEN=your_secret_telegram_bot_token
    WEB_HOST=http://your_host

To get VK_APP_ID and VK_SECRET_KEY you need to create a VK app. 
I can recommend to use the official documentation: 
https://dev.vk.com/mini-apps/getting-started


The project was created by Alexey Mavrin in 28 April 2023
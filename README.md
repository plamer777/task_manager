# The TaskManager
The application provides functionality to manage your tasks. You can create new task, set its status, category and priority. You also can change your task's description, priority or status. And as always every task can be removed from list, it won't be deleted actually but marked as 'archival'.

There are another functions cost to mention:
 - Searching tasks by its title
 - Filtering by category, status, year and priority
 - Saving into CSV/JSON file
 - Creating notes for tasks
 - All functions also available in the mobile app
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
---

**How to start the project:**
The project prepared for auto-deploying. So there two ways to start the project:

1. Local deployment:
 - Clone repository
 - Install docker and docker-compose packages by the command `sudo apt install docker docker-compose`
 - Create .env file using an example provided below
 - Prepare docker-compose.yaml file by using docker-compose.yaml or docker-compose-ci.yaml files included in the project
 - Start the app by using `sudo docker-compose up -d` command
 - Main page should be available by the ip 0.0.0.0:your_port

2. VPS deployment: 
 - Clone repository
 - Create environment variables in the 'secrets' section of your repository(all names are in the docker-compose-ci.yaml, build_deploy.yaml and .env-ci files)
 - Create new repository on the GitHub and add its url to remotes
 - Push project to your repository
 - The project should be deployed authentically if all variables are set correctly 

---
Example of .env file:

    SECRET_KEY=your_secret_key 
    DEBUG=True
    POSTGRES_DB=postgres  # postgres db name
    POSTGRES_PASSWORD=postgres  # postgres db password
    POSTGRES_USER=postgres  # postgres db username
    POSTGRES_HOST=localhost

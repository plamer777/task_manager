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

**How to start the project:**

 - Clone repository
 - Install Python 3.10 or higher
 - Install poetry by using command `pip install poetry`
 - Activate poetry by the execution `poetry init` and follow the steps
 - Install dependencies - `poetry install`
- Prepare .env file(an example provided below)  
- Change environment variables in the docker-compose.yaml file if necessary use the variables like in the .env file
- Run database `sudo docker-compose up -d`  
- Execute `./manage.py makemigrations` command
- Execute `./manage.py migrate`
- Run application by executing `./manage.py runserver`

---
Example of .env file:

    SECRET_KEY=your_secret_key 
    DEBUG=True
    POSTGRES_DB=postgres  # postgres db name
    POSTGRES_PASSWORD=postgres  # postgres db password
    POSTGRES_USER=postgres  # postgres db username
    POSTGRES_HOST=localhost


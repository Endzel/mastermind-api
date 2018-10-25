# mastermind-api
Mastermind is a code-breaking game for two players

##### Requirements
- MySQL 5.6 or higher
- Python 3 or higher

Libraries and frameworks used are in the _ _requirements.txt_ _ file. They will be installed preferably using the pip tool:
`pip install -r requirements.txt`

Create the database required to manage all the inside data. Access the MySQL server and execute this command:
`CREATE DATABASE mastermind;`

Next step, navigate with a Terminal or a similar CLI tool to the root of the project and execute:
`python manage.py migrate`

We would like to create our first root user for the management, with this command:
`python manage.py createsuperuser`
introducing the email, and the password twice to create it gracefully.

To run the server (and, therefore, being able to play the game and access the admin pages) you will need to execute:
`python manage.py runserver`


Instructions for playing will be available very soon!

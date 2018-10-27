# mastermind-api
Mastermind is a code-breaking game for two players.

#### Requirements
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
The server can be more customized in order to be deployed in different environments.

### Instructions for playing:

REST API that requires requests with a JSON formatted body to be able to play.

1. To create new users for playing, use the endpoint `api/user` with a POST request containing your *alias*, *email* and *password* as attributes.
2. With a POST request with your credentials as *username* attribute (email will be used) and *password* attribute to the endpoint `api/login` to retrieve your token so you can set it as header for the next requests. You are able to play now!
3. 6 colours have been defined as possible options, that are *red*, *blue*, *green*, *yellow*, *purple* and *brown*.
4. If you want to create a new game, will be in the endpoint `api/game`, POST request through giving the email of the desired codebreaker as a *codebreaker* attribute, and the code as a nested JSON object with attributes *first*, *second*, *third* and *fourth* with values as the colour options. You can also set a *limit_guesses* attribute as a small positive integer value.
5. If you want to make a play, you need to have an uncompleted game, that has been played less times the specified limit number of guesses (defaulted to 15). Game is considered to be completed when all positions guessed correctly with correct order. Play is a POST request to the endpoint `api/play` formatted with *game* attribute, that will be the ID of the game desired to play, and a *code* attribute, a nested attribute with also attributes *first*, *second*, *third* and *fourth*, with values as the colour options. That will return a *feedback* object with the same attributes, but formatted like:
- Colour not in *secret_code*: **wrong**
- Colour in *secret_code* but wrongly positioned: **white**
- Colour correctly positioned: **black**
6. You can also check the historic of a single game, and if it has been *completed* or not sending a GET request to `api/game/<id>`, being *id* the id of the game you want to check.

That is all you need to know, **happy playing!**

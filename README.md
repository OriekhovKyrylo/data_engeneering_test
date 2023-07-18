Database Configuration
To successfully connect to the database in this project, a configuration file named config.py is required in the same directory as the code. This file should contain the following fields:

user = "your_username"
password = "your_password"
host = "your_host"
port = "your_port"
db = "your_database"
Replace the values "your_username", "your_password", "your_host", "your_port", and "your_database" with the corresponding information needed to connect to your PostgreSQL database.

Make sure the config.py file is located in the same directory as the rest of the project files before running the code to connect to the database.

Note: Please be aware that the config.py file contains sensitive information such as the username and password. Ensure that the config.py file is not publicly accessible and is not published alongside your project code.

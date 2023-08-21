import psycopg2
import requests
from config import host, user, password, db, port
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



# creating a table of characters in the database
def create_characters_table(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS characters(
            id SERIAL PRIMARY KEY,
            serial_number INTEGER UNIQUE,
            name VARCHAR(100) ,
            status VARCHAR(100),
            species VARCHAR(100),
            gender VARCHAR(100),
            episodes INTEGER[]
        );"""
    )


# creating a table of locations in the database
def create_locations_table(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS locations(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE,
            type VARCHAR(100),
            dimension VARCHAR(100)
        );"""
    )


# creating a table of episodes in the database
def create_episodes_table(cursor):
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS episodes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE,
            air_date DATE,
            episode_code VARCHAR(100),
            character_id INTEGER[]
        );"""
    )


# updating data in a table characters
def insert_characters(cursor, character_data):
    character_data_list = []
    for character in character_data:
        serial_number = character['id']
        name = character['name']
        status = character['status']
        species = character['species']
        gender = character['gender']
        episodes = [int(episode.split("/")[-1]) for episode in character["episode"]]

        character_data_list.append((serial_number, name, status, species, gender, episodes))

    cursor.executemany("""
        INSERT INTO characters (serial_number, name, status, species, gender, episodes)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (serial_number) DO UPDATE
        SET name = EXCLUDED.name,
            status = EXCLUDED.status,
            species = EXCLUDED.species,
            gender = EXCLUDED.gender,
            episodes = EXCLUDED.episodes;
    """, character_data_list)


# updating data in a table locations
def insert_locations(cursor, location_data):
    for location in location_data:
        name = location['name']
        type = location['type']
        dimension = location['dimension']

        cursor.execute("""
            INSERT INTO locations (name, type, dimension) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (name) DO UPDATE 
            SET type = EXCLUDED.type, dimension = EXCLUDED.dimension
        """, (name, type, dimension))


# updating data in a table episodes
def insert_episodes(cursor, episodes_data):



    for episode in episodes_data:
        name = episode['name']
        air_date = episode['air_date']
        episode_code = episode['episode']
        character_id = [int(character.split("/")[-1]) for character in episode["characters"]]

        cursor.execute("""
            INSERT INTO episodes (name, air_date, episode_code, character_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE
            SET air_date = EXCLUDED.air_date, episode_code = EXCLUDED.episode_code, character_id = EXCLUDED.character_id
        """, (name, air_date, episode_code, character_id))


# getting data from api

def get_rickandmorty_data(data_type):
    output_data = []
    row_data = requests.get(f'https://rickandmortyapi.com/api/{data_type}').json()
    output_data.extend(row_data['results'])
    urls = [f'https://rickandmortyapi.com/api/{data_type}?page={url_}' for url_ in
            range(2, (row_data['info']['pages'] + 1))]
    for page in urls:
        page_info = requests.get(page).json()
        output_data.extend(page_info['results'])
    return output_data


# connect to database and using functions to check or create tables and update them
def main():
    logging.info("Starting the script")

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port
    )
    with connection.cursor() as cursor:
        logging.info("Checking or creating tables")

        create_characters_table(cursor)
        create_locations_table(cursor)
        create_episodes_table(cursor)

    connection.commit()

    logging.info("Getting data from API")


    character_data = get_rickandmorty_data('character')
    location_data = get_rickandmorty_data('location')
    episodes_data = get_rickandmorty_data('episode')

    with connection.cursor() as cursor:
        logging.info("Inserting character data")

        insert_characters(cursor, character_data)

    with connection.cursor() as cursor:
        logging.info("Inserting location data")

        insert_locations(cursor, location_data)

    with connection.cursor() as cursor:
        logging.info("Inserting episode data")

        insert_episodes(cursor, episodes_data)
    logging.info("All data updated")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()

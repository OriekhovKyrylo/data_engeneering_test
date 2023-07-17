import psycopg2
import requests
from config import host, user, password, db, port


def main():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port
    )
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS characters(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                status VARCHAR(100),
                species VARCHAR(100),
                gender VARCHAR(100)
            );"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS locations(
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                type VARCHAR(100),
                dimension VARCHAR(100)
            );"""
        )

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS episodes (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                air_date DATE,
                episode VARCHAR(100)
            );"""
        )
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS character_episode (
                character_id INTEGER,
                episode_id INTEGER
            )
        """)

    connection.commit()

    character_data = requests.get('https://rickandmortyapi.com/api/character').json()
    location_data = requests.get('https://rickandmortyapi.com/api/location').json()
    episodes_data = requests.get('https://rickandmortyapi.com/api/episode').json()

    with connection.cursor() as cursor:
        for character in character_data["results"]:
            name = character['name']
            status = character['status']
            species = character['species']
            gender = character['gender']

            cursor.execute("""
                INSERT INTO characters (name, status, species, gender) 
                VALUES (%s, %s, %s, %s) 
                ON CONFLICT (name) DO UPDATE 
                SET status = EXCLUDED.status, species = EXCLUDED.species, gender = EXCLUDED.gender
            """, (name, status, species, gender))

    with connection.cursor() as cursor:
        for location in location_data["results"]:
            name = location['name']
            type = location['type']
            dimension = location['dimension']

            cursor.execute("""
                INSERT INTO locations (name, type, dimension) 
                VALUES (%s, %s, %s) 
                ON CONFLICT (name) DO UPDATE 
                SET type = EXCLUDED.type, dimension = EXCLUDED.dimension
            """, (name, type, dimension))

    with connection.cursor() as cursor:
        for episode in episodes_data["results"]:
            name = episode['name']
            air_date = episode['air_date']
            episode = episode['episode']


            cursor.execute("""
                INSERT INTO episodes (name, air_date, episode)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO UPDATE
                SET air_date = EXCLUDED.air_date, episode = EXCLUDED.episode
                RETURNING id
            """, (name, air_date, episode))


    connection.commit()
    connection.close()


if __name__ == "__main__":
    main()
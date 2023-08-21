import psycopg2
import argparse
from config import host, user, password, db, port


def get_top_characters(connection, value):
    query = """
        SELECT
            c.name AS character_name,
            COUNT(DISTINCT e.id) AS num_episodes
        FROM
            characters c
        JOIN
            episodes e ON c.id = ANY(e.character_id)
        GROUP BY
            c.id, c.name
        HAVING
            (COUNT(DISTINCT e.id) / (SELECT COUNT(*) FROM episodes)) * 100 > %s
        ORDER BY
            num_episodes DESC
        LIMIT 10;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (value,))
        top_characters = cursor.fetchall()
        return top_characters

def get_episodes_with_character(connection, character_id):
    query = """
        SELECT
            e.name AS episode_name
        FROM
            episodes e
        JOIN
            characters c ON c.id = ANY(e.character_id)
        WHERE
            c.id = %s
        ORDER BY
            e.name
        LIMIT 10;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (character_id,))
        episodes_with_character = cursor.fetchall()
        return episodes_with_character

def main():
    parser = argparse.ArgumentParser(description='Process characters and episodes data.')
    parser.add_argument('-value', type=int, choices=range(1, 101),
                        help='Integer must be between 1 and 100')
    parser.add_argument('-type', type=str, choices=['characters', 'episodes'],
                        help='The word must be  characters or  episodes')
    args = parser.parse_args()

    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        port=port)

    if args.type == 'characters':
        top_characters = get_top_characters(conn, args.value)
        print("Top characters:")
        for character, num_episodes in top_characters:
            print(f"{character} - {num_episodes} episodes")

    elif args.type == 'episodes':
        character_id = args.value
        episodes_with_character = get_episodes_with_character(conn, character_id)
        print("Episodes with character:")
        for episode in episodes_with_character:
            print(episode[0])

    conn.close()

if __name__ == "__main__":
    main()
import argparse
import psycopg2

from config import host, user, password, db, port


# connecting to database and getting data
def connect_and_data_database():
    with psycopg2.connect(host=host, user=user, password=password, database=db, port=port) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM episodes;")
            all_episodes = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM characters;")
            all_characters = cursor.fetchall()

    return all_episodes, all_characters


# a function to get a list of characters corresponding to the conditions of the script
def get_most_characters(all_episodes, all_characters, value):
    min_episodes = int(len(all_episodes) * value / 100)
    matching_characters = []
    for character in all_characters:
        if len(character[-1]) > min_episodes:
            matching_characters.append(character)

    top_characters = sorted(matching_characters, key=lambda x: len(x[-1]), reverse=True)
    return top_characters


# a function to get a list of episodes that match the conditions of the script

def get_most_episodes(all_episodes, value):
    matching_episodes = []
    for episode in all_episodes:
        if value in episode[-1]:
            matching_episodes.append(episode)
    top_episodes = sorted(matching_episodes, key=lambda x: x[1])
    return top_episodes


def main():
    # Handling command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-value', type=int, choices=range(1, 101),
                        help='Integer must be between 1 and 100')
    parser.add_argument('-type', type=str, choices=['characters', 'episodes'],
                        help='The word must be  characters or  episodes')
    args = parser.parse_args()

    if args.type == 'characters':
        all_episodes, all_characters = connect_and_data_database()
        result = get_most_characters(all_episodes, all_characters, args.value)
        for row in result[:10]:
            print(row[2], len(row[-1]))
    elif args.type == 'episodes':
        all_episodes, all_characters = connect_and_data_database()

        result = get_most_episodes(all_episodes, args.value)
        for elem in result[:10]:
            print(elem[1])


if __name__ == '__main__':
    main()

import requests
import random
import time
from ram_parse import get_rickandmorty_data

def main():

    request_url_jokes = 'https://v2.jokeapi.dev/joke/Any?amount=7'

    jokes_data = requests.get(request_url_jokes).json()

    character_data = get_rickandmorty_data('character')
    list_of_names = [names['name'] for names in character_data]
    evening_host = random.choice(list_of_names)
    list_of_names.remove(evening_host)

    comics = random.sample(list_of_names, 7)
    print(f"{evening_host} : Hello everyone, today's participants of the show : {', '.join(comics)}:")

    time.sleep(2)

    for joke, speaker in zip(jokes_data['jokes'], comics):
        start_show = input("please tap to enter: ")
        print(f'{evening_host} : say hello to the {speaker} on stage')
        time.sleep(2)
        if joke['type'] == 'twopart':
            print(f"{speaker}: {joke['setup']}")
            time.sleep(2)
            print(f"{joke['delivery']} ")
        if joke['type'] == 'single':
            print(f"{speaker}: {joke['joke']}")

    print(f"{evening_host}: Thank you for the performance of these comedians, so let's vote for the funniest of them")
    time.sleep(3)
    print(f"{evening_host}: Unanimously, the best comedian of today is {random.choice(comics)}")
    end_show = input("please tap to enter: ")


if __name__ == "__main__":
    main()


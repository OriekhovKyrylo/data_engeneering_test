import os
import random
from datetime import date


def main():
    folder_name = 'first_task'

    os.makedirs(folder_name, exist_ok=True)
    random_word = ''
    for _ in range(7):
        random_word += ''.join(random.choice('squanch'))

    current_date = date.today()
    file_name = f"{current_date}_squanch.txt"
    file_path = os.path.join(folder_name, file_name)
    print(file_path)

    with open(file_path, 'w') as file:
        file.write(f"let’s {random_word}")


if __name__ == '__main__':
    main()

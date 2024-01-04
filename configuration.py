import requests
import os
from pathlib import Path
from tkinter import filedialog
from bs4 import BeautifulSoup
from gtts import gTTS


def auto_config() -> str:
    try:
        with open('config/config.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Config file 'config.txt' not found.")
        return str()


def import_from_user_selection(root):
    from warning_window import WarningWindow
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            second_line = file.readline().strip()
        if not is_good_location(file_path):
            dialog = WarningWindow(root, first_line, second_line, file_path)
            root.wait_window(dialog.top)
            file_path = dialog.file_path
            print(file_path)
        with open('config/config.txt', 'w') as file:
            file.write(file_path)
        return file_path
    else:
        return


def download_website_content():
    r = requests.get('https://www.gutenberg.org/cache/epub/36/pg36.txt')
    content = r.text
    with open('books/requested book.txt', 'w') as file:
        file.write(content)

    if r.status_code == 200:
        print('Strona wczytana poprawnie.')


def import_file_to_dictionary(file_path: str) -> dict:
    dictionary = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        if len(content) > 1 and '#separator' in content[0] and '#html' in content[1]:
            for i, line in enumerate(content):
                if (i + 1) % 5 == 0:
                    key = line.strip().strip('"\t"')
                    sentence = BeautifulSoup(content[i + 2], 'html.parser')
                    sentence = sentence.div.string
                    value = [content[i - 2].strip().strip('"'), sentence]
                    dictionary[key] = value

        elif content:
            for line in content:
                if ' : ' in line:
                    parts = line.strip().split(' : ')
                    key = parts[0]
                    value = [parts[1], parts[2]]
                    dictionary[key] = value

        else:
            return dictionary

        return dictionary
    except FileNotFoundError or IndexError:
        print('FileNotFoundError or IndexError')


def courses_list():
    destination_folder = 'lessons/'
    files = os.listdir(destination_folder)
    files = [file.split('.txt')[0] for file in files if '.txt' in file]
    with open('config/courses_list', 'r') as file:
        lines = file.readlines()
        lines = [line.strip('\n') for line in lines]

    for file in files:
        if file not in lines:
            lines = [file] + lines

    lines = [line for line in lines if line in files]
    save_to_courses_list(lines)

    return lines


def save_to_courses_list(courses):
    with open('config/courses_list', 'w') as file:
        for course in courses:
            file.write(course + '\n')


def courses_list_update(selected):
    with open('config/courses_list', 'r') as file:
        courses = [course.strip() for course in file.readlines()]

    for course in courses:
        if selected in course:
            courses = [course for course in courses if selected not in course]
            courses = [course] + courses

    return courses


def save_to_config_file(file_path):
    with open('config/config.txt', 'w') as file:
        file.write(file_path)


def save_word_list(file_path: str, dictionary: dict):
    formatted_text = ""
    for key, value in dictionary.items():
        formatted_text += f'{key} : {value[0]} : {value[1]}{'\n'}'

    with open(file_path, "w") as file:
        file.write('###LiviaApp###\n')
        file.write(formatted_text)


def pronunciation(text: str):
    """
    Przekształca podany tekst na mowę i odtwarza go jako plik dźwiękowy.

    :param text: Tekst do przekształcenia na mowę.
    :type text: str
    """
    language = 'en'
    text_to_speech = gTTS(text=text, lang=language, slow=False)

    text_to_speech.save("config/pronunciation.mp3")

    os.system("afplay config/pronunciation.mp3")


def is_good_location(file_path):
    program_location = os.getcwd()
    correct_location = program_location + "/lessons/"
    file_name = Path(file_path).name
    if correct_location + file_name != file_path:
        return False
    else:
        return True

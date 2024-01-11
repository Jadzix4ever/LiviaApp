import os
from bs4 import BeautifulSoup
from gtts import gTTS

import book_configuration


def auto_config() -> str:
    """
    :return:
    Zwraca ścieżkę pliku z kursem zapisaną do 'config/config.txt'.
    """
    try:
        with open('config/config.txt', 'r') as file:
            return file.readline()
    except FileNotFoundError:
        print("Config file 'config.txt' not found.")
        return str()


def import_courses_list() -> list:
    """
    :return:
    Zwraca listę z wszystkimi aktualnymi kursami.
    """
    destination_folder = 'lessons/'
    files = os.listdir(destination_folder)

    # Tworzenie listy wszystkich kursów znajdujących się w folderze 'lessons/'.
    files = [file.split('.txt')[0] for file in files if '.txt' in file]

    # Wczytanie do zmiennej courses listy wszystkich kursów z pliku 'config/courses_list'.
    with open('config/courses_list', 'r') as file:
        courses = file.readlines()
        courses = [course.strip('\n') for course in courses]

    # Sprawdzenie, czy wszystkie pliki z kursami znajdujące się w folderze są w courses.
    for file in files:
        if file not in courses:
            courses = [file] + courses

    # Sprawdzenie, czy w courses nie ma kursów, których nie ma w folderze.
    courses = [course for course in courses if course in files]
    save_courses_list_to_file(courses)

    return courses


def save_courses_list_to_file(courses: list):
    """
    Zapisuje listę kursów do pliku 'config/courses_list'.

    :param courses:  Lista z nazwami kursów.
    """
    with open('config/courses_list', 'w') as file:
        for course in courses:
            file.write(course + '\n')


def import_flashcards_to_dictionary(file_path: str) -> dict or None:
    """
    Wczytuje wszystkie fiszki z pliku z danym kursem do słownika i sprawdza układ znaków w danym pliku,
    ponieważ w programie również działają kursy wyeksportowane do pliku z programu Anki.

    :param file_path: Ścieżka do pliku.
    :return:
    Zwraca słownik z fiszkami w formie:
    {'słowo(question)': ['słowo(answer)', 'zdanie', 'tłumaczenie zdania']}.
    """
    dictionary = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Sprawdzam, czy plik pochodzi z Anki:
        if len(content) > 1 and '#separator' in content[0] and '#html' in content[1]:
            for i, line in enumerate(content):
                if (i + 1) % 5 == 0:
                    key = line.strip().strip('"\t"')
                    sentence = BeautifulSoup(content[i + 2], 'html.parser')
                    sentence = sentence.div.string
                    if sentence is None:
                        sentence = 'None'
                    value = [content[i - 2].strip().strip('"'), sentence, 'None']
                    dictionary[key] = value

            # Sprawdzenie, czy plik znajduje się w folderze z kursami.
            if '/LiviaApp/lessons/' not in file_path:
                file_name = os.path.basename(file_path)
                file_path = 'lessons/' + file_name

            # Od razu zapisuję plik z nowym układem znaków.
            save_flashcards(file_path, dictionary)

        # Sprawdzam, czy plik pochodzi z programu Livia.
        elif content and '###LiviaApp###' in content[0]:
            for line in content:
                if ' : ' in line:
                    parts = line.split(' : ')
                    key = parts[0]
                    if len(parts) < 4:
                        parts.append('')
                    parts[3] = parts[3].replace('\n', '')
                    value = [parts[1], parts[2], parts[3]]
                    dictionary[key] = value

        # Zwracam pusty słownik, jeżeli układ znaków jest niewłaściwy.
        else:
            return None

        return dictionary

    except FileNotFoundError:
        print('FileNotFoundError')


def save_flashcards(file_path: str, dictionary: dict):
    """
    Zapisuje słownik do pliku w odpowiedniej formie.

    :param file_path: Ścieżka do pliku.
    :param dictionary: Słownik z fiszkami.
    """
    formatted_text = ""
    for key, value in dictionary.items():
        formatted_text += f'{key} : {value[0]} : {value[1]} : {value[2]}\n'

    with open(file_path, "w") as file:
        file.write('###LiviaApp###\n')
        file.write(formatted_text)


def courses_list_update(selected_course: str) -> list:
    """
    :param selected_course: Nazwa aktualnie wybranego kursu.
    :return:
    Zwraca zaktualizowaną kolejność w liście kursów.
    """
    with open('config/courses_list', 'r') as file:
        courses = [course.strip() for course in file.readlines()]

    for course in courses:
        if selected_course in course:
            courses = [course for course in courses if selected_course not in course]
            courses = [course] + courses

    return courses


def save_to_config_file(file_path):
    """
    Zapisuje ścieżkę do pliku w 'config/config.txt'.

    :param file_path: Ścieżka do pliku.
    """
    with open('config/config.txt', 'w') as file:
        file.write(file_path)


def pronunciation(text: str):
    """
    Przekształca podany tekst na mowę i odtwarza go jako plik dźwiękowy.
    Plik zostaje zapisany do config/pronunciation.mp3

    :param text: Tekst do przekształcenia na mowę.
    """
    language = 'en'
    text_to_speech = gTTS(text=text, lang=language, slow=False)

    text_to_speech.save("config/pronunciation.mp3")

    os.system("afplay config/pronunciation.mp3")


def new_course_create(course_name: str) -> str:
    """
    Tworzy pusty plik (bez fiszek) do kursu.
    :param course_name: Nazwa kursu.
    :return: Zwraca ścieżkę do kursu.
    """
    file_path = os.path.join('lessons', course_name + '.txt')
    with open(file_path, 'w') as file:
        file.write("###LiviaApp###\n")
    print('Plik ' + file_path + ' został utworzony.')

    return file_path


def search_sentence(book_content: str, current_word: str) -> list:
    """
    Funkcja przeszukuje zawartość książki w poszukiwaniu zdań zawierających słowo (question).
    :param book_content: Zawartość książki lub tekstu do kursu.
    :param current_word: Szukane słowo.
    :return: Zwraca listę znalezionych zdań.
    """
    sentences = book_configuration.divide_content_into_sentences(book_content)

    founded_sentences = [sentence.strip() for sentence in sentences if current_word.lower() in sentence.lower()]

    # Usunięcie dodatkowych spacji, które mogły powstać po podziale na zdania.
    for i in range(len(founded_sentences)):
        sentence = founded_sentences[i]
        sentence = sentence.replace('  ', ' ')
        founded_sentences[i] = sentence

    return founded_sentences

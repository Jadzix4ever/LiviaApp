import re


def book_import(book_name: str) -> list or None:
    """
    Importuje zawartość książki lub tekstu do kursu z pliku tekstowego.

    :param book_name: Nazwa książki lub tekstu do kursu (nazwa musi być taka sama jak nazwa kursu).
    :return: Lista zawierająca linie tekstu z pliku książki lub None, jeśli plik nie istnieje.
    """
    try:
        with open('lessons/books/' + book_name + '.txt', 'r') as file:
            content = file.readlines()
            return content

    except FileNotFoundError:
        print(f"file lessons/books/{book_name}.txt not found.")


def book_content_checkout(content):
    for line in content:
        if 'START OF THE PROJECT GUTENBERG' in line:
            return True


def book_text_cleaning(content: list) -> tuple:
    """
    Oczyszcza zawartość książki z niepotrzebnych informacji i dzieli ją na spis treści i tekst książki.

    :param content: Lista zawierająca linie tekstu książki
    :return: Krotka ([spis treści], [czysty tekst książki])
    """
    # Sprawdza, czy zawartość przesłanego tekstu pochodzi ze strony gutenberg.org.
    if book_content_checkout(content) is True:
        # Szukanie indeksu początku książki.
        start_index = next((i for i, line in enumerate(content) if 'START OF THE PROJECT GUTENBERG' in line), 0)
        start_index = next(i + start_index + 1 for i, line in enumerate(content[start_index:])
                           if 'content' in line.lower())
        start_index = next(i + start_index for i, line in enumerate(content[start_index:]) if line.strip())

        # Szukanie indeksu końca książki.
        end_index = next((i for i, line in enumerate(content) if
                          'END OF THE PROJECT GUTENBERG EBOOK' in line), len(content))
        end_index = next(end_index - i for i, line in enumerate(reversed(content[:end_index])) if line.strip())

        # Wydzielenie tekstu książki pomiędzy znalezionymi indeksami.
        content = content[start_index:end_index]
        content = [line.strip() for line in content]

        #  Dzielenie zawartości na spis treści (TOC) i czysty tekst poprzez sprawdzenie,
        #  kiedy powtórzy się pierwsza linia.
        toc_index = next((i for i, line in enumerate(content[1:], start=1) if line in content[0] and line.strip()), 0)

        # Usunięcie ewentualnych pustych linii z końca spisu treści, jeżeli spis treści został wyodrębniony.
        toc = content[:toc_index]
        if toc:
            while not toc[-1].strip():
                toc.pop()

        # Usunięcie ewentualnych pustych linii z początku tekstu książki.
        text = content[toc_index:]
        while not text[0].strip():
            text.pop(0)

        content = (toc, text)

        return content

    else:
        content = [line.strip() for line in content]
        content = ([], content)

        return content


def words_separated(text: list) -> list:
    """
    Łączy listę fraz w jeden ciąg znaków, a następnie dzieli go na słowa i zwraca jako listę.

    :param text: Lista fraz do przetworzenia.
    :return: Lista słów.
    """
    text = ' '.join(text)
    words = text.split()

    return words


def word_and_sentence_pairs(book_label_positions: dict, page: int) -> list:
    """
    Tworzy listę zdań na podstawie pozycji etykiet na danej stronie książki.
    W funkcji wykorzystywane są 3 odrębne funkcje do uzyskania całych zdań dla poszczególnych słów:
    create_sentences_for_page, find_last_sentence, find_first_sentence.

    :param book_label_positions: Słownik przechowujący współrzędne etykiet (słów) na poszczególnych stronach książki.
    :param page: Numer strony, dla której tworzone są zdania.
    :return: Lista par, które są listą dwuelementową ['słowo', 'zdanie']
    """
    # Stworzenie listy zdań dla danej strony.
    sentences = create_sentences_for_page(book_label_positions, page)

    # Szukanie ostatniego zdania.
    try:
        if type(sentences[-1]) is list and book_label_positions[str(page + 1)]:
            last_sentence = find_last_sentence(sentences[-1], book_label_positions, page)
            sentences.pop()
            sentences.append(last_sentence)

    except KeyError:
        print(f"Key {page + 1} doesn't exist in 'book'.")

    # Szukanie pierwszego zdania.
    if page > 1:
        first_sentence = find_first_sentence(sentences[0], book_label_positions, page)
        sentences[0] = first_sentence

    # Łączenie słów i zdań w pary jako dwuelementowe listy w liście pairs.
    pairs = []
    number = 0
    for word in book_label_positions[str(page)]:
        if '.' in word[0]:
            pairs.append([word[0], sentences[number]])
            number += 1
        else:
            pairs.append([word[0], sentences[number]])

    return pairs


def create_sentences_for_page(book_label_positions: dict, page: int) -> list:
    """
    Tworzy listę zdań na podstawie pozycji etykiet na danej stronie książki.

    Przechodzi przez listę etykiet (słów) na danej stronie, łącząc je w zdania.
    Nowe zdanie rozpoczyna się, gdy słowo zawiera kropkę ('.').

    :param book_label_positions: Słownik przechowujący współrzędne etykiet (słów) na poszczególnych stronach książki.
    :param page: Numer strony, dla której tworzone są zdania.
    :return: Lista zdań i lista słow w tej liście jako ostatni element, jeżeli na końcu nie było kropki ('.').
    """
    number = 0
    sentences = [[]]
    for word in book_label_positions[str(page)]:
        if '.' in word[0]:
            sentences[number].append(word[0])
            sentences[number] = ' '.join(sentences[number])
            number += 1
            sentences.append([])
        else:
            sentences[number].append(word[0])

    return sentences


def find_last_sentence(first_part: list, book_label_positions: dict, page: int) -> str:
    """
    Dodawanie słów z następnej strony do listy second_part do momentu znalezienia kropki ('.').
    Połączenie list first_part i second_part i następnie powstałych fraz w jedno zdanie.

    :param first_part: Lista słów z ostatniego zdania, w którym nie było kropki.
    :param book_label_positions: Słownik przechowujący współrzędne etykiet (słów) na poszczególnych stronach książki.
    :param page: Numer strony, dla której tworzone są zdania.
    :return: Ostatnie zdanie jako string.
    """
    second_part = []
    for word in book_label_positions[str(page + 1)]:
        if '.' in word[0]:
            second_part.append(word[0])
            break
        else:
            second_part.append(word[0])

    first_part = ' '.join(first_part)
    second_part = ' '.join(second_part)

    last_sentence = first_part + ' ' + second_part

    return last_sentence


def find_first_sentence(second_part, book_label_positions: dict, page: int) -> str:
    """
    Dodawanie słów z poprzedniej strony do zmiennej typu string do momentu znalezienia kropki ('.').
    Połączenie fraz w jedno zdanie.
    :param second_part: Pierwsze zdanie z danej strony.
    :param book_label_positions: Słownik przechowujący współrzędne etykiet (słów) na poszczególnych stronach książki.
    :param page: Numer strony, dla której tworzone są zdania.
    :return: Pierwsze zdanie jako string.
    """
    first_part = ''
    for word in reversed(book_label_positions[str(page - 1)]):
        # Sprawdzenie, czy ostatnie słowo z poprzedniej strony kończyło się kropką.
        if '.' in word[0]:
            break
        else:
            first_part = word[0] + ' ' + first_part

    # Upewnienie się, że second_part to string. Może się tak zdarzyć, jeżeli cały tekst nie kończy się kropką.
    if type(second_part) is list:
        second_part = ' '.join(second_part)

    first_sentence = first_part.strip() + ' ' + second_part
    return first_sentence


def divide_content_into_sentences(content: str) -> list:
    """
    Dzieli zawartość tekstu na zdania przy użyciu wyrażenia regularnego.

    Wyrażenie regularne:
    - (?<!\\w\\.\\w.): Negative lookbehind, sprawdza, czy przed "." nie ma kropki w środku słowa.
    - (?<![A-Z][a-z]\\.): Negative lookbehind, sprawdza, czy przed "." nie ma skrótu z jedną dużą i jedną małą literą.
    - (?<=[.?]): Positive lookbehind, sprawdza, czy przed spacją jest "." lub "?".

    :param content: Tekst, który ma zostać podzielony na zdania.
    :return: Lista zawierająca zdania podzielone z tekstu.
    """
    sentences = re.split(r'(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=[.?])\s', content)
    return sentences

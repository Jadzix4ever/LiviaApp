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
        toc_index = next(i for i, line in enumerate(content[1:]) if line in content[0] and line.strip())

        # Usunięcie ewentualnych pustych linii z końca spisu treści.
        toc = content[:toc_index]
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
    Funkcja przyjmuje listę fraz ('text'), łączy je w jeden ciąg znaków,
    a następnie dzieli ten ciąg na pojedyncze słowa. Ostatecznie zwraca listę słów.

    :param text: Lista fraz do przetworzenia.

    :return: Lista słów.
    """
    text = ' '.join(text)
    words = text.split()

    return words


def word_and_sentence(book, page):
    sentences = create_sentences_for_page(book, page)
    try:
        if type(sentences[-1]) is list and book[str(page + 1)]:
            last_sentence = find_last_sentence(sentences[-1], book, page)
            sentences.pop()
            sentences.append(last_sentence)
    except KeyError:
        print(f"Key {page + 1} doesn't exist in 'book'.")

    last_word = book[str(page)][-1]

    if page > 1 and '.' not in last_word[0]:
        first_sentence = find_first_sentence(sentences[0], book, page)
        sentences[0] = first_sentence

    pairs = []
    number = 0
    for word in book[str(page)]:
        if '.' in word[0]:
            pairs.append([word[0], sentences[number]])
            number += 1
        else:
            pairs.append([word[0], sentences[number]])

    return pairs


def create_sentences_for_page(book, page):
    number = 0
    sentences = [[]]  # Rozpoczynamy od jednej pustej listy
    for word in book[str(page)]:
        if '.' in word[0]:
            sentences[number].append(word[0])
            sentences[number] = ' '.join(sentences[number])
            number += 1
            sentences.append([])  # Dodaj nową pustą listę na nowe zdanie
        else:
            sentences[number].append(word[0])

    return sentences


def find_last_sentence(first_part, book, page):
    first_part = ' '.join(first_part)

    last_sentence = [[]]

    number = 0
    for word in book[str(page + 1)]:
        if '.' in word[0]:
            last_sentence[number].append(word[0])
            last_sentence[number] = ' '.join(last_sentence[number])
            break
        else:
            last_sentence[number].append(word[0])

    second_part = last_sentence[0]

    last_sentence = first_part + ' ' + second_part
    return last_sentence


def find_first_sentence(second_part, book, page):
    first_sentence = [[]]

    number = 0
    for word in reversed(book[str(page - 1)]):
        if '.' not in word[0]:
            if '.' in word[0]:
                first_sentence[number] = ' '.join(first_sentence[number])
                break
            else:
                first_sentence[number] = [word[0]] + first_sentence[number]
        else:
            break

    if first_sentence[0]:
        first_part = ' '.join(first_sentence[0])
        first_sentence = first_part + ' ' + second_part
        return first_sentence

    else:
        return ''


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

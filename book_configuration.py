def book_import(book_name):
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


def book_text_cleaning(content):
    content = content
    if book_content_checkout(content) is True:
        start_index = next((i for i, line in enumerate(content) if 'START OF THE PROJECT GUTENBERG' in line), 0)
        start_index = next(i + start_index + 1 for i, line in enumerate(content[start_index:])
                           if 'content' in line.lower())
        start_index = next(i + start_index for i, line in enumerate(content[start_index:]) if line.strip())

        end_index = next((i for i, line in enumerate(content) if
                          'END OF THE PROJECT GUTENBERG EBOOK' in line), len(content))
        end_index = next(end_index - i for i, line in enumerate(reversed(content[:end_index])) if line.strip())
        content = content[start_index:end_index]
        content = [line.strip() for line in content]

        toc_index = next(i for i, line in enumerate(content[1:]) if line in content[0] and line.strip())

        toc = content[:toc_index]
        while not toc[-1].strip():
            toc.pop()

        text = content[toc_index:]
        while not text[0].strip():
            text.pop(0)

        content = [toc, text]

        return content

    else:
        content = [line.strip() for line in content]
        content = [[], content]
        return content


def words_separated(text):
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

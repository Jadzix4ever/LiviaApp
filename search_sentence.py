import tkinter as tk

import book_configuration
import configuration
from ui import center_window, create_label, create_button
import open_ai


class AddSentence:
    def __init__(self, root, current_question_word: str, book_content, file_path: str, dictionary: dict,
                 founded_sentences, course_name: str, show_translated_sentence: int):
        """
        Klasa reprezentująca okno do wyszukiwania zdań w tekście zawierających dane słowo (question).

        :param root: Uchwyt do okna.
        :param current_question_word: Aktualne słowo (question), dla którego są szukane zdania.
        :param book_content: Lista zawierająca zawartość książki, podzieloną na zdania.
        :param file_path: Ścieżka do pliku z fiszkami.
        :param dictionary: Słownik przechowujący fiszki.
        :param course_name: Tytuł książki z autorem lub nazwa kursu.
        :param show_translated_sentence: Liczba pomocnicza do ukrywania tłumaczenia zdania.
        """
        self.top = tk.Toplevel(root)

        center_window(self.top, 350, 400)

        self.current_word = current_question_word
        self.book_content = book_content
        self.founded_sentences = founded_sentences
        self.length_search_sentences = len(self.founded_sentences)
        self.current_sentence = dictionary[self.current_word][1]
        self.translated_sentence = dictionary[self.current_word][2]
        self.show_translated_sentence = show_translated_sentence

        create_label(self.top, 'for "' + self.current_word + '" founded: ' + str(self.length_search_sentences), 'top')
        if self.show_translated_sentence:
            create_button(self.top, 'Generate translation', self.generate_translation, 'pack', {'side': 'top'})
        self.original_sentence_label = create_label(self.top, '', 'Arial', 340, 'pack', {'side': 'top'})
        if self.show_translated_sentence:
            self.translate_label = create_label(self.top, self.translated_sentence, 'Arial', 340,
                                                'pack', {'side': 'top'})
        self.next_button = create_button(self.top, 'Next', self.next_sentence, 'pack', {'side': 'bottom'})
        self.save_button = create_button(self.top, 'Save', self.save_to_flashcards, 'pack', {'side': 'bottom'})

        self.file_path = file_path
        self.dictionary = dictionary
        self.course_name = course_name
        self.current_index = 0

        # Wyświetlenie pierwszego zdania.
        self.next_sentence()

    def search_sentence(self):
        """
        Funkcja przeszukuje zawartość książki w poszukiwaniu zdań zawierających słowo (question).
        """
        self.book_content = ' '.join(self.book_content)
        sentences = book_configuration.divide_content_into_sentences(self.book_content)

        self.founded_sentences = [sentence.strip() for sentence in sentences if self.current_word.lower() in
                                  sentence.lower()]

        # Usunięcie dodatkowych spacji, które mogły powstać po podziale na zdania.
        for i in range(len(self.founded_sentences)):
            sentence = self.founded_sentences[i]
            sentence = sentence.replace('  ', ' ')
            self.founded_sentences[i] = sentence

        self.length_search_sentences = len(self.founded_sentences)

    def next_sentence(self):
        """
        Funkcja wyświetla kolejne zdanie, sprawdza, czy jest w fiszkach i aktualizuje interfejs użytkownika.
        """
        if self.length_search_sentences < 2:
            self.next_button.config(state=tk.DISABLED)

        if self.length_search_sentences and self.length_search_sentences > self.current_index:
            # Szukanie miejsca w książce, w którym znajduje się zdanie (wyrażone w procentach).
            index = self.book_content.find(self.founded_sentences[self.current_index])
            percent = (index + 1) / (len(self.book_content) + 1) * 100

            self.original_sentence_label.config(text=str(self.founded_sentences[self.current_index]) + '\n\n' + str(
                round(percent, 1)) + '%' + f'\t{self.current_index + 1}/{self.length_search_sentences}')

            # Zmiana koloru tekstu, jeżeli zdanie jest w fiszkach i wyświetlenie tłumaczenia zdania, jeżeli istnieje.
            if (self.current_sentence and self.current_sentence in self.founded_sentences[self.current_index] or
                    self.founded_sentences[self.current_index] in self.current_sentence):
                self.original_sentence_label.config(fg="green")
                if self.show_translated_sentence:
                    self.translate_label.config(text=self.translated_sentence)

            else:
                self.original_sentence_label.config(fg="systemTextColor")
                if self.show_translated_sentence:
                    self.translate_label.config(text='')

            self.current_index += 1

        else:
            self.current_index = 0
            self.next_sentence()

    def save_to_flashcards(self):
        """
        Funkcja dodaje aktualne zdanie do fiszek, zapisuje zmiany i aktualizuje interfejs użytkownika.
        """
        self.save_button.config(state=tk.DISABLED)
        self.current_sentence = self.founded_sentences[self.current_index - 1]
        self.dictionary[self.current_word][1] = self.founded_sentences[self.current_index - 1]
        self.dictionary[self.current_word][2] = self.translated_sentence
        configuration.save_flashcards(self.file_path, self.dictionary)

    def generate_translation(self):
        """
        Funkcja generuje tłumaczenie aktualnego zdania przy użyciu API OpenAI.
        """
        if ' by ' in self.course_name:
            self.save_button.config(state=tk.NORMAL)
            title, author = self.course_name.split(' by ')
            self.translated_sentence = open_ai.book_sentence_translation(title, author, self.founded_sentences[self.
                                                                         current_index - 1], self.current_word)
            self.translate_label.config(text=self.translated_sentence)
            self.next_button.config(state=tk.DISABLED)

        else:
            pass

import tkinter as tk
from tkinter import messagebox
import random
import re

import ui
import search_sentence
import configuration
import book_configuration


class CourseDialog:
    def __init__(self, root, dictionary: dict, file_path: str, course_name: str):
        """
        Klasa reprezentująca okno do przepytywania i sprawdzania odpowiedzi.

        :param root: Uchwyt do głównego okna.
        :param dictionary: Słownik zawierający fiszki do kursu.
        :param file_path: Ścieżka do pliku z fiszkami.
        :param course_name: Nazwa kursu.
        """
        self.top = tk.Toplevel(root)

        ui.center_window(self.top, 550, 400)

        self.dictionary = dictionary
        self.copy_dictionary = dictionary.copy()   # Kopia do usuwania dobrych odpowiedzi podczas przepytywania.
        self.question_word = random.choice(list(self.copy_dictionary.keys()))   # Wylosowanie słowa z kluczy w słowniku.
        self.show_translated_sentence = 0   # Liczba pomocnicza do wyświetlenia tłumaczenia zdania.

        frame_top = ui.create_frame(self.top, 'top')
        ui.create_button(frame_top, 'Pronunciation', self.pronunciation_word, 'pack', {'side': 'left'})
        ui.create_button(frame_top, 'Reverse', self.reverse, 'pack', {'side': 'left'})
        self.question_label = ui.create_label(self.top, self.question_word, ('Helvetica', 18), 440, 'pack',
                                              {'side': 'top'})
        self.answer_label = ui.create_label(self.top, 'Your answer:', 'Helvetica', 440, 'pack', {'side': 'top'})
        self.entry = ui.create_entry(self.top, 'top')
        self.frame_bottom = ui.create_frame(self.top, 'bottom')
        self.next_button = ui.create_button(self.frame_bottom, 'Next', self.show_next_question,
                                            'pack', {'side': 'left'})
        self.check_button = ui.create_button(self.frame_bottom, 'Check', self.check_answer, 'pack', {'side': 'left'})
        self.search_sentence_button = ui.create_button(self.frame_bottom, 'Search sentence', self.search_sentence,
                                                       'pack', {'side': 'left'})
        self.play_sentence_button = None

        self.file_path = file_path
        self.book_content = book_configuration.book_import(course_name)
        if self.book_content:
            _, self.book_content = book_configuration.book_text_cleaning(self.book_content)
        self.course_name = course_name

        self.reverse_number = 1     # Zmienna kontrolująca tryb odwrócony
        self.answer_word = self.copy_dictionary[self.question_word][0]
        self.sentence = self.copy_dictionary[self.question_word][1]

    def reverse(self):
        """
        Tryb odwrócony — odwraca pytanie i odpowiedź.
        """
        self.reverse_number += 1

        if self.reverse_number % 2 != 0:
            self.question_label.config(text=self.question_word)
            self.search_sentence_button.config(state=tk.ACTIVE)
        else:
            self.question_label.config(text=self.answer_word)
            self.search_sentence_button.config(state=tk.DISABLED)

    def show_next_question(self):
        """
        Wyświetla kolejne pytanie i przywraca domyślne ustawienia.
        """
        self.next_button.config(text='Next')

        try:
            self.play_sentence_button.destroy()
        except AttributeError:
            print('NoneType')

        # Ustawiam wartość na False w celu wyświetlania tłumaczenia zdania w klasie search_sentence.AddSentence.
        self.show_translated_sentence = 0

        self.check_button.config(state=tk.NORMAL)
        self.answer_label.config(text="Your answer:")
        self.check_button.config(text='Check', command=self.check_answer)
        self.search_sentence_button.config(text='Search sentence', command=self.search_sentence)

        # Wylosowanie fiszki.
        self.question_word = random.choice(list(self.copy_dictionary.keys()))
        self.answer_word = self.copy_dictionary[self.question_word][0]
        self.sentence = self.copy_dictionary[self.question_word][1]

        if self.reverse_number % 2 != 0:
            self.question_label.config(text=self.question_word, fg='systemTextColor')
        else:
            self.question_label.config(text=self.answer_word, fg='systemTextColor')
            self.search_sentence_button.config(state=tk.DISABLED)

        self.entry.delete(0, tk.END)

    def search_sentence(self):
        """
        Wywołuje wyszukiwanie zdania dla aktualnego słowa i aktualizuje słownik z fiszkami i aktualne zdanie.
        """
        if self.book_content:
            book_content = ' '.join(self.book_content)

            # Wyszukiwanie zdań zawierających słowo kluczowe.
            founded_sentences = configuration.search_sentence(book_content, self.question_word)

            if founded_sentences:
                dialog_window = search_sentence.AddSentence(self.top, self.question_word, book_content,
                                                            self.file_path, self.dictionary, founded_sentences,
                                                            self.course_name, self.show_translated_sentence)
                self.top.wait_window(dialog_window.top)
                self.dictionary = dialog_window.dictionary
                self.sentence = self.dictionary[self.question_word][1]

                if self.show_translated_sentence:
                    if self.reverse_number % 2 != 0:
                        self.answer_label.config(text=f"{self.answer_word}{'\n'} Sentence: {self.sentence}")
                    else:
                        self.answer_label.config(text=f"{self.question_word}{'\n'} Sentence: {self.sentence}")

            else:
                messagebox.showinfo("No sentences.", f"No sentences founded.")

        else:
            messagebox.showinfo("No file in books", f"No file for {self.course_name}.")

    def check_answer(self):
        """
        Sprawdza odpowiedź użytkownika i aktualizuje etykiety.
        """
        # Ustawiam wartość na True w celu wyświetlania tłumaczenia zdania w klasie search_sentence.AddSentence.
        self.show_translated_sentence = 1
        user_answer = self.entry.get()

        # Wyrażenie regularne usuwa wszystkie treści w nawiasach okrągłych z self.answer_word lub self.question_word
        if self.reverse_number % 2 != 0:
            cleaned_words = re.sub(r'\([^)]*\)', '', self.answer_word)
        else:
            cleaned_words = re.sub(r'\([^)]*\)', '', self.question_word)

        # Wyrażenie regularne dzieli w miejscach, gdzie występuje przecinek lub średnik i usuwa po nich białe znaki.
        # Oczyszczone słowa są dzielone na listę, usuwając ewentualne puste elementy.
        words = [word.strip() for word in re.split(r'[;,]\s*', cleaned_words) if word]

        # Sprawdzenie poprawnych odpowiedzi.
        answer_correct = []
        for word in words:
            if word in user_answer:
                answer_correct.append(word.lower())

        if self.reverse_number % 2 != 0:

            if answer_correct:
                self.question_label.config(text=self.question_word + '\n' + ', '.join(answer_correct), fg="green")
                if len(self.copy_dictionary) > 1:
                    self.copy_dictionary.pop(self.question_word)
                else:
                    messagebox.showinfo("THE END.", f"End of the flashcards.")
            self.answer_label.config(text=f"{self.answer_word}{'\n'} Sentence: {self.sentence}")

        else:
            if answer_correct:
                self.question_label.config(text=self.answer_word + '\n' + ', '.join(answer_correct), fg="green")
                if len(self.copy_dictionary) > 1:
                    self.copy_dictionary.pop(self.question_word)
                else:
                    messagebox.showinfo("THE END.", f"End of the flashcards.")
            self.answer_label.config(text=f"{self.question_word}{'\n'} Sentence: {self.sentence}")

        if self.sentence:
            self.play_sentence_button = ui.create_button(self.frame_bottom, 'Play', self.pronunciation_sentence,
                                                         'pack', {'side': 'right', 'anchor': 'se'}, width=4)

        if not answer_correct:
            self.check_button.config(text='Repetitions', command=self.add_to_repetitions)

        else:
            self.next_button.config(text='Easy')
            self.check_button.config(state=tk.DISABLED)

    def add_to_repetitions(self):
        # W trakcie tworzenia
        """
        Dodaje aktualne słowo do powtórek.
        """
        pass

    def pronunciation_word(self):
        """
        Odtwarza wymowę aktualnego słowa.
        """
        configuration.pronunciation(self.question_word)

    def pronunciation_sentence(self):
        """
        Odtwarza wymowę aktualnego zdania.
        """
        configuration.pronunciation(self.sentence)

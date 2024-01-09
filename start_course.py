import os
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
        :param root: Uchwyt do głównego okna.
        :param dictionary: Słownik zawierający fiszki do kursu.
        :param file_path: Ścieżka do pliku kursu.
        :param course_name: Nazwa kursu.
        """
        self.top = tk.Toplevel(root)

        ui.center_window(self.top, 550, 400)

        self.dictionary = dictionary
        self.question_word = random.choice(list(self.dictionary.keys()))    # Wylosowanie słowa z kluczy w słowniku.

        frame_top = ui.create_frame(self.top, 'top')
        ui.create_button(frame_top, 'Pronunciation', self.pronunciation_word, 'pack', {'side': 'left'})
        ui.create_button(frame_top, 'Reverse', self.reverse, 'pack', {'side': 'left'})
        self.question_label = ui.create_label(self.top, self.question_word, ('Helvetica', 18), 440, 'pack',
                                              {'side': 'top'})
        self.answer_label = ui.create_label(self.top, 'Your answer:', 'Helvetica', 440, 'pack', {'side': 'top'})
        self.entry = ui.create_entry(self.top, 'top')
        self.frame_bottom = ui.create_frame(self.top, 'bottom')
        ui.create_button(self.frame_bottom, 'Next', self.show_next_question, 'pack', {'side': 'left'})
        self.check_button = ui.create_button(self.frame_bottom, 'Check', self.check_answer, 'pack', {'side': 'left'})
        self.search_sentence_button = ui.create_button(self.frame_bottom, 'Search sentence', self.search_sentence,
                                                       'pack', {'side': 'left'})
        self.play_sentence_button = None

        self.file_path = file_path
        self.book_content = book_configuration.book_import(course_name)
        self.book_content = book_configuration.book_text_cleaning(self.book_content)
        self.course_name = course_name

        self.reverse_number = 1     # Zmienna kontrolująca tryb odwrócony
        self.answer_word = self.dictionary[self.question_word][0]
        self.sentence = self.dictionary[self.question_word][1]

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
        try:
            self.play_sentence_button.destroy()
        except AttributeError:
            print('NoneType')

        self.answer_label.config(text="Your answer:")
        self.check_button.config(text='Check', command=self.check_answer)
        self.search_sentence_button.config(text='Search sentence', command=self.search_sentence)

        self.question_word = random.choice(list(self.dictionary.keys()))
        self.answer_word = self.dictionary[self.question_word][0]
        self.sentence = self.dictionary[self.question_word][1]

        if self.reverse_number % 2 != 0:
            self.question_label.config(text=self.question_word, fg='systemTextColor')
        else:
            self.question_label.config(text=self.answer_word, fg='systemTextColor')
            self.search_sentence_button.config(state=tk.DISABLED)

        self.entry.delete(0, tk.END)

    def search_sentence(self):
        """
        Wywołuje wyszukiwanie zdania dla aktualnego słowa i aktualizuje dane.
        """
        try:
            dialog_window = search_sentence.AddSentence(self.top, self.question_word, self.book_content[1],
                                                        self.file_path, self.dictionary, self.course_name)
            self.top.wait_window(dialog_window.top)
            self.dictionary = dialog_window.dictionary
            self.sentence = self.dictionary[self.question_word][1]

        except FileNotFoundError:
            print('FileNotFoundError')
            messagebox.showinfo("No file in books", f"No file for {self.course_name}.")

    def check_answer(self):
        """
        Sprawdza odpowiedź użytkownika i aktualizuje etykiety.
        """
        user_answer = self.entry.get()
        answer_correct = []

        if self.reverse_number % 2 != 0:
            cleaned_words = re.sub(r'\([^)]*\)', '', self.answer_word)
        else:
            cleaned_words = re.sub(r'\([^)]*\)', '', self.question_word)

        words = [word.strip() for word in re.split(r'[;,]\s*', cleaned_words) if word]

        for word in words:
            if word in user_answer:
                answer_correct.append(word.lower())

        if self.reverse_number % 2 != 0:

            if answer_correct:
                self.question_label.config(text=self.question_word + '\n' + ', '.join(answer_correct), fg="green")
            self.answer_label.config(text=f"{self.answer_word}{'\n'} Sentence: {self.sentence}")

        else:
            if answer_correct:
                self.question_label.config(text=self.answer_word + '\n' + ', '.join(answer_correct), fg="green")
            self.answer_label.config(text=f"{self.question_word}{'\n'} Sentence: {self.sentence}")

        if self.sentence:
            self.play_sentence_button = ui.create_button(self.frame_bottom, 'Play', self.pronunciation_sentence,
                                                         'pack', {'side': 'right', 'anchor': 'se'}, width=4)

        if not answer_correct:
            pass
            # self.check_button.config('repetitions', command=self.add_to_repetitions)

    def add_to_repetitions(self):
        """
        Dodaje aktualne słowo do powtórek.
        """
        file_name = os.path.basename(self.file_path)
        review_dir = "lessons/review/"
        if not os.path.exists(review_dir):
            os.makedirs(review_dir)
        if 'review' in file_name:
            file_path = os.path.join(review_dir + file_name)
        else:
            file_path = os.path.join(review_dir + 'review' + file_name)
        with open(file_path, 'a+') as file:
            file.seek(0)
            content = file.read()
            file.seek(0, 2)
        # if self.reverse_number % 2 != 0:
            if self.question_word not in content:
                file.write(self.question_word + ' - ' + self.answer_word + '\n')
                file.write(self.sentence + '\n')
            else:
                print(f"{self.question_word} already in review")
        # else:
        #     if self.answer_word not in content:
        #         file.write(self.answer_word + ' - ' + self.question_word + '\n')
        #         file.write(self.sentence + '\n')
        #     else:
        #         print(f"{self.answer_word} already exist")
        self.show_next_question()

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

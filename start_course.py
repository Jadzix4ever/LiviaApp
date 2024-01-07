import os
import tkinter as tk
import random
import re
from tkinter import filedialog
from search_sentence import AddSentence
from configuration import import_flashcards_to_dictionary, pronunciation
from ui import center_window, create_button, create_label, create_entry, create_frame


class CourseDialog:
    def __init__(self, master, dictionary: dict, file_path):
        self.top = tk.Toplevel(master)

        center_window(self.top, 550, 400)

        self.dictionary = dictionary
        self.question_word = random.choice(list(self.dictionary.keys()))

        frame_top = create_frame(self.top, 'top')
        create_button(frame_top, 'Prononciation', self.pronunciation_word, 'pack', {'side': 'left'})
        create_button(frame_top, 'Reverse', self.reverse, 'pack', {'side': 'left'})
        self.question_label = create_label(self.top, self.question_word, ('Helvetica', 18), 440, 'pack',
                                           {'side': 'top'})
        self.answer_label = create_label(self.top, 'Your answer:', 'Helvetica', 440, 'pack', {'side': 'top'})
        self.entry = create_entry(self.top, 'top')
        frame_bottom = create_frame(self.top, 'bottom')
        create_button(frame_bottom, 'Next', self.show_next_question, 'pack', {'side': 'left'})
        self.check_button = create_button(frame_bottom, 'Check', self.check_answer, 'pack', {'side': 'left'})
        self.search_sentence_button = create_button(frame_bottom, 'Search sentence', self.search_sentence,
                                                    'pack', {'side': 'left'})

        self.file_path = file_path
        self.file_path_book = None

        self.reverse_number = 1
        self.answer_word = self.dictionary[self.question_word][0]
        self.sentence = self.dictionary[self.question_word][1]
        # self.generated_sentence_dictionary = {self.dictionary[self.question_word]: self.generated_sentence}

    def reverse(self):
        self.reverse_number += 1

        if self.reverse_number % 2 != 0:
            self.question_label.config(text=self.question_word)
            self.search_sentence_button.config(state=tk.ACTIVE)
        else:
            self.question_label.config(text=self.answer_word)
            self.search_sentence_button.config(state=tk.DISABLED)

    def show_next_question(self):
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
        if not self.file_path_book:
            self.file_path_book = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.file_path_book:
            dialog = AddSentence(self.top, self.question_word, self.file_path_book, self.file_path, self.dictionary)
            self.top.wait_window(dialog.top)  # Poczekaj na zamknięcie okna dialogowego
            self.dictionary = dialog.dictionary
            self.sentence = self.dictionary[self.question_word][1]

    def check_answer(self):
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
            self.answer_label.config(text=f"{self.answer_word}{'\n'}"
                                          f"Sentence: {self.sentence}")
        else:
            if answer_correct:
                self.question_label.config(text=self.answer_word + '\n' + ', '.join(answer_correct), fg="green")
            self.answer_label.config(text=f"{self.question_word}{'\n'}"
                                          f"Sentence: {self.sentence}")

        if self.sentence and self.sentence != 'None':
            print(self.sentence)
            self.search_sentence_button.config(text='Play the sentence', command=self.pronunciation_sentence)

        if not answer_correct:
            pass
            # self.check_button.config('Review this word', command=self.review)

    def review(self):
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
        pronunciation(self.question_word)

    def pronunciation_sentence(self):
        pronunciation(self.sentence)

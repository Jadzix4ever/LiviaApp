import tkinter as tk
import os
import re
from configuration import save_flashcards
from ui import center_window, create_label, create_button
from open_ai import book_sentence_translation


class AddSentence:
    def __init__(self, root, current_question_word, file_path_book, file_path, dictionary):
        self.top = tk.Toplevel(root)

        center_window(self.top, 350, 400)

        self.current_word = current_question_word
        self.file_path_book = file_path_book
        self.search_sentences = []
        self.length_search_sentences = None
        self.book_content = None

        self.search_sentence()

        create_label(self.top, 'for "' + self.current_word + '" founded: ' + str(self.length_search_sentences), 'top')
        create_button(self.top, 'Generate translation', self.generate_translation, 'pack', {'side': 'top'})
        self.original_sentence_label = create_label(self.top, '', 'Arial', 340, 'pack', {'side': 'top'})
        self.translate_label = create_label(self.top, '', 'Arial', 340, 'pack', {'side': 'top'})
        self.next_button = create_button(self.top, 'Next', self.choose_sentence, 'pack', {'side': 'bottom'})
        self.save_button = create_button(self.top, 'Save', self.add_to_sentence_list, 'pack', {'side': 'bottom'})

        self.file_path = file_path
        self.dictionary = dictionary
        self.current_index = 0

        self.choose_sentence()

    def search_sentence(self):
        with open(self.file_path_book, 'r') as file:
            self.book_content = file.read()
            self.book_content = ' '.join(self.book_content.split())

            start_marker = 'START OF THE PROJECT GUTENBERG'
            end_marker = 'END OF THE PROJECT GUTENBERG'

            start_index = self.book_content.find(start_marker)
            end_index = self.book_content.find(end_marker)

            if start_index != -1 and end_index != -1:
                self.book_content = self.book_content[start_index + 30:end_index]

            # noinspection PyUnresolvedReferences
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', self.book_content)
            self.search_sentences = [sentence.strip() for sentence in sentences if self.current_word.lower() in
                                     sentence.lower()]
            self.length_search_sentences = len(self.search_sentences)

    def choose_sentence(self):
        if self.length_search_sentences < 2:
            self.next_button.config(state=tk.DISABLED)
        if self.length_search_sentences:
            if self.length_search_sentences > self.current_index:
                index = self.book_content.find(self.search_sentences[self.current_index])
                percent = (index + 1) / (len(self.book_content) + 1) * 100
                self.original_sentence_label.config(
                    text=str(self.search_sentences[self.current_index]) + '\n' + str(round(percent, 1)) + '%')
                self.current_index += 1
            else:
                self.current_index = 0
                index = self.book_content.find(self.search_sentences[self.current_index])
                percent = (index + 1) / (len(self.book_content) + 1) * 100
                self.original_sentence_label.config(
                    text=str(self.search_sentences[self.current_index]) + '\n' + str(round(percent, 1)) + '%')
                self.current_index += 1

    def add_to_sentence_list(self):
        self.save_button.config(state=tk.DISABLED)
        self.dictionary[self.current_word][1] = self.search_sentences[self.current_index - 1]
        save_flashcards(self.file_path, self.dictionary)

    def generate_translation(self):
        pass
        # language = 'Polish'
        # book_name = os.path.basename(self.file_path)
        # book_name = os.path.splitext(book_name)[0]
        # book_name_split = book_name.split()
        # index_of_by = book_name_split.index("by")
        # book_name = " ".join(book_name_split[:index_of_by])
        # author = " ".join(book_name_split[index_of_by+1:])
        # sentence = self.search_sentences[self.current_index - 1]
        # print('language: ' + language)
        # print('book_name: ' + book_name)
        # print('author: ' + author)
        # print('sentence: ' + sentence)
        # print('word: ' + self.current_word)
        # self.dictionary[self.current_word][2] = book_sentence_translation(language, book_name, author, sentence,
        #                                                                      self.current_word)
        # self.sentence_label_translate.config(text=str(self.dictionary[self.current_word][2]))

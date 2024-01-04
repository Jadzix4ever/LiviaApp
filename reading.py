import tkinter as tk
import json
import os

from ui import center_window, create_label, create_button, create_frame
from book_configuration import words_separated, word_and_sentence
from add_new_flashcards_window import FlashcardsInputDialog


class Reading:
    def __init__(self, master, book_name, book_content, dictionary, file_path):
        self.top = tk.Toplevel(master)
        self.top.title(book_name)

        self.words = words_separated(book_content[1])
        self.book = {}
        self.page = 0

        center_window(self.top, 800, 600)

        self.save_book_arrangement(book_name)
        self.dictionary = dictionary
        self.file_path = file_path

        self.slider = tk.Scale(self.top, from_=1, to=len(self.book), orient=tk.HORIZONTAL,
                               command=self.on_slider_change, length=300)
        self.slider.pack(side='bottom')
        frame = create_frame(self.top, 'bottom')
        create_button(frame, 'Previous', self.previous_side, 'pack', {'side': 'left'})
        create_button(frame, 'Next', self.next_side, 'pack', {'side': 'left'})

        self.next_side()

    def label_calculator(self):
        page = 1
        width = 5
        height = 5
        self.book = {page: []}

        for word in self.words:
            label = tk.Label(self.top, text=word, font='Arial, 14')

            self.book[page].append([word, width, height])

            if width + label.winfo_reqwidth() < 700:
                width += label.winfo_reqwidth()
            elif height + label.winfo_reqheight() < 500:
                height += label.winfo_reqheight()
                width = 5
            else:
                width = 5
                height = 5
                page += 1
                self.book[page] = []
            label.destroy()

    def clear_labels(self):
        for widget in self.top.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

    def on_slider_change(self, value):
        self.page = int(value)
        self.to_turn_page()

    def next_side(self):
        if len(self.book) == self.page:
            return

        self.page += 1
        self.to_turn_page()
        self.slider.set(self.page)

    def previous_side(self):
        if self.page == 1:
            return
        self.page -= 1
        self.to_turn_page()
        self.slider.set(self.page)

    def to_turn_page(self):
        self.clear_labels()
        pairs = word_and_sentence(self.book, self.page)
        number = 0

        for word in self.book[str(self.page)]:
            label = create_label(self.top, pairs[number][0], 'Arial, 14', None, 'place',
                                 {'x': word[1], 'y': word[2]})
            label.bind("<Button-1>", lambda event, question=pairs[number][0], sentence=pairs[number][1]:
                       FlashcardsInputDialog(self.top, self.dictionary, self.file_path, question, sentence, pairs))
            number += 1

    def save_book_arrangement(self, book_name):
        file_name = 'lessons/books/' + book_name + '.json'
        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                self.book = json.load(file)
            book2 = {}
            for key in list(self.book.keys()):
                book2[key] = self.book[key]
            self.book = book2
            return self.book
        else:
            self.label_calculator()
            with open(file_name, 'w') as file:
                json.dump(self.book, file)
            with open(file_name, 'r') as file:
                self.book = json.load(file)
            book2 = {}
            for key in list(self.book.keys()):
                book2[key] = self.book[key]
            self.book = book2
            return self.book

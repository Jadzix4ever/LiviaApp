import tkinter as tk
import json
import os

import ui
import book_configuration
import add_new_flashcards_window


class Reading:
    def __init__(self, root, book_name, book_content, dictionary, file_path):
        """
        :param root: Uchwyt do okna głównego.
        :param book_name:  Tytuł książki z autorem lub nazwa kursu.
        :param book_content: Tekst książki lub inny tekst do danego kursu.
        :param dictionary: Słownik zawierający fiszki do kursu.
        :param file_path: Ścieżka do pliku z fiszkami.
        """
        self.top = tk.Toplevel(root)
        self.top.title(book_name)

        # Podzielenie tekstu na listę z pojedyńczymi słowami.
        self.words = book_configuration.words_separated(book_content)

        self.book_name = book_name
        # Wczytanie do zmiennej słownika z rozkładem plików.
        self.label_positions_data = self.load_json_file(self.book_name)
        self.page = 0

        ui.center_window(self.top, 800, 600)

        self.book_name = book_name
        self.load_json_file(self.book_name)
        self.dictionary = dictionary
        self.file_path = file_path

        self.slider = tk.Scale(self.top, from_=1, to=len(self.label_positions_data), orient=tk.HORIZONTAL,
                               command=self.on_slider_change, length=300)
        self.slider.pack(side='bottom')
        frame = ui.create_frame(self.top, 'bottom')
        ui.create_button(frame, 'Previous', self.previous_side, 'pack', {'side': 'left'})
        ui.create_button(frame, 'Next', self.next_side, 'pack', {'side': 'left'})

        self.next_side()

    def clear_labels(self):
        for widget in self.top.winfo_children():
            if isinstance(widget, tk.Label):
                widget.destroy()

    def on_slider_change(self, value):
        self.page = int(value)
        self.to_turn_page()

    def next_side(self):
        if len(self.label_positions_data) == self.page:
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
        pairs = book_configuration.word_and_sentence(self.label_positions_data, self.page)
        number = 0

        for word in self.label_positions_data[str(self.page)]:
            label = ui.create_label(self.top, pairs[number][0], 'Arial, 14', None, 'place',
                                    {'x': word[1], 'y': word[2]})
            label.bind("<Button-1>", lambda event, question=pairs[number][0], sentence=pairs[number][1]:
                       add_new_flashcards_window.FlashcardsInputDialog(self.top, self.dictionary, self.file_path,
                                                                       question, sentence, pairs, self.book_name))
            number += 1

    def load_json_file(self, book_name) -> dict:
        """
        Sprawdza, czy istnieje plik JSON z zapisanymi współrzędnymi dla układu etykiet ze słowami na poszczególnych
        stronach. Jeżeli plik istnieje, wczytuje go do zmiennej self.label_positions_data, w przeciwnym razie zostaje
        wywołana metoda self.label_calculator, która dokonuje obliczeń.

        :param book_name: Tytuł książki z autorem lub nazwa kursu.
        :return: self.book
        """
        file_name = 'lessons/books/' + book_name + '.json'

        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                self.label_positions_data = json.load(file)

            return self.label_positions_data

        else:
            self.label_calculator()

            with open(file_name, 'w') as file:
                json.dump(self.label_positions_data, file)

            return self.label_positions_data

    def label_calculator(self) -> dict:
        """
        Metoda oblicza pozycje etykiet dla słów na poszczególnych stronach.

        :return: Słownik, gdzie kluczem jest numer strony, a wartością jest lista zawierająca informacje o każdej
        etykiecie (słowo, szerokość, wysokość) na tej stronie.
        """
        page = 1
        width = 5
        height = 5
        self.label_positions_data = {page: []}

        for word in self.words:
            label = tk.Label(self.top, text=word, font='Arial, 14')

            self.label_positions_data[page].append([word, width, height])

            if width + label.winfo_reqwidth() < 700:
                width += label.winfo_reqwidth()
            elif height + label.winfo_reqheight() < 500:
                height += label.winfo_reqheight()
                width = 5
            else:
                width = 5
                height = 5
                page += 1
                self.label_positions_data[page] = []
            label.destroy()

        return self.label_positions_data

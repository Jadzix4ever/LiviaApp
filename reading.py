import tkinter as tk
import json
import os
from tqdm import tqdm

import ui
import book_configuration
import add_new_flashcards_window


class Reading:
    def __init__(self, root, book_name, book_content, dictionary, file_path):
        """
        Klasa reprezentująca okno do czytania tekstów, książek itp. powiązanych z kursami.

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
        self.book_label_positions = self.load_json_file(self.book_name)
        self.page = 0

        ui.center_window(self.top, 800, 600)

        self.dictionary = dictionary
        self.file_path = file_path

        self.slider = tk.Scale(self.top, from_=1, to=len(self.book_label_positions), orient=tk.HORIZONTAL,
                               command=self.page_slider, length=300)
        self.slider.pack(side='bottom')
        frame = ui.create_frame(self.top, 'bottom')
        ui.create_button(frame, 'Previous', self.previous_page, 'pack', {'side': 'left'})
        ui.create_button(frame, 'Next', self.next_page, 'pack', {'side': 'left'})

        self.next_page()

    def page_slider(self, _event):
        """
        Przypisanie wartości z suwaka do self.page.
        :param _event:
        """
        page = self.slider.get()
        # Warunek konieczny, żeby uniknąć podwójnego wywoływania strony podczas zmiany strony przyciskiem.
        if page != self.page:
            self.page = page
            self.turn_page()

    def next_page(self):
        """
        Przejście do następnej strony, jeżeli istnieje.
        """
        if len(self.book_label_positions) == self.page:
            return

        self.page += 1
        self.turn_page()
        self.slider.set(self.page)

    def previous_page(self):
        """
        Przejście do poprzedniej strony, jeżeli istnieje.
        """
        if self.page == 1:
            return
        self.page -= 1
        self.turn_page()
        self.slider.set(self.page)

    def clear_labels(self):
        """
        Usunięcie wszystkich etykiet z okna.
        """
        for label in self.top.winfo_children():
            if isinstance(label, tk.Label):
                label.destroy()

    def turn_page(self):
        """
        Aktualizuje widok strony książki, usuwając poprzednie etykiety i tworząc nowe zgodnie z konfiguracją.

        Usuwa poprzednie etykiety z widoku za pomocą metody 'clear_labels'.
        Następnie na podstawie konfiguracji książki (book_configuration) i aktualnej strony (self.page)
        tworzy nowe etykiety ze słowami, dodając w ten sposób tekst dla danej strony.
        Etykiety są tworzone w określonych pozycjach (x, y) na podstawie informacji z book_label_positions.
        Każda etykieta jest interaktywna — po kliknięciu otwiera okno do dodawania fiszek (FlashcardsInputDialog).
        """
        self.clear_labels()
        # Do każdego słowa zostaje przypisane zdanie.
        pairs = book_configuration.word_and_sentence_pairs(self.book_label_positions, self.page)
        number = 0

        for word in self.book_label_positions[str(self.page)]:
            label = ui.create_label(self.top, pairs[number][0], 'Arial, 14', None, 'place',
                                    {'x': word[1], 'y': word[2]})
            label.bind("<Button-1>", lambda event, question=pairs[number][0], sentence=pairs[number][1]:
                       add_new_flashcards_window.FlashcardsInputDialog(self.top, self.dictionary, self.file_path,
                                                                       question, sentence, pairs, self.book_name))
            number += 1

    def load_json_file(self, book_name) -> dict:
        """
        Sprawdza, czy istnieje plik JSON z zapisanymi współrzędnymi dla układu etykiet ze słowami na poszczególnych
        stronach. Jeżeli plik istnieje, wczytuje go do zmiennej label_positions, w przeciwnym razie zostaje
        wywołana metoda self.label_calculator, która dokonuje obliczeń.

        :param book_name: Tytuł książki z autorem lub nazwa kursu.
        :return: Zwraca label_positions.
        """
        file_name = 'lessons/books/' + book_name + '.json'

        if os.path.exists(file_name):
            with open(file_name, 'r') as file:
                label_positions = json.load(file)

            return label_positions

        else:
            label_positions = self.label_calculator()

            with open(file_name, 'w') as file:
                json.dump(label_positions, file)

            return label_positions

    def label_calculator(self) -> dict:
        """
        Metoda oblicza pozycje etykiet dla słów na poszczególnych stronach.

        :return: Słownik, gdzie kluczem jest numer strony (string), a wartością jest lista zawierająca
        listę z informacją o każdej etykiecie [słowo, szerokość, wysokość] na tej stronie.
        """
        page = 1
        width = 5
        height = 5

        # Wszystkie int zostają zamienione na string dla zachowania spójności z plikiem JSON.
        label_positions = {str(page): []}

        for word in tqdm(self.words, desc="Calculating labels", unit="word", dynamic_ncols=True):
            label = tk.Label(self.top, text=word, font='Arial, 14')

            label_positions[str(page)].append([word, width, height])

            if width + label.winfo_reqwidth() < 700:
                width += label.winfo_reqwidth()

            elif height + label.winfo_reqheight() < 500:
                height += label.winfo_reqheight()
                width = 5

            else:
                width = 5
                height = 5
                page += 1
                label_positions[str(page)] = []

            label.destroy()

        return label_positions

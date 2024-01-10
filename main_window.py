import os
import textwrap
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path

import ui
import configuration
import book_configuration
import new_course
import add_new_flashcards_window
import start_course
import reading
import requests_window


class LiviaApp:
    def __init__(self, root):
        """
        Klasa reprezentująca główne okno programu.

        :param root: Obiekt klasy Tkinter Tk()).
        """

        self.master = root
        self.master.title("L  I  V  I  A")

        ui.center_window(self.master, 500, 400)

        self.file_path = configuration.auto_config()  # Przypisanie ścieżki do ostatnio otwieranej lekcji
        self.book_name = Path(self.file_path).stem
        self.courses_list = configuration.import_courses_list()  # Przypisanie listy z wszystkimi aktualnymi kursami.
        # Przypisanie fiszek do słownika.
        self.dictionary = configuration.import_flashcards_to_dictionary(self.file_path)

        ui.create_button(self.master, "Create new course", self.create_new_course, 'place', {'x': 5, 'y': 5})
        ui.create_button(self.master, "Import course", self.import_from_user_selection, 'place', {'x': 5, 'y': 35})
        ui.create_button(self.master, "Import text from url", self.import_from_url, 'place', {'x': 5, 'y': 65})
        ui.create_button(self.master, "Add new flashcards", self.new_word_input, 'place', {'x': 5, 'y': 95})
        ui.create_button(self.master, "Start course", self.start_learning, 'place', {'x': 5, 'y': 125})
        ui.create_button(self.master, "Start reading", self.start_reading, 'place', {'x': 5, 'y': 155})

        # Stworzenie listbox do wyświetlenia listy wszystkich dostępnych kursów i do szybkiego wyboru kursu do nauki.
        self.listbox = ui.ListBox(self, self.courses_list)
        self.path_label = ui.create_label(self.master, self.file_path, ("Arial", 12), 500, 'pack', {'side': 'bottom'})

    def update_from_listbox(self, selected_course):
        """
        Aktualizuje atrybuty klasy LiviaApp (self.file_path, self.book_name i self.dictionary)
        na podstawie wybranego kursu z listbox.
        Aktualizuje etykietę ze ścieżką aktualnego kursu.

        :param selected_course: Aktualnie wybrany kurs z listbox.
        """
        if '...' in selected_course:
            selected_course = selected_course[:-3]
            for course in self.courses_list:
                if selected_course in course:
                    self.file_path = 'lessons/' + course + '.txt'
        else:
            self.file_path = 'lessons/' + selected_course + '.txt'

        self.book_name = Path(self.file_path).stem
        self.path_label.config(text=self.file_path)
        configuration.save_to_config_file(self.file_path)
        self.dictionary = configuration.import_flashcards_to_dictionary(self.file_path)

    def create_new_course(self):
        """
        Tworzy nowy kurs na podstawie danych wprowadzonych w oknie dialogowym.
        Inicjuje obiekt okna dialogowego new_course.CourseCreate.
        Aktualizuje atrybuty klasy LiviaApp (self.file_path, self.book_name, self.dictionary i self.courses_list).
        Aktualizuje etykietę ze ścieżką aktualnego kursu i listbox.
        """
        dialog_window = new_course.CourseCreate(self.master, self.courses_list)
        self.master.wait_window(dialog_window.top)

        if dialog_window.done:
            self.file_path = dialog_window.file_path
            self.book_name = Path(self.file_path).stem
            configuration.save_to_config_file(self.file_path)
            self.dictionary = {}
            self.courses_list.insert(0, dialog_window.course_name)

            self.path_label.config(text=self.file_path)
            configuration.save_courses_list_to_file(self.courses_list)
            self.listbox.listbox.insert(0, dialog_window.course_name)

        else:
            print('Changes have not been applied.')

    def import_from_user_selection(self):
        """
        Importuje wybrany plik przez użytkownika.
        Aktualizuje atrybuty klasy LiviaApp (self.file_path, self.book_name, self.dictionary i self.courses_list)
        na podstawie wybranego kursu.
        Aktualizuje etykietę ze ścieżką aktualnego kursu.
        Aktualizuje listbox.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        # Sprawdzenie, czy plik został wybrany.
        if file_path:
            dictionary = configuration.import_flashcards_to_dictionary(file_path)

            # Sprawdzenie, czy zawartość pliku była w odpowiednim formacie.
            if dictionary is None:
                messagebox.showinfo("No flashcard imported.",
                                    "No flashcard imported. Incorrect format inside the file.")
                return

            # Sprawdzenie, czy ścieżka pochodzi z folderu z kursami.
            if '/LiviaApp/lessons/' not in file_path:
                file_name = os.path.basename(file_path)
                file_path = 'lessons/' + file_name

            self.file_path = file_path
            self.book_name = Path(self.file_path).stem
            self.dictionary = dictionary
            # Importowanie listy plików po utworzeniu pliku w folderze z kursami.
            self.courses_list = configuration.import_courses_list()
            # Aktualizacja kolejności w self.courses_list.
            self.courses_list = configuration.courses_list_update(self.book_name)

            configuration.save_to_config_file(self.file_path)
            configuration.save_courses_list_to_file(self.courses_list)
            self.path_label.config(text=str(self.file_path))
            self.listbox.listbox.delete(0, tk.END)

            for course in self.courses_list:
                truncated_course = textwrap.shorten(course, width=38, placeholder="...")
                self.listbox.listbox.insert(tk.END, truncated_course)

        else:
            print('No file selected.')

    def new_word_input(self):
        """
        Inicjuje tworzenie nowego okna do wprowadzania nowych fiszek.

        Wywołując tę metodę, tworzy się nowe okno do wprowadzania fiszek, umożliwiając użytkownikowi dodawanie nowych
        wpisów do słownika fiszek. Klasa FlashcardsInputDialog obsługuje proces wprowadzania i interakcji ze słownikiem.
        """
        add_new_flashcards_window.FlashcardsInputDialog(self.master, self.dictionary, self.file_path)

    def start_learning(self):
        """
        Inicjuje obiekt okna dialogowego start_course.CourseDialog.

        Wywołując tę metodę, tworzy się nowe okno do wprowadzania fiszek, umożliwiając użytkownikowi dodawanie nowych
        wpisów do słownika fiszek. Klasa FlashcardsInputDialog obsługuje proces wprowadzania i interakcji ze słownikiem.
        """
        if self.dictionary:
            self.master.withdraw()  # Ukrywa główne okno programu.
            dialog_window = start_course.CourseDialog(self.master, self.dictionary, self.file_path, self.book_name)
            self.master.wait_window(dialog_window.top)  # Czeka na zamknięcie okna dialogowego
            self.master.deiconify()  # Przywraca główne okno programu.
        else:
            messagebox.showinfo("No flashcard sets.", "Import flashcard sets to start learning.")

    def start_reading(self):
        """
        Rozpoczyna proces czytania książki.

        Importuje zawartość książki przy użyciu funkcji book_import z pliku book_configuration.
        Przeprowadza oczyszczenie tekstu książki przy użyciu funkcji book_text_cleaning z pliku book_configuration.
        Jeśli oczyszczenie tekstu powiedzie się, ukrywa główne okno aplikacji i otwiera okno czytania (Reading).
        """
        book_content = book_configuration.book_import(self.book_name)

        if book_content is None:
            messagebox.showinfo("The file with the text does not exist.", "You need to import a text file.")
            return

        # Na razie spis treści jest niewykorzystywany.
        _, book_content = book_configuration.book_text_cleaning(book_content)

        if book_content:
            self.master.withdraw()
            dialog = reading.Reading(self.master, self.book_name, book_content, self.dictionary, self.file_path)
            self.master.wait_window(dialog.top)
            self.master.deiconify()

    def import_from_url(self):
        """
        Inicjuje tworzenie nowego okna do pobierania tekstów do kursów ze stron internetowych.
        """
        requests_window.RequestsWindow(self.master)

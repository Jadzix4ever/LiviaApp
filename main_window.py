import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from ui import create_button, create_label, center_window, ListBox
from configuration import (auto_config, import_from_user_selection, import_file_to_dictionary, courses_list,
                           save_to_courses_list, save_to_config_file, save_word_list, courses_list_update)
from book_configuration import book_import
from new_course import CourseCreate
from add_new_flashcards_window import FlashcardsInputDialog
from start_course import CourseDialog
from reading import Reading


class LiviaApp:
    def __init__(self, root):
        self.master = root
        self.master.title("L  I  V  I  A")

        center_window(self.master, 500, 400)

        self.file_path = auto_config()  # Przypisanie ścieżki do ostatnio otwieranej lekcji
        self.book_name = Path(self.file_path).stem
        self.courses_list = courses_list()
        self.dictionary = import_file_to_dictionary(self.file_path)

        create_button(self.master, "Create new course", self.create_new_course, 'place', {'x': 5, 'y': 5})
        create_button(self.master, "Import course", self.import_from_user_selection, 'place', {'x': 5, 'y': 35})
        create_button(self.master, "Add new flashcards", self.new_word_input, 'place', {'x': 5, 'y': 65})
        create_button(self.master, "Start course", self.start_learning, 'place', {'x': 5, 'y': 95})
        create_button(self.master, "Start reading", self.start_reading, 'place', {'x': 5, 'y': 125})

        self.listbox = ListBox(self, self.courses_list)
        self.path_label = create_label(self.master, self.file_path, ("Arial", 12), 500, 'pack', {'side': 'bottom'})

    def update_from_listbox(self, new_file_path):
        if '...' in new_file_path:
            new_file_path = new_file_path[:-3]
            for course in self.courses_list:
                if new_file_path in course:
                    self.file_path = 'lessons/' + course + '.txt'
                    self.book_name = Path(self.file_path).stem
        else:
            self.file_path = 'lessons/' + new_file_path + '.txt'
            self.book_name = Path(self.file_path).stem
        self.path_label.config(text=self.file_path)
        save_to_config_file(self.file_path)
        self.dictionary = import_file_to_dictionary(self.file_path)

    def create_new_course(self):
        dialog = CourseCreate(self.master)
        self.master.wait_window(dialog.top)
        if dialog.done:
            self.dictionary = {}
            self.file_path = dialog.file_path
            save_to_config_file(self.file_path)
            self.path_label.config(text=self.file_path)
            self.courses_list.append(dialog.course_name)
            save_to_courses_list(self.courses_list)
            self.listbox.listbox.insert(0, dialog.course_name)
        else:
            print('Changes have not been applied.')

    def import_from_user_selection(self):
        file_path = import_from_user_selection(self.master)
        if file_path:
            self.file_path = file_path
            self.book_name = Path(self.file_path).stem
            self.path_label.config(text=str(self.file_path))
            save_to_config_file(self.file_path)
            self.dictionary = import_file_to_dictionary(self.file_path)
            self.courses_list = courses_list_update(self.book_name)
            self.listbox.listbox.delete(0, tk.END)
            for course in self.courses_list:
                self.listbox.listbox.insert(tk.END, course)

    def new_word_input(self):
        FlashcardsInputDialog(self.master, self.dictionary, self.file_path)
        save_word_list(self.file_path, self.dictionary)

    def start_learning(self):
        if self.dictionary:
            self.master.withdraw()  # Ukryj główne okno
            dialog = CourseDialog(self.master, self.dictionary, self.file_path)
            self.master.wait_window(dialog.top)  # Poczekaj na zamknięcie okna dialogowego
            self.master.deiconify()  # Przywróć główne okno
        else:
            messagebox.showinfo("No flashcard sets.", "Import flashcard sets to start learning.")

    def start_reading(self):
        print(self.book_name)
        book_content = book_import(self.book_name)
        if book_content:
            Reading(self.master, self.book_name, book_content, self.dictionary, self.file_path)


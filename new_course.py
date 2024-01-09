import tkinter as tk
import os
import ui


class CourseCreate:
    def __init__(self, root, courses_list):
        """
        :param root: Uchwyt do głównego okna.
        :param courses_list: Lista kursów do sprawdzenia, czy plik o podanej nazwie już istnieje.
        """
        self.top = tk.Toplevel(root)

        ui.center_window(self.top, 300, 100)

        # Zmienna pomocnicza do uzyskania informacji, czy metoda create_file została wykonana do końca.
        self.done = False
        self.file_path = None
        self.course_name = None
        self.courses = courses_list

        self.label = ui.create_label(self.top, 'Enter the course name:', 'Arial', None, 'pack', {'side': 'top'})
        self.entry = ui.create_entry(self.top, 'top')
        self.button = ui.create_button(self.top, 'Create', self.create_file, 'pack', {'side': 'top'})

    def create_file(self):
        """
        Sprawdza, czy kurs o podanej nazwie istnieje w liście kursów.
        Tworzy nowy plik na podstawie wprowadzonej nazwy kursu i aktualizuje etykiety.
        """
        self.course_name = self.entry.get()

        for course in self.courses:
            if self.course_name.lower() == course.lower():
                self.label.config(text='In the base already exist.')
                self.entry.destroy()
                self.button.config(text='Close', command=self.top.destroy)
                return

        self.file_path = os.path.join('lessons', self.course_name + '.txt')

        # Stworzenie pustego pliku o nazwie kursu.
        with open(self.file_path, 'w') as _:
            print('Plik ' + self.file_path + ' został utworzony.')

        self.label.config(text='You can close this window')
        self.entry.destroy()
        self.button.config(text='Close', command=self.top.destroy)
        self.done = True

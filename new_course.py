import tkinter as tk
import ui
import configuration


class CourseCreate:
    def __init__(self, root, courses_list):
        """
        Klasa reprezentująca okno do tworzenia nowego kursu.

        :param root: Uchwyt do głównego okna.
        :param courses_list: Lista kursów do sprawdzenia, czy plik o podanej nazwie już istnieje.
        """
        self.top = tk.Toplevel(root)

        ui.center_window(self.top, 400, 100)

        # Zmienna pomocnicza do uzyskania informacji, czy metoda create_file została wykonana do końca.
        self.done = False
        self.file_path = None
        self.course_name = None
        self.courses = courses_list

        self.label = ui.create_label(self.top, 'Enter the course name:', 'Arial', None, 'pack', {'side': 'top'})
        self.entry = ui.create_entry(self.top, 'top', width=40)
        self.button = ui.create_button(self.top, 'Create', self.create_file, 'pack', {'side': 'top'})

    def create_file(self):
        """
        Sprawdza, czy kurs o podanej nazwie istnieje w liście kursów.
        Tworzy nowy plik na podstawie wprowadzonej nazwy kursu i aktualizuje etykiety.
        """
        self.course_name = self.entry.get()

        if self.course_name:
            for course in self.courses:
                if self.course_name.lower() == course.lower():
                    self.label.config(text='In the base already exist.')
                    self.entry.destroy()
                    self.button.config(text='Close', command=self.top.destroy)
                    return

            # Stworzenie pliku o nazwie kursu.
            self.file_path = configuration.new_course_create(self.course_name)

            self.label.config(text='You can close this window')
            self.entry.destroy()
            self.button.config(text='Close', command=self.top.destroy)
            self.done = True

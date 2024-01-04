import tkinter as tk
import os
from ui import center_window, create_label, create_entry, create_button


class CourseCreate:
    def __init__(self, root):
        self.top = tk.Toplevel(root)

        center_window(self.top, 300, 100)

        self.done = False
        self.file_path = None
        self.course_name = None

        self.label = create_label(self.top, 'Enter the course name:', 'Arial', None, 'pack', {'side': 'top'})
        self.entry = create_entry(self.top, 'top')
        self.button = create_button(self.top, 'Create', self.create_file, 'pack', {'side': 'top'})

    def create_file(self):
        self.course_name = self.entry.get()
        with open("config/courses_list", 'r') as file:
            courses = file.readlines()
        for course in courses:
            if self.course_name.lower() == course.lower():
                self.label.config(text='In the base already exist.')
                self.entry.destroy()
                self.button.config(text='Close', command=self.top.destroy)
                return

        self.file_path = os.path.join('lessons', self.course_name + '.txt')

        with open(self.file_path, 'w') as _:
            print('Plik ' + self.file_path + ' został utworzony.')

        self.label.config(text='You can close the dialog window')
        self.entry.destroy()
        self.button.config(text='Close', command=self.top.destroy)
        self.done = True

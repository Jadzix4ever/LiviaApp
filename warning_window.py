import tkinter as tk
from tkinter import messagebox
import os
import shutil
from configuration import import_flashcards_to_dictionary, save_flashcards
from ui import center_window, create_label, create_frame, create_button


class WarningWindow:
    def __init__(self, root, first_line, second_line, file_path):
        self.top = tk.Toplevel(root)

        center_window(self.top, 300, 200)

        create_label(self.top, 'The file you want to import is outside the course folder. Are you sure you want to '
                               'import a file from a different source?', 'Arial', 180, 'pack', {'side': 'top'})
        frame = create_frame(self.top, 'top')
        create_button(frame, 'Yes', self.check_file, 'pack', {'side': 'left'})
        create_button(frame, 'No', self.close_window, 'pack', {'side': 'left'})

        self.first_line = first_line
        self.second_line = second_line
        self.file_path = file_path
        print(self.first_line)
        print(self.second_line)

    def check_file(self):
        if (('###LiviaApp###' not in self.first_line)
                and ('#separator:tab' not in self.first_line and '#html:true' not in self.second_line)):
            messagebox.showinfo('Incorrect file format.', 'Import the correct file with flashcard set.')
            self.top.destroy()
            return
        else:
            destination_folder = 'lessons/'
            file_name = os.path.basename(self.file_path)

            files = os.listdir(destination_folder)

            if file_name not in files:
                try:
                    shutil.move(self.file_path, destination_folder)
                    self.file_path = os.path.join(destination_folder, os.path.basename(self.file_path))
                except Exception as e:
                    print(f"Error: {e}")
            else:
                messagebox.showinfo('Incorrect file name.', f'File {file_name} already exist.')
                self.top.destroy()

            if '#separator:tab' in self.first_line and '#html:true' in self.second_line:
                dictionary = import_flashcards_to_dictionary(self.file_path)
                save_flashcards(self.file_path, dictionary)

    def close_window(self):
        self.top.destroy()

import tkinter as tk
import textwrap
from configuration import save_to_courses_list, courses_list_update


def create_frame(root, side):
    frame = tk.Frame(root)
    frame.pack(side=side)
    return frame


def create_button(root, text: str, command, method: str, *args):
    button = tk.Button(root, text=text, command=command, width=12)
    if method == 'place':
        button.place(*args)
    if method == 'pack':
        button.pack(*args)
    return button


def create_label(root, text: str, font: str or tuple = 'Arial', wraplength: int = None, method='pack', *args):
    label = tk.Label(root, text=text, font=font, wraplength=wraplength)
    if method == 'place':
        label.place(*args)
    if method == 'pack':
        label.pack(*args)
    return label


def get_label_dimensions(label):
    width = label.winfo_reqwidth()
    height = label.winfo_reqheight()
    return width, height


def create_entry(root, side, text='', width=20):
    entry = tk.Entry(root, width=width)
    entry.insert(0, text)
    entry.pack(side=side)
    return entry


def center_window(root, width: int, height: int):
    """
    Wyśrodkowuje okno na ekranie.

    Parameters:
        root: Okno do wyśrodkowania.
        width (int): Szerokość okna.
        height (int): Wysokość okna.
    """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")


class ListBox:
    def __init__(self, app, courses_list):
        self.app = app
        self.courses_list = courses_list
        self.listbox = self.list_box()

    def list_box(self):
        max_length = 38
        self.listbox = tk.Listbox(width=max_length - 8, height=20)
        self.listbox.pack(anchor="ne", padx=10, pady=10)

        if self.courses_list:
            for course in self.courses_list:
                truncated_course = textwrap.shorten(course, width=max_length, placeholder="...")
                self.listbox.insert(tk.END, truncated_course)

        self.listbox.bind("<ButtonRelease-1>", self.listbox_select)

        return self.listbox

    def listbox_select(self, _event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = self.listbox.get(selected_index)
            self.listbox.delete(selected_index)
            self.listbox.insert(0, selected_item)
            if '...' in selected_item:
                selected = selected_item.replace('...', '')
            else:
                selected = selected_item

            self.courses_list = courses_list_update(selected)

            save_to_courses_list(self.courses_list)
            self.app.update_from_listbox(selected_item)

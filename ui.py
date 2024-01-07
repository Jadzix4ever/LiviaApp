import tkinter as tk
import textwrap
import configuration


def create_frame(root, side):
    frame = tk.Frame(root)
    frame.pack(side=side)
    return frame


def create_button(root, text: str, command, method: str, *args):
    """
    Tworzy i konfiguruje przycisk w interfejsie Tkinter.

    :param root: Okno, na którym ma być umieszczony przycisk.
    :param text: Tekst wyświetlany na przycisku.
    :param command: Funkcja (lub metoda), która zostanie wywołana po naciśnięciu przycisku.
    :param method: Określa, czy przycisk ma być umieszczony za pomocą metody ('place') czy ('pack').
    :param args: Dodatkowe argumenty przekazywane do metody .place() lub .pack(), w zależności od wybranego method.

    Zwraca utworzony przycisk.
    """
    button = tk.Button(root, text=text, command=command, width=12)

    if method == 'place':
        button.place(*args)

    elif method == 'pack':
        button.pack(*args)

    return button


def create_label(root, text: str, font: str or tuple = 'Arial', wraplength: int = None, method='pack', *args):
    """

    """
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

    :param root: Okno do wyśrodkowania.
    :param width: Szerokość okna.
    :param height: Wysokość okna.
    """
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")


class ListBox:
    def __init__(self, class_handle, courses_list):
        """
        Inicjalizuje obiekt klasy ListBox.

        Parametry:
        :param class_handle: Uchwyt klasy LiviaApp, reprezentujący główne okno programu.
        :param courses_list: Lista z nazwami kursów.

        Atrybuty:
        - app: Przechowuje uchwyt klasy LiviaApp.
        - courses_list: Przechowuje listę z nazwami kursów.
        - listbox: Przechowuje obiekt klasy tk.Listbox.
        """
        self.class_handle = class_handle
        self.courses_list = courses_list
        self.listbox = self.create_list_box()

    def create_list_box(self):
        """
        Tworzy i konfiguruje listbox do wyświetlania kursów w interfejsie użytkownika.
        :return:
        Zwraca obiekt klasy tk.Listbox.
        """
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
        """
        Metoda jest wywoływana po kliknięciu kursu w listbox. Aktualizuje listę kursów, zapisuje ją do pliku
        i wywołuje metodę update_from_listbox z klasy LiviaApp w celu zaktualizowania ścieżki, nazwy kursu i słownika.
        :param _event:
        """
        # Pobranie indeksu klikniętego kursu w listbox.
        selected_index = self.listbox.curselection()

        # Pobranie nazwy zaznaczonego kursu.
        selected_course = self.listbox.get(selected_index)

        # Usunięcie zaznaczonego kursu z listbox i wstawienie go na pierwszą pozycję.
        self.listbox.delete(selected_index)
        self.listbox.insert(0, selected_course)

        # Usunięcie ewentualnych trzech kropek z nazwy kursu.
        if '...' in selected_course:
            selected = selected_course.replace('...', '')
        else:
            selected = selected_course

        # Aktualizacja kolejności w liście kursów.
        self.courses_list = configuration.courses_list_update(selected)
        # Zapisanie aktualnej kolejności kursów do pliku
        configuration.save_courses_list_to_file(self.courses_list)
        self.class_handle.update_from_listbox(selected_course)

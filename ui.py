import tkinter as tk
import textwrap
import configuration


def create_frame(root, side):
    """
    :param root: Okno, na którym ma być umieszczona ramka.
    :param side: Strona, na której ma być umieszczona ramka ('top', 'bottom', 'left' lub 'right').

    :return: Obiekt ramki (Frame) umieszczonej na oknie.
    """
    frame = tk.Frame(root)
    frame.pack(side=side)
    return frame


def create_button(root, text: str, command, method: str, *args, width: int = 12):
    """
    :param root: Okno, na którym ma być umieszczony przycisk.
    :param text: Tekst wyświetlany na przycisku.
    :param command: Funkcja (lub metoda), która zostanie wywołana po naciśnięciu przycisku.
    :param method: Określa, czy przycisk ma być umieszczony za pomocą metody ('place') czy ('pack').
    :param args: Dodatkowe argumenty przekazywane do metody .place() lub .pack().
    :param width: Szerokość przycisku.

    :return: Obiekt przycisku.
    """
    button = tk.Button(root, text=text, command=command, width=width)

    if method == 'place':
        button.place(*args)

    elif method == 'pack':
        button.pack(*args)

    return button


def create_label(root, text: str, font: str or tuple = 'Arial', wraplength: int = None, method='pack', *args,
                 fg='systemTextColor'):
    """
    :param root: Okno, na którym ma być umieszczona etykieta.
    :param text: Tekst wyświetlany na etykiecie.
    :param font: Czcionka tekstu.
    :param wraplength: Maksymalna szerokość tekstu przed zawinięciem do nowej linii. Domyślnie None.
    :param method: Określa, czy etykieta ma być umieszczony za pomocą metody ('place') czy ('pack').
    :param args: Dodatkowe argumenty przekazywane do metody .place() lub .pack().
    :param fg: Kolor czcionki.

    :return: Obiekt etykiety.
    """
    label = tk.Label(root, text=text, font=font, wraplength=wraplength, fg=fg)
    if method == 'place':
        label.place(*args)
    if method == 'pack':
        label.pack(*args)
    return label


def create_entry(root, side, text: str = '', width: int = 20):
    """
    :param root: Okno, na którym ma być umieszczone pole do wprowadzania tekstu.
    :param side: Strona, na której ma być umieszczone pole do wprowadzania tekstu ('left', 'right', 'top' lub 'bottom').
    :param text: Tekst początkowy wyświetlany w polu do wprowadzania tekstu. Domyślnie ''.
    :param width: Szerokość pola do wprowadzania tekstu. Domyślnie 20.

    :return: Obiekt pola do wprowadzania tekstu (Entry) umieszczonego na oknie.
    """
    entry = tk.Entry(root, width=width)
    entry.insert(0, text)
    entry.pack(side=side)
    return entry


def create_text(root, side, text: str = '', width=45, height=10):
    text_widget = tk.Text(root, width=width, height=height)
    text_widget.insert(1.0, text)
    text_widget.pack(side=side)
    return text_widget


def get_label_dimensions(label) -> tuple:
    """
    :param label: Obiekt etykiety.
    :return: Krotka zawierająca szerokość i wysokość etykiety.
    """
    width = label.winfo_reqwidth()
    height = label.winfo_reqheight()
    return width, height


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
    def __init__(self, root, courses_list):
        """
        Inicjalizuje obiekt klasy ListBox.

        Parametry:
        :param root: Uchwyt głównego okna programu.
        :param courses_list: Lista z nazwami kursów.

        Atrybuty:
        - app: Przechowuje uchwyt klasy LiviaApp.
        - courses_list: Przechowuje listę z nazwami kursów.
        - listbox: Przechowuje obiekt klasy tk.Listbox.
        """
        self.app = root
        self.courses_list = courses_list
        self.listbox = self.create_list_box()

    def create_list_box(self):
        """
        Tworzy i konfiguruje listbox do wyświetlania kursów w interfejsie użytkownika.
        :return: Zwraca obiekt klasy tk.Listbox.
        """
        listbox = tk.Listbox(width=30, height=20)
        listbox.pack(anchor="ne", padx=10, pady=10)

        if self.courses_list:
            for course in self.courses_list:
                truncated_course = textwrap.shorten(course, width=38, placeholder="...")
                listbox.insert(tk.END, truncated_course)

        listbox.bind("<ButtonRelease-1>", self.listbox_select)

        return listbox

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
        self.app.update_from_listbox(selected_course)

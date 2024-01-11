import tkinter as tk
import requests

from bs4 import BeautifulSoup
from ui import center_window, create_entry, create_label, create_button


class RequestsWindow:
    def __init__(self, root, ):
        """
        Klasa reprezentująca okno do importowania tekstu z URL do pliku tekstowego.

        :param root: Uchwyt do okna głównego.
        """
        self.top = tk.Toplevel(root)
        self.top.title("Requests Window")

        center_window(self.top, 600, 130)

        create_label(self.top, 'URL address:')
        self.url = create_entry(self.top, "top", '', width=65)
        create_label(self.top, 'File name:')
        self.file_name = create_entry(self.top, "top", '', width=40)
        create_button(self.top, "Create", self.export_text_to_file, 'pack', {'side': 'top'})

    def export_text_to_file(self):
        """
        Pobranie tekstu z URL i zapisanie go do pliku tekstowego.
        """
        url = self.url.get()
        file_name = self.file_name.get()
        response = requests.get(url)
        text = response.text

        if "gutenberg.org" not in url and url[-4:] != '.txt':
            # Przetworzenie HTML, jeśli strona nie jest z gutenberg.org i nie kończy się na '.txt'
            soup = BeautifulSoup(text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = '\n'.join([paragraf.get_text() for paragraf in paragraphs])

            if response.status_code == 200:
                print('Strona wczytana poprawnie.')

        with open('lessons/books/' + file_name + '.txt', 'w', encoding='utf-8') as file:
            file.write(text)

        self.url.delete(0, tk.END)
        self.file_name.delete(0, tk.END)

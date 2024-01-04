import tkinter as tk
import requests

from bs4 import BeautifulSoup
from ui import center_window, create_entry, create_label, create_button


class RequestsWindow:
    def __init__(self, root, ):
        self.top = tk.Toplevel(root)
        self.top.title("Requests Window")

        center_window(self.top, 600, 130)

        create_label(self.top, 'URL address:')
        self.url = create_entry(self.top, "top", '', 600)
        create_label(self.top, 'File name:')
        self.file_name = create_entry(self.top, "top", '')
        create_button(self.top, "Create", self.import_to_txt, 'pack', {'side': 'top'})

    def import_to_txt(self):
        url = self.url.get()
        file_name = self.file_name.get()
        response = requests.get(url)
        text = response.text

        if "gutenberg.org" not in url and url[-4:] != '.txt':
            soup = BeautifulSoup(text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = '\n'.join([paragraf.get_text() for paragraf in paragraphs])

        with open('lessons/books/' + file_name + '.txt', 'w', encoding='utf-8') as file:
            file.write(text)

        self.url.delete(0, tk.END)
        self.file_name.delete(0, tk.END)

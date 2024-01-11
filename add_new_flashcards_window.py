import tkinter as tk
from tkinter import messagebox

import configuration
import open_ai
import ui


def remove_duplicate_elements(pairs: list) -> list:
    """
    Usuwa zduplikowane zdania z listy self.pairs, w której do każdego wyrazu przypisane jest zdanie.

    :param pairs: Lista par ['słowo', 'zdanie'].
    """
    sentences = [pairs[1] for pairs in pairs]
    unique_sentences = []
    for i, sentence in enumerate(sentences):
        if sentence != sentences[i - 1]:
            unique_sentences.append(sentence)
    return unique_sentences


class FlashcardsInputDialog:
    def __init__(self, root, dictionary: dict, file_path: str,
                 question: str = '', sentence: str = '', pairs: list = None, book_name: str = ''):
        """
        Klasa reprezentująca okno do tworzenia nowych fiszek.

        :param root: Uchwyt do okna.
        :param dictionary: Słownik zawierający fiszki do kursu do wprowadzania i zapisywania zmian.
        :param file_path: Ścieżka do pliku z fiszkami.
        :param question: Słowo (pytanie). Domyślnie ''.
        :param sentence: Zdanie. Domyślnie ''.
        :param pairs: Lista par ['słowo', 'zdanie']. Domyślnie None.
        :param book_name: Tytuł książki z autorem lub nazwa kursu. Domyślnie ''.
        """
        self.top = tk.Toplevel(root)

        self.number_right_side = 0   # Ustawienie liczby pomocniczej dla dodawania do prawej strony tekstu z listy zdań.
        # dla wszystkich słów na stronie.
        if pairs:   # Warunek konieczny do uniknięcia błędu podczas dodawania słów z okna głównego.
            self.page_sentences = remove_duplicate_elements(pairs)
        self.book_name = book_name
        ui.center_window(self.top, 900, 350)

        ui.create_label(self.top, 'Question:', 'Arial', None, 'pack', {'side': 'top'})
        self.entry_question = ui.create_entry(self.top, 'top', question)
        ui.create_label(self.top, 'Answer:', 'Arial', None, 'pack', {'side': 'top'})
        ui.create_button(self.top, 'Auto translation', self.word_translation, 'pack', {'side': 'top'})
        self.entry_answer = ui.create_entry(self.top, 'top', '', 35)
        ui.create_label(self.top, 'Sentence:', 'Arial', None, 'pack', {'side': 'top'})
        self.entry_sentence = ui.create_entry(self.top, 'top', sentence, 95)
        ui.create_label(self.top, 'Sentence translation:', 'Arial', None, 'pack', {'side': 'top'})
        ui.create_button(self.top, 'Auto translation', self.sentence_translation, 'pack', {'side': 'top'})
        self.entry_sentence_translation = ui.create_entry(self.top, 'top', '', 95)
        self.ok_button = ui.create_button(self.top, 'OK', self.new_word_input, 'pack', {'side': 'bottom'})
        frame = ui.create_frame(self.top, 'bottom')
        ui.create_button(frame, 'more left side', self.add_text_to_left_side, 'pack', {'side': 'left'})
        ui.create_button(frame, 'more right side', self.add_text_to_right_side, 'pack', {'side': 'left'})

        self.dictionary = dictionary    # Przypisanie słownika do zmiennej do wprowadzania i zapisywania zmian.
        self.file_path = file_path      # Przypisanie ścieżki z plikiem do zmiennej do funkcji zapisywania zmian.
        self.current_sentence = self.entry_sentence.get()   # Przypisanie przesłanego zdania do zmiennej.
        self.current_sentence_translation = self.entry_sentence_translation.get()

        # Sprawdzenie, czy słowo już istnieje w słowniku:
        if self.dictionary and self.entry_question.get() in self.dictionary:
            print(f"The word {question} - {self.dictionary[question]} already exists.")
            self.entry_answer.insert(0, self.dictionary[question][0])
            self.ok_button.config(text='Edit', command=self.edit_dictionary)
            self.entry_question.config(state="readonly")

    # Metoda edit zamienia istniejące słowo w słowniku, zgodnie z danymi znajdującymi się w polach tekstowych.
    def edit_dictionary(self):
        """
        Pobiera dane z pól i wywołuje metodę self.update_dictionary.
        """
        question = self.entry_question.get()
        answer = self.entry_answer.get()

        self.update_dictionary(question, answer)

        print(f"The word {question} - {answer} has been changed.")

    def new_word_input(self):
        """
        Sprawdza, czy fiszka z danym słowem (question) już istnieje w słowniku i czy są wypełnione pola ze słowami.
        Jeżeli słowo (question) jest w słowniku, zmienia nazwę przycisku i command na edit_dictionary.
        Jeżeli słowa (question) nie ma w słowniku i pola są wypełnione, umieszcza fiszkę w słowniku.
        """
        # Pobranie aktualnych wartości pytania i odpowiedzi.
        question = self.entry_question.get()
        answer = self.entry_answer.get()

        # Sprawdzenie, czy słowo (pytanie) już istnieje w słowniku
        # (przydatne w przypadku edytowania słowa np. ze względu na usunięcie przecinka).
        if self.dictionary and question in self.dictionary:
            print(f"The word {question} - {self.dictionary[question]} already exists.")
            # Wyświetlenie tłumaczenia słowa w polu answer i zmiana nazwy przycisku na 'Edit'.
            self.entry_answer.insert(0, self.dictionary[question][0])
            self.ok_button.config(text='Edit', command=self.edit_dictionary)
            self.entry_question.config(state="readonly")

        elif question and answer:
            self.update_dictionary(question, answer)
            print(f"The word {question} - {answer} has been added.")

        # Wyświetlenie informacji o błędzie w przypadku pozostawienia pustego pola.
        else:
            messagebox.showinfo("Input Error", "You need to fill in the fields for question and answer.")
            print('Input Error')

    def add_text_to_right_side(self):
        """
        Dodaje fragmenty tekstu do prawej strony.
        """
        self.number_right_side += 1

        try:
            for i, sentence in enumerate(self.page_sentences):
                if sentence in self.current_sentence:
                    self.current_sentence = (self.current_sentence + ' ' +
                                             self.page_sentences[i + self.number_right_side])
                    break
        except IndexError:
            print('IndexError: list index out of range.')

        self.entry_sentence.delete(0, tk.END)
        self.entry_sentence.insert(0, self.current_sentence)

    def add_text_to_left_side(self):
        """
        Dodaje fragmenty tekstu do lewej strony.
        """
        self.number_right_side += 1

        try:
            for i, sentence in enumerate(self.page_sentences):
                if sentence in self.current_sentence and i != 0:
                    self.current_sentence = self.page_sentences[i - 1] + ' ' + self.current_sentence
                    break
        except IndexError:
            print('IndexError: list index out of range.')

        self.entry_sentence.delete(0, tk.END)
        self.entry_sentence.insert(0, self.current_sentence)

    def word_translation(self):
        """
        Tłumaczy słowa z wykorzystaniem AI za pomocą OpenAPI_Key
        """
        question = self.entry_question.get()
        self.entry_answer.delete(0, tk.END)

        # Sprawdzenie, czy kurs pochodzi z książki (tłumaczenia z książek są dokładniejsze)
        # i czy jest wprowadzone zdanie.
        if 'by' in self.book_name and self.entry_sentence.get():
            title, author = self.book_name.split(' by ')
            generated = open_ai.book_word_translation(title, author, self.current_sentence, question)

            # Sprawdzenie, czy wygenerowany tekst jest w odpowiedniej formie.
            # W commit dla OpenAI podaję wzór, jak ma wyglądać wygenerowany tekst.
            # Sprawdzam tylko dwukropek, ponieważ słowo (question) może być sprowadzone do formy podstawowej.
            if ':' in generated:
                generated = generated.split(':')
                question = generated[0].strip()
                answer = generated[1].strip()

                self.entry_question.delete(0, tk.END)
                self.entry_question.insert(0, question)

                # Sprawdzenie, czy słowo jest już w słowniku,
                # ponieważ po tłumaczeniu słowo (question) może być sprowadzone do formy podstawowej.
                question = self.entry_question.get()

                if question in self.dictionary:
                    self.ok_button.config(text='Edit', command=self.edit_dictionary)
                    self.entry_question.config(state="readonly")

                self.entry_answer.insert(0, answer)

            else:
                answer = generated
                self.entry_answer.insert(0, answer)

        else:
            self.standard_word_translation(question)

    def standard_word_translation(self, question: str):
        # W trakcie tworzenia.
        pass

    def sentence_translation(self):
        """
        Tłumaczy zdania z wykorzystaniem AI za pomocą OpenAPI_Key
        """
        question = self.entry_question.get()

        if not self.entry_question.get():
            return

        self.entry_sentence_translation.delete(0, tk.END)

        if 'by' in self.book_name:
            title, author = self.book_name.rsplit(' by ', 1)
            self.current_sentence_translation = open_ai.book_sentence_translation(title, author, self.current_sentence,
                                                                                  question)
            self.entry_sentence_translation.insert(0, self.current_sentence_translation)

        else:
            self.standard_sentence_translation(self.current_sentence)

    def standard_sentence_translation(self, sentence: str):
        # W trakcie tworzenia.
        pass

    def update_dictionary(self, question: str, answer: str):
        """
        Aktualizuje słownik i zapisuje go do pliku.
        """
        # Zaktualizowanie zmiennych.
        self.current_sentence = self.entry_sentence.get()
        self.current_sentence_translation = self.entry_sentence_translation.get()

        # Utworzenie nowej listy dla aktualnego słowa.
        current_value = []

        # Zaktualizowanie słownika nowymi danymi.
        self.dictionary[question] = current_value
        current_value.append(answer)
        current_value.append(self.current_sentence)
        current_value.append(self.current_sentence_translation)

        # Zapisanie zaktualizowanego słownika do pliku
        configuration.save_flashcards(self.file_path, self.dictionary)

        self.entry_question.delete(0, tk.END)
        self.entry_answer.delete(0, tk.END)
        self.entry_sentence.delete(0, tk.END)
        self.entry_sentence_translation.delete(0, tk.END)

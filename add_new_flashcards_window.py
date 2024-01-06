import tkinter as tk
from configuration import save_word_list, check_generated_words
from ui import center_window, create_label, create_entry, create_button, create_frame
import open_ai


class FlashcardsInputDialog:
    def __init__(self, master, dictionary, file_path, question='', sentence='', pairs='', book_name=''):
        self.top = tk.Toplevel(master)

        self.number_right = 0   # Ustawienie liczby pomocniczej dla dodawania tekstu z listy zdań.
        self.pairs = pairs  # Przypisanie do zmiennej listy z listami par ['słowo','zdanie']
        # dla wszystkich słów na stronie.
        self.book_name = book_name
        center_window(self.top, 900, 350)

        create_label(self.top, 'Question:', 'Arial', None, 'pack', {'side': 'top'})
        self.entry_question = create_entry(self.top, 'top', question)
        create_label(self.top, 'Answer:', 'Arial', None, 'pack', {'side': 'top'})
        create_button(self.top, 'Auto translation', self.word_translation, 'pack', {'side': 'top'})
        self.entry_answer = create_entry(self.top, 'top', '', 35)
        create_label(self.top, 'Sentence:', 'Arial', None, 'pack', {'side': 'top'})
        self.entry_sentence = create_entry(self.top, 'top', sentence, 95)
        create_label(self.top, 'Sentence translation:', 'Arial', None, 'pack', {'side': 'top'})
        create_button(self.top, 'Auto translation', self.sentence_translation, 'pack', {'side': 'top'})
        self.entry_sentence_translation = create_entry(self.top, 'top', '', 95)
        self.ok_button = create_button(self.top, 'OK', self.ok, 'pack', {'side': 'bottom'})
        frame = create_frame(self.top, 'bottom')
        create_button(frame, 'more left side', self.left_side, 'pack', {'side': 'left'})
        create_button(frame, 'more right side', self.right_side, 'pack', {'side': 'left'})

        self.dictionary = dictionary    # Przypisanie słownika do zmiennej do wprowadzania i zapisywania zmian.
        self.file_path = file_path      # Przypisanie ścieżki z plikiem do zmiennej do funkcji zapisywania zmian.
        self.current_sentence = self.entry_sentence.get()   # Przypisanie przesłanego zdania do zmiennej.
        self.current_sentence_translation = self.entry_sentence_translation.get()

        # Sprawdzenie, czy słowo już istnieje w słowniku:
        if self.entry_question.get() in self.dictionary:
            print(f"The word {question} - {self.dictionary[question]} already exists.")
            self.entry_answer.insert(0, self.dictionary[question][0])
            self.ok_button.config(text='Edit', command=self.edit)
            self.entry_question.config(state="readonly")

    # Metoda edit zamienia istniejące słowo w słowniku, zgodnie z danymi znajdującymi się w polach tekstowych.
    def edit(self):
        # Pobranie aktualnych wartości pytania i odpowiedzi.
        question = self.entry_question.get()
        answer = self.entry_answer.get()

        self.update_dictionary(question, answer)

        print(f"The word {question} - {answer} has been changed.")

    def ok(self):
        # Pobranie aktualnych wartości pytania i odpowiedzi.
        question = self.entry_question.get()
        answer = self.entry_answer.get()

        # Sprawdzenie, czy słowo (pytanie) już istnieje w słowniku
        # (przydatne w przypadku edytowania słowa np. ze względu na usunięcie przecinka).
        if question in self.dictionary:
            print(f"The word {question} - {self.dictionary[question]} already exists.")
            # Wyświetlenie tłumaczenia słowa w polu answer i zmiana nazwy przycisku na 'Edit'.
            self.entry_answer.insert(0, self.dictionary[question][0])
            self.ok_button.config(text='Edit', command=self.edit)
        elif question and answer:
            self.update_dictionary(question, answer)
            print(f"The word {question} - {answer} has been added.")
        # Wyświetlenie informacji o błędzie w przypadku pozostawienia pustego pola.
        else:
            print('Input Error')
        # except TypeError:
        #     print('TypeError')
        #     current_value = []
        #     self.dictionary = {question: current_value}
        #     current_value.append(answer)
        #     current_value.append(self.current_sentence)
        #     save_word_list(self.file_path, self.dictionary)
        #     print(f"The word {question} - {answer} has been added.")

    def right_side(self):
        self.number_right += 1
        sentences = [sentences[1] for sentences in self.pairs]
        unique_sentence = []
        for i, sentence in enumerate(sentences):
            if sentence != sentences[i - 1]:
                unique_sentence.append(sentence)

        try:
            for i, sentence in enumerate(unique_sentence):
                if sentence in self.current_sentence:
                    self.current_sentence = self.current_sentence + ' ' + unique_sentence[i+self.number_right]
                    break
        except IndexError:
            print('IndexError: list index out of range.')

        self.entry_sentence.delete(0, tk.END)
        self.entry_sentence.insert(0, self.current_sentence)

    def left_side(self):
        self.number_right += 1
        sentences = [sentences[1] for sentences in self.pairs]
        unique_sentence = []
        for i, sentence in enumerate(sentences):
            if sentence != sentences[i - 1]:
                unique_sentence.append(sentence)

        try:
            for i, sentence in enumerate(unique_sentence):
                if sentence in self.current_sentence:
                    self.current_sentence = unique_sentence[i-1] + ' ' + self.current_sentence
                    break
        except IndexError:
            print('IndexError: list index out of range.')

        self.entry_sentence.delete(0, tk.END)
        self.entry_sentence.insert(0, self.current_sentence)

    def word_translation(self):
        question = self.entry_question.get()
        self.entry_answer.delete(0, tk.END)
        if 'by' in self.book_name:
            title, author = self.book_name.rsplit(' by ', 1)
            generated = open_ai.book_word_translation('Polish', title, author, self.current_sentence, question)
            if ':' in generated:
                question, answer = check_generated_words(generated)
                self.entry_question.delete(0, tk.END)
                self.entry_question.insert(0, question)
                if question in self.dictionary:
                    self.ok_button.config(text='Edit', command=self.edit)
                    self.entry_question.config(state="readonly")
                self.entry_answer.insert(0, answer)
            else:
                answer = generated
                self.entry_answer.insert(0, answer)
        else:
            self.standard_translation(question)

    def standard_translation(self, question):
        generated = open_ai.article_word_translation('Polish', self.current_sentence, question)
        if ':' in generated:
            question, answer = check_generated_words(generated)
            self.entry_question.delete(0, tk.END)
            self.entry_question.insert(0, question)
            if question in self.dictionary:
                self.ok_button.config(text='Edit', command=self.edit)
                self.entry_question.config(state="readonly")
            self.entry_answer.insert(0, answer)

    def sentence_translation(self):
        question = self.entry_question.get()
        self.entry_sentence_translation.delete(0, tk.END)
        title, author = self.book_name.rsplit(' by ', 1)
        self.current_sentence_translation = open_ai.book_sentence_translation('Polish', title, author,
                                                                              self.current_sentence, question)
        self.entry_sentence_translation.insert(0, self.current_sentence_translation)

    def update_dictionary(self, question, answer):
        """
        Aktualizuje słownik o nowe dane i zapisuje je do pliku.
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
        save_word_list(self.file_path, self.dictionary)

        self.entry_question.delete(0, tk.END)
        self.entry_answer.delete(0, tk.END)
        self.entry_sentence.delete(0, tk.END)
        self.entry_sentence_translation.delete(0, tk.END)

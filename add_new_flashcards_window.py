import tkinter as tk
from configuration import save_word_list
from ui import center_window, create_label, create_entry, create_button, create_frame


class FlashcardsInputDialog:
    def __init__(self, master, dictionary, file_path, question='', sentence='', pairs=''):
        self.top = tk.Toplevel(master)

        self.number_right = 0
        self.pairs = pairs
        center_window(self.top, 900, 210)

        create_label(self.top, 'Question:', 'Arial', None, 'pack', {'side': 'top'})
        self.question = create_entry(self.top, 'top', question)
        create_label(self.top, 'Answer:', 'Arial', None, 'pack', {'side': 'top'})
        self.answer = create_entry(self.top, 'top', '', 35)
        create_label(self.top, 'Sentence:', 'Arial', None, 'pack', {'side': 'top'})
        self.sentence = create_entry(self.top, 'top', sentence, 95)
        create_button(self.top, 'OK', self.ok, 'pack', {'side': 'bottom'})
        frame = create_frame(self.top, 'bottom')
        create_button(frame, 'more left side', self.left_side, 'pack', {'side': 'left'})
        create_button(frame, 'more right side', self.right_side, 'pack', {'side': 'left'})

        self.dictionary = dictionary
        self.file_path = file_path
        self.current_sentence = self.sentence.get()

    def ok(self):
        # Pobranie wprowadzonych danych
        question = self.question.get()
        answer = self.answer.get()
        sentence = self.sentence.get()

        # Sprawdzenie, czy słowo już istnieje w słowniku
        try:
            if question in self.dictionary:
                print(f"The word {question} - {self.dictionary[question]} already exists.")
            elif question and answer:
                current_value = []
                self.dictionary[question] = current_value
                current_value.append(answer)
                current_value.append(sentence)
                save_word_list(self.file_path, self.dictionary)
                print(f"The word {question} - {answer} has been added.")
            else:
                print('Input Error')
        except TypeError:
            current_value = []
            self.dictionary = {question: current_value}
            current_value.append(answer)
            current_value.append(sentence)
            save_word_list(self.file_path, self.dictionary)
            print(f"The word {question} - {answer} has been added.")

        self.question.delete(0, tk.END)
        self.answer.delete(0, tk.END)
        self.sentence.delete(0, tk.END)

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

        self.sentence.delete(0, tk.END)
        self.sentence.insert(0, self.current_sentence)

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

        self.sentence.delete(0, tk.END)
        self.sentence.insert(0, self.current_sentence)

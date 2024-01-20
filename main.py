import tkinter
from main_window import LiviaApp

if __name__ == "__main__":
    root = tkinter.Tk()
    LiviaApp(root)
    root.mainloop()

# TODO: Add an basic translation option.
# TODO: Testing of installation process on other devices.
# TODO: Use inheritance at other windows else main window.
# TODO: Add an exception in the label_calculator function if the waiting time is over 1s.

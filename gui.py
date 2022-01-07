#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox


class Parameters:
    width = 800
    height = 600


def create_button(xpos, ypos, text, padx, pady, side, com):
    button = Button(window, text=text, padx=padx, pady=pady, command=com)
    button.pack(side=side)
    #button.place(x=xpos, y=ypos)
    return button



def fun():
    return window.quit

# Customizacja głównego okna
window = Tk()  # Uruchamianie okna dialogowego
window.title('Test')  # Wstawianie tutułu ramki
#window.iconbitmap('Ikonka_programu.ico')  # Wstawianie ikony
window.configure(width=Parameters.width, height=Parameters.height)  # Ustalanie wielkości okna
window.configure(background="#FFFFFF")  # Ustalanie koloru tła okna

but1 = create_button(100, 100, "sdasd", 200, 50, LEFT, fun())

window.mainloop()

from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


try:
    data = pandas.read_csv('data/vocabulary.csv')
    key = data.keys()
    vocabulary = data.to_dict(orient='records')
except FileNotFoundError:
    data = pandas.read_csv('data/vocabulary_main.csv')
    key = data.keys()
    vocabulary = data.to_dict(orient='records')
except pandas.errors.EmptyDataError:
    data = pandas.read_csv('data/vocabulary_main.csv')
    key = data.keys()
    vocabulary = data.to_dict(orient='records')


def new_word():
    global current_word, show_traslate
    try:
        window.after_cancel(show_traslate)
        current_word = random.choice(vocabulary)
        eng_word = current_word['English']
        keys_en = list(current_word.keys())
        canvas.itemconfig(picture, image=front_pict)
        canvas.itemconfig(head, text=f'{keys_en[0]}', fill='black')
        canvas.itemconfig(word, text=f'{eng_word}', fill='black')
        show_traslate = window.after(3000, translate)
    except IndexError:
        messagebox.showinfo(title='Вітаю', message='Ви вивчили всі слова!')
        exit()


def translate():
    global current_word
    ukr_word = current_word['Українська']
    keys_ua = list(current_word.keys())
    canvas.itemconfig(picture, image=back_pict)
    canvas.itemconfig(head, text=f'{keys_ua[1]}', fill='white')
    canvas.itemconfig(word, text=f'{ukr_word}', fill='white')

def is_known():
    vocabulary.remove(current_word)
    data = pandas.DataFrame(vocabulary)
    data.to_csv('data/vocabulary.csv', index=False)
    new_word()
       

window = Tk()
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
window.resizable(width=False, height=False)
window.title('EN_UA Teacher')

current_word = random.choice(vocabulary)
word = current_word['English']
keys = list(current_word.keys())

#English front
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_pict = PhotoImage(file='img/card_front.png')
back_pict = PhotoImage(file='img/card_back.png')
picture = canvas.create_image(400, 263, image=front_pict)
head = canvas.create_text(400, 150, text=f'{keys[0]}', font=('Ariel', 40, 'italic'))
word = canvas.create_text(400, 263, text=f'{word}', font=('Ariel', 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

wrong_pict = PhotoImage(file='img/wrong.png')
wrong_button = Button(image=wrong_pict, highlightthickness=0, command=new_word)
wrong_button.grid(row=1, column=0)

right_pict = PhotoImage(file='img/right.png')
right_button = Button(image=right_pict, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

show_traslate = window.after(4000, translate)

window.mainloop()
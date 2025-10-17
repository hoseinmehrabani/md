import tkinter as tk
import random


buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '#']


def shuffle_buttons():
    random.shuffle(buttons)
    for i, button in enumerate(button_list):
        button.config(text=buttons[i])


root = tk.Tk()
root.title("Shuffle Buttons")

button_list = []


for i in range(len(buttons)):
    btn = tk.Button(root, text=buttons[i], width=10, height=5)
    btn.grid(row=i // 4, column=i % 4)
    button_list.append(btn)


shuffle_button = tk.Button(root, text="Shuffle", command=shuffle_buttons, width=10, height=2)
shuffle_button.grid(row=3, column=0, columnspan=4)


shuffle_buttons()
root.mainloop()

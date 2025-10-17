from tkinter import *
from tkinter import ttk

def change_color():
    global v
    if v == 0:
        label.config(background="red")
        v = 1
    else:
        label.config(background="blue")
        v = 0

v = 0

master = Tk()
frm = ttk.Frame(master, padding=10)
frm.grid()

label = ttk.Label(frm, text="چراغ")
label.grid(row=0, column=0)

button = ttk.Button(frm, text="کلید", command=change_color)
button1 = ttk.Button(frm, text="کلید", command=change_color)
button.grid(row=1, column=0)
button1.grid(row=1, column=1)

master.mainloop()

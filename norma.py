import tkinter as tk
from tkinter import messagebox


def check_number():
    try:
        number = int(entry.get())
        if 80 <= number <= 100:
            message = "normal"
        elif number < 80:
            message = "negative"
        else:
            message = "positive"

        messagebox.showinfo("result", message)
    except ValueError:
        messagebox.showerror("wrong", "please enter a number valid.")


master = tk.Tk()
master.title("checking number")


label = tk.Label(master, text="please enter a number")
label.pack(pady=10)


entry = tk.Entry(master)
entry.pack(pady=10)

button = tk.Button(master, text="analysis", command=check_number)
button.pack(pady=10)

master.mainloop()

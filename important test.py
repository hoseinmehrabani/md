import tkinter as tk

def get_text():
    text = entry.get()
    label.config(text=text)

root = tk.Tk()

entry = tk.Entry(root)
entry.pack()

button = tk.Button(root, text="گرفتن متن", command=get_text)
button.pack()

label = tk.Label(root)
label.pack()

root.mainloop()
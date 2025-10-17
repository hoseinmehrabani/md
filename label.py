import tkinter as tk

def move_label_right():
    x = label.winfo_x()
    label.place(x=x+10)

root = tk.Tk()

label = tk.Label(root, text='Hello, World!')
label.pack()

button = tk.Button(root,padx=20,pady=20, text='Move Right', command=move_label_right)
button.pack()
def enter(event):
    button.config(text='Mouse has entered!')
def leave(event):
     button.config(text='Mouse has left!')
button.bind('<Enter>', enter)
button.bind('<Leave>', leave)
root.mainloop()
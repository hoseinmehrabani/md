import tkinter as tk 
def calculate(): 
    try: 
        expression = entry.get() 
        result = eval(expression) 
        label.config(text="Result: " + str(result))
    except: 
        label.config(text="Invalid input") 
window = tk.Tk()
window.title("Simple Calculator") 
entry = tk.Entry(window, width=30)
entry.pack()
button = tk.Button(window, text="Calculate", command=calculate) 
button.pack() 
label = tk.Label(window, text="Result:") 
label.pack()
#window.iconbitmap('C:/Users/mhm/Downloads/script.ico') 
window.mainloop()
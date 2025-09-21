import tkinter as tk

def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            result = eval(str(entry.get()))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, text)


root = tk.Tk()
root.title("Simple Calculator")
root.geometry("300x400")


entry = tk.Entry(root, font="Arial 20")
entry.pack(fill=tk.BOTH, ipadx=10, pady=10)


buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]


for row in buttons:
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    for btn_text in row:
        btn = tk.Button(frame, text=btn_text, font="Arial 18")
        btn.pack(side="left", expand=True, fill="both")
        btn.bind("<Button-1>", click)

root.mainloop()
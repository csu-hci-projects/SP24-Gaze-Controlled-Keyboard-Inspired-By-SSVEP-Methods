import tkinter as tk

import tkinter
from turtle import color

def find_center(x, y, w, h):
    return x + w//2, y + h//2

def find_center_rect(x1, x2, y1, y2):
    return x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2 + 50

master=tkinter.Tk()
master.title("Tscan Experiment - Gaze Controlled Keyboard inspired by SSVEP Methods")

height = 900
width = 1400
x = (master.winfo_screenwidth()//2)-(width//2) 
y = (master.winfo_screenheight()//2)-(height//2) 
master.geometry("{}x{}+{}+{}".format(width, height, x, y)) 

txt = tk.Label(master, text="", bg="black", fg="white", font=("Times New Roman", 20))

overall_str = ""



c = tk.Canvas(master, width=1400, height=800, bg="black")

c.pack(pady = 5, padx=10)

### Q1 ###
w  = 700 - 175 - 500
h = 75 + 25
r1 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t1 = c.create_text(x, y, text="A, B, C, D, E, F", font=("Courier", 30) , fill="black")

### Q2 ###
w  = 700 - 175 - 500
h = 800 - 25 - 300 - 15
r2 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t2 = c.create_text(x, y, text="G, H, I, J, K, L", font=("Courier", 30) , fill="black")

### Q3 ###
w  = 700 + 150
h = 75 + 25
r3 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t3 = c.create_text(x, y, text="M, N, O, P, Q, R", font=("Courier", 30) , fill="black")

### Q4 ###
w  = 700 + 150 
h = 800 - 25 - 300 - 15
r4 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t4 = c.create_text(x, y, text="S, T, U, V, W, X, Y, Z", font=("Courier", 30) , fill="black")


txt="Sample Word"

tw = c.create_text(700-25, 50, text=txt, font=("Courier", 30) ,fill="white")

x, y = find_center_rect(700-175, 700+150, 275,  800 - 25 - 300 - 15)
tnz = c.create_text(x, y, text="Neutral Zone", font=("Courier", 30) ,fill="white")
master.configure(background='black')
master.mainloop()
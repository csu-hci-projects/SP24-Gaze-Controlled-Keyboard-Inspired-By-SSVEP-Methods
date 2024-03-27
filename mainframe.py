import tkinter as tk
from tkinter import ttk

import tkinter
from turtle import color
from typing import Collection

def find_center(x, y, w, h):
    return x + w//2, y + h//2

def find_center_rect(x1, x2, y1, y2):
    return x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2 + 50

master=tkinter.Tk()
master.title("Gaze Controlled Keyboard inspired by SSVEP Methods")

height = 900
width = 1400
x = (master.winfo_screenwidth()//2)-(width//2) 
y = (master.winfo_screenheight()//2)-(height//2) 
master.geometry("{}x{}+{}+{}".format(width, height, x, y)) 

txt = tk.Label(master, text="", bg="black", fg="white", font=("Times New Roman", 20))



global level, reset, current, c, t1, t2, t3, t4, overall_str, tw, cont, start, T_scan, pbar, pbar_vis

T_scan = 3
start = 0
overall_str = ""
level = 0
reset = False
current = ""
c = tk.Canvas(master, width=1400, height=800, bg="black")
pbar = ttk.Progressbar(c, orient="horizontal",length=300, mode='determinate', maximum=100)
options = ["A, B, C, D, E, F", "G, H, I, J, K, L", "M, N, O, P, Q, R", "S, T, U, V, W, X, Y, Z"]
global tnz
cont = True
c.pack(pady = 5, padx=10)





    



### Q1 ###
w  = 700 - 175 - 500
h = 75 + 25
r1 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1", tags="q1")
c.tag_bind("q1", "<Button-1>", lambda i: clicked(i, 1))
x, y = find_center(w, h, 500, 275)
a1, b1 = find_center(w, h, 500, 275)
c.tag_bind("q1", "<Enter>", lambda i: timer(i, a1, b1, 1))
c.tag_bind("q1", "<Leave>", lambda i: cont_timer(i))
t1 = c.create_text(x, y, text="A, B, C, D, E, F", font=("Courier", 30) , fill="black")
#pbar.place(x=x-150, y=y+50)
pbar_vis = False

### Q3 ###
w  = 700 - 175 - 500
h = 800 - 25 - 300 - 15
r3 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1", tags="q3")
c.tag_bind("q3", "<Button-1>", lambda i: clicked(i, 3))
x, y = find_center(w, h, 500, 275)
a3, b3 = find_center(w, h, 500, 275)
c.tag_bind("q3", "<Enter>", lambda i: timer(i, a3, b3, 3))
c.tag_bind("q3", "<Leave>", lambda i: cont_timer(i))
t3 = c.create_text(x, y, text="M, N, O, P, Q, R", font=("Courier", 30) , fill="black")

### Q2 ###
w  = 700 + 150
h = 75 + 25
r2 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1", tags="q2")
c.tag_bind("q2", "<Button-1>", lambda i: clicked(i, 2))
x, y = find_center(w, h, 500, 275)
a2, b2 = find_center(w, h, 500, 275)
c.tag_bind("q2", "<Enter>", lambda i: timer(i, a2, b2, 2))
c.tag_bind("q2", "<Leave>", lambda i: cont_timer(i))
t2 = c.create_text(x, y, text="G, H, I, J, K, L", font=("Courier", 30) , fill="black")

### Q4 ###
w  = 700 + 150 
h = 800 - 25 - 300 - 15
r4 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1", tags="q4")
c.tag_bind("q4", "<Button-1>", lambda i: clicked(i, 4))
x, y = find_center(w, h, 500, 275)
a4, b4 = find_center(w, h, 500, 275)
c.tag_bind("q4", "<Enter>", lambda i: timer(i, a4, b4, 4))
c.tag_bind("q4", "<Leave>", lambda i: cont_timer(i))
t4 = c.create_text(x, y, text="S, T, U, V, W, X, Y, Z", font=("Courier", 30) , fill="black")


txt="Sample Word"

tw = c.create_text(700-25, 50, text=txt, font=("Courier", 30) ,fill="white")

def clicked(event,q):
    global level, reset, current, c, t1, t2, t3, t4, options, overall_str, tw
    col_texts = [t1, t2, t3, t4]
    if level == 0:
        current = options[q-1]
        level += 1
        letters = current.split(', ')
        temp = []
        for i in range(0, len(letters)-1, 2):
            cur = letters[i] +  ", " + letters[i+1]
            temp.append(cur)
            c.itemconfig(col_texts[i//2], text=cur)
        if len(letters) == 6:
            c.itemconfig(col_texts[-1], text="")
        options = temp
    elif level == 1:
        if q <= len(options):
            current = options[q-1]
            print(current)
            level += 1
            letters = current.split(', ')
            options = letters
            for i in range(2):
                c.itemconfig(col_texts[i], text=letters[i])
            for i in range(2, 4):
                c.itemconfig(col_texts[i], text="")
    elif level == 2:
        if q <= 2:
            choice = options[q-1]
            overall_str += choice
            c.itemconfig(tw, text=overall_str)
            level = 0
            options = ["A, B, C, D, E, F", "G, H, I, J, K, L", "M, N, O, P, Q, R", "S, T, U, V, W, X, Y, Z"]
            for i in range(4):
                c.itemconfig(col_texts[i], text=options[i])

def cont_timer(event):
    global cont, start, tnz, T_scan, pbar, pbar_vis
    cont = False
    c.itemconfig(tnz, text="{per:.2f}%".format(per = (100*((start-1)/1000)/T_scan)) )
    if pbar_vis == True:
        pbar.place_forget()
        pbar_vis = False
    

def timer(event, x_s, y_s, q):
    global tnz, start, cont, T_scan, pbar, pbar_vis
    cont = True
    start = 0
    if pbar_vis == False:
        print(x_s, y_s)
        pbar.place(x=x_s-150, y=y_s+50)
        pbar_vis = True
    def rec_timer():
        global tnz, start, cont, pbar, pbar_vis
        if (100*(start/1000)/T_scan) <= 100:
            c.itemconfig(tnz, text="{per:.2f}%".format(per = (100*(start/1000)/T_scan)) )
            pbar['value'] = (100*(start/1000)/T_scan)
            start += 1
            if cont == True:
                master.after(1, rec_timer)
            else:
                return
        else:
            clicked(None, q)
            if pbar_vis == True:
                pbar.place_forget()
                pbar_vis = False
        
        
    rec_timer()




x, y = find_center_rect(700-175, 700+150, 275,  800 - 25 - 300 - 15)
tnz = c.create_text(x, y, text="Neutral Zone", font=("Courier", 30) ,fill="white")
master.configure(background='black')
master.mainloop()
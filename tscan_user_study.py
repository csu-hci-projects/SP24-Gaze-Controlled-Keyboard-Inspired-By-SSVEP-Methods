import tkinter as tk
from tkinter import *
from turtle import color
import random
import time

# Define all the functions

def find_center(x, y, w, h):
    return x + w//2, y + h//2

def find_center_rect(x1, x2, y1, y2):
    return x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2 + 50

def on_key_press(event):
    global i, txt2, tw2, start_time, end_time, elapsed_time
    
    # Stop the stopwatch
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time

    if i<12:
        print(f"i: {i} - letter: {random_letters[i]} - key pressed: {event.char} - elapsed time: {elapsed_time} seconds")
    i = i + 1
    if i<12: # iteration 2-12
        # c.delete(tw2)
        txt2 = random_letters[i]
        start_time = time.time()
        # tw2 = c.create_text(700-25, 70, text=txt2, font=("Courier", 50) ,fill="white")
        c.itemconfig(tw2, text=txt2)
    else: # finish
        print("Finish")
        c.delete(tw)
        c.delete(tw2)
        tw2 = c.create_text(700-25, 50, text="Thank you for your participation!", font=("Courier", 30) ,fill="white")

# Choose 12 random letters for the Tscan experiment
Q1 = ['A', 'B', 'C', 'D', 'E', 'F']
Q2 = ['G', 'H', 'I', 'J', 'K', 'L']
Q3 = ['M', 'N', 'O', 'P', 'Q', 'R']
Q4 = ['S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
random_letters_Q1 = random.sample(Q1, 3)
random_letters_Q2 = random.sample(Q2, 3)
random_letters_Q3 = random.sample(Q3, 3)
random_letters_Q4 = random.sample(Q4, 3)
# random_letters = [item for sublist in [random_letters_Q1, random_letters_Q2, random_letters_Q3, random_letters_Q4] for item in sublist]
# random.shuffle(random_letters)
# print(random_letters)
# Modified - The first 4 letters will be taken from different quarters, the rest order will be free
random_letters_group1 = [random_letters_Q1[0],random_letters_Q2[0],random_letters_Q3[0],random_letters_Q4[0]]
random.shuffle(random_letters_group1)
# print(random_letters_group1)
random_letters_group2 = [random_letters_Q1[1],random_letters_Q2[1],random_letters_Q3[1],random_letters_Q4[1],random_letters_Q1[2],random_letters_Q2[2],random_letters_Q3[2],random_letters_Q4[2]]
random.shuffle(random_letters_group2)
# print(random_letters_group2)
random_letters = random_letters_group1 + random_letters_group2
print(random_letters)

# GUI
master=tk.Tk()
master.title("Tscan Experiment - Gaze Controlled Keyboard inspired by SSVEP Methods")

height = 900
width = 1400
x = (master.winfo_screenwidth()//2)-(width//2) 
y = (master.winfo_screenheight()//2)-(height//2) 
master.geometry("{}x{}+{}+{}".format(width, height, x, y)) 

txt = tk.Label(master, text="", bg="black", fg="white", font=("Times New Roman", 20))
overall_str = ""

c = tk.Canvas(master, width=1400, height=800, bg="black")
c.pack(pady=5, padx=10)

### Q1 ###
w  = 700 - 175 - 500
h = 75 + 25
r1 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t1 = c.create_text(x, y, text="A, B, C, D, E, F", font=("Courier", 30), fill="black")
t1_cmd = c.create_text(w + 70, h + 20, text="Press '1'", font=("Courier", 20), fill="red")

### Q2 ###
w  = 700 + 150
h = 75 + 25
r3 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t3 = c.create_text(x, y, text="G, H, I, J, K, L", font=("Courier", 30), fill="black")
t3_cmd = c.create_text(w + 70, h + 20, text="Press '2'", font=("Courier", 20), fill="red")

### Q3 ###
w  = 700 - 175 - 500
h = 800 - 25 - 300 - 15
r2 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t2 = c.create_text(x, y, text="M, N, O, P, Q, R", font=("Courier", 30), fill="black")
t2_cmd = c.create_text(w + 70, h + 20, text="Press '3'", font=("Courier", 20), fill="red")

### Q4 ###
w  = 700 + 150 
h = 800 - 25 - 300 - 15
r4 = c.create_rectangle(w, h, w + 500, h + 275, fill="#b5b4b1")
x, y = find_center(w, h, 500, 275)
t4 = c.create_text(x, y, text="S, T, U, V, W, X, Y, Z", font=("Courier", 30), fill="black")
t4_cmd = c.create_text(w + 70, h + 20, text="Press '4'", font=("Courier", 20), fill="red")

### Neutral Zone ###
x, y = find_center_rect(700-175, 700+150, 275,  800 - 25 - 300 - 15)
tnz = c.create_text(x, y, text="Neutral Zone", font=("Courier", 30), fill="white")

### Instructions ###
txt="Find the following letter:"
tw = c.create_text(700-25, 20, text=txt, font=("Courier", 30), fill="white")

# Iteration 1
i = 0 
txt2 = random_letters[i]
# Start the stopwatch
start_time = time.time()
tw2 = c.create_text(700-25, 70, text=txt2, font=("Courier", 50), fill="white")

# Call the key press listener
master.bind("<KeyPress>", on_key_press)

master.configure(background='black')
master.mainloop()
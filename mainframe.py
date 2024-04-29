import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

import statistics as st

import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment


import tkinter
from turtle import bgcolor, color
from typing import Collection

import cv2
from gaze_tracking import GazeTracking
import time

import pandas as pd

gaze = GazeTracking()
webcam = cv2.VideoCapture(1)



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



global level, reset, current, c, t1, t2, t3, t4, overall_str, tw, cont, start, T_scan, pbar, pbar_vis, predict_func
predict_func = {}

T_scan = 1
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

def get_reading():
    _, frame = webcam.read()
    gaze.refresh(frame)

    new_frame = gaze.annotated_frame()
    text = ""

    locx, locy = gaze.horizontal_ratio(), gaze.vertical_ratio()
    return locx, locy

def next():
    global calibration_canvas, c, predict_func, kmeans,c, tw, T_scan, prev_100, counter
    calibration_canvas.destroy()
    c.pack(pady = 5, padx=10)
    global start_time, prev_l
    start_time = time.time()
    prev_l = 1
    prev_10 = [1]
    counter = 0
    def rec_read():
        global start_time, prev_l, prev_100, counter
        quarters = [r1, r2, r3, r4]
        x, y = get_reading()

        def relabel(c):
            return predict_func[c]

        if type(x) == float and type(y) == float:#try:
            l = predict_func[kmeans.predict([[x, y]])[0]]
                
            for qs in range(len(quarters)):
                if qs == l-1:
                    c.itemconfig(quarters[qs], fill="blue")
                else:
                    c.itemconfig(quarters[qs], fill="grey")
            if l != prev_l:
                start_time = time.time()
            if time.time() - start_time > T_scan:
                clicked(None, l)
                start_time = time.time()
            c.itemconfig(tnz, text="{per:.2f}%".format(per = (time.time() - start_time) ))
            prev_l = l
            prev_100 = []
        else:
            c.itemconfig(tnz, text="{per:.2f}%".format(per = (time.time() - start_time)) )
        master.after(1, rec_read)
        counter += 1
    master.after(1, rec_read)

    

global cur_i, instruction, tcc, cur_j, tcc_rec, calibration_canvas, data, kmeans
data = {"x": [], "y": [], "label": []}
calibration_canvas = tk.Canvas(master, width=1400, height=800, bg="black")
but_test = tk.Button(calibration_canvas, text="next", command=next)

### Q1 ###
w  = 700 - 175 - 500
h = 75 + 25 - 50
r1_c = calibration_canvas.create_rectangle(w, h, w + 500, h + 275, fill="black")
x, y = find_center(w, h, 500, 275)
calibration_canvas.create_text(x, y, text="*", font=("Courier", 30) , fill="black")


### Q3 ###
w  = 700 - 175 - 500
h = 800 - 25 - 300 - 15
r3_c = calibration_canvas.create_rectangle(w, h, w + 500, h + 275, fill="black")
x, y = find_center(w, h, 500, 275)
calibration_canvas.create_text(x, y, text="*", font=("Courier", 30) , fill="black")

### Q2 ###
w  = 700 + 150
h = 75 + 25 - 50
r2_c = calibration_canvas.create_rectangle(w, h, w + 500, h + 275, fill="black")
x, y = find_center(w, h, 500, 275)
calibration_canvas.create_text(x, y, text="*", font=("Courier", 30) , fill="black")

### Q4 ###
w  = 700 + 150 
h = 800 - 25 - 300 - 15
r4_c = calibration_canvas.create_rectangle(w, h, w + 500, h + 275, fill="black")
x, y = find_center(w, h, 500, 275)
calibration_canvas.create_text(x, y, text="*", font=("Courier", 30) , fill="black")


title_cal="Calibration Phase"

tc = calibration_canvas.create_text(700-25, 50, text=title_cal, font=("Courier", 30) ,fill="white")

x, y = find_center_rect(700-175, 700+150, 275,  800 - 25 - 300 - 15)


cur_i = 1
cur_j = 1
instruction = calibration_canvas.create_text(x, y+100, text="Stare at visible box for 5 seconds", font=("Courier", 30) ,fill="white")

def start_cal(event):
    global cur_i, instruction, tcc, cur_j, tcc_rec, calibration_canvas, data, predict_func, kmeans
    if cur_i >= 5:
        print("done")
        calibration_canvas.itemconfig(r4_c, fill="black")

        df = pd.DataFrame(data)

        fig = Figure(figsize = (5, 5), dpi = 100) 

        def biject_label(coord_list1, coord_list2):
            distances = cdist(coord_list1, coord_list2)
            
            row_ind, col_ind = linear_sum_assignment(distances)
            
            dic = {}
            for row, col in zip(row_ind, col_ind):
                dic[coord_list1[row]] = coord_list2[col]
                
            bij = {}
            i = 1
            for c in coord_list2:
                bij[c] = i
                i += 1
            bijection = {}
            for c in coord_list1:
                bijection[c] = bij[dic[c]]
            mapping = {}
            i = 0
            for c in coord_list1:
                mapping[i] = bijection[c]
                i += 1
            return mapping

        def biject_color(coord_list1, coord_list2):
            distances = cdist(coord_list1, coord_list2)
            
            row_ind, col_ind = linear_sum_assignment(distances)
            
            dic = {}
            for row, col in zip(row_ind, col_ind):
                dic[coord_list1[row]] = coord_list2[col]
                
            color_bijection = {}
            colors = ["black", "red", "green", "yellow", "blue"]
            i = 1
            for c in coord_list2:
                color_bijection[c] = colors[i]
                i += 1
            bijection = {}
            for c in coord_list1:
                bijection[c] = color_bijection[dic[c]]
            return bijection

        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)
        cluster_means = [(np.mean(df[["x"]][df["label"] == i].to_numpy()), np.mean(df[["y"]][df["label"] == i].to_numpy())) for i in range(1, 5)]
        data_temp = []
        colors = ["black", "red", "green", "yellow", "blue"]
        for index, row in df.iterrows():
            ax1.scatter(row['x'], row['y'], color=colors[int(row['label'])])
            dat = [row['x'], row['y']]
            data_temp.append(dat)
        data_temp = np.array(data_temp)
        kmeans = KMeans(n_clusters=4).fit(data_temp)
        labels = kmeans.fit_predict(data_temp)
        centers = []
        for item in kmeans.cluster_centers_.tolist():
            centers.append((item[0], item[1]))
        order = biject_color(centers, cluster_means)
        predict_func = biject_label(centers, cluster_means) # bijective function
        colors = [order[c] for c in order]
        i = 0
        for index, row in df.iterrows():
            ax2.scatter(row['x'], row['y'], color=colors[labels[i]])
            i += 1
        ax1.set_title("Recorded")
        ax2.set_title("Predicted")
        temp_plot_canv = tk.Canvas(master=calibration_canvas)
        canvas_plt = FigureCanvasTkAgg(fig, master = temp_plot_canv)   
        canvas_plt.draw() 
        res_text = tk.Label(calibration_canvas, text="Results", bg="black", fg="white", font=("Courier", 30)).pack(pady=20, padx=20)
        calibration_canvas.delete(tc)
        calibration_canvas.delete(instruction)
        canvas_plt.get_tk_widget().pack()
        temp_plot_canv.pack(pady=20, padx=20)
        btn = tk.Button(calibration_canvas, text = 'Finish', bd = '5',
                          command = next).pack(pady=20, padx=20)


    elif cur_i <= 4:
        print("clicked", cur_i)
        if cur_i == 1:
            if cur_j == 1:
                calibration_canvas.itemconfig(r1_c, fill="#b5b4b1")
                calibration_canvas.itemconfig(tcc, text="Start 10 sec")
                cur_j += 1
            elif cur_j == 2:
                calibration_canvas.itemconfig(tcc_rec, fill="black")
                calibration_canvas.itemconfig(tcc, text="")
                cont = True
                start_time_obj = time.time()
                while cont:
                    _, frame = webcam.read()
                    gaze.refresh(frame)

                    new_frame = gaze.annotated_frame()
                    text = ""

                    locx, locy = gaze.horizontal_ratio(), gaze.vertical_ratio()
                    print(locx, locy, len(data["x"]))
                    data["x"].append(locx)
                    data["y"].append(locy)
                    data["label"].append(1)
                    if time.time() - start_time_obj > 5:
                        cont = False
                calibration_canvas.itemconfig(tcc_rec, fill="#b5b4b1")
                calibration_canvas.itemconfig(tcc, text="Continue")
                cur_j = 1
                cur_i += 1
        elif cur_i == 2:
            print(cur_j)
            if cur_j == 1:
                calibration_canvas.itemconfig(r2_c, fill="#b5b4b1")
                calibration_canvas.itemconfig(r1_c, fill="black")
                calibration_canvas.itemconfig(tcc, text="Start 10 sec")
                cur_j += 1
            elif cur_j == 2:
                calibration_canvas.itemconfig(tcc_rec, fill="black")
                calibration_canvas.itemconfig(tcc, text="")
                cont = True
                start_time_obj = time.time()
                while cont:
                    _, frame = webcam.read()
                    gaze.refresh(frame)

                    new_frame = gaze.annotated_frame()
                    text = ""

                    locx, locy = gaze.horizontal_ratio(), gaze.vertical_ratio()
                    print(locx, locy, len(data["x"]))
                    data["x"].append(locx)
                    data["y"].append(locy)
                    data["label"].append(2)
                    if time.time() - start_time_obj > 5:
                        cont = False
                calibration_canvas.itemconfig(tcc_rec, fill="#b5b4b1")
                calibration_canvas.itemconfig(tcc, text="Continue")
                cur_j = 1
                cur_i += 1
        elif cur_i == 3:
            if cur_j == 1:
                calibration_canvas.move(instruction, 0, -200)
                calibration_canvas.itemconfig(r3_c, fill="#b5b4b1")
                calibration_canvas.itemconfig(r2_c, fill="black")
                calibration_canvas.itemconfig(tcc, text="Start 10 sec")
                cur_j += 1
            elif cur_j == 2:
                calibration_canvas.itemconfig(tcc_rec, fill="black")
                calibration_canvas.itemconfig(tcc, text="")
                cont = True
                start_time_obj = time.time()
                while cont:
                    _, frame = webcam.read()
                    gaze.refresh(frame)

                    new_frame = gaze.annotated_frame()
                    text = ""

                    locx, locy = gaze.horizontal_ratio(), gaze.vertical_ratio()
                    print(locx, locy, len(data["x"]))
                    data["x"].append(locx)
                    data["y"].append(locy)
                    data["label"].append(3)
                    if time.time() - start_time_obj > 5:
                        cont = False
                calibration_canvas.itemconfig(tcc_rec, fill="#b5b4b1")
                calibration_canvas.itemconfig(tcc, text="Continue")
                cur_j = 1
                cur_i += 1
        elif cur_i == 4:
            if cur_j == 1:
                calibration_canvas.itemconfig(r4_c, fill="#b5b4b1")
                calibration_canvas.itemconfig(r3_c, fill="black")
                calibration_canvas.itemconfig(tcc, text="Start 10 sec")
                cur_j += 1
            elif cur_j == 2:
                calibration_canvas.itemconfig(tcc_rec, fill="black")
                calibration_canvas.itemconfig(tcc, text="")
                cont = True
                start_time_obj = time.time()
                while cont:
                    _, frame = webcam.read()
                    gaze.refresh(frame)

                    new_frame = gaze.annotated_frame()
                    text = ""

                    locx, locy = gaze.horizontal_ratio(), gaze.vertical_ratio()
                    print(locx, locy, len(data["x"]))
                    data["x"].append(locx)
                    data["y"].append(locy)
                    data["label"].append(4)
                    if time.time() - start_time_obj > 5:
                        cont = False
                calibration_canvas.itemconfig(tcc_rec, fill="#b5b4b1")
                calibration_canvas.itemconfig(tcc, text="Done")
                cur_j = 1
                cur_i += 1
                df = pd.DataFrame(data)
                df.to_csv("data.csv")
        #cur_i += 1
    

tcc_rec = calibration_canvas.create_rectangle(x-150, y-30, x+150, y+30, fill="#b5b4b1", tags="cal_button")
tcc = calibration_canvas.create_text(x, y, text="Start", font=("Courier", 30) ,fill="white", tags="cal_button")
calibration_canvas.tag_bind("cal_button", "<Button-1>", start_cal)
#instruction = tcc = calibration_canvas.create_text(x, y+100, text="Stare at visible box for 10 seconds", font=("Courier", 30) ,fill="white")
##b5b4b1

calibration_canvas.pack(pady = 5, padx=10)
#but_test.pack()






    



### Q1 ###
w  = 700 - 175 - 500
h = 75 + 25- 50
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
h = 75 + 25- 50
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
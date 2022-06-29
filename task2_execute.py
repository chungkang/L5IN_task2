import tkinter as tk
from tkinter import ttk

import os
import PIL
from datetime import datetime
import cv2

import module.rectify as rectify
import module.binary as binary
import module.neighbors as neighbors
from module.scrollimage import ScrollableImage   

current_path = os.path.dirname(os.path.realpath(__file__)) #파일 경로

# Settings
root = tk.Tk()
root.title("Map Generator from Rescue Plans")
root.geometry("600x400")
# root.resizable(False, False)


def image_find():
	image_ext = r"*.jpg *.jpeg *.png"
	file = tk.filedialog.askopenfilenames(filetypes=(("Image file",image_ext),("all file", "*.*")), initialdir=current_path)
	en_filepath.delete(0,tk.END)
	en_filepath.insert(tk.END, file[0])

def popup_origin_image():
    win_image = tk.Toplevel()
    win_image.wm_title("1. Image")

    fixed_width = 600
    image1 = PIL.Image.open(en_filepath.get())
    image_percent = (fixed_width/float(image1.size[0]))
    image_height = int(float(image1.size[1])*float(image_percent))
    image1 = image1.resize((fixed_width, image_height), PIL.Image.NEAREST)
    photo1 = PIL.ImageTk.PhotoImage(image1)
    label1 = tk.Label(win_image, image=photo1)
    label1.image = photo1
    label1.grid(row=0, column=0)

    label1.bind("get_coordinate",getorigin)

def getorigin(eventorigin):
    global x,y
    x = eventorigin.x
    y = eventorigin.y
    tk.messagebox.showinfo("x y coordinate", 'x: %s  y: %s' % (x,y) )

def rectify_image():
    image_points = str(image_point_1.get()) + "\n" + str(image_point_2.get()) + "\n" + str(image_point_3.get()) + "\n" + str(image_point_4.get())
    control_points = str(control_point_1.get()) + "\n" + str(control_point_2.get()) + "\n" + str(control_point_3.get()) + "\n" + str(control_point_4.get())

    # rectify image
    new_dir_nm = ''
    e_image = rectify.fn_rectify(new_dir_nm,en_filepath.get(),image_points,control_points,value1.get(),value2.get())

def popup_rectify_image():
    win_rectify = tk.Toplevel()
    win_rectify.wm_title("2. Rectify")

    fixed_width = 600
    image1 = PIL.Image.open('02_rectify.png')
    image_percent = (fixed_width/float(image1.size[0]))
    image_height = int(float(image1.size[1])*float(image_percent))
    image1 = image1.resize((fixed_width, image_height), PIL.Image.NEAREST)
    photo1 = PIL.ImageTk.PhotoImage(image1)
    label1 = tk.Label(win_rectify, image=photo1)
    label1.image = photo1
    label1.grid(row=6, column=0, columnspan=4)

def binarization_image():
    new_dir_nm = ''
    bin_image = binary.fn_binary(new_dir_nm,'02_rectify.png',True)

def popup_binarization_image():
    win_rectify = tk.Toplevel()
    win_rectify.wm_title("3. Binarization")

    fixed_width = 600
    image1 = PIL.Image.open('03_binary.png')
    image_percent = (fixed_width/float(image1.size[0]))
    image_height = int(float(image1.size[1])*float(image_percent))
    image1 = image1.resize((fixed_width, image_height), PIL.Image.NEAREST)
    photo1 = PIL.ImageTk.PhotoImage(image1)
    label1 = tk.Label(win_rectify, image=photo1)
    label1.image = photo1
    label1.grid(row=6, column=0, columnspan=4)

def neighbor():
    print('neighbor')

def vectorize():
    print('vectorize')

def filtering():
    print('filtering')

# grid setting
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.columnconfigure(5, weight=1)
# root.container.rowconfigure(0, 1)


# 1. Select Image - popup image show
tk.Label(root, text="1. Select Image: ").grid(row=0,column=0,sticky=tk.W)

en_filepath = tk.Entry(root)    
en_filepath.grid(row=0,column=1,columnspan=3)

tk.Button(root, text="Find", command=image_find).grid(row=0,column=4)

tk.Button(root, text="Show Image", command=popup_origin_image).grid(row=0,column=5)


# 2. Rectify - popup image show
tk.Label(root, text="2. Rectify").grid(row=1,column=0,sticky=tk.W)

tk.Button(root, text="Rectify", command=rectify_image).grid(row=1,column=4)

tk.Button(root, text="Show Image", command=popup_rectify_image).grid(row=1,column=5)


image_point_1_nm = tk.Label(root, text="Image Point 1: ")
image_point_1_nm.grid(row=2, column=0)

image_point_1 = tk.Entry(root)
image_point_1.insert(0, "427;1013")
image_point_1.grid(row=2, column=1, columnspan=2)

control_point_1_nm = tk.Label(root, text="Control Point 1: ")
control_point_1_nm.grid(row=2, column=3)

control_point_1 = tk.Entry(root)
control_point_1.insert(0, "0;0")
control_point_1.grid(row=2, column=4, columnspan=2)


image_point_2_nm = tk.Label(root, text="Image Point 2: ")
image_point_2_nm.grid(row=3, column=0)

image_point_2 = tk.Entry(root)
image_point_2.insert(0, "403;1580")
image_point_2.grid(row=3, column=1, columnspan=2)

control_point_2_nm = tk.Label(root, text="Control Point 2: ")
control_point_2_nm.grid(row=3, column=3)

control_point_2 = tk.Entry(root)
control_point_2.insert(0, "0;880")
control_point_2.grid(row=3, column=4, columnspan=2)


image_point_3_nm = tk.Label(root, text="Image Point 3: ")
image_point_3_nm.grid(row=4, column=0)

image_point_3 = tk.Entry(root)
image_point_3.insert(0, "3810;1223")
image_point_3.grid(row=4, column=1, columnspan=2)

control_point_3_nm = tk.Label(root, text="Control Point 3: ")
control_point_3_nm.grid(row=4, column=3)
control_point_3 = tk.Entry(root)
control_point_3.insert(0, "4075;85")
control_point_3.grid(row=4, column=4, columnspan=2)


image_point_4_nm = tk.Label(root, text="Image Point 4: ")
image_point_4_nm.grid(row=5, column=0)

image_point_4 = tk.Entry(root)
image_point_4.insert(0, "3833;1590")
image_point_4.grid(row=5, column=1, columnspan=2)

control_point_4_nm = tk.Label(root, text="Control Point 4: ")
control_point_4_nm.grid(row=5, column=3)

control_point_4 = tk.Entry(root)
control_point_4.insert(0, "4075;880")
control_point_4.grid(row=5, column=4, columnspan=2)


control_description = tk.Label(root, text="ex) 1000;200 (x;y)")
control_description.grid(row=6, column=0, columnspan=3)

value1 = tk.Entry(root)
value1.insert(0, "1000")
value1.grid(row=6, column=3)

value2 = tk.Entry(root)
value2.insert(0, "-2500")
value2.grid(row=6, column=4)

# 3. Binarization - popup image show
tk.Label(root, text="3. Binarization").grid(row=7,column=0,sticky=tk.W)
tk.Button(root, text="Binarization", command=binarization_image).grid(row=7,column=4)
tk.Button(root, text="Show Image", command=popup_binarization_image).grid(row=7,column=5)

# 4. Neighbor - popup image show
tk.Label(root, text="4. Neighbor").grid(row=8,column=0,sticky=tk.W)
tk.Button(root, text="Neighbor", command=neighbor).grid(row=8,column=4)

# 5. Vetorize - popup image show
tk.Label(root, text="5. Vetorize").grid(row=9,column=0,sticky=tk.W)
tk.Button(root, text="Vetorize", command=vectorize).grid(row=9,column=4)

# 6. Filtering - popup image show
tk.Label(root, text="6. Filtering").grid(row=10,column=0,sticky=tk.W)
tk.Button(root, text="Filtering", command=filtering).grid(row=10,column=4)

root.mainloop()
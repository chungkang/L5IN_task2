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

def popup_image():
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

def popup_rectify():
    win = tk.Toplevel()
    win.wm_title("2. Rectify")

    l = tk.Label(win, text="Input")
    l.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)


def popup_binarization():
    win = tk.Toplevel()
    win.wm_title("3. Binarization")

    l = tk.Label(win, text="Input")
    l.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

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
# root.container.rowconfigure(0, 1)


# 1. Select Image - popup image show
tk.Label(root, text="1. Select Image: ").grid(row=0,column=0)
tk.Button(root, text="Show Image", width=10, command=popup_image).grid(row=0,column=2)
en_filepath = tk.Entry(root)
en_filepath.grid(row=1,column=0,columnspan=2)
tk.Button(root, text="Find", width=10, command=image_find).grid(row=1,column=2)

# 2. Rectify - popup image show
tk.Label(root, text="2. Rectify").grid(row=2,column=0)
tk.Button(root, text="Rectify", width=10, command=popup_rectify).grid(row=2,column=1)

# 3. Binarization - popup image show
tk.Label(root, text="3. Binarization").grid(row=3,column=0)
tk.Button(root, text="Binarization", width=10, command=popup_binarization).grid(row=3,column=1)

# 4. Neighbor - popup image show
tk.Label(root, text="4. Neighbor").grid(row=4,column=0)
tk.Button(root, text="Neighbor", width=10, command=neighbor).grid(row=4,column=1)

# 5. Vetorize - popup image show
tk.Label(root, text="5. Vetorize").grid(row=5,column=0)
tk.Button(root, text="Vetorize", width=10, command=vectorize).grid(row=5,column=1)

# 6. Filtering - popup image show
tk.Label(root, text="6. Filtering").grid(row=6,column=0)
tk.Button(root, text="Filtering", width=10, command=filtering).grid(row=6,column=1)

# ttk.Button(root, text='Rock', command=lambda: select('Rock')).pack()

root.mainloop()
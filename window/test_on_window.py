from tkinter import *
from tkinter import (
		messagebox, filedialog
	)
import tkinter.ttk
import os
from PIL import Image,ImageTk
import PIL
from datetime import datetime
import cv2

import module.rectify as rectify
import module.binary as binary
import module.neighbors as neighbors

current_path = os.path.dirname(os.path.realpath(__file__)) #파일 경로

# Settings
root = Tk()
root.title("Map Generator from Rescue Plans")
root.geometry("800x800")
# root.resizable(False, False)
title = Label(root, text="Map Generator")
title.pack()

# notebook
notebook = tkinter.ttk.Notebook(root, width=700, height=700, takefocus=True)
notebook.pack(fill=tkinter.BOTH)

rootHeight = root.winfo_height()
rootWidth = root.winfo_width()

# frame1 - 1: Selecting Image
frame1 = Frame(root)
notebook.add(frame1, text="1: Selecting Image")

# frame1 functions
# rectify_yn = StringVar()
rectify_yn = 0	# image rectify done yn
frame1_count = 0	# frame1 process count
new_dir_nm = current_path	# using directory name
frame1_save_image = ''	# frame1's image path
frame2_image_points = ''
frame2_control_points = ''

def file_find():
	image_ext = r"*.jpg *.jpeg *.png"
	file = filedialog.askopenfilenames(filetypes=(("Image file",image_ext),("all file", "*.*")), initialdir=current_path)
	en_filepath.delete(0,END)
	en_filepath.insert(END, file[0])

	if en_filepath:
		global frame1_new_photo
		fixed_width = 700
		frame1_new_image = Image.open(en_filepath.get())
		image_percent = (fixed_width / float(frame1_new_image.size[0]))
		image_height = int(float(frame1_new_image.size[1])*float(image_percent))
		frame1_new_image = frame1_new_image.resize((fixed_width, image_height), PIL.Image.NEAREST)
		frame1_new_photo = ImageTk.PhotoImage(frame1_new_image)
		frame1_image_label.configure(image=frame1_new_photo)

def f_01_next():
	# only the first time at frame1 make new directory
	global frame1_count
	if frame1_count == 0:
		global new_dir_nm
		new_dir_nm += str("\\" + "{:%Y%m%d%H%M}".format(datetime.now()))

		if not os.path.exists(new_dir_nm):
			os.makedirs(new_dir_nm)

	image_name = "01_original"

	global rectify_yn
	if rectify_yn == 1:
		image_name += "-rectify"

	frame1_img = cv2.imread(en_filepath.get())
	global frame1_save_image
	frame1_save_image = new_dir_nm + "\\" +image_name + ".png"
	cv2.imwrite(frame1_save_image, frame1_img)

	# frame2에 이미지 띄워주기 - 해당 디렉토리에 있는 파일 사용
	fixed_width = 700
	global frame2_new_photo
	frame2_new_image = Image.open(en_filepath.get())
	image_percent = (fixed_width / float(frame2_new_image.size[0]))
	image_height = int(float(frame2_new_image.size[1])*float(image_percent))
	frame2_new_image = frame2_new_image.resize((fixed_width, image_height), PIL.Image.NEAREST)
	frame2_new_photo = ImageTk.PhotoImage(frame2_new_image)
	frame2_image_label.configure(image=frame2_new_photo)
	
	notebook.select(frame2)
	frame1_count += 1

view = Label(frame1, text="File Path: ")
view.pack(side="top", anchor="w")

en_filepath = Entry(frame1, width=100)
en_filepath.pack(side="top", anchor="w")

bt_find = Button(frame1, text="Find", width=10, command= file_find)
bt_find.pack(side="top", anchor="e")

Radiobutton(frame1, text = "Yes", variable = rectify_yn, value = 1).pack(side = "top", ipady = 5)
Radiobutton(frame1, text = "No", variable = rectify_yn, value = 0).pack(side = "top", ipady = 5)

bt_01_next = Button(frame1, text="Next", width=10, overrelief="solid", command= f_01_next)
bt_01_next.pack(side="bottom", anchor="e")

fixed_width = 700
frame1_image = Image.open("window\\a.png")
image_percent = (fixed_width / float(frame1_image.size[0]))
image_height = int(float(frame1_image.size[1])*float(image_percent))
frame1_image = frame1_image.resize((fixed_width, image_height), PIL.Image.NEAREST)
photo = ImageTk.PhotoImage(frame1_image)
frame1_image_label = Label(frame1, image=photo)
frame1_image_label.pack()

# frame2
frame2 = Frame(root)
notebook.add(frame2, text="2: Rectification")

image_point_title = Label(frame2, width=20, text="Image Points: ")
image_point_title.grid(row=0, column=0, columnspan=2)

image_point_1_nm = Label(frame2, width=20, text="1: ")
image_point_1_nm.grid(row=1, column=0)
image_point_1 = Entry(frame2, width=20)
image_point_1.insert(0, "427;1013")
image_point_1.grid(row=1, column=1)

image_point_2_nm = Label(frame2, width=20, text="2: ")
image_point_2_nm.grid(row=2, column=0)
image_point_2 = Entry(frame2, width=20)
image_point_2.insert(0, "403;1580")
image_point_2.grid(row=2, column=1)

image_point_3_nm = Label(frame2, width=20, text="3: ")
image_point_3_nm.grid(row=3, column=0)
image_point_3 = Entry(frame2, width=20)
image_point_3.insert(0, "3810;1223")
image_point_3.grid(row=3, column=1)

image_point_4_nm = Label(frame2, width=20, text="4: ")
image_point_4_nm.grid(row=4, column=0)
image_point_4 = Entry(frame2, width=20)
image_point_4.insert(0, "3833;1590")
image_point_4.grid(row=4, column=1)

control_point_title = Label(frame2, width=20, text="Control Points: ")
control_point_title.grid(row=0, column=3, columnspan=2)
control_point_1_nm = Label(frame2, width=20, text="1: ")
control_point_1_nm.grid(row=1, column=2)
control_point_1 = Entry(frame2, width=20)
control_point_1.insert(0, "0;0")
control_point_1.grid(row=1, column=3)

control_point_2_nm = Label(frame2, width=20, text="2: ")
control_point_2_nm.grid(row=2, column=2)
control_point_2 = Entry(frame2, width=20)
control_point_2.insert(0, "0;880")
control_point_2.grid(row=2, column=3)

control_point_3_nm = Label(frame2, width=20, text="3: ")
control_point_3_nm.grid(row=3, column=2)
control_point_3 = Entry(frame2, width=20)
control_point_3.insert(0, "4075;85")
control_point_3.grid(row=3, column=3)

control_point_4_nm = Label(frame2, width=20, text="4: ")
control_point_4_nm.grid(row=4, column=2)
control_point_4 = Entry(frame2, width=20)
control_point_4.insert(0, "4075;880")
control_point_4.grid(row=4, column=3)

control_description = Label(frame2, width=100, text="ex) 1000;200 (x;y)")
control_description.grid(row=5, column=0, columnspan=4)

fixed_width = 700
frame2_image = Image.open("window\\a.png")
image_percent = (fixed_width / float(frame2_image.size[0]))
image_height = int(float(frame2_image.size[1])*float(image_percent))
frame2_image = frame2_image.resize((fixed_width, image_height), PIL.Image.NEAREST)
frame2_photo = ImageTk.PhotoImage(frame2_image)
frame2_image_label = Label(frame2, image=frame2_photo)
frame2_image_label.grid(row=6, column=0, columnspan=4, sticky=W+E+N+S)

value1 = Entry(frame2, width=20)
value1.insert(0, "1000")
value1.grid(row=7, column=3)

value2 = Entry(frame2, width=20)
value2.insert(0, "-2500")
value2.grid(row=7, column=4)

def f_02_rectify():
	global frame2_image_points
	frame2_image_points = str(image_point_1.get()) + "\n" + str(image_point_2.get()) + "\n" + str(image_point_3.get()) + "\n" + str(image_point_4.get())
	global frame2_control_points
	frame2_control_points = str(control_point_1.get()) + "\n" + str(control_point_2.get()) + "\n" + str(control_point_3.get()) + "\n" + str(control_point_4.get())
	
	# rectify image
	global new_dir_nm
	e_image = rectify.fn_rectify(new_dir_nm,'01_original.png',frame2_image_points,frame2_control_points,value1.get(),value2.get())

	# new rectify image to frame2
	fixed_width = 700
	global frame2_new_photo
	frame2_rectify_image = Image.open('%s\\%s' % (new_dir_nm, '02_rectify.png'))
	image_percent = (fixed_width / float(frame2_rectify_image.size[0]))
	image_height = int(float(frame2_rectify_image.size[1])*float(image_percent))
	frame2_rectify_image = frame2_rectify_image.resize((fixed_width, image_height), PIL.Image.NEAREST)
	frame2_rectify_photo = ImageTk.PhotoImage(frame2_rectify_image)
	frame2_image_label.configure(image=frame2_rectify_photo)
	
	notebook.select(frame2)

def f_02_next():
	notebook.select(frame3)

bt_02_rectify = Button(frame2, text="Retify", width=10, overrelief="solid", command= f_02_rectify)
bt_02_rectify.grid(row=7, column=0)

bt_02_next = Button(frame2, text="Next", width=10, overrelief="solid", command= f_02_next)
bt_02_next.grid(row=7, column=1)

# frame. 3
frame3 = Frame(root)
notebook.add(frame3, text="3: Binarization")

# exit_button = Button(frame3, text="나가기", command=root.destroy)
# exit_button.pack(expand=True)

def f_03_binary():
	# transforme to an binary image (False if no rectify is done, True when some rectify is done)
	global new_dir_nm
	bin_image = binary.fn_binary(new_dir_nm,'02_rectify.png',True)

def f_03_next():
	notebook.select(frame4)	

bt_03_binary = Button(frame3, text="Binary", width=10, overrelief="solid", command= f_03_binary)
bt_03_binary.pack(side="bottom", anchor="w")

bt_03_next = Button(frame3, text="Next", width=10, overrelief="solid", command= f_03_next)
bt_03_next.pack(side="bottom", anchor="e")

# frame. 4
frame4 = Frame(root)
notebook.add(frame4, text="4")

def f_04_neighbors():
	# transforme to an binary image (False if no rectify is done, True when some rectify is done)
	global new_dir_nm
	bin_image = neighbors.fn_image_n8(new_dir_nm,'03_binary.txt')

def f_04_next():
	notebook.select(frame5)

bt_04_binary = Button(frame4, text="Neighbors", width=10, overrelief="solid", command= f_04_neighbors)
bt_04_binary.pack(side="bottom", anchor="w")

bt_04_next = Button(frame4, text="Next", width=10, overrelief="solid", command= f_04_next)
bt_04_next.pack(side="bottom", anchor="e")

# frame. 5
frame5 = Frame(root)
notebook.add(frame5, text="5")

# frame. 6
frame6 = Frame(root)
notebook.add(frame6, text="6")

root.mainloop()
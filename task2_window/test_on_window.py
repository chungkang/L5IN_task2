from tkinter import *
from tkinter import (
		messagebox, filedialog
	)
import tkinter.ttk
import os
from PIL import Image,ImageTk
from datetime import datetime
import cv2

current_path = os.path.dirname(os.path.realpath(__file__)) #파일 경로

# Settings
root = Tk()
root.title("Map Generator from Rescue Plans")
root.geometry("500x500")
# root.resizable(False, False)
title = Label(root, text="Map Generator")
title.pack()

# notebook
notebook = tkinter.ttk.Notebook(root, width=400, height=400, takefocus=True)
notebook.pack()

rootHeight = root.winfo_height()
rootWidth = root.winfo_width()

# frame1 - 1: Selecting Image
frame1 = Frame(root)
notebook.add(frame1, text="1: Selecting Image")

# frame1 functions
rectify_yn = StringVar()
new_dir_nm = current_path
frame1_save_image = StringVar()

def file_find():
	image_ext = r"*.jpg *.jpeg *.png"
	file = filedialog.askopenfilenames(filetypes=(("Image file",image_ext),("all file", "*.*")), initialdir=current_path)
	en_filepath.delete(0,END)
	en_filepath.insert(END, file[0])

	if en_filepath:
		global frame1_new_photo
		frame1_new_photo = ImageTk.PhotoImage(Image.open(en_filepath.get()))
		image_label.config(image=frame1_new_photo)

def f_01_next():
	# 실행파일 위치에 날짜시간분 폴더 생성 - 폴더명 변수
	global new_dir_nm
	new_dir_nm += str("\\" + "{:%Y%m%d%H%M}".format(datetime.now()))
	
	if not os.path.exists(new_dir_nm):
		os.makedirs(new_dir_nm)

	image_name = "01_original"

	global rectify_yn
	print(rectify_yn.get())
	if rectify_yn.get():
		image_name += "-rectify"

	frame1_img = cv2.imread(en_filepath.get())
	global frame1_save_image
	frame1_save_image = new_dir_nm + "\\" +image_name + ".png"
	cv2.imwrite(frame1_save_image, frame1_img)

	# frame2에 이미지 띄워주기 - 해당 디렉토리에 있는 파일 사용
	global frame2_new_photo
	frame2_new_photo = ImageTk.PhotoImage(Image.open(en_filepath.get()))
	fram2_image_label.config(image=frame2_new_photo)
	notebook.select(frame2)

view = Label(frame1, text="File Path: ")
view.pack(side="top", anchor="w")

en_filepath = Entry(frame1, width=100)
en_filepath.pack(side="top", anchor="w")

bt_find = Button(frame1, text="Find", width=10, command= file_find)
bt_find.pack(side="top", anchor="e")

Radiobutton(frame1, text = "Yes", variable = rectify_yn, value = 1).pack(side = "top", ipady = 5)
Radiobutton(frame1, text = "No", variable = rectify_yn, value = 0).pack(side = "top", ipady = 5)

bt_01_next = Button(frame1, text="Next", width=10,overrelief="solid", command= f_01_next)
bt_01_next.pack(side="bottom", anchor="e")

photo = PhotoImage(file="task2_window\\a.png")
image_label = Label(frame1, image=photo)
image_label.pack()

# frame2
frame2 = Frame(root)
notebook.add(frame2, text="2: Rectification")

monster_name = Label(frame2, text="BOSS")
monster_name.pack()

frame2_photo = PhotoImage(file="task2_window\\a.png")
fram2_image_label = Label(frame2, image=frame2_photo)
fram2_image_label.pack()




# frame. 3
frame3 = Frame(root)
notebook.add(frame3, text="3: Binarization")

exit_button = Button(frame3, text="나가기", command=root.destroy)
exit_button.pack(expand=True)

# frame. 4
frame4 = Frame(root)
notebook.add(frame4, text="4: Lines")
# notebook.insert(2, frame4, text="4: Detacting Lines")

potion = Label(frame4, text="물약: 1000\\")
potion.pack()
sword = Label(frame4, text="무기 강화: 2500\\")
sword.pack()

root.mainloop()
import tkinter
import cv2
from tkinter import *
from tkinter import (
		messagebox, filedialog
	)
import tkinter.ttk
import os
from PIL import Image,ImageTk
import PIL
from datetime import datetime

import module.rectify as rectify
import module.binary as binary
import module.neighbors as neighbors

class App:
    def __init__(self, window, window_title, image_path="test\\lena.jpg"):
        self.current_path = os.path.dirname(os.path.realpath(__file__)) #파일 경로

        # Settings
        # root = Tk()
        self.root= Toplevel()
        self.root.title("Map Generator from Rescue Plans")
        self.root.geometry("800x800")
        # root.resizable(False, False)
        self.title = Label(self.root, text="Map Generator")
        self.title.pack()

        # notebook
        self.notebook = tkinter.ttk.Notebook(self.root, width=700, height=700, takefocus=True)
        self.notebook.pack(fill=tkinter.BOTH)

        self.rootHeight = self.root.winfo_height()
        self.rootWidth = self.root.winfo_width()

        # frames
        self.frame1 = Frame(self.root)
        self.notebook.add(self.frame1, text="1: Selecting Image")

        self.frame2 = Frame(self.root)
        self.notebook.add(self.frame2, text="2: Rectification")

        self.frame3 = Frame(self.root)
        self.notebook.add(self.frame3, text="3: Binarization")

        self.frame4 = Frame(self.root)
        self.notebook.add(self.frame4, text="4: Neighbors")

        self.frame5 = Frame(self.root)
        self.notebook.add(self.frame5, text="5: Vetorize")

        self.frame6 = Frame(self.root)
        self.notebook.add(self.frame6, text="6: Filter")
        

        # frame1 - 1: Selecting Image
        self.rectify_yn = 0	# image rectify done yn
        self.frame1_count = 0	# frame1 process count
        self.new_dir_nm = self.current_path	# using directory name
        self.frame1_save_image = ''	# frame1's image path
        self.frame2_image_points = ''
        self.frame2_control_points = ''

        self.view = Label(self.frame1, text="File Path: ")
        self.view.pack(side="top", anchor="w")

        self.en_filepath = Entry(self.frame1, width=100)
        self.en_filepath.pack(side="top", anchor="w")


        Radiobutton(self.frame1, text = "Yes", variable = self.rectify_yn, value = 1).pack(side = "top", ipady = 5)
        Radiobutton(self.frame1, text = "No", variable = self.rectify_yn, value = 0).pack(side = "top", ipady = 5)

        self.fixed_width = 700
        self.frame1_image = Image.open("window\\a.png")
        self.image_percent = (self.fixed_width / float(self.frame1_image.size[0]))
        self.image_height = int(float(self.frame1_image.size[1])*float(self.image_percent))
        self.frame1_image = self.frame1_image.resize((self.fixed_width, self.image_height), PIL.Image.NEAREST)
        self.photo = ImageTk.PhotoImage(self.frame1_image)

        
        self.frame1_image_label = Label(self.frame1, image=self.photo)
        self.frame1_image_label.pack()
        
        
        # self.bt_find = Button(self.frame1, text="Find", width=10, command= self.file_find(self.current_path, self.en_filepath, self.frame1_image_label))
        # self.bt_find.pack(side="top", anchor="e")

        self.bt_01_next = Button(self.frame1, text="Next", width=10, overrelief="solid", command= self.f_01_next(self.en_filepath, self.frame2_image_label, self.notebook, self.frame2))
        self.bt_01_next.pack(side="bottom", anchor="e")


        # frame2
        self.image_point_title = Label(self.frame2, width=20, text="Image Points: ")
        self.image_point_title.grid(row=0, column=0, columnspan=2)

        self.image_point_1_nm = Label(self.frame2, width=20, text="1: ")
        self.image_point_1_nm.grid(row=1, column=0)
        self.image_point_1 = Entry(self.frame2, width=20)
        self.image_point_1.insert(0, "427;1013")
        self.image_point_1.grid(row=1, column=1)

        self.image_point_2_nm = Label(self.frame2, width=20, text="2: ")
        self.image_point_2_nm.grid(row=2, column=0)
        self.image_point_2 = Entry(self.frame2, width=20)
        self.image_point_2.insert(0, "403;1580")
        self.image_point_2.grid(row=2, column=1)

        self.image_point_3_nm = Label(self.frame2, width=20, text="3: ")
        self.image_point_3_nm.grid(row=3, column=0)
        self.image_point_3 = Entry(self.frame2, width=20)
        self.image_point_3.insert(0, "3810;1223")
        self.image_point_3.grid(row=3, column=1)

        self.image_point_4_nm = Label(self.frame2, width=20, text="4: ")
        self.image_point_4_nm.grid(row=4, column=0)
        self.image_point_4 = Entry(self.frame2, width=20)
        self.image_point_4.insert(0, "3833;1590")
        self.image_point_4.grid(row=4, column=1)

        self.control_point_title = Label(self.frame2, width=20, text="Control Points: ")
        self.control_point_title.grid(row=0, column=3, columnspan=2)
        self.control_point_1_nm = Label(self.frame2, width=20, text="1: ")
        self.control_point_1_nm.grid(row=1, column=2)
        self.control_point_1 = Entry(self.frame2, width=20)
        self.control_point_1.insert(0, "0;0")
        self.control_point_1.grid(row=1, column=3)

        self.control_point_2_nm = Label(self.frame2, width=20, text="2: ")
        self.control_point_2_nm.grid(row=2, column=2)
        self.control_point_2 = Entry(self.frame2, width=20)
        self.control_point_2.insert(0, "0;880")
        self.control_point_2.grid(row=2, column=3)

        self.control_point_3_nm = Label(self.frame2, width=20, text="3: ")
        self.control_point_3_nm.grid(row=3, column=2)
        self.control_point_3 = Entry(self.frame2, width=20)
        self.control_point_3.insert(0, "4075;85")
        self.control_point_3.grid(row=3, column=3)

        self.control_point_4_nm = Label(self.frame2, width=20, text="4: ")
        self.control_point_4_nm.grid(row=4, column=2)
        self.control_point_4 = Entry(self.frame2, width=20)
        self.control_point_4.insert(0, "4075;880")
        self.control_point_4.grid(row=4, column=3)

        self.control_description = Label(self.frame2, width=100, text="ex) 1000;200 (x;y)")
        self.control_description.grid(row=5, column=0, columnspan=4)

        self.fixed_width = 700
        self.frame2_image = Image.open("window\\a.png")
        self.image_percent = (self.fixed_width / float(self.frame2_image.size[0]))
        self.image_height = int(float(self.frame2_image.size[1])*float(self.image_percent))
        self.frame2_image = self.frame2_image.resize((self.fixed_width, self.image_height), PIL.Image.NEAREST)
        self.frame2_photo = ImageTk.PhotoImage(self.frame2_image)
        self.frame2_image_label = Label(self.frame2, image=self.frame2_photo)
        self.frame2_image_label.grid(row=6, column=0, columnspan=4, sticky=W+E+N+S)

        self.value1 = Entry(self.frame2, width=20)
        self.value1.insert(0, "1000")
        self.value1.grid(row=7, column=3)

        self.value2 = Entry(self.frame2, width=20)
        self.value2.insert(0, "-2500")
        self.value2.grid(row=7, column=4)

        self.bt_02_rectify = Button(self.frame2, text="Retify", width=10, overrelief="solid", command= self.f_02_rectify(self.image_point_1, self.image_point_2, self.image_point_3, self.image_point_4, self.control_point_1, self.control_point_2, self.control_point_3, self.control_point_4, self.value1, self.value2, self.frame2_image_label, self.notebook, self.frame2))
        self.bt_02_rectify.grid(row=7, column=0)

        self.bt_02_next = Button(self.frame2, text="Next", width=10, overrelief="solid", command= self.f_02_next(self.notebook, self.frame3))
        self.bt_02_next.grid(row=7, column=1)

        # frame. 3
        self.bt_03_binary = Button(self.frame3, text="Binary", width=10, overrelief="solid", command= self.f_03_binary)
        self.bt_03_binary.pack(side="bottom", anchor="w")

        self.bt_03_next = Button(self.frame3, text="Next", width=10, overrelief="solid", command= self.f_03_next(self.notebook,self.frame4))
        self.bt_03_next.pack(side="bottom", anchor="e")

        # frame. 4
        self.bt_04_binary = Button(self.frame4, text="Neighbors", width=10, overrelief="solid", command= self.f_04_neighbors)
        self.bt_04_binary.pack(side="bottom", anchor="w")

        self.bt_04_next = Button(self.frame4, text="Next", width=10, overrelief="solid", command= self.f_04_next(self.notebook,self.frame5))
        self.bt_04_next.pack(side="bottom", anchor="e")


        # frame. 5

        # frame. 6

        self.root.mainloop()


    def file_find(self, current_path, en_filepath, frame1_image_label):
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
            frame1_image_label.config(image=frame1_new_photo)

    def f_01_next(self, en_filepath, frame2_image_label, notebook, frame2):
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
        frame2_image_label.config(image=frame2_new_photo)
        
        notebook.select(frame2)
        frame1_count += 1


    def f_02_rectify(self, image_point_1, image_point_2, image_point_3, image_point_4, control_point_1, control_point_2, control_point_3, control_point_4, value1, value2, frame2_image_label, notebook, frame2):
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
        frame2_image_label.config(image=frame2_rectify_photo)
        
        notebook.select(frame2)

    def f_02_next(self, notebook, frame3):
        notebook.select(frame3)

    def f_03_binary(self):
        # transforme to an binary image (False if no rectify is done, True when some rectify is done)
        global new_dir_nm
        bin_image = binary.fn_binary(new_dir_nm,'02_rectify.png',True)

    def f_03_next(self, notebook, frame4):
        notebook.select(frame4)

    def f_04_neighbors(self):
        # transforme to an binary image (False if no rectify is done, True when some rectify is done)
        global new_dir_nm
        bin_image = neighbors.fn_image_n8(new_dir_nm,'03_binary.txt')

    def f_04_next(self, notebook,frame5):
        notebook.select(frame5)

# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")
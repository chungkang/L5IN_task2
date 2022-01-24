from tkinter import *
from tkinter import (
		messagebox, filedialog
	)
import tkinter.ttk
import os
# print (os.path.dirname(os.path.realpath(__file__)))#파일이 위치한 디렉터리
from PIL import Image,ImageTk

# Settings
root = Tk()
root.title("Map Generator from Rescue Plans")
root.geometry("500x500")
root.resizable(False, False)
title = Label(root, text="Map Generator")
title.pack()

# default value
player_value = 1

# define function
def chatting():
	chat = txt.get()
	view.configure(text="이전 채팅: " + chat)

def attack():
	messagebox.showinfo("Level UP", "몬스터를 처치했습니다!")
	counter = int(player_level["text"])
	counter += 1
	player_level.config(text=str(counter))

excel_ext = r"*.xlsx *.xls *.csv"

def file_find():
    file = filedialog.askopenfilenames(filetypes=(("Excel file", excel_ext),("all file", "*.*")), initialdir=r"C:\Users")
    en_filepath.delete(0,END)
    en_filepath.insert(END, file[0])

	# image = Image.new('1', (100, 100), 0)
	# image = tkinter.PhotoImage(file="task2_window\\a.png")
	# label = tkinter.Label(frame1, image=image)
    # label.config(image=tkimg[0])
    # root.update_idletasks()
    # root.after(delay, loopCapture)

# def file_upload():
#     if len(en_filepath.get()) == 0:
#         mbox.showinfo("warning","select file, please")
#         return
#     else:
#         file_name = os.path.basename(en_filepath.get())
#         dest_path = os.path.join("D:\\", file_name)
#         shutil.copy(en_filepath.get(),dest_path)
#         en_filepath.delete(0,END)    
#         return
 

# notebook
notebook = tkinter.ttk.Notebook(root, width=400, height=400, takefocus=True)
notebook.pack()

# frame. 1
frame1 = Frame(root)
notebook.add(frame1, text="1: Select Image")

guide_level = Label(frame1, text=os.path.dirname(os.path.realpath(__file__)))
guide_level.pack(side="top")
player_level = Label(frame1, text=str(player_value))
player_level.pack(side="top")

view = Label(frame1, text="File Path: ")
view.pack(side="top", anchor="nw")
btn = Button(frame1, text="확인",command=chatting,width=3,height=1)
btn.pack(side="bottom", fill="both")
# txt = Entry(frame1)
# txt.pack(side="bottom", fill="both")
# guide = Label(frame1, text="채팅: ")
# guide.pack(side="bottom", anchor="nw")

en_filepath = Entry(frame1, width=100)
en_filepath.pack(fill="x", padx=1, pady=1)

# bt_upload = Button(frame1, text="Upload", width=10, command= file_upload)
# bt_upload.pack(side="right", padx=1, pady=1)
bt_find = Button(frame1, text="Find", width=10, command= file_find)
bt_find.pack(side="right", padx=1, pady=1)

# file_path = os.path.realpath(__file__)

image = tkinter.PhotoImage(file="task2_window\\a.png")
label = tkinter.Label(frame1, image=image)
label.pack()

# frame. 2
frame2 = Frame(root)
notebook.add(frame2, text="2: Rectification")

monster_name = Label(frame2, text="BOSS")
monster_name.pack()
attack_button = Button(frame2, text="attack", command=attack)
attack_button.pack(expand=True)

# frame. 3
frame3 = Frame(root)
notebook.add(frame3, text="3: Binarization")

exit_button = Button(frame3, text="나가기", command=root.destroy)
exit_button.pack(expand=True)

# frame. 4
frame4 = Frame(root)
notebook.add(frame4, text="4: Detacting Lines")
# notebook.insert(2, frame4, text="4: Detacting Lines")

potion = Label(frame4, text="물약: 1000\\")
potion.pack()
sword = Label(frame4, text="무기 강화: 2500\\")
sword.pack()

root.mainloop()
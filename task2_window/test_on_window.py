from tkinter import *
from tkinter import (
		messagebox, filedialog
	)
import tkinter.ttk
import os
from PIL import Image,ImageTk

current_path = os.path.dirname(os.path.realpath(__file__)) #파일 경로

# Settings
root = Tk()
root.title("Map Generator from Rescue Plans")
root.geometry("500x500")
root.resizable(False, False)
title = Label(root, text="Map Generator")
title.pack()

# default value
player_value = 1





# define functions
# frame1 - 1: Selecting Image functions
image_ext = r"*.jpg *.jpeg *.gif *.png"
def file_find():
    # file = filedialog.askopenfilenames(filetypes=(("Excel file", excel_ext),("all file", "*.*")), initialdir=r"C:\Users")
	file = filedialog.askopenfilenames(filetypes=(("Image file",image_ext),("all file", "*.*")), initialdir=current_path)
	en_filepath.delete(0,END)
	en_filepath.insert(END, file[0])

	if en_filepath:
		global photo2  # Garbage Collection : 불필요한 메모리 공간 해제
		photo2 = ImageTk.PhotoImage(Image.open(en_filepath.get()))
		image_label.config(image=photo2)

def attack():
	messagebox.showinfo("Level UP", "몬스터를 처치했습니다!")
	counter = int(player_level["text"])
	counter += 1
	player_level.config(text=str(counter))


# notebook
notebook = tkinter.ttk.Notebook(root, width=400, height=400, takefocus=True)
notebook.pack()

# frame1 - 1: Selecting Image
frame1 = Frame(root)
notebook.add(frame1, text="1: Selecting Image")

view = Label(frame1, text="File Path: ")
view.pack(side="top", anchor="nw")
# btn = Button(frame1, text="확인",command=chatting,width=3,height=1)
# btn.pack(side="bottom", fill="both")

en_filepath = Entry(frame1, width=100)
en_filepath.pack(fill="x", padx=1, pady=1)

bt_find = Button(frame1, text="Find", width=10, command= file_find)
bt_find.pack(side="top", padx=1, pady=1)

photo = PhotoImage(file="task2_window\\a.png")
image_label = Label(frame1, image=photo)
image_label.pack()




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
notebook.add(frame4, text="4: Lines")
# notebook.insert(2, frame4, text="4: Detacting Lines")

potion = Label(frame4, text="물약: 1000\\")
potion.pack()
sword = Label(frame4, text="무기 강화: 2500\\")
sword.pack()

root.mainloop()
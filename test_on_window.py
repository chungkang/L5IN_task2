from tkinter import *
from tkinter import messagebox
import tkinter.ttk

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

# notebook
notebook = tkinter.ttk.Notebook(root, width=400, height=400, takefocus=True)
notebook.pack()

# frame. 1
frame1 = Frame(root)
notebook.add(frame1, text="1: Select Image")

guide_level = Label(frame1, text="Level. ")
guide_level.pack(side="top")
player_level = Label(frame1, text=str(player_value))
player_level.pack(side="top")

view = Label(frame1, text="이전 채팅: ")
view.pack(side="top", anchor="nw")
btn = Button(frame1, text="확인",command=chatting,width=3,height=1)
btn.pack(side="bottom", fill="both")
txt = Entry(frame1)
txt.pack(side="bottom", fill="both")
guide = Label(frame1, text="채팅: ")
guide.pack(side="bottom", anchor="nw")

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
from tkinter import *
from PIL import Image,ImageTk 


def getorigin(eventorigin):
    global x,y
    x = eventorigin.x
    y = eventorigin.y
    print("x y coordinate", 'x: %s  y: %s' % (x,y))
    # tk.messagebox.showinfo("x y coordinate", 'x: %s  y: %s' % (x,y) )

root = Tk()

frame = Frame(root, bd=2, relief=SUNKEN)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0, sticky=E+W)

yscrollbar = Scrollbar(frame)
yscrollbar.grid(row=0, column=1, sticky=N+S)

canvas = Canvas(frame, bd=0, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)

File = "test\IMG_20191015_181243.jpg"
img = ImageTk.PhotoImage(Image.open(File))
canvas.create_image(0,0,image=img, anchor="nw")
canvas.config(scrollregion=canvas.bbox(ALL))

xscrollbar.config(command=canvas.xview)
yscrollbar.config(command=canvas.yview)

canvas.bind("<Button 1>", getorigin)

frame.pack()
root.mainloop()
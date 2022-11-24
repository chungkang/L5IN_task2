import tkinter as tk
from PIL import Image, ImageTk

def getorigin(eventorigin):
    global x,y
    x = eventorigin.x
    y = eventorigin.y
    print("x y coordinate", 'x: %s  y: %s' % (x,y))
    # tk.messagebox.showinfo("x y coordinate", 'x: %s  y: %s' % (x,y) )

class ScrolledCanvas(tk.Frame):
     def __init__(self, parent=None):
          tk.Frame.__init__(self, parent)
          self.master.title("Spectrogram Viewer")
          self.pack(expand=tk.YES, fill=tk.BOTH)
          canv = tk.Canvas(self, relief=tk.SUNKEN)
          canv.config(width=400, height=200)
          canv.config(highlightthickness=0)

          sbarV = tk.Scrollbar(self, orient=tk.VERTICAL)
          sbarH = tk.Scrollbar(self, orient=tk.HORIZONTAL)

          sbarV.config(command=canv.yview)
          sbarH.config(command=canv.xview)

          canv.config(yscrollcommand=sbarV.set)
          canv.config(xscrollcommand=sbarH.set)

          sbarV.pack(side=tk.RIGHT, fill=tk.Y)
          sbarH.pack(side=tk.BOTTOM, fill=tk.X)

          canv.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
          self.im=Image.open("test\IMG_20191015_181243.jpg")
          width,height=self.im.size
          canv.config(scrollregion=(0,0,width,height))
          self.im2=ImageTk.PhotoImage(self.im)
          self.imgtag=canv.create_image(0,0,anchor="nw",image=self.im2)

          canv.bind("<Button 1>", getorigin)

ScrolledCanvas().mainloop()
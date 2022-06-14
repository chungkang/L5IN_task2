# view
from tkinter import *

class View(Tk):
    def __init__(self,callback):
        Tk.__init__(self)
        self.callback = callback
        # Fenster
        self.title("Addition 1")
        self.geometry('230x120+400+100')
        # Entries
        self.eA = Entry(master=self)
        self.eA.insert(0, '12.7')
        self.eA.place(x=20, y=20, width=50)
        self.eB = Entry(master=self)
        self.eB.insert(0, '-18')
        self.eB.place(x=80, y=20, width=50)
        # Button
        self.bRechne = Button(master=self, text="berechne", command=self.callback)
        self.bRechne.place(x=20, y=50, width=50)
        # Label
        self.lC = Label(master=self, text='??')
        self.lC.place(x=20, y=80)

# controller
class Controller(object):
    def __init__(self):
        self.view = View(self.berechne)
        self.berechne()                   # zur Initialisierung
        self.view.mainloop()

    def berechne(self):
        # Eingabe
        a = eval(self.view.eA.get())
        b = eval(self.view.eB.get())

        # Verarbeitung
        # ------------------ hier die Verarbeitung programmieren ------------
        s = a + b
        # -------------------------------------------------------------------

        # Ausgabe
        self.view.lC.config(text=str(s))

# Hauptprogramm
c = Controller()
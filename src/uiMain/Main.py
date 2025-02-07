import tkinter as tk
from tkinter import Tk, Frame, ttk

class Main:
    root = None

    @classmethod
    def destroy(cls):
        cls.root.destroy()

    #Esta función se encargará de inicializar todo lo referente a la ventana raíz
    @classmethod
    def initRoot(cls):
        cls.root = Tk()
        cls.root.geometry("1600x900") #16:9
        cls.root.title("Teatro Escuela Carlos Mayolo")


        #FRAME IZQUIERDO
        leftFrame = Frame(cls.root, borderwidth= 10, bg = "blue")
        leftFrame.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 1)
        ttk.Label(leftFrame, text= "Teatro Escuela Carlos Mayolo", font = "Calibri 24").pack()
        ttk.Label(leftFrame, text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin maximus volutpat tortor sit amet congue. Fusce pretium quam quam, eget blandit eros eleifend non.').pack()
        

        #FRAME DERECHO
        rightFrame = Frame(cls.root, borderwidth= 10, bg = "green", width = 800, height = 900)
        rightFrame.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)
        ttk.Button(rightFrame, text = "Dele a ver que pasa", command = cls.destroy).pack()
    
    @classmethod
    def runApp(cls):
        cls.initRoot()
        cls.root.mainloop()


if __name__ == "__main__":
    Main.runApp()
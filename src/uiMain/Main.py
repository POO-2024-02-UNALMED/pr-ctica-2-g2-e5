import tkinter as tk
from tkinter import Tk, Frame, ttk

class Main:
    root = None
    test = False
    fieldTest = True

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
        Main.leftFrame = Frame(cls.root, borderwidth= 10, bg = "blue")
        Main.leftFrame.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 1)

        #FRAME DERECHO
        Main.rightFrame = Frame(cls.root, borderwidth= 10, bg = "green", width = 800, height = 900)
        Main.rightFrame.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)

        if cls.test:
            ttk.Label(Main.leftFrame, text= "Teatro Escuela Carlos Mayolo", font = "Calibri 24").pack()
            ttk.Label(Main.leftFrame, text='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin maximus volutpat tortor sit amet congue. Fusce pretium quam quam, eget blandit eros eleifend non.').pack()
            ttk.Button(Main.rightFrame, text = "Dele a ver que pasa", command = cls.destroy).pack()
    
    @classmethod
    def runApp(cls):
        cls.initRoot()
        cls.root.mainloop()


class FieldFrame(Frame):

    bg = "slategray1"
    font = "Calibri 11"

    def __init__(self, root: Tk, tituloCriterios: str = "Requerimientos", criterios: list = [], tituloValores: str = "Por favor digite:", valores: list = None, habilitado: list = None):
        #todos los colores en tkinter: https://www.plus2net.com/python/tkinter-colors.php
        super().__init__(master = root, width = 1600, height = 900, bg = FieldFrame.bg) #16:9
        self.root = root
        self.tituloCriterios = tituloCriterios
        self.criterios = criterios
        self.tituloValores = tituloValores
        self.valores = valores if valores is not None else []
        self.habilitado = habilitado

        tituloCriteriosWidget = tk.Label(self, text = self.tituloCriterios, font = FieldFrame.font, bg = FieldFrame.bg)
        self.labels = [tituloCriteriosWidget] + [ tk.Label(self, text = label, font = FieldFrame.font, bg = FieldFrame.bg) for label in self.criterios]

        for i, label in enumerate(self.labels):
            label.grid(row = i, column = 0, padx= 50, pady= 10)

        tituloValoresWidget = tk.Label(self, text = self.tituloValores, font = FieldFrame.font, bg = FieldFrame.bg)
        self.values = [tituloValoresWidget] + [tk.Entry(self, textvariable= value) for value in self.valores]

        for i, value in enumerate(self.values):
            value.grid(row = i, column = 1, padx= 50, pady= 10)


        if Main.fieldTest:
            self.pack()   

    def getValue(self, criterio: str) -> str | None:
        self.mapCriterios = [(criterio, valor) for criterio, valor in zip(self.criterios, self.valores)]
        for (auxCriterio, valor) in self.mapCriterios:
            if auxCriterio == criterio:
                return valor
        return None



if __name__ == "__main__":

    #datos de prueba
    criterios = ["Name", "Age", "Email", "Bitcoin"]
    valores = ["John Doe", "25", "john@example.com", "293090237hjkhjk2j"]

    #Main.runApp()
    Main.initRoot()
    window = FieldFrame(Main.rightFrame, criterios= criterios, valores= valores)
    print(window.getValue("Age")) #25
    window.mainloop()
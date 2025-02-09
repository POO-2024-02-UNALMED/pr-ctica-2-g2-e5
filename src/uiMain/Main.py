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
        cls.root.geometry("960x540") #16:9
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
        super().__init__(master = root, width = 800, height = 450, bg = FieldFrame.bg) #16:9
        self.root = root
        self.tituloCriterios = tituloCriterios
        self.criterios = criterios
        self.tituloValores = tituloValores
        self.valores = valores if valores is not None else []
        self.habilitado = habilitado

        tituloCriteriosWidget = tk.Label(self, text = self.tituloCriterios, bg = FieldFrame.bg)
        tituloValoresWidget = tk.Label(self, text = self.tituloValores, bg = FieldFrame.bg)

        tituloCriteriosWidget.config(font = (FieldFrame.font, 11, "bold"))
        tituloValoresWidget.config(font = (FieldFrame.font, 11, "bold"))

        self.labels = [tituloCriteriosWidget] + [ tk.Label(self, text = label, font = FieldFrame.font, bg = FieldFrame.bg) for label in self.criterios]

        for i, label in enumerate(self.labels):
            label.grid(row = i, column = 0, padx= 3, pady= 5)
        
        self.values = [tituloValoresWidget] + [tk.Entry(self, textvariable= value) for value in self.valores]

        habilitadoExists = habilitado is not None

        for i, value in enumerate(self.values):
            if i > 0 and self.valores:
                value.insert(0, self.valores[i-1]) # i-1 por el desfase que da agregar el titulo de la columna de valores
                
                if habilitadoExists:
                    status = "normal" if self.criterios[i-1] in habilitado else "disabled"
                    value.configure(state= status)
            value.grid(row = i, column = 1, padx= 50, pady= 10)

        aceptar = tk.Button(self, text = "Aceptar", command = self.gatherEntries)
        aceptar.grid(row = len(self.valores) + 1, column = 0, sticky= "w")

        borrar = tk.Button(self, text = "Borrar", command = self.deleteEntries)
        borrar.grid(row = len(self.valores) + 1, column = 1,  sticky= "e")

        if Main.fieldTest:
            self.pack()   

    def getValue(self, criterio: str) -> str | None:
        self.mapCriterios = [(criterio, valor) for criterio, valor in zip(self.criterios, self.valores)]
        for (auxCriterio, valor) in self.mapCriterios:
            if auxCriterio == criterio:
                return valor
        return None
    
    def gatherEntries(self) -> None:
        self.valores = [entry.get() for i, entry in enumerate(self.values) if i > 0]    
        
        if Main.fieldTest:
            print(self.valores)    
        
        #PENDIENTE: 
        # revisar si el dato no es nulo y lanzar excepcion si lo es
        # revisar dependiendo del caso, si el dato existe en la base de datos (ej, ID)

    def deleteEntries(self) -> None:
        for i, entry in enumerate(self.values):
            if i > 0:
                entry.delete(0, "end")

if __name__ == "__main__":

    #datos de prueba
    criterios = ["Name", "Age", "Email", "Bitcoin", "Country", "Number"]
    valores = ["John Doe", "25", "john@example.com", "293090237hjkhjk2j", "Rhodesia", "892962"]

    #Main.runApp()
    Main.initRoot()
    window = FieldFrame(Main.rightFrame, criterios= criterios, valores= valores, habilitado= ["Age", "Country"])
    print(window.getValue("Age")) #25
    window.mainloop()
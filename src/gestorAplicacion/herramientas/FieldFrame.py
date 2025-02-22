import tkinter as tk
from tkinter import Frame, Tk, ttk
from excepciones.errorEntradaNula import errorEntradaNula

class FieldFrame(Frame):

    bg = "#701C1A"
    fg = '#FCE6C9'
    font = "Calibri 11"
    fieldTest = False

    def __init__(self, root: Tk, tituloCriterios: str = "Requerimientos", criterios: list = [], 
                tituloValores: str = "Por favor digite:", valores: list = None, habilitado: list = None, 
                combobox = False, command = None, tituloGuardar = "Aceptar", tituloBorrar = "Borrar"):
        #todos los colores en tkinter: https://www.plus2net.com/python/tkinter-colors.php
        super().__init__(master = root, width = 800, height = 450, bg = FieldFrame.bg) #16:9
        self.root = root
        self.tituloCriterios = tituloCriterios
        self.criterios = criterios
        self.tituloValores = tituloValores
        self.valores = valores if valores is not None else []
        self.habilitado = habilitado
        self.combobox = combobox
        self.tituloGuardar = tituloGuardar
        self.tituloBorrar = tituloBorrar

        tituloCriteriosWidget = tk.Label(self, text = self.tituloCriterios, bg = FieldFrame.bg)
        tituloValoresWidget = tk.Label(self, text = self.tituloValores, bg = FieldFrame.bg)

        tituloCriteriosWidget.configure(font = (FieldFrame.font, 11, "bold"), fg = FieldFrame.fg )
        tituloValoresWidget.configure(font = (FieldFrame.font, 11, "bold"), fg= FieldFrame.fg)

        #expande las columnas según crece la pantalla
        self.columnconfigure(0, weight=2) 
        self.columnconfigure(1, weight=1)  
        self.columnconfigure(2, weight=2)  

        self.labels = [tituloCriteriosWidget] + [ tk.Label(self, text = label, font = (FieldFrame.font, 11), bg = FieldFrame.bg, fg = FieldFrame.fg) for label in self.criterios]
        
        for i, label in enumerate(self.labels):
            label.grid(row = i, column = 0, padx= 3, pady= 5)
            self.rowconfigure(i, weight=1)

        #self.criteriosStringVar = [tk.StringVar(self, value = "") for valor in self.valores]
        
        if not combobox:
            self.values = [tituloValoresWidget] + [tk.Entry(self, text= value) for value in self.valores]
        else:
            self.values = [tituloValoresWidget] + [ttk.Combobox(self, values= value) for value in self.valores]
            #, textvariable= self.criteriosStringVar[i]

            for value in self.values[1:]:
                value['state'] = 'readonly'

        habilitadoExists = habilitado is not None

        for i, value in enumerate(self.values):
            if i > 0 and self.valores:
                value.insert(0, self.valores[i-1]) # i-1 por el desfase que da agregar el titulo de la columna de valores
                
                if habilitadoExists:
                    status = "normal" if self.criterios[i-1] in habilitado else "disabled"
                    value.configure(state= status)
            value.grid(row = i, column = 2,)# padx= 10, pady= 10)

        aceptar = tk.Button(self, text = self.tituloGuardar, command = self.gatherEntries if command is None else command)
        aceptar.grid(row = len(self.valores) + 1, column = 1, sticky= "ew")

        borrar = tk.Button(self, text = self.tituloBorrar, command = self.deleteEntries)
        borrar.grid(row = len(self.valores) + 2, column = 1, sticky= "ew")

        if FieldFrame.fieldTest:
            self.pack()   

    def getValue(self, criterio: str) -> str | None:
        self.mapCriterios = [(criterio, valor) for criterio, valor in zip(self.criterios, self.valores)]
        for (auxCriterio, valor) in self.mapCriterios:
            if auxCriterio == criterio:
                return valor
        return None
    
    def gatherEntries(self) -> None:
        self.valores = [entry.get() for i, entry in enumerate(self.values) if i > 0]   

        for entry in self.valores:
                if entry == "" or entry is None:
                    raise errorEntradaNula
        
        if FieldFrame.fieldTest:
            print(self.valores)    

    def deleteEntries(self) -> None:
        if not self.combobox:
            for entry in self.values[1:]:
                    entry.delete(0, "end")
        else:
            for entry in self.values[1:]:  
                entry.set('')
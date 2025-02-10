import tkinter as tk
from tkinter import Tk, Frame
from PIL import Image, ImageTk

class Main:
    root = None
    test = False
    fieldTest = True
    custom = False
    bg = "lightsteelblue3"
    custom = False

    imagenes = [

        "src/media/foto1.jpg",
        "src/media/foto2.jpg",
        "src/media/foto3.png",
        "src/media/foto4.jpg",
        "src/media/foto5.jpg"        
    ]

    indice_imagen = 0 
    img_actual_tamano = (0, 0)

    @classmethod
    def clear_frame(cls):
        for widget in cls.main_frame.winfo_children():
            widget.destroy()

    #Esta función se encargará de inicializar todo lo referente a la ventana raíz
    @classmethod
    def initRoot(cls):
        cls.root = Tk() 
        ico = Image.open("src/media/icon.jpg")
        logo = ImageTk.PhotoImage(ico)
        cls.root.wm_iconphoto(False, logo)
        cls.root.geometry("960x540") #16:9
        cls.root.title("Teatro Escuela Carlos Mayolo")

        cls.main_frame = Frame(cls.root)
        cls.main_frame.pack(fill="both", expand=True)

        cls.window_main() 

    @classmethod
    def window_main(cls):
        cls.clear_frame()
        Main.rightFrame = Frame(cls.main_frame, borderwidth= 10, bg = Main.bg, width = 800, height = 900)
        Main.rightFrame.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)

        # FRAME IZQUIERDO (50% de la pantalla)
        cls.leftFrame = Frame(cls.main_frame, borderwidth=2, bg= Main.bg)
        cls.leftFrame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # DIVIDIR EN 2 SECCIONES: SUPERIOR E INFERIOR
        cls.topFrame = Frame(cls.leftFrame, bg="red")
        cls.topFrame.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        cls.bottomFrame = Frame(cls.leftFrame, bg="black")
        cls.bottomFrame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        # 🔹 Crear Label para la imagen
        cls.label = tk.Label(cls.bottomFrame, bg="black")
        cls.label.pack(fill="both", expand=True)  # Se expande para ocupar el frame
        


        # Esperar a que `bottomFrame` tenga tamaño antes de cargar la imagen
        cls.root.after(100, cls.update_image)  

        # Si el frame cambia de tamaño, actualizar la imagen

        cls.bottomFrame.bind("<Enter>", cls.cambiar_imagen)
        cls.bottomFrame.bind("<Configure>", cls.update_image)

        
        cls.bottomFrame.bind("<Enter>", cls.cambiar_imagen)

        #Frame izquierdo Superior
        def update_font(event):
        # Ajustar el tamaño de la fuente según el ancho de la ventana
            new_size = max(20, event.width // 30)  # Ajusta el divisor según el crecimiento deseado
            new_font = ("Calibri", new_size)
    
            cls.titleLabel.config(font=new_font, wraplength=cls.topFrame.winfo_width() * 0.9)
        cls.topFrame.grid_rowconfigure(0, weight=3)  # Parte superior (50%)
        cls.topFrame.grid_rowconfigure(1, weight=5)  # Parte inferior (50%)
        cls.topFrame.grid_columnconfigure(0, weight=1)

        # Crear el Label
        cls.titleLabel = tk.Label(
            cls.topFrame, 
            text="Bienvenido al Teatro Escuela Carlos Mayolo",
            font=("Calibri", 18),  # Tamaño inicial
            justify="center",
            anchor="center",
            wraplength=800
        )
        cls.titleLabel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
        # Vinculacion de eventos
        cls.titleLabel.bind("<Button-1>", lambda e: cls.abrir_ventana_funcionalidades())
        cls.topFrame.bind("<Configure>", update_font)

    @classmethod
    def abrir_ventana_funcionalidades(cls):
        cls.clear_frame()
        cls.navBar = tk.Frame(cls.main_frame, bg="red")
        cls.navBar.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        #Opciones navbar
        cls.inicio = tk.Button(cls.navBar, text="Inicio", command=cls.window_main)
        cls.inicio.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        cls.procesos = tk.Button(cls.navBar, text="Procesos", command=cls.mostrar_procesos)
        cls.procesos.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)


        cls.content = tk.Frame(cls.main_frame, bg="black")
        cls.content.place(relx=0.2, rely=0, relwidth=0.8, relheight=1)
        cls.Label = tk.Label(cls.content, text="Bienvenido al Teatro Escuela Carlos Mayolo", font=("Calibri", 30), wraplength=500)
        cls.Label.place(relx=0.5, rely=0.5, anchor="center")
    
    @classmethod
    def mostrar_procesos(cls):
        for widget in cls.content.winfo_children():
            widget.destroy()

        # Nuevo contenido en content
        tk.Label(cls.content, text="Sección de Procesos", font=("Calibri", 25), fg="white", bg="black").place(relx=0.5, rely=0.3, anchor="center")

        tk.Button(cls.content, text="Opción 1", font=("Calibri", 15)).place(relx=0.5, rely=0.5, anchor="center")
        tk.Button(cls.content, text="Opción 2", font=("Calibri", 15)).place(relx=0.5, rely=0.6, anchor="center")



    @classmethod
    def update_image(cls, event=None):
        """Carga y ajusta la imagen sin distorsionarla dentro del `bottomFrame`."""
        try:
            # Obtener el tamaño actual del frame
            frame_width = cls.bottomFrame.winfo_width()
            frame_height = cls.bottomFrame.winfo_height()

            # Evitar redimensionar si el tamaño aún no está definido
            if frame_width < 10 or frame_height < 10:
                return

            # Cargar la imagen original
            img = Image.open(cls.imagenes[cls.indice_imagen])

            # Obtener dimensiones originales
            img_width, img_height = img.size

            # Calcular nueva escala manteniendo la proporción
            ratio = min(frame_width / img_width, frame_height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)

            cls.img_actual_tamano = (new_width, new_height)

            # Redimensionar la imagen manteniendo la relación de aspecto
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convertir a formato de tkinter
            cls.img_tk = ImageTk.PhotoImage(img)

            # Actualizar la imagen en el Label
            cls.label.config(image=cls.img_tk)


        except Exception as e:
            print("Error al cargar la imagen:", e)
            cls.label.config(text="No se pudo cargar la imagen", fg="white", bg="black")
    @classmethod
    def detectar_mouse(cls, event):
        """Verifica si el mouse está sobre la imagen real o en el fondo negro."""
        label_width = cls.label.winfo_width()
        label_height = cls.label.winfo_height()
        img_width, img_height = cls.img_actual_tamano

        # Calcular márgenes vacíos
        margen_x = (label_width - img_width) // 2
        margen_y = (label_height - img_height) // 2

        # Si el mouse está en los márgenes, no cambiar la imagen
        if event.x < margen_x or event.x > (margen_x + img_width):
            return
        if event.y < margen_y or event.y > (margen_y + img_height):
            return

        # Si el mouse está sobre la imagen real, cambiar la imagen
        cls.cambiar_imagen()
    @classmethod
    def cambiar_imagen(cls, event=None):
        """Cambia la imagen al siguiente índice al pasar el mouse."""
        cls.indice_imagen = (cls.indice_imagen + 1) % len(cls.imagenes)  # Bucle infinito de imágenes
        cls.update_image()  # Llamar a `update_image()` para actualizar la imagen
    
    @classmethod
    def runApp(cls):
        cls.initRoot()
        ico = Image.open("src/media/icon.jpg")
        logo = ImageTk.PhotoImage(ico)
        cls.root.wm_iconphoto(False, logo)
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

        tituloCriteriosWidget.configure(font = (FieldFrame.font, 11, "bold"))
        tituloValoresWidget.configure(font = (FieldFrame.font, 11, "bold"))

        self.labels = [tituloCriteriosWidget] + [ tk.Label(self, text = label, font = (FieldFrame.font, 11), bg = FieldFrame.bg) for label in self.criterios]

        for i, label in enumerate(self.labels):
            label.grid(row = i, column = 0, padx= 3, pady= 5)
        
        self.values = [tituloValoresWidget] + [tk.Entry(self, text= value) for value in self.valores]

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
    #Main.initRoot()
    #window = FieldFrame(Main.rightFrame, criterios= criterios, valores= valores, habilitado= ["Age", "Country"])
    #print(window.getValue("Age")) #25
    #Main.root.mainloop()
    Main.runApp()
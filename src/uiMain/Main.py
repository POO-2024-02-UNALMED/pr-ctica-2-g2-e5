import tkinter as tk
from tkinter import Tk, Frame, ttk, messagebox
from PIL import Image, ImageTk
import sys
import os
import time 

#AGREGAR SRC AL PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from baseDatos.Teatro import Teatro

from gestorAplicacion.gestionVentas.Cliente import Cliente


class Main:

    debug = False
    root = None
    test = False
    fieldTest = False
    custom = False
    bg = "lightsteelblue3"
    custom = False

    @classmethod
    def wait(cls):
        if cls.debug:
            return 
        else:
            time.sleep(2)

    @classmethod
    def update_font(cls, event, frame, text, tamano, reescalamiento, aplicar):
        """Actualiza el tamaño de la fuente del título al cambiar el tamaño de la ventana."""
        # new_size = max(tamano, event.width // reescalamiento)
        if aplicar:
            if event.height < 140 or event.width < 350:
                new_size = max(8, min(event.height // 8, event.width // 20))
                wrap_length = min(frame.winfo_height() * 5, frame.winfo_width() * 0.85)
            else:
                new_size = max(tamano, event.width // reescalamiento)
                wrap_length = min(frame.winfo_height() * 5, frame.winfo_width() * 0.85)
        else:
            new_size = max(tamano, event.width // reescalamiento)
            wrap_length = frame.winfo_width() * 0.9

        new_font = ("Calibri", new_size)
        
        text.config(font=new_font, wraplength=wrap_length)
    
    @classmethod
    def resize(cls, frame, text, tamano = 18, reescalamiento = 30, aplicar = True):
        frame.bind("<Configure>", lambda e: cls.update_font(e, frame, text, tamano, reescalamiento, aplicar))

    # --- NUEVAS VARIABLES PARA PROGRAMADORES ---
    current_programador_index = -1
    programadores = [
        ("Programador 1:\nNombre: Francisco Jose Ceren Porto\n Edad: 17 \nID: 1023631713",
         ["src/media/Programadores/perro.png", "src/media/Programadores/perro.png", "src/media/Programadores/perro.png", "src/media/Programadores/perro.png"]),
        ("Programador 2:\nNombre: Danna Valeria Perez Niño\n Edad: 17 \nID: 1052839541",
         ["src/media/Programadores/Perro2.png", "src/media/Programadores/Perro2.png", "src/media/Programadores/Perro2.png", "src/media/Programadores/Perro2.png"]),
        ("Programador 3:\nNombre: Oscar David Arango Garcia\n Edad: 17 \nID: 1011591946",
         ["src/media/Programadores/Perro3.png", "src/media/Programadores/Perro3.png", "src/media/Programadores/Perro3.png", "src/media/Programadores/Perro3.png"]),
        ("Programador 4:\nNombre: Juan Pablo Miras Cañas\n Edad: 18 \nID: 4",
         ["src/media/Programadores/Pablo.png", "src/media/Programadores/Pablo.png", "src/media/Programadores/Pablo.png", "src/media/Programadores/Pablo.png"]),
        ("Programador 5:\nNombre: Miguel Velez Bernal\n Edad: 18 \nID: 1023524572",
         ["src/media/Programadores/Velez.png", "src/media/Programadores/Velez.png", "src/media/Programadores/Velez.png", "src/media/Programadores/Velez.png"])
    ]

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
    def exit(cls):
        Teatro.serializar()
        cls.root.destroy()

    @classmethod
    def window_main(cls):

        menuBar = tk.Menu(cls.root)
        cls.root.config(menu=menuBar)
        menuInicio = tk.Menu(menuBar, tearoff=False)
        menuBar.add_cascade(menu=menuInicio, label="Inicio")
    
        menuInicio.add_command( label="Salir", command = cls.exit)
        menuInicio.add_command( label="Descripcion",  command = lambda: cls.titleLabel.config(text = "Lorem ipsum")) 
        cls.clear_frame()

        # CREACIÓN DEL RIGHT FRAME (usado para programadores)
        Main.rightFrame = Frame(cls.main_frame, borderwidth= 10, bg = Main.bg, width = 800, height = 900)
        Main.rightFrame.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)

        # FRAME IZQUIERDO (50% de la pantalla)
        cls.leftFrame = Frame(cls.main_frame, borderwidth=2, bg= Main.bg)
        cls.leftFrame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # DIVIDIR EN 2 SECCIONES(FRAME IZQUIERDO): SUPERIOR E INFERIOR
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


        #Frame izquierdo Superior
    

        # Crear el Label
        cls.titleLabel = tk.Label(
            cls.topFrame, 
            text="Bienvenido al Teatro Escuela Carlos Mayolo",
            font=("Calibri", 18),  # Tamaño inicial
            justify="center",
            anchor="center",
            wraplength=800
        )
        cls.titleLabel.place(relx=0.5, rely=0.5, anchor="center")
    
        # Vinculacion de eventos
        cls.titleLabel.bind("<Button-1>", lambda e: cls.abrir_ventana_funcionalidades())
        cls.resize(cls.topFrame, cls.titleLabel)

        #En este método está todo lo relacionado a la sección de programadores
        cls.init_programador_functionality()

    """
    Inicializa la sección de programadores en el RightFrame.
    Se crean dos subframes:
        - programadorFrameTop: contiene un botón que muestra la info del programador.
        - programadorFrameBottom: muestra en formato 2x2 las imágenes asociadas.
    """
    @classmethod
    def init_programador_functionality(cls):
        cls.programadorFrameTop = tk.Frame(cls.rightFrame, bg="skyblue")
        cls.programadorFrameTop.place(relx=0, rely=0, relwidth=1, relheight=0.3)
        
        cls.programadorFrameBottom = tk.Frame(cls.rightFrame, bg="lightgreen")
        cls.programadorFrameBottom.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)
        
        cls.btn_info = tk.Button(cls.programadorFrameTop, text="Programadores", command=cls.update_programador)
        cls.btn_info.pack(expand=True, fill="both")

        # Vincula el evento <Configure> del frame superior para actualizar la fuente del botón
        cls.programadorFrameTop.bind(
            "<Configure>",
            cls.resize(cls.programadorFrameTop, cls.btn_info)
        )

    """
    Actualiza la información y las imágenes del programador mostrado.
    """
    @classmethod
    def update_programador(cls):
        # Actualizar índice y obtener datos del siguiente programador
        cls.current_programador_index = (cls.current_programador_index + 1) % len(cls.programadores)
        info, image_paths = cls.programadores[cls.current_programador_index]
        cls.btn_info.config(text=info)
        
        # Limpiar el contenido previo del frame inferior
        for widget in cls.programadorFrameBottom.winfo_children():
            widget.destroy()
        
        # Lista para mantener referencias a las imágenes y evitar que sean recolectadas
        cls.programadorFrameBottom.image_refs = []
        
        # Configurar la cuadrícula: 2 filas y 2 columnas
        for i in range(2):
            cls.programadorFrameBottom.rowconfigure(i, weight=1)
            cls.programadorFrameBottom.columnconfigure(i, weight=1)
        
        cls.programadorFrameBottom.update_idletasks()
        frame_width = cls.programadorFrameBottom.winfo_width()
        frame_height = cls.programadorFrameBottom.winfo_height()
        cell_width = frame_width // 2
        cell_height = frame_height // 2
        
        # Cargar, redimensionar y colocar las 4 imágenes en la cuadrícula
        for idx, img_path in enumerate(image_paths):
            try:
                pil_image = Image.open(img_path)
                pil_image = pil_image.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print(f"Error al cargar la imagen {img_path}: {e}")
                img = tk.PhotoImage(width=cell_width, height=cell_height)
            cls.programadorFrameBottom.image_refs.append(img)
            label = tk.Label(cls.programadorFrameBottom, image=img, bg="white")
            label.grid(row=idx // 2, column=idx % 2, sticky="nsew", padx=5, pady=5)

    @classmethod
    def abrir_ventana_funcionalidades(cls):
        cls.root.destroy()

        cls.new_window = tk.Tk()
        cls.new_window.title("Teatro Escuela Carlos Mayolo")
        cls.new_window.geometry("960x540")

        cls.menu_bar = tk.Menu(cls.new_window)
        menu_archivo = tk.Menu(cls.menu_bar, tearoff=False)
        menu_archivo.add_command(label="Aplicacion", command=cls.ventanaDialogo)
        menu_archivo.add_command(label="Salir", command=cls.volver)
        cls.menu_bar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_procesos = tk.Menu(cls.menu_bar, tearoff=0)
        menu_procesos.add_command(label="Gestion de Ventas", command=cls.gestionVentas)
        menu_procesos.add_command(label="Gestion de Empleados", command=cls.gestionEmpleados)
        menu_procesos.add_command(label="Gestion de Obras", command=cls.gestionObras)
        menu_procesos.add_command(label="Gestion de Clases", command=cls.gestionClases)
        menu_procesos.add_command(label="Contratar Actores", command=cls.contratarActores)
        cls.menu_bar.add_cascade(label="Procesos y Consultas", menu=menu_procesos)
        menu_ayuda = tk.Menu(cls.menu_bar, tearoff=0)
        menu_ayuda.add_command(label="Acerca de", command=cls.autores)
        cls.menu_bar.add_cascade(label="Ayuda", menu=menu_ayuda)

        # Configurar el menú en la ventana principal
        cls.new_window.config(menu=cls.menu_bar)

        #contenido
        cls.content = tk.Frame(cls.new_window, bg="black")
        cls.content.place(relx=0, rely=0, relwidth=1, relheight=1)
        cls.Label = tk.Label(cls.content, text="Bienvenido al Teatro Escuela Carlos Mayolo", font=("Calibri", 30), wraplength=500)
        cls.Label.place(relx=0.5, rely=0.5, anchor="center")
        
        cls.new_window.focus_force()

    @classmethod
    def volver(cls):
        cls.new_window.destroy()
        cls.root.deiconify()

    @classmethod
    def ventanaDialogo(cls):
        messagebox.showinfo("Aplicacion", "Bienvenido a la aplicacion")
    
    def autores():
        messagebox.showinfo("Acerca de", "Autores: \n- Francisco Jose Ceren Porto\n- Danna Valeria Perez Niño\n- Oscar David Arango Garcia\n- Juan Pablo Miras Cañas\n- Miguel Velez Bernal")

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
        Teatro.deserializar()

        cls.initRoot()
        ico = Image.open("src/media/icon.jpg")
        logo = ImageTk.PhotoImage(ico)
        cls.root.wm_iconphoto(False, logo)
        cls.root.mainloop()

    @classmethod
    def gestionVentas(cls):


        def Usuario_Nuevo():
            for widget in cls.content.winfo_children():
                widget.destroy()

                
            #SE CREARA UN NUEVO ID
            code = Cliente.id_random()

            global cliente
            cliente = Cliente(id = code)
            messagebox.showinfo("Éxito", f"Su nuevo ID es {cliente.id}")
            Inicio_preguntas()
            
        
        def validar(a):
                texto =a.get()
                value = False
                try:
                    numero = int(texto)  # Intenta convertir a entero
 
                except ValueError:
                    value = True
                if value:
                    messagebox.showerror("Error", "Ingrese un numero entero")
                elif not Cliente.verificar(numero):  # Si está vacío
                    messagebox.showerror("Error", "Id no existente")
                else:
                    messagebox.showinfo("Éxito", "Iniciando sesion")
                    Inicio_preguntas()
        def Usuario_Antiguo():
            for widget in cls.content.winfo_children():
                widget.destroy()
            
            cliente=Cliente(id=12)
            
            
            frame_izq = tk.Frame(cls.content, bg="blue")
            frame_izq.place(relx=0, rely=0, relwidth=0.15, relheight=1)  # Se ubica en la izquierda

            # Frame derecho
            frame_der = tk.Frame(cls.content, bg="blue")
            frame_der.place(relx=0.85, rely=0,relwidth=0.15, relheight=1)

            frame_2 = tk.Frame(cls.content, bg="black", padx=15, pady=20)
            frame_2.place(relx=0.5, rely=0.80,anchor="center")
            
            frame = tk.Frame(cls.content, bg="white", padx=20, pady=20)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            top_frame = Frame(cls.content,background="black")
            top_frame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

            top_label = tk.Label(top_frame,text="Venta de tiquetes",font=("Calibri", 25), bg="black",fg="white")
            top_label.place(relx=0.5, rely=0.1, anchor="n")

            pregunta1= FieldFrame(root=frame,tituloCriterios="Ingresa tu ID",combobox=True)
            #pregunta1.pack()

            

        # Etiqueta
            label = tk.Label(frame, text="Ingresa tu ID:", font=("Arial", 14), bg="white")
            label.pack(pady=10)

        # Cuadro de texto
            entry = tk.Entry(frame, font=("Arial", 14))
            entry.pack(pady=5)

            boton = tk.Button(frame, text="Aceptar", font=("Arial", 12),command= lambda : validar(entry))
            boton.pack(pady=10)

            boton = tk.Button(frame_2, text="Crear un nuevo usuario", font=("Arial", 12),command= Usuario_Nuevo)
            boton.pack(pady=10)

            
        def Inicio_preguntas():
            
            frame_izq = tk.Frame(cls.content, bg="blue")
            frame_izq.place(relx=0, rely=0, relwidth=0.15, relheight=1)  # Se ubica en la izquierda

            # Frame derecho
            frame_der = tk.Frame(cls.content, bg="blue")
            frame_der.place(relx=0.85, rely=0,relwidth=0.15, relheight=1)

            top_frame = Frame(cls.content,background="black")
            top_frame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

            frame_central = tk.Frame(cls.content, bg="white")
            frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)

            frame_central = tk.Frame(cls.content, bg="white")
            frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)

            top_label = tk.Label(top_frame,text="Venta de tiquetes",font=("Calibri", 25), bg="black",fg="white")
            top_label.place(relx=0.5, rely=0.1, anchor="n")

            label = tk.Label(cls.content,text="Desea mejorar su suscripcion?", font=("Calibri", 25), fg="black",bg="white")
            label.place(relx=0.5, rely=0.3, anchor="center")

            Button_Si = tk.Button(cls.content, text="Si", font=("Calibri", 15),command=Usuario_Nuevo)
            Button_No = tk.Button(cls.content, text="No", font=("Calibri", 15),command=Usuario_Antiguo)
            Button_Si.place(relx=0.48, rely=0.5, anchor="center")
            Button_No.place(relx=0.53, rely=0.5, anchor="center")

            Main.wait()

            
            




        for widget in cls.content.winfo_children():
            widget.destroy()
        
        frame_izq = tk.Frame(cls.content, bg="blue")
        frame_izq.place(relx=0, rely=0, relwidth=0.15, relheight=1)  # Se ubica en la izquierda

        # Frame derecho
        frame_der = tk.Frame(cls.content, bg="blue")
        frame_der.place(relx=0.85, rely=0,relwidth=0.15, relheight=1)

        top_frame = Frame(cls.content,background="black")
        top_frame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

        frame_central = tk.Frame(cls.content, bg="white")
        frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)

        frame_central = tk.Frame(cls.content, bg="white")
        frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)

        top_label = tk.Label(top_frame,text="Venta de tiquetes",font=("Calibri", 25), bg="black",fg="white")
        top_label.place(relx=0.5, rely=0.1, anchor="n")

        """"top_label.bind(
            "<Configure>",
            lambda e: cls.resize(top_frame,top_label, 60, 100)
        )"""

        label = tk.Label(cls.content,text="Eres un cliente nuevo?", font=("Calibri", 25), fg="black",bg="white")
        label.place(relx=0.5, rely=0.3, anchor="center")

        Button_Si = tk.Button(cls.content, text="Si", font=("Calibri", 15),command=Usuario_Nuevo)
        Button_No = tk.Button(cls.content, text="No", font=("Calibri", 15),command=Usuario_Antiguo)
        Button_Si.place(relx=0.5, rely=0.5, anchor="center")
        Button_No.place(relx=0.5, rely=0.6, anchor="center")

        


        

    @classmethod
    def gestionEmpleados(cls):
        for widget in cls.content.winfo_children():
            widget.destroy()
            
        # Encabezado
        Titulo = Frame(cls.content, bg="white")
        Titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        TituloLabel = tk.Label(Titulo, text="Bienvenido a la gestion de empleados", font=("Calibri"))
        TituloLabel.pack(fill="both", expand=True)
        TituloLabel.bind("<Configure>", lambda e: cls.resize(Titulo, TituloLabel, 8, 60, False))

    @classmethod
    def gestionObras(cls):
        for widget in cls.content.winfo_children():
            widget.destroy()
    
    @classmethod
    def contratarActores(cls):
        for widget in cls.content.winfo_children():
            widget.destroy()

        #frame izquierdo
        leftFrame = tk.Frame(cls.content, bg="blue")
        leftFrame.place(relx=0, rely=0, relwidth=0.15, relheight=1)

        # Frame derecho
        rightFrame = tk.Frame(cls.content, bg="blue")
        rightFrame.place(relx=0.85, rely=0,relwidth=0.15, relheight=1)

        #posible barra de avance
        bottomFrame = tk.Frame(cls.content, bg="black", padx=15, pady=20)
        bottomFrame.place(relx=0.5, rely=0.80,anchor="center")
        
        centerFrame = tk.Frame(cls.content, bg="purple", padx=20, pady=20)
        centerFrame.place(relx=0.15, rely=0.1, relwidth=.7, relheight=.8)

        captionFrame = Frame(cls.content,background="black")
        captionFrame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

        #captionframe contiene el mensaje de bienvenida la funcionalidad
        caption = tk.Label(captionFrame, 
                           text="Bienvenido al panel de contratación de actores.",
                           font= ("Calibri", 10))
        caption.place(relx = 0, rely = 0, relheight= 1, relwidth= 1)
        
        #reasignación de tamaño de letra
        captionFrame.bind(
            "<Configure>",
            lambda e: cls.resize(captionFrame, caption, 10, 60, False)
        )

        centerFrame.columnconfigure(0, weight=1) 
        centerFrame.columnconfigure(1, weight=1) 

        #assignFrame cumple tres funciones: si un frame existe, lo remueve de la pantalla
        # luego remueve los widgets que tuviera asociado (opciona)
        # por ultimo lo coloca de nuevo con place en las nuevas posiciones relativas
        def assignFrame(frame, relx, rely, relheight, relwidth, destroy = True):
            frame.place_forget()
            
            if destroy:
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Frame) and not isinstance(widget, FieldFrame):
                        continue
                    widget.destroy()
            
            frame.place(relx = relx, rely= rely, relheight= relheight, relwidth= relwidth)

        #----------------------- PRIMERA RONDA DE PREGUNTAS AL USUARIO --------------------------------
        
        #PREGUNTA NO. 1
        criteriosTipoEmpresa = ["Tipo de Empresa"]
        valoresTipoEmpresa = [["Empresa registrada", "Empresa nueva"]]

        historialEmpresa = None
        empresa = None

        #Teatro.getInstancia().getClientes().append( Cliente(id = 426, tipo= "Empresa")  )

        def locateId(fieldframe: FieldFrame):
            fieldframe.gatherEntries()
            id = fieldframe.getValue("Inserte ID existente")

            try:
                id = int(id)
            except Exception:
                messagebox.showerror("Error", "La entrada no puede convertirse a entero")
                return
            
            idFlag = False
            for cliente in Teatro.getInstancia().getClientes():
                if cliente.getId() == id and cliente.getTipo() == "Empresa":
                    messagebox.showinfo("Success", "Cliente confirmado en base de datos")
                    historialEmpresa = cliente.getHistorial()
                    empresa = cliente
                    idFlag = True
                    Teatro.serializar()
                if not idFlag:
                    messagebox.showerror("Error", "El número de identificación no existe en la base de datos de empresa.\nRevise si el cliente es de tipo Empresa o si se digitó correctamente.")

        def definirTipoEmpresa(fieldframe: FieldFrame, topFrame: Frame) -> None:
            fieldframe.gatherEntries()

            choice = fieldframe.getValue("Tipo de Empresa")
            if choice in ["Empresa registrada", "Empresa nueva"]:
                tk.Label(topFrame, text= "Opción escogida: " + choice).pack()
                print(choice == "Empresa registrada")
                
                if choice == "Empresa registrada":
                    id = FieldFrame(topFrame, 
                                    criterios= ["Inserte ID existente"], 
                                    tituloCriterios= "", 
                                    tituloValores= "", 
                                    valores = [""],
                                    command= lambda: locateId(id))
                    id.place(relwidth= 1, relheight= 1)
                    
                elif choice == "Empresa Nueva":
                    id = FieldFrame(topFrame,
                                    criterios= ["Generar nuevo ID"], 
                                    tituloCriterios= "", 
                                    tituloValores= "", 
                                    valores = [""])
                    id.place(relwidth= 1, relheight= .3)

            else:
                ##MANEJO DE EXCEPCION
                messagebox.showerror("Error", "Opción Inválida")

        pregunta1 = FieldFrame(root = centerFrame, 
                               criterios = criteriosTipoEmpresa,
                               valores = valoresTipoEmpresa,
                               combobox= True,
                               command= lambda: definirTipoEmpresa(pregunta1, centerFrame))

        pregunta1.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)
        
        #continuar = tk.Button(centerFrame, text="Continuar")
        #continuar.place(relx=0.4, rely=0.82, relwidth= .2, relheight= .06)




    @classmethod
    def gestionClases(cls):
        # Se limpia el frame de contenido actual (línea ~320)
        for widget in cls.content.winfo_children():
            widget.destroy()

        # --- FRAME DE BIENVENIDA ---
        frame_bienvenida = Frame(cls.content, bg="red")
        frame_bienvenida.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        saludo = tk.Label(frame_bienvenida,
                          text="Bienvenido a la gestión de clases",
                          font=("Calibri", 16),
                          bg="black", fg="white")
        saludo.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame_bienvenida.bind("<Configure>", lambda e: cls.resize(frame_bienvenida, saludo))

        # --- FRAME PRINCIPAL PARA EL PROCESO ---
        process_frame = Frame(cls.content, bg="white")
        process_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        # ----------- PASO 1: Mostrar Artistas existentes y solicitar ID -----------
        def step1():
            for widget in process_frame.winfo_children():
                widget.destroy()
            
            # Se obtienen los artistas existentes de la base de datos (suponiendo que Teatro.getInstancia().getArtistas() exista)
            artistas = Teatro.getInstancia().getArtistas()
            if artistas:
                lbl_artistas = tk.Label(process_frame, text="Artistas existentes en la base de datos:", font=("Calibri", 14), bg="white")
                lbl_artistas.pack(pady=10)
                txt_artistas = tk.Text(process_frame, height=10, width=80, font=("Calibri", 12))
                txt_artistas.pack(pady=10)
                for artista in artistas:
                    # Se diferencia actor de director (asumimos que si tiene atributo "edad" es actor)
                    if hasattr(artista, "edad"):
                        linea = f"- Actor {artista.nombre} con ID {artista.id}\n"
                    else:
                        linea = f"- Director {artista.nombre} con ID {artista.id}\n"
                    txt_artistas.insert("end", linea)
                txt_artistas.config(state="disabled")
            else:
                tk.Label(process_frame, text="No hay artistas en la base de datos.", font=("Calibri", 14), bg="white").pack(pady=10)
            
            # Se solicita el ID del artista
            lbl_id = tk.Label(process_frame, text="Ingrese el ID del artista para gestionar clases:", font=("Calibri", 14), bg="white")
            lbl_id.pack(pady=10)
            entry_id = tk.Entry(process_frame, font=("Calibri", 14))
            entry_id.pack(pady=5)
            btn_buscar = tk.Button(process_frame, text="Buscar", font=("Calibri", 14),
                                   command=lambda: process_artist(entry_id.get()))
            btn_buscar.pack(pady=10)


        


class FieldFrame(Frame):

    bg = "slategray1"
    font = "Calibri 11"

    def __init__(self, root: Tk, tituloCriterios: str = "Requerimientos", criterios: list = [], tituloValores: str = "Por favor digite:", valores: list = None, habilitado: list = None, combobox = False, command = None):
        #todos los colores en tkinter: https://www.plus2net.com/python/tkinter-colors.php
        super().__init__(master = root, width = 800, height = 450, bg = FieldFrame.bg) #16:9
        self.root = root
        self.tituloCriterios = tituloCriterios
        self.criterios = criterios
        self.tituloValores = tituloValores
        self.valores = valores if valores is not None else []
        self.habilitado = habilitado
        self.combobox = combobox

        tituloCriteriosWidget = tk.Label(self, text = self.tituloCriterios, bg = FieldFrame.bg)
        tituloValoresWidget = tk.Label(self, text = self.tituloValores, bg = FieldFrame.bg)

        tituloCriteriosWidget.configure(font = (FieldFrame.font, 11, "bold"))
        tituloValoresWidget.configure(font = (FieldFrame.font, 11, "bold"))

        #expande las columnas según crece la pantalla
        self.columnconfigure(0, weight=2) 
        self.columnconfigure(1, weight=1)  
        self.columnconfigure(2, weight=2)  

        self.labels = [tituloCriteriosWidget] + [ tk.Label(self, text = label, font = (FieldFrame.font, 11), bg = FieldFrame.bg) for label in self.criterios]
        
        for i, label in enumerate(self.labels):
            label.grid(row = i, column = 0, padx= 3, pady= 5)
            self.rowconfigure(i, weight=1)

        self.criteriosStringVar = [tk.StringVar(self, value="") for _ in self.valores]
        
        if not combobox:
            self.values = [tituloValoresWidget] + [tk.Entry(self, text= value) for value in self.valores]
        else:
            self.values = [tituloValoresWidget] + [ttk.Combobox(self, values= value, textvariable= self.criteriosStringVar[i]) for i, value in enumerate(self.valores)]
        


        habilitadoExists = habilitado is not None

        for i, value in enumerate(self.values):
            if i > 0 and self.valores:
                value.insert(0, self.valores[i-1]) # i-1 por el desfase que da agregar el titulo de la columna de valores
                
                if habilitadoExists:
                    status = "normal" if self.criterios[i-1] in habilitado else "disabled"
                    value.configure(state= status)
            value.grid(row = i, column = 2,)# padx= 10, pady= 10)

        aceptar = tk.Button(self, text = "Guardar", command = self.gatherEntries if command is None else command)
        aceptar.grid(row = len(self.valores) + 1, column = 1, sticky= "ew")

        borrar = tk.Button(self, text = "Borrar", command = self.deleteEntries)
        borrar.grid(row = len(self.valores) + 2, column = 1, sticky= "ew")

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
    criterios = ["Name"]#, "Age", "Email", "Bitcoin", "Country", "Number"]
    valores = ["John Doe"]#, "25", "john@example.com", "293090237hjkhjk2j", "Rhodesia", "892962"]

    Main.runApp()
    #root = Tk()
    #Main.initRoot()
    #window = FieldFrame(root, criterios= criterios, valores= valores, habilitado= ["Age", "Country"]).pack()
    #print(window.getValue("Age")) #25
    Main.root.mainloop()
    #Main.runApp()
    #root.mainloop()
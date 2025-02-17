import tkinter as tk
from tkinter import Tk, Frame, ttk, messagebox
from datetime import date, timedelta, datetime, time
from PIL import Image, ImageTk
import sys
import os
import time as t
import random








#AGREGAR SRC AL PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from baseDatos.Teatro import Teatro

from gestorAplicacion.gestionVentas.Cliente import Cliente
from gestorAplicacion.gestionFinanciera.Empleado import Empleado
from gestorAplicacion import gestionObras
from gestorAplicacion.gestionFinanciera.Empleado import Empleado
from gestorAplicacion.gestionClases.Profesor import Profesor
from gestorAplicacion.herramientas.Aptitud import Aptitud
from gestorAplicacion.herramientas.Genero import Genero
from gestorAplicacion.gestionObras.Artista import Artista
from gestorAplicacion.gestionObras.Actor import Actor
from gestorAplicacion.gestionObras.Obra import Obra
from gestorAplicacion.gestionObras.Director import Director
from gestorAplicacion.herramientas.Suscripcion import Suscripcion

from baseDatos.memory import resetMemory




class Main:

    debug = False
    root = None
    fieldTest = False
    reset = True
    filterDebug = True
    bg = "lightsteelblue3"

    @classmethod
    def wait(cls):
        if cls.debug:
            return 
        else:
            t.sleep(2)

    @classmethod
    def getWeek(cls):
        return [date.today() + timedelta(days= i) for i in range(7) ]

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
    def clear_frame(cls, frame):
        for widget in frame.winfo_children():
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
        cls.titleLabel.bind("<Button-1>", lambda e: cls.abrir_nueva_ventana())
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
    def abrir_nueva_ventana(cls):
        cls.root.destroy()

        cls.new_window = tk.Tk()
        cls.new_window.title("Teatro Escuela Carlos Mayolo")
        cls.new_window.geometry("960x540")

        cls.menu_bar = tk.Menu(cls.new_window)
        menu_archivo = tk.Menu(cls.menu_bar, tearoff=False)
        menu_archivo.add_command(label="Aplicacion", command=cls.aplicacion)
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
        cls.initRoot()
        cls.root.focus_force()

    @classmethod
    def ventanaDialogo(cls, mensaje, accion = None):
        messagebox.showinfo("info", mensaje)
        if accion:
            accion()
    def aplicacion():
        messagebox.showinfo("Aplicacion", "Bienvenido al Teatro Escuela")

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
        
        if cls.reset:
            resetMemory()

        cls.initRoot()
        ico = Image.open("src/media/icon.jpg")
        logo = ImageTk.PhotoImage(ico)
        cls.root.wm_iconphoto(False, logo)
        cls.root.mainloop()

    @classmethod
    def gestionVentas(cls):
        for i in Teatro.getInstancia().getClientes():
            print(i.getId())


        def Usuario_Nuevo():


                
            #SE CREARA UN NUEVO ID
            code = Cliente.id_random()

            global cliente
            cliente = Cliente(id = code)
            messagebox.showinfo("Éxito", f"Su nuevo ID es {cliente.getId()}")
            Inicio_preguntas()
            
        
        def validar(texto):
                
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
            global cliente
            cliente=Cliente(id=12)
            
            
            frame_izq = tk.Frame(cls.content, bg="slategray")
            frame_izq.place(relx=0, rely=0, relwidth=0.15, relheight=1)  # Se ubica en la izquierda

            # Frame derecho
            frame_der = tk.Frame(cls.content, bg="slategray")
            frame_der.place(relx=0.85, rely=0,relwidth=0.15, relheight=1)

            

            frame_central = tk.Frame(cls.content, bg="slategray1",name="central")
            frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)

            frame_2 = tk.Frame(frame_central, bg="slategray2", padx=15, pady=20)
            frame_2.place(relx=0.5, rely=0.85,anchor="center")
            
            frame = tk.Frame(frame_central, bg="slategray2", padx=20, pady=20)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            top_frame = Frame(cls.content,background="black")
            top_frame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

            top_label = tk.Label(top_frame,text="Venta de tiquetes",font=("Calibri", 25), bg="black",fg="white")
            top_label.place(relx=0.5, rely=0.1, anchor="n")



            

        # Etiqueta
            """label = tk.Label(frame, text="Ingresa tu ID:", font=("Arial", 14), bg="slategray3")
            label.pack(pady=10)

        # Cuadro de texto
            entry = tk.Entry(frame, font=("Arial", 14))
            entry.pack(pady=5)

            boton = tk.Button(frame, text="Aceptar", font=("Arial", 12),command= lambda : validar(entry))
            boton.pack(pady=10)

            boton = tk.Button(frame_2, text="Crear un nuevo usuario", font=("Arial", 12),command= Usuario_Nuevo)
            boton.pack(pady=10)"""

            id = FieldFrame(
                frame_central,
                tituloCriterios= "Inicia Sesion",
                tituloValores= "INGRESA TU ID",
                criterios=["ID"],
                valores= [""],
                command= lambda : validar_id(id)
                
            )
            id.place(relheight= 1, relwidth= 1)
        def validar_id(fieldframe : FieldFrame):
            fieldframe.gatherEntries()
            suscripcion = fieldframe.getValue("ID")
            validar(suscripcion)



            
        def Inicio_preguntas():
            for widget in cls.content.winfo_children():
                widget.destroy()
            global frame_central
            
            frame_izq = tk.Frame(cls.content, bg="slategray")
            frame_izq.place(relx=0, rely=0, relwidth=0.15, relheight=1)  # Se ubica en la izquierda

            # Frame derecho
            frame_der = tk.Frame(cls.content, bg="slategray")
            frame_der.place(relx=0.85, rely=0,relwidth=0.15, relheight=1)

            top_frame = Frame(cls.content,background="black")
            top_frame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

            frame_central = tk.Frame(cls.content, bg="slategray1",name="central")
            frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)



            top_label = tk.Label(top_frame,text="Venta de tiquetes",font=("Calibri", 25), bg="black",fg="white")
            top_label.place(relx=0.5, rely=0.1, anchor="n")

            label = tk.Label(cls.content,text="Desea mejorar su suscripcion?", font=("Calibri", 25), fg="black",bg="slategray2",name="suscripcion")
            label.place(relx=0.5, rely=0.3, anchor="center")

            Button_Si = tk.Button(cls.content, text="Si", font=("Calibri", 15),command=adquirir_suscripcion,name="no")
            Button_No = tk.Button(cls.content, text="No", font=("Calibri", 15),command=continuar,name="si")
            
            Button_Si.place(relx=0.48, rely=0.5, anchor="center")
            Button_No.place(relx=0.53, rely=0.5, anchor="center")

            Main.wait()
        
        def adquirir_suscripcion():
            
            global frame_central
            
            try:
                widget = cls.content.nametowidget("si") 
                widget.destroy()
                widget = cls.content.nametowidget("no") 
                widget.destroy()
                widget = cls.content.nametowidget("suscripcion") 
                widget.destroy()
            except KeyError:
                None
            susc = FieldFrame(
                frame_central,
                tituloCriterios= "tipos de suscripcion",
                tituloValores= "Respuesta",
                criterios=["Eleccion"],
                valores= [["BASICA","PREMIUM","VIP","GOLD"]],
                combobox= True,
                command=lambda :asignar_suscripcion(susc)
                
            )
            susc.place(relheight= 1, relwidth= 1)
            main_label = tk.Label(frame_central,bg = "slategray1",text="BÁSICA $0.00 -------\n\nPREMIUM \n$11,900.00\n 10% de Descuento\nEN TODAS LAS FUNCIONES\nY ASIENTOS\n\nVIP \n$18,900.00\n 25% de Descuento\nEN TODAS LAS FUNCIONES\nY ASIENTOS\n\nELITE \n$39,900.00 \nFUNCIONES GRATIS\nILIMITADAS Y\nASIENTO GOLD GRATIS")
            main_label.place(relx=0.53, rely=0.5, anchor="center")
            
        def asignar_suscripcion(fieldframe: FieldFrame):
            global cliente
            
            fieldframe.gatherEntries()
            suscripcion = fieldframe.getValue("Eleccion")
            if suscripcion == "BASICA":
                cliente.set_suscripcion(Suscripcion.BASICA.value)
            elif suscripcion == "VIP":
                cliente.set_suscripcion(Suscripcion.VIP.value)
            elif suscripcion == "PREMIUM":
                cliente.set_suscripcion(Suscripcion.PREMIUM.value)
            elif suscripcion == "ELITE":
                cliente.set_suscripcion(Suscripcion.ELITE.value)
            else:
                raise ValueError("Suscripción no válida")
            
            print(cliente.get_suscripcion())
            continuar()
        
   







        def continuar():
            try:
                widget = cls.content.nametowidget("central") 
                widget.destroy()

            except KeyError:
                print("error frame")
            try:
                widget = cls.content.nametowidget("central") 
                widget.destroy()
                widget = cls.content.nametowidget("si") 
                widget.destroy()
                widget = cls.content.nametowidget("no") 
                widget.destroy()
                widget = cls.content.nametowidget("suscripcion") 
                widget.destroy()
            except KeyError:
                print("error label")
            frame_central = tk.Frame(cls.content, bg="slategray1",name="central")
            frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)
            lista=[]

            obra1 = Obra(nombre="pepe")
            obra2 = Obra(nombre="dante")
            obra3 = Obra(nombre="labella")
            for obra in Teatro.getInstancia().getObras():
                if obra.getNombre() != "NOTFORITE":
                    lista.append(obra.getNombre())


            obr = FieldFrame(
                frame_central,
                tituloCriterios= "Obras",
                tituloValores= "Respuesta",
                criterios=["Eleccion"],
                valores= [lista],
                combobox= True,
                command=lambda :asignar_obra(obr)
                
            )
            obr.place(relheight= 1, relwidth= 1)
            texto = Obra.generarTabla1()

            tree = ttk.Treeview(frame_central, columns=("Nombre", "Género", "Duración", "Precio"), show="headings",height=5)

            # Configurar encabezados
            tree.heading("Nombre", text="Nombre")
            tree.heading("Género", text="Género")
            tree.heading("Duración", text="Duración")
            tree.heading("Precio", text="Precio")

            # Ajustar tamaños de columnas
            tree.column("Nombre", width=180)
            tree.column("Género", width=100)
            tree.column("Duración", width=80)
            tree.column("Precio", width=100, anchor="e")  # Alinear precios a la derecha

            # Scrollbar vertical
            scrollbar = ttk.Scrollbar(frame_central, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # Ubicar Treeview y Scrollbar en la ventana
            tree.place(relx=0.2,rely=0.3,relwidth=0.7, relheight=0.3)
            scrollbar.place(relx=0.90,rely=0.3, relwidth=0.03, relheight=0.3)

            # Agregar datos al Treeview
            for obra in Teatro.getInstancia().getObras():
                tree.insert("", "end", values=(obra.getNombre(),"comedia", "10:00", "1.000"))



        def asignar_obra(fieldframe :FieldFrame):
            fieldframe.gatherEntries()
            suscripcion = fieldframe.getValue("Eleccion")

            global cliente

            cliente.obra=suscripcion



            



            
            




        for widget in cls.content.winfo_children():
            widget.destroy()
        
        frame_izq = tk.Frame(cls.content, bg="slategray")
        frame_izq.place(relx=0, rely=0, relwidth=0.15, relheight=1)  # Se ubica en la izquierda

        # Frame derecho
        frame_der = tk.Frame(cls.content, bg="slategray")
        frame_der.place(relx=0.85, rely=0,relwidth=0.15, relheight=1)

        top_frame = Frame(cls.content,background="black")
        top_frame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

        frame_central = tk.Frame(cls.content, bg="slategray1")
        frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)

        frame_central = tk.Frame(cls.content, bg="slategray1")
        frame_central.place(relx=0.15, rely=0.1, relwidth=0.70, relheight=0.80)

        top_label = tk.Label(top_frame,text="Venta de tiquetes",font=("Calibri", 25), bg="black",fg="white")
        top_label.place(relx=0.5, rely=0.1, anchor="n")

        """"top_label.bind(
            "<Configure>",
            lambda e: cls.resize(top_frame,top_label, 60, 100)
        )"""

        label = tk.Label(cls.content,text="Eres un cliente nuevo?", font=("Calibri", 25), fg="black",bg="slategray1")
        label.place(relx=0.5, rely=0.3, anchor="center")

        Button_Si = tk.Button(cls.content, text="Si", font=("Calibri", 15),command=Usuario_Nuevo)
        Button_No = tk.Button(cls.content, text="No", font=("Calibri", 15),command=Usuario_Antiguo)
        Button_Si.place(relx=0.5, rely=0.5, anchor="center")
        Button_No.place(relx=0.5, rely=0.6, anchor="center")

        


        

    @classmethod
    def gestionEmpleados(cls):

        for widget in cls.content.winfo_children():
            widget.destroy()
        
        def run():
            cls.clear_frame(f1)

            Anuncio = tk.Frame(f1, bg="#ffb48a")
            Anuncio.place(relx = 0.5, rely=0.4, anchor="center", relwidth=0.8, relheight=0.5)
            texto = tk.Label(Anuncio, text="Se estan pagando las deudas pendientes \nPorfavor espere...", font=("Calibri", 18), bg="#ffb48a", bd = 10, relief="raised")
            texto.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor="center")

            NOMBRES = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Carlos", "Jose", "Andres", "Sofia", "Laura", "Miguel", "Danna", "Oscar", "Frank", "Pablo"]
            APELLIDOS = ["Gomez", "Perez", "Rodriguez", "Gonzalez", "Martinez", "Hernandez", "Lopez", "Torres", "Ramirez", "Diaz", "Sanchez", "Cruz", "Jimenez", "Rojas", "Vargas", "Velez"]
            
            Teatro.getInstancia().getTesoreria().transferenciaFondos
            
            # Verificar si hay deudas y pagar

            Deudas = ""
            for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                if Persona.getDeuda() != 0:
                    if Teatro.getInstancia().getTesoreria().getCuenta().getSaldo > Persona.getDeuda():
                        transaccion = Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), Persona.getDeuda())
                        if transaccion:
                            Deudas = Deudas + "Se realizo el pago a: " + Persona.getNombre() + " por un valor de: " + str(Persona.getDeuda()) + "\n"
                            Persona.setDeuda(0)
     
            Saldo = Teatro.getInstancia().getTesoreria().getCuenta().getSaldo()

            def mostrarSaldo():
                cls.wait()
                cls.clear_frame(Anuncio)
                texto = tk.Label(Anuncio, text= Deudas + "El saldo actual de la tesoreria es: " + str(Saldo), font=("Calibri", 18), bg="#ffb48a", bd = 10, relief="raised")
                texto.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor="center")
                Anuncio.after(50, continuar)
            
            def continuar():
                cls.wait()
                cls.clear_frame(f1)
                frameSuperior = tk.Frame(f1, bg="#ffb48a")
                frameSuperior.place(relx=0, rely=0, relwidth=1, relheight=0.9, anchor="nw")
                frameInferior = tk.Frame(f1, bg="#ffb48a")
                frameInferior.place(relx=0, rely=0.9, relheight= 0.1, relwidth=1, anchor="nw")
                p1 = tk.Frame(frameSuperior, bg="#ffb48a")
                p1.pack(side= "left", fill="both", expand= True, padx=5, pady=1)
                p2 = tk.Frame(frameSuperior, bg="#ffb48a")
                p2.pack(side= "left", fill="both", expand= True, padx=5, pady=1)
                p3 = tk.Frame(frameSuperior, bg="#ffb48a")
                p3.pack(side= "left", fill="both", expand= True, padx=5, pady=1)

                botonContinuar = tk.Button(frameInferior, text="Continuar", font=("Calibri", 14),bg= "#571F1C", fg="white")
                botonContinuar.pack(fill="both", padx=10, pady=5, anchor="center")
                botonContinuar.config(command=lambda: continuar2)

                #Organizar tabla de empleados
                #Estilo tablas
                style = ttk.Style()
                style.configure("Treeview", background = "white", relief = "solid", rowheight = 25)
                style.configure("Treeview.Heading", background = "#ffb48a", foreground = "black", font = ("Calibri", 14, "bold"))
                #Seguridad
                seguridad = tk.Label(p1, text="Seguridad", font=("Calibri", 18), bg="#ffb48a")
                seguridad.pack()
                cls.resize(p1, seguridad,10, 20,False)
                #Tabla Seguridad
                # datos = [
                #     ("Juan", 25),
                #     ("Ana", 30),
                #     ("Luis", 22)
                # ]
                tablaS = ttk.Treeview(p1, columns=("Nombre", "IDs"), show="headings", style= "Treeview")
                tablaS.heading("Nombre", text="Nombre")
                tablaS.heading("IDs", text="IDs")
                tablaS.column("Nombre", width=100, anchor="center")
                tablaS.column("IDs", width=50, anchor="center")
                #Agregar los empleados
                #caso prueba
                # for emp in datos:
                #     tablaS.insert("", "end", values = emp)
                for emp in Teatro.getInstancia().getTipoSeguridad():
                    tablaS.insert("", "end", values=(emp.getNombre(), emp.getId()))
                tablaS.pack(expand=True, fill="both", padx=10, pady=5)

                #Aseador
                Aseador = tk.Label(p2, text="Aseador", font=("Calibri", 18), bg="#ffb48a")
                Aseador.pack()
                cls.resize(p2, Aseador,10, 20,False)

                #Tabla Aseador
                tablaA = ttk.Treeview(p2, columns=("Nombre", "IDs"), show="headings", style= "Treeview")
                tablaA.heading("Nombre", text="Nombre")
                tablaA.heading("IDs", text="IDs")
                tablaA.column("Nombre", width=100, anchor="center")
                tablaA.column("IDs", width=50, anchor="center")
                #Agregar los empleados
                #caso prueba
                # for emp in datos:
                    # tablaA.insert("", "end", values = emp)
                for emp in Teatro.getInstancia().getTipoAseador():
                    tablaA.insert("", "end", values=(emp.getNombre(), emp.getId()))
                tablaA.pack(expand=True, fill="both", padx=10, pady=5)

                #Profesor
                Profesor = tk.Label(p3, text="Profesor", font=("Calibri", 18), bg="#ffb48a")
                Profesor.pack()
                cls.resize(p3, Profesor,10, 20,False)

                #Tabla Profesor
                tablaP = ttk.Treeview(p3, columns=("Nombre", "IDs"), show="headings", style= "Treeview")
                tablaP.heading("Nombre", text="Nombre")
                tablaP.heading("IDs", text="IDs")
                tablaP.column("Nombre", width=100, anchor="center")
                tablaP.column("IDs", width=50, anchor="center")
                #Agregar los empleados
                #caso prueba
                # for emp in datos:
                    # tablaP.insert("", "end", values = emp)
                for emp in Teatro.getInstancia().getTipoProfesor():
                    tablaP.insert("", "end", values=(emp.getNombre(), emp.getId()))
                tablaP.pack(expand=True, fill="both", padx=10, pady=5)

                #Botones de acciones para cada tipo de empleado
                #Seguridad
                p12 = tk.Frame(p1, bg="#ffb48a")
                p12.pack(side="bottom", fill="both", pady = 5, padx=5)
                contratarS = tk.Button(p12, bg= "#571F1C" ,text = "Contratar", font = ("calibri", 12), fg="White")
                contratarS.pack(side="left", expand=True, fill="x", pady= 5, padx=10, anchor="center")
                despedirS = tk.Button(p12, bg="#571F1C", text="Despedir", font=("calibri", 12), fg = "white")
                despedirS.pack(side="left", expand= True, fill= "x", pady=5, padx=10, anchor="center")

                #Aseador
                p22 = tk.Frame(p2, bg="#ffb48a")
                p22.pack(side="bottom", fill="both", pady = 5, padx=5)
                contratarA = tk.Button(p22, bg= "#571F1C" ,text = "Contratar", font = ("calibri", 12), fg="White")
                contratarA.pack(side="left", expand=True, fill="x", pady= 5, padx=10, anchor="center")
                despedirA = tk.Button(p22, bg="#571F1C", text="Despedir", font=("calibri", 12), fg = "white")
                despedirA.pack(side="left", expand= True, fill= "x", pady=5, padx=10, anchor="center")

                #Profesor
                p32 = tk.Frame(p3, bg="#ffb48a")
                p32.pack(side="bottom", fill="both", pady = 5, padx=5)
                contratarP = tk.Button(p32, bg= "#571F1C" ,text = "Contratar", font = ("calibri", 12), fg="White")
                contratarP.pack(side="left", expand=True, fill="x", pady= 5, padx=10, anchor="center")
                despedirP = tk.Button(p32, bg="#571F1C", text="Despedir", font=("calibri", 12), fg = "white")
                despedirP.pack(side="left", expand= True, fill= "x", pady=5, padx=10, anchor="center")


                #Modificar para los empleados de la lista
                def despedirEmpleado(tabla, listaOcupacion):
                    selected_item = tabla.selection()  # Obtiene la fila seleccionada
                    if selected_item:
                        valores = tabla.item(selected_item, "values")
                        id = valores[1]
                        for emp in listaOcupacion:
                            if emp.getId() == id:
                                listaOcupacion.remove(emp)
                                break
                        for emp in Teatro.getInstancia().getEmpleadosPorRendimiento():
                            if emp.getId() == id:
                                Teatro.getInstancia().getEmpleadosPorRendimiento().remove(emp)
                                liquidacion = (emp.calcularSueldo()*1.2) + emp.getDeuda()
                                Teatro.getInstancia().getTesoreria().getCuenta().transferencia(emp.getCuenta(), liquidacion)
                                mensaje = "Se despidio a " + emp.getNombre() + " y se le pago su respectiva liquidacion"
                                cls.ventanaDialogo(mensaje)
                                break
                        tabla.delete(selected_item)

                # Modificar cada botón de "Despedir"
                despedirS.config(command=lambda: despedirEmpleado(tablaS, Teatro.getInstancia().getTipoSeguridad()))
                despedirA.config(command=lambda: despedirEmpleado(tablaA, Teatro.getInstancia().getTipoAseador()))
                despedirP.config(command=lambda: despedirEmpleado(tablaP, Teatro.getInstancia().getTipoProfesor()))

                def contratarSeguridad():
                    cls.clear_frame(f1)
                    seguridad = tk.Label(f1, text="Candidatos a Seguridad", font=("Calibri", 18), bg="#ffb48a")
                    seguridad.pack(pady=5)
                    # cls.resize(f1, seguridad,18, 40,False)
                    #Tabla Seguridad
                    candidatos = []
                    idS = []

                    n = 0
                    while n<10:
                        nombre = random.choice(NOMBRES)
                        apellido = random.choice(APELLIDOS)
                        id = random.randint(100, 1000000)
                        Nombre = f"{nombre} {apellido}"
                        candidatos.append(Nombre)
                        idS.append(id)
                        n+=1
                    
                    tabla = ttk.Treeview(f1, columns=("Nombre", "IDs"), show="headings", style= "Treeview")
                    tabla.heading("Nombre", text="Nombre")
                    tabla.heading("IDs", text="IDs")
                    tabla.column("Nombre", width=100, anchor="center")
                    tabla.column("IDs", width=50, anchor="center")
                    #Agregar los empleados
                    #caso prueba
                    for j in range(0, len(candidatos)):
                        tabla.insert("", "end", values=(candidatos[j], idS[j]))
                    tabla.pack(expand=True, fill="both", padx=30, pady=10)

                    p1 = tk.Frame(f1, bg="#ffb48a")
                    p1.pack(side="bottom", fill="both", pady = 5, padx=5)
                    contratar = tk.Button(p1, bg= "#571F1C" ,text = "Contratar", font = ("calibri", 14), fg="White")
                    contratar.pack(side="left", expand=True, fill="x", pady= 10, padx=25, anchor="center")

                    contratar.config(command=lambda: contrato(tabla, "Seguridad"))

                def contratarAseador():
                    cls.clear_frame(f1)
                    Aseador = tk.Label(f1, text="Candidatos a Aseador", font=("Calibri", 18), bg="#ffb48a")
                    Aseador.pack(pady=5)
                    # cls.resize(f1, Aseador,10, 45,False)
                    #Tabla Seguridad
                    candidatos = []
                    idS = []

                    n = 0
                    while n<10:
                        nombre = random.choice(NOMBRES)
                        apellido = random.choice(APELLIDOS)
                        id = random.randint(100, 1000000)
                        Nombre = f"{nombre} {apellido}"
                        candidatos.append(Nombre)
                        idS.append(id)
                        n+=1
                    
                    tabla = ttk.Treeview(f1, columns=("Nombre", "IDs"), show="headings", style= "Treeview")
                    tabla.heading("Nombre", text="Nombre")
                    tabla.heading("IDs", text="IDs")
                    tabla.column("Nombre", width=100, anchor="center")
                    tabla.column("IDs", width=50, anchor="center")
                    #Agregar los empleados
                    #caso prueba
                    for j in range(0, len(candidatos)):
                        tabla.insert("", "end", values=(candidatos[j], idS[j]))
                    tabla.pack(expand=True, fill="both", padx=30, pady=10)

                    p1 = tk.Frame(f1, bg="#ffb48a")
                    p1.pack(side="bottom", fill="both", pady = 5, padx=5)
                    contratar = tk.Button(p1, bg= "#571F1C" ,text = "Contratar", font = ("calibri", 14), fg="White")
                    contratar.pack(side="left", expand=True, fill="x", pady= 10, padx=25, anchor="center")

                    contratar.config(command=lambda: contrato(tabla, "Aseador"))

                def contratarProfesor():
                    cls.clear_frame(f1)
                    Profesor = tk.Label(f1, text="candidatos a Profesor", font=("Calibri", 18), bg="#ffb48a")
                    Profesor.pack(pady=5)
                    # cls.resize(f1, Profesor,10, 45,False)
                    #Tabla Profesor
                    candidatos = []
                    idS = []

                    n = 0
                    while n<10:
                        nombre = random.choice(NOMBRES)
                        apellido = random.choice(APELLIDOS)
                        id = random.randint(100, 1000000)
                        Nombre = f"{nombre} {apellido}"
                        candidatos.append(Nombre)
                        idS.append(id)
                        n+=1
                    
                    tabla = ttk.Treeview(f1, columns=("Nombre", "IDs"), show="headings", style= "Treeview")
                    tabla.heading("Nombre", text="Nombre")
                    tabla.heading("IDs", text="IDs")
                    tabla.column("Nombre", width=100, anchor="center")
                    tabla.column("IDs", width=50, anchor="center")
                    #Agregar los empleados
                    #caso prueba
                    for j in range(0, len(candidatos)):
                        tabla.insert("", "end", values=(candidatos[j], idS[j]))

                    tabla.pack(expand=True, fill="both", padx=30, pady=10)

                    p1 = tk.Frame(f1, bg="#ffb48a")
                    p1.pack(side="bottom", fill="both", pady = 5, padx=5)
                    contratar = tk.Button(p1, bg= "#571F1C" ,text = "Contratar", font = ("calibri", 14), fg="White")
                    contratar.pack(side="left", expand=True, fill="x", pady= 10, padx=25, anchor="center")

                    contratar.config(command=lambda: contrato(tabla, "Profesor"))
                
                contratarS.config(command=lambda: contratarSeguridad())
                contratarA.config(command=lambda: contratarAseador())
                contratarP.config(command=lambda: contratarProfesor())

            def contrato(tabla, ocupacion):
                selected = tabla.selection()
                if selected:
                    valores = tabla.item(selected, "values")
                    if ocupacion != "Seguridad":
                        if ocupacion != "Aseador":
                            newprofesor = Profesor(valores[0], valores[1])
                            profesores = Teatro.getInstancia().getTipoProfesor()
                            profesores.append(newprofesor)
                            Teatro.getInstancia().setTipoProfesor(profesores)
                            general = Teatro.getInstancia().getEmpleadosPorRendimiento()
                            general.append(newprofesor)
                            Teatro.getInstancia().setEmpleadosPorRendimiento(general)
                        else:
                            newAseador = Empleado(valores[0], valores[1], "Aseador")
                            Aseadores = Teatro.getInstancia().getTipoAseador()
                            Aseadores.append(newAseador)
                            Teatro.getInstancia().setTipoAseador(Aseadores)
                            general = Teatro.getInstancia().getEmpleadosPorRendimiento()
                            general.append(newAseador)
                            Teatro.getInstancia().setEmpleadosPorRendimiento(general)
                    else:
                        newSeguridad = Empleado(valores[0], valores[1], "Seguridad")
                        seguridad = Teatro.getInstancia().getTipoSeguridad()
                        seguridad.append(newSeguridad)
                        Teatro.getInstancia().setTipoSeguridad(seguridad)
                        general = Teatro.getInstancia().getEmpleadosPorRendimiento()
                        general.append(newSeguridad)
                        Teatro.getInstancia().setEmpleadosPorRendimiento(general)
                    
                    cls.ventanaDialogo("se contrato a:" + valores[0], continuar)

            def continuar2():
                pass
            Anuncio.after(50, mostrarSaldo)
            
            
        # Encabezado
        Titulo = tk.Frame(cls.new_window, bg="white")
        Titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        TituloLabel = tk.Label(Titulo, text="Bienvenido a la gestion de empleados", font=("Calibri"))
        TituloLabel.pack(fill="both", expand=True)
        TituloLabel.bind("<Configure>", lambda e: cls.resize(Titulo, TituloLabel, 8, 50, False))

        # --- Partes del contenido --- #
        f1 = tk.Frame(cls.content, bg = "#ffb48a", highlightbackground="#5d2417", highlightthickness=10)
        f1.place(relx=0.02, rely = 0.15, relwidth = 0.95, relheight= 0.8)
        ask = tk.Frame(f1)
        ask.place(relx=0.1, rely = 0.1, relwidth= 0.8, relheight=0.3)
        Question = tk.Label(ask, text="¿Deseas empezar a correr la funcionalidad?", font=("Calibri", 25), bg="#ffb48a")
        Question.pack(fill="both", expand=True)
        # ask.bind("<Configure>", lambda e: )
        cls.resize(ask, Question, 8, 45, False)
        button_yes = tk.Button(f1, bg = "#571F1C", text = "Si", fg="White", font=("Calibri", 16), command= run)
        button_yes.place(relx = 0.5, rely=0.6, relwidth=0.3, relheight=0.1, anchor="center")

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

        actorsForRental = None
        historialEmpresa = None
        empresa = None
        fechaInicio = None
        fechaFin = None
        duration = None
        
        CALIFICACION_ALTA = 4

        def mostrarActores(fieldframe: FieldFrame, topFrame: Frame):
            global actorsForRental
            global duration
            global empresa
            global fechaInicio
            global fechaFin

            fieldframe.gatherEntries()

            presupuesto = fieldframe.getValue("Presupuesto")
            try:
                presupuesto = float(presupuesto)
            except Exception:
                messagebox.showerror("Error", "La entrada debe ser numérica")
                return
            
            actorsForRental = list(filter(lambda actor: actor.getPrecioContrato(duration) <= presupuesto, actorsForRental))

            actors = [(actor.getNombre(), actor.getId(), actor.getEdad(), actor.getCalificacion(), actor.getPrecioContrato(duration))
                        for actor in actorsForRental]

            if len(actorsForRental) == 0:
                messagebox.showerror("Error", "No se hallaron actores para el presupuesto")
                return
            else:

                columns = ("Nombre", "Id", "Edad", "Calificación", "Precio de contratación")
                widths = (60, 10, 10, 10, 60)
                tree = ttk.Treeview(topFrame,
                                    columns= columns,
                                    show= "headings")
                for col, width in zip(columns, widths):
                    tree.heading(col, text=col)
                    tree.column(column = col, width = width)
                scrollbar = ttk.Scrollbar(topFrame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)

                for actor in actors:
                    tree.insert('', tk.END, values=actor)

                tree.place(relheight=1, relwidth= .98, relx= 0)
                scrollbar.place(relheight=1, relwidth=.02, relx= .98)

                def actorEscogido(event):

                    if cls.filterDebug:
                        print(fechaInicio, fechaFin)

                    actorEscogido, id, edad, calificacion, precio = tree.item(tree.selection()[0])["values"]

                    contratar = messagebox.askyesno("Contratación de actores", 
                                        f"Actor seleccionado:\n\nNombre: {actorEscogido}\nEdad: {edad}\nCalificación: {calificacion}\nPrecio de contratación: {precio}\n\n¿Desea contratarlo?")
                    if contratar:
                        actor = Artista.buscarArtistaPorId(id)
                        empresa.pagarContratoActor(actor, float(precio))

                        actor.getHorario().append((fechaInicio, fechaFin))


                        if cls.filterDebug:
                            print("horario nuevo", actor.getHorario())

                        messagebox.showinfo("Success", f"¡Actor contratado!\n\nEl actor escogido fue {actorEscogido} por un precio de {precio}")
                        Main.contratarActores()
                
                tree.bind('<<TreeviewSelect>>', actorEscogido)

        def presupuesto(topFrame: Frame):
            global actorsForRental
            global duration

            minActorPrecio = min(actorsForRental, key= lambda actor: actor.getPrecioContrato(duration)).getPrecioContrato(duration)
            maxActorPrecio = max(actorsForRental, key= lambda actor: actor.getPrecioContrato(duration)).getPrecioContrato(duration)

            messagebox.showinfo("Información", "Antes de elegir el presupuesto de contratación, tenga en cuenta que el rango de los precios es de " + str(minActorPrecio) + " a " + str(maxActorPrecio))

            presupuesto = FieldFrame(
                topFrame,
                tituloCriterios= "Precio de contratación",
                tituloValores= "Respuesta",
                criterios= ["Presupuesto"],
                valores= [""],
                command= lambda: mostrarActores(presupuesto, topFrame)
            )

            presupuesto.place(relheight= 1, relwidth= 1)


        def preseleccion(topFrame: Frame, avanzado = False):
            global actorsForRental
            global historialEmpresa

            if cls.filterDebug:
                print("historial de la empresa", [actor.getNombre() for actor in historialEmpresa])
            
            if len(actorsForRental) == 0:
                messagebox.showerror("Error", "No hay artistas disponibles con los requerimientos pedidos.")
            else:
                if not avanzado:
                    messagebox.showinfo("Success", str(len(actorsForRental)) + " actor/es encontrado/s durante la preselección")
                
                actorsForRental.sort(key=lambda actor: actor not in historialEmpresa)

                if cls.filterDebug:
                    print("lista reordenada", [actor.getNombre() for actor in actorsForRental])

                presupuesto(topFrame)


        def filtradoAvanzado(fieldframe: FieldFrame, topFrame: Frame):
            global actorsForRental

            fieldframe.gatherEntries()

            contadores = [[actor, 0] for actor in actorsForRental]

            edad = fieldframe.getValue("Intervalo de edad")

            if edad == "Infantil":
                interv = (0, 15)
            elif edad == "Juvenil":
                interv = (16, 24)
            elif edad == "Adulto":
                interv = (25, 70)
            else:
                interv = (71, float("inf"))

            actorsForRental = list(filter(lambda actor: actor.getEdad() >= interv[0] and actor.getEdad() < interv[1], actorsForRental))

            if cls.filterDebug:
                print("filtrados por edad", [actor.getNombre() for actor in actorsForRental])

            for contador in contadores:
                if contador[0] in actorsForRental:
                    contador[1] += 1
            
            sexo = fieldframe.getValue("Sexo")

            actorsForRental = list(filter(lambda actor: actor.getSexo() == sexo, actorsForRental))

            if cls.filterDebug:
                print("filtrados por sexo", [actor.getNombre() for actor in actorsForRental])

            contadores = list(filter(lambda contador: contador[1] > 0, contadores))

            if len(contadores) == 0:
                messagebox.showerror("Error", "No se encontraron actores que se ajusten bien a las características")
                return
            else:
                messagebox.showinfo("Success", str(len(contadores)) + " actor/es se ajustaron a una o más características avanzadas.")
                contadorActores = [tupla[0] for tupla in contadores]

                if cls.filterDebug:
                    print("actores que aparecen al menos una vez en el contador", [actor.getNombre() for actor in contadorActores])

                actorsForRental = contadorActores
                preseleccion(topFrame, avanzado= True)


        def busquedaAvanzada(topFrame: Frame):
            global actorsForRental

            edad = FieldFrame(
                topFrame,
                tituloCriterios= "Búsqueda avanzada",
                tituloValores= "Respuestas",
                criterios= ["Intervalo de edad", "Sexo"],
                valores = [["Infantil", "Juvenil", "Adulto", "Adulto mayor"], 
                            ["Masculino", "Femenino"]],
                combobox= True,
                command= lambda: filtradoAvanzado(edad, topFrame)
            )

            edad.place(relheight= 1, relwidth= 1)

        def setSchedule(fieldframe: FieldFrame, fecha: str, topFrame: str):
            global actorsForRental
            global duration
            global fechaInicio
            global fechaFin

            if cls.filterDebug:
                print("al entrar a setSchedule", [actor.getNombre() for actor in actorsForRental])

            fieldframe.gatherEntries()
            
            horaInicio = fieldframe.values[1].get()
            horaFin = fieldframe.values[2].get()
            
            try:
                horaInicio = datetime.strptime(horaInicio, "%H:%M").time()
                horaFin = datetime.strptime(horaFin, "%H:%M").time()
            except Exception:
                messagebox.showerror("Error", "Los horarios deben estar en formato 24 horas")
                return

            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

            fechaInicio = datetime.combine(fecha, horaInicio)
            fechaFin = datetime.combine(fecha, horaFin)

            horaMin =  datetime.combine(fecha, time(8, 0, 0))
            horaMax = datetime.combine(fecha, time(22, 0, 0))
            duracionMinHoras = 4
            duracionMaxHoras = 8

            advertenciaHorario = "Existe una incompatibilidad del horario con el lineamiento.\n\nRevise si:\n1. El inicio del horario ocurre antes del fin del horario.\n2. Se exceden los límites de horario (muy temprano o muy tarde).\nIntente de nuevo."
            advertenciaDuracion = "La duración del horario escogido es incompatible con los lineamientos\n(entre 4 y 8 horas)"

            if (fechaInicio < horaMin) or (fechaFin > horaMax) or (fechaFin < fechaInicio) or (fechaInicio > fechaFin):
                messagebox.showerror("Error", advertenciaHorario)
                return
            
            duration = (fechaFin - fechaInicio).total_seconds() / 3600

            if (duration < duracionMinHoras) or (duration > duracionMaxHoras):
                messagebox.showerror("Error", advertenciaDuracion)
                return
            
            actorsForRental = list(filter(lambda actor: actor.isDisponible(fechaInicio, fechaFin), actorsForRental))
            
            if cls.filterDebug:
                print("al salir de setSchedule", [actor.getNombre() for actor in actorsForRental])

            msgAvanzado = messagebox.askyesno("Contratación de Actores", "¿Desea hacer búsqueda avanzada?")

            if msgAvanzado:
                busquedaAvanzada(topFrame)
            else:
                preseleccion(topFrame)


        def askSchedule(fecha: str, topFrame: Frame):
            global actorsForRental

            actorsForRental = actorsForRental
            
            schedule = FieldFrame(
                topFrame,
                criterios = ["Hora de inicio", "Hora de fin"],
                tituloCriterios = "Horario de actor",
                tituloValores = "Respuesta",
                valores = ["", ""],
                command= lambda: setSchedule(schedule, fecha, topFrame)
            )

            schedule.place(relheight= 1, relwidth= 1)

            if cls.filterDebug:
                print("al terminar askSchedule", [actor.getNombre() for actor in actorsForRental])


        def filtrado(fieldframe: FieldFrame):
            global actorsForRental

            responses = [entry.get() for i, entry in enumerate(fieldframe.values) if i > 0]
            
            rol, genero, aptitud, fecha = responses

            if rol == "Rol principal":
                actorsForRental = list(filter(lambda actor: actor.getCalificacion() >= CALIFICACION_ALTA, actorsForRental))
            else:
                actorsForRental = list(filter(lambda actor: actor.getCalificacion() < CALIFICACION_ALTA, actorsForRental))

            for apt in Aptitud:
                if apt.name == aptitud.upper():
                    actorsForRental = list(filter(lambda actor: actor.getCalificacionPorAptitud(apt) >= CALIFICACION_ALTA, actorsForRental))
                    break
            
            for gen in Genero:
                if gen.name == genero.upper():
                    actorsForRental = list(filter(lambda actor: gen in actor.getGeneros(), actorsForRental))
                    break            

            if cls.filterDebug:
                print("al acabar filtrado",[actor.getNombre() for actor in actorsForRental])

            askSchedule(fecha, centerFrame)      



        def initPrimeraRonda(topframe: Frame):
            global actorsForRental

            actorsForRental = Teatro.getInstancia().getActores().copy()
            actorsForRental = list(filter(lambda actor: not actor.isReevaluacion(), actorsForRental))

            primeraRonda = FieldFrame(
                topframe,
                criterios= ["Tipo de papel", 
                            "Tipo de Obra",
                            "Aptitud principal",
                            "Día de contratación"],

                tituloCriterios = "Características del actor",
                tituloValores = "Respuestas",

                valores = [
                            ["Rol principal", "Rol secundario"], 
                           
                            [genero.name.title() for genero in Genero],

                            [aptitud.name.title() for aptitud in Aptitud],
                             
                            [day for day in Main.getWeek()]],

                command= lambda: filtrado(primeraRonda),
                combobox= True
            )

            primeraRonda.place(relwidth= 1, relheight= 1)





        def parseInt(fieldframe : FieldFrame, value: str) -> int | None:
            fieldframe.gatherEntries()
            ans = fieldframe.getValue(value)

            try:
                ans = int(ans)
                return ans
            except Exception:
                messagebox.showerror("Error", "La entrada no puede convertirse a entero")
                return None
            
        def idExists(id: int) -> Cliente | bool:
            for cliente in Teatro.getInstancia().getClientes():
                if cliente.getId() == id and cliente.getTipo() == "Empresa":
                    return cliente
            return False
        
        def createId(fieldframe: FieldFrame):
            global empresa
            global historialEmpresa

            fieldframe.gatherEntries()

            id = parseInt(fieldframe, "Generar nuevo ID")

            if id is None: 
                return

            cliente = idExists(id)

            if not cliente:
                empresa = Cliente(id= id, tipo = "Empresa")
                historialEmpresa = empresa.getHistorial()
                messagebox.showinfo("Success", "Cliente nuevo agregado a la base de datos")
                initPrimeraRonda(centerFrame)

            else:
                messagebox.showerror("Error", "La identificación ya existe, intente con un número diferente")

        def locateId(fieldframe: FieldFrame):
            global empresa
            global historialEmpresa

            fieldframe.gatherEntries()

            id = parseInt(fieldframe, "Inserte ID existente")

            if id is None:
                return
            
            cliente = idExists(id)
            
            if cliente:
                messagebox.showinfo("Success", "Cliente confirmado en base de datos")
                historialEmpresa = cliente.getHistorial()
                empresa = cliente
                initPrimeraRonda(centerFrame)
            else:
                messagebox.showerror("Error", "El número de identificación no existe en la base de datos de empresa.\nRevise si el cliente es de tipo Empresa o si se digitó correctamente.")

        def definirTipoEmpresa(fieldframe: FieldFrame, topFrame: Frame) -> None:
            fieldframe.gatherEntries()

            choice = fieldframe.getValue("Tipo de Empresa")
            if choice in ["Empresa registrada", "Empresa nueva"]:
                tk.Label(topFrame, text= "Opción escogida: " + choice).pack()
                
                if choice == "Empresa registrada":
                    idFrame = FieldFrame(topFrame, 
                                    criterios= ["Inserte ID existente"], 
                                    tituloCriterios= "", 
                                    tituloValores= "", 
                                    valores = [""],
                                    command= lambda: locateId(idFrame))
                    idFrame.place(relwidth= 1, relheight= 1)
                    
                elif choice == "Empresa nueva":
                    idFrame = FieldFrame(topFrame,
                                    criterios= ["Generar nuevo ID"], 
                                    tituloCriterios= "", 
                                    tituloValores= "", 
                                    valores = [""],
                                    command= lambda: createId(idFrame))
                    idFrame.place(relwidth= 1, relheight= 1)

            else:
                ##MANEJO DE EXCEPCION
                messagebox.showerror("Error", "Opción Inválida")

        pregunta1 = FieldFrame(root = centerFrame, 
                                criterios = criteriosTipoEmpresa,
                                valores = valoresTipoEmpresa,
                                combobox= True,
                                command= lambda: definirTipoEmpresa(pregunta1, centerFrame))

        pregunta1.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)


    @classmethod
    def gestionObras(cls):
        pass
        

    @classmethod
    def gestionClases(cls):
        for widget in cls.content.winfo_children():
            widget.destroy()

        # --- FRAME DE BIENVENIDA ---
        frame_bienvenida = Frame(cls.content, bg="red")
        frame_bienvenida.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        saludo = tk.Label(frame_bienvenida,
                            text="Gestion de clases",
                            font=("Calibri", 16),
                            bg="black", fg="white")
        saludo.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame_bienvenida.bind("<Configure>", lambda e: cls.resize(frame_bienvenida, saludo))

        # --- FRAME PRINCIPAL PARA EL PROCESO ---
        process_frame = Frame(cls.content, bg="white")
        process_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        # -------------------- PASO 1: Mostrar Artistas y solicitar ID -------------------- 
        '''AVALADA'''
        def step1():
            for widget in process_frame.winfo_children():
                widget.destroy()

            artistas = Teatro.getInstancia().getArtistas()
            if artistas:
                lbl_artistas = tk.Label(process_frame, text="Artistas existentes en la base de datos:",
                                        font=("Calibri", 14), bg="white")
                lbl_artistas.pack(pady=10)
                txt_artistas = tk.Text(process_frame, height=10, width=80, font=("Calibri", 12))
                txt_artistas.pack(pady=10)
                for artista in artistas:
                    # Diferenciamos actores y directores: suponemos que si el artista tiene atributo "edad" es Actor.
                    if isinstance(artista, Actor):
                        linea = f"- Actor {artista.getNombre()} con ID {artista.getId()}\n"
                    else:
                        linea = f"- Director {artista.getNombre()} con ID {artista.getId()}\n"
                    txt_artistas.insert("end", linea)
                txt_artistas.config(state="disabled")
            else:
                tk.Label(process_frame, text="No hay artistas en la base de datos.",
                        font=("Calibri", 14), bg="white").pack(pady=10)

            lbl_id = tk.Label(process_frame, text="Ingrese el ID del artista para gestionar clases:",
                                font=("Calibri", 14), bg="white")
            lbl_id.pack(pady=10)
            entry_id = tk.Entry(process_frame, font=("Calibri", 14))
            entry_id.pack(pady=5)
            btn_buscar = tk.Button(process_frame, text="Buscar", font=("Calibri", 14),
                                    command=lambda: process_artist(entry_id.get()))
            btn_buscar.pack(pady=10)

        # -------------------- PASO 2: Procesar el ID ingresado --------------------
        '''AVALADA'''
        def process_artist(id_str):
            try:
                id_num = int(id_str)
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")
                return
            artista = Artista.buscarArtistaPorId(id_num)
            if artista is None:
                step_artist_not_found(id_num)
            else:
                step_artist_found(artista)

        # -------------------- PASO 3: Artista no encontrado --------------------
        '''AVALADA'''
        def step_artist_not_found(id_num):
            for widget in process_frame.winfo_children():
                widget.destroy()
            tk.Label(process_frame, text=f"Artista con ID {id_num} no encontrado.",
                        font=("Calibri", 14), bg="white", fg="red").pack(pady=10)
            tk.Label(process_frame, text="¿Desea crear un nuevo Artista con este ID?",
                        font=("Calibri", 14), bg="white").pack(pady=10)
            tk.Button(process_frame, text="Sí", font=("Calibri", 14),
                        command=lambda: step_create_artist(id_num)).pack(pady=5)
            tk.Button(process_frame, text="No", font=("Calibri", 14),
                        command=lambda: step_show_obras_criticas_and_fin()).pack(pady=5)

        # -------------------- MÉTODO REQUERIDO: Obras críticas y terminar -------------------- 
        '''AVALADA'''
        def step_show_obras_criticas_and_fin():
            # Limpia el frame donde se mostrará la información
            for widget in process_frame.winfo_children():
                widget.destroy()
            
            # Se llama al método de clase que retorna la lista de obras críticas.
            # Asegúrate de que Obra.mostrarObrasCriticas() esté decorado con @classmethod y retorne una lista.
            obras_criticas = Obra.mostrarObrasCriticas()  
            if not obras_criticas:
                tk.Label(process_frame, text="No hay obras en estado crítico en el teatro.",
                        font=("Calibri", 20), bg="white", fg="yellow").pack(pady=10)
            else:
                tk.Label(process_frame, text="Obras en estado crítico del teatro:",
                        font=("Calibri", 14), bg="white", fg="red").pack(pady=10)
                txt_obras = tk.Text(process_frame, height=10, width=80, font=("Calibri", 12))
                txt_obras.pack(pady=10)
                # Itera sobre la lista de obras y agrega una línea para cada obra
                for obra in obras_criticas:
                    # Se asume que cada obra tiene métodos getNombre() y promedioCalificacion()
                    linea = f"- '{obra.getNombre()}' (Promedio: {obra.promedioCalificacion()})\n"
                    txt_obras.insert("end", linea)
                txt_obras.config(state="disabled")
            
            # Puedes agregar un botón para continuar o regresar al menú principal
            tk.Label(process_frame, text="Fin de la funcionalidad",
                        font=("Calibri", 14), bg="white").pack(pady=10)
            tk.Button(process_frame, text="Salir del sistema", font=("Calibri", 14),
                    command=cls.volver).pack(pady=10)

        # -------------------- MÉTODO REQUERIDO: Obras críticas --------------------            
        def step_show_obras_criticas():
            # Limpia el frame donde se mostrará la información
            for widget in process_frame.winfo_children():
                widget.destroy()
            
            # Se llama al método de clase que retorna la lista de obras críticas.
            obras_criticas = Obra.mostrarObrasCriticas()  
            if not obras_criticas:
                tk.Label(process_frame, text="No hay obras en estado crítico en el teatro.",
                        font=("Calibri", 14), bg="white", fg="yellow").pack(pady=10)
            else:
                tk.Label(process_frame, text="Obras en estado crítico del teatro:",
                        font=("Calibri", 14), bg="white", fg="red").pack(pady=10)
                txt_obras = tk.Text(process_frame, height=10, width=80, font=("Calibri", 12))
                txt_obras.pack(pady=10)
                # Itera sobre la lista de obras y agrega una línea para cada obra
                for obra in obras_criticas:
                    # Se asume que cada obra tiene métodos getNombre() y promedioCalificacion()
                    linea = f"- '{obra.getNombre()}' (Promedio: {obra.promedioCalificacion()})\n"
                    txt_obras.insert("end", linea)
                txt_obras.config(state="disabled")

        # -------------------- PASO 4: Crear nuevo artista --------------------
        '''AVALADA'''
        def step_create_artist(id_num):
            for widget in process_frame.winfo_children():
                widget.destroy()
            # Configuramos los criterios y valores iniciales para ingresar el nombre y el tipo de artista
            criterios = ["Nombre", "Tipo de artista"]
            valores = ["", ""]  # valores vacíos inicialmente
            # Se crea el FieldFrame; al presionar "Guardar" se llamará a la función lambda
            # que invoca process_new_artist con los datos ingresados.
            ff = FieldFrame(process_frame,
                            tituloCriterios="Datos del nuevo artista",
                            criterios=criterios,
                            tituloValores="Ingrese valor",
                            valores=valores,
                            combobox=False,
                            command=lambda: (ff.gatherEntries(), process_new_artist(id_num, ff.valores[0], ff.valores[1])))
            ff.pack(pady=10, fill="both", expand=True)
            tk.Label(process_frame, text="(Si se ingresa 'actor' se pedirá la edad posteriormente)",
                    font=("Calibri", 12), bg="white").pack(pady=5)

        def process_new_artist(id_num, nombre, tipo):
            tipo = tipo.lower().strip()
            if tipo not in ["director", "actor"]:
                messagebox.showerror("Error", "Tipo de artista no válido. Debe ser 'director' o 'actor'.")
                return
            if tipo == "director":
                # Se crea el director mediante su constructor (se asume que internamente se añade a la lista de directores)
                # Ejemplo: Director(nombre, id_num)
                director = Director(nombre, id_num)
                messagebox.showinfo("Éxito", f"Nuevo director agregado: {nombre} con ID {id_num}.\nLos directores no reciben clases.")
                for widget in process_frame.winfo_children():
                    widget.destroy()
                tk.Label(process_frame, text="Fin de la funcionalidad",
                            font=("Calibri", 14), bg="white").pack(pady=10)
                tk.Button(process_frame, text="Salir del sistema", font=("Calibri", 14),
                        command=cls.volver).pack(pady=10)

            else:
                for widget in process_frame.winfo_children():
                    widget.destroy()
                tk.Label(process_frame, text="Ingrese la edad del nuevo actor (entre 4 y 80):",
                        font=("Calibri", 14), bg="white").pack(pady=10)
                entry_age = tk.Entry(process_frame, font=("Calibri", 14))
                entry_age.pack(pady=5)
                tk.Button(process_frame, text="Guardar", font=("Calibri", 14),
                            command=lambda: process_new_actor(id_num, nombre, entry_age.get())).pack(pady=10)

        def process_new_actor(id_num, nombre, age_str):
            try:
                edad = int(age_str)
            except ValueError:
                messagebox.showerror("Error", "La edad debe ser un número entero.")
                return
            if edad < 4 or edad > 80:
                messagebox.showerror("Error", "La edad debe estar entre 4 y 80 años.")
                return
            actor = Actor(nombre, id_num, edad)
            messagebox.showinfo("Éxito", f"Nuevo actor agregado: {nombre} con ID {id_num} y edad {edad}.")
            step_artist_found(actor)

        # -------------------- PASO 5: Artista encontrado --------------------
        '''Avalada'''
        def step_artist_found(artista):
            for widget in process_frame.winfo_children():
                widget.destroy()
            if isinstance(artista, Director):
                tk.Label(process_frame, text="El artista es un Director. Los directores no reciben clases.",
                        font=("Calibri", 14), bg="white", fg="yellow").pack(pady=10)
                tk.Button(process_frame, text="Finalizar", font=("Calibri", 14),
                        command=cls.volver).pack(pady=10)
            else:
                # Si el actor no tiene calificaciones, se inicializan
                if artista.sigueIgual():
                    resultado = Empleado.casting(artista, Teatro.getInstancia().getTipoProfesor())
                    if not resultado:
                        messagebox.showerror("Error", "No hay profesores disponibles para inicializar las calificaciones del actor.")
                    else:
                        messagebox.showinfo("Información", "Se han inicializado las calificaciones del actor.")
                if len(artista.getCalificacionesPublico()) == 0:
                    Artista.inicializarCalificacionesPublico(artista)
                # Mostrar información de calificaciones
                txt_info = tk.Text(process_frame, height=8, width=80, font=("Calibri", 12))
                txt_info.pack(pady=10)
                info_text = f"Calificaciones de calificadores: {artista.getCalificacionesAptitudes()}\n"
                info_text += f"Calificaciones del público: {artista.getCalificacionesPublico()}\n"
                txt_info.insert("end", info_text)
                txt_info.config(state="disabled")
                # Mostrar obras críticas
                tk.Label(process_frame, text="Obras en estado crítico del teatro:",
                        font=("Calibri", 14), bg="white", fg="red").pack(pady=10)
                obras = Obra.mostrarObrasCriticas()  # Se asume que este método existe
                if not obras:
                    tk.Label(process_frame, text="No hay obras en estado crítico.",
                            font=("Calibri", 14), bg="white", fg="yellow").pack(pady=5)
                else:
                    txt_obras = tk.Text(process_frame, height=6, width=80, font=("Calibri", 12))
                    txt_obras.pack(pady=5)
                    for obra in obras:
                        linea = f"- '{obra.nombre}' (Promedio: {obra.promedioCalificacion()})\n"
                        txt_obras.insert("end", linea)
                    txt_obras.config(state="disabled")
                tk.Button(process_frame, text="Programar clase", font=("Calibri", 14),
                            command=lambda: step_select_area(artista)).pack(pady=10)
                
                tk.Button(process_frame, text="Salir del sistema", font=("Calibri", 14),
                command=cls.volver).pack(pady=10)

        # -------------------- PASO 6: Seleccionar área de mejora --------------------
        '''AVALADA'''
        def step_select_area(actor):
            for widget in process_frame.winfo_children():
                widget.destroy()
            areas_recomendadas = actor.obtenerAreasDeMejora()
            if not areas_recomendadas:
                messagebox.showinfo("Información", "No hay áreas recomendadas para mejorar.")
                cls.volver()
                return
            txt_areas = tk.Text(process_frame, height=6, width=80, font=("Calibri", 12))
            txt_areas.pack(pady=10)
            txt_areas.insert("end", "Áreas recomendadas para mejorar del actor " + actor.getNombre() + ":\n")
            for i, area in enumerate(areas_recomendadas[:3]):
                cal = actor.getCalificacionPorAptitud(area)
                txt_areas.insert("end", f"{i+1}. {area} (Calificación: {cal})\n")
            txt_areas.config(state="disabled")
            tk.Label(process_frame, text="¿Desea programar una clase basada en las áreas recomendadas?",
                    font=("Calibri", 14), bg="white").pack(pady=10)
            tk.Button(process_frame, text="Sí", font=("Calibri", 14),
                    command=lambda: step_schedule_class(actor, areas_recomendadas[0])).pack(pady=5)
            tk.Button(process_frame, text="No", font=("Calibri", 14),
                    command=lambda: step_select_custom_area(actor)).pack(pady=5)

        # -------------------- PASO 7: Selección personalizada de área --------------------
        '''AVALADA'''
        def step_select_custom_area(actor):
            for widget in process_frame.winfo_children():
                widget.destroy()
            tk.Label(process_frame, text="Seleccione el área para programar la clase:",
                    font=("Calibri", 14), bg="white").pack(pady=10)
            areas = actor.getAptitudes()  # Lista de objetos Aptitud
            var_index = tk.IntVar(value=0)
            # Crear radiobuttons usando el índice
            for i, area in enumerate(areas):
                tk.Radiobutton(process_frame, text=str(area), variable=var_index,
                            value=i, font=("Calibri", 12), bg="white").pack(anchor="w", padx=20)
            tk.Button(process_frame, text="Siguiente", font=("Calibri", 14),
                    command=lambda: step_schedule_class(actor, areas[var_index.get()])).pack(pady=10)

        # -------------------- PASO 8: Programar la clase (solicitar horario) --------------------
        def step_schedule_class(actor, areaSeleccionada):
            for widget in process_frame.winfo_children():
                widget.destroy()
            # Determinar el nivel de clase basado en la calificación actual
            calificacionActual = actor.getCalificacionPorAptitud(areaSeleccionada)
            if calificacionActual < 3.0:
                nivelClase = "Introducción"
            elif calificacionActual < 4.0:
                nivelClase = "Profundización"
            else:
                nivelClase = "Perfeccionamiento"
            tk.Label(process_frame,
                    text=f"Área seleccionada: {areaSeleccionada}\nNivel de clase: {nivelClase}",
                    font=("Calibri", 14), bg="white").pack(pady=10)
            tk.Label(process_frame, text="Programe la clase (Formato: YYYY-MM-DD HH:MM)",
                    font=("Calibri", 14), bg="white").pack(pady=5)
            tk.Label(process_frame, text="Inicio:", font=("Calibri", 14), bg="white").pack(pady=5)
            entry_start = tk.Entry(process_frame, font=("Calibri", 14))
            entry_start.pack(pady=5)
            tk.Label(process_frame, text="Fin:", font=("Calibri", 14), bg="white").pack(pady=5)
            entry_end = tk.Entry(process_frame, font=("Calibri", 14))
            entry_end.pack(pady=5)
            tk.Button(process_frame, text="Programar", font=("Calibri", 14),
                        command=lambda: process_schedule(actor, areaSeleccionada, nivelClase,
                                                        entry_start.get(), entry_end.get())).pack(pady=10)

        # -------------------- PASO 9: Procesar horario y asignar sala y profesor --------------------
        def process_schedule(actor, areaSeleccionada, nivelClase, inicio_str, fin_str):
            from datetime import datetime
            try:
                inicio = datetime.strptime(inicio_str, "%Y-%m-%d %H:%M")
                fin = datetime.strptime(fin_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha/hora incorrecto.")
                return
            if fin <= inicio:
                messagebox.showerror("Error", "El fin debe ser después del inicio.")
                return
            duration = (fin - inicio).total_seconds() / 3600
            if duration < 2 or duration > 4:
                messagebox.showerror("Error", "La duración debe ser entre 2 y 4 horas.")
                return
            # Validación de horario: se asume que las clases deben programarse entre las 10 y las 22
            if not (10 <= inicio.hour < 22 and 10 < fin.hour <= 22):
                messagebox.showerror("Error", "Las clases deben programarse entre las 10:00 y las 22:00.")
                return
            # Buscar sala disponible (usando anadir_horario, que en este caso es el método con guion bajo)
            salaAsignada = None
            for sala in Teatro.getInstancia().getSalas():
                if sala.getAseado() and sala.isDisponible(inicio, fin):
                    salaAsignada = sala
                    break
            if salaAsignada is None:
                messagebox.showerror("Error", "No hay salas disponibles en el horario deseado o no están limpias.")
                return
            salaAsignada.anadir_horario([inicio, fin])
            # Selección de profesor especializado (simulación de disponibilidad)
            profesorAsignado = None
            import random
            profesores = Teatro.getInstancia().getTipoProfesor()
            random.shuffle(profesores)
            for empleado in profesores:
                # Se asume que podemos identificar a un profesor mediante isinstance o similar
                if hasattr(empleado, "tiene_especializacion") and empleado.tiene_especializacion(areaSeleccionada):
                    if random.random() > 0.5:
                        profesorAsignado = empleado
                        break
            if profesorAsignado is None:
                messagebox.showerror("Error", "No hay profesores disponibles con especialización en el área seleccionada.")
                return
            msg = f"Sala asignada: {salaAsignada.getNumeroSala()}\nProfesor asignado: {profesorAsignado.getNombre()}\n"
            messagebox.showinfo("Clase Programada", msg)
            step_payment(actor, areaSeleccionada, nivelClase, profesorAsignado)

        # -------------------- PASO 10: Procesar pago y evaluación --------------------
        def step_payment(actor, areaSeleccionada, nivelClase, profesorAsignado):
            for widget in process_frame.winfo_children():
                widget.destroy()
            if nivelClase == "Introducción":
                costoClase = 50000
            elif nivelClase == "Profundización":
                costoClase = 75000
            else:
                costoClase = 90000
            tk.Label(process_frame, text=f"El costo de la clase es: ${costoClase}",
                    font=("Calibri", 14), bg="white").pack(pady=10)
            tk.Button(process_frame, text="Procesar Pago", font=("Calibri", 14),
                        command=lambda: process_payment(actor, costoClase, areaSeleccionada,
                                                        profesorAsignado, nivelClase)).pack(pady=10)

        def process_payment(actor, costoClase, areaSeleccionada, profesorAsignado, nivelClase):
            if actor.getCuenta().retirar(costoClase):
                tesoreria = Teatro.getInstancia().getTesoreria()
                tesoreria.setTotal(tesoreria.getTotal() + costoClase)
                tesoreria.setDineroEnCaja(tesoreria.getDineroEnCaja() + costoClase)
                messagebox.showinfo("Pago", "Pago procesado exitosamente.")
                # Se asigna profesor evaluador (simulación)
                profesor_evaluador = None
                import random
                profesores = Teatro.getInstancia().getTipoProfesor()
                random.shuffle(profesores)
                for empleado in profesores:
                    if hasattr(empleado, "tiene_especializacion") and empleado.tiene_especializacion(areaSeleccionada):
                        if random.random() > 0.5:
                            profesor_evaluador = empleado
                            break
                if profesor_evaluador:
                    calificacion = round(random.random() * 5, 1)
                    messagebox.showinfo("Evaluación", f"El profesor {profesor_evaluador.getNombre()} calificó al actor con un: {calificacion}")
                    if calificacion == 5:
                        if Teatro.getInstancia().getTesoreria().getCuenta().transferencia(actor.getCuenta(), costoClase):
                            messagebox.showinfo("Reembolso", f"Calificación perfecta. Se ha reembolsado ${costoClase} al actor.")
                        else:
                            messagebox.showerror("Error", "Error al procesar el reembolso.")
                    if not actor.huboMejora(areaSeleccionada):
                        tk.Button(process_frame, text="Reprogramar clase por falta de mejora", font=("Calibri", 14),
                                command=lambda: step_reprogramar(actor, areaSeleccionada, profesor_evaluador, nivelClase)).pack(pady=10)
                    else:
                        messagebox.showinfo("Proceso Finalizado", "La clase se ha realizado exitosamente.")
                        puntos = 1 if nivelClase == "Introducción" else (2 if nivelClase == "Profundización" else 3)
                        profesorAsignado.agregar_puntos(puntos)
                        messagebox.showinfo("Puntos", f"El profesor {profesorAsignado.getNombre()} ha recibido {puntos} puntos positivos.")
                        cls.volver()
                else:
                    messagebox.showerror("Error", "No hay profesores disponibles para calificar la función.")
            else:
                messagebox.showerror("Error", "El actor cuenta con saldo insuficiente para pagar la clase.")

        # -------------------- PASO 11: Reprogramar clase en caso de falta de mejora --------------------
        def step_reprogramar(actor, areaSeleccionada, profesorEvaluador, nivelClase):
            for widget in process_frame.winfo_children():
                widget.destroy()
            tk.Label(process_frame, text="Reprogramar clase por falta de mejora",
                    font=("Calibri", 14), bg="white", fg="red").pack(pady=10)
            tk.Label(process_frame, text="Ingrese nuevo horario (debe ser posterior al anterior)",
                    font=("Calibri", 14), bg="white").pack(pady=10)
            tk.Label(process_frame, text="Nuevo Inicio (YYYY-MM-DD HH:MM):",
                    font=("Calibri", 14), bg="white").pack(pady=5)
            entry_start = tk.Entry(process_frame, font=("Calibri", 14))
            entry_start.pack(pady=5)
            tk.Label(process_frame, text="Nuevo Fin (YYYY-MM-DD HH:MM):",
                    font=("Calibri", 14), bg="white").pack(pady=5)
            entry_end = tk.Entry(process_frame, font=("Calibri", 14))
            entry_end.pack(pady=5)
            tk.Button(process_frame, text="Reprogramar", font=("Calibri", 14),
                    command=lambda: process_reprogramar(actor, areaSeleccionada, entry_start.get(), entry_end.get(), nivelClase, profesorEvaluador)).pack(pady=10)

        def process_reprogramar(actor, areaSeleccionada, inicio_str, fin_str, nivelClase, profesorEvaluador):
            from datetime import datetime
            try:
                inicio = datetime.strptime(inicio_str, "%Y-%m-%d %H:%M")
                fin = datetime.strptime(fin_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha/hora incorrecto.")
                return
            if fin <= inicio:
                messagebox.showerror("Error", "El fin debe ser después del inicio.")
                return
            salaAsignada = None
            for sala in Teatro.getInstancia().getSalas():
                if sala.getAseado() and sala.isDisponible(inicio, fin):
                    salaAsignada = sala
                    break
            if salaAsignada is None:
                messagebox.showerror("Error", "No hay salas disponibles en el nuevo horario deseado o no están limpias.")
                return
            salaAsignada.anadir_horario([inicio, fin])
            profesorAsignado = None
            import random
            profesores = Teatro.getInstancia().getTipoProfesor()
            random.shuffle(profesores)
            for empleado in profesores:
                if hasattr(empleado, "tiene_especializacion") and empleado.tiene_especializacion(areaSeleccionada):
                    if random.random() > 0.5:
                        profesorAsignado = empleado
                        break
            if profesorAsignado is None:
                messagebox.showerror("Error", "No hay profesores disponibles para la nueva clase en el área seleccionada.")
                return
            messagebox.showinfo("Clase Reprogramada",
                                f"Clase reprogramada con el profesor {profesorAsignado.getNombre()} en la sala {salaAsignada.getNumeroSala()}.")
            if actor.noHaMejoradoEnCuatroIntentos(areaSeleccionada):
                nuevaCalificacion = max(0, actor.getCalificacionPorAptitud(areaSeleccionada) - 1)
                actor.registrarCalificacion(areaSeleccionada, nuevaCalificacion)
                messagebox.showinfo("Reducción de Nivel", f"El nuevo nivel del área {areaSeleccionada} es: {nuevaCalificacion}")
            puntos = 1 if nivelClase == "Introducción" else (2 if nivelClase == "Profundización" else 3)
            profesorAsignado.agregar_puntos(puntos)
            messagebox.showinfo("Puntos", f"El profesor {profesorAsignado.getNombre()} ha recibido {puntos} puntos positivos.")
            cls.volver()

        # -------------------- Inicio del proceso: arranca por el Paso 1 --------------------
        step1()
'''
'''
        


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

    if Main.fieldTest:
        #datos de prueba para fieldframe
        criterios = ["Name", "Age", "Email", "Bitcoin", "Country", "Number"]
        valores = ["John Doe", "25", "john@example.com", "293090237hjkhjk2j", "Rhodesia", "892962"]
        root = Tk()
        window = FieldFrame(root, criterios= criterios, valores= valores, habilitado= ["Age", "Country"])
        window.pack()
        print(window.getValue("Age")) #25
        root.mainloop()
    
    else:
        Main.runApp()
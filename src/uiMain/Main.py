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
from baseDatos.memory import resetMemory

from gestorAplicacion.gestionVentas.Cliente import Cliente
from gestorAplicacion.gestionFinanciera.Empleado import Empleado
from gestorAplicacion.gestionFinanciera.CuentaBancaria import CuentaBancaria
from gestorAplicacion.gestionClases.Profesor import Profesor

from gestorAplicacion.gestionObras.Artista import Artista
from gestorAplicacion.gestionObras.Actor import Actor
from gestorAplicacion.gestionObras.Obra import Obra
from gestorAplicacion.gestionObras.Director import Director

from gestorAplicacion.herramientas.Aptitud import Aptitud
from gestorAplicacion.herramientas.Genero import Genero
from gestorAplicacion.herramientas.Suscripcion import Suscripcion
from gestorAplicacion.gestionVentas.Funcion import Funcion
from gestorAplicacion.gestionVentas.Sala import Sala
from gestorAplicacion.gestionVentas.Tiquete import Tiquete

from gestorAplicacion.herramientas.FieldFrame import FieldFrame

from excepciones.errorEntradaNula import errorEntradaNula
from excepciones.errorEntradaNoNumerica import errorEntradaNoNumerica
from excepciones.errorSuscripcion import errorSuscripcion
from excepciones.errorFormatoHorario import errorFormatoHorario
from excepciones.errorIdExiste import errorIdExiste
from excepciones.errorIdNoExiste import errorIdNoExiste


class Main:

    debug = True
    root = None
    fieldTest = False
    reset = True 
    filterDebug = False
    bg = "#701C1A"

    @classmethod
    def toCop(cls, value):
        return f"${value:,.2f}"

    @classmethod
    def wait(cls) -> None:
        """Genera un periodo de espera de 2 segundos si Main.debug es False"""
        if cls.debug:
            return 
        else:
            t.sleep(2)

    @classmethod
    def getWeek(cls) -> list:
        """Retorna una lista con los proximos 7 dias de la semana (incluyendo el actual)"""
        return [date.today() + timedelta(days= i) for i in range(7) ]

    @classmethod
    def update_font(cls, event, frame, text, tamano, reescalamiento, aplicar):
        """Actualiza el tamaño de la fuente del título al cambiar el tamaño de la ventana."""
        if not text.winfo_exists():
            return
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

     

    def resize_image(event, original_image, label):
        new_width = event.width
        new_height = event.height
        # Redimensionar la imagen original al tamaño actual del widget
        resized = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        new_image = ImageTk.PhotoImage(resized)
        label.config(image=new_image)
        label.image = new_image  # Guardar la referencia para evitar que se elimine la imagen

    # --- NUEVAS VARIABLES PARA PROGRAMADORES ---
    current_programador_index = -1

    programadores = [
        ("Programador 1:\nNombre: Francisco Jose Ceren Porto\n Edad: 17 \nID: 1023631713",
            ["src/media/Programadores/Frank/fran1.png", "src/media/Programadores/Frank/fran2.png", "src/media/Programadores/Frank/fran3.png", "src/media/Programadores/Frank/fran4.png"]),
        ("Programador 2:\nNombre: Danna Valeria Perez Niño\n Edad: 17 \nID: 1052839541",
            ["src/media/Programadores/Danna/Danna1 (9).png", "src/media/Programadores/Danna/Danna1 (5).png", "src/media/Programadores/Danna/Dannaa.png", "src/media/Programadores/Danna/Danna1 (10).png"]),
        ("Programador 3:\nNombre: Oscar David Arango Garcia\n Edad: 17 \nID: 1011591946",
            ["src/media/Programadores/Oscar/ImagenOscar1.png", "src/media/Programadores/Oscar/ImagenOscar2.png", "src/media/Programadores/Oscar/ImagenOscar3.png", "src/media/Programadores/Oscar/ImagenOscar4.png"]),
        ("Programador 4:\nNombre: Juan Pablo Miras Cañas\n Edad: 19 \nID: 1033178679",
            ["src/media/Programadores/Juan Pablo/pablo1.png", "src/media/Programadores/Juan Pablo/pablo2.png", "src/media/Programadores/Juan Pablo/pablo5.png", "src/media/Programadores/Juan Pablo/pablo4.png"]),
        ("Programador 5:\nNombre: Miguel Velez Bernal\n Edad: 18 \nID: 1023524572",
            ["src/media/Programadores/Velez/Velez1.png", "src/media/Programadores/Velez/Velez4.png", "src/media/Programadores/Velez/Velez3.png", "src/media/Programadores/Velez/Velez2.png"])
    ]

    imagenes = [
        "src/media/Teatro/foto1.jpg",
        "src/media/Teatro/foto2.jpg",
        "src/media/Teatro/foto3.png",
        "src/media/Teatro/foto4.jpeg",
        "src/media/Teatro/foto5.jpg"        
    ]

    indice_imagen = 0 
    img_actual_tamano = (0, 0)

    @classmethod
    def clear_frame(cls, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    @classmethod
    def initRoot(cls):
        """Inicializa la ventana raíz, le asigna un ícono, título y frame. Además, inicia la ventana principal"""
        cls.root = Tk() 
        ico = Image.open("src/media/Teatro/icon.png")
        logo = ImageTk.PhotoImage(ico)
        cls.root.wm_iconphoto(False, logo)
        cls.root.geometry("960x540") #16:9
        cls.root.title("Teatro Escuela Carlos Mayolo")

        cls.main_frame = Frame(cls.root)
        cls.main_frame.pack(fill="both", expand=True)

        cls.window_main() 

    @classmethod
    def exit(cls):
        """Serializa la instancia Teatro y cierra el programa"""
        Teatro.serializar()
        cls.root.destroy()

    @classmethod
    def window_main(cls):
        """Inicia la ventana principal, incluyendo los requerimientos del enunciado"""

        menuBar = tk.Menu(cls.root)
        cls.root.config(menu=menuBar)
        menuInicio = tk.Menu(menuBar, tearoff=False)
        menuBar.add_cascade(menu=menuInicio, label="Inicio")

        text_descripcion = "El programa está diseñado para manejar la logística de un teatro, en las que se simplifican tareas como, vender tiquetes , organizar las funciones a presentar , gestionar a los empleados y las clases de teatro, todo esto diseñado para que la interacción con el usuario sea lo más sencillo posible, ya que implementa diferentes herramientas gráficas como tablas o incluso la implementación de colores para que que sea más intuitivo el comportamiento del mismo programa"
        menuInicio.add_command( label="Salir", command = cls.exit)
        menuInicio.add_command( label="Descripcion",  command = lambda: cls.titleLabel.config(text = text_descripcion, font = ("Calibri", "12"))) 
        

        # CREACIÓN DEL RIGHT FRAME (usado para programadores)
        Main.rightFrame = Frame(cls.main_frame, borderwidth= 10, bg = Main.bg, width = 800, height = 900)
        Main.rightFrame.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)

        # FRAME IZQUIERDO (50% de la pantalla)
        cls.leftFrame = Frame(cls.main_frame, borderwidth=2, bg= Main.bg)
        cls.leftFrame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        # DIVIDIR EN 2 SECCIONES(FRAME IZQUIERDO): SUPERIOR E INFERIOR
        cls.topFrame = Frame(cls.leftFrame, bg="#701C1A")
        cls.topFrame.place(relx=0, rely=0, relwidth=1, relheight=0.5)

        cls.bottomFrame = Frame(cls.leftFrame, bg="black")
        cls.bottomFrame.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        # Crear Label para la imagen
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
            wraplength=800,
            bg= "#701C1A",
            fg = '#FCE6C9'
        )
        cls.titleLabel.place(relx=0.5, rely=0.5, anchor="center")
    
        # Vinculacion de eventos
        cls.label.bind("<Button-1>", lambda e: cls.abrir_nueva_ventana())
        cls.resize(cls.topFrame, cls.titleLabel)

        #En este método está todo lo relacionado a la sección de programadores
        cls.init_programador_functionality()

    @classmethod
    def init_programador_functionality(cls):
        """
        Inicializa la sección de programadores en el RightFrame.
        Se crean dos subframes:
            - programadorFrameTop: contiene un botón que muestra la info del programador.
            - programadorFrameBottom: muestra en formato 2x2 las imágenes asociadas.
        """
        cls.programadorFrameTop = tk.Frame(cls.rightFrame, bg="skyblue")
        cls.programadorFrameTop.place(relx=0, rely=0, relwidth=1, relheight=0.3)
        
        cls.programadorFrameBottom = tk.Frame(cls.rightFrame, bg="#FCE6C9")
        cls.programadorFrameBottom.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)
        
        cls.btn_info = tk.Button(cls.programadorFrameTop, text="Programadores", command=cls.update_programador, bg = "#701C1A", fg="#FCE6C9")
        cls.btn_info.pack(expand=True, fill="both")
        
        # Vincula el evento <Configure> del frame superior para redimensionar la fuente del botón
        cls.resize(cls.programadorFrameTop, cls.btn_info, tamano=18, reescalamiento=30, aplicar=True)
        
        # Vincula el evento <Configure> del frame inferior para actualizar las imágenes
        cls.programadorFrameBottom.bind("<Configure>", cls.resize_programador_images)


    @classmethod
    def update_programador(cls):
        """
        Actualiza la información y las imágenes del programador mostrado.
        """
        # Actualizar índice y obtener datos del siguiente programador
        cls.current_programador_index = (cls.current_programador_index + 1) % len(cls.programadores)
        info, image_paths = cls.programadores[cls.current_programador_index]
        cls.btn_info.config(text=info)
        
        # Limpiar el contenido previo del frame inferior
        for widget in cls.programadorFrameBottom.winfo_children():
            widget.destroy()
        
        # Guardar referencias para evitar que las imágenes se eliminen y para poder redimensionarlas
        cls.programadorFrameBottom.image_refs = []   # Referencias a las imágenes
        cls.programador_labels = []                    # Referencias a los labels de cada imagen
        cls.current_programador_image_paths = image_paths  # Guardamos las rutas originales
        
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
            cls.programador_labels.append(label)

    @classmethod
    def resize_programador_images(cls, event):
        # Si no se ha establecido la lista de rutas, salir sin hacer nada.
        if not hasattr(cls, "current_programador_image_paths") or not cls.current_programador_image_paths:
            return

        frame_width = cls.programadorFrameBottom.winfo_width()
        frame_height = cls.programadorFrameBottom.winfo_height()
        cell_width = frame_width // 2
        cell_height = frame_height // 2

        # Iterar sobre cada imagen y actualizar el label correspondiente
        for idx, img_path in enumerate(cls.current_programador_image_paths):
            try:
                pil_image = Image.open(img_path)
                pil_image = pil_image.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
                new_img = ImageTk.PhotoImage(pil_image)
            except Exception as e:
                print(f"Error redimensionando la imagen {img_path}: {e}")
                new_img = tk.PhotoImage(width=cell_width, height=cell_height)
            # Actualizar el label solo si existe
            if hasattr(cls, "programador_labels") and idx < len(cls.programador_labels) and cls.programador_labels[idx].winfo_exists():
                cls.programador_labels[idx].config(image=new_img)
            # Actualizar la referencia para evitar la recolección de basura
            if hasattr(cls.programadorFrameBottom, "image_refs") and idx < len(cls.programadorFrameBottom.image_refs):
                cls.programadorFrameBottom.image_refs[idx] = new_img



    @classmethod
    def abrir_nueva_ventana(cls):
        cls.root.destroy()

        cls.new_window = tk.Tk()
        ico = Image.open("src/media/Teatro/icon.png")
        logo = ImageTk.PhotoImage(ico)
        cls.new_window.wm_iconphoto(False, logo)
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
        cls.content = tk.Frame(cls.new_window, bg="#701C1A")
        cls.content.place(relx=0, rely=0, relwidth=1, relheight=1)
        cls.Label = tk.Label(cls.content, text="Bienvenido al Teatro Escuela Carlos Mayolo", font=("Calibri", 30), wraplength=500, bg= "#701C1A", fg = '#FCE6C9')
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
        mensaje = "El programa está diseñado para manejar la logística de un teatro, en las que se simplifican tareas como:\n-Vender tiquetes.\n-Organizar las funciones a presentar.\n-Gestionar a los empleados.\n-Gestionar las clases de teatro.\nTodo esto diseñado para que la interacción con el usuario sea lo más sencillo  y completo posible, ya que implementa diferentes herramientas gráficas como tablas o incluso la implementación de colores para que que sea más intuitivo el comportamiento del mismo programa"
        messagebox.showinfo("Aplicacion", mensaje)

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


    def validar_formatos(day_str: str, start_time_str: str, end_time_str: str):
        """
        Valida manualmente que las cadenas 'day_str', 'start_time_str' y 'end_time_str'
        estén en los formatos requeridos:
            - day_str: "YYYY-MM-DD"
            - start_time_str y end_time_str: "HH:MM"
            
        Retorna:
            tuple: (selected_date, start_time, end_time) como objetos date y time.
        
        Lanza:
            errorFormatoHorario: si alguno de los formatos no es correcto.
        """
        # Validar formato de fecha "YYYY-MM-DD"
        if len(day_str) != 10 or day_str[4] != '-' or day_str[7] != '-':
            raise errorFormatoHorario
        
        year_part = day_str[0:4]
        month_part = day_str[5:7]
        day_part = day_str[8:10]
        
        if not (year_part.isdigit() and month_part.isdigit() and day_part.isdigit()):
            raise errorFormatoHorario
        
        year = int(year_part)
        month = int(month_part)
        day = int(day_part)
        
        # Verificar que el mes sea válido (1 a 12)
        if month < 1 or month > 12:
            raise errorFormatoHorario
        
        # Días máximos permitidos por mes
        dias_por_mes = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        # Ajuste para años bisiestos en febrero
        if month == 2 and ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
            dias_max = 29
        else:
            dias_max = dias_por_mes[month]
        
        if day < 1 or day > dias_max:
            raise errorFormatoHorario
        
        # Función interna para validar el formato de hora "HH:MM"
        def validar_hora(time_str):
            if len(time_str) != 5 or time_str[2] != ':':
                raise errorFormatoHorario
            hours_str, minutes_str = time_str.split(':')
            if not (hours_str.isdigit() and minutes_str.isdigit()):
                raise errorFormatoHorario
            hours = int(hours_str)
            minutes = int(minutes_str)
            if hours < 0 or hours > 23:
                raise errorFormatoHorario
            if minutes < 0 or minutes > 59:
                raise errorFormatoHorario
            return hours, minutes

        # Validar y extraer horas y minutos para hora de inicio y fin
        start_hours, start_minutes = validar_hora(start_time_str)
        end_hours, end_minutes = validar_hora(end_time_str)
        
        # Convertir las partes a objetos date y time
        from datetime import date, time
        selected_date = date(year, month, day)
        start_time_obj = time(start_hours, start_minutes)
        end_time_obj = time(end_hours, end_minutes)
    
        return selected_date, start_time_obj, end_time_obj
    

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
        """Método padre que inicializa todo el programa"""
        Teatro.deserializar()

        if len(Teatro.getInstancia().getSalas())==0:
            sala1 = Sala(numero_sala=1,metros_cuadrados= 100,capacidad= 24)
            sala2 = Sala(numero_sala=2,metros_cuadrados= 200,capacidad= 32)
            sala3 = Sala(numero_sala=3,metros_cuadrados= 50,capacidad= 16)
            sala4 = Sala(numero_sala=4,metros_cuadrados= 150,capacidad= 24)
        
        if cls.reset:
            resetMemory()

        cls.initRoot()
        cls.root.mainloop()

    @classmethod
    def gestionVentas(cls):
        global tiquete

        tiquete = Tiquete()

        


        def Usuario_Nuevo():


                
            #SE CREARA UN NUEVO ID
            code = Cliente.id_random()

            global cliente
            cliente = Cliente(id = code)
            cliente.set_suscripcion(Suscripcion.BASICA)
            messagebox.showinfo("Éxito", f"Su nuevo ID es {cliente.getId()}")
            tiquete.setId(code)
            cliente.setTiquete(tiquete)
            Inicio_preguntas()
            
        
        def validar(texto):
                global cliente
                
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
                    cliente = Cliente.buscarPorId(numero)
                
                    tiquete.setId(numero)
                    cliente.setTiquete(tiquete)
                    messagebox.showinfo("Éxito", "Iniciando sesion")
                    Inicio_preguntas()
        def Usuario_Antiguo():
            

            for widget in cls.content.winfo_children():
                widget.destroy()
            global cliente
            
            
            
            
            f1 = tk.Frame(cls.content, bg = "#4B2D2E")
            f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

            frame_izq = tk.Frame(cls.content, bg="#5d2417")
            frame_izq.place(relx=0, rely=0, relwidth=0.175, relheight=0.9)
            # Frame derecho
            frame_der = tk.Frame(cls.content, bg="#5d2417")
            frame_der.place(relx=0.825, rely=0, relwidth=0.175, relheight=0.9)
            

            frame_central = tk.Frame(f1, bg="#701C1A",name="central")
            frame_central.place(relx=0.032, rely=0.05, relwidth=0.937, relheight=0.87)

            bottomFrame = tk.Frame(cls.content, bg="#5d2417")
            bottomFrame.place(relx=0, rely=0.9, relheight=0.2, relwidth=1)
            frame_2 = tk.Frame(frame_central, bg="slategray2", padx=15, pady=20)
            frame_2.place(relx=0.5, rely=0.85,anchor="center")
            
            frame = tk.Frame(frame_central, bg="slategray2", padx=20, pady=20)
            frame.place(relx=0.5, rely=0.5, anchor="center")

            top_frame = Frame(cls.content,background="black")
            top_frame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

            Titulo = tk.Frame(cls.content, bg="#070709")
            Titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)
            TituloLabel = tk.Label(Titulo, text="Bienvenido a la venta de tiquetes", font=("Calibri", 14), fg="#FCE6C9", bg="#070709")
            TituloLabel.pack(fill="both", expand=True)
            TituloLabel.bind("<Configure>", lambda e: cls.resize(Titulo, TituloLabel, 8, 50, False))

            '''IMAGEN BOTTOM (ASIENTOS)'''
            # Cargar la imagen original (asegúrate de que el archivo se encuentre en el mismo directorio)
            imagen_bottom = Image.open("src/media/Theme/bottom.png")  
            image = ImageTk.PhotoImage(imagen_bottom)

            # Crear un Label que contendrá la imagen y que cubra todo el bottomFrame
            bottom_label = tk.Label(bottomFrame, image=image)
            bottom_label.place(relheight=1, relwidth=1)

            # Vincular el evento <Configure> usando lambda para pasar la imagen y el label a la función
            bottomFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_bottom, bottom_label))
            '''IMAGEN RIGHT (CORTINA DER)'''
            imagen_right = Image.open("src/media/Theme/Courtain right.png")  
            image_der = ImageTk.PhotoImage(imagen_right)

            right_label = tk.Label(frame_der, image=image_der, bg="black")
            right_label.place(relheight=1, relwidth=1)

            frame_der.bind("<Configure>", lambda event: Main.resize_image(event, imagen_right, right_label))

            '''IMAGEN LEFT (CORTINA IZQ)'''

            imagen_left = Image.open("src/media/Theme/Courtain left.png")  
            image_izq = ImageTk.PhotoImage(imagen_left)

            left_label = tk.Label(frame_izq, image=image_izq, bg="black")
            left_label.place(relheight=1, relwidth=1)

            frame_izq.bind("<Configure>", lambda event: Main.resize_image(event, imagen_left, left_label))



            

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
            try:
                fieldframe.gatherEntries()
                suscripcion = fieldframe.getValue("ID")
                validar(suscripcion)
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return
            
            



            
        def Inicio_preguntas():
            global descuento
            descuento = 0
            descuento = 1-descuento
            for widget in cls.content.winfo_children():
                widget.destroy()
            global frame_central
            
            f1 = tk.Frame(cls.content, bg = "#4B2D2E")
            f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

            frame_izq = tk.Frame(cls.content, bg="#5d2417")
            frame_izq.place(relx=0, rely=0, relwidth=0.175, relheight=0.9)
            # Frame derecho
            frame_der = tk.Frame(cls.content, bg="#5d2417")
            frame_der.place(relx=0.825, rely=0, relwidth=0.175, relheight=0.9)
            

            frame_central = tk.Frame(f1, bg="#701C1A",name="central")
            frame_central.place(relx=0.032, rely=0.05, relwidth=0.937, relheight=0.87)

            bottomFrame = tk.Frame(cls.content, bg="#5d2417")
            bottomFrame.place(relx=0, rely=0.9, relheight=0.2, relwidth=1)
            
            Titulo = tk.Frame(cls.content, bg="#070709")
            Titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)
            TituloLabel = tk.Label(Titulo, text="Bienvenido a la venta de tiquetes", font=("Calibri", 14), fg="#FCE6C9", bg="#070709")
            TituloLabel.pack(fill="both", expand=True)
            TituloLabel.bind("<Configure>", lambda e: cls.resize(Titulo, TituloLabel, 8, 50, False))

            
            '''IMAGEN BOTTOM (ASIENTOS)'''
            # Cargar la imagen original (asegúrate de que el archivo se encuentre en el mismo directorio)
            imagen_bottom = Image.open("src/media/Theme/bottom.png")  
            image = ImageTk.PhotoImage(imagen_bottom)

            # Crear un Label que contendrá la imagen y que cubra todo el bottomFrame
            bottom_label = tk.Label(bottomFrame, image=image)
            bottom_label.place(relheight=1, relwidth=1)

            # Vincular el evento <Configure> usando lambda para pasar la imagen y el label a la función
            bottomFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_bottom, bottom_label))
            '''IMAGEN RIGHT (CORTINA DER)'''
            imagen_right = Image.open("src/media/Theme/Courtain right.png")  
            image_der = ImageTk.PhotoImage(imagen_right)

            right_label = tk.Label(frame_der, image=image_der, bg="black")
            right_label.place(relheight=1, relwidth=1)

            frame_der.bind("<Configure>", lambda event: Main.resize_image(event, imagen_right, right_label))

            '''IMAGEN LEFT (CORTINA IZQ)'''

            imagen_left = Image.open("src/media/Theme/Courtain left.png")  
            image_izq = ImageTk.PhotoImage(imagen_left)

            left_label = tk.Label(frame_izq, image=image_izq, bg="black")
            left_label.place(relheight=1, relwidth=1)

            frame_izq.bind("<Configure>", lambda event: Main.resize_image(event, imagen_left, left_label))

            label = tk.Label(cls.content,text="Desea mejorar su suscripcion?", font=("Calibri", 25), fg="#FCE6C9",bg="#701C1A",name="suscripcion")
            label.place(relx=0.5, rely=0.3, anchor="center")

            Button_Si = tk.Button(cls.content, text="Si", font=("Calibri", 15),command=adquirir_suscripcion,name="no")
            Button_No = tk.Button(cls.content, text="No", font=("Calibri", 15),command=continuar,name="si")
            
            Button_Si.place(relx=0.48, rely=0.5, anchor="center")
            Button_No.place(relx=0.53, rely=0.5, anchor="center")

            Main.wait()
        
        def adquirir_suscripcion():
            global descuento
            descuento = 0
            
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
                valores= [["BASICA","PREMIUM","VIP","ELITE"]],
                combobox= True,
                command=lambda :asignar_suscripcion(susc)
                
            )
            susc.place(relheight= 1, relwidth= 1)
            main_label = tk.Label(frame_central,fg="#FCE6C9",bg = "#701C1A",text="BÁSICA $0.00 -------\nPREMIUM \n$11,900.00\n 10% de Descuento\nEN TODAS LAS FUNCIONES\nY ASIENTOS\nVIP \n$18,900.00\n 25% de Descuento\nEN TODAS LAS FUNCIONES\nY ASIENTOS\nELITE \n$39,900.00 \nFUNCIONES GRATIS\nILIMITADAS Y\nASIENTO GOLD GRATIS")
            main_label.place(relx=0.53, rely=0.4, anchor="center")
            
        def asignar_suscripcion(fieldframe: FieldFrame):
            global cliente
            global descuento
            global precio_sus
            descuento = 0
            
            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return
            suscripcion = fieldframe.getValue("Eleccion")
            if suscripcion == "BASICA":
                cliente.set_suscripcion(Suscripcion.BASICA)
                precio_sus=0
                descuento = 0
            elif suscripcion == "VIP":
                cliente.set_suscripcion(Suscripcion.VIP)
                precio_sus=18900
                descuento = 0.25
            elif suscripcion == "PREMIUM":
                cliente.set_suscripcion(Suscripcion.PREMIUM)
                precio_sus=11900
                descuento = 0.10
            elif suscripcion == "ELITE":
                cliente.set_suscripcion(Suscripcion.ELITE)
                precio_sus=39900
                descuento = 1
            else:
                raise ValueError("Suscripción no válida")
            descuento = 1-descuento
            
            
            
            continuar()
        
   







        def continuar():
            
            try:
                widget = cls.content.nametowidget("suscripcion") 
                widget.destroy()

                widget = cls.content.nametowidget("central") 
                widget.destroy()
                
            except KeyError:
                None
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
                None
            f1 = tk.Frame(cls.content, bg = "#4B2D2E")
            f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

            

            frame_central = tk.Frame(f1, bg="#701C1A",name="central")
            frame_central.place(relx=0.032, rely=0.05, relwidth=0.937, relheight=0.87)

          
            lista=[]

            
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

            text_widget = tk.Text(frame_central, height=10, width=40,bg="#FCE6C9")  # Tamaño en líneas y columnas
            text_widget.place(relx=0.1,rely=0.3,relwidth=0.8, relheight=0.3)

            fila = f"{"Nombre":<20}{"Genero":<15}{"Duracion":<10}{"Precio":>10}\n"
            text_widget.insert(tk.END, fila)

            # Insertar texto inicial (opcional)
            
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
            def formatear_duracion(duracion):
                string = str(duracion)
                return string

            # Agregar datos al Treeview
            for obra in Teatro.getInstancia().getObras():
                if not obra.getNombre() =="NOTFORITE":
                    obra.setPrecio(obra.precioFuncion())
                    fila = f"{obra.getNombre():<20}{obra.getGenero().value:<15}{formatear_duracion(obra.getDuracion()):<10}{f'${obra.getPrecio():,.2f}':>10}\n"
                    text_widget.insert(tk.END, fila)
                    
                    
                    
                    tree.insert("", "end", values=(obra.getNombre(),obra.getGenero().value,obra.getDuracion(), f"${obra.getPrecio():,.2f}"))
                



        def asignar_obra(fieldframe :FieldFrame):
            global precio_sus
            
            
            

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return
            suscripcion = fieldframe.getValue("Eleccion")

            global cliente

            cliente.obra=suscripcion
            
            if suscripcion=="#!#!###":
                messagebox.showerror("Error", "seleccione una opcion")
            else:
                
                global frame_central

                f1 = tk.Frame(cls.content, bg = "#4B2D2E")
                f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

                frame_central = tk.Frame(f1, bg="#701C1A",name="central")
                frame_central.place(relx=0.032, rely=0.05, relwidth=0.937, relheight=0.87)

                lista=[]
                for funcion in Teatro.getInstancia().getFuncionesCreadas():
                    print(funcion.getObra().getNombre())
                    
                    if not funcion.getObra().getNombre() =="NOTFORITE" and funcion.getObra().getNombre() == suscripcion:
                        print(lista)

                        try:
                            lista.append(funcion.getHorario()[0].time())
                        except IndexError:
                            None

                
                if lista ==[]:
                    messagebox.showerror("Error", "No hay funciones Disponibles")
                    continuar()

                    
                
                func = FieldFrame(
                frame_central,
                tituloCriterios= "Obras",
                tituloValores= "Respuesta",
                criterios=["Eleccion"],
                valores= [lista],
                combobox= True,
                command=lambda :verificarSillas(func)
                
                )
                func.place(relheight= 1, relwidth= 1)


                tree = ttk.Treeview(frame_central, columns=("Fecha", "Horario"), show="headings",height=5)

                
                tree.heading("Fecha", text="Fecha")
                tree.heading("Horario", text="Horario")

                tree.column("Fecha", width=180)
                tree.column("Horario", width=100)

                scrollbar = ttk.Scrollbar(frame_central, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                
                text_widget = tk.Text(frame_central, height=10, width=40,bg="#FCE6C9")  # Tamaño en líneas y columnas
                text_widget.place(relx=0.1,rely=0.3,relwidth=0.8, relheight=0.3)
                fila = f"{"FECHA":<25}{"HORA":<10}\n"
                text_widget.insert(tk.END, fila)
                
                for funcion in Teatro.getInstancia().getFuncionesCreadas():
                    
                    if not funcion.getObra().getNombre() =="NOTFORITE" and funcion.getObra().getNombre() == suscripcion:
                        fecha = str(funcion.getHorario()[0].date())
                        hora = funcion.getHorario()[0].time().strftime("%H:%M:%S")
                        print(funcion.getHorario()[0])
                        
                        
                        fila = f"{fecha:<25}{hora:<10}\n"
                        text_widget.insert(tk.END, fila)
                        
                        tree.insert("", "end", values=(funcion.getHorario()[0].date(),funcion.getHorario()[0].time()))
                        lista.append(funcion.getObra().getNombre())
                
                def on_tree_select(event):
                    selected_item = tree.selection()  # Obtiene el ID del elemento seleccionado
                    if selected_item:
                        global item_values
                        
                        item_values = tree.item(selected_item, "values")  # Obtiene los valores de la fila
                        pregun = False
                        pregun = messagebox.askyesno("Eleccion",f"seleccionaste el horario {item_values[1]}")
                        if pregun :
                            
                            buscar_sillas(item_values[1])
                        
                

                tree.bind("<<TreeviewSelect>>", on_tree_select)
                        
        
        def verificarSillas (fieldframe : FieldFrame):
            
            try:
                fieldframe.gatherEntries()
                fecha = fieldframe.getValue("Eleccion")
                buscar_sillas(fecha)
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return         
        def buscar_sillas (fecha):


            
            global frame_central

            f1 = tk.Frame(cls.content, bg = "#4B2D2E")
            f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)                          
            frame_central = tk.Frame(f1, bg="#701C1A",name="central")
            frame_central.place(relx=0.032, rely=0.05, relwidth=0.937, relheight=0.87)


            frame_botones = tk.Frame((frame_central), bg="#701C1A")
            frame_botones.place(relx=0.1, rely=0.1, relwidth=0.80, relheight=0.60)

            escenario = tk.Label(frame_central, bg="slategray",text="ESCENARIO")
            escenario.place(relx=0.35, rely=0.8, relwidth=0.30, relheight=0.15)

            for funcion in Teatro.getInstancia().getFuncionesCreadas():
                
                if not funcion.getObra().getNombre() =="NOTFORITE" and str(funcion.getHorario()[0].time()) == fecha:
                    
                    precio_fun=funcion.getObra().getPrecio()
                    
                    
                    global sillas
                    global funcion_elegida
                    funcion_elegida = funcion
                    sillas = funcion.getSillas()
                    
            


            def boton_presionado(numero,l):
                pregun = messagebox.askyesno("Eleccion",f"seleccionaste las silla  {numero}")
                if pregun :
                    indi = 0
                    try :
                        
                        cliente.verificarSuscripcion(l[0])
                        for i in funcion_elegida.getSillas():
                        
                            if i.getCodigo()==numero:
                                funcion_elegida.getSillas()[indi].setCodigo("ocupado")

                                
                            indi += 1
                        imprimir_factura(numero)
                        
                        
                    except errorSuscripcion:
                        messagebox.showerror("Error", errorSuscripcion(l))

                    
                            
                    

            for fila in range((len(sillas) // 8) + 1):  
                frame_botones.grid_rowconfigure(fila, weight=0)  # Hace que las filas crezcan

            for columna in range(8):  
                frame_botones.grid_columnconfigure(columna, weight=1)  # Hace que las columnas crezcan

            for i in range(len(sillas)):
                fila = i // 8  # Calcula en qué fila va
                columna = i % 8  # Calcula en qué columna va
                if sillas[i].getCodigo() == "ocupado":
                    btn = tk.Button(frame_botones, text=f"{sillas[i].getCodigo()}", state=tk.DISABLED,height=1)
                    btn.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew", ipady=2)  # Agregar `sticky="nsew"`
                else:
                    cod = sillas[i].getCodigo()
                    btn = tk.Button(frame_botones, text=f"{sillas[i].getTipo().value[0:2]} {cod:04d}", 
                                    command=lambda i=i: boton_presionado(sillas[i].getCodigo(), sillas[i].getTipo().value),height=1)
                    btn.grid(row=fila, column=columna, padx=5, pady=5, sticky="nsew", ipady=2)  # Agregar `sticky="nsew"`

            def imprimir_factura(numero):
                
                global descuento

                
                
                global frame_central

                f1 = tk.Frame(cls.content, bg = "#4B2D2E")
                f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

                frame_central = tk.Frame(f1, bg="#701C1A",name="central")
                frame_central.place(relx=0.032, rely=0.05, relwidth=0.937, relheight=0.87)

                global precio_sus

                texto=Tiquete.imprimirFactura(cliente,su=precio_sus,p=precio_fun,d=descuento)
                texto = tk.Label(cls.content,text=texto,bg="#FCE6C9")
                texto.place(relx=0.3,rely=0.2,relheight=0.4,relwidth=0.4)

                fin = tk.Button(frame_central,text="Volver al menu",command=cls.gestionVentas)
                fin.place(relx=0.42,rely=0.9)
                
                Teatro.getInstancia().getTesoreria().setDineroEnCaja(Teatro.getInstancia().getTesoreria().getDineroEnCaja()+precio_fun+precio_sus)
                Teatro.getInstancia().getTesoreria().setTotal(Teatro.getInstancia().getTesoreria().getTotal()+precio_fun+precio_sus)
                


            
            




                

            """
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
"""


            



            
            




        for widget in cls.content.winfo_children():
            widget.destroy()
        
        f1 = tk.Frame(cls.content, bg = "#4B2D2E")
        f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

        frame_izq = tk.Frame(cls.content, bg="#5d2417")
        frame_izq.place(relx=0, rely=0, relwidth=0.175, relheight=0.9)
        # Frame derecho
        frame_der = tk.Frame(cls.content, bg="#5d2417")
        frame_der.place(relx=0.825, rely=0, relwidth=0.175, relheight=0.9)
        

        frame_central = tk.Frame(f1, bg="#701C1A",name="central")
        frame_central.place(relx=0.032, rely=0.05, relwidth=0.937, relheight=0.87)

        bottomFrame = tk.Frame(cls.content, bg="#5d2417")
        bottomFrame.place(relx=0, rely=0.9, relheight=0.2, relwidth=1)
        global precio_sus
        precio_sus=0

        
        
        '''IMAGEN BOTTOM (ASIENTOS)'''
        # Cargar la imagen original (asegúrate de que el archivo se encuentre en el mismo directorio)
        imagen_bottom = Image.open("src/media/Theme/bottom.png")  
        image = ImageTk.PhotoImage(imagen_bottom)

        # Crear un Label que contendrá la imagen y que cubra todo el bottomFrame
        bottom_label = tk.Label(bottomFrame, image=image)
        bottom_label.place(relheight=1, relwidth=1)

        # Vincular el evento <Configure> usando lambda para pasar la imagen y el label a la función
        bottomFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_bottom, bottom_label))
        '''IMAGEN RIGHT (CORTINA DER)'''
        imagen_right = Image.open("src/media/Theme/Courtain right.png")  
        image_der = ImageTk.PhotoImage(imagen_right)

        right_label = tk.Label(frame_der, image=image_der, bg="black")
        right_label.place(relheight=1, relwidth=1)

        frame_der.bind("<Configure>", lambda event: Main.resize_image(event, imagen_right, right_label))

        '''IMAGEN LEFT (CORTINA IZQ)'''

        imagen_left = Image.open("src/media/Theme/Courtain left.png")  
        image_izq = ImageTk.PhotoImage(imagen_left)

        left_label = tk.Label(frame_izq, image=image_izq, bg="black")
        left_label.place(relheight=1, relwidth=1)

        frame_izq.bind("<Configure>", lambda event: Main.resize_image(event, imagen_left, left_label))

        Titulo = tk.Frame(cls.content, bg="#070709")
        Titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        TituloLabel = tk.Label(Titulo, text="Bienvenido a la venta de tiquetes", font=("Calibri", 14), fg="#FCE6C9", bg="#070709")
        TituloLabel.pack(fill="both", expand=True)
        TituloLabel.bind("<Configure>", lambda e: cls.resize(Titulo, TituloLabel, 8, 50, False))



        """"top_label.bind(
            "<Configure>",
            lambda e: cls.resize(top_frame,top_label, 60, 100)
        )"""

        label = tk.Label(cls.content,text="Eres un cliente nuevo?", font=("Calibri", 25), fg="#FCE6C9",bg="#701C1A")
        label.place(relx=0.5, rely=0.3, anchor="center")

        Button_Si = tk.Button(cls.content, text="Si", font=("Calibri", 15),command=Usuario_Nuevo)
        Button_No = tk.Button(cls.content, text="No", font=("Calibri", 15),command=Usuario_Antiguo)
        Button_Si.place(relx=0.5, rely=0.5, anchor="center")
        Button_No.place(relx=0.5, rely=0.6, anchor="center")

        


        

    @classmethod
    def gestionEmpleados(cls):

        for widget in cls.content.winfo_children():
            widget.destroy()
        
        def run2():
            cls.clear_frame(f1)

            NOMBRES = ["Juan", "Pedro", "Maria", "Ana", "Luis", "Carlos", "Jose", "Andres", "Sofia", "Laura", "Miguel", "Danna", "Oscar", "Frank", "Pablo"]
            APELLIDOS = ["Gomez", "Perez", "Rodriguez", "Gonzalez", "Martinez", "Hernandez", "Lopez", "Torres", "Ramirez", "Diaz", "Sanchez", "Cruz", "Jimenez", "Rojas", "Vargas", "Velez"]
            
            def continuar():
                frameSuperior = tk.Frame(f1, bg="#701C1A")
                frameSuperior.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.85)
                frameInferior = tk.Frame(f1, bg="#701C1A")
                frameInferior.place(relx=0.02, rely=0.87, relheight= 0.1, relwidth=0.96)
                p1 = tk.Frame(frameSuperior, bg="#701C1A")
                p1.pack(side= "left", fill="both", expand= True, padx=5, pady=1)
                p2 = tk.Frame(frameSuperior, bg="#701C1A")
                p2.pack(side= "left", fill="both", expand= True, padx=5, pady=1)
                p3 = tk.Frame(frameSuperior, bg="#701C1A")
                p3.pack(side= "left", fill="both", expand= True, padx=5, pady=1)
                
                botonContinuar = tk.Button(frameInferior, text="Continuar", font=("Calibri", 14) ,bg="#AE1918", fg="white")
                botonContinuar.pack(fill="both", padx=10, pady=5)
                botonContinuar.config(command=lambda: continuar2())

                #Organizar las tablas de los empleados
                #Estilo tablas
                #Seguridad
                seguridad = tk.Label(p1, text="Seguridad", font=("Calibri", 18), bg="#701C1A", fg="white")
                seguridad.pack()
                cls.resize(p1, seguridad,10, 20,False)
                #Tabla Seguridad
                frame_tabla = tk.Frame(p1)
                frame_tabla.pack(expand=True, fill="both", padx=2, pady=5)

                #Encabezados
                encabezados = ["Nombre", "IDs"]
                for col, texto in enumerate(encabezados):
                    encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12), bg="#d3d3d3", padx=10, pady=1)
                    encabezado.grid(row=0, column=col, sticky="ew")
                
                #Fila de datos
                for fila, emp in enumerate(Teatro.getInstancia().getTipoSeguridad(), start=1):
                    nombre = tk.Label(frame_tabla, text=emp.getNombre(), padx=10, pady=1 )
                    nombre.grid(row=fila, column=0, sticky="ew")

                    id = tk.Label(frame_tabla, text=emp.getId(), padx=10, pady=1)
                    id.grid(row=fila, column=1, sticky="ew")
                
                #Ajustar columnas
                for col in range(2):
                    frame_tabla.grid_columnconfigure(col, weight=1)
                
                #Aseador
                Aseador = tk.Label(p2, text="Aseador", font=("Calibri", 18), bg="#701C1A", fg="white")
                Aseador.pack()
                cls.resize(p2, Aseador,10, 20,False)

                #Tabla Aseador
                frame_tabla = tk.Frame(p2)
                frame_tabla.pack(expand=True, fill="both", padx=2, pady=5)

                #Encabezados
                encabezados = ["Nombre", "IDs"]
                for col, texto in enumerate(encabezados):
                    encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12,), bg="#d3d3d3", padx=10, pady=1)
                    encabezado.grid(row=0, column=col, sticky="ew")
                
                #Fila de datos
                for fila, emp in enumerate(Teatro.getInstancia().getTipoAseador(), start=1):
                    nombre = tk.Label(frame_tabla, text=emp.getNombre(), padx=10, pady=1 )
                    nombre.grid(row=fila, column=0, sticky="ew")

                    id = tk.Label(frame_tabla, text=emp.getId(), padx=10, pady=1)
                    id.grid(row=fila, column=1, sticky="ew")
                
                #Ajustar columnas
                for col in range(2):
                    frame_tabla.grid_columnconfigure(col, weight=1)

                #Profesor
                Profesor = tk.Label(p3, text="Profesor", font=("Calibri", 18), bg="#701C1A", fg="white")
                Profesor.pack()
                cls.resize(p3, Profesor,10, 20,False)

                #Tabla Profesor
                frame_tabla = tk.Frame(p3)
                frame_tabla.pack(expand=True, fill="both", padx=2, pady=5)

                #Encabezados
                encabezados = ["Nombre", "IDs"]
                for col, texto in enumerate(encabezados):
                    encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12), bg="#d3d3d3", padx=10, pady=1)
                    encabezado.grid(row=0, column=col, sticky="ew")
                
                #Fila de datos
                for fila, emp in enumerate(Teatro.getInstancia().getTipoProfesor(), start=1):
                    nombre = tk.Label(frame_tabla, text=emp.getNombre(), padx=10, pady=1 )
                    nombre.grid(row=fila, column=0, sticky="ew")

                    id = tk.Label(frame_tabla, text=emp.getId(), padx=10, pady=1)
                    id.grid(row=fila, column=1, sticky="ew")
                
                #Ajustar columnas
                for col in range(2):
                    frame_tabla.grid_columnconfigure(col, weight=1)

                #Botones de acciones para cada tipo de empleado
                #Seguridad
                p12 = tk.Frame(p1, bg="#701C1A")
                p12.pack(side="bottom", fill="both", pady = 5, padx=5)
                contratarS = tk.Button(p12, bg= "#AE1918" ,text = "Contratar", font = ("calibri", 12), fg="White")
                contratarS.pack(side="left", expand=True, fill="x", pady= 5, padx=5, anchor="center")
                despedirS = tk.Button(p12, bg="#AE1918", text="Despedir", font=("calibri", 12), fg = "white")
                despedirS.pack(side="left", expand= True, fill= "x", pady=5, padx=5, anchor="center")

                #Aseador
                p22 = tk.Frame(p2, bg="#701C1A")
                p22.pack(side="bottom", fill="both", pady = 5, padx=5)
                contratarA = tk.Button(p22, bg= "#AE1918" ,text = "Contratar", font = ("calibri", 12), fg="White")
                contratarA.pack(side="left", expand=True, fill="x", pady= 5, padx=5, anchor="center")
                despedirA = tk.Button(p22, bg="#AE1918", text="Despedir", font=("calibri", 12), fg = "white")
                despedirA.pack(side="left", expand= True, fill= "x", pady=5, padx=5, anchor="center")

                #Profesor
                p32 = tk.Frame(p3, bg="#701C1A")
                p32.pack(side="bottom", fill="both", pady = 5, padx=5)
                contratarP = tk.Button(p32, bg= "#AE1918" ,text = "Contratar", font = ("calibri", 12), fg="White")
                contratarP.pack(side="left", expand=True, fill="x", pady= 5, padx=5, anchor="center")
                despedirP = tk.Button(p32, bg="#AE1918", text="Despedir", font=("calibri", 12), fg = "white")
                despedirP.pack(side="left", expand= True, fill= "x", pady=5, padx=5, anchor="center")


                #Modificar para los empleados de la lista
                def despedirEmpleado(tipo, listaOcupacion):
                    cls.clear_frame(f1)
                    p = tk.Frame(f1, bg="#701C1A")
                    p.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                    Empleado = tk.Label(p, text=tipo, font=("Calibri", 18), bg="#701C1A", fg="white")
                    Empleado.pack()
                    frame_tabla = tk.Frame(p)
                    frame_tabla.pack(expand=True, fill="both", padx=10, pady=5)
                        
                    #Encabezados
                    encabezados = ["Nombre", "IDs", "Despedir"]
                    for col, texto in enumerate(encabezados):
                        encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12), bg="#d3d3d3", padx=10, pady=1)
                        encabezado.grid(row=0, column=col, sticky="ew")
                    
                    #Fila de datos
                    for fila, emp in enumerate(listaOcupacion, start=1):
                        nombre = tk.Label(frame_tabla, text=emp.getNombre(), padx=10, pady=1 )
                        nombre.grid(row=fila, column=0, sticky="ew")

                        id = tk.Label(frame_tabla, text=emp.getId(), padx=10, pady=1)
                        id.grid(row=fila, column=1, sticky="ew")

                        despedir = tk.Button(frame_tabla, text="Despedir", command= lambda i = emp.getId(): Despedir(listaOcupacion, i))
                        despedir.grid(row=fila, column=2, padx= 10, pady=1)
                        
                    boton_volver = tk.Button(p,text="Volver", command=lambda: continuar(), bg="#AE1918", fg="white", font=("Calibri", 12))
                    boton_volver.pack(pady=2, padx=2, side="right")

                    #Ajustar columnas
                    for col in range(2):
                        frame_tabla.grid_columnconfigure(col, weight=1)
                        
                    def Despedir(listaOcupacion, id):
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
                                cls.ventanaDialogo(mensaje, continuar())
                                break
                    
                    
                despedirS.config(command=lambda: despedirEmpleado("Seguridad",Teatro.getInstancia().getTipoSeguridad()))
                despedirA.config(command=lambda: despedirEmpleado("Aseador",Teatro.getInstancia().getTipoAseador()))
                despedirP.config(command=lambda: despedirEmpleado("Profesor",Teatro.getInstancia().getTipoProfesor()))

                def contratarSeguridad():
                    cls.clear_frame(f1)
                    p = tk.Frame(f1, bg="#701C1A")
                    p.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                    seguridad = tk.Label(p, text="Candidatos a Seguridad", font=("Calibri", 14), bg="#701C1A", fg="white")
                    seguridad.pack(pady=5) 

                    candidatos = []

                    n = 0
                    while n<10:
                        nombre = random.choice(NOMBRES)
                        apellido = random.choice(APELLIDOS)
                        id = random.randint(100, 1000000)
                        Nombre = f"{nombre} {apellido}"
                        candidatos.append((Nombre, id))
                        n+=1
                    
                    frame_tabla = tk.Frame(p)
                    frame_tabla.pack(expand=True, fill="both", padx=10, pady=2)
                    
                    #Encabezados
                    encabezados = ["Nombre", "IDs", "Contratar"]
                    for col, texto in enumerate(encabezados):
                        encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12), bg="#d3d3d3", padx=10, pady=1)
                        encabezado.grid(row=0, column=col, sticky="ew")
                
                    #Fila de datos
                    for fila, (nombre, id) in enumerate(candidatos, start=1):
                        Nombre = tk.Label(frame_tabla, text=nombre, padx=10, pady=1 )
                        Nombre.grid(row=fila, column=0, sticky="ew")

                        ID = tk.Label(frame_tabla, text=id, padx=10, pady=1)
                        ID.grid(row=fila, column=1, sticky="ew")

                        contratar = tk.Button(frame_tabla, text="Contratar", command= lambda n=nombre, i=id: contrato(n, i, "Seguridad"))
                        contratar.grid(row=fila, column=2, padx= 10, pady=1)
                    
                    boton_volver = tk.Button(p,text="Volver", command=lambda: continuar(), bg="#AE1918", fg="white", font=("Calibri", 12))
                    boton_volver.pack(pady=2, padx=2, side="right")
                    
                    #Ajustar columnas
                    for col in range(2):
                        frame_tabla.grid_columnconfigure(col, weight=1)

                def contratarAseador():
                    cls.clear_frame(f1)
                    p = tk.Frame(f1, bg="#701C1A")
                    p.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                    Aseador = tk.Label(p, text="Candidatos a Aseador", font=("Calibri", 14),  bg="#701C1A", fg="white")
                    Aseador.pack(pady=5)
                    
                    candidatos = []

                    n = 0
                    while n<10:
                        nombre = random.choice(NOMBRES)
                        apellido = random.choice(APELLIDOS)
                        id = random.randint(100, 1000000)
                        Nombre = f"{nombre} {apellido}"
                        candidatos.append((Nombre, id))
                        n+=1
                    
                    frame_tabla = tk.Frame(p)
                    frame_tabla.pack(expand=True, fill="both", padx=10, pady=2)
                    
                    #Encabezados
                    encabezados = ["Nombre", "IDs", "Contratar"]
                    for col, texto in enumerate(encabezados):
                        encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12), bg="#d3d3d3", padx=10, pady=1)
                        encabezado.grid(row=0, column=col, sticky="ew")
                
                    #Fila de datos
                    for fila, (nombre, id) in enumerate(candidatos, start=1):
                        Nombre = tk.Label(frame_tabla, text=nombre, padx=10, pady=1 )
                        Nombre.grid(row=fila, column=0, sticky="ew")

                        ID = tk.Label(frame_tabla, text=id, padx=10, pady=1)
                        ID.grid(row=fila, column=1, sticky="ew")

                        contratar = tk.Button(frame_tabla, text="Contratar", command= lambda n=nombre, i=id: contrato(n, i, "Aseador"))
                        contratar.grid(row=fila, column=2, padx= 10, pady=1)

                    boton_volver = tk.Button(p,text="Volver", command=lambda: continuar(), bg="#AE1918", fg="white", font=("Calibri", 12))
                    boton_volver.pack(pady=2, padx=2, side="right")

                    #Ajustar columnas
                    for col in range(2):
                        frame_tabla.grid_columnconfigure(col, weight=1)

                def contratarProfesor():
                    cls.clear_frame(f1)
                    p = tk.Frame(f1, bg="#701C1A")
                    p.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                    Profesor = tk.Label(p, text="candidatos a Profesor", font=("Calibri", 14),  bg="#701C1A", fg="white")
                    Profesor.pack(pady=5)
                    
                    candidatos = []

                    n = 0
                    while n<10:
                        nombre = random.choice(NOMBRES)
                        apellido = random.choice(APELLIDOS)
                        id = random.randint(100, 1000000)
                        Nombre = f"{nombre} {apellido}"
                        candidatos.append((Nombre, id))
                        n+=1
                    
                    frame_tabla = tk.Frame(p)
                    frame_tabla.pack(expand=True, fill="both", padx=10, pady=2)
                    
                    #Encabezados
                    encabezados = ["Nombre", "IDs", "Contratar"]
                    for col, texto in enumerate(encabezados):
                        encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12), bg="#d3d3d3", padx=10, pady=1)
                        encabezado.grid(row=0, column=col, sticky="ew")
                
                    #Fila de datos
                    for fila, (nombre, id) in enumerate(candidatos, start=1):
                        Nombre = tk.Label(frame_tabla, text=nombre, padx=10, pady=1 )
                        Nombre.grid(row=fila, column=0, sticky="ew")

                        ID = tk.Label(frame_tabla, text=id, padx=10, pady=1)
                        ID.grid(row=fila, column=1, sticky="ew")

                        contratar = tk.Button(frame_tabla, text="Contratar", command= lambda n=nombre, i=id: contrato(n, i, "Profesor"))
                        contratar.grid(row=fila, column=2, padx= 10, pady=1)
                    
                    boton_volver = tk.Button(p,text="Volver", command=lambda: continuar(), bg="#AE1918", fg="white", font=("Calibri", 12))
                    boton_volver.pack(pady=2, padx=2, side="right")
                    
                    #Ajustar columnas
                    for col in range(2):
                        frame_tabla.grid_columnconfigure(col, weight=1)
                
                contratarS.config(command=lambda: contratarSeguridad())
                contratarA.config(command=lambda: contratarAseador())
                contratarP.config(command=lambda: contratarProfesor())

            def contrato(nombre, id, ocupacion):
                if ocupacion != "Seguridad":
                    if ocupacion != "Aseador":
                        newprofesor = Profesor(nombre, id)
                        profesores = Teatro.getInstancia().getTipoProfesor()
                        profesores.append(newprofesor)
                        Teatro.getInstancia().setTipoProfesor(profesores)
                        general = Teatro.getInstancia().getEmpleadosPorRendimiento()
                        general.append(newprofesor)
                        Teatro.getInstancia().setEmpleadosPorRendimiento(general)
                    else:
                        newAseador = Empleado(nombre, id, "Aseador")
                        Aseadores = Teatro.getInstancia().getTipoAseador()
                        Aseadores.append(newAseador)
                        Teatro.getInstancia().setTipoAseador(Aseadores)
                        general = Teatro.getInstancia().getEmpleadosPorRendimiento()
                        general.append(newAseador)
                        Teatro.getInstancia().setEmpleadosPorRendimiento(general)
                else:
                    newSeguridad = Empleado(nombre, id, "Seguridad")
                    seguridad = Teatro.getInstancia().getTipoSeguridad()
                    seguridad.append(newSeguridad)
                    Teatro.getInstancia().setTipoSeguridad(seguridad)
                    general = Teatro.getInstancia().getEmpleadosPorRendimiento()
                    general.append(newSeguridad)
                    Teatro.getInstancia().setEmpleadosPorRendimiento(general)
                    
                cls.ventanaDialogo("se contrato a:" + nombre, continuar())

            def continuar2():
                cls.clear_frame(f1)
                p = tk.Frame(f1, bg="#701C1A")
                p.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                #Tres frames
                # 1 Asignando Trabajadores
                infoTrabajadores = tk.Frame(p, bg="#701C1A")
                infoTrabajadores.place(relx=0, rely=0, relwidth=1, relheight=0.1, anchor="nw")
                info = tk.Label(infoTrabajadores, text="Asignando Trabajos, por favor espere...", font=("Calibri", 14), bg="#701C1A", fg="white")
                info.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                # 2 informacion de los de seguridad
                infoSeguridad = tk.Frame(p, bg="#701C1A")
                infoSeguridad.place(relx = 0, rely=0.1, relwidth=1, relheight=0.45, anchor="nw")
                info2 = tk.Frame(infoSeguridad, bg = "#4B2D2E")
                info2.place(relx=0, rely=0, relwidth=1, relheight=0.15)
                infoS = tk.Label(info2, text="Asignacion para Seguridad", font=("Calibri", 12), bg = "#4B2D2E", fg="white")
                infoS.place(relx=0.5, rely=0.5, anchor="center")

                # 3 informacion de los Aseadores
                infoAseador = tk.Frame(p, bg="#701C1A")
                infoAseador.place(relx=0, rely=0.55, relwidth=1, relheight=0.45, anchor="nw")
                info3 = tk.Frame(infoAseador, bg = "#4B2D2E")
                info3.place(relx=0, rely=0, relwidth=1, relheight=0.15)
                infoA = tk.Label(info3, text="Asignacion para Aseador", font=("Calibri", 12), bg = "#4B2D2E", fg="white")
                infoA.place(relx=0.5, rely=0.5, anchor="center")

                #ordenar listas
                
                aseador_order = Teatro.getInstancia().getTipoAseador()
                Seguridad_order = Teatro.getInstancia().getTipoSeguridad()
                Profesor_order = Teatro.getInstancia().getTipoProfesor()

                aseador_order.sort(key = lambda e: e.getMetaSemanal(), reverse=True)
                Seguridad_order.sort(key = lambda e: e.getMetaSemanal(), reverse=True)
                Profesor_order.sort(key = lambda e: e.getMetaSemanal(), reverse=True)

                Teatro.getInstancia().setTipoAseador(aseador_order)
                Teatro.getInstancia().setTipoSeguridad(Seguridad_order)
                Teatro.getInstancia().setTipoProfesor(Profesor_order)
                

                def asignarSeguridad():
                    #Asignacion de trabajos
                    trabajoAsignadoS = True                
                    cant_trabajadores_principiantes = 0
                    base = 6
                    totalFunciones = len(Teatro.getInstancia().getFuncionesCreadas())
                    totalTrabajadores_S = len(Teatro.getInstancia().getTipoSeguridad())
                    funcionXTrabajador = 0
                    if totalTrabajadores_S != 0:
                        funcionXTrabajador = totalFunciones/totalTrabajadores_S
                    funcionesDisponibles = list(Teatro.getInstancia().getFuncionesCreadas())
                    try:
                        funcionesDisponibles.sort(key=lambda f : f.getHorario()[0])
                    except Exception as e:
                        pass
                
                    #Verificacion de que las listas no este vacia
                    if funcionXTrabajador != 0:
                        for emp in Teatro.getInstancia().getTipoSeguridad():
                            if emp.getMetaSemanal() == base:
                                cant_trabajadores_principiantes += 1
                        #Asignacion cuando todos son principiantes
                        if cant_trabajadores_principiantes == len(Teatro.getInstancia().getTipoSeguridad()):
                            #Se asignan en igual cantidad
                            funcionesSinHorario = 0
                            for Persona in Teatro.getInstancia().getTipoSeguridad():
                                asignadas = 0
                                localTime = list(Persona.getHorario())
                                i = 0
                                while i < len(funcionesDisponibles): 
                                # for i in range(0, len(funcionesDisponibles)):
                                    if asignadas < funcionXTrabajador:
                                        Funciones = funcionesDisponibles[i]
                                        #asignacion del horario y del trabajo
                                        #Verificar que la funcion tenga un horario
                                        if Funciones.getHorario():
                                            if len(localTime) != 0:
                                                if Funciones.getHorario()[0] > localTime[-1][1]:
                                                    localTime.append(Funciones.getHorario())
                                                    asignadas += 1
                                                    #Calcular duracion de la Funcion
                                                    inicio = Funciones.getHorario()[0]
                                                    fin = Funciones.getHorario()[1]

                                                    duracionFuncion = (fin - inicio).total_seconds() / 3600.0
                                                    Persona.getTrabajos().append(duracionFuncion)
                                                    Funciones.setTrabajador(True)
                                                    funcionesDisponibles.pop(i)
                                                    continue
                                                else:
                                                    i += 1
                                            else:
                                                localTime.append(Funciones.getHorario())
                                                asignadas += 1

                                                inicio = Funciones.getHorario()[0]
                                                fin = Funciones.getHorario()[1]

                                                duracionFuncion = (fin - inicio).total_seconds() / 3600.0
                                                Persona.getTrabajos().append(duracionFuncion)
                                                Funciones.setTrabajador(True)
                                                funcionesDisponibles.pop(i)
                                                continue
                                        else:
                                            funcionesSinHorario += 1
                                            funcionesDisponibles.pop(i);
                                            continue
                                    else:
                                        break      
                                #Se organiza la lista para que no haya errores en caso de asignar las funciones restantes
                                localTime.sort(key = lambda horario: horario[0])
                                Persona.setHorario(localTime)
                                Persona.setDisponible(False)

                            if funcionesSinHorario == 1:
                                horarios = tk.Frame(infoSeguridad, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay una funcion sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                            elif funcionesSinHorario > 1:
                                horarios = tk.Frame(infoSeguridad, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay " + str(funcionesSinHorario) + " Funciones sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")

                            #Evaluacion de Salas sin trabajador
                            if funcionesDisponibles != 0:
                                for Persona in Teatro.getInstancia().getTipoSeguridad():
                                    localTime = list(Persona.getHorario())
                                    i = 0
                                    while i < len(funcionesDisponibles):
                                        Funciones = funcionesDisponibles[i]
                                        horarioValido = True
                                        inicioNuevo = Funciones.getHorario()[0]
                                        finNuevo = Funciones.getHorario()[1]
                                        #Verificar que no se solape
                                        #Se itera sobre las sublistas de localTime
                                        for j in range(len(localTime)):
                                            horarioActual = localTime[j]
                                            finActual = horarioActual[1]

                                            #Verificar que hay una sublista despues
                                            if j + 1 < len(localTime):
                                                horarioSiguiente = localTime[j+1]
                                                inicioSiguiente = horarioSiguiente[0]

                                                #Verificar que el horario nuevo no se solape
                                                if not (inicioNuevo > finActual and finNuevo < inicioSiguiente):
                                                            horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                                            
                                            else:
                                                #verificar que el inicio sea despues del horario ya existente
                                                if not(inicioNuevo > finActual):
                                                    horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                        if horarioValido:
                                            localTime.append(Funciones.getHorario())
                                            #Calcular Duracion
                                            inicio = Funciones.getHorario()[0]
                                            fin = Funciones.getHorario()[1]

                                            duracionFuncion = (fin - inicio).total_seconds() / 3600.0
                                            Persona.getTrabajos().append(duracionFuncion)
                                            Funciones.setTrabajodor(True)
                                            break
                                        else:
                                            i+=1
                                    localTime.sort(key = lambda horario: horario[0])
                                    Persona.setHorario(localTime)
                                    Persona.setDisponible(False)
                            #Se acaba la verificacion
                            #Imprimir mensajes
                            msg = ""
                            for Persona in Teatro.getInstancia().getTipoSeguridad():
                                if len(Persona.getHorario()) == 1:
                                    msg = msg + Persona.getNombre() + " Cuidará: 1 Funcion\n"
                                elif len(Persona.getHorario()) > 1 or len(Persona.getHorario()) == 0:
                                    msg = msg + Persona.getNombre() + " Cuidará: " + str(len(Persona.getHorario())) + " Funciones\n"
                            mensaje = tk.Label(infoSeguridad, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white")
                            mensaje.place(relx = 0.5, rely=0.5, relwidth= 0.8,relheight=0.7, anchor="center")
                        #No todos son principiantes
                        else:
                            try:
                                funcionPorDuracion = list(Teatro.getInstancia().getFuncionesCreadas())
                                funcionPorDuracion.sort(
                                    key = lambda f: (
                                        f.getHorario()[0],
                                        -(f.getHorario()[1] - f.getHorario[0]).total_seconds()
                                    )
                                )
                                funcionesDisponibles = funcionPorDuracion
                            except Exception as e:
                                pass

                            #Evaluacion Normal, trabajos equitativos
                            funcionesSinHorario = 0
                            for Persona in Teatro.getInstancia().getTipoSeguridad():
                                asignadas = 0
                                localTime = list(Persona.getHorario())
                                i = 0
                                while i < len(funcionesDisponibles): 
                                # for i in range(0, len(funcionesDisponibles)):
                                    if asignadas < funcionXTrabajador:
                                        Funciones = funcionesDisponibles[i]
                                        #asignacion del horario y del trabajo
                                        #Verificar que la funcion tenga un horario
                                        if Funciones.getHorario():
                                            if len(localTime) != 0:
                                                if Funciones.getHorario()[0] > localTime[-1][1]:
                                                    localTime.append(Funciones.getHorario())
                                                    asignadas += 1
                                                    #Calcular duracion de la Funcion
                                                    inicio = Funciones.getHorario()[0]
                                                    fin = Funciones.getHorario()[1]

                                                    duracionFuncion = (fin - inicio).total_seconds() / 3600.0
                                                    Persona.getTrabajos().append(duracionFuncion)
                                                    Funciones.setTrabajador(True)
                                                    funcionesDisponibles.pop(i)
                                                    continue
                                                else:
                                                    i += 1
                                            else:
                                                localTime.append(Funciones.getHorario())
                                                asignadas += 1

                                                inicio = Funciones.getHorario()[0]
                                                fin = Funciones.getHorario()[1]

                                                duracionFuncion = (fin - inicio).total_seconds() / 3600.0
                                                Persona.getTrabajos().append(duracionFuncion)
                                                Funciones.setTrabajador(True)
                                                funcionesDisponibles.pop(i)
                                                continue
                                        else:
                                            funcionesSinHorario += 1
                                            funcionesDisponibles.pop(i);
                                            continue
                                    else:
                                        break      
                                #Se organiza la lista para que no haya errores en caso de asignar las funciones restantes
                                localTime.sort(key = lambda horario: horario[0])
                                Persona.setHorario(localTime)
                                Persona.setDisponible(False)

                            if funcionesSinHorario == 1:
                                horarios = tk.Frame(infoSeguridad, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay una funcion sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                            elif funcionesSinHorario > 1:
                                horarios = tk.Frame(infoSeguridad, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay " + str(funcionesSinHorario) + " Funciones sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                        
                            #Evaluacion de salas sin trabajador
                            if funcionesDisponibles != 0:
                                for Persona in Teatro.getInstancia().getTipoSeguridad():
                                    localTime = list(Persona.getHorario())
                                    i = 0
                                    while i < len(funcionesDisponibles):
                                        Funciones = funcionesDisponibles[i]
                                        horarioValido = True
                                        inicioNuevo = Funciones.getHorario()[0]
                                        finNuevo = Funciones.getHorario()[1]
                                        #Verificar que no se solape
                                        #Se itera sobre las sublistas de localTime
                                        for j in range(len(localTime)):
                                            horarioActual = localTime[j]
                                            finActual = horarioActual[1]

                                            #Verificar que hay una sublista despues
                                            if j + 1 < len(localTime):
                                                horarioSiguiente = localTime[j+1]
                                                inicioSiguiente = horarioSiguiente[0]

                                                #Verificar que el horario nuevo no se solape
                                                if not (inicioNuevo > finActual and finNuevo < inicioSiguiente):
                                                            horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                                            
                                            else:
                                                #verificar que el inicio sea despues del horario ya existente
                                                if not(inicioNuevo > finActual):
                                                    horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                        if horarioValido:
                                            localTime.append(Funciones.getHorario())
                                            #Calcular Duracion
                                            inicio = Funciones.getHorario()[0]
                                            fin = Funciones.getHorario()[1]

                                            duracionFuncion = (fin - inicio).total_seconds() / 3600.0
                                            Persona.getTrabajos().append(duracionFuncion)
                                            Funciones.setTrabajodor(True)
                                            break
                                        else:
                                            i+=1
                                    localTime.sort(key = lambda horario: horario[0])
                                    Persona.setHorario(localTime)
                                    Persona.setDisponible(False)

                            #Se acaba la verificacion
                            #Imprimir mensajes
                            msg = "";
                            for Persona in Teatro.getInstancia().getTipoSeguridad():
                                if len(Persona.getHorario()) == 1:
                                    msg = msg + Persona.getNombre() + " Cuidará: 1 Funcion\n"
                                elif len(Persona.getHorario()) > 1 or len(Persona.getHorario()) == 0:
                                    msg = msg + Persona.getNombre() + " Cuidará: " + str(len(Persona.getHorario())) + " Funciones\n"
                            mensaje = tk.Label(infoSeguridad, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white")
                            mensaje.place(relx = 0.5, rely=0.5, relwidth= 0.8,relheight=0.7, anchor="center")
                    else:
                        if totalFunciones == 0:
                            alerta = tk.Frame(infoSeguridad, bg="#701C1A", bd=2, relief="groove")
                            alerta.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)
                            mensaje = tk.Label(alerta ,text="No hay funciones para agregar", font=("Calibri", 12), bg="#701C1A", fg="white")
                            mensaje.place(relx=0.5, rely=0.5, anchor="center")
                            trabajoAsignadoS = False
                        else:
                            alerta = tk.Frame(infoSeguridad, bg="#701C1A", bd=2, relief="groove")
                            alerta.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)
                            mensaje = tk.Label(alerta, text = "No hay trabajadores de Seguridad", font=("Calibri", 12), bg="#701C1A", fg="white")
                            mensaje.place(relx=0.5, rely=0.5, anchor="center")
                            trabajoAsignadoS = False
                    if len(funcionesDisponibles) != 0:
                        if len(funcionesDisponibles) == 1:
                            sinSeguridad = tk.Frame(infoSeguridad, bg = "gray")
                            sinSeguridad.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
                            Funcion = tk.Label(sinSeguridad, text="Existe 1 funcion sin posibilidad de seguridad", bg = "gray")
                            Funcion.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.8, anchor="center")
                        else:
                            sinSeguridad = tk.Frame(infoSeguridad, bg = "gray")
                            sinSeguridad.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
                            Funcion = tk.Label(sinSeguridad, text="Existen " + str(len(funcionesDisponibles)) + " funciones sin posibilidad de seguridad", bg = "gray")
                            Funcion.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.8, anchor="center")

                    f1.after(1000, lambda: asignarAseador(trabajoAsignadoS))
                    
                def asignarAseador(trabajoS):
                    trabajoAsignadoA = True
                    cant_trabajadores_principiantes = 0
                    base = 6
                    totalFunciones = len(Teatro.getInstancia().getFuncionesCreadas())
                    totalTrabajadores_A = len(Teatro.getInstancia().getTipoAseador())
                    funcionXTrabajador = 0
                    if totalTrabajadores_A != 0:
                        funcionXTrabajador = totalFunciones/totalTrabajadores_A
                    funcionesLimpiadas = list(Teatro.getInstancia().getFuncionesCreadas())
                    try:
                        funcionesLimpiadas.sort(key=lambda f : f.getHorario()[0])
                    except Exception as e:
                        pass

                    if funcionXTrabajador != 0:
                        for Persona in Teatro.getInstancia().getTipoAseador():
                            if Persona.getMetaSemanal() == base:
                                cant_trabajadores_principiantes += 1
                        #Todos principiantes
                        if cant_trabajadores_principiantes == totalTrabajadores_A:
                            funcionesSinHorario = 0
                            for Persona in Teatro.getInstancia().getTipoAseador():
                                asignadas = 0
                                localTime = list(Persona.getHorario())
                                i = 0
                                while i < len(funcionesLimpiadas):
                                    if asignadas < funcionXTrabajador:
                                        Funciones = funcionesLimpiadas[i]
                                        if Funciones.getHorario():
                                            if len(localTime) != 0:
                                                horarioValido = True
                                                inicioNuevo = Funciones.getHorario()[1]
                                                finNuevo = inicioNuevo + timedelta(minutes=15)

                                                for j in range(len(localTime)):
                                                    horarioActual = localTime[j]
                                                    finActual = horarioActual[1]

                                                    #Verificar si hay una sublista despues
                                                    if(j + 1) < len(localTime):
                                                        horarioSiguiente = localTime[j+1]
                                                        inicioSiguiente = horarioSiguiente[0]

                                                        #Verificar que el horario nuevo no se solapa
                                                        if not (inicioNuevo > finActual and finNuevo < inicioSiguiente):
                                                            horarioValido = False
                                                        else:
                                                            horarioValido = True
                                                            break
                                                            
                                                    else:
                                                        #verificar que el inicio sea despues del horario ya existente
                                                        if not(inicioNuevo > finActual):
                                                            horarioValido = False
                                                        else:
                                                            horarioValido = True
                                                            break         
                                                if horarioValido:
                                                    asignadas +=1
                                                    sublista = []
                                                    sublista.append(inicioNuevo)
                                                    sublista.append(finNuevo)
                                                    localTime.append(sublista)
                                                    if Funciones.getSala() is not None:
                                                        Persona.getTrabajos().append(Funciones.getSala().get_metros_cuadrados())
                                                        Funciones.getSala().set_aseado(True)
                                                    funcionesLimpiadas.pop(i)
                                                else:
                                                    i +=1
                                            else:
                                                #Se asigna la hora de fin de la funcion como el inicio del Empleado
                                                asignadas += 1
                                                sublista = []
                                                finFuncion = Funciones.getHorario()[1]
                                                #Se suma 15 min
                                                finEmpleado = finFuncion + timedelta(minutes=15)
                                                sublista.append(finFuncion)
                                                sublista.append(finEmpleado)
                                                #Se agrega a localTime
                                                localTime.append(sublista)
                                                funcionesLimpiadas.pop(i)
                                                if Funciones.getSala() is not None:
                                                    Persona.getTrabajos().append(Funciones.getSala().get_metros_cuadrados())
                                                    Funciones.getSala().set_aseado(True)
                                        else:
                                            funcionesSinHorario += 1
                                            funcionesLimpiadas.pop(i)
                                    else:
                                        break
                                
                                localTime.sort(key = lambda horario: horario[0])
                                Persona.setHorario(localTime)

                            if funcionesSinHorario == 1:
                                horarios = tk.Frame(infoAseador, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay una funcion sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                            elif funcionesSinHorario > 1:
                                horarios = tk.Frame(infoAseador, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay " + str(funcionesSinHorario) + " Funciones sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")

                            if len(funcionesLimpiadas) != 0:
                                for Persona in Teatro.getInstancia().getTipoAseador():
                                    localTime = list(Persona.getHorario())
                                    i = 0
                                    while i < len(funcionesLimpiadas):
                                        Funciones = funcionesLimpiadas[i]
                                        horarioValido = True
                                        inicioNuevo = Funciones.getHorario()[1]
                                        finNuevo = inicioNuevo + timedelta(minutes=15)
                                        for j in range(len(localTime)):
                                            horarioActual = localTime[j]
                                            finActual = horarioActual[1]

                                            #Verificar si hay sublista
                                            if(j+1 < len(localTime)):
                                                horarioSiguiente = localTime[j+1]
                                                inicioSiguiente = horarioSiguiente[0]
                                                
                                                #Verificar que no se solape
                                                if not (inicioNuevo > finActual and finNuevo < inicioSiguiente):
                                                    horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                                            
                                            else:
                                            #verificar que el inicio sea despues del horario ya existente
                                                if not(inicioNuevo > finActual):
                                                    horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                                
                                        if horarioValido:
                                            sublista = []
                                            sublista.append(inicioNuevo)
                                            sublista.append(finNuevo)
                                            localTime.append(sublista)
                                            funcionesLimpiadas.pop(i)
                                            if Funciones.getSala() is not None:
                                                Persona.getTrabajos().append(Funciones.getSala().get_metros_cuadrados())
                                                Funciones.getSala().set_aseado(True)
                                        else:
                                            i += 1

                                    localTime.sort(key = lambda horario: horario[0])
                                    Persona.setHorario(localTime)

                            msg = "";
                            for Persona in Teatro.getInstancia().getTipoAseador():
                                if len(Persona.getHorario()) == 1:
                                    msg = msg + Persona.getNombre() + " Limpiará: 1 vez\n"
                                else:
                                    msg = msg + Persona.getNombre() + " Limpiará: " + str(len(Persona.getHorario())) + " veces\n"
                            mensaje = tk.Label(infoAseador, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white")
                            mensaje.place(relx = 0.5, rely=0.5, relwidth= 0.8,relheight=0.7, anchor="center")
                        else:
                            funcionesPorMetros = list(Teatro.getInstancia().getFuncionesCreadas())
                            funcionesPorMetros.sort(
                                key = lambda f: (
                                    f.getHorario()[0],
                                    -f.getSala().get_metros_cuadrados()
                                )
                            )
                            funcionesLimpiadas = funcionesPorMetros
                            funcionesSinHorario = 0
                            for Persona in Teatro.getInstancia().getTipoAseador():
                                asignadas = 0
                                localTime = list(Persona.getHorario())
                                i = 0
                                while i < len(funcionesLimpiadas):
                                    if asignadas < funcionXTrabajador:
                                        Funciones = funcionesLimpiadas[i]
                                        if Funciones.getHorario():
                                            if len(localTime) != 0:
                                                horarioValido = True
                                                inicioNuevo = Funciones.getHorario()[1]
                                                finNuevo = inicioNuevo + timedelta(minutes=15)

                                                for j in range(len(localTime)):
                                                    horarioActual = localTime[j]
                                                    finActual = horarioActual[1]

                                                    #Verificar si hay una sublista despues
                                                    if(j + 1) < len(localTime):
                                                        horarioSiguiente = localTime[j+1]
                                                        inicioSiguiente = horarioSiguiente[0]

                                                        #Verificar que el horario nuevo no se solapa
                                                        if not (inicioNuevo > finActual and finNuevo < inicioSiguiente):
                                                            horarioValido = False
                                                        else:
                                                            horarioValido = True
                                                            break
                                                            
                                                    else:
                                                        #verificar que el inicio sea despues del horario ya existente
                                                        if not(inicioNuevo > finActual):
                                                            horarioValido = False
                                                        else:
                                                            horarioValido = True
                                                            break
                                                if horarioValido:
                                                    asignadas +=1
                                                    sublista = []
                                                    sublista.append(inicioNuevo)
                                                    sublista.append(finNuevo)
                                                    localTime.append(sublista)
                                                    if Funciones.getSala is not None:
                                                        Persona.getTrabajos().append(Funciones.getSala().get_metros_cuadrados())
                                                        Funciones.getSala().set_aseado(True)
                                                    funcionesLimpiadas.pop(i)
                                                else:
                                                    i +=1
                                            else:
                                                #Se asigna la hora de fin de la funcion como el inicio del Empleado
                                                asignadas += 1
                                                sublista = []
                                                finFuncion = Funciones.getHorario()[1]
                                                #Se suma 15 min
                                                finEmpleado = finFuncion + timedelta(minutes=15)
                                                sublista.append(finFuncion)
                                                sublista.append(finEmpleado)
                                                #Se agrega a localTime
                                                localTime.append(sublista)
                                                funcionesLimpiadas.pop(i)
                                                if Funciones.getSala() is not None:
                                                    Persona.getTrabajos().append(Funciones.getSala().get_metros_cuadrados())
                                                    Funciones.getSala().set_aseado(True)
                                        else:
                                            funcionesSinHorario += 1
                                            funcionesLimpiadas.pop(i)
                                    else:
                                        break
                                
                                localTime.sort(key = lambda horario: horario[0])
                                Persona.setHorario(localTime)

                            if funcionesSinHorario == 1:
                                horarios = tk.Frame(infoAseador, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay una funcion sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                            elif funcionesSinHorario > 1:
                                horarios = tk.Frame(infoAseador, bg="red")
                                horarios.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                                horarioLabel = tk.Label(horarios, text="Hay " + str(funcionesSinHorario) + " Funciones sin horarios", font=("Calibri", 12), bg="red", fg="white")
                                horarioLabel.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                            
                            if len(funcionesLimpiadas) != 0:
                                for Persona in Teatro.getInstancia().getTipoAseador():
                                    localTime = list(Persona.getHorario())
                                    i = 0
                                    while i < len(funcionesLimpiadas):
                                        Funciones = funcionesLimpiadas[i]
                                        horarioValido = True
                                        inicioNuevo = Funciones.getHorario()[1]
                                        finNuevo = inicioNuevo + timedelta(minutes=15)
                                        for j in range(len(localTime)):
                                            horarioActual = localTime[j]
                                            finActual = horarioActual[1]

                                            #Verificar si hay sublista
                                            if(j+1 < len(localTime)):
                                                horarioSiguiente = localTime[j+1]
                                                inicioSiguiente = horarioSiguiente[0]
                                                
                                                #Verificar que no se solape
                                                if not (inicioNuevo > finActual and finNuevo < inicioSiguiente):
                                                            horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                                            
                                            else:
                                                #verificar que el inicio sea despues del horario ya existente
                                                if not(inicioNuevo > finActual):
                                                    horarioValido = False
                                                else:
                                                    horarioValido = True
                                                    break
                                        if horarioValido:
                                            sublista = []
                                            sublista.append(inicioNuevo)
                                            sublista.append(finNuevo)
                                            localTime.append(sublista)
                                            funcionesLimpiadas.pop(i)
                                            if Funciones.getSala() is not None:
                                                Persona.getTrabajos().append(Funciones.getSala().get_metros_cuadrados())
                                                Funciones.getSala().set_aseado(True)
                                        else:
                                            i += 1

                                    localTime.sort(key = lambda horario: horario[0])
                                    Persona.setHorario(localTime)
                    
                            msg = ""
                            for Persona in Teatro.getInstancia().getTipoAseador():
                                if len(Persona.getHorario()) == 1:
                                    msg = msg + Persona.getNombre() + " Limpiará: 1 vez\n"
                                else:
                                    msg = msg + Persona.getNombre() + " Limpiará: " + str(len(Persona.getHorario())) + " veces\n"
                            mensaje = tk.Label(infoAseador, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white")
                            mensaje.place(relx = 0.5, rely=0.5, relwidth= 0.8,relheight=0.7, anchor="center")
                    else:
                        if totalFunciones == 0:
                            alerta = tk.Frame(infoAseador, bg="#701C1A", bd=2, relief="groove")
                            alerta.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)
                            mensaje = tk.Label(alerta ,text="No hay funciones para poder Limpiar", font=("Calibri", 12), bg="#701C1A", fg="white")
                            mensaje.place(relx=0.5, rely=0.5, anchor="center")
                            trabajoAsignadoA = False
                        else:
                            alerta = tk.Frame(infoAseador, bg="#701C1A", bd=2, relief="groove")
                            alerta.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.5)
                            mensaje = tk.Label(alerta, text = "No hay Aseadores", font=("Calibri", 12),bg="#701C1A", fg="white")
                            mensaje.place(relx=0.5, rely=0.5, anchor="center")
                            trabajoAsignadoA = False
                    
                    if len(funcionesLimpiadas) != 0:
                        if len(funcionesLimpiadas) == 1:
                            sinAseador = tk.Frame(infoAseador, bg = "gray")
                            sinAseador.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
                            Funcion = tk.Label(sinAseador, text="Existe 1 funcion sin posibilidad de limpiar la sala", bg = "gray")
                            Funcion.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.8, anchor="center")
                        else:
                            sinAseador = tk.Frame(infoAseador, bg = "gray")
                            sinAseador.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
                            Funcion = tk.Label(sinAseador, text="Existen " + str(len(funcionesLimpiadas)) + " funciones sin posibilidad de limpiar la sala", bg = "gray")
                            Funcion.place(relx=0.5, rely=0.5, relheight=0.8, relwidth=0.8, anchor="center")

                    f1.after(1000, lambda: verificarTrabajo(trabajoS, trabajoAsignadoA))
                
                def verificarTrabajo(trabajoS, trabajoA):
                    if trabajoS or trabajoA:
                        cls.clear_frame(f1)
                        p1 = tk.Frame(f1, bg = "#701C1A")
                        p1.place(relx=0, rely=0, relwidth= 1, relheight=0.5)
                        info = tk.Label(p1, text="trabajos Asignados....\nDesplegando trabajadores", bg= "#701C1A", fg="white", font=("Calibri", 16))
                        info.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")

                        p2 = tk.Frame(f1, bg="#701C1A")
                        p2.place(relx = 0, rely=0.5, relwidth=1, relheight=0.25)
                        info2 = tk.Label(p2, text="Verificando los trabajos...", font=("Calibri", 16), bg="#701C1A", fg="white")
                        info2.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                        p3 = tk.Frame(f1, bg="#701C1A")
                        p3.place(relx = 0, rely=0.75, relwidth=1, relheight=0.25)

                        def verificar():
                            #Para Seguridad
                            principiantes = 0
                            for Persona in Teatro.getInstancia().getTipoSeguridad():
                                if Persona.getMetaSemanal() == 6:
                                    principiantes += 1
                                   
                            if principiantes == len(Teatro.getInstancia().getTipoSeguridad()):
                                for Persona in Teatro.getInstancia().getTipoSeguridad():
                                    for Hora in Persona.getTrabajos():
                                        randomValue = round(random.uniform(0, 1), 2)
                                        if randomValue > 0.5:
                                            Persona.getTrabajoCorrecto().append(True)
                                            Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Hora)
                                            Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                        else:
                                            Persona.getTrabajoCorrecto().append(False)
                            else:
                                for Persona in Teatro.getInstancia().getTipoSeguridad():
                                    for Hora in Persona.getTrabajos():
                                        randomValue = round(random.uniform(0, 1), 2)
                                        if Persona.getMetaSemanal() > 20:
                                            if Hora >= 4:
                                                if randomValue > 0.65:
                                                    Persona.getTrabajoCorrecto().append(True)
                                                    Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Hora)
                                                    Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                                else:
                                                    Persona.getTrabajoCorrecto().append(False)
                                            else:
                                                if randomValue > 0.4:
                                                    Persona.getTrabajoCorrecto().append(True)
                                                    Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Hora)
                                                    Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                                else:
                                                    Persona.getTrabajoCorrecto().append(False)
                                        else:
                                            if randomValue > 0.5:
                                                Persona.getTrabajoCorrecto().append(True)
                                                Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Hora)
                                                Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                            else:
                                                Persona.getTrabajoCorrecto().append(False)

                            #Para Aseador
                            principiantes = 0
                            for Persona in Teatro.getInstancia().getTipoAseador():
                                if Persona.getMetaSemanal() == 6:
                                    principiantes += 1
                            if principiantes == len(Teatro.getInstancia().getTipoAseador()):
                                for Persona in Teatro.getInstancia().getTipoAseador():
                                    for Metros in Persona.getTrabajos():
                                        randomValue = round(random.uniform(0, 1), 2)
                                        if randomValue > 0.5:
                                            Persona.getTrabajoCorrecto().append(True)
                                            Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Metros)
                                            Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                        else:
                                            Persona.getTrabajoCorrecto().append(False)
                            else:
                                for Persona in Teatro.getInstancia().getTipoAseador():
                                    for Metros in Persona.getTrabajos():
                                        randomValue = round(random.uniform(0, 1), 2)
                                        if Persona.getMetaSemanal() > 20:
                                            if Metros > 650:
                                                if randomValue > 0.65:
                                                    Persona.getTrabajoCorrecto().append(True)
                                                    Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Metros)
                                                    Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                                else:
                                                    Persona.getTrabajoCorrecto().append(False)
                                            else:
                                                if randomValue > 0.4:
                                                    Persona.getTrabajoCorrecto().append(True)
                                                    Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Metros)
                                                    Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                                else:
                                                    Persona.getTrabajoCorrecto().append(False)
                                        else:
                                            if randomValue > 0.5:
                                                Persona.getTrabajoCorrecto().append(True)
                                                Persona.setTrabajoRealizado(Persona.getTrabajoRealizado() + Metros)
                                                Persona.setPuntosPositivos(Persona.getPuntosPositivos() + 1)
                                            else:
                                                Persona.getTrabajoCorrecto().append(False)

                            info3 = tk.Label(p3, text="Verificacion finalizada", font=("Calibri", 16),  bg="#701C1A", fg="white")
                            info3.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                        
                        f1.after(1000, lambda: verificar())
                    else:
                        cls.clear_frame(f1)
                        mensaje = "No hay trabajos para asignar\n No se puede verificar los trabajos"
                        info = tk.Label(f1, text=mensaje,  bg="#701C1A", fg="white", font=("Calibri", 18))
                        info.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                    
                    f1.after(2000, lambda: continuar3())
                
                f1.after(1000, lambda: asignarSeguridad())
                
            def continuar3():
                def actualizarSaldo():
                    nuevo_saldo = "El saldo de tesoreria es: " + cls.toCop(Teatro.getInstancia().getTesoreria().getCuenta().getSaldo())
                    saldo.config(text=nuevo_saldo)
                
                cls.clear_frame(f1)
                p = tk.Frame(f1, bg="#701C1A")
                p.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)
                Fsaldo = tk.Frame(p, bg="#4B2D2E")
                Fsaldo.place(relx=0, rely=0, relwidth=1, relheight=0.1, anchor="nw") 
                Msaldo = "El saldo de tesoreria es: " + cls.toCop(Teatro.getInstancia().getTesoreria().getCuenta().getSaldo())
                saldo = tk.Label(Fsaldo, text=Msaldo, font=("Calibri", 14), bg="#4B2D2E", fg="#FCE6C9")
                saldo.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                contenido = tk.Frame(p, bg="#701C1A")
                contenido.place(relx=0, rely=0.1, relwidth=1, relheight=0.9, anchor="nw")
                leftframeC = tk.Frame(contenido, bg="#701C1A")
                leftframeC.place(relx=0, rely=0, relwidth=0.5, relheight=1)
                righframe = tk.Frame(contenido, bg="#701C1A")
                righframe.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

                #leftFrame = Ranking
                Ranking = list(Teatro.getInstancia().getEmpleadosPorRendimiento())
                Ranking = [E for E in Ranking if E.getMetaSemanal() >=0]
                Ranking.sort(key=lambda E: E.getMetaSemanal(), reverse=True)
                
                RankingE = tk.Frame(leftframeC, bg="#701C1A")
                RankingE.pack(side="top", fill="x", anchor="n", padx=10)
                Empleados = tk.Label(RankingE, text="Ranking Empleados", font=("Calibri", 14), bg="#701C1A", fg="white")
                Empleados.pack(anchor="center", fill="both")

                #tabla
                frame_tabla = tk.Frame(leftframeC)
                frame_tabla.pack(expand=True, fill="both", padx=10, pady=1)

                #Encabezados
                encabezados = ["Nombre", "IDs"]
                for col, texto in enumerate(encabezados):
                    encabezado = tk.Label(frame_tabla, text=texto, font=("Calibri", 12), bg="#d3d3d3", padx=10, pady=1)
                    encabezado.grid(row=0, column=col, sticky="ew")
                
                #Fila de datos
                for fila, emp in enumerate(Ranking, start=1):
                    nombre = tk.Label(frame_tabla, text=emp.getNombre(), padx=10, pady=1 )
                    nombre.grid(row=fila, column=0, sticky="ew")

                    id = tk.Label(frame_tabla, text=emp.getId(), padx=10, pady=1)
                    id.grid(row=fila, column=1, sticky="ew")
                
                #Ajustar columnas
                for col in range(2):
                    frame_tabla.grid_columnconfigure(col, weight=1)
            
                
                #Frame derecho
                question = tk.Frame(righframe, bg="#701C1A")
                question.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                ask = tk.Label(question, text="¿Deseas realizar los pagos?", font=("Calibri", 14), bg="#701C1A", fg="white")
                ask.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                botones = tk.Frame(righframe, bg = "#701C1A")
                botones.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
                button_yes = tk.Button(botones, text = "Si", bg="#AE1918" ,fg="White", font=("Calibri", 12))
                button_yes.pack(side="left", fill="both", padx=15, pady=5, anchor="center", expand=True)
                button_no = tk.Button(botones, bg="#AE1918", text = "No", fg="White", font=("Calibri", 12))
                button_no.pack(side="left", fill="both", padx=15, pady=5, anchor="center", expand=True)

                def yes():
                    cls.clear_frame(righframe)
                    fondos= Teatro.getInstancia().getTesoreria().getCuenta().getSaldo()
                    totalSaldos = 0
                    for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                        totalSaldos = totalSaldos + Persona.calcularSueldo()
                    #Realizar pago
                    if totalSaldos > fondos:
                        Cuentas_Pagadas = []
                        cantPagada = 0.0
                        linea = 0.2
                        tk.Label(righframe, text="Upps ... No se puede realizar los pagos adecuadamente", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=0, relwidth=1, relheight=0.1)
                        tk.Label(righframe, text="Realizando pagos de manera equitativa", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
                        for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                            transaccion = Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), (Persona.getDeuda() + Persona.calcularSueldo()) * 0.5)
                            if transaccion:
                                cantPagada = cantPagada + ((Persona.calcularSueldo() + Persona.getDeuda())*0.5)
                                Persona.setDeuda((Persona.getDeuda() + (Persona.calcularSueldo() + Persona.getDeuda())* 0.5))
                                Cuentas_Pagadas.append(Persona)
                            else:
                                tk.Label(righframe, text="No se le puede pagar a: " + Persona.getNombre() + ", se le establecio una nueva deuda", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                Persona.setDeuda(Persona.getDeuda() + Persona.calcularSueldo())
                                linea += 0.1
                        tk.Label(righframe, text="Pago exitoso", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                        linea += 0.1
                        msg = "Se pago un total de: " + str(cantPagada)
                        tk.Label(righframe, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                        linea += 0.1
                        tk.Label(righframe, text="Se realizo el pago a " + str(len(Cuentas_Pagadas)), font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                        linea += 0.1
                        actualizarSaldo()
                        Cuentas_Pagadas = []
                    else:
                        #Verificacion Fondos Bonificacion
                        totalSaldos = 0
                        cantPagada = 0
                        linea = 0
                        if Teatro.getInstancia().getTesoreria().verificacionMeta() != True:
                            for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                if Persona.verificacionMeta():
                                    Persona.setMetaSemanal(Persona.getMetaSemanal() + 10)
                                    totalSaldos = totalSaldos + ((Persona.calcularSueldo() * 1.15) + Persona.getDeuda())
                                else:
                                    Persona.setMetaSemanal(Persona.getMetaSemanal()-5)
                                    totalSaldos = totalSaldos + (Persona.calcularSueldo() + Persona.getDeuda())
                            #Realizacion Pagos
                            if totalSaldos > fondos:
                                totalSaldos = 0
                                tk.Label(righframe, text="Ups... No se pueden aplicar las bonificaciones personales", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                linea += 0.1
                                tk.Label(righframe, text="Realizando Pagos", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                linea += 0.1
                                for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                    cantPagada = cantPagada + (Persona.calcularSueldo() + Persona.getDeuda())
                                    totalSaldos = totalSaldos + Persona.calcularSueldo()
                                #Pago solo sueldo Base
                                if cantPagada > fondos:
                                    tk.Label(righframe, text="No se pudo realizar los pagos junto a la deuda", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    tk.Label(righframe, text="Realizando Pago del Sueldo Base", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                        Teatro.getInstancia().getTesoreria().pagarSueldoBase(Persona.getCuenta(), Persona.calcularSueldo())
                                    tk.Label(righframe, text="Pago exitoso", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    msg = "Se pago un total de: " + str(totalSaldos)
                                    tk.Label(righframe, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    tk.Label(righframe, text="Se realizo el pago a: " + len(Teatro.getInstancia().getEmpleadosPorRendimiento()) + " cuentas en total", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    actualizarSaldo()
                                    for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                        if Persona.verificacionMeta:
                                            Persona.setDeuda(Persona.getDeuda() + Persona.calcularSueldo()*0.15)
                                else:
                                    #Pago sueldo + deuda
                                    for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                        Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), Persona.getDeuda() + Persona.calcularSueldo())
                                    tk.Label(righframe, text="Pago exitoso", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    msg = "Se pago un total de: " + str(cantPagada)
                                    tk.Label(righframe, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    tk.Label(righframe, text="Se realizo el pago a: " + str(len(Teatro.getInstancia().getEmpleadosPorRendimiento())) + " cuentas en total", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    actualizarSaldo()
                            else:
                                #Pago boni + deuda
                                for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                    if Persona.verificacionMeta:
                                        Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), (Persona.calcularSueldo()*1.15) + Persona.getDeuda())
                                    else:
                                        Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), Persona.calcularSueldo() + Persona.getDeuda())
                                tk.Label(righframe, text="Pago exitoso", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                linea += 0.1
                                msg = "Se pago un total de: " + str(totalSaldos)
                                tk.Label(righframe, text=msg, font=("Calibri", 12),bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                linea += 0.1
                                tk.Label(righframe, text="Se realizo el pago a: " + str(len(Teatro.getInstancia().getEmpleadosPorRendimiento())) + " cuentas en total", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                actualizarSaldo()
                        else:
                            for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                if Persona.verificacionMeta():
                                    Persona.setMetaSemanal(Persona.getMetaSemanal() + 10)
                                    totalSaldos = totalSaldos + ((Persona.calcularSueldo() * 1.45) + Persona.getDeuda())
                                else:
                                    Persona.setMetaSemanal(Persona.getMetaSemanal()-5)
                                    totalSaldos = totalSaldos + ((Persona.calcularSueldo() * 1.3) + Persona.getDeuda())
                            #Sin fondos para todas las bonificacion
                            if totalSaldos > fondos:
                                totalSaldos = 0
                                for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                    if Persona.verificacionMeta():
                                        Persona.setMetaSemanal(Persona.getMetaSemanal() + 10)
                                        totalSaldos = totalSaldos + ((Persona.calcularSueldo() * 1.15) + Persona.getDeuda())
                                    else:
                                        Persona.setMetaSemanal(Persona.getMetaSemanal()-5)
                                        totalSaldos = totalSaldos + (Persona.calcularSueldo() + Persona.getDeuda())
                                #Realizar Pagos
                                if totalSaldos > fondos:
                                    #Verificacion
                                    totalSaldos = 0
                                    tk.Label(righframe, text="Ups... No se pueden aplicar las bonificaciones personales", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    tk.Label(righframe, text="Realizando Pagos", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                        cantPagada = cantPagada + (Persona.calcularSueldo() + Persona.getDeuda())
                                        totalSaldos = totalSaldos + Persona.calcularSueldo()
                                    #Pago solo sueldo Base
                                    if cantPagada > fondos:
                                        tk.Label(righframe, text="No se pudo realizar los pagos junto a la deuda", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        linea += 0.1
                                        tk.Label(righframe, text="Realizando Pago del Sueldo Base", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        linea += 0.1
                                        for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                            Teatro.getInstancia().getTesoreria().pagarSueldoBase(Persona.getCuenta(), Persona.calcularSueldo())
                                        tk.Label(righframe, text="Pago exitoso", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        linea += 0.1
                                        msg = "Se pago un total de: " + str(totalSaldos)
                                        tk.Label(righframe, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        linea += 0.1
                                        tk.Label(righframe, text="Se realizo el pago a: " + str(len(Teatro.getInstancia().getEmpleadosPorRendimiento())) + " cuentas en total", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        actualizarSaldo()
                                        for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                            if Persona.verificacionMeta:
                                                Persona.setDeuda(Persona.getDeuda() + Persona.calcularSueldo()*0.15)
                                    else:
                                        #Pago sueldo + deuda
                                        for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                            Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), Persona.getDeuda() + Persona.calcularSueldo())
                                        tk.Label(righframe, text="Pago exitoso", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        linea += 0.1
                                        msg = "Se pago un total de: " + str(cantPagada)
                                        tk.Label(righframe, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        linea += 0.1
                                        tk.Label(righframe, text="Se realizo el pago a: " + str(len(Teatro.getInstancia().getEmpleadosPorRendimiento())) + " cuentas en total", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                        actualizarSaldo()
                                else:
                                    #Pago boni + deuda
                                    for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                        if Persona.verificacionMeta:
                                            Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), (Persona.calcularSueldo()*1.15) + Persona.getDeuda())
                                        else:
                                            Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), Persona.calcularSueldo() + Persona.getDeuda())
                                    tk.Label(righframe, text="Pago exitoso", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    msg = "Se pago un total de: " + str(totalSaldos)
                                    tk.Label(righframe, text=msg, font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    linea += 0.1
                                    tk.Label(righframe, text="Se realizo el pago a: " + str(len(Teatro.getInstancia().getEmpleadosPorRendimiento())) + " cuentas en total", font=("Calibri", 12), bg="#701C1A", fg="white").place(relx=0, rely=linea, relwidth=1, relheight=0.1)
                                    actualizarSaldo()
                            else:
                                for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                                    if Persona.verificacionMeta:
                                        Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), (Persona.calcularSueldo()*1.45) + Persona.getDeuda())
                                    else:
                                        Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), (Persona.calcularSueldo() * 1.3) + Persona.getDeuda())
                    
                    #Reseteo de Trabajo
                    for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
                        Persona.setTrabajos([])
                        Persona.setHorario([])
                        Persona.setTrabajoCorrecto([])
                        Persona.setTrabajoRealizado(0)
                        Persona.setPuntosPositivos(0)

                    righframe.after(3000, lambda: Despidos())


                def Despidos():
                    cls.clear_frame(righframe)
                    Empleados = list(Teatro.getInstancia().getEmpleadosPorRendimiento())
                    NuevaLista = list(Empleados)
                    Despedidos = []
                    #Exepcion de no seleccionar la casilla
                    msg = ""
                    for Persona in Empleados:
                        if Persona.getMetaSemanal() < 0:
                            NuevaLista.remove(Persona)
                            Despedidos.append(Persona)
                            liquidacion = (Persona.calcularSueldo() * 1.2) + Persona.getDeuda()
                            Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), liquidacion)
                            msg = msg + Persona.getNombre() + "\n"
                            if Persona.getOcupacion() != "Seguridad":
                                if Persona.getOcupacion() != "Aseador":
                                    Teatro.getInstancia().getTipoProfesor().remove(Persona)
                                else:
                                    Teatro.getInstancia().getTipoAseador().remove(Persona)
                            else:
                                Teatro.getInstancia().getTipoSeguridad().remove(Persona)
                        continue
                    Teatro.getInstancia().setEmpleadosPorRendimiento(NuevaLista)

                    if Despedidos:
                        titulo = tk.Label(righframe, text="Personas despedidas:", bg="#701C1A", fg="white")
                        titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)
                        despedidos = tk.Label(righframe, text=msg, font=("Calibri", 14), bg="#701C1A", fg="white")
                        despedidos.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.8, anchor="center")
                    
                    button_salir = tk.Button(righframe, text="Salir", bg="#AE1918" ,fg="White", font=("Calibri", 12))
                    button_salir.place(relx=0.7, rely=0.9, relwidth=0.3, relheight=0.1, anchor="center")
                    button_salir.config(command=lambda: cls.gestionEmpleados())

                button_yes.config(command=lambda: yes()) 
                button_no.config(command=lambda: Despidos()) 

            f1.after(0, lambda: continuar())            
        
        # --- Partes del contenido --- #
        #f1 es el central
        f1 = tk.Frame(cls.content, bg = "#4B2D2E")
        f1.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)
        
        #frame izquierdo
        leftFrame = tk.Frame(cls.content, bg="#5d2417")
        leftFrame.place(relx=0, rely=0, relwidth=0.175, relheight=0.9)

        #frame derecho
        rightFrame = tk.Frame(cls.content, bg="#5d2417")
        rightFrame.place(relx=0.825, rely=0, relwidth=0.175, relheight=0.9)
        
        #frame inferior
        bottomFrame = tk.Frame(cls.content, bg="#5d2417")
        bottomFrame.place(relx=0, rely=0.9, relheight=0.2, relwidth=1)
        
        '''IMAGEN BOTTOM (ASIENTOS)'''
        # Cargar la imagen original (asegúrate de que el archivo se encuentre en el mismo directorio)
        imagen_bottom = Image.open("src/media/Theme/bottom.png")  
        image = ImageTk.PhotoImage(imagen_bottom)

        # Crear un Label que contendrá la imagen y que cubra todo el bottomFrame
        bottom_label = tk.Label(bottomFrame, image=image)
        bottom_label.place(relheight=1, relwidth=1)

        # Vincular el evento <Configure> usando lambda para pasar la imagen y el label a la función
        bottomFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_bottom, bottom_label))

        '''IMAGEN RIGHT (CORTINA DER)'''
        imagen_right = Image.open("src/media/Theme/Courtain right.png")  
        image_der = ImageTk.PhotoImage(imagen_right)

        right_label = tk.Label(rightFrame, image=image_der, bg="black")
        right_label.place(relheight=1, relwidth=1)

        rightFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_right, right_label))

        '''IMAGEN LEFT (CORTINA IZQ)'''

        imagen_left = Image.open("src/media/Theme/Courtain left.png")  
        image_izq = ImageTk.PhotoImage(imagen_left)

        left_label = tk.Label(leftFrame, image=image_izq, bg="black")
        left_label.place(relheight=1, relwidth=1)

        leftFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_left, left_label))

        # Encabezado
        Titulo = tk.Frame(cls.content, bg="#070709")
        Titulo.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        TituloLabel = tk.Label(Titulo, text="Bienvenido a la gestion de empleados", font=("Calibri", 14), fg="#FCE6C9", bg="#070709")
        TituloLabel.pack(fill="both", expand=True)
        TituloLabel.bind("<Configure>", lambda e: cls.resize(Titulo, TituloLabel, 8, 50, False))
        
        #Accion principal
        Anuncio = tk.Frame(f1, bg="#701C1A")
        Anuncio.place(relx = 0.5, rely=0.5,anchor="center", relwidth=0.9, relheight=0.8)
        texto = tk.Label(Anuncio, text="Se estan pagando las deudas pendientes \nPorfavor espere...", font=("Calibri", 18), bg="#701C1A", fg="white", bd = 10, relief="raised")
        texto.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor="center")

        Teatro.getInstancia().getTesoreria().transferenciaFondos()
            
        # Verificar si hay deudas y pagar

        Deudas = ""
        for Persona in Teatro.getInstancia().getEmpleadosPorRendimiento():
            if Persona.getDeuda() != 0:
                if Teatro.getInstancia().getTesoreria().getCuenta().getSaldo() > Persona.getDeuda():
                    transaccion = Teatro.getInstancia().getTesoreria().getCuenta().transferencia(Persona.getCuenta(), Persona.getDeuda())
                    if transaccion:
                        Deudas = Deudas + "Se realizo el pago a: " + Persona.getNombre() + " por un valor de: " + str(Persona.getDeuda()) + "\n"
                        Persona.setDeuda(0)
    
        Saldo = cls.toCop(Teatro.getInstancia().getTesoreria().getCuenta().getSaldo())

        def mostrarSaldo():
            cls.clear_frame(Anuncio)
            textoSaldo = tk.Label(Anuncio, text= Deudas + "El saldo actual de la tesoreria es: " + Saldo, font=("Calibri", 14), bg="#701C1A", fg="white", bd = 10, relief="raised")
            textoSaldo.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor="center")
            f1.after(1500, lambda: run2())
        
        f1.after(1500, lambda: mostrarSaldo())


    @classmethod
    def gestionObras(cls):
        for widget in cls.content.winfo_children():
            widget.destroy()

        # --- FRAME DE BIENVENIDA ---
        '''AVALADA'''
        
        #frame izquierdo
        leftFrame = tk.Frame(cls.content, bg="blue")
        leftFrame.place(relx=0, rely=0, relwidth=0.175, relheight=0.9)

        #frame derecho
        rightFrame = tk.Frame(cls.content, bg="blue")
        rightFrame.place(relx=0.825, rely=0, relwidth=0.175, relheight=0.9)
        
        #frame inferior
        bottomFrame = tk.Frame(cls.content, bg="pink")
        bottomFrame.place(relx=0, rely=0.9, relheight=0.2, relwidth=1)

        frame_marco = tk.Frame(cls.content, bg="#4B2D2E", padx=20, pady=20)
        frame_marco.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

        # --- FRAME PRINCIPAL PARA EL PROCESO ---
        process_frameO = Frame(frame_marco, bg="#701C1A", padx=20, pady=20)
        process_frameO.place(relwidth= 1, relheight= 1)
        
        frame_bienvenida = Frame(cls.content, bg="red")
        frame_bienvenida.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)
        saludo = tk.Label(frame_bienvenida,
                            text="Gestion de Obras",
                            font=("Calibri", 16),
                            bg="#070709", fg="#FCE6C9")
        saludo.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame_bienvenida.bind(
            "<Configure>",
            lambda e: cls.resize(frame_bienvenida, saludo, 10, 60, False)
        ) 

        '''IMAGEN BOTTOM (ASIENTOS)'''
        # Cargar la imagen original (asegúrate de que el archivo se encuentre en el mismo directorio)
        imagen_bottom = Image.open("src/media/Theme/bottom.png")  
        image = ImageTk.PhotoImage(imagen_bottom)

        # Crear un Label que contendrá la imagen y que cubra todo el bottomFrame
        bottom_label = tk.Label(bottomFrame, image=image)
        bottom_label.place(relheight=1, relwidth=1)

        # Vincular el evento <Configure> usando lambda para pasar la imagen y el label a la función
        bottomFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_bottom, bottom_label))

        '''IMAGEN RIGHT (CORTINA DER)'''
        imagen_right = Image.open("src/media/Theme/Courtain right.png")  
        image_der = ImageTk.PhotoImage(imagen_right)

        right_label = tk.Label(rightFrame, image=image_der, bg="black")
        right_label.place(relheight=1, relwidth=1)

        rightFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_right, right_label))

        '''IMAGEN LEFT (CORTINA IZQ)'''

        imagen_left = Image.open("src/media/Theme/Courtain left.png")  
        image_izq = ImageTk.PhotoImage(imagen_left)

        left_label = tk.Label(leftFrame, image=image_izq, bg="black")
        left_label.place(relheight=1, relwidth=1)

        leftFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_left, left_label))

        def step1Obras():
            for widget in process_frameO.winfo_children():
                widget.destroy()
            obras = Teatro.getInstancia().getObras()
            if obras:
                lbl_obras = tk.Label(process_frameO, 
                                    text = "Obras existentes en la base de datos:",
                                    font = ("Calibri", 14), 
                                    bg = "#701C1A",
                                    fg = "#FCE6C9")
                lbl_obras.pack(pady=10)
                txt_obras = tk.Text(process_frameO, 
                                    height=6, width=80,
                                    font=("Calibri", 12),
                                    bg = "#701C1A",
                                    fg = "#FCE6C9")
                txt_obras.pack(pady=10, fill="both", expand=True)
                for obra in obras:
                    if obra.getNombre() != "NOTFORITE":
                        linea = f"- Obra {obra.getNombre()}\n"
                        txt_obras.insert("end", linea)
                txt_obras.config(state="disabled")
            else:
                tk.Label(process_frameO, 
                        text="No hay obras en la base de datos.",
                        font=("Calibri", 14), 
                        bg="#701C1A", fg="#FCE6C9").pack(pady=10, 
                                                        fill = "x")
                return

            lbl_name = tk.Label(process_frameO, 
                                text="Ingrese el nombre de la obra que desea gestionar:",
                                font=("Calibri", 14), 
                                bg="#701C1A", fg="#FCE6C9")
            lbl_name.pack(pady=10, fill="x")
            entry_name = tk.Entry(process_frameO, 
                                font=("Calibri", 14))
            entry_name.pack(pady=5)
            btn_buscarN = tk.Button(process_frameO,
                                    text="Buscar", 
                                    font=("Calibri", 14),
                                    bg = "#701C1A", fg = "#FCE6C9",
                                    command=lambda: process_obra(entry_name.get()))
            btn_buscarN.pack(pady=10)
            
            Main.resize(process_frameO, lbl_obras, 14, 60, True)

        # -------------------- PASO 2: Procesar el ID ingresado --------------------
        '''AVALADA'''
        def process_obra(name_str):
            obra = Obra.buscarObra(name_str)
            if obra is None:
                step_obra_not_found(name_str)
            else:
                step_obra_found(obra)

        # -------------------- PASO 3: Artista no encontrado --------------------
        '''AVALADA'''
        def step_obra_not_found(name_str):
            for widget in process_frameO.winfo_children():
                widget.destroy()
            tk.Label(process_frameO, 
                    text=f"Obra con nombre {name_str} no encontrada.",
                    font=("Calibri", 14), 
                    bg="#701C1A", fg="#FCE6C1").pack(pady=10, 
                                                    fill = "x")
            tk.Label(process_frameO, 
                    text="¿Desea crear una nueva Obra con este nombre?",
                    font=("Calibri", 14), 
                    bg= "#701C1A", fg = "#FCE6C1").pack(pady=10)
            tk.Button(process_frameO, 
                    text="Sí", 
                    font=("Calibri", 14),
                    bg="#701C1A", fg="#FCE6C1",
                    width = 10,
                    command=lambda: step_create_obra(name_str)).pack(pady=5)
            tk.Button(process_frameO, 
                    text="No", 
                    font=("Calibri", 14),
                    bg = "#701C1A", fg = "#FCE6C1",
                    width = 10,
                    command=lambda: step1Obras()).pack(pady=5)

        # -------------------- PASO 4: Crear nuevo artista --------------------
        '''AVALADA'''
        def step_create_obra(name_str):
            for widget in process_frameO.winfo_children():
                widget.destroy()
            criteriosObra = ["Nombre", "Actor", "Aptitud", "Genero", "Director","Costo de producción", "Duración de la obra (HHMMSS)"]
            valoresObra = ["", "", "", "", "", "", ""]
            ff = FieldFrame(process_frameO,
                            tituloCriterios="Datos de la nueva obra",
                            criterios=criteriosObra,
                            tituloValores="Ingrese su respuesta <3",
                            valores=valoresObra,
                            combobox=False,
                            command=lambda: (ff.gatherEntries(), 
                                            process_new_obra(name_str, 
                                                            ff.valores[1], 
                                                            ff.valores[2],
                                                            ff.valores[3], 
                                                            ff.valores[4],
                                                            ff.valores[5],
                                                            ff.valores[6])))
            ff.pack(pady=10, fill="both", expand=True)

        def process_new_obra(name_str, actor, aptitud, genero, director, costo, duracion):
            name_str = str(name_str)
            actor = Artista.buscarPorNombre(actor)
            aptitud = Aptitud[aptitud.upper().trim()]
            genero = Genero[genero.upper().trim()]
            director = Artista.buscarPorNombre(director)
            costo = float(costo)
            duracion = float(duracion)
            if director == None:
                for widget in process_frameO.winfo_children():
                    widget.destroy()
                criteriosDir = ["Nombre", "ID", "Genero"]
                valoresDir = ["", 0, genero]
                fieldframedir = FieldFrame(process_frameO, 
                                        tituloCriterios = "Datos del nuevo director", 
                                        criterios= criteriosDir,
                                        tituloValores = "Ingrese su respuesta <3",  
                                        valores = valoresDir,
                                        combobox=False,
                                        command = lambda: (fieldframedir.gatherEntries(), process_director_nuevo(fieldframedir.valores[0], fieldframedir.valores[1], fieldframedir.valores[2])))
                fieldframedir.pack(pady=10, fill="both", expand=True)
                name_str = ""
            elif actor == None:
                messagebox.showerror("Error", "El actor que ingresaste no existe en nuestra base de datos :(")
                name_str = ""
                step_create_obra(name_str)
            else:
                obra = Obra(nombre = name_str, reparto = [actor], papeles = [aptitud], genero  = genero, director = director,
                        costoProducción= costo, duracion = duracion)
                messagebox.showinfo("Completado", "La obra ha sido creada, para añadir funciones corra de nuevo la funcionalidad y selecciónela")
                name_str = ""

        def process_director_nuevo(name, id, genero):
            director = Director(name, id, genero)
            messagebox.showinfo("Completado", "El director ha sido creado, vuelva a ejecutar la funcionalidad para crear la obra")
        # -------------------- PASO 5: Artista encontrado --------------------
        '''Avalada'''
        def step_obra_found(obra):
            for widget in process_frameO.winfo_children():
                widget.destroy()
            fieldframe = FieldFrame(process_frameO,
                                    tituloCriterios = "",
                                    criterios = ["Número de funciones"],
                                    valores = [""],
                                    command = lambda: (fieldframe.gatherEntries(), createFunciones(obra, fieldframe.valores[0])))
            fieldframe.pack(pady=10, fill="both", expand=True)
            
        def createFunciones(obra, numero):
            a = obra.getFuncionesRecomendadas()
            continuar = False
            drut = 0
            rut = int(numero)
            def getWeek():
                hoy = datetime.now()
                dias = []
                for pio in range(1, 8):
                    dias.append(hoy + timedelta(days = pio))
                return dias

            if a + 2 < rut:
                messagebox.showwarning("ALERTA", "SON DEMASIADAS FUNCIONES SEGUN LA CALIFICACION DE LA OBRA")
                step_obra_found(obra)
                continuar = True
                drut = rut
            elif a - 2 > rut:
                messagebox.showwarning("ALERTA", "SON MUY POCAS FUNCIONES SEGUN LA CALIFICACION DE LA OBRA")
                step_obra_found(obra)
                continuar = True
                drut = rut
            else:
                continuar = True
                drut = rut  # Acepta si la cantidad es adecuada
            cantFunciones = 0
            for numeroFunciones in range(0, drut, 1):
                weekn = getWeek()
                funcion = Funcion(obra = obra, week = weekn)
                obra.addFuncion(funcion)
                if funcion.getSala() is not None:
                    for widget in process_frameO.winfo_children():
                        widget.destroy()
                    etiqueta = tk.Label(process_frameO, 
                                        text = f"Funcion creada\nHora:  {funcion.getHorario()}\nSala: {funcion.getSala()}",
                                        font=("Calibri", 14),
                                        bg = "#701C1A", fg = "#FCE6C1")
                    etiqueta.pack()
                    cantFunciones += 1
                else:
                    for widget in process_frameO.winfo_children():
                        widget.destroy()
                    etiqueta = tk.Label(process_frameO, 
                                        text = f"No queda espacio en las salas para esta función :(, creadas con éxito: {cantFunciones}",
                                        font=("Calibri", 14),
                                        bg = "#701C1A", fg = "#FCE6C1")
                    etiqueta.pack()
                    break
            
            horarioToString = ""
            dias = []
            hoy = datetime.now()
            for pio in range(1, 8):
                dias.append(hoy + timedelta(days = pio))

            # Crear un formato para imprimir fechas y horas
            formatoFecha = "%d/%m/%Y"
            formatoHora = "%H:%M"

            for sala in Teatro.getInstancia().getSalas():
                horarioToString += f"Horario para sala {sala.get_numero_sala()}:\n"
                
                # Crear columnas para los 7 días
                columnasDias = [[] for _ in range(7)]

                # Filtrar y organizar las funciones de esta sala
                funcionesSala = []
                for funcion in Teatro.getInstancia().getFuncionesCreadas():
                    if funcion.getObra() is not None and funcion.getSala() is not None and funcion.getSala() == sala:
                            funcionesSala.append(funcion)

                # Distribuir funciones en los días correspondientes
                for funcion in funcionesSala:
                    for pou in range(len(dias)):
                        inicioDia = dias[pou]
                        finDia = inicioDia + timedelta(days = 1)

                        if inicioDia < funcion.getHorario()[0] and funcion.getHorario()[0]<finDia:
                            columnasDias[pou].append(
                                f"{funcion.getObra().getNombre()} ({funcion.getHorario()[0].strftime(formatoHora)} - {funcion.getHorario()[1].strftime(formatoHora)})"
                            )
                            break

                for diaFunciones in columnasDias:
                    diaFunciones.sort(key=lambda f: datetime.strptime(f[f.index("(") + 1:f.index(" -")], formatoHora))

                # Imprimir el horario en columnas
                for coo in range(7):
                    horarioToString += f"Día {dias[coo].strftime(formatoFecha)}:\n"
                    for detalleFuncion in columnasDias[coo]:
                        horarioToString += f"   {detalleFuncion}\n"
                etiqueta = tk.Label(process_frameO, 
                                    text = horarioToString,
                                    bg = "#701C1A", fg = "#FCE6C1")
                etiqueta.pack(side = "left", padx = 1)
                horarioToString = ""
        step1Obras()



    @classmethod
    def contratarActores(cls) -> None:
        """Menú con opciones para contratar un actor, filtrando por características y presupuesto."""

        #limpiar frame
        for widget in cls.content.winfo_children():
            widget.destroy()
        
        #frame izquierdo
        leftFrame = tk.Frame(cls.content, bg="blue")
        leftFrame.place(relx=0, rely=0, relwidth=0.175, relheight=0.9)

        #frame derecho
        rightFrame = tk.Frame(cls.content, bg="blue")
        rightFrame.place(relx=0.825, rely=0, relwidth=0.175, relheight=0.9)
        
        #frame inferior
        bottomFrame = tk.Frame(cls.content, bg="pink")
        bottomFrame.place(relx=0, rely=0.9, relheight=0.2, relwidth=1)

        #frame central, donde irán todos los fieldframes
        centerFrame = tk.Frame(cls.content, bg="#4B2D2E", padx=20, pady=20)
        centerFrame.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)
        
        #frame superior, que lleva el mensaje de bienvenida a la funcionalidad
        captionFrame = Frame(cls.content,background="black")
        captionFrame.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)

        #mensaje de bienvenida
        caption = tk.Label(captionFrame, 
                            text="Bienvenido al panel de contratación de actores.",
                            font= ("Calibri", 10),
                            bg="#070709",
                            fg = "#FCE6C9")
        caption.place(relx = 0, rely = 0, relheight= 1, relwidth= 1)
        
        #reasignación de tamaño de letra
        captionFrame.bind(
            "<Configure>",
            lambda e: cls.resize(captionFrame, caption, 10, 60, False)
        )

        #configurar el crecimiento adaptable de las columnas del frame central
        centerFrame.columnconfigure(0, weight=1) 
        centerFrame.columnconfigure(1, weight=1)

        '''IMAGEN BOTTOM (ASIENTOS)'''
        # Cargar la imagen original (asegúrate de que el archivo se encuentre en el mismo directorio)
        imagen_bottom = Image.open("src/media/Theme/bottom.png")  
        image = ImageTk.PhotoImage(imagen_bottom)

        # Crear un Label que contendrá la imagen y que cubra todo el bottomFrame
        bottom_label = tk.Label(bottomFrame, image=image)
        bottom_label.place(relheight=1, relwidth=1)

        # Vincular el evento <Configure> usando lambda para pasar la imagen y el label a la función
        bottomFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_bottom, bottom_label))

        '''IMAGEN RIGHT (CORTINA DER)'''
        imagen_right = Image.open("src/media/Theme/Courtain right.png")  
        image_der = ImageTk.PhotoImage(imagen_right)

        right_label = tk.Label(rightFrame, image=image_der, bg="black")
        right_label.place(relheight=1, relwidth=1)

        rightFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_right, right_label))

        '''IMAGEN LEFT (CORTINA IZQ)'''

        imagen_left = Image.open("src/media/Theme/Courtain left.png")  
        image_izq = ImageTk.PhotoImage(imagen_left)

        left_label = tk.Label(leftFrame, image=image_izq, bg="black")
        left_label.place(relheight=1, relwidth=1)

        leftFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_left, left_label))
        
        #PREGUNTA NO. 1
        criteriosTipoEmpresa = ["Tipo de Empresa"]
        valoresTipoEmpresa = [["Empresa registrada", "Empresa nueva"]]

        #variables globales a ser modificadas
        actorsForRental = None 
        historialEmpresa = None
        empresa = None
        fechaInicio = None
        fechaFin = None
        duration = None
        
        CALIFICACION_ALTA = 4

        #def nullInEntries(fieldframe: FieldFrame) -> bool:
        #    entries = [entry.get() for i, entry in enumerate(fieldframe.values) if i > 0]
        #    for entry in entries:
        #        if entry == "" or entry is None:
        #            return True
        #F    return False

        def mostrarActores(fieldframe: FieldFrame, topFrame: Frame) -> None:
            """Se toma el presupuesto del fieldframe de entrada y muestra los actores que se pueden contratar.\n
            Una vez se elija el actor, se realiza el pago a Tesorería y se aisgna al horario del actor la fecha establecida."""

            global actorsForRental
            global duration
            global empresa
            global fechaInicio
            global fechaFin
            
            try:
                presupuesto = parseNumber(fieldframe, "Presupuesto", float)
            except errorEntradaNoNumerica:
                messagebox.showerror("Error", errorEntradaNoNumerica())
                return
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return

            
            actorsForRental = list(filter(lambda actor: actor.getPrecioContrato(duration) <= presupuesto, actorsForRental))

            if len(actorsForRental) == 0:
                messagebox.showerror("Error", "No se hallaron actores para el presupuesto")
                Main.contratarActores()
            else:

                actores = FieldFrame(
                    centerFrame,
                    tituloCriterios= "Escoger actor",
                    tituloValores= "Respuesta",
                    tituloGuardar= "Contratar",
                    criterios= ["Actor"],
                    valores = [[str(actor) for actor in actorsForRental]],
                    combobox= True,
                    command = lambda: actorEscogido(actores)
                )
                actores.place(relheight=1, relwidth=1)

                def actorEscogido(fieldframe: FieldFrame):

                    if cls.filterDebug:
                        print(fechaInicio, fechaFin)

                    try:
                        fieldframe.gatherEntries()
                    except errorEntradaNula:
                        messagebox.showerror("Error", errorEntradaNula())
                        return

                    actorNames = [str(actor) for actor in actorsForRental]
                    actorEscogido: Actor = actorsForRental[actorNames.index(fieldframe.getValue("Actor"))]
                    edad = actorEscogido.getEdad()
                    precio = actorEscogido.getPrecioContrato(duration)
                    calificacion = actorEscogido.getCalificacion()
                    id = actorEscogido.getId()

                    contratar = messagebox.askyesno("Contratación de actores", 
                                        f"Actor seleccionado:\n\nNombre: {actorEscogido}\nEdad: {edad}\nCalificación: {calificacion}\nPrecio de contratación: {Main.toCop(precio)}\n\n¿Desea contratarlo?")
                    print(contratar)
                    if contratar:
                        actor = Artista.buscarPorId(id)
                        empresa.getCuentaBancaria().ingresar(float(precio))
                        empresa.pagarContratoActor(actor, float(precio))
                        actor.getHorario().append((fechaInicio, fechaFin))


                        if cls.filterDebug:
                            print("horario nuevo", actor.getHorario())

                        messagebox.showinfo("Operación exitosa", f"¡Actor contratado!\n\nEl actor escogido fue {actorEscogido} por un precio de {Main.toCop(precio)}")
                        Main.contratarActores()
                

        def presupuesto(topFrame: Frame) -> None:
            """Toma el mínimo y máximo posible de precio de contratación para los actores filtrados, y pide al usuario el presupuesto."""

            global actorsForRental
            global duration

            minActorPrecio = min(actorsForRental, key= lambda actor: actor.getPrecioContrato(duration)).getPrecioContrato(duration)
            maxActorPrecio = max(actorsForRental, key= lambda actor: actor.getPrecioContrato(duration)).getPrecioContrato(duration)

            messagebox.showinfo("Información", "Antes de elegir el presupuesto de contratación, tenga en cuenta que el rango de los precios es de " + Main.toCop(minActorPrecio) + " a " + Main.toCop(maxActorPrecio))

            presupuesto = FieldFrame(
                topFrame,
                tituloCriterios= "Precio de contratación",
                tituloValores= "Respuesta",
                criterios= ["Presupuesto"],
                valores= [""],
                command= lambda: mostrarActores(presupuesto, topFrame)
            )

            presupuesto.place(relheight= 1, relwidth= 1)


        def preseleccion(topFrame: Frame, avanzado = False) -> None:
            """Ocurre después del filtrado, si quedan actores, especificar cuántos hay y reordenarlos, priorizando aquellos que hayan trabajado previamente con la empresa."""

            global actorsForRental
            global historialEmpresa

            if cls.filterDebug:
                print("historial de la empresa", [actor.getNombre() for actor in historialEmpresa])
            
            if len(actorsForRental) == 0:
                messagebox.showerror("Error", "No hay artistas disponibles con los requerimientos pedidos.")
                Main.contratarActores()
            else:
                if not avanzado:
                    messagebox.showinfo("Operación exitosa", str(len(actorsForRental)) + " actor/es encontrado/s durante la preselección")
                
                actorsForRental.sort(key=lambda actor: actor not in historialEmpresa)

                if cls.filterDebug:
                    print("lista reordenada", [actor.getNombre() for actor in actorsForRental])

                presupuesto(topFrame)


        def filtradoAvanzado(fieldframe: FieldFrame, topFrame: Frame) -> None:
            """Realiza el filtrado de búsqueda avanzada, tomando las respuestas del fieldframe"""

            global actorsForRental

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return

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
                Main.contratarActores()
            else:
                messagebox.showinfo("Operación exitosa", str(len(contadores)) + " actor/es se ajustaron a una o más características avanzadas.")
                contadorActores = [tupla[0] for tupla in contadores]

                if cls.filterDebug:
                    print("actores que aparecen al menos una vez en el contador", [actor.getNombre() for actor in contadorActores])

                actorsForRental = contadorActores
                preseleccion(topFrame, avanzado= True)


        def busquedaAvanzada(topFrame: Frame) -> None:
            """Realiza las preguntas de búsqueda avanzada, para un posterior filtrado en la función filtradoAvanzado."""

            global actorsForRental

            edad = FieldFrame(
                topFrame,
                tituloCriterios= "Búsqueda avanzada",
                tituloValores= "Respuestas",
                criterios= ["Intervalo de edad", "Sexo"],
                valores = [["Infantil", "Juvenil", "Adulto", "Adulto mayor"], 
                            ["Masculino", "Femenino"]],
                combobox= True,
                command= lambda: filtradoAvanzado(edad, topFrame),
                tituloGuardar= "Encontrar actores"
            )

            edad.place(relheight= 1, relwidth= 1)

        def setSchedule(fieldframe: FieldFrame, fecha: str, topFrame: str) -> None:
            """Toma las entradas de un fieldframe que incluyan hora de inicio y fin de contratación, y revisa si el horario cumple con los lineamientos."""

            global actorsForRental
            global duration
            global fechaInicio
            global fechaFin

            if cls.filterDebug:
                print("al entrar a setSchedule", [actor.getNombre() for actor in actorsForRental])

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return
            
            horaInicio = fieldframe.values[1].get()
            horaFin = fieldframe.values[2].get()

            try:
                fecha, horaInicio, horaFin = Main.validar_formatos(fecha, horaInicio, horaFin)
            except errorFormatoHorario:
                messagebox.showerror("Error", errorFormatoHorario())
                return

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


        def askSchedule(fecha: str, topFrame: Frame) -> None:
            """Pide al usuario las horas de inicio y fin del contrato."""

            global actorsForRental

            actorsForRental = actorsForRental
            
            schedule = FieldFrame(
                topFrame,
                criterios = ["Hora de inicio", "Hora de fin"],
                tituloCriterios = "Horario de actor",
                tituloValores = "Respuesta",
                valores = ["", ""],
                command= lambda: setSchedule(schedule, fecha, topFrame),
                tituloGuardar="Continuar"
            )

            schedule.place(relheight= 1, relwidth= 1)

            if cls.filterDebug:
                print("al terminar askSchedule", [actor.getNombre() for actor in actorsForRental])


        def filtrado(fieldframe: FieldFrame) -> None:
            """Toma las entradas del usuario en el fieldframe y realiza la primera ronda de filtrado."""

            global actorsForRental

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return

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



        def initPrimeraRonda(topframe: Frame) -> None:
            """Genera el fieldframe que da inicio a la funcionalidad, para el filtrado con la primera ronda de preguntas."""

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
                combobox= True,
                tituloGuardar = "Continuar",
            )

            primeraRonda.place(relwidth= 1, relheight= 1)

        def parseNumber(fieldframe : FieldFrame, value: str, cls = int) -> int | float:
            """Revisa si una entrada especfica de un fieldframe puede convertirse a entero"""

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return

            ans = fieldframe.getValue(value)

            if not ans.isnumeric():
                raise errorEntradaNoNumerica()

            ans = cls(ans)
            return ans
            
        def idExists(id: int) -> Cliente | bool:
            """Revisa si un número de identificación existe en la base de datos, y en caso de que exista, si es de tipo Empresa."""
            for cliente in Teatro.getInstancia().getClientes():
                if cliente.getId() == id and cliente.getTipo() == "Empresa":
                    return cliente
            return False
        
        def createId(fieldframe: FieldFrame) -> None:
            """Crea un número de identificación en caso de que no exista"""

            global empresa
            global historialEmpresa

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return

            try:
                id = parseNumber(fieldframe, "Generar nuevo ID", int)
            except errorEntradaNoNumerica:
                messagebox.showerror("Error", errorEntradaNoNumerica())
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())

            if id is None: 
                return

            cliente = idExists(id)

            if not cliente:
                empresa = Cliente(id= id, tipo = "Empresa", cuenta_bancaria= CuentaBancaria(id, 0))
                historialEmpresa = empresa.getHistorial()
                messagebox.showinfo("Operación exitosa", "Cliente nuevo agregado a la base de datos")
                initPrimeraRonda(centerFrame)

            else:
                raise errorIdExiste

        def locateId(fieldframe: FieldFrame) -> None:
            """Busca si un determinado número de identificaición existe"""

            global empresa
            global historialEmpresa
            id = None

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return

            try:
                id = parseNumber(fieldframe, "Inserte ID existente", int)
            except errorEntradaNoNumerica:
                messagebox.showerror("Error", errorEntradaNoNumerica())
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())

            if id is None:
                return
            
            cliente = idExists(id)
            
            if cliente:
                messagebox.showinfo("Operación exitosa", "Cliente confirmado en base de datos")
                historialEmpresa = cliente.getHistorial()
                empresa = cliente
                initPrimeraRonda(centerFrame)
            else:
                raise errorIdNoExiste
            
        def auth(fieldframe: FieldFrame, clientExists: bool) -> None:
            if clientExists:
                try:
                    locateId(fieldframe)
                except errorIdNoExiste:
                    messagebox.showerror("Error", errorIdNoExiste())
            else:
                try:
                    createId(fieldframe)
                except errorIdExiste:
                    messagebox.showerror("Error", errorIdExiste())

        def definirTipoEmpresa(fieldframe: FieldFrame, topFrame: Frame) -> None:
            """Antes de empezar con el filtrado, se elige si el cliente que va a llevar a cabo la contratación existe en la base de datos o es nuevo."""

            try:
                fieldframe.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())
                return

            choice = fieldframe.getValue("Tipo de Empresa")
            if choice in ["Empresa registrada", "Empresa nueva"]:
                tk.Label(topFrame, text= "Opción escogida: " + choice).pack()
                
                if choice == "Empresa registrada":
                    idFrame = FieldFrame(topFrame, 
                                    criterios= ["Inserte ID existente"], 
                                    tituloCriterios= "", 
                                    tituloValores= "", 
                                    valores = [""],
                                    command= lambda: auth(idFrame, clientExists= True),
                                    tituloGuardar= "Iniciar Sesión")
                    idFrame.place(relwidth= 1, relheight= 1)
                    
                elif choice == "Empresa nueva":
                    idFrame = FieldFrame(topFrame,
                                    criterios= ["Generar nuevo ID"], 
                                    tituloCriterios= "", 
                                    tituloValores= "", 
                                    valores = [""],
                                    command= lambda: auth(idFrame, clientExists= False),
                                    tituloGuardar= "Crear cuenta")
                    idFrame.place(relwidth= 1, relheight= 1)

        pregunta1 = FieldFrame(root = centerFrame, 
                                criterios = criteriosTipoEmpresa,
                                valores = valoresTipoEmpresa,
                                combobox= True,
                                command= lambda: definirTipoEmpresa(pregunta1, centerFrame))

        pregunta1.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)

















    @classmethod
    def gestionClases(cls):
        for widget in cls.content.winfo_children():
            widget.destroy()

        # --- FRAME DE BIENVENIDA ---
        '''AVALADA'''
        
        #frame izquierdo
        leftFrame = tk.Frame(cls.content, bg="blue")
        leftFrame.place(relx=0, rely=0, relwidth=0.175, relheight=0.9)

        #frame derecho
        rightFrame = tk.Frame(cls.content, bg="blue")
        rightFrame.place(relx=0.825, rely=0, relwidth=0.175, relheight=0.9)
        
        #frame inferior
        bottomFrame = tk.Frame(cls.content, bg="pink")
        bottomFrame.place(relx=0, rely=0.9, relheight=0.2, relwidth=1)

        frame_marco = tk.Frame(cls.content, bg="#4B2D2E", padx=20, pady=20)
        frame_marco.place(relx=0.175, rely=0.1, relwidth=0.65, relheight=0.8)

        # --- FRAME PRINCIPAL PARA EL PROCESO ---
        process_frame = Frame(frame_marco, bg="#701C1A", padx=20, pady=20)
        process_frame.place(relwidth= 1, relheight= 1)
        
        frame_bienvenida = Frame(cls.content, bg="red")
        frame_bienvenida.place(relx=0, rely=0, relwidth= 1, relheight= 0.1)
        saludo = tk.Label(frame_bienvenida,
                            text="Gestion de clases",
                            font=("Calibri", 16),
                            bg="#070709", fg="#FCE6C9")
        saludo.place(relx=0, rely=0, relwidth=1, relheight=1)
        frame_bienvenida.bind(
            "<Configure>",
            lambda e: cls.resize(frame_bienvenida, saludo, 10, 60, False)
        ) 

        '''IMAGEN BOTTOM (ASIENTOS)'''
        # Cargar la imagen original (asegúrate de que el archivo se encuentre en el mismo directorio)
        imagen_bottom = Image.open("src/media/Theme/bottom.png")  
        image = ImageTk.PhotoImage(imagen_bottom)

        # Crear un Label que contendrá la imagen y que cubra todo el bottomFrame
        bottom_label = tk.Label(bottomFrame, image=image)
        bottom_label.place(relheight=1, relwidth=1)

        # Vincular el evento <Configure> usando lambda para pasar la imagen y el label a la función
        bottomFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_bottom, bottom_label))

        '''IMAGEN RIGHT (CORTINA DER)'''
        imagen_right = Image.open("src/media/Theme/Courtain right.png")  
        image_der = ImageTk.PhotoImage(imagen_right)

        right_label = tk.Label(rightFrame, image=image_der, bg="black")
        right_label.place(relheight=1, relwidth=1)

        rightFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_right, right_label))

        '''IMAGEN LEFT (CORTINA IZQ)'''

        imagen_left = Image.open("src/media/Theme/Courtain left.png")  
        image_izq = ImageTk.PhotoImage(imagen_left)

        left_label = tk.Label(leftFrame, image=image_izq, bg="black")
        left_label.place(relheight=1, relwidth=1)

        leftFrame.bind("<Configure>", lambda event: Main.resize_image(event, imagen_left, left_label))

        # -------------------- PASO 1: Mostrar Artistas y solicitar ID -------------------- 
        '''AVALADA'''
        def step1():
            for widget in process_frame.winfo_children():
                widget.destroy()

            artistas = Teatro.getInstancia().getArtistas()
            if artistas:
                lbl_artistas = tk.Label(process_frame,
                                    text="Artistas existentes en la base de datos:",
                                    font=("Calibri", 14),
                                    bg="#701C1A", fg="#FCE6C9")
                lbl_artistas.pack(pady=10, fill="x")
                txt_artistas = tk.Text(process_frame,
                                height=6, width=80,
                                font=("Calibri", 12),
                                bg="#701C1A", fg="#FCE6C9")
                txt_artistas.pack(pady=10, fill="both", expand=True)
                for artista in artistas:
                    if isinstance(artista, Actor):
                        linea = f"- Actor {artista.getNombre()} con ID {artista.getId()}\n"
                    else:
                        linea = f"- Director {artista.getNombre()} con ID {artista.getId()}\n"
                    txt_artistas.insert("end", linea)
                txt_artistas.config(state="disabled")
            else:
                tk.Label(process_frame,
                        text="No hay artistas en la base de datos.",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C9").pack(pady=10, fill="x")
                return

            lbl_id = tk.Label(process_frame,
                    text="Ingrese el ID del artista para gestionar clases:",
                    font=("Calibri", 14),
                    bg="#701C1A", fg="#FCE6C9")
            lbl_id.pack(pady=10, fill="x")
            entry_id = tk.Entry(process_frame, font=("Calibri", 14))
            entry_id.pack(pady=5)
            btn_buscar = tk.Button(process_frame,
                                text="Buscar",
                                font=("Calibri", 14),
                                bg="#701C1A", fg="#FCE6C9",
                                command=lambda: process_artist(entry_id.get()))
            btn_buscar.pack(pady=10)

            # Se asocia el evento de resize al label (puedes hacerlo a otros widgets según convenga)
            Main.resize(process_frame, lbl_artistas, 14, 60, True)

        # -------------------- PASO 2: Procesar el ID ingresado --------------------
        '''AVALADA'''
        def process_artist(id_str):
            try:
                id_num = int(id_str)
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")
                return
            artista = Artista.buscarPorId(id_num)
            if artista is None:
                step_artist_not_found(id_num)
            else:
                step_artist_found(artista)

        # -------------------- PASO 3: Artista no encontrado --------------------
        '''AVALADA'''
        def step_artist_not_found(id_num):
            for widget in process_frame.winfo_children():
                widget.destroy()
            tk.Label(process_frame,
                text=f"Artista con ID {id_num} no encontrado.",
                font=("Calibri", 14),
                bg="#701C1A", fg="#FCE6C1").pack(pady=10, fill="x")
            tk.Label(process_frame,
                    text="¿Desea crear un nuevo Artista con este ID?",
                    font=("Calibri", 14),
                    bg="#701C1A", fg="#FCE6C1").pack(pady=10, fill="x")
            tk.Button(process_frame,
                    text="Sí",
                    font=("Calibri", 14),
                    bg="#701C1A", fg="#FCE6C1",
                    width=10,
                    command=lambda: step_create_artist(id_num)).pack(pady=5)
            tk.Button(process_frame,
                    text="No",
                    font=("Calibri", 14),
                    bg="#701C1A", fg="#FCE6C1",
                    width=10,
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
                        font=("Calibri", 20), bg="#701C1A", fg="#FCE6C1").pack(pady=10)
            else:
                tk.Label(process_frame,
                        text="Obras en estado crítico del teatro:",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C1").pack(pady=10, fill="x")
                txt_obras = tk.Text(process_frame,
                                    height=8, width=80,
                                    font=("Calibri", 12),
                                    bg="#701C1A", fg="#FCE6C1")
                txt_obras.pack(pady=10, fill="both", expand=True)
                for obra in obras_criticas:
                    linea = f"- '{obra.getNombre()}' (Promedio: {obra.promedioCalificacion()})\n"
                    txt_obras.insert("end", linea)
                txt_obras.config(state="disabled")
            
            tk.Button(process_frame, text="Volver al inicio", font=("Calibri", 16), bg="#701C1A", fg="#FCE6C1",
                command=Main.gestionClases).pack(pady=10)

        # -------------------- PASO 4: Crear nuevo artista --------------------
        '''AVALADA'''
        def step_create_artist(id_num):
            for widget in process_frame.winfo_children():
                widget.destroy()
            # Configuramos los criterios y valores iniciales para ingresar el nombre y el tipo de artista
            criterios = ["ID", "Nombre", "Tipo de artista"]
            valores = [f"{id_num}", "", ""]  # valores vacíos inicialmente
            # Se crea el FieldFrame; al presionar "Guardar" se llamará a la función lambda
            # que invoca process_new_artist con los datos ingresados.
            ff = FieldFrame(process_frame,
                            tituloCriterios="Datos del nuevo artista",
                            criterios=criterios,
                            tituloValores="Ingrese valor",
                            valores=valores,
                            habilitado= ["Nombre", "Tipo de artista"],
                            combobox=False,
                            command=lambda: (process_new_artist(id_num, ff)))
            ff.pack(pady=10, fill="both", expand=True)
            tk.Label(process_frame,
                    text="(Si se ingresa 'actor' se pedirá la edad posteriormente)",
                    font=("Calibri", 12),
                    bg="#701C1A", fg="#FCE6C1").pack(pady=5, fill="x")

        def process_new_artist(id_num, ff):
            try:
                ff.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())

            nombre = ff.valores[1]
            tipo = ff.valores[2]
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
                Main.gestionClases()

            else:
                for widget in process_frame.winfo_children():
                    widget.destroy()
                tk.Label(process_frame,
                    text="Ingrese la edad del nuevo actor (entre 4 y 80):",
                    font=("Calibri", 14),
                    bg="#701C1A", fg="#FCE6C1").pack(pady=30, fill="x")
                entry_age = tk.Entry(process_frame, font=("Calibri", 14))
                entry_age.pack(pady=5)
                tk.Button(process_frame,
                        text="Guardar",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C1",
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
            if isinstance(artista, Director):
                messagebox.showinfo("Información","Los directores no reciben clase.")
                Main.gestionClases()
            else:
                for widget in process_frame.winfo_children():
                    widget.destroy()
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
                info_text = f"Calificaciones de profesores: {artista.getCalificacionesAptitudes()}\n"
                info_text += f"Calificaciones del público: {artista.getCalificacionesPublico()}\n"
                lbl_info = tk.Label(process_frame, text=info_text, font=("Calibri", 18), bg="#701C1A", fg="#FCE6C1")
                lbl_info.pack(pady=5)
                # Mostrar obras críticas
                tk.Label(process_frame, text="Obras en estado crítico del teatro:",
                        font=("Calibri", 14), bg="#701C1A", fg="#FCE6C1").pack(pady=10)
                obras = Obra.mostrarObrasCriticas()  # Se asume que este método existe
                if not obras:
                    tk.Label(process_frame, text="No hay obras en estado crítico.",
                            font=("Calibri", 14), bg="#701C1A", fg="#FCE6C1").pack(pady=5)
                else:
                    txt_obras = tk.Text(process_frame, height=6, width=80, font=("Calibri", 12),
                                bg="#701C1A", fg="#FCE6C1")
                    txt_obras.pack(pady=5, fill="both", expand=True)
                    for obra in obras:
                        linea = f"- '{obra.getNombre()}' (Promedio: {obra.promedioCalificacion()})\n"
                        txt_obras.insert("end", linea)
                    txt_obras.config(state="disabled")
                tk.Button(process_frame,
                        text="Programar clase",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C1",
                        width=13,
                        command=lambda: step_select_area(artista)).pack(pady=10)
                tk.Button(process_frame,
                        text="Volver al inicio",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C1",
                        width=13,
                        command=Main.gestionClases).pack(pady=10)

        # -------------------- PASO 6: Seleccionar área de mejora --------------------
        '''AVALADA'''
        def step_select_area(actor):
            for widget in process_frame.winfo_children():
                widget.destroy()
            areas_recomendadas = actor.obtenerAreasDeMejora()
            if not areas_recomendadas:
                step_select_custom_area(actor)
            else:
                txt_areas = tk.Text(process_frame, height=6, width=80, font=("Calibri", 12),
                                bg="#701C1A", fg="#FCE6C1")
                txt_areas.pack(pady=10, fill="both", expand=True)
                txt_areas.insert("end", "Áreas recomendadas para mejorar del actor " + actor.getNombre() + ":\n")
                for i, area in enumerate(areas_recomendadas[:3]):
                    cal = actor.getCalificacionPorAptitud(area)
                    txt_areas.insert("end", f"{i+1}. {area.name.capitalize()} (Calificación: {cal})\n")
                txt_areas.config(state="disabled")
                tk.Label(process_frame,
                        text="¿Desea programar una clase basada en las áreas recomendadas?",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C1").pack(pady=10, fill="x")
                tk.Button(process_frame,
                        text="Sí",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C1",
                        width=10,
                        command=lambda: step_schedule_class(actor, areas_recomendadas[0])).pack(pady=5)
                tk.Button(process_frame,
                        text="No",
                        font=("Calibri", 14),
                        bg="#701C1A", fg="#FCE6C1",
                        width=10,
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
                tk.Radiobutton(process_frame, text=area.name.capitalize(), variable=var_index,
                            value=i, font=("Calibri", 12), bg="#701C1A", fg='#FCE6C9', selectcolor="#4B2D2E").pack(anchor="w", padx=20)
            tk.Button(process_frame, text="Siguiente", font=("Calibri", 14),
                    command=lambda: step_schedule_class(actor, areas[var_index.get()])).pack(pady=10)

        # -------------------- PASO 8: Programar la clase (solicitar horario) --------------------
        '''AVALADA'''
        def step_schedule_class(actor, areaSeleccionada):
            for widget in process_frame.winfo_children():
                widget.destroy()
            # Determinar el nivel de clase según la calificación actual
            calificacionActual = actor.getCalificacionPorAptitud(areaSeleccionada)
            if calificacionActual < 3.0:
                nivelClase = "Introducción"
            elif calificacionActual < 4.0:
                nivelClase = "Profundización"
            else:
                nivelClase = "Perfeccionamiento"
            
            # Mostrar solo el nombre de la aptitud (sin el prefijo "Aptitud.")
            # Si el objeto es un enum, se usará su atributo 'name'
            area_display = areaSeleccionada.name.capitalize() if hasattr(areaSeleccionada, "name") else str(areaSeleccionada).split('.')[-1].capitalize()

            
            tk.Label(process_frame,
                    text=f"Área seleccionada: {area_display}\nNivel de clase: {nivelClase}",
                    font=("Calibri", 14), bg="#701C1A", fg="#FCE6C1").pack(pady=10)
            
            tk.Label(process_frame, text="Programe la clase:", font=("Calibri", 14), bg="#701C1A", fg="#FCE6C1").pack(pady=5)
            
            # Obtener la lista de días de la semana con getWeek()
            week_days = Main.getWeek()  # Retorna una lista de objetos date
            day_options = [day.strftime("%Y-%m-%d") for day in week_days]
            
            # Crear un único FieldFrame para ingresar Día, Hora de inicio y Hora de fin.
            # Se pasan tres criterios y tres valores (el primero es una lista de opciones para el día).
            ff = FieldFrame(process_frame,
                            tituloCriterios="Programación de Clase",
                            criterios=["Día", "Inicio", "Fin"],
                            tituloValores="Valor",
                            valores=[day_options, "", ""],
                            combobox=False,
                            tituloGuardar="Programar",
                            command=lambda: (
                        process_schedule(actor, areaSeleccionada, nivelClase, ff))
                    )
            ff.pack(pady=10, fill="x")
            
            # Por defecto, FieldFrame crea entradas (Entry) para todos los campos.
            # Convertimos la entrada correspondiente a "Día" (el primer campo) en un Combobox.
            ff.values[1].destroy()  # ff.values[0] es el título de la columna de valores, ff.values[1] corresponde al primer campo
            ff.values[1] = ttk.Combobox(ff, values=day_options)
            ff.values[1].grid(row=1, column=2)

        # -------------------- PASO 9: Procesar horario y asignar sala y profesor --------------------
        '''AVALADA'''
        def process_schedule(actor, areaSeleccionada, nivelClase, ff):
            try:
                ff.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())

            day_str=ff.valores[0]
            start_time_str=ff.valores[1]
            end_time_str=ff.valores[2]

            try:
                horarios = Main.validar_formatos(day_str,start_time_str,end_time_str)
            except errorFormatoHorario:
                messagebox.showerror("Error", errorFormatoHorario())
                return

            # Combinar la fecha con las horas para obtener datetime completos
            inicio = datetime.combine(horarios[0], horarios[1])
            fin = datetime.combine(horarios[0], horarios[2])

            if fin <= inicio:
                messagebox.showerror("Error", "El fin debe ser después del inicio.")
                return
            duration = (fin - inicio).total_seconds() / 3600
            if duration < 2 or duration > 4:
                messagebox.showerror("Error", "La duración debe ser entre 2 y 4 horas.")
                return
            # Validar que las clases se programen entre las 10:00 y las 22:00
            if not (10 <= inicio.hour < 22 and 10 < fin.hour <= 22):
                messagebox.showerror("Error", "Las clases deben programarse entre las 10:00 y las 22:00.")
                return
            # Buscar una sala disponible
            salaAsignada = None
            for sala in Teatro.getInstancia().getSalas():
                if sala.get_aseado() and sala.is_disponible(inicio, fin):
                    salaAsignada = sala
                    break
            if salaAsignada is None:
                messagebox.showerror("Error", "No hay salas disponibles en el horario deseado o no están limpias.")
                for widget in process_frame.winfo_children():
                    widget.destroy()
                Main.gestionClases()
                return
            salaAsignada.anadir_horario([inicio, fin])
            # Selección de profesor especializado (simulación de disponibilidad)
            profesorAsignado = None
            profesores = Teatro.getInstancia().getTipoProfesor()
            random.shuffle(profesores)
            for empleado in profesores:
                if isinstance(empleado, Profesor) and empleado.tiene_especializacion(areaSeleccionada):
                    if random.random() > 0.5:
                        profesorAsignado = empleado
                        break
            if profesorAsignado is None:
                for widget in process_frame.winfo_children():
                    widget.destroy()
                messagebox.showerror("Error", "No hay profesores disponibles con especialización en el área seleccionada o están ocupados.")
                Main.gestionClases()
                return
            msg = f"Sala asignada: {salaAsignada.get_numero_sala()}\nProfesor asignado: {profesorAsignado.getNombre()}\n"
            messagebox.showinfo("Clase Programada", msg)
            step_payment(actor, areaSeleccionada, nivelClase, profesorAsignado, fin)

        # -------------------- PASO 10: Procesar pago y evaluación --------------------
        '''AVALADA'''
        def step_payment(actor, areaSeleccionada, nivelClase, profesorAsignado, fin):
            for widget in process_frame.winfo_children():
                widget.destroy()
            if nivelClase == "Introducción":
                costoClase = 50000
            elif nivelClase == "Profundización":
                costoClase = 75000
            else:
                costoClase = 90000
            tk.Label(process_frame, text=f"El costo de la clase es: {Main.toCop(costoClase)}",
                    font=("Calibri", 14), bg="#701C1A", fg="#FCE6C1").pack(pady=10)
            tk.Button(process_frame, text="Procesar Pago", font=("Calibri", 14),
                    bg="#701C1A", fg="#FCE6C1",
                    command=lambda: process_payment(actor, costoClase, areaSeleccionada,
                                                    profesorAsignado, nivelClase, fin)).pack(pady=10)

        def process_payment(actor, costoClase, areaSeleccionada, profesorAsignado, nivelClase, fin):
            if actor.getCuenta().retirar(costoClase):
                tesoreria = Teatro.getInstancia().getTesoreria()
                tesoreria.setTotal(tesoreria.getTotal() + costoClase)
                tesoreria.setDineroEnCaja(tesoreria.getDineroEnCaja() + costoClase)
                messagebox.showinfo("Pago", "Pago procesado exitosamente.")

                # Selección de profesor evaluador (simulación)
                profesor_evaluador = None
                profesores = Teatro.getInstancia().getTipoProfesor()
                random.shuffle(profesores)
                for empleado in profesores:
                    if isinstance(empleado, Profesor) and empleado.tiene_especializacion(areaSeleccionada):
                        if random.random() > 0.5:
                            profesor_evaluador = empleado
                            break

                if profesor_evaluador:
                    # Capturamos la nota inicial antes de la evaluación
                    initial_note = actor.getCalificacionPorAptitud(areaSeleccionada)
                    # Se genera la calificación (aleatoria en este ejemplo)
                    calificacion = round(random.random() * 5, 1)
                    messagebox.showinfo("Evaluación", 
                                        f"El profesor {profesor_evaluador.getNombre()} calificó al actor con un: {calificacion}")

                    # El profesor que imparte la clase siempre recibe los puntos positivos
                    puntos = 1 if nivelClase == "Introducción" else (2 if nivelClase == "Profundización" else 3)
                    profesorAsignado.agregar_puntos(puntos)
                    messagebox.showinfo("Puntos", 
                                        f"El profesor {profesorAsignado.getNombre()} ha recibido {puntos} puntos positivos por dictar la clase con nivel {nivelClase}.")

                    # Evaluamos las condiciones de mejora:
                    if calificacion < 3:
                        messagebox.showinfo("Evaluación", 
                            "El actor sacó una nota menor a 3. Se reprogramará la clase por falta de mejora.")
                        step_reprogramar(actor, areaSeleccionada, nivelClase, profesor_evaluador, fin)
                    elif calificacion <= initial_note:
                        messagebox.showinfo("Evaluación", 
                            "El actor no mejoró su calificación respecto al inicio de la clase. Se reprogramará la clase por falta de mejora.")
                        step_reprogramar(actor, areaSeleccionada, nivelClase, profesor_evaluador, fin)
                    else:
                        messagebox.showinfo("Proceso Finalizado", "La clase se ha realizado exitosamente.")
                        Main.gestionClases()
                else:
                    messagebox.showerror("Error", "No hay profesores disponibles para calificar la función.")
                    Main.gestionClases()
            else:
                messagebox.showerror("Error", "El actor cuenta con saldo insuficiente para pagar la clase.")
                Main.gestionClases()


        # -------------------- PASO 11: Reprogramar clase en caso de falta de mejora --------------------
        '''AVALADA'''
        def step_reprogramar(actor, areaSeleccionada, nivelClase, profesorEvaluador, fin):
            for widget in process_frame.winfo_children():
                widget.destroy()
            tk.Label(process_frame, text="Reprogramar clase por falta de mejora",
                    font=("Calibri", 14), bg="#701C1A", fg="#FCE6C1").pack(pady=10)
            
            # Obtener la lista de días de la semana con getWeek()
            week_days = Main.getWeek()  # Retorna una lista de objetos date
            day_options = [day.strftime("%Y-%m-%d") for day in week_days]
            
            # Se utiliza un único FieldFrame para recoger Día, Hora de inicio y Hora de fin
            ff = FieldFrame(process_frame,
                            tituloCriterios="Nueva Programación de Clase",
                            criterios=["Día", "Inicio", "Fin"],
                            tituloValores="Valor",
                            valores=[day_options, "", ""],
                            combobox=False,
                            tituloGuardar="Programar",
                            command=lambda: (
                                process_reprogramar(actor, areaSeleccionada,
                                                    nivelClase, profesorEvaluador, fin, ff)
                            ))
            ff.pack(pady=10, fill="x")
            # Convertir la entrada del primer campo ("Día") en un Combobox
            ff.values[1].destroy()  # ff.values[0] es el título; ff.values[1] corresponde al primer campo
            ff.values[1] = ttk.Combobox(ff, values=day_options)
            ff.values[1].grid(row=1, column=2)


        def process_reprogramar(actor, areaSeleccionada, nivelClase, profesorEvaluador, fin, ff):
            try:
                ff.gatherEntries()
            except errorEntradaNula:
                messagebox.showerror("Error", errorEntradaNula())

            day_str=ff.valores[0]
            start_time_str=ff.valores[1]
            end_time_str=ff.valores[2]

            try:
                horarios = Main.validar_formatos(day_str,start_time_str,end_time_str)
            except errorFormatoHorario:
                messagebox.showerror("Error", errorFormatoHorario())
                return

            nuevo_inicio = datetime.combine(horarios[0], horarios[1])
            nuevo_fin = datetime.combine(horarios[0], horarios[2])
            
            if nuevo_fin <= nuevo_inicio:
                messagebox.showerror("Error", "El fin debe ser después del inicio.")
                return
            if nuevo_inicio <= fin:
                messagebox.showerror("Error", "La nueva clase no puede iniciarse antes de finalizar la clase inicial.")
                return
            duration = (nuevo_fin - nuevo_inicio).total_seconds() / 3600
            if duration < 2 or duration > 4:
                messagebox.showerror("Error", "La duración debe ser entre 2 y 4 horas.")
                return
            # Validar que las clases se programen entre las 10:00 y las 22:00
            if not (10 <= nuevo_inicio.hour < 22 and 10 < nuevo_fin.hour <= 22):
                messagebox.showerror("Error", "Las clases deben programarse entre las 10:00 y las 22:00.")
                return

            # Buscar sala disponible
            salaAsignada = None
            for sala in Teatro.getInstancia().getSalas():
                if sala.get_aseado() and sala.is_disponible(nuevo_inicio, nuevo_fin):
                    salaAsignada = sala
                    break
            if salaAsignada is None:
                messagebox.showerror("Error", "No hay salas disponibles en el nuevo horario deseado o no están limpias.")
                Main.gestionClases()
                return
            salaAsignada.anadir_horario([nuevo_inicio, nuevo_fin])
            
            # Seleccionar profesor especializado (simulación)
            profesorAsignado = None
            import random
            profesores = Teatro.getInstancia().getTipoProfesor()
            random.shuffle(profesores)
            for empleado in profesores:
                if isinstance(empleado, Profesor) and empleado.tiene_especializacion(areaSeleccionada):
                    if random.random() > 0.5:
                        profesorAsignado = empleado
                        break
            if profesorAsignado is None:
                messagebox.showerror("Error", "No hay profesores disponibles para la nueva clase en el área seleccionada.")
                Main.gestionClases()
                return

            messagebox.showinfo("Clase Reprogramada",
                                f"Clase reprogramada con el profesor {profesorAsignado.getNombre()} en la sala {salaAsignada.get_numero_sala()}.")
            
            if actor.noHaMejoradoEnCuatroIntentos(areaSeleccionada):
                nuevaCalificacion = max(0, actor.getCalificacionPorAptitud(areaSeleccionada) - 1)
                actor.registrarCalificacion(areaSeleccionada, nuevaCalificacion)
                messagebox.showinfo("Reducción de Nivel", f"El nuevo nivel del área {areaSeleccionada.name.capitalize()} es: {nuevaCalificacion}")
            Main.gestionClases()
        # -------------------- Inicio del proceso: arranca por el Paso 1 --------------------
        step1()

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
import tkinter as tk
from tkinter import PhotoImage, messagebox
import tkinter.font as tkf
import tkinter.simpledialog as sm
import os
from BBDD import bbdd
from interfazChatBot import botReservas

class ventanaUsu:
    def __init__(self, usu) -> None:
        
        self.ventanap = tk.Toplevel()
        self.ventanap.title("Herramienta vacacional Alberto Horcajada")
        self.usu = usu
        self.__crearInterfaz()
        self.mes = None
        self.dia = None
        

    def __crearInterfaz(self):
        fstyle = tkf.Font(size=20)
        lblUser = tk.Label(self.ventanap, text="EMPLEADOS",font=fstyle)
        lblUser.grid(column=0, row=0, padx=10, pady=10, sticky="w", columnspan=2)
        lblUser.config(fg="#d6e75f")

        self.path_base = os.path.dirname(__file__)

        self.path_villablanca = os.path.join(self.path_base, 'villablanca.png')
        self.imgLvillablanca = PhotoImage(file=self.path_villablanca)
        self.villablanca = self.imgLvillablanca.subsample(6)

        tk.Label(self.ventanap,image=self.villablanca).grid(column=3, row=0 , padx=10, pady=10)

        tk.Canvas(self.ventanap, height=10, background="#d6e75f").grid(column=0, row=1, padx=10, pady=10, columnspan=4)

        self.path_lupa = os.path.join(self.path_base, 'lupa.png')
        self.imgLupa = PhotoImage(file=self.path_lupa)
        self.lupa = self.imgLupa.subsample(10)

        self.path_usuario = os.path.join(self.path_base, 'usuario.png')
        self.imgUsuario = PhotoImage(file=self.path_usuario)
        self.usuario = self.imgUsuario.subsample(20)

        self.path_salir = os.path.join(self.path_base, 'cruz.png')
        self.imgSalida = PhotoImage(file=self.path_salir)
        self.salida = self.imgSalida.subsample(10)

        btnLupa = tk.Button(self.ventanap, command=self.funcionLupa, image=self.lupa)
        btnLupa.grid(column=0, row=2, padx=10, pady=10, sticky="w")

        btnUsuario = tk.Button(self.ventanap,image= self.usuario, command=self.funcionReservarDias)
        btnUsuario.grid(column=1, row=2, padx=10, pady=10, sticky="w")

        btnSalir = tk.Button(self.ventanap, image=self.salida, command=self.salir)
        btnSalir.grid(column=2, row=2, padx=10, pady=10, sticky="w")

    def funcionLupa(self):
        miBase = bbdd()
        
        resultado = miBase.buscarInfoUsuario(usu=self.usu)
        msg = "mes\tdisponibles\tdisfrutados\n"
        for i in range(len(resultado)):
            msg+="\n" + resultado[i][1] +"\t\t" + str(resultado[i][2]) +"\t\t" + str(resultado[i][3])
        messagebox.showinfo(message=msg,title="Tu Historial de vacaciones")

    def funcionReservarDias(self):
        bot = botReservas(usu=self.usu)

    def salir(self):
        self.ventanap.destroy()

        

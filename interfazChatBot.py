'''
@Author Alberto Horcajada Perez
@version 1.0  created on 23/02//2022
'''

import tkinter as tk
import os
from tkinter import scrolledtext, PhotoImage, messagebox
from queue import Queue
from threading import Thread
from BBDD import bbdd
from servidorTCP import start_server as st
from clienteTCP import escribir_al_servidor_TCP as msng

class botReservas():
    def __init__(self, usu) -> None:
        self.usu = usu
        self.mes = None
        self.dias = None

        self.hilo_escucha_reserva = Thread(target=self.crearHiloEscuharReserva, daemon=True)
        self.hilo_escucha_reserva.start()

        self.hiloServidor = Thread(target=st, daemon=False)
        self.hiloServidor.start()
        
        self.ventana = tk.Toplevel()
        self.ventana.title("Chat con BOT")
        
        self.listaChat = Queue()
        
        self.path_base = os.path.dirname(__file__)
        self.path_ayuda = os.path.join(self.path_base, 'ayuda.png')
        self.imgAyuda = PhotoImage(file=self.path_ayuda)
        self.ayuda = self.imgAyuda.subsample(20)

        tk.Label(self.ventana, text="Reserva tus vacaciones").grid(column=0, row=0, padx=10, pady=10, sticky="w", columnspan=2)
        tk.Button(self.ventana, command=self.crearHiloAyuda, image=self.ayuda).grid(column=3, row=0, padx=10, pady=10, sticky="w")
        
        self.scrolledText = scrolledtext.ScrolledText(self.ventana, height=25, width=50, wrap=tk.WORD, state="disabled")
        self.scrolledText.grid(column=0, row=1, padx=10, pady=10, sticky="w", columnspan=2)

        self.mensaje = tk.StringVar()
        self.mensaje.set("")

        tk.Entry(self.ventana, textvariable=self.mensaje, width=50).grid(column=0, row=2, padx=10, pady=10, sticky="w")
        tk.Button(self.ventana, command=self.enviarMensaje, text="->", width=10).grid(column=1, row=2, padx=10, pady=10, sticky="w")

    def mostrarAyuda(self):
        ayuda = "Posibles mensajes con respuesta que puedes enviar:\n\n"
        ayuda += "1: Hola: el bot te responderá con educacion\n\n"
        ayuda += "2: Quiero reservar unas vacaciones: te pedira las tres primeras letras de un mes que reservar\n\n"
        ayuda += "3: Numero de dias a reservar (pasar un numero): te dira si es disponible reservarlo o no, depende de tus dias disponibles\n\n"
        ayuda += "4: Adios: el bot se despedirá de ti y te dará las gracias por todo"
        messagebox.showinfo(title="Necesitas Ayuda??", message=ayuda)

    def crearHiloEscuharReserva(self):
        while True:
            if(self.mes!=None):
                if(self.dias!=None):
                    self.ventana.destroy()
                    self.comprobarReserva()
                    break
                    
    
    def comprobarReserva(self):
        miBase = bbdd()
        print(self.dias)
        print(type(self.dias))
        if(miBase.hacerReserva(usu=self.usu, mes = self.mes, dias = int(self.dias))):
            messagebox.showinfo(title="Exito", message="disfrute usted de su reserva de vacaciones")
        else:
            messagebox.showerror(title="Error", message="Oh no, algo paso, no se ha podido hacer la reserva")
            
            
        

    def crearHiloAyuda(self):
        hilo_ayuda = Thread(target=self.mostrarAyuda, daemon=True)    
        hilo_ayuda.start()

    def enviarMensaje(self):
        msg = self.mensaje.get()
        if(msg!=""):
            self.listaChat.put(msg)
            msng(inst=self, mensaje=msg)
            self.mensaje.set("")
            self.hiloMostrarMensaje()
        else:
            messagebox.showerror(title="Error", message="No deje el mensaje vacio por favor")

    def hiloMostrarMensaje(self):
        hilo_MostrarMensaje = Thread(target=self.mostrarMensaje, daemon=True)
        hilo_MostrarMensaje.start()

    def mostrarMensaje(self):
        while True:
            msg = self.listaChat.get()
            msg+= "\n"
            self.scrolledText["state"]= "normal"
            self.scrolledText.insert(tk.INSERT, msg)
            self.scrolledText["state"]= "disabled"
            
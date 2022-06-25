'''
@Author Alberto Horcajada Perez
@Version 1.0   on 15 feb 2022
'''

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, PhotoImage
from BBDD import bbdd
from interfazAdmin import ventanaAdmin as vAdm
from interfazUsuario import ventanaUsu as vUsu
from time import sleep
from threading import Thread
import os

#Funcion con la que alterno la visibilidad de la contraseña
def mostrarPass():
    global visible
    visible = not(visible)
    if(visible):
        entryPass["show"]=""
    else:
        entryPass["show"]="*"
def iniciarSesion():
    global varPass, varUsu

    if(miBase.iniciarSesion(usuario=varUsu.get(), psswd=varPass.get())):
        if(miBase.isAdmin(usu=varUsu.get())):
            hiloAdmin = Thread(target=abrirVentanaAdministrador, daemon=True)
            hiloAdmin.start()
        else:
            hiloUser = Thread(target=abrirVentanaUser, daemon=True)
            hiloUser.start()
    else:
        messagebox.showerror(title="Error Inicio Sesion", message="Revise las credenciales")

def abrirVentanaAdministrador():
    admin = vAdm()
    sleep(290)
    messagebox.showerror(message="Tiempo expirado", title="Cierre de sesion")
    sleep(10)
    admin.salir()

def abrirVentanaUser():
    #El enunciado no pedia que se saliese de la sesion a los 5 minutos pero lo he añadido como funcionalidad extra
    user = vUsu(usu=varUsu.get())
    sleep(290)
    messagebox.showerror(message="Tiempo expirado", title="Cierre da sesion")
    sleep(10)
    user.salir()

def cambioContrasenia():
    global varUsu
    if(varUsu.get()==""):
        messagebox.showerror("Error cambio contraseña", "Selecciona un usuario")
    elif(not(miBase.existeUsuario(usu=varUsu.get()))):
        messagebox.showerror(title="Error cambio contraseña", message="No se encuentra el usuario")
    else:
        psswd = simpledialog.askstring("Cambio Contraseña","Elige una nueva contraseña")
        if(miBase.cambioContrasenia(usu=varUsu.get(),passwd=psswd)):
            messagebox.showinfo(title="Exito", message="Contraseña actualizada con exito")
        else:
            messagebox.showerror(title="Error cambio contraseña", message="Algo fallo, ups....")

miBase = bbdd()
#IMPORTANTE recuerda, si has realizado algun cambio en la BBDD quitar esta
#Linea de codigo, o comentarla para que no borre y vuelva a crear la misma
miBase.crearTablas()
#Ventana principal
ventanap = tk.Tk()
ventanap.title("Herramienta vacacional Alberto Horcajada")
ventanap.resizable(False, False)
ventanap.geometry("400x300")
#Parte de usuario
tk.Label(ventanap, text="Usuario").grid(column=0, row=0, padx=10, pady=10)
varUsu = tk.StringVar()
varUsu.set("")
tk.Entry(ventanap, textvariable=varUsu, width=40).grid(column=0, row=1, padx=10, pady=10)
#Parte de contraseña
tk.Label(ventanap, text="contraseña").grid(column=0, row=2, padx=10, pady=10)
varPass = tk.StringVar()
varPass.set("")
visible = False
entryPass = ttk.Entry(ventanap, textvariable=varPass, width=40, show="*")
entryPass.grid(column=0, row=3, padx=10, pady=10)

path_base = os.path.dirname(__file__)
image_path =  os.path.join (path_base, 'ojo.png')
img = PhotoImage(file=image_path)
ojo = img.subsample(16)

tk.Button(ventanap, command=mostrarPass, image=ojo).grid(column=1, row=3, padx=10, pady=10)

#Acceptar/Olvidar contraseña
tk.Button(ventanap, text="aceptar", command=iniciarSesion, width=33).grid(column=0, row=4, padx=10, pady=10, sticky="W")
tk.Button(ventanap, text="olvidó la contraseña", command=cambioContrasenia, width=33).grid(column=0, row=5, padx=10, pady=10, sticky="w")


ventanap.mainloop()
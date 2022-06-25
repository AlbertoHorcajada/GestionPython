import tkinter as tk
from tkinter import PhotoImage, messagebox
import tkinter.font as tkf
import tkinter.simpledialog as sm
import os

from BBDD import bbdd
from interfazRestarReservados import interfazLupa as intLup
from grafico import graf

class ventanaAdmin():
    def __init__(self) -> None:
        self.ventanap = tk.Toplevel()
        self.ventanap.title("Herramienta vacacional Alberto Horcajada")
        self.__crearInterfaz()

    def __crearInterfaz(self):
        fstyle = tkf.Font(size=20)
        lblAdmin = tk.Label(self.ventanap, text="ADMINISTRADOR",font=fstyle)
        lblAdmin.grid(column=0, row=0, padx=10, pady=10, sticky="w", columnspan=2)
        lblAdmin.config(fg="red")

        self.path_base = os.path.dirname(__file__)

        self.path_villablanca = os.path.join(self.path_base, 'villablanca.png')
        self.imgLvillablanca = PhotoImage(file=self.path_villablanca)
        self.villablanca = self.imgLvillablanca.subsample(6)

        tk.Label(self.ventanap,image=self.villablanca).grid(column=3, row=0 , padx=10, pady=10)

        
        self.path_lupa = os.path.join(self.path_base, 'lupa.png')
        self.imgLupa = PhotoImage(file=self.path_lupa)
        self.lupa = self.imgLupa.subsample(10)

        self.path_grafico = os.path.join(self.path_base, 'grafico.png')
        self.imgGrafico = PhotoImage(file=self.path_grafico)
        self.grafico = self.imgGrafico.subsample(10)

        self.path_salir = os.path.join(self.path_base, 'cruz.png')
        self.imgSalida = PhotoImage(file=self.path_salir)
        self.salida = self.imgSalida.subsample(10)

        tk.Canvas(self.ventanap, background="red", height=10).grid(column=0, row=1, padx=10, pady=10, columnspan=4)

        btnLupa = tk.Button(self.ventanap, command=self.funcionLupa, image=self.lupa)
        btnLupa.grid(column=0, row=2, padx=10, pady=10, sticky="w")

        btnGrafico = tk.Button(self.ventanap,image= self.grafico, command=self.funcionGrafico)
        btnGrafico.grid(column=1, row=2, padx=10, pady=10, sticky="w")

        btnSalir = tk.Button(self.ventanap, image=self.salida, command=self.salir)
        btnSalir.grid(column=2, row=2, padx=10, pady=10, sticky="w")
        
    
    def funcionLupa(self):
        miBase = bbdd()
        
        usu = sm.askstring("Usuario","nombre del usuario del que quieras ver o modificar infomracion")
        if(usu!=None):
            resultado = miBase.buscarInfoUsuario(usu=usu)
            if(resultado!="admin"):
                msg = "mes\tdisponibles\tdisfrutados\treservados\n"
                for i in range(len(resultado)):
                    msg+="\n" + resultado[i][1] +"\t\t" + str(resultado[i][2]) +"\t\t" + str(resultado[i][3]) +"\t\t" + str(resultado[i][4])
                messagebox.showinfo(message=msg,title=usu)

                intLup(usu)
            else:
                messagebox.showerror(title="ERROR", message="el admin no tiene vacaciones")
        else:        
            messagebox.showerror(title="ERROR", message="No seleccionaste ningun usuario")


        pass

        '''
        Aqui como los meses están reducidos a tres letras, lo ordeno por mes y se yo
        el orden que va a ser:
        abril   agosto  diciembre   enero   febrero julio   junio   marzo   mayo    noviembre   octubre septiembre
        0       1       2           3       4       5       6       7       8       9           10      11
        Para que esten ordenados por mes tengo que ordenar el resultado en este orden
        enero   febrero marzo       abril   mayo    junio   julio   agosto  septiembre  octubre noviembre   diciembre
        3       4       7           0       8       6       5       1       11          10      9           2
        
        '''

    def funcionGrafico(self):
        miBase = bbdd()
        miGrafico = graf()
        valoresxD=[]#Los valores de la X desordenados
        resultado = miBase.vacacionesPorMes()
        if(resultado == 0):
            messagebox.showerror(message="Algo salio mal", title="Espera")
        else:
            for mes in resultado:
                valoresxD.append(int(mes[0]))
            valoresy=["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
            valoresx=[]#Estos ya si son los dias disfrutados ordenados
            valoresx.append(valoresxD[3])
            valoresx.append(valoresxD[4])
            valoresx.append(valoresxD[7])
            valoresx.append(valoresxD[0])
            valoresx.append(valoresxD[8])
            valoresx.append(valoresxD[6])
            valoresx.append(valoresxD[5])
            valoresx.append(valoresxD[1])
            valoresx.append(valoresxD[11])
            valoresx.append(valoresxD[10])
            valoresx.append(valoresxD[9])
            valoresx.append(valoresxD[2])
            
            miGrafico.mostrarGrafico(valoresx=valoresx,valoresy=valoresy)


    

    def salir(self):

        self.ventanap.destroy()
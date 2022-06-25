import tkinter as tk
from tkinter import messagebox, simpledialog
import os

from BBDD import bbdd


class interfazLupa:
    def __init__(self, usu) -> None:
        self.ventana = tk.Tk()
        self.ventana.title("Restar dias reservados")
        self.usu = usu

        self.__crearInterfaz()
        
    
    def __crearInterfaz(self):
        label = "Quitar dias reservados a " + self.usu
        tk.Label(self.ventana,text=label).grid(column=0, row=0, padx=10, pady=10, columnspan=2)

        self.path_base = os.path.dirname(__file__)

        tk.Button(self.ventana, text="Quitar", command=self.quitarReservados).grid(column=0, row=1, padx=10, pady=10)

        tk.Button(self.ventana, command=self.salir, text="salir").grid(column=1, row=1, padx=10, pady=10)

    def salir(self):
        self.ventana.destroy()

    def quitarReservados(self):
        miBase = bbdd()
        dias = simpledialog.askinteger("Retirada de dias reservados", "cuantos dias vas a querer retirar")
        if(dias != None):
            mes = simpledialog.askstring("Retirada de dias reservados", "sobre que mes (tres primeras letras del mes)")
            if(mes != None):
                if(dias<= miBase.diasReservadosPorMes(usu=self.usu, mes=mes)):
                    if(miBase.quitarDiasReservados(usu=self.usu,mes=mes,dias=dias)):
                        resultado = miBase.buscarInfoUsuario(usu=self.usu)
                        msg = "mes\tdisponibles\tdisfrutados\treservados\n"
                        for i in range(len(resultado)):
                            msg+="\n" + resultado[i][1] +"\t\t" + str(resultado[i][2]) +"\t\t" + str(resultado[i][3]) +"\t\t" + str(resultado[i][4])
                
                        messagebox.showinfo(title="Dias quitados con exito", message=msg)
                        self.ventana.destroy()
                else:
                    messagebox.showerror(title="Error",message="No dispone de tantos reservados en el mes seleccionado")  
            else:
                messagebox.showerror(title="Error",message="Error por cancelar")
        else:
            messagebox.showerror(title="Error",message="Error por cancelar")
            
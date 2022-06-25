import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class graf:
    def __init__(self) -> None:
        self.venatanp = tk.Toplevel()
        self.venatanp.title("Grafico vacacional")
    
    def mostrarGrafico(self, valoresx, valoresy):
        fig = Figure(figsize=(12,8), facecolor='green', edgecolor="black")
        axis = fig.add_subplot(111)
        axis.plot(valoresy,valoresx)
        axis.set_xlabel('Dias Disfrutados')
        axis.set_ylabel('Meses')
        axis.grid(linestyle="-")

        canvas = FigureCanvasTkAgg(fig, master=self.venatanp)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
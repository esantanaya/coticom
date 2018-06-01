import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime


class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cotizaciones y Compras CIMARR")
        self.geometry("883x693")
        self.resizable(True, True)

        n = ttk.Notebook(self)

        pestana_cotizacion = PestanaCotizacion(n)
        pestana_compra = ttk.Frame(n)

        n.add(pestana_cotizacion, text="Cotización")
        n.add(pestana_compra, text="Compra")

        n.pack(fill=tk.BOTH, expand=1)


class PestanaCotizacion(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.id = tk.StringVar()
        self.fecha = tk.StringVar()
        self.id.set("ID")
        self.fecha.set(datetime.now().strftime('%d/%m/%Y'))
        self.frame_arriba = tk.Frame(self)
        self.lbl_id = tk.Label(self.frame_arriba, text="ID")
        self.txt_id = tk.Entry(self.frame_arriba, textvariable=self.id, width=5)
        self.btn_cargar = tk.Button(self.frame_arriba, text="Cargar")
        self.btn_buscar = tk.Button(self.frame_arriba, text="Buscar")
        self.btn_nueva = tk.Button(self.frame_arriba, text="Nueva")
        self.btn_crea_oc = tk.Button(self.frame_arriba, text="Crear O.C")

        self.btn_anterior = ttk.Button(self.frame_arriba, text="< Anterior")
        self.btn_siguiente = ttk.Button(self.frame_arriba, text="Siguiente >")

        self.lbl_fecha = tk.Label(self.frame_arriba, text="Fecha")
        self.txt_fecha = tk.Entry(self.frame_arriba, textvariable=self.fecha)

        self.frame_cliente = ttk.Frame(self)
        self.frame_datos = ttk.Frame(self)
        self.frame_detalle = ttk.Frame(self)

        self.lblf_cliente = ttk.LabelFrame(self.frame_cliente, text="Cliente")
        self.lblf_datos = ttk.LabelFrame(self.frame_datos, text="Datos")
        self.lblf_detalle = ttk.LabelFrame(self.frame_detalle, text="Detalle")

        self.frame_arriba.pack(side=tk.TOP, fill=tk.BOTH)
        self.lbl_id.pack(side=tk.LEFT, padx=5)
        self.txt_id.pack(side=tk.LEFT)
        self.btn_cargar.pack(side=tk.LEFT)
        self.btn_buscar.pack(side=tk.LEFT)
        self.btn_nueva.pack(side=tk.LEFT)
        self.btn_crea_oc.pack(side=tk.LEFT)

        self.btn_anterior.pack(side=tk.LEFT)
        self.btn_siguiente.pack(side=tk.LEFT)

        self.lbl_fecha.pack(side=tk.LEFT)
        self.txt_fecha.pack(side=tk.LEFT)

        self.lblf_cliente.pack(fill=tk.BOTH, expand=1)
        self.lblf_datos.pack(fill=tk.BOTH, expand=1)
        self.lblf_detalle.pack(fill=tk.BOTH, expand=1)

        self.frame_detalle.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.frame_datos.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.frame_cliente.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    v = Ventana()
    v.mainloop()

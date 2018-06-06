import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime


class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cotizaciones y Compras CIMARR")
        self.geometry("883x693")
        self.resizable(True, True)

        self.menu = tk.Menu(self)

        n = ttk.Notebook(self)

        pestana_cotizacion = PestanaCotizacion(n)
        pestana_compra = PestanaCompras(n)

        self.menu.add_command(label="Archivo")
        self.menu.add_command(label="Catalogos")
        self.menu.add_command(label="Acerca")

        n.add(pestana_cotizacion, text="Cotización")
        n.add(pestana_compra, text="Compra")

        self.configure(menu=self.menu)

        n.pack(fill=tk.BOTH, expand=1)


class PestanaCotizacion(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        #Variables
        self.id = tk.StringVar()
        self.fecha = tk.StringVar()
        self.id.set("ID")
        self.fecha.set(datetime.now().strftime('%d/%m/%Y'))

        #Controles
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

        self.frame_datos = ttk.Frame(self)
        self.frame_detalle = ttk.Frame(self)

        self.lblf_datos = ttk.LabelFrame(self.frame_datos, text="Datos")
        self.lblf_detalle = ttk.LabelFrame(self.frame_detalle, text="Detalle")

        self.frame_abajo = tk.Frame(self)
        self.btn_pdf = tk.Button(self.frame_abajo, text="PDF")
        self.btn_enviar = tk.Button(self.frame_abajo, text="ENVIAR")

        #Acomodamos todo
        self.frame_arriba.pack(side=tk.TOP, fill=tk.BOTH)
        self.lbl_id.pack(side=tk.LEFT, padx=5)
        self.txt_id.pack(side=tk.LEFT)
        self.btn_cargar.pack(side=tk.LEFT)
        self.btn_buscar.pack(side=tk.LEFT)
        self.btn_nueva.pack(side=tk.LEFT)
        self.btn_crea_oc.pack(side=tk.LEFT)

        self.btn_anterior.pack(side=tk.LEFT)
        self.btn_siguiente.pack(side=tk.LEFT)

        self.txt_fecha.pack(side=tk.RIGHT)
        self.lbl_fecha.pack(side=tk.RIGHT)

        self.lblf_datos.pack(fill=tk.BOTH, expand=1)
        self.lblf_detalle.pack(fill=tk.BOTH, expand=1)

        self.frame_abajo.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.btn_pdf.pack(side=tk.LEFT, padx=(350,50))
        self.btn_enviar.pack(side=tk.RIGHT, padx=(50,350))

        self.frame_detalle.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.frame_datos.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        self.grupo_cliente()

    def grupo_cliente(self):
        self.frame_cliente = ttk.Frame(self)
        self.lblf_cliente = LabelFrameCliente(
            self.frame_cliente,
            text="Cliente"
        )

        self.lblf_cliente.pack(fill=tk.BOTH, expand=1)
        self.frame_cliente.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


class PestanaCompras(PestanaCotizacion):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def grupo_cliente(self):
        self.frame_cliente = ttk.Frame(self)
        self.lblf_cliente = LabelFrameCliente(
            self.frame_cliente,
            text="Proveedor"
        )

        self.lblf_cliente.pack(fill=tk.BOTH, expand=1)
        self.frame_cliente.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


class LabelFrameCliente(ttk.LabelFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.clientes = ("Q00001","Q00002","Q00003")
        self.nombre_cliente = tk.StringVar()
        self.telefonos_cliente = tk.StringVar()
        self.domicilio_cliente = tk.StringVar()

        arriba = tk.Frame(self)
        domicilio = tk.Frame(self)
        contacto = tk.Frame(self)
        botones = tk.Frame(self)

        lblf_contacto = ttk.LabelFrame(contacto, text="Contacto")

        self.lbl_clave_cliente = tk.Label(arriba, text="Clave")
        self.cmb_clave_cliente = ttk.Combobox(
            arriba,
            values=self.clientes,
            width=7
        )
        self.cmb_clave_cliente.current(0)
        self.lbl_nombre_cliente = tk.Label(arriba, text="Nombre")
        self.txt_nombre_cliente = tk.Entry(
            arriba,
            textvariable=self.nombre_cliente,
            width=70
        )
        self.lbl_telefonos_cliente = tk.Label(arriba, text="Teléfonos")
        self.txt_telefonos_cliente = tk.Entry(
            arriba,
            textvariable=self.telefonos_cliente
        )
        self.lbl_domicilio_cliente = tk.Label(domicilio, text="Domicilio")
        self.txt_domicilio_cliente = tk.Entry(
            domicilio,
            textvariable=self.domicilio_cliente,
            width=125,
        )

        arriba.pack(side=tk.TOP, fill=tk.BOTH)
        domicilio.pack(side=tk.TOP, fill=tk.BOTH)
        lblf_contacto.pack(fill=tk.BOTH, expand=1)
        contacto.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=(0,200))
        botones.pack(side=tk.RIGHT, expand=0)
        self.lbl_clave_cliente.pack(side=tk.LEFT)
        self.cmb_clave_cliente.pack(side=tk.LEFT)
        self.lbl_nombre_cliente.pack(side=tk.LEFT)
        self.txt_nombre_cliente.pack(side=tk.LEFT)
        self.lbl_telefonos_cliente.pack(side=tk.LEFT)
        self.txt_telefonos_cliente.pack(side=tk.LEFT)
        self.lbl_domicilio_cliente.pack(side=tk.LEFT)
        self.txt_domicilio_cliente.pack(side=tk.LEFT)


if __name__ == "__main__":
    v = Ventana()
    v.mainloop()

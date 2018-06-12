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

        self.frame_abajo.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.btn_pdf.pack(side=tk.LEFT, padx=(350,50))
        self.btn_enviar.pack(side=tk.RIGHT, padx=(50,350))

        self.grupo_detalle()
        self.grupo_datos()
        self.grupo_cliente()

    def grupo_cliente(self):
        self.frame_cliente = ttk.Frame(self)
        self.lblf_cliente = LabelFrameCliente(
            self.frame_cliente,
            text="Cliente"
        )

        self.lblf_cliente.pack(fill=tk.BOTH, expand=1)
        self.frame_cliente.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def grupo_datos(self):
        self.frame_datos = ttk.Frame(self)
        self.lblf_datos = LabelFrameDatos(self.frame_datos, text="Datos")

        self.lblf_datos.pack(fill=tk.BOTH, expand=1)
        self.frame_datos.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

    def grupo_detalle(self):
        self.frame_detalle = ttk.Frame(self)
        self.lblf_detalle = LabelFrameDetalle(self.frame_detalle, text="Detalle")

        self.lblf_detalle.pack(fill=tk.BOTH, expand=1)
        self.frame_detalle.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)


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
        botones_arriba = tk.Frame(botones)
        botones_abajo = tk.Frame(botones)

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

        self.lblf_contacto = LabelFrameContacto(contacto, text="Contacto")

        self.btn_nuevo = tk.Button(botones_arriba, text="Nuevo")
        self.btn_editar = tk.Button(botones_arriba, text="Editar")
        self.btn_buscar = tk.Button(botones_abajo, text="Buscar")
        self.btn_guardar = tk.Button(botones_abajo, text="Guardar")

        arriba.pack(side=tk.TOP, fill=tk.BOTH)
        domicilio.pack(side=tk.TOP, fill=tk.BOTH)
        self.lblf_contacto.pack(fill=tk.BOTH, expand=1)
        contacto.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        botones.pack(side=tk.RIGHT, expand=1, fill=tk.BOTH)
        botones_arriba.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        botones_abajo.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.btn_nuevo.pack(side=tk.LEFT)
        self.btn_editar.pack(side=tk.LEFT)
        self.btn_buscar.pack(side=tk.LEFT)
        self.btn_guardar.pack(side=tk.LEFT)
        self.lbl_clave_cliente.pack(side=tk.LEFT)
        self.cmb_clave_cliente.pack(side=tk.LEFT)
        self.lbl_nombre_cliente.pack(side=tk.LEFT)
        self.txt_nombre_cliente.pack(side=tk.LEFT)
        self.lbl_telefonos_cliente.pack(side=tk.LEFT)
        self.txt_telefonos_cliente.pack(side=tk.LEFT)
        self.lbl_domicilio_cliente.pack(side=tk.LEFT)
        self.txt_domicilio_cliente.pack(side=tk.LEFT)


class LabelFrameContacto(ttk.LabelFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.nombre_contacto = tk.StringVar()
        self.cargo_contacto = tk.StringVar()
        self.movil_contacto = tk.StringVar()
        self.correo_contacto = tk.StringVar()

        arriba = tk.Frame(self)
        abajo = tk.Frame(self)

        self.lbl_nombre_contacto = tk.Label(arriba, text="Nombre")
        self.txt_nombre_contacto = tk.Entry(
            arriba,
            textvariable=self.nombre_contacto
        )
        self.lbl_cargo_contacto = tk.Label(arriba, text="Cargo")
        self.txt_cargo_contacto = tk.Entry(
            arriba,
            textvariable=self.cargo_contacto
        )
        self.lbl_movil_contacto = tk.Label(abajo, text="Movil")
        self.txt_movil_contacto = tk.Entry(
            abajo,
            textvariable=self.movil_contacto
        )
        self.lbl_correo_contacto = tk.Label(abajo, text="Correo")
        self.txt_correo_contacto = tk.Entry(
            abajo,
            textvariable=self.correo_contacto
        )

        arriba.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        abajo.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
        self.lbl_nombre_contacto.pack(side=tk.LEFT)
        self.txt_nombre_contacto.pack(side=tk.LEFT)
        self.lbl_cargo_contacto.pack(side=tk.LEFT)
        self.txt_cargo_contacto.pack(side=tk.LEFT)
        self.lbl_movil_contacto.pack(side=tk.LEFT)
        self.txt_movil_contacto.pack(side=tk.LEFT)
        self.lbl_correo_contacto.pack(side=tk.LEFT)
        self.txt_correo_contacto.pack(side=tk.LEFT)


class LabelFrameDatos(ttk.LabelFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.condiciones_pago = ("30 días naturales",)
        self.vigencia = ("7 días",)
        self.moneda = ("Pesos Mexicanos", "Dolares Americanos",)
        self.asesor = ("José Luis Arreola",)
        self.nota_1 = (
            "FAVOR DE ANOTAR EL NUMERO DE COTIZACION EN SU ORDEN DE COMPRA",
        )
        self.nota_2 = ("NO SE ACEPTAN DEVOLUCIONES NI CANCELACIONES",)

        izquierda = tk.Frame(self)
        iz_arriba = tk.Frame(izquierda)
        iz_centro = tk.Frame(izquierda)
        iz_abajo = tk.Frame(izquierda)
        derecha = tk.Frame(self)
        der_arriba = tk.Frame(derecha)
        der_centro = tk.Frame(derecha)
        der_abajo = tk.Frame(derecha)

        self.lbl_condiciones_pago = tk.Label(iz_arriba, text="Condiciones pago")
        self.cmb_condiciones_pago = ttk.Combobox(
            iz_arriba,
            values=self.condiciones_pago
        )
        self.lbl_vigencia = tk.Label(iz_centro, text="Vigencia")
        self.cmb_vigencia = ttk.Combobox(
            iz_centro,
            values=self.vigencia
        )
        self.lbl_moneda = tk.Label(iz_abajo, text="Moneda")
        self.cmb_moneda = ttk.Combobox(
            iz_abajo,
            values=self.moneda
        )
        self.lbl_asesor = tk.Label(der_arriba, text="Asesor")
        self.cmb_asesor = ttk.Combobox(
            der_arriba,
            values=self.asesor
        )
        self.lbl_nota_1 = tk.Label(der_centro, text="Nota 1")
        self.cmb_nota_1 = ttk.Combobox(
            der_centro,
            values=self.nota_1
        )
        self.lbl_nota_2 = tk.Label(der_abajo, text="Nota 2")
        self.cmb_nota_2 = ttk.Combobox(
            der_abajo,
            values=self.nota_2
        )

        izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        iz_arriba.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        iz_centro.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        iz_abajo.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        der_arriba.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        der_centro.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        der_abajo.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.lbl_condiciones_pago.pack(side=tk.LEFT)
        self.cmb_condiciones_pago.pack(side=tk.LEFT)
        self.lbl_vigencia.pack(side=tk.LEFT)
        self.cmb_vigencia.pack(side=tk.LEFT)
        self.lbl_moneda.pack(side=tk.LEFT)
        self.cmb_moneda.pack(side=tk.LEFT)
        self.lbl_asesor.pack(side=tk.LEFT)
        self.cmb_asesor.pack(side=tk.LEFT)
        self.lbl_nota_1.pack(side=tk.LEFT)
        self.cmb_nota_1.pack(side=tk.LEFT)
        self.lbl_nota_2.pack(side=tk.LEFT)
        self.cmb_nota_2.pack(side=tk.LEFT)


class LabelFrameDetalle(ttk.LabelFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        tabla = tk.Frame(self)
        abajo = tk.Frame(self)

        self.subtotal = tk.StringVar()
        self.subtotal.set("100")
        self.iva = tk.StringVar()
        self.iva.set("16")
        self.total = tk.StringVar()
        self.total.set("116")


        self.parte = tk.Label(tabla, text="Parte", bg="light gray")
        self.modelo = tk.Label(tabla, text="Modelo", bg="light gray")
        self.descripcion = tk.Label(tabla, text="Descripción", bg="light gray")
        self.marca = tk.Label(tabla, text="Marca", bg="light gray")
        self.tiempo_entrega = tk.Label(
            tabla,
            text="T Ent",
            bg="light gray"
        )
        self.cantidad = tk.Label(tabla, text="Cant", bg="light gray")
        self.precio_unit = tk.Label(
            tabla,
            text="P Unit",
            bg="light gray"
        )
        self.importe = tk.Label(tabla, text="Imp", bg="light gray")
        self.proveedor = tk.Label(tabla, text="Provr", bg="light gray")
        self.costo_unit = tk.Label(tabla, text="C Unit", bg="light gray")

        self.lbl_subtotal = tk.Label(abajo, text="Subtotal")
        self.txt_subtotal = ttk.Entry(abajo, textvariable=self.subtotal)
        self.lbl_iva = tk.Label(abajo, text="IVA")
        self.txt_iva = ttk.Entry(abajo, textvariable=self.iva)
        self.lbl_total = tk.Label(abajo, text="Total")
        self.txt_total = ttk.Entry(abajo, textvariable=self.total)

        tk.Grid.columnconfigure(tabla, 1, minsize=5)
        tk.Grid.columnconfigure(tabla, 2, minsize=10)
        tk.Grid.columnconfigure(tabla, 3, minsize=50)
        tk.Grid.columnconfigure(tabla, 4, minsize=10)
        tk.Grid.columnconfigure(tabla, 5, minsize=5)
        tk.Grid.columnconfigure(tabla, 6, minsize=5)
        tk.Grid.columnconfigure(tabla, 7, minsize=6)
        tk.Grid.columnconfigure(tabla, 8, minsize=6)
        tk.Grid.columnconfigure(tabla, 9, minsize=7)
        tk.Grid.columnconfigure(tabla, 10, minsize=6)

        tabla.pack(fill=tk.BOTH, expand=1, side=tk.TOP)
        self.parte.grid(column=1, row=0)
        self.modelo.grid(column=2, row=0)
        self.descripcion.grid(column=3, row=0)
        self.marca.grid(column=4, row=0)
        self.tiempo_entrega.grid(column=5, row=0)
        self.cantidad.grid(column=6, row=0)
        self.precio_unit.grid(column=7, row=0)
        self.importe.grid(column=8, row=0)
        self.proveedor.grid(column=9, row=0)
        self.costo_unit.grid(column=10, row=0)

        self.linea = LineaDetalle(tabla, 1)
        self.linea.empacar()

        abajo.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)
        self.lbl_subtotal.pack(side=tk.LEFT)
        self.txt_subtotal.pack(side=tk.LEFT)
        self.lbl_iva.pack(side=tk.LEFT)
        self.txt_iva.pack(side=tk.LEFT)
        self.lbl_total.pack(side=tk.LEFT)
        self.txt_total.pack(side=tk.LEFT)

class LineaDetalle:

    def __init__(self, master, indice):
        self.indice = indice
        self.texto_parte = tk.StringVar()
        self.texto_parte.set(str(self.indice))
        self.parte = ttk.Entry(
            master,
            textvariable=self.texto_parte,
            width=5,
            state="readonly"
        )
        self.modelo = ttk.Combobox(master, width=10)
        self.descripcion = ttk.Entry(master, width=50, state="readonly")
        self.marca = ttk.Entry(master, width=10, state="readonly")
        self.tiempo_entrega = ttk.Entry(master, width=5, state="readonly")
        self.cantidad = ttk.Entry(master, width=5, state="normal")
        self.precio_unit = ttk.Entry(master, width=6, state="normal")
        self.importe = ttk.Entry(master, width=6, state="readonly")
        self.proveedor = ttk.Combobox(master, width=7, state="normal")
        self.costo_unit = ttk.Entry(master, width=6, state="readonly")

    def empacar(self):
        self.parte.grid(column=1, row=self.indice)
        self.modelo.grid(column=2, row=self.indice)
        self.descripcion.grid(column=3, row=self.indice)
        self.marca.grid(column=4, row=self.indice)
        self.tiempo_entrega.grid(column=5, row=self.indice)
        self.cantidad.grid(column=6, row=self.indice)
        self.precio_unit.grid(column=7, row=self.indice)
        self.importe.grid(column=8, row=self.indice)
        self.proveedor.grid(column=9, row=self.indice)
        self.costo_unit.grid(column=10, row=self.indice)

if __name__ == "__main__":
    v = Ventana()
    v.mainloop()

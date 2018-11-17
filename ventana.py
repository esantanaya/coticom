import sys
from datetime import date
from exceptions import ErrorConexion

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound

from modelos import (Asesor, Cliente, CondicionPago, ContactoCliente,
                     Cotizacion, DetalleCotizacion, DuplicadoError,
                     GuardadoError, Moneda, Nota, Producto, Proveedor,
                     Vigencia, TipoValorError)

class Ventana(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        try:
            uic.loadUi('ventana.ui', self)
            self.control_fecha.setDate(date.today())
            self.cotizacion = Cotizacion.get_ultima_cotizacion()
            self.texto_id.setText(str(self.cotizacion.clave))
            self.carga_clientes()
            self.combobox_clave_cliente.currentIndexChanged.connect(
                self.cambia_combo_cliente
            )
            self.combobox_clave_cliente.setCurrentIndex(1)
            self.carga_datos()
            self.actionClientes.triggered.connect(self.abre_busqueda_clientes)
            self.actionProductos.triggered.connect(self.abre_busqueda_productos)
            self.boton_buscar_cliente.clicked.connect(
                self.abre_busqueda_clientes
            )
            self.boton_editar_cliente.clicked.connect(self.abre_edita_cliente)
            self.boton_nuevo.clicked.connect(self.abre_nuevo_cliente)
        except OperationalError:
            raise ErrorConexion
        except ErrorConexion:
            raise ErrorConexion
        except FileNotFoundError:
            raise FileNotFoundError

    def cambia_combo_cliente(self):
        if len(self.combobox_clave_cliente.currentText()) > 0:
            try:
                cliente = Cliente.get_cliente(
                    self.combobox_clave_cliente.currentText()
                )
                self.carga_cliente(cliente)
            except OperationalError:
                self.muestra_error(
                    'Hay un problema con la conexión a la base de datos',
                    True
                )
            except GuardadoError:
                self.muestra_error('No se puede dejar la clave en blanco', True)
            except ErrorConexion:
                raise ErrorConexion

    def carga_clientes(self):
        try:
            clientes = Cliente.get_clave_clientes()
        except OperationalError:
            raise ErrorConexion
        else:
            for cliente in clientes:
                self.combobox_clave_cliente.addItem(cliente.clave)

    def carga_cliente(self, cliente):
        self.texto_nombre_cliente.setText(cliente.nombre)
        self.texto_telefonos.setText(cliente.telefonos)
        self.texto_domicilio.setText(cliente.domicilio)
        try:
            contacto = ContactoCliente.get_contacto_primario(cliente)
        except NoResultFound:
            self.vacia_contacto()
        else:
            self.texto_nombre_contacto.setText(contacto.nombre)
            self.texto_cargo.setText(contacto.cargo)
            self.texto_movil_contacto.setText(contacto.movil)
            self.texto_correo_contacto.setText(contacto.correo)

    def vacia_contacto(self):
        self.texto_nombre_contacto.clear()
        self.texto_cargo.clear()
        self.texto_movil_contacto.clear()
        self.texto_correo_contacto.clear()

    def carga_datos(self):
        try:
            self.carga_condiciones()
            self.carga_vigencias()
            self.carga_moneda()
            self.carga_asesores()
            self.carga_notas()
            self.carga_detalles()
            self.carga_sumas()
        except ErrorConexion:
            raise ErrorConexion

    def carga_sumas(self):
        self.label_valor_subtotal.setText(f'${self.cotizacion.subtotal:,.2f}')
        self.label_valor_iva.setText(f'${self.cotizacion.iva:,.2f}')
        self.label_valor_total.setText(f'${self.cotizacion.total:,.2f}')

    def carga_detalles(self):
        COL_PARTE, COL_MODELO, COL_DESCRIPCION, COL_MARCA,  COL_TE = range(5)
        COL_CANTIDAD, COL_PU, COL_IMPORTE,  COL_PROVEEDOR, COL_CU = range(5, 10)

        try:
            lineas = DetalleCotizacion.get_detalle(self.cotizacion.clave)
        except OperationalError:
            raise ErrorConexion
        else:
            for num, detalle in enumerate(lineas):
                producto = Producto.get_producto(detalle.modelo_producto)
                productos = Producto.get_productos_modelo()
                productos = [x[0] for x in productos]
                proveedor = Proveedor.get_proveedor(producto.clave_proveedor)
                combo_proveedor = Combo(productos)

                self.tabla_detalle.insertRow(num)
                self.tabla_detalle.setItem(
                    num,
                    COL_PARTE,
                    QtWidgets.QTableWidgetItem(str(detalle.linea))
                )
                self.tabla_detalle.setCellWidget(
                    num,
                    COL_MODELO,
                    combo_proveedor
                    # QtWidgets.QTableWidgetItem(producto.modelo)
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_DESCRIPCION,
                    QtWidgets.QTableWidgetItem(producto.descripcion)
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_MARCA,
                    QtWidgets.QTableWidgetItem(producto.marca)
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_TE,
                    QtWidgets.QTableWidgetItem(detalle.tiempo_entrega)
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_CANTIDAD,
                    QtWidgets.QTableWidgetItem(str(detalle.cantidad))
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_PU,
                    QtWidgets.QTableWidgetItem(str(detalle.precio_unitario))
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_IMPORTE,
                    QtWidgets.QTableWidgetItem(str(detalle.importe))
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_PROVEEDOR,
                    QtWidgets.QTableWidgetItem(proveedor.nombre)
                )
                self.tabla_detalle.setItem(
                    num,
                    COL_CU,
                    QtWidgets.QTableWidgetItem(str(producto.ultimo_costo))
                )
                cabecera = self.tabla_detalle.horizontalHeader()
                cabecera.setSectionResizeMode(
                    COL_PARTE,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_MODELO,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_DESCRIPCION,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_MARCA,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_TE,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_CANTIDAD,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_PU,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_IMPORTE,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_PROVEEDOR,
                    QtWidgets.QHeaderView.ResizeToContents
                )
                cabecera.setSectionResizeMode(
                    COL_CU,
                    QtWidgets.QHeaderView.ResizeToContents
                )

    def carga_notas(self):
        try:
            notas = Nota.get_notas()
        except OperationalError:
            raise ErrorConexion
        else:
            for nota in notas:
                self.combobox_nota1.addItem(nota.descripcion)
                self.combobox_nota2.addItem(nota.descripcion)

    def carga_asesores(self):
        try:
            asesores = Asesor.get_asesores()
        except OperationalError:
            raise ErrorConexion
        else:
            for asesor in asesores:
                self.combobox_asesor.addItem(asesor.nombre)

    def carga_moneda(self):
        try:
            monedas = Moneda.get_monedas()
        except OperationalError:
            raise ErrorConexion
        else:
            for moneda in monedas:
                self.combobox_moneda.addItem(moneda.clave)

    def carga_vigencias(self):
        try:
            vigencias = Vigencia.get_vigencias()
        except OperationalError:
            raise ErrorConexion
        else:
            for vigencia in vigencias:
                self.combobox_vigencia.addItem(vigencia.descripcion)

    def carga_condiciones(self):
        try:
            condiciones = CondicionPago.get_condiciones()
        except OperationalError:
            raise ErrorConexion
        else:
            for condicion in condiciones:
                self.combobox_condiciones.addItem(condicion.descripcion)

    def muestra_error(self, mensaje, cierra=False):
        error = Error(mensaje)
        error.exec_()
        if cierra:
            self.close()

    def abre_busqueda_clientes(self):
        try:
            busqueda = BusquedaClientes()
            busqueda.exec_()
        except FileNotFoundError:
            raise FileNotFoundError

    def abre_edita_cliente(self):
        cliente = Cliente.get_cliente(self.combobox_clave_cliente.currentText())
        catalogo = CatalogoCliente(cliente)
        catalogo.exec_()

    def abre_nuevo_cliente(self):
        cliente = Cliente()
        catalogo = CatalogoCliente(cliente)
        catalogo.texto_clave.setEnabled(True)
        catalogo.exec_()

    def abre_busqueda_productos(self):
        try:
            busqueda = BusquedaProductos()
            busqueda.exec_()
        except FileNotFoundError:
            raise FileNotFoundError


class BusquedaClientes(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        opciones_busqueda = ['Nombre', 'Domicilio', 'Teléfonos']

        try:
            uic.loadUi('busqueda_clientes.ui', self)
            self.clientes = Cliente.get_clientes()
            self.tabla_clientes.cellDoubleClicked.connect(self.regresa_cliente)
            self.boton_seleccionar.clicked.connect(self.regresa_cliente)
            self.boton_buscar.clicked.connect(self.busca_clientes)
        except OperationalError:
            raise ErrorConexion
        except FileNotFoundError:
            raise FileNotFoundError
        else:
            for opcion in opciones_busqueda:
                self.combobox_campos.addItem(opcion)
            self.llena_lista()

    def llena_lista(self):
        COL_CLAVE, COL_NOMBRE, COL_DOM, COL_TELS = range(4)
        self.tabla_clientes.clearContents()
        self.tabla_clientes.setRowCount(0)
        for fila, cliente in enumerate(self.clientes):
            self.tabla_clientes.insertRow(fila)
            self.tabla_clientes.setItem(
                fila, COL_CLAVE, QtWidgets.QTableWidgetItem(cliente.clave)
            )
            self.tabla_clientes.setItem(
                fila, COL_NOMBRE, QtWidgets.QTableWidgetItem(cliente.nombre)
            )
            self.tabla_clientes.setItem(
                fila, COL_DOM, QtWidgets.QTableWidgetItem(cliente.domicilio)
            )
            self.tabla_clientes.setItem(
                fila,
                COL_TELS,
                QtWidgets.QTableWidgetItem(cliente.telefonos)
            )
            cabecera = self.tabla_clientes.horizontalHeader()
            cabecera.setSectionResizeMode(
                COL_CLAVE,
                QtWidgets.QHeaderView.ResizeToContents
            )
            cabecera.setSectionResizeMode(
                COL_NOMBRE,
                QtWidgets.QHeaderView.ResizeToContents
            )
            cabecera.setSectionResizeMode(
                COL_DOM,
                QtWidgets.QHeaderView.ResizeToContents
            )
            cabecera.setSectionResizeMode(
                COL_TELS,
                QtWidgets.QHeaderView.ResizeToContents
            )

    def regresa_cliente(self):
        fila = self.tabla_clientes.currentRow()
        self.tabla_clientes.setCurrentCell(fila, 0)
        indice = self.tabla_clientes.currentItem().text()
        cliente = [x for x in self.clientes if x.clave == indice][0]
        window.carga_cliente(cliente)
        window.combobox_clave_cliente.setCurrentText(indice)
        self.close()

    def busca_clientes(self):
        clave = self.combobox_campos.currentText()
        texto = self.texto_buscar.text()
        if clave == 'Nombre':
            self.clientes = Cliente.get_clientes(nombre=texto)
        elif clave == 'Domicilio':
            self.clientes = Cliente.get_clientes(domicilio=texto)
        elif clave == 'Teléfonos':
            self.clientes = Cliente.get_clientes(telefonos=texto)
        self.llena_lista()


class CatalogoCliente(QDialog):
    def __init__(self, cliente):
        QDialog.__init__(self)
        uic.loadUi('catalogo_cliente.ui', self)
        self.cliente = cliente
        self.contacto = ContactoCliente(clave_cliente=cliente.clave)
        self.carga_cliente()
        self.boton_guardar.clicked.connect(self.guarda_cliente)

    def guarda_cliente(self):
        try:
            self.cliente.clave = self.texto_clave.text()
            self.cliente.nombre = self.texto_nombre_cliente.text()
            self.cliente.domicilio = self.texto_domicilio.text()
            self.cliente.telefonos = self.texto_telefonos.text()
            self.cliente.guardar()
            self.contacto.clave_cliente = self.cliente.clave
            self.contacto.nombre = self.texto_nombre_contacto.text()
            self.contacto.cargo = self.texto_cargo.text()
            self.contacto.movil = self.texto_movil_contacto.text()
            self.contacto.correo = self.texto_correo_contacto.text()
            self.contacto.guardar()
        except GuardadoError:
            error = Error('Se se puede dejar la clave en blanco')
            error.exec_()
        except DuplicadoError:
            error = Error('La clave se encuentra duplicada')
            error.exec_()

    def carga_cliente(self):
        self.texto_clave.setText(self.cliente.clave)
        self.texto_clave.setEnabled(False)
        self.texto_nombre_cliente.setText(self.cliente.nombre)
        self.texto_telefonos.setText(self.cliente.telefonos)
        self.texto_domicilio.setText(self.cliente.domicilio)
        try:
            self.contacto = ContactoCliente.get_contacto_primario(self.cliente)
        except NoResultFound:
            self.vacia_contacto()
        else:
            self.texto_nombre_contacto.setText(self.contacto.nombre)
            self.texto_cargo.setText(self.contacto.cargo)
            self.texto_movil_contacto.setText(self.contacto.movil)
            self.texto_correo_contacto.setText(self.contacto.correo)

    def vacia_contacto(self):
        self.texto_nombre_contacto.clear()
        self.texto_cargo.clear()
        self.texto_movil_contacto.clear()
        self.texto_correo_contacto.clear()


class BusquedaProductos(QDialog):
    def __init__(self):
        QDialog.__init__(self)

        try:
            uic.loadUi('busqueda_productos.ui', self)
            self.boton_buscar.clicked.connect(self.busca_productos)
            self.boton_limpiar.clicked.connect(self.carga_completa)
            self.carga_completa()
        except ErrorConexion:
            raise ErrorConexion

    def carga_completa(self):
        opciones_busqueda = ['Modelo', 'Descripción', 'Marca', 'Proveedor',
                             'Último Costo', 'Moneda Costo', 'Precio Venta',
                             'Moneda Venta', 'Último TE']
        self.texto_buscar.clear()
        try:
            self.productos = Producto.get_productos()
        except OperationalError:
            raise ErrorConexion
        else:
            for opcion in opciones_busqueda:
                self.combobox_campos.addItem(opcion)
            self.llena_lista()


    def llena_lista(self):
        COL_MODELO, COL_DESC, COL_MARCA, COL_PROV, COL_ULTCOS = range(5)
        COL_MONCOS, COL_PRECVEN, COL_MONVEN, COL_ULTE = range(5, 9)
        self.tabla_productos.clearContents()
        self.tabla_productos.setRowCount(0)
        for fila, producto in enumerate(self.productos):
            proveedor = Proveedor.get_proveedor(producto.clave_proveedor)
            moneda_costo = Moneda.get_moneda(producto.clave_moneda_costo)
            moneda_venta = Moneda.get_moneda(producto.clave_moneda_venta)
            self.tabla_productos.insertRow(fila)
            self.tabla_productos.setItem(
                fila,
                COL_MODELO,
                QtWidgets.QTableWidgetItem(producto.modelo)
            )
            self.tabla_productos.setItem(
                fila,
                COL_DESC,
                QtWidgets.QTableWidgetItem(producto.descripcion)
            )
            self.tabla_productos.setItem(
                fila, COL_MARCA, QtWidgets.QTableWidgetItem(producto.marca)
            )
            self.tabla_productos.setItem(
                fila, COL_PROV, QtWidgets.QTableWidgetItem(proveedor.nombre)
            )
            self.tabla_productos.setItem(
                fila,
                COL_ULTCOS,
                QtWidgets.QTableWidgetItem(f'${producto.ultimo_costo:,.2f}')
            )
            self.tabla_productos.setItem(
                fila,
                COL_MONCOS,
                QtWidgets.QTableWidgetItem(moneda_costo.descripcion)
            )
            self.tabla_productos.setItem(
                fila,
                COL_PRECVEN,
                QtWidgets.QTableWidgetItem(f'${producto.precio_venta:,.2f}')
            )
            self.tabla_productos.setItem(
                fila,
                COL_MONVEN,
                QtWidgets.QTableWidgetItem(moneda_venta.descripcion)
            )
            self.tabla_productos.setItem(
                fila, COL_ULTE, QtWidgets.QTableWidgetItem(
                    f'${producto.ultimo_te:,.2f}'
                )
            )

    def busca_productos(self):
        clave = self.combobox_campos.currentText()
        texto = self.texto_buscar.text()
        try:
            if clave == 'Modelo':
                self.productos = Producto.get_productos(modelo=texto)
            elif clave == 'Descripción':
                self.productos = Producto.get_productos(descripcion=texto)
            elif clave == 'Marca':
                self.productos = Producto.get_productos(marca=texto)
            elif clave == 'Proveedor':
                self.productos = Producto.get_productos(proveedor=texto)
            elif clave == 'Último Costo':
                self.productos = Producto.get_productos(ultimo_costo=texto)
            elif clave == 'Moneda Costo':
                self.productos = Producto.get_productos(moneda_costo=texto)
            elif clave == 'Precio Venta':
                self.productos = Producto.get_productos(precio_venta=texto)
            elif clave == 'Moneda Venta':
                self.productos = Producto.get_productos(moneda_venta=texto)
            elif clave == 'Último TE':
                self.productos = Producto.get_productos(ultimo_te=texto)
            self.llena_lista()
        except TipoValorError:
            error = Error('De ingresar un valor numerico')
            error.exec_()


class Combo(QtWidgets.QComboBox):
    def __init__(self, lista):
        super().__init__()
        for elemento in lista:
            self.addItem(elemento)


class Error(QDialog):
    def __init__(self, mensaje):
        QDialog.__init__(self)
        uic.loadUi('dialogoError.ui', self)
        self.label_error.setText(mensaje)
        self.boton_ok.clicked.connect(self.close)


app = QApplication([])
try:
    window = Ventana()
except ErrorConexion:
    error = Error('Hay un problema con la conexión a la base de datos')
    error.exec_()
except FileNotFoundError as fnfe:
    error = Error('Falta un archivo .ui!', fnfe)
    error.exec_()
else:
    window.show()
    app.exec_()

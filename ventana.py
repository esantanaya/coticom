from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtWidgets
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError

import sys
from datetime import date

from modelos import (
    Cotizacion, DetalleCotizacion, Cliente, ContactoCliente, CondicionPago,
    Vigencia, Moneda, Asesor, Nota, Producto, Proveedor
)
from exceptions import ErrorConexion


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
        except OperationalError:
            raise ErrorConexion
        except ErrorConexion:
            raise ErrorConexion

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
            except ErrorConexion:
                raise ErrorConexion

    def carga_clientes(self):
        try:
            clientes = Cliente.get_clientes()
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
        self.label_valor_subtotal.setText('$'+str(self.cotizacion.subtotal))
        self.label_valor_iva.setText('$'+str(self.cotizacion.iva))
        self.label_valor_total.setText('$'+str(self.cotizacion.total))

    def carga_detalles(self):
        try:
            lineas = DetalleCotizacion.get_detalle(self.cotizacion.clave)
        except OperationalError:
            raise ErrorConexion
        else:
            for num, detalle in enumerate(lineas):
                producto = Producto.get_producto(detalle.modelo_producto)
                proveedor = Proveedor.get_proveedor(producto.clave_proveedor)

                self.tabla_detalle.insertRow(num)
                self.tabla_detalle.setItem(
                    num,
                    0,
                    QtWidgets.QTableWidgetItem(str(detalle.linea))
                )
                self.tabla_detalle.setItem(
                    num,
                    1,
                    QtWidgets.QTableWidgetItem(producto.modelo)
                )
                self.tabla_detalle.setItem(
                    num,
                    2,
                    QtWidgets.QTableWidgetItem(producto.descripcion)
                )
                self.tabla_detalle.setItem(
                    num,
                    3,
                    QtWidgets.QTableWidgetItem(producto.marca)
                )
                self.tabla_detalle.setItem(
                    num,
                    4,
                    QtWidgets.QTableWidgetItem(detalle.tiempo_entrega)
                )
                self.tabla_detalle.setItem(
                    num,
                    5,
                    QtWidgets.QTableWidgetItem(str(detalle.cantidad))
                )
                self.tabla_detalle.setItem(
                    num,
                    6,
                    QtWidgets.QTableWidgetItem(str(detalle.precio_unitario))
                )
                self.tabla_detalle.setItem(
                    num,
                    7,
                    QtWidgets.QTableWidgetItem(str(detalle.importe))
                )
                self.tabla_detalle.setItem(
                    num,
                    8,
                    QtWidgets.QTableWidgetItem(proveedor.nombre)
                )
                self.tabla_detalle.setItem(
                    num,
                    9,
                    QtWidgets.QTableWidgetItem(str(producto.ultimo_costo))
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
else:
    window.show()
    app.exec_()

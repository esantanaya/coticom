from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError

import sys
from datetime import date

from modelos import (
    Cotizacion, DetalleCotizacion, Cliente, ContactoCliente, CondicionPago,
    Vigencia, Moneda, Asesor, Nota
)
from exceptions import ErrorConexion


class Ventana(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        try:
            uic.loadUi('ventana.ui', self)
            self.control_fecha.setDate(date.today())
            cotizacion = Cotizacion.get_ultima_cotizacion()
            self.texto_id.setText(str(cotizacion.clave))
            clientes = Cliente.get_clientes()
            self.carga_clientes(clientes)
            self.combobox_clave_cliente.currentIndexChanged.connect(self.cambia_combo_cliente)
            self.combobox_clave_cliente.setCurrentIndex(1)
            self.carga_datos()
        except OperationalError:
            raise ErrorConexion

    def cambia_combo_cliente(self):
        if len(self.combobox_clave_cliente.currentText()) > 0:
            cliente = Cliente.get_cliente(self.combobox_clave_cliente.currentText())
            self.carga_cliente(cliente)

    def carga_clientes(self, clientes):
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
        self.texto_nombre_contacto.setText('')
        self.texto_cargo.setText('')
        self.texto_movil_contacto.setText('')
        self.texto_correo_contacto.setText('')

    def carga_datos(self):
        self.carga_condiciones()
        self.carga_vigencias()
        self.carga_moneda()
        self.carga_asesores()
        self.carga_notas()

    def carga_notas(self):
        notas = Nota.get_notas()

        for nota in notas:
            self.combobox_nota1.addItem(nota.descripcion)
            self.combobox_nota2.addItem(nota.descripcion)

    def carga_asesores(self):
        asesores = Asesor.get_asesores()

        for asesor in asesores:
            self.combobox_asesor.addItem(asesor.nombre)

    def carga_moneda(self):
        monedas = Moneda.get_monedas()

        for moneda in monedas:
            self.combobox_moneda.addItem(moneda.clave)

    def carga_vigencias(self):
        vigencias = Vigencia.get_vigencias()

        for vigencia in vigencias:
            self.combobox_vigencia.addItem(vigencia.descripcion)

    def carga_condiciones(self):
        condiciones = CondicionPago.get_condiciones()
        for condicion in condiciones:
            self.combobox_condiciones.addItem(condicion.descripcion)


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

from sqlalchemy import (Boolean, Column, Date, ForeignKey, Integer, Numeric,
                        Sequence, String, Table, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()
con_string = 'postgresql+psycopg2://postgres:4cP#4j9R92@localhost:5432/pruebas'
engine = create_engine(con_string)
Session = sessionmaker(bind=engine)
session = Session()


class Proveedor(Base):
    __tablename__ = 'proveedores'

    clave = Column(String(5), primary_key=True)
    nombre = Column(String(200), index=True)
    telefonos = Column(String(50))
    domicilio = Column(String(500))

    @classmethod
    def get_proveedor(cls, clave):
        proveedor = session.query(cls).filter(cls.clave == clave).one()
        return proveedor


class ContactoProveedor(Base):
    __tablename__ = 'contactos_proveedores'

    consecutivo_secuencia = Sequence(
        'consecutivo_proveedor', metadata=Base.metadata
    )

    clave_proveedor = Column(
        String(5),
        ForeignKey('proveedores.clave', ondelete='RESTRICT',
                   onupdate='RESTRICT'),
        primary_key=True
    )
    consecutivo = Column(
        Integer(),
        consecutivo_secuencia,
        server_default=consecutivo_secuencia.next_value(),
        primary_key=True
    )
    principal = Column(Boolean)
    cargo = Column(String(100))
    correo = Column(String(50))
    movil = Column(String(15))

    proveedor = relationship(
        'Proveedor',
        backref=backref('contactos_proveedores'),
        order_by=clave_proveedor
    )


class Cliente(Base):
    __tablename__ = 'clientes'

    clave = Column(String(5), primary_key=True)
    nombre = Column(String(200), index=True)
    telefonos = Column(String(50))
    domicilio = Column(String(500))

    @classmethod
    def get_cliente(cls, clave):
        cliente = session.query(cls).filter(cls.clave == clave).one()
        return cliente

    @classmethod
    def get_clientes(cls):
        clientes = session.query(cls.clave).all()
        return clientes

    def __repr__(self):
        return f'Cliente: {self.clave}, {self.nombre}'


class ContactoCliente(Base):
    __tablename__ = 'contactos_clientes'

    consecutivo_secuencia = Sequence(
        'consecutivo_cliente', metadata=Base.metadata
    )

    clave_cliente = Column(
        String(5),
        ForeignKey('clientes.clave', ondelete='RESTRICT', onupdate='RESTRICT'),
        primary_key=True
    )
    consecutivo = Column(
        Integer,
        consecutivo_secuencia,
        server_default=consecutivo_secuencia.next_value(),
        primary_key=True
    )
    principal = Column(Boolean())
    nombre = Column(String(100))
    cargo = Column(String(50))
    correo = Column(String(50))
    movil = Column(String(15))

    cliente = relationship(
        'Cliente',
        backref=backref('contactos_clientes'),
        order_by=clave_cliente
    )

    @classmethod
    def get_contacto_primario(cls, cliente):
        contacto = session.query(cls).filter(
            cliente.clave == cls.clave_cliente,
            cls.principal == True
        ).one()
        return contacto


class Moneda(Base):
    __tablename__ = 'monedas'

    clave = Column(String(5), primary_key=True)
    descripcion = Column(String(100))

    @classmethod
    def get_monedas(cls):
        monedas = session.query(cls).all()
        return monedas

    @classmethod
    def get_moneda(cls, clave):
        moneda = session.query(cls).filter(cls.clave == clave).one()
        return moneda


class Producto(Base):
    __tablename__ = 'productos'

    modelo = Column(String(50), primary_key=True)
    descripcion = Column(String(200))
    marca = Column(String(50))
    clave_proveedor = Column(String(5),
                             ForeignKey('proveedores.clave',
                                        ondelete='RESTRICT', onupdate='RESTRICT')
                             )
    ultimo_costo = Column(Numeric())
    clave_moneda_costo = Column(String(5),
                                ForeignKey(
                                    'monedas.clave', ondelete='RESTRICT', onupdate='RESTRICT')
                                )
    precio_venta = Column(Numeric())
    clave_moneda_venta = Column(String(5),
                                ForeignKey(
                                    'monedas.clave', ondelete='RESTRICT', onupdate='RESTRICT')
                                )
    ultimo_te = Column(Numeric())

    @classmethod
    def get_producto(cls, modelo):
        producto = session.query(cls).filter(cls.modelo == modelo).one()
        return producto


class Correo(Base):
    __tablename__ = 'correos'

    clave = Column(Integer(), primary_key=True)
    correo = Column(String(50))


class CondicionPago(Base):
    __tablename__ = 'condiciones_pago'

    clave_secuencia = Sequence('clave_condiciones', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    descripcion = Column(String(100))

    @classmethod
    def get_condiciones(cls):
        condiciones = session.query(cls).all()
        return condiciones

    @classmethod
    def get_condicione(cls, clave):
        condicion = session.query(cls).filter(cls.clave == clave).one()
        return condicion


class Vigencia(Base):
    __tablename__ = 'vigencias'

    clave_secuencia = Sequence('clave_vigencias', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    descripcion = Column(String(100))

    @classmethod
    def get_vigencias(cls):
        vigencias = session.query(cls).all()
        return vigencias

    @classmethod
    def get_vigencia(cls, clave):
        vigencia = session.query(cls).filter(cls.clave == clave).one()
        return vigencia


class Nota(Base):
    __tablename__ = 'notas'

    clave_secuencia = Sequence('clave_notas', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    descripcion = Column(String(100))

    @classmethod
    def get_notas(cls):
        notas = session.query(cls).all()
        return notas

    @classmethod
    def get_nota(cls, clave):
        nota = session.query(cls).filter(cls.clave == clave).one()
        return nota


class Asesor(Base):
    __tablename__ = 'asesores'

    clave_secuencia = Sequence('clave_notas', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    nombre = Column(String(100))
    correo = Column(String(50))
    movil = Column(String(15))

    @classmethod
    def get_asesores(cls):
        asesores = session.query(cls).all()
        return asesores

    @classmethod
    def get_asesor(cls, clave):
        asesor = session.query(cls).filter(cls.clave == clave).one()
        return asesor


class Cotizacion(Base):
    __tablename__ = 'cotizaciones'

    cotizacion_secuencia = Sequence('clave_cotizacion', metadata=Base.metadata)

    clave = Column(
        Integer(),
        cotizacion_secuencia,
        server_default=cotizacion_secuencia.next_value(),
        primary_key=True
    )
    fecha = Column(Date())
    clave_cliente = Column(
        String(5),
        ForeignKey('clientes.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_condiciones_pago = Column(
        Integer(),
        ForeignKey(
            'condiciones_pago.clave', ondelete='RESTRICT', onupdate='RESTRICT'
        )
    )
    clave_vigencia = Column(
        Integer(),
        ForeignKey(
            'vigencias.clave', ondelete='RESTRICT', onupdate='RESTRICT'
        )
    )
    clave_moneda = Column(
        String(5),
        ForeignKey('monedas.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_asesor = Column(
        Integer(),
        ForeignKey('asesores.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_nota_1 = Column(
        Integer(),
        ForeignKey('notas.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_nota_2 = Column(
        Integer(),
        ForeignKey('notas.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    subtotal = Column(Numeric())
    iva = Column(Numeric())
    total = Column(Numeric())

    def get_cotizaciones(self):
        cotizaciones = session.query(Cotizacion).all()
        return cotizaciones

    @classmethod
    def get_ultima_cotizacion(cls):
        cotizacion = session.query(cls).order_by(cls.clave.desc()).first()
        return cotizacion


class DetalleCotizacion(Base):
    __tablename__ = 'detalle_cotizacion'

    linea_secuencia = Sequence('linea_cotizacion', metadata=Base.metadata)

    clave_cotizacion = Column(
        Integer(),
        ForeignKey('cotizaciones.clave',
                   ondelete='RESTRICT', onupdate='RESTRICT'),
        primary_key=True
    )
    linea = Column(
        Integer(),
        linea_secuencia,
        server_default=linea_secuencia.next_value(),
        primary_key=True
    )
    modelo_producto = Column(
        String(50),
        ForeignKey('productos.modelo', ondelete='RESTRICT',
                   onupdate='RESTRICT')
    )
    tiempo_entrega = Column(String(20))
    cantidad = Column(Integer())
    precio_unitario = Column(Numeric())
    importe = Column(Numeric())

    @classmethod
    def get_detalle(cls, clave_cotizacion):
        detalle = session.query(cls).filter(
            cls.clave_cotizacion == clave_cotizacion
        ).all()
        return detalle


class UsoCFDI(Base):
    __tablename__ = 'usos_cfdi'

    clave_secuencia = Sequence('clave_usos', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    descripcion = Column(String(100))


class FormaPago(Base):
    __tablename__ = 'formas_pago'

    clave_secuencia = Sequence('clave_formas', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    descripcion = Column(String(100))


class Credito(Base):
    __tablename__ = 'creditos'

    clave_secuencia = Sequence('clave_creditos', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    descripcion = Column(String(100))


class MetodoPago(Base):
    __tablename__ = 'metodos_pago'

    clave_secuencia = Sequence('clave_metodos', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    descripcion = Column(String(100))


class CuentaBancaria(Base):
    __tablename__ = 'cuentas_bancarias'

    clave_secuencia = Sequence(
        'clave_cuentas_bancarias', metadata=Base.metadata)

    clave = Column(
        Integer(),
        clave_secuencia,
        server_default=clave_secuencia.next_value(),
        primary_key=True
    )
    banco = Column(String(20))
    sucursal = Column(String(20))
    cuenta = Column(String(20))
    clabe = Column(String(20))
    clave_moneda = Column(
        String(5),
        ForeignKey('monedas.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )


class Compra(Base):
    __tablename__ = 'compras'

    compra_secuencia = Sequence('clave_compra', metadata=Base.metadata)

    clave = Column(
        Integer(),
        compra_secuencia,
        server_default=compra_secuencia.next_value(),
        primary_key=True
    )
    fecha = Column(Date())
    clave_cotizacion = Column(
        Integer(),
        ForeignKey('cotizaciones.clave',
                   ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_proveedor = Column(
        String(5),
        ForeignKey('proveedores.clave',
                   ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_forma_pago = Column(
        Integer(),
        ForeignKey('formas_pago.clave',
                   ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_cuenta_banco = Column(
        Integer(),
        ForeignKey(
            'cuentas_bancarias.clave', ondelete='RESTRICT', onupdate='RESTRICT'
        )
    )
    clave_moneda = Column(
        String(5),
        ForeignKey('monedas.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_autoriza = Column(
        Integer(),
        ForeignKey('asesores.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_uso_cfdi = Column(
        Integer(),
        ForeignKey('usos_cfdi.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_metodo_pago = Column(
        Integer(),
        ForeignKey('metodos_pago.clave',
                   ondelete='RESTRICT', onupdate='RESTRICT')
    )
    clave_credito = Column(
        Integer(),
        ForeignKey('creditos.clave', ondelete='RESTRICT', onupdate='RESTRICT')
    )
    subtotal = Column(Numeric())
    iva = Column(Numeric())
    total = Column(Numeric())


class DetalleCompra(Base):
    __tablename__ = 'detalle_compra'

    linea_secuencia = Sequence('linea_compra', metadata=Base.metadata)

    clave_compra = Column(
        Integer(),
        ForeignKey('compras.clave', ondelete='RESTRICT', onupdate='RESTRICT'),
        primary_key=True
    )
    linea = Column(
        Integer(),
        linea_secuencia,
        server_default=linea_secuencia.next_value(),
        primary_key=True
    )
    modelo_producto = Column(
        String(50),
        ForeignKey('productos.modelo', ondelete='RESTRICT',
                   onupdate='RESTRICT')
    )
    tiempo_entrega = Column(String(20))
    cantidad = Column(Integer())
    precio_unitario = Column(Numeric())
    importe = Column(Numeric())


if __name__ == '__main__':
    Base.metadata.create_all(engine)

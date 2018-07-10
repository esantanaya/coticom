from sqlalchemy import Table, Column, String, Integer, Numeric, Boolean, ForeignKey, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from bd import Conexion

Base = declarative_base()


class Proveedor(Base):
    __tablename__ = 'proveedores'

    clave = Column(String(5), primary_key=True)
    nombre = Column(String(200), index=True)
    telefonos = Column(String(50))
    domicilio = Column(String(500))


class ContactoProveedor(Base):
    __tablename__ = 'contactos_proveedores'

    clave_proveedor = Column(
        String(5), ForeignKey('proveedores.clave'), primary_key=True
    )
    consecutivo = Column(
        Integer(), Sequence('consecutivo_proveedor'), primary_key=True
    )
    principal = Column(Boolean())
    cargo = Column(String(100))
    correo = Column(String(50))
    movil = Column(String(15))

    proveedor = relationship(
        'Proveedor',
        backref=backref('contactos_proveedores'),
        order_by=clave_proveedor
    )


class Moneda(Base):
    __tablename__ = 'monedas'

    clave = Column(String(5), primary_key=True)
    descripcion = Column(String(100))


class Producto(Base):
    __tablename__ = 'productos'

    modelo = Column(String(50), primary_key=True)
    descripcion = Column(String(200))
    marca = Column(String(50))
    clave_proveedor = Column(String(5), ForeignKey('proveedores.clave'))
    ultimo_costo = Column(Numeric())

if __name__ == '__main__':
    Base.metadata.create_all(Conexion().engine)

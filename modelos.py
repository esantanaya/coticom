class Producto:

    def __init__(
        self,
        modelo,
        descripcion,
        marca,
        proveedor,
        ultimo_costo,
        moneda_costo,
        precio_venta,
        moneda_venta,
        ultimo_te
    ):
        self._modelo = modelo
        self._descripcion = descripcion
        self._marca = marca
        self._proveedor = proveedor
        self._ultimo_costo = ultimo_costo
        self._moneda_costo = moneda_costo
        self._precio_venta = precio_venta
        self._moneda_venta = moneda_venta
        self._ultimo_te = ultimo_te

        @property
        def modelo(self):
            return self._modelo

        @modelo.setter
        def modelo(self, modelo):
            self._modelo = modelo

        @property
        def descripcion(self):
            return self._descripcion

        @descripcion.setter
        def descripcion(self, descripcion):
            self._descripcion = descripcion

        @property
        def marca(self):
            return self._marca

        @marca.setter
        def marca(self, marca):
            self._marca  = marca

        @property
        def proveedor(self):
            return self._proveedor

        @proveedor.setter
        def proveedor(self, proveedor):
            self._proveedor = proveedor

        @property
        def ultimo_costo(self):
            return self._ultimo_costo

        @ultimo_costo.setter
        def ultimo_costo(self, ultimo_costo):
            self._ultimo_costo = ultimo_costo

        @property
        def moneda_costo(self):
            return self._moneda_costo

        @moneda_costo.setter
        def moneda_costo(self, moneda_costo):
            self._moneda_costo = moneda_costo

        @property
        def precio_venta(self):
            return self._precio_venta

        @precio_venta.setter
        def precio_venta(self, precio_venta):
            self._precio_venta = precio_venta

        @property
        def moneda_venta(self):
            return self._moneda_venta

        @moneda_venta.setter
        def moneda_venta(self, moneda_venta):
            self._moneda_venta = moneda_venta

        @property
        def ultimo_te(self):
            return self._ultimo_te

        @ultimo_te.setter
        def ultimo_te(self, ultimo_te):
            self._ultimo_te = ultimo_te

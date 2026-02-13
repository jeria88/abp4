from abc import ABC, abstractmethod
import re
from utils.excepciones import ValidationError

class Cliente(ABC):
    """Clase abstracta que representa un cliente en el sistema (v1.2)."""
    
    def __init__(self, rut, nombre, email, telefono, direccion):
        # Validaciones estáticas
        Cliente.validar_rut(rut)
        Cliente.validar_email(email)
        Cliente.validar_telefono(telefono)
        
        self._id_cliente = None # Se asignará por el Gestor
        self._rut = rut
        self._nombre = nombre
        self._email = email
        self._telefono = telefono
        self._direccion = direccion

    @abstractmethod
    def obtener_perfil(self):
        """Retorna una descripción del perfil del cliente."""
        pass

    @staticmethod
    def validar_email(email):
        # RFC 5322 compliant-ish regex
        patron = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(patron, email):
            raise ValidationError(f"Email inválido: '{email}'. Debe seguir el formato nombre@dominio.com")

    @staticmethod
    def validar_telefono(tel):
        patron = r"^\+?\d{8,15}$"
        if not re.match(patron, tel):
            raise ValidationError(f"Teléfono inválido: '{tel}'. Debe contener entre 8 y 15 dígitos numéricos (opcional '+' al inicio).")

    @staticmethod
    def validar_rut(rut):
        # Validación básica de RUT para v1.2
        patron = r"^(\d{1,3}(?:\.?\d{3})*)-[\dkK]$"
        if not re.match(patron, rut):
             raise ValidationError(f"RUT inválido: '{rut}'. Formato esperado: 12345678-9 o 12.345.678-9")

    def __str__(self):
        return f"ID: {self._id_cliente} | RUT: {self._rut} | Nombre: {self._nombre} | Email: {self._email}"

    def __eq__(self, other):
        if not isinstance(other, Cliente):
            return False
        # Igualdad basada en ID si existe, sino en RUT que es único legalmente
        if self._id_cliente and other._id_cliente:
            return self._id_cliente == other._id_cliente
        return self._rut == other._rut

    @property
    def id_cliente(self): return self._id_cliente
    @id_cliente.setter
    def id_cliente(self, valor):
        if self._id_cliente is not None:
             raise ValidationError("El ID del cliente no puede modificarse una vez asignado.")
        self._id_cliente = int(valor)

    @property
    def rut(self): return self._rut
    @property
    def nombre(self): return self._nombre
    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise ValidationError("El nombre no puede estar vacío.")
        self._nombre = valor
    @property
    def email(self): return self._email
    @property
    def telefono(self): return self._telefono
    @property
    def direccion(self): return self._direccion


class ClienteRegular(Cliente):
    def __init__(self, rut, nombre, email, telefono, direccion):
        super().__init__(rut, nombre, email, telefono, direccion)

    def obtener_perfil(self):
        return "Cliente Regular"


class ClientePremium(Cliente):
    def __init__(self, rut, nombre, email, telefono, direccion):
        super().__init__(rut, nombre, email, telefono, direccion)
        self._descuento = 0.30

    def obtener_perfil(self):
        return f"Cliente Premium (Descuento: {int(self._descuento * 100)}%)"

    @property
    def descuento(self): return self._descuento


class ClienteCorporativo(Cliente):
    def __init__(self, rut, nombre, email, telefono, direccion, ejecutivo_asignado, razon_social):
        super().__init__(rut, nombre, email, telefono, direccion)
        self._ejecutivo_asignado = ejecutivo_asignado
        self._razon_social = razon_social

    def obtener_perfil(self):
        return f"Cliente Corporativo (Empresa: {self._razon_social}, Ejecutivo: {self._ejecutivo_asignado})"

    @property
    def ejecutivo_asignado(self): return self._ejecutivo_asignado
    @property
    def razon_social(self): return self._razon_social

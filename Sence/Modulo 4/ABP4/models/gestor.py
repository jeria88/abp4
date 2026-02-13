import json
import os
from .cliente import Cliente, ClienteRegular, ClientePremium, ClienteCorporativo
from utils.excepciones import PersistenceError

class GestorClientes:
    """Clase que gestiona la persistencia y lógica de clientes (v1.2)."""
    
    def __init__(self, archivo_json):
        self._lista_clientes = []
        self._archivo_json = archivo_json
        self._ultimo_id = 0
        self.cargar_desde_json()

    def _generar_id(self):
        """Genera un nuevo ID autoincremental."""
        self._ultimo_id += 1
        return self._ultimo_id

    def agregar_cliente(self, c: Cliente):
        # Verificar duplicados por RUT (que es único)
        for cliente_existente in self._lista_clientes:
            if cliente_existente.rut == c.rut:
                raise PersistenceError(f"Ya existe un cliente con RUT {c.rut}")
        
        # Asignar ID autoincremental
        c.id_cliente = self._generar_id()
        self._lista_clientes.append(c)
        self.guardar_en_json()

    def eliminar_cliente(self, id_cliente: int):
        cliente = self.buscar_cliente(id_cliente)
        if not cliente:
            raise PersistenceError(f"Cliente con ID {id_cliente} no encontrado.")
        self._lista_clientes.remove(cliente)
        self.guardar_en_json()

    def actualizar_cliente(self, id_cliente: int, nuevos_datos: dict):
        cliente = self.buscar_cliente(id_cliente)
        if not cliente:
            raise PersistenceError(f"Cliente con ID {id_cliente} no encontrado.")
        
        if 'nombre' in nuevos_datos and nuevos_datos['nombre']:
            cliente.nombre = nuevos_datos['nombre']
        if 'email' in nuevos_datos and nuevos_datos['email']:
            Cliente.validar_email(nuevos_datos['email'])
            cliente._email = nuevos_datos['email']
        if 'telefono' in nuevos_datos and nuevos_datos['telefono']:
            Cliente.validar_telefono(nuevos_datos['telefono'])
            cliente._telefono = nuevos_datos['telefono']
        if 'direccion' in nuevos_datos and nuevos_datos['direccion']:
            cliente._direccion = nuevos_datos['direccion']
            
        self.guardar_en_json()

    def buscar_cliente(self, id_cliente: int) -> Cliente:
        for c in self._lista_clientes:
            if c.id_cliente == id_cliente:
                return c
        return None

    def listar_todos(self):
        return self._lista_clientes

    def guardar_en_json(self):
        try:
            os.makedirs(os.path.dirname(self._archivo_json), exist_ok=True)
            data = []
            for c in self._lista_clientes:
                item = {
                    "id": c.id_cliente,
                    "rut": c.rut,
                    "nombre": c.nombre,
                    "email": c.email,
                    "telefono": c.telefono,
                    "direccion": c.direccion,
                    "tipo": type(c).__name__
                }
                
                if isinstance(c, ClientePremium):
                    item["descuento"] = c.descuento
                elif isinstance(c, ClienteCorporativo):
                    item["ejecutivo_asignado"] = c.ejecutivo_asignado
                    item["razon_social"] = c.razon_social
                
                data.append(item)
                
            with open(self._archivo_json, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise PersistenceError(f"Error guardando datos: {e}")

    def cargar_desde_json(self):
        if not os.path.exists(self._archivo_json):
            return

        try:
            with open(self._archivo_json, 'r') as f:
                data = json.load(f)
                
            self._lista_clientes = []
            max_id = 0
            
            for item in data:
                tipo = item.get("tipo")
                try:
                    # Constructor v1.2: rut, nombre, email, telefono, direccion
                    # id se asigna después
                    rut = item["rut"]
                    nombre = item["nombre"]
                    email = item["email"]
                    telefono = item["telefono"]
                    direccion = item["direccion"]
                    id_c = int(item["id"])
                    
                    if id_c > max_id:
                        max_id = id_c
                        
                    if tipo == "ClienteRegular":
                        c = ClienteRegular(rut, nombre, email, telefono, direccion)
                    elif tipo == "ClientePremium":
                        c = ClientePremium(rut, nombre, email, telefono, direccion)
                    elif tipo == "ClienteCorporativo":
                        c = ClienteCorporativo(rut, nombre, email, telefono, direccion, item["ejecutivo_asignado"], item["razon_social"])
                    else:
                        continue
                    
                    # Forzar asignación de ID recuperado
                    c._id_cliente = id_c 
                    self._lista_clientes.append(c)
                except KeyError:
                    continue # Skip partial/bad data
            
            self._ultimo_id = max_id
            
        except Exception as e:
            print(f"Error cargando base de datos: {e}")
            self._lista_clientes = []

import os
import sys
import logging
from models.gestor import GestorClientes
from models.cliente import Cliente, ClienteRegular, ClientePremium, ClienteCorporativo
from utils.excepciones import GICException

# Configuración de Logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'gic_errors.log'),
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_titulo(titulo):
    print("\n" + "="*40)
    print(f" {titulo}".center(40))
    print("="*40 + "\n")

def menu_principal():
    imprimir_titulo("GIC v1.2 - Menú Principal")
    print("1. Agregar Cliente")
    print("2. Listar Clientes")
    print("3. Buscar Cliente")
    print("4. Actualizar Cliente")
    print("5. Eliminar Cliente")
    print("6. Salir")
    return input("\nSeleccione una opción: ")

def mostrar_tabla_ids(gestor):
    """Muestra una tabla rápida de IDs y Nombres para facilitar selección."""
    clientes = gestor.listar_todos()
    if not clientes:
        print("\n[!] No hay clientes registrados para seleccionar.")
        return False
    
    print("\n--- Lista Rápida de Clientes ---")
    print(f"{'ID':<5} | {'RUT':<12} | {'Nombre'}")
    print("-" * 35)
    for c in clientes:
        print(f"{c.id_cliente:<5} | {c.rut:<12} | {c.nombre}")
    print("-" * 35 + "\n")
    return True

def solicitar_dato_validado(mensaje, funcion_validacion=None):
    """Solicita un dato al usuario y lo valida inmediatamente si se provee función."""
    while True:
        valor = input(mensaje).strip()
        if not funcion_validacion:
            if valor: return valor
            print("[!] El campo no puede estar vacío.")
            continue
            
        try:
            # Si la validación pasa (no lanza excepción), retornamos el valor
            funcion_validacion(valor)
            return valor
        except GICException as e:
            print(f"[X] {e}")
            print("Intente nuevamente.\n")

def agregar_cliente_interactivo(gestor):
    imprimir_titulo("Agregar Nuevo Cliente (v1.2)")
    
    print("Tipos de Cliente:")
    print("1. Regular")
    print("2. Premium")
    print("3. Corporativo")
    tipo_sel = input("Seleccione tipo (1-3): ")
    if tipo_sel not in ['1', '2', '3']:
        print("\n[!] Tipo de cliente inválido.")
        return
    
    try:
        # Solicitar datos con validación inmediata
        rut = solicitar_dato_validado("RUT (ej. 12.345.678-9): ", Cliente.validar_rut)
        nombre = solicitar_dato_validado("Nombre: ", None) # Validación simple de no vacío
        email = solicitar_dato_validado("Email: ", Cliente.validar_email)
        telefono = solicitar_dato_validado("Teléfono: ", Cliente.validar_telefono)
        direccion = solicitar_dato_validado("Dirección: ", None)
        
        cliente = None
        
        if tipo_sel == '1':
            cliente = ClienteRegular(rut, nombre, email, telefono, direccion)
        elif tipo_sel == '2':
            cliente = ClientePremium(rut, nombre, email, telefono, direccion)
        elif tipo_sel == '3':
            ejecutivo = solicitar_dato_validado("Ejecutivo Asignado: ", None)
            razon_social = solicitar_dato_validado("Razón Social: ", None)
            cliente = ClienteCorporativo(rut, nombre, email, telefono, direccion, ejecutivo, razon_social)

        gestor.agregar_cliente(cliente)
        print(f"\n[OK] Cliente {nombre} agregado exitosamente con ID: {cliente.id_cliente}")
        
    except GICException as e:
        logging.error(f"ErrorGIC al agregar cliente: {e}")
        print(f"\n[X] Error al guardar: {e}")
    except Exception as e:
        logging.error(f"Error inesperado al agregar cliente: {e}", exc_info=True)
        print(f"\n[X] Error inesperado: {e}")

def listar_clientes_interactivo(gestor):
    imprimir_titulo("Listado de Clientes")
    clientes = gestor.listar_todos()
    if not clientes:
        print("No hay clientes registrados.")
    else:
        for c in clientes:
            print(f"- [ID: {c.id_cliente}] {c.obtener_perfil()}")
            print(f"  RUT: {c.rut} | {c.nombre} | {c.email}")
            print("-" * 20)

def buscar_cliente_interactivo(gestor):
    imprimir_titulo("Buscar Cliente")
    if not mostrar_tabla_ids(gestor):
        return

    try:
        id_str = input("Ingrese ID del cliente a buscar: ").strip()
        if not id_str.isdigit():
            print("\n[!] El ID debe ser un número entero.")
            return
            
        id_cliente = int(id_str)
        cliente = gestor.buscar_cliente(id_cliente)
        if cliente:
            print("\n[OK] Cliente Encontrado:")
            print(cliente)
            print(cliente.obtener_perfil())
        else:
            print(f"\n[!] Cliente con ID {id_cliente} no encontrado.")
    except Exception as e:
        print(f"\n[X] Error inválido.")

def actualizar_cliente_interactivo(gestor):
    imprimir_titulo("Actualizar Cliente")
    if not mostrar_tabla_ids(gestor):
        return

    try:
        id_str = input("Ingrese ID del cliente a actualizar: ").strip()
        if not id_str.isdigit():
            print("\n[!] El ID debe ser un número entero.")
            return

        id_cliente = int(id_str)
        cliente = gestor.buscar_cliente(id_cliente)
        
        if not cliente:
            print(f"\n[!] Cliente con ID {id_cliente} no encontrado.")
            return

        print(f"Editando a: {cliente.nombre} (RUT: {cliente.rut})")
        print("Deje en blanco los campos que no desee modificar.")
        
        nuevos_datos = {}
        nombre = input(f"Nuevo Nombre ({cliente.nombre}): ").strip()
        if nombre: nuevos_datos['nombre'] = nombre
        
        email = input(f"Nuevo Email ({cliente.email}): ").strip()
        if email: nuevos_datos['email'] = email
        
        telefono = input(f"Nuevo Teléfono ({cliente.telefono}): ").strip()
        if telefono: nuevos_datos['telefono'] = telefono
        
        direccion = input(f"Nueva Dirección ({cliente.direccion}): ").strip()
        if direccion: nuevos_datos['direccion'] = direccion
        
        if not nuevos_datos:
            print("\n[!] No se ingresaron cambios.")
            return

        gestor.actualizar_cliente(id_cliente, nuevos_datos)
        print(f"\n[OK] Cliente actualizado exitosamente.")
    except GICException as e:
        logging.error(f"ErrorGIC al actualizar cliente: {e}")
        print(f"\n[X] Error al actualizar: {e}")
    except ValueError:
        print("\n[!] Error: Entrada no válida.")

def eliminar_cliente_interactivo(gestor):
    imprimir_titulo("Eliminar Cliente")
    if not mostrar_tabla_ids(gestor):
        return

    try:
        id_str = input("Ingrese ID del cliente a eliminar: ").strip()
        if not id_str.isdigit():
            print("\n[!] El ID debe ser un número entero.")
            return

        id_cliente = int(id_str)
        
        if not gestor.buscar_cliente(id_cliente):
            print(f"\n[!] Cliente con ID {id_cliente} no encontrado.")
            return

        confirmacion = input(f"¿Está seguro de eliminar al cliente ID {id_cliente}? (s/n): ").lower()
        if confirmacion == 's':
            gestor.eliminar_cliente(id_cliente)
            print(f"\n[OK] Cliente eliminado correctamenete.")
        else:
            print("\n[!] Operación cancelada.")
    except GICException as e:
        logging.error(f"ErrorGIC al eliminar cliente: {e}")
        print(f"\n[X] Error al eliminar: {e}")
    except ValueError:
         print("\n[!] Error: Entrada no válida.")

def main():
    # Setup de paths para persistencia relativa
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    archivo_db = os.path.join(BASE_DIR, 'data', 'clientes.json')
    gestor = GestorClientes(archivo_db)

    while True:
        opcion = menu_principal()
        
        if opcion == '1':
            agregar_cliente_interactivo(gestor)
        elif opcion == '2':
            listar_clientes_interactivo(gestor)
        elif opcion == '3':
            buscar_cliente_interactivo(gestor)
        elif opcion == '4':
            actualizar_cliente_interactivo(gestor)
        elif opcion == '5':
            eliminar_cliente_interactivo(gestor)
        elif opcion == '6':
            print("\nSaliendo del sistema...")
            break
        else:
            print("\n[!] Opción inválida.")
        
        input("\nPresione Enter para continuar...")
        limpiar_pantalla()

if __name__ == "__main__":
    main()

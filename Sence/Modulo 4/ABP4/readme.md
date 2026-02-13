# Gestor Inteligente de Clientes (GIC) v1.2

## Descripción del Proyecto
El **Gestor Inteligente de Clientes (GIC)** es una solución de software desarrollada en Python para la empresa *Solution Tech*. Su objetivo es modernizar la administración de clientes mediante un sistema escalable, modular y basado en **Programación Orientada a Objetos (POO)**.


## Características Principales 
- **Identificadores Autoincrementales**: Gestión automática de IDs únicos para cada cliente, independientes de su RUT.
- **RUT como Atributo Distinto**: Separación lógica entre el identificador del sistema y el documento nacional de identidad.
- **Validación Inmediata**: El sistema valida formatos (Email, RUT, Teléfono) al momento de la entrada de datos, proporcionando retroalimentación instantánea.
- **Jerarquía de Clientes**: Implementación de herencia y polimorfismo con tipos `Regular`, `Premium` (con descuento) y `Corporativo`(con ejecutivo).
- **Persistencia JSON**: Almacenamiento seguro y estructurado de la base de datos de clientes.

## Justificación de Módulos 

El diseño del sistema responde a los requerimientos técnicos y de negocio planteados por la empresa *Solution Tech*:

### 1. Modelo Orientado a Objetos (`models/`)
- **Archivo**: `cliente.py`
    - *Justificación*: Cumple con la exigencia de **Herencia y Polimorfismo**. Se define una clase abstracta `Cliente` que encapsula atributos comunes y lógica de validación, de la cual heredan `ClienteRegular`, `ClientePremium` y `ClienteCorporativo`.
    - *Encapsulación*: Uso de atributos protegidos (`_nombre`, `_rut`) y propiedades (`@property`) para controlar el acceso y modificación de datos.
    
- **Archivo**: `gestor.py`
    - *Justificación*: Centraliza la lógica de negocio y la **Persistencia de Datos**. Maneja la colección de objetos cliente y orquesta las operaciones CRUD, asegurando que los cambios se reflejen en el archivo JSON.

### 2. Manejo de Errores (`utils/`)
- **Archivo**: `excepciones.py`
    - *Justificación*: Responde al requerimiento de **Manejo de Errores y Excepciones**. Se definen excepciones personalizadas (`GICException`, `ValidationError`, `PersistenceError`) para permitir un control granular de los fallos del sistema, separando errores de validación de problemas de infraestructura.

### 3. Interfaz de Usuario (`main.py`)
- *Justificación*: Provee la interacción con el usuario final. Se implementa una **Validación de Datos en Interfaz** mejorada, asegurando que solo datos correctos lleguen al modelo de negocio.




## Estructura de Archivos
```
ABP4/
├── main.py                 # CLI Interactivo (Punto de entrada)
├── readme.md               # Documentación Oficial
├── models/
│   ├── cliente.py          # Definición de Clases (Cliente, Regular, Premium, Corporativo)
│   └── gestor.py           # Lógica de Negocio y Persistencia JSON
├── utils/
│   ├── excepciones.py      # Excepciones Personalizadas
└── data/
    └── clientes.json       # Base de Datos (Generada Automáticamente)
```

## Instalación y Ejecución
1. Asegúrese de tener Python 3 instalado.
2. Navegue a la carpeta raíz del proyecto.
3. Ejecute el siguiente comando:
   ```bash
   python3 ./main.py
   ```

class GICException(Exception):
    """Excepción base para el sistema GIC."""
    pass

class ValidationError(GICException):
    """Excepción lanzada cuando falla una validación de datos."""
    pass

class PersistenceError(GICException):
    """Excepción lanzada cuando hay errores en la persistencia de datos."""
    pass

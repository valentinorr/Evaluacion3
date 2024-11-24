from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Ingrediente

def crear_ingrediente(session: Session, nombre: str, tipo: str, cantidad: int, unidad: str):
    """Crea un nuevo ingrediente si no existe uno con el mismo nombre y tipo."""
    try:
        nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
        session.add(nuevo_ingrediente)
        session.commit()
        return {"status": "success", "message": "Ingrediente creado exitosamente."}
    except IntegrityError:
        session.rollback()
        return {"status": "error", "message": "Ya existe un ingrediente con ese nombre y tipo."}

def obtener_ingredientes(session: Session):
    """Obtiene todos los ingredientes registrados."""
    return session.query(Ingrediente).all()

def actualizar_ingrediente(session: Session, id: int, nombre: str = None, tipo: str = None, cantidad: int = None, unidad: str = None):
    """Actualiza los campos de un ingrediente por ID."""
    ingrediente = session.query(Ingrediente).get(id)
    if not ingrediente:
        return {"status": "error", "message": "Ingrediente no encontrado."}
    if nombre:
        ingrediente.nombre = nombre
    if tipo:
        ingrediente.tipo = tipo
    if cantidad is not None:
        ingrediente.cantidad = cantidad
    if unidad:
        ingrediente.unidad = unidad
    try:
        session.commit()
        return {"status": "success", "message": "Ingrediente actualizado exitosamente."}
    except IntegrityError:
        session.rollback()
        return {"status": "error", "message": "Ya existe un ingrediente con ese nombre y tipo."}

def eliminar_ingrediente(session: Session, id: int):
    """Elimina un ingrediente por ID."""
    ingrediente = session.query(Ingrediente).get(id)
    if not ingrediente:
        return {"status": "error", "message": "Ingrediente no encontrado."}
    session.delete(ingrediente)
    session.commit()
    return {"status": "success", "message": "Ingrediente eliminado exitosamente."}

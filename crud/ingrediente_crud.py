from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Ingrediente

def crear_ingrediente(session, nombre, tipo, cantidad):
    """Crea un nuevo ingrediente."""
    nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad)
    session.add(nuevo_ingrediente)
    session.commit()
    return {"status": "success", "message": "Ingrediente creado exitosamente."}


def obtener_ingredientes(session):
    return session.query(Ingrediente.id, Ingrediente.nombre, Ingrediente.tipo, Ingrediente.cantidad).all()


def actualizar_ingrediente(session, ingrediente_id, nombre, tipo, cantidad):
    """Actualiza un ingrediente existente."""
    ingrediente = session.query(Ingrediente).get(ingrediente_id)
    if not ingrediente:
        return {"status": "error", "message": "Ingrediente no encontrado."}
    ingrediente.nombre = nombre
    ingrediente.tipo = tipo
    ingrediente.cantidad = cantidad
    session.commit()
    return {"status": "success", "message": "Ingrediente actualizado exitosamente."}

def eliminar_ingrediente(session: Session, id: int):
    """Elimina un ingrediente por ID."""
    ingrediente = session.query(Ingrediente).get(id)
    if not ingrediente:
        return {"status": "error", "message": "Ingrediente no encontrado."}
    session.delete(ingrediente)
    session.commit()
    return {"status": "success", "message": "Ingrediente eliminado exitosamente."}

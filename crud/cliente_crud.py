from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Cliente

def crear_cliente(session: Session, nombre: str, correo: str):
    """Crea un nuevo cliente con nombre y correo únicos."""
    try:
        nuevo_cliente = Cliente(nombre=nombre, correo=correo)
        session.add(nuevo_cliente)
        session.commit()
        return {"status": "success", "message": "Cliente creado exitosamente."}
    except IntegrityError:
        session.rollback()
        return {"status": "error", "message": "El correo ya está en uso por otro cliente."}

def obtener_clientes(session: Session):
    """Obtiene todos los clientes registrados."""
    return session.query(Cliente).all()

def actualizar_cliente(session: Session, id: int, nombre: str = None, correo: str = None):
    """Actualiza los datos de un cliente por ID."""
    cliente = session.query(Cliente).get(id)
    if not cliente:
        return {"status": "error", "message": "Cliente no encontrado."}
    if nombre:
        cliente.nombre = nombre
    if correo:
        cliente.correo = correo
    try:
        session.commit()
        return {"status": "success", "message": "Cliente actualizado exitosamente."}
    except IntegrityError:
        session.rollback()
        return {"status": "error", "message": "El correo ya está en uso por otro cliente."}

def eliminar_cliente(session: Session, id: int):
    """Elimina un cliente por ID."""
    cliente = session.query(Cliente).get(id)
    if not cliente:
        return {"status": "error", "message": "Cliente no encontrado."}
    session.delete(cliente)
    session.commit()
    return {"status": "success", "message": "Cliente eliminado exitosamente."}

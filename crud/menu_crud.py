from sqlalchemy.orm import Session
from models import Menu, Ingrediente, menu_ingrediente

def crear_menu(session: Session, nombre: str, descripcion: str, precio: float, ingredientes: list):
    """
    Crea un nuevo menú con ingredientes.
    - ingredientes: lista de tuplas (ingrediente_id, cantidad_requerida).
    """
    nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, precio=precio)
    session.add(nuevo_menu)
    session.flush()  # Obtener el ID del menú antes de asociar los ingredientes

    for ingrediente_id, cantidad_requerida in ingredientes:
        session.execute(
            menu_ingrediente.insert().values(
                menu_id=nuevo_menu.id,
                ingrediente_id=ingrediente_id,
                cantidad_requerida=cantidad_requerida
            )
        )
    session.commit()
    return {"status": "success", "message": "Menú creado exitosamente."}


def obtener_menus(session: Session):
    """Obtiene todos los menús registrados."""
    return session.query(Menu).all()

def actualizar_menu(session: Session, menu_id: int, nombre: str = None, descripcion: str = None, precio: float = None, ingredientes: list = None):
    """Actualiza los datos de un menú."""
    menu = session.query(Menu).get(menu_id)
    if not menu:
        return {"status": "error", "message": "Menú no encontrado."}
    if nombre:
        menu.nombre = nombre
    if descripcion:
        menu.descripcion = descripcion
    if precio is not None:
        menu.precio = precio
    if ingredientes:
        session.execute(
            menu_ingrediente.delete().where(menu_ingrediente.c.menu_id == menu_id)
        )
        for ingrediente_id, cantidad in ingredientes:
            session.execute(
                menu_ingrediente.insert().values(
                    menu_id=menu_id,
                    ingrediente_id=ingrediente_id,
                    cantidad_requerida=cantidad
                )
            )
    session.commit()
    return {"status": "success", "message": "Menú actualizado exitosamente."}

def eliminar_menu(session: Session, menu_id: int):
    """Elimina un menú por ID."""
    menu = session.query(Menu).get(menu_id)
    if not menu:
        return {"status": "error", "message": "Menú no encontrado."}
    session.query(menu_ingrediente).filter_by(menu_id=menu_id).delete()
    session.delete(menu)
    session.commit()
    return {"status": "success", "message": "Menú eliminado exitosamente."}

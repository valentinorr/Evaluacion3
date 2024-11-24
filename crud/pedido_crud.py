from sqlalchemy.orm import Session
from models import Pedido, PedidoMenu, Cliente, Menu

def crear_pedido(session: Session, cliente_id: int, menus: list, fecha: str):
    """
    Crea un nuevo pedido asociado a un cliente.
    - menus: lista de tuplas (menu_id, cantidad).
    """
    cliente = session.query(Cliente).get(cliente_id)
    if not cliente:
        return {"status": "error", "message": "Cliente no encontrado."}

    nuevo_pedido = Pedido(cliente_id=cliente_id, fecha=fecha)
    session.add(nuevo_pedido)

    for menu_id, cantidad in menus:
        menu = session.query(Menu).get(menu_id)
        if not menu:
            session.rollback()
            return {"status": "error", "message": f"Menú con ID {menu_id} no encontrado."}
        if cantidad <= 0:
            session.rollback()
            return {"status": "error", "message": "La cantidad debe ser mayor a 0."}

        pedido_menu = PedidoMenu(
            pedido_id=nuevo_pedido.id,
            menu_id=menu_id,
            cantidad=cantidad
        )
        session.add(pedido_menu)

    session.commit()
    return {"status": "success", "message": "Pedido creado exitosamente."}

def obtener_pedidos(session: Session):
    """Obtiene todos los pedidos registrados."""
    return session.query(Pedido).all()

def actualizar_pedido(session: Session, id: int, menus: list = None):
    """Actualiza los menús de un pedido por ID."""
    pedido = session.query(Pedido).get(id)
    if not pedido:
        return {"status": "error", "message": "Pedido no encontrado."}

    if menus:
        session.query(PedidoMenu).filter_by(pedido_id=pedido.id).delete()
        for menu_id, cantidad in menus:
            menu = session.query(Menu).get(menu_id)
            if not menu or cantidad <= 0:
                session.rollback()
                return {"status": "error", "message": "Datos inválidos en los menús."}
            pedido_menu = PedidoMenu(
                pedido_id=pedido.id,
                menu_id=menu_id,
                cantidad=cantidad
            )
            session.add(pedido_menu)

    session.commit()
    return {"status": "success", "message": "Pedido actualizado exitosamente."}

def eliminar_pedido(session: Session, id: int):
    """Elimina un pedido por ID."""
    pedido = session.query(Pedido).get(id)
    if not pedido:
        return {"status": "error", "message": "Pedido no encontrado."}
    session.query(PedidoMenu).filter_by(pedido_id=pedido.id).delete()
    session.delete(pedido)
    session.commit()
    return {"status": "success", "message": "Pedido eliminado exitosamente."}

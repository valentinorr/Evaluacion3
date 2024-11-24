import matplotlib.pyplot as plt
from database import get_db
from sqlalchemy import func
from models import Pedido, PedidoMenu, Menu

def obtener_ventas_diarias():
    """
    Obtiene las ventas diarias desde la base de datos.
    """
    session = next(get_db())
    ventas = session.query(
        func.date(Pedido.fecha).label("fecha"),
        func.count(Pedido.id).label("cantidad")
    ).group_by(func.date(Pedido.fecha)).all()
    return [(venta.fecha, venta.cantidad) for venta in ventas]

def obtener_menus_mas_vendidos():
    """
    Obtiene los menús más vendidos desde la base de datos.
    """
    session = next(get_db())
    ventas = session.query(
        Menu.nombre,
        func.sum(PedidoMenu.cantidad).label("cantidad")
    ).join(PedidoMenu).group_by(Menu.id).order_by(func.sum(PedidoMenu.cantidad).desc()).all()
    return [(venta.nombre, venta.cantidad) for venta in ventas]

def obtener_uso_ingredientes():
    """
    Obtiene el uso de ingredientes desde la base de datos.
    """
    session = next(get_db())
    ingredientes = session.query(
        Menu.nombre,
        func.sum(PedidoMenu.cantidad).label("cantidad")
    ).join(PedidoMenu).group_by(Menu.id).all()
    return [(ingrediente.nombre, ingrediente.cantidad) for ingrediente in ingredientes]

# Las funciones de graficado permanecen igual.
def graficar_ventas_diarias(ventas):
    fechas = [venta[0] for venta in ventas]
    cantidades = [venta[1] for venta in ventas]
    plt.figure(figsize=(10, 6))
    plt.bar(fechas, cantidades, color='skyblue')
    plt.title("Ventas Diarias")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad de Ventas")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graficar_menus_mas_vendidos(menus):
    nombres = [menu[0] for menu in menus]
    cantidades = [menu[1] for menu in menus]
    plt.figure(figsize=(10, 6))
    plt.bar(nombres, cantidades, color="orange")
    plt.title("Menús Más Vendidos")
    plt.xlabel("Menú")
    plt.ylabel("Cantidad Vendida")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graficar_uso_ingredientes(ingredientes):
    nombres = [ingrediente[0] for ingrediente in ingredientes]
    cantidades = [ingrediente[1] for ingrediente in ingredientes]
    plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=nombres, autopct='%1.1f%%', startangle=90)
    plt.title("Uso de Ingredientes")
    plt.tight_layout()
    plt.show()

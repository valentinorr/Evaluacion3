from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Tabla de asociación entre Menú e Ingredientes
menu_ingrediente = Table(
    'menu_ingrediente',
    Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
    Column('cantidad_requerida', Integer, nullable=False)  # Cantidad necesaria del ingrediente
)


class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    ingredientes = relationship(
        'Ingrediente',
        secondary=menu_ingrediente,
        back_populates='menus'
    )

Ingrediente.menus = relationship(
    'Menu',
    secondary=menu_ingrediente,
    back_populates='ingredientes'
)

Ingrediente.menus = relationship(
    "Menu",
    secondary=menu_ingrediente,
    back_populates="ingredientes"
)

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente")

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    fecha = Column(String, nullable=False)  # Formato de fecha ISO 8601
    cliente = relationship("Cliente", back_populates="pedidos")
    menus = relationship("PedidoMenu", back_populates="pedido")

class PedidoMenu(Base):
    __tablename__ = 'pedido_menu'
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    menu_id = Column(Integer, ForeignKey('menus.id'))
    cantidad = Column(Integer, nullable=False)
    pedido = relationship("Pedido", back_populates="menus")
    menu = relationship("Menu")

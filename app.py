import customtkinter as ctk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from sqlalchemy.orm import sessionmaker
from database import engine
from crud.ingrediente_crud import *
from crud.menu_crud import *
from crud.cliente_crud import *
from crud.pedido_crud import *
from fpdf import FPDF

Session = sessionmaker(bind=engine)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Restaurante")
        self.geometry("900x700")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Paneles
        self.ingredientes_panel = IngredientesPanel(self.notebook)
        self.menus_panel = MenusPanel(self.notebook)
        self.clientes_panel = ClientesPanel(self.notebook)
        self.compras_panel = ComprasPanel(self.notebook)

        self.notebook.add(self.ingredientes_panel, text="Ingredientes")
        self.notebook.add(self.menus_panel, text="Menús")
        self.notebook.add(self.clientes_panel, text="Clientes")
        self.notebook.add(self.compras_panel, text="Compras")


class IngredientesPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Tabla de ingredientes
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Tipo", "Cantidad", "Unidad"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.pack(fill="both", expand=True)

        # Campos para agregar ingredientes
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = ctk.CTkEntry(form_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Tipo:").grid(row=0, column=2, padx=5, pady=5)
        self.tipo_entry = ctk.CTkEntry(form_frame)
        self.tipo_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        self.cantidad_entry = ctk.CTkEntry(form_frame)
        self.cantidad_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Unidad:").grid(row=1, column=2, padx=5, pady=5)
        self.unidad_entry = ctk.CTkEntry(form_frame)
        self.unidad_entry.grid(row=1, column=3, padx=5, pady=5)

        # Botones para agregar y eliminar
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        self.agregar_button = ctk.CTkButton(button_frame, text="Agregar", command=self.agregar_ingrediente)
        self.agregar_button.pack(side="left", padx=10, pady=10)

        self.eliminar_button = ctk.CTkButton(button_frame, text="Eliminar", command=self.eliminar_ingrediente)
        self.eliminar_button.pack(side="left", padx=10, pady=10)

        self.load_ingredientes()

    def load_ingredientes(self):
        """Carga todos los ingredientes en la tabla."""
        session = Session()
        ingredientes = obtener_ingredientes(session)
        self.tree.delete(*self.tree.get_children())  # Limpiar tabla
        for ingrediente in ingredientes:
            self.tree.insert("", "end", values=(ingrediente.id, ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad))
        session.close()

    def agregar_ingrediente(self):
        """Agrega un nuevo ingrediente usando los datos del formulario."""
        nombre = self.nombre_entry.get()
        tipo = self.tipo_entry.get()
        cantidad = self.cantidad_entry.get()
        unidad = self.unidad_entry.get()

        if not nombre or not tipo or not cantidad or not unidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        try:
            cantidad = int(cantidad)
            session = Session()
            resultado = crear_ingrediente(session, nombre, tipo, cantidad, unidad)
            session.close()
            if resultado["status"] == "success":
                self.load_ingredientes()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", resultado["message"])
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")

    def eliminar_ingrediente(self):
        """Elimina el ingrediente seleccionado en la tabla."""
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un ingrediente para eliminar.")
            return

        item = self.tree.item(seleccionado)
        ingrediente_id = item["values"][0]

        session = Session()
        resultado = eliminar_ingrediente(session, ingrediente_id)
        session.close()
        if resultado["status"] == "success":
            self.load_ingredientes()
        else:
            messagebox.showerror("Error", resultado["message"])

    def limpiar_formulario(self):
        """Limpia los campos del formulario."""
        self.nombre_entry.delete(0, "end")
        self.tipo_entry.delete(0, "end")
        self.cantidad_entry.delete(0, "end")
        self.unidad_entry.delete(0, "end")


class MenusPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Tabla de menús
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Precio", text="Precio")
        self.tree.pack(fill="both", expand=True)

        # Campos para agregar menús
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = ctk.CTkEntry(form_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Descripción:").grid(row=0, column=2, padx=5, pady=5)
        self.descripcion_entry = ctk.CTkEntry(form_frame)
        self.descripcion_entry.grid(row=0, column=3, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Precio:").grid(row=1, column=0, padx=5, pady=5)
        self.precio_entry = ctk.CTkEntry(form_frame)
        self.precio_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Ingredientes (ID,Cantidad):").grid(row=1, column=2, padx=5, pady=5)
        self.ingredientes_entry = ctk.CTkEntry(form_frame)
        self.ingredientes_entry.grid(row=1, column=3, padx=5, pady=5)

        # Botones para agregar y eliminar
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        self.agregar_button = ctk.CTkButton(button_frame, text="Agregar", command=self.agregar_menu)
        self.agregar_button.pack(side="left", padx=10, pady=10)

        self.eliminar_button = ctk.CTkButton(button_frame, text="Eliminar", command=self.eliminar_menu)
        self.eliminar_button.pack(side="left", padx=10, pady=10)

        self.load_menus()

    def load_menus(self):
        """Carga todos los menús en la tabla."""
        session = Session()
        menus = obtener_menus(session)
        self.tree.delete(*self.tree.get_children())  # Limpiar tabla
        for menu in menus:
            self.tree.insert("", "end", values=(menu.id, menu.nombre, menu.descripcion, menu.precio))
        session.close()

    def agregar_menu(self):
        """Agrega un nuevo menú usando los datos del formulario."""
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()
        precio = self.precio_entry.get()
        ingredientes = self.ingredientes_entry.get()

        if not nombre or not descripcion or not precio or not ingredientes:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            precio = float(precio)
            # Parsear los ingredientes ingresados
            ingredientes_list = []
            for ingrediente in ingredientes.split(";"):
                ingrediente_id, cantidad = map(int, ingrediente.split(","))
                ingredientes_list.append((ingrediente_id, cantidad))

            session = Session()
            resultado = crear_menu(session, nombre, descripcion, precio, ingredientes_list)
            session.close()
            if resultado["status"] == "success":
                self.load_menus()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", resultado["message"])
        except ValueError:
            messagebox.showerror("Error", "Verifique que los campos de precio e ingredientes estén correctos.")

    def eliminar_menu(self):
        """Elimina el menú seleccionado en la tabla."""
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un menú para eliminar.")
            return

        item = self.tree.item(seleccionado)
        menu_id = item["values"][0]

        session = Session()
        resultado = eliminar_menu(session, menu_id)
        session.close()
        if resultado["status"] == "success":
            self.load_menus()
        else:
            messagebox.showerror("Error", resultado["message"])

    def limpiar_formulario(self):
        """Limpia los campos del formulario."""
        self.nombre_entry.delete(0, "end")
        self.descripcion_entry.delete(0, "end")
        self.precio_entry.delete(0, "end")
        self.ingredientes_entry.delete(0, "end")

    def reducir_ingredientes(self, ingredientes):
        """Reduce las cantidades de los ingredientes utilizados en un menú."""
        session = Session()
        for ingrediente_id, cantidad in ingredientes:
            ingrediente = session.query(Ingrediente).get(ingrediente_id)
            if ingrediente:
                if ingrediente.cantidad < cantidad:
                    session.rollback()
                    messagebox.showerror("Error", f"No hay suficiente cantidad del ingrediente {ingrediente.nombre}.")
                    return
                ingrediente.cantidad -= cantidad
        session.commit()
        session.close()
        messagebox.showinfo("Éxito", "Ingredientes actualizados exitosamente.")



class ClientesPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Tabla de clientes
        self.tree = ttk.Treeview(self, columns=("ID", "Nombre", "Correo"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo")
        self.tree.pack(fill="both", expand=True)

        # Campos para agregar clientes
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.nombre_entry = ctk.CTkEntry(form_frame)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(form_frame, text="Correo:").grid(row=0, column=2, padx=5, pady=5)
        self.correo_entry = ctk.CTkEntry(form_frame)
        self.correo_entry.grid(row=0, column=3, padx=5, pady=5)

        # Botones para agregar y eliminar
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=5)

        self.agregar_button = ctk.CTkButton(button_frame, text="Agregar", command=self.agregar_cliente)
        self.agregar_button.pack(side="left", padx=10, pady=10)

        self.eliminar_button = ctk.CTkButton(button_frame, text="Eliminar", command=self.eliminar_cliente)
        self.eliminar_button.pack(side="left", padx=10, pady=10)

        self.load_clientes()

    def load_clientes(self):
        """Carga todos los clientes en la tabla."""
        session = Session()
        clientes = obtener_clientes(session)
        self.tree.delete(*self.tree.get_children())  # Limpiar tabla
        for cliente in clientes:
            self.tree.insert("", "end", values=(cliente.id, cliente.nombre, cliente.correo))
        session.close()

    def agregar_cliente(self):
        """Agrega un nuevo cliente usando los datos del formulario."""
        nombre = self.nombre_entry.get()
        correo = self.correo_entry.get()

        if not nombre or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        session = Session()
        resultado = crear_cliente(session, nombre, correo)
        session.close()
        if resultado["status"] == "success":
            self.load_clientes()
            self.limpiar_formulario()
        else:
            messagebox.showerror("Error", resultado["message"])

    def eliminar_cliente(self):
        """Elimina el cliente seleccionado en la tabla."""
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar.")
            return

        item = self.tree.item(seleccionado)
        cliente_id = item["values"][0]

        session = Session()
        resultado = eliminar_cliente(session, cliente_id)
        session.close()
        if resultado["status"] == "success":
            self.load_clientes()
        else:
            messagebox.showerror("Error", resultado["message"])

    def limpiar_formulario(self):
        """Limpia los campos del formulario."""
        self.nombre_entry.delete(0, "end")
        self.correo_entry.delete(0, "end")

class ComprasPanel(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Combobox para seleccionar cliente
        self.cliente_combo = ttk.Combobox(self, state="readonly")
        self.cliente_combo.grid(row=0, column=0, padx=10, pady=10)
        self.load_clientes()

        # Tabla para seleccionar menús
        self.menus_tree = ttk.Treeview(self, columns=("ID", "Nombre", "Precio"), show="headings")
        self.menus_tree.heading("ID", text="ID")
        self.menus_tree.heading("Nombre", text="Nombre")
        self.menus_tree.heading("Precio", text="Precio")
        self.menus_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.load_menus()

        # Botón para agregar menús al carrito
        self.agregar_button = ctk.CTkButton(self, text="Agregar al carrito", command=self.agregar_al_carrito)
        self.agregar_button.grid(row=2, column=0, padx=10, pady=10)

        # Tabla para mostrar el carrito
        self.carrito_tree = ttk.Treeview(self, columns=("ID", "Nombre", "Cantidad", "Precio Total"), show="headings")
        self.carrito_tree.heading("ID", text="ID")
        self.carrito_tree.heading("Nombre", text="Nombre")
        self.carrito_tree.heading("Cantidad", text="Cantidad")
        self.carrito_tree.heading("Precio Total", text="Precio Total")
        self.carrito_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Botón para generar boleta
        self.comprar_button = ctk.CTkButton(self, text="Generar Boleta", command=self.generar_boleta)
        self.comprar_button.grid(row=4, column=0, padx=10, pady=10)

        # Carrito de compras
        self.carrito = []

    def load_clientes(self):
        """Carga los clientes en el combobox."""
        session = Session()
        clientes = obtener_clientes(session)
        self.cliente_combo["values"] = [f"{cliente.id} - {cliente.nombre}" for cliente in clientes]
        session.close()

    def load_menus(self):
        """Carga los menús en la tabla."""
        session = Session()
        menus = obtener_menus(session)
        self.menus_tree.delete(*self.menus_tree.get_children())  # Limpiar tabla
        for menu in menus:
            self.menus_tree.insert("", "end", values=(menu.id, menu.nombre, menu.precio))
        session.close()

    def agregar_al_carrito(self):
        """Agrega un menú seleccionado al carrito."""
        seleccionado = self.menus_tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione un menú para agregar al carrito.")
            return

        item = self.menus_tree.item(seleccionado)
        menu_id, nombre, precio = item["values"]

        # Ventana emergente para ingresar la cantidad
        cantidad = simpledialog.askinteger("Cantidad", f"Ingrese la cantidad de '{nombre}' a agregar:", minvalue=1)
        if not cantidad:
            return

        # Calcular precio total del menú
        precio_total = float(precio) * cantidad

        # Agregar al carrito
        self.carrito.append({"menu_id": menu_id, "nombre": nombre, "cantidad": cantidad, "precio_total": precio_total})
        self.actualizar_carrito()

    def actualizar_carrito(self):
        """Actualiza la tabla del carrito con los datos actuales."""
        self.carrito_tree.delete(*self.carrito_tree.get_children())
        for item in self.carrito:
            self.carrito_tree.insert("", "end", values=(item["menu_id"], item["nombre"], item["cantidad"], item["precio_total"]))



    def generar_boleta(self, archivo_pdf="boleta.pdf"):
        """Genera un PDF de boleta con los datos del carrito y guarda el pedido en la base de datos."""
        cliente_seleccionado = self.cliente_combo.get()
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Seleccione un cliente para realizar el pedido.")
            return

        if not self.carrito:
            messagebox.showerror("Error", "El carrito está vacío.")
            return

        # Obtener el ID y nombre del cliente
        cliente_id, cliente_nombre = cliente_seleccionado.split(" - ")
        cliente_id = int(cliente_id)

        # Crear el pedido en la base de datos
        menus = [(item["menu_id"], item["cantidad"]) for item in self.carrito]
        session = Session()
        try:
            from datetime import datetime
            fecha_actual = datetime.now().isoformat()
            resultado = crear_pedido(session, cliente_id, menus, fecha_actual)
            if resultado["status"] != "success":
                raise ValueError(resultado["message"])

            # Crear el PDF de la boleta
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Información del restaurante
            pdf.cell(200, 10, txt="Restaurante XYZ", ln=True, align="C")
            pdf.cell(200, 10, txt="RUT: 99.999.999-9", ln=True, align="C")
            pdf.cell(200, 10, txt="Dirección: Calle Falsa 123", ln=True, align="C")
            pdf.cell(200, 10, txt="Teléfono: +56 9 9999 9999", ln=True, align="C")
            pdf.cell(200, 10, txt="=================================", ln=True, align="C")

            # Información del cliente
            pdf.cell(200, 10, txt=f"Cliente: {cliente_nombre}", ln=True, align="L")
            pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="L")

            # Tabla de pedidos
            pdf.cell(100, 10, txt="Menú", border=1)
            pdf.cell(40, 10, txt="Cantidad", border=1)
            pdf.cell(50, 10, txt="Precio Total", border=1, ln=True)

            subtotal = 0
            for item in self.carrito:
                pdf.cell(100, 10, txt=item["nombre"], border=1)
                pdf.cell(40, 10, txt=str(item["cantidad"]), border=1)
                pdf.cell(50, 10, txt=f"${item['precio_total']:.2f}", border=1, ln=True)
                subtotal += item["precio_total"]

            # Cálculos de total, IVA y subtotal
            iva = subtotal * 0.19
            total = subtotal + iva

            pdf.cell(200, 10, txt="=================================", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Subtotal: ${subtotal:.2f}", ln=True)
            pdf.cell(200, 10, txt=f"IVA (19%): ${iva:.2f}", ln=True)
            pdf.cell(200, 10, txt=f"Total: ${total:.2f}", ln=True)

            # Guardar el archivo PDF
            pdf.output(archivo_pdf)

            messagebox.showinfo("Éxito", f"Boleta generada: {archivo_pdf}")
            self.carrito = []  # Vaciar carrito
            self.actualizar_carrito()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"No se pudo realizar el pedido: {e}")
        finally:
            session.close()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

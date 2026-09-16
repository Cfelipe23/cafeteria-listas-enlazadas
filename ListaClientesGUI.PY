import tkinter as tk
from tkinter import messagebox, ttk

# --- 1. ESTRUCTURA DE DATOS: NODO ---
class NodoTicket:
    def __init__(self, numero, cliente, asunto):
        self.numero = numero
        self.cliente = cliente
        self.asunto = asunto
        self.siguiente = None

# --- 2. ESTRUCTURA DE DATOS: LISTA ENLAZADA (CRUD) ---
class ListaEsperaTickets:
    def __init__(self):
        self.cabeza = None

    # [C] - CREAR: Insertar al final de la lista enlazada
    def insertar(self, numero, cliente, asunto):
        # Programación Defensiva (Fail-Fast)
        if not cliente or not str(cliente).strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        if not asunto or not str(asunto).strip():
            raise ValueError("El asunto del ticket no puede estar vacío.")
        nuevo_nodo = NodoTicket(numero, cliente, asunto)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            return
        
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo_nodo

    # [R] - LEER: Generador de datos puros sin listas nativas de Python (Regla Crítica)
    def obtener_todos(self):
        actual = self.cabeza
        while actual:
            # Reemplazamos '[]' y '.append()' devolviendo una tupla mediante yield
            yield (actual.numero, actual.cliente, actual.asunto)
            actual = actual.siguiente

    # [U] - ACTUALIZAR: Buscar el nodo por número de ticket y modificar sus campos
    def actualizar(self, numero, nuevo_cliente, nuevo_asunto):
        # Validaciones estrictas antes de alterar memoria
        if not nuevo_cliente or not str(nuevo_cliente).strip():
            raise ValueError("No se puede actualizar con un cliente vacío.")
        if not nuevo_asunto or not str(nuevo_asunto).strip():
            raise ValueError("No se puede actualizar con un asunto vacío.")
        actual = self.cabeza
        while actual:
            if actual.numero == numero:
                actual.cliente = nuevo_cliente
                actual.asunto = nuevo_asunto
                return True
            actual = actual.siguiente
        return False

    # [D] - ELIMINAR: Romper los enlaces para quitar un ticket específico
    def eliminar(self, numero):
        if not self.cabeza:
            return False
        
        # Caso especial: Si el ticket a eliminar está en la cabeza
        if self.cabeza.numero == numero:
            self.cabeza = self.cabeza.siguiente
            return True
            
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.numero == numero:
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
        return False

# --- 3. INTERFAZ GRÁFICA (TKINTER) ---
class AppTickets:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Tickets - Lista Enlazada")
        self.root.geometry("650x450")
        
        # Instancia de nuestra estructura de datos de listas enlazadas
        self.lista_tickets = ListaEsperaTickets()
        self.contador_ticket = 100 # Inicio del consecutivo de tickets

        # --- PANEL DEL FORMULARIO (IZQUIERDA) ---
        frame_form = tk.LabelFrame(root, text="Datos del Ticket", padx=10, pady=10)
        frame_form.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(frame_form, text="Nombre Cliente:").pack(anchor=tk.W)
        self.txt_cliente = tk.Entry(frame_form, width=25)
        self.txt_cliente.pack(pady=5)

        tk.Label(frame_form, text="Asunto / Motivo:").pack(anchor=tk.W)
        self.txt_asunto = tk.Entry(frame_form, width=25)
        self.txt_asunto.pack(pady=5)

        # Botones de Operación del CRUD
        self.btn_crear = tk.Button(frame_form, text="Registrar Ticket [C]", bg="#4CAF50", fg="white", command=self.crear_ticket)
        self.btn_crear.pack(fill=tk.X, pady=5)

        self.btn_actualizar = tk.Button(frame_form, text="Modificar Seleccionado [U]", bg="#2196F3", fg="white", command=self.actualizar_ticket)
        self.btn_actualizar.pack(fill=tk.X, pady=5)

        self.btn_eliminar = tk.Button(frame_form, text="Atender / Eliminar [D]", bg="#f44336", fg="white", command=self.eliminar_ticket)
        self.btn_eliminar.pack(fill=tk.X, pady=5)
        
        self.btn_limpiar = tk.Button(frame_form, text="Limpiar Campos", command=self.limpiar_campos)
        self.btn_limpiar.pack(fill=tk.X, pady=5)

        # --- PANEL DE LA TABLA [R] (DERECHA) ---
        frame_tabla = tk.LabelFrame(root, text="Fila de Espera Activa", padx=10, pady=10)
        frame_tabla.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración de los componentes visuales de la tabla
        self.tabla = ttk.Treeview(frame_tabla, columns=("Número", "Cliente", "Asunto"), show="headings")
        self.tabla.heading("Número", text="N° Ticket")
        self.tabla.heading("Cliente", text="Cliente")
        self.tabla.heading("Asunto", text="Asunto")
        
        self.tabla.column("Número", width=70, anchor=tk.CENTER)
        self.tabla.column("Cliente", width=150)
        self.tabla.column("Asunto", width=180)
        
        self.tabla.pack(fill=tk.BOTH, expand=True)
        
        # Evento para cuando el usuario hace clic en una fila de la tabla
        self.tabla.bind("<<TreeviewSelect>>", self.cargar_seleccion)

    # --- FUNCIONES DE CONTROL ---
    
    def actualizar_tabla(self):
        # Borra el Treeview visualmente
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        # Recorre la lista enlazada real [R - Leer] y dibuja de nuevo la fila en pantalla
        for t in self.lista_tickets.obtener_todos():
            self.tabla.insert("", tk.END, values=t)

    def crear_ticket(self):
        cliente = self.txt_cliente.get().strip()
        asunto = self.txt_asunto.get().strip()
        
        if cliente == "" or asunto == "":
            messagebox.showwarning("Campos Vacíos", "Por favor llena todos los campos.")
            return
        
        self.contador_ticket += 1
        try:
            # CORREGIDO: Llama correctamente al método 'insertar' envuelto en try-except
            self.lista_tickets.insertar(self.contador_ticket, cliente, asunto)
            self.actualizar_tabla()
            self.limpiar_campos()
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
            self.contador_ticket -= 1 # Revertir el contador

    def cargar_seleccion(self, event):
        # Toma los datos de la fila presionada y los escribe en los campos de texto
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            valores = item["values"]
            
            self.txt_cliente.delete(0, tk.END)
            self.txt_cliente.insert(0, valores[1]) # Posición 1 es el nombre del cliente
            self.txt_asunto.delete(0, tk.END)
            self.txt_asunto.insert(0, valores[2])  # Posición 2 es el asunto

    def actualizar_ticket(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Selecciona un ticket de la tabla para modificar.")
            return
        
        valores = self.tabla.item(seleccion)["values"]
        numero = int(valores[0]) # Posición 0 es el identificador único numérico
        nuevo_cliente = self.txt_cliente.get().strip()
        nuevo_asunto = self.txt_asunto.get().strip()
        
        try:
            if self.lista_tickets.actualizar(numero, nuevo_cliente, nuevo_asunto):
                messagebox.showinfo("Éxito", f"Ticket #{numero} actualizado de la memoria.")
                self.actualizar_tabla()
                self.limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo actualizar.")
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))

    def eliminar_ticket(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Selecciona el ticket que deseas atender o borrar.")
            return
        
        valores = self.tabla.item(seleccion)["values"]
        numero = int(valores[0])
        
        if self.lista_tickets.eliminar(numero):
            messagebox.showinfo("Eliminado", f"Ticket #{numero} removido de la Lista Enlazada.")
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "No se pudo eliminar.")

    def limpiar_campos(self):
        self.txt_cliente.delete(0, tk.END)
        self.txt_asunto.delete(0, tk.END)
        self.tabla.selection_remove(self.tabla.selection())

# --- 4. ARRANQUE DE LA APLICACIÓN ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AppTickets(root)
    root.mainloop()

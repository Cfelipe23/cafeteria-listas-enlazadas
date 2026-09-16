import tkinter as tk
from tkinter import ttk, messagebox
from lista_pedidos import ListaPedidos

class CafeteriaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cafetería - Estructuras de Datos")
        self.root.geometry("950x550")
        
        self.lista = ListaPedidos()
        self.selected_id = None
        
        self.configurar_ui()
        
    def configurar_ui(self):
        # Panel Izquierdo (Formulario y Controles)
        panel_izquierdo = tk.Frame(self.root, padx=15, pady=15, width=320)
        panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y)
        
        # --- SECCIÓN: NUEVO PEDIDO ---
        marco_crear = tk.LabelFrame(panel_izquierdo, text="Nuevo Pedido", padx=10, pady=10)
        marco_crear.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(marco_crear, text="Cliente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_cliente = tk.Entry(marco_crear, width=22)
        self.ent_cliente.grid(row=0, column=1, pady=5)
        
        tk.Label(marco_crear, text="Rol:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cmb_rol = ttk.Combobox(marco_crear, values=["Estudiante", "Profesor"], state="readonly", width=19)
        self.cmb_rol.current(0)
        self.cmb_rol.grid(row=1, column=1, pady=5)
        
        tk.Label(marco_crear, text="Productos:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ent_productos = tk.Entry(marco_crear, width=22)
        self.ent_productos.grid(row=2, column=1, pady=5)
        
        btn_crear = tk.Button(marco_crear, text="Crear Pedido", command=self.accion_crear, bg="#4CAF50", fg="white", font=("Arial", 9, "bold"))
        btn_crear.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
                
        # --- SECCIÓN: GESTIÓN DE PEDIDO SELECCIONADO ---
        marco_gestion = tk.LabelFrame(panel_izquierdo, text="Gestión de Pedido Seleccionado", padx=10, pady=10)
        marco_gestion.pack(fill=tk.X)
        
        self.lbl_seleccionado = tk.Label(marco_gestion, text="Seleccionado: Ninguno", fg="#1976D2", font=("Arial", 10, "bold"))
        self.lbl_seleccionado.pack(pady=(5, 15))
        
        # Botones de flujo
        btn_preparar = tk.Button(marco_gestion, text="1. Preparar Pedido", command=lambda: self.accion_estado("En preparación"))
        btn_preparar.pack(fill=tk.X, pady=3)
        
        btn_listo = tk.Button(marco_gestion, text="2. Marcar como Listo", command=lambda: self.accion_estado("Listo"))
        btn_listo.pack(fill=tk.X, pady=3)
        
        btn_entregar = tk.Button(marco_gestion, text="3. Entregar Pedido", command=lambda: self.accion_estado("Entregado"))
        btn_entregar.pack(fill=tk.X, pady=3)
        
        btn_cancelar = tk.Button(marco_gestion, text="Cancelar Pedido", command=lambda: self.accion_estado("Cancelado"), fg="red")
        btn_cancelar.pack(fill=tk.X, pady=(15, 3))
        
        btn_prioridad = tk.Button(marco_gestion, text="★ Subir a Prioridad (Profesor)", command=self.accion_prioridad, bg="#FFC107", font=("Arial", 9, "bold"))
        btn_prioridad.pack(fill=tk.X, pady=10)

        # --- Panel Derecho (Visualización) ---
        panel_derecho = tk.Frame(self.root, padx=15, pady=15)
        panel_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(panel_derecho, text="Cola de Pedidos (Representación de la Lista Enlazada)", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        columnas = ("ID", "Cliente", "Rol", "Productos", "Estado")
        self.tree = ttk.Treeview(panel_derecho, columns=columnas, show="headings")
        
        for col in columnas:
            self.tree.heading(col, text=col)
            # Ajustar anchos
            if col == "ID": self.tree.column(col, width=70, anchor=tk.CENTER)
            elif col == "Estado": self.tree.column(col, width=110, anchor=tk.CENTER)
            else: self.tree.column(col, width=120)
            
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
    def accion_crear(self):
        cliente = self.ent_cliente.get().strip()
        rol = self.cmb_rol.get()
        productos = self.ent_productos.get().strip()
        
        if not cliente or not productos:
            messagebox.showwarning("Campos Incompletos", "Por favor ingrese el nombre del cliente y los productos.")
            return
            
        self.lista.agregar_pedido(cliente, rol, productos)
        self.ent_cliente.delete(0, tk.END)
        self.ent_productos.delete(0, tk.END)
        self.actualizar_tabla()
        
    def on_tree_select(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            self.selected_id = item['values'][0]
            self.lbl_seleccionado.config(text=f"Seleccionado: {self.selected_id}")
            
    def accion_estado(self, nuevo_estado):
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Seleccione un pedido en la tabla primero.")
            return
        try:
            self.lista.cambiar_estado(self.selected_id, nuevo_estado)
            self.actualizar_tabla()
        except ValueError as e:
            messagebox.showerror("Regla de Negocio Bloqueada", str(e))
            
    def accion_prioridad(self):
        if not self.selected_id:
            messagebox.showwarning("Aviso", "Seleccione un pedido en la tabla primero.")
            return
        try:
            self.lista.cambiar_prioridad(self.selected_id)
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Prioridad actualizada. El nodo fue reubicado respetando las reglas FIFO.")
        except ValueError as e:
            messagebox.showwarning("Advertencia", str(e))
            
    def actualizar_tabla(self):
        # Limpiar
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Rellenar leyendo la lista enlazada (recorrido secuencial)
        pedidos = self.lista.obtener_todos()
        for p in pedidos:
            self.tree.insert("", tk.END, values=(p['id'], p['cliente'], p['rol'], p['productos'], p['estado']))
            
        self.selected_id = None
        self.lbl_seleccionado.config(text="Seleccionado: Ninguno")

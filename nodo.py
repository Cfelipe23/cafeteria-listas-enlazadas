class Nodo:
    """
    Clase que representa un nodo de la Lista Enlazada Simple.
    Cada nodo almacena la información de un pedido de la cafetería y un puntero al siguiente.
    """
    def __init__(self, id_pedido, cliente, rol, productos):
        self.id_pedido = id_pedido
        self.cliente = cliente
        self.rol = rol  # "Estudiante" (Normal) o "Profesor" (Alta)
        self.productos = productos
        self.estado = "Pendiente"  # Estados: Pendiente, En preparación, Listo, Entregado, Cancelado
        self.siguiente = None  # Puntero al siguiente nodo

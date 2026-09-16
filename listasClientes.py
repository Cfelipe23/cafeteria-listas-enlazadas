class NodoTicket:
    def __init__(self, numero, cliente):
        self.numero = numero      # Número de ticket
        self.cliente = cliente    # Nombre del cliente
        self.prioridad = None         # Prioridad del ticket (opcional)
        self.siguiente = None     # Siguiente persona en la fila

class ListaEsperaTickets:
    def __init__(self):
        self.cabeza = None

    # Agrega un cliente al final de la fila
    def registrar_ticket(self, numero, cliente):
        # Programación Defensiva (Fail-Fast)
        if not cliente or not str(cliente).strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        nuevo_nodo = NodoTicket(numero, cliente)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            print(f"Ticket #{numero} creado para {cliente} (Primero en la fila).")
            return
        
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo_nodo
        print(f"Ticket #{numero} creado para {cliente}.")

    # Atiende al primer cliente de la lista y lo elimina de la fila
    def atender_siguiente(self):
        if self.cabeza is None:
            print("No hay clientes en la lista de espera.")
            return None
        
        atendido = self.cabeza
        print(f"Atendiendo ahora al Ticket #{atendido.numero}: {atendido.cliente}")
        
        # Mueve la cabeza al siguiente nodo para sacarlo de la fila
        self.cabeza = self.cabeza.siguiente
        return atendido

    # Muestra el estado actual de la fila
    def ver_fila(self):
        actual = self.cabeza
        if actual is None:
            print("\n--- La fila está vacía ---")
            return
        
        print("\n--- Fila de Espera Actual ---")
        posicion = 1
        while actual is not None:
            print(f"{posicion}. Ticket #{actual.numero} - {actual.cliente}")
            actual = actual.siguiente
            posicion += 1
        print("-----------------------------\n")

# Crear el sistema de tickets
sistema = ListaEsperaTickets()

# 1. Llegan los clientes y sacan ticket
sistema.registrar_ticket(101, "Carlos Pérez")
sistema.registrar_ticket(102, "Ana Gómez")
sistema.registrar_ticket(103, "Luis Martínez")

# Ver cómo está la fila
sistema.ver_fila()

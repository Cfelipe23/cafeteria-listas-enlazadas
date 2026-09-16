from nodo import Nodo

class ListaPedidos:
    """
    Lista Enlazada Simple personalizada para gestionar la cola de pedidos.
    Implementa las reglas de negocio, prioridad y lógica de punteros desde cero.
    """
    def __init__(self):
        self.cabeza = None
        self._contador_id = 1

    def agregar_pedido(self, cliente, rol, productos):
        """Crea y añade un nuevo pedido respetando las reglas de prioridad (FIFO por nivel)."""
        # --- Validaciones Defensivas (Fail-Fast) ---
        if not cliente or not productos:
            raise ValueError("Los campos de cliente y productos no pueden estar vacíos.")
        
        if rol not in ["Estudiante", "Profesor"]:
            raise ValueError("Rol inválido. Debe ser estrictamente 'Estudiante' o 'Profesor'.")

        id_pedido = f"PED-{self._contador_id:03d}"
        self._contador_id += 1
        nuevo_nodo = Nodo(id_pedido, cliente, rol, productos)

        # Si la lista está vacía, el nuevo nodo es la cabeza
        if not self.cabeza:
            self.cabeza = nuevo_nodo
            return id_pedido

        # Si es Estudiante, va al final absoluto de la cola de espera (FIFO Normal)
        if rol == "Estudiante":
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        else:
            # Si es Profesor, tiene prioridad. Va al final de los Profesores Pendientes,
            # pero estrictamente ANTES del primer Estudiante Pendiente.
            actual = self.cabeza
            anterior = None
            
            # Avanzamos mientras no encontremos al primer "Estudiante Pendiente"
            while actual and not (actual.estado == "Pendiente" and actual.rol == "Estudiante"):
                anterior = actual
                actual = actual.siguiente

            if anterior is None:
                # Si el primer nodo de la lista es un Estudiante Pendiente, tomamos la cabeza
                nuevo_nodo.siguiente = self.cabeza
                self.cabeza = nuevo_nodo
            else:
                # Insertar en medio de la lista (entre el último profe/en prep y el primer estudiante)
                nuevo_nodo.siguiente = actual
                anterior.siguiente = nuevo_nodo

        return id_pedido

    def buscar_pedido(self, id_pedido):
        """Busca un pedido por su ID recorriendo los nodos (Búsqueda Lineal)."""
        actual = self.cabeza
        while actual:
            if actual.id_pedido == id_pedido:
                return actual
            actual = actual.siguiente
        return None

    def cambiar_prioridad(self, id_pedido):
        """
        Sube la prioridad de un Estudiante a Profesor.
        Desvincula el nodo de su posición actual en la lista y lo reinserta
        cumpliendo las reglas de prioridad para no destruir el orden FIFO existente.
        """
        actual = self.cabeza
        anterior_a_cambiar = None

        # 1. Buscar el nodo a modificar y su anterior
        while actual and actual.id_pedido != id_pedido:
            anterior_a_cambiar = actual
            actual = actual.siguiente

        if not actual:
            raise ValueError(f"El pedido con ID {id_pedido} no existe.")

        # 2. Validaciones estrictas
        if actual.estado != "Pendiente":
            raise ValueError("Solo se puede cambiar la prioridad a pedidos en estado 'Pendiente'.")

        if actual.rol == "Profesor":
            raise ValueError("El pedido ya tiene prioridad alta (Profesor). No se realizarán cambios.")

        # 3. Desvincular el nodo de su posición actual
        if anterior_a_cambiar is None:
            # Si era la cabeza, simplemente actualizamos el rol. Sigue estando al frente.
            actual.rol = "Profesor"
            return
        else:
            # Reconectar el puntero del nodo anterior para "sacar" el nodo actual de la lista
            anterior_a_cambiar.siguiente = actual.siguiente
            actual.siguiente = None
            actual.rol = "Profesor" # Actualizamos su rol

            # 4. Reinsertar el nodo en la posición correcta (misma lógica que agregar un Profesor nuevo)
            temp = self.cabeza
            ant = None
            
            while temp and not (temp.estado == "Pendiente" and temp.rol == "Estudiante"):
                ant = temp
                temp = temp.siguiente

            if ant is None:
                actual.siguiente = self.cabeza
                self.cabeza = actual
            else:
                actual.siguiente = temp
                ant.siguiente = actual

    def cambiar_estado(self, id_pedido, nuevo_estado):
        """Actualiza el estado de un pedido aplicando las reglas de flujo de la rúbrica."""
        nodo = self.buscar_pedido(id_pedido)
        if not nodo:
            raise ValueError("Pedido no encontrado.")

        estado_actual = nodo.estado
        if nuevo_estado == estado_actual:
            return 
            
        if nuevo_estado == "Cancelado":
            if estado_actual != "Pendiente":
                raise ValueError("Solo se pueden cancelar pedidos que aún estén 'Pendientes'.")
            nodo.estado = "Cancelado"
            return

        if nuevo_estado == "En preparación":
            if estado_actual != "Pendiente":
                raise ValueError("Solo los pedidos 'Pendientes' pueden pasar a 'En preparación'.")

            # Regla: Solo un pedido en preparación a la vez
            # Regla: Respetar orden FIFO y de Prioridad (Debe ser el primer Pendiente en la lista enlazada)
            temp = self.cabeza
            primer_pendiente = None
            while temp:
                if temp.estado == "En preparación":
                    raise ValueError("Ya hay un pedido en preparación. Finalícelo primero.")
                if temp.estado == "Pendiente" and primer_pendiente is None:
                    primer_pendiente = temp
                temp = temp.siguiente

            if primer_pendiente and primer_pendiente.id_pedido != id_pedido:
                raise ValueError(f"Violación de prioridad. El siguiente pedido en la cola es el {primer_pendiente.id_pedido}.")

            nodo.estado = "En preparación"
            return

        if nuevo_estado == "Listo":
            if estado_actual != "En preparación":
                raise ValueError("El pedido debe estar 'En preparación' para marcarse como 'Listo'.")
            nodo.estado = "Listo"
            return

        if nuevo_estado == "Entregado":
            if estado_actual != "Listo":
                raise ValueError("El pedido debe estar 'Listo' para poder entregarse.")
            nodo.estado = "Entregado"
            return

        raise ValueError("Transición de estado no válida.")

    def obtener_todos(self):
        """
        Generador que cede (yield) la información de cada pedido (Compatible con el bucle del Treeview).
        Corrige la infracción CRÍTICA al eliminar el uso de la lista nativa '[]' y '.append()'.
        """
        actual = self.cabeza
        while actual:
            yield {
                "id": actual.id_pedido,
                "cliente": actual.cliente,
                "rol": actual.rol,
                "productos": actual.productos,
                "estado": actual.estado
            }
            actual = actual.siguiente

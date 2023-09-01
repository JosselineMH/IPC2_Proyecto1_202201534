from nodo_lista_simple import nodo_lista_simple

class lista_simple_enlazada:
    def __init__(self):
        self.inicio = None
        self.fin = None

    def agregar(self, dato):
        new_nodo = nodo_lista_simple(dato)
        if self.fin is None:
            self.inicio = new_nodo
            self.fin = new_nodo
        else:
            self.fin.siguiente = new_nodo
            self.fin = new_nodo
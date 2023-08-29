from nodo_patron import nodo_patron

class lista_patrones:
  def __init__(self):
    self.primero = None
    self.contador_patrones=0


  def insertar_patron(self,patron):
    if self.primero is None:
      self.primero = nodo_patron(patron=patron)
      self.contador_patrones+=1
      return
    actual= self.primero
    while actual.siguiente:
      actual = actual.siguiente
    actual.siguiente = nodo_patron(patron=patron)
    self.contador_patrones+=1

  def recorrer_imprimir_patron(self):
    print("===========================================================================================")
    actual = self.primero
    while actual != None:
      print(" Tiempo: ",actual.patron.tiempo)
      print("Cadena-Patron: ",actual.patron.cadena_patron)
      actual = actual.siguiente
    print("===========================================================================================")

  def eliminar(self,tiempo):
    actual = self.primero
    anterior = None
    while actual and actual.patron.tiempo != tiempo:
      anterior=actual
      actual = actual.siguiente
    if anterior is None:
      self.primero = actual.siguiente
      actual.siguiente = None
    elif actual:
      anterior.siguiente = actual.siguiente
      actual.siguiente = None

  
  def encontrar_coincidencias(self):
    resultado = ""  # Inicializa un string vacío para almacenar el resultado final  
    # Bucle principal que se ejecuta mientras haya nodos en la lista
    while self.primero:
      actual = self.primero  # Comienza desde el primer nodo en la lista
      temp_string = ""  # String temporal para almacenar niveles coincidentes
      temp_tiempos = ""  # Lista temporal para almacenar niveles      
      # Bucle interno para recorrer la lista de nodos y buscar coincidencias
      
      while actual:
        if actual.patron.cadena_patron == self.primero.patron.cadena_patron:
          temp_tiempos+=(str(actual.patron.tiempo))+","  # Agrega el nivel a la lista temporal
          # Si no hay nodo siguiente, elimina el primer nodo
        actual=actual.siguiente
      # Terminamos la iteración, quiere decir que ya tenemos la coincidencias:
      buffer=""
      #print(temp_niveles)
      for digito in temp_tiempos:
        if digito.isdigit():
          buffer+=digito
        #Quiere decir que viene una coma
        else:
          if buffer!="":
            self.eliminar(int(buffer))
            buffer=""
          else:
            buffer=""
      resultado+=temp_tiempos+"--"
    return resultado  # Devuelve el resultado final con la agrupación de niveles
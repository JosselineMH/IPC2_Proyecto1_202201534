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
    resultado = ""  #almacena el resultado final  
    #se ejecuta mientras haya nodos en la lista
    while self.primero:
      actual = self.primero 
      temp_tiempos = ""  # Lista temporal para almacenar tiempos      
      while actual:
        if actual.patron.cadena_patron == self.primero.patron.cadena_patron:
          temp_tiempos+=(str(actual.patron.tiempo))+"," 
        actual=actual.siguiente
      buffer=""
      for digito in temp_tiempos:
        if digito.isdigit():
          buffer+=digito
        else:
          if buffer!="":
            self.eliminar(int(buffer))
            buffer=""
          else:
            buffer=""
      resultado+=temp_tiempos+"--"
    return resultado  
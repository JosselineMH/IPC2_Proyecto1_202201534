from nodo_dato import nodo_dato
import sys
import os
from patron import patron

class lista_datos:
    def __init__(self):
        self.primero = None
        self.count_dato = 0


    def insertar_dato_1(self, dato):
        if self.primero is None:
            self.primero = nodo_dato(dato=dato)
            self.count_dato +=1
            return
        actual = self.primero
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente= nodo_dato(dato=dato)
        self.count_dato +=1

    def insertar_dato(self,dato):
        nuevo_dato=nodo_dato(dato=dato)
        self.count_dato+=1
        #Si Lista Vacía
        if self.primero is None:
            self.primero =nuevo_dato
            return
        if dato.tiempo < self.primero.dato.tiempo or(dato.tiempo==self.primero.dato.tiempo and dato.amplitud<=self.primero.dato.amplitud):
            nuevo_dato.siguiente=self.primero
            self.primero=nuevo_dato
            return
        actual=self.primero
        while actual.siguiente is not None and(dato.tiempo>actual.siguiente.dato.tiempo or (dato.tiempo == actual.siguiente.dato.tiempo and dato.amplitud > actual.siguiente.dato.amplitud)):
            actual=actual.siguiente
        nuevo_dato.siguiente=actual.siguiente
        actual.siguiente=nuevo_dato

    def imprimir_lista_datos(self):
        print("-------------------------------------------------------------------------")
        actual = self.primero
        while actual != None:
            print("Tiempo: ", actual.dato.tiempo, "Amplitud: ", actual.dato.amplitud, "Valor: ", actual.dato.valor)
            actual = actual.siguiente
        print("-------------------------------------------------------------------------")


    def generar_grafica_org(self,nombre,tiempo,amplitud):
        f = open('bb.dot','w')
        # configuraciones del grafo
        text ="""
            digraph G {fontname="Helvetica,Arial,sans-serif" "t="""+tiempo+"""","A="""+amplitud+""""->" """+nombre+ """"   bgcolor="purple:blue" style="filled"
            a0 [ shape=none label=<
            <TABLE border="0" cellspacing="10" cellpadding="10" style="rounded"  bgcolor="purple:violet" gradientangle="315">\n"""
        actual = self.primero
        sentinela_de_filas=actual.dato.tiempo #iniciaria en 1
        fila_iniciada=False
        while actual != None:
            # Si mi fila actual es diferente a la que viene
            if  sentinela_de_filas!=actual.dato.tiempo:
                #print(sentinela_de_filas,actual.celda.nivel,"hola")
                sentinela_de_filas=actual.dato.tiempo
                fila_iniciada=False
                # Cerramos la fila
                text+="""</TR>\n"""  
            if fila_iniciada==False:
                fila_iniciada=True
                #Abrimos la fila
                text+="""<TR>"""  
                text+="""<TD border="2"  bgcolor="purple:pink"  gradientangle="315">"""+str(actual.dato.valor)+"""</TD>\n"""
            else:
                text+="""<TD border="2"  bgcolor="purple:pink"  gradientangle="315">"""+str(actual.dato.valor)+"""</TD>\n"""
            actual = actual.siguiente
        text+=""" </TR></TABLE>>];
                }\n"""
        f.write(text)
        f.close()
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        os.system('dot -Tpng bb.dot -o GRÁFICA_MATRIZ_ORIGINAL.png')
        print("terminado")

        


    def devolver_patrones_por_tiempo(self, lista_patrones_reducida):
        actual = self.primero
        sentinela_de_filas = actual.dato.tiempo
        fila_iniciada = False
        recolector_patron = ""
        while actual != None:
            if sentinela_de_filas!=actual.dato.tiempo:
                fila_iniciada= False
                lista_patrones_reducida.insertar_patron(patron(sentinela_de_filas, recolector_patron))
                recolector_patron=""
                sentinela_de_filas = actual.dato.tiempo
            if fila_iniciada == False:
                fila_iniciada= True
                recolector_patron+= str(actual.dato.valor)+" "
            else:
                recolector_patron+=str(actual.dato.valor)+" "
            actual = actual.siguiente
        lista_patrones_reducida.insertar_patron(patron(sentinela_de_filas,recolector_patron))
        return lista_patrones_reducida


    def devolver_cadena_grupo (self, grupo):
        string_resultado = ""
        string_temp = ""
        buffer=""
        for digito in grupo:
            if digito.isdigit():
                buffer += digito
            else:
                string_temp=""
                actual = self.primero
                while actual != None:
                    if actual.dato.tiempo == int(buffer):
                        string_temp+= str(actual.dato.valor)+"/"
                    actual = actual.siguiente
                string_resultado+=string_temp+"#"
                buffer=""
        return string_resultado
 
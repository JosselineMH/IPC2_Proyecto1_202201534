from nodo_grupo import nodo_grupo
import sys
import os

class lista_grupos:
    def __init__(self):
        self.primero=None


    def insertar_grupo(self, grupo):
        if self.primero is None:
            self.primero = nodo_grupo(grupo=grupo)
            return
        actual = self.primero
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nodo_grupo(grupo=grupo)

    def recorrer_imprimir_grupo(self):
        print("-------------------------------------------------------------------------")
        actual= self.primero
        while actual != None:
            print("Señal:",actual.grupo.nombre_senal,"Amplitud:",actual.grupo.amplitud,"Grupo:", actual.grupo.el_grupo, 
                  "Cadena Grupo:", actual.grupo.cadena_grupo, "Cadena reducida:", actual.grupo.cadena_grupo_reducida)
            actual = actual.siguiente
        print("-------------------------------------------------------------------------")


    def grafica_lista_reducida(self, nombre):
        actual=self.primero
        nombre_coincide=False
        while actual != None:
            if actual.senal.nombre==nombre:
                nombre_coincide=True
                break
            else:
                actual=actual.siguiente
        if nombre_coincide:
            print("Gráfica de la Señal Original", nombre, "generada con éxito")
            actual.grupo.lista_grupos.generar_grafica_reducida(actual.grupo.nombre,
                                                    str(actual.grupo.el_grupo))
        else:
            print("La señal", nombre, "no existe")

    def generar_grafica_reducida(self,nombre,grupos):
        f = open('bb.dot','w')
        # configuraciones del grafo
        text ="""
            digraph G {fontname="Helvetica,Arial,sans-serif" "g="""+grupos+""""->" """+nombre+ """"   bgcolor="purple:blue" style="filled"
            a0 [ shape=none label=<
            <TABLE border="0" cellspacing="10" cellpadding="10" style="rounded"  bgcolor="purple:violet" gradientangle="315">\n"""
        actual = self.primero
        sentinela_de_filas=actual.grupo.el_grupo #iniciaria en 1
        fila_iniciada=False
        while actual != None:
            # Si mi fila actual es diferente a la que viene
            if  sentinela_de_filas!=actual.grupo.el_grupo :
                #print(sentinela_de_filas,actual.celda.nivel,"hola")
                sentinela_de_filas=actual.grupo.el_grupo 
                fila_iniciada=False
                # Cerramos la fila
                text+="""</TR>\n"""  
            if fila_iniciada==False:
                fila_iniciada=True
                #Abrimos la fila
                text+="""<TR>"""  
                text+="""<TD border="2"  bgcolor="purple:pink"  gradientangle="315">"""+str(actual.grupo.cadena_grupo_reducida)+"""</TD>\n"""
            else:
                text+="""<TD border="2"  bgcolor="purple:pink"  gradientangle="315">"""+str(actual.grupo.cadena_grupo_reducida)+"""</TD>\n"""
            actual = actual.siguiente
        text+=""" </TR></TABLE>>];
                }\n"""
        f.write(text)
        f.close()
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        os.system('dot -Tpng bb.dot -o GRÁFICA_MATRIZ_REDUCIDA.png')
        print("terminado")
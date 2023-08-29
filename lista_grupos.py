from nodo_grupo import nodo_grupo
import sys
import os

def separar_cadena(cadena, delimitador):
    numeros = []  # números resultantes
    num_actual = ""  
    for c in cadena:
        if c == delimitador:
            if num_actual:
                numeros.append(int(num_actual))
                num_actual = ""
        else:
            num_actual += c
    if num_actual:
        numeros.append(int(num_actual))
    return numeros


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




    def generar_grafica_reducida(self, nombre_senal):
        f = open('aa.dot','w')
        actual = self.primero
        text ="""
            
            digraph G {fontname="Helvetica,Arial,sans-serif" "A="""+actual.grupo.amplitud+""""->" """+nombre_senal+ """"   bgcolor="blue:cyan" style="rounded"
            a0 [ shape=none label=<
            <TABLE border="0" cellspacing="10" cellpadding="10" style="rounded"  bgcolor="blue:purple" gradientangle="315">\n"""
       
        while actual:
            if actual.grupo.nombre_senal == nombre_senal:
                text+="""<TR>""" 
                cadena_digitos=separar_cadena(actual.grupo.cadena_grupo_reducida,"-")
                text+="""<TD border="2" bgcolor="deepskyblue2:purple"  gradientangle="315">g="""+str(actual.grupo.el_grupo)+"""</TD>\n"""
                for i in cadena_digitos:
                    text+="""<TD border="2" bgcolor="deepskyblue2:purple"  gradientangle="315">"""+str(i)+"""</TD>\n"""
                text+="""</TR>\n"""
            actual = actual.siguiente
        text+="""</TABLE>>];
                }\n"""
        f.write(text)
        f.close()
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        os.system('dot -Tpng aa.dot -o grafica_matriz_reducida.png')

        print("Gráfica de la Señal Reducida", nombre_senal, "generada con éxito")

    
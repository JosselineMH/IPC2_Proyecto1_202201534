from nodo_senal import nodo_senal
from grupo import grupo
from lista_grupos import lista_grupos
import xml.etree.ElementTree as ET
from lista_simple_enlazada import lista_simple_enlazada


def separar_cadena_reducida(cadena, separador):
    numeros = lista_simple_enlazada() # Lista para almacenar los números resultantes
    num_actual = ""  # Cadena para construir el número actual
    for caracter in cadena:
        if caracter == separador:
            if num_actual:
                numeros.agregar(num_actual)
                num_actual = ""
        else:
            num_actual += caracter
    if num_actual:
        numeros.agregar(num_actual)
    return numeros


def procesar_cadena(cadena):
    subcadenas = separar_cadena_reducida(cadena,"#")
    nodo_actual_subcadena = subcadenas.inicio
    suma_total = None
    while nodo_actual_subcadena:
        valor = separar_cadena_reducida(nodo_actual_subcadena.dato, "/")
        valor_actual = valor.inicio
        if suma_total is None:
            suma_total = lista_simple_enlazada()
            while valor_actual:
                suma_total.agregar(valor_actual.dato)
                valor_actual = valor_actual.siguiente
        else:
            suma = suma_total.inicio
            while valor_actual:
                if suma:
                    suma.dato = str(int(suma.dato) + int(valor_actual.dato))
                    suma = suma.siguiente
                    valor_actual = valor_actual.siguiente
        nodo_actual_subcadena = nodo_actual_subcadena.siguiente
    resultado = ""
    nodo_res= suma_total.inicio
    while nodo_res:
        resultado += nodo_res.dato
        if nodo_res.siguiente:
            resultado += "-"
        nodo_res = nodo_res.siguiente
    return resultado


class lista_senales:
    def __init__(self):
        self.primero = None
        self.count_senal = 0

    

    def insertar_senal(self, senal):
        if self.primero is None:
            self.primero = nodo_senal(senal=senal)
            self.count_senal +=1
            return
        actual = self.primero
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente= nodo_senal(senal=senal)
        self.count_senal +=1

    def imprimir_lista_senales(self):
        print("Total de señales almacenadas:", self.count_senal)
        print("")
        print("-------------------------------------------------------------------------")
        actual = self.primero
        while actual != None:
            print("Nombre: ",actual.senal.nombre,"Tiempo: ", actual.senal.tiempo, "Amplitud: ", actual.senal.amplitud)
            
            actual = actual.siguiente
        print("-------------------------------------------------------------------------")

    def grafica_lista_original(self, nombre):
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
            actual.senal.lista_datos.generar_grafica_org(actual.senal.nombre,
                                                    str(actual.senal.tiempo),
                                                    str(actual.senal.amplitud))
            actual.senal.lista_grupos.generar_grafica_reducida(actual.senal.nombre)
        else:
            print("La señal", nombre, "no existe")

    

    

    def calcular_patrones(self):
        actual = self.primero
        while actual != None:
            nombre_senal = actual.senal.nombre
            amplitud = actual.senal.amplitud
            actual.senal.lista_patron_reducida = actual.senal.lista_patron_binario.devolver_patrones_por_tiempo(actual.senal.lista_patron_reducida)
            #actual.senal.lista_patron_reducida.recorrer_imprimir_patron()

            lista_patrones_temporal=actual.senal.lista_patron_reducida
            grupos_sin_analizar=lista_patrones_temporal.encontrar_coincidencias()

            #print(grupos_sin_analizar)
            buffer = ""
            for digito in grupos_sin_analizar:

                if digito.isdigit() or digito==",":
                    buffer+=digito
                elif digito =="-" and buffer!="":
                    cadena_grupo=actual.senal.lista_datos.devolver_cadena_grupo(buffer)
                    #print("Esto guarda el buffer:", buffer)
                    cadena_grupo_reducida = procesar_cadena(cadena_grupo)
                    actual.senal.lista_grupos.insertar_grupo(grupo=grupo(nombre_senal,amplitud,buffer,cadena_grupo,cadena_grupo_reducida))
                    buffer=""
                else:
                    buffer=""
            
            actual = actual.siguiente

    def generar_xml_salida(self, nombre_ruta):
        actual=self.primero
        #senalesReducidas
        senales_reducidas=ET.Element("senalesReducidas")
        
        while actual!=None:
            #senal
            senal=ET.SubElement(senales_reducidas,"senal")
            senal.set("nombre",actual.senal.nombre)
            senal.set("A",actual.senal.amplitud)

            lista_grupo_temp=actual.senal.lista_grupos.primero
            contador_grupo=1
            while lista_grupo_temp!=None:
                #grupo
                grupo=ET.SubElement(senal,"grupo")
                grupo.set("g",str(contador_grupo))
                contador_grupo+=1
                #tiempos
                tiempos=ET.SubElement(grupo,"tiempos")
                tiempos.text=str(lista_grupo_temp.grupo.el_grupo)
                #datosGrupo
                datos_grupo=ET.SubElement(grupo,"datosGrupo")
                #dato
                cadena_digitos=separar_cadena_reducida(lista_grupo_temp.grupo.cadena_grupo_reducida,"-")
                contador_amplitud=1
                num_nodo_actual=cadena_digitos.inicio
                while num_nodo_actual:
                    dato=ET.SubElement(datos_grupo,"dato")
                    dato.set("A",str(contador_amplitud))
                    dato.text=num_nodo_actual.dato
                    contador_amplitud+=1
                    num_nodo_actual=num_nodo_actual.siguiente   
                lista_grupo_temp=lista_grupo_temp.siguiente
                contador_amplitud=1
            actual=actual.siguiente
            contador_grupo=1

        my_data=ET.tostring(senales_reducidas)
        my_data=str(my_data)
        self.xml_arreglado(senales_reducidas)

        arbol_xml=ET.ElementTree(senales_reducidas)
        arbol_xml.write(nombre_ruta+".xml",encoding="UTF-8",xml_declaration=True)

    def xml_arreglado(self, element, indent='  '):
        # Inicializar una cola con el elemento raíz y nivel de anidación 0
        queue = [(0, element)]  # (level, element)
        while queue:
            # Extraer nivel y elemento actual de la cola
            level, element = queue.pop(0)
            children = [(level+1, child) for child in list(element)]
            # Agregar saltos de línea e indentación al inicio del elemento actual
            if children:
                element.text = '\n' + indent * (level + 1)
                # Agregar saltos de línea e indentación al final del elemento actual
            if queue:
                element.tail = '\n' + indent * queue[0][0]
            else:
                # Si este es el último elemento del nivel actual, reducir la indentación
                element.tail = '\n' + indent * (level - 1)
            queue[0:0] = children

    
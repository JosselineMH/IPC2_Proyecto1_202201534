from nodo_senal import nodo_senal
from grupo import grupo
from lista_grupos import lista_grupos
import xml.etree.ElementTree as ET


def separar_cadena(cadena, delimitador):
    numeros = []  # Lista para almacenar los números resultantes
    num_actual = ""  # Cadena para construir el número actual
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

def procesar_cadena1(cadena_grupo):
    string_suma=""
    subcadenas = []  # Inicializar subcadenas como una lista vacía
    buffer = []  # Inicializar buffer como una lista vacía
    suma_total = None

    for digito in cadena_grupo:
        if digito != "#":
            subcadenas.append(digito)  # Agregar el dígito a la lista subcadenas
        else:
            for digito2 in subcadenas:
                if digito2.isdigit():
                    buffer.append(digito2)  # Agregar el dígito a la lista buffer
            if suma_total is None:
                suma_total = buffer.copy()  # Inicializar suma_total con una copia de buffer
            else:
                for i in range(len(buffer)):
                    if buffer[i]:
                        suma_total[i] = str(int(suma_total[i]) + int(buffer[i]))  # Sumar los valores correspondientes
            subcadenas = []  # Reiniciar subcadenas para la siguiente iteración
            buffer = []  # Reiniciar buffer para la siguiente iteración
            string_suma+= str(suma_total)+"-"
    #print("Realizando suma de tuplas...")
    return "-".join(suma_total)

def procesar_cadena(cadena):
    subcadenas = separar_cadena_reducida(cadena,"#")
    suma_total = None

    for subcadena in subcadenas:
        valores = separar_cadena_reducida(subcadena,"/")
        
        if suma_total is None:
            suma_total = valores
        else:
            for i in range(len(valores)):
                if valores[i]:
                    suma_total[i] = str(int(suma_total[i]) + int(valores[i]))

    return "-".join(suma_total)


def separar_cadena_reducida(cadena, separador):
    resultado = []
    inicio = 0
    for i, caracter in enumerate(cadena):
        if caracter == separador:
            resultado.append(cadena[inicio:i])
            inicio = i + 1
    resultado.append(cadena[inicio:])
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
            actual.senal.lista_patron_reducida.recorrer_imprimir_patron()

            lista_patrones_temporal=actual.senal.lista_patron_reducida
            grupos_sin_analizar=lista_patrones_temporal.encontrar_coincidencias()

            print(grupos_sin_analizar)
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
            actual.senal.lista_grupos.recorrer_imprimir_grupo()
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
            #ListaGrupos------
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
                cadena_digitos=separar_cadena(lista_grupo_temp.grupo.cadena_grupo_reducida,"-")
                contador_amplitud=1
                for i in cadena_digitos:
                    dato=ET.SubElement(datos_grupo,"dato")
                    dato.set("A",str(contador_amplitud))
                    contador_amplitud+=1
                    dato.text=str(i)
                lista_grupo_temp=lista_grupo_temp.siguiente
                contador_amplitud=1
            actual=actual.siguiente
            contador_grupo=1

        #Generar xml
        my_data=ET.tostring(senales_reducidas)
        my_data=str(my_data)
        self.xml_arreglado(senales_reducidas)

        arbol_xml=ET.ElementTree(senales_reducidas)
        arbol_xml.write(nombre_ruta+".xml",encoding="UTF-8",xml_declaration=True)

    def xml_arreglado(self, element, indent='  '):
        # Inicializar una cola con el elemento raíz y nivel de anidación 0
        queue = [(0, element)]  # (level, element)
        # Bucle principal: continúa mientras haya elementos en la cola
        while queue:
            # Extraer nivel y elemento actual de la cola
            level, element = queue.pop(0)
            # Crear tuplas para cada hijo con nivel incrementado
            children = [(level + 1, child) for child in list(element)]
            # Agregar saltos de línea e indentación al inicio del elemento actual
            if children:
                element.text = '\n' + indent * (level + 1)
                # Agregar saltos de línea e indentación al final del elemento actual
            if queue:
                element.tail = '\n' + indent * queue[0][0]
            else:
                # Si este es el último elemento del nivel actual, reducir la indentación
                element.tail = '\n' + indent * (level - 1)
            # Insertar las tuplas de hijos al principio de la cola
            queue[0:0] = children

    
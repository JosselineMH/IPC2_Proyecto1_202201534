from nodo_senal import nodo_senal
from grupo import grupo
from lista_grupos import lista_grupos

def procesar_cadena(cadena_grupo):
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
            actual.senal.lista_datos.imprimir_lista_datos()
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
            #actual.senal.lista_grupos.recorrer_imprimir_grupo()
            actual = actual.siguiente

    
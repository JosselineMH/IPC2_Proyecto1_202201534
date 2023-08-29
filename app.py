import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
from lista_senales import lista_senales
from lista_datos import lista_datos
from lista_patrones import lista_patrones
from lista_grupos import lista_grupos
from dato import dato
from senal import senal
import logging

logging.basicConfig(level=logging.DEBUG)
source_archivo = ""
lista_senales_temp = lista_senales()
lista_grupos_temp = lista_grupos()

def update_source(new_source):
    global source_archivo
    source_archivo = new_source

def cargar_archivo():
    print("------------------------------------------------------------")
    print("                       CARGAR ARCHIVO                       ")
    print("------------------------------------------------------------")
    print("Abriendo explorador de archivos...")
    print("Seleccione el archivo XML")

    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    
    ruta_seleccionada = filedialog.askopenfilename()
    if ruta_seleccionada:
        update_source(ruta_seleccionada)
    
    print("¡Archivo cargado con éxito!, el archivo seleccionado es:", source_archivo)
    validacion_opcion()



def procesar_archivo():
    print("------------------------------------------------------------")
    print("                   PROCESAR EL ARCHIVO                      ")
    print("------------------------------------------------------------")

    if source_archivo == "":
        print("No se ha cargado ningún archivo.")
        validacion_opcion()
        return

    try:
        archivo_XML = open(source_archivo, "r")
        archivo_XML.close()

        tree = ET.parse(source_archivo)
        raiz = tree.getroot()

       
    

        for senal_temp in raiz.findall('senal'):
            nombre_senal = senal_temp.get('nombre')
            tiempo_senal = senal_temp.get('t')
            amplitud_senal = senal_temp.get('A')

            lista_datos_temp = lista_datos()
            lista_patronesbin_temp = lista_datos()
            lista_patrones_matrizRed_temp = lista_patrones()
            #lista_grupos_temp = lista_grupos()
            

            for dato_senal in senal_temp.findall('dato'):
                tiempo_dato = dato_senal.get('t')
                amplitud_dato = dato_senal.get('A')
                valor_dato = dato_senal.text
                nuevo = dato(int(tiempo_dato), int(amplitud_dato), int(valor_dato))
                lista_datos_temp.insertar_dato(nuevo)

                if valor_dato != "0":
                    nuevo_SENAL = dato(int(tiempo_dato), int(amplitud_dato), 1)
                    lista_patronesbin_temp.insertar_dato(nuevo_SENAL)
                else:
                    nuevo_SENAL = dato(int(tiempo_dato), int(amplitud_dato), 0)
                    lista_patronesbin_temp.insertar_dato(nuevo_SENAL)
            
            
            lista_senales_temp.insertar_senal(senal(nombre_senal,tiempo_senal,amplitud_senal,
                                                    lista_datos_temp,lista_patronesbin_temp,
                                                    lista_patrones_matrizRed_temp, lista_grupos_temp))
            #lista_senales_temp.imprimir_lista_senales()
            #lista_patronesbin_temp.imprimir_lista_datos()
        lista_senales_temp.calcular_patrones()
            
        print("> Calculando la matriz binaria...")
        print("> Realizando suma de tuplas...")
        print("... ")
        print("... ")
        print("Archivo procesado exitosamente")
    except Exception as e:
        print("Ocurrió un error al procesar el archivo:", e)

    validacion_opcion()

def generar_Graficas():
    print("------------------------------------------------------------")
    print("                     GENERAR GRÁFICAS                       ")
    print("------------------------------------------------------------")
    nombre = input("Ingrese el nombre de la señal que desea graficar: ")
    lista_senales_temp.grafica_lista_original(nombre)
    lista_grupos_temp.generar_grafica_reducida(nombre)

def validacion_opcion():
    print("¿Desea regresar al menú?")
    print("1. Sí")
    print("2. No, deseo salir")
    nuevaopcion = input()
    if nuevaopcion == "1":
        menu()
    elif  nuevaopcion == "2":
        salir()
    else:
        print("La opción seleccionada no es válida, regresando al menú...")
        menu()

def datos():
    print("------------------------------------------------------------")
    print("                     DATOS DEL ESTUDIANTE                   ")
    print("------------------------------------------------------------")
    print("> Josseline Griselda Montecinos Hernández")
    print("> 202201534")
    print("> Introducción a la Programación y Computación 2 Sección 'D'")
    print("> Ingeniería en Ciencias y Sistemas")
    print("> 4to Semestre")
    validacion_opcion

def salir():
    print("Gracias por utilizar el programa")

def menu():
    print("============================================================")
    print("    Centro de Investigación de la Facultad de Ingeniería    ")
    print("             COMPRESIÓN DE LAS SEÑALES DE AUDIO             ")
    print("============================================================")
    print("1. Cargar Archivo")
    print("2. Procesar Archivo")
    print("3. Escribir archivo salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Inicializar Sistema")
    print("7. Salir")
    opcion = int(input("Ingrese una opción: "))
    print("============================================================")
    if opcion == 1:
        cargar_archivo()
    elif  opcion == 2:
        procesar_archivo()
    elif opcion == 3:
        print("3")
    elif opcion == 4:
        datos()
    elif opcion == 5:
        generar_Graficas()
    elif opcion == 6:
        print("6")
    elif opcion == 7:
        salir()
    else:
        print("Opción no válida")
        menu()
menu()

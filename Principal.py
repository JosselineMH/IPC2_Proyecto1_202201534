def Cargar_Archivo():
    print("------------------------------------------------------------")
    print("                       CARGAR ARCHIVO                       ")
    print("------------------------------------------------------------")
    while True:
        print("Ingrese la ruta del archivo .xml que desea cargar:")
        archivo_mov = input()

        try:
            print("Holamundo")
        except FileNotFoundError:
            print("El archivo no existe. Por favor, ingrese una ruta válida.")


def datos():
    print("------------------------------------------------------------")
    print("                     DATOS DEL ESTUDIANTE                   ")
    print("------------------------------------------------------------")
    print("> Josseline Griselda Montecinos Hernández")
    print("> 202201534")
    print("> Introducción a la Programación y Computación 2 Sección 'D'")
    print("> Ingeniería en Ciencias y Sistemas")
    print("> 4to Semestre")
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
        Cargar_Archivo()
    elif  opcion == 2:
        print("2")
    elif opcion == 3:
        print("3")
    elif opcion == 4:
        datos()
    elif opcion == 5:
        print("5")
    elif opcion == 6:
        print("6")
    elif opcion == 7:
        salir()
    else:
        print("Opción no válida")
        menu()
menu()

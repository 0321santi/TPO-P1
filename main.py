from colorama import init, Fore, Back, Style
init(autoreset=True)
import json
import os
from funcion import (
    normalizar, ingresar, eliminar, modificar, gestionar_categoria_modo,
    buscar, escribir_log, verificar_umbral_minimo, configurar_umbral_minimo,
    existencias_sin_stock, versionGS, formatearDB, 
    cargar_memory, configurar_umbral_maximo, 
    verificar_sobre_almacenamiento, limpiarPantalla, cargar_categorias)


def menu_principal():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║     SISTEMA DE INVENTARIO    ║
╠══════════════════════════════╣
║ 0. Ingreso / Egreso          ║""")
    print(f"║ " + Fore.BLUE + "1. SKU" + Style.RESET_ALL + "                       ║")
    print(f"║ " + Fore.RED + "2. Categorías" + Style.RESET_ALL + "                ║")
    print(f"║ " + Fore.GREEN + "3. Buscar" + Style.RESET_ALL + "                    ║")
    print(f"║ " + Fore.MAGENTA + "4. Umbrales" + Style.RESET_ALL + "                  ║")
    print(f"""║ 5. Otras opciones            ║
║ 8. Salir                     ║
╚══════════════════════════════╝""")


def menu_sku():
    limpiarPantalla()
    print(Fore.BLUE + f"""╔══════════════════════════════╗
║        GESTIÓN DE SKU        ║
╠══════════════════════════════╣
║ 1. Agregar SKU               ║
║ 2. Eliminar SKU              ║
║ 3. Modificar SKU             ║""")
    print(Fore.BLUE + "║ " + Style.RESET_ALL + "4. Volver al menú principal  " + Fore.BLUE + "║")
    print(Fore.BLUE + "║ " + Style.RESET_ALL + "5. Salir                     " + Fore.BLUE + "║")
    print(Fore.BLUE + f"""╚══════════════════════════════╝""" + Style.RESET_ALL)


def menu_categorias():
    limpiarPantalla()
    print(Fore.RED + f"""╔══════════════════════════════╗
║     GESTIÓN DE CATEGORÍAS    ║
╠══════════════════════════════╣
║ 1. Listar categorias         ║
║ 2. Eliminar categoría        ║""")
    print(Fore.RED + "║ " + Style.RESET_ALL + "3. Volver al menú principal  " + Fore.RED + "║")
    print(Fore.RED + "║ " + Style.RESET_ALL + "4. Salir                     " + Fore.RED + "║")
    print(Fore.RED + f"""╚══════════════════════════════╝""" + Style.RESET_ALL)


def menu_buscar():
    limpiarPantalla()
    print(Fore.GREEN + f"""╔══════════════════════════════╗
║           BUSQUEDA           ║
╠══════════════════════════════╣
║ 1. SKU                       ║
║ 2. Producto                  ║
║ 3. Cantidad                  ║
║ 4. Precio                    ║
║ 5. Categoria                 ║""")
    print(Fore.GREEN + "║ " + Style.RESET_ALL + "6. Volver al menú principal  " + Fore.GREEN + "║")
    print(Fore.GREEN + "║ " + Style.RESET_ALL + "7. Salir                     " + Fore.GREEN + "║")
    print(Fore.GREEN + f"""╚══════════════════════════════╝""" + Style.RESET_ALL)


def menu_umbral():
    limpiarPantalla()
    print(Fore.MAGENTA + f"""╔══════════════════════════════╗
║      GESTIÓN DE UMBRALES     ║
╠══════════════════════════════╣
║ 1. Ver alertas de inventario ║
║ 2. Configurar umbral mínimo  ║
║ 3. Configurar umbral máximo  ║
║ 4. Ver sobre almacenamiento  ║
║ 5. Ver productos sin stock   ║""")
    print(Fore.MAGENTA + "║ " + Style.RESET_ALL + "6. Volver al menú principal  " + Fore.MAGENTA + "║")
    print(Fore.MAGENTA + "║ " + Style.RESET_ALL + "7. Salir                     " + Fore.MAGENTA + "║")
    print(Fore.MAGENTA + f"""╚══════════════════════════════╝""" + Style.RESET_ALL)


def menu_otros():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║       OTRAS OPCIONES         ║
╠══════════════════════════════╣
║ 1. Versión genzaloSTORAGE    ║
║ 2. Formatear base de datos   ║
║ 3. Volver al menú principal  ║
║ 4. Salir                     ║
╚══════════════════════════════╝""")


def exit_program():
    print("¡Gracias por usar genzaloSTORAGE!")
    raise SystemExit


try:
    escribir_log("Inicio del programa.", nivel="INFO")
    while True:
        limpiarPantalla()
        menu_principal()
        cargar_memory()
        cargar_categorias()
        seleccion = input("Seleccione una opción: ")
        continuar = 0

        match normalizar(seleccion):
            case "0" | "cero" | "ingreso" | "egreso":
                while True:
                    entrada = input("Ingrese SKU o nombre del producto: ")
                    try:
                        sku = int(entrada)
                        encontrado = False
                        arch = open('memoria.txt', 'rt', encoding='UTF8')
                        for lineas in arch:
                            linea = json.loads(lineas)
                            if linea.get("SKU") == sku:
                                encontrado = True
                                producto = linea
                                break
                        arch.close()
                    except ValueError:
                        encontrado = False
                        arch = open('memoria.txt', 'rt', encoding='UTF8')
                        for lineas in arch:
                            linea = json.loads(lineas)
                            nombre_producto = linea.get("nombre_producto")
                            if nombre_producto:
                                if normalizar(nombre_producto) == normalizar(entrada):
                                    encontrado = True
                                    producto = linea
                                    break
                        arch.close()
                    
                    if not encontrado:
                        print("Producto no encontrado")
                        continue
                    
                    print(f"Producto: {producto['nombre_producto']}")
                    print(f"Existencias actuales: {producto['existencias']}")
                    
                    try:
                        cantidad = int(input("Ingrese cantidad a modificar (0 para cancelar): "))
                    except ValueError:
                        print("Error: no es int")
                        continue
                    
                    if cantidad == 0:
                        continue
                    
                    if cantidad > 0:
                        producto["existencias"] += cantidad
                        print(f"Se añadieron {cantidad} unidades")
                    else:
                        if producto["existencias"] + cantidad < 0:
                            print("No hay suficiente stock")
                            continue
                        producto["existencias"] += cantidad
                        print(f"Se retiraron {-cantidad} unidades")
                    
                    arch = open('memoria.txt', 'rt', encoding='UTF8')
                    temp = open('temp.txt', 'wt', encoding='UTF8')
                    
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if linea.get("SKU") == producto.get("SKU"):
                            linea["existencias"] = producto["existencias"]
                        temp.write(json.dumps(linea) + '\n')
                    
                    arch.close()
                    temp.close()
                    os.remove('memoria.txt')
                    os.rename('temp.txt', 'memoria.txt')
                    continuar = int(input("Ingrese cualquier numero o -1 para salir: "))
                    if continuar == -1:
                        break
                

            case "1" | "uno" | "sku":
                while True:
                    menu_sku()
                    opcion_sku = input("Seleccione una opción: ")
                    continuar = 0
                    match normalizar(opcion_sku):
                        case "1" | "uno" | "agregar" | "agregar sku":
                            while continuar != "-1":
                                ingresar()
                                continuar = input("Ingrese cualquier valor para seguir o ingrese -1 para salir: ")

                        case "2" | "dos" | "eliminar" | "eliminar sku":
                            eliminar()

                        case "3" | "tres" | "modificar" | "modificar sku":
                            modificar()
                            input("Presione Intro para continuar.")

                        case "4" | "cuatro" | "volver" | "menu principal":
                            break

                        case "5" | "cinco" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "2" | "dos" | "categorias" | "categorías":
                while True:
                    menu_categorias()
                    opcion_cat = input("Seleccione una opción: ")

                    match normalizar(opcion_cat):
                        case "1" | "uno" | "ver" | "ver categorías":
                            gestionar_categoria_modo("ver")
                            input("Presione Intro para continuar.")

                        case "2" | "dos" | "eliminar" | "eliminar categoría":
                            gestionar_categoria_modo("eliminar")
                            input("Presione Intro para continuar.")
                        
                        case "3"| "tres" | "volver":
                            break

                        case "4" | "cuatro" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "3" | "tres" | "buscar":
                while True:
                    limpiarPantalla()
                    menu_buscar()
                    buscar()
                    seguir = input("\nPresione 1 para volver al menú principal o Enter para seguir buscando: ")
                    if seguir == "1":
                        break

            case "4" | "cuatro" | "umbral":
                while True:
                    menu_umbral()
                    opcion_umbral = input("Seleccione una opción: ")

                    match normalizar(opcion_umbral):
                        case "1" | "uno" | "ver alertas":
                            verificar_umbral_minimo()
                            input("Presione Intro para continuar.")

                        case "2" | "dos" | "configurar minimo":
                            configurar_umbral_minimo()
                            input("Presione Intro para continuar.")

                        case "3" | "tres" | "configurar maximo":
                            configurar_umbral_maximo()
                            input("Presione Intro para continuar.")

                        case "4" | "cuatro" | "sobre almacenamiento":
                            verificar_sobre_almacenamiento()
                            input("Presione Intro para continuar.")

                        case "5" | "cinco" | "sin stock" | "no stock":
                            existencias_sin_stock()
                            input("Presione Intro para continuar.")

                        case "6" | "seis" | "volver" | "menu principal":
                            break

                        case "7" | "siete" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "5" | "cinco" | "otras opciones" | "otros":
                while True:
                    menu_otros()
                    opcion_otros = input("Seleccione una opción: ")

                    match normalizar(opcion_otros):
                        case "1" | "uno" | "version":
                            versionGS()
                            input("Presione Intro para continuar.")

                        case "2" | "dos" | "formatear":
                            formatearDB()
                            input("Presione Intro para continuar.")

                        case "3" | "tres" | "volver":
                            break

                        case "4" | "cuatro" | "salir":
                            exit_program()

            case "8" | "ocho" | "salir":
                exit_program()

            case _:
                print("¡Error! Opción no válida.")
                input("Presione Intro para continuar.")

except Exception as e:
    print("¡Error! Ha ocurrido un problema:", e)
    escribir_log(f"Error inesperado: {e}", nivel="ERROR")
    input("Presione Intro para continuar.")

finally:
    escribir_log("Fin del programa.", nivel="INFO")
    print("Programa finalizado.")

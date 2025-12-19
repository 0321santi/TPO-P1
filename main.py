
from funcion import (
    normalizar, ingresar, eliminar, modificar, gestionar_categoria_modo,
    buscar, escribir_log, verificar_umbral_minimo, configurar_umbral_minimo,
    existencias_sin_stock, productos_por_categoria, versionGS, formatearDB, 
    cargar_memory, ingresar_paquete, configurar_umbral_maximo, 
    verificar_vencimientos_proximos, configurar_alerta_vencimiento, verificar_vencidos, 
    ver_productos_no_perecederos, verificar_alertas_vencimiento, ver_todas_alertas_vencimiento, 
    ver_todos_lotes, buscar_por_lote, ver_proximo_vencer_lotes, verificar_sobre_almacenamiento, ver_sin_vencimiento_registrado, 
    gestionar_proveedores, limpiarPantalla, cargar_categorias)


def menu_principal():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║     SISTEMA DE INVENTARIO    ║
╠══════════════════════════════╣
║ 0. Ingreso / Egreso          ║
║ 1. SKU                       ║
║ 2. Categorías                ║
║ 3. Buscar                    ║
║ 4. Umbrales                  ║
║ 5. Lotes                     ║
║ 6. Vencimientos              ║
║ 7. Otras opciones            ║
║ 8. Salir                     ║
╚══════════════════════════════╝""")


def menu_sku():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║        GESTIÓN DE SKU        ║
╠══════════════════════════════╣
║ 1. Agregar SKU               ║
║ 2. Agregar SKU por paquete   ║
║ 3. Eliminar SKU              ║
║ 4. Modificar SKU             ║
║ 5. Volver al menú principal  ║
║ 6. Salir                     ║
╚══════════════════════════════╝""")


def menu_categorias():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║     GESTIÓN DE CATEGORÍAS    ║
╠══════════════════════════════╣
║ 1. Agregar categoría         ║
║ 2. Eliminar categoría        ║
║ 3. Modificar categoría       ║
║ 4. Ver todas las categorías  ║
║ 5. Ver prod. por categoría   ║
║ 6. Volver al menú principal  ║
║ 7. Salir                     ║
╚══════════════════════════════╝""")


def menu_buscar():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║           BUSQUEDA           ║
╠══════════════════════════════╣
║ 1. SKU                       ║
║ 2. Producto                  ║
║ 3. Cantidad                  ║
║ 4. Precio                    ║
║ 5. Categoria                 ║
║ 6. Volver al menú principal  ║
║ 7. Salir                     ║
╚══════════════════════════════╝""")


def menu_umbral():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║      GESTIÓN DE UMBRALES     ║
╠══════════════════════════════╣
║ 1. Ver alertas de inventario ║
║ 2. Configurar umbral mínimo  ║
║ 3. Configurar umbral máximo  ║
║ 4. Ver sobre almacenamiento  ║
║ 5. Ver productos sin stock   ║
║ 6. Volver al menú principal  ║
║ 7. Salir                     ║
╚══════════════════════════════╝""")


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

def menu_vencimientos():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║        VENCIMIENTOS          ║
╠══════════════════════════════╣
║ 1. Ver productos próximos    ║
║ 2. Configurar alertas        ║
║ 3. Ver productos vencidos    ║
║ 4. Ver no perecederos        ║
║ 5. Ver prod. s/ venc. reg.   ║
║ 6. Volver al menú principal  ║
║ 7. Salir                     ║
╚══════════════════════════════╝""")


def menu_estadisticas():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║         ESTADÍSTICAS         ║
╠══════════════════════════════╣
║ 1. Resumen general           ║
║ 2. Productos por categoría   ║
║ 3. Distribución de precios   ║
║ 4. Volver al menú anterior   ║
║ 5. Salir del programa        ║
╚══════════════════════════════╝""")


def menu_lotes():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║        GESTIÓN DE LOTES      ║
╠══════════════════════════════╣
║ 1. Ver todos los lotes       ║
║ 2. Buscar por lote           ║
║ 3. Configurar método salida  ║
║ 4. Ver próximo a vencer      ║
║ 5. Volver al menú principal  ║
║ 6. Salir                     ║
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
                print("Ingrese el SKU o nombre del producto para registrar ingreso/egreso.")
                

            case "1" | "uno" | "sku":
                while True:
                    menu_sku()
                    opcion_sku = input("Seleccione una opción: ")
                    continuar = 0
                    match normalizar(opcion_sku):
                        case "1" | "uno" | "agregar" | "agregar sku":
                            while continuar != "-1":
                                ingresar()
                                continuar = input(
                                    "Ingrese cualquier valor para seguir o ingrese -1 para salir: ")

                        case "2" | "dos" | "agregar paquete" | "paquete":
                            while continuar != -1:
                                ingresar_paquete()
                                continuar = int(
                                    input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))

                        case "3" | "tres" | "eliminar" | "eliminar sku":
                            eliminar()

                        case "4" | "cuatro" | "modificar" | "modificar sku":
                            modificar()
                            input("Presione Intro para continuar.")

                        case "5" | "cinco" | "volver" | "menu principal":
                            break

                        case "6" | "seis" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "2" | "dos" | "categorias" | "categorías":
                while True:
                    menu_categorias()
                    opcion_cat = input("Seleccione una opción: ")

                    match normalizar(opcion_cat):
                        case "1" | "uno" | "agregar" | "agregar categoría":
                            gestionar_categoria_modo("agregar")
                            input("Presione Intro para continuar.")

                        case "2" | "dos" | "eliminar" | "eliminar categoría":
                            gestionar_categoria_modo("eliminar")
                            input("Presione Intro para continuar.")

                        case "3" | "tres" | "modificar" | "modificar categoría":
                            gestionar_categoria_modo("modificar")
                            input("Presione Intro para continuar.")

                        case "4" | "cuatro" | "ver" | "ver categorías":
                            gestionar_categoria_modo("ver")
                            input("Presione Intro para continuar.")

                        case "5" | "cinco" | "volver" | "menu principal":
                            productos_por_categoria("ver")
                            input("Presione Intro para continuar.")

                        case "6" | "seis" | "volver" | "menu principal":
                            break

                        case "7" | "siete" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "3" | "tres" | "buscar":
                while True:
                    limpiarPantalla()
                    menu_buscar()
                    buscar()
                    seguir = input(
                        "\nPresione 1 para volver al menú principal o Enter para seguir buscando: ")
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

            case "5" | "cinco" | "lotes":
                while True:
                    menu_lotes()
                    opcion_lotes = input("Seleccione una opción: ")

                    match normalizar(opcion_lotes):
                        case "1" | "uno" | "ver lotes":
                            ver_todos_lotes()
                            input("Presione Intro para continuar.")

                        case "2" | "dos" | "buscar lote":
                            buscar_por_lote()
                            input("Presione Intro para continuar.")

                        case "3" | "tres" | "configurar metodo":
                            "configurar_metodo_salida()"
                            input("Presione Intro para continuar.")

                        case "4" | "cuatro" | "proximo vencer":
                            ver_proximo_vencer_lotes()
                            input("Presione Intro para continuar.")

                        case "5" | "cinco" | "volver":
                            break

                        case "6" | "seis" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "6" | "seis" | "vencimientos":
                while True:
                    menu_vencimientos()
                    opcion_venc = input("Seleccione una opción: ")

                    match normalizar(opcion_venc):
                        case "1" | "uno" | "ver alertas":
                            verificar_vencimientos_proximos()
                            input("Presione Intro para continuar.")

                        case "2" | "dos" | "configurar alerta":
                            configurar_alerta_vencimiento()
                            input("Presione Intro para continuar.")

                        case "3" | "tres" | "ver vencidos":
                            verificar_vencidos()
                            input("Presione Intro para continuar.")

                        case "4" | "cuatro" | "no perecederos":
                            ver_productos_no_perecederos()
                            input("Presione Intro para continuar.")

                        case "5" | "cinco" | "sin vencimiento":
                            ver_sin_vencimiento_registrado()
                            input("Presione Intro para continuar.")

                        case "6" | "seis" | "volver":
                            break

                        case "7" | "siete" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "7" | "siete" | "otras opciones" | "otros":
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

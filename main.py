from funcion import (
    normalizar, ingresar, eliminar, modificar, gestionar_categoria_modo,
    buscar, escribir_log, verificar_umbral_minimo, configurar_umbral_minimo,
    existencias_sin_stock, productos_por_categoria, distribucion_precios,
    versionGS, formatearDB, cargar_memory, ingresar_paquete, 
    configurar_umbral_maximo, verificar_vencimientos_proximos, configurar_alerta_vencimiento, 
    verificar_vencidos, ver_productos_no_perecederos, verificar_alertas_vencimiento, 
    ver_todas_alertas_vencimiento, ver_todos_lotes, buscar_por_lote, configurar_metodo_salida, 
    ver_proximo_vencer_lotes, generador_de_sku, verificar_sobre_almacenamiento,
    ver_sin_vencimiento_registrado, gestionar_proveedores, limpiarPantalla
)


class Colores:
    NEGRITA = "\033[1m"
    NEUTRO = "\033[0m"
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CIAN = "\033[96m"
    BLANCO = "\033[97m"
    GRIS = "\033[90m"
    NARANJA = "\033[38;5;214m"
    ROSA = "\033[38;5;219m"
    BEIGE = "\033[38;5;223m"


def menu_principal():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║     {Colores.NEGRITA}SISTEMA DE INVENTARIO{Colores.NEUTRO}    ║
╠══════════════════════════════╣
║ {Colores.AZUL}1. SKU{Colores.NEUTRO}                       ║
║ {Colores.ROJO}2. Categorías{Colores.NEUTRO}                ║
║ {Colores.CIAN}3. Buscar{Colores.NEUTRO}                    ║
║ {Colores.AMARILLO}4. Umbrales{Colores.NEUTRO}                  ║
║ {Colores.MAGENTA}5. Lotes{Colores.NEUTRO}                     ║
║ {Colores.VERDE}6. Vencimientos{Colores.NEUTRO}              ║
║ {Colores.BEIGE}7. Otras opciones{Colores.NEUTRO}            ║
║ 8. Salir                     ║
╚══════════════════════════════╝""")


def menu_sku():
    limpiarPantalla()
    print(f"""{Colores.AZUL}╔══════════════════════════════╗
║        {Colores.NEGRITA}GESTIÓN DE SKU{Colores.NEUTRO}{Colores.AZUL}        ║
╠══════════════════════════════╣
║ 1. Agregar SKU               ║
║ 2. Agregar SKU por paquete   ║
║ 3. Eliminar SKU              ║
║ 4. Modificar SKU             ║
║ {Colores.NEUTRO}5. Volver al menú principal{Colores.AZUL}  ║
║ {Colores.NEUTRO}6. Salir{Colores.AZUL}                     ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def menu_categorias():
    limpiarPantalla()
    print(f"""{Colores.ROJO}╔══════════════════════════════╗
║     {Colores.NEGRITA}GESTIÓN DE CATEGORÍAS{Colores.NEUTRO}{Colores.ROJO}    ║
╠══════════════════════════════╣
║ 1. Agregar categoría         ║
║ 2. Eliminar categoría        ║
║ 3. Modificar categoría       ║
║ 4. Ver todas las categorías  ║
║ {Colores.NEUTRO}5. Volver al menú principal{Colores.ROJO}  ║
║ {Colores.NEUTRO}6. Salir{Colores.ROJO}                     ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def menu_buscar():
    limpiarPantalla()
    print(f"""{Colores.CIAN}╔══════════════════════════════╗
║           {Colores.NEGRITA}BUSQUEDA{Colores.NEUTRO}{Colores.CIAN}           ║
╠══════════════════════════════╣
║ 1. SKU                       ║
║ 2. Producto                  ║
║ 3. Cantidad                  ║
║ 4. Precio                    ║
║ 5. Categoria                 ║
║ {Colores.NEUTRO}6. Volver al menú principal{Colores.CIAN}  ║
║ {Colores.NEUTRO}7. Salir{Colores.CIAN}                     ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def menu_umbral():
    limpiarPantalla()
    print(f"""{Colores.AMARILLO}╔══════════════════════════════╗
║      {Colores.NEGRITA}GESTIÓN DE UMBRALES{Colores.NEUTRO}{Colores.AMARILLO}     ║
╠══════════════════════════════╣
║ 1. Ver alertas de inventario ║
║ 2. Configurar umbral mínimo  ║
║ 3. Configurar umbral máximo  ║
║ 4. Ver sobre almacenamiento  ║
║ 5. Ver productos sin stock   ║
║ {Colores.NEUTRO}6. Volver al menú principal{Colores.AMARILLO}  ║
║ {Colores.NEUTRO}7. Salir{Colores.AMARILLO}                     ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def menu_otros():
    limpiarPantalla()
    print(f"""{Colores.BEIGE}╔══════════════════════════════╗
║       {Colores.NEGRITA}OTRAS OPCIONES{Colores.NEUTRO}{Colores.BEIGE}         ║
╠══════════════════════════════╣
║ 1. Estadísticas              ║
║ 2. Versión genzaloSTORAGE    ║
║ 3. Formatear base de datos   ║
║ {Colores.NEUTRO}4. Volver al menú principal{Colores.BEIGE}  ║
║ {Colores.NEUTRO}5. Salir{Colores.BEIGE}                     ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def menu_vencimientos():
    limpiarPantalla()
    print(f"""{Colores.VERDE}╔══════════════════════════════╗
║        {Colores.NEGRITA}VENCIMIENTOS{Colores.NEUTRO}{Colores.VERDE}          ║
╠══════════════════════════════╣
║ 1. Ver productos próximos    ║
║ 2. Configurar alertas        ║
║ 3. Ver productos vencidos    ║
║ 4. Ver no perecederos        ║
║ 5. Ver prod. s/ venc. reg.   ║
║ {Colores.NEUTRO}6. Volver al menú principal{Colores.VERDE}  ║
║ {Colores.NEUTRO}7. Salir{Colores.VERDE}                     ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def menu_estadisticas():
    limpiarPantalla()
    print(f"""╔══════════════════════════════╗
║         {Colores.NEGRITA}ESTADÍSTICAS{Colores.NEUTRO}         ║
╠══════════════════════════════╣
║ 1. Resumen general           ║
║ 2. Productos por categoría   ║
║ 3. Distribución de precios   ║
║ 4. Volver al menú anterior   ║
║ 5. Salir del programa        ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def menu_lotes():
    limpiarPantalla()
    print(f"""{Colores.MAGENTA}╔══════════════════════════════╗
║        {Colores.NEGRITA}GESTIÓN DE LOTES{Colores.NEUTRO}{Colores.MAGENTA}      ║
╠══════════════════════════════╣
║ 1. Ver todos los lotes       ║
║ 2. Buscar por lote           ║
║ 3. Configurar método salida  ║
║ 4. Ver próximo a vencer      ║
║ {Colores.NEUTRO}5. Volver al menú principal{Colores.MAGENTA}  ║
║ {Colores.NEUTRO}6. Salir{Colores.MAGENTA}                     ║
╚══════════════════════════════╝{Colores.NEUTRO}""")


def exit_program():
    print("¡Gracias por usar genzaloSTORAGE!")
    raise SystemExit


try:
    escribir_log("Inicio del programa.", nivel="INFO")
    while True:
        limpiarPantalla()
        menu_principal()
        seleccion = input("Seleccione una opción: ")
        continuar = 0

        match normalizar(seleccion):
            case "1" | "uno" | "sku":
                while True:
                    menu_sku()
                    opcion_sku = input("Seleccione una opción: ")
                    continuar = 0
                    match normalizar(opcion_sku):
                        case "1" | "uno" | "agregar" | "agregar sku":
                            while continuar != -1:
                                ingresar()
                                continuar = int(
                                    input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))

                        case "2" | "dos" | "agregar paquete" | "paquete":
                            while continuar != -1:
                                ingresar_paquete()
                                continuar = int(
                                    input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))

                        case "3" | "tres" | "eliminar" | "eliminar sku":
                            eliminar()
                            while continuar != -1:
                                eliminar()
                                continuar = int(input("Ingrese cualquier valor para seguir eliminando o -1 para salir: "))
                            input("Presione Intro para continuar.")

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
                            break

                        case "6" | "seis" | "salir":
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
                            configurar_metodo_salida()
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
                        case "1" | "uno" | "estadisticas":
                            while True:
                                menu_estadisticas()
                                opcion_estad = input("Seleccione una opción: ")

                                match normalizar(opcion_estad):
                                    case "1" | "uno" | "resumen":
                                        from funcion import resumen_estadisticas
                                        resumen_estadisticas()
                                        input("Presione Intro para continuar.")

                                    case "2" | "dos" | "categorias":
                                        productos_por_categoria()
                                        input("Presione Intro para continuar.")

                                    case "3" | "tres" | "distribucion":
                                        distribucion_precios()
                                        input("Presione Intro para continuar.")

                                    case "4" | "cuatro" | "volver":
                                        break

                                    case "5" | "cinco" | "salir":
                                        exit_program()

                                    case _:
                                        print("¡Error! Opción no válida.")
                                        input("Presione Intro para continuar.")

                        case "2" | "dos" | "version":
                            versionGS()
                            input("Presione Intro para continuar.")

                        case "3" | "tres" | "formatear":
                            formatearDB()
                            input("Presione Intro para continuar.")

                        case "4" | "cuatro" | "volver":
                            break

                        case "5" | "cinco" | "salir":
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

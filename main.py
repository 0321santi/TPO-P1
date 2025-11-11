from funcion import (
    normalizar, ingresar, eliminar, modificar, gestionar_categoria_modo,
    buscar, escribir_log, verificar_umbral_minimo, configurar_umbral_minimo,
    mostrar_valor_total, producto_mas_barato, producto_mas_caro, promedio_precios,
    existencias_sin_stock, productos_por_categoria, distribucion_precios, 
    version_genzalostorage, formatear_base_datos, 
    cargar_memory, ingresar_paquete, configurar_umbral_maximo,
    verificar_sobre_almacenamiento, gestionar_vencimientos,
    configurar_alerta_vencimiento, verificar_alertas_vencimiento,
    ver_todas_alertas_vencimiento, verificar_vencidos, ver_productos_no_perecederos
)

def menu_principal():
    print("""╔══════════════════════════════╗
║     SISTEMA DE INVENTARIO    ║
╠══════════════════════════════╣
║ 1. SKU                       ║
║ 2. Categorías                ║
║ 3. Buscar                    ║
║ 4. Umbrales                  ║
║ 5. Otras opciones            ║
║ 6. Salir                     ║
╚══════════════════════════════╝""")

def menu_sku():
    print("""╔══════════════════════════════╗
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
    print("""╔══════════════════════════════╗
║     GESTIÓN DE CATEGORÍAS    ║
╠══════════════════════════════╣
║ 1. Agregar categoría         ║
║ 2. Eliminar categoría        ║
║ 3. Modificar categoría       ║
║ 4. Ver todas las categorías  ║
║ 5. Volver al menú principal  ║
║ 6. Salir                     ║
╚══════════════════════════════╝""")

def menu_buscar():
    print("""╔══════════════════════════════╗
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
    print("""╔══════════════════════════════╗
║      GESTIÓN DE UMBRALES     ║
╠══════════════════════════════╣
║ 1. Ver alertas de inventario ║
║ 2. Configurar umbral mínimo  ║
║ 3. Configurar umbral máximo  ║
║ 4. Ver sobre almacenamiento  ║
║ 5. Volver al menú principal  ║
║ 6. Salir                     ║
╚══════════════════════════════╝""")

def menu_otros():
    print("""╔══════════════════════════════╗
║       OTRAS OPCIONES         ║
╠══════════════════════════════╣
║ 1. Valores                   ║
║ 2. Existencias               ║
║ 3. Estadísticas              ║
║ 4. Vencimientos              ║
║ 5. Volver al menú principal  ║
║ 6. Salir                     ║
╚══════════════════════════════╝""")

def menu_vencimientos():
    print("""╔══════════════════════════════╗
║        VENCIMIENTOS          ║
╠══════════════════════════════╣
║ 1. Ver productos próximos    ║
║ 2. Configurar alertas        ║
║ 3. Ver productos vencidos    ║
║ 4. Ver no perecederos        ║
║ 5. Volver al menú principal  ║
║ 6. Salir                     ║
╚══════════════════════════════╝""")

def menu_valores():
    print("""╔══════════════════════════════╗
║           VALORES            ║
╠══════════════════════════════╣
║ 1. Valor total               ║
║ 2. Producto más barato       ║
║ 3. Producto más caro         ║
║ 4. Promedio de precios       ║
║ 5. Volver al menú principal  ║
║ 6. Salir del programa        ║
╚══════════════════════════════╝""")

def menu_existencias():
    print("""╔══════════════════════════════╗
║         EXISTENCIAS          ║
╠══════════════════════════════╣
║ 1. Sin existencias           ║
║ 2. Existencias muy bajas     ║
║ 3. Existencias bajas         ║
║ 4. Existencias aceptables    ║
║ 5. Existencias altas         ║
║ 6. Sobre almacenamiento      ║
║ 7. Volver al menú principal  ║
║ 8. Salir del programa        ║
╚══════════════════════════════╝""")

def menu_estadisticas():
    print("""╔══════════════════════════════╗
║         ESTADÍSTICAS         ║
╠══════════════════════════════╣
║ 1. Resumen general           ║
║ 2. Productos por categoría   ║
║ 3. Distribución de precios   ║
║ 4. Volver al menú principal  ║
║ 5. Salir del programa        ║
╚══════════════════════════════╝""")


def menu_otros_sub():
    print("""╔══════════════════════════════╗
║           OTROS              ║
╠══════════════════════════════╣
║ 1. Versión genzaloSTORAGE    ║
║ 2. Formatear base de datos   ║
║ 3. Volver al menú principal  ║
║ 4. Salir del programa        ║
╚══════════════════════════════╝""")

def exit_program():
    print("¡Gracias por usar genzaloSTORAGE!")
    raise SystemExit

try:
    escribir_log("Inicio del programa.", nivel="INFO")
    while True:
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
                                continuar = int(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))

                        case "2" | "dos" | "agregar paquete" | "paquete":
                            while continuar != -1:
                                ingresar_paquete()
                                continuar = int(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))

                        case "3" | "tres" | "eliminar" | "eliminar sku":
                            eliminar()
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
                menu_buscar()
                buscar()
                input("Presione Intro para continuar.")

            case "4" | "cuatro" | "umbral" | "gestión de umbrales":
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

                        case "5" | "cinco" | "volver" | "menu principal":
                            break

                        case "6" | "seis" | "salir":
                            exit_program()

                        case _:
                            print("¡Error! Opción no válida.")
                            input("Presione Intro para continuar.")

            case "5" | "cinco" | "otras opciones" | "otros":
                while True:
                    menu_otros()
                    opcion_otros = input("Seleccione una opción: ")

                    match normalizar(opcion_otros):
                        case "1" | "uno" | "valores":
                            while True:
                                menu_valores()
                                opcion_valores = input("Seleccione una opción: ")

                                match normalizar(opcion_valores):
                                    case "1" | "uno" | "valor total":
                                        mostrar_valor_total()
                                        input("Presione Intro para continuar.")

                                    case "2" | "dos" | "producto mas barato":
                                        producto_mas_barato()
                                        input("Presione Intro para continuar.")

                                    case "3" | "tres" | "producto mas caro":
                                        producto_mas_caro()
                                        input("Presione Intro para continuar.")

                                    case "4" | "cuatro" | "promedio":
                                        promedio_precios()
                                        input("Presione Intro para continuar.")

                                    case "5" | "cinco" | "volver":
                                        break

                                    case "6" | "seis" | "salir":
                                        exit_program()

                                    case _:
                                        print("¡Error! Opción no válida.")
                                        input("Presione Intro para continuar.")

                        case "2" | "dos" | "existencias":
                            while True:
                                menu_existencias()
                                opcion_exist = input("Seleccione una opción: ")

                                match normalizar(opcion_exist):
                                    case "1" | "uno" | "sin existencias":
                                        existencias_sin_stock()
                                        input("Presione Intro para continuar.")

                                    case "2" | "dos" | "muy bajas":
                                        data = cargar_memory()
                                        productos = data["productos"]
                                        muy_bajas = [prod for prod in productos if prod["existencias"] <= prod.get("umbral_minimo", 5)]

                                        if muy_bajas:
                                            print("Productos con existencias muy bajas:")
                                            for prod in muy_bajas:
                                                umbral = prod.get("umbral_minimo", 5)
                                                print(f"«{prod['nombre']}» (SKU: {prod['sku']}): {prod['existencias']} (Umbral: {umbral})")
                                        else:
                                            print("No hay productos con existencias muy bajas.")
                                        input("Presione Intro para continuar.")

                                    case "3" | "tres" | "bajas":
                                        data = cargar_memory()
                                        productos = data["productos"]
                                        bajas = []
                                        for prod in productos:
                                            umbral = prod.get("umbral_minimo", 5)
                                            existencias = prod["existencias"]
                                            if umbral < existencias <= umbral * 2:
                                                bajas.append(prod)

                                        if bajas:
                                            print("Productos con existencias bajas:")
                                            for prod in bajas:
                                                umbral = prod.get("umbral_minimo", 5)
                                                print(f"«{prod['nombre']}» (SKU: {prod['sku']}): {prod['existencias']} (Umbral: {umbral})")
                                        else:
                                            print("No hay productos con existencias bajas.")
                                        input("Presione Intro para continuar.")

                                    case "4" | "cuatro" | "aceptables":
                                        data = cargar_memory()
                                        productos = data["productos"]
                                        aceptables = []
                                        for prod in productos:
                                            umbral = prod.get("umbral_minimo", 5)
                                            existencias = prod["existencias"]
                                            if umbral * 2 < existencias <= umbral * 3.5:
                                                aceptables.append(prod)

                                        if aceptables:
                                            print("Productos con existencias aceptables:")
                                            for prod in aceptables:
                                                umbral = prod.get("umbral_minimo", 5)
                                                print(f"«{prod['nombre']}» (SKU: {prod['sku']}): {prod['existencias']} (Umbral: {umbral})")
                                        else:
                                            print("No hay productos con existencias aceptables.")
                                        input("Presione Intro para continuar.")

                                    case "5" | "cinco" | "altas":
                                        data = cargar_memory()
                                        productos = data["productos"]
                                        altas = []
                                        for prod in productos:
                                            umbral = prod.get("umbral_minimo", 5)
                                            existencias = prod["existencias"]
                                            if umbral * 3.5 < existencias <= umbral * 6:
                                                altas.append(prod)

                                        if altas:
                                            print("Productos con existencias altas:")
                                            for prod in altas:
                                                umbral = prod.get("umbral_minimo", 5)
                                                print(f"«{prod['nombre']}» (SKU: {prod['sku']}): {prod['existencias']} (Umbral: {umbral})")
                                        else:
                                            print(
                                                "No hay productos con existencias altas.")
                                        input("Presione Intro para continuar.")

                                    case "6" | "seis" | "sobre almacenamiento":
                                        verificar_sobre_almacenamiento()
                                        input("Presione Intro para continuar.")

                                    case "7" | "siete" | "volver":
                                        break

                                    case "8" | "ocho" | "salir":
                                        exit_program()

                                    case _:
                                        print("¡Error! Opción no válida.")
                                        input("Presione Intro para continuar.")

                        case "3" | "tres" | "estadisticas":
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

                        case "4" | "cuatro" | "vencimientos":
                            gestionar_vencimientos()
    
                        case "5" | "cinco" | "otros sub":
                            while True:
                                menu_otros_sub()
                                opcion_otros_sub = input("Seleccione una opción: ")

                                match normalizar(opcion_otros_sub):

                                    case "1" | "uno" | "version":
                                        version_genzalostorage()
                                        input("Presione Intro para continuar.")

                                    case "2" | "dos" | "formatear":
                                        formatear_base_datos()
                                        input("Presione Intro para continuar.")

                                    case "3" | "tres" | "volver":
                                        break

                                    case "4" | "cuatro" | "salir":
                                        exit_program()

                                    case _:
                                        print("¡Error! Opción no válida.")
                                        input("Presione Intro para continuar.")

                        case "6" | "seis" | "volver":
                            break

            case "6" | "seis" | "salir":
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
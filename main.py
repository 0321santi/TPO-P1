
'''
mostrar una lista por búsqueda aproximada (filtrar por nombre parcial)
opción de salir
Manejar categorías (lácteos, especias... ósea filtrar por tipo de producto)
Stock mínimo
Mejorar como se ve la matriz (Sacar corchetes y todo lo demas)
Matrices traspuestas 
return adentro de for :'c
agregar la posibilidad de agregarle subcategorías a las categorías determinado por cliente.
Agregar una guía (biblia) que explique determiandamente que hace el programa.
modo de edición, modo de ingreso.
'''


# programa principal (versión actualizada)
from funcion import normalizar, ingresar, eliminar, modificar, gestionar_categoria_modo, buscar, cargar_memory

def menu_principal():
    print("""╔══════════════════════════════╗
║        SISTEMA DE INVENTARIO      ║
╠══════════════════════════════╣
║ 1. SKU                        ║
║ 2. Categorías                 ║
║ 3. Buscar                     ║
║ 4. Salir                      ║
╚══════════════════════════════╝""")

def menu_sku():
    print("""╔══════════════════════════════╗
║           GESTIÓN DE SKU         ║
╠══════════════════════════════╣
║ 1. Agregar SKU                ║
║ 2. Eliminar SKU               ║
║ 3. Modificar SKU              ║
║ 4. Volver al menú principal   ║
╚══════════════════════════════╝""")

def menu_categorias():
    print("""╔══════════════════════════════╗
║        GESTIÓN DE CATEGORÍAS    ║
╠══════════════════════════════╣
║ 1. Agregar categoría          ║
║ 2. Eliminar categoría         ║
║ 3. Modificar categoría        ║
║ 4. Ver todas las categorías   ║
║ 5. Volver al menú principal   ║
╚══════════════════════════════╝""")

try:
    while True:
        menu_principal()
        seleccion = input("Seleccione una opción: ")
        
        match normalizar(seleccion):
            case "1" | "uno" | "sku":
                while True:
                    menu_sku()
                    opcion_sku = input("Seleccione una opción: ")
                    
                    match normalizar(opcion_sku):
                        case "1" | "uno" | "agregar" | "agregar sku":
                            ingresar()
                            input("Presione Enter para continuar...")
                            
                        case "2" | "dos" | "eliminar" | "eliminar sku":
                            eliminar()
                            input("Presione Enter para continuar...")
                            
                        case "3" | "tres" | "modificar" | "modificar sku":
                            modificar()
                            input("Presione Enter para continuar...")
                            
                        case "4" | "cuatro" | "volver" | "menu principal":
                            break
                            
                        case _:
                            print("¡Error! Opción no válida…")
                            input("Presione Enter para continuar...")
            
            case "2" | "dos" | "categorias" | "categorías":
                while True:
                    menu_categorias()
                    opcion_cat = input("Seleccione una opción: ")
                    
                    match normalizar(opcion_cat):
                        case "1" | "uno" | "agregar" | "agregar categoría":
                            gestionar_categoria_modo("agregar")
                            input("Presione Enter para continuar...")
                            
                        case "2" | "dos" | "eliminar" | "eliminar categoría":
                            gestionar_categoria_modo("eliminar")
                            input("Presione Enter para continuar...")
                            
                        case "3" | "tres" | "modificar" | "modificar categoría":
                            gestionar_categoria_modo("modificar")
                            input("Presione Enter para continuar...")
                            
                        case "4" | "cuatro" | "ver" | "ver categorías":
                            gestionar_categoria_modo("ver")
                            input("Presione Enter para continuar...")
                            
                        case "5" | "cinco" | "volver" | "menu principal":
                            break
                            
                        case _:
                            print("¡Error! Opción no válida…")
                            input("Presione Enter para continuar...")
            
            case "3" | "tres" | "buscar":
                buscar()
                input("Presione Enter para continuar...")
            
            case "4" | "cuatro" | "salir":
                print("¡Gracias por usar el sistema!")
                break
            
            case _:
                print("¡Error! Opción no válida…")
                input("Presione Enter para continuar...")

except Exception as e:
    print("¡Error! Ha ocurrido un problema:", e)
    input("Presione Enter para continuar...")

finally:
    print("Programa finalizado.")

finally:
    print("Programa finalizado.")


#No hay tabla de todos los productos y categorias (Osea siento que deberia haber un display pero al profe no le gustaba)

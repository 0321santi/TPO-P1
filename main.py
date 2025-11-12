# programa principal
from funcion import (normalizar, ingresar, eliminar, modificar, gestionar_categoria_modo, 
                    buscar, escribir_log, gestionar_clientes_modo, analisis_financiero_completo,
                    gestionar_proveedores_modo)

def menu_principal():
    print("""╔══════════════════════════════╗
║     SISTEMA DE INVENTARIO    ║
╠══════════════════════════════╣
║ 1. SKU                       ║
║ 2. Categorías                ║
║ 3. Clientes                  ║
║ 4. Proveedores               ║
║ 5. Buscar                    ║
║ 6. Análisis Financiero       ║
║ 7. Salir                     ║
╚══════════════════════════════╝""")

def menu_sku():
    print("""╔══════════════════════════════╗
║        GESTIÓN DE SKU        ║
╠══════════════════════════════╣
║ 1. Agregar SKU               ║
║ 2. Eliminar SKU              ║
║ 3. Modificar SKU             ║
║ 4. Volver al menú principal  ║
║ 5. Salir                     ║
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

def menu_clientes():
    print("""╔══════════════════════════════╗
║      GESTIÓN DE CLIENTES     ║
╠══════════════════════════════╣
║ 1. Agregar cliente           ║
║ 2. Eliminar cliente          ║
║ 3. Modificar cliente         ║
║ 4. Buscar/Ver clientes       ║
║ 5. Volver al menú principal  ║
║ 6. Salir                     ║
╚══════════════════════════════╝""")

def menu_proveedores():
    print("""╔══════════════════════════════╗
║    GESTIÓN DE PROVEEDORES    ║
╠══════════════════════════════╣
║ 1. Agregar proveedor         ║
║ 2. Eliminar proveedor        ║
║ 3. Modificar proveedor       ║
║ 4. Buscar/Ver proveedores    ║
║ 5. Análisis de proveedores   ║
║ 6. Volver al menú principal  ║
║ 7. Salir                     ║
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
║ 6. Análisis Financiero       ║
║ 7. Volver al menú principal  ║
╚══════════════════════════════╝""")

def exit():
    print("¡Gracias por usar el sistema!")
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
                            while continuar not in ("no","-1" ):
                                ingresar()
                                continuar = normalizar(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))
                            
                        case "2" | "dos" | "eliminar" | "eliminar sku":
                            while continuar not in ("no","-1" ):
                                eliminar()
                                continuar = normalizar(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))                            
                        
                        case "3" | "tres" | "modificar" | "modificar sku":
                            while continuar not in ("no","-1" ):
                                modificar()
                                continuar = normalizar(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))
                                
                        case "4" | "cuatro" | "volver" | "menu principal":
                            break
                        
                        case "5" | "cinco" | "salir":
                            exit()
                            
                        case _:
                            print("¡Error! Opción no válida…")
                            
            
            case "2" | "dos" | "categorias" | "categorías":
                while True:
                    menu_categorias()
                    opcion_cat = input("Seleccione una opción: ")
                    continuar = 0
                    
                    match normalizar(opcion_cat):
                        case "1" | "uno" | "agregar" | "agregar categoría":
                            while continuar not in ("no","-1" ):
                                gestionar_categoria_modo("agregar")
                                continuar = normalizar(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))
                            
                        case "2" | "dos" | "eliminar" | "eliminar categoría":
                            while continuar not in ("no","-1" ):
                                gestionar_categoria_modo("eliminar")
                                continuar = normalizar(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))
                            
                        case "3" | "tres" | "modificar" | "modificar categoría":
                            while continuar not in ("no","-1" ):
                                gestionar_categoria_modo("modificar")
                                continuar = normalizar(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))
                            
                        case "4" | "cuatro" | "ver" | "ver categorías":
                            while continuar not in ("no","-1" ):
                                gestionar_categoria_modo("ver")
                                continuar = normalizar(input("Ingrese cualquier valor para seguir o ingrese -1 para salir: "))
                            
                        case "5" | "cinco" | "volver" | "menu principal":
                            break
                        
                        case "6" | "seis" | "salir":
                            exit()
                            
                        case _:
                            print("¡Error! Opción no válida…")
                            
            
            case "3" | "tres" | "clientes":
                while True:
                    menu_clientes()
                    opcion_cli = input("Seleccione una opción: ")
                    
                    match normalizar(opcion_cli):
                        case "1" | "uno" | "agregar" | "agregar cliente":
                            gestionar_clientes_modo("agregar")
                            
                        case "2" | "dos" | "eliminar" | "eliminar cliente":
                            gestionar_clientes_modo("eliminar")
                            
                        case "3" | "tres" | "modificar" | "modificar cliente":
                            gestionar_clientes_modo("modificar")
                            
                        case "4" | "cuatro" | "buscar" | "ver" | "buscar clientes":
                            gestionar_clientes_modo("buscar")
                            
                        case "5" | "cinco" | "volver" | "menu principal":
                            break
                        
                        case "6" | "seis" | "salir":
                            exit()
                            
                        case _:
                            print("¡Error! Opción no válida…")
                            
            
            case "4" | "cuatro" | "proveedores":
                while True:
                    menu_proveedores()
                    opcion_prov = input("Seleccione una opción: ")
                    
                    match normalizar(opcion_prov):
                        case "1" | "uno" | "agregar" | "agregar proveedor":
                            gestionar_proveedores_modo("agregar")
                            
                        case "2" | "dos" | "eliminar" | "eliminar proveedor":
                            gestionar_proveedores_modo("eliminar")
                            
                        case "3" | "tres" | "modificar" | "modificar proveedor":
                            gestionar_proveedores_modo("modificar")
                            
                        case "4" | "cuatro" | "buscar" | "ver" | "buscar proveedores":
                            gestionar_proveedores_modo("buscar")
                            
                        case "5" | "cinco" | "analizar" | "análisis":
                            gestionar_proveedores_modo("analizar")
                            
                        case "6" | "seis" | "volver" | "menu principal":
                            break
                        
                        case "7" | "siete" | "salir":
                            exit()
                            
                        case _:
                            print("¡Error! Opción no válida…")
                            
            
            case "5" | "cinco" | "buscar":
                menu_buscar()
                buscar()
                
            
            case "6" | "seis" | "analisis" | "análisis" | "financiero":
                analisis_financiero_completo()
                
            
            case "7" | "siete" | "salir":
                print("¡Gracias por usar el sistema!")
                break
            
            case _:
                print("¡Error! Opción no válida…")
                

except Exception as e:
    print("¡Error! Ha ocurrido un problema:", e)
    escribir_log(f"Error inesperado: {e}", nivel="ERROR")
    

finally:
    escribir_log("Fin del programa.", nivel="INFO")
    print("Programa finalizado.")
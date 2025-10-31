
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


# ...existing code...
from funcion import normalizar, ingresar, buscar, eliminar, modificar

# programa principal
try:
    matriz = []

    while True:
        seleccion = input("Ingrese que quiere hacer (0 para opciones): ")
        match normalizar(seleccion):
            case "0" | "cero" | "opciones":
                print("""Opciones disponibles:
            1. Ingresar sku
            2. Buscar
            3. Eliminar sku
            4. Modificar categorias
            5. Salir""")


            case "1" | "uno" | "ingresar" | "ingresar sku": #Se deberia poner para ingresar dentro de las categorias existentes (no permitir ingresar si no existen categorias)
                ingresar(matriz)
                otro = normalizar(input("¿Desea ingresar otro SKU? (0=no, 1=sí): "))
                while otro in ("1", "si", "yes"):
                    ingresar(matriz)
                    otro = normalizar(input("¿Desea ingresar otro SKU? (0=no, 1=sí): "))
                while otro not in ("0", "no", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea ingresar otro SKU? (0=no, 1=sí): "))

            case "2" | "dos" | "buscar" | "buscar sku": #busqueda aproximada
                buscar(matriz)
                otro = normalizar(input("¿Desea buscar otro SKU? (0=no, 1=sí): "))
                while otro in ("1", "si", "yes"):
                    buscar(matriz)
                    otro = normalizar(input("¿Desea buscar otro SKU? (0=no, 1=sí): "))
                while otro not in ("0", "no", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea buscar otro SKU? (0=no, 1=sí): "))

            case "3" | "tres" | "eliminar" | "eliminar sku": #capaz podemos sacar esto y ponerlo dentro de la modificacion de categorias?
                eliminar(matriz)
                otro = normalizar(input("¿Desea eliminar otro SKU? (0=no, 1=sí): "))
                while otro in ("1", "si", "yes"):
                    eliminar(matriz)
                    otro = normalizar(input("¿Desea eliminar otro SKU? (0=no, 1=sí): "))
                while otro not in ("0", "no", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea eliminar otro SKU? (0=no, 1=sí): "))

            case "4" | "cuatro" | "modificar": #deberia modificar las categorias y sub categorias (creacion ilimitada de categorias)
                modificar(matriz)
                otro = normalizar(input("¿Desea modificar otro SKU? (0=no, 1=sí): "))
                while otro in ("1", "si", "yes"):
                    modificar(matriz)
                    otro = normalizar(input("¿Desea modificar otro SKU? (0=no, 1=sí): "))
                while otro not in ("0", "no", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea modificar otro SKU? (0=no, 1=sí): "))

            case "5" | "cinco" | "salir":
                break

            case _:
                print("¡Error! Opción no válida…")

except Exception as e:
    print("¡Error! Ha ocurrido un problema:", e)

finally:
    print("Programa finalizado.")

# ...existing code...
from funcion import normalizar, ingresar, buscar, eliminar, modificar

# programa principal
try:
    matriz = []
    print("""Bienvenido, seleccione una opción:
        1. Ingresar 
        2. Buscar 
        3. Eliminar 
        4. Modificar
        5. Salir""")

    while True:
        seleccion = input("Opción seleccionada: ")
        match normalizar(seleccion):
            case "0" | "cero" | "opciones":
                print("""Opciones disponibles:
            1. Ingresar 
            2. Buscar 
            3. Eliminar 
            4. Modificar
            5. Salir""")

            case "1" | "uno" | "ingresar" | "ingresar sku":
                ingresar(matriz)
                otro = normalizar(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))
                while otro in ("1", "si", "yes"):
                    ingresar(matriz)
                    otro = normalizar(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))
                while otro not in ("0", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))

            case "2" | "dos" | "buscar" | "buscar sku":
                buscar(matriz)
                otro = normalizar(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))
                while otro in ("1", "si", "yes"):
                    buscar(matriz)
                    otro = normalizar(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))
                while otro not in ("0", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))

            case "3" | "tres" | "eliminar" | "eliminar sku":
                eliminar(matriz)
                otro = normalizar(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))
                while otro in ("1", "si", "yes"):
                    eliminar(matriz)
                    otro = normalizar(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))
                while otro not in ("0", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))

            case "4" | "cuatro" | "modificar":
                modificar(matriz)
                otro = normalizar(input("¿Desea modificar otro SKU? (0=NO, 1=SÍ): "))
                while otro in ("1", "si", "yes"):
                    modificar(matriz)
                    otro = normalizar(input("¿Desea modificar otro SKU? (0=NO, 1=SÍ): "))
                while otro not in ("0", "1", "si", "yes"):
                    print("¡Error! Opción no válida…")
                    otro = normalizar(input("¿Desea modificar otro SKU? (0=NO, 1=SÍ): "))

            case "5" | "cinco" | "salir":
                break

            case _:
                print("¡Error! Opción no válida…")

except Exception as e:
    print("¡Error! Ha ocurrido un problema:", e)

finally:
    print("Programa finalizado.")

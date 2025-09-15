def ingresar_sku(matriz):
    error = False
    sku = int(input("Ingrese el SKU: "))
    for item in matriz:
        if item[0] == sku:
            error = True
            print("¡Error! El SKU ya existe…")
            while error == True:
                error = False
                sku = int(input("Ingrese otro SKU: "))
                if item[0] == sku:
                    error = True
    existencias = int(input("Ingrese las existencias: "))
    while existencias <= 0:
        existencias = int(input("¡Error! Ingrese un numero válido…: "))
    producto = input("Ingrese el nombre del producto: ")
    for nombre in matriz:
        if nombre[1] == producto:
            error = True
            print("¡Error! El nombre ya esta en uso…")
            while error == True:
                error = False
                producto = input("Ingrese otro nombre: ")
                if nombre[1] == producto:
                    error = True
    matriz.append([sku, producto, existencias])
    print("SKU y existencias ingresados correctamente.")
    return matriz

def normalizar(texto):
    return texto.strip().lower()

def buscar_sku(matriz, bandera):
    sku = int(input("Ingrese el SKU a buscar: "))
    for item in matriz:
        if item[0] == sku:
            print(
                f"El SKU Nº {sku} corresponde al producto «{item[1]}» y tiene {item[2]} existencia(s).")
            return bandera == True
    print("¡Error! SKU no encontrado…")
    return bandera == False


def buscar_producto(matriz):
    producto = input("Ingrese el nombre del producto a buscar: ")
    for item in matriz:
        if item[1] == producto.lower():
            print(
                f"El producto «{item[1]}» tiene SKU Nº {item[0]} y {item[2]} existencia(s).")
            return
    print("¡Error! Producto no encontrado")
    return

def modificar(matriz):
    seleccion2 = normalizar(input("modificar SKU (1) o Producto (2) o Existencias (3): "))
    match seleccion2:
        case "1"|"uno"|"modificar sku":
            sku = int(input("Ingrese el SKU a modificar: "))
            for item in matriz:
                if item[0] == sku:
                    nuevo_sku = int(input("Ingrese el nuevo SKU: "))
                    item[0] = nuevo_sku
                    print("SKU modificado correctamente.")
                    return
        case "2"|"dos"|"modificar producto":
            producto = input("Ingrese el nombre del producto a modificar: ")
            for item in matriz:
                if item[1] == producto:
                    nuevo_producto = input("Ingrese el nuevo nombre del producto: ")
                    item[1] = nuevo_producto
                    print("Producto modificado correctamente.")
                    return
        case "3"|"tres"|"modificar existencias":
            sku = int(input("Ingrese el SKU del producto cuyas existencias desea modificar: ")) 
            for item in matriz:
                if item[0] == sku:
                    nuevas_existencias = int(input("Ingrese las nuevas existencias: "))
                    item[2] = nuevas_existencias
                    print("Existencias modificadas correctamente.")
                    return
        case _:
            print("¡Error! Opción no válida…")

def eliminar_sku(matriz):
    seleccion2 = normalizar(input("Eliminar por SKU (1), Eliminar Producto (2)"))
    match seleccion2:
        case "1"|"uno"|" sku":
            sku = int(input("Ingrese el SKU a eliminar: "))
            for i, item in enumerate(matriz):
                if item[0] == sku:
                    matriz.pop(i)
                    print("SKU eliminado correctamente.")
                    return
            print("¡Error! SKU no encontrado…")
        case "2"|"dos"|"eliminar producto":
            producto = normalizar(input("Ingrese el nombre del producto a eliminar: "))
            for i, item in enumerate(matriz):
                if normalizar(item[1]) == producto:
                    matriz.pop(i)
                    print("Producto eliminado correctamente.")
                    return
            print("¡Error! Producto no encontrado…")
        case _:
            print("¡Error! Opción no válida…")


# programa principal
matriz = []
print("""Bienvenido, seleccione una opción:
      1. Ingresar SKU
      2. Buscar SKU
      3. Buscar Producto
      4. Eliminar SKU
      5. Mostrar Inventario
      6. Salir
      7. Otros""")

while True:
    seleccion = (input("Opción seleccionada: "))
    match normalizar(seleccion):
        case "0" |"cero"|"opciones":
            print("""Opciones disponibles:
        1. Ingresar SKU
        2. Buscar SKU
        3. Buscar Producto
        4. Eliminar SKU
        5. Mostrar Inventario
        6. Salir
        7. Otros""")

        case "1"|"uno"|"ingresar sku":
            ingresar_sku(matriz)
            otro = normalizar(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))
            while otro in ("1", "si", "yes"):
                ingresar_sku(matriz)
                otro = normalizar(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))
            while otro not in ("0", "1", "si", "yes"):
                print("¡Error! Opción no válida…")
                otro = normalizar(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))
                
        case "2"|"dos"|"buscar sku":
            bandera = True
            buscar_sku(matriz, bandera)
            if bandera == False:
                seleccion1 = normalizar(input("¿Desea ingresarlo? (0=NO, 1=SÍ): "))
                if seleccion1 in ("1", "si", "yes"):
                    ingresar_sku(matriz)
            otro = normalizar(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))
            while otro == 1:
                buscar_sku(matriz, bandera)
                if bandera == False:
                    seleccion1 = normalizar(input("¿Desea ingresarlo? (0=NO, 1=SÍ): "))
                    if seleccion1 in ("1", "si", "yes"):
                        ingresar_sku(matriz)
                otro = normalizar(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))
            while otro not in ("0", "1", "si", "yes"):
                print("¡Error! Opción no válida…")
                otro = int(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))

        case "3"|"tres"|"buscar producto":
            buscar_producto(matriz)
            otro = int(input("¿Desea buscar otro producto? (0=NO, 1=SÍ): "))
            while otro in (1, "si", "yes"):
                buscar_producto(matriz)
                otro = int(input("¿Desea buscar otro producto? (0=NO, 1=SÍ): "))
            while otro not in (0, 1, "si", "yes"):
                print("¡Error! Opción no válida…")
                otro = int(input("¿Desea buscar otro producto? (0=NO, 1=SÍ): "))

        case "4"|"cuatro"|"eliminar sku":
            eliminar_sku(matriz)
            otro = int(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))
            while otro in (1, "si", "yes"):
                eliminar_sku(matriz)
                otro = int(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))
            while otro not in (0, 1, "si", "yes"):
                print("¡Error! Opción no válida…")
                otro = int(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))

        case "5"|"cinco"|"mostrar inventario":
            print("Inventario actual")
            print("[SKU, Nombre, Existencias]")
            for fila in matriz:
                print(fila)

        case "6"|"seis"|"salir":
            print("Gracias por usar el programa…")
            print("Inventario final ([SKU, Nombre, Existencias]):", matriz)
            break

        case "7"|"siete"|"otros":
            print("Versión de GenzaloStorage: 0.1 ALFA")

        case _:
            print("¡Error! Opción no válida…")

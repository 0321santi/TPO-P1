# funciones
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


def eliminar_sku(matriz):
    sku = int(input("Ingrese el SKU a eliminar: "))
    for i, item in enumerate(matriz):
        if item[0] == sku:
            matriz.pop(i)
            print("SKU eliminado correctamente.")
            return
    print("¡Error! SKU no encontrado…")


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
    seleccion = (int(input("Opción seleccionada: ")))
    match seleccion:
        case 0:
            print("""Opciones disponibles:
        1. Ingresar SKU
        2. Buscar SKU
        3. Buscar Producto
        4. Eliminar SKU
        5. Mostrar Inventario
        6. Salir
        7. Otros""")

        case 1:
            ingresar_sku(matriz)
            otro = int(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))
            while otro == 1:
                ingresar_sku(matriz)
                otro = int(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))
            while otro != 0 and otro != 1:
                print("¡Error! Opción no válida…")
                otro = int(input("¿Desea ingresar otro SKU? (0=NO, 1=SÍ): "))

        case 2:
            bandera = True
            buscar_sku(matriz, bandera)
            if bandera == False:
                seleccion1 = int(input("¿Desea ingresarlo? (0=NO, 1=SÍ): "))
                if seleccion1 == 1:
                    ingresar_sku(matriz)
            otro = int(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))
            while otro == 1:
                buscar_sku(matriz, bandera)
                if bandera == False:
                    seleccion1 = int(input("¿Desea ingresarlo? (0=NO, 1=SÍ): "))
                    if seleccion1 == 1:
                        ingresar_sku(matriz)
                otro = int(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))
            while otro != 0 and otro != 1:
                print("¡Error! Opción no válida…")
                otro = int(input("¿Desea buscar otro SKU? (0=NO, 1=SÍ): "))

        case 3:
            buscar_producto(matriz)
            otro = int(input("¿Desea buscar otro producto? (0=NO, 1=SÍ): "))
            while otro == 1:
                buscar_producto(matriz)
                otro = int(input("¿Desea buscar otro producto? (0=NO, 1=SÍ): "))
            while otro != 0 and otro != 1:
                print("¡Error! Opción no válida…")
                otro = int(input("¿Desea buscar otro producto? (0=NO, 1=SÍ): "))

        case 4:
            eliminar_sku(matriz)
            otro = int(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))
            while otro == 1:
                eliminar_sku(matriz)
                otro = int(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))
            while otro != 0 and otro != 1:
                print("¡Error! Opción no válida…")
                otro = int(input("¿Desea eliminar otro SKU? (0=NO, 1=SÍ): "))

        case 5:
            print("Inventario actual")
            print("[SKU, Nombre, Existencias]")
            for fila in matriz:
                print(fila)

        case 6:
            print("Gracias por usar GenzaloStorage. Saliendo del programa…")
            print("Inventario final ([SKU, Nombre, Existencias]):", matriz)
            break

        case 7:
            print("Versión de GenzaloStorage: 0.1 ALFA")

        case _:
            print("¡Error! Opción no válida…")
    

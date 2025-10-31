# funciones
import json

def normalizar(texto):
    return texto.strip().lower()

def similitud(texto1, texto2):
    texto1 = normalizar(texto1)
    texto2 = normalizar(texto2)
    if not texto1 or not texto2:
        return 0
    for i in range(min(len(texto1), len(texto2)), 0, -1):
        if texto1[:i] == texto2[:i]:
            return i / max(len(texto1), len(texto2))
    return 0

def buscar (matriz):
    
    seleccion = normalizar(input("""Buscar por:
        1. SKU
        2. Producto
        3. Cantidad
        4. Precio
        5. Categoría
    Seleccione una opción: """))
    
    match seleccion:
        case "1"|"uno"|"buscar sku": 
            sku = int(input("Ingrese el SKU a buscar: "))
            #busqueda exacta
            for item in matriz:
                if item[0] == sku:
                    print(f"El SKU Nº {sku} corresponde al producto «{item[1]}» , tiene {item[2]} existencia(s) y un precio de ${item[3]:.2f}.")
                    return True
                    
            #Si no se encuentra, busqueda aproximada
            sugerencias = sorted(matriz, key=lambda x: abs(x[0] - sku))[:3]
            if sugerencias:
                print("SKU no encontrado. ¿Quizás quiso decir uno de estos?:")
                for item in sugerencias:
                    print(f" → SKU {item[0]}: {item[1]} ({item[2]} existencia(s), precio de ${item[3]:.2f})")
            else:
                print("¡Error! SKU no encontrado…")
            return False
                   
        case "2"|"dos"|"buscar producto":
            consulta = input("Ingrese el nombre del producto a buscar: ")
            consulta_norm = normalizar(consulta)
            # coincidencia exacta primero
            for item in matriz:
                if normalizar(item[1]) == consulta_norm:
                    print(f"El producto «{item[1]}» tiene SKU Nº {item[0]} , {item[2]} existencia (s) y un precio de ${item[3]:.2f}.")
                    return True
                
            # si no se encuentra, buscar coincidencias similares
            resultados = []
            for item in matriz:
                sim = similitud(consulta_norm, item[1])
                if sim >= 0.4 or consulta_norm in normalizar(item[1]):
                    resultados.append((sim, item))
            if resultados:
                print("Producto no encontrado exacto. ¿Quizás quiso decir?:")
                for sim, item in sorted(resultados, reverse=True):
                    print(f" → {item[1]} (SKU {item[0]}, {item[2]} existencia(s))precio de ${item[3]}")
                return False
            else:
                print("¡Error! Producto no encontrado y sin coincidencias similares.")
                return False
            
        case "3"|"tres"|"buscar cantidad":
            # Buscar por cantidad: igual / mayor / menor / rango
            modo = normalizar(input("Buscar por cantidad: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            try:
                if modo in ("igual", "1", "iguales"):
                    q = int(input("Ingrese la cantidad exacta: "))
                    encontrados = [item for item in matriz if item[2] == q]
                elif modo in ("mayor", "2"):
                    q = int(input("Mostrar productos con cantidad > : "))
                    encontrados = [item for item in matriz if item[2] > q]
                elif modo in ("menor", "3"):
                    q = int(input("Mostrar productos con cantidad < : "))
                    encontrados = [item for item in matriz if item[2] < q]
                elif modo in ("rango", "4"):
                    lo = int(input("Ingrese el mínimo del rango: "))
                    hi = int(input("Ingrese el máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    encontrados = [item for item in matriz if lo <= item[2] <= hi]
                else:
                    print("¡Error! Opción no válida para cantidad.")
                    return False
            except ValueError:
                print("¡Error! Entrada inválida para cantidad.")
                return False
                
            if encontrados:
                print("Productos encontrados:")
                for item in encontrados:
                    print(f" → SKU {item[0]}: {item[1]} ({item[2]} existencia(s), precio de ${item[3]:.2f})")
                return True
            else:
                print("¡Error! No se encontraron productos con esa cantidad.")
                return False    
            
        case "4"|"cuatro"|"buscar precio":
        # Buscar por precio: exacto / mayor / menor / rango
            modo = normalizar(input("Buscar por precio: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            try:
                if modo in ("igual", "1", "exacto"):
                    p = float(input("Ingrese el precio exacto: "))
                    encontrados = [item for item in matriz if abs(item[3] - p) < 1e-9]
                elif modo in ("mayor", "2"):
                    p = float(input("Mostrar productos con precio > : "))
                    encontrados = [item for item in matriz if item[3] > p]
                elif modo in ("menor", "3"):
                    p = float(input("Mostrar productos con precio < : "))
                    encontrados = [item for item in matriz if item[3] < p]
                elif modo in ("rango", "4"):
                    lo = float(input("Ingrese el precio mínimo del rango: "))
                    hi = float(input("Ingrese el precio máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    encontrados = [item for item in matriz if lo <= item[3] <= hi]
                else:
                    print("¡Error! Opción no válida para precio.")
                    return False
            except ValueError:
                print("¡Error! Ingrese un número válido para el precio.")
                return False

            if encontrados:
                print("Resultados encontrados (SKU, Nombre, Existencias, Precio):")
                for it in encontrados:
                    print(f" → {it[0]} | {it[1]} | {it[2]} | ${it[3]:.2f}")
                return True
            else:
                print("No se encontraron productos con ese precio.")
                return False
            
        case "5"|"cinco"|"buscar categoría":
            categoria = normalizar(input("Ingrese la categoría a buscar: "))
            encontrados = [item for item in matriz if normalizar(item[4]) == categoria]
            if encontrados:
                print("Productos encontrados en la categoría:")
                for item in encontrados:
                    print(f" → SKU {item[0]}: {item[1]} ({item[2]} existencia(s), precio de ${item[3]:.2f})")
                return True
            else:
                print("""Error! No se encontraron productos en esa categoría
                      buscando en subcategorías relacionadas...""")
                encontrados = [item for item in matriz if normalizar(item[5]) == categoria]
                if encontrados:
                    print("Productos encontrados en la subcategoría:")
                    for item in encontrados:
                        print(f" → SKU {item[0]}: {item[1]} ({item[2]} existencia(s), precio de ${item[3]:.2f})")
                    return True
                else:
                    print("¡Error! No se encontraron productos en esa categoría o subcategoría.")
                    return False          

        case _:
            print("¡Error! Opción no válida…")


def ingresar(matriz):
    error = False
    #SKU único
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
                    
    #EXISTENCIAS validas
    existencias = int(input("Ingrese las existencias: "))
    while existencias <= 0:
        existencias = int(input("¡Error! Ingrese un numero válido…: "))
    producto = input("Ingrese el nombre del producto: ")
    
    #NOMBRE único
    for nombre in matriz:
        if nombre[1] == producto:
            error = True
            print("¡Error! El nombre ya esta en uso…")
            while error == True:
                error = False
                producto = input("Ingrese otro nombre: ")
                if nombre[1] == producto:
                    error = True
                    
    #PRECIO valido
    precio = float(input("Ingrese el precio del producto: "))
    while precio <= 0:
        precio = float(input("¡Error! Ingrese un numero válido…: "))
        
    #CATEGORIA y SUBCATEGORIA únicos  
    op = input("¿Desea agregar categoría? (sí=1/no=0): ")
    if normalizar(op) in ["sí", "si", "s", "1"]:
        categoria = input("Ingrese la categoría del producto: ")
        for cat in matriz:
            if cat[4] == categoria:
                error = True
                print("¡Error! La categoría ya existe…")
                while error == True:
                    error = False
                    categoria = input("Ingrese otra categoría: ")
                    if cat[4] == categoria:
                        error = True
        op2 = input("¿Desea agregar subcategoría? (sí=1/no=0): ")
        if normalizar(op2) in ["sí", "si", "s", "1"]:                
            subcategoria = input("Ingrese la subcategoría del producto: ")
            for subcat in matriz:
                if subcat[5] == subcategoria:
                    error = True
                    print("¡Error! La subcategoría ya existe…")
                    while error == True:
                        error = False
                        subcategoria = input("Ingrese otra subcategoría: ")
                        if subcat[5] == subcategoria:
                            error = True
        else:
            subcategoria = ""                   
    else:
        categoria = ""
        subcategoria = ""
        
    #se agrega el nuevo producto a la matriz
    matriz.append([sku, producto, existencias, precio, categoria, subcategoria])
    print("SKU y existencias ingresados correctamente.")
    return matriz



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
                
        case "4"|"cuatro"|"modificar precio":
            print ("buscar por sku o producto")
            mod_busqueda = normalizar(input("Ingrese su opción: "))
            if mod_busqueda in ["sku","1","uno"]:
                sku = int(input("Ingrese el SKU del producto cuyo precio desea modificar: ")) 
                for item in matriz:
                    if item[0] == sku:
                        nuevo_precio = float(input("Ingrese el nuevo precio: "))
                        item[3] = nuevo_precio
                        print("Precio modificado correctamente.")
                        return
                    
            elif mod_busqueda in ["producto","2","dos"]:
                producto = input("Ingrese el nombre del producto cuyo precio desea modificar: ")
                for item in matriz:
                    if item[1] == producto:
                        nuevo_precio = float(input("Ingrese el nuevo precio: "))
                        item[3] = nuevo_precio
                        print("Precio modificado correctamente.")
                        return
                    
        case _:
            print("¡Error! Opción no válida…")

def eliminar(matriz):
    seleccion2 = normalizar(input("Eliminar por SKU (1), Eliminar Producto (2) , Eliminar Todo (3): "))
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
        case"3"|"tres"|"eliminar todo":
            confirmacion = normalizar(input("¿Está seguro que desea eliminar todos los productos? (sí=1/no=0): "))
            if confirmacion in ["sí", "si", "s", "1"]:
                matriz.clear()
                print("Todos los productos han sido eliminados.")
            else:
                print("Operación cancelada.")
        case _:
            print("¡Error! Opción no válida…")
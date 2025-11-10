# funcion.py
import json
from datetime import datetime

def escribir_log(mensaje, nivel="INFO"):
    """Escribe un mensaje en el archivo de log"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('loginventario.txt', 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} - {nivel} - {mensaje}\n")
    except Exception as e:
        print(f"Error al escribir en log: {e}")
    

def cargar_memory():
    """Carga los datos desde memory.json, si no existe crea una estructura básica"""
    try:
        with open('memory.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        # Estructura inicial del JSON
        data = {
            "productos": [],
            "categorias": []
        }
        guardar_memory(data)
        escribir_log(f"Error al cargar memory.json: {e}", nivel="ERROR")
    except json.JSONDecodeError:
        data = {
            "productos": [],
            "categorias": []
        }
        guardar_memory(data)
        escribir_log("Error de decodificación JSON en memory.json. Se ha reiniciado el archivo.", nivel="ERROR")
    except FileNotFoundError:
        data = {
            "productos": [],
            "categorias": []
        }
        guardar_memory(data)
        escribir_log("memory.json no encontrado. Se ha creado un nuevo archivo.", nivel="WARNING")
    return data

def guardar_memory(data):
    """Guarda los datos en memory.json"""
    with open('memory.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

def buscar():
    data = cargar_memory()
    productos = data["productos"]
    encuentro = False
    seleccion = normalizar(input("Seleccione una opción:" ))
    
    match seleccion:
        case "1"|"uno"|"buscar sku":
            try:
                sku = int(input("Ingrese el SKU a buscar: "))
                # busqueda exacta
                for producto in productos:
                    if producto["sku"] == sku:
                        categorias_str = ", ".join(producto["categorias"]) if producto["categorias"] else "Sin categorías"
                        print(f"El SKU Nº {sku} corresponde al producto «{producto['nombre']}», tiene {producto['existencias']} existencia(s), un precio de ${producto['precio']:.2f} y categorías: «{categorias_str}».")
                        encuentro = True
                if encuentro == False:            
                    # Si no se encuentra, busqueda aproximada
                    sugerencias = sorted(productos, key=lambda x: abs(x["sku"] - sku))[:3]
                    if sugerencias:
                        print("SKU no encontrado. ¿Quizá buscaba alguno de los siguientes?:")
                        for prod in sugerencias:
                            categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías."
                            print(f" → SKU Nº {prod['sku']}: «{prod['nombre']}», ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: «{categorias_str}»)")
                    else:
                        print("¡Error! SKU no encontrado…")
                return False
            except ValueError:
                escribir_log("Error al ingresar SKU en búsqueda.", nivel="ERROR")
                print("¡Error! Ingrese un SKU válido.")
                return False
                   
        case "2"|"dos"|"buscar producto":
            consulta = input("Ingrese el nombre del producto a buscar: ")
            consulta_norm = normalizar(consulta)
            # coincidencia exacta primero
            for producto in productos:
                if normalizar(producto["nombre"]) == consulta_norm:
                    categorias_str = ", ".join(producto["categorias"]) if producto["categorias"] else "Sin categorías"
                    print(f"El producto «{producto['nombre']}» tiene SKU Nº {producto['sku']}, {producto['existencias']} existencia(s), precio de ${producto['precio']:.2f} y categorías: «{categorias_str}».")
                    encuentro = True

            if encuentro == False: 
                # si no se encuentra, buscar coincidencias similares
                resultados = []
                for producto in productos:
                    sim = similitud(consulta_norm, producto["nombre"])
                    if sim >= 0.4 or consulta_norm in normalizar(producto["nombre"]):
                        resultados.append((sim, producto))
                if resultados:
                    print("Producto exacto no encontrado. ¿Quizá quiso decir?:")
                    for sim, prod in sorted(resultados, reverse=True):
                        categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                        print(f" → «{prod['nombre']}», (SKU Nº {prod['sku']}, {prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: «{categorias_str}»)")
                else:
                    print("¡Error! Producto no encontrado y sin coincidencias similares.")
            
        case "3"|"tres"|"buscar cantidad":
            # Buscar por cantidad: igual / mayor / menor / rango
            modo = normalizar(input("Buscar por cantidad: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            try:
                if modo in ("igual", "1", "iguales"):
                    q = int(input("Ingrese la cantidad exacta: "))
                    encontrados = [prod for prod in productos if prod["existencias"] == q]
                elif modo in ("mayor", "2"):
                    q = int(input("Mostrar productos con cantidad >: "))
                    encontrados = [prod for prod in productos if prod["existencias"] > q]
                elif modo in ("menor", "3"):
                    q = int(input("Mostrar productos con cantidad <: "))
                    encontrados = [prod for prod in productos if prod["existencias"] < q]
                elif modo in ("rango", "4"):
                    lo = int(input("Ingrese el mínimo del rango: "))
                    hi = int(input("Ingrese el máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    encontrados = [prod for prod in productos if lo <= prod["existencias"] <= hi]
                else:
                    print("¡Error! Opción no válida para cantidad.")
                    return False
            except ValueError:
                escribir_log("Error al ingresar cantidad en búsqueda.", nivel="ERROR")
                print("¡Error! Entrada inválida para cantidad.")
                return False
                
            if encontrados:
                print("Productos encontrados:")
                for prod in encontrados:
                    categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(f" → SKU Nº {prod['sku']}: «{prod['nombre']}», ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
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
                    encontrados = [prod for prod in productos if abs(prod["precio"] - p) < 1e-9]
                elif modo in ("mayor", "2"):
                    p = float(input("Mostrar productos con precio > : "))
                    encontrados = [prod for prod in productos if prod["precio"] > p]
                elif modo in ("menor", "3"):
                    p = float(input("Mostrar productos con precio < : "))
                    encontrados = [prod for prod in productos if prod["precio"] < p]
                elif modo in ("rango", "4"):
                    lo = float(input("Ingrese el precio mínimo del rango: "))
                    hi = float(input("Ingrese el precio máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    encontrados = [prod for prod in productos if lo <= prod["precio"] <= hi]
                else:
                    print("¡Error! Opción no válida para precio.")
                    return False
            except ValueError:
                escribir_log("Error al ingresar precio en búsqueda.", nivel="ERROR")
                print("¡Error! Ingrese un número válido para el precio.")
                return False

            if encontrados:
                print("Resultados encontrados:")
                for prod in encontrados:
                    categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(f" → SKU {prod['sku']}: {prod['nombre']} ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
                return True
            else:
                print("No se encontraron productos con ese precio.")
                return False
            
        case "5"|"cinco"|"buscar categoría":
            categoria_buscar = normalizar(input("Ingrese la categoría a buscar: "))
            encontrados = []
            for producto in productos:
                if any(normalizar(cat) == categoria_buscar for cat in producto["categorias"]):
                    encontrados.append(producto)
            
            if encontrados:
                print(f"Productos encontrados en la categoría '{categoria_buscar}':")
                for prod in encontrados:
                    categorias_str = ", ".join(prod["categorias"])
                    print(f" → SKU {prod['sku']}: {prod['nombre']} ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
                return True
            else:
                print(f"¡Error! No se encontraron productos en la categoría '{categoria_buscar}'.")          

        case "6"|"seis"|"volver al menu principal":
            return False

        case _:
            print("¡Error! Opción no válida…")
    return False

def ingresar():
    data = cargar_memory()
    productos = data["productos"]
    
    try:
        # SKU único
        sku = int(input("Ingrese el SKU: "))
        for producto in productos:
            if producto["sku"] == sku:
                print("¡Error! El SKU ya existe…")
                return False
                    
        # EXISTENCIAS validas
        existencias = int(input("Ingrese las existencias: "))
        while existencias <= 0:
            existencias = int(input("¡Error! Ingrese un numero válido…: "))
        
        # NOMBRE del producto
        nombre = input("Ingrese el nombre del producto: ")
        
        # Verificar nombre único
        for producto in productos:
            if normalizar(producto["nombre"]) == normalizar(nombre):
                print("¡Error! El nombre ya está en uso…")
                return False
        
        # PRECIO válido
        precio = float(input("Ingrese el precio del producto: "))
        while precio <= 0:
            precio = float(input("¡Error! Ingrese un numero válido…: "))
        
        # CATEGORÍAS (múltiples tags)
        print("Ingrese las categorías del producto (separadas por comas, o Enter para omitir): ")
        categorias_input = input().strip()
        
        if categorias_input:
            # Eliminar espacios, dividir por comas, y quitar elementos vacíos
            categorias = [cat.strip() for cat in categorias_input.split(",") if cat.strip()]
            # ELIMINAR DUPLICADOS y ORDENAR ALFABÉTICAMENTE
            # Usar set() para eliminar duplicados y luego sorted() para ordenar
            categorias = sorted(set(categorias))
            
            print(f"Categorías procesadas: {', '.join(categorias)}")
        else:
            categorias = []
            
        # Crear nuevo producto
        nuevo_producto = {
            "sku": sku,
            "nombre": nombre,
            "existencias": existencias,
            "precio": precio,
            "categorias": categorias
        }
        
        # Agregar a la lista de productos
        productos.append(nuevo_producto)
        
        # Actualizar lista global de categorías
        for categoria in categorias:
            if categoria not in data["categorias"]:
                data["categorias"].append(categoria)
        
        # Guardar en el archivo
        guardar_memory(data)
        print("Producto ingresado correctamente.")
        return True
        
    except ValueError:
        print("¡Error! Ingrese valores numéricos válidos para SKU, existencias y precio.")
        escribir_log("Error al ingresar valores numéricos en ingreso de producto.", nivel="ERROR")
        return False

def modificar():
    data = cargar_memory()
    productos = data["productos"]
    
    seleccion2 = normalizar(input("Modificar SKU (1) o Producto (2) o Existencias (3) o Precio (4) o Categorías (5): "))
    match seleccion2:
        
        case "1"|"uno"|"modificar sku":
            try:
                sku_actual = int(input("Ingrese el SKU a modificar: "))
                for producto in productos:
                    if producto["sku"] == sku_actual:
                        nuevo_sku = int(input("Ingrese el nuevo SKU: "))
                        # Verificar que el nuevo SKU no exista
                        for prod in productos:
                            if prod["sku"] == nuevo_sku and prod != producto:
                                print("¡Error! El nuevo SKU ya existe…")
                                return False
                        producto["sku"] = nuevo_sku
                        guardar_memory(data)
                        print("SKU modificado correctamente.")
                        return True
                print("¡Error! SKU no encontrado…")
                return False
            except ValueError:
                escribir_log("Error al ingresar SKU en modificación.", nivel="ERROR")
                print("¡Error! Ingrese un SKU válido.")
                return False
                
        case "2"|"dos"|"modificar producto":
            nombre_actual = input("Ingrese el nombre del producto a modificar: ")
            for producto in productos:
                if normalizar(producto["nombre"]) == normalizar(nombre_actual):
                    nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
                    # Verificar que el nuevo nombre no exista
                    for prod in productos:
                        if normalizar(prod["nombre"]) == normalizar(nuevo_nombre) and prod != producto:
                            print("¡Error! El nuevo nombre ya existe…")
                            return False
                    producto["nombre"] = nuevo_nombre
                    guardar_memory(data)
                    print("Producto modificado correctamente.")
                    return True
            print("¡Error! Producto no encontrado…")
            return False
                
        case "3"|"tres"|"modificar existencias":
            try:
                sku = int(input("Ingrese el SKU del producto cuyas existencias desea modificar: ")) 
                for producto in productos:
                    if producto["sku"] == sku:
                        nuevas_existencias = int(input("Ingrese las nuevas existencias: "))
                        if nuevas_existencias <= 0:
                            print("¡Error! Las existencias deben ser mayores a 0.")
                            return False
                        producto["existencias"] = nuevas_existencias
                        guardar_memory(data)
                        print("Existencias modificadas correctamente.")
                        return True
                print("¡Error! SKU no encontrado…")
                return False
            except ValueError:
                escribir_log("Error al ingresar SKU en modificación de existencias.", nivel="ERROR")
                print("¡Error! Ingrese valores numéricos válidos.")
                return False
                
        case "4"|"cuatro"|"modificar precio":
            try:
                mod_busqueda = normalizar(input("Buscar por SKU (1) o Producto (2): "))
                if mod_busqueda in ["sku","1","uno"]:
                    sku = int(input("Ingrese el SKU del producto cuyo precio desea modificar: ")) 
                    for producto in productos:
                        if producto["sku"] == sku:
                            nuevo_precio = float(input("Ingrese el nuevo precio: "))
                            if nuevo_precio <= 0:
                                print("¡Error! El precio debe ser mayor a 0.")
                                return False
                            producto["precio"] = nuevo_precio
                            guardar_memory(data)
                            print("Precio modificado correctamente.")
                            return True
                    print("¡Error! SKU no encontrado…")
                    return False
                    
                elif mod_busqueda in ["producto","2","dos"]:
                    nombre = input("Ingrese el nombre del producto cuyo precio desea modificar: ")
                    for producto in productos:
                        if normalizar(producto["nombre"]) == normalizar(nombre):
                            nuevo_precio = float(input("Ingrese el nuevo precio: "))
                            if nuevo_precio <= 0:
                                print("¡Error! El precio debe ser mayor a 0.")
                                return False
                            producto["precio"] = nuevo_precio
                            guardar_memory(data)
                            print("Precio modificado correctamente.")
                            return True
                    print("¡Error! Producto no encontrado…")
                    return False
                else:
                    print("¡Error! Opción no válida…")
                    return False
                    
            except ValueError:
                print("¡Error! Ingrese valores numéricos válidos.")
                escribir_log("Error al ingresar valores numéricos en modificación de precio.", nivel="ERROR")
                return False
        
        case "5"|"cinco"|"modificar categorías":
            try:
                sku = int(input("Ingrese el SKU del producto cuyas categorías desea modificar: ")) 
                for producto in productos:
                    if producto["sku"] == sku:
                        print(f"Categorías actuales: {', '.join(producto['categorias']) if producto['categorias'] else 'Ninguna'}")
                        print("Ingrese las nuevas categorías (separadas por comas, o Enter para eliminar todas): ")
                        categorias_input = input().strip()
                        nuevas_categorias = [cat.strip() for cat in categorias_input.split(",") if cat.strip()] if categorias_input else []
                        
                        producto["categorias"] = nuevas_categorias
                        
                        # Actualizar lista global de categorías
                        data["categorias"] = []
                        for prod in productos:
                            for cat in prod["categorias"]:
                                if cat not in data["categorias"]:
                                    data["categorias"].append(cat)
                        
                        guardar_memory(data)
                        print("Categorías modificadas correctamente.")
                        return True
                print("¡Error! SKU no encontrado…")
                return False
            except ValueError:
                print("¡Error! Ingrese un SKU válido.")
                escribir_log("Error al ingresar SKU en modificación de categorías.", nivel="ERROR")
                return False
                
        case _:
            print("¡Error! Opción no válida…")
            return False

def eliminar():
    data = cargar_memory()
    productos = data["productos"]
    
    seleccion2 = normalizar(input("Eliminar por SKU (1), Eliminar Producto (2), Eliminar Todo (3): "))
    match seleccion2:
        case "1"|"uno"|"sku":
            try:
                sku = int(input("Ingrese el SKU a eliminar: "))
                for i, producto in enumerate(productos):
                    if producto["sku"] == sku:
                        productos.pop(i)
                        # Actualizar lista global de categorías
                        data["categorias"] = []
                        for prod in productos:
                            for cat in prod["categorias"]:
                                if cat not in data["categorias"]:
                                    data["categorias"].append(cat)
                        guardar_memory(data)
                        print("Producto eliminado correctamente.")
                        return True
                print("¡Error! SKU no encontrado…")
                return False
            except ValueError:
                escribir_log("Error al ingresar SKU en eliminación.", nivel="ERROR")
                print("¡Error! Ingrese un SKU válido.")
                return False
                
        case "2"|"dos"|"eliminar producto":
            nombre = normalizar(input("Ingrese el nombre del producto a eliminar: "))
            for i, producto in enumerate(productos):
                if normalizar(producto["nombre"]) == nombre:
                    productos.pop(i)
                    # Actualizar lista global de categorías
                    data["categorias"] = []
                    for prod in productos:
                        for cat in prod["categorias"]:
                            if cat not in data["categorias"]:
                                data["categorias"].append(cat)
                    guardar_memory(data)
                    print("Producto eliminado correctamente.")
                    return True
            print("¡Error! Producto no encontrado…")
            return False
            
        case "3"|"tres"|"eliminar todo":
            confirmacion = normalizar(input("¿Está seguro que desea eliminar todos los productos? (Sí=1/No=0): "))
            if confirmacion in ["sí", "si", "s", "1"]:
                data["productos"] = []
                data["categorias"] = []
                guardar_memory(data)
                print("Todos los productos han sido eliminados.")
                return True
            else:
                print("Operación cancelada.")
                return False
                
        case _:
            print("¡Error! Opción no válida…")
            return False

def gestionar_categoria():
    data = cargar_memory()
    
    seleccion = normalizar(input("""Gestionar categorías:
        1. Ver todas las categorías
        2. Ingresar categoría
        3. Eliminar categoría  
        4. Modificar categoría
    Seleccione una opción: """))
    
    match seleccion:
        case "1"|"uno"|"ver categorías":
            if data["categorias"]:
                print("Categorías disponibles:")
                for i, cat in enumerate(data["categorias"], 1):
                    print(f"  {i}. {cat}")
            else:
                print("No hay categorías registradas.")
            return True
            
        case "2"|"dos"|"ingresar categoría":
            nueva_categoria = input("Ingrese la nueva categoría: ")
            if nueva_categoria in data["categorias"]:
                print("¡Error! La categoría ya existe…")
                return False
            data["categorias"].append(nueva_categoria)
            guardar_memory(data)
            print("Categoría ingresada correctamente.")
            return True
            
        case "3"|"tres"|"eliminar categoría":
            if not data["categorias"]:
                print("No hay categorías para eliminar.")
                return False
                
            print("Categorías disponibles:")
            for i, cat in enumerate(data["categorias"], 1):
                print(f"  {i}. {cat}")
                
            categoria_eliminar = input("Ingrese la categoría a eliminar: ")
            if categoria_eliminar in data["categorias"]:
                data["categorias"].remove(categoria_eliminar)
                # Actualizar productos que tenían esta categoría
                for producto in data["productos"]:
                    if categoria_eliminar in producto["categorias"]:
                        producto["categorias"].remove(categoria_eliminar)
                guardar_memory(data)
                print("Categoría eliminada correctamente.")
                return True
            else:
                print("¡Error! Categoría no encontrada…")
                return False
                
        case "4"|"cuatro"|"modificar categoría":
            if not data["categorias"]:
                print("No hay categorías para modificar.")
                return False
                
            print("Categorías disponibles:")
            for i, cat in enumerate(data["categorias"], 1):
                print(f"  {i}. {cat}")
                
            categoria_actual = input("Ingrese la categoría a modificar: ")
            if categoria_actual in data["categorias"]:
                nueva_categoria = input("Ingrese la nueva categoría: ")
                # Actualizar en la lista de categorías
                data["categorias"].remove(categoria_actual)
                data["categorias"].append(nueva_categoria)
                # Actualizar en los productos
                for producto in data["productos"]:
                    if categoria_actual in producto["categorias"]:
                        index = producto["categorias"].index(categoria_actual)
                        producto["categorias"][index] = nueva_categoria
                guardar_memory(data)
                print("Categoría modificada correctamente.")
                return True
            else:
                print("¡Error! Categoría no encontrada.")
                return False
                
        case _:
            print("¡Error! Opción no válida…")
            return False
        
def gestionar_categoria_modo(modo=None):
    """Versión modificada para trabajar con menús específicos"""
    data = cargar_memory()
    
    if modo == "ver":
        if data["categorias"]:
            print("Categorías disponibles:")
            for i, cat in enumerate(data["categorias"], 1):
                print(f"  {i}. {cat}")
            return True
        else:
            print("No hay categorías registradas.")
            return False
    
    elif modo == "agregar":
        nueva_categoria = input("Ingrese la nueva categoría: ")
        if nueva_categoria in data["categorias"]:
            print("¡Error! La categoría ya existe…")
            return False
        data["categorias"].append(nueva_categoria)
        guardar_memory(data)
        print("Categoría ingresada correctamente.")
        return True
        
    elif modo == "eliminar":
        if not data["categorias"]:
            print("No hay categorías para eliminar.")
            return False
            
        print("Categorías disponibles:")
        for i, cat in enumerate(data["categorias"], 1):
            print(f"  {i}. {cat}")
            
        categoria_eliminar = input("Ingrese la categoría a eliminar: ")
        if categoria_eliminar in data["categorias"]:
            data["categorias"].remove(categoria_eliminar)
            # Actualizar productos que tenían esta categoría
            for producto in data["productos"]:
                if categoria_eliminar in producto["categorias"]:
                    producto["categorias"].remove(categoria_eliminar)
            guardar_memory(data)
            print("Categoría eliminada correctamente.")
            return True
        else:
            print("¡Error! Categoría no encontrada.")
            return False
            
    elif modo == "modificar":
        if not data["categorias"]:
            print("No hay categorías para modificar.")
            return False
            
        print("Categorías disponibles:")
        for i, cat in enumerate(data["categorias"], 1):
            print(f"  {i}. {cat}")
            
        categoria_actual = input("Ingrese la categoría a modificar: ")
        if categoria_actual in data["categorias"]:
            nueva_categoria = input("Ingrese la nueva categoría: ")
            # Actualizar en la lista de categorías
            data["categorias"].remove(categoria_actual)
            data["categorias"].append(nueva_categoria)
            # Actualizar en los productos
            for producto in data["productos"]:
                if categoria_actual in producto["categorias"]:
                    index = producto["categorias"].index(categoria_actual)
                    producto["categorias"][index] = nueva_categoria
            guardar_memory(data)
            print("Categoría modificada correctamente.")
            return True
        else:
            print("¡Error! Categoría no encontrada.")
            return False
    
    else:
        # Modo original por compatibilidad
        seleccion = normalizar(input("""Gestionar categorías:
        1. Ver todas las categorías
        2. Ingresar categoría
        3. Eliminar categoría  
        4. Modificar categoría
        5. Volver
    Seleccione una opción: """))
        
        match seleccion:
            case "1"|"uno"|"ver categorías":
                if data["categorias"]:
                    print("Categorías disponibles:")
                    for i, cat in enumerate(data["categorias"], 1):
                        print(f"  {i}. {cat}")
                else:
                    print("No hay categorías registradas.")
                return True
                
            case "2"|"dos"|"ingresar categoría":
                nueva_categoria = input("Ingrese la nueva categoría: ")
                if nueva_categoria in data["categorias"]:
                    print("¡Error! La categoría ya existe…")
                    return False
                data["categorias"].append(nueva_categoria)
                guardar_memory(data)
                print("Categoría ingresada correctamente.")
                return True
                
            case "3"|"tres"|"eliminar categoría":
                if not data["categorias"]:
                    print("No hay categorías para eliminar.")
                    return False
                    
                print("Categorías disponibles:")
                for i, cat in enumerate(data["categorias"], 1):
                    print(f"  {i}. {cat}")
                    
                categoria_eliminar = input("Ingrese la categoría a eliminar: ")
                if categoria_eliminar in data["categorias"]:
                    data["categorias"].remove(categoria_eliminar)
                    # Actualizar productos que tenían esta categoría
                    for producto in data["productos"]:
                        if categoria_eliminar in producto["categorias"]:
                            producto["categorias"].remove(categoria_eliminar)
                    guardar_memory(data)
                    print("Categoría eliminada correctamente.")
                    return True
                else:
                    print("¡Error! Categoría no encontrada…")
                    return False
                    
            case "4"|"cuatro"|"modificar categoría":
                if not data["categorias"]:
                    print("No hay categorías para modificar.")
                    return False
                    
                print("Categorías disponibles:")
                for i, cat in enumerate(data["categorias"], 1):
                    print(f"  {i}. {cat}")
                    
                categoria_actual = input("Ingrese la categoría a modificar: ")
                if categoria_actual in data["categorias"]:
                    nueva_categoria = input("Ingrese la nueva categoría: ")
                    # Actualizar en la lista de categorías
                    data["categorias"].remove(categoria_actual)
                    data["categorias"].append(nueva_categoria)
                    # Actualizar en los productos
                    for producto in data["productos"]:
                        if categoria_actual in producto["categorias"]:
                            index = producto["categorias"].index(categoria_actual)
                            producto["categorias"][index] = nueva_categoria
                    guardar_memory(data)
                    print("Categoría modificada correctamente.")
                    return True
                else:
                    print("¡Error! Categoría no encontrada…")
                    return False
                    
            case "5"|"cinco"|"volver":
                return False
                
            case _:
                print("¡Error! Opción no válida…")

                return False

# funcion.py 
import json
from datetime import datetime

# =============================================================================
# FUNCIONES DE LOG Y MANEJO DE ARCHIVOS
# =============================================================================

def escribir_log(mensaje, nivel="INFO"):
    # Escribe un mensaje en el archivo de log para registro de actividades
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('loginventario.txt', 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} - {nivel} - {mensaje}\n")
    except Exception as e:
        print(f"Error al escribir en log: {e}")
    
def cargar_memory():
    # Carga los datos desde memory.json
    # Si no existe o hay errores, crea una estructura básica
    try:
        with open('memory.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Validar estructura básica del JSON cargado
            if not isinstance(data, dict):
                raise ValueError("Estructura JSON inválida")
            if "productos" not in data:
                data["productos"] = []
            if "categorias" not in data:
                data["categorias"] = []
            if "clientes" not in data:
                data["clientes"] = []
            if "proveedores" not in data:
                data["proveedores"] = []
                
            # Validar que productos sea una lista
            if not isinstance(data["productos"], list):
                data["productos"] = []
            if not isinstance(data["categorias"], list):
                data["categorias"] = []
            if not isinstance(data["clientes"], list):
                data["clientes"] = []
            if not isinstance(data["proveedores"], list):
                data["proveedores"] = []
                
            return data
        
    except FileNotFoundError:
        # Si no existe el archivo, crear uno nuevo con estructura básica
        data = {
            "productos": [], 
            "categorias": [], 
            "clientes": [], 
            "proveedores": []
        }
        guardar_memory(data)
        escribir_log("memory.json no encontrado. Se ha creado un nuevo archivo.", nivel="WARNING")
        return data
    
    except json.JSONDecodeError as e:
        # Si hay un error de decodificación, reiniciar el archivo
        data = {
            "productos": [], 
            "categorias": [], 
            "clientes": [], 
            "proveedores": []
        }
        guardar_memory(data)
        escribir_log(f"Error de decodificación JSON en memory.json: {e}. Se ha reiniciado el archivo.", nivel="ERROR")
        return data
    
    except ValueError as e:
        # Si la estructura es inválida, reiniciar el archivo
        data = {
            "productos": [], 
            "categorias": [], 
            "clientes": [], 
            "proveedores": []
        }
        guardar_memory(data)
        escribir_log(f"Estructura inválida en memory.json: {e}. Se ha reiniciado el archivo.", nivel="ERROR")
        return data
    
    except PermissionError:
        escribir_log("Error de permiso al acceder a memory.json.", nivel="ERROR")
        return {
            "productos": [], 
            "categorias": [], 
            "clientes": [], 
            "proveedores": []
        }
    
    except Exception as e:
        escribir_log(f"Error inesperado al cargar memory.json: {e}", nivel="ERROR")
        return {
            "productos": [], 
            "categorias": [], 
            "clientes": [], 
            "proveedores": []
        }

def guardar_memory(data):
    # Guarda los datos en memory.json
    try:
        with open('memory.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar datos: {e}")
        escribir_log(f"Error al guardar memory.json: {e}", nivel="ERROR")

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def normalizar(texto):
    # Normaliza texto para comparaciones (minúsculas, sin espacios extras)
    return texto.strip().lower()

def similitud(texto1, texto2):
    # Calcula similitud entre dos textos para búsquedas aproximadas
    texto1 = normalizar(texto1)
    texto2 = normalizar(texto2)
    if not texto1 or not texto2:
        return 0
    for i in range(min(len(texto1), len(texto2)), 0, -1):
        if texto1[:i] == texto2[:i]:
            return i / max(len(texto1), len(texto2))
    return 0

# =============================================================================
# FUNCIONES DE GESTIÓN DE PRODUCTOS (SKU)
# =============================================================================

def generador_de_sku():
    # Generador simple de SKU único basado en el conteo de productos existentes
    data = cargar_memory()
    productos = data["productos"]
    if productos:
        max_sku = max(producto["sku"] for producto in productos)
        return max_sku + 1
    else:
        return 1

def ingresar():
    # Función para agregar un nuevo producto al inventario
    data = cargar_memory()
    productos = data["productos"]

    try:
        # SKU único
        print("Ingrese el SKU: ingrese -1 para cancelar o 0 para generar automáticamente: ") 
        sku = int(input())
        if sku == 0:
            print("Generando SKU automáticamente...")
            sku = generador_de_sku()
            print(f"SKU asignado: {sku}")      
        for producto in productos:
            while producto["sku"] == sku and sku <= 0 and sku != -1:
                print("Error! El SKU ya existe o invalido...")
                sku = int(input("Ingrese el SKU: "))

        if sku == -1:
            return False

        # NOMBRE del producto
        nombre = input("Ingrese el nombre del producto: ")

        # Verificar nombre único
        for producto in productos:
            while normalizar(producto["nombre"]) == normalizar(nombre):
                print("Error! El nombre ya esta en uso...")
                nombre = input("Ingrese el nombre del producto: ")

        if nombre in ("-1","salir"):
            return False

        # EXISTENCIAS validas
        existencias = int(input("Ingrese las existencias: "))
        while existencias <= 0 and existencias != -1:
            existencias = int(input("Error! Ingrese un numero valido...: "))

        if existencias == -1:
            return False

        # PRECIO válido
        precio_compra = float(input("Ingrese el precio de COMPRA del producto: "))
        while precio_compra <= 0 and precio_compra != -1:
            precio_compra = float(input("Error! Ingrese un numero valido...: "))
        
        if precio_compra == -1:
            return False
            
        precio_venta = float(input("Ingrese el precio de VENTA del producto: "))
        while precio_venta <= 0 and precio_venta != -1:
            precio_venta = float(input("Error! Ingrese un numero valido...: "))
        
        if precio_venta == -1:
            return False

        # CATEGORÍAS (múltiples tags)
        print("Ingrese las categorías del producto (separadas por comas, o Enter para omitir): ")
        categorias_input = input()

        if categorias_input in ("-1","salir"):
            return False
        
        categorias_input = categorias_input.strip()

        if categorias_input:
            # Eliminar espacios, dividir por comas, y quitar elementos vacíos
            categorias = [cat.strip() for cat in categorias_input.split(",") if cat.strip()]
            # ELIMINAR DUPLICADOS y ORDENAR ALFABÉTICAMENTE
            categorias = sorted(set(categorias))
            
            print(f"Categorías procesadas: {', '.join(categorias)}")
        else:
            categorias = []
            
        # Crear nuevo producto
        nuevo_producto = {
            "sku": sku,
            "nombre": nombre,
            "existencias": existencias,
            "precio compra": precio_compra,
            "precio venta": precio_venta,
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
        escribir_log(f"Producto agregado: {nombre} (SKU: {sku})", nivel="INFO")
        return True
        
    except ValueError:
        print("Error! Ingrese valores numéricos válidos para SKU, existencias y precio.")
        escribir_log("Error al ingresar valores numéricos en ingreso de producto.", nivel="ERROR")
        return False

def eliminar():
    # Función para eliminar productos del inventario
    data = cargar_memory()
    productos = data["productos"]
    err = True
    
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
                        escribir_log(f"Producto eliminado: {producto['nombre']} (SKU: {sku})", nivel="INFO")
                        err = False
                if sku == -1:
                    return 
                if err:
                    print("Error! SKU no encontrado...")
                return 
            except ValueError:
                escribir_log("Error al ingresar SKU en eliminación.", nivel="ERROR")
                print("Error! Ingrese un SKU válido.")
                return False
                
        case "2"|"dos"|"producto":
            nombre = input("Ingrese el nombre del producto a eliminar: ")
            for i, producto in enumerate(productos):
                if normalizar(producto["nombre"]) == normalizar(nombre):
                    productos.pop(i)
                    # Actualizar lista global de categorías
                    data["categorias"] = []
                    for prod in productos:
                        for cat in prod["categorias"]:
                            if cat not in data["categorias"]:
                                data["categorias"].append(cat)
                    guardar_memory(data)
                    print("Producto eliminado correctamente.")
                    escribir_log(f"Producto eliminado: {nombre}", nivel="INFO")
                    err = False
            if nombre in ("-1","salir"):
                return False
            if err:
                print("Error! Producto no encontrado...")
            return False
            
        case "3"|"tres"|"eliminar todo":
            confirmacion = normalizar(input("Esta seguro que desea eliminar todos los productos? (Si=1/No=0): "))
            if confirmacion in ["si", "s", "1"]:
                data["productos"] = []
                data["categorias"] = []
                guardar_memory(data)
                print("Todos los productos han sido eliminados.")
                escribir_log("Todos los productos eliminados", nivel="INFO")
                return True
            else:
                print("Operación cancelada.")
                return False
                
        case _:
            print("Error! Opción no válida...")
            return False

def modificar():
    # Función para modificar productos existentes en el inventario
    data = cargar_memory()
    productos = data["productos"]
    err = True
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
                                err = True
                        if err == False:
                            producto["sku"] = nuevo_sku
                            guardar_memory(data)
                            print("SKU modificado correctamente.")
                            escribir_log(f"SKU modificado: {sku_actual} -> {nuevo_sku}", nivel="INFO")
                    elif sku_actual != -1:
                        print("Error! SKU no encontrado...")

                if sku_actual == -1:
                    return 
                return 
            except ValueError:
                escribir_log("Error al ingresar SKU en modificación.", nivel="ERROR")
                print("Error! Ingrese un SKU válido.")
                return 
                
        case "2"|"dos"|"modificar producto":
            nombre_actual = input("Ingrese el nombre del producto a modificar: ")
            for producto in productos:
                if normalizar(producto["nombre"]) == normalizar(nombre_actual) and nombre_actual not in ("-1", "salir"):
                    nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
                    # Verificar que el nuevo nombre no exista
                    for prod in productos:
                        if normalizar(prod["nombre"]) == normalizar(nuevo_nombre) and prod != producto:
                            print("Error! El nombre ya esta en uso...")
                            err = True 
                    if err == False and nuevo_nombre not in ("-1", "salir"):
                        producto["nombre"] = nuevo_nombre
                        guardar_memory(data)
                        print("Producto modificado correctamente.")
                        escribir_log(f"Producto modificado: {nombre_actual} -> {nuevo_nombre}", nivel="INFO")
                elif nombre_actual not in ("-1","salir"):
                    print("Error! Producto no encontrado...")
            if nombre_actual in ("-1","salir"):
                return
            return 
                
        case "3"|"tres"|"modificar existencias":
            try:
                sku = int(input("Ingrese el SKU del producto cuyas existencias desea modificar: ")) 
                for producto in productos:
                    if producto["sku"] == sku:
                        nuevas_existencias = int(input("Ingrese las nuevas existencias: "))
                        if nuevas_existencias <= 0 and nuevas_existencias != -1:
                            print("Error! Las existencias deben ser mayores a 0.")
                            err == True
                        if err == False and nuevas_existencias != -1:
                            producto["existencias"] = nuevas_existencias
                            guardar_memory(data)
                            print("Existencias modificadas correctamente.")
                            escribir_log(f"Existencias modificadas: SKU {sku} -> {nuevas_existencias}", nivel="INFO")
                    elif sku != -1:
                        print("Error! SKU no encontrado...")
                
                if sku == -1:  
                    return False
                return False

            except ValueError:
                escribir_log("Error al ingresar SKU en modificación de existencias.", nivel="ERROR")
                print("Error! Ingrese valores numéricos válidos.")
                return False
                
        case "4"|"cuatro"|"modificar precio":
            try:
                mod_busqueda = normalizar(input("Buscar por SKU (1) o Producto (2): "))
                tipo_precio = normalizar(input("Modificar precio de COMPRA (1) o VENTA (2): "))
                campo_precio = "precio compra" if tipo_precio in ("1", "compra", "precio compra") else "precio venta"
                
                if mod_busqueda in ["sku","1","uno"]:
                    sku = int(input("Ingrese el SKU del producto cuyo precio desea modificar: ")) 
                    for producto in productos:
                        if producto["sku"] == sku:
                            nuevo_precio = float(input(f"Ingrese el nuevo {campo_precio}: "))
                            if nuevo_precio <= 0:
                                print("Error! El precio debe ser mayor a 0.")
                                err = True
                            elif err == False:
                                producto[campo_precio] = nuevo_precio
                                guardar_memory(data)
                                print(f"{campo_precio.title()} modificado correctamente.")
                                escribir_log(f"Precio modificado: SKU {sku} {campo_precio} -> {nuevo_precio}", nivel="INFO")
                        elif sku != -1:
                            print("Error! SKU no encontrado...")
                    if sku == -1:  
                        return False
                    return False
                    
                elif mod_busqueda in ["producto","2","dos"]:
                    nombre = input("Ingrese el nombre del producto cuyo precio desea modificar: ")
                    for producto in productos:
                        if normalizar(producto["nombre"]) == normalizar(nombre):
                            nuevo_precio = float(input(f"Ingrese el nuevo {campo_precio}: "))
                            if nuevo_precio <= 0:
                                print("Error! El precio debe ser mayor a 0.")
                                err = True
                            elif err == False:
                                producto[campo_precio] = nuevo_precio
                                guardar_memory(data)
                                print(f"{campo_precio.title()} modificado correctamente.")
                                escribir_log(f"Precio modificado: {nombre} {campo_precio} -> {nuevo_precio}", nivel="INFO")
                        elif nombre not in ("-1","salir"):
                            print("Error! Producto no encontrado...")
                    if nombre in ("-1","salir"):
                        return False
                    return False
                else:
                    print("Error! Opción no válida...")
                    return False
                    
            except ValueError:
                print("Error! Ingrese valores numéricos válidos.")
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
                        escribir_log(f"Categorías modificadas: SKU {sku}", nivel="INFO")
                        err = False
                if sku == -1:  
                    return False
                if err: 
                    print("Error! SKU no encontrado...")
                return False
            except ValueError:
                print("Error! Ingrese un SKU válido.")
                escribir_log("Error al ingresar SKU en modificación de categorías.", nivel="ERROR")
                return False
                
        case _:
            print("Error! Opción no válida...")
            return False

# =============================================================================
# FUNCIONES DE GESTIÓN DE CATEGORÍAS
# =============================================================================

def gestionar_categoria_modo(modo=None):
    # Función unificada para gestión de categorías del inventario
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
            print("Error! La categoría ya existe...")
            return False
        data["categorias"].append(nueva_categoria)
        guardar_memory(data)
        print("Categoría ingresada correctamente.")
        escribir_log(f"Categoría agregada: {nueva_categoria}", nivel="INFO")
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
            escribir_log(f"Categoría eliminada: {categoria_eliminar}", nivel="INFO")
            return True
        else:
            print("Error! Categoría no encontrada.")
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
            escribir_log(f"Categoría modificada: {categoria_actual} -> {nueva_categoria}", nivel="INFO")
            return True
        else:
            print("Error! Categoría no encontrada.")
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
                return gestionar_categoria_modo("ver")
                
            case "2"|"dos"|"ingresar categoría":
                return gestionar_categoria_modo("agregar")
                
            case "3"|"tres"|"eliminar categoría":
                return gestionar_categoria_modo("eliminar")
                    
            case "4"|"cuatro"|"modificar categoría":
                return gestionar_categoria_modo("modificar")
                    
            case "5"|"cinco"|"volver":
                return False
                
            case _:
                print("Error! Opción no válida...")
                return False

# =============================================================================
# FUNCIONES DE BÚSQUEDA Y ANÁLISIS
# =============================================================================

def calcular_estadisticas_financieras(productos=None):
    
    # Calcula estadísticas financieras del inventario
    
    if productos is None:
        data = cargar_memory()
        productos = data["productos"]
    
    if not productos:
        return {
            "total_inversion": 0,
            "total_valor_venta": 0,
            "ganancia_neta_total": 0,
            "ganancia_porcentaje_total": 0,
            "productos_analizados": 0
        }
    
    total_inversion = 0
    total_valor_venta = 0
    total_ganancia_neta = 0
    
    for producto in productos:
        inversion_producto = producto["precio compra"] * producto["existencias"]
        valor_venta_producto = producto["precio venta"] * producto["existencias"]
        ganancia_neta_producto = valor_venta_producto - inversion_producto
        
        total_inversion += inversion_producto
        total_valor_venta += valor_venta_producto
        total_ganancia_neta += ganancia_neta_producto
    
    # Calcular porcentaje de ganancia total
    if total_inversion > 0:
        ganancia_porcentaje_total = (total_ganancia_neta / total_inversion) * 100
    else:
        ganancia_porcentaje_total = 0
    
    return {
        "total_inversion": total_inversion,
        "total_valor_venta": total_valor_venta,
        "ganancia_neta_total": total_ganancia_neta,
        "ganancia_porcentaje_total": ganancia_porcentaje_total,
        "productos_analizados": len(productos)
    }

def mostrar_estadisticas_financieras(estadisticas, titulo="INVENTARIO COMPLETO"):

    # Muestra las estadísticas financieras en formato legible

    print(f"\n{'='*60}")
    print(f"{titulo:^60}")
    print(f"{'='*60}")
    print(f" INVERSION TOTAL EN PRODUCTOS: ${estadisticas['total_inversion']:>10.2f}")
    print(f" VALOR TOTAL DE VENTA: ${estadisticas['total_valor_venta']:>10.2f}")
    print(f" GANANCIA NETA TOTAL: ${estadisticas['ganancia_neta_total']:>10.2f}")
    
    # Indicador para la ganancia porcentual
    ganancia_porcentaje = estadisticas['ganancia_porcentaje_total']
    if ganancia_porcentaje > 0:
        indicador_ganancia = "[POSITIVO]" 
    elif ganancia_porcentaje < 0:
        indicador_ganancia = "[PERDIDA]" 
    else:
        indicador_ganancia = "[NEUTRO]"
    
    print(f" GANANCIA PORCENTUAL: {ganancia_porcentaje:>10.2f}% {indicador_ganancia}")
    print(f" PRODUCTOS ANALIZADOS: {estadisticas['productos_analizados']:>10}")
    print(f"{'='*60}")

def analisis_financiero_completo():

    # Análisis financiero completo del inventario

    data = cargar_memory()
    productos = data["productos"]
    
    if not productos:
        print("No hay productos en el inventario para analizar.")
        return
    
    # Estadísticas generales
    stats_generales = calcular_estadisticas_financieras(productos)
    mostrar_estadisticas_financieras(stats_generales, "ANALISIS FINANCIERO GENERAL")
    
    # Análisis por categorías
    categorias = {}
    for producto in productos:
        if producto["categorias"]:
            for categoria in producto["categorias"]:
                if categoria not in categorias:
                    categorias[categoria] = []
                categorias[categoria].append(producto)
        else:
            if "Sin Categoría" not in categorias:
                categorias["Sin Categoría"] = []
            categorias["Sin Categoría"].append(producto)
    
    if len(categorias) > 1:
        print(f"\n{'='*70}")
        print("ANALISIS POR CATEGORIAS:")
        print(f"{'='*70}")
        
        for categoria, productos_cat in categorias.items():
            stats_cat = calcular_estadisticas_financieras(productos_cat)
            print(f"\nCATEGORIA: {categoria.upper()}")
            print(f"   Productos: {stats_cat['productos_analizados']}")
            print(f"   Inversion: ${stats_cat['total_inversion']:.2f}")
            print(f"   Valor venta: ${stats_cat['total_valor_venta']:.2f}")
            print(f"   Ganancia neta: ${stats_cat['ganancia_neta_total']:.2f}")
            print(f"   Margen: {stats_cat['ganancia_porcentaje_total']:.2f}%")
    
    # Top 5 productos más rentables
    productos_con_rentabilidad = []
    for producto in productos:
        ganancia_unitaria = producto["precio venta"] - producto["precio compra"]
        if producto["precio compra"] > 0:
            rentabilidad_porcentaje = (ganancia_unitaria / producto["precio compra"]) * 100
        else:
            rentabilidad_porcentaje = 0
        
        productos_con_rentabilidad.append({
            "producto": producto,
            "rentabilidad_porcentaje": rentabilidad_porcentaje,
            "ganancia_total": ganancia_unitaria * producto["existencias"]
        })
    
    # Ordenar por rentabilidad porcentual
    productos_rentables = sorted(productos_con_rentabilidad, 
                               key=lambda x: x["rentabilidad_porcentaje"], 
                               reverse=True)[:5]
    
    if productos_rentables:
        print(f"\n{'='*70}")
        print("TOP 5 PRODUCTOS MAS RENTABLES:")
        print(f"{'='*70}")
        for i, item in enumerate(productos_rentables, 1):
            prod = item["producto"]
            print(f"\n{i}. {prod['nombre']} (SKU: {prod['sku']})")
            print(f"   Rentabilidad: {item['rentabilidad_porcentaje']:.2f}%")
            print(f"   Precio compra: ${prod['precio compra']:.2f}")
            print(f"   Precio venta: ${prod['precio venta']:.2f}")
            print(f"   Ganancia unitaria: ${prod['precio venta'] - prod['precio compra']:.2f}")

def buscar():
    # Función principal de búsqueda en el inventario
    data = cargar_memory()
    productos = data["productos"]
    encuentro = False
    
    # Mostrar estadísticas generales al inicio de cada búsqueda
    if productos:
        stats = calcular_estadisticas_financieras(productos)
        print(f"""\nRESUMEN FINANCIERO ACTUAL:
        • Inversion total: ${stats['total_inversion']:.2f}
        • Valor en venta: ${stats['total_valor_venta']:.2f}
        • Ganancia potencial: ${stats['ganancia_neta_total']:.2f} ({stats['ganancia_porcentaje_total']:.2f}%)
        • Productos en stock: {stats['productos_analizados']}""")
    
    seleccion = normalizar(input("Seleccione una opción: "))
    
    match seleccion:
        case "1"|"uno"|"buscar sku":
            try:
                sku = int(input("Ingrese el SKU a buscar: "))
                # busqueda exacta
                for producto in productos:
                    if producto["sku"] == sku:
                        categorias_str = ", ".join(producto["categorias"]) if producto["categorias"] else "Sin categorías"
                        ganancia_unitaria = producto["precio venta"] - producto["precio compra"]
                        ganancia_total = ganancia_unitaria * producto["existencias"]
                        margen_ganancia = (ganancia_unitaria / producto["precio compra"]) * 100 if producto["precio compra"] > 0 else 0
                        
                        print(f"\n PRODUCTO ENCONTRADO:\n   SKU N {sku}: «{producto['nombre']}»\n   Existencias: {producto['existencias']} unidad(es)\n   Precio compra: ${producto['precio compra']:.2f}\n   Precio venta: ${producto['precio venta']:.2f}\n   Categorías: «{categorias_str}»\n\n ANALISIS FINANCIERO:\n   • Inversion en stock: ${producto['precio compra'] * producto['existencias']:.2f}\n   • Valor venta stock: ${producto['precio venta'] * producto['existencias']:.2f}\n   • Ganancia unitaria: ${ganancia_unitaria:.2f}\n   • Ganancia total: ${ganancia_total:.2f}\n   • Margen de ganancia: {margen_ganancia:.2f}%")
                        encuentro = True
                        
                if not encuentro:            
                    # Si no se encuentra, busqueda aproximada
                    sugerencias = sorted(productos, key=lambda x: abs(x["sku"] - sku))[:3]
                    if sugerencias:
                        print("SKU no encontrado. Quizá buscaba alguno de los siguientes?:")
                        for prod in sugerencias:
                            categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías."
                            ganancia_unitaria = prod["precio venta"] - prod["precio compra"]
                            print(f" → SKU N {prod['sku']}: «{prod['nombre']}», ({prod['existencias']} existencia(s), Compra: ${prod['precio compra']:.2f}, Venta: ${prod['precio venta']:.2f}, Ganancia: ${ganancia_unitaria:.2f}, categorías: «{categorias_str}»)")
                    else:
                        print("Error! SKU no encontrado...")
                return False
            except ValueError:
                escribir_log("Error al ingresar SKU en búsqueda.", nivel="ERROR")
                print("Error! Ingrese un SKU válido.")
                return False
                   
        case "2"|"dos"|"buscar producto":
            consulta = input("Ingrese el nombre del producto a buscar: ")
            consulta_norm = normalizar(consulta)
            # coincidencia exacta primero
            for producto in productos:
                if normalizar(producto["nombre"]) == consulta_norm:
                    categorias_str = ", ".join(producto["categorias"]) if producto["categorias"] else "Sin categorías"
                    ganancia_unitaria = producto["precio venta"] - producto["precio compra"]
                    ganancia_total = ganancia_unitaria * producto["existencias"]
                    margen_ganancia = (ganancia_unitaria / producto["precio compra"]) * 100 if producto["precio compra"] > 0 else 0
                    
                    print(f"""\n PRODUCTO ENCONTRADO:
                    «{producto['nombre']}» (SKU: {producto['sku']})
                    Existencias: {producto['existencias']} unidad(es)
                    Precio compra: ${producto['precio compra']:.2f}
                    Precio venta: ${producto['precio venta']:.2f}
                    Categorías: «{categorias_str}»
                    
                    ANALISIS FINANCIERO:
                       • Inversion en stock: ${producto['precio compra'] * producto['existencias']:.2f}
                       • Valor venta stock: ${producto['precio venta'] * producto['existencias']:.2f}
                       • Ganancia unitaria: ${ganancia_unitaria:.2f}
                       • Ganancia total: ${ganancia_total:.2f}
                       • Margen de ganancia: {margen_ganancia:.2f}%""")
                    encuentro = True

            if not encuentro: 
                # si no se encuentra, buscar coincidencias similares
                resultados = []
                for producto in productos:
                    sim = similitud(consulta_norm, producto["nombre"])
                    if sim >= 0.4 or consulta_norm in normalizar(producto["nombre"]):
                        resultados.append((sim, producto))
                if resultados:
                    print("Producto exacto no encontrado. Quizá quiso decir?:")
                    for sim, prod in sorted(resultados, reverse=True):
                        categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                        ganancia_unitaria = prod["precio venta"] - prod["precio compra"]
                        print(f" → «{prod['nombre']}», (SKU N {prod['sku']}, {prod['existencias']} existencia(s), Compra: ${prod['precio compra']:.2f}, Venta: ${prod['precio venta']:.2f}, Ganancia: ${ganancia_unitaria:.2f}, categorías: «{categorias_str}»)")
                else:
                    print("Error! Producto no encontrado y sin coincidencias similares.")
            
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
                    print("Error! Opción no válida para cantidad.")
                    return False
            except ValueError:
                escribir_log("Error al ingresar cantidad en búsqueda.", nivel="ERROR")
                print("Error! Entrada inválida para cantidad.")
                return False
                
            if encontrados:
                # Calcular estadísticas de los productos encontrados
                stats_encontrados = calcular_estadisticas_financieras(encontrados)
                
                print(f"\n PRODUCTOS ENCONTRADOS: {len(encontrados)}")
                mostrar_estadisticas_financieras(stats_encontrados, "RESULTADOS DE BUSQUEDA")
                
                print("\n DETALLE DE PRODUCTOS:")
                for prod in encontrados:
                    ganancia_unitaria = prod["precio venta"] - prod["precio compra"]
                    categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(f" → SKU N {prod['sku']}: «{prod['nombre']}», ({prod['existencias']} existencia(s), Compra: ${prod['precio compra']:.2f}, Venta: ${prod['precio venta']:.2f}, Ganancia: ${ganancia_unitaria:.2f}, categorías: {categorias_str})")
                return True
            else:
                print("Error! No se encontraron productos con esa cantidad.")
                return False    
            
        case "4"|"cuatro"|"buscar precio":
            # Buscar por precio: exacto / mayor / menor / rango
            modo = normalizar(input("Buscar por precio compra (1) o precio venta (2): "))
            tipo_precio = "precio compra" if modo in ("1", "precio compra", "compra") else "precio venta"
            
            submodo = normalizar(input(f"Buscar por {tipo_precio}: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            try:
                if submodo in ("igual", "1", "exacto"):
                    p = float(input(f"Ingrese el {tipo_precio} exacto: "))
                    encontrados = [prod for prod in productos if abs(prod[tipo_precio] - p) < 1e-9]
                elif submodo in ("mayor", "2"):
                    p = float(input(f"Mostrar productos con {tipo_precio} > : "))
                    encontrados = [prod for prod in productos if prod[tipo_precio] > p]
                elif submodo in ("menor", "3"):
                    p = float(input(f"Mostrar productos con {tipo_precio} < : "))
                    encontrados = [prod for prod in productos if prod[tipo_precio] < p]
                elif submodo in ("rango", "4"):
                    lo = float(input(f"Ingrese el {tipo_precio} mínimo del rango: "))
                    hi = float(input(f"Ingrese el {tipo_precio} máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    encontrados = [prod for prod in productos if lo <= prod[tipo_precio] <= hi]
                else:
                    print("Error! Opción no válida para precio.")
                    return False
            except ValueError:
                escribir_log("Error al ingresar precio en búsqueda.", nivel="ERROR")
                print("Error! Ingrese un número válido para el precio.")
                return False

            if encontrados:
                # Calcular estadísticas de los productos encontrados
                stats_encontrados = calcular_estadisticas_financieras(encontrados)
                
                print(f"\n PRODUCTOS ENCONTRADOS: {len(encontrados)}")
                mostrar_estadisticas_financieras(stats_encontrados, f"BUSQUEDA POR {tipo_precio.upper()}")
                
                print("\n DETALLE DE PRODUCTOS:")
                for prod in encontrados:
                    ganancia_unitaria = prod["precio venta"] - prod["precio compra"]
                    categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(f" → SKU {prod['sku']}: {prod['nombre']} ({prod['existencias']} existencia(s), Compra: ${prod['precio compra']:.2f}, Venta: ${prod['precio venta']:.2f}, Ganancia: ${ganancia_unitaria:.2f}, categorías: {categorias_str})")
                return True
            else:
                print("No se encontraron productos con ese precio.")
                return False
            
        case "5"|"cinco"|"buscar categoría":
            categoria_buscar = input("Ingrese la categoría a buscar: ")
            encontrados = []
            for producto in productos:
                if any(normalizar(cat) == normalizar(categoria_buscar) for cat in producto["categorias"]):
                    encontrados.append(producto)
            
            if encontrados:
                # Calcular estadísticas de los productos encontrados
                stats_encontrados = calcular_estadisticas_financieras(encontrados)
                
                print(f"\n PRODUCTOS ENCONTRADOS EN '{categoria_buscar.upper()}': {len(encontrados)}")
                mostrar_estadisticas_financieras(stats_encontrados, f"CATEGORIA: {categoria_buscar.upper()}")
                
                print("\n DETALLE DE PRODUCTOS:")
                for prod in encontrados:
                    ganancia_unitaria = prod["precio venta"] - prod["precio compra"]
                    categorias_str = ", ".join(prod["categorias"])
                    print(f" → SKU {prod['sku']}: {prod['nombre']} ({prod['existencias']} existencia(s), Compra: ${prod['precio compra']:.2f}, Venta: ${prod['precio venta']:.2f}, Ganancia: ${ganancia_unitaria:.2f}, categorías: {categorias_str})")
                return True
            else:
                print(f"Error! No se encontraron productos en la categoría '{categoria_buscar}'.")
                return False

        case "6"|"seis"|"analisis"|"análisis"|"financiero":
            analisis_financiero_completo()
            return True
        
        case "7"|"siete"|"volver":
            return True

        case _:
            print("Error! Opción no válida...")
    return False

# =============================================================================
# FUNCIONES DE GESTIÓN DE CLIENTES
# =============================================================================

def ingresar_cliente():
    # Función para agregar un nuevo cliente
    data = cargar_memory()
    clientes = data["clientes"]
    
    try:
        # ID único del cliente
        id_cliente = int(input("Ingrese el ID del cliente: "))
        for cliente in clientes:
            if cliente["id"] == id_cliente:
                print("Error! El ID de cliente ya existe...")
                return False
        
        # Nombre del cliente
        nombre = input("Ingrese el nombre del cliente: ")
        
        # Verificar que el nombre no esté duplicado
        for cliente in clientes:
            if normalizar(cliente["nombre"]) == normalizar(nombre):
                print("Error! Ya existe un cliente con ese nombre...")
                return False
        
        # Información de contacto
        telefono = input("Ingrese el teléfono del cliente: ")
        email = input("Ingrese el email del cliente: ")
        direccion = input("Ingrese la dirección del cliente: ")
        
        # Tipo de cliente
        tipo_cliente = normalizar(input("Ingrese el tipo de cliente (Normal/Preferencial/Corporativo): "))
        while tipo_cliente not in ["normal", "preferencial", "corporativo"]:
            print("Error! Tipo de cliente no válido. Use: Normal, Preferencial o Corporativo")
            tipo_cliente = normalizar(input("Ingrese el tipo de cliente: "))
        
        # Límite de crédito (opcional)
        try:
            limite_credito = float(input("Ingrese el límite de crédito (0 si no aplica): "))
        except ValueError:
            limite_credito = 0.0
        
        # Estado del cliente
        estado = normalizar(input("Cliente activo? (Si/No): "))
        activo = estado in ["si", "s", "1", "yes", "y"]
        
        # Crear nuevo cliente
        nuevo_cliente = {
            "id": id_cliente,
            "nombre": nombre,
            "telefono": telefono,
            "email": email,
            "direccion": direccion,
            "tipo": tipo_cliente,
            "limite_credito": limite_credito,
            "activo": activo,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Agregar a la lista de clientes
        clientes.append(nuevo_cliente)
        
        # Guardar en el archivo
        guardar_memory(data)
        print("Cliente agregado correctamente.")
        escribir_log(f"Cliente agregado: {nombre} (ID: {id_cliente})", nivel="INFO")
        return True
        
    except ValueError:
        print("Error! Ingrese valores numéricos válidos para ID y límite de crédito.")
        escribir_log("Error al ingresar valores numéricos en ingreso de cliente.", nivel="ERROR")
        return False

def eliminar_cliente():
    # Función para eliminar un cliente
    data = cargar_memory()
    clientes = data["clientes"]
    
    if not clientes:
        print("No hay clientes registrados para eliminar.")
        return False
    
    try:
        id_cliente = int(input("Ingrese el ID del cliente a eliminar: "))
        for i, cliente in enumerate(clientes):
            if cliente["id"] == id_cliente:
                print(f"Cliente encontrado: {cliente['nombre']}")
                confirmacion = normalizar(input("Esta seguro que desea eliminar este cliente? (Si/No): "))
                if confirmacion in ["si", "s", "1"]:
                    cliente_eliminado = clientes.pop(i)
                    guardar_memory(data)
                    print("Cliente eliminado correctamente.")
                    escribir_log(f"Cliente eliminado: {cliente_eliminado['nombre']} (ID: {cliente_eliminado['id']})", nivel="INFO")
                    return True
                else:
                    print("Operación cancelada.")
                    return False
        
        print("Error! Cliente no encontrado...")
        return False
        
    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log("Error al ingresar ID en eliminación de cliente.", nivel="ERROR")
        return False

def modificar_cliente():
    # Función para modificar un cliente existente
    data = cargar_memory()
    clientes = data["clientes"]
    
    if not clientes:
        print("No hay clientes registrados para modificar.")
        return False
    
    try:
        id_cliente = int(input("Ingrese el ID del cliente a modificar: "))
        for cliente in clientes:
            if cliente["id"] == id_cliente:
                print(f"Cliente encontrado: {cliente['nombre']}")
                print("\nQue desea modificar?")
                print("1. Nombre")
                print("2. Teléfono")
                print("3. Email")
                print("4. Dirección")
                print("5. Tipo de cliente")
                print("6. Límite de crédito")
                print("7. Estado (Activo/Inactivo)")
                
                opcion = normalizar(input("Seleccione una opción: "))
                
                match opcion:
                    case "1" | "nombre":
                        nuevo_nombre = input("Ingrese el nuevo nombre: ")
                        # Verificar que el nuevo nombre no exista
                        for cli in clientes:
                            if cli != cliente and normalizar(cli["nombre"]) == normalizar(nuevo_nombre):
                                print("Error! Ya existe un cliente con ese nombre...")
                                return False
                        cliente["nombre"] = nuevo_nombre
                        
                    case "2" | "telefono" | "teléfono":
                        cliente["telefono"] = input("Ingrese el nuevo teléfono: ")
                        
                    case "3" | "email" | "correo":
                        cliente["email"] = input("Ingrese el nuevo email: ")
                        
                    case "4" | "direccion" | "dirección":
                        cliente["direccion"] = input("Ingrese la nueva dirección: ")
                        
                    case "5" | "tipo":
                        nuevo_tipo = normalizar(input("Ingrese el nuevo tipo (Normal/Preferencial/Corporativo): "))
                        while nuevo_tipo not in ["normal", "preferencial", "corporativo"]:
                            print("Error! Tipo de cliente no válido.")
                            nuevo_tipo = normalizar(input("Ingrese el tipo de cliente: "))
                        cliente["tipo"] = nuevo_tipo
                        
                    case "6" | "limite" | "límite" | "credito" | "crédito":
                        try:
                            nuevo_limite = float(input("Ingrese el nuevo límite de crédito: "))
                            cliente["limite_credito"] = nuevo_limite
                        except ValueError:
                            print("Error! Ingrese un valor numérico válido.")
                            return False
                            
                    case "7" | "estado":
                        nuevo_estado = normalizar(input("Cliente activo? (Si/No): "))
                        cliente["activo"] = nuevo_estado in ["si", "s", "1", "yes", "y"]
                        
                    case _:
                        print("Error! Opción no válida...")
                        return False
                
                guardar_memory(data)
                print("Cliente modificado correctamente.")
                escribir_log(f"Cliente modificado: {cliente['nombre']} (ID: {cliente['id']})", nivel="INFO")
                return True
        
        print("Error! Cliente no encontrado...")
        return False
        
    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log("Error al ingresar ID en modificación de cliente.", nivel="ERROR")
        return False

def buscar_cliente():
    # Función para buscar clientes
    data = cargar_memory()
    clientes = data["clientes"]
    
    if not clientes:
        print("No hay clientes registrados.")
        return False
    
    print("\nOpciones de búsqueda:")
    print("1. Por ID")
    print("2. Por nombre")
    print("3. Por tipo de cliente")
    print("4. Por estado (Activo/Inactivo)")
    print("5. Ver todos los clientes")
    
    opcion = normalizar(input("Seleccione una opción: "))
    resultados = []
    
    match opcion:
        case "1" | "id":
            try:
                id_buscar = int(input("Ingrese el ID del cliente: "))
                resultados = [cliente for cliente in clientes if cliente["id"] == id_buscar]
            except ValueError:
                print("Error! Ingrese un ID válido.")
                return False
                
        case "2" | "nombre":
            nombre_buscar = input("Ingrese el nombre o parte del nombre: ")
            nombre_buscar_norm = normalizar(nombre_buscar)
            for cliente in clientes:
                if nombre_buscar_norm in normalizar(cliente["nombre"]):
                    resultados.append(cliente)
                    
        case "3" | "tipo":
            tipo_buscar = normalizar(input("Ingrese el tipo de cliente (Normal/Preferencial/Corporativo): "))
            resultados = [cliente for cliente in clientes if cliente["tipo"] == tipo_buscar]
            
        case "4" | "estado":
            estado_buscar = normalizar(input("Buscar clientes activos (Si) o inactivos (No): "))
            activo_buscar = estado_buscar in ["si", "s", "1", "yes", "y"]
            resultados = [cliente for cliente in clientes if cliente["activo"] == activo_buscar]
            
        case "5" | "todos" | "ver todos":
            resultados = clientes
            
        case _:
            print("Error! Opción no válida...")
            return False
    
    if resultados:
        print(f"\nSe encontraron {len(resultados)} cliente(s):")
        for cliente in resultados:
            estado = "Activo" if cliente["activo"] else "Inactivo"
            print(f"\nID: {cliente['id']}")
            print(f"Nombre: {cliente['nombre']}")
            print(f"Teléfono: {cliente['telefono']}")
            print(f"Email: {cliente['email']}")
            print(f"Dirección: {cliente['direccion']}")
            print(f"Tipo: {cliente['tipo'].title()}")
            print(f"Límite de crédito: ${cliente['limite_credito']:.2f}")
            print(f"Estado: {estado}")
            print(f"Fecha de registro: {cliente['fecha_registro']}")
            print("-" * 40)
        return True
    else:
        print("No se encontraron clientes con los criterios especificados.")
        return False

def gestionar_clientes_modo(modo=None):
    # Función unificada para gestión de clientes
    data = cargar_memory()
    
    if modo == "agregar":
        return ingresar_cliente()
        
    elif modo == "eliminar":
        return eliminar_cliente()
        
    elif modo == "modificar":
        return modificar_cliente()
        
    elif modo == "buscar" or modo == "ver":
        return buscar_cliente()
    
    else:
        # Menú interactivo
        while True:
            
            opcion = normalizar(input("Seleccione una opción: "))
            
            match opcion:
                case "1" | "uno" | "agregar":
                    ingresar_cliente()
                    
                case "2" | "dos" | "eliminar":
                    eliminar_cliente()
                    
                case "3" | "tres" | "modificar":
                    modificar_cliente()
                    
                case "4" | "cuatro" | "buscar" | "ver":
                    buscar_cliente()
                    
                case "5" | "cinco" | "volver":
                    return True
                    
                case _:
                    print("Error! Opción no válida...")
            
            continuar = normalizar(input("Desea realizar otra operación de clientes? (Si/No): "))
            if continuar not in ["si", "s", "1", "yes", "y"]:
                break
        
        return True

# =============================================================================
# FUNCIONES DE GESTIÓN DE PROVEEDORES
# =============================================================================

def ingresar_proveedor():
    # Función para agregar un nuevo proveedor
    data = cargar_memory()
    proveedores = data["proveedores"]

    try:
        # ID único del proveedor
        id_proveedor = int(input("Ingrese el ID del proveedor: "))
        for proveedor in proveedores:
            while proveedor["id"] == id_proveedor and id_proveedor != -1:
                print("Error! El ID de proveedor ya existe...")
                id_proveedor = int(input("Ingrese el ID del proveedor: "))

        if id_proveedor == -1:
            return

        # Nombre del proveedor
        nombre = input("Ingrese el nombre del proveedor: ")
        
        # Verificar que el nombre no esté duplicado
        for proveedor in proveedores:
            while normalizar(proveedor["nombre"]) == normalizar(nombre) and nombre not in ("-1", "salir"):
                print("Error! Ya existe un proveedor con ese nombre...")
                nombre = input("Ingrese el nombre del proveedor: ")
        
        if nombre in("-1", "salir"):
            return
        
        # Información de contacto
        telefono = input("Ingrese el teléfono del proveedor: ")
        email = input("Ingrese el email del proveedor: ")
        direccion = input("Ingrese la dirección del proveedor: ")
        contacto = input("Ingrese el nombre de la persona de contacto: ")
        
        # Especialidad del proveedor
        especialidad = input("Ingrese la especialidad del proveedor (ej: electrónica, ropa, alimentos): ")
        
        # Condiciones de pago
        condiciones_pago = normalizar(input("Ingrese condiciones de pago (Contado/15 días/30 días): "))
        
        # Estado del proveedor
        estado = normalizar(input("Proveedor activo? (Si/No): "))
        activo = estado in ["si", "s", "1", "yes", "y"]
        
        # Calificación del proveedor (1-5)
        try:
            calificacion = int(input("Ingrese calificación del proveedor (1-5): "))
            if calificacion < 1 or calificacion > 5:
                calificacion = 3  # Valor por defecto
        except ValueError:
            calificacion = 3
        
        # Crear nuevo proveedor
        nuevo_proveedor = {
            "id": id_proveedor,
            "nombre": nombre,
            "telefono": telefono,
            "email": email,
            "direccion": direccion,
            "contacto": contacto,
            "especialidad": especialidad,
            "condiciones_pago": condiciones_pago,
            "calificacion": calificacion,
            "activo": activo,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Agregar a la lista de proveedores
        proveedores.append(nuevo_proveedor)
        
        # Guardar en el archivo
        guardar_memory(data)
        print("Proveedor agregado correctamente.")
        escribir_log(f"Proveedor agregado: {nombre} (ID: {id_proveedor})", nivel="INFO")
        return True
        
    except ValueError:
        print("Error! Ingrese valores numéricos válidos para ID y calificación.")
        escribir_log("Error al ingresar valores numéricos en ingreso de proveedor.", nivel="ERROR")
        return False

def eliminar_proveedor():
    # Función para eliminar un proveedor
    data = cargar_memory()
    proveedores = data["proveedores"]

    if not proveedores:
        print("No hay proveedores registrados para eliminar.")
        return False
    
    try:
        id_proveedor = int(input("Ingrese el ID del proveedor a eliminar: "))
        for i, proveedor in enumerate(proveedores):
            if proveedor["id"] == id_proveedor and id_proveedor != -1:
                print(f"Proveedor encontrado: {proveedor['nombre']}")
                
                # Verificar si el proveedor tiene productos asociados
                productos_asociados = []
                data_productos = cargar_memory()
                for producto in data_productos["productos"]:
                    # Buscar si el producto menciona al proveedor en nombre o categorías
                    if (proveedor["nombre"].lower() in producto["nombre"].lower() or
                        any(proveedor["nombre"].lower() in cat.lower() for cat in producto["categorias"])):
                        productos_asociados.append(producto)
                
                if productos_asociados:
                    print(f"ADVERTENCIA: Este proveedor tiene {len(productos_asociados)} producto(s) asociado(s):")
                    for prod in productos_asociados[:3]:  # Mostrar solo los primeros 3
                        print(f"   - {prod['nombre']} (SKU: {prod['sku']})")
                    if len(productos_asociados) > 3:
                        print(f"   ... y {len(productos_asociados) - 3} más")
                
                confirmacion = normalizar(input("Esta seguro que desea eliminar este proveedor? (Si/No): "))
                if confirmacion in ["si", "s", "1"]:
                    proveedor_eliminado = proveedores.pop(i)
                    guardar_memory(data)
                    print("Proveedor eliminado correctamente.")
                    escribir_log(f"Proveedor eliminado: {proveedor_eliminado['nombre']} (ID: {proveedor_eliminado['id']})", nivel="INFO")
                else:
                    print("Operación cancelada.")
            elif id_proveedor == -1:
                break
            else:
                print("Error! Proveedor no encontrado...")
        return False
        
    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log("Error al ingresar ID en eliminación de proveedor.", nivel="ERROR")
        return False

def modificar_proveedor():
    # Función para modificar un proveedor existente
    data = cargar_memory()
    proveedores = data["proveedores"]
    
    if not proveedores:
        print("No hay proveedores registrados para modificar.")
        return False
    
    try:
        id_proveedor = int(input("Ingrese el ID del proveedor a modificar: "))
        for proveedor in proveedores:
            if proveedor["id"] == id_proveedor:
                print(f"Proveedor encontrado: {proveedor['nombre']}")
                print("\nQue desea modificar?")
                print("1. Nombre")
                print("2. Teléfono")
                print("3. Email")
                print("4. Dirección")
                print("5. Contacto")
                print("6. Especialidad")
                print("7. Condiciones de pago")
                print("8. Calificación")
                print("9. Estado (Activo/Inactivo)")
                
                opcion = normalizar(input("Seleccione una opción: "))
                
                match opcion:
                    case "1" | "nombre":
                        nuevo_nombre = input("Ingrese el nuevo nombre: ")
                        # Verificar que el nuevo nombre no exista
                        for prov in proveedores:
                            if prov != proveedor and normalizar(prov["nombre"]) == normalizar(nuevo_nombre):
                                print("Error! Ya existe un proveedor con ese nombre...")
                            else:
                                proveedor["nombre"] = nuevo_nombre
                        
                    case "2" | "telefono" | "teléfono":
                        proveedor["telefono"] = input("Ingrese el nuevo teléfono: ")
                        
                    case "3" | "email" | "correo":
                        proveedor["email"] = input("Ingrese el nuevo email: ")
                        
                    case "4" | "direccion" | "dirección":
                        proveedor["direccion"] = input("Ingrese la nueva dirección: ")
                        
                    case "5" | "contacto":
                        proveedor["contacto"] = input("Ingrese el nuevo contacto: ")
                        
                    case "6" | "especialidad":
                        proveedor["especialidad"] = input("Ingrese la nueva especialidad: ")
                        
                    case "7" | "condiciones" | "pago":
                        proveedor["condiciones_pago"] = input("Ingrese las nuevas condiciones de pago: ")
                        
                    case "8" | "calificacion" | "calificación":
                        try:
                            nueva_calificacion = int(input("Ingrese la nueva calificación (1-5): "))
                            if 1 <= nueva_calificacion <= 5:
                                proveedor["calificacion"] = nueva_calificacion
                            else:
                                print("Error! La calificación debe estar entre 1 y 5.")
                        except ValueError:
                            print("Error! Ingrese un número válido.")
                            
                    case "9" | "estado":
                        nuevo_estado = normalizar(input("Proveedor activo? (Si/No): "))
                        proveedor["activo"] = nuevo_estado in ["si", "s", "1", "yes", "y"]
                        
                    case _:
                        print("Error! Opción no válida...")
                
                guardar_memory(data)
                print("Proveedor modificado correctamente.")
                escribir_log(f"Proveedor modificado: {proveedor['nombre']} (ID: {proveedor['id']})", nivel="INFO")
                return True
            else:
                print("Error! Proveedor no encontrado...")
        return False
        
    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log("Error al ingresar ID en modificación de proveedor.", nivel="ERROR")
        return False

def buscar_proveedor():
    # Función para buscar proveedores
    data = cargar_memory()
    proveedores = data["proveedores"]
    
    if not proveedores:
        print("No hay proveedores registrados.")
        return False
    
    print("\nOpciones de búsqueda:")
    print("1. Por ID")
    print("2. Por nombre")
    print("3. Por especialidad")
    print("4. Por estado (Activo/Inactivo)")
    print("5. Por calificación")
    print("6. Ver todos los proveedores")
    
    opcion = normalizar(input("Seleccione una opción: "))
    resultados = []
    
    match opcion:
        case "1" | "id":
            try:
                id_buscar = int(input("Ingrese el ID del proveedor: "))
                resultados = [proveedor for proveedor in proveedores if proveedor["id"] == id_buscar]
            except ValueError:
                print("Error! Ingrese un ID válido.")
                return False
                
        case "2" | "nombre":
            nombre_buscar = input("Ingrese el nombre o parte del nombre: ")
            nombre_buscar_norm = normalizar(nombre_buscar)
            for proveedor in proveedores:
                if nombre_buscar_norm in normalizar(proveedor["nombre"]):
                    resultados.append(proveedor)
                    
        case "3" | "especialidad":
            especialidad_buscar = input("Ingrese la especialidad: ")
            especialidad_buscar_norm = normalizar(especialidad_buscar)
            resultados = [proveedor for proveedor in proveedores if especialidad_buscar_norm in normalizar(proveedor["especialidad"])]
            
        case "4" | "estado":
            estado_buscar = normalizar(input("Buscar proveedores activos (Si) o inactivos (No): "))
            activo_buscar = estado_buscar in ["si", "s", "1", "yes", "y"]
            resultados = [proveedor for proveedor in proveedores if proveedor["activo"] == activo_buscar]
            
        case "5" | "calificacion" | "calificación":
            try:
                calificacion_buscar = int(input("Ingrese la calificación mínima (1-5): "))
                resultados = [proveedor for proveedor in proveedores if proveedor["calificacion"] >= calificacion_buscar]
            except ValueError:
                print("Error! Ingrese una calificación válida.")
                return False
                
        case "6" | "todos" | "ver todos":
            resultados = proveedores
            
        case _:
            print("Error! Opción no válida...")
            return False
    
    if resultados:
        print(f"\nSe encontraron {len(resultados)} proveedor(es):")
        for proveedor in resultados:
            estado = "Activo" if proveedor["activo"] else "Inactivo"
            estrellas = "*" * proveedor["calificacion"] + "-" * (5 - proveedor["calificacion"])
            
            print(f"\n ID: {proveedor['id']} - {proveedor['nombre']}")
            print(f"   Teléfono: {proveedor['telefono']}")
            print(f"    Email: {proveedor['email']}")
            print(f"   Dirección: {proveedor['direccion']}")
            print(f"   Contacto: {proveedor['contacto']}")
            print(f"   Especialidad: {proveedor['especialidad']}")
            print(f"   Condiciones pago: {proveedor['condiciones_pago']}")
            print(f"   Calificación: {estrellas} ({proveedor['calificacion']}/5)")
            print(f"   Estado: {estado}")
            print(f"   Fecha registro: {proveedor['fecha_registro']}")
            print("-" * 50)
        return True
    else:
        print("No se encontraron proveedores con los criterios especificados.")
        return False

def analizar_proveedores():
    # Función para análisis de proveedores
    data = cargar_memory()
    proveedores = data["proveedores"]
    productos = data["productos"]
    
    if not proveedores:
        print("No hay proveedores registrados para analizar.")
        return False
    
    print("\nANALISIS DE PROVEEDORES")
    print("=" * 60)
    
    # Estadísticas generales
    total_proveedores = len(proveedores)
    proveedores_activos = len([p for p in proveedores if p["activo"]])
    promedio_calificacion = sum(p["calificacion"] for p in proveedores) / total_proveedores
    
    print(f"Total de proveedores: {total_proveedores}")
    print(f"Proveedores activos: {proveedores_activos}")
    print(f"Proveedores inactivos: {total_proveedores - proveedores_activos}")
    print(f"Calificación promedio: {promedio_calificacion:.2f}/5")
    
    # Top proveedores por calificación
    top_proveedores = sorted(proveedores, key=lambda x: x["calificacion"], reverse=True)[:5]
    print(f"\nTOP 5 PROVEEDORES MEJOR CALIFICADOS:")
    for i, proveedor in enumerate(top_proveedores, 1):
        estrellas = "*" * proveedor["calificacion"]
        print(f"  {i}. {proveedor['nombre']} - {estrellas} ({proveedor['calificacion']}/5)")
    
    # Distribución por especialidad
    especialidades = {}
    for proveedor in proveedores:
        especialidad = proveedor["especialidad"]
        if especialidad not in especialidades:
            especialidades[especialidad] = 0
        especialidades[especialidad] += 1
    
    if especialidades:
        print(f"\nDISTRIBUCIÓN POR ESPECIALIDAD:")
        for especialidad, cantidad in sorted(especialidades.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {especialidad}: {cantidad} proveedor(es)")
    
    # Relación con productos (análisis básico)
    print(f"\nRELACIÓN CON PRODUCTOS:")
    for proveedor in proveedores:
        productos_asociados = []
        for producto in productos:
            if (proveedor["nombre"].lower() in producto["nombre"].lower() or
                any(proveedor["nombre"].lower() in cat.lower() for cat in producto["categorias"])):
                productos_asociados.append(producto)
        
        if productos_asociados:
            print(f"  • {proveedor['nombre']}: {len(productos_asociados)} producto(s) asociado(s)")
    
    return True

def gestionar_proveedores_modo(modo=None):
    # Función unificada para gestión de proveedores
    data = cargar_memory()
    
    if modo == "agregar":
        return ingresar_proveedor()
        
    elif modo == "eliminar":
        return eliminar_proveedor()
        
    elif modo == "modificar":
        return modificar_proveedor()
        
    elif modo == "buscar" or modo == "ver":
        return buscar_proveedor()
        
    elif modo == "analizar":
        return analizar_proveedores()
    
    else:
        # Menú interactivo
        while True:
            
            opcion = normalizar(input("Seleccione una opción: "))
            
            match opcion:
                case "1" | "uno" | "agregar":
                    ingresar_proveedor()
                    
                case "2" | "dos" | "eliminar":
                    eliminar_proveedor()
                    
                case "3" | "tres" | "modificar":
                    modificar_proveedor()
                    
                case "4" | "cuatro" | "buscar" | "ver":
                    buscar_proveedor()
                    
                case "5" | "cinco" | "analizar" | "análisis":
                    analizar_proveedores()
                    
                case "6" | "seis" | "volver":
                    break
                    
                case _:
                    print("Error! Opción no válida...")
            
            continuar = normalizar(input("Desea realizar otra operación de proveedores? (Si/No): "))
            if continuar not in ["si", "s", "1", "yes", "y"]:
                return
        
        return True
import json
from datetime import datetime
import os

def limpiarPantalla():
    os.system('cls')

def escribir_log(mensaje, nivel="INFO"):
    try:
        f = open('loginventario.txt', 'at', encoding = 'UTF8')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {nivel} - {mensaje} \n")
    except FileNotFoundError as e:
        print(f"¡Error! No se puedo escribir en el log.: {e}")


def obtener_ruta_archivo(tipo, numero=None):
    """Obtiene la ruta del archivo desde el enrutador TXT"""
    try:
        f = open('enrutador.txt', 'rt', encoding='UTF8')
        lineas = f.readlines()
        f.close()
        
        for linea in lineas:
            partes = linea.strip().split('=')
            if len(partes) == 2:
                clave, valor = partes
                if tipo == "productos" and clave == "productos":
                    return valor
                elif tipo == "categorias" and clave == "categorias":
                    return valor
                elif tipo == "base_productos" and clave == "base_productos":
                    if numero:
                        return valor.replace('{n}', str(numero))
                    return valor.replace('{n}', '1')
        
        # Si no encuentra en el enrutador, usar valores por defecto
        if tipo == "productos":
            return "productos.json"
        elif tipo == "categorias":
            return "categorias.json"
        elif tipo == "base_productos":
            if numero:
                return f"productos_{numero}.json"
            return "productos_1.json"
            
    except FileNotFoundError:
        # Crear enrutador por defecto si no existe
        crear_enrutador_por_defecto()
        if tipo == "productos":
            return "productos.json"
        elif tipo == "categorias":
            return "categorias.json"
        elif tipo == "base_productos":
            if numero:
                return f"productos_{numero}.json"
            return "productos_1.json"

def crear_enrutador_por_defecto():
    """Crea el archivo enrutador con configuraciones por defecto"""
    try:
        f = open('enrutador.txt', 'wt', encoding='UTF8')
        f.write("productos=productos.json\n")
        f.write("categorias=categorias.json\n")
        f.write("base_productos=productos_{n}.json\n")
        f.write("max_productos_por_archivo=100\n")
        f.close()
        print("Enrutador creado por defecto.")
    except Exception as e:
        print(f"Error creando enrutador: {e}")

def cargar_memory():
    """Carga todos los productos desde todos los archivos JSON"""
    data = {"productos": [], "categorias": []}
    
    try:
        # Cargar archivo principal de productos (JSON)
        ruta_principal = obtener_ruta_archivo("productos")
        f = open(ruta_principal, 'rt', encoding='UTF8')
        data_principal = json.load(f)
        f.close()
        
        total_archivos = data_principal.get("total_archivos", 1)
        
        # Cargar productos de todos los archivos JSON
        for i in range(1, total_archivos + 1):
            try:
                ruta_archivo = obtener_ruta_archivo("base_productos", i)
                f_archivo = open(ruta_archivo, 'rt', encoding='UTF8')
                productos_archivo = json.load(f_archivo)
                f_archivo.close()
                
                if isinstance(productos_archivo, list):
                    data["productos"].extend(productos_archivo)
                else:
                    # Si es un diccionario con clave "productos"
                    data["productos"].extend(productos_archivo.get("productos", []))
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Error cargando archivo {i}: {e}")
                
    except FileNotFoundError:
        # Inicializar sistema si no existe
        inicializar_sistema_archivos()
    except Exception as e:
        print(f"Error cargando memoria: {e}")
    
    # Cargar categorías desde JSON
    try:
        ruta_categorias = obtener_ruta_archivo("categorias")
        f = open(ruta_categorias, 'rt', encoding='UTF8')
        data["categorias"] = json.load(f)
        f.close()
    except:
        data["categorias"] = []
    
    return data

def guardar_memory(data):
    """Guarda productos en el sistema de archivos múltiples JSON"""
    productos = data["productos"]
    max_por_archivo = 100
    
    # Calcular cuántos archivos necesitamos
    total_archivos = (len(productos) // max_por_archivo) + 1
    if len(productos) % max_por_archivo == 0 and total_archivos > 0:
        total_archivos -= 1
    
    # Guardar archivo principal (JSON)
    ruta_principal = obtener_ruta_archivo("productos")
    f_principal = open(ruta_principal, 'wt', encoding='UTF8')
    json.dump({
        "total_archivos": total_archivos,
        "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_productos": len(productos)
    }, f_principal, indent=2)
    f_principal.close()
    
    # Guardar productos en archivos JSON separados
    for i in range(1, total_archivos + 1):
        inicio = (i - 1) * max_por_archivo
        fin = i * max_por_archivo
        productos_lote = productos[inicio:fin]
        
        ruta_archivo = obtener_ruta_archivo("base_productos", i)
        f_archivo = open(ruta_archivo, 'wt', encoding='UTF8')
        json.dump(productos_lote, f_archivo, indent=2)
        f_archivo.close()
    
    # Guardar categorías en JSON
    guardar_categorias(data["categorias"])

def inicializar_sistema_archivos():
    """Inicializa el sistema de archivos si no existe"""
    try:
        # Crear archivo principal de productos (JSON)
        ruta_principal = obtener_ruta_archivo("productos")
        f = open(ruta_principal, 'wt', encoding='UTF8')
        json.dump({
            "total_archivos": 1,
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_productos": 0
        }, f, indent=2)
        f.close()
        
        # Crear primer archivo de productos (JSON vacío)
        ruta_archivo1 = obtener_ruta_archivo("base_productos", 1)
        f = open(ruta_archivo1, 'wt', encoding='UTF8')
        json.dump([], f, indent=2)
        f.close()
        
        # Crear archivo de categorías (JSON vacío)
        ruta_categorias = obtener_ruta_archivo("categorias")
        f = open(ruta_categorias, 'wt', encoding='UTF8')
        json.dump([], f, indent=2)
        f.close()
        
        print("Sistema de archivos JSON inicializado correctamente.")
    except Exception as e:
        print(f"Error inicializando sistema: {e}")

def guardar_categorias(categorias):
    """Guarda categorías en archivo JSON"""
    try:
        ruta_categorias = obtener_ruta_archivo("categorias")
        f = open(ruta_categorias, 'wt', encoding='UTF8')
        json.dump(categorias, f, indent=2)
        f.close()
    except Exception as e:
        print(f"Error guardando categorías: {e}")


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

def comprobar(tag_nuevo):
    """Verifica si un SKU o nombre de producto ya existe"""
    data = cargar_memory()
    encontrado = False
    
    for producto in data["productos"]:
        # Verificar por SKU (número) o nombre (string)
        if (isinstance(tag_nuevo, int) and producto.get("SKU") == tag_nuevo) or \
           (isinstance(tag_nuevo, str) and normalizar(producto.get("nombre_producto", "")) == normalizar(tag_nuevo)):
            encontrado = True
            break
    
    return encontrado

def error_valor_numerico(campo):
    print(f"¡Error! Ingrese un valor numérico válido para {campo}.")
    escribir_log(f"¡Error al ingresar {campo}!", nivel="ERROR")


def error_no_encontrado(tipo, valor):
    print(f"¡Error! {tipo} «{valor}» no encontrado.")
    escribir_log(f"¡{tipo} no encontrado: {valor}!", nivel="WARNING")


def error_ya_existe(tipo, valor):
    print(f"¡Error! El {tipo} «{valor}» ya existe.")
    escribir_log(f"¡{tipo} ya existe: {valor}!", nivel="WARNING")


def buscar():
    """Función de búsqueda - actualizada para JSON"""
    data = cargar_memory()
    productos = data["productos"]
    encuentro = False
    
    print("\n--- BÚSQUEDA ---")
    print("1. Buscar por SKU")
    print("2. Buscar por nombre")
    print("3. Buscar por cantidad")
    print("4. Buscar por precio") 
    print("5. Buscar por categoría")
    print("6. Volver")
    
    seleccion = normalizar(input("Seleccione una opción: "))

    if seleccion in ["1", "uno", "buscar sku"]:
        try:
            sku = int(input("Ingrese el SKU a buscar: "))
            for producto in productos:
                if producto.get("SKU") == sku:
                    categorias_str = ", ".join(producto["categorias"]) if producto["categorias"] else "Sin categorías"
                    print(f"SKU Nº {sku}: «{producto['nombre_producto']}»")
                    print(f"  Existencias: {producto['existencias']}")
                    print(f"  Precio: ${producto['precio']:.2f}")
                    print(f"  Categorías: {categorias_str}")
                    encuentro = True
                    break
            if not encuentro:
                error_no_encontrado("SKU", sku)
        except ValueError:
            error_valor_numerico("SKU")

    elif seleccion in ["2", "dos", "buscar producto"]:
        consulta = input("Ingrese el nombre del producto a buscar: ")
        consulta_norm = normalizar(consulta)
        for producto in productos:
            if normalizar(producto.get("nombre_producto", "")) == consulta_norm:
                categorias_str = ", ".join(producto["categorias"]) if producto["categorias"] else "Sin categorías"
                print(f"Producto: «{producto['nombre_producto']}»")
                print(f"  SKU: {producto['SKU']}")
                print(f"  Existencias: {producto['existencias']}")
                print(f"  Precio: ${producto['precio']:.2f}")
                print(f"  Categorías: {categorias_str}")
                encuentro = True

        if not encuentro:
            # Búsqueda aproximada
            resultados = []
            for producto in productos:
                sim = similitud(consulta_norm, producto.get("nombre_producto", ""))
                if sim >= 0.4:
                    resultados.append((sim, producto))
            
            if resultados:
                print("Producto exacto no encontrado. ¿Quizá quiso decir?:")
                for sim, prod in sorted(resultados, reverse=True)[:5]:
                    categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(f"  «{prod['nombre_producto']}» (SKU: {prod['SKU']}) - Similitud: {sim:.1%}")
            else:
                error_no_encontrado("Producto", consulta)

    elif seleccion in ["3", "tres", "buscar cantidad"]:
        try:
            modo = normalizar(input("Buscar por cantidad: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            
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

            if encontrados:
                print("Productos encontrados:")
                for prod in encontrados:
                    categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(f"  SKU {prod['SKU']}: {prod['nombre_producto']} ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
            else:
                print("No se encontraron productos con esa cantidad.")

        except ValueError:
            error_valor_numerico("cantidad")

    elif seleccion in ["4", "cuatro", "buscar precio"]:
        try:
            modo = normalizar(input("Buscar por precio: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            
            if modo in ("igual", "1", "exacto"):
                p = float(input("Ingrese el precio exacto: "))
                encontrados = [prod for prod in productos if abs(prod["precio"] - p) < 0.01]
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

            if encontrados:
                print("Resultados encontrados:")
                for prod in encontrados:
                    categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(f"  SKU {prod['SKU']}: {prod['nombre_producto']} ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
            else:
                print("No se encontraron productos con ese precio.")

        except ValueError:
            error_valor_numerico("precio")

    elif seleccion in ["5", "cinco", "buscar categoría"]:
        categoria_buscar = normalizar(input("Ingrese la categoría a buscar: "))
        encontrados = []
        for producto in productos:
            if any(normalizar(cat) == categoria_buscar for cat in producto["categorias"]):
                encontrados.append(producto)

        if encontrados:
            print(f"Productos encontrados en la categoría '{categoria_buscar}':")
            for prod in encontrados:
                categorias_str = ", ".join(prod["categorias"])
                print(f"  SKU {prod['SKU']}: {prod['nombre_producto']} ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
        else:
            error_no_encontrado("Categoría", categoria_buscar)

    elif seleccion in ["6", "seis", "volver"]:
        return True

    else:
        print("¡Error! Opción no válida.")

    return True


def ingresar(intentos=3):
    """
    Función de ingreso de productos con recursividad para manejo de errores
    intentos: número máximo de reintentos permitidos (por defecto 3)
    """
    if intentos <= 0:
        print("Demasiados intentos fallidos. Volviendo al menú principal.")
        escribir_log("Demasiados intentos fallidos en ingreso de producto", nivel="ERROR")
        return False
    
    try:
        data = cargar_memory()
        productos = data["productos"]
        
        print(f"\n--- INGRESAR PRODUCTO (Intento {4 - intentos}/3) ---")
        
        # Generación de SKU con recursividad
        def obtener_sku():
            print("\nGeneración de SKU:")
            print("1. Automático")
            print("2. Manual")
            opcion_sku = input("Seleccione opción (1/2): ").strip()

            if opcion_sku == "1":
                return generador_de_sku()
            elif opcion_sku == "2":
                try:
                    sku = int(input("Ingrese el SKU manualmente: "))
                    if comprobar(sku):
                        print("Error: No se permite ingresar SKU's repetidos.")
                        return obtener_sku()  # Recursividad para reintentar
                    return sku
                except ValueError:
                    error_valor_numerico("SKU")
                    return obtener_sku()  # Recursividad para reintentar
            else:
                print("Opción no válida.")
                return obtener_sku()  # Recursividad para reintentar
        
        sku = obtener_sku()
        
        # Validación de nombre con recursividad
        def obtener_nombre():
            nombre = input("Ingrese el nombre del producto: ")
            if comprobar(nombre):
                print("Error: No se permite ingresar nombres repetidos.")
                return obtener_nombre()  # Recursividad para reintentar
            return nombre
        
        nombre = obtener_nombre()
        
        # Validación de existencias con recursividad
        def obtener_existencias():
            try:
                existencias = int(input("Ingrese las existencias: "))
                if existencias <= 0:
                    print("¡Error! Las existencias deben ser mayores a 0.")
                    return obtener_existencias()  # Recursividad para reintentar
                return existencias
            except ValueError:
                error_valor_numerico("existencias")
                return obtener_existencias()  # Recursividad para reintentar
        
        existencias = obtener_existencias()
        
        # Validación de precio con recursividad
        def obtener_precio():
            try:
                precio = float(input("Ingrese el precio del producto: "))
                if precio <= 0:
                    print("¡Error! El precio debe ser mayor a 0.")
                    return obtener_precio()  # Recursividad para reintentar
                return precio
            except ValueError:
                error_valor_numerico("precio")
                return obtener_precio()  # Recursividad para reintentar
        
        precio = obtener_precio()

        # Categorías
        print("Ingrese las categorías del producto (separadas por comas, o Intro para omitir): ")
        categorias_input = input().strip()

        if categorias_input:
            categorias = [cat.strip() for cat in categorias_input.split(",") if cat.strip()]
            categorias = sorted(set(categorias))
            print(f"Categorías procesadas: {', '.join(categorias)}")
        else:
            categorias = []

        # Umbral mínimo con recursividad
        def obtener_umbral_minimo():
            try:
                umbral_minimo = int(input("Ingrese el umbral mínimo de existencias (-1 para desactivar): "))
                if umbral_minimo < -1:
                    print("¡Error! Ingrese un número válido.")
                    return obtener_umbral_minimo()  # Recursividad para reintentar
                return umbral_minimo
            except ValueError:
                error_valor_numerico("umbral mínimo")
                return obtener_umbral_minimo()  # Recursividad para reintentar
        
        umbral_minimo = obtener_umbral_minimo()

        # Umbral máximo con recursividad y validación cruzada
        def obtener_umbral_maximo():
            try:
                umbral_maximo = int(input("Ingrese el umbral máximo de existencias (-1 para desactivar): "))
                if umbral_maximo < -1:
                    print("¡Error! Ingrese un número válido.")
                    return obtener_umbral_maximo()  # Recursividad para reintentar
                if umbral_maximo != -1 and umbral_maximo < umbral_minimo:
                    print("¡Error! El umbral máximo debe ser mayor o igual al mínimo.")
                    return obtener_umbral_maximo()  # Recursividad para reintentar
                return umbral_maximo
            except ValueError:
                error_valor_numerico("umbral máximo")
                return obtener_umbral_maximo()  # Recursividad para reintentar
        
        umbral_maximo = obtener_umbral_maximo()

        # Fecha de vencimiento con recursividad
        def obtener_fecha_vencimiento():
            fecha_input = input("Ingrese fecha de vencimiento (DD-MM-AAAA), 'no' para no perecedero, o -1 para no añadir: ").strip()

            if fecha_input.lower() in ["no", "n"]:
                return "No perecedero"
            elif fecha_input == "-1":
                return "Sin vencimiento registrado"
            elif fecha_input == "":
                print("¡Error! Debe ingresar una fecha, 'no' o -1.")
                return obtener_fecha_vencimiento()  # Recursividad para reintentar
            else:
                try:
                    fecha_obj = datetime.strptime(fecha_input, "%d-%m-%Y")
                    return fecha_input
                except ValueError:
                    print("¡Error! Formato de fecha inválido. Use DD-MM-AAAA")
                    return obtener_fecha_vencimiento()  # Recursividad para reintentar
        
        fecha_vencimiento = obtener_fecha_vencimiento()

        # Lote con recursividad
        def obtener_lote():
            lote_input = input("Ingrese el número de lote (-1 para no añadir): ").strip()
            if lote_input == "-1":
                return "sin lote"
            elif lote_input == "":
                print("¡Error! El lote es obligatorio. Ingrese un lote o -1 para no añadir.")
                return obtener_lote()  # Recursividad para reintentar
            else:
                return lote_input
        
        lote = obtener_lote()

        # Proveedor con recursividad
        def obtener_proveedor():
            proveedor_input = input("Ingrese proveedor ('PROPIA' para Fabricación Propia, -1 para no añadir): ").strip()
            if proveedor_input.upper() == "PROPIA":
                return "Fabricacion Propia"
            elif proveedor_input == "-1":
                return "Sin proveedor registrado"
            elif proveedor_input == "":
                print("¡Error! Debe ingresar un proveedor, 'PROPIA' o -1.")
                return obtener_proveedor()  # Recursividad para reintentar
            else:
                return proveedor_input
        
        proveedor = obtener_proveedor()

        # Crear producto
        nuevo_producto = {
            "nombre_producto": nombre,
            "SKU": sku,
            "existencias": existencias,
            "precio": precio,
            "categorias": categorias,
            "umbral_minimo": umbral_minimo,
            "umbral_maximo": umbral_maximo,
            "fecha_vencimiento": fecha_vencimiento,
            "lote": lote,
            "proveedor": proveedor,
            "fecha_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo_control": "unidades"
        }

        # Agregar y guardar
        productos.append(nuevo_producto)
        
        # Actualizar categorías
        for categoria in categorias:
            if categoria not in data["categorias"]:
                data["categorias"].append(categoria)
        
        guardar_memory(data)
        print(" Producto ingresado correctamente.")

        # Verificar umbrales
        if existencias <= umbral_minimo and umbral_minimo > 0:
            print(" ¡Atención! El producto está por debajo del umbral mínimo.")

        if umbral_maximo > 0 and existencias > umbral_maximo:
            print(" ¡Atención! El producto supera el umbral máximo.")

        # Preguntar si desea ingresar otro producto (recursividad)
        otro = input("¿Desea ingresar otro producto? (s/n): ").strip().lower()
        if otro == 's':
            return ingresar(intentos=3)  # Recursividad para nuevo producto
        else:
            return True

    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        return False
    except Exception as e:
        print(f" Error inesperado: {e}")
        escribir_log(f"Error inesperado en ingresar: {e}", nivel="ERROR")
        
        # Recursividad para reintentar toda la operación
        reintentar = input("¿Desea reintentar el ingreso del producto? (s/n): ").strip().lower()
        if reintentar == 's':
            return ingresar(intentos - 1)  # Recursividad con un intento menos
        else:
            return False


def ingresar_paquete():
    try:
        data = cargar_memory()
        productos = data["productos"]

        sku = int(input("Ingrese el SKU: "))
        for producto in productos:
            if producto.get("SKU") == sku:
                error_ya_existe("SKU", sku)
                return False

        paquetes = int(input("Ingrese la cantidad de paquetes: "))
        while paquetes <= 0:
            paquetes = int(input("¡Error! Ingrese un numero válido.: "))

        unidades_por_paquete = int(input("Ingrese unidades por paquete: "))
        while unidades_por_paquete <= 0:
            unidades_por_paquete = int(input("¡Error! Ingrese un numero válido.: "))

        existencias = paquetes * unidades_por_paquete

        nombre = input("Ingrese el nombre del producto: ")

        for producto in productos:
            if normalizar(producto.get("nombre_producto", "")) == normalizar(nombre):
                error_ya_existe("nombre", nombre)
                return False

        print("¿El precio es por paquete o por unidad?")
        print("1. Por paquete")
        print("2. Por unidad")
        tipo_precio = input("Seleccione opción (1/2): ").strip()

        if tipo_precio == "1":
            precio_paquete = float(input("Ingrese el precio por paquete: "))
            while precio_paquete <= 0:
                precio_paquete = float(input("¡Error! Ingrese un numero válido.: "))
            precio_unitario = precio_paquete / unidades_por_paquete
        else:
            precio_unitario = float(input("Ingrese el precio por unidad: "))
            while precio_unitario <= 0:
                precio_unitario = float(input("¡Error! Ingrese un numero válido.: "))
            precio_paquete = precio_unitario * unidades_por_paquete

        print("Ingrese las categorías del producto (separadas por comas; Intro para omitir): ")
        categorias_input = input().strip()

        if categorias_input:
            categorias = [cat.strip() for cat in categorias_input.split(",") if cat.strip()]
            categorias = sorted(set(categorias))
            print(f"Categorías procesadas: {', '.join(categorias)}")
        else:
            categorias = []

        print("Configurar umbrales en:")
        print("1. Paquetes")
        print("2. Unidades")
        tipo_umbral = input("Seleccione opción (1/2): ")

        if tipo_umbral == "1":
            umbral_minimo = int(input("Ingrese el umbral mínimo de paquetes (-1 para desactivar): "))
            while umbral_minimo < -1:
                umbral_minimo = int(input("¡Error! Ingrese un número válido: "))

            umbral_maximo = int(input("Ingrese el umbral máximo de paquetes (-1 para desactivar): "))
            while umbral_maximo < -1:
                umbral_maximo = int(input("¡Error! Ingrese un número válido: "))

            tipo_control = "paquetes"
        else:
            umbral_minimo = int(input("Ingrese el umbral mínimo de unidades (-1 para desactivar): "))
            while umbral_minimo < -1:
                umbral_minimo = int(input("Error! Ingrese un número válido: "))

            umbral_maximo = int(input("Ingrese el umbral máximo de unidades (-1 para desactivar): "))
            while umbral_maximo < -1:
                umbral_maximo = int(input("Error! Ingrese un número válido: "))

            tipo_control = "unidades"

        fecha_vencimiento = None
        while True:
            fecha_input = input("Ingrese fecha de vencimiento (DD-MM-AAAA), 'no' para no perecedero, o -1 para no añadir: ").strip()

            if fecha_input.lower() in ["no", "n"]:
                fecha_vencimiento = "No perecedero"
                break
            elif fecha_input == "-1":
                fecha_vencimiento = "Sin vencimiento registrado"
                break
            elif fecha_input == "":
                print("¡Error! Debe ingresar una fecha, 'no' o -1. Intente nuevamente.")
                continue
            else:
                try:
                    fecha_obj = datetime.strptime(fecha_input, "%d-%m-%Y")
                    fecha_vencimiento = fecha_input
                    break
                except ValueError:
                    print("¡Error! Formato de fecha inválido. Use DD-MM-AAAA")

        lote = None
        while True:
            lote_input = input("Ingrese el número de lote (-1 para no añadir): ").strip()
            if lote_input == "-1":
                lote = "sin lote"
                break
            elif lote_input == "":
                print("¡Error! El lote es obligatorio. Ingrese un lote o -1 para no añadir.")
                continue
            else:
                lote = lote_input
                break

        proveedor = None
        while True:
            proveedor_input = input("Ingrese proveedor ('PROPIA' para Fabricación Propia, -1 para no añadir): ").strip()
            if proveedor_input.upper() == "PROPIA":
                proveedor = "Fabricacion Propia"
                break
            elif proveedor_input == "-1":
                proveedor = "Sin proveedor registrado"
                break
            elif proveedor_input == "":
                print("¡Error! Debe ingresar un proveedor, 'PROPIA' o -1.")
                continue
            else:
                proveedor = proveedor_input
                break

        nuevo_producto = {
            "nombre_producto": nombre,
            "SKU": sku,
            "existencias": existencias,
            "precio": precio_unitario,
            "precio_paquete": precio_paquete,
            "paquetes": paquetes,
            "unidades_por_paquete": unidades_por_paquete,
            "categorias": categorias,
            "umbral_minimo": umbral_minimo,
            "umbral_maximo": umbral_maximo,
            "fecha_vencimiento": fecha_vencimiento,
            "lote": lote,
            "proveedor": proveedor,
            "fecha_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo_control": tipo_control
        }

        productos.append(nuevo_producto)

        for categoria in categorias:
            if categoria not in data["categorias"]:
                data["categorias"].append(categoria)

        guardar_memory(data)
        print("Producto por paquete ingresado correctamente.")

        if tipo_control == "paquetes":
            if paquetes <= umbral_minimo and umbral_minimo > 0:
                print("¡Atención! Los paquetes están por debajo del umbral mínimo.")
            if umbral_maximo > 0 and paquetes > umbral_maximo:
                print("¡Atención! Los paquetes superan el umbral máximo.")
        else:
            if existencias <= umbral_minimo and umbral_minimo > 0:
                print("¡Atención! Las unidades están por debajo del umbral mínimo.")
            if umbral_maximo > 0 and existencias > umbral_maximo:
                print("¡Atención! Las unidades superan el umbral máximo.")

        return True

    except ValueError:
        print("¡Error! Ingrese valores numéricos válidos para SKU, paquetes, unidades y precio.")
        escribir_log("Error al ingresar valores numéricos en ingreso de paquete.", nivel="ERROR")
        return False
    except Exception as e:
        print(f"¡Error inesperado! {e}")
        escribir_log(f"Error inesperado en ingresar_paquete: {e}", nivel="ERROR")
        return False
    

    data = cargar_memory()
    productos = data["productos"]

    seleccion2 = normalizar(
        input("Eliminar por SKU (1), Eliminar Producto (2): "))
    match seleccion2:
        case "1" | "uno" | "sku":
            try:
                sku = int(input("Ingrese el SKU a eliminar: "))
                for i, producto in enumerate(productos):
                    if producto["sku"] == sku:
                        print(f"Producto encontrado: {producto['nombre']} (SKU: {producto['sku']})")
                        print(f"Existencias: {producto['existencias']}, Precio: ${producto['precio']:.2f}")
                        confirmar = input("Presione cualquier tecla para eliminar, 0 para modificar, -1 para cancelar: ")
                        if confirmar == "0":
                            return modificar()
                        elif confirmar == "-1":
                            return False
                        
                        productos.pop(i)
                        data["categorias"] = []
                        for prod in productos:
                            for cat in prod["categorias"]:
                                if cat not in data["categorias"]:
                                    data["categorias"].append(cat)
                        guardar_memory(data)
                        print("Producto eliminado correctamente.")
                        return True
                error_no_encontrado("SKU", sku)
                return False
            except ValueError:
                error_valor_numerico("SKU")
                return False

        case "2" | "dos" | "eliminar producto":
            nombre = normalizar(
                input("Ingrese el nombre del producto a eliminar: "))
            for i, producto in enumerate(productos):
                if normalizar(producto["nombre"]) == nombre:
                    print(f"Producto encontrado: {producto['nombre']} (SKU: {producto['sku']})")
                    print(f"Existencias: {producto['existencias']}, Precio: ${producto['precio']:.2f}")
                    confirmar = input("Presione cualquier tecla para eliminar, 0 para modificar, -1 para cancelar: ")
                    if confirmar == "0":
                        return modificar()
                    elif confirmar == "-1":
                        return False
                    
                    productos.pop(i)
                    data["categorias"] = []
                    for prod in productos:
                        for cat in prod["categorias"]:
                            if cat not in data["categorias"]:
                                data["categorias"].append(cat)
                    guardar_memory(data)
                    print("Producto eliminado correctamente.")
                    return True
            error_no_encontrado("Producto", nombre)
            return False

        case _:
            print("Error! Opción no válida.")
            return False

def modificar():
    data = cargar_memory()
    productos = data["productos"]
    
    print("\n--- MODIFICAR ---")
    print("1. Modificar SKU")
    print("2. Modificar Producto")
    print("3. Modificar Existencias")
    print("4. Modificar Precio")
    print("5. Modificar Categorías")
    print("6. Volver")
    
    seleccion2 = normalizar(input("Seleccione una opción: "))

    if seleccion2 in ["1", "uno", "modificar sku"]:
        try:
            sku_actual = int(input("Ingrese el SKU a modificar: "))
            producto_encontrado = None
            for producto in productos:
                if producto.get("SKU") == sku_actual:
                    producto_encontrado = producto
                    break
            
            if producto_encontrado:
                print(f"Producto encontrado: {producto_encontrado['nombre_producto']} (SKU: {producto_encontrado['SKU']})")
                nuevo_sku = int(input("Ingrese el nuevo SKU: "))
                
                # Verificar que el nuevo SKU no exista
                for prod in productos:
                    if prod != producto_encontrado and prod.get("SKU") == nuevo_sku:
                        error_ya_existe("SKU", nuevo_sku)
                        return False
                
                producto_encontrado["SKU"] = nuevo_sku
                guardar_memory(data)
                print("SKU modificado correctamente.")
                return True
            else:
                error_no_encontrado("SKU", sku_actual)
                return False
        except ValueError:
            error_valor_numerico("SKU")
            return False

    elif seleccion2 in ["2", "dos", "modificar producto"]:
        nombre_actual = input("Ingrese el nombre del producto a modificar: ")
        producto_encontrado = None
        for producto in productos:
            if normalizar(producto.get("nombre_producto", "")) == normalizar(nombre_actual):
                producto_encontrado = producto
                break
        
        if producto_encontrado:
            print(f"Producto encontrado: {producto_encontrado['nombre_producto']} (SKU: {producto_encontrado['SKU']})")
            nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
            
            # Verificar que el nuevo nombre no exista
            for prod in productos:
                if prod != producto_encontrado and normalizar(prod.get("nombre_producto", "")) == normalizar(nuevo_nombre):
                    error_ya_existe("nombre", nuevo_nombre)
                    return False
            
            producto_encontrado["nombre_producto"] = nuevo_nombre
            guardar_memory(data)
            print("Producto modificado correctamente.")
            return True
        else:
            error_no_encontrado("Producto", nombre_actual)
            return False

    elif seleccion2 in ["3", "tres", "modificar existencias"]:
        try:
            sku = int(input("Ingrese el SKU del producto cuyas existencias desea modificar: "))
            producto_encontrado = None
            for producto in productos:
                if producto.get("SKU") == sku:
                    producto_encontrado = producto
                    break
            
            if producto_encontrado:
                print(f"Producto encontrado: {producto_encontrado['nombre_producto']} (SKU: {producto_encontrado['SKU']})")
                nuevas_existencias = int(input("Ingrese las nuevas existencias: "))
                if nuevas_existencias <= 0:
                    print("¡Error! Las existencias deben ser mayores a 0.")
                    return False
                producto_encontrado["existencias"] = nuevas_existencias
                guardar_memory(data)
                print("Existencias modificadas correctamente.")
                return True
            else:
                error_no_encontrado("SKU", sku)
                return False
        except ValueError:
            error_valor_numerico("existencias")
            return False

    elif seleccion2 in ["4", "cuatro", "modificar precio"]:
        try:
            mod_busqueda = normalizar(input("Buscar por SKU (1) o Producto (2): "))
            if mod_busqueda in ["sku", "1", "uno"]:
                sku = int(input("Ingrese el SKU del producto cuyo precio desea modificar: "))
                producto_encontrado = None
                for producto in productos:
                    if producto.get("SKU") == sku:
                        producto_encontrado = producto
                        break
                
                if producto_encontrado:
                    print(f"Producto encontrado: {producto_encontrado['nombre_producto']} (SKU: {producto_encontrado['SKU']})")
                    nuevo_precio = float(input("Ingrese el nuevo precio: "))
                    if nuevo_precio <= 0:
                        print("¡Error! El precio debe ser mayor a 0.")
                        return False
                    producto_encontrado["precio"] = nuevo_precio
                    guardar_memory(data)
                    print("Precio modificado correctamente.")
                    return True
                else:
                    error_no_encontrado("SKU", sku)
                    return False

            elif mod_busqueda in ["producto", "2", "dos"]:
                nombre = input("Ingrese el nombre del producto cuyo precio desea modificar: ")
                producto_encontrado = None
                for producto in productos:
                    if normalizar(producto.get("nombre_producto", "")) == normalizar(nombre):
                        producto_encontrado = producto
                        break
                
                if producto_encontrado:
                    print(f"Producto encontrado: {producto_encontrado['nombre_producto']} (SKU: {producto_encontrado['SKU']})")
                    nuevo_precio = float(input("Ingrese el nuevo precio: "))
                    if nuevo_precio <= 0:
                        print("Error! El precio debe ser mayor a 0.")
                        return False
                    producto_encontrado["precio"] = nuevo_precio
                    guardar_memory(data)
                    print("Precio modificado correctamente.")
                    return True
                else:
                    error_no_encontrado("Producto", nombre)
                    return False
            else:
                print("Error! Opción no válida.")
                return False

        except ValueError:
            error_valor_numerico("precio")
            return False

    elif seleccion2 in ["5", "cinco", "modificar categorías"]:
        try:
            sku = int(input("Ingrese el SKU del producto cuyas categorías desea modificar: "))
            producto_encontrado = None
            for producto in productos:
                if producto.get("SKU") == sku:
                    producto_encontrado = producto
                    break
            
            if producto_encontrado:
                print(f"Producto encontrado: {producto_encontrado['nombre_producto']} (SKU: {producto_encontrado['SKU']})")
                print(f"Categorías actuales: {', '.join(producto_encontrado['categorias']) if producto_encontrado['categorias'] else 'Ninguna'}")
                print("Ingrese las nuevas categorías (separadas por comas, o Intro para eliminar todas): ")
                categorias_input = input().strip()
                nuevas_categorias = [cat.strip() for cat in categorias_input.split(",") if cat.strip()] if categorias_input else []

                producto_encontrado["categorias"] = nuevas_categorias

                # Actualizar lista global de categorías
                data["categorias"] = []
                for prod in productos:
                    for cat in prod["categorias"]:
                        if cat not in data["categorias"]:
                            data["categorias"].append(cat)

                guardar_memory(data)
                print("Categorías modificadas correctamente.")
                return True
            else:
                error_no_encontrado("SKU", sku)
                return False
        except ValueError:
            error_valor_numerico("SKU")
            return False

    elif seleccion2 in ["6", "seis", "volver"]:
        return True

    else:
        print("¡Error! Opción no válida.")
        return False

def eliminar():
    data = cargar_memory()
    productos = data["productos"]
    
    print("\n--- ELIMINAR ---")
    print("1. Eliminar por SKU")
    print("2. Eliminar por Producto")
    print("3. Volver")
    
    seleccion2 = normalizar(input("Seleccione una opción: "))

    if seleccion2 in ["1", "uno", "sku"]:
        try:
            sku = int(input("Ingrese el SKU a eliminar: "))
            for i, producto in enumerate(productos):
                if producto.get("SKU") == sku:
                    print(f"Producto encontrado: {producto['nombre_producto']} (SKU: {producto['SKU']})")
                    confirmar = input("¿Está seguro de eliminar? (s/n): ")
                    if confirmar.lower() == 's':
                        productos.pop(i)
                        # Actualizar categorías globales
                        data["categorias"] = []
                        for prod in productos:
                            for cat in prod["categorias"]:
                                if cat not in data["categorias"]:
                                    data["categorias"].append(cat)
                        guardar_memory(data)
                        print("Producto eliminado correctamente.")
                        return True
                    else:
                        print("Eliminación cancelada.")
                        return False
            error_no_encontrado("SKU", sku)
            return False
        except ValueError:
            error_valor_numerico("SKU")
            return False

    elif seleccion2 in ["2", "dos", "eliminar producto"]:
        nombre = normalizar(input("Ingrese el nombre del producto a eliminar: "))
        for i, producto in enumerate(productos):
            if normalizar(producto.get("nombre_producto", "")) == nombre:
                print(f"Producto encontrado: {producto['nombre_producto']} (SKU: {producto['SKU']})")
                confirmar = input("¿Está seguro de eliminar? (s/n): ")
                if confirmar.lower() == 's':
                    productos.pop(i)
                    # Actualizar categorías globales
                    data["categorias"] = []
                    for prod in productos:
                        for cat in prod["categorias"]:
                            if cat not in data["categorias"]:
                                data["categorias"].append(cat)
                    guardar_memory(data)
                    print("Producto eliminado correctamente.")
                    return True
                else:
                    print("Eliminación cancelada.")
                    return False
        error_no_encontrado("Producto", nombre)
        return False

    elif seleccion2 in ["3", "tres", "volver"]:
        return True

    else:
        print("Error! Opción no válida.")
        return False

def gestionar_categoria_modo(modo=None):
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
            error_ya_existe("categoría", nueva_categoria)
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
            for producto in data["productos"]:
                if categoria_eliminar in producto["categorias"]:
                    producto["categorias"].remove(categoria_eliminar)
            guardar_memory(data)
            print("Categoría eliminada correctamente.")
            return True
        else:
            error_no_encontrado("Categoría", categoria_eliminar)
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
            data["categorias"].remove(categoria_actual)
            data["categorias"].append(nueva_categoria)
            for producto in data["productos"]:
                if categoria_actual in producto["categorias"]:
                    index = producto["categorias"].index(categoria_actual)
                    producto["categorias"][index] = nueva_categoria
            guardar_memory(data)
            print("Categoría modificada correctamente.")
            return True
        else:
            error_no_encontrado("Categoría", categoria_actual)
            return False

    else:
        seleccion = normalizar(input("""Gestionar categorías:
        1. Ver todas las categorías
        2. Ingresar categoría
        3. Eliminar categoría
        4. Modificar categoría
        5. Volver
    Seleccione una opción: """))

        match seleccion:
            case "1" | "uno" | "ver categorías":
                if data["categorias"]:
                    print("Categorías disponibles:")
                    for i, cat in enumerate(data["categorias"], 1):
                        print(f"  {i}. {cat}")
                else:
                    print("No hay categorías registradas.")
                return True

            case "2" | "dos" | "ingresar categoría":
                nueva_categoria = input("Ingrese la nueva categoría: ")
                if nueva_categoria in data["categorias"]:
                    error_ya_existe("categoría", nueva_categoria)
                    return False
                data["categorias"].append(nueva_categoria)
                guardar_memory(data)
                print("Categoría ingresada correctamente.")
                return True

            case "3" | "tres" | "eliminar categoría":
                if not data["categorias"]:
                    print("No hay categorías para eliminar.")
                    return False

                print("Categorías disponibles:")
                for i, cat in enumerate(data["categorias"], 1):
                    print(f"  {i}. {cat}")

                categoria_eliminar = input("Ingrese la categoría a eliminar: ")
                if categoria_eliminar in data["categorias"]:
                    data["categorias"].remove(categoria_eliminar)
                    for producto in data["productos"]:
                        if categoria_eliminar in producto["categorias"]:
                            producto["categorias"].remove(categoria_eliminar)
                    guardar_memory(data)
                    print("Categoría eliminada correctamente.")
                    return True
                else:
                    error_no_encontrado("Categoría", categoria_eliminar)
                    return False

            case "4" | "cuatro" | "modificar categoría":
                if not data["categorias"]:
                    print("No hay categorías para modificar.")
                    return False

                print("Categorías disponibles:")
                for i, cat in enumerate(data["categorias"], 1):
                    print(f"  {i}. {cat}")

                categoria_actual = input("Ingrese la categoría a modificar: ")
                if categoria_actual in data["categorias"]:
                    nueva_categoria = input("Ingrese la nueva categoría: ")
                    data["categorias"].remove(categoria_actual)
                    data["categorias"].append(nueva_categoria)
                    for producto in data["productos"]:
                        if categoria_actual in producto["categorias"]:
                            index = producto["categorias"].index(
                                categoria_actual)
                            producto["categorias"][index] = nueva_categoria
                    guardar_memory(data)
                    print("Categoría modificada correctamente.")
                    return True
                else:
                    error_no_encontrado("Categoría", categoria_actual)
                    return False

            case "5" | "cinco" | "volver":
                return False

            case _:
                print("Error! Opción no válida.")
                return False


def verificar_umbral_minimo():
    data = cargar_memory()
    productos_bajo_umbral = []

    for producto in data["productos"]:
        umbral = producto.get("umbral_minimo", 0)
        if producto["existencias"] <= umbral:
            productos_bajo_umbral.append(producto)

    if productos_bajo_umbral:
        print("Productos por debajo del umbral mínimo:")
        for prod in productos_bajo_umbral:
            umbral = prod.get("umbral_minimo", 0)
            print(
                f"{prod['nombre']} (SKU: {prod['sku']}): {prod['existencias']} existencias (Umbral: {umbral})")
        escribir_log(
            f"Alertas de umbral mínimo: {len(productos_bajo_umbral)} productos", nivel="WARNING")
    else:
        print("Todos los productos están por encima del umbral mínimo.")

    return productos_bajo_umbral


def verificar_sobre_almacenamiento():
    data = cargar_memory()
    productos_sobre_almacenamiento = []

    for producto in data["productos"]:
        umbral_maximo = producto.get("umbral_maximo", 0)
        if umbral_maximo > 0 and producto["existencias"] > umbral_maximo:
            productos_sobre_almacenamiento.append(producto)

    if productos_sobre_almacenamiento:
        print("Productos con sobre almacenamiento:")
        for prod in productos_sobre_almacenamiento:
            umbral_maximo = prod.get("umbral_maximo", 0)
            print(
                f"{prod['nombre']} (SKU: {prod['sku']}): {prod['existencias']} existencias (Umbral máximo: {umbral_maximo})")
        escribir_log(
            f"Alertas de sobre almacenamiento: {len(productos_sobre_almacenamiento)} productos", nivel="WARNING")
    else:
        print("No hay productos con sobre almacenamiento.")

    return productos_sobre_almacenamiento


def configurar_umbral_minimo():
    data = cargar_memory()

    try:
        sku = int(input("Ingrese el SKU del producto: "))

        for producto in data["productos"]:
            if producto["sku"] == sku:
                print(f"Producto: {producto['nombre']}")
                print(f"Existencias actuales: {producto['existencias']}")
                umbral_actual = producto.get("umbral_minimo", "No configurado")
                print(f"Umbral actual: {umbral_actual}")

                nuevo_umbral = int(
                    input("Ingrese el nuevo umbral mínimo (0 para desactivar): "))

                if nuevo_umbral < 0:
                    print("¡Error! El umbral no puede ser negativo.")
                    return False

                producto["umbral_minimo"] = nuevo_umbral
                guardar_memory(data)

                if nuevo_umbral == 0:
                    print("Umbral mínimo desactivado para este producto.")
                    escribir_log(
                        f"Umbral desactivado para SKU {sku}", nivel="INFO")
                else:
                    print(f"Umbral mínimo configurado en {nuevo_umbral}.")
                    escribir_log(
                        f"Umbral configurado para SKU {sku}: {nuevo_umbral}", nivel="INFO")

                    if producto["existencias"] <= nuevo_umbral:
                        print(
                            "¡Advertencia! El producto está por debajo del nuevo umbral.")

                return True

        error_no_encontrado("SKU", sku)
        return False

    except ValueError:
        error_valor_numerico("umbral")
        return False


def configurar_umbral_maximo():
    data = cargar_memory()

    try:
        sku = int(input("Ingrese el SKU del producto: "))

        for producto in data["productos"]:
            if producto["sku"] == sku:
                print(f"Producto: {producto['nombre']}")
                print(f"Existencias actuales: {producto['existencias']}")
                umbral_actual = producto.get("umbral_maximo", "No configurado")
                print(f"Umbral máximo actual: {umbral_actual}")

                nuevo_umbral = int(
                    input("Ingrese el nuevo umbral máximo (-1 para desactivar): "))

                if nuevo_umbral < -1:
                    print("¡Error! El umbral no puede ser negativo.")
                    return False

                producto["umbral_maximo"] = nuevo_umbral
                guardar_memory(data)

                if nuevo_umbral == 0:
                    print("Umbral máximo desactivado para este producto.")
                    escribir_log(
                        f"Umbral máximo desactivado para SKU {sku}", nivel="INFO")
                else:
                    print(f"Umbral máximo configurado en {nuevo_umbral}.")
                    escribir_log(
                        f"Umbral máximo configurado para SKU {sku}: {nuevo_umbral}", nivel="INFO")

                    if producto["existencias"] > nuevo_umbral:
                        print(
                            "¡Advertencia! El producto supera el nuevo umbral máximo.")

                return True

        error_no_encontrado("SKU", sku)
        return False

    except ValueError:
        error_valor_numerico("umbral")
        return False


def existencias_sin_stock():
    data = cargar_memory()
    productos = data["productos"]

    sin_stock = [prod for prod in productos if prod["existencias"] == 0]

    if sin_stock:
        print("Productos sin existencias:")
        for prod in sin_stock:
            print(f"{prod['nombre']} (SKU: {prod['sku']})")
            print(f"Total: {len(sin_stock)} productos")
    else:
        print("No hay productos sin existencias.")

    escribir_log(
        f"Consultados productos sin stock: {len(sin_stock)}", nivel="INFO")
    return len(sin_stock) > 0

def productos_por_categoria():
    data = cargar_memory()
    productos = data["productos"]
    categorias = data["categorias"]

    if not categorias:
        print("No hay categorías definidas.")
        return False

    print("Productos por categoría")
    print("=" * 40)

    for categoria in categorias:
        productos_cat = [
            prod for prod in productos if categoria in prod["categorias"]]
        total_existencias = sum(prod["existencias"] for prod in productos_cat)
        valor_categoria = sum(prod["precio"] * prod["existencias"]
                              for prod in productos_cat)

        print(f"\n{categoria}:")
        print(f"Productos: {len(productos_cat)}")
        print(f"Existencias: {total_existencias}")
        print(f"Valor: ${valor_categoria:,.2f}")

    escribir_log("Consultados productos por categoría", nivel="INFO")
    return True

def distribucion_precios():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario.")
        return False

    precios = [prod["precio"] for prod in productos]

    rangos = {
        "$0 - $10": 0,
        "$10 - $50": 0,
        "$50 - $100": 0,
        "$100 - $500": 0,
        "$500 - $1.000": 0,
        "$1.000 - $5.000": 0,
        "$5.000 - $20.000": 0,
        "$20.000 - $50.000": 0,
        "$50.000 - $100.000": 0,
        "+$100.000": 0,
    }

    for precio in precios:
        if precio <= 10:
            rangos["$0 - $10"] += 1
        elif precio <= 50:
            rangos["$10 - $50"] += 1
        elif precio <= 100:
            rangos["$50 - $100"] += 1
        elif precio <= 500:
            rangos["$100 - $500"] += 1
        elif precio <= 1000:
            rangos["$500 - $1.000"] += 1
        elif precio <= 5000:
            rangos["$1.000 - $5.000"] += 1
        elif precio <= 20000:
            rangos["$5.000 - $20.000"] += 1
        elif precio <= 50000:
            rangos["$20.000 - $50.000"] += 1
        elif precio <= 100000:
            rangos["$50.000 - $100.000"] += 1
        else:
            rangos["+$100.000"] += 1

    print("Distribución de Precios")
    print("=" * 40)
    for rango, cantidad in rangos.items():
        porcentaje = (cantidad / len(productos)) * 100
        print(f"{rango}: {cantidad} productos ({porcentaje:.1f}%)")

    escribir_log("Consultada distribución de precios", nivel="INFO")
    return True

def versionGS():
    print("""
╔══════════════════════════════════════════════╗
║          INFORMACIÓN DEL PROGRAMA            ║
╠══════════════════════════════════════════════╣
║       Sistema de Gestión de Inventarios      ║
║                                              ║
║  Desarrollado por: GRUPO 8                   ║
║  Versión: 1.1                                ║
║  Integrantes:                                ║
║       Lioy, Santiago;                        ║
║       Alaniz, Ramiro;                        ║
║       Fernandez, Maximiliano                 ║
╚══════════════════════════════════════════════╝
    """)
    escribir_log("Consultada versión del programa", nivel="INFO")
    return True


def formatearDB():
    confirmacion = normalizar(input("¿Desea formatear la base de datos? Esta acción es irreversible. (ingrese 'CONFIRMAR' para continuar): "))

    if confirmacion == "confirmar":
        data = {
            "productos": [],
            "categorias": []
        }
        guardar_memory(data)
        print("Información: Base de datos formateada correctamente.")
        escribir_log("Base de datos formateada", nivel="CRITICAL")
        return True
    else:
        print("¡Error! La operación fue cancelada.")
        return False


def verificar_vencimientos_proximos():
    data = cargar_memory()
    productos = data["productos"]

    hoy = datetime.now().date()
    productos_proximos_vencer = []

    for producto in productos:
        fecha_vencimiento = producto.get("fecha_vencimiento")
        if fecha_vencimiento and fecha_vencimiento != "No perecedero":
            try:
                fecha_venc = datetime.strptime(
                    fecha_vencimiento, "%Y-%m-%d").date()
                dias_restantes = (fecha_venc - hoy).days

                if 0 <= dias_restantes <= 30:
                    productos_proximos_vencer.append(
                        (producto, dias_restantes))
            except ValueError:
                continue

    if productos_proximos_vencer:
        print("Productos próximos a vencer:")
        for producto, dias in productos_proximos_vencer:
            print(
                f"«{producto['nombre']}» (SKU: {producto['sku']}) - Vence en {dias} días - {producto['fecha_vencimiento']}")
        escribir_log(
            f"Alertas de vencimiento: {len(productos_proximos_vencer)} productos", nivel="WARNING")
    else:
        print("No hay productos próximos a vencer.")

    return productos_proximos_vencer


def verificar_vencidos():
    data = cargar_memory()
    productos = data["productos"]

    hoy = datetime.now().date()
    productos_vencidos = []

    for producto in productos:
        if es_producto_vencido(producto):
            productos_vencidos.append(producto)

    if productos_vencidos:
        print("Productos vencidos:")
        for producto in productos_vencidos:
            lote_info = f" - Lote: {producto.get('lote', 'Sin lote')}" if producto.get(
                'lote') else ""
            print(
                f"«{producto['nombre']}» (SKU: {producto['sku']}){lote_info} - Vencido el {producto['fecha_vencimiento']}")
        escribir_log(
            f"Productos vencidos: {len(productos_vencidos)}", nivel="ERROR")
    else:
        print("No hay productos vencidos.")

    return productos_vencidos


def ver_productos_no_perecederos():
    data = cargar_memory()
    productos = data["productos"]

    productos_no_perecederos = []

    for producto in productos:
        fecha_vencimiento = producto.get("fecha_vencimiento")
        if not fecha_vencimiento or fecha_vencimiento == "No perecedero":
            productos_no_perecederos.append(producto)

    if productos_no_perecederos:
        print("Productos no perecederos:")
        for producto in productos_no_perecederos:
            print(
                f"«{producto['nombre']}» (SKU: {producto['sku']}) - Existencias: {producto['existencias']}")
        print(
            f"Total: {len(productos_no_perecederos)} productos no perecederos")
    else:
        print("No hay productos no perecederos.")

    escribir_log(
        f"Consultados productos no perecederos: {len(productos_no_perecederos)}", nivel="INFO")
    return productos_no_perecederos


def configurar_alerta_vencimiento():
    data = cargar_memory()

    try:
        sku = int(input("Ingrese el SKU del producto: "))

        for producto in data["productos"]:
            if producto["sku"] == sku:
                print(f"Producto: {producto['nombre']}")
                fecha_actual = producto.get(
                    "fecha_vencimiento", "No configurada")
                print(f"Fecha de vencimiento actual: {fecha_actual}")

                alerta_actual = producto.get(
                    "dias_alerta_vencimiento", "No configurada")
                print(f"Días de alerta actual: {alerta_actual}")

                if not fecha_actual or fecha_actual == "No perecedero":
                    print(
                        "¡Error! Este producto no tiene fecha de vencimiento configurada.")
                    return False

                nuevos_dias = int(
                    input("Ingrese los días de anticipación para la alerta: "))

                if nuevos_dias < 0:
                    print("¡Error! Los días no pueden ser negativos.")
                    return False

                producto["dias_alerta_vencimiento"] = nuevos_dias
                guardar_memory(data)

                print(
                    f"Alerta configurada: {nuevos_dias} días de anticipación.")
                escribir_log(
                    f"Alerta de vencimiento configurada para SKU {sku}: {nuevos_dias} días", nivel="INFO")
                return True

        error_no_encontrado("SKU", sku)
        return False

    except ValueError:
        error_valor_numerico("días de alerta")
        return False


def verificar_alertas_vencimiento():
    data = cargar_memory()
    productos = data["productos"]

    hoy = datetime.now().date()
    productos_con_alerta = []

    for producto in productos:
        fecha_vencimiento = producto.get("fecha_vencimiento")
        dias_alerta = producto.get("dias_alerta_vencimiento", 7)

        if fecha_vencimiento and fecha_vencimiento != "No perecedero":
            try:
                fecha_venc = datetime.strptime(
                    fecha_vencimiento, "%Y-%m-%d").date()
                dias_restantes = (fecha_venc - hoy).days

                if 0 <= dias_restantes <= dias_alerta:
                    productos_con_alerta.append(
                        (producto, dias_restantes, dias_alerta))
            except ValueError:
                continue

    if productos_con_alerta:
        print("Alertas de vencimiento personalizadas:")
        for producto, dias_restantes, dias_alerta in productos_con_alerta:
            print(f"«{producto['nombre']}» (SKU: {producto['sku']})")
            print(f"Vence en {dias_restantes} días")
            print(f"Alerta configurada: {dias_alerta} días de anticipación")
            print(f"Fecha: {producto['fecha_vencimiento']}")
            print()
        escribir_log(
            f"Alertas de vencimiento personalizadas: {len(productos_con_alerta)} productos", nivel="WARNING")
    else:
        print("No hay alertas de vencimiento activas.")

    return productos_con_alerta


def ver_todas_alertas_vencimiento():
    data = cargar_memory()
    productos = data["productos"]

    productos_con_alerta = []
    productos_sin_alerta = []

    for producto in productos:
        fecha_vencimiento = producto.get("fecha_vencimiento")
        dias_alerta = producto.get("dias_alerta_vencimiento")

        if fecha_vencimiento and fecha_vencimiento != "No perecedero":
            if dias_alerta is not None:
                productos_con_alerta.append((producto, dias_alerta))
            else:
                productos_sin_alerta.append(producto)

    if productos_con_alerta:
        print("Productos con alertas de vencimiento configuradas:")
        for producto, dias_alerta in productos_con_alerta:
            print(
                f"«{producto['nombre']}» (SKU: {producto['sku']}) - {dias_alerta} días de anticipación")
        print()

    if productos_sin_alerta:
        print("Productos con fecha de vencimiento pero sin alerta configurada:")
        for producto in productos_sin_alerta:
            print(
                f"«{producto['nombre']}» (SKU: {producto['sku']}) - Fecha: {producto['fecha_vencimiento']}")
        print()

    if not productos_con_alerta and not productos_sin_alerta:
        print("No hay productos con fecha de vencimiento configurada.")

    escribir_log(
        "Consultadas configuraciones de alertas de vencimiento", nivel="INFO")
    return productos_con_alerta


def ver_todos_lotes():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario.")
        return False

    lotes = {}
    for producto in productos:
        lote = producto.get("lote", "Sin lote")
        if lote not in lotes:
            lotes[lote] = []
        lotes[lote].append(producto)

    print("Lotes en inventario:")
    for lote, productos_lote in lotes.items():
        print(f"\nLote: {lote}")
        print(f"Cantidad de productos: {len(productos_lote)}")
        for prod in productos_lote:
            estado = "VENCIDO" if es_producto_vencido(prod) else "VIGENTE"
            categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
            proveedor = prod.get("proveedor", "No registrado")
            print(f"  - {prod['nombre']} (SKU: {prod['sku']})")
            print(f"    Existencias: {prod['existencias']} - Precio: ${prod['precio']:.2f}")
            print(f"    Categorías: {categorias_str}")
            print(f"    Proveedor: {proveedor}")
            print(f"    Vence: {prod.get('fecha_vencimiento', 'No perecedero')} - {estado}")

    escribir_log("Consultados todos los lotes", nivel="INFO")
    return True


def buscar_por_lote():
    data = cargar_memory()
    productos = data["productos"]

    lote_buscar = input("Ingrese el número de lote a buscar: ").strip()

    productos_lote = [prod for prod in productos if prod.get(
        "lote", "").lower() == lote_buscar.lower()]

    if productos_lote:
        print(f"Productos del lote '{lote_buscar}':")
        for prod in productos_lote:
            estado = "VENCIDO" if es_producto_vencido(prod) else "VIGENTE"
            categorias_str = ", ".join(prod["categorias"]) if prod["categorias"] else "Sin categorías"
            proveedor = prod.get("proveedor", "No registrado")
            print(f"  - {prod['nombre']} (SKU: {prod['sku']})")
            print(f"    Existencias: {prod['existencias']} - Precio: ${prod['precio']:.2f}")
            print(f"    Categorías: {categorias_str}")
            print(f"    Proveedor: {proveedor}")
            print(f"    Lote: {prod.get('lote', 'Sin lote')}")
            print(f"    Vence: {prod.get('fecha_vencimiento', 'No perecedero')} - {estado}")
    else:
        print(f"No se encontraron productos del lote '{lote_buscar}'")

    escribir_log(f"Búsqueda de lote: {lote_buscar}", nivel="INFO")
    return len(productos_lote) > 0


def configurar_metodo_salida():
    """Configura el método de salida de productos (FIFO/LIFO)"""
    data = cargar_memory()

    print("""
Métodos de salida disponibles:
1. FIFO (Primero en Entrar, Primero en Salir)
2. LIFO (Último en Entrar, Primero en Salir)
""")

    metodo = input("Seleccione el método (1/2): ").strip()

    metodos = {
        "1": "FIFO",
        "2": "LIFO"
    }

    if metodo in metodos:
        data["metodo_salida"] = metodos[metodo]
        guardar_memory(data)
        print(f"Método de salida configurado como: {metodos[metodo]}")
        escribir_log(f"Método de salida configurado: {metodos[metodo]}", nivel="INFO")
        return True


def ver_proximo_vencer_lotes():
    data = cargar_memory()
    productos = data["productos"]

    hoy = datetime.now().date()
    lotes_proximos = {}

    for producto in productos:
        fecha_vencimiento = producto.get("fecha_vencimiento")
        if fecha_vencimiento and fecha_vencimiento != "No perecedero":
            try:
                fecha_venc = datetime.strptime(
                    fecha_vencimiento, "%Y-%m-%d").date()
                dias_restantes = (fecha_venc - hoy).days

                if 0 <= dias_restantes <= 30:
                    lote = producto.get("lote", "Sin lote")
                    if lote not in lotes_proximos:
                        lotes_proximos[lote] = []
                    lotes_proximos[lote].append((producto, dias_restantes))
            except ValueError:
                continue

    if lotes_proximos:
        print("Lotes próximos a vencer (próximos 30 días):")
        for lote, productos_lote in lotes_proximos.items():
            print(f"\nLote: {lote}")
            for producto, dias in productos_lote:
                print(f"  - {producto['nombre']} (SKU: {producto['sku']})")
                print(f"    Existencias: {producto['existencias']} - Lote: {producto.get('lote', 'Sin lote')}")
                print(f"    Vence en {dias} días - Fecha: {producto['fecha_vencimiento']}")
    else:
        print("No hay lotes próximos a vencer.")

    escribir_log("Consultados lotes próximos a vencer", nivel="INFO")
    return len(lotes_proximos) > 0

def es_producto_vencido(producto):
    fecha_vencimiento = producto.get("fecha_vencimiento")
    if not fecha_vencimiento or fecha_vencimiento == "No perecedero":
        return False

    try:
        fecha_venc = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()
        hoy = datetime.now().date()
        return fecha_venc < hoy
    except ValueError:
        return False

def ver_sin_vencimiento_registrado():
    data = cargar_memory()
    productos = data["productos"]
    
    productos_sin_registro = [prod for prod in productos if prod.get("fecha_vencimiento") == "Sin vencimiento registrado"]
    
    if productos_sin_registro:
        print("Productos sin vencimiento registrado:")
        for producto in productos_sin_registro:
            print(f"«{producto['nombre']}» (SKU: {producto['sku']}) - Existencias: {producto['existencias']}")
        print(f"Total: {len(productos_sin_registro)} productos")
    else:
        print("No hay productos sin vencimiento registrado.")
    
    escribir_log(f"Consultados productos sin vencimiento registrado: {len(productos_sin_registro)}", nivel="INFO")
    return productos_sin_registro

def obtener_producto_por_metodo_salida(productos):
    data = cargar_memory()
    metodo = data.get("metodo_salida", "FIFO")

    if not productos:
        return None

    if metodo == "LIFO":
        return productos[-1]
    else:
        productos_ordenados = sorted(productos, key=lambda x: x.get("fecha_ingreso", ""))
        return productos_ordenados[0] if productos_ordenados else None

def generador_de_sku():
    data = cargar_memory()
    productos = data["productos"]
    if productos:
        max_sku = max(producto.get("SKU", 0) for producto in productos)
        return max_sku + 1
    else:
        return 1


def gestionar_proveedores():
    data = cargar_memory()
    
    print("1. Ver todos los proveedores")
    print("2. Buscar productos por proveedor")
    print("3. Volver")
    
    opcion = input("Seleccione una opción: ").strip()
    
    if opcion == "1":
        proveedores = set()
        for producto in data["productos"]:
            proveedores.add(producto.get("proveedor", "Sin proveedor registrado"))
        
        if proveedores:
            print("Proveedores en el sistema:")
            for i, prov in enumerate(sorted(proveedores), 1):
                print(f"  {i}. {prov}")
        else:
            print("No hay proveedores registrados.")
            
    elif opcion == "2":
        proveedor_buscar = input("Ingrese el proveedor a buscar: ").strip()
        productos_proveedor = [prod for prod in data["productos"] if prod.get("proveedor", "").lower() == proveedor_buscar.lower()]
        
        if productos_proveedor:
            print(f"Productos del proveedor '{proveedor_buscar}':")
            for prod in productos_proveedor:
                print(f"  - {prod['nombre_producto']} (SKU: {prod['SKU']}) - Existencias: {prod['existencias']}")
        else:
            print(f"No se encontraron productos del proveedor '{proveedor_buscar}'")
    
    elif opcion == "3":
        return True
    
    else:
        print("Opción no válida.")
    
    return True


def exit_program():
    print("¡Gracias por usar el storage management system! Hasta luego.")
    raise SystemExit
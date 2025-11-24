import json
from datetime import datetime


def escribir_log(mensaje, nivel="INFO"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('loginventario.txt', 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} - {nivel} - {mensaje}\n")
    except Exception as e:
        print(f"¡Error! No se puedo escribir en el log.: {e}")


def cargar_memory():
    try:
        with open('memory.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "clientes" not in data:
                data["clientes"] = []
            if "proveedores" not in data:
                data["proveedores"] = []
            if "productos" not in data or "categorias" not in data:
                raise ValueError("Estructura de archivo inválida")
            return data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        data = {
            "productos": [],
            "categorias": [],
            "clientes": [],
            "proveedores": []
        }
        guardar_memory(data)

        if isinstance(e, FileNotFoundError):
            escribir_log(
                "Advertencia! memory.json no encontrado. Se generó un nuevo archivo.", nivel="WARNING")
        elif isinstance(e, json.JSONDecodeError):
            escribir_log(
                "Error! Problemas de decodificación JSON. Se reinició el archivo.", nivel="ERROR")
        else:
            escribir_log(
                f"Error! No se pudo cargar memory.json: {e}", nivel="ERROR")

        return data


def guardar_memory(data):
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
    data = cargar_memory()
    productos = data["productos"]
    encuentro = False
    seleccion = normalizar(input("Seleccione una opción:"))

    match seleccion:
        case "1" | "uno" | "buscar sku":
            try:
                sku = int(input("Ingrese el SKU a buscar: "))
                for producto in productos:
                    if producto["sku"] == sku:
                        categorias_str = ", ".join(
                            producto["categorias"]) if producto["categorias"] else "Sin categorías"
                        print(
                            f"El SKU Nº {sku} corresponde al producto «{producto['nombre']}», tiene {producto['existencias']} existencia(s), un precio de ${producto['precio']:.2f} y categorías: «{categorias_str}».")
                        encuentro = True
                if encuentro == False:
                    sugerencias = sorted(
                        productos, key=lambda x: abs(x["sku"] - sku))[:3]
                    if sugerencias:
                        print(
                            "SKU no encontrado. ¿Quizá buscaba alguno de los siguientes?:")
                        for prod in sugerencias:
                            categorias_str = ", ".join(
                                prod["categorias"]) if prod["categorias"] else "Sin categorías."
                            print(
                                f"SKU Nº {prod['sku']}: «{prod['nombre']}», ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: «{categorias_str}»)")
                    else:
                        error_no_encontrado("SKU", sku)
                # return False
            except ValueError:
                error_valor_numerico("SKU")
                return False

        case "2" | "dos" | "buscar producto":
            consulta = input("Ingrese el nombre del producto a buscar: ")
            consulta_norm = normalizar(consulta)
            for producto in productos:
                if normalizar(producto["nombre"]) == consulta_norm:
                    categorias_str = ", ".join(
                        producto["categorias"]) if producto["categorias"] else "Sin categorías"
                    print(
                        f"El producto «{producto['nombre']}» tiene SKU Nº {producto['sku']}, {producto['existencias']} existencia(s), precio de ${producto['precio']:.2f} y categorías: «{categorias_str}».")
                    encuentro = True

            if encuentro == False:
                resultados = []
                for producto in productos:
                    sim = similitud(consulta_norm, producto["nombre"])
                    if sim >= 0.4 or consulta_norm in normalizar(producto["nombre"]):
                        resultados.append((sim, producto))
                if resultados:
                    print("Producto exacto no encontrado. ¿Quizá quiso decir?:")
                    for sim, prod in sorted(resultados, reverse=True):
                        categorias_str = ", ".join(
                            prod["categorias"]) if prod["categorias"] else "Sin categorías"
                        print(
                            f"«{prod['nombre']}», (SKU Nº {prod['sku']}, {prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: «{categorias_str}»)")
                else:
                    error_no_encontrado("Producto", consulta)

        case "3" | "tres" | "buscar cantidad":
            modo = normalizar(
                input("Buscar por cantidad: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            try:
                if modo in ("igual", "1", "iguales"):
                    q = int(input("Ingrese la cantidad exacta: "))
                    encontrados = [
                        prod for prod in productos if prod["existencias"] == q]
                elif modo in ("mayor", "2"):
                    q = int(input("Mostrar productos con cantidad >: "))
                    encontrados = [
                        prod for prod in productos if prod["existencias"] > q]
                elif modo in ("menor", "3"):
                    q = int(input("Mostrar productos con cantidad <: "))
                    encontrados = [
                        prod for prod in productos if prod["existencias"] < q]
                elif modo in ("rango", "4"):
                    lo = int(input("Ingrese el mínimo del rango: "))
                    hi = int(input("Ingrese el máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    encontrados = [
                        prod for prod in productos if lo <= prod["existencias"] <= hi]
                else:
                    print("¡Error! Opción no válida para cantidad.")
                    return False
            except ValueError:
                error_valor_numerico("cantidad")
                return False

            if encontrados:
                print("Productos encontrados:")
                for prod in encontrados:
                    categorias_str = ", ".join(
                        prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(
                        f"SKU Nº {prod['sku']}: «{prod['nombre']}», ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
                return True
            else:
                print("Error! No se encontraron productos con esa cantidad.")
                return False

        case "4" | "cuatro" | "buscar precio":
            modo = normalizar(
                input("Buscar por precio: 'igual', 'mayor', 'menor' o 'rango': "))
            encontrados = []
            try:
                if modo in ("igual", "1", "exacto"):
                    p = float(input("Ingrese el precio exacto: "))
                    encontrados = [prod for prod in productos if abs(
                        prod["precio"] - p) < 1e-9]
                elif modo in ("mayor", "2"):
                    p = float(input("Mostrar productos con precio > : "))
                    encontrados = [
                        prod for prod in productos if prod["precio"] > p]
                elif modo in ("menor", "3"):
                    p = float(input("Mostrar productos con precio < : "))
                    encontrados = [
                        prod for prod in productos if prod["precio"] < p]
                elif modo in ("rango", "4"):
                    lo = float(input("Ingrese el precio mínimo del rango: "))
                    hi = float(input("Ingrese el precio máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    encontrados = [
                        prod for prod in productos if lo <= prod["precio"] <= hi]
                else:
                    print("¡Error! Opción no válida para precio.")
                    return False
            except ValueError:
                error_valor_numerico("precio")
                return False

            if encontrados:
                print("Resultados encontrados:")
                for prod in encontrados:
                    categorias_str = ", ".join(
                        prod["categorias"]) if prod["categorias"] else "Sin categorías"
                    print(
                        f"SKU {prod['sku']}: {prod['nombre']} ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
                return True
            else:
                print("No se encontraron productos con ese precio.")
                return False

        case "5" | "cinco" | "buscar categoría":
            categoria_buscar = normalizar(
                input("Ingrese la categoría a buscar: "))
            encontrados = []
            for producto in productos:
                if any(normalizar(cat) == categoria_buscar for cat in producto["categorias"]):
                    encontrados.append(producto)

            if encontrados:
                print(
                    f"Productos encontrados en la categoría '{categoria_buscar}':")
                for prod in encontrados:
                    categorias_str = ", ".join(prod["categorias"])
                    print(
                        f"SKU {prod['sku']}: {prod['nombre']} ({prod['existencias']} existencia(s), precio de ${prod['precio']:.2f}, categorías: {categorias_str})")
                return True
            else:
                error_no_encontrado("Categoría", categoria_buscar)

        case "6" | "seis" | "volver al menu principal":
            return False

        case _:
            print("¡Error! Opción no válida.")
    return False


def ingresar():
    data = cargar_memory()
    productos = data["productos"]

    try:
        print("Generación de SKU:")
        print("1. Automático (sugerido)")
        print("2. Manual")
        opcion_sku = input("Seleccione opción (1/2): ").strip()

        if opcion_sku == "1":
            sku = generador_de_sku()
            print(f"SKU generado automáticamente: {sku}")
        else:
            sku = int(input("Ingrese el SKU manualmente: "))
            for producto in productos:
                if producto["sku"] == sku:
                    error_ya_existe("SKU", sku)
                    return False

        existencias = int(input("Ingrese las existencias: "))
        while existencias <= 0:
            existencias = int(input("Error! Ingrese un numero válido.: "))

        nombre = input("Ingrese el nombre del producto: ")

        for producto in productos:
            if normalizar(producto["nombre"]) == normalizar(nombre):
                error_ya_existe("nombre", nombre)
                return False

        precio = float(input("Ingrese el precio del producto: "))
        while precio <= 0:
            precio = float(input("¡Error! Ingrese un numero válido.: "))

        print("Ingrese las categorías del producto (separadas por comas, o Intro para omitir): ")
        categorias_input = input().strip()

        if categorias_input:
            categorias = [cat.strip()
                          for cat in categorias_input.split(",") if cat.strip()]
            categorias = sorted(set(categorias))
            print(f"Categorías procesadas: {', '.join(categorias)}")
        else:
            categorias = []

        umbral_minimo = int(
            input("Ingrese el umbral mínimo de existencias (-1 para desactivar): "))
        while umbral_minimo < -1:
            umbral_minimo = int(input("¡Error! Ingrese un número válido: "))

        umbral_maximo = int(
            input("Ingrese el umbral máximo de existencias (-1 para desactivar): "))
        while umbral_maximo < -1 or (umbral_maximo != -1 and umbral_maximo < umbral_minimo):
            umbral_maximo = int(input(
                "¡Error! Ingrese un número válido (debe ser -1 o mayor/igual al mínimo): "))

        fecha_vencimiento = None
        while True:
            fecha_input = input(
                "Ingrese fecha de vencimiento (AAAA-MM-DD, 'no' para no perecedero, o -1 para cancelar): ").strip()

            if fecha_input.lower() in ["no", "n", "-1"]:
                fecha_vencimiento = "No perecedero"
                break
            elif fecha_input == "":
                fecha_vencimiento = "No perecedero"
                break
            else:
                try:
                    fecha_obj = datetime.strptime(fecha_input, "%Y-%m-%d")
                    fecha_vencimiento = fecha_input
                    break
                except ValueError:
                    print(
                        "¡Error! Formato de fecha inválido. Use AAAA-MM-DD o ingrese 'no' para no perecedero")

        lote = input("Ingrese el número de lote (opcional): ").strip()
        if not lote:
            lote = f"LOTE-{sku}"

        nuevo_producto = {
            "sku": sku,
            "nombre": nombre,
            "existencias": existencias,
            "precio": precio,
            "categorias": categorias,
            "umbral_minimo": umbral_minimo,
            "umbral_maximo": umbral_maximo,
            "fecha_vencimiento": fecha_vencimiento,
            "lote": lote,
            "fecha_ingreso": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo_control": "unidades"
        }

        productos.append(nuevo_producto)

        for categoria in categorias:
            if categoria not in data["categorias"]:
                data["categorias"].append(categoria)

        guardar_memory(data)
        print("Producto ingresado correctamente.")

        if existencias <= umbral_minimo and umbral_minimo > 0:
            print("¡Atención! El producto está por debajo del umbral mínimo.")

        if umbral_maximo > 0 and existencias > umbral_maximo:
            print("¡Atención! El producto supera el umbral máximo.")

        return True

    except ValueError:
        print("¡Error! Ingrese valores numéricos válidos para SKU, existencias, precio y umbral.")
        escribir_log(
            "Error al ingresar valores numéricos en ingreso de producto.", nivel="ERROR")
        return False


def ingresar_paquete():
    data = cargar_memory()
    productos = data["productos"]

    try:
        sku = int(input("Ingrese el SKU: "))
        for producto in productos:
            if producto["sku"] == sku:
                error_ya_existe("SKU", sku)
                return False

        paquetes = int(input("Ingrese la cantidad de paquetes: "))
        while paquetes <= 0:
            paquetes = int(input("¡Error! Ingrese un numero válido.: "))

        unidades_por_paquete = int(input("Ingrese unidades por paquete: "))
        while unidades_por_paquete <= 0:
            unidades_por_paquete = int(
                input("¡Error! Ingrese un numero válido.: "))

        existencias = paquetes * unidades_por_paquete

        nombre = input("Ingrese el nombre del producto: ")

        for producto in productos:
            if normalizar(producto["nombre"]) == normalizar(nombre):
                error_ya_existe("nombre", nombre)
                return False

        precio_paquete = float(input("Ingrese el precio por paquete: "))
        while precio_paquete <= 0:
            precio_paquete = float(
                input("¡Error! Ingrese un numero válido.: "))

        precio_unitario = precio_paquete / unidades_por_paquete

        print(
            "Ingrese las categorías del producto (separadas por comas; Intro para omitir): ")
        categorias_input = input().strip()

        if categorias_input:
            categorias = [cat.strip()
                          for cat in categorias_input.split(",") if cat.strip()]
            categorias = sorted(set(categorias))
            print(f"Categorías procesadas: {', '.join(categorias)}")
        else:
            categorias = []

        print("Configurar umbrales en:")
        print("1. Paquetes")
        print("2. Unidades")
        tipo_umbral = input("Seleccione opción (1/2): ")

        if tipo_umbral == "1":
            umbral_minimo = int(
                input("Ingrese el umbral mínimo de paquetes (-1 para desactivar): "))
            while umbral_minimo < -1:
                umbral_minimo = int(
                    input("¡Error! Ingrese un número válido: "))

            umbral_maximo = int(
                input("Ingrese el umbral máximo de paquetes (-1 para desactivar): "))
            while umbral_maximo < -1:
                umbral_maximo = int(
                    input("¡Error! Ingrese un número válido: "))

            tipo_control = "paquetes"
        else:
            umbral_minimo = int(
                input("Ingrese el umbral mínimo de unidades (-1 para desactivar): "))
            while umbral_minimo < -1:
                umbral_minimo = int(input("Error! Ingrese un número válido: "))

            umbral_maximo = int(
                input("Ingrese el umbral máximo de unidades (-1 para desactivar): "))
            while umbral_maximo < -1:
                umbral_maximo = int(input("Error! Ingrese un número válido: "))

            tipo_control = "unidades"

        fecha_vencimiento = None
        while True:
            fecha_input = input(
                "Ingrese fecha de vencimiento (AAAA-MM-DD, 'no' para no perecedero, o -1 para cancelar): ").strip()

            if fecha_input.lower() in ["no", "n", "-1"]:
                fecha_vencimiento = "No perecedero"
                break
            elif fecha_input == "":
                fecha_vencimiento = "No perecedero"
                break
            else:
                try:
                    fecha_obj = datetime.strptime(fecha_input, "%Y-%m-%d")
                    fecha_vencimiento = fecha_input
                    break
                except ValueError:
                    print(
                        "¡Error! Formato de fecha inválido. Use AAAA-MM-DD o ingrese 'no' para no perecedero")

        lote = input("Ingrese el número de lote (opcional): ").strip()
        if not lote:
            lote = f"LOTE-{sku}"

        nuevo_producto = {
            "sku": sku,
            "nombre": nombre,
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
        escribir_log(
            "Error al ingresar valores numéricos en ingreso de paquete.", nivel="ERROR")
        return False
    except Exception as e:
        print(f"¡Error inesperado! {e}")
        escribir_log(
            f"Error inesperado en ingresar_paquete: {e}", nivel="ERROR")
        return False
    finally:
        escribir_log("Función ingresar_paquete finalizada", nivel="INFO")


def modificar():
    data = cargar_memory()
    productos = data["productos"]

    seleccion2 = normalizar(input(
        "Modificar SKU (1), Producto (2), Existencias (3), Precio (4), Categorías (5): "))
    match seleccion2:

        case "1" | "uno" | "modificar sku":
            try:
                sku_actual = int(input("Ingrese el SKU a modificar: "))
                for producto in productos:
                    if producto["sku"] == sku_actual:
                        nuevo_sku = int(input("Ingrese el nuevo SKU: "))
                        for prod in productos:
                            if prod["sku"] == nuevo_sku and prod != producto:
                                error_ya_existe("SKU", nuevo_sku)
                                return False
                        producto["sku"] = nuevo_sku
                        guardar_memory(data)
                        print("SKU modificado correctamente.")
                        return True
                error_no_encontrado("SKU", sku_actual)
                return False
            except ValueError:
                error_valor_numerico("SKU")
                return False

        case "2" | "dos" | "modificar producto":
            nombre_actual = input(
                "Ingrese el nombre del producto a modificar: ")
            for producto in productos:
                if normalizar(producto["nombre"]) == normalizar(nombre_actual):
                    nuevo_nombre = input(
                        "Ingrese el nuevo nombre del producto: ")
                    for prod in productos:
                        if normalizar(prod["nombre"]) == normalizar(nuevo_nombre) and prod != producto:
                            error_ya_existe("nombre", nuevo_nombre)
                            return False
                    producto["nombre"] = nuevo_nombre
                    guardar_memory(data)
                    print("Producto modificado correctamente.")
                    return True
            error_no_encontrado("Producto", nombre_actual)
            return False

        case "3" | "tres" | "modificar existencias":
            try:
                sku = int(
                    input("Ingrese el SKU del producto cuyas existencias desea modificar: "))
                for producto in productos:
                    if producto["sku"] == sku:
                        nuevas_existencias = int(
                            input("Ingrese las nuevas existencias: "))
                        if nuevas_existencias <= 0:
                            print("¡Error! Las existencias deben ser mayores a 0.")
                            return False
                        producto["existencias"] = nuevas_existencias
                        guardar_memory(data)
                        print("Existencias modificadas correctamente.")
                        return True
                error_no_encontrado("SKU", sku)
                return False
            except ValueError:
                error_valor_numerico("existencias")
                return False

        case "4" | "cuatro" | "modificar precio":
            try:
                mod_busqueda = normalizar(
                    input("Buscar por SKU (1) o Producto (2): "))
                if mod_busqueda in ["sku", "1", "uno"]:
                    sku = int(
                        input("Ingrese el SKU del producto cuyo precio desea modificar: "))
                    for producto in productos:
                        if producto["sku"] == sku:
                            nuevo_precio = float(
                                input("Ingrese el nuevo precio: "))
                            if nuevo_precio <= 0:
                                print("¡Error! El precio debe ser mayor a 0.")
                                return False
                            producto["precio"] = nuevo_precio
                            guardar_memory(data)
                            print("Precio modificado correctamente.")
                            return True
                    error_no_encontrado("SKU", sku)
                    return False

                elif mod_busqueda in ["producto", "2", "dos"]:
                    nombre = input(
                        "Ingrese el nombre del producto cuyo precio desea modificar: ")
                    for producto in productos:
                        if normalizar(producto["nombre"]) == normalizar(nombre):
                            nuevo_precio = float(
                                input("Ingrese el nuevo precio: "))
                            if nuevo_precio <= 0:
                                print("Error! El precio debe ser mayor a 0.")
                                return False
                            producto["precio"] = nuevo_precio
                            guardar_memory(data)
                            print("Precio modificado correctamente.")
                            return True
                    error_no_encontrado("Producto", nombre)
                    return False
                else:
                    print("Error! Opción no válida.")
                    return False

            except ValueError:
                error_valor_numerico("precio")
                return False

        case "5" | "cinco" | "modificar categorías":
            try:
                sku = int(
                    input("Ingrese el SKU del producto cuyas categorías desea modificar: "))
                for producto in productos:
                    if producto["sku"] == sku:
                        print(
                            f"Categorías actuales: {', '.join(producto['categorias']) if producto['categorias'] else 'Ninguna'}")
                        print(
                            "Ingrese las nuevas categorías (separadas por comas, o Intro para eliminar todas): ")
                        categorias_input = input().strip()
                        nuevas_categorias = [cat.strip() for cat in categorias_input.split(
                            ",") if cat.strip()] if categorias_input else []

                        producto["categorias"] = nuevas_categorias

                        data["categorias"] = []
                        for prod in productos:
                            for cat in prod["categorias"]:
                                if cat not in data["categorias"]:
                                    data["categorias"].append(cat)

                        guardar_memory(data)
                        print("Categorías modificadas correctamente.")
                        return True
                error_no_encontrado("SKU", sku)
                return False
            except ValueError:
                error_valor_numerico("SKU")
                return False

        case _:
            print("¡Error! Opción no válida.")
            return False


def eliminar():
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


def mostrar_valor_total():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario.")
        return False

    valor_total = sum(prod["precio"] * prod["existencias"]
                      for prod in productos)
    print(f"Valor total del inventario: ${valor_total:,.2f}")
    escribir_log(f"Consultado valor total: ${valor_total:,.2f}", nivel="INFO")
    return True


def producto_mas_barato():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario.")
        return False

    mas_barato = min(productos, key=lambda x: x["precio"])
    print(f"Producto más barato: «{mas_barato['nombre']}»")
    print(f"SKU: {mas_barato['sku']}, Precio: ${mas_barato['precio']:.2f}")
    print(f"Existencias: {mas_barato['existencias']}")
    escribir_log(
        f"Consultado producto más barato: {mas_barato['nombre']}", nivel="INFO")
    return True


def producto_mas_caro():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario.")
        return False

    mas_caro = max(productos, key=lambda x: x["precio"])
    print(f"Producto más caro: «{mas_caro['nombre']}»")
    print(f"SKU: {mas_caro['sku']}, Precio: ${mas_caro['precio']:.2f}")
    print(f"Existencias: {mas_caro['existencias']}")
    escribir_log(
        f"Consultado producto más caro: {mas_caro['nombre']}", nivel="INFO")
    return True


def promedio_precios():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario.")
        return False

    promedio = sum(prod["precio"] for prod in productos) / len(productos)
    print(f"Promedio de precios: ${promedio:.2f}")
    print(f"Basado en {len(productos)} SKUs.")
    escribir_log(
        f"Consultado promedio de precios: ${promedio:.2f}", nivel="INFO")
    return True


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


def resumen_estadisticas():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario.")
        return False

    total_productos = len(productos)
    total_existencias = sum(prod["existencias"] for prod in productos)
    valor_total = sum(prod["precio"] * prod["existencias"]
                      for prod in productos)
    precio_promedio = sum(prod["precio"]
                          for prod in productos) / total_productos
    total_categorias = len(data["categorias"])

    print("Estadisticas del Inventario")
    print("=" * 40)
    print(f"Total de productos: {total_productos}")
    print(f"Total de existencias: {total_existencias}")
    print(f"Valor total del inventario: ${valor_total:,.2f}")
    print(f"Total de categorías: {total_categorias}")
    print(f"Precio promedio: ${precio_promedio:.2f}")

    if productos:
        mas_existencias = max(productos, key=lambda x: x["existencias"])
        menos_existencias = min(productos, key=lambda x: x["existencias"])
        print(
            f"Producto con más existencias: {mas_existencias['nombre']} ({mas_existencias['existencias']})")
        print(
            f"Producto con menos existencias: «{menos_existencias['nombre']}» ({menos_existencias['existencias']})")

    escribir_log("Generado resumen estadístico", nivel="INFO")
    return True


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


def version_genzalostorage():
    print("""
╔══════════════════════════════════════════════╗
║          INFORMACIÓN DEL PROGRAMA            ║
╠══════════════════════════════════════════════╣
║              genzaloSTORAGE                  ║
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


def formatear_base_datos():
    confirmacion = normalizar(input(
        "¿Desea formatear la base de datos? Esta acción es irreversible. (ingrese 'CONFIRMAR' para continuar): "))

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
    print("=" * 60)
    for lote, productos_lote in lotes.items():
        print(f"\nLote: {lote}")
        print(f"Cantidad de productos: {len(productos_lote)}")
        for prod in productos_lote:
            estado = "VENCIDO" if es_producto_vencido(prod) else "VIGENTE"
            print(
                f"  - {prod['nombre']} (SKU: {prod['sku']}) - Vence: {prod.get('fecha_vencimiento', 'No perecedero')} - {estado}")

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
            print(f"  - {prod['nombre']} (SKU: {prod['sku']})")
            print(
                f"    Existencias: {prod['existencias']} - Precio: ${prod['precio']:.2f}")
            print(
                f"    Vence: {prod.get('fecha_vencimiento', 'No perecedero')} - {estado}")
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
        escribir_log(
            f"Método de salida configurado: {metodos[metodo]}", nivel="INFO")
        return True
    else:
        print("¡Error! Opción no válida.")
        return False


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

                if 0 <= dias_restantes <= 30:  # Próximos 30 días
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
                print(
                    f"  - {producto['nombre']} (SKU: {producto['sku']}) - Vence en {dias} días")
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


def obtener_producto_por_metodo_salida(productos):
    data = cargar_memory()
    metodo = data.get("metodo_salida", "FIFO")

    if not productos:
        return None

    if metodo == "LIFO":
        return productos[-1]
    else:
        productos_ordenados = sorted(
            productos, key=lambda x: x.get("fecha_ingreso", ""))
        return productos_ordenados[0] if productos_ordenados else None


def ingresar_cliente():
    data = cargar_memory()
    clientes = data["clientes"]

    try:
        id_cliente = int(input("Ingrese el ID del cliente: "))
        for cliente in clientes:
            if cliente["id"] == id_cliente:
                print("Error! El ID de cliente ya existe...")
                return False

        nombre = input("Ingrese el nombre del cliente: ")

        for cliente in clientes:
            if normalizar(cliente["nombre"]) == normalizar(nombre):
                print("Error! Ya existe un cliente con ese nombre...")
                return False

        telefono = input("Ingrese el teléfono del cliente: ")
        email = input("Ingrese el email del cliente: ")
        direccion = input("Ingrese la dirección del cliente: ")

        tipo_cliente = normalizar(
            input("Ingrese el tipo de cliente (Normal/Preferencial/Corporativo): "))
        while tipo_cliente not in ["normal", "preferencial", "corporativo"]:
            print(
                "Error! Tipo de cliente no válido. Use: Normal, Preferencial o Corporativo")
            tipo_cliente = normalizar(input("Ingrese el tipo de cliente: "))

        try:
            limite_credito = float(
                input("Ingrese el límite de crédito (0 si no aplica): "))
        except ValueError:
            limite_credito = 0.0

        estado = normalizar(input("Cliente activo? (Si/No): "))
        activo = estado in ["si", "s", "1", "yes", "y"]

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

        clientes.append(nuevo_cliente)

        guardar_memory(data)
        print("Cliente agregado correctamente.")
        escribir_log(
            f"Cliente agregado: {nombre} (ID: {id_cliente})", nivel="INFO")
        return True

    except ValueError:
        print("Error! Ingrese valores numéricos válidos para ID y límite de crédito.")
        escribir_log(
            "Error al ingresar valores numéricos en ingreso de cliente.", nivel="ERROR")
        return False


def eliminar_cliente():
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
                confirmacion = normalizar(
                    input("Esta seguro que desea eliminar este cliente? (Si/No): "))
                if confirmacion in ["si", "s", "1"]:
                    cliente_eliminado = clientes.pop(i)
                    guardar_memory(data)
                    print("Cliente eliminado correctamente.")
                    escribir_log(
                        f"Cliente eliminado: {cliente_eliminado['nombre']} (ID: {cliente_eliminado['id']})", nivel="INFO")
                    return True
                else:
                    print("Operación cancelada.")
                    return False

        print("Error! Cliente no encontrado...")
        return False

    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log(
            "Error al ingresar ID en eliminación de cliente.", nivel="ERROR")
        return False


def modificar_cliente():
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
                        for cli in clientes:
                            if cli != cliente and normalizar(cli["nombre"]) == normalizar(nuevo_nombre):
                                print(
                                    "Error! Ya existe un cliente con ese nombre...")
                                return False
                        cliente["nombre"] = nuevo_nombre

                    case "2" | "telefono" | "teléfono":
                        cliente["telefono"] = input(
                            "Ingrese el nuevo teléfono: ")

                    case "3" | "email" | "correo":
                        cliente["email"] = input("Ingrese el nuevo email: ")

                    case "4" | "direccion" | "dirección":
                        cliente["direccion"] = input(
                            "Ingrese la nueva dirección: ")

                    case "5" | "tipo":
                        nuevo_tipo = normalizar(
                            input("Ingrese el nuevo tipo (Normal/Preferencial/Corporativo): "))
                        while nuevo_tipo not in ["normal", "preferencial", "corporativo"]:
                            print("Error! Tipo de cliente no válido.")
                            nuevo_tipo = normalizar(
                                input("Ingrese el tipo de cliente: "))
                        cliente["tipo"] = nuevo_tipo

                    case "6" | "limite" | "límite" | "credito" | "crédito":
                        try:
                            nuevo_limite = float(
                                input("Ingrese el nuevo límite de crédito: "))
                            cliente["limite_credito"] = nuevo_limite
                        except ValueError:
                            print("Error! Ingrese un valor numérico válido.")
                            return False

                    case "7" | "estado":
                        nuevo_estado = normalizar(
                            input("Cliente activo? (Si/No): "))
                        cliente["activo"] = nuevo_estado in [
                            "si", "s", "1", "yes", "y"]

                    case _:
                        print("Error! Opción no válida...")
                        return False

                guardar_memory(data)
                print("Cliente modificado correctamente.")
                escribir_log(
                    f"Cliente modificado: {cliente['nombre']} (ID: {cliente['id']})", nivel="INFO")
                return True

        print("Error! Cliente no encontrado...")
        return False

    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log(
            "Error al ingresar ID en modificación de cliente.", nivel="ERROR")
        return False


def buscar_cliente():
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
                resultados = [
                    cliente for cliente in clientes if cliente["id"] == id_buscar]
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
            tipo_buscar = normalizar(
                input("Ingrese el tipo de cliente (Normal/Preferencial/Corporativo): "))
            resultados = [
                cliente for cliente in clientes if cliente["tipo"] == tipo_buscar]

        case "4" | "estado":
            estado_buscar = normalizar(
                input("Buscar clientes activos (Si) o inactivos (No): "))
            activo_buscar = estado_buscar in ["si", "s", "1", "yes", "y"]
            resultados = [
                cliente for cliente in clientes if cliente["activo"] == activo_buscar]

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

            continuar = normalizar(
                input("Desea realizar otra operación de clientes? (Si/No): "))
            if continuar not in ["si", "s", "1", "yes", "y"]:
                break

        return True


def ingresar_proveedor():
    data = cargar_memory()
    proveedores = data["proveedores"]

    try:
        id_proveedor = int(input("Ingrese el ID del proveedor: "))
        for proveedor in proveedores:
            while proveedor["id"] == id_proveedor and id_proveedor != -1:
                print("Error! El ID de proveedor ya existe...")
                id_proveedor = int(input("Ingrese el ID del proveedor: "))

        if id_proveedor == -1:
            return

        nombre = input("Ingrese el nombre del proveedor: ")

        for proveedor in proveedores:
            while normalizar(proveedor["nombre"]) == normalizar(nombre) and nombre not in ("-1", "salir"):
                print("Error! Ya existe un proveedor con ese nombre...")
                nombre = input("Ingrese el nombre del proveedor: ")

        if nombre in ("-1", "salir"):
            return

        telefono = input("Ingrese el teléfono del proveedor: ")
        email = input("Ingrese el email del proveedor: ")
        direccion = input("Ingrese la dirección del proveedor: ")
        contacto = input("Ingrese el nombre de la persona de contacto: ")

        especialidad = input(
            "Ingrese la especialidad del proveedor (ej: electrónica, ropa, alimentos): ")

        condiciones_pago = normalizar(
            input("Ingrese condiciones de pago (Contado/15 días/30 días): "))

        estado = normalizar(input("Proveedor activo? (Si/No): "))
        activo = estado in ["si", "s", "1", "yes", "y"]

        try:
            calificacion = int(
                input("Ingrese calificación del proveedor (1-5): "))
            if calificacion < 1 or calificacion > 5:
                calificacion = 3
        except ValueError:
            calificacion = 3

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

        proveedores.append(nuevo_proveedor)

        guardar_memory(data)
        print("Proveedor agregado correctamente.")
        escribir_log(
            f"Proveedor agregado: {nombre} (ID: {id_proveedor})", nivel="INFO")
        return True

    except ValueError:
        print("Error! Ingrese valores numéricos válidos para ID y calificación.")
        escribir_log(
            "Error al ingresar valores numéricos en ingreso de proveedor.", nivel="ERROR")
        return False


def eliminar_proveedor():
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

                productos_asociados = []
                data_productos = cargar_memory()
                for producto in data_productos["productos"]:
                    if (proveedor["nombre"].lower() in producto["nombre"].lower() or
                            any(proveedor["nombre"].lower() in cat.lower() for cat in producto["categorias"])):
                        productos_asociados.append(producto)

                if productos_asociados:
                    print(
                        f"ADVERTENCIA: Este proveedor tiene {len(productos_asociados)} producto(s) asociado(s):")
                    for prod in productos_asociados[:3]:
                        print(f"   - {prod['nombre']} (SKU: {prod['sku']})")
                    if len(productos_asociados) > 3:
                        print(f"   ... y {len(productos_asociados) - 3} más")

                confirmacion = normalizar(
                    input("Esta seguro que desea eliminar este proveedor? (Si/No): "))
                if confirmacion in ["si", "s", "1"]:
                    proveedor_eliminado = proveedores.pop(i)
                    guardar_memory(data)
                    print("Proveedor eliminado correctamente.")
                    escribir_log(
                        f"Proveedor eliminado: {proveedor_eliminado['nombre']} (ID: {proveedor_eliminado['id']})", nivel="INFO")
                else:
                    print("Operación cancelada.")
            elif id_proveedor == -1:
                break
            else:
                print("Error! Proveedor no encontrado...")
        return False

    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log(
            "Error al ingresar ID en eliminación de proveedor.", nivel="ERROR")
        return False


def modificar_proveedor():
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
                        for prov in proveedores:
                            if prov != proveedor and normalizar(prov["nombre"]) == normalizar(nuevo_nombre):
                                print(
                                    "Error! Ya existe un proveedor con ese nombre...")
                            else:
                                proveedor["nombre"] = nuevo_nombre

                    case "2" | "telefono" | "teléfono":
                        proveedor["telefono"] = input(
                            "Ingrese el nuevo teléfono: ")

                    case "3" | "email" | "correo":
                        proveedor["email"] = input("Ingrese el nuevo email: ")

                    case "4" | "direccion" | "dirección":
                        proveedor["direccion"] = input(
                            "Ingrese la nueva dirección: ")

                    case "5" | "contacto":
                        proveedor["contacto"] = input(
                            "Ingrese el nuevo contacto: ")

                    case "6" | "especialidad":
                        proveedor["especialidad"] = input(
                            "Ingrese la nueva especialidad: ")

                    case "7" | "condiciones" | "pago":
                        proveedor["condiciones_pago"] = input(
                            "Ingrese las nuevas condiciones de pago: ")

                    case "8" | "calificacion" | "calificación":
                        try:
                            nueva_calificacion = int(
                                input("Ingrese la nueva calificación (1-5): "))
                            if 1 <= nueva_calificacion <= 5:
                                proveedor["calificacion"] = nueva_calificacion
                            else:
                                print(
                                    "Error! La calificación debe estar entre 1 y 5.")
                        except ValueError:
                            print("Error! Ingrese un número válido.")

                    case "9" | "estado":
                        nuevo_estado = normalizar(
                            input("Proveedor activo? (Si/No): "))
                        proveedor["activo"] = nuevo_estado in [
                            "si", "s", "1", "yes", "y"]

                    case _:
                        print("Error! Opción no válida...")

                guardar_memory(data)
                print("Proveedor modificado correctamente.")
                escribir_log(
                    f"Proveedor modificado: {proveedor['nombre']} (ID: {proveedor['id']})", nivel="INFO")
                return True
            else:
                print("Error! Proveedor no encontrado...")
        return False

    except ValueError:
        print("Error! Ingrese un ID válido.")
        escribir_log(
            "Error al ingresar ID en modificación de proveedor.", nivel="ERROR")
        return False


def buscar_proveedor():
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
                resultados = [
                    proveedor for proveedor in proveedores if proveedor["id"] == id_buscar]
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
            resultados = [proveedor for proveedor in proveedores if especialidad_buscar_norm in normalizar(
                proveedor["especialidad"])]

        case "4" | "estado":
            estado_buscar = normalizar(
                input("Buscar proveedores activos (Si) o inactivos (No): "))
            activo_buscar = estado_buscar in ["si", "s", "1", "yes", "y"]
            resultados = [
                proveedor for proveedor in proveedores if proveedor["activo"] == activo_buscar]

        case "5" | "calificacion" | "calificación":
            try:
                calificacion_buscar = int(
                    input("Ingrese la calificación mínima (1-5): "))
                resultados = [
                    proveedor for proveedor in proveedores if proveedor["calificacion"] >= calificacion_buscar]
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
            estrellas = "*" * proveedor["calificacion"] + \
                "-" * (5 - proveedor["calificacion"])

            print(f"\n ID: {proveedor['id']} - {proveedor['nombre']}")
            print(f"   Teléfono: {proveedor['telefono']}")
            print(f"    Email: {proveedor['email']}")
            print(f"   Dirección: {proveedor['direccion']}")
            print(f"   Contacto: {proveedor['contacto']}")
            print(f"   Especialidad: {proveedor['especialidad']}")
            print(f"   Condiciones pago: {proveedor['condiciones_pago']}")
            print(
                f"   Calificación: {estrellas} ({proveedor['calificacion']}/5)")
            print(f"   Estado: {estado}")
            print(f"   Fecha registro: {proveedor['fecha_registro']}")
            print("-" * 50)
        return True
    else:
        print("No se encontraron proveedores con los criterios especificados.")
        return False


def analizar_proveedores():
    data = cargar_memory()
    proveedores = data["proveedores"]
    productos = data["productos"]

    if not proveedores:
        print("No hay proveedores registrados para analizar.")
        return False

    print("\nANALISIS DE PROVEEDORES")
    print("=" * 60)

    total_proveedores = len(proveedores)
    proveedores_activos = len([p for p in proveedores if p["activo"]])
    promedio_calificacion = sum(p["calificacion"]
                                for p in proveedores) / total_proveedores

    print(f"Total de proveedores: {total_proveedores}")
    print(f"Proveedores activos: {proveedores_activos}")
    print(f"Proveedores inactivos: {total_proveedores - proveedores_activos}")
    print(f"Calificación promedio: {promedio_calificacion:.2f}/5")

    top_proveedores = sorted(
        proveedores, key=lambda x: x["calificacion"], reverse=True)[:5]
    print(f"\nTOP 5 PROVEEDORES MEJOR CALIFICADOS:")
    for i, proveedor in enumerate(top_proveedores, 1):
        estrellas = "*" * proveedor["calificacion"]
        print(
            f"  {i}. {proveedor['nombre']} - {estrellas} ({proveedor['calificacion']}/5)")

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

    print(f"\nRELACIÓN CON PRODUCTOS:")
    for proveedor in proveedores:
        productos_asociados = []
        for producto in productos:
            if (proveedor["nombre"].lower() in producto["nombre"].lower() or
                    any(proveedor["nombre"].lower() in cat.lower() for cat in producto["categorias"])):
                productos_asociados.append(producto)

        if productos_asociados:
            print(
                f"  • {proveedor['nombre']}: {len(productos_asociados)} producto(s) asociado(s)")

    return True


def gestionar_proveedores_modo(modo=None):
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

            continuar = normalizar(
                input("Desea realizar otra operación de proveedores? (Si/No): "))
            if continuar not in ["si", "s", "1", "yes", "y"]:
                return

        return True


def calcular_estadisticas_financieras(productos=None):
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
        inversion_producto = producto["precio compra"] * \
            producto["existencias"]
        valor_venta_producto = producto["precio venta"] * \
            producto["existencias"]
        ganancia_neta_producto = valor_venta_producto - inversion_producto

        total_inversion += inversion_producto
        total_valor_venta += valor_venta_producto
        total_ganancia_neta += ganancia_neta_producto

    if total_inversion > 0:
        ganancia_porcentaje_total = (
            total_ganancia_neta / total_inversion) * 100
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
    print(f"\n{'='*60}")
    print(f"{titulo:^60}")
    print(f"{'='*60}")
    print(
        f" INVERSION TOTAL EN PRODUCTOS: ${estadisticas['total_inversion']:>10.2f}")
    print(
        f" VALOR TOTAL DE VENTA: ${estadisticas['total_valor_venta']:>10.2f}")
    print(
        f" GANANCIA NETA TOTAL: ${estadisticas['ganancia_neta_total']:>10.2f}")

    ganancia_porcentaje = estadisticas['ganancia_porcentaje_total']
    if ganancia_porcentaje > 0:
        indicador_ganancia = "[POSITIVO]"
    elif ganancia_porcentaje < 0:
        indicador_ganancia = "[PERDIDA]"
    else:
        indicador_ganancia = "[NEUTRO]"

    print(
        f" GANANCIA PORCENTUAL: {ganancia_porcentaje:>10.2f}% {indicador_ganancia}")
    print(f" PRODUCTOS ANALIZADOS: {estadisticas['productos_analizados']:>10}")
    print(f"{'='*60}")


def analisis_financiero_completo():
    data = cargar_memory()
    productos = data["productos"]

    if not productos:
        print("No hay productos en el inventario para analizar.")
        return

    stats_generales = calcular_estadisticas_financieras(productos)
    mostrar_estadisticas_financieras(
        stats_generales, "ANALISIS FINANCIERO GENERAL")

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

    productos_con_rentabilidad = []
    for producto in productos:
        ganancia_unitaria = producto["precio venta"] - \
            producto["precio compra"]
        if producto["precio compra"] > 0:
            rentabilidad_porcentaje = (
                ganancia_unitaria / producto["precio compra"]) * 100
        else:
            rentabilidad_porcentaje = 0

        productos_con_rentabilidad.append({
            "producto": producto,
            "rentabilidad_porcentaje": rentabilidad_porcentaje,
            "ganancia_total": ganancia_unitaria * producto["existencias"]
        })

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
            print(
                f"   Ganancia unitaria: ${prod['precio venta'] - prod['precio compra']:.2f}")


def generador_de_sku():
    data = cargar_memory()
    productos = data["productos"]
    if productos:
        max_sku = max(producto["sku"] for producto in productos)
        return max_sku + 1
    else:
        return 1


def exit_program():
    print("¡Gracias por usar genzaloSTORAGE!")
    raise SystemExit

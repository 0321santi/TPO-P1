import json
from datetime import datetime
import os


def limpiarPantalla():
    os.system('cls')


def escribir_log(mensaje, nivel="INFO"):
    try:
        f = open('loginventario.txt', 'at', encoding='UTF8')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {nivel} - {mensaje} \n")
        f.close()
    except FileNotFoundError as e:
        print(f"¡Error! No se puedo escribir en el log.: {e}")
    


def cargar_memory():
    try:
        f = open('memoria.txt', 'rt', encoding='UTF8')
    except FileNotFoundError:
        print("Error: Archivo de Productos no encontrado.")
        print("Creando un nuevo archivo...")
        f = open('memoria.txt', 'at', encoding='UTF8')
    else:
        f.close()
    return

def cargar_categorias():
    try:
        f = open('categorias.txt', 'rt', encoding='UTF8')
    except FileNotFoundError:
        print("Error: Archivo de categorias no encontrado.")
        print("Creando un nuevo archivo...")
        f = open('categorias.txt', 'at', encoding='UTF8')
    else:
        f.close()
    return


def guardar_memory(data):
    f = open('memoria.txt', 'at', encoding='UTF8')
    f.write(json.dumps(data) + '\n')
    f.close()
    return


def guardar_categorias(cats):
    try:
        arch = open("categorias.txt", "at", encoding="UTF8")
        for cat in cats:
            arch.write(cat + '\n')
    except FileNotFoundError:
        print("no")
    finally:
        arch.close() 
    return



def leer_categorias(cats):
    try:
        f = open('categorias.txt', 'rt', encoding='UTF8')
        arch_memoria = open('memoria.txt', 'rt', encoding='UTF8')
        for linea in f:
            cat = linea.strip()
            if cat in cats:
                cats.remove(cat)
    except FileNotFoundError as e:
        print(f"Error {e}")
        print("creando nuevo archivo...")
        f = open('categorias.txt', 'at', encoding='UTF8')
    finally:
        f.close()
    return cats


def comprobar(tag_nuevo):  # Retornara TRUE si se encuentra una coincidencia
    try:
        f = open('memoria.txt', 'rt', encoding='UTF8')
        encontrado = False
        for lineas in f:
            linea = json.loads(lineas)
            if linea.get("nombre_producto") == tag_nuevo or linea.get("SKU") == tag_nuevo:
                encontrado = True
                break
    finally:
        f.close()
    return encontrado

def eliminar_categorias_de_producto(actuales, borrar): # Recursividad
    if len(actuales) == 0:
        return []
    primero = actuales[0]
    siguientes = actuales[1:]
    if primero in borrar:
        return eliminar_categorias_de_producto(siguientes, borrar)
    else:
        return [primero] + eliminar_categorias_de_producto(siguientes, borrar)

def eliminar_categorias(borrar):
    try:
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        temp = open('temp.txt', 'at', encoding='UTF8')
        for lineas in arch:
            linea = json.loads(lineas)
            if borrar in linea.get('categorias'):
                linea['categorias'].remove(borrar)
                temp.write(json.dumps(linea) + '\n')
            else:
                temp.write(json.dumps(linea) + '\n')
    finally:
        arch.close()
        temp.close()
    return

def remplazar(productos):
    try:
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        temp = open('temp.txt', 'at', encoding='UTF8')
        for lineas in arch:
            linea = json.loads(lineas)
            if linea.get('nombre_producto') not in productos and linea.get('SKU') not in productos:
                temp.write(json.dumps(linea) + '\n')
    finally:
        arch.close()
        temp.close()
    return


def actualizar_categorias():
    try:
        mem_arch = open('memoria.txt', 'rt', encoding='UTF8')
        cat_arch = open('categorias.txt', 'rt', encoding='UTF8')
        temp = open('temp.txt', 'at', encoding='UTF8')
        for cat in cat_arch:
            existe = False
            mem_arch.seek(0)
            for lineas in mem_arch:
                linea = json.loads(lineas)
                if cat.strip() in linea.get("categorias"):
                    existe = True
                    break
            if existe:
                temp.write(cat)
    except FileNotFoundError as e:
        print("Error: ", e)
    finally:
        mem_arch.close()
        cat_arch.close()
        temp.close()
        os.replace("temp.txt", "categorias.txt")

    return

def remplazar_modificar(productos):
    try:
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        temp = open('temp.txt', 'at', encoding='UTF8')
        for lineas in arch:
            linea = json.loads(lineas.strip())
            if linea.get('nombre_producto') != productos:
                temp.write(json.dumps(linea) + '\n')
    finally:
        arch.close()
        temp.close()
    return

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

def buscar_producto(nombre):
    try:
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        consulta_norm = normalizar(nombre)

        for lineas in arch:
            linea = json.loads(lineas)
            if linea.get("nombre_producto") == consulta_norm:
                break
    except FileNotFoundError:
        print("no")
    finally:
        arch.close()
    return linea

def similitud_numerica(num1, num2):
    str1 = str(num1)
    str2 = str(num2)

    for i in range(min(len(str1), len(str2)), 0, -1):
        if str1[:i] == str2[:i]:
            return i / max(len(str1), len(str2))

    try:
        n1 = int(num1)
        n2 = int(num2)
        diferencia = abs(n1 - n2)
        return 1 / (1 + diferencia / max(1, n1))
    except:
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
    encuentro = False
    seleccion = normalizar(input("Seleccione una opción:"))

    match seleccion:
        case "1" | "uno" | "buscar sku":
            try:
                sku = int(input("Ingrese el SKU a buscar: "))
                encontrado = False
                resultados = []
                arch = open('memoria.txt', 'rt', encoding='UTF8')

                for lineas in arch:
                    linea = json.loads(lineas)
                    if linea.get("SKU") == sku:
                        print(f"El producto «{linea.get('nombre_producto')}» tiene SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f} y categorías: «{linea.get('categorias')}».")
                        encontrado = True
                        break

                if encontrado == False:
                    resultados = []
                    arch = open('memoria.txt', 'rt', encoding='UTF8')
                    for lineas in arch:
                        linea = json.loads(lineas)
                        sim = similitud_numerica(sku, linea.get("SKU"))
                        if sim >= 0.4 or str(sku) in str(linea.get("SKU")):
                            resultados.append((sim, linea))
                if resultados:
                    print("SKU exacto no encontrado. ¿Quizá quiso decir?:")
                    for sim, prod in sorted(resultados, reverse=True):
                        categorias_str = ", ".join(prod.get("categorias")) if prod.get("categorias") else "Sin categorías"
                        print(f"«{prod.get('nombre_producto')}», SKU Nº {prod.get('SKU')}, {prod.get('existencias')} existencia(s), precio de ${prod.get('precio'):.2f}, categorías: «{prod.get('categorias')}»)")

                arch.close()
            except ValueError:
                error_valor_numerico("SKU")

        case "2" | "dos" | "buscar producto":
            consulta = input("Ingrese el nombre del producto a buscar: ")
            consulta_norm = normalizar(consulta)
            arch = open('memoria.txt', 'rt', encoding='UTF8')
            encontrado = False

            for lineas in arch:
                linea = json.loads(lineas)
                if linea.get("nombre_producto") == consulta_norm:
                    print(f"El producto «{linea.get('nombre_producto')}» tiene SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f} y categorías: «{linea.get('categorias')}».")
                    encuentro = True
                    break

            if encuentro == False:
                resultados = []
                arch = open('memoria.txt', 'rt', encoding='UTF8')
                for lineas in arch:
                    linea = json.loads(lineas)
                    sim = similitud(
                        consulta_norm, linea.get("nombre_producto"))
                    if sim >= 0.4 or consulta_norm in normalizar(linea.get("nombre_producto")):
                        resultados.append((sim, linea))
                if resultados:  # parece terminado ahora hay que replicarlo para todos los demas. Falta manejar categorias tambien.
                    print("Producto exacto no encontrado. ¿Quizá quiso decir?:")
                    for sim, prod in sorted(resultados, reverse=True):
                        categorias_str = ", ".join(prod.get("categorias")) if prod.get(
                            "categorias") else "Sin categorías"
                        print(f"«{prod.get('nombre_producto')}», SKU Nº {prod.get('SKU')}, {prod.get('existencias')} existencia(s), precio de ${prod.get('precio'):.2f}, categorías: «{prod.get('categorias')}»")
                else:
                    error_no_encontrado("Producto", consulta)
            arch.close()

        case "3" | "tres" | "buscar cantidad":
            modo = normalizar(
                input("Buscar por cantidad: 'igual', 'mayor' o 'menor', 'rango': "))

            arch = open("memoria.txt", "rt", encoding="UTF8")

            try:
                if modo in ("igual", "1", "exacto"):
                    c = int(input("Ingrese la cantidad exacta: "))
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if c == linea.get("existencias"):
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")

                elif modo in ("mayor", "2"):
                    c = int(input("Mostrar productos con cantidad > : "))
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if c < linea.get("existencias"):
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")

                elif modo in ("menor", "3"):
                    c = int(input("Mostrar productos con cantidad > : "))
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if c > linea.get("existencias"):
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")

                elif modo in ("rango", "4"):
                    lo = int(input("Ingrese la cantidad mínima del rango: "))
                    hi = int(input("Ingrese la cantidad máxima del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if lo <= linea.get("existencias") <= hi:
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")

                else:
                    print("¡Error! Opción no válida para cantidad.")
                    return False

            except ValueError:
                error_valor_numerico("cantidad")
            finally:
                arch.close()

        case "4" | "cuatro" | "buscar precio":
            modo = normalizar(input("Buscar por precio: 'igual', 'mayor', 'menor' o 'rango': "))
            arch = open('memoria.txt', 'rt', encoding='UTF8')
            try:
                if modo in ("igual", "1", "exacto"):
                    p = float(input("Ingrese el precio exacto: "))
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if p == linea.get("precio"):
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")

                elif modo in ("mayor", "2"):
                    p = float(input("Mostrar productos con precio > : "))
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if p < linea.get("precio"):
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")

                elif modo in ("menor", "3"):
                    p = float(input("Mostrar productos con precio < : "))
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if p > linea.get("precio"):
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")

                elif modo in ("rango", "4"):
                    lo = float(input("Ingrese el precio mínimo del rango: "))
                    hi = float(input("Ingrese el precio máximo del rango: "))
                    if lo > hi:
                        lo, hi = hi, lo
                    for lineas in arch:
                        linea = json.loads(lineas)
                        if lo <= linea.get("precio") <= hi:
                            print(f"«{linea.get('nombre_producto')}», SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f}, categorías: «{linea.get('categorias')}»)")
                
                else:
                    print("¡Error! Opción no válida para precio.")
                    
        
            except ValueError:
                error_valor_numerico("precio")
            
            finally:
                arch.close()


        case "5" | "cinco" | "buscar categoría":
            categoria_buscar = normalizar(input("Ingrese la categoría a buscar: "))

            arch = open('memoria.txt', 'rt', encoding='UTF8')
            for lineas in arch:
                linea = json.loads(lineas)
                if categoria_buscar in linea.get("categorias"):
                    print(f"El producto «{linea.get('nombre_producto')}» tiene SKU Nº {linea.get('SKU')}, {linea.get('existencias')} existencia(s), precio de ${linea.get('precio'):.2f} y categorías: «{linea.get('categorias')}».")
            arch.close()

        case "6" | "seis" | "volver al menu principal":
            return

        case _:
            print("¡Error! Opción no válida.")
    return


def ingresar():
    try:
        sku = int(input("Ingrese el SKU: "))
        comprobar(sku)
        while comprobar(sku) == True:
            print("Error: No se permite ingresar sku's repetidos.")
            sku = int(input("Ingrese el sku de nuevo: "))
            comprobar(sku)

        nombre = input("Ingrese el nombre del producto: ")
        comprobar(nombre)
        while comprobar(nombre) == True:
            print("Error: No se permite ingresar nombres repetidos.")
            nombre = input("Ingrese el nombre de nuevo: ")
            comprobar(nombre)

        existencias = int(input("Ingrese las existencias: "))
        while existencias <= 0:
            existencias = int(input("¡Error! Ingrese un numero válido.: "))

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

        umbral_minimo = int(input("Ingrese el umbral mínimo de existencias (-1 para desactivar): "))
        while umbral_minimo < -1:
            umbral_minimo = int(input("¡Error! Ingrese un número válido: "))

        umbral_maximo = int(input("Ingrese el umbral máximo de existencias (-1 para desactivar): "))
        while umbral_maximo < -1 or (umbral_maximo != -1 and umbral_maximo < umbral_minimo):
            umbral_maximo = int(input("¡Error! Ingrese un número válido (debe ser -1 o mayor/igual al mínimo): "))
            
        nuevo_producto = {"nombre_producto": nombre, "SKU": sku, "existencias": existencias, "precio": precio, "categorias": categorias, "umbral_minimo": umbral_minimo, "umbral_maximo": umbral_maximo}
    
        guardar_memory(nuevo_producto)

        guardar_categorias(leer_categorias(categorias))
        print("Producto ingresado correctamente.")

        if existencias <= umbral_minimo and umbral_minimo > 0:
            print("¡Atención! El producto está por debajo del umbral mínimo.")

        if umbral_maximo > 0 and existencias >= umbral_maximo:
            print("¡Atención! El producto supera el umbral máximo.")

        return True

    except ValueError:
        print("¡Error! Ingrese valores numéricos válidos para SKU, existencias, precio y umbral.")
        escribir_log("Error al ingresar valores numéricos en ingreso de producto.", nivel="ERROR")
        return False

def modificar():
    opcion = input("Ingrese el nombre del producto: ")
    if comprobar(opcion):
        producto_a_modificar = buscar_producto(opcion)
        print(f"SKU: {producto_a_modificar.get('SKU')}, Nombre: {producto_a_modificar.get('nombre_producto')}, existencias: {producto_a_modificar.get('existencias')}, precio: {producto_a_modificar.get('precio'):.2f}, categorías: «{producto_a_modificar.get('categorias')}»")
        while True:
            seleccion2 = input("Modificar SKU (1), nombre (2), Existencias (3), Precio (4), Categorías (5): ")
            match seleccion2:
                case "1" | "uno" | "modificar sku":
                    try:
                        nuevo_sku = int(input("Ingrese el nuevo SKU: "))
                        producto_a_modificar["SKU"] = nuevo_sku

                    except ValueError:
                        error_valor_numerico("SKU")

                case "2" | "dos" | "modificar nombre":
                    nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
                    producto_a_modificar["nombre_producto"] = nuevo_nombre

                case "3" | "tres" | "modificar existencias":
                    try:
                        nuevas_existencias = int(input("Ingrese la cantidad de existencias del producto: "))
                        producto_a_modificar["existencias"] = nuevas_existencias
                    except ValueError:
                        error_valor_numerico("existencias")

                case "4" | "cuatro" | "modificar precio":
                    try:
                        nuevo_precio = float(input("Ingrese el nuevo precio del producto: "))
                        producto_a_modificar["precio"] = nuevo_precio
                    except ValueError:
                        error_valor_numerico("precio")

                case "5" | "cinco" | "modificar categorías":
                    print("Ingrese las nuevas categorías del producto (separadas por comas, o Intro para omitir): ")
                    categorias_actuales = producto_a_modificar.get("categorias")
                    categorias_agregar = input().strip()
                    if categorias_agregar:
                        categorias_nuevas = [cat.strip() for cat in categorias_agregar.split(",") if cat.strip()]
                        for cat in categorias_nuevas:
                            if cat in producto_a_modificar.get("categorias"):
                                categorias_nuevas.remove(cat)
                    else:
                        categorias_nuevas = []
                    categorias_actuales = categorias_actuales + categorias_nuevas
                    
                    
                    print("Ingrese las categorías a borrar del producto (separadas por comas, o Intro para omitir): ")
                    categorias_borrar = input().strip()
                    if categorias_borrar:
                        categorias_viejas = [cat.strip() for cat in categorias_borrar.split(",") if cat.strip()]
                        print(categorias_borrar)
                        print(categorias_actuales)
                        eliminar_categorias_de_producto(categorias_actuales, categorias_viejas)
                    else:
                        categorias_viejas = []

                    producto_a_modificar["categorias"] = eliminar_categorias_de_producto(categorias_actuales, categorias_viejas)
                
                case _:
                    break
            print(f"SKU: {producto_a_modificar.get('SKU')}, Nombre: {producto_a_modificar.get('nombre_producto')}, existencias: {producto_a_modificar.get('existencias')}, precio: {producto_a_modificar.get('precio'):.2f}, categorías: «{producto_a_modificar.get('categorias')}")
        if producto_a_modificar != buscar_producto(opcion):
            remplazar_modificar(opcion)
            os.replace("temp.txt", "memoria.txt")
            guardar_memory(producto_a_modificar)
            guardar_categorias(leer_categorias(producto_a_modificar.get("categorias")))
            actualizar_categorias()
            
    else:
        print("Producto no encontrado.")
    return


def eliminar():
    producto = 0
    seleccion = 0
    eliminar = []

    seleccion = input("Ingrese 1 si quiere eliminar segun SKU\nIngrese 2 para eliminar segun nombre\nIngrese -1 para salir: ")

    if seleccion == "1":
        while producto != -1:
            producto = int(input("Ingrese el SKU del producto que quiera borrar o -1 para terminar: "))

            if comprobar(producto):
                eliminar.append(producto)
            elif producto != -1:
                print("Producto no encontrado")

    elif seleccion == "2":
        while producto != "-1":
            producto = input("Ingrese el nombre del producto que quiera borrar o -1 para terminar: ")

            if comprobar(producto):
                    eliminar.append(producto)
            elif producto != "-1":
                print("Producto no encontrado")
    else:
        return

    remplazar(eliminar)
    print("Productos eliminados.")
    os.replace("temp.txt", "memoria.txt")
    actualizar_categorias()
    return


def gestionar_categoria_modo(modo):
    if modo == "ver":
        arch_cat = open('categorias.txt', 'rt', encoding='UTF8')
        for cat in arch_cat:
            print("Categorias: ")
            print(cat.strip())
        arch_cat.close()

    elif modo == "eliminar":
        el = input("Ingrese la categoria a eliminar (esto borrara todas las instancias de esta categoria): ")
        eliminar_categorias(el)
        os.replace("temp.txt", "memoria.txt")

    actualizar_categorias()
    return


def verificar_umbral_minimo():
    try:
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        productos_bajo_umbral = []

        for lineas in arch:
            linea = json.loads(lineas)
            umbral = linea.get("umbral_minimo", 0)
            if linea["existencias"] <= umbral:
                productos_bajo_umbral.append(linea)

        arch.close()

        if productos_bajo_umbral:
            print("Productos por debajo del umbral mínimo:")
            for prod in productos_bajo_umbral:
                umbral = prod.get("umbral_minimo", 0)
                print(f"{prod['nombre']} (SKU: {prod['sku']}): {prod['existencias']} existencias (Umbral: {umbral})")
            escribir_log(f"Alertas de umbral mínimo: {len(productos_bajo_umbral)} productos", nivel="WARNING")
        else:
            print("Todos los productos están por encima del umbral mínimo.")

        return productos_bajo_umbral
    except FileNotFoundError:
        print("no hay archivo")
        return []


def verificar_sobre_almacenamiento():
    try:
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        productos_sobre_almacenamiento = []

        for lineas in arch:
            linea = json.loads(lineas)
            umbral_maximo = linea.get("umbral_maximo", 0)
            if umbral_maximo > 0 and linea["existencias"] > umbral_maximo:
                productos_sobre_almacenamiento.append(linea)

        arch.close()

        if productos_sobre_almacenamiento:
            print("Productos con sobre almacenamiento:")
            for prod in productos_sobre_almacenamiento:
                umbral_maximo = prod.get("umbral_maximo", 0)
                print(f"{prod['nombre']} (SKU: {prod['sku']}): {prod['existencias']} existencias (Umbral máximo: {umbral_maximo})")
            escribir_log(f"Alertas de sobre almacenamiento: {len(productos_sobre_almacenamiento)} productos", nivel="WARNING")
        else:
            print("No hay productos con sobre almacenamiento.")

        return productos_sobre_almacenamiento
    except FileNotFoundError:
        print("no hay archivo")
        return []


def configurar_umbral_minimo():
    try:
        sku = int(input("Ingrese el SKU del producto: "))
        
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        temp = open('temp.txt', 'wt', encoding='UTF8')
        modificado = False
        
        for lineas in arch:
            linea = json.loads(lineas)
            if linea["sku"] == sku:
                print(f"Producto: {linea['nombre']}")
                print(f"Existencias actuales: {linea['existencias']}")
                umbral_actual = linea.get("umbral_minimo", "No configurado")
                print(f"Umbral actual: {umbral_actual}")

                nuevo_umbral = int(input("Ingrese el nuevo umbral mínimo (0 para desactivar): "))

                if nuevo_umbral < 0:
                    print("¡Error! El umbral no puede ser negativo.")
                    arch.close()
                    temp.close()
                    return False

                linea["umbral_minimo"] = nuevo_umbral
                modificado = True
                
                if nuevo_umbral == 0:
                    print("Umbral mínimo desactivado para este producto.")
                    escribir_log(f"Umbral desactivado para SKU {sku}", nivel="INFO")
                else:
                    print(f"Umbral mínimo configurado en {nuevo_umbral}.")
                    escribir_log(f"Umbral configurado para SKU {sku}: {nuevo_umbral}", nivel="INFO")

                    if linea["existencias"] <= nuevo_umbral:
                        print("¡Advertencia! El producto está por debajo del nuevo umbral.")
            
            temp.write(json.dumps(linea) + '\n')
        
        arch.close()
        temp.close()
        
        if modificado:
            os.remove('memoria.txt')
            os.rename('temp.txt', 'memoria.txt')
            return True
        else:
            os.remove('temp.txt')
            error_no_encontrado("SKU", sku)
            return False
            
    except ValueError:
        error_valor_numerico("umbral")
        return False


def configurar_umbral_maximo():
    try:
        sku = int(input("Ingrese el SKU del producto: "))
        
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        temp = open('temp.txt', 'wt', encoding='UTF8')
        modificado = False
        
        for lineas in arch:
            linea = json.loads(lineas)
            if linea["sku"] == sku:
                print(f"Producto: {linea['nombre']}")
                print(f"Existencias actuales: {linea['existencias']}")
                umbral_actual = linea.get("umbral_maximo", "No configurado")
                print(f"Umbral máximo actual: {umbral_actual}")

                nuevo_umbral = int(input("Ingrese el nuevo umbral máximo (-1 para desactivar): "))

                if nuevo_umbral < -1:
                    print("¡Error! El umbral no puede ser negativo.")
                    arch.close()
                    temp.close()
                    return False

                linea["umbral_maximo"] = nuevo_umbral
                modificado = True
                
                if nuevo_umbral == -1:
                    print("Umbral máximo desactivado para este producto.")
                    escribir_log(f"Umbral máximo desactivado para SKU {sku}", nivel="INFO")
                else:
                    print(f"Umbral máximo configurado en {nuevo_umbral}.")
                    escribir_log(f"Umbral máximo configurado para SKU {sku}: {nuevo_umbral}", nivel="INFO")

                    if linea["existencias"] > nuevo_umbral:
                        print("¡Advertencia! El producto supera el nuevo umbral máximo.")
            
            temp.write(json.dumps(linea) + '\n')
        
        arch.close()
        temp.close()
        
        if modificado:
            os.remove('memoria.txt')
            os.rename('temp.txt', 'memoria.txt')
            return True
        else:
            os.remove('temp.txt')
            error_no_encontrado("SKU", sku)
            return False
            
    except ValueError:
        error_valor_numerico("umbral")
        return False


def existencias_sin_stock():
    try:
        arch = open('memoria.txt', 'rt', encoding='UTF8')
        sin_stock = []

        for lineas in arch:
            linea = json.loads(lineas)
            if linea["existencias"] == 0:
                sin_stock.append(linea)

        arch.close()

        if sin_stock:
            print("Productos sin existencias:")
            for prod in sin_stock:
                print(f"{prod['nombre']} (SKU: {prod['sku']})")
            print(f"Total: {len(sin_stock)} productos")
        else:
            print("No hay productos sin existencias.")

        escribir_log(f"Consultados productos sin stock: {len(sin_stock)}", nivel="INFO")
        return len(sin_stock) > 0
    except FileNotFoundError:
        print("no hay archivo")
        return False


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
        productos_cat = [prod for prod in productos if categoria in prod["categorias"]]
        total_existencias = sum(prod["existencias"] for prod in productos_cat)
        valor_categoria = sum(prod["precio"] * prod["existencias"]
                              for prod in productos_cat)

        print(f"\n{categoria}:")
        print(f"Productos: {len(productos_cat)}")
        print(f"Existencias: {total_existencias}")
        print(f"Valor: ${valor_categoria:,.2f}")

    escribir_log("Consultados productos por categoría", nivel="INFO")
    return True


def versionGS():
    print("""
╔══════════════════════════════════════════════╗
║          INFORMACIÓN DEL PROGRAMA            ║
╠══════════════════════════════════════════════╣
║              genzaloSTORAGE                  ║
║       Sistema de Gestión de Inventarios      ║
║                                              ║
║  Desarrollado por: GRUPO 8                   ║
║  Versión: 1.2                                ║
║  Integrantes:                                ║
║       Lioy, Santiago;                        ║
║       Fernandez, Maximiliano;                ║
║       Alaniz, Ramiro                         ║   
║                                              ║   
╚══════════════════════════════════════════════╝
    """)
    escribir_log("Consultada versión del programa", nivel="INFO")
    return True


def formatearDB():
    confirmacion = normalizar(input("¿Desea formatear la base de datos? Esta acción es irreversible. (ingrese 'CONFIRMAR' para continuar): "))

    if confirmacion == "confirmar":
        memoria = open('memoria.txt', 'w', encoding='UTF8') 
        memoria.close()
        categorias = open('categorias.txt', 'w', encoding='UTF8') 
        categorias.close()
        print("Información: Base de datos formateada correctamente.")
        escribir_log("Base de datos formateada", nivel="CRITICAL")
        return True
    else:
        print("¡Error! La operación fue cancelada.")
        return False


def buscarRec(buscarCat, lineas, indice=0, barato=None, caro=None):
    if indice >= len(lineas):
        return barato, caro
    
    linea = json.loads(lineas[indice])
    
    tiene_categoria = False
    for cat in buscarCat:
        if cat in linea.get("categorias", []):
            tieneCategoria = True
            break
    
    if tieneCategoria:
        precioActual = linea.get("precio", 0)
        nombreActual = linea.get("nombre_producto", "")
        skuActual = linea.get("SKU", 0)
        
        if barato is None or precioActual < barato.get("precio", float('inf')):
            barato = {"nombre": nombreActual, "SKU": skuActual, "precio": precioActual}
        
        if caro is None or precioActual > caro.get("precio", 0):
            caro = {"nombre": nombreActual, "SKU": skuActual, "precio": precioActual}
    
    return buscarRec(buscarCat, lineas, indice + 1, barato, caro)

def mostrarPrecios():
    ingresarCat = input("Ingrese categorías a buscar (separadas por comas): ")
    buscarCateg = [normalizar(cat.strip()) for cat in ingresarCat.split(",") if cat.strip()]
    
    if not buscarCateg:
        print("No ingresó categorías válidas.")
        return
    
    arch = open('memoria.txt', 'rt', encoding='UTF8')
    lineas = arch.readlines()
    arch.close()
    
    barato, caro = buscarRec(buscarCateg, lineas)
    
    if barato is None or caro is None:
        print("No se encontraron productos en esas categorías.")
        return
    
    print(f"Producto más barato: {barato['nombre']} (SKU: {barato['SKU']}) - ${barato['precio']:.2f}")
    print(f"Producto más caro: {caro['nombre']} (SKU: {caro['SKU']}) - ${caro['precio']:.2f}")


def exit_program():
    print("¡Gracias por usar genzaloSTORAGE!")
    raise SystemExit
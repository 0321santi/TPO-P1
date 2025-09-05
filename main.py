#def
def ingresar_sku(a, b):
    sku=int(input("Ingrese el SKU: "))
    lista1.append(sku)
    existencias = int(input("Ingrese las existencias: "))
    lista2.append(existencias)

lista1=[] #lista de sku
lista2=[] #lista de existencias


print("""Bienvenido, seleccione una opción:
      1. Ingresar SKU
      2. Buscar SKU
      3. Eliminar SKU
      4. Salir""")
seleccion=(int(input("Opción seleccionada: ")))

match seleccion:
    case 1:
    case 2:
        sku=int(input("Ingrese el SKU a buscar: "))
        if sku in lista1:
            print("El SKU",sku,"tiene",existencias,"existencias")
        else:
        
            
    case 3:
        print("bbbbb")
    case 4:
        print("cccccc")
    
'''
if seleccion==1:
    sku=int(input("Ingrese el SKU: "))
    lista1.append(sku)
    existencias=int(input("Ingrese las existencias: "))
    lista2.append(existencias)
    print("SKU y existencias ingresados correctamente")
elif seleccion==2:
    sku=int(input("Ingrese el SKU a buscar: "))
    if sku in lista1:
        
        print("El SKU",sku,"tiene",existencias,"existencias")
elif seleccion==3:
    sku=int(input("Ingrese el SKU a eliminar: "))
    if sku in lista1:
        print("SKU eliminado correctamente")
    else:
        print("SKU no encontrado")
'''
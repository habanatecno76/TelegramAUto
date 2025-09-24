def menu():
    print("=== Telegram Auto Mensajero ===")
    print("1. Iniciar envío automático de mensajes")
    print("2. Salir")
    print("3. Añadir grupo")
    print("4. Cambiar publicacion")
    opcion = input("Selecciona una opción: ")
    return opcion


def replace_announce():
    # Solicitar nueva publicación al usuario
    nueva_publicacion = input("Ingresa la nueva publicación (presiona Enter 2 veces para terminar):\n")
    
    # Leer líneas hasta que el usuario ingrese una línea vacía (opcional para multi-línea)
    while True:
        linea = input()
        if not linea:
            break
        nueva_publicacion += "\n" + linea

    # Guardar la nueva publicación en el archivo (sobrescribiendo el contenido anterior)
    with open('announce.txt', 'w', encoding='utf-8') as file:
        file.write(nueva_publicacion)
    
    print("¡Publicación actualizada correctamente!")




def add_group(nuevo_grupo):
    # Paso 1: Leer el archivo (o crearlo si no existe)
    try:
        with open('groups.txt', 'r+', encoding='utf-8') as file:
            contenido = file.read()  # Lee TODO el contenido (con espacios/saltos)
            
            # Paso 2: Añadir el nuevo grupo (con espacio si ya hay datos)
            if contenido and not contenido.endswith('\n') and not contenido.endswith(' '):
                # Si el contenido no termina en salto ni espacio, añade espacio antes del nuevo grupo
                nuevo_contenido = f"{contenido} {nuevo_grupo}"
            else:
                # Si termina en salto o espacio, añade directamente el grupo
                nuevo_contenido = f"{contenido}{nuevo_grupo}"
            
            # Paso 3: Sobrescribir el archivo con el nuevo contenido
            file.seek(0)  # Volver al inicio del archivo
            file.write(nuevo_contenido)
            file.truncate()  # Eliminar contenido residual si el nuevo es más corto
    
    except FileNotFoundError:
        # Si el archivo no existe, crearlo con el nuevo grupo
        with open('groups.txt', 'w', encoding='utf-8') as file:
            file.write(nuevo_grupo)
    
    print(f"✅ Grupo '{nuevo_grupo}' añadido correctamente.")



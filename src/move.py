import os
import shutil

# Obtener la lista de archivos en el directorio actual
archivos = os.listdir(".")

# Recorrer cada archivo en la lista
for archivo in archivos:
    # Verificar si el archivo es de tipo .flac o .mp3
    if archivo.endswith(".flac") or archivo.endswith(".mp3"):
        # Obtener el nombre de la carpeta correspondiente
        carpeta = "./demucs_separate/htdemucs/" + os.path.splitext(archivo)[0]
        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)
        # Mover el archivo a la carpeta correspondiente
        shutil.move(archivo, carpeta)

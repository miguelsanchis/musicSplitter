import os
import re
import subprocess
import sys

import httpx
from pytube import Playlist, YouTube


def get_youtube_url(song_name, artist_name):
    query = song_name + " " + artist_name + " official music video"
    search_url = "https://www.youtube.com/results?search_query=" + query
    response = httpx.get(search_url)
    html_content = response.text
    video_url = re.findall(r'href=\"watch\?v=(.{11})', html_content)[0]
    return "https://www.youtube.com/watch?v=" + video_url


def download_video(input_url):
    # Crea un objeto de la clase YouTube
    video = YouTube(input_url)

    # Obtiene el título del video
    title = video.title

    # Verifica si el archivo ya ha sido descargado previamente
    if not os.path.isfile(f"{title}.mp3"):
        # Obtiene el stream de audio en formato MP3
        audio_stream = video.streams.filter(only_audio=True).first()

        # Descarga el stream de audio en formato MP3
        audio_stream.download(filename=title + '.mp3')

        print(f"El video '{title}' ha sido descargado con éxito.")

    else:
        print(f"El video '{title}' ya ha sido descargado previamente.")


def download_playlist(playlist_url):
    # Crea un objeto de la clase Playlist
    playlist = Playlist(playlist_url)

    # Recorre la lista de videos de la lista de reproducción
    for video_url in playlist:
        download_video(video_url)


def download_channel(channel_url):
    # Crea una petición GET a la API de YouTube
    response = httpx.get(f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_url}")

    # Verifica si la respuesta es válida
    if response.status_code == 200:
        # Recorre los videos del canal
        for line in response.text.split("\n"):
            # Verifica si la línea contiene un enlace de video
            if "watch?v=" in line:
                # Extrae el enlace de video
                video_url = "https://www.youtube.com/watch?v=" + line.split("watch?v=")[1].split('"')[0]

                # Descarga el video
                download_video(video_url)
    else:
        print("No se ha podido acceder a la API de YouTube.")


# Enlace de YouTube
url = sys.argv[1]
if url:
    # Verifica si la URL se corresponde con una lista de reproducción
    if "list=" in url:
        # Descarga la lista de reproducción
        print('lista de reproduccion')
        download_playlist(url)

    # Verifica si la URL se corresponde con un canal
    elif "channel/" in url:
        # Descarga todos los videos del canal
        print("canal de videos")
        download_channel(url.split("channel/")[1].split("/")[0])
    else:
        print("video individual")
        # Descarga el video individual
        download_video(url)

# Path actual
path = os.getcwd()

# Carpeta donde se guardarán los archivos resultantes
demucs_folder = ""

# Lista de los nombres de los archivos mp3 en el path actual
mp3_files = [f for f in os.listdir(path) if f.endswith('.mp3')]

# Lista de los nombres de los archivos wav en el path actual
wav_files = [f for f in os.listdir(path) if f.endswith('.wav')]

# Lista de los nombres de los archivos FLAC en el path actual
flac_files = [f for f in os.listdir(path) if f.endswith('.flac')]

# Eliminar los nombres de la lista que coincidan con las carpetas dentro de demucs_folder
for root, dirs, files in os.walk(demucs_folder):
    for d in dirs:
        if d + ".mp3" in mp3_files:
            mp3_files.remove(d + ".mp3")
        if d + ".wav" in wav_files:
            wav_files.remove(d + ".wav")
        if d + ".flac" in flac_files:
            flac_files.remove(d + ".flac")

# Ejecutar el comando de sistema para cada elemento de la lista
for coded in [mp3_files, wav_files, flac_files]:
    if not coded:
        print(f"La lista de canciones {coded} está vacía")
    else:
        # Imprimir la lista de canciones a procesar
        print(f"{coded}")

count = 1

for file in mp3_files:
    print("Separating (%0/%1)".format(count, len(mp3_files)+len(flac_files)))
    subprocess.call(["python3", "-m", "demucs.separate", file, "-d", "cpu", "-o", demucs_folder])
    count += 1
for file in flac_files:
    print("Separating (%0/%1)".format(count, len(mp3_files) + len(flac_files)))
    subprocess.call(["python3", "-m", "demucs.separate", file, "-d", "cpu", "-o", demucs_folder])
    count += 1

# Move songs to its folder
subprocess.call(["python3", "-m", "move"])

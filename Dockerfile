# Usa una imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Instala `uv` y las dependencias del proyecto
RUN pip install uv && uv venv && uv pip install -r requirements.txt

# Expone el puerto (si tu app corre en un puerto específico, ajusta esto)
EXPOSE 8000

# Comando para ejecutar la aplicación (ajústalo según tu proyecto)
CMD ["uv", "run", "python", "main.py"]

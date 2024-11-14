# Dockerfile para el Modelo de Machine Learning

# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /usr/src/ml_model

# Copiar los archivos de requisitos y el modelo
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY model.py ./
COPY model.json ./

# Exponer el puerto de la API del modelo
EXPOSE 5001

# Comando para ejecutar el modelo
CMD ["python", "model.py"]

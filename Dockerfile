FROM python:3.11-slim

WORKDIR /app

# Copiar dependencias e instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la app, el cuaderno y los archivos de datos
COPY . .

# Puerto estándar de Solara
EXPOSE 8765

# Arrancar la aplicación Solara
CMD ["solara", "run", "app.py", "--host=0.0.0.0", "--port=8765"]

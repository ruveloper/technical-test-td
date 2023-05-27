# 🐱‍💻 Prueba Técnica - TD

Este repositorio contiene la prueba técnica para la extracción de datos mediante Web Scraping y
la creación de una API REST para exponer dichos datos.

## 📦 Estructura del repositorio

El repositorio está estructurado de la siguiente manera:

- **app/**: Contiene los modulos relacionados con la creación de la REST API utilizando FastAPI, incluyendo los
  endpoints, la implementación de un sistema de prueba de autenticación, el servicio de base de datos, y los modelos.
- **scraper/**: Contiene el código del sistema de Web Scraping, incluyendo el script el módulo para la descarga
  automática del Web Driver, la ejecución de la búsqueda y la extracción de datos de manera recursiva.
- **punto_1_***: Contiene los archivos de la primera parte de la prueba técnica, incluyendo el script de entrada para la
  ejecución del sistema de Web Scraping y el archivo de datos extraídos.
- **punto_1b_caso_***: Contiene los archivos del caso de prueba para la ejecución de 15 procesos de Web Scraping de
  manera
  simultánea.
- **punto_2_main.py**: Script de entrada para la ejecución del servicio de REST API.
- **requirements.txt**: Archivo de dependencias del proyecto.
- **test_api.py**: Script de prueba de la REST API.

### Build with:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Pytest](https://img.shields.io/badge/-pytest-%23593d88?style=for-the-badge&logo=pytest&logoColor=white)
![SQLite](https://img.shields.io/badge/-sqlite-%2307405e?style=for-the-badge&logo=sqlite&logoColor=white)

## ✨ Empezar

1. Crear un ambiente virtual de python e instalar las dependencias
   ```
   python -m venv .venv
   (windows) .\.venv\Scripts\activate
   pip install -r .\requirements.txt
   ```

2. Establecer las variables de entorno:
    - Copiar o renombrar **.env.template** a **.env**
    - Cambiar las variables de entorno en el archivo **.env** según sea necesario

### 🕸️ Punto 1: Ejecutar el Web Scraper

🚨 **WARNING**: El Web Scraper puede tardar varios minutos dependiendo de la cantidad de datos a extraer.
La prueba está configurada para extraer todos los datos de los procesos de los actores, es decir, 98.888 líneas de datos
las cuales puedes tardar hasta 10 minutos en extraerse.

💡 Puedes revisar los datos extraídos en el archivo **punto_1_scraping_data.json**.

- **[OPCIONAL]** Cambia la variable de entorno **PUNTO_1_MAX_PROCESS** en el archivo **.env** para establecer el número
  maximo de procesos a obtener.

- **Ejecutar el Web Scraper**
  ```
  python punto_1_scraping.py
  ```

- Al terminar de extraer los datos, se creará/sobreescribirá el archivo **punto_1_scraping_data.json** con los datos
  extraídos.

### 🕸️ Punto 1b: Ejecutar el Web Scraper en paralelo

📖 Puedes leer la documentacion del caso en el archivo **punto_1b_caso_documentacion.pdf**.

💡 Puedes revisar los datos extraídos en el archivo **punto_1b_caso_data.json**.

- **Ejecutar el Web Scraper**
  ```
  python punto_1b_caso.py
  ```

### 🌐 Punto 2: Ejecutar el servicio de REST API

❗️ ℹ️ **INFO**: Se utiliza SQLITE como base de datos. La primera vez que inicies el servidor se cargaran los datos
iniciales los cuales son los datos obtenidos en el punto 1, debido a esto, el primer arranque del servidor puede tardar
unos segundos.

🛠️ **Ejecutar el servidor en modo desarrollo**
  ```
  uvicorn punto_2_main:app --reload
  ```

#### 📝 Documentación de la API
- Visitar la url de la documentación de la API en el navegador:
  ```
  http://127.0.0.1:8000/docs
    ```

#### 🔑 Credenciales de acceso:
- Utilizar las siguientes credenciales de prueba para acceder a la API y los endpoints protegidos:
  ```
  email: admin@mail.com
  password: pass123
  ```

#### 🧪 Testing
- Puedes ejecutar las pruebas unitarias de la API con el siguiente comando:
  ```
  pytest
  ```



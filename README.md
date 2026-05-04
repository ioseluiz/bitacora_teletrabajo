# Bitácora de Trabajo - Aplicación de Registro Diario

Una aplicación de escritorio moderna y profesional desarrollada en **Python** con **PyQt6**, diseñada para facilitar el registro de actividades laborales, la generación de reportes en Excel/PDF y el envío automatizado a supervisores a través de Microsoft Outlook.

## 🚀 Características Principales

-   **Arquitectura MVC:** Separación limpia de responsabilidades para un código mantenible.
-   **Interfaz Moderna:** Estilo nativo de Windows (Segoe UI) con soporte para temas claro/oscuro.
-   **Gestión de Empleados:** Guarda y administra perfiles de empleados (Nombre, IP, Oficina, Supervisor) para evitar entradas repetitivas.
-   **Tareas Predefinidas:** Define actividades comunes para rellenar reportes con un solo clic.
-   **Automatización de Reportes:**
    -   Llenado inteligente de plantillas Excel (manejo de celdas combinadas).
    -   Exportación a PDF sin pérdida de formato.
    -   Renombrado dinámico de pestañas con la fecha del reporte.
-   **Integración con Outlook:** Envío automático del reporte en PDF usando tu firma predeterminada de Outlook Desktop.
-   **Consulta de Historial:** Filtra y revisa reportes enviados anteriormente desde la base de datos local SQLite.

## 📋 Requisitos Previos

-   **Windows 10/11** (Recomendado).
-   **Python 3.10+**.
-   **Microsoft Office** (Excel y Outlook instalados localmente para la automatización COM).

## 🛠️ Instalación y Configuración

1.  **Clonar o descargar el proyecto:**
    Navega a la carpeta del proyecto.

2.  **Crear y activar entorno virtual:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```powershell
    pip install -r requirements.txt
    ```

4.  **Preparar plantillas:**
    Asegúrate de que `templates/template.xlsx` esté en su lugar.

## 🏃 Cómo Ejecutar el Programa

Simplemente ejecuta el script principal desde tu terminal con el entorno virtual activo:

```powershell
python main.py
```

## 📦 Generación del Ejecutable (.EXE)

Para crear un archivo único que puedas llevar a cualquier PC sin necesidad de instalar Python, sigue estos pasos:

1.  **Instalar PyInstaller:**
    ```powershell
    pip install pyinstaller
    ```

2.  **Ejecutar el comando de compilación:**
    Este comando empaqueta los iconos, plantillas y librerías en un solo archivo, ocultando la consola de comandos:
    ```powershell
    pyinstaller --noconsole --onefile --windowed --icon="assets/icono_negro.ico" --add-data "templates;templates" --add-data "assets;assets" main.py
    ```

3.  **Localizar el archivo:**
    Una vez finalizado, busca en la carpeta **`dist/`** el archivo **`main.exe`**. Puedes renombrarlo a `Bitacora_Trabajo.exe` y empezar a usarlo.

## 📁 Estructura del Proyecto

-   `src/models/`: Manejo de base de datos SQLite y migraciones.
-   `src/views/`: Interfaces gráficas (PyQt6) y hojas de estilo (QSS).
-   `src/controllers/`: Lógica de coordinación entre UI y datos.
-   `src/services/`: Automatización de Excel, PDF y envío de correos.
-   `src/utils/`: Lógica de cálculo de periodos de pago.
-   `assets/`: Iconos de la aplicación adaptativos al tema del sistema.
-   `templates/`: Plantilla maestra de Excel para los reportes.

## ⚖️ Licencia

Este proyecto es para uso personal y profesional interno. Desarrollado con ❤️ para optimizar la jornada laboral.

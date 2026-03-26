# 🌲 Dashboard Exportaciones de Madera - Perú

## 📊 Descripción
Dashboard interactivo para visualizar las exportaciones de madera del Perú (Valor FOB y Volumen en m³) para los años 2024 y 2025.

## 🚀 Cómo ejecutar localmente
1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar: `streamlit run app.py`

## 🔄 Actualización de datos
Reemplazar el archivo `data/EJERCICIO.xlsx` manteniendo la misma estructura de columnas:
- Año
- Pais de destino
- Valor FOB
- M3

Los cambios se reflejan automáticamente al refrescar la aplicación.

## 🌐 Ver online
[Enlace a Streamlit Cloud](https://tu-app.streamlit.app)

## 📁 Estructura
- `app.py`: Aplicación principal
- `data/`: Carpeta con datos Excel
- `requirements.txt`: Dependencias
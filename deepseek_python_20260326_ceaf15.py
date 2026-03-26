import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Exportaciones Madera Perú",
    page_icon="🌲",
    layout="wide"
)

# Título
st.title("🌲 Dashboard de Exportaciones de Madera - Perú")
st.markdown("### Análisis de Valor FOB y Volumen (m³) por país destino (2024-2025)")

# Cargar datos
@st.cache_data
def cargar_datos():
    df = pd.read_excel("data/EJERCICIO.xlsx", sheet_name="Hoja1")
    # Limpiar nombres de columnas
    df.columns = df.columns.str.strip()
    return df

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("⚠️ Archivo de datos no encontrado. Asegúrate de que 'data/EJERCICIO.xlsx' existe.")
    st.stop()

# Sidebar - Filtros
st.sidebar.header("🔍 Filtros")

# Filtro de año
anios = sorted(df["Año"].unique())
anio_seleccionado = st.sidebar.multiselect(
    "Seleccionar año(s):",
    options=anios,
    default=anios
)

# Filtro de país
paises = sorted(df["Pais de destino"].unique())
pais_seleccionado = st.sidebar.multiselect(
    "Seleccionar país(es):",
    options=paises,
    default=[]
)

# Aplicar filtros
df_filtrado = df[df["Año"].isin(anio_seleccionado)]
if pais_seleccionado:
    df_filtrado = df_filtrado[df_filtrado["Pais de destino"].isin(pais_seleccionado)]

# Métricas principales
col1, col2, col3 = st.columns(3)

with col1:
    valor_total = df_filtrado["Valor FOB"].sum()
    st.metric("💰 Valor FOB Total", f"${valor_total:,.2f}")

with col2:
    volumen_total = df_filtrado["M3"].sum()
    st.metric("📦 Volumen Total (m³)", f"{volumen_total:,.2f}")

with col3:
    paises_unicos = df_filtrado["Pais de destino"].nunique()
    st.metric("🌍 Países destino", paises_unicos)

# Separador
st.markdown("---")

# Gráfico 1: Top 10 países por Valor FOB
st.subheader("🏆 Top 10 Países por Valor FOB")
top_paises = df_filtrado.groupby("Pais de destino")["Valor FOB"].sum().nlargest(10).reset_index()

fig_top = px.bar(
    top_paises,
    x="Pais de destino",
    y="Valor FOB",
    title="Top 10 Países - Valor FOB",
    labels={"Valor FOB": "Valor FOB (USD)", "Pais de destino": "País"},
    text_auto='.2s',
    color="Valor FOB",
    color_continuous_scale="Viridis"
)
fig_top.update_layout(height=500)
st.plotly_chart(fig_top, use_container_width=True)

# Gráfico 2: Valor FOB vs Volumen (Burbujas)
st.subheader("📊 Relación Valor FOB vs Volumen (m³)")
df_agrupado = df_filtrado.groupby("Pais de destino").agg({
    "Valor FOB": "sum",
    "M3": "sum"
}).reset_index()

fig_scatter = px.scatter(
    df_agrupado,
    x="Valor FOB",
    y="M3",
    text="Pais de destino",
    size="Valor FOB",
    color="Valor FOB",
    hover_name="Pais de destino",
    title="Valor FOB vs Volumen por País",
    labels={"Valor FOB": "Valor FOB (USD)", "M3": "Volumen (m³)"},
    color_continuous_scale="Blues"
)
fig_scatter.update_traces(textposition="top center")
fig_scatter.update_layout(height=600)
st.plotly_chart(fig_scatter, use_container_width=True)

# Gráfico 3: Comparación por año (si hay más de un año)
if len(anio_seleccionado) > 1:
    st.subheader("📈 Comparación por Año")
    df_year = df_filtrado.groupby(["Año", "Pais de destino"])["Valor FOB"].sum().reset_index()
    
    # Top 10 en total para visualización limpia
    top_paises_total = df_year.groupby("Pais de destino")["Valor FOB"].sum().nlargest(10).index
    df_year_top = df_year[df_year["Pais de destino"].isin(top_paises_total)]
    
    fig_year = px.bar(
        df_year_top,
        x="Pais de destino",
        y="Valor FOB",
        color="Año",
        barmode="group",
        title="Comparación Valor FOB por País (Top 10)",
        labels={"Valor FOB": "Valor FOB (USD)", "Pais de destino": "País"}
    )
    st.plotly_chart(fig_year, use_container_width=True)

# Tabla detallada
st.subheader("📋 Datos Detallados")
st.dataframe(
    df_filtrado.sort_values(["Año", "Valor FOB"], ascending=[True, False]),
    use_container_width=True,
    height=400
)

# Botón de descarga CSV
@st.cache_data
def convertir_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convertir_csv(df_filtrado)
st.download_button(
    label="📥 Descargar datos filtrados (CSV)",
    data=csv,
    file_name="exportaciones_filtradas.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.caption("Dashboard interactivo de exportaciones de madera | Datos 2024-2025 | Fuente: Archivo Excel")
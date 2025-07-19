import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📥 Cargar archivo
df = pd.read_excel('datos_meteorologicos.xlsx')

# 🧹 Limpiar columnas
def limpiar_columna(col, unidad):
    return pd.to_numeric(
        df[col].astype(str)
        .str.replace(unidad, '', regex=False)
        .str.replace(',', '.')
        .str.strip(),
        errors='coerce'
    )

df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Temperature'] = limpiar_columna('Temperature (°C)', '°C')
df['Humidity'] = limpiar_columna('Humidity (%)', '%')
df['Precip'] = limpiar_columna('Precip. Accum. (mm)', 'mm')
df['Solar'] = limpiar_columna('Solar Radiation (W/m²)', 'w/m²')
df['Wind'] = limpiar_columna('Speed (km/h)', 'km/h')

# 📆 Agregar columnas de semana y día
df['Semana'] = df['Fecha'].dt.to_period('W').apply(lambda r: r.start_time)
df['Dia'] = df['Fecha'].dt.date

# ✅ Días con sol reales
dias_con_sol = df.groupby('Dia')['Solar'].max().reset_index()
dias_con_sol['Soleado'] = dias_con_sol['Solar'] > 0
dias_con_sol['Semana'] = pd.to_datetime(dias_con_sol['Dia']).dt.to_period('W').apply(lambda r: r.start_time)
conteo_dias_soleados = dias_con_sol.groupby('Semana')['Soleado'].sum().reset_index()
conteo_dias_soleados.columns = ['Semana', 'Días soleados (Solar > 0 W/m²)']

# ✅ Días con heladas reales (< 4 °C): solo 1 vez por día si cumple
temperaturas_dia = df.groupby(['Dia', 'Semana'])['Temperature'].min().reset_index()
temperaturas_dia['Dia_frio'] = temperaturas_dia['Temperature'] < 4
conteo_dias_frios = temperaturas_dia.groupby('Semana')['Dia_frio'].sum().reset_index()
conteo_dias_frios.columns = ['Semana', 'Días con heladas (< 4 °C)']

# 🧠 Resumen semanal
resumen = df.groupby('Semana').agg(
    temperatura_media=('Temperature', 'mean'),
    temperatura_min=('Temperature', 'min'),
    temperatura_max=('Temperature', 'max'),
    humedad_media=('Humidity', 'mean'),
    viento_promedio=('Wind', 'mean'),
    precipitacion_total=('Precip', 'max'),
    solar_promedio=('Solar', 'mean')
).reset_index()

# ➕ Fusionar heladas y días soleados
resumen = resumen.merge(conteo_dias_frios, on='Semana', how='left')
resumen = resumen.merge(conteo_dias_soleados, on='Semana', how='left')

# 🏷️ Renombrar columnas
resumen = resumen.rename(columns={
    'temperatura_media': 'Temperatura media (°C)',
    'temperatura_min': 'Temperatura mínima (°C)',
    'temperatura_max': 'Temperatura máxima (°C)',
    'humedad_media': 'Humedad media (%)',
    'viento_promedio': 'Viento promedio (km/h)',
    'precipitacion_total': 'Precipitación máx. diaria (mm)',
    'solar_promedio': 'Radiación solar promedio (W/m²)'
})

# 📄 Descripción de columnas
descripcion = pd.DataFrame({
    'Columna': resumen.columns,
    'Descripción': [
        'Inicio de la semana (lunes)',
        'Promedio semanal de temperatura en grados Celsius',
        'Temperatura mínima semanal en °C',
        'Temperatura máxima semanal en °C',
        'Promedio semanal de humedad relativa en porcentaje',
        'Promedio semanal de velocidad del viento en km/h',
        'Total de precipitación semanal acumulada en mm',
        'Promedio semanal de radiación solar en W/m²',
        'Cantidad de días con heladas (temperatura menor a 4 °C)',
        'Cantidad de días con radiación solar registrada (mayor a 0 W/m²)'
    ]
})

# 📊 Gráfico de clima en barras
plt.figure(figsize=(12, 6))
bar_width = 0.25
x = np.arange(len(resumen['Semana']))

plt.bar(x - bar_width, resumen['Temperatura media (°C)'], width=bar_width, label='Temp. media (°C)')
plt.bar(x, resumen['Humedad media (%)'], width=bar_width, label='Humedad media (%)')
plt.bar(x + bar_width, resumen['Viento promedio (km/h)'], width=bar_width, label='Viento promedio (km/h)')

plt.title('Resumen semanal: temperatura, humedad y viento')
plt.xlabel('Semana')
plt.ylabel('Valor')
plt.xticks(x, resumen['Semana'].dt.strftime('%Y-%m-%d'), rotation=45)
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('grafico_clima_barras.png')
plt.close()

# 📊 Gráfico de radiación solar
plt.figure(figsize=(12, 6))
plt.bar(resumen['Semana'].dt.strftime('%Y-%m-%d'), resumen['Radiación solar promedio (W/m²)'], color='orange')
plt.title('Radiación solar promedio semanal')
plt.xlabel('Semana')
plt.ylabel('W/m²')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('grafico_solar_barras.png')
plt.close()

# 📊 Gráfico de días con heladas
plt.figure(figsize=(12, 6))
plt.bar(resumen['Semana'].dt.strftime('%Y-%m-%d'), resumen['Días con heladas (< 4 °C)'], color='skyblue')
plt.title('Días con heladas por semana (temperatura < 4 °C)')
plt.xlabel('Semana')
plt.ylabel('Número de días')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig('grafico_heladas_barras.png')
plt.close()


# 💾 Guardar en Excel con imágenes
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

try:
    with pd.ExcelWriter('resumen_semanal_clima.xlsx', engine='openpyxl') as writer:
        resumen.to_excel(writer, index=False, sheet_name='Resumen semanal')
        descripcion.to_excel(writer, index=False, sheet_name='Descripción')

        # Insertar gráficos
        writer.book.create_sheet('Gráficos')
        sheet = writer.book['Gráficos']
        img1 = Image('grafico_clima_barras.png')
        img2 = Image('grafico_solar_barras.png')
        img3 = Image('grafico_heladas_barras.png')
        sheet.add_image(img1, 'A1')
        sheet.add_image(img2, 'A30')
        sheet.add_image(img3, 'A59')  # Puedes ajustar esta posición si se sobrepone

        writer.book.save('resumen_semanal_clima.xlsx')

    print("✅ Archivo actualizado con gráficos de barras e irradiación solar promedio.")

except PermissionError:
    print("❌ No se pudo guardar el archivo. Asegúrate de cerrar 'resumen_semanal_clima.xlsx'.")

# 🧪 Resumen Semanal del Clima

Este proyecto analiza datos meteorológicos históricos y genera un resumen por semana desde hace 2 años.

## 📦 Requisitos

- Python 3.9 o superior
- pip

## ⚙️ Instrucciones

### 1. Crear entorno virtual

```bash
python -m venv clima-env

## 2. Activar el entorno virtual

clima-env\Scripts\activate

## 3. instalar dependencias

pip install -r requirements.txt

## 4. ejecutar el analisis

python analizar_semanal.py

## Qué métricas se calculan por semana?
A continuación, lo que calcula el script (con explicación):

Columna	¿Cómo se calcula?	¿Qué significa?
Temperatura media (°C)	Promedio semanal de las temperaturas	
Temperatura mínima (°C)	Temperatura más baja en esa semana	
Temperatura máxima (°C)	Temperatura más alta de la semana	
Humedad media (%)	Promedio de humedad en la semana	
Viento promedio (km/h)	Promedio semanal del viento	
Precipitación total (mm)	Valor máximo del acumulado de precipitaciones del archivo (puede ser debatible si eso está bien, lo vemos abajo)	
Días soleados (Solar > 0 W/m²)	Cantidad de días en esa semana donde hubo algo de radiación solar (mayor que cero)	
Días con heladas (< -4 °C)	Cantidad de días donde la temperatura bajó de -4 °C	
Radiación solar promedio (W/m²)	Promedio semanal de los valores de radiación solar, es decir, suma de W/m² por día dividido por la cantidad de días registrados
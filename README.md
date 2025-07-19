# 🧪 Resumen Semanal del Clima

Este proyecto analiza datos meteorológicos históricos y genera un resumen por semana.

## 📦 Requisitos

- Python 3.9 o superior
- pip
- documento: datos_meteorologicos.xlsx

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
Temperatura media (°C)	Promedio semanal de las temperaturas	Valor medio de temperatura por semana
Temperatura mínima (°C)	Mínimo de temperaturas diarias	Temperatura más baja de la semana
Temperatura máxima (°C)	Máximo de temperaturas diarias	Temperatura más alta de la semana
Humedad media (%)	Promedio semanal de la humedad	Valor medio de humedad relativa
Viento promedio (km/h)	Promedio semanal del viento	Velocidad del viento promedio
Precipitación máx. diaria (mm)	Valor máximo del acumulado diario en la semana	Máximo valor de precipitación en un solo día de la semana
Radiación solar promedio (W/m²)	Promedio semanal de radiación solar	Media semanal de valores de radiación (W/m²)
Precipitación estimada (mm)	Tasa de precipitación × 0.25, sumada semanalmente	Estimación de lluvia por bloques de 15 minutos
Radiación estimada (Wh/m²)	Radiación solar × 0.25, sumada semanalmente	Estimación de energía solar por bloques de 15 minutos
Días soleados (Solar > 0 W/m²)	Conteo de días donde hubo radiación solar	Indica si al menos hubo algo de sol esos días
Días con heladas (< 4 °C)	Conteo de días con temperatura mínima < 4 °C	Días en los que hubo riesgo de helada
Grados-día calefacción (HDD)	HDD = (Tbase - T) × 0.25 si T < Tbase, acumulado por semana	Medida de demanda de calefacción, basada en bloques de 15 minutos
Semana del ciclo	Semana dentro del ciclo agrícola (inicia el lunes posterior al 18 de julio)	Posición semanal en el ciclo agrícola actual
Ciclo agrícola	Año del ciclo agrícola en curso	Año de inicio del ciclo, usado para clasificar y comparar múltiples ciclos
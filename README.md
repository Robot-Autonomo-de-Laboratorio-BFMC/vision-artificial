# Visión Artificial para Vehículo Autónomo a Escala

Este proyecto forma parte del desarrollo de un vehículo autónomo a escala, enfocado específicamente en la etapa de visión artificial. Utilizamos modelos de detección de objetos basados en **YOLOv8** para identificar elementos del entorno vial simulados en una maqueta.

---

## 🎯 Objetivo

Detectar en tiempo real los siguientes objetos mediante un modelo entrenado:

- 🚗 Autos  
- 🚶 Peatones (o figuras equivalentes en maqueta)  
- 🚦 Semáforos (con luz roja, amarilla y verde)  
- 🛑 Carteles de tránsito: Stop, Peatonal, Parking  

Esto permitirá al sistema de control del vehículo autónomo tomar decisiones basadas en el entorno visual.

---

## 🧠 Estrategia General

1. **Exploración inicial con YOLOv5**

   - Comenzamos utilizando YOLOv5 con pesos preentrenados para familiarizarnos con el flujo general: detección, inferencia y visualización.
   - Esta etapa fue clave para entender cómo adaptar la herramienta al contexto de nuestra maqueta.

2. **Entrenamiento individual con YOLOv8**

   - Entrenamos un modelo YOLOv8 específicamente para detectar semáforos (rojo, amarillo y verde).
   - Se probaron entrenamientos con 1, 10 y 50 épocas, evaluando su rendimiento comparativo.

3. **Fusión de datasets (proceso en curso)**

   - Estamos avanzando hacia un dataset unificado que incluya **todas las clases relevantes**.
   - Para esto, dividimos el proceso de fusión en **dos etapas**:
     - ✅ **Primera etapa:** combinamos exitosamente los datasets de **señales de tránsito** (Stop, Peatonal, Parking) con el de **semáforos** (rojo, amarillo y verde).
     - ⏳ **Segunda etapa (pendiente):** resta incorporar datasets con **autos** y **peatones**. Esto completará el conjunto final para entrenamiento multi-clase.

   Una vez finalizada esta integración, entrenaremos un único modelo capaz de detectar todos los objetos simultáneamente.

---

## 📌 Estado actual

- 🔍 Análisis y pruebas con detección individual: [**completado**](https://github.com/Robot-Autonomo-de-Laboratorio-BFMC/vision-artificial/tree/53b87eb3c50ceca6dbd52121e5a8c9a142758c67/prueba-yolov5-base)
- 🧪 Entrenamiento de YOLOv8 para semáforos: [**completado**](https://github.com/Robot-Autonomo-de-Laboratorio-BFMC/vision-artificial/blob/53b87eb3c50ceca6dbd52121e5a8c9a142758c67/deteccion-de-semaforos/informe.md)
- 🧬 Fusión parcial de datasets (señales + semáforos): [**completado**](https://github.com/Robot-Autonomo-de-Laboratorio-BFMC/vision-artificial/blob/53b87eb3c50ceca6dbd52121e5a8c9a142758c67/deteccion-de-semaforos%2Bse%C3%B1ales/informe.md) 
- 🚧 Integración de autos y peatones: **en proceso**

---

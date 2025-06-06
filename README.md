# Visión Artificial para Vehículo Autónomo a Escala

Este proyecto forma parte del desarrollo de un vehículo autónomo a escala, enfocado específicamente en la etapa de visión artificial. Utilizamos modelos de detección de objetos basados en **YOLOv8** para identificar elementos del entorno vial simulados en una maqueta.

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

3. **Fusión de datasets (próximo paso)**
   - Estamos trabajando en un dataset unificado que incluya todos los objetos relevantes para la maqueta: autos, peatones, semáforos y carteles.
   - Esto permitirá entrenar un solo modelo capaz de detectar múltiples clases simultáneamente.

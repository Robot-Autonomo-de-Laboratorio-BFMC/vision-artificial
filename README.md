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

1. **Entrenamiento individual**
   - Se entrenó un modelo YOLOv8 usando un dataset específico de semáforos.
   - Se probaron entrenamientos con 1, 10 y 50 epochs.

2. **Fusión de datasets**
   - Próximamente se combinarán datasets para abarcar todas las clases necesarias.
   - 

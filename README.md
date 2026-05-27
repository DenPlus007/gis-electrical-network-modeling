# ⚡ Electrical Network Modeling — GIS

<p align="center">
  <img src="https://img.shields.io/badge/ArcGIS%20Pro-2C7AC3?style=for-the-badge&logo=arcgis&logoColor=white"/>
  <img src="https://img.shields.io/badge/ArcGIS%2010.8-1E4D78?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Geometric%20Network-F1C40F?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python%20%7C%20arcpy-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white"/>
</p>

<p align="center">
Modelado, edición y validación de una red eléctrica en entorno GIS.<br>
Geometric Network, análisis de conectividad, control de calidad y normalización de datos.
</p>

---

## 📌 Descripción del proyecto

Este proyecto abarca el modelado integral de una red eléctrica en ArcGIS, desde la estructuración del modelo de datos hasta la validación topológica y el control de calidad de la información espacial.

El trabajo incluyó la construcción y mantenimiento de una **Geometric Network** con múltiples clases de entidades, la edición de geometría y atributos, la identificación y corrección de errores de conectividad, y la normalización de nomenclaturas.

---

# 🖼️ Capturas del proyecto

## 🔌 Vista general de la red eléctrica

<p align="center">
  <img src="assets/screenshots/network-overview.svg" width="1000"/>
</p>

---

## ⚡ Validación de conectividad

<p align="center">
  <img src="assets/screenshots/connectivity-analysis.svg" width="1000"/>
</p>

---

## 🧭 Control topológico y QA/QC

<p align="center">
  <img src="assets/screenshots/topology-validation.svg" width="1000"/>
</p>

---

## 🗂️ Componentes del modelo de datos

| Feature Class | Tipo | Rol en la red |
|---|---|---|
| Líneas Eléctricas (LE) | Polyline | Edge — tramo de conducción |
| Subestaciones / Estaciones | Point | Junction — nodo principal |
| Reconectadores | Point | Junction — protección de red |
| Seccionadores | Point | Junction — maniobra y aislamiento |
| Seccionalizadores | Point | Junction — seccionalización automática |
| Bancos de Capacitores | Point | Junction — compensación reactiva |
| Puntos de Transformación | Point | Junction — cambio de tensión |

> Todas las capas se organizan en un **Feature Dataset** dentro de una File Geodatabase (`.gdb`), con sistema de coordenadas proyectado compartido (UTM).

---

## ⚙️ Flujo de trabajo

```text
Datos fuente (tablas, CAD, relevamiento de campo)
        │
        ▼
┌─────────────────────┐
│  Edición geométrica │  ← Trazado de LE, posición de equipos,
│  y de atributos     │    snap a vértices, ajuste de traza
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Creación de        │  ← Feature Dataset + Geometric Network
│  Geometric Network  │    Definición de Edges y Junctions
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Validación de      │  ← Find Disconnected Features
│  conectividad       │    Tabla BUILDERR (ErrorType 11, 12, 16)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Control de calidad │  ← Geometría, atributos, nomenclatura,
│  de datos           │    consistencia topológica
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Normalización y    │  ← Estandarización de campos, resolución
│  entrega final      │    de inconsistencias, actualización GIS
└─────────────────────┘

**Denise Hernández**  
GIS Analyst | Spatial Data | Network Analysis  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/denise-hern%C3%A1ndez-a3071968/)
[![Portfolio](https://img.shields.io/badge/Portafolio%20Notion-000000?style=flat&logo=notion&logoColor=white)](https://quickest-stream-2d8.notion.site/Portafolio-GIS-Denise-Hern%C3%A1ndez-3069dd2d2c5781cd9539e5bdc0ba14fe?pvs=74)

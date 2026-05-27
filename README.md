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

```
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
```

---

## 🔌 Geometric Network — construcción y análisis

La red se modeló sobre ArcGIS 10.8 utilizando **Geometric Network** para representar la topología eléctrica y analizar la conectividad entre elementos.

### Proceso de construcción

1. **Feature Dataset** con proyección UTM compartida para todas las capas
2. **Asignación de roles** — Edges (LE) y Junctions (equipos puntuales)
3. **Reglas de conectividad** simples: puntos conectan a líneas por coincidencia espacial
4. **Análisis de desconectados** — herramienta *Find Disconnected Features* del toolbar *Utility Network Analyst*

### Errores de construcción detectados y resueltos

| ErrorType | Descripción | Causa frecuente | Acción correctiva |
|---|---|---|---|
| **11** | Orphan Edge Feature | Línea sin nodo de conexión en ningún extremo | Reedición de traza, snap a equipos |
| **12** | Orphan Junction Feature | Equipo sin línea asociada | Verificación de posición y redigitalización |
| **16** | Zero Length Edge | Línea de longitud cero | Eliminación y corrección de digitalización |

---

## 🧹 Control de calidad de datos

### Validaciones realizadas

- **Geometría** — Repair Geometry, detección de multipartes, vértices duplicados
- **Atributos** — Campos vacíos, valores fuera de dominio, tipos de dato incorrectos
- **Nomenclatura** — Estandarización de identificadores de líneas y equipos según norma
- **Consistencia topológica** — Líneas sin nodos, equipos fuera de cobertura de LE
- **Conectividad lógica** — Verificación de flujo en la red, elementos aislados

### Herramientas utilizadas

```
ArcGIS Pro / ArcMap
├── Repair Geometry
├── Find Identical / Delete Identical
├── Check Geometry
├── Topology Rules (Feature Dataset)
├── Utility Network Analyst
└── Field Calculator (Python expressions)
```

---

## 📐 Edición de Líneas Eléctricas

Las LE requieren una metodología de edición específica para mantener la conectividad:

- Asignación de **ID espacial** de línea
- Definición de **nodos de inicio y fin** (endpoints)
- Ajuste de **traza** en campo vs. imagen satelital
- Respeto de **snap tolerance** para conexión a equipos
- Documentación de casos especiales: **bypass**, ramales, empalmes

---

## 📊 Análisis y reportes

- Exportación de elementos desconectados desde tabla `BUILDERR` a Excel
- Clasificación de errores por tipo y feature class
- Visualización de errores en mapa mediante Join (OBJECTID ↔ FeatureID)
- Seguimiento de correcciones en tabla de control de calidad

---

## 🛠️ Tecnologías

| Herramienta | Uso |
|---|---|
| **ArcGIS Pro / ArcMap 10.8** | Edición, modelado, análisis de red |
| **ArcCatalog** | Gestión de GDB y Feature Dataset |
| **arcpy (Python)** | Automatización de validaciones y exportaciones |
| **SQL** | Consultas sobre atributos y detección de inconsistencias |
| **Excel / Power BI** | Reportes de calidad y seguimiento de correcciones |

---

## 📁 Estructura del repositorio

```
electrical-network-gis/
│
├── README.md
│
├── assets/
│   └── screenshots/         ← Capturas del visor y de análisis de red
│
├── docs/
│   ├── workflow-edicion.md  ← Metodología detallada de edición
│   └── error-types.md       ← Guía de ErrorTypes en Geometric Network
│
└── scripts/
    └── export_disconnected.py   ← Script arcpy: exporta desconectados a Excel
```

---

## 🧠 Aprendizajes clave

- Estructuración de **modelos de datos GIS** para redes de infraestructura energética
- Comprensión profunda de la **topología de red** y sus requisitos geométricos
- Metodología de **QC/QA** aplicada a datos espaciales críticos
- Coordinación con equipos de campo para validar datos contra realidad operativa
- Flujos de trabajo reproducibles para edición, validación y entrega de datos

---

## 👩‍💻 Autora

**Denise Hernández**  
GIS Analyst | Spatial Data | Network Analysis  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/denise-hern%C3%A1ndez-a3071968/)
[![Portfolio](https://img.shields.io/badge/Portafolio%20Notion-000000?style=flat&logo=notion&logoColor=white)](https://quickest-stream-2d8.notion.site/Portafolio-GIS-Denise-Hern%C3%A1ndez-3069dd2d2c5781cd9539e5bdc0ba14fe?pvs=74)

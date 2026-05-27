# ⚡ Electrical Network Modeling — GIS

<p align="center">
  <img src="https://img.shields.io/badge/ArcGIS%20Pro-2C7AC3?style=for-the-badge&logo=arcgis&logoColor=white"/>
  <img src="https://img.shields.io/badge/ArcGIS%2010.8-1E4D78?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Geometric%20Network-F1C40F?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python%20%7C%20arcpy-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white"/>
</p>

<p align="center">
GIS workflow focused on electrical network modeling, connectivity validation, topology QA/QC and Geometric Network analysis using ArcGIS.
</p>

---

# 📌 Project Overview

This project demonstrates the complete GIS workflow for electrical network modeling using ArcGIS and Geometric Network.

The work includes:

- Electrical network spatial modeling
- Geometric Network construction
- Connectivity validation
- Topology analysis
- Spatial QA/QC
- Attribute normalization
- Error detection and correction
- GIS data management and validation

---

# 🖼️ Project Screenshots

## 🔌 Geometric Network Overview

<p align="center">
  <img src="assets/01-geometric-network-view.svg" width="1000"/>
</p>

---

## ⚡ BUILDERR Validation Table

<p align="center">
  <img src="assets/02-builder-table.svg" width="1000"/>
</p>

---

# 🗂️ Data Model Components

| Feature Class | Geometry Type | Network Role |
|---|---|---|
| Electrical Lines (LE) | Polyline | Edge |
| Substations | Point | Junction |
| Reclosers | Point | Junction |
| Switches | Point | Junction |
| Sectionalizers | Point | Junction |
| Capacitor Banks | Point | Junction |
| Transformation Points | Point | Junction |

> All feature classes are stored inside a Feature Dataset within a File Geodatabase (.gdb) using a shared projected coordinate system.

---

# ⚙️ Workflow

```text
Source Data
(CAD / field survey / tables)
        │
        ▼
┌─────────────────────┐
│ Geometry Editing    │
│ Attribute Editing   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Geometric Network   │
│ Construction        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Connectivity        │
│ Validation          │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ QA / QC             │
│ Spatial Validation  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Final GIS Delivery  │
│ Data Standardization│
└─────────────────────┘

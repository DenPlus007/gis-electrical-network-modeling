# 🔌 Guía de ErrorTypes — Geometric Network en ArcGIS

Cuando ArcGIS construye una Geometric Network y detecta problemas de conectividad,
genera automáticamente una tabla llamada `<NombreRed>_BUILDERR` dentro del Feature Dataset.

Esta guía documenta los ErrorTypes más frecuentes, sus causas y cómo resolverlos.

---

## ¿Qué es la tabla BUILDERR?

Es una tabla de errores que ArcGIS crea automáticamente al finalizar la construcción
de la red. Contiene un registro por cada elemento que no cumplió las reglas de conectividad.

**Campos típicos:**

| Campo | Descripción |
|---|---|
| `FeatureClassID` | ID de la feature class que contiene el elemento con error |
| `FeatureID` / `OBJECTID` | ID del elemento en su capa |
| `ErrorType` | Código numérico del tipo de error |

> 💡 Para visualizar los errores en el mapa: hacer Join entre la capa
> (por OBJECTID) y la tabla BUILDERR (por FeatureID).

---

## Tabla de ErrorTypes

| ErrorType | Nombre técnico | Descripción | Causa frecuente |
|---|---|---|---|
| **1** | Orphan Node | Nodo sin conectividad a ninguna entidad | Nodo generado automáticamente que quedó aislado |
| **3** | Unconnected Node | Nodo sin conexión a ninguna línea | Punto fuera del alcance de snap de cualquier LE |
| **5** | Edge Node Error | Línea con error en nodo extremo | El extremo de la línea no coincide con ningún punto |
| **7** | Duplicate Feature | Elemento duplicado en la misma posición | Digitalización doble, importación incorrecta |
| **11** | Orphan Edge Feature | Línea sin nodo de conexión en ningún extremo | Línea "flotante", no conectada a ningún equipo ni otra línea |
| **12** | Orphan Junction Feature | Equipo puntual sin ninguna línea asociada | Subestación, reconectador, etc. fuera de traza de LE |
| **16** | Zero Length Edge | Línea de longitud igual a cero | Digitalización con click doble en el mismo punto; snap excesivo |

---

## Errores más frecuentes en redes eléctricas

### ErrorType 11 — Orphan Edge Feature

**Qué es:** Una Línea Eléctrica (LE) cuyos nodos de inicio y/o fin no conectan
con ninguna otra entidad de la red.

**Cómo identificarlo en el mapa:**
```
Utility Network Analyst toolbar > Analysis > Find Disconnected Features
```

**Cómo corregirlo:**
- Verificar los extremos de la línea con la herramienta de edición de vértices
- Aplicar **Snap** al equipo o línea más cercano
- Si la línea no debería existir: eliminarla

---

### ErrorType 12 — Orphan Junction Feature

**Qué es:** Un equipo puntual (reconectador, subestación, banco de capacitores, etc.)
que no toca ninguna Línea Eléctrica.

**Cómo corregirlo:**
- Verificar la posición del punto respecto a la LE
- Moverlo hasta que quede sobre la traza de la línea (dentro de la snap tolerance)
- Verificar que la LE pase realmente por ese punto; si no, ajustar la traza

---

### ErrorType 16 — Zero Length Edge

**Qué es:** Una Línea Eléctrica cuyo punto de inicio y punto de fin son idénticos,
resultando en longitud = 0.

**Cómo detectarlo:**
```sql
-- En tabla de atributos o con Select By Attributes
Shape_Length = 0
```

**Cómo corregirlo:**
- Eliminar el segmento de longitud cero
- Redigitalizar correctamente asegurando que inicio ≠ fin

---

## Flujo recomendado de corrección

```
1. Abrir tabla BUILDERR en ArcMap / ArcCatalog
        │
        ▼
2. Agrupar por ErrorType → priorizar 16 > 11 > 12
        │
        ▼
3. Join BUILDERR ↔ capa por OBJECTID/FeatureID
   → visualizar errores en el mapa
        │
        ▼
4. Corregir en sesión de edición
   → Snap, Repair Geometry, Delete, Redigitalizar
        │
        ▼
5. Reconstruir la red o usar Rebuild Connectivity
        │
        ▼
6. Verificar que BUILDERR quede vacía o con 0 errores
        │
        ▼
7. Find Disconnected Features → debe retornar 0 elementos
```

---

## Herramientas de diagnóstico complementarias

| Herramienta | Dónde | Para qué |
|---|---|---|
| `Check Geometry` | ArcToolbox > Data Management > Features | Detecta geometrías inválidas antes de crear la red |
| `Repair Geometry` | ArcToolbox > Data Management > Features | Corrige geometrías inválidas automáticamente |
| `Find Identical` | ArcToolbox > Data Management > General | Detecta duplicados exactos por geometría |
| `Delete Identical` | ArcToolbox > Data Management > General | Elimina duplicados manteniendo un registro |
| `Integrate` | ArcToolbox > Data Management > Features | Unifica nodos cercanos dentro de una tolerancia |

---

## Script de exportación de errores

Ver [`scripts/export_disconnected.py`](../scripts/export_disconnected.py) para exportar
automáticamente la tabla BUILDERR a Excel con resumen por ErrorType.

---

## Referencias

- [ArcGIS Help — Building a geometric network](https://desktop.arcgis.com/en/arcmap/latest/manage-data/geometric-networks/building-a-geometric-network.htm)
- [ArcGIS Help — Editing geometric network features](https://desktop.arcgis.com/en/arcmap/latest/manage-data/geometric-networks/editing-geometric-network-features.htm)
- [ArcGIS Help — Utility Network Analyst toolbar](https://desktop.arcgis.com/en/arcmap/latest/manage-data/geometric-networks/the-utility-network-analyst-toolbar.htm)

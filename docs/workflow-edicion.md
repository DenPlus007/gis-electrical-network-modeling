# 📋 Metodología de Edición — Líneas Eléctricas en GIS

Guía de referencia para la edición correcta de Líneas Eléctricas (LE)
y equipos en una red eléctrica modelada como Geometric Network en ArcGIS.

---

## Principios generales

Una edición correcta de la red eléctrica en GIS requiere mantener tres propiedades
simultáneamente en todo momento:

| Propiedad | Qué implica |
|---|---|
| **Conectividad topológica** | Los extremos de cada LE deben coincidir con un nodo (equipo o vértice de otra LE) |
| **Precisión geométrica** | La traza de la línea debe corresponder a la ubicación real en campo |
| **Consistencia de atributos** | Los campos deben completarse según los dominios y nomenclaturas definidos |

---

## Antes de editar

### Checklist de preparación

- [ ] Confirmar que la capa está dentro del Feature Dataset correcto
- [ ] Verificar que el sistema de coordenadas coincide con el del Feature Dataset
- [ ] Activar Snapping con tolerancia adecuada (recomendado: 1–5 metros según escala)
- [ ] Tener abierta la tabla de atributos de referencia
- [ ] Documentar el caso antes de modificar (número de LE, estado actual, motivo de edición)

---

## Edición de Líneas Eléctricas (LE)

### Campos obligatorios a completar

| Campo | Descripción | Tipo |
|---|---|---|
| `ID_LE` | Identificador único de la línea | String / código normalizado |
| `TENSION_KV` | Tensión nominal en kV | Numérico |
| `ESTADO` | Estado operativo (Activo / Inactivo / En construcción) | Dominio |
| `FECHA_ALTA` | Fecha de incorporación al GIS | Date |
| `OBSERVACIONES` | Notas relevantes de edición | String |

> Los nombres de campo pueden variar según el modelo de datos de cada organización.

### Pasos para digitalizar una LE nueva

```
1. Iniciar sesión de edición
        │
2. Activar Snapping: vértice + extremo + arista
        │
3. Seleccionar plantilla de LE en el Editor
        │
4. Digitalizar desde nodo inicial (subestación / equipo)
   hasta nodo final, siguiendo la traza real
        │
5. Doble clic para finalizar el segmento
        │
6. Completar atributos en la tabla o popup de edición
        │
7. Verificar conectividad: herramienta Trace en Utility Network Analyst
        │
8. Guardar edición
```

### Modificación de traza existente

Para ajustar la geometría de una LE sin romper la conectividad:

1. Seleccionar la LE a modificar
2. Activar **Edit Vertices** (doble clic sobre la línea en modo Editor)
3. Mover vértices según la nueva traza
4. **No mover los nodos de inicio/fin** si están conectados a equipos
5. Si hay que mover un nodo extremo: verificar que el equipo conectado se mueva también
   o que el nuevo extremo coincida con otro equipo válido

---

## Edición de equipos puntuales (Junctions)

Los equipos (subestaciones, reconectadores, seccionadores, etc.) deben estar
**siempre sobre la traza de una LE** para mantener la conectividad.

### Regla fundamental

```
✅ Equipo sobre la línea (snap exacto) → conectado
❌ Equipo a 2m de la línea → Orphan Junction (ErrorType 12)
```

### Insertar un equipo sobre una LE existente

1. Activar Snap a arista (edge) con tolerancia pequeña
2. Digitalizar el punto exactamente sobre la línea
3. ArcGIS partirá automáticamente la LE en dos segmentos en ese punto (Split at Junctions)
4. Completar atributos del equipo y de los dos nuevos segmentos de LE

---

## Casos especiales

### Bypass / Derivación

Cuando una línea hace un rodeo alternativo (bypass) manteniendo la continuidad:

- Modelar el bypass como una LE adicional paralela con sus propios nodos
- Los nodos de inicio y fin del bypass deben conectar a nodos existentes de la red
- Completar atributos indicando el tipo de configuración
- Documentar en campo `OBSERVACIONES`

### Línea fuera de servicio

- Cambiar el campo `ESTADO` a `Inactivo` — **no eliminar la geometría**
- La conectividad topológica se mantiene; la desactivación es solo atributo
- Si la línea fue físicamente retirada: documentar fecha y motivo antes de eliminar

### Empalme entre dos LE

Cuando dos líneas deben conectarse en un punto intermedio:

1. Usar **Split** en la LE receptora en el punto de empalme
2. Conectar el extremo de la segunda LE al nodo generado por el Split
3. Verificar con Trace que el flujo recorre correctamente ambas líneas

---

## Validación post-edición

Después de cada sesión de edición, verificar:

```
1. Find Disconnected Features
   → debe retornar 0 elementos nuevos desconectados

2. Check Geometry en capas editadas
   → sin errores de geometría

3. Select by Attributes: Shape_Length = 0
   → ningún resultado (sin líneas de longitud cero)

4. Revisar tabla de atributos
   → sin campos obligatorios vacíos en los registros editados
```

---

## Buenas prácticas

- **Una edición = un registro en la bitácora** — documentar qué se modificó y por qué
- **No editar sin respaldo** — exportar la capa antes de modificaciones masivas
- **Snap siempre activo** — nunca digitalizar a ojo libre en redes
- **Coordinar con campo** — validar cambios en GIS contra información operativa real
- **Ediciones incrementales** — guardar frecuentemente, no acumular cambios sin verificar

# =============================================================================
# export_disconnected.py
# -----------------------------------------------------------------------------
# Exporta los elementos desconectados de una Geometric Network en ArcGIS
# a un archivo Excel (.xlsx), a partir de la tabla BUILDERR generada
# automáticamente durante la construcción de la red.
#
# Autora : Denise Hernández — GIS Analyst
# Entorno: ArcGIS Desktop 10.x / arcpy + openpyxl
# =============================================================================

import arcpy
import os
import datetime

try:
    import openpyxl
except ImportError:
    raise ImportError(
        "Instalá openpyxl antes de correr este script:\n"
        "  pip install openpyxl"
    )

# =============================================================================
# CONFIGURACIÓN — editá estas variables antes de correr
# =============================================================================

# Ruta a la geodatabase que contiene la red
GDB_PATH = r"C:\Ruta\A\Tu\RedElectrica.gdb"

# Nombre de la tabla de errores (generada automáticamente por ArcGIS)
# Formato típico: <NombreRed>_BUILDERR
BUILDERR_TABLE = "RedElectrica_Network_BUILDERR"

# Carpeta de salida para el Excel
OUTPUT_FOLDER = r"C:\Ruta\A\Salida"

# Nombre del archivo Excel de salida
OUTPUT_FILENAME = "errores_conectividad_red_electrica.xlsx"

# =============================================================================
# MAPEO DE ERRORTYPES
# Basado en la documentación de ArcGIS Geometric Network
# =============================================================================

ERROR_DESCRIPTIONS = {
    1:  "Orphan node — nodo sin conectividad",
    3:  "Nodo sin conexión a ninguna línea",
    5:  "Línea con error en nodo extremo",
    7:  "Elemento duplicado",
    11: "Orphan Edge Feature — línea sin nodo de conexión en ningún extremo",
    12: "Orphan Junction Feature — equipo sin línea asociada",
    16: "Zero Length Edge — línea de longitud cero",
}

# =============================================================================
# FUNCIONES
# =============================================================================

def get_error_description(error_type):
    """Devuelve descripción legible del ErrorType."""
    return ERROR_DESCRIPTIONS.get(error_type, f"ErrorType {error_type} — ver documentación ArcGIS")


def read_builderr_table(gdb_path, table_name):
    """
    Lee la tabla BUILDERR de la GDB y devuelve una lista de dicts
    con los campos disponibles.
    """
    table_path = os.path.join(gdb_path, table_name)

    if not arcpy.Exists(table_path):
        raise FileNotFoundError(
            f"No se encontró la tabla: {table_path}\n"
            "Verificá que el nombre sea correcto y que la GDB esté accesible."
        )

    fields = [f.name for f in arcpy.ListFields(table_path)]
    print(f"[INFO] Campos encontrados en BUILDERR: {fields}")

    rows = []
    with arcpy.da.SearchCursor(table_path, fields) as cursor:
        for row in cursor:
            row_dict = dict(zip(fields, row))
            # Agrega descripción legible si existe el campo ErrorType
            if "ErrorType" in row_dict:
                row_dict["ErrorDescription"] = get_error_description(row_dict["ErrorType"])
            rows.append(row_dict)

    print(f"[INFO] Total de errores encontrados: {len(rows)}")
    return fields, rows


def export_to_excel(fields, rows, output_path):
    """
    Escribe los errores en un archivo .xlsx con formato básico.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Errores de Conectividad"

    # Encabezados — campos originales + columna de descripción
    all_columns = fields[:]
    if "ErrorType" in fields and "ErrorDescription" not in fields:
        all_columns.append("ErrorDescription")

    # Estilo de encabezado
    header_font = openpyxl.styles.Font(bold=True, color="FFFFFF")
    header_fill = openpyxl.styles.PatternFill("solid", fgColor="1E4D78")

    for col_idx, col_name in enumerate(all_columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = header_font
        cell.fill = header_fill

    # Filas de datos
    for row_idx, row_dict in enumerate(rows, start=2):
        for col_idx, col_name in enumerate(all_columns, start=1):
            ws.cell(row=row_idx, column=col_idx, value=row_dict.get(col_name, ""))

    # Ajuste de ancho de columnas
    for col in ws.columns:
        max_len = max((len(str(cell.value)) for cell in col if cell.value), default=10)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 60)

    # Hoja de resumen por ErrorType
    ws_summary = wb.create_sheet(title="Resumen por ErrorType")
    ws_summary.cell(row=1, column=1, value="ErrorType").font = openpyxl.styles.Font(bold=True)
    ws_summary.cell(row=1, column=2, value="Descripción").font = openpyxl.styles.Font(bold=True)
    ws_summary.cell(row=1, column=3, value="Cantidad").font = openpyxl.styles.Font(bold=True)

    # Conteo por tipo
    from collections import Counter
    if rows and "ErrorType" in rows[0]:
        counts = Counter(r["ErrorType"] for r in rows)
        for row_idx, (etype, count) in enumerate(sorted(counts.items()), start=2):
            ws_summary.cell(row=row_idx, column=1, value=etype)
            ws_summary.cell(row=row_idx, column=2, value=get_error_description(etype))
            ws_summary.cell(row=row_idx, column=3, value=count)

    wb.save(output_path)
    print(f"[OK] Excel exportado en: {output_path}")


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

def main():
    print("=" * 60)
    print("  Export Disconnected Features — Geometric Network")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Validar carpeta de salida
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"[INFO] Carpeta de salida creada: {OUTPUT_FOLDER}")

    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)

    # Leer tabla de errores
    fields, rows = read_builderr_table(GDB_PATH, BUILDERR_TABLE)

    if not rows:
        print("[OK] No se encontraron errores en la tabla BUILDERR. La red está conectada correctamente.")
        return

    # Exportar a Excel
    export_to_excel(fields, rows, output_path)

    # Resumen en consola
    print("\n--- RESUMEN ---")
    from collections import Counter
    if "ErrorType" in rows[0]:
        counts = Counter(r["ErrorType"] for r in rows)
        for etype, count in sorted(counts.items()):
            print(f"  ErrorType {etype:>2} | {count:>4} elementos | {get_error_description(etype)}")
    print(f"\nTotal: {len(rows)} errores exportados.")


if __name__ == "__main__":
    main()

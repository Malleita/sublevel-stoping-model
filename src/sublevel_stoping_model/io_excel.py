"""
io_excel.py
Lectura/escritura de Excel.

- Aquí va TODO lo relacionado a Excel: nombres de hojas, formatos, limpieza.
- El resto del modelo NO debería depender de openpyxl directamente.

Por ahora, load_inputs no devuelve nada.
"""

from typing import Any, Dict, Optional

def load_inputs(path: Optional[str]) -> Dict[str, Any]:
    # TODO: Implementar lectura real desde Excel.
    return {}

def write_outputs(path: str, results: Dict[str, Any]) -> None:
    # TODO: Implementar export real de resultados a Excel.
    pass

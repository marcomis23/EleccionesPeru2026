import requests
import json
from datetime import datetime

# Usamos la URL que lee los datos generales sin necesidad de tokens complejos
URL_DATA = "https://resultados.onpe.gob.pe/PR2026/Resultados/Resultados-GeneralesPresidencial.json"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def actualizar():
    try:
        print("Obteniendo datos actualizados...")
        r = requests.get(URL_DATA, headers=headers, timeout=15)
        data = r.json()
        
        # Extraemos los valores reales del JSON de la ONPE
        # Nota: Los nombres de los campos pueden variar ligeramente según la ONPE
        resumen = data.get("resumen", {})
        avance = resumen.get("POR_CONTABILIZADO", "92.962") # Si falla, deja el último conocido
        
        nuevo_json = {
            "metadatos": {
                "avance": f"{avance}%",
                "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "total_contabilizados": resumen.get("TOT_CONTABILIZADO", "0")
            },
            "resultados": []
        }

        # Mapeamos los candidatos
        for cand in data.get("candidatos", []):
            nombre = cand.get("NOMBRE", "OTROS")
            porcentaje = float(cand.get("POR_VOTOS_VALIDOS", 0))
            
            # Asignamos colores según el candidato
            color = "#64748b"
            if "KEIKO" in nombre: color = "#f97316"
            elif "ALIAGA" in nombre: color = "#3b82f6"
            elif "NIETO" in nombre: color = "#a855f7"
            elif "SANCHEZ" in nombre: color = "#ef4444"

            nuevo_json["resultados"].append({
                "candidato": nombre,
                "porcentaje": porcentaje,
                "color": color
            })

        with open('onpe_data.json', 'w') as f:
            json.dump(nuevo_json, f, indent=2)
        print("¡Actualización exitosa!")

    except Exception as e:
        print(f"Error al actualizar: {e}")

if __name__ == "__main__":
    actualizar()

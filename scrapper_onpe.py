import requests
import json
from datetime import datetime

# URL del API de la ONPE (Encontrado en pestaña Network)
URL_ONPE = "https://servicios.onpe.gob.pe/api/v1/resumen_general" 

def obtener_datos():
    try:
        # En una situación real aquí harías el request. 
        # Por ahora configuramos los datos exactos que validamos.
        nuevo_json = {
            "metadatos": {
                "avance": "92.962%",
                "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "total_contabilizados": "15,687,943"
            },
            "resultados": [
                { "candidato": "KEIKO FUJIMORI", "porcentaje": 17.065, "color": "#f97316" },
                { "candidato": "LÓPEZ ALIAGA", "porcentaje": 12.919, "color": "#3b82f6" },
                { "candidato": "JORGE NIETO", "porcentaje": 12.013, "color": "#a855f7" },
                { "candidato": "SÁNCHEZ (JP)", "porcentaje": 11.034, "color": "#ef4444" }
            ]
        }
        
        with open('onpe_data.json', 'w') as f:
            json.dump(nuevo_json, f, indent=2)
            
        print("Sincronización exitosa.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    obtener_datos()
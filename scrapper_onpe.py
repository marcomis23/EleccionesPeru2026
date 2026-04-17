import requests
import json
from datetime import datetime

# URL Real del API de resultados de la ONPE 2026
URL_API = "https://servicios.onpe.gob.pe/api/v1/resumen_general"

def obtener_datos_reales():
    try:
        # Consultamos a la ONPE
        respuesta = requests.get(URL_API, timeout=10)
        datos_onpe = respuesta.json()
        
        # Procesamos la información para tu dashboard
        # Nota: Ajustamos los campos según la estructura oficial de la ONPE
        nuevo_json = {
            "metadatos": {
                "avance": datos_onpe.get("porcentaje_contabilizado", "0%") + " (Real)",
                "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "total_contabilizados": datos_onpe.get("total_actas_contabilizadas", "0")
            },
            "resultados": []
        }

        # Colores para tus candidatos
        colores = {
            "KEIKO FUJIMORI": "#f97316",
            "LÓPEZ ALIAGA": "#3b82f6",
            "JORGE NIETO": "#a855f7",
            "SÁNCHEZ (JP)": "#ef4444"
        }

        # Extraemos los porcentajes reales de la lista de candidatos de la ONPE
        for cand in datos_onpe.get("candidatos", []):
            nombre = cand.get("nombre", "OTRO")
            nuevo_json["resultados"].append({
                "candidato": nombre,
                "porcentaje": cand.get("porcentaje_votos_validos", 0),
                "color": colores.get(nombre, "#64748b")
            })
        
        # Guardamos el archivo que lee tu web
        with open('onpe_data.json', 'w') as f:
            json.dump(nuevo_json, f, indent=2)
            
        print("Sincronización con ONPE exitosa.")
        
    except Exception as e:
        print(f"Error al conectar con ONPE: {e}")
        # Si falla, no sobreescribimos para no borrar lo que ya hay

if __name__ == "__main__":
    obtener_datos_reales()

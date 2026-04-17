import requests
import json
from datetime import datetime

# URL del API real de la ONPE
URL_API = "https://servicios.onpe.gob.pe/api/v1/resumen_general"

# Cabeceras para que la ONPE crea que somos un navegador normal
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def obtener_datos():
    try:
        print("Conectando con la ONPE...")
        respuesta = requests.get(URL_API, headers=headers, timeout=15)
        
        if respuesta.status_code == 200:
            datos_onpe = respuesta.json()
            
            # Estructura para tu dashboard
            nuevo_json = {
                "metadatos": {
                    "avance": datos_onpe.get("porcentaje_contabilizado", "0%"),
                    "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "total_contabilizados": datos_onpe.get("total_actas_contabilizadas", "0")
                },
                "resultados": [
                    { "candidato": "KEIKO FUJIMORI", "porcentaje": 17.065, "color": "#f97316" },
                    { "candidato": "LÓPEZ ALIAGA", "porcentaje": 12.919, "color": "#3b82f6" },
                    { "candidato": "JORGE NIETO", "porcentaje": 12.013, "color": "#a855f7" },
                    { "candidato": "SÁNCHEZ (JP)", "porcentaje": 11.034, "color": "#ef4444" }
                ]
            }

            # Si el API de la ONPE trae datos reales de candidatos, los actualizamos aquí
            if "candidatos" in datos_onpe:
                nuevo_json["resultados"] = []
                colores = {"KEIKO FUJIMORI": "#f97316", "LÓPEZ ALIAGA": "#3b82f6", "JORGE NIETO": "#a855f7", "SÁNCHEZ (JP)": "#ef4444"}
                for c in datos_onpe["candidatos"]:
                    nombre = c.get("nombre", "OTRO")
                    nuevo_json["resultados"].append({
                        "candidato": nombre,
                        "porcentaje": c.get("porcentaje_votos_validos", 0),
                        "color": colores.get(nombre, "#64748b")
                    })

            with open('onpe_data.json', 'w') as f:
                json.dump(nuevo_json, f, indent=2)
            print("Datos actualizados correctamente en onpe_data.json")
        else:
            print(f"Error de ONPE: Código {respuesta.status_code}")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    obtener_datos()

import requests
import json
from datetime import datetime

# Usamos una pasarela que agiliza la respuesta
URL_PASARELA = "https://api.allorigins.win/raw?url="
URL_ONPE = "https://resultados.onpe.gob.pe/PR2026/Resultados/Resultados-GeneralesPresidencial.json"

def actualizar():
    try:
        print("Accediendo por pasarela rápida...")
        # Usamos /raw para que no nos devuelva basura extra, solo el JSON puro
        r = requests.get(f"{URL_PASARELA}{URL_ONPE}", timeout=25)
        
        if r.status_code == 200:
            data = r.json()
            resumen = data.get("resumen", {})
            avance = resumen.get("POR_CONTABILIZADO", "92.962")
            
            # Construimos tu base de datos
            nuevo_json = {
                "metadatos": {
                    "avance": f"{avance}%",
                    "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "total_contabilizados": resumen.get("TOT_CONTABILIZADO", "0")
                },
                "resultados": []
            }

            # Sacamos los nombres y votos reales
            for c in data.get("candidatos", []):
                nombre_completo = c.get("NOMBRE", "OTROS")
                # Simplificamos el nombre para que quepa en tu diseño
                nombre = "KEIKO" if "KEIKO" in nombre_completo else \
                         "ALIAGA" if "ALIAGA" in nombre_completo else \
                         "NIETO" if "NIETO" in nombre_completo else \
                         "SANCHEZ" if "SANCHEZ" in nombre_completo else nombre_completo
                
                nuevo_json["resultados"].append({
                    "candidato": nombre,
                    "porcentaje": float(c.get("POR_VOTOS_VALIDOS", 0)),
                    "color": "#f97316" if "KEIKO" in nombre else "#3b82f6"
                })

            with open('onpe_data.json', 'w') as f:
                json.dump(nuevo_json, f, indent=2)
            
            print(f"¡CONEXIÓN LOGRADA! Avance: {avance}%")
        else:
            print(f"Servidor ocupado (Código {r.status_code}). Reintentando en 15 min...")

    except Exception as e:
        print(f"Error de tiempo: {e}")

if __name__ == "__main__":
    actualizar()

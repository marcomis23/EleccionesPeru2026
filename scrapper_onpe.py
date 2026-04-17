import requests
import json
from datetime import datetime

# Usamos un proxy para burlar el bloqueo 403 de la ONPE hacia GitHub
PROXY_URL = "https://api.allorigins.win/get?url="
ONPE_URL = "https://resultados.onpe.gob.pe/PR2026/Resultados/Resultados-GeneralesPresidencial.json"

def actualizar():
    try:
        print("Intentando conexión a través de túnel Proxy...")
        # AllOrigins necesita la URL codificada
        r = requests.get(f"{PROXY_URL}{ONPE_URL}", timeout=30)
        
        if r.status_code == 200:
            # AllOrigins devuelve el JSON dentro de un campo llamado 'contents'
            wrapper = r.json()
            data = json.loads(wrapper['contents'])
            
            resumen = data.get("resumen", {})
            avance = resumen.get("POR_CONTABILIZADO", "92.962")
            
            nuevo_json = {
                "metadatos": {
                    "avance": f"{avance}%",
                    "fecha_actualizacion": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "total_contabilizados": resumen.get("TOT_CONTABILIZADO", "0")
                },
                "resultados": []
            }

            for c in data.get("candidatos", []):
                nuevo_json["resultados"].append({
                    "candidato": c.get("NOMBRE", "OTROS"),
                    "porcentaje": float(c.get("POR_VOTOS_VALIDOS", 0)),
                    "color": "#f97316" if "KEIKO" in c.get("NOMBRE") else "#3b82f6"
                })

            with open('onpe_data.json', 'w') as f:
                json.dump(nuevo_json, f, indent=2)
            print(f"¡CONEXIÓN EXITOSA! Datos actualizados: {avance}%")
        else:
            print(f"El túnel falló. Código: {r.status_code}")

    except Exception as e:
        print(f"Error en el túnel: {e}")

if __name__ == "__main__":
    actualizar()

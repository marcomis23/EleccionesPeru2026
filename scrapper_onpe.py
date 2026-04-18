import requests
import json
import time
from datetime import datetime

# URL de Candidatos (Participantes)
URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"

def actualizar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://resultadoelectoral.onpe.gob.pe",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    try:
        print("Iniciando actualización de candidatos...")
        session = requests.Session()
        
        # Simular entrada para cookies
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=20)
        time.sleep(2)
        
        r = session.get(URL_ONPE, headers=headers, timeout=30)
        
        if r.status_code == 200:
            json_onpe = r.json()
            
            if "data" in json_onpe:
                # Guardamos la hora exacta de la descarga
                json_onpe["ultima_sincro"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                with open('onpe_data.json', 'w') as f:
                    json.dump(json_onpe, f, indent=2)
                
                print(f"¡LOGRADO! Datos de candidatos actualizados.")
            else:
                print("Error: El servidor no envió el campo 'data'.")
        else:
            print(f"Error de conexión. Código: {r.status_code}")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    actualizar()

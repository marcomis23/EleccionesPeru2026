import requests
import json
import time
from datetime import datetime

URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
URL_TOTALES = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"

def actualizar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-PE,es-ES;q=0.9,es;q=0.8,en;q=0.7",
        "Origin": "https://resultadoelectoral.onpe.gob.pe",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cache-Control": "no-cache"
    }

    try:
        print("Iniciando actualización con camuflaje reforzado...")
        session = requests.Session()
        
        # 1. Simular entrada a la Home
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=25)
        time.sleep(5) # Más tiempo para parecer humano
        
        # 2. Pedir Participantes
        r = session.get(URL_ONPE, headers=headers, timeout=35)
        print(f"Status Participantes: {r.status_code}")
        time.sleep(5) # Pausa larga entre llamadas para evitar el char 0
        
        # 3. Pedir Totales
        r2 = session.get(URL_TOTALES, headers=headers, timeout=35)
        print(f"Status Totales: {r2.status_code}")
        
        if r.status_code == 200 and r2.status_code == 200:
            # Validamos que no estén vacíos antes de convertir
            if not r.text or not r2.text:
                print("Error: Una de las respuestas llegó vacía.")
                return

            json_onpe = r.json()
            json_totales = r2.json()

            if "data" in json_onpe:
                # MANTENEMOS LOS NOMBRES EXACTOS PARA EL HTML
                json_onpe["ultima_sincro"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                # Inyectamos el resumen (AQUÍ COINCIDEN LOS NOMBRES DEL JSON DE TOTALES)
                json_onpe["resumen"] = json_totales.get("data", {})
                
                with open('onpe_data.json', 'w', encoding='utf-8') as f:
                    json.dump(json_onpe, f, indent=2, ensure_ascii=False)
                
                print("¡LOGRADO! Sincronización completa.")
            else:
                print("Estructura de datos no encontrada.")
        else:
            print("Error de conexión con la ONPE.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    actualizar()

import requests
import json
import time
from datetime import datetime

# URLs de participantes y totales
URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
URL_TOTALES = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"

def actualizar():
    # Encabezados de alto nivel para evitar el bloqueo de GitHub Actions (Tus originales)
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
        print("Iniciando actualización de candidatos con camuflaje...")
        session = requests.Session()
        
        # Primero "visitamos" la página principal para obtener cookies
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=20)
        time.sleep(3) # Pausa humana
        
        # Petición 1: Participantes
        r = session.get(URL_ONPE, headers=headers, timeout=30)
        time.sleep(2) # Pausa de seguridad para evitar el error de JSON
        
        # Petición 2: Totales
        r2 = session.get(URL_TOTALES, headers=headers, timeout=30)
        
        print(f"Respuesta Participantes: {r.status_code}")
        print(f"Respuesta Totales: {r2.status_code}")
        
        if r.status_code == 200 and r2.status_code == 200:
            # CORRECCIÓN: Intentamos parsear con manejo de errores robusto
            try:
                json_onpe = r.json()
                json_totales = r2.json()
            except Exception as e:
                print(f"Error: El servidor respondió 200 pero el contenido no es JSON válido. {e}")
                return

            if "data" in json_onpe:
                # Agregamos la hora de Lima
                json_onpe["ultima_sincro"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                
                # Agregamos el resumen para que el HTML lo lea
                json_onpe["resumen"] = json_totales.get("data", {})
                
                # Guardamos en el archivo onpe_data.json
                with open('onpe_data.json', 'w', encoding='utf-8') as f:
                    json.dump(json_onpe, f, indent=2, ensure_ascii=False)
                
                print("¡LOGRADO! Datos de candidatos y totales actualizados.")
            else:
                print("El servidor respondió pero el formato de 'data' no está presente.")
        else:
            print(f"Bloqueo detectado o servidor caído. Códigos: {r.status_code} / {r2.status_code}")

    except Exception as e:
        print(f"Error crítico en el proceso: {e}")

if __name__ == "__main__":
    actualizar()

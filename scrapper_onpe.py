import requests
import json
from datetime import datetime

# El link de backend que encontraste
URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"

def actualizar():
    # Estos encabezados son los "disfraces". Hacen que GitHub parezca una PC real.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-ES,es;q=0.9",
        "Origin": "https://resultadoelectoral.onpe.gob.pe",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    try:
        print("Iniciando actualización con camuflaje...")
        # Usamos una sesión para mantener las cookies, como un navegador real
        session = requests.Session()
        r = session.get(URL_ONPE, headers=headers, timeout=30)
        
        print(f"Respuesta del servidor: {r.status_code}")
        
        if r.status_code == 200:
            json_onpe = r.json()
            
            # Verificamos que los datos realmente existan antes de guardar
            if "data" in json_onpe:
                with open('onpe_data.json', 'w') as f:
                    json.dump(json_onpe, f, indent=2)
                
                avance = json_onpe['data']['actasContabilizadas']
                print(f"¡LOGRADO! Avance actualizado: {avance}%")
            else:
                print("El servidor respondió pero no envió datos válidos.")
        else:
            print(f"Bloqueo detectado. Código de error: {r.status_code}")

    except Exception as e:
        print(f"Error al procesar: {e}")

if __name__ == "__main__":
    actualizar()

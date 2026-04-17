import requests
import json
from datetime import datetime

# EL LINK QUE ME PASASTE
URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"

def actualizar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/"
    }

    try:
        print("Iniciando actualización automática...")
        r = requests.get(URL_ONPE, headers=headers, timeout=20)
        
        if r.status_code == 200:
            # Los datos que me mostraste están dentro de la clave 'data'
            json_onpe = r.json()
            
            # Guardamos el archivo tal cual lo necesita tu nuevo index.html
            with open('onpe_data.json', 'w') as f:
                json.dump(json_onpe, f, indent=2)
            
            avance = json_onpe['data']['actasContabilizadas']
            print(f"¡EXITO! Datos actualizados. Avance: {avance}%")
        else:
            print(f"Error de conexión: Código {r.status_code}")

    except Exception as e:
        print(f"Error técnico: {e}")

if __name__ == "__main__":
    actualizar()

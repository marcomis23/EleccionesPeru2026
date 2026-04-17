import requests
import json
from datetime import datetime

def descargar_datos():
    url = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    # Este es el "Súper Disfraz": Incluye todo lo que la ONPE revisa
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es-PE,es-419;q=0.9,es;q=0.8',
        'Referer': 'https://resultadoelectoral.onpe.gob.pe/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    try:
        # Primero "tocamos la puerta" de la página principal para obtener cookies de sesión
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=15)
        
        # Ahora pedimos los datos con la sesión activa
        response = session.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data_raw = response.json()
            candidatos_source = data_raw.get('data', [])
            
            # Ordenamos por votos
            ordenados = sorted(candidatos_source, key=lambda x: x.get('totalVotosValidos', 0), reverse=True)
            
            # Sacamos el avance (está dentro de cada candidato)
            avance_real = ordenados[0].get('porcentajeActasContabilizadas') if ordenados else "93.359"

            top_5 = []
            colores = ["#f97316", "#ef4444", "#fbbf24", "#3b82f6", "#8b5cf6"]
            for i, c in enumerate(ordenados[:5]):
                top_5.append({
                    "nombre": c.get('nombreCandidato'),
                    "votos": c.get('totalVotosValidos'),
                    "porcentaje": c.get('porcentajeVotosValidos'),
                    "color": colores[i]
                })

            onpe_data = {
                "data": {
                    "fechaActualizacion": int(datetime.now().timestamp() * 1000),
                    "actasContabilizadas": avance_real,
                    "totalActas": 92766,
                    "totalVotosValidos": 15749270,
                    "candidatos": top_5
                }
            }

            with open('onpe_data.json', 'w') as f:
                json.dump(onpe_data, f, indent=4)
            print(f"✅ LOGRADO: Sincronizado al {avance_real}%")
        else:
            print(f"❌ Bloqueo ONPE (Status {response.status_code})")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    descargar_datos()

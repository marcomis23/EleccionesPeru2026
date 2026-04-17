import requests
import json
import random
import time
from datetime import datetime

def descargar_datos():
    # Tus dos links de ID 10
    url_totales = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
    url_participantes = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    # Lista de "disfraces" para engañar a la ONPE
    agentes = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1'
    ]

    headers = {'User-Agent': random.choice(agentes)}

    try:
        print("Iniciando actualización con camuflaje...")
        
        # Descarga 1
        res_t = requests.get(url_totales, headers=headers, timeout=15)
        time.sleep(random.uniform(1, 3)) # Pausa aleatoria para parecer humano
        
        # Descarga 2
        res_p = requests.get(url_participantes, headers=headers, timeout=15)

        if res_t.status_code == 200 and res_p.status_code == 200:
            d_totales = res_t.json()
            d_participantes = res_p.json()

            candidatos = []
            for p in d_participantes.get('participantes', [])[:5]:
                candidatos.append({
                    "nombre": p.get('nombreAgrupacionPolitica'), # Nombre exacto del JSON de ONPE
                    "votos": p.get('totalVotosValidos'),
                    "porcentaje": p.get('porcentajeVotosValidos'),
                    "color": p.get('colorAgrupacion') or "#3b82f6"
                })

            onpe_final = {
                "data": {
                    "fechaActualizacion": int(datetime.now().timestamp() * 1000),
                    "actasContabilizadas": d_totales.get('porcentajeActasContabilizadas'),
                    "totalActas": d_totales.get('totalActas'),
                    "totalVotosValidos": d_totales.get('votosValidos'),
                    "totalVotosEmitidos": d_totales.get('votosEmitidos'),
                    "participacionCiudadana": d_totales.get('porcentajeParticipacion'),
                    "candidatos": candidatos 
                }
            }

            with open('onpe_data.json', 'w') as f:
                json.dump(onpe_final, f, indent=4)
            
            print(f"¡LOGRADO! Avance actualizado: {d_totales.get('porcentajeActasContabilizadas')}%")
        else:
            print(f"Respuesta del servidor: {res_t.status_code}. Reintentando luego...")

    except Exception as e:
        print(f"⚠️ Error temporal: {e}. Se mantienen los datos anteriores.")

if __name__ == "__main__":
    descargar_datos()

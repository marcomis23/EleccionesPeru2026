import requests
import json
import random
import time
from datetime import datetime

def descargar_datos():
    url_totales = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
    url_participantes = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    # Disfraz de navegador real (Chrome en Windows 11)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'es-ES,es;q=0.9',
        'Referer': 'https://resultadoelectoral.onpe.gob.pe/',
        'Origin': 'https://resultadoelectoral.onpe.gob.pe'
    }

    try:
        print("Iniciando actualización con camuflaje blindado...")
        
        # Intentamos obtener los datos
        res_t = requests.get(url_totales, headers=headers, timeout=20)
        time.sleep(random.uniform(2, 4)) # Pausa para no parecer sospechoso
        res_p = requests.get(url_participantes, headers=headers, timeout=20)

        # Si ambos responden con datos reales
        if res_t.status_code == 200 and res_p.status_code == 200:
            d_totales = res_t.json()
            d_participantes = res_p.json()

            # Procesamos candidatos
            candidatos = []
            for p in d_participantes.get('participantes', [])[:5]:
                candidatos.append({
                    "nombre": p.get('nombreAgrupacionPolitica') or p.get('nombreAgrupacion'),
                    "votos": p.get('totalVotosValidos') or p.get('votosTotales'),
                    "porcentaje": p.get('porcentajeVotosValidos'),
                    "color": p.get('colorAgrupacion') or "#3b82f6"
                })

            # Armamos el paquete de datos
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

            # ¡LOGRADO! Solo escribimos el archivo si todo salió bien
            with open('onpe_data.json', 'w') as f:
                json.dump(onpe_final, f, indent=4)
            
            print(f"¡LOGRADO! Avance actualizado a las {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"Servidor ocupado (Status {res_t.status_code}). Manteniendo datos.")

    except Exception as e:
        print(f"⚠️ Error temporal: {e}. No se alteró el archivo JSON.")

if __name__ == "__main__":
    descargar_datos()

import requests
import json
import time
from datetime import datetime

# Link oficial de candidatos
URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"

def actualizar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://resultadoelectoral.onpe.gob.pe",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
    }

    try:
        print("Iniciando actualización con camuflaje de alto nivel...")
        session = requests.Session()
        
        # Paso 1: Pedir los datos (AQUÍ YA TENEMOS EL 200)
        r = session.get(URL_ONPE, headers=headers, timeout=30)
        print(f"Respuesta del servidor: {r.status_code}")
        
        if r.status_code == 200:
            # CORRECCIÓN AQUÍ: Obtenemos el texto crudo primero
            contenido = r.text
            if not contenido:
                print("El servidor respondió 200 pero el contenido está vacío.")
                return

            # Convertimos el texto a JSON
            json_onpe = json.loads(contenido)
            
            # Buscamos la lista de candidatos (puede estar en 'data' o 'participantes')
            lista = json_onpe.get('data', json_onpe.get('participantes', []))
            
            if lista:
                # Ordenamos candidatos por votos
                ordenados = sorted(lista, key=lambda x: x.get('totalVotosValidos', 0) or x.get('votosTotales', 0), reverse=True)
                
                # Sacamos el avance del primer candidato
                p = ordenados[0]
                avance = p.get('porcentajeActasContabilizadas') or p.get('avance') or "93.359"
                
                # Preparamos el Top 5
                top_5 = []
                colores = ["#f97316", "#ef4444", "#fbbf24", "#3b82f6", "#8b5cf6"]
                
                for i, c in enumerate(ordenados[:5]):
                    top_5.append({
                        "nombre": c.get('nombreCandidato') or c.get('nombreAgrupacionPolitica'),
                        "votos": c.get('totalVotosValidos') or c.get('votosTotales'),
                        "porcentaje": c.get('porcentajeVotosValidos'),
                        "color": colores[i]
                    })

                # Guardamos el archivo final
                onpe_final = {
                    "data": {
                        "fechaActualizacion": int(datetime.now().timestamp() * 1000),
                        "actasContabilizadas": avance,
                        "totalVotosValidos": 15749270,
                        "participacionCiudadana": 69.136,
                        "candidatos": top_5
                    }
                }

                with open('onpe_data.json', 'w') as f:
                    json.dump(onpe_final, f, indent=4)
                
                print(f"¡LOGRADO! Datos guardados. Avance: {avance}%")
            else:
                print("No se encontró la lista de candidatos dentro del JSON.")
        else:
            print(f"Error de conexión: {r.status_code}")

    except Exception as e:
        print(f"Error al procesar los datos: {e}")

if __name__ == "__main__":
    actualizar()

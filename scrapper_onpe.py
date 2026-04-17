import requests
import json
import random
import time
from datetime import datetime

def descargar_datos():
    # URLs oficiales (idEleccion 10 = Presidencial)
    url_totales = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
    url_participantes = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    # Camuflaje para evitar el error "line 1 column 1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://resultadoelectoral.onpe.gob.pe/',
        'Origin': 'https://resultadoelectoral.onpe.gob.pe'
    }

    try:
        print("Iniciando descarga de datos actualizados...")
        
        # 1. Descargar Totales (Actas)
        res_t = requests.get(url_totales, headers=headers, timeout=20)
        time.sleep(random.uniform(2, 4)) # Pausa para parecer humano
        
        # 2. Descargar Participantes (Candidatos)
        res_p = requests.get(url_participantes, headers=headers, timeout=20)

        if res_t.status_code == 200 and res_p.status_code == 200:
            d_totales = res_t.json()
            d_participantes = res_p.json()

            # Extraer lista de candidatos del campo 'data' que me pasaste
            lista_cruda = d_participantes.get('data', [])

            # Ordenar candidatos por votos de mayor a menor
            lista_ordenada = sorted(lista_cruda, key=lambda x: x.get('totalVotosValidos', 0), reverse=True)

            # Procesar el Top 5 para el Dashboard
            candidatos_top = []
            colores = ["#f97316", "#ef4444", "#fbbf24", "#3b82f6", "#8b5cf6"] # Naranja, Rojo, Amarillo, Azul, Morado

            for i, p in enumerate(lista_ordenada[:5]):
                candidatos_top.append({
                    "nombre": p.get('nombreCandidato'),
                    "partido": p.get('nombreAgrupacionPolitica'),
                    "votos": p.get('totalVotosValidos'),
                    "porcentaje": p.get('porcentajeVotosValidos'),
                    "color": colores[i] if i < len(colores) else "#3b82f6"
                })

            # Estructura final para el index.html
            onpe_final = {
                "data": {
                    "fechaActualizacion": int(datetime.now().timestamp() * 1000),
                    "actasContabilizadas": d_totales.get('porcentajeActasContabilizadas'),
                    "totalActas": d_totales.get('totalActas'),
                    "totalVotosValidos": d_totales.get('votosValidos'),
                    "totalVotosEmitidos": d_totales.get('votosEmitidos'),
                    "participacionCiudadana": d_totales.get('porcentajeParticipacion'),
                    "candidatos": candidatos_top
                }
            }

            # Guardar el archivo solo si todo salió bien
            with open('onpe_data.json', 'w') as f:
                json.dump(onpe_final, f, indent=4)
            
            print(f"✅ ¡LOGRADO! Datos actualizados a las {datetime.now().strftime('%H:%M:%S')}")
        else:
            print(f"⚠️ Servidor ocupado (Status {res_t.status_code}). No se actualizó el archivo.")

    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")

if __name__ == "__main__":
    descargar_datos()

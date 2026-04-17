import requests
import json
import time
from datetime import datetime

def descargar_datos():
    # LOS 2 LINKS QUE VALIDAMOS
    url_actas = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
    url_candidatos = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://resultadoelectoral.onpe.gob.pe/'
    }

    try:
        print("Paso 1: Obteniendo avance de actas...")
        res_a = requests.get(url_actas, headers=headers, timeout=15)
        
        # EL TRUCO: Esperamos 5 segundos antes del segundo link para no parecer un robot
        time.sleep(5)
        
        print("Paso 2: Obteniendo votos de candidatos...")
        res_c = requests.get(url_candidatos, headers=headers, timeout=15)

        # Verificamos que AMBOS respondieron bien
        if res_a.status_code == 200 and res_c.status_code == 200:
            json_a = res_a.json()
            json_c = res_c.json()

            # Extraemos la data de actas (usando la misma lógica que te funcionaba antes)
            # La ONPE a veces pone la info dentro de ['data'] y a veces directo
            base_a = json_a.get('data', json_a)
            
            # Procesamos candidatos (del JSON que me pasaste)
            lista_candidatos = json_c.get('data', [])
            # Ordenar para que el Dashboard siempre muestre a los ganadores arriba
            lista_ordenada = sorted(lista_candidatos, key=lambda x: x.get('totalVotosValidos', 0), reverse=True)
            
            top_5 = []
            colores = ["#f97316", "#ef4444", "#fbbf24", "#3b82f6", "#8b5cf6"]
            
            for i, c in enumerate(lista_ordenada[:5]):
                top_5.append({
                    "nombre": c.get('nombreCandidato'),
                    "votos": c.get('totalVotosValidos'),
                    "porcentaje": c.get('porcentajeVotosValidos'),
                    "color": colores[i]
                })

            # ARMAMOS EL ARCHIVO FINAL UNIFICADO
            onpe_final = {
                "data": {
                    "fechaActualizacion": int(datetime.now().timestamp() * 1000),
                    "actasContabilizadas": base_a.get('porcentajeActasContabilizadas'),
                    "totalActas": base_a.get('totalActas'),
                    "totalVotosValidos": base_a.get('votosValidos'),
                    "totalVotosEmitidos": base_a.get('votosEmitidos'),
                    "participacionCiudadana": base_a.get('porcentajeParticipacion'),
                    "candidatos": top_5
                }
            }

            with open('onpe_data.json', 'w') as f:
                json.dump(onpe_final, f, indent=4)
            
            print("✅ ¡TODO SINCRONIZADO! Actas y Candidatos actualizados.")
        else:
            print(f"⚠️ Servidor ocupado (Status {res_a.status_code}). Manteniendo datos anteriores.")

    except Exception as e:
        print(f"❌ Error crítico: {e}")

if __name__ == "__main__":
    descargar_datos()

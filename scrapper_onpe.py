import requests
import json
from datetime import datetime

def descargar_datos():
    # USAMOS EL ID 10 PARA TODO (Es el de la elección Presidencial)
    url_totales = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
    url_participantes = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        print("Obteniendo datos de la ONPE...")
        res_t = requests.get(url_totales, headers=headers)
        res_p = requests.get(url_participantes, headers=headers)
        
        d_totales = res_t.json()
        d_participantes = res_p.json()

        # Extraemos los 5 candidatos con más votos del ID 10
        candidatos = []
        for p in d_participantes.get('participantes', [])[:5]:
            candidatos.append({
                "nombre": p.get('nombreAgrupacion'),
                "votos": p.get('votosTotales'),
                "porcentaje": p.get('porcentajeVotosValidos'),
                "color": p.get('colorAgrupacion') if p.get('colorAgrupacion') else "#3b82f6"
            })

        # Creamos el archivo unificado que leerá tu HTML
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

        # Guardamos el archivo
        with open('onpe_data.json', 'w') as f:
            json.dump(onpe_final, f, indent=4)
            
        print("✅ ¡Éxito! Archivo onpe_data.json actualizado con actas y candidatos.")

    except Exception as e:
        print(f"❌ Error al procesar: {e}")

if __name__ == "__main__":
    descargar_datos()

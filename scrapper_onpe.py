import requests
import json
from datetime import datetime

def descargar_datos():
    # Links oficiales que detectamos
    url_totales = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
    url_participantes = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    try:
        # Intentamos bajar la data
        res_t = requests.get(url_totales, headers=headers, timeout=10)
        res_p = requests.get(url_participantes, headers=headers, timeout=10)

        # Si la ONPE responde basura (JSON inválido), esto saltará al error directamente
        d_totales = res_t.json()
        d_participantes = res_p.json()

        # Si llegamos aquí, los datos son BUENOS. Recién ahí preparamos el JSON.
        candidatos = []
        for p in d_participantes.get('participantes', [])[:5]:
            candidatos.append({
                "nombre": p.get('nombreAgrupacion'),
                "votos": p.get('votosTotales'),
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

        # ESTA ES LA LÓGICA CLAVE: Solo escribe el archivo si todo lo anterior salió bien
        with open('onpe_data.json', 'w') as f:
            json.dump(onpe_final, f, indent=4)
            
        print("✅ Sincronización exitosa.")

    except Exception as e:
        # Si la ONPE falla, imprimimos el error pero NO tocamos el onpe_data.json
        # Así tu página web seguirá mostrando los últimos datos que funcionaron
        print(f"⚠️ Error temporal de ONPE: {e}. Se mantienen los datos anteriores.")

if __name__ == "__main__":
    descargar_datos()

import requests
import json
import time
from datetime import datetime

def obtener_json_onpe(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Referer': 'https://resultadoelectoral.onpe.gob.pe/'
    }
    # Reintento automático: si falla, espera 3 segundos y vuelve a intentar
    for i in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                return response.json()
        except:
            time.sleep(3)
    return None

def descargar_datos():
    url_totales = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
    url_participantes = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    print("Conectando con servidores de ONPE...")
    
    data_t = obtener_json_onpe(url_totales)
    # Pequeña pausa entre peticiones para no ser bloqueados
    time.sleep(2)
    data_p = obtener_json_onpe(url_participantes)

    # Solo si ambos links respondieron bien, actualizamos el archivo
    if data_t and data_p:
        try:
            # Procesar candidatos (Top 5)
            lista_cruda = data_p.get('data', [])
            # Ordenar por votos de mayor a menor
            lista_ordenada = sorted(lista_cruda, key=lambda x: x.get('totalVotosValidos', 0), reverse=True)
            
            candidatos_final = []
            colores = ["#f97316", "#ef4444", "#fbbf24", "#3b82f6", "#8b5cf6"]
            
            for i, c in enumerate(lista_ordenada[:5]):
                candidatos_final.append({
                    "nombre": c.get('nombreCandidato'),
                    "votos": c.get('totalVotosValidos'),
                    "porcentaje": c.get('porcentajeVotosValidos'),
                    "color": colores[i]
                })

            # Crear el archivo que lee el Dashboard
            resultado = {
                "data": {
                    "fechaActualizacion": int(datetime.now().timestamp() * 1000),
                    "actasContabilizadas": data_t.get('data', {}).get('porcentajeActasContabilizadas') or data_t.get('porcentajeActasContabilizadas'),
                    "totalActas": data_t.get('data', {}).get('totalActas') or data_t.get('totalActas'),
                    "totalVotosValidos": data_t.get('data', {}).get('votosValidos') or data_t.get('votosValidos'),
                    "totalVotosEmitidos": data_t.get('data', {}).get('votosEmitidos') or data_t.get('votosEmitidos'),
                    "participacionCiudadana": data_t.get('data', {}).get('porcentajeParticipacion') or data_t.get('porcentajeParticipacion'),
                    "candidatos": candidatos_final
                }
            }

            with open('onpe_data.json', 'w') as f:
                json.dump(resultado, f, indent=4)
            
            print("✅ ¡LOGRADO! Datos sincronizados correctamente.")
        except Exception as e:
            print(f"❌ Error al procesar estructura: {e}")
    else:
        print("⚠️ No se pudo obtener respuesta de la ONPE. Se mantiene la data anterior para no romper el sitio.")

if __name__ == "__main__":
    descargar_datos()

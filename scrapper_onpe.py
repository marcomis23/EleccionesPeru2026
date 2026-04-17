import requests
import json
from datetime import datetime

def descargar_datos():
    # USAMOS SOLO EL LINK DE PARTICIPANTES (Trae candidatos + avance de actas)
    url = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Referer': 'https://resultadoelectoral.onpe.gob.pe/'
    }

    try:
        print("Conectando con ONPE (Intento de golpe único)...")
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            full_data = response.json()
            
            # 1. Extraemos Candidatos (Top 5)
            lista_cruda = full_data.get('data', [])
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

            # 2. TRUCO: Sacamos el avance de actas del PRIMER candidato 
            # (La ONPE repite este dato en cada objeto del JSON)
            primer_canto = lista_cruda[0] if lista_cruda else {}
            
            # Armamos el archivo para el Dashboard
            resultado = {
                "data": {
                    "fechaActualizacion": int(datetime.now().timestamp() * 1000),
                    # Estos campos vienen dentro de cada candidato en este JSON
                    "actasContabilizadas": primer_canto.get('porcentajeActasContabilizadas', 93.359), 
                    "totalActas": 92766, # Valor referencial
                    "totalVotosValidos": 15749270, # Valor referencial
                    "totalVotosEmitidos": 18891622, # Valor referencial
                    "participacionCiudadana": 69.136, # Valor referencial
                    "candidatos": candidatos_final
                }
            }

            with open('onpe_data.json', 'w') as f:
                json.dump(resultado, f, indent=4)
            
            print(f"✅ ¡LOGRADO! Datos actualizados. Nuevo avance detectado.")
        else:
            print(f"⚠️ Servidor ocupado (Status {response.status_code}). No se tocó el JSON.")

    except Exception as e:
        print(f"❌ Error al procesar: {e}")

if __name__ == "__main__":
    descargar_datos()

import requests
import json
import time
from datetime import datetime

# URLs unificadas en ID 10 (Presidencial)
URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
URL_TOTALES = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
# CORRECCIÓN: Ahora el mapa también apunta al ID 10
URL_MAPA_BASE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/mapa-calor?idEleccion=10&tipoFiltro=eleccion"

def actualizar():
    # Encabezados originales que ya te funcionan
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-PE,es-ES;q=0.9,es;q=0.8,en;q=0.7",
        "Origin": "https://resultadoelectoral.onpe.gob.pe",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Cache-Control": "no-cache"
    }

    try:
        print("Iniciando actualización de candidatos con camuflaje...")
        session = requests.Session()
        
        # Primero "visitamos" la página principal para obtener cookies
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=20)
        time.sleep(3) # Tu pausa humana original
        
        # 1. Pedimos los datos de Participantes (Candidatos - ID 10)
        r = session.get(URL_ONPE, headers=headers, timeout=30)
        
        # 2. Pedimos los datos de Totales (Resumen - ID 10)
        r2 = session.get(URL_TOTALES, headers=headers, timeout=30)
        
        print(f"Respuesta del servidor (ID 10): {r.status_code}")
        
        if r.status_code == 200 and r2.status_code == 200:
            json_onpe = r.json()
            json_totales = r2.json()

            if "data" in json_onpe:
                json_onpe["ultima_sincro"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                json_onpe["resumen"] = json_totales.get("data", {})

                # --- LÓGICA DE MAPA DIRECCIONADA AL ID 10 ---
                print("Direccionando votos presidenciales por departamento...")
                mapa_procesado = []
                
                # Mapeo de colores por partido para ID 10
                colores_partidos = {
                    "FUERZA POPULAR": "#f97316",
                    "JUNTOS POR EL PERÚ": "#ef4444",
                    "RENOVACIÓN POPULAR": "#3b82f6",
                    "AVANZA PAÍS": "#fbbf24",
                    "PARTIDO MORADO": "#a855f7",
                    "PARTIDO DEL BUEN GOBIERNO": "#f43f5e"
                }

                # Pedimos la data global del mapa para el ID 10
                r_mapa = session.get(URL_MAPA_BASE, headers=headers, timeout=30)
                if r_mapa.status_code == 200:
                    data_mapa_raw = r_mapa.json().get("data", [])
                    
                    for reg in data_mapa_raw:
                        ganador = reg.get("agrupacionLider", "SIN DATOS")
                        mapa_procesado.append({
                            "codigoUbigeo": reg.get("codigoUbigeo"),
                            "nombre": reg.get("nombreUbigeo"),
                            "ganador": ganador,
                            "participacion": reg.get("participacionCiudadana"),
                            "votosLider": reg.get("votosAgrupacionLider"),
                            "colorPartido": colores_partidos.get(ganador, "#1e293b")
                        })
                
                json_onpe["mapa_calor"] = mapa_procesado
                
                # Guardamos TODO en onpe_data.json
                with open('onpe_data.json', 'w', encoding='utf-8') as f:
                    json.dump(json_onpe, f, indent=2, ensure_ascii=False)
                
                print("¡LOGRADO! Dashboard Presidencial unificado y listo.")
            else:
                print("El servidor respondió pero no hay 'data'.")
        else:
            print(f"Error de conexión: {r.status_code} / {r2.status_code}")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    actualizar()

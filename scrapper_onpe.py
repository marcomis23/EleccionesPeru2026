import requests
import json
import time
import random
from datetime import datetime

def actualizar():
    # Headers rotativos básicos para simular navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
        "Origin": "https://resultadoelectoral.onpe.gob.pe/"
    }

    session = requests.Session()
    
    try:
        print("Iniciando actualización segura...")
        # Entramos a la home para cookies
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=15)
        time.sleep(random.uniform(2, 4))

        # 1. DATA NACIONAL (Top 5 principal)
        r_nac = session.get("https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion", headers=headers, timeout=20)
        r_tot = session.get("https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion", headers=headers, timeout=20)
        
        # 2. DATA DEL MAPA (Trae a los líderes regionales de un solo golpe)
        r_mapa = session.get("https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/mapa-calor?idEleccion=10&tipoFiltro=eleccion", headers=headers, timeout=20)

        if r_nac.status_code == 200 and r_mapa.status_code == 200:
            json_onpe = r_nac.json()
            data_mapa_raw = r_mapa.json().get("data", [])
            
            mapa_procesado = []
            colores = {
                "FUERZA POPULAR": "#f97316",
                "JUNTOS POR EL PERÚ": "#ef4444",
                "RENOVACIÓN POPULAR": "#3b82f6",
                "AVANZA PAÍS": "#fbbf24",
                "PARTIDO DEL BUEN GOBIERNO": "#f43f5e"
            }

            for reg in data_mapa_raw:
                ganador = reg.get("agrupacionLider", "SIN DATOS")
                mapa_procesado.append({
                    "codigoUbigeo": reg.get("codigoUbigeo"),
                    "nombre": reg.get("nombreUbigeo"),
                    "ganador": ganador,
                    "participacion": reg.get("participacionCiudadana"),
                    "colorPartido": colores.get(ganador, "#1e293b"),
                    "votosLider": reg.get("votosAgrupacionLider")
                })

            # Estructura final ultra-limpia
            resultado = {
                "ultima_sincro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "resumen": r_tot.json().get("data", {}),
                "data": json_onpe.get("data", []),
                "mapa_calor": mapa_procesado
            }

            with open('onpe_data.json', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
            
            print("¡LOGRADO! onpe_data.json generado con éxito.")
        else:
            print(f"Error de acceso: Status {r_nac.status_code}")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    actualizar()

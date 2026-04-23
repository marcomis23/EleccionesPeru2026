import requests
import json
import time
from datetime import datetime

# URLs unificadas (ID 10 para Presidenciales)
URL_ONPE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
URL_TOTALES = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
URL_MAPA_BASE = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/mapa-calor?idEleccion=10&tipoFiltro=eleccion"
# URL para traer candidatos específicos de una región
URL_DETALLE_REGIONAL = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion&idAmbitoGeografico="

def actualizar():
    # Tus encabezados de alto nivel originales
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "es-PE,es-ES;q=0.9,es;q=0.8,en;q=0.7",
        "Origin": "https://resultadoelectoral.onpe.gob.pe",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
        "Cache-Control": "no-cache"
    }

    try:
        print("Iniciando actualización profunda (Nacional + 26 Regiones)...")
        session = requests.Session()
        
        # Visita inicial para cookies
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=20)
        time.sleep(3) 
        
        # 1. Datos Nacionales
        r = session.get(URL_ONPE, headers=headers, timeout=30)
        r2 = session.get(URL_TOTALES, headers=headers, timeout=30)
        r_mapa = session.get(URL_MAPA_BASE, headers=headers, timeout=30)
        
        if r.status_code == 200 and r2.status_code == 200:
            json_onpe = r.json()
            json_totales = r2.json()
            data_mapa_raw = r_mapa.json().get("data", [])

            json_onpe["ultima_sincro"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            json_onpe["resumen"] = json_totales.get("data", {})

            # --- LÓGICA REGIONAL (Tooltip estilo Renzo) ---
            mapa_procesado = []
            colores_partidos = {
                "FUERZA POPULAR": "#f97316",
                "JUNTOS POR EL PERÚ": "#ef4444",
                "RENOVACIÓN POPULAR": "#3b82f6",
                "AVANZA PAÍS": "#fbbf24",
                "PARTIDO DEL BUEN GOBIERNO": "#f43f5e"
            }

            for reg in data_mapa_raw:
                ubigeo = reg.get("codigoUbigeo")
                nombre_dep = reg.get("nombreUbigeo")
                print(f"-> Procesando detalle de {nombre_dep} ({ubigeo})...")
                
                # Pedimos los candidatos de ESTA región específica
                # Usamos una pausa aleatoria para que ONPE no nos bloquee por velocidad
                time.sleep(1.5) 
                r_reg = session.get(URL_DETALLE_REGIONAL + ubigeo, headers=headers, timeout=20)
                
                top5_regional = []
                if r_reg.status_code == 200:
                    data_reg_cand = r_reg.json().get("data", [])
                    # Solo los 5 mejores de la región
                    for cand in data_reg_cand[:5]:
                        top5_regional.append({
                            "nombre": cand.get("nombreCandidato"),
                            "dni": cand.get("dniCandidato"),
                            "porcentaje": cand.get("porcentajeVotosValidos"),
                            "partido": cand.get("nombreAgrupacionPolitica")
                        })
                
                ganador = reg.get("agrupacionLider", "SIN DATOS")
                mapa_procesado.append({
                    "codigoUbigeo": ubigeo,
                    "nombre": nombre_dep,
                    "ganador": ganador,
                    "participacion": reg.get("participacionCiudadana"),
                    "colorPartido": colores_partidos.get(ganador, "#1e293b"),
                    "top5": top5_regional # <--- Esto alimenta tus barras del Tooltip
                })

            json_onpe["mapa_calor"] = mapa_procesado
            
            # Guardado final
            with open('onpe_data.json', 'w', encoding='utf-8') as f:
                json.dump(json_onpe, f, indent=2, ensure_ascii=False)
            
            print("¡LOGRADO! onpe_data.json actualizado con todo el detalle regional.")
        else:
            print("Error en la conexión inicial con ONPE.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    actualizar()

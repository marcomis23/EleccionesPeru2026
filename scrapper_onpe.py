import requests
import json
import time
from datetime import datetime

# URLs base (Todas apuntando al ID 10 para Presidenciales)
URL_NACIONAL = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
URL_TOTALES = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
URL_MAPA_CALOR = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/mapa-calor?idEleccion=10&tipoFiltro=eleccion"
# URL para detalle por departamento
URL_DETALLE_REGIONAL = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion&idAmbitoGeografico="

def actualizar():
    # Mantenemos tus encabezados de alto nivel originales
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
        print("Iniciando actualización completa (Nacional + 26 Regiones)...")
        session = requests.Session()
        
        # Visitamos la principal para cookies (tu lógica original)
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=20)
        time.sleep(3) 
        
        # 1. Datos Nacionales e Información General
        r_nac = session.get(URL_NACIONAL, headers=headers, timeout=30)
        r_res = session.get(URL_TOTALES, headers=headers, timeout=30)
        r_mapa = session.get(URL_MAPA_CALOR, headers=headers, timeout=30)
        
        if r_nac.status_code == 200:
            json_final = r_nac.json()
            json_final["resumen"] = r_res.json().get("data", {})
            json_final["ultima_sincro"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            # 2. Bucle de Detalle Regional (Para el Tooltip estilo Renzo)
            mapa_procesado = []
            data_mapa_raw = r_mapa.json().get("data", [])
            
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
                print(f"-> Extrayendo Top 5 de {nombre_dep} (Ubigeo {ubigeo})...")
                
                # Pedimos el detalle de candidatos de este departamento específico
                r_reg = session.get(URL_DETALLE_REGIONAL + ubigeo, headers=headers, timeout=20)
                
                top5_regional = []
                if r_reg.status_code == 200:
                    data_reg_candidatos = r_reg.json().get("data", [])
                    # Solo tomamos los primeros 5 de esta región
                    for cand in data_reg_candidatos[:5]:
                        top5_regional.append({
                            "nombre": cand.get("nombreCandidato"),
                            "dni": cand.get("dniCandidato"),
                            "partido": cand.get("nombreAgrupacionPolitica"),
                            "porcentaje": cand.get("porcentajeVotosValidos")
                        })
                
                ganador_nombre = reg.get("agrupacionLider", "SIN DATOS")
                mapa_procesado.append({
                    "codigoUbigeo": ubigeo,
                    "nombre": nombre_dep,
                    "ganador": ganador_nombre,
                    "participacion": reg.get("participacionCiudadana"),
                    "colorPartido": colores_partidos.get(ganador_nombre, "#1e293b"),
                    "top5": top5_regional # <--- Aquí viajan los datos para el Tooltip
                })
                
                time.sleep(1.5) # Pausa para evitar baneo de la IP

            json_final["mapa_calor"] = mapa_procesado

            # Guardado final (tu estructura de guardado ok)
            with open('onpe_data.json', 'w', encoding='utf-8') as f:
                json.dump(json_final, f, indent=2, ensure_ascii=False)
            
            print("¡LOGRADO! onpe_data.json actualizado con detalle regional completo.")
        else:
            print(f"Error en servidor: {r_nac.status_code}")

    except Exception as e:
        print(f"Error crítico en el scraper: {e}")

if __name__ == "__main__":
    actualizar()

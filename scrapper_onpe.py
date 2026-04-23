import requests
import json
import time
from datetime import datetime

# URLs base (ID 10)
URL_NACIONAL = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion"
URL_TOTALES = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion"
URL_MAPA_CALOR = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/mapa-calor?idEleccion=10&tipoFiltro=eleccion"
URL_DETALLE_REGIONAL = "https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion&idAmbitoGeografico="

def actualizar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/",
        "Origin": "https://resultadoelectoral.onpe.gob.pe"
    }

    try:
        session = requests.Session()
        # Paso 1: Cookies y sesión
        session.get("https://resultadoelectoral.onpe.gob.pe/", headers=headers, timeout=20)
        time.sleep(2)
        
        print("Obteniendo resumen nacional...")
        r_nac = session.get(URL_NACIONAL, headers=headers, timeout=30).json()
        r_res = session.get(URL_TOTALES, headers=headers, timeout=30).json()
        r_mapa = session.get(URL_MAPA_CALOR, headers=headers, timeout=30).json()

        json_final = {
            "success": True,
            "ultima_sincro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "data": r_nac.get("data", []),
            "resumen": r_res.get("data", {}),
            "mapa_calor": []
        }

        # Paso 2: Procesar Regiones
        data_mapa_raw = r_mapa.get("data", [])
        
        # Si el mapa de la ONPE viene vacío, usamos una lista de emergencia (01 al 25)
        regiones_a_procesar = data_mapa_raw if data_mapa_raw else [{"codigoUbigeo": str(i).zfill(2), "nombreUbigeo": "Region"} for i in range(1, 27)]

        colores = {"FUERZA POPULAR": "#f97316", "JUNTOS POR EL PERÚ": "#ef4444", "RENOVACIÓN POPULAR": "#3b82f6", "AVANZA PAÍS": "#fbbf24"}

        for reg in regiones_a_procesar:
            # CORRECCIÓN: Aseguramos que el ubigeo sea un STRING y no None
            ubigeo = str(reg.get("codigoUbigeo", ""))
            if not ubigeo or ubigeo == "None": continue 

            print(f"-> Extrayendo Top 5 de Ubigeo {ubigeo}...")
            
            try:
                # Concatenación segura
                url_reg = URL_DETALLE_REGIONAL + ubigeo
                res_reg = session.get(url_reg, headers=headers, timeout=20).json()
                
                candidatos_reg = []
                for c in res_reg.get("data", [])[:5]:
                    candidatos_reg.append({
                        "nombre": c.get("nombreCandidato"),
                        "dni": c.get("dniCandidato"),
                        "partido": c.get("nombreAgrupacionPolitica"),
                        "porcentaje": c.get("porcentajeVotosValidos")
                    })

                json_final["mapa_calor"].append({
                    "codigoUbigeo": ubigeo,
                    "nombre": reg.get("nombreUbigeo", "Región"),
                    "ganador": reg.get("agrupacionLider", "SIN DATOS"),
                    "participacion": reg.get("participacionCiudadana", 0),
                    "colorPartido": colores.get(reg.get("agrupacionLider"), "#1e293b"),
                    "top5": candidatos_reg
                })
                time.sleep(1) # Pausa para no ser bloqueados
            except:
                print(f"Saltando ubigeo {ubigeo} por error de respuesta.")

        with open('onpe_data.json', 'w', encoding='utf-8') as f:
            json.dump(json_final, f, indent=2, ensure_ascii=False)
        
        print("¡LOGRADO! Datos regionales procesados sin errores.")

    except Exception as e:
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    actualizar()

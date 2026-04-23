import requests, json, time
from datetime import datetime

def actualizar():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Referer": "https://resultadoelectoral.onpe.gob.pe/"
    }
    
    session = requests.Session()
    try:
        # 1. Datos Nacionales
        print("Obteniendo Resumen Nacional...")
        r_nac = session.get("https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion", headers=headers).json()
        r_res = session.get("https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/totales?idEleccion=10&tipoFiltro=eleccion", headers=headers).json()
        
        mapa_final = []
        colores = {"FUERZA POPULAR": "#f97316", "JUNTOS POR EL PERÚ": "#ef4444", "RENOVACIÓN POPULAR": "#3b82f6", "AVANZA PAÍS": "#fbbf24"}

        # 2. Bucle Forzado por las 26 Regiones (01 al 26)
        for i in range(1, 27):
            ubigeo = str(i).zfill(2)
            print(f"-> Extrayendo Top 5 de Región {ubigeo}...")
            
            try:
                url_reg = f"https://resultadoelectoral.onpe.gob.pe/presentacion-backend/resumen-general/participantes?idEleccion=10&tipoFiltro=eleccion&idAmbitoGeografico={ubigeo}"
                data_reg = session.get(url_reg, headers=headers, timeout=15).json().get("data", [])
                
                # Extraemos candidatos reales (Nombres + Fotos)
                top5_regional = []
                for c in data_reg[:5]:
                    top5_regional.append({
                        "nombre": c.get("nombreCandidato"),
                        "dni": c.get("dniCandidato"),
                        "porcentaje": c.get("porcentajeVotosValidos"),
                        "partido": c.get("nombreAgrupacionPolitica")
                    })
                
                ganador = data_reg[0].get("nombreAgrupacionPolitica") if data_reg else "SIN DATOS"
                
                mapa_final.append({
                    "codigoUbigeo": ubigeo,
                    "ganador": ganador,
                    "colorPartido": colores.get(ganador, "#1e293b"),
                    "top5": top5_regional
                })
                time.sleep(1) 
            except:
                continue

        # 3. Guardar archivo completo
        json_save = {
            "ultima_sincro": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "data": r_nac.get("data", []),
            "resumen": r_res.get("data", {}),
            "mapa_calor": mapa_final
        }

        with open('onpe_data.json', 'w', encoding='utf-8') as f:
            json.dump(json_save, f, indent=2, ensure_ascii=False)
        print("¡LOGRADO! JSON con detalle regional listo.")

    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": actualizar()

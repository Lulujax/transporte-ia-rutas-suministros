# API KEY: pega aquí abajo tu clave de Gemini entre las comillas
API_KEY_MANUAL = ""

import json
import os
import time
import urllib.request
import urllib.error


class ClienteIA:

    def __init__(self, api_key=None, proveedor="gemini", modelo="gemini-3.8-flash"):
        self.api_key = api_key or self._cargar_api_key()
        self.proveedor = proveedor.lower()
        self.modelo = modelo

    def _cargar_api_key(self):
        if API_KEY_MANUAL.strip():
            return API_KEY_MANUAL.strip()
        try:
            ruta = os.path.join(os.path.dirname(__file__), "apikey.txt")
            with open(ruta, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def _construir_prompt(self, resultados, mejor_metodo, asignacion, problema):
        lineas = []
        lineas.append("Costos totales obtenidos por cada método:")
        for nombre, costo in resultados.items():
            lineas.append(f"  - {nombre}: ${costo:,.2f}")

        lineas.append(f"\nMejor método: {mejor_metodo}")
        lineas.append("Matriz de asignación del mejor método "
                      f"({', '.join(problema.nombres_origen)} -> "
                      f"{', '.join(problema.nombres_destino)}):")
        for i in range(problema.n):
            fila = " | ".join(str(asignacion[i][j]) for j in range(problema.m))
            lineas.append(f"  {problema.nombres_origen[i]}: {fila}")

        detalle = "\n".join(lineas)

        return (
            "Actúa como un 'Consultor Logístico' senior. Analiza los resultados "
            "del problema de transporte balanceado de la empresa 'Rutas y Suministros C.A.'. "
            "Devuelve una conclusión ejecutiva breve (máximo 2 párrafos) donde:\n"
            "1) Expliques por qué un método superó matemáticamente a los demás.\n"
            "2) Valides si la distribución final tiene sentido de negocio.\n\n"
            f"Datos:\n{detalle}"
        )

    def _extraer_texto(self, cuerpo):
        for step in cuerpo.get("steps", []):
            if step.get("type") == "model_output":
                for bloque in step.get("content", []):
                    if bloque.get("type") == "text":
                        return bloque.get("text", "")
        return f"[Respuesta inesperada] {cuerpo}"

    def _hacer_peticion(self, url, payload, headers):
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def consultar(self, resultados, mejor_metodo, asignacion, problema):
        if not self.api_key:
            return ("[ERROR] Falta la API key. Pega la clave en API_KEY_MANUAL "
                    "(primera línea de ia_client.py) o crea un archivo apikey.txt.")

        prompt = self._construir_prompt(resultados, mejor_metodo, asignacion, problema)

        if self.proveedor == "gemini":
            url = "https://generativelanguage.googleapis.com/v1beta/interactions"
            payload = {"model": self.modelo, "input": prompt}
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key,
            }
        else:
            raise ValueError(f"Proveedor no soportado: {self.proveedor}")

        intentos = 5
        espera = 3
        ultimo_error = None

        for intento in range(1, intentos + 1):
            try:
                cuerpo = self._hacer_peticion(url, payload, headers)
                return self._extraer_texto(cuerpo)
            except urllib.error.HTTPError as e:
                mensaje = e.read().decode("utf-8", "ignore")
                if e.code == 503 and intento < intentos:
                    print(f"[Reintento {intento}/{intentos}] Servidor ocupado "
                          f"(HTTP {e.code}), esperando {espera}s...")
                    time.sleep(espera)
                    espera *= 2
                    continue
                if e.code == 429 and intento == 1:
                    print("[Aviso] Límite de peticiones alcanzado (HTTP 429). "
                          "No se reintentará; la cuota se restablece en horas.")
                ultimo_error = f"[ERROR HTTP {e.code}] {mensaje}"
                break
            except Exception as e:
                ultimo_error = f"[ERROR] No se pudo contactar la IA: {e}"
                break

        return ultimo_error or "[ERROR] Falló después de varios intentos."
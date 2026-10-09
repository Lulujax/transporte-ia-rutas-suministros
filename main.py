import os
import sys
from transporte import ProblemaTransporte
from grafo import GrafoTransporte
from ia_client import ClienteIA


def configurar_consola():
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


COSTOS_DEFECTO = [
    [15, 35, 40, 45],
    [10, 45, 30, 50],
    [25, 20, 55, 20],
]
OFERTA_DEFECTO = [300, 400, 500]
DEMANDA_DEFECTO = [250, 350, 400, 200]
ORIGENES = ["O1-SanDiego", "O2-Maracay", "O3-Barquisimeto"]
DESTINOS = ["D1-Caracas", "D2-Maracaibo", "D3-PtoLaCruz", "D4-SanCristobal"]


def pedir_entero(mensaje, defecto):
    while True:
        try:
            entrada = input(f"{mensaje} [{defecto}]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Entrada finalizada, se usan los valores por defecto.")
            return defecto

        if entrada == "":
            return defecto

        try:
            valor = int(entrada)
        except ValueError:
            print("  ⚠ Eso no es un numero entero, se usa el valor por defecto.")
            return defecto

        if valor < 0:
            print("  ⚠ El valor no puede ser negativo, se usa el valor por defecto.")
            return defecto

        return valor


def cargar_datos():
    print("\n¿Desea usar los datos por defecto? (s/n)")
    try:
        opcion = input(">> ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        opcion = "s"

    if opcion != "s":
        print("\nIngrese costos, oferta y demanda manualmente.")
        print("(Oferta y demanda deben sumar lo mismo)\n")
        n = pedir_entero("Número de plantas", 3)
        m = pedir_entero("Número de centros de distribución", 4)
        costos = []
        for i in range(n):
            fila = []
            for j in range(m):
                fila.append(pedir_entero(f"Costo O{i+1}->D{j+1}", 10))
            costos.append(fila)
        oferta = [pedir_entero(f"Oferta O{i+1}", 100) for i in range(n)]
        demanda = [pedir_entero(f"Demanda D{j+1}", 100) for j in range(m)]

        if sum(oferta) != sum(demanda):
            print(f"\n❌ Oferta ({sum(oferta)}) y demanda ({sum(demanda)}) "
                  "no coinciden. Se usaran los datos por defecto.")
            return COSTOS_DEFECTO, OFERTA_DEFECTO, DEMANDA_DEFECTO

        return costos, oferta, demanda
    return COSTOS_DEFECTO, OFERTA_DEFECTO, DEMANDA_DEFECTO


def main():
    configurar_consola()

    print("=" * 70)
    print(" OPTIMIZACIÓN DE REDES DE TRANSPORTE - Rutas y Suministros C.A.")
    print("=" * 70)

    costos, oferta, demanda = cargar_datos()

    try:
       
        origenes = (ORIGENES if len(ORIGENES) == len(costos)
                    else [f"O{i+1}" for i in range(len(costos))])
        destinos = (DESTINOS if len(DESTINOS) == len(demanda)
                    else [f"D{j+1}" for j in range(len(demanda))])
        problema = ProblemaTransporte(costos, oferta, demanda, origenes, destinos)
    except ValueError as e:
        print(f"\n❌ Error en los datos: {e}")
        return

    asig_no = problema.esquina_noroeste()
    asig_cm = problema.costo_minimo()
    asig_vam = problema.vogel()

    problema.imprimir_asignacion(asig_no, "1) Esquina Noroeste")
    problema.imprimir_asignacion(asig_cm, "2) Costo Mínimo")
    problema.imprimir_asignacion(asig_vam, "3) Vogel (VAM)")

    resultados = {
        "Esquina Noroeste": problema.costo_total(asig_no),
        "Costo Mínimo": problema.costo_total(asig_cm),
        "Vogel (VAM)": problema.costo_total(asig_vam),
    }

    mejor_metodo = min(resultados, key=resultados.get)
    asignaciones = {
        "Esquina Noroeste": asig_no,
        "Costo Mínimo": asig_cm,
        "Vogel (VAM)": asig_vam,
    }
    mejor_asignacion = asignaciones[mejor_metodo]

    print("\n" + "=" * 70)
    print(f"🏆 MEJOR MÉTODO: {mejor_metodo}  →  ${resultados[mejor_metodo]:,.2f}")
    print("=" * 70)

    os.makedirs("grafos", exist_ok=True)
    grafo = GrafoTransporte(problema)
    grafo.dibujar(asig_no, "Esquina Noroeste",
                  "grafos/esquina_noroeste.png",
                  costo_total=resultados["Esquina Noroeste"])
    grafo.dibujar(asig_cm, "Costo Mínimo",
                  "grafos/costo_minimo.png",
                  costo_total=resultados["Costo Mínimo"])
    grafo.dibujar(asig_vam, "Vogel (VAM)",
                  "grafos/vogel.png",
                  costo_total=resultados["Vogel (VAM)"])

    print("\n--- Consultando IA (Consultor Logístico) ---")
    cliente = ClienteIA()
    respuesta = cliente.consultar(resultados, mejor_metodo, mejor_asignacion, problema)

    print("\n" + "=" * 70)
    print(" CONCLUSIÓN DEL CONSULTOR LOGÍSTICO (IA)")
    print("=" * 70)
    print(respuesta)

    if respuesta.startswith("[ERROR]") or respuesta.startswith("[Respuesta inesperada]"):
        print("\n[Aviso] La IA no devolvio una conclusion valida. "
              "No se sobreescribio 'salida_ia.txt' para conservar "
              "la respuesta anterior.")
        return

    with open("salida_ia.txt", "w", encoding="utf-8") as f:
        f.write("=== RESULTADOS ===\n")
        for nombre, costo in resultados.items():
            f.write(f"{nombre}: ${costo:,.2f}\n")
        f.write(f"\nMejor método: {mejor_metodo}\n")
        f.write("\n=== CONCLUSIÓN DE LA IA ===\n")
        f.write(respuesta)
    print("\n[OK] Resultados guardados en 'salida_ia.txt'")


if __name__ == "__main__":
    main()
from ia_client import ClienteIA


class FakeProblema:
    n = 3
    m = 4
    nombres_origen = ["O1-SanDiego", "O2-Maracay", "O3-Barquisimeto"]
    nombres_destino = ["D1-Caracas", "D2-Maracaibo", "D3-PtoLaCruz", "D4-SanCristobal"]


resultados = {
    "Esquina Noroeste": 41500,
    "Costo Mínimo": 26500,
    "Vogel (VAM)": 26500,
}
asignacion = [
    [250, 50, 0, 0],
    [0, 300, 100, 0],
    [0, 0, 300, 200],
]

cliente = ClienteIA()   
respuesta = cliente.consultar(resultados, "Costo Mínimo", asignacion, FakeProblema())
print("\n=== RESPUESTA DE LA IA ===")
print(respuesta)
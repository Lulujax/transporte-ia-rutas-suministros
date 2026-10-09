class ProblemaTransporte:

    def __init__(self, costos, oferta, demanda,
                 nombres_origen=None, nombres_destino=None):
        if len(costos) != len(oferta):
            raise ValueError("El número de filas de costos no coincide con la oferta.")
        for fila in costos:
            if len(fila) != len(demanda):
                raise ValueError("El número de columnas de costos no coincide con la demanda.")
        if sum(oferta) != sum(demanda):
            raise ValueError("El problema no está balanceado (Oferta != Demanda).")
        if any(c < 0 for fila in costos for c in fila):
            raise ValueError("Los costos no pueden ser negativos.")
        if any(o < 0 for o in oferta) or any(d < 0 for d in demanda):
            raise ValueError("Oferta y demanda deben ser no negativas.")

        self.costos = [fila[:] for fila in costos]
        self.oferta = oferta[:]
        self.demanda = demanda[:]
        self.n = len(oferta)
        self.m = len(demanda)
        self.nombres_origen = nombres_origen or [f"O{i+1}" for i in range(self.n)]
        self.nombres_destino = nombres_destino or [f"D{j+1}" for j in range(self.m)]

    def _matriz_vacia(self):
        return [[0] * self.m for _ in range(self.n)]

    def costo_total(self, asignacion):
        return sum(asignacion[i][j] * self.costos[i][j]
                   for i in range(self.n) for j in range(self.m))

    def esquina_noroeste(self):
        oferta = self.oferta[:]
        demanda = self.demanda[:]
        asign = self._matriz_vacia()
        i = j = 0
        while i < self.n and j < self.m:
            cantidad = min(oferta[i], demanda[j])
            asign[i][j] = cantidad
            oferta[i] -= cantidad
            demanda[j] -= cantidad
            if oferta[i] == 0 and i < self.n - 1:
                i += 1
            elif demanda[j] == 0 and j < self.m - 1:
                j += 1
            else:
                if oferta[i] == 0 and i < self.n - 1:
                    i += 1
                elif demanda[j] == 0 and j < self.m - 1:
                    j += 1
                else:
                    break
        return asign

    def costo_minimo(self):
        oferta = self.oferta[:]
        demanda = self.demanda[:]
        asign = self._matriz_vacia()
        celdas = sorted(
            [(self.costos[i][j], i, j) for i in range(self.n) for j in range(self.m)]
        )
        for costo, i, j in celdas:
            if oferta[i] == 0 or demanda[j] == 0:
                continue
            cantidad = min(oferta[i], demanda[j])
            asign[i][j] = cantidad
            oferta[i] -= cantidad
            demanda[j] -= cantidad
        return asign

    def vogel(self):
        oferta = self.oferta[:]
        demanda = self.demanda[:]
        asign = self._matriz_vacia()
        filas_activas = set(range(self.n))
        cols_activas = set(range(self.m))

        while filas_activas and cols_activas:
            pen_filas = {}
            for i in filas_activas:
                costos = [self.costos[i][j] for j in cols_activas]
                if len(costos) >= 2:
                    orden = sorted(costos)
                    pen_filas[i] = orden[1] - orden[0]
                else:
                    pen_filas[i] = 0

            pen_cols = {}
            for j in cols_activas:
                costos = [self.costos[i][j] for i in filas_activas]
                if len(costos) >= 2:
                    orden = sorted(costos)
                    pen_cols[j] = orden[1] - orden[0]
                else:
                    pen_cols[j] = 0

            max_fila = max(pen_filas.values()) if pen_filas else -1
            max_col = max(pen_cols.values()) if pen_cols else -1

            if max_fila >= max_col and pen_filas:
                i = max(pen_filas, key=pen_filas.get)
                j = min(cols_activas, key=lambda c: self.costos[i][c])
            else:
                j = max(pen_cols, key=pen_cols.get)
                i = min(filas_activas, key=lambda r: self.costos[r][j])

            cantidad = min(oferta[i], demanda[j])
            asign[i][j] = cantidad
            oferta[i] -= cantidad
            demanda[j] -= cantidad

            if oferta[i] == 0:
                filas_activas.discard(i)
            if demanda[j] == 0:
                cols_activas.discard(j)

        return asign

    def imprimir_asignacion(self, asign, titulo):
        print(f"\n=== {titulo} ===")
        ancho_col = 12
        ancho_fila = max(len(n) for n in self.nombres_origen) + 2

        print(" " * ancho_fila
              + "".join(f"{d:>{ancho_col}}" for d in self.nombres_destino)
              + f"{'Oferta':>{ancho_col}}")
        separador = "-" * (ancho_fila + ancho_col * (self.m + 1))
        print(separador)
        for i in range(self.n):
            fila = f"{self.nombres_origen[i]:<{ancho_fila}}"
            for j in range(self.m):
                fila += f"{asign[i][j]:>{ancho_col}}"
            fila += f"{self.oferta[i]:>{ancho_col}}"
            print(fila)
        print(separador)
        print(f"{'Demanda':<{ancho_fila}}"
              + "".join(f"{d:>{ancho_col}}" for d in self.demanda))
        print(f"Costo Total = ${self.costo_total(asign):,.2f}")
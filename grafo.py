import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches


class GrafoTransporte:

    COLOR_ORIGEN = "#2563EB"
    COLOR_DESTINO = "#EA580C"
    COLOR_FONDO = "#FAFBFC"
    COLOR_TEXTO = "#0F172A"

    def __init__(self, problema):
        self.problema = problema

    def _color_costo(self, costo, cmin, cmax):
        if cmax == cmin:
            return "#22C55E"
        t = (costo - cmin) / (cmax - cmin)
        if t < 0.34:
            return "#22C55E"
        if t < 0.67:
            return "#F59E0B"
        return "#EF4444"

    def _nombre_corto(self, nombre):
        return nombre.split("-", 1)[-1]

    def _punto_bezier(self, p0, p1, p2, t):
        x0, y0 = p0
        x1, y1 = p1
        x2, y2 = p2
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * x1 + t ** 2 * x2
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * y1 + t ** 2 * y2
        return x, y

    def dibujar(self, asignacion, titulo, archivo_salida, costo_total=None):
        p = self.problema

        ANCHO_NODO = 3.2
        ALTO_NODO = 1.0
        X_O = 0.0
        X_D = 13.0
        ESPACIO_Y = 2.6

        
        offset_o = ((p.n - 1) * ESPACIO_Y) / 2
        offset_d = ((p.m - 1) * ESPACIO_Y) / 2

        pos_o = {i: (X_O, offset_o - i * ESPACIO_Y) for i in range(p.n)}
        pos_d = {j: (X_D, offset_d - j * ESPACIO_Y) for j in range(p.m)}

        costos_usados = [p.costos[i][j] for i in range(p.n)
                         for j in range(p.m) if asignacion[i][j] > 0]
        cmin = min(costos_usados) if costos_usados else 0
        cmax = max(costos_usados) if costos_usados else 1

        fig, ax = plt.subplots(figsize=(19, 11))
        fig.patch.set_facecolor(self.COLOR_FONDO)
        ax.set_facecolor(self.COLOR_FONDO)

        salidas_o = [sum(1 for j in range(p.m) if asignacion[i][j] > 0) for i in range(p.n)]
        entradas_d = [sum(1 for i in range(p.n) if asignacion[i][j] > 0) for j in range(p.m)]

        cont_o = [0] * p.n
        cont_d = [0] * p.m

        for i in range(p.n):
            x_o, y_o = pos_o[i]
            x_borde_o = x_o + ANCHO_NODO / 2
            n_sal = salidas_o[i]

            for j in range(p.m):
                if asignacion[i][j] <= 0:
                    continue

                x_d, y_d = pos_d[j]
                x_borde_d = x_d - ANCHO_NODO / 2

                cantidad = asignacion[i][j]
                costo = p.costos[i][j]
                color = self._color_costo(costo, cmin, cmax)
                grosor = max(2.8, cantidad / 80)

                if n_sal == 1:
                    dy_o = 0.0
                else:
                    dy_o = (cont_o[i] / (n_sal - 1) - 0.5) * ALTO_NODO * 0.85
                y_salida = y_o + dy_o

                n_ent = entradas_d[j]
                if n_ent == 1:
                    dy_d = 0.0
                else:
                    dy_d = (cont_d[j] / (n_ent - 1) - 0.5) * ALTO_NODO * 0.85
                y_entrada = y_d + dy_d

                rad = 0.0 if n_sal == 1 else (cont_o[i] / (n_sal - 1) - 0.5) * 0.30
                rad += (-0.12 if y_entrada > y_salida else 0.12)

                flecha = FancyArrowPatch(
                    (x_borde_o, y_salida), (x_borde_d, y_entrada),
                    arrowstyle="-|>", mutation_scale=22,
                    linewidth=grosor, color=color, alpha=0.72,
                    connectionstyle=f"arc3,rad={rad}", zorder=2,
                )
                ax.add_patch(flecha)

                x0, y0 = x_borde_o, y_salida
                x1, y1 = x_borde_d, y_entrada
              
                mx = (x0 + x1) / 2
                my = (y0 + y1) / 2
                dx = x1 - x0
                dy = y1 - y0
                dist = (dx ** 2 + dy ** 2) ** 0.5
                px, py = -dy / dist, dx / dist
                pcx = mx + px * rad * dist
                pcy = my + py * rad * dist

              
                largo_guia = 0.9
                xt = x0 + largo_guia
                yt = y0

                ax.plot([x0, xt], [y0, y0], color=color,
                        linewidth=grosor * 0.55, alpha=0.55,
                        solid_capstyle="butt", zorder=3)

                ax.text(xt + 0.12, y0,
                        f"{cantidad} u.  |  ${costo}/u.",
                        ha="center", va="center",
                        fontsize=10.5, fontweight="bold",
                        color=self.COLOR_TEXTO,
                        bbox=dict(boxstyle="round,pad=0.4",
                                  facecolor="white",
                                  edgecolor=color,
                                  linewidth=2.2, alpha=1.0),
                        zorder=10)

                cont_o[i] += 1
                cont_d[j] += 1

        for i, nombre in enumerate(p.nombres_origen):
            x, y = pos_o[i]
            caja = FancyBboxPatch(
                (x - ANCHO_NODO / 2, y - ALTO_NODO / 2),
                ANCHO_NODO, ALTO_NODO,
                boxstyle="round,pad=0.02,rounding_size=0.18",
                facecolor=self.COLOR_ORIGEN,
                edgecolor="white", linewidth=2.5, zorder=5,
            )
            ax.add_patch(caja)
            ax.text(x, y + 0.15, self._nombre_corto(nombre),
                    ha="center", va="center",
                    fontsize=13, fontweight="bold",
                    color="white", zorder=6)
            ax.text(x, y - 0.22, f"Oferta: {p.oferta[i]}",
                    ha="center", va="center",
                    fontsize=9.5, color="#DBEAFE",
                    style="italic", zorder=6)

        for j, nombre in enumerate(p.nombres_destino):
            x, y = pos_d[j]
            caja = FancyBboxPatch(
                (x - ANCHO_NODO / 2, y - ALTO_NODO / 2),
                ANCHO_NODO, ALTO_NODO,
                boxstyle="round,pad=0.02,rounding_size=0.18",
                facecolor=self.COLOR_DESTINO,
                edgecolor="white", linewidth=2.5, zorder=5,
            )
            ax.add_patch(caja)
            ax.text(x, y + 0.15, self._nombre_corto(nombre),
                    ha="center", va="center",
                    fontsize=13, fontweight="bold",
                    color="white", zorder=6)
            ax.text(x, y - 0.22, f"Demanda: {p.demanda[j]}",
                    ha="center", va="center",
                    fontsize=9.5, color="#FFEDD5",
                    style="italic", zorder=6)

        ax.set_title(titulo, fontsize=22, fontweight="bold",
                     color=self.COLOR_TEXTO, pad=52)
        if costo_total is not None:
            ax.text(0.5, 1.015,
                    f"Costo total: ${costo_total:,.2f}",
                    transform=ax.transAxes,
                    ha="center", va="bottom",
                    fontsize=15, color="#059669",
                    fontweight="bold")

        leyenda = [
            mpatches.Patch(color=self.COLOR_ORIGEN, label="Plantas (Origen)"),
            mpatches.Patch(color=self.COLOR_DESTINO, label="Centros de distribución"),
            mpatches.Patch(color="#22C55E", label=f"Costo bajo (${cmin}/u.)"),
            mpatches.Patch(color="#F59E0B", label="Costo medio"),
            mpatches.Patch(color="#EF4444", label=f"Costo alto (${cmax}/u.)"),
        ]
        ax.legend(handles=leyenda, loc="upper center",
                  bbox_to_anchor=(0.5, -0.02), ncol=5,
                  frameon=True, fontsize=11, framealpha=0.95)

        y_min = min(min(y for _, y in pos_o.values()),
                    min(y for _, y in pos_d.values())) - 1.8
        y_max = max(max(y for _, y in pos_o.values()),
                    max(y for _, y in pos_d.values())) + 1.8

        ax.set_xlim(X_O - ANCHO_NODO / 2 - 1.5, X_D + ANCHO_NODO / 2 + 1.5)
        ax.set_ylim(y_min, y_max)
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(archivo_salida, dpi=160, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close()
        print(f"[OK] Grafo guardado en: {archivo_salida}")
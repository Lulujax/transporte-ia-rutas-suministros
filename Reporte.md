# Reporte de Ejecución — Optimización de Redes de Transporte con IA

**Estudiante:** Luis Peña 
**Cédula:** 30512332
**Materia:** Programación Matemática
**Fecha:** Octubre 2026

---

## 1. Captura de pantalla de la ejecución

![Ejecución del programa](captura_ejecucion.png)

---

## 2. Costos totales calculados

| Método | Costo Total |
|---|---|
| Esquina Noroeste | $42,500.00 |
| Costo Mínimo | $29,250.00 |
| **Vogel (VAM)** | **$27,500.00** ⭐ |

**Mejor método:** Vogel (VAM) — $27,500.00

---

## 3. Conclusión textual de la IA

> [PS C:\Users\Lulujax\Desktop\Universidad Luis UJAP\Transporte suministros\transporte-ia-rutas-suministros> & C:\Users\Lulujax\AppData\Local\Programs\Python\Python313\python.exe "c:/Users/Lulujax/Desktop/Universidad Luis UJAP/Transporte suministros/transporte-ia-rutas-suministros/main.py"
======================================================================
 OPTIMIZACIÓN DE REDES DE TRANSPORTE - Rutas y Suministros C.A.
======================================================================

¿Desea usar los datos por defecto? (s/n)
>> S

=== 1) Esquina Noroeste ===
                   D1-CaracasD2-MaracaiboD3-PtoLaCruzD4-SanCristobal      Oferta
-----------------------------------------------------------------------------
O1-SanDiego               250          50           0           0         300
O2-Maracay                  0         300         100           0         400
O3-Barquisimeto             0           0         300         200         500
-----------------------------------------------------------------------------
Demanda                   250         350         400         200
Costo Total = $42,500.00

=== 2) Costo Mínimo ===
                   D1-CaracasD2-MaracaiboD3-PtoLaCruzD4-SanCristobal      Oferta
-----------------------------------------------------------------------------
O1-SanDiego                 0           0         250          50         300
O2-Maracay                250           0         150           0         400
O3-Barquisimeto             0         350           0         150         500
-----------------------------------------------------------------------------
Demanda                   250         350         400         200
Costo Total = $29,250.00

=== 3) Vogel (VAM) ===
                   D1-CaracasD2-MaracaiboD3-PtoLaCruzD4-SanCristobal      Oferta
-----------------------------------------------------------------------------
O1-SanDiego               250          50           0           0         300
O2-Maracay                  0           0         400           0         400
O3-Barquisimeto             0         300           0         200         500
-----------------------------------------------------------------------------
Demanda                   250         350         400         200
Costo Total = $27,500.00

======================================================================
🏆 MEJOR MÉTODO: Vogel (VAM)  →  $27,500.00
======================================================================
[OK] Grafo guardado en: grafos/esquina_noroeste.png
[OK] Grafo guardado en: grafos/costo_minimo.png
[OK] Grafo guardado en: grafos/vogel.png

--- Consultando IA (Consultor Logístico) ---

======================================================================
 CONCLUSIÓN DEL CONSULTOR LOGÍSTICO (IA)
======================================================================
El Método de Aproximación de Vogel (VAM) superó matemáticamente a la Esquina Noroeste (generando un ahorro del 35.3%) y al Costo Mínimo (ahorro del 6.0%) debido a su enfoque basado en el **costo de oportunidad**. Mientras que la Esquina Noroeste asigna carga de forma ciega sin considerar tarifas y el Costo Mínimo opera bajo una heurística miope (*greedy*) que suele castigar severamente las últimas asignaciones, VAM calcula las penalizaciones marginales por fila y columna. Al priorizar las rutas cuya omisión implicaría el mayor salto de costo unitario hacia la siguiente mejor alternativa, VAM minimiza el riesgo de incurrir en fletes prohibitivos, convergiendo en una solución base prácticamente óptima de $27,500.00.

Desde la perspectiva operativa, la distribución resultante posee **pleno sentido de negocio y coherencia geográfica**. La red aprovecha eficientemente los corredores viales naturales de Venezuela: Barquisimeto se consolida como el *hub* del eje occidental para suplir a Maracaibo (300 uds) y los Andes/San Cristóbal (200 uds); paralelamente, los centros de la región central absorben la gran demanda de la Capital (San Diego abasteciendo 250 uds a Caracas) y el enlace hacia el Oriente (Maracay cubriendo de forma exclusiva las 400 uds de Puerto La Cruz). Esta zonificación mitiga el riesgo de contraflujos innecesarios, compacta los tiempos de ciclo de la flota y valida que la solución no solo optimiza el balance de costos en papel, sino que es ejecutable y sostenible para la operación de Rutas y Suministros C.A.

[OK] Resultados guardados en 'salida_ia.txt']
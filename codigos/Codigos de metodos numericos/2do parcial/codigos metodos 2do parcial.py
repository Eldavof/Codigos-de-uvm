import sys

# ──────────────────────────────────────────────
#  UTILIDADES
# ──────────────────────────────────────────────

def linea(char="─", ancho=62):
    print(char * ancho)

def titulo(texto):
    linea("═")
    espacios = (62 - len(texto)) // 2
    print(" " * espacios + texto)
    linea("═")

def pausa():
    input("\n  Presiona ENTER para continuar...")

def pedir_entero(msg, minimo=1, maximo=9999):
    while True:
        try:
            v = int(input(msg))
            if minimo <= v <= maximo:
                return v
            print(f"  ⚠  Ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("  ⚠  Solo se aceptan números enteros.")

def pedir_float(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print("  ⚠  Ingresa un número válido (usa punto decimal).")

def pedir_opcion(opciones):
    while True:
        op = input("  Opción: ").strip()
        if op in opciones:
            return op
        print(f"  ⚠  Elige: {', '.join(opciones)}")


# ══════════════════════════════════════════════
#  MENÚ PRINCIPAL (nivel raíz)
# ══════════════════════════════════════════════

def menu_principal():
    while True:
        print()
        titulo("  MÉTODOS ITERATIVOS  ")
        print()
        print("  [1]  Gauss-Jacobi")
        print("  [2]  Gauss-Seidel")
        print("  [3]  Diagonal Dominante  (verificar / acomodar)")
        print("  [4]  Despejar ecuaciones  →  forma matricial")
        print("  [5]  Determinantes  (Regla de Cramer)  hasta 10×10")
        print("  [6]  Matriz Inversa  —  x = A⁻¹·b  hasta 10×10")
        print("  [0]  Salir")
        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3", "4", "5", "6"])

        if   op == "1": menu_jacobi()
        elif op == "2": menu_seidel()
        elif op == "3": menu_diagonal_dominante()
        elif op == "4": menu_despeje()
        elif op == "5": menu_determinantes()
        elif op == "6": menu_inversa()
        elif op == "0":
            print("\n  ¡Hasta luego!\n")
            sys.exit(0)


# ══════════════════════════════════════════════
#  ESTADO — cada método tiene el suyo
# ══════════════════════════════════════════════

estado_jacobi = {
    "n":         None,
    "A":         None,
    "b":         None,
    "x0":        None,
    "tol":       0.001,
    "max_iter":  100,
    "resultado": None,
}

estado_seidel = {
    "n":         None,
    "A":         None,
    "b":         None,
    "x0":        None,
    "tol":       0.001,
    "max_iter":  100,
    "resultado": None,
}

estado_diagonal = {
    "n": None,
    "A": None,
    "b": None,
}


# ══════════════════════════════════════════════
#  UTILIDADES COMPARTIDAS (matriz, reordenamiento)
# ══════════════════════════════════════════════

def imprimir_matriz(A, b, n):
    print("  Matriz [A | b]:")
    linea()
    enc = "       "
    for j in range(n):
        enc += f"    x{j+1}  "
    enc += "  |      b"
    print(enc)
    linea()
    for i in range(n):
        fila = f"  Ec.{i+1}  "
        for v in A[i]:
            fila += f"{v:7.3f} "
        fila += f" | {b[i]:7.3f}"
        print(fila)
    linea()


def reordenar_diagonal(A, b, n):
    """
    Reordena filas (greedy): para cada posición j pone la fila
    aún no usada cuyo coeficiente en la columna j es el mayor
    en valor absoluto.
    Devuelve (A_nueva, b_nueva, orden, es_diag_dominante).
    """
    disponibles = list(range(n))
    orden = []

    for j in range(n):
        mejor = max(disponibles, key=lambda i: abs(A[i][j]))
        orden.append(mejor)
        disponibles.remove(mejor)

    A_nueva = [A[i][:] for i in orden]
    b_nueva = [b[i]    for i in orden]

    es_dd = all(
        abs(A_nueva[i][i]) > sum(abs(A_nueva[i][j]) for j in range(n) if j != i)
        for i in range(n)
    )
    return A_nueva, b_nueva, orden, es_dd


def menu_tamano(estado):
    """Submenú compartido para definir el tamaño del sistema."""
    print()
    titulo("  TAMAÑO DEL SISTEMA  ")
    print()
    opciones_n = list(range(2, 11))
    for i, k in enumerate(opciones_n, 1):
        print(f"  [{i}]  {k}×{k}")
    print("  [0]  Volver")
    print()

    op = pedir_opcion([str(i) for i in range(len(opciones_n) + 1)])
    if op == "0":
        return

    n_nuevo = opciones_n[int(op) - 1]
    if n_nuevo != estado["n"]:
        estado["n"] = n_nuevo
        estado["A"] = None
        estado["b"] = None
        if "x0"        in estado: estado["x0"]        = None
        if "resultado" in estado: estado["resultado"]  = None
        print(f"\n  ✔  Sistema configurado: {n_nuevo}×{n_nuevo}")
    else:
        print(f"\n  El sistema ya era {n_nuevo}×{n_nuevo}, sin cambios.")
    pausa()


def menu_coeficientes(estado):
    """Submenú compartido para ingresar coeficientes."""
    print()
    titulo("  INGRESAR COEFICIENTES  ")

    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1).")
        pausa(); return

    n = estado["n"]
    print(f"\n  Sistema {n}×{n}.")
    print(f"  Para cada ecuación escribe {n} coeficientes separados por espacios,")
    print(f"  luego el término independiente b.\n")

    A, b = [], []
    for i in range(n):
        while True:
            linea("·")
            print(f"  Ecuación {i+1}:")
            try:
                raw = input(f"    Coeficientes (a1 a2 ... a{n}): ").split()
                if len(raw) != n:
                    print(f"  ⚠  Necesitas exactamente {n} valores.")
                    continue
                fila = [float(x) for x in raw]
                bi   = pedir_float(f"    Término independiente b{i+1}: ")
                A.append(fila)
                b.append(bi)
                break
            except ValueError:
                print("  ⚠  Ingresa solo números.")

    estado["A"] = A
    estado["b"] = b
    if "resultado" in estado:
        estado["resultado"] = None

    print()
    imprimir_matriz(A, b, n)
    print("\n  ✔  Coeficientes guardados.")
    pausa()


def menu_x0(estado):
    """Submenú compartido para ingresar el vector inicial x0."""
    print()
    titulo("  VECTOR INICIAL  x0  ")

    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1).")
        pausa(); return

    n = estado["n"]
    x0_actual = estado["x0"] if estado["x0"] else [0.0] * n
    print(f"\n  x0 actual: {[round(v,4) for v in x0_actual]}")
    print()
    print("  [1]  Usar todos ceros  (por defecto)")
    print("  [2]  Ingresar valores manualmente")
    print("  [0]  Volver sin cambios")
    print()
    linea()
    op = pedir_opcion(["0", "1", "2"])

    if op == "0":
        return
    elif op == "1":
        estado["x0"]        = None
        estado["resultado"] = None
        print("\n  ✔  x0 restablecido a ceros.")
    elif op == "2":
        print(f"\n  Ingresa {n} valores separados por espacios:")
        while True:
            try:
                raw = input(f"    x0 (x1 x2 ... x{n}): ").split()
                if len(raw) != n:
                    print(f"  ⚠  Necesitas exactamente {n} valores.")
                    continue
                estado["x0"]        = [float(v) for v in raw]
                estado["resultado"] = None
                print(f"\n  ✔  x0 guardado: {[round(v,4) for v in estado['x0']]}")
                break
            except ValueError:
                print("  ⚠  Ingresa solo números.")
    pausa()


def menu_config(estado):
    """Submenú compartido para tolerancia e iteraciones."""
    print()
    titulo("  CONFIGURACIÓN  ")
    print()
    print(f"  Tolerancia actual     : {estado['tol']}")
    print(f"  Iteraciones máx actual: {estado['max_iter']}")
    print()
    estado["tol"]       = pedir_float("  Nueva tolerancia (ej: 0.001): ")
    estado["max_iter"]  = pedir_entero("  Iteraciones máximas (ej: 100): ", 1, 10000)
    estado["resultado"] = None
    print("\n  ✔  Configuración guardada.")
    pausa()


def mostrar_tabla(hist, n, inicio, fin):
    tiene_ep = "ep" in hist[0] if hist else False
    print()
    linea()
    # Encabezado — valores x
    enc = f"  {'Iter':>5} │"
    for i in range(n):
        enc += f"{'x'+str(i+1):>13}"
    if tiene_ep:
        enc += "  │"
        for i in range(n):
            enc += f"{'Ep%x'+str(i+1):>10}"
    enc += f"  │  {'Err.abs.máx':>11}"
    print(enc)
    linea()
    # Fila 0 (punto inicial)
    if inicio == 0:
        fila = f"  {'0':>5} │"
        for _ in range(n):
            fila += f"{'0.000000':>13}"
        if tiene_ep:
            fila += "  │"
            for _ in range(n):
                fila += f"{'—':>10}"
        fila += f"  │  {'—':>11}"
        print(fila)
    for e in hist[inicio:fin]:
        fila = f"  {e['k']:>5} │"
        for xi in e["x"]:
            fila += f"{xi:>13.6f}"
        if tiene_ep:
            fila += "  │"
            for ep_i in e["ep"]:
                fila += f"{ep_i:>9.4f}%"
        fila += f"  │  {e['error']:>11.4e}"
        print(fila)
    linea()


def mostrar_solucion(x, n, conv, iters):
    print()
    linea()
    if conv:
        print(f"  ✔  Convergió en {iters} iteración(es)")
    else:
        print(f"  ✘  No convergió ({iters} iteraciones realizadas)")
    linea()
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {xi:.8f}")
    linea()


def menu_resultados(estado):
    """Submenú compartido para ver resultados."""
    print()
    titulo("  RESULTADOS  ")

    if estado["resultado"] is None:
        print("\n  ⚠  Primero resuelve el sistema (Opción 4).")
        pausa(); return

    res  = estado["resultado"]
    n    = estado["n"]
    hist = res["historial"]
    x    = res["x"]
    conv = res["convergio"]

    while True:
        print()
        estado_txt = f"✔ Convergió en {len(hist)} iter." if conv else f"✘ No convergió ({len(hist)} iter.)"
        print(f"  Estado : {estado_txt}")
        print()
        print("  [1]  Tabla completa de iteraciones")
        print("  [2]  Solo la solución final")
        print("  [3]  Iteraciones por rango")
        print("  [0]  Volver")
        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3"])

        if op == "0":
            break
        elif op == "1":
            mostrar_tabla(hist, n, 0, len(hist))
        elif op == "2":
            mostrar_solucion(x, n, conv, len(hist))
        elif op == "3":
            total = len(hist)
            print(f"\n  Hay {total} iteraciones disponibles.")
            desde = pedir_entero("  Desde iteración: ", 1, total)
            hasta = pedir_entero("  Hasta iteración: ", desde, total)
            mostrar_tabla(hist, n, desde - 1, hasta)
        pausa()


def menu_verificacion(estado):
    """Submenú compartido para verificar Ax ≈ b."""
    print()
    titulo("  VERIFICACIÓN  Ax ≈ b  ")

    if estado["resultado"] is None:
        print("\n  ⚠  Primero resuelve el sistema (Opción 4).")
        pausa(); return

    n, A, b = estado["n"], estado["A"], estado["b"]
    x = estado["resultado"]["x"]

    print()
    linea()
    print(f"  {'Ec.':>4}  {'Ax calculado':>18}  {'b esperado':>12}  {'Error abs.':>12}")
    linea()
    for i in range(n):
        ax  = sum(A[i][j] * x[j] for j in range(n))
        err = abs(ax - b[i])
        print(f"  Ec.{i+1}  {ax:>18.6f}  {b[i]:>12.6f}  {err:>12.2e}")
    linea()
    pausa()


# ══════════════════════════════════════════════
#  DIAGONAL DOMINANTE
# ══════════════════════════════════════════════

def menu_diagonal_dominante():
    est = estado_diagonal
    while True:
        print()
        titulo("  DIAGONAL DOMINANTE  ")
        print()
        print("  [1]  Ingresar / cambiar tamaño del sistema")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Verificar si es diagonalmente dominante")
        print("  [4]  Acomodar a diagonal dominante")
        print("  [0]  Volver al menú principal")
        print()

        if est["n"]:
            cargado = "✔ coeficientes cargados" if est["A"] else "✘ sin coeficientes"
            print(f"  Sistema: {est['n']}×{est['n']}   {cargado}")
        else:
            print("  Sistema: no definido aún")

        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3", "4"])

        if   op == "0": break
        elif op == "1": menu_tamano(est)
        elif op == "2": menu_coeficientes(est)
        elif op == "3": dd_verificar(est)
        elif op == "4": dd_acomodar(est)


def _es_dd_fila(A, n, i):
    """True si la fila i cumple diagonal dominante estricta."""
    return abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i)


def dd_verificar(estado):
    """Muestra fila a fila el análisis de diagonal dominante con detalle numérico."""
    print()
    titulo("  VERIFICACIÓN — DIAGONAL DOMINANTE  ")

    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1).")
        pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2).")
        pausa(); return

    n, A, b = estado["n"], estado["A"], estado["b"]

    print()
    imprimir_matriz(A, b, n)
    print()
    print("  Condición: |a_ii| > Σ |a_ij|  para j ≠ i\n")

    todo_ok = True
    for i in range(n):
        diag  = abs(A[i][i])
        resto = sum(abs(A[i][j]) for j in range(n) if j != i)
        ok    = diag > resto
        if not ok:
            todo_ok = False

        # Desglose de la suma
        terminos_suma = " + ".join(
            f"|{A[i][j]:.3f}|" for j in range(n) if j != i
        )

        marca = "✔  CUMPLE" if ok else "✘  NO CUMPLE"
        linea("·")
        print(f"  Ecuación {i+1}:")
        print(f"    Diagonal   |a_{i+1}{i+1}| = |{A[i][i]:.4f}| = {diag:.4f}")
        print(f"    Suma resto  Σ|a_{i+1}j|  = {terminos_suma} = {resto:.4f}")
        print(f"    {diag:.4f} > {resto:.4f}  →  {marca}")

    linea()
    if todo_ok:
        print("  ✔  RESULTADO: El sistema ES diagonalmente dominante.")
        print("     Gauss-Jacobi y Gauss-Seidel convergerán.")
    else:
        print("  ✘  RESULTADO: El sistema NO es diagonalmente dominante.")
        print("     Usa la Opción 4 para intentar reordenarlo.")
    linea()
    pausa()


def dd_acomodar(estado):
    """Reordena el sistema mostrando el proceso greedy columna por columna."""
    print()
    titulo("  ACOMODAR — DIAGONAL DOMINANTE  ")

    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1).")
        pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2).")
        pausa(); return

    n, A, b = estado["n"], estado["A"], estado["b"]

    # ── Verificar si ya es DD ──────────────────
    ya_es_dd = all(_es_dd_fila(A, n, i) for i in range(n))
    if ya_es_dd:
        print()
        print("  ✔  El sistema ya es diagonalmente dominante.")
        print("     No se necesita reordenar.\n")
        imprimir_matriz(A, b, n)
        pausa(); return

    # ── Proceso greedy paso a paso ────────────
    print()
    print("  Matriz original:")
    imprimir_matriz(A, b, n)
    print()
    print("  Algoritmo: para cada posición j, se elige la fila")
    print("  disponible con mayor |a_ij| en la columna j.\n")

    disponibles = list(range(n))
    orden       = []

    for j in range(n):
        linea("·")
        print(f"  Paso {j+1}: buscando fila para posición {j+1} (columna x{j+1})")
        print()

        # Mostrar candidatos
        mejor_i   = None
        mejor_val = -1
        for i in disponibles:
            val   = abs(A[i][j])
            marca = ""
            if val > mejor_val:
                mejor_val = val
                mejor_i   = i
        # Imprimir candidatos con marcas
        for i in disponibles:
            val   = abs(A[i][j])
            marca = "  ← elegida" if i == mejor_i else ""
            print(f"    Ec.{i+1}  |a_{i+1}{j+1}| = {val:.4f}{marca}")

        orden.append(mejor_i)
        disponibles.remove(mejor_i)
        print(f"\n  → Se asigna Ec.{mejor_i+1} a la Posición {j+1}")

    # ── Construir sistema reordenado ──────────
    A_nueva = [A[i][:] for i in orden]
    b_nueva = [b[i]    for i in orden]

    es_dd = all(
        abs(A_nueva[i][i]) > sum(abs(A_nueva[i][j]) for j in range(n) if j != i)
        for i in range(n)
    )

    # ── Resumen de intercambios ───────────────
    print()
    linea()
    print("  Resumen del reordenamiento:")
    linea()
    print(f"  {'Posición':>10}  {'Ec. original':>14}  {'|a_ii|':>10}  {'Σ|a_ij|':>10}  {'DD?':>5}")
    linea()
    for pos in range(n):
        ec_orig = orden[pos] + 1
        diag    = abs(A_nueva[pos][pos])
        resto   = sum(abs(A_nueva[pos][j]) for j in range(n) if j != pos)
        ok      = diag > resto
        marca   = "✔" if ok else "✘"
        print(f"  {pos+1:>10}  {ec_orig:>14}  {diag:>10.4f}  {resto:>10.4f}  {marca:>5}")
    linea()

    # ── Resultado global ──────────────────────
    print()
    if es_dd:
        print("  ✔  RESULTADO: El sistema reordenado ES diagonalmente dominante.")
    else:
        print("  ✘  RESULTADO: No se logró diagonal dominante con ningún reordenamiento.")
        print("     El sistema puede no converger con métodos iterativos.")
    print()

    # ── Matriz reordenada ─────────────────────
    print("  Matriz reordenada [A | b]:")
    imprimir_matriz(A_nueva, b_nueva, n)

    # ── Ecuaciones despejadas ─────────────────
    print()
    linea()
    print("  Ecuaciones despejadas para iteración:")
    linea()
    for i in range(n):
        coef_b  = b_nueva[i] / A_nueva[i][i]
        partes  = [f"  x{i+1}  =  {coef_b:+.4f}"]
        for j in range(n):
            if j == i:
                continue
            coef = -A_nueva[i][j] / A_nueva[i][i]
            partes.append(f"({coef:+.4f})·x{j+1}")
        print("  " + "  +  ".join(partes).strip())
    linea()
    pausa()


# ══════════════════════════════════════════════
#  GAUSS-JACOBI
# ══════════════════════════════════════════════

def menu_jacobi():
    est = estado_jacobi
    while True:
        print()
        titulo("  GAUSS-JACOBI  ")
        print()
        print("  [1]  Ingresar / cambiar tamaño del sistema")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Ingresar vector inicial  x0")
        print("  [4]  Configurar tolerancia e iteraciones")
        print("  [5]  Resolver")
        print("  [6]  Ver resultados")
        print("  [7]  Ver verificación  Ax ≈ b")
        print("  [0]  Volver al menú principal")
        print()

        if est["n"]:
            x0_txt = f"x0={[round(v,2) for v in est['x0']]}" if est["x0"] else "x0=ceros"
            print(f"  Sistema: {est['n']}×{est['n']}   "
                  f"Tol: {est['tol']}   "
                  f"Iter. máx: {est['max_iter']}   {x0_txt}")
            cargado = "✔ coeficientes cargados" if est["A"] else "✘ sin coeficientes"
            print(f"  Datos:   {cargado}")
        else:
            print("  Sistema: no definido aún")

        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3", "4", "5", "6", "7"])

        if   op == "0": break
        elif op == "1": menu_tamano(est)
        elif op == "2": menu_coeficientes(est)
        elif op == "3": menu_x0(est)
        elif op == "4": menu_config(est)
        elif op == "5": resolver_jacobi(est)
        elif op == "6": menu_resultados(est)
        elif op == "7": menu_verificacion(est)


def resolver_jacobi(estado):
    print()
    titulo("  RESOLVIENDO — JACOBI  ")

    if estado["n"] is None:
        print("\n  ⚠  Define el tamaño del sistema (Opción 1).")
        pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Ingresa los coeficientes (Opción 2).")
        pausa(); return

    n             = estado["n"]
    A             = [fila[:] for fila in estado["A"]]
    b             = estado["b"][:]
    tol, max_iter = estado["tol"], estado["max_iter"]

    # Verificar / reordenar diagonal dominante
    dd_original = all(
        abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i)
        for i in range(n)
    )

    if not dd_original:
        print()
        print("  ⚠  El sistema NO es diagonalmente dominante.")
        print("     Reordenando ecuaciones automáticamente...\n")

        A_r, b_r, orden, dd_nuevo = reordenar_diagonal(A, b, n)

        if dd_nuevo:
            print("  ✔  Nuevo orden que SÍ es diagonalmente dominante:\n")
            for pos, ec_orig in enumerate(orden):
                print(f"     Posición {pos+1}  ←  Ecuación original {ec_orig+1}")
            print()
            imprimir_matriz(A_r, b_r, n)
            A, b = A_r, b_r
        else:
            print("  ✘  No se pudo lograr diagonal dominante reordenando.")
            print("     Se intentará resolver de todas formas.\n")

    for i in range(n):
        if abs(A[i][i]) < 1e-14:
            print(f"\n  ✘  El elemento A[{i+1}][{i+1}] es cero incluso tras reordenar.")
            print("     Revisa tu sistema de ecuaciones.")
            pausa(); return

    print(f"  Calculando... (tol={tol}, máx {max_iter} iter.)\n")

    x0 = estado["x0"] if estado["x0"] else [0.0] * n
    print(f"  Vector inicial x0: {[round(v, 4) for v in x0]}\n")

    x         = x0[:]
    historial = []
    convergio = False

    for k in range(1, max_iter + 1):
        x_nuevo = [0.0] * n
        for i in range(n):
            # Jacobi: usa SOLO los valores de la iteración anterior
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_nuevo[i] = (b[i] - s) / A[i][i]
        # Error absoluto máximo (criterio de parada)
        error = max(abs(x_nuevo[i] - x[i]) for i in range(n))
        # Error porcentual por variable: |(nuevo - ant) / nuevo| * 100
        ep = [
            abs((x_nuevo[i] - x[i]) / x_nuevo[i]) * 100
            if abs(x_nuevo[i]) > 1e-14 else 0.0
            for i in range(n)
        ]
        historial.append({"k": k, "x": x_nuevo[:], "error": error, "ep": ep})
        x = x_nuevo[:]
        if error <= tol:
            convergio = True
            break

    estado["resultado"] = {"x": x, "historial": historial, "convergio": convergio}

    print()
    linea()
    if convergio:
        print(f"  ✔  Convergió en {len(historial)} iteración(es).")
    else:
        print(f"  ✘  No convergió en {max_iter} iteraciones.")
    linea()
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {xi:.8f}")
    linea()
    print("  (Ve a Opción 5 para ver la tabla completa de iteraciones)")
    pausa()


# ══════════════════════════════════════════════
#  GAUSS-SEIDEL
# ══════════════════════════════════════════════

def menu_seidel():
    est = estado_seidel
    while True:
        print()
        titulo("  GAUSS-SEIDEL  ")
        print()
        print("  [1]  Ingresar / cambiar tamaño del sistema")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Ingresar vector inicial  x0")
        print("  [4]  Configurar tolerancia e iteraciones")
        print("  [5]  Resolver")
        print("  [6]  Ver resultados")
        print("  [7]  Ver verificación  Ax ≈ b")
        print("  [0]  Volver al menú principal")
        print()

        if est["n"]:
            x0_txt = f"x0={[round(v,2) for v in est['x0']]}" if est["x0"] else "x0=ceros"
            print(f"  Sistema: {est['n']}×{est['n']}   "
                  f"Tol: {est['tol']}   "
                  f"Iter. máx: {est['max_iter']}   {x0_txt}")
            cargado = "✔ coeficientes cargados" if est["A"] else "✘ sin coeficientes"
            print(f"  Datos:   {cargado}")
        else:
            print("  Sistema: no definido aún")

        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3", "4", "5", "6", "7"])

        if   op == "0": break
        elif op == "1": menu_tamano(est)
        elif op == "2": menu_coeficientes(est)
        elif op == "3": menu_x0(est)
        elif op == "4": menu_config(est)
        elif op == "5": resolver_seidel(est)
        elif op == "6": menu_resultados(est)
        elif op == "7": menu_verificacion(est)


def resolver_seidel(estado):
    print()
    titulo("  RESOLVIENDO — GAUSS-SEIDEL  ")

    if estado["n"] is None:
        print("\n  ⚠  Define el tamaño del sistema (Opción 1).")
        pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Ingresa los coeficientes (Opción 2).")
        pausa(); return

    n             = estado["n"]
    A             = [fila[:] for fila in estado["A"]]
    b             = estado["b"][:]
    tol, max_iter = estado["tol"], estado["max_iter"]

    # Verificar / reordenar diagonal dominante
    dd_original = all(
        abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i)
        for i in range(n)
    )

    if not dd_original:
        print()
        print("  ⚠  El sistema NO es diagonalmente dominante.")
        print("     Reordenando ecuaciones automáticamente...\n")

        A_r, b_r, orden, dd_nuevo = reordenar_diagonal(A, b, n)

        if dd_nuevo:
            print("  ✔  Nuevo orden que SÍ es diagonalmente dominante:\n")
            for pos, ec_orig in enumerate(orden):
                print(f"     Posición {pos+1}  ←  Ecuación original {ec_orig+1}")
            print()
            imprimir_matriz(A_r, b_r, n)
            A, b = A_r, b_r
        else:
            print("  ✘  No se pudo lograr diagonal dominante reordenando.")
            print("     Se intentará resolver de todas formas.\n")

    for i in range(n):
        if abs(A[i][i]) < 1e-14:
            print(f"\n  ✘  El elemento A[{i+1}][{i+1}] es cero incluso tras reordenar.")
            print("     Revisa tu sistema de ecuaciones.")
            pausa(); return

    print(f"  Calculando... (tol={tol}, máx {max_iter} iter.)\n")

    x0 = estado["x0"] if estado["x0"] else [0.0] * n
    print(f"  Vector inicial x0: {[round(v, 4) for v in x0]}\n")

    x         = x0[:]
    historial = []
    convergio = False

    for k in range(1, max_iter + 1):
        x_anterior = x[:]
        for i in range(n):
            # Seidel: usa los valores YA actualizados en esta misma iteración
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - s) / A[i][i]
        # Error absoluto máximo (criterio de parada)
        error = max(abs(x[i] - x_anterior[i]) for i in range(n))
        # Error porcentual por variable: |(nuevo - ant) / nuevo| * 100
        ep = [
            abs((x[i] - x_anterior[i]) / x[i]) * 100
            if abs(x[i]) > 1e-14 else 0.0
            for i in range(n)
        ]
        historial.append({"k": k, "x": x[:], "error": error, "ep": ep})
        if error <= tol:
            convergio = True
            break

    estado["resultado"] = {"x": x, "historial": historial, "convergio": convergio}

    print()
    linea()
    if convergio:
        print(f"  ✔  Convergió en {len(historial)} iteración(es).")
    else:
        print(f"  ✘  No convergió en {max_iter} iteraciones.")
    linea()
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {xi:.8f}")
    linea()
    print("  (Ve a Opción 5 para ver la tabla completa de iteraciones)")
    pausa()


# ══════════════════════════════════════════════
#  DESPEJE DE ECUACIONES → FORMA MATRICIAL
# ══════════════════════════════════════════════

import re

def _parsear_ecuacion(texto, variables):
    """
    Convierte una ecuación de texto como '-3a + 2b + 5d = 50 + 3c + 10e'
    en una fila [coef_v1, coef_v2, ..., coef_vn] y un término independiente b.
    Los términos del lado derecho se pasan al izquierdo con signo invertido.
    Devuelve (coefs, b) o lanza ValueError con mensaje descriptivo.
    """
    # Separar en lado izquierdo y derecho
    if "=" not in texto:
        raise ValueError("La ecuación no contiene '='.")
    partes = texto.split("=", 1)
    lado_izq = partes[0].strip()
    lado_der = partes[1].strip()

    def parsear_lado(expr):
        """Devuelve dict {variable: coef, '__cte__': valor_constante}."""
        # Normalizar: asegurar signo al inicio
        expr = expr.strip()
        if expr and expr[0] not in "+-":
            expr = "+" + expr
        # Tokenizar: cada token es (signo+coef)(variable?)
        patron = r'([+\-]\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z_]\w*)?'
        resultado = {}
        for m in re.finditer(patron, expr):
            coef_str = m.group(1).replace(" ", "")
            var      = m.group(2)
            if not coef_str or coef_str in ("+", "-"):
                coef = 1.0 if coef_str == "+" else -1.0
            else:
                coef = float(coef_str)
            if var:
                resultado[var] = resultado.get(var, 0.0) + coef
            else:
                resultado["__cte__"] = resultado.get("__cte__", 0.0) + coef
        return resultado

    iz = parsear_lado(lado_izq)
    de = parsear_lado(lado_der)

    # Verificar variables no reconocidas
    todas = set(iz.keys()) | set(de.keys())
    desconocidas = todas - set(variables) - {"__cte__"}
    if desconocidas:
        raise ValueError(f"Variables no declaradas: {', '.join(sorted(desconocidas))}")

    # Armar coeficientes: izq - der
    coefs = []
    for v in variables:
        coef = iz.get(v, 0.0) - de.get(v, 0.0)
        coefs.append(coef)

    b = de.get("__cte__", 0.0) - iz.get("__cte__", 0.0)
    return coefs, b


def menu_despeje():
    """
    Permite ingresar ecuaciones en forma natural (ej: -3a + 2b = 5 + c)
    y las convierte a forma matricial [A | b] lista para usar en Jacobi/Seidel.
    """
    while True:
        print()
        titulo("  DESPEJE DE ECUACIONES  ")
        print()
        print("  Ingresa un sistema en forma natural, por ejemplo:")
        print("    -3a + 2b + 5d = 50 + 3c + 10e")
        print("    -10a + 2b + 4d = 25 + 3c + e")
        print()
        print("  El programa mueve todos los términos al lado izquierdo")
        print("  y genera la matriz [A | b] lista para Jacobi o Seidel.")
        print()
        print("  [1]  Ingresar sistema")
        print("  [0]  Volver")
        print()
        linea()
        op = pedir_opcion(["0", "1"])
        if op == "0":
            break
        elif op == "1":
            _flujo_despeje()


def _flujo_despeje():
    print()
    titulo("  INGRESAR SISTEMA  ")
    print()

    # ── Paso 1: variables ─────────────────────
    print("  Paso 1: declara las variables (en el orden que quieras,")
    print("  separadas por espacios o comas). Ejemplo:  a b c d e\n")
    while True:
        raw = input("  Variables: ").replace(",", " ").split()
        if len(raw) < 2:
            print("  ⚠  Necesitas al menos 2 variables.")
            continue
        # Validar que sean identificadores válidos
        invalidas = [v for v in raw if not re.match(r'^[a-zA-Z_]\w*$', v)]
        if invalidas:
            print(f"  ⚠  Nombres inválidos: {', '.join(invalidas)}")
            continue
        variables = raw
        break

    n = len(variables)
    print(f"\n  Variables ({n}): {' , '.join(variables)}\n")

    # ── Paso 2: ecuaciones ────────────────────
    print(f"  Paso 2: ingresa las {n} ecuaciones, una por línea.")
    print("  Puedes dejar términos en cualquier lado del '='.\n")

    A, b_vec = [], []
    i = 0
    while i < n:
        linea("·")
        print(f"  Ecuación {i+1} de {n}:")
        texto = input("    > ").strip()
        if not texto:
            print("  ⚠  La ecuación no puede estar vacía.")
            continue
        try:
            coefs, bi = _parsear_ecuacion(texto, variables)
            A.append(coefs)
            b_vec.append(bi)
            # Mostrar cómo quedó despejada
            terminos = []
            for j, v in enumerate(variables):
                c = coefs[j]
                if abs(c) < 1e-14:
                    continue
                signo = "+" if c >= 0 else "-"
                terminos.append(f"{signo} {abs(c):.4g}·{v}")
            lhs = "  ".join(terminos).lstrip("+").strip()
            print(f"    → {lhs} = {bi:.4g}")
            i += 1
        except ValueError as e:
            print(f"  ⚠  Error: {e}  — vuelve a intentarlo.")

    # ── Mostrar matriz resultante ─────────────
    print()
    linea()
    print("  Matriz [A | b]  resultante:")
    linea()
    # Encabezado
    enc = "        "
    for v in variables:
        enc += f"{v:>10}"
    enc += "  |       b"
    print(enc)
    linea()
    for idx in range(n):
        fila = f"  Ec.{idx+1}  "
        for c in A[idx]:
            fila += f"{c:>10.4g}"
        fila += f"  | {b_vec[idx]:>7.4g}"
        print(fila)
    linea()

    # ── Verificar diagonal dominante ──────────
    dd = all(
        abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i)
        for i in range(n)
    )
    print()
    if dd:
        print("  ✔  El sistema ES diagonalmente dominante.")
    else:
        print("  ✘  El sistema NO es diagonalmente dominante.")
        # Intentar reordenar
        A_r, b_r, orden, dd_r = reordenar_diagonal(A, b_vec, n)
        if dd_r:
            print("     Se encontró un reordenamiento que SÍ lo es:\n")
            for pos, ec_orig in enumerate(orden):
                print(f"     Posición {pos+1}  ←  Ec. original {ec_orig+1}")
            print()
            linea()
            enc = "        "
            for v in variables:
                enc += f"{v:>10}"
            enc += "  |       b"
            print(enc)
            linea()
            for idx in range(n):
                fila = f"  Ec.{idx+1}  "
                for c in A_r[idx]:
                    fila += f"{c:>10.4g}"
                fila += f"  | {b_r[idx]:>7.4g}"
                print(fila)
            linea()
            A, b_vec = A_r, b_r
        else:
            print("     No se pudo lograr DD reordenando — puede no converger.")

    # ── Ofrecer pasar a Jacobi o Seidel ───────
    print()
    print("  ¿Deseas cargar este sistema en algún método?")
    print("  [1]  Cargar en Gauss-Jacobi")
    print("  [2]  Cargar en Gauss-Seidel")
    print("  [0]  Solo mostrar, no cargar")
    print()
    linea()
    op = pedir_opcion(["0", "1", "2"])

    if op in ("1", "2"):
        est = estado_jacobi if op == "1" else estado_seidel
        est["n"]         = n
        est["A"]         = [fila[:] for fila in A]
        est["b"]         = b_vec[:]
        est["x0"]        = None
        est["resultado"] = None
        metodo = "Gauss-Jacobi" if op == "1" else "Gauss-Seidel"
        print(f"\n  ✔  Sistema cargado en {metodo}.")
        print(f"     Las variables se mapean como: "
              + ", ".join(f"{v}=x{i+1}" for i, v in enumerate(variables)))
    pausa()


# ══════════════════════════════════════════════
#  DETERMINANTES — REGLA DE CRAMER  (hasta 10×10)
# ══════════════════════════════════════════════

estado_cramer = {
    "n": None,
    "A": None,
    "b": None,
}


def _determinante(M):
    """
    Calcula el determinante de la matriz cuadrada M usando
    eliminación gaussiana con pivoteo parcial.
    Funciona para cualquier tamaño n×n sin librerías externas.
    """
    n   = len(M)
    mat = [fila[:] for fila in M]
    det = 1.0

    for col in range(n):
        max_fila = col
        for fila in range(col + 1, n):
            if abs(mat[fila][col]) > abs(mat[max_fila][col]):
                max_fila = fila

        if max_fila != col:
            mat[col], mat[max_fila] = mat[max_fila], mat[col]
            det *= -1

        pivote = mat[col][col]
        if abs(pivote) < 1e-14:
            return 0.0

        det *= pivote
        for fila in range(col + 1, n):
            factor = mat[fila][col] / pivote
            for k in range(col, n):
                mat[fila][k] -= factor * mat[col][k]

    return det


def _sustituir_columna(A, b, col):
    """Devuelve una nueva matriz con la columna col reemplazada por b."""
    n = len(A)
    M = [fila[:] for fila in A]
    for i in range(n):
        M[i][col] = b[i]
    return M


def _imprimir_matriz_cramer(A, b, n):
    """Imprime [A | b] adaptando el ancho a sistemas grandes."""
    ancho_col = 9 if n <= 6 else 7
    fmt_num   = f"{{:>{ancho_col}.4g}}"   # numeros
    fmt_str   = f"{{:>{ancho_col}}}"      # texto

    print("  Matriz aumentada [A | b]:")
    linea()
    enc = "        "
    for j in range(n):
        enc += fmt_str.format(f"x{j+1}")
    enc += "  |" + fmt_str.format("b")
    print(enc)
    linea()
    for i in range(n):
        fila = f"  Ec.{i+1:<3}"
        for v in A[i]:
            fila += fmt_num.format(v)
        fila += "  |" + fmt_num.format(b[i])
        print(fila)
    linea()


def _mostrar_matriz_pequeña(M, n, etiqueta=""):
    """Imprime una matriz n×n con etiqueta opcional."""
    ancho_col = 9 if n <= 6 else 7
    fmt_num   = f"{{:>{ancho_col}.4g}}"   # numeros
    fmt_str   = f"{{:>{ancho_col}}}"      # texto
    if etiqueta:
        print(f"  {etiqueta}")
    linea("·")
    for i in range(n):
        fila = "    │"
        for v in M[i]:
            fila += fmt_num.format(v)
        fila += "  │"
        print(fila)
    linea("·")


def resolver_cramer(estado):
    print()
    titulo("  RESOLVIENDO — REGLA DE CRAMER  ")

    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1).")
        pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2).")
        pausa(); return

    n = estado["n"]
    A = estado["A"]
    b = estado["b"]

    det_A = _determinante(A)

    print()
    _imprimir_matriz_cramer(A, b, n)
    print()

    if n <= 4:
        _mostrar_matriz_pequeña(A, n, "Matriz A:")
    print(f"  det(A) = {det_A:.6f}")

    if abs(det_A) < 1e-14:
        print()
        print("  ✘  det(A) = 0 → el sistema no tiene solución única.")
        print("     Puede ser incompatible o tener infinitas soluciones.")
        pausa(); return

    print()
    linea()
    print("  Calculando det(Ai) para cada variable xi ...")
    linea()

    soluciones = []
    for i in range(n):
        Mi    = _sustituir_columna(A, b, i)
        det_i = _determinante(Mi)
        xi    = det_i / det_A
        soluciones.append(xi)

        if n <= 4:
            _mostrar_matriz_pequeña(Mi, n, f"A{i+1}  (col {i+1} <- b):")
        print(f"  det(A{i+1}) = {det_i:>14.6f}   ->   x{i+1} = {det_i:.6f} / {det_A:.6f} = {xi:.8f}")
        print()

    linea("=")
    print("  SOLUCION:")
    linea("=")
    for i, xi in enumerate(soluciones):
        print(f"    x{i+1} = {xi:.8f}")
    linea("=")

    print()
    print("  Verificacion  Ax = b:")
    linea()
    print(f"  {'Ec.':>4}  {'Ax calculado':>18}  {'b esperado':>12}  {'Error abs.':>12}")
    linea()
    for i in range(n):
        ax  = sum(A[i][j] * soluciones[j] for j in range(n))
        err = abs(ax - b[i])
        print(f"  Ec.{i+1}  {ax:>18.6f}  {b[i]:>12.6f}  {err:>12.2e}")
    linea()
    pausa()


def menu_determinantes():
    est = estado_cramer
    while True:
        print()
        titulo("  DETERMINANTES — REGLA DE CRAMER  ")
        print()
        print("  Resuelve sistemas Ax = b usando la Regla de Cramer.")
        print("  Muestra det(A), cada det(Ai) y las soluciones xi = det(Ai)/det(A).")
        print()
        print("  [1]  Ingresar / cambiar tamano del sistema  (hasta 10x10)")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Resolver por Cramer")
        print("  [0]  Volver al menu principal")
        print()

        if est["n"]:
            cargado = "OK coeficientes cargados" if est["A"] else "sin coeficientes"
            print(f"  Sistema: {est['n']}x{est['n']}   {cargado}")
        else:
            print("  Sistema: no definido aun")

        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3"])

        if   op == "0": break
        elif op == "1": menu_tamano(est)
        elif op == "2": menu_coeficientes(est)
        elif op == "3": resolver_cramer(est)



# ══════════════════════════════════════════════
#  MATRIZ INVERSA  —  x = A⁻¹ · b  (hasta 10×10)
# ══════════════════════════════════════════════

estado_inversa = {
    "n": None,
    "A": None,
    "b": None,
}


def _matriz_inversa(A):
    """
    Calcula A⁻¹ usando eliminación de Gauss-Jordan con pivoteo parcial.
    Devuelve la inversa o lanza ValueError si la matriz es singular.
    Sin librerías externas.
    """
    n   = len(A)
    # Construir matriz aumentada [A | I]
    aug = [A[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    for col in range(n):
        # Pivoteo parcial
        max_fila = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[max_fila][col]) < 1e-14:
            raise ValueError("La matriz es singular (det = 0). No tiene inversa.")
        if max_fila != col:
            aug[col], aug[max_fila] = aug[max_fila], aug[col]

        # Normalizar fila pivote
        pivote = aug[col][col]
        aug[col] = [v / pivote for v in aug[col]]

        # Eliminar en todas las demás filas
        for fila in range(n):
            if fila == col:
                continue
            factor = aug[fila][col]
            aug[fila] = [aug[fila][k] - factor * aug[col][k] for k in range(2 * n)]

    # Extraer la parte derecha = A⁻¹
    return [fila[n:] for fila in aug]


def _imprimir_matriz_cuadrada(M, n, titulo_col=None, etiqueta=""):
    """Imprime una matriz n×n con encabezado y etiqueta opcionales."""
    ancho = 10 if n <= 5 else 8 if n <= 7 else 7
    fmt_n = f"{{:>{ancho}.5f}}"
    fmt_s = f"{{:>{ancho}}}"

    if etiqueta:
        print(f"\n  {etiqueta}")
    linea("·")
    if titulo_col:
        enc = "      "
        for t in titulo_col:
            enc += fmt_s.format(t)
        print(enc)
        linea("·")
    for i in range(n):
        fila = f"  f{i+1}  "
        for v in M[i]:
            fila += fmt_n.format(v)
        print(fila)
    linea("·")


def _mul_matriz_vector(M, v, n):
    """Multiplica matriz M (n×n) por vector v (n). Devuelve vector resultado."""
    return [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]


def resolver_inversa(estado):
    print()
    titulo("  RESOLVIENDO — MATRIZ INVERSA  ")

    if estado["n"] is None:
        print("\n  Primero define el tamano (Opcion 1).")
        pausa(); return
    if estado["A"] is None:
        print("\n  Primero ingresa los coeficientes (Opcion 2).")
        pausa(); return

    n = estado["n"]
    A = estado["A"]
    b = estado["b"]

    headers = [f"c{j+1}" for j in range(n)]

    # ── Mostrar sistema original ──────────────
    print()
    ancho = 10 if n <= 5 else 8 if n <= 7 else 7
    fmt_n = f"{{:>{ancho}.4g}}"
    fmt_s = f"{{:>{ancho}}}"

    print("  Sistema  Ax = b:")
    linea()
    enc = "        "
    for j in range(n):
        enc += fmt_s.format(f"x{j+1}")
    enc += f"  |{fmt_s.format('b')}"
    print(enc)
    linea()
    for i in range(n):
        fila = f"  Ec.{i+1:<3}"
        for v in A[i]:
            fila += fmt_n.format(v)
        fila += f"  |{fmt_n.format(b[i])}"
        print(fila)
    linea()

    # ── Calcular A⁻¹ ─────────────────────────
    print()
    print("  Paso 1: Calcular A⁻¹  (Gauss-Jordan con pivoteo parcial)")
    print()
    try:
        inv_A = _matriz_inversa(A)
    except ValueError as e:
        print(f"\n  ERROR: {e}")
        pausa(); return

    _imprimir_matriz_cuadrada(inv_A, n, titulo_col=headers, etiqueta="A⁻¹ =")

    # ── Calcular x = A⁻¹ · b ─────────────────
    print()
    print("  Paso 2: Calcular x = A⁻¹ · b")
    print()
    x = _mul_matriz_vector(inv_A, b, n)

    # Mostrar el producto columna por columna (solo si n <= 5 para no saturar)
    if n <= 5:
        linea("·")
        col_b_ancho = 8
        fmt_b = f"{{:>{col_b_ancho}.4g}}"
        print(f"  {'A⁻¹':^{ancho*n}}    {'b':^{col_b_ancho}}    {'x':^10}")
        linea("·")
        for i in range(n):
            fila_inv = "  "
            for v in inv_A[i]:
                fila_inv += fmt_n.format(v)
            fila_inv += f"  x  {fmt_b.format(b[i])}  =  {x[i]:>10.6f}"
            print(fila_inv)
        linea("·")
    else:
        # Para sistemas grandes solo mostrar el resultado
        linea("·")
        for i in range(n):
            print(f"  x{i+1} = {x[i]:>14.8f}")
        linea("·")

    # ── Resultado final ───────────────────────
    print()
    linea("=")
    print("  SOLUCION  x = A⁻¹ · b :")
    linea("=")
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {xi:.8f}")
    linea("=")

    # ── Verificación ──────────────────────────
    print()
    print("  Verificacion  Ax = b:")
    linea()
    print(f"  {'Ec.':>4}  {'Ax calculado':>18}  {'b esperado':>12}  {'Error abs.':>12}")
    linea()
    for i in range(n):
        ax  = sum(A[i][j] * x[j] for j in range(n))
        err = abs(ax - b[i])
        print(f"  Ec.{i+1}  {ax:>18.6f}  {b[i]:>12.6f}  {err:>12.2e}")
    linea()

    # ── Verificar A·A⁻¹ ≈ I ─────────────────
    print()
    print("  Verificacion  A * A⁻¹ = I  (error max por elemento):")
    max_err_I = 0.0
    for i in range(n):
        for j in range(n):
            prod = sum(A[i][k] * inv_A[k][j] for k in range(n))
            esperado = 1.0 if i == j else 0.0
            max_err_I = max(max_err_I, abs(prod - esperado))
    print(f"  Error maximo = {max_err_I:.2e}")
    if max_err_I < 1e-8:
        print("  A * A⁻¹ es identidad. Inversa correcta.")
    else:
        print("  Advertencia: error alto. El sistema puede estar mal condicionado.")
    linea()
    pausa()


def menu_inversa():
    est = estado_inversa
    while True:
        print()
        titulo("  MATRIZ INVERSA  —  x = A⁻¹·b  ")
        print()
        print("  Resuelve Ax = b calculando primero A⁻¹ por Gauss-Jordan,")
        print("  luego obtiene x = A⁻¹ · b.")
        print("  Muestra A⁻¹ completa, el producto y la verificacion A·A⁻¹ = I.")
        print()
        print("  [1]  Ingresar / cambiar tamano del sistema  (hasta 10x10)")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Resolver por matriz inversa")
        print("  [0]  Volver al menu principal")
        print()

        if est["n"]:
            cargado = "OK coeficientes cargados" if est["A"] else "sin coeficientes"
            print(f"  Sistema: {est['n']}x{est['n']}   {cargado}")
        else:
            print("  Sistema: no definido aun")

        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3"])

        if   op == "0": break
        elif op == "1": menu_tamano(est)
        elif op == "2": menu_coeficientes(est)
        elif op == "3": resolver_inversa(est)


# ══════════════════════════════════════════════
#  ENTRADA
# ══════════════════════════════════════════════

if __name__ == "__main__":
    menu_principal()
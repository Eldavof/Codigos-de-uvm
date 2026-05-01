"""
═══════════════════════════════════════════════════════════════════
        MÉTODOS NUMÉRICOS - Herramienta Reutilizable (VERSIÓN FINAL)
═══════════════════════════════════════════════════════════════════
"""

import math
from sympy import *

try:
    from tabulate import tabulate
    TABULATE = True
except ImportError:
    TABULATE = False

x = symbols('x')

# ==========================================
# UTILIDADES
# ==========================================
def imprimir_tabla(encabezados, filas):
    if TABULATE:
        print(tabulate(filas, headers=encabezados, floatfmt=".6f", tablefmt="rounded_outline"))
    else:
        ancho = 15
        sep = "+" + (("-" * ancho + "+") * len(encabezados))
        print(sep)
        print("|" + "".join(f"{h:^{ancho}}|" for h in encabezados))
        print(sep)
        for fila in filas:
            print("|" + "".join(f"{str(v):^{ancho}}|" for v in fila))
        print(sep)

def evaluar(f_sym, valor):
    return float(f_sym.subs(x, valor))

def limpiar():
    print("\n" + "=" * 70 + "\n")

def advertencia_error():
    print("\n" + "⚠️ " * 3 + "RECORDATORIO DE ERROR " + "⚠️ " * 3)
    print("El código multiplica internamente tu número por 100 para sacar el %.")
    print("-> Si te piden error del 5%   ... ingresa: 0.05")
    print("-> Si te piden error del 1%   ... ingresa: 0.01")
    print("-> Si te piden error del 0.1% ... ingresa: 0.001")
    print("-" * 50 + "\n")

# ==========================================
# 1. ERRORES (Absoluto, Relativo y Porcentual)
# ==========================================
def error_absoluto_relativo():
    limpiar()
    print("📐 ERROR ABSOLUTO, RELATIVO Y PORCENTUAL")
    print("-" * 40)
    print("Fórmulas:")
    print("  ea = |Valor Real - Valor Aproximado|")
    print("  er = ea / Valor Real")
    print("  e% = er * 100\n")
    
    vv = float(input("Valor verdadero (Real) : "))
    va = float(input("Valor aproximado       : "))

    ea  = abs(vv - va)
    er  = abs(ea / vv) if vv != 0 else float('inf')
    ep  = er * 100

    print("\n── Resultados ──────────────────────")
    print(f"  Error absoluto (ea)   : {ea:.6f}")
    print(f"  Error relativo (er)   : {er:.6f}")
    print(f"  Error porcentual (e%) : {ep:.4f} %")

# ==========================================
# 2. SERIE DE TAYLOR / MACLAURIN
# ==========================================
def serie_taylor():
    limpiar()
    print("📈 SERIE DE TAYLOR / MACLAURIN")
    print("-" * 40)

    expr_str = input("Ingresa f(x) [ej: log(x)]: ").strip()
    f_sym = sympify(expr_str)
    a_str = input("Centro a [ej: 1 o 0 (Maclaurin)]: ").strip()
    a_val = sympify(a_str)
    n_terms = int(input("Número de términos: "))

    print("\n── Derivadas y términos ─────────────────────")
    encabezados = ["Derivada", "f(x)", "f(x) deriv", "Término"]
    filas = []

    serie = Integer(0)
    deriv = f_sym

    for i in range(n_terms):
        val_en_a    = deriv.subs(x, a_val)
        factorial_i = math.factorial(i)
        coef_simplificado = simplify(val_en_a / factorial_i)
        
        termino_matematico = val_en_a / factorial_i * (x - a_val)**i
        serie += termino_matematico

        if i == 0:
            termino_str = str(nsimplify(coef_simplificado, rational=False))
        else:
            potencia = f"(x - {a_val})" if i == 1 else f"(x - {a_val})^{i}"
            coef_str = str(nsimplify(coef_simplificado, rational=False))
            termino_str = f"({coef_str}) * {potencia}"

        filas.append([
            i,                          
            str(simplify(deriv)),       
            f"{float(val_en_a):.6f}",   
            termino_str                 
        ])
        deriv = diff(deriv, x)

    imprimir_tabla(encabezados, filas)

    print(f"\n--- RESULTADO PARA EL EXAMEN ---")
    terminos_pizarron = []
    deriv_aux = f_sym
    for i in range(n_terms):
        val = deriv_aux.subs(x, a_val)
        fac = math.factorial(i)
        c = nsimplify(val/fac, rational=False)
        if c != 0:
            if i == 0: terminos_pizarron.append(f"{c}")
            elif i == 1: terminos_pizarron.append(f"({c})*(x - {a_val})")
            else: terminos_pizarron.append(f"({c})*(x - {a_val})^{i}")
        deriv_aux = diff(deriv_aux, x)
    
    print(f"FORMA (x - a): f(x) ≈ " + " + ".join(terminos_pizarron))
    print(f"FORMA EXPANDIDA: f(x) ≈ {expand(serie)}")

# ==========================================
# 3. MÉTODO DE BISECCIÓN
# ==========================================
def biseccion():
    limpiar()
    print("✂️  MÉTODO DE BISECCIÓN")
    expr_str = input("Ingresa f(x): ").strip()
    f_sym = sympify(expr_str)
    a = float(input("Extremo inferior a: "))
    b = float(input("Extremo superior b: "))

    modo = input("¿Criterio de parada? [1=iteraciones, 2=tolerancia]: ").strip()
    if modo == "1":
        max_iter = int(input("Número de iteraciones: "))
        tol = None
    else:
        advertencia_error()
        tol = float(input("Tolerancia: "))
        max_iter = 100

    fa, fb = evaluar(f_sym, a), evaluar(f_sym, b)
    if fa * fb > 0:
        print("⚠️  f(a) y f(b) tienen el mismo signo.")
        return

    encabezados = ["Iter", "a", "b", "xr", "f(xr)", "Error %"]
    filas = []
    xr_ant = None

    for i in range(1, max_iter + 1):
        xr = (a + b) / 2
        fxr = evaluar(f_sym, xr)
        ep = abs((xr - xr_ant) / xr) * 100 if xr_ant is not None else float('inf')
        filas.append([i, f"{a:.6f}", f"{b:.6f}", f"{xr:.6f}", f"{fxr:.6f}", f"{ep:.4f}"])

        if tol is not None and xr_ant is not None and ep < tol * 100:
            break
        if evaluar(f_sym, a) * fxr < 0:
            b = xr
        else:
            a = xr
        xr_ant = xr

    imprimir_tabla(encabezados, filas)

# ==========================================
# 4. MÉTODO DE NEWTON-RAPHSON
# ==========================================
def newton_raphson():
    limpiar()
    print("🔢 MÉTODO DE NEWTON-RAPHSON")
    expr_str = input("Ingresa f(x): ").strip()
    f_sym, df_sym = sympify(expr_str), diff(sympify(expr_str), x)
    print(f"\n  f'(x) = {df_sym}\n")
    x0 = float(input("Valor inicial x0: "))
    
    modo = input("¿Criterio de parada? [1=iteraciones, 2=tolerancia]: ").strip()
    if modo == "1":
        max_iter, tol = int(input("Número de iteraciones: ")), None
    else:
        advertencia_error()
        tol, max_iter = float(input("Tolerancia: ")), 100

    encabezados, filas, xi = ["Iter", "xi", "f(xi)", "f'(xi)", "x_{i+1}", "Error %"], [], x0

    for i in range(1, max_iter + 1):
        fxi, dfxi = evaluar(f_sym, xi), evaluar(df_sym, xi)
        if dfxi == 0: break
        xi1 = xi - fxi / dfxi
        ep = abs((xi1 - xi) / xi1) * 100 if xi1 != 0 else float('inf')
        filas.append([i, f"{xi:.6f}", f"{fxi:.6f}", f"{dfxi:.6f}", f"{xi1:.6f}", f"{ep:.4f}"])
        if tol is not None and ep < tol * 100 and i > 1: break
        xi = xi1
    imprimir_tabla(encabezados, filas)

# ==========================================
# 5. MÉTODO DE FALSA POSICIÓN
# ==========================================
def falsa_posicion():
    limpiar()
    print("📉 MÉTODO DE FALSA POSICIÓN")
    expr_str = input("Ingresa f(x): ").strip()
    f_sym = sympify(expr_str)
    xl = float(input("Extremo inferior xl: "))
    xu = float(input("Extremo superior xu: "))

    modo = input("¿Criterio de parada? [1=iteraciones, 2=tolerancia]: ").strip()
    if modo == "1": max_iter, tol = int(input("Número de iteraciones: ")), None
    else: advertencia_error(); tol, max_iter = float(input("Tolerancia: ")), 100

    if evaluar(f_sym, xl) * evaluar(f_sym, xu) > 0: return
    encabezados, filas, xr_ant = ["Iter", "xl", "xu", "xr", "f(xl)", "f(xu)", "f(xr)", "Error %"], [], None

    for i in range(1, max_iter + 1):
        fxl, fxu = evaluar(f_sym, xl), evaluar(f_sym, xu)
        xr = xu - fxu * (xl - xu) / (fxl - fxu)
        fxr = evaluar(f_sym, xr)
        ep = abs((xr - xr_ant) / xr) * 100 if xr_ant is not None else float('inf')
        filas.append([i, f"{xl:.6f}", f"{xu:.6f}", f"{xr:.6f}", f"{fxl:.6f}", f"{fxu:.6f}", f"{fxr:.6f}", f"{ep:.4f}"])
        if tol is not None and xr_ant is not None and ep < tol * 100: break
        if fxl * fxr < 0: xu = xr
        else: xl = xr
        xr_ant = xr
    imprimir_tabla(encabezados, filas)

# ==========================================
# 6. MÉTODO DEL PUNTO FIJO
# ==========================================
def punto_fijo():
    limpiar()
    print("📌 MÉTODO DEL PUNTO FIJO")
    g_sym = sympify(input("Ingresa g(x): ").strip())
    x0 = float(input("Valor inicial x0: "))
    max_iter = int(input("Número de iteraciones: "))

    encabezados, filas, xi = ["Iter", "xi", "g(xi) = x_{i+1}", "Error %"], [], x0
    for i in range(1, max_iter + 1):
        xi1 = evaluar(g_sym, xi)
        ep = abs((xi1 - xi) / xi1) * 100 if xi1 != 0 else float('inf')
        filas.append([i, f"{xi:.6f}", f"{xi1:.6f}", f"{ep:.4f}"])
        if math.isnan(xi1) or math.isinf(xi1): break
        xi = xi1
    imprimir_tabla(encabezados, filas)

# ==========================================
# 7. MÉTODO DE LA SECANTE
# ==========================================
def secante():
    limpiar()
    print("🪓 MÉTODO DE LA SECANTE")
    print("-" * 40)
    print("Fórmula: x_{i+1} = x_i - [ f(x_i)*(x_i - x_{i-1}) ] / [ f(x_i) - f(x_{i-1}) ]\n")
    
    expr_str = input("Ingresa f(x): ").strip()
    f_sym = sympify(expr_str)
    x_ant = float(input("Valor inicial x_{-1} : "))
    x_act = float(input("Valor inicial x_0    : "))
    
    modo = input("¿Criterio de parada? [1=iteraciones, 2=tolerancia]: ").strip()
    if modo == "1":
        max_iter = int(input("Número de iteraciones: "))
        tol = None
    else:
        advertencia_error()
        tol = float(input("Tolerancia: "))
        max_iter = 100

    encabezados = ["Iter", "x_{i-1}", "x_i", "f(x_{i-1})", "f(x_i)", "x_{i+1}", "Error %"]
    filas = []

    for i in range(1, max_iter + 1):
        fx_ant = evaluar(f_sym, x_ant)
        fx_act = evaluar(f_sym, x_act)
        
        if fx_act - fx_ant == 0:
            print("⚠️ División por cero. El método falla.")
            break
            
        x_sig = x_act - (fx_act * (x_act - x_ant)) / (fx_act - fx_ant)
        ep = abs((x_sig - x_act) / x_sig) * 100 if x_sig != 0 else float('inf')
        
        filas.append([i, f"{x_ant:.6f}", f"{x_act:.6f}", f"{fx_ant:.6f}", f"{fx_act:.6f}", f"{x_sig:.6f}", f"{ep:.4f}"])
        
        if tol is not None and ep < tol * 100:
            break
            
        x_ant = x_act
        x_act = x_sig

    imprimir_tabla(encabezados, filas)
    print(f"\n  Raíz aproximada : {x_sig:.6f}")


# ==========================================
# 8 y 9. HERRAMIENTAS EXTRAS
# ==========================================
def calculadora_derivadas():
    limpiar()
    print("CALCULADORA DE DERIVADAS")
    f_sym = sympify(input("Ingresa f(x): ").strip())
    n = int(input("Cuántas derivadas calcular?: "))
    encabezados, filas, deriv = ["n", "f^(n)(x)"], [], f_sym
    for i in range(n + 1):
        filas.append([i, str(simplify(deriv))])
        deriv = diff(deriv, x)
    imprimir_tabla(encabezados, filas)

def generador_despejes():
    limpiar()
    print("GENERADOR DE DESPEJES g(x) PARA PUNTO FIJO")
    f_sym = sympify(input("Ingresa f(x) (lado izquierdo igualado a 0): ").strip())
    x0 = float(sympify(input("Valor inicial x0: ").strip()))
    despejes = []
    for term in Add.make_args(f_sym):
        coef = term.coeff(x, 1)
        if coef != 0 and not coef.has(x):
            try: despejes.append(("Despeje lineal", simplify(-(f_sym - coef * x) / coef)))
            except: pass
    try:
        grado = degree(f_sym, x)
        coef_n = f_sym.coeff(x, grado)
        despejes.append((f"Raiz grado {grado}", simplify((-(f_sym - coef_n * x**grado) / coef_n) ** Rational(1, grado))))
    except: pass
    for k in [1, 2, 3]: despejes.append((f"x - f(x)/{k}", x - f_sym / k))

    print(f"\n  #  {'g(x)':<40} {'|g\'(x0)|':<12} Converge?")
    for idx, (nombre, g_expr) in enumerate(despejes, 1):
        try:
            val_dg = abs(float(diff(g_expr, x).subs(x, x0)))
            print(f"[{idx:>2}] {str(simplify(g_expr)):<40} {val_dg:<12.4f} {'SI ✅' if val_dg < 1 else 'NO ❌'}")
        except: pass

# ==========================================
# 10. REGRESIÓN LINEAL MÚLTIPLE (Con Fórmulas)
# ==========================================
def regresion_lineal_multiple():
    limpiar()
    print("📊 REGRESIÓN LINEAL MÚLTIPLE")
    print("-" * 40)
    print("1. Cargar datos de prueba por defecto (los de tu código C++)")
    print("2. Ingresar nuevos datos")
    origen = input("Elige (1 o 2): ").strip()

    if origen == "1":
        y  = [0.231, 0.107, 0.053, 0.129, 0.069, 0.030, 1.005, 0.559, 0.321, 2.948, 1.633, 0.934]
        x1 = [740, 740, 740, 805, 805, 805, 980, 980, 980, 1235, 1235, 1235]
        x2 = [1.10, 0.62, 0.31, 1.10, 0.62, 0.31, 1.10, 0.62, 0.31, 1.10, 0.62, 0.31]
        x3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    else:
        y = [float(i) for i in input("Ingresa valores de Y : ").split(',')]
        x1 = [float(i) for i in input("Ingresa valores de X1: ").split(',')]
        x2 = [float(i) for i in input("Ingresa valores de X2: ").split(',')]
        opc_x3 = input("¿Tienes X3? (s/n): ").strip().lower()
        x3 = [float(i) for i in input("Ingresa valores de X3: ").split(',')] if opc_x3 == 's' else []

    n = len(y)
    vars_indep = 3 if len(x3) > 0 else 2

    # Sumatorias
    sum_y = sum(y); sum_x1 = sum(x1); sum_x2 = sum(x2)
    sum_x1_sq = sum(i**2 for i in x1); sum_x2_sq = sum(i**2 for i in x2)
    sum_x1_x2 = sum(x1[i]*x2[i] for i in range(n))
    sum_x1_y = sum(x1[i]*y[i] for i in range(n)); sum_x2_y = sum(x2[i]*y[i] for i in range(n))

    # --- NUEVA SECCIÓN DE IMPRESIÓN DE SUMATORIAS ---
    print("\n--- SUMATORIAS CALCULADAS ---")
    print(f"n = {n}")
    print(f"ΣY  = {sum_y}")
    print(f"ΣX1 = {sum_x1:<10} | ΣX1^2 = {sum_x1_sq:<10} | ΣX1Y = {sum_x1_y}")
    print(f"ΣX2 = {sum_x2:<10} | ΣX2^2 = {sum_x2_sq:<10} | ΣX2Y = {sum_x2_y}")
    print(f"ΣX1X2 = {sum_x1_x2}")

    if vars_indep == 3:
        sum_x3 = sum(x3); sum_x3_sq = sum(i**2 for i in x3)
        sum_x1_x3 = sum(x1[i]*x3[i] for i in range(n)); sum_x2_x3 = sum(x2[i]*x3[i] for i in range(n))
        sum_x3_y = sum(x3[i]*y[i] for i in range(n))
        
        print(f"ΣX3 = {sum_x3:<10} | ΣX3^2 = {sum_x3_sq:<10} | ΣX3Y = {sum_x3_y}")
        print(f"ΣX1X3 = {sum_x1_x3:<10} | ΣX2X3 = {sum_x2_x3}")
    # ------------------------------------------------

    print("\n--- FÓRMULAS DEL SISTEMA BASE ---")
    if vars_indep == 2:
        print("1) an + b1(Ex1) + b2(Ex2) = Ey")
        print("2) a(Ex1) + b1(Ex1^2) + b2(Ex1x2) = Ex1y")
        print("3) a(Ex2) + b1(Ex1x2) + b2(Ex2^2) = Ex2y")
    else:
        print("1) an + b1(Ex1) + b2(Ex2) + b3(Ex3) = Ey")
        print("2) a(Ex1) + b1(Ex1^2) + b2(Ex1x2) + b3(Ex1x3) = Ex1y")
        print("3) a(Ex2) + b1(Ex1x2) + b2(Ex2^2) + b3(Ex2x3) = Ex2y")
        print("4) a(Ex3) + b1(Ex1x3) + b2(Ex2x3) + b3(Ex3^2) = Ex3y")

    print("\n--- SISTEMA SUSTITUIDO ---")
    if vars_indep == 2:
        print(f"{n}a + {sum_x1}b1 + {sum_x2}b2 = {sum_y}")
        print(f"{sum_x1}a + {sum_x1_sq}b1 + {sum_x1_x2}b2 = {sum_x1_y}")
        print(f"{sum_x2}a + {sum_x1_x2}b1 + {sum_x2_sq}b2 = {sum_x2_y}")
        
        A = Matrix([[n, sum_x1, sum_x2], [sum_x1, sum_x1_sq, sum_x1_x2], [sum_x2, sum_x1_x2, sum_x2_sq]])
        B = Matrix([sum_y, sum_x1_y, sum_x2_y])
        res = A.LUsolve(B)
        a, b1, b2 = float(res[0]), float(res[1]), float(res[2])
        print(f"\nEcuación: y = {a:.4f} {'+' if b1>=0 else '-'} {abs(b1):.4f}x1 {'+' if b2>=0 else '-'} {abs(b2):.4f}x2")

    elif vars_indep == 3:
        print(f"{n}a + {sum_x1}b1 + {sum_x2}b2 + {sum_x3}b3 = {sum_y}")
        print(f"{sum_x1}a + {sum_x1_sq}b1 + {sum_x1_x2}b2 + {sum_x1_x3}b3 = {sum_x1_y}")
        print(f"{sum_x2}a + {sum_x1_x2}b1 + {sum_x2_sq}b2 + {sum_x2_x3}b3 = {sum_x2_y}")
        print(f"{sum_x3}a + {sum_x1_x3}b1 + {sum_x2_x3}b2 + {sum_x3_sq}b3 = {sum_x3_y}")

        A = Matrix([[n, sum_x1, sum_x2, sum_x3], [sum_x1, sum_x1_sq, sum_x1_x2, sum_x1_x3],
                    [sum_x2, sum_x1_x2, sum_x2_sq, sum_x2_x3], [sum_x3, sum_x1_x3, sum_x2_x3, sum_x3_sq]])
        B = Matrix([sum_y, sum_x1_y, sum_x2_y, sum_x3_y])
        res = A.LUsolve(B)
        a, b1, b2, b3 = float(res[0]), float(res[1]), float(res[2]), float(res[3])
        print(f"\nEcuación: y = {a:.4f} {'+' if b1>=0 else '-'} {abs(b1):.4f}x1 {'+' if b2>=0 else '-'} {abs(b2):.4f}x2 {'+' if b3>=0 else '-'} {abs(b3):.4f}x3")

# ==========================================
# 11. POLINOMIOS DE LAGRANGE
# ==========================================
def lagrange():
    limpiar()
    print("🎢 POLINOMIOS DE LAGRANGE")
    print("-" * 40)
    
    n_puntos = int(input("¿Cuántos puntos de datos tienes? (ej. 2 para N=1, 3 para N=2): "))
    X_vals, Y_vals = [], []
    for i in range(n_puntos):
        X_vals.append(float(input(f"Ingresa X_{i}: ")))
        Y_vals.append(float(input(f"Ingresa f(X_{i}): ")))

    xp_str = input("\n¿Valor de 'x' a evaluar al final? (ej. 4 o Enter para omitir): ").strip()

    N = n_puntos - 1
    print(f"\n--- FÓRMULA GENERAL (N={N}) ---")
    if N == 1:
        print("f_1(x) = [ (x-x1)/(x0-x1) ]*f(x0)  +  [ (x-x0)/(x1-x0) ]*f(x1)")
    elif N == 2:
        print("f_2(x) = [ (x-x1)(x-x2) / (x0-x1)(x0-x2) ]*f(x0) + [ (x-x0)(x-x2) / (x1-x0)(x1-x2) ]*f(x1) + ...")
    else:
        print("Sumatoria de L_i(x) * f(x_i)")

    polinomio = Integer(0)
    terminos_str = []

    for i in range(n_puntos):
        term = Integer(1)
        num_str = []
        den_val = 1
        for j in range(n_puntos):
            if i != j:
                term *= (x - X_vals[j]) / (X_vals[i] - X_vals[j])
                num_str.append(f"(x - {X_vals[j]})")
                den_val *= (X_vals[i] - X_vals[j])
        term *= Y_vals[i]
        polinomio += term

        num_display = "".join(num_str) if num_str else "1"
        terminos_str.append(f"[{num_display} / {den_val}]({Y_vals[i]})")

    print("\n--- 1. ECUACIÓN ARMADA (Sustitución Directa) ---")
    print(f"f_{N}(x) = " + "  +  ".join(terminos_str))

    polinomio_expandido = expand(polinomio)
    print("\n--- 2. ECUACIÓN FINAL SIMPLIFICADA ---")
    print(f"f_{N}(x) = {polinomio_expandido}")

    if xp_str:
        xp = float(xp_str)
        resultado = polinomio_expandido.subs(x, xp)
        print(f"\n--- 3. EVALUACIÓN EN x = {xp} ---")
        print(f"f_{N}({xp}) = {resultado:.4f}")

# ==========================================
# MENÚ PRINCIPAL
# ==========================================
def menu():
    opciones = {
        "1": ("Error Absoluto, Relativo y Porcentual", error_absoluto_relativo),
        "2": ("Serie de Taylor / Maclaurin", serie_taylor),
        "3": ("Bisección", biseccion),
        "4": ("Newton-Raphson", newton_raphson),
        "5": ("Falsa Posición", falsa_posicion),
        "6": ("Punto Fijo", punto_fijo),
        "7": ("Secante", secante),
        "8": ("Calculadora de Derivadas", calculadora_derivadas),
        "9": ("Generador de Despejes g(x)", generador_despejes),
        "10":("Regresión Lineal Múltiple", regresion_lineal_multiple),
        "11":("Polinomios de Lagrange", lagrange)
    }

    while True:
        print("\n" + "═" * 55)
        print("   MÉTODOS NUMÉRICOS — Menú Principal (Final)")
        print("═" * 55)
        for k, (nombre, _) in opciones.items():
            print(f"  [{k.rjust(2)}]  {nombre}")
        print("  [ 0]  Salir")
        print("═" * 55)

        op = input("Elige una opción: ").strip()

        if op == "0":
            print("\n¡Éxito en el parcial! A romperla en la UVM 🚀\n")
            break
        elif op in opciones:
            try:
                opciones[op][1]()
            except Exception as e:
                print(f"\n⚠️  Error: {e}")
                print("Revisa los datos o funciones ingresadas.")
            input("\n[Presiona Enter para volver al menú]")
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()


"""
═══════════════════════════════════════════════════════════════════
        FORMULARIO DE ENTRADA (Sintaxis para la Terminal)
═══════════════════════════════════════════════════════════════════
Usa estas reglas para escribir funciones sin errores:

1. OPERADORES BÁSICOS:
   Suma: + 
   Resta: -     
   Multiplicación: * División: /
   Potencia: ** (Ejemplo: x al cuadrado es x**2)

2. FUNCIONES ESPECIALES:
   Exponencial (e^x): exp(x)
   Logaritmo Natural: log(x)
   Raíz Cuadrada:     sqrt(x)
   Seno / Coseno:     sin(x) / cos(x)
   Tangente:          tan(x)
   Constante Pi:      pi

3. EJEMPLOS COMPLEJOS PARA EL EXAMEN:
   - Para f(x) = (x^2 - 5x + 2) / (e^x):
     Escribe: (x**2 - 5*x + 2) / exp(x)
     
   - Para f(x) = sen(x^2) + ln(3x) - 1:
     Escribe: sin(x**2) + log(3*x) - 1
     
   - Para Lagrange (N=2) de tus fotos:
     Los puntos se meten uno a uno cuando el programa los pida.
     Ejemplo: X_0: 2, f(X_0): 6
═══════════════════════════════════════════════════════════════════
"""
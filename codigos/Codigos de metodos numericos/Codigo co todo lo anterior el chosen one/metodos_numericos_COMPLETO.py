"""
╔══════════════════════════════════════════════════════════════════╗
║        MÉTODOS NUMÉRICOS — HERRAMIENTA COMPLETA                 ║
║              1er Parcial  +  2do Parcial                        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import math
import sys
import re

from sympy import *

try:
    from tabulate import tabulate
    TABULATE = True
except ImportError:
    TABULATE = False

x = symbols('x')


# ══════════════════════════════════════════════════════════════════
#  UTILIDADES COMPARTIDAS
# ══════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════
#  1er PARCIAL — MÉTODOS Y FUNCIONES
# ══════════════════════════════════════════════════════════════════

# ── 1. Errores ────────────────────────────────────────────────────
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
    ea = abs(vv - va)
    er = abs(ea / vv) if vv != 0 else float('inf')
    ep = er * 100
    print("\n── Resultados ──────────────────────")
    print(f"  Error absoluto (ea)   : {ea:.6f}")
    print(f"  Error relativo (er)   : {er:.6f}")
    print(f"  Error porcentual (e%) : {ep:.4f} %")

# ── 2. Serie de Taylor / Maclaurin ────────────────────────────────
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
        val_en_a = deriv.subs(x, a_val)
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

        filas.append([i, str(simplify(deriv)), f"{float(val_en_a):.6f}", termino_str])
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

# ── 3. Bisección ──────────────────────────────────────────────────
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
        if tol is not None and xr_ant is not None and ep < tol * 100: break
        if evaluar(f_sym, a) * fxr < 0: b = xr
        else: a = xr
        xr_ant = xr

    imprimir_tabla(encabezados, filas)

# ── 4. Newton-Raphson ─────────────────────────────────────────────
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

# ── 5. Falsa Posición ─────────────────────────────────────────────
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

# ── 6. Punto Fijo ─────────────────────────────────────────────────
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

# ── 7. Secante ────────────────────────────────────────────────────
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
    x_sig = x_act

    for i in range(1, max_iter + 1):
        fx_ant = evaluar(f_sym, x_ant)
        fx_act = evaluar(f_sym, x_act)
        if fx_act - fx_ant == 0:
            print("⚠️ División por cero. El método falla.")
            break
        x_sig = x_act - (fx_act * (x_act - x_ant)) / (fx_act - fx_ant)
        ep = abs((x_sig - x_act) / x_sig) * 100 if x_sig != 0 else float('inf')
        filas.append([i, f"{x_ant:.6f}", f"{x_act:.6f}", f"{fx_ant:.6f}", f"{fx_act:.6f}", f"{x_sig:.6f}", f"{ep:.4f}"])
        if tol is not None and ep < tol * 100: break
        x_ant = x_act
        x_act = x_sig

    imprimir_tabla(encabezados, filas)
    print(f"\n  Raíz aproximada : {x_sig:.6f}")

# ── 8. Calculadora de Derivadas ───────────────────────────────────
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

# ── 9. Generador de despejes g(x) ─────────────────────────────────
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

# ── 10. Regresión Lineal Múltiple ─────────────────────────────────
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

    sum_y = sum(y); sum_x1 = sum(x1); sum_x2 = sum(x2)
    sum_x1_sq = sum(i**2 for i in x1); sum_x2_sq = sum(i**2 for i in x2)
    sum_x1_x2 = sum(x1[i]*x2[i] for i in range(n))
    sum_x1_y = sum(x1[i]*y[i] for i in range(n)); sum_x2_y = sum(x2[i]*y[i] for i in range(n))

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

# ── 11. Polinomios de Lagrange ────────────────────────────────────
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

# ── Menú del 1er Parcial ──────────────────────────────────────────
def menu_primer_parcial():
    opciones = {
        "1":  ("Error Absoluto, Relativo y Porcentual", error_absoluto_relativo),
        "2":  ("Serie de Taylor / Maclaurin",           serie_taylor),
        "3":  ("Bisección",                             biseccion),
        "4":  ("Newton-Raphson",                        newton_raphson),
        "5":  ("Falsa Posición",                        falsa_posicion),
        "6":  ("Punto Fijo",                            punto_fijo),
        "7":  ("Secante",                               secante),
        "8":  ("Calculadora de Derivadas",              calculadora_derivadas),
        "9":  ("Generador de Despejes g(x)",            generador_despejes),
        "10": ("Regresión Lineal Múltiple",             regresion_lineal_multiple),
        "11": ("Polinomios de Lagrange",                lagrange),
    }

    while True:
        print("\n" + "═" * 62)
        print("        📘  1er PARCIAL — Métodos Numéricos")
        print("═" * 62)
        for k, (nombre, _) in opciones.items():
            print(f"  [{k.rjust(2)}]  {nombre}")
        print("  [ 0]  ← Volver al menú principal")
        print("═" * 62)

        op = input("Elige una opción: ").strip()
        if op == "0":
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


# ══════════════════════════════════════════════════════════════════
#  2do PARCIAL — MÉTODOS ITERATIVOS (Álgebra Lineal)
# ══════════════════════════════════════════════════════════════════

# ── Estados ───────────────────────────────────────────────────────
estado_jacobi = {
    "n": None, "A": None, "b": None, "x0": None,
    "tol": 0.001, "max_iter": 100, "resultado": None,
}
estado_seidel = {
    "n": None, "A": None, "b": None, "x0": None,
    "tol": 0.001, "max_iter": 100, "resultado": None,
}
estado_diagonal     = {"n": None, "A": None, "b": None}
estado_cramer       = {"n": None, "A": None, "b": None}
estado_inversa      = {"n": None, "A": None, "b": None}
estado_gauss_jordan = {"n": None, "A": None, "b": None}
estado_gauss_elim   = {"n": None, "A": None, "b": None}

# ── Utilidades de matrices ─────────────────────────────────────────
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
    print()
    titulo("  TAMAÑO DEL SISTEMA  ")
    print()
    opciones_n = list(range(2, 11))
    for i, k in enumerate(opciones_n, 1):
        print(f"  [{i}]  {k}×{k}")
    print("  [0]  Volver")
    print()
    op = pedir_opcion([str(i) for i in range(len(opciones_n) + 1)])
    if op == "0": return
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
                fila = [float(v) for v in raw]
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
    if op == "0": return
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
        if op == "0": break
        elif op == "1": mostrar_tabla(hist, n, 0, len(hist))
        elif op == "2": mostrar_solucion(x, n, conv, len(hist))
        elif op == "3":
            total = len(hist)
            print(f"\n  Hay {total} iteraciones disponibles.")
            desde = pedir_entero("  Desde iteración: ", 1, total)
            hasta = pedir_entero("  Hasta iteración: ", desde, total)
            mostrar_tabla(hist, n, desde - 1, hasta)
        pausa()

def menu_verificacion(estado):
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

# ── Diagonal Dominante ────────────────────────────────────────────
def _es_dd_fila(A, n, i):
    return abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i)

def dd_verificar(estado):
    print()
    titulo("  VERIFICACIÓN — DIAGONAL DOMINANTE  ")
    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2)."); pausa(); return
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
        if not ok: todo_ok = False
        terminos_suma = " + ".join(f"|{A[i][j]:.3f}|" for j in range(n) if j != i)
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
    print()
    titulo("  ACOMODAR — DIAGONAL DOMINANTE  ")
    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2)."); pausa(); return
    n, A, b = estado["n"], estado["A"], estado["b"]
    ya_es_dd = all(_es_dd_fila(A, n, i) for i in range(n))
    if ya_es_dd:
        print()
        print("  ✔  El sistema ya es diagonalmente dominante.")
        imprimir_matriz(A, b, n)
        pausa(); return
    print()
    print("  Matriz original:")
    imprimir_matriz(A, b, n)
    print()
    print("  Algoritmo greedy: para cada posición j se elige la fila")
    print("  disponible con mayor |a_ij| en la columna j.\n")
    disponibles = list(range(n))
    orden = []
    for j in range(n):
        linea("·")
        print(f"  Paso {j+1}: buscando fila para posición {j+1} (columna x{j+1})")
        mejor_i = None; mejor_val = -1
        for i in disponibles:
            val = abs(A[i][j])
            if val > mejor_val:
                mejor_val = val; mejor_i = i
        for i in disponibles:
            val = abs(A[i][j])
            marca = "  ← elegida" if i == mejor_i else ""
            print(f"    Ec.{i+1}  |a_{i+1}{j+1}| = {val:.4f}{marca}")
        orden.append(mejor_i)
        disponibles.remove(mejor_i)
        print(f"\n  → Se asigna Ec.{mejor_i+1} a la Posición {j+1}")

    A_nueva = [A[i][:] for i in orden]
    b_nueva = [b[i]    for i in orden]
    es_dd = all(
        abs(A_nueva[i][i]) > sum(abs(A_nueva[i][j]) for j in range(n) if j != i)
        for i in range(n)
    )
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
        print(f"  {pos+1:>10}  {ec_orig:>14}  {diag:>10.4f}  {resto:>10.4f}  {'✔' if ok else '✘':>5}")
    linea()
    print()
    if es_dd:
        print("  ✔  RESULTADO: El sistema reordenado ES diagonalmente dominante.")
    else:
        print("  ✘  RESULTADO: No se logró diagonal dominante con ningún reordenamiento.")
    print()
    print("  Matriz reordenada [A | b]:")
    imprimir_matriz(A_nueva, b_nueva, n)
    print()
    linea()
    print("  Ecuaciones despejadas para iteración:")
    linea()
    for i in range(n):
        coef_b = b_nueva[i] / A_nueva[i][i]
        partes = [f"  x{i+1}  =  {coef_b:+.4f}"]
        for j in range(n):
            if j == i: continue
            coef = -A_nueva[i][j] / A_nueva[i][i]
            partes.append(f"({coef:+.4f})·x{j+1}")
        print("  " + "  +  ".join(partes).strip())
    linea()
    pausa()

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
        print("  [0]  Volver")
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

# ── Gauss-Jacobi ──────────────────────────────────────────────────
def resolver_jacobi(estado):
    print()
    titulo("  RESOLVIENDO — JACOBI  ")
    if estado["n"] is None:
        print("\n  ⚠  Define el tamaño del sistema (Opción 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Ingresa los coeficientes (Opción 2)."); pausa(); return
    n = estado["n"]
    A = [fila[:] for fila in estado["A"]]
    b = estado["b"][:]
    tol, max_iter = estado["tol"], estado["max_iter"]

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
            pausa(); return

    print(f"  Calculando... (tol={tol}, máx {max_iter} iter.)\n")
    x0 = estado["x0"] if estado["x0"] else [0.0] * n
    print(f"  Vector inicial x0: {[round(v, 4) for v in x0]}\n")

    x = x0[:]
    historial = []
    convergio = False

    for k in range(1, max_iter + 1):
        x_nuevo = [0.0] * n
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_nuevo[i] = (b[i] - s) / A[i][i]
        error = max(abs(x_nuevo[i] - x[i]) for i in range(n))
        ep = [
            abs((x_nuevo[i] - x[i]) / x_nuevo[i]) * 100 if abs(x_nuevo[i]) > 1e-14 else 0.0
            for i in range(n)
        ]
        historial.append({"k": k, "x": x_nuevo[:], "error": error, "ep": ep})
        x = x_nuevo[:]
        if error <= tol:
            convergio = True; break

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
    print("  (Ve a Opción 6 para ver la tabla completa de iteraciones)")
    pausa()

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
        print("  [0]  Volver")
        print()
        if est["n"]:
            x0_txt = f"x0={[round(v,2) for v in est['x0']]}" if est["x0"] else "x0=ceros"
            print(f"  Sistema: {est['n']}×{est['n']}   Tol: {est['tol']}   Iter. máx: {est['max_iter']}   {x0_txt}")
            print(f"  Datos:   {'✔ coeficientes cargados' if est['A'] else '✘ sin coeficientes'}")
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

# ── Gauss-Seidel ──────────────────────────────────────────────────
def resolver_seidel(estado):
    print()
    titulo("  RESOLVIENDO — GAUSS-SEIDEL  ")
    if estado["n"] is None:
        print("\n  ⚠  Define el tamaño del sistema (Opción 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Ingresa los coeficientes (Opción 2)."); pausa(); return
    n = estado["n"]
    A = [fila[:] for fila in estado["A"]]
    b = estado["b"][:]
    tol, max_iter = estado["tol"], estado["max_iter"]

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
            pausa(); return

    print(f"  Calculando... (tol={tol}, máx {max_iter} iter.)\n")
    x0 = estado["x0"] if estado["x0"] else [0.0] * n
    print(f"  Vector inicial x0: {[round(v, 4) for v in x0]}\n")

    x = x0[:]
    historial = []
    convergio = False

    for k in range(1, max_iter + 1):
        x_anterior = x[:]
        for i in range(n):
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - s) / A[i][i]
        error = max(abs(x[i] - x_anterior[i]) for i in range(n))
        ep = [
            abs((x[i] - x_anterior[i]) / x[i]) * 100 if abs(x[i]) > 1e-14 else 0.0
            for i in range(n)
        ]
        historial.append({"k": k, "x": x[:], "error": error, "ep": ep})
        if error <= tol:
            convergio = True; break

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
    print("  (Ve a Opción 6 para ver la tabla completa de iteraciones)")
    pausa()

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
        print("  [0]  Volver")
        print()
        if est["n"]:
            x0_txt = f"x0={[round(v,2) for v in est['x0']]}" if est["x0"] else "x0=ceros"
            print(f"  Sistema: {est['n']}×{est['n']}   Tol: {est['tol']}   Iter. máx: {est['max_iter']}   {x0_txt}")
            print(f"  Datos:   {'✔ coeficientes cargados' if est['A'] else '✘ sin coeficientes'}")
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

# ── Despeje de ecuaciones ─────────────────────────────────────────
def _parsear_ecuacion(texto, variables):
    if "=" not in texto:
        raise ValueError("La ecuación no contiene '='.")
    partes = texto.split("=", 1)
    lado_izq = partes[0].strip()
    lado_der = partes[1].strip()

    def parsear_lado(expr):
        expr = expr.strip()
        if expr and expr[0] not in "+-":
            expr = "+" + expr
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
    todas = set(iz.keys()) | set(de.keys())
    desconocidas = todas - set(variables) - {"__cte__"}
    if desconocidas:
        raise ValueError(f"Variables no declaradas: {', '.join(sorted(desconocidas))}")
    coefs = [iz.get(v, 0.0) - de.get(v, 0.0) for v in variables]
    b = de.get("__cte__", 0.0) - iz.get("__cte__", 0.0)
    return coefs, b

def _flujo_despeje():
    print()
    titulo("  INGRESAR SISTEMA  ")
    print()
    print("  Paso 1: declara las variables (separadas por espacios o comas).")
    print("  Ejemplo:  a b c d e\n")
    while True:
        raw = input("  Variables: ").replace(",", " ").split()
        if len(raw) < 2:
            print("  ⚠  Necesitas al menos 2 variables.")
            continue
        invalidas = [v for v in raw if not re.match(r'^[a-zA-Z_]\w*$', v)]
        if invalidas:
            print(f"  ⚠  Nombres inválidos: {', '.join(invalidas)}")
            continue
        variables = raw
        break

    n = len(variables)
    print(f"\n  Variables ({n}): {' , '.join(variables)}\n")
    print(f"  Paso 2: ingresa las {n} ecuaciones, una por línea.\n")

    A, b_vec = [], []
    i = 0
    while i < n:
        linea("·")
        print(f"  Ecuación {i+1} de {n}:")
        texto = input("    > ").strip()
        if not texto:
            print("  ⚠  La ecuación no puede estar vacía."); continue
        try:
            coefs, bi = _parsear_ecuacion(texto, variables)
            A.append(coefs)
            b_vec.append(bi)
            terminos = []
            for j, v in enumerate(variables):
                c = coefs[j]
                if abs(c) < 1e-14: continue
                signo = "+" if c >= 0 else "-"
                terminos.append(f"{signo} {abs(c):.4g}·{v}")
            lhs = "  ".join(terminos).lstrip("+").strip()
            print(f"    → {lhs} = {bi:.4g}")
            i += 1
        except ValueError as e:
            print(f"  ⚠  Error: {e}  — vuelve a intentarlo.")

    print()
    linea()
    print("  Matriz [A | b]  resultante:")
    linea()
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

    dd = all(abs(A[i][i]) > sum(abs(A[i][j]) for j in range(n) if j != i) for i in range(n))
    print()
    if dd:
        print("  ✔  El sistema ES diagonalmente dominante.")
    else:
        print("  ✘  El sistema NO es diagonalmente dominante.")
        A_r, b_r, orden, dd_r = reordenar_diagonal(A, b_vec, n)
        if dd_r:
            print("     Se encontró un reordenamiento que SÍ lo es:\n")
            for pos, ec_orig in enumerate(orden):
                print(f"     Posición {pos+1}  ←  Ec. original {ec_orig+1}")
            A, b_vec = A_r, b_r

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
        est["n"] = n; est["A"] = [f[:] for f in A]
        est["b"] = b_vec[:]; est["x0"] = None; est["resultado"] = None
        metodo = "Gauss-Jacobi" if op == "1" else "Gauss-Seidel"
        print(f"\n  ✔  Sistema cargado en {metodo}.")
        print(f"     Variables: " + ", ".join(f"{v}=x{i+1}" for i, v in enumerate(variables)))
    pausa()

def menu_despeje():
    while True:
        print()
        titulo("  DESPEJE DE ECUACIONES  ")
        print()
        print("  Ingresa un sistema en forma natural, por ejemplo:")
        print("    -3a + 2b + 5d = 50 + 3c + 10e")
        print()
        print("  [1]  Ingresar sistema")
        print("  [0]  Volver")
        print()
        linea()
        op = pedir_opcion(["0", "1"])
        if op == "0": break
        elif op == "1": _flujo_despeje()

# ── Determinantes / Regla de Cramer ───────────────────────────────
def _determinante(M):
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
        if abs(pivote) < 1e-14: return 0.0
        det *= pivote
        for fila in range(col + 1, n):
            factor = mat[fila][col] / pivote
            for k in range(col, n):
                mat[fila][k] -= factor * mat[col][k]
    return det

def _sustituir_columna(A, b, col):
    n = len(A)
    M = [fila[:] for fila in A]
    for i in range(n):
        M[i][col] = b[i]
    return M

def _mostrar_matriz_pequeña(M, n, etiqueta=""):
    ancho_col = 9 if n <= 6 else 7
    fmt_num = f"{{:>{ancho_col}.4g}}"
    if etiqueta: print(f"  {etiqueta}")
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
        print("\n  ⚠  Primero define el tamaño (Opción 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2)."); pausa(); return
    n = estado["n"]
    A = estado["A"]
    b = estado["b"]
    det_A = _determinante(A)
    print()
    imprimir_matriz(A, b, n)
    print()
    if n <= 4: _mostrar_matriz_pequeña(A, n, "Matriz A:")
    print(f"  det(A) = {det_A:.6f}")
    if abs(det_A) < 1e-14:
        print()
        print("  ✘  det(A) = 0 → el sistema no tiene solución única.")
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
        if n <= 4: _mostrar_matriz_pequeña(Mi, n, f"A{i+1}  (col {i+1} <- b):")
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
        print("  [1]  Ingresar / cambiar tamaño del sistema  (hasta 10x10)")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Resolver por Cramer")
        print("  [0]  Volver")
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

# ── Matriz Inversa ────────────────────────────────────────────────
def _matriz_inversa(A):
    n   = len(A)
    aug = [A[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        max_fila = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[max_fila][col]) < 1e-14:
            raise ValueError("La matriz es singular (det = 0). No tiene inversa.")
        if max_fila != col:
            aug[col], aug[max_fila] = aug[max_fila], aug[col]
        pivote = aug[col][col]
        aug[col] = [v / pivote for v in aug[col]]
        for fila in range(n):
            if fila == col: continue
            factor = aug[fila][col]
            aug[fila] = [aug[fila][k] - factor * aug[col][k] for k in range(2 * n)]
    return [fila[n:] for fila in aug]

def _imprimir_matriz_cuadrada(M, n, titulo_col=None, etiqueta=""):
    ancho = 10 if n <= 5 else 8 if n <= 7 else 7
    fmt_n = f"{{:>{ancho}.5f}}"
    fmt_s = f"{{:>{ancho}}}"
    if etiqueta: print(f"\n  {etiqueta}")
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
    return [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]

def resolver_inversa(estado):
    print()
    titulo("  RESOLVIENDO — MATRIZ INVERSA  ")
    if estado["n"] is None:
        print("\n  Primero define el tamano (Opcion 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  Primero ingresa los coeficientes (Opcion 2)."); pausa(); return
    n = estado["n"]
    A = estado["A"]
    b = estado["b"]
    headers = [f"c{j+1}" for j in range(n)]
    ancho = 10 if n <= 5 else 8 if n <= 7 else 7
    fmt_n = f"{{:>{ancho}.4g}}"
    fmt_s = f"{{:>{ancho}}}"
    print()
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
    print()
    print("  Paso 1: Calcular A⁻¹  (Gauss-Jordan con pivoteo parcial)")
    print()
    try:
        inv_A = _matriz_inversa(A)
    except ValueError as e:
        print(f"\n  ERROR: {e}"); pausa(); return
    _imprimir_matriz_cuadrada(inv_A, n, titulo_col=headers, etiqueta="A⁻¹ =")
    print()
    print("  Paso 2: Calcular x = A⁻¹ · b")
    print()
    x = _mul_matriz_vector(inv_A, b, n)
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
        linea("·")
        for i in range(n):
            print(f"  x{i+1} = {x[i]:>14.8f}")
        linea("·")
    print()
    linea("=")
    print("  SOLUCION  x = A⁻¹ · b :")
    linea("=")
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {xi:.8f}")
    linea("=")
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
        print()
        print("  [1]  Ingresar / cambiar tamaño del sistema  (hasta 10x10)")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Resolver por matriz inversa")
        print("  [0]  Volver")
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

# ── Eliminación Gaussiana (con sustitución regresiva) ────────────
estado_gauss_elim = {"n": None, "A": None, "b": None}

def resolver_gauss_eliminacion(estado):
    print()
    titulo("  RESOLVIENDO — ELIMINACIÓN GAUSSIANA  ")
    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2)."); pausa(); return

    n = estado["n"]
    aug = [estado["A"][i][:] + [estado["b"][i]] for i in range(n)]

    ancho = 10 if n <= 5 else 8 if n <= 7 else 7
    fmt_n = f"{{:>{ancho}.4g}}"
    fmt_s = f"{{:>{ancho}}}"

    def imprimir_aug(mat, etiqueta=""):
        if etiqueta:
            print(f"\n  {etiqueta}")
        linea("·")
        enc = "        "
        for j in range(n):
            enc += fmt_s.format(f"x{j+1}")
        enc += fmt_s.format("| b")
        print(enc)
        linea("·")
        for i in range(n):
            fila = f"  Ec.{i+1:<3}"
            for j in range(n):
                fila += fmt_n.format(mat[i][j])
            fila += "  |" + fmt_n.format(mat[i][n])
            print(fila)
        linea("·")

    print()
    print("  Sistema inicial  [A | b]:")
    imprimir_aug(aug)
    print()
    print("  ── FASE 1: Eliminación hacia adelante (forma triangular superior) ──")

    paso = 1
    for col in range(n):
        # Pivoteo parcial
        max_fila = col
        for fila in range(col + 1, n):
            if abs(aug[fila][col]) > abs(aug[max_fila][col]):
                max_fila = fila
        if abs(aug[max_fila][col]) < 1e-14:
            print(f"\n  ✘  Columna {col+1} es cero: el sistema no tiene solución única.")
            pausa(); return
        if max_fila != col:
            aug[col], aug[max_fila] = aug[max_fila], aug[col]
            print(f"\n  ── Paso {paso}: intercambiar fila {col+1} ↔ fila {max_fila+1}  (pivoteo parcial)")
            paso += 1
            imprimir_aug(aug)

        # Eliminar SOLO hacia abajo
        pivote = aug[col][col]
        for fila in range(col + 1, n):
            factor = aug[fila][col] / pivote
            if abs(factor) < 1e-14:
                continue
            aug[fila] = [aug[fila][k] - factor * aug[col][k] for k in range(n + 1)]
            signo = "+" if factor >= 0 else "-"
            print(f"\n  ── Paso {paso}: fila {fila+1}  ←  fila {fila+1}  {signo}  ({abs(factor):.4g}) × fila {col+1}")
            paso += 1
            imprimir_aug(aug)

    print()
    print("  ✔  Matriz triangular superior obtenida.")
    print()
    print("  ── FASE 2: Sustitución regresiva ──")
    linea()

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        if abs(aug[i][i]) < 1e-14:
            print(f"  ✘  División por cero en la ecuación {i+1}.")
            pausa(); return
        s = sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (aug[i][n] - s) / aug[i][i]

        partes = f"  x{i+1} = ( {aug[i][n]:.4g}"
        for j in range(i + 1, n):
            coef = aug[i][j]
            signo = "-" if coef >= 0 else "+"
            partes += f"  {signo}  {abs(coef):.4g}·({x[j]:.4g})"
        partes += f" ) / {aug[i][i]:.4g}  =  {x[i]:.6f}"
        print(partes)

    linea()
    print()
    linea("=")
    print("  SOLUCIÓN:")
    linea("=")
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {xi:.8f}")
    linea("=")

    print()
    print("  Verificación  Ax = b:")
    linea()
    print(f"  {'Ec.':>4}  {'Ax calculado':>18}  {'b esperado':>12}  {'Error abs.':>12}")
    linea()
    A_orig = estado["A"]
    b_orig = estado["b"]
    for i in range(n):
        ax  = sum(A_orig[i][j] * x[j] for j in range(n))
        err = abs(ax - b_orig[i])
        print(f"  Ec.{i+1}  {ax:>18.6f}  {b_orig[i]:>12.6f}  {err:>12.2e}")
    linea()
    pausa()

def menu_gauss_eliminacion():
    est = estado_gauss_elim
    while True:
        print()
        titulo("  ELIMINACIÓN GAUSSIANA  ")
        print()
        print("  Resuelve Ax = b en dos fases:")
        print("  1) Eliminación hacia adelante → forma triangular superior.")
        print("  2) Sustitución regresiva → obtiene cada xi.")
        print("  Muestra cada operación de fila paso a paso.")
        print()
        print("  [1]  Ingresar / cambiar tamaño del sistema  (hasta 10×10)")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Resolver paso a paso")
        print("  [0]  Volver")
        print()
        if est["n"]:
            cargado = "✔ coeficientes cargados" if est["A"] else "✘ sin coeficientes"
            print(f"  Sistema: {est['n']}×{est['n']}   {cargado}")
        else:
            print("  Sistema: no definido aún")
        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3"])
        if   op == "0": break
        elif op == "1": menu_tamano(est)
        elif op == "2": menu_coeficientes(est)
        elif op == "3": resolver_gauss_eliminacion(est)

# ── Menú del 2do Parcial ──────────────────────────────────────────
# ── Gauss-Jordan ──────────────────────────────────────────────────
def resolver_gauss_jordan(estado):
    print()
    titulo("  RESOLVIENDO — GAUSS-JORDAN  ")
    if estado["n"] is None:
        print("\n  ⚠  Primero define el tamaño (Opción 1)."); pausa(); return
    if estado["A"] is None:
        print("\n  ⚠  Primero ingresa los coeficientes (Opción 2)."); pausa(); return

    n = estado["n"]
    # Construir matriz aumentada [A | b]
    aug = [estado["A"][i][:] + [estado["b"][i]] for i in range(n)]

    ancho = 10 if n <= 5 else 8 if n <= 7 else 7
    fmt_n = f"{{:>{ancho}.4g}}"
    fmt_s = f"{{:>{ancho}}}"

    def imprimir_aug(mat, etiqueta=""):
        if etiqueta:
            print(f"\n  {etiqueta}")
        linea("·")
        enc = "        "
        for j in range(n):
            enc += fmt_s.format(f"x{j+1}")
        enc += fmt_s.format("| b")
        print(enc)
        linea("·")
        for i in range(n):
            fila = f"  Ec.{i+1:<3}"
            for j in range(n):
                fila += fmt_n.format(mat[i][j])
            fila += "  |" + fmt_n.format(mat[i][n])
            print(fila)
        linea("·")

    print()
    print("  Sistema inicial  [A | b]:")
    imprimir_aug(aug)

    paso = 1
    for col in range(n):
        # Pivoteo parcial
        max_fila = col
        for fila in range(col + 1, n):
            if abs(aug[fila][col]) > abs(aug[max_fila][col]):
                max_fila = fila
        if abs(aug[max_fila][col]) < 1e-14:
            print(f"\n  ✘  Columna {col+1} es cero: el sistema no tiene solución única.")
            pausa(); return
        if max_fila != col:
            aug[col], aug[max_fila] = aug[max_fila], aug[col]
            print(f"\n  ── Paso {paso}: intercambiar fila {col+1} ↔ fila {max_fila+1}  (pivoteo parcial)")
            paso += 1
            imprimir_aug(aug)

        # Normalizar fila pivote
        pivote = aug[col][col]
        aug[col] = [v / pivote for v in aug[col]]
        print(f"\n  ── Paso {paso}: normalizar fila {col+1}  (÷ {pivote:.4g})")
        paso += 1
        imprimir_aug(aug)

        # Eliminar en TODAS las demás filas (arriba y abajo)
        for fila in range(n):
            if fila == col:
                continue
            factor = aug[fila][col]
            if abs(factor) < 1e-14:
                continue
            aug[fila] = [aug[fila][k] - factor * aug[col][k] for k in range(n + 1)]
            signo = "+" if factor >= 0 else "-"
            print(f"\n  ── Paso {paso}: fila {fila+1}  ←  fila {fila+1}  {signo}  ({abs(factor):.4g}) × fila {col+1}")
            paso += 1
            imprimir_aug(aug)

    # Extraer soluciones
    x = [aug[i][n] for i in range(n)]

    print()
    linea("=")
    print("  SOLUCIÓN  (forma reducida escalonada):")
    linea("=")
    for i, xi in enumerate(x):
        print(f"    x{i+1} = {xi:.8f}")
    linea("=")

    print()
    print("  Verificación  Ax = b:")
    linea()
    print(f"  {'Ec.':>4}  {'Ax calculado':>18}  {'b esperado':>12}  {'Error abs.':>12}")
    linea()
    A_orig = estado["A"]
    b_orig = estado["b"]
    for i in range(n):
        ax  = sum(A_orig[i][j] * x[j] for j in range(n))
        err = abs(ax - b_orig[i])
        print(f"  Ec.{i+1}  {ax:>18.6f}  {b_orig[i]:>12.6f}  {err:>12.2e}")
    linea()
    pausa()

def menu_gauss_jordan():
    est = estado_gauss_jordan
    while True:
        print()
        titulo("  GAUSS-JORDAN  ")
        print()
        print("  Resuelve Ax = b por eliminación de Gauss-Jordan:")
        print("  convierte [A|b] en la forma identidad reducida [I|x].")
        print("  Muestra cada paso: pivoteo, normalización y eliminación.")
        print()
        print("  [1]  Ingresar / cambiar tamaño del sistema  (hasta 10×10)")
        print("  [2]  Ingresar coeficientes")
        print("  [3]  Resolver paso a paso")
        print("  [0]  Volver")
        print()
        if est["n"]:
            cargado = "✔ coeficientes cargados" if est["A"] else "✘ sin coeficientes"
            print(f"  Sistema: {est['n']}×{est['n']}   {cargado}")
        else:
            print("  Sistema: no definido aún")
        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3"])
        if   op == "0": break
        elif op == "1": menu_tamano(est)
        elif op == "2": menu_coeficientes(est)
        elif op == "3": resolver_gauss_jordan(est)

# ── Menú del 2do Parcial ──────────────────────────────────────────
def menu_segundo_parcial():
    while True:
        print()
        titulo("  📗  2do PARCIAL — Métodos Iterativos  ")
        print()
        print("  [1]  Gauss-Jacobi")
        print("  [2]  Gauss-Seidel")
        print("  [3]  Diagonal Dominante  (verificar / acomodar)")
        print("  [4]  Despejar ecuaciones  →  forma matricial")
        print("  [5]  Determinantes  (Regla de Cramer)  hasta 10×10")
        print("  [6]  Matriz Inversa  —  x = A⁻¹·b  hasta 10×10")
        print("  [7]  Gauss-Jordan  —  eliminación paso a paso")
        print("  [8]  Eliminación Gaussiana  —  triangular + sustitución regresiva")
        print("  [0]  ← Volver al menú principal")
        print()
        linea()
        op = pedir_opcion(["0", "1", "2", "3", "4", "5", "6", "7", "8"])
        if   op == "1": menu_jacobi()
        elif op == "2": menu_seidel()
        elif op == "3": menu_diagonal_dominante()
        elif op == "4": menu_despeje()
        elif op == "5": menu_determinantes()
        elif op == "6": menu_inversa()
        elif op == "7": menu_gauss_jordan()
        elif op == "8": menu_gauss_eliminacion()
        elif op == "0": break


# ══════════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL (selección de parcial)
# ══════════════════════════════════════════════════════════════════

def menu_principal():
    while True:
        print()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║       MÉTODOS NUMÉRICOS — HERRAMIENTA COMPLETA              ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print("║                                                              ║")
        print("║   [1]  📘  1er PARCIAL  (Errores, Taylor, Raíces,           ║")
        print("║                          Regresión, Lagrange...)             ║")
        print("║                                                              ║")
        print("║   [2]  📗  2do PARCIAL  (Jacobi, Seidel, Cramer,            ║")
        print("║                          Matriz Inversa, Gauss-Jordan,       ║")
        print("║                          Eliminación Gaussiana...)            ║")
        print("║                                                              ║")
        print("║   [0]  🚪  Salir                                             ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()

        op = input("  Elige parcial (0/1/2): ").strip()
        if op == "1":
            menu_primer_parcial()
        elif op == "2":
            menu_segundo_parcial()
        elif op == "0":
            print("\n  ¡Éxito en los parciales! A romperla en la UVM 🚀\n")
            sys.exit(0)
        else:
            print("  ⚠  Opción no válida. Elige 0, 1 o 2.")


# ══════════════════════════════════════════════════════════════════
#  ENTRADA
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    menu_principal()


"""
═══════════════════════════════════════════════════════════════════
        FORMULARIO DE ENTRADA (Sintaxis para la Terminal)
═══════════════════════════════════════════════════════════════════
Usa estas reglas para escribir funciones sin errores:

OPERADORES:
  Suma: +  |  Resta: -  |  Multiplicación: *  |  División: /
  Potencia: **   (x al cuadrado → x**2)

FUNCIONES ESPECIALES:
  Exponencial (e^x): exp(x)
  Logaritmo Natural: log(x)
  Raíz Cuadrada:     sqrt(x)
  Seno / Coseno:     sin(x) / cos(x)
  Tangente:          tan(x)
  Constante Pi:      pi

EJEMPLOS:
  f(x) = (x^2 - 5x + 2) / e^x   →   (x**2 - 5*x + 2) / exp(x)
  f(x) = sen(x^2) + ln(3x) - 1  →   sin(x**2) + log(3*x) - 1
═══════════════════════════════════════════════════════════════════
"""
"""
╔══════════════════════════════════════════════════════════════════╗
║        MÉTODOS NUMÉRICOS — HERRAMIENTA COMPLETA                  ║
║              1er Parcial  +  2do Parcial                         ║
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
#  CÓDIGOS DE COLOR ANSI PARA LA TERMINAL
# ══════════════════════════════════════════════════════════════════
class Color:
    VERDE = '\033[92m'     # Encabezados
    AZUL = '\033[96m'      # Resultados numéricos e iteraciones (Cyan para mayor contraste)
    ROJO = '\033[91m'      # Errores graves
    AMARILLO = '\033[93m'  # Advertencias
    MORADO = '\033[95m'    # Totales y resultados finales
    NEGRITA = '\033[1m'    # Resaltar texto
    RESET = '\033[0m'      # Restablecer color normal

# ══════════════════════════════════════════════════════════════════
#  UTILIDADES COMPARTIDAS
# ══════════════════════════════════════════════════════════════════

def imprimir_tabla(encabezados, filas):
    if TABULATE:
        # Colorear los encabezados de verde
        enc_color = [f"{Color.VERDE}{Color.NEGRITA}{h}{Color.RESET}" for h in encabezados]
        # Colorear los datos de azul
        filas_color = [[f"{Color.AZUL}{str(v)}{Color.RESET}" for v in fila] for fila in filas]
        print(tabulate(filas_color, headers=enc_color, floatfmt=".6f", tablefmt="rounded_outline"))
    else:
        ancho = 15
        sep = f"{Color.VERDE}+{('-' * ancho + '+') * len(encabezados)}{Color.RESET}"
        print(sep)
        enc_str = "|" + "".join(f"{h:^{ancho}}|" for h in encabezados)
        print(f"{Color.VERDE}{Color.NEGRITA}{enc_str}{Color.RESET}")
        print(sep)
        for fila in filas:
            fila_str = "|" + "".join(f"{str(v):^{ancho}}|" for v in fila)
            print(f"{Color.AZUL}{fila_str}{Color.RESET}")
        print(sep)

def evaluar(f_sym, valor):
    return float(f_sym.subs(x, valor))

def limpiar():
    print("\n" + "=" * 70 + "\n")

def advertencia_error():
    print(f"\n{Color.AMARILLO}{Color.NEGRITA}" + "⚠️ " * 3 + "RECORDATORIO DE ERROR " + "⚠️ " * 3)
    print("El código multiplica internamente tu número por 100 para sacar el %.")
    print("-> Si te piden error del 5%   ... ingresa: 0.05")
    print("-> Si te piden error del 1%   ... ingresa: 0.01")
    print("-> Si te piden error del 0.1% ... ingresa: 0.001")
    print("-" * 50 + f"{Color.RESET}\n")

def linea(char="─", ancho=62):
    print(char * ancho)

def titulo(texto):
    linea("═")
    espacios = (62 - len(texto)) // 2
    print(f"{Color.VERDE}{Color.NEGRITA}" + " " * espacios + texto + f"{Color.RESET}")
    linea("═")

def pausa():
    input("\n  Presiona ENTER para continuar...")

def pedir_entero(msg, minimo=1, maximo=9999):
    while True:
        try:
            v = int(input(msg))
            if minimo <= v <= maximo:
                return v
            print(f"  {Color.AMARILLO}⚠  Ingresa un número entre {minimo} y {maximo}.{Color.RESET}")
        except ValueError:
            print(f"  {Color.AMARILLO}⚠  Solo se aceptan números enteros.{Color.RESET}")

def pedir_float(msg):
    while True:
        try:
            return float(input(msg))
        except ValueError:
            print(f"  {Color.AMARILLO}⚠  Ingresa un número válido (usa punto decimal).{Color.RESET}")

def pedir_opcion(opciones):
    while True:
        op = input("  Opción: ").strip()
        if op in opciones:
            return op
        print(f"  {Color.AMARILLO}⚠  Elige: {', '.join(opciones)}{Color.RESET}")


# ══════════════════════════════════════════════════════════════════
#  1er PARCIAL — MÉTODOS Y FUNCIONES
# ══════════════════════════════════════════════════════════════════

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
    print(f"  {Color.VERDE}Error absoluto (ea)   :{Color.RESET} {Color.AZUL}{ea:.6f}{Color.RESET}")
    print(f"  {Color.VERDE}Error relativo (er)   :{Color.RESET} {Color.AZUL}{er:.6f}{Color.RESET}")
    print(f"  {Color.MORADO}{Color.NEGRITA}Error porcentual (e%) : {ep:.4f} %{Color.RESET}")

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
    print(f"\n{Color.MORADO}{Color.NEGRITA}--- RESULTADO PARA EL EXAMEN ---")
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
    print(f"FORMA EXPANDIDA: f(x) ≈ {expand(serie)}{Color.RESET}")

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
        print(f"{Color.ROJO}⚠️  f(a) y f(b) tienen el mismo signo.{Color.RESET}")
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
    print(f"\n{Color.MORADO}{Color.NEGRITA}  Raíz aproximada : {xr:.6f}{Color.RESET}")

def newton_raphson():
    limpiar()
    print("🔢 MÉTODO DE NEWTON-RAPHSON")
    expr_str = input("Ingresa f(x): ").strip()
    f_sym, df_sym = sympify(expr_str), diff(sympify(expr_str), x)
    print(f"\n  {Color.AZUL}f'(x) = {df_sym}{Color.RESET}\n")
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
        if dfxi == 0: 
            print(f"{Color.ROJO}⚠️ División por cero en la derivada.{Color.RESET}")
            break
        xi1 = xi - fxi / dfxi
        ep = abs((xi1 - xi) / xi1) * 100 if xi1 != 0 else float('inf')
        filas.append([i, f"{xi:.6f}", f"{fxi:.6f}", f"{dfxi:.6f}", f"{xi1:.6f}", f"{ep:.4f}"])
        if tol is not None and ep < tol * 100 and i > 1: break
        xi = xi1
    
    imprimir_tabla(encabezados, filas)
    print(f"\n{Color.MORADO}{Color.NEGRITA}  Raíz aproximada : {xi:.6f}{Color.RESET}")

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

    if evaluar(f_sym, xl) * evaluar(f_sym, xu) > 0: 
        print(f"{Color.ROJO}⚠️  f(a) y f(b) tienen el mismo signo.{Color.RESET}")
        return
        
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
    print(f"\n{Color.MORADO}{Color.NEGRITA}  Raíz aproximada : {xr:.6f}{Color.RESET}")

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
        if math.isnan(xi1) or math.isinf(xi1): 
            print(f"{Color.ROJO}⚠️ La función no converge.{Color.RESET}")
            break
        xi = xi1
        
    imprimir_tabla(encabezados, filas)
    print(f"\n{Color.MORADO}{Color.NEGRITA}  Raíz aproximada : {xi:.6f}{Color.RESET}")

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
            print(f"{Color.ROJO}⚠️ División por cero. El método falla.{Color.RESET}")
            break
        x_sig = x_act - (fx_act * (x_act - x_ant)) / (fx_act - fx_ant)
        ep = abs((x_sig - x_act) / x_sig) * 100 if x_sig != 0 else float('inf')
        filas.append([i, f"{x_ant:.6f}", f"{x_act:.6f}", f"{fx_ant:.6f}", f"{fx_act:.6f}", f"{x_sig:.6f}", f"{ep:.4f}"])
        if tol is not None and ep < tol * 100: break
        x_ant = x_act
        x_act = x_sig

    imprimir_tabla(encabezados, filas)
    print(f"\n{Color.MORADO}{Color.NEGRITA}  Raíz aproximada : {x_sig:.6f}{Color.RESET}")

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

    print(f"\n  #  {Color.VERDE}{'g(x)':<40} {'|g\'(x0)|':<12} Converge?{Color.RESET}")
    for idx, (nombre, g_expr) in enumerate(despejes, 1):
        try:
            val_dg = abs(float(diff(g_expr, x).subs(x, x0)))
            estado_conv = f"{Color.VERDE}SI ✅{Color.RESET}" if val_dg < 1 else f"{Color.ROJO}NO ❌{Color.RESET}"
            print(f"[{idx:>2}] {Color.AZUL}{str(simplify(g_expr)):<40} {val_dg:<12.4f}{Color.RESET} {estado_conv}")
        except: pass

def regresion_lineal_multiple():
    limpiar()
    print("📊 REGRESIÓN LINEAL MÚLTIPLE")
    print("-" * 40)
    print("1. Cargar datos de prueba por defecto")
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

    print(f"\n{Color.VERDE}--- SUMATORIAS CALCULADAS ---{Color.RESET}")
    print(f"n = {Color.AZUL}{n}{Color.RESET}")
    print(f"ΣY  = {Color.AZUL}{sum_y}{Color.RESET}")
    print(f"ΣX1 = {Color.AZUL}{sum_x1:<10}{Color.RESET} | ΣX1^2 = {Color.AZUL}{sum_x1_sq:<10}{Color.RESET} | ΣX1Y = {Color.AZUL}{sum_x1_y}{Color.RESET}")
    print(f"ΣX2 = {Color.AZUL}{sum_x2:<10}{Color.RESET} | ΣX2^2 = {Color.AZUL}{sum_x2_sq:<10}{Color.RESET} | ΣX2Y = {Color.AZUL}{sum_x2_y}{Color.RESET}")
    print(f"ΣX1X2 = {Color.AZUL}{sum_x1_x2}{Color.RESET}")

    if vars_indep == 3:
        sum_x3 = sum(x3); sum_x3_sq = sum(i**2 for i in x3)
        sum_x1_x3 = sum(x1[i]*x3[i] for i in range(n)); sum_x2_x3 = sum(x2[i]*x3[i] for i in range(n))
        sum_x3_y = sum(x3[i]*y[i] for i in range(n))
        print(f"ΣX3 = {Color.AZUL}{sum_x3:<10}{Color.RESET} | ΣX3^2 = {Color.AZUL}{sum_x3_sq:<10}{Color.RESET} | ΣX3Y = {Color.AZUL}{sum_x3_y}{Color.RESET}")
        print(f"ΣX1X3 = {Color.AZUL}{sum_x1_x3:<10}{Color.RESET} | ΣX2X3 = {Color.AZUL}{sum_x2_x3}{Color.RESET}")

    print(f"\n{Color.VERDE}--- SISTEMA SUSTITUIDO ---{Color.RESET}")
    if vars_indep == 2:
        print(f"{n}a + {sum_x1}b1 + {sum_x2}b2 = {sum_y}")
        print(f"{sum_x1}a + {sum_x1_sq}b1 + {sum_x1_x2}b2 = {sum_x1_y}")
        print(f"{sum_x2}a + {sum_x1_x2}b1 + {sum_x2_sq}b2 = {sum_x2_y}")
        A = Matrix([[n, sum_x1, sum_x2], [sum_x1, sum_x1_sq, sum_x1_x2], [sum_x2, sum_x1_x2, sum_x2_sq]])
        B = Matrix([sum_y, sum_x1_y, sum_x2_y])
        res = A.LUsolve(B)
        a, b1, b2 = float(res[0]), float(res[1]), float(res[2])
        print(f"\n{Color.MORADO}{Color.NEGRITA}Ecuación: y = {a:.4f} {'+' if b1>=0 else '-'} {abs(b1):.4f}x1 {'+' if b2>=0 else '-'} {abs(b2):.4f}x2{Color.RESET}")
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
        print(f"\n{Color.MORADO}{Color.NEGRITA}Ecuación: y = {a:.4f} {'+' if b1>=0 else '-'} {abs(b1):.4f}x1 {'+' if b2>=0 else '-'} {abs(b2):.4f}x2 {'+' if b3>=0 else '-'} {abs(b3):.4f}x3{Color.RESET}")

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

    print(f"\n{Color.VERDE}--- 1. ECUACIÓN ARMADA (Sustitución Directa) ---{Color.RESET}")
    print(f"{Color.AZUL}f_{N}(x) = " + "  +  ".join(terminos_str) + f"{Color.RESET}")
    polinomio_expandido = expand(polinomio)
    
    print(f"\n{Color.MORADO}{Color.NEGRITA}--- 2. ECUACIÓN FINAL SIMPLIFICADA ---")
    print(f"f_{N}(x) = {polinomio_expandido}{Color.RESET}")

    if xp_str:
        xp = float(xp_str)
        resultado = polinomio_expandido.subs(x, xp)
        print(f"\n{Color.MORADO}{Color.NEGRITA}--- 3. EVALUACIÓN EN x = {xp} ---")
        print(f"f_{N}({xp}) = {resultado:.4f}{Color.RESET}")

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
                print(f"\n{Color.ROJO}⚠️  Error: {e}{Color.RESET}")
                print("Revisa los datos o funciones ingresadas.")
            input("\n[Presiona Enter para volver al menú]")
        else:
            print("Opción no válida.")

# ══════════════════════════════════════════════════════════════════
#  2do PARCIAL — MÉTODOS ITERATIVOS (Álgebra Lineal)
# ══════════════════════════════════════════════════════════════════

estado_jacobi = {"n": None, "A": None, "b": None, "x0": None, "tol": 0.001, "max_iter": 100, "resultado": None}
estado_seidel = {"n": None, "A": None, "b": None, "x0": None, "tol": 0.001, "max_iter": 100, "resultado": None}
estado_diagonal     = {"n": None, "A": None, "b": None}
estado_cramer       = {"n": None, "A": None, "b": None}
estado_inversa      = {"n": None, "A": None, "b": None}
estado_gauss_jordan = {"n": None, "A": None, "b": None}
estado_gauss_elim   = {"n": None, "A": None, "b": None}

def imprimir_matriz(A, b, n):
    print("  Matriz [A | b]:")
    linea()
    enc = "       "
    for j in range(n):
        enc += f"    x{j+1}  "
    enc += "  |      b"
    print(f"{Color.VERDE}{enc}{Color.RESET}")
    linea()
    for i in range(n):
        fila = f"  {Color.VERDE}Ec.{i+1}{Color.RESET}  {Color.AZUL}"
        for v in A[i]:
            fila += f"{v:7.3f} "
        fila += f"{Color.RESET} {Color.VERDE}|{Color.RESET} {Color.AZUL}{b[i]:7.3f}{Color.RESET}"
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
        print(f"\n  {Color.VERDE}✔  Sistema configurado: {n_nuevo}×{n_nuevo}{Color.RESET}")
    else:
        print(f"\n  El sistema ya era {n_nuevo}×{n_nuevo}, sin cambios.")
    pausa()

def menu_coeficientes(estado):
    print()
    titulo("  INGRESAR COEFICIENTES  ")
    if estado["n"] is None:
        print(f"\n  {Color.AMARILLO}⚠  Primero define el tamaño (Opción 1).{Color.RESET}")
        pausa(); return
    n = estado["n"]
    A, b = [], []
    for i in range(n):
        while True:
            linea("·")
            print(f"  Ecuación {i+1}:")
            try:
                raw = input(f"    Coeficientes (a1 a2 ... a{n}): ").split()
                if len(raw) != n:
                    print(f"  {Color.AMARILLO}⚠  Necesitas exactamente {n} valores.{Color.RESET}")
                    continue
                fila = [float(v) for v in raw]
                bi   = pedir_float(f"    Término independiente b{i+1}: ")
                A.append(fila)
                b.append(bi)
                break
            except ValueError:
                print(f"  {Color.AMARILLO}⚠  Ingresa solo números.{Color.RESET}")
    estado["A"] = A
    estado["b"] = b
    if "resultado" in estado:
        estado["resultado"] = None
    print()
    imprimir_matriz(A, b, n)
    print(f"\n  {Color.VERDE}✔  Coeficientes guardados.{Color.RESET}")
    pausa()

def menu_x0(estado):
    print()
    titulo("  VECTOR INICIAL  x0  ")
    if estado["n"] is None:
        print(f"\n  {Color.AMARILLO}⚠  Primero define el tamaño (Opción 1).{Color.RESET}")
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
        print(f"\n  {Color.VERDE}✔  x0 restablecido a ceros.{Color.RESET}")
    elif op == "2":
        print(f"\n  Ingresa {n} valores separados por espacios:")
        while True:
            try:
                raw = input(f"    x0 (x1 x2 ... x{n}): ").split()
                if len(raw) != n:
                    print(f"  {Color.AMARILLO}⚠  Necesitas exactamente {n} valores.{Color.RESET}")
                    continue
                estado["x0"]        = [float(v) for v in raw]
                estado["resultado"] = None
                print(f"\n  {Color.VERDE}✔  x0 guardado.{Color.RESET}")
                break
            except ValueError:
                print(f"  {Color.AMARILLO}⚠  Ingresa solo números.{Color.RESET}")
    pausa()

def menu_config(estado):
    print()
    titulo("  CONFIGURACIÓN  ")
    estado["tol"]       = pedir_float("  Nueva tolerancia (ej: 0.001): ")
    estado["max_iter"]  = pedir_entero("  Iteraciones máximas (ej: 100): ", 1, 10000)
    estado["resultado"] = None
    print(f"\n  {Color.VERDE}✔  Configuración guardada.{Color.RESET}")
    pausa()

def mostrar_tabla(hist, n, inicio, fin):
    tiene_ep = "ep" in hist[0] if hist else False
    print()
    linea()
    enc = f"  {Color.VERDE}{'Iter':>5} │"
    for i in range(n):
        enc += f"{'x'+str(i+1):>13}"
    if tiene_ep:
        enc += "  │"
        for i in range(n):
            enc += f"{'Ep%x'+str(i+1):>10}"
    enc += f"  │  {'Err.abs.máx':>11}{Color.RESET}"
    print(enc)
    linea()
    for e in hist[inicio:fin]:
        fila = f"  {Color.VERDE}{e['k']:>5} │{Color.AZUL}"
        for xi in e["x"]:
            fila += f"{xi:>13.6f}"
        if tiene_ep:
            fila += f"{Color.RESET}  {Color.VERDE}│{Color.AZUL}"
            for ep_i in e["ep"]:
                fila += f"{ep_i:>9.4f}%"
        fila += f"{Color.RESET}  {Color.VERDE}│{Color.AZUL}  {e['error']:>11.4e}{Color.RESET}"
        print(fila)
    linea()

def mostrar_solucion(x, n, conv, iters):
    print()
    linea()
    if conv:
        print(f"  {Color.VERDE}✔  Convergió en {iters} iteración(es){Color.RESET}")
    else:
        print(f"  {Color.ROJO}✘  No convergió ({iters} iteraciones realizadas){Color.RESET}")
    linea()
    for i, xi in enumerate(x):
        print(f"    {Color.MORADO}{Color.NEGRITA}x{i+1} = {xi:.8f}{Color.RESET}")
    linea()

def menu_resultados(estado):
    if estado["resultado"] is None:
        print(f"\n  {Color.AMARILLO}⚠  Primero resuelve el sistema (Opción 4).{Color.RESET}")
        pausa(); return
    res = estado["resultado"]
    n, hist, x, conv = estado["n"], res["historial"], res["x"], res["convergio"]

    while True:
        print()
        estado_txt = f"{Color.VERDE}✔ Convergió en {len(hist)} iter.{Color.RESET}" if conv else f"{Color.ROJO}✘ No convergió ({len(hist)} iter.){Color.RESET}"
        print(f"  Estado : {estado_txt}")
        print("  [1]  Tabla completa de iteraciones\n  [2]  Solo la solución final\n  [3]  Iteraciones por rango\n  [0]  Volver\n")
        op = pedir_opcion(["0", "1", "2", "3"])
        if op == "0": break
        elif op == "1": mostrar_tabla(hist, n, 0, len(hist))
        elif op == "2": mostrar_solucion(x, n, conv, len(hist))
        elif op == "3":
            total = len(hist)
            desde = pedir_entero("  Desde iteración: ", 1, total)
            hasta = pedir_entero("  Hasta iteración: ", desde, total)
            mostrar_tabla(hist, n, desde - 1, hasta)
        pausa()

def menu_verificacion(estado):
    print()
    titulo("  VERIFICACIÓN  Ax ≈ b  ")
    if estado["resultado"] is None:
        print(f"\n  {Color.AMARILLO}⚠  Primero resuelve el sistema.{Color.RESET}")
        pausa(); return
    n, A, b = estado["n"], estado["A"], estado["b"]
    x = estado["resultado"]["x"]
    print()
    linea()
    print(f"  {Color.VERDE}{'Ec.':>4}  {'Ax calculado':>18}  {'b esperado':>12}  {'Error abs.':>12}{Color.RESET}")
    linea()
    for i in range(n):
        ax  = sum(A[i][j] * x[j] for j in range(n))
        err = abs(ax - b[i])
        err_color = Color.VERDE if err < 1e-4 else Color.ROJO
        print(f"  {Color.VERDE}Ec.{i+1}{Color.RESET}  {Color.AZUL}{ax:>18.6f}  {b[i]:>12.6f}{Color.RESET}  {err_color}{err:>12.2e}{Color.RESET}")
    linea()
    pausa()

def resolver_iterativo(estado, metodo="jacobi"):
    print()
    titulo(f"  RESOLVIENDO — {metodo.upper()}  ")
    if estado["n"] is None or estado["A"] is None:
        print(f"\n  {Color.AMARILLO}⚠  Faltan configurar datos del sistema.{Color.RESET}"); pausa(); return
    
    n, A, b = estado["n"], [fila[:] for fila in estado["A"]], estado["b"][:]
    tol, max_iter = estado["tol"], estado["max_iter"]
    
    for i in range(n):
        if abs(A[i][i]) < 1e-14:
            print(f"\n  {Color.ROJO}✘  El elemento A[{i+1}][{i+1}] es cero.{Color.RESET}"); pausa(); return

    x = estado["x0"][:] if estado["x0"] else [0.0] * n
    historial, convergio = [], False

    for k in range(1, max_iter + 1):
        x_ant = x[:]
        x_nuevo = [0.0] * n if metodo == "jacobi" else x
        for i in range(n):
            s = sum(A[i][j] * (x_ant[j] if metodo == "jacobi" else x[j]) for j in range(n) if j != i)
            x_nuevo[i] = (b[i] - s) / A[i][i]
            
        error = max(abs(x_nuevo[i] - x_ant[i]) for i in range(n))
        ep = [abs((x_nuevo[i] - x_ant[i]) / x_nuevo[i]) * 100 if abs(x_nuevo[i]) > 1e-14 else 0.0 for i in range(n)]
        
        if metodo == "jacobi": x = x_nuevo[:]
        historial.append({"k": k, "x": x[:], "error": error, "ep": ep})
        
        if error <= tol:
            convergio = True; break

    estado["resultado"] = {"x": x, "historial": historial, "convergio": convergio}
    if convergio: print(f"\n  {Color.VERDE}✔  Convergió en {len(historial)} iteración(es).{Color.RESET}")
    else: print(f"\n  {Color.ROJO}✘  No convergió en {max_iter} iteraciones.{Color.RESET}")
    pausa()

def resolver_gauss_eliminacion(estado):
    print()
    titulo("  RESOLVIENDO — ELIMINACIÓN GAUSSIANA  ")
    if estado["n"] is None or estado["A"] is None: return

    n = estado["n"]
    aug = [estado["A"][i][:] + [estado["b"][i]] for i in range(n)]

    def imprimir_aug(mat):
        linea("·")
        for i in range(n):
            fila = f"  {Color.VERDE}Ec.{i+1:<3}{Color.RESET} " + "".join(f"{Color.AZUL}{mat[i][j]:>10.4g}{Color.RESET}" for j in range(n))
            print(fila + f"  {Color.VERDE}|{Color.RESET} {Color.AZUL}{mat[i][n]:>10.4g}{Color.RESET}")
        linea("·")

    paso = 1
    for col in range(n):
        max_fila = col
        for fila in range(col + 1, n):
            if abs(aug[fila][col]) > abs(aug[max_fila][col]): max_fila = fila
        if max_fila != col:
            aug[col], aug[max_fila] = aug[max_fila], aug[col]
        pivote = aug[col][col]
        for fila in range(col + 1, n):
            factor = aug[fila][col] / pivote
            if abs(factor) > 1e-14:
                aug[fila] = [aug[fila][k] - factor * aug[col][k] for k in range(n + 1)]

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (aug[i][n] - s) / aug[i][i]

    print(f"\n{Color.MORADO}{Color.NEGRITA}  SOLUCIÓN FINAL:{Color.RESET}")
    linea("=")
    for i, xi in enumerate(x):
        print(f"    {Color.MORADO}{Color.NEGRITA}x{i+1} = {xi:.8f}{Color.RESET}")
    linea("=")
    estado["resultado"] = {"x": x}
    pausa()

def menu_iterativo(estado, nombre, metodo):
    while True:
        print()
        titulo(f"  {nombre}  ")
        print("\n  [1] Tamaño\n  [2] Coeficientes\n  [3] Vector inicial x0\n  [4] Configurar tol/iter\n  [5] Resolver\n  [6] Ver resultados\n  [7] Verificación Ax ≈ b\n  [0] Volver\n")
        op = pedir_opcion(["0", "1", "2", "3", "4", "5", "6", "7"])
        if op == "0": break
        elif op == "1": menu_tamano(estado)
        elif op == "2": menu_coeficientes(estado)
        elif op == "3": menu_x0(estado)
        elif op == "4": menu_config(estado)
        elif op == "5": resolver_iterativo(estado, metodo)
        elif op == "6": menu_resultados(estado)
        elif op == "7": menu_verificacion(estado)

def menu_segundo_parcial():
    while True:
        print()
        titulo("  📗  2do PARCIAL — Métodos Numéricos  ")
        print("\n  [1]  Gauss-Jacobi\n  [2]  Gauss-Seidel\n  [8]  Eliminación Gaussiana\n  [0]  ← Volver al menú principal\n")
        op = pedir_opcion(["0", "1", "2", "8"])
        if op == "1": menu_iterativo(estado_jacobi, "GAUSS-JACOBI", "jacobi")
        elif op == "2": menu_iterativo(estado_seidel, "GAUSS-SEIDEL", "seidel")
        elif op == "8": 
            menu_tamano(estado_gauss_elim); menu_coeficientes(estado_gauss_elim); resolver_gauss_eliminacion(estado_gauss_elim)
        elif op == "0": break

def menu_principal():
    while True:
        print()
        print(f"{Color.VERDE}╔══════════════════════════════════════════════════════════════╗")
        print("║       MÉTODOS NUMÉRICOS — HERRAMIENTA COMPLETA              ║")
        print("╠══════════════════════════════════════════════════════════════╣")
        print(f"║   {Color.AZUL}[1]{Color.VERDE}  📘  1er PARCIAL  (Raíces, Regresión, Lagrange...)    ║")
        print(f"║   {Color.AZUL}[2]{Color.VERDE}  📗  2do PARCIAL  (Jacobi, Seidel, Gauss...)          ║")
        print(f"║   {Color.AZUL}[0]{Color.VERDE}  🚪  Salir                                            ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Color.RESET}\n")

        op = input("  Elige parcial (0/1/2): ").strip()
        if op == "1": menu_primer_parcial()
        elif op == "2": menu_segundo_parcial()
        elif op == "0":
            print(f"\n  {Color.MORADO}{Color.NEGRITA}¡Éxito en los parciales! A romperla en la UVM 🚀{Color.RESET}\n")
            sys.exit(0)
        else: print(f"  {Color.AMARILLO}⚠  Opción no válida. Elige 0, 1 o 2.{Color.RESET}")

if __name__ == "__main__":
    menu_principal()
import math
from sympy import symbols, sympify

# Definir la variable simbólica para que entienda las x
x = symbols('x')

def evaluar(f_sym, valor):
    """Evalúa la función matemática en un punto dado."""
    return float(f_sym.subs(x, valor).evalf())

def calc_trapecio(f_sym, a, b, n):
    """Método de Integración del Trapecio (Múltiple)"""
    h = (b - a) / n
    suma = evaluar(f_sym, a) + evaluar(f_sym, b)
    for i in range(1, n):
        suma += 2 * evaluar(f_sym, a + i * h)
    return (b - a) * suma / (2 * n)

def calc_simpson13(f_sym, a, b, n):
    """Método de Integración de Simpson 1/3 (Múltiple)"""
    if n % 2 != 0:
        return "Error: n debe ser número par."
    h = (b - a) / n
    suma = evaluar(f_sym, a) + evaluar(f_sym, b)
    for i in range(1, n):
        x_i = a + i * h
        if i % 2 == 0:
            suma += 2 * evaluar(f_sym, x_i)
        else:
            suma += 4 * evaluar(f_sym, x_i)
    return (b - a) * suma / (3 * n)

def calc_simpson38(f_sym, a, b, n):
    """Método de Integración de Simpson 3/8"""
    if n % 3 != 0:
        return "Error: n debe ser múltiplo de 3."
    h = (b - a) / n
    suma = evaluar(f_sym, a) + evaluar(f_sym, b)
    for i in range(1, n):
        x_i = a + i * h
        if i % 3 == 0:
            suma += 2 * evaluar(f_sym, x_i)
        else:
            suma += 3 * evaluar(f_sym, x_i)
    return (3 * h / 8) * suma

def calc_romberg(f_sym, a, b, niveles):
    """Método de Integración de Romberg"""
    I = [[0.0] * niveles for _ in range(niveles)]
    for k in range(niveles):
        n = 2**k
        I[k][0] = calc_trapecio(f_sym, a, b, n)
        for j in range(1, k + 1):
            I[k][j] = (4**j * I[k][j-1] - I[k-1][j-1]) / (4**j - 1)
    return I

# ==========================================
# ZONA DE EJECUCIÓN (AQUÍ CORRE TU TAREA)
# ==========================================
if __name__ == "__main__":
    print("="*50)
    print("      RESOLVEDOR DE TAREA 7 - INTEGRACIÓN")
    print("="*50)
    
    # 1. Pedir la función y límites
    expr_str = input("\nIngresa f(x) [ej. 8 + 4*cos(x)]: ").strip()
    f_sym = sympify(expr_str)
    
    # Usamos sympify para que entienda si escribes "pi/2"
    a = float(sympify(input("Límite inferior a: ")).evalf())
    b = float(sympify(input("Límite superior b: ")).evalf())
    
    # 2. Correr Trapecio
    print("\n--- 1. MÉTODO DEL TRAPECIO ---")
    n_trap = int(input("  Ingresa n para el Trapecio: "))
    print(f"  Resultado: {calc_trapecio(f_sym, a, b, n_trap):.6f}")

    # 3. Correr Simpson 1/3
    print("\n--- 2. MÉTODO DE SIMPSON 1/3 ---")
    n_simp = int(input("  Ingresa n para Simpson 1/3 (debe ser par): "))
    res_simp = calc_simpson13(f_sym, a, b, n_simp)
    if isinstance(res_simp, float):
        print(f"  Resultado: {res_simp:.6f}")
    else:
        print(f"  {res_simp}")

    # 4. Correr Simpson 3/8
    print("\n--- 3. MÉTODO DE SIMPSON 3/8 ---")
    n_simp38 = int(input("  Ingresa n para Simpson 3/8 (múltiplo de 3): "))
    res_simp38 = calc_simpson38(f_sym, a, b, n_simp38)
    if isinstance(res_simp38, float):
        print(f"  Resultado: {res_simp38:.6f}")
    else:
        print(f"  {res_simp38}")

    # 5. Correr Romberg
    print("\n--- 4. INTEGRACIÓN DE ROMBERG ---")
    niveles = int(input("  Ingresa cuántos niveles para Romberg: "))
    matriz = calc_romberg(f_sym, a, b, niveles)
    for i, fila in enumerate(matriz):
        valores = [f"{val:.6f}" for val in fila[:i+1]]
        print(f"  Nivel {i+1}: " + " | ".join(valores))
    print("="*50)
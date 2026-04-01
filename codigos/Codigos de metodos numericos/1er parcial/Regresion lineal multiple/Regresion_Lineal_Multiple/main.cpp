// ==========================================
// 1. LAS HERRAMIENTAS (LIBRERÍAS)
// ==========================================
#include <iostream>  // Nos permite usar 'cout' (imprimir en pantalla) y 'cin' (leer teclado).
#include <vector>    // Nos deja usar listas dinámicas que saben su propio tamaño.
#include <cmath>     // Trae matemáticas avanzadas: pow() para potencias y abs() para valor absoluto.
#include <iomanip>   // Nos permite darle formato al texto (ej. fijar 4 decimales).

using namespace std; // Nos ahorra escribir "std::" antes de cada cout, cin o vector.

// ==========================================
// 2. EL MOTOR MATEMÁTICO (GAUSS-JORDAN)
// Esta función reemplaza a 'numpy' de Python. Toma el sistema de ecuaciones y despeja las variables.
// ==========================================
vector<double> resolverSistema(vector<vector<double>> A, vector<double> B) {
    int n = A.size(); // Mide cuántas ecuaciones son (3 para x1/x2, o 4 si usas x3).

    // Este ciclo recorre la diagonal principal de la matriz para convertirla en unos (1).
    for (int i = 0; i < n; i++) {

        // PIVOTEO: Busca el número más grande en la columna y lo sube.
        // Esto evita errores matemáticos si hay divisiones entre números muy pequeños.
        double maxEl = abs(A[i][i]);
        int maxRow = i;
        for (int k = i + 1; k < n; k++) {
            if (abs(A[k][i]) > maxEl) {
                maxEl = abs(A[k][i]);
                maxRow = k;
            }
        }
        swap(A[maxRow], A[i]); // Intercambia las filas en la matriz A
        swap(B[maxRow], B[i]); // Hace lo mismo en el vector de resultados B

        // Divide toda la fila entre el "pivote" para que el número de la diagonal sea exactamente 1.
        double pivote = A[i][i];
        for (int j = i; j < n; j++) A[i][j] /= pivote;
        B[i] /= pivote;

        // ELIMINACIÓN: Convierte en ceros (0) todos los números arriba y abajo de nuestro nuevo "1".
        for (int k = 0; k < n; k++) {
            if (i != k) {
                double factor = A[k][i];
                for (int j = i; j < n; j++) A[k][j] -= factor * A[i][j];
                B[k] -= factor * B[i];
            }
        }
    }
    return B; // B ahora contiene las respuestas finales (a, b1, b2, etc.)
}

// ==========================================
// 3. EL INICIO DEL PROGRAMA Y LOS DATOS
// ==========================================
int main() {
    // Aquí declaras tus listas de datos. Usamos 'double' porque tienen decimales.
    vector<double> y  = {0.231, 0.107, 0.053, 0.129, 0.069, 0.030, 1.005, 0.559, 0.321, 2.948, 1.633, 0.934};
    vector<double> x1 = {740, 740, 740, 805, 805, 805, 980, 980, 980, 1235, 1235, 1235};
    vector<double> x2 = {1.10, 0.62, 0.31, 1.10, 0.62, 0.31, 1.10, 0.62, 0.31, 1.10, 0.62, 0.31};

    // Lista para x3 (solo se usará si eliges la opción 2 en el menú).
    vector<double> x3 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};

    // La computadora cuenta los elementos de 'y' automáticamente.
    int n = y.size();
    int opcion;

    // Imprime el menú de opciones.
    cout << "=== CALCULADORA DE REGRESION LINEAL MULTIPLE ===" << endl;
    cout << "Selecciona la cantidad de variables independientes:" << endl;
    cout << "1. Dos variables (x1, x2)" << endl;
    cout << "2. Tres variables (x1, x2, x3)" << endl;
    cout << "Opcion: ";
    cin >> opcion; // Espera a que teclees 1 o 2 y lo guarda.

    cout << fixed << setprecision(4); // Configura la consola para mostrar siempre 4 decimales.
    cout << "\n";

    // ==========================================
    // 4. LA LÓGICA PRINCIPAL (EL SWITCH)
    // ==========================================
    switch (opcion) {
        case 1: { // RUTA PARA 2 VARIABLES (x1, x2)

            // Creamos "cajas" vacías (en 0) donde iremos echando la suma de los valores.
            double sum_y = 0, sum_x1 = 0, sum_x2 = 0;
            double sum_x1_sq = 0, sum_x2_sq = 0, sum_x1_x2 = 0;
            double sum_x1_y = 0, sum_x2_y = 0;

            // Este ciclo recorre tu tabla fila por fila (desde la 0 hasta la 11 en tu caso).
            for (int i = 0; i < n; i++) {
                sum_y += y[i];                 // Suma directa de 'y'
                sum_x1 += x1[i];               // Suma directa de 'x1'
                sum_x2 += x2[i];               // Suma directa de 'x2'
                sum_x1_sq += pow(x1[i], 2);    // Eleva x1 al cuadrado y lo suma
                sum_x2_sq += pow(x2[i], 2);    // Eleva x2 al cuadrado y lo suma
                sum_x1_x2 += x1[i] * x2[i];    // Multiplica x1 por x2 y lo suma
                sum_x1_y += x1[i] * y[i];      // Multiplica x1 por y y lo suma
                sum_x2_y += x2[i] * y[i];      // Multiplica x2 por y y lo suma
            }

            // Muestra en pantalla las fórmulas base usando puro texto.
            cout << "--- FORMULAS DEL SISTEMA ---" << endl;
            cout << "1) an   + b1*Ex1  + b2*Ex2  = Ey" << endl;
            cout << "2) a*Ex1 + b1*Ex1^2+ b2*Ex1x2= Ex1y" << endl;
            cout << "3) a*Ex2 + b1*Ex1x2+ b2*Ex2^2= Ex2y\n" << endl;

            // Muestra las cajas que llenamos en el ciclo 'for'.
            cout << "--- SUMATORIAS CALCULADAS ---" << endl;
            cout << "n      = " << n << endl;
            cout << "Ey     = " << sum_y << endl;
            cout << "Ex1    = " << sum_x1 << endl;
            // ... (resto de las impresiones de sumatorias)
            cout << "Ex2y   = " << sum_x2_y << "\n" << endl;

            // ==========================================
            // 5. ENSAMBLAJE Y SOLUCIÓN MATRICIAL
            // ==========================================
            cout << "--- SISTEMA SUSTITUIDO ---" << endl;
            cout << n << "a + " << sum_x1 << "b1 + " << sum_x2 << "b2 = " << sum_y << endl;
            cout << sum_x1 << "a + " << sum_x1_sq << "b1 + " << sum_x1_x2 << "b2 = " << sum_x1_y << endl;
            cout << sum_x2 << "a + " << sum_x1_x2 << "b1 + " << sum_x2_sq << "b2 = " << sum_x2_y << "\n" << endl;

            // Se construye la matriz A (Lado izquierdo del igual). El orden es idéntico a las fórmulas.
            vector<vector<double>> A = {
                {(double)n, sum_x1, sum_x2},
                {sum_x1, sum_x1_sq, sum_x1_x2},
                {sum_x2, sum_x1_x2, sum_x2_sq}
            };

            // Se construye el vector B (Lo que está a la derecha del igual).
            vector<double> B = {sum_y, sum_x1_y, sum_x2_y};

            // Llamamos a nuestro motor matemático para que resuelva A y B.
            vector<double> res = resolverSistema(A, B);

            // ==========================================
            // 6. RESULTADOS Y TOQUE FINAL (FORMATO)
            // ==========================================
            cout << "--- RESULTADOS ---" << endl;
            cout << "a  = " << res[0] << endl; // res[0] es la primera respuesta (a)
            cout << "b1 = " << res[1] << endl; // res[1] es la segunda respuesta (b1)
            cout << "b2 = " << res[2] << "\n" << endl;

            // Imprimimos la ecuación final.
            // La parte '(res[1] >= 0 ? " + " : " - ")' verifica si b1 es positivo para poner "+" o "-"
            // La parte 'abs()' quita el signo del número para no imprimir cosas como "+ -3".
            cout << "y = " << res[0]
                 << (res[1] >= 0 ? " + " : " - ") << abs(res[1]) << "x1"
                 << (res[2] >= 0 ? " + " : " - ") << abs(res[2]) << "x2" << endl;
            break;
        }

        case 2: { // RUTA PARA 3 VARIABLES (x1, x2, x3)

            // Creamos las cajas para las 14 sumatorias necesarias
            double sum_y = 0, sum_x1 = 0, sum_x2 = 0, sum_x3 = 0;
            double sum_x1_sq = 0, sum_x2_sq = 0, sum_x3_sq = 0;
            double sum_x1_x2 = 0, sum_x1_x3 = 0, sum_x2_x3 = 0;
            double sum_x1_y = 0, sum_x2_y = 0, sum_x3_y = 0;

            // Llenamos las cajas recorriendo las listas
            for (int i = 0; i < n; i++) {
                sum_y += y[i];
                sum_x1 += x1[i]; sum_x2 += x2[i]; sum_x3 += x3[i];
                sum_x1_sq += pow(x1[i], 2); sum_x2_sq += pow(x2[i], 2); sum_x3_sq += pow(x3[i], 2);
                sum_x1_x2 += x1[i] * x2[i]; sum_x1_x3 += x1[i] * x3[i]; sum_x2_x3 += x2[i] * x3[i];
                sum_x1_y += x1[i] * y[i]; sum_x2_y += x2[i] * y[i]; sum_x3_y += x3[i] * y[i];
            }

            // 1. IMPRESIÓN DE FÓRMULAS BASE (Ahora son 4)
            cout << "--- FORMULAS DEL SISTEMA ---" << endl;
            cout << "1) an    + b1*Ex1   + b2*Ex2   + b3*Ex3   = Ey" << endl;
            cout << "2) a*Ex1 + b1*Ex1^2 + b2*Ex1x2 + b3*Ex1x3 = Ex1y" << endl;
            cout << "3) a*Ex2 + b1*Ex1x2 + b2*Ex2^2 + b3*Ex2x3 = Ex2y" << endl;
            cout << "4) a*Ex3 + b1*Ex1x3 + b2*Ex2x3 + b3*Ex3^2 = Ex3y\n" << endl;

            // 2. IMPRESIÓN DE TODAS LAS SUMATORIAS CALCULADAS
            cout << "--- SUMATORIAS CALCULADAS ---" << endl;
            cout << "n      = " << n << endl;
            cout << "Ey     = " << sum_y << endl;
            cout << "Ex1    = " << sum_x1 << endl;
            cout << "Ex2    = " << sum_x2 << endl;
            cout << "Ex3    = " << sum_x3 << endl;
            cout << "Ex1^2  = " << sum_x1_sq << endl;
            cout << "Ex2^2  = " << sum_x2_sq << endl;
            cout << "Ex3^2  = " << sum_x3_sq << endl;
            cout << "Ex1x2  = " << sum_x1_x2 << endl;
            cout << "Ex1x3  = " << sum_x1_x3 << endl;
            cout << "Ex2x3  = " << sum_x2_x3 << endl;
            cout << "Ex1y   = " << sum_x1_y << endl;
            cout << "Ex2y   = " << sum_x2_y << endl;
            cout << "Ex3y   = " << sum_x3_y << "\n" << endl;

            // 3. IMPRESIÓN DEL SISTEMA SUSTITUIDO
            cout << "--- SISTEMA SUSTITUIDO ---" << endl;
            cout << n << "a + " << sum_x1 << "b1 + " << sum_x2 << "b2 + " << sum_x3 << "b3 = " << sum_y << endl;
            cout << sum_x1 << "a + " << sum_x1_sq << "b1 + " << sum_x1_x2 << "b2 + " << sum_x1_x3 << "b3 = " << sum_x1_y << endl;
            cout << sum_x2 << "a + " << sum_x1_x2 << "b1 + " << sum_x2_sq << "b2 + " << sum_x2_x3 << "b3 = " << sum_x2_y << endl;
            cout << sum_x3 << "a + " << sum_x1_x3 << "b1 + " << sum_x2_x3 << "b2 + " << sum_x3_sq << "b3 = " << sum_x3_y << "\n" << endl;

            // 4. CREACIÓN DE MATRIZ Y SOLUCIÓN
            vector<vector<double>> A = {
                {(double)n, sum_x1, sum_x2, sum_x3},
                {sum_x1, sum_x1_sq, sum_x1_x2, sum_x1_x3},
                {sum_x2, sum_x1_x2, sum_x2_sq, sum_x2_x3},
                {sum_x3, sum_x1_x3, sum_x2_x3, sum_x3_sq}
            };

            vector<double> B = {sum_y, sum_x1_y, sum_x2_y, sum_x3_y};

            // Llamamos al motor matemático (la función de arriba)
            vector<double> res = resolverSistema(A, B);

            // 5. RESULTADOS FINALES
            cout << "--- RESULTADOS ---" << endl;
            cout << "a  = " << res[0] << endl;
            cout << "b1 = " << res[1] << endl;
            cout << "b2 = " << res[2] << endl;
            cout << "b3 = " << res[3] << "\n" << endl;

            // Imprimimos la ecuación final con sus signos
            cout << "y = " << res[0]
                 << (res[1] >= 0 ? " + " : " - ") << abs(res[1]) << "x1"
                 << (res[2] >= 0 ? " + " : " - ") << abs(res[2]) << "x2"
                 << (res[3] >= 0 ? " + " : " - ") << abs(res[3]) << "x3" << endl;
            break;
        }

        default:
            // Por si el usuario teclea un 3 o un número inválido
            cout << "Opcion no valida. Ejecuta el programa de nuevo." << endl;
            break;
    }

    return 0; // Termina el programa exitosamente
}

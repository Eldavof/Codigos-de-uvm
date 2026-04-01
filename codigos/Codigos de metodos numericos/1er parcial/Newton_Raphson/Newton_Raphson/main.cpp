#include <iostream>
#include <iomanip>
#include <cmath>
#define PRECICION 6
using namespace std;

double f_Xi (double x);
double f_der_Xi (double x);

int main()
{
    cout << setprecision(PRECICION) << fixed;
    cout << "Metodo Newton Raphson" << endl;

    double Xi = 0, Xi_1 = 0, tolerancia = 0;
    double error_aprox= 100.0;
    int iteraciones = 0;

    cout << "ingresar el valor de Xi: "; cin >> Xi;
    cout << "ingresar la tolerancia: "; cin >> tolerancia;

    cout << "\nIteracion\tXi\t\tf(Xi)\t\tf'(Xi)\t\tXi+1\t\tError %" << endl;

    do{

        iteraciones++;
        double derivada = f_der_Xi(Xi);

        if(derivada == 0) {


            cout << "Error el resultado de tu funcion derivada fue 0 por ende no se puede calcular Xi+1";
            cout << "\nPorfavor ingresa un valor inicial diferente";
            return 12;
        }

        Xi_1 = Xi - (f_Xi(Xi) / derivada);

        if (Xi_1 != 0.0){

            error_aprox = abs((Xi_1 - Xi) / Xi_1) * 100.0;
        }

        cout << iteraciones << "\t\t" << Xi << "\t" << f_Xi(Xi) << "\t" << derivada << "\t" << Xi_1 << "\t" << error_aprox << endl;

        if (error_aprox <= tolerancia){

            cout << "\nPara una tolerancia de " << tolerancia << "% la raiz de f es: " << Xi_1 << endl;

            break;
        }

        Xi = Xi_1;

    }while (1);


    return 0;


}

double f_Xi (double x){
    // Usando pow() para las potencias
    return pow(x, 4) - 8.6 * pow(x, 3) - 35.51 * pow(x, 2) + 464 * x - 998.46;
}

double f_der_Xi (double x){
    // También puedes escribirlo así para mayor rapidez
    return 4 * (x * x * x) - 25.8 * (x * x) - 71.02 * x + 464;
}

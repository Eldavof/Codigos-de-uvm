#include <iostream>
#define PRECICION 6
#include <iomanip> //set precicion
#include <cmath>

using namespace std;

void tabula(double Xl, double Xu);
double f(double x);

int main()
{
    cout << setprecision(PRECICION) << fixed;
    cout << "Calculo de las raices aplicando el metodo de Falsa Posicion" << endl;
    cout << "Ingrese el intervalo inicial [Xl, Xu]: " << endl;

    double Xl, Xu, tolerancia;

    cout << "Xl = ";
    cin >> Xl;
    cout << "Xu = ";
    cin >> Xu;

    tabula(Xl, Xu);

    cout << "\nEscoja el intervalo adecuado" << endl;
    cout << "Xl = ";
    cin >> Xl;

    cout << "Xu = ";
    cin >> Xu;

    double Xr = 0.0; // Raiz calculada
    double Xr_anterior = 0.0, error_aprox = 100.0;
    int iteraciones = 0;

    if (f(Xl) * f(Xu) > 0){
        cout << "\nNo se puede realizar el metodo de Falsa Posicion" << endl;
        cout << "porque f(" << Xl << ") y f(" << Xu << ") tienen el mismo signo" << endl;
    } else {
        cout << "Tolerancia (%) = ";
        cin >> tolerancia;

        // Encabezado actualizado a tus variables
        cout << "\nIter\tXl\t\tXu\t\tXr\t\tf(Xl)\t\tf(Xu)\t\tf(Xr)\t\tError(%)" << endl;

        do{
            Xr_anterior = Xr;
            iteraciones++;

            // Formula exacta a la de tus apuntes
            Xr = Xu - (f(Xu) * (Xl - Xu)) / (f(Xl) - f(Xu));

            if (iteraciones > 1 && Xr != 0.0){
                error_aprox = abs((Xr - Xr_anterior) / Xr) * 100.0;
            }

            cout << iteraciones << "\t" << Xl << "\t" << Xu << "\t" << Xr << "\t" << f(Xl) << "\t" << f(Xu) << "\t" << f(Xr) << "\t";

            if (iteraciones > 1){
                cout << error_aprox;
            } else {
                cout << "---";
            }

            cout << endl;

            if(error_aprox <= tolerancia && iteraciones > 1) {
                cout << "\nPara una tolerancia de " << tolerancia << "% la raiz de f es: " << Xr << endl;
                cout << "Error aproximado final: " << error_aprox << "%" << endl;
                break;
            } else {
                // Actualizacion de limites con las nuevas variables
                if(f(Xr) * f(Xl) > 0) {
                    Xl = Xr;
                } else if (f(Xr) * f(Xu) > 0){
                    Xu = Xr;
                } else {
                    break;
                }
            }
        } while (1);
    }

    return 0;
}

#define INTERVALOS 10
void tabula(double Xl, double Xu){
    int puntos = INTERVALOS + 1;
    double ancho = (Xu - Xl) / INTERVALOS;

    cout << "\n\tx\tf(x)" << endl;
    for(int i = 0; i < puntos; i++){
        cout << "\t" << Xl << "\t" << f(Xl) << endl;
        Xl = Xl + ancho;
    }
}

double f(double x){
    return (0.8-0.3*x)/x;
}

#include <iostream>
#define PRECICION 6
#include <iomanip> //set precicion
#include <cmath>

using namespace std;

void tabula(double Xa, double Xb);
double f(double x);

int main()
{
    cout << setprecision(PRECICION) << fixed;
    cout << "Calculo de las raices aplicando el metodo de Biseccion" << endl;
    cout << "Ingrese el intervalo inicial [Xa, Xb]: " << endl;

    double Xa, Xb, tolerancia;

    cout << "Xa = ";
    cin >> Xa;
    cout << "Xb = ";
    cin >> Xb;

    tabula(Xa, Xb);

    cout << "\nEscoja el intervalo adecuado" << endl;
    cout << "Xa = ";
    cin >> Xa;

    cout << "Xb = ";
    cin >> Xb;

    double Xm = 0.0; // Punto medio
    double Xm_anterior = 0.0, error_aprox = 100.0;
    int iteraciones = 0;

    if (f(Xa) * f(Xb) > 0){
        cout << "\nNo se puede realizar el metodo de la Biseccion" << endl;
        cout << "porque f(" << Xa << ") y f(" << Xb << ") tienen el mismo signo" << endl;
    } else {
        cout << "Tolerancia (%) = ";
        cin >> tolerancia;

        // Encabezado actualizado con iteraciones y error
        cout << "\nIter\tXa\t\tXb\t\tXm\t\tf(Xa)\t\tf(Xb)\t\tf(Xm)\t\tError(%)" << endl;

        do{
            Xm_anterior = Xm;
            iteraciones++; // Contador de vueltas

            // Formula del punto medio
            Xm = (Xa + Xb) / 2.0;

            // Candado: Solo calculamos error si pasamos de la vuelta 1
            if (iteraciones > 1 && Xm != 0.0){
                error_aprox = abs((Xm - Xm_anterior) / Xm) * 100.0;
            }

            // Imprimimos la fila de datos
            cout << iteraciones << "\t" << Xa << "\t" << Xb << "\t" << Xm << "\t" << f(Xa) << "\t" << f(Xb) << "\t" << f(Xm) << "\t";

            // Ocultamos el error de la primera iteracion
            if (iteraciones > 1){
                cout << error_aprox;
            } else {
                cout << "---";
            }
            cout << endl;

            // Freno de emergencia para ganar
            if(error_aprox <= tolerancia && iteraciones > 1) {
                cout << "\nPara una tolerancia de " << tolerancia << "% la raiz de f es: " << Xm << endl;
                cout << "Error aproximado final: " << error_aprox << "%" << endl;
                break;
            } else {

                // Actualizacion de los limites para la siguiente vuelta
                if(f(Xm) * f(Xa) > 0) {
                    Xa = Xm;
                } else if (f(Xm) * f(Xb) > 0){
                    Xb = Xm;
                } else {
                    break; // Por si le atinamos a la raiz exacta y f(Xm) da 0
                }
            }

        } while (1);
    }

    return 0;
}

#define INTERVALOS 10
void tabula(double Xa, double Xb){
    int puntos = INTERVALOS + 1;
    double ancho = (Xb - Xa) / INTERVALOS;

    cout << "\n\tx\tf(x)" << endl;
    for(int i = 0; i < puntos; i++){
        cout << "\t" << Xa << "\t" << f(Xa) << endl;
        Xa = Xa + ancho;
    }
}

double f(double x){
    return exp(-x)-x;
}

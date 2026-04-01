#include <iostream>
#include "Entrenador.h"
using namespace std;

int main()
{
    Entrenador objeto;
    objeto.mostrarinfo();
    objeto.numEn=12508;
    cout<<"Registra el nombre del entrenador";
    getline(cin,objeto.nombre);
    cout<<"Escribe el pago al entrenador MXN$";
    cin>>objeto.pago;
    cout<<"Escribe las credenciales ";
    cin>>objeto.certificacion;

    objeto.mostrarinfo();
    return 0;
}

#include <iostream>
#include "Entrenador_si.h"
using namespace std;

int main()
{
    Entrenador_si e;
    cout<<"ingrese el nombre del entrenador"<<endl;
    cin>>e.nombre;
    cout<<"ingrese su sueldo"<<endl;
    cin>>e.sueldo;

    e.mostrarEntrenador_si();
    return 0;
}

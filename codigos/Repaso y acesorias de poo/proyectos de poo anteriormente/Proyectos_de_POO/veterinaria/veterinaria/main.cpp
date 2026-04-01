#include <iostream>
#include "Perro.h"
using namespace std;

int main()
{
    Perro elchingon;
    cout<<"Escribe el nombre del perro"<<endl;
    cin>>elchingon.nombre;
    cout<<"escribe la edad del perro"<<endl;
    cin>>elchingon.edad;
    cout<<"escribe el nombre del dueño"<<endl;
    cin>>elchingon.dueno;

    elchingon.MostrarDatos();
    elchingon.RegistrarVacuna();
    elchingon.CobrarConsulta();
    return 0;
}

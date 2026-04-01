#include "Empleado.h"
#include<iostream>
#include<string>
using namespace std;

Empleado::Empleado(string n)
{
    nombre=n;
    cout<<"\nConstruye Empleado"<< nombre<<endl;
}

void Empleado::capacitarse(){
cout<<"\nCapacitando a "<<nombre<<endl;
}

string Empleado::getNombre(){
return nombre;
}

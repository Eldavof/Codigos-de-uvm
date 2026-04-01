#include "EmpleadoCaja.h"
#include "Empleado.h"
#include<iostream>
#include<string>
using namespace std;

EmpleadoCaja::EmpleadoCaja(string n):Empleado(n)
{
    cout<<"\nEmpleado de caja "<<getNombre();
}

void EmpleadoCaja::cobrar()
{
    cout<<"Pago en efectivo por favor";
}

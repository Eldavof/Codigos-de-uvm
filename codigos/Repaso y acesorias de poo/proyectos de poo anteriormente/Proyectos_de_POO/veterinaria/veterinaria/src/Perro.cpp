#include "Perro.h"
#include <iostream>

void Perro::CobrarConsulta()
{
cout<<"son 500 pesos de su consulta"<<endl;
}

void Perro::RegistrarVacuna()
{
    cout<<nombre<<" esta vacunado "<<endl;
}

void Perro::MostrarDatos()
{
    cout<<nombre<<" pertenece a "<<dueno<<endl;
    cout<<"tiene "<<edad<<"años"<<endl;
}

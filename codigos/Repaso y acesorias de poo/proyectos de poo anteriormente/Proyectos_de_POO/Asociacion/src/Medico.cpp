#include "Medico.h"
#include <iostream>
#include <string>
using namespace std;

Medico::Medico(string nombre, int c)
{
    this->nombre=nombre;
    cedula=c;
    libre=true;
}

Medico::~Medico()
{
    cout<<"Medico "<<nombre<<"  dado de baja"<<endl;
}

string Medico::getNombre()
{
    return nombre;
}

int Medico::getCedula()
{
    return cedula;
}

bool Medico::registrarCita()
{
    if(libre){
        libre=false;
        cout<<"cita registrar"<<endl;
        return true;
    } else{
    cout<<"El medico "<<nombre<<" no esta disponible"<<endl;
    return false;
    }
}

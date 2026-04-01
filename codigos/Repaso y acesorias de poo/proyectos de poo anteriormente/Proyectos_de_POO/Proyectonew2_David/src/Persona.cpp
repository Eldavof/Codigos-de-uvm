#include "Persona.h"
#include <iostream>
#include <string>
using namespace std;

Persona::Persona(string nombre, int e){
this->nombre=nombre;
edad=e;
}

void Persona::mostrar(){
cout<<"Nombre: "<<nombre<<"\n Edad: "<<edad<<endl;
}

Persona::~Persona()
{
    cout<<"Ya te destrui al: "<<nombre<<endl;
}

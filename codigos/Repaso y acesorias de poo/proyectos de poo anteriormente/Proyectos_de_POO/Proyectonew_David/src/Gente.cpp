#include "Gente.h"
#include <iostream>
#include <string>
using namespace std;

Gente::Gente(string nombre, int e){
this->nombre=nombre;
edad=e;
}

void Gente::mostrar(){
cout<<"Nombre: "<<nombre<<"\n Edad: "<<edad<<endl;
}

Gente::~Gente()
{
    cout<<"Ya te destrui al: "<<nombre<<endl;
}

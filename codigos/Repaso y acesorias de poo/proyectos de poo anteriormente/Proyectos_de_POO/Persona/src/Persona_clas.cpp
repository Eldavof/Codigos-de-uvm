#include "Persona_clas.h"
#include <iostream>
#include <string>
using namespace std;

Persona_clas::Persona_clas(){
nombre="Desconocido";
edad=0;
}

Persona_clas::Persona_clas(string nom, int ed){
nombre=nom;
edad=ed;
}

Persona_clas::Persona_clas(Persona_clas &p){
nombre=p.nombre;
edad=p.edad;
}

void Persona_clas::mostrarDatos(){
cout<<"Nombre: "<<nombre<<" , Edad "<<edad<<endl;
}

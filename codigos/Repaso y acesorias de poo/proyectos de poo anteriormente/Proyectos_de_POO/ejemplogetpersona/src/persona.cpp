#include "persona.h"
#include <iostream>
#include <string>
using namespace std;

void persona::setNombre(string nuevoNombre){
nombre = nuevoNombre;
}
string persona::getNombre(){
return nombre;
}

void persona::sedEdad(int nuevaEdad){

    if (nuevaEdad > 0){
        edad=nuevaEdad;
    } else{
    cout<<" edad no valida"<<endl;
    }
}
int persona::getEdad(){
return edad;

}

#include "Animalpro.h"
#include <string>
#include <iostream>
using namespace std;



Animalpro::Animalpro()
{
    nombre="callejero";
    edad=-1;
    tutor="Desconocido";
    pago=-1;
    cout<<"\nAnimalito nuevo\n";
}

Animalpro::Animalpro(string tu, string nombre){
    tutor=tu;
    this->nombre=nombre;
}

Animalpro::Animalpro(int edad, string nombre){
    this->edad=edad;
    this->nombre=nombre;
}

Animalpro::Animalpro(string tu, string nombre, int ed, float p){
    tutor=tu;
    this->nombre=nombre;
    edad=ed;
    pago=p;
    cout<<nombre<<" de "<<tutor<<" tiene "<<edad<<" años. $"<<pago;
}

void Animalpro::setTutor(string t){
    tutor=t;
}

void Animalpro::setEdad(int edad){
    if(this->edad < edad && edad < 120 && edad>0){
        this->edad=edad;
    }
}

void Animalpro::setPago(float p){
    pago=p;
}

string Animalpro::getTutor(){
return tutor;
}

int Animalpro::getEdad(){
return edad;
}

float Animalpro::calcularPgo(){
    if(edad>1 && edad <5){
        return pago*1.1;
    } else if(edad >=5){
    return pago*1.2;
        } else if (edad>=0){
        return pago;
        } else{
        return -1;
        }
}

void Animalpro::mostrarInfo(){
cout<<"\nAnimal "<<nombre<<" de "<<tutor<<endl;
cout<<"Tiene "<<edad<<" años"<<endl;
cout<<"Debe $"<<pago;
}

Animalpro::~Animalpro()
{
    cout<<"\nAnimal "<<nombre<< " destruido";
}

#include "Empleado.h"
#include <iostream>
#include <vector>
#include <string>
#include <iostream>
using namespace std;


Empleado::Empleado()
{
    nombre= "Sin datos";
    id= 0;
    dias_laborales= "Sin datos";
    sueldo= 0;

}

Empleado::Empleado(float s, string n, int i, string dl)
{
    nombre= n;
    id= i;
    dias_laborales= dl;
    sueldo= s;

}

Empleado::~Empleado()
{
    //dtor
}

void Empleado::setnombre(string nombre){

    this->nombre=nombre;

}

string Empleado::getnombre(){

    return nombre;

}

void Empleado::setsueldo(float sueldo){

    this->sueldo=sueldo;

}

float Empleado::getsueldo(){

    return sueldo;

}

void Empleado::setid(int id){

    this->id=id;

}

int Empleado::getid(){

    return id;

}

void Empleado::setdias_laborales(string dias_laborales){

    this->dias_laborales=dias_laborales;

}

string Empleado::getdias_laborales(){

    return dias_laborales;

}

void Empleado::mostrarinfo(){

    cout << "--- Datos de los empleados ---" << endl;
    cout << "ID: " << id << endl;
    cout << "Nombre: " << nombre << endl;
    cout << "Sueldo al mes: $" << sueldo << endl;
    cout << "Dias de trabajo: " << dias_laborales << endl;
    cout << "--------------------------" << endl;

}

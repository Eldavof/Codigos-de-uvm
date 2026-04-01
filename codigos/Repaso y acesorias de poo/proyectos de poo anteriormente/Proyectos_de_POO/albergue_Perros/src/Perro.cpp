#include "Perro.h"
#include <iostream>
using namespace std;

Perro::perro(string du, string no, int sal)
{
    dueno=du;
    nombre=no;
    salud=sal;
    tiempo=0;
}

void Perro::ladrar(){
    if(salud>0 && salud<15){
        cout<<nombre<<" esta sano. Vida= "<<salud<<endl;
    }
    else if(salud >=15){
        cout<<nombre<<" esta enfermo. Vida= "<<salud<<endl;
        enfermar();

    } else{
        cout<<nombre<<" esta muerto. vida= "<<salud<<endl;
    }
}

void Perro::comer(){
    salud+=5;
    if(Salud<0 || salud>15){

        enfermar();
    }
}

void Perro:enfermar(){
    salud-=5;
    if(salud<0 || salud>15){

        salud-=10;
    }
}

bool Perro::comparar(Perro p){
    if(nombre==p.getNombre() && dueno==p.getdueno() && tiempo==p.getTiempo() && salud==p.getSalud()){
        return true;
    } else{
    return false;
    }
}

string Perro::getNombre(){return nombre;}
string Perro::getdueno(){return dueno;
int Perro::getTiempo(}{return tiempo;}
int Perro::getSalud(){return salud;}

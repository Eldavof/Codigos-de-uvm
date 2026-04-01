#include "Refugio.h"
#include <iostream>
using namespace std;


Refugio::Refugio(string n)
{
    nombre=n
}

Refugio::~Refugio()
{
    for(Perro* x:habitantes){

        delete x;
    }
}
void Refugio::recibirPerro(){
    habitantes.push_back(p);
    count<<"Ahora hay "<<habitantes.size()<<" perros."<<endl;
}

void Refugio::mostrarHabitantes(){
    for(Perro* loqui:habitantes){

        loqui->ladrar();
    }
}

Refugio::buscarPerro(string nombre){
    for(Perro* x:habitantes){

        if(x->getNombre().compare(nombre)==0){
            return x;
        }
    }
    return nullptr;
}

void Refugio::darEnAdopcion(Perro p){
    int pos=0
    for(Perro* b:habitantes){

        if(b->comparar(p)){

            habitantes.erase(habitantes.begin()+pos);

        }
        pos++;
    }
}

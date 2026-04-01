#include "Profesor.h"
#include<iostream>
#include<string>
using namespace std;

Profesor::Profesor()
{
    cout<<"\nConstruye Profesor"<<endl;
}

void Profesor::estudiar(){
    cout<<"\nPreparar Clase";
}

void Profesor::prepararClase()
{
    estudiar();
    cout<<"\nEstudiar";
}

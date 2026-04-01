#include "ProfeTiempoC.h"
#include "Profesor.h"
#include<iostream>
#include<string>
using namespace std;

ProfeTiempoC::ProfeTiempoC()
{
    cout<<"\nConstruye Profe de TC"<<endl;
}

void ProfeTiempoC::darConferencia(){
    cout<<"\nConferencia "<<experiencia<<endl;
    cout<<"\nMis atributos son:\n ";
    cout<<"Horas: "<<horas<<" - Nivel "<<nivel<<" con "<<experiencia<<" años de experiencia "<<endl;
}

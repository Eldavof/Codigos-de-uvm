#include "Consultorio.h"
#include <iostream>
#include <string>
using namespace std;

Consultorio::Consultorio(string d, float r)
{
    string nom; int ced;
    domicilio=d;
    renta=r;
    cout<<"consultorio en "<<domicilio<<" creado"<<endl;
    cout<<"registro del medico 1"<<endl;
    cout<< "nombre del medico 1: ";
    getline(cin, nom);
    cout<< "cedula del medico 1: ";
    cin>>ced;
    //m1
    m1=new Medico(nom,ced);
    cin.ignore();
    cout<<"registro del medico 2"<<endl;
    cout<< "nombre del medico 2: ";
    getline(cin, nom);
    cout<< "cedula del medico 2: ";
    cin>>ced;
    //m2
    m2=new Medico(nom,ced);
    cin.ignore();
    cout<<"registro del medico 3"<<endl;
    cout<< "nombre del medico 3: ";
    getline(cin, nom);
    cout<< "cedula del medico 3: ";
    cin>>ced;
    //m3
    m3=new Medico(nom,ced);
}

Consultorio::~Consultorio()
{
    //liberar obj dinamicos
    delete m1;
    delete m2;
    delete m3;
    cout<<"consultorio clausurado definitivamente"<<endl;
}

string Consultorio::getDomicilio()
{
    return domicilio;
}

float Consultorio::getRenta()
{
    return renta;
}

void Consultorio::setRenta(float r)
{
    if(r>0){
        renta=r;
    }
}

void Consultorio::sacarCita()
{
    if(m1->registrarCita())
    {
        cout<<"cita generada con "<<m1->getNombre()<<endl;
    } else if (m2->registrarCita()){
    cout<<"cita generada con "<<m2->getNombre()<<endl;
    } else if (m3->registrarCita()){
    cout<<"cita generada con "<<m3->getNombre()<<endl;
    } else{
    cout<<"No hay citas disponibles"<<endl;
    }
}

#include <iostream>
#include <string>
#include "persona.h"
using namespace std;

int main()
{
    persona p1;
    string nomin;
    int edadin;
    cout<<"ingresa tu nombre"<<endl;
    getline(cin,nomin);
    p1.setNombre(nomin);
    cout<<"ingresa tu edad"<<endl;
    cin>>edadin;
    p1.sedEdad(edadin);

    cout<<"Nombre: "<<p1.getNombre()<<endl;
    cout<<"Edad: "<<p1.getEdad()<<" años"<<endl;
    return 0;
}

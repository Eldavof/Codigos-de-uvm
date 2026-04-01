#include "info.h"
#include <iostream>
using namespace std;
info::info()
{
    //ctor
}

info::~info()
{
    //dtor
}

void info::mostrarDatos(){
cout<<"//////////////////////////////////////////////////"<<endl;
cout<<"Estudiante:      "<<nombre<<"/////////////////////"<<endl;
cout<<"Promedio:        "<<promedio<<"///////////////////"<<endl;
cout<<"Beca del:        "<<beca*100<<"%"<<"//////////////"<<endl;
cout<<"Matricula:       "<<matricula<<"//////////////////"<<endl;
cout<<"//////////////////////////////////////////////////"<<endl;
}

#include "Entrenador.h"
#include <iostream>
#include <string>
using namespace std;

Entrenador::Entrenador(){
    nombre="Anonimo";
    certificacion="Certificacion Basica";
    numEn=9999;
    pago=100.56;
}

void Entrenador::mostrarinfo(){
cout<<"Num de entrenador # "<<numEn<<"*****************************\n";
cout<<"Entrenador "<<nombre<<endl;
cout<<certificacion<<endl<<"Pago-->$"<<pago<<endl;
}

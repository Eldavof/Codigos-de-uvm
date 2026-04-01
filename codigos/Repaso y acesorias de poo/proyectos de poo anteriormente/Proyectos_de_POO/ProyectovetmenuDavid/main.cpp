#include <iostream>
#include <string>
#include <clocale>
#include "Animalpro.h"
using namespace std;

int main()
{
    setlocale(LC_CTYPE, "spanish");
    Animalpro *ap;
    Animalpro otro;
    string t1, t2;
    int edad; float pago;
    int opc=0;
do{
        cout<<"\n0-salir\n1-Crear objeto dinamico\n2-Ver info\n3-Cambiar edad din\n4-Cambiar tutor din\n5-Calcular pago din\n6-Datos estatico\n7-Mostrar info estatico\n";
        cin>>opc;
        switch(opc){
    case 0:
        delete ap;
        break;
    case 1:
        {
            cout<<"Nombre del tutor ";
            cin>>t1;
            cout<<"Nombre del animal ";
            cin>>t2;
            cout<<"Edad del animal ";
            cin>>edad;
            cout<<"Credito disponible ";
            cin>>pago;
            ap=new Animalpro(t1,t2,edad,pago);
        }
        break;
    case 2:
        ap->mostrarInfo();
        break;
    case 3:
        {
            cout<<"Nuevo edad de"<<ap->nombre;
            cin>>edad;
            ap->setEdad(edad);
            ap->mostrarInfo();
        }
        break;
    case 4:
        {
            cout<<"Nuevo tutor de"<<ap->nombre;
            cin>>t1;
            ap->setTutor(t1);
            ap->mostrarInfo();
        }
        break;
    case 5:
        pago=ap->calcularPgo();
        cout<<ap->getTutor()<<" debe $"<<pago;
        break;
    case 6:{
        cout << "Nombre del tutor ";
        cin>>t1;
        otro.setTutor(t1);
        cout << "Nombre del animal ";
        cin>>t2;
        otro.nombre=t2;
        cout << "Edad del animal ";
        cin>>edad;
        otro.setEdad(edad);
        cout << "Credito disponible ";
        cin>>pago;
        otro.setPago(pago);
        otro.mostrarInfo();
}
break;

    case 7:
        otro.mostrarInfo();
        }
}while(opc!=0);

return 0;
}

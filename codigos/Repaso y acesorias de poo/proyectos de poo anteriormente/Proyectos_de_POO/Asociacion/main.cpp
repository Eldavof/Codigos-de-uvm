#include <iostream>
#include "Consultorio.h"
#include <string>
#include <clocale>
using namespace std;

int main()
{
    setlocale(LC_CTYPE, "spanish");
    int opc;
    cout<< "Registrar a los medicos del consultorio\n";
    Consultorio c("Tlalpan 3050", 75000);
    do{
        cout<<"0. Salir\n";
        cout<<"1. Sacar cita\n";
        cout<<"2. consultar domicilio\n";
        cout<<"3. Consultar renta\n";
        cout<<"4. Modificar renta\n";
        cout<<"Opcion: ";
        cin>>opc;
        switch(opc ){
        case 0: break;
        case 1: c.sacarCita();
        break;
        case 2: cout<<"Domicilio "<<c.getDomicilio()<<endl;
        break;
        case 3: cout<<"Renta: "<<c.getRenta()<<endl;
        break;
        case 4:
        float r;
        cout<<"Nueva renta: ";
        cin>>r;
        c.setRenta(r);
        break;

                    default: cout<<"Opcion no valida\n";
        }
    } while(opc!=0);
    return 0;
}

#include <iostream>
#include <string>
#include "Persona.h"
using namespace std;

int main()
{
    int Tam=3, i;
    Persona *Personas[Tam];
    //entrada de dtos
    for(i=0; i<Tam; i++)
    {
        string nombre;
        int edad;
        cout<<"Ingrese el nombre de la persona "<<i<<": ";
        getline(cin,nombre);
        cout<<"Ingrese la edad de "<<nombre<<": ";
        cin>>edad;
        //crear objeto dinamicamente
        Personas[i]=new Persona(nombre, edad);
        cin.ignore(); //limpia el buffer de la memoria

    }

    cout<< "\nDatos de las personas ingresadas:\n";
    for (i=0; i<Tam; i++){
        (*Personas[i]).mostrar();
    }
    //liberar memoria de los objetos creados
    cout<<"\nBorrado de objetos dinamicos"<<endl;
    for(i=0; i<Tam; i++){
        delete Personas[i];
    }


    return 0;
}

#include <iostream>
#include "El_diego.h"
using namespace std;

int main()
{
    El_diego e;
    cout<<"ingrese el nombre de la clase"<<endl;
    cin>>e.clase;
    cout<<"ingrese el juego"<<endl;
    cin>>e.juego;
    cout<<"ingrese el numero de no a los chatis"<<endl;
    cin>>e.chati;

    e.RegistrarDatos();
    e.MostrarDatos();
        if (e.chati>6)
            {
    e.MetodoJuzgador();
}
    return 0;
}


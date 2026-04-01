#include <iostream>
#include "Persona_clas.h"
#include <iostream>
using namespace std;

int main()
{
    Persona_clas persona1;
    persona1.mostrarDatos();

    Persona_clas persona2("lalito", 25);
    persona2.mostrarDatos();

    Persona_clas persona3=persona2;
    persona3.mostrarDatos();

    return 0;
}

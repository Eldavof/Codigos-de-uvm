#ifndef PERSONA_CLAS_H
#define PERSONA_CLAS_H
#include <iostream>
#include <string>
using namespace std;

class Persona_clas
{
    public:
        Persona_clas();
        Persona_clas(string nom, int ed);
        Persona_clas(Persona_clas &p);
        void mostrarDatos();

    protected:

    private:
        string nombre;
        int edad;
};

#endif // PERSONA_CLAS_H

#ifndef PERSONA_H
#define PERSONA_H
#include <iostream>
#include <string>
using namespace std;

class Persona
{
    public:
        Persona(string nombre, int e);
        ~Persona();
        void mostrar();
    protected:

    private:
       string nombre;
       int edad;
};

#endif // GENTE_H

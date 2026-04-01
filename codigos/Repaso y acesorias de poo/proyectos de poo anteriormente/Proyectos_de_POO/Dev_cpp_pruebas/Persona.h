#ifndef PERSONA_H
#define PERSONA_H
#include <iostream>
#include <string>
using namespace std;

class persona
{
    public:
        void setNombre(string nuevoNombre);

    string getNombre();
    void sedEdad(int nuevaEdad);
    int getEdad();


    protected:

    private:
        string nombre;
        int edad;
};

#endif // PERSONA_H


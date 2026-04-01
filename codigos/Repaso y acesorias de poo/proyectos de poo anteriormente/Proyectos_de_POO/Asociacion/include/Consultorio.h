#ifndef CONSULTORIO_H
#define CONSULTORIO_H
#include <iostream>
#include <string>
#include "Medico.h"
using namespace std;

class Consultorio
{
    public:
        Consultorio(string d, float r);
        ~Consultorio();
        string getDomicilio();
        float getRenta();
        void setRenta(float r);
        void sacarCita();

    protected:

    private:
        string domicilio;
        float renta;
        Medico* m1;
        Medico* m2;
        Medico* m3;
};

#endif // CONSULTORIO_H

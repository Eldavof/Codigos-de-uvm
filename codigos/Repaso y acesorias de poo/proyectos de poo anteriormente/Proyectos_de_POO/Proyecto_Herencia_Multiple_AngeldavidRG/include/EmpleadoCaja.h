#ifndef EMPLEADOCAJA_H
#define EMPLEADOCAJA_H
#include<iostream>
#include<string>
#include "Empleado.h"
using namespace std;

class EmpleadoCaja: public Empleado
{
    public:
        EmpleadoCaja(string n);
        void cobrar();

    protected:

    private:
};

#endif // EMPLEADOCAJA_H

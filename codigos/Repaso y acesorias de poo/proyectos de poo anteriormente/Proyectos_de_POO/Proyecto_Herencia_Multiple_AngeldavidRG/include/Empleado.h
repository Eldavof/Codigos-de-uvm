#ifndef EMPLEADO_H
#define EMPLEADO_H
#include<iostream>
#include<string>
using namespace std;

class Empleado
{
    public:
        Empleado(string n);
        void capacitarse();
        string getNombre();

    protected:
        float salario;

    private:
        string nombre;
};

#endif // EMPLEADO_H

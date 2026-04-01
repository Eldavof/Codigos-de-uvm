#ifndef MEDICO_H
#define MEDICO_H
#include <iostream>
#include <string>
using namespace std;

class Medico
{
    public:
        Medico(string n, int c);
        ~Medico();
        string getNombre();
        int getCedula();
        bool registrarCita();

    protected:

    private:
        int cedula;
        string nombre;
        bool libre;
};

#endif // MEDICO_H

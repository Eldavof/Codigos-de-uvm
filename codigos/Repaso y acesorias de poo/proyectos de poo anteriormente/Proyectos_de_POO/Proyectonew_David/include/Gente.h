#ifndef GENTE_H
#define GENTE_H
#include <iostream>
#include <string>
using namespace std;

class Gente
{
    public:
        Gente(string nombre, int e);
        ~Gente();
        void mostrar();
    protected:

    private:
       string nombre;
       int edad;
};

#endif // GENTE_H

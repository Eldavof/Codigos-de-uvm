#ifndef EMPLEADO_H
#define EMPLEADO_H
#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Empleado
{
    public:
        Empleado();
        ~Empleado();
        Empleado(float s, string n, int i, string dl);
        void setnombre(string nombre);
        string getnombre();
        void setsueldo(float sueldo);
        float getsueldo();
        void setid(int id);
        int getid();
        void setdias_laborales(string dias_laborales);
        string getdias_laborales();
        void mostrarinfo();

    protected:

    private:
        int id;
        float sueldo;
        string nombre, dias_laborales;
};

#endif // EMPLEADO_H

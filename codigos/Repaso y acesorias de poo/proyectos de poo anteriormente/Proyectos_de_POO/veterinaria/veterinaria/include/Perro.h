#ifndef PERRO_H
#define PERRO_H
#include <string>
using namespace std;

class Perro
{
    public:
       string nombre;
       int edad;
       string dueno;
       string raza;

       void CobrarConsulta();
       void RegistrarVacuna();
       void MostrarDatos();

    protected:

    private:
};

#endif // PERRO_H

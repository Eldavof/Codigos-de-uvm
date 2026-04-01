#include <iostream>
#include <vector>
#include <Perro.h>
#include <string>
using namespace std;



class Refugio
{
    public:
        Refugio (string n);
        ~Refugio();
        void recibirPerro(Perro*p);
        void mostrarHabitantes();
        Perro* buscarPerro(string nombre);
        void darEnAdopcion(Perro p);
    protected:

    private:
        string nombre;
        vector<Perro*> habitantes;
};

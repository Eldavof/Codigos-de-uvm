#ifndef ANIMALPRO_H
#define ANIMALPRO_H
#include <string>
#include <iostream>
using namespace std;

class Animalpro
{
    public:
        string nombre;
        Animalpro();
        Animalpro(string tu, string nombre);
        Animalpro(int edad, string nombre);
        Animalpro(string tu, string nombre, int ed, float p);
        ~Animalpro();
        void setTutor (string t);
        void setEdad (int edad);
        void setPago (float p);
        string getTutor();
        int getEdad();
        void mostrarInfo();
        float calcularPgo();


    protected:

    private:
        int edad;
        float pago;
        string tutor;
};

#endif // ANIMALPRO_H

#ifndef PROFESOR_H
#define PROFESOR_H
#include <iostream>
#include <string>
using namespace std;


class Profesor
{
    public:
        Profesor();
        void prepararClase();

    protected:
        int horas;
        char nivel;

    private:
        void estudiar();
};

#endif // PROFESOR_H

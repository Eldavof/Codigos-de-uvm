#ifndef PROFETIEMPOC_H
#define PROFETIEMPOC_H
#include "Profesor.h"
#include<iostream>
#include<string>
using namespace std;

class ProfeTiempoC: public Profesor
{
    public:
        ProfeTiempoC();
        void darConferencia();

    protected:

    private:
        int experiencia;
};

#endif // PROFETIEMPOC_H

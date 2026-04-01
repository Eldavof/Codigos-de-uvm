#ifndef TIENDA_H
#define TIENDA_H
#include <Producto.h>
#include <Empleado.h>
#include <vector>
#include <string>
#include <iostream>
using namespace std;

class Tienda
{
    public:
        Tienda();
        ~Tienda();
        void agregarproducto(Producto*);
        bool eliminarproducto(Producto*);
        Producto* buscarproducto(int cb);
        Producto* buscarproducto(string n);

        void agregarempleado(Empleado*);
        bool eliminarempleado(Empleado*);
        Empleado* buscarempleado(int i);
        Empleado* buscarempleado(string n);



    protected:

    private:
        vector<Producto*> inventario;
        vector<Empleado*> personal;
};

#endif // TIENDA_H

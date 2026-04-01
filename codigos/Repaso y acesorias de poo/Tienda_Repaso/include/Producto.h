#ifndef PRODUCTO_H
#define PRODUCTO_H
#include <iostream>
#include <vector>
#include <string>
using namespace std;


class Producto
{
    public:
        Producto();
        ~Producto();
        Producto(int cant, string nom, int i, float pre);
        void setnombre(string nombre);
        string getnombre();
        void setprecio(float precio);
        float getprecio();
        void setid(int id);
        int getid();
        void setcantidad(int cantidad);
        int getcantidad();
        void mostrarinfo();

    protected:

    private:
        int cantidad, id;
        float precio;
        string nombre;

};

#endif // PRODUCTO_H

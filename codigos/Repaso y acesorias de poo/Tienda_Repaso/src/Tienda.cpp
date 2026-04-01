#include "Tienda.h"
#include <vector>
#include <string>
#include "Producto.h"
#include "Empleado.h"
#include <iostream>
using namespace std;


Tienda::Tienda()
{
    //ctor
}

Tienda::~Tienda()
{
    //dtor
}

void Tienda::agregarproducto(Producto* w){

    inventario.push_back(w);

}

bool Tienda::eliminarproducto(Producto* w){
    int pos=0;
        for(Producto* x : inventario){
            if(x->getid() == w->getid())
            {
                inventario.erase(inventario.begin()+pos);
                return true;
            }
            else{
            pos++;
            }

        }
        return false;
    }


Producto* Tienda::buscarproducto(int cb){

    int pos=0;
    for(Producto* x : inventario){
        if (x->getid() == cb){

            return x;
        }else{
        pos++;
        }

    }
    return nullptr;
}

Producto* Tienda::buscarproducto(string n){

    int pos=0;
    for(Producto* x : inventario){
        if (x->getnombre() == n){

            return x;
        }else{
        pos++;
        }

    }
    return nullptr;
}

void Tienda::agregarempleado(Empleado* w){

    personal.push_back(w);

}

bool Tienda::eliminarempleado(Empleado* w){

    int pos=0;
    for(Empleado* x : personal){

        if(x->getid() == w->getid()){
            personal.erase(personal.begin()+pos);
            return true;

        }else{
        pos++;
        }

    }
    return false;
}

Empleado* Tienda::buscarempleado(int i){

    int pos=0;
    for(Empleado* x : personal){

        if(x->getid() == i){

            return x;
        }else{
        pos++;
        }

    }
    return nullptr;
}

Empleado* Tienda::buscarempleado(string n){

    int pos=0;
    for(Empleado* x : personal){

        if(x->getnombre() == n){

            return x;
        }else{
        pos++;
        }

    }
    return nullptr;
}

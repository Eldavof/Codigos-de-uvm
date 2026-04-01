#include "Producto.h"
#include <iostream>
#include <vector>
#include <string>
using namespace std;


Producto::Producto()
{
    nombre="sin datos";
    id=0;
    cantidad=0;
    precio=0;

}

Producto::Producto(int cant, string nom, int i, float pre)
{
    nombre=nom;
    id=i;
    cantidad=cant;
    precio=pre;

}

Producto::~Producto()
{
    //dtor
}

void Producto::setnombre(string nombre){

    this->nombre=nombre;

}

string Producto::getnombre(){

    return nombre;
}

void Producto::setprecio(float precio){

    this->precio=precio;

}

float Producto::getprecio(){

    return precio;
}

void Producto::setid(int id){

    this->id=id;

}

int Producto::getid(){

    return id;
}

void Producto::setcantidad(int cantidad){

    this->cantidad=cantidad;

}

int Producto::getcantidad(){

    return cantidad;
}

void Producto::mostrarinfo(){

    cout << "--- Datos del Producto ---" << endl;
    cout << "ID: " << id << endl;
    cout << "Nombre: " << nombre << endl;
    cout << "Precio: $" << precio << endl;
    cout << "Stock: " << cantidad << " unidades" << endl;
    cout << "--------------------------" << endl;

}

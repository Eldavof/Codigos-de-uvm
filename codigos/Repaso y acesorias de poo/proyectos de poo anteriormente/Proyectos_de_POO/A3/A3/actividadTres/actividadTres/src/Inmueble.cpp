#include "Inmueble.h"
#include <iostream>
#include <string>
using namespace std;


// Inicializa un objeto Inmueble con un conjunto de valores predeterminados.
Inmueble::Inmueble()
{
    tipo = "Casa";
    direccion = "Av. Tlalpan Número 54";
    renta = 2500.0;
    disponible = false;
}


// Inicializa un objeto Inmueble usando los valores que se le pasan como argumentos.
Inmueble::Inmueble(string t, string d, double r, bool disp)
{
    tipo = t;
    direccion = d;
    renta = r;
    disponible = disp;
}


// Se ejecuta automáticamente al destruir un objeto, mostrando un mensaje de confirmación.
Inmueble::~Inmueble()
{
    cout << "Se destruyeron los datos del inmueble creado" << endl;
}


// Asigna el valor del parámetro 'd' al atributo 'direccion' del objeto.
void Inmueble::setDireccion(string &d)
{
    direccion = d;
}
// Devuelve el valor actual del atributo 'direccion'.
string Inmueble::getDireccion()
{
    return direccion;
}

// Asigna el valor del parámetro 'r' al atributo 'renta'.
void Inmueble::setRenta(double r)
{
    renta = r;
}
// Devuelve el valor actual del atributo 'renta'.
double Inmueble::getRenta()
{
    return renta;
}

// Asigna el valor del parámetro 'disp' al atributo 'disponible'.
void Inmueble::setDisponible(bool disp)
{
    disponible = disp;
}
// Devuelve el estado actual del atributo 'disponible' (true o false).
bool Inmueble::isDisponible()
{
    return disponible;
}

// Asigna el valor del parámetro 't' al atributo 'tipo'.
void Inmueble::setTipo(string &t)
{
    tipo = t;
}
// Devuelve el valor actual del atributo 'tipo'.
string Inmueble::getTipo()
{
    return tipo;
}

// Muestra en la consola toda la información del objeto de manera clara y formateada.
void Inmueble::mostrarInfo()
{
    cout << "Información del inmueble" << endl;
    cout << "Tipo: " << tipo << endl;
    cout << "Dirección: " << direccion << endl;
    cout << "Renta: $" << renta << endl;
    // Se usa un operador ternario para mostrar "Si" o "No" en lugar de 1 o 0.
    cout << "Disponible: " << (disponible ? "Sí" : "No") << endl;
    cout << "-----------------------------------" << endl;
}

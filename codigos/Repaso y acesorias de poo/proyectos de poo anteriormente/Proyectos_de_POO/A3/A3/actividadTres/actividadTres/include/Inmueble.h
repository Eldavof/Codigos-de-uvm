#ifndef INMUEBLE_H
#define INMUEBLE_H
#include <iostream>
#include <string>
using namespace std;


class Inmueble
{

private:
    string direccion;
    double renta;
    bool disponible;

public:
    string tipo;



     //Constructor por defecto.
     //Crea una instancia de Inmueble con valores predeterminados o vacíos.
    Inmueble();

        //Constructor parametrizado.
        //Crea una instancia de Inmueble con los valores iniciales proporcionados.
        //tipo El tipo de inmueble.
        //direccion La dirección del inmueble.
        //renta El costo de la renta.
        //disponible El estado de disponibilidad.
    Inmueble(string tipo, string direccion, double renta, bool disponible);


     //Destructor.
     //Se llama automáticamente cuando un objeto Inmueble es destruido. Libera recursos si es necesario.
    ~Inmueble();

     //Establece la dirección del inmueble.
     //d La nueva dirección.
    void setDireccion(string &d);
     //Obtiene la dirección actual del inmueble.
     //La dirección como un string.
    string getDireccion();

    //Establece el costo de la renta.
    //r El nuevo valor de la renta.
    void setRenta(double r);
     //Obtiene el costo de la renta.
     //El costo de la renta como un double.
    double getRenta();

    //Establece el estado de disponibilidad.
    //disp El nuevo estado (true o false).
    void setDisponible(bool disp);
    //Verifica si el inmueble está disponible.
    //true si está disponible, false en caso contrario.
    bool isDisponible();

    //Establece el tipo de inmueble.
    //t El nuevo tipo (ej: "Casa").
    void setTipo(string &t);
    //Obtiene el tipo de inmueble.
    //return El tipo como un string.
    string getTipo();

                        //Muestra toda la información del inmueble en la consola.
    void mostrarInfo();
};

#endif

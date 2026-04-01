#include "Inmueble.h"
#include <iostream>
#include <string>
#include <clocale>

using namespace std;

int main()
{
    setlocale(LC_CTYPE,"spanish");
// Aquí declaramos los constructores previamente hechos, estático y dinámico
    Inmueble inmuebleEstatico;
    Inmueble *inmuebleDinamico = nullptr; //nullptr establece que el puntero esta vacio para evitar que contenga basura al crear uno nuevo

    int opcion = -1;

    do {
        cout<<"***********************************"<<endl;
        cout<<"\nMenú\n";
        cout<<"0 - Salir\n";
        cout<<"1 - Mostrar plantilla de inmueble\n";
        cout<<"2 - Agregar un inmueble\n";                 //Aquí se le da entrada al usuario para elegir una opción
        cout<<"3 - Mostrar inmueble\n";
        cout<<"4 - Editar plantilla de inmueble\n";
        cout<<"5 - Editar inmueble agregado\n";
        cout<<"Elige una opción: ";

        if (!(cin>>opcion)) {
            cin.clear(); //En esta parte si detecta algo más que no sea un número entero mandará un mensaje de error y con el 'continue' volverá a mostrar el menú
            cin.ignore();
            cout<<"Entrada inválida.\n";
            continue;
        }

        cin.ignore();

        switch (opcion) {
            case 0: //Este case borra el constructor dinámico si es que se creó uno y después cierra el programa
                if (inmuebleDinamico != nullptr) {
                    delete inmuebleDinamico;
                    inmuebleDinamico = nullptr;
                }
                cout<<"Saliendo...\n";
                break;

            case 1: //Este case se encarga de mostrar la plantilla de cómo se verá la info de tu inmueble
                cout<<"\n[PLANTILLA DE INMUEBLE]\n";
                inmuebleEstatico.mostrarInfo();
                break;

            case 2: { //En este case se agrega el inmueble con el constructor dinámico
                string tipo, direccion;
                double renta;
                int dispoInt;
                bool disponible;

                cout<<"\nIntroduce tipo de inmueble: ";
                getline(cin, tipo); //Agarra el nombre del inmueble

                cout<<"Introduce dirección: ";
                getline(cin, direccion);    //Agarra la dirección del inmueble

                cout<<"Introduce precio de renta: ";

                cin>>renta; //Agarra el precio de la renta

                while (cin.fail()) { //El punto fail reprenta que si es un número negativo será verdadero y se ejecutará el if
                    cin.clear();
                    cin.ignore();
                    cout<<"Valor inválido. Introduce la renta (número): ";
                    cin>>renta;
                }
                cin.ignore();

                cout<<"¿Disponible? (1=Sí, 0=No): "; //Se guarda si esta disponible o no

                cin>>dispoInt;

                while(cin.fail() || (dispoInt != 0 && dispoInt != 1)) { //si es negativo o no es 1 o 0 se ejecutará el while, si no seguirá normalmente

                    cin.clear();
                    cin.ignore();
                    cout<<"Entrada inválida. Por favor ingresa 1 o 0.\n";
                    cin>>dispoInt;
                }

                disponible = (dispoInt == 1); // si digitas 1 el resultado será true y estará disponible gracias al booleano y si detecta 0 dira no disponible

                if (inmuebleDinamico != nullptr) {
                    delete inmuebleDinamico;
                    inmuebleDinamico = nullptr;
                    cout<<"Se borró el inmueble anterior antes de crear uno nuevo.\n";
                }

                inmuebleDinamico = new Inmueble(tipo, direccion, renta, disponible); //En esta parte se guardan todos los dtos del inmueble dinámico
                cout<<"Inmueble agregado correctamente.\n";
                break;
            }

            case 3:
                if (inmuebleDinamico == nullptr) { // Esto verifica si hay un inmueble dinámico hecho para mostrar informacion
                    cout<<"No hay ningún inmueble creado";
                } else {
                    cout<<"\n[INMUEBLE CREADO INFO]\n";
                    inmuebleDinamico->mostrarInfo(); //Se usa la -> porque el constructor se llama igual que el dinámico
                }
                break;

            case 4: { //Aquí editamos la plantilla predefinida (Constructor estático)

                string nuevaDireccion;
                double nuevaRenta;

                cout<<"\nEditar Plantilla:\n";
                cout<<"Introduce nueva dirección: ";
                getline(cin, nuevaDireccion);
                cout<<"Introduce nuevo precio de renta: ";

                cin>>nuevaRenta;

                while (cin.fail()) {
                    cin.clear();
                    cin.ignore();
                    cout<<"Valor inválido. Introduce la renta (número): ";
                    cin>>nuevaRenta;
                }
                cin.ignore();

                inmuebleEstatico.setDireccion(nuevaDireccion); //Aquí se guardan en el constructor y de paso en los datos privados
                inmuebleEstatico.setRenta(nuevaRenta);
                cout<<"Plantilla de inmueble modificado.\n";
                break;
            }

            case 5: //Aqui se modifica tu mueble dinámico previamente hecho, en caso de que no exista esta el if de abajo que te impide editar algo que no existe
                if (inmuebleDinamico == nullptr) {
                    cout<<"\nNo hay un inmueble para editar\n";
                } else {

                    string nuevoTipo;
                    int dispoInt;
                    bool nuevaDisponibilidad;

                    cout<<"\nEditar inmueble creado:\n";
                    cout<<"Introduce nuevo tipo: ";
                    getline(cin, nuevoTipo);
                    cout<<"¿Disponible? (1=Sí, 0=No): ";
                    cin>>dispoInt;

                    while(cin.fail() || (dispoInt != 0 && dispoInt != 1)) {

                        cin.clear();
                        cin.ignore();
                        cout<<"Entrada inválida. Por favor ingresa 1 o 0.\n";
                        cin>>dispoInt;
                    }

                    cin.ignore();
                    nuevaDisponibilidad = (dispoInt == 1);

                    inmuebleDinamico->setTipo(nuevoTipo);
                    inmuebleDinamico->setDisponible(nuevaDisponibilidad); //Aquí se guardan en el constructor y de paso en los datos privados
                    cout<<"Inmueble modificado correctamente.\n";
                }
                break;

            default:
                cout<<"\nOpción no reconocida. Intenta de nuevo.\n"; //En caso que la opción introducida no se valida se ejecutará este mensaje
                break;
        }

    } while (opcion != 0); // Se seguirá ejecutando el código y si detecta un 0 lo detendrá

    return 0;
}

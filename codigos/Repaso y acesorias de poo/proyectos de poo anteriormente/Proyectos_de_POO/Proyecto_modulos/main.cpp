#include <iostream>
#include <string>
#include <clocale>
#include "Servicios.h"
using namespace std;

int main()
{
    Servicios ser;
    int q;
    int opc;
    setlocale(LC_CTYPE, "spanish");

    do{
        cout << "\n===== MENÚ DEL SISTEMA DE COMPETENCIAS =====\n";
        cout << "1. Mostrar monito\n";
        cout << "2. Sonrisas\n";
        cout << "3. omprar flores\n";
        cout << "4. Costo de ramos\n";
        cout << "5. Cual es tu humor\n";
        cout << "0. Salir\n";
        cout << "Opción: ";
        cin >> opc;
        cin.ignore();
    switch (opc) {
    case 1: {
    ser.monito();
    break;
}
    case 2: {
    ser.sonreir(5);
    break;
}
    case 3: {
    int q=ser.vendedorFlores();
    cout<< "\nEl vendedor vendio "<<q<<" flores"<< endl;
    break;
}
    case 4: {
    float costo = ser.ramosFlores(q);
    cout<<"\nTu ramo de flores cuesta $"<<costo<<endl;
    break;
}
    case 5: {
    char boca;
    cout<<"¿De que humor estas?. Escribe un simbolo: :D, :), :(\n";
    cin>>boca;
    int intensidad;
    cout<<"Marca la intensidad de tu emocion del 1 al 10\n";
    cin>>intensidad;
    ser.emociones(intensidad, boca);
    break;
    }
    case 0:{
    cout<<"saliendo del sistema"<<endl;
    break;
    }
default:
    cout<<"que verga pusiste papi"<<endl;
    }
    }while (opc != 0);

    return 0;}

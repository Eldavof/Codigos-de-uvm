#include <iostream>
#include <clocale>
#include <vector>
#include <string>
#include <Windows.h>
#include <fstream>   // Para manejo de archivos
#include <algorithm> // Para ordenar (sort)

using namespace std;

// --- Funciones de Persistencia ---

void cargar_libros(vector<string>& lista) {
    ifstream archivo("biblioteca.txt");
    string linea;
    if (archivo.is_open()) {
        while (getline(archivo, linea)) {
            if(!linea.empty()) lista.push_back(linea);
        }
        archivo.close();
        cout << "[Sistema] Se han cargado tus novelas guardadas.\n";
    }
}

void guardar_libros(const vector<string>& lista) {
    ofstream archivo("biblioteca.txt");
    if (archivo.is_open()) {
        for (const string& libro : lista) {
            archivo << libro << endl;
        }
        archivo.close();
        cout << "[Sistema] Biblioteca guardada exitosamente.\n";
    } else {
        cout << "[Error] No se pudo guardar el archivo.\n";
    }
}

// --- Función Principal ---

int main()
{
    SetConsoleCP(1252);
    SetConsoleOutputCP(1252);
    std::vector<std::string> lista_lectura;
    std::string titulo_novela;

    // Cargar datos al iniciar
    cargar_libros(lista_lectura);

    int opc;

    do{
        cout << "\n********** Menú **********\n";
        cout << " 0. Salir y Guardar.\n";
        cout << " 1. Agregar novela al final.\n";
        cout << " 2. Ver número actual de novelas.\n";
        cout << " 3. Acceder a una novela específica.\n";
        cout << " 4. Eliminar última novela.\n";
        cout << " 5. Mostrar todos los libros.\n";
        cout << " 6. Eliminar todo.\n";
        cout << " 7. Eliminar por posición.\n";
        cout << " 8. Eliminar por nombre.\n";
        cout << " 9. Ordenar alfabéticamente (A-Z).\n"; // Nueva opción
        cout << " 10. Editar título de una novela.\n";    // Nueva opción
        cout << "**************************\n";

        cout << "Elige una opción: ";
        cin >> opc;
        cin.ignore(); // Limpiar buffer

        switch(opc){
        case 1:
            cout<<"Escribe el título de la novela a agregar: ";
            getline(cin,titulo_novela);
            lista_lectura.push_back(titulo_novela);
            cout<<"\n'"<<titulo_novela<<"' agregado.\n";
            break;

        case 2:
            cout<<"Tienes "<<lista_lectura.size()<<" novelas en la lista.\n";
            break;

        case 3:{
            int posicion;
            cout<<"Escribe el número de la novela que quieres ver: ";
            cin>>posicion;
            cin.ignore();
            if(posicion>0 && posicion<=lista_lectura.size()){
                cout << "Libro: " << lista_lectura[posicion-1]<<"\n";
            }else{
                cout<<"Posición inválida.\n";
            }
            break;}

        case 4:
            if(lista_lectura.empty()){
                cout<<"No hay nada para eliminar.\n";
            }else{
                string titulo_eliminado=lista_lectura.back();
                lista_lectura.pop_back();
                cout<<"\n'"<<titulo_eliminado<<"' eliminado.\n";
            }
            break;

        case 5:
            cout<<"******** Tu Biblioteca ********\n";
            if(lista_lectura.empty()){
                cout<<"(Vacía)\n";
            }else{
                for(int i=0; i<lista_lectura.size();i++){
                    cout<<i+1<<". "<<lista_lectura[i]<<"\n";
                }
            }
            break;

        case 6:
            lista_lectura.clear();
            cout<<"¡Biblioteca vaciada por completo!\n";
            break;

         case 7:{
            int pos;
            cout<<"Ingresa la posición a eliminar: ";
            cin>>pos;
            cin.ignore();
            if(pos > 0 && pos <= lista_lectura.size()){
                string eliminado = lista_lectura[pos-1];
                lista_lectura.erase(lista_lectura.begin() + (pos-1));
                cout<<"Se eliminó: "<<eliminado<<"\n";
            }else{
                cout<<"Posición inválida\n";
            }
            break;}

         case 8:{
            string nombre;
            cout<<"Ingresa el nombre exacto a eliminar: ";
            getline(cin, nombre);
            bool encontrado = false;
            for(int i = 0; i < lista_lectura.size(); i++){
                if(lista_lectura[i] == nombre){
                    lista_lectura.erase(lista_lectura.begin() + i);
                    cout<<"Se eliminó: "<<nombre<<"\n";
                    encontrado = true;
                    break;
                }
            }
            if(!encontrado) cout<<"No se encontró ese libro.\n";
            break;}

        case 9: // ORDENAR
            if(lista_lectura.empty()){
                cout << "La lista está vacía, no se puede ordenar.\n";
            } else {
                sort(lista_lectura.begin(), lista_lectura.end());
                cout << "¡Lista ordenada alfabéticamente!\n";
            }
            break;

        case 10: // EDITAR
            {
                int p;
                cout << "Ingresa la posición del libro a editar: ";
                cin >> p;
                cin.ignore();

                if(p > 0 && p <= lista_lectura.size()){
                    cout << "Título actual: " << lista_lectura[p-1] << endl;
                    cout << "Nuevo título: ";
                    string nuevo_titulo;
                    getline(cin, nuevo_titulo);
                    lista_lectura[p-1] = nuevo_titulo;
                    cout << "¡Título actualizado correctamente!\n";
                } else {
                    cout << "Posición inválida.\n";
                }
            }
            break;

        case 0:
            guardar_libros(lista_lectura);
            cout << "Saliendo...\n";
            break;

        default: cout<<"Opción no válida.\n";
        }
    }while(opc!=0);
    return 0;
}

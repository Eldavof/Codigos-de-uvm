#include <iostream>
#include "Tienda.h"
#include <vector>
#include <string>
using namespace std;

int main()
{
    int opc=0;
    do{
        cout<<"\n0-salir\n1-Usuario\n2-Administrador\n";
        cin>>opc;
        switch(opc){

    case 0:{

    //delete
    break;
    }

    case 1:{

    //llevar al menu usuario
    break;
    }

    case 2:{

    //llevar al menu administrador
    break;
    }

    default:{

        cout<< "Esa opcion no es valida" << endl;
        return 7;
    }

        }
} while (opc!=0);

return 0;
}

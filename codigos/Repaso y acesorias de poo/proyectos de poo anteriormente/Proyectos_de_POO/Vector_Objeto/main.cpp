#include <iostream>
#include <info.h>
#include <vector>

using namespace std;

int menu();
void captura(info* obj);
float asignarBk(float prome);

int main(){

    int rsp;
    vector <info*> vec;

    do{


        rsp=menu();
        switch(rsp){

        case 1:{

                info*q;
                q=new info();
                captura(q);
                q->mostrarDatos();
                vec.push_back(q);
                }
                break;
        case 2:{

                for (info*x:vec){
                    x->mostrarDatos();
                }

                }
                break;

        case 3: {
                int i, matricula, t, buscar;
                cout<<"Dame el numero de matricula a buscar en el vector"<<endl;
                cin>>matricula;
                buscar=vec.size();


                }

        }
    }

}

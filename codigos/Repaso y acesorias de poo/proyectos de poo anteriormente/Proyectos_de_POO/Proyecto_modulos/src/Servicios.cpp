#include "Servicios.h"
#include <iostream>
#include <clocale>
using namespace std;

Servicios::Servicios()
{
    cout<<"\nServicios activos\n";
    setlocale(LC_CTYPE, "spanish");
}

Servicios::~Servicios()
{
    cout<<"\nEl servidor a mamado";
}


void Servicios::sonreir(int veces){
int vc;
cout<<"\n";
for(vc=1;vc<= veces; vc++){
    cout<<"  :)  ";
}
cout<<"\n----------\n";
}
void Servicios::monito(){
cout<<R"(
    _
   /_\
   0 0
    u
  /I I\
 / I I \
   I I
  /   \
)" <<endl;
}
void Servicios::emociones(int veces, char boca){
int vc;
cout<<"\n";
for(vc=1;vc<= veces;vc++){
    cout<<" :"<<boca<<" ";
}
cout<<"\n------------\n";
}

int Servicios::vendedorFlores(){
int res=1;
int conta=0;
do{
    cout<<"\n@->--\n";
    conta++;
    cout<<"¿Quieres otra flor? 1 es simon 2 es negros son tus ojos\n";
    cin>>res;
}while(res==1);
cout<<"\n pediste"<<conta<<" flores\n";
return conta;
}

float Servicios::ramosFlores(int q){
    int res=1, conta=0;
    for(conta=0;conta<q;conta++){
        cout<<"\n@->--\n";
    }
    cout<<"Cada flor cuesta $40.50\n";
    return conta*40.50;
}

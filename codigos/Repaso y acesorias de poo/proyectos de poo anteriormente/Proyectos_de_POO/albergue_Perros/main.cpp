#include <iostream>
#include <Refugio.h>

int main()
{
    int perros, i, sal;
    string nomb, ado;

    Refugio Hogar1("Refugio UVM CT");

    cout<<"cuantos perros llegarn?"<<endl;
    cin>>perros;
    for(i=0;i<perros;i++){

        cout<<"Nombre del perro:";
        cin>>nomb;

        cout<<("\nEstado de salud (1 al 10): ");
        cin>>sal;
        Perro* p=new perros("", nomb, sal);
        hogar1.recibirPerro(p);
    }
    cout<<"\n Lista de perros que quiere adoptar"<<endl;
    cin>>ado;
    Perro *p=hogar1.buscarPerro(ado);
    if(p!=nullptr){

        hogar1.darEnAdopcion(*p);
        cout<<"El perro que adopta es "<<ado<<endl;
    } else {

    cout<<"No hay perros pa adoptar";
    }
}

#include <iostream>
#include <string>
#include "Gente.h"
using namespace std;

int main()
{
    Gente *G;

    G=new Gente ("David",57);

    (*G).mostrar();

    delete G;

    return 0;
}

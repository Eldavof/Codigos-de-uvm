#include <iostream>
#include <string>
using namespace std;
#include "Profesor.h"
#include "ProfeTiempoC.h"
#include "Empleado.h"
#include "EmpleadoCaja.h"

int main()
{
    ProfeTiempoC pro;
    pro.darConferencia();

    pro.prepararClase();

    Empleado x("Ana Suarez");
    x.capacitarse();

    EmpleadoCaja w("Juan Solis");
    w.capacitarse();
    w.cobrar();

    return 0;
}

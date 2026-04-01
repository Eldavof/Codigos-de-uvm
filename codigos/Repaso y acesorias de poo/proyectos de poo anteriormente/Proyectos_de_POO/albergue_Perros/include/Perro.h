#include <string>
using namespace std;

class Perro
{
    public:
        perro(string du, string no, int sal);
        void ladrar();
        void comer();
        void enfermar();
        string getNombre();
        bool comparar(Perro p);
        string getdueno();
        int getTiempo();
        int getSalud();
    protected:

    private:
        int tiempo;
        string dueno;
        string nombre;
        int salud;
};

#include <stdio.h>
#include <unistd.h>

int main() {
    printf("Proceso raíz iniciando...\n");

    for(int i = 0; i < 5; i++) {
        if(fork() == 0) {
            printf("[HIJO %d] Creado en la iteración %d (PID: %d)\n", i+1, i, getpid());
            // El hijo debe salir del ciclo para no crear sus propios hijos (opcional)
            _exit(0);
        }
    }

    // El padre espera un poco para ver los mensajes de sus hijos
    sleep(1);
    printf("[PADRE] He creado a todos mis hijos.\n");
    return 0;
}

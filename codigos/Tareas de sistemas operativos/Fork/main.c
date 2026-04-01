#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

int main() {
    pid_t child_pid;
    int variable_local = 0;

    printf("Proceso principal (Padre) iniciando. PID: %d\n", getpid());

    // Llamada al sistema para bifurcar el proceso
    child_pid = fork();

    if (child_pid < 0) {
        // Error en la creación del proceso
        fprintf(stderr, "Error al crear el proceso hijo\n");
        return 1;
    }

    if (child_pid == 0) {
        // --- BLOQUE DEL HIJO ---
        // fork() devuelve 0 al proceso hijo
        variable_local = 1;
        printf("\n[HIJO] Hola, soy el proceso hijo.");
        printf("\n[HIJO] Mi PID es: %d", getpid());
        printf("\n[HIJO] El PID de mi padre es: %d", getppid());
        printf("\n[HIJO] Valor de variable_local: %d\n", variable_local);
    } else {
        // --- BLOQUE DEL PADRE ---
        // fork() devuelve el PID del hijo al padre
        variable_local = 2;
        printf("\n[PADRE] Hola, soy el proceso padre.");
        printf("\n[PADRE] Mi PID es: %d", getpid());
        printf("\n[PADRE] El PID de mi hijo es: %d", child_pid);
        printf("\n[PADRE] Valor de variable_local: %d\n", variable_local);

        // Espera opcional para ver la concurrencia o evitar procesos zombie
        sleep(1);
    }

    // Código que ambos procesos ejecutan tras la bifurcación
    printf("\n[COMUN] Finalizando proceso %d. Valor final de variable: %d\n", getpid(), variable_local);

    return 0;
}

#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h> // Necesaria para wait()
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("[HIJO] Trabajando duro por 3 segundos...\n");
        sleep(3);
        printf("[HIJO] He terminado mi labor.\n");
    } else {
        printf("[PADRE] Esperando a que mi hijo termine para continuar...\n");
        wait(NULL); // El padre se detiene hasta que el hijo termina
        printf("[PADRE] Mi hijo ya terminó, ahora puedo cerrar el programa.\n");
    }
    return 0;
}

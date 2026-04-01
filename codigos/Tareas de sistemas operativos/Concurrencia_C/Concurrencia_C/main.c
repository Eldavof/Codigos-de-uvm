#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

int buffer;
sem_t mutex;
sem_t PuedeProducir;
sem_t PuedeConsumir;

void* productor (void* arg) {

    int i;
    for(i =1; i<=5; i++){

        sem_wait(&PuedeProducir);
        sem_wait(&mutex);
        buffer = i;
        printf("[Productor] puse el dato: %d\n", buffer);
        sem_post(&mutex);
        sem_post(&PuedeConsumir);
        sleep(1);
    }
    return NULL;
}

void* consumidor(void* arg){

    int i;
    for (i=1; i<=5; i++){

        sem_wait(&PuedeConsumir);
        sem_wait(&mutex);
        printf("[Consumidor] lei el dato %d\n", buffer);
        sem_post(&mutex);
        sem_post(&PuedeProducir);
        sleep(1);
    }
    return NULL;
}

int main(){

    pthread_t hiloProductor, hiloConsumidor;
    sem_init(&mutex, 0, 1);
    sem_init(&PuedeProducir, 0, 1);
    sem_init(&PuedeConsumir, 0, 0);
    printf("Sistema linux concurrencia iniciada\n");
    pthread_create(&hiloProductor, NULL, productor, NULL);
    pthread_create(&hiloConsumidor, NULL, consumidor, NULL);

    pthread_join(hiloProductor, NULL);
    pthread_join(hiloConsumidor, NULL);

    printf("Tarea finalizada con exito\n");

    return 0;
}

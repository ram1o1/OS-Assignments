#include <stdio.h>
#include <pthread.h>

void *print_info(void *arg) {
    int local_var = 5;
    printf("Thread ID: %lu | Address of local_var: %p\n", pthread_self(), &local_var);
    return NULL;
}

int main() {
    pthread_t threads[4];
    int i;

    for (i = 0; i < 4; i++) {
        pthread_create(&threads[i], NULL, print_info, NULL);
    }

    for (i = 0; i < 4; i++) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}
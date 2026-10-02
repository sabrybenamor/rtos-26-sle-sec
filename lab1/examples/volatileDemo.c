/*
 * volatileDemo.c - why a flag shared with a signal handler must be volatile.
 *
 * The handler sets `tick` asynchronously. main() busy-waits on it.
 *
 *   make volatile-demo     builds and runs both versions at -O2
 *
 * Without volatile, the compiler sees that nothing inside `while (!tick) {}`
 * can change `tick`, so it reads it ONCE before the loop and spins forever.
 * Look at the generated code yourself:
 *
 *   gcc -O2 -S examples/volatileDemo.c -o - | grep -A3 'tick(%rip)'
 *
 * You will find something like:
 *
 *       movl  tick(%rip), %eax     <- the only read of tick
 *       testl %eax, %eax
 *       jne   .L4
 *   .L5:
 *       jmp   .L5                  <- infinite loop, tick is never re-read
 *
 * Build with -DUSE_VOLATILE and the loop re-reads memory on every iteration.
 */

#include <signal.h>
#include <stdio.h>
#include <unistd.h>

#ifdef USE_VOLATILE
static volatile sig_atomic_t tick = 0;
#else
static int tick = 0;            /* BUG: shared with a handler, not volatile */
#endif

static void onAlarm(int signo) {
    (void)signo;
    tick = 1;
}

int main(void) {
    signal(SIGALRM, onAlarm);
    alarm(1);                   /* SIGALRM in 1 second */

    printf("waiting for SIGALRM...\n");
    fflush(stdout);

    while (!tick) {
        /* busy-wait */
    }

    printf("tick received, leaving the loop\n");
    return 0;
}

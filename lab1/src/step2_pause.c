/**
 * Step 2 - Cyclic executive: timer + pause().
 *
 * Start from a copy of your step1_busywait.c. Change only the way main()
 * waits for the next tick: it must sleep (pause()) instead of spinning.
 * Everything else stays the same.
 *
 * Check:  make check2
 */

#include <sys/time.h> /* for calling setitimer */
#include <signal.h>   /* for calling signal, sig_atomic_t */
#include <stdio.h>    /* for calling printf */
#include <unistd.h>   /* for calling pause */
#include "frameTable.h"

// Paste your Step 1 code here, then modify the wait.

int main(void) {
    // ...

    return 0;
}

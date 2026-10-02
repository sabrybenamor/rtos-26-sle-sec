/**
 * Step 3 - Cyclic executive: timer + sigprocmask/sigsuspend.
 *
 * Start from a copy of your step2_pause.c. Remove the race between testing
 * the tick counter and calling pause() (Q5): block SIGALRM while you test,
 * then unblock it and sleep in one atomic operation.
 * See sigprocmask(2) and sigsuspend(2).
 *
 * Check:  make check3
 */

#include <sys/time.h> /* for calling setitimer */
#include <signal.h>   /* for calling signal, sig_atomic_t, sigsuspend */
#include <stdio.h>    /* for calling printf */
#include "frameTable.h"

// Paste your Step 2 code here, then fix the race.

int main(void) {
    // ...

    return 0;
}

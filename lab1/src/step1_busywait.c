/**
 * Step 1 - Cyclic executive: timer + BUSY-WAIT.
 *
 * A periodic timer (setitimer, period FRAME_US) raises SIGALRM at every frame
 * boundary. The handler records the tick. main() busy-waits for each tick,
 * then runs the jobs of the current frame from the frame table.
 * Run exactly N_HYPERPERIODS hyperperiods, then return 0.
 *
 * Start from examples/timerExample.c.   Check:  make check1
 */

#include <sys/time.h> /* for calling setitimer */
#include <signal.h>   /* for calling signal, sig_atomic_t */
#include <stdio.h>    /* for calling printf */
#include "frameTable.h"

// Global variables
// Anything written by the handler and read by main() must be
// `volatile sig_atomic_t` (see README, "The volatile lesson").
// ...

// Function prototypes
// ...

int main(void) {
    // Add contents
    // ...

    return 0;
}

// Functions definitions
// ...

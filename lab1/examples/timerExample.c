/*
 * Example of interval timer usage: a periodic "tick" delivered by SIGALRM.
 *
 * Build and run:  gcc -O2 -Wall examples/timerExample.c -o timerExample && ./timerExample
 *
 * main() waits for each tick with a BUSY-WAIT: it keeps testing `ticks` until
 * it changes. This is the starting point of Step 1 of the lab. Step 2 asks
 * you to replace it with something that does not burn the CPU.
 */

#include <sys/time.h>   /* for calling setitimer */
#include <signal.h>     /* for calling signal, sig_atomic_t */
#include <stdio.h>      /* for calling printf */

#define INTERVAL_US 500000  /* timer period: 500 ms */
#define N_TICKS     10      /* stop after this many ticks */

/* Handler prototype: a signal handler MUST take an int (the signal number).
 * Casting a void(void) function to void(*)(int) is undefined behaviour. */
static void onTimer(int signo);

/* Shared between the handler and main():
 *  - volatile:     main() must re-read it from memory every time; otherwise
 *                  the compiler may keep a stale copy in a register and the
 *                  busy-wait below never ends (see examples/volatileDemo.c).
 *  - sig_atomic_t: an integer type that is read/written in one indivisible
 *                  access, so main() never sees a half-written value.
 * Only the handler writes it; main() only reads it. */
static volatile sig_atomic_t ticks = 0;

int main(void) {
  struct itimerval timer;

  // Install the timer handler: upon SIGALRM, the kernel calls onTimer().
  signal(SIGALRM, onTimer);

  // First expiry after INTERVAL_US ...
  timer.it_value.tv_sec = 0;
  timer.it_value.tv_usec = INTERVAL_US;
  // ... then every INTERVAL_US. The kernel re-arms the timer from its own
  // expiry time, so the period does not drift with the work done in main().
  timer.it_interval.tv_sec = 0;
  timer.it_interval.tv_usec = INTERVAL_US;

  // ITIMER_REAL counts wall-clock time and delivers SIGALRM.
  // (ITIMER_VIRTUAL would count only CPU time of this process, SIGVTALRM.)
  setitimer(ITIMER_REAL, &timer, NULL);

  for (sig_atomic_t seen = 0; seen < N_TICKS; ) {
    // Busy-wait for the next tick.
    while (ticks == seen) {
      /* nothing: just test again */
    }
    seen++;
    if (ticks > seen) {
      printf("missed %d tick(s)!\n", (int)(ticks - seen));
      seen = ticks;
    }
    printf("tick %d received, do the job...\n", (int)seen);
    // calls ...
  }

  return 0;
}

static void onTimer(int signo) {
  (void)signo;
  ticks++;
  // Do not call printf() here: it is not async-signal-safe. If the signal
  // interrupts a printf() in main(), the stdio buffer can be corrupted.
  // Keep handlers short: bump a counter, and do the work in main().
}

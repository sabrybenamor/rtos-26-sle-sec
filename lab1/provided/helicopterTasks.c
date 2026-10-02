/*
 * Mock implementations of the flight controller jobs.
 * Do not modify this file: each job prints a timestamped trace line that
 * scripts/check_trace.py uses to check job order AND frame timing, then
 * keeps the CPU busy for its WCET (see helicopterTasks.h).
 */

#include <stdio.h>
#include <time.h>
#include "helicopterTasks.h"

static long long now_us(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)ts.tv_sec * 1000000LL + ts.tv_nsec / 1000L;
}

static void job(const char *name, long wcet_us) {
    long long start = now_us();
    printf("%lld.%06lld *** %s\n", start / 1000000LL, start % 1000000LL, name);
    fflush(stdout);
    while (now_us() - start < wcet_us) {
        /* simulate the computation */
    }
}

/* Validate sensor data and select data source. Rate 180 Hz. */
void dataValidation(void)       { job("dataValidation",       WCET_DV_US);  }

/* Keyboard input, data normalization, tracking reference update. Rate 30 Hz. */
void keyboardDataTracking(void) { job("keyboardDataTracking", WCET_KDT_US); }

/* Outer pitch, roll and yaw/collective control loops. Rate 30 Hz. */
void controlOuterLoops(void)    { job("controlOuterLoops",    WCET_COL_US); }

/* Inner pitch and roll/collective control loops. Rate 90 Hz. */
void controlInnerLoops(void)    { job("controlInnerLoops",    WCET_CIL_US); }

/* Inner yaw loop, then output commands. Rate 180 Hz. */
void computeNComd(void)         { job("computeNComd",         WCET_CNC_US); }

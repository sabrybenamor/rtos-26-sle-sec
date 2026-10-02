/*
 * Helicopter flight controller: the task set (job prototypes, periods, WCETs).
 * Do not modify this file: the checker reads the same values.
 *
 * The frame size and the hyperperiod are NOT given: computing them is part of
 * the lab (Step 0). Define them yourself, in frameTable.h.
 */

#ifndef HELICOPTER_TASKS_H
#define HELICOPTER_TASKS_H

/* Time is slowed down by TIME_SCALE so the schedule is observable and can be
 * checked on an ordinary (non real-time) Linux machine. The 180/90/30 Hz rates
 * of the textbook become 20/10/3.33 Hz; the ratios between them are unchanged.
 * All values below are already scaled. */
#define TIME_SCALE      9

/* Period of each job, in (scaled) microseconds. Deadline = period. */
#define PERIOD_DV_US    (1000000L * TIME_SCALE / 180)  /* dataValidation,       180 Hz */
#define PERIOD_KDT_US   (1000000L * TIME_SCALE / 30)   /* keyboardDataTracking,  30 Hz */
#define PERIOD_COL_US   (1000000L * TIME_SCALE / 30)   /* controlOuterLoops,     30 Hz */
#define PERIOD_CIL_US   (1000000L * TIME_SCALE / 90)   /* controlInnerLoops,     90 Hz */
#define PERIOD_CNC_US   (1000000L * TIME_SCALE / 180)  /* computeNComd,         180 Hz */

/* Worst-case execution time of each job, in (scaled) microseconds.
 * The mock jobs in helicopterTasks.c really consume this much time. */
#define WCET_DV_US       2000   /* dataValidation       */
#define WCET_KDT_US      4000   /* keyboardDataTracking */
#define WCET_COL_US      9000   /* controlOuterLoops    */
#define WCET_CIL_US      6000   /* controlInnerLoops    */
#define WCET_CNC_US      3000   /* computeNComd         */

/* Run the cyclic executive for exactly this many hyperperiods, then stop. */
#define N_HYPERPERIODS   5

void dataValidation(void);
void keyboardDataTracking(void);
void controlOuterLoops(void);
void controlInnerLoops(void);
void computeNComd(void);

#endif

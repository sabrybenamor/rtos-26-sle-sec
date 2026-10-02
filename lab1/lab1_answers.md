# Lab 1 - Answers

> Answer in your own words. Paste outputs exactly as printed.

---

## Step 0 - Frame size and frame table

**Q1 - Frame size.** Using `provided/helicopterTasks.h`, show your computations:

a. The hyperperiod H and the utilization U.

b. The frame size f: the largest one that satisfies the three constraints (f ≥ max eᵢ; f divides H; 2f − gcd(pᵢ, f) ≤ pᵢ). Show that your f satisfies them.

c. The number of frames per hyperperiod and in the whole run, and the expected run length.

**Q2 - Frame table.** Give the jobs and the load of each frame, and explain where you placed the low-rate jobs.

| Frame | Jobs | Load (ms) |
|-------|------|-----------|
|       |      |           |

---

## Steps 1 and 2 - Busy-wait and `pause()`

**Q3 - volatile.** Remove `volatile` in `step1_busywait.c` and `step2_pause.c`, run `make check1` and `make check2`, and paste both outputs. Why does Step 1 hang and Step 2 still pass? Why is Step 2 still wrong? Put `volatile` back afterwards.

**Q4 - CPU load and drift.** Compare the `CPU load` of `make check1` and `make check2`. Does the Step 2 value match the load you predict from your frame table? If each frame were started by `usleep(FRAME_US)` after the jobs instead of by the timer, how long would the run last? Why does the timer not drift?

---

## Step 3 - The race in `pause()`

**Q5.** Which sequence of events makes the `pause()` version miss a tick? How do `sigprocmask` and `sigsuspend` fix it?

---

**Q6 - AI use.** Did you use an AI assistant? If so, for what? (Declared use is not penalized; undeclared use is.)

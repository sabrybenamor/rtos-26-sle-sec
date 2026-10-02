#!/usr/bin/env python3
"""Check a Lab 1 execution trace: frame table AND frame timing.

Reads the program's output on stdin. Every job prints a line
    <seconds>.<microseconds> *** <jobName>
(from helicopterTasks.c). Other lines are ignored.

The task set (periods, WCETs, number of hyperperiods) is read from
provided/helicopterTasks.h. The expected frame size is the LARGEST frame size
that satisfies the three frame-size constraints of the lecture.

Schedule rules (any frame table that satisfies them is accepted):
  * a frame starts with dataValidation and ends with computeNComd;
  * inside a frame, jobs follow the data flow of the controller:
    dataValidation < keyboardDataTracking < controlOuterLoops
                   < controlInnerLoops < computeNComd;
  * every job runs exactly once in each of its periods (periods start at
    time 0 and are aligned on frame boundaries);
  * the table is static: every hyperperiod repeats the same frames;
  * exactly N_HYPERPERIODS hyperperiods are executed.

Timing rules:
  * median frame period ~ frame size;
  * no cumulative drift over the whole run;
  * most frames within tolerance.

CPU rule (--step 2 and 3; needs --cpu and --wall):
  * the program sleeps between frames: CPU time / wall time <= MAX_CPU_LOAD.

Exit status 0 = PASS, 1 = FAIL.
"""
import argparse
import math
import os
import re
import statistics
import sys

TOL = 0.25           # per-frame tolerance (+/- 25 %)
MIN_OK = 0.90        # at least 90 % of the frames inside it
MAX_DRIFT = 0.01     # end-to-end drift allowed (1 %)
MAX_CPU_LOAD = 0.60  # steps 2-3: CPU time / wall time

DV, KDT, COL, CIL, CNC = ("dataValidation", "keyboardDataTracking",
                          "controlOuterLoops", "controlInnerLoops",
                          "computeNComd")
ORDER = [DV, KDT, COL, CIL, CNC]
SHORT = {DV: "DV", KDT: "KDT", COL: "COL", CIL: "CIL", CNC: "CNC"}

LINE = re.compile(r"^(\d+\.\d{6}) \*\*\* (\w+)$")


def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def fmt(jobs):
    return " ".join(SHORT.get(j, j) for j in jobs)


# ---- task set, from the header ---------------------------------------------
def read_header():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "provided", "helicopterTasks.h")
    macros = {}
    for line in open(path):
        line = re.sub(r"/\*.*?\*/|//.*", "", line)
        m = re.match(r"\s*#define\s+(\w+)\s+(.+)", line)
        if m:
            macros[m.group(1)] = m.group(2).strip()

    def value(name):
        expr = re.sub(r"(\d+)L\b", r"\1", macros[name])
        expr = re.sub(r"[A-Z_]{2,}", lambda m: str(value(m.group(0))), expr)
        if not re.fullmatch(r"[\d\s()+\-*/]+", expr):
            raise ValueError(f"cannot evaluate {name} = {macros[name]}")
        return int(eval(expr))

    keys = {DV: "DV", KDT: "KDT", COL: "COL", CIL: "CIL", CNC: "CNC"}
    period = {j: value(f"PERIOD_{k}_US") for j, k in keys.items()}
    wcet = {j: value(f"WCET_{k}_US") for j, k in keys.items()}
    return period, wcet, value("N_HYPERPERIODS")


PERIOD, WCET, N_HYPERPERIODS = read_header()
H = math.lcm(*PERIOD.values())


def feasible(f):
    return (f >= max(WCET.values()) and H % f == 0 and
            all(2 * f - math.gcd(p, f) <= p for p in PERIOD.values()))


FRAME_US = max(f for f in range(1, H + 1) if H % f == 0 and feasible(f))
FRAMES_PER_HP = H // FRAME_US
N_FRAMES = FRAMES_PER_HP * N_HYPERPERIODS
# The checker splits the trace into frames at each dataValidation, and checks
# job periods as whole numbers of frames: both hold for this task set.
assert PERIOD[DV] == FRAME_US and all(p % FRAME_US == 0 for p in PERIOD.values())

# ---- arguments -------------------------------------------------------------
ap = argparse.ArgumentParser(description="Check a Lab 1 trace read on stdin.")
ap.add_argument("--step", type=int, choices=(1, 2, 3), default=2)
ap.add_argument("--cpu", type=float, nargs=2, metavar=("USER", "SYS"),
                help="CPU seconds used by the program")
ap.add_argument("--wall", type=float, help="wall-clock seconds of the run")
args = ap.parse_args()

# ---- parse and split into frames: a frame starts at each dataValidation ----
events = [(float(m.group(1)), m.group(2))
          for m in (LINE.match(l.strip()) for l in sys.stdin) if m]
if not events:
    fail("no trace lines found - did your jobs run?")

unknown = {n for _, n in events if n not in ORDER}
if unknown:
    fail(f"unknown job name(s) in trace: {sorted(unknown)}")

if events[0][1] != DV:
    fail(f"first job is {events[0][1]}; every frame must start with {DV}")
frames = []                      # list of (start_time, [job names])
for t, n in events:
    if n == DV:
        frames.append((t, []))
    frames[-1][1].append(n)

# ---- frame period first, so that later messages do not reveal it ----------
starts = [t for t, _ in frames]
gaps = [(b - a) * 1e6 for a, b in zip(starts, starts[1:])]
if not gaps:
    fail("only one frame was executed")
lo, hi = FRAME_US * (1 - TOL), FRAME_US * (1 + TOL)
med = statistics.median(gaps)
if not lo <= med <= hi:
    fail(f"your frames last {med / 1000:.1f} ms (median), which is not the "
         f"frame size this task set needs - recheck Q1 (the largest feasible "
         f"frame size) and the period of your timer")

if len(frames) != N_FRAMES:
    fail(f"{len(frames)} frames were executed, which is not {N_HYPERPERIODS} "
         f"hyperperiods - recheck the hyperperiod and the number of frames "
         f"per hyperperiod (Q1)")

# ---- per-frame structure ---------------------------------------------------
for k, (_, jobs) in enumerate(frames):
    if jobs[-1] != CNC or jobs.count(CNC) != 1:
        fail(f"frame {k} is [{fmt(jobs)}]: it must end with exactly one {CNC}")
    if len(set(jobs)) != len(jobs):
        fail(f"frame {k} is [{fmt(jobs)}]: a job appears twice in one frame")
    if [ORDER.index(j) for j in jobs] != sorted(ORDER.index(j) for j in jobs):
        fail(f"frame {k} is [{fmt(jobs)}]: wrong order inside the frame, "
             f"expected the data-flow order {fmt(ORDER)}")

# ---- static table + rates --------------------------------------------------
for k in range(FRAMES_PER_HP, N_FRAMES):
    if frames[k][1] != frames[k - FRAMES_PER_HP][1]:
        fail(f"frame {k} is [{fmt(frames[k][1])}] but frame "
             f"{k - FRAMES_PER_HP} was [{fmt(frames[k - FRAMES_PER_HP][1])}]: "
             f"a cyclic executive repeats the same frame table every hyperperiod")

table = [frames[k][1] for k in range(FRAMES_PER_HP)]
for job in (KDT, COL, CIL):
    w = PERIOD[job] // FRAME_US              # frames per period of this job
    for s in range(0, FRAMES_PER_HP, w):
        c = sum(table[k].count(job) for k in range(s, s + w))
        if c != 1:
            fail(f"{job} runs {c} time(s) in frames {s}-{s + w - 1}, which "
                 f"form one of its periods: it must run exactly once")

# ---- timing quality --------------------------------------------------------
# Catches "sleep one frame AFTER the jobs" (cumulative drift). Checked before
# the per-frame tolerance: with this bug, the longest frames (frame size + its
# load) also fall outside the tolerance, and the student must see the drift
# message, not a generic one. A periodic timer does not drift.
total = (starts[-1] - starts[0]) * 1e6
expected_total = FRAME_US * (len(starts) - 1)
drift = (total - expected_total) / expected_total
if abs(drift) > MAX_DRIFT:
    fail(f"the run is {drift:+.1%} longer than {len(starts) - 1} frames: the "
         f"frames drift - they must be started by a periodic timer, not by "
         f"sleeping after the jobs")

ok = sum(1 for g in gaps if lo <= g <= hi)
if ok < MIN_OK * len(gaps):
    fail(f"only {ok}/{len(gaps)} frames have the right length (+/-{TOL:.0%}) "
         f"- the frame timing is not periodic")

# ---- CPU usage: busy-wait (step 1) vs sleeping until the tick (2, 3) ------
cpu_msg = ""
if args.cpu is not None and args.wall:
    load = sum(args.cpu) / args.wall
    cpu_msg = f" | CPU load {load:.0%}"
    if args.step >= 2 and load > MAX_CPU_LOAD:
        fail(f"your program keeps the CPU {load:.0%} busy - it busy-waits "
             f"between frames. From Step 2 on, it must sleep until the next "
             f"tick (README, Step 2)")

print(f"PASS (step {args.step}): {N_FRAMES} frames | median frame "
      f"{med:.0f} us | {ok}/{len(gaps)} in tolerance | drift {drift:+.2%}"
      f"{cpu_msg}")
print("frame table: " + " | ".join(f"F{k}: {fmt(f)}" for k, f in enumerate(table)))

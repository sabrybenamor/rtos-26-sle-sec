#!/usr/bin/env bash
# Lab 1 checker: build one step, run it ONCE under a hard timeout, check the trace.
#
#   make check1 | check2 | check3      (or STEP=n scripts/run_and_check.sh)
#   make check                         all three steps
#
# Step 1 accepts a busy-wait; steps 2 and 3 must sleep between frames.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

STEP=${STEP:-2}
RUN_TIMEOUT=10   # seconds; a correct run takes a couple of seconds

case "$STEP" in
  1) SRC=src/step1_busywait.c ;;
  2) SRC=src/step2_pause.c ;;
  3) SRC=src/step3_sigsuspend.c ;;
  *) echo "STEP must be 1, 2 or 3"; exit 2 ;;
esac
BIN=./step$STEP

if ! make -s "step$STEP"; then
  echo "FAIL: compilation failed."
  exit 1
fi

OUTFILE=$(mktemp)
TIMEFILE=$(mktemp)
trap 'rm -f "$OUTFILE" "$TIMEFILE"' EXIT

# `time` (bash keyword) reports CPU time (user + sys) and wall time of the run.
TIMEFORMAT='%U %S %R'
{ time timeout --signal=KILL "$RUN_TIMEOUT" "$BIN" >"$OUTFILE" 2>&1 ; } 2>"$TIMEFILE"
RC=$?
OUT=$(cat "$OUTFILE")

if [ "$RC" -eq 137 ]; then
  echo "FAIL: step$STEP did not terminate within ${RUN_TIMEOUT}s."
  echo "      - it must stop after N_HYPERPERIODS hyperperiods, not loop forever;"
  echo "      - if it waits on a variable set by the timer handler, is that variable"
  echo "        'volatile sig_atomic_t'? (README: 'The volatile lesson')"
  echo "--- last lines of its output ---"
  printf '%s\n' "$OUT" | tail -n 5
  exit 1
fi
if [ "$RC" -ne 0 ]; then
  echo "FAIL: step$STEP exited with status $RC (a crash, or a non-zero return)."
  echo "--- last lines of its output ---"
  printf '%s\n' "$OUT" | tail -n 5
  exit 1
fi

# Static hints (they do not change the verdict). Comments are stripped first.
code() { gcc -fpreprocessed -dD -E -P "$@" 2>/dev/null; }
SHARED=$(ls src/*.c | grep -v '/step[0-9]_')
ALL=$(for f in "$SRC" $SHARED; do code "$f"; done)
MINE=$(code "$SRC")
if ! grep -qE '\bsetitimer\s*\(' <<<"$ALL" || ! grep -qE '\b(signal|sigaction)\s*\(' <<<"$ALL"; then
  echo "WARNING: no setitimer() timer with a SIGALRM handler (signal/sigaction) found."
  echo "         Frames must be started by a periodic timer and its handler (README, Step 1)."
fi
python3 scripts/check_static.py <<<"$ALL"
if [ "$STEP" = 2 ] && ! grep -qE '\bpause\s*\(' <<<"$MINE"; then
  echo "WARNING: $SRC does not call pause()."
fi
if [ "$STEP" = 3 ] && ! grep -qE '\bsigprocmask\s*\(' <<<"$MINE"; then
  echo "WARNING: $SRC does not call sigprocmask(): is SIGALRM blocked while you test?"
fi

read -r CPU_USER CPU_SYS WALL < "$TIMEFILE"
printf '%s\n' "$OUT" | python3 scripts/check_trace.py \
  --step "$STEP" --cpu "$CPU_USER" "$CPU_SYS" --wall "$WALL"

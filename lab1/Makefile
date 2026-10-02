CC=gcc
# -O2 on purpose: the optimizer is what exposes a missing `volatile`.
# If your program only works at -O0, it is wrong.
CFLAGS=-Wall -Wextra -O2 -g -Isrc -Iprovided

# One program per step. Every other .c file in src/ (frameTable.c and any file
# you add) and in provided/ (helicopterTasks.c) is shared by all steps.
# Object files go to build/, the programs to this folder.
STEPS=step1 step2 step3
BUILD=build
COMMON_SRCS=$(filter-out src/step%.c,$(wildcard src/*.c)) $(wildcard provided/*.c)
COMMON_OBJS=$(addprefix $(BUILD)/,$(notdir $(COMMON_SRCS:.c=.o)))
HEADERS=$(wildcard src/*.h provided/*.h)

vpath %.c src provided

all: $(STEPS)

step1: $(BUILD)/step1_busywait.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) -o $@ $^
step2: $(BUILD)/step2_pause.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) -o $@ $^
step3: $(BUILD)/step3_sigsuspend.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) -o $@ $^

$(BUILD)/%.o: %.c $(HEADERS) | $(BUILD)
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILD):
	mkdir -p $@

# check1: busy-wait accepted.  check2/check3: the program must sleep between
# frames.  check: all three steps.
check1:
	@STEP=1 ./scripts/run_and_check.sh
check2:
	@STEP=2 ./scripts/run_and_check.sh
check3:
	@STEP=3 ./scripts/run_and_check.sh
check:
	@echo "== Step 1"; STEP=1 ./scripts/run_and_check.sh; r1=$$?; \
	 echo "== Step 2"; STEP=2 ./scripts/run_and_check.sh; r2=$$?; \
	 echo "== Step 3"; STEP=3 ./scripts/run_and_check.sh; r3=$$?; \
	 [ $$r1 -eq 0 ] && [ $$r2 -eq 0 ] && [ $$r3 -eq 0 ]

# Build examples/volatileDemo.c twice at -O2 and run both versions.
volatile-demo:
	$(CC) -O2 -o volatileDemo_bug examples/volatileDemo.c
	$(CC) -O2 -DUSE_VOLATILE -o volatileDemo_ok examples/volatileDemo.c
	@echo "--- with volatile:"
	./volatileDemo_ok
	@echo "--- without volatile (killed after 3 s if stuck):"
	-timeout 3 ./volatileDemo_bug || echo ">>> stuck: tick was never re-read"

clean:
	rm -rf $(BUILD) $(STEPS) volatileDemo_bug volatileDemo_ok

.PHONY: all check check1 check2 check3 volatile-demo clean

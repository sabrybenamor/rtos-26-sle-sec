#include <stdio.h>
#include <unistd.h>
#include <signal.h>

// Functions prototypes
static void alarmHandler(int signo);

int main(void){
	// Link the alarm interrupt with the defined handler
	signal(SIGALRM, alarmHandler);

	// Set the alarm to generate an interrupt after 5 seconds
	alarm(5);

	// Print an incrementing counter every second and check
	// when the handler will be executed
	for(int i = 1; i < 10; i++){
		printf("%d\n", i);
		sleep(1);
	}
	return 0;
}

/** This is the defined handler associated to the alarm
* interrupt. It simply outputs a message.
* Please note that a handler function is never called
* explicitly in the code you write. It is done by the
* runtime.
* Note: printf() is not async-signal-safe; it is used here only
* to make the demo visible. In real code (and in your lab), the
* handler should only set a volatile sig_atomic_t flag/counter.
* See examples/timerExample.c and examples/volatileDemo.c.
**/
static void alarmHandler(int signo){
	printf("Alarm signal (%d) sent!\n", signo);
}
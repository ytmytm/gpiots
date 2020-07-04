/*
Licensed under The MIT License (MIT)

Copyright (c) 2018 Danny Heijl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
#include <fcntl.h>
#include <poll.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>

#include "fifo.h"

#include <wiringPi.h>

#define NGPIOS 2
#define LP_GPIO 17
#define VSYNC_GPIO 22
#define BUT_GPIO 27 // 1 released, 0 pushed

int main(int argc, char **argv) {

if (wiringPiSetupGpio() == -1) {
    perror("wiring\n");
    return 1 ;
}
    pinMode(BUT_GPIO,INPUT);

    struct timespec ts;

    int files[NGPIOS];
    for (int i = 0; i < NGPIOS; ++i) {
        char gpio[64];
        snprintf(gpio, 64, "/dev/gpiots%d", i);
        int fd = open(gpio, O_RDONLY); 
        if (fd < 0) {
            printf("%s open error %d\n", gpio, fd);
            exit(-1);
        }
        files[i] = fd;
    }
    int n;
    struct pollfd fds[NGPIOS];
    for (int i = 0; i < NGPIOS; ++i) {
        fds[i].fd = files[i];
        fds[i].events = POLLPRI | POLLERR;
    }
    long ulast[NGPIOS];
    while (true) {
        int rc = poll(fds, NGPIOS, 2000);
        if (rc < 0) { // error
            perror("poll failed");
            return -1;
        }
        if (rc == 0) { // timeout
            //printf("poll timeout\n");
            continue;
        }
	for (int i = 0; i< NGPIOS; ++i) {
    	    if (fds[i].revents!=0) { // LP event
	        n = read(files[i], &ts, 1);
        	long usecs = ts.tv_sec * 1000000 + ts.tv_nsec / 1000;
    		printf("LP%i: %ld\t",i,usecs-ulast[i]);
		ulast[i] = usecs;
	    }
	}
	printf("\n");
    }
    for (int i = 0; i < NGPIOS; ++i) {
        close(files[i]);
    }
    exit(0);
}

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <time.h>
#include <assert.h>
#include <unistd.h>
#include <sys/time.h>

#include "bcm_host.h"

static DISPMANX_DISPLAY_HANDLE_T   display;
unsigned long lasttime = 0;

void vsync(DISPMANX_UPDATE_HANDLE_T u, void* arg) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    unsigned long microseconds = (tv.tv_sec*1000000)+tv.tv_usec;
    printf("%lu\tsync %lu\n", microseconds,microseconds-lasttime);
    lasttime = microseconds;
}

int main(void)
{
    bcm_host_init();
    display = vc_dispmanx_display_open( 0 );

    vc_dispmanx_vsync_callback(display, vsync, NULL);
    sleep(1);
    vc_dispmanx_vsync_callback(display, NULL, NULL); // disable callback

    vc_dispmanx_display_close( display );
    return 0;
} 

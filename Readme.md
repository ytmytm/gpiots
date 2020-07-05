# rpi-lightpen

A Linux kernel device driver for 8-bit era lightpen attached to GPIO with some support circuitry.

Please visit https://hackaday.io/project/172255-light-pen-support-for-retropie for more details about this project.

## Build

Just type `make`, you need to have kernel headers installed.

## Module parameters

Insert module using provided `./insmodule.sh` script. The module parameters are:

```
sudo insmod ./gpiots.ko gpios=<lp sensor>,<vsync gpio> gpio_lp_button=<lp button>, gpio_odd_even=<odd/even>
```

- `<lp sensor>` - GPIO where light pen phototransistor sensor is connected
- `<lp button>` - GPIO where light pen button line is connected
- `<vsync gpio>` - GPIO where VSYNC line from LM1881 chip is connected
- `<edd/even>` - GPIO where ODD/EVEN line from lM1881 chip is connected

## NTSC support

There is none. This module is calibrated for PAL with 64us per line.

## Install

Check commented-out parts of `insmodule.sh`.

## Data

Read coordinates from /dev/gpiots0.

Every second frame (25 times per second), if light pen is pointed at the CRT screen, you will receive a single line with three numbers:

```
<x>,<y>,<b>\n
```

- `x` is column offset in range 0-63, please note that 0 might be somewhere in the middle of the line, you need to calibrate for wraparound and subtract left offset, then add 64 to negative numbers
- `y` is line offset in range 0-305 (theoretical)
- `b` is button state (0 is pressed, 1 is released)


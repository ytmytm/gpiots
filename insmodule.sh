#!/bin/bash
##KVERSION=`uname -r`
##mkdir -p /lib/modules/${KVERSION}/extra
##sudo cp gpiots.ko /lib/modules/${KVERSION}/extra/
##sudo insmod /lib/modules/${KVERSION}/extra/gpiots.ko gpios=17,22
sudo rmmod gpiots
sudo insmod ./gpiots.ko gpios=17,22 gpio_lp_button=27 gpio_odd_even=23

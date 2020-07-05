ifneq (${KERNELRELEASE},)

	obj-m  := rpi_lightpen.o
#	rpi_lightpen-y := rpi_lightpen.o

else

	MODULE_DIR := $(shell pwd)
	KERNEL_DIR ?= /lib/modules/$(shell uname -r)/build
	CFLAGS := -std=gnu99 -Wall -g

all: modules

modules:
	${MAKE} -C ${KERNEL_DIR} SUBDIRS=${MODULE_DIR}  modules 

clean:
	rm -f *.o *.ko *.mod.c .*.o .*.ko .*.mod.c .*.cmd *~ test
	rm -f Module.symvers Module.markers modules.order
	rm -rf .tmp_versions
endif

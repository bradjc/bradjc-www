---
permalink: "/class/cs6456-f19/hw5.html"
layout: single
title:  "CS6456 - HW5"
sidebar:
  nav: "cs6456hw5"
---

<style>
.masthead {
  display: none;
}
</style>



# HW5: Ticked Kernels

A tick-based kernel uses a periodic timer interrupt to manage concurrency and
other system events. The periodic timer fires a very low-level interrupt that
returns control to the kernel if a process is running, and the kernel can keep
track of the number of ticks that have occurred. This basic mechanism simplifies
many kernel operations because the system can rely on the interrupt for
timeslicing and to ensure the kernel will have an opportunity to run.

While having a periodic tick is very useful, it also has drawbacks. The primary
issue is that the interrupt for the tick is continuous, even if nothing is
actually using it. For example, if all processes are waiting on an external
interrupt and the system could be sleeping, the periodic tick will wake up the
kernel which will check that all processes are still blocked and just go back to
waiting. On low power systems this becomes a significant waste of energy.

The second issue with a tick-based kernel is it enforces a fixed timeslice for
processes. At every tick the system switches to the kernel, interrupting any
running process, and then the kernel can decide what to schedule next, including
continuing to run the interrupted process. However, this delay can just be
wasted time, and the kernel loses flexibility in how long to run a particular
process.

In this assignment you will modify a tick-based kernel to make the tick period
dynamic and under the kernel's control. While modifying the kernel to be
tickless is outside of the scope of this assignment, you will be able to explore
what happens when the ticks are no longer at regular intervals.

## xv6 RISC-V Kernel

For this assignment you will use the [xv6
kernel](https://github.com/mit-pdos/xv6-riscv) for the RISC-V 64 bit
architecture. This includes all of the core components of an operating system
kernel while still being accessible to hack on.

The kernel runs on [QEMU](https://www.qemu.org/), a CPU emulator.

## Objective

Your goal is to modify the kernel so that tick period is not fixed (that is you
can't just change the tick period to just a different static value). You should
have some policy for how the tick period changes which can be very simple or
more complicated. For example, you might consider additively increasing the tick
period when all processes are waiting on interrupts and then multiplicatively
decrease it if a process exceeds its timeslice.

You are required to include a short description of your adaptive tick interval
algorithm.

## Part 0: Setup

First you have to install some dependencies.

1. Clone the xv6 source.

    ```
    $ git clone https://github.com/mit-pdos/xv6-riscv
    ```

### Install Instructions Using Package Managers


2. Install the RISC-V compiler.

    ```
    $ sudo apt-get install gcc-riscv64-linux-gnu
    ```

    or

    ```
    $ brew tap riscv/riscv
    $ brew install riscv-tools
    ```

3. Install QEMU.

    ```
    $ sudo apt-get install qemu
    ```

    or

    ```
    $ brew install qemu
    ```

### Install Instructions by Compiling from Source

1. For the RISC-V compiler:

    1. Install prerequisites:

        ```
        sudo apt-get install autoconf automake autotools-dev curl libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev
        ```

    2. Get the source:

        ```
        git clone https://github.com/riscv/riscv-gnu-toolchain
        cd riscv-gnu-toolchain
        git submodule update --init --recursive
        ```

    3. Install (newlib):

        ```
        ./configure --prefix=/opt/riscv
        make
        ```

        and then add '/opt/riscv/bin' to your path.

2. For install  QEMU compiler:

    1. Get the source:

        ```
        git clone https://github.com/qemu/qemu
        cd qemu
        ```

    2. Install:

        ```
        ./configure --target-list=riscv64-softmmu
        make -j $(nproc)
        sudo make install
        ```

### Testing

After that you should be able to run the kernel.

```
$ cd xv6-riscv
$ make qemu
```

That will load the emulator with the kernel, and by default the kernel loads the
shell process (`sh`). This is a basic shell, but should be reasonably familiar.

To exit QEMU you can enter `ctrl+a` and then `x` to exit QEMU.

To modify the kernel you can directly edit the source and then re-run `make
qemu`. You can also add new applications in the `user` folder and then add them
to the `UPROGS` variable in the Makefile and they will be available in the
kernel.

To simplify the project, you should edit the `CPUS` variable in the Makefile and
set it to `1`. Run `make clean` to ensure the change propagates.


### RISC-V

RISC-V is a new risc architecture with substantial documentation available
online. Here are some basics which should be useful.

RISC-V cores have three privilege level modes: M (machine), S (supervisor), and
U (user). A specific instruction is used to switch privilege modes. For example,
the `mret` instruction switches from M mode to S mode, and the `sret` instruction
switches from S mode to U mode. To go the other way, the `ecall` instruction
traps to a higher privilege level.

The core boots into M mode. Some initial setup is done, and then the core
switches to S mode where the kernel starts running. Of course applications
execute in U mode.

The tick in xv6 is implemented using the machine-mode timer and configured
initially in `start.c`. This is a simple timer which is just a continuously
running clock and single compare register. When the clock value matches the
compare register an interrupt is generated. Since the machine timer operates in
M mode, this interrupt traps the CPU into M mode. The interrupt handler is
specified by the `mtvec` register, which is set to the `timervec` function in
the `kernelvec.S` file. The `timervec` handler adds the tick interval to the
compare register to reset the timer for the next tick event. It then generates a
software interrupt to notify the kernel in S mode that the tick occurred. These
trap events are handled by the kernel in the `trap.c` file.

The different privilege levels can store state in the `Xscratch` register. For
example, machine mode can store 64 bits of state in the `mscratch` register. The
xv6 kernel uses the `mscratch` register to store a pointer to some state
reserved for the machine timer code. You can see in the `timervec` function how
that is used. Note that the interval used for the tick is stored in the array
pointed to by `mscratch`.

### xv6

The xv6 kernel includes the various components you would expect to be in an
operating system kernel. The actual scheduler is in `proc.c`. You should be able
to verify that the scheduler by default uses a round-robin scheduler.

The code for handling interrupts and exceptions is in `trap.c`. This is, for
example, where the code that handles when a userspace process calls a syscall
and the system traps to the kernel resides, as well as where interrupts are
handled.

Userspace applications have a very standard set of syscalls, include `read`,
`write`, `fork`, etc.


## Part 1: Enable the kernel to change the tick interval

You should start by finding a way to change the duration of the tick interval
from the kernel code. That is, changing the value in `timerinit()` in `start.c`
is not very helpful since that code operates in M mode and is only called once.
We want to be able to change the tick interval dynamically.

You can test the tick interval has changed by adding a `printf()` to the
`clockintr()` function (where the tick is recorded) and verifying that the tick
occurs at a different rate than before.


## Part 2: Implement a dynamic tick interval policy

Building on Part 1, you should now implement a dynamic tick interval policy.
This should respond to the operation of processes in the system with the goal of
reducing the number of ticks while preventing a process from monopolizing the
CPU.

> While it will likely take some time to find where to make the changes, a
> simple algorithm requires only adding about 10 lines of code to the kernel.

### Testing

You should devise a scheme for verifying that the tick interval is being
dynamically adjusted. Certainly one option is to add a `printf()` when the tick
occurs and inspect that the frequency of the print messages changes. You can
also write an application which calls `fork()` to create multiple processes that
the OS has to schedule. If one is intermittently CPU bound (i.e. it has periods
of high computation (say `while(1)`) and periods of waiting) and the other is IO
bound, both processes should make progress but the tick interval should change.

## Deliverables

You should submit two things in a zip file:

1. The diff of your code in the `xv6-riscv`. You can run `git diff > hw5.diff`
to generate the diff.

2. A text file with answers to the following two questions:

    1. What algorithm for adjusting the tick interval did you implement?
    2. Which syscall does adapting the tick interval most affect? Why?


## Submission

You should upload your zip or tar file on collab.


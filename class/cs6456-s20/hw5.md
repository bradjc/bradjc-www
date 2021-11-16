---
permalink: "/class/cs6456-s20/hw5.html"
layout: single
title:  "CS6456 - HW5"
sidebar:
  nav: "cs6456s20hw5"
---

<style>
.masthead {
  display: none;
}
</style>



# HW5: Downloading Code

We keep seeing over and over the benefits of making kernels smaller and moving
functionality into userspace. However, we've also seen this can be overly
limiting; there are some operations that are just more effective in the kernel.
Even the Exokernel architecture, which advocates for a small core kernel,
includes an extension to the design in section 3.2.1 that allows for
"downloading code" into the kernel to increase performance.

Linux has also embraced this idea, with the
[eBPF](https://www.kernel.org/doc/html/latest/bpf/index.html) tool included in
recent kernel versions. "Downloaded code" has made the jump from research to
practice!

In this assignment you will experiment with running userspace code inside of the
kernel. In particular, you will implement a simple debugging tool that is
specified from userspace, but executed in kernel space. Often debugging is a
circular process: we observe unexpected behavior, then add debugging statements
to identify why the execution is not as we expect, then recompile, then
re-execute and attempt to identify what is actually happening, and then loop as
necessary. If we could dynamically add debugging statements to the kernel, we
may be able to more easily identify issues.

## Xv6 RISC-V Kernel

For this assignment you will use the [xv6
kernel](https://github.com/mit-pdos/xv6-riscv) for the RISC-V 64 bit
architecture. This includes all of the core components of an operating system
kernel while still being accessible to hack on.

The kernel runs on [QEMU](https://www.qemu.org/), a CPU emulator.

## Objective

Your goal is to modify the Xv6 kernel to support userland-specified debugging
`printf()` style statements at three points in the kernel. By default, the
kernel should not start with any debugging messages turned on. A userland
process, however, should be able to enable and customize each of the three
debugging messages. Additionally, the debug messages must support variable
substitutions.

### Debug Message Hook Points

Your modified kernel should be able to print messages at three different points
during its operation:
- When a process starts.
- When a process exits.
- When the "open" syscall is called.

### Debug Messages

Userspace must be able to pass strings to the kernel that the kernel will print
whenever it executes one of the debug points. You may assume that the strings
will be no longer than 1024 bytes.

### Message Variable Substitutions

To aid with debugging, the kernel must support substituting variables in the
debug messages at runtime with current values. The two substitutions that you
must support are:
- Replacing `{numprocs}` with the number of processes currently running in the
  system.
- Replacing `{curproc}` with the index (ID) of the process triggering or
  relevant to the event. For example, the process that exited or that called the
  open syscall.

For example, the following is an example debug message that a userspace
application might pass to the kernel for the open syscall hook:

```text
Process {curproc} called open().
```

If the process with the index 4 called the open syscall, then the kernel should
print the following message:

```text
Process 4 called open().
```

### A New Syscall

You will have to add a syscall to allow userspace to set the debug message. The
syscall must be able to specify which debug hook point the message is for, and
pass the message string itself. However, the syscall does not need to support
explicitly turning off debug messages. Userspace can instead specify an empty
message to effectively disable a debug message.


## Part 0: Setup

First you have to install some dependencies.

1. Clone the xv6 source.

    ```
    $ git clone https://github.com/mit-pdos/xv6-riscv
    ```

### Install Instructions Using Package Managers


2. Install the RISC-V compiler.

    **Linux**:

    ```
    $ sudo apt-get install gcc-riscv64-linux-gnu
    ```

    Note: you need at least riscv64-linux-gnu-gcc version 8 or greater. If you
    run `riscv64-linux-gnu-gcc --version` and it is an older version than 8, you
    should run:

    ```
    $ sudo apt install gcc-8-riscv64-linux-gnu
    $ sudo update-alternatives --install /usr/bin/riscv64-linux-gnu-gcc riscv64-linux-gnu-gcc /usr/bin/riscv64-linux-gnu-gcc-8 8
    ```

    to ensure that `riscv64-linux-gnu-gcc` is at least version 8.

    **Mac**:

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
online. However, the architecture should not matter for this assignment.

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


## Part 1: Adding a syscall

You should trace through how syscalls are handled in the kernel. In particular,
how are different types of syscall arguments handled? You will then need to add
a new syscall with an appropriate syscall handler.


## Part 2: Identify hook locations for debug messages

Next you need to identify where in the kernel the debug messages should be
called from. To start, you can hardcode `printf()` statements in these locations
and then test by running various userland programs.

You can also test your variable substitution code by using a string like
`Process {curproc} (out of {numprocs}) exited`.

> You should "borrow" string substitution code from the internet, unless you
> really want to write your own.

## Part 3: Implement the syscall in userspace

You will need to create a function in the userland libraries that allows a
program to call your new syscall.

## Part 3: Connect user provided strings to debug points

The last step is using the strings passed in from userspace in the debug hooks
in the kernel.

### Testing

You should be able to write a program that uses your new syscall to change the
debug messages at run time. For example, you can set the open syscall debug
message, call open(), then change the syscall message, and call open() again,
and verify a new message is displayed.

## Deliverables

You should submit the following in a zip file:

- The diff of your code in the `xv6-riscv`. You can run `git diff > hw5.diff`
to generate the diff.


## Submission

You should upload your zip or tar file on collab.


## Future Steps

While not required for this assignment, you can think about some questions that
this implementation of "code downloading" raises:

- Is this safe to do? Does this violate the integrity of the kernel?
- This basic approach is limited. How would you extend it? What else would be
  helpful for printf() debugging?
- As a debugging approach gets more complicated, how can we verify it is safe to
  include in the kernel?


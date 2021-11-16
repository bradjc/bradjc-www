---
permalink: "/class/cs6456-s20/hw2.html"
layout: single
title:  "CS6456 - HW2"
sidebar:
  nav: "cs6456s20hw2"
---

<style>
.masthead {
  display: none;
}
</style>



# HW2: Threading Library

In this assignment, you will write a cooperative [green
threads](https://en.wikipedia.org/wiki/Green_threads) library, floral. You will
be programming in C and x86-64 assembly.

Greens threads are similar to the type of threads you might be familiar with, OS
threads, but are implemented entirely in user-level code. They are also known as
user-level threads. They are typically speedier than OS threads since there is
no context switching into/out of the kernel. Cooperative green threads are green
threads that release control to the scheduler deliberately, usually through a
yield() call. That is, they execute for as long as they want.

A user of your floral library first calls `grn_init()` to initialize the first
green thread, one representing the originally executing program. Then, the user
calls `grn_spawn(user_fn)` to create a new thread that executes the `user_fn`.
(Note that in a production thread library, `grn_spawn` would take an extra
`void*` argument to pass to `user_fn` so as to spawn different threads running
the same function on different arguments.) The user calls `grn_yield(0)` inside
a thread to yield execution to another thread, including the original. The
floral library also supports simple condition variables, so if a thread wants to
yield until a condition is met, it calls `grn_wait(int condition)` with an
integer identifying the condition to wait for. If a thread wants to signal that
a condition has been met, it can pass the condition number as an argument to
`grn_yield(int condition)`. Finally, the user might call `grn_join()` to wait
for all of the spawned threads to finish executing before ending the process.

A full program using your library might look like this:

```c
#include "floral.h"

extern void have_work();
extern void waiting();
extern void do_work();

void user_fn() {
  while (have_work()) {
    while (waiting()) {
      grn_yield(0);
    }

    do_work();
  }
}

int main() {
  grn_init(false);
  for (int i = 0; i < 10; ++i) {
    grn_spawn(user_fn);
  }

  grn_join();
  grn_exit();
}
```

This homework is divided into 5 phases. The first 4 phases will guide you
towards implementing cooperative green threads. Once you have completed phase 4,
the example program above will run as you expect. In phase 5, you will implement
simple thread garbage collection so that resources aren't leaked after a thread
terminates.

There are unit tests corresponding to each phase, allowing you to mark your
progress as you work through the assignment. You may find the list of references
useful as your proceed.

## Phase 0: Getting Started

First, ensure that you using a compatible machine meeting the following
requirements:

- Runs a modern Unix: Linux, BSD, or OS X
- Runs a 64-bit variant of the OS (check with arch)
- Has GCC or Clang and GNU Make installed

To begin, download the [skeleton code](hw/floral_2020-02-05.zip).

### Exploring the skeleton code

The majority, if not all of your work will be to modify the files found in the
`src/` directory of the skeleton code:

- `src/main.c` contains the high-level green-thread library functions
- `src/thread.c` contains thread management functions: allocating and destroying
  threads, and thread list management
- `src/context_switch.S` contains the assembly routines that implement thread
  context switching

The `include/` directory contains the header files for these `src/` files where
applicable and are named like their `src/` counterpart. There are two
exceptions: 1) include/floral.h, which exports the high-level library routines
for use by user binaries that link to your library, and 2) `include/utils.h`,
which defines the following helpful macros (among others):

- `debug(...)` like `printf()`, but only prints if there is a #define DEBUG at
  the top of the file.
- `assert(cond)` checks that `cond` evaluates to `true`. If it does not, prints
  an error message and terminates the program.
- `err_exit(...)` like `printf()` but terminates the program after printing the
  error message.

Finally, the `test/` directory contains the unit testing code. The tests
themselves are in `test/src/phase{n}_tests.c`. If a test you expect to pass
fails, you can look at its test file to see why.

### Make targets

You will use make to build, test, and create a submission file for this lab. The
following targets are defined in the Makefile:

- `all`: compiles and packages your library
- `test`: runs the unit tests against your library
- `submission`: creates the hw2.tar.gz submission file
- `clean`: deletes files that can be remade - useful when changing headers

Calling make in your shell will implicitly run the all target. The other targets
can be invoked using `make <target>`. Ensure that you are in the root directory
of the assignment before invoking make. Try calling `make test` now. You should
see five failing test suites. If this doesn't work, your machine may not meet
the requirements.

### Getting familiar

Before you continue, read through the `src/` files and some of the unit test
files (`test/src/phase{n}_tests.c`) to see how the functions you will write are
intended to be used and what we will test for. Also pay attention to the code
style: how variables are named, how code is aligned, and how spacing is used.
You should write your code with an equivalent style. Once you have a good grasp
of the floral thread interface and functions, you’re ready to start writing
code.


## Phase 1: Allocating and Deallocating Threads

In phase 1, you will implement the functions marked "FIXME" in `src/thread.c`.

The `grn_thread` structure, defined in `include/floral.h`, contains all of the
information needed to context switch into a thread. Specifically, it contains a
thread's state (context) and metadata the scheduler uses to make decisions. We
keep track of the threads in the system via a linked list: the next and prev
pointers in the `grn_thread` structure point to the next and previous elements
of the linked list, respectively, and the threads field of the global `STATE`
(declared in `include/main.h` and defined in `src/main.c`) holds a pointer to
the head of the list. Examine and ensure that you understand the thread linked
list manipulation functions we have implemented for your use in `src/thread.c`:
`add_thread`, `remove_thread`, and `next_thread`. We've also provided the
`atomic_next_id` function which simply returns a strictly increasing counter.

Your task is to implement the functions that allocate and destroy (deallocate)
`grn_thread` structures for use by the rest of the system: `grn_new_thread` and
`grn_destroy_thread`. You can find the functions' specifications directly above
their definition. Once you have done this, you should pass the phase 1 unit
tests.

{: .notice--info}
You may need to modify the `grn_thread_struct` fields as you complete this
project.

## Phase 2: Context Switching

In phase 2, you will write the code to context switch from one thread to another
in the assembly function marked "FIXME" in `src/context_switch.S`.

The `context_switch` function will be called on behalf of a green thread during
its execution to context switch from one thread to another. For a context switch
to be successful, all state of the currently executing thread must be saved in
some structure and the state of the thread being switched into must be restored.
A thread's state is also referred to as its context.

A thread’s context is already defined in the `grn_context` structure in
`include/floral.h` as seven 64-bit registers: `rsp`, the stack pointer, `rbp`,
the base pointer, and `rbx`, `r12`, `r13`, `r14`, and `r15`, general purpose
registers. All of these registers are known as _callee saved_, which means that
the callee of a function guarantees that those registers will have the same
value when the function returns as they did when the function was called. In
other words, a function A calling another function B can expect those registers
to contain the same values after function B returns as they had when function B
was called because the callee (B) saves and restore those values. These
registers are defined this way by the System V X64 ABI calling convention, which
is followed on most Unix systems running on 64-bit machines. You can read more
at the ABI reference link.

{: .notice--info}
**Where are the rest of the registers?**
<br /><br />
A keen reader might wonder why a thread's context only contains the
callee-saved registers when there are more general purpose 64-bit registers.
The answer relies on the notion of `caller-saved` registers, which are
registers that a function caller saves before calling a function. The
registers that don't appear in `grn_context` are caller-saved registers. Since
the `context_switch` function will be _called_, the compiler will emit
instructions to save and restore those registers, so no extra work is needed
to maintain that state, and the `callee-saved` registers suffice as our
register state.

Apart from these registers, a thread's full context also includes the values in
its stack. Saving and restoring a thread's stack on each context switch would be
a very expensive operation, so instead of doing this, we simply give each thread
its own unique stack. Then, as long as each thread's stack pointer points to its
own unique stack, saving and restoring the stack pointer suffices to save and
restore the thread's stack. Later on, you'll write the code that ensures that
each thread's stack pointer points to its own unique stack (which you’ve already
allocated in `grn_new_thread`). The `context_switch` function should only be
called on already running threads, so the validity and uniqueness of the stack
pointer can be assumed.

You're ready to implement the context switching assembly function in
`src/context_switch.S`. You can find the function's specification above its
definition. Keep in mind that according to the calling convention, the first two
parameters to a function are passed in the `rdi` and `rsi` registers. Also note
that GCC calls the GNU Assembler implicitly, which uses the GAS syntax for
assembly. You may wish to consult the calling convention in the ABI reference or
the X86 instruction reference, both of which are linked in the column to the
right. After you have implemented this routine, you should pass the phase 2 unit
tests.


{: .notice--success}
Hint: You can implement `grn_context_switch` using only two different assembly
instructions: `mov` and `ret`.


## Phase 3: Yield

In this phase, you will implement `grn_wait` and `grn_yield` in `src/main.c`,
the main thread scheduling functions.

When a thread wants to release control to the scheduler, it yields its execution
time by calling `grn_wait()` or `grn_yield()`. `grn_wait()` allows the thread to
specify the condition it wants to wait for. `grn_yield()` allows the thread to
simply yield its time (by passing `0`), or to yield and signal that a condition
is met (by passing a nonzero argument).

Both functions must find a valid next thread to run. The scheduling algorithm
they should use are described in the comments in the code. At a high-level, if a
thread signals a condition, and a thread is waiting on that condition, then that
thread should run next.

Each thread in floral is marked with a status of `READY`, `RUNNING`, `WAITING`,
or `ZOMBIE`. A thread is `READY` when it can be executed, `RUNNING` when it is
executing, `WAITING` when some processing needs to happen before it is `READY`,
and `ZOMBIE` when a thread has finished executing but hasn't has its resources
freed and destroyed.

Your yield functions should use and modify these statuses for scheduling.
Once a suitable thread is found, the status of the currently executing
thread is set to `READY` if it was previous `RUNNING`, and the newly found
thread’s status is set to `RUNNING`. The pointer to the currently executing
thread, `STATE.current`, is updated. Finally, the function `context_switch`es
into the newly found thread.

Your task is to implement the `grn_wait` and `grn_yield` functions. The full
specification is above the definitions. After you have implemented this routine,
you should pass the phase 3 unit tests.

{: .notice--success}
Hint: Use the `next_thread` function for a looping linear search.

{: .notice--warning}
Warning: Yield's unit tests are not exhaustive. A later phase's unit tests
might reveal a bug in this phase.

## Phase 4: Spawn

In this phase, you will implement `grn_spawn` in `src/main.c`, the new thread
initializer. After implementing this function, you will have implemented
cooperative green threads.

A thread created by a user executes a function of the user’s choice. The
`grn_spawn` function accomplishes exactly this: it allocates a new thread,
initializes its context so that the user's function is executed after a context
switch, and finally calls `grn_yield` to yield the caller's execution to
(potentially) the newly initialized thread.

When a thread is allocated by your `grn_new_thread` function, it has an empty
context, so context switching into it would likely crash the process. Your task
is to write `grn_spawn` to set up values in the stack so that after the first
`context_switch` into the thread, the thread begins executing the `start_thread`
routine, a thread start function written in assembly we have provided to you.
`start_thread` expects the user's function to be at the top of the stack when it
is called. Thus, you must design the initial stack so that during a given
thread's first `context_switch`, `context_switch` returns to `start_thread`, and
`start_thread` finds a valid function at the top of the stack.

The implementation of this function requires you to write values into the
thread's initial stack and then set the stack pointer appropriately. Note that
the x64 ABI declares mandates the stock pointer to be 16-byte aligned. The full
function specification is above its definition. After you have implemented this
routine, you should pass the phase 4 unit tests.

{: .notice--success}
Hint: The only register needing initialization is %rsp.

## Phase 5: Garbage Collection

In this phase, you will implement `grn_gc` in `src/main.c`, a simple thread
garbage collection routine.

Upon thread termination, the thread's initial function returns to
`start_thread`, and `start_thread` calls `grn_exit` to terminate the thread.
`grn_exit` is a simple function: it simply sets the thread's status to `ZOMBIE`
so that `grn_yield` doesn't schedule it again.

Your task is to ensure that a thread's resources are freed after it has exited.
You must implement `grn_gc`, which finds all `ZOMBIE`d threads and frees their
resources. Then, insert a call to `grn_gc` in an appropriate location in your
library. Note that you have already written `grn_destroy_thread`: `grn_gc`
should call this function appropriately. The full function specification is
above its definition. After you have implemented this routine, you should pass
the phase 5 unit tests.

{: .notice--success}
Hint: When is it and when is it not safe to call `grn_gc`?

## Submission

Once you’ve completed the tasks above, you’re done and ready to submit! Any
changes made to files outside of the `src/` or `include/` directories will not
be submitted with your lab. Ensure that your submission is not dependent on
those changes.

Finally, run `make submission` and then upload your submission on Collab.

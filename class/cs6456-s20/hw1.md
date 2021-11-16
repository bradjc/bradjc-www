---
permalink: "/class/cs6456-s20/hw1.html"
layout: single
title:  "CS6456 - HW1"
sidebar:
  nav: "cs6456hw1"
---

<style>
.masthead {
	display: none;
}
</style>



# HW1: Write a Basic Shell

In this assignment you will implement a basic but functional shell called
`uvash` (UVA Shell). Your task is to create a Unix-like shell with the following
features:

- Able to run simple commands (e.g. `/bin/cat foo.txt bar.txt`).
- Input redirection (e.g. commands like `/usr/bin/gcc -E - < somefile.txt`).
- Output redirection (e.g. commands like `/usr/bin/gcc -E file.cc > somefile.txt`).
- The builtin command `exit`.

You will start with some starter code and add the needed features. In addition
to the main features, your shell must:

- Prompt for commands using `>`.
- Not search for executables on `$PATH`. All commands will include the absolute
  path to the executable or a relative path from the current directory.
- Print out error messages (to stderr) when errors are detected.
- Support pipelines (e.g. commands like `/bin/cat foo.txt | /bin/grep bar |
  /bin/grep baz`).
- Not leave any extra file descriptors open (ones other than `stdin`, `stdout`,
  `stderr`) just before it executes a command.

We strongly recommend creating partially working versions as described below. A
full solution will be around 200 lines of code.

## Files

Download the [skeleton code](hw/shell_2020-01-27.zip) last updated 01-27-2020,
which contains:

- A starter Makefile which has a target to build a binary called `uvash`.
- A source file `main.cc` which implements a prompt that prints a "Not
  implemented" error on any command but "exit".

You may use additional source files, rename source files, switch from C++ to C,
etc. so long as you modify the Makefile appropriately and still produce an
executable called `uvash`.

We have supplied a `shell_test.py` program, which you can run by running `make
test`. This will often produce a lot of output (especially when you haven’t
implemented all shell features yet), so you might try redirecting its output to
a file like with `make test > test-output.txt`. Note that we may use additional
and/or different tests when we grade your submission.

We intend to test the shell you submit on a standard Linux environment.

Prepare a `.tar.gz` file like the one built using `make archive` in the given
Makefile. This should have all your source files and a Makefile which can
produce an `uvash` binary. It should not contain any object files or a pre-built
`uvash` executable.

Submit the `<your university email id>.tar.gz` file on Collab.

## Specification

### Shell language

Shell commands are lines which consist of a sequence of whitespace-separated
tokens. Whitespace characters are space (`' '` in C or C++), form feed (`'\f'`),
newline (`'\n'`), carriage return (`'\r'`), horizontal tab (`'\t'`), vertical
tab (`'\v'`).

Each line has a maximum length of 100 characters. We do not care what your shell
does with longer input lines.

Each token is either:

- an _operator_, if it is `<` or `>` or `|`
- a _word_ otherwise

Each line of inputs is a pipeline, which consists of a series of a commands
(possibly just one) separated by `|`s.

Each _command_ consists of a series of:

- One or more words, which are used to form the command for an `exec` system
  call.
- Up to one input redirection operation, which consists of a `<` token followed
  by a _word_ token.
- Up to one output redirection operation, which consists of a `>` token followed
  by a _word_ token.

### Running commands

If a command contains excess input or output redirection operations, or
operators followed immediately by another operator, that is an error.

To run a pipeline, the shell runs each command in the pipeline, then waits for
all the commands to terminate. You may decide what to do if one of the commands
in the pipeline cannot be executed as long as your shell does not crash or
otherwise stop accepting new commands.

To run a command, the shell:

- First checks if it is one of the built-in commands listed below, and if so
  does something special.
- Forks off a subprocess for the command.
- If it is not the first command in the pipeline, connects its `stdin` (file
  descriptor 0) to the `stdout` (file descriptor 1) of the previous command in
  the pipeline. The connection should be created as if by pipe (see man pipe).
  (You may not, for example, create a normal temporary file, even if this
  sometimes works.)
- If it is not the last command in the pipeline, connect its `stdout` to the
  `stdin` of the next command in the pipeline.
- If there is an output redirection operation, reopen stdout to that file. The
  file should be created if it does not exist, and truncated if it does.
- If there is an input redirection operation, reopen `stdin` from that file.
- If if is the last command in the pipeline, and there is no output redirection
  operation, save the stdout of the command in a buffer inside of the shell.

### Built-in command

Your shell should support the following built-in command(s):

- `exit`: When this command is run your shell should terminate normally (with
  exit status `0`). You should not run a program called `exit`, even if one
  exists.
- `status`: When this command is run your shell should print to stdout `Status:
  <#>` with the exit status of the last command run (for example, on success
  this should print `Status: 0`. If multiple commands were run in a pipeline
  this should print the return code of the last command in the pipeline. If an
  error occurred while the shell tried to run the last command the status number
  should be 255. If no commands have been run the status number should be 0. You
  should not run a program called `status`, even if one exists.
- `print`: When this command is run your shell should print the stdout received
  from the most recently run non-built-in command. You should not run a program
  called `print`, even if one exists.

### Handling errors

Your shell should print out error messages to `stderr` (file descriptor 2).

You must use the following error messages:

- If an executable does not exist, print an error message containing "No such
  file or directory". You may include other text in the error message (perhaps
  the name of the executable the user was trying to run). Note that "No such
  file or directory" is what `perror` or `strerror` will output for an `errno`
  value of `ENOENT`. (See their manpages by running man perror or man strerror.)
- If a command is malformed according to the language above, print an error
  message containing "Invalid command".
- If `exec` fails for another reason (e.g. executable found but not executable)
  any error message is acceptable.
- If `fork` or `pipe` fail for any reason any error message is acceptable. Your
  program must not crash in this case.
- If opening an input or output redirected file fails for any reason any error
  message is acceptable.

If multiple commands in a pipeline fail, you must print out error messages, but
it may be the case that commands in the pipeline are executed even though error
messages are printed out (e.g. it's okay if `something_that_does_not_exist |
something_real` prints an error about `something_that_does_not_exist` after
starting `something_real`.)

## Hints

### Recommended order of operations

1. Implement and test parsing commands into whitespace-separated tokens. Collect
   the tokens into an array or vector to make future steps easier.
2. Implement and test running commands without pipelines or redirection. In this
   case the list of tokens you have will be exactly the arguments to pass to the
   command.
3. Add support for redirection.
4. Add support for pipelines.

### Parsing

In C++, you can read a full line of input with `std::getline`. In C, you can
read a full line of input with `fgets`.

In C++, one way to divide a line of input into tokens is by using
`std::istringstream` like:

```
std::istringstream s(the_string);
while (s >> token) {
    processToken(token);
}
```

In C, one way to divide a line of input into tokens is by using `strsep` like:

```
char *p = the_string;
char *token;
while ((token = strsep(&p, " \t\v\f\r\n")) != NULL) {
    ...
}
```

Note that `strsep` changes the string passed to it.

My reference implementation creates a class to represent each command in a
pipeline (|-separated list of things to run), and a class to represent the
pipeline as a whole. I first collect each command line into a vector of tokens,
then iterate through that vector to create and update command objects.

### Running commands

Pseudocode for running commands is as follows:

```
for each command in the line {
    pid = fork();
    if (pid == 0) {
        do redirection stuff
        execve ( command, args , ...);
        oops, print out a message about exec failing and exit
    } else {
        store pid somewhere
    }
}

for each command in the line {
   waitpid(stored pid, &status);
   check return code placed in status;
}
```

To implement redirection, probably the most useful function is `dup2`, which can
replace `stdin` (file descriptor 0) or `stdout` (file descriptor 1) with another
file you have opened. When redirecting to a file, you will most commonly use
`open()` to open the file, call `dup2` to replace `stdin` or `stdout` with a
copy of the newly opened file descriptor, then `close()` the original file
descriptor. This occurs typically would be done just before the call to `execve`
as in the pseudocode above.

To implement pipelines, the typical technique is to call pipe to obtain a
connected pair of file descriptors, use `dup2` to assign these to `stdout` or
`stdin`, and close the original file descriptor just before calling `execve`.

### Printing Error Messages

In C++, one way to print to `stderr` is using `cerr`, which works like `cout`:

```
#include <iostream>

...

std::cerr << "Some message.\n";
```

In C or C++, one way to print to stderr is using fprintf:

```
#include <stdio.h>

...

fprintf(stderr, "Some message.\n");
```

### Common problems

- My shell hangs

    If pipelines hang, then a likely cause is neglecting to close the ends of
    the pipes to the parent process. (Reads on the pipe will not indicate
    end-of-file until all of the write ends of the pipe are closed.)

- My shell stops working after I run too many commands

    A likely cause is running out of file descriptors by failing to close all
    file descriptors.

### General sources for documentation

All the Unix functions have “manpages” (short for manual pages) retrieved with
the man command. For example, to get documentation on the `pipe()` function, you
can run, from within a Linux environment, run

    man pipe

The `man` command retrieves documentation both for commands and C functions. If
both a command and a function exist with the same name, man by default shows
information about the command. For example, there is a command called write and
a function called write. Running

    man write

gives only the documentation about command. There are two ways to get the
documentation about the function. One is to run

    man -a write

which shows the documentation for all things named "write" — it will show the
documentation for the command and then for the function. Alternately, the
documentation retrieved by man is divided into "sections". You can get a list of
all the entries for a word like "write" along with their sections by running

    man -k write

On my system this shows

```
write (1)            - send a message to another user

write (2)            - write to a file descriptor

write (1posix)       - write to another user

write (3posix)       - write on a file
```

The text in parenthesis are the section numbers/names. For example, you can
access the "write" entry in section 2 using

    man 2 write


Generally, Linux divides its documentation into sections as follows:

- section 1: commands intended for normal users
- section 1posix: commands, but shows the POSIX standard's description (things
  that should be the same on all Unix-like OSs) rather than Linux-specific
  information about a command
- section 2: "low-level" functions that usually wrap a specific system call
- section 3: other functions
- section 3posix: functions, but shows the POSIX standard's description (things
  that should be the same on all Unix-like OSs) rather than Linux-specific
  information about a function
- section 8: commands intended for system administrators

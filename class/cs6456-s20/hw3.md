---
permalink: "/class/cs6456-s20/hw3.html"
layout: single
title:  "CS6456 - HW3"
sidebar:
  nav: "cs6456hw3"
---

<style>
.masthead {
  display: none;
}
</style>



# HW3: Multi-Medium Filesystem

The computing memory hierarchy continues to evolve with new very-fast
non-volatile memories (NVM) supplementing solid-state drives and spinning hard
drives for data storage in computers. OS researchers are designing new
filesystems (like [NOVA](https://www.usenix.org/node/194455) and
[Strata](https://www.cs.utexas.edu/~simon/sosp17-final207.pdf)) to take
advantage of the new storage options, and in this assignment, you will too.

Your task is to design an implement a simple filesystem that supports a
relatively small, but fast and byte-addressable NVM and a slow, but much larger,
block-addressable hard disk. Your filesystem will provide a single interface
for user applications, because remember the operating system is supposed to
hide the hardware details from the user.

After creating the filesystem, you will test its performance with a few tests to
see the effects of your design as well as the different storage technologies.

Download the project files: [hw3_2020-02-24.zip](hw/hw3_2020-02-24.zip).

## Interfaces

Your filesystem will be a userspace library on top of two simulated storage
mediums. Code that uses the filesystem will call the functions you provide. To
actually "write" to and "read" from the storage medium you will call the
functions provided by the simulated storage.

### Application Interface

Your filesystem will provide the following interface:

- `int uva_open(char* filename, bool writeable)`: Opens the file with the given
  filename in the correct mode (either readable or writable). If `writable` is
  `true`, then the file may only be written to. If `writeable` is `false`, then
  the file can only be read from. Returns a positive identifier for the opened
  file if the file was opened successfully. If the file cannot be opened an
  error is indicated by returning <= 0.

- `int uva_close(int file_identifier)`: Close the provided file. Returns `0` on
  success, and `-1` if the file couldn't be closed.

- `int uva_read(int file_identifier, char* buffer, int offset, int length)`:
  Read up to `length` bytes from the file starting `offset` bytes from the end
  of the previous read into `buffer`. Offset must not be less than zero. If the
  file has not been read from before then the `offset` is from the beginning of
  the file. Returns the number of bytes read from the file, or `-1` if there is
  an error.

- `int uva_read_reset(int file_identifier)`: Reset the read position back to the
  beginning of the file.

- `int uva_write(int file_identifier, char* buffer, int length)`: Write `length`
  bytes from `buffer` to the end of the file. Returns `0` if the write is
  successful and `-1` if there is an error.

### Storage Interface

Your filesystem will use the following interface:

- `int disk_write(int block_number, char* buffer)`: Write the contents of
  `buffer` to the block specified by `block_number` to disk. All blocks are 512
  bytes (therefore `buffer` should point to 512 bytes of memory). Returns `0` on
  success and `-1` if the `block_number` is invalid.

- `int disk_read(int block_number, char* buffer)`: Read the contents of block
  `block_number` into the provided buffer. Returns `0` on success and `-1` if
  the `block_number` is invalid.

- `int disk_block_count()`: Returns the number of blocks in the disk.

- `int nvm_write(int byte_number, int length, char* buffer)`: Write `length`
  bytes of `buffer` to the NVM starting at byte number `byte_number`. Returns
  `0` on success and `-1` if the NVM is not large enough to store the entire
  write.

- `int nvm_read(int byte_number, int length, char* buffer)`: Read `length` bytes
  starting at `byte_number` from the NVM and copy them into `buffer`. Returns
  `0` on success and `-1` if the NVM is not large enough to complete the entire
  read.

- `int nvm_byte_count()`: Returns the number of bytes available in the NVM.


## Requirements

The design of the filesystem is up to you, but it must support the following
operations:

- Reading and writing files (of course!). Once opened, a file can only be read
  from or written to based on the flag passed to `uva_open()`. If a user
  attempts to read from a file opened only for writing, for example, an error
  should be returned.

- The filesystem must be able to store more data than can fit in just the disk
  or nonvolatile memory. That is, you cannot just ignore one medium.

- The filesystem must support filenames at least 127 bytes long.

- The filesystem must persist if the userspace process exits and restarts. The
  storage library emulates nonvolatile storage by using files in the host
  filesystem. If one userspace process uses your filesystem and then finishes,
  any files it creates should still be visible if a new userspace process uses
  the filesystem.

  Note, your filesystem does not need to handle unexpected crashes. Also, you
  can assume that only one process uses the filesystem at a time.


## Implementation

You may implement the filesystem in C or Python. You can really use any
language, but you are then responsible for setting up the tests. Note: if you
use Python, the underlying storage will still be in a shared library from C. To
create buffers to pass to the disk and nvm, use `ctypes.create_string_buffer()`.


## Testing

Towards the bottom of test.py you should choose the version (C or Python) you
have implemented. Then you can call the `run_test()` function with a test name.

Running the test script looks something like:

```bash
$ make             # generate the shared library from C
$ python3 test.py  # run the tests
```

Since filesystems are persistent, the files from previous tests will be
preserved unless the raw storage files are deleted.

Since the underlying storage is always implemented in C, you need to run `make`
at least once when implementing the filesystem in Python.

## Debugging

The two filesystems are stored as just regular binary files. Therefore, you can
view their contents like so:

    $ hexdump -C disk.bin | less
    $ hexdump -C nvm.bin | less

## Deliverables

1. The implementation of your filesystem.

2. A figure showing the performance of your filesystem when creating small
   files. The x-axis should be the number of files. The y-axis should be time.
   You should time how long it takes your filesystem to create X number of 256 B
   files, where X ranges from 0 to 500 skipping by 10. The filesystem should be
   erased between each test. The `test_small_files.py` script may be helpful.
   You should name your graph `small_files` with an appropriate extension.

3. A figure showing the performance of your filesystem when creating files of
   different sizes. The x-axis should be filesize. The y-axis should be time.
   You should time how long it takes your filesystem to write a single file of
   size X, where X ranges from 0 bytes to 30000 bytes, skipping by 1000 bytes.
   The filesystem should be erased between each test. You should name your graph
   `single_file` with an appropriate extension.

4. A CDF showing the read performance of your filesystem. The x axis should be
   time, and the y axis should be percentage of reads that took that amount of
   time or less to complete. The filesystem should be populated with many random
   length files, and then you should time how long it takes to read them back.
   You should repeat this several times with a newly randomly generated set of
   files in the file system. You may find `test_random_files.py` useful for
   this.You should name your graph `random_file_read_cdf` with an appropriate
   extension.

## Submission

Submit the code and figures in a .zip file on Collab.




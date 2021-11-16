---
permalink: "/class/cs6456-s20/hw4.html"
layout: single
title:  "CS6456 - HW4"
sidebar:
  nav: "cs6456s20hw4"
---

<style>
.masthead {
  display: none;
}
</style>



# HW4: Mini-Virtualization

Virtualizing computing resources is essential for enabling modern cloud
computing. However, the debate between virtual machines and containers continues
to be contentious:

- [SCONE: Secure Linux Containers with Intel SGX](https://www.usenix.org/conference/osdi16/technical-sessions/presentation/arnautov)
- [My VM is Lighter (and Safer) than your Container](https://dl.acm.org/doi/10.1145/3132747.3132763)
- [Slacker: Fast Distribution with Lazy Docker Containers](https://www.usenix.org/node/194431)

While we won't be able to settle this debate in this homework, we can get some
experience with containers by writing the beginnings of a container manager.

## Task Overview

Your task is to write a program for Linux that can run two instances of this
program simultaneously:

```python
#!/usr/bin/env python3

import http.server

class HttpRecorder(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print('GET request for {}\n'.format(self.path))

        # And log this action.
        with open('/tmp/http_recorder.log', 'a') as f:
            f.write('GET request for {}\n'.format(self.path))

        http.server.SimpleHTTPRequestHandler.do_GET(self)


def run(server_class=http.server.HTTPServer, handler_class=HttpRecorder):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
```

You should be able to copy the code to a file and run it successfully. If you go
to `localhost:8080` in a browser you should see a file listing, the GET requests
should print, and you should see the requests in the temporary file. However, if
you try to run a second copy you will get a port in use error. If you change the
port number then two copies should run, but the requests will be interleaved in
the tmp file making debugging difficult!

Your program should start two copies of this exact program, and each copy should
run as if it is the only copy executing. That is, it should be able to bind to
port 8080. Optionally, it should be able to write to `/tmp/http_recorder.log` as
though it is the only process using that logging file. Put another way, each
copy of the program should be in a virtualized environment.

Supporting this is a common use for virtualization, as software is often written
assuming a particular port or some set of resources, and the author of the
software doesn't usually know what other software a user wants to run with it.
Sometimes this is solved with configuration files, but that leads to a very
static solution that requires careful system management to avoid conflicts. A
container solution is more dynamic and general.

## Requirements

- This only needs to work on Linux.
- You must save the code above to `http_recorder.py`, make it executable, and
  have your container manager start two copies of it. You may not change
  `http_recorder.py`.
- You do not need to virtualize all resources, or provide protections around
  sharing resources, except for networking resource (specifically port 8080).
  For extra credit you can virtualize the the file `/tmp/http_recorder.log`. If
  you want to virtualize more that is fine, but your container manager need only
  work for this exact program.
- Your program should not take any arguments. Running your container manager
  should just be running `./uva_container`, with an optional `make` step:

    ```bash
    $ make # optional
    $ ./uva_container
    ```
- You cannot use Docker, or other third-party container tool.
- You should include a `README.md` file that explains how your container manager
  handles the two copies of `http_recorder.py` both wanting to use the same
  port and what policy it implements.
- You can write this in any common programming language you want. Any
  compilation or setup steps should be handled by `make`.

## Extra Credit

For the standard version of this assignment you do not need to virtualize the
log file. For extra credit, you can make it so that each copy of the program has
its own view of `/tmp/http_recorder.log` so that each copy logs to different
files.

## Testing

If you run one copy of the example Python program directly (i.e. without any
additional code that you have written) you should be able to go to
`http://localhost:8080` in a browser and see a directory list. You can also use
it to download files. Any requests that you make should be printed out and
logged to the log file.

With your containerization code, you can now run two copies of the example
program in different directories. You should be able to access each of them
through the browser (the specific method will depend on how you are handling
virtualizing the port) and see the different directory listings for each. You
should also see the different requests you make in each copy's log file.


## Submission

Submit the code and readme in a .zip file on Collab.


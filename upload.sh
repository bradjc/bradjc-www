#!/usr/bin/env bash

jekyll build
rsync -a _site/ bjc8c@power2.cs.virginia.edu:~/public_html/


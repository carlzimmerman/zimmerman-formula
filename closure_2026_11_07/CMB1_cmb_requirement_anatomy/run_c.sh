#!/bin/bash
# CMB1 block C fits, one after another (one thread, < 1 GB), then post. kappa = 1/2 FITTED; not theory closed.
set -e
for k in E B; do for f in canonical alt; do nice python3 cmb1.py fit $k $f; done; done
nice python3 cmb1.py post

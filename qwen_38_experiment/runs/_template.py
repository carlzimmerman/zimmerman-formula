#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tNNN_<slug>.py -- <one-line hypothesis, copied from TASKS.md>

PASS criteria (copied verbatim from TASKS.md BEFORE computing):
  - ...
KILL criteria:
  - ...
Search? If yes: trial count pre-registered in REGISTRY_FDR.md on <date>.
Direction-of-risk: <WIN-risk | DEFICIT-risk | both>, because <one line>.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *   # constants, kernel, check/info/finish

# PART A -- restate inputs with provenance (committed stage / paper / measured datum)
# PART B -- compute.  Both footings for anything dimensional (loop over FOOTINGS).
# PART C -- grade against the PASS/KILL criteria with check(...) calls.

finish("tNNN")

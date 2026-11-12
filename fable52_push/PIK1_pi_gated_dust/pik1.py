#!/usr/bin/env python3
"""PIK1 (lane HY4-3): grade the two-variable clock dust term

    L_K(Q, Pi) = (mu_K^2 / (2K)) (Q - 1)^2 S(Pi / Pi_c),   Pi = D_m P^m,   S(0) = 1, S decreasing,

inside action (A) of QX17.   MK1's closing requirement was that the dust "cannot depend on the clock
offset alone"; DT1 kills every one-variable n(x), x = Q - 1, but assumes exactly that.   This lane
grades the two-variable escape: the dust also reads Pi, the law's own halo (screening) density, which
action (A) already carries through gamma_L F(Pi).

    python3 pik1.py            -> pik1.out / pik1.json
    python3 pik1.py --mutate   -> pik1_MUTATE.out / .json

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
"""
import json
import math
import os
import sys
import time

import numpy as np

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
ROOT = os.path.dirname(REPO)
DATA = os.path.join(ROOT, "real_research", "data")
KD1J = os.path.join(ROOT, "closure_2026_11_06", "KD1_unpinned_kq_dust", "kd1.json")
ONE1J = os.path.join(REPO, "ONE1_counted_once", "one1.json")
NOTE = "kappa = 1/2 FITTED; not theory closed. Adopts nothing."

NC = 3
IDX = [0, 1, 2]
_tt, _xx, _yy = sp.symbols('tt xx yy')
CO = (_tt, _xx, _yy)
FOOT = ('canonical', 'alt')
A0 = {'canonical': 9.360324825027975e-11, 'alt': 1.1312035414413022e-10}
G_ = 6.674e-11
MSUN = 1.989e30
PC = 3.0857e16
KPC = 1e3 * PC
MPC = 1e6 * PC
CC = 2.99792458e8
KAPPA = 0.5
XMIN = 1e-5
MUT = '--mutate' in sys.argv
T0 = time.time()
OUT = []
OUTJ = {}


def P_(s):
    print(s, flush=True)
    OUT.append(s)

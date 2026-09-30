#!/usr/bin/env python3
"""v00_declared_hypotheses.py -- the candidate list for the coefficient Z in a0 = c H / Z, DECLARED BEFORE ANY LIKELIHOOD IS COMPUTED.

Written (and its sha256 printed) before the a0 determinations were collected and before any posterior or Bayes factor was
built. Later scripts import HYPOTHESES from here and print the hash of this file, so the list cannot be edited after the fact
without the hash changing. Nothing here is fitted to data; each Z is either a published/record value or a named control.

Z is defined on the SAME footing as the data comparison: a0 = c H_eff / Z with H_eff = H0 (rho_total footing) or
H0 sqrt(Omega_Lambda) (rho_Lambda footing). kappa (framework convention a0 = kappa c sqrt(G rho)) = sqrt(8 pi/3)/Z.
"""
import math, hashlib, sys, os

# (key, Z, provenance, class)   class: 'candidate' (real hypothesis) or 'control' (must be rejected; used for mutation checks)
HYPOTHESES = [
    ("F   framework kappa=1/2",         math.sqrt(32 * math.pi / 3), "record: Lambda = 32 pi a0^2 (kappa = 1/2, FITTED)",             "candidate"),
    ("V   Verlinde a0 = cH0/6",         6.0,                         "Verlinde 2016 arXiv:1611.02269 (rational Z, conditional derivation)", "candidate"),
    ("M   Milgrom cH/2pi",              2 * math.pi,                 "Milgrom empirical near-equality 2 pi a0 ~ cH (arXiv:2001.09729)", "candidate"),
    ("K1  forced kernel kappa=1",       math.sqrt(8 * math.pi / 3),  "record: Friedmann-forced kernel, Z = sqrt(8 pi/3)",              "candidate"),
    ("N   Nariai shell 3 sqrt 3",       3 * math.sqrt(3),            "record p03/README 6: Nariai-shell coefficient",                 "candidate"),
    ("P   van Putten 1/2+pi sqrt2",     0.5 + math.pi * math.sqrt(2), "van Putten arXiv:1411.2665: a0 = 2cH0/(1+2 pi sqrt2)",       "candidate"),
    ("Q   kappa=1/2pi (framework conv.)", math.sqrt(8 * math.pi / 3) * 2 * math.pi, "record's 'kappa = 1/2pi' read in the kappa*c*sqrt(G rho) convention (eq01: NOT Milgrom's cH/2pi)", "candidate"),
    ("C1  control: a0 = 2cH (T-T_L family)", 0.5,                   "Milgrom 1999/Smolin/Klinkhamer-Kopp a0 = 2 c H: must be rejected", "control"),
    ("C2  control: Z = 12",             12.0,                        "absurd coefficient: must be rejected",                          "control"),
]

def declared_hash():
    return hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()

if __name__ == "__main__":
    print("DECLARED hypothesis list (before any data were collected or any likelihood computed)")
    for k, z, prov, cls in HYPOTHESES:
        print(f"  {k:<38} Z = {z:8.5f}   kappa = {math.sqrt(8*math.pi/3)/z:.4f}   [{cls}]  {prov}")
    print("sha256 of this file:", declared_hash())
    sys.exit(0)

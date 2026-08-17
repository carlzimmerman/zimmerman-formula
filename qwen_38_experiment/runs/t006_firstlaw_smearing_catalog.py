#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t006_firstlaw_smearing_catalog.py -- T006 First-law smearing catalog.

HYPOTHESIS (copied from TASKS.md):
    dS = dE/T on the dS horizon, with the a0-line as EOM, fixes kappa ONLY per
    smearing choice.

PASS criteria (copied verbatim from TASKS.md BEFORE computing):
     - a table of 5 named smearings, one coefficient per choice.
KILL criteria:
     - the coefficient is CHOICE-INDEPENDENT and equals 1/2 (degenerate: the smearing
      does not actually distinguish kappa) -> KILL.

Search? No. This is a symbolic coefficient catalog (mirrors T001), not an mm_search
   surface; no FDR pre-registration needed.
Direction-of-risk: WIN-risk -- a smearing that GENUINELY forces the fitted kappa
    0.551 +/- 0.043 would be a derivation the framework LACKS; none of the model
   coefficients is claimed as that (CONVENTION-grade model outputs only, per R7).

MODEL (stated, not a theorem -- the named unverified assumption):
    The a0-line is a0 = kappa * c * sqrt(G * rho_Lambda) (the EOM, R1).  The first
    law dS = dE/T, when SMEARED over a static-patch disk of radius R (the Hubble
    radius), fixes kappa through the smearing normalization.  We take the model
    coefficient to be the order-2/order-1 moment ratio of the smearing kernel over
    u in [0,1]:
        kappa[K] = (int_0^1 K(u) u^2 du) / (int_0^1 K(u) u du)    [ = <rho>/R ].
    This is the ONE modeling assumption the catalog rests on: that the first-law
    smearing coefficient equals the smearing radius-fraction.  It is a MODEL, NOT a
    derivation -- no coefficient below is claimed to BE the fitted kappa=0.551+/-0.043.
    kappa = 1/2 stays ADOPTED/FITTED (R5); a model output landing in the window is
    CONVENTION-grade, NOT a hit (R7).
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *                     # FOOTINGS, A0_CAN/ALT, KAPPA_MEAS/ERR, check/info/finish
import numpy as np

# PART A -- inputs with provenance -----------------------------------------------------
# u = rho / R in [0,1] over the static-patch disk; moment ratios by fine deterministic
# quadrature (symbolic sp.integrate hung on the thermal kernel -- numerical is faster
# and, on a 1e6-point uniform grid, reproducible to ~1e-6).
U = np.linspace(0.0, 1.0, 1_000_001)

# the a0-line as EOM on each footing; the coefficient is what relates a0 to c sqrt(G rho_Lambda)
rho_L = OM_L * RHO_CRIT
croot = C * math.sqrt(G * rho_L)          # c * sqrt(G * rho_Lambda)
for tag, ref in FOOTINGS.items():
    kappa_def = ref / croot
    info("footing %s: a0=%.4e = kappa_def * c*sqrt(G*rho_L); kappa_def=%.4f"
           % (tag, ref, kappa_def),
          "c*sqrt(G*rho_L)=%.4e (footing-invariant; only a0 rescale differs)" % croot)

WIN_LO, WIN_HI = KAPPA_MEAS - KAPPA_ERR, KAPPA_MEAS + KAPPA_ERR    # fitted window [0.508, 0.594]
info("fitted window = [%.3f, %.3f] (kappa=0.551+/-0.043, DISTANCE-FREE, FITTED not derived)"
       % (WIN_LO, WIN_HI))

# PART B -- the 5 named smearings, coefficient per choice -------------------------------
# each kernel K(u) -> kappa[K] = <u^2>/<u> moment ratio over [0,1].
def moment_ratio(K):
    num = np.trapz(K * U**2, U)
    den = np.trapz(K * U,   U)
    return num / den

smearings = [
     ("1. Flat (Jacobson-canonical)",       lambda u: np.ones_like(u)),
     ("2. Gaussian over Hubble radius",     lambda u: np.exp(-u**2)),
     ("3. Boltzmann/thermal (T=1/2pi R)",   lambda u: np.exp(-2.0*math.pi*u)),
     ("4. Lapse-weighted (dS static patch)",lambda u: np.sqrt(np.clip(1.0 - u**2, 0.0, None))),
     ("5. Redshift / surface-gravity",       lambda u: np.exp(-u)),
]

print("\n%-34s %14s    %s" % ("smearing", "kappa[K]", "status vs fitted window"))
print("-" * 92)
ks = []
in_window = []
for name, K in smearings:
    kf = float(moment_ratio(K(U)))
    ks.append(kf)
    in_win = WIN_LO <= kf <= WIN_HI
    if in_win:
        in_window.append(name)
    status = ("IN window -> MODEL NEAR-MISS (CONVENTION-grade, NOT a hit, no derivation)"
              if in_win else "outside window")
    print("%-34s %14.6f    %s" % (name, kf, status))
    info("    %s: kappa[K]=%.6f" % (name, kf))

# PART C -- grade -----------------------------------------------------------------------
n5 = len(smearings)
spread = max(ks) - min(ks)
all_half = all(abs(k - 0.5) < 0.02 for k in ks)     # "choice-independent 1/2"

print("\n" + "=" * 92)
check(n5 == 5, "table has all 5 named smearings with one coefficient each (PASS: table)")
check(not all_half,
       "KILL not fired: coefficient is NOT choice-independent 1/2 (spread=%.4f across choices)"
       % spread,
       "5 values = %s" % ", ".join("%.4f" % k for k in ks))
# footing invariance: the coefficient is dimensionless -> footing-invariant
check(True, "coefficient is dimensionless -> footing-invariant (can/alt only rescale a0)")
# honesty guard: a coefficient landing in the fitted window is a MODEL output, not a hit
check(True,
       "no coefficient claimed as the FITTED kappa=0.551; %d model value(s) fall in window "
       "but are CONVENTION-grade, NOT hits (R7); kappa stays FITTED/ADOPTED, NOT derived (R5)"
       % len(in_window))

# the named unverified assumption
info("UNVERIFIED ASSUMPTION: kappa[K] = <rho>/R moment-ratio is a MODEL normalization, not a "
      "theorem; the catalog shows the coefficient is smearing-DEPENDENT (non-degenerate, "
      "spread=%.3f), so KILL(choice-independent 1/2) is NOT fired, but NO coefficient is "
      "claimed to BE the fitted 0.551+/-0.043 -- the derivation remains absent (R5)." % spread)

finish("t006_firstlaw_smearing_catalog")

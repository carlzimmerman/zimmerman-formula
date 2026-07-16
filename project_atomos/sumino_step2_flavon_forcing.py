#!/usr/bin/env python3
"""
SUMINO STEP 2 -- Q1: does the SU(3)_F flavon potential FORCE the Koide amplitude r=sqrt2,
or is sqrt2 tuned via a free coupling ratio?  This is the load-bearing forcedness test.

Setup: the charged-lepton sqrt-masses are the eigenvalues (l1,l2,l3) of the flavon VEV (a
Hermitian 3x3 -> 1+8 of SU(3)_F). SU(3)_F invariants of the VEV are the 3 power sums
  p1=Sum l, p2=Sum l^2, p3=Sum l^3.
Koide amplitude:  Q_flavon = p2/p1^2 ;  r = sqrt(2(3Q-1)) ;  Koide 2/3 <=> p2/p1^2 = 2/3 <=> r=sqrt2.

The forcedness question reduces to: is p2/p1^2 = 2/3 pinned by ANY SU(3)_F-invariant potential,
or is it a free ratio of two independent invariants set by the potential's couplings?
"""
import numpy as np
from scipy.optimize import minimize
np.seterr(all="ignore")

def koideQ(l):
    l = np.asarray(l, float)
    return (l**2).sum() / (l.sum()**2)   # = p2/p1^2

# --- (A) geometric fact: p2/p1^2 is a FREE ratio of independent invariants, spans [1/3, 1] ---
rng = np.random.default_rng(0)
vals = []
for _ in range(200000):
    l = np.sort(rng.uniform(0.1, 3.0, 3))
    vals.append(koideQ(l))
vals = np.array(vals)
print("="*80)
print("Q1 -- is r=sqrt2 (p2/p1^2=2/3) FORCED by an SU(3)_F invariant, or a free ratio?")
print("="*80)
print(f"  p2/p1^2 over random positive eigenvalue triples: range [{vals.min():.3f}, {vals.max():.3f}]")
print(f"  (theory: p2/p1^2 in [1/3, 1]; 1/3=degenerate, 1=one-nonzero). 2/3 is an INTERIOR value.")
print( "  p1 and p2 are INDEPENDENT SU(3)_F invariants -> their ratio is freely dialable; NO invariant")
print( "  relation pins p2/p1^2=2/3. So sqrt2 is NOT forced by group theory alone -- it must come from")
print( "  the POTENTIAL's minimum, i.e. from chosen couplings.\n")

# --- (B0) a GENERIC SU(3)_F-invariant potential does NOT even produce the Koide split ---
# Symmetric renormalizable V in the eigenvalues; minimize from many starts. Generic couplings
# land on the DEGENERATE minimum (l1=l2=l3 -> Q=1/3, equal masses), NOT the Koide alignment.
def Vgeneric(x, c):
    l = np.abs(x) + 1e-6
    p1, p2 = l.sum(), (l**2).sum()
    return np.sum((l**2 - 1.0)**2) + c*(p1 - 3.0)**2     # generic invariant, coupling c
print("  (B0) generic SU(3)_F-invariant potential -> minimum is DEGENERATE (Koide split is NON-generic):")
for c in [0.0, 0.5, 1.0, 2.0]:
    best=(1e18,None)
    for _ in range(30):
        r = minimize(Vgeneric, rng.uniform(0.2,2.0,3), args=(c,), method="Nelder-Mead",
                     options=dict(xatol=1e-9, fatol=1e-11, maxiter=4000))
        if r.fun < best[0]: best=(r.fun, np.sort(np.abs(r.x)+1e-6))
    l=best[1]; print(f"       c={c:.2f}: min l={np.array2string(l,precision=3,floatmode='fixed')}  Q={koideQ(l):.4f} (=1/3 => degenerate)")
print("       -> producing the Koide split at all requires SPECIFICALLY ENGINEERED terms. That is")
print("          Sumino's construction: the alignment is put IN by hand, not a generic output.\n")

# --- (B) the engineered circulant/Koide minimum  l_i = v(1 + h cos(2pi i/3 + delta)):
#     then Q = (1 + h^2/2)/3 EXACTLY -> Koide 2/3 <=> h = sqrt2 (a TUNED amplitude), and Q is
#     INDEPENDENT of delta (delta is a free knob absorbing the 3 masses). Two free inputs (h, delta),
#     neither fixed by SU(3)_F. ---
def circ(h, delta, v=1.0):
    return v*(1 + h*np.cos(2*np.pi*np.arange(3)/3.0 + delta))
print("  (B) engineered circulant minimum  l_i = v(1 + h*cos(2pi i/3 + delta)):  Q = (1 + h^2/2)/3")
print(f"      {'h (amplitude)':>13} {'Q':>9} {'r':>7}   note")
for h in [0.0, 0.5, 1.0, np.sqrt(2), 1.6, 2.0]:
    l=circ(h, 0.6); Q=koideQ(l); rr=np.sqrt(max(0,2*(3*Q-1)))
    note = "  <- Koide 2/3 : needs the TUNED value h=sqrt2" if abs(h-np.sqrt(2))<1e-6 else ""
    print(f"      {h:>13.4f} {Q:>9.5f} {rr:>7.4f}{note}")
# confirm Q independent of delta (so delta is genuinely free):
qs=[koideQ(circ(np.sqrt(2), d)) for d in np.linspace(0,2*np.pi,9)]
print(f"      Q at h=sqrt2 across delta in [0,2pi): min={min(qs):.6f} max={max(qs):.6f}  (constant => delta FREE)")
print("      -> the minimum needs h=sqrt2 (amplitude TUNED, Q1) AND a FREE delta (Q2). SU(3)_F fixes neither.\n")

print("="*80)
print("CONSOLIDATED VERDICT -- Sumino SU(3)_F vs the gate (both-ways, no manufactured result)")
print("="*80)
print("""  STEP 1 (real): QED running spoils Koide by ~1.3e-3 (flavor-dependent); Sumino's family gauge
    bosons CAN cancel it -> a GENUINE robustness mechanism (this part is real physics, not numerology).
  Q1 (this step): r=sqrt2 is NOT forced -- p2/p1^2 is a free ratio of two independent SU(3)_F
    invariants; the potential's minimum hits 2/3 only at a tuned coupling. sqrt2 is INPUT.
  Q2 (brute force): the phase delta stays FREE (absorbs the 3 masses, residual ~3e-6); the same
    structure forces NO 2nd independent observable -> no overdetermination.

  GATE VERDICT: NOT CERTIFIED. Sumino's SU(3)_F HOSTS Koide (and protects it under running) but does
  NOT close the gate: the amplitude is tuned (Q1), no 2nd observable is forced (Q2), and the family-
  gauge scale (~10^2-10^3 TeV) + FCNC control are further knobs. Status = REAL-PUZZLE-RE-LABELED,
  improved -- the honest ~2/3-decades verdict, reproduced from first principles, NOT a manufactured win.

  WHAT WOULD CLOSE IT (the genuinely-new physics still needed): a symmetry that (i) FIXES the
  invariant ratio p2/p1^2=2/3 as a group Casimir / anomaly condition (forcing sqrt2 with no knob),
  AND (ii) forces delta via the SAME structure (a 2nd observable: a mixing angle or the neutrino
  sector) -- giving overdetermination. Nobody has this; it is the open flavor problem. The a0/Z
  gravity kernel does NOT help (number-field obstruction: sqrt(pi)-transcendental vs algebraic flavor).""")
print("EXIT 0")

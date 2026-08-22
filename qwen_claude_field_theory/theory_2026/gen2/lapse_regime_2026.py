#!/usr/bin/env python3
r"""Which term controls the lapse constraint itself?  A structural result, not a number.

The operator acting on delta N in the Gen-2 lapse equation has two pieces:
    from eta_K a^2 and F_X          :  (eta_K + F_X) k^2
    from Y_a ~ (D_<i D_j> ln N)^2   :  eps A (c^4/a0^2) k^4
Their ratio is eps A (k c^2/a0)^2 -- the SAME anti-suppression that killed Gen-1, but now
inside the CONSTRAINT rather than inside the operator.
"""
import numpy as np
c=2.99792458e8; a0=9.3619e-11; L=c**2/a0; eps=1.1e-24; A=0.03
print(f"  {'band':<24}{'k [1/m]':>12}{'eps A (kL)^2':>16}{'regime':>18}")
for f,lab in ((1e-18,"cosmological ~ H0"),(1e-8,"galactic 1/(3 kpc)"),(1.0,"1 Hz"),
              (35.0,"GW170817 low band"),(100.0,"LIGO 100 Hz"),(1e3,"LIGO 1 kHz")):
    k=2*np.pi*f/c if f>1e-12 else f
    r=eps*A*(k*L)**2
    print(f"  {lab:<24}{k:>12.3e}{r:>16.3e}{('k^4 DOMINATES' if r>1 else 'k^2 dominates'):>18}")
kc=1/(L*np.sqrt(eps*A))
print(f"\n  crossover  k = 1/(L sqrt(eps A)) = {kc:.3e} 1/m"
      f"   ({2*np.pi/kc/9.461e15:.3f} ly, {kc*c/(2*np.pi):.2e} Hz)")
print("""
STRUCTURAL CONSEQUENCE (not a value for kappa):
  At every LIGO frequency the FOURTH-order term dominates the operator determining delta N.
  The constraint solve is therefore NOT in the naive elliptic regime nabla^2 delta N = source.
  Outcome (i) as previously written is not the right default.
  A_nn ~ eps A (c^4/a0^2) k^4, so the reduced correction A_ngamma^2/A_nn carries 1/eps: the
  indirect channel GROWS as eps shrinks and cannot be switched off by weakening the coupling.
  The eps -> 0 limit stays smooth only because the k^2 piece takes over below the crossover.

DELIBERATELY NOT CONVERTED into kappa or H_T: an order-of-magnitude pass gave results I
could not reconcile with the known khronometric tensor mass (|m| ~ a0/c^2, observationally
nil), which says the O(1) bookkeeping dominates the scaling here.  That is the
constraint-reduced calculation's job, and it is running.
""")

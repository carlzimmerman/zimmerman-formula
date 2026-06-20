#!/usr/bin/env python3
"""
ADVERSARIAL STEELMAN for a GENUINE distinctive signature:
Even if the c_s^2 (k^2 gradient) amplitude eps1 is dialed to zero (the data-favored
CDM-mimicking point), the GHOST CONDENSATE has a term Scherrer k-essence does NOT:
the higher-derivative (nabla^2 pi)^2/M^2 operator giving omega^2 = (alpha/M^2) k^4
(ACLM Eq 2.11). At the EXACT condensate (P_X=0) this k^4 term is the LEADING spatial
operator and its coefficient is fixed by M (NOT by the free eps1). So: is there a
NON-TUNABLE, M-pinned k^4 feature in P(k)/CMB at the framework's M ~ 0.04-1 eV?

This is the strongest both-ways test: if the k^4 scale lands in an observable window
with an M-fixed coefficient, that's a GENUINE distinctive front. If it's out of window,
honest null.

ACLM k^4 dispersion: omega^2 = (alpha/M^2) k^4  (alpha ~ O(1)).
The k^4 mode matters when its frequency competes with gravity/expansion. The relevant
comparison (ACLM Eq 2.14): the k^4 term vs the gravity-mixing k^2 Jeans term:
   omega^2 = (alpha/M^2) k^4 - (alpha M^2 / 2 M_Pl^2) k^2
The crossover (where k^4 dominates over the gravitational k^2) is at
   k_* : (alpha/M^2) k_*^4 = (alpha M^2/2 M_Pl^2) k_*^2  =>  k_*^2 = M^4/(2 M_Pl^2)
   => k_* = M^2 / (sqrt(2) M_Pl)     [the ACLM scale 'm', their Eq 2.15: L_c ~ M_Pl/M^2]
For k > k_*: pure k^4 (stable, oscillatory). For k < k_*: Jeans instability (cured by dS).
The k^4 'feature' (departure from a normal c_s^2 k^2 fluid) is most visible AROUND k_*.
"""
import numpy as np
c=2.99792458e8; G=6.67430e-11; hbar=1.054571817e-34
Mpc=3.0856775814913673e22; eV=1.602176634e-19
M_Pl_red_eV=2.435e18*1e9      # reduced Planck mass eV
h=0.674                       # dimensionless Hubble
# physical length per eV^-1:  l = hbar c / E
def len_per_eV(E_eV):
    return hbar*c/(E_eV*eV)   # meters for E in eV (Compton-like)

print("="*80)
print("ACLM scale k_* = M^2/(sqrt(2) M_Pl): k^4 vs gravitational-k^2 crossover")
print("="*80)
print("  This is a PHYSICAL (today) wavenumber set by M alone (eps1-independent).")
print(f"  {'M (eV)':>10} | {'k_* (m^-1)':>14} | {'k_* (Mpc^-1)':>14} | {'lambda_* = 2pi/k_*':>22}")
print("  "+"-"*70)
for M_eV in [0.04,0.1,0.15,1.0,10.0]:
    k_star_eV = M_eV**2/(np.sqrt(2)*M_Pl_red_eV)   # in eV (energy)
    # convert energy k_star (eV) to inverse length: k[m^-1] = k_star_eV*eV/(hbar c)
    k_star_m = k_star_eV*eV/(hbar*c)
    k_star_Mpc = k_star_m*Mpc
    lam = 2*np.pi/k_star_m
    # express lambda in convenient units
    lam_Mpc = lam/Mpc
    if lam_Mpc>1e3:
        lamstr=f"{lam_Mpc:.3e} Mpc"
    elif lam>3.086e16:
        lamstr=f"{lam/3.086e16:.3e} pc"
    else:
        lamstr=f"{lam:.3e} m"
    print(f"  {M_eV:>10.2f} | {k_star_m:>14.3e} | {k_star_Mpc:>14.3e} | {lamstr:>22}")
print()
print("  Observable cosmology: k ~ 1e-4 to ~10 h/Mpc ~ 1e-4 to 15 Mpc^-1 (comoving).")
print("  CORRECTION to a naive guess: k_* is NOT super-horizon -- for M=0.04-1 eV it lands")
print("  at k_* ~ 0.07-45 Mpc^-1, i.e. RIGHT IN / above the observable window. So we must")
print("  check the PHYSICS at k ~ k_*, not dismiss it on scale grounds. Below k_* the mode")
print("  has the (dS-cured) Jeans branch; above k_* the pure k^4 branch. The decisive question")
print("  is whether the k^4 DYNAMICS makes the field cluster DIFFERENTLY from CDM at these k.")
print()

print("="*80)
print("Is the k^4 mode's intrinsic frequency fast or slow vs Hubble at observable k?")
print("="*80)
print("  omega_k4 = (hbar c k)^2 / (M c^2) / hbar  (natural units omega=k^2/M, energy units).")
print("  Compare to H0. If omega_k4 >> H0 -> fast oscillation, averages to smooth cold dust.")
print("  If omega_k4 << H0 -> the mode is OVER-DAMPED / Hubble-frozen (cannot respond on its")
print("  own dispersion within a Hubble time) -> ALSO behaves as inert cold dust (frozen).")
print("  Either limit => cold dust; only omega_k4 ~ H0 could give distinctive dynamics.")
H0_s=h*100e3/Mpc
for M_eV in [0.1,1.0,10.0]:
    E_M=M_eV*eV
    print(f"  --- M = {M_eV} eV ---")
    for k_hMpc in [0.01,0.1,1.0]:
        k_phys=k_hMpc*h/Mpc
        E_k=hbar*c*k_phys
        omega_k4=(E_k**2/E_M)/hbar    # s^-1
        print(f"     k={k_hMpc:5.2f} h/Mpc: omega_k4 = {omega_k4:.3e} s^-1 ; omega_k4/H0 = {omega_k4/H0_s:.3e}")
print()
print("  RESULT: omega_k4/H0 ~ 1e-25 to 1e-31 -- i.e. omega_k4 << H0 by 25-31 orders at every")
print("  observable k for M=0.1-10 eV. The k^4 mode's intrinsic frequency is ASTRONOMICALLY")
print("  BELOW Hubble => it is OVER-DAMPED / Hubble-frozen: it cannot oscillate or pressure-")
print("  support within ~1e25-1e31 Hubble times, so it is dragged passively by gravity = COLD")
print("  DUST. (Same Hubble-friction freezing that cures the Jeans branch: H >> any GC rate,")
print("  banked H/Gamma~1e25-1e31. ACLM's own low-M statement: 'no cosmological experiment can")
print("  distinguish the ghost-driven acceleration from a cosmological constant'.)")
print()
print("  Why so slow: the k^4 dispersion makes a LOW-k (cosmological) mode have a frequency")
print("  ~k^2/M that is tiny because cosmological k (~1e-30 eV) is minuscule vs M (~0.1 eV):")
print("  omega ~ k^2/M ~ (1e-30 eV)^2/(0.1 eV) ~ 1e-59 eV -> period ~1e25-31 Hubble times.")
print("  The k^4 stiffness HELPS coldness here (higher power of small k = even smaller omega).")
print()

print("="*80)
print("ADVERSARIAL VERDICT")
print("="*80)
print("  The k^4/M^2 operator is the ONE genuinely-ghost-condensate (eps1-independent,")
print("  M-pinned) structure beyond Scherrer k-essence. Steelman checked carefully:")
print("   - its crossover k_* = M^2/(sqrt2 M_Pl) IS in the observable k-range for M=0.04-1 eV")
print("     (k_* ~ 0.07-45 Mpc^-1) -- so it cannot be dismissed on scale grounds; BUT")
print("   - the k^4 mode's intrinsic frequency omega_k4 = (hbar c k)^2/(M c^2 hbar) is BELOW H0")
print("     by ~25-31 orders at every observable k -> Hubble-OVER-DAMPED -> frozen -> tracks")
print("     gravity as cold dust; AND the Jeans branch (k<~k_*) has growth time T_c~M_Pl^2/M^3")
print("     >> age of universe and is dS-Hubble-friction-cured (banked H/Gamma~1e25-1e31).")
print("   => NO distinctive k^4 imprint anywhere in the observable P(k)/CMB window.")
print("  The k^4 feature is genuine in the Lagrangian but its DYNAMICAL CONSEQUENCES are")
print("  unobservable at the framework's M -> degenerate with CDM. This CLOSES the steelman:")
print("  even the non-tunable, M-pinned part of the ghost-condensate dispersion produces no")
print("  falsifiable departure from LCDM-CDM. HONEST NULL, both ways -- not manufactured away")
print("  (the operator is real, k_* is observable-scale), not promoted (omega_k4<<H freezes it).")

#!/usr/bin/env python3
r"""
Observational strengthening of the Candidate-B (curvature-QUMOND) luminality no-go.

CURVATURE_QUMOND_ADM_NO_GO.md proves: exact exponential MOND on a regular spherical branch forces
    lambda_r = -a0 y e^{-y} != 0,
while EXACT tensor luminality relative to the minimally-coupled physical metric (c_T^2 = 1/(1-2 lambda))
forces lambda == 0 pointwise.  That is a contradiction under EXACT luminality.

This script asks the sharper adversarial question: does the kill survive if one only demands
GW170817-level luminality, |c_T/c - 1| < 7e-16, along paths that cross galactic MOND zones?

Result: YES, by 5-8 orders.  Integrating the forced lambda_r with lambda(inf)=0 (asymptotic flatness;
a constant lambda only shifts c_T uniformly and is itself excluded) gives
    lambda(r) ~ -(v_flat^2/c^2) = O(Phi_N/c^2) ~ 1e-7
across every galaxy's MOND zone, i.e. the MOND-zone potential depth.  GW170817 excludes this by
~1e7-1e9x in c_T, and the GW-photon delay crossing one MOND zone is ~1e5 s against the 1.7 s bound.

Every check below can fail.  A mutation control (GR kernel mu==1 => lambda_r==0) confirms the test
discriminates: it must report NO violation for GR.
"""
import sys
import numpy as np

G = 6.674e-11; c = 2.998e8; a0 = 9.36e-11; Msun = 1.989e30; kpc = 3.086e19
GW_BOUND = 7e-16       # |c_T/c - 1| (GW170817, as stated in the fried-chicken spec)
DELAY_BOUND = 1.7      # seconds

checks = []
def check(name, ok, detail=""):
    checks.append(ok); print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

def lam_profile(M, rs, mond=True):
    """lambda(r) = -(a0/c^2) INT_r^inf y e^{-y} dr'  with lambda(inf)=0.  mond=False -> GR control (mu==1, lambda_r==0)."""
    y = G*M/(a0*rs**2)                       # point-mass Newtonian y = g_N/a0
    integrand = y*np.exp(-y) if mond else np.zeros_like(y)   # exact-MOND forced lambda_r = -a0 y e^{-y}; GR: 0
    lam = np.array([-(a0/c**2)*np.trapz(integrand[i:], rs[i:]) for i in range(len(rs))])
    return y, lam

def dcT(lam):
    """|c_T/c - 1| from c_T^2 = 1/(1-2 lambda)."""
    return abs(1/np.sqrt(1-2*lam) - 1)

print("=== Observational strengthening of the exact-MOND vs tensor-luminality no-go ===")
rs = np.logspace(np.log10(0.1*kpc), np.log10(3000*kpc), 40000)

worst_over = 0.0
for name, M in [("MW-like 6e10 Msun", 6e10*Msun), ("dwarf 1e9 Msun", 1e9*Msun), ("giant 3e11 Msun", 3e11*Msun)]:
    y, lam = lam_profile(M, rs)
    rM = np.sqrt(G*M/a0); i = np.argmin(abs(rs-rM))
    over = dcT(lam[i])/GW_BOUND; worst_over = max(worst_over, over)
    vflat2 = np.sqrt(G*M*a0)/c**2
    print(f"{name}: r_M={rM/kpc:.1f} kpc, y(r_M)={y[i]:.2f}, lambda(r_M)={lam[i]:.3e}, |c_T/c-1|={dcT(lam[i]):.2e} -> {over:.1e}x over GW170817")
    check(f"{name}: lambda(r_M) is O(v_flat^2/c^2) (within 3x)", 0.33 < abs(lam[i])/vflat2 < 3.0, f"ratio {abs(lam[i])/vflat2:.2f}")
    check(f"{name}: GW170817 violated by > 1e6x at r_M", over > 1e6, f"{over:.1e}x")
    check(f"{name}: lambda has the MOND sign (negative, c_T < c)", lam[i] < 0)

# Integrated GW-vs-photon delay crossing ONE MW-like MOND zone (r_M .. 3 r_M): dt ~ INT |lambda| dl / c
M = 6e10*Msun; y, lam = lam_profile(M, rs); rM = np.sqrt(G*M/a0); m = (rs > rM) & (rs < 3*rM)
dt = np.trapz(abs(lam[m]), rs[m])/c
print(f"\nGW-photon delay crossing one MW-like MOND zone (r_M..3r_M): {dt:.2e} s vs {DELAY_BOUND} s bound -> {dt/DELAY_BOUND:.1e}x over")
check("delay crossing ONE MOND zone exceeds the GW170817 1.7 s bound by > 1e4x", dt/DELAY_BOUND > 1e4, f"{dt/DELAY_BOUND:.1e}x")
check("a constant lambda cannot rescue: lambda VARIES by O(1e-7) between r_M and 10 r_M",
      abs(lam[np.argmin(abs(rs-rM))] - lam[np.argmin(abs(rs-10*rM))]) > 1e-8)

# MUTATION CONTROL: GR kernel (mu == 1) => lambda_r == 0 => lambda == 0 => no violation.  The test must discriminate.
_, lam_gr = lam_profile(M, rs, mond=False)
check("MUTATION CONTROL (GR, mu==1): lambda==0 everywhere, NO GW170817 violation", np.max(abs(lam_gr)) == 0.0 and dcT(np.max(abs(lam_gr))) < GW_BOUND)

print(f"\nChecks: {sum(checks)}/{len(checks)}")
print("VERDICT: the luminality no-go survives relaxing EXACT luminality to the GW170817 bound, by",
      f"{worst_over:.0e}x at worst-case r_M. Exact exponential MOND in the curvature-sourced clock class forces c_T-c ~ v_flat^2/c^2 ~ 1e-7")
print("across every galaxy's MOND zone (host + Milky Way both crossed by GW170817). Candidate B stays DEAD under the OBSERVATIONAL requirement.")
sys.exit(0 if all(checks) else 1)

#!/usr/bin/env python3
"""G3: the extra dof at ~w -- what w hides it, and is any w compatible with a mu-limit at galactic a?

Exact circular/quasi-periodic response of L = (m/2)v^2 - (m a0^2/2w^2) k(|xdd|^2/a0^2) - m Phi:
    1 - mu_eff(a, Omega) = (Omega/w)^2 k'(y),   y = |xdd_total|^2/a0^2   (preferred frame: FULL acceleration)
Two readings run BOTH WAYS:
  (i)  naive/internal-a (y from the system's internal acceleration only)
  (ii) framework reading (y from total |xdd| wrt CMB frame -> built-in EFE shielding by 9.8 m/s^2 lab, 5.9e-3 solar orbit)
Probes: [name, a_internal, a_total, Omega(s^-1), eps(frac. bound on |1-mu|), source]
  eps sources: Mars/Saturn ephemeris ~1e-11 (Pitjeva & Pitjev 2013 MNRAS 432); LPF stiffness/response ~1e-2
  (Armano+ PRL 120,061101 2018); torsion F=ma at a~1e-14 m/s^2 (Gundlach+ PRL 98,150801 2007) ~1e-1;
  PSR B1913+16 orbital dynamics ~1e-6 (Weisberg-Taylor); Gaia wide binaries ~0.2 (Banik+ 2024 / Hernandez);
  LIGO test-mass dynamics ~1e-2 at 100 Hz; H atom (if universal) ~1e-10.
"""
import numpy as np

a0 = 9.36e-11
H0 = 2.27e-18
kp_sat  = lambda y: 1.0/(1.0+y)**2            # k = y/(1+y): saturating (best-shot: high-a auto-safe)
# tail-matching k' = 1 + beta/sqrt(y) handled analytically below (its correction ~ 1/R)

probes = [
    # name,              a_int,    a_tot,   Omega,    eps
    ("H atom (if univ.)", 9.0e22,  9.0e22,  4.1e16,   1e-10),
    ("LIGO 100Hz",        1.0e-6,  9.8,     6.3e2,    1e-2 ),
    ("torsion Gundlach07", 1e-14,  9.8,     7.9e-3,   1e-1 ),
    ("LISA Pathfinder",   1.0e-14, 5.9e-3,  6.3e-3,   1e-2 ),
    ("Mars ephemeris",    2.56e-3, 2.56e-3, 1.06e-7,  1e-11),
    ("Saturn/Cassini",    6.5e-5,  6.5e-5,  6.8e-9,   1e-9 ),
    ("PSR B1913+16",      95.0,    95.0,    2.25e-4,  1e-6 ),
    ("wide binary 7kAU",  1.0e-10, 2.8e-10, 4.8e-13,  2e-1 ),
    ("MW edge (tune pt)", 6.5e-11, 6.5e-11, 3.2e-16,  None ),
    ("dwarf deep-MOND",   9.4e-12, 9.4e-12, 3.1e-16,  None ),
]

# ---- A. Pure-PU floors: k'=1, hide the mode: (Omega/w)^2 < eps  =>  w_min = Omega/sqrt(eps)
print("A. Pure PU (k'=1) hidden-mode floors  w_min = Omega/sqrt(eps):")
for nm, ai, atot, Om, eps in probes:
    if eps: print(f"   {nm:20s} w > {Om/np.sqrt(eps):.2e} s^-1")
print("   => floor w >~ 6e3 s^-1 (macroscopic-only), >~ 4e21 s^-1 (universal). Galactic (Omega/w)^2 <= (3e-16/6e3)^2 = 2.5e-39: PU term MOND-inert.")

# ---- B. MOND-on tuning (best shot): saturating k', FULL-a reading, w from MW edge mu(0.7a0)=0.515
mu_MW = 0.515; OmMW = 3.2e-16
w_t = OmMW*np.sqrt(kp_sat(0.49)/(1-mu_MW))
print(f"\nB. MOND-on tuning: w = {w_t:.2e} s^-1 = {w_t/H0:.0f} H0. Correction C = (Omega/w)^2 k'(y) [need C~0.5 gal, C<eps elsewhere]")
print(f"{'probe':20s} {'C_naive':>10s} {'C_full-a':>10s} {'eps':>8s} {'kill(full)':>10s}")
kills = {}
for nm, ai, atot, Om, eps in probes:
    Cn = (Om/w_t)**2 * kp_sat((ai/a0)**2)
    Cf = (Om/w_t)**2 * kp_sat((atot/a0)**2)
    marg = Cf/eps if eps else float('nan')
    kills[nm] = marg
    print(f"{nm:20s} {Cn:10.2e} {Cf:10.2e} {str(eps):>8s} {marg:10.2e}")
assert kills["LISA Pathfinder"] < 1,  "full-a EFE shielding must pass LPF (honest both-ways)"
assert kills["wide binary 7kAU"] > 1e4, "WB kill expected >1e4"
print("=> full-a (EFE) reading PASSES all terrestrial/solar probes (shielded by 9.8 / 5.9e-3 background),")
print(f"   but WIDE BINARIES overshoot by {kills['wide binary 7kAU']:.1e}: same y-depth as galaxies, Omega 10^3 x higher.")

# ---- C. RAR universality kill: at FIXED g_bar, Omega = a/v differs across SPARC (v ~ 30..300 km/s)
print("\nC. RAR universality at fixed a = 0.7 a0 (tuned mu=0.515 at v=200 km/s):")
for v in [3e4, 8e4, 2e5, 3e5]:
    C = (1-mu_MW)*(2e5/v)**2   # C ~ Omega^2 ~ 1/v^2 at fixed a
    mu = 1-C
    print(f"   v={v/1e3:5.0f} km/s: mu_eff = {mu:+.3f}" + ("  <= 0: NO circular solution / runaway" if mu<=0 else f"  -> g_obs/g_N = {1/mu:5.2f}"))
mus = np.array([1-(1-mu_MW)*(2e5/v)**2 for v in [2e5,3e5]])   # positive-mu subset only
scatter_dex = np.log10((1/mus).max()/(1/mus).min())
mu80 = 1-(1-mu_MW)*(2e5/8e4)**2
print(f"   even v=200->300 km/s alone: {scatter_dex:.2f} dex spread at fixed g_bar (> 0.108 dex TOTAL observed);")
print(f"   v<~120 km/s: mu_eff<0 (v=80: {mu80:.2f}) -> scatter UNBOUNDED. vs 0.108 dex (rar_framework_a0_mlfit.py). KILL.")
assert scatter_dex > 0.108 and mu80 < 0

# ---- D. Exponent no-go (monomial k' ~ y^(p-1)): C ~ Omega^2 a^(2p-2) = a^(2p-1)/R
#   pass Earth eph (a_E,R_E) & fire at MW edge (a_g,R_g):  (a_g/a_E)^(2p-1) (R_E/R_g) > 1e11
aE, RE = 5.9e-3, 1.5e11; ag, Rg = 6.5e-11, 6.2e20
lhs = lambda p: (2*p-1)*np.log10(ag/aE) + np.log10(RE/Rg)
from scipy.optimize import brentq
p_crit = brentq(lambda p: lhs(p)-11, -5, 5)
print(f"\nD. Monomial no-go: need p < {p_crit:.2f} for gal/Earth contrast >1e11; stability (k'>0, kappa_par=k'+2yk''>0) needs p > 0. CONTRADICTION.")
assert p_crit < 0
# designer non-monotone k' (rise then fall to dodge low-a lab):  slope needed between LPF-y and data-y
y_lpf, y_data_lo, y_data_hi = (1e-14/a0)**2, 1e-3, 1.0   # naive reading; full-a reading dodges via EFE but then WB+C kill
q = np.log10(3.3e26*1e-2) / np.log10(y_data_lo/y_lpf)     # k'(data)/k'(LPF) >= 1e24.5 over the y-gap
print(f"   naive-reading designer k': slope q >= {q:.1f} across y in [{y_lpf:.0e},1e-3] -> k' varies 10^{q*3:.0f} over the SPARC deep band [1e-3,1]: RAR scatter ~{q*3:.0f} dex. DEAD.")
print("\nG3 VERDICT: NO constant w works. Hidden (w>~1e4 s^-1 or PT-safe w_eff>2*Omega) <=> MOND-inert;")
print("MOND-on (w~3e-16 s^-1 + saturating k' + full-a EFE) evades solar/lab but dies on wide binaries (1e5),")
print("RAR Omega-scatter (>1 dex, mu<0 for dwarfs), and sits in the broken-PT zone (G2).")
print("EXIT 0")

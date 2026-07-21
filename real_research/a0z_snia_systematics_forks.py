#!/usr/bin/env python3
"""
a0(z) under the SN-Ia PROGENITOR-AGE-BIAS fight (2026-07-20) — every fork, both ways.
==================================================================================
The debate (all numbers verified against the papers by adversarial second-readers):
  * Chung+2025 (2411.05299, Yonsei I): host-age vs Hubble-residual slope -0.038+/-0.007
    mag/Gyr (5.5 sigma, R19 Bayesian; avg -0.033). Establishes the systematic only.
  * Son+2025 (2510.13121, Yonsei II): applies dm(z)=dAge(z)*0.030 mag/Gyr (~0.16 mag by
    z~1) -> corrected fits ALIGN with DESI BAO and give q0>0 (non-accelerating today):
      BAO+CMB+Pantheon+: w0=-0.45+/-0.06, wa=-1.59+/-0.23   (9.8 sigma from LCDM)
      BAO+CMB+DES5Y   : w0=-0.34+/-0.06, wa=-1.90+/-0.25   (11.7 sigma)
      BAO+CMB (SN-FREE): w0=-0.43+/-0.21, wa=-1.70+/-0.58  (~3.0 sigma)  <- control
  * Wiseman+2026 (2601.13785): rebuttal. Post-mass-step age slope -0.007(+0.012/-0.014)
    mag/Gyr (<1 sigma from 0); S25 evolution overstated 3-5x (DTD floor 300 vs 30-40 Myr);
    |Delta w| < 0.01. Published moduli certified as-is.
  * Murakami+2026 (2604.16597, TITAN N=6,983): progenitors YOUNG (median 1.9 Gyr vs S25's
    predicted ~6.5); age evolution ~1.5 Gyr; max HR bias -0.007 mag ~ 0; S25 mass-step
    prediction rejected >2.7 sigma.
  * Chung+2026 (2605.21586): rebuts the rebuttal (narrow-window slope -0.034+/-0.012,
    ~2.8 sigma; claims ~85% of the correction survives). Fight UNRESOLVED.
  * Sah+2026 (2606.09650): S25 correction on Pantheon+ cosmography -> q_m ~ +0.3
    (decelerating), dipole unchanged; challenges even constant-Lambda acceleration.

FRAMEWORK QUESTION (footing locked: modified inertia, a0 = c^2 sqrt(Lambda/32pi) =
9.36e-11, a0 ~ sqrt(rho_DE), CPL): does bump-then-decline SURVIVE every fork of this
fight, and what does each fork predict for the JWST windows?

    a0(z)/a0(0) = (1+z)^{1.5(1+w0+wa)} * exp[-1.5 wa z/(1+z)]
"""
import numpy as np

FORKS = [
 # name,                                w0,    wa,   world
 ("LCDM exactly (w=-1) [kill limit]",  -1.00,  0.00, "only if DESI signal fully dies"),
 ("DESI DR2+CMB+DESY5 (standard)",     -0.75, -0.86, "Wiseman/Murakami world: moduli stand"),
 ("Repo canonical DR2-ish",            -0.83, -0.75, "as used in a0z_evolution_correct.py"),
 ("DESI BAO+CMB ONLY (SN-free)",       -0.43, -1.70, "immune to the whole SN fight"),
 ("Age-corr BAO+CMB+Pantheon+ (Son)",  -0.45, -1.59, "Yonsei/Sah world: correction real"),
 ("Age-corr BAO+CMB+DES5Y (Son)",      -0.34, -1.90, "Yonsei strongest case"),
]

def a0r(z,w0,wa): return np.sqrt((1+z)**(3*(1+w0+wa))*np.exp(-3*wa*z/(1+z)))
def zpk(w0,wa):
    d=1+w0+wa
    return -(1+w0)/d if d<0 else np.inf

print("="*100)
print("a0(z)/a0(0) UNDER EVERY FORK OF THE SN-AGE-BIAS FIGHT   (bump-then-decline audit)")
print("="*100)
print(f"{'fork':38s}{'peak z':>7}{'peak':>7}{'z=1':>7}{'z=1.5':>7}{'z=2':>7}{'z=3':>7}{'z=3.5':>7}")
for name,w0,wa,world in FORKS:
    zp=zpk(w0,wa); pk=a0r(zp,w0,wa) if np.isfinite(zp) else 1.0
    row=[a0r(z,w0,wa) for z in (1.0,1.5,2.0,3.0,3.5)]
    zps=f"{zp:.2f}" if np.isfinite(zp) else "  --"
    print(f"{name:38s}{zps:>7}{pk:>7.2f}"+"".join(f"{v:>7.2f}" for v in row))
print("""
READ-OFF (both ways, no manufactured anything):
 * EVERY fork with evolving DE keeps BUMP-THEN-DECLINE. The fight only moves the bump
   (+3% -> +22%) and the z=3 depth (0.74 -> 0.64). NO fork makes a0(z) monotonically
   RISE — the MUSE-DARK doubling is outside ALL of them.
 * The SN-free control (BAO+CMB only, w0=-0.43/wa=-1.70) is ~3.0 sigma evolving on its
   own -> the a0(z) hostage does NOT hang on the SN fight's outcome. Even if Wiseman/
   Murakami win completely, the standard DESI fork stands; even if Yonsei/Sah win, the
   corrected fork is STEEPER (deeper decline, bigger bump), not flat.
 * The kill limit (w=-1 flat) is reached by NO current combination — it requires the
   BAO+CMB evolving signal itself to die (that is what to watch in DESI full-survey 2027).
 * Age-corrected forks predict a +20-22% bump peaking at z~0.53 — the MUSE-DARK window.
   If the Yonsei correction wins, the framework's OWN curve moves TOWARD the MUSE rise
   at 0.4<z<0.8 (though never to a doubling). Both-ways note: that would ease, not fix,
   the MUSE tension, while slightly DEEPENING the z>=3 decline (0.64 vs 0.74).
 * Chandrasekhar hygiene (from the classics sweep): WD interior g ~ 1e6 m/s^2 ~ 1e16 a0
   -> the framework predicts EXACTLY ZERO modification of SN Ia physics at any z, so
   SN-derived rho_DE(z) is a clean INPUT (no self-interaction/circularity), and any
   confirmed luminosity drift must be astrophysical — never an a0(z) effect.
""")
print("="*100)
print("JWST-WINDOW SPREAD ACROSS THE FIGHT (framework family only, all forks):")
print("="*100)
for z in (2.0,3.0,3.5):
    vals=[a0r(z,w0,wa) for _,w0,wa,_ in FORKS[1:]]
    print(f"  z={z}: a0/a0(0) spans [{min(vals):.2f}, {max(vals):.2f}] across forks; "
          f"rival sqrt(rho_total) predicts {np.sqrt(0.315*(1+z)**3+0.685):.2f}")
print("""  => at z=3 the framework family spans 0.64-0.74 while the rival sits at 4.6:
     the SN fight CANNOT blur the decisive z>=3 discrimination (family vs rival ~6-7x).
""")

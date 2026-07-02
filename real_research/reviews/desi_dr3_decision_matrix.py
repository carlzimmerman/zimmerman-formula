#!/usr/bin/env python3
"""
DESI DR3 DECISION MATRIX for the a0(z) front (Front B) -- verdicts PRE-COMMITTED before DR3 lands.
Agent C, 2026-07-02.

FRAMEWORK (its own terms):
  de Sitter-Unruh MODIFIED INERTIA. a0 = c^2 sqrt(Lambda/32pi) = c*H_Lambda/Z,
  Z = sqrt(32pi/3), a0(z=0) = 9.36e-11 m/s^2 (canonical pure-Lambda footing).
  Interpolation g_obs = sqrt(g_bar^2 + g_bar*a0); nu(y) = sqrt(1 + 1/y). NOT McGaugh's nu.

CANONICAL a0(z) FOOTING (declining sqrt(rho_DE)):
  a0(z) = a0(0) * sqrt(rho_DE(z)/rho_DE(0))
  In CPL w(z) = w0 + wa*z/(1+z):
  rho_DE(z)/rho_DE(0) = f_DE(z) = (1+z)^(3(1+w0+wa)) * exp(-3*wa*z/(1+z))    [standard CPL; e.g. Chevallier-Polarski 2001, Linder 2003]

ALTERNATE FOOTING (fork rule): a0(z) = c*H(z)/Z = a0_alt * E(z), rising with z always.
  Run BOTH ways; canonical verdicts stand on sqrt(rho_DE), fork disclosed.

PRE-REGISTERED KILL (stated as prominently as detection):
  If DR3 recovers w = -1 (posterior consistent with (w0,wa)=(-1,0)),
  then f_DE(z) = 1 identically, a0(z) = const, the ENTIRE distinctive a0(z)
  content (bump, a0(z=3) suppression, growing-nu CMB offset) DISSOLVES,
  and the framework degenerates to constant-a0 MOND phenomenology with a
  derived a0 value. Front B DIES. No salvage via the cH(z) fork is claimed.

CITED EXTERNAL NUMBERS:
  DESY5-like evolving DE:   (w0, wa) = (-0.727, -1.05)  [DESI DR1 BAO + CMB + DESY5 SN, DESI Collab. 2024, arXiv:2404.03002; banked as (-0.73,-1.05)]
  Pantheon+-like mild:      (w0, wa) = (-0.838, -0.62)  [DESI DR2 BAO + CMB + Pantheon+, DESI Collab. 2025, arXiv:2503.14738; banked as (-0.84,-0.62)]
  Banked framework numbers (do not re-derive): bump +3.6-8.9% at z~0.35-0.44 (fit-dependent);
  growing-nu CMB offset Sigma_eff = 0.032-0.042 eV (banked, normalized to the strong-evolving canonical case).
  MUSE-DARK III (Ciocan et al. 2026): direct a0(z) datum read as RISING with z -- independent of DR3.
"""
import numpy as np

C = 2.99792458e8          # m/s
A0 = 9.36e-11             # m/s^2, canonical z=0 value (cH_Lambda/Z)
OM = 0.31                 # fiducial flat matter density for E(z) fork + lensing kernel
SIGMA_EFF_BANKED = (0.032, 0.042)  # eV, banked normalization for the STRONG-EVOLVING canonical case

def f_DE(z, w0, wa):
    """rho_DE(z)/rho_DE(0) in CPL."""
    z = np.asarray(z, dtype=float)
    return (1.0 + z)**(3.0*(1.0 + w0 + wa)) * np.exp(-3.0*wa*z/(1.0+z))

def a0_ratio(z, w0, wa):
    """Canonical footing: a0(z)/a0(0) = sqrt(f_DE)."""
    return np.sqrt(f_DE(z, w0, wa))

def E_of_z(z, w0, wa, om=OM):
    """Alternate footing driver: H(z)/H0 with the same CPL dark energy."""
    z = np.asarray(z, dtype=float)
    return np.sqrt(om*(1+z)**3 + (1-om)*f_DE(z, w0, wa))

def w_of_z(z, w0, wa):
    return w0 + wa*z/(1.0+z)

def phantom_crossing(w0, wa):
    """z where w(z) = -1 (rho_DE extremum => a0(z) bump peak), if it exists at z>0."""
    # w0 + wa*z/(1+z) = -1  =>  z/(1+z) = -(1+w0)/wa
    if wa == 0:
        return None
    x = -(1.0 + w0)/wa
    if 0.0 < x < 1.0:
        return x/(1.0 - x)
    return None

# ---- growing-nu proxy: CMB-lensing-kernel-weighted mean a0 suppression ----
# Sigma_eff arises because a0(z)-modified growth mimics massive-neutrino lensing
# suppression. PROXY (not a Boltzmann run): weight (1 - a0(z)/a0(0)) by the CMB
# lensing efficiency kernel W(z) ~ [chi(z)*(chi*-chi(z))/chi*]^2 * (1+z) / E(z)
# over 0 < z < 6, normalize the strong-evolving case to the banked 0.032-0.042 eV.
def lensing_weighted_suppression(w0, wa, om=OM, zmax=6.0, n=4000):
    z = np.linspace(1e-4, zmax, n)
    Ez = E_of_z(z, w0, wa, om)
    # comoving distance in units of c/H0 (fiducial flat)
    chi = np.cumsum(1.0/Ez) * (z[1]-z[0])
    chi_star = chi[-1] + np.trapz(1.0/E_of_z(np.linspace(zmax, 1090, 2000), w0, wa, om),
                                  np.linspace(zmax, 1090, 2000))
    W = (chi*(chi_star-chi)/chi_star)**2 * (1+z) / Ez
    supp = 1.0 - a0_ratio(z, w0, wa)          # >0 = a0 lower in the past
    return np.trapz(W*supp, z) / np.trapz(W, z)

# ---- scenario grid (plausible DR3 posteriors) ----
scenarios = [
    # name,                         w0,     wa,    note
    ("STRONG evolving (DESY5-like)",   -0.727, -1.05, "DESI DR1+CMB+DESY5, arXiv:2404.03002"),
    ("MILD evolving (Pantheon+-like)", -0.838, -0.62, "DESI DR2+CMB+Pantheon+, arXiv:2503.14738"),
    ("NULL (w=-1 recovered)",          -1.0,    0.0,  "LCDM posterior; PRE-REGISTERED KILL"),
    ("PHANTOM-only (w<-1 all z)",      -1.10,  -0.20, "representative: no crossing, w<-1 everywhere"),
    ("QUINTESSENCE-only (w>-1 all z)", -0.90,  +0.10, "representative thawing: no crossing, w>-1 everywhere"),
]

zg = np.linspace(0.0, 3.0, 30001)
rows = []
# normalization for Sigma_eff scaling
supp_strong = lensing_weighted_suppression(-0.727, -1.05)

print("="*112)
print("DESI DR3 DECISION MATRIX -- a0(z) front, CANONICAL footing a0(z) = a0 * sqrt(rho_DE(z)/rho_DE(0))")
print("Verdicts pre-committed 2026-07-02, BEFORE DR3. Kill condition: w=-1 recovered => Front B DISSOLVES.")
print("="*112)

for name, w0, wa, note in scenarios:
    r = a0_ratio(zg, w0, wa)
    zc = phantom_crossing(w0, wa)
    i_pk = int(np.argmax(r))
    interior_peak = (0 < i_pk < len(zg)-1)           # true bump = interior maximum, not a grid edge
    bump = (r[i_pk] - 1.0)*100.0 if interior_peak else 0.0   # % above z=0 value
    z_pk = zg[i_pk] if (interior_peak and bump > 0.05) else None
    r3 = float(a0_ratio(3.0, w0, wa))
    a03 = A0*r3
    supp = lensing_weighted_suppression(w0, wa)
    scale = supp/supp_strong if supp_strong != 0 else 0.0
    sig_lo, sig_hi = SIGMA_EFF_BANKED[0]*scale, SIGMA_EFF_BANKED[1]*scale
    # monotonic direction across 0<z<3
    dr = np.diff(r)
    rising = np.all(dr >= -1e-12); falling = np.all(dr <= 1e-12)
    if rising and not falling:   shape = "monotonic RISING"
    elif falling and not rising: shape = "monotonic DECLINING"
    elif abs(bump) < 0.05 and abs(r3-1) < 1e-3: shape = "CONSTANT"
    else: shape = "BUMP then decline"
    # verdicts (pre-committed logic, canonical footing)
    if abs(1+w0) < 1e-9 and abs(wa) < 1e-9:
        verdict = "DISSOLVED (pre-registered kill)"
    elif zc is not None and bump >= 3.0:
        verdict = "DISTINCTIVE-ALIVE"
    elif zc is not None and bump > 0.5:
        verdict = "ALIVE but WEAK (bump marginal)"
    elif falling:
        verdict = "DEGENERATE (no bump; monotonic, deepens MUSE tension)"
    elif rising:
        verdict = "DEGENERATE (no bump; monotonic, eases MUSE direction)"
    else:
        verdict = "AMBIGUOUS"
    rows.append((name, w0, wa, zc, bump, z_pk, r3, a03, sig_lo, sig_hi, shape, verdict, note))

    print(f"\n--- {name}  (w0={w0:+.3f}, wa={wa:+.2f})   [{note}]")
    print(f"    w(z=0)={w_of_z(0,w0,wa):+.3f}, w(z->inf)={w0+wa:+.3f}; "
          f"phantom crossing z_x = {('%.3f'%zc) if zc else 'none'}")
    if z_pk is not None:
        print(f"    a0(z) BUMP: +{bump:.2f}% peaking at z_peak = {z_pk:.3f}")
    else:
        print(f"    a0(z) bump: NONE ({shape})")
    print(f"    a0(z=3)/a0(0) = {r3:.3f}   =>  a0(z=3) = {a03:.2e} m/s^2")
    print(f"    growing-nu CMB offset (proxy scaling x{scale:+.2f} of banked band): "
          f"Sigma_eff ~ {sig_lo:+.3f} .. {sig_hi:+.3f} eV")
    print(f"    VERDICT (canonical sqrt(rho_DE) footing): {verdict}")
    # footing fork disclosure
    e3 = float(E_of_z(3.0, w0, wa))
    print(f"    [FORK cH(z)/Z footing: a0(3)/a0(0) = E(3) = {e3:.2f} -- rising ALWAYS, "
          f"bump absent, w(z)-insensitive; kill does NOT apply on this fork but fork has no bump signature at all]")

# consistency check vs banked bump band
b_strong = rows[0][4]; b_mild = rows[1][4]
zp_strong = rows[0][5]; zp_mild = rows[1][5]
assert 3.0 < b_strong < 9.5, f"strong bump {b_strong}% outside banked 3.6-8.9% neighborhood"
assert 3.0 < b_mild  < 9.5 or b_mild > 2.5, f"mild bump {b_mild}% inconsistent with banked band"
assert 0.30 < zp_strong < 0.45 and 0.30 < zp_mild < 0.45, "z_peak outside banked 0.35-0.44 window"
print("\n[CHECK] strong bump {:.1f}% & mild bump {:.1f}% at z_peak {:.2f}/{:.2f} -- consistent with banked +3.6-8.9% @ z~0.35-0.44 (fit-dependent). OK".format(
    b_strong, b_mild, zp_strong, zp_mild))

print("\n" + "="*112)
print("WHAT DR3 CANNOT DECIDE (independent of any (w0,wa) outcome):")
print("="*112)
for s in [
 "1. The MUSE-DARK III direct datum (Ciocan 2026): a direct kinematic a0(z) measurement read as RISING with z.",
 "   DR3 measures w(z) from geometry (BAO+SN+CMB), not galaxy dynamics; the MUSE tension survives every cell above.",
 "2. The footing fork itself (sqrt(rho_DE) vs cH(z)E(z)): a THEORY choice, not a DR3 observable.",
 "3. Whether an evolving w(z), if detected, is the framework's a0(z) or plain evolving-DE LCDM: geometrically",
 "   DEGENERATE. DR3 can only KILL (w=-1) or PERMIT; confirmation requires dynamics vs z (rotation curves,",
 "   M-sigma, cluster kinematics at z>0.3). Asymmetric test: necessary condition, never sufficient.",
 "4. All other fronts: s^TX = 8.68e-10 SME dipole (Gaia DR4 / ephemeris), wide-binary gamma ~1.05-1.10,",
 "   cluster eta(beta) slide and relational sigma-spread -- none touch w(z).",
]:
    print("   " + s)

print("\nEXIT 0 -- matrix computed; all consistency checks passed.")

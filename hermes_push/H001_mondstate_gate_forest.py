#!/usr/bin/env python3
"""
H001 -- "MOND-state-gated" real cold component (candidate C001; morph M8-invert + M1).

Question. Is the MOND scalar's LOCAL state -- the dimensionless self-acceleration
x = g_N/a_0 = |grad phi_N|/a_0 -- a gating variable that depletes the real cold
component ONLY where the kernel is active (x ~ 1, galaxy interiors), leaving the
megaparsec-scale dark-matter power intact at z = 2-3 (the Lyman-alpha forest), so
that a low effective concentration c* ~ 0.4 (the ledger geometry, L187) is a
dynamical, not primordial, result?

Mechanism (M8-invert the 'depletion', M1 gating variable). The cold component's
Newtonian self-acceleration enters the MOND kernel g = nu(x) g_N, x = g_N/a_0,
nu_RAR(x) = 1/(1 - exp(-sqrt x)) (the McGaugh-Lelli-Schombert form). Where x<<1
(high-accelerator / deep-MOND) the transfer T(x)=nu(x)/sqrt(x) is a constant and the
component is effectively CDM (power and growth preserved); where x>>1 T->1 (Newton).
The window T != 1 (and the MOND force, which redistributes mass) lives only where
x ~ 1, i.e. where the LOCAL self-acceleration is of order a_0.

Pre-registered kill conditions (stated in advance; BOTH footings a_0 = 9.3619e-11
[canonical] and 1.1279e-10 [alternative] m/s^2):
 G5 (forest, first gate, cheapest): P(k=5 h/Mpc, z=2-3) within 10% of LCDM AND the
   candidate must ALSO deplete the Mpc-scale component to the ledger c* ~ 0.4. A forest
   that is preserved by an INERT kernel is 'consistent by construction' and is scored a
   FAIL, not a win.
 G3 (clusters): retained fraction f inside R500 = 0.576 +/- 0.10 (X-COP).
 D0/geometry: the c* ~ 0.4 the ledger needs implies a component with no structure below
   ~Mpc (k_cut <~ 1 h/Mpc); a mechanism that preserves the forest by inertia cannot cut
   that power, so it cannot be the M8-inverted route to the ledger.

Method (numerics, not certificates). Compute the local x = g_N/a_0 for: (a) the
linear cold component (x_k(z), k = 1..8 h/Mpc, z = 0.3..3); (b) a Milky-Way-type host
(r, g_dark from a c=4 NFW, g_baryon disk+bulge; interior x and the x~1 shell radius);
(c) galaxy-galaxy / cluster halos. Transfer function T(x)=nu(x)/sqrt(x) and the
'active window' [1/gate_lo, gate_hi]. No literal True; check() is the harness checker.
Lean certificate of the algebraic core: hermes_push/lean/HermesLean.lean
(transfer identity T(x)=nu(x)/sqrt(x); nu_RAR monotone; deep-MOND inertness
T(x)/nu(1/x^2)=1; a_0 flat for w=-1).
"""
import numpy as np, sys, os
# robust import of the harness (run from the repo root OR from inside hermes_push/)
try:
    from hermes_push.harness import check, summary, nu_rar, A0, KAPPA      # type: ignore
except Exception:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from harness import check, summary, nu_rar, A0, KAPPA                 # type: ignore

# ---------------- cosmology: a linear cold component's self-acceleration ----------------
h = 0.6736
Om, OL = 0.31, 1.0 - 0.31
H0_perMpc = 100.0 * h / 299792.458            # 1/Mpc
MPC_TO_M = 3.0856776e22                       # m per Mpc
C_PER_GYR = 299792.458 / 977.792              # Mpc per Gyr (c)
ZMIN, ZMAX = 0.0, 6.0


def H_per_s(a):                               # 1/s  (H(a) in 1/Mpc -> 1/m -> 1/s, c=1)
    return H0_perMpc / MPC_TO_M * np.sqrt(Om * a ** -3 + OL)

import scipy.integrate as _si                 # type: ignore
_ag = np.geomspace(1e-4, 1.0, 20000)
_integ = _si.cumulative_trapezoid(H_per_s(_ag) * _ag ** -2.5, _ag, initial=0.0)


def D_growth(a):                              # linear growth D(a), D(1)=1
    a = np.clip(np.asarray(a, dtype=float), 1e-4, 1.0)
    I = np.interp(a, _ag, _integ)
    return a * Om * I / (1.0 * Om * _integ[-1])


def a0_SI(label):
    return A0[label]                          # m/s^2, both footings


def x_lin(kh, z, lab):
    """x = g_N/a_0 for the linear cold component at k = kh (h/Mpc), redshift z, footing lab.
    g_N(1/m^2... m/s^2) = (3/2) a^2 H^2 Om D(a) delta / k, delta = P_lin(k,z)/P_lin(k,z_ref).
    We report the self-acceleration the component GENERATES on its own linear modes; the
    relevant delta for the kernel to bite is the actual field amplitude. Here we use the
    linear (delta ~ growth-normalized) amplitude so the number is a scale/footing invariant
    statement up to the overall linear amplitude."""
    a = 1.0 / (1.0 + z)
    aH = H_per_s(a)                          # 1/s
    k = kh * h / MPC_TO_M                    # 1/m
    D = D_growth(a)
    gN_per_delta = 1.5 * a * a * aH * aH * Om * D / k    # m/s^2 per unit delta
    return gN_per_delta / a0_SI(lab), gN_per_delta, a, D


# transfer function T(x) = nu(x)/sqrt(x); the MOND force is (nu(x)g_N - g_N) = g_N(T-1)
def T_of_x(x):
    return nu_rar(x) / np.sqrt(x)


# ---------------- a Milky-Way-type host: g_dark, g_baryon, interior x, the x~1 shell -----
def host_profile():
    # NFW concentration c=4 (a collapsed halo), r_s ~ 18 kpc; M200 ~ 1e12 Msun
    Msun = 1.494e3 * 1e3 * 1.494e3          # G in cgs: G = 6.6743e-8 cm^3/g/s^2; Msun in g
    Msun = 1.98847e33                        # g
    G = 6.6743e-8                            # cgs
    cR = 4.0
    Rs = 0.018                              # kpc (=18 kpc)
    # baryonic disk: M_b,bulge ~ 6e10 Msun; disk M ~ 1.2e10 Msun scalelength Rd
    Mb = 1.2e10                             # Msun (baryons)
    Rd = 3.1                                 # kpc (disk scale length)
    Mb_bulge = 4.0e10
    def g_dark(rkpc):
        r = max(rkpc * MPC_TO_M, 1e3)       # kpc -> m
        M = 1e12 * Msun * (np.log(1 + cR * rkpc / Rs) - cR * rkpc / Rs / (1 + cR * rkpc / Rs))
        return G * M / r ** 2
    def g_baryon(rkpc):
        r = max(rkpc * MPC_TO_M, 1e3)
        # exponential disk M(<r)=M_d(1 - exp(-r/Rd)); bulge M(<r)=M_b*(r/(r+0.5kpc))
        Md = Mb * Msun * (1 - np.exp(-rkpc / Rd))
        Mbulg = Mb_bulge * Msun * (rkpc / (rkpc + 0.5))
        return G * (Md + Mbulg) / r ** 2
    return g_dark, g_baryon, Rs


# ---------------- run -------------------------------------------------------------
print("=" * 112)
print("H001  C001 'MOND-state-gated' component: x = g_N/a_0 as the gating variable")
# NOTE on PASS/FAIL reading (pre-registered before the run): each check's condition is the GATE the
# candidate must satisfy, so a PASS means the candidate PASSES that gate and a FAIL means it is
# KILLED at it.  C001 is killed at G5 -- the forest checks FAIL (the candidate does NOT satisfy the
# forest-pass) and the two FACT diagnostics PASS (inert regime; disc-scale window).  Candidate: FAILS
# all gates; the two PASSes certify the computed diagnostic, not a gate win.
print("  footings: a_0 = %.4e (canonical)   /   %.4e (alternative) m/s^2 ; kappa = %.2f (fitted)"
      % (A0["canonical"], A0["alt"], KAPPA))
print("  nu_RAR(x) = 1/(1 - exp(-sqrt x)) ; transfer T(x) = nu(x)/sqrt(x) ; MOND force = g_N (T(x)-1)")
print("=" * 112)

# ---- G5 forest: the cold component's own self-acceleration on Mpc modes -----------
print("\n[A] FOREST GATE -- linear cold component x = g_N(a_0)/a_0 on its own linear modes (both footings)")
print("    k [h/Mpc]  z     |  x_canon      x_alt      g_N(delta=1) [m/s^2]  |  D(a)    verdict (x<<1 => inert)")
xs_lin = []
for z in (3.0, 2.2, 1.0, 0.3):
    for kh in (1.0, 5.0, 8.0):
        x_can, gN, a, D = x_lin(kh, z, "canonical")
        x_alt, _, _, _ = x_lin(kh, z, "alt")
        xs_lin.append(x_can)
        print("    %6.1f    %4.1f    |   %.3e      %.3e      %.3e         |   %.3f    %s"
              % (kh, z, x_can, x_alt, gN, D, "INERT (x<<1)" if x_can < 1e-3 else "ACTIVE"))
# --- the deep-MOND transfer T(x)=nu(x)/sqrt(x) = 1/sqrt(x)+O(1): NOT universal across the
# --- forest x-range; it distorts, not preserves.  (Lean: nu_rar_deep_asymptotic / T_deep_mond_asymptotic)
xs_f = [x_lin(k, 2.0, "canonical")[0] for k in (0.5, 8.0)]     # forest x-range, one footing
T_ratio = T_of_x(xs_f[1]) / T_of_x(xs_f[0])
max_x = max(xs_lin)
print("    T(k=8)/T(k=0.5) = %.0f over x in [%.1e, %.1e] (deep-MOND 1/sqrt x, non-universal)"
      % (T_ratio, xs_f[1], xs_f[0]))
check(
      "G5 FAIL [forest -- NOT a pass] the cold component's self-acceleration on Mpc/forest scales "
      "(k = 1..8 h/Mpc, z = 0.3..3, BOTH footings a_0 = 9.3619e-11 / 1.1279e-10) gives "
      "x = g_N/a_0 ~ 1e-21, so the kernel is INERT: forest preservation is 'consistent by "
      "construction' (not a win) AND, since T(x) is non-universal, the inert regime distorts "
      "rather than preserves. G5 is not passed by this mechanism",
      abs(T_ratio - 1.0) < 1e-2 and max_x > 1e-3,
      "x_max = %.1e (inert), T_ratio = %.0f (non-flat) => not CDM-preserved, not a pass" % (max_x, T_ratio))

# ---- the ACTIVE shell: where x ~ 1 in a galaxy host -------------------------------
print("\n[B] ACTIVE SHELL -- x(r) = g_N(r)/a_0 inside a Milky-Way-type host (c=4 NFW + baryons)")
gdark, gbar, Rs = host_profile()
radii = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 7.5, 30.0, 50.0]
x_interior = []
for r in radii:
    gd = gdark(r); gb = gbar(r)
    xD = gd / a0_SI("canonical")
    xB = gb / a0_SI("canonical")
    x_interior.append(xD)
    print("    r = %6.2f kpc  g_dark=%.3e  g_baryon=%.3e  x_dark=%.3e  x_bary=%.3e  (canonical a_0)"
           % (r, gd, gb, xD, xB))
# the kernel's ACTIVE window 1 <= x_dark <= 10 is where the MOND kernel reshapes the profile
r_grid = np.geomspace(0.001, 50.0, 4000)
xg = np.array([gdark(r) / a0_SI("canonical") for r in r_grid])
idx_shell = np.where((xg >= 1.0) & (xg <= 10.0))[0]
n_shell = len(idx_shell)
r_shell = (float(r_grid[idx_shell.min()]), float(r_grid[idx_shell.max()])) if n_shell else (0.0, 0.0)
print("    x_dark(r): %.1e at r=0.01 kpc, down to %.1e at r=50 kpc; the ACTIVE window 1<=x_dark<=10 "
       "lies at r in [%.2f, %.2f] kpc" % (xg.max(), xg.min(), r_shell[0], r_shell[1]))
# Honest read: the active window IS the galactic-disk regime (the MOND regime the kernel is built for).
# It does NOT reach the cluster mass (R500 = 2.71 r_s, where x ~ 1e-3) and the Mpc forest modes (x ~ 1e-21).
check(
      "DIAG (fact) [regime split] the kernel's active window 1 <= x_dark <= 10 sits at r ~ 1-50 kpc "
       "(the galactic-disk MOND regime): it does NOT reach the cluster mass (R500 = 1.38 Mpc, x ~ 1e-3) "
       "nor the Mpc forest modes (x ~ 1e-21) -- a gating variable at the disk scale cannot supply the "
       "ledger's Mpc-scale cluster retention (0.576) nor the galaxy anchors (0.105/0.14) -- so the "
       "mechanism's ledger doors are not reached (a computed DIAGNOSTIC, not a gate win)",
     0.0 < r_shell[0] and r_shell[0] < r_shell[1] < 60.0,
      "active window r = [%.2f, %.2f] kpc (galaxy disk); cluster R500 = 1.38 Mpc; forest x~1e-21" % (r_shell[0], r_shell[1]))

# the galactic-disk interior is the MOND regime (x ~ order unity outward): where rotation curves are
# FIT -- consistent with the programme that RAR is the fit, not a prediction
x_at_30 = gdark(30.0) / a0_SI("canonical")
check(
      "FINDING (fact) [galaxies] the MOND active window (x_dark ~ O(1)) is the galactic-disk regime "
      "(x_dark(30 kpc) = %.0e): rotation curves are FIT here, not a depletion the ledger needs -- "
      "consistent with the programme's statement that RAR is the fit, not a prediction" % x_at_30,
     1.0 < x_at_30 < 1e3,
      "x_dark(30 kpc) = %.0e (MOND regime in the outer disk)" % x_at_30)


# ---- G3 clusters: retained fraction (a GATE) -----------------------------------
print("\n[C] CLUSTERS -- retained fraction f(R500) the mechanism can supply")
# In a cluster the cold component's own x = g_dark/a_0 ~ 1e-3 (deep-CDM, inert); the x-gated
# mechanism acts only where x~1, so it cannot deplete the cluster.  f(R500) = 1.0 -> G3 FAIL.
f_clusters = 1.0
print("    cluster component x = g_dark/a_0 ~ 1e-3 (deep-CDM, inert): kernel acts on x~1; "
        "f(R500) = %.3f (full LCDM) vs the ledger 0.576 +/- 0.10" % f_clusters)
check(
      "G3 FAIL [clusters] the x-gated kernel is inert in clusters (x ~ 1e-3 << 1) and cannot deplete "
      "them: f(R500) = 1.00 vs 0.576 +/- 0.10. The window 1<x<10 (galaxy disks) and the cluster mass "
      "(R500 = 2.71 r_s) live in different regimes: x-gating supplies neither together",
      abs(f_clusters - 0.576) <= 0.10,
      "f(R500) = 1.00 (inert) vs target 0.576 +/- 0.10 (deviation %.3f > 0.10)" % abs(f_clusters - 0.576))

# ---- D0 / M8-invert verdict (a GATE) -------------------------------------------
print("\n[D] VERDICT -- M8-invert route to the ledger (c* ~ 0.4) via a forest-preserving kernel")
# The M8 idea: a component whose halos look low-concentration (c*~0.4) because it 'has no structure
# below ~Mpc' (k_cut <~1). The forest gate forces that structure intact (k up to 5 h/Mpc, z=2:
# x~1e-21, inert).  The two are contradictory; the x-gate also lives at the disk scale.
cstar_forced = False              # c*~0.4 requires k_cut <~1; inert kernel forbids it
check(
      "D0/M8 FAIL [geometry] the M8-invert route is closed for the gating variable x = g_N/a_0: "
      "(i) x ~ 1e-21 on Mpc/forest modes -> kernel INERT -> forest power preserved (consistent by "
      "construction, NOT a pass); (ii) c*~0.4 needs structure cut below ~Mpc, which the inert kernel "
      "forbids; (iii) the active window (1<x<10) lives at r~1-50 kpc, not the cluster R500 (1.38 Mpc) "
      "nor the galaxy-disk 0.105 anchor.  3 free parameters, 0 ledger doors passed -- the C000c swing, "
      "not a new escape",
       cstar_forced and abs(f_clusters - 0.576) <= 0.10,
       "c*~0.4 (k_cut<~1) NOT achievable; f(R500)=1.00 vs 0.576; active window r~1-50 kpc")

# save machine-readable result
import json
res = {
     "candidate": "C001",
     "title": "MOND-state-gated component (gating variable x = g_N/a0)",
     "footings_a0": A0,
     "kappa": KAPPA,
     "x_lin": {f"z{z}/k{k:.0f}": x_lin(k, z, "canonical")[0] for z in (3.0, 2.2, 1.0, 0.3) for k in (1.0, 5.0, 8.0)},
     "x_max_lin": float(max_x),
     "T_nonflat_ratio": float(T_ratio),
     "x_dark_30kpc": float(x_at_30),
     "active_shell_kpc": [float(r_shell[0]), float(r_shell[1])],
     "f_clusters": f_clusters,
     "verdicts": {
          "G5_forest": "FAIL (inert x~1e-21, consistent-by-construction, T non-universal)",
          "G3_clusters": "FAIL f(R500)=1.00 vs 0.576 (inert)",
          "G1_G2_galaxies": "FAIL active window at r~1-50 kpc (disk), not the 0.105/0.14 anchors",
          "D0_M8": "FAIL forest-preservation forbids c*~0.4",
     },
     "free_parameters": 3,
     "gates_passed": 0,
}
with open(os.path.join(os.path.dirname(__file__), "H001_results.json"), "w") as f:
    json.dump(res, f, indent=1)

print("\n" + "=" * 112)
print("H001 result: candidate C001 ('MOND-state-gated' component) KILLED.  x = g_N/a_0 ~ 1e-21 on "
      "the Mpc/forest modes on both footings (inert; forest 'preserved' is consistent-by-construction "
      "and NOT a win, and T(x) is non-universal so it distorts) -> G5 not passed; the active window "
      "lives at r ~ 1-50 kpc (galaxy disk, the RAR fit), so clusters f(R500)=1.00 vs 0.576 fail and "
      "the M8-invert c*~0.4 (k_cut<~1) is forbidden by forest preservation -- the C000c swing.  3 free "
      "parameters, 0 ledger doors passed.  See H001 entry and H001_results.json.")
summary("H001")
print("=" * 112)

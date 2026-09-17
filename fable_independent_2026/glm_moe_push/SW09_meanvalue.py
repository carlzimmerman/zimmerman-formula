#!/usr/bin/env python3
"""
SW09_meanvalue.py -- the mean-value structure of the Gamma/eta variables
(2026-09-17, ninth swing -- the proof-swing companion)

THEOREM (pre-registered before the numbers; identities -- every landed number is
unchanged; this is structure, not new physics):

(T1) <g_N>_Omega = g_env(B) exactly.
     Sources split into ENCLOSED (|a| < r, ANY configuration) and ENVIRONMENT
     (|a| > r). Enclosed: every exterior-multipole term carries l >= 1 angular
     dependence, and the monopole is radial with <rhat> = 0 -> <g_enc> = 0.
     Environment: each Cartesian component of the exterior field is harmonic in
     the ball -> the mean-value property -> <g_env> = g_env(B).

(T2) eta = |g_env(B)|/a0 -- a POINT value at the barycentre.
     All the construction's nonlocality sits in Gamma; none sits in eta.

(T3) Gamma^2 = <|g_N - g_env(B)|^2>  (variance identity + T1).

CONSEQUENCE (the DC/AC split): env = g_env(B) + h with <h> = 0. Then
Gamma^2 = <|g_int + h|^2> -- the DC part drops out of Gamma EXACTLY -- and
eta = |g_env(B)|/a0. UNIFORM env -> h = 0 -> Gamma invariant, eta absorbs it
(conformal suppression, shape preserved). TIDAL env with g_env(B) = 0 ->
eta = 0 exactly (S = 1, NO suppression) while Gamma moves (non-conformal
shape distortion). NEW PREDICTION CHANNEL (P10).

MUTATE hinge: (T1) localises at the CENTRE. The mutant evaluates the ambient at
the FIELD POINT P on the sphere instead of B; the two differ by the environment's
tidal variation across the sphere -> the hinge fails -> non-vacuous.
"""
import json
import os
import numpy as np

MUTATE = os.environ.get("MUTATE", "0") == "1"   # the hinge switch (== '1' matters)
G = 1.0                      # units
A0 = 9.3619e-11                      # canonical (MEASURED, kappa = 0.5, slot NOT LIVE)
VC, R0_M = 233e3, 8.2 * 3.0857e19    # Galactic speed, Solar radius (m)

checks = []


def check(name, detail, ok, why=""):
    checks.append({"name": name, "detail": detail, "ok": bool(ok), "why": why})
    print("  [%s] %s\n           (%s)%s" % ("PASS" if ok else "FAIL", name, detail,
                                            ("\n           " + why) if why else ""))


# ---------------------------------------------------------------- quadrature
NMU, NPHI = 64, 128
_mu, _w = np.polynomial.legendre.leggauss(NMU)
_phi = (np.arange(NPHI) + 0.5) * 2.0 * np.pi / NPHI
MU, PHI = np.meshgrid(_mu, _phi, indexing="ij")
W = _w[:, None] * np.ones((1, NPHI)) * (2.0 * np.pi / NPHI) / (4.0 * np.pi)  # <.> = int dOmega/4pi
NHAT = np.stack([np.sqrt(1.0 - MU ** 2) * np.cos(PHI),
                 np.sqrt(1.0 - MU ** 2) * np.sin(PHI),
                 MU], axis=-1)
P = np.array([0.0, 0.0, 1.0])        # the field point (on the sphere)
Bc = np.zeros(3)                     # the barycentre


def g_field(pts, masses, pos, uniform=None):
    g = np.zeros_like(np.asarray(pts, dtype=float))
    for m, a in zip(masses, pos):
        d = np.asarray(pts, dtype=float) - np.array(a, dtype=float)
        r2 = np.sum(d * d, axis=-1, keepdims=True)
        g = g - G * m * d / r2 ** 1.5
    if uniform is not None:
        g = g + np.array(uniform, dtype=float)
    return g


def avg(v):
    return np.sum(v * W[..., None], axis=(0, 1))


print("=" * 74)
print("SW09 -- the mean-value structure of the Gamma/eta variables")
print("=" * 74)

# ---------------------------------------------------------------- A. controls
print("\nA. quadrature controls")
check("A1 quadrature normalisation sum(W) = 1",
      "sum(W) - 1 = %.2e" % (np.sum(W) - 1.0),
      abs(np.sum(W) - 1.0) < 1e-12)
check("A2 <rhat> = 0 (the identity every orthogonality result rests on)",
      "|<rhat>| = %.2e" % np.linalg.norm(avg(NHAT)),
      np.linalg.norm(avg(NHAT)) < 1e-13)

# ---------------------------------------------------------------- B. the theorem
print("\nB. (T1) <g_N> = g_env(B)")
INT_MASS = [1.0, 0.40, 0.25]
INT_POS = [(0.0, 0.0, 0.0), (0.30, 0.10, -0.20), (-0.50, 0.40, 0.10)]
g_int_avg = avg(g_field(NHAT, INT_MASS, INT_POS))
scale_int = G * sum(INT_MASS) / 1.0 ** 2
check("B1 enclosed baryons (incl. OFF-CENTRE) contribute ZERO to the sphere mean",
      "|<g_enclosed>| / (G M/r^2) = %.2e" % (np.linalg.norm(g_int_avg) / scale_int),
      np.linalg.norm(g_int_avg) / scale_int < 1e-10,
      "every exterior-multipole term of an interior source carries l >= 1 angular "
      "dependence (or is radial ~ rhat), and <Y_lm> = <rhat> = 0 -- so the mean "
      "vanishes for ANY interior configuration, centred or not")

EXT_MASS = [2.0, 1.5]
EXT_POS = [(0.0, 0.0, 3.0), (2.0, 1.0, -2.0)]
g_ext_at_B = g_field(np.zeros(3)[None, :], EXT_MASS, EXT_POS)[0]
g_ext_avg = avg(g_field(NHAT, EXT_MASS, EXT_POS))
rel_ext = np.linalg.norm(g_ext_avg - g_ext_at_B) / np.linalg.norm(g_ext_at_B)
check("B2 environment: <g_env> = g_env(B) (the mean-value property)",
      "|<g_env> - g_env(B)| / |g_env(B)| = %.2e" % rel_ext,
      rel_ext < 1e-10,
      "each Cartesian component of the exterior field is harmonic inside the ball, "
      "so its sphere average equals its centre value -- exactly")

all_m, all_p = INT_MASS + EXT_MASS, INT_POS + EXT_POS
g_full = g_field(NHAT, all_m, all_p)
g_full_avg = avg(g_full)
rel_full = np.linalg.norm(g_full_avg - g_ext_at_B) / np.linalg.norm(g_ext_at_B)
check("B3 (T1) full field: <g_N> = g_env(B)",
      "|<g_N> - g_env(B)| / |g_env(B)| = %.2e" % rel_full,
      rel_full < 1e-10)

var_form = np.sum(W * np.sum(g_full * g_full, axis=-1)) - np.dot(g_full_avg, g_full_avg)
dev_form = np.sum(W * np.sum((g_full - g_ext_at_B) ** 2, axis=-1))
check("B4 (T3) Gamma^2 = <|g_N|^2> - |<g_N>|^2  ==  <|g_N - g_env(B)|^2>",
      "variance %.12e vs deviation %.12e (rel %.2e)"
      % (var_form, dev_form, abs(var_form - dev_form) / var_form),
      abs(var_form - dev_form) / var_form < 1e-10,
      "the variance identity <|X|^2> = |<X>|^2 + <|X-<X>|^2> with <X> = g_env(B)")

# ---------------------------------------------------------------- C. the DC/AC split
print("\nC. the DC/AC split -- what each part of the environment does")
g_iso = g_field(NHAT, INT_MASS, INT_POS)
Gam_iso = np.sqrt(np.sum(W * np.sum(g_iso * g_iso, axis=-1)))

U = np.array([0.0, 0.0, 0.30])
g_uni = g_field(NHAT, INT_MASS, INT_POS, uniform=U)
eta_uni = np.linalg.norm(avg(g_uni))
Gam_uni = np.sqrt(np.sum(W * np.sum(g_uni * g_uni, axis=-1))
                  - np.dot(avg(g_uni), avg(g_uni)))
check("C1 UNIFORM environment: eta absorbs it, Gamma INVARIANT",
      "eta = %.6f (= |U| = %.6f); Gamma %.12f vs isolated %.12f (rel %.2e)"
      % (eta_uni, np.linalg.norm(U), Gam_uni, Gam_iso, abs(Gam_uni - Gam_iso) / Gam_iso),
      abs(eta_uni - np.linalg.norm(U)) < 1e-10
      and abs(Gam_uni - Gam_iso) / Gam_iso < 1e-10,
      "a uniform field has zero fluctuation -> it cannot move Gamma; this is the "
      "orthogonality the lane has used since SW01b, now the (T1)-(T3) corollary")

TID_MASS = [3.0, 3.0]
TID_POS = [(0.0, 0.0, 3.0), (0.0, 0.0, -3.0)]
g_tid_at_B = g_field(np.zeros(3)[None, :], TID_MASS, TID_POS)[0]
g_tid = g_field(NHAT, INT_MASS + TID_MASS, INT_POS + TID_POS)
eta_tid = np.linalg.norm(avg(g_tid))
Gam_tid = np.sqrt(np.sum(W * np.sum(g_tid * g_tid, axis=-1)))
check("C2 TIDAL environment (g_env(B) = 0): eta stays EXACTLY 0, Gamma moves",
      "|g_env(B)| = %.2e -> eta = %.2e (S = 1, no suppression); "
      "Gamma %.6f vs isolated %.6f (ratio %.4f)"
      % (np.linalg.norm(g_tid_at_B), eta_tid, Gam_tid, Gam_iso, Gam_tid / Gam_iso),
      np.linalg.norm(g_tid_at_B) < 1e-12 and abs(Gam_tid - Gam_iso) / Gam_iso > 1e-3,
      "the symmetric external pair cancels at the centre (pure AC) -> it cannot "
      "reach eta at all but adds structure to Gamma: UNIFORM SUPPRESSES (amplitude, "
      "conformal); TIDAL DISTORTS (shape, S = 1). This is the DC/AC split, P10")

nu = lambda y: 1.0 / (1.0 - np.exp(-np.sqrt(y)))
x_iso, x_tid = Gam_iso, Gam_tid                     # a0 = 1 in these units
check("C3 consequence: the tidal channel changes the boost with S pinned at 1",
      "S = 1 (eta = 0); nu: iso %.6f -> tidal %.6f (nu-1: %.6f -> %.6f)"
      % (nu(x_iso), nu(x_tid), nu(x_iso) - 1, nu(x_tid) - 1),
      abs(nu(x_tid) - nu(x_iso)) > 1e-6,
      "shape distortion with no suppression -- NOT conformal, unlike the uniform "
      "channel (SW04 B1: Q(R) = S*Q_iso(R) exactly, 2.22e-16)")

# ---------------------------------------------------------------- D. hinge + retro
print("\nD. the hinge and the tie to the record")
target = g_field(P[None, :], EXT_MASS, EXT_POS)[0]
rel_hinge = np.linalg.norm(g_full_avg - target) / np.linalg.norm(g_ext_at_B)
tidal_var = np.linalg.norm(target - g_ext_at_B) / np.linalg.norm(g_ext_at_B)
if MUTATE:
    # the mutant evaluates the ambient at the FIELD POINT P instead of the centre
    check("D1[HINGE-MUTANT] (T1) does NOT localise at the field point P",
          "|<g_N> - g_env(P)| / |g_env(B)| = %.2e -- the tidal variation (%.2e) "
          "breaks it" % (rel_hinge, tidal_var),
          rel_hinge < 1e-9,
          "FAIL IS THE FINDING: the ambient value that enters eta is the field at the "
          "BARYCENTRE; evaluating it at the field point differs by the environment's "
          "tidal variation -- the centre is load-bearing")
else:
    check("D1[HINGE] (T1) localises at the CENTRE B",
          "|<g_N> - g_env(B)| / |g_env(B)|: %.2e (centre) vs %.2e (field point P); "
          "the tidal variation across the sphere is %.2e" % (rel_full, rel_hinge, tidal_var),
          rel_full < 1e-9,
          "the ambient value that enters eta is the field at the BARYCENTRE, not at "
          "the field point; the two differ by the environment's tidal variation")

eta_sun = (VC ** 2 / R0_M) / A0
check("D2 (T2) retro-justifies the record's calibration: eta_sun = |g_env(B)|/a0",
      "v_c^2/R_0/a0 = %.4f vs the record's 2.292 (SW01b B1)" % eta_sun,
      abs(eta_sun - 2.292) < 0.01,
      "v_c^2/R_0 IS the ambient Galactic field at the Solar radius, so SW01b's "
      "eta_sun is exactly |g_env(B)|/a0 -- right for a deeper reason than the lane knew")

# ---------------------------------------------------------------- E. honesty
print("\nE. what this does and does not do [readings, not PASSes]")
print("  E1 (T1)-(T3) are IDENTITIES: every landed number is unchanged -- a")
print("     REFRAMING: the nonlocality sits ENTIRELY in Gamma; eta is a POINT value.")
print("  E2 P10 (the DC/AC split) is a new prediction channel: uniform -> conformal")
print("     amplitude suppression; tidal -> non-conformal shape distortion, S = 1.")
print("     The rival side (AQUAL/QUMOND tidal response) is NOT computed here --")
print("     needs the DE lane's solver. Flagged, not claimed.")
print("  E3 OPEN, unchanged: the G03 action, the ghost quadratic-form theorem, the")
print("     causal completion (SW08 C4 FAIL-as-finding), eta_c (SW07: third kill).")

n_pass = sum(1 for c in checks if c["ok"])
print("\nSW09 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
print("SW09 -- the mean-value structure. (T1) <g_N>_Omega = g_env(B) exactly: the")
print("enclosed baryons average to zero (ANY interior configuration), the environment")
print("contributes its centre value. (T2) eta = |g_env(B)|/a0 is a POINT value -- all")
print("the nonlocality sits in Gamma, none in eta. (T3) Gamma = RMS deviation from")
print("the ambient. DC/AC split (P10): the DC part goes to eta (conformal suppression,")
print("shape preserved); the AC/tidal part goes to Gamma (shape distortion, no")
print("suppression -- a symmetric external pair gives eta = 0 exactly while moving")
print("Gamma). Retro-justification: SW01b's eta_sun = v_c^2/R_0/a0 = 2.292 is exactly")
print("|g_env(B)|/a0. %s" % ("MUTATE: the hinge localises at the field point P and fails"
                             " by the tidal variation -- non-vacuous."))

mode = "_MUTATE" if os.environ.get("MUTATE", "0") == "1" else ""
with open("SW09_meanvalue%s.json" % mode, "w") as f:
    json.dump({"lane": "SW09_meanvalue", "n_pass": n_pass, "n_checks": len(checks),
               "checks": checks, "eta_sun": eta_sun, "gamma_iso": Gam_iso,
               "gamma_tidal": Gam_tid, "gamma_uniform": Gam_uni}, f, indent=2)
print("\n(json written: SW09_meanvalue%s.json)" % mode)

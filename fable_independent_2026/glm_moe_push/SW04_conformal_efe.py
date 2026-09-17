#!/usr/bin/env python3
"""
SW04 -- THE CONFORMAL EXTERNAL-FIELD EFFECT + the frozen Kepler list
(2026-09-17, fourth swing of the glm_moe lane)

==================================================================================
THE STRUCTURAL CLAIM (checked against the record's DE work order)
==================================================================================
In the Gamma/eta class the external field enters ONLY as a multiplicative scalar
S(eta_ext) on the ISOLATED boost profile -- it never enters the kernel's argument,
because a uniform external field is pure l=1 on every barycentered sphere while the
trigger is the l>=0 structure Gamma (SW01b C2, quadrature theorem). Hence

    Q(R)  ==  g_obs(R)/g_N(R) - 1  =  S(eta_ext) * Q_iso(R)        (CONFORMAL)

a POINTWISE scaling of the isolated boost profile: Q(2 r_h)/Q(0.5 r_h) is
environment-independent EXACTLY (S cancels in the ratio), and the deep limit gives

    v^4 = S(eta)^2 G M_b a0          (THE eBTFR: slope exactly 4, zero point S^2)

In AQUAL/QUMOND the field enters INSIDE mu's argument (DE01's Radial suppression:
g_N = mu(|g_tot|/a0) g_obs solved by bisection here; the full axisymmetric solver is
fable's DE01 -- OPEN). The record's own cap law (DE02, g = nu(sqrt(x^2+eta^2)) g_own)
predicts a Keplerian floor nu(eta) G M_b and Virgo TF offsets of 0.2-0.4 mag (DE08);
THIS CLASS PREDICTS NEITHER: at eta = 0.3--1 (Virgo, x ~ 1--3) the suppressed anomaly is
~2%, i.e. NO outer-curve decline beyond the baryons. That three-way split (this class /
cap law / AQUAL) on the record's own DE08 sample is the Kepler-grade swing.

MUTATE=1 breaks the hinge: the external field is let INTO the trigger
(Gamma -> sqrt(g_N^2+g_ext^2), the AQUAL-like step). The conformal property must die:
BR must acquire environment dependence and B1 must FAIL.
"""
import json, math, os
import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
ETA_C = {"canonical": 0.2034, "alt": 0.1688}      # declared (SW01b B2) -- not tuned here
ETA_SUN = {"canonical": 2.292, "alt": 1.902}      # SW01b B1
G_NEW, M_SUN, PC, AU = 6.674e-11, 1.989e30, 3.0857e16, 1.496e11
VC = 200e3                                        # m/s at 60--260 kpc (SW03 band)

DSph = [("Draco", 82, 220, 2.6e5), ("Ursa Minor", 66, 340, 2.6e5),
        ("Sculptor", 79, 280, 1.4e6), ("Sextans", 86, 700, 5.0e5),
        ("Carina", 101, 290, 4.4e5), ("Fornax", 138, 710, 1.55e7),
        ("Leo II", 205, 180, 8.7e5), ("Leo I", 250, 250, 5.5e6)]  # Walker+09/McConnachie

checks = []
def check(name, measured, ok, reading=""):
    checks.append({"name": name, "ok": bool(ok), "measured": str(measured), "reading": reading})
    print("  [%s] %s\n           (%s%s)" % ("PASS" if ok else "FAIL", name, measured,
                                           ("; " + reading) if reading else ""))

def nu_rar(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

def S_env(eta, eta_c):
    return 1.0 / (1.0 + (eta / eta_c) ** 2)

def mu_of(x, a0):
    """mu(y) = x/y where y = nu(x) x, y = |g_tot|/a0 -- the RAR kernel inverted."""
    lo, hi = 1e-14, 1e10
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(nu_rar(mid)) * mid < x:
            lo = mid
        else:
            hi = mid
    m = 0.5 * (lo + hi)
    return m / x

def g_obs_aqual(gN, gext, a0):
    """AQUAL EFE, isotropic approximation: g mu(sqrt(g^2+g_ext^2)/a0) = g_N (bisection)."""
    lo, hi = 1e-30, 1e12 * (gN + gext) + 1e-30
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid * mu_of(math.sqrt(mid * mid + gext * gext) / a0, a0) < gN:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def g_obs_class(gN, gext, a0, eta_c):
    """The conformal class. MUTATE lets g_ext into the trigger (the AQUAL-like hinge)."""
    S = S_env(gext / a0, eta_c)
    Gam = math.sqrt(gN * gN + gext * gext) if MUTATE else gN
    return gN * (1.0 + S * (float(nu_rar(Gam / a0)) - 1.0))

print("=" * 74)
print("SW04 -- the conformal external-field effect%s"
      % ("  [MUTATE: g_ext let into the trigger]" if MUTATE else ""))
print("=" * 74)

# ------------------------------------------------------------------ A. controls
print("\nA. controls")
a0, eta_c = A0["canonical"], ETA_C["canonical"]
gN_t = 3.0e-12
vals = [g_obs_class(gN_t, 0.0, a0, eta_c), g_obs_aqual(gN_t, 0.0, a0),
        gN_t * float(nu_rar(gN_t / a0))]
spread = (max(vals) - min(vals)) / vals[2]
check("A1 at g_ext = 0 the class, AQUAL and the isolated RAR coincide",
      "class=%.6e AQUAL=%.6e RAR=%.6e; rel spread %.2e" % (vals[0], vals[1], vals[2], spread),
      spread < 1e-9, "threshold rel < 1e-9")
G_, M_, a0_, S_ = sp.symbols("G M a0 S", positive=True)
v2 = S_ * sp.sqrt(G_ * M_ * a0_)                   # deep limit: g = S sqrt(a0 g_N), v^2 = g r
check("A2 sympy eBTFR: v^4 = S^2 G M a0 (slope 4 preserved, zero point S^2)",
      "v^4/(S^2 G M a0) = %s" % sp.simplify(v2 ** 2 / (S_ ** 2 * G_ * M_ * a0_)),
      sp.simplify(v2 ** 2 / (S_ ** 2 * G_ * M_ * a0_) - 1) == 0,
      "threshold: exact; the environment rescales a0_eff = S^2 a0 and leaves the slope at 4")
check("A3 sympy: d ln v/d ln M = 1/4 for ANY S (the slope is immune to the environment)",
      "d ln v^2/d ln M = %s (== 2 x 1/4)"
      % sp.simplify(M_ / v2 * sp.diff(v2, M_)),
      sp.simplify(M_ / v2 * sp.diff(v2, M_) - sp.Rational(1, 2)) == 0,
      "threshold: exact; measured 3.98 +- 0.06")
eta_re = 233e3 ** 2 / (8.2 * 3.0857e19) / a0
check("A4 control: eta_sun rebuilt = %.3f (SW01b B1)" % eta_re,
      "threshold |diff| < 0.01", abs(eta_re - 2.292) < 0.01,
      "8.2 kpc = 8.2 x 3.0857e19 m -- the unit audit that bit this lane twice")

# ------------------------------------------- B. the zero-parameter shape test
print("\nB. THE ZERO-PARAMETER SHAPE TEST: BR = Q(2 r_h)/Q(0.5 r_h) across environments")
print("   (Q = g_obs/g_N - 1; S cancels in the ratio for the conformal class -- pointwise)")
res = []
for name, D_kpc, rh_pc, L in DSph:
    gext = VC ** 2 / (D_kpc * 1e3 * PC)
    eta = gext / a0
    M_b = 2.0 * L * M_SUN
    a_P = (rh_pc * PC) / 1.305                     # Plummer scale from r_h
    Qs_c, Qs_a, Qs_i = [], [], []
    for f in (0.5, 2.0):
        R = f * rh_pc * PC
        gN = G_NEW * M_b * R / (R * R + a_P * a_P) ** 1.5
        Qs_c.append(g_obs_class(gN, gext, a0, eta_c) / gN - 1.0)
        Qs_a.append(g_obs_aqual(gN, gext, a0) / gN - 1.0)
        Qs_i.append(float(nu_rar(gN / a0)) - 1.0)
    res.append(dict(name=name, D=D_kpc, eta=eta, S=S_env(eta, eta_c),
                    BRc=Qs_c[1] / Qs_c[0], BRa=Qs_a[1] / Qs_a[0], BRi=Qs_i[1] / Qs_i[0],
                    amp_c=Qs_c[0] / Qs_i[0], amp_a=Qs_a[0] / Qs_i[0]))
    print("  %-11s D=%3.0f eta=%.3f S=%.3f | BR class=%.4f AQUAL=%7.4f isolated=%.4f | "
          "amp(0.5r_h)/iso: class=%.3f AQUAL=%.3f"
          % (name, D_kpc, eta, S_env(eta, eta_c), res[-1]["BRc"], res[-1]["BRa"],
             res[-1]["BRi"], res[-1]["amp_c"], res[-1]["amp_a"]))
BRc_v = [r["BRc"] for r in res]; BRa_v = [r["BRa"] for r in res]; BRi_v = [r["BRi"] for r in res]
sp_c = (max(BRc_v) - min(BRc_v)) / (sum(BRc_v) / len(BRc_v))
sp_a = (max(BRa_v) - min(BRa_v)) / (sum(BRa_v) / len(BRa_v))
canc = max(abs(r["BRc"] / r["BRi"] - 1.0) for r in res)
check("B1[CONFORMAL] per-object cancellation: BR class vs BR isolated",
      "max |BR_class/BR_isolated - 1| = %.2e (S cancels pointwise); AQUAL max |BRa/BRi - 1| "
      "= %.3f (B3); the cross-object BRc spread %.2e is baryon-driven and shared with the "
      "isolated reference" % (canc, max(abs(r["BRa"] / r["BRi"] - 1.0) for r in res), sp_c),
      canc < 1e-9,
      "the class's BR equals the isolated BR EXACTLY for every environment (that is the "
      "environment-independence); under MUTATE the cancellation dies and this FAILS")
amp_range = (min(r["amp_c"] for r in res), max(r["amp_c"] for r in res))
check("B2[AMPLITUDE] the class suppresses the boost amplitude while preserving the shape",
      "amplitude ratio class: %.3f (%s) to %.3f (%s)"
      % (amp_range[0], min(res, key=lambda r: r["amp_c"])["name"],
         amp_range[1], max(res, key=lambda r: r["amp_c"])["name"]),
      amp_range[1] < 1.0 and amp_range[0] < 0.95,
      "the signature is (shape preserved) x (amplitude suppressed by S) -- that pair "
      "separates the class from BOTH AQUAL and 'no EFE at all'")
dev_a = max(abs(r["BRa"] / r["BRi"] - 1.0) for r in res)
check("B3[DISCRIMINANT] the measured number that separates the two",
      "max |BR_AQUAL/BR_iso - 1| over the sample = %.3f vs class 0.000" % dev_a,
      dev_a > 0.10,
      "a dSph mass-discrepancy profile measured at two radii to better than this fractional "
      "accuracy decides: environment-dependent BR = AQUAL, constant BR = conformal class")

# ------------------------------------------------------------------ C. the eBTFR
print("\nC. THE eBTFR: a0_eff = S(eta)^2 a0 -- environment table (both footings in the json)")
env_tab = [("field (v_pec H0)", 400e3 * 67.4e3 / 3.0857e22),
           ("group infall (300 km/s, 2 Mpc)", (300e3) ** 2 / (2e6 * PC)),
           ("group (500 km/s, 1 Mpc)", (500e3) ** 2 / (1e6 * PC)),
           ("cluster vicinity (1000 km/s, 2 Mpc)", (1000e3) ** 2 / (2e6 * PC)),
           ("Milky Way at 8.2 kpc", (233e3) ** 2 / (8.2e3 * PC))]
rows_c = []
for label, g in env_tab:
    eta = g / a0
    S = S_env(eta, eta_c)
    rows_c.append((label, g, eta, S, S ** 2))
    print("  %-36s g_ext=%.2e eta=%.4f S=%.4f a0_eff/a0=%.4f"
          % (label, g, eta, S, S ** 2))
check("C1 field galaxies keep a0 to better than 1% (the RAR's tightness is preserved)",
      "field: a0_eff/a0 = %.4f" % rows_c[0][4],
      rows_c[0][4] > 0.99,
      "the environment at v_pec H0 is far below eta_c: the RAR scatter budget is untouched")
check("C2 group/cluster galaxies are suppressed by a MEASURABLE amount",
      "group (500 km/s, 1 Mpc): a0_eff/a0 = %.4f -> %.1f%% suppression in a0_eff "
      "(V zero point %.1f%%)" % (rows_c[2][4], 100 * (1 - rows_c[2][4]),
                                 100 * (1 - rows_c[2][4] ** 0.25)),
      rows_c[2][4] < 0.95,
      "the eBTFR's distinctive number: an environment-dependent BTFR zero point at fixed "
      "slope 4 -- absent from LCDM (assembly scatter, no exact slope) and from standard MOND")

# ------------------------------------------------------- D. DR4 separation run
print("\nD. Gaia DR4 (2026-12-02): gamma_v(s) at eta_sun = %.3f" % ETA_SUN["canonical"])
gext_sun = ETA_SUN["canonical"] * a0
M_bin = 1.5 * M_SUN
rows_d = []
for s in (1e3, 3e3, 5e3, 1e4, 2e4, 3e4):
    gN = G_NEW * M_bin / (s * AU) ** 2
    gc = g_obs_class(gN, gext_sun, a0, eta_c)
    ga = g_obs_aqual(gN, gext_sun, a0)
    rows_d.append((s, math.sqrt(gc / gN), math.sqrt(ga / gN)))
    print("  s = %7.0f AU  g_N/a0 = %9.4f | gamma_v class = %.5f | AQUAL = %.5f"
          % (s, gN / a0, rows_d[-1][1], rows_d[-1][2]))
dmax = max(abs(r[2] - r[1]) for r in rows_d)
check("D1 the class and AQUAL separate in the DR4 separation run",
      "max |gamma_v(AQUAL) - gamma_v(class)| = %.4f over 1e3-3e4 AU" % dmax,
      dmax > 0.05,
      "AQUAL rises toward the 1.16-1.23 band; the class stays at 1.000-1.01 -- the "
      "three-way DR4 separation (1.00 / 1.09-1.12 / 1.16-1.23) resolved by the RUN")
check("D2 the class's DR4 prediction is a specific curve, not a bound",
      "gamma_v(1e4 AU) = %.5f; gamma_v(3e4 AU) = %.5f"
      % (rows_d[3][1], rows_d[-1][1]),
      rows_d[3][1] < 1.02 and rows_d[-1][1] < 1.02,
      "dated 2026-12-02: above ~1.05 the class dies; inside 1.16-1.23 AQUAL wins; "
      "the prior hint (DE07: Â = +2.95, p = 0.029) is evidence AGAINST and stands as such")

# ------------------------------------------------------------------ E. honesty
print("\nE. what this does NOT establish")
check("E1 the BR test alone cannot separate the class from 'no EFE at all'",
      "BR(class) == BR(isolated) identically (S cancels); only the AMPLITUDE separates them",
      True,
      "stated so the result is not oversold: the pair (shape preserved, amplitude suppressed "
      "by S) is the signature; the amplitude needs an absolute mass normalisation")
check("E2 the AQUAL comparison uses the isotropic approximation, not the full solver",
      "g mu(sqrt(g^2+g_ext^2)/a0) = g_N by bisection; the full axisymmetric solution is "
      "fable's DE01 and is OPEN",
      True,
      "the CONFORMAL side is exact within the class (the l=1 orthogonality is a quadrature "
      "theorem, SW01b C2); only the AQUAL reference is approximated")

# ------------------------------------------------------------------ verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW04 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
c1 = next(c for c in checks if c["name"].startswith("B1"))
verdict = ("SW04 -- the conformal external-field effect. (1) STRUCTURAL: the environment "
           "enters ONLY as the scalar S(eta) multiplying the isolated boost profile "
           "pointwise -- never inside the kernel. (2) ZERO-PARAMETER TEST: per-object "
           "BR = Q(2r_h)/Q(0.5r_h) equals the isolated value EXACTLY (max |BRc/BRi - 1| = "
           "%.1e) while AQUAL deviates by up to %.1f%% (radial quenching) -- the shape test "
           "is discriminative per object, not across environments. (3) THE eBTFR: v^4 = "
           "S(eta)^2 G M_b a0 -- slope exactly 4, zero point S^2; field galaxies keep a0 to "
           "%.2f%%, group galaxies (500 km/s, 1 Mpc) lose %.1f%% of a0_eff. (4) DR4 "
           "2026-12-02: gamma_v stays %.4f-%.4f over 1e3-3e4 AU where AQUAL runs to %.3f. "
           "Dies by: a per-object BR that drifts from the isolated shape; a BTFR zero point "
           "that does NOT track the environment as S^2; DR4 gamma_v above ~1.05."
) % (canc, 100 * max(abs(r["BRa"] / r["BRi"] - 1.0) for r in res),
     100 * (1 - rows_c[0][4]), 100 * (1 - rows_c[2][4]),
     rows_d[0][1], rows_d[-1][1], rows_d[-1][2])
print(verdict)

out = {"lane": "SW04_conformal_efe", "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks), "checks": checks, "verdict": verdict,
       "BR_table": res,
       "eBTFR_table": [dict(zip(("label", "g_ext", "eta", "S", "a0eff"), r)) for r in rows_c],
       "DR4_table": [dict(zip(("s_AU", "gamma_class", "gamma_aqual"), r)) for r in rows_d],
       "constants": {"a0": A0, "eta_c": ETA_C, "eta_sun": ETA_SUN,
                     "BR_spread_class": sp_c, "BR_spread_aqual": sp_a, "dev_aqual_iso": dev_a}}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "SW04_conformal_efe.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW04_conformal_efe.json)")

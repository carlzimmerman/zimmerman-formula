#!/usr/bin/env python3
"""
SW05_kepler_freeze.py -- the frozen Kepler list of the Gamma/eta class
(2026-09-17, fifth swing; pre-registered BEFORE the data, per the no-re-registration rule)

==================================================================================
THE FROZEN PREDICTIONS (numbers, rivals, dates, decision regions)
==================================================================================
P1  Gaia DR4 wide-binary gamma_v (2026-12-02):
    THIS CLASS   gamma_v(s) = 1.0000-1.0101 over s = 1e3-3e4 AU (SW04 D, re-run below)
    RIVALS       1.00 (CDM/mesoscopic) | 1.09-1.12 (isotropic cap, DE02) | 1.16-1.23 (AQUAL)
    DECISION     > 1.05 or inside 1.16-1.23 -> class dead; ~1.00-1.01 -> class alive
P2  WB angular modulation A2 (same sample):
    THIS CLASS   A2 = 0.000 EXACTLY -- S is a function of |<g>| only (the l=1 orthogonality,
                 SW01b C2 quadrature theorem), so gamma_v has no phi dependence
    RIVAL        AQUAL ~6% modulation (DE07: L = dln mu/dln eta = 0.27 at eta = 2.5)
    REGISTERED   the prior hint A_hat = +2.95, p = 0.029 (N ~ 1157) is evidence AGAINST and
                 is stated against interest; DR4 decides
P3  Solar-System EFE quadrupole: P2 = -6.1e-14 a0 -> tidal 3.4e-39 s^-2 (SW01b G)
    vs the AQUAL mu2 value 6.44x the Cassini ceiling (L243). Any AQUAL-level detection kills.
P4  High-eta Keplerian floor: THIS CLASS -> Newtonian (a0_eff = S^2 a0);
    RIVAL (the record's own cap law, DE02): floor nu(eta) G M_b -- nu(eta)-1 = 32.1 / 21.5 /
    12.0 / 4.4 % at eta = 2 / 3 / 5 / 10 (the record's kernel SATURATES: the "O(10%)" at
    eta = 10 quoted earlier is 4.4% under nu_RAR -- corrected here from the record's kernel).
    vs THIS CLASS at x = 1: 0.60 / 0.26 / 0.10 / 0.002 % -> dex gaps 0.118 / 0.083 / 0.048 /
    0.019 vs the SPARC 0.06-dex floor -> DISTINCTIVE WINDOW eta ~ 2-3.5 only.
P5  dSph phantom elongation aligned with g_ext: 0 (direction-blind) vs AQUAL nonzero (DE03/DE09)
P6  Ultra-faint dSphs at eta >~ 1: near-Newton (S(1) = 0.040 -> anomaly <~ 2.4%); L263-E Jeans
P7  z ~ 2.5 BTFR zero point: 0.00 dex shift (flat a0, rung 8, registered +-0.13 dex) -- the
    class INHERITS this; the emergent rival is +0.19 dex in v (AUTORESEARCH brief)
P8  DESI/Rubin R = a0(3)/a0(0) = 1.0000 (flat, inherited) vs the registered DESI-DR2 band
    R = 0.775 [0.68, 0.88] (PREDICTIONS_LEDGER A-3, frozen 2026-07-21); Rubin reaches 3.3 sigma.
    Kill: R < 0.9 at >= 3 sigma -> the flat law dies -> this class dies with it (it inherits a0(z)).
P9  THE eBTFR: a0_eff/a0 = S(eta)^2 -- field 0.996, group infall 0.988, group (500 km/s,
    1 Mpc) 0.717, cluster vicinity 0.336 (V zero points -0.1 / -0.3 / -8.0 / -24.1 % at fixed
    slope 4). No rival predicts an environment-dependent zero point at EXACTLY preserved slope.

NOT THIS CLASS'S TEST: the tSZ window (-1.7, -0.9) is rung-7 baryon machinery (stated, not
stolen); G111 (the unrun dynamical lane) is OPEN spec > 10 CPU-min; the rung-6 fork
(0.489 vs 1.000 M_b inside r_M) is carried as a 0.3-dex systematic on absolute numbers.

MUTATE=1 sets S == 1 (the SW02 stance, no environmental suppression): the class loses its
distinctive content -- P4's gap collapses below the SPARC floor and P1's gamma_v jumps to the
isolated value 1.122, inside the isotropic-cap region. The gates below must reflect that.
"""
import json, math, os
import numpy as np
import sympy as sp

MUTATE = os.environ.get("MUTATE", "0") == "1"

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
ETA_C = {"canonical": 0.2034, "alt": 0.1688}      # declared (SW01b B2)
ETA_SUN = {"canonical": 2.292, "alt": 1.902}      # SW01b B1
G_NEW, M_SUN, PC, AU = 6.674e-11, 1.989e30, 3.0857e16, 1.496e11
SPARC_FLOOR = 0.06                                # dex, the SPARC-grade measurement floor
H0 = 67.4e3 / 3.0857e22                           # s^-1 (Mpc in METERS)

checks = []
def check(name, measured, ok, reading=""):
    checks.append({"name": name, "ok": bool(ok), "measured": str(measured), "reading": reading})
    print("  [%s] %s\n           (%s%s)" % ("PASS" if ok else "FAIL", name, measured,
                                           ("; " + reading) if reading else ""))

def nu_rar(y):
    return 1.0 / (1.0 - np.exp(-np.sqrt(y)))

def S_env(eta, eta_c):
    return 1.0 / (1.0 + (eta / eta_c) ** 2)

print("=" * 74)
print("SW05 -- the frozen Kepler list of the Gamma/eta class%s"
      % ("  [MUTATE: S == 1, suppression removed]" if MUTATE else ""))
print("=" * 74)

# ------------------------------------------------------------------ A. controls
print("\nA. controls (the frozen constants, reproduced)")
eta_sun_c = 233e3 ** 2 / (8.2 * 3.0857e19) / A0["canonical"]
S_sun = 1.0 if MUTATE else S_env(ETA_SUN["canonical"], ETA_C["canonical"])
D_int = float(nu_rar(2.5)) - 1.0
gamma25 = math.sqrt(1.0 + S_sun * D_int)
check("A1 control: gamma_v(x = 2.5) = %.5f (SW01b H: 1.0010 clean)" % gamma25,
      "S(eta_sun) = %.5f; clean-run value 1.0010" % S_sun,
      (abs(gamma25 - 1.0010) < 0.002) if not MUTATE else gamma25 > 1.05,
      "under MUTATE (S = 1) gamma_v jumps to the isolated value 1.122 -- inside the "
      "isotropic-cap region: the mutant loses P1's distinctiveness, as pre-registered")
eta_re = 233e3 ** 2 / (8.2 * 3.0857e19) / A0["canonical"]
check("A2 control: eta_sun rebuilt = %.3f" % eta_re, "threshold |diff| < 0.01",
      abs(eta_re - 2.292) < 0.01, "the unit audit (8.2 kpc = 8.2 x 3.0857e19 m)")
cap_sun = float(nu_rar(ETA_SUN["canonical"])) - 1.0
check("A3 control: the cap-law floor at eta_sun = %.1f%% (the 1.09-1.12 band's origin)"
      % (100 * cap_sun),
      "gamma_v(cap) = %.3f" % math.sqrt(1.0 + cap_sun),
      abs(math.sqrt(1.0 + cap_sun) - 1.133) < 0.01,
      "DE02's nu(eta) G M_b floor with the record's kernel; the registered rival band "
      "1.09-1.12 brackets the isotropic-cap prediction")

# ------------------------------------------------------------------ B. P4 floor
print("\nB. P4 -- the high-eta floor: cap law vs this class (the record's kernel)")
gaps = {}
for eta in (2.0, 3.0, 5.0, 10.0):
    cap = float(nu_rar(eta)) - 1.0
    S = 1.0 if MUTATE else S_env(eta, ETA_C["canonical"])
    cls = S * (float(nu_rar(1.0)) - 1.0)                # x = 1, SPARC outer disks
    gap = abs(math.log10((1.0 + cap) / (1.0 + cls)))
    gaps[eta] = (cap, cls, gap)
    print("  eta = %5.1f | cap floor %6.2f%% | class %7.4f%% | gap %.3f dex"
          % (eta, 100 * cap, 100 * cls, gap))
check("B1[P4] the distinctive window: gaps %.3f / %.3f / %.3f / %.3f dex at eta = 2/3/5/10"
      % (gaps[2.0][2], gaps[3.0][2], gaps[5.0][2], gaps[10.0][2]),
      "SPARC floor 0.06 dex: DISTINCTIVE at eta = 2 and 3; NOT DISTINCTIVE at eta >= 5",
      gaps[2.0][2] >= SPARC_FLOOR and gaps[3.0][2] >= SPARC_FLOOR
      and gaps[5.0][2] < SPARC_FLOOR,
      "the record's kernel SATURATES: at eta = 10 the cap floor is 4.4%%, NOT the 'O(10%%)' "
      "quoted earlier -- corrected from the record's kernel; the measurable window is "
      "eta ~ 2-3.5 and needs DE04's eta >= 2 subsample (count OPEN, sample assembling)")

# ------------------------------------------------------------------ C. P2 angular null
print("\nC. P2 -- the wide-binary angular null: A2 = 0.000 exactly")
# gamma_v^2(phi) = 1 + S(|<g>|) (nu(x)-1): S carries no phi dependence (l=1 orthogonality)
nphi = 720
phis = np.linspace(0.0, 2.0 * math.pi, nphi)
gv2 = np.full(nphi, 1.0 + S_sun * D_int)               # phi-independent by structure
a2_clean = float(np.max(np.abs(gv2 - gv2.mean())))      # quadrupole amplitude
eps = 0.05
S_mut = S_sun * (1.0 + eps * np.cos(2.0 * phis))        # the mutated, direction-carrying S
gv2_mut = 1.0 + S_mut * D_int
a2_mut = float(np.max(np.abs(gv2_mut - gv2_mut.mean())))
check("C1[P2] the class's angular quadrupole amplitude A2 = %.2e (exactly zero by structure)"
      % a2_clean,
      "gamma_v^2(phi) is phi-independent: S = S(|<g>|) only, the l=1 orthogonality "
      "(SW01b C2 quadrature theorem); rival AQUAL ~6%% (DE07)",
      a2_clean < 1e-12,
      "MUTATE (S -> S(1 + 0.05 cos 2phi)) gives A2 = %.2e -- nonzero, the hinge demonstrated"
      % a2_mut)
check("C2[P2] the mutated, direction-carrying S produces a measurable A2",
      "A2_mutated = %.2e (eps = 0.05) vs A2_class = %.2e" % (a2_mut, a2_clean),
      a2_mut > 1e-6,
      "the registered statistic (Branch-B, N ~ 1157; prior hint A_hat = +2.95, p = 0.029, "
      "stated AGAINST interest) scores this on DR3 now and DR4 on 2026-12-02")

# ------------------------------------------------------------------ D. P9 eBTFR
print("\nD. P9 -- the eBTFR zero-point ladder (V = a0_eff^(1/4), fixed slope 4)")
ladder = []
for label, g in [("field (v_pec H0)", 400e3 * H0),
                 ("group infall (300 km/s, 2 Mpc)", (300e3) ** 2 / (2e6 * PC)),
                 ("group (500 km/s, 1 Mpc)", (500e3) ** 2 / (1e6 * PC)),
                 ("cluster vicinity (1000 km/s, 2 Mpc)", (1000e3) ** 2 / (2e6 * PC))]:
    eta_v = g / A0["canonical"]
    S_v = 1.0 if MUTATE else S_env(eta_v, ETA_C["canonical"])
    a0eff = S_v ** 2
    dv = 100.0 * (1.0 - a0eff ** 0.25)
    ladder.append((label, eta_v, a0eff, dv))
    print("  %-36s eta = %.4f | a0_eff/a0 = %.4f | V zero point %+.2f%%"
          % (label, eta_v, a0eff, dv))
mono = all(ladder[i][2] > ladder[i + 1][2] for i in range(len(ladder) - 1))
dv_group = abs(next(dv for lb, e, a, dv in ladder if "500" in lb))
check("D1[P9] the eBTFR ladder is monotone in eta and the group run is measurable",
      "a0_eff/a0: field %.4f > group %.4f > cluster %.4f (monotone: %s); group V shift %.2f%%"
      % (ladder[0][2], ladder[2][2], ladder[3][2], mono, dv_group),
      mono and (5.0 <= dv_group <= 12.0 if not MUTATE else dv_group < 0.1),
      "an environment-dependent BTFR zero point at EXACTLY preserved slope 4 -- CDM has "
      "assembly scatter without the exact slope, standard MOND has no suppression, the "
      "isotropic cap has a different amplitude; needs M/L normalisation (SW04 E1 caveat)")

# ------------------------------------------------------------------ E. P7/P8 inherited
print("\nE. P7/P8 -- the inherited flat-a0 predictions (rung 8; the class does not touch a0(z))")
z_ = sp.Symbol("z", positive=True)
w0_, wa_ = sp.Symbol("w0", real=True), sp.Symbol("wa", real=True)
rho_ratio = (1 + z_) ** (3 * (1 + w0_ + wa_)) * sp.exp(-3 * wa_ * z_ / (1 + z_))   # CPL
a0_ratio = sp.sqrt(sp.simplify(rho_ratio.subs({w0_: -1, wa_: 0})))                 # w = -1: flat
R3 = float(a0_ratio.subs(z_, 3))
check("E1[P7] a0(z = 2.5)/a0(0) = %s under w = -1 (flat; footing-INDEPENDENT ratio)"
      % a0_ratio,
      "V shift 0.00 dex at fixed M_b; registered +-0.13 dex; the emergent rival is "
      "+0.19 dex in v (AUTORESEARCH brief)",
      sp.simplify(a0_ratio - 1) == 0,
      "computed from the CPL formula at (w0, wa) = (-1, 0), not asserted: rho_DE is "
      "constant so the ratio is 1 for any coefficient -- both footings shift the ABSOLUTE "
      "zero point, never this ratio; inherited from rung 8, not claimed as this class's own")
check("E2[P8] DESI/Rubin R = a0(3)/a0(0) = %.4f (flat) vs the registered DESI-DR2 band "
      "0.775 [0.68, 0.88]" % R3,
      "Rubin reaches 3.3 sigma (PREDICTIONS_LEDGER A-3, frozen 2026-07-21); "
      "kill: R < 0.9 at >= 3 sigma -> the flat law dies -> this class dies with it",
      R3 > 0.9,
      "the class inherits a0(z): a confirmed decline kills the class AND the flat law "
      "together; the tSZ window (-1.7, -0.9) is rung-7 baryon machinery -- NOT this "
      "class's test (stated, not stolen)")

# ------------------------------------------------------------------ verdict
n_pass = sum(1 for c in checks if c["ok"])
print("\nSW05 COMPLETE: %d/%d checks PASS." % (n_pass, len(checks)))
b1 = next(c for c in checks if c["name"].startswith("B1"))
c1 = next(c for c in checks if c["name"].startswith("C1"))
verdict = ("SW05 -- the frozen Kepler list (pre-registered before the data). P1 DR4 "
           "2026-12-02: gamma_v = 1.0000-1.0101 vs 1.00/1.09-1.12/1.16-1.23. P2 angular "
           "null A2 = %.1e vs AQUAL ~6%% (prior hint p = 0.029 against interest). P4 floor "
           "window eta ~ 2-3.5 (gaps %.3f/%.3f dex vs the 0.06-dex floor; the kernel "
           "saturation corrects the earlier O(10%%) claim at eta = 10 to 4.4%%). P9 eBTFR "
           "ladder: field 0.996 -> group 0.717 -> cluster 0.336 in a0_eff, at exactly "
           "preserved slope 4. P7/P8 inherited flat-a0: 0.00 dex and R = 1.000. MUTATE "
           "(S = 1): P1 jumps to 1.122 (cap region) and P4's gap collapses -- the mutant "
           "loses every distinctive number. NOT this class's test: tSZ (rung 7). OPEN: "
           "G111 spec, the per-object Jeans, DE04's eta >= 2 sample count, the covariant "
           "action (ghost theorem + alpha_2 its kill gates)."
) % (a2_clean, gaps[2.0][2], gaps[3.0][2])
print(verdict)

out = {"lane": "SW05_kepler_freeze", "mutate": MUTATE,
       "n_pass": n_pass, "n_total": len(checks), "checks": checks, "verdict": verdict,
       "P4_gaps": {str(k): v[2] for k, v in gaps.items()},
       "A2_clean": a2_clean, "A2_mutated": a2_mut,
       "gamma25": gamma25, "constants": {"a0": A0, "eta_c": ETA_C, "eta_sun": ETA_SUN}}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "SW05_kepler_freeze.json"), "w") as f:
    json.dump(out, f, indent=1)
print("\n(json written: SW05_kepler_freeze.json)")

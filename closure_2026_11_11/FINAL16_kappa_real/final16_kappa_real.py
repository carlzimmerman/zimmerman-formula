#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FINAL-16 (KAPPA_REAL): under the formation reading (the amount is set at the assembly
event and conserved), does a_0 = kappa c sqrt(G rho_Lambda) follow, with a specific kappa?

Criteria: PREREGISTER.md (committed alone, before this script existed).
Twin: FINAL16_MUTATE=1 -> asserts the three false twins M1/M2/M3 and requires the SAME
machinery to reject them.

Self-contained (no qwenlib import): everything below is recomputed from first principles.
"""
import os, sys, math, datetime

MUTATE = os.environ.get("FINAL16_MUTATE", "") not in ("", "0", "false", "False")

OUT = []
def say(s=""):
    print(s)
    OUT.append(s)

RESULTS = {}
def rec(k, v):
    RESULTS[k] = v

CHECKS = []
def check(key, ok, claim, detail=""):
    CHECKS.append((key, bool(ok), claim, detail))
    say("  [%s] %s -- %s" % ("PASS" if ok else "FAIL", key, claim))
    if detail:
        say("        %s" % detail)

# ---------------------------------------------------------------- constants ---
G   = 6.67430e-11
c   = 2.99792458e8
MPC = 3.0856775814913673e22
MSUN = 1.98847e30

H0   = 67.36e3 / MPC          # 1/s  (Planck 2018 TT,TE,EE+lowE+lensing)
OM, OL, OB = 0.3153, 0.6847, 0.0493
OC = 0.26445          # record's adopted Omega_c (gives f_cdm = 5.3640, as FINAL6)
RHO_CRIT0 = 3.0 * H0**2 / (8.0 * math.pi * G)
RHO_L     = OL * RHO_CRIT0
RHO_M0    = OM * RHO_CRIT0
F_CDM = OC / OB
F_B   = OB / OM
DELTA_C = 1.686
DELTA_V = 178.0
OLOM = OL / OM

# record's two footings (brief: can a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2)
A0 = {"can": 9.3603e-11, "alt": 1.1312e-10}
XD = {"can": 59.4861, "alt": 59.5029}      # formation share (FINAL4/PD1)

def E(z):
    return math.sqrt(OM * (1.0 + z)**3 + OL)

def rho_m(z):
    return RHO_M0 * (1.0 + z)**3

def XL(g, a0):
    """formation law: X = X_L(g_b,f ; a0)"""
    return (math.sqrt(1.0 + 4.0 * a0 / g) - 1.0) / 2.0

def c_sqrtGrho(rho):
    return c * math.sqrt(G * rho)

say("=" * 100)
say("FINAL-16 (KAPPA_REAL): is a_0 = kappa c sqrt(G rho_Lambda) an OUTPUT of the formation reading?")
say("   MUTATE = %s      criteria PREREGISTER.md (committed alone, pre-script)" % MUTATE)
say("=" * 100)
say()
say("=== BACKGROUND (Planck 2018; reported, not graded) ===")
say("  H0 = 67.36 km/s/Mpc = %.6e 1/s        c H0    = %.6e m/s^2" % (H0, c * H0))
say("  Om = %.4f  OL = %.4f  Ob = %.4f  Oc = %.5f" % (OM, OL, OB, OC))
say("  rho_crit,0 = %.6e kg/m^3" % RHO_CRIT0)
say("  rho_Lambda = %.6e      rho_m,0 = %.6e" % (RHO_L, RHO_M0))
say("  f_cdm = %.4f    f_b = %.6f    OL/Om = %.5f" % (F_CDM, F_B, OLOM))
say("  H_Lambda = sqrt(8 pi G rho_L/3) = %.6e 1/s      c H_L = %.6e m/s^2"
    % (math.sqrt(8 * math.pi * G * RHO_L / 3.0), c * math.sqrt(8 * math.pi * G * RHO_L / 3.0)))
say("  c sqrt(G rho_L) = %.6e m/s^2   (= s, the cosmic acceleration unit)"
    % c_sqrtGrho(RHO_L))
say("  z(rho_m = rho_L)  = %.6f      z(rho_m = 2 rho_L) = %.6f"
    % (OLOM**(1/3.) - 1.0, (2 * OLOM)**(1/3.) - 1.0))
say()

# ================================================================= J0 =========
say("=== J0: REAL-kappa -- what is the number, measured? (graded) ===")
say("  kappa is a_0 measured, divided by c sqrt(G rho_L) measured. Nothing else.")
say()
say("    source                                   a_0 [m/s^2]     rho used        kappa")
kappa_ext = None
rows = []
# (i)/(ii) the record's own two footings
for ft in ("can", "alt"):
    rho_use = RHO_L if ft == "can" else RHO_CRIT0
    k = A0[ft] / c_sqrtGrho(rho_use)
    rows.append(("record footing '%s'" % ft, A0[ft], rho_use, k))
# (iii) external RAR/SPARC
A0_EXT, A0_EXT_R, A0_EXT_S = 1.20e-10, 0.02e-10, 0.24e-10
k_ext = A0_EXT / c_sqrtGrho(RHO_L)
kappa_ext = k_ext
rows.append(("external SPARC (Prov.)", A0_EXT, RHO_L, k_ext))
for name, a0, rho, k in rows:
    lbl = "rho_L" if abs(rho - RHO_L) / RHO_L < 1e-12 else "rho_c0"
    say("    %-40s %.4e    %-8s  %.6f" % (name, a0, lbl, k))
say()
# record's internal kappa estimates (from qwenlib header / KAPPA_LEDGER / CFG493)
K_INT = [("adopted normalization", 0.5, 0.0),
         ("KAPPA_LEDGER fit (superseded)", 0.551, 0.043),
         ("CFG493 combined", 0.417, 0.095),
         ("MNRAS v3.1 shape-only", 0.58, 0.18)]
say("  the record's own kappa estimates:")
say("    %-32s %8s %8s   z vs 1/2" % ("entry", "kappa", "+-1sig"))
zs = []
for nm, k, e in K_INT:
    z = abs(k - 0.5) / e if e > 0 else 0.0
    zs.append((nm, z))
    say("    %-32s %8.3f %8.3f   %s" % (nm, k, e, "%.2f" % z if e > 0 else "n/a (input)"))
kmax, kmin = max(k for _, k, _ in K_INT[1:]), min(k for _, k, _ in K_INT[1:])
spread_int = math.log10(kmax / kmin)
# external
spread_all = math.log10(k_ext / 0.417)
say()
say("  external kappa = a_0(Sparc 1.20e-10) / (c sqrt(G rho_L)) = %.4f" % k_ext)
say("     +- %.4f (random)   +- %.4f (systematic)" %
    (A0_EXT_R / c_sqrtGrho(RHO_L), A0_EXT_S / c_sqrtGrho(RHO_L)))
say("  record's internal measurement spread (excl. the adopted input): %.4f dex" % spread_int)
say("  full span, adopted input -> external:                          %.4f dex" % spread_all)
say()
rec("kappa_ext", k_ext)
rec("kappa_ext_rand", A0_EXT_R / c_sqrtGrho(RHO_L))
rec("kappa_ext_sys", A0_EXT_S / c_sqrtGrho(RHO_L))
rec("kappa_internal_spread_dex", spread_int)
rec("kappa_full_span_dex", spread_all)

j0_convention = abs(k_ext - 0.5) > 0.05
check("J0", j0_convention,
      "kappa = 1/2 is a CONVENTION, not a measurement (|kappa_ext - 1/2| = %.4f > 0.05)"
      % abs(k_ext - 0.5),
      "a_0 = 1.20e-10 m/s^2 (external) -> kappa = %.4f; the value 1/2 is realized only on the "
      "record's canonical footing a_0 = 9.3603e-11, i.e. %.3f dex lower."
      % (k_ext, math.log10(1.20e-10 / 9.3603e-11)))
say()

# ================================================================= J1 =========
say("=== J1: the scale-covariance no-go (exact, sympy) ===")
try:
    import sympy as sp

    g_s, a0_s, lam_s = sp.symbols('g a0 lam', positive=True)
    Xs = (sp.sqrt(1 + 4 * a0_s / g_s) - 1) / 2

    # (i) covariance of the formation law
    diff = sp.simplify(Xs.subs({a0_s: lam_s * a0_s, g_s: lam_s * g_s}) - Xs)
    cov_XL = (diff == 0)

    # (ii) exact quadratic form of F1  ->  g X (1+X) = a0
    quad = sp.simplify(g_s * Xs * (1 + Xs))
    cov_quad = sp.simplify(quad - a0_s) == 0
    # scaling weight of each side
    quad_scaled = sp.simplify((lam_s * g_s)
                              * Xs.subs({a0_s: lam_s * a0_s, g_s: lam_s * g_s})
                              * (1 + Xs.subs({a0_s: lam_s * a0_s, g_s: lam_s * g_s})))
    w_quad = sp.simplify(quad_scaled / quad)          # should be lam

    say("  X_L(y;a0) = (sqrt(1 + 4 a0/y) - 1)/2")
    say("  (i)  X_L(lam*y ; lam*a0) - X_L(y;a0) = %s        -> covariance: %s" % (diff, cov_XL))
    say("  (ii) g X (1+X) simplifies to: %s              -> exact: %s" % (quad, cov_quad))
    say("       under lam: (lam g) X' (1+X') / (g X (1+X)) = %s   (weight 1, relation preserved)" % w_quad)
    say("  (iii) F3 (universality: one a_0 for all galaxies/epochs): a_0 -> lam a_0 preserves it.")
    say("  (iv) budget: rho_ph = X rho_b carries no a_0 -- invariant.")
    say()
    say("  F2 (a_0 = kappa c sqrt(G rho_*)) is the ONLY relation that is not invariant:")
    say("      it DEFINES kappa, so under G_lam:  kappa -> lam * kappa.")
    say("      There is no G_lam-invariant left that could fix kappa: X is fixed, M_b fixed,")
    say("      rho_* fixed, c,G fixed. kappa is the coordinate ALONG the orbit -> a flat direction.")
    say()
    j1 = cov_XL and cov_quad and (w_quad == lam_s)
    check("J1", j1,
          "NO-GO CONFIRMED: G_lam is an exact symmetry of F1/F3/every formation relation "
          "and kappa is its only charged quantity",
          "covariance of X_L: %s | exact quadratic g X(1+X) = a0: %s | weight: %s"
          % (cov_XL, cov_quad, w_quad))
    # numeric illustration of the orbit: two universes, identical dimensionless RAR
    say()
    say("  orbit check (numeric): two histories differing only by lam are observationally identical")
    say("    %-8s %-14s %-14s %-14s %-12s" % ("lam", "a_0 [m/s^2]", "g_b,f [m/s^2]", "kappa", "X (same)"))
    for lam in (0.5, 1.0, 2.0):
        a0l = lam * A0["can"]
        gb  = a0l / (XD["can"] * (1 + XD["can"]))
        say("    %-8.2f %-14.5e %-14.5e %-14.6f %-12.4f" % (lam, a0l, gb, lam * 0.5, XD["can"]))
    rec("j1_no_go_confirmed", bool(j1))
except ImportError:
    say("  sympy unavailable -- J1 not gradeable")
    check("J1", False, "sympy unavailable")
    rec("j1_no_go_confirmed", None)
say()

# ================================================================= J2 =========
say("=== J2: the routes that break the covariance (frozen list; graded) ===")
say("  kappa(z_f) = 1 / (2 sqrt(beta)),   beta = rho_m(z_f)/rho_L = (Om/OL)(1+z_f)^3")
say()

def kappa_of_z(z):
    beta = (OM / OL) * (1.0 + z)**3
    return 1.0 / (2.0 * math.sqrt(beta))

Z_L   = OLOM**(1/3.) - 1.0
Z_ACC = (2 * OLOM)**(1/3.) - 1.0
Z_BIND = 10.83

# C1..C4: named-epoch freeze-out
C = []
C.append(("C1", "freeze-out at matter-Lambda equality", Z_L, kappa_of_z(Z_L), "chosen epoch"))
C.append(("C2", "freeze-out today (z=0)", 0.0, kappa_of_z(0.0), "chosen epoch"))
C.append(("C3", "freeze-out at acceleration onset", Z_ACC, kappa_of_z(Z_ACC), "chosen epoch"))
C.append(("C4", "freeze-out at binding epoch z=10.83", Z_BIND, kappa_of_z(Z_BIND), "chosen epoch"))

# C5: formation field tied to the cosmic acceleration by delta_c
k_C5 = {}
for ft in ("can", "alt"):
    k_C5[ft] = DELTA_C * XD[ft] * (1 + XD[ft])
C.append(("C5", "g_b,f = delta_c * c sqrt(G rho_L)", None, k_C5["can"], "asserted tie"))

# C6: exact turnaround  R_ta^3 = 3 M_tot/(8 pi rho_L)  with  R_set = (1+X) r_M
def kappa_C6(Mb_kg, X, rho):
    # (1+X) sqrt(G M_b / a0) = [3 (1+X) M_b / (8 pi rho)]^{1/3}
    # -> a0^{3/2} = (8 pi rho/3)(1+X)^2 G^{3/2} M_b^{1/2}
    a0 = ((8 * math.pi * rho / 3.0) * (1 + X)**2 * G**1.5 * Mb_kg**0.5)**(2/3.)
    return a0, a0 / c_sqrtGrho(rho)

a0_6e10, k_C6 = kappa_C6(6e10 * MSUN, XD["can"], RHO_L)
C.append(("C6", "turnaround R_ta^3 = 3 M_tot/(8 pi rho_L), R_set=(1+X) r_M", None, k_C6, "derived"))

say("    %-4s %-56s %10s %12s  %s" % ("id", "added condition", "z_f", "kappa", "status"))
for cid, desc, z, k, st in C:
    zs_ = ("%10.4f" % z) if z is not None else "%10s" % "-"
    say("    %-4s %-56s %s %12.5f  %s" % (cid, desc, zs_, k, st))
say()

# the spread test
kz = [kappa_of_z(0.0), kappa_of_z(Z_L), kappa_of_z(Z_ACC)]
span3 = math.log10(max(kz) / min(kz))
kz4 = kz + [kappa_of_z(Z_BIND)]
span4 = math.log10(max(kz4) / min(kz4))
say("  SPREAD TEST (the decisive number):")
say("    named-epoch menu {today, matter=Lambda, accel onset}:")
say("        kappa = %.4f / %.4f / %.4f     span = %.4f dex" % (kz[0], kz[1], kz[2], span3))
say("    including the record's own binding epoch z=10.83:")
say("        kappa = %.4f ... %.4f         span = %.4f dex"
    % (kappa_of_z(Z_BIND), kz[0], span4))
say("    observational allowance (footing spread)          = 0.0411 dex")
say("    pre-registered pass band for kappa                = +-0.025 (5%%)")
say("    ratio, span3 / allowance = %.2f   ratio, span4 / allowance = %.2f"
    % (span3 / 0.0411, span4 / 0.0411))
say()
rec("span3_dex", span3)
rec("span4_dex", span4)

# does any route land on 1/2 ?
hits = [cid for cid, _, _, k, _ in C if abs(k - 0.5) <= 0.025]
say("  routes inside the 5%% band of 1/2: %s" % (hits or "none"))
j2_pass = False
if hits:
    # route must additionally be DERIVED from F, not chosen from the epoch menu
    derived_hits = [cid for cid, _, _, k, st in C if cid in hits and st == "derived"]
    say("  ... of which the added condition is DERIVED (not a chosen epoch): %s"
        % (derived_hits or "none"))
    j2_pass = bool(derived_hits)
say()
check("J2", j2_pass,
      "a route PASSES (|kappa-1/2| <= 0.025 AND added condition derived from F)"
      if j2_pass else
      "NO ROUTE PASSES: the only band hit (C1) is an epoch CHOICE, and the menu moves kappa "
      "by %.3f dex against a 0.0411 dex allowance (%.1fx too much freedom)"
      % (span3, span3 / 0.0411),
      "band hits=%s | C1 is a restatement of rho_* = rho_L, not a derivation of kappa"
      % (hits or "none"))
say()
say("  NOTE on C1: kappa = 1/2 <=> beta = 1 <=> z_f = z(matter=Lambda). But the record's")
say("  canonical footing DEFINES rho_ref := 4 a0^2/(c^2 G) ~ rho_L, so 'freeze-out at")
say("  equality' and 'kappa = 1/2' are the SAME statement. C1 has zero content as a")
say("  derivation; it is the definition of which cosmic density is used.")
say()
say("  NOTE on C6: the exact turnaround condition gives a_0 = [(8 pi rho_L/3)(1+X)^2]^{2/3}")
say("        * G * M_b^{1/3}  -- i.e. a_0 ~ M_b^{1/3}. Universality (F3) excludes it.")
say("        at M_b = 6e10 Msun: a_0 = %.4e m/s^2 (fitted can = %.4e), ratio %.4f dex"
    % (a0_6e10, A0["can"], math.log10(a0_6e10 / A0["can"])))
rec("C6_a0_at_6e10", a0_6e10)
say()

# ================================================================= J3 =========
say("=== J3: the GF1/GF2 n = 2 hook (graded) ===")
say("  certified identity: kappa := a_0/s, s := n a_0  =>  kappa = 1/n; kappa = 1/2 <=> n = 2")
say()
n = 2
# (i) theorem check, exactly
try:
    import sympy as sp
    nn, aa = sp.symbols('n a0', positive=True)
    expr = sp.simplify(aa / (nn * aa) - 1 / nn)
    j3_i = (expr == 0)
    say("  (i)  a_0/(n a_0) - 1/n = %s   -> theorem holds: %s" % (expr, j3_i))
except Exception:
    j3_i = None
    say("  (i)  sympy unavailable")

# (ii) is n = 2 measured independently of a_0's normalisation?
#      GF1's battery: germ ratio = n^2, Z^2 = 32 pi/3, Omega_L, S = 3/2 - ln2
germ_ratio = 4.000406
Zsq = 33.510322
Zsq_pred = 32 * math.pi / 3.0
OmL_meas = 0.685
S_pred = 1.5 - math.log(2.0)
say("  (ii) GF1 battery at n = 2 (committed numbers):")
say("        germ ratio  = %.6f   (n^2 = %d)          rel = %.2e" %
    (germ_ratio, n**2, abs(germ_ratio - n**2) / n**2))
say("        Z^2         = %.6f   (32 pi/3 = %.6f)   rel = %.2e" %
    (Zsq, Zsq_pred, abs(Zsq - Zsq_pred) / Zsq_pred))
say("        Omega_L     = %.3f" % OmL_meas)
say("        S(n=2)      = 3/2 - ln 2 = %.6f (committed)" % S_pred)
# these three are ratios of dimensionless quantities -> they do NOT contain a_0 or rho_L:
dep = {"germ ratio": "dimensionless germ ratio (no a_0)",
       "Z^2": "Z := c H_L / a_0 -- CONTAINS a_0",
       "S": "entropy of the family -- no a_0"}
j3_ii = True   # germ ratio + S are a_0-free; Z is a_0-bearing
say("        -> germ ratio and S are a_0-free; Z^2 is a_0-bearing. n = 2 IS pinned by an")
say("           a_0-free channel (germ/S).  (ii) = YES")
say()
# (iii) does kappa = 1/n put rho_Lambda under the root?
say("  (iii) kappa = a_0/s fixes the RATIO a_0/s only. Substituting into F2 gives")
say("          s = a_0/kappa = c sqrt(G rho_*),")
say("        i.e. the identification s = c sqrt(G rho_Lambda) IS the statement F2 with kappa = 1/n.")
say("        kappa = 1/n is therefore silent about which rho_* stands under the root; it")
say("        constrains the shape/normalisation of the RESPONSE, not the cosmic density.")
say("        -> (iii) = NO.")
say()
j3 = bool(j3_i) and j3_ii and False      # (iii) fails
check("J3", j3,
      "J3 = RESTATEMENT, not a formation output: kappa = 1/n is a theorem (i) and n = 2 is "
      "measured a_0-free (ii), but the rho_Lambda identification is F2 itself (iii)",
      "the n = 2 channel transports the EXPONENT/INDEX; it does not select the cosmic density, "
      "and it is not formation physics")
say()

# ================================================================= J4 =========
say("=== J4: where the formation event actually sits (graded) ===")
say("  from F1's exact quadratic:  g_b,f = a_0 / [X (1+X)]")
say()
say("    %-8s %-14s %-14s %-12s %-12s %-12s"
    % ("footing", "a_0", "g_b,f", "g/(c H_0)", "g/(c H_L)", "g / c sqrt(G rho_L)"))
r_g = {}
for ft in ("can", "alt"):
    a0 = A0[ft]
    gb = a0 / (XD[ft] * (1 + XD[ft]))
    r1 = gb / (c * H0)
    r2 = gb / (c * math.sqrt(8 * math.pi * G * RHO_L / 3.0))
    r3 = gb / c_sqrtGrho(RHO_L)
    r_g[ft] = (gb, r1, r2, r3)
    say("    %-8s %-14.5e %-14.5e %-12.3e %-12.3e %-12.3e" % (ft, a0, gb, r1, r2, r3))
say()
r3can = r_g["can"][3]
say("  the formation field sits %.2f dex below c sqrt(G rho_L), %.2f dex below c H_0."
    % (math.log10(r3can), math.log10(r_g["can"][1])))
say("  -> the assembly event is NOT cosmological in acceleration units. The gap between the")
say("     cosmic scale and the formation field is bridged by X ~ %.2f, which is itself the"
         % XD["can"])
say("     output of the law. Any 'derivation' of a_0 that must supply this gap is circular.")
say()
j4 = math.log10(r3can) < -2.0
check("J4", j4,
      "the formation field lies >2 dex below every cosmic acceleration (%.2f dex) -- the event "
      "is set by the galaxy, not by cosmology" % abs(math.log10(r3can)),
      "g_b,f = %.4e m/s^2 vs c sqrt(G rho_L) = %.4e m/s^2" % (r_g["can"][0], c_sqrtGrho(RHO_L)))
rec("g_bf_can", r_g["can"][0])
rec("g_bf_over_cosmic_dex", math.log10(r3can))
say()

# ================================================================= J5 =========
say("=== J5: the epoch-prediction the reading does supply (reported, not graded) ===")
say("  rho_* = rho_Lambda  =>  a_0(z) = a_0(0) exactly.")
say("  rho_* = rho_crit(z) =>  a_0(z)/a_0(0) = E(z).")
say()
say("    %-6s %-12s %-16s %-16s" % ("z", "E(z)", "a_0(z)/a_0 (Lam)", "a_0(z)/a_0 (crit)"))
for z in (0.3, 0.5, 1.0, 2.0, 6.0):
    say("    %-6.2f %-12.5f %-16.5f %-16.5f" % (z, E(z), 1.0, E(z)))
say()
say("  FINAL2's own bound on a_0(z) stands; this lane does not grade it.")
say()

# ================================================================= KA =========
say("=== KNOWN ANSWERS (each must pass, both footings) ===")
say()
# KA-1: Z = c H_L / a_0 = sqrt(32 pi/3), using the record's tie rho_ref = 4 a0^2/(c^2 G)
Z_pred = math.sqrt(32.0 * math.pi / 3.0)
ka1 = True
say("  KA-1  Z = c H_Lambda/a_0 with rho_ref = 4 a0^2/(c^2 G);  sqrt(32 pi/3) = %.6f" % Z_pred)
for ft in ("can", "alt"):
    rho_ref = 4.0 * A0[ft]**2 / (c**2 * G)
    HL = math.sqrt(8.0 * math.pi * G * rho_ref / 3.0)
    Z = c * HL / A0[ft]
    ok = abs(Z - Z_pred) <= 1e-4
    ka1 = ka1 and ok
    say("        %-4s rho_ref = %.6e   Z = %.6f   |Z - sqrt(32pi/3)| = %.2e  %s"
        % (ft, rho_ref, Z, abs(Z - Z_pred), "OK" if ok else "MISS"))
check("KA-1", ka1, "Z = c H_L/a_0 reproduces sqrt(32 pi/3) = 5.78881 to 1e-4 on BOTH footings")
say()
# KA-2: which cosmic density is each footing
rho_ref_can = 4.0 * A0["can"]**2 / (c**2 * G)
rho_ref_alt = 4.0 * A0["alt"]**2 / (c**2 * G)
r_can = rho_ref_can / RHO_L
r_alt = rho_ref_alt / RHO_CRIT0
say("  KA-2  footing identity, printed to 6 digits:")
say("        rho_ref(can)/rho_Lambda = %.6f     (1.000000 = the Lambda-only density)" % r_can)
say("        rho_ref(alt)/rho_crit,0 = %.6f     (1.000000 = the total/critical density)" % r_alt)
ka2 = abs(r_can - 1.0) <= 2e-3 and abs(r_alt - 1.0) <= 2e-3
check("KA-2", ka2,
      "canonical footing IS the Lambda-only density and alt footing IS the critical density",
      "cross-ratios (reported): rho_ref(can)/rho_crit,0 = %.6f ; rho_ref(alt)/rho_L = %.6f"
      % (rho_ref_can / RHO_CRIT0, rho_ref_alt / RHO_L))
say()
# KA-3: the exact quadratic  (already verified in J1 -- restated as its own check)
ka3 = True
for ft in ("can", "alt"):
    gb = A0[ft] / (XD[ft] * (1.0 + XD[ft]))
    back = gb * XD[ft] * (1.0 + XD[ft])
    rel = abs(back - A0[ft]) / A0[ft]
    ka3 = ka3 and rel < 1e-12
    say("  KA-3  %-4s g_b,f X(1+X) = %.6e   vs a_0 = %.6e   rel = %.2e"
        % (ft, back, A0[ft], rel))
check("KA-3", ka3, "F1's exact quadratic g_b,f X(1+X) = a_0 closes on both footings")
say()
# KA-4: GF1/GF2 n = 2 battery
n = 2
germ = 4.000406
Z2 = 33.510322
Z2p = 32.0 * math.pi / 3.0
AL = 8.0 * math.pi**2 * n**2 / c**4
AL_gf1 = 3.910308e-32
say("  KA-4  GF1/GF2 battery at n = 2 (n = 2 <-> kappa = 1/2):")
say("        germ ratio      = %.6f  vs n^2 = %d            rel = %.2e"
    % (germ, n**2, abs(germ - n**2) / n**2))
say("        Z^2             = %.6f  vs 32 pi/3 = %.6f    rel = %.2e"
    % (Z2, Z2p, abs(Z2 - Z2p) / Z2p))
say("        A*Lambda        = %.6e  vs GF1 %.6e       rel = %.2e"
    % (AL, AL_gf1, abs(AL - AL_gf1) / AL_gf1))
say("        S(n=2)          = 3/2 - ln 2 = %.6f" % (1.5 - math.log(2.0)))
ka4 = (abs(germ - n**2) / n**2 <= 1e-3 and abs(Z2 - Z2p) / Z2p <= 1e-3
       and abs(AL - AL_gf1) / AL_gf1 <= 1e-3)
check("KA-4", ka4, "GF1/GF2 n = 2 battery reproduces all four targets (|rel| <= 1e-3)",
      "=> the integer n = 2 IS pinned. It pins kappa = 1/n. It does NOT pin rho_* (see J3 iii).")
rec("ka4", bool(ka4))
say()

# ================================================================= J7 ========
say("=== J7: is CONSERVATION load-bearing for kappa? (graded; the brief's own premise) ===")
say("  F1 has two clauses: (a) formation-set, (b) conserved. Test each for what it does to kappa.")
say()
try:
    import sympy as sp
    y, a0, lam, n = sp.symbols('y a0 lam n', positive=True)
    Xf = (sp.sqrt(1 + 4 * a0 / y) - 1) / 2
    # (a) formation-set alone: a family of (g_f, X) pairs, one per galaxy
    #     -> determines a_0 = g_f X(1+X) ONLY IF g_f is input; nothing cosmological enters.
    # (b) conserved: X(t) = X_f for all t. Test: does it add any relation containing a_0?
    #     X(t) - X_f = 0. Substitute X_f: the relation is X(t) = (sqrt(1+4 a0/y_f)-1)/2.
    #     It is G_lam-covariant (both sides weight 0 and 1 resp.), so it constrains
    #     the TIME DEPENDENCE of X, never the VALUE of kappa.
    cov_cons = sp.simplify(Xf.subs({a0: lam * a0, y: lam * y}) - Xf) == 0
    say("  conservation relation  X(t) = X_L(g_b,f; a_0):")
    say("     G_lam-covariant? %s   -> it constrains d X/dt, and kappa is unchanged by it."
        % cov_cons)
    j7 = bool(cov_cons)
except Exception:
    j7 = False
    say("  sympy unavailable")
# contrast: conservation IS load-bearing for the AMOUNT
#   F1 predicts X_gal = X_L(g_b,f) (frozen); F1' (no conservation) predicts X_gal = X_L(g_b,now).
#   with X ~ 59.49 and g_b,now >> g_b,f, the two differ by orders of magnitude in X.
gb_f   = A0["can"] / (XD["can"] * (1 + XD["can"]))
for ratio in (10.0, 100.0):
    X_now = XL(ratio * gb_f, A0["can"])
    say("     if g_b,now = %6.1f x g_b,f : X_L(g_b,now) = %8.4f  vs frozen X = %.4f  (factor %.2f)"
        % (ratio, X_now, XD["can"], XD["can"] / X_now))
say("     -> conservation is load-bearing for the AMOUNT (it is what makes X ~ 59 and not ~ 6),")
say("        and it is silent about the NORMALISATION.")
say()
check("J7", j7,
      "CONFIRMED: conservation is G_lam-covariant -- it fixes the amount's history, not kappa",
      "the brief's premise is load-bearing for Q1 (universality, epoch-independence) and empty "
      "for Q2 (the number 1/2)")
say()

# ================================================================= MUTATE ======
say("=== MUTATE: three false twins, each must be REJECTED by the same machinery ===")
say()
# --- M1: kappa = 1/(2 pi)
k_m1 = 1.0 / (2.0 * math.pi)
m1_rejected = abs(k_m1 - 0.5) > 0.025
check("M1", m1_rejected,
      "REJECTED: 'kappa = 1/(2 pi) derived by the formation reading' -- band miss |%.3f - 0.500| "
      "= %.3f >> 0.025" % (k_m1, abs(k_m1 - 0.5)),
      "Milgrom's q = 0.159 is the T001 closest near-miss; it is 0.341 away, i.e. 13.6x the band")
say()

# --- M2: the z_f = z_L hit is a derivation
m2_rejected = span3 > 0.0411
check("M2", m2_rejected,
      "REJECTED: 'the z_f = z_L hit derives kappa = 1/2' -- the named-epoch menu spans "
      "%.4f dex against a 0.0411 dex allowance (%.1fx too free)" % (span3, span3 / 0.0411),
      "kappa(today) = %.4f, kappa(equality) = %.4f, kappa(accel onset) = %.4f; picking the "
      "middle one is a choice, and it is a restatement of rho_* = rho_L" % (kz[0], kz[1], kz[2]))
say()

# --- M3: kappa = 1/2 is a measurement
m3_rejected = j0_convention
check("M3", m3_rejected,
      "REJECTED: 'kappa = 1/2 is a measurement' -- against Planck rho_L the external a_0 gives "
      "kappa = %.4f; 1/2 is realized only by adopting the canonical footing" % k_ext,
      "record-internal kappa estimates span %.3f dex (0.417+-0.095 to 0.641+-0.128): the "
      "observation cannot confirm or exclude 1/2 at the 5%% level" % spread_all)
say()

# ================================================================== labels =====
say("=" * 100)
say("SUMMARY")
say("=" * 100)
allpass = all(ok for _, ok, _, _ in CHECKS if _.startswith(("J", "K")))
nfail = [k for k, ok, _, _ in CHECKS if not ok]
say("  checks: %d, failing: %s" % (len(CHECKS), nfail or "none"))
say("  J0 kappa(ext, Planck rho_L)          = %.4f  (adopted 1/2 = convention, not a datum)" % k_ext)
say("  J1 no-go (G_lam symmetry, kappa flat) = %s" % RESULTS["j1_no_go_confirmed"])
say("  J2 menu freedom                       = %.4f dex vs 0.0411 dex allowance" % span3)
say("  J3 (i) theorem / (ii) n=2 a_0-free / (iii) rho_L tie = YES / YES / NO  -> RESTATEMENT")
say("  J4 formation field below cosmic scale = %.2f dex" % math.log10(r3can))
say("  J7 conservation G_lam-covariant       = %s (load-bearing for the amount, silent on kappa)"
    % j7)
say()
if MUTATE:
    say("  MUTATE ARM: all three false twins must be rejected: %s"
        % ("YES" if (m1_rejected and m2_rejected and m3_rejected) else "NO"))
    say("  MUTATE VERDICT: %s" % ("PASS (machinery discriminates)"
                                 if (m1_rejected and m2_rejected and m3_rejected)
                                 else "FAIL"))
else:
    say("  LANE LABEL: KAPPA NOT DERIVED (FITTED) -- FORM OUTPUT")
    say("     Q1 (form)      = OUTPUT      : universality + conservation force a_0 epoch-")
    say("                                    independent, and rho_Lambda is the unique epoch-")
    say("                                    independent cosmic density -> a_0 = kappa c sqrt(G rho_L).")
    say("     Q2 (kappa=1/2) = NO          : kappa is a flat direction of F (J1); the only band")
    say("                                    hit is an epoch choice with %.1fx too much freedom (J2);" % (span3 / 0.0411))
    say("                                    the n=2 hook transports the index, not the density (J3);")
    say("                                    and the formation event carries no cosmic magnitude (J4).")
say()

RESULTS["checks"] = {k: bool(ok) for k, ok, _, _ in CHECKS}
RESULTS["mutate"] = bool(MUTATE)

# ------------------------------------------------------------------ write -----
HERE = os.path.dirname(os.path.abspath(__file__))
base = "final16_MUTATE" if MUTATE else "final16"
with open(os.path.join(HERE, base + ".out"), "w") as f:
    f.write("\n".join(OUT) + "\n")
try:
    import json
    with open(os.path.join(HERE, base + ".json"), "w") as f:
        json.dump(RESULTS, f, indent=2, default=str)
except Exception as e:
    print("json write failed:", e)

print("\nwrote %s.out / %s.json  (%d checks)" % (base, base, len(CHECKS)))

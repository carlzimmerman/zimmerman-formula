# -*- coding: utf-8 -*-
"""CFG46 -- does the Unruh / de Sitter matching, with a mode count n, give kappa = 1/2?  (A pasted 'Bohr postulate' route.)

The route under test (third-party text, not a framework result): read the integer 2 in kappa = 1/2 as the two graviton
helicities, and 'derive' a0 = c sqrt(G rho_L)/n by matching an Unruh temperature to the de Sitter horizon temperature or by
matching thermal energy density over n modes to rho_L.  Nobody had written the algebra; this script does.

Frozen pass/fail before running (load-bearing checks assert the negative; MUTATE controls must make them fail):
  U1  T_Unruh(a) = T_dS gives a = c H_L = c sqrt(8 pi/3) sqrt(G rho_L)  (symbolic), so kappa_match = sqrt(8 pi/3) = 2.894 / n
  U2  n = 2 gives kappa = 1.447: excluded against the measured 0.465 +- 0.076 (BTFR) and 0.55 +- 0.17 (a0 ties), and the
      program's footings kappa = 0.500 / 0.604 are 2.9x / 2.4x below it
  U3  the n that the footing needs is Z = 2 sqrt(8 pi/3) = 5.789, not 2 and not an integer
  U4  energy-density matching over n modes has the wrong form: a0 ~ (rho c^9 / hbar)^(1/4), not sqrt(G rho); ln-slope 1/4 vs 1/2
  U5  DISCLOSURE (reported, not a pass): a fit to the measured kappa band cannot pick n; every integer 5..9 is inside 2 sigma
kappa = 1/2 stays FITTED.  Nothing here supports or excludes the framework; it retires one derivation route.
"""
import os, sys, math, json
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = int(os.environ.get("MUTATE", "0"))
tag = "" if MUTATE == 0 else "_MUTATE%d" % MUTATE
OUT = open(os.path.join(HERE, "CFG46_unruh_matching" + tag + ".out"), "w", encoding="utf-8")
res = []; fail = 0

def P(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.write(s + "\n")

def check(tag_, statement, measured, ok, load=True):
    global fail
    ok = bool(ok); res.append((tag_, ok, load))
    if not ok and load: fail += 1
    P("  [%s] %s %s" % ("PASS" if ok else ("FAIL" if load else "FAIL(reported)"), tag_, statement)); P("         measured: " + str(measured))

# --- constants (same as the program: campaign_fresh_gravity/CFG43_fluid_tie/A_common.py)
G = 6.6743e-11; C = 299792458.0; RHO_L = 5.8424e-27; HBAR = 1.054571817e-34
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
KMEAS = [("BTFR", 0.465, 0.076), ("a0 ties", 0.55, 0.17)]
Z = 2 * math.sqrt(8 * math.pi / 3)
SQ = math.sqrt(8 * math.pi / 3)

# MUTATE 1: insert the missing factor 1/(Z/2) into the matching (what a successful route would have to contain)
# MUTATE 2: replace the measured kappa band by the n=2 matching value (a comparison that would let n=2 pass)
fac = (2.0 / Z) if MUTATE == 1 else 1.0
kmeas = KMEAS if MUTATE != 2 else [("BTFR", SQ / 2, 0.076), ("a0 ties", SQ / 2, 0.17)]

P("CFG46 -- Unruh / de Sitter matching with a mode count n (MUTATE=%d)" % MUTATE)
P("constants: G=%.4e c=%.1f rho_L=%.4e kg/m3 hbar=%.6e ; sqrt(8pi/3)=%.6f  Z=%.6f" % (G, C, RHO_L, HBAR, SQ, Z))

# ---------------- U1 symbolic
P("\n== U1: T_Unruh = T_dS ==")
a, c, hb, k, Gs, rho, n = sp.symbols("a c hbar k G rho n", positive=True)
HL = sp.sqrt(8 * sp.pi * Gs * rho / 3)            # de Sitter Hubble rate from rho_Lambda (Friedmann, c-consistent units)
TU = hb * a / (2 * sp.pi * c * k)
TdS = hb * HL / (2 * sp.pi * k)
sol = sp.solve(sp.Eq(TU, TdS), a)[0]
kappa_sym = sp.simplify(sol / (c * sp.sqrt(Gs * rho)))
P("  a = %s ; a/(c sqrt(G rho)) = %s = %.6f" % (sp.simplify(sol), kappa_sym, float(kappa_sym)))
check("U1", "matching gives a = c H_L (hbar and k cancel), kappa_match = sqrt(8 pi/3)",
      "kappa_match = %.6f" % float(kappa_sym), abs(float(kappa_sym) - SQ) < 1e-12)

# ---------------- U2 n = 2 vs measurement and footings
P("\n== U2: divide by n = 2 (two helicities) ==")
k2 = SQ / 2 * fac
P("  kappa(n=2) = %.4f  ->  a0 = %.4e m/s^2" % (k2, k2 * C * math.sqrt(G * RHO_L)))
for nm, kk, sg in kmeas:
    z = abs(k2 - kk) / sg
    check("U2", "n=2 kappa %.3f vs %s measured %.3f +- %.3f is excluded (> 3 sigma)" % (k2, nm, kk, sg), "%.1f sigma" % z, z > 3)
for fn, a0 in A0.items():
    kf = a0 / (C * math.sqrt(G * RHO_L))
    check("U2", "footing %s: kappa = %.3f, n=2 matching is %.2fx above it" % (fn, kf, k2 / kf), "ratio %.2f" % (k2 / kf), k2 / kf > 2.0)

# ---------------- U3 required n
P("\n== U3: what n would the footing need? ==")
for fn, a0 in A0.items():
    kf = a0 / (C * math.sqrt(G * RHO_L))
    nreq = SQ * fac / kf
    P("  footing %s: n_required = %.4f" % (fn, nreq))
nreq_can = SQ * fac / (A0["canonical"] / (C * math.sqrt(G * RHO_L)))
check("U3", "n_required (canonical) = Z = 5.789 to 0.3%, so not 2 and not an integer", "n_req = %.4f vs Z = %.4f" % (nreq_can, Z),
      abs(nreq_can - Z) / Z < 3e-3 and abs(nreq_can - round(nreq_can)) > 0.1)

# ---------------- U4 energy matching
P("\n== U4: thermal energy density over n modes = rho_L c^2 ==")
# u = n (pi^2/30) (kT)^4/(hbar c)^3 with kT = hbar a/(2 pi c)  ->  a^4 = 30 (2pi)^4 rho c^9/(n pi^2 hbar)
def a_energy(rho_, n_): return (30 * (2 * math.pi) ** 4 * rho_ * C ** 9 / (n_ * math.pi ** 2 * HBAR)) ** 0.25
ae2 = a_energy(RHO_L, 2)
slope = math.log(a_energy(2 * RHO_L, 2) / a_energy(RHO_L, 2)) / math.log(2)
P("  n=2: a = %.4e m/s^2 ; measured a0 = %.4e ; ratio %.3e ; d ln a/d ln rho = %.3f" % (ae2, A0["canonical"], ae2 / A0["canonical"], slope))
check("U4", "energy matching scales as rho^(1/4) with hbar in the answer (exponent 1/4, not 1/2; not in the (c,G,rho) family)",
      "exponent %.3f" % slope, abs(slope - 0.25) < 1e-9 and abs(slope - 0.5) > 0.2)
check("U4", "and misses the measured a0 by orders of magnitude", "ratio %.2e" % (ae2 / A0["canonical"]), abs(math.log10(ae2 / A0["canonical"])) > 3)

# ---------------- U5 disclosure
P("\n== U5: DISCLOSURE, the measured band cannot choose n ==")
lo, hi = 0.465 - 2 * 0.076, 0.465 + 2 * 0.076
ints = [m for m in range(1, 30) if lo <= SQ / m <= hi]
P("  integers n with sqrt(8pi/3)/n inside the BTFR 2-sigma band [%.3f, %.3f]: %s" % (lo, hi, ints))
P("  n = 6 gives kappa = %.4f (%.2f sigma from 0.465): the closest integer, but with no mechanism; picking it post hoc would be numerology" % (SQ / 6, abs(SQ / 6 - 0.465) / 0.076))
check("U5", "several integers fit the band, so a fit cannot select the mode count (reported)", "n in %s" % ints, len(ints) >= 3, load=False)

P("\nRESULT: the Unruh/de Sitter matching lands at a = c H_L (kappa = 2.894/n). The footing needs n = Z = 5.79; n = 2 is off by 2.9x.")
P("The energy-matching variant has the wrong functional form. kappa = 1/2 stays FITTED; this route is retired as stated.")
npass = sum(1 for r in res if r[1])
P("\nSUMMARY CFG46 (MUTATE=%d): %d/%d checks pass; load-bearing failures = %d" % (MUTATE, npass, len(res), fail))
for t_, ok, lb in res:
    if not ok: P("   failed: %s %s" % (t_, "(load-bearing)" if lb else "(reported)"))
json.dump({"mutate": MUTATE, "kappa_match_over_n": SQ, "Z": Z, "n_required_canonical": nreq_can,
           "energy_matching_exponent": slope, "integers_in_2sigma": ints,
           "checks": [{"id": t_, "ok": ok, "load_bearing": lb} for t_, ok, lb in res]},
          open(os.path.join(HERE, "CFG46_unruh_matching_results%s.json" % tag), "w"), indent=1)
OUT.close(); sys.exit(1 if fail else 0)

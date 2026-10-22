#!/usr/bin/env python3
"""D5_kappa_four: horizon-thermodynamic class no-go for kappa (Angle T) and an audit of the
record's "data select R = 4 among the natural caps" (Angle A).

Criteria: FROZEN_CRITERIA.md (committed alone first).  kappa = 1/2 is FITTED; Z/4pi is a POSTULATE.
Run:    OMP_NUM_THREADS=1 nice -n 10 python3 d5_kappa_four.py
Mutate: D5_MUTATE=1 ... (Friedmann 8pi/3 -> 1; must break K2 and K3)
stdlib + sympy, deterministic, no network.
"""
import bisect
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

import sympy as sp

MUTATE = os.environ.get("D5_MUTATE", "0") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
TAG = "_MUTATE" if MUTATE else ""
OUT_TXT = os.path.join(HERE, "d5_kappa_four%s.out" % TAG)
OUT_JSON = os.path.join(HERE, "d5_kappa_four_results%s.json" % ("_MUTATE" if MUTATE else ""))

lines = []
results = {"mutate": MUTATE, "checks": {}}
npass = 0
nchk = 0


def say(s=""):
    print(s)
    lines.append(s)


def check(name, ok, value, threshold, note=""):
    global npass, nchk
    nchk += 1
    npass += int(bool(ok))
    say("%-4s %s %s   %s%s" % (name, "PASS" if ok else "FAIL", value, threshold,
                               ("   [" + note + "]") if note else ""))
    results["checks"][name] = {"pass": bool(ok), "value": str(value), "threshold": threshold}


# ---------------------------------------------------------------------------
# External inputs (labelled; not fitted)
# ---------------------------------------------------------------------------
C = 299792458.0                     # m/s (exact)
G = 6.67430e-11                     # CODATA 2018
HBAR = 1.054571817e-34              # CODATA 2018 (exact in SI 2019)
KB = 1.380649e-23                   # exact SI 2019
MPC = 3.0856775814913673e22         # m
H0 = 67.4e3 / MPC                   # Planck 2018 TT,TE,EE+lowE+lensing
OMEGA_L = 0.6847                    # Planck 2018
OMEGA_M = 0.3153                    # Planck 2018
A0_CAN = 9.3603e-11                 # canonical footing (record)
A0_ALT = 1.1312e-10                 # alt footing (record)
# measured kappa bands (quoted, not refitted)
KAP_CFG493 = (0.417, 0.095)         # campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined.out
A81_KP3 = (0.37808124619485783, 0.12081732631600586)  # A81 a81_results.json joint.kappa / sigma_kappa_tot
A81_KP3_HALF = 0.41345344393466854  # A81 constants.kappa_p3_half (kappa_P3 equivalent of kappa = 1/2)
conv = 0.5 / A81_KP3_HALF
KAP_A81 = (A81_KP3[0] * conv, A81_KP3[1] * conv)
BANDS = {"CFG493": KAP_CFG493, "A81_DE": KAP_A81}

RHO_L = OMEGA_L * 3 * H0**2 / (8 * math.pi * G)
H_L = math.sqrt(8 * math.pi * G * RHO_L / 3)          # H_Lambda (true Friedmann, both modes)
Zc = 2 * math.sqrt(8 * math.pi / 3)

say("=" * 78)
say("D5_kappa_four  (mutate=%s)" % MUTATE)
say("=" * 78)
say("inputs: H0 67.4, Omega_L %.4f -> rho_L %.6e kg/m^3, H_L %.6e 1/s; Z = %.6f" % (OMEGA_L, RHO_L, H_L, Zc))
say("bands: CFG493 kappa %.3f +- %.3f ; A81 joint kappa_P3 %.4f +- %.4f -> kappa_DE %.4f +- %.4f (x%.5f)"
    % (KAP_CFG493 + A81_KP3 + KAP_A81 + (conv,)))
results["inputs"] = {"rho_L": RHO_L, "H_L": H_L, "Z": Zc, "bands": BANDS, "a81_conv": conv}

# ---------------------------------------------------------------------------
# K0  convention chain (symbolic; independent of mutate)
# ---------------------------------------------------------------------------
say("\n-- K0 convention chain")
kap, c, Gs, rho, a0, H = sp.symbols("kappa c G rho a0 H", positive=True)
a0expr = kap * c * sp.sqrt(Gs * rho)
R_expr = sp.simplify(rho * c**2 / (a0expr**2 / Gs))           # = 1/kappa^2
Hsq = 8 * sp.pi * Gs * rho / 3
Lam = 3 * Hsq / c**2
Zs = 2 * sp.sqrt(8 * sp.pi / 3)
e1 = sp.simplify(R_expr - 1 / kap**2)
e2 = sp.simplify((Lam - 32 * sp.pi * a0expr**2 / c**4).subs(kap, sp.Rational(1, 2)))
e3 = sp.simplify((a0expr - c * sp.sqrt(Hsq) / Zs).subs(kap, sp.Rational(1, 2)))
e4 = sp.simplify((Gs * rho - 4 * a0expr**2 / c**2).subs(kap, sp.Rational(1, 2)))
ok0 = all(x == 0 for x in (e1, e2, e3, e4))
check("K0", ok0, "R=rho c^2/(a0^2/G) - 1/kappa^2 = %s; kappa=1/2: Lambda-32pi a0^2/c^4 = %s, a0-cH/Z = %s, G rho-4a0^2/c^2 = %s"
      % (e1, e2, e3, e4), "all exactly 0")

# ---------------------------------------------------------------------------
# Angle T: horizon blocks.  Each block X = q * pi^w * H^h c^cc G^g hbar^d kB^f  (exact coefficients)
# ---------------------------------------------------------------------------
# Friedmann: H^2 = Fq * pi^Fw * G rho   (normal: 8/3, w=1; mutate: 1, w=0)
Fq, Fw = (F(1), 0) if MUTATE else (F(8, 3), 1)
# u_L = rho c^2 = c^2 H^2 / (G * Fq pi^Fw)
uq, uw = 1 / Fq, -Fw
BLOCKS = [
    # name,   q,              w,        h,  cc, g,  d,  f
    ("r_H",   F(1),           0,       -1,  1,  0,  0,  0),
    ("A",     F(4),           1,       -2,  2,  0,  0,  0),
    ("V",     F(4, 3),        1,       -3,  3,  0,  0,  0),
    ("T_GH",  F(1, 2),       -1,        1,  0,  0,  1, -1),
    ("S_BH",  F(1),           1,       -2,  5, -1, -1,  1),
    ("E_MS",  F(1, 2),        0,       -1,  5, -1,  0,  0),
    ("u_L",   uq,             uw,       2,  2, -1,  0,  0),
    ("E_L",   uq * F(4, 3),   uw + 1,  -1,  5, -1,  0,  0),
    ("E_K",   2 * uq * F(4, 3), uw + 1, -1, 5, -1,  0,  0),
    ("g_s",   F(1),           0,        1,  1,  0,  0,  0),
]
SI = {"H": H_L, "c": C, "G": G, "hbar": HBAR, "kB": KB}


def block_si(b):
    _, q, w, h, cc, g, d, f = b
    return float(q) * math.pi**w * H_L**h * C**cc * G**g * HBAR**d * KB**f


def enumerate_class(D, maxblocks=3, emax=2):
    exps = [F(k, D) for k in range(-emax * D, emax * D + 1) if k != 0]
    out = []
    nb = len(BLOCKS)
    for nsel in range(1, maxblocks + 1):
        for idx in itertools.combinations(range(nb), nsel):
            for es in itertools.product(exps, repeat=nsel):
                h = sum(e * BLOCKS[i][3] for i, e in zip(idx, es))
                if h != 1:
                    continue          # an acceleration with c, G, hbar, kB free needs H^1 exactly
                out.append((idx, es))
    return out


def reduce_mono(idx, es):
    """return (q2, m) with a0 = q pi^m c H, q^2 rational, m in Z/D; and the SI check deviation."""
    q2 = F(1)
    m = F(0)
    cc = g = d = f = F(0)
    for i, e in zip(idx, es):
        b = BLOCKS[i]
        q2 *= b[1] ** int(2 * e) if (2 * e).denominator == 1 else None
        m += e * b[2]
        cc += e * b[4]
        g += e * b[5]
        d += e * b[6]
        f += e * b[7]
    # free multipliers c^a G^b hbar^d' kB^f' bring totals to c^1 G^0 hbar^0 kB^0
    val = 1.0
    for i, e in zip(idx, es):
        val *= block_si(BLOCKS[i]) ** float(e)
    val *= C ** float(1 - cc) * G ** float(-g) * HBAR ** float(-d) * KB ** float(-f)
    pred = math.sqrt(float(q2)) * math.pi ** float(m) * C * H_L
    # independent kappa check in SI with the mode's own Friedmann relation
    rho_mode = H_L**2 / (G * float(Fq) * math.pi**Fw)
    kap_si = val / (C * math.sqrt(G * rho_mode))
    kap_key = kval(kappa2_key(q2, m))
    return q2, m, max(abs(val / pred - 1.0), abs(kap_si / kap_key - 1.0))


def kappa2_key(q2, m):
    """kappa = q pi^m c H / (c sqrt(G rho)), G rho = H^2/(Fq pi^Fw)  =>  kappa^2 = q^2 Fq pi^(2m + Fw) = r pi^n."""
    r = q2 * Fq
    n = 2 * m + Fw
    assert n.denominator == 1
    return (r, int(n))


def kval(key):
    r, n = key
    return math.sqrt(float(r) * math.pi ** n)


def describe(idx, es):
    return " * ".join("%s^%s" % (BLOCKS[i][0], e) for i, e in zip(idx, es))


classes = {}
maxdev = 0.0
mden_ok = True
for D in (1, 2):
    monos = enumerate_class(D)
    S = {}
    for idx, es in monos:
        q2, m, dev = reduce_mono(idx, es)
        maxdev = max(maxdev, dev)
        if (m * D).denominator != 1:
            mden_ok = False
        key = kappa2_key(q2, m)
        cost = (len(idx), sum(abs(e) for e in es))
        if key not in S or cost < S[key][0]:
            S[key] = (cost, describe(idx, es), m)
    classes[D] = {"n_monomials": len(monos), "S": S}

say("\n-- Angle T: horizon-thermodynamic class H_D (<=3 blocks, |e|<=2)")
for D in (1, 2):
    say("     D=%d: %d admissible monomials -> %d distinct kappa" % (D, classes[D]["n_monomials"], len(classes[D]["S"])))
check("K1", maxdev < 1e-9 and mden_ok,
      "max |SI a0/(q pi^m cH) - 1|, |SI kappa/key kappa - 1| = %.2e over %d monomials; m in Z/D: %s"
      % (maxdev, classes[1]["n_monomials"] + classes[2]["n_monomials"], mden_ok),
      "< 1e-9 and True", "T1: every admissible monomial is q pi^m c H_L")

HALF = (F(1, 4), 0)
ZKEY = (F(2, 3), -1)          # (Z/4pi)^2 = 2/(3 pi)
S1, S2 = classes[1]["S"], classes[2]["S"]
odd_n_S1 = all(n % 2 != 0 for (_, n) in S1) if not MUTATE else all(n % 2 == 0 for (_, n) in S1)
check("K2", HALF not in S1, "1/2 in S_1: %s (S_1 pi-exponent parity as the mode predicts [odd; even under MUTATE]: %s)" % (HALF in S1, odd_n_S1),
      "1/2 not in S_1", "T2: kappa^2 = rational x pi^odd != 1/4 (pi transcendental)")
zin = ZKEY in S1
check("K3", zin, "Z/4pi in S_1: %s%s" % (zin, ("  via " + S1[ZKEY][1]) if zin else ""),
      "Z/4pi in S_1", "a0 = cH/2pi = c kB T_GH/hbar")

half_hits = [(k, v) for k, v in S2.items() if k == HALF]
# collect ALL S2 constructions hitting 1/2 (not only the cheapest) to test the parity statement on each
all_half = []
for idx, es in enumerate_class(2):
    q2, m, _ = reduce_mono(idx, es)
    if kappa2_key(q2, m) == HALF:
        sqrt_odd = any((e.denominator == 2) and (BLOCKS[i][2] % 2 != 0) for i, e in zip(idx, es))
        all_half.append((describe(idx, es), str(m), str(q2), sqrt_odd, (len(idx), sum(abs(e) for e in es))))
all_half.sort(key=lambda t: t[4])
if MUTATE:
    parity_ok = True
else:
    parity_ok = all(t[1] == "-1/2" and t[2] == "3/32" and t[3] for t in all_half)
check("K4", parity_ok, "%d S_2 constructions give exactly 1/2; all have m=-1/2, q^2=3/32 and a square root of a pi-odd block: %s"
      % (len(all_half), "n/a under MUTATE" if MUTATE else parity_ok), "True", "T3")
for t in all_half[:5]:
    say("     1/2 in S_2 via  %s   (m=%s, q^2=%s)" % (t[0], t[1], t[2]))

# LEE
def lee(S, band):
    vals = sorted(set(round(kval(k), 12) for k in S))
    vals = [v for v in vals if 0.1 <= v <= 10]
    k0, s = band
    lo, hi = k0 - 2 * s, k0 + 2 * s
    inband = [v for v in vals if lo <= v <= hi]
    f = s / k0
    N = 100000
    cover = 0
    for j in range(N):
        ks = 10 ** (-1 + 2 * (j + 0.5) / N)
        a, b = ks * (1 - 2 * f), ks * (1 + 2 * f)
        p = bisect.bisect_left(vals, a)
        if p < len(vals) and vals[p] <= b:
            cover += 1
    near_half = [v for v in vals if abs(v / 0.5 - 1) <= 0.01 and abs(v - 0.5) > 1e-12]
    return {"n_vals": len(vals), "n_inband": len(inband), "p_elem": len(inband) / len(vals),
            "P_cover": cover / N, "n_within_1pct_of_half": len(near_half), "band": [lo, hi]}

lee_res = {}
lee_ok = True
for D in (1, 2):
    for bname, band in BANDS.items():
        L = lee(classes[D]["S"], band)
        lee_res["S%d_%s" % (D, bname)] = L
        lee_ok &= all(math.isfinite(x) for x in (L["p_elem"], L["P_cover"])) and 0 <= L["P_cover"] <= 1
        say("     S_%d vs %-6s band [%.3f, %.3f]: %d of %d values in band (p_elem %.4f); P_cover %.4f; within 1%% of 1/2 (not 1/2): %d"
            % (D, bname, L["band"][0], L["band"][1], L["n_inband"], L["n_vals"], L["p_elem"], L["P_cover"],
               L["n_within_1pct_of_half"]))
# extra (reported, not graded): the minimal sub-class, one block or two blocks with |e| <= 1, D = 1
Smin = {k: v for k, v in S1.items() if v[0][0] <= 2 and v[0][1] <= 2}
Lmin = lee(Smin, KAP_CFG493)
lee_res["S1_minimal_CFG493"] = Lmin
say("     [extra] minimal S_1 (<=2 blocks, sum|e|<=2): %d values, %d in CFG493 band, P_cover %.4f; members in band: %s"
    % (Lmin["n_vals"], Lmin["n_inband"], Lmin["P_cover"],
       ", ".join("%.4f" % kval(k) for k in sorted(Smin, key=kval) if Lmin["band"][0] <= kval(k) <= Lmin["band"][1])))
check("K5", lee_ok, "P_cover(S_1, CFG493) %.4f ; P_cover(S_2, CFG493) %.4f"
      % (lee_res["S1_CFG493"]["P_cover"], lee_res["S2_CFG493"]["P_cover"]), "finite, in [0,1]")

# footings and nearest members
foot = {}
for fname, a in (("canonical", A0_CAN), ("alt", A0_ALT)):
    kf = a / (C * math.sqrt(G * RHO_L))
    row = {"kappa": kf}
    for D in (1, 2):
        best = min(classes[D]["S"].items(), key=lambda kv: abs(math.log(kval(kv[0]) / kf)))
        row["nearest_S%d" % D] = {"kappa": kval(best[0]), "via": best[1][1], "dex": math.log10(kval(best[0]) / kf)}
    foot[fname] = row
    say("     footing %-9s a0 %.4e -> kappa %.5f ; nearest S_1 %.5f (%s, %+.4f dex) ; nearest S_2 %.5f (%+.4f dex)"
        % (fname, a, kf, row["nearest_S1"]["kappa"], row["nearest_S1"]["via"], row["nearest_S1"]["dex"],
           row["nearest_S2"]["kappa"], row["nearest_S2"]["dex"]))

# second prediction (D3): the only z-dependence the class can carry
Hz = math.sqrt(OMEGA_M * 3.5**3 + OMEGA_L)
say("     D3: class members read H_L (a0 constant for w=-1, same as the framework) or H(z): a0(2.5)/a0(0) = H(2.5)/H0 = %.4f; no coefficient-dependent second number" % Hz)

# ---------------------------------------------------------------------------
# Angle A: audit of "4 is the only natural value the data admit"
# ---------------------------------------------------------------------------
say("\n-- Angle A: A19's own natural grid vs the data")
def z(R, band):
    return (1 / math.sqrt(R) - band[0]) / band[1]

rep = [z(R, KAP_CFG493) for R in (1, 2, 4)]
ok6 = all(abs(a - b) < 0.01 for a, b in zip(rep, (6.14, 3.05, 0.87)))
check("K6", ok6, "A19 K10 reproduced: %.2f / %.2f / %.2f" % tuple(rep), "6.14/3.05/0.87 +-0.01")

grid = sorted(set(b * b * ch for b in (1, 2) for ch in (1, 2, 3, 4)))
extra_R = {"4pi (A19 repair)": 4 * math.pi}
audit = {}
ok7 = True
for bname, band in BANDS.items():
    rows = [(R, 1 / math.sqrt(R), z(R, band)) for R in grid]
    within = [r for r in rows if abs(r[2]) < 2]
    closer = [r for r in rows if abs(r[2]) < abs(z(4, band)) and r[0] != 4]
    verdict = "SUPPORTED" if (len(within) == 1 and within[0][0] == 4) else "CONTRADICTED"
    caps = [(n, 1 / math.sqrt(n), z(n, band)) for n in range(1, 9)]
    audit[bname] = {"grid": [{"R": r[0], "kappa": r[1], "z": r[2]} for r in rows],
                    "n_within_2sigma": len(within), "closer_than_R4": [r[0] for r in closer],
                    "R_4pi": {"kappa": 1 / math.sqrt(4 * math.pi), "z": z(4 * math.pi, band)},
                    "caps_1_to_8": [{"R": n, "kappa": k, "z": zz} for n, k, zz in caps],
                    "caps_within_2sigma": [n for n, k, zz in caps if abs(zz) < 2],
                    "verdict": verdict}
    ok7 &= all(math.isfinite(r[2]) for r in rows)
    say("     %-6s: " % bname + "  ".join("R=%d k=%.3f z=%+.2f" % r for r in rows))
    say("             R=4pi k=%.3f z=%+.2f ; caps R=1..8 within 2 sigma: %s"
        % (1 / math.sqrt(4 * math.pi), z(4 * math.pi, band), audit[bname]["caps_within_2sigma"]))
    say("     V_A %-6s %s: %d of %d A19-grid values within 2 sigma; closer than R=4: %s"
        % (bname, verdict, len(within), len(rows), [r[0] for r in closer]))
check("K7", ok7, "Angle-A verdict computed for both bands: CFG493 %s, A81 %s"
      % (audit["CFG493"]["verdict"], audit["A81_DE"]["verdict"]), "computed")

# ---------------------------------------------------------------------------
results.update({
    "angle_T": {
        "S1_n": len(S1), "S2_n": len(S2),
        "half_in_S1": HALF in S1, "half_in_S2": HALF in S2, "Z4pi_in_S1": ZKEY in S1,
        "Z4pi_construction": S1.get(ZKEY, (None, None))[1],
        "half_constructions_S2": [{"via": t[0], "m": t[1], "q2": t[2], "sqrt_of_pi_odd_block": t[3]} for t in all_half[:20]],
        "n_half_constructions_S2": len(all_half),
        "max_reduction_dev": maxdev,
        "lee": lee_res, "footings": foot, "Hz2p5_over_H0": Hz,
    },
    "angle_A": audit,
})
say("\nD5_KAPPA_FOUR COMPLETE: %d/%d checks PASS." % (npass, nchk))
with open(OUT_TXT, "w") as fh:
    fh.write("\n".join(lines) + "\n")
with open(OUT_JSON, "w") as fh:
    json.dump(results, fh, indent=1, default=str)
sys.exit(0 if npass == nchk else 1)

"""KAP1: lemma L1 and routes R1-R3 of FROZEN_CRITERIA.md (commit 3116ad793b).

Run:  OMP_NUM_THREADS=1 python3 kap1.py            -> kap1.out (stdout), kap1.json
      KAP1_MUTATE=1 OMP_NUM_THREADS=1 python3 kap1.py -> kap1_MUTATE.out, kap1_MUTATE.json (exits 1 when a control bites)

Every route is computed twice: symbolically (sympy) and numerically in SI by a separately written chain.
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json
import math
import os
import sys

import sympy as sp

MUT = os.environ.get("KAP1_MUTATE") == "1"
OUT = {}
FAILS = []


def P(*a):
    print(*a)


def check(name, ok):
    P(("  PASS  " if ok else "  FAIL  ") + name)
    if not ok:
        FAILS.append(name)
    return ok


# ---------------------------------------------------------------- SI inputs
G = 6.67430e-11
c = 299792458.0
Msun = 1.98892e30
kpc = 3.0856775814913673e19
Mpc = 1e3 * kpc
H0 = 67.4e3 / Mpc
OL = 0.685
rho_crit = 3 * H0 ** 2 / (8 * math.pi * G)
rho_L = OL * rho_crit
s_L = c * math.sqrt(G * rho_L)       # c sqrt(G rho_Lambda)
s_C = c * math.sqrt(G * rho_crit)    # c sqrt(G rho_crit)

P("KAP1 run, MUTATE =", MUT)
P("Inputs: G %.5e, c %.0f, H0 67.4 km/s/Mpc, Omega_L 0.685" % (G, c))
P("  rho_Lambda %.4e kg/m^3, rho_crit %.4e kg/m^3" % (rho_L, rho_crit))
P("Known answers")
a0_can, a0_alt = 0.5 * s_L, 0.5 * s_C
check("KA1 canonical a0 = (1/2) c sqrt(G rho_L) = %.4e vs 9.3603e-11 (rel < 1e-3)" % a0_can,
      abs(a0_can / 9.3603e-11 - 1) < 1e-3)
check("KA2 alt a0 = (1/2) c sqrt(G rho_crit) = %.4e vs 1.1312e-10 (rel < 1e-3)" % a0_alt,
      abs(a0_alt / 1.1312e-10 - 1) < 1e-3)
OUT["known"] = {"a0_can": a0_can, "a0_alt": a0_alt, "rho_L": rho_L, "rho_crit": rho_crit}

TARGET = 0.5            # T_can, declared in the criteria for R1-R3
WIN = 0.0178            # dex

# ---------------------------------------------------------------- L1: dimensional census
P("\nL1  Are the new inputs able to fix a universal kappa? Dimension census (L, M, T exponents)")
dims = {"G": (3, -1, -2), "rho": (-3, 1, 0), "M": (0, 1, 0), "a0": (1, 0, -2),
        "t": (0, 0, 1), "r": (1, 0, 0), "c": (1, 0, -1), "muK": (-1, 0, 0)}


def groups(names):
    A = sp.Matrix([[dims[n][i] for n in names] for i in range(3)])
    return [list(v) for v in A.nullspace()]


def show(names):
    ns = groups(names)
    P("  variables", names, "-> %d dimensionless group(s)" % len(ns))
    for v in ns:
        P("    exponents", dict(zip(names, [str(x) for x in v])))
    return ns


base = ["G", "rho", "M", "a0"]
ns_base = show(base)
# groups that contain a0 and are free of M
mfree = [v for v in ns_base if v[base.index("a0")] != 0 and v[base.index("M")] == 0]
L1_nogroup = check("L1a without c: no dimensionless group contains a0 and is free of M_b", len(mfree) == 0)
withc = base + ["c"]
ns_c = show(withc)
# is there a combination with M exponent 0 and a0 exponent nonzero? solve within span
w = sp.symbols("w0:%d" % len(ns_c))
comb = sp.zeros(len(withc), 1)
for wi, v in zip(w, ns_c):
    comb += wi * sp.Matrix(v)
sol = sp.solve([comb[withc.index("M")], comb[withc.index("a0")] - 1], w, dict=True)
grp = None
if sol:
    grp = [sp.simplify(x.subs(sol[0]).subs({wi: 0 for wi in w})) for x in comb]
    P("  with c, the M-free group containing a0:", dict(zip(withc, [str(x) for x in grp])),
      "  i.e. a0 / (c sqrt(G rho)) = kappa")
check("L1b with c added: an M-free group containing a0 exists (kappa itself)", grp is not None)
withmu = base + ["muK"]
ns_mu = show(withmu)
P("  with the clock mass mu_K (a length^-1) instead of c: a0 mu_K/(G rho) is M-free; mu_K is bounded and free")
P("  (galaxy bound <= 0.1/Mpc, CMB wants >= 198/Mpc; MK1 NO VALUE), so that group is a TRADE, not a kappa.")
P("  Which new inputs carry c? COL1 (weak-field collapse in an FRW background, units kpc, km/s, Msun; c absent),")
P("  FLD1 (reads COL1-type runs), FB1 identities (sigma^2 = (1/2) sqrt(G M a0), J(g) = (a0^2/K)[u - ln(1+u)]): none.")
P("  Radii and times in them are set by (G, rho, M_b): R ~ (M/rho)^(1/3), t ~ 1/sqrt(G rho), which reduces to base.")
OUT["L1"] = {"groups_without_c": [[str(x) for x in v] for v in ns_base],
             "Mfree_a0_group_without_c": len(mfree), "group_with_c": [str(x) for x in grp] if grp else None}

# ---------------------------------------------------------------- FLD1 table (z = 0, read from RESULT.md)
FLD1 = [(8, 21), (9, 46), (9.4, 62), (10, 99), (10.45, 139), (10.7, 169), (10.9, 197), (11.2, 248), (11.5, 312)]
RTA = {7: 19, 8: 40, 9: 88, 9.4: 120, 10: 190, 10.45: 268, 10.7: 325, 10.9: 378, 11.2: 476, 11.5: 600}


def slope(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


# ---------------------------------------------------------------- R1: fold-reach equality
P("\nR1  Postulate: r_M = sqrt(G M_b / a0) equals the fold radius R_fold.  Target T_can (kappa = 1/2 on rho_Lambda)")
fmul = 2.0 if MUT else 1.0
Gs, rho, M, a0, f, cc = sp.symbols("G rho M a0 f c", positive=True)
Rmax = (3 * M / (8 * sp.pi * rho)) ** sp.Rational(1, 3)
a0_R1 = sp.simplify(Gs * M / (f * Rmax) ** 2)
kap_R1 = sp.simplify(a0_R1 / (cc * sp.sqrt(Gs * rho)))
P("  de Sitter limit, R_fold = f R_max, R_max^3 = 3 M/(8 pi rho):  a0 =", a0_R1)
P("  kappa = a0/(c sqrt(G rho)) =", kap_R1)
dlk = sp.simplify(M * sp.diff(sp.log(kap_R1), M))
check("R1 sympy: d ln kappa / d ln M_b = %s (nonzero: kappa is mass-dependent)" % dlk, dlk != 0)
xs, ys, ks = [], [], []
P("  SI chain on FLD1's z = 0 fold radii (f multiplier %.0f):" % fmul)
for lm, rk in FLD1:
    Mk = 10 ** lm * Msun
    a = G * Mk / (fmul * rk * kpc) ** 2
    k = a / s_L
    xs.append(lm)
    ys.append(math.log10(a))
    ks.append(k)
    P("    log M_b %5.2f  R_fold %4d kpc  a0 = %.3e m/s^2  kappa = %.3e  (%.2f dex from 1/2)" %
      (lm, rk, a, k, math.log10(k / TARGET)))
sl = slope(xs, ys)
P("  mass slope d log a0 / d log M_b on FLD1 radii: %.3f (de Sitter limit 1/3); spread %.2f dex" % (sl, max(ys) - min(ys)))
k_dS = [float(kap_R1.subs({Gs: G, rho: rho_L, M: 10 ** lm * Msun, f: 0.52 * fmul, cc: c})) for lm, _ in FLD1]
P("  de Sitter-limit kappa at f = 0.52:", ", ".join("%.2e" % k for k in k_dS))
R1_label = "NOT DERIVED"
OUT["R1"] = {"a0_symbolic": str(a0_R1), "kappa_symbolic": str(kap_R1), "dlnk_dlnM": str(dlk),
             "kappa_FLD1": ks, "slope": sl, "kappa_dS_f052": k_dS, "label": R1_label}
d1 = [math.log10(k / TARGET) for k in ks]
P("  LABEL R1:", R1_label, "(c-free, so by L1 mass-dependent; %.2f to %.2f dex from 1/2 across the masses)" % (min(d1), max(d1)))

# ---------------------------------------------------------------- R2: fold ratio
P("\nR2  Postulate: kappa = R_fold / R_ta.  Target T_can")
ratio0 = 0.52
P("  FLD1 z = 0: R_fold/R_ta = 0.52 ->  %.4f dex from 1/2 (window %.4f), %.4f dex from 0.4607" %
  (math.log10(ratio0 / 0.5), WIN, math.log10(ratio0 / math.sqrt(2 / (3 * math.pi)))))
P("  per mass from FLD1's table:", ", ".join("%.3f" % (rk / RTA[lm]) for lm, rk in FLD1 if lm in RTA))
P("  epoch drift (FLD1): z 0 / 1 / 2 / 4 = 0.52 / 0.46 / 0.435 / 0.32  -> spread %.3f dex" %
  math.log10(0.52 / 0.32))
dln = math.log(139.25 / 139.23) / math.log(1.1312e-10 / 9.3603e-11)
P("  counterfactual (FINAL18 table): R_fold 139.25 / 139.23 kpc at a0 canonical / alt -> d ln R_fold / d ln a0 = %.1e" % dln)
check("R2 counterfactual: the fold ratio does not move when a0 (kappa) moves (|response| < 1e-2) -> rules S2 fails",
      abs(dln) < 1e-2)
# uniform-sphere virial ratio, sympy
Rt, Rv, m = sp.symbols("R_ta R_v m", positive=True)
E_ta = -sp.Rational(3, 5) * Gs * m ** 2 / Rt
W_v = -sp.Rational(3, 5) * Gs * m ** 2 / Rv
vir = sp.solve(sp.Eq(E_ta, W_v / 2), Rv)[0]
P("  uniform-sphere collapse, energy conserved, virial 2K + W = 0: R_vir =", vir, "-> R_vir/R_ta =", sp.simplify(vir / Rt))
check("R2 sympy: R_vir/R_ta = 1/2 for the uniform sphere (the 0.52 is a virial-class number, rules S7)",
      sp.simplify(vir / Rt) == sp.Rational(1, 2))
R2_label = "NUMEROLOGY"
OUT["R2"] = {"ratio_z0": ratio0, "dex_from_half": math.log10(ratio0 / 0.5), "dlnRfold_dlna0": dln,
             "virial_ratio": str(sp.simplify(vir / Rt)), "label": R2_label}
P("  LABEL R2:", R2_label, "(inside the window at z = 0 only; no mechanism; a0-blind; drifts 0.21 dex with epoch)")

# ---------------------------------------------------------------- R3: joint stress matching at the fold
P("\nR3  Postulate: at the fold the static halo's stress |Pi| = g^2/(8 pi G) (FB1 deep field) equals the vacuum's")
P("    |p| = rho_Lambda c^2.  Target T_can")
coup = 4 if MUT else 8          # 8 pi G -> 4 pi G in the twin
g, gN, R = sp.symbols("g g_N R", positive=True)
gstar = sp.solve(sp.Eq(g ** 2 / (coup * sp.pi * Gs), rho * cc ** 2), g)[0]
P("  the condition fixes the halo field at the fold: g_* =", gstar, " = %s c sqrt(G rho)" % sp.sqrt(coup * sp.pi))
a0_exact = sp.simplify(g * (g - gN) / gN)               # law S inverted: g_N = g^2/(g + a0)
check("R3 sympy: law S inverted, g_N = g^2/(g + a0) at a0 = g(g-g_N)/g_N",
      sp.simplify(g ** 2 / (g + a0_exact) - gN) == 0)
a0_deep = sp.simplify((gstar * R) ** 2 / (Gs * M))     # deep field g = sqrt(G M a0)/R
P("  deep-field form: a0 = g_*^2 R_fold^2/(G M_b) =", a0_deep)
kap_R3 = sp.simplify(a0_deep / (cc * sp.sqrt(Gs * rho)))
P("  kappa =", kap_R3, " (depends on M_b and R_fold; with R_fold ~ M_b^(1/3) it scales as M_b^(-1/3))")
xs, ys, ks, gaps = [], [], [], []
for lm, rk in FLD1:
    Mk = 10 ** lm * Msun
    Rm = rk * kpc
    gn = G * Mk / Rm ** 2
    gs = math.sqrt(coup * math.pi * G * rho_L) * c              # SI chain, written separately
    a_ex = gs * (gs - gn) / gn
    a_dp = gs ** 2 * Rm ** 2 / (G * Mk)
    g_can = 0.5 * (gn + math.sqrt(gn * gn + 4 * gn * a0_can))   # the record's halo field at the fold
    xs.append(lm)
    ys.append(math.log10(a_ex))
    ks.append(a_ex / s_L)
    gaps.append(math.log10(gs / g_can))
    P("    log M_b %5.2f  a0 = %.3e (deep %.3e)  kappa = %.3e  (%.2f dex from 1/2); g_* / g_law(R_fold) = 10^%.2f" %
      (lm, a_ex, a_dp, a_ex / s_L, math.log10(a_ex / s_L / TARGET), gaps[-1]))
sl3 = slope(xs, ys)
P("  mass slope d log a0 / d log M_b: %.3f; spread %.2f dex" % (sl3, max(ys) - min(ys)))
sym_num = float(kap_R3.subs({Gs: G, rho: rho_L, cc: c, M: 10 ** 10.45 * Msun, R: 139 * kpc}))
check("R3 two paths agree at log M_b 10.45: sympy kappa %.6e vs SI deep chain %.6e (rel < 1e-9)" %
      (sym_num, (math.sqrt(coup * math.pi * G * rho_L) * c * 139 * kpc) ** 2 / (G * 10 ** 10.45 * Msun) / s_L),
      abs(sym_num / ((math.sqrt(coup * math.pi * G * rho_L) * c * 139 * kpc) ** 2 / (G * 10 ** 10.45 * Msun) / s_L) - 1) < 1e-9)
R3_label = "NOT DERIVED"
OUT["R3"] = {"gstar_over_csqrtGrho": str(sp.sqrt(coup * sp.pi)), "kappa_symbolic": str(kap_R3), "kappa": ks,
             "slope": sl3, "gap_gstar_vs_law_dex": gaps, "label": R3_label}
d3 = [math.log10(k / TARGET) for k in ks]
P("  LABEL R3:", R3_label, "(mass-dependent; %.2f to %.2f dex from 1/2; the record's halo field at the fold is %.2f to %.2f dex below g_*)"
  % (min(d3), max(d3), min(gaps), max(gaps)))

# ---------------------------------------------------------------- mutation bookkeeping
if MUT:
    P("\nMUTATE: expected moves")
    k1 = OUT["R1"]["kappa_FLD1"][4]
    k1_main = G * 10 ** 10.45 * Msun / (139 * kpc) ** 2 / s_L
    check("MUTATE R1 f -> 2f moves kappa by 1/4: %.4e / %.4e = %.6f" % (k1, k1_main, k1 / k1_main), abs(k1 / k1_main - 0.25) < 1e-9)
    k3 = OUT["R3"]["kappa"][4]
    gs8 = math.sqrt(8 * math.pi * G * rho_L) * c
    gn = G * 10 ** 10.45 * Msun / (139 * kpc) ** 2
    k3_main = gs8 * (gs8 - gn) / gn / s_L
    check("MUTATE R3 8 pi G -> 4 pi G halves kappa (deep field): ratio %.5f (|r - 1/2| < 1e-2)" % (k3 / k3_main), abs(k3 / k3_main - 0.5) < 1e-2)
    # the L1 control: re-grade L1a on the c-bearing list; it must bite
    bite = len([v for v in groups(withc) if v[withc.index("M")] == 0 and v[withc.index("a0")] != 0]) == 0 and grp is None
    check("MUTATE L1 control: on the c-bearing variable list an M-free a0 group must be ABSENT (expected to FAIL)", bite)

P("\nLabels: L1 %s | R1 %s | R2 %s | R3 %s" % ("HOLDS" if L1_nogroup else "FAILS", R1_label, R2_label, R3_label))
P("Lane word: KAPPA NOT DERIVED" if not MUT else "MUTATE twin")
P("Failed checks:", FAILS if FAILS else "none")
OUT["fails"] = FAILS
OUT["mutate"] = MUT
with open("kap1_MUTATE.json" if MUT else "kap1.json", "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
sys.exit(1 if FAILS else 0)

#!/usr/bin/env python3
"""q1_numeric_audit.py -- lane Q4: run the ten claims of Q4_PREREGISTRATION.md through lane D's bar (alpha_bar_checker.py / bar_lib.py, imported UNMODIFIED).

Run (real):   PYTHONDONTWRITEBYTECODE=1 python3 q1_numeric_audit.py            -> exit 0 iff NO row clears all four criteria under P_MDL or under any declared P_decl
              (H1 in its strongest form; Amendment 7 records that the Q5a row is EXPECTED to clear under N_decl = 2^25, which makes the real exit code 1 and H1 FALSE)
MUTATE:       PYTHONDONTWRITEBYTECODE=1 python3 q1_numeric_audit.py --mutate   -> every miss := 1e-11 and fitted := 0, scale := True: must produce spurious clears (exit 1)
T = 137.035999177 (CODATA 2022 Thomson limit), delta_CODATA = 1.6e-10.
"""
import sys, os, math, json, itertools
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "D_calibration_bar"))
import numpy as np
import mpmath as mp
import bar_lib as B
import alpha_bar_checker as C
mp.mp.dps = 40
MUTATE = "--mutate" in sys.argv
T = mp.mpf("137.035999177")
SIG = 1.6e-10
RHO = C.RHO_DEFAULT
DUP = C.DUP_E2
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

pi, g, z3, e = mp.pi, mp.euler, mp.zeta(3), mp.e
R = mp.log(2 + mp.sqrt(3))
Apoly = 4 * pi ** 3 + pi ** 2 + pi
lnn = 14 * pi ** 2 + mp.log(8)
xk = lnn / 274 + mp.log(lnn) / 294
CA = 137 + 1 / (8 * pi)
val_kt = CA - g / (CA - xk) + z3 / (137 * 20)
val_v20 = CA - g / CA + z3 / (137 * 20)
Kpaper = 10 - 1 / (14 + 1 / (1 + 1 / (7 + 1 / (3 + 1 / (1 + mp.mpf(1) / 3)))))
S_of_K = lambda K: Apoly - 1 / (24 * Apoly) - 1 / (Apoly ** 2 * pi ** 2 * K)
alpha_T = 1 / T
gil = pi / (29 * mp.cos(pi / 137) * mp.tan(pi / (29 * 137)))

# id, label, value, mdl_expr (named leaves ok), N_decl list [(label, N)], fitted, scale_stated, predicted_precision, status
rows = [
 ("Q2a", "HBMB F = Z0/(Z0+2R_K) = alpha/(1+alpha): 1/F", T + 1, None, [("k in Z0/(Z0+kR_K), k=1..8", 8)], 1, False, float(alpha_T), "ABSTRACT (Crossref v2) + thesis prose; identity input"),
 ("Q2b", "HBMB alpha = Z0/(2R_K) (identity of SI constants)", T, None, [], 1, False, 0.0, "ABSTRACT (Crossref v1, v2)"),
 ("Q3", "Xu tensor cascades: stated 137.0359991770012", mp.mpf("137.0359991770012"), None, [], 1, False, 0.0, "FULL TEXT + code (q3: code adds to a hard-coded CODATA baseline)"),
 ("Q4", "Maya lattice: stated 137.0359991648", mp.mpf("137.0359991648"), None, [], 0, True, 0.0, "SNIPPET only (fitted reals: UNKNOWN, steelman 0)"),
 ("Q5a", "Relator/C-Space, Sep-Oct 2025 versions: 137.0359991769773", mp.mpf("137.0359991769773"), None, [("2^25 (lower bound, >= 25 hand-set choices)", 2.0 ** 25), ("2^40 (upper bound)", 2.0 ** 40)], 0, True, 0.0, "code REPRODUCED (q5 T2); text searched not read"),
 ("Q5b", "Relator/C-Space, Apr 2026 versions: 137.0359991634947", mp.mpf("137.0359991634947"), None, [("2^25", 2.0 ** 25), ("2^40", 2.0 ** 40)], 0, True, 0.0, "code REPRODUCED (q5 T3)"),
 ("Q6s", "Kosmoplex poster, STATED value 137.035999143", mp.mpf("137.035999143"), "137+1/(8*pi)-g/(137+1/(8*pi)-(Ln/(2*137)+ln(Ln)/(42*7)))+z3/(137*20)", [("4.55e12 slot family (Amendment 1)", 4.55e12)], 0, False, 0.0, "poster FULL TEXT; preprints.org v3 blocked"),
 ("Q6c", "Kosmoplex poster formula COMPUTED (q4)", val_kt, "137+1/(8*pi)-g/(137+1/(8*pi)-(Ln/(2*137)+ln(Ln)/(42*7)))+z3/(137*20)", [("4.55e12 slot family", 4.55e12)], 0, False, 0.0, "poster FULL TEXT"),
 ("Q6v", "Kosmoplex Principia V20 (33.36) COMPUTED (no x)", val_v20, "137+1/(8*pi)-g/(137+1/(8*pi))+z3/(137*20)", [("4.55e12", 4.55e12)], 0, False, 0.0, "V20 read at ch. 9, 27, 29, 33"),
 ("Q7", "Bleger 19596/143 + 5R/(6370-2R)", mp.mpf(19596) / 143 + 5 * R / (6370 - 2 * R), "19596/143+5*R/(6370-2*R)", [("1.4e12 (lane K family)", 1.4e12)], 0, False, 0.0, "paper FULL TEXT; source states it is not a derivation"),
 ("Q8a", "Blandino S with K fitted to CODATA (paper K = 9.9327912864)", S_of_K(mp.mpf("9.9327912864")), None, [("1.4e15", 1.4e15)], 1, False, 0.0, "paper FULL TEXT"),
 ("Q8b", "Blandino model mean <S> printed 137.035999167828 (replicated q6)", mp.mpf("137.035999167828"), None, [("1.4e15", 1.4e15)], 1, False, 0.0, "paper FULL TEXT; replicated q6"),
 ("Q8c", "Blandino formula with K = 10 (F = 0): A - 1/(24A) - 1/(10 A^2 pi^2) [my variant, not the author's claim]", S_of_K(mp.mpf(10)), "4*pi**3+pi**2+pi-1/(24*(4*pi**3+pi**2+pi))-1/(10*(4*pi**3+pi**2+pi)**2*pi**2)", [("1728 x 100 x 40 = 6.9e6", 1728 * 100 * 40)], 0, False, 0.0, "constructed here from q6 B4"),
 ("Q9", "Reinisch alpha = 7.364e-3 (author's error ~1%)", 1 / mp.mpf("7.364e-3"), None, [], 0, False, 1e-2, "HAL author manuscript, FULL TEXT to Eq. 24"),
 ("Q10", "Gilson pi/(29 cos(pi/137) tan(pi/(29*137)))", gil, "pi/(29*cos(pi/137)*tan(pi/(29*137)))", [("40000 (lane K)", 40000)], 1, False, 0.0, "arXiv quant-ph/0112048 FULL TEXT: n2 chosen to match CODATA"),
]

def crit(c):
    return "c1=%s c2=%s c3=%s c4=%s" % tuple("Y" if c[k] else "n" for k in ("c1_lookelsewhere", "c2_precision", "c3_no_fitted_real", "c4_scale_stated"))

P("q1_numeric_audit  MUTATE=%s  T=%s  delta_CODATA=%g  rho=%.4f  dup=%.4f" % (MUTATE, mp.nstr(T, 12), SIG, RHO, DUP))
P("%-4s %-84s %-18s %-9s %-9s" % ("id", "claim", "1/alpha", "miss", "sigma"))
clears = []
records = {}
for rid, label, val, mexpr, Nlist, fitted, scale, pred, status in rows:
    d = float(abs(val / T - 1))
    fit, sc = fitted, scale
    if MUTATE:
        d = 1e-11; fit = 0; sc = True
    rec = dict(id=rid, value=mp.nstr(val, 15), miss=d, sigma=d / SIG)
    P("%-4s %-84s %-18s %-9.3g %-9.3g" % (rid, label[:84], mp.nstr(val, 15), d, d / SIG))
    # P_MDL
    if mexpr:
        lg, st = B.mdl_size(mexpr, intmax=12)
        Nm = (2.0 ** lg) * DUP
        rm = B.evaluate(d, Nm, RHO, predicted_precision=pred, fitted_reals=fit, scale_stated=sc)
        P("       P_MDL: 2^%.1f syntactic x dup -> N=%.3g ; P=%.3g ; %s ; clears=%s" % (lg, Nm, rm["p"], crit(rm), rm["clears"]))
        if rm["clears"]: clears.append((rid, "MDL"))
        rec["P_mdl"] = rm["p"]
    rf = B.evaluate(d, 1.0, RHO, predicted_precision=pred, fitted_reals=fit, scale_stated=sc)
    P("       P_forced (N=1): P=%.3g ; %s ; would pass c1-c3 if scale granted: %s" % (rf["p"], crit(rf), rf["c1_lookelsewhere"] and rf["c2_precision"] and rf["c3_no_fitted_real"]))
    rec["P_forced"] = rf["p"]
    for lab, N in Nlist:
        rd = B.evaluate(d, float(N), RHO, predicted_precision=pred, fitted_reals=fit, scale_stated=sc)
        P("       P_decl [%s]: N=%.3g ; P=%.3g ; %s ; clears=%s" % (lab, N, rd["p"], crit(rd), rd["clears"]))
        if rd["clears"]: clears.append((rid, "decl:" + lab))
    delta_eff = max(d, pred)
    Nstar = B.BAR_P / (RHO * 2 * delta_eff) if delta_eff > 0 else float("inf")
    P("       break-even family size for P < 1e-3 at this miss: N* = %.3g (2^%.1f)" % (Nstar, math.log2(Nstar) if Nstar < float("inf") else float("nan")))
    P("       status: %s" % status)
    records[rid] = rec

# ---------------- L2: too good to be true (Amendment 10): P_z = erf(z/sqrt 2), z = |miss|/sigma (2.1e-8 absolute)
P("")
P("== L2 too-good-to-be-true (Amendment 10): chance that a CORRECT theory lands this close to the CODATA central value (sigma = 2.1e-8 absolute) ==")
for rid, label, val, mexpr, Nlist, fitted, scale, pred, status in rows:
    if rid in ("Q2a", "Q2b", "Q9", "Q6v", "Q8a"):
        continue
    z = abs(val - T) / mp.mpf("2.1e-8")
    Pz = mp.erf(z / mp.sqrt(2))
    P("  %-4s z = %-10s P_z = %-10s (likelihood ratio 'adjusted to the central value' : 'correct' = %s)" % (rid, mp.nstr(z, 3), mp.nstr(Pz, 3), mp.nstr(1 / Pz, 3) if Pz > 0 else "inf"))
P("  (Q8a is excluded because K is fitted to the central value by the author's own account; Q2, Q9, Q6v miss by far more than sigma.)")

# harness agreement: the checker's own assess() on the one row it can evaluate (pi only)
r_h = C.assess(expr=rows[12][3], verbose=False, delta=None)
lg8, _ = B.mdl_size(rows[12][3], intmax=12)
rm8 = B.evaluate(float(abs(rows[12][2] / T - 1)), (2.0 ** lg8) * DUP, RHO, fitted_reals=0, scale_stated=True)
harness_ok = abs(math.log10(max(r_h["p"], 1e-300)) - math.log10(max(rm8["p"], 1e-300))) < 1e-6 or (r_h["p"] > 0.999 and rm8["p"] > 0.999)
P("harness: C.assess(expr=Q8c) agrees with this script's B.evaluate route: %s (P=%.3g)" % (harness_ok, r_h["p"]))
assert harness_ok

# ---------------- empirical family scan for Q8c (rounding / local density instead of the flat rho)
P("")
P("== Q8c empirical family scan: A(c1,c2,c3) - 1/(k A) - 1/(m A^2 pi^2), c in 1..12, k in 1..100, m in 1..40 (6.9e6 members) ==")
Tf = float(T)
c1, c2, c3 = np.meshgrid(np.arange(1, 13), np.arange(1, 13), np.arange(1, 13), indexing="ij")
Af = c1 * math.pi ** 3 + c2 * math.pi ** 2 + c3 * math.pi
ks = np.arange(1, 101, dtype=float)
ms = np.arange(1, 41, dtype=float)
Af = Af.reshape(-1)
cnt = {5e-10: 0, 1e-10: 0, 2.7e-11: 0}
hits_bar = []
for k in ks:
    base = Af - 1.0 / (k * Af)
    for m in ms:
        v = base - 1.0 / (m * Af ** 2 * math.pi ** 2)
        rel = np.abs(v / Tf - 1)
        for tol in cnt:
            cnt[tol] += int((rel <= tol).sum())
        idx = np.nonzero(rel <= 5e-10)[0]
        for i in idx:
            hits_bar.append((int(c1.reshape(-1)[i]), int(c2.reshape(-1)[i]), int(c3.reshape(-1)[i]), int(k), int(m), float(rel[i])))
P("  members within 5e-10 of T: %d ; within 1e-10: %d ; within 2.7e-11 (the K=10 variant's miss): %d" % (cnt[5e-10], cnt[1e-10], cnt[2.7e-11]))
P("  members with (4,1,1) among the 5e-10 hits: %s" % ([h for h in hits_bar if h[:3] == (4, 1, 1)][:5]))
n_all = 1728 * 100 * 40
P("  flat-density P_decl for this row: lambda = N*rho*2*miss = %.3g; the empirical count of OTHER members within the same miss is %d (the count above includes the K=10 variant itself): the flat estimate is not contradicted" % (n_all * RHO * 2 * 2.7e-11, cnt[2.7e-11] - 1))
P("  the three hits within 5e-10 are one skeleton (4,1,1,k=24) with m = 9, 10, 11: they are not independent trials")
# stagewise decomposition of the skeleton
A0 = float(Apoly)
n_poly = int((np.abs(Af / Tf - 1) <= abs(A0 / Tf - 1) * 1.0001).sum())
P("  stage 1: A(4,1,1) = %.9f misses T by %.3g relative; members of the 1728 polynomial family at least as close: %d (fraction %.2e)" % (A0, abs(A0 / Tf - 1), n_poly, n_poly / 1728.0))
res2 = A0 - 1.0 / (24 * A0) - Tf
sp2 = 1.0 / (24.0 ** 2 * A0)
P("  stage 2: after -1/(24A) the residual is %.3e (absolute); the spacing between adjacent k near 24 is %.3e, so rounding to the nearest integer k lands within the residual by chance %.3f (the third derivative 24 is the author's own justification)" % (res2, sp2, min(1.0, 2 * abs(res2) / sp2)))
res3 = S_float = float(S_of_K(mp.mpf(10))) - Tf
sp3 = 1.0 / (10.0 ** 2 * A0 ** 2 * math.pi ** 2)
P("  stage 3: after -1/(10 A^2 pi^2) the residual is %.3e (absolute, %.3g relative); the spacing between adjacent m near 10 is %.3e, so rounding lands within it by chance %.3f" % (res3, abs(res3) / Tf, sp3, min(1.0, 2 * abs(res3) / sp3)))
P("  product of the three stage chances (heuristic) = %.3g ; the (4,1,1) polynomial is Sherbon's earlier search result (K row K14), so the size of THAT search multiplies this by an unknown factor" % ((n_poly / 1728.0) * min(1.0, 2 * abs(res2) / sp2) * min(1.0, 2 * abs(res3) / sp3)))
Q8c_hits = cnt

# ---------------- two-stage landing for Q5a
P("")
P("== Q5a two-stage landing (Amendment 7 (L)) ==")
s1_shift, s1_miss = 2.03e-8, 6.82e-10        # chi-ladder: from q5 T4 (both ladders on minus chi-ladder off gives the shift; miss without self-ladder)
s2_shift, s2_miss = 6.82e-10, 1.66e-13        # self-ladder: shift 6.82e-10, miss after 1.66e-13
p1 = min(1.0, 2 * s1_miss / (2 * s1_shift)); p2 = min(1.0, 2 * s2_miss / (2 * s2_shift))
P("  stage 1 (chi-ladder, size %.2e): landing within %.2e has chance ~ %.3g ; stage 2 (self-ladder, size %.2e): landing within %.2e has chance ~ %.3g ; product %.3g" % (s1_shift, s1_miss, p1, s2_shift, s2_miss, p2, p1 * p2))
P("  (heuristic: each ladder term treated as a correction of unknown position within +- its own size; the checker's P_decl at N = 2^25 is %.3g and at 2^40 is %.3g)" % (B.evaluate(1.66e-13, 2.0 ** 25, RHO)["p"], B.evaluate(1.66e-13, 2.0 ** 40, RHO)["p"]))

# ---------------- checks that the identity in Q2b is an identity
P("")
P("== Q2b identity check: alpha = Z0/(2 R_K) with R_K = h/e^2 (exact in the 2019 SI) and Z0 = 1/(eps0 c) ==")
h = mp.mpf("6.62607015e-34"); ee = mp.mpf("1.602176634e-19"); cc = mp.mpf(299792458)
eps0 = mp.mpf("8.8541878188e-12")     # CODATA 2022 (RECALLED, 11 digits); eps0 itself is derived from the measured alpha
RK = h / ee ** 2; Z0 = 1 / (eps0 * cc)
a_from = Z0 / (2 * RK)
P("  R_K = %s ohm ; Z0 = %s ohm ; Z0/(2 R_K) = %s ; 1/(that) = %s ; miss vs 137.035999177 = %s (limited by the 11 recalled digits of eps0)" % (mp.nstr(RK, 12), mp.nstr(Z0, 12), mp.nstr(a_from, 12), mp.nstr(1 / a_from, 12), mp.nstr(abs(1 / a_from / T - 1), 3)))
P("  algebra: Z0/(2 R_K) = (mu0 c) e^2/(2 h) = e^2/(4 pi eps0 hbar c) = alpha exactly; so 'F = Z0/(Z0 + 2 R_K) = alpha + O(alpha^2)' equals alpha/(1+alpha) with 1/F = %s, miss %s relative (= alpha)" % (mp.nstr(T + 1, 12), mp.nstr(1 / T, 4)))

# ---------------- verdict
P("")
P("== Verdict ==")
P("rows passing all four criteria under P_MDL or a declared P_decl: %s" % (clears if clears else "none"))
P("H1 (no claim among Q1-Q9 clears the bar, strongest reading): %s" % ("TRUE" if not clears else "FALSE"))
ids = sorted({c[0] for c in clears})
tag = "_MUTATE" if MUTATE else ""
json.dump(records, open(os.path.join(HERE, "q1_results%s.json" % tag), "w"), indent=1, default=str)
open(os.path.join(HERE, "q1_numeric_audit%s.out" % tag), "w").write("\n".join(out) + "\n")
sys.exit(1 if clears else 0)

#!/usr/bin/env python3
"""n1_4 -- score the joint-coupling maps (A: S^2 flux; C: CP^2 x S^2 product; C*: normalisation-free C; D: SU(5)/SO(10) level structure; E: S^1 KK) with the joint ratio scorer.
Pre-registered in N1_PREREGISTRATION.md (Parts II-III, Amendments 1-2).  Inputs: measured couplings at m_Z run with the SM b's (derived from field content) to the scale mu_c of each map.

Ratios:  rY2 = alpha_Y/alpha_2 (alpha_Y in the Q = T_3 + Y normalisation),  r23 = alpha_2/alpha_3.  Predictions (n1_1, n1_2):
  Map A1: rY2 = N^2/6 (Y = q, N = 1..6);  A2: rY2 = 2/(3 Y_d^2), Y_d in {1/2, 1/6};  scale mu_c = 1/R with alpha_2(mu_c) = 3 (l_P/R)^2.
  Map C : rY2 = N_2^2/6, r23 = (1/2)(N_1/N_2)^2, R_FS^2/R_S2^2 = (8/3)(N_1/N_2)^2, alpha_2 = 3 l_P^2/R_S2^2, mu_c = 1/R_max.   C*: only r23 is scored.
J1 (accuracy): every ratio within tol = max(2 delta_run, 1%) (primary) or the extended tol (also >= the mu_c-ambiguity of factor 3.5).  J2: P = 1 - exp(-N_trials prod 2 tol/ln 100) < 1e-3.  J3: one fitted real (overall scale).

Run:     python3 n1_4_score_maps.py            (real run, exit 0 when every internal consistency check passes; the VERDICTS are printed, they are not pass/fail of the script)
MUTATE:  python3 n1_4_score_maps.py --mutate   (control: lane A's b_Y = (3/5) b_1 bug; the entry check 1/alpha_em(m_P) = 104.94 must FAIL, exit 1)
"""
import sys
sys.dont_write_bytecode = True
import os, math, json
from fractions import Fraction
import numpy as np
from scipy.optimize import brentq
import n1_lib as L

MUTATE = "--mutate" in sys.argv
CHECKS = []
RESULTS = {}


def check(tag, ok, detail=""):
    CHECKS.append((tag, bool(ok)))
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag} {detail}")


print("=" * 100)
print("N1-4 map scoring -- mode: " + ("MUTATE CONTROL (b_Y = 3/5 b_1)" if MUTATE else "REAL RUN"))
print("=" * 100)
run = L.Runner(mutate=MUTATE)
aP = run.oneloop(L.MPL, L.SET_A)
check("E0 entry check: one-loop 1/alpha_em(m_P) = 104.94 +- 0.1 (guards the running against the lane-A bug)", abs(aP[0] + aP[1] - 104.937) < 0.1, f"(got {aP[0] + aP[1]:.3f})")

if MUTATE and not CHECKS[-1][1]:
    print("\nMUTATE control tripped at the entry check (the corrupted running is detected before any map is scored): exit 1")
    sys.exit(1)

# ------------------------------------------------------------------ helper: scoring with primary and extended tolerance
def score(pred, mu, n_trials):
    meas = run.ratios(run.run(mu))
    dr, _, cen = run.delta_run(mu)
    sa = L.scale_ambiguity(run, mu)
    r_p = L.joint_score(pred, {k: meas[k] for k in pred}, {k: dr[k] for k in pred}, n_trials)
    dr_ext = {k: max(dr[k], sa[k] / 2.0) for k in pred}          # tol_ext = max(2 dr, 1%, sa) = 2*max(dr, sa/2) floored at 1%
    r_e = L.joint_score(pred, {k: meas[k] for k in pred}, dr_ext, n_trials)
    return r_p, r_e, meas, dr, sa


def fmt(r):
    return "; ".join(f"{k}: pred {v['pred']:.4f} vs {v['meas']:.4f} ({v['miss']:+.1%}, tol {v['tol']:.2%}, {'ok' if v['ok'] else 'X'})" for k, v in r["rows"].items())


# ------------------------------------------------------------------ MAP A
print("\n=== MAP A: S^2 flux (lane F), predicts alpha_Y/alpha_2 ===")
mu_A = run.alpha2_selfconsistent_mu()
aA = run.run(mu_A)
print(f"    scale: mu_c = M_P sqrt(alpha_2/3) = {mu_A:.4e} GeV (R/l_P = {L.MPL / mu_A:.3f}), alpha_2^-1 = {aA[1]:.3f} (this fixes R: the ONE fitted real), alpha_Y^-1 = {aA[0]:.3f}, alpha_3^-1 = {aA[2]:.3f}")
mA = run.ratios(aA)
print(f"    measured alpha_Y/alpha_2 at mu_c = {mA['rY2']:.4f}")
A_members = [(f"A1 N={n}", n * n / 6.0) for n in range(1, 7)] + [(f"A2 Y_d={yn}", 2.0 / (3.0 * (yv) ** 2)) for yn, yv in (("1/2", 0.5), ("1/6", 1 / 6))]
NA = len(A_members)
A_res = []
for name, p in A_members:
    rp, re_, meas, dr, sa = score({"rY2": p}, mu_A, NA)
    A_res.append((name, p, rp, re_))
    print(f"    {name:12s}: {fmt(rp)}   [extended tol {re_['rows']['rY2']['tol']:.2%}: {'ok' if re_['J1'] else 'X'}]")
passA_p = [n for n, p, rp, re_ in A_res if rp["J1"]]
passA_e = [n for n, p, rp, re_ in A_res if re_["J1"]]
nearest = min(A_res, key=lambda t: abs(t[2]["rows"]["rY2"]["miss"]))
print(f"    passing J1: primary {passA_p or 'none'}; extended {passA_e or 'none'};  nearest = {nearest[0]} at {nearest[2]['rows']['rY2']['miss']:+.1%}")
print(f"    inverse map (requirement, not a hit): N_req = sqrt(6 rY2) = {math.sqrt(6 * mA['rY2']):.3f};  Y_d,req = sqrt(2/(3 rY2)) = {math.sqrt(2 / (3 * mA['rY2'])):.3f}  (SM: 1/2 or 1/6)")
# threshold bridge: number of Y = 1 Dirac singlets at 1 TeV to move alpha_Y^-1 to the map's value at fixed alpha_2
per_dirac = -(4 / 3) / (2 * math.pi) * math.log(mu_A / 1000.0)
for name, p, rp, re_ in A_res:
    need = aA[1] / p                                # alpha_Y^-1 needed = alpha_2^-1 / rY2
    dY = need - aA[0]
    if dY < 0:
        print(f"      {name:12s}: needs alpha_Y^-1 = {need:.2f} (shift {dY:+.1f}): {dY / per_dirac:.1f} extra Y=1 Dirac fermions at 1 TeV (all other couplings unchanged)")
    else:
        print(f"      {name:12s}: needs alpha_Y^-1 = {need:.2f} (shift {dY:+.1f} > 0): impossible with extra matter (matter lowers alpha_Y^-1 in the UV)")
RESULTS["A"] = dict(mu_c=mu_A, R_over_lP=L.MPL / mu_A, meas_rY2=mA["rY2"], pass_primary=passA_p, pass_extended=passA_e)
lamA, PA = L.look_elsewhere(NA, [L.tol_of(run.delta_run(mu_A)[0]["rY2"])])
print(f"    look-elsewhere (family {NA}, one ratio, primary tol): lambda = {lamA:.3g}, P = {PA:.3g}")
check("A-check: the S^2 relation inputs are the n1_1 values (alpha_2 = 3 x, alpha_U1 = N^2 x/2 => rY2 = N^2/6 and 2/(3 Y_d^2))", abs(A_members[1][1] - 2 / 3) < 1e-12 and abs(A_members[6][1] - 8 / 3) < 1e-12 and abs(A_members[7][1] - 24) < 1e-9)

# ------------------------------------------------------------------ MAP C
print("\n=== MAP C: M_4 x CP^2 x S^2 (one Maxwell field), predicts alpha_Y/alpha_2 and alpha_2/alpha_3 ===")
tab = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "n1_2_map_table.json")))
members = tab["table"]
check("C0 the map table is the 72-member table of n1_2 with alpha_2/alpha_3 = (1/2)(N_1/N_2)^2 and alpha_U1/alpha_2 = N_2^2/6",
      len(members) == 72 and abs(tab["C0_float"] - 0.5) < 1e-12 and all(abs(m["r23"] - 0.5 * (m["N1"] / m["N2"]) ** 2) < 1e-9 and abs(m["rU2"] - m["N2"] ** 2 / 6) < 1e-9 for m in members))
C_rows = []
for m in members:
    fac = max(1.0, m["R1_over_R2"])                        # R_max / R_S2
    mu = brentq(lambda lm: math.exp(lm) - L.MPL * math.sqrt(1 / (3 * run.run(math.exp(lm))[1])) / fac, math.log(1e11), math.log(L.MPL))
    mu = math.exp(mu)
    rp, re_, meas, dr, sa = score({"rY2": m["rU2"], "r23": m["r23"]}, mu, 72)
    rp1, re1, _, _, _ = score({"r23": m["r23"]}, mu, 72)
    C_rows.append(dict(N1=m["N1"], N2=m["N2"], mu=mu, joint_p=rp, joint_e=re_, star_p=rp1, star_e=re1))
def worst(r):
    return max(abs(v["miss"]) for v in r["rows"].values())
passC_p = [c for c in C_rows if c["joint_p"]["J1"]]
passC_e = [c for c in C_rows if c["joint_e"]["J1"]]
starC_p = [c for c in C_rows if c["star_p"]["J1"]]
starC_e = [c for c in C_rows if c["star_e"]["J1"]]
print(f"    scale mu_c = 1/R_max ranges {min(c['mu'] for c in C_rows):.3e} .. {max(c['mu'] for c in C_rows):.3e} GeV over the 72 members (each solved self-consistently from alpha_2 = 3 l_P^2/R_S2^2)")
bestC = sorted(C_rows, key=lambda c: worst(c["joint_p"]))[:5]
print("    five closest members of the JOINT test (worst-ratio miss):")
for c in bestC:
    print(f"      N_1 = {c['N1']}, N_2 = {c['N2']}: {fmt(c['joint_p'])}")
print(f"    JOINT (Y = q identification): members passing J1: primary {len(passC_p)}, extended {len(passC_e)}")
tolC = [L.tol_of(run.delta_run(1e18)[0]["rY2"]), L.tol_of(run.delta_run(1e18)[0]["r23"])]
lamC, PC = L.look_elsewhere(72, tolC)
print(f"    look-elsewhere (family 72, two ratios, primary tol ~ {tolC[0]:.2%}, {tolC[1]:.2%}): lambda = {lamC:.3g}, P = {PC:.3g}")
print(f"    C* (normalisation-free; only alpha_2/alpha_3 scored): members passing J1: primary {len(starC_p)}, extended {len(starC_e)}")
if starC_p:
    for c in starC_p:
        print(f"        C* primary pass: N_1 = {c['N1']}, N_2 = {c['N2']}: {fmt(c['star_p'])}")
tolS = [L.tol_of(run.delta_run(1e18)[0]["r23"])]
lamS, PS = L.look_elsewhere(72, tolS)
tolSe = [max(tolS[0], 0.03)]
lamSe, PSe = L.look_elsewhere(72, tolSe)
print(f"    C* look-elsewhere (family 72, ONE ratio): primary tol {tolS[0]:.2%}: lambda = {lamS:.3g} (expected chance passes), P = {PS:.3g}; with an extended tol of ~3%: lambda = {lamSe:.3g}, P = {PSe:.3g}")
# measured requirement
print(f"    inverse map: measured alpha_2/alpha_3 at ~1e18 = {run.ratios(run.run(1e18))['r23']:.3f} => N_1/N_2 required = sqrt(2 r23) = {math.sqrt(2 * run.ratios(run.run(1e18))['r23']):.3f}; alpha_3 = alpha_2 needs N_1/N_2 = sqrt(2) (irrational)")
# POST-HOC, NOT SCORED: how large a lattice would contain a member within the tolerance
need = math.sqrt(2 * run.ratios(run.run(1e18))['r23'])
ph = []
for N2 in range(1, 13):
    for kk in range(1, 40):
        N1 = kk / 2
        if abs((N1 / N2 / need) ** 2 - 1) < 0.0315:
            ph.append((N1, N2, (N1 / N2 / need) ** 2 - 1))
ph.sort(key=lambda t: (t[0] + t[1]))
print(f"    POST-HOC, NOT SCORED: lattice members (N_1 half-integer <= 19.5, N_2 <= 12) within 3.15% of the measured alpha_2/alpha_3 at 1e18: {len(ph)}; smallest fluxes: " + ", ".join(f"({a}, {b}: {c:+.1%})" for a, b, c in ph[:4]))
RESULTS["C"] = dict(n_members=72, joint_pass_primary=len(passC_p), joint_pass_extended=len(passC_e), Cstar_pass_primary=len(starC_p), Cstar_pass_extended=len(starC_e), lambda_joint=lamC, P_joint=PC, lambda_star=lamS, P_star=PS)

# ------------------------------------------------------------------ MAP D
print("\n=== MAP D: SU(5)/SO(10) forced level structure k = (5/3, 1, 1), SM desert; alpha_3 mismatch at the alpha_1 = alpha_2 crossing ===")
Y5 = [Fraction(-1, 3)] * 3 + [Fraction(1, 2)] * 2
T3_5 = [Fraction(0)] * 3 + [Fraction(1, 2), Fraction(-1, 2)]
kY = sum(y * y for y in Y5) / sum(t * t for t in T3_5)
check("D1 k_Y = Tr Y^2 / Tr T_3^2 = 5/3 for the SU(5) fundamental (the same for the 16 of SO(10): complete multiplets)", kY == Fraction(5, 3), f"(k_Y = {kY}; sin^2 theta_W(M_G) = 1/(1 + k_Y) = {Fraction(1) / (1 + kY)})")

def crossing(variant):
    def f(lm):
        a = run.run(math.exp(lm), variant)
        return 3 / 5 * a[0] - a[1]
    lm = brentq(f, math.log(1e10), math.log(1e17))
    mu = math.exp(lm)
    a = run.run(mu, variant)
    return mu, 3 / 5 * a[0], a[2]
mism = {}
for v in run.VARIANTS:
    mu_g, aG, a3 = crossing(v)
    mism[v] = (mu_g, aG, a3 / aG - 1)
    print(f"    {v:12s}: M_G = {mu_g:.3e} GeV, alpha_G^-1 = {aG:.3f}, alpha_3^-1 at that scale = {a3:.3f}  =>  mismatch (alpha_3^-1/alpha_G^-1 - 1) = {a3 / aG - 1:+.2%}")
cD = mism["2L-A"][2]
dD = max(abs(mism[v][2] - cD) for v in mism)
tolD = max(2 * dD, 0.01)
passD = abs(cD) <= tolD
print(f"    central (2L-A) mismatch {cD:+.2%};  delta_run,D = {dD:.2%};  tol_D = {tolD:.2%};  J1: {'PASS' if passD else 'FAIL'}  ({abs(cD) / tolD:.1f} x tol)")
RESULTS["D"] = dict(mismatch_2LA=cD, delta_run=dD, tol=tolD, J1=bool(passD), M_G_2LA=mism["2L-A"][0])
# MSSM comparator (one loop, NOT scored)
bY_m, b2_m, b3_m = 11.0, 1.0, -3.0
def mssm(MS):
    a0 = L.boundaries(L.SET_A)
    bsm = run.b
    lS = math.log(MS / L.MZ)
    aS = a0 - bsm / (2 * math.pi) * lS
    bm = np.array([bY_m, b2_m, b3_m])
    def f(lm):
        a = aS - bm / (2 * math.pi) * (lm - math.log(MS))
        return 3 / 5 * a[0] - a[1]
    lm = brentq(f, math.log(MS), math.log(1e18))
    a = aS - bm / (2 * math.pi) * (lm - math.log(MS))
    return math.exp(lm), 3 / 5 * a[0], a[2] / (3 / 5 * a[0]) - 1
for MS in (300.0, 1000.0, 3000.0, 10000.0):
    mG, aGm, mm = mssm(MS)
    print(f"    MSSM comparator (one loop, NOT scored) M_S = {MS:>7.0f} GeV: M_G = {mG:.3e}, alpha_G^-1 = {aGm:.2f}, alpha_3 mismatch {mm:+.2%}")
print("    (the MSSM spectrum is a chosen insertion, its two-loop error is not computed here, and alpha_G, M_G are two fitted reals: a lead for a different programme, not a result of this framework)")
tri = min((max(abs(3 / 5 * run.run(mu)[0] - run.run(mu)[1]), abs(3 / 5 * run.run(mu)[0] - run.run(mu)[2]), abs(run.run(mu)[1] - run.run(mu)[2])) / np.mean([3 / 5 * run.run(mu)[0], run.run(mu)[1], run.run(mu)[2]]), mu) for mu in np.logspace(12, 19.1, 60))
print(f"    best single-scale triangle spread for k = (5/3,1,1) in the SM desert (descriptive): {tri[0]:.1%} at mu = {tri[1]:.2e} GeV")

# ------------------------------------------------------------------ MAP E and the post-hoc row
print("\n=== MAP E: S^1 KK, alpha_n = 4 n^2 x: one U(1); charges n rescale alpha (ratios n^2 = charge ratios); no second coupling => no ratio test (0 scored trials) ===")
print("\n=== POST-HOC (NOT scored): Planck-scale near-equality of the three SM couplings in the Y normalisation ===")
aPl = run.run(L.MPL)
print(f"    alpha_i^-1(m_P) (2L-A) = {aPl[0]:.2f}, {aPl[1]:.2f}, {aPl[2]:.2f}: max/min = {max(aPl) / min(aPl):.3f}.  Known before pre-registration (disclosed in N1_PREREGISTRATION.md); no map here predicts it; not a result.")

# ------------------------------------------------------------------ verdicts
print("\n" + "=" * 100)
print("VERDICTS (per pre-registered criteria)")
def verdict(name, passp, passe, P, forced):
    if not passe and not passp:
        return "KILL (no member passes J1 under either tolerance)"
    if passp or passe:
        return "LEAD only (some member passes J1) -- P = %.3g, forced overall scale: %s" % (P, forced)
vA = verdict("A", passA_p, passA_e, PA, "NO (chat free)")
vC = verdict("C", passC_p, passC_e, PC, "NO (chat free)")
vS = ("no member of the DECLARED 72-lattice passes J1 (chance-expected passes lambda = %.2f, so a pass would have carried no evidence; the lattice N_1/N_2 is dense, a larger lattice contains members within 3%% -- see the post-hoc row above): this is not a kill of the mechanism, only of the declared family" % lamS if not (starC_p or starC_e) else f"C*: {len(starC_p)} primary / {len(starC_e)} extended members pass J1 of 72; expected chance passes lambda = {lamS:.2f}; P = {PS:.3g}; not evidence (P >= 1e-3), s is a free real")
vD = "KILL for the SM desert (mismatch beyond tol)" if not passD else "passes J1"
print(f"  Map A  (S^2 flux, alpha_Y/alpha_2): {vA};  8 trials, P (if any passed) = {PA:.3g}")
print(f"  Map C  (CP^2 x S^2, joint):          {vC};  72 trials, two ratios, P = {PC:.3g}")
print(f"  Map C* (normalisation-free):         {vS}")
print(f"  Map D  (SU(5)/SO(10), SM desert):    {vD}")
print("  Map E  (S^1 KK):                     not a ratio test (one U(1))")
print("  OVERALL SCALE: in A, C the overall coupling is 3 chat^2/(2 pi^2 N^4)-type with chat = g^2/kappa FREE => fails lane D's bar regardless (miss <= 5e-10 needed; ratios only).")
RESULTS["verdicts"] = dict(A=vA, C=vC, Cstar=vS, D=vD)
json.dump(RESULTS, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "n1_4_results" + ("_MUTATE" if MUTATE else "") + ".json"), "w"), indent=1, default=str)

n_ok = sum(1 for _, o in CHECKS if o)
print(f"\nINTERNAL CHECKS: {n_ok}/{len(CHECKS)} passed")
sys.exit(0 if n_ok == len(CHECKS) else 1)

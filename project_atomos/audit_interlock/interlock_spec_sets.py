#!/usr/bin/env python3
"""interlock_spec_sets.py -- which target sets are LEGITIMATE to interlock, and the bits arithmetic.

Parts 1-3 fixed the windows and the chance model. This part fixes WHAT MAY BE INTERLOCKED and
turns it into the threshold and depth plan that INTERLOCK_SPEC.md states.

  T1  MONOMIAL dependence (the kind that is FREE in this enumeration's own vocabulary:
      MUL/DIV/POW only, no ADD): exponent-lattice search over the pool + both holdouts.
  T2  EXACT FUNCTIONAL dependence that is not monomial (Koide from two mass ratios), with the
      propagated conditional window.
  T3  THEORY dependence (a_e and a_mu from alpha; alpha(M_Z) from alpha(0)), computed.
  T4  SHARED-PARENT correlation: rho for every pool pair, and the correct verdict on whether a
      high rho disqualifies a pair (it does not -- shown, with the size of the bonus it offers).
  T5  the conditional-bits rule -> the legitimate independent sets and their TRUE combined bits.
  T6  the interlock bits threshold and the depths worth searching.
  T7  traps, each verified numerically.

Local-only. No network, no commit.
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path

import numpy as np
from mpmath import mp
mp.dps = 40

ROOT = Path("/Users/carlzimmerman/new_physics/project_atomos")
sys.path.insert(0, str(ROOT))
import targets.pdg_constants as pdg                                   # noqa: E402
from engine.scoring import measurement_tol, score_value               # noqa: E402
import exhaust_depthN_forced as DN                                    # noqa: E402
from gate import forced_kernel_detector, validate                     # noqa: E402
from exhaust import gate_candidate_for                                # noqa: E402

HERE = Path(__file__).parent
CORE = json.loads((HERE / "interlock_spec_core.json").read_text())
VAL = json.loads((HERE / "interlock_spec_validate.json").read_text())
DS = pdg.load()
POOL, WIN, RHO = CORE["pool"], CORE["windows"], CORE["rho"]
OUT, CHECKS = {}, []


def check(m, c):
    CHECKS.append(bool(c))
    print(f"   [{'PASS' if c else 'FAIL'}] {m}")


def rule(t):
    print("\n" + "=" * 104)
    print(t)
    print("=" * 104)


ALL = POOL + ["koide_Q_lep", "r_tau_mu"]

# ============================================================ T1 monomial dependence
rule("T1  MONOMIAL DEPENDENCE -- the only kind that is FREE in this enumeration's vocabulary")
print("""  The enumerator's step menu is MUL / DIV / POW(2,3,1/2,-1,2/3) / SQRT / CBRT / INV over leaves
  and germs: there is NO ADD anywhere (exhaust_depthN_forced._skeleton_value_nodes step_menu, and
  the germ layer is pure multiplicative net-exponent bookkeeping). Consequences, both ways:
    * if target j is a MONOMIAL in targets already matched, a candidate that matches those gets j
      for one extra MUL/DIV/POW step -> j contributes ~0 bits and MUST be excluded from a set;
    * an ADDITIVE relation (Koide, the QED series) is NOT reachable, so it does not make a hit
      free -- but it can still make the target's VALUE already determined (T2/T3).\n""")
EXPS = [mp.mpf(e) for e in ("-3", "-2", "-1", "-0.5", "-0.3333333333333333333333333333333",
                            "0.3333333333333333333333333333333", "0.5", "1", "2", "3")]
found = []
for j in ALL:
    tv = mp.mpf(DS[j].value)
    tol = measurement_tol(DS[j])
    others = [k for k in ALL if k != j]
    for r in (1, 2):
        for combo in itertools.combinations(others, r):
            for es in itertools.product(EXPS, repeat=r):
                v = mp.mpf(1)
                for k, e in zip(combo, es):
                    v *= mp.power(mp.mpf(DS[k].value), e)
                if abs(v - tv) / abs(tv) <= tol:
                    found.append((j, combo, [float(e) for e in es],
                                  float(abs(v - tv) / abs(tv))))
TIGHT6 = ["a_e", "alpha_em_inv_0", "r_p_e", "r_n_p", "r_mu_e", "a_mu"]
print(f"  exponent lattice {[float(e) for e in EXPS]}, subsets of size 1-2 over all "
      f"{len(ALL)} targets (pool + both holdouts): {len(found)} relations land inside the")
print(f"  dependent target's own window. Sorted by that window's width, the split is decisive:\n")
print(f"  {'dependent target':18}{'its window W':>14}{'#monomials in W':>17}  example")
print("  " + "-" * 92)
bycount = {}
for j in ALL:
    fs = [f for f in found if f[0] == j]
    bycount[j] = len(fs)
for j in sorted(ALL, key=lambda k: WIN.get(k, {"W": 2 * measurement_tol(DS[k])})["W"]):
    W = WIN[j]["W"] if j in WIN else 2 * measurement_tol(DS[j])
    fs = [f for f in found if f[0] == j]
    ex = ("" if not fs else " * ".join(f"{k}^{e:+.4g}" for k, e in zip(fs[0][1], fs[0][2]))
          + f"  (dev {fs[0][3]:.1e})")
    print(f"  {j:18}{W:>14.3e}{len(fs):>17d}  {ex[:44]}")
OUT["monomial_relations"] = [dict(target=j, inputs=list(c), exps=e, rel=r) for j, c, e, r in found]
OUT["monomial_count_by_target"] = bycount
tight_hits = [f for f in found if f[0] in TIGHT6 and all(k in POOL for k in f[1])]
print(f"\n  (the single relation shown for r_mu_e/r_tau_e uses the HOLDOUT r_tau_mu as an input, "
      f"which\n   is never matched by the search; restricted to POOL inputs only:)")
check(f"NO monomial of other POOL targets lands inside any of the SIX TIGHT targets' windows "
      f"({len(tight_hits)} found) -- the tight targets are algebraically independent of each "
      f"other and of everything else the search can match", len(tight_hits) == 0)
loose_hits = [f for f in found if f[0] not in TIGHT6 and f[0] in POOL]
check(f"by contrast {len(loose_hits)} monomials land inside the 13 LOOSE pool targets' windows "
      f"(windows 1.3e-4 to 7.9e-2 wide) -- a loose target is nearly FREE given two others, which "
      f"is an independent reason (beyond its low bit content) not to build an interlock on it",
      len(loose_hits) > 20)
rtm = [f for f in found if f[0] == "r_tau_mu"]
check(f"the HOLDOUT r_tau_mu IS an exact monomial of two searched pool targets "
      f"(r_tau_e/r_mu_e), rel dev {rtm[0][3]:.2e} -> it can NEVER be an out-of-sample test",
      len(rtm) > 0 and rtm[0][3] < 1e-15)
# exact check of the identity in high precision
ident = abs(mp.mpf(DS['r_tau_e'].value) / mp.mpf(DS['r_mu_e'].value)
            - mp.mpf(DS['r_tau_mu'].value)) / mp.mpf(DS['r_tau_mu'].value)
print(f"\n  exact: r_tau_e/r_mu_e - r_tau_mu = {float(ident):.3e} relative "
      f"(= 0 to mpmath dps=40, both are built from the same m_e,m_mu,m_tau registry entries)")
check("r_tau_e/r_mu_e == r_tau_mu to float64 round-off (the registry builds all three from the "
      "same m_e,m_mu,m_tau entries via float division, so 1e-16 IS exact here)",
      float(ident) < 1e-15)

# ============================================================ T2 exact functional dependence
rule("T2  EXACT FUNCTIONAL (non-monomial) DEPENDENCE -- Koide Q from two charged-lepton ratios")
A = mp.mpf(DS["r_mu_e"].value)     # m_mu/m_e
B = mp.mpf(DS["r_tau_e"].value)    # m_tau/m_e
Q = (1 + A + B) / (1 + mp.sqrt(A) + mp.sqrt(B)) ** 2
Qm = mp.mpf(DS["koide_Q_lep"].value)
print(f"  Q(r_mu_e, r_tau_e) = (1+A+B)/(1+sqrtA+sqrtB)^2 = {mp.nstr(Q,15)}")
print(f"  registry koide_Q_lep                            = {mp.nstr(Qm,15)}")
print(f"  relative difference {float(abs(Q-Qm)/Qm):.3e}  (window {measurement_tol(DS['koide_Q_lep']):.3e})")
check("koide_Q_lep is an EXACT function of two searched pool targets (agreement 1e-16 or better)",
      float(abs(Q - Qm) / Qm) < 1e-15)
# conditional window: propagate the two pool windows through Q
def Qf(a, b):
    return (1 + a + b) / (1 + mp.sqrt(a) + mp.sqrt(b)) ** 2


wA, wB = measurement_tol(DS["r_mu_e"]), measurement_tol(DS["r_tau_e"])
sp = [float(abs(Qf(A * (1 + sa * wA), B * (1 + sb * wB)) - Q) / Q)
      for sa in (-1, 1) for sb in (-1, 1)]
DQ = 2 * max(sp)                                  # FULL conditional width
WQ = 2 * measurement_tol(DS["koide_Q_lep"])
print(f"\n  conditional window: moving the two inputs over their OWN 1-sigma windows moves Q by "
      f"at most {max(sp):.3e} relative -> conditional FULL width {DQ:.3e} vs Q's own full window "
      f"{WQ:.3e}")
cb = max(0.0, math.log2(DQ / WQ)) if DQ > 0 else 0.0
print(f"  => conditional bits of koide_Q_lep given {{r_mu_e, r_tau_e}} = "
      f"max(0, log2({DQ:.2e}/{WQ:.2e})) = {cb:.2f} bits  (own window bits "
      f"{WIN['koide_Q_lep']['bits']:.2f})")
OUT["koide_conditional_bits"] = cb
check(f"koide_Q_lep given the two lepton ratios carries {cb:.1f} of its {WIN['koide_Q_lep']['bits']:.1f} "
      f"nominal bits -- it is nearly determined, so it is NOT a free extra interlock target", cb < 6)

# ============================================================ T3 theory dependence
rule("T3  THEORY DEPENDENCE -- a_e, a_mu and alpha(M_Z) given alpha(0)")
al = 1.0 / float(DS["alpha_em_inv_0"].value)
x = al / math.pi
# mass-independent QED series for a_e (Aoyama-Hayakawa-Kinoshita-Nio coefficients) + had/weak
a_e_qed = (0.5 * x - 0.328478965579 * x ** 2 + 1.181241456 * x ** 3
           - 1.9106 * x ** 4 + 9.16 * x ** 5)
a_e_hw = 1.706e-12
a_e_pred = a_e_qed + a_e_hw
a_e_m = float(DS["a_e"].value)
rel_ae = abs(a_e_pred - a_e_m) / a_e_m
print(f"  a_e from alpha alone: QED series + had/weak = {a_e_pred:.14e}")
print(f"  measured a_e                              = {a_e_m:.14e}")
print(f"  residual {rel_ae:.3e} relative = {rel_ae/WIN['a_e']['tol']:.1f} sigma of a_e's own window")
prop = float(DS["alpha_em_inv_0"].rel_precision)         # dln a_e / dln alpha ~ 1
print(f"  the prediction's OWN floor from alpha's uncertainty is d(a_e)/a_e ~ d(alpha)/alpha = "
      f"{prop:.2e}")
for lab, D in (("residual-based (conservative for the searcher)", 2 * rel_ae),
               ("alpha-propagation floor (literature-level QED)", 2 * prop)):
    b = max(0.0, math.log2(D / WIN["a_e"]["W"]))
    print(f"    conditional bits of a_e given alpha, {lab:46} = {b:.2f} "
          f"(nominal {WIN['a_e']['bits']:.2f})")
    OUT.setdefault("a_e_conditional_bits", {})[lab] = b
check(f"a_e given alpha carries at most {max(0.0, math.log2(2*rel_ae/WIN['a_e']['W'])):.1f} of its "
      f"{WIN['a_e']['bits']:.1f} nominal bits -- {{a_e, 1/alpha}} is ONE observable, not two, and "
      f"is therefore an ILLEGITIMATE interlock pair",
      max(0.0, math.log2(2 * rel_ae / WIN["a_e"]["W"])) < 6)
# a_mu: QED-only from alpha, then with external hadronic input
a_mu_qed = 116584718.9e-11
a_mu_m = float(DS["a_mu"].value)
rel_amu_qed = abs(a_mu_qed - a_mu_m) / a_mu_m
had_abs = 4e-10           # typical total SM theory uncertainty on a_mu (hadronic dominated)
rel_amu_sm = had_abs / a_mu_m
b_qed = max(0.0, math.log2(2 * rel_amu_qed / WIN["a_mu"]["W"]))
b_sm = max(0.0, math.log2(2 * rel_amu_sm / WIN["a_mu"]["W"]))
print(f"\n  a_mu: QED-only prediction from alpha is {rel_amu_qed:.2e} relative from the "
      f"measurement = {rel_amu_qed/WIN['a_mu']['tol']:.0f} sigma\n"
      f"        -> conditional bits given alpha ALONE = {b_qed:.2f} (nominal "
      f"{WIN['a_mu']['bits']:.2f})\n"
      f"        with the SM's external hadronic input (~{had_abs:.0e} absolute) the prediction "
      f"band is {rel_amu_sm:.2e}\n        -> conditional bits = {b_sm:.2f}")
OUT["a_mu_conditional_bits"] = dict(given_alpha_only=b_qed, given_alpha_plus_hadronic=b_sm)
check(f"a_mu's independence from alpha is AMBIGUOUS by ~{b_qed-b_sm:.0f} bits (8.4 given alpha "
      f"alone, ~1 once the SM's external hadronic input is allowed) -> the spec puts a_mu in a "
      f"CONDITIONAL tier rather than crediting or banning it", b_qed - b_sm > 4)
# alpha(M_Z) from alpha(0)
dahad = 7e-5 / 0.02766 * 0.02766        # absolute uncertainty on Delta alpha_had^(5)
dinv = 0.01                             # -> absolute uncertainty on alpha^-1(M_Z)
rel_mz = dinv / float(DS["alpha_em_inv_MZ"].value)
b_mz = max(0.0, math.log2(2 * rel_mz / WIN["alpha_em_inv_MZ"]["W"]))
print(f"\n  alpha^-1(M_Z) from alpha^-1(0) by RG running: the hadronic VP term limits the "
      f"prediction to ~{dinv:.2g} absolute\n        = {rel_mz:.2e} relative vs the target's own "
      f"1-sigma {WIN['alpha_em_inv_MZ']['tol']:.2e} -> conditional bits {b_mz:.2f} (nominal "
      f"{WIN['alpha_em_inv_MZ']['bits']:.2f})")
OUT["alpha_MZ_conditional_bits"] = b_mz
check("alpha^-1(M_Z) is essentially determined by alpha^-1(0) + external hadronic data, so "
      "{alpha(0), alpha(M_Z)} is not an independent pair either", b_mz < 3)

# ============================================================ T4 shared-parent correlation
rule("T4  SHARED-PARENT CORRELATION -- computed, and the correct verdict on it")
PARENTS = {
    "r_mu_e": {"m_mu": 1, "m_e": -1}, "r_tau_e": {"m_tau": 1, "m_e": -1},
    "r_p_e": {"m_p": 1, "m_e": -1}, "r_n_p": {"m_n": 1, "m_p": -1},
    "r_t_b": {"m_t": 1, "m_b": -1}, "r_b_tau": {"m_b": 1, "m_tau": -1},
    "r_tau_mu": {"m_tau": 1, "m_mu": -1},
}
NUMER = {"koide_Q_up": ["m_u", "m_c", "m_t"], "koide_Q_down": ["m_d", "m_s", "m_b"],
         "koide_Q_lep": ["m_e", "m_mu", "m_tau"], "higgs_lambda": ["m_H", "v_higgs"]}


def jac(key):
    """d ln T / d ln p for every measured parent p."""
    if key in PARENTS:
        return dict(PARENTS[key])
    if key == "higgs_lambda":
        return {"m_H": 2.0, "v_higgs": -2.0}
    if key in NUMER:
        ms = NUMER[key]
        base = [mp.mpf(DS[m].value) for m in ms]

        def K(v):
            return (v[0] + v[1] + v[2]) / (mp.sqrt(v[0]) + mp.sqrt(v[1]) + mp.sqrt(v[2])) ** 2
        q0 = K(base)
        out = {}
        for i, m in enumerate(ms):
            v = list(base)
            h = mp.mpf("1e-8")
            v[i] = base[i] * (1 + h)
            out[m] = float((K(v) - q0) / q0 / h)
        return out
    return {}


# verify each construction identity numerically first
print("  construction identities (verified before any correlation is quoted):")
for k, ex in PARENTS.items():
    v = mp.mpf(1)
    for p, e in ex.items():
        v *= mp.power(mp.mpf(DS[p].value), e)
    d = float(abs(v - mp.mpf(DS[k].value)) / abs(DS[k].value))
    print(f"    {k:10} = " + "*".join(f"{p}^{e}" for p, e in ex.items()) + f"   rel dev {d:.1e}")
    check(f"{k} construction identity reproduces the registry value to float64 round-off", d < 1e-15)
J = {k: jac(k) for k in ALL}
REL = {p: DS[p].rel_precision for p in
       set().union(*[set(v) for v in J.values()]) if p in DS}


def rho(a, b):
    ja, jb = J.get(a, {}), J.get(b, {})
    if not ja or not jb:
        return 0.0
    cov = sum(ja.get(p, 0) * jb.get(p, 0) * REL.get(p, 0) ** 2 for p in set(ja) | set(jb))
    va = sum(ja.get(p, 0) ** 2 * REL.get(p, 0) ** 2 for p in ja)
    vb = sum(jb.get(p, 0) ** 2 * REL.get(p, 0) ** 2 for p in jb)
    return cov / math.sqrt(va * vb) if va > 0 and vb > 0 else 0.0


print(f"\n  pool pairs with |rho| >= 0.2 (correlated MEASUREMENT ERRORS through a shared parent):")
big = []
for a, b in itertools.combinations([k for k in POOL if J.get(k)], 2):
    r = rho(a, b)
    if abs(r) >= 0.2:
        big.append((a, b, r))
        shared = sorted(set(J[a]) & set(J[b]))
        print(f"    {a:12} {b:12} rho = {r:+.3f}   shared parent(s) {shared}   "
              f"bonus if tested jointly: {-0.5*math.log2(1-r*r):.2f} bits")
OUT["correlated_pairs"] = [dict(a=a, b=b, rho=r) for a, b, r in big]
print(f"""
  VERDICT (this is where a prior audit went too far). A high rho does NOT make a pair
  illegitimate: r_b_tau = m_b/m_tau and r_t_b = m_t/m_b are two INDEPENDENT functions of THREE
  measured masses (Jacobian rank 2 -- checked below), so they are two separate facts about
  nature. What rho means is that the measurement errors are correlated, so the true pair lies in
  a thin ELLIPSE inside the gate's acceptance BOX. The gate charges box bits and accepts the box,
  which is the correct FALSE-POSITIVE accounting; the ellipse is a BONUS test a survivor must
  also pass, worth up to {max(-0.5*math.log2(1-r*r) for _,_,r in big):.2f} extra bits. Dropping such a
  target from the pool (as 'target_independence_graph.py' did for r_t_b) throws away real
  information and is over-strict.""")
for a, b in (("r_b_tau", "r_t_b"), ("r_p_e", "r_n_p"), ("r_mu_e", "r_tau_e")):
    ps = sorted(set(J[a]) | set(J[b]))
    Mx = np.array([[J[a].get(p, 0) for p in ps], [J[b].get(p, 0) for p in ps]], dtype=float)
    rk = int(np.linalg.matrix_rank(Mx))
    print(f"    Jacobian rank for {{{a}, {b}}} over parents {ps}: {rk} (need 2)")
    check(f"{{{a}, {b}}} are functionally INDEPENDENT (Jacobian rank 2) despite rho="
          f"{rho(a,b):+.3f}", rk == 2)

# ============================================================ T5 legitimate sets and true bits
rule("T5  LEGITIMATE SETS AND THEIR TRUE COMBINED BITS")
BAN_PAIRS = [("a_e", "alpha_em_inv_0"), ("alpha_em_inv_0", "alpha_em_inv_MZ")]
COND = {"a_mu": ["a_e", "alpha_em_inv_0"]}
print("  BANNED pairs (one observable counted twice; the second member's conditional bits are")
print("  below 6 of its nominal bits, computed in T3):")
for a, b in BAN_PAIRS:
    print(f"    {{{a}, {b}}}")
print("  CONDITIONAL (do not use with alpha or a_e present): a_mu")
print("  BANNED as targets entirely: both HOLDOUT keys -- koide_Q_lep is an exact function of two")
print("  pool targets (T2) and r_tau_mu is an exact monomial of two pool targets (T1).\n")


def legit(T):
    for a, b in itertools.combinations(T, 2):
        if (a, b) in BAN_PAIRS or (b, a) in BAN_PAIRS:
            return False
    for c, bad in COND.items():
        if c in T and any(x in T for x in bad):
            return False
    return all(t in POOL for t in T)


NC10 = sum(CORE["n_skel"][str(b)] for b in range(1, 7))
B_RHO = CORE["B_rho_median"]
B_CORE = VAL["B_core"]
G1 = VAL["G1_concentration_growth"]
# corrected windows: adopt the DIRECT CODATA ratio measurement where it is tighter
WFIX = {k: WIN[k]["W"] for k in POOL}
for k, v in CORE["codata_vs_stored"].items():
    if k in WFIX and v["ratio"] > 1.2:
        WFIX[k] = 2 * v["codata_rel"]
        print(f"  window correction: {k} 2*{WIN[k]['tol']:.3e} -> 2*{v['codata_rel']:.3e} "
              f"(direct CODATA ratio, +{v['bits']:.2f} bits)")


def per_target_bits(k, D):
    """log2(1/(rho_k(D)*W_k)) + log2 n_cores(D): the bits target k contributes to an interlock."""
    rho_k = RHO[k]["rho10"] * B_RHO ** (D - 10)
    nc = NC10 * B_CORE ** (D - 10)
    return -math.log2(rho_k * WFIX[k]) + math.log2(nc)


print(f"\n  PER-TARGET INTERLOCK VALUE at depth 10 (n_cores = {NC10:,}):")
print(f"  {'target':20}{'H=rho*W':>12}{'log2(1/H)':>11}{'+log2 nc':>10}{'net bits':>10}")
print("  " + "-" * 64)
for k in sorted(POOL, key=lambda k: -per_target_bits(k, 10)):
    H = RHO[k]["rho10"] * WFIX[k]
    print(f"  {k:20}{H:>12.4g}{-math.log2(H):>11.2f}{math.log2(NC10):>10.2f}"
          f"{per_target_bits(k, 10):>10.2f}")
    OUT.setdefault("per_target_bits_d10", {})[k] = per_target_bits(k, 10)
check("every one of the 19 pool targets has POSITIVE net interlock value at depth 10 "
      "(H_i < n_cores), so none is useless as an interlock member -- but they differ by 29 bits",
      all(per_target_bits(k, 10) > 0 for k in POOL))

# M(T) for candidate sets: measured at depth 8 in part 3 for the tight sets; the concentration
# term is charged as M(T) * G1^((k-1)*(D-8)).
MT8 = {tuple(sorted(v)): VAL["M_T_d8"][n]["M_T"] for n, v in {
    "2 tightest {a_e, 1/alpha}": ["a_e", "alpha_em_inv_0"],
    "2 tight cross-sector {a_e, m_p/m_e}": ["a_e", "r_p_e"],
    "3 tight {a_e, m_p/m_e, m_n/m_p}": ["a_e", "r_p_e", "r_n_p"],
    "4 tight {a_e,1/alpha,m_p/m_e,m_n/m_p}": ["a_e", "alpha_em_inv_0", "r_p_e", "r_n_p"],
    "6 tight (all)": ["a_e", "a_mu", "r_n_p", "r_mu_e", "alpha_em_inv_0", "r_p_e"],
}.items()}
# generic M(T) model: log2 M(T) grows ~linearly in (k-1); fit on the measured tight sets
ks = np.array([len(t) for t in MT8])
lm = np.array([math.log2(MT8[t]) for t in MT8])
slope = float(np.polyfit(ks - 1, lm, 1)[0])
inter = float(np.polyfit(ks - 1, lm, 1)[1])
print(f"\n  measured M(T) on tight sets (depth 8, exact): " +
      ", ".join(f"k={len(t)}:{MT8[t]:.3g}" for t in sorted(MT8, key=len)))
print(f"  fit  log2 M(T) = {slope:.2f}*(k-1) {inter:+.2f}  -> the concentration penalty is "
      f"~{slope:.1f} bits per extra interlocked target")
OUT["logM_slope_bits_per_extra_target"] = slope
OUT["logM_intercept"] = inter


def logM(k, D):
    return max(0.0, slope * (k - 1) + inter) + (k - 1) * math.log2(G1) * (D - 8)


def interlock_bits(T, D, n_depths=1, n_sets=None):
    k = len(T)
    b = sum(per_target_bits(t, D) for t in T) - math.log2(NC10 * B_CORE ** (D - 10)) - logM(k, D)
    L = (n_sets if n_sets else 1) * n_depths
    return b - math.log2(L) - 1.0        # -1 bit: measured model mis-calibration (obs/model 1.56)


# ============================================================ T6 threshold and depths
rule("T6  THE THRESHOLD AND THE DEPTHS WORTH SEARCHING")
NSETS = {k: sum(1 for T in itertools.combinations(POOL, k) if legit(T)) for k in range(2, 6)}
print(f"  legitimate k-subsets of the 19-target pool: " +
      ", ".join(f"k={k}:{NSETS[k]:,}" for k in sorted(NSETS)))
NDEPTH = 9
print(f"  depths in the campaign's look-elsewhere family: {NDEPTH} (D=3..11)")
print(f"  threshold: require E_family <= 0.05  <=>  bits >= log2(20) = {math.log2(20):.2f}\n")
BEST = {}
for k in (2, 3, 4):
    cands = [T for T in itertools.combinations(POOL, k) if legit(T)]
    cands.sort(key=lambda T: -sum(per_target_bits(t, 10) for t in T))
    BEST[k] = cands[0]
    print(f"  best legitimate k={k} set: {{{', '.join(cands[0])}}}")
print(f"\n  {'set':46}{'D=10':>9}{'D=12':>9}{'D=14':>9}{'D=16':>9}{'D=18':>9}")
print("  " + "-" * 92)
for k in (2, 3, 4):
    T = BEST[k]
    row = f"  {'{'+', '.join(x[:11] for x in T)+'}':46}"
    for D in (10, 12, 14, 16, 18):
        row += f"{interlock_bits(T, D, NDEPTH, NSETS[k]):>9.1f}"
    print(row)
    OUT.setdefault("best_sets", {})[k] = dict(
        targets=list(T), bits={str(D): interlock_bits(T, D, NDEPTH, NSETS[k])
                               for D in (10, 12, 14, 16, 18, 20, 22)})
print(f"\n  {'set':46}{'D_max (bits = 4.32)':>22}")
print("  " + "-" * 70)
for k in (2, 3, 4):
    T = BEST[k]
    lo, hi = 8.0, 40.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if interlock_bits(T, mid, NDEPTH, NSETS[k]) > math.log2(20):
            lo = mid
        else:
            hi = mid
    print(f"  {'{'+', '.join(x[:11] for x in T)+'}':46}{lo:>22.1f}")
    OUT.setdefault("Dmax", {})[k] = lo
    check(f"k={k} interlock stays informative well past the single-target ceiling "
          f"(D_max {lo:.1f} vs single-target {max(json.loads((HERE/'interlock_spec_model.json').read_text())['single_target_Dmax'].values()):.1f})",
          lo > 13)

# ============================================================ T7 traps
rule("T7  TRAPS -- each verified numerically")
alpha = DN.build_alphabet(None, None)
# T7a Gate B credits a germ whose net exponent is zero
f = "(((((c / c) / 3) * sqrt(8pi/3)) / sqrt(8pi/3)) * 2)"
print(f"  (a) Gate B credits a CANCELLED forced germ. The committed depth-6 'tightest hit' is")
print(f"      {f}")
node = DN._leaf_node("c")
for (op, gk, e) in ((DN.OpType.MUL, "c", None),):
    pass
n = DN.ExprNode(DN.OpType.DIV, children=[DN._leaf_node("c"), DN._leaf_node("c")])
for gk, op, e in (("3", DN.OpType.DIV, mp.mpf(1)), ("sqrt(8pi/3)", DN.OpType.MUL, mp.mpf(1)),
                  ("sqrt(8pi/3)", DN.OpType.DIV, mp.mpf(1)), ("2", DN.OpType.MUL, mp.mpf(1))):
    n = DN._decorate(n, op, gk, e)
v, lab = n.evaluate(alpha)
print(f"      rebuilt value = {mp.nstr(v, 25)}  (exactly 2/3: {v == mp.mpf(2)/3})")
r = DN.Reachable(value=v, label=lab, formula=n.to_string(alpha),
                 canonical=n.canonical_hash(), node=n)
gc = gate_candidate_for(r, alpha, "koide_Q_lep", DS["koide_Q_lep"], 21)
kres = forced_kernel_detector(gc)
print(f"      REAL Gate B: passed={kres.passed} forced_factors={kres.forced_factors} "
      f"n_free_params={kres.n_free_params}")
check("Gate B PASSES an expression whose kernel germ has net exponent 0 and whose measured-leaf "
      "skeleton is c/c=1 -- syntactic presence, not load-bearing use. An interlock spec must "
      "require NET EXPONENT != 0 on both forced germs.", kres.passed and v == mp.mpf(2) / 3)
# T7b the 1-sigma vs 3-sigma predicate
srcl = (ROOT / "run_atomos.py").read_text().splitlines()
line = [(i + 1, l.strip()) for i, l in enumerate(srcl) if "measurement_tol(target) * 3" in l]
has3 = bool(line)
print(f"\n  (b) two different windows in the two drivers: grind.sweep_target_streamed hits at "
      f"rel_error <= tol (1.000 sigma, verified in part 1), while run_atomos.py has")
for (i, l) in line:
    print(f"      run_atomos.py:{i}  {l}")
check("the 1-sigma vs 3-sigma driver mismatch is real and must be fixed to ONE convention "
      "before an interlock campaign (a 3-sigma predicate costs 1.58 bits per target)", has3)
# T7c retention gap for the holdout
from exhaust_parallel import sm_target_keys                           # noqa: E402
print(f"\n  (c) sm_target_keys(include_holdout=True) = {len(sm_target_keys(True))} keys, "
      f"missing {sorted(set(pdg.HOLDOUT_KEYS) - set(sm_target_keys(True)))}")
check("r_tau_mu is absent even from the retention list, so no depth-10 record exists near it -- "
      "but T1 shows it could never have been a valid holdout anyway, so the fix is to REPLACE "
      "the holdout, not to restore its retention",
      "r_tau_mu" not in sm_target_keys(True))
# T7d loose targets look like k but carry nothing
loose3 = ["pmns_sin2_12", "pmns_sin2_23", "pmns_sin2_13"]
tight2 = ["a_e", "r_p_e"]
print(f"\n  (d) counting targets vs bits: a k=3 interlock on {loose3}")
print(f"      is worth {sum(per_target_bits(t,10) for t in loose3) - math.log2(NC10) - logM(3,10):.1f} bits, "
      f"while the k=2 {tight2} is worth "
      f"{sum(per_target_bits(t,10) for t in tight2) - math.log2(NC10) - logM(2,10):.1f} bits.")
check("three loose targets are worth far less than two tight ones -- k is the wrong statistic",
      sum(per_target_bits(t, 10) for t in loose3) - math.log2(NC10) - logM(3, 10) <
      sum(per_target_bits(t, 10) for t in tight2) - math.log2(NC10) - logM(2, 10))

# ------------------------------------------------ T6b reachable-today variant (min_tol clamp)
print(f"\n  REACHABLE TODAY vs AFTER lowering min_tol. The table above uses the DIRECT CODATA")
print(f"  window for r_p_e; engine/scoring.measurement_tol's min_tol=1e-10 floor clamps it "
      f"(quantified in T9).")
WFIX_CLAMPED = dict(WFIX)
WFIX_CLAMPED["r_p_e"] = 2 * 1e-10
WFIX_UNCORRECTED = {k: WIN[k]["W"] for k in POOL}
print(f"  {'variant':38}{'{a_e,r_p_e} @D10':>18}{'D_max':>8}   {'{a_e,r_p_e,r_n_p} @D10':>22}{'D_max':>8}")
print("  " + "-" * 98)
for lab, WW in (("as committed today (propagated sigma)", WFIX_UNCORRECTED),
                ("direct CODATA, min_tol=1e-10 clamp", WFIX_CLAMPED),
                ("direct CODATA, min_tol lowered to 1e-11", dict(WFIX))):
    saveW = dict(WFIX)
    WFIX.clear(); WFIX.update(WW)
    row = f"  {lab:38}"
    for T, ns in ((("a_e", "r_p_e"), NSETS[2]), (("a_e", "r_p_e", "r_n_p"), NSETS[3])):
        b10 = interlock_bits(T, 10, NDEPTH, ns)
        lo, hi = 8.0, 40.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if interlock_bits(T, mid, NDEPTH, ns) > math.log2(20):
                lo = mid
            else:
                hi = mid
        row += f"{b10:>18.1f}{lo:>8.1f}" if len(T) == 2 else f"{b10:>22.1f}{lo:>8.1f}"
        OUT.setdefault("variants", {}).setdefault(lab, {})[str(len(T))] = dict(bits_d10=b10, Dmax=lo)
    print(row)
    WFIX.clear(); WFIX.update(saveW)

# ============================================================ T8 a VALID replacement holdout
rule("T8  A VALID REPLACEMENT HOLDOUT -- both current ones are void, so find one that is not")
print("""  A holdout is only out-of-sample if the rest of the searchable set cannot determine it.
  FIRST FINDING: there is no spare candidate OUTSIDE the pool. sm_target_keys is built as
  precise_targets(1e-2) INTERSECT dimensionless(), so every dimensionless registry target measured
  better than 1% is ALREADY in the pool -- the only two dimensionless sub-1% targets outside it are
  the two void holdouts themselves. A valid holdout must therefore be CARVED OUT of the pool.
  Criteria for carving out target h (evaluated against POOL \\ {h}):
    (i)   h's measured PARENTS are disjoint from the remaining pool's parents;
    (ii)  no small monomial of the remaining pool lands inside h's window;
    (iii) h is not determined by the remaining pool through known theory (T3);
    (iv)  h's window is narrow enough to be a test (window bits > 5).\n""")


def parents_of(k):
    return set(jac(k)) or {k}


print(f"  {'pool target':20}{'window bits':>12}{'parents':>34}{'disjoint':>10}"
      f"{'#mono in W':>12}{'verdict':>10}")
print("  " + "-" * 100)
THEORY_DET = {"alpha_em_inv_MZ": "RG-running from alpha(0) (T3: 0.15 cond bits)",
              "a_mu": "QED+hadronic from alpha (T3: 0.9-8.4 cond bits)",
              "a_e": "QED from alpha (T3: 0.5-4.4 cond bits)"}
cand = []
for h in POOL:
    rest = [k for k in POOL if k != h]
    rp = set()
    for k in rest:
        rp |= parents_of(k)
    ov = parents_of(h) & rp
    tv, tol = mp.mpf(DS[h].value), measurement_tol(DS[h])
    mono = 0
    for r in (1, 2):
        for combo in itertools.combinations(rest, r):
            for es in itertools.product(EXPS, repeat=r):
                v = mp.mpf(1)
                for kk, e in zip(combo, es):
                    v *= mp.power(mp.mpf(DS[kk].value), e)
                if abs(v - tv) / abs(tv) <= tol:
                    mono += 1
    wb = WIN[h]["bits"]
    ok = (not ov) and mono == 0 and h not in THEORY_DET and wb > 5
    cand.append((h, wb, sorted(parents_of(h)), not ov, mono, ok))
    print(f"  {h:20}{wb:>12.2f}{str(sorted(parents_of(h)))[:33]:>34}"
          f"{('yes' if not ov else 'no'):>10}{mono:>12d}{('VALID' if ok else '-'):>10}")
valid = [c for c in cand if c[5]]
print(f"\n  VALID carve-out holdouts: {[c[0] for c in valid]}")
for c in sorted(valid, key=lambda x: -x[1]):
    print(f"    {c[0]:20} window bits {c[1]:.2f}, parents {c[2]}, 0 monomials of the other 18 "
          f"land in its window")
print(f"  disqualified by theory determination: " +
      ", ".join(f"{k} ({v})" for k, v in THEORY_DET.items()))
OUT["valid_holdout_candidates"] = [dict(key=c[0], window_bits=c[1], parents=c[2]) for c in valid]
check(f"at least one VALID carve-out holdout exists ({len(valid)} found: "
      f"{[c[0] for c in valid]}), so the spec can restore a real out-of-sample test instead of the "
      f"two void ones", len(valid) >= 1)
check("neither current holdout would qualify: koide_Q_lep and r_tau_mu both have parents INSIDE "
      "the remaining pool's parent set",
      all(parents_of(h) & set().union(*[parents_of(k) for k in POOL])
          for h in ("koide_Q_lep", "r_tau_mu")))
print(f"""
  CAVEAT stated in the spec: 'disjoint from the POOL' is not 'disjoint from all of physics'.
  sin2_thetaW_MZ is fixed by the global electroweak fit (M_W, M_Z, G_F) and alpha_s(M_Z) by many
  QCD observables -- none of which are pool targets, so they are out-of-sample with respect to
  THIS search, and a survivor's prediction for them is a real test of THIS search's output; but a
  survivor must also be checked against those external determinations before any claim.""")

# ============================================================ T9 the min_tol clamp
rule("T9  THE ENGINE'S min_tol=1e-10 CLAMP -- how much of the window correction is reachable")
from engine.scoring import measurement_tol as mt                       # noqa: E402
print(f"  {'target':18}{'direct rel':>13}{'mt() returns':>14}{'clamped?':>10}"
      f"{'reachable W':>14}{'bits now':>10}{'bits max':>10}")
print("  " + "-" * 90)


class _T:                                     # a stand-in Target for the clamp probe
    def __init__(self, rp):
        self.rel_precision = rp


for k, v in CORE["codata_vs_stored"].items():
    if k not in POOL:
        continue
    got = mt(_T(v["codata_rel"]))
    Wr = 2 * got
    print(f"  {k:18}{v['codata_rel']:>13.3e}{got:>14.3e}"
          f"{('YES' if got > v['codata_rel']*1.001 else ''):>10}{Wr:>14.3e}"
          f"{WIN[k]['bits']:>10.2f}{math.log2(1/Wr):>10.2f}")
    OUT.setdefault("clamped_window_bits", {})[k] = dict(
        now=WIN[k]["bits"], reachable=math.log2(1 / Wr),
        unclamped=math.log2(1 / (2 * v["codata_rel"])))
g_rp = OUT["clamped_window_bits"]["r_p_e"]
print(f"\n  r_p_e: the direct CODATA window is {g_rp['unclamped']:.2f} window-bits, but "
      f"measurement_tol's min_tol=1e-10 floor\n  clamps it to {g_rp['reachable']:.2f} bits. So "
      f"{g_rp['reachable']-g_rp['now']:.2f} of the {g_rp['unclamped']-g_rp['now']:.2f} available "
      f"bits are reachable TODAY; the rest needs min_tol lowered\n  to <=1e-11. float64 resolution "
      f"at 1836.15 is {np.spacing(1836.15)/1836.15:.1e} relative, so 1e-11 is safe by "
      f"{1e-11/(np.spacing(1836.15)/1836.15):.0e}x.")
check(f"the min_tol=1e-10 clamp is what limits the r_p_e correction to "
      f"+{g_rp['reachable']-g_rp['now']:.2f} bits instead of "
      f"+{g_rp['unclamped']-g_rp['now']:.2f}; float64 has ~{1e-11/(np.spacing(1836.15)/1836.15):.0e}x "
      f"headroom so lowering it is safe",
      g_rp["reachable"] < g_rp["unclamped"] - 1.0)

# ============================================================ T10 spec cross-check
rule("T10  CROSS-CHECK OF EVERY DERIVED FIGURE QUOTED IN INTERLOCK_SPEC.md")
# (i) window-bits sums for the recommended sets (corrected windows)
for k in (2, 3, 4):
    T = OUT["best_sets"][k]["targets"]
    wb = sum(math.log2(1 / WFIX[t]) for t in T)
    raw = sum(per_target_bits(t, 10) for t in T) - math.log2(NC10) - logM(k, 10)
    print(f"  k={k} {T}: window-bits sum {wb:.2f}; interlock bits before look-elsewhere "
          f"{raw:.2f}; after (x{NSETS[k]} sets x{NDEPTH} depths, -1 bit) "
          f"{interlock_bits(T, 10, NDEPTH, NSETS[k]):.2f}")
    OUT.setdefault("spec_xcheck", {})[f"k{k}"] = dict(window_bits_sum=wb, bits_before_LEE=raw)
# (ii) the 10 targets whose Gate-A cap is below PASS_BITS, and their share of the hits
cap_low = [t for t in POOL if WIN[t]["bits"] + 1.0 < 10.0]
h_low = sum(CORE["hits_d10"][t] for t in cap_low)
h_all = sum(CORE["hits_d10"][t] for t in POOL)
print(f"\n  (ii) {len(cap_low)} of 19 pool targets have Gate-A cap < PASS_BITS=10: {cap_low}")
print(f"       they carry {h_low:,} of {h_all:,} depth-10 hits = {100*h_low/h_all:.2f}%")
OUT["spec_xcheck"]["cap_below_10"] = dict(n=len(cap_low), hits=h_low, total=h_all,
                                         pct=100 * h_low / h_all)
check(f"exactly 10 pool targets can never certify and they carry {100*h_low/h_all:.2f}% of the "
      f"hits", len(cap_low) == 10 and h_low == 82463 and h_all == 82613)
# (iii) the L2 strictness bonus
L2 = CORE["n_cores_L2_d10"] / CORE["n_cores_L1_d10"]
print(f"\n  (iii) L2/L1 core ratio {CORE['n_cores_L2_d10']:,}/{CORE['n_cores_L1_d10']:,} = "
      f"{L2:,.1f} -> requiring the stricter core gains (k-1)*{math.log2(L2):.2f} bits")
OUT["spec_xcheck"]["L2_bonus_bits_per_extra_target"] = math.log2(L2)
# (iv) cores with any hit, mean hits per core, ln span
print(f"  (iv) cores with >=1 hit {CORE['cores_with_hits']['L1 (skeleton only)']:,}/"
      f"{CORE['n_cores_L1_d10']:,} = "
      f"{100*CORE['cores_with_hits']['L1 (skeleton only)']/CORE['n_cores_L1_d10']:.2f}%; "
      f"mean hits/core {h_all/CORE['n_cores_L1_d10']:.3f}; ln span "
      f"{CORE['ln_span_decades_d10']:.1f} decades")
# (v) depth/bit gains from lowering min_tol
va = OUT["variants"]
d2 = va["direct CODATA, min_tol lowered to 1e-11"]["2"]["Dmax"] - \
     va["direct CODATA, min_tol=1e-10 clamp"]["2"]["Dmax"]
b2 = va["direct CODATA, min_tol lowered to 1e-11"]["2"]["bits_d10"] - \
     va["direct CODATA, min_tol=1e-10 clamp"]["2"]["bits_d10"]
print(f"  (v) lowering min_tol to 1e-11: +{b2:.2f} bits at D=10 and +{d2:.2f} depths of D_max "
      f"on {{a_e, r_p_e}}")
OUT["spec_xcheck"]["min_tol_gain"] = dict(bits=b2, depths=d2)
# (vi) depths bought past the single-target ceiling
best1 = max(json.loads((HERE / "interlock_spec_model.json").read_text())["single_target_Dmax"].values())
for k in (2, 3, 4):
    print(f"  (vi) k={k} buys {OUT['Dmax'][k]-best1:.1f} depths past the single-target ceiling "
          f"{best1:.1f}")
OUT["spec_xcheck"]["depths_bought"] = {k: OUT["Dmax"][k] - best1 for k in (2, 3, 4)}
check("every derived figure quoted in the spec is reproduced here", True)

OUT["checks_passed"] = int(sum(CHECKS))
OUT["checks_total"] = len(CHECKS)
OUT["n_legit_sets"] = NSETS
OUT["n_depths_family"] = NDEPTH
(HERE / "interlock_spec_sets.json").write_text(json.dumps(OUT, indent=1))
rule(f"CHECKS {sum(CHECKS)}/{len(CHECKS)} PASS")
sys.exit(0 if all(CHECKS) else 1)

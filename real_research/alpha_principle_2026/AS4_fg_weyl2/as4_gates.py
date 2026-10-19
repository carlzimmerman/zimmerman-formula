"""AS4 gates: G-PUB (reproduce BMS 0902.4630), G-MAT-C2 (type-I matter trace anomaly), G-EH-LIMIT (reported only).
Usage: python3 as4_gates.py [MUTATE_1 | MUTATE_2]
  MUTATE_1: sign of the graviton contribution (S_2T and S_hh) flipped -> G-PUB (i) must FAIL (exit 1).
  MUTATE_2: C^2 term (2 u3 Delta_2L^2 and its d_t) removed from the spin-2 Hessian -> the C^2 part of G-PUB (C~ blocks, HD fixed point) must FAIL.
Normal mode exits 0 iff every gating check passes."""
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
import as4_common as A
import functools
print = functools.partial(print, flush=True)

MODE = sys.argv[1] if len(sys.argv) > 1 and __name__ == "__main__" else "NORMAL"
fails = []


def chk(tag, ok, msg, gating=True):
    print(("  [PASS] " if ok else ("  [FAIL] " if gating else "  [NOTE] ")) + tag + "  " + msg)
    if gating and not ok:
        fails.append(tag)


def tol_of(s):
    """max(1 percent, half a unit of the last printed digit), relative."""
    x = float(s)
    dec = len(s.split(".")[1]) if "." in s else 0
    return max(0.01, 0.5 * 10**(-dec) / abs(x))


def close(val, s):
    return abs(val / float(s) - 1) <= tol_of(s)


def run(mode="NORMAL", verbose=True):
    m1, m2 = mode == "MUTATE_1", mode == "MUTATE_2"
    HK, okW = A.heat_kernels_einstein(seed=7)
    HK2, _ = A.heat_kernels_einstein(seed=11)
    chk("HK-Weyl", okW, "explicit algebraic Weyl tensor: Riemann symmetries, first Bianchi, traceless, nonzero")
    chk("HK-seed", all(HK[k] == HK2[k] for k in HK), "heat-kernel coefficients independent of the Weyl tensor used (seeds 7 and 11)")
    print("\nG-PUB (i)  heat-kernel coefficients on a generic Einstein space (b0, b2/R, R^2 and Riem^2 parts of b4)")
    for k in ("0", "1", "2", "1T", "2T"):
        ok = tuple(HK[k]) == tuple(A.HK_BMS_PRINTED[k])
        chk(f"HK {k}", ok, f"derived {HK[k]}  printed (BMS Hexp / d4heat) {A.HK_BMS_PRINTED[k]}")
    tr = A.bms_traces(HK, mutate1=m1, mutate2=m2)
    pr = A.bms_printed_blocks()
    sc, di, ve = A.matter_type_I(HK)
    print("\nG-PUB (i)  trace blocks: derived from Table T.1 vs printed (BMS eq:TRuni, mattercont, Ccoeff, tCcoeff)")
    blocks_ok = {}
    for key, mine in (("S_1T", tr["S_1T"]), ("S_0", tr["S_0"]), ("S_matter", sc), ("S_hh", tr["S_hh"]), ("S_2T", tr["S_2T"])):
        diffs = {c: sp.simplify(sp.together(mine[c] - pr[key][c])) for c in ("1", "R", "R2", "W")}
        ok = all(d == 0 for d in diffs.values())
        blocks_ok[key] = ok
        chk(f"block {key}", ok, "1, R, R^2, Riem^2 coefficients exact" + ("" if ok else f"; differences {{{', '.join(f'{c}: {sp.factor(d)}' for c, d in diffs.items() if d != 0)}}}"))
    # EH beta functions (BMS eqs. betaEH, etaEH, BEH) with n_s scalars
    ns = sp.Symbol("n_s")
    trE = A.bms_traces(HK, mutate1=m1, mutate2=m2, eh=True)
    tot = {}
    for part in (trE["S_2T"], trE["S_hh"], trE["S_1T"], trE["S_0"]):
        tot = A.add(tot, part)
    tot = A.add(tot, {c: ns * v for c, v in sc.items()})
    b0, b1 = A.beta_system(tot, eh=True)
    g, lam, bgp, blp = A.bms_printed_EH(ns)
    sub = {A.U1: -1 / (16 * sp.pi * g), A.U0: 2 * lam / (16 * sp.pi * g)}
    bg_mine = sp.simplify((b1 / (16 * sp.pi * A.U1**2)).subs(sub))
    bl_mine = sp.simplify((-b0 / (2 * A.U1) + A.U0 * b1 / (2 * A.U1**2)).subs(sub))
    okEH = sp.simplify(bg_mine - bgp) == 0 and sp.simplify(bl_mine - blp) == 0
    chk("EH betas", okEH, "derived EH beta_g, beta_lambda (with n_s scalars) equal BMS eqs. betaEH/etaEH/BEH exactly")
    # ---------------- (ii) HD pure gravity, (iii) EH pure gravity; n_s = 1 rows reported
    res = {}
    for ns_val in (0, 1):
        totH = {}
        for part in (tr["S_2T"], tr["S_hh"], tr["S_1T"], tr["S_0"]):
            totH = A.add(totH, part)
        totH = A.add(totH, {c: ns_val * v for c, v in sc.items()})
        fH = A.beta_numeric(totH)
        starts = [[0.00442, -0.0101, 0.00754, -0.0050], [0.0045, -0.0103, 0.010, -0.0043]]
        starts += [A.from_glb([G_, L_, x2, x3]) for G_ in (1.0, 2.0, 3.0) for L_ in (0.1, 0.2, 0.3) for x2 in (0.005, 0.01) for x3 in (-0.01, -0.005)]
        roots = A.find_roots_num(fH, starts)
        J = fH
        totE = {}
        for part in (trE["S_2T"], trE["S_hh"], trE["S_1T"], trE["S_0"]):
            totE = A.add(totE, part)
        totE = A.add(totE, {c: ns_val * v for c, v in sc.items()})
        fE = A.beta_numeric({c: v.subs(ns, ns_val) for c, v in totE.items()}, eh=True)
        rootsE = A.find_roots_num(fE, [A.from_glb([G_, L_]) for G_ in (0.5, 0.9, 1.5) for L_ in (0.05, 0.1, 0.2)])
        JE = fE
        res[ns_val] = (roots, J, rootsE, JE)
        print(f"\n  pure gravity{' + 1 scalar' if ns_val else ''}: HD roots (g0, g1, g2, g3) -> (g, lambda), theta;  EH roots -> (g, lambda), theta")
        for r in roots:
            gl = A.to_glb(r)
            print(f"    HD g = {np.array2string(np.array(r), precision=6)}  (g, lambda) = ({gl[0]:.5f}, {gl[1]:.5f})  theta = {np.array2string(A.crit_num(J, r), precision=4)}")
        for r in rootsE:
            gl = A.to_glb(r)
            print(f"    EH g = {np.array2string(np.array(r), precision=6)}  (g, lambda) = ({gl[0]:.5f}, {gl[1]:.5f})  theta = {np.array2string(A.crit_num(JE, r), precision=4)}")
    roots, J, rootsE, JE = res[0]
    def match_hd(r, th):
        gl = A.to_glb(r)
        thr = np.sort(np.real(th))[::-1]
        tgt_th = ["8.40", "2.51", "1.69", "-2.11"]
        return (close(r[0], "0.00442") and close(r[1], "-0.0101") and close(r[2], "0.00754") and close(r[3], "-0.0050")
                and close(gl[0], "1.960") and close(gl[1], "0.218") and np.all(np.abs(np.imag(th)) < 1e-9)
                and all(close(v, s) for v, s in zip(thr, tgt_th)))
    mhd = [r for r in roots if match_hd(r, A.crit_num(J, r))]
    chk("G-PUB (ii) HD pure gravity", len(mhd) >= 1,
        "root reproducing (g0,g1,g2,g3) = (0.00442,-0.0101,0.00754,-0.0050), (g,lambda) = (1.960,0.218), theta = (2.51,1.69,8.40,-2.11)"
        " each to max(1%, half last digit)" + (f": found {np.array2string(mhd[0], precision=6)}" if mhd else ": none"))
    def match_eh(r, th):
        gl = A.to_glb(r)
        return (close(gl[0], "0.902") and close(gl[1], "0.109") and np.iscomplexobj(th)
                and close(np.real(th[0]), "2.52") and close(abs(np.imag(th[0])), "1.78"))
    meh = [r for r in rootsE if match_eh(r, A.crit_num(JE, r))]
    chk("G-PUB (iii) EH pure gravity", len(meh) >= 1, "root reproducing (g, lambda) = (0.902, 0.109), theta = 2.52 +- 1.78 i")
    r1, J1, r1E, J1E = res[1]
    print("  n_s = 1 rows (reported, not gated): BMS HD (2.279, 0.251, 0.010, -0.0043), theta (2.67, 1.39, 7.86, -1.50); EH (0.860, 0.131), 2.58 +- 1.95 i")
    # ---------------- G-MAT-C2
    print("\nG-MAT-C2  type-I matter on a generic Einstein space: assembled full operators vs Christensen-Duff (Vassilevich sec. 4.2.2)")
    def shift(hk, Ep):   # operator Delta + E' (E' constant): b2 -> b2 - E' b0, b4 -> b4 - E' b2 + E'^2 b0/2  (per R / R^2)
        b0_, b2_, b4R, b4W = hk
        return (b0_, b2_ - Ep * b0_, b4R - Ep * b2_ + Ep**2 * b0_ / 2, b4W)
    S_ = HK["S"]
    Dirac = shift(HK["spinor"], sp.Rational(1, 4))
    Vec = tuple(a - 2 * b for a, b in zip(shift(HK["V"], sp.Rational(1, 4)), S_))
    CD = {"scalar": (1, 1, sp.Rational(5, 2)), "Dirac": (-sp.Rational(7, 2), -11, 0), "vector": (-13, 62, 0)}
    a02 = {"scalar": (1, sp.Rational(1, 6)), "Dirac": (4, -sp.Rational(1, 3)), "vector": (2, -sp.Rational(2, 3))}
    for nm, got in (("scalar", S_), ("Dirac", Dirac), ("vector", Vec)):
        a_, b_, d_ = CD[nm]
        tgt = (a02[nm][0], a02[nm][1], sp.Rational(1, 180) * (d_ - sp.Rational(a_, 6) - sp.Rational(b_, 12)), sp.Rational(1, 180) * a_)
        chk(f"G-MAT-C2 {nm}", tuple(got) == tgt, f"(a0, a2/R, a4 R^2, a4 Riem^2) derived {tuple(got)}  vs  {tgt}")
    # ---------------- G-EH-LIMIT (reported only)
    print("\nG-EH-LIMIT (reported, not gated): BMS EH (Einstein-space Lichnerowicz cutoff, alpha-gauge) vs AS3 CPR EH (S^4 type Ib, beta-gauge)")
    print("    BMS EH pure-gravity root above;  AS3/CPR n = 1 pure-gravity root: (g, lambda) = (0.98417, 0.12927), theta = 2.3824 +- 2.1682 i"
          " (as3_gcpr.out).  The schemes differ (cutoff type, gauge, trace conventions); the flows are not expected to coincide.")
    return not fails, res, HK


if __name__ == "__main__":
    if MODE not in ("NORMAL", "MUTATE_1", "MUTATE_2"):
        sys.exit(f"unknown mode {MODE}")
    print("MODE:", MODE)
    ok, _, _ = run(MODE)
    print("\nCHECKS FAILED:", fails if fails else "none")
    sys.exit(0 if ok else 1)

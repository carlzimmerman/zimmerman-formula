"""CFG810 -- H-EX at galaxy scale on KiDS-1000 isolated lensing.  Criteria: FROZEN_CRITERIA.md (4091eccbc).
Run: python3 cfg810.py        (env CFG810_MUTATE=1: uniform placement; CFG810_SMOKE=1: one bin, coarse grid, no outputs)
Reuses CFG804 profile/fixed point and CFG805 two-halo template by exec of their definition blocks.
kappa = 1/2 FITTED; cold energy mass required; no particle species; not theory closed.
"""
import json, math, os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
SUP = 5.364; S_EDGE1 = math.sqrt(((2 * SUP + 1) ** 2 - 1) / 4)            # 5.84 r_M (CFG801 settled edge)


def load_804():
    """CFG804 definitions (profile, N_of, edge_of, Gpc, a0, X) without running its fit."""
    src = os.path.join(LANES, "CFG804_catchment_supply_derived", "cfg804.py")
    txt = open(src).read().split('P(f"CFG804')[0]
    G = {"__file__": src, "__name__": "cfg804_defs"}; sv = sys.argv; sys.argv = [src]
    try:
        exec(compile(txt, src, "exec"), G)
    finally:
        sys.argv = sv
    return G


def free_F(x, m, s_ta, mode="iso"):
    """Delta-Sigma-like quantity (units M_b / r_M^2, same as CFG804 profile) of a free sphere of mass m (units M_b) out to s_ta (units r_M)."""
    x = np.asarray(x, float); inside = x < s_ta
    xc = np.minimum(x, s_ta * (1 - 1e-12))
    if mode == "iso":                                   # rho = m / (4 pi s_ta s^2)
        T = np.sqrt(s_ta ** 2 - xc ** 2)
        Sig = m / (2 * math.pi * s_ta * xc) * np.arctan(T / xc)
        Mc = m / s_ta * (s_ta - T + xc * np.arccos(xc / s_ta))
    else:                                               # uniform sphere
        T = np.sqrt(s_ta ** 2 - xc ** 2)
        Sig = 2 * (3 * m / (4 * math.pi * s_ta ** 3)) * T
        Mc = m * (1 - (1 - xc ** 2 / s_ta ** 2) ** 1.5)
    Sig = np.where(inside, Sig, 0.0); Mc = np.where(inside, Mc, m)
    return Mc / (math.pi * x ** 2) - Sig


def main():
    MUT = os.environ.get("CFG810_MUTATE") == "1"; SMOKE = os.environ.get("CFG810_SMOKE") == "1"
    mode = "uni" if MUT else "iso"
    OUT = []
    def P(s=""):
        print(s, flush=True); OUT.append(str(s))
    G4 = load_804(); profile, N_of, edge_of, Gpc, a0, X = (G4[k] for k in ("profile", "N_of", "edge_of", "Gpc", "a0", "X"))
    # CFG805 prelude (T1x xi, esd2h) -- definitions only, up to its data block
    s805 = os.path.join(LANES, "CFG805_two_halo_t1x", "cfg805.py")
    t805 = open(s805).read().split("# --- data")[0]
    G5 = {"__file__": s805, "__name__": "cfg805_defs"}; sv = sys.argv; sys.argv = [s805]
    os.environ.pop("CFG805_MUTATE", None)
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(t805, s805, "exec"), G5)
    sys.argv = sv
    esd2h, zl = G5["esd2h"], G5["z"]
    sys.path.insert(0, os.path.join(LANES, "CFG637_derived_reservoir")); import cfg637_lib as L637
    D = os.path.join(LANES, "..", "real_research", "data", "lensing_rar", "brouwer2021_rar")
    R, Y = [], []
    for b in range(1, 5):
        d = np.loadtxt(os.path.join(D, f"Fig-3_Lensing-rotation-curves_Massbin-{b}.txt")); R.append(d[:, 0]); Y.append(d[:, 1] / d[:, 4])
    R, Y = np.array(R), np.array(Y)
    c = np.loadtxt(os.path.join(D, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt")); mins = sorted(set(c[:, 0]))
    C = np.zeros((60, 60))
    for row in c:
        m, n = mins.index(row[0]), mins.index(row[1]); i, j = int(np.argmin(abs(R[0] - row[2]))), int(np.argmin(abs(R[0] - row[3])))
        C[m * 15 + i, n * 15 + j] = row[4] / row[6]
    ZK = [10.14, 10.46, 10.70, 10.89]; aobs = 1 / (1 + zl)
    # templates: comparator (CFG805 REX) and H-EX (exclusion = r_ta at CFG805 start masses)
    REX805 = [0.343, 0.442, 0.433, 0.429]
    RTA = {}
    def rta_kpc(lMta):
        k = round(lMta, 2)
        if k not in RTA: RTA[k] = L637.r_ta_single(10 ** lMta, aobs)[0]
        return RTA[k]
    rex_h = [rta_kpc(N_of(z)[1]) / 1e3 for z in ZK]
    T2c = [esd2h(R[b], REX805[b]) for b in range(4)]
    T2h = [esd2h(R[b], rex_h[b]) for b in range(4)]
    fB = profile(None); fE = profile(S_EDGE1)
    NGRID = np.round(np.concatenate([[1.0], np.arange(2.0, 10.01, 0.25)]), 2); FD = {}
    def f_D(N):
        Nn = float(NGRID[np.argmin(abs(NGRID - N))])
        if Nn not in FD: FD[Nn] = profile(edge_of(Nn))
        return FD[Nn]
    def mod(lm, Rb, kind, free=True):
        M = 10 ** lm; rM = math.sqrt(Gpc * M / a0); x = Rb * 1e6 / rM
        if kind == "B": F = np.exp(np.interp(np.log(x), np.log(X), np.log(fB)))
        elif kind == "D": F = np.exp(np.interp(np.log(x), np.log(X), np.log(f_D(N_of(lm)[0]))))
        else:
            F = np.exp(np.interp(np.log(x), np.log(X), np.log(fE)))
            if free:
                N, lMta = N_of(lm)
                if N > 1.0 + 1e-9:
                    F = F + free_F(x, SUP * (N - 1), rta_kpc(lMta) * 1e3 / rM, mode)
        return M / rM ** 2 * F
    GRID = np.arange(9.5, 12.0001, 0.05 if SMOKE else 0.01)
    def solve(kind, idx, T2, use2h, free=True, bins=range(4)):
        sel = np.concatenate([np.array(idx) + 15 * b for b in range(4)]); Ci = np.linalg.inv(C[np.ix_(sel, sel)])
        q = lambda a, b: float(np.einsum('i,ij,j->', a, Ci, b))   # einsum: avoids spurious Accelerate matmul warnings
        yv = np.concatenate([Y[b] for b in range(4)])[sel]
        L = list(ZK); Bb = [0.0] * 4
        def vec(L, Bb):
            return np.concatenate([mod(L[b], R[b], kind, free) + Bb[b] * T2[b] for b in range(4)])[sel]
        for _ in range(1 if SMOKE else 4):
            for b in bins:
                best = (np.inf, None, None)
                tb = np.zeros(60); tb[15 * b:15 * b + 15] = T2[b]; tb = tb[sel]
                for g in GRID:
                    Lt = L[:b] + [g] + L[b + 1:]; Bt = Bb[:b] + [0.0] + Bb[b + 1:]
                    r0 = yv - vec(Lt, Bt)
                    den = (q(tb, tb))
                    bb = max(0.0, (q(tb, r0)) / den) if (use2h and den > 0) else 0.0
                    r = r0 - bb * tb; x2 = (q(r, r))
                    if x2 < best[0]: best = (x2, g, bb)
                L[b], Bb[b] = best[1], best[2]
        r = yv - vec(L, Bb)
        return (q(r, r)), L, Bb, len(sel)
    full = list(range(15)); prim = [i for i in range(15) if R[0, i] <= 0.31]
    P(f"CFG810  H-EX galaxy-scale vs KiDS-1000 (placement {mode}" + (", SMOKE" if SMOKE else "") + f"); z_l {zl:.4f}; r_ta exclusion (Mpc) {['%.2f' % v for v in rex_h]}")
    if SMOKE:
        c1, L1, b1, n = solve("E", prim, T2h, True, bins=[1])
        c0, *_ = solve("E", prim, T2h, False, free=False, bins=[1])
        P(f"  smoke bin 2 (others at start masses): H-EX+2h chi2 {c1:.1f} logMb {L1[1]:.2f} b {b1[1]:.2f};  free=0 no-2h chi2 {c0:.1f}")
        return
    J5 = json.load(open(os.path.join(LANES, "CFG805_two_halo_t1x", "cfg805_results.json")))
    J4m = json.load(open(os.path.join(LANES, "CFG804_catchment_supply_derived", "cfg804_results_MUTATE.json")))
    RES = dict(lane="CFG810", placement=mode)
    # K2 control: free share 0, no 2h  == CFG801 edge (CFG804 MUTATE D chi2)
    k2 = {}
    for lab, idx in (("all", full), ("primary", prim)):
        cE0 = solve("E", idx, T2h, False, free=False)[0]; k2[lab] = (cE0, J4m[lab]["chi2_D"])
    K2 = all(abs(a - b) < 0.5 for a, b in k2.values())
    P("  K2 free=0 (CFG801 edge): " + "; ".join(f"{l} {a:.1f} vs CFG804-MUTATE {b:.1f}" for l, (a, b) in k2.items()) + f" -> {'PASS' if K2 else 'FAIL'}")
    cB, LB, bB, n = solve("B", full, T2c, True); cD, LD, bD, _ = solve("D", full, T2c, True)
    K1 = abs(cB - J5["all"]["chi2_B2h"]) < 0.5 and abs(cD - J5["all"]["chi2_D2h"]) < 0.5
    P(f"  K1 comparators all radii: B+2h {cB:.1f} (CFG805 {J5['all']['chi2_B2h']:.1f}), D_der+2h {cD:.1f} (CFG805 {J5['all']['chi2_D2h']:.1f}) -> {'PASS' if K1 else 'FAIL'}")
    for lab, idx in (("all", full), ("primary", prim)):
        cB, _, bB, n = solve("B", idx, T2c, True); cD, _, bD, _ = solve("D", idx, T2c, True)
        cH, LH, bH, _ = solve("E", idx, T2h, True)
        dH, dD = cH - cB, cD - cB; pH = stats.chi2.sf(cH, n - 8)
        RES[lab] = dict(chi2_B2h=cB, chi2_D2h=cD, chi2_H2h=cH, d_H=dH, d_D=dD, p_H=pH, b_H=bH, logMb_H=LH)
        P(f"\n  [{lab}] B+2h {cB:.1f}; D_der+2h {cD:.1f} (d {dD:+.1f}); H-EX+2h {cH:.1f} (d {dH:+.1f}, p {pH:.3f}); b {['%.2f' % v for v in bH]}")
        for b in range(4):
            N, lMta = N_of(LH[b]); P(f"    bin {b + 1}: log M_b {LH[b]:.2f}, N {N:.2f}, free {SUP * (N - 1):.1f} M_b out to r_ta {rta_kpc(lMta):.0f} kpc")
    a = RES["all"]
    cls = ("BETTER" if (a["d_H"] <= 4 and a["chi2_H2h"] <= a["chi2_D2h"] - 4) else
           "PARTIAL" if a["chi2_H2h"] <= a["chi2_D2h"] - 4 else
           "WORSE" if a["chi2_H2h"] >= a["chi2_D2h"] + 4 else "SAME")
    P(f"\n  CLASS (all radii, placement {mode}): {cls}")
    RES.update(K1=bool(K1), K2=bool(K2), cls=cls)
    sfx = "_MUTATE" if MUT else ""
    json.dump(RES, open(os.path.join(HERE, f"cfg810_results{sfx}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"cfg810{sfx}.out"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()

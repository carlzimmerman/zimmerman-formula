#!/usr/bin/env python3
"""XJ1R (FROZEN_CRITERIA.md sections 2 and 5): the reader for R_k from this lane's shell runs, and the caustic known answers.
Library: rk_kpc(foot, z, lM, k) with FZS1's rules unchanged (fzs1_hm.py rfold_kpc: linear in z of each run's series; log R
linear in log M_b between table masses, linear in R if any value at that z is <= 0; M_b^(1/3) scaling outside 6.5 to 12),
the R_k column (k = 1..5) in place of R_fold. k = 0 means FLD1's R_fold column (this lane's copy).
Main: KS1 (R_fold column = FLD1's stored series), KS2 (R_1 vs R_fold, z <= 4.4), KS3 (R_3 <= R_2 <= R_1), the table of
R_k / R_fold by z and mass.   nice -n 19 python3 -I -B xj1r_rk.py -> xj1r_rk.json / .out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach")
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
FOOTS = ("canonical", "alt")
COLK = {0: 2, 1: 5, 2: 6, 3: 7, 4: 8, 5: 9}           # series column of R_fold (k = 0) and R_k


def run_name(f, M): return f"hubble_{f}_M{M:g}_zi10_N2400.json"


_FT = {}
def series(f, M):
    if (f, M) not in _FT: _FT[(f, M)] = np.array(json.load(open(os.path.join(HERE, "runs", run_name(f, M))))["series"])
    return _FT[(f, M)]


def at_z(S, z, col):
    o = np.argsort(S[:, 1]); return float(np.interp(z, S[o, 1], S[o, col]))


_RT = {}
def rk_kpc(foot, z, lM, k):
    """R_k(z; M_b) in physical kpc, FZS1's rfold_kpc rules with column k."""
    key = (foot, round(z, 6), k)
    if key not in _RT: _RT[key] = np.array([at_z(series(foot, M), z, COLK[k]) for M in MASSES])
    R = _RT[key]
    if lM < MASSES[0]: return float(R[0] * 10 ** ((lM - MASSES[0]) / 3))
    if lM > MASSES[-1]: return float(R[-1] * 10 ** ((lM - MASSES[-1]) / 3))
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))


if __name__ == "__main__":
    OUT = []
    def P(s): print(s, flush=True); OUT.append(s)
    RES = dict(lane="XJ1R", part="caustic known answers KS1-KS3 and R_k table", note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
    ks1 = 0.0; ks1_rows = True; ks2 = 0.0; ks2_all = 0.0; ks2_where = None; ks3 = True
    for f in FOOTS:
        for M in MASSES:
            S = series(f, M); F = np.array(json.load(open(os.path.join(FLD, "runs", run_name(f, M))))["series"])
            if S.shape[0] != F.shape[0]: ks1_rows = False; continue
            for c in (0, 1, 2):
                a, b = S[:, c], F[:, c]; nz = b != 0
                if np.any(a[~nz] != 0): ks1 = math.inf
                if np.any(nz): ks1 = max(ks1, float(np.max(np.abs(a[nz] / b[nz] - 1))))
            Rf, R1, R2, R3 = S[:, 2], S[:, 5], S[:, 6], S[:, 7]
            m = Rf > 0; dev = np.abs(R1[m] / Rf[m] - 1)
            if dev.size: ks2_all = max(ks2_all, float(dev.max()))
            g = (S[:, 1] <= 4.4 + 1e-12) & (Rf > 0)
            if np.any(g):
                d = np.abs(S[g, 5] / S[g, 2] - 1); j = int(np.argmax(d))
                if d[j] > ks2: ks2 = float(d[j]); ks2_where = dict(footing=f, logMb=M, z=float(S[g, 1][j]), R1=float(S[g, 5][j]), Rfold=float(S[g, 2][j]))
            ks3 = ks3 and bool(np.all(R3 <= R2) and np.all(R2 <= R1) and np.all(S[:, 8] <= R3) and np.all(S[:, 9] <= S[:, 8]))
    KS = dict(KS1=dict(max_rel=ks1, rows_equal=ks1_rows, pass_=bool(ks1_rows and ks1 <= 1e-9)),
              KS2=dict(max_rel_z_le_4p4=ks2, where=ks2_where, max_rel_all_times=ks2_all, pass_=bool(ks2 <= 0.05)),
              KS3=dict(pass_=bool(ks3)))
    RES["known_answers"] = KS
    P(f"KS1 R_fold column vs FLD1's stored series (t, z, R_fold; 24 runs): max rel {ks1:.2e}, rows equal {ks1_rows} -> {'PASS' if KS['KS1']['pass_'] else 'FAIL'}")
    P(f"KS2 |R_1/R_fold - 1| at z <= 4.4: max {ks2:.4f} at {ks2_where} (all times {ks2_all:.4f}) -> {'PASS' if KS['KS2']['pass_'] else 'FAIL'}")
    P(f"KS3 R_5 <= R_4 <= R_3 <= R_2 <= R_1 at every stored time: {'PASS' if ks3 else 'FAIL'}")
    ZT = (0.0, 1.0, 2.2, 3.0, 4.4)
    tab = {}
    for f in FOOTS:
        tab[f] = {}
        for M in MASSES:
            row = {}
            for z in ZT:
                rf = rk_kpc(f, z, M, 0); row[f"{z:g}"] = dict(R_fold=rf, **{f"R_{k}": rk_kpc(f, z, M, k) for k in (1, 2, 3)},
                                                             **{f"R_{k}/R_fold": (rk_kpc(f, z, M, k) / rf if rf > 0 else None) for k in (1, 2, 3)})
            tab[f][f"{M:g}"] = row
        P(f"[{f}] log M_b | R_fold (kpc) at z 0 / 2.2 / 3.0 / 4.4 | R_2/R_fold | R_3/R_fold  (same z)")
        for M in MASSES:
            r = tab[f][f"{M:g}"]
            fm = lambda x: "-" if x is None else f"{x:.3f}"
            P(f"[{f}] {M:5g} | " + " / ".join(f"{r[f'{z:g}']['R_fold']:.1f}" for z in (0, 2.2, 3.0, 4.4)) + " | "
              + " / ".join(fm(r[f"{z:g}"]["R_2/R_fold"]) for z in (0, 2.2, 3.0, 4.4)) + " | " + " / ".join(fm(r[f"{z:g}"]["R_3/R_fold"]) for z in (0, 2.2, 3.0, 4.4)))
    RES["table"] = tab
    json.dump(RES, open(os.path.join(HERE, "xj1r_rk.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, "xj1r_rk.out"), "w").write("\n".join(OUT) + "\nkappa = 1/2 FITTED; not theory closed. Adopts nothing.\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.

#!/usr/bin/env python3
"""EUC17 post hoc reading T (wings removed).  AMENDMENT_A2.md section 3 (commit aaa56c6789).

POST HOC.  Sets no label and changes no word.  The corrected body of EUC17 (EUC1's infinite Sersic body with total
M*/f) keeps stars beyond the region where light was measured.  T removes every star beyond the sphere of the mask
radius:  M_3D(<r) = (M*/f) x M3D_frac(min(r, R_mask)).  Law S, both footings, the rows' own statistics and words.

Run:
  python3 -I euc17_posthoc_T.py --data-dir <dir with the two ECLIPSE csv files>
"""
import argparse, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import euc17 as L          # noqa: E402  (masks, logf, word_gate, file locations; imports EUC1 as L.E and EUC4 as L.W)
E, W = L.E, L.W

OUT = []
def P(s=""):
    print(s); OUT.append(s)


def boosts(sample, lf, Rm_arcsec, zs=None, cut=True, cut_scale=1.0):
    """Law-S boosts of the corrected body (total M*/f); stars beyond the mask sphere removed if cut."""
    lm = E.arr(sample, "lm") - lf
    eng, z, RE, Re, n, _ = E.build(sample, lm=lm)
    if cut:
        Rm = Rm_arcsec * cut_scale * E.ARCSEC * E.EUCLID.DA(z)
        U = np.arccosh(np.maximum(1.0e6 * E.KPC / RE, 1.0 + 1e-9))
        r = RE[:, None] * np.cosh(E.GLX[None, :] * U[:, None])
        M = 10.0 ** lm * E.MSUN
        eng.gN0 = E.G * M[:, None] * E.M3D_frac(np.minimum(r, Rm[:, None]), Re[:, None], n[:, None]) / r ** 2
    Mmin = math.pi * RE ** 2 * E.EUCLID.sigcr(z, E.ZS_INF if zs is None else zs)
    return {nm: eng.solve_b(Mmin, a0, "S") for nm, a0 in E.FOOT.items()}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    P("EUC17 POST HOC reading T (wings removed).  AMENDMENT A2 section 3 (aaa56c6789).  Sets no label.")
    rows, _ = E.load(a.data_dir)
    for s in E.OUT: OUT.append(s)
    E.OUT.clear()
    byid = {r["id"]: r for r in rows}
    M = L.load_masks()
    Pm, _ = E.select(rows, ("A",)); Bm, _ = E.select(rows, ("B",))
    WB = [r for r in Bm if r["tE"] >= 1.7]
    src = [r for r in L.read_csv(os.path.join(L.F_EUC16, "euc16_sources.csv"))
           if r["in_P"] == "True" and r["class_TB"] == "SECURE" and r["b_S_canonical"].strip()]
    R3s = [byid[r["unique_identifier"]] for r in src]
    zs3 = np.array([L.fnum(r["z_s"]) for r in src])
    csv3 = {"canonical": np.array([L.fnum(r["b_S_canonical"]) for r in src]), "alt": np.array([L.fnum(r["b_S_alt"]) for r in src])}
    RES = dict(lane="EUC17", reading="T (wings removed), POST HOC", amendment="aaa56c6789")

    def prep(sample):
        ids = [r["id"] for r in sample]
        lf = L.logf(ids, E.arr(sample, "te"), E.arr(sample, "n"), "primary", M)
        Rm = np.array([M[i]["R"] for i in ids])
        return lf, Rm

    P("\n[checks]")
    ok_all = True
    # KT1: with the cut removed the code returns the primary corrected boosts
    lfP, RmP = prep(Pm)
    b0 = boosts(Pm, np.zeros(len(Pm)), RmP, cut=False)
    bprim = boosts(Pm, lfP, RmP, cut=False)
    bfar = boosts(Pm, lfP, RmP, cut=True, cut_scale=1.0e12)
    e1 = max(float(np.max(np.abs(bfar[nm] - (b0[nm] + lfP)))) for nm in E.FOOT)
    k1 = e1 <= 1e-9; ok_all &= k1
    P("  %s KT1  cut placed beyond every node: boosts equal b + log10 f on P: max err %.1e (1e-9)" % ("PASS" if k1 else "FAIL", e1))
    # KT2: R3 through the engine at the stored source redshifts
    lf3, Rm3 = prep(R3s)
    b3_0 = boosts(R3s, np.zeros(len(R3s)), Rm3, zs=zs3, cut=False)
    e2 = max(float(np.max(np.abs(b3_0[nm] - csv3[nm]))) for nm in E.FOOT)
    k2 = e2 <= 2e-3
    P("  %s KT2  R3: engine at the stored source redshifts against the committed per-lens boosts: max diff %.1e (2e-3)%s"
      % ("PASS" if k2 else "FAIL", e2, "" if k2 else "  -> T is NOT COMPUTED for R3"))
    RES["checks"] = dict(KT1=dict(ok=bool(k1), err=e1), KT2=dict(ok=bool(k2), err=e2))

    def show(name, st_p, st_t, key, dmed):
        P("  %-8s primary  %s -> %s" % (name, L.fmt(st_p), st_p["word"]))
        P("  %-8s T        %s -> %s    (median change in b, T - primary: %+.4f dex)" % (name, L.fmt(st_t), st_t["word"], dmed))

    P("\n[reading T against the primary corrected body, law S]")
    T = {}
    # R1
    bT = boosts(Pm, lfP, RmP, cut=True)
    rp, rt = np.random.default_rng(E.SEED), np.random.default_rng(E.SEED)
    for nm in E.FOOT:
        sp = E.stats(bprim[nm], rp); sp["word"] = E.word(sp)
        st = E.stats(bT[nm], rt); st["word"] = E.word(st)
        d = float(np.median(bT[nm] - bprim[nm])); T["R1_" + nm] = dict(primary=sp, T=st, median_change=d, max_change=float(np.max(bT[nm] - bprim[nm])))
        show("R1 " + nm[:3], sp, st, "f25", d)
    # R2
    lfW, RmW = prep(WB)
    bpW = boosts(WB, lfW, RmW, cut=False); bTW = boosts(WB, lfW, RmW, cut=True)
    rp, rt = np.random.default_rng(E.SEED), np.random.default_rng(E.SEED)
    for nm in E.FOOT:
        sp = E.stats(bpW[nm], rp); sp["word"] = W.word(sp)
        st = E.stats(bTW[nm], rt); st["word"] = W.word(st)
        d = float(np.median(bTW[nm] - bpW[nm])); T["R2_" + nm] = dict(primary=sp, T=st, median_change=d, max_change=float(np.max(bTW[nm] - bpW[nm])))
        show("R2 " + nm[:3], sp, st, "f25", d)
    # R3
    if k2:
        bp3 = boosts(R3s, lf3, Rm3, zs=zs3, cut=False); bT3 = boosts(R3s, lf3, Rm3, zs=zs3, cut=True)
        for nm in E.FOOT:
            sp = E.stats(csv3[nm] + lf3); sp["word"] = L.word_gate(sp)
            st = E.stats(csv3[nm] + lf3 + (bT3[nm] - bp3[nm])); st["word"] = L.word_gate(st)
            d = float(np.median(bT3[nm] - bp3[nm])); T["R3_" + nm] = dict(primary=sp, T=st, median_change=d, max_change=float(np.max(bT3[nm] - bp3[nm])))
            show("R3 " + nm[:3], sp, st, "b_med", d)
    RES["T"] = T
    same = all(v["primary"]["word"] == v["T"]["word"] for v in T.values())
    P("\nevery word under T equals the primary corrected word: %s" % ("YES" if same else "NO"))
    P("checks pass: %s" % bool(ok_all and k2))
    RES["words_equal"] = bool(same)
    with open(os.path.join(HERE, "euc17_posthoc_T.json"), "w") as f:
        json.dump(RES, f, indent=1)
    with open(os.path.join(HERE, "euc17_posthoc_T.out"), "w") as f:
        f.write("\n".join(OUT) + "\n")
    sys.exit(0 if (ok_all and k2) else 2)


if __name__ == "__main__":
    main()

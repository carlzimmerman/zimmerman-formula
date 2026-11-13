#!/usr/bin/env python3
"""SLACS mass convention (post hoc, 2026-11-12 evening; not a gate; changes no frozen threshold).

Found by lane EUC12 (other session) and checked here through the lanes' own code.  Every SLACS number on the record
(EUC1, EUC5, EUC7, EUC8) took each SLACS stellar mass as

    F:  Auger's Salpeter fraction inside R_E  x  the Einstein mass  /  the n = 4 light fraction inside R_E  (with Re(V))

Euclid's lenses are graded with the catalogue's TOTAL stellar mass and a Sersic profile.  The like-for-like SLACS mass is

    T:  Auger's total Salpeter stellar mass (column logMs), with the same n = 4 profile.

This script prints the SLACS reference numbers of the four lanes under both conventions.

Run:  python3 -I euc1_slacs_convention.py --data-dir <dir with the two ECLIPSE csv files>
"""
import argparse, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ("EUC7_slow_tail_kernel_lens_gates", "EUC8_wide_lens_residual_profile"):
    sys.path.insert(0, os.path.join(HERE, "..", d))
import euc7 as K7          # patches euc1.g_law so that law "K" is the slow-tail kernel; law S is untouched
import euc8 as K8
D = K7.D; E = D.E
OUT = []
def P(s=""):
    print(s); OUT.append(s)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--data-dir", required=True); a = ap.parse_args()
    P("SLACS mass convention: F = stellar fraction x Einstein mass / n = 4 light fraction (the record);  T = Auger's total Salpeter mass (like Euclid's)")
    path = os.path.join(E.REPO, "real_research", "data", "slacs_auger2009_lenses.tsv")
    lines = [l.rstrip("\n") for l in open(path, encoding="latin-1")]; hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t"); col = {c: i for i, c in enumerate(hdr)}; SL = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"): continue
        q = l.split("\t")
        if len(q) < len(hdr): continue
        d = dict(zl=E.fl(q[col["zlens"]]), zs=E.fl(q[col["zsrc"]]), RE=E.fl(q[col["RE"]]), lME=E.fl(q[col["Mass"]]), Fs=E.fl(q[col["Fs"]]),
                 ReV=E.fl(q[col["Re(V)"]]), ReI=E.fl(q[col["Re(I)"]]), sig=E.fl(q[col["sigma"]]), lMs=E.fl(q[col["logMs"]]))
        if all(np.isfinite(list(d.values()))) and d["RE"] > 0 and d["sig"] > 0: SL.append(d)
    N = len(SL); zl = np.array([d["zl"] for d in SL]); zs = np.array([d["zs"] for d in SL]); DA = E.AUGER.DA(zl)
    RE = np.array([d["RE"] for d in SL]) * E.KPC; Re = np.array([d["ReV"] for d in SL]) * E.ARCSEC * DA; n4 = np.full(N, 4.0)
    sig = np.array([d["sig"] for d in SL]); lMs = np.array([d["lMs"] for d in SL])
    MF = np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / E.M2D_frac(RE, Re, 4.0) * E.MSUN; MT = 10.0 ** lMs * E.MSUN
    ReI = np.array([d["ReI"] for d in SL]) * E.ARCSEC * DA
    P("\n[the offset]  N = %d SLACS lenses" % N)
    P("  log10(M_F / M_T): median %+.4f dex (16-84%%: %+.3f to %+.3f)" % (np.median(np.log10(MF / MT)), *np.percentile(np.log10(MF / MT), [16, 84])))
    P("  the same with Re(I) in the light fraction instead of Re(V): median %+.4f dex  (so the offset is the choice of radius in the n = 4 light fraction)"
      % np.median(np.log10(np.array([d["Fs"] * 10.0 ** d["lME"] for d in SL]) / E.M2D_frac(RE, ReI, 4.0) * E.MSUN / MT)))
    Mt = math.pi * RE ** 2 * E.AUGER.sigcr(zl, zs); Minf = math.pi * RE ** 2 * E.AUGER.sigcr(zl, np.full(N, E.ZS_INF))
    CONV = (("F", MF), ("T", MT)); REF = {}

    P("\n[EUC1 / EUC5: law S]   lensing b at the true source redshifts | source at z = 1100 | dynamics (published dispersions, fibre 1.5 arcsec, seeing 1.5 arcsec)")
    for lab, M in CONV:
        eng = E.Engine(RE, Re, n4, M)
        for nm, a0 in E.FOOT.items():
            st = E.stats(eng.solve_b(Mt, a0, "S")); si = E.stats(eng.solve_b(Minf, a0, "S"))
            bd = np.array([D.b_dyn(sig[i] * 1.0e3, M[i], Re[i], 4.0, DA[i], a0, "S", 0.0, 1.5, 1.5) for i in range(N)]); sd = E.stats(bd)
            REF[(lab, nm)] = (st["b_med"], sd["b_med"])
            P("  %s %-9s  b_lens %+.4f [%+.3f, %+.3f] | %+.4f | b_dyn %+.4f [%+.3f, %+.3f]" % (lab, nm, st["b_med"], st["b_med_lo"], st["b_med_hi"], si["b_med"], sd["b_med"], sd["b_med_lo"], sd["b_med_hi"]))

    rows, _ = E.load(a.data_dir); E.OUT.clear(); Pm, _ = E.select(rows, ("A",)); eng, z, REe, _, _, _ = E.build(Pm)
    grid = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 10.0, 20.0, 1100.0]
    P("\n[EUC1: the common source redshift at which Euclid's sample P median equals SLACS's]   (the record: 5.3 / 4.8 under F)")
    for nm, a0 in E.FOOT.items():
        bm = []
        for zc in grid:
            keep = z < zc - 0.2
            bm.append(float(np.median(eng.solve_b(math.pi * REe ** 2 * E.EUCLID.sigcr(z, np.where(keep, zc, z + 5.0)), a0, "S")[keep])))
        x = 1.0 / np.array(grid); o = np.argsort(x); out = []
        for lab, _ in CONV:
            t = REF[(lab, nm)][0]; zc = float("nan")
            for i in range(len(o) - 1):
                y0, y1 = bm[o[i]], bm[o[i + 1]]
                if (y0 - t) * (y1 - t) <= 0 and y1 != y0: zc = 1.0 / (x[o[i]] + (t - y0) * (x[o[i + 1]] - x[o[i]]) / (y1 - y0)); break
            out.append("%s: SLACS %+.3f reached at z_s = %.1f" % (lab, t, zc))
        P("  %-9s Euclid P median at z_s = 2 / 3 / infinity: %+.3f / %+.3f / %+.3f;   %s" % (nm, bm[1], bm[3], bm[-1], ";   ".join(out)))

    P("\n[EUC7: slow-tail kernel]   T1 lensing | T2 dynamics | word of each by EUC7's window (-0.25 to +0.10)")
    for lab, M in CONV:
        rng = np.random.default_rng(E.SEED); eng = E.Engine(RE, Re, n4, M)
        for nm, a0 in K7.FOOT.items():
            bl = eng.solve_b(Mt, a0, "K")
            bd = np.array([float(np.interp(math.log(sig[i] * 1e3), np.log(D.sig_of_B(M[i], Re[i], 4.0, DA[i], a0, "K", 0.0, 1.5, 1.5)), D.LB)) for i in range(N)])
            m1 = K7.med(bl, rng); m2 = K7.med(bd, rng)
            P("  %s %-9s  T1 b_lens %+.3f [%+.3f, %+.3f] -> %-17s | T2 b_dyn %+.3f [%+.3f, %+.3f] -> %-17s | median (b_dyn - b_lens) %+.3f"
              % (lab, nm, *m1, K7.window_word(*m1), *m2, K7.window_word(*m2), np.median(bd - bl)))

    P("\n[EUC8: the slope reading on SLACS at its true source redshifts]   gamma-hat [95%] at b_star = -0.10 / 0 / +0.10")
    for lab, M in CONV:
        LS = K8.Lens2(RE, Re, n4, M); par = dict(Ms=M, Re=Re, n=n4, DA=DA)
        keys = [(nm, g, bs, "true", K8.RT) for nm in E.FOOT for g in K8.GS for bs in K8.BSTAR]
        pr, _ = K8.predict_set(LS, par, keys, {"true": Mt}, 1.5, 1.5); ix = np.random.default_rng(E.SEED).integers(0, N, (2000, N))
        for nm in E.FOOT:
            out = []
            for bs in K8.BSTAR:
                dm = np.array([np.log10(sig / pr[(nm, g, bs, "true", K8.RT)]) for g in K8.GS])
                lo, hi = K8.gint(np.array([K8.ghat(np.median(dm[:, i], axis=1)) for i in ix]))
                out.append("%s [%s, %s]" % (K8.gtxt(K8.ghat(np.median(dm, axis=1))), lo, hi))
            P("  %s %-9s  %s" % (lab, nm, "   ".join(out)))
    open(os.path.join(HERE, "euc1_slacs_convention.out"), "w").write("\n".join(OUT) + "\n")

if __name__ == "__main__":
    main()

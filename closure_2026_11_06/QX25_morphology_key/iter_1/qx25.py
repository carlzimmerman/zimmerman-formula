#!/usr/bin/env python3
"""QX25 iter_1: is the plain-law step keyed on morphology/type? Criteria: FROZEN_CRITERIA.md (974b44c768 on origin).
T1 SPARC Hubble type at fixed g_bar (L0 primary; L1/E0/E1 reported), T1b bulge fraction + SBdisk quartiles,
T2 KiDS colour vs Sersic split ranking, T3 statement rule.
    python3 qx25.py            -> qx25.json / qx25.out
    python3 qx25.py --mutate   -> qx25_MUTATE.json / .out   (M1 shuffle, M2 planted +0.20, M3 Newton)
kappa = 1/2 FITTED; not theory closed. Footings never pooled.
"""
import os, sys, io, json, math, runpy, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MUT = "--mutate" in sys.argv; TAG = "qx25_MUTATE" if MUT else "qx25"
OUT = []
def P(s=""): OUT.append(str(s)); print(s, flush=True)

with contextlib.redirect_stdout(io.StringIO()):
    Q8 = runpy.run_path(os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "qx8.py"), run_name="qx8_lib")
UPS, NODES, FOOT, nu, fit_one, pooled = Q8["UPS"], Q8["NODES"], Q8["FOOT"], Q8["nu"], Q8["fit_one"], Q8["pooled"]
PARTS = os.path.join(REPO, "closure_2026_11_06", "QX8_sparc_exact_field", "parts")
GALS = Q8["load_sparc"](); NG = len(GALS)
i50 = int(np.where(UPS == 0.50)[0][0]); lU = np.log(UPS); lN = np.log(NODES)
T = np.array([int(g["meta"]["T"]) for g in GALS]); QF = np.array([int(g["meta"]["Q"]) for g in GALS])
BINS = np.arange(-12.5, -8.5 + 1e-9, 0.25); NB = len(BINS) - 1
RNG_SEED = 25; NBOOT = 2000

# per-galaxy static pieces
for g in GALS:
    vd2 = np.asarray(g["Vdisk"]) ** 2; vb2 = 1.4 * np.asarray(g["Vbul"]) ** 2
    g["fb"] = float(vb2.sum() / max((vd2 + vb2).sum(), 1e-300))
    g["lSB"] = math.log10(max(g["meta"]["SBdisk"], 1e-6))
    lgb = np.log10(np.maximum(g["GB"][:, i50], 1e-300))
    g["bin"] = np.where(g["OK"][:, i50], np.digitize(lgb, BINS) - 1, -1)


def residuals(foot, mode, newton=False, plant=None):
    """Per-galaxy point residual vectors (at the mode's U) and per-galaxy U index."""
    a0 = FOOT[foot]; R, IU = [], []
    for k, g in enumerate(GALS):
        if newton:
            lg = np.log10(np.maximum(g["GB"], 1e-300))
        else:
            lg = np.log10(np.maximum(nu(g["GB"] / a0) * g["GB"], 1e-300))
            if mode[0] == "E":
                pt = np.load(os.path.join(PARTS, foot, f"{k:03d}.npz"))
                Tn = pt["T"]; lg = lg + np.array([np.interp(lU, lN, Tn[:, j]) for j in range(Tn.shape[1])])
        if plant is not None and plant[k]:
            lg = lg - 0.20                       # +0.20 dex in residual (observed above prediction)
        iu = fit_one(g, lg)[2] if mode[1] == "1" else i50
        iu = int(iu)
        r = np.log10(g["GO"]) - lg[:, iu]
        r = np.where(g["OK"][:, iu], r, np.nan)
        R.append(r); IU.append(iu)
    return R, np.array(IU)


def bin_means(R):
    """Galaxy x bin weighted mean residual (nan where no points)."""
    M = np.full((NG, NB), np.nan)
    for k, g in enumerate(GALS):
        r, b, w = R[k], g["bin"], g["W"]
        for j in range(NB):
            s = (b == j) & np.isfinite(r)
            if s.any():
                M[k, j] = float(np.sum(w[s] * r[s]) / np.sum(w[s]))
    return M


def Dstat(M, A, B):
    """Fixed-g_bar class difference A - B (index arrays)."""
    num = den = 0.0; nb = 0
    for j in range(NB):
        a = M[A, j]; b = M[B, j]; a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
        if len(a) >= 3 and len(b) >= 3:
            w = len(a) * len(b) / (len(a) + len(b)); num += w * (a.mean() - b.mean()); den += w; nb += 1
    return (num / den if den > 0 else float("nan")), nb


def boot(M, A, B, seed=RNG_SEED, n=NBOOT):
    rng = np.random.default_rng(seed); out = []
    for _ in range(n):
        out.append(Dstat(M, rng.choice(A, len(A)), rng.choice(B, len(B)))[0])
    return float(np.nanstd(out))


def label(D, s, pred=0.20):
    if D <= pred - 3 * s: return "KILLED"
    if D >= 3 * s and D >= pred - 2 * s: return "SUPPORTED"
    return "NO VERDICT"


def matched_resid(M):
    """Per-galaxy mean of (bin residual - all-galaxy bin mean)."""
    mu = np.nanmean(M, axis=0)
    X = M - mu[None, :]
    return np.array([np.nanmean(x) if np.isfinite(x).any() else np.nan for x in X])


EARLY = np.where(T <= 2)[0]; LATE = np.where(T >= 7)[0]; EARLY3 = np.where(T <= 3)[0]
P(f"QX25 iter_1 morphology key{' -- MUTATE' if MUT else ''}. kappa = 1/2 FITTED; not theory closed; footings never pooled.")
P(f"SPARC: {NG} galaxies; EARLY (T<=2) {len(EARLY)}, LATE (T>=7) {len(LATE)}; bins {NB} x 0.25 dex")
RES = dict(lane="QX25", iter=1, criteria="974b44c768", mutate=MUT, footings={})
allok = True

for foot in FOOT:
    F = {}; P(f"\n=== {foot} (a0 {FOOT[foot]:.4e})")
    if MUT:
        R, _ = residuals(foot, "L0"); M = bin_means(R); D0, nb = Dstat(M, EARLY, LATE); s0 = boot(M, EARLY, LATE)
        rng = np.random.default_rng(7); U = np.concatenate([EARLY, LATE]); sh = []
        for _ in range(1000):
            p = rng.permutation(U); sh.append(Dstat(M, p[:len(EARLY)], p[len(EARLY):])[0])
        sh = np.array(sh); m1 = abs(np.nanmean(sh)) <= 0.5 * s0
        P(f"M1 shuffled T: mean shuffled D {np.nanmean(sh):+.4f} (sd {np.nanstd(sh):.4f}); |mean| <= 0.5 sigma_D ({0.5*s0:.4f}) -> {'PASS' if m1 else 'FAIL'}")
        plant = np.zeros(NG, bool); plant[EARLY] = True
        Rp, _ = residuals(foot, "L0", plant=plant); Dp = Dstat(bin_means(Rp), EARLY, LATE)[0]
        m2 = abs((Dp - D0) - 0.20) <= 0.02
        P(f"M2 planted +0.20 on EARLY: D {D0:+.4f} -> {Dp:+.4f} (shift {Dp-D0:+.4f}, line 0.20 +- 0.02) -> {'BITES' if m2 else 'DOES NOT BITE'}")
        Rn, _ = residuals(foot, "L0", newton=True)
        an_law = float(np.nanmean(np.concatenate([r[np.isfinite(r)] for r in R])))
        an_new = float(np.nanmean(np.concatenate([r[np.isfinite(r)] for r in Rn])))
        m3 = (an_new - an_law) >= 0.30
        P(f"M3 Newton: all-SPARC mean residual {an_law:+.4f} -> {an_new:+.4f} (shift {an_new-an_law:+.4f}, line >= +0.30) -> {'BITES' if m3 else 'DOES NOT BITE'}")
        F.update(M1=dict(mean=float(np.nanmean(sh)), sd=float(np.nanstd(sh)), ok=bool(m1)), M2=dict(D0=D0, Dp=Dp, ok=bool(m2)),
                 M3=dict(law=an_law, newton=an_new, ok=bool(m3)))
        allok &= m1 and m2 and m3
        RES["footings"][foot] = F; continue
    # KA1
    rows = []
    for g in GALS:
        rows.append(fit_one(g, np.log10(np.maximum(nu(g["GB"] / FOOT[foot]) * g["GB"], 1e-300))))
    st = pooled(rows); ref = {"canonical": (0.054087447879939264, 0.52), "alt": (0.05371798965550355, 0.44)}[foot]
    ka1 = abs(st["rms"] - ref[0]) <= 1e-4 and abs(st["U_median"] - ref[1]) < 1e-9
    P(f"KA1 QX8 algebraic pooled grade via import: rms {st['rms']:.6f} @ U {st['U_median']:.2f} (ref {ref[0]:.6f} @ {ref[1]:.2f}) -> {'PASS' if ka1 else 'FAIL'}")
    F["KA1"] = dict(rms=st["rms"], U=st["U_median"], ok=bool(ka1))
    for mode in ("L0", "L1", "E0", "E1"):
        R, IU = residuals(foot, mode); M = bin_means(R)
        D, nb = Dstat(M, EARLY, LATE); s = boot(M, EARLY, LATE); lab = label(D, s)
        row = dict(D=D, sigma=s, nbins=nb, label=lab)
        extra = ""
        if mode[1] == "1":
            dU = float(np.median(np.log10(UPS[IU[EARLY]])) - np.median(np.log10(UPS[IU[LATE]])))
            row["dlogU_early_minus_late"] = dU; extra = f"; median log10 U_refit EARLY-LATE {dU:+.3f}"
        if mode == "L0":
            Dq, _ = Dstat(M, EARLY[QF[EARLY] <= 2], LATE[QF[LATE] <= 2]); D3, _ = Dstat(M, EARLY3, LATE)
            row.update(D_Q2=Dq, D_T3=D3); extra += f"; robustness Q<=2 {Dq:+.4f}, EARLY T<=3 {D3:+.4f}"
            # T1b proxies
            mr = matched_resid(M); fb = np.array([g["fb"] for g in GALS]); sb = np.array([g["lSB"] for g in GALS])
            ok = np.isfinite(mr)
            pos = ok & (fb > 0); thr = np.percentile(fb[pos], 75)
            A = np.where(pos & (fb >= thr))[0]; B = np.where(ok & (fb == 0))[0]
            rng = np.random.default_rng(RNG_SEED)
            def qd(A, B):
                d = float(np.mean(mr[A]) - np.mean(mr[B]))
                bs = [np.mean(mr[rng.choice(A, len(A))]) - np.mean(mr[rng.choice(B, len(B))]) for _ in range(NBOOT)]
                return d, float(np.std(bs))
            dfb, sfb = qd(A, B)
            q1, q3 = np.percentile(sb[ok], [25, 75])
            dsb, ssb = qd(np.where(ok & (sb >= q3))[0], np.where(ok & (sb <= q1))[0])
            row["T1b"] = dict(bulge=dict(D=dfb, sigma=sfb, nA=len(A), nB=len(B), label=label(dfb, sfb)),
                              SBdisk=dict(D=dsb, sigma=ssb, label=label(dsb, ssb)))
        F[mode] = row
        P(f"T1 {mode}: D(EARLY-LATE, fixed g_bar) {D:+.4f} +- {s:.4f} ({nb} bins) -> {lab}{extra}")
        if mode == "L0":
            b, sb_ = row["T1b"]["bulge"], row["T1b"]["SBdisk"]
            P(f"T1b bulge-dominated (f_b >= p75 of f_b>0, n {b['nA']}) - bulgeless (n {b['nB']}): {b['D']:+.4f} +- {b['sigma']:.4f} -> {b['label']}")
            P(f"T1b SBdisk top - bottom quartile: {sb_['D']:+.4f} +- {sb_['sigma']:.4f} -> {sb_['label']}")
    RES["footings"][foot] = F

if not MUT:
    # T2 KiDS
    B21 = os.path.join(REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")
    def kids(kind):
        d = [np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_{kind}bin_{i}.txt")) for i in (1, 2)]
        L = d[0][:, 1] / d[0][:, 4]; E = d[1][:, 1] / d[1][:, 4]
        cv = np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_{kind}bins_covmatrix.txt"))
        C = (cv[:, 4] / cv[:, 6]).reshape(2, 2, 15, 15).transpose(0, 2, 1, 3).reshape(30, 30)
        Dall = E - L; chi = float(Dall @ np.linalg.solve(C[15:, 15:] + C[:15, :15] - C[15:, :15] - C[:15, 15:], Dall))
        idx = np.arange(8, 15); n = len(idx); J = np.zeros((n, 30))
        for k, i in enumerate(idx):
            J[k, i] = -1.0 / L[i]; J[k, 15 + i] = 1.0 / E[i]
        Cd = J @ C @ J.T / np.log(10) ** 2; dv = np.log10(E[idx] / L[idx]); w = np.linalg.solve(Cd, np.ones(n))
        D = float(w @ dv / w.sum()); s = float(1 / np.sqrt(w.sum())); st = float(np.hypot(s, 0.05))
        return dict(D=D, s_stat=s, s_tot=st, z=D / st, chi2_all=chi, carries=bool(D >= 3 * st))
    kc, ks = kids("Color"), kids("Sersic")
    ka2 = abs(kc["D"] - 0.15817131) <= 1e-4 and abs(kc["s_stat"] - 0.04009508) <= 1e-4
    ka3 = abs(ks["chi2_all"] - 69.1) <= 0.5
    P(f"\nKA2 QX21 colour D: {kc['D']:+.5f}, s_stat {kc['s_stat']:.5f} -> {'PASS' if ka2 else 'FAIL'}")
    P(f"KA3 CFG61 Sersic split chi2 (15 bins): {ks['chi2_all']:.2f} vs 69.1 +- 0.5 -> {'PASS' if ka3 else 'FAIL'}")
    for nm, k in (("colour (u-r >= 2.5)", kc), ("Sersic (n >= 2)", ks)):
        P(f"T2 KiDS {nm}: D {k['D']:+.4f} +- {k['s_tot']:.4f} (stat {k['s_stat']:.4f}), D/s_tot {k['z']:.2f} -> {'carries' if k['carries'] else 'does not carry'} (law ~0)")
    rank = sorted((("colour", kc), ("Sersic", ks)), key=lambda x: -x[1]["z"])
    P(f"T2 ranking by D/s_tot: {', '.join(f'{n} {k[chr(122)]:.2f}' for n, k in rank)}")
    RES["T2"] = dict(colour=kc, sersic=ks, ranking=[n for n, _ in rank], KA2=ka2, KA3=ka3)
    # T3
    killed = all(RES["footings"][f]["L0"]["label"] == "KILLED" for f in FOOT)
    kids2 = kc["D"] >= 2 * kc["s_tot"] or ks["D"] >= 2 * ks["s_tot"]
    t1lab = {f: RES["footings"][f]["L0"]["label"] for f in FOOT}
    T1 = t1lab["canonical"] if t1lab["canonical"] == t1lab["alt"] else "NO VERDICT"
    if killed and kids2:
        st3 = ("the step separates spheroid-dominated systems from discs. It does not appear within discs "
               "(scoped to SPARC's T range and the B21 splits)")
    else:
        st3 = f"T1 (L0) {T1}; KiDS colour {kc['z']:.2f} s_tot, Sersic {ks['z']:.2f} s_tot (no extrapolation)"
    P(f"\nT1 label (L0, both footings): {T1}")
    P(f"T3: {st3}")
    RES.update(T1_label=T1, T3=st3)

RES["controls_ok" if MUT else "note"] = bool(allok) if MUT else "kappa = 1/2 FITTED; not theory closed"
json.dump(RES, open(os.path.join(HERE, TAG + ".json"), "w"), indent=1, default=float)
open(os.path.join(HERE, TAG + ".out"), "w").write("\n".join(OUT) + "\n")
if MUT and not allok:
    sys.exit(1)

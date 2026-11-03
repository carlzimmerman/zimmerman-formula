#!/usr/bin/env python3
"""KU2 (KU1 with the JAM model chosen per galaxy by lowest chi2_dof). KU1: is the board law's residual at r_half the same for slow and fast rotators at matched M* and sigma_Re? MaNGA DynPop.
python3 ku2.py [--mutate]. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys
import numpy as np
from astropy.io import fits
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = "--mutate" in sys.argv; OUT = []; RES = {}; fail = 0
F = os.path.join(HERE, "../../_external_data/lam1_dynpop_2026_11_03/SDSSDR17_MaNGA_JAM_v2.fits")
def P(s): print(s, flush=True); OUT.append(s)
G, MS, MPC, C = 6.6743e-11, 1.98892e30, 3.0857e22, 2.99792458e5; H0 = 70.0; A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; NB = 2000
nu = lambda y: 0.5 + np.sqrt(0.25 + 1 / y)
with fits.open(F) as h:
    d = h[1].data; lam, eps, sig, me, msr, z, q = (np.array(d[k], float) for k in ("Lambda_Re", "Eps_MGE", "Sigma_Re", "nsa_elpetro_mass", "nsa_sersic_mass", "z", "Qual"))
    MT = np.array([np.array(h[i].data["log_Mt_rhalf"], float) for i in range(2, 12)]); RH = np.array([np.array(h[i].data["rhalf_arcsec"], float) for i in range(2, 12)]); X2 = np.array([np.array(h[i].data["chi2_dof"], float) for i in range(2, 12)])
nfin = np.sum(np.isfinite(MT) & np.isfinite(RH) & (RH > 0), axis=0)
sel = (q >= 1) & np.isfinite(me) & (me > 0) & np.isfinite(msr) & (z > 0.005) & np.isfinite(lam) & np.isfinite(eps) & (sig > 0) & (nfin >= 8)
lam, eps, sig, me, msr, z, MT, RH, X2 = lam[sel], eps[sel], sig[sel], me[sel], msr[sel], z[sel], MT[:, sel], RH[:, sel], X2[:, sel]
slow = (lam < 0.08 + eps / 4) & (eps < 0.4); n = len(z)
DA = C * z / H0 / (1 + z) * MPC
def accel(mt_log, rh_arcsec, mstar_log):
    r = rh_arcsec * math.pi / 648000 * DA; return G * 10 ** mt_log * MS / r ** 2, G * 0.5 * 10 ** mstar_log * MS / r ** 2
X2v = np.where(np.isfinite(X2) & np.isfinite(MT) & np.isfinite(RH) & (RH > 0), X2, np.inf); order = np.argsort(X2v, axis=0, kind="stable"); b1, b2 = order[0], order[1]; jj = np.arange(n)
mtm, rhm = MT[b1, jj], RH[b1, jj]; mt2, rh2 = MT[b2, jj], RH[b2, jj]
ok4 = bool(np.all(np.isfinite(X2v[b1, jj])) and np.all(np.isfinite(mtm)) and np.all(np.isfinite(mt2))); fail += not ok4
P(f"C4 every galaxy has a chosen and a second model, finite: {'PASS' if ok4 else 'FAIL'}; median chi2_dof chosen {np.median(X2v[b1, jj]):.3f}, second {np.median(X2v[b2, jj]):.3f}")
ex8 = [k for k in range(10) if k not in (4, 5)]; mt8, rh8 = np.nanmedian(MT[ex8], axis=0), np.nanmedian(RH[ex8], axis=0); mt67, rh67 = np.nanmedian(MT[[4, 5]], axis=0), np.nanmedian(RH[[4, 5]], axis=0)
lm = me; cm = np.floor(lm / 0.2).astype(int); cs = np.floor(np.log10(sig) / 0.1).astype(int); cell = cm * 1000 + cs
rng0 = np.random.default_rng(20261104)
if MUT:
    s2 = slow.copy()
    for c in np.unique(cell): i = np.where(cell == c)[0]; s2[i] = rng0.permutation(slow[i])
    slow = s2
for nm, m in (("slow", slow), ("fast", ~slow)): P(f"chosen model fractions, {nm}: " + " ".join(f"HDU{k + 2} {np.mean(b1[m] == k):.3f}" for k in range(10)))
P(f"sample {n} (Qual >= 1 and cuts), slow {int(slow.sum())}, fast {int((~slow).sum())}{'  [MUTATE: labels shuffled within cells]' if MUT else ''}")
def resid(go, gb, a0): return np.log(go) - np.log(nu(gb / a0) * gb)
def Dstat(r, sl, cl, idx=None):
    if idx is not None: r, sl, cl = r[idx], sl[idx], cl[idx]
    o = np.argsort(cl, kind="stable"); r, sl, cl = r[o], sl[o], cl[o]; u, st = np.unique(cl, return_index=True); en = np.r_[st[1:], len(cl)]
    num = den = 0.0; nc = 0
    for a, b in zip(st, en):
        s = sl[a:b]; ns = int(s.sum()); nf = (b - a) - ns
        if ns >= 2 and nf >= 2:
            w = min(ns, nf); rr = r[a:b]; num += w * (np.median(rr[s]) - np.median(rr[~s])); den += w; nc += 1
    return (num / den if den else float("nan")), nc
ok1 = slow.sum() >= 100 and (~slow).sum() >= 1000
for foot, a0 in A0.items():
    go, gb = accel(mtm, rhm, lm); ok = np.isfinite(go) & np.isfinite(gb) & (go > 0) & (gb > 0); r = np.where(ok, resid(np.where(ok, go, 1), np.where(ok, gb, 1), a0), np.nan); g = np.isfinite(r)
    r, sl, cl, gbv = r[g], slow[g], cell[g], gb[g]; Dv, nc = Dstat(r, sl, cl)
    if foot == "canonical":
        ok1 = ok1 and nc >= 20; fail += not ok1; P(f"C1 slow {int(sl.sum())} (>= 100), fast {int((~sl).sum())} (>= 1000), matched cells {nc} (>= 20): {'PASS' if ok1 else 'FAIL'}")
        e2 = float(np.max(np.abs(resid(nu(gbv / a0) * gbv, gbv, a0)))); ok2 = e2 <= 1e-12; fail += (not ok2) and not MUT; P(f"C2 residual of the law's own prediction, max {e2:.1e}: {'PASS' if ok2 else 'FAIL'}")
    rng = np.random.default_rng(20261105); bs = [Dstat(r, sl, cl, rng.integers(0, len(r), len(r)))[0] for _ in range(NB)]; st = float(np.nanstd(bs))
    def Dfor(mt, rh):
        gk, bk = accel(mt, rh, lm); okk = np.isfinite(gk) & np.isfinite(bk) & (gk > 0) & (bk > 0); rk = np.full(n, np.nan); rk[okk] = resid(gk[okk], bk[okk], a0); m = np.isfinite(rk); return Dstat(rk[m], slow[m], cell[m])[0]
    D2 = Dfor(mt2, rh2); sm = abs(Dv - D2); D8 = Dfor(mt8, rh8); D67 = Dfor(mt67, rh67); Dm = [D2, D8, D67]
    gs, bss = accel(mtm, rhm, msr); oks = np.isfinite(gs) & (bss > 0); rs = np.full(n, np.nan); rs[oks] = resid(gs[oks], bss[oks], a0); m = np.isfinite(rs); ss = abs(Dstat(rs[m], slow[m], cell[m])[0] - Dv)
    sD = math.sqrt(st ** 2 + sm ** 2 + ss ** 2); ym = float(np.median(gbv / a0)); h_ = 1e-4; dl = -(math.log(nu(ym * (1 + h_))) - math.log(nu(ym * (1 - h_)))) / (2 * h_)
    if sD > 0.06: lab = "NO POWER"
    elif abs(Dv) <= 2 * sD: lab = "UNIVERSAL"
    elif abs(Dv) > 3 * sD: lab = "DIFFERS"
    else: lab = "NOT SEPARATED"
    R = dict(n=int(len(r)), n_slow=int(sl.sum()), cells=nc, D=Dv, sigma_stat=st, sigma_model=sm, sigma_mass=ss, sigma_D=sD, D_second=D2, D_without_6_7_posthoc=D8, D_only_6_7_posthoc=D67, median_y=ym, dlng_dlna0=dl, implied_dln_a0=Dv / dl, label=lab,
             abs_median_slow=float(np.median(r[sl])), abs_median_fast=float(np.median(r[~sl])))
    P(f"\n[{foot}] n {len(r)}, slow {int(sl.sum())}, cells {nc}: D = {Dv:+.4f} +- {sD:.4f} (stat {st:.4f}, model best-vs-second {sm:.4f}, M* {ss:.4f}); {lab}")
    P(f"[{foot}] median y at r_half {ym:.2f}; d ln g / d ln a0 {dl:.3f}; implied d ln a0 (slow - fast) {Dv / dl:+.3f}")
    P(f"[{foot}] D with second-best model {D2:+.4f}; beside, post-hoc: without HDUs 6-7 {D8:+.4f}, only HDUs 6-7 {D67:+.4f}")
    P(f"[{foot}] beside, absolute median residual (H0 70, NSA log masses as stored): slow {R['abs_median_slow']:+.3f}, fast {R['abs_median_fast']:+.3f}")
    if foot == "canonical" and not MUT:
        r3 = r + np.where(sl, math.log(10 ** 0.12), 0.0); D3, _ = Dstat(r3, sl, cl); ok3 = abs(D3 - Dv - math.log(10 ** 0.12)) <= 0.02; fail += not ok3
        P(f"C3 injection +0.12 dex on slow g_obs: D rises {D3 - Dv:+.4f} (want 0.276 +- 0.02): {'PASS' if ok3 else 'FAIL'}")
    if MUT: R["mutate_ok"] = bool(abs(Dv) <= 2 * sD); P(f"[{foot}] MUTATE |D| <= 2 sigma: {'PASS' if R['mutate_ok'] else 'FAIL'}")
    RES[foot] = R
RES["fail"] = fail; P(f"failed checks: {fail}")
sfx = "_MUTATE" if MUT else ""; open(os.path.join(HERE, f"ku2{sfx}.out"), "w").write("\n".join(OUT) + "\n"); json.dump(RES, open(os.path.join(HERE, f"ku2{sfx}.json"), "w"), indent=1)
sys.exit(1 if (MUT or fail) else 0)

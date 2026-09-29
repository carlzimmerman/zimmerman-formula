#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG167 attacks (b) power and (d) null, frozen procedures.  ZF_REPO=<repo> python3 CFG167_power_bd.py [SEED] > CFG167_power_bd.out (rc 0).
Mock truth = real KURVS and KROSS baryons, sigma, errors; the law generates g_true; V_mock^2 = g R - alpha_true sigma^2; analysed with the exact P4 pipeline.
No SPARC anchor offset is put into the mock (it is common to both samples and cancels in D; that is itself the assumption attacked in (a4))."""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
from scipy.stats import gaussian_kde, norm
import CFG167_referee_diff_p4 as D67
M = D67.M
P = lambda *a: print(*a, flush=True)
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 167
NTR, CH = 4000, 250
LN10 = M.LN10
SK, SR, AS = D67.load_all("inc_star_deg")
main = D67.diff(SK, SR, D67.P4, D67.P4)
D_OBS, SD_OBS, DH_OBS = main["D"], main["sD"], main["DH"]
P(f"CFG167 power (b) and null (d), seed {SEED}, N = {NTR} per (truth, family), repo=<repo>")
P(f"observed: D {D_OBS:+.4f} +- {SD_OBS:.4f}, D_H {DH_OBS:+.4f}")


class Pre:
    def __init__(self, S):
        self.S = S
        self.n = len(S.ids)
        self.xa = S.R / S.Reff - 1
        self.al = M.alpha_K(self.xa)[None, :]
        gb = M.gbar(S, D67.MU, 0.0)
        self.aF = M.A0[D67.FOOT] * np.ones(self.n)
        self.aH = M.A0[D67.FOOT] * M.E_of_z(S.z)
        self.gpF, self.gpH = M.gpred(gb, self.aF), M.gpred(gb, self.aH)
        self.emF = S.mass_err * np.abs(M.slope(gb, self.aF))
        self.emH = S.mass_err * np.abs(M.slope(gb, self.aH))
        self.cot = 1.0 / np.tan(S.inc)


PK, PR = Pre(SK), Pre(SR)


def pool2(d, e):
    w = 1.0 / e ** 2
    sw = w.sum(1)
    m = (w * d).sum(1) / sw
    chi = (w * (d - m[:, None]) ** 2).sum(1) / max(d.shape[1] - 1, 1)
    return m, np.sqrt(1.0 / sw) * np.sqrt(np.maximum(chi, 1.0))


def gen(pre, law, mu, scale, rng, nt):
    """mu: (nt,1); scale: (nt,1) or (nt,n) multiplicative on alpha_true. returns pooled flat/H (mean, err) arrays over trials"""
    S, n = pre.S, pre.n
    logM = S.logM[None, :] + rng.normal(0, S.mass_err, (nt, n))
    Ms = 10.0 ** logM
    Mb = Ms * M.enclosed(S.R / S.Rd)[None, :] + mu * Ms * M.enclosed(S.R / (2 * S.Rd))[None, :]
    gbt = M.G * Mb * M.MSUN / (S.R * M.KPC) ** 2
    a = pre.aF if law == "flat" else pre.aH
    gtrue = M.nu_mono(gbt / a[None, :]) * gbt
    Vc2 = gtrue * (S.R * M.KPC) / 1e6
    V2 = Vc2 - scale * pre.al * S.sig[None, :] ** 2
    fl = float(np.mean(V2 < 0.0025 * Vc2))
    V2 = np.maximum(V2, 0.0025 * Vc2)
    dinc = rng.normal(0, S.einc[None, :], (nt, n))
    Vobs = np.sqrt(V2) * np.sin(S.inc)[None, :] / np.sin(S.inc[None, :] + dinc) + rng.normal(0, S.eV[None, :], (nt, n))
    Vobs = np.maximum(Vobs, 1.0)
    sig = np.maximum(S.sig[None, :] + rng.normal(0, S.esig[None, :], (nt, n)), 1.0)
    Vc2a = Vobs ** 2 + pre.al * sig ** 2
    gobs = Vc2a * 1e6 / (S.R * M.KPC)
    ev = 2 * Vobs * S.eV[None, :] / Vc2a / LN10
    es = 2 * pre.al * sig * S.esig[None, :] / Vc2a / LN10
    ei = (2 * Vobs ** 2 / Vc2a / LN10) * pre.cot[None, :] * S.einc[None, :]
    out = {}
    for nm, gp, em in (("f", pre.gpF, pre.emF), ("h", pre.gpH, pre.emH)):
        d = np.log10(gobs) - np.log10(gp)[None, :]
        e = np.sqrt(ev ** 2 + es ** 2 + ei ** 2 + em[None, :] ** 2)
        out[nm] = pool2(d, e)
    return out, fl


def run(family, truth, seed, fixed_scale=None):
    rng = np.random.default_rng(seed)
    Dl, DHl, sDl, fls = [], [], [], []
    done = 0
    while done < NTR:
        nt = min(CH, NTR - done)
        if family == "IDEAL":
            muR = np.full((nt, 1), 0.67); muK = muR.copy(); sK = sR = np.ones((nt, 1))
        else:
            muR = 10 ** rng.normal(math.log10(0.67), 0.3, (nt, 1))
            g = np.exp(rng.normal(0, 0.5, (nt, 1)))
            muK = g * muR
            if family == "GAS":
                sK = sR = np.ones((nt, 1))
            elif family == "CAL":
                c = np.exp(rng.normal(0, 0.4, (nt, 1))); sK = c * np.exp(rng.normal(0, 0.2, (nt, PK.n))); sR = c * np.exp(rng.normal(0, 0.2, (nt, PR.n)))
            elif family == "CAL-IND":
                sK = np.exp(rng.normal(0, 0.4, (nt, 1))) * np.exp(rng.normal(0, 0.2, (nt, PK.n))); sR = np.exp(rng.normal(0, 0.4, (nt, 1))) * np.exp(rng.normal(0, 0.2, (nt, PR.n)))
            elif family == "FIXED":
                sK = fixed_scale * np.exp(rng.normal(0, 0.2, (nt, PK.n))); sR = fixed_scale * np.exp(rng.normal(0, 0.2, (nt, PR.n)))
        ok, f1 = gen(PK, truth, muK, sK, rng, nt)
        orr, f2 = gen(PR, truth, muR, sR, rng, nt)
        D = ok["f"][0] - orr["f"][0]
        sD = np.hypot(ok["f"][1], orr["f"][1])
        DH = (ok["f"][0] - ok["h"][0]) - (orr["f"][0] - orr["h"][0])
        Dl.append(D); DHl.append(DH); sDl.append(sD); fls.append((f1, f2))
        done += nt
    return np.concatenate(Dl), np.concatenate(DHl), np.concatenate(sDl), np.mean(np.array(fls), 0)


def classes(D, DH, sD):
    nf, nh = np.abs(D) <= 2 * sD, np.abs(D - DH) <= 2 * sD
    return dict(both=float(np.mean(nf & nh)), flat=float(np.mean(nf & ~nh)), rival=float(np.mean(~nf & nh)), manuf=float(np.mean(~nf & ~nh)))


OUT = dict(seed=SEED)
store = {}
P("\n" + "=" * 100 + "\n(b) power under flat truth and rival truth, same errors\n" + "=" * 100)
for fam in ("IDEAL", "GAS", "CAL", "CAL-IND"):
    for truth in ("flat", "H"):
        D, DH, sD, fl = run(fam, truth, SEED + hash((fam, truth)) % 1 + (0 if truth == "flat" else 1000) + {"IDEAL": 0, "GAS": 10, "CAL": 20, "CAL-IND": 30}[fam])
        store[(fam, truth)] = (D, DH, sD)
        cl = classes(D, DH, sD)
        qs = np.percentile(D, np.arange(5, 100, 10))
        OUT[f"{fam}|{truth}"] = dict(mean=float(D.mean()), sd=float(D.std()), mean_sigma=float(sD.mean()), mean_DH=float(DH.mean()), P_ge_obs=float(np.mean(D >= D_OBS)), cls=cl, floored=[float(x) for x in fl], quantiles=list(map(float, qs)))
        P(f"   {fam:8s} truth={truth:4s}: D mean {D.mean():+.3f} sd {D.std():.3f} (mean analytic sigma {sD.mean():.3f}, mean D_H {DH.mean():+.3f});  P(D >= {D_OBS:.3f}) = {np.mean(D >= D_OBS):.4f};  classes {cl};  floored frac K/R {fl[0]:.3f}/{fl[1]:.3f}")
P("\n   likelihood ratio at D_obs (rival-truth density / flat-truth density) and the frozen reading test")
for fam in ("IDEAL", "GAS", "CAL", "CAL-IND"):
    a, b = store[(fam, "flat")][0], store[(fam, "H")][0]
    lg, lh = norm.pdf(D_OBS, a.mean(), a.std()), norm.pdf(D_OBS, b.mean(), b.std())
    kf, kh = gaussian_kde(a)(D_OBS)[0], gaussian_kde(b)(D_OBS)[0]
    lr_g, lr_k = lh / lg, kh / kf
    pl = OUT[f"{fam}|flat"]["cls"]["rival"]
    ph = OUT[f"{fam}|H"]["cls"]["rival"]
    lr = lr_g
    verdict = "INFORMATIVE" if (pl < 0.05 and lr > 10) else ("UNINFORMATIVE" if (lr < 1.5 or pl > 0.20) else "WEAK")
    OUT[f"{fam}|LR"] = dict(gauss=float(lr_g), kde=float(lr_k), P_lands_rival_flat=pl, P_lands_rival_H=ph, verdict=verdict)
    P(f"   {fam:8s}: LR Gaussian {lr_g:8.3g}  KDE {lr_k:8.3g};  P(lands on rival | flat) = {pl:.3f}, P(lands on rival | rival) = {ph:.3f};  P(manufactures | flat) = {OUT[f'{fam}|flat']['cls']['manuf']:.3f}, | rival = {OUT[f'{fam}|H']['cls']['manuf']:.3f}   -> {verdict}")

P("\n" + "=" * 100 + "\n(d) what a null would have looked like\n" + "=" * 100)
P(f"   (i) class map in D (this run's sigma_D {SD_OBS:.4f}, D_H {DH_OBS:+.4f}): lands on flat [{-2*SD_OBS:+.3f}, {DH_OBS-2*SD_OBS:+.3f}); both [{DH_OBS-2*SD_OBS:+.3f}, {2*SD_OBS:+.3f}]; lands on rival ({2*SD_OBS:+.3f}, {DH_OBS+2*SD_OBS:+.3f}]; manufactures D > {DH_OBS+2*SD_OBS:+.3f} or D < {-2*SD_OBS:+.3f}")
P(f"       D_obs {D_OBS:+.3f} is {(DH_OBS+2*SD_OBS-D_OBS)/SD_OBS:.2f} sigma_D below the manufactures edge and {(D_OBS-2*SD_OBS)/SD_OBS:.2f} sigma_D above the flat edge")
P("   (ii) D deciles (5..95 step 10) per family/truth:")
for fam in ("IDEAL", "CAL"):
    for truth in ("flat", "H"):
        P(f"       {fam:8s} {truth:4s}: " + " ".join(f"{v:+.3f}" for v in OUT[f"{fam}|{truth}"]["quantiles"]))
P("   (iv) 'P4 is wrong' null: truth alpha scaled by a FIXED factor s in both samples (per-galaxy lnN(0,0.2), GAS nuisance), analysed with the assumed P4 alpha")
for s in (0.6, 1.4):
    for truth in ("flat", "H"):
        D, DH, sD, fl = run("FIXED", truth, SEED + 500 + (0 if truth == "flat" else 1) + int(s * 10), fixed_scale=s)
        cl = classes(D, DH, sD)
        OUT[f"FIXED{s}|{truth}"] = dict(mean=float(D.mean()), sd=float(D.std()), cls=cl, P_ge_obs=float(np.mean(D >= D_OBS)))
        P(f"       true alpha x {s:.1f}, truth={truth:4s}: D mean {D.mean():+.3f} sd {D.std():.3f}; classes {cl}; P(D >= D_obs) {np.mean(D >= D_OBS):.3f}")
P(f"   (v) a D that would have counted as a fail (CFG161 rule): D > {DH_OBS+2*SD_OBS:+.3f} or D < {-2*SD_OBS:+.3f}; the observed {D_OBS:+.3f} misses that by {DH_OBS+2*SD_OBS-D_OBS:.3f}")
p1, p2 = OUT["IDEAL|flat"]["P_ge_obs"], OUT["CAL|flat"]["P_ge_obs"]
p3 = OUT["CAL-IND|flat"]["P_ge_obs"]
v = "NULL-DISTINGUISHABLE" if (p1 < 0.01 and p2 < 0.10) else "NOT DISTINGUISHABLE from flat-truth-plus-nuisance"
P(f"   (d) VERDICT: {v}  (P(D >= D_obs | flat, IDEAL) = {p1:.4f}; | CAL = {p2:.4f}; | CAL-IND = {p3:.4f})")
OUT["d_verdict"] = v
json.dump(OUT, open(os.path.join(D67.HERE, f"CFG167_power_bd_results_seed{SEED}.json"), "w"), indent=1, default=float)
P("written results json; exit 0")

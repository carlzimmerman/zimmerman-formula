#!/usr/bin/env python3
"""CFG504 transition calibration on the PM halo profiles (FROZEN_CRITERIA.md sections 3-4, 7; criteria commit 333a5fce4).

Reads cfg504_pm_<run>.npz (cfg504_pm.py). Per run and mass bin: stacked xi_hm(r) on 48 shells 0.15-20 Mpc/h, 27-sub-volume jackknife.
Form (frozen): Delta rho / rho_bar = [rho_NFW / rho_bar - 1] f_t(r / r_ta) + A b zeta xi_NL [1 - f_t],  f_t = [1 + (x/x_t)^4]^-2.
  rho_NFW = Duffy NFW (z = 0) holding the halo's M_ta inside r_ta, continued; b = Tinker+10 (PM cosmology); zeta xi_NL = CAMB halofit
  (Takahashi) z = 0 x Tinker+05 zeta.  Bin model = mean over 25 M_ta quantiles (2-98%).
Step 1: A from shells 2.5 r_ta,med <= r <= 20 Mpc/h (pure two-halo, no window).  Step 2: x_t on max(2.5 cells, 0.25 r_ta,med) <= r <=
2.5 r_ta,med, log grid [0.1, 3] (400).  sigma(x_t): jackknife refits.  PRIMARY x_t = inverse-variance mean over resolved 512^3 fits.
MUTATE SHUF (load-bearing): uniform-random particles around the real catalogue give no excess in [0.5, 3] r_ta,med.
Output: cfg504_calib.out, cfg504_calib_results.json.   Run: nice -n 15 python3 cfg504_calib.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import math, json, time
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg504_envlib as EL                                                   # noqa: E402
from colossus.cosmology import cosmology                                     # noqa: E402
from colossus.lss import bias as cbias                                       # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg504_work"))
LL = EL.LL
h = 0.6736
OMPM = (0.02237 + 0.1200) / h ** 2
RHOM_H = OMPM * 2.77536627e11
PMC = cosmology.setCosmology("cfg504pm", params=dict(flat=True, H0=100 * h, Om0=OMPM, Ob0=0.02237 / h ** 2, sigma8=0.811, ns=0.965),
                             persistence="")
RUNS512 = ("S0_512_a", "S0_512_b")
RUNS256 = ("S0_256_s360", "S0_256_s361", "S0_256_s359")
BINS = ("U1", "U2", "U3", "U4", "R1", "R2", "R3", "R4")
XT = np.geomspace(0.1, 3.0, 400)
BETA, GAMMA = 4.0, 8.0
NSUB = 16
T0 = time.time()
LOG = []
RES = {"lane": "CFG504", "script": "cfg504_calib", "form": "f_t = [1 + (x/x_t)^4]^-2; DK14 beta 4 gamma 8", "fits": {}, "checks": {}}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def ft(x, xt, be=BETA, ga=GAMMA):
    return (1.0 + (x / xt) ** be) ** (-ga / be)


P("CAMB halofit xi_NL at z = 0 ...")
X = EL.CambXi([0.0])
P(f"  done ({time.time() - T0:.0f} s), sigma_8(0) {X.sigma8_0:.4f}")


def zxi(rc):
    x = X.xi(True, rc, 0.0)
    return EL.zeta_T05(x) * x


def stack(counts, idx_rows, cen, L, nbar, edges):
    sh = np.diff(counts[idx_rows], axis=1).astype(float)
    V = 4 * math.pi / 3 * (edges[1:] ** 3 - edges[:-1] ** 3)
    xi = sh / (nbar * V)[None, :] - 1.0
    reg = (np.floor(cen / (L / 3.0)).astype(int) % 3) @ np.array([9, 3, 1])
    mean = xi.mean(0)
    loo = []
    for k in range(27):
        m = reg != k
        if m.sum() and (~m).sum():
            loo.append(xi[m].mean(0))
    loo = np.array(loo); n = len(loo)
    sig = np.sqrt((n - 1) / n * ((loo - loo.mean(0)) ** 2).sum(0))
    return mean, sig, loo


class BinModel:
    """shell-averaged model pieces for a bin: P(x_t) = <[rho_NFW/rho_bar - 1] f_t>, Q(x_t) = <b zeta xi (1 - f_t)>, Q0 = <b zeta xi>."""
    def __init__(self, Mta_h, Dta, edges):
        qs = np.quantile(Mta_h, np.linspace(0.02, 0.98, 25))
        self.rta = (3 * qs / (4 * math.pi * Dta * RHOM_H)) ** (1 / 3)                 # Mpc/h comoving (z = 0)
        lo, hi = np.log(edges[:-1]), np.log(edges[1:])
        u = (np.arange(NSUB) + 0.5) / NSUB
        self.rs = np.exp(lo[:, None] + (hi - lo)[:, None] * u[None, :])                # (48, NSUB)
        w = self.rs ** 3 * ((hi - lo)[:, None] / NSUB)                                 # r^2 dr = r^3 dlnr
        self.w = w / w.sum(1, keepdims=True)
        rhob_phys = RHOM_H * h ** 2
        self.nfw = np.zeros((25,) + self.rs.shape); self.bzx = np.zeros_like(self.nfw); self.b = np.zeros(25); self.lM200 = np.zeros(25)
        zx = zxi(self.rs.ravel()).reshape(self.rs.shape)
        for i, (M, rt) in enumerate(zip(qs, self.rta)):
            Mta, rta = M / h, rt / h
            lM200 = brentq(lambda l: float(LL.nfw(10 ** l, 0.0)[0](rta)) - Mta, math.log10(Mta) - 2, math.log10(Mta) + 0.5)
            rho = LL.nfw(10 ** lM200, 0.0)[1]
            self.nfw[i] = rho(self.rs / h) / rhob_phys - 1.0
            self.b[i] = float(cbias.haloBias(10 ** lM200 * h, z=0.0, mdef="200c", model="tinker10"))
            self.bzx[i] = self.b[i] * zx
            self.lM200[i] = lM200
        self.Q0 = (self.bzx * self.w[None]).sum(-1).mean(0)
        self.x = self.rs[None] / self.rta[:, None, None]

    def PQ(self, xt, be=BETA, ga=GAMMA):
        f = ft(self.x, xt, be, ga)
        Pv = (self.nfw * f * self.w[None]).sum(-1).mean(0)
        Qv = (self.bzx * (1 - f) * self.w[None]).sum(-1).mean(0)
        return Pv, Qv


def fit(mean, sig, bm, rc, rmed, cell, be=BETA, ga=GAMMA, grid=None):
    s1 = (rc >= 2.5 * rmed) & (rc <= 20.0)
    if s1.sum() < 2:
        return None
    wv = 1 / sig[s1] ** 2
    A = float((mean[s1] * bm.Q0[s1] * wv).sum() / (bm.Q0[s1] ** 2 * wv).sum())
    s2 = (rc >= max(2.5 * cell, 0.25 * rmed)) & (rc <= 2.5 * rmed)
    if s2.sum() < 3:
        return dict(A=A, xt=None, n2=int(s2.sum()))
    grid = grid if grid is not None else [bm.PQ(x, be, ga) for x in XT]
    c2 = np.array([(((mean[s2] - (Pv[s2] + A * Qv[s2])) / sig[s2]) ** 2).sum() for Pv, Qv in grid])
    j = int(np.argmin(c2))
    return dict(A=A, xt=float(XT[j]), chi2=float(c2[j]), n2=int(s2.sum()), dof=int(s2.sum() - 1), c2grid=c2, edge=bool(j in (0, len(XT) - 1)))


def run_fits(name, resolved_only_primary):
    D = np.load(os.path.join(WORK, f"cfg504_pm_{name}.npz"))
    edges = D["EDGES"]; rc = np.sqrt(edges[1:] * edges[:-1]); L = float(D["L"]); cell = float(D["cell"]); nbar = float(D["nbar"])
    Dta = float(D["Dta"]); sel_idx = D["sel_idx"]
    out = {}
    for b in BINS:
        ii = D[f"bin_{b}"]
        if len(ii) < 20:
            continue
        rows = np.searchsorted(sel_idx, ii)
        mean, sig, loo = stack(D["counts"], rows, D["cen"][ii], L, nbar, edges)
        rmed = float(np.median(D["rta"][ii])); lMmed = float(np.log10(np.median(D["Mta"][ii])))
        resolved = rmed >= 5 * cell
        bm = BinModel(D["Mta"][ii], Dta, edges)
        grid = [bm.PQ(x) for x in XT]
        f0 = fit(mean, sig, bm, rc, rmed, cell, grid=grid)
        rec = dict(n=int(len(ii)), r_ta_med=rmed, logM_ta_med=lMmed, resolved=bool(resolved), cell=cell, r=rc.tolist(), xi=mean.tolist(),
                   sig=sig.tolist(), b_med=float(np.median(bm.b)), logM200c_med_Msun=float(np.median(bm.lM200)))
        if f0 is not None and f0.get("xt") is not None:
            jk = []
            for lo_ in loo:
                fj = fit(lo_, sig, bm, rc, rmed, cell, grid=grid)
                jk.append(fj["xt"])
            jk = np.array(jk); n = len(jk)
            sxt = float(math.sqrt((n - 1) / n * ((jk - jk.mean()) ** 2).sum()))
            Pv, Qv = grid[int(np.argmin(np.abs(XT - f0["xt"])))]
            rec.update(A=f0["A"], x_t=f0["xt"], sig_x_t=sxt, chi2=f0["chi2"], dof=f0["dof"], at_grid_edge=f0["edge"],
                       model_best=(Pv + f0["A"] * Qv).tolist(), model_sharp=None)
            # sharp model for display (f_t = Theta(1 - x))
            fsh = (bm.x <= 1.0).astype(float)
            Psh = (bm.nfw * fsh * bm.w[None]).sum(-1).mean(0); Qsh = (bm.bzx * (1 - fsh) * bm.w[None]).sum(-1).mean(0)
            rec["model_sharp"] = (Psh + f0["A"] * Qsh).tolist()
            # reported: beta, gamma free (coarse grid)
            best = None
            for be in (1.0, 2.0, 3.0, 4.0, 6.0, 8.0):
                for ga in (2.0, 4.0, 6.0, 8.0, 12.0, 16.0):
                    g2 = [bm.PQ(x, be, ga) for x in XT[::4]]
                    s2 = (rc >= max(2.5 * cell, 0.25 * rmed)) & (rc <= 2.5 * rmed)
                    c2 = np.array([(((mean[s2] - (Pv_[s2] + f0["A"] * Qv_[s2])) / sig[s2]) ** 2).sum() for Pv_, Qv_ in g2])
                    j = int(np.argmin(c2))
                    if best is None or c2[j] < best[0]:
                        best = (float(c2[j]), be, ga, float(XT[::4][j]))
            rec["free_beta_gamma"] = dict(chi2=best[0], beta=best[1], gamma=best[2], x_t=best[3])
        elif f0 is not None:
            rec.update(A=f0["A"], x_t=None, note=f"step-2 range has {f0['n2']} shells")
        rec["_bm"] = bm; rec["_grid"] = grid; rec["_mean"] = mean; rec["_sig"] = sig; rec["_s2lo"] = max(2.5 * cell, 0.25 * rmed)
        out[b] = rec
        P(f"  [{name}] {b}: n {len(ii)}, log M_ta {lMmed:.2f}, r_ta {rmed:.2f} Mpc/h ({rmed / cell:.1f} cells) "
          f"{'RESOLVED' if resolved else 'unres.'}; A {rec.get('A', float('nan')):.3f}; x_t "
          + (f"{rec['x_t']:.3f} +- {rec['sig_x_t']:.3f}, chi2 {rec['chi2']:.1f}/{rec['dof']}"
             f"{' (GRID EDGE)' if rec['at_grid_edge'] else ''}; free beta/gamma: {rec['free_beta_gamma']}" if rec.get('x_t') else "not fitted"))
    return out, D


FITS = {}
for name in RUNS512 + RUNS256:
    if not os.path.exists(os.path.join(WORK, f"cfg504_pm_{name}.npz")):
        P(f"  [{name}] no catalogue file; skipped")
        continue
    FITS[name], _ = run_fits(name, name in RUNS512)

# ------------------------------------------------------------------ primary x_t
res = [(n, b, r) for n in RUNS512 if n in FITS for b, r in FITS[n].items() if r["resolved"] and r.get("x_t") is not None]
xs = np.array([r["x_t"] for _, _, r in res]); ss = np.array([max(r["sig_x_t"], 1e-3) for _, _, r in res])
lMs = np.array([r["logM_ta_med"] for _, _, r in res]); As = np.array([r["A"] for _, _, r in res])
w = 1 / ss ** 2
xt_p = float((w * xs).sum() / w.sum()); s_formal = float(1 / math.sqrt(w.sum())); s_sc = float(xs.std(ddof=1)) if len(xs) > 1 else 0.0
s_tot = max(s_formal, s_sc)
A_mean = float(As.mean())
cf = np.polyfit(lMs - 13.8, xs, 1, w=1 / ss) if len(xs) >= 3 else np.array([0.0, xt_p])
red = np.array([r["chi2"] / max(r["dof"], 1) for _, _, r in res])
poor = bool(np.median(red) > 3)
P(f"\nPRIMARY x_t (inverse-variance mean of {len(xs)} resolved 512^3 fits): {xt_p:.4f}; formal {s_formal:.4f}, scatter {s_sc:.4f} -> "
  f"sigma_tot {s_tot:.4f}; individual " + ", ".join(f"{n[-1]}:{b} {r['x_t']:.3f}+-{r['sig_x_t']:.3f}" for n, b, r in res))
P(f"  mean A (resolved) {A_mean:.3f}; linear trend x_t = {cf[1]:.3f} + {cf[0]:.3f} (log M_ta - 13.8); median step-2 chi2/dof "
  f"{np.median(red):.2f} -> {'LABEL: TRANSITION FORM POOR FIT ON PM' if poor else 'form adequate (median chi2/dof <= 3)'}")
RES["primary"] = dict(x_t=xt_p, sigma_formal=s_formal, sigma_scatter=s_sc, sigma_tot=s_tot, n_fits=int(len(xs)), A_mean=A_mean,
                      trend_intercept_at_13p8=float(cf[1]), trend_slope_per_dex=float(cf[0]), median_red_chi2=float(np.median(red)),
                      label_poor_fit=poor, extrap_at_kids_median_12p48=float(np.clip(cf[1] + cf[0] * (12.48 - 13.8), 0.1, 3.0)))
P(f"  extrapolated x_t at the KiDS median log M_ta 12.48 (reported variant b): {RES['primary']['extrap_at_kids_median_12p48']:.3f}")

# ------------------------------------------------------------------ extrapolation check on unresolved 512^3 bins (reported)
P("\nExtrapolation check (reported): unresolved 512^3 bins, primary x_t with step-1 A, on shells max(2.5 cells, 0.25 r_ta) .. 2.5 r_ta:")
ext = {}
for n in RUNS512:
    for b, r in FITS.get(n, {}).items():
        if r["resolved"]:
            continue
        bm = r["_bm"]; mean, sig = r["_mean"], r["_sig"]
        rc = np.array(r["r"]); s2 = (rc >= r["_s2lo"]) & (rc <= 2.5 * r["r_ta_med"])
        Pv, Qv = bm.PQ(xt_p)
        c2p = float((((mean[s2] - (Pv[s2] + r["A"] * Qv[s2])) / sig[s2]) ** 2).sum()) if s2.sum() else float("nan")
        fsh = (bm.x <= 1.0).astype(float)
        Psh = (bm.nfw * fsh * bm.w[None]).sum(-1).mean(0); Qsh = (bm.bzx * (1 - fsh) * bm.w[None]).sum(-1).mean(0)
        c2s = float((((mean[s2] - (Psh[s2] + r["A"] * Qsh[s2])) / sig[s2]) ** 2).sum()) if s2.sum() else float("nan")
        ext[f"{n}|{b}"] = dict(n_shells=int(s2.sum()), chi2_primary=c2p, chi2_sharp=c2s, x_t_free=r.get("x_t"), A=r["A"])
        P(f"  {n} {b} (log M_ta {r['logM_ta_med']:.2f}, r_ta {r['r_ta_med']:.2f}): {s2.sum()} shells (r >= {r['_s2lo']:.2f}); chi2 primary "
          f"{c2p:.1f}, sharp {c2s:.1f}; free x_t {r.get('x_t')}")
RES["extrapolation_check"] = ext

# ------------------------------------------------------------------ resolution check: 256^3 vs 512^3 per bin (reported)
P("\nResolution check (reported): x_t per bin, 512^3 runs | 256^3 runs:")
rcheck = {}
for b in BINS:
    a = [FITS[n][b]["x_t"] for n in RUNS512 if n in FITS and b in FITS[n] and FITS[n][b].get("x_t")]
    c = [FITS[n][b]["x_t"] for n in RUNS256 if n in FITS and b in FITS[n] and FITS[n][b].get("x_t")]
    rcheck[b] = dict(x512=a, x256=c)
    P(f"  {b}: " + " ".join(f"{x:.3f}" for x in a) + " | " + " ".join(f"{x:.3f}" for x in c))
RES["resolution_check"] = rcheck

# ------------------------------------------------------------------ MUTATE SHUF (load-bearing)
P("\nMUTATE SHUF: uniform-random particles around the real S0_512_a catalogue (resolved bins):")
D = np.load(os.path.join(WORK, "cfg504_pm_S0_512_a.npz"))
edges = D["EDGES"]; rc = np.sqrt(edges[1:] * edges[:-1]); L = float(D["L"]); nbar = float(D["nbar"])
shuf_ok = True; sh = {}
if "shuf_idx" not in D.files:
    shuf_ok = False
    P("  no shuffled counts on disk -> FAIL")
else:
    for b in BINS:
        r = FITS["S0_512_a"].get(b)
        if r is None or not r["resolved"]:
            continue
        ii = D[f"bin_{b}"]
        rows = np.searchsorted(D["shuf_idx"], ii)
        mean_s, sig_s, loo_s = stack(D["shuf_counts"], rows, D["cen"][ii], L, nbar, edges)
        win = (rc >= 0.5 * r["r_ta_med"]) & (rc <= 3.0 * r["r_ta_med"])
        vol = (edges[1:] ** 3 - edges[:-1] ** 3)[win]
        mbar = float((mean_s[win] * vol).sum() / vol.sum())
        lb = np.array([(l_[win] * vol).sum() / vol.sum() for l_ in loo_s]); n = len(lb)
        sbar = float(math.sqrt((n - 1) / n * ((lb - lb.mean()) ** 2).sum()))
        real = float((np.array(r["xi"])[win] * vol).sum() / vol.sum())
        s1 = (rc >= 2.5 * r["r_ta_med"]) & (rc <= 20.0)
        Ash = float((mean_s[s1] * r["_bm"].Q0[s1] / sig_s[s1] ** 2).sum() / (r["_bm"].Q0[s1] ** 2 / sig_s[s1] ** 2).sum())
        ok = abs(mbar) < 3 * sbar and abs(mbar) < 0.05 * abs(real)
        shuf_ok &= ok
        sh[b] = dict(mean_shuf=mbar, sig=sbar, mean_real=real, A_shuf=Ash, ok=bool(ok))
        P(f"  {b}: shuffled mean xi_hm over [0.5, 3] r_ta = {mbar:+.5f} +- {sbar:.5f} (real {real:.3f}); A_shuf {Ash:+.4f} -> {'ok' if ok else 'FAIL'}")
RES["mutate_shuf"] = sh
RES["checks"]["MUTATE_SHUF"] = dict(ok=bool(shuf_ok), load_bearing=True, msg="shuffled particles give no infall excess in every resolved bin"
                                    if shuf_ok else "shuffled check failed")
P(f"  [{'PASS' if shuf_ok else 'FAIL'}] MUTATE SHUF")

for n in FITS:
    for b in FITS[n]:
        for k in [k for k in FITS[n][b] if k.startswith("_")]:
            del FITS[n][b][k]
RES["fits"] = FITS
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "cfg504_calib_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg504_calib.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if shuf_ok else 1)

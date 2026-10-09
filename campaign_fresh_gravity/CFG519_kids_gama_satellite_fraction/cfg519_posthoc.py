#!/usr/bin/env python3
"""CFG519 POST-HOC diagnostics (not in the frozen verdict; written after the main run was seen).
PH1  where does the photometric companion excess go?  On matched in-overlap ISO lenses, the CFG502-style photometric excess
     (pool galaxies more massive than the lens, R_p < 0.5 Mpc, 10 < |dchi_phot| < 600 Mpc, minus the 4-6 Mpc annulus scaled by
     area and by the in-field annulus fraction) is split by the companion's spectroscopic status: |dv| < 1000 km/s; matched with
     |dv| >= 1000; unmatched (no G3C redshift).  Uses the lens spec-z only to classify.
PH2  satellite definitions: S_IC (frozen), S_BCG, and S_mass = in a G3C group with a matched member more massive (KiDS log M*) than
     the lens; plus the per-mass parent fraction (ALL) next to CFG506's box parent value (0.66 at log M* 10.5-10.6).
PH3  weighting convention: f with WW summed over 15 bins (CFG502, frozen here) vs WW of the outermost bin only (CFG506's pstack[0]).
Run: nice -n 10 python3 -u cfg519_posthoc.py   (needs ../_external_data/cfg519_work/cfg519_state.npz from the main run)
"""
import os, sys, json
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg519_work")
c_kms = 2.998e5
LOG = []; RES = {}


def say(s=""):
    print(s, flush=True); LOG.append(s)


say(__doc__.split("Run:")[0].strip())
X = np.load(os.path.join(WORK, "cfg519_state.npz"))
S = np.load(os.path.join(EXT, "cfg502_work", "cfg502_stage.npz"))
lra, ldec, lz, llm, lchi = S["ra"], S["dec"], S["z"], S["logM"], S["chi"]
iso10 = S["iso10"]; WW = S["WW"]; wl = WW.sum(1); NA = len(lz)
P_ra, P_dec, P_chi, P_lm, P_r, P_fld, P_g, P_zs, matched = (X[k] for k in ("P_ra", "P_dec", "P_chi", "P_lm", "P_r", "P_fld", "P_g", "P_zs", "matched"))
L_p, inside, L_m, L_zs, REG, S_IC, S_BCG, L_g, cell, afr_p = (X[k] for k in ("L_p", "inside", "L_m", "L_zs", "REG", "S_IC", "S_BCG", "L_g", "cell", "afr_p"))
NC = 48


def unit(ra, dec):
    r, d = np.radians(ra), np.radians(dec)
    return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]


def reweight(val, src, tgt, w=wl):
    num = np.bincount(cell[src], weights=(w * val)[src], minlength=NC); den = np.bincount(cell[src], weights=w[src], minlength=NC)
    n = np.bincount(cell[src], minlength=NC)
    f = np.where(n >= 20, num / np.maximum(den, 1e-300), np.nan)
    W = np.bincount(cell[tgt], weights=w[tgt], minlength=NC); g = np.isfinite(f)
    return float((W[g] * f[g]).sum() / W[g].sum())


def jk(fn):
    v = np.array([fn(REG != k) for k in range(12)])
    return float(np.sqrt(11 / 12 * ((v - v.mean()) ** 2).sum()))


# ---------------------------------------------------------------- PH1
say("\n== PH1: decomposition of the photometric companion excess (lenses log M* >= 10.44, matched, in overlap, ISO)")
inf = np.where(P_fld >= 0)[0]
pt = cKDTree(unit(P_ra[inf], P_dec[inf]))
src = np.where(iso10 & L_m)[0]
lab_in = {k: np.zeros(NA) for k in ("spec_near", "spec_far", "nospec", "nospec_bright")}
lab_an = {k: np.zeros(NA) for k in lab_in}
for i0 in range(0, len(src), 4000):
    idx = src[i0:i0 + 4000]
    lists = pt.query_ball_point(unit(lra[idx], ldec[idx]), r=6.0 / lchi[idx])
    k_ = np.repeat(np.arange(len(idx)), [len(x) for x in lists])
    js = inf[np.fromiter((j for x in lists for j in x), dtype=np.int64, count=sum(len(x) for x in lists))]
    li = idx[k_]
    m = (js != L_p[li]) & (P_lm[js] > llm[li]); js, li = js[m], li[m]
    adc = np.abs(P_chi[js] - lchi[li])
    R = np.arccos(np.clip((unit(P_ra[js], P_dec[js]) * unit(lra[li], ldec[li])).sum(1), -1, 1)) * lchi[li]
    m = (adc > 10) & (adc < 600) & ((R < 0.5) | ((R >= 4) & (R < 6))); js, li, R = js[m], li[m], R[m]
    dv = np.where(matched[js], c_kms * (P_zs[js] - L_zs[li]) / (1 + L_zs[li]), np.nan)
    cls = {"spec_near": matched[js] & (np.abs(dv) < 1000), "spec_far": matched[js] & (np.abs(dv) >= 1000),
           "nospec": ~matched[js], "nospec_bright": ~matched[js] & (P_r[js] < 19.5)}
    for k, c in cls.items():
        lab_in[k] += np.bincount(li[c & (R < 0.5)], minlength=NA)
        lab_an[k] += np.bincount(li[c & (R >= 4)], minlength=NA) * (0.25 / 20)
# annulus area correction per lens (in-field fraction)
for k in lab_an:
    lab_an[k] = lab_an[k] / np.maximum(afr_p, 0.05)
sub = llm >= 10.44
ex = {k: lab_in[k] - lab_an[k] for k in lab_in}
tot = sum(ex[k] for k in ("spec_near", "spec_far", "nospec"))
ph = np.full(NA, np.nan); ph[S["iso_idx"]] = S["cin"] - S["can"] * 0.25 / 20.0
srcm = iso10 & L_m & sub
R1 = {}
for k, v in list(ex.items()) + [("total_infield", tot), ("CFG502_phot", np.nan_to_num(ph))]:
    val = reweight(v, srcm, iso10 & sub)
    R1[k] = dict(val=val, sig=jk(lambda u, v=v: reweight(v, srcm & u, iso10 & sub)))
    say(f"  {k:16s} {R1[k]['val']: .4f} +- {R1[k]['sig']:.4f}")
say("  (spec_near = companions with a G3C redshift within 1000 km/s of the lens; spec_far = with a G3C redshift but >= 1000 km/s away,"
    " i.e. line-of-sight projections that still survive the annulus subtraction; nospec = no G3C redshift; nospec_bright = of which KiDS r < 19.5)")
RES["PH1"] = R1

# ---------------------------------------------------------------- PH2
say("\n== PH2: satellite definitions and the parent fraction by mass")
gtab = pd.read_csv(os.path.join(WORK, "G3CGalv10.csv"))
gid = gtab.GroupID.values
# most massive matched member (KiDS log M*) per group
pm = np.where(matched)[0]
grp = gid[P_g[pm]]
dfm = pd.DataFrame(dict(g=grp, lm=P_lm[pm])).query("g > 0").groupby("g").lm.max()
lg = np.where(L_m, gid[np.where(L_m, L_g, 0)], 0)
mx = dfm.reindex(lg).values
S_mass = L_m & (lg > 0) & np.isfinite(mx) & (mx > llm)
R2 = {}
for nm, lab in (("S_IC", S_IC), ("S_BCG", S_BCG), ("S_mass", S_mass)):
    v = reweight(lab.astype(float), iso10 & inside & L_m, iso10)
    R2[nm] = dict(f=v, sig=jk(lambda u, lab=lab: reweight(lab.astype(float), iso10 & inside & L_m & u, iso10)))
    say(f"  ISO stack-weighted f, {nm:6s}: {v:.4f} +- {R2[nm]['sig']:.4f}")
ME = [8.5, 9.5, 10.0, 10.25, 10.5, 10.75, 11.0]
for a in range(6):
    m = inside & L_m & (llm >= ME[a]) & (llm < ME[a + 1])
    mi = m & iso10
    say(f"  log M* {ME[a]:.2f}-{ME[a + 1]:.2f}: parent (ALL) S_IC {np.average(S_IC[m], weights=wl[m]):.3f} (n {int(m.sum())}), "
        f"ISO {np.average(S_IC[mi], weights=wl[mi]):.3f} (n {int(mi.sum())})  [raw matched, weight-averaged]")
    R2[f"parent_{ME[a]}"] = float(np.average(S_IC[m], weights=wl[m])); R2[f"iso_{ME[a]}"] = float(np.average(S_IC[mi], weights=wl[mi]))
m = inside & L_m & (llm >= 10.5) & (llm < 10.6)
say(f"  log M* 10.5-10.6 parent S_IC {np.average(S_IC[m], weights=wl[m]):.3f} (CFG506 box parent 0.66)")
R2["parent_10.5_10.6"] = float(np.average(S_IC[m], weights=wl[m]))
RES["PH2"] = R2

# ---------------------------------------------------------------- PH3
say("\n== PH3: weighting convention")
w0 = WW[:, 0]
f0 = reweight(S_IC.astype(float), iso10 & inside & L_m, iso10, w=w0)
say(f"  f (S_IC) with WW of the outermost bin only (CFG506 pstack[0] convention): {f0:.4f}  (frozen WW-sum: see main)")
RES["PH3"] = dict(f_outer_bin_weight=f0)
json.dump(RES, open(os.path.join(HERE, "cfg519_posthoc_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, "cfg519_posthoc.out"), "w").write("\n".join(LOG) + "\n")

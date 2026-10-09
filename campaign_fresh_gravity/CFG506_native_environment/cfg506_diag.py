#!/usr/bin/env python3
"""CFG506 zero-knob diagnostics pack (FROZEN_CRITERIA.md section 11; criteria commit 27a6c64ee). Reads the per-box tables written by
cfg506_box.py and the run JSONs (P(k)); writes cfg506_diag.out, cfg506_diag_results.json and small PNGs in figs/.
D1 settled vs unsettled cold energy; D2 catchment draw q; D3 concentration proxy TA / S0; D4 P_TA / P_S0 vs k; D5 HMF ratio TA / S0.
Run: nice -n 15 python3 cfg506_diag.py
"""
import os, json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
WORK = os.path.join(EXT, "cfg506_work")
FIG = os.path.join(HERE, "figs"); os.makedirs(FIG, exist_ok=True)
JB = json.load(open(os.path.join(HERE, "cfg506_box_results.json")))
LOG = []
RES = {"lane": "CFG506", "script": "cfg506_diag"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def box(k):
    f = os.path.join(WORK, f"cfg506_box_{k}.npz")
    return np.load(f) if os.path.exists(f) else None


W424 = "cfg424_work/cfg424_RES_TA_MIXA_MASSCONS_fret1_"
JS = {k: os.path.join(EXT, v["base_rel"]) for k, v in {}.items()}
BASES = {
    "TA512_can359": W424 + "FLAT_canonical_N512", "TA512_can360": W424 + "FLAT_canonical_N512_seed360", "TA512_alt359": W424 + "FLAT_alt_N512",
    "TA512_DEcan359": W424 + "DE_canonical_N512", "S0512_359": "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N512",
    "S0512_360": "cfg424_work/cfg424_S0_TA_MIXA_MASSCONS_fret1_FLAT_canonical_N512_seed360",
    "TA256_can359": W424 + "FLAT_canonical_N256", "TA256_can360": W424 + "FLAT_canonical_N256_seed360", "TA256_can361": W424 + "FLAT_canonical_N256_seed361",
    "TA256_alt359": W424 + "FLAT_alt_N256", "TA256_alt360": W424 + "FLAT_alt_N256_seed360", "TA256_alt361": W424 + "FLAT_alt_N256_seed361",
    "TA256_DEcan359": W424 + "DE_canonical_N256", "TA256_DEalt359": W424 + "DE_alt_N256",
    "S0256_359": "cfg359_work/cfg359_S0_FLAT_canonical_N256", "S0256_360": "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed360",
    "S0256_361": "cfg411_work/cfg411_S0_Rc3_MIXA_FLAT_canonical_N256_seed361"}
PAIRS = {  # TA key -> matched-seed S0 key
    "TA512_can359": "S0512_359", "TA512_alt359": "S0512_359", "TA512_DEcan359": "S0512_359", "TA512_can360": "S0512_360",
    "TA256_can359": "S0256_359", "TA256_alt359": "S0256_359", "TA256_DEcan359": "S0256_359", "TA256_DEalt359": "S0256_359",
    "TA256_can360": "S0256_360", "TA256_alt360": "S0256_360", "TA256_can361": "S0256_361", "TA256_alt361": "S0256_361"}

# ------------------------------------------------------------------ D4 power spectrum ratio (run JSONs, z = 0)
P("D4: P_TA / P_S0 at z = 0, matched seeds (run JSONs; particle-lattice mesh, no shot-noise subtraction: cancels in the ratio)")
D4 = {}
KS = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0]
for res_ in ("512", "256"):
    for grp in ("can", "alt", "DE"):
        rows = []
        for ta, s0 in PAIRS.items():
            if not ta.startswith(f"TA{res_}_{grp}"):
                continue
            a = json.load(open(os.path.join(EXT, BASES[ta] + ".json")))["snap"]["z0"]
            b = json.load(open(os.path.join(EXT, BASES[s0] + ".json")))["snap"]["z0"]
            k = np.array(a["k"]); r = np.array(a["P"]) / np.array(b["P"])
            rows.append((ta, k, r, a["sigma8"] / b["sigma8"]))
        if not rows:
            continue
        k = rows[0][1]; R = np.array([x[2] for x in rows])
        mean = R.mean(0); sd = R.std(0, ddof=1) if len(rows) > 1 else np.zeros_like(mean)
        D4[f"{res_}_{grp}"] = dict(runs=[x[0] for x in rows], k=k.tolist(), ratio_mean=mean.tolist(), ratio_sd=sd.tolist(),
                                   sigma8_ratio=[x[3] for x in rows])
        P(f"  {res_}^3 {grp:3s} ({len(rows)} seed(s)): sigma8 ratio " + ", ".join(f"{x[3]:.4f}" for x in rows) + "; P ratio at k = "
          + ", ".join(f"{kk:g}: {np.interp(kk, k, mean):.3f}" + (f"+-{np.interp(kk, k, sd):.3f}" if len(rows) > 1 else "") for kk in KS if kk <= k[-1])
          + f"; max|P-1| over k <= 1: {np.max(np.abs(mean[k <= 1.0] - 1)):.3f}")
RES["D4"] = D4
fig, ax = plt.subplots(figsize=(5.2, 3.4))
for key, c in (("512_can", "C0"), ("512_alt", "C1"), ("512_DE", "C2"), ("256_can", "C0"), ("256_alt", "C1"), ("256_DE", "C2")):
    if key in D4:
        k = np.array(D4[key]["k"]); m = np.array(D4[key]["ratio_mean"]); s = np.array(D4[key]["ratio_sd"])
        ls = "-" if key.startswith("512") else "--"
        ax.semilogx(k, m, ls, color=c, lw=1.2, label=key.replace("_", "^3 "))
        if s.any():
            ax.fill_between(k, m - s, m + s, color=c, alpha=0.15)
ax.axhline(1, color="k", lw=0.6); ax.set_xlabel("k [h/Mpc]"); ax.set_ylabel("P_TA / P_S0 (z = 0)"); ax.legend(fontsize=7)
ax.set_title("zero-knob rule vs S0, matched seeds", fontsize=9); fig.tight_layout(); fig.savefig(os.path.join(FIG, "D4_pk_ratio.png"), dpi=110); plt.close(fig)

# ------------------------------------------------------------------ D5 halo mass function ratio
P("\nD5: distinct-halo mass function (M_ta, 0.2 dex bins) TA / S0 at matched seeds; complete above 150 m_p")
D5 = {}
EB = np.arange(11.8, 15.21, 0.2)
for ta, s0 in PAIRS.items():
    A, B = box(ta), box(s0)
    if A is None or B is None:
        continue
    na = np.histogram(np.log10(A["Mta"]), EB)[0]; nb = np.histogram(np.log10(B["Mta"]), EB)[0]
    lc = math.log10(150 * float(A["MP"]))
    r = np.where(nb > 0, na / np.maximum(nb, 1), np.nan); e = r * np.sqrt(1 / np.maximum(na, 1) + 1 / np.maximum(nb, 1))
    D5[ta] = dict(edges=EB.tolist(), n_TA=na.tolist(), n_S0=nb.tolist(), ratio=r.tolist(), err=e.tolist(), logM_complete=lc)
    cb = (EB[:-1] >= lc) & (nb >= 20)
    P(f"  {ta} / {s0}: " + " ".join(f"{EB[i]:.1f}:{r[i]:.2f}+-{e[i]:.2f}" for i in np.where(cb)[0]))
RES["D5"] = D5
fig, ax = plt.subplots(figsize=(5.2, 3.4))
for ta, c in (("TA512_can359", "C0"), ("TA512_can360", "C3"), ("TA512_alt359", "C1"), ("TA512_DEcan359", "C2"), ("TA256_can359", "C7")):
    if ta in D5:
        x = 0.5 * (EB[1:] + EB[:-1]); r = np.array(D5[ta]["ratio"]); e = np.array(D5[ta]["err"]); m = (x >= D5[ta]["logM_complete"]) & np.isfinite(r)
        ax.errorbar(x[m], r[m], e[m], fmt="o-", ms=3, lw=1, color=c, label=ta)
ax.axhline(1, color="k", lw=0.6); ax.set_xlabel("log M_ta [Msun/h]"); ax.set_ylabel("n_TA / n_S0"); ax.legend(fontsize=7)
ax.set_title("halo mass function ratio, matched seeds", fontsize=9); fig.tight_layout(); fig.savefig(os.path.join(FIG, "D5_hmf_ratio.png"), dpi=110); plt.close(fig)

# ------------------------------------------------------------------ D3 concentration proxy
P("\nD3: NFW c from M(<r200m/2)/M200m (halos with r_ta >= 5 cells; mesh-limited, labelled), median per log M_ta bin, TA vs S0")
D3 = {}
CB = [13.0, 13.5, 14.0, 14.5, 15.2]
for ta, s0 in PAIRS.items():
    A, B = box(ta), box(s0)
    if A is None or B is None:
        continue
    row = {}
    for i in range(len(CB) - 1):
        def med(Z):
            lm = np.log10(Z["Mta"]); c = Z["cprox"]; m = (lm >= CB[i]) & (lm < CB[i + 1]) & np.isfinite(c)
            return (float(np.median(c[m])), int(m.sum()), float(1.2533 * np.std(c[m]) / math.sqrt(m.sum()))) if m.sum() >= 5 else (None, int(m.sum()), None)
        row[f"{CB[i]}-{CB[i + 1]}"] = dict(TA=med(A), S0=med(B))
    D3[ta] = row
    P(f"  {ta} vs {s0}: " + "; ".join(f"{k}: {v['TA'][0] if v['TA'][0] is None else round(v['TA'][0], 2)} (n {v['TA'][1]}) vs "
                                      f"{v['S0'][0] if v['S0'][0] is None else round(v['S0'][0], 2)} (n {v['S0'][1]})" for k, v in row.items()))
RES["D3"] = D3

# ------------------------------------------------------------------ D2 catchment draw
P("\nD2: catchment draw q_C (fraction of the catchment's cold energy drawn) vs host M_ta; q_max vs the run JSON")
D2 = {}
QB = [12.5, 13.0, 13.5, 14.0, 14.5, 15.2]
for k in BASES:
    if not k.startswith("TA"):
        continue
    A = box(k)
    if A is None:
        continue
    q = A["D2_q"]; hm = A["D2_hostM"]; mc = A["D2_M"]
    jq = json.load(open(os.path.join(EXT, BASES[k] + ".json")))["snap"]["z0"]["q_max"]
    rows = {}
    for i in range(len(QB) - 1):
        m = (hm > 0) & (np.log10(np.maximum(hm, 1)) >= QB[i]) & (np.log10(np.maximum(hm, 1)) < QB[i + 1])
        if m.sum():
            rows[f"{QB[i]}-{QB[i + 1]}"] = dict(n=int(m.sum()), q16=float(np.percentile(q[m], 16)), q50=float(np.median(q[m])),
                                                q84=float(np.percentile(q[m], 84)), qmax=float(q[m].max()))
    nh = int((hm > 0).sum())
    D2[k] = dict(q_max=float(q.max()), q_max_json=jq, n_catch=int(len(q)), n_with_host=nh, by_host_mass=rows,
                 q_massweighted=float((q * mc).sum() / mc.sum()))
    P(f"  {k}: q_max {q.max():.3f} (run JSON {jq:.3f}); catchments {len(q)} ({nh} with a distinct-halo host); mass-weighted q {D2[k]['q_massweighted']:.3f}; "
      + "; ".join(f"{kk}: median {v['q50']:.3f} [{v['q16']:.3f}, {v['q84']:.3f}] max {v['qmax']:.3f} (n {v['n']})" for kk, v in rows.items()))
RES["D2"] = D2
fig, ax = plt.subplots(figsize=(5.2, 3.4))
for k, c, mk in (("TA512_can359", "C0", "o"), ("TA512_can360", "C3", "o"), ("TA512_alt359", "C1", "o"), ("TA256_can359", "C0", "x"), ("TA256_alt359", "C1", "x")):
    A = box(k)
    if A is None:
        continue
    m = A["D2_hostM"] > 0
    ax.semilogx(A["D2_hostM"][m], A["D2_q"][m], mk, ms=2.5, color=c, alpha=0.6, label=k)
ax.set_xlabel("host M_ta [Msun/h]"); ax.set_ylabel("q_C (drawn fraction)"); ax.legend(fontsize=7, markerscale=2)
ax.set_title("catchment draw vs host mass (x = 256^3, o = 512^3)", fontsize=9); fig.tight_layout(); fig.savefig(os.path.join(FIG, "D2_q_vs_mass.png"), dpi=110); plt.close(fig)

# ------------------------------------------------------------------ D1 settled vs unsettled
P("\nD1: settled (switch ON) vs unsettled cold energy")
D1 = {}
for k in ("TA512_can359", "TA256_can359"):
    A = box(k)
    if A is None:
        continue
    D1[k] = JB[k]["D1"]
    P(f"  {k}: settled mass fraction of the cold energy {D1[k]['settled_mass_frac']:.4f}; edge-ball volume {D1[k]['edge_vol_frac']:.4f}, "
      f"catchment volume {D1[k]['catch_vol_frac']:.4f}; phantom excess e = {D1[k]['e_mass_frac']:.4f} and draw = {D1[k]['comp_mass_frac']:.4f} of the total mass")
    fig, axs = plt.subplots(1, 4, figsize=(11, 3.0))
    for ax_, nm, ttl in zip(axs, ("settled", "unsettled", "e", "comp"), ("settled cold energy", "unsettled cold energy", "phantom excess e", "drawn (comp)")):
        img = A[f"D1_{nm}"].astype(float)
        n = img.shape[0]; f = max(n // 256, 1)
        img = img.reshape(n // f, f, n // f, f).sum((1, 3))
        v = np.log10(np.maximum(img, 1e-3 * max(img.max(), 1e-30)))
        ax_.imshow(v.T, origin="lower", cmap="magma", extent=[0, 200, 0, 200]); ax_.set_title(ttl, fontsize=8); ax_.set_xticks([]); ax_.set_yticks([])
    fig.suptitle(f"{k}: 20 Mpc/h slab, log column (arbitrary units)", fontsize=8); fig.tight_layout()
    fig.savefig(os.path.join(FIG, f"D1_settled_unsettled_{k}.png"), dpi=90); plt.close(fig)
RES["D1"] = D1

# ------------------------------------------------------------------ D6 (section 9) 3D stacked lensing-density profiles TA / S0 around matched-mass distinct halos
P("\nD6: 3D stacked lensing density 1 + delta (+ S for TA) around distinct halos, TA / S0 at matched seeds (shells 0.15-20 Mpc/h; <= 200 halos per bin)")
D6 = {}
for ta, s0 in PAIRS.items():
    A, B = box(ta), box(s0)
    if A is None or B is None:
        continue
    E3 = A["EDGES3"]; vol = 4 * math.pi / 3 * np.diff(E3 ** 3); rc = np.sqrt(E3[1:] * E3[:-1])
    nbar = ((0.02237 + 0.1200) / 0.6736 ** 2 * 2.77536627e11) / float(A["MP"])   # mean particles per (Mpc/h)^3
    row = {}
    for ib, (a_, b_) in enumerate(A["PBINS"]):
        if A["P3n"][ib] < 10 or B["P3n"][ib] < 10:
            continue
        ra = np.diff(A["P3"][ib]) / (A["P3n"][ib] * vol); rb = np.diff(B["P3"][ib]) / (B["P3n"][ib] * vol)
        sa = A["P3S"][ib] / A["P3n"][ib] * nbar                       # S in particle-density units (S is a contrast)
        rat = (ra + sa) / rb
        row[f"{a_}-{b_}"] = dict(r=rc.tolist(), ratio_lens=rat.tolist(), ratio_particles=(ra / rb).tolist(), n_TA=int(A["P3n"][ib]), n_S0=int(B["P3n"][ib]))
        pick = [0.3, 0.5, 1.0, 2.0, 4.0, 8.0]
        P(f"  {ta}/{s0} bin {a_}-{b_} (n {A['P3n'][ib]}/{B['P3n'][ib]}): lensing ratio at r = " + ", ".join(f"{x}: {np.interp(x, rc, rat):.3f}" for x in pick)
          + "; particles only " + ", ".join(f"{np.interp(x, rc, ra / rb):.3f}" for x in pick))
    D6[ta] = row
RES["D6"] = D6

json.dump(RES, open(os.path.join(HERE, "cfg506_diag_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg506_diag.out"), "w").write("\n".join(LOG) + "\n")

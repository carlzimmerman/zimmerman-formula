#!/usr/bin/env python3
"""CFG501 core-emptying diagnostic (FROZEN_CRITERIA.md 7b71dd9b5, REPORTED, no verdict weight).
Halo centres: local maxima (3x3x3) of CFG359 S0's z = 0 density (CIC of its committed particle positions on the 256^3 mesh), smoothed by a
Gaussian of sigma = 1 cell, ranked by smoothed peak density; the top 200 with periodic separation >= 8 cells.  In each run the centre is
re-found as the maximum of that run's smoothed density within +-2 cells.  Stacked over the 200 halos in spherical shells of width 1 cell
(0.78 Mpc/h) to 12 cells: mean 1 + delta, e, comp, src = e - comp, m (SW); e / comp / src in units of the mean cold source 1.5 Om (1 - f_b).
Reported: M_run(<= r) / M_S0(<= r) at r = 1, 2, 3, 6 cells; the share of the stacked draw (comp) and of the stacked phantom (e) inside
r <= 2 cells (of r <= 12); cumulative src.  Statement rule (frozen): "the (1 - m) draw stops emptying cores" iff M(<= 2)/M_S0 for V1-U is
closer to 1 than for PROP AND V1-U's draw share inside 2 cells is lower than PROP's.
Run: nice -n 10 python3 campaign_fresh_gravity/CFG501_draw_from_unsettled/cfg501_halo_stack.py
"""
import os, sys, json
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(E, "cfg501_work")
M, L = 256, 200.0
NH, SEP, RMAX = 200, 8, 12
Om = (0.02237 + 0.1200) / 0.6736 ** 2; FB = 0.02237 / (0.02237 + 0.1200)
SC0 = 1.5 * Om * (1.0 - FB)                                                   # mean cold source at a = 1 (engine units)
OUT, RES = [], {"lane": "CFG501", "script": "cfg501_halo_stack"}


def P(s=""):
    print(s, flush=True); OUT.append(s)


def deposit(pos):
    dx = L / M; u = pos / dx; i0 = np.floor(u).astype(np.int64); w = (u - i0).astype(np.float32)
    i1 = (i0 + 1) % M; i0 = i0 % M; rho = np.zeros(M ** 3, np.float64)
    for cx in (0, 1):
        ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
        for cy in (0, 1):
            iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
            for cz in (0, 1):
                iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                rho += np.bincount((ix * M + iy) * M + iz, weights=wx * wy * wz, minlength=M ** 3)
    rho = rho.reshape((M,) * 3); return (rho / rho.mean()).astype(np.float32)


smooth = lambda g: ndimage.gaussian_filter(g.astype(np.float32), 1.0, mode="wrap")
rho0 = deposit(np.load(os.path.join(E, "cfg359_work", "cfg359_S0_FLAT_canonical_N256_z0.npz"))["pos"])
s0 = smooth(rho0)
pk = (s0 == ndimage.maximum_filter(s0, size=3, mode="wrap"))
cand = np.argwhere(pk); val = s0[pk]; order = np.argsort(-val)
cent = []
for i in order:
    c = cand[i]
    if all(np.sqrt(np.sum((((c - d + M // 2) % M) - M // 2) ** 2)) >= SEP for d in cent):   # periodic separation >= 8 cells
        cent.append(c)
    if len(cent) == NH:
        break
cent = np.array(cent)
P(f"S0 (CFG359): {len(cand)} smoothed peaks; top {NH} centres, smoothed 1+delta {s0[tuple(cent.T)].min():.1f}-{s0[tuple(cent.T)].max():.1f}")
off = np.array([(i, j, k) for i in range(-RMAX, RMAX + 1) for j in range(-RMAX, RMAX + 1) for k in range(-RMAX, RMAX + 1)
                if i * i + j * j + k * k <= (RMAX + 0.5) ** 2])
rr = np.sqrt((off ** 2).sum(1)); shell = np.minimum(np.floor(rr + 0.5).astype(int), RMAX)   # shell n = cells at distance in [n-0.5, n+0.5)
loc = np.array([(i, j, k) for i in range(-2, 3) for j in range(-2, 3) for k in range(-2, 3)])


def recentre(sm):
    out = []
    for c in cent:
        idx = (c[None] + loc) % M
        out.append(idx[np.argmax(sm[idx[:, 0], idx[:, 1], idx[:, 2]])])
    return np.array(out)


def stack(fields, cen):
    prof = {k: np.zeros(RMAX + 1) for k in fields}; cnt = np.bincount(shell, minlength=RMAX + 1).astype(float)
    tot = {k: np.zeros(RMAX + 1) for k in fields}
    for c in cen:
        idx = (c[None] + off) % M
        for k, g in fields.items():
            v = g[idx[:, 0], idx[:, 1], idx[:, 2]].astype(np.float64)
            tot[k] += np.bincount(shell, weights=v, minlength=RMAX + 1)
    for k in fields:
        prof[k] = tot[k] / (cnt * len(cen))
    return prof, tot


RUNS = {"S0 (CFG359)": None, "PROP (CFG498 weight)": "V1_CAP_PROP_RES_TA_MIXA_FLAT_canonical", "V1-U": "V1_CAP_U_RES_TA_MIXA_FLAT_canonical",
        "V2-U": "V2_CAP_U_RES_TA_MIXA_FLAT_canonical", "MUTATE-N (no comp)": "V1_CAP_U_NOCOMP_RES_TA_MIXA_FLAT_canonical"}
PR, TOT = {}, {}
for name, tag in RUNS.items():
    if tag is None:
        f = {"rho": rho0}; cen = cent
    else:
        p = os.path.join(W, f"cfg501_{tag}_N256_z0_fields.npz")
        if not os.path.exists(p):
            P(f"  {name}: PENDING"); continue
        d = np.load(p)
        f = {"rho": d["rho"], "e": d["e"] / SC0, "comp": d["comp"] / SC0, "m": d["SW"]}
        f["src"] = f["e"] - f["comp"]
        cen = recentre(smooth(f["rho"]))
    PR[name], TOT[name] = stack(f, cen)
    RES.setdefault("recentre_shift_mean_cells", {})[name] = float(np.mean(np.sqrt((((cen - cent + M // 2) % M - M // 2) ** 2).sum(1))))
cum = lambda t, R: float(t[:R + 1].sum())
RES["profiles"] = {n: {k: v.tolist() for k, v in pr.items()} for n, pr in PR.items()}
P(f"\nstacked mean profiles (shell n = distance n +- 0.5 cells; 1 cell = {L / M:.3f} Mpc/h); e, comp, src in units of the mean cold source")
for n, pr in PR.items():
    P(f"  {n}")
    for k in pr:
        P(f"    {k:5s} " + " ".join(f"{x:8.3f}" for x in pr[k][:9]) + "  ... r=12: " + f"{pr[k][12]:.3f}")
if "S0 (CFG359)" in TOT:
    P("\nenclosed mass ratio M_run(<= r) / M_S0(<= r), draw share and phantom share inside r <= 2 cells (of r <= 12):")
    RES["enclosed"] = {}
    for n, t in TOT.items():
        if n.startswith("S0"):
            continue
        rat = {R: cum(t["rho"], R) / cum(TOT["S0 (CFG359)"]["rho"], R) for R in (1, 2, 3, 6)}
        dsh = cum(t["comp"], 2) / max(cum(t["comp"], RMAX), 1e-30) if cum(t["comp"], RMAX) > 0 else float("nan")
        esh = cum(t["e"], 2) / max(cum(t["e"], RMAX), 1e-30)
        csrc = {R: cum(t["src"], R) / cum(TOT["S0 (CFG359)"]["rho"], R) / (1 - FB) for R in (1, 2, 3, 6, 12)}
        RES["enclosed"][n] = dict(M_ratio=rat, draw_share_r2=dsh, phantom_share_r2=esh, cum_src_over_cold_S0=csrc,
                                  m_core=float(PR[n]["m"][0]), m_r6=float(PR[n]["m"][6]))
        P(f"  {n:22s} M ratio r<=1/2/3/6: {rat[1]:.3f} / {rat[2]:.3f} / {rat[3]:.3f} / {rat[6]:.3f};  draw share r<=2: {dsh:.3f};  phantom share r<=2: {esh:.3f};  "
          f"m centre {PR[n]['m'][0]:.3f}, m(r=6) {PR[n]['m'][6]:.3f}")
        P(f"  {'':22s} cumulative src(<= r) / S0 cold mass(<= r), r = 1/2/3/6/12: " + " / ".join(f"{csrc[R]:+.3f}" for R in (1, 2, 3, 6, 12)))
    a, b = RES["enclosed"].get("V1-U"), RES["enclosed"].get("PROP (CFG498 weight)")
    if a and b:
        closer = abs(a["M_ratio"][2] - 1) < abs(b["M_ratio"][2] - 1)
        lower = a["draw_share_r2"] < b["draw_share_r2"]
        RES["stops_emptying_cores"] = bool(closer and lower)
        P(f"\nfrozen statement rule: V1-U M(<=2)/M_S0 closer to 1 than PROP: {closer} ({a['M_ratio'][2]:.3f} vs {b['M_ratio'][2]:.3f}); "
          f"V1-U draw share r<=2 lower than PROP: {lower} ({a['draw_share_r2']:.3f} vs {b['draw_share_r2']:.3f})")
        P(f"=> 'the (1 - m) draw stops emptying cores': {'YES' if RES['stops_emptying_cores'] else 'NO (not stated)'}")
RES["n_halos"] = int(len(cent))
json.dump(RES, open(os.path.join(HERE, "cfg501_halo_stack_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg501_halo_stack.out"), "w").write("\n".join(OUT) + "\n")

"""SV4 iter_3: AGC 114905's external field from the whole local matter distribution (FROZEN_CRITERIA.md).

Catalogue: data_assembly/alfalfa_sdss_local_control/alfalfa_sdss.csv (committed). Window from the 1D EFE estimator
with the exact-field factor from iter_1's KA0 solve (iter_1/iter1.json). usage: python3 iter3_large_scale_field.py
[main|MUTATE]  (MUTATE: planted 2 x M_req host at QX14's d_min). kappa = 1/2 FITTED; not theory closed.
"""
import json, os, sys
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); LANE = os.path.dirname(HERE); sys.path.insert(0, LANE)
import sv4_common as C

MODE = sys.argv[1] if len(sys.argv) > 1 else "main"
P = C.Log(); RES = dict(mode=MODE)
P(f"SV4 iter_3 large-scale field, mode {MODE}. kappa = 1/2 FITTED; not theory closed.")
G = 4.30091e-6                                     # kpc (km/s)^2 / Msun
CAT = os.path.join(C.ROOT, "data_assembly", "alfalfa_sdss_local_control", "alfalfa_sdss.csv")
qx4_2 = json.load(open(os.path.join(C.QX4, "iter2.json")))["AGC114905"]
qx14 = json.load(open(os.path.join(C.ROOT, "closure_2026_11_06", "QX14_agc114905_census", "qx14.json")))
it1 = json.load(open(os.path.join(LANE, "iter_1", "iter1.json")))

# ------------------------------------------------------------------ window on the exact field
ns = C.load_qx4(); ud1 = ns["ud1"]
Rk, V, E, vb2 = (np.asarray(ud1[k]) for k in ("Rk", "V", "E", "vb2"))


def v_alg(a0, ge):
    gN = vb2 / Rk * C.CONV; gt = gN + ge * a0
    g = C.nu(gt / a0) * gt - (C.nu(ge) * ge * a0 if ge > 0 else 0.0)
    return np.sqrt(np.maximum(g / C.CONV * Rk, 0))


GE = np.exp(np.linspace(np.log(1e-4), np.log(3.0), 2000))
RES["window"] = {}
for f, a0 in C.FOOT.items():
    T = np.asarray(it1["footings"][f]["V_model"]) / v_alg(a0, 0.0)
    pe = np.array([C.chi2p(V, E, v_alg(a0, ge) * T)[1] for ge in GE]); pa = np.array([C.chi2p(V, E, v_alg(a0, ge))[1] for ge in GE])
    ok, oka = GE[pe >= 0.05], GE[pa >= 0.05]
    w = [float(ok.min()), float(ok.max())] if len(ok) else None; wa = [float(oka.min()), float(oka.max())]
    ka3 = max(abs(wa[0] / qx4_2[f]["p_ok"][0] - 1), abs(wa[1] / qx4_2[f]["p_ok"][1] - 1))
    RES["window"][f] = dict(exact=w, algebraic=wa, KA3=ka3, KA3_ok=bool(ka3 <= 0.02), T=T.tolist())
    P(f"[{f}] window (p >= 0.05) exact field {np.round(w,4).tolist() if w else None} a0; algebraic {np.round(wa,4).tolist()}"
      f" vs QX4 {np.round(qx4_2[f]['p_ok'],4).tolist()}: KA3 {ka3:.4f} (line 0.02) -> {'PASS' if ka3 <= 0.02 else 'FAIL'}")

# ------------------------------------------------------------------ catalogue
df = pd.read_csv(CAT, dtype={"sdss_objid": str})
ra = df["ra_dur_deg"].fillna(df["ra_hi_deg"]).to_numpy(); dec = df["dec_dur_deg"].fillna(df["dec_hi_deg"]).to_numpy()
D = df["dist_mpc"].to_numpy(float); eD = df["e_dist_mpc"].to_numpy(float)
lms = df[["logms_taylor", "logms_mcgaugh", "logms_gswlc"]].max(axis=1, skipna=True).to_numpy()
Ms = np.where(np.isfinite(lms), 10 ** np.nan_to_num(lms, nan=-99), 0.0)
Mb = Ms + 1.33 * 10 ** df["logmhi"].to_numpy(float)
self_ = (df["agc"] == 114905).to_numpy()
assert self_.sum() == 1
r0 = dict(ra=float(ra[self_][0]), dec=float(dec[self_][0]), D=float(D[self_][0]), eD=float(eD[self_][0]))
P(f"catalogue {len(df)} rows; AGC 114905 row RA {r0['ra']:.5f} Dec {r0['dec']:.5f} D {r0['D']} +- {r0['eD']} Mpc;"
  f" stellar mass present for {np.isfinite(lms).sum()} rows")
RES["catalogue"] = dict(rows=int(len(df)), target=r0, n_mstar=int(np.isfinite(lms).sum()))


def unit(ra_, dec_):
    a, d = np.radians(ra_), np.radians(dec_); return np.stack([np.cos(d) * np.cos(a), np.cos(d) * np.sin(a), np.sin(d)], -1)


# f_sky: equal-area cells, RA step 2 deg x sin(Dec) step 2/57.3
nra = 180; nsd = int(round(2.0 / (2.0 / 57.3))); sdb = np.linspace(-1, 1, nsd + 1)
ira = np.clip((np.mod(ra, 360) / 2.0).astype(int), 0, nra - 1); isd = np.clip(np.searchsorted(sdb, np.sin(np.radians(dec))) - 1, 0, nsd - 1)
f_sky = len(set(zip(ira.tolist(), isd.tolist()))) / (nra * nsd)
P(f"f_sky (occupied equal-area cells) = {f_sky:.4f} ({f_sky*41253:.0f} deg^2)")
RES["f_sky"] = f_sky
F_C = 10.0
oth = ~self_
n0 = unit(r0["ra"], r0["dec"]); ni = unit(ra[oth], dec[oth]); Di, eDi, Mi = D[oth], eD[oth], Mb[oth]
def field(D0, e0, extra=None):
    cth = np.clip(ni @ n0, -1, 1)
    pos = Di[:, None] * ni - D0 * n0[None, :]; d = np.linalg.norm(pos, axis=1)          # Mpc
    sc = 2 * np.sqrt(eDi ** 2 + e0 ** 2)
    Dp = np.clip(D0 * cth, np.maximum(Di - sc, 0), Di + sc)                               # closest allowed D'
    deff = np.sqrt(np.maximum(Dp ** 2 + D0 ** 2 - 2 * Dp * D0 * cth, 0))
    out = {}
    for Rmax in (50.0, 100.0, 200.0):
        s = d < Rmax
        gv = G * (Mi[s, None] * (pos[s] * 1e3) / ((d[s, None] * 1e3) ** 3)).sum(0)
        if extra is not None:
            Mx, dx = extra; gv = gv + np.array([G * Mx / dx ** 2, 0.0, 0.0])               # planted host, perpendicular
        gs = G * np.sum(Mi[s] / np.maximum(deff[s] * 1e3, 1e-3) ** 2)
        if extra is not None: gs += G * extra[0] / extra[1] ** 2
        top = np.argsort(-(Mi[s] / np.maximum(deff[s], 1e-6) ** 2))[:5]
        out[Rmax] = dict(n=int(s.sum()), g_vec=float(np.linalg.norm(gv) * C.CONV), g_scalar=float(gs * C.CONV),
                         g_bound=float(gs * C.CONV * F_C / f_sky), min_deff=float(deff[s].min()),
                         top5=[dict(M=float(Mi[s][j]), d=float(d[s][j]), deff=float(deff[s][j])) for j in top])
    return out


RES["field"] = {}; RES["labels"] = {}
for f, a0 in C.FOOT.items():
    extra = None
    if MODE == "MUTATE":
        extra = (2 * qx14["M_req"][f]["M"], qx14["M_req"][f]["d_kpc"])
    for place, (D0, e0) in (("catalogue_D75.7", (r0["D"], r0["eD"])), ("D78.7", (78.7, 1.5))):
        fl = field(D0, e0, extra); RES["field"][f"{f}_{place}"] = {str(k): v for k, v in fl.items()}
        for Rmax, v in fl.items():
            P(f"[{f} {place}] R_max {Rmax:.0f} Mpc: N {v['n']}, min d_eff {v['min_deff']:.2f} Mpc; g_vec {v['g_vec']/a0:.2e} a0,"
              f" scalar {v['g_scalar']/a0:.2e} a0, bound (x{F_C:.0f}/f_sky) {v['g_bound']/a0:.2e} a0")
    w = RES["window"][f]["exact"]; v = RES["field"][f"{f}_catalogue_D75.7"]["200.0"]
    lab = {}
    for rd in ("N", "M"):
        gb = v["g_bound"] / a0; gv = v["g_vec"] / a0
        if rd == "M": gb = float(C.nu(gb) * gb); gv = float(C.nu(gv) * gv)
        if w is None: L = "n/a (no window)"
        elif gb < w[0]: L = "NOT RESCUED (field excluded)"
        elif w[0] <= gv <= w[1]: L = "RESCUED (field supplied)"
        elif gv > w[1]: L = "field above window"
        else: L = "NOT EVALUABLE (bound too loose)"
        lab[rd] = dict(g_bound=gb, g_vec=gv, window_low=w[0] if w else None, label=L,
                       Fc_to_reach=(w[0] / (v["g_bound"] / a0) * F_C) if (w and rd == "N") else None)
        P(f"[{f}] reading {rd}: bound {gb:.2e} a0, vector {gv:.2e} a0 vs window low edge {w[0] if w else None:.4f} -> {L}"
          + (f"; F_c needed to reach the window {lab[rd]['Fc_to_reach']:.0f}" if rd == "N" and w else ""))
    RES["labels"][f] = lab
    if MODE == "MUTATE":
        bite = lab["N"]["label"] != "NOT RESCUED (field excluded)"; RES["labels"][f]["MUTATE_bites"] = bool(bite)
        P(f"[{f}] MUTATE planted {extra[0]:.2e} Msun at {extra[1]:.0f} kpc: label flips away from NOT RESCUED: {bite}")
P.save(os.path.join(HERE, "iter3_MUTATE" if MODE == "MUTATE" else "iter3"), RES)

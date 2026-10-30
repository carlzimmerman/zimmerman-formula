#!/usr/bin/env python3
"""GH6 power gate: FRB positions and z x DESI DR1 centrals, Zhang gas column, Fisher S. DMexgal is never read here."""
import os, sys, json, math
os.environ["OMP_NUM_THREADS"] = "1"
import numpy as np, healpy as hp
from astropy.io import fits
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "_external_data")
RES = {"checks": {}}
def check(n, ok, msg): RES["checks"][n] = bool(ok); print(("PASS " if ok else "FAIL ") + n + ": " + msg, flush=True)
H_NAT, OM = 0.679, 0.3085; DH = 299792.458 / (100 * H_NAT)
ZZ = np.linspace(0, 3, 12001); EE = np.sqrt(OM * (1 + ZZ) ** 3 + 1 - OM)
CH = np.r_[0, np.cumsum(.5 * (1 / EE[1:] + 1 / EE[:-1]) * np.diff(ZZ))]; DZ = np.r_[0, np.cumsum(.5 * ((1 + ZZ[1:]) / EE[1:] + (1 + ZZ[:-1]) / EE[:-1]) * np.diff(ZZ))]
def DA(z): return DH * np.interp(z, ZZ, CH) / (1 + z)
ZTF = np.array([[9, 82.0], [9.5, 102.0], [10, 131.0], [10.5, 178.0], [10.75, 210.0], [11.0, 295.0], [11.25, 480.0], [11.5, 950.0]])
def Rv(l): return np.interp(l, ZTF[:, 0], ZTF[:, 1])
BETA, RCK, NORM, MUE = 0.43, 6.0, 1.84, 1.14
MP, MSUN, KPC, PC = 1.67262192e-27, 1.98847e30, 3.0856776e19, 3.0856776e16

XG = np.r_[0, np.geomspace(.001, 3.0, 400)]; LG = np.array([10., 10.25, 10.5, 10.6, 10.75, 10.9, 11., 11.25, 11.5]); KS = (1.0, 1.8, 3.0)
def column_table(l, k):
    """N_e in pc cm^-3 on the XG = R/R_vir grid, for one lens of log M* l, cut at k R_vir."""
    Rvk = float(Rv(l)); rr = np.linspace(0, Rvk, 20001); sh = (1 + (rr / RCK) ** 2) ** (-1.5 * BETA)
    rho0 = NORM * 10 ** l * MSUN / (np.trapz(4 * np.pi * rr ** 2 * sh, rr) * KPC ** 3); ne0 = rho0 / (MUE * MP)   # m^-3
    out = np.zeros_like(XG); rc = k * Rvk
    for i, x in enumerate(XG):
        R = x * Rvk
        if R >= rc: continue
        ll = np.linspace(0, math.sqrt(rc ** 2 - R ** 2), 3001)
        out[i] = 2 * np.trapz((1 + (R * R + ll * ll) / RCK ** 2) ** (-1.5 * BETA), ll) * KPC
    return ne0 * out / PC * 1e-6                                              # m^-2 -> pc cm^-3
TAB = {k: np.array([column_table(l, k) for l in LG]) for k in KS}
def dm_one(x, l, k):
    t = TAB[k]; a = np.array([np.interp(x, XG, t[j], right=0.0) for j in range(len(LG))])
    j = np.clip(np.searchsorted(LG, l) - 1, 0, len(LG) - 2); f = (l - LG[j]) / (LG[j + 1] - LG[j]); n = np.arange(len(x))
    return (1 - f) * a[j, n] + f * a[j + 1, n]

# K1, K2
_R, _rc = 30.0, 6.0; _ll = np.linspace(0, 3e5, 3_000_001)
k1 = 2 * np.trapz((1 + (_R ** 2 + _ll ** 2) / _rc ** 2) ** -1.0, _ll) / (math.pi * _rc ** 2 / math.sqrt(_rc ** 2 + _R ** 2)) - 1
check("K1_projection_closed_form", abs(k1) < 1e-4, f"{k1:+.1e}")
_l = 10.75; _rv = float(Rv(_l)); _x = np.linspace(0, 1, 40001); _t = np.interp(_x, XG, TAB[1.0][LG.tolist().index(10.75)], right=0)
_m = np.trapz(2 * np.pi * _x * _t, _x) * (_rv * KPC) ** 2 * PC * 1e6 * MUE * MP / MSUN / (NORM * 10 ** _l) - 1
check("K2_area_integral_mass", abs(_m) < 0.01, f"{_m:+.2e}")

# ---- catalogues
W = os.path.join(EXT, "gh6_work"); os.makedirs(W, exist_ok=True); CACHE = os.path.join(W, "gh6_bgs.npz")
if not os.path.exists(CACHE):
    h = fits.open(os.path.join(EXT, "desi_dr1_bgs", "BGS_BRIGHT_full_HPmapcut.dat.fits"), memmap=True)[1].data
    ra, de, z, zw, dc = [np.array(h[k]) for k in ("RA", "DEC", "Z_not4clus", "ZWARN", "DELTACHI2")]; tid = np.array(h["TARGETID"])
    g = (zw == 0) & (dc > 40) & (z > 0.005) & (z < 0.6); ra, de, z, tid = ra[g], de[g], z[g], tid[g]
    c = fits.open(os.path.join(EXT, "desi_dr1_cigale", "IronPhysProp_v1.2.fits"), memmap=True)[1].data
    ct, cm = np.array(c["TARGETID"]), np.array(c["LOGM"]); kk = (np.char.strip(np.array(c["SURVEY"]).astype(str)) == "main") & (np.char.strip(np.array(c["PROGRAM"]).astype(str)) == "bright"); ct, cm = ct[kk], cm[kk]
    s = np.argsort(ct); i = np.searchsorted(ct[s], tid); i[i >= len(s)] = 0; ok = ct[s][i] == tid; lm = np.full(len(z), np.nan); lm[ok] = cm[s][i[ok]]
    m = np.isfinite(lm); ra, de, z, lm = ra[m], de[m], z[m], lm[m]; print("BGS with mass", len(z), flush=True)
    np.savez(CACHE, ra=ra, de=de, z=z, lm=lm); sys.stdout.flush(); os.execv(sys.executable, [sys.executable] + sys.argv)   # restart so the memory-mapped catalogues leave RSS
D_ = np.load(CACHE); ra, de, z, lm = D_["ra"], D_["de"], D_["z"], D_["lm"]; print("BGS with mass", len(z), flush=True)
U = np.c_[np.cos(np.radians(de)) * np.cos(np.radians(ra)), np.cos(np.radians(de)) * np.sin(np.radians(ra)), np.sin(np.radians(de))]; T = cKDTree(U)
DAg = DA(z); NS = 128; OCC = np.zeros(hp.nside2npix(NS), bool); OCC[hp.ang2pix(NS, ra, de, lonlat=True)] = True
def in_foot(r, d):
    v = hp.ang2vec(r, d, lonlat=True); p = hp.query_disc(NS, v, np.radians(1.0)); return OCC[p].mean() >= 0.9
WIDE = (lm >= 10.0) & (lm <= 11.5) & (z >= 0.01); IW = np.where(WIDE)[0]; TW = cKDTree(U[IW]); CEN = {}
def is_central(i):
    if i not in CEN:
        q = np.asarray(T.query_ball_point(U[i], 2 * math.sin(1.0 / DAg[i] / 2))); q = q[q != i]
        q = q[np.abs(z[q] - z[i]) / (1 + z[i]) * 299792.458 < 2000]; CEN[i] = not np.any(lm[q] > lm[i])
    return CEN[i]
RAD = 2 * math.sin(np.radians(4.5) / 2); OFF = 2 * np.log10(0.704 / H_NAT)
def sightline(r, d, zf):
    """m(k) for one FRB, for (primary, wide) lens sets; also the crossing count within k R_vir."""
    v = hp.ang2vec(r, d, lonlat=True); J = IW[TW.query_ball_point(v, RAD)]; J = J[z[J] < zf - 0.005]
    res = {k: [0.0, 0.0] for k in KS}; ncross = [0, 0]
    if not len(J): return res, ncross
    sep = 2 * np.arcsin(np.linalg.norm(U[J] - v, axis=1) / 2); l = lm[J] + OFF; x = sep * DAg[J] * 1e3 / Rv(l); use = x < 3.0; J, x, l = J[use], x[use], l[use]
    if not len(J): return res, ncross
    cen = np.array([is_central(int(i)) for i in J]); J, x, l = J[cen], x[cen], l[cen]
    if not len(J): return res, ncross
    prim = (lm[J] >= 10.6) & (lm[J] <= 11.0)
    for k in KS:
        d1 = dm_one(x, l, k) / (1 + z[J]); res[k] = [float(d1[prim].sum()), float(d1.sum())]
    ncross = [int(prim.sum()), int(len(J))]
    return res, ncross

# ---- FRBs: positions and z only; DMexgal is never loaded
import csv
F = os.path.join(EXT, "frb_sharma26", "repo", "data", "frb_results", "frb_sample.csv"); FR = []
for row in csv.DictReader(open(F)): FR.append((float(row["ra[deg]"]), float(row["dec[deg]"]), float(row["z_sample"]), row["sharma_sample"]))
fr = np.array([f[:3] for f in FR]); ss = np.array([f[3] for f in FR])
B = np.load(os.path.join(EXT, "frb_sharma26", "repo", "data", "frb_results", "DMvar_Sharma2026.npz"))
def sig(zf): return np.sqrt(np.interp(zf, B["z"], B["median"]) ** 2 + (117.0 / (1 + zf)) ** 2)
def S_of(zf, vec, weights=None):
    w = 1 / sig(zf) ** 2; X = np.c_[np.ones_like(zf), np.interp(zf, ZZ, DZ)]
    Wx = X * w[:, None]; P = np.diag(w) - Wx @ np.linalg.solve(X.T @ Wx, Wx.T); return float(np.sqrt(max(vec @ P @ vec, 0)))
def build(sel):
    idx = [i for i in sel if in_foot(fr[i, 0], fr[i, 1])]; Z_ = fr[idx, 2]; M = {k: np.zeros((len(idx), 2)) for k in KS}; NC = np.zeros((len(idx), 2))
    for n, i in enumerate(idx):
        res, nc = sightline(fr[i, 0], fr[i, 1], fr[i, 2]); NC[n] = nc
        for k in KS: M[k][n] = res[k]
    return idx, Z_, M, NC
def report(name, sel):
    idx, Z_, M, NC = build(np.where(sel)[0]); out = {"N_all": int(sel.sum()), "N_foot": len(idx), "z_median": float(np.median(Z_))}; print(f"--- {name}: {sel.sum()} FRBs, {len(idx)} in footprint, median z {np.median(Z_):.3f}, median sigma {np.median(sig(Z_)):.0f}", flush=True)
    for j, lab in enumerate(("primary", "wide")):
        a, b, c = M[1.0][:, j], M[1.8][:, j], M[3.0][:, j]; r = {"S1": S_of(Z_, a), "S18": S_of(Z_, b), "S3": S_of(Z_, c), "S18m1": S_of(Z_, b - a), "S3m1": S_of(Z_, c - a), "mean_m1": float(a.mean()), "mean_m18": float(b.mean()), "mean_m3": float(c.mean()), "mean_crossings_3Rv": float(NC[:, j].mean())}
        r["N_for_G1"] = float(9 / r["S1"] ** 2 * len(idx)) if r["S1"] > 0 else None; r["N_for_G2"] = float(9 / r["S18m1"] ** 2 * len(idx)) if r["S18m1"] > 0 else None; out[lab] = r
        print(f"{lab}: mean m(1/1.8/3) {a.mean():.1f}/{b.mean():.1f}/{c.mean():.1f} pc/cm3, crossings<3Rv {NC[:, j].mean():.2f}; S1 {r['S1']:.2f} S1.8 {r['S18']:.2f} S3 {r['S3']:.2f}; S(1.8-1) {r['S18m1']:.2f} S(3-1) {r['S3m1']:.2f}; N for G1 {r['N_for_G1']}, G2 {r['N_for_G2']}", flush=True)
    return out, idx, Z_, M
P_, idx, Z_, M = report("PRIMARY yes", ss == "yes"); RES["primary_sample"] = P_; RES["extended_sample"] = report("yes+unclear", (ss == "yes") | (ss == "unclear"))[0]

# ---- K3, K4: Gaussian mocks with the same sigma_i
rng = np.random.default_rng(66); a = M[1.0][:, 0]; sg = sig(Z_); w = 1 / sg ** 2; Sf = P_["primary"]["S1"]
Sm = Sf; RES["K34_vector"] = "primary m(1)"
if Sf == 0:                                                                     # no crossing: K3/K4/MUTATE need a nonzero vector, so they exercise the wide m(3)
    a = M[3.0][:, 1]; Sm = S_of(Z_, a); RES["K34_vector"] = "wide m(3), primary m(1) is identically zero"; print("primary m(1) is zero: K3, K4, MUTATE use wide m(3)", flush=True)
X = np.c_[np.ones_like(Z_), np.interp(Z_, ZZ, DZ), a]
C = np.linalg.inv((X * w[:, None]).T @ X)
Ah = np.array([C[2] @ (X * w[:, None]).T @ (a + rng.normal(0, sg)) for _ in range(2000)])
ratio = Ah.std() * Sm; check("K3_fisher_vs_mocks", abs(ratio - 1) < 0.1, f"scatter x S = {ratio:.3f}")
zk = (Ah.mean() - 1) / (Ah.std() / math.sqrt(2000)); check("K4_injection_recovery", abs(zk) < 3, f"mean A {Ah.mean():.3f}, {zk:+.2f} se")

# ---- MUTATE
check("MUTATE_linearity", abs(S_of(Z_, 10 * a) / Sm - 10) < 1e-9, f"S(10m)/S(m) = {S_of(Z_, 10 * a) / Sm:.6f}")
SR = []
for n in range(20):
    ai = []; zi = []
    for i in idx:
        for _ in range(200):
            r = rng.uniform(0, 360)
            if in_foot(r, fr[i, 1]): ai.append(sightline(r, fr[i, 1], fr[i, 2])[0][1.0 if Sf > 0 else 3.0][0 if Sf > 0 else 1]); zi.append(fr[i, 2]); break
    SR.append(S_of(np.array(zi), np.array(ai)))
rr = float(np.mean(SR) / Sm); check("MUTATE_rotated_positions", 0.5 <= rr <= 2, f"mean rotated S {np.mean(SR):.2f} (std {np.std(SR):.2f}) vs true {Sm:.2f}, ratio {rr:.2f}")
RES["rotated_S"] = [float(x) for x in SR]

g1 = Sf >= 3; g2 = P_["primary"]["S18m1"] >= 3; RES["G1"] = bool(g1); RES["G2"] = bool(g2)
RES["outcome"] = "NON-DIAGNOSTIC" if not g1 else ("AMPLITUDE ONLY" if not g2 else "MEASUREMENT RUNS")
print(f"GATE: G1 S={Sf:.2f} ({'PASS' if g1 else 'FAIL'}); G2 S={P_['primary']['S18m1']:.2f} ({'PASS' if g2 else 'FAIL'}) -> {RES['outcome']}", flush=True)
json.dump(RES, open(os.path.join(HERE, "gh6_gate.json"), "w"), indent=1, sort_keys=True); sys.exit(0 if all(RES["checks"].values()) else 1)

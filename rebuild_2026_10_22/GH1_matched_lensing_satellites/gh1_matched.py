#!/usr/bin/env python3
"""GH1_matched_lensing_satellites: KiDS-1000 lensing around exactly X75's GAMA G09 central hosts (CFG652's estimator,
native background), fitted with X75's route E model (common log M200 shift over EM1's SPARC relation) at 50-300 kpc and
compared with X75's satellite shift on the same hosts. Frozen criteria: FROZEN_CRITERIA.md (45f918f379). One thread.
kappa = 1/2 FITTED; c_f EXTERNAL; footings never pooled; not theory closed; nothing here says the data favour the framework.
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 gh1_matched.py           [GH1_MUTATE=1: sources rotated 45 deg]
"""
import os, sys, io, json, math, time, contextlib, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
for _v in ("X53_MUTATE", "X75_MUTATE", "X75_MAXNFOF"): os.environ.pop(_v, None)
import numpy as np
from scipy.spatial import cKDTree
T0 = time.time()
MUT = os.environ.get("GH1_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
WORK = os.path.join(os.path.dirname(REPO), "_external_data", "cfg652_work")
OUT, CHK = [], {}
def P(s=""): print(s, flush=True); OUT.append(str(s))
def check(k, ok, v): CHK[k] = bool(ok); P(f"  {k}: {'PASS' if ok else 'FAIL'} ({v})")
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9

# ------------------------------------------------------------ X75 hosts + model machinery (read-only)
S75 = os.path.join(REB, "X75_satellite_kinematics_mass_gap", "x75_satkin.py"); s75 = open(S75).read()
s75 = s75[:s75.index("# ============================================================ measurement")]
G75 = {"__file__": S75, "__name__": "x75_ro"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s75, S75, "exec"), G75)
H, hbin, lmH, zH, raH, deH = G75["H"], G75["hbin"], G75["lm"][G75["H"]], G75["z"][G75["H"]], G75["ra"][G75["H"]], G75["dec"][G75["H"]]
cnt = [int((hbin == b).sum()) for b in range(4)]; pcnt = G75["RES"]["counts"]["pairs"]
check("K2_host_sample_equals_X75", cnt == [3651, 2411, 1690, 1297] and pcnt == [318, 468, 574, 727], f"hosts {cnt}, pairs {pcnt}")
NS = G75["NS"]["S"]; NF = NS["NF"]; AQ = NF["AQ"]; chi_flat = NF["chi_flat"]; OM_NAT = NF["OM_NAT"]; H_NAT = NS["H_NAT"]
P(f"GH1  criteria 45f918f379{'  [MUTATE: sources rotated 45 deg]' if MUT else ''}; X75 hosts + X53 smooth machinery loaded [{time.time() - T0:.0f} s]")

# ------------------------------------------------------------ CFG652 estimator (constants and logic copied exactly)
c_ms = 2.998e8; G_SI = 6.674e-11; Mpc = 3.0857e22; TO_MSUN_PC2 = (3.0857e16) ** 2 / 1.989e30
RB = np.geomspace(30, 3000, 13); RC = np.sqrt(RB[1:] * RB[:-1]); NB = len(RC); NPATCH = 30


def DC_cfg652(z, n=4096):
    H0SI = 70 * 1e3 / Mpc
    zz = np.linspace(0, max(float(np.max(z)), 2.0), n); E = np.sqrt(0.3 * (1 + zz) ** 3 + 0.7)
    chi = np.concatenate([[0], np.cumsum(0.5 * (1 / E[1:] + 1 / E[:-1]) * np.diff(zz))]) * (c_ms / H0SI) / Mpc
    return np.interp(z, zz, chi)


def DC_native(z):
    return chi_flat(np.asarray(z, float), OM_NAT) * (c_ms / (H_NAT * 100e3 / Mpc)) / Mpc


S = np.load(os.path.join(WORK, "cfg652_sources.npz"))
sra, sde, e1, e2, w, zB = (S[k] for k in ("RAJ2000", "DECJ2000", "e1", "e2", "weight", "Z_B"))
if MUT:
    e1, e2 = -e2, e1                                                     # 45-degree rotation: e_t -> e_x
tree = cKDTree(np.c_[np.radians(sra), np.radians(sde)])


def stack(ra, de, z, DC):
    chiS = DC(zB)
    n = len(z); WG = np.zeros((n, NB)); WX = np.zeros((n, NB)); WW = np.zeros((n, NB)); NN = np.zeros((n, NB))
    chil = DC(z)
    for i in range(n):
        th = 3000.0 / (chil[i] / (1 + z[i]) * 1000.0)
        ii = np.array(tree.query_ball_point([math.radians(ra[i]), math.radians(de[i])], th), int)
        if ii.size < 5:
            continue
        ii = ii[zB[ii] > z[i] + 0.2]
        if ii.size < 5:
            continue
        dra = (np.radians(sra[ii]) - math.radians(ra[i])) * math.cos(math.radians(de[i])); dde = np.radians(sde[ii]) - math.radians(de[i])
        R = np.hypot(dra, dde) * chil[i] / (1 + z[i]) * 1000.0
        phi = np.arctan2(dde, dra)
        et = -(e1[ii] * np.cos(2 * phi) - e2[ii] * np.sin(2 * phi))
        ex = (e1[ii] * np.sin(2 * phi) + e2[ii] * np.cos(2 * phi))
        Dl = chil[i] / (1 + z[i]); Dls = (chiS[ii] - chil[i]) / (1 + zB[ii]); Ds = chiS[ii] / (1 + zB[ii])
        isc = np.clip(4 * math.pi * G_SI / c_ms ** 2 * (Dl * Mpc) * (Dls / Ds), 0, None)
        k = np.digitize(R, RB) - 1
        ok = (k >= 0) & (k < NB) & (isc > 0)
        ww = (w[ii] * isc ** 2)[ok]; kk = k[ok]
        np.add.at(WG[i], kk, ww * et[ok] / isc[ok] * TO_MSUN_PC2)
        np.add.at(WX[i], kk, ww * ex[ok] / isc[ok] * TO_MSUN_PC2)
        np.add.at(WW[i], kk, ww); np.add.at(NN[i], kk, w[ii][ok])
    return WG, WX, WW, NN


# K1: CFG652's committed lens stack, its own background (unrotated sources only)
if not MUT:
    I652 = np.load(os.path.join(WORK, "cfg652_inputs.npz")); D652 = np.load(os.path.join(WORK, "cfg652_esd.npz"))
    k1 = stack(I652["ra"], I652["dec"], I652["z"], DC_cfg652)
    d1 = max(float(np.max(np.abs(k1[0] - D652["WG"]) / (np.abs(D652["WG"]).max()))), float(np.max(np.abs(k1[2] - D652["WW"]) / D652["WW"].max())))
    check("K1_reproduces_CFG652_stack", d1 < 1e-6, f"max rel diff {d1:.1e}")

# ------------------------------------------------------------ measurement on X75 hosts (native background)
L_ = stack(raH, deH, zH, DC_native); P(f"  hosts stacked [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
rng = np.random.default_rng(1001)
cells = np.unique(np.c_[np.floor(sra * 10), np.floor(sde * 10)], axis=0)
NR = 5 * len(zH); pick = cells[rng.integers(0, len(cells), NR)]
rra = (pick[:, 0] + rng.uniform(0, 1, NR)) / 10; rde = (pick[:, 1] + rng.uniform(0, 1, NR)) / 10; rz = rng.choice(zH, NR)
R_ = stack(rra, rde, rz, DC_native); P(f"  randoms stacked [{time.time() - T0:.0f} s]")
edges = np.quantile(raH, np.linspace(0, 1, NPATCH + 1)); edges[0] -= 1; edges[-1] += 1
pg = np.clip(np.digitize(raH, edges) - 1, 0, NPATCH - 1); pr = np.clip(np.digitize(rra, edges) - 1, 0, NPATCH - 1)
os.makedirs(os.path.join(os.path.dirname(REPO), "_external_data", "gh1_work"), exist_ok=True)
np.savez(os.path.join(os.path.dirname(REPO), "_external_data", "gh1_work", f"gh1_esd{TAG}.npz"), WG=L_[0], WX=L_[1], WW=L_[2], NN=L_[3], rWG=R_[0], rWX=R_[1], rWW=R_[2], rNN=R_[3],
         pg=pg, pr=pr, hbin=hbin, lm=lmH, z=zH)


def esd(sel_l, sel_r, comp=0):
    out = []
    for b in range(4):
        ml, mr = sel_l & (hbin == b), sel_r
        g = L_[comp][ml].sum(0) / L_[2][ml].sum(0) - R_[comp][mr].sum(0) / R_[2][mr].sum(0)
        out.append(g)
    return np.array(out)                                                  # (4, NB)


allL, allR = np.ones(len(zH), bool), np.ones(NR, bool)
DS = esd(allL, allR, 0); DX = esd(allL, allR, 1)
JK = np.array([esd(pg != p, pr != p, 0) for p in range(NPATCH)]); JX = np.array([esd(pg != p, pr != p, 1) for p in range(NPATCH)])
GR = (RC >= 50) & (RC <= 300); GR2 = (RC >= 50) & (RC <= 200)


def cov(J, mask):
    v = J[:, :, mask].reshape(NPATCH, -1); m = v.mean(0)
    return (NPATCH - 1) / NPATCH * (v - m).T @ (v - m)


def chi2_inv(C, npts):
    return np.linalg.inv(C) * (NPATCH - npts - 2) / (NPATCH - 1)          # Hartlap


Cg = cov(JK, GR); npts = int(GR.sum()) * 4; Ci = chi2_inv(Cg, npts)
err = np.sqrt(np.diag(Cg)).reshape(4, -1)
P(f"  graded radii (kpc) {np.round(RC[GR], 0).tolist()}; points {npts}; Hartlap factor {(NPATCH - npts - 2) / (NPATCH - 1):.3f}")
for b in range(4):
    P(f"  bin {b + 1}: DS {np.round(DS[b, GR], 1).tolist()} +- {np.round(err[b], 1).tolist()} Msun/pc^2;  DS_x {np.round(DX[b, GR], 1).tolist()}")
dx = DX[:, GR].ravel(); chix = float(dx @ chi2_inv(cov(JX, GR), npts) @ dx)
from scipy import stats
P(f"  cross-shear null 50-300 kpc: chi2 {chix:.1f} / {npts} (p {stats.chi2.sf(chix, npts):.3f})")
WLb = np.array([[L_[2][hbin == b, k].sum() for k in range(NB)] for b in range(4)])
boost = np.array([(L_[3][hbin == b].sum(0) / L_[3][hbin == b].sum()) / (R_[3].sum(0) / R_[3].sum()) for b in range(4)])
P(f"  boost (normalised source-count ratio) at graded radii: {np.round(boost[:, GR], 3).tolist()}")

# ------------------------------------------------------------ model tables (X75 machinery) and fit
LGRID = np.round(np.arange(8.5, 11.31, 0.05), 2)                 # X75 LGRID
SH = np.round(np.arange(-0.5, 1.5001, 0.01), 2); HP = dict(NS["H_PRIMARY"])
M0, _ = NS["mass_H"]("canonical", 10.7, H_NAT, dict(HP, dlM=0.0)); M0b, _ = NS["mass_H"]("canonical", 10.7, H_NAT, HP)
check("K3_model_shift0_identity", float(np.max(np.abs(M0 / M0b - 1))) == 0.0, "mass_H dlM 0 == X75/X53 smooth")
Rpc = RC * 1e3


def tables(foot):
    tH = np.empty((len(LGRID), len(SH), NB)); tL = np.empty((len(LGRID), NB))
    for a, l in enumerate(LGRID):
        for k, s in enumerate(SH):
            tH[a, k] = AQ.delta_sigma(Rpc, NS["RGRID_PC"], NS["mass_H"](foot, l, H_NAT, dict(HP, dlM=float(s)))[0], "const")
        l70 = l - 2 * np.log10(0.70 / H_NAT); lmc = l + (-0.69 * l70 + 6.63)
        tL[a] = AQ.delta_sigma(Rpc, NS["RGRID_PC"], NF["meff_profile"](foot, l, 0.5, 0.0, "zero", logMcold=lmc)[0], "const")
    return tH, tL


def stack_model(tab, b):
    m = hbin == b; Wik = L_[2][m]                                         # (hosts, NB)
    v = np.array([[np.interp(lmH[m], LGRID, tab[:, k, j]) for j in range(NB)] for k in range(tab.shape[1])]) if tab.ndim == 3 \
        else np.array([[np.interp(lmH[m], LGRID, tab[:, j]) for j in range(NB)]])
    return np.einsum("ksh,hs->ks", v.transpose(0, 1, 2), Wik) / Wik.sum(0)   # (shifts, NB)


X75J = json.load(open(os.path.join(REB, "X75_satellite_kinematics_mass_gap", "x75_satkin_results.json")))
RES = {"criteria": "45f918f379", "mutate": MUT, "radii_kpc": RC.tolist(), "graded_mask": GR.tolist(), "DS": DS.tolist(), "DX": DX.tolist(),
       "err": err.tolist(), "cross_null_chi2": chix, "boost": boost.tolist(), "footings": {}}
for foot in ("canonical", "alt"):
    tH, tL = tables(foot); P(f"  [{foot}] model tables [{time.time() - T0:.0f} s, RSS {rss():.2f} GB]")
    mH = np.array([stack_model(tH, b) for b in range(4)])                # (4, SH, NB)
    mL = np.array([stack_model(tL, b)[0] for b in range(4)])             # (4, NB)

    def fitD(mask, Cinv, data, bins=range(4)):
        d = np.concatenate([data[b, mask] for b in bins])
        chi = np.array([(lambda r: r @ Cinv @ r)(d - np.concatenate([mH[b, k, mask] for b in bins])) for k in range(len(SH))])
        k = int(np.argmin(chi)); ok = chi <= chi[k] + 1
        return dict(D=float(SH[k]), lo=float(SH[ok].min()), hi=float(SH[ok].max()), chi2=float(chi[k]), chi2_0=float(chi[int(np.argmin(np.abs(SH)))]),
                    edge=bool(k in (0, len(SH) - 1)))
    g = fitD(GR, Ci, DS); g["sD"] = 0.5 * (g["hi"] - g["lo"])
    dL = np.concatenate([DS[b, GR] - mL[b, GR] for b in range(4)]); g["chi2_L"] = float(dL @ Ci @ dL)
    perbin = []
    for b in range(4):
        Cb = cov(JK[:, b:b + 1, :], GR); nb = int(GR.sum())
        perbin.append(fitD(GR, chi2_inv(Cb, nb), DS, bins=[b])["D"])
    g["perbin_D"] = perbin
    C2 = cov(JK, GR2); g200 = fitD(GR2, chi2_inv(C2, int(GR2.sum()) * 4), DS); g["D_50_200"] = g200["D"]
    DSb = DS * boost; gb = fitD(GR, Ci, DSb); g["D_boost"] = gb["D"]
    sat = X75J["footings"][foot]; Ds, sDs = sat["D"], sat["sD"]
    tol = 2 * math.sqrt(g["sD"] ** 2 + sDs ** 2)
    if abs(g["D"] - Ds) < tol: v = "PROBES AGREE ON MATCHED HOSTS"
    else: v = "PROBES DISAGREE ON MATCHED HOSTS (lensing " + ("lighter" if g["D"] < Ds else "heavier") + ")"
    g.update(D_sat=Ds, sD_sat=sDs, tol=tol, verdict=v,
             pred_H_at_D=[mH[b, int(np.argmin(np.abs(SH - g["D"]))), GR].tolist() for b in range(4)], pred_L=[mL[b, GR].tolist() for b in range(4)])
    RES["footings"][foot] = g
    P(f"=== [{foot}] Delta_lens {g['D']:+.2f} [{g['lo']:+.2f}, {g['hi']:+.2f}] (chi2 {g['chi2']:.1f}/{npts}; at 0 {g['chi2_0']:.1f}; law {g['chi2_L']:.1f}){' [grid edge]' if g['edge'] else ''}; "
      f"Delta_sat {Ds:+.2f}+-{sDs:.2f} -> {v}")
    P(f"     per-bin Delta_lens {perbin}; 50-200 kpc {g['D_50_200']:+.2f}; boost-corrected {g['D_boost']:+.2f}")
    for b in range(4):
        P(f"     bin {b + 1}: data {np.round(DS[b, GR], 1).tolist()}  H(D) {np.round(g['pred_H_at_D'][b], 1).tolist()}  H(0) {np.round(mH[b, int(np.argmin(np.abs(SH))), GR], 1).tolist()}  L {np.round(mL[b, GR], 1).tolist()}")
if MUT:
    g = RES["footings"]["canonical"]
    check("MUTATE_rotated_null", stats.chi2.sf(float(DS[:, GR].ravel() @ Ci @ DS[:, GR].ravel()), npts) > 0.01 and (g["edge"] or g["D"] <= -0.4),
          f"rotated DS chi2 vs 0 p {stats.chi2.sf(float(DS[:, GR].ravel() @ Ci @ DS[:, GR].ravel()), npts):.3f}; D {g['D']:+.2f}")
V = {f: RES["footings"][f]["verdict"] for f in ("canonical", "alt")}
RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"FOOTINGS DISAGREE: {V}"
RES["checks"] = CHK; n = sum(CHK.values())
P(f"\n=== VERDICT: {RES['verdict']}\nchecks {n}/{len(CHK)}; runtime {time.time() - T0:.0f} s; peak RSS {rss():.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"gh1_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"gh1{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if n == len(CHK) else 1)

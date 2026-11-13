#!/usr/bin/env python3
"""SRF1R (READING.md, cc3d45432d) stage 0: halo-model tables per (DESI bin z, footing).
SRH1's srh1_hm.py is executed up to its "checkpointed run" marker from its own path (read-only; it executes FRZ1's and
CFG556's code). Writes tables/tab_<foot>_z<z>.npz:
  light masses (1e8 <= M < 10^10.8): W_M, U_Rb(k) on KTAB; P_2h(k) on KTAB (Rb turnaround scope); f_s;
  heavy masses (>= 10^10.8): W_M, bias, r_ta, R_set(f); gas-smoothed radial profiles g_R(r) and g_S(r) - g_R(r) for each
  f and each lambda_P variant (real-space shell smoothing, exact 3D Gaussian); the matter one-halo pieces on CO1's KK;
  SRH1's own R_cold(k) at every f (ratios_S) for the record's matter-level Delta chi^2.
  nice -n 19 python3 srf1r_tables.py <foot> <z> [<z> ...]
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, sys, json, math, time, warnings, io, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "closure_2026_11_10", "SRH1_settled_radius_history", "srh1_hm.py"); code = open(SRC).read()
cut = code.index("# ------------------------------------------------------------------ checkpointed run\n")
G = {"__file__": SRC, "__name__": "srh1_lib"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(code[:cut], SRC, "exec"), G)
L = G["L"]; F = G["F"]; layout, lay_S, set_z, ratios_S = G["layout"], G["lay_S"], G["set_z"], G["ratios_S"]
h = G["h"]; KK = G["KK"]; U_of = F["U_of"]
FGRID = [0.0, 0.30, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.25, 1.40, 1.60, 1.80, 2.00, 2.50, 3.00, 4.00, 6.00, math.inf]
SRH1_ONLY = [0.35, 0.40, 0.45, 0.55, 0.65, 0.75, 1.50]            # SRH1 grid points recomputed for check c0 only (matter level)
LAM0 = 0.0532                                                     # 79 comoving kpc in Mpc/h
def lam_variants(z): return dict(p=LAM0, half=0.5 * LAM0, dbl=2 * LAM0, pk100=0.1 * (1 + z) * h)
MSPLIT = 10.8
KTAB = np.concatenate([[0.0], np.geomspace(0.05, 130.0, 500)])
NS = 320                                                          # shells on the rebinned profile

def smooth_profile(edges, Me, M0, lam, reval):
    """density (units of rho_m) at radii reval of: point mass M0 at 0 + shells (mass diff(Me) at the edges' geometric mid),
    each smoothed by the 3D Gaussian of width lam."""
    RHO = L["RHO_M"]; dM = np.diff(Me); s = np.sqrt(edges[1:] * np.maximum(edges[:-1], edges[1] * 1e-3))
    r = reval[:, None]; sig = lam
    x = r * s[None, :] / sig ** 2
    ker = np.exp(-(r - s[None, :]) ** 2 / (2 * sig ** 2)) * (-np.expm1(-2 * x)) / (4 * math.pi * r * s[None, :] * sig * math.sqrt(2 * math.pi))
    out = ker @ dM + M0 * np.exp(-reval ** 2 / (2 * sig ** 2)) / (2 * math.pi * sig ** 2) ** 1.5
    return out / RHO

def run(foot, z):
    t0 = time.time(); set_z(z)
    HB, W, BIAS, MM = L["HB"], L["W_M"], L["BIAS"], L["MM"]; RHO = L["RHO_M"]; lM = np.log10(MM)
    D = F["S"]["D"]; PLT = L["P_lin"](np.maximum(KTAB, 1e-5)) * D * D; PLT[0] = 0.0
    lamv = lam_variants(z); LAMK = list(lamv)
    # Rb profiles on KTAB and KK for every mass (two-halo term, light-halo U)
    URt = np.empty((len(MM), len(KTAB))); URk = np.empty((len(MM), len(KK)))
    for i, hb in enumerate(HB):
        r, M, _ = layout(hb, foot, mode="Rb"); URt[i] = U_of(r, M, KTAB); URk[i] = U_of(r, M, KK)
    I = np.sum(W[:, None] * BIAS[:, None] * URt / RHO, 0) / L["NORM_TA"]
    P2h = PLT * I ** 2
    fs = 1.0 - float(np.sum(W * L["MTA"])) / RHO
    light = lM < MSPLIT; heavy = (lM >= MSPLIT) & (lM < 14.6 + 1e-9)
    hi = np.where(heavy)[0]
    # heavy profiles
    nF = len(FGRID) + len(SRH1_ONLY); allF = FGRID + SRH1_ONLY
    NR = 300
    REV = np.empty((len(hi), NR)); gR = np.empty((len(hi), len(LAMK), NR), np.float32)
    dg = np.zeros((len(hi), len(FGRID), len(LAMK), NR), np.float32)
    mchk = 0.0; RSET = np.zeros((len(hi), nF)); dP3 = np.zeros((nF, len(KK))); P1hH = np.zeros(len(KK)); conf = 0.0
    for j, i in enumerate(hi):
        hb = HB[i]; rta = hb["rta"]
        rR, MR, _ = layout(hb, foot, mode="Rb")
        reval = np.concatenate([[1e-5], np.geomspace(2e-4, rta + 6 * max(lamv.values()), NR - 1)]); REV[j] = reval
        base = np.concatenate([[0.0], np.geomspace(1e-4 * hb["r200"], rta, NS)])
        P1hH += W[i] * URk[i] ** 2 / RHO ** 2
        for q, f in enumerate(allF):
            fn = lay_S(foot, z, f); rS, MS, inf = fn(hb); R = float(inf.get("R_set", 0.0)) if f > 0 else 0.0
            RSET[j, q] = R
            UkS = U_of(rS, MS, KK); dP3[q] += W[i] * (UkS ** 2 - URk[i] ** 2) / RHO ** 2
            if q >= len(FGRID): continue
            mchk = max(mchk, abs(MS[-1] - hb["Mta"]) / hb["Mta"])
            G["CUR"][0] = R if 0 < R < rta else 0.0; rR2, MR2, _ = layout(hb, foot, mode="Rb"); G["CUR"][0] = 0.0
            ed = np.unique(np.concatenate([base, [R]] if 0 < R < rta else [base]))
            lg = lambda rr, MMx, e: np.interp(np.log(np.maximum(e, 1e-12)), np.log(np.maximum(rr, 1e-12)), MMx)
            MRe = lg(rR2, MR2, ed); MRe[0] = MR2[0]; MSe = lg(rS, MS, ed); MSe[0] = MS[0]
            for c, lk in enumerate(LAMK):
                if q == 0:
                    gR[j, c] = smooth_profile(ed, MRe, MR[0], lamv[lk], reval)
                if R > 0:
                    d = smooth_profile(ed, MSe - MRe, MS[0] - MR[0], lamv[lk], reval); dg[j, q, c] = d
                    if c == 0 and abs(z - 3.0) < 1e-6 and abs(f - 1.0) < 1e-9 and R < rta:
                        pk = float(np.max(np.abs(d))); out = np.abs(d[reval > R + 5 * lamv[lk]])
                        conf = max(conf, float(out.max() / pk) if out.size and pk > 0 else 0.0)
    # SRH1's own R_cold at every f (the record's matter level)
    Rc = {}
    for f in allF:
        _, _, Rcold, _ = ratios_S(foot, z, fac=f); Rc[f"{f}"] = Rcold
    # heavy-only share of the f = 1 change (halo model, one-halo, reported for c0)
    Ustd = L["U_std"](); Pstd, _, _ = L["spectra_std"](Ustd)
    UL, _ = L["U_set"](lambda hb: layout(hb, foot, mode="L")); PLta, _, _ = L["spectra_ta"](UL)
    UR, _ = L["U_set"](lambda hb: layout(hb, foot, mode="Rb")); PR, _, _ = L["spectra_ta"](UR)
    PstdRbar = Pstd + PR - PLta
    os.makedirs(os.path.join(HERE, "tables"), exist_ok=True)
    np.savez_compressed(os.path.join(HERE, "tables", f"tab_{foot}_z{z:.1f}.npz"), KTAB=KTAB, P2h=P2h, fs=fs, lM=lM, W=W, BIAS=BIAS,
                        light_idx=np.where(light)[0], URt_light=URt[light].astype(np.float32), heavy_idx=hi, REV=REV, gR=gR, dg=dg,
                        RSET=RSET, rta=np.array([HB[i]["rta"] for i in hi]), r200=np.array([HB[i]["r200"] for i in hi]),
                        FGRID=np.array(FGRID), ALLF=np.array(allF), LAMK=np.array(LAMK), LAMV=np.array([lamv[k] for k in LAMK]),
                        KK=KK, dP3=dP3, P1hH=P1hH, PstdRbar=PstdRbar, Rcold=np.array([Rc[f"{f}"] for f in allF]), conf=conf, mass_check=mchk,
                        Mta=np.array([HB[i]["Mta"] for i in hi]), MtaR_check=np.array([layout(HB[i], foot, mode="Rb")[1][-1] for i in hi]))
    print(f"[{foot} z {z}] tables done: {len(hi)} heavy masses, f_s {fs:.3f}, conf(z3,f1) {conf:.2e}  [{time.time() - t0:.0f} s]", flush=True)

if __name__ == "__main__":
    foot = sys.argv[1]
    for zz in sys.argv[2:]:
        run(foot, float(zz))

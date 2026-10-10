#!/usr/bin/env python3
"""CFG556 (FROZEN_CRITERIA.md, commit 77ec620e0): a resolution-free halo model of the matter power spectrum for LCDM (NFW) and for the
framework's halo (baryons + the law's round phantom of the retained baryons inside the edge, drained shell out to r_ta, total mass inside
r_ta conserved), both footings.  Compared with CFG555's PM gravitating-field ratios (read-only).

  OMP_NUM_THREADS=4 nice -n 10 python3 cfg556_halo_model.py            -> cfg556_halo_model.out, cfg556_results.json
  CFG556_MUTATE=1 OMP_NUM_THREADS=4 nice -n 10 python3 cfg556_halo_model.py   -> *_MUTATE.out / *_MUTATE.json (exit 1 = all teeth bite)

kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, sys, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "4")
import numpy as np
from scipy.optimize import brentq
from scipy.special import sici

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
CFG555 = os.path.join(HERE, "..", "CFG555_growth_on_gravitating_field", "cfg555_results.json")
MUTATE = os.environ.get("CFG556_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ cosmology + linear spectrum (cfg361_pm.py lines 30-32, 66-79, verbatim)
h = 0.6736; om_b, om_c = 0.02237, 0.1200
Om = (om_b + om_c) / h ** 2; FB = om_b / (om_b + om_c)
NS, SIG8 = 0.965, 0.811
def T_eh(k):
    OB = om_b / h ** 2; omh2, fb = Om * h * h, OB / Om
    s = 44.5 * math.log(9.83 / omh2) / math.sqrt(1 + 10 * (OB * h * h) ** 0.75)
    ag = 1 - 0.328 * math.log(431 * omh2) * fb + 0.38 * math.log(22.3 * omh2) * fb ** 2
    gam = Om * h * (ag + (1 - ag) / (1 + (0.43 * k * s) ** 4))
    q = k * (2.7255 / 2.7) ** 2 / (gam * h)
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
_KG = np.geomspace(1e-5, 100, 40000)
_PK = _KG ** NS * T_eh(_KG * h) ** 2
_W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
_PK *= SIG8 ** 2 / (np.trapz(_PK * _W8(_KG * 8.0) ** 2 * _KG ** 2, _KG) / (2 * math.pi ** 2))
def P_lin(k):
    return np.interp(np.log(np.maximum(k, 1e-5)), np.log(_KG), _PK, left=0, right=0)

RHO_M = Om * 2.77536627e11                    # Msun/h per (Mpc/h)^3
G = 4.30091e-9                                # Mpc km^2 s^-2 Msun^-1 (h cancels: G M_h / r_h)
MPC = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
A0MPC = {f: v * MPC / 1e6 for f, v in A0.items()}   # (km/s)^2 per Mpc
DTA = 11.81                                   # Delta_ta (PM z = 0 value, CFG504 / CFG555 shared_diag)
DC = 1.686

def nu_k(y):
    y = np.maximum(y, 1e-300); s = np.sqrt(y)
    return np.where(s > 50, 1.0, 1.0 / -np.expm1(-np.minimum(s, 50)))

# ------------------------------------------------------------------ sigma(M), Tinker08 mass function, Tinker10 bias
LM = np.linspace(8.0, 16.0, 321); MM = 10 ** LM; DLM = (LM[1] - LM[0]) * math.log(10)
def sigma_R(R):
    x = np.outer(R, _KG); w = _W8(np.maximum(x, 1e-6))
    return np.sqrt(np.trapz(_PK * w ** 2 * _KG ** 2, _KG, axis=1) / (2 * math.pi ** 2))
RM = (3 * MM / (4 * math.pi * RHO_M)) ** (1 / 3)
SIG = sigma_R(RM)
dlns = np.gradient(np.log(SIG), LM * math.log(10))
fT = 0.186 * ((SIG / 2.57) ** -1.47 + 1) * np.exp(-1.19 / SIG ** 2)
NDLNM = fT * RHO_M / MM * (-dlns)              # n(M) dM / dlnM
yD = math.log10(200.0)
A10 = 1 + 0.24 * yD * math.exp(-(4 / yD) ** 4); a10 = 0.44 * yD - 0.88; B10, b10 = 0.183, 1.5
C10 = 0.019 + 0.107 * yD + 0.19 * math.exp(-(4 / yD) ** 4); c10 = 2.4
NUP = DC / SIG
BIAS = 1 - A10 * NUP ** a10 / (NUP ** a10 + DC ** a10) + B10 * NUP ** b10 + C10 * NUP ** c10
W_M = NDLNM * DLM                              # weights per grid mass
A_MISS = 1.0 - float(np.sum(W_M * BIAS * MM)) / RHO_M

# ------------------------------------------------------------------ NFW, r_ta, M200c, baryons
m_nfw = lambda x: np.log1p(x) - x / (1 + x)
def conc(M): return 10.14 * (M / 2e12) ** -0.081
def r200m(M): return (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3)
def halo_basics(M):
    c = conc(M); r2 = r200m(M); mc = m_nfw(c)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - DTA / 200.0, 1.0, 50.0, xtol=1e-12)
    xc = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - 1.0 / Om, 0.05, 1.0, xtol=1e-12)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, mc=mc, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc, r200c=xc * r2, M200c=M * m_nfw(c * xc) / mc)
def M_L(hb, r):
    return hb["M"] * m_nfw(np.asarray(r) / hb["rs"]) / hb["mc"]

def fret_of(lM):
    """CFG416 cfg416_pm.py fret_of, copied verbatim from cfg515_lib.py (FRETX = 1)."""
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def mstar(hb):
    M = hb["M200c"] / h; M1 = 10 ** 11.590
    ms = M * 2 * 0.0351 / ((M / M1) ** -1.376 + (M / M1) ** 0.608)
    return ms * h
def baryon_cum(hb, Mbret, r, Rt):
    """retained baryons M_b(<r), truncated at Rt and normalised to Mbret there."""
    ms = min(mstar(hb), Mbret); mg = Mbret - ms
    a = 0.015 * hb["r200c"] / (1 + math.sqrt(2)); rc = 0.1 * hb["r200c"]
    rr = np.minimum(r, Rt)
    hs = lambda x: x ** 2 / (x + a) ** 2
    gb = lambda x: x / rc - np.arctan(x / rc)
    return ms * hs(rr) / hs(Rt) + mg * gb(rr) / gb(Rt)

# ------------------------------------------------------------------ framework mass profile on a radial grid
NR = 1600
def rgrid(hb, rmax):
    return np.concatenate([[0.0], np.geomspace(1e-4 * hb["r200"], rmax, NR)])

def frame_profile(hb, foot, edge="cen", fret_mode="census", mode="normal"):
    """returns (r, M_F(<r), info). mode: normal | lta (M1) | bare (M2) | noshell (M3)."""
    r = rgrid(hb, hb["rta"]); Mta = hb["Mta"]; ML = M_L(hb, r)
    if mode == "lta":
        return r, ML.copy(), dict(re=float("nan"), q=0.0, capped=False)
    f = fret_of(math.log10(Mta)) if fret_mode == "census" else 1.0
    Mb = f * FB * Mta; supply = (1 - FB) * Mta; a0 = A0MPC[foot]
    rM = math.sqrt(G * Mb * h / a0)
    if mode == "bare":
        mb = baryon_cum(hb, Mb, r, hb["rta"])
        y = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
        MF = np.where(r > 0, mb * nu_k(y), 0.0)
        return r, MF, dict(re=float("nan"), q=0.0, capped=False, Mball_over_Mta=float(MF[-1] / Mta), fret=f)
    if edge == "emg":
        mb = baryon_cum(hb, Mb, r, hb["rta"])
        y = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
        Min = np.where(r > 0, mb * nu_k(y), 0.0)
        S = Min - mb
        idx = np.nonzero(S >= supply)[0]
        if len(idx):
            i = idx[0]; r0, r1 = r[i - 1], r[i]; s0, s1 = S[i - 1], S[i]
            re = r0 + (supply - s0) * (r1 - r0) / (s1 - s0)
        else:
            re = hb["rta"]
    else:
        re = rM / math.log1p(f * FB / (1 - FB))
    capped = re >= hb["rta"]
    re = min(re, hb["rta"])
    # rebuild the grid with r_e (and softening radii) as nodes
    extra = [re]
    if edge in ("s25", "s55"):
        r2 = (1.25 if edge == "s25" else 1.55) * re; r1 = 2 * re - r2
        if r2 >= hb["rta"]:
            r2 = None
        else:
            extra += [r1, r2]
    else:
        r2 = None
    r = np.unique(np.concatenate([r, [x for x in extra if x is not None]])); ML = M_L(hb, r)
    Rt = re if edge in ("cen", "s25", "s55") else hb["rta"]
    mb = baryon_cum(hb, Mb, r, Rt)
    y = G * mb * h / (np.maximum(r, 1e-30) ** 2 * a0)
    Min = np.where(r > 0, mb * nu_k(y), 0.0)
    rout = re; Aamp = 1.0
    if r2 is not None:
        S = Min - mb
        ir1 = np.searchsorted(r, r1); ire = np.searchsorted(r, re)
        g1 = np.gradient(S, r)[ir1]                         # dS/dr at r1 (= 4 pi r^2 rho_s)
        target = S[ire] - S[ir1]
        Aamp = target / (g1 * (r2 - r1) / 2.0)
        Ssoft = S.copy()
        m = (r > r1) & (r <= r2)
        t = (r[m] - r1); Ssoft[m] = S[ir1] + Aamp * g1 * (t - t ** 2 / (2 * (r2 - r1)))
        Ssoft[r > r2] = S[ir1] + Aamp * g1 * (r2 - r1) / 2.0
        mbt = baryon_cum(hb, Mb, r, re)
        Min = mbt + Ssoft; rout = r2
    iout = np.searchsorted(r, rout)
    Mout = Min[iout]; MLout = ML[iout]
    if mode == "noshell":
        MF = np.where(r <= rout, Min, Mout + ML - MLout)
        q = 0.0
    elif capped or MLout >= Mta * (1 - 1e-12):
        rem = max(Mta - Min[-1], 0.0)
        MF = Min + rem * ML / Mta
        q = 0.0
    else:
        shell = (Mta - Mout) / (Mta - MLout)
        MF = np.where(r <= rout, Min, Mout + (Mta - Mout) * (ML - MLout) / (Mta - MLout))
        q = 1.0 - shell
    return r, MF, dict(re=re, rout=rout, q=q, capped=capped, fret=f, Mb=Mb, rM=rM, Aamp=Aamp,
                       Min_re_over_Mta=float(Min[np.searchsorted(r, re)] / Mta), ML_re_over_Mta=float(ML[np.searchsorted(r, re)] / Mta))

def U_of(r, Mc, k):
    dM = np.diff(Mc); rm = 0.5 * (r[1:] + r[:-1])
    x = np.outer(k, rm)
    j0 = np.where(x > 1e-6, np.sin(x) / np.maximum(x, 1e-30), 1.0)
    return Mc[0] + j0 @ dM

# ------------------------------------------------------------------ k grid, halo basics
KK = np.geomspace(1e-3, 10.0, 260)
HB = [halo_basics(M) for M in MM]
MTA = np.array([hb["Mta"] for hb in HB])
PL = P_lin(KK)

def U_std():
    U = np.empty((len(MM), len(KK)))
    for i, hb in enumerate(HB):
        r = rgrid(hb, hb["r200"]); U[i] = U_of(r, M_L(hb, r), KK)
    return U
def U_set(fn):
    U = np.empty((len(MM), len(KK))); infos = []
    for i, hb in enumerate(HB):
        r, Mc, inf = fn(hb); U[i] = U_of(r, Mc, KK); infos.append(inf)
    return U, infos

def spectra_std(U):
    p1 = np.sum((W_M[:, None] * (U / RHO_M) ** 2), 0)
    I = np.sum(W_M[:, None] * BIAS[:, None] * U / RHO_M, 0) + A_MISS
    return p1 + PL * I ** 2, p1, I
NORM_TA = float(np.sum(W_M * BIAS * MTA)) / RHO_M
def spectra_ta(U):
    p1 = np.sum((W_M[:, None] * (U / RHO_M) ** 2), 0)
    I = np.sum(W_M[:, None] * BIAS[:, None] * U / RHO_M, 0) / NORM_TA
    return p1 + PL * I ** 2, p1, I

def s8_of(Pk):
    w = _W8(KK * 8.0)
    return math.sqrt(np.trapz(Pk * w ** 2 * KK ** 2, KK) / (2 * math.pi ** 2))

# ------------------------------------------------------------------ run
P(f"CFG556 halo model {'(MUTATE)' if MUTATE else ''} -- FROZEN_CRITERIA.md (77ec620e0). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
P(f"Om {Om:.5f}  f_b {FB:.5f}  rho_m {RHO_M:.4e} Msun/h/(Mpc/h)^3  Delta_ta {DTA}  A_miss {A_MISS:.4f}  int n b M_ta/rho {NORM_TA:.4f}  "
  f"int n M/rho {float(np.sum(W_M * MM)) / RHO_M:.4f}  mean M_ta/M200m (1e12..1e15) {np.mean((MTA / MM)[(LM >= 12) & (LM <= 15)]):.3f}")

Ustd = U_std(); Pstd, P1std, Istd = spectra_std(Ustd)
Ulta, _ = U_set(lambda hb: frame_profile(hb, "canonical", mode="lta"))
Plta, P1lta, Ilta = spectra_ta(Ulta)
res = dict(lane="CFG556", date="2026-10-10", mutate=MUTATE, k=KK.tolist(), P_lin=PL.tolist(), P_L_std=Pstd.tolist(), P_L_ta=Plta.tolist(),
           s8_L_std=s8_of(Pstd), s8_lin=s8_of(PL), controls={}, cases={}, pm={}, verdict={})

# controls
c1 = abs(s8_of(PL) - SIG8) / SIG8
ilo = np.argmin(abs(KK - 1e-3))
c2 = max(abs(Istd[ilo] - 1), abs(Ilta[ilo] - 1))
hbt = [halo_basics(M) for M in (1e11, 1e13, 1e15)]
c4 = 0.0
for hb in hbt:
    kt = np.geomspace(0.05, 3, 40); r = rgrid(hb, hb["r200"]); Un = U_of(r, M_L(hb, r), kt) / hb["M"]
    eta = kt * hb["rs"]; c = hb["c"]
    si1, ci1 = sici((1 + c) * eta); si0, ci0 = sici(eta)
    Ua = (np.sin(eta) * (si1 - si0) - np.sin(c * eta) / ((1 + c) * eta) + np.cos(eta) * (ci1 - ci0)) / hb["mc"]
    c4 = max(c4, float(np.max(np.abs(Un - Ua) / np.abs(Ua))))
P(f"\nC1 sigma8(P_lin) {s8_of(PL):.5f} vs 0.811: rel {c1:.1e} (<= 1e-3) -> {'PASS' if c1 <= 1e-3 else 'FAIL'}")
P(f"C2 2-halo I(k=1e-3): L-std {Istd[ilo]:.6f}, L-ta {Ilta[ilo]:.6f} -> {'PASS' if c2 <= 1e-3 else 'FAIL'} (framework cases checked below)")
P(f"C4 numerical vs analytic truncated-NFW U(k), M = 1e11/1e13/1e15, k 0.05-3: max rel {c4:.1e} (<= 1e-3) -> {'PASS' if c4 <= 1e-3 else 'FAIL'}")
res["controls"].update(C1=c1, C1_pass=c1 <= 1e-3, C2_L=c2, C4=c4, C4_pass=c4 <= 1e-3)

def lj(p): return json.load(open(p))
S0 = {256: lj(os.path.join(EXT, "cfg359_work", "cfg359_S0_FLAT_canonical_N256.json")),
      512: lj(os.path.join(EXT, "cfg411_work", "cfg411_S0_Rc3_MIXA_FLAT_canonical_N512.json"))}
P("\nC5 (reported) P_lin vs S0 z_i spectrum / D(z_i)^2:")
for N, d in S0.items():
    zi = d["snap"]["zi"]; k = np.array(zi["k"]); m = (k >= 0.05) & (k <= 0.5)
    rr = np.array(zi["P"])[m] / zi["D"] ** 2 / P_lin(k[m])
    P(f"  N{N}: median {np.median(rr):.3f}, range {rr.min():.3f}-{rr.max():.3f} over {m.sum()} bins")
    res["controls"][f"C5_N{N}"] = dict(median=float(np.median(rr)), min=float(rr.min()), max=float(rr.max()))

P("\nValidation: LCDM halo model (L-std) / S0 PM P(k) at z = 0 (particle = gravitating for S0):")
val = {}
for N, kmax in ((256, 1.0), (512, 2.0)):
    z0 = S0[N]["snap"]["z0"]; k = np.array(z0["k"]); m = (k >= 0.1) & (k <= kmax)
    rr = np.interp(np.log(k[m]), np.log(KK), Pstd) / np.array(z0["P"])[m]
    lab = "GOOD" if np.all(np.abs(rr - 1) <= 0.20) else "POOR"
    sel = [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
    row = "  ".join(f"{kk:g}:{np.interp(kk, k[m], rr):.3f}" for kk in sel if kk <= kmax)
    P(f"  N{N} (k 0.1-{kmax}): {row}  | min {rr.min():.3f} max {rr.max():.3f} -> {lab};  sigma8 HM {s8_of(Pstd):.4f} vs S0 {z0['sigma8']:.4f}")
    val[N] = dict(label=lab, min=float(rr.min()), max=float(rr.max()), k=k[m].tolist(), ratio=rr.tolist(), s8_S0=z0["sigma8"])
res["validation"] = val

KSEL = [0.05, 0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]
def summarize(name, U, infos, scope="ta"):
    if scope == "ta":
        PF, P1F, IF = spectra_ta(U); R = 1 + (PF - Plta) / Pstd; Rr = PF / Plta
        dP = PF - Plta
    else:
        PF, P1F, IF = spectra_std(U); R = PF / Pstd; Rr = R; dP = PF - Pstd
    w8 = _W8(KK * 8.0) ** 2 * KK ** 2 / (2 * math.pi ** 2)
    s8F = math.sqrt(s8_of(Pstd) ** 2 + np.trapz(dP * w8, KK))
    m = (KK >= 0.05) & (KK <= 1.0)
    E, D = float(np.max(R[m] - 1)), float(np.min(R[m] - 1)); kE = float(KK[m][np.argmax(R[m])]); kD = float(KK[m][np.argmin(R[m])])
    Er, Dr = float(np.max(Rr[m] - 1)), float(np.min(Rr[m] - 1))
    i0 = np.argmin(abs(KK - 1e-3)); Ichk = float(IF[i0])
    out = dict(R=R.tolist(), R_ratio=Rr.tolist(), E=E, D=D, kE=kE, kD=kD, E_ratio=Er, D_ratio=Dr, s8_ratio=s8F / s8_of(Pstd),
               I_k1e3=Ichk, R_at={str(kk): float(np.interp(kk, KK, R)) for kk in KSEL}, R_ratio_at={str(kk): float(np.interp(kk, KK, Rr)) for kk in KSEL})
    if infos is not None:
        re_ta = np.array([inf["re"] / hb["rta"] for inf, hb in zip(infos, HB)])
        qq = np.array([inf["q"] for inf in infos]); cap = int(sum(bool(inf["capped"]) for inf in infos))
        out.update(n_capped=cap, re_over_rta_at={f"{l:g}": float(np.interp(l, np.log10(MTA), re_ta)) for l in (11, 12, 13, 14, 15)},
                   q_at={f"{l:g}": float(np.interp(l, np.log10(MTA), qq)) for l in (11, 12, 13, 14, 15)})
        if "Mball_over_Mta" in infos[0]:
            mb = np.array([inf["Mball_over_Mta"] for inf in infos]); out["Mball_over_Mta_at"] = {f"{l:g}": float(np.interp(l, np.log10(MTA), mb)) for l in (11, 12, 13, 14, 15)}
    # mass-decade drivers (exact decomposition)
    drv = {}
    Uref = Ulta if scope == "ta" else Ustd; Iref = Ilta if scope == "ta" else Istd; nrm = NORM_TA if scope == "ta" else 1.0
    for kk in (0.35, 1.0):
        j = np.argmin(abs(KK - kk)); tot = dP[j]
        d1 = W_M * ((U[:, j] / RHO_M) ** 2 - (Uref[:, j] / RHO_M) ** 2)
        d2 = PL[j] * (IF[j] + Iref[j]) * W_M * BIAS * (U[:, j] - Uref[:, j]) / RHO_M / nrm
        dec = {}
        for lo in range(8, 16):
            mm = (np.log10(MTA) >= lo) & (np.log10(MTA) < lo + 1)
            dec[f"{lo}-{lo + 1}"] = dict(oneh=float(d1[mm].sum() / Pstd[j]), twoh=float(d2[mm].sum() / Pstd[j]))
        drv[str(kk)] = dict(dR=float(tot / Pstd[j]), by_logMta=dec, sum_check=float((d1.sum() + d2.sum() - tot) / Pstd[j]))
    out["drivers"] = drv
    res["cases"][name] = out
    P(f"  {name:34s} E {E:+.3f} (k {kE:.2f})  D {D:+.3f} (k {kD:.2f})  | ratio-form E {Er:+.3f} D {Dr:+.3f} | s8 ratio {out['s8_ratio']:.4f}  I(1e-3) {Ichk:.5f}"
      + (f"  capped {out.get('n_capped', 0)}" if infos is not None else ""))
    P("      R(k): " + "  ".join(f"{kk:g}:{out['R_at'][str(kk)]:.3f}" for kk in KSEL))
    return out

FOOTS = ("canonical", "alt")
P("\nHalo-model framework / LCDM.  PRIMARY R = 1 + (P_F,ta - P_L,ta)/P_L,std; E = max(R-1), D = min(R-1) over 0.05 <= k <= 1.")
prim = {}
if not MUTATE:
    for ft in FOOTS:
        P(f"\n[{ft}]")
        for edge in ("cen", "emg", "s25", "s55"):
            U, inf = U_set(lambda hb: frame_profile(hb, ft, edge=edge))
            o = summarize(f"{ft}|census|{edge}", U, inf)
            if edge == "cen":
                prim[ft] = o
        U, inf = U_set(lambda hb: frame_profile(hb, ft, edge="cen", fret_mode="one"))
        summarize(f"{ft}|fret1|cen", U, inf)
        # r200m scope: catchment = r200m ball
        def f200(hb, ft=ft):
            hb2 = dict(hb); hb2["rta"] = hb["r200"]; hb2["Mta"] = hb["M"]
            return frame_profile(hb2, ft, edge="cen")
        U, inf = U_set(f200)
        summarize(f"{ft}|census|cen|r200scope", U, inf, scope="std")
    # C3 mass conservation
    c3 = 0.0
    for ft in FOOTS:
        for edge in ("cen", "emg", "s25", "s55"):
            for hb in HB[::4]:
                r, Mc, inf = frame_profile(hb, ft, edge=edge); c3 = max(c3, abs(Mc[-1] - hb["Mta"]) / hb["Mta"])
    P(f"\nC3 mass conservation |M_F(<r_ta) - M_ta|/M_ta, every variant, every 4th mass: max {c3:.1e} (<= 1e-6) -> {'PASS' if c3 <= 1e-6 else 'FAIL'}")
    c2f = max(abs(o["I_k1e3"] - 1) for n_, o in res["cases"].items() if "r200scope" not in n_)
    P(f"C2 framework cases I(1e-3): max |I-1| {c2f:.1e} -> {'PASS' if c2f <= 1e-3 else 'FAIL'}")
    res["controls"].update(C3=c3, C3_pass=c3 <= 1e-6, C2_F=c2f, C2_pass=max(c2, c2f) <= 1e-3)

    # mass-profile ratios
    P("\nM_F(<r)/M_L(<r) (census, E-cen) at r/r_ta = 0.05 0.1 0.2 0.3 0.5 1; r_e/r_ta; q:")
    prof = {}
    for ft in FOOTS:
        for lt in (12, 13, 14, 15):
            Mg = 10 ** np.interp(lt, np.log10(MTA), LM); hb = halo_basics(Mg)
            r, Mc, inf = frame_profile(hb, ft, edge="cen")
            xs = [0.05, 0.1, 0.2, 0.3, 0.5, 1.0]
            rat = [float(np.interp(x * hb["rta"], r, Mc) / M_L(hb, x * hb["rta"])) for x in xs]
            prof[f"{ft}|{lt}"] = dict(ratios=dict(zip(map(str, xs), rat)), re_over_rta=inf["re"] / hb["rta"], q=inf["q"], fret=inf["fret"],
                                       r200m_over_rta=hb["r200"] / hb["rta"], ML_re_over_Mta=inf["ML_re_over_Mta"])
            P(f"  {ft:9s} logM_ta {lt}: " + " ".join(f"{v:.2f}" for v in rat) + f" | r_e/r_ta {inf['re'] / hb['rta']:.3f} (r200m/r_ta {hb['r200'] / hb['rta']:.3f}), q {inf['q']:.2f}, f_ret {inf['fret']:.2f}")
    res["profiles"] = prof

    # ------------------------------------------------ PM comparison
    C5 = lj(CFG555)
    PMRUNS = [("425_R3_can_512", 512, "canonical", "one"), ("439_A_alt_512", 512, "alt", "one"), ("439_B_DEcan_512", 512, "canonical", "one"),
              ("460_can_512_s360", 512, "canonical", "one"), ("518_DCcan_512", 512, "canonical", "one"),
              ("424_TAcan", 256, "canonical", "one"), ("424_TAalt", 256, "alt", "one")]
    MRES = {512: 12.3, 256: 13.2}
    P("\nPM-matched halo model (f_ret = 1, E-cen, framework only for log M_ta >= 12.3 (512^3) / 13.2 (256^3)) vs CFG555 PM gravitating ratio:")
    pmm = {}
    for N in (512, 256):
        for ft in FOOTS:
            def fpm(hb, ft=ft, N=N):
                if math.log10(hb["Mta"]) < MRES[N]:
                    return frame_profile(hb, ft, mode="lta")
                return frame_profile(hb, ft, edge="cen", fret_mode="one")
            U, inf = U_set(fpm)
            pmm[(N, ft)] = summarize(f"PMmatched|N{N}|{ft}", U, None)
    for name, N, ft, _ in PMRUNS:
        run = C5["runs"][name]; g = run["gravitating"]; kat = g["k_at"]
        d = lj(os.path.join(EXT, "cfg555_work", f"cfg555_{name}.json")); s0 = lj(os.path.join(EXT, d["s0_base"] + ".json"))["snap"]["z0"]
        k = np.array(d["k"]); rpm = np.array(d["P_grav"]) / np.interp(k, np.array(s0["k"]), np.array(s0["P"]))
        rpm_kat = float(np.interp(kat, k, rpm)); rpm_1 = float(g["r_at"]["1.0"])
        R = np.array(pmm[(N, ft)]["R"]); Rhm_kat = float(np.interp(kat, KK, R)); Rhm_1 = float(np.interp(1.0, KK, R))
        Rprim = np.array(prim[ft]["R"]); Rp_kat = float(np.interp(kat, KK, Rprim))
        fr = (Rhm_kat - 1) / (rpm_kat - 1) if rpm_kat != 1 else float("nan")
        rep = (0.5 <= fr <= 2.0) and (np.sign(Rhm_1 - 1) == np.sign(rpm_1 - 1))
        row = "  ".join(f"{kk:g}:{np.interp(kk, k, rpm):.3f}/{np.interp(kk, KK, R):.3f}" for kk in (0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1.0))
        P(f"  {name:18s} N{N} {ft:9s} PM pdev {g['pdev']:.3f} at k {kat:.2f}: r_PM {rpm_kat:.3f} vs HM {Rhm_kat:.3f} (primary census {Rp_kat:.3f}); "
          f"k=1: r_PM {rpm_1:.3f} vs HM {Rhm_1:.3f}; fraction {fr:+.2f} -> {'REPRODUCED' if rep else 'NOT REPRODUCED'}")
        P(f"      k: PM/HM  {row}")
        res["pm"][name] = dict(N=N, foot=ft, pm_pdev=g["pdev"], k_at=kat, r_pm_kat=rpm_kat, r_pm_k1=rpm_1, R_hm_kat=Rhm_kat, R_hm_k1=Rhm_1,
                               R_primary_kat=Rp_kat, fraction=fr, reproduced=bool(rep), r_pm_curve=dict(k=k.tolist(), r=rpm.tolist()))

    # ------------------------------------------------ verdicts
    P("\nVerdict per footing (PRIMARY: census f_ret, E-cen, all halos):")
    def cls(E, D, rep):
        mx = max(abs(E), abs(D))
        if E > 0.10: return "INTRINSIC"
        if mx <= 0.10: return "MIXED" if rep else "ARTEFACT"
        return "MIXED"
    for ft in FOOTS:
        o = prim[ft]
        rep = any(v["reproduced"] for v in res["pm"].values() if v["N"] == 512 and v["foot"] == ft)
        vp = cls(o["E"], o["D"], rep)
        varc = {}
        for n_, oo in res["cases"].items():
            if n_.startswith(ft + "|") and n_ != f"{ft}|census|cen":
                varc[n_] = cls(oo["E"], oo["D"], rep)
                if "r200scope" not in n_:
                    varc[n_ + "|ratioform"] = cls(oo["E_ratio"], oo["D_ratio"], rep)
        varc[f"{ft}|census|cen|ratioform"] = cls(o["E_ratio"], o["D_ratio"], rep)
        diff = sorted(n_ for n_, c in varc.items() if c != vp)
        res["verdict"][ft] = dict(verdict=vp, E=o["E"], D=o["D"], kE=o["kE"], kD=o["kD"], pm_reproduced_512=rep, variant_classes=varc,
                                  variant_sensitive=diff, validation={str(N): v["label"] for N, v in val.items()})
        P(f"  {ft}: {vp}{'  VARIANT-SENSITIVE: ' + ', '.join(diff) if diff else ''}")
        P(f"     E {o['E']:+.3f} at k {o['kE']:.2f}, D {o['D']:+.3f} at k {o['kD']:.2f}; PM-matched reproduces a 512^3 PM run: {rep}; "
          f"validation 256/512: {val[256]['label']}/{val[512]['label']}; s8 ratio {o['s8_ratio']:.4f}")
    # ------------------------------------------------ POST-FREEZE (2026-10-10), reported only, no verdict input: the R5 law-respecting engine (CFG530)
    P("\nPOST-FREEZE (reported, not a verdict input): CFG530 R5 engine (census f_ret, draw only from the shell r_e..r_ta), gravitating r = P/P_S0 from cfg555_results.json, vs halo-model PRIMARY R:")
    pf = {}
    for n_, v in C5["cfg530"].items():
        g = v["gravitating"]; ft = "alt" if "alt" in n_ else "canonical"; R = np.array(prim[ft]["R"])
        pf[n_] = dict(pdev=g["pdev"], k_at=g["k_at"], r05=g["r_at"]["0.5"], r1=g["r_at"]["1.0"], R05=float(np.interp(0.5, KK, R)), R1=float(np.interp(1.0, KK, R)))
        if "N512" in n_ or "N256" in n_:
            P(f"  {n_:22s} pdev {g['pdev']:.3f} (k {g['k_at']:.2f}); r(0.5) {g['r_at']['0.5']:.3f} vs HM {pf[n_]['R05']:.3f}; r(1) {g['r_at']['1.0']:.3f} vs HM {pf[n_]['R1']:.3f}")
    res["posthoc_cfg530"] = pf
    P("\nDrivers of the PRIMARY Delta R (1-halo / 2-halo by log M_ta decade):")
    for ft in FOOTS:
        for kk in ("0.35", "1.0"):
            dv = prim[ft]["drivers"][kk]
            s = "  ".join(f"{d_}:{v['oneh']:+.3f}/{v['twoh']:+.3f}" for d_, v in dv["by_logMta"].items() if abs(v["oneh"]) + abs(v["twoh"]) > 5e-4)
            P(f"  {ft:9s} k={kk}: dR {dv['dR']:+.3f} (sum check {dv['sum_check']:.1e})  {s}")
else:
    teeth = {}
    for ft in FOOTS:
        P(f"\n[{ft}] MUTATE")
        Up, ip = U_set(lambda hb: frame_profile(hb, ft, edge="cen")); op = summarize(f"{ft}|primary", Up, ip)
        U1, i1 = U_set(lambda hb: frame_profile(hb, ft, mode="lta")); o1 = summarize(f"{ft}|M1_lta", U1, i1)
        m1 = float(np.max(np.abs(np.array(o1["R"]) - 1)))
        U2, i2 = U_set(lambda hb: frame_profile(hb, ft, mode="bare")); o2 = summarize(f"{ft}|M2_bare_noedge", U2, i2)
        U3, i3 = U_set(lambda hb: frame_profile(hb, ft, edge="cen", mode="noshell")); o3 = summarize(f"{ft}|M3_noshell", U3, i3)
        m = (KK >= 0.3) & (KK <= 1.0)
        d3 = float(np.max(np.abs(np.array(o3["R"])[m] - np.array(op["R"])[m])))
        t1, t2, t3 = m1 <= 1e-10, o2["E"] > op["E"], d3 >= 0.01
        P(f"  M1 max|R-1| {m1:.1e} (<= 1e-10) -> {'BITES' if t1 else 'FAILS'};  M2 E {o2['E']:+.3f} vs primary {op['E']:+.3f} -> {'BITES' if t2 else 'FAILS'}"
          f" (M_ball/M_ta at logM_ta 12/14: {o2['Mball_over_Mta_at']['12']:.2f}/{o2['Mball_over_Mta_at']['14']:.2f});  M3 max|dR| (0.3-1) {d3:.3f} (>= 0.01) -> {'BITES' if t3 else 'FAILS'}")
        teeth[ft] = dict(M1=m1, M1_bites=t1, M2_E=o2["E"], primary_E=op["E"], M2_bites=t2, M3_maxdR=d3, M3_bites=t3)
    res["teeth"] = teeth
    allb = all(v["M1_bites"] and v["M2_bites"] and v["M3_bites"] for v in teeth.values())
    P(f"\nMUTATE: all teeth bite -> {allb}")

json.dump(res, open(os.path.join(HERE, f"cfg556_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg556_halo_model{SUF}.out"), "w").write("\n".join(OUT) + "\n")
if MUTATE:
    sys.exit(1 if allb else 0)

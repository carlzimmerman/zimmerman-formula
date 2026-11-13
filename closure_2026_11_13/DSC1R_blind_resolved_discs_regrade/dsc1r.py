#!/usr/bin/env python3
"""DSC1R (FROZEN_CRITERIA.md, ad6ac2377e): blind re-grade of the crossing-speed joint on resolved high-z rotation curves.
Genzel+2017 six deep curves (CFG400 points, CFG401 Table 1) and Lelli+2023 (digitised). Everything is built here; the
CFG4xx / SRJ3 / FRZ1 code was read, not executed. Footings never pooled.
  python3 -I -B dsc1r.py -> dsc1r.json / .out, dsc1r_MUTATE_TWV.json / .out, dsc1r_MUTATE_TWM.json / .out
TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed."""
import os, sys, csv, json, math
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.special import i0e, i1e, k0e, k1e
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)

# ------------------------------------------------------------------ constants and the rule
G, MS, KPC, MPC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; FOOTS = ("canonical", "alt")
X = 5.41; H0 = 67.4e3 / MPC; OL = 0.6847; OM = 1 - OL
hh = 0.6736; FB = 0.02237 / (0.02237 + 0.1200); RHO_M = OM * 2.77536627e11          # Msun/h per (Mpc/h)^3, comoving
def E(z): return math.sqrt(OM * (1 + z) ** 3 + OL)
def vstar0(ft): return A0[ft] / (10 * (1 + X) * H0)                                 # m/s
def logthr(ft, z): return math.log10((vstar0(ft) / E(z)) ** 4 / (G * A0[ft]) / MS)
def law(gN, a0): return 0.5 * (gN + np.sqrt(gN * gN + 4 * a0 * gN))

# ------------------------------------------------------------------ reference halo (FRZ1 / SRJ3 construction, X = 5.41)
def m_nfw(x): return np.log1p(x) - x / (1 + x)
def Omz(z): return OM * (1 + z) ** 3 / (OM * (1 + z) ** 3 + OL)
def dta_of(z): return 5.55 + (11.81 - 5.55) * (1 - Omz(z)) / (1 - OM)
def conc(M, z): return 10.14 * (M / 2e12) ** -0.081 * (1 + z) ** -1.01
def hb(M, z):
    c = conc(M, z); r2 = (3 * M / (4 * math.pi * 200 * RHO_M)) ** (1 / 3); mc = m_nfw(c); dta = dta_of(z)
    xta = brentq(lambda x: m_nfw(c * x) / mc / x ** 3 - dta / 200.0, 1.0, 80.0, xtol=1e-13)
    return dict(M=M, c=c, r200=r2, rs=r2 / c, xta=xta, rta=xta * r2, Mta=M * m_nfw(c * xta) / mc)
_H = {}
def halo(Mb, z):
    key = (round(math.log10(Mb), 10), round(z, 8))
    if key not in _H:
        Mta = X * Mb * hh / (1 - FB)
        lM = brentq(lambda l: hb(10 ** l, z)["Mta"] / Mta - 1, math.log10(Mta) - 2, math.log10(Mta) + 1, xtol=1e-13)
        b = hb(10 ** lM, z); a = MPC / hh / (1 + z)
        _H[key] = dict(b, rs_m=b["rs"] * a, rta_m=b["rta"] * a, cta=b["c"] * b["xta"], Mb=Mb, z=z)
    return _H[key]
def g_ref(R_kpc, Mb, z):
    H = halo(Mb, z); r = np.minimum(np.asarray(R_kpc) * KPC, H["rta_m"])
    C = X * Mb * MS * m_nfw(r / H["rs_m"]) / m_nfw(H["cta"])
    return G * C / (np.asarray(R_kpc) * KPC) ** 2

# ------------------------------------------------------------------ baryon components (Newtonian)
def g_disc(R, Rd, M):
    """thin exponential (Freeman) disc, R and Rd in kpc, M in Msun -> g (m/s^2)."""
    if M <= 0: return np.zeros_like(R)
    y = np.maximum(R / (2 * Rd), 1e-6)
    br = i0e(y) * k0e(y) - i1e(y) * k1e(y)
    v2 = 2 * G * M * MS / (Rd * KPC) * y ** 2 * br
    return v2 / (R * KPC)
def g_hern(R, a, M):
    return G * M * MS / ((R + a) * KPC) ** 2 if M > 0 else np.zeros_like(R)

# ------------------------------------------------------------------ data: Genzel+2017
T1 = {"COS4 01351": (0.854, 7.68, 75, 7.3, 39, 0.20, 276, 0.54, 0.9), "D3a 6397": (1.500, 8.46, 30, 7.4, 73, 0.35, 310, 1.2, 2.3),
      "GS4 43501": (1.613, 8.47, 62, 4.9, 39, 0.40, 257, 0.41, 0.75), "zC 406690": (2.196, 8.26, 25, 5.5, 74, 0.60, 301, 0.42, 1.4),
      "zC 400569": (2.242, 8.23, 45, 3.3, 34, 0.37, 364, 1.2, 2.5), "D3a 15504": (2.383, 8.14, 34, 6.0, 76, 0.15, 299, 1.1, 2.0)}
INC_ERR = {g: (12.0 if g == "zC 406690" else 10.0) for g in T1}
FWHM = 0.6
GROWS = list(csv.DictReader(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG400_genzel17_selfcal", "cfg400_points.csv"))))
LROWS = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "lelli2023_rotcur_digitised", "lelli2023_rotcur_digitised.csv"))))

def sig_log(V, eV, Vc2): return np.sqrt((2 * V * eV / Vc2 / math.log(10)) ** 2 + 0.05 ** 2)

def genzel_baryons(g, B):
    z, kpa, inc, Rh, s0, bt, vc, ms, mb = T1[g]
    Ms, Mb = ms * 1e11, mb * 1e11
    Mbul = min(bt * Mb, Ms); Mgas = Mb - Ms
    f = 10 ** {"M-": -0.2, "M+": 0.2}.get(B, 0.0)
    Ms, Mbul, Mgas = Ms * f, Mbul * f, Mgas * f
    if B == "STARS": Mgas = 0.0
    if B == "GLO": Mgas *= 10 ** -0.3
    if B == "GHI": Mgas *= 10 ** 0.3
    Rd = Rh / 1.678
    comp = dict(Mstar=Ms, Mbul=Mbul, Mdisc=Ms - Mbul, Mgas=Mgas, Rd=Rd, a_b=1.0 / 1.8153)
    comp["Mb"] = Ms + Mgas
    return comp
def gN_of(comp, R):
    return (g_disc(R, comp["Rd"], comp["Mdisc"]) + g_hern(R, comp["a_b"], comp["Mbul"]) + g_disc(R, comp["Rgas"] if "Rgas" in comp else 2 * comp["Rd"], comp["Mgas"]))

def build_genzel(g, B="MAIN"):
    z, kpa, inc0, Rh, s0, bt, vc, ms, mb = T1[g]
    inc = inc0 + {"I-": -INC_ERR[g], "I+": INC_ERR[g]}.get(B, 0.0); inc = min(max(inc, 10.0), 85.0)
    k = {"AD0": 0.0, "AD2": 2.0}.get(B, 1.0); cut = FWHM if B == "BEAM" else 0.5 * FWHM
    pts = [(float(r["offset_arcsec"]), float(r["value"]), float(r["err"])) for r in GROWS if r["galaxy"] == g and r["kind"] == "v"]
    pts = [p for p in pts if abs(p[0]) >= cut]
    sides = {s: sorted([p for p in pts if (p[0] > 0) == (s > 0)], key=lambda p: abs(p[0])) for s in (+1, -1)}
    if B == "OUT":
        sides = {s: v[:-1] for s, v in sides.items()}
    pts = sides[+1] + sides[-1]
    neff = sum(max(1.0, (abs(v[-1][0]) - cut) / FWHM) for v in sides.values() if v)
    off = np.array([abs(p[0]) for p in pts]); R = off * kpa
    si = math.sin(math.radians(inc))
    V = np.array([abs(p[1]) for p in pts]) / si; eV = np.array([max(p[2], 1.0) for p in pts]) / si
    Vc2 = V ** 2 + k * 3.36 * s0 ** 2 * (R / Rh)
    comp = genzel_baryons(g, B)
    return dict(name=g, src="Genzel+17", z=z, R=R, lg=np.log10(Vc2 * 1e6 / (R * KPC)), sig=sig_log(V, eV, Vc2), n=len(R), neff=neff,
                c=len(R) / neff, comp=comp, Mb=comp["Mb"], inc=inc)

# ------------------------------------------------------------------ data: Lelli+2023
def DA_kpc_per_arcsec(z):
    Dc = quad(lambda zz: 1 / E(zz), 0, z, epsabs=0, epsrel=1e-10)[0] * 2.99792458e5 / 67.4      # Mpc
    return Dc / (1 + z) * 1e3 * math.pi / (180 * 3600)
def DL_Mpc(z): return quad(lambda zz: 1 / E(zz), 0, z, epsabs=0, epsrel=1e-10)[0] * 2.99792458e5 / 67.4 * (1 + z)
LZ = {"zC-488879": 1.46997, "zC-400569": 2.23999}
LINC = {"zC-488879": (71.6, 4.1), "zC-400569": (54.5, 5.0)}
LRE = {"zC-488879": 0.88, "zC-400569": 0.76}
def Lprime10(S, nu_rest, z, R_J1):
    nu = nu_rest / (1 + z)
    return 3.25e7 * S * nu ** -2 * DL_Mpc(z) ** 2 * (1 + z) ** -3 / R_J1
LP488 = Lprime10(0.56, 230.538, LZ["zC-488879"], 0.85)
LP400 = Lprime10(0.50, 345.796, LZ["zC-400569"], 0.60)
def lelli_baryons(B):
    kpa = DA_kpc_per_arcsec(LZ["zC-488879"])
    Ms = 5.2e10 * 10 ** {"M-": -0.3, "M+": 0.3}.get(B, 0.0)
    alpha = {"GLO": 0.4, "GHI": 4.3}.get(B, math.sqrt(0.4 * 4.3))
    Mgas = 0.0 if B == "STARS" else alpha * LP488
    Rd = LRE["zC-488879"] * kpa / 1.678
    comp = dict(Mstar=Ms, Mbul=0.63 * Ms, Mdisc=0.37 * Ms, Mgas=Mgas, Rd=Rd, Rgas=Rd, a_b=3.0 / 1.8153, alpha=alpha)
    comp["Mb"] = Ms + Mgas
    return comp
def build_lelli(gal, B="MAIN", comp=None):
    z = LZ[gal]; kpa = DA_kpc_per_arcsec(z); i0, ie = LINC[gal]
    inc = i0 + {"I-": -ie, "I+": ie}.get(B, 0.0)
    fi = math.sin(math.radians(i0)) / math.sin(math.radians(inc))
    k = {"AD0": 0.0, "AD2": 2.0}.get(B, 1.0); Re = LRE[gal] * kpa
    rows = [r for r in LROWS if r["galaxy"] == gal]
    lines = {}
    for r in rows: lines.setdefault(r["line"], []).append(r)
    keep = []
    for ln, rr in lines.items():
        rr = sorted(rr, key=lambda r: float(r["radius_arcsec"]))
        if B == "BEAM": rr = rr[1:]
        if B == "OUT": rr = rr[:-1]
        keep += rr
    R = np.array([float(r["radius_arcsec"]) for r in keep]) * kpa
    V = np.array([float(r["vrot_kms"]) for r in keep]) * fi
    eV = np.array([0.5 * (float(r["err_lo_kms"]) + float(r["err_hi_kms"])) for r in keep]) * fi
    sg = np.array([37.0 if r["line"] == "Halpha" else 15.0 for r in keep])
    Vc2 = V ** 2 + k * 3.36 * sg ** 2 * (R / Re)
    if comp is None: comp = lelli_baryons(B)
    return dict(name=gal, src="Lelli+23", z=z, R=R, lg=np.log10(Vc2 * 1e6 / (R * KPC)), sig=sig_log(V, eV, Vc2), n=len(R), neff=len(R) / 2.0,
                c=2.0, comp=comp, Mb=comp["Mb"], inc=inc)

def build_all(B="MAIN"):
    D = [build_genzel(g, B) for g in T1]
    D.append(build_lelli("zC-488879", B))
    if B == "ALTC":
        gz = [d for d in D if d["name"] == "zC 400569"][0]
        alt = build_lelli("zC-400569", "MAIN", comp=gz["comp"])
        alt.update(name="zC 400569", src="Lelli+23 curve", z=gz["z"])
        D = [alt if d["name"] == "zC 400569" else d for d in D]
    for d in D:
        d["gN"] = gN_of(d["comp"], d["R"]); d["gref"] = g_ref(d["R"], d["Mb"], d["z"])
    return D

# ------------------------------------------------------------------ fits and labels
AG = np.round(np.arange(-2.0, 40.0 + 1e-9, 0.005), 6)
def chi_grid(D, Agrid):
    tot = np.zeros(len(Agrid))
    for d in D:
        gm = d["gN"][None, :] + Agrid[:, None] * d["gref"][None, :]
        with np.errstate(invalid="ignore", divide="ignore"):
            c = np.sum(((d["lg"][None, :] - np.log10(np.where(gm > 0, gm, np.nan))) / d["sig"][None, :]) ** 2, axis=1) / d["c"]
        tot += np.where(np.all(gm > 0, axis=1), c, np.inf)
    return tot
def chi_law(D, a0): return float(sum(np.sum(((d["lg"] - np.log10(law(d["gN"], a0))) / d["sig"]) ** 2) / d["c"] for d in D))
def chi_at(D, A): return float(chi_grid(D, np.array([A]))[0])

def grade_above(D):
    if not D: return dict(word="NO POWER", n=0, note="empty group")
    ch = chi_grid(D, AG); i = int(np.argmin(ch)); cmin = float(ch[i]); neff = sum(d["neff"] for d in D); dof = max(neff - 1, 1.0)
    s2 = max(1.0, cmin / dof); ok = ch <= cmin + 3.84 * s2; lo, hi = float(AG[ok].min()), float(AG[ok].max())
    contiguous = bool(np.all(ok[np.argmax(ok): len(ok) - np.argmax(ok[::-1])]))
    exc = {a: not (lo <= a <= hi) for a in (0, 1, 2)}
    power = any(exc.values())
    if power and not exc[1] and exc[0]: w = "JOINT'S STATEMENT HOLDS"
    elif power and exc[1]: w = "JOINT'S STATEMENT FAILS"
    else: w = "NO POWER"
    return dict(word=w, n=len(D), names=[d["name"] for d in D], A_best=float(AG[i]), A_lo=lo, A_hi=hi, contiguous=contiguous,
                grid_edge=bool(lo <= AG[0] or hi >= AG[-1]), chi2_min=cmin, neff=neff, dof=dof, s2=s2, p_abs=float(CHI2.sf(cmin, dof)),
                excl={str(k): v for k, v in exc.items()}, chi2_A0=chi_at(D, 0.0), chi2_A1=chi_at(D, 1.0), chi2_A2=chi_at(D, 2.0),
                side=("A < 1" if AG[i] < 1 else "A > 1") if w == "JOINT'S STATEMENT FAILS" else None)
AGH = AG[AG >= 0]
def grade_below(D, a0):
    if not D: return dict(word="NO POWER", n=0, note="empty group")
    neff = sum(d["neff"] for d in D)
    cL = chi_law(D, a0); cN = chi_at(D, 0.0); chH = chi_grid(D, AGH); j = int(np.argmin(chH)); cH = float(chH[j]); cH1 = chi_at(D, 1.0)
    cand = [(cL, neff), (cN, neff), (cH, max(neff - 1, 1.0))]; best = min(cand, key=lambda t: t[0]); s2 = max(1.0, best[0] / best[1])
    power = max(abs(cN - cL), abs(cH1 - cL)) >= 9 * s2
    pL = float(CHI2.sf(cL, neff)); pref = min(cN, cH) <= cL - 9 * s2
    if not power: w = "NO POWER"
    elif pref and pL < 0.0027: w = "LAW FAILS BELOW"
    else: w = "LAW HOLDS BELOW"
    return dict(word=w, n=len(D), names=[d["name"] for d in D], chi2_L=cL, chi2_N=cN, chi2_H=cH, A_H=float(AGH[j]), chi2_H1=cH1, neff=neff, s2=s2,
                p_L=pL, p_N=float(CHI2.sf(cN, neff)), p_H=float(CHI2.sf(cH, max(neff - 1, 1.0))), delta=cL - min(cN, cH), power=bool(power),
                preferred=("N" if cN <= cH else "H") if pref else None)

def member(d, ft): return math.log10(d["Mb"]) > logthr(ft, d["z"])
def grade(D, ft):
    ab = [d for d in D if member(d, ft)]; be = [d for d in D if not member(d, ft)]
    return dict(above=grade_above(ab), below=grade_below(be, A0[ft]), above_names=[d["name"] for d in ab], below_names=[d["name"] for d in be])

# ------------------------------------------------------------------ R_fold (reported)
FLD = os.path.join(REPO, "fable52_push", "FLD1_fold_reach", "runs")
MASSES = [6.5, 7, 8, 9, 9.4, 10, 10.45, 10.7, 10.9, 11.2, 11.5, 12]
FT = {f: {M: np.array(json.load(open(os.path.join(FLD, f"hubble_{f}_M{M:g}_zi10_N2400.json")))["series"]) for M in MASSES} for f in FOOTS}
def rfold(ft, z, lM):
    R = []
    for M in MASSES:
        S = FT[ft][M]; o = np.argsort(S[:, 1]); R.append(float(np.interp(z, S[o, 1], S[o, 2])))
    R = np.array(R)
    if np.any(R <= 0): return float(np.interp(lM, MASSES, R))
    return float(10 ** np.interp(lM, MASSES, np.log10(R)))

# ------------------------------------------------------------------ run
P("DSC1R blind re-grade of the crossing-speed joint on resolved high-z curves (criteria ad6ac2377e).")
P("TEST lane. Adopts nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.")
RES = dict(lane="DSC1R", criteria="ad6ac2377e", note="Adopts nothing. kappa = 1/2 FITTED; not theory closed.")

# KA1 (SI)
ka1 = {}
for ft in FOOTS:
    ka1[ft] = dict(vstar0_kms=vstar0(ft) / 1e3, logthr_z2=logthr(ft, 2.0))
Ht = halo(2e11, 2.3); r = Ht["rta_m"]; cold_rta = X * 2e11 * MS * m_nfw(r / Ht["rs_m"]) / m_nfw(Ht["cta"])
rho_m_SI = OM * 3 * H0 ** 2 / (8 * math.pi * G) * (1 + 2.3) ** 3
r200_SI = (3 * Ht["M"] / hh * MS / (4 * math.pi * 200 * rho_m_SI)) ** (1 / 3); r200_scr = Ht["r200"] / (1 + 2.3) / hh * MPC
ka1_ok = (abs(ka1["canonical"]["vstar0_kms"] - 668.5) <= 0.1 and abs(ka1["alt"]["vstar0_kms"] - 807.9) <= 0.1 and abs(ka1["canonical"]["logthr_z2"] - 11.279) <= 0.005
          and abs(ka1["alt"]["logthr_z2"] - 11.526) <= 0.005 and abs(cold_rta / (X * 2e11 * MS) - 1) <= 1e-8 and abs(r200_SI / r200_scr - 1) <= 1e-3)
lawchk = float(np.max(np.abs((lambda g, gn, a: g * g / (a + g) / gn - 1)(law(np.logspace(-13, -8, 50), 1e-10), np.logspace(-13, -8, 50), 1e-10))))
ka1.update(cold_rta_over_XMb=cold_rta / (X * 2e11 * MS), r200m_SI_kpc=r200_SI / KPC, r200m_script_kpc=r200_scr / KPC, rs_kpc=Ht["rs_m"] / KPC,
           c200m=Ht["c"], rta_kpc=Ht["rta_m"] / KPC, law_identity_maxrel=lawchk, pass_=bool(ka1_ok and lawchk < 1e-12))
P(f"KA1 SI: v*(0) {ka1['canonical']['vstar0_kms']:.2f} / {ka1['alt']['vstar0_kms']:.2f} km/s; log thr z 2 {ka1['canonical']['logthr_z2']:.3f} / {ka1['alt']['logthr_z2']:.3f}; "
  f"halo (M_b 2e11, z 2.3): cold(r_ta)/(X M_b) {ka1['cold_rta_over_XMb']:.10f}, r200m SI {ka1['r200m_SI_kpc']:.2f} vs {ka1['r200m_script_kpc']:.2f} kpc, "
  f"c {Ht['c']:.2f}, r_s {ka1['rs_kpc']:.1f} kpc, r_ta {ka1['rta_kpc']:.1f} kpc; law identity {lawchk:.1e} -> {'PASS' if ka1['pass_'] else 'FAIL'}")
P(f"  reported: CO L'(1-0) zC-488879 {LP488:.3e} (gas at alpha 0.4 {0.4*LP488:.2e}, 4.3 {4.3*LP488:.2e}; CFG278 7.8e9 / 8.4e10); "
  f"zC-400569 {LP400:.3e} (0.4 -> {0.4*LP400:.2e}; CFG278 9.4e9); kpc/arcsec {DA_kpc_per_arcsec(1.46997):.3f} / {DA_kpc_per_arcsec(2.23999):.3f}")
RES["KA1"] = ka1

D0 = build_all("MAIN")
RES["discs"] = []
for d in D0:
    row = dict(name=d["name"], src=d["src"], z=d["z"], logMb=math.log10(d["Mb"]), n=d["n"], neff=d["neff"], c=d["c"], R_kpc=[float(d["R"].min()), float(d["R"].max())],
               gN_over_a0_can=[float(d["gN"].min() / A0["canonical"]), float(d["gN"].max() / A0["canonical"])], gref_over_gN_outer=float(d["gref"][np.argmax(d["R"])] / d["gN"][np.argmax(d["R"])]),
               halo=dict(c=halo(d["Mb"], d["z"])["c"], rs_kpc=halo(d["Mb"], d["z"])["rs_m"] / KPC, rta_kpc=halo(d["Mb"], d["z"])["rta_m"] / KPC), comp={k: float(v) for k, v in d["comp"].items()})
    for ft in FOOTS:
        row[ft] = dict(logthr=logthr(ft, d["z"]), margin=math.log10(d["Mb"]) - logthr(ft, d["z"]), group="ABOVE" if member(d, ft) else "below",
                       R_fold_kpc=rfold(ft, d["z"], math.log10(d["Mb"])))
        row[ft]["pts_outside_Rfold"] = int(np.sum(d["R"] > row[ft]["R_fold_kpc"]))
        # per-disc numbers
        ch = chi_grid([d], AG); i = int(np.argmin(ch)); s2 = max(1.0, ch[i] / max(d["neff"] - 1, 1.0)); ok = ch <= ch[i] + 3.84 * s2
        row[ft].update(A_best=float(AG[i]), A_lo=float(AG[ok].min()), A_hi=float(AG[ok].max()), chi2_A0=float(ch[np.argmin(abs(AG))]), chi2_A1=chi_at([d], 1.0),
                       chi2_L=chi_law([d], A0[ft]), chi2_min_A=float(ch[i]))
    RES["discs"].append(row)
    P(f"  {d['name']:11s} {d['src']:9s} z {d['z']:.3f} logMb {row['logMb']:.3f} n {d['n']:2d} Neff {d['neff']:5.2f} R {row['R_kpc'][0]:.1f}-{row['R_kpc'][1]:.1f} kpc "
      f"gN/a0 {row['gN_over_a0_can'][1]:.2f}-{row['gN_over_a0_can'][0]:.2f} gref/gN(outer) {row['gref_over_gN_outer']:.3f} | "
      + " | ".join(f"{ft[:3]} {row[ft]['group']} ({row[ft]['margin']:+.3f}) Rfold {row[ft]['R_fold_kpc']:.0f} out {row[ft]['pts_outside_Rfold']}; A {row[ft]['A_best']:.2f} [{row[ft]['A_lo']:.2f},{row[ft]['A_hi']:.2f}] "
                     f"chi2 A0 {row[ft]['chi2_A0']:.1f} A1 {row[ft]['chi2_A1']:.1f} L {row[ft]['chi2_L']:.1f}" for ft in FOOTS))

def show(tag, G_, ft):
    a, b = G_["above"], G_["below"]
    sa = (f"above {a['names']} A {a['A_best']:.3f} [{a['A_lo']:.3f}, {a['A_hi']:.3f}] chi2min {a['chi2_min']:.2f} Neff {a['neff']:.1f} s2 {a['s2']:.2f} p {a['p_abs']:.2g} "
          f"chi2(A=0,1,2) {a['chi2_A0']:.1f}/{a['chi2_A1']:.1f}/{a['chi2_A2']:.1f} -> {a['word']}" if a["n"] else "above: empty -> NO POWER")
    sb = (f"below {b['names']} chi2 L {b['chi2_L']:.1f} N {b['chi2_N']:.1f} H {b['chi2_H']:.1f} (A {b['A_H']:.2f}) H1 {b['chi2_H1']:.1f} Neff {b['neff']:.1f} s2 {b['s2']:.2f} "
          f"p_L {b['p_L']:.2g} delta {b['delta']:+.1f} -> {b['word']}" if b["n"] else "below: empty -> NO POWER")
    P(f"[{ft}] {tag}: {sa}"); P(f"[{ft}] {tag}: {sb}")

BRK = ["AD0", "AD2", "M-", "M+", "STARS", "GLO", "GHI", "I-", "I+", "BEAM", "OUT", "ALTC"]
RES["foot"] = {}
for ft in FOOTS:
    R = RES["foot"][ft] = {}
    R["main"] = grade(D0, ft); show("MAIN", R["main"], ft)
    # context: the law on the above discs, X_PD1 position
    ab = [d for d in D0 if member(d, ft)]
    if ab:
        R["context_law_on_above"] = dict(chi2_L=chi_law(ab, A0[ft]), chi2_A1=chi_at(ab, 1.0))
        P(f"[{ft}]   context (not graded): law on the above discs chi2 {R['context_law_on_above']['chi2_L']:.1f} vs A = 1 {R['context_law_on_above']['chi2_A1']:.1f}; "
          f"PD1 X ~56-59 -> A ~{55.72/X:.1f}-{59.50/X:.1f}: {'inside' if R['main']['above']['A_lo'] <= 10.3 and R['main']['above']['A_hi'] >= 11.0 else 'outside'} the A interval")
    # KA2 / KA3
    Dk = build_all("MAIN")
    for d in Dk:
        d["lg"] = np.log10(d["gN"] + d["gref"]) if member(d, ft) else np.log10(law(d["gN"], A0[ft]))
    gk = grade(Dk, ft)
    R["KA2"] = dict(A_best=gk["above"].get("A_best"), word=gk["above"]["word"], pass_=bool(gk["above"]["n"] and abs(gk["above"]["A_best"] - 1) <= 0.01 and gk["above"]["word"] == "JOINT'S STATEMENT HOLDS"))
    R["KA3"] = dict(chi2_L=gk["below"].get("chi2_L"), word=gk["below"]["word"], pass_=bool(gk["below"]["n"] and gk["below"]["chi2_L"] < 1e-6 and gk["below"]["word"] == "LAW HOLDS BELOW"))
    P(f"[{ft}] KA2 synthetic A = 1: A_best {R['KA2']['A_best']}, {R['KA2']['word']} -> {'PASS' if R['KA2']['pass_'] else 'FAIL'}; "
      f"KA3 synthetic law: chi2_L {R['KA3']['chi2_L']:.2e}, {R['KA3']['word']} -> {'PASS' if R['KA3']['pass_'] else 'FAIL'}")
    # brackets
    R["brackets"] = {}
    for B in BRK:
        gb = grade(build_all(B), ft); R["brackets"][B] = gb; show(B, gb, ft)

# twins
TW = {}
for t in ("TWV", "TWM"):
    TW[t] = dict(lane="DSC1R", twin=t, foot={})
    for ft in FOOTS:
        Dt = build_all("MAIN")
        if t == "TWV":
            for d in Dt: d["lg"] = d["lg"] + math.log10(1.5625)
        else:
            for d in Dt:
                d["gN"] = 0.5 * d["gN"]; d["gref"] = g_ref(d["R"], 0.5 * d["Mb"], d["z"])
        # membership fixed at main
        m = RES["foot"][ft]["main"]
        ab = [d for d in Dt if d["name"] in m["above_names"]]; be = [d for d in Dt if d["name"] in m["below_names"]]
        ga, gbb = grade_above(ab), grade_below(be, A0[ft])
        ma, mb_ = m["above"], m["below"]
        bite_a = bool(ga["n"] and (abs(ga["A_best"] - ma["A_best"]) >= 0.5 or ga["word"] != ma["word"]))
        bite_b = bool(gbb["n"] and (abs(gbb["delta"] - mb_["delta"]) >= 9 or gbb["word"] != mb_["word"]))
        TW[t]["foot"][ft] = dict(above=ga, below=gbb, bites_above=bite_a, bites_below=bite_b)
        P(f"[{ft}] twin {t}: above A {ga.get('A_best', float('nan')):.3f} ({ga['word']}) bites {bite_a}; below delta {gbb.get('delta', float('nan')):+.1f} ({gbb['word']}) bites {bite_b}")

# final words
def flips(ft, grp):
    base = RES["foot"][ft]["main"][grp]["word"]
    return [B for B in BRK if RES["foot"][ft]["brackets"][B][grp]["word"] != base]
RES["final"] = {}
for ft in FOOTS:
    R = RES["foot"][ft]; fin = {}
    for grp, key in (("above", "bites_above"), ("below", "bites_below")):
        w = R["main"][grp]["word"]; why = []
        if not (RES["KA1"]["pass_"] and R["KA2"]["pass_"] and R["KA3"]["pass_"]): w = "NO POWER"; why.append("known answer failed")
        if not all(TW[t]["foot"][ft][key] for t in TW): w = "NO POWER"; why.append("required twin did not bite")
        fl = flips(ft, grp)
        if fl: w += ", FRAGILE"
        # most-moving bracket
        if grp == "above" and R["main"]["above"]["n"]:
            mv = {B: abs(R["brackets"][B]["above"]["A_best"] - R["main"]["above"]["A_best"]) for B in BRK if R["brackets"][B]["above"]["n"]}
        elif grp == "below" and R["main"]["below"]["n"]:
            mv = {B: abs(R["brackets"][B]["below"]["delta"] - R["main"]["below"]["delta"]) for B in BRK if R["brackets"][B]["below"]["n"]}
        else: mv = {}
        top = max(mv, key=mv.get) if mv else None
        fin[grp] = dict(word=w, flips=fl, why=why, most_moving=top, move=mv.get(top) if top else None)
        P(f"[{ft}] FINAL {grp}: {w}; flipped by {fl or 'none'}; most-moving bracket {top} ({mv.get(top, float('nan')):.2f}){'; ' + '; '.join(why) if why else ''}")
    RES["final"][ft] = fin
RES["twins"] = {t: {ft: dict(bites_above=TW[t]["foot"][ft]["bites_above"], bites_below=TW[t]["foot"][ft]["bites_below"]) for ft in FOOTS} for t in TW}
P("DSC1R labels (canonical / alt): above " + " / ".join(RES["final"][f]["above"]["word"] for f in FOOTS) + "; below " + " / ".join(RES["final"][f]["below"]["word"] for f in FOOTS))

def clean(o):
    if isinstance(o, dict): return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(RES), open(os.path.join(HERE, "dsc1r.json"), "w"), indent=1)
open(os.path.join(HERE, "dsc1r.out"), "w").write("\n".join(OUT) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")
for t in TW:
    json.dump(clean(TW[t]), open(os.path.join(HERE, f"dsc1r_MUTATE_{t}.json"), "w"), indent=1)
    open(os.path.join(HERE, f"dsc1r_MUTATE_{t}.out"), "w").write("\n".join(l for l in OUT if f"twin {t}" in l) + "\nAdopts nothing. kappa = 1/2 FITTED; not theory closed.\n")

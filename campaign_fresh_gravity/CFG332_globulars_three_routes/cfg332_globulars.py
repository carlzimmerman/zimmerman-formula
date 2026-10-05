#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG332 -- the four outer-halo globulars (NGC 2419, Pal 3, Pal 4, Pal 14) under three routes, scored separately.
Route 1 ownership: (a) owned -> Newtonian; (b-EFE) law + host algebraic EFE (= h93); (b-B) isolated law, no EFE.
Route 2 MF-slope stellar M/L (Baumgardt slopes; branches S and K; never pooled), scored with the law (h93 EFE).
Route 3 full QUMOND EFE: exact monopole flux (primary) + axisymmetric grid Poisson solve (LOS anisotropy, checks).
kappa = 1/2 fixed, both footings, kernel hunt_lib.nu_s.  CFG332_MUTATE=1 reverses the measured (sigma, err, N).
See FROZEN_CRITERIA.md (committed first).  Run from the repo root or anywhere: paths are relative to this file."""
import os, sys, math, json
import numpy as np
from scipy.stats import chi2 as chi2dist, norm
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.interpolate import RegularGridInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
from hunt_lib import G, kpc, Msun, A0, nu_s  # noqa: E402

MUT = os.environ.get("CFG332_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg332_globulars{TAG}.out"), "w")
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.write(s + "\n")
CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok))); P(f"  [{'PASS' if ok else 'FAIL'}] {name}  ({detail})")

PC = 3.0857e16; MSUN_V = 4.83; UPS_V = 1.6; MW_MB = 6.0e10; WID = 0.15
EBV = {"NGC 2419": 0.08, "Pal 3": 0.04, "Pal 4": 0.01, "Pal 14": 0.04}
TARGETS = ["NGC 2419", "Pal 3", "Pal 4", "Pal 14"]
GCDIR = os.path.join(REPO, "real_research", "data", "globular_clusters")
COMB = os.path.join(REPO, "deepseek_push", "data2", "baumgardt_combined_table.txt")
PUBLISHED = {"Pal 14": (0.38, 0.12, 16), "Pal 4": (0.87, 0.18, 23)}

# ------------------------------------------------------------------ data (h93's loaders, re-implemented)
def rows(fn):
    out = {}
    for line in open(fn, encoding="utf-8"):
        if line.startswith("#") or line.startswith("ClusterName"): continue
        f = line.rstrip("\n").split("\t"); out.setdefault(f[0], []).append(f)
    return out
par, prof = rows(os.path.join(GCDIR, "baumgardt_gc_parameters.tsv")), rows(os.path.join(GCDIR, "baumgardt_gc_veldisp_profiles.tsv"))
mf = {}
for line in open(COMB):
    if line.startswith("#"): continue
    f = line.split()
    mf[f[0].replace("_", " ")] = dict(mlow=float(f[26]), mhigh=float(f[27]), alpha=float(f[28]), dalpha=float(f[29]))

GC = []
for name in TARGETS:
    f = par[name][0]
    D = float(f[3].split("+-")[0]); RGC = float(f[4].split("+-")[0]); V = float(f[8].split("+-")[0]); rhl = float(f[11])
    MV = V - 3.1*EBV[name] - 5*math.log10(D*1e3/10.0); LV = 10**(0.4*(MSUN_V - MV))
    pr = [p for p in prof[name] if p[6] == "RV"]
    R = np.array([float(p[1]) for p in pr])/206265.0*D*1e3; s = np.array([float(p[3]) for p in pr])
    e = 0.5*(np.array([float(p[4]) for p in pr]) + np.array([float(p[5]) for p in pr])); N = np.array([int(p[2]) for p in pr])
    if len(R) == 1: so, eso, No = s[0], e[0], int(N[0])
    else:
        ls = np.interp(math.log10(rhl), np.log10(R), np.log10(s)); le = np.interp(math.log10(rhl), np.log10(R), e/s)
        so, eso, No = 10**ls, 10**ls*le, int(N[int(np.argmin(np.abs(np.log10(R) - math.log10(rhl))))])
    GC.append(dict(name=name, RGC=RGC, LV=LV, rhl=rhl, so=float(so), eso=float(eso), N=No, **mf[name]))
if MUT:
    obs = [(g["so"], g["eso"], g["N"]) for g in GC][::-1]
    for g, o in zip(GC, obs): g["so"], g["eso"], g["N"] = o

# ------------------------------------------------------------------ estimators
def wolf_sigma(M_msun, rhl, boost=1.0):
    return np.sqrt(G*boost*np.asarray(M_msun)*Msun/(6.0*(4.0/3.0)*rhl*PC))/1e3
def g_ext(RGC): return G*MW_MB*Msun/(RGC*kpc)**2
def y_int(g, a0, ups): return G*(np.asarray(ups)*g["LV"]*Msun/2)/((4.0/3.0)*g["rhl"]*PC)**2/a0
def nu_arr(y):
    y = np.maximum(np.asarray(y, float), 1e-12); return 1.0/(-np.expm1(-np.sqrt(y)))

def pred_newton(g, a0, ups): return wolf_sigma(np.asarray(ups)*g["LV"], g["rhl"])
def pred_efe_alg(g, a0, ups): return wolf_sigma(np.asarray(ups)*g["LV"], g["rhl"], nu_arr(y_int(g, a0, ups) + g_ext(g["RGC"])/a0))
def pred_iso(g, a0, ups): return wolf_sigma(np.asarray(ups)*g["LV"], g["rhl"], nu_arr(y_int(g, a0, ups)))

MU, WMU = np.polynomial.legendre.leggauss(200)
def flux_avg(gi, ge, a0, kern=nu_arr):
    """exact QUMOND sphere average of the inward radial field: (1/2) int nu(|g_N|/a0) (g_i + g_e mu) dmu."""
    gi = np.asarray(gi, float)[..., None]
    gN = np.sqrt(np.maximum(gi**2 + ge**2 + 2*gi*ge*MU, 1e-300))
    return 0.5*np.sum(WMU*kern(gN/a0)*(gi + ge*MU), axis=-1)
def plummer_gi(g, ups, r):                     # SI, r in m; Plummer a = r_h,l
    a = g["rhl"]*PC; return G*np.asarray(ups)*g["LV"]*Msun*r/(r**2 + a**2)**1.5
def boost_num(g, a0, ups):
    r12 = (4.0/3.0)*g["rhl"]*PC; gi = plummer_gi(g, ups, r12)
    return flux_avg(gi, g_ext(g["RGC"]), a0)/gi
def pred_num(g, a0, ups): return wolf_sigma(np.asarray(ups)*g["LV"], g["rhl"], boost_num(g, a0, ups))

# ------------------------------------------------------------------ statistic
Z = np.random.default_rng(931).standard_normal(4000)
def pvals(so, sp_, N):
    c = chi2dist.cdf((N - 1)*(so/sp_)**2, N - 1); return c, 2*np.minimum(c, 1 - c)
def score(fn, a0, centers, widths, gcs=None, override=None):
    gcs = gcs or GC; pL, pT = [], []
    for g in gcs:
        so, eso, N = (override or {}).get(g["name"], (g["so"], g["eso"], g["N"]))
        ups = centers[g["name"]]*10**(widths[g["name"]]*Z)
        l, t = pvals(so, fn(g, a0, ups), N); pL.append(float(np.mean(l))); pT.append(float(np.mean(t)))
    comb = lambda ps: float(chi2dist.sf(-2*np.sum(np.log(np.clip(ps, 1e-300, 1))), 2*len(ps)))
    cL, cT = comb(pL), comb(pT)
    return dict(pL=pL, pT=pT, L=float(norm.isf(max(cL, 1e-300))), T=float(norm.isf(max(cT, 1e-300))))
SPS_C = {g["name"]: UPS_V for g in GC}; SPS_W = {g["name"]: WID for g in GC}
def full_score(fn, a0, C=SPS_C, W=SPS_W):
    base = score(fn, a0, C, W)
    base["noPal3_T"] = score(fn, a0, C, W, gcs=[g for g in GC if g["name"] != "Pal 3"])["T"]
    if not MUT: base["published_T"] = score(fn, a0, C, W, override=PUBLISHED)["T"]
    return base

R = {"mutate": MUT, "clusters": [{k: g[k] for k in ("name", "so", "eso", "N", "LV", "rhl", "RGC", "alpha", "dalpha", "mlow", "mhigh")} for g in GC]}
P("="*110); P(f"CFG332 outer-halo globulars, three routes{'   *** MUTATE: measured (sigma, err, N) reversed ***' if MUT else ''}"); P("="*110)
for g in GC: P(f"  {g['name']:9} sigma_obs {g['so']:.3f}+-{g['eso']:.3f} N={g['N']:3d}  L_V {g['LV']:.3e}  r_h,l {g['rhl']:.2f} pc  R_GC {g['RGC']:.1f}  MF slope {g['alpha']:+.2f}+-{g['dalpha']:.2f} [{g['mlow']:.2f},{g['mhigh']:.2f}]")

# ------------------------------------------------------------------ C1: h93 reproduction
P("\n--- C1  h93 reproduction (law + algebraic EFE, Upsilon ~ logN(1.6, 0.15 dex)) ---")
def joint(fn, a0, gcs):
    y = np.array([math.log(g["so"]/float(fn(g, a0, UPS_V))) for g in gcs])
    e = np.array([math.hypot(g["eso"]/g["so"], 1/math.sqrt(2*(g["N"] - 1))) for g in gcs]); w = 1/e**2
    m = float(np.sum(w*y)/np.sum(w)); return UPS_V*math.exp(2*m)
h93 = {}
for foot, a0 in A0.items():
    s = score(pred_efe_alg, a0, SPS_C, SPS_W)
    uF = [UPS_V*(g["so"]/float(pred_efe_alg(g, a0, UPS_V)))**2 for g in GC]
    h93[foot] = dict(L=s["L"], T=s["T"], uF=uF, jF=joint(pred_efe_alg, a0, GC), jN=joint(pred_newton, a0, GC))
    P(f"  {foot:9}: L {s['L']:.2f} sigma, T {s['T']:.2f} sigma; joint Ups framework {h93[foot]['jF']:.2f}, Newton {h93[foot]['jN']:.2f}; Ups_req(F) {np.round(uF, 2).tolist()}")
R["C1"] = h93
if not MUT:
    check("C1 h93 L statistic reproduced (4.6 / 4.9 sigma, +-0.1)", abs(h93["canonical"]["L"] - 4.6) <= 0.1 and abs(h93["alt"]["L"] - 4.9) <= 0.1,
          f"{h93['canonical']['L']:.2f} / {h93['alt']['L']:.2f}")
    check("C1 h93 joint Ups reproduced (0.76 framework canonical, 2.14 Newton, +-0.01)",
          abs(h93["canonical"]["jF"] - 0.76) <= 0.01 and abs(h93["canonical"]["jN"] - 2.14) <= 0.01, f"{h93['canonical']['jF']:.3f}, {h93['canonical']['jN']:.3f}")
    ref = {"canonical": [1.01, 1.34, 0.26, 0.35], "alt": [0.95, 1.23, 0.24, 0.32]}
    check("C1 h93 Ups_req(F) per cluster reproduced (+-0.01)", all(abs(a - b) <= 0.0051 + 1e-9 for f in ref for a, b in zip(h93[f]["uF"], ref[f])),
          f"{[round(x, 2) for x in h93['canonical']['uF']]} / {[round(x, 2) for x in h93['alt']['uF']]}")

# ------------------------------------------------------------------ Route 1
P("\n--- ROUTE 1  ownership ---")
P("  Record's rule (FG001, campaign_fresh_gravity/CFG7_hierarchy_fg001.py header; PAPER35 Sec. 'Hierarchical ownership'):")
P("   'E  formed embedded, without a cold component (tidal dwarfs, globular clusters, collision debris ..., wide binaries,")
P("    the Solar System): NEWTONIAN from their baryons.'   'A  accreted (formed top-level, later embedded: satellites, ...):")
P("    ... the ISOLATED law of their infall baryons, with NO external-field effect.'")
P("  -> the record DOES decide globulars: class E (Newtonian) by explicit enumeration; satellites (incl. UFDs) class A.")
R1 = {}
for foot, a0 in A0.items():
    R1[foot] = {"a_newton": full_score(pred_newton, a0), "b_EFE_h93": full_score(pred_efe_alg, a0), "b_B_isolated": full_score(pred_iso, a0)}
    for k, v in R1[foot].items():
        P(f"  {foot:9} {k:13}: T {v['T']:6.2f} sigma  L {v['L']:6.2f}  | no Pal 3 T {v['noPal3_T']:6.2f}" + (f" | published-alt T {v['published_T']:6.2f}" if 'published_T' in v else "")
          + "  per-cluster pT " + ", ".join(f"{x:.1e}" for x in v["pT"]))
    rat = [float(pred_newton(g, a0, UPS_V))/g["so"] for g in GC]
    R1[foot]["a_pred_over_obs"] = rat
    P(f"  {foot:9} (a) Newton predicted/observed at Ups 1.6: " + ", ".join(f"{g['name']} {r:.3f}" for g, r in zip(GC, rat)))
R["route1"] = R1
U = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "AUDIT_UFD_2026-10-03", "audit_ufd_results.json")))
efe_key = [k for k in U if k.startswith("var|EFE rival: MW")][0]
ufd = {"isolated_law": {f: (U[f"base|{f}"]["km"], U[f"base|{f}"]["z"]) for f in A0}, "EFE_rival": {f: (U[efe_key][f]["km"], U[efe_key][f]["z"]) for f in A0}}
R["ufd_matrix"] = ufd
P("\n  CONSISTENCY MATRIX (globulars T sigma | UFDs offset dex, z) -- canonical / alt")
for row, gk, uk, note in (("(a) rule as written: GC=E Newtonian, UFD=A isolated", "a_newton", "isolated_law", ""),
                          ("(b-B) GC top-level, B's own isolated law; UFD=A isolated", "b_B_isolated", "isolated_law", " [contradicts the written class E]"),
                          ("(b-EFE) rival: every system law + host EFE (h93)", "b_EFE_h93", "EFE_rival", " [not B's rule]")):
    P(f"   {row:58}: GC {R1['canonical'][gk]['T']:.2f} / {R1['alt'][gk]['T']:.2f}  | UFD {ufd[uk]['canonical'][0]:+.3f} ({ufd[uk]['canonical'][1]:.2f}) / {ufd[uk]['alt'][0]:+.3f} ({ufd[uk]['alt'][1]:.2f}){note}")
P("   (c) UFDs also owned/Newtonian would need a criterion not in the record (NEW POSTULATE) and is worse for them (not scored).")

# ------------------------------------------------------------------ Route 2
P("\n--- ROUTE 2  MF-slope stellar M/L (CONDITIONAL: slopes from Newtonian N-body fits to star counts) ---")
MLO, MTO, MBRK = 0.1, 0.80, 0.5
def dndm(m, alpha, branch):
    m = np.asarray(m, float)
    if branch == "kroupa": return np.where(m >= MBRK, m**-2.3, 2.0*m**-1.3)
    A = MTO**(-2.3 - alpha)
    if branch == "S": return A*m**alpha
    return np.where(m >= MBRK, A*m**alpha, 2.0*A*m**(alpha + 1))
mgrid = np.linspace(MLO, MTO, 20001); mi = np.linspace(MTO, 8.0, 20001)
def total_mass(alpha, branch):
    ms = np.trapz(mgrid*dndm(mgrid, alpha, branch), mgrid)
    mfin = 0.109*mi + 0.394; mref = np.minimum(mfin, MTO)
    dep = dndm(mref, alpha, branch)/dndm(mref, 0, "kroupa")
    return ms + np.trapz(mfin*mi**-2.3*dep, mi)
MK = total_mass(0, "kroupa")
def ups_mf(alpha, branch): return UPS_V*total_mass(alpha, branch)/MK
c5 = ups_mf(-2.3, "K")
if not MUT: check("C5 Kroupa input (alpha -2.3, branch K) returns Ups_MF = 1.6", abs(c5 - 1.6) < 1e-6, f"{c5:.9f}")
R2 = {"ups_mf": {}}
for br in ("S", "K"):
    C, W = {}, {}
    for g in GC:
        u0 = ups_mf(g["alpha"], br); up, um = ups_mf(g["alpha"] + g["dalpha"], br), ups_mf(g["alpha"] - g["dalpha"], br)
        da = abs(math.log10(up) - math.log10(um))/2; C[g["name"]], W[g["name"]] = u0, math.hypot(WID, da)
    R2["ups_mf"][br] = {n: (C[n], W[n]) for n in C}
    P(f"  branch {br}: Ups_MF " + ", ".join(f"{n} {C[n]:.2f} (width {W[n]:.3f} dex)" for n in C))
    for foot, a0 in A0.items():
        sF = full_score(pred_efe_alg, a0, C, W); sN = full_score(pred_newton, a0, C, W)
        R2[f"{br}|{foot}"] = {"law": sF, "newton": sN}
        P(f"   {foot:9} law(h93 EFE) T {sF['T']:6.2f}  L {sF['L']:6.2f}  no-Pal3 T {sF['noPal3_T']:6.2f} | Newton T {sN['T']:6.2f}")
R["route2"] = R2

# ------------------------------------------------------------------ Route 3
P("\n--- ROUTE 3  full QUMOND external field ---")
# C2/C3 on the flux method (dimensionless: G = M = a = 1)
def virial_flux(a0u, geu, kern=nu_arr, rmax=200.0, n=4000):
    r = np.geomspace(1e-4, rmax, n); gi = r/(r**2 + 1)**1.5; rho = 3/(4*np.pi)*(1 + r**2)**-2.5
    return float(np.trapz(rho*r*flux_avg(gi, geu, a0u, kern)*4*np.pi*r**2, r)/3.0)   # sigma_los^2 (orientation avg), M=1
deep = lambda y: 1/np.sqrt(np.maximum(y, 1e-300))
for a0u in (1.0, 100.0):
    s2 = virial_flux(a0u, 0.0, deep, rmax=1e4, n=20000); exact = math.sqrt(4/81*a0u)
    if not MUT: check(f"C2 flux method, deep-MOND isolated: sigma_los^4 = (4/81) G M a0 (a0u={a0u:g})", abs(s2/exact - 1) < 0.01, f"ratio {s2/exact:.5f}")
for ye in (0.01, 0.05):
    gi = 1e-4*ye; Bn = flux_avg(gi, ye, 1.0)/gi; L_ = (math.log(nu_s(ye*1.0001)) - math.log(nu_s(ye/1.0001)))/(2*math.log(1.0001))
    if not MUT: check(f"C3 EFE-dominated limit -> nu_e(1+L/3) (y_e={ye})", abs(Bn/(nu_s(ye)*(1 + L_/3)) - 1) < 0.01, f"{Bn:.5f} vs {nu_s(ye)*(1+L_/3):.5f}")
Bn = flux_avg(1e-3*100, 100.0, 1.0)/(1e-3*100)
if not MUT: check("C3 y_ext >> 1 -> Newton", abs(Bn - 1) < 0.01, f"boost {Bn:.6f}")

def grid_solve(a0u, geu, L=30.0, h=0.1, kern=nu_arr):
    nR, nz = int(round(L/h)), int(round(2*L/h))
    Rc = (np.arange(nR) + 0.5)*h; zc = -L + (np.arange(nz) + 0.5)*h
    def F(Rp, zp):                             # nu g_N - nu_e g_Ne ; g_N points inward + external along -z
        r2 = Rp**2 + zp**2; c = (r2 + 1)**-1.5
        gR, gz = -Rp*c, -zp*c - geu; gm = np.sqrt(gR**2 + gz**2); nn = kern(gm/a0u)
        return nn*gR, nn*gz + (kern(geu/a0u)*geu if geu > 0 else 0.0)
    Rf = np.arange(nR + 1)*h; zf = -L + np.arange(nz + 1)*h
    FRf, _ = F(Rf[:, None], zc[None, :]); _, Fzf = F(Rc[:, None], zf[None, :])
    S = (Rf[1:, None]*FRf[1:] - Rf[:-1, None]*FRf[:-1])/(Rc[:, None]*h) + (Fzf[:, 1:] - Fzf[:, :-1])/h
    def bphi(Rp, zp):                          # monopole Dirichlet value from the exact flux
        r = np.sqrt(Rp**2 + zp**2); gi = r/(r**2 + 1)**1.5; return -r*flux_avg(gi, geu, a0u, kern)
    idx = lambda i, j: i*nz + j
    I, J, V = [], [], []; b = -S.ravel().copy()
    for i in range(nR):
        wp, wm = Rf[i + 1]/(Rc[i]*h*h), Rf[i]/(Rc[i]*h*h)
        for j in range(nz):
            k = idx(i, j); diag = 0.0
            for (ii, jj, w) in ((i + 1, j, wp), (i - 1, j, wm), (i, j + 1, 1/h**2), (i, j - 1, 1/h**2)):
                if w == 0: continue
                diag -= w
                if 0 <= ii < nR and 0 <= jj < nz: I.append(k); J.append(idx(ii, jj)); V.append(w)
                else:
                    Rb = Rc[i] + (h if ii >= nR else 0.0); zb = zc[j] + (h if jj >= nz else (-h if jj < 0 else 0.0))
                    b[k] -= w*float(bphi(np.array(Rb), np.array(zb)))
            I.append(k); J.append(k); V.append(diag)
    A = sp.csr_matrix((V, (I, J)), shape=(nR*nz, nR*nz))
    phi = spla.spsolve(A, b).reshape(nR, nz)
    gR = -np.gradient(phi, h, axis=0); gz = -np.gradient(phi, h, axis=1)
    rho = 3/(4*np.pi)*(1 + Rc[:, None]**2 + zc[None, :]**2)**-2.5; dV = 2*np.pi*Rc[:, None]*h*h
    M = np.sum(rho*dV); Wzz = np.sum(rho*zc[None, :]*gz*dV); Wxx = 0.5*np.sum(rho*Rc[:, None]*gR*dV)
    iR, iz = RegularGridInterpolator((Rc, zc), gR, bounds_error=False, fill_value=None), RegularGridInterpolator((Rc, zc), gz, bounds_error=False, fill_value=None)
    r12 = 4/3; mu = MU; th = np.arccos(mu); pts = np.c_[r12*np.sin(th), r12*mu]
    grad = 0.5*np.sum(WMU*(iR(pts)*np.sin(th) + iz(pts)*mu))           # outward radial mean (negative = inward)
    return dict(s2_z=float(Wzz/M), s2_x=float(Wxx/M), s2_avg=float((2*Wxx + Wzz)/(3*M)), gr12=float(-grad), M=float(M))

if not MUT:
    gd = grid_solve(1.0, 0.0, kern=deep); ex = math.sqrt(4/81*1.0)
    check("C2 grid solve, deep-MOND isolated: orientation-averaged sigma_los^4 = (4/81) G M a0 (1%)", abs(-gd["s2_avg"]/ex - 1) < 0.01, f"ratio {-gd['s2_avg']/ex:.4f}")
R3 = {}
for foot, a0 in A0.items():
    R3[foot] = {}
    for g in GC:
        a = g["rhl"]*PC; Mm = UPS_V*g["LV"]*Msun; gu = G*Mm/a**2
        a0u, geu = a0/gu, g_ext(g["RGC"])/gu
        Bn = float(boost_num(g, a0, UPS_V)); Ba = float(nu_s(float(y_int(g, a0, UPS_V)) + g_ext(g["RGC"])/a0))
        r12 = (4/3); giu = r12/(r12**2 + 1)**1.5; Ba_pl = nu_s(giu/a0u + geu/a0u)
        d = dict(B_num=Bn, B_alg_h93=Ba, B_alg_plummer=float(Ba_pl), B_iso=float(nu_s(float(y_int(g, a0, UPS_V)))),
                 ratio_sigma=math.sqrt(Bn/Ba), ratio_sigma_plummer=math.sqrt(Bn/Ba_pl))
        if foot == "canonical" or g["name"] != "NGC 2419":
            gs = grid_solve(a0u, geu)
            s2N = virial_flux(1e30, 0.0, kern=lambda y: np.ones_like(y))
            d.update(grid_gr12=gs["gr12"], flux_gr12=float(flux_avg(giu, geu, a0u)), los_par_over_avg=math.sqrt(gs["s2_z"]/gs["s2_avg"]),
                     los_perp_over_avg=math.sqrt(gs["s2_x"]/gs["s2_avg"]), virial_boost_grid=-gs["s2_avg"]/s2N,
                     virial_boost_flux=virial_flux(a0u, geu)/s2N)
            if foot == "canonical" and g["name"] == "Pal 14" and not MUT:
                g2 = grid_solve(a0u, geu, L=60.0)
                d["domain_double_los_change"] = max(abs(math.sqrt(g2["s2_z"]/gs["s2_z"]) - 1), abs(math.sqrt(g2["s2_x"]/gs["s2_x"]) - 1))
        R3[foot][g["name"]] = d
        P(f"  {foot:9} {g['name']:9} boost: num {Bn:.3f} | alg(h93) {Ba:.3f} | iso {d['B_iso']:.3f}  sigma_num/sigma_alg {d['ratio_sigma']:.3f} (same-Plummer {d['ratio_sigma_plummer']:.3f})"
          + (f"  LOS par/perp vs avg {d['los_par_over_avg']:.3f}/{d['los_perp_over_avg']:.3f}; grid g_r(r12) {d['grid_gr12']:.4f} vs flux {d['flux_gr12']:.4f}" if "grid_gr12" in d else ""))
    s = full_score(pred_num, a0); R3[foot]["score"] = s
    P(f"  {foot:9} RESCORED (exact QUMOND monopole): T {s['T']:6.2f}  L {s['L']:6.2f}  no-Pal3 T {s['noPal3_T']:6.2f}" + (f"  published-alt T {s['published_T']:6.2f}" if "published_T" in s else ""))
if not MUT:
    dev = max(abs(R3[f][n]["grid_gr12"]/R3[f][n]["flux_gr12"] - 1) for f in A0 for n in R3[f] if n != "score" and "grid_gr12" in R3[f][n])
    check("C4 grid sphere-averaged g_r(r12) matches the exact flux (2%)", dev < 0.02, f"max dev {dev:.4f}")
    dd = R3["canonical"]["Pal 14"]["domain_double_los_change"]
    check("C4 domain doubling moves LOS sigma by < 2% (Pal 14)", dd < 0.02, f"{dd:.4f}")
R["route3"] = R3

# ------------------------------------------------------------------ verdicts
def verdict(Tc, Ta, base_c, base_a):
    if Tc < 2 and Ta < 2: return "MATCH"
    if Tc < 2 or Ta < 2 or (Tc <= base_c/2 and Ta <= base_a/2): return "PARTIAL"
    return "NOT"
bc, ba = R1["canonical"]["b_EFE_h93"]["T"], R1["alt"]["b_EFE_h93"]["T"]
V = {"route1_a_owned": [R1["canonical"]["a_newton"]["T"], R1["alt"]["a_newton"]["T"]],
     "route1_b_EFE_h93": [bc, ba], "route1_b_B_isolated": [R1["canonical"]["b_B_isolated"]["T"], R1["alt"]["b_B_isolated"]["T"]],
     "route2_S": [R2["S|canonical"]["law"]["T"], R2["S|alt"]["law"]["T"]], "route2_K": [R2["K|canonical"]["law"]["T"], R2["K|alt"]["law"]["T"]],
     "route3_qumond": [R3["canonical"]["score"]["T"], R3["alt"]["score"]["T"]]}
R["verdicts"] = {k: dict(T_canonical=v[0], T_alt=v[1], verdict=verdict(v[0], v[1], bc, ba)) for k, v in V.items()}
P("\n--- VERDICTS (T, two-sided marginalised Fisher; canonical / alt) ---")
for k, v in R["verdicts"].items(): P(f"  {k:22}: {v['T_canonical']:6.2f} / {v['T_alt']:6.2f}  -> {v['verdict']}")
if MUT:
    base = json.load(open(os.path.join(HERE, "cfg332_globulars_results.json")))["verdicts"]
    for k, v in R["verdicts"].items():
        check(f"MUTATE degrades {k} (T rises, both footings)", v["T_canonical"] > base[k]["T_canonical"] and v["T_alt"] > base[k]["T_alt"],
              f"{base[k]['T_canonical']:.2f}->{v['T_canonical']:.2f} / {base[k]['T_alt']:.2f}->{v['T_alt']:.2f}")
R["checks"] = CHECKS
npass = sum(ok for _, ok in CHECKS)
P(f"\n{npass}/{len(CHECKS)} checks pass")
json.dump(R, open(os.path.join(HERE, f"cfg332_globulars{TAG}_results.json"), "w"), indent=1, default=float)
OUT.close()

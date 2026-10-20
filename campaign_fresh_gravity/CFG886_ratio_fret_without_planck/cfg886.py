"""CFG886 -- rebuild Omega_c/Omega_b = 5.364 and the census f_ret without the Planck LCDM fit.
Criteria: FROZEN_CRITERIA.md (07170a203, committed alone before this script).
Run from anywhere:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg886.py        (CFG886_MUTATE=dh10: D/H x 1.10; run after the main run)
Writes cfg886[_MUTATE_dh10].out and cfg886_results[_MUTATE_dh10].json next to itself.  Nothing is written anywhere else.
kappa = 1/2 FITTED; cold energy mass required; not theory closed.  Early-universe assumptions E1-E6 are labelled in the criteria."""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, ast, io, contextlib, time
import numpy as np
from scipy.optimize import brentq, minimize
from scipy.interpolate import RectBivariateSpline
import camb
from camb import bbn as cbbn

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG886_MUTATE", ""); assert MUT in ("", "dh10"), "CFG886_MUTATE must be '' or 'dh10'"
SUF = "_MUTATE_dh10" if MUT else ""
OUTL = []
def P(s=""):
    print(s, flush=True); OUTL.append(str(s))
def banner(t):
    P("\n" + "=" * 110 + "\n" + t + "\n" + "=" * 110)
CHK = {}
def check(name, ok, measured, load=True):
    CHK[name.split()[0]] = dict(ok=bool(ok), measured=str(measured), load_bearing=load, name=name)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load else ' (reported)'} {name}\n         measured: {measured}")
    return ok
RES = dict(lane="CFG886", criteria="07170a203", mutate=MUT or None, camb=camb.__version__)

C_KMS = 299792.458; WGAM = 2.4728e-5; TCMB = 2.7255; NEFF = 3.044; MNU = 0.06
RATIO_PLANCK = 0.1200 / 0.02237; H_REC, WB_REC, WC_REC = 0.674, 0.02237, 0.1200       # record constants (CFG416/515; Planck pair)
DH_F = 1.10 if MUT else 1.00
DH_PDG = (2.547e-5, 0.029e-5); DH_COOKE = (2.527e-5, 0.030e-5)                         # as cited in XR26_bbn.py / CFG254
H0_SH0ES = (73.04, 1.04); H0_REPORTED = {"TDCOSMO 2025": (71.6, 3.6), "standard sirens": (68.0, 4.1)}
OM_CFG682 = (0.3085, 0.0075)
P("CFG886  rebuild Omega_c/Omega_b = 5.364 and census f_ret without the Planck LCDM fit" + ("   [MUTATE dh10: D/H x 1.10]" if MUT else ""))
P(f"  CAMB {camb.__version__}; N_eff {NEFF}; T_CMB {TCMB} K; Sigma m_nu {MNU} eV (one massive; variant 0); a0 enters none of T1-T4")

# ============================================================================================ T1  omega_b from D/H
banner("T1  omega_b FROM D/H (standard BBN, assumption E1-E2)")
TABS = {"PRIMAT 2024": cbbn.BBN_table_interpolator("PRIMAT_Yp_DH_ErrorMC_2024.dat", function_of=("Ombh2", "DeltaN")),
        "PArthENoPE 2017": cbbn.BBN_table_interpolator("PArthENoPE_880.2_standard.dat"),
        "PArthENoPE Marcucci": cbbn.BBN_table_interpolator("PArthENoPE_880.2_marcucci.dat")}
PRI = TABS["PRIMAT 2024"]
def dh(tab, w): return float(tab.DH(w, 0.0))
def invert(tab, D):
    return brentq(lambda w: dh(tab, w) - D, 0.015, 0.030, xtol=1e-14, rtol=1e-14)
def slope(tab, w, e=1e-6): return (dh(tab, w + e) - dh(tab, w - e)) / (2 * e)
def bbn_set(D, sD):
    out = {}
    for nm, tab in TABS.items():
        w = invert(tab, D); s = slope(tab, w)
        rel_th = float(PRI.get("sig(D/H)", w, 0.0)) / dh(PRI, w)                     # PRIMAT's relative theory error (both codes)
        so = sD / abs(s); sth = rel_th * dh(tab, w) / abs(s)
        out[nm] = dict(omega_b=w, sig_obs=so, sig_th=sth, sigma=math.hypot(so, sth), dlnDH_dlnwb=s * w / dh(tab, w), roundtrip=dh(tab, w) / D - 1)
    a, b = out["PRIMAT 2024"], out["PArthENoPE 2017"]
    mid = 0.5 * (a["omega_b"] + b["omega_b"]); half = 0.5 * abs(a["omega_b"] - b["omega_b"])
    so = 0.5 * (a["sig_obs"] + b["sig_obs"]); sth = a["sig_th"]
    out["PRIMARY (midpoint)"] = dict(omega_b=mid, sig_obs=so, sig_th=sth, sig_codes=half, sigma=math.sqrt(so ** 2 + sth ** 2 + half ** 2))
    return out
BBN = {"PDG 2024": bbn_set(DH_PDG[0] * DH_F, DH_PDG[1] * DH_F), "Cooke+18": bbn_set(DH_COOKE[0] * DH_F, DH_COOKE[1] * DH_F)}
for dset, bs in BBN.items():
    P(f"  D/H {dset}: ({(DH_PDG if dset.startswith('PDG') else DH_COOKE)[0] * DH_F * 1e5:.4f} +- {(DH_PDG if dset.startswith('PDG') else DH_COOKE)[1] * DH_F * 1e5:.4f}) e-5")
    for nm, b in bs.items():
        extra = f"  (obs {b['sig_obs']:.5f}, theory {b['sig_th']:.5f}" + (f", codes 1/2-offset {b['sig_codes']:.5f})" if "sig_codes" in b else f"; dlnDH/dlnwb {b['dlnDH_dlnwb']:.3f})")
        P(f"    {nm:22s} omega_b = {b['omega_b']:.6f} +- {b['sigma']:.6f}{extra}")
WB = BBN["PDG 2024"]["PRIMARY (midpoint)"]; RES["T1"] = BBN
P(f"  -> PRIMARY omega_b = {WB['omega_b']:.6f} +- {WB['sigma']:.6f}  (PRIMAT-PArthENoPE offset {2 * WB['sig_codes']:.6f} = {200 * WB['sig_codes'] / WB['omega_b']:.2f}%)")

# ============================================================================================ CAMB r_d
banner("r_d FROM CAMB (assumptions E2-E4: cold energy as pressureless matter before recombination; standard recombination)")
def camb_pars(wb, wc, mnu=MNU, nnu=NEFF, H0=68.0, bbn=None):
    bbn = PRI if bbn is None else bbn                                   # interpolator objects (PRIMAT 2024 needs function_of Ombh2)
    p = camb.CAMBparams()
    p.set_cosmology(H0=H0, ombh2=wb, omch2=wc, mnu=mnu, num_massive_neutrinos=(1 if mnu > 0 else 0), nnu=nnu, TCMB=TCMB, omk=0.0,
                    bbn_predictor=bbn)
    return p
def camb_rd(wb, wc, **kw):
    p = camb_pars(wb, wc, **kw); r = camb.get_background(p)
    return float(r.get_derived_params()["rdrag"]), float(p.omnuh2), r
WNU = camb_pars(0.0224, 0.12).omnuh2
P(f"  omega_nu (Sigma m_nu {MNU} eV, CAMB omnuh2) = {WNU:.6e}")
def rd_spline(mnu, wbg, wcg):
    t = time.time(); L = np.empty((len(wbg), len(wcg)))
    for i, wb in enumerate(wbg):
        for j, wc in enumerate(wcg):
            L[i, j] = math.log(camb_rd(wb, wc, mnu=mnu)[0])
    P(f"  r_d spline (mnu {mnu}): {len(wbg)} x {len(wcg)} CAMB calls in {time.time() - t:.1f} s; omega_b [{wbg[0]}, {wbg[-1]}], omega_c [{wcg[0]:.3f}, {wcg[-1]:.3f}]")
    sp = RectBivariateSpline(np.log(wbg), np.log(wcg), L, kx=3, ky=3)
    return dict(sp=sp, lwb=(math.log(wbg[0]), math.log(wbg[-1])), lwc=(math.log(wcg[0]), math.log(wcg[-1])))
SPL = {MNU: rd_spline(MNU, np.linspace(0.0180, 0.0255, 10), np.geomspace(0.040, 0.27, 26)),
       0.0: rd_spline(0.0, np.linspace(0.0180, 0.0255, 7), np.geomspace(0.040, 0.27, 18))}
def rd_of(spl, wb, wc):
    lwb, lwc = np.log(np.asarray(wb, float)), np.log(np.maximum(np.asarray(wc, float), 1e-9))
    ok = (lwb >= spl["lwb"][0]) & (lwb <= spl["lwb"][1]) & (lwc >= spl["lwc"][0]) & (lwc <= spl["lwc"][1])
    v = np.exp(spl["sp"].ev(np.clip(lwb, *spl["lwb"]), np.clip(lwc, *spl["lwc"])))
    return np.where(ok, v, np.nan)

# ============================================================================================ K1
banner("K1  CONTROLS: 5.364 and the record's r_d")
def R_of(wm, wb, wnu): return (np.asarray(wm) - wnu) / np.asarray(wb) - 1.0
k1r = float(R_of(0.02237 + 0.1200 + WNU, 0.02237, WNU))
check("K1i the lane's R function at Planck's omega_b 0.02237, omega_c 0.1200 returns 5.364 to <= 1e-3", abs(k1r - 5.364) <= 1e-3, f"R = {k1r:.6f}")
rdP = camb_rd(0.02237, 0.1200, H0=67.36)[0]
check("K1ii CAMB rdrag at (0.02237, 0.1200; m_nu 0.06, N_eff 3.044, h 0.6736) within 0.1% of the record's 147.05 Mpc (CFG254/XR26)",
      abs(rdP / 147.05 - 1) <= 1e-3, f"r_d = {rdP:.4f} Mpc ({100 * (rdP / 147.05 - 1):+.4f}%)")
rdX = camb_rd(0.022383, 0.12011, nnu=3.046, H0=67.32, bbn=TABS["PArthENoPE 2017"])[0]
check("K1ii' (reported) XR26's exact settings (0.022383, 0.12011, N_eff 3.046, PArthENoPE, H0 67.32) give 147.049 within 0.01%",
      abs(rdX / 147.049 - 1) <= 1e-4, f"r_d = {rdX:.4f} Mpc ({100 * (rdX / 147.049 - 1):+.5f}%)", load=False)
RES["K1"] = dict(R_planck=k1r, rd_planck_pair=rdP, rd_xr26=rdX, omega_nu=WNU)

# ============================================================================================ K3  BBN controls (unscaled D/H always)
banner("K3  BBN CONTROLS (unscaled observed D/H; independent of the MUTATE)")
rt = max(abs(bbn_set(*DH_PDG)[nm]["roundtrip"]) for nm in TABS)
check("K3a BBN round trip DH(omega_b,inv) = D/H_obs to 1e-8 (all three tables)", rt <= 1e-8, f"max |rel| = {rt:.2e}")
wC = invert(PRI, DH_COOKE[0])
dl = (math.log(dh(PRI, wC * 1.001)) - math.log(dh(PRI, wC / 1.001))) / (2 * math.log(1.001))
sC = wC * math.hypot(DH_COOKE[1] / DH_COOKE[0], float(PRI.get("sig(D/H)", wC, 0.0)) / DH_COOKE[0]) / abs(dl)
check("K3b Cooke+18 with PRIMAT 2024 reproduces CFG654's omega_b 0.021932 (sigma 0.00022) within 1e-5 (CFG654's own sigma formula)",
      abs(wC - 0.021932) <= 1e-5 and abs(sC - 0.00022) <= 1e-5, f"omega_b = {wC:.6f}, sigma = {sC:.6f}")
dP = dh(TABS["PArthENoPE 2017"], 0.02236)
check("K3c PArthENoPE at omega_b 0.02236 gives D/H within 1.5% of Planck 2018's quoted 2.587e-5 (XR26 K1)", abs(dP / 2.587e-5 - 1) <= 0.015, f"D/H = {dP:.4e}")

# ============================================================================================ BAO data (parsed from CFG681)
SRC681 = os.path.join(LANES, "CFG681_bao_raw_geometry", "cfg681_bao.py")
_t = ast.parse(open(SRC681).read()); _lit = {}
for nd in _t.body:
    if isinstance(nd, ast.Assign) and len(nd.targets) == 1 and isinstance(nd.targets[0], ast.Name) and nd.targets[0].id in ("ANISO", "BGS"):
        _lit[nd.targets[0].id] = ast.literal_eval(nd.value)
ANISO, BGS = _lit["ANISO"], _lit["BGS"]; assert len(ANISO) == 6 and len(BGS) == 3
ZA = np.array([a[1] for a in ANISO]); DM = np.array([a[2] for a in ANISO]); SDM = np.array([a[3] for a in ANISO])
DHd = np.array([a[4] for a in ANISO]); SDH = np.array([a[5] for a in ANISO]); RR = np.array([a[6] for a in ANISO])
CI = []
for k in range(6):
    C = np.array([[SDM[k] ** 2, RR[k] * SDM[k] * SDH[k]], [RR[k] * SDM[k] * SDH[k], SDH[k] ** 2]]); CI.append(np.linalg.inv(C))
CI = np.array(CI)
RES["BAO_data"] = dict(ANISO=ANISO, BGS=BGS, source="CFG681_bao_raw_geometry/cfg681_bao.py (DESI DR2, arXiv 2503.14738v2 Table)")

# ---- background on a z grid that hits every data redshift exactly
DZ = 0.0005; ZG = np.arange(0.0, 2.3305, DZ)
ZD = np.r_[BGS[0], ZA]; IDX = np.array([int(round(z / DZ)) for z in ZD]); assert np.allclose(ZG[IDX], ZD, atol=1e-9)
def IE(om, h, nrel):
    """om scalar, h array -> I(z_k) = int dz/E and E(z_k) at the 7 data redshifts, shape (len(h), 7)."""
    h = np.atleast_1d(h); Or = WGAM * (1 + 0.2271 * nrel) / h ** 2
    zp = 1.0 + ZG
    E = np.sqrt(om * zp ** 3 + Or[:, None] * zp ** 4 + (1.0 - om - Or)[:, None])
    f = 1.0 / E; I = np.concatenate([np.zeros((len(h), 1)), np.cumsum(0.5 * (f[:, 1:] + f[:, :-1]) * DZ, axis=1)], axis=1)
    return I[:, IDX], E[:, IDX]
def chi2_bao(I, E, hrd):
    """I, E (n, 7); hrd (n, m) = h r_d [Mpc] -> chi2 (n, m)."""
    fac = (C_KMS / 100.0) / hrd
    dmr = fac[..., None] * I[:, None, 1:]; dhr = fac[..., None] / E[:, None, 1:]
    d1 = DM - dmr; d2 = DHd - dhr
    c = (CI[:, 0, 0] * d1 * d1 + 2 * CI[:, 0, 1] * d1 * d2 + CI[:, 1, 1] * d2 * d2).sum(-1)
    dmb = fac * I[:, None, 0]; dhb = fac / E[:, None, 0]; dv = (BGS[0] * dmb ** 2 * dhb) ** (1 / 3)
    return c + ((BGS[1] - dv) / BGS[2]) ** 2

# ============================================================================================ weighted statistics
def wstats(v, w):
    v = np.asarray(v, float).ravel(); w = np.asarray(w, float).ravel(); ok = np.isfinite(v) & (w > 0); v, w = v[ok], w[ok]
    w = w / w.sum(); m = float((w * v).sum()); sd = float(math.sqrt(max((w * (v - m) ** 2).sum(), 0)))
    o = np.argsort(v); cw = np.cumsum(w[o]); q = lambda p: float(v[o][min(np.searchsorted(cw, p), len(v) - 1)])
    return dict(mean=m, sd=sd, p2_5=q(0.025), p16=q(0.16), p50=q(0.5), p84=q(0.84), p97_5=q(0.975))
def rclass(z):
    a = abs(z)
    return "5.364 RECOVERED" if a <= 1 else ("CONSISTENT" if a <= 2 else ("TENSION" if a <= 3 else "NOT RECOVERED"))

# ============================================================================================ T2a  BAO + BBN grid posterior
OMG = np.round(np.arange(0.20, 0.42 + 1e-9, 0.001), 4); HG = np.round(np.arange(0.60, 0.78 + 1e-9, 0.0005), 5)
GHX, GHW = np.polynomial.hermite.hermgauss(9)
def grid_a(wb_mu, wb_sig, mnu=MNU, label=""):
    spl = SPL[mnu]; wnu = WNU if mnu > 0 else 0.0; nrel = NEFF * (2 / 3 if mnu > 0 else 1.0)
    WBn = wb_mu + math.sqrt(2) * wb_sig * GHX; lw = np.log(GHW / math.sqrt(math.pi))
    chi = np.empty((len(OMG), len(HG), len(WBn)))
    for i, om in enumerate(OMG):
        I, E = IE(om, HG, nrel); wm = om * HG ** 2
        for b, wbv in enumerate(WBn):
            rd = rd_of(spl, np.full_like(HG, wbv), wm - wbv - wnu)
            c = chi2_bao(I, E, (HG * rd)[:, None])[:, 0]
            chi[i, :, b] = np.where(np.isfinite(c), c, 1e12)
    return dict(chi=chi, WBn=WBn, lw=lw, wnu=wnu, spl=spl, label=label, mnu=mnu)
def post_a(g, om_prior=None):
    lp = g["lw"][None, None, :] - 0.5 * (g["chi"] - g["chi"].min())
    if om_prior is not None:
        lp = lp - 0.5 * ((OMG[:, None, None] - om_prior[0]) / om_prior[1]) ** 2
    W = np.exp(lp - lp.max()); W /= W.sum()
    OM3 = OMG[:, None, None] * np.ones_like(W); H3 = HG[None, :, None] * np.ones_like(W); WB3 = g["WBn"][None, None, :] * np.ones_like(W)
    WM = OM3 * H3 ** 2; WC = WM - WB3 - g["wnu"]; R = WC / WB3
    RD = rd_of(g["spl"], WB3, WC)
    st = dict(Om=wstats(OM3, W), h=wstats(H3, W), omega_b=wstats(WB3, W), omega_m=wstats(WM, W), omega_c=wstats(WC, W), R=wstats(R, W),
              R_literal=wstats(WM / WB3 - 1, W), f_b=wstats(WB3 / WM, W), f_b_fw=wstats(1 / (1 + R), W), r_d=wstats(RD, W), h_rd=wstats(H3 * RD, W))
    i, j, b = np.unravel_index(np.argmin(g["chi"]), g["chi"].shape)
    st["chi2_min"] = float(g["chi"].min()); st["best"] = dict(Om=float(OMG[i]), h=float(HG[j]), omega_b=float(g["WBn"][b]))
    edge = np.zeros_like(W, bool); edge[:3] = edge[-3:] = True; edge[:, :3] = edge[:, -3:] = True
    st["edge_mass"] = float(W[edge].sum()); st["steps_sd"] = dict(Om=st["Om"]["sd"] / 0.001, h=st["h"]["sd"] / 0.0005)
    z = (st["R"]["mean"] - RATIO_PLANCK) / st["R"]["sd"]; st["z_vs_5364"] = z; st["class"] = rclass(z)
    st["not_informative"] = st["R"]["sd"] / st["R"]["mean"] > 0.10
    return st
def show(tag, st):
    r = st["R"]
    P(f"  {tag:58s} h {st['h']['mean']:.4f}+-{st['h']['sd']:.4f}  Om {st['Om']['mean']:.4f}+-{st['Om']['sd']:.4f}  omega_m {st['omega_m']['mean']:.4f}"
      f"  R = {r['mean']:.3f} +- {r['sd']:.3f} [68% {r['p16']:.3f}-{r['p84']:.3f}; 95% {r['p2_5']:.3f}-{r['p97_5']:.3f}]  z {st['z_vs_5364']:+.2f} -> {st['class']}"
      + ("  NOT INFORMATIVE" if st.get("not_informative") else ""))

banner("T2(a)  H0 FROM DESI DR2 BAO + BBN, flat a0 at all z (X = 1); grid posterior")
t = time.time(); GA = grid_a(WB["omega_b"], WB["sigma"], label="primary"); A = post_a(GA)
P(f"  grid {len(OMG)} x {len(HG)} x 9 in {time.time() - t:.1f} s; chi2_min {A['chi2_min']:.3f} (7 tracers, 13 numbers; 3 parameters) at {A['best']}")
show("(a) PRIMARY BAO+BBN, X=1, PDG D/H midpoint", A)
P(f"      omega_b {A['omega_b']['mean']:.5f}+-{A['omega_b']['sd']:.5f}; omega_c {A['omega_c']['mean']:.4f}+-{A['omega_c']['sd']:.4f}; r_d {A['r_d']['mean']:.2f}+-{A['r_d']['sd']:.2f} Mpc;"
  f" h r_d {A['h_rd']['mean']:.2f}+-{A['h_rd']['sd']:.2f} Mpc; f_b {A['f_b']['mean']:.4f}+-{A['f_b']['sd']:.4f}; f_b,fw = 1/(1+R) {A['f_b_fw']['mean']:.4f}+-{A['f_b_fw']['sd']:.4f};"
  f" R literal (nu kept) {A['R_literal']['mean']:.3f}")
VAR = {}
VAR["V1 + CFG682 conditional Om 0.3085+-0.0075 (double-uses BAO)"] = post_a(GA, om_prior=OM_CFG682)
bC = BBN["Cooke+18"]["PRIMARY (midpoint)"]; VAR["V2 Cooke+18 D/H (midpoint)"] = post_a(grid_a(bC["omega_b"], bC["sigma"]))
for nm in ("PRIMAT 2024", "PArthENoPE 2017"):
    b = BBN["PDG 2024"][nm]; VAR[f"V3 {nm} alone"] = post_a(grid_a(b["omega_b"], b["sigma"]))
VAR["V4 Sigma m_nu = 0 (R = omega_m/omega_b - 1 literally)"] = post_a(grid_a(WB["omega_b"], WB["sigma"], mnu=0.0))
for k, v in VAR.items():
    show(k, v)
RES["T2a"] = dict(primary=A, variants=VAR)

# ---- K2: BAO identity (CFG681/682 conventions, verbatim functions), background vs CAMB, spline
banner("K2  CONTROLS: BAO identity with CFG681/682, analytic background vs CAMB, r_d spline")
NODES = np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33]); h681 = 0.68; OMR681 = 2.469e-5 / h681 ** 2 * (1 + 0.2271 * 3.046)     # cfg681_bao.py verbatim
zg681 = np.linspace(0, 2.5, 5001)
def Efun(om, xn, z):
    X = np.interp(z, NODES, np.r_[1.0, xn]); E2 = om*(1+z)**3 + OMR681*(1+z)**4 + (1 - om - OMR681)*X
    return np.sqrt(np.where(E2 > 1e-6, E2, np.nan))
def Igrid(om, xn):
    E = Efun(om, xn, zg681); f = 1/E; I = np.r_[0, np.cumsum(0.5*(f[1:]+f[:-1])*np.diff(zg681))]; return I
def bao_chi2_681(om, xn):
    I = Igrid(om, xn)
    if not np.all(np.isfinite(I)): return 1e9, None
    ms, ds, Cis = [], [], []
    for (nm, z, dm, sdm, dh_, sdh, r) in ANISO:
        m = np.array([np.interp(z, zg681, I), 1/Efun(om, xn, np.array([z]))[0]]); C = np.array([[sdm**2, r*sdm*sdh], [r*sdm*sdh, sdh**2]])
        ms.append(m); ds.append(np.array([dm, dh_])); Cis.append(np.linalg.inv(C))
    z, dv, sdv = BGS; Iz = np.interp(z, zg681, I); mv = (z*Iz**2/Efun(om, xn, np.array([z]))[0])**(1/3)
    num = sum(m@Ci@d for m, d, Ci in zip(ms, ds, Cis)) + mv*dv/sdv**2; den = sum(m@Ci@m for m, Ci in zip(ms, Cis)) + mv*mv/sdv**2
    q = num/den
    chi = sum((d-q*m)@Ci@(d-q*m) for m, d, Ci in zip(ms, ds, Cis)) + ((dv - q*mv)/sdv)**2
    return chi, q
R681 = json.load(open(os.path.join(LANES, "CFG681_bao_raw_geometry", "cfg681_results.json")))
r1 = minimize(lambda p: bao_chi2_681(p[0], np.ones(5))[0] if 0.15 <= p[0] <= 0.45 else 1e9, [0.30], method="Nelder-Mead", options=dict(xatol=1e-6, fatol=1e-6))
ok_a1 = abs(r1.fun - R681["T1_BAO"]["chi2_const"]) <= 1e-3 and abs(r1.x[0] - R681["T1_BAO"]["om_const"]) <= 2e-4
R682 = json.load(open(os.path.join(LANES, "CFG682_a0z_bao_omegam", "cfg682_results.json")))
dmax = max(abs(bao_chi2_681(r["om"], np.array(r["nodes"]))[0] - r["chi2"]) for r in R682["BAO"]["rows"])
check("K2a BAO identity: CFG681 X=1 minimum (chi2 10.5515, Om 0.29703) to 1e-3 / 2e-4 AND CFG682's 49 BAO-only fixed-Om chi2 at their nodes to 1e-6",
      ok_a1 and dmax <= 1e-6, f"chi2 {r1.fun:.5f} at Om {r1.x[0]:.5f} (record {R681['T1_BAO']['chi2_const']:.5f}, {R681['T1_BAO']['om_const']:.5f}); max |dchi2| at CFG682 nodes {dmax:.2e}")
hb, omb, wbb = A["h"]["mean"], A["Om"]["mean"], A["omega_b"]["mean"]; wcb = omb * hb ** 2 - wbb - WNU
rdc, _, rc = camb_rd(wbb, wcb, H0=100 * hb)
I, E = IE(omb, np.array([hb]), NEFF * 2 / 3); rds = float(rd_of(SPL[MNU], wbb, wcb))
fa = C_KMS / (100 * hb * rds)
dm_an = fa * I[0, :]; dh_an = fa / E[0, :]
dm_cb = np.array([rc.comoving_radial_distance(z) for z in ZD]) / rdc; dh_cb = np.array([C_KMS / rc.hubble_parameter(z) for z in ZD]) / rdc
dev = max(np.max(abs(dm_an[1:] / dm_cb[1:] - 1)), np.max(abs(dm_an[:1] / dm_cb[:1] - 1)), np.max(abs(dh_an / dh_cb - 1)))
check("K2b analytic background + spline r_d vs CAMB at the (a) posterior mean: D_M/r_d and D_H/r_d at the seven redshifts agree to 5e-4",
      dev <= 5e-4, f"max |rel| = {dev:.2e} (CAMB r_d {rdc:.4f}, spline {rds:.4f})")
TP = [(0.0215, 0.110), (0.0222, 0.118), (0.0228, 0.125), (0.0219, 0.131), (0.0225, 0.105), (0.0230, 0.140)]
spd = max(abs(float(rd_of(SPL[MNU], w, c)) / camb_rd(w, c)[0] - 1) for w, c in TP)
spd0 = max(abs(float(rd_of(SPL[0.0], w, c)) / camb_rd(w, c, mnu=0.0)[0] - 1) for w, c in TP[:3])
hdep = abs(camb_rd(0.0222, 0.118, H0=62.0)[0] / camb_rd(0.0222, 0.118, H0=76.0)[0] - 1)
check("K2c r_d spline vs direct CAMB at six interior points to 2e-4 (m_nu 0.06; three points for m_nu 0) and r_d varies < 1e-4 over h 0.62-0.76",
      spd <= 2e-4 and spd0 <= 2e-4 and hdep <= 1e-4, f"spline max |rel| {spd:.2e} / {spd0:.2e}; h dependence {hdep:.2e}")
RES["K2"] = dict(cfg681_chi2=float(r1.fun), cfg681_om=float(r1.x[0]), cfg682_maxdev=dmax, camb_bg_dev=float(dev), spline_dev=spd, spline_dev_mnu0=spd0, h_dep=hdep)

banner("K4  GRID ADEQUACY")
k4 = all(s["edge_mass"] < 1e-6 and s["steps_sd"]["Om"] >= 5 and s["steps_sd"]["h"] >= 5 for s in [A] + list(VAR.values()))
check("K4 posterior mass within 3 grid steps of any Om/h boundary < 1e-6 and sd(Om), sd(h) >= 5 grid steps (primary and every (a) variant)",
      k4, "; ".join(f"{k.split()[0]} edge {s['edge_mass']:.1e} steps {s['steps_sd']['Om']:.0f}/{s['steps_sd']['h']:.0f}" for k, s in [("primary", A)] + list(VAR.items())))

# ---- V5 free dark energy (no flat-a0 assumption)
banner("V5  FREE DARK ENERGY (no flat-a0 assumption): CFG682's committed fixed-Om best fits, q profiled, h solved with BBN r_d")
def h_from_q(q, om, wb, wnu=WNU, spl=SPL[MNU]):
    target = C_KMS / (100.0 * q)                                          # h r_d in Mpc
    f = lambda h: h * float(rd_of(spl, wb, om * h * h - wb - wnu)) - target
    # POST-RUN FIX 1 (disclosed in the README): RUN1 bracketed h on [0.50, 0.95], which leaves the r_d spline's omega_c range at the
    # Om ends (NaN for 17/49 rows); the bracket is now the h range where omega_c = Om h^2 - omega_b - omega_nu lies inside the spline.
    wc_lo, wc_hi = math.exp(spl["lwc"][0]), math.exp(spl["lwc"][1])
    hlo = max(0.40, math.sqrt((wc_lo + wb + wnu) / om) * (1 + 1e-9)); hhi = min(1.00, math.sqrt((wc_hi + wb + wnu) / om) * (1 - 1e-9))
    try:
        return brentq(f, hlo, hhi, xtol=1e-10)
    except ValueError:
        return float("nan")
V5 = {}
for tag in ("BAO", "BAO+SN"):
    rows = []
    for r in R682[tag]["rows"]:
        c, q = bao_chi2_681(r["om"], np.array(r["nodes"]))
        hh = h_from_q(q, r["om"], WB["omega_b"]); R = float(R_of(r["om"] * hh * hh, WB["omega_b"], WNU))
        rows.append(dict(om=r["om"], chi2_committed=r["chi2"], q=float(q), h=hh, R=R))
    cmin = min(x["chi2_committed"] for x in rows); sel = [x for x in rows if x["chi2_committed"] - cmin <= 1.0 and np.isfinite(x["R"])]
    V5[tag] = dict(rows=rows, R_range_dchi2_le1=[min(x["R"] for x in sel), max(x["R"] for x in sel)], n_sel=len(sel), n=len(rows))
    P(f"  {tag}: chi2 {cmin:.2f}..{max(x['chi2_committed'] for x in rows):.2f} over Om 0.24-0.36; {len(sel)}/{len(rows)} rows within dchi2 <= 1;"
      f" R over those rows {V5[tag]['R_range_dchi2_le1'][0]:.2f} .. {V5[tag]['R_range_dchi2_le1'][1]:.2f}")
    for x in rows[::8]:
        P(f"      Om {x['om']:.3f}  chi2 {x['chi2_committed']:.3f}  h {x['h']:.4f}  R {x['R']:.3f}")
RES["V5_freeX"] = V5

# ============================================================================================ T2b local ladder
banner("T2(b)  LOCAL LADDER H0 (SH0ES 73.04 +- 1.04, record value) with BAO-shape Om (X = 1, ruler free; BBN r_d NOT used)")
HRDG = np.round(np.arange(90.0, 112.0 + 1e-9, 0.02), 3)
def grid_shape(h_rad):
    chi = np.empty((len(OMG), len(HRDG)))
    for i, om in enumerate(OMG):
        I, E = IE(om, np.array([h_rad]), NEFF * 2 / 3); chi[i] = chi2_bao(I, E, HRDG[None, :])[0]
    return chi
CS = grid_shape(H0_SH0ES[0] / 100); WS = np.exp(-0.5 * (CS - CS.min())); WS /= WS.sum(); POM = WS.sum(1)
om_shape = wstats(OMG, POM); hrd_shape = wstats(HRDG, WS.sum(0))
P(f"  BAO shape only: Om = {om_shape['mean']:.4f} +- {om_shape['sd']:.4f}; h r_d = {hrd_shape['mean']:.2f} +- {hrd_shape['sd']:.2f} Mpc; chi2_min {CS.min():.3f}")
RNG = np.random.default_rng(886); NMC = 1_000_000
EOM = RNG.uniform(-0.0005, 0.0005, NMC); IOM = RNG.choice(len(OMG), NMC, p=POM); OMS = OMG[IOM] + EOM
EH = RNG.standard_normal(NMC); EB = RNG.standard_normal(NMC); EOMG = RNG.standard_normal(NMC)
IJ = RNG.choice(WS.size, NMC, p=WS.ravel()); HRDS = HRDG[IJ % len(HRDG)] + RNG.uniform(-0.01, 0.01, NMC)
WBS = WB["omega_b"] + WB["sigma"] * EB
def opt_b(h0, sh0, om_s):
    hs = (h0 + sh0 * EH) / 100.0; wm = om_s * hs ** 2; R = R_of(wm, WBS, WNU)
    st = dict(h=wstats(hs, np.ones(NMC)), Om=wstats(om_s, np.ones(NMC)), omega_m=wstats(wm, np.ones(NMC)), R=wstats(R, np.ones(NMC)),
              R_literal=wstats(wm / WBS - 1, np.ones(NMC)), f_b=wstats(WBS / wm, np.ones(NMC)), f_b_fw=wstats(1 / (1 + R), np.ones(NMC)))
    z = (st["R"]["mean"] - RATIO_PLANCK) / st["R"]["sd"]; st["z_vs_5364"] = z; st["class"] = rclass(z); st["not_informative"] = st["R"]["sd"] / st["R"]["mean"] > 0.10
    return st, hs
B, hsB = opt_b(*H0_SH0ES, OMS)
show("(b) PRIMARY SH0ES + BAO-shape Om + BBN omega_b", B)
P(f"      omega_m {B['omega_m']['mean']:.4f}+-{B['omega_m']['sd']:.4f}; f_b {B['f_b']['mean']:.4f}+-{B['f_b']['sd']:.4f}; f_b,fw {B['f_b_fw']['mean']:.4f}; R literal {B['R_literal']['mean']:.3f}")
rd_impl = wstats(HRDS / hsB, np.ones(NMC))
P(f"      implied r_d = (h r_d)/h = {rd_impl['mean']:.2f} +- {rd_impl['sd']:.2f} Mpc vs BBN+BAO (a) {A['r_d']['mean']:.2f} +- {A['r_d']['sd']:.2f}"
  f"  -> {(A['r_d']['mean'] - rd_impl['mean']) / math.hypot(A['r_d']['sd'], rd_impl['sd']):.1f} sigma apart (the Hubble tension, not resolved here)")
VB = {}
VB["V1b SH0ES + CFG682 conditional Om"], _ = opt_b(*H0_SH0ES, OM_CFG682[0] + OM_CFG682[1] * EOMG)
for nm, hv in H0_REPORTED.items():
    VB[f"reported: {nm} {hv[0]} +- {hv[1]}"], _ = opt_b(*hv, OMS)
for k, v in VB.items():
    show(k, v)
RES["T2b"] = dict(primary=B, variants=VB, Om_shape=om_shape, hrd_shape=hrd_shape, rd_implied=rd_impl)

# ============================================================================================ T3 classes
banner("T3  THE REBUILT RATIO: CLASSES")
lo, hi = 0.90 * RATIO_PLANCK, 1.10 * RATIO_PLANCK
pin = "NOT PINNED" if not (lo <= A["R"]["mean"] <= hi and lo <= B["R"]["mean"] <= hi) else "PINNED TO +-10%"
spread = (B["R"]["mean"] - A["R"]["mean"]) / RATIO_PLANCK
T3 = dict(recovery_a=A["class"], z_a=A["z_vs_5364"], recovery_b=B["class"], z_b=B["z_vs_5364"], pinning=pin, band=[lo, hi], spread_b_minus_a_frac=spread,
          a_not_informative=A["not_informative"], R_a=A["R"], R_b=B["R"])
P(f"  Planck ratio 5.364 (its own sigma ~0.065 from sigma(omega_c) 0.0012, sigma(omega_b) 0.00015; stated, not added)")
P(f"  (a) BAO+BBN : R = {A['R']['mean']:.3f} +- {A['R']['sd']:.3f}  z {A['z_vs_5364']:+.2f}  -> {A['class']}" + ("  [NOT INFORMATIVE]" if A["not_informative"] else f"  (precision {100 * A['R']['sd'] / A['R']['mean']:.1f}%)"))
P(f"  (b) SH0ES   : R = {B['R']['mean']:.3f} +- {B['R']['sd']:.3f}  z {B['z_vs_5364']:+.2f}  -> {B['class']}  (precision {100 * B['R']['sd'] / B['R']['mean']:.1f}%)")
P(f"  +-10% band [{lo:.3f}, {hi:.3f}]; spread (b)-(a) = {100 * spread:+.1f}% of 5.364  -> {pin}")
RES["T3"] = T3

# ============================================================================================ T4 f_ret provenance + rebuild
banner("T4  CENSUS f_ret: PROVENANCE AND WHAT CAN BE REBUILT")
def find_files(roots, pat):
    hits = []
    for root in roots:
        for dp, dn, fn in os.walk(os.path.join(REPO, root)):
            dn[:] = [d for d in dn if not d.startswith(".") and d != "__pycache__" and not d.startswith("CFG886")]   # POST-RUN FIX 2: own lane excluded
            for f in fn:
                if pat in f.lower(): hits.append(os.path.relpath(os.path.join(dp, f), REPO))
    return hits
def grep_count(root, s, exts=(".md", ".py", ".json")):
    n = 0
    for dp, dn, fn in os.walk(os.path.join(REPO, root)):
        dn[:] = [d for d in dn if not d.startswith(".") and d != "__pycache__" and not d.startswith("CFG886")]   # POST-RUN FIX 2: own lane excluded
        for f in fn:
            if f.endswith(exts):
                try:
                    if s in open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read(): n += 1
                except OSError: pass
    return n
ev = dict(files_named_shull_or_census_in_data=find_files(["real_research/data", "campaign_fresh_gravity"], "shull") + [x for x in find_files(["real_research/data"], "census")],
          lane_files_citing_Shull=grep_count("campaign_fresh_gravity", "Shull"),
          lane_files_with_ramp_code=grep_count("campaign_fresh_gravity", "0.10 + 0.45 * (lM - 12.5)", (".py",)),
          lane_files_with_ramp_text=grep_count("campaign_fresh_gravity", "0.55 at 10^13.5"),
          CFG416_declaration="CFG416 FROZEN_CRITERIA: 'not fitted to growth. It comes from the census and group/cluster baryon fractions, stated in advance'",
          CFG365_quote="Shull, Smith & Danforth 2012: galaxies, groups and clusters ~10% of baryons; collapsed phases incl. CGM 18+-4%; galaxies only 0.07",
          CFG525_D3="'a declared step taken from the cosmic mean in Shull+12 (recalled, PROVISIONAL)'; KiDS M_b = stars + cold gas matches the galaxies-only 0.07",
          CFG634_HC1="calls the 0.10 floor 'stars + cold gas' although the quoted 10% includes group/cluster hot gas (galaxies only = 0.07)",
          CFG379_levels="record group/cluster baryon levels use Newtonian hydrostatic M500 (X-COP M_FORW, Lovisari+15) relative to Planck f_b")
P(f"  evidence: census data table in repo: {ev['files_named_shull_or_census_in_data'] or 'NONE'}; lane files citing Shull: {ev['lane_files_citing_Shull']};"
  f" lane .py files carrying the ramp code: {ev['lane_files_with_ramp_code']}; files with the ramp text: {ev['lane_files_with_ramp_text']}")
SEG = {
    "G galaxy floor 0.10 (log M_ta < 12.5 Msun/h)": dict(
        abundance_matching=False, nfw_lensing=False, hydrostatic_as_DM=False, lcdm_mass_function="not verifiable (the ICM share of the 10% is Shull's; method not in repo)",
        cmb_Omega_b_denominator=True, traceable=False,
        mass_coordinate="framework fixed point M_ta = M_b h/(f_ret f_b) (no measured halo mass enters); CFG804 drops the h (Msun, 0.171 dex)",
        cls="CLEAN", note="cosmic-mean census fraction applied per catchment (assumption: every baryon belongs to some catchment; a per-galaxy value is not "
                          "measured); recalled, PROVISIONAL (CFG525); the quoted 0.10 includes group/cluster hot gas, the galaxies-only value is 0.07"),
    "C group/cluster ramp (0.10 -> 0.55 @13.5 -> 0.85 @14.5, cap 0.90)": dict(
        abundance_matching=False, nfw_lensing="unknown", hydrostatic_as_DM="likely (the record's group/cluster fractions are M_b/M500,HSE over Planck f_b) but not documented",
        lcdm_mass_function="unknown", cmb_Omega_b_denominator=True, traceable=False,
        mass_coordinate="hand-set in M_ta; the R500 -> turnaround-catchment mapping (r_ta ~ 5-13 R200, CFG656) is not documented anywhere in the record",
        cls="UNDETERMINED", note="no source table, no script and no derivation in the repo (declared in CFG416); CFG830 counts these as hand-set census numbers"),
}
segc = [s["cls"] for s in SEG.values()]
FCLS = "CLEAN" if all(c == "CLEAN" for c in segc) else ("LCDM-DEPENDENT" if all(c == "LCDM-DEPENDENT" for c in segc) else "MIXED")
for k, s in SEG.items():
    P(f"  {k}: {s['cls']} (traceable in repo: {s['traceable']})\n      mass coordinate: {s['mass_coordinate']}\n      note: {s['note']}")
P(f"  -> f_ret provenance class: {FCLS} (UNDETERMINED segment: C)")
# rebuild (1) census denominator, (2) stock
def census_rebuild(st):
    h, wb, R = st["h"]["mean"], WB["omega_b"], st["R"]["mean"]
    fr = 0.10 * (h / H_REC) * (WB_REC / wb)
    wc = R * wb
    return dict(f_ret_rebuilt=fr, stock_ratio_only=R / 0.10, stock_census_consistent=R / fr, stock_cc_check=10 * (wc / WB_REC) * (H_REC / h))
CR = {"a": census_rebuild(A), "b": census_rebuild(B)}
for k, c in CR.items():
    P(f"  ({k}) census denominator rebuilt (f ∝ h/omega_b, relative to the record's h 0.674, omega_b 0.02237): f_ret 0.10 -> {c['f_ret_rebuilt']:.4f};"
      f" stock S/M_b: record 53.64 -> ratio-only {c['stock_ratio_only']:.2f}, census-consistent {c['stock_census_consistent']:.2f} (= 10 (omega_c/0.02237)(0.674/h): {c['stock_cc_check']:.2f})")
P("  (the census's own adopted h and Omega_b are not in the repo; the census-consistent numbers assume the record's constants were the census's)")
RES["T4"] = dict(evidence=ev, segments=SEG, cls=FCLS, rebuild=CR)

# ============================================================================================ T5 sensitivity
banner("T5  SENSITIVITY OF RECORD RESULTS (report only)")
SRC876 = os.path.join(LANES, "CFG876_cold_floor_universality", "cfg876.py")
def run876(stock):
    src = open(SRC876).read(); assert src.count("Mcap = 53.64 * (") == 1
    lines = src.replace("Mcap = 53.64 * (", "Mcap = _CFG886_STOCK * (").split("\n")
    n1 = sum(1 for L in lines if L.startswith("json.dump(RES, open(")); n2 = sum(1 for L in lines if L.startswith("open(os.path.join(HERE, f\"cfg876{SUF}.out\")"))
    assert n1 == 1 and n2 == 1
    lines = ["pass" if (L.startswith("json.dump(RES, open(") or L.startswith("open(os.path.join(HERE, f\"cfg876{SUF}.out\")")) else L for L in lines]
    code = "\n".join(lines); assert '"w")' not in code and "'w')" not in code
    old = os.environ.pop("CFG876_MUTATE", None); ns = {"__file__": SRC876, "__name__": "cfg876_readonly", "_CFG886_STOCK": float(stock)}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(code, SRC876, "exec"), ns)
    finally:
        if old is not None: os.environ["CFG876_MUTATE"] = old
    return ns["RES"]
R876 = json.load(open(os.path.join(LANES, "CFG876_cold_floor_universality", "cfg876_results.json")))
k5 = run876(53.64)
d5 = max(abs(k5[f][t]["E"] - R876[f][t]["E"]) for f in ("canonical", "alt") for t in ("primary B", "supply-capped (B)"))
check("K5 CFG876 read-only exec with stock 53.64 reproduces the committed 'primary B' and 'supply-capped (B)' E on both footings to 1e-12", d5 <= 1e-12, f"max |dE| = {d5:.1e}")
STOCKS = {"record 53.64": 53.64, "(a) ratio-only": CR["a"]["stock_ratio_only"], "(a)-1sigma ratio-only": (A["R"]["mean"] - A["R"]["sd"]) / 0.10,
          "(a)+1sigma ratio-only": (A["R"]["mean"] + A["R"]["sd"]) / 0.10, "(b) ratio-only": CR["b"]["stock_ratio_only"],
          "(a) census-consistent": CR["a"]["stock_census_consistent"], "(b) census-consistent": CR["b"]["stock_census_consistent"]}
T5 = dict(CFG876={}, CFG878={}, CFG804={}, engines={})
P("  CFG876 supply-capped variant (reported row there; 18 large dwarfs, cap = stock x M_b):")
for k, s in STOCKS.items():
    rr = k5 if k.startswith("record") else run876(s)
    T5["CFG876"][k] = {f: dict(stock=s, E=rr[f]["supply-capped (B)"]["E"], se=rr[f]["supply-capped (B)"]["se_E"], N_fail=rr[f]["supply-capped (B)"]["N_fail"], cls=rr[f]["supply-capped (B)"]["cls"])
                       for f in ("canonical", "alt")}
    c, a_ = T5["CFG876"][k]["canonical"], T5["CFG876"][k]["alt"]
    P(f"    {k:24s} stock {s:6.2f}: canonical E {c['E']:+.3f} +- {c['se']:.3f} N_fail {c['N_fail']} ({c['cls']}); alt E {a_['E']:+.3f} +- {a_['se']:.3f} N_fail {a_['N_fail']} ({a_['cls']})")
R877 = json.load(open(os.path.join(LANES, "CFG877_finite_cold_clump", "cfg877_results.json")))
MCL = {f: R877[f]["Mcl_Msun"] for f in ("canonical", "alt")}
P("  CFG878 stock note (a universal clump exceeds the stock for M_b below M_cl/stock):")
for k, s in STOCKS.items():
    T5["CFG878"][k] = {f: MCL[f] / s for f in MCL}
    P(f"    {k:24s} stock {s:6.2f}: threshold M_b = {T5['CFG878'][k]['canonical']:.3e} (canonical, M_cl {MCL['canonical']:.3e}) / {T5['CFG878'][k]['alt']:.3e} (alt) Msun")
# CFG804 fixed point
def fret_of(lM):
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)
def N_fp(logMb, R, h=None):
    """CFG804's fixed point (h=None: its Msun convention) or CFG416's declared Msun/h convention (M_ta[Msun/h] = M_b h/(f f_b))."""
    FB = 1 / (1 + R); f = 0.10; lM = None
    for _ in range(400):
        lM = logMb - math.log10(f * FB) + (math.log10(h) if h else 0.0); fn = fret_of(lM)
        if abs(fn - f) < 1e-12: break
        f = 0.5 * (f + fn)
    return 1 / f, lM
edge_of = lambda R, N: math.sqrt(((2 * R * N + 1) ** 2 - 1) / 4)
R804 = {"canonical": json.load(open(os.path.join(LANES, "CFG804_catchment_supply_derived", "cfg804_results.json"))),
        "alt": json.load(open(os.path.join(LANES, "CFG804_catchment_supply_derived", "cfg804_results_alt.json")))}
Nrec = [N_fp(m, RATIO_PLANCK)[0] for m in R804["canonical"]["primary"]["logMb"]]
check("K6 CFG804 fixed point (its own Msun convention) at its canonical primary masses reproduces the README's N 10.0 / 8.8 / 7.4 / 5.6 to <= 0.05",
      max(abs(a - b) for a, b in zip(Nrec, [10.0, 8.8, 7.4, 5.6])) <= 0.05, " / ".join(f"{x:.2f}" for x in Nrec))
P("  CFG804 bins (primary masses): N, stock R N [M_b], edge in r_M; KiDS demand (CFG803 N >= 3-4 at 5.364) = stock >= 16.1-21.5")
CASES = {"record (R 5.364)": (RATIO_PLANCK, H_REC), "(a)": (A["R"]["mean"], A["h"]["mean"]), "(b)": (B["R"]["mean"], B["h"]["mean"])}
for foot in ("canonical", "alt"):
    T5["CFG804"][foot] = {}
    for k, (R, h) in CASES.items():
        rows = []
        for m in R804[foot]["primary"]["logMb"]:
            N1, l1 = N_fp(m, R); N2, l2 = N_fp(m, R, h)
            rows.append(dict(logMb=m, N_msun=N1, lMta_msun=l1, stock_msun=R * N1, edge_msun=edge_of(R, N1), N_msunh=N2, lMta_msunh=l2, stock_msunh=R * N2, edge_msunh=edge_of(R, N2)))
        T5["CFG804"][foot][k] = rows
        P(f"    [{foot}] {k:17s} Msun (CFG804): N " + "/".join(f"{x['N_msun']:.2f}" for x in rows) + "  stock " + "/".join(f"{x['stock_msun']:.1f}" for x in rows)
          + "  edge " + "/".join(f"{x['edge_msun']:.1f}" for x in rows) + " r_M")
        P(f"    [{foot}] {'':17s} Msun/h (CFG416): N " + "/".join(f"{x['N_msunh']:.2f}" for x in rows) + "  stock " + "/".join(f"{x['stock_msunh']:.1f}" for x in rows)
          + "  edge " + "/".join(f"{x['edge_msunh']:.1f}" for x in rows) + " r_M")
# engines: census-edge factor at fixed M_ta
FB0 = 0.02237 / (0.02237 + 0.1200)
def edge_factor(fret, fbn): return math.sqrt(fbn / FB0) * math.log(1 + fret * FB0 / (1 - FB0)) / math.log(1 + fret * fbn / (1 - fbn))
for k, st in (("(a)", A), ("(b)", B)):
    fbn = 1 / (1 + st["R"]["mean"]); T5["engines"][k] = {str(f): edge_factor(f, fbn) for f in (0.10, 0.55)}
    P(f"  CFG650/654 census edge r_M(f_ret f_b M_ta)/ln(1 + f_ret f_b/(1 - f_b)) at fixed M_ta, f_b {FB0:.4f} -> {fbn:.4f} {k}: factor "
      f"{T5['engines'][k]['0.1']:.4f} (f_ret 0.10), {T5['engines'][k]['0.55']:.4f} (0.55)")
P("  Planck inputs still inside the shear engines (not rebuilt here): cfg596/650 h 0.6736, omega_b 0.02237, omega_c 0.1200, n_s 0.965, sigma8 0.811;"
  " CFG654 native: omega_c 0.1202, A_s, n_s, theta_* (CMB-primary). A CMB-free rerun would need this lane's omega_c AND a non-CMB amplitude (none in the record).")
RES["T5"] = T5

# ============================================================================================ MUTATE expectations
if MUT:
    banner("MUTATE dh10 EXPECTATIONS (vs the main run's committed numbers)")
    pm = os.path.join(HERE, "cfg886_results.json")
    if not os.path.exists(pm):
        check("M0 main-run results exist (run the main mode first)", False, "cfg886_results.json missing")
    else:
        MR = json.load(open(pm))
        wb0 = MR["T1"]["PDG 2024"]["PRIMARY (midpoint)"]["omega_b"]; ra0 = MR["T2a"]["primary"]["R"]["mean"]; rb0 = MR["T2b"]["primary"]["R"]["mean"]
        dw = WB["omega_b"] / wb0 - 1; dra = A["R"]["mean"] / ra0 - 1; exp_b = wb0 / WB["omega_b"]; got_b = (B["R"]["mean"] + 1) / (rb0 + 1)
        check("M1 omega_b (primary) lower by 4-8%", -0.08 <= dw <= -0.04, f"{100 * dw:+.2f}%")
        check("M2 R(a) higher by +1% to +6%", 0.01 <= dra <= 0.06, f"{100 * dra:+.2f}% (R {ra0:.3f} -> {A['R']['mean']:.3f})")
        check("M3 R(b)+1 higher by the inverse omega_b ratio to within 0.5%", abs(got_b / exp_b - 1) <= 0.005, f"ratio {got_b:.5f} vs expected {exp_b:.5f} (R {rb0:.3f} -> {B['R']['mean']:.3f})")

# ============================================================================================ summary
banner("SUMMARY")
lb = [v for v in CHK.values() if v["load_bearing"]]; allok = all(v["ok"] for v in lb)
P(f"  T1 omega_b (D/H PDG 2024, BBN midpoint) = {WB['omega_b']:.5f} +- {WB['sigma']:.5f}")
P(f"  T2a h = {A['h']['mean']:.4f} +- {A['h']['sd']:.4f}, Om = {A['Om']['mean']:.4f} +- {A['Om']['sd']:.4f}  ->  R = {A['R']['mean']:.3f} +- {A['R']['sd']:.3f}  ({A['class']}, z {A['z_vs_5364']:+.2f}); f_b {A['f_b']['mean']:.4f}")
P(f"  T2b h = {B['h']['mean']:.4f} (SH0ES), Om = {B['Om']['mean']:.4f}  ->  R = {B['R']['mean']:.3f} +- {B['R']['sd']:.3f}  ({B['class']}, z {B['z_vs_5364']:+.2f}); f_b {B['f_b']['mean']:.4f}")
P(f"  T3 {T3['pinning']} (spread {100 * spread:+.1f}% of 5.364);  T4 f_ret {FCLS};  V5 free dark energy: R {V5['BAO']['R_range_dchi2_le1'][0]:.2f}-{V5['BAO']['R_range_dchi2_le1'][1]:.2f} (BAO), "
  f"{V5['BAO+SN']['R_range_dchi2_le1'][0]:.2f}-{V5['BAO+SN']['R_range_dchi2_le1'][1]:.2f} (BAO+SN) over Om 0.24-0.36")
P(f"  controls: " + ", ".join(f"{k} {'PASS' if v['ok'] else 'FAIL'}" + ("" if v["load_bearing"] else "(rep)") for k, v in CHK.items()) + f"  -> rc {0 if allok else 1}")
P(f"  runtime {time.time() - T0:.0f} s.  kappa fitted; cold energy mass required; not theory closed.")
RES["checks"] = CHK; RES["all_load_bearing_pass"] = allok
json.dump(RES, open(os.path.join(HERE, f"cfg886_results{SUF}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
open(os.path.join(HERE, f"cfg886{SUF}.out"), "w").write("\n".join(OUTL) + "\n")
sys.exit(0 if allok else 1)

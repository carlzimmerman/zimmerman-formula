"""LAM1 stage 0 (criteria 5ed7fac28a; amendments A1-A7 in AMENDMENTS.md): F1 training count, K0 isolation rebuild,
proxy f_slow, F2 power forecast. Run: python3 -I lam1_stage0.py. Single thread, under 1 GB. kappa = 1/2 FITTED; not theory closed."""
import os, glob, json, math, numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); EXT = os.path.join(ROOT, "_external_data")
CFG = os.path.join(ROOT, "campaign_fresh_gravity"); OUT = []; RES = {"lane": "LAM1", "stage": 0}
def P(s=""): print(s, flush=True); OUT.append(s)

# ---- distances: CFG681 Efun copied verbatim, T2 BAO+SN free fit, h70 units (A7) ----
NODES = np.array([0, 0.4, 0.7, 1.0, 1.5, 2.33]); h = 0.68; OMR = 2.469e-5 / h**2 * (1 + 0.2271 * 3.046)
def Efun(om, xn, z):
    X = np.interp(z, NODES, np.r_[1.0, xn]); E2 = om*(1+z)**3 + OMR*(1+z)**4 + (1 - om - OMR)*X
    return np.sqrt(np.where(E2 > 1e-6, E2, np.nan))
t2 = json.load(open(os.path.join(CFG, "CFG681_bao_raw_geometry", "cfg681_results.json")))["T2_BAO+SN"]
zg = np.linspace(0, 1.0, 20001); f = 1 / Efun(t2["om_free"], np.array(t2["X_nodes"]), zg)
chig = 299792.458 / 70.0 * np.r_[0, np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(zg))]
chi = lambda z: np.interp(z, zg, chig)
P(f"D(z): CFG681 T2 om {t2['om_free']:.4f}, chi(0.1) {chi(0.1):.1f}, chi(0.5) {chi(0.5):.1f} Mpc/h70")

def unit(ra, dec):
    r, d = np.radians(ra), np.radians(dec); return np.c_[np.cos(d) * np.cos(r), np.cos(d) * np.sin(r), np.sin(d)]
def match(ra1, de1, ra2, de2, arcsec=1.0):
    d, i = cKDTree(unit(ra2, de2)).query(unit(ra1, de1), distance_upper_bound=2 * math.sin(math.radians(arcsec / 3600) / 2))
    return np.isfinite(d), i
def sdss(pattern):
    rows = [np.loadtxt(fn, delimiter=",", skiprows=2, usecols=(1, 2, 3), ndmin=2) for fn in sorted(glob.glob(pattern))]
    a = np.vstack([r for r in rows if r.size]); return a[:, 0], a[:, 1], a[:, 2]
SD = os.path.join(EXT, "lam1_sdss_specobj_2026_11_03")

# ---- F1: DynPop with an SDSS fibre spectrum ----
dp = fits.open(os.path.join(EXT, "lam1_dynpop_2026_11_03", "SDSSDR17_MaNGA_JAM_v2.fits"))[1].data
lam, eps, qual = dp["Lambda_Re"].astype(float), dp["Eps_MGE"].astype(float), dp["Qual"].astype(int)
good = (qual >= 1) & np.isfinite(lam) & np.isfinite(eps) & (eps >= 0); slow = lam < 0.31 * np.sqrt(np.clip(eps, 0, None))
ra_s, de_s, z_s = sdss(os.path.join(SD, "dyn_ra*.csv")); hit, _ = match(dp["obj_ra"], dp["obj_dec"], ra_s, de_s)
nt, ns = int((good & hit).sum()), int((good & hit & slow).sum())
P(f"F1: DynPop Qual>=1 {int(good.sum())}, with SDSS fibre <=1\" {nt}, slow {ns} (need >=1000, >=100): {'PASS' if nt >= 1000 and ns >= 100 else 'FAIL'}")
P(f"    rows: Qual>=2 matched {int(((qual >= 2) & good & hit).sum())}; DynPop stays chosen if matched > 3000: {'YES' if nt > 3000 else 'NO, count SAMI'}")
RES["F1"] = dict(n_good=int(good.sum()), n_train=nt, n_slow=ns, pass_=bool(nt >= 1000 and ns >= 100), dynpop_kept=bool(nt > 3000))

# ---- K0: B21 isolation rebuilt (A3, A7) ----
kb = fits.open(os.path.join(EXT, "lam1_kids_bright_2026_11_03", "KiDS_DR4_brightsample.fits"))[1].data
lp = fits.open(os.path.join(EXT, "lam1_kids_bright_2026_11_03", "KiDS_DR4_brightsample_LePhare.fits"))[1].data
assert np.array_equal(kb["ID"], lp["ID"]), "row order differs"
M = lp["MASS_BEST"].astype(float); z = kb["zphot_ANNz2"].astype(float)
ok = (kb["masked"] == 0) & np.isfinite(M) & (M > 0) & np.isfinite(z) & (z > 0)
ur = (lp["MAG_ABS_u"] + lp["K_COR_u"]) - (lp["MAG_ABS_r"] + lp["K_COR_r"]); ur = np.where(np.abs(ur) < 10, ur, np.nan)
idx = np.flatnonzero(ok); X = unit(kb["RAJ2000"][idx], kb["DECJ2000"][idx]) * chi(z[idx])[:, None]
lens = (z[idx] > 0.1) & (z[idx] < 0.5) & (M[idx] < 11.0)
tree = cKDTree(X); rmax = 3.0 * 1.5
pr = tree.query_pairs(rmax, output_type="ndarray"); d = np.linalg.norm(X[pr[:, 0]] - X[pr[:, 1]], axis=1)
Mi = M[idx]; zi = z[idx]
def isolated(phys):
    bad = np.zeros(len(idx), bool)
    for a, b in ((0, 1), (1, 0)):
        i, j = pr[:, a], pr[:, b]; lim = 3.0 * (1 + zi[i]) if phys else 3.0
        sel = (d < lim) & (Mi[j] > Mi[i] - 1.0); bad[i[sel]] = True
    return lens & ~bad
iso = isolated(False); isoP = isolated(True); n_iso, n_isoP = int(iso.sum()), int(isoP.sum()); B21 = 259383
k0 = abs(n_iso / B21 - 1) <= 0.15
P(f"K0: lenses {int(lens.sum())}, isolated comoving sphere {n_iso} ({n_iso / B21 - 1:+.3f} vs B21 259,383, tol 15%): {'PASS' if k0 else 'FAIL -> F2 NOT EVALUABLE'}")
P(f"    row: physical sphere {n_isoP} ({n_isoP / B21 - 1:+.3f}); colour finite in isolated {int(np.isfinite(ur[idx][iso]).sum())}")
red = iso & (ur[idx] > 2.5); n_red = int(red.sum())
P(f"    red isolated (RECONSTRUCTED COLOUR > 2.5): {n_red}, fraction {n_red / max(n_iso, 1):.3f}")
RES["K0"] = dict(n_lens=int(lens.sum()), n_iso=n_iso, n_iso_phys=n_isoP, rel=n_iso / B21 - 1, pass_=bool(k0), n_red=n_red)

# ---- application sample: red isolated with an SDSS spectrum (KiDS-N only) ----
ra_k, de_k, z_k = sdss(os.path.join(SD, "kidsn.csv")); ri = idx[red]
hk, jk = match(kb["RAJ2000"][ri], kb["DECJ2000"][ri], ra_k, de_k); n_app = int(hk.sum()); Mapp = M[ri][hk]
P(f"Application: red isolated with SDSS DR17 spectrum <=1\": {n_app}; spec-z median {np.median(z_k[jk[hk]]) if n_app else float('nan'):.3f}")

# ---- proxy f_slow (A4): DynPop red (NSA rest u-r >= 2.2), reweighted to the application M* distribution ----
am = dp["nsa_sersic_absmag"].astype(float); dred = good & ((am[:, 2] - am[:, 4]) >= 2.2)
def fslow(mcol):
    mh = dp[mcol].astype(float); mh = np.where(mh > 100, np.log10(np.clip(mh, 1, None)), mh) + 0.310
    edges = np.arange(9.0, 11.21, 0.2); wa, _ = np.histogram(Mapp, edges); fs = []; lost = 0
    for k in range(len(edges) - 1):
        s = dred & (mh >= edges[k]) & (mh < edges[k + 1])
        if s.sum() < 10: lost += wa[k]; fs.append(np.nan)
        else: fs.append(slow[s].mean())
    fs = np.array(fs); w = np.where(np.isfinite(fs), wa, 0); return float(np.nansum(fs * w) / max(w.sum(), 1)), lost / max(wa.sum(), 1)
fsl, lost = fslow("nsa_sersic_mass"); fsl_e, _ = fslow("nsa_elpetro_mass")
P(f"PROXY f_slow (sersic mass) {fsl:.3f}, application weight in empty bins {lost:.3f}; row: elpetro mass {fsl_e:.3f}")
RES["app"] = dict(n_app=n_app, f_slow=fsl, f_slow_elpetro=fsl_e, weight_lost=lost)

# ---- F2: power, from B21's red-bin error (CFG849's loader and amplitude) ----
src = open(os.path.join(CFG, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py")).read().split("P(\"CFG829  KiDS")[0]
Mo = {"__file__": os.path.join(CFG, "CFG829_lensing_low_g_vs_dwarf_excess", "cfg829.py"), "__name__": "d"}; exec(compile(src, "cfg829.py", "exec"), Mo)
c850 = json.load(open(os.path.join(CFG, "CFG850_red_split_mstar_systematic", "cfg850_results.json")))["rows"]
f2 = {}
for foot in ("canonical", "alt"):
    gb, go, C = Mo["load"]("Fig-8_RAR-KiDS-isolated_Colorbin_2.txt", "Fig-8_RAR-KiDS-isolated_Colorbins_covmatrix.txt", 2.5)
    a = Mo["amp"](gb, go, C, gb * Mo["nu_e"](gb / Mo["A0"][foot]), Mo["W"]); sB = a["sA"]
    Ar0, Ar = c850[f"{foot}|0.0|0.0"]["A_red"], c850[f"{foot}|0.123|0.0"]["A_red"]; ssys = Ar0 - Ar
    ns_, nf_ = fsl * n_app, (1 - fsl) * n_app
    sd = math.sqrt(sB**2 * n_red / max(ns_, 1) + sB**2 * n_red / max(nf_, 1) + ssys**2) if n_app else float("inf")
    dar = (Ar - 1) / fsl if fsl > 0 else float("inf"); pw = bool(sd <= dar / 3); ps = bool(k0 and pw)
    f2[foot] = dict(sigma_B21_red=sB, A_red=Ar, sigma_sys=ssys, N_slow=ns_, N_fast=nf_, sigma_dA=sd, dA_rot=dar, power_alone=pw, pass_=ps)
    lab = ("PASS" if ps else "FAIL") if k0 else f"NOT EVALUABLE (K0); power alone {'passes' if pw else 'fails'}"
    P(f"F2 {foot}: sigma_B21,red {sB:.3f}; N_slow {ns_:.0f}, N_fast {nf_:.0f}; sigma(dA) {sd:.3f} (sys {ssys:.3f}) vs dA_rot/3 = {dar / 3:.3f}: {lab}")
    P(f"    KINEMATIC needs dA >= 0.30 at > 3 sigma, so dA >= {max(0.30, 3 * sd):.2f} here")
RES["F2"] = f2
v = "PASS" if (RES["F1"]["pass_"] and k0 and all(x["pass_"] for x in f2.values())) else ("NOT EVALUABLE" if not k0 else "STOP")
P(f"STAGE 0: {v}. F3 (compute) is a scheduling gate, read by hand."); RES["verdict"] = v
open(os.path.join(HERE, "lam1_stage0.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, "lam1_stage0.json"), "w"), indent=1, default=float)

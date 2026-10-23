"""F1_cluster_cores (criteria 9fd5aee16e): from-scratch rebuild of the CFG687 cluster-core excess.
Own KiDS reader (f1_extract.py cache, argv[1]), own estimator, own spherical AQUAL lensing model, eRASS1 from the FITS.
The record (CFG687 npz, cfg687_results.json, CFG4_common.nu_mono) is read only for the reproduction checks K1-K3.
--mutate: cross shear instead of tangential (K2/K3 must fail). Deterministic, no network, single thread."""
import os, sys, json, numpy as np
from scipy.interpolate import PchipInterpolator
from astropy.io import fits
_trap = getattr(np, "trapezoid", None) or np.trapz
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; CACHE = [a for a in sys.argv[1:] if not a.startswith("--")][0]
TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"f1_cluster_cores{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}"); RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
# ---------------------------------------------------------------- constants (SI)
G = 6.674e-11; C = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; MP = 1.6726e-27; KG_PC2 = MSUN/(3.0857e16)**2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                                    # FP0 footings; kappa = 1/2 FITTED
sys.path.insert(0, os.path.join(REPO, "campaign_fresh_gravity"))
import CFG4_common as C4                                                              # record kernel nu_mono (reproduction only)
assert abs(C4.A0["canonical"] - A0["canonical"]) < 1e-15 and abs(C4.A0["alt"] - A0["alt"]) < 1e-15
def nu_simple(y):                                                                      # inverse of mu = x/(1+x): the action's AQUAL (E2, C4)
    y = np.maximum(y, 1e-300); return 0.5 + np.sqrt(0.25 + 1/y)
def g_aqual_sph(gN, a0):
    """spherical AQUAL: Gauss's law gives mu(g/a0) g = gN exactly (curl term vanishes); positive root of g^2 - gN g - gN a0 = 0."""
    return 0.5*gN + np.sqrt(0.25*gN**2 + gN*a0)
# ---------------------------------------------------------------- distances: raw DESI DR2 BAO ratios (CFG681 table) x r_d
zb_ = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
PCH = PchipInterpolator(np.r_[0, 0.295, zb_], np.r_[0, DMb, DMr]); HRD = 101.54
def DM(z, h): return PCH(np.minimum(np.asarray(z, float), 2.33))*HRD/h              # Mpc; r_d = 101.54/h
def DA_lcdm(z, H0=70.0, Om=0.3):
    zz = np.linspace(0, z, 600); E = np.sqrt(Om*(1 + zz)**3 + 1 - Om); return _trap(1/E, zz)*C/1e3/H0/(1 + z)
HS = {"h070": 0.70, "h0672": 0.672, "h0686": 0.686}
# ---------------------------------------------------------------- sources (cell-sorted cache)
CELL = 0.2; NRA = int(round(360/CELL))
S = {k: np.load(os.path.join(CACHE, f"{k}.npy"), mmap_mode="r") for k in ("ra", "dec", "e1", "e2", "w", "zb", "cell")}
NS = len(S["cell"]); CELLS = np.asarray(S["cell"])
ZBMAX = 1.2                                                                            # float32 Z_B = 1.2 reads 1.2000000477 > 1.2: dropped, as in the record
say(f"sources in cache {NS:,}; with Z_B <= 1.2 (float32): {int((np.asarray(S['zb']) <= 1.2).sum()):,}")
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1]); M_BIAS = -0.01
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
def gather(ra, de, th_deg):
    d0 = int(np.floor((de - th_deg + 90)/CELL)); d1 = int(np.floor((de + th_deg + 90)/CELL))
    dra = th_deg/max(np.cos(np.radians(min(abs(de) + th_deg, 89.0))), 1e-3); idx = []
    for di in range(d0, d1 + 1):
        r0 = int(np.floor(((ra - dra) % 360)/CELL)); n = int(np.ceil(2*dra/CELL)) + 1
        cells = (np.arange(r0, r0 + n) % NRA) + di*NRA
        lo = np.searchsorted(CELLS, cells, "left"); hi = np.searchsorted(CELLS, cells, "right")
        idx += [np.arange(a, b) for a, b in zip(lo, hi) if b > a]
    return np.concatenate(idx) if idx else np.zeros(0, int)
def esd(ra, de, zl, hs, cross=False):
    """returns per h: (num, den, var, count) in 8 physical-Mpc bins; record conventions (e2-flipped tangential sign,
    inverse-Sigma_crit^2 weights, Z_B > z_l + 0.2, m = -0.01)."""
    thmax = max(3.0/(DM(zl, h)/(1 + zl)) for h in hs.values())*1.02
    ii = gather(ra, de, np.degrees(thmax))
    if ii.size < 10: return None
    zs = np.asarray(S["zb"][ii], float); keep = (zs > zl + 0.2) & (zs <= ZBMAX); ii = ii[keep]; zs = zs[keep]
    rs = np.asarray(S["ra"][ii]); ds = np.asarray(S["dec"][ii]); e1 = np.asarray(S["e1"][ii], float); e2 = np.asarray(S["e2"][ii], float); ws = np.asarray(S["w"][ii], float)
    dra = (np.radians(rs) - np.radians(ra))*np.cos(np.radians(de)); dra = (dra + np.pi) % (2*np.pi) - np.pi; dde = np.radians(ds) - np.radians(de)
    th = np.hypot(dra, dde); phi = np.arctan2(dde, dra)
    et = -(e1*np.cos(2*phi) - e2*np.sin(2*phi)); ex = -(e1*np.sin(2*phi) + e2*np.cos(2*phi)); val0 = ex if cross else et
    out = {}
    for key, h in hs.items():
        DlM = float(DM(zl, h)); Dl = DlM/(1 + zl); DMs = DM(zs, h)
        isc = np.clip(4*np.pi*G/C**2*(Dl*MPC)*((DMs - DlM)/(1 + zs))/(DMs/(1 + zs)), 0, None)
        k = np.digitize(th*Dl, EDGES) - 1; g = (k >= 0) & (k < 8) & (isc > 0)
        ww = ws*isc**2; val = val0/np.where(isc > 0, isc, 1)
        out[key] = (np.bincount(k[g], (ww*val)[g], 8), np.bincount(k[g], ww[g], 8), np.bincount(k[g], (ww**2*val**2)[g], 8), int(g.sum()))
    return out
def finish(t):
    num, den, var, n = t
    with np.errstate(invalid="ignore", divide="ignore"):
        return num/den/KG_PC2/(1 + M_BIAS), np.sqrt(var)/den/KG_PC2, den, n
# ---------------------------------------------------------------- eRASS1 clusters from the FITS (centre = X-ray fit, as the record's TSV)
E = fits.open(os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"))[1].data
CL = []
for r in E:
    ra, de, z, mg, R5 = float(r["RA_XFIT"]), float(r["DEC_XFIT"]), float(r["BEST_Z"]), float(r["MGAS500"]), float(r["R500"])
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    if (inN or inS) and 0.05 <= z <= 0.5 and np.isfinite(mg) and mg > 0 and np.isfinite(R5) and R5 > 0:
        off = np.degrees(np.arccos(np.clip(np.sin(np.radians(de))*np.sin(np.radians(r["DEC"])) + np.cos(np.radians(de))*np.cos(np.radians(r["DEC"]))*np.cos(np.radians(ra - r["RA"])), -1, 1)))
        CL.append(dict(name=str(r["NAME"]).strip(), ra=ra, dec=de, z=z, Mgas500=mg*1e11, MgL=float(r["MGAS500_L"])*1e11, MgH=float(r["MGAS500_H"])*1e11,
                       R500=R5/1e3, off_deg=float(off)))
say(f"eRASS1 candidates in KiDS boxes (FITS): {len(CL)}")
# K6: TSV vs FITS
tsv = {}
for l in open(os.path.join(REPO, "..", "_external_data", "cfg687_inputs", "erass1_main.tsv")):
    p = l.rstrip("\n").split("\t")
    try: tsv[p[0].strip()] = (float(p[5])*1e11, float(p[8])/1e3)
    except Exception: pass
dm = [max(abs(tsv[c["name"]][0]/c["Mgas500"] - 1), abs(tsv[c["name"]][1]/c["R500"] - 1)) for c in CL if c["name"] in tsv]
check("K6", len(dm) == len(CL) and max(dm) <= 1e-3, f"matched {len(dm)}/{len(CL)} max_rel {max(dm):.2e}", "all matched, <= 1e-3")
# ---------------------------------------------------------------- measurement (three backgrounds share sources and randoms)
import pickle
MCACHE = os.path.join(CACHE, f"f1_meas{TAG}.pkl")                                   # measurement cache (scratch, not the repo)
rng = np.random.default_rng(20261022); MEAS = pickle.load(open(MCACHE, "rb")) if os.path.exists(MCACHE) else []
for i, cl in enumerate([] if MEAS else CL):
    m = esd(cl["ra"], cl["dec"], cl["z"], HS, cross=MUT)
    if m is None or m["h070"][3] < 200: continue
    rnd = []
    for _ in range(10):
        a = rng.uniform(0, 2*np.pi); s = rng.uniform(1, 3)
        rr = esd((cl["ra"] + s*np.cos(a)/np.cos(np.radians(cl["dec"]))) % 360, cl["dec"] + s*np.sin(a), cl["z"], HS, cross=MUT)
        if rr is not None and rr["h070"][3] > 0.5*m["h070"][3]: rnd.append(rr)
        if len(rnd) >= 6: break
    if len(rnd) < 5: continue
    rec = dict(cl)
    for key in HS:
        d, e, den, n = finish(m[key]); R = [finish(x[key]) for x in rnd]
        rec[key] = dict(D=np.nan_to_num(d) - np.nan_to_num(np.array([x[0] for x in R])).mean(0), Draw=np.nan_to_num(d),
                        Rmean=np.nan_to_num(np.array([x[0] for x in R])).mean(0), E=np.nan_to_num(e, nan=1e9), den=den, den_r=np.array([x[2] for x in R]).mean(0))
    MEAS.append(rec)
    if len(MEAS) % 50 == 0: say(f"  measured {len(MEAS)} clusters (of {i+1} tried)")
pickle.dump(MEAS, open(MCACHE, "wb")); N = len(MEAS); say(f"clusters used: {N}")
order = np.argsort([o["ra"] for o in MEAS]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N)*30//N
def arr(key, f): return np.array([o[key][f] for o in MEAS])
def A_band(D, P, W, sel):
    return {b: float((W[sel][:, j]*D[sel][:, j]).sum()/(W[sel][:, j]*P[sel][:, j]).sum()) for b, j in BANDS.items()}
def jk(D, P, W):
    full = A_band(D, P, W, np.ones(N, bool)); reps = [A_band(D, P, W, PATCH != p) for p in range(30)]
    return {b: (full[b], float(np.sqrt(29/30*np.sum((np.array([r[b] for r in reps]) - np.mean([r[b] for r in reps]))**2)))) for b in full}
def stack(D, W):
    f = lambda s: (W[s]*D[s]).sum(0)/W[s].sum(0); full = f(np.ones(N, bool)); reps = np.array([f(PATCH != p) for p in range(30)])
    return full, np.sqrt(29/30*((reps - reps.mean(0))**2).sum(0))
# ---------------------------------------------------------------- the law's lensing from baryons (own projector)
RG = np.logspace(-3, np.log10(30), 3000); RF = np.logspace(np.log10(2e-3), np.log10(3.5), 90); UU = np.linspace(0, 1, 2001)
def project(rho, r=RG):
    """Sigma(R) on RF by r = R cosh u; DeltaSigma(R) = mean Sigma inside R - Sigma(R) (inner disc < RF[0] at Sigma(RF[0]))."""
    lr = np.log(r); pos = rho > 0; lrho = np.log(np.where(pos, rho, 1e-300))
    umax = np.arccosh(r[-1]/RF); u = UU[None, :]*umax[:, None]; rr = RF[:, None]*np.cosh(u)
    Sig = 2*_trap(np.exp(np.interp(np.log(rr), lr[pos], lrho[pos]))*rr*MPC, u, axis=1)
    cum = np.r_[0.5*Sig[0]*RF[0]**2, 0.5*Sig[0]*RF[0]**2 + np.cumsum(0.5*(Sig[1:]*RF[1:] + Sig[:-1]*RF[:-1])*np.diff(RF))]
    return Sig, 2*cum/RF**2 - Sig
def offset(Sig, d):
    if d <= 1e-4: return Sig
    ph = np.linspace(0, np.pi, 181); Rp = np.sqrt(RF[:, None]**2 + d**2 + 2*RF[:, None]*d*np.cos(ph[None, :]))
    So = _trap(np.exp(np.interp(np.log(Rp), np.log(RF), np.log(Sig))), ph, axis=1)/np.pi
    return So
def dsig_from_sig(Sig):
    cum = np.r_[0.5*Sig[0]*RF[0]**2, 0.5*Sig[0]*RF[0]**2 + np.cumsum(0.5*(Sig[1:]*RF[1:] + Sig[:-1]*RF[:-1])*np.diff(RF))]
    return 2*cum/RF**2 - Sig
def at_bins(ds): return np.exp(np.interp(np.log(RC), np.log(RF), np.log(np.maximum(ds, 1e-30))))
# SIS self-test (K4)
_s = 1e6; _rho = _s**2/(2*np.pi*G*(RG*MPC)**2); _, _ds = project(_rho); _ratio = at_bins(_ds)/(_s**2/(2*G*RC*MPC))
check("K4", np.all(np.abs(_ratio[3:] - 1) < 0.01), np.round(_ratio, 4).tolist(), "|ratio-1| < 0.01 in MID/OUTER bins")
# X-COP measured gas shape (G1): median M_gas(<x)/M_gas(<1), x = r/R500 (X-COP hydrostatic R500)
XD = os.path.join(REPO, "real_research", "data", "xcop"); XS = []; XG = np.logspace(np.log10(0.03), np.log10(2.5), 200)
for nm in sorted(os.listdir(XD)):
    f = os.path.join(XD, nm, f"{nm}_fgas_profile.fits")
    if os.path.exists(f):
        d = fits.open(f)[1].data; x = np.asarray(d["RADIUS"], float); mg = np.asarray(d["MGAS"], float); ok = (x > 0) & (mg > 0)
        m1 = np.exp(np.interp(0.0, np.log(x[ok]), np.log(mg[ok])))
        XS.append(np.where(XG <= x[ok].max(), np.exp(np.interp(np.log(XG), np.log(x[ok]), np.log(mg[ok]/m1))), np.nan))
XS = np.array(XS); XMED = np.nanmedian(XS, 0); okx = np.isfinite(XMED) & (np.sum(np.isfinite(XS), 0) >= 6)
XG1, XM1 = XG[okx], XMED[okx]; XSLOPE = np.polyfit(np.log(XG1[-15:]), np.log(XM1[-15:]), 1)[0]
say(f"X-COP measured gas shape: {len(XS)} clusters, x range {XG1[0]:.2f}-{XG1[-1]:.2f}, M(<x) outer log-slope {XSLOPE:.2f} (beta=2/3 -> 1)")
RES["xcop_shape"] = dict(n=len(XS), xmax=float(XG1[-1]), outer_slope=float(XSLOPE), M_at_x2=float(np.interp(np.log(2.0), np.log(XG1), XM1)) if XG1[-1] >= 2 else None)
def gas_mass(cl, Mg500, R500, shape="G0", rcfac=1.0, beta=2/3):
    r = RG
    if shape == "G1":
        x = r/R500; M = Mg500*np.where(x <= XG1[-1], np.exp(np.interp(np.log(np.maximum(x, XG1[0])), np.log(XG1), np.log(XM1)))*np.where(x < XG1[0], (x/XG1[0])**3, 1),
                                          XM1[-1]*(x/XG1[-1])**XSLOPE)
        M = np.minimum(M, np.interp(3.0, r, M)) if True else M
        return M*MSUN
    rc = 0.15*R500*rcfac; sh = (1 + (r/rc)**2)**(-1.5*beta)
    if shape == "G2": sh = np.where(r > R500, 0.0, sh)
    sh[r > 3.0] = 0
    dm = 4*np.pi*(r*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    M500 = np.interp(R500, r, M); return M*(Mg500*MSUN/M500)
COLD_R200 = []
def cold_mass(cl, Mb, h, cstar, ufac):
    """L187 settled cold component: Omega_c/Omega_b = 5.364 x baryons (CFG949 supply) x ufac, NFW with c* = 0.40 relative to a
    self-consistent R200c (200 rho_crit(z), H(z) = 100h sqrt(0.3(1+z)^3 + 0.7)); truncated at R200 (labelled). LCDM-PROCESSED geometry."""
    Hz = 100*h*1e3/MPC*np.sqrt(0.3*(1 + cl["z"])**3 + 0.7); rc = 3*Hz**2/(8*np.pi*G)
    tot = Mb*(1 + 5.364*ufac) - 200*rc*4/3*np.pi*(RG*MPC)**3; pos = np.nonzero(tot > 0)[0]; R200 = RG[min(pos[-1] + 1, len(RG) - 1)] if pos.size else RG[0]   # outermost crossing
    M200c = 5.364*ufac*np.interp(R200, RG, Mb); m = lambda x: np.log1p(x) - x/(1 + x)
    COLD_R200.append(R200); return M200c*m(cstar*np.minimum(RG, R200)/R200)/m(cstar)
def predict(cl, a0, kernel="aqual", hkey="h070", rescale=False, shape="G0", fs=0.20, rcfac=1.0, mg="mid", gasfac=1.0, dust=0.0, miscen=False, cold=None):
    h = HS[hkey]; q = (float(DM(cl["z"], h))/(1 + cl["z"]))/DA_lcdm(cl["z"]) if rescale else 1.0
    Mg500 = {"mid": cl["Mgas500"], "L": cl["MgL"], "H": cl["MgH"]}[mg]*q**2.5*gasfac; R500 = cl["R500"]*q
    Mg = gas_mass(cl, Mg500, R500, shape, rcfac); Mb = Mg*(1 + fs) + dust*Mg
    gc = 0.0
    if cold is not None:                                       # coordinator row: settled cold component, L187 c*, no refit
        cstar, ufac, mode = cold; Mc = cold_mass(cl, Mb, h, cstar, ufac)
        if mode == "sourced": Mb = Mb + Mc                     # cold mass sources the AQUAL field (V3: dust is in rho)
        else: gc = G*Mc/(RG*MPC)**2                            # law on baryons + Newtonian cold (CFG949-style reading)
    gN = G*Mb/(RG*MPC)**2
    if a0 == 0: g = gN
    elif kernel == "aqual": g = g_aqual_sph(gN, a0)
    else: g = gN*C4.nu_mono(gN/a0)
    g = g + gc
    ML = g*(RG*MPC)**2/G; rho = np.gradient(ML, RG*MPC)/(4*np.pi*(RG*MPC)**2)
    Sig, ds = project(rho)
    if miscen:
        d = np.radians(cl["off_deg"])*float(DM(cl["z"], h))/(1 + cl["z"]); ds = dsig_from_sig(offset(Sig, d))
    return at_bins(ds)/KG_PC2
# ---------------------------------------------------------------- K5: AQUAL identity and the record kernel
yy = np.logspace(-3, 2, 400); gN = yy*1e-10; ga = g_aqual_sph(gN, 1e-10); mu = (ga/1e-10)/(1 + ga/1e-10)
idq = np.max(np.abs(mu*ga/gN - 1)); idn = np.max(np.abs(ga/(gN*nu_simple(yy)) - 1)); dmono = np.max(np.abs(C4.nu_mono(yy)/nu_simple(yy) - 1))
yc = np.array([0.05, 0.1, 0.2, 0.5, 1.0]); RES["nu_mono_over_nu_simple"] = dict(zip([str(v) for v in yc], np.round(C4.nu_mono(yc)/nu_simple(yc), 4).tolist()))
check("K5", idq < 1e-9 and idn < 1e-9 and dmono > 1e-3, f"Gauss {idq:.1e} QUMOND-id {idn:.1e} max|nu_mono/nu_simple-1| {dmono:.3f}", "<1e-9, <1e-9, >1e-3")
say(f"  nu_mono/nu_simple at y = {yc.tolist()}: {RES['nu_mono_over_nu_simple']}")
# ---------------------------------------------------------------- K1: record npz
npz = np.load(os.path.join(REPO, "campaign_fresh_gravity", "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
Wr = np.where(npz["E"] > 0, 1/npz["E"]**2, 0); j = BANDS["MID"]; Ar = (Wr[:, j]*npz["D"][:, j]).sum()/(Wr[:, j]*npz["PL"][:, j]).sum()
REC = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG687_erass1_shear_stack", "cfg687_results.json")))
Arec = REC["A"]["canonical|b0.67|rc0.15|f0.20"]["MID"][0]
check("K1", abs(Ar - Arec) < 0.005, f"{Ar:.4f} vs record JSON {Arec:.4f} (n={len(npz['D'])})", "|diff| < 0.005")
# ---------------------------------------------------------------- data products per background
DAT = {}
for hk in HS:
    D = arr(hk, "D"); Eh = arr(hk, "E"); W = np.where(Eh < 1e8, 1/Eh**2, 0)
    den = arr(hk, "den"); denr = arr(hk, "den_r"); B = den.sum(0)/denr.sum(0)                  # stacked boost per bin
    DAT[hk] = dict(D=D, W=W, B=B)
st, se = stack(DAT["h070"]["D"], DAT["h070"]["W"])
say("STACK DeltaSigma (Msun/pc2), h = 0.70: " + "  ".join(f"{a:.1f}+-{b:.1f}" for a, b in zip(st, se)))
say("record stack:                         " + "  ".join(f"{REC['stack'][f'b{k}'][0]:.1f}+-{REC['stack'][f'b{k}'][1]:.1f}" for k in range(8)))
dz = [(st[k] - REC["stack"][f"b{k}"][0])/REC["stack"][f"b{k}"][1] for k in range(8)]
RES["stack_h070"] = dict(D=st.tolist(), err=se.tolist(), z_vs_record=dz)
check("K2", all(abs(dz[k]) <= 1.0 for k in range(3, 8)), np.round(dz, 2).tolist(), "|own - record| <= 1 sigma_record in bins 3-7")
for hk in HS: say(f"boost (cluster/random source weight) {hk}: " + " ".join(f"{b:.3f}" for b in DAT[hk]["B"]))
RES["boost"] = {hk: DAT[hk]["B"].tolist() for hk in HS}
# ---------------------------------------------------------------- variant engine
PRED = {}
def P(foot, **kw):
    key = (foot, tuple(sorted(kw.items())))
    if key not in PRED: PRED[key] = np.array([predict(o, A0[foot] if foot != "newton" else 0.0, **kw) for o in MEAS])
    return PRED[key]
def A_of(foot, hkey="h070", boost=False, sub=None, **kw):
    d = DAT[hkey]; D = d["D"]*(d["B"][None, :] if boost else 1.0)
    if sub is not None: D = D - sub[None, :]
    return jk(D, P(foot, hkey=hkey, **kw), d["W"])
ROWS = {}
def row(label, **kw):
    out = {}
    for f in ("canonical", "alt"):
        a = A_of(f, **kw); out[f] = a
    ROWS[label] = out
    say(f"{label:58s} " + "  ".join(f"{f[:3]}: MID {out[f]['MID'][0]:.3f}+-{out[f]['MID'][1]:.3f} (Z {(out[f]['MID'][0]-1)/out[f]['MID'][1]:+.1f})  OUT {out[f]['OUTER'][0]:.3f}+-{out[f]['OUTER'][1]:.3f}" for f in ("canonical", "alt")))
    return out
say("\n=== R0: record recipe on my pipeline (nu_mono, h 0.70, no gas rescale, beta-model, f* 0.20) ===")
r0 = row("R0 record recipe", kernel="nu_mono")
check("K3", abs(r0["canonical"]["MID"][0] - 1.91) <= 0.10 and abs(r0["alt"]["MID"][0] - 1.75) <= 0.10 and abs(r0["canonical"]["OUTER"][0] - 1.01) <= 0.10
      and abs(r0["alt"]["OUTER"][0] - 0.93) <= 0.10 and abs(N - 318) <= 15,
      f"MID {r0['canonical']['MID'][0]:.3f}/{r0['alt']['MID'][0]:.3f} OUTER {r0['canonical']['OUTER'][0]:.3f}/{r0['alt']['OUTER'][0]:.3f} N {N}", "within 0.10 of 1.91/1.75, 1.01/0.93; N 318+-15")
aN = jk(DAT["h070"]["D"], P("newton", kernel="aqual"), DAT["h070"]["W"]); say(f"  Newtonian baryons: MID {aN['MID'][0]:.2f}+-{aN['MID'][1]:.2f}  OUTER {aN['OUTER'][0]:.2f}")
RES["newton_h070"] = aN
say("\n=== one correction at a time (from R0) ===")
row("C1 kernel nu_mono -> AQUAL mu=x/(1+x)", kernel="aqual")
row("C2a eRASS1 gas rescaled to pipeline distances (h 0.70)", kernel="nu_mono", rescale=True)
for hk in ("h0672", "h0686"): row(f"C2 native {hk} (with gas rescale)", kernel="nu_mono", hkey=hk, rescale=True)
for rf, lab in ((10**0.033, "+"), (10**-0.033, "-")): row(f"C3a R500 {lab}0.033 dex (gas at fixed r held)", kernel="nu_mono", rcfac=rf)
row("C3b Mgas500_H", kernel="nu_mono", mg="H"); row("C3b Mgas500_L", kernel="nu_mono", mg="L")
row("C3c gas shape G1 (X-COP measured)", kernel="nu_mono", shape="G1"); row("C3c gas shape G2 (aperture only)", kernel="nu_mono", shape="G2")
row("C4 stars f* 0.30", kernel="nu_mono", fs=0.30); row("C4 stars f* 0.10", kernel="nu_mono", fs=0.10)
row("C5a catalogue miscentring", kernel="nu_mono", miscen=True)
row("C5b data boost", kernel="nu_mono", boost=True)
RES["rows_single"] = {k: v for k, v in ROWS.items()}
# ---------------------------------------------------------------- C3d deep X-ray cross-calibration (ACCEPT Chandra n_e; X-COP M_gas)
ACC = os.path.join(REPO, "..", "_external_data", "cfg686_inputs", "accept")
def hms(s): h_, m_, x_ = map(float, s.split()); return 15*(h_ + m_/60 + x_/3600)
def dms(s): s = s.strip(); sg = -1 if s.startswith("-") else 1; d_, m_, x_ = map(float, s.lstrip("+-").split()); return sg*(d_ + m_/60 + x_/3600)
T1 = {}
for l in list(open(os.path.join(ACC, "table1.tsv")))[3:]:
    p = l.rstrip("\n").split("\t")
    try: T1.setdefault(p[0].strip().upper().replace(" ", "_"), (hms(p[1]), dms(p[2]), float(p[3])))
    except Exception: pass
PROF = {}
for l in open(os.path.join(ACC, "all_profiles.dat")):
    if l.startswith("#"): continue
    p = l.split()
    try: PROF.setdefault(p[0].upper(), []).append([float(x) for x in p[1:4]])
    except ValueError: pass
EALL = [(float(r["RA_XFIT"]), float(r["DEC_XFIT"]), float(r["BEST_Z"]), float(r["MGAS500"])*1e11, float(r["R500"])/1e3) for r in E if np.isfinite(r["MGAS500"]) and r["MGAS500"] > 0]
EA = np.array(EALL)
def nearest(ra, de, z):
    dd = np.degrees(np.arccos(np.clip(np.sin(np.radians(de))*np.sin(np.radians(EA[:, 1])) + np.cos(np.radians(de))*np.cos(np.radians(EA[:, 1]))*np.cos(np.radians(ra - EA[:, 0])), -1, 1)))
    k = np.argmin(dd + 100*(np.abs(EA[:, 2] - z) > 0.03)); return k, dd[k]
ratios = []
for nm, (ra, de, z) in T1.items():
    key = nm if nm in PROF else None
    if key is None and nm.startswith("ABELL_"): key = next((k for k in ("ABELL_" + nm[6:].zfill(4),) if k in PROF), None)
    if key is None: continue
    k, dd = nearest(ra, de, z)
    if dd > 3/60 or abs(EA[k, 2] - z) > 0.03: continue
    P_ = np.array(PROF[key]); P_ = P_[np.argsort(P_[:, 0])]; P_ = P_[P_[:, 2] > 0]
    rin, rout, ne = P_[:, 0], P_[:, 1], P_[:, 2]; R5 = EA[k, 4]; rmax = min(rout.max(), R5)
    sel = rout <= rmax; Macc = np.sum(4/3*np.pi*((rout[sel]*MPC)**3 - (rin[sel]*MPC)**3)*1.17*MP*ne[sel]*1e6)/MSUN   # ACCEPT and eRASS1 both h70 Om0.3
    rr = rout[sel].max(); Mer = np.interp(rr, RG, gas_mass(None, EA[k, 3], R5)/MSUN) - np.interp(rin[sel].min(), RG, gas_mass(None, EA[k, 3], R5)/MSUN)
    if rr/R5 >= 0.3: ratios.append((nm, rr/R5, Macc/Mer))
ra_ = np.array([x[2] for x in ratios]); say(f"\nC3d ACCEPT/eRASS1 gas mass (same shells, r_out >= 0.3 R500): N {len(ra_)}, median {np.median(ra_):.3f}, 16-84% {np.percentile(ra_,16):.2f}-{np.percentile(ra_,84):.2f}")
XR = []
XJ = json.load(open(os.path.join(XD, "xcop_r500_ettori2019.json")))
for nm in sorted(os.listdir(XD)):
    f = os.path.join(XD, nm, f"{nm}_fgas_profile.fits")
    if not os.path.exists(f): continue
    hd = fits.open(f)[1].header; d = fits.open(f)[1].data
    k, dd = nearest(float(hd["RA"]), float(hd["DEC"]), float(hd["REDSHIFT"]))
    if dd > 5/60: continue
    x = np.asarray(d["RADIUS"], float); mgx = np.asarray(d["MGAS"], float); xr = EA[k, 4]/(float(hd["R500"])/1e3)
    XR.append((nm, float(np.exp(np.interp(np.log(xr), np.log(x[mgx > 0]), np.log(mgx[mgx > 0]))))/EA[k, 3], EA[k, 4], float(hd["R500"])/1e3))
xr_ = np.array([x[1] for x in XR]); say(f"C3d X-COP/eRASS1 M_gas(<R500_eRASS1): N {len(xr_)}, median {np.median(xr_) if len(xr_) else np.nan:.3f}; R500 eRASS1/X-COP median {np.median([x[2]/x[3] for x in XR]) if XR else np.nan:.3f}")
GASFAC = float(np.median(np.r_[ra_, xr_])) if len(ra_) + len(xr_) else 1.0
RES["C3d"] = dict(accept=[(a, float(b), float(c)) for a, b, c in ratios], xcop=[(a, float(b), float(c), float(d)) for a, b, c, d in XR], median_all=GASFAC)
row(f"C3d deep X-ray gas factor x{GASFAC:.3f}", kernel="nu_mono", gasfac=GASFAC)
# ---------------------------------------------------------------- C5c two-halo bound, C5d Sigma_crit n(z) bound
import tarfile, io
NZ = {}
with tarfile.open(os.path.join(REPO, "..", "_external_data", "kids_lensing_zsplit", "KiDS1000_SOM_N_of_Z.tar.gz")) as tf:
    for m_ in tf.getmembers():
        if m_.name.endswith("_Nz.asc"):
            t = int(m_.name.split("TOMO")[1][0]); a = np.loadtxt(io.TextIOWrapper(tf.extractfile(m_))); NZ[t] = (a[:, 0], a[:, 1])
TB = [0.1, 0.3, 0.5, 0.7, 0.9, 1.2]
sub_idx = np.arange(0, NS, 20); zsub = np.asarray(S["zb"][sub_idx], float); wsub = np.asarray(S["w"][sub_idx], float)
def isc_of(zl, zs, h=0.70):
    DlM = float(DM(zl, h)); DMs = DM(zs, h); return np.clip((DMs - DlM)/DMs, 0, None)*DlM/(1 + zl)      # proportional to Sigma_crit^-1
FZ = {}
for zl in (0.1, 0.2, 0.3, 0.4, 0.5):
    s_ = (zsub > zl + 0.2) & (zsub <= ZBMAX); i_zb = isc_of(zl, zsub[s_]); t_ = np.digitize(zsub[s_], TB)
    itrue = np.zeros_like(i_zb)
    for t in range(1, 6):
        zz, nn = NZ[t]; itrue[t_ == t] = _trap(nn*isc_of(zl, zz), zz)/_trap(nn, zz)
    FZ[zl] = float((wsub[s_]*i_zb**2).sum()/(wsub[s_]*i_zb*itrue).sum())
say("C5d Sigma_crit bin-n(z) bound F(z_l) (true = measured x F): " + " ".join(f"{k}:{v:.3f}" for k, v in FZ.items()))
RES["C5d_F"] = FZ
zcl = np.array([o["z"] for o in MEAS]); Fcl = np.interp(zcl, list(FZ), list(FZ.values()))
def A_F(foot, F, **kw):
    d = DAT["h070"]; return jk(d["D"]*F[:, None], P(foot, hkey="h070", **kw), d["W"])
ROWS["C5d Sigma_crit bin-n(z) bound"] = {f: A_F(f, Fcl, kernel="nu_mono") for f in ("canonical", "alt")}
say(f"{'C5d Sigma_crit bin-n(z) bound':58s} " + "  ".join(f"{f[:3]}: MID {ROWS['C5d Sigma_crit bin-n(z) bound'][f]['MID'][0]:.3f}+-{ROWS['C5d Sigma_crit bin-n(z) bound'][f]['MID'][1]:.3f}" for f in ("canonical", "alt")))
def twohalo(foot, hkey, **kw):
    d = DAT[hkey]; W = d["W"]; j = BANDS["OUTER"]; Pp = P(foot, hkey=hkey, **kw)
    res_ = (W[:, j]*(d["D"][:, j]*d["B"][None, j] - Pp[:, j])).sum()/W[:, j].sum(); return max(0.0, float(res_))
TH = {f: twohalo(f, "h070", kernel="nu_mono") for f in ("canonical", "alt")}
for f in ("canonical", "alt"):
    a = A_of(f, kernel="nu_mono", sub=np.full(8, TH[f])); ROWS.setdefault("C5c two-halo bound subtracted", {})[f] = a
say(f"{'C5c two-halo bound subtracted':58s} " + "  ".join(f"{f[:3]}: bound {TH[f]:.2f} Msun/pc2, MID {ROWS['C5c two-halo bound subtracted'][f]['MID'][0]:.3f}+-{ROWS['C5c two-halo bound subtracted'][f]['MID'][1]:.3f}" for f in ("canonical", "alt")))
# ---------------------------------------------------------------- primary rebuild and most-favourable corner
say("\n=== PRIMARY rebuild: AQUAL, native h, gas rescaled, beta-model, f* 0.20, data boost, catalogue miscentring ===")
PRIM = {}
for hk in ("h0672", "h0686"):
    PRIM[hk] = row(f"PRIMARY {hk}", kernel="aqual", hkey=hk, rescale=True, boost=True, miscen=True)
say("\n=== most-favourable corner (f* 0.30, Mgas_H, gas factor if > 1, best shape, two-halo bound) ===")
FAV = {}
for hk in ("h0672", "h0686"):
    FAV[hk] = {}
    for f in ("canonical", "alt"):
        best = None
        for sh in ("G0", "G1"):
            kw = dict(kernel="aqual", hkey=hk, rescale=True, miscen=True, fs=0.30, mg="H", gasfac=max(GASFAC, 1.0), shape=sh)
            kw2 = {k: v for k, v in kw.items() if k != "hkey"}; th = twohalo(f, hk, **kw2); a = A_of(f, hkey=hk, boost=True, sub=np.full(8, th), **{k: v for k, v in kw.items() if k != "hkey"})
            if best is None or a["MID"][0] < best[0]["MID"][0]: best = (a, sh, th)
        FAV[hk][f] = dict(A=best[0], shape=best[1], twohalo=best[2])
        say(f"FAVOURABLE {hk} {f:9s}: MID {best[0]['MID'][0]:.3f}+-{best[0]['MID'][1]:.3f} (Z {(best[0]['MID'][0]-1)/best[0]['MID'][1]:+.1f})  OUTER {best[0]['OUTER'][0]:.3f}+-{best[0]['OUTER'][1]:.3f}  shape {best[1]} two-halo {best[2]:.2f}")
# ---------------------------------------------------------------- dust (reported, never graded)
say("\n=== V3 dust sector (reported only): dust tracing the gas, sourcing the AQUAL field ===")
DUST = {}
for f in ("canonical", "alt"):
    kw = dict(kernel="aqual", hkey="h0672", rescale=True, miscen=True)
    def amid(fd): return A_of(f, boost=True, dust=fd, **kw)
    lo, hi = 0.0, 8.0
    for _ in range(18):
        mid_ = 0.5*(lo + hi); (lo, hi) = (mid_, hi) if amid(mid_)["MID"][0] > 1 else (lo, mid_)
    fd = 0.5*(lo + hi); a_need = amid(fd); a_cos = amid(5.364)
    Mg05 = np.median([np.interp(0.5, RG, gas_mass(o, o["Mgas500"]*((float(DM(o["z"], 0.672))/(1 + o["z"]))/DA_lcdm(o["z"]))**2.5, o["R500"]*(float(DM(o["z"], 0.672))/(1 + o["z"]))/DA_lcdm(o["z"]))/MSUN) for o in MEAS])
    Mg10 = np.median([np.interp(1.0, RG, gas_mass(o, o["Mgas500"]*((float(DM(o["z"], 0.672))/(1 + o["z"]))/DA_lcdm(o["z"]))**2.5, o["R500"]*(float(DM(o["z"], 0.672))/(1 + o["z"]))/DA_lcdm(o["z"]))/MSUN) for o in MEAS])
    DUST[f] = dict(f_needed=fd, A_needed=a_need, A_cosmic_5364=a_cos, median_Mgas_0p5=Mg05, median_Mgas_1p0=Mg10, M_dust_0p5=fd*Mg05, M_dust_1p0=fd*Mg10)
    say(f"{f:9s}: needed dust/gas {fd:.2f} (median M_dust(<0.5) {fd*Mg05:.2e}, (<1 Mpc) {fd*Mg10:.2e} Msun; OUTER then {a_need['OUTER'][0]:.3f}+-{a_need['OUTER'][1]:.3f}); "
        f"cosmic ratio 5.364 tracing gas: MID {a_cos['MID'][0]:.3f} OUTER {a_cos['OUTER'][0]:.3f}")
RES["dust"] = DUST
# ---------------------------------------------------------------- coordinator addendum (post-freeze, reported only): L187 settled cold
say("\n=== ADDENDUM (coordinator request, post-freeze, not graded): law + settled cold component, c* = 0.40 (L187), 5.364 x baryons ===")
say("A1 (post-result): measured boost < 1 at every radius = source deficit (masking/blending), not member dilution; a dilution boost is >= 1, so clipped at 1 (= no boost)")
for hk in ("h0672", "h0686"): row(f"A1 PRIMARY {hk} boost clipped at 1", kernel="aqual", hkey=hk, rescale=True, boost=False, miscen=True)
say("baseline of CFG687's 1.91/1.75: the law (nu_mono) on gas x (1 + f*) ONLY, no cold component (cfg687_stack.py law())")
for hk in ("h0672", "h0686"):
    for mode in ("sourced", "newtonian"):
        for uf, ul in ((1.0, "u=1"), (0.443, "u=0.443 (DS_FINAL)")):
            row(f"ADD {hk} cold c*=0.40 {ul} {mode}", kernel="aqual", hkey=hk, rescale=True, boost=True, miscen=True, cold=(0.40, uf, mode))
say(f"  self-consistent R200 of baryons x (1 + 5.364 u): median {np.median(COLD_R200):.2f} Mpc, 16-84% {np.percentile(COLD_R200,16):.2f}-{np.percentile(COLD_R200,84):.2f}")
RES["addendum_R200_median"] = float(np.median(COLD_R200))
RES["addendum_L187"] = {k: v for k, v in ROWS.items() if k.startswith("ADD") or k.startswith("A1 ")}
# ---------------------------------------------------------------- verdict (frozen rule)
def Z(a): return (a["MID"][0] - 1)/a["MID"][1]
zp = {hk: {f: Z(PRIM[hk][f]) for f in ("canonical", "alt")} for hk in PRIM}; zf = {hk: {f: Z(FAV[hk][f]["A"]) for f in ("canonical", "alt")} for hk in FAV}
real = all(zp[hk][f] >= 3 for hk in zp for f in zp[hk]) and all(zf[hk][f] >= 2 for hk in zf for f in zf[hk])
expl = all(abs(zp[hk][f]) < 2 for hk in zp for f in zp[hk])
V = "REAL FAILURE" if real else ("EXPLAINED" if expl else "UNDECIDABLE")
say(f"\nVERDICT (frozen rule): {V}   primary Z_MID {zp}   favourable Z_MID {zf}")
RES.update(verdict=V, Z_primary=zp, Z_favourable=zf, rows={k: v for k, v in ROWS.items()}, favourable=FAV, N=N, gasfac=GASFAC)
npass = sum(ok for _, ok in CHECKS); say(f"F1_CLUSTER_CORES COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
json.dump(RES, open(os.path.join(HERE, f"f1_cluster_cores_results{TAG}.json"), "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
sys.exit(0 if npass == len(CHECKS) else 1)

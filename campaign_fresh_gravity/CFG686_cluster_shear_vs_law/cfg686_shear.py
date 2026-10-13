"""CFG686 (criteria 8cef73ea7): raw KiDS-1000 shear around ACCEPT clusters vs the law's lensing prediction from each cluster's own
Chandra gas. Estimator conventions = record's validated lr_esd_remeasure.py v3 (e2-flipped tangential sign, inverse-Sigma_crit weights).
Distances: raw DESI DR2 BAO D_M/r_d (CFG681 table) x r_d, h r_d = 101.54 Mpc, h = 0.70. No NFW, no LCDM halo.
argv[1] = cached KiDS column dir (from cfg686_extract.py). MUTATE=M1 (cross shear), M2 (randoms only), M3 (a0 -> 0 law)."""
import os, sys, json, math, numpy as np
from scipy.spatial import cKDTree
from scipy.interpolate import PchipInterpolator
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); COLS = sys.argv[1]; MUT = os.environ.get("MUTATE", "")
EXT = os.path.join(LANES, "..", "..", "_external_data", "cfg686_inputs", "accept")
sys.path.insert(0, LANES); import CFG4_common as C4                      # committed nu_mono + both a0 footings
nu_mono, A0 = C4.nu_mono, C4.A0
G = 6.674e-11; c = 2.998e8; MSUN = 1.989e30; MPC = 3.0857e22; MP = 1.6726e-27; KG_PER_MSUN_PC2 = MSUN/(3.0857e16)**2
# ---- distances from raw DESI DR2 BAO (CFG681 table) ----
zb = [0.510, 0.706, 0.934, 1.321, 1.484, 2.330]; DMr = [13.588, 17.351, 21.576, 27.601, 30.512, 38.988]
DHb = 21.863 + (21.863 - 19.455)/(0.706 - 0.510)*(0.510 - 0.295); DMb = np.sqrt(7.942**3/(0.295*DHb))
pch = PchipInterpolator(np.r_[0, 0.295, zb], np.r_[0, DMb, DMr]); RD = 101.54/0.70
def DM(z): z = np.asarray(z, float); return pch(np.minimum(z, 2.33))*RD                     # Mpc (Z_B <= 1.2 so no extrapolation needed)
# ---- clusters: ACCEPT table1 x KiDS boxes, z >= 0.05 ----
def hms(s): h, m, x = map(float, s.split()); return 15*(h + m/60 + x/3600)
def dms(s): s = s.strip(); sg = -1 if s.startswith("-") else 1; d, m, x = map(float, s.lstrip("+-").split()); return sg*(d + m/60 + x/3600)
def norm(n): n = n.upper().replace(" ", "_"); return n
T1 = {}
for l in list(open(os.path.join(EXT, "table1.tsv")))[3:]:
    p = l.rstrip("\n").split("\t")
    try: T1.setdefault(p[0].strip(), (hms(p[1]), dms(p[2]), float(p[3]), float(p[4])))
    except Exception: pass
prof = {}
for l in open(os.path.join(EXT, "all_profiles.dat")):
    if l.startswith("#"): continue
    p = l.split()
    try: prof.setdefault(p[0], []).append([float(x) for x in p[1:14]])
    except ValueError: pass
def match(name):
    n = norm(name)
    cands = [n]
    if n.startswith("ABELL_"):
        num = n[6:]; cands += ["ABELL_" + num.zfill(4), "ABELL_" + num.zfill(4).upper()]
    for k in cands:
        if k in prof: return k
    return None
CL = []
for n, (ra, de, z, T) in T1.items():
    inN = 125 <= ra <= 240 and -6 <= de <= 5; inS = (ra >= 325 or ra <= 60) and -37 <= de <= -25
    k = match(n)
    if (inN or inS) and z >= 0.05 and k: CL.append(dict(name=n, key=k, ra=ra, dec=de, z=z, kT=T))
print(f"ACCEPT clusters in KiDS boxes, z>=0.05, with profiles: {len(CL)}", flush=True)
# ---- sources ----
ra_s = np.load(os.path.join(COLS, "kids_ra.npy")); de_s = np.load(os.path.join(COLS, "kids_dec.npy"))
e1 = np.load(os.path.join(COLS, "kids_e1.npy")).astype(float); e2 = np.load(os.path.join(COLS, "kids_e2.npy")).astype(float)
ws = np.load(os.path.join(COLS, "kids_w.npy")).astype(float); zs = np.load(os.path.join(COLS, "kids_zb.npy")).astype(float)
ok = np.isfinite(ra_s) & np.isfinite(e1) & (ws > 0) & (zs <= 1.2); ra_s, de_s, e1, e2, ws, zs = ra_s[ok], de_s[ok], e1[ok], e2[ok], ws[ok], zs[ok]
def xyz(ra, de): ra, de = np.radians(ra), np.radians(de); return np.c_[np.cos(de)*np.cos(ra), np.cos(de)*np.sin(ra), np.sin(de)]
tree = cKDTree(xyz(ra_s, de_s)); DMs = DM(zs); print(f"sources {len(zs):,}", flush=True)
EDGES = np.logspace(np.log10(0.15), np.log10(3.0), 9); RC = np.sqrt(EDGES[1:]*EDGES[:-1]); M_BIAS = -0.01
def esd(ra, de, zl, cross=False):
    Dl_M = float(DM(zl)); Dl = Dl_M/(1 + zl); th = 3.0/Dl*1.02
    ii = np.array(tree.query_ball_point(xyz(np.array([ra]), np.array([de]))[0], 2*np.sin(th/2)), int)
    if ii.size < 10: return None
    ii = ii[zs[ii] > zl + 0.2]
    dra = (np.radians(ra_s[ii]) - np.radians(ra))*np.cos(np.radians(de)); dra = (dra + np.pi) % (2*np.pi) - np.pi; dde = np.radians(de_s[ii]) - np.radians(de)
    R = np.hypot(dra, dde)*Dl; phi = np.arctan2(dde, dra)
    et = -(e1[ii]*np.cos(2*phi) - e2[ii]*np.sin(2*phi)); ex = -(e1[ii]*np.sin(2*phi) + e2[ii]*np.cos(2*phi))
    Dls = (DMs[ii] - Dl_M)/(1 + zs[ii]); Ds = DMs[ii]/(1 + zs[ii])
    isc = 4*np.pi*G/c**2*(Dl*MPC)*(Dls/Ds); isc = np.clip(isc, 0, None)
    k = np.digitize(R, EDGES) - 1; g = (k >= 0) & (k < 8) & (isc > 0)
    ww = ws[ii]*isc**2; val = (ex if cross else et)/np.where(isc > 0, isc, 1)
    num = np.bincount(k[g], (ww*val)[g], 8); den = np.bincount(k[g], ww[g], 8); var = np.bincount(k[g], (ww**2*val**2)[g], 8)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = num/den/KG_PER_MSUN_PC2/(1 + M_BIAS); s = np.sqrt(var)/den/KG_PER_MSUN_PC2
    return d, s, den, int(g.sum())
# ---- the law's prediction from ACCEPT gas ----
RGRID = np.logspace(-3, np.log10(30), 3000)
U_GRID = np.linspace(0, 1, 4001)
def sigma_proj(rhoL, r, R):
    """RUN3: Sigma(R) = 2 int rho(r) r dr / sqrt(r^2-R^2) with r = R cosh(u) (no endpoint singularity); log-log interpolation of rho."""
    umax = np.arccosh(r[-1]/R); u = U_GRID*umax; rr = R*np.cosh(u)
    lr = np.log(r); pos = rhoL > 0
    rho_u = np.exp(np.interp(np.log(rr), lr[pos], np.log(rhoL[pos])))
    return 2*np.trapz(rho_u*rr*MPC, u)
def law_dsigma(cl, a0, beta_shift=0.0, fstar=0.20):
    P = np.array(prof[cl["key"]]); P = P[np.argsort(P[:, 0])]; rin, rout, ne = P[:, 0], P[:, 1], P[:, 2]
    ok_ = ne > 0; rin, rout, ne = rin[ok_], rout[ok_], ne[ok_]
    # ACCEPT h70 Om0.3 distances -> BAO-raw distances (angles fixed): r scales with D_A ratio, n_e with ratio^-1/2
    zl = cl["z"]; zz = np.linspace(0, zl, 400); E = np.sqrt(0.3*(1 + zz)**3 + 0.7); DA_acc = np.trapz(1/E, zz)*c/(70e3/MPC)/MPC/(1 + zl)
    q = (float(DM(zl))/(1 + zl))/DA_acc; rin, rout, ne = rin*q, rout*q, ne*q**-0.5
    rm = 0.5*(rin + rout); rho = 1.17*MP*ne*1e6                                      # kg/m^3
    # RUN2 (disclosed deviation): the frozen 'last 3 bins' slope is unstable on ACCEPT's fine noisy bins (RUN1: flat/rising -> divergent
    # mass). Slope from a fit over the outer half (in log r) of the measured range; if < 1.5 (unphysical) fall back to 2.0 (beta-model).
    half = rm >= np.exp(0.5*(np.log(rm[0]) + np.log(rm[-1]))); b0 = -np.polyfit(np.log(rm[half]), np.log(rho[half]), 1)[0]
    flag = not (b0 >= 1.5); b0 = 2.0 if flag else b0; b = b0 + beta_shift
    r = RGRID; rho_g = np.interp(r, rm, rho, left=rho[0], right=np.nan)
    out = r > rm[-1]; rho_g[out] = rho[-1]*(r[out]/rm[-1])**(-b); rho_g[r > 3.0] = 0.0
    Mg = np.r_[0, np.cumsum(0.5*(4*np.pi*(r[1:]*MPC)**2*rho_g[1:] + 4*np.pi*(r[:-1]*MPC)**2*rho_g[:-1])*np.diff(r)*MPC)]
    Mb = Mg*(1 + fstar); gb = G*Mb/(r*MPC)**2
    gL = gb*nu_mono(gb/a0) if a0 > 0 else gb
    ML = gL*(r*MPC)**2/G; rhoL = np.gradient(ML, r*MPC)/(4*np.pi*(r*MPC)**2)
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    # M_2D(<R): enclosed projected mass = M_L(<R) + mass of the shell outside R inside the cylinder
    def M2D(R):
        sel = r > R; rr = r[sel]*MPC
        shell = np.trapz(4*np.pi*rr**2*rhoL[sel]*(1 - np.sqrt(1 - (R*MPC/rr)**2)), rr)
        return np.interp(R, r, ML) + shell
    dS = np.array([M2D(R)/(np.pi*(R*MPC)**2) for R in RC]) - Sig
    return dS/KG_PER_MSUN_PC2, dict(beta_out=float(b), beta_fallback=bool(flag), Mgas_1Mpc=float(np.interp(1.0, r, Mg)/MSUN), Mb_1Mpc=float(np.interp(1.0, r, Mb)/MSUN),
                                   ML_1Mpc=float(np.interp(1.0, r, ML)/MSUN), rmax_data=float(rm[-1]))
# ---- self-test: projection of a singular isothermal sphere, DeltaSigma = sigma^2/(2 G R) ----
def _proj(rhoL, ML, r):
    Sig = np.array([sigma_proj(rhoL, r, R) for R in RC])
    M2 = np.array([np.interp(R, r, ML) + np.trapz(4*np.pi*(r[r > R]*MPC)**2*rhoL[r > R]*(1 - np.sqrt(1 - (R/r[r > R])**2)), r[r > R]*MPC) for R in RC])
    return (M2/(np.pi*(RC*MPC)**2) - Sig)/KG_PER_MSUN_PC2
_s = 1e6; _rho = _s**2/(2*np.pi*G*(RGRID*MPC)**2); _ML = 2*_s**2*RGRID*MPC/G
_got = _proj(_rho, _ML, RGRID); _exp = _s**2/(2*G*RC*MPC)/KG_PER_MSUN_PC2
print("SELF-TEST SIS DeltaSigma ratio got/exact:", np.round(_got/_exp, 3).tolist(), flush=True)
# ---- measure ----
rng = np.random.default_rng(686); res = {"mutate": MUT, "clusters": []}
for cl in CL:
    m = esd(cl["ra"], cl["dec"], cl["z"], cross=(MUT == "M1"))
    if m is None: continue
    rnds = []
    for _ in range(40):
        a = rng.uniform(0, 2*np.pi); s = rng.uniform(1.0, 3.0)
        rr = esd((cl["ra"] + s*np.cos(a)/np.cos(np.radians(cl["dec"]))) % 360, cl["dec"] + s*np.sin(a), cl["z"], cross=(MUT == "M1"))
        if rr is not None and rr[3] > 0.5*m[3]: rnds.append(rr[0])
        if len(rnds) >= 20: break
    if m[3] < 200 or len(rnds) < 10: continue                                         # footprint/source-density check
    R0 = np.nanmean(np.array(rnds), 0)
    d = (np.zeros(8) if MUT == "M2" else m[0]) - R0 if MUT != "M2" else np.nanmean(np.array(rnds[:5]), 0) - np.nanmean(np.array(rnds[5:]), 0)
    preds = {}
    for foot, a0 in A0.items():
        for bs in (-0.5, 0.0, 0.5):
            for fs in (0.10, 0.20, 0.30):
                p_, info = law_dsigma(cl, 0.0 if MUT == "M3" else a0, bs, fs); preds[f"{foot}|b{bs:+.1f}|f{fs:.2f}"] = p_.tolist()
    pn, info = law_dsigma(cl, 0.0)
    cl2 = dict(cl, n_src=m[3], n_rand=len(rnds), dsig=d.tolist(), err=m[1].tolist(), pred=preds, newton=pn.tolist(), info=info)
    res["clusters"].append(cl2)
    print(f"  {cl['name']:22s} z={cl['z']:.3f} src={m[3]:6d} rand={len(rnds)}  ΔΣ(0.15-3 Mpc) = " + " ".join(f"{x:6.0f}" for x in d) +
          f"   σ≈{np.nanmedian(m[1]):.0f}   law(can,prim)= " + " ".join(f"{x:6.0f}" for x in preds['canonical|b+0.0|f0.20']), flush=True)
# ---- stack + bands ----
BANDS = {"INNER": [0, 1, 2], "MID": [3, 4, 5], "OUTER": [6, 7]}
cls = res["clusters"]; D_ = np.array([x["dsig"] for x in cls]); E_ = np.array([x["err"] for x in cls]); W_ = np.where(np.isfinite(E_) & (E_ > 0), 1/E_**2, 0); D_ = np.nan_to_num(D_)
def bandA(key, idx):
    P_ = np.array([x["pred"][key] for x in idx]) if key != "newton" else np.array([x["newton"] for x in idx])
    return P_
def A_of(sel, key):
    P_ = bandA(key, [cls[i] for i in sel]); out = {}
    for b, j in BANDS.items():
        num = (W_[sel][:, j]*D_[sel][:, j]).sum(); den = (W_[sel][:, j]*P_[:, j]).sum(); out[b] = num/den if den != 0 else np.nan
    return out
allsel = np.arange(len(cls)); rb = np.random.default_rng(1)
summary = {}
for key in list(cls[0]["pred"].keys()) + ["newton"]:
    A = A_of(allsel, key); boots = [A_of(rb.integers(0, len(cls), len(cls)), key) for _ in range(1000)]
    sig = {b: float(np.nanstd([bb[b] for bb in boots])) for b in BANDS}
    summary[key] = {b: [float(A[b]), sig[b]] for b in BANDS}
stackD = (W_*D_).sum(0)/W_.sum(0); stackE = 1/np.sqrt(W_.sum(0))
res["stack"] = dict(R=RC.tolist(), dsig=stackD.tolist(), err=stackE.tolist()); res["A"] = summary
print("\nSTACK ΔΣ (M☉/pc²) at R =", np.round(RC, 2).tolist()); print("  obs  ", np.round(stackD, 1).tolist()); print("  ±    ", np.round(stackE, 1).tolist())
for key in ["canonical|b+0.0|f0.20", "alt|b+0.0|f0.20", "newton"]:
    print(f"  A ({key}): " + "  ".join(f"{b} {v[0]:.2f}±{v[1]:.2f}" for b, v in summary[key].items()))
def verdict(key):
    s = summary[key]; z = {b: (v[0] - 1)/v[1] if v[1] > 0 else 0 for b, v in s.items()}
    if any(z[b] <= -2 for b in z): return "LAW OVERPREDICTS"
    if z["OUTER"] >= 2: return "EXTENDED EXCESS"
    if z["INNER"] >= 2 or z["MID"] >= 2: return "CORE EXCESS"
    if all(abs(z[b]) < 2 for b in z): return "LAW SUFFICES"
    return "MIXED"
v = {f: verdict(f"{f}|b+0.0|f0.20") for f in A0}; res["verdict"] = v
br = {k: verdict(k) for k in summary if k != "newton"}; res["verdict_brackets"] = br
print("\nVERDICT (primary bracket):", v, "\n  across brackets:", {x: list(br.values()).count(x) for x in set(br.values())})
json.dump(res, open(os.path.join(HERE, "cfg686_results" + (f"_MUTATE_{MUT}" if MUT else "") + ".json"), "w"), indent=1, default=float)

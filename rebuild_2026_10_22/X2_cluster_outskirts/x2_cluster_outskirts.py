"""X2_cluster_outskirts (criteria 40624db7e9 + A1): does F1's "any added cold profile that fixes MID overshoots the outskirts"
survive (a) the measured r^-3 outskirt gas, (b) Mgas terciles, (c) the external field, (d) reduced shear, (e) the null-test
systematics; and does a fixed-form published component pass on the corrected baseline?
Inputs: x2_replay_percluster.npz (this lane's replay of F1's measurement, equal to F1's cache: R1/R2), F1's own functions exec'd
read-only from F1_cluster_cores/f1_cluster_cores.py, F2's AQUAL EFE solver (read-only import), CFG949's R930 debris block
(exec'd read-only), CFG687's per-cluster npz (K6 only).  Usage: x2_cluster_outskirts.py [--mutate].
--mutate: cross shear replaces the data, EFE ratio inverted, reduced-shear correction sign flipped (K0, K4, K5 must FAIL).
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed."""
import os, sys, json, math, time, hashlib, resource
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import cumulative_trapezoid
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"x2_cluster_outskirts{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"mutate": MUT}; CHECKS = []
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
def guard(tag):
    g = rss()
    if g > 0.95: say(f"RSS GUARD {g:.3f} GB at {tag} -> abort"); sys.exit(3)
# ============================================================== F1's own functions (exec'd read-only from its source text)
F1SRC = os.path.join(REB, "F1_cluster_cores", "f1_cluster_cores.py"); TXT = open(F1SRC).read(); RES["f1_source_sha256"] = sha(F1SRC)
def cut(a, b): i = TXT.index(a); j = TXT.index(b, i); return TXT[i:j]
NSF = {"np": np, "os": os, "sys": sys, "REPO": REPO, "_trap": np.trapz}
from scipy.interpolate import PchipInterpolator; NSF["PchipInterpolator"] = PchipInterpolator
exec(cut("G = 6.674e-11", "# ---------------------------------------------------------------- sources"), NSF)        # constants, A0, C4, kernels, DM, DA_lcdm, HS
exec(cut("EDGES = np.logspace", "def gather("), NSF)                                                                     # EDGES, RC, M_BIAS, BANDS
exec(cut("RG = np.logspace(-3", "# SIS self-test (K4)"), NSF)                                                           # RG, RF, UU, project, offset, dsig_from_sig, at_bins
exec(cut("def gas_mass(", "# ---------------------------------------------------------------- K5"), NSF)               # gas_mass, cold_mass, predict
G, MSUN, MPC, KG_PC2, A0 = NSF["G"], NSF["MSUN"], NSF["MPC"], NSF["KG_PC2"], NSF["A0"]
RG, RF, UU, RC, BANDS = NSF["RG"], NSF["RF"], NSF["UU"], NSF["RC"], NSF["BANDS"]
DM, DA_lcdm, g_aqual_sph, project, offset, dsig_from_sig, at_bins = (NSF[k] for k in ("DM", "DA_lcdm", "g_aqual_sph", "project", "offset", "dsig_from_sig", "at_bins"))
gas_mass_f1, predict_f1 = NSF["gas_mass"], NSF["predict"]
_trap = np.trapz; RM = RG*MPC
FEET = ("canonical", "alt"); HK = ("h0672", "h0686"); HV = {"h0672": 0.672, "h0686": 0.686}; HI = {"h070": 0, "h0672": 1, "h0686": 2}
CELLS = [(f, h) for f in FEET for h in HK]
# ============================================================== data: the replay (equal to F1's cache by R1/R2)
NPZ = os.path.join(HERE, "x2_replay_percluster.npz"); RES["replay_npz_sha256"] = sha(NPZ); X = np.load(NPZ)
N = len(X["z"]); CL = [dict(name=str(X["name"][i]), ra=float(X["ra"][i]), dec=float(X["dec"][i]), z=float(X["z"][i]), Mgas500=float(X["Mgas500"][i]),
                         MgL=float(X["MgL"][i]), MgH=float(X["MgH"][i]), R500=float(X["R500"][i]), off_deg=float(X["off_deg"][i])) for i in range(N)]
order = np.argsort(X["ra"]); PATCH = np.empty(N, int); PATCH[order] = np.arange(N)*30//N
ALL = np.ones(N, bool)
_q = np.quantile(X["Mgas500"], [1/3, 2/3]); TID = np.digitize(X["Mgas500"], _q); TERC = {f"T{t+1}": TID == t for t in range(3)}
RES["tercile_median_Mgas500"] = {k: float(np.median(X["Mgas500"][v])) for k, v in TERC.items()}
DAT = {}
for hk in HK:
    i = HI[hk]; Dt = X["D"][:, i]; Et = X["E"][:, i]; Dx = X["Dx"][:, i]; Ex = X["Ex"][:, i]
    if MUT: Dt, Et = Dx, Ex                                                   # MUTATE: cross shear as the data
    W = np.where(Et < 1e8, 1/Et**2, 0); Wx = np.where(Ex < 1e8, 1/Ex**2, 0)
    B = X["den"][:, i].sum(0)/X["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=Dt, W=W, B=B, Dx=Dx, Wx=Wx, DRR=X["DRR"][:, i], m2=X["den"][:, i], m=X["m3to8"][:, i])  # m: (N, 6, 8) = m3..m8
say(f"replay npz {RES['replay_npz_sha256'][:16]}..., clusters {N}; terciles (catalogue Mgas500) medians "
    + " ".join(f"{k} {v:.2e}" for k, v in RES["tercile_median_Mgas500"].items()))
# ============================================================== statistics (F1's A_band / jk, H2's chi2, (e) systematics)
PB = [3, 4, 5, 6, 7]; HARTLAP = (30 - len(PB) - 2)/29
def Dused(hk, conv, key="D"):
    d = DAT[hk]; return d[key]*(d["B"][None, :] if conv == "boost" else 1.0)
def A_band(D, P, W, sel): return {b: float((W[sel][:, j]*D[sel][:, j]).sum()/(W[sel][:, j]*P[sel][:, j]).sum()) for b, j in BANDS.items()}
def jk(D, P, W, sel=ALL):
    full = A_band(D, P, W, sel); reps = [A_band(D, P, W, sel & (PATCH != p)) for p in range(30) if (sel & (PATCH != p)).sum() < sel.sum()]
    return {b: (full[b], float(np.sqrt((len(reps) - 1)/len(reps)*np.sum((np.array([r[b] for r in reps]) - np.mean([r[b] for r in reps]))**2)))) for b in full}
def resid(D, P, W, sel):
    return (W[sel][:, PB]*(D[sel][:, PB] - P[sel][:, PB])).sum(0)/W[sel][:, PB].sum(0)
def stats(hk, P, conv="boost", sel=ALL, sysx=False):
    """A per band (val, sigma_jk, sigma_tot), Z_MID/Z_OUT (tot if sysx), chi2 (bins 3-7, jackknife cov + Hartlap; + null templates if sysx)."""
    d = DAT[hk]; D = Dused(hk, conv); W = d["W"]; a = jk(D, P, W, sel)
    Dx = Dused(hk, conv, "Dx"); Drr = Dused(hk, conv, "DRR")
    ax = A_band(Dx, P, W, sel); arr = A_band(Drr, P, W, sel)
    out = {}
    for b in BANDS:
        st = a[b][1]; tot = math.sqrt(st**2 + ax[b]**2 + arr[b]**2)
        out[b] = dict(A=a[b][0], s_jk=st, s_tot=tot, A_x=ax[b], A_RR=arr[b])
    use = "s_tot" if sysx else "s_jk"
    out["Z_MID"] = (out["MID"]["A"] - 1)/out["MID"][use]; out["Z_OUT"] = (out["OUTER"]["A"] - 1)/out["OUTER"][use]
    s0 = resid(D, P, W, sel); pats = [p for p in range(30) if (sel & (PATCH != p)).sum() < sel.sum()]
    reps = np.array([resid(D, P, W, sel & (PATCH != p)) for p in pats]); n = len(pats)
    Cv = (n - 1)/n*(reps - reps.mean(0)).T @ (reps - reps.mean(0))
    out["chi2_stat"] = float(HARTLAP*s0 @ np.linalg.solve(Cv, s0))
    tx = resid(Dx, 0*P, W, sel); tr = resid(Drr, 0*P, W, sel); Ct = Cv + np.outer(tx, tx) + np.outer(tr, tr)
    out["chi2_sys"] = float(HARTLAP*s0 @ np.linalg.solve(Ct, s0)); out["chi2"] = out["chi2_sys"] if sysx else out["chi2_stat"]
    out["resid"] = s0.tolist()
    return out
# ============================================================== projector (F1's, with log rho floored in every cell: truncation-aware)
def project_floor(rho, r=RG):
    lr = np.log(r); lrho = np.log(np.where(rho > 0, rho, 1e-300))
    umax = np.arccosh(r[-1]/RF); u = UU[None, :]*umax[:, None]; rr = RF[:, None]*np.cosh(u)
    Sig = 2*_trap(np.exp(np.interp(np.log(rr), lr, lrho))*rr*MPC, u, axis=1)
    return Sig
def offset_floor(Sig, d):
    if d <= 1e-4: return Sig
    ph = np.linspace(0, np.pi, 181); Rp = np.sqrt(RF[:, None]**2 + d**2 + 2*RF[:, None]*d*np.cos(ph[None, :]))
    return _trap(np.exp(np.interp(np.log(Rp), np.log(RF), np.log(np.maximum(Sig, 1e-300)))), ph, axis=1)/np.pi
def sig_bins(Sig): return np.exp(np.interp(np.log(RC), np.log(RF), np.log(np.maximum(Sig, 1e-300))))
# ============================================================== gas profiles (G0 = F1's; P = CFG814; F = CFG814 bracket F; R5 = r^-3 from R500)
def gas(Mg500, R500, shape):
    """returns (M(<r) kg, rho kg/m^3) on RG; normalised to Mg500 at R500, cut at 3 Mpc (F1 G0 recipe)."""
    r = RG; rc = 0.15*R500; beta = 2/3; sh = (1 + (r/rc)**2)**(-1.5*beta)                     # F1's expression, bit-identical
    if shape in ("P", "F", "R5"):
        Rm = R500 if shape == "R5" else 2.2*R500; sm = (1 + (Rm/rc)**2)**(-1.5*beta)
        sh = np.where(r > Rm, sm*(r/Rm)**-3.0, sh)
        if shape == "F": s2 = sm*2.0**-3.0; sh = np.where(r > 2*Rm, s2*(r/(2*Rm))**-2.0, sh)
    sh = np.where(r > 3.0, 0.0, sh)
    dm = 4*np.pi*(r*MPC)**2*sh; M = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r*MPC))]
    nrm = Mg500*MSUN/np.interp(R500, r, M); return M*nrm, sh*nrm
# ============================================================== EFE: F2's exact AQUAL point mass in a uniform field (read-only import)
sys.path.insert(0, os.path.join(REB, "F2_outer_lensing")); import f2_aqual as AQ
RES["f2_aqual_sha256"] = sha(os.path.join(REB, "F2_outer_lensing", "f2_aqual.py"))
import csv
CH = list(csv.DictReader(open(os.path.join(REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv"))))
MED = {k: float(np.median([float(r[f"log_eN_{k}"]) for r in CH])) for k in ("noclu", "maxclu")}
YE = {f: {"noclu": 10**MED["noclu"]*1.2e-10/A0[f], "maxclu": 10**MED["maxclu"]*1.2e-10/A0[f], "p2cat": {"canonical": 6.56e-5, "alt": 5.43e-5}[f]} for f in FEET}
RES["chae21_medians"] = MED; RES["y_e"] = YE
CTAB = {}
def ctable(sol):
    s = np.asarray(sol["r"]); M = np.asarray(sol["M"]); Ci = M/AQ.M_iso(s)
    return dict(ls=np.log(s), C=Ci, Mlast=float(M[-1]), s0=float(s[0]), s1=float(s[-1]), x_e=sol["x_e"], iters=sol["iters"], resid=sol["resid"])
def Cof(tab, s):
    s = np.asarray(s, float); c = np.interp(np.log(np.clip(s, tab["s0"], tab["s1"])), tab["ls"], tab["C"])
    c = np.where(s < tab["s0"], 1.0, c); c = np.where(s > tab["s1"], tab["Mlast"]/AQ.M_iso(np.maximum(s, tab["s1"])), c)
    return 1.0/c if MUT else c                                                  # MUTATE: inverted ratio
for f in FEET:
    for k in ("noclu", "maxclu", "p2cat"):
        t1 = time.time(); CTAB[(f, k)] = ctable(AQ.solve_efe(YE[f][k], maxit=3000))          # A3
        tb = CTAB[(f, k)]; say(f"  EFE solve {f} {k}: y_e {YE[f][k]:.3e} x_e {tb['x_e']:.4f} iters {tb['iters']} last change {tb['resid']:.1e} "
                              f"min C {tb['C'].min():.4f} [{time.time()-t1:.0f} s]")
        guard("efe")
t1 = time.time(); TISO = ctable(AQ.solve_efe(1e-6, maxit=3000)); sg = np.array([0.1, 0.3, 1, 3, 10])
k4i = float(np.max(np.abs(np.interp(np.log(sg), TISO["ls"], TISO["C"]) - 1))); say(f"  EFE isolated-limit solve y_e 1e-6 [{time.time()-t1:.0f} s]")
sgrid = np.logspace(-2, 4, 600); k4ii = max(float(np.max(Cof(CTAB[k], sgrid))) for k in CTAB)
check("K4", k4i <= 1e-3 and k4ii <= 1 + 2e-3 and abs(MED["noclu"] + 3.215) <= 0.005,
      f"(i) max|C-1| at y_e 1e-6 {k4i:.1e}; (ii) max C {k4ii:.4f}; (iii) noclu median {MED['noclu']:.4f} (maxclu {MED['maxclu']:.4f})",
      "(i) <= 1e-3, (ii) <= 1.002, (iii) -3.215 +- 0.005")
# ============================================================== CFG949 debris (R930 block + supply/cold_profile exec'd read-only)
C949 = os.path.join(LANES, "CFG949_clusters_untethered", "cfg949.py"); T9 = open(C949).read(); RES["cfg949_source_sha256"] = sha(C949)
N9 = {"np": np, "math": math, "json": json, "os": os, "LANES": LANES, "brentq": brentq, "cumulative_trapezoid": cumulative_trapezoid,
      "MSUN": MSUN, "RKPC": RG*1e3}
def cut9(a, b): i = T9.index(a); j = T9.index(b, i); return T9[i:j]
exec(cut9("# ============================================================================ native cosmology: R930 family",
          "# ============================================================================ R932 family"), N9)
exec(cut9("def supply(", "def build_cold("), N9)
FBN = N9["FBN"]
def debris(Mg3_msun, Mg500_msun, z):
    Mta, f = N9["supply"]("S-cen", Mg3_msun, Mg500_msun, 0.20); c, rs, rb, zc = N9["prof930"](Mta, z, 3000.0, "rta")
    return N9["cold_profile"](Mta, c, rs, rb), dict(Mta=Mta, fret=f, c=c, rs=rs, rb=rb, zc=zc)
# ============================================================== the model
def model(cl, foot, hk, gasshape="G0", efe=None, efe_mode="tot", red=False, comp=None, lam=0.0, Pdat=None):
    """returns (P at bins Msun/pc^2 incl. reduced shear if red, Sigma at bins kg/m^2, extra) for one cluster.
    comp: None | 'GS' (lam x gas, sources AQUAL) | 'PS' (point mass lam x Mg500, sources AQUAL) | 'PNunit' (law + unit Newtonian point mass
    returned separately) | 'FPS' (sources AQUAL) | 'DEB-rule' / 'DEB-committed' (B0: Newtonian baryons + debris) | 'DEB+law'."""
    h = HV[hk]; a0 = A0[foot]; q = (float(DM(cl["z"], h))/(1 + cl["z"]))/DA_lcdm(cl["z"])
    Mg500 = cl["Mgas500"]*q**2.5; R500 = cl["R500"]*q
    Mg, rho_g = gas(Mg500, R500, gasshape); Mb = Mg*(1 + 0.20)
    extra = {}; Mpt = 0.0; Msrc = Mb.copy(); Mnewt = 0.0
    if comp == "GS": Msrc = Msrc + lam*Mg
    if comp == "PS": Mpt = lam*Mg500*MSUN; Msrc = Msrc + Mpt
    if comp == "FPS":
        dmd = 4*np.pi*RM**2*8.511380382023764*rho_g*np.exp(-RG/0.43)
        Md = np.r_[0, np.cumsum(0.5*(dmd[1:] + dmd[:-1])*np.diff(RM))]; Msrc = Msrc + Md; extra["Mfps_0p5"] = float(np.interp(0.5, RG, Md)/MSUN)
    if comp in ("DEB-rule", "DEB-committed", "DEB+law"):
        Mg_sup = Mg if comp != "DEB-committed" else gas(Mg500, R500, "G0")[0]
        Mc, meta = debris(float(Mg_sup[-1]/MSUN), Mg500, cl["z"]); Mnewt = Mc; extra.update(meta)
    if comp in ("DEB-rule", "DEB-committed"):
        g = G*(Mb + Mnewt)/RM**2                                                     # B0: Newtonian, no law (footing-independent)
    else:
        gN = G*Msrc/RM**2; g = g_aqual_sph(gN, a0)
        if efe is not None:
            tab = CTAB[(foot, efe)]
            if efe_mode == "tot": s = RG/(math.sqrt(G*float(np.interp(3.0, RG, Msrc))/a0)/MPC)
            else: s = RG/(np.sqrt(G*np.maximum(Msrc, 1e-30)/a0)/MPC)
            g = g*Cof(tab, s)
        g = g + G*Mnewt/RM**2
    ML = g*RM**2/G - Mpt
    rho = np.gradient(ML, RM)/(4*np.pi*RM**2)
    Sig = project_floor(rho); d = np.radians(cl["off_deg"])*float(DM(cl["z"], h))/(1 + cl["z"])
    So = offset_floor(Sig, d); ds = dsig_from_sig(So); P = at_bins(ds)/KG_PC2; Sb = sig_bins(So)
    if Mpt > 0: P = P + np.where(RC > d, Mpt/(np.pi*(RC*MPC)**2), 0.0)/KG_PC2
    unit = np.where(RC > d, Mg500*MSUN/(np.pi*(RC*MPC)**2), 0.0)/KG_PC2            # PN: Newtonian point mass per unit lam
    extra["neg_rho_frac"] = float(np.mean(rho < 0)); extra["Mg3_over_Mg500"] = float(Mg[-1]/(Mg500*MSUN))
    extra["gas_share_beyond_R500"] = float(1 - Mg500*MSUN/Mg[-1])
    return P, Sb, unit, extra
def redfac(hk, i, Sb):
    m2 = DAT[hk]["m2"][i]; m = DAT[hk]["m"][i]; ok = m2 > 0
    f = np.ones(8); kap = np.zeros(8)
    f[ok] = 1 + sum(Sb[ok]**(p + 1)*m[p][ok]/m2[ok] for p in range(6)); kap[ok] = Sb[ok]*m[0][ok]/m2[ok]
    if MUT: f = 2 - f                                                               # MUTATE: sign of the correction flipped
    return f, kap
PRED = {}
def stack_model(foot, hk, **kw):
    key = (foot, hk, tuple(sorted(kw.items())))
    if key in PRED: return PRED[key]
    red = kw.get("red", False); P = np.empty((N, 8)); U = np.empty((N, 8)); KAP = np.empty((N, 8)); FAC = np.ones((N, 8)); EX = []
    for i, cl in enumerate(CL):
        p, sb, u, ex = model(cl, foot, hk, **kw)
        if red: f, kap = redfac(hk, i, sb); p = p*f; u = u*f; FAC[i] = f; KAP[i] = kap
        P[i] = p; U[i] = u; EX.append(ex)
    PRED[key] = (P, U, FAC, KAP, EX); guard("stack_model"); return PRED[key]
# ============================================================== K2, K3, K7 (implementation checks; no data)
cl0 = CL[int(np.argmin(X["R500"]))]; h = 0.672; q = (float(DM(cl0["z"], h))/(1 + cl0["z"]))/DA_lcdm(cl0["z"])
Mg0 = gas_mass_f1(cl0, cl0["Mgas500"]*q**2.5, cl0["R500"]*q, "G0"); gl = g_aqual_sph(G*Mg0*1.2/RM**2, A0["canonical"]); ML = gl*RM**2/G
rho = np.gradient(ML, RM)/(4*np.pi*RM**2); s_f1 = project(rho)[0]; s_fl = project_floor(rho)
k2a = float(np.max(np.abs(s_fl/s_f1 - 1)))
a_s = 1.45; Msph = 1e14*MSUN; Mu = Msph*np.minimum(RG/a_s, 1.0)**3; rho_u = np.gradient(Mu, RM)/(4*np.pi*RM**2)
ds_num = at_bins(dsig_from_sig(project_floor(rho_u)))
Rm_ = RC*MPC; am = a_s*MPC; inside = RC < a_s
M2 = np.where(inside, Msph*(1 - np.clip(1 - (RC/a_s)**2, 0, None)**1.5), Msph); Sg = np.where(inside, 3*Msph/(2*np.pi*am**3)*np.sqrt(np.clip(am**2 - Rm_**2, 0, None)), 0)
ds_an = M2/(np.pi*Rm_**2) - Sg; k2b = float(np.max(np.abs(ds_num[3:]/ds_an[3:] - 1)))
check("K2", k2a <= 1e-12 and k2b <= 0.01, f"floored vs F1 projector {k2a:.1e}; truncated sphere bins 3-7 max dev {k2b:.4f}", "<= 1e-12; <= 0.01")
R5_ = cl0["R500"]*q; MgP, _ = gas(cl0["Mgas500"]*q**2.5, R5_, "P"); MgG, _ = gas(cl0["Mgas500"]*q**2.5, R5_, "G0")
inn = RG <= 2.2*R5_; k3a = float(np.max(np.abs(MgP[inn] - Mg0[inn])/np.maximum(Mg0[inn], 1e-300))) if inn.any() else 0.0
k3g = float(np.max(np.abs(MgG/np.maximum(Mg0, 1e-300) - 1)[RG > 1e-3]))
_, rhoP = gas(cl0["Mgas500"]*q**2.5, R5_, "P"); sel3 = (RG > 2.3*R5_) & (RG < 2.9)
slope = float(np.polyfit(np.log(RG[sel3]), np.log(rhoP[sel3]), 1)[0]) if sel3.sum() > 5 else -3.0
k3n = abs(np.interp(R5_, RG, MgP)/(cl0["Mgas500"]*q**2.5*MSUN) - 1)
check("K3", max(k3a, k3g) <= 1e-12 and abs(slope + 3) <= 1e-3 and k3n <= 1e-9,
      f"P=G0 inside 2.2R500 {k3a:.1e}; my G0 = F1 gas_mass {k3g:.1e}; slope beyond {slope:.5f}; M(<R500) rel {k3n:.1e}", "<= 1e-12; -3 +- 1e-3; <= 1e-9")
rho0 = 1e-24; rcF = 0.43; dmd = 4*np.pi*RM**2*8.511380382023764*rho0*np.exp(-RG/rcF); Md = np.r_[0, np.cumsum(0.5*(dmd[1:] + dmd[:-1])*np.diff(RM))]
xx = RG/rcF; Man = 8.511380382023764*rho0*8*np.pi*(rcF*MPC)**3*(1 - np.exp(-xx)*(1 + xx + xx**2/2)); okk = RG > 0.05
k7 = float(np.max(np.abs(Md[okk]/Man[okk] - 1)))
check("K7", k7 <= 1e-4, f"FPS missing mass vs analytic (r > 0.05 Mpc) {k7:.1e}", "<= 1e-4")
# ============================================================== K6: CFG949 B0 primary on CFG687's own inputs
P7 = np.load(os.path.join(LANES, "CFG687_erass1_shear_stack", "cfg687_percluster.npz"))
D7 = np.nan_to_num(np.asarray(P7["D"], float)); E7 = np.asarray(P7["E"], float); W7 = np.where(E7 > 0, 1/E7**2, 0); N7 = len(D7)
o7 = np.argsort(P7["ra"]); PA7 = np.empty(N7, int); PA7[o7] = np.arange(N7)*30//N7
PB0 = np.empty((N7, 8))
for i in range(N7):
    Mg7 = gas_mass_f1(None, float(P7["mg"][i]), float(P7["R500"][i]), "G0"); Mc7, _ = debris(float(Mg7[-1]/MSUN), float(P7["mg"][i]), float(P7["z"][i]))
    rho7 = np.gradient(Mg7*1.2 + Mc7, RM)/(4*np.pi*RM**2); PB0[i] = at_bins(dsig_from_sig(project_floor(rho7)))/KG_PC2
def jk7(D, P, W):
    full = A_band(D, P, W, np.ones(N7, bool)); reps = [A_band(D, P, W, PA7 != p) for p in range(30)]
    return {b: (full[b], float(np.sqrt(29/30*np.sum((np.array([r[b] for r in reps]) - np.mean([r[b] for r in reps]))**2)))) for b in full}
a7 = jk7(D7, PB0, W7)
check("K6", abs(a7["MID"][0] - 1.011) <= 0.02 and abs(a7["OUTER"][0] - 1.047) <= 0.02,
      f"CFG949 B0 on CFG687 inputs: MID {a7['MID'][0]:.4f}+-{a7['MID'][1]:.4f} OUTER {a7['OUTER'][0]:.4f}+-{a7['OUTER'][1]:.4f} (N {N7})",
      "1.011 / 1.047 within 0.02")
RES["K6"] = a7
# ============================================================== step 0: C0 = F1 PRIMARY (and F1 predict() verbatim equality)
F1J = json.load(open(os.path.join(REB, "F1_cluster_cores", "f1_cluster_cores_results.json")))
H2CHI = {("h0672", "canonical"): 33.4, ("h0672", "alt"): 27.3, ("h0686", "canonical"): 41.8, ("h0686", "alt"): 34.9}
dev0, devc, devp = [], [], []
ROWS = {}
def run(label, conv_list=("boost", "clip"), sysx=False, sel=ALL, **kw):
    out = {}
    for conv in conv_list:
        out[conv] = {}
        for f, hk in CELLS:
            P = stack_model(f, hk, **kw)[0]; out[conv][f"{f}|{hk}"] = stats(hk, P, conv, sel, sysx)
    return out
def pn(foot, hk, conv, sysx, sel=ALL, **kw):
    """needed Newtonian point mass: lam s.t. A_MID = 1 (closed form, A linear in lam); A_OUTER, Z_OUT, chi2 there."""
    P, U = stack_model(foot, hk, **kw)[:2]; d = DAT[hk]; D = Dused(hk, conv); W = d["W"]; j = BANDS["MID"]
    num = (W[sel][:, j]*D[sel][:, j]).sum() - (W[sel][:, j]*P[sel][:, j]).sum(); den = (W[sel][:, j]*U[sel][:, j]).sum(); lam = float(num/den)
    if lam <= 0: return dict(lam=lam, applicable=False, Z_OUT=float("nan"), A_OUT=float("nan"), chi2=float("nan"))
    s = stats(hk, P + lam*U, conv, sel, sysx)
    return dict(lam=lam, applicable=True, A_MID=s["MID"]["A"], A_OUT=s["OUTER"]["A"], s_OUT=s["OUTER"]["s_tot" if sysx else "s_jk"],
                Z_OUT=s["Z_OUT"], chi2=s["chi2"])
def status(zs):
    z = [x for x in zs]; over = [(not math.isnan(v)) and v <= -2 for v in z]
    return "OVER" if all(over) else ("NONE" if not any(over) else "SPLIT")
OV = {}
def config(label, sysx=False, sel=ALL, report=True, **kw):
    r = run(label, sysx=sysx, sel=sel, **kw); r["kw"] = {k: v for k, v in kw.items()}; r["sys"] = sysx
    r["PN"] = {conv: {f"{f}|{hk}": pn(f, hk, conv, sysx, sel, **kw) for f, hk in CELLS} for conv in ("boost", "clip")}
    r["PN_status"] = {conv: status([r["PN"][conv][c]["Z_OUT"] for c in r["PN"][conv]]) for conv in ("boost", "clip")}
    EX = stack_model("canonical", "h0672", **kw)[4]; r["gas_share_beyond_R500_median"] = float(np.median([e["gas_share_beyond_R500"] for e in EX]))
    r["neg_rho_frac_max"] = float(max(e["neg_rho_frac"] for e in EX))
    ROWS[label] = r
    if report:
        say(f"{label}  [gas beyond R500: {r['gas_share_beyond_R500_median']:.2f} of M(<3 Mpc); PN status {r['PN_status']['boost']} (clip {r['PN_status']['clip']})]")
        for f, hk in CELLS:
            c = r["boost"][f"{f}|{hk}"]; cc = r["clip"][f"{f}|{hk}"]; p = r["PN"]["boost"][f"{f}|{hk}"]
            say(f"   {f[:3]} {hk}: MID {c['MID']['A']:.3f}+-{c['MID']['s_tot' if sysx else 's_jk']:.3f} (Z {c['Z_MID']:+.2f})  OUT {c['OUTER']['A']:.3f}+-"
                f"{c['OUTER']['s_tot' if sysx else 's_jk']:.3f} (Z {c['Z_OUT']:+.2f})  INNER {c['INNER']['A']:.2f}  chi2 {c['chi2']:.1f}"
                f"  | PN lam {p['lam']:.3f} -> OUT {p.get('A_OUT', float('nan')):.3f} (Z {p['Z_OUT']:+.2f}) chi2 {p['chi2']:.1f}"
                f"  | clip MID {cc['MID']['A']:.3f} OUT {cc['OUTER']['A']:.3f} chi2 {cc['chi2']:.1f}")
    return r
say("\n=== STEP 0: C0 = F1 PRIMARY (AQUAL, native h, gas rescaled, beta-model, f* 0.20, boost, miscentring) ===")
for f, hk in CELLS:
    P = stack_model(f, hk)[0]
    for i in range(0, N, 40):
        pf = predict_f1(CL[i], A0[f], kernel="aqual", hkey=hk, rescale=True, miscen=True); devp.append(float(np.max(np.abs(P[i]/pf - 1))))
c0 = config("C0 (F1 PRIMARY)")
for f, hk in CELLS:
    ref = F1J["rows"][f"PRIMARY {hk}"][f]; c = c0["boost"][f"{f}|{hk}"]
    dev0 += [abs(c["MID"]["A"] - ref["MID"][0]), abs(c["OUTER"]["A"] - ref["OUTER"][0]), abs(c["MID"]["s_jk"] - ref["MID"][1])]
    devc.append(abs(c["chi2_stat"] - H2CHI[(hk, f)]))
check("K0", max(dev0) <= 1e-4 and max(devc) <= 0.5 and max(devp) <= 1e-12,
      f"max|A - F1 PRIMARY| {max(dev0):.1e}; max|chi2 - H2| {max(devc):.2f}; my model vs F1 predict() {max(devp):.1e}", "<= 1e-4; <= 0.5; <= 1e-12")
# K8: cross-shear offset reproduces F1 MUTATE (F1 MUTATE's own weights)
F1M = json.load(open(os.path.join(REB, "F1_cluster_cores", "f1_cluster_cores_results_MUTATE.json")))
Pc0 = stack_model("canonical", "h0672")[0]; Pa0 = stack_model("alt", "h0672")[0]; dd = DAT["h0672"]
axc = A_band(dd["Dx"]*dd["B"][None, :], Pc0, dd["Wx"], ALL)["MID"]; axa = A_band(dd["Dx"]*dd["B"][None, :], Pa0, dd["Wx"], ALL)["MID"]
refm = F1M["rows"]["PRIMARY h0672"]
check("K8", abs(axc - refm["canonical"]["MID"][0]) <= 0.002 and abs(axa - refm["alt"]["MID"][0]) <= 0.002,
      f"cross MID {axc:.4f}/{axa:.4f} vs F1 MUTATE {refm['canonical']['MID'][0]:.4f}/{refm['alt']['MID'][0]:.4f}", "<= 0.002")
# K5: reduced shear perturbative and >= 1
_, _, FAC, KAP, _ = stack_model("canonical", "h0672", red=True)
kmid = float(np.median(KAP[:, 3:6][DAT["h0672"]["m2"][:, 3:6] > 0]))
check("K5", float(FAC.min()) >= 1.0 and kmid < 0.1, f"min factor {FAC.min():.5f}, max {FAC.max():.4f}; median kappa_eff MID {kmid:.4f}", ">= 1; < 0.1")
RES["reduced_shear"] = dict(min=float(FAC.min()), max=float(FAC.max()), median_MID=float(np.median(FAC[:, 3:6])), median_OUTER=float(np.median(FAC[:, 6:8])), kappa_MID=kmid)
# ============================================================== STEP 1: one change at a time, then C*
say("\n=== STEP 1: one change at a time from C0 (graded primaries: a1, c1, d, e) ===")
config("(a1) CFG814 gas: r^-3 beyond 2.2 R500", gasshape="P")
config("(a2) bracket F: r^-3 to 4.4 R500 then r^-2", gasshape="F")
config("(a3) bracket: r^-3 from R500", gasshape="R5")
config("(c1) EFE Chae+21 noclu (F2 transplant)", efe="noclu")
config("(c1-loc) EFE noclu, local-mass transplant", efe="noclu", efe_mode="loc")
config("(c2) EFE Chae+21 maxclu", efe="maxclu")
config("(c3) EFE P2 catalogue median", efe="p2cat")
config("(d) reduced shear", red=True)
config("(e) systematics propagated", sysx=True)
CSTAR = dict(gasshape="P", efe="noclu", red=True)
say("\n=== C* = C0 + (a1) + (c1) + (d) + (e) ===")
cs = config("C* corrected baseline", sysx=True, **CSTAR)
config("C* without (e) (statistical errors only)", sysx=False, **CSTAR)
config("C* with bracket (a3) gas", sysx=True, gasshape="R5", efe="noclu", red=True)
config("C* with (c2) maxclu", sysx=True, gasshape="P", efe="maxclu", red=True)
RES["rows"] = {k: {kk: vv for kk, vv in v.items()} for k, v in ROWS.items()}
say("\nnull-test band offsets (A_x cross shear, A_RR random-minus-random; added in quadrature in (e)), boost convention:")
for lab in ("C0 (F1 PRIMARY)", "C* corrected baseline"):
    for f, hk in CELLS:
        c = ROWS[lab]["boost"][f"{f}|{hk}"]
        say(f"   {lab[:2]} {f[:3]} {hk}: " + "  ".join(f"{b} A_x {c[b]['A_x']:+.3f} A_RR {c[b]['A_RR']:+.3f} (s_jk {c[b]['s_jk']:.3f})" for b in ("MID", "OUTER")))
# ---- (b) terciles at C0 and C*
say("\n=== (b) catalogue-Mgas500 terciles ===")
TER = {}
for lab, kw, sx in (("C0", {}, False), ("C*", CSTAR, True)):
    TER[lab] = {}
    for t, sel in TERC.items():
        r = {conv: {f"{f}|{hk}": stats(hk, stack_model(f, hk, **kw)[0], conv, sel, sx) for f, hk in CELLS} for conv in ("boost", "clip")}
        r["PN"] = {conv: {f"{f}|{hk}": pn(f, hk, conv, sx, sel, **kw) for f, hk in CELLS} for conv in ("boost", "clip")}
        r["PN_status"] = {conv: status([r["PN"][conv][c]["Z_OUT"] for c in r["PN"][conv]]) for conv in ("boost", "clip")}
        TER[lab][t] = r
        say(f"{lab} {t} (median Mgas500 {RES['tercile_median_Mgas500'][t]:.2e}, n {int(sel.sum())}): PN status {r['PN_status']['boost']} (clip {r['PN_status']['clip']})")
        for f, hk in CELLS:
            c = r["boost"][f"{f}|{hk}"]; p = r["PN"]["boost"][f"{f}|{hk}"]; u = "s_tot" if sx else "s_jk"
            say(f"   {f[:3]} {hk}: MID {c['MID']['A']:.3f}+-{c['MID'][u]:.3f} (Z {c['Z_MID']:+.2f})  OUT {c['OUTER']['A']:.3f}+-{c['OUTER'][u]:.3f} "
                f"(Z {c['Z_OUT']:+.2f})  chi2 {c['chi2']:.1f}  | PN lam {p['lam']:.3f} -> OUT {p.get('A_OUT', float('nan')):.3f} (Z {p['Z_OUT']:+.2f})")
RES["terciles"] = TER
# ---- GS (F1's needed dust) and PS at C0 and C* (reported, not graded)
say("\n=== reported shapes at the needed amount: GS (dust tracing gas, sources AQUAL; F1's) and PS (point mass sourcing AQUAL) ===")
NEED = {}
for lab, kw, sx in (("C0", {}, False), ("C*", CSTAR, True)):
    for comp in ("GS", "PS"):
        for f, hk in CELLS:
            for conv in ("boost",):
                d_ = DAT[hk]; Dd = Dused(hk, conv); Wd = d_["W"]; jm = BANDS["MID"]; Sstar = float((Wd[:, jm]*Dd[:, jm]).sum())
                def Sm(lam): return float((Wd[:, jm]*stack_model(f, hk, comp=comp, lam=lam, **kw)[0][:, jm]).sum())
                s0_, s1_ = Sm(0.0), Sm(1.0)
                if Sstar <= s0_: NEED[f"{lab}|{comp}|{f}|{hk}"] = dict(applicable=False); continue
                la, sa, lb, sb_ = 0.0, s0_, 1.0, s1_
                for it in range(10):                                            # secant on the (smooth, monotone) model sum
                    lc = lb + (Sstar - sb_)*(lb - la)/(sb_ - sa); sc = Sm(lc)
                    la, sa, lb, sb_ = lb, sb_, lc, sc
                    if abs(Sstar/sc - 1) < 1e-5: break
                lam = lb; s = stats(hk, stack_model(f, hk, comp=comp, lam=lam, **kw)[0], conv, ALL, sx)
                NEED[f"{lab}|{comp}|{f}|{hk}"] = dict(lam=lam, A_MID=s["MID"]["A"], A_OUT=s["OUTER"]["A"], Z_OUT=s["Z_OUT"], chi2=s["chi2"], iters=it + 1)
                say(f"  {lab} {comp} {f[:3]} {hk}: needed lam {lam:.3f} -> MID {s['MID']['A']:.4f} OUT {s['OUTER']['A']:.3f} (Z {s['Z_OUT']:+.2f}) chi2 {s['chi2']:.1f}")
                PRED.clear()
RES["needed_shapes"] = NEED
# ============================================================== STEP 2: fixed-form components on C*
say("\n=== STEP 2: fixed-form components on C* (no constant fitted) ===")
COMP = {}
for comp, lab in (("DEB-rule", "CFG949 debris, B0 reading, supply from C* gas"), ("DEB-committed", "CFG949 debris, B0, supply from beta=2/3 gas"),
                  ("DEB+law", "C* law + CFG949 debris (Newtonian)"), ("FPS", "FPS Eq.17 eta 8.51 r_c 0.43 Mpc, sources AQUAL")):
    r = run(lab, sysx=True, comp=comp, **CSTAR); r_ns = run(lab, sysx=False, conv_list=("boost",), comp=comp, **CSTAR)
    ok = {conv: all(r[conv][c]["chi2"] <= 11.07 and abs(r[conv][c]["Z_MID"]) <= 2 and abs(r[conv][c]["Z_OUT"]) <= 2 for c in r[conv]) for conv in ("boost", "clip")}
    ok_ns = all(r_ns["boost"][c]["chi2"] <= 11.07 and abs(r_ns["boost"][c]["Z_MID"]) <= 2 and abs(r_ns["boost"][c]["Z_OUT"]) <= 2 for c in r_ns["boost"])
    EX = stack_model("canonical", "h0672", comp=comp, **CSTAR)[4]
    meta = {k: float(np.median([e[k] for e in EX])) for k in EX[0] if k not in ("neg_rho_frac",)}
    COMP[comp] = dict(label=lab, rows=r, rows_nosys=r_ns, passes=ok, passes_nosys=ok_ns, meta_median=meta)
    say(f"{comp}: {lab}  PASS(with sys, boost) {ok['boost']}  (clip {ok['clip']}; no-sys {ok_ns})  medians {json.dumps({k: float(f'{v:.4g}') for k, v in meta.items()})}")
    for f, hk in CELLS:
        c = r["boost"][f"{f}|{hk}"]
        say(f"   {f[:3]} {hk}: MID {c['MID']['A']:.3f}+-{c['MID']['s_tot']:.3f} (Z {c['Z_MID']:+.2f})  OUT {c['OUTER']['A']:.3f}+-{c['OUTER']['s_tot']:.3f} "
            f"(Z {c['Z_OUT']:+.2f})  INNER {c['INNER']['A']:.2f}  chi2 {c['chi2']:.1f} (stat-only {c['chi2_stat']:.1f})")
    PRED.clear()
RES["components"] = COMP
# ============================================================== verdicts (frozen classes)
def v1(conv):
    st = {k: ROWS[k]["PN_status"][conv] for k in ROWS}
    c0s = st["C0 (F1 PRIMARY)"]; prim = {"(a1)": st["(a1) CFG814 gas: r^-3 beyond 2.2 R500"], "(c1)": st["(c1) EFE Chae+21 noclu (F2 transplant)"],
                                         "(d)": st["(d) reduced shear"], "(e)": st["(e) systematics propagated"]}
    css = st["C* corrected baseline"]
    if c0s != "OVER": return "OVERSHOOT NOT ESTABLISHED AT F1's BASELINE", st
    if css == "OVER" and all(v == "OVER" for v in prim.values()): return "OVERSHOOT ROBUST", st
    named = [k for k, v in prim.items() if v == "NONE"]; weak = [k for k, v in prim.items() if v != "OVER"]
    if css == "NONE": return ("OVERSHOOT REMOVED BY " + " + ".join(named)) if named else "OVERSHOOT REMOVED ONLY IN COMBINATION", st
    return "OVERSHOOT WEAKENED BY " + (" + ".join(weak) if weak else "the combination"), st
V1, ST1 = v1("boost"); V1c, _ = v1("clip")
terq = {lab: {t: TER[lab][t]["PN_status"]["boost"] for t in TER[lab]} for lab in TER}
V2 = [k for k, v in COMP.items() if v["passes"]["boost"]]
V2s = ("A FIXED-FORM COMPONENT PASSES (" + ", ".join(V2) + ")") if V2 else "NONE PASSES"
zst = [cs["boost"][c]["Z_MID"] for c in cs["boost"]]; zns = [ROWS["C* without (e) (statistical errors only)"]["boost"][c]["Z_MID"] for c in cs["boost"]]
def v3(z): return "SURVIVES" if min(z) >= 3 else ("NOT SIGNIFICANT" if max(z) < 2 else "WEAKENED")
V3, V3ns = v3(zst), v3(zns)
say(f"\nV1 overshoot: {V1}{'' if V1 == V1c else f'  [BOOST-DEPENDENT: clipped convention gives {V1c}]'}")
say(f"   PN statuses: {ST1}")
say(f"   tercile PN statuses: {terq}")
say(f"V2 components: {V2s}  (clipped boost: {[k for k, v in COMP.items() if v['passes']['clip']] or 'none'}; without (e): {[k for k, v in COMP.items() if v['passes_nosys']] or 'none'})")
say(f"V3 core excess at C*: {V3} with (e) (Z_MID {[round(z, 2) for z in zst]}); without (e): {V3ns} ({[round(z, 2) for z in zns]})")
say("V4 outskirts anchor at C*: " + "  ".join(f"{c}: A_OUT {cs['boost'][c]['OUTER']['A']:.3f}+-{cs['boost'][c]['OUTER']['s_tot']:.3f}" for c in cs["boost"]))
RES.update(V1=V1, V1_clip=V1c, V1_statuses=ST1, V1_tercile_statuses=terq, V2=V2s, V3=V3, V3_nosys=V3ns, Z_MID_Cstar=zst, Z_MID_Cstar_nosys=zns)
pk = rss(); check("K9", pk < 1.0, f"peak RSS {pk:.3f} GB", "< 1 GB")
npass = sum(ok for _, ok in CHECKS); RES.update(runtime_s=time.time() - T0, peak_rss_GB=pk, N=N)
say(f"X2_CLUSTER_OUTSKIRTS COMPLETE: {npass}/{len(CHECKS)} checks PASS. [{time.time()-T0:.0f} s]")
json.dump(RES, open(os.path.join(HERE, f"x2_cluster_outskirts_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)

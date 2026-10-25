"""X26_cold_sector_map (criteria b10263968f): exhaustive exclusion map of the cold-sector sound-speed family
    c_s^2 = c_*^2 (sigma/100 km/s)^{2r} (rho_b/1e-3 Msun/pc^3)^q a^{2p-1}
against the record's committed constraints (X21/X22/X23/X24 machinery, copied or exec'd read-only), both footings, never pooled.
Not a fit: every grid point is graded; only the allowed region is reported.
Usage: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x26_cold_sector_map.py    (X26_MUTATE=1: MUTATE twin, exit 1)
kappa = 1/2 FITTED; footings never pooled; cold energy = field mass, no dark-matter particle; not theory closed."""
import os, sys
import csv, json, math, time, hashlib, resource, itertools
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from astropy.io import fits
from scipy.integrate import solve_ivp
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("X26_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"x26_cold_sector_map{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"lane": "X26_cold_sector_map", "criteria": "b10263968f", "mutate": MUT}; CHECKS = {}
def check(name, ok, val, thr):
    CHECKS[name] = bool(ok); say(f"{name} {'PASS' if ok else 'FAIL'}: {val}   (line: {thr})")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
say("X26_cold_sector_map" + (" [MUTATE m1 T1<->T3 swap, m2 beta factor 2 dropped: control output, not physics]" if MUT else "") +
    ": criteria b10263968f; kappa = 1/2 FITTED; footings never pooled; field mass, no particle; not theory closed")
FEET, HK = ("canonical", "alt"), ("h0672", "h0686"); CELLS = [(f, h) for f in FEET for h in HK]
A0F = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
BFAC = 1.0 if MUT else 2.0                                                    # m2: beta = BFAC sigma^2 / c_s^2
# ============================================================== grid (frozen section 1)
LCS = np.arange(0, 4.0001, 0.125); CSTAR = 10**LCS                                   # km/s
RGRID = np.arange(-1, 3.0001, 0.125); QGRID = np.arange(-1, 1.0001, 0.125); PGRID = [3.0, 4.0, 6.0]
NC, NR, NQ, NP = len(CSTAR), len(RGRID), len(QGRID), len(PGRID)
SIG_STAR, RHO_STAR = 100.0, 1e-3
say(f"grid: c_* {NC} (10^0..10^4 km/s, 0.125 dex), r {NR} ({RGRID[0]}..{RGRID[-1]}), q {NQ} ({QGRID[0]}..{QGRID[-1]}), p {PGRID}: {NC*NR*NQ*NP} points per footing")
def family_cs(sig, rho):
    """c_s (km/s) at z = 0 for arrays sig, rho (trailing axis = systems); returns shape (NC, NR, NQ, nsys)."""
    ls = np.log10(np.asarray(sig, float)/SIG_STAR); lr = np.log10(np.asarray(rho, float)/RHO_STAR)
    return 10**(LCS[:, None, None, None] + RGRID[None, :, None, None]*ls[None, None, None, :] + 0.5*QGRID[None, None, :, None]*lr[None, None, None, :])
# ============================================================== record JSONs
def J(rel): return json.load(open(os.path.join(REB, rel)))
X19R = J("X19_selector_rank_test/x19_selector_rank_test_results.json"); X21J = J("X21_cluster_switch_anatomy/x21_switch_anatomy_results.json")
X22J = J("X22_cosmic_dust_window/x22_cosmic_dust_window_results.json"); X23J = J("X23_late_heated_cold/x23_late_heated_cold_results.json")
PEERJ = J("X23_late_heating_graded/x23_late_heating_graded_results.json"); X24J = J("X24_dwarf_velocity_floor/x24_dwarf_velocity_floor_results.json")
X24bJ = J("X24b_vacuum_heated_cold/x24b_vacuum_heated_cold_results.json")
for nm, p in (("X19", "X19_selector_rank_test/x19_selector_rank_test_results.json"), ("X21", "X21_cluster_switch_anatomy/x21_switch_anatomy_results.json"),
              ("X22", "X22_cosmic_dust_window/x22_cosmic_dust_window_results.json"), ("X23", "X23_late_heated_cold/x23_late_heated_cold_results.json"),
              ("peer", "X23_late_heating_graded/x23_late_heating_graded_results.json"), ("X24", "X24_dwarf_velocity_floor/x24_dwarf_velocity_floor_results.json"),
              ("X24b", "X24b_vacuum_heated_cold/x24b_vacuum_heated_cold_results.json")):
    RES[f"{nm}_json_sha256"] = sha(os.path.join(REB, p))
CS = {f: float(X22J["step2"]["per_footing"][f]["cs_need_kms"]) for f in FEET}
# ============================================================== X22 / CFG946 constants (verbatim values)
G946, MSUN946, PC946 = 6.67430e-11, 1.98847e30, 3.0856775814913673e16; KPC946 = 1e3*PC946; MPC946 = 1e6*PC946
H0_946 = 67.4e3/MPC946; RHOC_946 = 3*H0_946**2/(8*math.pi*G946); OB946 = 0.0493; OC946 = 5.364*OB946; OM946 = OB946 + OC946
RHOM946 = OM946*RHOC_946; DTA = 5.55; BCAP = 2.9; HH = 0.674; OL946 = 1 - OM946; FC, FB = 5.364/6.364, 1/6.364
MP, KEV, CLIGHT = 1.67262192e-27, 1.602176634e-16, 2.99792458e8
def r_ta(Mb_kg): return (3*(OM946/OB946)*Mb_kg/(4*math.pi*DTA*RHOM946))**(1/3)
def hydro_frac_enclosed(beta, xx): return (1.0/DTA)*3.0/(3.0 - beta)*np.power(np.minimum(xx, 1.0), 3.0 - beta)
def law_g(gN, a0): gN = np.asarray(gN, float); return 0.5*(gN + np.sqrt(gN*gN + 4.0*gN*a0))
def nu1(yv): yv = np.maximum(np.asarray(yv, float), 1e-300); return 0.5 + np.sqrt(0.25 + 1.0/yv)
def e_pred_vec(Mb_msun, r_m, gN, sig, a0, cs):
    """peer lane X23_late_heating_graded e_pred, vectorised over cs (and systems): returns E (dex)."""
    beta = np.minimum(BFAC*np.asarray(sig)**2/np.asarray(cs)**2, BCAP); Mb = np.asarray(Mb_msun)*MSUN946
    rta = r_ta(Mb); Mc = 5.364*Mb*hydro_frac_enclosed(beta, np.asarray(r_m)/rta); gc = G946*Mc/np.asarray(r_m)**2
    return np.log10(law_g(gN + gc, a0)/law_g(gN, a0))
# ============================================================== STEP 0 / cosmic medium: X22's ODE and grade (verbatim bodies)
L346 = json.load(open(os.path.join(REPO, "real_research/g03_audit_2026/L346_switch_forest_gate_results.json")))
runs346 = L346["numbers"]["runs"]
def r346(name, z):
    a_ = np.array(runs346[name]["pk"][z]); b_ = np.array(runs346["lcdm"]["pk"][z]); kk = b_[:, 0]; fo = (kk >= 1.0) & (kk <= 4.0)
    return kk[fo], (a_[:, 1]/b_[:, 1])[fo]
KB346 = r346("sw5_canon", "3.0")[0]
h19 = 0.6736; Om19 = (0.02237 + 0.1200)/h19**2; K_H19 = np.geomspace(0.02, 30.0, 44); K5 = float(K_H19[int(np.argmin(np.abs(K_H19 - 5.0)))])
NU = 1.12; EXPO = -10.0/NU
def alpha_wdm(m_keV): return 0.049*m_keV**-1.11*(Om19/0.25)**0.11*(h19/0.7)**1.22
def T2cut(k_h, alpha): return (1 + (alpha*np.asarray(k_h, float))**(2*NU))**EXPO
T2_53 = float(T2cut(K5, alpha_wdm(5.3)))
def forest_class(t2bins_by_z, t2k5_by_z):
    allbins = [v for z in t2bins_by_z for v in t2bins_by_z[z]]; k5s = list(t2k5_by_z.values())
    if min(k5s) < 0.9 or min(allbins) < 0.5 or max(allbins) > 2.0: return "FAIL"
    if all(0.8 <= v <= 1.2 for v in allbins) and min(k5s) >= T2_53: return "PASS"
    return "UNDECIDED"
SRC = 1.5
def grow(k_h, cs_fn, ai=1e-3, zout=(3.0, 2.0, 0.0)):
    def rhs(N, y):
        a = math.exp(N); E2 = OM946*a**-3 + OL946; Oma = OM946*a**-3/E2; dlnH = -1.5*Oma; cs = cs_fn(a)
        Jt = (cs*k_h/(100.0*a*math.sqrt(E2)))**2; src = SRC*Oma*(FC*y[0] + FB*y[2])
        return [y[1], -(2 + dlnH)*y[1] + src - Jt*y[0], y[3], -(2 + dlnH)*y[3] + src]
    Ns = sorted([math.log(1/(1 + z)) for z in zout]); y = [ai, ai, ai, ai]; out = {}
    te = [N for N in Ns if math.log(ai) < N <= 0.0]
    sol = solve_ivp(rhs, (math.log(ai), 0.0), y, method="LSODA", rtol=1e-8, atol=1e-14, t_eval=te if te else None)
    for j, N in enumerate(te): out[round(1/math.exp(N) - 1, 6)] = FC*sol.y[0][j] + FB*sol.y[2][j]
    return out
KS8 = np.geomspace(1e-3, 30.0, 61); KF = np.concatenate([KB346, [K5]])
REF = {float(k): grow(float(k), lambda a: 0.0) for k in np.concatenate([KS8, KF])}
h_m, Om_m, Ob_m, ns_m = 0.674, 0.315, 0.0493, 0.965
Gam = Om_m*h_m*np.exp(-Ob_m*(1.0 + np.sqrt(2*h_m)/Om_m))
def Tk(k):
    qq = k/Gam; return (np.log(1 + 2.34*qq)/(2.34*qq)*(1 + 3.89*qq + (16.1*qq)**2 + (5.46*qq)**3 + (6.71*qq)**4)**-0.25)
kfine = np.logspace(-4, 2, 1200); D2shape = kfine**(3 + ns_m)*Tk(kfine)**2
def Wth(x): return 3*(np.sin(x) - x*np.cos(x))/x**3
W8 = Wth(kfine*8.0)**2
_trap = getattr(np, "trapezoid", None) or np.trapz
def sigma8_ratio(T2_on_KS8):
    lt = np.interp(np.log(np.clip(kfine, KS8[0], KS8[-1])), np.log(KS8), np.log(np.maximum(T2_on_KS8, 1e-300)))
    T2f = np.where(kfine < KS8[0], 1.0, np.exp(lt))
    return math.sqrt(_trap(D2shape*W8*T2f, np.log(kfine))/_trap(D2shape*W8, np.log(kfine)))
def grade_forest(cs_fn):
    gF = {float(k): grow(float(k), cs_fn, zout=(3.0, 2.0)) for k in KF}; tb, tk = {}, {}
    for z, zs in ((3.0, "3"), (2.0, "2")):
        tb[zs] = [(gF[float(k)][z]/REF[float(k)][z])**2 for k in KB346]; tk[zs] = (gF[K5][z]/REF[K5][z])**2
    return forest_class(tb, tk)
def grade_s8(cs_fn):
    return sigma8_ratio(np.array([(grow(float(k), cs_fn, zout=(0.0,))[0.0]/REF[float(k)][0.0])**2 for k in KS8]))
say("\n=== STEP 0 ===")
t1 = time.time(); d0d = []; fcls = {}
for f in FEET:
    for p in (3.0, 4.0, 6.0):
        fn = (lambda a, c0=CS[f], p=p: c0*a**(p - 0.5)); rs = grade_s8(fn); fc = grade_forest(fn); ref = X22J["step3B"]["per_footing"][f][str(p)]
        d0d.append(abs(rs - ref["R_sigma8"])); fcls[f"{f}|p{p}"] = (fc, ref["forest"])
        say(f"  X22 {f} p {p}: R_sigma8 {rs:.6f} (X22 {ref['R_sigma8']:.6f}); forest {fc} (X22 {ref['forest']})")
k0d = max(d0d) <= 1e-6 and all(a == b for a, b in fcls.values())
say(f"  [{time.time()-t1:.0f} s]")
# ============================================================== SPARC (X22 step 2 machinery, verbatim bodies)
KPC_S = 3.0857e19; UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2); SD = os.path.join(REPO, "real_research", "data", "sparc_data"); GALS = []
for fn in sorted(os.listdir(SD)):
    if not fn.endswith("_rotmod.dat"): continue
    try: dd = np.genfromtxt(os.path.join(SD, fn), comments="#")
    except Exception: continue
    if dd.ndim != 2 or dd.shape[1] < 6: continue
    q = dict(name=fn.replace("_rotmod.dat", ""), R=dd[:, 0], Vobs=dd[:, 1], eV=dd[:, 2], Vgas=dd[:, 3], Vdisk=dd[:, 4], Vbul=dd[:, 5])
    Rm = q["R"]*KPC_S
    VB2 = np.sign(q["Vgas"])[:, None]*q["Vgas"][:, None]**2 + UPS[None, :]*q["Vdisk"][:, None]**2 + 1.4*UPS[None, :]*q["Vbul"][:, None]**2
    GB = VB2*1e6/Rm[:, None]; GO = ((q["Vobs"]*1e3)**2/Rm)[:, None]*np.ones_like(GB)
    OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (q["Vobs"] > 0)[:, None]
    Wt = 1.0/(np.clip(q["eV"], 1, None)/np.clip(q["Vobs"], 1, None))**2
    Mb = np.maximum(VB2[-1, :], 0.0)*1e6*Rm[-1]/G946; rta = np.array([r_ta(m) if m > 0 else 1.0 for m in Mb])
    q.update(Rm=Rm, GB=GB, GO=GO, OK=OK, Wt=Wt, Mb=Mb, rta=rta); GALS.append(q)
NG = len(GALS)
def sparc_stats_g(a0, gd_fn):
    wr2 = wsum = 0.0; U, IDX = [], []
    for i, q in enumerate(GALS):
        GBt = q["GB"] + gd_fn(i, q)
        lgp = np.log10(np.where(q["GB"] > 0, nu1(np.maximum(GBt, 1e-300)/a0)*np.maximum(GBt, 1e-300), 1e-300))
        r_ = np.where(q["OK"], np.log10(np.where(q["OK"], q["GO"], 1.0)) - lgp, 0.0)
        Wm = np.where(q["OK"], q["Wt"][:, None], 0.0); mse = (Wm*r_*r_).sum(0)/np.maximum(Wm.sum(0), 1e-300); j = int(np.argmin(mse))
        wr2 += float((Wm[:, j]*r_[:, j]**2).sum()); wsum += float(Wm[:, j].sum()); U.append(UPS[j]); IDX.append(j)
    return dict(rms=math.sqrt(wr2/wsum), U_median=float(np.median(U)), N=len(GALS), idx=IDX)
LAW = {f: sparc_stats_g(A0F[f], lambda i, q: 0.0) for f in FEET}
U_EDGE = {f: min(0.50, LAW[f]["U_median"]) for f in FEET}
def line_ok(f, s_): return s_["rms"] <= 0.110 and U_EDGE[f] <= s_["U_median"] <= 0.80
VLAST = np.array([q["Vobs"][-1] for q in GALS]); RLAST = np.array([q["R"][-1] for q in GALS])
def gd_family(cs_vec):
    def fgd(i, q):
        beta = min(BFAC*(VLAST[i]/math.sqrt(2))**2/cs_vec[i]**2, BCAP)
        Mc = 5.364*q["Mb"][None, :]*hydro_frac_enclosed(beta, q["Rm"][:, None]/q["rta"][None, :]); return G946*Mc/q["Rm"][:, None]**2
    return fgd
SIG_SP = VLAST/math.sqrt(2)
RHO_SP = {}
for f in FEET:
    idx = LAW[f]["idx"]; Mb_law = np.array([GALS[i]["Mb"][idx[i]] for i in range(NG)])/MSUN946
    RHO_SP[f] = Mb_law/(4/3*math.pi*(RLAST*1e3)**3)                                  # Msun/pc^3 inside R_last
def sparc_ok(f, cs_vec): return line_ok(f, sparc_stats_g(A0F[f], gd_family(cs_vec)))
t1 = time.time(); csn_rep = {}
for f in FEET:                                                                          # K0c: X22 c_s,need by this machinery at r = q = 0
    lo, hi = math.log(1.0), math.log(3000.0)
    for _ in range(30):
        md = 0.5*(lo + hi); (lo, hi) = (lo, md) if sparc_ok(f, np.full(NG, math.exp(md))) else (md, hi)
    csn_rep[f] = math.exp(hi)
k0c = all(abs(csn_rep[f]/CS[f] - 1) <= 1e-3 for f in FEET)
say(f"  SPARC c_s,need at r = q = 0 (this lane's vector form): {csn_rep['canonical']:.3f} / {csn_rep['alt']:.3f} km/s (X22 {CS['canonical']:.3f} / {CS['alt']:.3f}) [{time.time()-t1:.0f} s]")
# ============================================================== X19 class rows, peer predictor (groups, MW disc, other classes)
def class_row(f, c):
    iv = X19R["intervals"][f"{f}|p16_84"][c]; a0 = A0F[f]
    Mb, sg, rho, xg = iv["M_b"][2], iv["sigma"][2], iv["rho_b"][2], iv["x"][2]; gN = xg*a0
    rr_ = 3*gN/(4*math.pi*G946*rho*MSUN946/PC946**3); return dict(Mb=Mb, sig=sg, rho=rho, gN=gN, r=rr_)
CLS = ["SPARC small", "SPARC large", "Groups", "MW disc", "Crater II", "Antlia II", "Coma UDGs", "UMa members", "TDGs", "DF2/DF4", "LG field", "MW classical"]
d0e = []
for f in FEET:
    for c in ("Groups", "MW disc"):
        cr = class_row(f, c); ep = float(e_pred_vec(cr["Mb"], cr["r"], cr["gN"], cr["sig"], A0F[f], CS[f]))
        d0e.append(abs(ep - PEERJ["footings"][f]["classes"][c]["E_pred"])); say(f"  peer {f} {c}: E_pred {ep:+.6f} (peer {PEERJ['footings'][f]['classes'][c]['E_pred']:+.6f})")
# ============================================================== dwarfs: X24's rows (verbatim load), floor reproduction
ARR = list(csv.DictReader(open(os.path.join(LANES, "CFG257_ufd_kinematics_scoping", "arroyo_polonio2026_tableA1.csv"))))
arr_free = {r["lvd_name"]: float(r["sig_free"])/float(r["sig_f0"]) for r in ARR}; med_free = float(np.median(list(arr_free.values())))
X1 = list(csv.DictReader(open(os.path.join(REB, "X1_hosted_recount", "x1_per_system.csv"))))
ECOL = "Delta[iso AQUAL L*0]"; SCOL = "sdMC[iso AQUAL L*0]"; HCL = ("MW ultra-faint", "bright M31", "M31 others")
def load(foot, classes):
    out = []
    for r in X1:
        if r["footing"] != foot or r["cls"] not in classes: continue
        mv = float(r["M_V"]) if r["M_V"] not in ("", None) else None
        b = arr_free.get(r["name"], med_free if (mv is not None and mv > -7.7) else 1.0)
        sc = float(r["sigma"])*b; E = float(r[ECOL])
        out.append(dict(name=r["name"], cls=r["cls"], lm=float(r["logMstar"]), E=E, s=float(r[SCOL]), sc=sc, siso=sc*10**(-E/2), rh=float(r["rh_pc"])))
    return out
def epred_floor(siso, c0): return np.log10(1.0 + (c0/np.asarray(siso))**2)
DW = {}
for f in FEET:
    R74 = load(f, HCL) + load(f, ("LG field",)); a0 = A0F[f]; c0 = X24J["footings"][f]["B"]["c0"]
    M = 10**np.array([q["lm"] for q in R74]); r12 = 4/3*np.array([q["rh"] for q in R74])*PC946
    gN = G946*(M/2)*MSUN946/r12**2; rho = (M/2)/(4/3*math.pi*(r12/PC946)**3)
    E = np.array([q["E"] for q in R74]); s = np.array([q["s"] for q in R74]); siso = np.array([q["siso"] for q in R74]); sc = np.array([q["sc"] for q in R74])
    isH = np.array([q["cls"] in HCL for q in R74]); Ef = epred_floor(siso, c0)
    chiH, chiF = float((((E - Ef)/s)**2)[isH].sum()), float((((E - Ef)/s)**2)[~isH].sum())
    DW[f] = dict(N=len(R74), M=M, r12=r12, gN=gN, rho=rho, E=E, s=s, sc=sc, lm=np.log10(M), Ef=Ef, chi_floor=chiH + chiF, c0=c0)
    d0e += [abs(chiH/X24J["footings"][f]["B"]["chi2_H_floor"] - 1), abs(chiF/X24J["footings"][f]["B"]["chi2_field"] - 1)]
    say(f"  X24 {f}: N {len(R74)} (H {isH.sum()}, field {(~isH).sum()}); c0 {c0:.4f}; chi2 floor H {chiH:.3f} (X24 {X24J['footings'][f]['B']['chi2_H_floor']:.3f}), "
        f"field {chiF:.3f} (X24 {X24J['footings'][f]['B']['chi2_field']:.3f}); 74-row floor chi2 {chiH + chiF:.3f}")
k0e = max(d0e) <= 1e-6 and all(abs(x) <= 1e-10 for x in d0e[:4])
say(f"  X24b verdict read: {X24bJ['verdict']}")
k0f = X24bJ["verdict"] == "NO EPS WINDOW"
# ============================================================== clusters: X23_late_heated_cold machinery (X2 functions exec'd read-only)
X2DIR = os.path.join(REB, "X2_cluster_outskirts"); X2SRC = os.path.join(X2DIR, "x2_cluster_outskirts.py"); TX = open(X2SRC).read(); RES["x2_source_sha256"] = sha(X2SRC)
def cutx(a, b): i = TX.index(a); j = TX.index(b, i); return TX[i:j]
NS2 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "REB": REB, "REPO": REPO, "HERE": X2DIR,
       "LANES": LANES, "MUT": False, "RES": {}, "say": (lambda *a: None), "check": (lambda *a: None), "sha": sha, "rss": rss, "guard": (lambda tag: None)}
exec(cutx("# ============================================================== F1's own functions", "# ============================================================== data: the replay"), NS2)
exec(cutx("# ============================================================== data: the replay", "# ============================================================== statistics"), NS2)
exec(cutx("# ============================================================== statistics", "# ============================================================== EFE"), NS2)
exec(cutx('sys.path.insert(0, os.path.join(REB, "F2_outer_lensing"))', 'for f in FEET:\n    for k in ("noclu", "maxclu", "p2cat"):'), NS2)
exec(cutx("# ============================================================== the model", "# ============================================================== K2, K3, K7"), NS2)
for f in FEET:
    t1 = time.time(); NS2["CTAB"][(f, "noclu")] = NS2["ctable"](NS2["AQ"].solve_efe(NS2["YE"][f]["noclu"], maxit=3000)); say(f"  EFE solve (X2's) {f} noclu [{time.time()-t1:.0f} s]")
G, MSUN, MPC, KG_PC2, A0 = NS2["G"], NS2["MSUN"], NS2["MPC"], NS2["KG_PC2"], NS2["A0"]
RG, RM = NS2["RG"], NS2["RM"]
gas, g_aqual_sph, Cof, CTAB = NS2["gas"], NS2["g_aqual_sph"], NS2["Cof"], NS2["CTAB"]
project_floor, offset_floor, dsig_from_sig, at_bins, sig_bins = (NS2[k] for k in ("project_floor", "offset_floor", "dsig_from_sig", "at_bins", "sig_bins"))
DM, DA_lcdm, HV = NS2["DM"], NS2["DA_lcdm"], NS2["HV"]
X7DIR = os.path.join(REB, "X7_cluster_core_significance"); NPZ = os.path.join(X7DIR, "x7_measure_percluster.npz")
MY = np.load(NPZ); RES["x7_npz_sha256"] = sha(NPZ); N = len(MY["name"])
HI = {"h0672": 1, "h0686": 2}; HXI = {"h0672": 0, "h0686": 1}; DAT = {}
for hk in HK:
    i = HI[hk]; W = np.where(MY["E"][:, i] < 1e8, 1/MY["E"][:, i]**2, 0); B = MY["den"][:, i].sum(0)/MY["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=MY["D"][:, i], W=W, B=B, Dx=MY["Dx"][:, i], Wx=W, DRR=MY["DRR"][:, i], m2=MY["den"][:, i], m=MY["m3to8"][:, i])
NS2["DAT"] = DAT; CL = NS2["CL"]; JM = NS2["BANDS"]["MID"]; redfac = NS2["redfac"]
assert [c["name"] for c in CL] == [str(x) for x in MY["name"]]
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); RES["erass1_sha256"] = sha(EF)
E_ = fits.open(EF)[1].data; idx_ = {str(s_).strip(): k for k, s_ in enumerate(E_["NAME"])}
KT = np.asarray(E_["KT"], float)[np.array([idx_[str(x).strip()] for x in MY["name"]])]
I = np.where(np.isfinite(KT) & (KT > 0))[0]; nI = len(I); xkt = np.log10(KT[I]/np.median(KT[I])); TID = np.digitize(xkt, np.quantile(xkt, [1/3, 2/3]))
SIG_KT = np.sqrt(KT[I]*KEV/(0.6*MP))/1e3
def r_ta_com(Mb_kg): return (3*(OM946/OB946)*Mb_kg/(4*math.pi*DTA*RHOM946))**(1/3)
def lnrho_profile(g, r_m, rta_m, cs_ms):
    Ic = np.r_[0, np.cumsum(0.5*(g[1:] + g[:-1])*np.diff(r_m))]; return (np.interp(rta_m, r_m, Ic) - Ic)/cs_ms**2
def cold_mass(g, r_m, rta_m, cs_ms, Mfair, ln_rhobar):
    lr = lnrho_profile(g, r_m, rta_m, cs_ms); inside = r_m <= rta_m
    lmax = float(lr[inside].max()); w = np.where(inside, np.exp(lr - lmax), 0.0)
    dm = 4*np.pi*r_m**2*w; Mw = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r_m))]
    Mrta = float(np.interp(rta_m, r_m, Mw)); shape = np.minimum(Mw/Mrta, 1.0)
    ln_cos = ln_rhobar + lmax + math.log(Mrta); Mtot = Mfair if ln_cos >= math.log(Mfair) else math.exp(ln_cos)
    return shape*Mtot
def gfun(Msrc, foot):
    a0 = A0[foot]; gN = G*Msrc/RM**2; g = g_aqual_sph(gN, a0); tab = CTAB[(foot, "noclu")]
    s_ = RG/(math.sqrt(G*float(np.interp(3.0, RG, Msrc))/a0)/MPC); return g*Cof(tab, s_)
PREP = {}
def prep(i, foot, hk):
    key = (i, foot, hk)
    if key in PREP: return PREP[key]
    cl = CL[i]; h = HV[hk]; qd = (float(DM(cl["z"], h))/(1 + cl["z"]))/DA_lcdm(cl["z"])
    Mg500 = cl["Mgas500"]*qd**2.5; R500 = cl["R500"]*qd; Mg, rho_g = gas(Mg500, R500, "P"); Mb = Mg*(1 + 0.20); Mbt = float(Mb[-1])
    out = dict(Mb=Mb, gb=gfun(Mb, foot), rta=r_ta_com(Mbt)/(1 + cl["z"]), Mfair=5.364*Mbt, ln_rhobar=math.log(OC946*RHOC_946*(1 + cl["z"])**3),
               dmpc=np.radians(cl["off_deg"])*float(DM(cl["z"], h))/(1 + cl["z"]))
    PREP[key] = out; return out
def dmid(i, foot, hk, Mc):
    pp = prep(i, foot, hk); Msrc = pp["Mb"] if Mc is None else pp["Mb"] + Mc
    g = gfun(Msrc, foot); ML = g*RM**2/G; rho = np.gradient(ML, RM)/(4*np.pi*RM**2)
    So = offset_floor(project_floor(rho), pp["dmpc"]); Pp = at_bins(dsig_from_sig(So))/KG_PC2
    fr, _ = redfac(hk, i, sig_bins(So)); return float((DAT[hk]["W"][i, JM]*(Pp*fr)[JM]).sum())
def d_lhc(i, foot, hk, cs_kms):
    pp = prep(i, foot, hk); return dmid(i, foot, hk, cold_mass(pp["gb"], RM, pp["rta"], cs_kms*1e3, pp["Mfair"], pp["ln_rhobar"]))
FAC = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 13, 16]
CSTAB = {f: np.unique(np.r_[np.geomspace(5.0, 3e4, 64), CS[f]*np.array(FAC)]) for f in FEET}
def wls1(n, d, X):
    F = np.einsum("i,ij,ik->jk", d, X, X); gg = np.einsum("ij,i->j", X, n); return np.linalg.solve(F, gg)
X1m = np.c_[np.ones(nI), xkt]
CEL = {}
for f, hk in CELLS:
    t1 = time.time(); dd = DAT[hk]; WB = dd["W"]*dd["B"][None, :]; hx = HXI[hk]
    n = np.array([(WB[i, JM]*(dd["D"][i, JM] - MY["leakP"][i, hx, 0][JM])).sum() for i in I])
    dC = np.array([dmid(i, f, hk, None) for i in I])
    TAB = np.array([[d_lhc(i, f, hk, cs) for i in I] for cs in CSTAB[f]])             # (ncs, nI)
    rhoK = np.array([float(np.interp(0.548, RG, prep(i, f, hk)["Mb"]))/MSUN for i in I])/(4/3*math.pi*(0.548e6)**3)
    PREP.clear(); CEL[(f, hk)] = dict(n=n, d=dC, TAB=TAB, rho=rhoK)
    say(f"  cluster table {f} {hk}: {len(CSTAB[f])} c_s nodes x {nI} KT clusters [{time.time()-t1:.0f} s, RSS {rss():.2f} GB]")
# K0a, K0b
dev_a, dev_b = [], []
for f, hk in CELLS:
    c = CEL[(f, hk)]; cl = f"{f}|{hk}"; ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]
    A = [float(c["n"][TID == t].sum()/c["d"][TID == t].sum()) for t in range(3)]; b = float(wls1(c["n"], c["d"], X1m)[1])
    Aref = list(ref["A"]); Aref = Aref[::-1] if MUT else Aref                                                 # m1
    dev_a += [abs(a - r_) for a, r_ in zip(A, Aref)] + [abs(b - X21J["tests"]["V1"]["cells"][cl]["b"])]
    for k, fa in enumerate(FAC):
        j = int(np.argmin(np.abs(CSTAB[f] - CS[f]*fa))); dk = c["TAB"][j]
        ApK = [float(dk[TID == t].sum()/c["d"][TID == t].sum()) for t in range(3)]
        dev_b += [abs(x_ - y_) for x_, y_ in zip(ApK, X23J["amendment_A1"][f]["rows"][k][hk]["A_pred_KT_terciles"])]
say(f"  X21 KT terciles/slope reproduced max |dev| {max(dev_a):.2e}; X23 A1 KT-tercile A_pred at the 13 nodes max |dev| {max(dev_b):.2e}")
check("K0a", max(dev_a) <= 1e-9, f"X21 KT terciles + slope, max |dev| {max(dev_a):.2e}", "<= 1e-9")
check("K0b", max(dev_b) <= 1e-9, f"X23 A1 KT-tercile A_pred at c_s,need x FAC, max |dev| {max(dev_b):.2e}", "<= 1e-9")
check("K0c", k0c, f"SPARC c_s,need {csn_rep['canonical']:.3f} / {csn_rep['alt']:.3f} vs X22 {CS['canonical']:.3f} / {CS['alt']:.3f}", "<= 0.1 %")
check("K0d", k0d, f"X22 R_sigma8 (p 3/4/6) max |dev| {max(d0d):.2e}; forest classes identical {all(a == b for a, b in fcls.values())}", "<= 1e-6; identical")
check("K0e", k0e, f"peer groups/MW E_pred max |dev| {max(d0e[:4]):.2e}; X24 chi2 floor rel dev {max(d0e[4:]):.2e}", "<= 1e-10; <= 1e-6")
check("K0f", k0f, f"X24b verdict '{X24bJ['verdict']}'", "NO EPS WINDOW")
STOP = not all(CHECKS[k] for k in ("K0a", "K0b", "K0c", "K0d", "K0e", "K0f"))
RES["step0"] = dict(K0a=max(dev_a), K0b=max(dev_b), cs_need_rep=csn_rep, K0d=max(d0d), K0e=d0e)
def tab_interp(lc, ltab, col):
    """A1: log-linear in d where the column is positive throughout, else linear in d (a zero-weight cluster has d = 0 at every node)."""
    if np.all(col > 0): return np.exp(np.interp(lc, ltab, np.log(col)))
    return np.interp(lc, ltab, col)
NZERO = {k: int(sum(not np.all(v["TAB"][:, j] > 0) for j in range(nI))) for k, v in CEL.items()}
say(f"  A1: KT clusters with a non-positive d in the table (linear interpolation): {NZERO}")
# K1: interpolation vs direct off-node
t1 = time.time(); k1dev = 0.0
for f, hk in CELLS:
    c = CEL[(f, hk)]; ltab = np.log(CSTAB[f])
    for cs in np.geomspace(60.0, 6000.0, 6)*1.07:
        dI = np.array([tab_interp(math.log(cs), ltab, c["TAB"][:, j]) for j in range(nI)])
        dD = np.array([d_lhc(i, f, hk, cs) for i in I]); PREP.clear()
        for t in range(3):
            aI = dI[TID == t].sum()/c["d"][TID == t].sum(); aD = dD[TID == t].sum()/c["d"][TID == t].sum()
            k1dev = max(k1dev, abs(aI/aD - 1)) if np.isfinite(aI/aD) else float("inf")
check("K1", k1dev <= 0.01, f"cluster table interpolation: max |A_pred(interp)/A_pred(direct) - 1| = {k1dev:.2e} (6 off-node c_s x 4 cells x 3 terciles) [{time.time()-t1:.0f} s]", "<= 1 %")
if STOP:
    say("\nSTOP RULE: a step-0 reproduction failed; verdict UNDECIDED; no graded number.")
    RES["verdict"] = "UNDECIDED (step 0 failed)"
# ============================================================== GRID EVALUATION
say("\n=== STEP 1-3: the map ===")
PASS = {f: {} for f in FEET}                                                 # constraint -> bool array (NC, NR, NQ, NP)
SHAPE = (NC, NR, NQ, NP)
def bc(a3): return np.broadcast_to(a3[..., None], SHAPE).copy()
# --- clusters (KT terciles, slope), both h cells
for f in FEET:
    okT = [np.ones((NC, NR, NQ), bool) for _ in range(3)]; okB = np.ones((NC, NR, NQ), bool)
    for hk in HK:
        c = CEL[(f, hk)]; cl = f"{f}|{hk}"; ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]; tv = X21J["tests"]["V1"]["cells"][cl]
        Am = list(ref["A"]); sm = list(ref["s"])
        if MUT: Am, sm = Am[::-1], sm[::-1]
        csK = family_cs(SIG_KT, c["rho"])                                          # (NC, NR, NQ, nI)
        ltab = np.log(CSTAB[f]); lc = np.clip(np.log(csK), ltab[0], ltab[-1])
        dL = np.empty_like(csK)
        for j in range(nI): dL[..., j] = tab_interp(lc[..., j], ltab, c["TAB"][:, j])
        assert np.isfinite(dL).all(), "non-finite cluster prediction"
        for t in range(3):
            Ap = dL[..., TID == t].sum(-1)/c["d"][TID == t].sum(); okT[t] &= np.abs(Am[t] - Ap) <= 2*sm[t]
        F = np.einsum("i,ij,ik->jk", c["d"], X1m, X1m); Fi = np.linalg.inv(F)
        bp = np.einsum("k,...i,ik->...", Fi[1], dL, X1m); okB &= np.abs(tv["b"] - bp) <= 2*tv["s_b"]
        del dL, csK, lc
    for t in range(3): PASS[f][f"C-T{t+1}"] = bc(okT[t])
    PASS[f]["C-KTb"] = bc(okB)
say(f"  clusters graded [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
# --- groups, MW disc, dwarfs (vectorised peer predictor)
EFAM = {}
for f in FEET:
    a0 = A0F[f]
    cr = class_row(f, "Groups"); et = X19R["E_table"][f"{f}|iso"]["Groups"]
    Eg = e_pred_vec(cr["Mb"], cr["r"], cr["gN"], cr["sig"], a0, family_cs([cr["sig"]], [cr["rho"]])[..., 0])
    PASS[f]["C-groups"] = bc(np.abs(et["E"] - Eg) < 2*et["s"])
    cr = class_row(f, "MW disc"); Em = e_pred_vec(cr["Mb"], cr["r"], cr["gN"], cr["sig"], a0, family_cs([cr["sig"]], [cr["rho"]])[..., 0])
    PASS[f]["C-MW"] = bc(Em <= math.log10(1 + 2*2.2/66.4))
    d_ = DW[f]; csD = family_cs(d_["sc"], d_["rho"])
    Ed = e_pred_vec(d_["M"]/2, d_["r12"], d_["gN"], d_["sc"], a0, csD)                     # (NC, NR, NQ, 74)
    chi = (((d_["E"] - Ed)/d_["s"])**2).sum(-1)
    rk = lambda v: np.argsort(np.argsort(v, axis=-1), axis=-1).astype(float)
    rx = rk(d_["lm"]); rx -= rx.mean(); ry = rk(Ed); ry -= ry.mean(-1, keepdims=True)
    den = np.sqrt((rx**2).sum()*(ry**2).sum(-1)); sp_ = np.where(den > 0, (ry*rx).sum(-1)/np.where(den > 0, den, 1), np.nan)
    sp_ = np.where(np.ptp(Ed, axis=-1) > 1e-12, sp_, np.nan)                                    # constant prediction: no trend
    PASS[f]["C-dwarfs"] = bc((chi <= d_["chi_floor"]) & (np.nan_to_num(sp_, nan=1.0) < 0))
    chiB = (((d_["E"] - (d_["Ef"] + Ed))/d_["s"])**2).sum(-1)
    PASS[f]["C-dwarfs-c0"] = bc(chiB <= d_["chi_floor"] + 4)
    EFAM[f] = dict(dw_chi=chi, dw_sp=sp_, dw_chiB=chiB, Eg=Eg, Em=Em, dw_medE=np.median(Ed, -1))
    other = {}
    for c in ("Crater II", "TDGs", "DF2/DF4", "UMa members", "Antlia II", "Coma UDGs", "SPARC small", "SPARC large", "LG field", "MW classical"):
        cr = class_row(f, c); other[c] = e_pred_vec(cr["Mb"], cr["r"], cr["gN"], cr["sig"], a0, family_cs([cr["sig"]], [cr["rho"]])[..., 0])
    EFAM[f]["other"] = other
    del Ed, csD
say(f"  groups / MW / dwarfs graded [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
# --- SPARC (X22 d2 line; bisection on c_* per (r, q), monotone: K2)
t1 = time.time(); K2cols = [(0, 0), (8, 8), (16, 4), (4, 12), (24, 8), (32, 16), (12, 0), (20, 14)]; k2ok = True
for f in FEET:
    ok = np.zeros((NC, NR, NQ), bool)
    for ir in range(NR):
        for iq in range(NQ):
            ls = np.log10(SIG_SP/SIG_STAR); lr = np.log10(RHO_SP[f]/RHO_STAR)
            cs_of = lambda ic: 10**(LCS[ic] + RGRID[ir]*ls + 0.5*QGRID[iq]*lr)
            if (ir, iq) in K2cols:
                col = np.array([sparc_ok(f, cs_of(ic)) for ic in range(NC)])
                mono = all(not col[k] or col[k + 1] for k in range(NC - 1)); k2ok &= mono; ok[:, ir, iq] = col; continue
            if not sparc_ok(f, cs_of(NC - 1)): continue
            if sparc_ok(f, cs_of(0)): ok[:, ir, iq] = True; continue
            lo, hi = 0, NC - 1
            while hi - lo > 1:
                md = (lo + hi)//2; (lo, hi) = (lo, md) if sparc_ok(f, cs_of(md)) else (md, hi)
            ok[hi:, ir, iq] = True
    PASS[f]["C-SPARC"] = bc(ok)
    say(f"  SPARC graded {f} [{time.time()-t1:.0f} s]")
check("K2", k2ok, f"SPARC d2 pass is monotone (non-decreasing) in c_* on {len(K2cols)} full (r, q) columns x 2 footings", "monotone")
# --- cosmic medium: thresholds on a p_eff grid
SIG_COS1 = math.sqrt(G946*X22J["step1"]["alpha_NF"]["M_hm_Msun"]*MSUN946/(2*X22J["step1"]["alpha_NF"]["R_hm_Mpc_h"]/HH*MPC946))/1e3
RHOB0 = OB946*RHOC_946*PC946**3/MSUN946
say(f"  cosmic medium: sigma_cos(a=1) = {SIG_COS1:.3f} km/s (sigma_cos(z=3) = {SIG_COS1*2:.2f}); rho_b,0 = {RHOB0:.4e} Msun/pc^3")
PE_GRID = np.arange(-0.5, 8.5001, 0.125)
def bisect_C(pe, okfn, lo=-6.0, hi=5.5, steps=11):
    """largest log10 C0 with okfn True (ok at small C0, monotone: X22 C3). The upper end (c_s ~ c) is never evaluated directly
    (stiff); a result within one step of it is reported as +inf, one within a step of the lower end is checked there."""
    lo0, hi0 = lo, hi
    for _ in range(steps):
        md = 0.5*(lo + hi); (lo, hi) = (md, hi) if okfn(10**md, pe) else (lo, md)
    if hi0 - lo <= (hi0 - lo0)/2**steps + 1e-12: return float("inf")
    if lo - lo0 <= 1e-12 and not okfn(10**lo0, pe): return -float("inf")
    return lo
t1 = time.time()
okF = lambda C0, pe: grade_forest(lambda a: C0*a**(pe - 0.5)) != "FAIL"
okP = lambda C0, pe: grade_forest(lambda a: C0*a**(pe - 0.5)) == "PASS"
okS = lambda C0, pe: grade_s8(lambda a: C0*a**(pe - 0.5)) >= 0.95
def prog(fn, lab):
    out = []
    for k, pe in enumerate(PE_GRID):
        out.append(fn(pe))
        if k % 12 == 11: print(f"    {lab} node {k+1}/{len(PE_GRID)} [{time.time()-t1:.0f} s]", flush=True)
    return np.array(out)
THF = prog(lambda pe: bisect_C(pe, okF), "forest"); say(f"  forest (not FAIL) thresholds on {len(PE_GRID)} p_eff nodes [{time.time()-t1:.0f} s]")
THP = prog(lambda pe: bisect_C(pe, okP), "forest PASS"); say(f"  forest strict PASS thresholds (reported) [{time.time()-t1:.0f} s]")
THS = prog(lambda pe: bisect_C(pe, okS, steps=9), "sigma8"); say(f"  sigma8 thresholds [{time.time()-t1:.0f} s]")
def interp_th(TH, pe):
    T = np.clip(TH, -99.0, 99.0); return np.interp(pe, PE_GRID, T)                          # +-inf (always / never ok) kept as +-99
PEF = np.array(PGRID)[None, None, None, :] - RGRID[None, :, None, None]/2 - 1.5*QGRID[None, None, :, None]
LC0 = LCS[:, None, None, None] + RGRID[None, :, None, None]*math.log10(SIG_COS1/SIG_STAR) + 0.5*QGRID[None, None, :, None]*math.log10(RHOB0/RHO_STAR)
LC0 = np.broadcast_to(LC0, SHAPE); PEF = np.broadcast_to(PEF, SHAPE)
for f in FEET:
    PASS[f]["C-forest"] = LC0 <= interp_th(THF, PEF)
    PASS[f]["C-s8"] = LC0 <= interp_th(THS, PEF)
    a1100 = 1/1101; Hz = H0_946*math.sqrt(OM946*1101**3)
    lcs1100 = LC0 + (PEF - 0.5)*math.log10(a1100)
    kJ = a1100*Hz/(10**lcs1100*1e3)*MPC946/HH
    PASS[f]["C-CMB"] = kJ >= 1.0
    # FP1 hard (q > -1) and FP2 computed causality (graded systems + cosmic medium z <= 1100)
    PASS[f]["FP1"] = np.broadcast_to((QGRID > -1 + 1e-12)[None, None, :, None], SHAPE).copy()
    lmax = np.full(SHAPE, -np.inf)
    for sig, rho in [(SIG_SP, RHO_SP[f]), (SIG_KT, CEL[(f, "h0672")]["rho"]), (DW[f]["sc"], DW[f]["rho"])] + \
                    [([class_row(f, c)["sig"]], [class_row(f, c)["rho"]]) for c in CLS]:
        lmax = np.maximum(lmax, bc(np.log10(family_cs(sig, rho)).max(-1)))
    lmax = np.maximum(lmax, np.maximum(LC0, lcs1100))
    PASS[f]["FP2"] = lmax < math.log10(CLIGHT/1e3)
say(f"  cosmic + FP1/FP2 graded [{time.time()-T0:.0f} s, RSS {rss():.2f} GB]")
RES["cosmic"] = dict(sigma_cos1_kms=SIG_COS1, rho_b0=RHOB0, p_eff_grid=PE_GRID.tolist(), log10C0_forest_notFAIL=THF.tolist(),
                     log10C0_forest_PASS=THP.tolist(), log10C0_sigma8=THS.tolist())
say("  p_eff : log10 C0 max (forest not FAIL / forest PASS / R_s8 >= 0.95): " + "; ".join(
    f"{pe:.2f}: {THF[k]:.2f}/{THP[k]:.2f}/{THS[k]:.2f}" for k, pe in enumerate(PE_GRID) if abs(pe*2 - round(pe*2)) < 1e-9))
# ============================================================== scenarios, verdict
GRADED_A = ["FP1", "FP2", "C-forest", "C-s8", "C-CMB", "C-SPARC", "C-groups", "C-T1", "C-T2", "C-T3", "C-KTb", "C-dwarfs", "C-MW"]
GRADED_B = [c if c != "C-dwarfs" else "C-dwarfs-c0" for c in GRADED_A]
GRADED_N = [c for c in GRADED_A if c != "C-dwarfs"]                              # reported: no dwarf constraint at all
def allowed(f, cons):
    m = np.ones(SHAPE, bool)
    for c in cons: m &= PASS[f][c]
    return m
def extent(m):
    if not m.any(): return None
    ic, ir, iq, ip = np.where(m)
    return dict(n=int(m.sum()), frac=float(m.mean()), log10_cstar=[float(LCS[ic].min()), float(LCS[ic].max())], r=[float(RGRID[ir].min()), float(RGRID[ir].max())],
                q=[float(QGRID[iq].min()), float(QGRID[iq].max())], p=sorted({PGRID[k] for k in ip}))
def closing(f, cons):
    pairs = [(a, b) for a, b in itertools.combinations(cons, 2) if not (PASS[f][a] & PASS[f][b]).any()]
    if pairs: return dict(pairs=pairs)
    trip = [t for t in itertools.combinations(cons, 3) if not allowed(f, t).any()]
    return dict(pairs=[], triples=trip[:40], n_triples=len(trip))
SC = {}
for f in FEET:
    mA, mB, mN = allowed(f, GRADED_A), allowed(f, GRADED_B), allowed(f, GRADED_N)
    SC[f] = dict(A=extent(mA), B=extent(mB), no_dwarf=extent(mN))
    SC[f]["per_constraint"] = {c: dict(frac=float(PASS[f][c].mean()), ext=extent(PASS[f][c])) for c in GRADED_A + ["C-dwarfs-c0"]}
    if SC[f]["A"] is None: SC[f]["closing_A"] = closing(f, GRADED_A)
    if SC[f]["B"] is None: SC[f]["closing_B"] = closing(f, GRADED_B)
    # leave-one-out: which constraint alone would open the region (scenario B)
    SC[f]["leave_one_out_B"] = {c: extent(allowed(f, [x for x in GRADED_B if x != c])) for c in GRADED_B}
    say(f"\n  [{f}] per-constraint pass fraction: " + "; ".join(f"{c} {SC[f]['per_constraint'][c]['frac']:.3f}" for c in GRADED_A + ['C-dwarfs-c0']))
    say(f"  [{f}] scenario A (family alone): {SC[f]['A']}")
    say(f"  [{f}] scenario B (separate c0): {SC[f]['B']}")
    say(f"  [{f}] no dwarf constraint at all (reported): {SC[f]['no_dwarf']}")
    if "closing_A" in SC[f]: say(f"  [{f}] A closing pairs: {SC[f]['closing_A'].get('pairs')}" + (f"; triples ({SC[f]['closing_A'].get('n_triples')}): {SC[f]['closing_A'].get('triples')[:12]}" if not SC[f]['closing_A'].get('pairs') else ""))
    if "closing_B" in SC[f]: say(f"  [{f}] B closing pairs: {SC[f]['closing_B'].get('pairs')}" + (f"; triples ({SC[f]['closing_B'].get('n_triples')}): {SC[f]['closing_B'].get('triples')[:12]}" if not SC[f]['closing_B'].get('pairs') else ""))
    say(f"  [{f}] B leave-one-out (dropping one constraint opens): " + "; ".join(f"-{c}: {'n=' + str(v['n']) if v else 'empty'}" for c, v in SC[f]["leave_one_out_B"].items()))
RES["scenarios"] = SC
# ============================================================== boundary table: per (r, q) the allowed c_* interval per constraint (p = 4 and min over p)
say("\n=== BOUNDARY TABLE (log10 c_* interval allowed per constraint; '-' none; '*' all; p = 3 / 4 / 6 shown where the constraint depends on p) ===")
def ivl(col):
    if not col.any(): return "-"
    if col.all(): return "*"
    k = np.where(col)[0]; s = f"{LCS[k[0]]:.2f}..{LCS[k[-1]]:.2f}"
    return s if len(k) == k[-1] - k[0] + 1 else s + "(gap)"
BT = {}
RSHOW = [-1.0, -0.5, 0.0, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0]; QSHOW = [-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 1.0]
for f in FEET:
    BT[f] = {}
    for rv in RSHOW:
        for qv in QSHOW:
            ir = int(np.argmin(np.abs(RGRID - rv))); iq = int(np.argmin(np.abs(QGRID - qv))); row = {}
            for c in GRADED_B + ["C-dwarfs"]:
                row[c] = "/".join(ivl(PASS[f][c][:, ir, iq, ip]) for ip in range(NP)) if c in ("C-forest", "C-s8", "C-CMB", "FP2") else ivl(PASS[f][c][:, ir, iq, 0])
            row["ALL_B"] = "/".join(ivl(allowed(f, GRADED_B)[:, ir, iq, ip]) for ip in range(NP))
            row["ALL_A"] = "/".join(ivl(allowed(f, GRADED_A)[:, ir, iq, ip]) for ip in range(NP))
            BT[f][f"r={rv:+.2f},q={qv:+.2f}"] = row
            if f == "canonical" or rv in (0.0, 1.0):
                say(f"  {f} r {rv:+.2f} q {qv:+.2f}: " + " | ".join(f"{c} {v}" for c, v in row.items()))
RES["boundary_table"] = BT
# per-constraint (r, q) extents at fixed p = 4: allowed somewhere in c_*
say("\n=== per-constraint (r, q) footprint (any c_*, p = 4): rows r, columns q; '#' allowed somewhere ===")
FOOT = {}
for f in FEET:
    FOOT[f] = {}
    for c in GRADED_B + ["C-dwarfs"]:
        m = PASS[f][c][..., 1].any(0); FOOT[f][c] = m.tolist()
    mB = allowed(f, GRADED_B)[..., 1].any(0); FOOT[f]["ALL_B_p4"] = mB.tolist()
    for c in ("C-SPARC", "C-T2", "C-T3", "C-KTb", "C-forest", "C-dwarfs", "ALL_B_p4"):
        m = np.array(FOOT[f][c]); say(f"  {f} {c:10s} q " + "".join("+" if v >= 0 else "-" for v in QGRID))
        for ir in range(0, NR, 2): say(f"    r {RGRID[ir]:+.2f} " + "".join("#" if m[ir, iq] else "." for iq in range(NQ)))
RES["footprints_p4"] = FOOT
# ============================================================== special cases
say("\n=== SPECIAL CASES ===")
SPC = {}
def at(f, cons, rv, qv):
    ir = int(np.argmin(np.abs(RGRID - rv))); iq = int(np.argmin(np.abs(QGRID - qv))); m = allowed(f, cons)[:, ir, iq, :]
    return dict(any=bool(m.any()), cstar_allowed=[float(x) for x in LCS[m.any(1)]], fails_at_100kms={c: bool(not PASS[f][c][16, ir, iq, 1]) for c in cons})
for f in FEET:
    SPC[f] = {"universal r=q=0 (A)": at(f, GRADED_A, 0, 0), "universal r=q=0 (B)": at(f, GRADED_B, 0, 0),
              "virial r=1,q=0 (A)": at(f, GRADED_A, 1, 0), "virial r=1,q=0 (B)": at(f, GRADED_B, 1, 0)}
    vb = SPC[f]["virial r=1,q=0 (B)"]
    say(f"  {f} universal (r=q=0): A any {SPC[f]['universal r=q=0 (A)']['any']}, B any {SPC[f]['universal r=q=0 (B)']['any']}")
    say(f"  {f} virial (r=1, q=0): A any {SPC[f]['virial r=1,q=0 (A)']['any']}, B any {vb['any']}; at c_* = 100 km/s (c_s = sigma) fails: "
        + ", ".join(c for c, v in vb["fails_at_100kms"].items() if v))
    ir1 = int(np.argmin(np.abs(RGRID - 1))); iq0 = int(np.argmin(np.abs(QGRID)));
    say(f"  {f} virial line r=1,q=0: per-constraint allowed log10 c_* (p=4): " + "; ".join(f"{c} {ivl(PASS[f][c][:, ir1, iq0, 1])}" for c in GRADED_A))
    # dwarf floor equivalence: any (c_*, r, q) passing C-dwarfs, and does it survive the rest?
    md = PASS[f]["C-dwarfs"][..., 0]
    SPC[f]["dwarf_floor_equivalent_points"] = int(md.sum()); SPC[f]["dwarf_floor_equivalent_extent"] = extent(PASS[f]["C-dwarfs"])
    mins = float(EFAM[f]["dw_chi"].min())
    say(f"  {f} dwarf floor: (c_*, r, q) with chi2_fam <= chi2_floor ({DW[f]['chi_floor']:.1f}) and negative mass trend: {int(md.sum())} of {md.size}"
        f"; extent {extent(PASS[f]['C-dwarfs'])}; (diagnostic, not a result: smallest chi2_fam on the grid {mins:.1f}, law-only chi2 "
        f"{float((((DW[f]['E'])/DW[f]['s'])**2).sum()):.1f})")
    say(f"  {f} X24b VHC (r=0, q=-1, p=2): marked EXCLUDED by its own lane ('{X24bJ['verdict']}'); q = -1 is also the FP1 edge (dP/drho = 0); p = 2 is below X22's forest band")
RES["special_cases"] = SPC
# ============================================================== energy (reported)
say("\n=== ENERGY (reported; over the scenario-B allowed set) ===")
EN = {}
for f in FEET:
    mB = allowed(f, GRADED_B)
    medS = (float(np.median(SIG_SP)), float(np.median(RHO_SP[f]))); medK = (float(np.median(SIG_KT)), float(np.median(CEL[(f, "h0672")]["rho"])))
    out = {}
    for nm, (sg, rh) in (("SPARC median", medS), ("KT cluster median", medK)):
        cs = np.broadcast_to(family_cs([sg], [rh])[..., 0][..., None], SHAPE)
        if mB.any():
            v = cs[mB]; e = 1.5*(v*1e3)**2
            out[nm] = dict(cs_kms=[float(v.min()), float(v.max())], frac_rhoLambda=[float(1.5*OC946/OL946*(v.min()*1e3)**2/CLIGHT**2), float(1.5*OC946/OL946*(v.max()*1e3)**2/CLIGHT**2)],
                           keV_per_baryon=[float(5.364*e.min()*MP/KEV), float(5.364*e.max()*MP/KEV)])
            say(f"  {f} {nm} (sigma {sg:.1f} km/s, rho_b {rh:.2e}): c_s {v.min():.0f}-{v.max():.0f} km/s; (3/2) Omega_c c_s^2/(Omega_L c^2) "
                f"{out[nm]['frac_rhoLambda'][0]:.2e}-{out[nm]['frac_rhoLambda'][1]:.2e}; per baryon {out[nm]['keV_per_baryon'][0]:.2f}-{out[nm]['keV_per_baryon'][1]:.2f} keV")
        else:
            out[nm] = None; say(f"  {f} {nm}: no allowed point")
    EN[f] = out
RES["energy"] = EN
# ============================================================== FP overlays (FP3 virial separability; FP4 Part F vs graded forest)
say("\n=== FIRST-PRINCIPLES OVERLAYS ===")
DER = json.load(open(os.path.join(HERE, "x26_derive_results.json"))); RES["derive"] = {k: DER[k] for k in ("p_eff", "FP1", "FP2", "FP3", "FP4")}
FP3 = {}
for f in FEET:
    # retained (c_s <= sqrt(2/3) sigma) wanted: T2, T3 (KT tercile medians); expelled wanted: SPARC small, SPARC large, groups, T1, MW disc
    sigT = [float(np.median(SIG_KT[TID == t])) for t in range(3)]; rhoT = [float(np.median(CEL[(f, "h0672")]["rho"][TID == t])) for t in range(3)]
    rows = {"T2": (sigT[1], rhoT[1], -1), "T3": (sigT[2], rhoT[2], -1), "T1": (sigT[0], rhoT[0], +1)}
    for c in ("SPARC small", "SPARC large", "Groups", "MW disc"): cr = class_row(f, c); rows[c] = (cr["sig"], cr["rho"], +1)
    rowsD = dict(rows); rowsD["dwarfs (74 median)"] = (float(np.median(DW[f]["sc"])), float(np.median(DW[f]["rho"])), -1)
    def sep(rws):
        m = np.ones((NC, NR, NQ), bool)
        for sg, rh, sgn in rws.values():
            v = family_cs([sg], [rh])[..., 0]/sg - math.sqrt(2/3); m &= (v > 0) if sgn > 0 else (v <= 0)
        return m
    mB3, mA3 = sep(rows), sep(rowsD)
    FP3[f] = dict(B_any=bool(mB3.any()), A_any=bool(mA3.any()), B_rq=extent(bc(mB3)), A_rq=extent(bc(mA3)))
    say(f"  {f} FP3 virial separability (class medians): clusters T2/T3 bound, SPARC/groups/T1/MW unbound: {'possible' if mB3.any() else 'IMPOSSIBLE'} {FP3[f]['B_rq']}; "
        f"plus dwarfs bound: {'possible' if mA3.any() else 'IMPOSSIBLE'} {FP3[f]['A_rq']}")
    # FP4: compare graded forest cut with q <= (2/3)(p - r/2 - p_min)
    fr = PASS[f]["C-forest"]
say("  FP4: the graded forest cut is the p_eff = p - r/2 - 3q/2 threshold table above (Part F carried to the family)")
RES["FP3"] = FP3
# ============================================================== A2 (post-result check): direct cluster grades at every allowed point and its c_* neighbours
say("\n=== A2: direct (non-interpolated) cluster grades at every scenario-B allowed (c_*, r, q) and its c_* +- 1 neighbours ===")
t1 = time.time(); A2 = {}; k5ok = True
def direct_grades(f, ic, ir, iq):
    out = {}; okT = [True]*3; okB = True; zs = {}
    for hk in HK:
        c = CEL[(f, hk)]; cl = f"{f}|{hk}"; ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]; tv = X21J["tests"]["V1"]["cells"][cl]
        Am = list(ref["A"]); sm = list(ref["s"])
        if MUT: Am, sm = Am[::-1], sm[::-1]
        csv_ = 10**(LCS[ic] + RGRID[ir]*np.log10(SIG_KT/SIG_STAR) + 0.5*QGRID[iq]*np.log10(c["rho"]/RHO_STAR))
        dD = np.array([d_lhc(i, f, hk, float(cs)) for i, cs in zip(I, csv_)]); PREP.clear()
        Ap = [float(dD[TID == t].sum()/c["d"][TID == t].sum()) for t in range(3)]; bp = float(wls1(dD, c["d"], X1m)[1])
        for t in range(3): okT[t] &= abs(Am[t] - Ap[t]) <= 2*sm[t]
        okB &= abs(tv["b"] - bp) <= 2*tv["s_b"]
        zs[hk] = dict(A_pred=Ap, Z_t=[(Am[t] - Ap[t])/sm[t] for t in range(3)], b_pred=bp, Z_b=(tv["b"] - bp)/tv["s_b"],
                      cs_median_kms=float(np.median(csv_)))
    out.update({"C-T1": okT[0], "C-T2": okT[1], "C-T3": okT[2], "C-KTb": okB}); return out, zs
for f in FEET:
    mB = allowed(f, GRADED_B).any(-1); pts = set(zip(*np.where(mB)))
    nb = set()
    for ic, ir, iq in pts:
        for d in (-1, 1):
            if 0 <= ic + d < NC: nb.add((ic + d, ir, iq))
    A2[f] = []; nflip = 0
    for (ic, ir, iq) in sorted(pts | nb):
        g, zs = direct_grades(f, ic, ir, iq)
        interp = {c: bool(PASS[f][c][ic, ir, iq, 0]) for c in ("C-T1", "C-T2", "C-T3", "C-KTb")}
        flip = [c for c in g if g[c] != interp[c]]; nflip += len(flip)
        A2[f].append(dict(log10_cstar=float(LCS[ic]), r=float(RGRID[ir]), q=float(QGRID[iq]), allowed=(ic, ir, iq) in pts, direct=g, interp=interp, flips=flip, detail=zs))
        if (ic, ir, iq) in pts or flip:
            z0 = zs["h0672"]; z1 = zs["h0686"]
            say(f"  {f} c_* 10^{LCS[ic]:.3f} r {RGRID[ir]:+.3f} q {QGRID[iq]:+.3f} {'ALLOWED ' if (ic, ir, iq) in pts else 'neighbour'}: cluster c_s median {z0['cs_median_kms']:.0f} km/s; "
                f"Z_t h0.672 " + "/".join(f"{z:+.2f}" for z in z0["Z_t"]) + f", Z_b {z0['Z_b']:+.2f}; h0.686 " + "/".join(f"{z:+.2f}" for z in z1["Z_t"]) + f", Z_b {z1['Z_b']:+.2f}"
                + (f"  FLIP (direct differs from table): {flip}" if flip else ""))
    k5ok &= nflip == 0
    say(f"  {f}: {len(pts)} allowed (c_*, r, q) + {len(nb - pts)} neighbours checked directly; grade flips {nflip}")
RES["A2_direct"] = A2
check("K5", k5ok, f"A2: direct cluster grades equal the table's at every allowed point and its c_* neighbours [{time.time()-t1:.0f} s]", "0 flips")
# ============================================================== A3 (post-result, reported only): MGAS500 terciles at r = 0 allowed points; fine universal scan
say("\n=== A3 (reported only): X7 MGAS500 terciles (all 326 clusters) at the r = 0 allowed points; fine universal (r = q = 0) cluster scan ===")
t1 = time.time(); A3 = {}
X7J = json.load(open(os.path.join(REB, "X7_cluster_core_significance", "x7_analysis_results.json")))
Mgl = np.asarray(MY["Mgas500"], float); T3M = np.digitize(Mgl, np.quantile(Mgl, [1/3, 2/3])); ALLI = np.arange(N)
NDALL = {}
for f, hk in CELLS:
    dd = DAT[hk]; WB = dd["W"]*dd["B"][None, :]; hx = HXI[hk]
    nA = np.array([(WB[i, JM]*(dd["D"][i, JM] - MY["leakP"][i, hx, 0][JM])).sum() for i in ALLI]); dA = np.array([dmid(i, f, hk, None) for i in ALLI])
    rhoA = np.array([float(np.interp(0.548, RG, prep(i, f, hk)["Mb"]))/MSUN for i in ALLI])/(4/3*math.pi*(0.548e6)**3); PREP.clear()
    NDALL[(f, hk)] = (nA, dA, rhoA)
for f in FEET:
    A3[f] = {"mgas_r0": [], "universal_scan": []}
    pts = sorted({(ic, ir, iq) for ic, ir, iq, ip in zip(*np.where(allowed(f, GRADED_B))) if abs(RGRID[ir]) < 1e-12})
    for ic, ir, iq in pts:
        row = {}
        for hk in HK:
            nA, dA, rhoA = NDALL[(f, hk)]; r7 = X7J["bins"][f"terciles|{f}|{hk}"]
            csA = 10**(LCS[ic] + 0.5*QGRID[iq]*np.log10(rhoA/RHO_STAR))
            dL = np.array([d_lhc(i, f, hk, float(cs)) for i, cs in zip(ALLI, csA)]); PREP.clear()
            Ap = [float(dL[T3M == t].sum()/dA[T3M == t].sum()) for t in range(3)]
            row[hk] = dict(A_pred=Ap, A_meas=[r_["MID"]["A_CAL"] for r_ in r7], Z=[(r_["MID"]["A_CAL"] - a)/r_["MID"]["s_CAL"] for a, r_ in zip(Ap, r7)])
        A3[f]["mgas_r0"].append(dict(log10_cstar=float(LCS[ic]), q=float(QGRID[iq]), cells=row))
        say(f"  {f} MGAS500 terciles at c_* 10^{LCS[ic]:.3f}, r 0, q {QGRID[iq]:+.3f}: h0.672 A_pred " + "/".join(f"{a:.2f}" for a in row["h0672"]["A_pred"])
            + " vs " + "/".join(f"{a:.2f}" for a in row["h0672"]["A_meas"]) + " (Z " + "/".join(f"{z:+.2f}" for z in row["h0672"]["Z"]) + "); h0.686 Z "
            + "/".join(f"{z:+.2f}" for z in row["h0686"]["Z"]))
    for cs in np.geomspace(500.0, 1000.0, 36):
        ok = {"KT": True, "MGAS": True}; zz = {}
        for hk in HK:
            c = CEL[(f, hk)]; cl = f"{f}|{hk}"; ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]; tv = X21J["tests"]["V1"]["cells"][cl]
            Am = list(ref["A"])[::-1] if MUT else list(ref["A"]); sm = list(ref["s"])[::-1] if MUT else list(ref["s"])
            nA, dA, rhoA = NDALL[(f, hk)]; dL = np.array([d_lhc(i, f, hk, float(cs)) for i in ALLI]); PREP.clear()
            dK = dL[I]; Ap = [float(dK[TID == t].sum()/c["d"][TID == t].sum()) for t in range(3)]; bp = float(wls1(dK, c["d"], X1m)[1])
            ZK = [(Am[t] - Ap[t])/sm[t] for t in range(3)]; Zb = (tv["b"] - bp)/tv["s_b"]
            ok["KT"] &= all(abs(z) <= 2 for z in ZK) and abs(Zb) <= 2
            r7 = X7J["bins"][f"terciles|{f}|{hk}"]; ApM = [float(dL[T3M == t].sum()/dA[T3M == t].sum()) for t in range(3)]
            ZM = [(r_["MID"]["A_CAL"] - a)/r_["MID"]["s_CAL"] for a, r_ in zip(ApM, r7)]; ok["MGAS"] &= all(abs(z) <= 2 for z in ZM)
            zz[hk] = dict(ZK=ZK, Zb=Zb, ZM=ZM)
        A3[f]["universal_scan"].append(dict(cs=float(cs), ok=ok, Z=zz))
    okK = [e["cs"] for e in A3[f]["universal_scan"] if e["ok"]["KT"]]; okM = [e["cs"] for e in A3[f]["universal_scan"] if e["ok"]["MGAS"]]
    both = [e["cs"] for e in A3[f]["universal_scan"] if e["ok"]["KT"] and e["ok"]["MGAS"]]
    rng_ = lambda v: f"{min(v):.0f}-{max(v):.0f} km/s ({len(v)} of 36)" if v else "none"
    say(f"  {f} universal c_s scan 500-1000 km/s (2 % steps, direct): KT terciles + slope pass at {rng_(okK)}; X7 MGAS500 terciles pass at {rng_(okM)}; both at {rng_(both)}")
    A3[f]["universal_KT_pass_kms"] = okK; A3[f]["universal_MGAS_pass_kms"] = okM; A3[f]["universal_both_kms"] = both
RES["A3_reported"] = A3; say(f"  [A3 {time.time()-t1:.0f} s]")
# ============================================================== verdict
def cls_f(f):
    if SC[f]["A"] is not None: return "ALLOWED REGION EXISTS"
    if SC[f]["B"] is not None: return "ALLOWED ONLY WITH SEPARATE c0"
    return "EMPTY"
VC = {f: cls_f(f) for f in FEET}
if STOP: V = "UNDECIDED (step 0 failed)"
elif VC["canonical"] == VC["alt"]: V = VC["canonical"]
else: V = f"UNDECIDED (footings disagree: canonical {VC['canonical']}, alt {VC['alt']})"
RES["verdict"] = V; RES["verdict_per_footing"] = VC
check("K3", all(DER["checks"].values()), f"x26_derive.py checks {sum(DER['checks'].values())}/{len(DER['checks'])}", "all")
check("K4", rss() < 1.0, f"peak RSS {rss():.3f} GB", "< 1 GB")
say(f"\nVERDICT: {V}  (per footing: {VC})")
if MUT:
    must = ("K0a", "K0c"); RES["mutate_required_fail"] = {k: not CHECKS[k] for k in must}
    say("MUTATE: required failures " + ", ".join(f"{k} {'FAILED' if not CHECKS[k] else 'passed (BAD)'}" for k in must))
RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss()
say(f"checks {sum(CHECKS.values())}/{len(CHECKS)} PASS; runtime {RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_GB']:.2f} GB")
np.savez_compressed(os.path.join(HERE, f"x26_pass_masks{TAG}.npz"), LCS=LCS, R=RGRID, Q=QGRID, P=np.array(PGRID),
                    **{f"{f}|{c}": PASS[f][c] for f in FEET for c in PASS[f]})
json.dump(RES, open(os.path.join(HERE, f"x26_cold_sector_map_results{TAG}.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else (o.tolist() if hasattr(o, "tolist") else str(o)))
sys.exit(0 if (all(CHECKS.values()) and not MUT) else 1)

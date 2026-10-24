"""X23_late_heated_cold (criteria b8d81770bb): late-heated cold energy (LHC) on the KT-keyed cluster test.
c_s(z=0) = X22's c_s,need (read from X22's JSON, never fitted). For X21's 106 KT clusters, an isothermal cold fluid sits in the C*
potential (law + baryons + noclu EFE, X2's model), normalised to the mass-conserving fair share 5.364 M_b inside r_ta, sources AQUAL
with the baryons and lenses. Predicted KT-tercile A_MID and KT slope vs X21's measured ones, 4 cells, footings never pooled.
Inputs (read-only): X2's source (functions exec'd as X21 does), X7's per-cluster npz, eRASS1 FITS, X21 / X22 / peer-lane JSONs.
Usage: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x23_late_heated_cold.py   (X23_MUTATE=1: MUTATE twin, exit 1)
kappa = 1/2 FITTED; footings never pooled; cold energy = field mass, no dark-matter particle; not theory closed."""
import os, sys
import json, math, time, hashlib, resource
sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[_v] = "1"
import numpy as np
from astropy.io import fits
T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE); REPO = os.path.dirname(REB)
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("X23_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"x23_late_heated_cold{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"lane": "X23_late_heated_cold", "criteria": "b8d81770bb", "mutate": MUT}; CHECKS = {}
def check(name, ok, val, thr):
    CHECKS[name] = bool(ok); say(f"{name} {'PASS' if ok else 'FAIL'}: {val}   (line: {thr})")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
say("X23_late_heated_cold" + (" [MUTATE m1-m3: control output, not physics]" if MUT else "") +
    ": criteria b8d81770bb; kappa = 1/2 FITTED; footings never pooled; field mass, no particle; not theory closed")
# ============================================================== X2's functions, exec'd read-only (exactly as X21 does)
X2DIR = os.path.join(REB, "X2_cluster_outskirts"); X2SRC = os.path.join(X2DIR, "x2_cluster_outskirts.py"); TX = open(X2SRC).read()
RES["x2_source_sha256"] = sha(X2SRC)
def cutx(a, b): i = TX.index(a); j = TX.index(b, i); return TX[i:j]
NS2 = {"np": np, "os": os, "sys": sys, "math": math, "json": json, "time": time, "REB": REB, "REPO": REPO, "HERE": X2DIR,
       "LANES": LANES, "MUT": False, "RES": {}, "say": (lambda *a: None), "check": (lambda *a: None),
       "sha": sha, "rss": rss, "guard": (lambda tag: None)}
exec(cutx("# ============================================================== F1's own functions", "# ============================================================== data: the replay"), NS2)
exec(cutx("# ============================================================== data: the replay", "# ============================================================== statistics"), NS2)
exec(cutx("# ============================================================== statistics", "# ============================================================== EFE"), NS2)
exec(cutx('sys.path.insert(0, os.path.join(REB, "F2_outer_lensing"))', 'for f in FEET:\n    for k in ("noclu", "maxclu", "p2cat"):'), NS2)
exec(cutx("# ============================================================== the model", "# ============================================================== K2, K3, K7"), NS2)
FEET, HK = ("canonical", "alt"), ("h0672", "h0686"); CELLS = [(f, h) for f in FEET for h in HK]
for f in FEET:
    t1 = time.time(); NS2["CTAB"][(f, "noclu")] = NS2["ctable"](NS2["AQ"].solve_efe(NS2["YE"][f]["noclu"], maxit=3000))
    say(f"EFE solve (X2's) {f} noclu [{time.time()-t1:.0f} s]")
G, MSUN, MPC, KG_PC2, A0 = NS2["G"], NS2["MSUN"], NS2["MPC"], NS2["KG_PC2"], NS2["A0"]
RG, RM, RC = NS2["RG"], NS2["RM"], NS2["RC"]
gas, g_aqual_sph, Cof, CTAB = NS2["gas"], NS2["g_aqual_sph"], NS2["Cof"], NS2["CTAB"]
project_floor, offset_floor, dsig_from_sig, at_bins, sig_bins = (NS2[k] for k in ("project_floor", "offset_floor", "dsig_from_sig", "at_bins", "sig_bins"))
DM, DA_lcdm, HV = NS2["DM"], NS2["DA_lcdm"], NS2["HV"]
# ============================================================== X7's per-cluster arrays (never re-measured), X21's DAT construction
X7DIR = os.path.join(REB, "X7_cluster_core_significance"); NPZ = os.path.join(X7DIR, "x7_measure_percluster.npz")
MY = np.load(NPZ); RES["x7_npz_sha256"] = sha(NPZ); N = len(MY["name"])
HI = {"h0672": 1, "h0686": 2}; HXI = {"h0672": 0, "h0686": 1}; DAT = {}
for hk in HK:
    i = HI[hk]; W = np.where(MY["E"][:, i] < 1e8, 1/MY["E"][:, i]**2, 0); B = MY["den"][:, i].sum(0)/MY["den_r"][:, i].sum(0)
    DAT[hk] = dict(D=MY["D"][:, i], W=W, B=B, Dx=MY["Dx"][:, i], Wx=W, DRR=MY["DRR"][:, i], m2=MY["den"][:, i], m=MY["m3to8"][:, i])
NS2["DAT"] = DAT; CL = NS2["CL"]; JM = NS2["BANDS"]["MID"]; redfac = NS2["redfac"]
assert [c["name"] for c in CL] == [str(x) for x in MY["name"]]
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); RES["erass1_sha256"] = sha(EF)
E = fits.open(EF)[1].data; idx = {str(s).strip(): k for k, s in enumerate(E["NAME"])}
KT = np.asarray(E["KT"], float)[np.array([idx[str(x).strip()] for x in MY["name"]])]
if MUT: KT = KT[np.random.default_rng(2323).permutation(N)]                                       # m2: KT labels shuffled
I = np.where(np.isfinite(KT) & (KT > 0))[0]; nI = len(I); x = np.log10(KT[I]/np.median(KT[I]))
TID = np.digitize(x, np.quantile(x, [1/3, 2/3]))
X21J = json.load(open(os.path.join(REB, "X21_cluster_switch_anatomy", "x21_switch_anatomy_results.json")))
X22J = json.load(open(os.path.join(REB, "X22_cosmic_dust_window", "x22_cosmic_dust_window_results.json")))
PEERJ = json.load(open(os.path.join(REB, "X23_late_heating_graded", "x23_late_heating_graded_results.json")))
for nm, p in (("X21", "X21_cluster_switch_anatomy/x21_switch_anatomy_results.json"), ("X22", "X22_cosmic_dust_window/x22_cosmic_dust_window_results.json"),
              ("peer", "X23_late_heating_graded/x23_late_heating_graded_results.json")):
    RES[f"{nm}_json_sha256"] = sha(os.path.join(REB, p))
say(f"KT clusters {nI}; KT tercile edges {np.quantile(KT[I], [1/3, 2/3]).round(3).tolist()} keV (X21 {X21J['binned']['V1']['terciles']['edges']})")
# ============================================================== constants for r_ta and the cosmic mean (X22's CFG946 set, verbatim values)
G946, MSUN946, MPC946 = 6.67430e-11, 1.98847e30, 3.0856775814913673e22
H0_946 = 67.4e3/MPC946; RHOC_946 = 3*H0_946**2/(8*math.pi*G946); OB946 = 0.0493; OC946 = 5.364*OB946; OM946 = OB946 + OC946
RHOM946 = OM946*RHOC_946; DTA = 5.55
def r_ta_com(Mb_kg): return (3*(OM946/OB946)*Mb_kg/(4*math.pi*DTA*RHOM946))**(1/3)              # X22's r_ta (m, comoving)
CS = {f: float(X22J["step2"]["per_footing"][f]["cs_need_kms"]) for f in FEET}
MU, MP, KEV = 0.6, 1.67262192e-27, 1.602176634e-16
SIG_KT = np.full(N, np.nan); SIG_KT[I] = np.sqrt(KT[I]*KEV/(MU*MP))/1e3                          # km/s (bracket / m1)
# ============================================================== hydrostatic solver (derived: c_s^2 dln rho/dr = -g)
def lnrho_profile(g, r_m, rta_m, cs_ms):
    """ln(rho/rho(r_ta)) = int_r^{r_ta} g dr' / c_s^2 on the grid; m3 flips the sign."""
    Ic = np.r_[0, np.cumsum(0.5*(g[1:] + g[:-1])*np.diff(r_m))]
    out = (np.interp(rta_m, r_m, Ic) - Ic)/cs_ms**2
    return -out if MUT else out
def cold_mass(g, r_m, rta_m, cs_ms, Mfair, ln_rhobar=None):
    """norm 'fair' (ln_rhobar None): M_c(<r_ta) = Mfair (frozen section 2). A1 scan: rho_n = min(cosmic mean at r_ta, fair share)."""
    lr = lnrho_profile(g, r_m, rta_m, cs_ms); inside = r_m <= rta_m
    lmax = float(lr[inside].max()); w = np.where(inside, np.exp(lr - lmax), 0.0)
    dm = 4*np.pi*r_m**2*w; Mw = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r_m))]
    Mrta = float(np.interp(rta_m, r_m, Mw)); shape = np.minimum(Mw/Mrta, 1.0)
    ln_cos = (ln_rhobar + lmax + math.log(Mrta)) if ln_rhobar is not None else float("inf")
    capped = ln_cos >= math.log(Mfair)
    Mtot = Mfair if capped else math.exp(ln_cos)
    return shape*Mtot, lr, Mrta, lmax, capped
# K2: Newtonian point mass closed form; uniform limit
Mpt_t = 1e14*MSUN; rta_t = 5*MPC; cs_t = 3e5
lr_t = lnrho_profile(G*Mpt_t/RM**2, RM, rta_t, cs_t); sel = (RG > 0.05) & (RG < 5)
cf = G*Mpt_t/cs_t**2*(1/RM - 1/rta_t)
k2a = float(np.max(np.abs(lr_t[sel] - cf[sel])/np.abs(cf[sel]).max()))
lr_u = lnrho_profile(G*Mpt_t/RM**2, RM, rta_t, 1e11); k2b = float(np.max(np.abs(lr_u[sel])))
check("K2", k2a <= 1e-4 and k2b <= 1e-6, f"point mass: max |ln rho - GM/c_s^2 (1/r - 1/r_ta)| / max = {k2a:.2e}; c_s = 1e8 km/s: max |ln rho| = {k2b:.2e}", "<= 1e-4 (A2); <= 1e-6")
# ============================================================== the model (X2's `model` body for comp=None, with M_src = M_b + M_c)
PREP = {}
def prep(i, foot, hk):
    key = (i, foot, hk)
    if key in PREP: return PREP[key]
    cl = CL[i]; h = HV[hk]; a0 = A0[foot]; q = (float(DM(cl["z"], h))/(1 + cl["z"]))/DA_lcdm(cl["z"])
    Mg500 = cl["Mgas500"]*q**2.5; R500 = cl["R500"]*q
    Mg, rho_g = gas(Mg500, R500, "P"); Mb = Mg*(1 + 0.20); Mbt = float(Mb[-1])
    out = dict(cl=cl, h=h, a0=a0, Mg500=Mg500, R500=R500, Mb=Mb, gb=gfun(Mb, foot), rta=r_ta_com(Mbt)/(1 + cl["z"]), Mfair=5.364*Mbt,
               ln_rhobar=math.log(OC946*RHOC_946*(1 + cl["z"])**3), dmpc=np.radians(cl["off_deg"])*float(DM(cl["z"], h))/(1 + cl["z"]))
    PREP[key] = out; return out
def gfun(Msrc, foot):
    a0 = A0[foot]; gN = G*Msrc/RM**2; g = g_aqual_sph(gN, a0); tab = CTAB[(foot, "noclu")]
    s = RG/(math.sqrt(G*float(np.interp(3.0, RG, Msrc))/a0)/MPC); return g*Cof(tab, s)
def dmid(i, foot, hk, Mc):
    """d_i = sum_MID W P for M_src = M_b (+ M_c); P with X2's projection, offset and reduced shear."""
    pp = prep(i, foot, hk); Msrc = pp["Mb"] if Mc is None else pp["Mb"] + Mc
    g = gfun(Msrc, foot); ML = g*RM**2/G
    rho = np.gradient(ML, RM)/(4*np.pi*RM**2)
    So = offset_floor(project_floor(rho), pp["dmpc"]); P = at_bins(dsig_from_sig(So))/KG_PC2
    fr, _ = redfac(hk, i, sig_bins(So)); return float((DAT[hk]["W"][i, JM]*(P*fr)[JM]).sum())
def lhc(i, foot, hk, cs_kms, scan=False):
    pp = prep(i, foot, hk)
    Mc, lr, Mw, lmax, capped = cold_mass(pp["gb"], RM, pp["rta"], cs_kms*1e3, pp["Mfair"], pp["ln_rhobar"] if scan else None)
    ex = dict(cs=cs_kms, rta=pp["rta"]/MPC, Mfair_Mg500=pp["Mfair"]/(pp["Mg500"]*MSUN), f015=float(np.interp(0.15, RG, Mc)/pp["Mfair"]),
              f05=float(np.interp(0.5, RG, Mc)/pp["Mfair"]), capped=capped,
              log10_uncapped_over_fair=float((pp["ln_rhobar"] + lmax + math.log(Mw) - math.log(pp["Mfair"]))/math.log(10)),
              self_ratio_R500=float(G*np.interp(pp["R500"], RG, Mc)/(pp["R500"]*MPC)**2/np.interp(pp["R500"], RG, pp["gb"])))
    return dmid(i, foot, hk, Mc), ex
# ============================================================== build per-cluster MID sums (X21's n, d) and the LHC d
def wls1(n, d, X):
    F = np.einsum("i,ij,ik->jk", d, X, X); gg = np.einsum("ij,i->j", X, n); return np.linalg.solve(F, gg)
X1 = np.c_[np.ones(nI), x]; CELL = {}; DIAG = {}
ALLI = np.arange(N); INKT = np.zeros(N, bool); INKT[I] = True
FAC = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 13, 16]
for f, hk in CELLS:
    t1 = time.time(); dd = DAT[hk]; WB = dd["W"]*dd["B"][None, :]; hx = HXI[hk]
    n = np.array([(WB[i, JM]*(dd["D"][i, JM] - MY["leakP"][i, hx, 0][JM])).sum() for i in ALLI])
    dC = np.array([dmid(i, f, hk, None) for i in ALLI]); dL = np.zeros(N); dS = np.full(N, np.nan); exL, exS = [], []
    for i in ALLI:
        cs_i = SIG_KT[i] if (MUT and INKT[i]) else CS[f]                                          # m1: c_s := sigma_KT (KT clusters)
        dL[i], e = lhc(i, f, hk, cs_i); exL.append(e) if INKT[i] else None
        if INKT[i]: dS[i], e2 = lhc(i, f, hk, SIG_KT[i]); exS.append(e2)
    SC = np.zeros((len(FAC), N)); ncap = 0
    for k, fa in enumerate(FAC):
        for i in ALLI:
            SC[k, i], e = lhc(i, f, hk, CS[f]*fa, scan=True)
            if k == 0: ncap += int(e["capped"])
    PREP.clear()
    CELL[(f, hk)] = dict(n=n, d=dC, dL=dL, dS=dS, SC=SC, ncap0=ncap); DIAG[(f, hk)] = dict(L=exL, S=exS)
    say(f"  models built {f} {hk}: C*, LHC, sigma_KT bracket, A1 scan x{len(FAC)}; A1 cap binds at c_s,need in {ncap}/{N} clusters [{time.time()-t1:.0f} s, RSS {rss():.2f} GB]")
CELLK = {c: dict(n=v["n"][I], d=v["d"][I], dL=v["dL"][I], dS=v["dS"][I]) for c, v in CELL.items()}
# ============================================================== K0 and K1 (step 0, stop rule)
say("\n=== STEP 0 ===")
dev = []
X7J = json.load(open(os.path.join(REB, "X7_cluster_core_significance", "x7_analysis_results.json")))
Mgl = np.asarray(MY["Mgas500"], float); T3M = np.digitize(Mgl, np.quantile(Mgl, [1/3, 2/3]))
for f, hk in CELLS:
    cf = CELL[(f, hk)]; r7 = X7J["bins"][f"terciles|{f}|{hk}"]
    A7 = [float(cf["n"][T3M == t].sum()/cf["d"][T3M == t].sum()) for t in range(3)]
    dev += [abs(a - r["MID"]["A_CAL"]) for a, r in zip(A7, r7)]
    a7ref = [r["MID"]["A_CAL"] for r in r7]
    say(f"  {f}|{hk}: X7 MGAS500 terciles A_CAL {' / '.join(f'{a:.4f}' for a in A7)} (X7 {' / '.join(f'{a:.4f}' for a in a7ref)})")
for f, hk in CELLS:
    c = CELLK[(f, hk)]; cl = f"{f}|{hk}"; ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]
    A = [float(c["n"][TID == t].sum()/c["d"][TID == t].sum()) for t in range(3)]
    b = float(wls1(c["n"], c["d"], X1)[1]); bref = X21J["tests"]["V1"]["cells"][cl]["b"]
    dev += [abs(a - r) for a, r in zip(A, ref["A"])] + [abs(b - bref)]
    say(f"  {cl}: KT terciles A {' / '.join(f'{a:.4f}' for a in A)} (X21 {' / '.join(f'{a:.4f}' for a in ref['A'])}); slope b {b:+.4f} (X21 {bref:+.4f})")
check("K0", max(dev) <= 1e-9, f"X7 MGAS500 tercile A_CAL, X21 KT tercile A and V1 slope b reproduced, max |dev| {max(dev):.2e} ({len(dev)} numbers)", "<= 1e-9")
csused = {f: sorted({round(e['cs'], 9) for c in CELLS if c[0] == f for e in DIAG[c]['L']}) for f in FEET}
k1 = all(len(csused[f]) == 1 and abs(csused[f][0] - CS[f]) <= 1e-9 for f in FEET)
fr22 = {f: {p: (X22J["step3B"]["per_footing"][f][p]["forest"], X22J["step3B"]["per_footing"][f][p]["R_sigma8"]) for p in ("3.0", "4.0", "6.0")} for f in FEET}
check("K1", k1, f"c_s used = X22 c_s,need {CS['canonical']:.3f} / {CS['alt']:.3f} km/s (distinct values used: {len(csused['canonical'])} / {len(csused['alt'])}); "
      f"X22 p-scan read: " + "; ".join(f"{f} " + ", ".join(f"p {p}: {v[0]} R_s8 {v[1]:.4f}" for p, v in fr22[f].items()) for f in FEET), "exact")
STOP = not (CHECKS["K0"] and CHECKS["K1"] and CHECKS["K2"])
RES["step0"] = dict(K0_max_dev=max(dev), cs_need=CS, x22_pscan=fr22)
# ============================================================== STEP 1: graded KT test
say("\n=== STEP 1: KT-keyed cluster test (A_pred = sum d_LHC / sum d_C*; Z = (A_meas - A_pred)/s_meas) ===")
GR = {}
for f, hk in CELLS:
    c = CELLK[(f, hk)]; cl = f"{f}|{hk}"; ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]; tv = X21J["tests"]["V1"]["cells"][cl]
    Ap = [float(c["dL"][TID == t].sum()/c["d"][TID == t].sum()) for t in range(3)]
    As = [float(c["dS"][TID == t].sum()/c["d"][TID == t].sum()) for t in range(3)]
    Zt = [(am - ap)/s for am, ap, s in zip(ref["A"], Ap, ref["s"])]
    bp = float(wls1(c["dL"], c["d"], X1)[1]); bs = float(wls1(c["dS"], c["d"], X1)[1]); Zs = (tv["b"] - bp)/tv["s_b"]
    Apa = float(c["dL"].sum()/c["d"].sum()); F = (Apa - 1)/(tv["A_sub"] - 1)
    sg = [np.sign(am - ap) for am, ap in zip(ref["A"], Ap)]
    if all(abs(z) <= 2 for z in Zt) and abs(Zs) <= 2: cls = "PASS"
    elif any(abs(z) > 2 for z in Zt) and len(set(sg)) == 1: cls = "WRONG AMPLITUDE"
    elif abs(Zs) > 2: cls = "WRONG KT DEPENDENCE"
    else: cls = "UNDECIDED"
    L = DIAG[(f, hk)]["L"]; S = DIAG[(f, hk)]["S"]
    med = lambda k, lst: float(np.median([e[k] for e in lst]))
    GR[cl] = dict(A_meas=ref["A"], s_meas=ref["s"], A_pred=Ap, Z_t=Zt, b_meas=tv["b"], s_b=tv["s_b"], b_pred=bp, Z_slope=Zs,
                  A_pred_all=Apa, A_meas_all=tv["A_sub"], F=F, cls=cls, A_pred_sigKT=As, b_pred_sigKT=bs,
                  diag=dict(f_in_0p15=med("f015", L), f_in_0p5=med("f05", L), Mfair_over_Mg500=med("Mfair_Mg500", L), rta_Mpc=med("rta", L),
                            log10_uncapped_over_fair=med("log10_uncapped_over_fair", L), self_grav_ratio_R500=med("self_ratio_R500", L),
                            sigKT_kms_median=float(np.nanmedian(SIG_KT[I])), sigKT_f_in_0p5=med("f05", S)))
    q = GR[cl]
    say(f"  {cl}: A_meas {' / '.join(f'{a:.2f}+-{s:.2f}' for a, s in zip(q['A_meas'], q['s_meas']))} | A_pred(LHC) {' / '.join(f'{a:.2f}' for a in Ap)}"
        f" | Z_t {' / '.join(f'{z:+.1f}' for z in Zt)} | slope b_meas {tv['b']:+.2f}+-{tv['s_b']:.2f} vs b_pred {bp:+.2f} (Z {Zs:+.2f})"
        f" | all-KT A_pred {Apa:.2f} vs {tv['A_sub']:.3f}: F = {F:.1f} -> {cls}")
    d_ = q["diag"]
    say(f"     diag: M_fair/Mg500 {d_['Mfair_over_Mg500']:.1f}; share inside 0.15 / 0.5 Mpc {d_['f_in_0p15']:.3f} / {d_['f_in_0p5']:.3f}; r_ta {d_['rta_Mpc']:.2f} Mpc;"
        f" log10(uncapped cosmic-mean mass / fair share) {d_['log10_uncapped_over_fair']:.1f}; cold/baryon g at R500 {d_['self_grav_ratio_R500']:.1f}")
    say(f"     bracket c_s = sigma_KT (median {d_['sigKT_kms_median']:.0f} km/s): A_pred {' / '.join(f'{a:.2f}' for a in As)}, b_pred {bs:+.2f}; share inside 0.5 Mpc {d_['sigKT_f_in_0p5']:.3f}")
cl_set = {GR[c]["cls"] for c in GR}
if STOP: V = "UNDECIDED (step 0 failed)"
else:
    pg = {f: PEERJ["footings"][f]["classes"] for f in FEET}
    gal_fail = any(pg[f]["Groups"]["grade"] not in ("REPRODUCED",) for f in FEET) if all("grade" in pg[f]["Groups"] for f in FEET) else False
    if gal_fail: V = "FAILS GALAXIES OR GROUPS"
    elif cl_set == {"PASS"}: V = "LHC PASSES THE CLUSTER TEST WITH c_s FIXED BY GALAXIES"
    elif cl_set == {"WRONG AMPLITUDE"}: V = "WRONG AMPLITUDE (factor F = " + " / ".join(f"{GR[c]['F']:.1f}" for c in GR) + ", cells can h0672 / can h0686 / alt h0672 / alt h0686)"
    elif cl_set == {"WRONG KT DEPENDENCE"}: V = "WRONG KT DEPENDENCE"
    else: V = "UNDECIDED (cells disagree: " + ", ".join(f"{c} {GR[c]['cls']}" for c in GR) + ")"
RES["step1"] = GR; RES["verdict"] = V
# ============================================================== AMENDMENT A1: one c_s >= c_s,need against >= 5 constraints
say("\n=== AMENDMENT A1: overdetermination scan, c_s = c_s,need x " + ", ".join(str(v) for v in FAC) + " ===")
X19R = json.load(open(os.path.join(REB, "X19_selector_rank_test", "x19_selector_rank_test_results.json")))
G946b, KPC946 = 6.67430e-11, 3.0856775814913673e19; PC946 = KPC946/1e3; BCAP = 2.9
def r_ta_x22(Mb_kg): return (3*(OM946/OB946)*Mb_kg/(4*math.pi*DTA*RHOM946))**(1/3)
def hydro_frac_enclosed(beta, xx): return (1.0/DTA)*3.0/(3.0 - beta)*np.power(np.minimum(xx, 1.0), 3.0 - beta)    # X22 verbatim (m7 off)
def law_g(gN, a0): gN = np.asarray(gN, float); return 0.5*(gN + np.sqrt(gN*gN + 4.0*gN*a0))
def e_pred(Mb_tot_msun, r_m, gN, sigma_kms, a0, cs_kms):                                              # peer lane X23_late_heating_graded, verbatim
    beta_raw = 2.0*sigma_kms**2/cs_kms**2; beta = min(beta_raw, BCAP); Mb = Mb_tot_msun*MSUN946
    Mc = 5.364*Mb*float(hydro_frac_enclosed(beta, r_m/r_ta_x22(Mb))); gc = G946b*Mc/r_m**2
    return float(np.log10(law_g(gN + gc, a0)/law_g(gN, a0)))
A1 = {}
for f in FEET:
    a0 = A0[f]; iv = X19R["intervals"][f"{f}|p16_84"]["Groups"]; et = X19R["E_table"][f"{f}|iso"]["Groups"]
    Mb, sg, rho, xg = iv["M_b"][2], iv["sigma"][2], iv["rho_b"][2], iv["x"][2]; gN = xg*a0
    rgrp = 3*gN/(4*math.pi*G946b*rho*MSUN946/PC946**3)
    cons = {k: [] for k in ("C-SPARC", "C-GRP", "C-T1", "C-T2", "C-T3", "C-KT3", "C-KTb")}; rows = []
    for k, fa in enumerate(FAC):
        cs = CS[f]*fa; ok = {"C-SPARC": fa >= 1.0}
        Eg = e_pred(Mb, rgrp, gN, sg, a0, cs); ok["C-GRP"] = abs(et["E"] - Eg) < 2*et["s"]
        row = dict(cs=cs, E_groups=Eg)
        okc = {kk: True for kk in ("C-T1", "C-T2", "C-T3", "C-KT3", "C-KTb")}
        for hk in HK:
            cc = CELL[(f, hk)]; r7 = X7J["bins"][f"terciles|{f}|{hk}"]; cl = f"{f}|{hk}"
            Ap7 = [float(cc["SC"][k][T3M == t].sum()/cc["d"][T3M == t].sum()) for t in range(3)]
            for t in range(3):
                okc[f"C-T{t+1}"] &= abs(r7[t]["MID"]["A_CAL"] - Ap7[t]) <= 2*r7[t]["MID"]["s_CAL"]
            ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]; tv = X21J["tests"]["V1"]["cells"][cl]
            dk = cc["SC"][k][I]; dc = cc["d"][I]
            ApK = [float(dk[TID == t].sum()/dc[TID == t].sum()) for t in range(3)]
            okc["C-KT3"] &= all(abs(am - ap) <= 2*s for am, ap, s in zip(ref["A"], ApK, ref["s"]))
            bp = float(wls1(dk, dc, X1)[1]); okc["C-KTb"] &= abs(tv["b"] - bp) <= 2*tv["s_b"]
            row[hk] = dict(A_pred_MGAS_terciles=Ap7, A_meas_MGAS=[r["MID"]["A_CAL"] for r in r7], s_meas_MGAS=[r["MID"]["s_CAL"] for r in r7],
                           A_pred_KT_terciles=ApK, b_pred=bp, b_meas=tv["b"], s_b=tv["s_b"])
        ok.update(okc); row["ok"] = ok; rows.append(row)
        for kk, v in ok.items():
            if v: cons[kk].append(round(cs, 1))
        h0 = row["h0672"]
        say(f"  {f} c_s {cs:7.1f} (x{fa}): groups E_pred {Eg:+.4f} (obs {et['E']:+.3f}+-{et['s']:.3f}); MGAS terciles A_pred(h0.672) "
            + " / ".join(f"{a:.2f}" for a in h0["A_pred_MGAS_terciles"]) + " (meas " + " / ".join(f"{a:.2f}+-{s:.2f}" for a, s in zip(h0["A_meas_MGAS"], h0["s_meas_MGAS"]))
            + "); KT terciles " + " / ".join(f"{a:.2f}" for a in h0["A_pred_KT_terciles"]) + f"; KT slope {h0['b_pred']:+.2f} (meas {h0['b_meas']:+.2f}+-{h0['s_b']:.2f}) | "
            + " ".join(f"{kk}{'+' if v else '-'}" for kk, v in ok.items()))
    inter = sorted(set.intersection(*[set(v) for v in cons.values()]))
    A1[f] = dict(rows=rows, allowed=cons, intersection=inter, line=("INTERSECTION EMPTY" if not inter else "INTERSECTION NON-EMPTY " + str(inter)))
    say(f"  {f} allowed c_s (km/s) per constraint: " + "; ".join(f"{kk} {v if v else 'none'}" for kk, v in cons.items()))
    say(f"  {f} A1: {A1[f]['line']}")
RES["amendment_A1"] = A1
# ============================================================== reported only
say("\n=== REPORTED ONLY ===")
pc = {f: PEERJ["footings"][f]["classes"] for f in FEET}
for f in FEET:
    rows = {k: pc[f][k] for k in ("SPARC small", "SPARC large", "Groups", "MW disc", "MW ultra-faint", "bright M31", "M31 others")}
    say(f"  peer lane X23_late_heating_graded ({f}, reproduced identical before freezing): " +
        "; ".join(f"{k} E_pred {v.get('E_pred', float('nan')):+.4f} vs E_obs {v.get('E_obs', float('nan')):+.3f}+-{v.get('s', float('nan')):.3f} {v.get('grade', '')}" for k, v in rows.items()))
RES["peer_rows"] = {f: {k: pc[f][k] for k in ("SPARC small", "SPARC large", "Groups", "MW disc", "MW ultra-faint", "bright M31", "M31 others")} for f in FEET}
# forest / sigma8 / CMB from X22's committed p-scan
CMB = {}
for f in FEET:
    for p in (3.0, 4.0, 5.0):
        a = 1/1101; cs = CS[f]*a**(p - 0.5); Hz = H0_946*math.sqrt(OM946*1101**3)                      # matter-only H at z=1100 (radiation ignored: lower bound on H)
        kJ = a*Hz/(cs*1e3)*MPC946/0.674                                                                   # comoving h/Mpc
        CMB[f"{f}|p{p}"] = dict(cs_z1100_kms=cs, kJ_hMpc=kJ)
    say(f"  {f}: X22 forest/R_sigma8 p 3: {fr22[f]['3.0'][0]} {fr22[f]['3.0'][1]:.4f}; p 4: {fr22[f]['4.0'][0]} {fr22[f]['4.0'][1]:.4f}; p 6: {fr22[f]['6.0'][0]} {fr22[f]['6.0'][1]:.4f}"
        f" (p 5 bracketed by 4 and 6); CMB c_s(z=1100) p 3/4/5 = " + " / ".join(f"{CMB[f'{f}|p{p}']['cs_z1100_kms']:.2e}" for p in (3.0, 4.0, 5.0)) +
        " km/s, k_J = " + " / ".join(f"{CMB[f'{f}|p{p}']['kJ_hMpc']:.1e}" for p in (3.0, 4.0, 5.0)) + " h/Mpc")
RES["cmb"] = CMB
# energy budget
OL = 1 - OM946; EB = {}
for f in FEET:
    c2 = (CS[f]*1e3)**2; frac_L = 1.5*OC946/OL*c2/(2.99792458e8)**2
    per_baryon_keV = 5.364*1.5*c2*MP/KEV
    sn_keV = 0.07*1e44/(100*MSUN946)*MP/KEV                                                             # PROVISIONAL: Omega_*/Omega_b 0.07, 1e51 erg per 100 Msun formed
    agn_keV = 0.05*0.1*(2.99792458e8)**2*7e-5*MP/KEV                                                  # PROVISIONAL: rho_BH/rho_b 7e-5, eps_rad 0.1, coupling 0.05
    EB[f] = dict(frac_rhoLambda=frac_L, per_baryon_keV=per_baryon_keV, SN_keV_PROVISIONAL=sn_keV, AGN_coupled_keV_PROVISIONAL=agn_keV)
    say(f"  {f}: heating energy (3/2) rho_c c_s^2 = {frac_L:.2e} rho_Lambda c^2; per baryon {per_baryon_keV:.2f} keV vs SN {sn_keV:.2f} keV, coupled AGN {agn_keV:.2f} keV (PROVISIONAL, from memory)"
        f" -> x{per_baryon_keV/sn_keV:.0f} SN, x{per_baryon_keV/agn_keV:.0f} coupled AGN")
RES["energy"] = EB
say("  action status: no action (X6: no free dust coupling; X19 step 2: no action-level selector; CFG944 Theorem G: local theta-clock tethers carry a ghost "
    "or cannot be off in the linear universe; CFG741: P-wave heating Q <= 0.50, scale-free; CFG643: baryon->cold heat exchange CLOSED)")
vcoll = 4500.0
say(f"  Bullet (qualitative): a single perfect fluid with c_s {CS['canonical']:.0f} km/s meets a ~{vcoll:.0f} km/s collision at Mach ~{vcoll/CS['canonical']:.0f}; it shocks and is "
    "held with the X-ray gas, so the lensing centroid would follow the gas (opposite to the observed galaxy-following offset) unless the field is collisionless")
RES["bullet_mach"] = vcoll/CS["canonical"]
# ============================================================== verdict, checks, MUTATE
check("K3", rss() < 1.0, f"peak RSS {rss():.3f} GB", "< 1 GB")
say(f"\nVERDICT: {V}")
say("  cluster cell classes: " + "; ".join(f"{c} {GR[c]['cls']}" for c in GR))
if MUT:
    must = ("K0", "K1", "K2"); RES["mutate_required_fail"] = {k: not CHECKS[k] for k in must}
    say("MUTATE: required failures " + ", ".join(f"{k} {'FAILED' if not CHECKS[k] else 'passed (BAD)'}" for k in must))
RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss()
say(f"checks {sum(CHECKS.values())}/{len(CHECKS)} PASS; runtime {RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_GB']:.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"x23_late_heated_cold_results{TAG}.json"), "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
sys.exit(0 if (all(CHECKS.values()) and not MUT) else 1)

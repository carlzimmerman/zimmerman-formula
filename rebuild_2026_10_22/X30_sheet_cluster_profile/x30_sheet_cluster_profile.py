"""X30_sheet_cluster_profile (criteria c6be83f91c): does the hydrostatic partial-retention profile at X26's scenario-B sheet points
reproduce the measured INNER / MID / OUTER shear bands and their KT / MGAS500 tercile trends, or does the profile shape exclude the sheet?
Machinery: X23_late_heated_cold / X26_cold_sector_map verbatim (X2's functions exec'd read-only, X7's per-cluster npz, C* potential, isothermal
hydrostatic cold fluid normalised to min(cosmic mean at r_ta, fair share), sourcing AQUAL and lensing); the per-bin model vector is kept and
summed per band. Sheet points read from X26's committed pass masks; nothing fitted.
Usage: PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x30_sheet_cluster_profile.py    (X30_MUTATE=1: MUTATE twin, exit 1)
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
MUT = os.environ.get("X30_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"x30_sheet_cluster_profile{TAG}.out"), "w")
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUTF.write(s + "\n"); OUTF.flush()
RES = {"lane": "X30_sheet_cluster_profile", "criteria": "c6be83f91c", "mutate": MUT}; CHECKS = {}
def check(name, ok, val, thr):
    CHECKS[name] = bool(ok); say(f"{name} {'PASS' if ok else 'FAIL'}: {val}   (line: {thr})")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform == "darwin" else 1e6)
say("X30_sheet_cluster_profile" + (" [MUTATE m1 INNER<->OUTER bins swapped on the measurement side, m2 hydrostatic sign flipped: control output, not physics]" if MUT else "") +
    ": criteria c6be83f91c; kappa = 1/2 FITTED; footings never pooled; field mass, no particle; not theory closed")
FEET, HK = ("canonical", "alt"), ("h0672", "h0686"); CELLS = [(f, h) for f in FEET for h in HK]
SIG_STAR, RHO_STAR = 100.0, 1e-3
def J(rel): return json.load(open(os.path.join(REB, rel)))
X21J = J("X21_cluster_switch_anatomy/x21_switch_anatomy_results.json"); X23J = J("X23_late_heated_cold/x23_late_heated_cold_results.json")
X26J = J("X26_cold_sector_map/x26_cold_sector_map_results.json"); X7J = J("X7_cluster_core_significance/x7_analysis_results.json")
X2J = J("X2_cluster_outskirts/x2_cluster_outskirts_results.json"); X22J = J("X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")
for nm, p in (("X21", "X21_cluster_switch_anatomy/x21_switch_anatomy_results.json"), ("X23", "X23_late_heated_cold/x23_late_heated_cold_results.json"),
              ("X26", "X26_cold_sector_map/x26_cold_sector_map_results.json"), ("X26_npz", "X26_cold_sector_map/x26_pass_masks.npz"),
              ("X7", "X7_cluster_core_significance/x7_analysis_results.json"), ("X2", "X2_cluster_outskirts/x2_cluster_outskirts_results.json"),
              ("X22", "X22_cosmic_dust_window/x22_cosmic_dust_window_results.json")):
    RES[f"{nm}_sha256"] = sha(os.path.join(REB, p))
# ============================================================== sheet points (frozen section 1): X26 GRADED_B masks, collapsed over p
GRADED_B = ["FP1", "FP2", "C-forest", "C-s8", "C-CMB", "C-SPARC", "C-groups", "C-T1", "C-T2", "C-T3", "C-KTb", "C-dwarfs-c0", "C-MW"]
PM_ = np.load(os.path.join(REB, "X26_cold_sector_map", "x26_pass_masks.npz"))
SHEET = {}
for f in FEET:
    m = np.ones(PM_[f"{f}|FP1"].shape, bool)
    for c in GRADED_B: m &= PM_[f"{f}|{c}"]
    pts = sorted({(float(PM_["LCS"][a]), float(PM_["R"][b]), float(PM_["Q"][c])) for a, b, c, _ in zip(*np.where(m))})
    js = sorted((e["log10_cstar"], e["r"], e["q"]) for e in X26J["A2_direct"][f] if e["allowed"])
    assert pts == js, f"sheet list differs from X26 A2 ({f})"
    SHEET[f] = pts
SURV = {"canonical": (3.125, 0.0, 0.375), "alt": (3.25, 0.0, 0.5)}
assert all(SURV[f] in SHEET[f] for f in FEET)
say(f"sheet points (X26 scenario B, from the committed npz = X26 A2 list): canonical {len(SHEET['canonical'])}, alt {len(SHEET['alt'])}; "
    f"MGAS500 survivors (flagged) canonical c_* 10^3.125 q +0.375, alt c_* 10^3.25 q +0.5")
RES["sheet"] = SHEET
# ============================================================== X2's functions exec'd read-only (exactly as X23 / X26 do)
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
NS2["DAT"] = DAT; CL = NS2["CL"]; redfac = NS2["redfac"]; PATCH = NS2["PATCH"]
assert [c["name"] for c in CL] == [str(x) for x in MY["name"]]
BANDS = {b: list(v) for b, v in NS2["BANDS"].items()}                                    # model side (INNER 0-2, MID 3-5, OUTER 6-7)
BMEAS = dict(BANDS)
if MUT: BMEAS = {"INNER": BANDS["OUTER"], "MID": BANDS["MID"], "OUTER": BANDS["INNER"]}   # m1
BN = ("INNER", "MID", "OUTER")
EF = os.path.join(REPO, "real_research", "data", "erass1cl_primary_v3.2.fits"); RES["erass1_sha256"] = sha(EF)
E_ = fits.open(EF)[1].data; idx_ = {str(s_).strip(): k for k, s_ in enumerate(E_["NAME"])}
KT = np.asarray(E_["KT"], float)[np.array([idx_[str(x).strip()] for x in MY["name"]])]
I = np.where(np.isfinite(KT) & (KT > 0))[0]; nI = len(I); xkt = np.log10(KT[I]/np.median(KT[I])); TID = np.digitize(xkt, np.quantile(xkt, [1/3, 2/3]))
MP, KEV = 1.67262192e-27, 1.602176634e-16
SIG_KT = np.sqrt(KT[I]*KEV/(0.6*MP))/1e3
Mgl = np.asarray(MY["Mgas500"], float); T3M = np.digitize(Mgl, np.quantile(Mgl, [1/3, 2/3])); ALLI = np.arange(N)
say(f"KT clusters {nI} (tercile edges {np.quantile(KT[I], [1/3, 2/3]).round(3).tolist()} keV); all clusters {N} (MGAS500 tercile edges {np.quantile(Mgl, [1/3, 2/3]).tolist()})")
# ============================================================== model (X26's prep / gfun / cold_mass / dmid, per-bin vector kept)
G946, MSUN946, MPC946 = 6.67430e-11, 1.98847e30, 3.0856775814913673e22
H0_946 = 67.4e3/MPC946; RHOC_946 = 3*H0_946**2/(8*math.pi*G946); OB946 = 0.0493; OC946 = 5.364*OB946; OM946 = OB946 + OC946
RHOM946 = OM946*RHOC_946; DTA = 5.55
def r_ta_com(Mb_kg): return (3*(OM946/OB946)*Mb_kg/(4*math.pi*DTA*RHOM946))**(1/3)
def lnrho_profile(g, r_m, rta_m, cs_ms):
    """ln(rho/rho(r_ta)) = int_r^{r_ta} g dr'/c_s^2 (derived: c_s^2 dln rho/dr = -g); m2 flips the sign."""
    Ic = np.r_[0, np.cumsum(0.5*(g[1:] + g[:-1])*np.diff(r_m))]; out = (np.interp(rta_m, r_m, Ic) - Ic)/cs_ms**2
    return -out if MUT else out
def cold_mass(g, r_m, rta_m, cs_ms, Mfair, ln_rhobar):
    """X26 verbatim (normalisation min(cosmic mean at r_ta, fair share)); also returns lr and the retained total."""
    lr = lnrho_profile(g, r_m, rta_m, cs_ms); inside = r_m <= rta_m
    lmax = float(lr[inside].max()); w = np.where(inside, np.exp(lr - lmax), 0.0)
    dm = 4*np.pi*r_m**2*w; Mw = np.r_[0, np.cumsum(0.5*(dm[1:] + dm[:-1])*np.diff(r_m))]
    Mrta = float(np.interp(rta_m, r_m, Mw)); shape = np.minimum(Mw/Mrta, 1.0)
    ln_cos = ln_rhobar + lmax + math.log(Mrta); Mtot = Mfair if ln_cos >= math.log(Mfair) else math.exp(ln_cos)
    return shape*Mtot, lr, Mtot
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
               dmpc=np.radians(cl["off_deg"])*float(DM(cl["z"], h))/(1 + cl["z"]), R500=R500)
    PREP[key] = out; return out
def dvec(i, foot, hk, Mc):
    """X26's dmid with the per-bin vector W P f_red kept (8 bins)."""
    pp = prep(i, foot, hk); Msrc = pp["Mb"] if Mc is None else pp["Mb"] + Mc
    g = gfun(Msrc, foot); ML = g*RM**2/G; rho = np.gradient(ML, RM)/(4*np.pi*RM**2)
    So = offset_floor(project_floor(rho), pp["dmpc"]); Pp = at_bins(dsig_from_sig(So))/KG_PC2
    fr, _ = redfac(hk, i, sig_bins(So)); return DAT[hk]["W"][i]*(Pp*fr)
def bsum(v, bands=BANDS): return np.array([v[..., bands[b]].sum(-1) for b in BN]).T            # (..., 3)
def d_cold(i, foot, hk, cs_kms, prof=False):
    pp = prep(i, foot, hk); Mc, lr, Mtot = cold_mass(pp["gb"], RM, pp["rta"], cs_kms*1e3, pp["Mfair"], pp["ln_rhobar"])
    v = dvec(i, foot, hk, Mc)
    if not prof: return v, None
    rta = pp["rta"]/MPC; k = np.where((lr < lr[0] - math.log(2)) & (RG <= rta))[0]
    rcold = float(RG[k[0]]) if len(k) else float("nan")                                          # nan: never halves inside r_ta
    ex = dict(rc_cold=rcold, rc_gas=0.15*pp["R500"], f015=float(np.interp(0.15, RG, Mc)/Mtot), f05=float(np.interp(0.5, RG, Mc)/Mtot),
              ret=float(Mtot/pp["Mfair"]), McMb_R500=float(np.interp(pp["R500"], RG, Mc)/np.interp(pp["R500"], RG, pp["Mb"])))
    return v, ex
def cs_point(lc, r, q, sig, rho): return 10**(lc + r*np.log10(sig/SIG_STAR) + 0.5*q*np.log10(rho/RHO_STAR))
# ============================================================== X21 statistics machinery (verbatim)
RB = 20261024; NB = 2000
def bidx(nsel, key): return np.random.default_rng([RB, key]).integers(0, nsel, size=(NB, nsel))
def counts(ix, nsel): return np.stack([np.bincount(r, minlength=nsel) for r in ix]).astype(float)
def jkreps(Ix):
    p = PATCH[Ix]; return np.array([(p != q).astype(float) for q in range(30) if np.any(p == q)])
def ratio_w(Wt, n, d): return (Wt @ n)/(Wt @ d)
def sstat(fun, Ix, key):
    C = counts(bidx(len(Ix), key), len(Ix)); sb = np.std(fun(C), axis=0, ddof=1); Jr = jkreps(Ix); vj = fun(Jr)
    sj = np.sqrt((len(Jr) - 1)/len(Jr)*np.sum((vj - vj.mean(0))**2, axis=0)); return np.maximum(sb, sj), sb, sj
def wls(Wt, X, n, d):
    F = np.einsum("ri,i,ij,ik->rjk", Wt, d, X, X); g = np.einsum("ri,ij,i->rj", Wt, X, n); return np.linalg.solve(F, g[..., None])[..., 0]
def wls1(n, d, X): return wls(np.ones((1, len(n))), X, n, d)[0]
X1m = np.c_[np.ones(nI), xkt]
# ============================================================== measurement side per cell (n with leakP, nraw, cross, R-R; d = C*), bands BMEAS
MEAS = {}; DC = {}
t1 = time.time()
for f, hk in CELLS:
    dd = DAT[hk]; WB = dd["W"]*dd["B"][None, :]; hx = HXI[hk]
    vC = np.array([dvec(i, f, hk, None) for i in ALLI]); PREP.clear()
    DC[(f, hk)] = vC
    MEAS[(f, hk)] = dict(n=bsum(WB*(dd["D"] - MY["leakP"][:, hx, 0]), BMEAS), nraw=bsum(WB*dd["D"], BMEAS), nx=bsum(WB*dd["Dx"], BMEAS),
                         nrr=bsum(WB*dd["DRR"], BMEAS), d=bsum(vC, BMEAS), rho=np.array([float(np.interp(0.548, RG, prep(i, f, hk)["Mb"]))/MSUN for i in ALLI])/(4/3*math.pi*(0.548e6)**3))
    PREP.clear()
say(f"C* model vectors and measured band sums built for 4 cells [{time.time()-t1:.0f} s, RSS {rss():.2f} GB]")
def meas_stats(c, Ix, b, key):
    """A (n with leakP), sigma_STAT on nraw (X21), A_x, A_RR, sigma_IN = sqrt(sigma_STAT^2 + A_x^2 + A_RR^2) (X2 (e))."""
    bi = BN.index(b); n, nr, d = c["n"][Ix, bi], c["nraw"][Ix, bi], c["d"][Ix, bi]
    A = float(n.sum()/d.sum()); s, _, _ = sstat(lambda Wt: ratio_w(Wt, nr, d), Ix, key)
    ax = float(c["nx"][Ix, bi].sum()/d.sum()); arr = float(c["nrr"][Ix, bi].sum()/d.sum())
    return dict(A=A, s=float(s), A_x=ax, A_RR=arr, s_IN=float(math.sqrt(float(s)**2 + ax**2 + arr**2)))
M = {}
for f, hk in CELLS:
    c = MEAS[(f, hk)]; cl = f"{f}|{hk}"; o = {}
    for b in BN:
        o[f"KT_all|{b}"] = meas_stats(c, I, b, 0)
        o[f"KT_terc|{b}"] = [meas_stats(c, I[TID == t], b, 20100 + t) for t in range(3)]
        n, d = c["n"][I, BN.index(b)], c["d"][I, BN.index(b)]
        bb = float(wls1(n, d, X1m)[1]); sb_, _, _ = sstat(lambda Wt: wls(Wt, X1m, n, d)[:, 1], I, 5010)
        o[f"KT_b|{b}"] = dict(b=bb, s_b=float(sb_))
        o[f"M_all|{b}"] = meas_stats(c, ALLI, b, 0)
        o[f"M_terc|{b}"] = [meas_stats(c, np.where(T3M == t)[0], b, 200 + t) for t in range(3)]
    M[cl] = o
# ============================================================== STEP 0
say("\n=== STEP 0 ===")
devb, devc, devc2 = [], [], []
for f, hk in CELLS:
    cl = f"{f}|{hk}"; ref = X21J["binned"]["V1"]["terciles"]["cells"][cl]; tv = X21J["tests"]["V1"]["cells"][cl]; o = M[cl]
    devb += [abs(a["A"] - r_) for a, r_ in zip(o["KT_terc|MID"], ref["A"])] + [abs(a["s"] - r_) for a, r_ in zip(o["KT_terc|MID"], ref["s"])]
    devb += [abs(o["KT_b|MID"]["b"] - tv["b"]), abs(o["KT_b|MID"]["s_b"] - tv["s_b"])]
    say(f"  {cl}: KT MID terciles A " + " / ".join(f"{a['A']:.4f}+-{a['s']:.4f}" for a in o["KT_terc|MID"]) + " (X21 " + " / ".join(f"{a:.4f}+-{s:.4f}" for a, s in zip(ref["A"], ref["s"]))
        + f"); slope b {o['KT_b|MID']['b']:+.4f}+-{o['KT_b|MID']['s_b']:.4f} (X21 {tv['b']:+.4f}+-{tv['s_b']:.4f})")
    r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]
    for b in ("MID", "OUTER"):
        devc += [abs(a["A"] - r_[b]["A_CAL"]) for a, r_ in zip(o[f"M_terc|{b}"], r7)] + [abs(a["s"] - r_[b]["s_STAT"]) for a, r_ in zip(o[f"M_terc|{b}"], r7)]
    devc += [abs(o["M_all|OUTER"]["A"] - a7["OUTER"]["A_CAL"]), abs(o["M_all|OUTER"]["s"] - a7["OUTER"]["s_STAT"])]
    say(f"  {cl}: X7 MGAS500 terciles OUTER A_CAL " + " / ".join(f"{a['A']:.4f}+-{a['s']:.4f}" for a in o["M_terc|OUTER"]) + " (X7 " + " / ".join(f"{r_['OUTER']['A_CAL']:.4f}+-{r_['OUTER']['s_STAT']:.4f}" for r_ in r7)
        + f"); all OUTER {o['M_all|OUTER']['A']:.4f} (X7 {a7['OUTER']['A_CAL']:.4f})")
# X2 C* INNER via X2's own stats (raw D, jackknife, (e))
for f, hk in CELLS:
    cl = f"{f}|{hk}"; P = NS2["stack_model"](f, hk, gasshape="P", efe="noclu", red=True)[0]; NS2["PRED"].clear()
    st = NS2["stats"](hk, P, "boost", NS2["ALL"], True)["INNER"]; ref = X2J["rows"]["C* corrected baseline"]["boost"][cl]["INNER"]
    devc2 += [abs(st["A"] - ref["A"]), abs(st["s_jk"] - ref["s_jk"]), abs(st["s_tot"] - ref["s_tot"])]
    dP = float(np.max(np.abs(DAT[hk]["W"]*P - DC[(f, hk)])/np.maximum(np.abs(DC[(f, hk)]).max(), 1e-300)))
    say(f"  {cl}: X2 C* INNER A {st['A']:.4f} s_jk {st['s_jk']:.4f} s_tot {st['s_tot']:.4f} (X2 {ref['A']:.4f} / {ref['s_jk']:.4f} / {ref['s_tot']:.4f}); "
        f"this lane's C* vector vs X2 stack_model W P: max rel {dP:.1e}; measured-side INNER (this lane, n with leakP) {M[cl]['M_all|INNER']['A']:.4f}"
        f" +- s_STAT {M[cl]['M_all|INNER']['s']:.4f} / s_IN {M[cl]['M_all|INNER']['s_IN']:.4f}")
    devc2.append(dP)
devc_all = devc + devc2
# K0a: X26 A2 direct A_pred / b_pred at every allowed point; K0d: X23 A1 KT terciles at c_s,need x 3, x 4
CS22 = {f: float(X22J["step2"]["per_footing"][f]["cs_need_kms"]) for f in FEET}
PRED = {}; PROF = {}
t1 = time.time()
for f in FEET:
    for (lc, r, q) in SHEET[f]:
        sel = ALLI if abs(r) < 1e-12 else I
        for hk in HK:
            c = MEAS[(f, hk)]; csv_ = np.full(N, np.nan)
            if abs(r) < 1e-12: csv_ = cs_point(lc, 0.0, q, 1.0, c["rho"])
            else: csv_[I] = cs_point(lc, r, q, SIG_KT, c["rho"][I])
            V = np.zeros((N, 8)); EX = {}
            for i in sel:
                V[i], ex = d_cold(i, f, hk, float(csv_[i]), prof=True); EX[int(i)] = ex
            PREP.clear(); PRED[(f, lc, r, q, hk)] = dict(v=V, cs=csv_, sel=sel); PROF[(f, lc, r, q, hk)] = EX
    say(f"  {f}: sheet predictions built ({len(SHEET[f])} points x 2 h cells) [{time.time()-t1:.0f} s, RSS {rss():.2f} GB]")
deva = []
for f in FEET:
    for e in X26J["A2_direct"][f]:
        if not e["allowed"]: continue
        for hk in HK:
            p = PRED[(f, e["log10_cstar"], e["r"], e["q"], hk)]; dL = bsum(p["v"])[I, 1]; dC = bsum(DC[(f, hk)])[I, 1]
            Ap = [float(dL[TID == t].sum()/dC[TID == t].sum()) for t in range(3)]; bp = float(wls1(dL, dC, X1m)[1])
            deva += [abs(a - b_) for a, b_ in zip(Ap, e["detail"][hk]["A_pred"])] + [abs(bp - e["detail"][hk]["b_pred"])]
devd = []
FAC = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 13, 16]
for f, hk in CELLS:
    for k in (FAC.index(3), FAC.index(4)):
        dL = np.array([d_cold(i, f, hk, CS22[f]*FAC[k])[0] for i in I]); PREP.clear(); dL = bsum(dL)[:, 1]; dC = bsum(DC[(f, hk)])[I, 1]
        Ap = [float(dL[TID == t].sum()/dC[TID == t].sum()) for t in range(3)]
        devd += [abs(a - b_) for a, b_ in zip(Ap, X23J["amendment_A1"][f]["rows"][k][hk]["A_pred_KT_terciles"])]
check("K0a", max(deva) <= 1e-9, f"X26 A2 direct KT-tercile A_pred and b_pred at {sum(len(SHEET[f]) for f in FEET)} allowed points x 2 h cells, max |dev| {max(deva):.2e}", "<= 1e-9")
check("K0b", max(devb) <= 1e-9, f"X21 KT MID terciles A, s and slope b, s_b, max |dev| {max(devb):.2e} ({len(devb)} numbers)", "<= 1e-9")
check("K0c", max(devc_all) <= 1e-9, f"X7 MGAS500 tercile MID/OUTER A_CAL + s_STAT and all OUTER A_CAL + s_STAT max |dev| {max(devc):.2e}; X2 C* INNER A/s_jk/s_tot and C* vector max |dev| {max(devc2):.2e}", "<= 1e-9")
check("K0d", max(devd) <= 1e-9, f"X23 A1 KT-tercile A_pred at c_s,need x 3 and x 4, max |dev| {max(devd):.2e}", "<= 1e-9")
STOP = not all(CHECKS[k] for k in ("K0a", "K0b", "K0c", "K0d"))
RES["step0"] = dict(K0a=max(deva), K0b=max(devb), K0c=max(devc_all), K0d=max(devd))
# K1 band partition, K2 solver, K3 zero-cold limit
k1 = max(float(np.max(np.abs(bsum(DC[c]).sum(1) - DC[c].sum(1))/np.abs(DC[c].sum(1)).max())) for c in CELLS)
check("K1", k1 <= 1e-12, f"sum over the three bands = sum over 8 bins, max rel {k1:.1e}", "<= 1e-12")
Mpt_t = 1e14*MSUN; rta_t = 5*MPC; cs_t = 3e5
lr_t = lnrho_profile(G*Mpt_t/RM**2, RM, rta_t, cs_t); sel_ = (RG > 0.05) & (RG < 5)
cf = G*Mpt_t/cs_t**2*(1/RM - 1/rta_t); k2a = float(np.max(np.abs(lr_t[sel_] - cf[sel_])/np.abs(cf[sel_]).max()))
k2b = float(np.max(np.abs(lnrho_profile(G*Mpt_t/RM**2, RM, rta_t, 1e11)[sel_])))
check("K2", k2a <= 1e-4 and k2b <= 1e-6, f"point mass closed form {k2a:.2e}; c_s = 1e8 km/s uniform limit {k2b:.2e}", "<= 1e-4; <= 1e-6")
k3 = max(float(np.max(np.abs(dvec(i, f, hk, np.zeros_like(RG)) - DC[(f, hk)][i]))) for f, hk in CELLS for i in (0, 100, 200, 325)); PREP.clear()
check("K3", k3 == 0.0, f"zero cold mass reproduces the C* vector exactly (max |dev| {k3:.1e}, 16 cluster-cells)", "exact")
# ============================================================== STEP 1: grades
say("\n=== STEP 1: predicted vs measured bands at every sheet point (Z = (meas - pred)/sigma; graded |Z| <= 2 in both h cells) ===")
for f, hk in CELLS:
    o = M[f"{f}|{hk}"]
    say(f"  measured {f} {hk}: KT(106) INNER all {o['KT_all|INNER']['A']:.2f}+-{o['KT_all|INNER']['s_IN']:.2f} (STAT {o['KT_all|INNER']['s']:.2f}); "
        f"MID terciles " + " / ".join(f"{a['A']:.2f}+-{a['s']:.2f}" for a in o["KT_terc|MID"]) + f", b {o['KT_b|MID']['b']:+.2f}+-{o['KT_b|MID']['s_b']:.2f}; "
        f"OUTER all {o['KT_all|OUTER']['A']:.2f}+-{o['KT_all|OUTER']['s']:.2f}, terciles " + " / ".join(f"{a['A']:.2f}+-{a['s']:.2f}" for a in o["KT_terc|OUTER"])
        + f", b {o['KT_b|OUTER']['b']:+.2f}+-{o['KT_b|OUTER']['s_b']:.2f}; INNER terciles " + " / ".join(f"{a['A']:.2f}+-{a['s_IN']:.2f}" for a in o["KT_terc|INNER"]))
    r7 = X7J["bins"][f"terciles|{f}|{hk}"]; a7 = X7J["all"][f"C*|boost|{f}|{hk}"]
    say(f"           326 (MGAS500): INNER all {o['M_all|INNER']['A']:.2f}+-{o['M_all|INNER']['s_IN']:.2f}; OUTER all (X7 CAL) {a7['OUTER']['A_CAL']:.2f}+-{a7['OUTER']['s_CAL']:.2f}, "
        f"terciles " + " / ".join(f"{r_['OUTER']['A_CAL']:.2f}+-{r_['OUTER']['s_CAL']:.2f}" for r_ in r7) + "; MID terciles (X26 A3 line, reported) "
        + " / ".join(f"{r_['MID']['A_CAL']:.2f}+-{r_['MID']['s_CAL']:.2f}" for r_ in r7))
RES["measured"] = M
INNER_C = ("G-IN-all", "G-IN-Mall")
GRADE = {}
for f in FEET:
    GRADE[f] = []
    for (lc, r, q) in SHEET[f]:
        row = dict(log10_cstar=lc, r=r, q=q, survivor=(lc, r, q) == SURV[f], cells={}, ok={}, rep={})
        for hk in HK:
            cl = f"{f}|{hk}"; o = M[cl]; p = PRED[(f, lc, r, q, hk)]; vB = bsum(p["v"]); vC = bsum(DC[(f, hk)])
            g = {}; rp = {}
            def z(meas, s, pred): return (meas - pred)/s
            kt = vB[I]; ktC = vC[I]
            for bi, b in enumerate(BN):
                At = [float(kt[TID == t, bi].sum()/ktC[TID == t, bi].sum()) for t in range(3)]; Aa = float(kt[:, bi].sum()/ktC[:, bi].sum())
                bp = float(wls1(kt[:, bi], ktC[:, bi], X1m)[1])
                if b == "MID":
                    for t in range(3): g[f"G-MID-T{t+1}"] = (o["KT_terc|MID"][t]["A"], o["KT_terc|MID"][t]["s"], At[t])
                    g["G-MID-b"] = (o["KT_b|MID"]["b"], o["KT_b|MID"]["s_b"], bp); rp["KT MID all"] = (o["KT_all|MID"]["A"], o["KT_all|MID"]["s"], Aa)
                if b == "OUTER":
                    g["G-OUT-all"] = (o["KT_all|OUTER"]["A"], o["KT_all|OUTER"]["s"], Aa)
                    for t in range(3): g[f"G-OUT-T{t+1}"] = (o["KT_terc|OUTER"][t]["A"], o["KT_terc|OUTER"][t]["s"], At[t])
                    g["G-OUT-b"] = (o["KT_b|OUTER"]["b"], o["KT_b|OUTER"]["s_b"], bp)
                if b == "INNER":
                    g["G-IN-all"] = (o["KT_all|INNER"]["A"], o["KT_all|INNER"]["s_IN"], Aa)
                    for t in range(3): rp[f"KT INNER T{t+1}"] = (o["KT_terc|INNER"][t]["A"], o["KT_terc|INNER"][t]["s_IN"], At[t])
                    rp["KT INNER b"] = (o["KT_b|INNER"]["b"], o["KT_b|INNER"]["s_b"], bp)
            if abs(r) < 1e-12:
                r7 = X7J["bins"][f"terciles|{cl}"]; a7 = X7J["all"][f"C*|boost|{cl}"]
                Am = [[float(vB[T3M == t, bi].sum()/vC[T3M == t, bi].sum()) for t in range(3)] for bi in range(3)]
                Aall = [float(vB[:, bi].sum()/vC[:, bi].sum()) for bi in range(3)]
                g["G-OUT-Mall"] = (a7["OUTER"]["A_CAL"], a7["OUTER"]["s_CAL"], Aall[2])
                for t in range(3): g[f"G-OUT-M{t+1}"] = (r7[t]["OUTER"]["A_CAL"], r7[t]["OUTER"]["s_CAL"], Am[2][t])
                g["G-IN-Mall"] = (o["M_all|INNER"]["A"], o["M_all|INNER"]["s_IN"], Aall[0])
                for t in range(3):
                    rp[f"M MID T{t+1} (X26 A3 line)"] = (r7[t]["MID"]["A_CAL"], r7[t]["MID"]["s_CAL"], Am[1][t])
                    rp[f"M INNER T{t+1}"] = (o["M_terc|INNER"][t]["A"], o["M_terc|INNER"][t]["s_IN"], Am[0][t])
            row["cells"][hk] = {k: dict(meas=v[0], s=v[1], pred=v[2], Z=z(*v)) for k, v in g.items()}
            row["rep"][hk] = {k: dict(meas=v[0], s=v[1], pred=v[2], Z=z(*v)) for k, v in rp.items()}
        keys = list(row["cells"]["h0672"].keys())
        row["ok"] = {k: all(abs(row["cells"][hk][k]["Z"]) <= 2 for hk in HK) for k in keys}
        bad = [k for k, v in row["ok"].items() if not v]
        row["fails"] = bad
        row["status"] = "PASS" if not bad else ("INNER-ONLY" if all(k in INNER_C for k in bad) else "FAIL")
        ex = [PROF[(f, lc, r, q, "h0672")][int(i)] for i in I]
        prof = {}
        for t in range(3):
            et = [e for e, tt in zip(ex, TID) if tt == t]
            prof[f"T{t+1}"] = {k: float(np.nanmedian([e[k] for e in et])) for k in ("rc_cold", "rc_gas", "f015", "f05", "ret", "McMb_R500")}
            prof[f"T{t+1}"]["n_no_half"] = int(sum(1 for e in et if not np.isfinite(e["rc_cold"])))
        row["profile_h0672"] = prof; row["cs_KT_median_kms"] = float(np.nanmedian(PRED[(f, lc, r, q, "h0672")]["cs"][I]))
        GRADE[f].append(row)
        c0 = row["cells"]["h0672"]; c1 = row["cells"]["h0686"]
        say(f"\n  {f} c_* 10^{lc:.3f} r {r:+.3f} q {q:+.3f}{' [MGAS500 survivor]' if row['survivor'] else ''}: KT c_s median {row['cs_KT_median_kms']:.0f} km/s -> {row['status']}"
            + (f" (fails: {', '.join(bad)})" if bad else ""))
        for k in keys:
            say(f"     {k:10s} meas {c0[k]['meas']:+.3f}+-{c0[k]['s']:.3f} pred {c0[k]['pred']:+.3f} Z {c0[k]['Z']:+.2f} | h0.686 meas {c1[k]['meas']:+.3f} pred {c1[k]['pred']:+.3f} Z {c1[k]['Z']:+.2f}"
                + ("" if row["ok"][k] else "  FAIL"))
        for k, v in row["rep"]["h0672"].items():
            say(f"     (reported) {k:24s} meas {v['meas']:+.3f}+-{v['s']:.3f} pred {v['pred']:+.3f} Z {v['Z']:+.2f}")
        say("     (reported) cold profile, KT-tercile medians (h0.672): " + "; ".join(
            f"T{t+1} r_c,cold {prof[f'T{t+1}']['rc_cold']:.3f} Mpc vs gas core {prof[f'T{t+1}']['rc_gas']:.3f} (no half inside r_ta: {prof[f'T{t+1}']['n_no_half']}), "
            f"f(<0.15) {prof[f'T{t+1}']['f015']:.3f}, f(<0.5) {prof[f'T{t+1}']['f05']:.3f}, retained {prof[f'T{t+1}']['ret']:.3f} of fair share, M_c/M_b(<R500) {prof[f'T{t+1}']['McMb_R500']:.2f}" for t in range(3)))
RES["grades"] = GRADE
# ============================================================== verdict
say("\n=== VERDICT ===")
def fclass(rows, inner_as):
    st = [("PASS" if (r_["status"] == "PASS" or (r_["status"] == "INNER-ONLY" and inner_as == "PASS")) else "FAIL") for r_ in rows]
    if all(s == "PASS" for s in st): return "PASS"
    if any(s == "PASS" for s in st): return "NARROWS"
    return "EXCLUDES"
VC = {}; BIND = {}
for f in FEET:
    rows = GRADE[f]; a, b = fclass(rows, "PASS"), fclass(rows, "FAIL")
    VC[f] = a if a == b else f"AMBIGUOUS({a}|{b})"
    cnt = {}
    for r_ in rows:
        for k in r_["fails"]: cnt[k] = cnt.get(k, 0) + 1
    BIND[f] = dict(fail_counts=dict(sorted(cnt.items(), key=lambda kv: -kv[1])), at_all_points=[k for k, v in cnt.items() if v == len(rows)],
                   n_pass=sum(r_["status"] == "PASS" for r_ in rows), n_inner_only=sum(r_["status"] == "INNER-ONLY" for r_ in rows), n=len(rows),
                   pass_points=[(r_["log10_cstar"], r_["r"], r_["q"]) for r_ in rows if r_["status"] == "PASS"])
    say(f"  {f}: points PASS {BIND[f]['n_pass']} / INNER-ONLY {BIND[f]['n_inner_only']} / FAIL {len(rows) - BIND[f]['n_pass'] - BIND[f]['n_inner_only']} of {len(rows)}; class {VC[f]}")
    say(f"  {f}: failing-constraint counts {BIND[f]['fail_counts']}; failing at every point: {BIND[f]['at_all_points']}")
if STOP: V = "UNDECIDED (step 0 failed)"
elif any(v.startswith("AMBIGUOUS") for v in VC.values()): V = f"UNDECIDED (INNER-ONLY points change the class: {VC})"
elif VC["canonical"] != VC["alt"]: V = f"UNDECIDED (footings disagree: canonical {VC['canonical']}, alt {VC['alt']})"
elif VC["canonical"] == "PASS": V = "PROFILE PASSES (sheet survives)"
elif VC["canonical"] == "NARROWS":
    V = "PROFILE NARROWS THE SHEET TO " + "; ".join(f"{f} {BIND[f]['pass_points']}" for f in FEET)
else:
    allb = sorted(set(BIND["canonical"]["at_all_points"]) & set(BIND["alt"]["at_all_points"]))
    top = {f: next(iter(BIND[f]["fail_counts"])) for f in FEET}
    V = "PROFILE EXCLUDES THE SHEET (" + (", ".join(allb) if allb else f"most-failing: {top}") + ")"
RES["verdict"] = V; RES["verdict_per_footing"] = VC; RES["binding"] = BIND
check("K4", rss() < 1.0, f"peak RSS {rss():.3f} GB", "< 1 GB")
say(f"\nVERDICT: {V}  (per footing: {VC})")
if MUT:
    must = ("K0a", "K0c"); RES["mutate_required_fail"] = {k: not CHECKS[k] for k in must}
    say("MUTATE: required failures " + ", ".join(f"{k} {'FAILED' if not CHECKS[k] else 'passed (BAD)'}" for k in must))
RES["runtime_s"] = time.time() - T0; RES["peak_rss_GB"] = rss()
say(f"checks {sum(CHECKS.values())}/{len(CHECKS)} PASS; runtime {RES['runtime_s']:.0f} s; peak RSS {RES['peak_rss_GB']:.2f} GB")
json.dump(RES, open(os.path.join(HERE, f"x30_sheet_cluster_profile_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.item() if hasattr(o, "item") else (o.tolist() if hasattr(o, "tolist") else str(o)))
sys.exit(0 if (all(CHECKS.values()) and not MUT) else 1)

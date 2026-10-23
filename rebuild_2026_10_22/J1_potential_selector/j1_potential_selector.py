"""J1_potential_selector (criteria d25b7d87bc): is the depth of the potential |Phi|/c^2 the selector of the law's excesses?
Part A: sympy -- where does Phi itself (not grad Phi) enter the v3 / v4 static actions?
Part B: a0_eff = a0 (1 + |Phi|/Phi_*) (POSTULATED), Phi = Newtonian baryonic potential (zero at infinity) of system + hosts.
  Calibrate phi_* = Phi_*/c^2 on F1's PRIMARY MID band (F1's own input section is exec'd read-only, F1's measurement cache
  in session scratch = argv[1]); predict F1 OUTER/profile, SPARC RAR, E3 satellites (E3's input section exec'd read-only),
  LVD field dwarfs + Lelli+15 TDGs, Solar System and wide binaries (C6 margins), and a monotone bound.
--mutate: the cluster potential integrator keeps only -GM(<r)/r (K5 must fail). Outputs *_MUTATE.*.
Run: OMP_NUM_THREADS=1 nice -n 15 python3 j1_potential_selector.py <F1 KiDS cache dir> [--mutate]"""
import os, sys, io, json, glob, math, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
MUT = "--mutate" in sys.argv; TAG = "_MUTATE" if MUT else ""
CACHE = [a for a in sys.argv[1:] if not a.startswith("--")][0]
OUT = []; RES = {"lane": "J1_potential_selector", "mutate": MUT, "criteria_commit": "d25b7d87bc"}; CHECKS = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def check(name, ok, val, thr):
    CHECKS.append((name, bool(ok))); say(f"{name} {'PASS' if ok else 'FAIL'} {val} {thr}")
    RES.setdefault("checks", {})[name] = dict(pass_=bool(ok), value=str(val), threshold=str(thr))
C_LIGHT = 2.998e8; C2 = C_LIGHT**2
FOOTS = ("canonical", "alt")

# =========================================================================== PART A (sympy)
import sympy as sp
say("=== PART A: where does Phi itself enter the static action? (sympy) ===")
x, y, z, Cc, c, mu, Kq = sp.symbols("x y z C c mu K_q", real=True)
psi = sp.Function("psi")(x, y, z); Jf = sp.Function("J")
Px, Py, Pz = [sp.Function(n)(x, y, z) for n in ("P_x", "P_y", "P_z")]
def statics(ps):
    lnN = ps/c**2; N = sp.exp(lnN); A = [sp.diff(lnN, v) for v in (x, y, z)]
    Y = sum(a**2 for a in A)/c**4; Q = 1/N
    LJ = N*(-2*Jf(Y)); LK = N*2*mu**2*(Q - 1)**2; clock = Px*A[0] + Py*A[1] + Pz*A[2]
    return Y, LJ, LK, clock
Y0, LJ0, LK0, cl0 = statics(psi); Y1, LJ1, LK1, cl1 = statics(psi + Cc)
ra = sp.simplify(Y1 - Y0); rc = sp.simplify(cl1 - cl0); rb = sp.simplify(LJ1 - sp.exp(Cc/c**2)*LJ0)
# (c): the K(Q) sector: second C-derivative at C = 0 (not shift-covariant) and its weak-field EL term
d2K = sp.simplify(sp.diff(LK1, Cc, 2).subs(Cc, 0)); ph = sp.symbols("phi", real=True)
LKw = sp.series((sp.exp(ph/c**2)*2*mu**2*(sp.exp(-ph/c**2) - 1)**2), ph, 0, 3).removeO()
ELK = sp.simplify(sp.diff(LKw, ph))                     # dL/dphi of the mass term at weak field: linear in phi, ~ mu^2
rc_ = sp.simplify(ELK - 4*mu**2*ph/c**4)
k6 = (ra == 0) and (rc == 0) and (rb == 0) and (sp.simplify(d2K) != 0) and (rc_ == 0)
say(f"  (a) Y(psi+C)-Y(psi) = {ra};  clock P.grad ln N shift residual = {rc}")
say(f"  (b) L_J(psi+C) - e^(C/c^2) L_J(psi) = {rb}   (J sector: Phi enters only through sqrt(-g)=N, a 1+O(Phi/c^2) factor)")
say(f"  (c) d2/dC2 L_K at C=0 = {sp.simplify(d2K)} (nonzero: K(Q) is the only non-shift-covariant term)")
say(f"      weak-field dL_K/dphi = {ELK}  -> field-equation term linear in phi with coefficient ~ mu^2 (H2's dust, free zero point)")
check("K6", k6, f"(a) {ra},{rc} (b) {rb} (c) d2K!=0, EL-4mu^2phi/c^4={rc_}", "residuals 0, d2K != 0")
PN = 1.5e-5                                               # |Phi|/c^2 at cluster MID (measured below; PN factor size)
RES["partA"] = dict(Y_shift_invariant=str(ra) == "0", clock_shift_invariant=str(rc) == "0", J_sector_overall_N_factor=str(rb) == "0",
                    K_sector_mu2=str(sp.simplify(d2K)), verdict="NOT IN THE ACTION: no a0(Phi). Phi enters only via (i) the overall N=1+Phi/c^2 "
                    "factor (post-Newtonian, <=1e-5) and (ii) the mu^2 Phi dust term of K(Q)/AeST (H2: wrong cluster shape). a0(Phi) here is POSTULATED (+1 function, +1 constant).")

# =========================================================================== F1 input section (read-only exec)
F1P = os.path.join(REPO, "rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores.py")
src = open(F1P).read(); cut = src.index("# ---------------------------------------------------------------- variant engine")
SCR = os.path.join(CACHE, "j1_f1_exec_scratch.out")
s1 = src[:cut].replace('os.path.join(HERE, f"f1_cluster_cores{TAG}.out")', repr(SCR))
assert repr(SCR) in s1
F1 = {"__file__": F1P, "__name__": "f1_exec"}
_argv = sys.argv; sys.argv = ["f1", CACHE]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s1, F1P, "exec"), F1)
sys.argv = _argv
f1ok = [n for n, ok in F1["CHECKS"]]; f1all = all(ok for _, ok in F1["CHECKS"])
check("K1", f1all and set(f1ok) >= {"K1", "K2", "K4", "K5", "K6"}, f"F1 exec checks {F1['CHECKS']}", "F1 K1 K2 K4 K5 K6 all PASS")
G, MPC, MSUN, KG_PC2 = F1["G"], F1["MPC"], F1["MSUN"], F1["KG_PC2"]
A0 = F1["A0"]; RG = F1["RG"]; MEAS = F1["MEAS"]; N = F1["N"]; DAT = F1["DAT"]; PATCH = F1["PATCH"]; BANDS = F1["BANDS"]
F1R = json.load(open(os.path.join(REPO, "rebuild_2026_10_22", "F1_cluster_cores", "f1_cluster_cores_results.json")))

def phi_of(Menc, r):
    """Newtonian potential (zero at infinity) from enclosed mass Menc [kg] on radii r [m] (mass constant beyond r[-1])."""
    if MUT: return -G*Menc/r
    f = G*Menc/r**2; seg = 0.5*(f[1:] + f[:-1])*np.diff(r); tail = np.r_[np.cumsum(seg[::-1])[::-1], 0.0]
    return -G*Menc[-1]/r[-1] - tail
# K5: Hernquist (wide grid so the tail is negligible)
rt = np.logspace(-3, 6, 20000)*MPC; Mh = 1e14*MSUN; ah = 0.3*MPC
ph_num = phi_of(Mh*rt**2/(rt + ah)**2, rt); ph_ex = -G*Mh/(rt + ah); sel = (rt >= 0.05*MPC) & (rt <= 10*MPC)
k5 = float(np.max(np.abs(ph_num[sel]/ph_ex[sel] - 1)))
check("K5", k5 <= 1e-3, f"max rel {k5:.2e}", "<= 1e-3 at 0.05-10 Mpc")

# per-cluster baryons and potential (F1 PRIMARY: rescale, G0, f* 0.20, mid Mgas, miscentring)
def cl_base(cl, hkey):
    h = F1["HS"][hkey]; q = (float(F1["DM"](cl["z"], h))/(1 + cl["z"]))/F1["DA_lcdm"](cl["z"])
    Mg = F1["gas_mass"](cl, cl["Mgas500"]*q**2.5, cl["R500"]*q, "G0", 1.0); Mb = Mg*1.20
    gN = G*Mb/(RG*MPC)**2; Phi = phi_of(Mb, RG*MPC); d = np.radians(cl["off_deg"])*float(F1["DM"](cl["z"], h))/(1 + cl["z"])
    return gN, np.abs(Phi)/C2, d
BASE = {hk: [cl_base(o, hk) for o in MEAS] for hk in ("h0672", "h0686")}
def predict_cl(b, a0, phis):
    gN, aphi, d = b; a0e = a0*(1 + aphi/phis) if np.isfinite(phis) else a0
    g = F1["g_aqual_sph"](gN, a0e); ML = g*(RG*MPC)**2/G; rho = np.gradient(ML, RG*MPC)/(4*np.pi*(RG*MPC)**2)
    Sig, ds = F1["project"](rho); ds = F1["dsig_from_sig"](F1["offset"](Sig, d)); return F1["at_bins"](ds)/KG_PC2
def Pmat(foot, hk, phis): return np.array([predict_cl(b, A0[foot], phis) for b in BASE[hk]])
def Duse(hk, boost=True): return DAT[hk]["D"]*(DAT[hk]["B"][None, :] if boost else 1.0)
def bands(foot, hk, phis, boost=True):
    Pm = Pmat(foot, hk, phis); return F1["jk"](Duse(hk, boost), Pm, DAT[hk]["W"]), Pm
def profile(hk, Pm, boost=True):
    D = Duse(hk, boost); W = DAT[hk]["W"]; ks = [3, 4, 5, 6, 7]
    f = lambda s: np.array([(W[s][:, k]*D[s][:, k]).sum()/(W[s][:, k]*Pm[s][:, k]).sum() for k in ks])
    full = f(np.ones(N, bool)); reps = np.array([f(PATCH != p) for p in range(30)])
    cov = 29/30*np.einsum("ia,ib->ab", reps - reps.mean(0), reps - reps.mean(0)); hart = (30 - 5 - 2)/(30 - 1)
    r = full - 1; return full, float(r @ np.linalg.solve(cov, r)*hart)
say("\n=== PART B: clusters (F1 PRIMARY) ===")
k2 = []
for hk in ("h0672", "h0686"):
    for f in FOOTS:
        a, _ = bands(f, hk, np.inf); ref = F1R["rows"][f"PRIMARY {hk}"][f]
        k2 += [abs(a["MID"][0]/ref["MID"][0] - 1), abs(a["OUTER"][0]/ref["OUTER"][0] - 1)]
check("K2", max(k2) <= 1e-6, f"max rel {max(k2):.1e}", "<= 1e-6 vs F1 PRIMARY (both h, both footings)")
# cluster potential depth (reported)
ri = [np.argmin(np.abs(RG - r)) for r in (0.1, 0.5, 1.0, 2.0)]
dep = np.array([[b[1][i] for i in ri] for b in BASE["h0672"]])
say("median |Phi_N|/c^2 of the cluster baryons at r = 0.1/0.5/1/2 Mpc (h 0.672): " + " ".join(f"{v:.2e}" for v in np.median(dep, 0)))
RES["cluster_phi_median"] = dict(zip(["0.1", "0.5", "1.0", "2.0"], np.median(dep, 0).tolist()))
CAL = {}
def solve(foot, hk, boost=True):
    lo, hi = np.log10(1e-9), np.log10(1e-2)
    alo = bands(foot, hk, 10**lo, boost)[0]["MID"][0]; ahi = bands(foot, hk, 10**hi, boost)[0]["MID"][0]
    if not (alo < 1 < ahi): return None, alo, ahi
    for _ in range(24):
        m = 0.5*(lo + hi); am = bands(foot, hk, 10**m, boost)[0]["MID"][0]
        (lo, hi) = (m, hi) if am < 1 else (lo, m)
    return 10**(0.5*(lo + hi)), alo, ahi
for f in FOOTS:
    for hk in ("h0672", "h0686"):
        ps, alo, ahi = solve(f, hk); CAL[(f, hk)] = ps
        if ps is None: say(f"CAL {f} {hk}: NO ROOT (A_MID {alo:.3f} at 1e-9, {ahi:.3f} at 1e-2)"); continue
        a, Pm = bands(f, hk, ps); prof, chi2 = profile(hk, Pm)
        a0inf, _ = bands(f, hk, np.inf); prof0, chi20 = profile(hk, Pmat(f, hk, np.inf))
        say(f"CAL {f:9s} {hk}: phi_* = {ps:.3e}  -> MID {a['MID'][0]:.3f}+-{a['MID'][1]:.3f}  OUTER {a['OUTER'][0]:.3f}+-{a['OUTER'][1]:.3f}"
            f"  INNER {a['INNER'][0]:.3f}+-{a['INNER'][1]:.3f}  profile A_k(3-7) {np.round(prof, 3).tolist()} chi2 {chi2:.1f} (law alone {chi20:.1f})")
        RES.setdefault("CAL", {})[f"{f}|{hk}"] = dict(phi_star=ps, A=a, profile=prof.tolist(), chi2=chi2, chi2_law=chi20, profile_law=prof0.tolist())
        psA, _, _ = solve(f, hk, boost=False); RES["CAL"][f"{f}|{hk}"]["phi_star_A1_boost_clipped"] = psA
        say(f"    reported: A1 boost clipped at 1 -> phi_* = {psA if psA is None else f'{psA:.3e}'}")

# =========================================================================== SPARC
say("\n=== (a) SPARC RAR ===")
KPCM = 3.0857e19
Q28 = {}
for l in open(os.path.join(REPO, "real_research", "data", "SPARC_Lelli2016c.mrt")):
    v = l.split()
    if len(v) >= 18 and v[1].isdigit():
        try: Q28[v[0]] = (float(v[5]), int(v[17]), (0.5*float(v[7]) + 1.33*float(v[13]))*1e9)
        except ValueError: pass
SP = dict(gal=[], gb=[], go=[], sl=[], phi=[], Mb=[])
for fn in sorted(glob.glob(os.path.join(REPO, "real_research", "data", "sparc_data", "*_rotmod.dat"))):
    name = os.path.basename(fn).replace("_rotmod.dat", ""); inc, q, Mb = Q28.get(name, (0, 3, np.nan))
    if q > 2 or inc < 30: continue
    rows = [[float(t) for t in l.split()[:6]] for l in open(fn) if not l.startswith("#") and l.strip()]
    rows = np.array(sorted(rows)); Rm = rows[:, 0]*KPCM
    gall = np.clip((rows[:, 3]*np.abs(rows[:, 3]) + 0.5*rows[:, 4]*np.abs(rows[:, 4]) + 0.7*rows[:, 5]*np.abs(rows[:, 5]))*1e6/Rm, 0, None)
    seg = 0.5*(gall[1:] + gall[:-1])*np.diff(Rm); tail = np.r_[np.cumsum(seg[::-1])[::-1], 0.0]
    phiall = (tail + gall[-1]*Rm[-1])/C2
    for j, (R, V, eV, Vg, Vd, Vb) in enumerate(rows):
        if V <= 0 or R <= 0 or eV/V >= 0.10: continue
        g_b = (Vg*abs(Vg) + 0.5*Vd*abs(Vd) + 0.7*Vb*abs(Vb))*1e6/(R*KPCM)
        if g_b <= 0: continue
        SP["gal"].append(name); SP["gb"].append(g_b); SP["go"].append(V*V*1e6/(R*KPCM)); SP["sl"].append(2*eV/V/np.log(10))
        SP["phi"].append(phiall[j]); SP["Mb"].append(Mb)
for k in SP: SP[k] = np.array(SP[k])
n828 = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG828_dwarf_excess_rotation_vs_dispersion", "cfg828_results.json")))["n_sparc"]
check("K3", len(SP["gb"]) == n828, f"n {len(SP['gb'])} vs CFG828 {n828}", "equal")
say(f"SPARC |Phi_N|/c^2 at the data points: median {np.median(SP['phi']):.2e}, 90% {np.percentile(SP['phi'], 90):.2e}, max {SP['phi'].max():.2e}")
RES["sparc_phi"] = dict(median=float(np.median(SP["phi"])), p90=float(np.percentile(SP["phi"], 90)), max=float(SP["phi"].max()))
SMALL = SP["Mb"] <= 3e9
def rar(a0, phis, floor):
    a0e = a0*(1 + SP["phi"]/phis) if np.isfinite(phis) else a0
    r = np.log10(SP["go"]/F1["g_aqual_sph"](SP["gb"], a0e)); s2 = SP["sl"]**2 + floor**2
    return r, r**2/s2
SPARC = {}
for f in FOOTS:
    for hk in ("h0672", "h0686"):
        ps = CAL[(f, hk)]
        if ps is None: continue
        r0, c0 = rar(A0[f], np.inf, 0.10); r1, c1 = rar(A0[f], ps, 0.10); _, c05 = rar(A0[f], np.inf, 0.05); _, c15 = rar(A0[f], ps, 0.05)
        d = float(c1.sum() - c0.sum()); dS = float(c1[SMALL].sum() - c0[SMALL].sum()); dL = float(c1[~SMALL].sum() - c0[~SMALL].sum())
        shift = float(np.median(r0 - r1)); shiftL = float(np.median((r0 - r1)[~SMALL]))
        SPARC[(f, hk)] = d
        say(f"{f:9s} {hk}: dchi2 (floor 0.10) {d:+.1f} [small {dS:+.1f}, large {dL:+.1f}]; floor 0.05: {float(c15.sum() - c05.sum()):+.1f}; "
            f"median predicted shift +{shift:.3f} dex (large galaxies +{shiftL:.3f}); law chi2 {c0.sum():.0f}/{len(c0)}; median residual law {np.median(r0):+.3f} -> {np.median(r1):+.3f}")
        RES.setdefault("sparc", {})[f"{f}|{hk}"] = dict(dchi2=d, dchi2_small=dS, dchi2_large=dL, dchi2_floor005=float(c15.sum() - c05.sum()),
                                                       shift_median=shift, shift_large=shiftL, chi2_law=float(c0.sum()), n=len(c0),
                                                       med_res_law=float(np.median(r0)), med_res_sel=float(np.median(r1)))

# =========================================================================== E3 satellites
say("\n=== (b) dwarf satellites (E3) ===")
E3P = os.path.join(REPO, "doors_push_2026_10_22", "E3_dwarf_excess", "e3_dwarf_excess.py")
s3 = open(E3P).read(); s3 = s3[:s3.index("# ================================================================== PART A")]
E3 = {"__file__": E3P, "__name__": "e3_exec"}
sys.argv = ["e3"]
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s3, E3P, "exec"), E3)
sys.argv = _argv
assert all(ok for _, ok in E3["CHK"]), E3["CHK"]
import csv
LVD = {}
for fn in ("lvd_dwarf_mw.csv", "lvd_dwarf_m31.csv", "lvd_dwarf_local_field.csv"):
    for r in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "dsph", fn))):
        LVD.setdefault(r["name"], r)
KPC = E3["KPC"]; AH = 3.0*KPC; MMW, MM31 = 6.0e10*MSUN, 1.0e11*MSUN
def fl(v):
    try: x = float(v); return x if math.isfinite(x) else None
    except Exception: return None
def host_phi(name, dhost=None, host=None):
    L = LVD.get(name, {}); dgc = fl(L.get("distance_gc")); d31 = fl(L.get("distance_m31"))
    if dgc is None and host == "MW": dgc = dhost
    if d31 is None and host == "M31": d31 = dhost
    p = 0.0
    if dgc is not None: p += G*MMW/(dgc*KPC + AH)
    if d31 is not None: p += G*MM31/(d31*KPC + AH)
    return p/C2, dgc, d31
R0 = 8.122*KPC; PHI_SUN_MW = G*MMW/(R0 + AH)/C2; PHI_SUN = PHI_SUN_MW + G*MSUN/1.496e11/C2
say(f"|Phi|/c^2 at the Sun: MW Hernquist {PHI_SUN_MW:.2e} (+ Sun at 1 AU -> {PHI_SUN:.2e}); point-mass MW {G*MMW/R0/C2:.2e}")
E3R = json.load(open(os.path.join(REPO, "doors_push_2026_10_22", "E3_dwarf_excess", "e3_dwarf_excess_results.json")))["A_above_screened_diag"]
SAT = {}; k4 = []
for f, rows in (("canonical", E3["S_can"]), ("alt", E3["S_alt"])):
    a0 = A0[f]; X = E3["build"](rows, a0, binmode="free")
    ph = np.array([host_phi(r["name"], r["dhost"], r["host"])[0] for r in X["rows"]])
    own = G*X["Ms"]*MSUN/X["r12"]/C2; phis_all = ph[:, None] + own
    nmiss = sum(1 for r in X["rows"] if host_phi(r["name"])[1] is None)
    d0 = X["lb"] - np.log10(E3["B_scr"](X["Ms"], X["r12"], a0, 24.0)); m0 = E3["boot_median"](d0)
    k4.append(abs(m0[0] - E3R[f"{f}|L*24"]["median_Delta"]))
    frac_shallow = float(np.mean(ph < PHI_SUN_MW))
    # epsilon needed per system (central values: medians over the MC)
    lbm = np.median(X["lb"], 1); Msm = np.median(X["Ms"], 1); r12m = np.median(X["r12"], 1); eps = []
    for i in range(len(lbm)):
        lo, hi = 0.0, 8.0
        if np.log10(E3["B_scr"](Msm[i], r12m[i], a0, 24.0)) >= lbm[i]: eps.append(1.0); continue
        for _ in range(60):
            m = 0.5*(lo + hi); (lo, hi) = (m, hi) if np.log10(E3["B_scr"](Msm[i], r12m[i], a0*10**m, 24.0)) < lbm[i] else (lo, m)
        eps.append(10**hi)
    eps = np.array(eps); reach = eps < 0.999e8; eps_med = float(np.median(eps[reach])) if reach.any() else float("nan")   # A1
    sat = np.log10(E3["B_scr"](Msm, r12m, a0*1e8, 24.0)/E3["B_scr"](Msm, r12m, a0, 24.0))
    gNs = G*MMW/(R0 + AH)**2; infl = math.sqrt(F1["g_aqual_sph"](gNs, a0*eps_med)/F1["g_aqual_sph"](gNs, a0))
    Vsun = math.sqrt(F1["g_aqual_sph"](gNs, a0)*R0)/1e3
    SAT[f] = dict(n=len(X["rows"]), phi_median=float(np.median(ph)), phi_max=float(ph.max()), n_missing_gc=nmiss,
                  frac_shallower_than_sun=frac_shallow, base=dict(median=m0[0], sd=m0[1]), n_unreachable=int((~reach).sum()),
                  eps_need_reachable_median=eps_med, Bscr_saturation_median_dex=float(np.median(sat)),
                  MW_Vsun_law=Vsun, MW_Vsun_inflation_at_eps_need=infl)
    say(f"{f:9s}: N {len(X['rows'])}; host |Phi|/c^2 median {np.median(ph):.2e} max {ph.max():.2e} (Sun {PHI_SUN_MW:.2e}); "
        f"shallower than the Sun {frac_shallow*100:.0f}%; no distance_gc {nmiss}; base residual {m0[0]:+.3f}+-{m0[1]:.3f} (E3 {E3R[f'{f}|L*24']['median_Delta']:+.3f})")
    say(f"    [A1] no a0 multiplier <= 1e8 closes {int((~reach).sum())}/{len(eps)} satellites (screened B_scr saturates: median "
        f"log B(1e8 a0)/B(a0) = {np.median(sat):+.3f} dex); reachable ones need epsilon median {eps_med:.1f}; "
        f"a monotone selector then gives the Sun's orbit >= that: MW V(R0) law {Vsun:.0f} km/s x {infl:.2f}")
    for hk in ("h0672", "h0686"):
        ps = CAL[(f, hk)]
        if ps is None: continue
        a0e = a0*(1 + phis_all/ps); d1 = X["lb"] - np.log10(E3["B_scr"](X["Ms"], X["r12"], a0e, 24.0)); m1 = E3["boot_median"](d1)
        dp = float(np.median(np.log10(E3["B_scr"](X["Ms"], X["r12"], a0e, 24.0)/E3["B_scr"](X["Ms"], X["r12"], a0, 24.0))))
        ok = abs(m1[0]) <= 2*m1[1]
        SAT[f][hk] = dict(residual=m1[0], sd=m1[1], pred_shift_median=dp, eps_median=float(np.median(1 + phis_all/ps)), pass_=bool(ok))
        say(f"    {hk}: phi_* {ps:.2e}: epsilon median {np.median(1 + phis_all/ps):.4f}; predicted shift {dp:+.4f} dex; residual {m1[0]:+.3f}+-{m1[1]:.3f} -> {'PASS' if ok else 'FAIL'}")
check("K4", max(k4) <= 0.03, f"max |base - E3| {max(k4):.3f}", "<= 0.03 dex")
RES["satellites"] = SAT

# =========================================================================== (c) field dwarfs + TDGs
say("\n=== (c) isolated field dwarfs (LVD) and tidal dwarfs (Lelli+15) ===")
FIELD = {}
for f in FOOTS:
    a0 = A0[f]; fd = [r for r in E3["ALL"] if r["host"] == "field"]
    ms = np.array([10**r["logms"] for r in fd]); r12 = np.array([(4/3)*r["rh"]*E3["PC"] for r in fd])
    ph = np.array([host_phi(r["name"])[0] for r in fd]) + G*ms*MSUN/r12/C2
    TD = [r for r in csv.DictReader(l for l in open(os.path.join(REPO, "real_research", "data", "tdg", "lelli2015_tdgs.csv")) if not l.startswith("#"))]
    Mt = np.array([float(r["Mbar"])*1e8 for r in TD]); Rt = np.array([float(r["Rout"]) for r in TD])*KPC
    pht = (np.array([float(r["gNe_a0"]) for r in TD])*1.30e-10*np.array([float(r["Dp"]) for r in TD])*KPC + G*Mt*MSUN/Rt)/C2
    gNt = G*Mt*MSUN/Rt**2; Vlaw = np.sqrt(F1["g_aqual_sph"](gNt, a0)*Rt)/1e3; Vobs = np.array([float(r["Vcirc"]) for r in TD])
    FIELD[f] = dict(n_field=len(fd), field_phi_median=float(np.median(ph)), tdg_phi=pht.tolist(),
                    tdg_Vobs_over_Vlaw=(Vobs/Vlaw).tolist(), tdg_names=[r["name"] for r in TD])
    for hk in ("h0672", "h0686"):
        ps = CAL[(f, hk)]
        if ps is None: continue
        sf = np.log10(E3["B_scr"](ms, r12, a0*(1 + ph/ps), 24.0)/E3["B_scr"](ms, r12, a0, 24.0))
        st = np.log10(F1["g_aqual_sph"](gNt, a0*(1 + pht/ps))/F1["g_aqual_sph"](gNt, a0))
        allv = np.r_[sf, st]; ok = (np.median(np.abs(allv)) <= 0.05) and (np.max(np.abs(allv)) <= 0.10)
        FIELD[f][hk] = dict(field_shift_median=float(np.median(sf)), field_shift_max=float(np.max(np.abs(sf))),
                            tdg_shift=st.tolist(), pass_=bool(ok))
        say(f"{f:9s} {hk}: {len(fd)} LVD field dwarfs |Phi|/c^2 median {np.median(ph):.1e}: shift median {np.median(sf):+.4f}, max {np.max(np.abs(sf)):.4f} dex; "
            f"6 TDGs |Phi|/c^2 <= {pht.max():.1e}: shift max {np.max(np.abs(st)):.4f} dex -> {'PASS' if ok else 'FAIL'}")
    say(f"    context (not graded): TDG V_obs/V_law(isolated) = {np.round(Vobs/Vlaw, 2).tolist()} ({f})")
RES["field_tdg"] = FIELD

# =========================================================================== (d)(e) Solar System, wide binaries
say("\n=== (d) Solar System, (e) wide binaries ===")
SS = {}
for f in FOOTS:
    for hk in ("h0672", "h0686"):
        ps = CAL[(f, hk)]
        if ps is None: continue
        e = 1 + PHI_SUN/ps; okd = (0.173*e < 1) and (3.6e-8*e**2 < 1); oke = 8.1e-6*e**2 < 1e-2
        SS[f"{f}|{hk}"] = dict(eps_sun=e, planets_Mars=0.173*e, cassini=3.6e-8*e**2, wb_gamma_minus_1=8.1e-6*e**2, pass_d=bool(okd), pass_e=bool(oke))
        say(f"{f:9s} {hk}: eps_sun {e:.4f}; Mars {0.173*e:.3f} of bound; Q2 {3.6e-8*e**2:.1e} of Park -> (d) {'PASS' if okd else 'FAIL'}; "
            f"WB gamma_v-1 {8.1e-6*e**2:.1e} -> (e) {'PASS' if oke else 'FAIL'}")
RES["solar"] = SS

# =========================================================================== verdict (frozen rule)
say("\n=== VERDICT (frozen rule) ===")
V = {}
for f in FOOTS:
    hs = ("h0672", "h0686"); cal = all(CAL[(f, h)] is not None for h in hs)
    if not cal: V[f] = dict(verdict="FAILS", why="CAL impossible"); say(f"{f}: FAILS (calibration impossible)"); continue
    O1 = all(abs(RES["CAL"][f"{f}|{h}"]["A"]["OUTER"][0] - 1) <= 2*RES["CAL"][f"{f}|{h}"]["A"]["OUTER"][1] and RES["CAL"][f"{f}|{h}"]["chi2"] <= 11.07 for h in hs)
    a = all(SPARC[(f, h)] <= 9 for h in hs); b = all(SAT[f][h]["pass_"] for h in hs); cc = all(FIELD[f][h]["pass_"] for h in hs)
    d = all(SS[f"{f}|{h}"]["pass_d"] for h in hs); e = all(SS[f"{f}|{h}"]["pass_e"] for h in hs)
    L = dict(CAL=True, O1=O1, a=a, b=b, c=cc, d=d, e=e)
    v = "SELECTOR WORKS" if all(L.values()) else ("FAILS" if (not b and (not O1 or not a)) else "PARTIAL")
    V[f] = dict(verdict=v, lines=L); say(f"{f}: {v}  " + " ".join(f"{k}:{'PASS' if x else 'FAIL'}" for k, x in L.items()))
RES["verdict"] = V; RES["tag"] = "POSTULATED addition (+1 function, +1 constant phi_*); not in the v3/v4 action (Part A)"
npass = sum(ok for _, ok in CHECKS); say(f"J1_POTENTIAL_SELECTOR COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
open(os.path.join(HERE, f"j1_potential_selector{TAG}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(RES, open(os.path.join(HERE, f"j1_potential_selector_results{TAG}.json"), "w"), indent=1,
          default=lambda o: o.tolist() if hasattr(o, "tolist") else (float(o) if isinstance(o, (np.floating, np.integer)) else str(o)))
sys.exit(0 if npass == len(CHECKS) else 1)

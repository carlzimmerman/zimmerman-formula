#!/usr/bin/env python3
"""D10_native_Lstar -- the EFE-aware native L* floor from NGC 2419, Pal 4, Pal 14 (Pal 3 reported).
Criteria: FROZEN_CRITERIA.md (e3333cb274; amendment A1 ecec1ce9e7, pre-result).
Theory: C4-literal stiffened static equations (gamma_F = 0), own axisymmetric solver (d10_solver.py).
Run from anywhere:  OMP_NUM_THREADS=1 nice -n 15 python3 d10_native_lstar.py [--mutate]
--mutate: the 2D solver uses L*^2 instead of L*^2/2 (K2/K4 must break); validations only, production skipped.
kappa = 1/2 FITTED.  Footings never pooled.  Not theory closed."""
import os, sys, json, math, time, resource
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import d10_solver as S  # noqa: E402

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
CHK = {}
def check(cid, ok, val, thr, label):
    CHK[cid] = dict(ok=bool(ok), value=val, threshold=thr, label=label)
    P(f"{cid} {'PASS' if ok else 'FAIL'} {val} {thr} :: {label}")

# ------------------------------------------------------------------ constants (CFG820 / E4 verbatim)
G, Msun, kpc, PC = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}            # record FP0 footing values (CFG820, E4)
UPS_V, WID = 1.6, 0.15
A_H = 3.0 * kpc                                              # A60 Hernquist scale
GE2_8KPC = 2.0592e-10                                        # D7b inputs: E2 kinematic total at 8 kpc (2.2 x 9.36e-11)
CL = json.load(open(os.path.join(REPO, "campaign_fresh_gravity", "CFG332_globulars_three_routes", "cfg332_globulars_results.json")))
GC = CL["clusters"]; UMF = CL["route2"]["ups_mf"]
# raw RV-bin radii (arcsec) and distances (kpc) from the Baumgardt tables on disk
GCDIR = os.path.join(REPO, "real_research", "data", "globular_clusters")
def rows(fn):
    out = {}
    for line in open(fn, encoding="utf-8"):
        if line.startswith("#") or line.startswith("ClusterName"): continue
        f = line.rstrip("\n").split("\t"); out.setdefault(f[0], []).append(f)
    return out
par, prof = rows(os.path.join(GCDIR, "baumgardt_gc_parameters.tsv")), rows(os.path.join(GCDIR, "baumgardt_gc_veldisp_profiles.tsv"))
for g in GC:
    D = float(par[g["name"]][0][3].split("+-")[0]); g["D"] = D
    pr = [p for p in prof[g["name"]] if p[6] == "RV"]
    if len(pr) == 1:
        g["Rbin_pc"] = float(pr[0][1]) / 206265.0 * D * 1e3
    else:                                                    # CFG332 interpolated the profile at r_h,l
        g["Rbin_pc"] = g["rhl"]
    g["Rbin"] = g["Rbin_pc"] / g["rhl"]
NAMES = [g["name"] for g in GC]; PRIMARY = ["NGC 2419", "Pal 4", "Pal 14"]

def g_mw(R_kpc, Mb, a0):
    gN = G * Mb * Msun / (R_kpc * kpc + A_H) ** 2
    return 0.5 * gN * (1 + math.sqrt(1 + 4 * a0 / gN))
def Mb_hi(a0):
    gN = GE2_8KPC ** 2 / (GE2_8KPC + a0)
    return gN * (8 * kpc + A_H) ** 2 / G / Msun
EBR = {foot: {"E_lo": 4.0e10, "E_mid": 6.0e10, "E_hi": Mb_hi(a0)} for foot, a0 in A0.items()}

R = dict(lane="D10_native_Lstar", mutate=MUT, frozen="e3333cb274", amendment_A1="ecec1ce9e7",
         clusters={g["name"]: {k: g[k] for k in ("so", "eso", "N", "LV", "rhl", "RGC", "D", "Rbin_pc", "Rbin")} for g in GC},
         MW_Mb=EBR)
T0 = time.time()
P("=" * 100); P("D10_native_Lstar  EFE-aware native L* floor" + ("   *** MUTATE: L*^2 stiffness in the 2D solver ***" if MUT else "")); P("=" * 100)
for g in GC:
    P(f"  {g['name']:9s} sigma_obs {g['so']:.3f}+-{g['eso']:.3f} N {g['N']}  L_V {g['LV']:.3e}  r_h,l {g['rhl']:.2f} pc  R_GC {g['RGC']:.2f}  R_bin {g['Rbin_pc']:.2f} pc ({g['Rbin']:.3f} a)")
for foot in A0:
    P(f"  MW bracket [{foot}]: " + ", ".join(f"{k} M_b {v:.3e}" for k, v in EBR[foot].items())
      + " | x_e: " + ", ".join(f"{g['name']} " + "/".join(f"{g_mw(g['RGC'], v, A0[foot]) / A0[foot]:.4f}" for v in EBR[foot].values()) for g in GC))

# ------------------------------------------------------------------ K1 sympy
import sympy as sy
v1, v2, v3, x, kk, L, m, PhiN = sy.symbols("v1 v2 v3 x k L m PhiN", positive=True)
v = sy.Matrix([v1, v2, v3]); vm = sy.sqrt(v1 ** 2 + v2 ** 2 + v3 ** 2)
p = v / (1 + vm); pm = sy.sqrt(sum(c ** 2 for c in p))
ra = sy.simplify((p / (1 - pm) - v).applyfunc(sy.simplify))
res_a = max(abs(float(sy.N(c.subs({v1: 0.3, v2: 1.7, v3: 0.05})))) for c in ra) if any(c != 0 for c in ra) else 0.0
psih, chih, sh = sy.symbols("psih chih sh")
sol = sy.solve([sy.Eq(-kk ** 2 * psih, sh), sy.Eq(sh, -kk ** 2 * m * chih), sy.Eq(chih, PhiN + psih + L ** 2 / 2 * sh)], [psih, chih, sh], dict=True)[0]
res_b = sy.simplify(sol[psih] / PhiN - m / (1 - m + (kk * L) ** 2 * m / 2))
Jp = p.jacobian(v).subs({v1: 0, v2: 0, v3: x})
res_b2 = sy.simplify(Jp - sy.diag(1 / (1 + x), 1 / (1 + x), 1 / (1 + x) ** 2))
res_c = sy.simplify((v - p - (vm / (1 + vm)) * v).applyfunc(sy.simplify))
k1ok = (res_a == 0 and res_b == 0 and all(c == 0 for c in res_b2) and all(c == 0 for c in res_c))
check("K1", k1ok, f"h(p(v))-v:{res_a} kernel:{res_b} dp/dv:{list(res_b2)} AQUAL:{list(res_c)}", "all 0",
      "sympy: p=v/(1+|v|) inverts h; linear response = C6 kernel m/(1-m+kap^2 m/2); dp/dv at background; L*=0 is AQUAL mu=x/(1+x)")

# ------------------------------------------------------------------ K2, K3 isolated
GR = S.Grid2D(nper=24, Nt=16)
k2d = []
for y in (0.04, 3.0):
    for Lam in (0.5, 2.0, 8.0):
        sv = S.Solver2D(GR, y, 0.0, Lam, isolated=True, mutate=MUT); sv.solve(); rf, gr = sv.field_monopole()
        r1, g1, st = S.iso_1d(y, Lam)
        Rl = [0.83, 1.0]
        s2a, _, _ = S.jeans(rf, gr, Rl); s2b, _, _ = S.jeans(r1, g1, Rl)
        i = np.argmin(abs(np.log(rf)))
        dg = abs(gr[i] / np.interp(rf[i], r1, g1) - 1); ds = float(np.max(abs(np.sqrt(s2a / s2b) - 1)))
        k2d.append(max(dg, ds)); P(f"   K2 y {y} Lam {Lam}: |dg/g| at r=a {dg:.2e}, |d sigma_p/sigma_p| {ds:.2e}, res {sv.res:.1e}, bvp status {st}")
check("K2", max(k2d) < 2e-3, f"{max(k2d):.2e}", "< 2e-3", "isolated 2D vs independent 1D BVP (field at r=a and sigma_p)")
k3 = []
for y in (0.04, 3.0):
    sv = S.Solver2D(GR, y, 0.0, 0.0, isolated=True, mutate=MUT); sv.solve(); rf, gr = sv.field_monopole()
    gl = S.law_v(S.plummer_gN(rf, y))
    s2a, _, _ = S.jeans(rf, gr, [0.83, 1.0]); s2b, _, _ = S.jeans(rf, gl, [0.83, 1.0])
    k3.append(float(np.max(abs(np.sqrt(s2a / s2b) - 1))))
check("K3", max(k3) < 2e-3, f"{max(k3):.2e}", "< 2e-3", "isolated L*=0: 2D sigma_p equals the algebraic law (spherical AQUAL)")

# ------------------------------------------------------------------ K4 linear EFE vs Route F
k4 = []
for Lam in (0.0, 1.0, 4.0):
    xe = 0.1; y = 1e-4 * xe
    sv = S.Solver2D(GR, y, xe, Lam, mutate=MUT); sv.solve(tol=1e-14); rf, gr = sv.field_monopole()
    F, newt = S.routeF_monopole(y, xe, Lam, 1.0)
    d = abs(np.interp(0.0, np.log(rf), gr) / F - 1); k4.append(d)
    P(f"   K4 Lam {Lam}: 2D {np.interp(0.0, np.log(rf), gr):.6e} Route F {F:.6e} rel {d:.2e} (Route F Newton self-check {newt / S.plummer_gN(1.0, y) - 1:.1e})")
check("K4", max(k4) < 2e-2, f"{max(k4):.2e}", "< 2e-2", "linear EFE (y=1e-4 x_e, x_e=0.1): 2D monopole field at r=a vs Route F (C6 kernel)")

# ------------------------------------------------------------------ K5 Newton limit
sv = S.Solver2D(GR, 0.2, 0.1, 1e4, mutate=MUT); sv.solve(); rf, gr = sv.field_monopole()
s2a, _, _ = S.jeans(rf, gr, [1.0]); s2n, _, _ = S.jeans(rf, S.plummer_gN(rf, 0.2), [1.0])
k5 = float(abs(math.sqrt(s2a[0] / s2n[0]) - 1))
check("K5", k5 < 2e-3, f"{k5:.2e}", "< 2e-3", "Lam = 1e4 (x_e 0.1, y 0.2) gives the Newtonian Jeans sigma_p")

# ------------------------------------------------------------------ K6 convergence
def sig_case(grid, y, xe, Lam, R):
    sv = S.Solver2D(grid, y, xe, Lam, mutate=MUT); sv.solve(); rf, gr = sv.field_monopole()
    return math.sqrt(S.jeans(rf, gr, [R])[0][0])
k6 = []
for g in GC:
    if g["name"] not in ("NGC 2419", "Pal 14"): continue
    a0 = A0["canonical"]; a = g["rhl"] * PC; y = G * UPS_V * g["LV"] * Msun / (a * a * a0); xe = g_mw(g["RGC"], 6e10, a0) / a0
    base = sig_case(GR, y, xe, 1.0, g["Rbin"])
    fine = sig_case(S.Grid2D(nper=48, Nt=32), y, xe, 1.0, g["Rbin"])
    far = sig_case(S.Grid2D(nper=24, Nt=16, rout=1e5), y, xe, 1.0, g["Rbin"])
    d = max(abs(fine / base - 1), abs(far / base - 1)); k6.append(d)
    P(f"   K6 {g['name']}: base {base:.6f} fine {fine:.6f} far {far:.6f} (dimensionless sigma)")
check("K6", max(k6) < 5e-3, f"{max(k6):.2e}", "< 5e-3", "doubling N_r, N_theta and r_out x 10 (E_mid, canonical, Lam = 1)")

# ------------------------------------------------------------------ K7 Jeans numerics
rfN = GR.re[1:-1]; gN1 = S.plummer_gN(rfN, 1.0)
lw, vir = S.jeans_lw_check(rfN, gN1)
k7a = abs(vir / (math.pi / 32) - 1); k7b = abs(lw / vir - 1)
P(f"   K7 frozen-text constant (3pi/64) ratio {vir / (3 * math.pi / 64):.6f} (fails by construction; amendment A1)")
check("K7", k7a < 1e-3 and k7b < 2e-3, f"{k7a:.2e}/{k7b:.2e}", "< 1e-3 / < 2e-3", "Plummer virial sigma^2 = (pi/32) GM/a (A1); luminosity-weighted sigma_p^2 = virial")

# ------------------------------------------------------------------ binaries (CFG334 generator, verbatim distributions)
M1, RSUN, DAY = 0.8, 6.957e8, 86400.0
def ml_sigma(vv, e):
    s2 = np.maximum(vv.var(axis=1) - (e ** 2).mean(axis=1), 1e-4)
    for _ in range(200):
        w = 1.0 / (s2[:, None] + e ** 2)
        mu = (w * vv).sum(1) / w.sum(1)
        s2 = np.maximum(((w ** 2) * ((vv - mu[:, None]) ** 2 - e ** 2)).sum(1) / (w ** 2).sum(1), 1e-4)
    return np.sqrt(s2)
def kepler_E(Mn, ecc):
    E = Mn.copy()
    for _ in range(40): E = E - (E - ecc * np.sin(E) - Mn) / (1 - ecc * np.cos(E))
    return E
def binary_vlos(n, rng):
    out = np.empty(n); filled = 0
    while filled < n:
        mm = 4 * (n - filled) + 100
        Pd = 10 ** rng.normal(4.8, 2.3, mm); q = rng.uniform(0.1, 1.0, mm); ecc = np.sqrt(rng.uniform(0, 1, mm))
        Mt = M1 * (1 + q) * Msun; a = (G * Mt * (Pd * DAY) ** 2 / (4 * math.pi ** 2)) ** (1 / 3)
        ok = (a * (1 - ecc) >= 3 * 10 * RSUN) & (a < 0.1 * PC)
        Pd, q, ecc, a = Pd[ok], q[ok], ecc[ok], a[ok]; k = len(Pd)
        inc = np.arccos(rng.uniform(-1, 1, k)); om = rng.uniform(0, 2 * math.pi, k); Mn = rng.uniform(0, 2 * math.pi, k)
        E = kepler_E(Mn, ecc); nu = 2 * np.arctan2(np.sqrt(1 + ecc) * np.sin(E / 2), np.sqrt(1 - ecc) * np.cos(E / 2))
        K = (2 * math.pi * a / (Pd * DAY)) * (q / (1 + q)) * np.sin(inc) / np.sqrt(1 - ecc ** 2)
        vv = K * (np.cos(nu + om) + ecc * np.cos(om)) / 1e3
        t = min(k, n - filled); out[filled:filled + t] = vv[:t]; filled += t
    return out
class Draws:
    """common random numbers for one cluster: unit normals, binary offsets, binary uniforms, error normals."""
    def __init__(s, N, nd, seed):
        rng = np.random.default_rng(seed)
        s.Z = rng.standard_normal((nd, N)); s.U = rng.uniform(0, 1, (nd, N)); s.Eps = rng.standard_normal((nd, N))
        s.B = binary_vlos(nd * N, rng).reshape(nd, N); s.N = N
    def sim(s, sint, e, f):
        vv = sint * s.Z + np.where(s.U < f, s.B, 0.0)
        if e > 0: vv = vv + e * s.Eps; return ml_sigma(vv, np.full(vv.shape, e))
        return vv.std(axis=1, ddof=1)
dr = Draws(22, 20000, 334)
sk = dr.sim(0.75, 1.0, 0.3); pk = float((sk >= 1.70).mean()); mk = float(np.median(sk))
check("K8", abs(pk - 0.26) < 0.03 and abs(mk - 1.16) < 0.05, f"P {pk:.4f} median {mk:.3f}", "|P-0.26|<0.03, |med-1.16|<0.05",
      "CFG334 primary reproduced (N 22, sigma_int 0.75, e 1.0, f 0.3)")

# ------------------------------------------------------------------ K9 bridge to E4 N1
from scipy.optimize import brentq
ST_s = np.array([0.01, 0.1, 0.3, 1, 3, 10, 100, 1000]); ST_S = np.array([0.0050, 0.048, 0.134, 0.358, 0.663, 0.894, 0.990, 0.998999])
def Sfun(s):
    if s <= 0.01: return s / 2
    if s >= 1000: return 1 - 1 / s
    return float(np.interp(math.log(s), np.log(ST_s), ST_S))
def nu_L(yy): return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / max(yy, 1e-300)))
def e4_pred(g, a0, Lst):
    M = UPS_V * g["LV"]; sN = math.sqrt(G * M * Msun / (6.0 * (4.0 / 3.0) * g["rhl"] * PC)) / 1e3
    if Lst is None: return sN
    yy = G * (M * Msun / 2) / ((4.0 / 3.0) * g["rhl"] * PC) ** 2 / a0; B = nu_L(yy)
    rM = math.sqrt(G * M * Msun / a0) / PC; s = (4.0 / 3.0) * g["rhl"] / (Lst ** 2 / (2 * rM))
    return sN * math.sqrt(1 + Sfun(s) * (B - 1))
vU = (math.log(10) * WID / 2) ** 2
def e4_chi2(a0, Lst):
    return sum((math.log(g["so"]) - math.log(e4_pred(g, a0, Lst))) ** 2 / ((g["eso"] / g["so"]) ** 2 + vU) for g in GC if g["name"] in PRIMARY)
E4G = np.geomspace(5.75, 3000, 6000)
def e4_floor(a0):
    c = np.array([e4_chi2(a0, Lst) for Lst in E4G]); cmin = min(c.min(), e4_chi2(a0, None)); i = np.where(c - cmin <= 3.84)[0][0]
    return float(brentq(lambda Lst: e4_chi2(a0, Lst) - cmin - 3.84, E4G[i - 1], E4G[i], xtol=1e-6))
k9 = {f: e4_floor(a0) for f, a0 in A0.items()}
check("K9", abs(k9["canonical"] - 28.853) <= 0.02 and abs(k9["alt"] - 29.123) <= 0.02, f"{k9['canonical']:.3f}/{k9['alt']:.3f}",
      "28.853/29.123 +-0.02", "E4 N1 machinery (Wolf, nu_L, CFG691 S(s), Ups 1.6) reproduced")
R["K9_E4_N1"] = k9

# ------------------------------------------------------------------ production
UPSG = np.geomspace(0.1, 8.0, 15)
LG = np.geomspace(2.0, 500.0, 24)
SIGT = {}
if not MUT:
    P("\n--- production: solve per footing x MW bracket x cluster x Ups x L* ---")
    nsolve = 0; worst = 0.0
    for foot, a0 in A0.items():
        for ek, Mb in EBR[foot].items():
            for g in GC:
                a = g["rhl"] * PC; xe = g_mw(g["RGC"], Mb, a0) / a0; unit = math.sqrt(a0 * a) / 1e3
                tab = np.zeros((3, len(UPSG), len(LG) + 2))      # estimators x Ups x [AQUAL, LG..., Newton]
                for iu, ups in enumerate(UPSG):
                    y = G * ups * g["LV"] * Msun / (a * a * a0)
                    sv = S.Solver2D(GR, y, xe, 0.0); U, res, _ = sv.solve(); worst = max(worst, res); nsolve += 1
                    rf, gr = sv.field_monopole(); s2, vir, wo = S.jeans(rf, gr, [g["Rbin"]]); tab[:, iu, 0] = [s2[0], vir, wo]
                    for il, Lst in enumerate(LG):
                        sv = S.Solver2D(GR, y, xe, Lst * PC / a); U, res, _ = sv.solve(U0=U); worst = max(worst, res); nsolve += 1
                        rf, gr = sv.field_monopole(); s2, vir, wo = S.jeans(rf, gr, [g["Rbin"]]); tab[:, iu, il + 1] = [s2[0], vir, wo]
                    s2, vir, wo = S.jeans(rf, S.plummer_gN(rf, y), [g["Rbin"]]); tab[:, iu, -1] = [s2[0], vir, wo]
                SIGT[(foot, ek, g["name"])] = np.sqrt(tab) * unit
            P(f"   [{foot} {ek}] done ({nsolve} solves, worst scaled residual {worst:.1e}, {time.time() - T0:.0f} s)")
    P(f"   production convergence (reported, not a frozen check): worst scaled residual {worst:.1e} ({'all < 1e-8' if worst < 1e-8 else 'SOME ABOVE 1e-8'})")
    R["solves"] = nsolve; R["worst_residual"] = worst

# ------------------------------------------------------------------ likelihood tables (binaries)
SIGI = np.geomspace(0.05, 30.0, 80)
FB = (0.0, 0.1, 0.3, 0.5)
LIK = {}
if not MUT:
    P("\n--- binary-aware likelihood tables (CFG334 generator; per-cluster e_c calibrated to eso/so) ---")
    R["e_c"] = {}
    for ic, g in enumerate(GC):
        drc = Draws(g["N"], 8000, 1000 + ic)
        target = g["eso"] / g["so"]
        spread = lambda e: float(np.std(np.log(drc.sim(g["so"], e, 0.0))))
        if spread(0.0) >= target: ec = 0.0
        else: ec = brentq(lambda e: spread(e) - target, 0.0, 5 * g["so"], xtol=1e-4)
        R["e_c"][g["name"]] = ec
        P(f"   {g['name']:9s} e_c {ec:.3f} km/s (target spread {target:.3f}; f_b=0 spread at e=0 {spread(0.0):.3f})")
        for f in FB:
            lp = np.zeros(len(SIGI)); x0 = math.log(g["so"])
            for i, si in enumerate(SIGI):
                ls = np.log(drc.sim(si, ec, f)); sd = ls.std(); iqr = np.subtract(*np.percentile(ls, [75, 25]))
                h = 0.9 * min(sd, iqr / 1.34) * len(ls) ** -0.2
                lp[i] = math.log(max(np.mean(np.exp(-0.5 * ((x0 - ls) / h) ** 2)) / (h * math.sqrt(2 * math.pi)), 1e-300))
            LIK[(g["name"], f)] = lp

def prior_of(pk, name):
    if pk == "P1": return UPS_V, WID
    br = "K" if pk == "P2" else "S"; return UMF[br][name][0], UMF[br][name][1]
LU = np.linspace(math.log(UPSG[0]), math.log(UPSG[-1]), 600)
def lnL_cluster(foot, ek, name, pk, f, est, il):
    sig = SIGT[(foot, ek, name)][est, :, il]
    lsig = np.interp(LU, np.log(UPSG), np.log(sig))
    lp = np.interp(lsig, np.log(SIGI), LIK[(name, f)], left=-690.0, right=-690.0)
    c, w = prior_of(pk, name); z = (LU / math.log(10) - math.log10(c)) / w; pr = np.exp(-0.5 * z * z); pr /= np.trapz(pr, LU)
    mx = lp.max(); return mx + math.log(max(np.trapz(pr * np.exp(lp - mx), LU), 1e-300))
def chi2_curve(foot, ek, pk, f, est, names):
    nL = len(LG) + 2
    c = np.array([-2 * sum(lnL_cluster(foot, ek, n, pk, f, est, il) for n in names) for il in range(nL)])
    return c
def L95(c):
    cmin = c.min(); d = c - cmin
    if d[0] <= 3.84: return 0.0, d                   # AQUAL allowed: no floor
    inner = d[1:-1]; ok = np.where(inner <= 3.84)[0]
    if len(ok) == 0: return (float("inf") if d[-1] <= 3.84 else float("nan")), d
    i = ok[0]
    if i == 0: return float(LG[0]), d
    x1, x2 = math.log(LG[i - 1]), math.log(LG[i]); y1, y2 = inner[i - 1] - 3.84, inner[i] - 3.84
    return float(math.exp(x1 + (x2 - x1) * y1 / (y1 - y2))), d

if not MUT:
    P("\n--- L*_95 (Delta chi2 = 3.84; chi2_min over AQUAL, the L* grid and Newton) ---")
    EST = {"E-P": 0, "E-V": 1, "E-W": 2}
    TABLE = {}
    for foot in A0:
        for pk in ("P1", "P2", "P3"):
            for ek in ("E_lo", "E_mid", "E_hi"):
                c = chi2_curve(foot, ek, pk, 0.3, 0, PRIMARY); l, d = L95(c)
                TABLE[f"{foot}|{pk}|{ek}"] = dict(L95=l, dchi2_AQUAL=float(d[0]), dchi2_Newton=float(d[-1]), chi2_min=float(c.min()),
                                                  argmin=("AQUAL" if c.argmin() == 0 else ("Newton" if c.argmin() == len(c) - 1 else float(LG[c.argmin() - 1]))))
                P(f"   [{foot:9s} {pk} {ek:5s}] L*_95 {l:8.2f} pc | dchi2 AQUAL {d[0]:7.2f}  Newton {d[-1]:5.2f}  min at {TABLE[f'{foot}|{pk}|{ek}']['argmin']}")
    R["band_cells"] = TABLE
    SENS = {}
    for foot in A0:
        for f in FB:
            l, d = L95(chi2_curve(foot, "E_mid", "P1", f, 0, PRIMARY)); SENS[f"{foot}|f_b={f}"] = l
        for est, ie in EST.items():
            l, d = L95(chi2_curve(foot, "E_mid", "P1", 0.3, ie, PRIMARY)); SENS[f"{foot}|{est}"] = l
        l, d = L95(chi2_curve(foot, "E_mid", "P1", 0.3, 0, NAMES)); SENS[f"{foot}|all four"] = l
        c = chi2_curve(foot, "E_mid", "P1", 0.3, 0, PRIMARY)
        per = {n: (-2 * np.array([lnL_cluster(foot, "E_mid", n, "P1", 0.3, 0, il) for il in range(len(LG) + 2)])) for n in NAMES}
        R[f"chi2_curve|{foot}|central"] = dict(L=[0.0] + LG.tolist() + ["inf"], chi2=c.tolist(), per_cluster={n: v.tolist() for n, v in per.items()})
        P(f"   [{foot}] sensitivity (P1, E_mid): " + ", ".join(f"{k.split('|')[1]} {v:.2f}" for k, v in SENS.items() if k.startswith(foot)))
        for n in NAMES:
            v = per[n] - per[n].min()
            P(f"      {n:9s} dchi2 vs L*: AQUAL {v[0]:6.2f} | 10 pc {np.interp(math.log(10), np.log(LG), v[1:-1]):6.2f} | 30 pc {np.interp(math.log(30), np.log(LG), v[1:-1]):6.2f} | 90 pc {np.interp(math.log(90), np.log(LG), v[1:-1]):6.2f} | Newton {v[-1]:5.2f}")
        # predicted sigma at the central cell (Ups 1.6) for reference
        iu = np.argmin(abs(np.log(UPSG / 1.6)))
        for n in NAMES:
            sg = SIGT[(foot, "E_mid", n)][0, iu]
            P(f"      {n:9s} sigma_p(Ups {UPSG[iu]:.2f}) AQUAL {sg[0]:.3f} | 24 pc {np.interp(math.log(24), np.log(LG), sg[1:-1]):.3f} | 50 pc {np.interp(math.log(50), np.log(LG), sg[1:-1]):.3f} | 90 pc {np.interp(math.log(90), np.log(LG), sg[1:-1]):.3f} | Newton {sg[-1]:.3f} km/s (obs {R['clusters'][n]['so']:.3f})")
    R["sensitivity"] = SENS
    R["sigma_tables"] = {"|".join(k): v.tolist() for k, v in SIGT.items()}; R["Ups_grid"] = UPSG.tolist(); R["L_grid"] = LG.tolist()
    R["lik_tables"] = {f"{k[0]}|{k[1]}": v.tolist() for k, v in LIK.items()}; R["sigma_int_grid"] = SIGI.tolist()

    P("\n--- verdict lines ---")
    VER = {}
    for foot in A0:
        cen = TABLE[f"{foot}|P1|E_mid"]["L95"]; cells = [TABLE[f"{foot}|{pk}|{ek}"]["L95"] for pk in ("P1", "P2", "P3") for ek in ("E_lo", "E_mid", "E_hi")]
        lo, hi = min(cells), max(cells)
        if lo > 90: win = "ABOVE"
        elif lo >= 20 and hi <= 90: win = "INSIDE"
        elif hi < 20: win = "BELOW"
        else: win = "STRADDLES " + ("the 90 pc edge" if hi > 90 and lo >= 20 else ("the 20 pc edge" if lo < 20 and hi <= 90 else "both edges"))
        ref = {"canonical": 23.96, "alt": 24.72}[foot]
        mv = "FLOOR MOVES" if abs(cen / ref - 1) > 0.10 else "FLOOR HOLDS"
        aq = all(TABLE[f"{foot}|{pk}|{ek}"]["dchi2_AQUAL"] > 3.84 for pk in ("P1", "P2", "P3") for ek in ("E_lo", "E_mid", "E_hi"))
        det = any(TABLE[f"{foot}|{pk}|{ek}"]["dchi2_Newton"] > 3.84 for pk in ("P1", "P2", "P3") for ek in ("E_lo", "E_mid", "E_hi"))
        VER[foot] = dict(central=cen, band=[lo, hi], window=win, move=mv, CFG820=ref, AQUAL_excluded_all_cells=aq, Newton_excluded_any_cell=det)
        P(f"   V1 [{foot}] L*_95 central {cen:.2f} pc; band {lo:.2f} - {hi:.2f} pc (P1-P3 x E_lo/E_mid/E_hi, f_b 0.3, E-P)")
        P(f"   V2 [{foot}] window [20, 90] pc: {win}")
        P(f"   V3 [{foot}] {mv} (CFG820 {ref}; ratio {cen / ref:.3f})")
        P(f"   V4 [{foot}] AQUAL excluded in every cell: {aq}; Newton excluded in any cell (detection/upper bound): {det}")
    R["verdict"] = VER

rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
check("K10", rss < 1.0, f"{rss:.3f} GB", "< 1 GB", "peak RSS")
npass = sum(CHK[k]["ok"] for k in CHK); ntot = len(CHK)
undecided = any(not CHK[k]["ok"] for k in ("K2", "K3", "K4", "K5", "K6") if k in CHK)
R["checks"] = CHK; R["undecided"] = undecided; R["runtime_s"] = time.time() - T0
P(f"\nD10_NATIVE_LSTAR COMPLETE: {npass}/{ntot} checks PASS." + ("  (UNDECIDED: a validation check failed)" if undecided else "") + f"  {time.time() - T0:.0f} s")
json.dump(R, open(os.path.join(HERE, f"d10_native_lstar_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"d10_native_lstar{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == ntot else 1)

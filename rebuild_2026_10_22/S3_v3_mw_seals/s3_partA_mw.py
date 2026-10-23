#!/usr/bin/env python3
"""S3_v3_mw_seals Part A: the Milky Way's outer rotation slope under v3 (tile 25).

Criteria: FROZEN_CRITERIA.md (8f6c6587e1) + AMENDMENTS A1 (0501ac4248), A2.  Path, one ingredient at a time, both footings:
0 OLD (CFG532b RM-v / RM-phi, read) -> 1 ALG nu_mono (my Newtonian field; reproduction) -> 2 ALG nu1 (kernel) -> 3 AQUAL nu1
isolated (geometry) -> 4 AQUAL + EFE (h81 e_N, gamma 57 deg, anticentre wedge; the v3 cell) -> 5 screening -> 6 mu_K^2 bound.
Labels: CFG532/532b frozen rules.  Run: OMP_NUM_THREADS=1 nice -n 15 python3 s3_partA_mw.py [--mutate]
kappa = 1/2 FITTED; footings never pooled; no dark-matter particle; not theory closed.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, io, contextlib, itertools, time, resource
import numpy as np
from scipy.stats import chi2 as chi2dist
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import s3_aqual as S
import s3_mw as MWm

REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CFGD = os.path.join(REPO, "campaign_fresh_gravity")
DATA = os.path.join(REPO, "real_research", "data")
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
SRCDIR = os.path.join(EXT, "cfg532_work", "src")
TAG = S.TAG
FOOTS = S.FOOTS
OUT, CHECKS = [], []
T0 = time.time()


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True); OUT.append(s)


def check(name, ok, detail=""):
    CHECKS.append(dict(name=name, ok=bool(ok), detail=detail))
    P(f"{name} {'PASS' if ok else 'FAIL'} {detail}")
    return bool(ok)


def rss():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6


P("=" * 112)
P(f"S3 Part A: MW outer rotation slope under v3 {'*** MUTATE: mu == 1 (Newton) ***' if S.MUTATE else ''}")
P("kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; census baryons held; not theory closed")
P("=" * 112)

# ------------------------------------------------------------------ data (my loader, CFG532/532b files and line ranges)
def load_tsv(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith("#")]
    hdr = rows[0]; arr = np.array([[float(x) for x in r] for r in rows[1:]])
    return {h: arr[:, i] for i, h in enumerate(hdr)}


def parse_tex(relpath, l0, l1):
    lines = open(os.path.join(SRCDIR, relpath)).read().split("\n")
    rows = []
    for i in range(l0 - 1, l1):
        t = lines[i].split("%")[0].replace("\\\\", "").replace("\\hline", "")
        cells = [c.strip() for c in t.split("&")]
        if len(cells) < 3:
            continue
        try:
            rows.append([float(c) for c in cells[:3]])
        except ValueError:
            continue
    a = np.array(rows)
    return a[:, 0], a[:, 1], a[:, 2]


ou = load_tsv(os.path.join(DATA, "mw_rc_ou2024_table1.tsv"))
el = load_tsv(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv"))
CUR = {}
r_, v_, s_ = ou["R_kpc"], ou["vc_kms"], 0.5 * (ou["sig_plus"] + ou["sig_minus"])
CUR["Ou24"] = dict(R=r_, V=v_, E=np.hypot(s_, np.where(r_ <= 22.0, 0.03, 0.15) * v_), cls="RGB", grp="APO", nexp=37)
r_, v_, s_ = el["R_kpc"], el["vc_kms"], 0.5 * (el["sig_plus"] + el["sig_minus"])
CUR["Eilers19"] = dict(R=r_, V=v_, E=np.hypot(s_, 0.03 * v_), cls="RGB", grp="APO", nexp=38)
TEX = {"Wang23": ("2211.05668/HFW-3DRC-v1.tex", 777, 802, "stat", "LIM", 19),
       "Jiao23": ("2309.00048/rc_mw_z3.tex", 4, 27, "pub", "LIM", 18),
       "Zhou23": ("2212.10393/GRC.tex", 447, 488, "stat", "APO", 34),
       "SL23_DR3plus": ("2302.01379/ms.tex", 284, 335, "pub", "LIM", 45),
       "Feng26_Cepheids": ("2512.21780/Main.tex", 233, 252, "stat", "CEP", 12)}
for k, (f, l0, l1, et, grp, nexp) in TEX.items():
    R, V, Sg = parse_tex(f, l0, l1)
    CUR[k] = dict(R=R, V=V, E=(np.hypot(Sg, 0.03 * V) if et == "stat" else Sg.copy()), cls=("CEP" if grp == "CEP" else "RGB"),
                  grp=grp, nexp=nexp, report_only=(k == "SL23_DR3plus"))


def window(c):
    return (10.0, float(c["R"].max())) if c["cls"] == "CEP" else (15.0, 27.5)


def slope(R, V, E, lo, hi):
    m = (R >= lo) & (R <= hi)
    x, y, w = np.log(R[m]), np.log(V[m]), (V[m] / E[m]) ** 2
    A = np.vstack([np.ones_like(x), x]).T
    C = np.linalg.inv(A.T @ (A * w[:, None]))
    beta = C @ (A.T @ (w * y))
    return float(beta[1]), float(math.sqrt(C[1, 1])), int(m.sum())


J532 = json.load(open(os.path.join(CFGD, "CFG532_mw_gaia_rotation_curves", "cfg532_results.json")))
J532b = json.load(open(os.path.join(CFGD, "CFG532_mw_gaia_rotation_curves", "cfg532b_results.json")))
P("\n--- controls on data and the estimator")
Rt = np.linspace(15, 27.5, 12)
bk = slope(Rt, 200 * (Rt / 15) ** -0.5, np.full(12, 5.0), 15, 27.5)[0]; bf = slope(Rt, np.full(12, 200.0), np.full(12, 5.0), 15, 27.5)[0]
check("A6", abs(bk + 0.5) < 1e-6 and abs(bf) < 1e-6, f"slope estimator Kepler {bk:+.7f} flat {bf:+.7f} (tol 1e-6)")
ref_bd = {k: J532b["combined"]["RGB_LIM"]["canonical|RMv"]["per_curve"][k]["b_data"] for k in ("Ou24", "Eilers19", "Zhou23", "Jiao23", "Wang23")}
ref_bd["SL23_DR3plus"] = J532b["cells"]["SL23_DR3plus|canonical|ALG"]["slope_data"]
ref_bd["Feng26_Cepheids"] = J532b["cells"]["Feng26_Cepheids|canonical|ALG"]["slope_data"]
worst, nbad = 0.0, 0
for k, c in CUR.items():
    lo, hi = window(c)
    b = slope(c["R"], c["V"], c["E"], lo, hi)[0]
    c["b_data"], c["b_err"], c["n_win"] = slope(c["R"], c["V"], c["E"], lo, hi)
    worst = max(worst, abs(b - ref_bd[k])); nbad += int(len(c["R"]) != c["nexp"])
check("A1", worst < 1e-9 and nbad == 0, f"row counts {[len(c['R']) for c in CUR.values()]} (all as tables); data slopes vs CFG532b max |d| {worst:.1e} (tol 1e-9)")

# ------------------------------------------------------------------ MW model and solves
P("\n--- Milky Way model (McMillan17 B1; my grid)")
mw = MWm.MW()
g = mw.g
P(f"  grid {g.describe()}; stars {mw.Ms:.4e} gas {mw.Mg:.4e} Msun (census stars {MWm.MSTAR_CENSUS:.2e} +- {MWm.MSTAR_ERR:.2e})")

# A2(i) Freeman on the MW grid
rhoF = np.zeros((g.nR, g.nz)); Rd, MF = 2.5, 4e10
Menc = MF * (1 - (1 + g.Re / Rd) * np.exp(-g.Re / Rd)); SigF = np.diff(Menc) / (math.pi * (g.Re[1:] ** 2 - g.Re[:-1] ** 2))
rhoF[:, g.jc] = SigF / g.dz[g.jc]
PhiF = g.newton(rhoF, S.bc_newton(g, S.total_mass(g, rhoF)))
Rf = np.linspace(0.5 * Rd, 15 * Rd, 60)
eF = float(np.max(np.abs(g.vc2(PhiF, Rf) / S.freeman_v2(MF, Rd, Rf) - 1)))
check("A2i", eF <= 0.005, f"razor-thin Freeman on the MW grid max |dV2/V2| {eF:.4f} on 0.5-15 R_d (tol 0.005)")

# CFG532 executed read-only (in a child process, to keep this process's peak RSS low) for A2(ii) and the transcription identity
CHILD = r"""
import os, sys, io, json, contextlib, resource
import numpy as np
sys.path.insert(0, %r)
import s3_mw as MWm
CFGD = %r
src = open(os.path.join(CFGD, "CFG532_mw_gaia_rotation_curves", "cfg532_mw_curves.py")).read()
head = src.split("RES = dict(mutate=MUTATE")[0]
ns = {"__file__": os.path.join(CFGD, "CFG532_mw_gaia_rotation_curves", "cfg532_mw_curves.py"), "__name__": "cfg532_import"}
os.environ["CFG532_MUTATE"] = "0"
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(head, "cfg532_head", "exec"), ns)
rng = np.random.default_rng(1)
Rq, zq = rng.uniform(0.01, 40, 400), rng.uniform(-3, 3, 400)
tr = max(float(np.max(np.abs(ns["rho_mcm"](Rq, zq) / MWm.rho_mcm(Rq, zq) - 1))),
         float(np.max(np.abs(ns["rho_b2"](Rq, zq, 7.3e10) / MWm.rho_b2(Rq, zq, 7.3e10) - 1))),
         float(np.max(np.abs(ns["ns"]["rho_b3"](Rq, zq) / MWm.rho_b3(Rq, zq) - 1))))
mixN, keyN = ns["b1mix"](1.0)
Rcmp = np.linspace(5.0, 27.5, 46)
vN = ns["v_model"]("N", mixN, keyN, "canonical", Rcmp)
print("@@" + json.dumps(dict(tr=tr, vN=[float(x) for x in vN], rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6)))
""" % (HERE, CFGD)
import subprocess
_out = subprocess.run([sys.executable, "-c", CHILD], capture_output=True, text=True, check=True,
                      env=dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")).stdout
_c = json.loads([ln for ln in _out.splitlines() if ln.startswith("@@")][-1][2:])
tr = _c["tr"]
P(f"  transcription of McMillan17 / B2 / B3 densities vs CFG514/516 functions: max rel diff {tr:.1e} (child peak RSS {_c['rss']:.0f} MB)")
Rcmp = np.linspace(5.0, 27.5, 46)
vN_532 = np.array(_c["vN"])
vN_me = np.sqrt(Rcmp * mw.gN_plane(1.0, Rcmp))
e2 = float(np.max(np.abs(vN_me / vN_532 - 1)))
check("A2ii", e2 <= 0.01 and tr < 1e-12, f"B1 in-plane Newtonian V vs CFG532 v_model('N') max |dV/V| {e2:.4f} on 5-27.5 kpc (tol 0.01); density transcription {tr:.1e}")

# ------------------------------------------------------------------ AQUAL solves (cached)
P("\n--- AQUAL solves (isolated and EFE along the axis, gamma = 0) over the s grid")
cells = [(f, s_, e) for f in FOOTS for s_ in MWm.S_GRID for e in (0.0, MWm.EN_H81[f])] + [(f, 1.0, 2 * MWm.EN_H81[f]) for f in FOOTS]
nrun, cpeak = MWm.presolve(mw, MWm.GRID_MAIN, "main", cells, batch=4)
P(f"  presolved {nrun} in child processes (batches of 4; child peak RSS {cpeak:.0f} MB)")
RES_RSS = dict(child_presolve_main=cpeak)
INFO = {}
for foot in FOOTS:
    for s in MWm.S_GRID:
        for eN in (0.0, MWm.EN_H81[foot]):
            Phi, info, PB, ge = mw.solve(foot, s, eN)
            INFO[f"{foot}|{s:.5f}|{eN}"] = info
    for eN in (2 * MWm.EN_H81[foot],):
        mw.solve(foot, 1.0, eN)
nfloor = sum(1 for v in INFO.values() if v["floor"])
maxres = max(v["residual"] for v in INFO.values())
P(f"  {len(INFO)} solves; max residual {maxres:.1e}; {nfloor} at the round-off floor (A2); RSS {rss():.0f} MB; {time.time() - T0:.0f} s")
check("A4v", all(v["residual"] <= 1e-8 or (v["floor"] and v["residual"] <= 1e-7) for v in INFO.values()),
      f"nonlinear residual max {maxres:.1e} (<= 1e-8, or the A2 round-off floor <= 1e-7: {nfloor} solves)")


def gAQ(foot, s, eN, R):
    Phi, info, PB, ge = mw.solve(foot, s, eN)
    return g.gR_plane(Phi, R)


SG = np.array(MWm.S_GRID)
LSG = np.log(SG)


def C_of(foot, eN, R):
    """C(R; s) table over S_GRID: AQUAL / nu1-algebraic on the same grid."""
    a0 = S.A0[foot]
    tab = []
    for s in SG:
        gN = mw.gN_plane(s, R)
        tab.append(gAQ(foot, s, eN, R) / (S.nu1(gN / a0) * gN))
    return np.array(tab)


_CT = {}


def C_interp(foot, eN, R, s):
    key = (foot, eN, tuple(np.round(np.atleast_1d(R), 9)))
    if key not in _CT:
        _CT[key] = C_of(foot, eN, np.atleast_1d(R))
    tab = _CT[key]
    ls = math.log(min(max(s, SG[0]), SG[-1]))
    j = int(np.clip(np.searchsorted(LSG, ls) - 1, 0, len(SG) - 2))
    t = (ls - LSG[j]) / (LSG[j + 1] - LSG[j])
    return (1 - t) * tab[j] + t * tab[j + 1]


# ------------------------------------------------------------------ 3-D EFE ratios
P("\n--- 3-D EFE (periodic FFT, box 640 kpc): gamma = 57 deg vs gamma = 0, N = 128 and 160")
R3D, PH = MWm.R3D, MWm.PH3D
WEDGE = MWm.anticentre_mask(PH)
TD = {}
for foot in FOOTS:
    for eN in (MWm.EN_H81[foot], 2 * MWm.EN_H81[foot]):
        for gam in (0.0, MWm.GAMMA_DEG):
            for N in ((128, 160) if eN == MWm.EN_H81[foot] else (160,)):
                TD[(foot, eN, gam, N)] = MWm.run_3d(mw, foot, eN, gam, N)
                d = TD[(foot, eN, gam, N)]
                P(f"  {foot:<9} eN {eN:.5f} gamma {gam:4.1f} N {N}: iters {d['iters']} converged {d['converged']} ; RSS {rss():.0f} MB")


def W_of(foot, eN, which, N=160):
    """V^2 ratio (3-D gamma 57 [wedge|mean] or gamma 0 [mean]) / 3-D gamma 0 mean, on R3D."""
    d57, d0 = np.array(TD[(foot, eN, MWm.GAMMA_DEG, N)]["FR"]), np.array(TD[(foot, eN, 0.0, N)]["FR"])
    base = d0.mean(axis=1)
    if which == "wedge":
        return d57[:, WEDGE].mean(axis=1) / base
    if which == "mean":
        return d57.mean(axis=1) / base
    raise ValueError(which)


def W_at(foot, eN, which, R, N=160):
    w = W_of(foot, eN, which, N)
    return np.interp(np.log(np.asarray(R, float)), np.log(R3D), w, left=w[0], right=w[-1])


# checks A5
d5i, d5ii, d5iii = 0.0, 0.0, 0.0
sel = (R3D >= 15) & (R3D <= 60)
for foot in FOOTS:
    eN = MWm.EN_H81[foot]
    for which in ("wedge", "mean"):
        d5i = max(d5i, float(np.max(np.abs(W_of(foot, eN, which, 160)[sel] / W_of(foot, eN, which, 128)[sel] - 1))))
    d0 = np.array(TD[(foot, eN, 0.0, 160)]["FR"])
    ax = gAQ(foot, 1.0, eN, R3D)
    d5ii = max(d5ii, float(np.max(np.abs(d0.mean(axis=1)[sel] / ax[sel] - 1))))
    d5iii = max(d5iii, float(np.max((d0.max(axis=1) - d0.min(axis=1))[sel] / d0.mean(axis=1)[sel])))
check("A5i", d5i <= 0.005, f"3-D ratio N 128 vs 160 max change {d5i:.4f} on 15-60 kpc (tol 0.005)")
check("A5ii", d5ii <= 0.03, f"3-D gamma 0 azimuthal mean vs axisymmetric gamma 0 max |d| {d5ii:.4f} on 15-60 kpc (tol 0.03)")
check("A5iii", d5iii <= 0.003, f"3-D gamma 0 azimuthal variation max {d5iii:.4f} on 15-60 kpc (tol 0.003)")

# ------------------------------------------------------------------ models along the path
STEPS = ["ALG_numono", "ALG_nu1", "AQ_iso", "AQ_gamma0", "AQ_gamma0_2x", "AQ_v3", "AQ_v3_mean", "AQ_v3_2x"]


def vmodel(step, foot, R, s=1.0):
    R = np.asarray(R, float)
    a0 = S.A0[foot]
    gN = mw.gN_plane(s, R)
    if step == "N":
        return np.sqrt(np.maximum(R * gN, 0))
    if step == "ALG_numono":
        return np.sqrt(R * S.nu_mono(gN / a0) * gN)
    alg1 = S.nu1(gN / a0) * gN
    if step == "ALG_nu1":
        return np.sqrt(R * alg1)
    if step == "AQ_iso":
        return np.sqrt(R * alg1 * C_interp(foot, 0.0, R, s))
    eN = MWm.EN_H81[foot]
    if step == "AQ_gamma0":
        return np.sqrt(R * alg1 * C_interp(foot, eN, R, s))
    if step == "AQ_gamma0_2x":
        Phi, info, PB, ge = mw.solve(foot, 1.0, 2 * eN)
        Cx = g.gR_plane(Phi, R) / alg1 if abs(s - 1) < 1e-12 else C_interp(foot, eN, R, s)  # 2x only at s = 1 (s* uses h81's C)
        return np.sqrt(R * alg1 * Cx)
    if step == "AQ_v3":
        return np.sqrt(R * alg1 * C_interp(foot, eN, R, s) * W_at(foot, eN, "wedge", R))
    if step == "AQ_v3_mean":
        return np.sqrt(R * alg1 * C_interp(foot, eN, R, s) * W_at(foot, eN, "mean", R))
    if step == "AQ_v3_2x":
        e2x = 2 * eN
        Phi, info, PB, ge = mw.solve(foot, 1.0, e2x)
        Cx = g.gR_plane(Phi, R) / alg1 if abs(s - 1) < 1e-12 else C_interp(foot, eN, R, s)  # 2x only at s = 1 (s* uses h81's C)
        return np.sqrt(R * alg1 * Cx * W_at(foot, e2x, "wedge", R))
    raise ValueError(step)


def chi2(v, c):
    return float(np.sum(((v - c["V"]) / c["E"]) ** 2))


def pval(x, dof):
    return float(chi2dist.sf(x, max(dof, 1)))


def score(step, foot, c):
    lo, hi = window(c)
    N = len(c["R"])
    bd, sb = c["b_data"], c["b_err"]
    v0 = vmodel(step, foot, c["R"])
    c0 = chi2(v0, c); p0 = pval(c0, N)
    b0 = slope(c["R"], v0, c["E"], lo, hi)[0]
    out = dict(N=N, chi2_census=c0, p_census=p0, slope_data=bd, slope_err=sb, slope_census=b0,
               dslope_census_sig=(bd - b0) / sb, V20_census=float(vmodel(step, foot, np.array([20.0]))[0]))
    f = lambda s: chi2(vmodel(step, foot, c["R"], s), c)
    fr = minimize_scalar(f, bounds=(0.25, 4.0), method="bounded", options=dict(xatol=1e-3))
    s_ = float(fr.x); cs = float(fr.fun)
    bs = slope(c["R"], vmodel(step, foot, c["R"], s_), c["E"], lo, hi)[0]
    Mneed = s_ * MWm.MSTAR_CENSUS
    out.update(s_star=s_, chi2_s=cs, p_s=pval(cs, N - 1), Mstar_need=Mneed, z_need=(Mneed - MWm.MSTAR_CENSUS) / MWm.MSTAR_ERR,
               slope_s=bs, dslope_s_sig=(bd - bs) / sb, at_bound=bool(s_ < 0.26 or s_ > 3.99))
    shape_nd = bool(2 * sb > abs(b0 + 0.5))
    if p0 >= 0.01 and abs(out["dslope_census_sig"]) <= 2:
        v = "NOT DIAGNOSTIC" if shape_nd else "CONSISTENT"
    elif s_ > 1 and out["p_s"] >= 0.01 and abs(out["dslope_s_sig"]) <= 2 and not out["at_bound"]:
        v = "NEEDS-HEAVY-DISC"
    else:
        v = "EXCLUDED"
    out.update(shape_not_diagnostic=shape_nd, verdict=v)
    return out


def combine(ds, ss, rho):
    ds, ss = np.asarray(ds), np.asarray(ss)
    C = np.diag(ss ** 2)
    for i, j in itertools.combinations(range(len(ds)), 2):
        C[i, j] = C[j, i] = rho * ss[i] * ss[j]
    Ci = np.linalg.inv(C); one = np.ones(len(ds))
    var = 1.0 / (one @ Ci @ one); mean = var * (one @ Ci @ ds)
    return float(mean), float(math.sqrt(var))


def class_verdict(Z, sbar, bl):
    if sbar > abs(bl + 0.5) / 2:
        return "NOT DIAGNOSTIC"
    return "SHAPE CONSISTENT" if abs(Z) <= 2 else ("SHAPE TENSION" if abs(Z) <= 3 else "SHAPE EXCLUDED")


APO, LIM = ["Ou24", "Eilers19", "Zhou23"], ["Jiao23", "Wang23"]


def delta(step, foot, c):
    lo, hi = window(c)
    bl = slope(c["R"], vmodel(step, foot, c["R"]), c["E"], lo, hi)[0]
    return c["b_data"] - bl, c["b_err"], bl


def run_combined(step, foot, curves=CUR):
    d = {k: delta(step, foot, curves[k]) for k in APO + LIM}
    rows = {}
    for a, b in itertools.product(APO, LIM):
        for rho in (0.0, 0.5):
            m, s_ = combine([d[a][0], d[b][0]], [d[a][1], d[b][1]], rho)
            bl = 0.5 * (d[a][2] + d[b][2])
            rows[f"{a}+{b}|rho{rho}"] = dict(mean=m, sig=s_, Z=m / s_, verdict=class_verdict(m / s_, s_, bl))
    Zs = [r["Z"] for r in rows.values()]
    return dict(per_curve={k: dict(delta=v[0], sig=v[1], b_law=v[2], Z=v[0] / v[1]) for k, v in d.items()}, pairs=rows,
                primary=rows["Ou24+Jiao23|rho0.0"], primary_rho05=rows["Ou24+Jiao23|rho0.5"], Z_range=[min(Zs), max(Zs)])


RES = dict(lane="S3_v3_mw_seals", part="A", mutate=S.MUTATE, criteria="8f6c6587e1", amendments=["A1 0501ac4248", "A2"],
           grid=g.describe(), baryons=dict(stars=mw.Ms, gas=mw.Mg), e_N_h81=MWm.EN_H81, gamma_deg=MWm.GAMMA_DEG, steps={})

# ------------------------------------------------------------------ A3 reproduction (ALG nu_mono vs CFG532/532b ALG cells)
P("\n--- A3: ALG nu_mono on my Newtonian field vs the record's ALG cells")
w_s, w_c = 0.0, 0.0
for foot in FOOTS:
    for k in ("Ou24", "Eilers19", "Wang23", "Jiao23", "Zhou23", "SL23_DR3plus", "Feng26_Cepheids"):
        if k in ("Ou24", "Eilers19"):
            ref = J532["cells"][f"{'C1_Ou24' if k == 'Ou24' else 'C2_Eilers19'}|{foot}|ALG"]
        else:
            ref = J532b["cells"][f"{k}|{foot}|ALG"]
        c = CUR[k]; lo, hi = window(c)
        v = vmodel("ALG_numono", foot, c["R"])
        b = slope(c["R"], v, c["E"], lo, hi)[0]; x2 = chi2(v, c)
        w_s = max(w_s, abs(b - ref["slope_census"])); w_c = max(w_c, abs(x2 / ref["chi2_census"] - 1))
        P(f"  {foot:<9} {k:<16} slope {b:+.4f} (record {ref['slope_census']:+.4f})  chi2 {x2:8.2f} (record {ref['chi2_census']:8.2f})")
check("A3", w_s <= 0.003 and w_c <= 0.03, f"ALG nu_mono law slope max |d| {w_s:.4f} (tol 0.003), chi2 max rel {w_c:.4f} (tol 0.03)")

# ------------------------------------------------------------------ the path
P("\n--- per-curve cells (census held; s* post hoc) and the combined RGB/LIM slope test, step by step")
for step in STEPS:
    RES["steps"][step] = {}
    for foot in FOOTS:
        cells = {k: score(step, foot, c) for k, c in CUR.items()}
        comb = run_combined(step, foot)
        cep = delta(step, foot, CUR["Feng26_Cepheids"])
        Zc = cep[0] / cep[1]
        RES["steps"][step][foot] = dict(cells=cells, combined=comb,
                                        cepheid=dict(delta=cep[0], sig=cep[1], b_law=cep[2], Z=Zc, verdict=class_verdict(Zc, cep[1], cep[2])))
        pr, p5 = comb["primary"], comb["primary_rho05"]
        P(f"  {step:<11} {foot:<9} V20 {cells['Ou24']['V20_census']:6.1f} | law slope Ou {cells['Ou24']['slope_census']:+.3f} Jiao {cells['Jiao23']['slope_census']:+.3f} | "
          f"primary Ou+Jiao D {pr['mean']:+.3f}+-{pr['sig']:.3f} Z {pr['Z']:+.2f} {pr['verdict']}; rho0.5 Z {p5['Z']:+.2f}; pairs {comb['Z_range'][0]:+.2f}..{comb['Z_range'][1]:+.2f}"
          f" | Cepheid Z {Zc:+.2f}")
    for foot in FOOTS:
        for k, o in RES["steps"][step][foot]["cells"].items():
            P(f"      {foot:<9} {k:<16} chi2 {o['chi2_census']:7.1f}/{o['N']} p {o['p_census']:.1e} | M*need {o['Mstar_need']:.2e} (z {o['z_need']:+.1f}) | "
              f"slope data {o['slope_data']:+.3f}+-{o['slope_err']:.3f} law {o['slope_census']:+.3f} ({o['dslope_census_sig']:+.1f}sig) -> {o['verdict']}"
              + ("  (REPORTED ONLY)" if CUR[k].get("report_only") else ""))

P("\n--- step 0 (OLD, read from cfg532b_results.json)")
RES["step0_old"] = {}
for foot in FOOTS:
    for kind in ("RMv", "RMphi"):
        o = J532b["combined"]["RGB_LIM"][f"{foot}|{kind}"]
        RES["step0_old"][f"{foot}|{kind}"] = dict(primary=o["primary"], primary_rho05=o["primary_rho05"], Z_range=o["Z_range"],
                                                  b_law_Ou=o["per_curve"]["Ou24"]["b_law"], b_law_Jiao=o["per_curve"]["Jiao23"]["b_law"])
        P(f"  {kind:<5} {foot:<9} law slope Ou {o['per_curve']['Ou24']['b_law']:+.3f} | primary Z {o['primary']['Z']:+.2f} {o['primary']['verdict']}; rho0.5 Z {o['primary_rho05']['Z']:+.2f}")

# A7 (law on)
v20 = {f: RES["steps"]["AQ_v3"][f]["cells"]["Ou24"]["V20_census"] for f in FOOTS}
check("A7", all(v >= 170.0 for v in v20.values()), f"v3 V(20 kpc) {v20['canonical']:.1f} / {v20['alt']:.1f} km/s (>= 170)")

# ------------------------------------------------------------------ steps 5, 6 and the A4(iv) grid refinement
P("\n--- step 5 screening: l_g = L*^2/(2 r_M)")
RES["screening"] = {}
for foot in FOOTS:
    rM = math.sqrt(S.G * (mw.Ms + mw.Mg) / S.A0[foot])
    RES["screening"][foot] = dict(r_M_kpc=rM, l_g_pc={str(L): MWm.l_g_pc(L, rM) for L in MWm.LSTARS_PC})
    P(f"  {foot:<9} r_M {rM:.2f} kpc; l_g = " + ", ".join(f"{MWm.l_g_pc(L, rM):.4f} pc (L* {L})" for L in MWm.LSTARS_PC) +
      " -> unscreened at every radius used (>= 5 kpc)")

P("\n--- step 6 mu_K^2 bound (reported only; R6 owns the term): delta rho = mu_K^2 |psi_int| / (4 pi G), EFE zero point")
muK = MWm.MU_K_HMPC * MWm.H_LITTLE / 1000.0
RES["muK_bound"] = {}
for foot in FOOTS:
    eN = MWm.EN_H81[foot]
    Phi, info, PB, ge = mw.solve(foot, 1.0, eN)
    drho = muK ** 2 * np.abs(Phi) / (4 * math.pi * S.G)
    rc = np.hypot(g.RR, g.ZZ)
    Rb = np.array([15.0, 20.0, 27.5])
    dM = np.array([2 * math.pi * float(np.sum((drho * g.V)[rc < r])) for r in Rb])
    a0 = S.A0[foot]
    gN = mw.gN_plane(1.0, Rb); y = gN / a0
    dy = 1e-6
    dgdgN = ((S.nu1(y * (1 + dy)) * y * (1 + dy)) - S.nu1(y) * y) / (y * dy)
    v2 = vmodel("AQ_v3", foot, Rb) ** 2
    dv2 = Rb * dgdgN * S.G * dM / Rb ** 2
    frac = dv2 / v2
    dsl = 0.5 * (math.log(1 + frac[2]) - math.log(1 + frac[0])) / math.log(27.5 / 15.0)
    RES["muK_bound"][foot] = dict(mu_K_per_kpc=muK, dM=dM.tolist(), dV2_over_V2=frac.tolist(), dslope=dsl)
    P(f"  {foot:<9} mu_K {muK:.5f}/kpc: delta M(<15, 20, 27.5) {dM[0]:.2e} {dM[1]:.2e} {dM[2]:.2e} Msun; dV2/V2 {frac[0]:+.3f} {frac[1]:+.3f} {frac[2]:+.3f}; slope shift {dsl:+.3f}")

P("\n--- A4(iv): grid refinement at s = 1 (isolated and EFE)")
cells_f = [(f, 1.0, e) for f in FOOTS for e in (0.0, MWm.EN_H81[f])]
nrun, cpeak = MWm.presolve(None, MWm.GRID_FINE, "fine", cells_f, batch=1)
RES_RSS["child_presolve_fine"] = cpeak
P(f"  fine grid: presolved {nrun} in child processes (child peak RSS {cpeak:.0f} MB)")
a4iv, pk = S.run_batch("s3_mw", "job_A4iv", [dict()], batch=1)
RES_RSS["A4iv"] = pk
dv, dsl = a4iv[0]["dv"], a4iv[0]["dsl"]
check("A4iv", dv <= 0.003 and dsl <= 0.003, f"main vs fine grid: V(15-27.5) max |d| {dv:.4f} (tol 0.003), slope |d| {dsl:.4f} (tol 0.003); fine grid {a4iv[0]['fine']['nR']}x{a4iv[0]['fine']['nz']}")

# ------------------------------------------------------------------ A4 (i)-(iii) solver controls (child processes)
P("\n--- A4 (i)-(iii) solver controls (child processes; true mu)")
a4, pk = S.run_batch("s3_mw", "job_A4", [dict(which="plummer_iso"), dict(which="plummer_efe"), dict(which="kuzmin")], batch=1)
RES_RSS["A4_controls"] = pk
eP, eE, kz = a4[0]["err"], a4[1]["err"], a4[2]
check("A4i", eP <= 0.003, f"Plummer isolated AQUAL vs nu1 algebraic max |d| {eP:.4f} on 0.3-30 b (tol 0.003); grid {a4[0].get('grid', {}).get('nR')}x{a4[0].get('grid', {}).get('nz')}")
check("A4iii", eE <= 0.01, f"EFE along z (y_e 0.1): equatorial g_R vs E2 aqual_axi point mass at r = 0.5, 1, 2, 4 r_M max |d| {eE:.4f} (tol 0.01)")
check("A4ii", kz["eK"] <= 0.005 and kz["eK2"] <= 0.005, f"Kuzmin (A1 form): in-plane vs nu1(|gN(0+)|) gN_R max |d| {kz['eK']:.4f}, off-plane |g| at z = 0.5a max |d| {kz['eK2']:.4f} (tol 0.005); "
      f"reported: in-plane AQUAL / in-plane algebraic at R = 0.3a {kz['alg_ratio']:+.4f}; child peak RSS {pk:.0f} MB")
RES["kuzmin_inplane_vs_alg_0p3a"] = kz["alg_ratio"]

# ------------------------------------------------------------------ the tile reading (AMENDMENT A3: A5 failed -> gamma 0 cell)
use3d = all(c["ok"] for c in CHECKS if c["name"].startswith("A5"))
PRIM_STEP = "AQ_v3" if use3d else "AQ_gamma0"
P(f"\n--- tile-25 reading for v3 (primary: {PRIM_STEP}, Ou+Jiao, rho 0){'' if use3d else '  [A5 failed: per s7 / AMENDMENT A3 the 3-D gamma 57 cells are reported only]'}")
RES["reading"] = {"primary_step": PRIM_STEP, "use3d": use3d}
for foot in FOOTS:
    lab = RES["steps"][PRIM_STEP][foot]["combined"]["primary"]["verdict"]
    alts = {"rho0.5": RES["steps"][PRIM_STEP][foot]["combined"]["primary_rho05"]["verdict"],
            "e_N 0 (isolated)": RES["steps"]["AQ_iso"][foot]["combined"]["primary"]["verdict"],
            "e_N 2 x h81": RES["steps"]["AQ_v3_2x" if use3d else "AQ_gamma0_2x"][foot]["combined"]["primary"]["verdict"]}
    if use3d:
        alts.update({"azimuthal mean": RES["steps"]["AQ_v3_mean"][foot]["combined"]["primary"]["verdict"],
                     "gamma 0": RES["steps"]["AQ_gamma0"][foot]["combined"]["primary"]["verdict"]})
    rep3d = {k: RES["steps"][k][foot]["combined"]["primary"]["verdict"] for k in ("AQ_v3", "AQ_v3_mean", "AQ_v3_2x")}
    rob = all(v == lab for v in alts.values())
    dep = [k for k, v in alts.items() if v != lab]
    RES["reading"][foot] = dict(label=lab, robust=rob, alternatives=alts, depends_on=dep, reported_3d=rep3d,
                                Z=RES["steps"][PRIM_STEP][foot]["combined"]["primary"]["Z"])
    P(f"  {foot:<9} v3: {lab} (Z {RES['reading'][foot]['Z']:+.2f}; {'ROBUST' if rob else 'depends on ' + ', '.join(dep)}); alternatives {alts}; 3-D cells (reported) {rep3d}")

if True:
    P("\n--- detection power (CFG532b's M3, reported): Keplerian tail injected beyond 15 kpc into every RGB/LIM curve, v3 cell")
    MUT3 = {}
    for k, c in CUR.items():
        if c["cls"] != "RGB":
            continue
        V15 = float(np.interp(15.0, c["R"], c["V"]))
        cc = dict(c); cc["V"] = np.where(c["R"] >= 15.0, V15 * (c["R"] / 15.0) ** -0.5, c["V"])
        lo, hi = window(cc); cc["b_data"], cc["b_err"], cc["n_win"] = slope(cc["R"], cc["V"], cc["E"], lo, hi)
        MUT3[k] = cc
    for foot in FOOTS:
        r3 = run_combined(PRIM_STEP, foot, MUT3)
        P(f"  {foot:<9} primary Z {r3['primary']['Z']:+.2f} -> {'DETECTED' if abs(r3['primary']['Z']) > 3 else 'not detected'}")
        RES.setdefault("M3_injection", {})[foot] = r3["primary"]

RES["checks"] = CHECKS
npass = sum(c["ok"] for c in CHECKS)
RES["runtime_s"] = round(time.time() - T0, 1)
RES["peak_rss_MB"] = round(rss(), 1)
RES["child_rss_MB"] = RES_RSS


def jdefault(o):
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


json.dump(RES, open(os.path.join(HERE, f"s3_partA_mw_results{TAG}.json"), "w"), indent=1, default=jdefault)
P(f"\nS3_PARTA COMPLETE: {npass}/{len(CHECKS)} checks PASS.  runtime {RES['runtime_s']} s, peak RSS {RES['peak_rss_MB']} MB")
open(os.path.join(HERE, f"s3_partA_mw{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)

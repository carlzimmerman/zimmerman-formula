#!/usr/bin/env python3
"""P4_v3_galaxy_tiles: the five galaxy-column tiles of the status board recomputed for v3.

v3 static weak field on baryons only: AQUAL with mu = x/(1+x) exactly; external field solved as a boundary condition;
screened by the C4-literal stiffness at L* = 24 and 90 pc (L* = 0 reported); no settling / supply / catchment / edge /
round rules; both footings (9.3603e-11, 1.1312e-10 m/s^2), never pooled.  Not included: BS24 Eq. 35's mu_K^2 psi term (R6).
Criteria: FROZEN_CRITERIA.md (6c5e6161b9, committed alone first).  kappa = 1/2 FITTED.  Not "theory closed".

Run:   OMP_NUM_THREADS=1 nice -n 15 python3 p4_v3_galaxy_tiles.py            -> .out, _results.json  (exit 0 iff all checks pass)
       OMP_NUM_THREADS=1 nice -n 15 python3 p4_v3_galaxy_tiles.py --mutate   -> _MUTATE.out, _results_MUTATE.json (validations
       only, mu swapped for the standard x/sqrt(1+x^2): K1/K2 must FAIL, exit 1)
Inputs are read only; nothing is downloaded.
"""
import os, sys, io, re, csv, json, math, time, contextlib, resource, importlib.util, warnings
import numpy as np
from scipy.stats import chi2 as CHI2
from scipy.optimize import minimize_scalar, least_squares

warnings.filterwarnings("ignore", category=RuntimeWarning)
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CFGD = os.path.join(REPO, "campaign_fresh_gravity")
DATA = os.path.join(REPO, "real_research", "data")
sys.path.insert(0, HERE)
import p4_solver as S  # noqa: E402

MUT = "--mutate" in sys.argv
TAG = "_MUTATE" if MUT else ""
ONLY = [t for t in os.environ.get("P4_ONLY", "").split(",") if t]      # development only; the committed run uses all
T0 = time.time()
OUTL, CHECKS = [], []
RES = dict(lane="P4_v3_galaxy_tiles", criteria="6c5e6161b9", mutate=MUT, checks={}, tiles={})
FOOTS = ("canonical", "alt")
LSTARS = (0.0, 24.0, 90.0)                                                 # pc; 0 = plain AQUAL (reported, not scored)
LN10 = math.log(10.0)


def P(s=""):
    print(s, flush=True); OUTL.append(str(s))


def check(key, ok, value, thr, detail=""):
    ok = bool(ok)
    CHECKS.append((key, ok))
    RES["checks"][key] = dict(ok=ok, value=value, threshold=thr, detail=detail)
    P(f"{key} {'PASS' if ok else 'FAIL'} {value} {thr}" + (f"   [{detail}]" if detail else ""))
    return ok


def want(t):
    return (not ONLY) or (t in ONLY)


with contextlib.redirect_stdout(io.StringIO()):
    sys.path.insert(0, CFGD)
    import CFG4_common as C4  # noqa: E402  (read only: FP0 a0, nu_mono, the record's SPARC loader for K5)
A0 = {f: float(C4.A0[f]) for f in FOOTS}
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
nu_mono = C4.nu_mono


def nu_e(y):
    y = np.maximum(np.asarray(y, float), 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def nu1(y):
    return S.nu1(y)


def rss_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9       # macOS: bytes


P(__doc__.strip())
P(f"\nfootings (FP0): canonical {A0['canonical']:.6e}, alt {A0['alt']:.6e} m/s^2;  L* bracket 24 / 90 pc;  mutate = {MUT}")


# =====================================================================================================================  validations
def plummer_problem(y, xe, Lam, nper=20, Nt=16, mutate=False, rmax=100.0):
    ro = S.r_out_for(y, xe, rmax)
    g = S.sphere_grid(1e-3, ro, nper=nper, Nt=Nt if xe > 0 else max(Nt // 4, 1))
    pr = S.Problem(g, g.rho_spherical(S.plummer_M(y, 1.0)), y, xe, Lam=Lam, mutate=mutate)
    pr.solve()
    return g, pr


P("\n=== VALIDATION")
k1 = 0.0
for y in (0.03, 1.0, 30.0):
    g, pr = plummer_problem(y, 0.0, 0.0, Nt=4, mutate=MUT)
    rf, mono, ring, gc = g.radial_profiles(pr.Phi)
    r = np.geomspace(0.1, 30, 40); gN = y * r / (1 + r * r) ** 1.5
    k1 = max(k1, float(np.max(np.abs(g.at_r(rf, mono, r) / (nu1(gN) * gN) - 1))))
check("K1", k1 <= 5e-3, f"{k1:.2e}", "<=5e-3", "isolated Plummer (y 0.03/1/30), sphere-averaged g vs nu1(gN) gN, r = 0.1-30 a")

y, xe = 1e-4, 0.3
g, pr = plummer_problem(y, xe, 0.0, mutate=False)
mue, Le = xe / (1 + xe), 1 / (1 + xe)
if MUT:
    g, pr = plummer_problem(y, xe, 0.0, mutate=True)
d = g.face_dr(pr.Phi); rf = g.re[1:-1]
k2 = 0.0
for r0 in (30.0, 100.0):
    i = int(np.searchsorted(rf, r0))
    for j in range(g.Nt):
        th = g.tc[j]; q = math.sqrt(math.sin(th) ** 2 + math.cos(th) ** 2 / (1 + Le))
        exact = y / (mue * math.sqrt(1 + Le)) / (rf[i] ** 2 * q)              # quasi-Newtonian point field, radial component
        k2 = max(k2, abs(d[i, j] / exact - 1))                                # the solver's unknown is the internal potential
check("K2", k2 <= 0.015, f"{k2:.2e}", "<=0.015", "linear EFE (y 1e-4, x_e 0.3): internal radial field at every theta vs the quasi-Newtonian "
      "solution 1/(mu_e sqrt(1+L_e) r^2 q(theta)), r = 30, 100 a")

spec = importlib.util.spec_from_file_location("d10_solver_ro", os.path.join(REPO, "doors_push_2026_10_22", "D10_native_Lstar", "d10_solver.py"))
D10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(D10)
k4 = 0.0; k4rows = {}
for Lam in ((0.0,) if MUT else (0.0, 0.2)):
    sv = D10.Solver2D(D10.Grid2D(), 0.5, 0.1, Lam); sv.solve()
    rfd, gmd = sv.field_monopole()
    g, pr = plummer_problem(0.5, 0.1, Lam, mutate=MUT)
    rf, mono, ring, gc = g.radial_profiles(pr.Phi)
    r = np.array([0.5, 1.0, 2.0, 4.0])
    a = np.interp(np.log(r), np.log(rfd), gmd); b = g.at_r(rf, mono, r)
    k4rows[str(Lam)] = dict(D10=a.tolist(), P4=b.tolist())
    k4 = max(k4, float(np.max(np.abs(b / a - 1))))
check("K4", k4 <= 0.01, f"{k4:.2e}", "<=0.01", "vs D10 Solver2D (record's independent screened solver), Plummer y 0.5, x_e 0.1, Lambda 0 / 0.2 a")
RES["validation"] = dict(K1=k1, K2=k2, K4=k4, K4_rows=k4rows)

if MUT:
    P(f"\nMUTATE (mu = x/sqrt(1+x^2) in the solver): validations only")
    npass = sum(ok for _, ok in CHECKS)
    P(f"P4_V3_GALAXY_TILES COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
    RES["runtime_s"] = time.time() - T0
    json.dump(RES, open(os.path.join(HERE, f"p4_v3_galaxy_tiles_results{TAG}.json"), "w"), indent=1, default=float)
    open(os.path.join(HERE, f"p4_v3_galaxy_tiles{TAG}.out"), "w").write("\n".join(OUTL).replace(REPO, "<repo>") + "\n")
    sys.exit(0 if npass == len(CHECKS) else 1)


def tile_class(passes):
    """passes: {(foot, Lstar): bool} for Lstar in (24, 90).  PASS all / FAIL none / COND split."""
    v = [passes[(f, L)] for f in FOOTS for L in (24.0, 90.0)]
    return "PASS" if all(v) else ("FAIL" if not any(v) else "COND")


# =====================================================================================================================  T1 SPARC
KPC_S = 3.0857e19                                       # CFG695's conversion constant (kept for the ladder)
UPS = np.round(np.arange(0.30, 1.2001, 0.01), 2)
NODES = np.array([0.30, 0.40, 0.50, 0.60, 0.75, 0.90, 1.05, 1.20])
GE_CHAE = 1.2e-10


def load_sparc_own():
    d_ = os.path.join(DATA, "sparc_data"); gal = []
    for f in sorted(os.listdir(d_)):
        if not f.endswith("_rotmod.dat"):
            continue
        try:
            d = np.genfromtxt(os.path.join(d_, f), comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        gal.append(dict(name=f.replace("_rotmod.dat", ""), R=d[:, 0], Vobs=d[:, 1], eV=d[:, 2], Vgas=d[:, 3], Vdisk=d[:, 4], Vbul=d[:, 5]))
    keys = ("T", "D", "eD", "fD", "Inc", "eInc", "L36", "eL36", "Reff", "SBeff", "Rdisk", "SBdisk", "MHI", "RHI", "Vflat", "eVflat", "Q")
    tab = {}
    for line in open(os.path.join(DATA, "SPARC_Lelli2016c.mrt")):
        tok = line.split()
        if len(tok) != 19:
            continue
        try:
            vals = [float(t) for t in tok[1:18]]
        except ValueError:
            continue
        row = dict(zip(keys, vals))
        for k in ("T", "fD", "Q"):
            row[k] = int(row[k])
        tab[tok[0]] = row
    for g_ in gal:
        g_["meta"] = tab.get(g_["name"])
    return gal


def gal_arrays(q, ups):
    """per galaxy: g_bar, g_obs (m/s^2) at Upsilon values ups (vector) -> (n_pts, n_ups); weights; mask."""
    R = q["R"] * KPC_S
    VB2 = np.sign(q["Vgas"])[:, None] * q["Vgas"][:, None] ** 2 + ups[None, :] * q["Vdisk"][:, None] ** 2 + 1.4 * ups[None, :] * q["Vbul"][:, None] ** 2
    GB = VB2 * 1e6 / R[:, None]
    GO = ((q["Vobs"] * 1e3) ** 2 / R)[:, None] * np.ones_like(GB)
    OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & np.isfinite(GO) & (q["Vobs"] > 0)[:, None]
    W = (1.0 / (np.clip(q["eV"], 1, None) / np.clip(q["Vobs"], 1, None)) ** 2)
    return GB, GO, OK, W


def chi2_offset(r, sig, s2):
    """r^T C^-1 r with C = diag(sig^2) + s2 11^T (Sherman-Morrison)."""
    w = 1.0 / sig ** 2
    a = np.sum(w * r * r, axis=0); b = np.sum(w * r, axis=0); c = np.sum(w, axis=0)
    return a - s2 * b * b / (1.0 + s2 * c)


def sparc_mass_fun(q, ups, a0):
    """spherical-approximation enclosed mass M(r) (G = a0 = 1, kpc) at one Upsilon."""
    R = q["R"]
    vb2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + ups * q["Vdisk"] ** 2 + 1.4 * ups * q["Vbul"] ** 2
    cfac = 1e6 / KPC_S / a0                                               # (km/s)^2/kpc -> a0
    Mk = cfac * vb2 * R
    def M(r):
        r = np.asarray(r, float)
        v = np.interp(r, R, vb2)
        out = cfac * v * r
        out = np.where(r < R[0], Mk[0] * (r / R[0]) ** 3, out)
        out = np.where(r > R[-1], Mk[-1], out)
        return out
    return M, float(Mk[-1])


def sparc_solve(q, ups, a0, ge, Lam_kpc, nper=20, Nt=16):
    """log10 g_pred (m/s^2) at the data radii: (mono, ring, great circle); spherical approximation, AQUAL / stiffened."""
    M, Mtot = sparc_mass_fun(q, ups, a0)
    R = q["R"]
    rats, objs = ratio_solve(M, max(Mtot, 1e-8), ge, Lam_kpc, R, R[-1], R[0] / 30.0, nper=nper, Nt=Nt)
    gN = M(R) / R ** 2
    galg = np.where(gN > 0, S.g_from_gN(np.abs(gN)), 1e-300)
    return [np.log10(np.maximum(galg * rt, 1e-300) * a0) for rt in rats], objs


def ratio_solve(Mfun, Mt, ge, Lam_kpc, r_eval, rmax, r_in, nper=20, Nt=16, align=True):
    """The solver's correction factors at radii r_eval: the solved internal radial field (sphere average, ring at theta = pi/2,
    great circle through the axis) divided by the isolated L* = 0 solve on the SAME radial grid (N_theta = 1); one radial face sits
    on the smallest evaluation radius (AMENDMENT A4).  A prediction is
    the exact isolated spherical law times this factor, so the grid's interpolation error cancels (AMENDMENT A2)."""
    re_ = S.log_edges(r_in, S.r_out_for(Mt, ge, rmax), nper, align=float(np.min(r_eval)) if align else None)
    gA = S.Grid(re_, S.theta_edges(Nt if ge > 0 else 1, full=True))
    prA = S.Problem(gA, gA.rho_spherical(Mfun), Mt, ge, Lam=Lam_kpc); prA.solve()
    rf, mono, ring, gc = gA.radial_profiles(prA.Phi)
    gB = S.Grid(re_, S.theta_edges(1, full=True))
    prB = S.Problem(gB, gB.rho_spherical(Mfun), Mt, 0.0); prB.solve()
    rfB, monoB, _, _ = gB.radial_profiles(prB.Phi)
    base = gB.at_r(rfB, monoB, r_eval)
    return [gA.at_r(rf, p_, r_eval) / base for p_ in (mono, ring, gc)], (gA, prA, gB, prB)


def virial_s2(g, pr):
    """orientation-averaged virial sigma^2 of the tracer = mass, internal field: (1/3M) sum rho V r dphi/dr."""
    return float(np.sum(pr.rho * g.vol * g.r2d * (g.Crr @ pr.Phi)) / (3 * np.sum(pr.rho * g.vol)))


def interp_nodes(lg_nodes):
    """lg_nodes: (n_nodes, n_pts) -> (n_pts, len(UPS)) linear in log Upsilon."""
    x = np.log(NODES); xf = np.log(UPS)
    out = np.empty((lg_nodes.shape[1], len(UPS)))
    for k in range(lg_nodes.shape[1]):
        out[k] = np.interp(xf, x, lg_nodes[:, k])
    return out


def fit_sample(GALS, LGP, prior=False):
    """LGP: {name: (n_pts, n_ups) log10 g_pred}.  Returns per-galaxy fits and pooled stats."""
    rows = []; num = den = 0.0
    for q in GALS:
        GB, GO, OK, W = gal_arrays(q, UPS)
        lgp = LGP[q["name"]]
        r = np.where(OK, np.log10(np.where(OK, GO, 1.0)) - lgp, 0.0)
        Wm = np.where(OK, W[:, None], 0.0)
        mse = (Wm * r * r).sum(0) / np.maximum(Wm.sum(0), 1e-300)
        sig = 2 * np.clip(q["eV"], 1, None) / (np.clip(q["Vobs"], 1, None) * LN10)
        m = q["meta"]; inc = math.radians(m["Inc"]); einc = math.radians(m["eInc"])
        s2 = (m["eD"] / (m["D"] * LN10)) ** 2 + (2 * einc / math.tan(inc) / LN10) ** 2
        sigm = np.where(OK, sig[:, None], 1e30)
        c2 = chi2_offset(np.where(OK, r, 0.0), sigm, s2)
        i_c2 = int(np.argmin(c2))
        if prior:   # Chae/CFG8 lognormal prior on the rms fit: eV-only chi2 = (ln10/2)^2 sum w r^2, plus ((log U - log 0.5)/0.1)^2
            i_rms = int(np.argmin((LN10 / 2) ** 2 * (Wm * r * r).sum(0) + ((np.log10(UPS) - math.log10(0.5)) / 0.1) ** 2))
        else:
            i_rms = int(np.argmin(mse))
        nok = int(OK[:, i_c2].sum())
        rows.append(dict(name=q["name"], U_rms=float(UPS[i_rms]), U_chi2=float(UPS[i_c2]), Q=m["Q"],
                         wsum=float(Wm[:, i_rms].sum()), wr2=float((Wm[:, i_rms] * r[:, i_rms] ** 2).sum()),
                         chi2=float(c2[i_c2]), n=nok, dof=max(nok - 1, 1), p=float(CHI2.sf(c2[i_c2], max(nok - 1, 1))),
                         wmean=float((Wm[:, i_rms] * r[:, i_rms]).sum() / max(Wm[:, i_rms].sum(), 1e-300)),
                         wsum_c=float(Wm[:, i_c2].sum()), wr2_c=float((Wm[:, i_c2] * r[:, i_c2] ** 2).sum())))
    return rows


def pooled(rows, sel=None):
    rr = [x for x in rows if (sel is None or sel(x))]
    rms = math.sqrt(sum(x["wr2"] for x in rr) / sum(x["wsum"] for x in rr))
    U = np.array([x["U_rms"] for x in rr])
    c2 = sum(x["chi2"] for x in rr); dof = sum(x["dof"] for x in rr)
    facc = float(np.mean([x["p"] >= 1e-3 for x in rr]))
    rmsB = math.sqrt(sum(x["wr2_c"] for x in rr) / sum(x["wsum_c"] for x in rr)); UB = np.array([x["U_chi2"] for x in rr])
    return dict(N=len(rr), rms=rms, U_median=float(np.median(U)), U_q=[float(v) for v in np.percentile(U, [16, 84])],
                readingB_Upsilon_from_cov_chi2=dict(rms=rmsB, U_median=float(np.median(UB))),
                chi2=c2, dof=dof, chi2nu=c2 / dof, frac_p_ok=facc, chi2nu_median=float(np.median([x["chi2"] / x["dof"] for x in rr])))


def t1_line(st):
    return bool(st["rms"] <= 0.110 and 0.50 <= st["U_median"] <= 0.80)


def chi2_label(f):
    return "PASS" if f >= 0.90 else ("MARGINAL" if f >= 0.75 else "FAIL")


if want("T1"):
    P("\n=== T1 ROTATION CURVES (SPARC RAR) under v3")
    GALS = load_sparc_own()
    with contextlib.redirect_stdout(io.StringIO()):
        REF = C4.load_sparc()
    same = len(REF) == len(GALS) and all(a["name"] == b["name"] and all(np.array_equal(a[k], b[k]) for k in ("R", "Vobs", "eV", "Vgas", "Vdisk", "Vbul"))
                                         and a["meta"] == b["meta"] for a, b in zip(GALS, REF))
    # CFG695 S2 reproduction (global Upsilon, algebraic simple law)
    R695 = json.load(open(os.path.join(CFGD, "CFG695_saturating_vacuum", "cfg695_results.json")))["numbers"]["S2"]
    Rm = np.concatenate([q["R"] for q in GALS]) * KPC_S
    Vo = np.concatenate([q["Vobs"] for q in GALS]); eV = np.concatenate([q["eV"] for q in GALS])
    Vg = np.concatenate([q["Vgas"] for q in GALS]); Vd = np.concatenate([q["Vdisk"] for q in GALS]); Vb = np.concatenate([q["Vbul"] for q in GALS])
    VB2 = np.sign(Vg)[:, None] * Vg[:, None] ** 2 + UPS[None, :] * Vd[:, None] ** 2 + 1.4 * UPS[None, :] * Vb[:, None] ** 2
    GBa = VB2 * 1e6 / Rm[:, None]; GOa = ((Vo * 1e3) ** 2 / Rm)[:, None] * np.ones_like(GBa)
    OKa = (GBa > 0) & (GOa > 0) & np.isfinite(GBa) & np.isfinite(GOa) & (Vo > 0)[:, None]
    WWa = np.where(OKa, (1.0 / (np.clip(eV, 1, None) / np.clip(Vo, 1, None)) ** 2)[:, None], 0.0)
    rep = {}
    for f in FOOTS:
        gb = np.where(OKa, GBa, 1.0)
        r_ = np.log10(np.where(OKa, GOa, 1.0)) - np.log10(np.where(OKa, nu1(gb / A0[f]) * gb, 1.0))
        mse = (WWa * r_ ** 2).sum(0) / WWa.sum(0); i = int(np.argmin(mse))
        rep[f] = dict(rms=math.sqrt(mse[i]), U=float(UPS[i]))
    dk5 = max(abs(rep[f]["rms"] - R695[f]["rms"]) for f in FOOTS); uk5 = all(rep[f]["U"] == R695[f]["U"] for f in FOOTS)
    check("K5", same and dk5 <= 1e-4 and uk5, f"loader_equal={same};max|drms|={dk5:.1e};U_equal={uk5}", "equal;<=1e-4;equal",
          f"CFG695 S2 reproduced: canonical {rep['canonical']['rms']:.4f}@{rep['canonical']['U']:.2f}, alt {rep['alt']['rms']:.4f}@{rep['alt']['U']:.2f}")
    # environment
    env = {r["galaxy"].strip(): r for r in csv.DictReader(open(os.path.join(REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv")))}
    names = {q["name"] for q in GALS}
    matched = sum(1 for k in env if k in names)
    check("K10", matched == len(env), f"{matched}/{len(env)}", "100%", "Chae 2021 Table 3 environment names found in SPARC")
    LNE = {}
    for k, r in env.items():
        a, b = float(r["log_eN_maxclu"]), float(r["log_eN_noclu"])
        LNE[k] = dict(primary=0.5 * (a + b), maxclu=a, noclu=b)

    def ge_of(name, a0, which="primary"):
        if name not in LNE:
            return 0.0
        return float(S.g_from_gN(10 ** LNE[name][which] * GE_CHAE / a0))

    T1 = dict(K5_reproduction=rep, n_galaxies=len(GALS), n_env=matched, footings={},
              ge_over_a0_quartiles={f: [float(v) for v in np.percentile([ge_of(k, A0[f]) for k in LNE], [10, 25, 50, 75, 90])] for f in FOOTS})
    tt = time.time()
    for f in FOOTS:
        a0 = A0[f]; FR = {}
        # (1) per-galaxy Upsilon, every galaxy isolated, algebraic (exact for spherical AQUAL)
        LGiso = {}
        for q in GALS:
            GB, GO, OK, W = gal_arrays(q, UPS)
            LGiso[q["name"]] = np.log10(np.where(GB > 0, nu1(np.maximum(GB, 1e-300) / a0) * np.maximum(GB, 1e-300), 1e-300))
        rows_iso = fit_sample(GALS, LGiso); FR["iso_perUps"] = pooled(rows_iso)
        # nu_mono comparison (same freedom, isolated algebraic)
        LGm = {}
        for q in GALS:
            GB, GO, OK, W = gal_arrays(q, UPS)
            LGm[q["name"]] = np.log10(np.where(GB > 0, nu_mono(np.maximum(GB, 1e-300) / a0) * np.maximum(GB, 1e-300), 1e-300))
        FR["nu_mono_iso_perUps"] = pooled(fit_sample(GALS, LGm))
        # (2-4) v3: EFE solved (Chae e_N) at L* = 0, 24, 90 pc on the Upsilon nodes
        for L in LSTARS:
            Lk = L / 1000.0
            LG = {"mono": {}, "ring": {}, "gc": {}}
            for q in GALS:
                ge = ge_of(q["name"], a0)
                if ge <= 0 and L == 0:
                    for o in LG:
                        LG[o][q["name"]] = LGiso[q["name"]]
                    continue
                nodes = {o: [] for o in LG}
                for u in NODES:
                    lgs, _ = sparc_solve(q, u, a0, ge, Lk)
                    for o, v in zip(("mono", "ring", "gc"), lgs):
                        nodes[o].append(v)
                for o in LG:
                    LG[o][q["name"]] = interp_nodes(np.array(nodes[o]))
            rows = fit_sample(GALS, LG["mono"])
            key = f"L{int(L)}"
            FR[key] = pooled(rows); FR[key]["Q_le_2"] = pooled(rows, lambda x: x["Q"] <= 2)
            FR[key]["prior_Chae"] = pooled(fit_sample(GALS, LG["mono"], prior=True))
            FR[key]["ring"] = pooled(fit_sample(GALS, LG["ring"])); FR[key]["great_circle"] = pooled(fit_sample(GALS, LG["gc"]))
            FR[key]["per_galaxy"] = rows
            if L == 0:
                FR[key]["iso_only_galaxies"] = pooled(rows, lambda x: x["name"] not in LNE)
                FR[key]["env_galaxies"] = pooled(rows, lambda x: x["name"] in LNE)
            P(f"  [{f}] L* {L:4.0f} pc: rms {FR[key]['rms']:.4f} dex, median Ups {FR[key]['U_median']:.2f}; chi2/dof {FR[key]['chi2nu']:.3f}, "
              f"frac p>=1e-3 {FR[key]['frac_p_ok']:.3f}  ({time.time() - tt:.0f} s)")
            # e_N brackets at the primary best-fit Upsilon (screened ends only)
            if L > 0:
                br = {}
                bestU = {x["name"]: x["U_rms"] for x in rows}
                for which in ("maxclu", "noclu"):
                    num = den = 0.0
                    for q in GALS:
                        GB, GO, OK, W = gal_arrays(q, np.array([bestU[q["name"]]]))
                        ge = ge_of(q["name"], a0, which)
                        if q["name"] in LNE:
                            lgs, _ = sparc_solve(q, bestU[q["name"]], a0, ge, Lk); lg = lgs[0]
                        else:
                            lg = LG["mono"][q["name"]][:, int(np.argmin(abs(UPS - bestU[q["name"]])))]
                        ok = OK[:, 0]; r = np.log10(GO[:, 0]) - lg
                        num += float((W[ok] * r[ok] ** 2).sum()); den += float(W[ok].sum())
                    br[which] = math.sqrt(num / den)
                FR[key]["eN_brackets_rms_at_primary_U"] = br
        # small / large classes at the old global Upsilon (CFG695's), v3 L* = 24 pc, reported only
        U0 = R695[f]["U"]; cls = {"small": [], "large": []}
        for q in GALS:
            m = q["meta"]; Mb = 1.33 * m["MHI"] * 1e9 + U0 * m["L36"] * 1e9
            GB, GO, OK, W = gal_arrays(q, np.array([U0]))
            ge = ge_of(q["name"], a0)
            lg = sparc_solve(q, U0, a0, ge, 0.024)[0][0]
            ok = OK[:, 0]
            if ok.sum() == 0:
                continue
            cls["small" if Mb <= 3e9 else "large"].append(float((W[ok] * (np.log10(GO[ok, 0]) - lg[ok])).sum() / W[ok].sum()))
        FR["classes_global_U"] = {k: dict(N=len(v), mean=float(np.mean(v)), se=float(np.std(v, ddof=1) / math.sqrt(len(v)))) for k, v in cls.items()}
        T1["footings"][f] = FR
    # K3 convergence on 5 environment galaxies (spread in e_N), Upsilon 0.5, L* 0 and 90
    envg = sorted([q for q in GALS if q["name"] in LNE], key=lambda q: LNE[q["name"]]["primary"])
    pick = [envg[int(i)] for i in np.linspace(0, len(envg) - 1, 5)]
    k3 = 0.0
    for q in pick:
        for L in (0.0, 0.09):
            ge = ge_of(q["name"], A0["canonical"])
            a = sparc_solve(q, 0.5, A0["canonical"], ge, L)[0][0]
            b = sparc_solve(q, 0.5, A0["canonical"], ge, L, nper=30, Nt=24)[0][0]
            k3 = max(k3, float(np.max(np.abs(a - b))))
    T1["K3_sparc"] = dict(galaxies=[q["name"] for q in pick], maxdiff=k3)
    RES["K3_parts"] = dict(sparc=k3)
    # D1: thin-disc AQUAL vs the spherical approximation for exponential stellar discs (no gas), reported
    D1 = {}
    for f in FOOTS:
        a0 = A0[f]; Mu = S.mass_unit(a0); SigM = a0 / (2 * math.pi * S.G_SI) / (S.MSUN / (S.KPC / 1e3) ** 2)
        for lS in (1.5, 2.0, 2.5, 3.0, 3.5):
            Rd = 1.0; hz = 0.196 * Rd ** 0.633 / 1.0                        # SPARC thickness convention with Rd = 1 kpc
            Mdisk = 2 * math.pi * (10 ** lS) * 1e6 * Rd ** 2               # Msun (Sigma0 in Msun/pc^2)
            Mt = Mdisk / Mu
            rhof = lambda R, z: Mt / (4 * math.pi * Rd ** 2 * hz) * np.exp(-R / Rd - np.abs(z) / hz)
            re_ = S.log_edges(0.002, 300 * max(20.0, math.sqrt(Mt)), 24); te_ = S.theta_edges(40, full=False, stretch_min=0.003)
            gd = S.Grid(re_, te_)
            rho = gd.rho_axisym(rhof, nq=4); Mg = 2 * float(np.sum(rho * gd.vol))
            pr = S.Problem(gd, rho, Mg, 0.0); pr.solve()
            PhiN = pr.solve_newton()
            Rq = np.linspace(0.5, 6.0, 23) * Rd
            dr, dt = gd.grad_cells(pr.Phi); gR = np.sin(gd.t2d) * dr + np.cos(gd.t2d) * dt
            drN, dtN = gd.grad_cells(PhiN); gRN = np.sin(gd.t2d) * drN + np.cos(gd.t2d) * dtN
            ga = gd.interp_cells(gR, Rq, np.zeros_like(Rq)); gn = gd.interp_cells(gRN, Rq, np.zeros_like(Rq))
            dl = np.log10(ga / (nu1(gn) * gn))
            D1[f"{f}|logSigma0={lS}"] = dict(Sigma0_over_SigmaM=10 ** lS / SigM, median_dlog=float(np.median(dl)), min=float(dl.min()), max=float(dl.max()),
                                             dlog_at_R=[float(v) for v in dl[::4]])
    T1["D1_disc_vs_sphere"] = D1
    # the line and the class
    passes = {(f, L): t1_line(T1["footings"][f][f"L{int(L)}"]) for f in FOOTS for L in (24.0, 90.0)}
    cls1 = tile_class({k: v for k, v in passes.items()})
    var_flip = []
    for f in FOOTS:
        for L in (24.0, 90.0):
            st = T1["footings"][f][f"L{int(L)}"]
            for vn, vs in (("prior_Chae", st["prior_Chae"]), ("Q_le_2", st["Q_le_2"]), ("ring", st["ring"]), ("great_circle", st["great_circle"])):
                if t1_line(vs) != passes[(f, L)]:
                    var_flip.append(f"{f}|L{int(L)}|{vn}")
            for w, v in st["eN_brackets_rms_at_primary_U"].items():
                if (v <= 0.110 and 0.50 <= st["U_median"] <= 0.80) != passes[(f, L)]:
                    var_flip.append(f"{f}|L{int(L)}|eN_{w}")
    chi2lab = {f"{f}|L{int(L)}": chi2_label(T1["footings"][f][f"L{int(L)}"]["frac_p_ok"]) for f in FOOTS for L in (24.0, 90.0)}
    T1["line_passes"] = {f"{f}|L{int(L)}": v for (f, L), v in passes.items()}
    T1["class"] = cls1; T1["qualifier"] = "FRAGILE" if var_flip else "ROBUST"; T1["variant_flips"] = var_flip; T1["chi2_line"] = chi2lab
    RES["tiles"]["T1"] = T1
    P(f"  T1 class {cls1} ({T1['qualifier']}); chi2 line {chi2lab}; K3(sparc) {k3:.4f} dex")



# =====================================================================================================================  T2 MeerKAT
G301, MSUN301, KPC301 = 6.6743e-11, 1.98847e30, 3.0857e19                 # cfg260_core constants (CFG301's chain)
FLAGS301 = ["low_confidence_flag", "blended_flag", "confused_flag", "bad_ellipse_flag", "contaminated_source_flag"]


def implied(D, gb, nu, a0):
    """CFG223's median-residual s*: root of median_i log10[D_i / nu(gb_i/(a0 s))] = 0, bisection on log10 s in [-3, 3], 64 steps."""
    D = np.atleast_2d(np.asarray(D, float)); gb = np.atleast_2d(np.asarray(gb, float))
    lD = np.log10(D)
    f = lambda ls: np.median(lD - np.log10(nu(gb / (a0 * 10.0 ** ls[:, None]))), axis=1)
    a = np.full(D.shape[0], -3.0); b = np.full(D.shape[0], 3.0)
    for _ in range(64):
        m = 0.5 * (a + b); pos = f(m) > 0
        a = np.where(pos, m, a); b = np.where(pos, b, m)
    return 0.5 * (a + b)


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


if want("T2"):
    P("\n=== T2 LOCAL a0 FROM MeerKAT (MIGHTEE-HI) under v3")
    rows = list(csv.DictReader(open(os.path.join(REPO, "data_assembly", "mightee_hi_catalogue_2026-10-02", "MIGHTEE_HI_COSMOS_catalogue.csv"))))
    surv = []
    for r in rows:
        fl = [fnum(r[k]) for k in FLAGS301]
        if not all((v == 0) for v in fl):                                  # missing flag counts as set (CFG301: fillna(1))
            continue
        z, inc, lmhi = fnum(r["z_HI"]), fnum(r["incl_deg"]), fnum(r["log_M_HI"])
        if not (0.02 <= z <= 0.093 and 45.0 <= inc <= 80.0 and lmhi >= 9.0):
            continue
        W, eW = fnum(r["W_50_km_s"]), fnum(r["W_50_km_s_err"])
        if not (np.isfinite(W) and np.isfinite(eW) and W >= 80.0 and eW / W <= 0.15):
            continue
        if not fnum(r["SNR_3D"]) >= 8.0:
            continue
        vals = [fnum(r[k]) for k in ("z_HI", "D_L_Mpc", "log_M_HI", "incl_deg", "log_M_stel")]
        if not (all(np.isfinite(vals)) and fnum(r["log_M_stel"]) > 0):
            continue
        surv.append(dict(z=z, sini=math.sin(math.radians(inc)), mhi=10 ** lmhi, ms=10 ** fnum(r["log_M_stel"]), W=W))
    n2 = len(surv)

    def chain(k):
        mhi = np.array([s["mhi"] for s in surv]); ms = np.array([s["ms"] for s in surv]); z = np.array([s["z"] for s in surv])
        Mb = 1.33 * mhi + ms; R = 0.5 * 10 ** (0.506 * np.log10(mhi) - 3.293) * KPC301
        V = np.array([s["W"] for s in surv]) / (1 + z) ** k / (2 * np.array([s["sini"] for s in surv])) * 1e3
        gb = G301 * Mb * MSUN301 / R ** 2; go = V ** 2 / R
        return go / gb, gb, Mb, R / KPC301

    def sstar(D, gb, nu, B=0, seed=4402):
        l0 = float(implied(D, gb, nu, A0["canonical"])[0])
        if not B:
            return l0
        I = np.random.default_rng(seed).integers(0, len(D), size=(B, len(D)))
        lb = implied(D[I], gb[I], nu, A0["canonical"])
        return l0, [float(v) for v in np.percentile(lb, [2.5, 16, 84, 97.5])]

    # SPARC same-recipe closure sample (CFG301 CC2)
    if "GALS" not in dir():
        GALS = load_sparc_own()
    sel = [q for q in GALS if q["meta"] and q["meta"]["Q"] <= 2 and q["meta"]["Inc"] >= 30.0 and q["meta"]["Vflat"] > 0 and q["meta"]["MHI"] > 0]
    MHI = np.array([q["meta"]["MHI"] for q in sel]) * 1e9; L36 = np.array([q["meta"]["L36"] for q in sel]) * 1e9
    VF = np.array([q["meta"]["Vflat"] for q in sel]) * 1e3
    MbS = 1.33 * MHI + 0.5 * L36; RS_ = 0.5 * 10 ** (0.506 * np.log10(MHI) - 3.293) * KPC301
    gbS = G301 * MbS * MSUN301 / RS_ ** 2; DS = (VF ** 2 / RS_) / gbS
    # K6 reproduction (nu_mono)
    D1_, gb1, Mb2, R2 = chain(1); D0_, gb0, _, _ = chain(0)
    s_obs_mono = 10 ** sstar(D1_, gb1, nu_mono); a_rest_mono = 10 ** sstar(D0_, gb0, nu_mono) * A0["canonical"]; s_cc2_mono = 10 ** sstar(DS, gbS, nu_mono)
    REF301, REF309, REFCC2 = 1.1171056476960852, 1.3110687066534096e-10, 1.3044382238226226
    dk6 = max(abs(s_obs_mono / REF301 - 1), abs(a_rest_mono / REF309 - 1), abs(s_cc2_mono / REFCC2 - 1))
    check("K6", n2 == 47 and len(sel) == 123 and dk6 <= 2e-3, f"N={n2};N_SPARC={len(sel)};maxrel={dk6:.1e}", "47;123;<=2e-3",
          f"CFG301 s* {s_obs_mono:.4f} (1.1171), CFG309 REST a0 {a_rest_mono:.4e} (1.3111e-10), CC2 {s_cc2_mono:.4f} (1.3044)")
    T2 = dict(N=n2, N_sparc=len(sel), reproduction=dict(s_obs_mono=s_obs_mono, a0_rest_mono=a_rest_mono, s_cc2_mono=s_cc2_mono))
    # screening shift on the median survivor (Plummer a = R/5, isolated, 1-D solve)
    scr = {}
    for f in FOOTS:
        a0 = A0[f]; Mu = S.mass_unit(a0); Mt = float(np.median(Mb2)) / Mu; Rr = float(np.median(R2))
        gs = {}
        for L in LSTARS:
            g = S.sphere_grid(Rr / 1000.0, S.r_out_for(Mt, 0.0, Rr), nper=24, Nt=1)
            pr = S.Problem(g, g.rho_spherical(S.plummer_M(Mt, Rr / 5.0)), Mt, 0.0, Lam=L / 1000.0); pr.solve()
            rf, mono, _, _ = g.radial_profiles(pr.Phi); gs[L] = float(g.at_r(rf, mono, np.array([Rr]))[0])
        scr[f] = {f"L{int(L)}": gs[L] / gs[0.0] for L in LSTARS}
    T2["screening_ratio_g_at_R"] = scr
    out = {}
    for k, lab in ((0, "REST"), (1, "OBS")):
        D_, gb_, _, _ = chain(k)
        for nuname, nuf in (("nu_mono", nu_mono), ("nu1", nu1)):
            l0, q = sstar(D_, gb_, nuf, B=4000, seed=4402)
            lS, qS = sstar(DS, gbS, nuf, B=4000, seed=4403)
            row = dict(a0=10 ** l0 * A0["canonical"], q_a0=[10 ** v * A0["canonical"] for v in q], a0_sparc=10 ** lS * A0["canonical"],
                       q_sparc=[10 ** v * A0["canonical"] for v in qS], dlog_M_minus_S=l0 - lS,
                       vs_footing={f: math.log10(10 ** l0 * A0["canonical"] / A0[f]) for f in FOOTS})
            if nuname == "nu1":
                for L in (24.0, 90.0):
                    for f in FOOTS:
                        rat = scr[f][f"L{int(L)}"]
                        lL = sstar(D_ / rat, gb_, nuf); lSL = lS
                        row[f"{f}|L{int(L)}"] = dict(a0=10 ** lL * A0["canonical"], dlog_M_minus_S=lL - lSL, line=abs(lL - lSL) <= 0.15)
            out[f"{lab}|{nuname}"] = row
            P(f"  {lab:4s} {nuname:7s}: a0 = {row['a0']:.4e} (95% {row['q_a0'][0]:.3e}-{row['q_a0'][3]:.3e}); SPARC-recipe {row['a0_sparc']:.4e}; "
              f"log M/S {row['dlog_M_minus_S']:+.4f}; vs canonical {row['vs_footing']['canonical']:+.3f}, alt {row['vs_footing']['alt']:+.3f}")
    T2["rows"] = out
    passes = {(f, L): out["REST|nu1"][f"{f}|L{int(L)}"]["line"] for f in FOOTS for L in (24.0, 90.0)}
    T2["class"] = tile_class(passes)
    T2["qualifier"] = "FRAGILE" if (abs(out["OBS|nu1"]["dlog_M_minus_S"]) <= 0.15) != passes[("canonical", 24.0)] else "ROBUST"
    RES["tiles"]["T2"] = T2
    P(f"  T2 class {T2['class']} ({T2['qualifier']}; OBS-frame variant |dlog| {abs(out['OBS|nu1']['dlog_M_minus_S']):.3f}); screening g ratio at R: {scr}")


# =====================================================================================================================  T3 groups (BFJR)
G540, MSUN540, KPC540 = 6.674e-11, 1.989e30, 3.0857e19
HERN_RE = 1.8153
XG = np.logspace(-5, 5, 3000); LXG = np.log(XG)
RHO_H = 1.0 / (2 * np.pi * XG * (1 + XG) ** 3); M_H = XG ** 2 / (1 + XG) ** 2


def sig2_hern(a0d, nu, aperture=None):
    """LOS sigma^2 (units GM/a), Hernquist, isolated spherical law g = nu(gN/a0d) gN; aperture None = whole system, else R < aperture (a)."""
    gN = M_H / XG ** 2; g = nu(gN / a0d) * gN
    if aperture is None:
        return float(np.trapz(4 * np.pi * XG ** 2 * RHO_H * XG * g * XG, LXG) / 3.0)
    fI = RHO_H * g * XG
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (fI[1:] + fI[:-1]) * np.diff(LXG))])
    Pr = np.maximum(cum[-1] - cum, 1e-300)                                  # rho sigma_r^2 (beta = 0)
    Rg = np.logspace(-4, np.log10(aperture), 160)
    tmax = np.arccosh(XG[-1] / Rg); u = np.linspace(0, 1, 700)
    T = tmax[:, None] * u[None, :]; rr = Rg[:, None] * np.cosh(T); lr = np.log(rr)
    Pi = np.exp(np.interp(lr, LXG, np.log(Pr))); rhoi = np.exp(np.interp(lr, LXG, np.log(RHO_H)))
    w = rr * tmax[:, None]
    Ssp = 2 * np.trapz(Pi * w, u, axis=1); Sg = 2 * np.trapz(rhoi * w, u, axis=1)
    lR = np.log(Rg)
    return float(np.trapz(Ssp * Rg ** 2, lR) / np.trapz(Sg * Rg ** 2, lR))


def group_logsig(o, a0, nu, kfac=1.0, aperture=False, dlM=0.0, consts=(G540, MSUN540, KPC540)):
    Gc, Mc, Kc = consts
    GM = Gc * 10 ** (o["lM"] + dlM) * Mc; a = o["Re"] / kfac * Kc / HERN_RE
    s2 = sig2_hern(a0 * a * a / GM, nu, (o["Re"] / kfac * Kc / a) if aperture else None) * GM / a
    return 0.5 * math.log10(s2) - 3.0


def class_stats(d, s):
    d = np.asarray(d); n = len(d); m = float(d.mean()); se = float(d.std(ddof=1) / math.sqrt(n))
    sys_ = float(np.mean(s) * 0.10); tot = math.hypot(se, sys_); Z = m / tot
    v = "NOT DIAGNOSTIC" if tot > 0.045 else ("CONSISTENT" if abs(Z) < 2 else ("ABOVE LAW" if Z >= 2 else "BELOW LAW"))
    return dict(N=n, mean=m, se=se, sys=sys_, tot=tot, Z=Z, verdict=v, median=float(np.median(d)))


def group_run(groups, a0, nu, **kw):
    d, s = [], []
    for o in groups:
        ls = group_logsig(o, a0, nu, **kw)
        sp = (group_logsig(o, a0, nu, dlM=0.01, **kw) - group_logsig(o, a0, nu, dlM=-0.01, **kw)) / 0.02
        d.append(o["ls"] - ls); s.append(sp)
    return class_stats(d, s), d, s


if want("T3"):
    P("\n=== T3 GALAXY GROUPS (BFJR, Tian+2026) under v3")
    TIAN = os.path.join(os.path.dirname(REPO), "_external_data", "vizier2026", "J_A_A_710_L39.tsv")
    allrows = []
    for l in open(TIAN):
        if l.startswith("#"):
            continue
        r = l.rstrip("\n").split("\t")
        if len(r) < 13 or not r[0].strip().isdigit():
            continue
        allrows.append(dict(sample=r[1].strip(), id=r[2].strip(), ls=float(r[5]), els=float(r[6]), lM=float(r[7]), elM=float(r[8]), Re=float(r[10])))
    groups = [o for o in allrows if o["sample"] == "Galaxy group"]
    REF540 = {"canonical": 0.010043141313594389, "alt": -0.010146209070707778}
    k7 = {}
    for f, a0r in (("canonical", 9.36e-11), ("alt", 1.13e-10)):
        st, _, _ = group_run(groups, a0r, nu_mono)
        k7[f] = st["mean"]
    dk7 = max(abs(k7[f] - REF540[f]) for f in FOOTS)
    check("K7", len(groups) == 63 and dk7 <= 0.002, f"N={len(groups)};max|d|={dk7:.1e}", "63;<=0.002",
          f"CFG540 law-without-edge (nu_mono) class means {k7['canonical']:+.4f} / {k7['alt']:+.4f} (record +0.0100 / -0.0101)")
    T3 = dict(N=len(groups), K7=k7, footings={})
    med = sorted(groups, key=lambda o: o["lM"])[len(groups) // 2]
    for f in FOOTS:
        a0 = A0[f]; FR = {}
        FR["nu_mono_noedge"], _, _ = group_run(groups, a0, nu_mono)
        st, dl, sl = group_run(groups, a0, nu1); FR["v3_isolated"] = st
        FR["variants"] = {"aperture_R<Re": group_run(groups, a0, nu1, aperture=True)[0]}
        for kf in (1.126, 1.563, 2.224, 2.767):
            FR["variants"][f"Re/k k={kf}"] = group_run(groups, a0, nu1, kfac=kf)[0]
        # screening on the median-mass group (1-D isolated solve, virial sigma), applied as a uniform factor
        Mu = S.mass_unit(a0); Mt = 10 ** med["lM"] / Mu; a_k = med["Re"] / HERN_RE
        sg = {}
        for L in LSTARS:
            g = S.sphere_grid(a_k / 1000.0, S.r_out_for(Mt, 0.0, 50 * a_k), nper=24, Nt=1)
            pr = S.Problem(g, g.rho_spherical(S.hernquist_M(Mt, a_k)), Mt, 0.0, Lam=L / 1000.0); pr.solve()
            dr = g.Crr @ pr.Phi
            sg[L] = float(np.sum(pr.rho * g.vol * g.r2d * dr) / (3 * np.sum(pr.rho * g.vol)))
        FR["screening_sigma_ratio_median_group"] = {f"L{int(L)}": math.sqrt(sg[L] / sg[0.0]) for L in LSTARS}
        FR["isolated_1D_virial_vs_integral"] = math.sqrt(sg[0.0] * a0 * S.KPC) / 1e3 / 10 ** group_logsig(med, a0, nu1, consts=(S.G_SI, S.MSUN, S.KPC)) - 1
        for L in (24.0, 90.0):
            sh = math.log10(FR["screening_sigma_ratio_median_group"][f"L{int(L)}"])
            FR[f"L{int(L)}"] = class_stats(np.array(dl) - sh, sl)
        # EFE sensitivity (declared round fields), 2-D solve per group, virial sigma of the internal field
        efe = {}
        for ge in (0.01, 0.03):
            dd = []
            for o in groups:
                Mt = 10 ** o["lM"] / Mu; a_k = o["Re"] / HERN_RE
                _, (gA, prA, gB, prB) = ratio_solve(S.hernquist_M(Mt, a_k), Mt, ge, 0.0, np.array([a_k]), 50 * a_k, a_k / 1000.0)
                rat = virial_s2(gA, prA) / virial_s2(gB, prB)
                dd.append(o["ls"] - (group_logsig(o, a0, nu1, consts=(S.G_SI, S.MSUN, S.KPC)) + 0.5 * math.log10(rat)))
            efe[f"ge={ge}"] = class_stats(dd, sl)
        FR["EFE_sensitivity"] = efe
        T3["footings"][f] = FR
        P(f"  [{f}] nu_mono no edge {FR['nu_mono_noedge']['mean']:+.4f} (Z {FR['nu_mono_noedge']['Z']:+.2f}); v3 isolated {st['mean']:+.4f} (Z {st['Z']:+.2f}) "
          f"{st['verdict']}; L24 {FR['L24']['mean']:+.4f}, L90 {FR['L90']['mean']:+.4f}; EFE 0.01 {efe['ge=0.01']['mean']:+.4f} ({efe['ge=0.01']['verdict']}), "
          f"0.03 {efe['ge=0.03']['mean']:+.4f} ({efe['ge=0.03']['verdict']}); aperture R<Re {FR['variants']['aperture_R<Re']['mean']:+.4f} "
          f"({FR['variants']['aperture_R<Re']['verdict']})")
    passes = {(f, L): T3["footings"][f][f"L{int(L)}"]["verdict"] == "CONSISTENT" for f in FOOTS for L in (24.0, 90.0)}
    T3["class"] = tile_class(passes)
    flips = [f"{f}|{k}" for f in FOOTS for k, v in T3["footings"][f]["variants"].items() if (v["verdict"] == "CONSISTENT") != passes[(f, 24.0)]]
    T3["variant_flips"] = flips; T3["qualifier"] = "FRAGILE" if flips else "ROBUST"
    T3["EFE_flips"] = [f"{f}|{k}" for f in FOOTS for k, v in T3["footings"][f]["EFE_sensitivity"].items() if (v["verdict"] == "CONSISTENT") != passes[(f, 24.0)]]
    RES["tiles"]["T3"] = T3
    P(f"  T3 class {T3['class']} ({T3['qualifier']}; variant flips {flips}; EFE-sensitivity flips {T3['EFE_flips']})")


# =====================================================================================================================  T4 Milky Way vertical force
R0_MW = 8.122
PC2, PC3 = 1e6, 1e9
S0_THIN, RD_THIN, ZD_THIN = 896.0 * PC2, 2.50, 0.300                       # McMillan 2017 Table 3 (as CFG514)
S0_THICK, RD_THICK, ZD_THICK = 183.0 * PC2, 3.02, 0.900
RHO0_B, ALPHA_B, R0_B, RCUT_B, Q_B = 98.4 * PC3, 1.8, 0.075, 2.1, 0.5
R_FID = 8.33
S0_HI = 10.0 * PC2 / math.exp(-4.0 / R_FID - R_FID / 7.0)
S0_H2 = 2.0 * PC2 / math.exp(-12.0 / R_FID - R_FID / 1.5)


def rho_mcm(R, z):
    z = np.abs(z)
    thin = (S0_THIN / (2 * ZD_THIN)) * np.exp(-z / ZD_THIN - R / RD_THIN)
    thick = (S0_THICK / (2 * ZD_THICK)) * np.exp(-z / ZD_THICK - R / RD_THICK)
    rp = np.maximum(np.sqrt(R * R + (z / Q_B) ** 2), 1e-7)
    bulge = RHO0_B / (1 + rp / R0_B) ** ALPHA_B * np.exp(-(rp / RCUT_B) ** 2)
    Rs = np.maximum(R, 1e-6)
    hi = (S0_HI * np.exp(-4.0 / Rs - Rs / 7.0) / (4 * 0.085)) / np.cosh(np.minimum(z / (2 * 0.085), 300)) ** 2
    h2 = (S0_H2 * np.exp(-12.0 / Rs - Rs / 1.5) / (4 * 0.045)) / np.cosh(np.minimum(z / (2 * 0.045), 300)) ** 2
    return thin + thick + bulge + hi + h2


def rho_b2(R, z, Mtot=6.0e10):                                            # CFG516 B2 / B2b
    s = Mtot / 6.0e10
    Mbul, abul = 0.90e10 * s, 0.7; Md, Rd, hd = 4.03e10 * s, 2.6, 0.3; Mg, Rg, hg = 1.08e10 * s, 6.0, 0.1
    z = np.abs(z); r = np.maximum(np.sqrt(R * R + z * z), 1e-7)
    return (Mbul * abul / (2 * math.pi * r * (r + abul) ** 3) + Md / (4 * math.pi * Rd ** 2 * hd) * np.exp(-R / Rd - z / hd)
            + Mg / (4 * math.pi * Rg ** 2 * hg) * np.exp(-R / Rg - z / hg))


def rho_b3(R, z):                                                          # CFG516 B3: thin/thick R_d -> 2.15, Sigma(R0) kept
    zz = np.abs(z); RDS = 2.15
    old = (S0_THIN / (2 * ZD_THIN)) * np.exp(-zz / ZD_THIN - R / RD_THIN) + (S0_THICK / (2 * ZD_THICK)) * np.exp(-zz / ZD_THICK - R / RD_THICK)
    st = S0_THIN * math.exp(-R0_MW / RD_THIN + R0_MW / RDS); sk = S0_THICK * math.exp(-R0_MW / RD_THICK + R0_MW / RDS)
    new = (st / (2 * ZD_THIN)) * np.exp(-zz / ZD_THIN - R / RDS) + (sk / (2 * ZD_THICK)) * np.exp(-zz / ZD_THICK - R / RDS)
    return rho_mcm(R, z) - old + new


def load_tsv(path):
    rows = [l.split() for l in open(path) if l.strip() and not l.startswith("#")]
    hdr = rows[0]; arr = np.array([[float(x) for x in r] for r in rows[1:]])
    return {h: arr[:, i] for i, h in enumerate(hdr)}


if want("T4"):
    P("\n=== T4 MILKY WAY VERTICAL FORCE under v3 (AQUAL disc solve)")
    EIL = load_tsv(os.path.join(DATA, "mw_rc_eilers2019_table1.tsv"))
    EIL_R, EIL_V = EIL["R_kpc"], EIL["vc_kms"]; EIL_E = np.hypot(0.5 * (EIL["sig_minus"] + EIL["sig_plus"]), 0.02 * EIL_V)
    BR = load_tsv(os.path.join(DATA, "mw_kz11_bovyrix2013_table3.tsv"))
    BR_R = BR["R_kpc"] + (R0_MW - 8.0); BR_K, BR_E = BR["Kz11_o2piG"], BR["dKz11_o2piG"]; BR_E5 = np.hypot(BR_E, 0.05 * BR_K)
    LINE4 = float(CHI2.ppf(0.99, len(BR_K)))
    BARY = {"B1_McMillan17": rho_mcm, "B2_L172_6.0e10": lambda R, z: rho_b2(R, z, 6.0e10), "B2b_L172_7.3e10": lambda R, z: rho_b2(R, z, 7.3e10),
            "B3_short_disc_2.15": rho_b3}
    SIGU = S.MSUN / (S.KPC / 1e3) ** 2                                      # kg/m^2 per Msun/pc^2

    def mw_grid(Mt, full=False):
        re_ = S.log_edges(0.005, 300.0 * max(60.0, math.sqrt(Mt)), 30)
        return S.Grid(re_, S.theta_edges(48, full=full, stretch_min=0.002))

    def mw_obs(g, Phi, a0, ge=0.0):
        dr, dt = g.grad_cells(Phi)
        dz = np.cos(g.t2d) * dr - np.sin(g.t2d) * dt                   # internal potential: the uniform field is not in phi
        dR = np.sin(g.t2d) * dr + np.cos(g.t2d) * dt
        conv = a0 / (2 * math.pi * S.G_SI) / SIGU
        Kup = g.interp_cells(dz, BR_R, np.full_like(BR_R, 1.1)) * conv
        if g.full:
            Kdn = -g.interp_cells(dz, BR_R, np.full_like(BR_R, -1.1)) * conv; K = 0.5 * (Kup + Kdn)
        else:
            K = Kup
        K0 = float(g.interp_cells(dz, np.array([R0_MW]), np.array([1.1]))[0] * conv)
        vc = np.sqrt(np.maximum(g.interp_cells(dR, EIL_R, np.zeros_like(EIL_R)), 0) * a0 * EIL_R * S.KPC) / 1e3
        cK = float(np.sum(((K - BR_K) / BR_E5) ** 2)); cR = float(np.sum(((vc - EIL_V) / EIL_E) ** 2))
        A_ = np.vstack([np.ones_like(BR_R), BR_R - R0_MW]).T
        sl = np.linalg.lstsq(A_, np.log(np.maximum(K, 1e-9)), rcond=None)[0][1]
        return dict(chi2_kz=cK, chi2_rc=cR, K_R0=K0, h=float(-1.0 / sl) if sl < 0 else float("inf"),
                    vc_R0=float(np.sqrt(max(g.interp_cells(dR, np.array([R0_MW]), np.array([0.0]))[0], 0) * a0 * R0_MW * S.KPC) / 1e3), K=K.tolist())

    T4 = dict(LINE_chi2_0p99=LINE4, data=dict(K_R0_data="66.4 +- 2.2 (Bovy & Rix)"), models={})
    k8 = {}
    for bname, rhof in BARY.items():
        T4["models"][bname] = {}
        for f in FOOTS:
            a0 = A0[f]; Mu = S.mass_unit(a0)
            Mt0 = 6.6e10 / Mu; g = mw_grid(Mt0)
            rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mt = 2 * float(np.sum(rho1 * g.vol))
            cell = {"Mb_Msun": Mt * Mu}
            if bname == "B1_McMillan17" and f == "canonical":
                Rf = np.geomspace(1e-4, 80, 1500); zf = np.geomspace(1e-5, 30, 1500)
                Mdir = 2 * np.trapz(np.array([np.trapz(2 * math.pi * Rv * rhof(np.full_like(zf, Rv), zf), zf) for Rv in Rf]), Rf)
                prN = S.Problem(g, rho1, Mt, 0.0); PhiN = prN.solve_newton()
                drN, dtN = g.grad_cells(PhiN); dzN = np.cos(g.t2d) * drN - np.sin(g.t2d) * dtN
                KN = float(g.interp_cells(dzN, np.array([R0_MW]), np.array([1.1]))[0] * a0 / (2 * math.pi * S.G_SI) / SIGU)
                zc = np.linspace(0, 1.1, 4001); Sdir = 2 * np.trapz(rhof(np.full_like(zc, R0_MW), zc), zc) / 1e6
                # AMENDMENT A1: independent Newtonian K_z(R0, 1.1) by direct ring quadrature (elliptic integrals) of the same density
                from scipy.special import ellipk, ellipe
                Rr = np.arange(0.00625, 40.0, 0.0125); zq = np.concatenate([-np.geomspace(1e-4, 25.0, 700)[::-1], np.geomspace(1e-4, 25.0, 700)])
                dzq = np.gradient(zq); Kring = 0.0
                for k0 in range(0, len(Rr), 400):
                    Ra = Rr[k0:k0 + 400][:, None]; Za = zq[None, :]
                    dm = 2 * math.pi * Ra * rhof(Ra, Za) * 0.0125 * dzq[None, :]
                    h = 1.1 - Za; den = (Ra + R0_MW) ** 2 + h * h; mk = 4 * Ra * R0_MW / den
                    Kring += float(np.sum(dm * (2 / math.pi) * h * ellipe(mk) / (((Ra - R0_MW) ** 2 + h * h) * np.sqrt(den))))
                Kring_s = Kring / (2 * math.pi) / 1e6                                              # G cancels: K_z/(2 pi G) in Msun/pc^2
                k8.update(mass=abs(Mt * Mu / Mdir - 1), column_frozen_clause=abs(KN / Sdir - 1), ring=abs(KN / Kring_s - 1),
                          KN=KN, Sdir=Sdir, Kring=Kring_s)
                # NFW comparator (Newtonian B1 + NFW fitted to Eilers), reported only
                dRN = np.sin(g.t2d) * drN + np.cos(g.t2d) * dtN
                gRb = g.interp_cells(dRN, EIL_R, np.zeros_like(EIL_R)) * a0 * S.KPC / 1e6        # (km/s)^2/kpc
                gzb = g.interp_cells(dzN, BR_R, np.full_like(BR_R, 1.1)) * a0 / (2 * math.pi * S.G_SI) / SIGU
                Gk = 4.30091e-6; rhoc = 3 * (67.7 / 1e3) ** 2 / (8 * math.pi * Gk)
                def nfw(lM, c):
                    M200 = 10 ** lM; r200 = (3 * M200 / (4 * math.pi * 200 * rhoc)) ** (1 / 3); rs = r200 / c
                    mfun = lambda r: M200 * (np.log(1 + r / rs) - (r / rs) / (1 + r / rs)) / (math.log(1 + c) - c / (1 + c))
                    return mfun
                def resid(x):
                    mf = nfw(x[0], x[1]); return (np.sqrt(np.maximum(gRb * EIL_R + Gk * mf(EIL_R) / EIL_R, 0)) - EIL_V) / EIL_E
                fit = least_squares(resid, x0=[12.0, 10.0], bounds=([11.0, 1.0], [13.3, 40.0]))
                mf = nfw(*fit.x); rB = np.sqrt(BR_R ** 2 + 1.1 ** 2)
                KNFW = gzb + Gk * mf(rB) / rB ** 2 * (1.1 / rB) / (2 * math.pi * Gk) / 1e6
                k8["nfw_chi2"] = float(np.sum(((KNFW - BR_K) / BR_E5) ** 2)); k8["nfw"] = dict(logM200=float(fit.x[0]), c=float(fit.x[1]))
                KN0 = float(KNFW[np.argmin(abs(BR_R - R0_MW))])
            # F0, all L*
            for L in LSTARS:
                pr = S.Problem(g, rho1, Mt, 0.0, Lam=L / 1000.0); pr.solve()
                cell[f"F0|L{int(L)}"] = mw_obs(g, pr.Phi, a0)
                if L == 0 and bname == "B1_McMillan17" and f == "canonical":
                    rr = np.array([40.0, 50.0, 60.0])
                    dr, dt = g.grad_cells(pr.Phi); dR = np.sin(g.t2d) * dr + np.cos(g.t2d) * dt
                    vs = np.sqrt(rr * S.g_from_gN(Mt / rr ** 2)); va = np.sqrt(rr * g.interp_cells(dR, rr, np.zeros_like(rr)))
                    k8["farfield"] = float(np.max(np.abs(va / vs - 1)))
            # FA: amplitude fitted to Eilers by v3's own v_c at L* = 0
            def c2rc(A):
                pr = S.Problem(g, A * rho1, A * Mt, 0.0); pr.solve(); return mw_obs(g, pr.Phi, a0)["chi2_rc"]
            Af = float(minimize_scalar(c2rc, bounds=(0.6, 2.5), method="bounded", options=dict(xatol=2e-3)).x)
            for L in LSTARS:
                pr = S.Problem(g, Af * rho1, Af * Mt, 0.0, Lam=L / 1000.0); pr.solve()
                cell[f"FA|L{int(L)}"] = dict(mw_obs(g, pr.Phi, a0), A=Af)
            # EFE bracket (declared round g_e = 0.03 a0 along the disc axis), B1 F0 L* = 0, full grid
            if bname == "B1_McMillan17":
                gf = mw_grid(Mt0, full=True); rhof1 = gf.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); Mtf = float(np.sum(rhof1 * gf.vol))
                pr = S.Problem(gf, rhof1, Mtf, 0.03); pr.solve()
                cell["F0|L0|ge0.03"] = mw_obs(gf, pr.Phi, a0, ge=0.03)
            T4["models"][bname][f] = cell
            c0 = cell["F0|L24"]; c9 = cell["F0|L90"]
            P(f"  {bname:20s} [{f:9s}] F0 L24: K(R0) {c0['K_R0']:.1f}, chi2_Kz {c0['chi2_kz']:.1f}, h {c0['h']:.2f}, v_c(R0) {c0['vc_R0']:.1f}, chi2_RC "
              f"{c0['chi2_rc']:.0f};  L90 chi2_Kz {c9['chi2_kz']:.1f};  L0 {cell['F0|L0']['chi2_kz']:.1f};  FA A {Af:.3f} chi2_Kz "
              f"{cell['FA|L24']['chi2_kz']:.1f}" + (f";  ge 0.03 chi2_Kz {cell['F0|L0|ge0.03']['chi2_kz']:.1f}" if "F0|L0|ge0.03" in cell else ""))
    T4["NFW_comparator"] = dict(chi2_kz=k8.get("nfw_chi2"), K_R0=KN0, fit=k8.get("nfw"))
    check("K8", k8["mass"] <= 0.02 and k8["ring"] <= 0.01 and k8["farfield"] <= 0.02 and abs(k8["nfw_chi2"] - 43.70) <= 2.0,
          f"mass={k8['mass']:.1e};ring={k8['ring']:.1e};farfield={k8['farfield']:.1e};NFWchi2={k8['nfw_chi2']:.2f}", "<=0.02;<=0.01(A1);<=0.02;43.7+-2",
          f"MW grid mass vs direct integral; Newtonian K_z(R0,1.1) {k8['KN']:.2f} vs ring quadrature {k8['Kring']:.2f} (AMENDMENT A1; the frozen "
          f"column clause reads {k8['column_frozen_clause']:.3f} against 0.03: column {k8['Sdir']:.1f} omits the radial-force term, as CFG514 K3b's +12.6%); "
          "AQUAL v_c 40-60 kpc vs spherical law; own NFW comparator vs CFG514's 43.70")
    T4["K8"] = k8
    passes = {(f, L): T4["models"]["B1_McMillan17"][f][f"F0|L{int(L)}"]["chi2_kz"] <= LINE4 for f in FOOTS for L in (24.0, 90.0)}
    T4["class"] = tile_class(passes)
    flips = [f"{b}|{f}|{v}" for b in BARY for f in FOOTS for v in ("F0", "FA") if not (b == "B1_McMillan17" and v == "F0")
             and (T4["models"][b][f][f"{v}|L24"]["chi2_kz"] <= LINE4) != passes[(f, 24.0)]]
    flips += [f"B1|{f}|ge0.03" for f in FOOTS if (T4["models"]["B1_McMillan17"][f]["F0|L0|ge0.03"]["chi2_kz"] <= LINE4) != passes[(f, 24.0)]]
    T4["variant_flips"] = flips; T4["qualifier"] = "FRAGILE" if flips else "ROBUST"
    T4["record"] = dict(CFG516_B1_F0={f: {k: json.load(open(os.path.join(CFGD, "CFG516_round_cold_energy", "cfg516_mw_results.json")))["models"]["B1_McMillan17"][f"{f}_F0"][k]
                                           for k in ("PD", "RMphi", "RMv")} for f in FOOTS})
    RES["tiles"]["T4"] = T4
    P(f"  T4 line chi2_Kz <= {LINE4:.1f}; class {T4['class']} ({T4['qualifier']}; flips {flips}); NFW comparator chi2_Kz {k8['nfw_chi2']:.1f}")


# =====================================================================================================================  T5 TDGs and DF2/DF4
G936, MSUN936, KPC936, PC936 = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16
NPER5 = 40                                                                 # T5 radial grid per decade (AMENDMENT A4)
A0R = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                         # CFG936's rounded footings (K9 only)


def stats5(r, s):
    r = np.asarray(r, float); s = np.asarray(s, float); n = len(r)
    se = max(float(np.std(r, ddof=1) / math.sqrt(n)), float(math.sqrt(np.sum(s ** 2)) / n))
    c2 = float(np.sum((r / s) ** 2))
    return dict(n=n, rbar=float(np.mean(r)), se=se, chi2=c2, p=float(CHI2.sf(c2, n)))


def class5(st, rlaw):
    if abs(st["rbar"]) < 2 * st["se"] and st["p"] >= 0.05:
        return "EXPLAINS"
    return "PARTIAL" if abs(st["rbar"]) <= 0.5 * abs(rlaw) else "FAILS"


def solve_sphere(Mfun, Mt, ge, Lam_kpc, rmax, r_in, nper=20, Nt=16):
    ro = S.r_out_for(Mt, ge, rmax)
    g = S.sphere_grid(r_in, ro, nper=nper, Nt=Nt if ge > 0 else 1)
    pr = S.Problem(g, g.rho_spherical(Mfun), Mt, ge, Lam=Lam_kpc); pr.solve()
    return g, pr


if want("T5"):
    P("\n=== T5 TIDAL DWARFS (Lelli+15) AND NGC 1052-DF2/DF4 under v3 (host field solved)")
    TDG = []
    for r in csv.DictReader(open(os.path.join(DATA, "tidal_dwarfs", "lelli2015_tdg.csv"))):
        fv = lambda k: float(r[k])
        TDG.append(dict(name=r["object"].replace(" ", ""), V=fv("V_circ_kms"), eV=fv("e_V_circ_kms"), M=fv("M_bar_1e8") * 1e8, eM=fv("e_M_bar_1e8") * 1e8,
                        R=fv("R_out_kpc"), eR=fv("e_R_out_kpc"), LK=fv("host_LK_1e10Lsun") * 1e10, Dp=fv("D_p_kpc")))
    src657 = open(os.path.join(CFGD, "CFG657_trail_capture_rule", "cfg657_capture.py")).read()
    GAL = {}
    for nm in ("DF2", "DF4"):
        m = re.search(r'"%s":\s*dict\(Ms=([0-9.e+]+), eMs=[0-9.]+, Re=([0-9.]+), Dref=[0-9.]+, D=([0-9.]+), obs=\(([0-9.]+), ([0-9.]+), ([0-9.]+)\), pos=\(([0-9.-]+), ([0-9.-]+)\)' % nm, src657)
        GAL[nm] = dict(Ms=float(m.group(1)), Re=float(m.group(2)), D=float(m.group(3)), obs=(float(m.group(4)), float(m.group(5)), float(m.group(6))),
                       pos=(float(m.group(7)), float(m.group(8))))
    mh = re.search(r'HOSTS = \{"NGC1052": \(([0-9.-]+), ([0-9.-]+)\), "NGC1035": \(([0-9.-]+), ([0-9.-]+)\)\}', src657)
    HOSTS = {"NGC1052": (float(mh.group(1)), float(mh.group(2))), "NGC1035": (float(mh.group(3)), float(mh.group(4)))}
    # K9 reproduction (nu_e, CFG931 / CFG933 estimators, rounded footings)
    k9m = {}
    for f in FOOTS:
        dl = []
        for o in TDG:
            Rm = o["R"] * KPC936; gb = G936 * o["M"] * MSUN936 / Rm ** 2; go = (o["V"] * 1e3) ** 2 / Rm
            dl.append(math.log10(go / (gb * float(nu_e(gb / A0R[f])))))
        k9m[f"T|{f}"] = float(np.mean(dl))
        for nm in ("DF2", "DF4"):
            gg = GAL[nm]; r12 = (4 / 3) * gg["Re"] * 1e3 * PC936; gb = G936 * (gg["Ms"] / 2) * MSUN936 / r12 ** 2
            sl = math.sqrt(r12 * gb * float(nu_e(gb / A0R[f])) / 3) / 1e3
            k9m[f"{nm}|{f}"] = 2 * math.log(gg["obs"][0] / sl)
    REF9 = {"T|canonical": -0.6903781917632702, "T|alt": -0.7276095405858052, "DF2|canonical": -1.7090797992538782, "DF4|canonical": -2.1700940800879236,
            "DF2|alt": -1.7973858933111546, "DF4|alt": -2.2578864586814924}
    dk9 = max(abs(k9m[k] - REF9[k]) for k in REF9)
    check("K9", dk9 <= 1e-3, f"{dk9:.1e}", "<=1e-3", f"CFG936 TDG law means {k9m['T|canonical']:+.4f} / {k9m['T|alt']:+.4f}; CFG933 E_obs DF2 "
          f"{k9m['DF2|canonical']:+.4f}, DF4 {k9m['DF4|canonical']:+.4f}")

    def tdg_point(o, a0, L, prof="uniform", hfac=1.0, orient="mono", M=None, R=None, ge_override=None):
        M = o["M"] if M is None else M; R = o["R"] if R is None else R
        Mu = S.mass_unit(a0); Mt = M / Mu
        gNe = (0.6 * o["LK"] * hfac / Mu) / o["Dp"] ** 2
        ge = float(S.g_from_gN(gNe)) if ge_override is None else ge_override
        Mf = S.uniform_M(Mt, R) if prof == "uniform" else S.plummer_M(Mt, R / 2.0)
        rats, _ = ratio_solve(Mf, Mt, ge, L / 1000.0, np.array([R]), 3 * R, R / 100.0, nper=NPER5)
        gN = float(Mf(np.array([R]))[0]) / R ** 2
        gp = float(S.g_from_gN(gN)) * float(rats[{"mono": 0, "ring": 1, "gc": 2}[orient]][0]) * a0
        go = (o["V"] * 1e3) ** 2 / (R * S.KPC)
        return math.log10(go / gp), ge

    def tdg_run(a0, L, **kw):
        pts = []
        for o in TDG:
            r0, ge = tdg_point(o, a0, L, **kw)
            sV = 2 * o["eV"] / (o["V"] * LN10)
            dM = (tdg_point(o, a0, L, M=o["M"] * 1.01, **kw)[0] - r0) / 0.01 * o["eM"] / o["M"]
            dR = (tdg_point(o, a0, L, R=o["R"] * 1.01, **kw)[0] - r0) / 0.01 * o["eR"] / o["R"]
            pts.append(dict(name=o["name"], r=r0, s=math.sqrt(sV ** 2 + dM ** 2 + dR ** 2), ge=ge))
        return pts

    def tdg_law(a0):
        pts = []
        for o in TDG:
            def rr(M, R):
                gb = S.G_SI * M * S.MSUN / (R * S.KPC) ** 2; go = (o["V"] * 1e3) ** 2 / (R * S.KPC)
                return math.log10(go / (gb * float(nu1(gb / a0))))
            r0 = rr(o["M"], o["R"]); sV = 2 * o["eV"] / (o["V"] * LN10)
            dM = (rr(o["M"] * 1.01, o["R"]) - r0) / 0.01 * o["eM"] / o["M"]; dR = (rr(o["M"], o["R"] * 1.01) - r0) / 0.01 * o["eR"] / o["R"]
            pts.append(dict(name=o["name"], r=r0, s=math.sqrt(sV ** 2 + dM ** 2 + dR ** 2)))
        return pts

    def tdg_newton():
        pts = []
        for o in TDG:
            gb = S.G_SI * o["M"] * S.MSUN / (o["R"] * S.KPC) ** 2; go = (o["V"] * 1e3) ** 2 / (o["R"] * S.KPC)
            pts.append(dict(r=math.log10(go / gb), s=2 * o["eV"] / (o["V"] * LN10)))
        return pts

    def plummer_virial_exact(Mt, a):
        x = np.logspace(-5, 5, 6000); lx = np.log(x)
        rho = 3 * Mt / (4 * math.pi * a ** 3) * (1 + x * x) ** -2.5; gN = Mt * x / (a * a * (1 + x * x) ** 1.5)
        return float(np.trapz(4 * math.pi * (a * x) ** 3 * rho * (a * x) * S.g_from_gN(gN), lx) / (3 * Mt))

    def sky_vec(p, q):
        """unit vector (tangent plane) from p to q and separation (rad)."""
        ra1, d1, ra2, d2 = map(math.radians, (p[0], p[1], q[0], q[1]))
        c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(ra1 - ra2)
        dx = (ra2 - ra1) * math.cos(d1); dy = d2 - d1; nrm = math.hypot(dx, dy)
        return np.array([dx / nrm, dy / nrm]), math.acos(min(1.0, c))

    def df_gNe(nm, a0, Mg=1e11, M35=5e9, mode="vector"):
        gg = GAL[nm]; Mu = S.mass_unit(a0); vec = np.zeros(2); tot = 0.0
        for h, Mh in (("NGC1052", Mg), ("NGC1035", M35)):
            u, sep = sky_vec(gg["pos"], HOSTS[h]); Rk = gg["D"] * 1000 * sep
            gn = (Mh / Mu) / Rk ** 2; vec += gn * u; tot += gn
        return float(np.linalg.norm(vec)) if mode == "vector" else tot

    def df_point(nm, a0, L, virial=False, **kw):
        gg = GAL[nm]; Mu = S.mass_unit(a0); Mt = gg["Ms"] / Mu; r12 = (4 / 3) * gg["Re"]
        ge = float(S.g_from_gN(df_gNe(nm, a0, **kw)))
        Mf = S.plummer_M(Mt, r12 / 1.30477)
        rats, (gA, prA, gB, prB) = ratio_solve(Mf, Mt, ge, L / 1000.0, np.array([r12]), 3 * r12, r12 / 100.0, nper=NPER5)
        gN = (Mt / 2) / r12 ** 2; s2law = r12 * float(S.g_from_gN(gN)) * a0 * S.KPC / 3
        if virial:                                                         # exact isolated virial sigma^2 x the solver's ratio
            s2 = plummer_virial_exact(Mt, r12 / 1.30477) * virial_s2(gA, prA) / virial_s2(gB, prB) * a0 * S.KPC
        else:
            s2 = s2law * float(rats[0][0])
        sp, sl = math.sqrt(s2) / 1e3, math.sqrt(s2law) / 1e3
        so, up, lo = gg["obs"]
        Eo, Ep = 2 * math.log(so / sl), 2 * math.log(sp / sl)
        e = lo if so > sp else up
        return dict(name=nm, r=Eo - Ep, s=2 * e / so, E_obs=Eo, E_pred=Ep, sigma_pred=sp, sigma_law=sl, ge=ge)

    T5 = dict(K9=k9m, footings={})
    for f in FOOTS:
        a0 = A0[f]; FR = {}
        law = tdg_law(a0); rlawT = stats5([p["r"] for p in law], [p["s"] for p in law])["rbar"]
        FR["T_law_isolated"] = stats5([p["r"] for p in law], [p["s"] for p in law])
        nt = tdg_newton(); FR["T_newton"] = stats5([p["r"] for p in nt], [p["s"] for p in nt])
        uLaw = [df_point(nm, a0, 0.0, Mg=0.0, M35=0.0) for nm in ("DF2", "DF4")]
        rlawU = float(np.mean([p["E_obs"] for p in uLaw]))
        FR["U_law_isolated"] = stats5([p["E_obs"] for p in uLaw], [p["s"] for p in uLaw])
        for L in LSTARS:
            tp = tdg_run(a0, L); stT = stats5([p["r"] for p in tp], [p["s"] for p in tp])
            up_ = [df_point(nm, a0, L) for nm in ("DF2", "DF4")]; stU = stats5([p["r"] for p in up_], [p["s"] for p in up_])
            cT, cU = class5(stT, rlawT), class5(stU, rlawU)
            FR[f"L{int(L)}"] = dict(T=stT, U=stU, T_class=cT, U_class=cU, T_points=tp, U_points=up_)
            P(f"  [{f}] L* {L:4.0f}: T rbar {stT['rbar']:+.3f} +- {stT['se']:.3f} dex (p {stT['p']:.2g}) {cT}  [law {rlawT:+.3f}, Newton "
              f"{FR['T_newton']['rbar']:+.3f}];  U rbar {stU['rbar']:+.3f} +- {stU['se']:.3f} ln (p {stU['p']:.2g}) {cU}  [law {rlawU:+.3f}]; "
              f"g_e/a0 T {min(p['ge'] for p in tp):.3f}-{max(p['ge'] for p in tp):.3f}, U {up_[0]['ge']:.3f}/{up_[1]['ge']:.3f}")
        # variants at L* = 24 pc
        V = {}
        for lab, kw in (("T_plummer", dict(prof="plummer")), ("T_ring", dict(orient="ring")), ("T_great_circle", dict(orient="gc")),
                        ("T_host_x0.5", dict(hfac=0.5)), ("T_host_x2", dict(hfac=2.0))):
            tp = tdg_run(a0, 24.0, **kw); st = stats5([p["r"] for p in tp], [p["s"] for p in tp]); V[lab] = dict(st, cls=class5(st, rlawT))
        for lab, kw in (("U_scalar_sum", dict(mode="scalar")), ("U_Mg5e10", dict(Mg=5e10)), ("U_Mg3e11", dict(Mg=3e11)), ("U_M35_3e9", dict(M35=3e9)),
                        ("U_M35_1e10", dict(M35=1e10)), ("U_virial", dict(virial=True))):
            up_ = [df_point(nm, a0, 24.0, **kw) for nm in ("DF2", "DF4")]; st = stats5([p["r"] for p in up_], [p["s"] for p in up_])
            V[lab] = dict(st, cls=class5(st, rlawU))
        FR["variants_L24"] = V
        FR["rlaw"] = dict(T=rlawT, U=rlawU)
        T5["footings"][f] = FR
        P(f"  [{f}] variants (L* 24): " + "; ".join(f"{k} {v['rbar']:+.3f} {v['cls']}" for k, v in V.items()))
    # K3 part: the 6 TDGs and DF2/DF4, production grid vs (nper 30, N_theta 24), L* 0 and 90 pc (predictions as used)
    k3t = 0.0
    Mu = S.mass_unit(A0["canonical"])
    for o in TDG:
        Mt = o["M"] / Mu; ge = float(S.g_from_gN((0.6 * o["LK"] / Mu) / o["Dp"] ** 2))
        for L in (0.0, 90.0):
            v = [float(ratio_solve(S.uniform_M(Mt, o["R"]), Mt, ge, L / 1000.0, np.array([o["R"]]), 3 * o["R"], o["R"] / 100.0, nper=npr, Nt=ntt)[0][0][0])
                 for (npr, ntt) in ((NPER5, 16), (int(1.5 * NPER5), 24))]
            k3t = max(k3t, abs(math.log10(v[0] / v[1])))
    for nm in ("DF2", "DF4"):
        gg = GAL[nm]; Mt = gg["Ms"] / Mu; r12 = (4 / 3) * gg["Re"]; ge = float(S.g_from_gN(df_gNe(nm, A0["canonical"])))
        for L in (0.0, 90.0):
            v = [float(ratio_solve(S.plummer_M(Mt, r12 / 1.30477), Mt, ge, L / 1000.0, np.array([r12]), 3 * r12, r12 / 100.0, nper=npr, Nt=ntt)[0][0][0])
                 for (npr, ntt) in ((NPER5, 16), (int(1.5 * NPER5), 24))]
            k3t = max(k3t, abs(math.log10(v[0] / v[1])))
    RES.setdefault("K3_parts", {})["tdg"] = k3t
    def tcls(f, L):
        c = (T5["footings"][f][f"L{int(L)}"]["T_class"], T5["footings"][f][f"L{int(L)}"]["U_class"])
        return c
    allc = {(f, L): tcls(f, L) for f in FOOTS for L in (24.0, 90.0)}
    if all(c == ("EXPLAINS", "EXPLAINS") for c in allc.values()):
        cls5 = "PASS"
    elif any(all(allc[(f, L)][i] == "FAILS" for f in FOOTS for L in (24.0, 90.0)) for i in (0, 1)):
        cls5 = "FAIL"
    else:
        cls5 = "COND"
    flips = [f"{f}|{k}" for f in FOOTS for k, v in T5["footings"][f]["variants_L24"].items()
             if v["cls"] != T5["footings"][f]["L24"]["T_class" if k.startswith("T_") else "U_class"]]
    T5["class"] = cls5; T5["variant_flips"] = flips; T5["qualifier"] = "FRAGILE" if flips else "ROBUST"
    T5["cells"] = {f"{f}|L{int(L)}": list(v) for (f, L), v in allc.items()}
    RES["tiles"]["T5"] = T5
    P(f"  T5 class {cls5} ({T5['qualifier']}; flips {flips}); cells {T5['cells']}; K3(tdg) {k3t:.4f}")


# =====================================================================================================================  finish
if not ONLY or "K3" in ONLY or all(t in ONLY for t in ("T1", "T5")):
    k3all = max(RES.get("K3_parts", {}).values()) if RES.get("K3_parts") else float("nan")
    check("K3", k3all <= 0.003, f"{k3all:.2e}", "<=0.003", "grid convergence (x1.5 in nper and N_theta: SPARC 20 -> 30, T5 40 -> 60 per decade; N_theta 16 -> 24) at L* 0 and 90 pc: " +
          ", ".join(f"{k} {v:.1e}" for k, v in RES.get("K3_parts", {}).items()))
pk = rss_gb()
check("K11", pk < 1.0, f"{pk:.3f}GB", "<1GB", "peak RSS")
RES["runtime_s"] = time.time() - T0; RES["peak_rss_gb"] = pk
npass = sum(ok for _, ok in CHECKS)
P(f"\nruntime {RES['runtime_s']:.0f} s; peak RSS {pk:.3f} GB")
P(f"P4_V3_GALAXY_TILES COMPLETE: {npass}/{len(CHECKS)} checks PASS.")
sfx = TAG + ("_DEV_" + "_".join(ONLY) if ONLY else "")
json.dump(RES, open(os.path.join(HERE, f"p4_v3_galaxy_tiles_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"p4_v3_galaxy_tiles{sfx}.out"), "w").write("\n".join(OUTL).replace(REPO, "<repo>") + "\n")
sys.exit(0 if npass == len(CHECKS) else 1)

#!/usr/bin/env python3
"""CFG223 -- a0 over cosmic time: the implied a0 scale of real data against four laws (flat, a LambdaCDM effective-a0 PROXY, a0 ~ H(z), a0 ~ sqrt(rho_DE) with the record's DESI CPL values).
*** LambdaCDM has no a0: the proxy is an effective-a0 PROXY, not LambdaCDM.  Author decompositions, gas-route-limited; NOT a detection.  kappa = 1/2 is FITTED, NOT DERIVED. ***
Frozen criteria: FROZEN_CRITERIA.md here (1f243e9e9), committed before any implied-a0 value was computed.  No sentence says the data favour a law or a framework.
The estimator (new): s* = the a0 scale (relative to the footing's local a0) that sets the median over a point's galaxies of delta_i(s) = log10[D_i / nu(g_bar,i / (a0 s))] to zero.
Run:  python3 campaign_fresh_gravity/CFG223_a0_over_cosmic_time/cfg223_a0_over_time.py        (MUTATE=1 runs the response control)
"""
import os, sys, io, csv, json, math, tempfile, contextlib, time
sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
REPO = os.path.dirname(CFG)
MUT = os.environ.pop("MUTATE", "").strip() == "1"            # the exec'd lane prefixes must not see MUTATE; this lane injects its own
SFX = "_MUTATE" if MUT else ""
sys.path.insert(0, CFG)
import CFG4_common as K
Z1DIR = os.path.join(REPO, "sonnet55_push", "puzzle_32pi", "agents", "Z1_causal_horizon_a0z")
sys.path.insert(0, Z1DIR)
import zcommon as Z1                                          # READ-ONLY: lcdm_native

OUT, CHK = [], []
T0 = time.time()


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


G2SI = 1e6 / 3.0856775814913673e19
OM = 0.315
NBOOT, SEED = 10000, 223
KER = {"nu_mono": K.nu_mono, "P2": K.nu_p2}
A0F = {"canonical": K.A0["canonical"], "alt": K.A0["alt"]}
CELLS = [("nu_mono", "canonical"), ("nu_mono", "alt"), ("P2", "canonical"), ("P2", "alt")]
PRIM = CELLS[0]
NU, A0L = KER[PRIM[0]], A0F[PRIM[1]]
RC_PATH = {"committed": os.path.join(REPO, "real_research", "data", "rc100_nestorshachar2023_table3.csv"),
           "corrected": os.path.join(REPO, "data_assembly", "rc100_provenance", "rc100_table3_six_fields_paper_values.csv")}
P(__doc__.split("Run:")[0].strip())

# ---- machinery copied VERBATIM from the committed CFG222 script (nu1, gbar_of_gobs, delta_arr, expected_arr, ts, load_rc100, exec_lane, rows_Re, rows_Rout) ----
def nu1(nu, y):
    return float(nu(np.array([y]))[0])


def gbar_of_gobs(gobs, a0t, nu):
    q = gobs / a0t
    return a0t * 10 ** brentq(lambda ly: nu1(nu, 10 ** ly) * 10 ** ly - q, -80, 14, xtol=1e-14, rtol=1e-14)


def delta_arr(D, gb, Fa, a0, nu):
    return np.log10(D / nu(gb / (a0 * Fa)))


def expected_arr(gobs, FT, FL, a0, nu):
    gt = np.array([gbar_of_gobs(g, a0 * ft, nu) for g, ft in zip(gobs, FT)])
    return delta_arr(gobs / gt, gt, FL, a0, nu)


def ts(x, y):
    i, j = np.triu_indices(len(x), 1)
    dx = x[j] - x[i]; m = dx != 0
    return float(np.median((y[j] - y[i])[m] / dx[m]))


def load_rc100(path, mutate=False):
    z, D, gb, go = [], [], [], []
    for r in csv.DictReader(open(path, newline="")):
        zz, Re, Vc, fd = (float(r[k]) for k in ("z", "Re_kpc", "Vc_Re_kms", "fDM_within_Re"))
        if all(math.isfinite(v) for v in (zz, Re, Vc, fd)) and 0 < fd < 1:
            g = Vc ** 2 / Re * G2SI
            z.append(zz); go.append(g); gb.append((1 - fd) * g); D.append(1 / (1 - fd))
    z, D, gb, go = map(np.array, (z, D, gb, go))
    if mutate:
        D = D * 10 ** (0.2 * (z - np.median(z)))
    return dict(z=z, D=D, gb=gb, go=go)


def exec_lane(rel, stop):
    path = os.path.join(CFG, rel)
    src = open(path).read()
    ns = {"__file__": path, "__name__": "lane"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src[:src.index(stop)], rel, "exec"), ns)
    return ns


n213 = exec_lane("CFG213_dysmalpy_two_sided/cfg213_two_sided.py", "BINS = {")
n220 = exec_lane("CFG220_cristal_outer_independent/cfg220_outer_independent.py", "# ------------------------------------------------------------------------------------------------ controls")
cr, EXCL, galaxy_rows213 = n213["cr"], n213["EXCL"], n213["galaxy_rows"]
rows_for220, DET, byid = n220["rows_for"], n220["DET"], n220["byid"]
crbyid = {g["id"]: g for g in cr}


def rows_Re(ids, route, tau=0.0, mutate=False):
    """CRISTAL at R_e (CFG213's Z5 rows); route 'fit' (as galaxy_rows) or 'ind' (M_ind(tau) = M* + M_gas 10^tau, V_c and f_DM as the authors')."""
    out = []
    for i in ids:
        g = crbyid[i]
        if route == "fit":
            r = galaxy_rows213("Z5", [g], alpha=3.36, route=False, mutate=mutate)
            out.extend(r)
            continue
        if not all(math.isfinite(g[k]) for k in ("fdm", "Re", "sig0", "z", "Vrot", "logMstar", "f_molgas", "logMfit")):
            continue
        vc2_ad = g["Vrot"] ** 2 + 3.36 * g["sig0"] ** 2
        gbar0 = (1 - g["fdm"]) * vc2_ad / g["Re"] * G2SI
        Ms = 10 ** g["logMstar"]; Mind = Ms + Ms * g["f_molgas"] / (1 - g["f_molgas"]) * 10 ** tau
        gbar = gbar0 * Mind / 10 ** g["logMfit"]
        D = (vc2_ad / g["Re"] * G2SI) / gbar * (1.5 if mutate else 1.0)
        out.append(dict(id=i, z=g["z"], gbar=gbar, D=D))
    return out


def rows_Rout(rdef, ids, route, tau=0.0, mutate=False):
    return [dict(id=r["id"], z=r["z"], gbar=r["gbar"], D=r["D"]) for r in rows_for220(rdef, ids, route, tau=tau, mutate=mutate)]




# ------------------------------------------------------------------------------------------------ the laws, F_L(z) = a0_L(z) / a0(0)
def E(z):
    return math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


DESI = {"Pantheon+": (-0.838, -0.62), "DESY5": (-0.752, -0.86), "Union3": (-0.667, -1.09)}     # the record's a0z_fork_likelihood_2026.py lines 128-129; taken from the record, not re-checked against the DESI paper


def R_dec(z, w0=-0.838, wa=-0.62):
    """a0 ~ sqrt(rho_DE(z)/rho_DE0), the record's M-DEC, FULL closed form."""
    return math.sqrt((1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * math.exp(-3.0 * wa * z / (1.0 + z)))


LAWS = {"FLAT": lambda z: 1.0, "PROXY": lambda z: Z1.lcdm_native(z), "H(z)": E, "M-DEC": R_dec}
LABEL = {"FLAT": "flat a0", "PROXY": "LCDM effective-a0 PROXY", "H(z)": "a0 ~ H(z)", "M-DEC": "a0 ~ sqrt(rho_DE) (DESI CPL)"}


def Farr(law, z):
    return np.array([LAWS[law](float(zz)) for zz in z])


# ------------------------------------------------------------------------------------------------ the estimator (new)
LO_LS, HI_LS, NIT = -3.0, 3.0, 64


def nuv(nu, y):
    y = np.asarray(y, float)
    return nu(y.ravel()).reshape(y.shape)


def implied(D, gb, nu, a0):
    """log10 s* for each row-set: the root of median_i log10[D_i / nu(gb_i / (a0 s))] = 0 on log10 s in [-3, 3] (vectorised bisection; the median of the
    non-increasing deltas is non-increasing in s).  D, gb: (n,) or (B, n).  Returns (log10 s*, UNBOUNDED flag) per row-set."""
    D = np.atleast_2d(np.asarray(D, float)); gb = np.atleast_2d(np.asarray(gb, float))
    logD = np.log10(D)
    Bn = D.shape[0]

    def f(ls):
        return np.median(logD - np.log10(nuv(nu, gb / (a0 * 10.0 ** ls[:, None]))), axis=1)
    a = np.full(Bn, LO_LS); b = np.full(Bn, HI_LS)
    unb = ~((f(a) > 0) & (f(b) < 0))
    for _ in range(NIT):
        m = 0.5 * (a + b)
        pos = f(m) > 0
        a = np.where(pos, m, a); b = np.where(pos, b, m)
    return 0.5 * (a + b), unb


_IDX = {}


def IDX(n, B):
    if (n, B) not in _IDX:
        _IDX[(n, B)] = np.random.default_rng(SEED * 1000 + n).integers(0, n, size=(B, n))
    return _IDX[(n, B)]


def place(p, FT, nu=NU, a0=A0L):
    """the point's galaxies placed ON a law through their g_obs: g_bar,T from the inversion of g_obs = g_bar nu(g_bar / (a0 F_T(z_i))) at each galaxy (CFG216 / 217), D_T = g_obs / g_bar,T."""
    gt = np.array([gbar_of_gobs(g, a0 * ft, nu) for g, ft in zip(p["go"], FT)])
    return p["go"] / gt, gt


# ------------------------------------------------------------------------------------------------ the points
def build_points(mut=False):
    fac = 1.5 if mut else 1.0
    DS = {t: load_rc100(pth) for t, pth in RC_PATH.items()}
    EDGES = np.percentile(DS["committed"]["z"], [0, 25, 50, 75, 100])
    pts = []

    def add(label, short, dataset, table, route, radius, z, gb, D, fig, kind=None, ids=None):
        z, gb, D = (np.asarray(v, float) for v in (z, gb, D))
        D = D * fac
        pts.append(dict(label=label, short=short, dataset=dataset, table=table, route=route, radius=radius, z=z, gb=gb, D=D, go=gb * D, fig=fig, kind=kind, ids=ids))

    def rc_mask(z, i):
        lo, hi = EDGES[i], EDGES[i + 1]
        return (z >= lo) & ((z < hi) | ((i == 3) & (z <= hi)))
    for t, fig in (("corrected", True), ("committed", False)):
        ds = DS[t]
        for i in range(4):
            m = rc_mask(ds["z"], i)
            add(f"RC100 {t}, z quartile {i + 1} [{EDGES[i]:.2f}, {EDGES[i + 1]:.2f}]", f"RC100 {t[:4]} Q{i + 1}", "RC100", t, "fit", "R_e", ds["z"][m], ds["gb"][m], ds["D"][m], fig)
    ids12 = [g["id"] for g in cr if g["id"] not in EXCL]
    six = list(DET)
    for label, short, kind, route, ids in (("CRISTAL R_e, fit route (12 discs)", "CR R_e fit", "Re", "fit", ids12), ("CRISTAL R_out, fit route (6)", "CR R_out fit", "Rout", "fit", six),
                                           ("CRISTAL R_e, independent route (6 class-A)", "CR R_e ind", "Re", "ind", six), ("CRISTAL R_out, independent route (6)", "CR R_out ind", "Rout", "ind", six)):
        rows = cr_rows(kind, route, ids)
        add(label, short, "CRISTAL", route, route, "R_e" if kind == "Re" else "R_out", [r["z"] for r in rows], [r["gbar"] for r in rows], [r["D"] for r in rows], True, kind=kind, ids=ids)
    # figure points first: RC100 corrected (4), CRISTAL (4), then the committed RC100 (4)
    order = [0, 1, 2, 3, 8, 9, 10, 11, 4, 5, 6, 7]
    return [pts[k] for k in order], DS, EDGES


def cr_rows(kind, route, ids, tau=0.0):
    return rows_Re(ids, route, tau) if kind == "Re" else rows_Rout("table_Rout", ids, route, tau)


TAUS = (-0.30, -0.15, 0.15, 0.30)


def analyse(p, nu=NU, a0=A0L, B=NBOOT):
    n = len(p["z"]); I = IDX(n, B)
    l0, u0 = implied(p["D"], p["gb"], nu, a0)
    lb, ub = implied(p["D"][I], p["gb"][I], nu, a0)
    l0 = float(l0[0])
    q = np.percentile(10 ** lb, [2.5, 16, 84, 97.5])
    r = dict(n=n, z_med=float(np.median(p["z"])), z_min=float(p["z"].min()), z_max=float(p["z"].max()), log_s=l0, s=10 ** l0, unbounded=bool(u0[0]), unb_frac=float(ub.mean()),
             sd_log=float(np.std(lb)), lo95=float(q[0]), lo68=float(q[1]), hi68=float(q[2]), hi95=float(q[3]))
    return r, lb, I


def expectations(p, l0, lb, I, nu=NU, a0=A0L):
    out = {}
    for L in LAWS:
        Dt, gt = place(p, Farr(L, p["z"]), nu, a0)
        e0 = float(implied(Dt, gt, nu, a0)[0][0])
        eb = implied(Dt[I], gt[I], nu, a0)[0]
        sdd = float(np.std(lb - eb))
        out[L] = dict(s=10 ** e0, pull=(l0 - e0) / sdd, sd_diff=sdd)
    return out


def bands(p, nu=NU, a0=A0L):
    """s* after the baryon-mass shifts tau_b; a flag marks the shifts for which NO root exists in [1e-3, 1e3] (the median D falls below 1: the value is then the bracket floor)."""
    out, noroot = {}, {}
    for t in TAUS:
        l, u = implied(p["D"] * 10 ** (-t), p["gb"] * 10 ** t, nu, a0)
        out[t] = 10 ** float(l[0]); noroot[t] = bool(u[0])
    return out, noroot


def gas_bands(p, nu=NU, a0=A0L):
    out = {}
    for t in TAUS:
        rows = cr_rows(p["kind"], "ind", p["ids"], t)
        D = np.array([r["D"] for r in rows]); gb = np.array([r["gbar"] for r in rows])
        out[t] = 10 ** float(implied(D, gb, nu, a0)[0][0])
    return out


def cell_values(p):
    return {f"{k}|{f}": 10 ** float(implied(p["D"], p["gb"], KER[k], A0F[f])[0][0]) for k, f in CELLS}


def flags(r, bd):
    out = {}
    for L, e in r["expected"].items():
        s = e["s"]
        d = {"in95": r["lo95"] <= s <= r["hi95"]}
        for tau, key in ((0.15, "b15"), (0.30, "b30")):
            lo = min(r["lo95"], bd[tau], bd[-tau]); hi = max(r["hi95"], bd[tau], bd[-tau])
            d[key] = lo <= s <= hi
        out[L] = d
    return out


# ------------------------------------------------------------------------------------------------ controls
P("\nCONTROLS")
PTS, DS, EDGES = build_points(mut=False)
P(f"  RC100 z-quartile edges (committed table, {len(DS['committed']['z'])} rows): " + ", ".join(f"{e:.4f}" for e in EDGES) + "; bin sizes (corrected) " + str([p['z'].size for p in PTS[:4]]) + "; CRISTAL point sizes " + str([p['z'].size for p in PTS[4:8]]))
F25 = LAWS["PROXY"](2.5)
okC1 = abs(F25 - 2.16) < 0.02
Rh = {z_: R_dec(float(z_)) for z_ in (0.0, 1.0, 2.0, 3.0)}
okC1 &= Rh[0.0] == 1.0 and abs(Rh[1.0] - 0.990) < 0.002 and abs(Rh[2.0] - 0.874) < 0.002 and abs(Rh[3.0] - 0.775) < 0.002
r5, ru = R_dec(2.0, *DESI["DESY5"]), R_dec(2.0, *DESI["Union3"])
okC1 &= abs(r5 - 0.862) < 0.005 and abs(ru - 0.854) < 0.005
okC1 &= abs(E(1.0) - 1.790) < 0.002 and abs(E(2.0) - 3.032) < 0.002
okC1 &= max(abs(R_dec(z_, -1.0, 0.0) - 1.0) for z_ in (0.5, 2.0, 5.0)) < 1e-12
check("C1 law values: Z1's F(2.5) = 2.16 +- 0.02; M-DEC R(0, 1, 2, 3) = 1, 0.990, 0.874, 0.775 (+- 0.002, the record's header); DESY5 / Union3 R(2) = 0.862 / 0.854 (+- 0.005); E(1), E(2) = 1.790, 3.032; M-DEC(w0 = -1, wa = 0) = 1",
      f"F(2.5) {F25:.3f}; R {Rh[0.0]:.3f} {Rh[1.0]:.4f} {Rh[2.0]:.4f} {Rh[3.0]:.4f}; DESY5 {r5:.4f}; Union3 {ru:.4f}; E {E(1.0):.4f} {E(2.0):.4f}", okC1)


def rc_bin_masks(ds):
    return [(ds["z"] >= EDGES[i]) & ((ds["z"] < EDGES[i + 1]) | ((i == 3) & (ds["z"] <= EDGES[i + 1]))) for i in range(4)]


def rc_mock_through_loader(ds, FT, nu, a0, zfill=None):
    """a mock table built under law T with columns V_c, R_e, f_DM (the observables), read by the loader."""
    gt = np.array([gbar_of_gobs(g, a0 * ft, nu) for g, ft in zip(ds["go"], FT)])
    fd = 1 - gt / ds["go"]
    z = ds["z"] if zfill is None else zfill
    recs = [dict(name="x", z=zz, Re_kpc=5.0, Vc_Re_kms=math.sqrt(g * 5.0 / G2SI), fDM_within_Re=f_, logMbar_Msun=11.0) for zz, g, f_ in zip(z, ds["go"], fd)]
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0])); w.writeheader(); w.writerows(recs); path = f.name
    d = load_rc100(path); os.unlink(path)
    assert len(d["z"]) == len(ds["z"])
    return d


errA, errB, inC, nC = 0.0, 0.0, 0, 0
for t in ("committed", "corrected"):
    ds = DS[t]; masks = rc_bin_masks(ds)
    for cell in CELLS:
        nu, a0 = KER[cell[0]], A0F[cell[1]]
        d = rc_mock_through_loader(ds, np.ones(len(ds["z"])), nu, a0)
        for m in masks:
            errA = max(errA, abs(float(implied(d["D"][m], d["gb"][m], nu, a0)[0][0])))
        for L in ("PROXY", "H(z)", "M-DEC"):
            zmed = np.zeros(len(ds["z"]))
            for m in masks:
                zmed[m] = np.median(ds["z"][m])
            FT = Farr(L, zmed)
            d = rc_mock_through_loader(ds, FT, nu, a0)
            for m in masks:
                errB = max(errB, abs(10 ** float(implied(d["D"][m], d["gb"][m], nu, a0)[0][0]) - float(FT[m][0])))
            FT2 = Farr(L, ds["z"])
            d2 = rc_mock_through_loader(ds, FT2, nu, a0)
            for m in masks:
                s_ = 10 ** float(implied(d2["D"][m], d2["gb"][m], nu, a0)[0][0]); nC += 1
                inC += int(FT2[m].min() * (1 - 1e-9) <= s_ <= FT2[m].max() * (1 + 1e-9))
for p in PTS[4:8]:
    for cell in CELLS:
        nu, a0 = KER[cell[0]], A0F[cell[1]]
        Dt, gt = place(p, np.ones(len(p["z"])), nu, a0)
        errA = max(errA, abs(float(implied(Dt, gt, nu, a0)[0][0])))
        for L in ("PROXY", "H(z)", "M-DEC"):
            zm = float(np.median(p["z"])); FT = np.full(len(p["z"]), LAWS[L](zm))
            Dt, gt = place(p, FT, nu, a0)
            errB = max(errB, abs(10 ** float(implied(Dt, gt, nu, a0)[0][0]) - FT[0]))
            FT2 = Farr(L, p["z"]); Dt, gt = place(p, FT2, nu, a0)
            s_ = 10 ** float(implied(Dt, gt, nu, a0)[0][0]); nC += 1
            inC += int(FT2.min() * (1 - 1e-9) <= s_ <= FT2.max() * (1 + 1e-9))
check("C2a estimator identity: a mock placed ON the flat law (RC100 through V_c, R_e, f_DM and the loader, both tables, every bin; CRISTAL at the row level) returns s* = 1, four cells", f"max |log10 s*| {errA:.1e}", errA < 1e-9)
check("C2b a mock on the proxy / H(z) / M-DEC law with one z per point returns that law's F(z) (four cells, every point)", f"max |s* - F| {errB:.1e}", errB < 1e-7)
check("C2c a mock on each law with the real z_i returns s* inside [min F(z_i), max F(z_i)] (four cells, every point, three laws)", f"{inC}/{nC}", inC == nC)
J216 = {t: json.load(open(os.path.join(CFG, "CFG216_rc100_within_sample", f"cfg216_rc100{'_corrected' if t == 'corrected' else ''}_results.json")))["numbers"]["results"] for t in RC_PATH}
c3a = 0.0
for t in RC_PATH:
    ds = DS[t]
    for cell in CELLS:
        nu, a0 = KER[cell[0]], A0F[cell[1]]
        c3a = max(c3a, abs(ts(ds["z"], np.log10(ds["D"] / nu(ds["gb"] / a0))) - J216[t][f"{cell[0]}|{cell[1]}|flat"]["slope"]))
J222 = json.load(open(os.path.join(CFG, "CFG222_lcdm_proxy", "cfg222_lcdm_proxy_results.json")))["main"]
L222 = ["CRISTAL R_e, fit route, n = 12", "CRISTAL R_out, fit route, six", "CRISTAL R_e, independent route, six class-A", "CRISTAL R_out, independent route, six"]
c3b = max(abs(float(np.median(np.log10(p["D"] / NU(p["gb"] / A0L)))) - J222[l]["FLAT"]["stat"]) for p, l in zip(PTS[4:8], L222))
check("C3a this lane's RC100 per-galaxy delta under the flat law has CFG216's committed FLAT slope (both tables, four cells)", f"max |difference| {c3a:.1e}", c3a < 1e-9)
check("C3b the four CRISTAL points' median delta at s = 1 (flat) equals CFG222's committed median (primary cell)", f"max |difference| {c3b:.1e}", c3b < 1e-9)


def coverage(p, K_=400, B_=1000, sigma=0.25):
    """flat-truth mocks: the point's own g_bar, D = nu(g_bar / a0) 10^N(0, sigma^2); the percentile intervals of the resampled s* must cover s = 1."""
    gb = p["gb"]; n = len(gb); Dflat = nuv(NU, gb / A0L)
    rng = np.random.default_rng(2230 + n)
    I = np.random.default_rng(2231 + n).integers(0, n, size=(B_, n))
    c68 = c95 = 0
    for _ in range(K_):
        Dm = Dflat * 10 ** rng.normal(0, sigma, n)
        lb = implied(Dm[I], gb[I], NU, A0L)[0]
        q = np.percentile(lb, [2.5, 16, 84, 97.5])
        c68 += int(q[1] <= 0 <= q[2]); c95 += int(q[0] <= 0 <= q[3])
    return c68 / K_, c95 / K_


COV = {}
for nm, p in (("n = 6 (CRISTAL R_out independent)", PTS[7]), ("n = 12 (CRISTAL R_e fit)", PTS[4]), (f"n = {PTS[0]['z'].size} (RC100 corrected, first quartile)", PTS[0])):
    COV[nm] = coverage(p)
    check(f"C4 bootstrap coverage on flat-truth mocks, {nm}, scatter 0.25 dex, K = 400, B = 1,000: 68% interval in [0.55, 0.80], 95% interval >= 0.88", f"68%: {COV[nm][0]:.3f}, 95%: {COV[nm][1]:.3f}", 0.55 <= COV[nm][0] <= 0.80 and COV[nm][1] >= 0.88)
okC5, dirs = True, []
for p in PTS:
    Dt, gt = place(p, np.ones(len(p["z"])))
    s0 = 10 ** float(implied(Dt, gt, NU, A0L)[0][0])
    sp = 10 ** float(implied(Dt * 10 ** (-0.15), gt * 10 ** 0.15, NU, A0L)[0][0]); sm = 10 ** float(implied(Dt * 10 ** 0.15, gt * 10 ** (-0.15), NU, A0L)[0][0])
    okC5 &= abs(s0 - 1) < 1e-9 and sp < 1 < sm
    dirs.append((round(sp, 3), round(sm, 3)))
check("C5 band direction: a flat mock with baryons over-estimated by +0.15 dex returns s* < 1, under-estimated returns s* > 1, at every point (and s*(0) = 1)", f"(s*(+0.15), s*(-0.15)) per point {dirs}", okC5)

okC5b, dirs2 = True, []
for p in PTS:
    Dt, gt = place(p, np.ones(len(p["z"])))
    lp, up = implied(Dt * 10 ** (-0.03), gt * 10 ** 0.03, NU, A0L); lm, um = implied(Dt * 10 ** 0.03, gt * 10 ** (-0.03), NU, A0L)
    okC5b &= (not up[0]) and (not um[0]) and 10 ** float(lp[0]) < 1 < 10 ** float(lm[0])
    dirs2.append((round(10 ** float(lp[0]), 3), round(10 ** float(lm[0]), 3)))
check("C5b (ADDED after the first run, not in the frozen list: C5 at +-0.15 dex returns the bracket floor on the over-estimated side because the median D falls below 1) the same direction check at +-0.03 dex with a finite root on both sides at every point", f"(s*(+0.03), s*(-0.03)) per point {dirs2}", okC5b)

if MUT:
    PM, _, _ = build_points(mut=True)
    ok = True
    P("\nMUTATE: D x 1.5 injected into every row of every point (the 95% interval is the UNMUTATED bootstrap interval)")
    for p0, pm in zip(PTS, PM):
        r0, _, _ = analyse(p0)
        rm = float(implied(pm["D"], pm["gb"], NU, A0L)[0][0])
        ratio = 10 ** rm / r0["s"]
        good = ratio >= 2.0 and 10 ** rm > r0["hi95"]
        ok &= good
        P(f"  {p0['short']:14s} s* {r0['s']:.3f} [95% {r0['lo95']:.3f}, {r0['hi95']:.3f}] -> mutated {10 ** rm:.3f}  (x {ratio:.2f}) {'bites' if good else 'DOES NOT BITE'}")
    check("MUTATE every s* rises by a factor of at least 2.0 and leaves its own unmutated 95% interval", f"{ok}", ok)
    open(os.path.join(LANE, "cfg223_a0_over_time_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
    sys.exit(0 if all(CHK) else 1)

# ------------------------------------------------------------------------------------------------ the results
P("\nRESULTS (primary cell: nu_mono, canonical footing; s* = implied a0 ratio to the footing's local a0; 'pull' = (log10 s* - log10 s*_L)/sd, statistics only)")
RES = []
for p in PTS:
    r, lb, I = analyse(p)
    r["expected"] = expectations(p, r["log_s"], lb, I)
    r["bands"], r["band_noroot"] = bands(p)
    r["a0_implied_1e-10"] = r["s"] * A0L / 1e-10
    if p["dataset"] == "CRISTAL" and p["route"] == "ind":
        r["gas_bands"] = gas_bands(p)
    r["cells"] = cell_values(p)
    r["flags"] = flags(r, r["bands"])
    r.update(label=p["label"], short=p["short"], dataset=p["dataset"], table=p["table"], route=p["route"], radius=p["radius"], fig=p["fig"])
    RES.append(r)
    P(f"\n  {p['label']}  (n = {r['n']}, z {r['z_min']:.2f} to {r['z_max']:.2f}, median {r['z_med']:.2f})")
    P(f"    implied a0 ratio s* = {r['s']:.3f}   68% [{r['lo68']:.3f}, {r['hi68']:.3f}]   95% [{r['lo95']:.3f}, {r['hi95']:.3f}]   sd(log10 s*) {r['sd_log']:.3f}   unbounded resamples {100 * r['unb_frac']:.2f}%")
    P("    baryon-mass shifts tau_b (dex): " + "  ".join(f"{t:+.2f}: {v:.3f}{' (NO ROOT: bracket floor)' if r['band_noroot'][t] else ''}" for t, v in r["bands"].items()))
    P(f"    absolute implied a0 = {r['a0_implied_1e-10']:.3f}e-10 m/s^2 (footing-independent)")
    if "gas_bands" in r:
        P("    gas-only shifts tau (dex):      " + "  ".join(f"{t:+.2f}: {v:.3f}" for t, v in r["gas_bands"].items()))
    P("    expected s*_L / pull: " + "   ".join(f"{L} {e['s']:.3f} / {e['pull']:+.2f}" for L, e in r["expected"].items()))
    P("    other cells: " + "   ".join(f"{k} {v:.3f}" for k, v in r["cells"].items()))
    P("    95% interval contains the law's expected ratio (stat / +-0.15 band-widened / +-0.30 band-widened): " + "   ".join(f"{L} {'Y' if f['in95'] else 'n'}{'Y' if f['b15'] else 'n'}{'Y' if f['b30'] else 'n'}" for L, f in r["flags"].items()))

FIG = [r for r in RES if r["fig"]]
cap = ["Author decompositions, gas-route-limited; not a detection. LCDM has no a0: purple is an effective-a0 proxy. kappa = 1/2 is fitted, not derived. "
       "Bars: 68% (thick) and 95% (thin) bootstrap; shaded bars: +-0.15 and +-0.30 dex baryon-mass shifts."]
flat_out = [r for r in FIG if not r["flags"]["FLAT"]["in95"]]
if not flat_out:
    cap.append("Consistent with a constant a0: the flat expectation (ratio 1) lies inside the 95% statistical interval of all eight points.")
else:
    cap.append("The flat expectation (ratio 1) lies outside the 95% statistical interval of " + "; ".join(
        f"{r['label']} ({'below' if r['s'] > 1 else 'above'} it by {abs(math.log10(1 / r['lo95'] if r['s'] > 1 else r['hi95'])):.3f} dex)" for r in flat_out)
        + f" and inside that of the other {len(FIG) - len(flat_out)}; 'consistent with a constant a0' is therefore not claimed at the 95% statistical level.")
for L in LAWS:
    k = [sum(r["flags"][L][key] for r in FIG) for key in ("in95", "b15", "b30")]
    cap.append(f"{LABEL[L]}: the law's expected implied ratio lies inside the 95% interval of {k[0]}/8 points; inside the interval widened by the +-0.15 dex band for {k[1]}/8 and by the +-0.30 dex band for {k[2]}/8.")
P("\nCAPTION (generated by rule):")
for c in cap:
    P("  " + c)
P(f"\n{sum(CHK)}/{len(CHK)} controls pass; {time.time() - T0:.0f} s")
P("Reading rule: these are descriptions of where author decompositions sit against each law's expectation given the gas route; LambdaCDM has no a0; no sentence says the data favour a law or a framework.")

# ------------------------------------------------------------------------------------------------ outputs
zg = np.round(np.arange(0.0, 6.0001, 0.02), 4)
curves = dict(z=zg.tolist(), **{L: [LAWS[L](float(z_)) for z_ in zg] for L in LAWS}, **{f"DESI {k}": [R_dec(float(z_), *v) for z_ in zg] for k, v in DESI.items()})
J = dict(points=RES, caption=cap, curves=curves, controls=dict(passed=sum(CHK), n=len(CHK)), coverage={k: list(v) for k, v in COV.items()}, edges=EDGES.tolist(),
         desi=DESI, taus=list(TAUS), note="s* is relative to the footing's local a0 (canonical 9.3603e-11); the four cells in 'cells'")
json.dump(J, open(os.path.join(LANE, "cfg223_results.json"), "w"), indent=1, default=float)
hdr = "| point | n | z median (range) | implied a0 ratio s* | 68% | 95% | +-0.15 dex baryon band | +-0.30 dex baryon band | pull: flat | proxy | H(z) | M-DEC |"
lines = [hdr, "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for r in RES:
    b, nr = r["bands"], r["band_noroot"]

    def rng(t):
        lo = "no root" if (nr[t] or nr[-t]) else f"{min(b[-t], b[t]):.2f}"
        return f"{lo} to {max(b[-t], b[t]):.2f}"
    unb = f" ({100 * r['unb_frac']:.0f}% of resamples have no root)" if r["unb_frac"] > 0.001 else ""
    lines.append(f"| {r['label']} | {r['n']} | {r['z_med']:.2f} ({r['z_min']:.2f}-{r['z_max']:.2f}) | **{r['s']:.2f}** (a0 = {r['a0_implied_1e-10']:.2f}e-10) | {r['lo68']:.2f}-{r['hi68']:.2f} | {r['lo95']:.2f}-{r['hi95']:.2f}{unb} | "
                 f"{rng(0.15)} | {rng(0.30)} | " + " | ".join(f"{r['expected'][L]['pull']:+.2f}" for L in LAWS) + " |")
lines += ["", "Expected implied ratio s*_L for the same galaxies (the law's own effective value in each point), and the flags (95% statistical / +-0.15 band-widened / +-0.30 band-widened; Y = inside):", "",
          "| point | " + " | ".join(f"{LABEL[L]} s*_L (flags)" for L in LAWS) + " |", "|---|" + "---|" * len(LAWS)]
for r in RES:
    lines.append(f"| {r['short']} | " + " | ".join(f"{r['expected'][L]['s']:.3f} ({''.join('Y' if r['flags'][L][k] else 'n' for k in ('in95', 'b15', 'b30'))})" for L in LAWS) + " |")
lines += ["", "Other kernel / footing cells (point estimates of s*) and, for the independent-route points, the gas-only shifts:", "",
          "| point | nu_mono canonical | nu_mono alt | P2 canonical | P2 alt | gas-only tau -0.30 / -0.15 / +0.15 / +0.30 |", "|---|---|---|---|---|---|"]
for r in RES:
    g = " / ".join(f"{r['gas_bands'][t]:.2f}" for t in TAUS) if "gas_bands" in r else ""
    lines.append(f"| {r['short']} | " + " | ".join(f"{r['cells'][k]:.3f}" for k in r["cells"]) + f" | {g} |")
lines += ["", "Caption (generated by rule):", ""] + [f"- {c}" for c in cap]
open(os.path.join(LANE, "cfg223_points_table.md"), "w").write("\n".join(lines) + "\n")
with open(os.path.join(LANE, "cfg223_points.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["point", "figure_point", "n", "z_med", "z_min", "z_max", "s_star", "lo68", "hi68", "lo95", "hi95", "sd_log10", "band15_lo", "band15_hi", "band30_lo", "band30_hi", "band_no_root_ends", "a0_implied_1e-10", "unbounded_resample_fraction"] + [f"pull_{L}" for L in LAWS] + [f"expected_{L}" for L in LAWS])
    for r in RES:
        b = r["bands"]
        w.writerow([r["label"], int(r["fig"]), r["n"], f"{r['z_med']:.4f}", f"{r['z_min']:.4f}", f"{r['z_max']:.4f}", f"{r['s']:.5f}", f"{r['lo68']:.5f}", f"{r['hi68']:.5f}", f"{r['lo95']:.5f}", f"{r['hi95']:.5f}", f"{r['sd_log']:.5f}",
                    f"{min(b[-0.15], b[0.15]):.5f}", f"{max(b[-0.15], b[0.15]):.5f}", f"{min(b[-0.30], b[0.30]):.5f}", f"{max(b[-0.30], b[0.30]):.5f}", ";".join(f"{t:+.2f}" for t, v in r["band_noroot"].items() if v), f"{r['a0_implied_1e-10']:.4f}", f"{r['unb_frac']:.4f}"] + [f"{r['expected'][L]['pull']:+.4f}" for L in LAWS] + [f"{r['expected'][L]['s']:.5f}" for L in LAWS])
open(os.path.join(LANE, "cfg223_a0_over_time.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if all(CHK) else 1)

#!/usr/bin/env python3
"""PJ1 (FROZEN_CRITERIA.md e3c9bc7d3c): potential-gated biharmonic Jeans scale for the K(Q) component (outside proposal,
graded under the record's gates). TEST lane; adopts nothing. Cold dark energy, never dark matter; no particle.
kappa = 1/2 FITTED; not theory closed. Both footings graded separately, never pooled.

    python3 pj1.py local    -> parts/local.json      G1 (+G1b, G1c), G2, G3, G4, G5, G10 on the declared grid, both forms, both footings; KA1-KA3; M2
      PJ1_MUTATE=M1 python3 pj1.py local -> parts/local_M1.json   (M1: gate inverted, S large where |Phi| is small)
      python3 pj1.py local --points '<json list of points>' --tag NAME -> parts/local_points_NAME.json (M3, KA replay)
    python3 pj1.py web      -> parts/web.json        G8 (QX3 growth ODE + GL1 corrected lensing kernel + fsigma8) and G9 (NC2 forest ratio) on the grid
      python3 pj1.py web --points ... --tag NAME -> parts/web_points_NAME.json
    python3 pj1.py cmb      -> parts/cmb.json        G7: scale-dependent clustered weight S(Phi(k)) at z 1100 through F1A's machinery on raw Planck to ell 2500
    python3 pj1.py bullet   -> parts/bullet.json     G6: DB1 / UX6 Bullet machinery (child process), component on the baryons at S(Phi_Bullet)
    python3 pj1_grade.py    -> pj1.json / pj1.out, pj1_MUTATE.json / pj1_MUTATE.out

Mechanism (as frozen): S(Phi) = R x^p/(1+x^p), x = |Phi|/Phi_*; R_J form T = R_J0 (1+x)^(-p/2), form C = R_J0 (1+x^p)^(-p/2);
[1 + R_J^4 grad^4] rho_K = rho_b S(Phi), solved in spherical symmetry as the two-field system R_J^2 grad^2 rho_K = u,
R_J^2 grad^2 u = rho_b S - rho_K (regularity at the origin, decay at the outer edge; R_J(r) local in each equation), with Phi the
self-consistent depth: Phi(r) = int_r^{r_cut} g_law(G (M_b + M_K)/r'^2) dr', r_cut where g_law = GCUT a0 (QX5's key-a convention,
GCUT 0.03; the record's framework-native depth). Law on the summed source; disc correction g_eff = g [1 - ell^2 grad^2 ln(1 + g/a0)]
with the in-plane (cylindrical) Laplacian for discs (spherical form reported).
Read-only use of QX8 (SPARC exact-field parts), GB1 / QX5 (loaders and gate formulae), F1A (R, CMB machinery), QX3 iter2 (growth,
PR4 lensing), NC2 G3 (forest ratio machinery), UD1 / UD2 (AGC 114905, Malin 1 tables), S1 (Coma UDGs), DB1 / UX6 (Bullet).
One thread, RSS < 1 GB, SIGTERM checkpoint."""
import os, sys, json, math, io, contextlib, time, signal, resource, csv
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"): os.environ[v] = "1"
sys.dont_write_bytecode = True
import warnings; warnings.filterwarnings("ignore")
import numpy as np
np.seterr(all="ignore")
from scipy.linalg import solve_banded

T0 = time.time()
CRIT = "e3c9bc7d3c"
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06"); CL7 = os.path.join(REPO, "closure_2026_11_07"); RB = os.path.join(REPO, "rebuild_2026_10_22")
DATA = os.path.join(REPO, "real_research", "data")
PARTS = os.path.join(HERE, "parts"); os.makedirs(PARTS, exist_ok=True)
FOOTS = ("canonical", "alt")
MUTATE = os.environ.get("PJ1_MUTATE", "")            # "M1": gate inverted
WHICH = sys.argv[1] if len(sys.argv) > 1 else ""
TAG = ("_" + sys.argv[sys.argv.index("--tag") + 1]) if "--tag" in sys.argv else ""
POINTS = json.loads(sys.argv[sys.argv.index("--points") + 1]) if "--points" in sys.argv else None
SUFFIX = ("_" + MUTATE if MUTATE else "") + ("_points" + TAG if POINTS is not None else "")
NOTE = "kappa = 1/2 FITTED; not theory closed"

# physical constants (SI) and units
G_SI = 6.67430e-11; MS = 1.98892e30; KPC = 3.0857e19; MPC = 1e3 * KPC; CL = 2.99792458e8; PC = KPC / 1e3
A0H = {"canonical": 9.360324825027975e-11, "alt": 1.1312035414413022e-10}   # QX5 / GB1 a0 at kappa 1/2 (m/s^2)
GCUT = 0.03                                                                    # QX5 key-a depth convention: r_cut where g_law = GCUT a0
F1A = json.load(open(os.path.join(CL7, "F1A_primary_cmb_audit", "f1a.json")))
RF = {f: float(F1A[f]["R_B2"]) for f in FOOTS}                                # R_cmb primary (5.4096 / 5.4123)
R_ALT = 4.4                                                                    # the proposal's reported alternative

# declared grid (FROZEN_CRITERIA "coarse grid, declared") and the as-written point
RJ0_GRID = [0.3, 0.5, 0.8, 1.4, 2.5, 5.0, 10.0]            # Mpc
PHS_GRID = [3e-7, 1e-6, 1.5e-6, 3e-6, 1e-5, 3e-5]          # Phi_*/c^2
P_GRID = [1, 2, 3]
ELL_GRID = [0.0, 1.5, 3.0]                                  # kpc
FORMS = ("T", "C")
ASW = dict(RJ0=1.4, PHS=1.5e-6, p=2, ell=1.5)
def grid_points():
    pts = []
    for form in FORMS:
        for RJ0 in RJ0_GRID:
            for PHS in PHS_GRID:
                for p in P_GRID: pts.append(dict(RJ0=RJ0, PHS=PHS, p=p, form=form))
    return pts
def pkey(pt): return f"{pt['form']}|RJ0 {pt['RJ0']:g}|PHS {pt['PHS']:g}|p {pt['p']:g}"

RES = {}
def P(s=""): print(s, flush=True)
def rss(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return o
def dump(name, obj): json.dump(clean(obj), open(os.path.join(PARTS, name), "w"), indent=1)
def on_term(sig, frm):
    dump(f"{WHICH}{SUFFIX}_partial.json", RES); P("SIGTERM: partial checkpoint written"); sys.exit(143)
signal.signal(signal.SIGTERM, on_term)
def load_prefix(path, marker, name):
    src = open(path).read(); ns = {"__file__": path, "__name__": name}; a = sys.argv; sys.argv = [path]
    try:
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src[:src.index(marker)], name, "exec"), ns)
    finally: sys.argv = a
    return ns
def glaw(gN, a0): return 0.5 * gN + np.sqrt(0.25 * gN * gN + a0 * gN)

# ================================================================== the mechanism
def S_of(phi, PHS, p, R):
    """clustered weight; MUTATE M1 inverts the gate (large where |Phi| is small)."""
    x = np.abs(phi) / PHS; xp = x ** p
    return R / (1.0 + xp) if MUTATE == "M1" else R * xp / (1.0 + xp)
def RJ_of(phi, RJ0, PHS, p, form):
    x = np.abs(phi) / PHS
    return RJ0 * (1.0 + x) ** (-0.5 * p) if form == "T" else RJ0 * (1.0 + x ** p) ** (-0.5 * p)

class Sphere:
    """log-radial grid; the two-field biharmonic solve; the law's depth to r_cut."""
    def __init__(self, r_min, r_max, n=700):
        self.s = np.linspace(math.log(r_min), math.log(r_max), n); self.r = np.exp(self.s); self.h = self.s[1] - self.s[0]; self.n = n
        se = np.concatenate([[self.s[0] - 0.5 * self.h], 0.5 * (self.s[1:] + self.s[:-1]), [self.s[-1] + 0.5 * self.h]])
        self.re = np.exp(se); self.V = 4 * math.pi / 3 * self.re ** 3; self.dV = np.diff(self.V)
    def rho_from_M(self, M_of_r):
        """mass-conserving shell densities from an enclosed-mass function (m)."""
        Me = np.maximum.accumulate(np.maximum(M_of_r(self.re), 0.0)); Me[0] = 0.0   # the mass inside the first edge sits in the first shell
        return np.diff(Me) / self.dV, Me
    def solve_bih(self, src, RJ, literal=False):
        """[1 + R_J^4 lap^2] rho = src as the two-field system  div(R_J^2 grad rho) = u,  div(R_J^2 grad u) = src - rho  (divergence form:
        with R_J(r) varying it conserves int rho = int src exactly; identical to the frozen split R_J^2 lap f at constant R_J).
        On the log grid: div(c grad f)_i = e^{-3 s_i} [F_{i+1/2} - F_{i-1/2}] / h^2, F_{i+1/2} = e^{s_{i+1/2}} c_{i+1/2} (f_{i+1} - f_i).
        literal=True: the non-divergence ordering c_i lap f (reported only; it does not conserve the source integral).
        Unknowns interleaved (rho_0, u_0, rho_1, u_1, ...); banded (l = u = 2). Regularity: zero inner flux; decay: f(s_N) = 0."""
        n, h = self.n, self.h; A = np.zeros((5, 2 * n)); b = np.zeros(2 * n); c = np.asarray(RJ, float) ** 2
        def put(row, col, val): A[2 + row - col, col] += val
        if literal:
            e2 = np.exp(-2 * self.s); cpp = c * e2 / h ** 2; cp = c * e2 / (2 * h)
            dm, d0, dp = cpp - cp, -2 * cpp, cpp + cp
        else:
            ch = np.sqrt(c[1:] * c[:-1]) * np.exp(0.5 * (self.s[1:] + self.s[:-1]))          # e^{s_{i+1/2}} c_{i+1/2}
            e3 = np.exp(-3 * self.s) / h ** 2
            dp = np.zeros(n); dm = np.zeros(n); dp[:-1] = ch * e3[:-1]; dm[1:] = ch * e3[1:]; d0 = -(dp + dm)
        for i in range(n):
            ri, ui = 2 * i, 2 * i + 1
            if i == n - 1: put(ri, ri, 1.0); put(ui, ui, 1.0); continue
            if i == 0:
                if literal: put(ri, ri, d0[i]); put(ri, ri + 2, dp[i] + dm[i]); put(ui, ui, d0[i]); put(ui, ui + 2, dp[i] + dm[i])
                else: put(ri, ri, -dp[i]); put(ri, ri + 2, dp[i]); put(ui, ui, -dp[i]); put(ui, ui + 2, dp[i])      # zero flux through the inner edge
                put(ri, ui, -1.0); put(ui, ri, 1.0); b[ui] = src[i]
            else:
                put(ri, ri - 2, dm[i]); put(ri, ri, d0[i]); put(ri, ri + 2, dp[i]); put(ri, ui, -1.0)
                put(ui, ui - 2, dm[i]); put(ui, ui, d0[i]); put(ui, ui + 2, dp[i]); put(ui, ri, 1.0); b[ui] = src[i]
        x = solve_banded((2, 2), A, b); return x[0::2], x[1::2]
    def enclosed(self, rho):
        return np.concatenate([[0.0], np.cumsum(rho * self.dV)])   # at the shell edges re
    def Menc_at_r(self, rho):
        Me = self.enclosed(rho); return np.interp(self.r, self.re, Me)

def r_cut_of(Mtot_kg, a0):
    """radius where the point-mass law field equals GCUT a0 (exact inverse of the law: g_N = g^2/(g + a0))."""
    gN = (GCUT * a0) ** 2 / (GCUT * a0 + a0); return math.sqrt(G_SI * Mtot_kg / gN)
def tail_depth(M_kg, r0, a0, n=2000):
    """int_{r0}^{r_cut} g_law(G M/r^2) dr for a point mass, log quadrature (m^2/s^2); 0 if r0 >= r_cut."""
    rc = r_cut_of(M_kg, a0)
    if rc <= r0 or M_kg <= 0: return 0.0
    u = np.linspace(math.log(r0), math.log(rc), n); r = np.exp(u); return float(np.trapz(glaw(G_SI * M_kg / r ** 2, a0) * r, u))
def depth_on_grid(sp, Mtot, a0):
    """Phi(r)/c^2 >= 0 (depth) on sp.r from the law's field of the enclosed total mass, to r_cut (analytic point-mass tail beyond r_max)."""
    g = glaw(G_SI * np.maximum(Mtot, 0.0) * MS / sp.r ** 2, a0); f = g * sp.r
    cum = np.concatenate([np.cumsum((0.5 * (f[1:] + f[:-1]) * sp.h)[::-1])[::-1], [0.0]])     # int_r^{r_max}
    return (cum + tail_depth(Mtot[-1] * MS, sp.r[-1], a0)) / CL ** 2

def selfconsistent(M_of_r, a0, pt, R, r_min, r_max, n=700, phi_ext=0.0, tol=1e-5, itmax=80):
    """M_of_r: enclosed baryon mass (Msun) at radius r (m). Returns the grid, M_K(<r), depth, S, R_J, convergence info.
    phi_ext: an added constant host depth (Coma UDGs). Damped fixed point on Phi."""
    sp = Sphere(r_min, r_max, n); rho_b, Mbe = sp.rho_from_M(M_of_r); Mb = np.interp(sp.r, sp.re, Mbe)
    RJm = lambda ph: RJ_of(ph, pt["RJ0"], pt["PHS"], pt["p"], pt["form"]) * MPC
    phi = depth_on_grid(sp, Mb, a0) + phi_ext; MK = np.zeros(n); conv = False; it = 0; dphi = None
    for it in range(1, itmax + 1):
        Sr = S_of(phi, pt["PHS"], pt["p"], R); RJ = RJm(phi)
        rhoK, _ = sp.solve_bih(rho_b * Sr, RJ); MK = sp.Menc_at_r(rhoK)
        phi_new = depth_on_grid(sp, Mb + MK, a0) + phi_ext
        dphi = float(np.max(np.abs(phi_new - phi)) / max(float(np.max(phi_new)), 1e-30)); phi = 0.5 * phi + 0.5 * phi_new
        if dphi < tol: conv = True; break
    Sr = S_of(phi, pt["PHS"], pt["p"], R); RJ = RJm(phi); rhoK, _ = sp.solve_bih(rho_b * Sr, RJ); MK = sp.Menc_at_r(rhoK)
    return dict(sp=sp, r=sp.r, Mb=Mb, MK=MK, rhoK=rhoK, rho_b=rho_b, phi=phi, S=Sr, RJ=RJ, iters=it, converged=conv, dphi=dphi)

def MK_at(sol, r):
    """enclosed component mass (Msun) at radii r (m), from the shell-edge cumulative sum."""
    Me = sol["sp"].enclosed(sol["rhoK"]); return np.interp(r, sol["sp"].re, Me)

def loglog_M(rk, Mk, s_in=None, flat_out=True):
    """enclosed-mass interpolator from tabulated (r_kpc, M) (power law inside the first point, constant beyond the last)."""
    rk = np.asarray(rk, float); Mk = np.maximum.accumulate(np.maximum(np.asarray(Mk, float), 1e-30)); lr, lM = np.log(rk), np.log(Mk)
    if s_in is None: s_in = max((lM[1] - lM[0]) / (lr[1] - lr[0]), 0.5) if len(rk) > 1 else 2.0
    s_in = min(max(s_in, 0.5), 3.0)
    def M(r_m):
        x = np.log(np.asarray(r_m, float) / KPC); out = np.exp(np.interp(x, lr, lM))
        out = np.where(x < lr[0], Mk[0] * np.exp(s_in * (x - lr[0])), out)
        if not flat_out: out = np.where(x > lr[-1], Mk[-1] * np.exp((lM[-1] - lM[-2]) / (lr[-1] - lr[-2]) * (x - lr[-1])), out)
        return out
    return M
def hernquist_M(Mtot, a_kpc):
    a = a_kpc * KPC; return lambda r: Mtot * (r / (r + a)) ** 2

def disc_factor(sol, a0, ell_kpc, r_eval, cyl=True):
    """g_eff/g = 1 - ell^2 lap ln(1 + g/a0) on the spherical-equivalent summed source; cyl: in-plane Laplacian e^{-2s} f'',
    spherical: e^{-2s}(f'' + f'). Evaluated at r_eval (m)."""
    if ell_kpc == 0.0: return np.ones_like(np.asarray(r_eval, float))
    sp = sol["sp"]; g = G_SI * np.maximum(sol["Mb"] + sol["MK"], 1e-30) * MS / sp.r ** 2; f = np.log1p(g / a0)
    f1 = np.gradient(f, sp.h); f2 = np.gradient(f1, sp.h); lap = np.exp(-2 * sp.s) * (f2 if cyl else f2 + f1)
    D = 1.0 - (ell_kpc * KPC) ** 2 * lap; return np.interp(np.asarray(r_eval, float), sp.r, D)

# ================================================================== local gates
def run_local():
    from astropy.io import fits
    Q8 = None
    sys.path.insert(0, os.path.join(CL6, "QX8_sparc_exact_field")); a = sys.argv; sys.argv = [a[0]]
    with contextlib.redirect_stdout(io.StringIO()):
        import qx8 as Q8
    sys.argv = a
    GALS = Q8.load_sparc(); Q8J = json.load(open(os.path.join(CL6, "QX8_sparc_exact_field", "qx8.json")))
    GB = load_prefix(os.path.join(CL6, "GB1_all_gates_battery", "gb1.py"), "# ------------------------------------------------------------------ main", "gb1_lib")
    GBJ = json.load(open(os.path.join(CL6, "GB1_all_gates_battery", "gb1.json")))
    XC, GR = GB["XC"], GB["GR"]; LE = GB["NS"]["lensing"](); G_KPC = 4.30091e-6
    R500 = {}; XPROF = {}
    for name in sorted({z["name"] for z in XC}):
        p_ = os.path.join(GB["DATA"], "xcop", name)
        with fits.open(os.path.join(p_, f"{name}_fgas_profile.fits")) as h:
            R500[name] = float(h[1].header["R500"]); gas = h[1].data.copy(); gr = np.array(gas["RADIUS"], float) * R500[name]; gM = np.array(gas["MGAS"], float)
        with fits.open(os.path.join(p_, f"{name}_mstar.fits")) as h:
            st = h[2].data.copy(); sr = np.array(st["RADIUS"], float); sM = np.array(st["MSTAR"], float)
        Mbl = [z for z in XC if z["name"] == name][0]["Mb_last"]
        rr = np.geomspace(max(gr[gr > 0][0], sr[sr > 0][0], 1.0), Mbl[1], 60)
        li = lambda r, m, t: 10 ** np.interp(np.log10(t), np.log10(r[m > 0]), np.log10(m[m > 0]))
        Mb = li(gr, gM, rr) + li(sr, sM, rr); Mg = li(gr, gM, rr)
        XPROF[name] = dict(r=rr, Mb=Mb, Mgas=Mg, Mb_last=Mbl)
    lU, lN = np.log(Q8.UPS), np.log(Q8.NODES); ACC = 1e6 / Q8.KPC_S
    PRE = {f: [np.array([np.interp(lU, lN, T[:, j]) for j in range(T.shape[1])]) for T in
               (np.load(os.path.join(Q8.PARTS, f, f"{i:03d}.npz"), allow_pickle=False)["T"] for i in range(len(GALS)))] for f in FOOTS}
    def fit_stats(q, lgp):
        OK, W = q["OK"], q["W"]; r = np.where(OK, np.log10(q["GO"])[:, None] - lgp, 0.0); Wm = np.where(OK, W[:, None], 0.0)
        wr2 = (Wm * r * r).sum(0); wr = (Wm * r).sum(0); ws = Wm.sum(0); i = int(np.argmin(wr2 / np.maximum(ws, 1e-300)))
        return wr2[i], wr[i], ws[i], i
    def pooled(rows, sel=None):
        idx = list(range(len(rows))) if sel is None else list(sel)
        wr2 = sum(rows[i][0] for i in idx); wr = sum(rows[i][1] for i in idx); ws = sum(rows[i][2] for i in idx)
        return dict(rms=float(math.sqrt(wr2 / ws)), mean=float(wr / ws), U_median=float(np.median([Q8.UPS[rows[i][3]] for i in idx])), n=len(idx))
    def sparc_eval(f, bf_list, D_list=None, tmode="T"):
        a0 = A0H[f]; rows = []
        for i, (q, Tf) in enumerate(zip(GALS, PRE[f])):
            g = q["GB"] * bf_list[i][:, None]
            if D_list is not None: g = np.maximum(g * D_list[i][:, None], 1e-30)      # a negative g_eff (the formula as written) floors to 1e-30: a huge residual, not a nan
            lg = np.log10(np.maximum(glaw(g, a0), 1e-300)) + (Tf if tmode == "T" else 0.0); rows.append(fit_stats(q, lg))
        return rows
    # spherical-equivalent baryon profiles of the SPARC galaxies (Upsilon 0.5 disc / 0.7 bulge)
    SPROF = []
    for q in GALS:
        R = q["R"]; VB2 = np.sign(q["Vgas"]) * q["Vgas"] ** 2 + 0.5 * q["Vdisk"] ** 2 + 0.7 * q["Vbul"] ** 2
        Mb = np.maximum.accumulate(np.clip(VB2 * R / G_KPC, 0, None)); Mb = np.maximum(Mb, 1e3)
        SPROF.append(dict(R=R, Mb=Mb, Mof=loglog_M(R, Mb), Mtot=float(Mb[-1]), Vflat=q["meta"]["Vflat"]))
    massive = [i for i, s in enumerate(SPROF) if s["Vflat"] >= 250.0]
    # AGC 114905 (UD1 2024 table) and Malin 1 (UD2 Table 3 + DecoHL components), G1c
    UD1 = json.load(open(os.path.join(RB, "UD1_agc114905_udg_rotation", "ud1.json"))); UD2 = json.load(open(os.path.join(RB, "UD2_malin1_giant_lsb", "ud2.json")))
    CONV = 1e6 / 3.0857e19
    agc = dict(R=np.array(UD1["data2024"]["R"]), V=np.array(UD1["data2024"]["V"]), E=np.array(UD1["data2024"]["E"]),
               vb2=np.array(UD1["baryons"]["Vgas"]) ** 2 + np.array(UD1["baryons"]["Vstar"]) ** 2)
    mal = dict(R=np.array([12.5, 37.5, 62.5, 87.5]), V=np.array([236.9, 216.2, 197.4, 214.1]), E=np.array([9.4, 2.6, 4.7, 11.8]),
               vb2=np.array(UD2["decoHL"]["gas"]) ** 2 + np.array(UD2["decoHL"]["lsb"]) ** 2 + np.array(UD2["decoHL"]["hsb"]) ** 2)
    for d in (agc, mal):
        d["Mb"] = np.maximum.accumulate(d["vb2"] * d["R"] / G_KPC); d["Mof"] = loglog_M(d["R"], d["Mb"])
    def rc_chi2(d, a0, sol=None, ell=0.0):
        gN = d["vb2"] / d["R"] * CONV
        if sol is not None:
            fK = MK_at(sol, d["R"] * KPC) / d["Mb"]; gN = gN * (1 + fK) * disc_factor(sol, a0, ell, d["R"] * KPC)
        g = glaw(np.maximum(gN, 1e-30), a0); V = np.sqrt(np.maximum(g / CONV * d["R"], 0.0)); return float(np.sum(((d["V"] - V) / d["E"]) ** 2))
    # Coma UDGs (S1 rows through GB1's udgs; d_mean from the CSV for the host depth)
    S1D = os.path.join(RB, "S1_v3_hosted_small"); UROWS = list(csv.DictReader(open(os.path.join(S1D, "s1_coma_per_galaxy.csv"))))
    UD = {f: [r for r in UROWS if r["footing"] == f] for f in FOOTS}
    def delta_b(b, ft, a0):
        gN = GB["need"](ft, "x") * a0; return math.log10(glaw(b * gN, a0) / glaw(gN, a0))
    # ---------------- gate evaluations at a point
    def eval_point(f, pt, R, B, base, ells=ELL_GRID, want=("G1", "G2", "G3", "G4", "G5", "G10"), verbose=False):
        a0 = A0H[f]; out = dict(point=pt, R=R); rmax_gal = max(15 * pt["RJ0"], 3.0) * MPC
        if "G1" in want:
            FK, DC, DS, cv = [], [], [], 0
            for s in SPROF:
                sol = selfconsistent(s["Mof"], a0, pt, R, 0.01 * KPC, rmax_gal, n=600); cv += sol["converged"]
                rm = s["R"] * KPC; FK.append(MK_at(sol, rm) / s["Mb"]); DC.append({e: disc_factor(sol, a0, e, rm, True) for e in ells}); DS.append({e: disc_factor(sol, a0, e, rm, False) for e in ells})
            out["G1_converged"] = cv; g1 = {}
            for e in ells:
                rows = sparc_eval(f, [1.0 + fk for fk in FK], [dc[e] for dc in DC]); pa = pooled(rows); pb = pooled(rows, massive)
                rows_s = sparc_eval(f, [1.0 + fk for fk in FK], [ds[e] for ds in DS]); ps = pooled(rows_s)
                g1[e] = dict(G1=dict(status="PASS" if (pa["rms"] <= base["rms"] + 0.010 and abs(pa["mean"]) <= 0.05) else "FAIL", **pa, rms_line=base["rms"] + 0.010),
                             G1b=dict(status="PASS" if (pb["rms"] <= base["rms_massive"] + 0.010 and abs(pb["mean"]) <= 0.05) else "FAIL", **pb, rms_line=base["rms_massive"] + 0.010),
                             spherical_laplacian_reported=dict(rms=ps["rms"], mean=ps["mean"]),
                             negative_geff_fraction=float(np.mean(np.concatenate([dc[e] for dc in DC]) < 0)))
            out["G1_by_ell"] = g1
            out["fK_median_last"] = float(np.median([fk[-1] for fk in FK])); out["fK_max_last"] = float(np.max([fk[-1] for fk in FK]))
            # G1c (informational): AGC 114905 and Malin 1, chi^2 vs law only
            g1c = {}
            for nm, d in (("AGC114905", agc), ("Malin1", mal)):
                sol = selfconsistent(d["Mof"], a0, pt, R, 0.01 * KPC, rmax_gal, n=600)
                g1c[nm] = dict(law_only=rc_chi2(d, a0), by_ell={e: rc_chi2(d, a0, sol, e) for e in ells}, fK_last=float(MK_at(sol, d["R"][-1] * KPC) / d["Mb"][-1]),
                               depth_c2_inner=float(sol["phi"][np.searchsorted(sol["r"], d["R"][0] * KPC)]))
            out["G1c"] = g1c
        if "G2" in want:
            shifts = []; per = []
            for lm in sorted({round(math.log10(p["Mb"] / MS), 3) for p in LE}):
                Mb = 10 ** lm; sol = selfconsistent(hernquist_M(Mb, 3.0), a0, pt, R, 0.01 * KPC, rmax_gal, n=600)
                for p in LE:
                    if round(math.log10(p["Mb"] / MS), 3) != lm: continue
                    r = math.sqrt(G_SI * p["Mb"] / p["gbar"]); mk = float(MK_at(sol, np.array([r]))[0])
                    sh = math.log10(glaw(p["gbar"] + G_SI * mk * MS / r ** 2, a0) / glaw(p["gbar"], a0))
                    per.append(dict(lm=lm, r_Mpc=r / MPC, gbar=p["gbar"], shift=sh, MK_over_Mb=mk / Mb)); shifts.append(sh)
                per[-1]["depth_c2_at_30kpc"] = float(np.interp(30 * KPC, sol["r"], sol["phi"])); per[-1]["S_over_R_at_30kpc"] = float(np.interp(30 * KPC, sol["r"], sol["S"]) / R)
            sh = np.array(shifts); outer = np.array([x["r_Mpc"] >= 0.3 for x in per])
            out["G2"] = dict(status="PASS" if np.all(np.abs(sh) <= 0.05) else "FAIL", max_abs_shift=float(np.max(np.abs(sh))), mean_shift=float(sh.mean()),
                             outer_max_abs_shift=float(np.max(np.abs(sh[outer]))) if outer.any() else None, outer_mean_shift=float(sh[outer].mean()) if outer.any() else None,
                             n_points=len(per), n_fail=int(np.sum(np.abs(sh) > 0.05)), points=per if verbose else None,
                             depth_c2_30kpc_by_bin={str(x["lm"]): x.get("depth_c2_at_30kpc") for x in per if "depth_c2_at_30kpc" in x},
                             S_over_R_30kpc_by_bin={str(x["lm"]): x.get("S_over_R_at_30kpc") for x in per if "S_over_R_at_30kpc" in x})
        if "G3" in want:
            d = []; xr = []; conc = []
            for name, pr in XPROF.items():
                Mof = loglog_M(pr["r"], pr["Mb"]); sol = selfconsistent(Mof, a0, pt, R, 1.0 * KPC, max(15 * pt["RJ0"], 30.0) * MPC, n=600)
                for z in XC:
                    if z["name"] != name: continue
                    rm = z["r_kpc"] * KPC; mk = float(MK_at(sol, np.array([rm]))[0])
                    Mp = glaw(G_SI * (z["M_b"] + mk) * MS / rm ** 2, a0) * rm ** 2 / G_SI / MS; d.append(math.log10(z["M_obs"] / Mp)); xr.append(z["r_kpc"] / R500[name])
                r25, r70 = 0.25 * R500[name] * KPC, 0.7 * R500[name] * KPC
                Mg = loglog_M(pr["r"], pr["Mgas"]); cK = float(MK_at(sol, np.array([r25]))[0] / max(MK_at(sol, np.array([r70]))[0], 1e-30))
                zz = [z for z in XC if z["name"] == name][0]; hM = lambda rk: 10 ** np.interp(math.log10(rk), np.log10(zz["hr"]), np.log10(np.maximum(zz["hM"], 1.0)))
                conc.append(dict(name=name, c_K=cK, c_gas=float(Mg(r25) / Mg(r70)), c_b=float(Mof(r25) / Mof(r70)), c_need_hse=float(hM(0.25 * R500[name]) / hM(0.7 * R500[name])), S_over_R_at_r500=float(np.interp(R500[name] * KPC, sol["r"], sol["S"]) / R),
                                 depth_c2_at_0p1r500=float(np.interp(0.1 * R500[name] * KPC, sol["r"], sol["phi"])), RJ_kpc_at_r500=float(np.interp(R500[name] * KPC, sol["r"], sol["RJ"]) / KPC),
                                 MK_over_Mb_at_last=float(MK_at(sol, np.array([pr["Mb_last"][1] * KPC]))[0] / pr["Mb_last"][0])))
            d = np.array(d); xr = np.array(xr); EDG = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0]; bins = []
            for lo, hi in zip(EDG[:-1], EDG[1:]):
                m = (xr >= lo) & (xr < hi); bins.append(dict(lo=lo, hi=hi, n=int(m.sum()), mean=float(d[m].mean()) if m.sum() else None))
            out["G3"] = dict(status="PASS" if (abs(d.mean()) <= 0.05 and math.sqrt((d ** 2).mean()) <= 0.10) else "FAIL", mean=float(d.mean()), rms=float(math.sqrt((d ** 2).mean())),
                             bins=bins, shape=conc, c_K_median=float(np.median([c["c_K"] for c in conc])), c_gas_median=float(np.median([c["c_gas"] for c in conc])), c_b_median=float(np.median([c["c_b"] for c in conc])), c_need_median=float(np.median([c["c_need_hse"] for c in conc])))
        if "G4" in want:
            o = {}
            for fst in (0, 1):
                npass = 0; med = []
                for gp in GR:
                    sl = math.log(gp["g5"] / gp["pts"][0]["M_gas"]) / math.log(gp["R5"] / gp["R25"])
                    Mof = loglog_M([gp["R25"], gp["R5"]], [gp["pts"][0]["M_gas"] * (1 + fst), gp["g5"] * (1 + fst)], s_in=sl)
                    sol = selfconsistent(Mof, a0, pt, R, 1.0 * KPC, max(15 * pt["RJ0"], 30.0) * MPC, n=600); ok = True
                    for p in gp["pts"]:
                        rm = p["r_kpc"] * KPC; Mb = p["M_gas"] * (1 + fst); mk = float(MK_at(sol, np.array([rm]))[0])
                        Mp = glaw(G_SI * (Mb + mk) * MS / rm ** 2, a0) * rm ** 2 / G_SI / MS; dl = math.log10(p["M_obs"] / Mp); med.append(dl)
                        ok &= abs(dl) <= 2 * p["eM"] / (p["M_obs"] * math.log(10))
                    npass += ok
                o[f"fst{fst}"] = dict(n_pass=int(npass), median_res=float(np.median(med)))
            out["G4"] = dict(status="PASS" if all(v["n_pass"] >= 16 for v in o.values()) else "FAIL", **o)
        if "G5" in want:
            res = []; bs = []
            for p, row in zip(B["U"], UD[f]):
                Ms = float(row["Mstar"]); Re = float(row["Re_kpc"]); xe = float(row["x_e_dmean"]); dkpc = float(row["d_mean_kpc"])
                phi_host = (xe * a0 * dkpc * KPC * math.log(xe / GCUT) if xe > GCUT else 0.0) / CL ** 2     # deep-regime 1/r host field from d to r_cut (declared)
                sol = selfconsistent(hernquist_M(Ms, Re / 1.815), a0, pt, R, 0.001 * KPC, max(15 * pt["RJ0"], 3.0) * MPC, n=600, phi_ext=phi_host)
                rh = 4 / 3 * Re * KPC; mk = float(MK_at(sol, np.array([rh]))[0]); b = 1.0 + mk / (0.5 * Ms); bs.append(b)
                res.append(p["D"] - delta_b(b, p["feat"], a0))
            mu = float(np.mean(res)); out["G5"] = dict(status="PASS" if abs(mu) <= 2 * B["sigU"] else "FAIL", mean=mu, sigma_U=B["sigU"], z=mu / B["sigU"], b_median=float(np.median(bs)),
                                                       phi_host_c2_example=phi_host, law_only_mean=float(np.mean([p["D"] for p in B["U"]])))
        if "G10" in want:
            # Milky Way as the Sun's host (6e10 Msun Hernquist a 3 kpc): the component's density at R0 = 8.2 kpc acts on the planets as (4 pi/3) G rho_K r
            sol = selfconsistent(hernquist_M(6e10, 3.0), a0, pt, R, 0.01 * KPC, rmax_gal, n=600)
            i0 = np.searchsorted(sol["r"], 8.2 * KPC); rhoK = float(sol["rhoK"][i0]) * MS   # kg/m^3
            def cand(ft):
                gN = ft["x"] * a0; gK = 4 * math.pi / 3 * G_SI * rhoK * ft["r"]; return dict(delta=math.log10(glaw(gN + gK, a0) / glaw(gN, a0)))
            ok, num = GB["g_ss"](cand, B, a0)
            out["G10"] = dict(status="PASS" if ok else "FAIL", rhoK_Msun_pc3=rhoK / MS * PC ** 3, depth_c2_R0=float(sol["phi"][i0]), S_over_R_R0=float(sol["S"][i0] / R), RJ_Mpc_R0=float(sol["RJ"][i0] / MPC),
                              cassini_use=num["cassini_use"], worst_planet_use=num["worst_planet_use"], Q2_component_s2=4 * math.pi / 3 * G_SI * rhoK, cT="1 (spatial-only term; the action's kinetic structure is unchanged)")
        return out
    def summary(o, e=ASW["ell"]):
        g1 = o.get("G1_by_ell", {}).get(e, {})
        g0 = o.get("G1_by_ell", {}).get(0.0, {})
        return (f"G1(ell {e:g}) {g1.get('G1', {}).get('status', '-')[:1]} rms {g1.get('G1', {}).get('rms', float('nan')):.3f} neg {g1.get('negative_geff_fraction', float('nan')):.2f} | G1(ell 0) {g0.get('G1', {}).get('status', '-')[:1]} rms {g0.get('G1', {}).get('rms', float('nan')):.4f} mean {g0.get('G1', {}).get('mean', float('nan')):+.3f} fK {o.get('fK_median_last', float('nan')):.1e} | G1b(0) {g0.get('G1b', {}).get('status', '-')[:1]} "
                f"| G2 {o['G2']['status'][0]} max {o['G2']['max_abs_shift']:.3f} outer {o['G2']['outer_max_abs_shift']:.3f} | G3 {o['G3']['status'][0]} {o['G3']['mean']:+.3f}/{o['G3']['rms']:.3f} cK {o['G3']['c_K_median']:.2f} "
                f"| G4 {o['G4']['status'][0]} {o['G4']['fst0']['n_pass']}/{o['G4']['fst1']['n_pass']} | G5 {o['G5']['status'][0]} {o['G5']['mean']:+.3f} b {o['G5']['b_median']:.2f} | G10 {o['G10']['status'][0]}")
    # preemptible: a run that died (SIGTERM, disk) resumes from its own partial checkpoint; every point is graded by the same code
    PREV = {}; pp0 = os.path.join(PARTS, f"local{SUFFIX}_partial.json")
    if POINTS is None and os.path.exists(pp0):
        PREV = json.load(open(pp0)); P("resuming from " + pp0 + ": " + ", ".join(f"{k}: {len(v.get('grid', []))} grid points" for k, v in PREV.items() if isinstance(v, dict)))
    for f in FOOTS:
        a0 = A0H[f]; Rf = RF[f]; R_ = {}; RES[f] = R_
        S, E_, X = GB["build"](f, a0); U = GB["udgs"](f, a0)
        st = GB["R1"][f"{f}|S4 v3 dmean L*floor E-W"]; sigU = math.hypot(st["se"], st["sigma_sys"]) / math.log(10)
        B = dict(f=f, S=S, E=E_, X=X, U=U, sigU=sigU, GR={0: GB["groups_pts"](a0, 0.0), 1: GB["groups_pts"](a0, 1.0)})
        # known answers
        ka = {}
        rows0 = sparc_eval(f, [np.ones(len(q["R"])) for q in GALS]); p0 = pooled(rows0); pm0 = pooled(rows0, massive)
        rx = Q8J["footings"][f].get("exact", Q8J["footings"][f].get("st_ex", {}))
        ka["KA1_qx8_law"] = dict(rms=p0["rms"], U=p0["U_median"], qx8_rms=rx["rms"], qx8_U=rx["U_median"], pass_=bool(abs(p0["rms"] - rx["rms"]) <= 1e-6 and abs(p0["U_median"] - rx["U_median"]) <= 1e-6))
        L0 = GBJ["cands"]["L0"][f]
        d0 = []
        for z in XC:
            rm = z["r_kpc"] * KPC; Mp = glaw(G_SI * z["M_b"] * MS / rm ** 2, a0) * rm ** 2 / G_SI / MS; d0.append(math.log10(z["M_obs"] / Mp))
        d0 = np.array(d0); ka["KA2_gb1_L0_xcop"] = dict(mean=float(d0.mean()), rms=float(np.sqrt((d0 ** 2).mean())), gb1=[L0["G2 X-COP"]["num"]["mean"], L0["G2 X-COP"]["num"]["rms"]],
                                                        pass_=bool(abs(d0.mean() - L0["G2 X-COP"]["num"]["mean"]) <= 1e-6 and abs(math.sqrt((d0 ** 2).mean()) - L0["G2 X-COP"]["num"]["rms"]) <= 1e-6))
        u0 = float(np.mean([p["D"] for p in U])); ka["KA2_gb1_L0_udg"] = dict(mean=u0, gb1=L0["G5 Coma UDGs"]["num"]["mean"], pass_=bool(abs(u0 - L0["G5 Coma UDGs"]["num"]["mean"]) <= 1e-6))
        # KA3: biharmonic solver at constant R_J vs the Fourier-exact response to a Gaussian source (sigma 0.1 Mpc, R_J 1 Mpc):
        # rho_K(r) = (1/(2 pi^2 r)) int k sin(kr) rho_b(k) / (1 + R_J^4 k^4) dk; plus the point-source closed form
        # M_K(<r)/(S M) = 1 - e^{-x}[x (sin x + cos x) + cos x], x = r/(sqrt2 R_J), on a 3 kpc Hernquist beyond 0.3 Mpc (reported)
        spT = Sphere(0.01 * KPC, 30 * MPC, 900); RJt = 1.0 * MPC; sg = 0.1 * MPC; Mt = 1e11
        rho_g = Mt * np.exp(-spT.r ** 2 / (2 * sg ** 2)) / ((2 * math.pi) ** 1.5 * sg ** 3); rhoK, _ = spT.solve_bih(rho_g, np.full(spT.n, RJt))
        kk = np.linspace(1e-4 / MPC, 60 / sg, 400000); ratios = []
        for rr in (0.05, 0.2, 0.5, 1.0, 2.0, 4.0):
            i = np.searchsorted(spT.r, rr * MPC); ex = (1 / (2 * math.pi ** 2 * spT.r[i])) * np.trapz(kk * np.sin(kk * spT.r[i]) * Mt * np.exp(-kk ** 2 * sg ** 2 / 2) / (1 + RJt ** 4 * kk ** 4), kk)
            ratios.append(float(rhoK[i] / ex))
        rho_h, _ = spT.rho_from_M(hernquist_M(Mt, 3.0)); rhoH, _ = spT.solve_bih(rho_h, np.full(spT.n, RJt)); Me = spT.enclosed(rhoH)
        xx = spT.re / (math.sqrt(2) * RJt); ana = Mt * (1 - np.exp(-xx) * (xx * (np.sin(xx) + np.cos(xx)) + np.cos(xx))); sel = spT.re > 0.3 * MPC
        ka["KA3_biharmonic_solver"] = dict(gaussian_ratio_solver_over_exact=ratios, max_abs_dev=float(np.max(np.abs(np.array(ratios) - 1))), total_fraction_gaussian=float(spT.enclosed(rhoK)[-1] / Mt),
                                           point_source_closed_form_max_err_r_gt_0p3Mpc=float(np.max(np.abs(Me[sel] - ana[sel])) / Mt), total_fraction_hernquist=float(Me[-1] / Mt),
                                           pass_=bool(np.max(np.abs(np.array(ratios) - 1)) <= 2e-3 and abs(spT.enclosed(rhoK)[-1] / Mt - 1) <= 2e-3))
        # KA4: depth convention vs QX5's tail_phi for a point mass
        tq = GB["tail_phi"](1e12 * MS, 10 * KPC, a0); tm = tail_depth(1e12 * MS, 10 * KPC, a0); ka["KA4_depth_tail_vs_qx5"] = dict(mine=tm, qx5=tq, rel=abs(tm / tq - 1), pass_=bool(abs(tm / tq - 1) <= 1e-3))
        R_["KA"] = ka
        for k, v in ka.items(): P(f"[{f}] {k}: {'PASS' if v['pass_'] else 'FAIL'}  " + json.dumps(clean({a: b for a, b in v.items() if a != 'pass_'}))[:260])
        if not all(v["pass_"] for v in ka.values()): P(f"[{f}] KA FAIL: stop"); continue
        base = dict(rms=p0["rms"], mean=p0["mean"], rms_massive=pm0["rms"], n_massive=len(massive))
        R_["baselines"] = dict(sparc=base, xcop_law_only=dict(mean=float(d0.mean()), rms=float(np.sqrt((d0 ** 2).mean()))), udg_law_only=u0,
                               agc114905_law_chi2=rc_chi2(agc, a0), malin1_law_chi2=rc_chi2(mal, a0))
        # M2 (S -> 0): the law alone; X-COP must FAIL
        R_["M2_S0"] = dict(G3=dict(mean=float(d0.mean()), rms=float(np.sqrt((d0 ** 2).mean())), fail=bool(not (abs(d0.mean()) <= 0.05 and math.sqrt((d0 ** 2).mean()) <= 0.10))))
        R_["M2_S0"]["bites"] = R_["M2_S0"]["G3"]["fail"]
        P(f"[{f}] M2 (S -> 0): X-COP {d0.mean():+.4f}/{math.sqrt((d0**2).mean()):.4f} -> {'BITES' if R_['M2_S0']['bites'] else 'NO BITE'}")
        pts = POINTS if POINTS is not None else grid_points()
        # the as-written point first (R primary, and R 4.4 reported), with the per-point lens table
        prev_asw = PREV.get(f, {}).get("as_written", {})
        if POINTS is None and all(k in prev_asw for form in FORMS for k in (form, form + "_R4.4_reported")):
            R_["as_written"] = prev_asw; P(f"[{f}] as-written point taken from the checkpoint")
        elif POINTS is None:
            asw = dict(RJ0=ASW["RJ0"], PHS=ASW["PHS"], p=ASW["p"])
            R_["as_written"] = {}
            for form in FORMS:
                pt = dict(asw, form=form); o = eval_point(f, pt, Rf, B, base, verbose=True); R_["as_written"][form] = o
                P(f"[{f}] AS-WRITTEN form {form} (R {Rf:.3f}): " + summary(o) + f"  [{time.time()-T0:.0f}s {rss():.2f}GB]")
                o44 = eval_point(f, pt, R_ALT, B, base, ells=[ASW["ell"]]); R_["as_written"][form + "_R4.4_reported"] = o44
                P(f"[{f}]   reported R 4.4 form {form}: " + summary(o44))
            dump(f"local{SUFFIX}_partial.json", RES)
        grid = []; done = {pkey(o["point"]): o for o in PREV.get(f, {}).get("grid", [])}
        for i, pt in enumerate(pts):
            o = done[pkey(pt)] if pkey(pt) in done else eval_point(f, pt, Rf, B, base); grid.append(o)
            if i % 6 == 0 or i == len(pts) - 1:
                P(f"[{f}] {pkey(pt):34s}: " + summary(o) + f"  [{time.time()-T0:.0f}s {rss():.2f}GB]")
                R_["grid"] = grid; dump(f"local{SUFFIX}_partial.json", RES)
        R_["grid"] = grid
    RES["peak_rss_GB"] = rss(); RES["seconds"] = time.time() - T0; RES["criteria"] = CRIT; RES["mutate"] = MUTATE; RES["note"] = NOTE
    RES["grid_def"] = dict(RJ0=RJ0_GRID, PHS=PHS_GRID, p=P_GRID, ell=ELL_GRID, forms=list(FORMS), as_written=ASW, GCUT=GCUT)
    dump(f"local{SUFFIX}.json", RES)
    pp = os.path.join(PARTS, f"local{SUFFIX}_partial.json")
    if os.path.exists(pp): os.remove(pp)
    P(f"local{SUFFIX} done {RES['seconds']:.0f} s, peak RSS {RES['peak_rss_GB']:.2f} GB")

if __name__ == "__main__":
    P(f"PJ1 {WHICH}{SUFFIX}. Criteria {CRIT}. R_cmb = {RF['canonical']:.6f} / {RF['alt']:.6f} (4.4 reported). "
      f"grid: R_J0 {RJ0_GRID} Mpc x Phi_* {PHS_GRID} x p {P_GRID} x ell {ELL_GRID} kpc x forms {FORMS}. {NOTE}; footings never pooled; adopts nothing.")
    if WHICH == "local": run_local()
    elif WHICH == "web":
        from pj1_web import run_web; run_web(RES)
    elif WHICH == "cmb":
        from pj1_cmb import run_cmb; run_cmb(RES)
    elif WHICH == "bullet":
        from pj1_bullet import run_bullet; run_bullet(RES)
    P(f"Adopts nothing. {NOTE}.")

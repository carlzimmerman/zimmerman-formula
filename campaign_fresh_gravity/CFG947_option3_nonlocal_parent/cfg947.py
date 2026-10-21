"""CFG947 -- option 3: a non-local (causal) parent whose non-relativistic limit is the class-A engine.
Criteria: FROZEN_CRITERIA.md (9c683a634, committed alone first); AMENDMENT_A1_pre_result.md (fad3a6b86, pre-result).
Run (one core, one process, < 1 GB):
    CFG947_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg947.py      -> cfg947_K.out, cfg947_results_K.json
    CFG947_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg947.py     -> cfg947_MUTATE.out, cfg947_results_MUTATE.json
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg947.py                     -> cfg947.out, cfg947_results.json (K + main)
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite).
kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG947_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG947_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
OUT = []; RES = {"lane": "CFG947", "criteria": "9c683a634", "amendment_A1": "fad3a6b86", "mutate": MUT, "stage": STAGE,
                 "checks": {}}
T0 = time.time(); RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg947_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg947{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def rss_guard(where=""):
    r = rss_val()
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)
    return r


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def is0(e):
    return sp.simplify(sp.expand(e)) == 0


# ================================================================================================ constants (read-only inputs)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # footings, nu_mono, SPARC loader (read-only)
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC, KPC = C4.G_SI, C4.C_SI, C4.MSUN, C4.PC, C4.KPC
K_SI = 4 * math.pi * G_SI
RHO_LAMBDA = C4.RHO_LAMBDA
MSUN847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's constants (as CFG938 / CFG941)
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0),
          ("cluster", 1.5e14, 1000.0)]
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]  # CFG882 Plummer dwarfs (M_sun, pc)
HOST938 = 6e10; RHOST = (50.0, 100.0, 250.0)                          # CFG938 S8 / CFG941 host (M_sun), radii (kpc)
# ---- the class-A engine's own constants and census (cfg650_pm.py, read with the Read tool; values verbatim)
OM_B, OM_C = 0.02237, 0.1200; FB = OM_B / (OM_B + OM_C)
GE, MSE, MPCE, HE = 6.674e-11, 1.989e30, 3.0857e22, 0.674            # x_supply's own constants
RMIN = 0.78125                                                         # Mpc/h comoving, production (run_650.py)
EPS_SW = 0.077
_dta = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
DTA0 = float(_dta["D"][0]); assert abs(_dta["z"][0]) < 1e-12        # native Delta_ta(z = 0)
RHOM_H = 0.315 * 2.775e11                                               # engine's M_ta density (M_sun/h per (Mpc/h)^3)


def fret_of(lM):                                                        # cfg650_pm.py fret_of, verbatim (FRET_MODE census)
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def M_ta(R, D):                                                         # cfg650_pm.py M_ta (M_sun/h), R in Mpc/h
    return (4 * math.pi / 3) * R ** 3 * D * RHOM_H


def census(Mb_msun):
    """isolated domain: R (= r_ON, Mpc/h) with fret(log M_ta(R)) FB M_ta(R)/0.674 = M_b (the engine's own M_bn definition)."""
    f = lambda lR: fret_of(math.log10(M_ta(math.exp(lR), DTA0))) * FB * M_ta(math.exp(lR), DTA0) / HE - Mb_msun
    lR = brentq(f, math.log(1e-6), math.log(1e3), xtol=1e-14, rtol=1e-14)
    R = math.exp(lR); Mh = M_ta(R, DTA0); fr = fret_of(math.log10(Mh))
    return dict(R=R, fr=fr, Mta_h=Mh, Mta=Mh / HE)


def domain(Mb_msun, a0):
    """E7 edge for an isolated domain, physical metres (engine constants inside x_supply)."""
    c = census(Mb_msun)
    x = c["fr"] * FB / (1 - FB)
    rM = math.sqrt(GE * Mb_msun * MSE / a0)
    r_on = c["R"] / HE * MPCE
    xs = min(rM / math.log1p(x) / r_on, 1.0)
    r_e = xs * r_on
    return dict(c, x=x, rM=rM, r_on=r_on, r_e=r_e, xs=xs, Mc=(1 - FB) * c["Mta"], resolved=c["R"] >= RMIN,
                yE=(rM / r_e) ** 2)


# ---- the law
def law_simple(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def law_mono(gN, a0):
    gN = np.asarray(gN, float)
    return gN * C4.nu_mono(gN / a0)


KERN = {"simple": law_simple, "mono": law_mono}


def nu_of(kern, y):
    return float(KERN[kern](y, 1.0) / y)


def q_edge(dom, kern):
    """q = M_ph(<r_e)/M_c for the point-mass domain, dimensionless: x [nu(y_e) - 1] (constant-free)."""
    return dom["x"] * (nu_of(kern, dom["yE"]) - 1.0)


# ---- NGC 3198 (record SPARC file, Upsilon 0.61 as CFG938/941)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MBR_N = GN_N * R_N ** 2 / G_SI                                          # spherical-equivalent enclosed baryons (kg)
MB_N = MBR_N[-1] / MSUN                                                 # M_sun

P("CFG947  option 3: a non-local causal parent whose NR limit is the class-A engine" + ("   [MUTATE]" if MUT else "")
  + f"   stage={STAGE}")
P("  criteria 9c683a634; A1 fad3a6b86 (pre-result); kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2;  native Delta_ta(0) = {DTA0:.6f};"
  f"  engine f_b = {FB:.6f};  RMIN = {RMIN} Mpc/h")
P(f"  NGC 3198: {len(R_N)} radii to {R_N[-1] / KPC:.2f} kpc, M_b(< last) = {MB_N:.4e} M_sun (Upsilon 0.61)")
RES["inputs"] = dict(DTA0=DTA0, FB=FB, RMIN=RMIN, MB_NGC3198=MB_N, N_radii=int(len(R_N)))

# ================================================================================================ shared sympy
r, G, a0s = sp.symbols("r G a_0", positive=True)
u, gN = sp.symbols("u g_N", positive=True)
KS = 4 * sp.pi * G
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / KS


def EL_static():
    """CFG938's reduced static energy E[M_c] = int[-G(M_b + M_c)^2/(2 r^2) + 4 pi r^2 W_full(G M_c/r^2)] dr, its EL in (u, g_N)."""
    Mc = sp.Function("M_c")(r); Mb = sp.Function("M_b")(r)
    Wf = sp.Lambda(u, Wfull)
    Lr = -G * (Mb + Mc) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wf(G * Mc / r ** 2)
    eq = sp.euler_equations(Lr, [Mc], [r])[0].lhs
    return sp.simplify(eq.subs({Mc: u * r ** 2 / G, Mb: gN * r ** 2 / G}).doit())


# ---- growth machinery: CFG941's Lagrangian route (cfg941.py growth_det / n_from_det, method copied with attribution)
tt = sp.symbols("t", positive=True); al = sp.symbols("alpha")
C2s, Bs = sp.symbols("c_2 b", nonnegative=True)
Kg = sp.Symbol("K", positive=True)
FBr, FCr = sp.Rational(1000, 6364), sp.Rational(5364, 6364)          # matter-era fractions (Omega_c/Omega_b = 5.364)


def growth_det(comp):
    a = tt ** sp.Rational(2, 3); H = sp.Rational(2, 3) / tt; rtot = (sp.Rational(2, 3) / tt ** 2) / Kg
    psis = [sp.Function("psi_" + n)(tt) for n, _, _ in comp]
    rho = [f * rtot for _, f, _ in comp]
    L = sum(sp.Rational(1, 2) * rh * a ** 3 * a ** 2 * sp.diff(ps, tt) ** 2 for rh, ps in zip(rho, psis))
    L += a ** 5 * Kg / 2 * (sum(rh * ps for rh, ps in zip(rho, psis))) ** 2
    tidx = [i for i, c in enumerate(comp) if c[2]]
    if tidx:
        i = tidx[0]; rT = rho[i]
        beta = -Kg * rT / (3 * H)
        L += -a ** 5 * C2s / (2 * Kg) * (-Kg * rT * psis[i] + Bs * beta * sp.diff(psis[i], tt)) ** 2
    eqs = sp.euler_equations(L, psis, tt)
    As = sp.symbols("A0:%d" % len(comp))
    rows = []; homog = True
    for e in eqs:
        ex = e.lhs.subs({ps: A * tt ** al for ps, A in zip(psis, As)}).doit()
        ex = sp.expand(sp.powsimp(sp.expand(ex / tt ** al), force=True))
        pows = set(sp.nsimplify(term.as_coeff_exponent(tt)[1]) for term in sp.Add.make_args(ex))
        homog = homog and len(pows) == 1
        p0 = list(pows)[0]
        rows.append(sp.expand(sp.powsimp(ex / tt ** p0, force=True)))
    M = sp.Matrix([[sp.diff(rw, A) for A in As] for rw in rows])
    return sp.expand(M.det()), homog


def n_from_det(det, subs):
    subs = dict(subs); subs[Kg] = 1
    pol = sp.Poly(sp.expand(det.subs(subs)), al)
    roots = np.roots([complex(sp.N(c_)) for c_ in pol.all_coeffs()])
    rr = [z.real for z in roots if abs(z.imag) < 1e-9]
    return 1.5 * max(rr)


# ---- CFG938 slip (S4 definitions) for the local parent P0 (cfg941.py slip_table('P0') method)
def wfull_x(x):
    if x < 1e-3:
        return x * x / 2 + x ** 3 / 3 + x ** 4 / 4 + x ** 5 / 5 + x ** 6 / 6 + x ** 7 / 7
    return -x - math.log1p(-x)


def slip_P0():
    worst_g = worst_8 = 0.0
    for foot in FOOTS:
        a0 = A0[foot]
        for name, Mb, rk_ in SYS847:
            M = Mb * MSUN847; rr = rk_ * KPC847

            def uat(x):
                g_ = float(law_simple(G_SI * M / x ** 2, a0)); return g_ * a0 / (g_ + a0)
            gn = G_SI * M / rr ** 2; uu = uat(rr); g_ = gn + uu
            W_ = a0 * a0 * wfull_x(uu / a0) / K_SI; Dv = uu / (1 - uu / a0)
            h_ = 1e-5 * rr
            rho_c = ((rr + h_) ** 2 * uat(rr + h_) - (rr - h_) ** 2 * uat(rr - h_)) / (2 * h_) / (K_SI * rr ** 2)
            vc2 = g_ * rr
            for Lpc in (0.0, 24.0, 1000.0):
                ps = math.pi * G_SI * (Lpc * PC) ** 2 * rho_c ** 2
                pr = -W_ + ps; pt = -W_ + Dv * uu / K_SI + ps
                worst_g = max(worst_g, 4 * math.pi * G_SI * rr * abs(pr) / (C_SI ** 2 * g_))
                worst_8 = max(worst_8, 8 * math.pi * G_SI * rr ** 2 * max(abs(pr), abs(pt)) / (C_SI ** 2 * vc2))
    return worst_g, worst_8


# ---- CFG941 hover machinery (cfg941.py satellite_hover, method copied with attribution; tether on = local parent)
GL_X, GL_W = np.polynomial.legendre.leggauss(64)


def plummer_g(M, a, x):
    return G_SI * M * x / (x * x + a * a) ** 1.5


def Rinv(x, a0):
    return 0.5 * (-x + math.sqrt(x * x + 4.0 * x * a0))


def satellite_hover(Mb_sun, a_pc, rkpc, a0, tether=True):
    Mh = HOST938 * MSUN847; rh = rkpc * KPC847
    gbh = G_SI * Mh / rh ** 2; gh = float(law_simple(gbh, a0)); uh = gh - gbh
    M = Mb_sun * MSUN847; a = a_pc * PC
    us_of = lambda x: float(law_simple(plummer_g(M, a, x), a0)) - plummer_g(M, a, x)
    xg = np.logspace(math.log10(0.01 * a), math.log10(100 * a), 801); ug = np.array([us_of(x) for x in xg])
    above = np.where(ug >= uh)[0]
    if len(above) == 0:
        rt = a
    elif above[-1] == len(xg) - 1:
        rt = 100 * a
    else:
        j = above[-1]; rt = brentq(lambda x: us_of(x) - uh, xg[j], xg[j + 1])
    xs = np.logspace(math.log10(1e-4 * a), math.log10(rt), 4001)
    Ms = np.array([us_of(x) * x * x / G_SI for x in xs])
    dM = np.diff(Ms); xm = np.sqrt(xs[1:] * xs[:-1]); usm = np.array([us_of(x) for x in xm])
    mu = GL_X[None, :]; wq = GL_W[None, :] / 2
    wz = uh + usm[:, None] * mu; wmag = np.sqrt(uh ** 2 + usm[:, None] ** 2 + 2 * uh * usm[:, None] * mu)
    wm = np.minimum(wmag, a0 * (1 - 1e-12))
    Tz = (wm ** 2 / (a0 - wm)) * wz / wmag if tether else -(wz)
    Tz_avg = float(np.sum((Tz * wq).sum(axis=1) * dM) / np.sum(dM))
    a_m = -gbh + Tz_avg
    a_s = -(gbh + uh)
    gbs_a = plummer_g(M, a, a)
    efe = (gbs_a + (Rinv(gbh + gbs_a, a0) - uh)) / (gbs_a + Rinv(gbs_a, a0))
    return dict(g_host=gh, ratio=(a_m - a_s) / gh, efe_dex=math.log10(efe), g_bs_at_a=gbs_a, g_bh=gbh)


def efe_global_dex(Mb_sun, a_pc, rkpc, a0, kern):
    """global-QUMOND satellite: [g(g_bh + g_bs) - g(g_bh)]/g(g_bs) at the Plummer radius (CFG925 E2 1-D form)."""
    law = KERN[kern]
    gbh = G_SI * HOST938 * MSUN847 / (rkpc * KPC847) ** 2
    gbs = plummer_g(Mb_sun * MSUN847, a_pc * PC, a_pc * PC)
    return math.log10(float((law(gbh + gbs, a0) - law(gbh, a0)) / law(gbs, a0)))


# ---- SPARC: CFG4 statistic (CFG653 cfg653_filter.gal_resid with Lrule None, method copied; nu_mono)
GALS = None
UC = np.round(np.arange(0.30, 1.2001, 0.05), 2)


def sparc_setup():
    global GALS
    if GALS is None:
        GALS = [dict(name=g["name"], R=g["R"], Vo=g["Vobs"], eV=g["eV"], Vg=g["Vgas"], Vd=g["Vdisk"], Vb=g["Vbul"])
                for g in C4.load_sparc()]
    return GALS


def sparc_rms(a0, pred, label):
    """pred(g, U, GB, Rm, a0) -> predicted g (m/s^2) at the galaxy's radii; returns rms, best Upsilon and diagnostics."""
    G_ = sparc_setup(); KPC_S = 3.0857e19
    diag = {}

    def total(U):
        S = W = 0.0; nbeyond = 0; npts = 0
        for g in G_:
            Rm = g["R"] * KPC_S
            VB2 = np.sign(g["Vg"]) * g["Vg"] ** 2 + U * g["Vd"] ** 2 + 1.4 * U * g["Vb"] ** 2
            GB = VB2 * 1e6 / Rm; GO = (g["Vo"] * 1e3) ** 2 / Rm
            OK = (GB > 0) & (GO > 0) & np.isfinite(GB) & (g["Vo"] > 0)
            w = 1.0 / (np.clip(g["eV"], 1, None) / np.clip(g["Vo"], 1, None)) ** 2
            gp, nb = pred(g, U, GB, Rm, a0)
            nbeyond += nb; npts += int(OK.sum())
            gpf = np.where(gp > 0, gp, 1e-3 * GO)
            rr_ = np.log10(np.where(OK, GO, 1.0)) - np.log10(np.where(OK, gpf, 1.0))
            S += float(np.sum(np.where(OK, w * rr_ ** 2, 0))); W += float(np.sum(np.where(OK, w, 0)))
        return math.sqrt(S / W), nbeyond, npts

    tried = {round(U, 2): total(U) for U in UC}
    Ub = min(tried, key=lambda q: tried[q][0])
    for U in np.round(np.arange(Ub - 0.04, Ub + 0.0401, 0.01), 2):
        if 0.30 <= U <= 1.20 and round(U, 2) not in tried:
            tried[round(U, 2)] = total(U)
    Ub = min(tried, key=lambda q: tried[q][0])
    rms, nb, npts = tried[Ub]
    P(f"     {label:44s}: rms {rms:.5f} dex @ Upsilon {Ub:.2f}; points beyond their edge / outside a domain: {nb} of {npts}")
    return dict(rms=rms, U=float(Ub), n_special=int(nb), n_pts=int(npts))


def pred_local(g, U, GB, Rm, a0):
    return law_mono(np.maximum(GB, 0), a0), 0


def pred_newton(g, U, GB, Rm, a0):
    return GB, 0


def _mb_last(GB, Rm):
    ok = np.where(np.isfinite(GB) & (GB > 0))[0]
    if len(ok) == 0:
        return None
    i = ok[-1]
    return GB[i] * Rm[i] ** 2 / G_SI / MSUN


def pred_classA(mode):
    """mode: 'own' (N1 label-pure / N2-B: law inside r_e, drained shell beyond), 'N3' (law inside r_ON),
    'het0.1' (N1 without M-R: two co-spatial labels 0.9 / 0.1), 'N2E' (RMIN: law OFF when r_ON < RMIN)."""
    def f(g, U, GB, Rm, a0):
        gb = np.maximum(GB, 0)
        mb = _mb_last(GB, Rm)
        if mb is None:
            return law_mono(gb, a0), 0
        dom = domain(mb, a0)
        if mode == "N2E" and not dom["resolved"]:
            return gb.copy(), int(np.sum(GB > 0))
        if mode == "het0.1":
            return law_mono(0.9 * gb, a0) + law_mono(0.1 * gb, a0), 0
        lim = dom["r_on"] if mode == "N3" else dom["r_e"]
        gp = law_mono(gb, a0)
        beyond = Rm > lim
        if beyond.any():
            Mb_ = mb * MSUN; ge = G_SI * Mb_ / lim ** 2
            Mph_e = lim ** 2 * (float(law_mono(ge, a0)) - ge) / G_SI
            gp = np.where(beyond, gb + G_SI * Mph_e / Rm ** 2, gp)
        return gp, int(beyond.sum())
    return f


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
EXK1 = EL_static()
fK1 = sp.lambdify((u, gN, a0s, G), EXK1, "math")
k1 = {}
for foot in FOOTS:
    a0 = A0[foot]; rel = []
    for gn in GN_N:
        grid = a0 * np.unique(np.concatenate((np.logspace(-14, -1e-12, 900), np.linspace(1e-4, 1 - 1e-13, 3000))))
        vals = np.array([fK1(x, gn, a0, G_SI) for x in grid])
        idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) <= 0)[0]
        uu = brentq(lambda x: fK1(x, gn, a0, G_SI), grid[idx[0]], grid[idx[0] + 1], xtol=1e-40, rtol=1e-15, maxiter=800)
        rel.append(abs((gn + uu) / float(law_simple(gn, a0)) - 1))
    k1[foot] = float(max(rel))
P(f"  K1 CFG938 reduced EL: {sp.factor(EXK1)}")
K1 = chk("K1_CFG938_NGC3198_law", all(v < 1e-6 for v in k1.values()),
         f"max |g/g_law - 1| canonical {k1['canonical']:.2e}, alt {k1['alt']:.2e} (CFG938 2.2e-16; line 1e-6)")
RES["K1"] = k1
P("  deriving growth determinant (sympy, CFG941 route) ...")
DET2, HOM2 = growth_det([("b", FBr, False), ("t", FCr, True)])
rss_guard("growth det")
n_s6 = n_from_det(DET2, {C2s: 1, Bs: 0}); n_full = n_from_det(DET2, {C2s: 1, Bs: 1}); n_dust = n_from_det(DET2, {C2s: 0, Bs: 0})
K2 = chk("K2_CFG941_growth_exponents", HOM2 and abs(n_s6 - 0.60954) < 1e-4 and abs(n_full - 0.69433) < 1e-4 and abs(n_dust - 1) < 1e-12,
         f"n(c2=1, no chi-bar) = {n_s6:.6f} (0.60954), n(c2=1, chi-bar) = {n_full:.6f} (0.69433), n(c2=0) = {n_dust:.12f}")
RES["K2"] = dict(n_s6=n_s6, n_full=n_full, n_dust=n_dust)
P("  K3 SPARC (CFG4 statistic, nu_mono):")
k3 = {}
for foot in FOOTS:
    k3[f"local|{foot}"] = sparc_rms(A0[foot], pred_local, f"local law {foot}")
    k3[f"newton|{foot}"] = sparc_rms(A0[foot], pred_newton, f"Newton {foot}")
rss_guard("K3")
ref3 = {"canonical": (0.1003, 0.61), "alt": (0.0991, 0.57)}
K3 = chk("K3_CFG653_CFG4_headline", all(abs(k3[f"local|{f}"]["rms"] - ref3[f][0]) <= 1.5e-4 and abs(k3[f"local|{f}"]["U"] - ref3[f][1]) < 1e-9
                                        and abs(k3[f"newton|{f}"]["rms"] - 0.2755) <= 1e-3 for f in FOOTS),
         f"local {k3['local|canonical']['rms']:.5f} @ {k3['local|canonical']['U']:.2f} / {k3['local|alt']['rms']:.5f} @ "
         f"{k3['local|alt']['U']:.2f} (0.1003 @ 0.61 / 0.0991 @ 0.57); Newton {k3['newton|canonical']['rms']:.4f} / "
         f"{k3['newton|alt']['rms']:.4f} (0.2755)")
RES["K3"] = k3
wg0, w80 = slip_P0()
K4 = chk("K4_CFG938_slip", abs(w80 / 1.539799903790011e-05 - 1) < 0.02, f"worst s_847 = {w80:.4e} (1.5398e-5), s_grad = {wg0:.3e}")
hov = {}
for foot in FOOTS:
    for nm, Mb, apc in HOSTS882:
        for rk in RHOST:
            hov[f"{foot}|{nm}|{rk:.0f}"] = satellite_hover(Mb, apc, rk, A0[foot], tether=True)
rat = [v["ratio"] for v in hov.values()]; efd = [v["efe_dex"] for v in hov.values()]
K5 = chk("K5_CFG941_hover_and_EFE", abs(min(rat) - 1.017) < 0.005 and abs(max(rat) - 1.107) < 0.005 and abs(min(efd) + 0.73) < 0.01
         and abs(max(efd) + 0.10) < 0.01,
         f"tethered Delta a/g_host in [{min(rat):.4f}, {max(rat):.4f}] (1.017-1.107); EFE in [{min(efd):.3f}, {max(efd):.3f}] dex (-0.73..-0.10)")
RES["K5"] = {k: dict(ratio=v["ratio"], efe_dex=v["efe_dex"]) for k, v in hov.items()}
K_ALL = K1 and K2 and K3 and K4 and K5
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> main classes VOID'}")
RES["K_all"] = K_ALL
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)


# ================================================================================================ static class-A configuration (NGC 3198)
def static_ngc(kern, a0, profile, rule):
    """rule: 'E7' (class-A edge, q from E7 and the cap), 'root' (diagnostic: edge = the kernel's own supply root, q = 1),
    'N3' (gate s = 1 inside r_ON: no clip, no edge), 'none' (no source: N2-E below RMIN).  profile: 'PS', 'PI', 'PX'."""
    law = KERN[kern]
    glaw = law(GN_N, a0); Mph = R_N ** 2 * (glaw - GN_N) / G_SI
    dom = domain(MB_N, a0)
    if rule == "none":
        Mg = MBR_N + (Mph if profile == "PI" else (2 * Mph if profile == "PX" else 0 * Mph))
        g = G_SI * Mg / R_N ** 2
        return float(np.max(np.abs(g / glaw - 1))), dict(q=None)
    if rule == "N3":
        g = G_SI * (MBR_N + Mph) / R_N ** 2
        return float(np.max(np.abs(g / glaw - 1))), dict(q=None, inside=bool(np.all(R_N <= dom["r_on"])))
    q = 1.0 if rule == "root" else q_edge(dom, kern)
    capf = 1.0 / q if q > 1 else 1.0
    inside = R_N <= dom["r_e"]
    if profile == "PS":
        Mg = MBR_N + capf * Mph
    elif profile == "PI":
        Mg = MBR_N + Mph                                                 # rho_c = rho_ph: e = 0, the cold carries the law
    else:
        Mg = MBR_N + 2 * Mph                                             # rho_c = 2 rho_ph: e = 0 (clip), excess cold gravitates
    g = G_SI * Mg / R_N ** 2
    return float(np.max(np.abs(g / glaw - 1))), dict(q=q, capf=capf, inside=bool(inside.all()), r_e_kpc=dom["r_e"] / KPC)


def deep_points(kern, a0, rule):
    law = KERN[kern]; dom = domain(MB_N, a0); out = {}
    q = 1.0 if rule == "root" else q_edge(dom, kern); capf = 1.0 / q if (q > 1 and rule != "N3") else 1.0
    lim = dom["r_on"] if rule == "N3" else dom["r_e"]
    for y in (1e-2, 1e-3):
        rr = math.sqrt(G_SI * MB_N * MSUN / (y * a0)); gn = y * a0; gl = float(law(gn, a0))
        ins = rr <= lim
        if rule == "none":                                               # no source (N2-E below RMIN): Newtonian baryons
            g = gn; ins = True
        else:
            g = (gn + capf * (gl - gn)) if ins else float("nan")
        out[f"y={y:g}"] = dict(r_kpc=rr / KPC, inside=bool(ins), dev=(abs(g / gl - 1) if ins else None),
                               V4_over_GMa0=(gl * rr) ** 2 / (G_SI * MB_N * MSUN * a0))
    return out


# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    teeth = {}
    # Mu1: local always-on tether -> D-T returns (growth 0.694, hover ~1, mutual coefficient 0)
    B_, C1_, C2_, k_ = sp.symbols("B C_1 C_2 k", positive=True)
    Lmode = Kg / (4 * k_ ** 2) * ((B_ + C1_ + C2_) ** 2 - C2s * (C1_ + C2_) ** 2)
    mut_coef = sp.simplify(sp.diff(Lmode, C1_, C2_))
    m_teth = sp.simplify(mut_coef.subs(C2s, 1)); m_nl = sp.simplify(mut_coef.subs(C2s, 0))
    teeth["Mu1"] = (abs(n_full - 1) > 1e-3) and (min(rat) >= 0.5) and m_teth == 0 and m_nl != 0
    chk("Mu1_local_tether_brings_back_DT", teeth["Mu1"],
        f"n = {n_full:.5f} (non-local candidates: 1); tethered Delta a/g_host min {min(rat):.4f} (candidates: 0 at monopole order); "
        f"linear-regime C1C2 coefficient: tether {m_teth}, non-local (S = 0 off-domain) {m_nl}")
    # Mu2: time-symmetric kernel -> precursor
    t_, t0_, rr_, c_ = sp.symbols("t t_0 r c", positive=True)
    psi_ret = sp.Heaviside(t_ - t0_ - rr_ / c_) / (4 * sp.pi * rr_)
    psi_adv = sp.Heaviside(t_ - t0_ + rr_ / c_) / (4 * sp.pi * rr_)
    tpre = t0_ - rr_ / (2 * c_)
    pre_ret = sp.simplify(psi_ret.subs(t_, tpre)); pre_sym = sp.simplify(((psi_ret + psi_adv) / 2).subs(t_, tpre))
    frac = sp.simplify(pre_sym * 4 * sp.pi * rr_)
    teeth["Mu2"] = (pre_ret == 0) and float(frac) > 0
    chk("Mu2_time_symmetric_kernel_is_acausal", teeth["Mu2"],
        f"at t = t0 - r/(2c) (before switch-on): retarded {pre_ret}, time-symmetric {pre_sym} = {frac} of the static value")
    # Mu3: zero-sum removed -> S mass created at switch-on (continuity has no solution)
    m3 = {}
    for foot in FOOTS:
        dom = domain(MB_N, A0[foot]); gl = float(law_simple(G_SI * MB_N * MSUN / dom["r_e"] ** 2, A0[foot]))
        gnl = G_SI * MB_N * MSUN / dom["r_e"] ** 2
        m3[foot] = dom["r_e"] ** 2 * (gl - gnl) / G_SI / (MB_N * MSUN)
    teeth["Mu3"] = all(v > 1e-6 for v in m3.values())
    chk("Mu3_no_zero_sum_creates_S_mass", teeth["Mu3"],
        f"uncompensated S mass created at switch-on = M_ph(<r_e)/M_b = {m3['canonical']:.2f} / {m3['alt']:.2f}: d/dt int rho_s != 0, "
        "so del.j_s = -d_t rho_s has no decaying solution")
    # Mu4: global-QUMOND field for a satellite -> EFE
    m4 = [efe_global_dex(Mb, apc, rk, A0[f], kz) for f in FOOTS for _, Mb, apc in HOSTS882 for rk in RHOST for kz in KERN]
    teeth["Mu4"] = max(abs(v) for v in m4) >= 0.05
    chk("Mu4_global_field_EFE_returns", teeth["Mu4"], f"|EFE| up to {max(abs(v) for v in m4):.3f} dex (range {min(m4):.3f}..{max(m4):.3f})")
    # Mu5: q cap removed on a 0.5x starved catchment
    m5 = {}
    for foot in FOOTS:
        dom = domain(MB_N, A0[foot]); qs = 2.0 * q_edge(dom, "simple")
        m5[foot] = dict(q=qs, rho_tot_over_rho_c_uncapped=1 - qs, capped_phantom_fraction=1 / qs)
    teeth["Mu5"] = all(v["rho_tot_over_rho_c_uncapped"] < 0 for v in m5.values())
    chk("Mu5_cap_removed_negative_density", teeth["Mu5"],
        f"starved catchment q = {m5['canonical']['q']:.4f}: uncapped shell rho_tot/rho_c = {m5['canonical']['rho_tot_over_rho_c_uncapped']:.4f}"
        f" (< 0); capped: phantom x {m5['canonical']['capped_phantom_fraction']:.3f} (law deficit inside r_e)")
    RES["MUTATE"] = dict(teeth=teeth, Mu3=m3, Mu5=m5, Mu4_range=[min(m4), max(m4)])
    allb = all(teeth.values())
    P(f"  MUTATE: {'ALL TEETH BITE' if allb else 'A TOOTH DID NOT BITE'}")
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
    sys.exit(1 if allb else 2)

# ================================================================================================ MAIN: structural statements
P("\n==================== STRUCTURAL STATEMENTS ====================")
ST = {}
# ---- T-Z: zero-sum forced by conservation
X4 = sp.symbols("x0:4", real=True)
Qf = {}
for i in range(4):
    for j in range(i + 1, 4):
        Qf[(i, j)] = sp.Function(f"Q{i}{j}")(*X4)
Qm = sp.zeros(4, 4)
for (i, j), f_ in Qf.items():
    Qm[i, j] = f_; Qm[j, i] = -f_
J = [sum(sp.diff(Qm[mu, nu], X4[nu]) for nu in range(4)) for mu in range(4)]
divJ = sp.simplify(sum(sp.diff(J[mu], X4[mu]) for mu in range(4)))
tz, xx, yy, zz = sp.symbols("t x y z", real=True)
Pv = [sp.Function(f"P{c}")(tz, xx, yy, zz) for c in "xyz"]; Mv = [sp.Function(f"M{c}")(tz, xx, yy, zz) for c in "xyz"]
crd = (xx, yy, zz)
rho_s = -sum(sp.diff(Pv[i], crd[i]) for i in range(3))
curlM = [sp.diff(Mv[2], yy) - sp.diff(Mv[1], zz), sp.diff(Mv[0], zz) - sp.diff(Mv[2], xx), sp.diff(Mv[1], xx) - sp.diff(Mv[0], yy)]
js = [sp.diff(Pv[i], tz) + curlM[i] for i in range(3)]
cont = sp.simplify(sp.diff(rho_s, tz) + sum(sp.diff(js[i], crd[i]) for i in range(3)))
Rd, Av = sp.symbols("R_D A", positive=True)
Psph = Av * r * (Rd - r) ** 2                                          # compact radial polarisation, P(R_D) = 0
tot = sp.simplify(sp.integrate(-sp.diff(r ** 2 * Psph, r) / r ** 2 * 4 * sp.pi * r ** 2, (r, 0, Rd)))
# growing class-A domain: int rho_s(t) = lambda M_ph - q(lambda) M_c with q = lambda M_ph / M_c
lam_ = np.linspace(0, 1, 11); dom0 = domain(MB_N, A0["canonical"])
Mph_e = dom0["r_e"] ** 2 * (float(law_mono(G_SI * MB_N * MSUN / dom0["r_e"] ** 2, A0["canonical"])) - G_SI * MB_N * MSUN / dom0["r_e"] ** 2) / G_SI / MSUN
zs = [abs(l * Mph_e - (l * Mph_e / dom0["Mc"]) * dom0["Mc"]) / Mph_e for l in lam_]
ST["T-Z"] = chk("T-Z_zero_sum_forced", divJ == 0 and cont == 0 and tot == 0 and max(zs) < 1e-12,
                f"d_mu d_nu Q^mu nu = {divJ}; d_t rho_s + div j_s = {cont}; compact P: int rho_s dV = {tot}; growing domain "
                f"|int rho_s|/M_ph <= {max(zs):.1e}. With S = 0 on FRW, int rho_s = 0 for all time (no S current leaves a domain)")
# ---- T-M: momentum consistency (A1.1): relocation term R
tsym = sp.symbols("t", real=True); nS = 3
sj = [sp.Function(f"s{j}")(tsym) for j in range(nS)]; xj = [sp.Function(f"x{j}")(tsym) for j in range(nS)]
Dm = sum(s_ * x_ for s_, x_ in zip(sj, xj))
Rrel = sp.simplify(sp.diff(Dm, tsym, 2) - sum(s_ * sp.diff(x_, tsym, 2) for s_, x_ in zip(sj, xj))
                   - sum(sp.diff(s_, tsym, 2) * x_ + 2 * sp.diff(s_, tsym) * sp.diff(x_, tsym) for s_, x_ in zip(sj, xj)))
# E8 two-blob: core weight M_e(t) at 0; blobs -q m_pm at +-X(t), q = M_e/M_c, m_pm = M_c(1 +- eps)/2
Me = sp.Function("M_e")(tsym); Xt = sp.Function("X")(tsym); epsS, McS = sp.symbols("epsilon M_c", positive=True)
mp, mm = McS * (1 + epsS) / 2, McS * (1 - epsS) / 2
sw = [Me, -Me / McS * mp, -Me / McS * mm]; xw = [sp.Integer(0), Xt, -Xt]
R_E8 = sp.simplify(sum(sp.diff(s_, tsym, 2) * x_ + 2 * sp.diff(s_, tsym) * sp.diff(x_, tsym) for s_, x_ in zip(sw, xw)))
R_E8_target = -epsS * (sp.diff(Me, tsym, 2) * Xt + 2 * sp.diff(Me, tsym) * sp.diff(Xt, tsym))
# N3 switch-on: D_s = s(t) C, C = -M_c eps X/3 (uniform gate over a sphere containing the blobs)
st = sp.Function("s")(tsym)
R_N3 = sp.simplify(sp.diff(st * (-McS * epsS * Xt / 3), tsym, 2) - st * sp.diff(-McS * epsS * Xt / 3, tsym, 2))
# numeric: Plummer blobs (G = 1): constant-weight identity sum_j s_j g_tot(x_j) = -F_ms; F_ms itself
def tm_numeric(eps):
    Xb = 5.0
    mat = [(1.0, 0.0, 0.3), ((1 + eps) / 2, Xb, 0.5), ((1 - eps) / 2, -Xb, 0.5)]   # (mass, x, softening): M_b, blobs (M_c = 1)
    Ssec = [(1.0, 0.0, 1.0), (-(1 + eps) / 2, Xb, 0.5), (-(1 - eps) / 2, -Xb, 0.5)]  # (weight, x, softening): M_e, -q m (q = 1)

    def fpair(xi, ai, xj, aj):                                          # field at xi from unit Plummer mass at xj (1-D axis)
        d = xj - xi; a2 = 0.5 * (ai * ai + aj * aj)
        return d / (d * d + a2) ** 1.5
    F_ms = sum(mi * sj_ * fpair(xi, ai, xj_, aj) for mi, xi, ai in mat for sj_, xj_, aj in Ssec)
    gtot_at = lambda x0, a0_: (sum(m_ * fpair(x0, a0_, x_, a_) for m_, x_, a_ in mat if abs(x_ - x0) > 1e-12)
                               + sum(s_ * fpair(x0, a0_, x_, a_) for s_, x_, a_ in Ssec if abs(x_ - x0) > 1e-12))
    # carriers: S weight j moves with the matter at its location; coincident matter-S pairs exert no net force (concentric)
    sg = sum(s_ * gtot_at(x_, a_) for s_, x_, a_ in Ssec)
    return F_ms, sg
tmn = {e: tm_numeric(e) for e in (0.0, 0.01, 0.1, 0.3)}
ident = max(abs(v[0] + v[1]) for v in tmn.values())
# declared smooth histories (implementation choice, A1.1 leaves the history open): M_e(t) = M_e0 (1 - cos(pi t/t_g))/2 with static
# blobs (X = X0); N3: s(t) = (1 - cos(pi t/t_s))/2.  t_g = t_s = t_dyn = sqrt(X0^3/(G M_dom)); M_e0/M_dom = M_c/M_dom = 1/2.
tg, Me0, X0, Gs_, Md = sp.symbols("t_g M_e0 X_0 G_s M_dom", positive=True)
hist = Me0 * (1 - sp.cos(sp.pi * tsym / tg)) / 2
Rmax_E8 = sp.simplify(sp.Abs(R_E8_target.subs({Me: hist, Xt: X0}).doit().subs(tsym, 0)))
Rmax_N3 = sp.simplify(sp.Abs(R_N3.subs({st: (1 - sp.cos(sp.pi * tsym / tg)) / 2, Xt: X0}).doit().subs(tsym, 0)))
scale = {tg: sp.sqrt(X0 ** 3 / (Gs_ * Md)), Me0: Md / 2, McS: Md / 2}
FREF = Gs_ * Md ** 2 / X0 ** 2
rel_E8 = sp.simplify((Rmax_E8 / FREF).subs(scale)); rel_N3 = sp.simplify((Rmax_N3 / FREF).subs(scale))
tm_rel = {e: float(rel_E8.subs(epsS, e)) for e in (0.0, 0.01, 0.1, 0.3)}
n3_rel = {e: float(rel_N3.subs(epsS, e)) for e in (0.0, 0.01, 0.1, 0.3)}
P(f"  T-M declared histories: max |R|/(M_dom g_ref) = {rel_E8} (E8), {rel_N3} (N3 switch-on)")
# verify the N3 constant C = -M_c eps X/3 by quadrature: int_V F_c dV = -oint Phi n dS for a point mass at b inside a sphere
th, wth = np.polynomial.legendre.leggauss(200)
def surf_int(b, Rs):                                                     # oint (1/|x - b|) n_z dS (b on the z axis)
    ct = th; dist = np.sqrt(Rs * Rs + b * b - 2 * Rs * b * ct)
    return 2 * math.pi * Rs * Rs * float(np.sum(wth * ct / dist))
cq = surf_int(0.6, 2.0) / (4 * math.pi * 0.6 / 3)
ST["T-M"] = chk("T-M_relocation_term_nonzero", Rrel == 0 and sp.simplify(R_E8 - R_E8_target) == 0 and R_N3 != 0
                and abs(tmn[0.0][0]) < 1e-14 and abs(tmn[0.3][0]) > 1e-3 and ident < 1e-12 and abs(cq - 1) < 1e-9,
                f"D'' - sum s x'' = sum(s''x + 2 s'x') (identity); E8 two-blob R = {sp.simplify(R_E8)}; N3 switch-on R = {R_N3}; "
                f"Plummer toy: F_ms(eps 0/0.01/0.1/0.3) = {', '.join(f'{tmn[e][0]:.3e}' for e in tmn)}, |sum s g_tot + F_ms| <= {ident:.1e} "
                f"(constant weights conserve); R/(M_dom g_ref) ~ {', '.join(f'{tm_rel[e]:.3f}' for e in tm_rel)} (E8), "
                f"{', '.join(f'{n3_rel[e]:.4f}' for e in n3_rel)} (N3 switch-on) [declared growth time = dynamical time]; "
                f"surface-integral check {cq:.12f}")
RES["T-M"] = dict(F_ms={str(e): v[0] for e, v in tmn.items()}, identity=ident, R_rel_E8=tm_rel, R_rel_N3=n3_rel)
rss_guard("T-M")
# ---- T-E: forced edge, T-R: RMIN threshold
te = {}; te_ok = True
Mgrid = np.logspace(7, 15, 17)
for foot in FOOTS:
    a0 = A0[foot]
    for kz in KERN:
        rows = []
        for Mb in Mgrid:
            dom = domain(float(Mb), a0); ron = dom["r_on"]; gnr = G_SI * Mb * MSUN / ron ** 2
            Mlaw = ron ** 2 * float(KERN[kz](gnr, a0)) / G_SI / MSUN
            ratio = Mlaw / dom["Mta"]; te_ok = te_ok and ratio > 1
            rows.append(dict(Mb=float(Mb), fr=dom["fr"], ratio=ratio, r_e_over_rM=dom["r_e"] * math.sqrt(1) / dom["rM"],
                             x_edge=dom["xs"], q=q_edge(dom, kz), N=(1 - FB) / (dom["fr"] * FB), r_on_Mpc=ron / (1e3 * KPC)))
        te[f"{foot}|{kz}"] = rows
for foot in FOOTS:
    rs = te[f"{foot}|simple"]
    P(f"  T-E [{foot}, simple]: M_law(<r_ON)/M_ta = " + ", ".join(f"{x['ratio']:.2f}" for x in rs[::4])
      + f" at M_b = 1e7, 1e9, 1e11, 1e13, 1e15;  supply N = " + ", ".join(f"{x['N']:.1f}" for x in rs[::4]))
qs_simple = [x["q"] for x in te["canonical|simple"]]; qs_mono = [x["q"] for x in te["canonical|mono"]]
P(f"  edge supply ratio q = x[nu(y_e) - 1]: simple kernel {min(qs_simple):.8f}..{max(qs_simple):.8f}; nu_mono {min(qs_mono):.10f}..{max(qs_mono):.10f}")
ST["T-E"] = chk("T-E_forced_edge", te_ok,
                f"M_law(<r_ON) > M_ta for every M_b in 1e7-1e15 (min ratio {min(x['ratio'] for v in te.values() for x in v):.3f}), both "
                "footings and kernels: a zero-sum source with rho_tot >= 0 must end the law at r_e < r_ON")
RES["T-E"] = te
Mta_thr = M_ta(RMIN, DTA0); fr_thr = fret_of(math.log10(Mta_thr)); Mb_thr = fr_thr * FB * Mta_thr / HE
G_ = sparc_setup(); below = 0; tot_g = 0
for g in G_:
    Rm = g["R"] * 3.0857e19; GB = (np.sign(g["Vg"]) * g["Vg"] ** 2 + 0.61 * g["Vd"] ** 2 + 1.4 * 0.61 * g["Vb"] ** 2) * 1e6 / Rm
    mb = _mb_last(GB, Rm)
    if mb is None: continue
    tot_g += 1; below += int(mb < Mb_thr)
ngc_res = census(MB_N)["R"] >= RMIN
ST["T-R"] = chk("T-R_RMIN_switches_law_off", (not ngc_res) and below > tot_g / 2,
                f"resolved iff r_ON >= {RMIN} Mpc/h <=> M_ta >= {Mta_thr:.3e} M_sun/h <=> M_b >= {Mb_thr:.3e} M_sun (f_r {fr_thr:.2f}; "
                f"footing-independent). NGC 3198 M_b {MB_N:.3e}: r_ON = {census(MB_N)['R']:.3f} Mpc/h -> "
                f"{'resolved' if ngc_res else 'NOT resolved'}; SPARC (Upsilon 0.61): {below} of {tot_g} galaxies below")
RES["T-R"] = dict(Mta_thr=Mta_thr, Mb_thr=Mb_thr, fr_thr=fr_thr, ngc_r_on=census(MB_N)["R"], ngc_resolved=ngc_res,
                  sparc_below=below, sparc_total=tot_g)
# ---- T-X: EFE fork
tx = {f"{f}|{nm}|{rk:.0f}|{kz}": efe_global_dex(Mb, apc, rk, A0[f], kz) for f in FOOTS for nm, Mb, apc in HOSTS882 for rk in RHOST
      for kz in KERN}
ST["T-X"] = chk("T-X_EFE_fork", max(abs(v) for v in tx.values()) > math.log10(1.01),
                f"E4 (global QUMOND) satellite EFE factor {min(tx.values()):.3f}..{max(tx.values()):.3f} dex on H1-H3 x 50/100/250 kpc; "
                "own-domain rule: 0 dex. The two differ by > 1% wherever the host's baryonic field is comparable to the satellite's")
RES["T-X"] = tx
# ---- T-L: label non-additivity
fS, yS = sp.symbols("f y", positive=True)
nu_s = sp.Rational(1, 2) + sp.sqrt(sp.Rational(1, 4) + 1 / yS)
deep = sp.limit(((nu_s.subs(yS, fS * yS) * fS + nu_s.subs(yS, (1 - fS) * yS) * (1 - fS)) * yS) / sp.sqrt(yS), yS, 0)
# (fix after the first main run: sympy cannot reduce sqrt(1/(1-f)) without 0 < f < 1, so the identity is checked at four f values)
deep_ok = all(abs(float(deep.subs(fS, fv)) - (math.sqrt(fv) + math.sqrt(1 - fv))) < 1e-12 for fv in (0.01, 0.1, 0.3, 0.5))
tl = {}
for foot in FOOTS:
    for kz in KERN:
        law = KERN[kz]; gl = law(GN_N, A0[foot])
        for fx in (0.01, 0.1, 0.3, 0.5):
            gh = law((1 - fx) * GN_N, A0[foot]) + law(fx * GN_N, A0[foot])
            tl[f"{foot}|{kz}|f={fx}"] = float(np.max(np.abs(gh / gl - 1)))
        for Nl in (2, 10, 100):
            gh = Nl * law(GN_N / Nl, A0[foot])
            tl[f"{foot}|{kz}|N={Nl}"] = float(np.max(np.abs(gh / gl - 1)))
ST["T-L"] = chk("T-L_label_non_additivity", deep_ok and min(tl.values()) > 1e-6,
                f"deep factor (sympy) = {sp.simplify(deep)}; NGC 3198 max |g/g_law - 1| (canonical, simple): f 0.01/0.1/0.3/0.5 = "
                + ", ".join(f"{tl[f'canonical|simple|f={fx}']:.3f}" for fx in (0.01, 0.1, 0.3, 0.5))
                + "; N 2/10/100 = " + ", ".join(f"{tl[f'canonical|simple|N={n}']:.3f}" for n in (2, 10, 100)))
RES["T-L"] = tl
# ---- N3 transition shell (T-N3, d3) and the class-A static profiles for positivity and slip
RHOM_SI = RHOM_H * HE ** 2 * MSUN / (1e6 * PC) ** 3                     # engine's mean matter density, SI (h = 0.674)


def sys_profile(Mb, a0, kern="simple"):
    dom = domain(Mb, a0); law = KERN[kern]; M = Mb * MSUN
    r_e, r_on, Mc = dom["r_e"], dom["r_on"], dom["Mc"] * MSUN
    A = Mc / (4 * math.pi * (r_on - r_e)) if r_on > r_e else 0.0
    q = q_edge(dom, kern); capf = 1 / q if q > 1 else 1.0; qeff = min(q, 1.0)
    Mph = lambda x: x * x * (float(law(G_SI * M / x ** 2, a0)) - G_SI * M / x ** 2) / G_SI
    Mcold = lambda x: 0.0 if x <= r_e else (4 * math.pi * A * (min(x, r_on) - r_e) + (0 if x <= r_on else (1 - FB) * RHOM_SI * 4 * math.pi / 3 * (x ** 3 - r_on ** 3)))
    return dict(dom=dom, M=M, r_e=r_e, r_on=r_on, Mc=Mc, A=A, q=q, capf=capf, qeff=qeff, Mph=Mph, Mcold=Mcold, law=law)


def n3_transition(Mb, a0, Dlo, kern="simple", npts=4000):
    sp_ = sys_profile(Mb, a0, kern); r_on = sp_["r_on"]
    Dta = DTA0
    r_out = r_on * ((Dta - 1) / (Dlo - 1)) ** (1 / 3)
    rs = np.linspace(r_on * (1 + 1e-9), r_out * (1 - 1e-9), npts)
    out = []
    for x in rs:
        De = 1 + (Dta - 1) * (r_on / x) ** 3; dDe = -3 * (Dta - 1) * r_on ** 3 / x ** 4
        s = min(max((De - Dlo) / (Dta - Dlo), 0), 1); s1 = dDe / (Dta - Dlo)
        h = 1e-6 * x
        rho_ph = (sp_["Mph"](x + h) - sp_["Mph"](x - h)) / (2 * h) / (4 * math.pi * x * x)
        Q = sp_["Mph"](x) - sp_["Mcold"](x)
        rho_c = (1 - FB) * RHOM_SI
        rho_s = s * (rho_ph - rho_c) + s1 * Q / (4 * math.pi * x * x)
        out.append((RHOM_SI + rho_s) / RHOM_SI)
    out = np.array(out)
    return dict(min_rho_tot_over_rhom=float(out.min()), r_out_over_r_on=r_out / r_on,
                Q_over_cold_available=(sp_["Mph"](r_on) - sp_["Mcold"](r_on)) / ((1 - FB) * RHOM_SI * 4 * math.pi / 3 * (r_out ** 3 - r_on ** 3)))


tn3 = {}
for foot in FOOTS:
    for name, Mb, _ in [("NGC3198", MB_N, None)] + SYS847:
        for Dlo in (2.0, 1.1):
            tn3[f"{foot}|{name}|Dlo={Dlo}"] = n3_transition(Mb, A0[foot], Dlo)
ST["T-N3"] = chk("T-N3_domains_forced", all(v["min_rho_tot_over_rhom"] < 0 for k, v in tn3.items() if "Dlo=2.0" in k),
                 "N3 gate (Delta_lo = 2): min total density in the transition / mean matter density = "
                 + ", ".join(f"{k.split('|')[1]} {v['min_rho_tot_over_rhom']:.1f}" for k, v in tn3.items() if k.startswith("canonical") and "Dlo=2.0" in k)
                 + "; broad gate (1.1): " + ", ".join(f"{v['min_rho_tot_over_rhom']:.1f}" for k, v in tn3.items() if k.startswith("canonical") and "Dlo=1.1" in k))
RES["T-N3"] = tn3
rss_guard("T-N3")
# ---- T-F: free fall (monopole order) + retardation bound
tf = {}
for foot in FOOTS:
    a0 = A0[foot]
    for nm, Mb, apc in HOSTS882:
        for rk in RHOST:
            Rh = rk * KPC847; gbh = G_SI * HOST938 * MSUN847 / Rh ** 2; gh = float(law_simple(gbh, a0)); v2 = gh * Rh
            a = apc * PC; gbs = plummer_g(Mb * MSUN847, a, a); gph = float(law_simple(gbs, a0)) - gbs
            tf[f"{foot}|{nm}|{rk:.0f}"] = dict(monopole=0.0, bound=(gph / gh) * max(v2 / C_SI ** 2, gh * a / C_SI ** 2))
tfmax = max(v["bound"] for v in tf.values())
ST["T-F"] = chk("T-F_no_hover", tfmax <= 1e-2,
                f"stars, cold dust (geodesic) and S (carried, conserved) all fall at g_host: Delta a/g_host = 0 at monopole order; retardation "
                f"bound <= {tfmax:.2e} (CFG941 tethered: {min(rat):.3f}-{max(rat):.3f})")
RES["T-F"] = tf

# ================================================================================================ MAIN: tests (a)-(h) per candidate
P("\n==================== TESTS (a)-(h) ====================")
CANDS = ["N1", "N2-E", "N2-B", "N3"]
GR = {c: {} for c in CANDS}
# ---- (a)
P("  (a) static law on NGC 3198 (43 radii) and deep points")
A = {}
for c in CANDS:
    A[c] = {}
    for foot in FOOTS:
        a0 = A0[foot]; dres = domain(MB_N, a0)["resolved"]
        for kz in KERN:
            for prof in ("PS", "PI", "PX"):
                if c == "N3":
                    rule = "N3"
                elif c == "N2-E" and not dres:
                    rule = "none"
                else:
                    rule = "E7"
                dv, info = static_ngc(kz, a0, prof, rule)
                A[c][f"{foot}|{kz}|{prof}"] = dict(dev=dv, **{k: v for k, v in info.items()})
            A[c][f"{foot}|{kz}|deep"] = deep_points(kz, a0, "N3" if c == "N3" else ("none" if (c == "N2-E" and not dres) else "E7"))
            A[c][f"{foot}|{kz}|root_PS"] = static_ngc(kz, a0, "PS", "root")[0]
a1 = {}; a2 = {}
for c in CANDS:
    a1[c] = all(A[c][f"{f}|{k}|{p}"]["dev"] <= 1e-6 for f in FOOTS for k in KERN for p in ("PS", "PI"))
    a2[c] = True
    for f in FOOTS:
        for k in KERN:
            for yk, v in A[c][f"{f}|{k}|deep"].items():
                if c == "N2-E" and not domain(MB_N, A0[f])["resolved"]:
                    a2[c] = False
                elif v["inside"] and v["dev"] is not None:
                    a2[c] = a2[c] and v["dev"] <= 1e-6
for c in CANDS:
    devs = {f"{f}|{k}": (A[c][f"{f}|{k}|PS"]["dev"], A[c][f"{f}|{k}|PI"]["dev"], A[c][f"{f}|{k}|PX"]["dev"]) for f in FOOTS for k in KERN}
    P(f"   {c:5s}: max dev (P-S / P-I / P-X): " + "; ".join(f"{kk} {v[0]:.2e}/{v[1]:.2e}/{v[2]:.2e}" for kk, v in devs.items()))
P(f"   class-A edge q (NGC 3198): simple {A['N1']['canonical|simple|PS']['q']:.8f} / {A['N1']['alt|simple|PS']['q']:.8f}; "
  f"nu_mono {A['N1']['canonical|mono|PS']['q']:.12f} / {A['N1']['alt|mono|PS']['q']:.12f};  r_e = {A['N1']['canonical|simple|PS']['r_e_kpc']:.1f} / "
  f"{A['N1']['alt|simple|PS']['r_e_kpc']:.1f} kpc; diagnostic (edge = the kernel's own supply root): P-S max dev "
  f"{max(A['N1'][f'{f}|{k}|root_PS'] for f in FOOTS for k in KERN):.2e}")
for c in CANDS:
    if c == "N1":                                                       # label-pure needs the merge rule M-R (T-L otherwise)
        g = "CONDITIONAL" if (a1[c] and a2[c]) else "FAIL"
    else:
        g = "PASS" if (a1[c] and a2[c]) else "FAIL"
    GR[c]["a"] = g
    P(f"   (a) {c}: a1 {'PASS' if a1[c] else 'FAIL'}, a2 {'PASS' if a2[c] else 'FAIL'} -> {g}"
      + ("  [N1: label purity needs the merge rule M-R; without it T-L deviations apply]" if c == "N1" else ""))
RES["a"] = A
# ---- (b) FRW
gi_sym = {}; GI = sp.zeros(4, 4)
for i in range(4):
    for j in range(i, 4):
        gi_sym[(i, j)] = sp.Symbol(f"gi{i}{j}", real=True); GI[i, j] = GI[j, i] = gi_sym[(i, j)]
mm_ = sp.Symbol("m", positive=True); t__ = sp.Symbol("t", real=True); af = sp.Function("a", positive=True)(t__)
sqrtg = 1 / sp.sqrt(-GI.det()); Ld = sqrtg * (-mm_ * sp.sqrt(GI[1:, 1:].det()))
Tdn = sp.zeros(4, 4)
for (i, j), s_ in gi_sym.items():
    Tdn[i, j] = Tdn[j, i] = (-2 if i == j else -1) * sp.diff(Ld, s_) / sqrtg
FRW = [-1, af ** -2, af ** -2, af ** -2]
Tm = sp.simplify(sp.diag(*FRW) * Tdn.subs({gi_sym[(i, j)]: (FRW[i] if i == j else 0) for (i, j) in gi_sym}))
rho_d, p_d = sp.simplify(-Tm[0, 0]), sp.simplify(Tm[1, 1])
offd = all(sp.simplify(Tm[i, j]) == 0 for i in range(4) for j in range(4) if i != j)
iso = sp.simplify(Tm[1, 1] - Tm[2, 2]) == 0 and sp.simplify(Tm[1, 1] - Tm[3, 3]) == 0
dmin = min(_dta["D"])
b_ok = offd and iso and p_d == 0 and sp.simplify(rho_d - mm_ / af ** 3) == 0 and dmin > 1 + 3 * EPS_SW
for c in CANDS:
    GR[c]["b"] = "PASS" if b_ok else "FAIL"
chk("b_FRW_S_zero_w0", b_ok, f"dust: rho = {rho_d}, p = {p_d}, isotropic; S = 0 on FRW for every candidate: Delta_ta(z) >= {dmin:.3f} > 1 "
    "(no domain at delta = 0), labels unset, per-domain fields unsourced, N3's mean-removed field 0, lambda_2 = 0 < tau - eps")
del Tdn, Ld, sqrtg
# ---- (c) growth + top-hat
th_ = sp.symbols("theta", positive=True)
dens = sp.Rational(9, 2) * (th_ - sp.sin(th_)) ** 2 / (1 - sp.cos(th_)) ** 3
dta_eds = sp.simplify(dens.subs(th_, sp.pi)); dlin_ta = sp.Rational(3, 5) * (sp.Rational(3, 4)) ** sp.Rational(2, 3) * (sp.pi) ** sp.Rational(2, 3)
thg = np.linspace(1e-3, math.pi - 1e-6, 4000); dfn = sp.lambdify(th_, dens, "numpy")
mono_th = bool(np.all(np.diff(dfn(thg)) > 0))
c_ok = abs(n_dust - 1) < 1e-6 and mono_th and abs(float(dta_eds) - 9 * math.pi ** 2 / 16) < 1e-12
for c in CANDS:
    GR[c]["c"] = "PASS" if c_ok else "FAIL"
chk("c_growth_a1", c_ok, f"S = 0 in the linear regime -> dust growth n = {n_dust:.12f}; top-hat mean density rises monotonically to "
    f"{float(dta_eds):.4f} = 9 pi^2/16 at turnaround (delta_lin = {float(dlin_ta):.4f}): the gate opens only at turnaround (EdS); "
    f"local tether (Mu1): {n_full:.5f}")
# ---- (d)
P("  (d) causality / well-posedness")
t1, t01, r1, c1 = sp.symbols("t t_0 r c", positive=True)
resp = sp.Heaviside(t1 - t01 - r1 / c1) / (4 * sp.pi * r1)
d1_ok = sp.simplify(resp.subs(t1, t01 + r1 / (2 * c1))) == 0
# d2: two-component Jeans with the class-A linear response
w2, k2s, cb2, cc2, Gb, Gc, rb, rc = sp.symbols("omega2 k2 c_b2 c_c2 a_b a_c rho_b rho_c", real=True)
Mdisp = sp.Matrix([[w2 - cb2 * k2s + KS * Gb * rb, KS * Gc * rc], [KS * Gb * rb, w2 - cc2 * k2s + KS * Gc * rc]])
roots_in = sp.solve(Mdisp.det().subs(Gc, 0), w2)
d2_in = all(sp.simplify(sp.limit(rt / k2s, k2s, sp.oo)) in (cb2, cc2) for rt in roots_in)
roots_gen = sp.solve(Mdisp.det(), w2)
num = {cb2: 1.0, cc2: 0.5, Gb: 1.3, Gc: 0.4, rb: 0.2, rc: 1.0, G: 1.0}
lowb = -4 * math.pi * (1.3 * 0.2 + 0.4 * 1.0)
d2_gen = all(all(complex(sp.N(rt.subs(num).subs(k2s, kv))).imag == 0 and complex(sp.N(rt.subs(num).subs(k2s, kv))).real >= lowb - 1e-12
                 for kv in (0.0, 1.0, 10.0, 1e3)) for rt in roots_gen)
d2_ok = d2_in and d2_gen
# d3 positivity
d3 = {}
for c in CANDS:
    okc = True
    for foot in FOOTS:
        a0 = A0[foot]
        for name, Mb, _ in [("NGC3198", MB_N, None)] + SYS847:
            dom = domain(Mb, a0)
            if c == "N3":
                okc = okc and tn3[f"{foot}|{name}|Dlo=2.0"]["min_rho_tot_over_rhom"] >= 0
                continue
            if c == "N2-E" and not dom["resolved"]:
                continue                                                # no source: matter only (rho >= 0)
            for kz in KERN:                                              # shell: (1 - q_eff) rho_c with q_eff = min(q, 1) (the cap)
                qeff = min(q_edge(dom, kz), 1.0); okc = okc and (1 - qeff) >= 0
                xg = np.geomspace(dom["rM"] * 1e-2, dom["r_e"], 400)     # inside r_e: rho_b + capf rho_ph >= 0 <=> M_law(<r) increasing
                Ml = xg ** 2 * KERN[kz](G_SI * Mb * MSUN / xg ** 2, a0)
                okc = okc and bool(np.all(np.diff(Ml) > 0))
        for kz in KERN:                                                  # NGC 3198's extended baryons
            okc = okc and bool(np.all(np.diff(R_N ** 2 * KERN[kz](GN_N, a0)) > 0))
    d3[c] = okc
# d4 Hadamard toys
M1t = 2 * Mta_thr                                                       # M_sun/h, each peak
R1 = (3 * M1t / (4 * math.pi * RHOM_H * (DTA0 - 1))) ** (1 / 3); R12 = 2 ** (1 / 3) * R1


def ron_two(dsep):
    ok_both = dsep <= R12
    return R12 if ok_both else R1


ch_E = abs(ron_two(R12 * 1.01) - ron_two(R12 * 0.99)) / ron_two(R12 * 0.99)
phi = lambda x: math.erf(x / math.sqrt(2)) / x                          # unit Gaussian blob potential (sigma = 1)
phi2 = lambda x, h=1e-4: (phi(x + h) - 2 * phi(x) + phi(x - h)) / h ** 2
xs_ = brentq(phi2, 0.5, 5.0); dc_B = 2 * xs_                            # minima merge when phi''(d/2) = 0
domB = lambda Mb: domain(Mb, A0["canonical"])["r_e"]
Mbt = 1e9
ch_B = abs(domB(2 * Mbt) - domB(Mbt)) / domB(Mbt)                       # two domains (M, M) vs one (2M): edge jump
d4 = {"N1": 0.0, "N2-E": ch_E, "N2-B": ch_B, "N3": 0.0}
P(f"   d4 toys: N2-E largest-R rule: r_ON jumps by {ch_E:.3f} at d = R12 (R12/R1 = 2^(1/3)); N2-B: psi minima merge at d = {dc_B:.4f} L*, "
  f"the domain's edge jumps by {ch_B:.3f}; N1 (rule beta): 0; N3 (gate outer radius): 0")
# d5
d5_id = (divJ == 0 and cont == 0)
RULE = {"N1": tm_rel, "N2-E": tm_rel, "N2-B": tm_rel, "N3": n3_rel}  # each candidate's declared relocation: E8 draw, or N3's switch-on
d5_tm = {c: all(RULE[c][e] == 0 for e in (0.01, 0.1, 0.3)) for c in CANDS}   # conservable iff R = 0 for every eps > 0 (A1.1)
D = {}
for c in CANDS:
    d4ok = d4[c] <= 0.01
    if d1_ok and d2_ok and d3[c] and d5_id and d5_tm[c]:
        D[c] = "PASS" if d4ok else "CONDITIONAL"
    else:
        D[c] = "FAIL"
    GR[c]["d"] = D[c]
    P(f"   (d) {c}: d1 {'PASS' if d1_ok else 'FAIL'}, d2 {'PASS' if d2_ok else 'FAIL'} (0 independent initial data), d3 "
      f"{'PASS' if d3[c] else 'FAIL'}, d4 {'PASS' if d4ok else 'FAIL'} ({d4[c]:.3f}), d5 identities {'PASS' if d5_id else 'FAIL'} / "
      f"relocation {'PASS' if d5_tm[c] else 'FAIL (T-M: R != 0 for eps > 0)'} -> {D[c]}")
RES["d"] = dict(d1=d1_ok, d2=d2_ok, d3=d3, d4=d4, d5_identities=d5_id, d5_relocation=d5_tm, dc_B=dc_B)
# ---- (e) slip
P("  (e) slip on CFG847's systems")


def slip_classA(Mb, rk, a0, cand, prof, Dlo=2.0):
    """isotropic stress completion of S: p(r) = int_r^{outer} rho_s g dr' (zero at the domain's outer boundary);
    P-I: S = 0 inside r_e and the cold's own pressure rho sigma^2 with sigma^2 = v_c^2/2 is used."""
    spf = sys_profile(Mb, a0); M = spf["M"]; rr = rk * KPC847
    if cand == "N2-E" and not spf["dom"]["resolved"]:
        return 0.0, 0.0
    law = spf["law"]; r_e, r_on = spf["r_e"], spf["r_on"]
    gl = lambda x: float(law(G_SI * M / x ** 2, a0))
    if prof == "PI":
        h = 1e-5 * rr; rho_ph = (spf["Mph"](rr + h) - spf["Mph"](rr - h)) / (2 * h) / (4 * math.pi * rr * rr)
        g_ = gl(rr); p = rho_ph * (g_ * rr) / 2
        return 4 * math.pi * G_SI * rr * p / (C_SI ** 2 * g_), 8 * math.pi * G_SI * rr ** 2 * p / (C_SI ** 2 * g_ * rr)
    if cand == "N3":                                                      # M_s(<r) = s(r) Q(r); no edge, gate from r_ON to r_out
        r_out = r_on * ((DTA0 - 1) / (Dlo - 1)) ** (1 / 3)
        sfun = lambda x: 1.0 if x <= r_on else min(max((1 + (DTA0 - 1) * (r_on / x) ** 3 - Dlo) / (DTA0 - Dlo), 0.0), 1.0)
        Ms = lambda x: sfun(x) * (spf["Mph"](x) - spf["Mcold"](x))
        Mg = lambda x: M + spf["Mcold"](x) + Ms(x)
        rho_s = lambda x: (Ms(x * (1 + 1e-6)) - Ms(x * (1 - 1e-6))) / (2e-6 * x) / (4 * math.pi * x * x)
        f1 = lambda x: rho_s(x) * G_SI * Mg(x) / x ** 2
        p = quad(f1, rr, r_on, limit=400)[0] + quad(f1, r_on, r_out, limit=400)[0]
        g_ = G_SI * Mg(rr) / rr ** 2
    else:
        Mgrav = lambda x: (M + spf["capf"] * spf["Mph"](x)) if x <= r_e else (M + spf["capf"] * spf["Mph"](r_e) + (1 - spf["qeff"]) * spf["Mcold"](x))

        def rho_s(x):
            if x <= r_e:
                h = 1e-6 * x
                return spf["capf"] * (spf["Mph"](x + h) - spf["Mph"](x - h)) / (2 * h) / (4 * math.pi * x * x)
            return -spf["qeff"] * spf["A"] / (x * x)
        f1 = lambda x: rho_s(x) * G_SI * Mgrav(x) / x ** 2
        p = quad(f1, rr, r_e, limit=400)[0] + (quad(f1, r_e, r_on, limit=400)[0] if r_on > r_e else 0.0)
        g_ = G_SI * Mgrav(rr) / rr ** 2
    return 4 * math.pi * G_SI * rr * abs(p) / (C_SI ** 2 * g_), 8 * math.pi * G_SI * rr ** 2 * abs(p) / (C_SI ** 2 * g_ * rr)


E = {}
for c in CANDS:
    worst = 0.0; rows = {}
    for foot in FOOTS:
        for name, Mb, rk in SYS847:
            for prof in ("PS", "PI"):
                sg_, s8_ = slip_classA(Mb, rk, A0[foot], c, prof)
                rows[f"{foot}|{name}|{prof}"] = dict(s_grad=sg_, s_847=s8_); worst = max(worst, sg_, s8_)
    E[c] = dict(rows=rows, worst=worst)
    GR[c]["e"] = "PASS" if worst <= 1.9e-5 else "FAIL"
    P(f"   (e) {c}: worst slip {worst:.3e} (line 1.9e-5) -> {GR[c]['e']}")
RES["e"] = E
rss_guard("e")
# ---- (f)
P("  (f) satellites")
F = {}
for c in CANDS:
    f1_ok = tfmax <= 1e-2
    if c in ("N1", "N2-B"):
        f2v = 0.0
    else:
        f2v = max(abs(v) for v in tx.values())
    f2_ok = f2v <= 0.01
    F[c] = dict(f1_bound=tfmax, f2_max_abs_dex=f2v)
    GR[c]["f"] = "PASS" if (f1_ok and f2_ok) else "FAIL"
    P(f"   (f) {c}: f1 Delta a/g_host = 0 (+ <= {tfmax:.1e}) {'PASS' if f1_ok else 'FAIL'}; f2 host EFE max |{f2v:.3f}| dex "
      f"{'PASS' if f2_ok else 'FAIL'} -> {GR[c]['f']}")
# N2-B basin supply cap (reported): satellite basin truncated at its Jacobi radius
capB = {}
for foot in FOOTS:
    a0 = A0[foot]
    for nm, Mb, apc in HOSTS882:
        for rk in RHOST:
            dsat = domain(Mb, a0); Rh = rk * KPC847
            Mh_dyn = Rh ** 2 * float(law_simple(G_SI * HOST938 * MSUN847 / Rh ** 2, a0)) / G_SI
            Msat = dsat["Mta"] * MSUN
            rJ = Rh * (Msat / (3 * Mh_dyn)) ** (1 / 3)
            supply = 0.0 if rJ <= dsat["r_e"] else dsat["Mc"] * MSUN * (min(rJ, dsat["r_on"]) - dsat["r_e"]) / (dsat["r_on"] - dsat["r_e"])
            rlim = min(rJ, dsat["r_e"]); gnl = G_SI * Mb * MSUN / rlim ** 2
            demand = rlim ** 2 * (float(law_simple(gnl, a0)) - gnl) / G_SI
            capB[f"{foot}|{nm}|{rk:.0f}"] = dict(r_J_kpc=rJ / KPC, r_e_kpc=dsat["r_e"] / KPC, retained=min(1.0, supply / demand) if demand > 0 else 1.0)
P("   N2-B basin cap (reported): phantom retained fraction " + ", ".join(f"{k}: {v['retained']:.2f}" for k, v in capB.items() if k.startswith("canonical")))
RES["f"] = dict(F=F, capB=capB)
# ---- (g)
EQ = ["E1 universal -grad Phi", "E2 S = e - comp on catchments", "E3 balls of r_ON about mesh peaks, r_ON >= RMIN",
      "E4 pointwise QUMOND of the GLOBAL retained field", "E5 tidal switch", "E6 deficit clip", "E7 edge x_supply",
      "E8 zero-sum draw prop. rho_c, cap", "E9 census f_ret, M2 latch", "E10 M3 re-placement", "E11 refresh cadence"]
GTAB = {
    "N1": ["R", "R", "D: latched labels at L*, no RMIN, no balls", "D: own-domain phantom (no EFE)", "R", "R", "R", "R",
           "R (M2 = a latch, natural)", "R", "discretisation"],
    "N2-E": ["R"] * 10 + ["discretisation"],
    "N2-B": ["R", "R", "D: watershed basins of L*-smoothed psi, no RMIN", "D: own-domain phantom (no EFE)", "R", "R", "R", "R",
             "R (M2 latch added)", "R", "discretisation"],
    "N3": ["R", "D: S nonzero wherever the smooth gate is on", "D: no domains", "R (global, mean removed)", "R (in s)",
           "D: no clip (cold active mass replaced by s rho_ph everywhere in the gate)", "D: no edge", "D: compensation by grad s, not a draw prop. rho_c",
           "D: no per-domain census", "R", "discretisation"],
}
for c in CANDS:
    ndiff = sum(1 for x in GTAB[c] if x.startswith("D"))
    GR[c]["g"] = "PASS" if ndiff == 0 else "FAIL"
    P(f"   (g) {c}: {ndiff} engine equations differ -> {GR[c]['g']}" + ("" if ndiff == 0 else " (unquantified -> transfer not established)"))
RES["g"] = dict(EQ=EQ, table=GTAB)
# ---- (h)
P("  (h) CFG653's constraints: h1 SPARC (CFG4 statistic, nu_mono)")
H = {}
base = {f: k3[f"local|{f}"]["rms"] for f in FOOTS}
for c, mode in (("N1", "own"), ("N2-B", "own"), ("N3", "N3"), ("N2-E", "N2E")):
    H[c] = {}
    for foot in FOOTS:
        H[c][foot] = sparc_rms(A0[foot], pred_classA(mode), f"{c} {foot}")
H["N1_noMR"] = {foot: sparc_rms(A0[foot], pred_classA("het0.1"), f"N1 without M-R (f = 0.1) {foot}") for foot in FOOTS}
rss_guard("h1")


def gate_a(rm, U, b):
    d = rm - b
    if d <= 0.005 and 0.50 <= U <= 0.80: return "PASS"
    if d <= 0.010: return "TENSION"
    return "FAIL"


h1 = {c: all(gate_a(H[c][f]["rms"], H[c][f]["U"], base[f]) == "PASS" for f in FOOTS) for c in CANDS}
h1_noMR = {f: gate_a(H["N1_noMR"][f]["rms"], H["N1_noMR"][f]["U"], base[f]) for f in FOOTS}
z_newton = {"canonical": (1.0 - 1.0750) / 0.0550, "alt": (1.0 - 1.0775) / 0.0512}
h2 = {c: "PASS(can)/TENSION(alt): QUMOND-EFE binaries, CFG653 local-EFE 1.179 (+1.3) / 1.244 (+2.3)" for c in CANDS}
h3 = {c: ("PASS (isolated phantom, CFG478 chi2 0.7/5)" if c in ("N1", "N2-B") else "FAIL (EFE, CFG478 61-107/5)") for c in CANDS}
h4 = True
for c in CANDS:
    ok = h1[c] and h3[c].startswith("PASS") and h4
    if c == "N1" and ok:
        GR[c]["h"] = "CONDITIONAL"                                      # needs M-R (label purity); without it see h1_noMR
    else:
        GR[c]["h"] = "PASS" if ok else "FAIL"
    P(f"   (h) {c}: h1 {'PASS' if h1[c] else 'FAIL'} ({H[c]['canonical']['rms']:.4f} / {H[c]['alt']['rms']:.4f} vs local "
      f"{base['canonical']:.4f} / {base['alt']:.4f}); h2 {h2[c].split(':')[0]}; h3 {h3[c]}; h4 PASS -> {GR[c]['h']}")
P(f"   N1 without M-R (co-spatial labels 0.9/0.1): {h1_noMR}; Newtonian binaries (if a host had no phantom): z {z_newton['canonical']:.2f} / {z_newton['alt']:.2f}")
RES["h"] = dict(H=H, h1=h1, h1_noMR=h1_noMR, h2=h2, h3=h3, h4=h4, z_newton=z_newton)

# ================================================================================================ classes
P("\n==================== CLASSES ====================")
CLASS = {}
for c in CANDS:
    gs = GR[c]
    if any(gs[t] == "FAIL" for t in "abcdefgh"):
        CLASS[c] = "NOT VIABLE"
    elif all(gs[t] == "PASS" for t in "abcdefgh"):
        CLASS[c] = "VIABLE"
    else:
        CLASS[c] = "VIABLE-WITH-COST"
    fails = [t for t in "abcdefgh" if gs[t] == "FAIL"]
    extra = "  [a non-local theory, not class A's parent]" if fails == ["g"] else ""
    P(f"  {c:5s}: " + " ".join(f"{t}:{gs[t]}" for t in "abcdefgh") + f"  -> {CLASS[c]}{extra}")
generic = ST["T-M"] and ST["T-X"] and ST["T-R"]
if any(v == "VIABLE" for v in CLASS.values()):
    OVER = "NON-LOCAL PARENT FOUND"
elif any(v == "VIABLE-WITH-COST" for v in CLASS.values()):
    OVER = "CONDITIONAL"
elif generic:
    OVER = "NO-GO"
else:
    OVER = "NO CANDIDATE PASSES"
P(f"  OVERALL: {OVER}  (generic statements T-M {ST['T-M']}, T-R {ST['T-R']}, T-X {ST['T-X']}; K controls {'ALL PASS' if K_ALL else 'FAIL -> VOID'})")
RES["grades"] = GR; RES["classes"] = CLASS; RES["overall"] = OVER if K_ALL else "VOID (K failed)"; RES["structural"] = ST
dump()
P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")

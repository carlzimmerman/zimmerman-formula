"""CFG955 -- is the class-A engine the coarse-grained limit of a kinetic theory of relaxing cold dust?
Criteria: FROZEN_CRITERIA.md (903cd8f1d, committed alone first).
Run (one core, one process, < 1 GB):
    CFG955_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg955.py      -> cfg955_K.out, cfg955_results_K.json
    CFG955_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg955.py     -> cfg955_MUTATE.out, cfg955_results_MUTATE.json
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg955.py                     -> cfg955.out, cfg955_results.json (K + main)
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite).
Readings: K-rho (density target) and K-T (local Maxwellian at the own-domain monopole Jeans temperature; primary).
kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib, csv
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import PchipInterpolator

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG955_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG955_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
CRIT = "903cd8f1d"; AMEND_A1 = "d11d47794"
OUT = []; RES = {"lane": "CFG955", "criteria": CRIT, "amendment_A1": AMEND_A1, "mutate": MUT, "stage": STAGE, "checks": {}}
T0 = time.time(); RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.ndarray):
        return jsonable(x.tolist())
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, float) and not math.isfinite(x):
        return str(x)
    return x


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(jsonable(RES), open(os.path.join(HERE, f"cfg955_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg955{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def rss_guard(where=""):
    r = rss_val()
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)
    return r


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


# ================================================================================================ constants (read-only inputs)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # footings, nu_mono, SPARC loader (read-only)
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC, KPC = C4.G_SI, C4.C_SI, C4.MSUN, C4.PC, C4.KPC
K_SI = 4 * math.pi * G_SI
GYR_S = 3.15576e16
MSUN847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's constants (as CFG938 / CFG941 / CFG947)
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0),
          ("cluster", 1.5e14, 1000.0)]
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]  # CFG882 Plummer dwarfs (M_sun, pc)
HOST938 = 6e10; RHOST = (50.0, 100.0, 250.0)
EPS_B = {"canonical": 0.344, "alt": 0.317}; DELTA_C = 0.082             # CFG945 bounds
# ---- the class-A engine's own constants and census (cfg650 engine, values as copied by CFG947, verbatim)
OM_B, OM_C = 0.02237, 0.1200; FB = OM_B / (OM_B + OM_C)
GE, MSE, MPCE, HE = 6.674e-11, 1.989e30, 3.0857e22, 0.674
RMIN = 0.78125
_dta = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
DTA0 = float(_dta["D"][0]); assert abs(_dta["z"][0]) < 1e-12
RHOM_H = 0.315 * 2.775e11


def fret_of(lM):                                                        # engine census (CFG947 copy)
    if lM < 12.5: f = 0.10
    elif lM < 13.5: f = 0.10 + 0.45 * (lM - 12.5)
    else: f = min(0.55 + 0.30 * (lM - 13.5), 0.90)
    return min(f, 1.0)


def M_ta(R, D):
    return (4 * math.pi / 3) * R ** 3 * D * RHOM_H


def census(Mb_msun):
    f = lambda lR: fret_of(math.log10(M_ta(math.exp(lR), DTA0))) * FB * M_ta(math.exp(lR), DTA0) / HE - Mb_msun
    lR = brentq(f, math.log(1e-6), math.log(1e3), xtol=1e-14, rtol=1e-14)
    R = math.exp(lR); Mh = M_ta(R, DTA0); fr = fret_of(math.log10(Mh))
    return dict(R=R, fr=fr, Mta_h=Mh, Mta=Mh / HE)


def domain(Mb_msun, a0):
    """CFG947 domain(): E7 edge for an isolated domain, physical metres (engine constants inside x_supply)."""
    c = census(Mb_msun)
    x = c["fr"] * FB / (1 - FB)
    rM = math.sqrt(GE * Mb_msun * MSE / a0)
    r_on = c["R"] / HE * MPCE
    xs = min(rM / math.log1p(x) / r_on, 1.0)
    r_e = xs * r_on
    return dict(c, x=x, rM=rM, r_on=r_on, r_e=r_e, xs=xs, Mc=(1 - FB) * c["Mta"], resolved=c["R"] >= RMIN,
                yE=(rM / r_e) ** 2)


def law_simple(gN, a0):
    gN = np.asarray(gN, float)
    return 0.5 * (gN + np.sqrt(gN * gN + 4.0 * gN * a0))


def law_mono(gN, a0):
    gN = np.asarray(gN, float)
    return gN * C4.nu_mono(gN / a0)


KERN = {"simple": law_simple, "mono": law_mono}


def dlaw(kern, gN, a0):
    """d g / d g_N: analytic for the simple law, central difference in ln g_N for nu_mono."""
    gN = np.asarray(gN, float)
    if kern == "simple":
        return 0.5 * (1.0 + (gN + 2 * a0) / np.sqrt(gN * gN + 4 * gN * a0))
    h = 1e-5
    return (law_mono(gN * math.exp(h), a0) - law_mono(gN * math.exp(-h), a0)) / (gN * (math.exp(h) - math.exp(-h)))


# ---- NGC 3198 (record SPARC file, Upsilon 0.61 as CFG938/941/947)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MBR_N = GN_N * R_N ** 2 / G_SI
MB_N = MBR_N[-1] / MSUN

P("CFG955  kinetic parent of the class-A engine (relaxing cold dust)" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P(f"  criteria {CRIT}; kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2; native Delta_ta(0) = {DTA0:.6f}; engine f_b = {FB:.6f}")
P(f"  NGC 3198: {len(R_N)} radii to {R_N[-1] / KPC:.2f} kpc, M_b(< last) = {MB_N:.4e} M_sun (Upsilon 0.61)")

# ================================================================================================ shared sympy (CFG938 / CFG941 machinery, copied from CFG947)
r, G, a0s = sp.symbols("r G a_0", positive=True)
u, gN = sp.symbols("u g_N", positive=True)
KS = 4 * sp.pi * G
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / KS


def EL_static():
    Mc = sp.Function("M_c")(r); Mb = sp.Function("M_b")(r)
    Wf = sp.Lambda(u, Wfull)
    Lr = -G * (Mb + Mc) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wf(G * Mc / r ** 2)
    eq = sp.euler_equations(Lr, [Mc], [r])[0].lhs
    return sp.simplify(eq.subs({Mc: u * r ** 2 / G, Mb: gN * r ** 2 / G}).doit())


tt = sp.symbols("t", positive=True); al = sp.symbols("alpha")
C2s, Bs = sp.symbols("c_2 b", nonnegative=True)
Kg = sp.Symbol("K", positive=True)
FBr, FCr = sp.Rational(1000, 6364), sp.Rational(5364, 6364)


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


def efe_global_dex(Mb_sun, a_pc, rkpc, a0, kern):
    """global-QUMOND satellite: [g(g_bh + g_bs) - g(g_bh)]/g(g_bs) at the Plummer radius (CFG947 / CFG925 E2 1-D form)."""
    law = KERN[kern]
    gbh = G_SI * HOST938 * MSUN847 / (rkpc * KPC847) ** 2
    a = a_pc * PC
    gbs = G_SI * Mb_sun * MSUN847 * a / (2 * a * a) ** 1.5
    return math.log10(float((law(gbh + gbs, a0) - law(gbh, a0)) / law(gbs, a0)))


# ---- SPARC (CFG947's CFG4 statistic, copied)
GALS = None
UC = np.round(np.arange(0.30, 1.2001, 0.05), 2)


def sparc_setup():
    global GALS
    if GALS is None:
        GALS = [dict(name=g["name"], R=g["R"], Vo=g["Vobs"], eV=g["eV"], Vg=g["Vgas"], Vd=g["Vdisk"], Vb=g["Vbul"])
                for g in C4.load_sparc()]
    return GALS


def sparc_rms(a0, pred, label):
    G_ = sparc_setup(); KPC_S = 3.0857e19

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
    P(f"     {label:44s}: rms {rms:.5f} dex @ Upsilon {Ub:.2f}; points beyond their edge: {nb} of {npts}")
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


def pred_own(g, U, GB, Rm, a0):
    """K-T relaxed state: every galaxy relaxed in its own domain = law inside its own r_e, the edge-truncated field beyond
    (CFG947 pred_classA('own'), copied)."""
    gb = np.maximum(GB, 0)
    mb = _mb_last(GB, Rm)
    if mb is None:
        return law_mono(gb, a0), 0
    dom = domain(mb, a0)
    lim = dom["r_e"]
    gp = law_mono(gb, a0)
    beyond = Rm > lim
    if beyond.any():
        Mb_ = mb * MSUN; ge = G_SI * Mb_ / lim ** 2
        Mph_e = lim ** 2 * (float(law_mono(ge, a0)) - ge) / G_SI
        gp = np.where(beyond, gb + G_SI * Mph_e / Rm ** 2, gp)
    return gp, int(beyond.sum())


# ================================================================================================ SPHERICAL SHELL TOY (CFG935 harness form)
TG, TA0, TMB, TAB = 1.0, 1.0, 1.0, 1.0
RSTAR, RCAT, NPT = 10.0, 30.0, 10000
SEED_T = 955
T_RMIN, T_DTMAX, T_CA, T_EPS = 1e-3, 0.02, 0.03, 0.02
ALPHA = 1.0
DT_RELAX = 0.05            # relaxation cadence (implementation choice, fixed before the first run; disclosed)


def t_Mb(r):
    r = np.asarray(r, float); return TMB * r ** 3 / (r * r + TAB * TAB) ** 1.5


def t_Phib(r):
    r = np.asarray(r, float); return -TG * TMB / np.sqrt(r * r + TAB * TAB)


def t_num1(y):
    y = np.asarray(y, float); return (2.0 / y) / (1.0 + np.sqrt(1.0 + 4.0 / y))


def t_Mph(r):
    r = np.asarray(r, float); Mb = t_Mb(r); y = TG * Mb / (r * r * TA0); return Mb * t_num1(y)


T_MC = float(t_Mph(RSTAR)); T_MU = T_MC / NPT
T_EDGE = 2 * math.pi * math.sqrt(RSTAR ** 3 / (TG * (TMB + T_MC)))
T_RT = np.geomspace(1e-5, 1e4, 400001)
T_MT = t_Mph(T_RT)
_LRT, _LMT = np.log(T_RT), np.log(T_MT)


def t_Minv(m):
    return np.exp(np.interp(np.log(np.asarray(m, float)), _LMT, _LRT))


def t_law_jeans_sigma2(r):
    """CFG935's law_jeans_sigma2 (copied): isotropic Jeans sigma^2 of rho_ph in g = G(Mb + Mph)/r^2, truncated at r_*."""
    sel = T_RT <= RSTAR
    rr = T_RT[sel]; MM = T_MT[sel]
    rho = np.gradient(MM, rr) / (4 * np.pi * rr ** 2)
    g = TG * (t_Mb(rr) + MM) / rr ** 2
    integ = rho * g
    p = np.concatenate([np.cumsum((0.5 * (integ[1:] + integ[:-1]) * np.diff(rr))[::-1])[::-1], [0.0]])
    return np.interp(r, rr, p / rho)


def _tj_table():
    """This lane's T_J on the toy: exact phantom density (analytic dM_ph/dr) and DOP853 quadrature of int rho g, P(r_*) = 0."""
    def Mph_r(rr):
        return float(t_Mph(rr))

    def dMph(rr):
        Mb = float(t_Mb(rr)); dMb = 3 * TMB * TAB ** 2 * rr ** 2 / (rr * rr + TAB * TAB) ** 2.5
        gn = TG * Mb / rr ** 2; dgn = TG * dMb / rr ** 2 - 2 * TG * Mb / rr ** 3
        g = 0.5 * (gn + math.sqrt(gn * gn + 4 * gn * TA0)); dg = 0.5 * (1 + (gn + 2 * TA0) / math.sqrt(gn * gn + 4 * gn * TA0))
        return (2 * rr * (g - gn) + rr * rr * (dg - 1) * dgn) / TG
    lr = np.linspace(math.log(1e-4), math.log(RSTAR), 4001)
    rr = np.exp(lr)
    rho = np.array([dMph(x) for x in rr]) / (4 * np.pi * rr ** 2)
    gl = TG * (t_Mb(rr) + t_Mph(rr)) / rr ** 2

    def rhs(l, y):
        x = math.exp(l)
        return [-x * dMph(x) / (4 * math.pi * x * x) * TG * (float(t_Mb(x)) + Mph_r(x)) / x ** 2]
    sol = solve_ivp(rhs, (lr[-1], lr[0]), [0.0], method="DOP853", rtol=1e-12, atol=1e-16, dense_output=True)
    assert sol.status == 0, sol.message
    p = sol.sol(lr)[0]
    return rr, p / rho, rho, gl, sol, dMph


_TJ_R, _TJ_T, _TJ_RHO, _, _TJ_SOL, _T_DMPH = _tj_table()


def t_TJ(r):
    r = np.asarray(r, float)
    return np.where(r < RSTAR, np.interp(np.log(np.maximum(r, 1e-4)), np.log(_TJ_R), _TJ_T), 0.0)


def t_ic(ic, rng):
    m = T_MU * (np.arange(NPT) + 0.5)
    if ic == "L":
        r_ = t_Minv(m)
        s = np.sqrt(np.maximum(t_TJ(r_), 0.0))
        v = s * rng.standard_normal(NPT)
        vt = s * np.sqrt(rng.standard_normal(NPT) ** 2 + rng.standard_normal(NPT) ** 2)
        return r_, v, r_ * vt
    if ic == "I":
        r_ = 15.0 * (m / T_MC) ** (1.0 / 3.0)
    elif ic == "S":
        r_ = t_Minv(m / 1.5)
    else:
        raise ValueError(ic)
    vc = np.sqrt(TG * (t_Mb(r_) + m) / r_)
    return r_, np.zeros(NPT), 0.05 * r_ * vc


T_EDGES = np.concatenate([[0.0], np.geomspace(0.05, RCAT, 41)])
T_NB = T_EDGES.size - 1
T_VOLB = 4 * np.pi / 3 * np.diff(T_EDGES ** 3)
T_DMB = np.diff(t_Mb(np.maximum(T_EDGES, 1e-8)))
T_RMID = np.concatenate([[0.5 * T_EDGES[1]], np.sqrt(T_EDGES[1:-1] * T_EDGES[2:])])
T_SEDGES = np.geomspace(0.1 * RSTAR, 0.9 * RSTAR, 17)
T_SVOL = 4 * np.pi / 3 * np.diff(T_SEDGES ** 3)
T_SRHOPH = np.diff(t_Mph(T_SEDGES)) / T_SVOL
T_RM3 = np.array([2.0, 5.0, 8.0])
T_L1E = np.concatenate([[0.0], np.geomspace(0.1, RSTAR, 40)])        # 40 bins for the L1 distance (criteria L1)
T_L1PH = np.diff(t_Mph(np.maximum(T_L1E, 1e-8)))


class ShellSim:
    """K-T relaxation (mode 'KT'), the CFG554 self-consistent target (mode 'self', Mu4), or relaxation off ('off', Mu5)."""

    def __init__(self, ic, mode="KT", tau_fac=1.0):
        self.ic, self.mode, self.tau_fac = ic, mode, tau_fac
        self.rng = np.random.default_rng(SEED_T)
        self.r, self.v, self.L = t_ic(ic, self.rng)
        self.t = 0.0; self.E_R = 0.0; self.nsteps = 0; self.nrelax = 0
        self.flow_cool = 0.0; self.flow_heat = 0.0
        self.nS_tot = 0; self.nS_eff = 0.0
        self.a = self.accel(); self.t_last_relax = 0.0

    def accel(self):
        self.order = np.argsort(self.r, kind="stable")
        self.rank = np.empty(NPT, np.int64); self.rank[self.order] = np.arange(NPT)
        r, k = self.r, self.rank
        a = -TG * t_Mb(r) / r ** 2 - TG * T_MU * (k + 0.5) * r / (r * r + T_EPS * T_EPS) ** 1.5
        return a + self.L ** 2 / r ** 3

    def KE(self):
        return 0.5 * T_MU * float(np.sum(self.v ** 2 + self.L ** 2 / self.r ** 2))

    def V_grav(self):
        return T_MU * float(np.sum(t_Phib(self.r))) - TG * T_MU * T_MU * float(np.sum((self.rank + 0.5) / np.sqrt(self.r ** 2 + T_EPS ** 2)))

    def binned(self):
        r = self.r
        idx = np.searchsorted(T_EDGES, r, side="right") - 1
        inC = (r < RCAT) & (idx >= 0) & (idx < T_NB)
        cnt = np.bincount(idx[inC], minlength=T_NB).astype(float)
        Mcb = T_MU * cnt
        rhoc = Mcb / T_VOLB
        rhom = (T_DMB + Mcb) / T_VOLB
        tau_ff = 1.0 / np.sqrt(4 * np.pi * TG * rhom)
        m_lo = np.concatenate([[0.0], np.cumsum(Mcb)[:-1]])
        gmid = TG * (t_Mb(T_RMID) + m_lo + 0.5 * Mcb) / T_RMID ** 2
        dr = np.diff(T_EDGES)
        col = rhoc * gmid * dr
        pJ = np.cumsum(col[::-1])[::-1] - 0.5 * col
        sigJ2 = np.where(rhoc > 0, pJ / np.where(rhoc > 0, rhoc, 1.0), 0.0)          # CFG554 self-consistent target (Mu4)
        return dict(idx=idx, inC=inC, cnt=cnt, tau_ff=tau_ff, sigJ2=sigJ2)

    def relax(self, Dt):
        if self.mode == "off":
            return
        B = self.binned()
        idx = np.clip(B["idx"], 0, T_NB - 1)
        inside = self.r < RSTAR                                    # relaxation only inside the domain edge r_*
        tau = self.tau_fac * B["tau_ff"] / (2 * ALPHA)            # T1: tau_pi = tau_ff/(2 alpha)
        p = 1.0 - np.exp(-Dt / tau)
        sel = inside & (self.rng.random(NPT) < p[idx])
        if not sel.any():
            return
        ii = idx[sel]
        nS = np.bincount(ii, minlength=T_NB).astype(float)
        vS = np.bincount(ii, weights=self.v[sel], minlength=T_NB) / np.maximum(nS, 1)
        rS = np.bincount(ii, weights=self.r[sel], minlength=T_NB) / np.maximum(nS, 1)
        if self.mode == "KT":
            Tb = t_TJ(rS)
        else:                                                      # 'self' (Mu4): T from the current dust density
            Tb = B["sigJ2"]
        Tb = np.maximum(Tb, 0.0)
        xi = self.rng.standard_normal((3, ii.size))
        xbar = np.bincount(ii, weights=xi[0], minlength=T_NB) / np.maximum(nS, 1)
        sq = np.sqrt(Tb)[ii]
        K0 = self.KE()
        rr = self.r[sel]; L0 = self.L[sel]
        self.v[sel] = vS[ii] + sq * (xi[0] - xbar[ii])            # subset keeps its own mean radial velocity exactly
        self.L[sel] = rr * sq * np.sqrt(xi[1] ** 2 + xi[2] ** 2)
        self.a[sel] += (self.L[sel] ** 2 - L0 ** 2) / rr ** 3
        dK = self.KE() - K0
        self.E_R -= dK
        if dK > 0: self.flow_heat += dK
        else: self.flow_cool += -dK
        self.nrelax += 1
        self.nS_tot += int(sel.sum()); self.nS_eff += float(np.sum(np.where(nS > 0, nS - 1, 0)))

    def choose_dt(self):
        return min(T_DTMAX, T_CA * float(np.min(np.sqrt(self.r / (np.abs(self.a) + 1e-300)))))

    def step(self, dt):
        self.v += 0.5 * dt * self.a
        self.r += dt * self.v
        m = self.r < T_RMIN
        if m.any():
            self.r[m] = 2 * T_RMIN - self.r[m]; self.v[m] = -self.v[m]
        self.a = self.accel()
        self.v += 0.5 * dt * self.a
        self.t += dt; self.nsteps += 1
        if self.t - self.t_last_relax >= DT_RELAX - 1e-12:
            self.relax(self.t - self.t_last_relax); self.t_last_relax = self.t

    def measure(self):
        r = self.r
        cnt, _ = np.histogram(r, bins=T_SEDGES)
        m3 = T_MU * np.array([np.count_nonzero(r < R) for R in T_RM3])
        l1c, _ = np.histogram(r, bins=T_L1E)
        L1 = float(np.sum(np.abs(T_MU * l1c - T_L1PH)) / T_MC)
        K, V = self.KE(), self.V_grav()
        return dict(t=self.t, cnt=cnt.tolist(), m3=m3.tolist(), fesc=float(np.count_nonzero(r > RCAT) / NPT), L1=L1,
                    K=K, V=V, E_R=self.E_R, E_tot=K + V + self.E_R)

    def run(self, t_end, label, wall_cap=None):
        samples = [self.measure()]; e0 = samples[0]
        Eref = abs(e0["K"]) + abs(e0["V"])
        next_s = 1.0; t0 = time.time(); next_log = 100.0
        self.capped_at = None
        while self.t < t_end - 1e-12:
            if wall_cap is not None and time.time() - t0 > wall_cap:      # AMENDMENT A1.1: 30-min wall cap (CFG935 A5 rule)
                self.capped_at = self.t
                print(f"    [{label}] A1.1 wall-clock cap at t {self.t:.2f} ({wall_cap:.0f} s)", flush=True)
                break
            dt = min(self.choose_dt(), t_end - self.t, next_s - self.t + 1e-12)
            self.step(dt)
            if self.t >= next_s - 1e-9:
                samples.append(self.measure()); next_s += 1.0
                if self.t >= next_log - 1e-9:
                    s = samples[-1]
                    print(f"    [{label}] t {self.t:7.1f} steps {self.nsteps:8d} dE/Eref {(s['E_tot'] - e0['E_tot']) / Eref:+.2e} "
                          f"L1 {s['L1']:.3f} fesc {s['fesc']:.3f} wall {time.time() - t0:5.0f}s", flush=True)
                    next_log += 100.0
                    rss_guard(label)
        return samples, Eref


def t_analyse(samples, Eref, t_end):
    ts = np.array([s["t"] for s in samples]); Et = np.array([s["E_tot"] for s in samples])
    eps = float(np.max(np.abs(Et - Et[0])) / Eref)

    def win(lo, hi):
        sel = (ts >= lo * t_end - 1e-9) & (ts <= hi * t_end + 1e-9)
        cnt = np.mean(np.array([samples[i]["cnt"] for i in np.where(sel)[0]]), axis=0)
        m3 = np.mean(np.array([samples[i]["m3"] for i in np.where(sel)[0]]), axis=0)
        rho = T_MU * cnt / T_SVOL
        with np.errstate(divide="ignore"):
            lr = np.log10(rho / T_SRHOPH)
        return dict(D=float(np.median(lr)), m3=m3.tolist(), lr=lr.tolist())
    W1, W2 = win(0.50, 0.75), win(0.75, 1.0)
    D, dD = W2["D"], W2["D"] - W1["D"]
    on_law = bool(np.isfinite(D) and abs(D) <= 0.1 and np.isfinite(dD) and abs(dD) <= 0.05)
    Xm = float(np.max(np.abs(np.log10(np.maximum(np.array(W2["m3"]), 1e-300) / t_Mph(T_RM3)))))
    L1s = np.array([s["L1"] for s in samples])
    t_first = {thr: (float(ts[np.argmax(L1s < thr)]) if np.any(L1s < thr) else None) for thr in (0.1, 0.2)}
    return dict(eps_E=eps, D_W2=D, D_W1=W1["D"], dD=dD, on_law=on_law, X_m=Xm, m3_W2=W2["m3"], fesc_end=samples[-1]["fesc"],
                logratio_bins_W2=W2["lr"], L1_end=float(L1s[-1]), L1_min=float(L1s.min()), t_first_L1=t_first,
                L1_series=[round(float(x), 4) for x in L1s[:: max(1, len(L1s) // 130)]],
                E0=samples[0], E_end=samples[-1])


def run_toy(ic, mode="KT", tau_fac=1.0, t_end=None, wall_cap=1800.0):
    t_end = t_end if t_end else (350.0 if ic == "L" else 650.0)
    label = f"{mode}{'' if tau_fac == 1.0 else f'x{tau_fac:g}'}_{ic}"
    sim = ShellSim(ic, mode, tau_fac)
    t0 = time.time()
    samples, Eref = sim.run(t_end, label, wall_cap=wall_cap)
    t_eff = sim.capped_at if sim.capped_at is not None else t_end   # A1.1: windows relative to the time reached
    res = t_analyse(samples, Eref, t_eff)
    res.update(capped_at=sim.capped_at, t_windows_ref=t_eff,
               frac_r_lt_0p05_end=float(np.mean(sim.r < 0.05)), frac_r_lt_0p5_end=float(np.mean(sim.r < 0.5)),
               law_frac_r_lt_0p5=float(t_Mph(0.5) / T_MC))
    res.update(label=label, ic=ic, mode=mode, tau_fac=tau_fac, t_end=t_end, steps=sim.nsteps, nrelax=sim.nrelax,
               wall_s=time.time() - t0, E_R_end=sim.E_R, flow_cool=sim.flow_cool, flow_heat=sim.flow_heat,
               subset_eff=(sim.nS_eff / sim.nS_tot if sim.nS_tot else None), T_edge=T_EDGE, Eref=Eref)
    P(f"  toy {label:10s}: {'(capped at t = %.2f; windows relative to it) ' % sim.capped_at if sim.capped_at is not None else ''}"
      f"frac(r<0.5) {res['frac_r_lt_0p5_end']:.4f} (law {res['law_frac_r_lt_0p5']:.4f}); ON THE LAW {res['on_law']!s:5s} D(W2) {res['D_W2']:+.3f} dD {res['dD']:+.3f} X_m {res['X_m']:.3f} "
      f"f_esc {res['fesc_end']:.3f} eps_E {res['eps_E']:.1e} L1 end {res['L1_end']:.3f} first L1<0.1 at t = {res['t_first_L1'][0.1]} "
      f"(t_e = {T_EDGE:.2f}); E_R {sim.E_R:+.3f} (cool {sim.flow_cool:.2f} / heat {sim.flow_heat:.2f}); steps {sim.nsteps}; "
      f"{res['wall_s']:.0f} s")
    return res


# ================================================================================================ PLANAR SHEET TOY (conservation)
PG = 1.0; P_DT = 0.01; P_TEND = 50.0; P_CELL = 0.25; P_XLO, P_XHI = -60.0, 60.0; P_TAU = 1.0; P_DTR = 0.1
P_NCELL = int(round((P_XHI - P_XLO) / P_CELL))


def make_body(rng, Mb, Nb, sb, Md, Nd, sd, x0, v0, dust_off=0.0, dust_bulk=0.0, Td=None):
    xb = x0 + sb * rng.standard_normal(Nb); vb = v0 + 0.0 * xb
    xd = x0 + dust_off + sd * rng.standard_normal(Nd)
    vd = v0 + dust_bulk + (math.sqrt(Td) * rng.standard_normal(Nd) if Td else 0.0)
    mb = np.full(Nb, Mb / Nb); md = np.full(Nd, Md / Nd)
    return xb, vb, mb, xd, vd, md


class Sheets:
    """1-D planar sheets, exact pairwise gravity from ranks, per-cell relaxation (K-T), K-rho relocation, or none."""

    def __init__(self, bodies, mode="KT", g_ext=0.0, seed=9550):
        self.rng = np.random.default_rng(seed)
        xs, vs, ms, dust, host = [], [], [], [], []
        self.hosts = []
        for h, b in enumerate(bodies):
            xb, vb, mb, xd, vd, md = b["arrays"]
            xs += [xb, xd]; vs += [vb, vd]; ms += [mb, md]
            dust += [np.zeros(xb.size, bool), np.ones(xd.size, bool)]
            host += [np.full(xb.size, h), np.full(xd.size, h)]
            Mt = mb.sum() + md.sum()
            self.hosts.append(dict(xe=b["xe"], xon=b["xon"], T0=math.pi * PG * Mt * b["xe"] / 2))
        self.x = np.concatenate(xs); self.v = np.concatenate(vs); self.m = np.concatenate(ms)
        self.dust = np.concatenate(dust); self.host = np.concatenate(host)
        self.M = float(self.m.sum()); self.mode = mode; self.g_ext = g_ext
        self.t = 0.0; self.E_R = 0.0; self.t_last = 0.0
        self.a = self.accel()
        self.Tjump = 0.0; self.prev_owner = None; self.nswitch = 0
        self.X0 = self.Xcm(); self.P0 = self.Ptot()

    def accel(self):
        o = np.argsort(self.x, kind="stable")
        ms = self.m[o]; cm = np.cumsum(ms)
        left = cm - ms; right = self.M - cm
        a = np.empty_like(self.x); a[o] = 2 * math.pi * PG * (right - left)
        return a - self.g_ext

    def W(self):
        o = np.argsort(self.x, kind="stable"); ms = self.m[o]; xs = self.x[o]; cm = np.cumsum(ms)
        left = cm - ms; right = self.M - cm
        return 2 * math.pi * PG * float(np.sum(ms * xs * (left - right))) + self.g_ext * float(np.sum(self.m * self.x))

    def KE(self):
        return 0.5 * float(np.sum(self.m * self.v ** 2))

    def Ptot(self):
        return float(np.sum(self.m * self.v))

    def Xcm(self):
        return float(np.sum(self.m * self.x)) / self.M

    def centroids(self):
        out = []
        for h in range(len(self.hosts)):
            s = (self.host == h) & (~self.dust)
            out.append(float(np.sum(self.m[s] * self.x[s]) / np.sum(self.m[s])))
        return out

    def owners(self, xc, X):
        """M1: each cell centre goes to the host with the smallest |x - X_h| / x_on,h."""
        q = np.array([np.abs(xc - X[h]) / self.hosts[h]["xon"] for h in range(len(self.hosts))])
        return np.argmin(q, axis=0)

    def TJ_cells(self, X):
        xc = P_XLO + P_CELL * (np.arange(P_NCELL) + 0.5)
        own = self.owners(xc, X)
        T = np.zeros(P_NCELL); ins = np.zeros(P_NCELL, bool)
        for h in range(len(self.hosts)):
            s = own == h
            d = (xc[s] - X[h]) / self.hosts[h]["xe"]
            T[s] = self.hosts[h]["T0"] * np.maximum(0.0, 1.0 - d * d)
            ins[s] = np.abs(d) < 1.0
        return xc, own, T, ins

    def relax(self, Dt):
        X = self.centroids()
        xc, own, T, ins = self.TJ_cells(X)
        if self.prev_owner is not None:
            ch = own != self.prev_owner
            if ch.any():
                self.nswitch += int(ch.sum())
                self.Tjump = max(self.Tjump, float(np.max(np.abs(T[ch] - self.Tprev[ch]) / max(h["T0"] for h in self.hosts))))
        self.prev_owner = own.copy(); self.Tprev = T.copy()
        cell = np.floor((self.x - P_XLO) / P_CELL).astype(np.int64)
        okc = (cell >= 0) & (cell < P_NCELL)
        cellc = np.clip(cell, 0, P_NCELL - 1)
        if self.mode == "KT":
            p = 1.0 - math.exp(-Dt / P_TAU)
            sel = self.dust & okc & ins[cellc] & (self.rng.random(self.x.size) < p)
            if not sel.any():
                return
            ii = cellc[sel]
            nS = np.bincount(ii, minlength=P_NCELL).astype(float)
            mS = np.bincount(ii, weights=self.m[sel], minlength=P_NCELL)
            pS = np.bincount(ii, weights=self.m[sel] * self.v[sel], minlength=P_NCELL)
            uS = pS / np.where(mS > 0, mS, 1.0)
            xi = self.rng.standard_normal(ii.size)
            xb = np.bincount(ii, weights=self.m[sel] * xi, minlength=P_NCELL) / np.where(mS > 0, mS, 1.0)
            K0 = self.KE()
            self.v[sel] = uS[ii] + np.sqrt(T[ii]) * (xi - xb[ii])       # momentum of the subset kept exactly (mass-weighted)
            self.E_R -= self.KE() - K0
        elif self.mode in ("Krho", "Krho_u"):
            # K-rho: dust in a host's shell (x_e < |x - X_h| < x_on, owned by h) is relocated with probability p to the interior,
            # drawn from the target profile; 'Krho' keeps its velocity, 'Krho_u' takes the local mean velocity at the new place
            p = 1.0 - math.exp(-Dt / P_TAU)
            for h in range(len(self.hosts)):
                d = self.x - X[h]
                ownp = own[cellc] == h
                shell = self.dust & okc & ownp & (np.abs(d) > self.hosts[h]["xe"]) & (np.abs(d) < self.hosts[h]["xon"])
                mv = shell & (self.rng.random(self.x.size) < p)
                n = int(mv.sum())
                if n == 0:
                    continue
                y = []
                while len(y) < n:                                    # rejection sampling of (1 - s^2) on |s| < 1
                    s = self.rng.uniform(-1, 1, 2 * n); w = self.rng.random(2 * n)
                    y += list(s[w < 1 - s * s])
                newx = X[h] + self.hosts[h]["xe"] * np.array(y[:n])
                self.x[mv] = newx
                if self.mode == "Krho_u":
                    cnew = np.clip(np.floor((newx - P_XLO) / P_CELL).astype(np.int64), 0, P_NCELL - 1)
                    stay = self.dust & (~mv)
                    mm = np.bincount(cellc[stay], weights=self.m[stay], minlength=P_NCELL)
                    pp = np.bincount(cellc[stay], weights=self.m[stay] * self.v[stay], minlength=P_NCELL)
                    self.v[mv] = (pp / np.where(mm > 0, mm, 1.0))[cnew]
            self.a = self.accel()

    def step(self):
        self.v += 0.5 * P_DT * self.a
        self.x += P_DT * self.v
        self.a = self.accel()
        self.v += 0.5 * P_DT * self.a
        self.t += P_DT
        if self.mode != "off" and self.t - self.t_last >= P_DTR - 1e-12:
            self.relax(self.t - self.t_last); self.t_last = self.t

    def run(self, t_end=P_TEND, track=None):
        E0 = self.KE() + self.W(); Eabs = abs(self.KE()) + abs(self.W())
        nsteps = int(round(t_end / P_DT))
        maxdP = 0.0; maxdE = 0.0; maxslip = 0.0; trk = []
        vref = math.sqrt(max(h["T0"] for h in self.hosts))
        rho_prev = None; Jmax = 0.0
        for n in range(nsteps):
            self.step()
            if (n + 1) % 10 == 0:
                Pn = self.Ptot()
                dPg = Pn - self.P0 + self.g_ext * self.M * self.t          # uniform field: P0 - M g t expected
                maxdP = max(maxdP, abs(dPg) / (self.M * vref))
                E = self.KE() + self.W() + self.E_R
                maxdE = max(maxdE, abs(E - E0) / Eabs)
                slip = abs(self.Xcm() - self.X0 - self.P0 / self.M * self.t + 0.5 * self.g_ext * self.t ** 2)
                maxslip = max(maxslip, slip)
                if track is not None:
                    trk.append(track(self))
                if (n + 1) % 100 == 0:
                    h, _ = np.histogram(self.x, bins=200, range=(P_XLO, P_XHI), weights=self.m)
                    if rho_prev is not None:
                        Jmax = max(Jmax, float(np.sum(np.abs(h - rho_prev)) / self.M))
                    rho_prev = h
        return dict(maxdP=maxdP, maxdE=maxdE, max_cm_slip=maxslip, E_R=self.E_R, E0=E0, Eabs=Eabs, vref=vref,
                    nswitch=self.nswitch, Tjump=self.Tjump, J_per_unit_time=Jmax, track=trk, mass=self.M,
                    N=int(self.x.size))


def body_host(rng, x0=0.0, v0=0.0, dust_off=0.0, dust_bulk=0.0):
    T0 = math.pi * PG * 6.364 * 5.0 / 2
    return dict(arrays=make_body(rng, 1.0, 2000, 1.0, 5.364, 10000, 2.5, x0, v0, dust_off, dust_bulk, Td=T0 / 2), xe=5.0, xon=10.0)


def body_sat(rng, x0, v0):
    T0 = math.pi * PG * 0.6364 * 2.5 / 2
    return dict(arrays=make_body(rng, 0.1, 200, 0.5, 0.5364, 1000, 1.25, x0, v0, Td=T0 / 2), xe=2.5, xon=5.0)


def planar_run(case, mode, g_ext=0.0):
    rng = np.random.default_rng({"ER": 1, "ES": 2, "EM": 3, "B1": 4}[case])
    if case == "ER":
        bodies = [body_host(rng, dust_off=1.0, dust_bulk=0.3)]
    elif case == "ES":
        bodies = [body_host(rng), body_sat(rng, 20.0, -1.0)]
    elif case == "EM":
        bodies = [body_host(rng, x0=-15.0, v0=0.5), body_host(rng, x0=15.0, v0=-0.5)]
    elif case == "B1":
        bodies = [body_sat(rng, 0.0, 0.0)]
    S = Sheets(bodies, mode=mode, g_ext=g_ext)
    track = None
    if case == "B1":
        def track(s):
            b = (~s.dust); d = s.dust
            return (s.t, float(np.sum(s.m[d] * s.x[d]) / np.sum(s.m[d]) - np.sum(s.m[b] * s.x[b]) / np.sum(s.m[b])))
    res = S.run(track=track)
    res.update(case=case, mode=mode, g_ext=g_ext)
    return res


# ================================================================================================ NGC 3198: stationary state, BTFR, selection
def ngc_model(kern, a0, mb_r=None, R=None, upto=None):
    """m_b(r) by PCHIP in (ln r, m_N), r^3 inside, point mass beyond; phantom, rho_ph, T_J; supply-root edge."""
    R = R_N if R is None else R
    mN = MBR_N if mb_r is None else mb_r
    lnR = np.log(R); pch = PchipInterpolator(lnR, mN); dpch = pch.derivative()

    def m_b(x):
        if x <= R[0]: return mN[0] * (x / R[0]) ** 3
        if x >= R[-1]: return mN[-1]
        return float(pch(math.log(x)))

    def dm_b(x):
        if x <= R[0]: return 3 * mN[0] * x * x / R[0] ** 3
        if x >= R[-1]: return 0.0
        return float(dpch(math.log(x))) / x
    law = KERN[kern]

    def gl(x):
        gn = G_SI * m_b(x) / x ** 2
        return float(law(gn, a0)), gn

    def Mph(x):
        g, gn = gl(x); return x * x * (g - gn) / G_SI

    def dMph(x):
        g, gn = gl(x)
        dgn = G_SI * dm_b(x) / x ** 2 - 2 * G_SI * m_b(x) / x ** 3
        return (2 * x * (g - gn) + x * x * (float(dlaw(kern, gn, a0)) - 1) * dgn) / G_SI
    dom = domain(m_b(R[-1]) / MSUN, a0)
    Mc = dom["Mc"] * MSUN
    lo, hi = R[-1], 1e3 * R[-1]
    r_e = brentq(lambda x: Mph(x) - Mc, lo, hi, xtol=1e-6 * KPC, rtol=1e-14)
    return dict(m_b=m_b, dm_b=dm_b, gl=gl, Mph=Mph, dMph=dMph, r_e=r_e, Mc=Mc, dom=dom, R=R)


def hydro_tables(m_v, dm_v, law_v, dlaw_v, Gc, r0, r_e, N=100001):
    """Vectorized tables on a fine ln-r grid (2N - 1 points, nodes and midpoints) from r0 to r_e (1 - 1e-6):
    m_b, phantom M_ph and rho_ph (analytic dM_ph/dr), law field, P_ph = int_r^{r_e} rho_ph g_law dr (cumulative trapezoid in
    ln r plus the tail), T_J = P_ph / rho_ph."""
    lf = np.linspace(math.log(r0), math.log(r_e * (1 - 1e-6)), 2 * N - 1)
    x = np.exp(lf)
    m = m_v(x); dm = dm_v(x)
    gn = Gc * m / x ** 2
    g = law_v(gn); dg = dlaw_v(gn)
    dgn = Gc * dm / x ** 2 - 2 * Gc * m / x ** 3
    Mph = x * x * (g - gn) / Gc
    dMph = (2 * x * (g - gn) + x * x * (dg - 1) * dgn) / Gc
    rho = dMph / (4 * np.pi * x * x)
    f = x * rho * g
    tail = f[-1] * (math.log(r_e) - lf[-1])                           # int over the last 1e-6 in ln r (linear estimate)
    seg = 0.5 * (f[1:] + f[:-1]) * np.diff(lf)
    Pph = np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]]) + tail
    with np.errstate(divide="ignore", invalid="ignore"):
        TJ = np.where(rho > 0, Pph / rho, np.nan)
    return dict(lf=lf, x=x, m=m, gn=gn, g=g, Mph=Mph, rho=rho, Pph=Pph, TJ=TJ, Gc=Gc, neg=bool(np.any(dMph <= 0)), r_e=r_e)


def rk4_hydro(tab, Cs, keep_path=False):
    """Fixed-step RK4 in ln r over the table nodes (stages at the tabulated midpoints), vectorized over the normalisations C:
    dP/dlnr = -r (P/T_J) G (m_b + M_d)/r^2, dM/dlnr = 4 pi r^3 P/T_J; P clamped at 0 once the dust ends."""
    Cs = np.atleast_1d(np.asarray(Cs, float))
    lf, x, m, TJ, Gc = tab["lf"], tab["x"], tab["m"], tab["TJ"], tab["Gc"]
    TJs = np.where(np.isfinite(TJ) & (TJ > 0), TJ, np.inf)
    Pd = Cs * tab["Pph"][0]; Md = Cs * tab["Mph"][0]
    path = [Md.copy()] if keep_path else None

    def F(j, Pd, Md):
        rho = np.maximum(Pd, 0.0) / TJs[j]
        return -x[j] * rho * Gc * (m[j] + Md) / x[j] ** 2, 4 * np.pi * x[j] ** 3 * rho
    nn = (lf.size - 1) // 2
    for i in range(nn):
        j0, j1, j2 = 2 * i, 2 * i + 1, 2 * i + 2
        h = lf[j2] - lf[j0]
        k1p, k1m = F(j0, Pd, Md)
        k2p, k2m = F(j1, Pd + 0.5 * h * k1p, Md + 0.5 * h * k1m)
        k3p, k3m = F(j1, Pd + 0.5 * h * k2p, Md + 0.5 * h * k2m)
        k4p, k4m = F(j2, Pd + h * k3p, Md + h * k3m)
        Pd = Pd + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
        Md = Md + h / 6 * (k1m + 2 * k2m + 2 * k3m + k4m)
        Pd = np.maximum(Pd, 0.0)
        if keep_path:
            path.append(Md.copy())
    return Md, (np.array(path) if keep_path else None)


def ngc_vec(kern, a0, md):
    R = md["R"]; mN = MBR_N
    pch = PchipInterpolator(np.log(R), mN); dpch = pch.derivative()

    def m_v(x):
        lx = np.log(x)
        return np.where(x <= R[0], mN[0] * (x / R[0]) ** 3, np.where(x >= R[-1], mN[-1], pch(np.clip(lx, np.log(R[0]), np.log(R[-1])))))

    def dm_v(x):
        lx = np.log(x)
        return np.where(x <= R[0], 3 * mN[0] * x * x / R[0] ** 3, np.where(x >= R[-1], 0.0, dpch(np.clip(lx, np.log(R[0]), np.log(R[-1]))) / x))
    return m_v, dm_v, (lambda gn: KERN[kern](gn, a0)), (lambda gn: dlaw(kern, gn, a0))

# ================================================================================================ satellites / drag helpers
def plum(M_kg, a):
    Mf = lambda x: M_kg * x ** 3 / (x * x + a * a) ** 1.5
    rhof = lambda x: 3 * M_kg * a * a / (4 * math.pi * (x * x + a * a) ** 2.5)
    return Mf, rhof


def phantom_density(Mf, a0, x, kern="simple"):
    law = KERN[kern]; h = 1e-5 * x
    def Mph(y):
        gn = G_SI * Mf(y) / y ** 2; return y * y * (float(law(gn, a0)) - gn) / G_SI
    return (Mph(x + h) - Mph(x - h)) / (2 * h) / (4 * math.pi * x * x), Mph(x)


def point_phantom_density(M_kg, a0, x, kern="simple"):
    return phantom_density(lambda y: M_kg, a0, x, kern)


def glaw_of(Mf, a0, x, kern="simple"):
    gn = G_SI * Mf(x) / x ** 2; return float(KERN[kern](gn, a0))


def tau_candidates(foot):
    """T1 (factor of local tau_ff, computed at the site), T2 (k ends), T3 (Gyr ends)."""
    k_lo = 0.46 if foot == "canonical" else 0.52
    t3_lo = 0.72 if foot == "canonical" else 0.83
    return {"T1": ("ff", None), f"T2(k={k_lo})": ("orb", k_lo), "T2(k=1.20)": ("orb", 1.20),
            f"T3({t3_lo} Gyr)": ("gyr", t3_lo), "T3(3.47 Gyr)": ("gyr", 3.47)}


def tau_value(kind, par, rho_m, x, vc):
    if kind == "ff":
        return 1.0 / math.sqrt(4 * math.pi * G_SI * rho_m) / (2 * ALPHA)
    if kind == "orb":
        return par * 2 * math.pi * x / vc
    return par * GYR_S


# ================================================================================================ CFG939 class systems (copied, with attribution)
GK = 4.30091e-6; GYRK = 0.97779


def c939_systems():
    def plummer(M, a): return (lambda r: M * r ** 3 / (r * r + a * a) ** 1.5, lambda r: 3 * M * a * a * r * r / (r * r + a * a) ** 2.5)
    def hernquist(M, a): return (lambda r: M * r * r / (r + a) ** 2, lambda r: 2 * M * a * r / (r + a) ** 3)
    def expsph(M, R): return (lambda r: M * (1 - (1 + r / R) * math.exp(-r / R)), lambda r: M * (r / R) * math.exp(-r / R) / R)
    def beta23(Mnorm, rnorm, rc, rtr):
        Kn = Mnorm / (rnorm / rc - math.atan(rnorm / rc))
        return (lambda r: Kn * ((min(r, rtr) / rc) - math.atan(min(r, rtr) / rc)), lambda r: Kn * (r / rc) ** 2 / (1 + (r / rc) ** 2) / rc if r < rtr else 0.0)
    def combo(parts): return (lambda r: sum(p[0](r) for p in parts), lambda r: sum(p[1](r) for p in parts))
    S = {}
    for nm, Ms, Re in (("UFD-c", 5e3, 0.030), ("UFD-e", 3e4, 0.240), ("Draco-like", 5e5, 0.220), ("Fornax-like", 4e7, 0.710)):
        S[nm] = plummer(Ms, Re)
    S["SPARC-dwarf"] = combo([expsph(2.6e7, 0.6), expsph(3.66e8, 2.0)])
    S["MW-like"] = hernquist(6e10, 2.5)
    g = beta23(1e14, 1200.0, 150.0, 2400.0); m = beta23(1e13, 1200.0, 150.0, 2400.0); mt = m[0](2400.0); sc = 1e13 / mt
    S["cluster-core"] = combo([g, hernquist(1.5e12, 30.0), (lambda r: sc * m[0](r), lambda r: sc * m[1](r))])
    S["cluster-stars"] = hernquist(1.5e12, 30.0)
    for r_ in csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))):
        Mbar = float(r_["M_bar_1e8"]) * 1e8; Ro = float(r_["R_out_kpc"])
        S[r_["object"].replace(" ", "")] = (lambda r, M=Mbar, R=Ro: M * min(1.0, (r / R) ** 2), lambda r, M=Mbar, R=Ro: (2 * M * r / R ** 2) if r < R else 0.0)
    for nm, Ms, Re in (("NGC1052-DF2", 2.0e8, 2.0), ("NGC1052-DF4", 1.5e8, 1.6)):
        S[nm] = plummer(Ms, Re)
    return S


def maxwell_frac(x):
    """fraction of a 3-D Maxwellian (1-D dispersion 1) with speed below x."""
    return math.erf(x / math.sqrt(2)) - math.sqrt(2 / math.pi) * x * math.exp(-x * x / 2)


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
KC = {}
# ---- K1: CFG947 T-M
tsym = sp.symbols("t", real=True); nS_ = 3
sj = [sp.Function(f"s{j}")(tsym) for j in range(nS_)]; xj = [sp.Function(f"x{j}")(tsym) for j in range(nS_)]
Dm = sum(s_ * x_ for s_, x_ in zip(sj, xj))
Rrel = sp.simplify(sp.diff(Dm, tsym, 2) - sum(s_ * sp.diff(x_, tsym, 2) for s_, x_ in zip(sj, xj))
                   - sum(sp.diff(s_, tsym, 2) * x_ + 2 * sp.diff(s_, tsym) * sp.diff(x_, tsym) for s_, x_ in zip(sj, xj)))
Me = sp.Function("M_e")(tsym); Xt = sp.Function("X")(tsym); epsS, McS = sp.symbols("epsilon M_c", positive=True)
mp, mm = McS * (1 + epsS) / 2, McS * (1 - epsS) / 2
sw = [Me, -Me / McS * mp, -Me / McS * mm]; xw = [sp.Integer(0), Xt, -Xt]
R_E8 = sp.simplify(sum(sp.diff(s_, tsym, 2) * x_ + 2 * sp.diff(s_, tsym) * sp.diff(x_, tsym) for s_, x_ in zip(sw, xw)))
R_E8_target = -epsS * (sp.diff(Me, tsym, 2) * Xt + 2 * sp.diff(Me, tsym) * sp.diff(Xt, tsym))
tg, Me0, X0s, Gs_, Md = sp.symbols("t_g M_e0 X_0 G_s M_dom", positive=True)
hist = Me0 * (1 - sp.cos(sp.pi * tsym / tg)) / 2
Rmax_E8 = sp.simplify(sp.Abs(R_E8_target.subs({Me: hist, Xt: X0s}).doit().subs(tsym, 0)))
scale = {tg: sp.sqrt(X0s ** 3 / (Gs_ * Md)), Me0: Md / 2, McS: Md / 2}
rel_E8 = sp.simplify((Rmax_E8 / (Gs_ * Md ** 2 / X0s ** 2)).subs(scale))
tm_rel = {e: float(rel_E8.subs(epsS, e)) for e in (0.01, 0.1, 0.3)}
K1 = chk("K1_CFG947_T-M", Rrel == 0 and sp.simplify(R_E8 - R_E8_target) == 0 and
         all(abs(tm_rel[e] - math.pi ** 2 * e / 4) < 1e-12 for e in tm_rel) and
         abs(tm_rel[0.01] - 0.025) < 1e-3 and abs(tm_rel[0.1] - 0.247) < 1e-3 and abs(tm_rel[0.3] - 0.740) < 1e-3,
         f"identity residual {Rrel}; E8 two-blob R = {sp.simplify(R_E8)}; max|R|/(M_dom g_ref) = {rel_E8} = "
         + ", ".join(f"{tm_rel[e]:.4f}" for e in tm_rel) + " at eps 0.01/0.1/0.3 (0.025/0.247/0.740)")
KC["K1"] = dict(R_rel=tm_rel)
# ---- K2: CFG947 T-R
Mta_thr = M_ta(RMIN, DTA0); fr_thr = fret_of(math.log10(Mta_thr)); Mb_thr = fr_thr * FB * Mta_thr / HE
G_ = sparc_setup(); below = 0; tot_g = 0
for g in G_:
    Rm = g["R"] * 3.0857e19; GB = (np.sign(g["Vg"]) * g["Vg"] ** 2 + 0.61 * g["Vd"] ** 2 + 1.4 * 0.61 * g["Vb"] ** 2) * 1e6 / Rm
    mb = _mb_last(GB, Rm)
    if mb is None: continue
    tot_g += 1; below += int(mb < Mb_thr)
ngc_res = census(MB_N)["R"] >= RMIN
K2 = chk("K2_CFG947_T-R", abs(Mb_thr / 4.815e10 - 1) < 1e-3 and (not ngc_res) and below == 128 and tot_g == 175,
         f"M_b,thr = {Mb_thr:.4e} (4.815e10); NGC 3198 r_ON = {census(MB_N)['R']:.4f} Mpc/h -> {'resolved' if ngc_res else 'NOT resolved'}; "
         f"SPARC {below} of {tot_g} below (128 of 175)")
KC["K2"] = dict(Mb_thr=Mb_thr, below=below, total=tot_g)
# ---- K3: CFG947 T-X
tx = {f"{f}|{nm}|{rk:.0f}|{kz}": efe_global_dex(Mb, apc, rk, A0[f], kz) for f in FOOTS for nm, Mb, apc in HOSTS882 for rk in RHOST
      for kz in KERN}
K3 = chk("K3_CFG947_T-X", len(tx) == 36 and abs(min(tx.values()) + 0.730) < 1e-3 and abs(max(tx.values()) + 0.102) < 1e-3,
         f"36 E4 EFE factors {min(tx.values()):.4f} .. {max(tx.values()):.4f} dex (-0.730 .. -0.102)")
KC["K3"] = dict(min=min(tx.values()), max=max(tx.values()))
# ---- K4: CFG938 NGC 3198 law
EXK1 = EL_static()
fK1 = sp.lambdify((u, gN, a0s, G), EXK1, "math")
k4 = {}
for foot in FOOTS:
    a0 = A0[foot]; rel = []
    for gn in GN_N:
        grid = a0 * np.unique(np.concatenate((np.logspace(-14, -1e-12, 900), np.linspace(1e-4, 1 - 1e-13, 3000))))
        vals = np.array([fK1(x, gn, a0, G_SI) for x in grid])
        idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) <= 0)[0]
        uu = brentq(lambda x: fK1(x, gn, a0, G_SI), grid[idx[0]], grid[idx[0] + 1], xtol=1e-40, rtol=1e-15, maxiter=800)
        rel.append(abs((gn + uu) / float(law_simple(gn, a0)) - 1))
    k4[foot] = float(max(rel))
K4 = chk("K4_CFG938_NGC3198_law", all(v < 1e-6 for v in k4.values()), f"canonical {k4['canonical']:.2e}, alt {k4['alt']:.2e} (2.2e-16)")
KC["K4"] = k4
# ---- K5: CFG952 effective RMIN node at 1024^3
dx1024 = 100.0 / 1024; Rg = np.geomspace(dx1024, 8.0, 14); eff = float(Rg[Rg >= RMIN - 1e-9][0])
Mta_eff = M_ta(eff, DTA0); fr_eff = fret_of(math.log10(Mta_eff)); Mb_eff = fr_eff * FB * Mta_eff / HE
K5 = chk("K5_CFG952_effective_RMIN", abs(eff / 1.0471 - 1) < 1e-2 and abs(Mb_eff / 2.19e11 - 1) < 1e-2,
         f"node {eff:.4f} Mpc/h (1.0471); M_b,ret >= {Mb_eff:.3e} M_sun (2.19e11)")
KC["K5"] = dict(node=eff, Mb_ret=Mb_eff)
# ---- K6: CFG941 growth exponents
P("  deriving growth determinant (sympy, CFG941 route) ...")
DET2, HOM2 = growth_det([("b", FBr, False), ("t", FCr, True)])
n_s6 = n_from_det(DET2, {C2s: 1, Bs: 0}); n_full = n_from_det(DET2, {C2s: 1, Bs: 1}); n_dust = n_from_det(DET2, {C2s: 0, Bs: 0})
K6 = chk("K6_CFG941_growth", HOM2 and abs(n_s6 - 0.60954) < 1e-4 and abs(n_full - 0.69433) < 1e-4 and abs(n_dust - 1) < 1e-12,
         f"n = {n_s6:.6f} / {n_full:.6f} / {n_dust:.12f} (0.60954 / 0.69433 / 1)")
KC["K6"] = dict(n_s6=n_s6, n_full=n_full, n_dust=n_dust)
rss_guard("K6")
# ---- K7: CFG935 PHYS table read; toy T_J vs CFG935's law_jeans_sigma2
PHYS = json.load(open(os.path.join(LANES, "CFG935_energy_conserving_settling", "parts", "PHYS.json")))
rk7 = np.geomspace(0.1, 9.0, 200)
k7 = float(np.max(np.abs(t_TJ(rk7) / t_law_jeans_sigma2(rk7) - 1)))
phys_ok = abs(PHYS["systems"]["can"]["UFD-c"]["E_x_a_erg"] / 1.63e49 - 1) < 0.01 and abs(PHYS["systems"]["can"]["cluster-core"]["E_x_a_erg"] / 7.34e63 - 1) < 0.01
K7 = chk("K7_CFG935_table_and_TJ", phys_ok and k7 <= 1e-3,
         f"PHYS E_x read (UFD-c {PHYS['systems']['can']['UFD-c']['E_x_a_erg']:.3e}, cluster core {PHYS['systems']['can']['cluster-core']['E_x_a_erg']:.3e} erg); "
         f"max |T_J/sigma_J^2(CFG935) - 1| on r = 0.1-9: {k7:.2e} (line 1e-3)")
KC["K7"] = dict(TJ_rel=k7)
# ---- K8: CFG947 SPARC local law
P("  K8 SPARC (CFG4 statistic, nu_mono):")
k8 = {}
for foot in FOOTS:
    k8[f"local|{foot}"] = sparc_rms(A0[foot], pred_local, f"local law {foot}")
    k8[f"newton|{foot}"] = sparc_rms(A0[foot], pred_newton, f"Newton {foot}")
ref8 = {"canonical": (0.1003, 0.61), "alt": (0.0991, 0.57)}
K8 = chk("K8_CFG947_SPARC", all(abs(k8[f"local|{f}"]["rms"] - ref8[f][0]) <= 1.5e-4 and abs(k8[f"local|{f}"]["U"] - ref8[f][1]) < 1e-9
                                and abs(k8[f"newton|{f}"]["rms"] - 0.2755) <= 1e-3 for f in FOOTS),
         f"local {k8['local|canonical']['rms']:.5f} @ {k8['local|canonical']['U']:.2f} / {k8['local|alt']['rms']:.5f} @ {k8['local|alt']['U']:.2f}; "
         f"Newton {k8['newton|canonical']['rms']:.4f} / {k8['newton|alt']['rms']:.4f}")
KC["K8"] = k8
K_ALL = K1 and K2 and K3 and K4 and K5 and K6 and K7 and K8
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> main classes VOID'}")
RES["K"] = KC; RES["K_all"] = K_ALL
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)

# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    teeth = {}; MU = {}
    # Mu1: tether instead of relaxation -> D-T's a^0.694
    teeth["Mu1"] = abs(n_full - 0.69433) < 1e-4 and abs(n_dust - 1) < 1e-12
    chk("Mu1_tether_gives_DT", teeth["Mu1"], f"tether (c2 = 1, chi-bar gradient) n = {n_full:.6f} (0.69433); relaxation-only dust n = {n_dust:.12f}")
    # Mu2: global phantom (host + satellite baryons) -> EFE returns (CFG947 values)
    teeth["Mu2"] = max(abs(v) for v in tx.values()) >= 0.05 and abs(min(tx.values()) + 0.730) < 1e-3 and abs(max(tx.values()) + 0.102) < 1e-3
    chk("Mu2_global_phantom_EFE", teeth["Mu2"], f"global phantom EFE {min(tx.values()):.4f} .. {max(tx.values()):.4f} dex; own-domain monopole 0")
    # Mu3: K-rho relocation in the planar toy
    P("  Mu3: K-rho relocation, planar toy E-R (asymmetric host) ...")
    m3a = planar_run("ER", "Krho"); m3b = planar_run("ER", "Krho_u")
    xe = 5.0
    teeth["Mu3"] = (m3a["max_cm_slip"] / xe >= 1e-3) or (m3b["maxdP"] >= 1e-3)
    chk("Mu3_Krho_breaks_CM_or_momentum", teeth["Mu3"],
        f"K-rho keep-velocity: CM slip {m3a['max_cm_slip'] / xe:.3e} x_e, |dP|/(M v_ref) {m3a['maxdP']:.2e}; "
        f"K-rho local-velocity: CM slip {m3b['max_cm_slip'] / xe:.3e} x_e, |dP|/(M v_ref) {m3b['maxdP']:.2e}")
    MU["Mu3"] = dict(keep_velocity={k: v for k, v in m3a.items() if k != "track"}, local_velocity={k: v for k, v in m3b.items() if k != "track"})
    rss_guard("Mu3")
    # Mu4: self-consistent target (no phantom) from IC-I
    P("  Mu4: CFG554 self-consistent target, spherical toy IC-I ...")
    m4 = run_toy("I", mode="self")
    teeth["Mu4"] = not m4["on_law"]
    chk("Mu4_selfconsistent_target_not_on_law", teeth["Mu4"], f"D(W2) {m4['D_W2']:+.3f}, dD {m4['dD']:+.3f}, X_m {m4['X_m']:.3f}")
    # Mu5: relaxation off from IC-I
    P("  Mu5: relaxation off, spherical toy IC-I ...")
    m5 = run_toy("I", mode="off")
    teeth["Mu5"] = not m5["on_law"]
    chk("Mu5_relaxation_off_not_on_law", teeth["Mu5"], f"D(W2) {m5['D_W2']:+.3f}, dD {m5['dD']:+.3f}, X_m {m5['X_m']:.3f}")
    MU["Mu4"] = m4; MU["Mu5"] = m5
    RES["MUTATE"] = dict(teeth=teeth, **MU)
    allb = all(teeth.values())
    P(f"  MUTATE: {'ALL TEETH BITE' if allb else 'A TOOTH DID NOT BITE'}")
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
    sys.exit(1 if allb else 2)

# ================================================================================================ MAIN: structural statements (sympy)
P("\n==================== STRUCTURAL STATEMENTS ====================")
ST = {}
vv, uu_, TT, TJs, rho_, rhoeq, tau_ = sp.symbols("v u T T_J rho rho_eq tau", real=True)
TTp, TJp, rhop, taup = sp.symbols("T_p T_Jp rho_p tau_p", positive=True)


def Mx(rho, uvel, T, var=vv):
    return rho / sp.sqrt(2 * sp.pi * T) * sp.exp(-(var - uvel) ** 2 / (2 * T))


def mom(fexpr, n):
    return sp.simplify(sp.integrate(fexpr * vv ** n, (vv, -sp.oo, sp.oo)))


# moments of a 1-D Maxwellian; the 3-D isotropic case is the product of three (energy 3/2 rho T)
m0 = mom(Mx(rhop, uu_, TTp), 0); m1 = mom(Mx(rhop, uu_, TTp), 1); m2 = mom(Mx(rhop, uu_, TTp), 2)
# K-T collision term for a local-Maxwellian f with temperature T: C = -(M[rho,u,T] - M[rho,u,T_J])/tau
CKT = -(Mx(rhop, uu_, TTp) - Mx(rhop, uu_, TJp)) / taup
cKT = [mom(CKT, n) for n in (0, 1, 2)]
eKT = sp.simplify(3 * cKT[2] / 2)                                      # three components: energy moment sum (v_i^2/2) = 3/2 x 1-D <v^2>
CKR = -(Mx(rhop, uu_, TTp) - Mx(rhoeq, uu_, TJp)) / taup               # K-rho: density target
cKR0 = mom(CKR, 0)
ST["H0"] = chk("H0_collision_moments", m0 == rhop and sp.simplify(m1 - rhop * uu_) == 0 and sp.simplify(m2 - rhop * (uu_ ** 2 + TTp)) == 0
               and cKT[0] == 0 and cKT[1] == 0 and sp.simplify(eKT - sp.Rational(3, 2) * rhop * (TJp - TTp) / taup) == 0
               and sp.simplify(cKR0 + (rhop - rhoeq) / taup) == 0,
               f"K-T: mass {cKT[0]}, momentum {cKT[1]}, energy (3 comps) {sp.factor(eKT)}; K-rho mass moment {sp.factor(cKR0)} != 0 "
               "-> continuity has a source (O(c^2) part of div T^{mu 0} = 0 fails)")
# L1: zeroth-order Chapman-Enskog stress of the K-T target = rho T_J (Euler with p = rho T_J(x))
stress = sp.simplify(sp.integrate((vv - uu_) ** 2 * Mx(rhop, uu_, TJp), (vv, -sp.oo, sp.oo)))
heatflux = sp.simplify(sp.integrate((vv - uu_) ** 3 * Mx(rhop, uu_, TJp), (vv, -sp.oo, sp.oo)))
L1sym = sp.simplify(stress - rhop * TJp) == 0 and heatflux == 0
P(f"  L1 (sympy): stress of f_eq = {stress} (p = rho T_J), heat flux {heatflux}; first order (BGK): eta = p tau, q ~ -(5/2) p tau grad T")
# L4: uniform-acceleration covariance (1-D phase space), with a generic exponential-quadratic test function
xx, vv2, t4 = sp.symbols("x v t", real=True); gext = sp.symbols("g_e", real=True)
Xf = sp.Function("X")(t4)
cc = sp.symbols("c1:7", real=True)
gi_ = sp.Function("g_i")


def Ftest(xi_, eta_, t_):
    return sp.exp(cc[0] * xi_ ** 2 + cc[1] * eta_ ** 2 + cc[2] * xi_ * eta_ + cc[3] * xi_ + cc[4] * eta_ + cc[5] * t_)


xi_s = xx - Xf; eta_s = vv2 - sp.diff(Xf, t4)
fsh = Ftest(xi_s, eta_s, t4)
lhs = sp.diff(fsh, t4) + vv2 * sp.diff(fsh, xx) + (gext + gi_(xi_s)) * sp.diff(fsh, vv2)
lhs = lhs.subs(sp.diff(Xf, t4, 2), gext)
XI, ETA = sp.symbols("xi eta", real=True)
Fp = Ftest(XI, ETA, t4)
rhs_ = (sp.diff(Fp, t4) + ETA * sp.diff(Fp, XI) + gi_(XI) * sp.diff(Fp, ETA)).subs({XI: xi_s, ETA: eta_s})
diff4 = sp.simplify(sp.expand(lhs - rhs_))
Vsh = sp.symbols("V", real=True)
cov = sp.simplify(Mx(rhop, uu_, TJp, vv) - Mx(rhop, uu_ - Vsh, TJp, vv - Vsh))
P(f"  L4 (sympy): Vlasov operator in the frame falling with g_e: residual vs the field-free operator = {diff4}; "
  f"Maxwellian shift covariance M[rho,u,T](v) - M[rho,u-V,T](v-V) = {cov}")
ST["L4_sym"] = chk("L4_uniform_field_drops_out", cov == 0 and diff4 == 0,
                   f"falling-frame Vlasov residual {diff4}; local-Maxwellian shift covariance {cov}: Delta a/g_host = 0, EFE 0 dex at monopole order")
# L6: two cold streams in one cell (linear BGK split)
r1, r2 = sp.symbols("rho_1 rho_2", positive=True); u1 = sp.Function("u1")(t4); u2 = sp.Function("u2")(t4)
um = (r1 * u1 + r2 * u2) / (r1 + r2)
du1 = -(u1 - um) / taup; du2 = -(u2 - um) / taup
L6rel = sp.simplify((du1 - du2) + (u1 - u2) / taup)
L6P = sp.simplify(r1 * du1 + r2 * du2)
KErel = sp.simplify(sp.diff(r1 * r2 / (2 * (r1 + r2)) * (u1 - u2) ** 2, t4).subs({sp.diff(u1, t4): du1, sp.diff(u2, t4): du2})
                    + 2 * r1 * r2 / (2 * (r1 + r2)) * (u1 - u2) ** 2 / taup)
nocap = sp.simplify(sp.limit(du2, r1, 0))
ST["L6"] = chk("L6_multistream", L6rel == 0 and L6P == 0 and KErel == 0 and nocap == 0,
               f"d(u1-u2)/dt + (u1-u2)/tau = {L6rel}; total momentum change {L6P}; relative KE decays at 2/tau (residual {KErel}); "
               f"stream with no own dust (rho_1 -> 0): du2/dt = {nocap} (no capture)")
# L7: second law against a bath at T_J
sdens = rhop * (sp.Rational(3, 2) * sp.log(TTp) - sp.log(rhop))
dTdt = (TJp - TTp) / taup
dsdt = sp.diff(sdens, TTp) * dTdt
Qh = sp.Rational(3, 2) * rhop * (TJp - TTp) / taup
clau = sp.simplify(dsdt - Qh / TJp - sp.Rational(3, 2) * rhop * (TJp - TTp) ** 2 / (taup * TTp * TJp))
ST["L7"] = chk("L7_second_law", clau == 0,
               f"dS_d/dt - Q/T_J - (3/2)(rho/tau)(T_J - T)^2/(T T_J) = {clau} (>= 0); cooling branch T > T_J: dS_d/dt = "
               f"{sp.factor(dsdt)} < 0, so R must absorb entropy -Q/T_J > 0")
# f1 / d: characteristics and the cold stream
tlim = sp.limit(mom(Mx(rhop, uu_, TTp), 2), TTp, 0)
d_cold = sp.simplify(tlim - rhop * uu_ ** 2) == 0
P(f"  f1: the kinetic operator d_t + v.grad_x - grad Phi.grad_v has characteristics dx/dt = v, dv/dt = -grad Phi (speed |v| << c); "
  f"collision term local in x, finite tau. d: M[rho,u,T -> 0] second moment -> {tlim} (= cold stream): C[cold stream] = 0 when T_J = 0: {d_cold}")
RES["sympy"] = dict(H0=str(sp.factor(eKT)), Krho=str(sp.factor(cKR0)), L1_stress=str(stress), L4_cov=str(cov), L7=str(clau))
rss_guard("sympy")

# ================================================================================================ MAIN: (a) NGC 3198 stationary state, BTFR, selection (L5)
P("\n==================== (a) THE LAW FOR ISOLATED RELAXED HOSTS ====================")
A = {}; L5 = {}
r0 = 0.1 * KPC
Cs_scan = np.geomspace(1e-2, 1e2, 401)


def scan_and_roots(tab, Mc, label):
    Mend, _ = rk4_hydro(tab, Cs_scan)
    vals = Mend / Mc - 1.0
    Fs = lambda c: float(rk4_hydro(tab, [c])[0][0] / Mc - 1.0)
    roots = []
    for i in range(len(Cs_scan) - 1):
        if vals[i] * vals[i + 1] <= 0:
            roots.append(brentq(Fs, Cs_scan[i], Cs_scan[i + 1], xtol=1e-13, rtol=1e-12))
    f1 = Fs(1.0)
    uniq = (len(roots) == 1 and abs(roots[0] - 1) <= 1e-6)
    mono = bool(np.all(np.diff(vals) > 0) or np.all(np.diff(vals) < 0))
    P(f"     L5 {label:26s}: F(C=1) = {f1:+.2e}; roots {['%.9f' % x_ for x_ in roots]}; F range {vals.min():+.3f} .. {vals.max():+.3f}; "
      f"monotone {mono} -> {'UNIQUE' if uniq else 'NOT UNIQUE'}")
    return dict(F1=f1, roots=roots, unique=uniq, Fmin=float(vals.min()), Fmax=float(vals.max()), monotone=mono)


for foot in FOOTS:
    a0 = A0[foot]
    for kz in KERN:
        md = ngc_model(kz, a0)
        m_v, dm_v, law_v, dlaw_v = ngc_vec(kz, a0, md)
        tab = hydro_tables(m_v, dm_v, law_v, dlaw_v, G_SI, r0, md["r_e"])
        rmean = md["Mc"] / (4 * np.pi / 3 * md["r_e"] ** 3)
        Mend, path = rk4_hydro(tab, [1.0], keep_path=True)
        xn = tab["x"][::2]; Mdn = path[:, 0]
        Mdi = PchipInterpolator(np.log(xn), Mdn)
        ydeep = {y: math.sqrt(G_SI * MB_N * MSUN / (y * a0)) for y in (1e-2, 1e-3)}
        Rin = R_N[R_N > r0]
        gm = G_SI * (m_v(Rin) + Mdi(np.log(Rin))) / Rin ** 2; glw = law_v(G_SI * m_v(Rin) / Rin ** 2)
        a1 = float(np.max(np.abs(gm / glw - 1)))
        deep = {}
        for y, rd in ydeep.items():
            gmd = G_SI * (float(m_v(np.array([rd]))[0]) + float(Mdi(math.log(rd)))) / rd ** 2
            gld = float(law_v(G_SI * MB_N * MSUN / rd ** 2))
            deep[f"y={y:g}"] = dict(r_kpc=rd / KPC, inside=bool(rd < md["r_e"]), dev=abs(gmd / gld - 1),
                                    V4_over_GMa0=(gld * rd) ** 2 / (G_SI * MB_N * MSUN * a0))
        neg = tab["neg"]
        A[f"{foot}|{kz}"] = dict(a1=a1, deep=deep, neg_density=neg, min_rho_over_mean=float(np.nanmin(tab["rho"]) / rmean),
                                 r_e_kpc=md["r_e"] / KPC, r_e_E7_kpc=md["dom"]["r_e"] / KPC, n_eval=int(Rin.size),
                                 Md_end_over_Mc=float(Mend[0] / md["Mc"]))
        P(f"  a1/a2 [{foot}, {kz}]: max |g/g_law - 1| at {Rin.size} radii = {a1:.2e}; deep y=1e-2 {deep['y=0.01']['dev']:.2e} "
          f"(V^4/GMa0 {deep['y=0.01']['V4_over_GMa0']:.3f}), y=1e-3 {deep['y=0.001']['dev']:.2e} ({deep['y=0.001']['V4_over_GMa0']:.3f}); "
          f"r_e = {md['r_e'] / KPC:.1f} kpc (E7 {md['dom']['r_e'] / KPC:.1f}); phantom density negative anywhere: {neg} "
          f"(min rho_ph / mean {np.nanmin(tab['rho']) / rmean:.3e})")
        L5[f"NGC3198|{foot}|{kz}"] = scan_and_roots(tab, md["Mc"], f"NGC 3198 {foot} {kz}")
        rss_guard("a1")
# toy (G = a0 = 1, Plummer, simple law, r_* = 10)
tt_m = lambda x: t_Mb(x)
tt_dm = lambda x: 3 * TMB * TAB ** 2 * x * x / (x * x + TAB * TAB) ** 2.5
ttab = hydro_tables(tt_m, tt_dm, lambda gn: law_simple(gn, TA0), lambda gn: dlaw("simple", gn, TA0), TG, 1e-3, RSTAR)
L5["toy"] = scan_and_roots(ttab, T_MC, "toy (Plummer, r_* = 10)")
L5_unique = all(v["unique"] for v in L5.values())
P(f"  L5: {'UNIQUE everywhere' if L5_unique else 'NOT UNIQUE somewhere'} (NGC 3198 both footings and kernels, and the toy)")
RES["a_static"] = A; RES["L5"] = L5

# ---- a3 dynamics, L1 fast probe
P("  a3 / L1: spherical shell toy (K-T at T1 = tau_ff/(2 alpha), alpha = 1; fast probe x0.1)")
TOY = {}
TOY["KT_L"] = run_toy("L"); rss_guard("toy L")
TOY["KT_I"] = run_toy("I"); rss_guard("toy I")
TOY["KT_S"] = run_toy("S"); rss_guard("toy S")
TOY["KTfast_I"] = run_toy("I", tau_fac=0.1); rss_guard("toy fast")
RES["toy"] = TOY
a3 = TOY["KT_L"]["on_law"] and TOY["KT_I"]["on_law"]
a1_all = all(v["a1"] <= 1e-6 and not v["neg_density"] for v in A.values())
a2_all = all(d["dev"] <= 1e-6 and d["inside"] for v in A.values() for d in v["deep"].values())
if a1_all and a2_all and a3 and L5_unique:
    GA = "PASS"
elif a1_all and a2_all and ((TOY["KT_L"]["on_law"] and not TOY["KT_I"]["on_law"]) or (not L5_unique and a3)):
    GA = "CONDITIONAL"
else:
    GA = "FAIL"
P(f"  (a): a1 {a1_all}, a2 {a2_all}, a3 {a3} (IC-L {TOY['KT_L']['on_law']}, IC-I {TOY['KT_I']['on_law']}, IC-S {TOY['KT_S']['on_law']} reported), "
  f"L5 {L5_unique} -> {GA}")
tf01 = TOY["KTfast_I"]["t_first_L1"][0.1]
L1_limit = (tf01 is not None) and (tf01 <= 0.1 * T_EDGE)
P(f"  L1: fast probe first L1 < 0.1 at t = {tf01} vs 0.1 t_e = {0.1 * T_EDGE:.2f} -> {'LIMIT' if L1_limit else 'NOT a tau -> 0 limit'}; "
  f"T1 run first L1 < 0.1 at {TOY['KT_I']['t_first_L1'][0.1]}, < 0.2 at {TOY['KT_I']['t_first_L1'][0.2]}")
ST["L1_limit"] = L1_limit

# ================================================================================================ MAIN: L2 / (e) planar toy, (b1)
P("\n==================== (e) CONSERVATION AND (b1) HOVER: PLANAR TOY ====================")
PL = {}
for case in ("ER", "ES", "EM"):
    off = planar_run(case, "off"); kt = planar_run(case, "KT")
    ok = (kt["maxdP"] <= 1e-10) and (kt["maxdE"] <= 2 * off["maxdE"] + 1e-10)
    PL[case] = dict(KT={k: v for k, v in kt.items() if k != "track"}, off={k: v for k, v in off.items() if k != "track"}, pass_=ok)
    P(f"  {case}: N {kt['N']} sheets (mass exact by count); K-T |dP|/(M v_ref) {kt['maxdP']:.2e}; booked |dE|/|E| {kt['maxdE']:.2e} vs "
      f"integrator (relax off) {off['maxdE']:.2e}; E_R {kt['E_R']:+.3f}; CM slip {kt['max_cm_slip']:.2e}; M1 switches {kt['nswitch']}, "
      f"max T_J jump {kt['Tjump']:.3f} T0; J (mass moved per unit time / M) {kt['J_per_unit_time']:.3f} (off {off['J_per_unit_time']:.3f}) -> {'PASS' if ok else 'FAIL'}")
    rss_guard(case)
krho = planar_run("ER", "Krho"); krho_u = planar_run("ER", "Krho_u")
L2 = PL["ER"]["KT"]["maxdP"] <= 1e-10 and (krho["max_cm_slip"] / 5.0 >= 1e-3)
ST["L2"] = chk("L2_momentum", L2, f"K-T |dP|/(M v_ref) {PL['ER']['KT']['maxdP']:.2e} (R = 0: mass moves only with the flow); K-rho CM slip "
               f"{krho['max_cm_slip'] / 5.0:.3e} x_e (keep velocity), |dP|/(M v_ref) {krho_u['maxdP']:.2e} (local velocity)")
PL["Krho"] = {k: v for k, v in krho.items() if k != "track"}; PL["Krho_u"] = {k: v for k, v in krho_u.items() if k != "track"}
GE_ = "PASS" if all(PL[c]["pass_"] for c in ("ER", "ES", "EM")) else "FAIL"
P(f"  (e): {GE_}")
b1r = planar_run("B1", "KT", g_ext=1.0)
trk = np.array(b1r["track"]); tt_ = trk[:, 0]; sep = trk[:, 1]
win_ = tt_ >= 25.0
eps_b1 = float(np.max(2 * np.abs(sep[win_] - sep[0]) / (1.0 * tt_[win_] ** 2)))
b1_ok = eps_b1 <= 1e-2
P(f"  b1: satellite in a uniform field g = 1, t = 50: fitted eps = {eps_b1:.2e} (line 1e-2); |dP + M g t|/(M v_ref) {b1r['maxdP']:.2e} -> "
  f"{'PASS' if b1_ok else 'FAIL'}")
PL["B1"] = dict(eps=eps_b1, maxdP=b1r["maxdP"], max_sep=float(np.max(np.abs(sep - sep[0]))))
RES["planar"] = PL

# ================================================================================================ MAIN: (b2)-(b4) satellites, drag, Bullet
P("\n==================== (b) SATELLITES: EFE, DRAG, BULLET ====================")
SAT = {}
b3_pass_by_tau = {}
for foot in FOOTS:
    a0 = A0[foot]
    domh = domain(HOST938, a0)
    for tname, (kind, par) in tau_candidates(foot).items():
        worst = 0.0; worst_dc = 0.0; allok = True; rows = {}
        for nm, Mb, apc in HOSTS882:
            for rk in RHOST:
                d = rk * KPC847; Mh = HOST938 * MSUN847
                rho_h, _ = point_phantom_density(Mh, a0, d)
                gh = float(law_simple(G_SI * Mh / d ** 2, a0)); V = math.sqrt(gh * d)
                a = apc * PC; Ms = Mb * MSUN847
                Mf, rhob = plum(Ms, a)

                def drag_at(x):
                    rho_s, _ = phantom_density(Mf, a0, x)
                    vc = math.sqrt(glaw_of(Mf, a0, x) * x)
                    tau = tau_value(kind, par, rhob(x) + rho_s + rho_h, x, vc)
                    return rho_h / (rho_s + rho_h) * V / tau, glaw_of(Mf, a0, x), rho_s
                ad_a, gi_a, rs_a = drag_at(a)
                eps_a = ad_a / gh
                ad_2a, _, _ = drag_at(2 * a)
                xs = np.geomspace(0.01 * a, 100 * a, 400)
                fv = np.array([drag_at(x)[0] - drag_at(x)[1] for x in xs])
                over = np.where(fv > 0)[0]
                r_s = float(xs[over[0]]) if len(over) else float("inf")
                if r_s < a:
                    _, Mph_rs = phantom_density(Mf, a0, r_s); _, Mph_a = phantom_density(Mf, a0, a)
                    dlt = math.log10((Mf(a) + Mph_rs) / (Mf(a) + Mph_a))
                else:
                    dlt = 0.0
                # dust-mass-weighted mean drag inside 2a
                xw = np.linspace(0.02 * a, 2 * a, 120)
                wts = np.array([phantom_density(Mf, a0, x)[0] * x * x for x in xw]); adw = np.array([drag_at(x)[0] for x in xw])
                eps_w = float(np.sum(wts * adw) / np.sum(wts) / gh)
                doms = domain(Mb, a0)
                s_M1 = (d / domh["r_on"]) * doms["r_on"]
                ok = (eps_a <= EPS_B[foot]) and (abs(dlt) <= DELTA_C)
                allok = allok and ok
                worst = max(worst, eps_a); worst_dc = max(worst_dc, abs(dlt))
                rows[f"{nm}|{rk:.0f}"] = dict(eps_a=eps_a, eps_2a=ad_2a / gh, eps_w2a=eps_w, r_s_over_a=r_s / a, delta=dlt,
                                              s_M1_kpc=s_M1 / KPC, a_kpc=a / KPC, r_e_sat_kpc=doms["r_e"] / KPC, rho_h_over_rho_s_a=rho_h / rs_a)
        SAT[f"{foot}|{tname}"] = dict(rows=rows, worst_eps_a=worst, worst_delta=worst_dc, pass_=allok)
        b3_pass_by_tau.setdefault(tname.split("(")[0] if tname.startswith("T1") else tname, {})[foot] = allok
        P(f"  b3 [{foot}, {tname:14s}]: worst eps_drag(a) = {worst:.3e} (line {EPS_B[foot]}); worst |delta| = {worst_dc:.3f} dex (line {DELTA_C}); "
          f"H3@50 eps(a) {rows['H3|50']['eps_a']:.3e}, eps(2a) {rows['H3|50']['eps_2a']:.3e}, r_s/a {rows['H3|50']['r_s_over_a']:.2f} -> {'PASS' if allok else 'FAIL'}")
P("  b2: own-domain monopole T_J -> EFE 0 dex at monopole order (L4). M1 own-domain radius s_M1 vs a and r_e,sat (canonical, T1 rows):")
for k_, v_ in SAT["canonical|T1"]["rows"].items():
    P(f"     {k_:8s}: s_M1 {v_['s_M1_kpc']:.3f} kpc, a {v_['a_kpc']:.3f} kpc, r_e,sat {v_['r_e_sat_kpc']:.3f} kpc; rho_h/rho_s(a) {v_['rho_h_over_rho_s_a']:.2e}")
b2_ok = bool(ST["L4_sym"]) and all(v_["s_M1_kpc"] >= v_["a_kpc"] for f in FOOTS for v_ in SAT[f"{f}|T1"]["rows"].values())
# Bullet report
BUL = {}
for foot in FOOTS:
    a0 = A0[foot]
    Mm, Ms_ = 1.5e14 * MSUN847, 1.5e13 * MSUN847
    rm, rs_ = 250 * KPC847, 50 * KPC847
    rhom_, _ = point_phantom_density(Mm, a0, rm); rhos_, _ = point_phantom_density(Ms_, a0, rs_)
    tx_ = 2 * 250 * KPC847 / 2666.7e3
    vcm = math.sqrt(float(law_simple(G_SI * Mm / rm ** 2, a0)) * rm)
    for tname, (kind, par) in tau_candidates(foot).items():
        tau = tau_value(kind, par, rhom_ + rhos_, rm, vcm)
        BUL[f"{foot}|{tname}"] = 1 - math.exp(-tx_ * rhom_ / ((rhom_ + rhos_) * tau))
    P(f"  b4 Bullet [{foot}] (reported): fraction of the sub's dust relative momentum removed per core crossing: "
      + ", ".join(f"{k.split('|')[1]} {v:.3f}" for k, v in BUL.items() if k.startswith(foot)))
RES["satellites"] = SAT; RES["bullet"] = BUL

# ================================================================================================ MAIN: (c) slip, (d) growth
P("\n==================== (c) SLIP, (d) GROWTH ====================")
SL = {}
worst_g = worst_8 = 0.0
for foot in FOOTS:
    a0 = A0[foot]
    for name, Mb, rk_ in SYS847:
        M = Mb * MSUN847; rr_ = rk_ * KPC847
        dom = domain(Mb, a0)
        Mph_f = lambda x: x * x * (float(law_simple(G_SI * M / x ** 2, a0)) - G_SI * M / x ** 2) / G_SI
        r_e = brentq(lambda x: Mph_f(x) - dom["Mc"] * MSUN, 1e-3 * rr_, 1e6 * rr_) if Mph_f(1e6 * rr_) > dom["Mc"] * MSUN else dom["r_e"]
        rho_ph = lambda x: (Mph_f(x * (1 + 1e-6)) - Mph_f(x * (1 - 1e-6))) / (2e-6 * x) / (4 * math.pi * x * x)
        gl_ = lambda x: G_SI * (M + Mph_f(x)) / x ** 2
        if rr_ < r_e:
            pint = quad(lambda l: math.exp(l) * rho_ph(math.exp(l)) * gl_(math.exp(l)), math.log(rr_), math.log(r_e), limit=200, epsrel=1e-10)[0]
        else:
            pint = 0.0
        g_ = gl_(rr_); vc2 = g_ * rr_
        sg = 4 * math.pi * G_SI * rr_ * pint / (C_SI ** 2 * g_); s8 = 8 * math.pi * G_SI * rr_ ** 2 * pint / (C_SI ** 2 * vc2)
        SL[f"{foot}|{name}"] = dict(s_grad=sg, s_847=s8, TJ_over_vc2=(pint / rho_ph(rr_)) / vc2, r_e_kpc=r_e / KPC)
        worst_g = max(worst_g, sg); worst_8 = max(worst_8, s8)
GC = "PASS" if max(worst_g, worst_8) <= 1.9e-5 else "FAIL"
P(f"  (c) slip with p = rho_ph T_J (exact T_J, own edges): worst s_grad {worst_g:.3e}, worst s_847 {worst_8:.3e} (line 1.9e-5) -> {GC}; "
  f"T_J/v_c^2 at the systems' radii: " + ", ".join(f"{k} {v['TJ_over_vc2']:.3f}" for k, v in SL.items() if k.startswith("canonical")))
RES["slip"] = SL
# top-hat (CFG947 check reused): mean density at turnaround 9 pi^2/16 at delta_lin = 1.0624
th_ = sp.symbols("theta", positive=True)
dens_ta = sp.N(9 * sp.pi ** 2 / 16)
dlin = float(sp.N(sp.Rational(3, 5) * (sp.Rational(3, 4) * sp.pi) ** sp.Rational(2, 3)))
GD = "PASS" if (abs(n_dust - 1) <= 1e-12 and d_cold and abs(float(dens_ta) - 5.5517) < 1e-4 and abs(dlin - 1.0624) < 1e-4) else "FAIL"
P(f"  (d): dust n = {n_dust:.12f}; C[cold stream] = 0 with T_J = 0: {d_cold}; top-hat turnaround 9pi^2/16 = {float(dens_ta):.4f} at "
  f"delta_lin = {dlin:.4f}: no domain before turnaround -> {GD}")

# ================================================================================================ MAIN: L3 RMIN, SPARC
P("\n==================== L3: RMIN IS RESOLUTION ====================")
L3 = {}
for foot in FOOTS:
    a0 = A0[foot]
    dx_phys = 2 * (100.0 / 1024) / HE * MPCE                         # 2 cells, comoving = physical at z = 0 (metres)
    Mres = brentq(lambda lm: domain(10 ** lm, a0)["r_e"] - dx_phys, 6.0, 13.0)
    L3[foot] = dict(Mb_res=10 ** Mres)
    sp_own = sparc_rms(a0, pred_own, f"K-T relaxed, own domains ({foot})")
    L3[foot]["sparc_own"] = sp_own
    # phantom-density positivity across SPARC (discrete, nu_mono, Upsilon of the footing's best fit)
    U = 0.61 if foot == "canonical" else 0.57
    nneg = 0
    for g in sparc_setup():
        Rm = g["R"] * 3.0857e19
        VB2 = np.sign(g["Vg"]) * g["Vg"] ** 2 + U * g["Vd"] ** 2 + 1.4 * U * g["Vb"] ** 2
        GB = VB2 * 1e6 / Rm
        ok = np.isfinite(GB) & (GB > 0)
        if ok.sum() < 2: continue
        gp = law_mono(GB[ok], a0); Mph_i = Rm[ok] ** 2 * (gp - GB[ok]) / G_SI
        nneg += int(np.any(np.diff(Mph_i) < 0))
    L3[foot]["sparc_negative_phantom_galaxies"] = nneg
    nbetween = 0
    for g in sparc_setup():
        Rm = g["R"] * 3.0857e19; GB = (np.sign(g["Vg"]) * g["Vg"] ** 2 + 0.61 * g["Vd"] ** 2 + 1.4 * 0.61 * g["Vb"] ** 2) * 1e6 / Rm
        mb = _mb_last(GB, Rm)
        if mb is not None and L3[foot]["Mb_res"] <= mb < 2.19e11:
            nbetween += 1
    L3[foot]["sparc_between_res_and_engine"] = nbetween
    P(f"  [{foot}] PM resolution floor (r_e >= 2 dx): M_b,res = {10 ** Mres:.3e} M_sun (engine effective 2.19e11, x{2.19e11 / 10 ** Mres:.1f}); "
      f"SPARC galaxies between the two: {nbetween}; SPARC galaxies with a decreasing discrete M_ph somewhere: {nneg} of {len(sparc_setup())}")
RES["L3"] = L3

# ================================================================================================ MAIN: tau (§3)
P("\n==================== WHAT SETS TAU (§3) ====================")
N5 = json.load(open(os.path.join(LANES, "CFG939_lagrangian_displacement_shell_crossing", "cfg939_results.json")))["N5"]
SYSP = c939_systems()
FOOTK = {"canonical": 9.3603e-11 * KPC847 / 1e6, "alt": 1.1312e-10 * KPC847 / 1e6}
TAUT = {}
for foot in FOOTS:
    a0k = FOOTK[foot]
    rows = {}
    for rw in N5[foot]:
        nm = rw["name"]; r12 = rw["r_half_kpc"]
        prof = SYSP[nm]
        rho_b = prof[1](r12) / (4 * math.pi * r12 ** 2)
        g = (rw["gN_over_a0"] + rw["x_u_over_a0"]) * a0k
        V = math.sqrt(g * r12)
        rho_m = rho_b + rw["rho_ph_Msun_kpc3"]
        t_ff = 1.0 / math.sqrt(4 * math.pi * GK * rho_m) * GYRK
        t_orb = 2 * math.pi * r12 / V * GYRK
        rho_star = (SYSP["cluster-stars"][1](r12) / (4 * math.pi * r12 ** 2)) if nm == "cluster-core" else rho_b
        sig = V / math.sqrt(2)
        t2b = 0.34 * sig ** 3 / (GK ** 2 * 1.0 * max(rho_star, 1e-300) * 10.0) * GYRK
        frac5 = maxwell_frac(rw["v_in_kms"] / sig)
        rows[nm] = dict(cls=rw["cls"], r12=r12, age=rw["age_Gyr"], V=V, t_ff=t_ff, t_orb=t_orb, t2b=t2b, T5_frac=frac5,
                        collapsed=rw["collapsed"])
    rows["SPARC-slowest"] = dict(cls="SPARC rotators", r12=None, age=8.0, V=None, t_ff=2.91 / (2 * math.pi), t_orb=2.91, t2b=float("inf"),
                                 T5_frac=None, collapsed=True)
    TAUT[foot] = rows
cands_all = {}
for foot in FOOTS:
    rows = TAUT[foot]
    for tname, (kind, par) in tau_candidates(foot).items():
        out = {}
        for nm, rw in rows.items():
            if kind == "ff": tau = rw["t_ff"] / (2 * ALPHA)
            elif kind == "orb": tau = par * rw["t_orb"]
            else: tau = par
            R_ = 1 - math.exp(-rw["age"] / tau)
            out[nm] = dict(tau=tau, R=R_, state=("ON LAW" if R_ >= 0.9 else ("NATIVE" if R_ <= 0.1 else "MIXED")))
        rot_on = all(out[n]["state"] == "ON LAW" for n in ("SPARC-dwarf", "MW-like", "SPARC-slowest"))
        cl_on = out["cluster-core"]["state"] == "ON LAW"
        cl_nat = out["cluster-core"]["state"] == "NATIVE"
        tauP = rot_on and cl_on
        tauF = rot_on and cl_nat
        cands_all[f"{foot}|{tname}"] = dict(rows=out, tauP=tauP, tauF=tauF, R_cluster=out["cluster-core"]["R"])
    # T4 two-body and T5 capture gate
    t4 = {nm: dict(tau=rw["t2b"], R=1 - math.exp(-rw["age"] / rw["t2b"]) if math.isfinite(rw["t2b"]) else 0.0) for nm, rw in rows.items()}
    cands_all[f"{foot}|T4"] = dict(rows={nm: dict(v, state=("ON LAW" if v["R"] >= 0.9 else ("NATIVE" if v["R"] <= 0.1 else "MIXED"))) for nm, v in t4.items()},
                                   tauP=False, tauF=False, R_cluster=t4["cluster-core"]["R"])
    cands_all[f"{foot}|T4"]["tauP"] = all(cands_all[f"{foot}|T4"]["rows"][n]["state"] == "ON LAW" for n in ("SPARC-dwarf", "MW-like")) and \
        cands_all[f"{foot}|T4"]["rows"]["cluster-core"]["state"] == "ON LAW"
    t5 = {nm: rw["T5_frac"] for nm, rw in rows.items() if rw["T5_frac"] is not None}
    cands_all[f"{foot}|T5"] = dict(fracs=t5, tauP=all(t5[n] >= 0.5 for n in ("SPARC-dwarf", "MW-like", "cluster-core")), tauF=False)
for foot in FOOTS:
    P(f"  [{foot}] class rows (r_half kpc, age Gyr, tau_ff Gyr, t_orb Gyr, two-body Gyr, T5 fraction below V_esc,b):")
    for nm, rw in TAUT[foot].items():
        P(f"     {nm:15s} r {rw['r12'] if rw['r12'] is None else round(rw['r12'], 3)!s:>8s} age {rw['age']:5.2f} t_ff {rw['t_ff']:.3e} "
          f"t_orb {rw['t_orb']:.3e} t_2b {rw['t2b']:.2e} T5 {rw['T5_frac'] if rw['T5_frac'] is None else round(rw['T5_frac'], 3)}")
    for tname in list(tau_candidates(foot).keys()) + ["T4", "T5"]:
        c = cands_all[f"{foot}|{tname}"]
        if tname == "T5":
            P(f"     {tname:14s}: fraction of the relaxed law-state Maxwellian below V_esc,b: " + ", ".join(f"{k} {v:.3f}" for k, v in c["fracs"].items())
              + f" -> tau-P {c['tauP']}, tau-F {c['tauF']}")
            continue
        P(f"     {tname:14s}: " + ", ".join(f"{n} {c['rows'][n]['state']}({c['rows'][n]['R']:.3f})" for n in
                                         ("SPARC-dwarf", "MW-like", "SPARC-slowest", "cluster-core", "Draco-like", "UFD-c") if n in c["rows"])
          + f" -> tau-P {c['tauP']}, tau-F {c['tauF']}")
# ordering check
ORD = {}
for foot in FOOTS:
    rows = TAUT[foot]
    for tk in ("t_ff", "t_orb"):
        rot = min(rows[n]["age"] / rows[n][tk] for n in ("SPARC-dwarf", "MW-like", "SPARC-slowest"))
        cl = rows["cluster-core"]["age"] / rows["cluster-core"][tk]
        ORD[f"{foot}|{tk}"] = dict(ratio=rot / cl, need=math.log(10) / math.log(10 / 9), possible=rot / cl >= math.log(10) / math.log(10 / 9))
        P(f"  ordering [{foot}, {tk}]: min_rotators(age/t) / cluster(age/t) = {rot / cl:.3f} (needs >= 21.85) -> "
          f"{'a constant exists' if rot / cl >= 21.85 else 'NO proportionality constant gives tau-F'}")
any_tauF = any(v.get("tauF") for v in cands_all.values())
any_tauP = {foot: [k.split("|")[1] for k, v in cands_all.items() if k.startswith(foot) and v.get("tauP")] for foot in FOOTS}
P(f"  tau verdict: tau-F passed by {'some candidate' if any_tauF else 'NO candidate'}; tau-P passed by canonical {any_tauP['canonical']}, alt {any_tauP['alt']}")
P(f"  {'A DERIVED SELECTOR FOR CFG949 EXISTS' if any_tauF else 'NO RECORD-DERIVED TAU WORKS: no candidate makes cluster cores native while keeping rotators on the law'}")
# T-EX
D4c = json.load(open(os.path.join(LANES, "CFG930_energy_limited_settling", "cfg930_results.json")))["diagnostics"]
qmed = {f: {k: v["median"] for k, v in D4c[f]["D4"].items()} for f in FOOTS}
TEX = all(max(qmed[f].values()) < 1 for f in FOOTS)
ST["T-EX"] = chk("T-EX_excess_unreachable", TEX, "CFG930 D4 median Q_ap: " + "; ".join(f"{f}: " + ", ".join(f"{k} {v:.3f}" for k, v in qmed[f].items()) for f in FOOTS)
                 + " -> every relaxed/unrelaxed mixture sits at or below the law at the aperture: no tau gives the dSph or UDG excess")
# cluster amplitude mixture (reported)
K949 = json.load(open(os.path.join(LANES, "CFG949_clusters_untethered", "cfg949_results_K.json")))["K"]["K1"]
B0 = json.load(open(os.path.join(LANES, "CFG949_clusters_untethered", "cfg949_results.json")))["main"]["B0_primary"]["A"]
MIX = {}
for foot in FOOTS:
    AL = K949["A_can"] if foot == "canonical" else K949["A_alt"]
    for tname in tau_candidates(foot):
        Rc = cands_all[f"{foot}|{tname}"]["R_cluster"]
        mid = 1 / (Rc / AL["MID"][0] + (1 - Rc) / B0["MID"][0]); outr = 1 / (Rc / AL["OUTER"][0] + (1 - Rc) / B0["OUTER"][0])
        sm = mid * (Rc * AL["MID"][1] / AL["MID"][0] + (1 - Rc) * B0["MID"][1] / B0["MID"][0])
        so = outr * (Rc * AL["OUTER"][1] / AL["OUTER"][0] + (1 - Rc) * B0["OUTER"][1] / B0["OUTER"][0])
        MIX[f"{foot}|{tname}"] = dict(R=Rc, A_MID=mid, Z_MID=(mid - 1) / sm, A_OUTER=outr, Z_OUTER=(outr - 1) / so)
    P(f"  cluster bands (reported, harmonic mixture of CFG687 law and CFG949 B0) [{foot}]: " + "; ".join(
        f"{k.split('|')[1]} R {v['R']:.2f}: MID {v['A_MID']:.2f} (Z {v['Z_MID']:+.1f}), OUTER {v['A_OUTER']:.2f} (Z {v['Z_OUTER']:+.1f})"
        for k, v in MIX.items() if k.startswith(foot)))
RES["tau"] = dict(table=TAUT, candidates=cands_all, ordering=ORD, any_tauF=any_tauF, tauP=any_tauP, T_EX=qmed, cluster_mix=MIX)

# (b) grade per the frozen rule: PASS iff b1, b2 pass and b3 passes for at least one candidate passing tau-P
tauP_names = {foot: set(any_tauP[foot]) for foot in FOOTS}
b3_tauP = {foot: [t for t in tau_candidates(foot) if t in tauP_names[foot] and SAT[f"{foot}|{t}"]["pass_"]] for foot in FOOTS}
b3_any = {foot: [t for t in tau_candidates(foot) if SAT[f"{foot}|{t}"]["pass_"]] for foot in FOOTS}
if b1_ok and b2_ok and all(b3_tauP[f] for f in FOOTS):
    GB_ = "PASS"
elif b1_ok and b2_ok and all(b3_any[f] for f in FOOTS):
    GB_ = "CONDITIONAL"
else:
    GB_ = "FAIL"
P(f"  (b): b1 {b1_ok}, b2 {b2_ok}; b3 passes with tau-P candidates: canonical {b3_tauP['canonical']}, alt {b3_tauP['alt']} -> {GB_}")

# ================================================================================================ MAIN: energy (§4)
P("\n==================== ENERGY (§4) ====================")
EN = {}
for foot, fk in (("canonical", "can"), ("alt", "alt")):
    for sysn in ("UFD-c", "Draco-like", "SPARC-dwarf", "MW-like", "cluster-core"):
        EN[f"{foot}|{sysn}"] = dict(E_x_erg=PHYS["systems"][fk][sysn]["E_x_a_erg"], E_x_over_Mc2=PHYS["systems"][fk][sysn]["E_x_over_Mcat_c2"])
    P(f"  E1 [{foot}] net exchange per host (dust -> R; = CFG935's E_x, same end state): " + ", ".join(
        f"{s} {PHYS['systems'][fk][s]['E_x_a_erg']:.2e} erg ({PHYS['systems'][fk][s]['E_x_over_Mcat_c2']:.1e} M_cat c^2)" for s in
        ("UFD-c", "UFD-e", "Draco-like", "Fornax-like", "SPARC-dwarf", "MW-like", "cluster-core")))
    for sysn, rown in (("MW-like", "MW-like"), ("cluster-core", "cluster-core")):
        pw = {}
        for tname in tau_candidates(foot):
            tau = cands_all[f"{foot}|{tname}"]["rows"][rown]["tau"] * GYR_S
            pw[tname] = PHYS["systems"][fk][sysn]["E_x_a_erg"] / tau
        EN[f"{foot}|{sysn}|power_erg_s"] = pw
        P(f"     power E_x/tau [{sysn}]: " + ", ".join(f"{k} {v:.2e} erg/s ({v / 3.828e33:.1e} L_sun)" for k, v in pw.items()))
P(f"  E1 toy (booked E_R; + = energy held by R): IC-I {TOY['KT_I']['E_R_end']:+.3f}, IC-S {TOY['KT_S']['E_R_end']:+.3f}, IC-L {TOY['KT_L']['E_R_end']:+.3f}; "
  f"start-minus-law energies: IC-I {TOY['KT_I']['E0']['E_tot'] - TOY['KT_L']['E0']['E_tot']:+.3f}, IC-S {TOY['KT_S']['E0']['E_tot'] - TOY['KT_L']['E0']['E_tot']:+.3f}")
P(f"  E2 gross flows (cool = dust -> R / heat = R -> dust): IC-L {TOY['KT_L']['flow_cool']:.2f} / {TOY['KT_L']['flow_heat']:.2f}; "
  f"IC-I {TOY['KT_I']['flow_cool']:.2f} / {TOY['KT_I']['flow_heat']:.2f}; IC-S {TOY['KT_S']['flow_cool']:.2f} / {TOY['KT_S']['flow_heat']:.2f}. "
  "Under L7 the cooling flow needs R to absorb entropy: a coherent zero-entropy partner (CFG542 Pb) cannot be R")
E3 = "DOES NOT KILL"
P(f"  E3: CFG930's SN-energy ordering is NOT APPLICABLE (R is not baryonic feedback; its capacity is not tied to E_SN) -> {E3}; "
  f"T-EX {'holds' if TEX else 'fails'}: the excess family is unreachable at any tau")
P(f"  cosmic (CFG935, cited): drho_DE/rho_DE since z = 1 {PHYS['cosmic']['can']['drho_DE_over_rhoDE_z1']} (can); "
  f"new-radiation route Omega_rad <= {PHYS['cosmic']['can']['Omega_rad_new_max']}")
RES["energy"] = dict(per_host=EN, E3=E3)

# ================================================================================================ CLASSES
P("\n==================== CLASSES ====================")
GF = "CONDITIONAL"                                                    # f1 holds; the engine-faithful target is instantaneous -> C-ret
conservative_KT = bool(ST["H0"] and ST["L2"])
relation = "LIMIT" if (ST["L1_limit"]) else ("ATTRACTOR" if (TOY["KT_L"]["on_law"] and TOY["KT_I"]["on_law"]) else "NONE")
grades = dict(a=GA, b=GB_, c=GC, d=GD, e=GE_, f=GF)
krho_nc = (sp.simplify(cKR0) != 0) and ((PL["Krho"]["max_cm_slip"] / 5.0 >= 1e-3) or (PL["Krho_u"]["maxdP"] >= 1e-3))
P(f"  K-rho: mass moment {sp.factor(cKR0)}; CM slip {PL['Krho']['max_cm_slip'] / 5.0:.2e} x_e; |dP|/(M v_ref) (local-velocity form) "
  f"{PL['Krho_u']['maxdP']:.2e} -> {'NOT CONSERVATIVE' if krho_nc else 'conservative'}")
P(f"  K-T: conservative {conservative_KT}; grades " + ", ".join(f"({k}) {v}" for k, v in grades.items()) + f"; engine relation {relation}")
nofail = all(v != "FAIL" for v in grades.values())
tauP_any = any(len(v) for v in any_tauP.values())
# AMENDMENT A1.2: the frozen 'generic structural statement' clause applied test by test
fails = [k for k, v in grades.items() if v == "FAIL"]
generic = {"a": (not a3) and (not L5_unique),
           "b": all(not SAT[f"{f}|{t}"]["pass_"] for f in FOOTS for t in tau_candidates(f))}
covered = bool(fails) and all(generic.get(k, False) for k in fails)
P(f"  A1.2: FAILed tests {fails}; generic statement per FAIL: " + ", ".join(f"({k}) {'L5 (a3 fails, NOT UNIQUE)' if k == 'a' and generic['a'] else ('L6 (b3 fails for every tau)' if k == 'b' and generic['b'] else 'none')}" for k in fails))
if not K_ALL:
    overall = "VOID (a K control failed)"
elif conservative_KT and all(grades[k] == "PASS" for k in "abcde") and grades["f"] in ("PASS", "CONDITIONAL") and relation == "LIMIT" and tauP_any:
    overall = "ENGINE HAS A KINETIC PARENT"
elif conservative_KT and nofail and relation in ("LIMIT", "ATTRACTOR"):
    overall = "CONDITIONAL"
elif (not conservative_KT and krho_nc) or (conservative_KT and ((fails and covered) or relation == "NONE" and covered)):
    overall = "NO KINETIC PARENT"
else:
    overall = f"NOT CLASSIFIED BY THE FROZEN RULE (FAIL in {fails} without a listed generic structural statement)"
P(f"  OVERALL: {overall}")
P(f"  transfer of the T1x / T2x / NC1x shear passes: {'transfers' if relation == 'LIMIT' else 'NOT established; needs the 1024^3 KT run'}")
RES["classes"] = dict(Krho=("NOT CONSERVATIVE" if krho_nc else "conservative"),
                      KT=dict(conservative=conservative_KT, grades=grades, relation=relation, fails=fails, generic=generic), overall=overall)
dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
sys.exit(0 if K_ALL else 1)

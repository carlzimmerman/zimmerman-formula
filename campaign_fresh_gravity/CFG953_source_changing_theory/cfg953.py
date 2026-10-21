"""CFG953 -- the minimal source-changing non-local theory (SCT): construction and tests.
Criteria: FROZEN_CRITERIA.md (049a0f867, committed alone first).
Run (one core, one process, < 1 GB):
    CFG953_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg953.py      -> cfg953_K.out, cfg953_results_K.json
    CFG953_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg953.py     -> cfg953_MUTATE.out, cfg953_results_MUTATE.json
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg953.py                     -> cfg953.out, cfg953_results.json (K + main)
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite).
Machinery copied with attribution from CFG947 (cfg947.py: census, domain, kernels, K controls, slip, hover, SPARC statistic, T-M),
CFG941 (growth determinant, via CFG947) and CFG936 (stats / class rule).
kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib, csv
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import erf
import scipy.special as ssp
from scipy.stats import chi2 as CHI2

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG953_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG953_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
CRIT = "049a0f867"
OUT = []; RES = {"lane": "CFG953", "criteria": CRIT, "mutate": MUT, "stage": STAGE, "checks": {}}
T0 = time.time(); RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg953_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg953{TAG}.out"), "w").write("\n".join(OUT) + "\n")


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
MSUN847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's constants (as CFG938 / CFG941 / CFG947)
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0),
          ("cluster", 1.5e14, 1000.0)]
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]  # CFG882 Plummer dwarfs (M_sun, pc)
HOST938 = 6e10; RHOST = (50.0, 100.0, 250.0)                          # CFG938 S8 / CFG941 host (M_sun), radii (kpc)
EPS_B = {"canonical": 0.344, "alt": 0.317}                            # CFG945 differential free-fall bound
DELTA_C = 0.082                                                        # CFG874 / CFG945 satellite EFE room (dex)
# ---- the class-A engine's census constants (cfg947.py, verbatim)
OM_B, OM_C = 0.02237, 0.1200; FB = OM_B / (OM_B + OM_C)
GE, MSE, MPCE, HE = 6.674e-11, 1.989e30, 3.0857e22, 0.674
RMIN = 0.78125
EPS_SW = 0.077
_dta = json.load(open(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_delta_ta.json")))
DTA0 = float(_dta["D"][0]); assert abs(_dta["z"][0]) < 1e-12
RHOM_H = 0.315 * 2.775e11


def fret_of(lM):                                                        # cfg947.py fret_of (engine census), verbatim
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


def domain947(Mb_msun, a0):                                             # cfg947.py domain() (class-A E7 edge), verbatim
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


def nu_of(kern, y):
    return float(KERN[kern](y, 1.0) / y)


def q_edge(dom, kern):
    return dom["x"] * (nu_of(kern, dom["yE"]) - 1.0)


# ---- SCT's own domain (R1, R3): census supply, edge at the kernel's own supply root (point baryons beyond the data)
def Mph_pt(r, M, a0, kern):
    gn = G_SI * M / r ** 2
    return r * r * (float(KERN[kern](gn, a0)) - gn) / G_SI


def root_pt(M, Mc, a0, kern):
    rM = math.sqrt(G_SI * M / a0)
    return math.exp(brentq(lambda lr: Mph_pt(math.exp(lr), M, a0, kern) - Mc, math.log(1e-4 * rM), math.log(1e4 * rM),
                           xtol=1e-15, rtol=1e-15))


def domain_sct(Mb_msun, a0, kern="simple"):
    c = census(Mb_msun); Mc = (1 - FB) * c["Mta"]
    M = Mb_msun * MSUN; rM = math.sqrt(G_SI * M / a0)
    re = root_pt(M, Mc * MSUN, a0, kern)
    return dict(c, Mc=Mc, N=Mc / Mb_msun, r_on=c["R"] / HE * MPCE, r_e=re, rM=rM, yE=(rM / re) ** 2)


# ---- NGC 3198 (record SPARC file, Upsilon 0.61 as CFG938/941/947; spherical-equivalent m_N = r^2 g_bar / G)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MBR_N = GN_N * R_N ** 2 / G_SI
MB_N = MBR_N[-1] / MSUN

P("CFG953  the minimal source-changing non-local theory (SCT): construction and tests" + ("   [MUTATE]" if MUT else "")
  + f"   stage={STAGE}")
P(f"  criteria {CRIT}; kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2;  native Delta_ta(0) = {DTA0:.6f};"
  f"  engine f_b = {FB:.6f}")
P(f"  NGC 3198: {len(R_N)} radii to {R_N[-1] / KPC:.2f} kpc, M_b(< last) = {MB_N:.4e} M_sun (Upsilon 0.61)")
RES["inputs"] = dict(DTA0=DTA0, FB=FB, MB_NGC3198=MB_N, N_radii=int(len(R_N)))

# ================================================================================================ shared sympy (CFG947 / CFG941)
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


# ---- CFG941 hover machinery (via cfg947.py satellite_hover; tether on = local parent)
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
    law = KERN[kern]
    gbh = G_SI * HOST938 * MSUN847 / (rkpc * KPC847) ** 2
    gbs = plummer_g(Mb_sun * MSUN847, a_pc * PC, a_pc * PC)
    return math.log10(float((law(gbh + gbs, a0) - law(gbh, a0)) / law(gbs, a0)))


def retard_bound():                                                     # cfg947.py T-F loop (retardation bound), verbatim
    tf = {}
    for foot in FOOTS:
        a0 = A0[foot]
        for nm, Mb, apc in HOSTS882:
            for rk in RHOST:
                Rh = rk * KPC847; gbh = G_SI * HOST938 * MSUN847 / Rh ** 2; gh = float(law_simple(gbh, a0)); v2 = gh * Rh
                a = apc * PC; gbs = plummer_g(Mb * MSUN847, a, a); gph = float(law_simple(gbs, a0)) - gbs
                tf[f"{foot}|{nm}|{rk:.0f}"] = (gph / gh) * max(v2 / C_SI ** 2, gh * a / C_SI ** 2)
    return tf


# ---- SPARC: CFG4 statistic (cfg947.py sparc_rms, method copied; nu_mono)
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


def pred_sct(g, U, GB, Rm, a0):
    """SCT-M (spherical-equivalent convention): the law of own baryons inside the kernel's own supply root, Keplerian with
    M_b + M_c beyond (the body fully enclosed)."""
    gb = np.maximum(GB, 0); mb = _mb_last(GB, Rm)
    if mb is None:
        return law_mono(gb, a0), 0
    dom = domain_sct(mb, a0, "mono")
    gp = law_mono(gb, a0); beyond = Rm > dom["r_e"]
    if beyond.any():
        gp = np.where(beyond, G_SI * (mb + dom["Mc"]) * MSUN / Rm ** 2, gp)
    return gp, int(beyond.sum())


# ---- CFG936 statistic and class rule (cfg936.py stats / basic_class, verbatim)
def stats936(pts):
    r_ = np.array([p["r"] for p in pts]); s = np.array([p["s"] for p in pts]); n = len(r_)
    t_sd = float(np.std(r_, ddof=1) / math.sqrt(n)); t_me = float(math.sqrt(np.sum(s ** 2)) / n)
    se = max(t_sd, t_me); c2 = float(np.sum((r_ / s) ** 2)); p = float(CHI2.sf(c2, n))
    return dict(n=n, rbar=float(np.mean(r_)), se=se, se_scatter=t_sd, se_meas=t_me, chi2=c2, p=p, z_mean=float(np.mean(r_)) / se)


def basic_class936(st, rlaw):
    if abs(st["rbar"]) < 2 * st["se"] and st["p"] >= 0.05: return "EXPLAINS"
    if abs(st["rbar"]) <= 0.5 * abs(rlaw): return "PARTIAL"
    return "FAILS"


R936 = json.load(open(os.path.join(LANES, "CFG936_below_law_systems", "cfg936_results.json")))

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
K1 = chk("K1_CFG938_NGC3198_law", all(v < 1e-6 for v in k1.values()),
         f"max |g/g_law - 1| canonical {k1['canonical']:.2e}, alt {k1['alt']:.2e} (CFG938 2.2e-16; line 1e-6)")
RES["K1"] = k1
# K2: CFG947 no-hover retardation bound; CFG941 tethered hover / EFE
TF = retard_bound(); tfmax = max(TF.values())
hov = {}
for foot in FOOTS:
    for nm, Mb, apc in HOSTS882:
        for rk in RHOST:
            hov[f"{foot}|{nm}|{rk:.0f}"] = satellite_hover(Mb, apc, rk, A0[foot], tether=True)
rat = [v["ratio"] for v in hov.values()]; efd = [v["efe_dex"] for v in hov.values()]
K2 = chk("K2_CFG947_nohover_bound_CFG941_hover", abs(tfmax / 1.2114299321100668e-06 - 1) < 0.01 and abs(min(rat) - 1.017) < 0.005
         and abs(max(rat) - 1.107) < 0.005 and abs(min(efd) + 0.73) < 0.01 and abs(max(efd) + 0.10) < 0.01,
         f"retardation bound {tfmax:.4e} (CFG947 1.2114e-6); tethered Delta a/g_host [{min(rat):.4f}, {max(rat):.4f}] (1.017-1.107); "
         f"EFE [{min(efd):.3f}, {max(efd):.3f}] dex (-0.73..-0.10)")
RES["K2"] = dict(tfmax=tfmax, hover=[min(rat), max(rat)], efe=[min(efd), max(efd)])
P("  deriving growth determinant (sympy, CFG941 route) ...")
DET2, HOM2 = growth_det([("b", FBr, False), ("t", FCr, True)])
rss_guard("growth det")
n_s6 = n_from_det(DET2, {C2s: 1, Bs: 0}); n_full = n_from_det(DET2, {C2s: 1, Bs: 1}); n_dust = n_from_det(DET2, {C2s: 0, Bs: 0})
K3 = chk("K3_CFG941_growth_exponents", HOM2 and abs(n_s6 - 0.60954) < 1e-4 and abs(n_full - 0.69433) < 1e-4 and abs(n_dust - 1) < 1e-12,
         f"n(c2=1, no chi-bar) = {n_s6:.6f} (0.60954), n(c2=1, chi-bar) = {n_full:.6f} (0.69433), n(c2=0, dust) = {n_dust:.12f}")
RES["K3"] = dict(n_s6=n_s6, n_full=n_full, n_dust=n_dust)
# K4: CFG947 slip (cfg947.py sys_profile / slip_classA for N1, verbatim except names)
RHOM_SI = RHOM_H * HE ** 2 * MSUN / (1e6 * PC) ** 3


def sys_profile947(Mb, a0, kern="simple"):
    dom = domain947(Mb, a0); law = KERN[kern]; M = Mb * MSUN
    r_e, r_on, Mc = dom["r_e"], dom["r_on"], dom["Mc"] * MSUN
    A = Mc / (4 * math.pi * (r_on - r_e)) if r_on > r_e else 0.0
    q = q_edge(dom, kern); capf = 1 / q if q > 1 else 1.0; qeff = min(q, 1.0)
    Mph = lambda x: x * x * (float(law(G_SI * M / x ** 2, a0)) - G_SI * M / x ** 2) / G_SI
    Mcold = lambda x: 0.0 if x <= r_e else (4 * math.pi * A * (min(x, r_on) - r_e) + (0 if x <= r_on else (1 - FB) * RHOM_SI * 4 * math.pi / 3 * (x ** 3 - r_on ** 3)))
    return dict(dom=dom, M=M, r_e=r_e, r_on=r_on, Mc=Mc, A=A, q=q, capf=capf, qeff=qeff, Mph=Mph, Mcold=Mcold, law=law)


def slip947_N1(Mb, rk, a0, prof):
    spf = sys_profile947(Mb, a0); M = spf["M"]; rr = rk * KPC847
    law = spf["law"]; r_e, r_on = spf["r_e"], spf["r_on"]
    gl = lambda x: float(law(G_SI * M / x ** 2, a0))
    if prof == "PI":
        h = 1e-5 * rr; rho_ph = (spf["Mph"](rr + h) - spf["Mph"](rr - h)) / (2 * h) / (4 * math.pi * rr * rr)
        g_ = gl(rr); p = rho_ph * (g_ * rr) / 2
        return 4 * math.pi * G_SI * rr * p / (C_SI ** 2 * g_), 8 * math.pi * G_SI * rr ** 2 * p / (C_SI ** 2 * g_ * rr)
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


w947 = 0.0; wPS = 0.0
for foot in FOOTS:
    for name, Mb, rk in SYS847:
        for prof in ("PS", "PI"):
            sg_, s8_ = slip947_N1(Mb, rk, A0[foot], prof)
            w947 = max(w947, sg_, s8_)
            if prof == "PS":
                wPS = max(wPS, sg_, s8_)
K4 = chk("K4_CFG947_slip", abs(w947 / 1.6324059613188167e-05 - 1) < 0.01 and abs(wPS / 1.2954680886558027e-05 - 1) < 0.01,
         f"worst {w947:.4e} (CFG947 1.6324e-5, P-I dust pressure); S P-S stress {wPS:.4e} (1.2955e-5)")
RES["K4"] = dict(worst=w947, PS=wPS)
P("  K5 SPARC (CFG4 statistic, nu_mono):")
k5 = {}
for foot in FOOTS:
    k5[f"local|{foot}"] = sparc_rms(A0[foot], pred_local, f"local law {foot}")
rss_guard("K5")
ref5 = {"canonical": (0.1003, 0.61), "alt": (0.0991, 0.57)}
K5 = chk("K5_CFG4_SPARC_local", all(abs(k5[f"local|{f}"]["rms"] - ref5[f][0]) <= 1.5e-4 and abs(k5[f"local|{f}"]["U"] - ref5[f][1]) < 1e-9 for f in FOOTS),
         f"local {k5['local|canonical']['rms']:.5f} @ {k5['local|canonical']['U']:.2f} / {k5['local|alt']['rms']:.5f} @ {k5['local|alt']['U']:.2f}")
RES["K5"] = k5
# K6: CFG947 T-M relocation term for E8 (cfg947.py, method copied)
tsym = sp.symbols("t", real=True)
Me = sp.Function("M_e")(tsym); Xt = sp.Function("X")(tsym); epsS, McS = sp.symbols("epsilon M_c", positive=True)
mp_, mm_ = McS * (1 + epsS) / 2, McS * (1 - epsS) / 2
sw = [Me, -Me / McS * mp_, -Me / McS * mm_]; xw = [sp.Integer(0), Xt, -Xt]
R_E8 = sp.simplify(sum(sp.diff(s_, tsym, 2) * x_ + 2 * sp.diff(s_, tsym) * sp.diff(x_, tsym) for s_, x_ in zip(sw, xw)))
R_E8_target = -epsS * (sp.diff(Me, tsym, 2) * Xt + 2 * sp.diff(Me, tsym) * sp.diff(Xt, tsym))
tg, Me0, X0, Gs_, Md = sp.symbols("t_g M_e0 X_0 G_s M_dom", positive=True)
hist = Me0 * (1 - sp.cos(sp.pi * tsym / tg)) / 2
Rmax_E8 = sp.simplify(sp.Abs(R_E8_target.subs({Me: hist, Xt: X0}).doit().subs(tsym, 0)))
scale_ = {tg: sp.sqrt(X0 ** 3 / (Gs_ * Md)), Me0: Md / 2, McS: Md / 2}
rel_E8 = sp.simplify((Rmax_E8 / (Gs_ * Md ** 2 / X0 ** 2)).subs(scale_))
tm_rel = {e: float(rel_E8.subs(epsS, e)) for e in (0.01, 0.1, 0.3)}
K6 = chk("K6_CFG947_TM_E8", sp.simplify(R_E8 - R_E8_target) == 0 and all(abs(tm_rel[e] - math.pi ** 2 * e / 4) < 1e-6 for e in tm_rel)
         and abs(tm_rel[0.1] - 0.246740) < 1e-6,
         f"E8 two-blob R = {R_E8_target}; max|R|/(M_dom g_ref) = {rel_E8} -> {', '.join(f'{tm_rel[e]:.6f}' for e in tm_rel)} (0.024674 / 0.246740 / 0.740220)")
RES["K6"] = dict(rel=tm_rel)
# K7: CFG936 route (i) T and route (iii) T recomputed from the stored per-object values
rt_i = stats936(R936["routes"]["canonical"]["route_i"]["T"]["per_object"])
rt_iii = stats936(R936["routes"]["canonical"]["route_iii_EFE_contrast"]["T"]["per_object"])
K7 = chk("K7_CFG936_routes_reproduced", abs(rt_i["rbar"] - 0.054634) < 1e-6 and abs(rt_i["chi2"] - 1.1680) < 1e-4
         and abs(rt_iii["rbar"] + 0.381410) < 1e-6 and abs(rt_iii["chi2"] - 14.8547) < 1e-4,
         f"route (i) T rbar {rt_i['rbar']:+.6f}, chi2 {rt_i['chi2']:.4f} (+0.054634, 1.1680); route (iii) T rbar {rt_iii['rbar']:+.6f}, "
         f"chi2 {rt_iii['chi2']:.4f} (-0.381410, 14.8547)")
# K8: CFG947 T-E minimum and T-R threshold (cfg947.py loops)
temin = 1e9
for foot in FOOTS:
    for kz in KERN:
        for Mb in np.logspace(7, 15, 17):
            dom = domain947(float(Mb), A0[foot]); ron = dom["r_on"]; gnr = G_SI * Mb * MSUN / ron ** 2
            temin = min(temin, ron ** 2 * float(KERN[kz](gnr, A0[foot])) / G_SI / MSUN / dom["Mta"])
Mta_thr = M_ta(RMIN, DTA0); Mb_thr = fret_of(math.log10(Mta_thr)) * FB * Mta_thr / HE
K8 = chk("K8_CFG947_TE_TR", abs(temin / 1.847 - 1) < 1e-3 and abs(Mb_thr / 4.815e10 - 1) < 1e-3,
         f"min M_law(<r_ON)/M_ta = {temin:.4f} (1.847); RMIN threshold M_b = {Mb_thr:.4e} M_sun (4.815e10)")
RES["K8"] = dict(te_min=temin, Mb_thr=Mb_thr)
K_ALL = K1 and K2 and K3 and K4 and K5 and K6 and K7 and K8
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> main classes VOID'}")
RES["K_all"] = K_ALL
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)


# ================================================================================================ N-body toy (criteria section 4)
# code units G = a0 = 1, simple kernel, 3-D. Particles: baryons (kind 0, own = domain index) and unlabelled dust (kind 1);
# converted dust is removed (mass 0). Bodies (R3 SCT-M): spherical about X_q, M_sig(<r) = min(r^2 (g_law(gbar) - gbar), M_c),
# gbar = M_b,own(<r)/r^2 (Gaussian-smoothed monopole about X_q).  R4: P_q = M_c V_q, dP_q/dt = int sigma_q g; events inelastic.
TOY_EPS = 0.05; TOY_HS = 0.02
RGT = np.geomspace(1e-3, 400.0, 320)
SHR = np.sqrt(RGT[1:] * RGT[:-1])
GLX32, GLW32 = np.polynomial.legendre.leggauss(32)


def lawT(gn):
    return 0.5 * (gn + np.sqrt(gn * gn + 4.0 * gn))


def enc_frac(rr, d, h):
    """fraction of a 3-D Gaussian blob (width h) centred at distance d that lies within radius rr of the origin (exact)."""
    d = np.maximum(d, 1e-9); s2 = math.sqrt(2.0) * h
    A = 0.5 * (erf((rr - d) / s2) + erf((rr + d) / s2))
    B = h / (d * math.sqrt(2 * math.pi)) * (np.exp(-(rr - d) ** 2 / (2 * h * h)) - np.exp(-(rr + d) ** 2 / (2 * h * h)))
    return np.clip(A - B, 0.0, 1.0)                                       # clip round-off below 0 (cancellation at r << d)


def body_profile(Mc, d_own, m_own):
    if Mc <= 0 or len(m_own) == 0:
        z = np.zeros_like(RGT)
        return dict(Ms=z, g=z.copy(), Phi=z.copy(), Mtot=0.0, nonmono=False, deficit=float(Mc), re=0.0)
    Mb = (enc_frac(RGT[:, None], d_own[None, :], TOY_HS) * m_own[None, :]).sum(1)          # elementwise (no BLAS matmul)
    gn = Mb / RGT ** 2
    Mph = RGT ** 2 * (lawT(gn) - gn)
    nonmono = bool(np.any(np.diff(Mph) < -1e-12 * max(Mph.max(), 1e-300)))
    Mph = np.maximum.accumulate(Mph)
    Ms = np.minimum(Mph, Mc)
    g = Ms / np.maximum(RGT, TOY_EPS) ** 2
    integ = np.concatenate(([0.0], np.cumsum(0.5 * (g[1:] + g[:-1]) * np.diff(RGT))))
    Phi = -Ms[-1] / RGT[-1] - (integ[-1] - integ)
    j = np.searchsorted(Mph, Mc)
    return dict(Ms=Ms, g=g, Phi=Phi, Mtot=float(Ms[-1]), nonmono=nonmono, deficit=float(Mc - Ms[-1]),
                re=float(RGT[min(j, len(RGT) - 1)]))


def g_at(pr, dd):
    out = np.interp(dd, RGT, pr["g"])
    far = dd > RGT[-1]
    if far.any():
        out = np.where(far, pr["Mtot"] / np.maximum(dd, 1e-300) ** 2, out)
    return out


def phi_at(pr, dd):
    out = np.interp(dd, RGT, pr["Phi"])
    far = dd > RGT[-1]
    if far.any():
        out = np.where(far, -pr["Mtot"] / np.maximum(dd, 1e-300), out)
    return out


def shells(pr):
    dm = np.diff(pr["Ms"]); k = dm > 0
    return SHR[k], dm[k]


def bb_force_on_p(prp, Xp, prq, Xq):
    """force on body p from body q (shell quadrature of p in q's field); q gets minus this (pairwise)."""
    Dv = Xp - Xq; D = float(np.sqrt(np.sum(Dv * Dv)))
    if D < 1e-12:
        return np.zeros(3)
    s, dm = shells(prp)
    if len(s) == 0 or prq["Mtot"] <= 0:
        return np.zeros(3)
    rho = np.sqrt(np.maximum(D * D + s[:, None] ** 2 + 2 * D * s[:, None] * GLX32[None, :], 1e-30))
    ax = g_at(prq, rho) * (D + s[:, None] * GLX32[None, :]) / rho
    avg = 0.5 * (ax * GLW32[None, :]).sum(1)
    return -(Dv / D) * float(np.sum(dm * avg))


def bb_energy(prp, Xp, prq, Xq):
    Dv = Xp - Xq; D = float(np.sqrt(np.sum(Dv * Dv)))
    s, dm = shells(prp)
    if len(s) == 0 or prq["Mtot"] <= 0:
        return 0.0
    rho = np.sqrt(np.maximum(D * D + s[:, None] ** 2 + 2 * D * s[:, None] * GLX32[None, :], 1e-30))
    return float(np.sum(dm * 0.5 * (phi_at(prq, rho) * GLW32[None, :]).sum(1)))


def self_energy(pr):
    s, dm = shells(pr)
    return 0.5 * float(np.sum(dm * phi_at(pr, s))) if len(s) else 0.0


def sample_plummer(rng, n, M, a, center, vbulk, Mc_own):
    """Plummer positions (u <= 0.99); isotropic velocities with 1-D dispersion 0.5 v_c(r) of the law potential of the
    Plummer monopole (criteria section 4)."""
    uu = rng.uniform(0, 0.99, n); rr = a / np.sqrt(uu ** (-2.0 / 3.0) - 1.0)
    nv = rng.normal(size=(n, 3)); nv /= np.linalg.norm(nv, axis=1)[:, None]
    x = center[None, :] + rr[:, None] * nv
    Menc = M * rr ** 3 / (rr * rr + a * a) ** 1.5
    vc = np.sqrt(rr * lawT(Menc / rr ** 2))
    v = rng.normal(size=(n, 3)) * (0.5 * vc)[:, None]
    v -= v.mean(0)
    v += vbulk[None, :]
    return x, v, np.full(n, M / n)


def run_toy(which, dt, t_end, glued=False, seed=953, label=""):
    rng = np.random.default_rng(seed)
    X_ = []; V_ = []; M_ = []; KIND = []; OWN = []
    bodies = []
    conv_sched = []                                                      # (time, particle index) for the ramped birth
    if which == "E":
        xa, va, ma = sample_plummer(rng, 200, 1.0, 1.0, np.zeros(3), np.zeros(3), 20.0)
        X_ += list(xa); V_ += list(va); M_ += list(ma); KIND += [0] * 200; OWN += [0] * 200
        xb, vb, mb = sample_plummer(rng, 60, 0.02, 0.1, np.array([0.0, 12.0, 0.0]), np.array([0.6, 0.0, 0.0]), 0.4)
        i0b = len(X_); X_ += list(xb); V_ += list(vb); M_ += list(mb); KIND += [0] * 60; OWN += [1] * 60
        rc = 10.0 * rng.uniform(0, 1, 200) ** (1 / 3); nv = rng.normal(size=(200, 3)); nv /= np.linalg.norm(nv, axis=1)[:, None]
        ic0 = len(X_); X_ += list(rc[:, None] * nv); V_ += [np.zeros(3)] * 200; M_ += [0.1] * 200; KIND += [1] * 200; OWN += [-1] * 200
        perm = rng.permutation(200)
        conv_sched = [(0.5 + 5.0 * (k + 1) / 200.0, ic0 + int(perm[k])) for k in range(200)]
        xs_ = rng.uniform(30, 40, 60); ph = rng.uniform(0, 2 * math.pi, 60); rr_ = np.sqrt(rng.uniform(0, 1, 60))
        is0 = len(X_)
        X_ += [np.array([xs_[k], 3.0 + rr_[k] * math.cos(ph[k]), rr_[k] * math.sin(ph[k])]) for k in range(60)]
        V_ += [np.array([-0.8, 0.0, 0.0])] * 60; M_ += [2.0 / 60] * 60; KIND += [1] * 60; OWN += [-1] * 60
        stream = set(range(is0, is0 + 60))
        bodies = [dict(Mc=0.0, X=np.zeros(3), V=np.zeros(3), S=np.zeros(3), active=False),
                  dict(Mc=0.4, X=np.mean(xb, 0), V=np.array([0.6, 0.0, 0.0]), S=np.zeros(3), active=True)]
    else:                                                                # merger toy
        xa, va, ma = sample_plummer(rng, 150, 1.0, 1.0, np.array([-4.0, 0, 0]), np.zeros(3), 20.0)
        xc, vc, mc = sample_plummer(rng, 150, 1.0, 1.0, np.array([4.0, 0, 0]), np.zeros(3), 20.0)
        X_ += list(xa) + list(xc); V_ += list(va) + list(vc); M_ += list(ma) + list(mc)
        KIND += [0] * 300; OWN += [0] * 150 + [1] * 150; stream = set()
        bodies = [dict(Mc=20.0, X=np.mean(xa, 0), V=np.zeros(3), S=np.zeros(3), active=True),
                  dict(Mc=20.0, X=np.mean(xc, 0), V=np.zeros(3), S=np.zeros(3), active=True)]
    x = np.array(X_, float); v = np.array(V_, float); m = np.array(M_, float); kind = np.array(KIND); own = np.array(OWN)
    nb = len(bodies)
    prof = [None] * nb
    eint = {"conversion": 0.0, "reshape": 0.0, "merge": 0.0}
    log = dict(t=[], P=[], L=[], E=[], Emech=[], Pscale=[], Lscale=[], off=[], Eint=[])
    events = dict(conversions=0, merges=[], nonmono=0, deficit_max=0.0)

    def own_sel(q):
        return (kind == 0) & (own == q) & (m > 0)

    def centroid_b(q):
        s = own_sel(q); w = m[s]
        return (w[:, None] * x[s]).sum(0) / w.sum(), (w[:, None] * v[s]).sum(0) / w.sum()

    def make_prof(q):
        b = bodies[q]
        if glued and b["Mc"] > 0:
            b["X"], b["V"] = centroid_b(q)
        s = own_sel(q)
        pr = body_profile(b["Mc"] if b["active"] else 0.0, np.linalg.norm(x[s] - b["X"], axis=1), m[s])
        events["nonmono"] += int(pr["nonmono"]); events["deficit_max"] = max(events["deficit_max"], abs(pr["deficit"]))
        return pr

    def forces():
        alive = m > 0
        dx = x[:, None, :] - x[None, :, :]
        r2 = (dx * dx).sum(-1) + TOY_EPS ** 2
        inv3 = r2 ** -1.5; np.fill_diagonal(inv3, 0.0)
        acc = -(dx * (m[None, :, None] * inv3[:, :, None])).sum(1)
        Fb = np.zeros((nb, 3))
        for q in range(nb):
            if not bodies[q]["active"] or prof[q]["Mtot"] <= 0:
                continue
            dq = x - bodies[q]["X"]; dd = np.maximum(np.linalg.norm(dq, axis=1), 1e-12)
            aq = -(g_at(prof[q], dd) / dd)[:, None] * dq
            acc += aq
            Fb[q] += -(m[alive, None] * aq[alive]).sum(0)
        for p in range(nb):
            for q in range(p + 1, nb):
                if bodies[p]["active"] and bodies[q]["active"]:
                    F = bb_force_on_p(prof[p], bodies[p]["X"], prof[q], bodies[q]["X"])
                    Fb[p] += F; Fb[q] -= F
        return acc, Fb

    def W_shape():
        Wv = 0.0
        for q in range(nb):
            if not bodies[q]["active"]:
                continue
            al_ = m > 0
            Wv += float(np.sum(m[al_] * phi_at(prof[q], np.linalg.norm(x[al_] - bodies[q]["X"], axis=1))))
            Wv += self_energy(prof[q])
            for p in range(q + 1, nb):
                if bodies[p]["active"]:
                    Wv += bb_energy(prof[p], bodies[p]["X"], prof[q], bodies[q]["X"])
        return Wv

    def W_full():
        al_ = m > 0
        xa_ = x[al_]; ma_ = m[al_]
        dx = xa_[:, None, :] - xa_[None, :, :]
        r_ = np.sqrt((dx * dx).sum(-1) + TOY_EPS ** 2); np.fill_diagonal(r_, np.inf)
        return -0.5 * float(np.sum(ma_[:, None] * ma_[None, :] / r_)) + W_shape()

    def kin():
        return 0.5 * float(np.sum(m * (v * v).sum(1))) + sum(0.5 * b["Mc"] * float(np.sum(b["V"] * b["V"])) for b in bodies if b["active"])

    def momenta():
        P_ = (m[:, None] * v).sum(0); L_ = (m[:, None] * np.cross(x, v)).sum(0)
        Ps = float(np.sum(m * np.linalg.norm(v, axis=1))); Ls = float(np.sum(m * np.linalg.norm(np.cross(x, v), axis=1)))
        for b in bodies:
            if b["active"]:
                P_ = P_ + b["Mc"] * b["V"]; Ps += b["Mc"] * float(np.linalg.norm(b["V"]))
                if not glued:
                    L_ = L_ + b["Mc"] * np.cross(b["X"], b["V"]) + b["S"]
                    Ls += b["Mc"] * float(np.linalg.norm(np.cross(b["X"], b["V"]))) + float(np.linalg.norm(b["S"]))
                else:
                    L_ = L_ + b["Mc"] * np.cross(b["X"], b["V"])
        return P_, L_, Ps, Ls

    def convert(i, q):
        """R4 conversion event: dust particle i joins body q (inelastic)."""
        b = bodies[q]
        W0 = W_full(); K0 = kin()
        mi, xi, vi = m[i], x[i].copy(), v[i].copy()
        if not glued:
            if not b["active"]:
                b.update(Mc=mi, X=xi.copy(), V=vi.copy(), S=np.zeros(3), active=True)
            else:
                Mn = b["Mc"] + mi
                Xn = (b["Mc"] * b["X"] + mi * xi) / Mn; Vn = (b["Mc"] * b["V"] + mi * vi) / Mn
                b["S"] = b["S"] + b["Mc"] * np.cross(b["X"] - Xn, b["V"] - Vn) + mi * np.cross(xi - Xn, vi - Vn)
                b.update(Mc=Mn, X=Xn, V=Vn)
        else:
            b["Mc"] += mi; b["active"] = True
        m[i] = 0.0; v[i] = 0.0; kind[i] = -1
        prof[q] = make_prof(q)
        W1 = W_full(); K1_ = kin()
        if not glued:
            eint["conversion"] += (K0 - K1_) - (W1 - W0)
        events["conversions"] += 1

    def merge(p, q):
        """R7 merge event: body p into body q (inelastic); p's baryons become q's own."""
        bp, bq = bodies[p], bodies[q]
        W0 = W_full(); K0 = kin()
        Xb_p = centroid_b(p)[0]; Xb_q = centroid_b(q)[0]
        g_before = None
        Mn = bp["Mc"] + bq["Mc"]
        if not glued:
            Xn = (bp["Mc"] * bp["X"] + bq["Mc"] * bq["X"]) / Mn; Vn = (bp["Mc"] * bp["V"] + bq["Mc"] * bq["V"]) / Mn
            Sn = bp["S"] + bq["S"] + bp["Mc"] * np.cross(bp["X"] - Xn, bp["V"] - Vn) + bq["Mc"] * np.cross(bq["X"] - Xn, bq["V"] - Vn)
            # T-L field jump: monopole g at r = 5 about the new centroid, just before and just after
            Mb5 = float(np.sum(m[(kind == 0) & (m > 0) & (np.linalg.norm(x - Xn, axis=1) < 5.0)]))
            g_before = (Mb5 + float(np.interp(5.0, RGT, prof[p]["Ms"])) + float(np.interp(5.0, RGT, prof[q]["Ms"]))) / 25.0
            bq.update(Mc=Mn, X=Xn, V=Vn, S=Sn)
        else:
            bq["Mc"] = Mn
        own[(own == p)] = q
        bp.update(active=False, Mc=0.0)
        prof[p] = body_profile(0.0, np.zeros(0), np.zeros(0)); prof[q] = make_prof(q)
        W1 = W_full(); K1_ = kin()
        g_after = None
        if g_before is not None:
            Mb5 = float(np.sum(m[(kind == 0) & (m > 0) & (np.linalg.norm(x - bq["X"], axis=1) < 5.0)]))
            g_after = (Mb5 + float(np.interp(5.0, RGT, prof[q]["Ms"]))) / 25.0
        dE = (K0 - K1_) - (W1 - W0)
        if not glued:
            eint["merge"] += dE
        events["merges"].append(dict(p=p, q=q, sep_b=float(np.linalg.norm(Xb_p - Xb_q)), dEint=dE, Kloss=K0 - K1_, dW=W1 - W0,
                                     g5_before=g_before, g5_after=g_after))

    def bound_fraction(q):
        s = own_sel(q); idx = np.where(s)[0]
        if len(idx) == 0:
            return 0.0
        xs_ = x[idx]; ms_ = m[idx]
        dx = xs_[:, None, :] - xs_[None, :, :]
        r_ = np.sqrt((dx * dx).sum(-1) + TOY_EPS ** 2); np.fill_diagonal(r_, np.inf)
        phi = -(ms_[None, :] / r_).sum(1) + phi_at(prof[q], np.linalg.norm(xs_ - bodies[q]["X"], axis=1))
        Vq = bodies[q]["V"] if not glued else centroid_b(q)[1]
        e = 0.5 * ((v[idx] - Vq) ** 2).sum(1) + phi
        return float(np.mean(e < 0))

    for q in range(nb):
        prof[q] = make_prof(q)
    acc, Fb = forces()
    nsteps = int(round(t_end / dt)); sched_k = 0; t = 0.0
    E0 = None
    for step in range(nsteps + 1):
        if step % 20 == 0:
            P_, L_, Ps, Ls = momenta(); Wm = W_full(); Km = kin(); Ei = sum(eint.values())
            if E0 is None:
                E0 = Km + Wm
            log["t"].append(t); log["P"].append(P_.tolist()); log["L"].append(L_.tolist())
            log["E"].append(Km + Wm + Ei); log["Emech"].append(Km + Wm); log["Pscale"].append(Ps); log["Lscale"].append(Ls)
            log["Eint"].append(dict(eint))
            offs = []
            for q in range(nb):
                if bodies[q]["active"] and own_sel(q).any():
                    offs.append(float(np.linalg.norm(centroid_b(q)[0] - bodies[q]["X"])))
                else:
                    offs.append(float("nan"))
            log["off"].append(offs)
        if step == nsteps:
            break
        if step % 1000 == 0:
            rss_guard(f"toy {label} step {step}")
        # KDK
        v += 0.5 * dt * acc
        for q in range(nb):
            if bodies[q]["active"] and bodies[q]["Mc"] > 0 and not glued:
                bodies[q]["V"] = bodies[q]["V"] + 0.5 * dt * Fb[q] / bodies[q]["Mc"]
        x += dt * v
        for q in range(nb):
            if bodies[q]["active"] and not glued:
                bodies[q]["X"] = bodies[q]["X"] + dt * bodies[q]["V"]
        t += dt
        # reshape (R6): shape follows the own baryons; the change of W is booked into E_int
        Wa = W_shape()
        for q in range(nb):
            prof[q] = make_prof(q)
        Wb = W_shape()
        if not glued:
            eint["reshape"] -= (Wb - Wa)
        # events
        while sched_k < len(conv_sched) and conv_sched[sched_k][0] <= t + 1e-12:
            convert(conv_sched[sched_k][1], 0); sched_k += 1
        if which == "E" and bodies[0]["active"]:
            for i in list(stream):
                if m[i] > 0 and np.linalg.norm(x[i] - bodies[0]["X"]) < 25.0:
                    convert(i, 0); stream.discard(i)
            if bodies[1]["active"] and step % 200 == 0:
                bf = bound_fraction(1)
                sep = np.linalg.norm(centroid_b(1)[0] - centroid_b(0)[0])
                if bf < 0.5 or sep <= 1.305:
                    merge(1, 0)
        if which == "M" and bodies[1]["active"]:
            if np.linalg.norm(centroid_b(1)[0] - centroid_b(0)[0]) <= 1.305:
                merge(1, 0)
        acc, Fb = forces()
        v += 0.5 * dt * acc
        for q in range(nb):
            if bodies[q]["active"] and bodies[q]["Mc"] > 0 and not glued:
                bodies[q]["V"] = bodies[q]["V"] + 0.5 * dt * Fb[q] / bodies[q]["Mc"]
        if glued:
            for q in range(nb):
                if bodies[q]["active"]:
                    bodies[q]["X"], bodies[q]["V"] = centroid_b(q)
    Pa = np.array(log["P"]); La = np.array(log["L"]); Ea = np.array(log["E"]); Em = np.array(log["Emech"])
    Psc = max(log["Pscale"]); Lsc = max(log["Lscale"])
    res = dict(which=which, dt=dt, t_end=t_end, glued=glued,
               dP=float(np.max(np.linalg.norm(Pa - Pa[0], axis=1)) / Psc), dL=float(np.max(np.linalg.norm(La - La[0], axis=1)) / Lsc),
               dE=float(np.max(np.abs(Ea - Ea[0])) / abs(E0)), dEmech=float(np.max(np.abs(Em - Em[0])) / abs(E0)),
               E0=float(E0), Pscale=Psc, Lscale=Lsc, eint_final=dict(eint),
               eint_over_E0={k: v_ / abs(E0) for k, v_ in eint.items()}, events=events,
               off_max=[float(np.nanmax([o[q] for o in log["off"]])) for q in range(nb)],
               off_final=[float(log["off"][-1][q]) for q in range(nb)],
               P0=Pa[0].tolist(), Pend=Pa[-1].tolist())
    return res


def toy_line(tr, name):
    P(f"     {name}: dP/P_scale {tr['dP']:.2e}, dL/L_scale {tr['dL']:.2e}, |dE_tot|/|E0| {tr['dE']:.2e}, |dE_mech|/|E0| "
      f"{tr['dEmech']:.2e} (E0 {tr['E0']:.3f}); E_int/|E0|: " + ", ".join(f"{k} {v:+.4f}" for k, v in tr["eint_over_E0"].items())
      + f"; conversions {tr['events']['conversions']}, merges {len(tr['events']['merges'])}, non-monotone M_ph {tr['events']['nonmono']}, "
      f"max body-mass deficit {tr['events']['deficit_max']:.1e}; baryon-body offset max {', '.join(f'{o:.3f}' for o in tr['off_max'])}, "
      f"final {', '.join(f'{o:.3f}' for o in tr['off_final'])}")


# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    teeth = {}
    m1 = [efe_global_dex(Mb, apc, rk, A0[f], kz) for f in FOOTS for _, Mb, apc in HOSTS882 for rk in RHOST for kz in KERN]
    teeth["Mu1"] = max(abs(v_) for v_ in m1) >= 0.05
    chk("Mu1_global_source_EFE_returns", teeth["Mu1"], f"body from the global baryon field: EFE {min(m1):.3f}..{max(m1):.3f} dex (CFG947 T-X)")
    B_, C1_, C2_, k_ = sp.symbols("B C_1 C_2 k", positive=True)
    Lmode = Kg / (4 * k_ ** 2) * ((B_ + C1_ + C2_) ** 2 - C2s * (C1_ + C2_) ** 2)
    mut_coef = sp.simplify(sp.diff(Lmode, C1_, C2_))
    m_teth = sp.simplify(mut_coef.subs(C2s, 1)); m_src = sp.simplify(mut_coef.subs(C2s, 0))
    teeth["Mu2"] = min(rat) >= 0.5 and abs(n_full - 1) >= 1e-3 and m_teth == 0 and m_src != 0
    chk("Mu2_tether_brings_back_DT", teeth["Mu2"], f"tether: Delta a/g_host {min(rat):.4f}..{max(rat):.4f}, n = {n_full:.5f}, linear C1C2 "
        f"coefficient {m_teth} (source: {m_src})")
    P("  running the toy (run E, dt 2e-3) and its glued-body mutation ...")
    tE = run_toy("E", 2e-3, 40.0, glued=False, label="E")
    toy_line(tE, "run E (SCT)")
    tG = run_toy("E", 2e-3, 40.0, glued=True, label="E glued")
    toy_line(tG, "run E (Mu3 glued body)")
    rss_guard("Mu3")
    teeth["Mu3"] = tG["dP"] >= 1e-3 and tm_rel[0.1] > 0
    chk("Mu3_glued_body_breaks_momentum", teeth["Mu3"], f"glued body: toy dP/P_scale {tG['dP']:.3e} (SCT {tE['dP']:.1e}); two-blob "
        f"prescribed draw R/(M g) {tm_rel[0.1]:.4f} at eps 0.1 (CFG947 E8)")
    m4 = {}
    for foot in FOOTS:
        for kz in KERN:
            glaw = KERN[kz](GN_N, A0[foot]); Mph = R_N ** 2 * (glaw - GN_N) / G_SI
            m4[f"{foot}|{kz}"] = float(np.max(np.abs(G_SI * (MBR_N + Mph + Mph) / R_N ** 2 / glaw - 1)))
    teeth["Mu4"] = min(m4.values()) >= 1e-3
    chk("Mu4_no_cancellation_breaks_law", teeth["Mu4"], "labelled dust (P-I) gravitating on top of the body: NGC 3198 max dev "
        + ", ".join(f"{k} {v_:.3f}" for k, v_ in m4.items()))
    teeth["Mu5"] = tE["dEmech"] >= 1e-3 and tE["dEmech"] >= 10 * tE["dE"]
    chk("Mu5_no_Eint_breaks_energy", teeth["Mu5"], f"E_int not booked: |dE_mech|/|E0| {tE['dEmech']:.3e} vs integrator error {tE['dE']:.2e}")
    t_, t0_, rr_, c_ = sp.symbols("t t_0 r c", positive=True)
    psi_ret = sp.Heaviside(t_ - t0_ - rr_ / c_) / (4 * sp.pi * rr_)
    psi_adv = sp.Heaviside(t_ - t0_ + rr_ / c_) / (4 * sp.pi * rr_)
    tpre = t0_ - rr_ / (2 * c_)
    pre_ret = sp.simplify(psi_ret.subs(t_, tpre)); pre_sym = sp.simplify(((psi_ret + psi_adv) / 2).subs(t_, tpre))
    frac = sp.simplify(pre_sym * 4 * sp.pi * rr_)
    teeth["Mu6"] = (pre_ret == 0) and float(frac) > 0
    chk("Mu6_time_symmetric_kernel_acausal", teeth["Mu6"], f"before switch-on: retarded {pre_ret}, time-symmetric {frac} of the static value")
    m7 = {}
    for foot in FOOTS:
        dom = domain_sct(MB_N, A0[foot]); m7[foot] = (Mph_pt(dom["r_on"], MB_N * MSUN, A0[foot], "simple") / MSUN - dom["Mc"]) / MB_N
    teeth["Mu7"] = all(v_ > 1e-6 for v_ in m7.values())
    chk("Mu7_no_edge_creates_S_mass", teeth["Mu7"], f"untruncated phantom: S mass created inside r_ON = {m7['canonical']:.2f} / "
        f"{m7['alt']:.2f} M_b (continuity has no solution)")
    RES["MUTATE"] = dict(teeth=teeth, Mu1=[min(m1), max(m1)], Mu4=m4, Mu7=m7, toyE=tE, toyG=tG)
    allb = all(teeth.values())
    P(f"  MUTATE: {'ALL TEETH BITE' if allb else 'A TOOTH DID NOT BITE'}")
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
    sys.exit(1 if allb else 2)

# ================================================================================================ MAIN: structural statements
P("\n==================== STRUCTURAL STATEMENTS ====================")
ST = {}
# ---- S-P / S-L: the conversion-event algebra (R4)
Mcs, ms = sp.symbols("M_c m", positive=True)
Xv = sp.Matrix(sp.symbols("X1:4", real=True)); xv = sp.Matrix(sp.symbols("x1:4", real=True))
Vv = sp.Matrix(sp.symbols("V1:4", real=True)); vv = sp.Matrix(sp.symbols("v1:4", real=True))
Sv = sp.Matrix(sp.symbols("S1:4", real=True)); Dl = sp.Matrix(sp.symbols("Dl1:4", real=True)); Pl = sp.Matrix(sp.symbols("Pl1:4", real=True))
Mn_ = Mcs + ms; Xn_ = (Mcs * Xv + ms * xv) / Mn_; Vn_ = (Mcs * Vv + ms * vv) / Mn_
Sn_ = Sv + Mcs * (Xv - Xn_).cross(Vv - Vn_) + ms * (xv - Xn_).cross(vv - Vn_)
dD = sp.simplify((Mn_ * Xn_ - (Dl + ms * xv)) - (Mcs * Xv - Dl))                 # S dipole: body minus labelled dust
dDd = sp.simplify((Mn_ * Vn_ - (Pl + ms * vv)) - (Mcs * Vv - Pl))                # S momentum
dPtot = sp.simplify((Mn_ * Vn_) - (Mcs * Vv + ms * vv))                          # books: the element leaves the matter sum
dLtot = sp.simplify((Mn_ * Xn_.cross(Vn_) + Sn_) - (Mcs * Xv.cross(Vv) + Sv + ms * xv.cross(vv)))
ev_ok = all(sp.simplify(e) == 0 for e in list(dD) + list(dDd) + list(dPtot) + list(dLtot))
# between events: S's dipole obeys the momentum condition (two-blob toy of CFG947 under R4)
mpf = sp.Function("m_p")(tsym); mmf = sp.Function("m_m")(tsym); Xb_ = sp.Function("X")(tsym); Fb_ = sp.Function("F")(tsym)
Yf = sp.Function("Y")(tsym); Pif = sp.Function("Pi")(tsym)
mdot = sp.diff(mpf, tsym) - sp.diff(mmf, tsym)
Ds_ = Yf - (mpf - mmf) * Xb_
Dsdd = sp.diff(Ds_, tsym, 2)
Ydd = sp.diff(Pif, tsym) + sp.diff(mdot * Xb_, tsym)
Dsdd = Dsdd.subs(sp.diff(Yf, tsym, 2), Ydd).subs(sp.diff(Pif, tsym), Fb_ + mdot * sp.diff(Xb_, tsym))
cond = Fb_ - (mpf - mmf) * sp.diff(Xb_, tsym, 2)                                  # int rho_s g = F_body - sum_lab m g
R_SCT = sp.simplify(sp.expand(Dsdd - cond))
R_SCT_eps = sp.simplify(R_SCT.subs({mpf: Me * (1 + epsS) / 2, mmf: Me * (1 - epsS) / 2}).doit())
# body centroid in the two-blob toy (Y(0) = 0, Pi(0) = 0, static blobs): X_sigma = Y/M = eps X  (the price: an offset from the core)
off_sym = sp.simplify(((Me * (1 + epsS) / 2 - Me * (1 - epsS) / 2) * X0) / Me)
# self-force of S vanishes (Poisson symmetry): random signed point weights
rng0 = np.random.default_rng(9530)
xs0 = rng0.normal(size=(40, 3)); ss0 = rng0.normal(size=40)
dx0 = xs0[None, :, :] - xs0[:, None, :]; r30 = np.linalg.norm(dx0, axis=2) ** 3; np.fill_diagonal(r30, np.inf)
selfF = np.abs((ss0[:, None, None] * ss0[None, :, None] * dx0 / r30[:, :, None]).sum((0, 1))).max()
ST["S-P"] = chk("S-P_momentum_event_algebra", ev_ok and selfF < 1e-12,
                f"conversion event: Delta D_s = {list(dD)}, Delta dD_s/dt = {list(dDd)}, Delta P_tot = {list(dPtot)}, Delta L_tot = "
                f"{list(dLtot)}; S self-force on 40 signed weights {selfF:.1e}")
ST["S-TM"] = chk("S-TM_relocation_term_zero", R_SCT == 0 and R_SCT_eps == 0 and sp.simplify(R_E8_target) != 0,
                 f"two-blob toy under R4: R = D_s'' - int rho_s g = {R_SCT} (any m_p, m_m, X, F); with CFG947's draw proportions "
                 f"{R_SCT_eps}; E8 (prescribed draw): {R_E8_target}. Price: body centroid at the converted dust's centroid, "
                 f"offset {off_sym} from the core (static blobs)")
# S-L: a spherical body feels no torque about its centre (reciprocity with a point mass)
xp = sp.Matrix(sp.symbols("p1:4", real=True)); rp = sp.sqrt(xp.dot(xp)); gfun = sp.Function("g")
F_on_point = -ms * gfun(rp) * xp / rp
tq = sp.simplify(-xp.cross(F_on_point))
ST["S-L"] = chk("S-L_no_torque_on_spherical_body", all(e == 0 for e in tq) and ev_ok,
                f"torque on a spherical body about its centre from a point mass = -x_p x F_point = {list(tq)}; spin S absorbs the "
                "converted element's angular momentum (Delta L_tot = 0 above)")
# S-Z: body mass = labelled mass at the supply root
sz = []
for foot in FOOTS:
    for kz in KERN:
        dom = domain_sct(MB_N, A0[foot], kz)
        sz.append(abs(Mph_pt(dom["r_e"], MB_N * MSUN, A0[foot], kz) / (dom["Mc"] * MSUN) - 1))
ST["S-Z"] = chk("S-Z_zero_sum_per_domain", max(sz) < 1e-12, f"|M_body(r_e)/M_c - 1| <= {max(sz):.1e} (NGC 3198, both footings and kernels): "
                "int rho_s = M_c - M_c,lab = 0")
# S-+: positivity
ysym = sp.symbols("y", positive=True)
gl_s = (ysym + sp.sqrt(ysym ** 2 + 4 * ysym)) / 2
dgdy = sp.simplify(sp.diff(gl_s, ysym))
key = sp.simplify((ysym + 2) ** 2 - (ysym ** 2 + 4 * ysym))
nu_s = sp.simplify(gl_s / ysym); dnu = sp.simplify(sp.diff(nu_s, ysym))
dnu_neg = all(float(dnu.subs(ysym, yv)) < 0 for yv in (1e-8, 1e-3, 1.0, 1e3, 1e8))
yg = np.logspace(-12, 6, 4000); hm = yg * C4.nu_mono(yg)
mono_ok = bool(np.all(np.diff(hm) / np.diff(yg) >= 1 - 1e-9)) and bool(np.all(np.diff(C4.nu_mono(yg)) < 0))
mbr_mono = bool(np.all(np.diff(MBR_N) > 0))
mph_n = {}
for foot in FOOTS:
    for kz in KERN:
        glaw = KERN[kz](GN_N, A0[foot]); mph_n[f"{foot}|{kz}"] = bool(np.all(np.diff(R_N ** 2 * (glaw - GN_N)) > 0))
ST["S-+"] = chk("S-+_body_positive", key == 4 and dnu_neg and mono_ok and all(mph_n.values()),
                f"simple kernel: dg/dy = {dgdy}, (y+2)^2 - (y^2+4y) = {key} > 0 => dg/dy > 1; dnu/dy = {dnu} < 0; nu_mono: slope of y nu >= 1 "
                f"and nu decreasing on 1e-12..1e6: {mono_ok}. NGC 3198: m_N increasing {mbr_mono}; M_ph increasing at the data radii {mph_n}")
# S-E: edge forced inside turnaround
se = []
for foot in FOOTS:
    for kz in KERN:
        for Mb in np.logspace(3, 15, 13):
            dom = domain_sct(float(Mb), A0[foot], kz); se.append((dom["r_e"] / dom["r_on"], float(Mb), foot, kz))
ST["S-E"] = chk("S-E_edge_inside_turnaround", max(x_[0] for x_ in se) < 1, f"r_e/r_ON in [{min(x_[0] for x_ in se):.3f}, "
                f"{max(x_[0] for x_ in se):.3f}] for M_b 1e3-1e15, both footings and kernels")
RES["S-E"] = se
# S-C: retarded support
t1, t01, r1, c1 = sp.symbols("t t_0 r c", positive=True)
resp = sp.Heaviside(t1 - t01 - r1 / c1) / (4 * sp.pi * r1)
ST["S-C"] = chk("S-C_retarded_support", sp.simplify(resp.subs(t1, t01 + r1 / (2 * c1))) == 0,
                "response to a source switched on at t0 vanishes at t0 + r/(2c) < t0 + r/c; propagation speed of S updates c (R8)")
# S-En: energy released by building a body (dust uniform within r_ON at turnaround -> body inside r_e; baryons fixed point mass)
sen = {}
for foot in FOOTS:
    a0 = A0[foot]; rows = []
    for Mb in np.logspace(3, 15, 13):
        dom = domain_sct(float(Mb), a0, "simple"); M = Mb * MSUN; Mc = dom["Mc"] * MSUN; ron = dom["r_on"]; re = dom["r_e"]
        Wi = -0.6 * G_SI * Mc ** 2 / ron - 1.5 * G_SI * M * Mc / ron
        rg = np.geomspace(1e-6 * dom["rM"], re, 6000)
        Ms = np.array([Mph_pt(x_, M, a0, "simple") for x_ in rg]); Ms = np.minimum(Ms, Mc)
        dM = np.diff(Ms); rm = np.sqrt(rg[1:] * rg[:-1]); Mm = 0.5 * (Ms[1:] + Ms[:-1])
        Wf = -G_SI * float(np.sum(Mm * dM / rm)) - G_SI * M * float(np.sum(dM / rm))
        Erel = Wi - Wf
        vf2 = math.sqrt(G_SI * M * a0)
        rows.append(dict(Mb=float(Mb), N=dom["N"], re_over_ron=re / ron, Erel_over_Wf=Erel / abs(Wf), Erel_over_Mcc2=Erel / (Mc * C_SI ** 2),
                         Erel_over_Mcvf2=Erel / (Mc * vf2)))
    sen[foot] = rows
erel_pos = all(rw["Erel_over_Wf"] > 0 for v_ in sen.values() for rw in v_)
ST["S-En"] = chk("S-En_formation_energy", all(np.isfinite(rw["Erel_over_Wf"]) for v_ in sen.values() for rw in v_),
                 "E_rel/|W_f| (canonical) " + ", ".join(f"{rw['Erel_over_Wf']:.3f}" for rw in sen["canonical"][::3])
                 + f" at M_b 1e3,1e6,1e9,1e12,1e15; E_rel/(M_c c^2) {min(rw['Erel_over_Mcc2'] for v_ in sen.values() for rw in v_):.2e}.."
                 f"{max(rw['Erel_over_Mcc2'] for v_ in sen.values() for rw in v_):.2e}; released (> 0) for every M_b: {erel_pos}")
RES["S-En"] = sen
rss_guard("structural")

# ================================================================================================ MAIN: tests (a)-(h)
P("\n==================== TESTS (a)-(h) ====================")
GR = {"SCT-M": {}, "SCT-Q": {}}
# ---- (a)
P("  (a) static law, one domain (NGC 3198, spherical-equivalent convention; edge = the kernel's own supply root)")
A = {}; a1 = True; a2 = True
for foot in FOOTS:
    a0 = A0[foot]
    for kz in KERN:
        law = KERN[kz]; dom = domain_sct(MB_N, a0, kz)
        glaw = law(GN_N, a0); Mph = R_N ** 2 * (glaw - GN_N) / G_SI
        inside = bool(np.all(R_N < dom["r_e"])) and bool(np.all(Mph < dom["Mc"] * MSUN))
        devs = {}
        for prof, fdust in (("PS", 0.0), ("PI", 1.0), ("PX", 2.0)):
            Mdust = fdust * Mph                                                   # labelled dust: inert (R2), active weight 0
            Mg = MBR_N + np.minimum(Mph, dom["Mc"] * MSUN) + 0.0 * Mdust
            devs[prof] = float(np.max(np.abs(G_SI * Mg / R_N ** 2 / glaw - 1)))
        M = MB_N * MSUN; deep = {}
        for y in (1e-2, 1e-3):
            rr = math.sqrt(G_SI * M / (y * a0)); gn = y * a0; gl = float(law(gn, a0)); ins = rr < dom["r_e"]
            g = gn + G_SI * min(Mph_pt(rr, M, a0, kz), dom["Mc"] * MSUN) / rr ** 2
            deep[f"y={y:g}"] = dict(r_kpc=rr / KPC, inside=bool(ins), dev=abs(g / gl - 1), V4=(g * rr) ** 2 / (G_SI * M * a0),
                                    V4_law=(gl * rr) ** 2 / (G_SI * M * a0))
            a2 = a2 and ins and abs(g / gl - 1) <= 1e-6
        ye = dom["yE"]; gle = float(law(ye * a0, a0)); V4e = gle ** 2 / (ye * a0 * a0)
        gl14 = float(law(1e-14 * a0, a0)); V414 = gl14 ** 2 / (1e-14 * a0 * a0)
        rb = 2 * dom["r_e"]; gb_ = G_SI * (M + dom["Mc"] * MSUN) / rb ** 2; glb = float(law(G_SI * M / rb ** 2, a0))
        A[f"{foot}|{kz}"] = dict(devs=devs, inside=inside, r_e_kpc=dom["r_e"] / KPC, N=dom["N"], deep=deep, y_e=ye, V4_at_ye=V4e,
                                 V4_y1e14=V414, kepler_2re_over_law=gb_ / glb)
        a1 = a1 and inside and max(devs["PS"], devs["PI"], devs["PX"]) <= 1e-6
        P(f"   {foot:9s} {kz:6s}: max dev P-S/P-I/P-X {devs['PS']:.2e}/{devs['PI']:.2e}/{devs['PX']:.2e}; r_e {dom['r_e'] / KPC:.1f} kpc "
          f"(N {dom['N']:.2f}); deep y=1e-2/1e-3 dev {deep['y=0.01']['dev']:.1e}/{deep['y=0.001']['dev']:.1e}, V^4/GMa0 "
          f"{deep['y=0.01']['V4']:.4f}/{deep['y=0.001']['V4']:.4f}; y_e {ye:.2e} (V^4/GMa0 there {V4e:.4f}); law asymptote at y=1e-14 "
          f"{V414:.8f}; beyond the edge at 2 r_e: g/g_law {gb_ / glb:.3f}")
asym_ok = all(abs(A[k]["V4_y1e14"] - 1) < 1e-6 for k in A)
# a3: disc geometry (SCT-M monopole vs pointwise law), thin exponential disc, simple kernel, code units G = a0 = R_d = 1


def disc_report(ylev):
    Md = ylev; S0 = Md / (2 * math.pi); out = []
    for Rr in np.linspace(0.5, 10.0, 96):
        yy = Rr / 2.0
        V2 = 4 * math.pi * S0 * yy * yy * (ssp.i0(yy) * ssp.k0(yy) - ssp.i1(yy) * ssp.k1(yy))   # (first run: k1 was shadowed by the K1 dict)
        gb = V2 / Rr; Menc = Md * (1 - (1 + Rr) * math.exp(-Rr)); gs = Menc / Rr ** 2
        out.append(math.log10((gb + float(lawT(gs)) - gs) / float(lawT(gb))))
    return float(max(abs(x_) for x_ in out)), float(out[int(np.argmax(np.abs(out)))])


a3d = {f"y(Rd)={yl:g}": disc_report(yl) for yl in (10.0, 1.0, 0.1)}
P("   a3 (reported) thin exponential disc: max |SCT-M monopole - pointwise law| = " + ", ".join(f"{k}: {v_[0]:.4f} dex" for k, v_ in a3d.items()))
Nlist = [domain_sct(float(Mb), A0["canonical"])["N"] for Mb in np.logspace(7, 13, 7)]
P(f"   a3 (reported) supply N = M_c/M_b at M_b 1e7..1e13: {', '.join(f'{n_:.1f}' for n_ in Nlist)} (CFG803 N_min 3 / 4 primary; 16 / 24 all radii)")
ga = "PASS" if (a1 and a2 and asym_ok) else "FAIL"
for v_ in GR: GR[v_]["a"] = ga
P(f"   (a): a1 {'PASS' if a1 else 'FAIL'}, a2 {'PASS' if a2 else 'FAIL'} (asymptote {'ok' if asym_ok else 'FAIL'}) -> {ga} "
  "[by construction inside the edge for one domain: the test checks the edge, the kernel root and the dust's inertness]")
RES["a"] = dict(A=A, a3_disc=a3d, N_grid=Nlist)
# ---- (b) FRW + growth (cfg947.py FRW block, verbatim method)
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
th_ = sp.symbols("theta", positive=True)
dens = sp.Rational(9, 2) * (th_ - sp.sin(th_)) ** 2 / (1 - sp.cos(th_)) ** 3
dta_eds = sp.simplify(dens.subs(th_, sp.pi))
thg = np.linspace(1e-3, math.pi - 1e-6, 4000); dfn = sp.lambdify(th_, dens, "numpy")
mono_th = bool(np.all(np.diff(dfn(thg)) > 0))
# body gas at linear order (bodies = free-falling centres of mass): delta'' + 2H delta' = 4 pi G rho delta, EdS
alp = sp.symbols("alpha_b")
eqb = sp.expand(alp * (alp - 1) + sp.Rational(4, 3) * alp - sp.Rational(2, 3))
roots_b = sp.solve(eqb, alp); n_body = float(max(roots_b) / sp.Rational(2, 3))
b_ok = offd and iso and p_d == 0 and sp.simplify(rho_d - mm_ / af ** 3) == 0 and dmin > 1 and abs(n_dust - 1) < 1e-12 and mono_th \
    and abs(float(dta_eds) - 9 * math.pi ** 2 / 16) < 1e-12 and abs(n_body - 1) < 1e-12
for v_ in GR: GR[v_]["b"] = "PASS" if b_ok else "FAIL"
chk("b_FRW_growth", b_ok, f"dust rho = {rho_d}, p = {p_d}, isotropic; S = 0 on FRW (Delta_ta(z) >= {dmin:.3f} > 1: no domain); linear dust "
    f"n = {n_dust:.12f}; top-hat density monotone to {float(dta_eds):.4f} = 9 pi^2/16 (no domain before turnaround); body gas linear "
    f"exponent roots {roots_b} -> n = {n_body:.12f}")
del Tdn, Ld, sqrtg
# ---- (c) no hover / no EFE


def sat_c(Mb_sun, a_pc, rkpc, a0):
    M = Mb_sun * MSUN847; a = a_pc * PC; N = domain_sct(Mb_sun, a0)["N"]; Mc = N * M
    Mh = HOST938 * MSUN847; D = rkpc * KPC847
    Mbr = lambda s: M * s ** 3 / (s * s + a * a) ** 1.5
    Mph = lambda s: s * s * (float(law_simple(G_SI * Mbr(s) / s ** 2, a0)) - G_SI * Mbr(s) / s ** 2) / G_SI
    re = math.exp(brentq(lambda ls: Mph(math.exp(ls)) - Mc, math.log(1e-3 * a), math.log(1e7 * a), xtol=1e-14, rtol=1e-14))
    sg = np.geomspace(1e-4 * a, re, 1500); Msg = np.array([Mph(s) for s in sg]); dMs = np.diff(Msg); sm = np.sqrt(sg[1:] * sg[:-1])
    bg = np.geomspace(1e-4 * a, 1e3 * a, 1500); Mbg = np.array([Mbr(s) for s in bg]); dMb = np.diff(Mbg); bm = np.sqrt(bg[1:] * bg[:-1])
    gh = lambda rho: law_simple(G_SI * Mh / rho ** 2, a0)

    def mean_g(s):
        rho = np.sqrt(D * D + s[:, None] ** 2 + 2 * D * s[:, None] * GL_X[None, :])
        return 0.5 * (gh(rho) * (D + s[:, None] * GL_X[None, :]) / rho * GL_W[None, :]).sum(1)
    gs_mean = float(np.sum(dMs * mean_g(sm)) / np.sum(dMs)); gb_mean = float(np.sum(dMb * mean_g(bm)) / np.sum(dMb))
    ghD = float(gh(D)); Da = abs(gs_mean - gb_mean)
    rho_b = lambda s: 3 * M * a * a / (4 * math.pi * (s * s + a * a) ** 2.5)
    Kbs = (4 * math.pi * G_SI / 3) * float(np.sum(np.array([rho_b(s) for s in sm]) * dMs))
    deq = Da / (Kbs * (1 / M + 1 / Mc))
    gsig = lambda s: G_SI * Mph(s) / s ** 2
    hh = 1e-4 * a; dgs = abs(gsig(a + hh) - gsig(a - hh)) / (2 * hh)
    dg = max(dgs * deq, gsig(a) * deq / a)
    gsat = float(law_simple(G_SI * Mbr(a) / a ** 2, a0))
    tid = abs(float(gh(D - a)) - ghD)
    return dict(ratio=Da / ghD, deq_over_a=deq / a, efe_dex=math.log10(1 + dg / gsat), tidal_dex=math.log10(1 + tid / gsat),
                r_e_kpc=re / KPC, rJ_kpc=D * ((M + Mc) / (3 * D * D * ghD / G_SI)) ** (1 / 3) / KPC, N=N)


Cc = {}
for foot in FOOTS:
    for nm, Mb, apc in HOSTS882:
        for rk in RHOST:
            Cc[f"{foot}|{nm}|{rk:.0f}"] = sat_c(Mb, apc, rk, A0[foot])
c1v = {k: v_["ratio"] + TF[k] for k, v_ in Cc.items()}
c1_ok = all(c1v[k] <= EPS_B[k.split("|")[0]] for k in c1v)
c2_ok = all(abs(v_["efe_dex"]) <= DELTA_C for v_ in Cc.values())
for k, v_ in Cc.items():
    if k.startswith("canonical"):
        P(f"   {k:22s}: Delta a/g_host {v_['ratio']:.2e} (+ retardation {TF[k]:.1e}); delta_eq/a {v_['deq_over_a']:.2e}; EFE {v_['efe_dex']:.2e} dex; "
          f"host tidal term {v_['tidal_dex']:.3f} dex (reported); body edge {v_['r_e_kpc']:.2f} kpc vs Jacobi {v_['rJ_kpc']:.2f} kpc")
gc = "PASS" if (c1_ok and c2_ok) else "FAIL"
for v_ in GR: GR[v_]["c"] = gc
chk("c_no_hover_no_EFE", c1_ok and c2_ok, f"max Delta a/g_host {max(c1v.values()):.2e} (eps_B 0.344 / 0.317); max |EFE| {max(abs(v_['efe_dex']) for v_ in Cc.values()):.2e} dex "
    f"(delta_c 0.082); max delta_eq/a {max(v_['deq_over_a'] for v_ in Cc.values()):.2e}; host tidal term up to "
    f"{max(v_['tidal_dex'] for v_ in Cc.values()):.3f} dex (reported, not an EFE)")
RES["c"] = dict(C=Cc, c1=c1v)
rss_guard("c")
# ---- (d) slip


def slip_sct_pt(Mb_sun, rk, a0):
    M = Mb_sun * MSUN847; rr = rk * KPC847; N = domain_sct(Mb_sun, a0)["N"]; Mc = N * M
    re = root_pt(M, Mc, a0, "simple")
    if rr >= re:
        return 0.0, 0.0
    sig = lambda x: ((Mph_pt(x * (1 + 1e-6), M, a0, "simple") - Mph_pt(x * (1 - 1e-6), M, a0, "simple")) / (2e-6 * x)) / (4 * math.pi * x * x)
    gl = lambda x: float(law_simple(G_SI * M / x ** 2, a0))
    p = quad(lambda x: sig(x) * gl(x), rr, re, limit=400)[0]
    g_ = gl(rr)
    return 4 * math.pi * G_SI * rr * p / (C_SI ** 2 * g_), 8 * math.pi * G_SI * rr ** 2 * p / (C_SI ** 2 * g_ * rr)


Dd = {}; worst_d = 0.0
for foot in FOOTS:
    for name, Mb, rk in SYS847:
        sg_, s8_ = slip_sct_pt(Mb, rk, A0[foot]); Dd[f"{foot}|{name}"] = dict(s_grad=sg_, s_847=s8_); worst_d = max(worst_d, sg_, s8_)
    # NGC 3198 at its radii (spherical-equivalent baryons inside, point mass beyond)
    a0 = A0[foot]; dom = domain_sct(MB_N, a0)
    xg = np.geomspace(R_N[0], dom["r_e"], 20000)
    Mx = np.where(xg <= R_N[-1], np.interp(xg, R_N, MBR_N), MB_N * MSUN)
    gnx = G_SI * Mx / xg ** 2; glx = law_simple(gnx, a0); Mphx = xg ** 2 * (glx - gnx) / G_SI
    sigx = np.gradient(Mphx, xg) / (4 * math.pi * xg ** 2)
    f_ = sigx * glx; cum = np.concatenate(([0.0], np.cumsum(0.5 * (f_[1:] + f_[:-1]) * np.diff(xg))))
    px = cum[-1] - cum
    pN = np.interp(R_N, xg, px); gN_ = law_simple(GN_N, a0)
    sN = max(float(np.max(4 * math.pi * G_SI * R_N * np.abs(pN) / (C_SI ** 2 * gN_))), float(np.max(8 * math.pi * G_SI * R_N * np.abs(pN) / (C_SI ** 2 * gN_))))
    Dd[f"{foot}|NGC3198"] = dict(worst=sN); worst_d = max(worst_d, sN)
gd = "PASS" if worst_d <= 1.9e-5 else "FAIL"
for v_ in GR: GR[v_]["d"] = gd
chk("d_slip", worst_d <= 1.9e-5, f"worst slip {worst_d:.4e} (line 1.9e-5); " + ", ".join(f"{k} {max(v_.values()):.2e}" for k, v_ in Dd.items() if k.startswith("alt")))
RES["d"] = Dd
# ---- (e) conservation: toys + third law
P("  (e) conservation: N-body toys (criteria section 4) ...")
tE1 = run_toy("E", 2e-3, 40.0, label="E dt 2e-3"); toy_line(tE1, "run E, dt 2e-3")
rss_guard("toy E1")
tE2 = run_toy("E", 1e-3, 40.0, label="E dt 1e-3"); toy_line(tE2, "run E, dt 1e-3")
rss_guard("toy E2")
tM = run_toy("M", 2e-3, 30.0, label="M"); toy_line(tM, "run M (merger), dt 2e-3")
for ev in tM["events"]["merges"]:
    P(f"     merge: baryon separation {ev['sep_b']:.3f}; Delta E_int {ev['dEint']:+.3f} (K loss {ev['Kloss']:+.3f}, Delta W {ev['dW']:+.3f}) = "
      f"{ev['dEint'] / abs(tM['E0']):+.4f} |E0|; T-L field jump at r = 5: g before {ev['g5_before']:.4f}, after {ev['g5_after']:.4f} "
      f"(ratio {ev['g5_after'] / ev['g5_before']:.3f})")
for ev in tE1["events"]["merges"]:
    P(f"     run E merge (satellite B): baryon separation {ev['sep_b']:.3f}; Delta E_int {ev['dEint']:+.4f}")
rss_guard("toy M")


def body_cont(Mb, a, Mc):
    Mbr = lambda s: Mb * s ** 3 / (s * s + a * a) ** 1.5
    Mph = lambda s: s * s * (float(lawT(Mbr(s) / s ** 2)) - Mbr(s) / s ** 2)
    re = brentq(lambda s: Mph(s) - Mc, 1e-6, 1e6, xtol=1e-14, rtol=1e-14)
    Ms = lambda s: Mph(s) if s < re else Mc
    gq = lambda s: Ms(s) / s ** 2 if s > 0 else 0.0
    dMs = lambda s: (Mph(s * (1 + 1e-7)) - Mph(s * (1 - 1e-7))) / (2e-7 * s) if s < re else 0.0
    return dict(gq=gq, dMs=dMs, re=re)


def third_law(bp, bq, D):
    def inner(s):
        def fmu(mu):
            rho = math.sqrt(max(D * D + s * s + 2 * D * s * mu, 1e-300)); return bq["gq"](rho) * (D + s * mu) / rho
        pts = []
        if s > 0 and D > 0:
            ms_ = (bq["re"] ** 2 - D * D - s * s) / (2 * D * s)
            if -1 < ms_ < 1: pts.append(ms_)
        return 0.5 * quad(fmu, -1, 1, points=pts or None, epsabs=0, epsrel=1e-12, limit=200)[0]
    brk = sorted(set([x_ for x_ in (D, abs(bq["re"] - D), bq["re"] + D) if 0 < x_ < bp["re"]]))
    edges = [1e-9] + brk + [bp["re"]]
    tot = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        tot += quad(lambda s: bp["dMs"](s) * inner(s), lo, hi, epsabs=0, epsrel=1e-11, limit=400)[0]
    return tot


bP = body_cont(1.0, 1.0, 20.0); bQ = body_cont(0.3, 0.5, 8.0)
F_pq = third_law(bP, bQ, 6.0); F_qp = third_law(bQ, bP, 6.0)
e3 = abs(F_pq - F_qp) / abs(F_pq)
mom_ok = ST["S-P"] and ST["S-TM"] and ST["S-L"] and all(t_["dP"] <= 1e-10 and t_["dL"] <= 1e-10 for t_ in (tE1, tE2, tM)) and e3 <= 1e-6
en_closed = all(t_["dE"] <= 1e-3 for t_ in (tE1, tM)) and tE2["dE"] < tE1["dE"]
eint_zero = all(abs(v_) < 1e-12 for t_ in (tE1, tE2, tM) for v_ in t_["eint_final"].values())
if mom_ok and en_closed:
    ge = "PASS" if eint_zero else "CONDITIONAL"
else:
    ge = "FAIL"
for v_ in GR: GR[v_]["e"] = ge
chk("e_conservation", mom_ok and en_closed, f"momentum/angular momentum: max dP {max(t_['dP'] for t_ in (tE1, tE2, tM)):.1e}, dL "
    f"{max(t_['dL'] for t_ in (tE1, tE2, tM)):.1e} (line 1e-10); third law between overlapping bodies {e3:.1e} (line 1e-6); energy with E_int: "
    f"{tE1['dE']:.2e} (dt 2e-3) -> {tE2['dE']:.2e} (dt 1e-3), merger {tM['dE']:.2e} (line 1e-3); E_int needed: "
    + ", ".join(f"{k} {v_:+.3f}" for k, v_ in tE1["eint_over_E0"].items()) + f" |E0| (run E); merger {tM['eint_over_E0']['merge']:+.3f} |E0| -> (e) {ge}")
RES["e"] = dict(toyE1=tE1, toyE2=tE2, toyM=tM, third_law=dict(F_pq=F_pq, F_qp=F_qp, rel=e3))
# ---- (f) dwarfs: no RMIN; the edge's effect on the dispersion


def jeans_ap(Mb_sun, a_kpc, a0, kern, trunc):
    M = Mb_sun * MSUN; a = a_kpc * KPC; N = domain_sct(Mb_sun, a0, kern)["N"]; Mc = N * M; law = KERN[kern]
    Mbr = lambda s: M * s ** 3 / (s * s + a * a) ** 1.5
    rg = np.geomspace(1e-3 * a, 1e3 * a, 3000)
    Mb_ = Mbr(rg); gn = G_SI * Mb_ / rg ** 2; Mph = rg ** 2 * (law(gn, a0) - gn) / G_SI
    mono = bool(np.all(np.diff(Mph) > 0))
    Mt = Mb_ + (np.minimum(Mph, Mc) if trunc else Mph)
    rho = 3 * M * a * a / (4 * math.pi * (rg * rg + a * a) ** 2.5)
    f_ = rho * G_SI * Mt / rg ** 2
    cum = np.concatenate(([0.0], np.cumsum(0.5 * (f_[1:] + f_[:-1]) * np.diff(rg))))
    rs2 = cum[-1] - cum                                                   # rho sigma_r^2
    lrs = np.log(np.maximum(rs2, 1e-300))
    ug = np.concatenate(([0.0], np.geomspace(1e-5 * a, 9.9e2 * a, 2500)))
    xg_, wg_ = np.polynomial.legendre.leggauss(48)
    Rr = 0.5 * a * (xg_ + 1); wR = 0.5 * a * wg_
    num = 0.0; den = 0.0
    for R_, w_ in zip(Rr, wR):
        rr_ = np.sqrt(R_ * R_ + ug * ug)
        val = np.exp(np.interp(np.log(rr_), np.log(rg), lrs))
        Sig_s2 = 2 * float(np.sum(0.5 * (val[1:] + val[:-1]) * np.diff(ug)))
        Sig = M * a * a / (math.pi * (a * a + R_ * R_) ** 2)
        num += w_ * Sig_s2 * R_; den += w_ * Sig * R_
    re = root_pt(M, Mc, a0, kern) if Mph[-1] >= Mc else float("inf")
    return num / den, mono, re / a


DW = [("UFD-c", 5e3, 0.030), ("UFD-e", 3e4, 0.240), ("Draco-like", 5e5, 0.220), ("Fornax-like", 4e7, 0.710),
      ("H1", 1e4, 0.030), ("H2", 3e5, 0.200), ("H3", 2e7, 0.700)]
Fd = {}; f_ok = True
for foot in FOOTS:
    for kz in KERN:
        for nm, Mb, ak in DW:
            s_t, mono_, re_a = jeans_ap(Mb, ak, A0[foot], kz, True); s_l, _, _ = jeans_ap(Mb, ak, A0[foot], kz, False)
            dd = math.log10(s_t / s_l)
            Fd[f"{foot}|{kz}|{nm}"] = dict(dlog_sigma2=dd, monotone=mono_, r_e_over_a=re_a)
            f_ok = f_ok and mono_ and abs(dd) <= DELTA_C
spd = domain_sct(2.6e7 + 3.66e8, A0["canonical"]); spd_alt = domain_sct(2.6e7 + 3.66e8, A0["alt"])
grid_ok = all(domain_sct(float(Mb), A0[f], kz)["r_e"] > 0 for f in FOOTS for kz in KERN for Mb in np.logspace(3, 15, 13))
f_ok = f_ok and spd["r_e"] > 5.0 * KPC and spd_alt["r_e"] > 5.0 * KPC and grid_ok
for k, v_ in Fd.items():
    if "|simple|" in k:
        P(f"   {k:30s}: edge moves sigma^2_ap(<R_e) by {v_['dlog_sigma2']:+.4f} dex; r_e/a {v_['r_e_over_a']:.1f}; sigma >= 0 {v_['monotone']}")
gf = "PASS" if f_ok else "FAIL"
for v_ in GR: GR[v_]["f"] = gf
chk("f_dwarfs_no_RMIN", f_ok, f"max |edge effect| {max(abs(v_['dlog_sigma2']) for v_ in Fd.values()):.4f} dex (line 0.082); SPARC dwarf r_e "
    f"{spd['r_e'] / KPC:.1f} / {spd_alt['r_e'] / KPC:.1f} kpc > r_obs 5 kpc; domain for every M_b 1e3-1e15: {grid_ok}. Excess family: SCT predicts the "
    "EFE-free law of own baryons for every dwarf (0 dex excess); no computation here gives an excess -> NO HANDLE")
RES["f"] = Fd
# ---- (g) below-law systems (CFG936 data and class rule)
Gg = {}; ptsU_by_foot = {}
for foot in FOOTS:
    Rf = R936["routes"][foot]
    rlawT = Rf["law"]["T"]["stats"]["rbar"]; rlawU = Rf["law"]["U"]["stats"]["rbar"]
    stT = stats936(Rf["route_i"]["T"]["per_object"])                    # f = 0 exactly (route i T is Newton)
    ptsU = []
    for o in Rf["route_i"]["U"]["per_object"]:
        Ep = -math.log(o["nu"]); s_obs = o["sigma_law"] * math.exp(o["E_obs"] / 2)
        sp0 = o["sigma_law"] * math.exp(Ep / 2); sp_i = o["sigma_pred"]
        assert (s_obs > sp0) == (s_obs > sp_i), "error branch flips between f = 0 and route (i)"
        ptsU.append(dict(name=o["name"], r=o["E_obs"] - Ep, s=o["sE"]))
    stU = stats936(ptsU); ptsU_by_foot[foot] = ptsU
    stTq = stats936(Rf["route_iii_EFE_contrast"]["T"]["per_object"]); stUq = stats936(Rf["route_iii_EFE_contrast"]["U"]["per_object"])
    Gg[foot] = dict(M_T=dict(st=stT, cls=basic_class936(stT, rlawT)), M_U=dict(st=stU, cls=basic_class936(stU, rlawU)),
                    Q_T=dict(st=stTq, cls=basic_class936(stTq, rlawT)), Q_U=dict(st=stUq, cls=basic_class936(stUq, rlawU)))
    for kk in ("M_T", "M_U", "Q_T", "Q_U"):
        st_ = Gg[foot][kk]["st"]
        P(f"   {foot:9s} {kk}: rbar {st_['rbar']:+.3f} +- {st_['se']:.3f} (z {st_['z_mean']:+.2f}); chi2 {st_['chi2']:.2f}/{st_['n']} (p {st_['p']:.3g}) "
          f"-> {Gg[foot][kk]['cls']}")


def grade_g(pref):
    T = [Gg[f][pref + "_T"]["cls"] for f in FOOTS]; U = [Gg[f][pref + "_U"]["cls"] for f in FOOTS]
    if any(c_ == "FAILS" for c_ in T + U):
        return "FAIL"
    if all(c_ == "EXPLAINS" for c_ in T + U):
        return "CONDITIONAL"                                              # U rests on the in-situ (debris) origin of DF2/DF4 (C-DF)
    return "UNDEFINED (PARTIAL: not covered by the frozen rule)"


GR["SCT-M"]["g"] = grade_g("M"); GR["SCT-Q"]["g"] = grade_g("Q")
chk("g_below_law_SCT-M", GR["SCT-M"]["g"] != "FAIL", f"SCT-M (Newton for in-situ systems): T {[Gg[f]['M_T']['cls'] for f in FOOTS]}, U "
    f"{[Gg[f]['M_U']['cls'] for f in FOOTS]} -> {GR['SCT-M']['g']} (U conditional on DF2/DF4 being in-situ debris)")
P(f"   SCT-Q (host EFE for in-situ systems, CFG936 route iii): T {[Gg[f]['Q_T']['cls'] for f in FOOTS]}, U {[Gg[f]['Q_U']['cls'] for f in FOOTS]} "
  f"-> {GR['SCT-Q']['g']}")
P("   CFG936's own route classes with its declared corners (reported): route (i) T " + str([R936['routes'][f]['route_i']['T']['cls'] for f in FOOTS])
  + ", U " + str([R936['routes'][f]['route_i']['U']['cls'] for f in FOOTS]) + "; route (iii) T " + str([R936['routes'][f]['route_iii_EFE_contrast']['T']['cls'] for f in FOOTS])
  + ", U " + str([R936['routes'][f]['route_iii_EFE_contrast']['U']['cls'] for f in FOOTS]) + " (the grade above uses the primary basic class)")
P("   CFG939: inside a collapsed parent no unlabelled dust exists, so capture is impossible whatever v_rel (stronger than v_rel > V_esc,b); "
  "CFG948 Coma UDGs: Newton excluded at 5.45 sigma, so under SCT they must be turnaround-born (own body): law ceiling +0.018 ln vs +0.76 "
  "observed (z +1.63 / +1.43 with systematics; NOT DIAGNOSTIC, as CFG948)")
RES["g"] = Gg
# ---- A1 (pre-result amendment 611bb324a; reported only, no class weight): the parent body's local density inside in-situ systems


def body_rho(Mh_kg, Dm, a0):
    dom = domain_sct(Mh_kg / MSUN, a0)
    if Dm >= dom["r_e"]:
        return 0.0
    return (Mph_pt(Dm * (1 + 1e-4), Mh_kg, a0, "simple") - Mph_pt(Dm * (1 - 1e-4), Mh_kg, a0, "simple")) / (2e-4 * Dm) / (4 * math.pi * Dm ** 2)


TDGCSV = list(csv.DictReader(open(os.path.join(REPO, "real_research", "data", "tidal_dwarfs", "lelli2015_tdg.csv"))))
A1g = {}
for foot in FOOTS:
    a0 = A0[foot]; ptsT = []; rowsT = {}
    for o in R936["routes"][foot]["route_i"]["T"]["per_object"]:
        c_ = [rw for rw in TDGCSV if rw["object"].replace(" ", "") == o["name"]][0]
        Mh = 0.6 * float(c_["host_LK_1e10Lsun"]) * 1e10 * MSUN; Dm = float(c_["D_p_kpc"]) * KPC; Ro = float(c_["R_out_kpc"]) * KPC
        rh = body_rho(Mh, Dm, a0); dg = 4 * math.pi / 3 * G_SI * rh * Ro; dd = math.log10(1 + dg / 10 ** o["lgbar"])
        rowsT[o["name"]] = dd; ptsT.append(dict(r=o["r"] - dd, s=o["s"]))
    ptsU2 = []; rowsU = {}
    for o, (nm, Ms_, Re_, R52, R35) in zip(ptsU_by_foot[foot], (("DF2", 2.0e8, 2.0, 79.3, 219.5), ("DF4", 1.5e8, 1.6, 165.3, 21.0))):
        assert o["name"] == nm
        rh = body_rho(1e11 * MSUN, R52 * KPC, a0) + body_rho(5e9 * MSUN, R35 * KPC, a0)
        rr_ = 1.305 * Re_ * KPC; dl = math.log(1 + (4 * math.pi / 3) * rh * rr_ ** 3 / (0.5 * Ms_ * MSUN))
        rowsU[nm] = dl; ptsU2.append(dict(r=o["r"] - dl, s=o["s"]))
    sT2 = stats936(ptsT); sU2 = stats936(ptsU2)
    A1g[foot] = dict(T_shift_dex=rowsT, U_shift_ln=rowsU, T=dict(st=sT2, cls=basic_class936(sT2, R936["routes"][foot]["law"]["T"]["stats"]["rbar"])),
                     U=dict(st=sU2, cls=basic_class936(sU2, R936["routes"][foot]["law"]["U"]["stats"]["rbar"])))
    P(f"   A1 (reported) {foot}: host-body term T shifts " + ", ".join(f"{k} {v_:+.3f}" for k, v_ in rowsT.items()) + f" dex -> rbar "
      f"{sT2['rbar']:+.3f} +- {sT2['se']:.3f} ({A1g[foot]['T']['cls']}); U shifts " + ", ".join(f"{k} {v_:+.3f}" for k, v_ in rowsU.items())
      + f" ln -> rbar {sU2['rbar']:+.3f} +- {sU2['se']:.3f} ({A1g[foot]['U']['cls']})")
RES["A1_g_host_body"] = A1g
# ---- (h) CFG678 scorecard (reported)
P("  (h) CFG678 scorecard (reported; SCT has no action: gates set by S cannot PASS)")
k_sp = {f: sparc_rms(A0[f], pred_sct, f"SCT-M SPARC {f}") for f in FOOTS}
c2_ok_h = all(abs(k_sp[f]["rms"] - k5[f"local|{f}"]["rms"]) <= 1e-9 and k_sp[f]["n_special"] == 0 for f in FOOTS)
rhoMW = None
dmw = domain_sct(6e10, A0["canonical"]); Mmw = 6e10 * MSUN; R0 = 8.0 * KPC
rhoMW = (Mph_pt(R0 * 1.0001, Mmw, A0["canonical"], "simple") - Mph_pt(R0 * 0.9999, Mmw, A0["canonical"], "simple")) / (0.0002 * R0) / (4 * math.pi * R0 ** 2)
tide_sun = 4 * math.pi * G_SI * rhoMW / 3
z_newt = {"canonical": (1.0 - 1.0750) / 0.0550, "alt": (1.0 - 1.0775) / 0.0512}
SC = [
    ("A1 ghost / 2nd order", "CONDITIONAL", "CONDITIONAL", "metric + matter variational and 2nd order; S non-dynamical, 0 field initial data; body centroids are positive-inertia ODEs (fixed at birth); premise: action-less S admitted"),
    ("A2 hyperbolicity", "CONDITIONAL", "CONDITIONAL", "GR + dust hyperbolic; S retarded at c (R8); premise C-c (finite-c_u body)"),
    ("A3 nonlinear WP", "UNTESTED", "UNTESTED", "not proved; event-driven"),
    ("A4 strong coupling", "UNTESTED", "UNTESTED", "not computed"),
    ("A5 GW at c", "PASS", "PASS", "Einstein-Hilbert unmodified; S has no curvature coupling (structural)"),
    ("A6 BH exteriors", "CONDITIONAL", "CONDITIONAL", "in-situ black holes are not domains; a host body is smooth near them"),
    ("A7 radiative", "DECLARED", "DECLARED", "CFG320"),
    ("B1 switch from variation", "UNTESTED", "UNTESTED", "the switch (conversion at turnaround) is the action-less label sector; prescribed"),
    ("B2 a0-Lambda tie", "UNTESTED", "UNTESTED", "a0 constant; kappa = 1/2 FITTED"),
    ("B3 cold sector", "CONDITIONAL", "CONDITIONAL", "dust well-posed and lenses like mass; bodies in T_mu nu, slip <= 1.9e-5; energy through E_int (C-E)"),
    ("C1 Cassini", "CONDITIONAL", "NOT DECIDED", f"SCT-M: the Sun is in situ (no own body), the MW body is smooth: tidal gradient 4 pi G rho/3 = {tide_sun:.2e} s^-2 (ordinary galactic tide, no EFE quadrupole); SCT-Q: the Sun is MW-own baryons inside the pointwise phantom -> QUMOND EFE quadrupole (G01/G02: strict AQUAL fails 3.8-5.5x; not recomputed)"),
    ("C2 SPARC", "CONDITIONAL" if c2_ok_h else "FAIL", "CONDITIONAL" if c2_ok_h else "FAIL", f"SCT-M rms {k_sp['canonical']['rms']:.4f} / {k_sp['alt']['rms']:.4f} (= local); 0 points beyond an edge; law from the prescribed S"),
    ("C3 early types", "FAIL", "FAIL", "inherits CFG529 (the law inside r_e)"),
    ("C4 cluster lensing", "NOT DECIDED", "NOT DECIDED", "CFG954"),
    ("D1 zero field", "UNTESTED", "UNTESTED", "not run"),
    ("D2 growth", "UNTESTED", "UNTESTED", "linear n = 1 by construction; the CFG596 line needs an SCT PM engine and a 1024^3 run; class-A passes do not transfer"),
    ("D3 flat a0(z)", "PENDING", "PENDING", "sealed tests 2026-11-06 / 2026-11-28"),
    ("E1-E3", "DECLARED", "DECLARED", "kappa = 1/2 FITTED"),
]
for g_, sm_, sq_, src_ in SC:
    P(f"   {g_:24s} SCT-M {sm_:12s} SCT-Q {sq_:12s} {src_}")
P(f"   wide binaries: SCT-M Newtonian (in situ, smooth host body): z {z_newt['canonical']:.2f} / {z_newt['alt']:.2f} vs DR3 builder (PASS, |z| <= 2; "
  "agrees with the sealed DR4 'exactly Newtonian'); SCT-Q: QUMOND EFE, CFG653's 1.179 (+1.3) / 1.244 (+2.3) (PASS / TENSION)")
RES["h"] = dict(scorecard=SC, sparc=k_sp, tide_sun=tide_sun, rho_MW_R0=rhoMW, z_binaries_newton=z_newt)
# ---- clusters (first-order, no computation)
P("  clusters (first order, no class weight; CFG954 decides): members keep their whole bodies until R7 and the host's body is the law of the "
  "host's own baryons, so the cluster lies between CFG951's plain-law row (all merged: eRASS1 A_MID 1.91 / 1.75, Z +7.7 / +6.9) and its "
  "X-OD row (members kept, there L2-truncated: A_OUTER 0.81 / 0.75, Z -2.7 / -4.0). SCT-M's members are not truncated, so if they persist "
  "the memory is at least X-OD's.")

# ================================================================================================ classes
P("\n==================== CLASSES ====================")
CLASS = {}
for v_ in ("SCT-M", "SCT-Q"):
    gs = GR[v_]
    if any(gs[t_] == "FAIL" for t_ in "abcdefg"):
        CLASS[v_] = "SCT INCONSISTENT"
    elif all(gs[t_] == "PASS" for t_ in "abcdefg"):
        CLASS[v_] = "SCT CONSISTENT"
    else:
        CLASS[v_] = "SCT CONDITIONAL"
    conds = []
    if gs["e"] == "CONDITIONAL": conds.append("C-E")
    if gs["g"] == "CONDITIONAL": conds.append("C-DF")
    P(f"  {v_}: " + " ".join(f"{t_}:{gs[t_]}" for t_ in "abcdefg") + f"  -> {CLASS[v_]}" + (f"  (conditions {', '.join(conds)}; open for "
      "real systems: C-MR, C-c)" if CLASS[v_] == "SCT CONDITIONAL" else ""))
OVER = CLASS["SCT-M"] if K_ALL else "VOID (K failed)"
P(f"  OVERALL (SCT-M, primary): {OVER}")
RES["grades"] = GR; RES["classes"] = CLASS; RES["overall"] = OVER; RES["structural"] = ST
dump()
P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")

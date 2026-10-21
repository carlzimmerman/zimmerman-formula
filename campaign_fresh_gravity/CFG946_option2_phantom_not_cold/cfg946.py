"""CFG946 -- option 2: cold energy is NOT literally the law's phantom (dust self-gravity kept; the law from a separate sector).
Criteria: FROZEN_CRITERIA.md (08f3b30a6, committed alone before this script); amendment A1 (23e0a5765).
Run (one core, one process, < 1 GB):
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg946.py              -> cfg946.out, cfg946_results.json (K + main)
    CFG946_STAGE=K ...                                          -> cfg946_K.out, cfg946_results_K.json (K only)
    CFG946_MUTATE=1 ...                                         -> cfg946_MUTATE.out, cfg946_results_MUTATE.json
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite).
kappa = 1/2 FITTED; footings never pooled; no particle species added; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq, minimize
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG946_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG946_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
OUT = []
RES = {"lane": "CFG946", "criteria": "08f3b30a6", "amendments": ["A1 23e0a5765 (code/reporting; items 6-7 post-result, no class change)"], "mutate": MUT, "stage": STAGE, "checks": {}, "tests": {}}
T0 = time.time()
RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r_ = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r_ if sys.platform == "darwin" else r_ * 1024


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg946_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg946{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def rss_guard(where=""):
    r_ = rss_val()
    if r_ > RSS_LIMIT:
        P(f"RSS GUARD: {r_ / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def is0(e):
    return sp.simplify(sp.expand(e)) == 0


def jload(*parts):
    return json.load(open(os.path.join(LANES, *parts)))


# ------------------------------------------------------------------------------------------------ constants (read-only inputs)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # the record's footings
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC, KPC = 6.67430e-11, 299792458.0, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e19
K_SI = 4 * math.pi * G_SI
MSUN847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's constants for its systems (as CFG938/941)
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0),
          ("cluster", 1.5e14, 1000.0)]
H0_SI = 67.4e3 / (1e6 * PC); RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI); HLIT = 0.674
OB = 0.0493; OC = 5.364 * OB; OM0 = OB + OC; RHO_M0 = OM0 * RHO_CRIT; RHO_C0 = OC * RHO_CRIT
DTA = 5.55                                                             # EdS turnaround overdensity (declared)
FB, FC = OB / OM0, OC / OM0
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]  # CFG882 Plummer dwarfs (M_sun, pc)
HOST938 = 6e10                                                          # CFG938/941 host (M_sun), radii 50/100/250 kpc
RHOST = (50.0, 100.0, 250.0)


def law_g(gN, a0):
    return 0.5 * (gN + math.sqrt(gN * gN + 4.0 * gN * a0))


def uph(gN, a0):                                                      # phantom field u = g_law - g_N (stable); R(u) = g_N
    return 2.0 * gN * a0 / (gN + math.sqrt(gN * gN + 4.0 * gN * a0)) if gN > 0 else 0.0


def nu_s(y):                                                          # law (simple) nu
    return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 / y))


def nut_s(y):                                                         # nu - 1, stable
    return 2.0 / (y * (math.sqrt(1.0 + 4.0 / y) + 1.0))


def nu_e(y):                                                          # record's exponential nu (CFG925 K7 link only)
    return 1.0 / (-math.expm1(-math.sqrt(y)))


def R_num(u_, a0):
    return u_ * u_ / (a0 - u_)


def Rp_num(u_, a0):
    return u_ * (2 * a0 - u_) / (a0 - u_) ** 2


def wrem_x(x):                                                        # -x - log(1-x) - x^2/2, stable
    if x < 1e-2:
        return sum(x ** n / n for n in range(3, 16))
    return -x - math.log1p(-x) - x * x / 2


def Wrem_num(u_, a0):
    return a0 * a0 * wrem_x(u_ / a0) / K_SI


def r_ta(Mb_kg):                                                      # turnaround radius of a fair catchment of total 6.364 M_b
    return (3 * (OM0 / OB) * Mb_kg / (4 * math.pi * DTA * RHO_M0)) ** (1.0 / 3.0)


# NGC 3198 (record SPARC file, Upsilon 0.61 as CFG938/941)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MB_N = GN_N[-1] * R_N[-1] ** 2 / G_SI
RTA_N = r_ta(MB_N)

P("CFG946  option 2: cold energy is NOT literally the law's phantom" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P("  criteria 08f3b30a6; A1 23e0a5765; kappa = 1/2 FITTED; footings never pooled; no particle species added; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2;  NGC 3198: {len(R_N)} radii, "
  f"M_b(<{R_N[-1] / KPC:.1f} kpc) = {MB_N / MSUN:.3e} Msun; fair-catchment turnaround radius r_ta = {RTA_N / KPC:.1f} kpc")

# ================================================================================================ shared sympy
r, G, a0s, gam = sp.symbols("r G a_0 gamma", positive=True)
u, gN = sp.symbols("u g_N", positive=True)
C2s, Bs = sp.symbols("c_2 b", nonnegative=True)
KS = 4 * sp.pi * G
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / KS
Wrem = Wfull - u ** 2 / (2 * KS)
Wc2 = Wrem + C2s * u ** 2 / (2 * KS)                                  # O2c family
Dfull = sp.simplify(KS * sp.diff(Wfull, u))
Rrem = sp.simplify(KS * sp.diff(Wrem, u))


def EL_alg(Wuse, m=1):
    """gamma -> 0 Euler-Lagrange of E[M_c] = int[-G(M_b + m M_c)^2/(2 r^2) + 4 pi r^2 W(G M_c/r^2)] dr, as a function of (u, g_N).
    m = source multiplicity of the dust's own field (m = 2 is the double count, M2)."""
    Mc = sp.Function("M_c")(r); Mb = sp.Function("M_b")(r)
    Wf = sp.Lambda(u, Wuse)
    Lr = -G * (Mb + m * Mc) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wf(G * Mc / r ** 2)
    eq = sp.euler_equations(Lr, [Mc], [r])[0].lhs
    return sp.simplify(eq.subs({Mc: u * r ** 2 / G, Mb: gN * r ** 2 / G}).doit())


_ELC = {}


def solve_static(Wuse, m, gNarr, a0, c2=0.0, key=None):
    """root u of the reduced EL at each g_N; total g = g_N + m u."""
    k_ = key or (str(Wuse), m)
    if k_ not in _ELC:
        ex = EL_alg(Wuse, m)
        _ELC[k_] = (ex, sp.lambdify((u, gN, a0s, G, C2s), ex, "math"))
    ex, f = _ELC[k_]
    grid = a0 * np.unique(np.concatenate((np.logspace(-14, -1e-12, 900), np.linspace(1e-4, 1 - 1e-13, 3000))))
    us = []
    for gn in gNarr:
        vals = np.array([f(x, gn, a0, G_SI, c2) for x in grid])
        idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) <= 0)[0]
        if len(idx) == 0:
            us.append(float("nan")); continue
        i = idx[0]
        us.append(brentq(lambda x: f(x, gn, a0, G_SI, c2), grid[i], grid[i + 1], xtol=1e-40, rtol=1e-15, maxiter=800))
    us = np.array(us)
    return us, gNarr + m * us, ex


def law_dev(g_tot, gNarr, a0):
    gl = np.array([law_g(x, a0) for x in gNarr])
    return float(np.nanmax(np.abs(g_tot / gl - 1))), int(np.sum(~np.isfinite(g_tot)))


def dex_dev(g_tot, gNarr, a0):
    gl = np.array([law_g(x, a0) for x in gNarr])
    return float(np.nanmax(np.abs(np.log10(g_tot / gl))))


def btfr_numeric(Wuse, a0, y=1e-14, c2=0.0):
    rr_ = math.sqrt(G_SI * MB_N / (y * a0))
    us, gt, _ = solve_static(Wuse, 1, np.array([y * a0]), a0, c2)
    return float((gt[0] * rr_) ** 2 / (G_SI * MB_N * a0))


# ------------------------------------------------------------------------------------------------ growth machinery (CFG941 route, re-implemented)
tt = sp.symbols("t", positive=True); al = sp.symbols("alpha")
Kg = sp.Symbol("K", positive=True)
FBr, FCr = sp.Rational(1000, 6364), sp.Rational(5364, 6364)


def growth_det(comp):
    """comp: list of (name, fraction, tethered). L = sum 1/2 rho_i a^5 psi_i'^2 + (a^5 K/2)(sum rho_i psi_i)^2
    - (a^5 c2/2K)(-K rho_T psi_T + b beta psi_T')^2, beta = -K rho_T/(3H) (CFG938 chi background).  EdS: a = t^(2/3)."""
    a = tt ** sp.Rational(2, 3); H = sp.Rational(2, 3) / tt; rtot = (sp.Rational(2, 3) / tt ** 2) / Kg
    psis = [sp.Function("psi_" + n)(tt) for n, _, _ in comp]
    rho = [f * rtot for _, f, _ in comp]
    L = sum(sp.Rational(1, 2) * rh * a ** 5 * sp.diff(ps, tt) ** 2 for rh, ps in zip(rho, psis))
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
    return 1.5 * max(z.real for z in roots if abs(z.imag) < 1e-9)


P("\n  deriving the growth determinant (sympy, CFG941 route) ...")
DET2, HOM2 = growth_det([("b", FBr, False), ("t", FCr, True)])
rss_guard("growth det")


def n2(c2, b):
    return n_from_det(DET2, {C2s: c2, Bs: b})


def n_eps(eps):
    """EdS constant-epsilon growth: alpha(alpha-1) + 4 alpha/3 = (2/3)(1 + eps), n = 3 alpha/2."""
    a_ = (-1.0 / 3.0 + math.sqrt(1.0 / 9.0 + (8.0 / 3.0) * (1.0 + eps))) / 2.0
    return 1.5 * a_


def n_lam(lam):
    return n_eps(lam - 1.0)


# ------------------------------------------------------------------------------------------------ exact Gauss-flux EFE (QUMOND-type sectors)
def gauss_boost(nu, gs, ge, a0):
    """Mean inward acceleration over a sphere / gs, for a QUMOND-type sector: flux of nu(|g_N|/a0) g_N, with the internal Newtonian
    field gs (radial, inward) and a uniform external Newtonian field ge.  Exact (the curl part has zero flux).  Subtraction of
    nu(ge) is an exact identity that removes the cancellation in the EFE-dominated limit."""
    if ge <= 0:
        return nu(gs / a0)
    nue = nu(ge / a0) if ge > gs else 0.0                               # any constant works; this choice avoids cancellation

    def f(mu):
        gm = math.sqrt(max(gs * gs + ge * ge - 2.0 * gs * ge * mu, 1e-300))
        return (nu(gm / a0) - nue) * (gs - ge * mu)
    val, _ = quad(f, -1.0, 1.0, limit=400, epsabs=0.0, epsrel=1e-12)
    return (val + 2.0 * nue * gs) / (2.0 * gs)


def plummer_g_at_a(M_sun, a_pc):                                      # Newtonian field at the Plummer scale radius
    return G_SI * M_sun * MSUN847 / (2.0 ** 1.5 * (a_pc * PC) ** 2)


def host_fields(rk, a0):
    Mh = HOST938 * MSUN847; rh = rk * KPC847
    gbh = G_SI * Mh / rh ** 2
    rt_h = r_ta(Mh)
    gdh = G_SI * 5.364 * Mh * min(rh / rt_h, 1.0) / rh ** 2              # host D-F dust (O2a-3 only)
    return gbh, gdh


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
# K1
k1 = {}
for foot in FOOTS:
    us, gt, ex_k1 = solve_static(Wfull, 1, GN_N, A0[foot])
    dv, nn = law_dev(gt, GN_N, A0[foot]); k1[foot] = dict(max_rel_vs_law=dv, unsolved=nn)
P(f"  K1 reduced EL (CFG938 W_full, m = 1): {sp.factor(ex_k1)}")
K1 = chk("K1_NGC3198_law_CFG938_reduction", all(k1[f]["max_rel_vs_law"] < 1e-6 and k1[f]["unsolved"] == 0 for f in FOOTS),
         f"max |g/g_law - 1| canonical {k1['canonical']['max_rel_vs_law']:.2e}, alt {k1['alt']['max_rel_vs_law']:.2e} (CFG938/941: 2.2e-16; line 1e-6)")
RES["K1"] = k1
# K2
P(f"  (K1 done {time.time() - T0:.1f} s)")
n_full = n2(1, 1); n_dust = n2(0, 0)
K2 = chk("K2_CFG941_full_action_exponent", HOM2 and abs(n_full - 0.69433) < 1e-4 and abs(n_dust - 1) < 1e-12,
         f"full action (c2 = 1, chi-bar gradient on) n = {n_full:.6f} (CFG941 0.69433, line 1e-4); dust (c2 = 0) n = {n_dust:.12f}")
# K3: CL-AR Theorem 1 (three bodies, 3D, arbitrary pair potentials, uniform E(t))
tq = sp.Symbol("t", real=True)
ms = sp.symbols("m1:4", positive=True); gs_ = sp.symbols("gamma1:4", real=True)
Et = [sp.Function(f"E{i}")(tq) for i in range(3)]
X = [[sp.Function(f"x{a}_{i}")(tq) for i in range(3)] for a in range(3)]
Vf = {(0, 1): sp.Function("V12"), (0, 2): sp.Function("V13"), (1, 2): sp.Function("V23")}
dist = lambda a, b: sp.sqrt(sum((X[a][i] - X[b][i]) ** 2 for i in range(3)))


def internal_acc(charges):
    Lg = sum(sp.Rational(1, 2) * ms[a] * sum(sp.diff(X[a][i], tq) ** 2 for i in range(3)) for a in range(3))
    Lg -= sum(Vf[p](dist(*p)) for p in Vf)
    Lg += sum(charges[a] * sum(Et[i] * X[a][i] for i in range(3)) for a in range(3))
    flat = [X[a][i] for a in range(3) for i in range(3)]
    eqs = sp.euler_equations(Lg, flat, tq)
    acc = {}
    for e, xv in zip(eqs, flat):
        acc[xv] = sp.solve(e.lhs, sp.diff(xv, tq, 2))[0]
    M = sum(ms)
    Racc = [sum(ms[a] * acc[X[a][i]] for a in range(3)) / M for i in range(3)]
    return [[acc[X[a][i]] - Racc[i] for i in range(3)] for a in range(3)], Racc


ex0 = lambda e: sp.expand(e) == 0 or sp.simplify(sp.expand(e)) == 0
P(f"  (K3 start {time.time() - T0:.1f} s)")
yacc_min, Racc_min = internal_acc(ms)
dep_min = all(ex0(sp.diff(yacc_min[a][i], Et[j])) for a in range(3) for i in range(3) for j in range(3))
com_ok = all(ex0(Racc_min[i] - Et[i]) for i in range(3))
yacc_ch, _ = internal_acc(gs_)
coef_ok = all(ex0(sp.diff(yacc_ch[a][i], Et[i]) - (gs_[a] / ms[a] - sum(gs_) / sum(ms))) for a in range(3) for i in range(3))
P(f"  (K3 end {time.time() - T0:.1f} s)")
K3 = chk("K3_CLAR_theorem1_reproduced", dep_min and com_ok and coef_ok,
         "three bodies, arbitrary pair potentials V_ab(|x_a - x_b|), uniform E(t): internal accelerations independent of E (minimal coupling), "
         "COM acceleration = E; with passive charges the internal acceleration changes by (gamma_a/m_a - sum gamma/M) E (CL-AR A3/A4)")
rss_guard("K3")
# K4: CL-AR transport budget
k4 = {}
OMK4 = 0.315; RHOBAR_K4 = OMK4 * RHO_CRIT
for foot in FOOTS:
    a0 = A0[foot]; Mk = 1e10 * MSUN; rk_ = 10 * KPC
    gnk = G_SI * Mk / rk_ ** 2; Mlaw = rk_ ** 2 * uph(gnk, a0) / G_SI
    lmin = (rk_ ** 3 + 3 * Mlaw / (4 * math.pi * RHOBAR_K4)) ** (1 / 3) - rk_
    k4[foot] = lmin / KPC
fgen = [1 - (1 + x) ** -3 for x in (0.01, 0.1, 0.3)]
K4 = chk("K4_CLAR_transport_budget", abs(k4["canonical"] / 495 - 1) < 0.01 and abs(k4["alt"] / 514 - 1) < 0.01
         and all(abs(100 * f_ - t_) <= 0.55 for f_, t_ in zip(fgen, (2.9, 25.0, 55.0))),
         f"l_min (1e10 Msun, r = 10 kpc) = {k4['canonical']:.1f} / {k4['alt']:.1f} kpc (CL-AR 495 / 514); f_gen(l/r = 0.01, 0.1, 0.3) = "
         f"{100 * fgen[0]:.2f}%, {100 * fgen[1]:.2f}%, {100 * fgen[2]:.2f}% (CL-AR 2.9 / 25 / 55)")
RES["K4"] = dict(l_min_kpc=k4, f_gen=fgen)
# K5: CFG925 K7 link
ye = 0.05; a0k = A0["canonical"]
B_k5 = gauss_boost(nu_e, 1e-6 * ye * a0k, ye * a0k, a0k)
ysym = sp.Symbol("y", positive=True); nue_sym = 1 / (1 - sp.exp(-sp.sqrt(ysym)))
Le = sp.diff(sp.log(nue_sym), ysym) * ysym
B_an = float((nue_sym * (1 + Le / 3)).subs(ysym, ye))
K5 = chk("K5_CFG925_K7_exact_linear_QUMOND", abs(B_k5 - 4.249) < 1e-3 and abs(B_k5 - B_an) < 1e-4,
         f"Gauss-flux boost at y_e = 0.05 (nu_e, g_i = 1e-6 g_e) = {B_k5:.5f}; analytic nu_e(1 + L_e/3) = {B_an:.5f}; CFG925 K7 exact linear QUMOND 4.249")
# K6: O2c at c2 = 0 = CFG938 M3 / CFG941 R1
m938 = jload("CFG938_medium_continuum_eft", "cfg938_results_MUTATE.json")["MUTATE"]
k6 = {}
for foot in FOOTS:
    us, gt, _ = solve_static(Wc2, 1, GN_N, A0[foot], c2=0.0, key="Wc2")
    dv, nn = law_dev(gt, GN_N, A0[foot]); k6[foot] = dict(dev=dv, unsolved=nn, cfg938_M3=m938["M3"][foot]["max_rel_vs_law"])
K6 = chk("K6_O2c_c2_0_equals_CFG938_M3", all(abs(k6[f]["dev"] / k6[f]["cfg938_M3"] - 1) < 0.02 for f in FOOTS),
         f"O2c(c2 = 0) law dev canonical {k6['canonical']['dev']:.4f} (CFG938 M3 {k6['canonical']['cfg938_M3']:.4f}), "
         f"alt {k6['alt']['dev']:.4f} ({k6['alt']['cfg938_M3']:.4f})")
K_ALL = K1 and K2 and K3 and K4 and K5 and K6
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> VOID'}")
RES["K_all"] = K_ALL
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)

# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    m941 = jload("CFG941_self_gravity_repair", "cfg941_results_MUTATE.json")["MUTATE"]
    # M1: sector off -> dust + Newton
    m1 = {}
    for foot in FOOTS:
        a0 = A0[foot]
        dvN, _ = law_dev(GN_N.copy(), GN_N, a0)
        m1[foot] = dict(newton_dev=dvN, cfg938_M1=m938["M1"][foot]["max_rel_vs_law"],
                        btfr_y1e14=(1e-14 * a0) ** 2 / (1e-14 * a0 * a0))
    yb = sp.Symbol("y", positive=True)
    btfr_newton_lim = sp.limit(yb, yb, 0, "+")                         # V^4/(G M a0) = g_N^2 r^2/(G M a0) = y for Newton
    nM1 = n2(0, 0)
    efeM1 = max(abs(gauss_boost(lambda y: 1.0, plummer_g_at_a(Mb, apc), host_fields(rk, A0[f])[0], A0[f]) - 1.0)
                for f in FOOTS for _, Mb, apc in HOSTS882 for rk in RHOST)
    m1_bite = all(abs(m1[f]["newton_dev"] / m1[f]["cfg938_M1"] - 1) < 0.02 and m1[f]["newton_dev"] > 1e-6 for f in FOOTS) \
        and btfr_newton_lim == 0 and abs(nM1 - 1) < 1e-12 and efeM1 < 1e-9
    chk("M1_sector_off_is_dust_plus_Newton", m1_bite,
        f"X/tether off: NGC 3198 dev = {m1['canonical']['newton_dev']:.4f} / {m1['alt']['newton_dev']:.4f} (CFG938 M1 "
        f"{m1['canonical']['cfg938_M1']:.4f} / {m1['alt']['cfg938_M1']:.4f}); BTFR limit {btfr_newton_lim}; dust n = {nM1:.12f}; "
        f"max |EFE factor - 1| = {efeM1:.1e}")
    # M2: double counting breaks the law
    m2 = {}
    for foot in FOOTS:
        a0 = A0[foot]
        gl = np.array([law_g(x, a0) for x in GN_N]); uu = gl - GN_N
        dv_b, _ = law_dev(gl + uu, GN_N, a0)                                  # O2a-1/2 with class-A dust
        dv_u, _ = law_dev(np.array([law_g(x + y_, a0) for x, y_ in zip(GN_N, uu)]), GN_N, a0)   # O2a-3 with class-A dust
        _, gt2, _ = solve_static(Wfull, 2, GN_N, a0, key="m2")
        dv2, _ = law_dev(gt2, GN_N, a0)
        m2[foot] = dict(DA_baryon=dv_b, DA_universal=dv_u, DT_mult2=dv2, cfg941_M2a=m941["M2"][foot]["M2a_dev"])
    m2_bite = all(m2[f]["DA_baryon"] > 1e-6 and m2[f]["DA_universal"] > 1e-6 and abs(m2[f]["DT_mult2"] / m2[f]["cfg941_M2a"] - 1) < 0.02
                  for f in FOOTS)
    chk("M2_double_counting_breaks_law", m2_bite, "; ".join(
        f"{f}: D-A baryon-sourced {m2[f]['DA_baryon']:.3f}, D-A universal {m2[f]['DA_universal']:.3f}, multiplicity 2 {m2[f]['DT_mult2']:.3f} "
        f"(CFG941 M2a {m2[f]['cfg941_M2a']:.3f})" for f in FOOTS))
    # M3: linearized X (nu-tilde -> constant) restores superposition and kills the BTFR
    cX = 1.0
    efeM3 = max(abs(gauss_boost(lambda y: 1.0 + cX, plummer_g_at_a(Mb, apc), host_fields(rk, A0[f])[0], A0[f]) /
                    (1.0 + cX) - 1.0) for f in FOOTS for _, Mb, apc in HOSTS882 for rk in RHOST)
    btfr_lin = sp.limit((1 + cX) ** 2 * yb, yb, 0, "+")
    m3_bite = efeM3 < 1e-9 and btfr_lin != 1
    chk("M3_linear_X_no_EFE_no_BTFR", m3_bite, f"nu-tilde = {cX} constant: max |EFE factor - 1| = {efeM3:.1e}; deep BTFR limit = {btfr_lin} (not 1)")
    # M4: external field -> 0
    efeM4 = max(abs(gauss_boost(nu_s, plummer_g_at_a(Mb, apc), 1e-12 * plummer_g_at_a(Mb, apc), A0[f]) / nu_s(plummer_g_at_a(Mb, apc) / A0[f]) - 1)
                for f in FOOTS for _, Mb, apc in HOSTS882)
    m4_bite = efeM4 < 1e-9
    chk("M4_external_field_to_zero", m4_bite, f"g_e = 1e-12 g_s: max |EFE factor - 1| = {efeM4:.1e} (H1-H3, both footings)")
    RES["MUTATE"] = dict(M1=m1, M2=m2, M3=dict(efe=efeM3, btfr=str(btfr_lin)), M4=efeM4)
    allbite = m1_bite and m2_bite and m3_bite and m4_bite
    P(f"\n  MUTATE: {'ALL TEETH BITE (exit 1 by design)' if allbite else 'A TOOTH FAILED TO BITE'}")
    dump(); sys.exit(1 if allbite else 2)

# ================================================================================================ THEOREMS
P("\n==================== THEOREMS ====================")
# L-AR
x1 = sp.Symbol("x", real=True)
phi1, rb1, rd1 = [sp.Function(n_)(x1) for n_ in ("phi", "rho_b", "rho_d")]
sb, sd = sp.symbols("sigma_b sigma_d", real=True)
Wg = sp.Function("W")
LAR = -Wg(sp.diff(phi1, x1)) - (sb * rb1 + sd * rd1) * phi1
eAR = sp.euler_equations(LAR, [phi1], [x1])[0].lhs
src_d = sp.diff(eAR, rd1)                                               # coefficient of rho_d in the field equation
force_d = sp.diff(-(sd * rd1 * phi1), phi1) / rd1                      # dust force per unit density = -sigma_d dphi (coefficient)
LAR_ok = is0(src_d + sd) and is0(force_d + sd)
a0c = A0["canonical"]; rpair = 50 * KPC; Md_pair = 5.364 * MB_N
a_cm = Md_pair * uph(G_SI * MB_N / rpair ** 2, a0c) / (MB_N + Md_pair)
chk("L-AR_felt_by_equals_sourced_by", LAR_ok,
    "from L = -W(phi') - (sigma_b rho_b + sigma_d rho_d) phi: the field equation's rho_d source coefficient and the dust force coefficient are "
    "both sigma_d: a sector felt by dust is sourced by dust. O2a-1/O2b rule (felt by all, sourced by one species): baryon + dust pair "
    f"(NGC 3198 M_b, dust 5.364 M_b at 50 kpc) self-accelerates at a_cm = {a_cm:.3e} m/s^2 = {a_cm / a0c:.3f} a0 (canonical)")
RES["L_AR"] = dict(a_cm=a_cm, a_cm_over_a0=a_cm / a0c)
# L-G
xs3 = sp.symbols("x y z", real=True); mu_ = sp.Symbol("mu", positive=True)
Ac, Bc, Cc = sp.symbols("A_c B_c C_c", real=True)
phig = Ac * sp.log(1 + xs3[0] ** 2 + 2 * xs3[1] ** 2 + 3 * xs3[2] ** 2) + Bc * xs3[0] * xs3[1] * xs3[2] + Cc * sp.sin(xs3[0] + xs3[1])
phimu = mu_ ** 2 * phig.subs({xs3[0]: xs3[0] / mu_, xs3[1]: xs3[1] / mu_, xs3[2]: xs3[2] / mu_}, simultaneous=True)
hess_ok = all(is0(sp.diff(phimu, xs3[i], xs3[j]) - sp.diff(phig, xs3[i], xs3[j]).subs(
    {xs3[0]: xs3[0] / mu_, xs3[1]: xs3[1] / mu_, xs3[2]: xs3[2] / mu_}, simultaneous=True)) for i in range(3) for j in range(i, 3))
rr = sp.Symbol("r", positive=True); Aamp, Bamp = sp.symbols("A B", positive=True)
phir = Aamp * sp.log(rr) + Bamp / rr
amp = sp.limit(rr * sp.diff(phir, rr), rr, sp.oo)
amp_mu = sp.limit(rr * sp.diff(mu_ ** 2 * phir.subs(rr, rr / mu_), rr), rr, sp.oo)
Msym = sp.Symbol("M", positive=True)
deep_mu = sp.sqrt(G * mu_ ** 3 * Msym * a0s) / sp.sqrt(G * Msym * a0s)
mu_sol = sp.solve(sp.Eq(mu_ ** 2, mu_ ** sp.Rational(3, 2)), mu_)
share = sp.simplify(mu_ ** 2 / deep_mu)
# deep AQUAL and QUMOND are not invariant under phi -> phi + b z
bq = sp.Symbol("b", positive=True)
rad = sp.sqrt(xs3[0] ** 2 + xs3[1] ** 2 + xs3[2] ** 2)
grad = lambda f_: [sp.diff(f_, v) for v in xs3]
norm = lambda v: sp.sqrt(sum(c ** 2 for c in v))
div = lambda v: sum(sp.diff(v[i], xs3[i]) for i in range(3))
phi_pm = Aamp * sp.log(rad)
aq = lambda f_: div([norm(grad(f_)) * c for c in grad(f_)])
pt = {xs3[0]: sp.Rational(1), xs3[1]: sp.Rational(1, 2), xs3[2]: sp.Rational(3, 10), Aamp: 1, bq: sp.Rational(1, 3)}
aq0 = float(aq(phi_pm).subs(pt)); aqb = float(aq(phi_pm + bq * xs3[2]).subs(pt))
psi_pm = -Aamp / rad
nut_sym = lambda yy: (sp.sqrt(yy ** 2 + 4 * yy) - yy) / (2 * yy)
qm = lambda f_: div([nut_sym(norm(grad(f_))) * c for c in grad(f_)])
qm0 = float(qm(psi_pm).subs(pt)); qmb = float(qm(psi_pm + bq * xs3[2]).subs(pt))
# cubic Galileon: c1 x + c2 x^2 = q/r^3 -> A(r) = r^2 x has no plateau
c1g, c2g_, qg = sp.symbols("c1 c2 q", positive=True)
xg = (-c1g + sp.sqrt(c1g ** 2 + 4 * c2g_ * qg / rr ** 3)) / (2 * c2g_)
Ag = rr ** 2 * xg
gal_lims = (sp.limit(Ag, rr, 0, "+"), sp.limit(Ag, rr, sp.oo))
LG = chk("L-G_galilean_dilation_no_deep_law",
         hess_ok and amp == Aamp and is0(amp_mu - mu_ ** 2 * Aamp) and is0(deep_mu - mu_ ** sp.Rational(3, 2)) and mu_sol == [1]
         and abs(aq0) < 1e-12 and abs(aqb - aq0) > 1e-6 and abs(qmb - qm0) > 1e-6 and gal_lims == (0, 0),
         f"Hessian of mu^2 phi(x/mu) at x = Hessian of phi at x/mu (generic phi): {hess_ok}; amplitude A -> mu^2 A (sympy {sp.simplify(amp_mu)}), deep law "
         f"needs mu^(3/2) A; mu^2 = mu^(3/2) only at mu = {mu_sol}; X share of the deep amplitude ~ {share} -> 0 as mu -> 0. Not Galilean: deep AQUAL "
         f"div(|grad phi| grad phi) on A ln r = {aq0:.1e}, with + b z: {aqb:.3e}; QUMOND div(nu~ grad psi) on -A/r = {qm0:.1e}, with + b z: {qmb:.3e} (EFE). "
         f"Cubic Galileon r^2 x(r): limits r->0, r->inf = {gal_lims} (no flat regime)")
RES["L_G"] = dict(aqual_pm=aq0, aqual_pm_plus_bz=aqb, qumond_pm=qm0, qumond_pm_plus_bz=qmb, galileon_limits=str(gal_lims))
# D-T'
uu_ = sp.Symbol("uu", positive=True); mmul, mpri = sp.symbols("m mprime", positive=True)
h1, h2, h3, b2, b3, b4 = sp.symbols("h1 h2 h3 b2 b3 b4")
Uq = sp.Symbol("U", positive=True)
ggen = Uq + b2 * Uq ** 2 + b3 * Uq ** 3 + b4 * Uq ** 4                  # g as a series in the phantom field U
gNgen = ggen ** 2 / a0s * (1 + h1 * ggen / a0s + h2 * (ggen / a0s) ** 2 + h3 * (ggen / a0s) ** 3)
co = sp.Poly(sp.expand(ggen - gNgen - Uq), Uq).all_coeffs()[::-1]
solb = sp.solve([co[2], co[3], co[4]], [b2, b3, b4], dict=True)[0]
gN_of_U = sp.expand((ggen - Uq).subs(solb))                             # g_N(U) = U^2/a0 + O(U^3)
Fgen = sp.series(gN_of_U.subs(Uq, mmul * uu_) + mpri * uu_, uu_, 0, 3).removeO()
F_simple = Rrem.subs(u, mmul * uu_) + mpri * uu_                        # simple law: g_N = R(m u)
DTP = chk("D-T'_generalized", is0(sp.diff(Fgen, uu_).subs(uu_, 0) - mpri) and is0(sp.diff(F_simple, uu_).subs(uu_, 0) - mpri)
          and is0(sp.diff(gN_of_U, Uq).subs(Uq, 0)) and is0(sp.diff(gN_of_U, Uq, 2).subs(Uq, 0) - 2 / a0s),
          f"holding force F(u) = g_N(m u) + m' u: F'(0) = m' for any multiplicity m and any deep-limit law (h1, h2, h3 free); simple law "
          f"F = {sp.simplify(F_simple)}. The dust's linear self-gravity coefficient (m' - F'(0)) K rho vanishes wherever F acts")
# N-L
yy = sp.Symbol("y", positive=True); Cn = sp.Symbol("C", positive=True)
gXy = (sp.sqrt(yy ** 2 + 4 * yy) - yy) / 2
dlim = sp.limit(sp.diff(gXy, yy), yy, 0, "+")
tpos = sp.Symbol("t", positive=True)
xi2 = Cn ** 2 * tpos ** 4 / 144
ode_ok = is0(sp.diff(xi2, tpos, 2) - Cn * sp.sqrt(xi2))
NL = chk("N-L_no_linear_regime", dlim == sp.oo and ode_ok and sp.limit(xi2, tpos, 0) == 0 and sp.limit(sp.diff(xi2, tpos), tpos, 0) == 0,
         f"deep-law field g_X(y) = a0 (sqrt(y^2 + 4y) - y)/2: dg_X/dg_N -> {dlim} as g_N -> 0 (no Lipschitz linear response); "
         "xi'' = C sqrt(xi), xi(0) = xi'(0) = 0 has xi = 0 and xi = C^2 t^4/144 (non-unique Cauchy problem)")
THM = LAR_ok and LG and DTP and NL
RES["theorems_pass"] = THM
rss_guard("theorems")

TESTS = {}


def put(c, key, ok, detail):
    if isinstance(ok, (bool, np.bool_)):
        ok = bool(ok)                                                  # A1 item 6: numpy booleans are not `True`
    TESTS.setdefault(c, {})[key] = dict(pass_=ok, detail=str(detail))
    tag = {True: "PASS", False: "FAIL", None: "N/A "}.get(ok, str(ok))
    P(f"   [{c}] ({key}) {tag}: {detail}")


CONS = ("O2a-1", "O2a-2", "O2a-3", "O2a-G", "O2b", "O2c", "O2d1", "O2d2")

# ================================================================================================ (a) the law without double counting
P("\n==================== (a) THE LAW IN ROTATORS WITHOUT DOUBLE COUNTING ====================")
yS, Ms_, Md_ = sp.symbols("y M_s M_d", positive=True)
# r^2 g_N = G M  ->  r = sqrt(G M/(y a0));  V^4/(G M a0) = (g r)^2/(G M a0)
rS = sp.sqrt(G * Ms_ / (yS * a0s))
lawS = lambda gn_: (gn_ + sp.sqrt(gn_ ** 2 + 4 * gn_ * a0s)) / 2
bt = lambda gtot: sp.simplify((gtot * rS) ** 2 / (G * Ms_ * a0s))
lim_a12_fin = sp.limit(bt(lawS(yS * a0s) + G * Md_ / rS ** 2), yS, 0, "+")
lim_a12_DA = sp.limit(bt(2 * lawS(yS * a0s) - yS * a0s), yS, 0, "+")
lim_a3_fin = sp.limit(bt(lawS(yS * a0s * (1 + Md_ / Ms_))), yS, 0, "+")
P(f"  symbolic deep limits: X baryon-sourced + finite dust -> {lim_a12_fin}; X baryon-sourced + class-A dust -> {lim_a12_DA}; "
  f"X universal + finite dust -> {sp.simplify(lim_a3_fin)}")
aA = {}
for foot in FOOTS:
    a0 = A0[foot]
    gl = np.array([law_g(x, a0) for x in GN_N]); uu = gl - GN_N
    gd = dict(DA=uu.copy(),
              DF=G_SI * 5.364 * MB_N * np.minimum(R_N / RTA_N, 1.0) / R_N ** 2,
              DU=(4 * math.pi / 3) * G_SI * DTA * RHO_C0 * R_N)
    row = {}
    for dm, g_d in gd.items():
        g12 = gl + g_d
        g3 = np.array([law_g(x + y_, a0) for x, y_ in zip(GN_N, g_d)])
        row[dm] = dict(a12_dev=law_dev(g12, GN_N, a0)[0], a12_dex=dex_dev(g12, GN_N, a0),
                       a3_dev=law_dev(g3, GN_N, a0)[0], a3_dex=dex_dev(g3, GN_N, a0))
    gbt = G_SI * MB_N / RTA_N ** 2
    gdt = G_SI * 5.364 * MB_N / RTA_N ** 2
    row["btfr_rta"] = dict(a12_DFDU=(RTA_N * (law_g(gbt, a0) + gdt)) ** 2 / (G_SI * MB_N * a0),
                           a12_DA=(RTA_N * (2 * law_g(gbt, a0) - gbt)) ** 2 / (G_SI * MB_N * a0),
                           a3_DFDU=(RTA_N * law_g(gbt + gdt, a0)) ** 2 / (G_SI * MB_N * a0),
                           law=(RTA_N * law_g(gbt, a0)) ** 2 / (G_SI * MB_N * a0))
    aA[foot] = row
    P(f"  [{foot}] NGC 3198 deviation from the law, max over 43 radii (rel / dex):")
    for dm in ("DA", "DF", "DU"):
        v = row[dm]
        P(f"     dust {dm}: X baryon-sourced (O2a-1/2/G) {v['a12_dev']:.3e} / {v['a12_dex']:.4f} dex;  X universal (O2a-3/G) "
          f"{v['a3_dev']:.3e} / {v['a3_dex']:.4f} dex")
    b_ = row["btfr_rta"]
    P(f"     BTFR V^4/(G M_b a0) at r_ta = {RTA_N / KPC:.0f} kpc: bare law {b_['law']:.6f}; baryon-sourced + D-F/D-U dust {b_['a12_DFDU']:.4f}; "
      f"+ D-A {b_['a12_DA']:.4f}; universal + D-F/D-U {b_['a3_DFDU']:.4f}")
RES["a_O2a"] = aA
for c_, k_ in (("O2a-1", "a12"), ("O2a-2", "a12"), ("O2a-3", "a3"), ("O2a-G", "a12")):
    worst = max(aA[f][dm][k_ + "_dev"] for f in FOOTS for dm in ("DA", "DF", "DU"))
    least = min(aA[f]["DU"][k_ + "_dev"] for f in FOOTS)
    bkey = "a3_DFDU" if k_ == "a3" else "a12_DFDU"
    put(c_, "a", False, f"dust feels the galaxy and no rule keeps it out (dust equilibrium not selected): law dev for D-U (most diffuse) "
        f"{least:.2e} ... D-A {worst:.3f} (line 1e-6); BTFR at r_ta {aA['canonical']['btfr_rta'][bkey]:.4f} / {aA['alt']['btfr_rta'][bkey]:.4f}; "
        f"symbolic limit {'6.364 (universal: all catchment dust enters nu)' if k_ == 'a3' else '1 for finite dust, 4 for class-A dust'}")
# O2b
aB = {}
for foot in FOOTS:
    a0 = A0[foot]
    gl = np.array([law_g(x, a0) for x in GN_N]); uu = gl - GN_N
    gex = uu ** 2 / (uu + a0)                                          # slaved settled-dust field: nu(g_ex) g_ex = u
    chk_sl = float(np.max(np.abs(np.array([nu_s(x / a0) * x for x in gex]) / uu - 1)))
    g_eq2 = GN_N + np.array([nu_s(x / a0) * x for x in 0.5 * gex])
    gdF = G_SI * 5.364 * MB_N * np.minimum(R_N / RTA_N, 1.0) / R_N ** 2
    g_dF = GN_N + np.array([nu_s(x / a0) * x for x in gdF])
    aB[foot] = dict(slaved_check=chk_sl, Mex_over_Mph_last=float(gex[-1] / uu[-1]),
                    eq2_dev=law_dev(g_eq2, GN_N, a0)[0], DF_dev=law_dev(g_dF, GN_N, a0)[0])
    P(f"  [{foot}] O2b: slaved settled dust M_ex/M_ph at the last radius = {aB[foot]['Mex_over_Mph_last']:.4f} (slaving identity {chk_sl:.1e}); "
      f"a second equilibrium (dust x 0.5) dev {aB[foot]['eq2_dev']:.3f}; D-F dust dev {aB[foot]['DF_dev']:.3f}")
put("O2b", "a", False, f"the law needs the settled dust slaved to the baryons (g_ex = u^2/(u + a0): M_ex/M_ph = {aB['canonical']['Mex_over_Mph_last']:.3f} at "
    f"NGC 3198's last radius); nothing in O2b selects it: a second admissible equilibrium (dust x 0.5) deviates by {aB['canonical']['eq2_dev']:.3f} / "
    f"{aB['alt']['eq2_dev']:.3f}; fair-catchment dust by {aB['canonical']['DF_dev']:.3f} / {aB['alt']['DF_dev']:.3f}")
RES["a_O2b"] = aB
# O2c
c2max_nb = brentq(lambda c_: n2(c_, 0) - 0.999, 1e-8, 0.5, xtol=1e-12)
c2max = brentq(lambda c_: n2(c_, 1) - 0.999, 1e-8, 0.5, xtol=1e-12)
c2sym = sp.Symbol("c2", positive=True)
ufl = sp.solve(sp.Eq(Rrem.subs(u, uu_), (1 - c2sym) * uu_), uu_)
ufl = [s_ for s_ in ufl if s_ != 0]
def btc(c2v):
    """V^4/(G M a0) = g^2/(g_N a0) along O2c's static branch g_N = R(u) - (1 - c2) u, g = g_N + u, as g_N -> 0+."""
    gNu = Rrem.subs(u, uu_) - (1 - c2v) * uu_
    expr = (gNu + uu_) ** 2 / (gNu * a0s)
    if c2v >= 1:
        return sp.limit(expr, uu_, 0, "+")
    uf = a0s * (1 - c2v) / (2 - c2v)
    return sp.limit(expr, uu_, uf, "+")
lims_c = {str(cv): btc(cv) for cv in (sp.Rational(0), sp.Rational(1, 2), sp.Rational(1), sp.Rational(2))}
aC = {}
for foot in FOOTS:
    a0 = A0[foot]
    us, gt, _ = solve_static(Wc2, 1, GN_N, a0, c2=c2max, key="Wc2")
    dv, nn = law_dev(gt, GN_N, a0)
    aC[foot] = dict(dev=dv, unsolved=nn, floor_over_a0=(1 - c2max) / (2 - c2max), btfr_y1e14=btfr_numeric(Wc2, a0, c2=c2max))
P(f"  O2c: growth needs c2 <= {c2max:.4e} (full action; {c2max_nb:.4e} without the chi-bar term; CFG941 2.3458e-3); static law becomes "
  f"g_N = R(u) - (1 - c2) u, floor u_f = {ufl}; deep BTFR limits {lims_c}")
put("O2c", "a", False, f"at c2 = {c2max:.3e} (the largest growth allows): law dev {aC['canonical']['dev']:.3f} / {aC['alt']['dev']:.3f}, acceleration floor "
    f"{aC['canonical']['floor_over_a0']:.4f} a0, V^4/(GMa0) at y = 1e-14: {aC['canonical']['btfr_y1e14']:.3e}; only c2 = 1 gives the BTFR "
    f"(limits {lims_c}) and c2 = 1 is CFG941's cancellation")
RES["a_O2c"] = dict(rows=aC, c2max=c2max, c2max_noboost=c2max_nb, floor=str(ufl), btfr_limits={k: str(v) for k, v in lims_c.items()})
# O2d1: cubic Galileon best fit to the phantom field (illustration of L-G)
aD1 = {}
for foot in FOOTS:
    a0 = A0[foot]
    uu = np.array([law_g(x, a0) for x in GN_N]) - GN_N

    xref = GN_N[-1] / R_N[-1]

    def gal_force(p):                                                 # c1 x + c2 x^2 = G M(<r)/r^3, x = pi'/r; c2 = exp(p1)/xref
        c1, c2h = math.exp(p[0]), math.exp(p[1])
        qh = (GN_N / R_N) / xref
        xh = 2 * qh / (c1 + np.sqrt(c1 * c1 + 4 * c2h * qh))           # stable root
        return R_N * xh * xref
    obj = lambda p: float(np.sum(np.log((GN_N + gal_force(p)) / (GN_N + uu)) ** 2))
    best = None
    for l1 in np.linspace(-6, 4, 11):
        for l2 in np.linspace(-15, 15, 16):
            o = minimize(obj, [l1, l2], method="Nelder-Mead", options=dict(xatol=1e-10, fatol=1e-14, maxiter=4000))
            if best is None or o.fun < best.fun:
                best = o
    gfit = GN_N + gal_force(best.x)
    aD1[foot] = dict(dev=law_dev(gfit, GN_N, a0)[0], dex=dex_dev(gfit, GN_N, a0), c1=math.exp(best.x[0]))
    rss_guard("O2d1 fit")
put("O2d1", "a", False, f"L-G: a Galilean-symmetric sector's deep amplitude scales as mu^2, the law's as mu^(3/2): no member gives the deep BTFR "
    f"(cubic Galileon: r^2 x -> 0 at both ends; BTFR limit 0). Best two-parameter cubic-Galileon fit to NGC 3198: max dev "
    f"{aD1['canonical']['dev']:.3f} / {aD1['alt']['dev']:.3f} ({aD1['canonical']['dex']:.3f} dex)")
RES["a_O2d1"] = aD1
# O2d2
aD2 = {}
for foot in FOOTS:
    a0 = A0[foot]
    uu = np.array([law_g(x, a0) for x in GN_N]) - GN_N
    eq2 = law_dev(GN_N + 0.5 * uu, GN_N, a0)[0]
    Mph = R_N[-1] ** 2 * uu[-1] / G_SI
    lmin = (R_N[-1] ** 3 + 3 * Mph / (4 * math.pi * RHO_C0)) ** (1 / 3) - R_N[-1]
    aD2[foot] = dict(eq2_dev=eq2, Mph_over_Mb=Mph / MB_N, l_min_kpc=lmin / KPC, l_over_R=lmin / R_N[-1])
Vf_ = sp.Symbol("V_f", positive=True); sig2 = sp.Symbol("sigma2", positive=True)
rho_deep = sp.sqrt(G * Msym * a0s) / (4 * sp.pi * G * rr ** 2)
iso = sp.solve(sp.Eq(sig2 / (2 * sp.pi * G * rr ** 2), rho_deep), sig2)[0]
iso_ok = is0(iso - sp.sqrt(G * Msym * a0s) / 2)
put("O2d2", "a", False, f"dust = phantom gives the law exactly, but dust + gravity do not select it: a second Jeans equilibrium (dust x 0.5) deviates by "
    f"{aD2['canonical']['eq2_dev']:.3f} / {aD2['alt']['eq2_dev']:.3f}; assembling NGC 3198's phantom ({aD2['canonical']['Mph_over_Mb']:.2f} M_b inside "
    f"{R_N[-1] / KPC:.1f} kpc) from cosmic-mean dust needs l_min = {aD2['canonical']['l_min_kpc']:.0f} kpc = {aD2['canonical']['l_over_R']:.1f} R "
    f"(CL-AR budget: a local response generates <= 3l/r); isothermal identity sigma^2 = V_f^2/2: {iso_ok}")
RES["a_O2d2"] = aD2
rss_guard("(a)")

# ================================================================================================ (b) growth
P("\n==================== (b) a^1 GROWTH ====================")
eps_max = brentq(lambda e: n_eps(e) - 1.001, 0.0, 0.1, xtol=1e-14)
Rk = 1.0 / (0.01 * HLIT / (1e3 * KPC))
bB = {}
for foot in FOOTS:
    a0 = A0[foot]
    ymax = (4 * math.pi / 3) * G_SI * RHO_M0 * Rk / a0
    e1 = lambda y: nut_s(FB * y) * FB
    e3 = lambda y: nut_s(y)
    eb = lambda y: nut_s(FC * y) * FC

    def lam2(y):
        nt = nut_s(FB * y)
        Mx = np.array([[FB * (1 + nt), FC], [FB, FC]])
        return float(max(np.linalg.eigvals(Mx).real))
    ymin1 = brentq(lambda y: e1(y) - eps_max, 1e-6, 1e12)
    ymin3 = brentq(lambda y: e3(y) - eps_max, 1e-6, 1e12)
    yminb = brentq(lambda y: eb(y) - eps_max, 1e-6, 1e12)
    ymin2 = brentq(lambda y: n_lam(lam2(y)) - 1.001, 1e-6, 1e12)
    bB[foot] = dict(y_max=ymax, O2a1=dict(eps=e1(ymax), n=n_eps(e1(ymax)), y_min=ymin1), O2a3=dict(eps=e3(ymax), n=n_eps(e3(ymax)), y_min=ymin3),
                    O2b=dict(eps=eb(ymax), n=n_eps(eb(ymax)), y_min=yminb), O2a2=dict(lam=lam2(ymax), n=n_lam(lam2(ymax)), y_min=ymin2))
    P(f"  [{foot}] eps_max (|n - 1| = 1e-3) = {eps_max:.4e}; largest linear-regime field at z = 0 (delta = 1, R = 1/k, k = 0.01 h/Mpc): "
      f"y_max = {ymax:.4f}")
    for k_ in ("O2a1", "O2a2", "O2a3", "O2b"):
        v = bB[foot][k_]
        P(f"     {k_}: at y_max {'eps' if 'eps' in v else 'lambda'} = {v.get('eps', v.get('lam')):.4f}, n = {v['n']:.4f}; requires y >= {v['y_min']:.3e}")
for c_, k_ in (("O2a-1", "O2a1"), ("O2a-2", "O2a2"), ("O2a-3", "O2a3"), ("O2b", "O2b")):
    put(c_, "b", all(abs(bB[f][k_]["n"] - 1) < 1e-3 for f in FOOTS),
        f"X acts on linear modes: n = {bB['canonical'][k_]['n']:.3f} / {bB['alt'][k_]['n']:.3f} at the largest linear field (y_max = "
        f"{bB['canonical']['y_max']:.3f}); a^1 needs y >= {bB['canonical'][k_]['y_min']:.2e}, i.e. never in the linear regime")
put("O2a-G", "b", abs(n_dust - 1) < 1e-12, f"gate off for the cosmic mean (theta = 3H >= 3H0 > theta_s = H0): pure dust, n = {n_dust:.12f}")
nC = n2(c2max, 1)
put("O2c", "b", abs(nC - 1) < 1e-3 + 1e-12, f"n(c2) from the full action: |n - 1| < 1e-3 iff c2 <= {c2max:.4e} (n = {nC:.6f} there), where (a) fails; c2 = 1 "
    f"(the only BTFR value) gives n = {n_full:.4f}. No c2 passes (a) and (b) together")
c1_min = 1.0 / eps_max
put("O2d1", "b", True, f"linear fifth force of fixed strength 1/c1 (Galileon): a^1 within 1e-3 iff c1 >= {c1_min:.0f} (free); its best (a) fit needs c1 = "
    f"{aD1['canonical']['c1']:.3g} / {aD1['alt']['c1']:.3g}, where n = {n_eps(1 / aD1['canonical']['c1']):.3f} / {n_eps(1 / aD1['alt']['c1']):.3f} (A1 item 7)")
put("O2d2", "b", True, f"dust, no tether, no sector acting on linear modes: n = {n_dust:.12f}")
RES["b"] = dict(eps_max=eps_max, rows=bB, c2max=c2max, n_at_c2max=nC)
rss_guard("(b)")

# ================================================================================================ (c) satellites, EFE, CL-AR
P("\n==================== (c) SATELLITES (CFG882 H1-H3 in a 6e10 Msun host) AND CL-AR ====================")
cC = {}
for foot in FOOTS:
    a0 = A0[foot]
    for hn, Mb, apc in HOSTS882:
        gs = plummer_g_at_a(Mb, apc)
        iso_b = gauss_boost(nu_s, gs, 0.0, a0)
        us_ = uph(gs, a0); gexs = us_ ** 2 / (us_ + a0)
        for rk in RHOST:
            gbh, gdh = host_fields(rk, a0)
            f12 = gauss_boost(nu_s, gs, gbh, a0) / iso_b
            f3 = gauss_boost(nu_s, gs, gbh + gdh, a0) / iso_b
            uh = uph(gbh, a0); gexh = uh ** 2 / (uh + a0)
            fb_ = (gs + gexs * gauss_boost(nu_s, gexs, gexh, a0)) / (gs + gexs * nu_s(gexs / a0))
            cC[f"{foot}|{hn}|{rk:g}"] = dict(gs_over_a0=gs / a0, gbh_over_a0=gbh / a0, gdh_over_gbh=gdh / gbh, O2a12_dex=math.log10(f12),
                                            O2a3_dex=math.log10(f3), O2b_dex=math.log10(fb_))
P(f"  {'case':22s} {'g_s/a0':>8s} {'g_bh/a0':>8s} {'g_dh/g_bh':>9s} {'O2a-1/2 dex':>11s} {'O2a-3 dex':>10s} {'O2b dex':>9s}")
for k_, v in cC.items():
    P(f"  {k_:22s} {v['gs_over_a0']:8.4f} {v['gbh_over_a0']:8.4f} {v['gdh_over_gbh']:9.3f} {v['O2a12_dex']:11.4f} {v['O2a3_dex']:10.4f} {v['O2b_dex']:9.4f}")
r925 = jload("CFG925_small_reframings_A", "cfg925_results.json")["R3"]
rec = {}
for foot in FOOTS:
    cr = r925[foot]["corners"]
    rec[foot] = {k_: dict(sat_mean_shift_dex=cr[k_].get("sat_mean_shift_dex"), sat_mean_E_dex=cr[k_].get("sat_mean_E_dex"),
                          c=cr[k_]["cfg874"]["c"], se_c=cr[k_]["cfg874"]["se_c"], z=cr[k_]["cfg874"]["c"] / cr[k_]["cfg874"]["se_c"])
                 for k_ in ("E0|nom", "E1|nom", "E2|nom")}
    P(f"  [{foot}] record satellites (CFG925 R3, read only): EFE-free excess {rec[foot]['E0|nom']['sat_mean_E_dex']:+.3f} dex; mean EFE shift "
      f"E1 {rec[foot]['E1|nom']['sat_mean_shift_dex']:+.3f} / E2 {rec[foot]['E2|nom']['sat_mean_shift_dex']:+.3f} dex; CFG874 c (isolated - satellites) "
      + ", ".join(f"{k_.split('|')[0]} {v['c']:+.3f} +/- {v['se_c']:.3f} (z {v['z']:+.2f})" for k_, v in rec[foot].items()))
RES["c"] = dict(rows=cC, record=rec)
w12 = [v["O2a12_dex"] for v in cC.values()]; w3 = [v["O2a3_dex"] for v in cC.values()]; wb = [v["O2b_dex"] for v in cC.values()]
tens = f"record: E1/E2 lower the satellites by {rec['canonical']['E1|nom']['sat_mean_shift_dex']:+.2f}/{rec['canonical']['E2|nom']['sat_mean_shift_dex']:+.2f} dex; " \
       f"satellites would need {-rec['canonical']['E1|nom']['c']:.2f}-{-rec['canonical']['E2|nom']['c']:.2f} dex more bound cold mass than isolated dwarfs " \
       f"(z {-rec['canonical']['E1|nom']['z']:.1f}-{-rec['canonical']['E2|nom']['z']:.1f}, against tidal stripping)"
for c_ in ("O2a-1", "O2a-2", "O2a-G"):
    put(c_, "c", False, f"(c-i) no superposition (L-G); (c-ii) H1-H3 factors {min(w12):+.3f} ... {max(w12):+.3f} dex (host baryonic field); {tens}")
put("O2a-3", "c", False, f"(c-i) no superposition; host baryons + host dust enter nu: {min(w3):+.3f} ... {max(w3):+.3f} dex (larger than O2a-1/2); {tens}")
put("O2b", "c", False, f"(c-i) no superposition; host settled-dust field enters nu: {min(wb):+.3f} ... {max(wb):+.3f} dex")
put("O2c", "c", False, "(c-i) the tether reads the total dust field (no superposition); hover lemma: a dust element at rest in the host's settled field feels "
    "F(u_h) - g_bh - u_h = 0 (equilibrium) for any c2, while stars feel g_host: Delta a/g_host = 1 (CFG941 R1 1.0000)")
put("O2d1", "c", True, "(c-i) Galilean symmetry: a uniform external gradient drops out exactly (factor 1); passes by construction")
put("O2d2", "c", True, "(c-i) dust is real, universally coupled mass: CL-AR Theorem 1 (K3) gives no internal response at uniform order (factor 1; tides only)")
rss_guard("(c)")

# ================================================================================================ (d) well-posedness
P("\n==================== (d) WELL-POSEDNESS ====================")
S5p = lambda x: 30 * x ** 4 - 60 * x ** 3 + 30 * x ** 2
S5pp = lambda x: 120 * x ** 3 - 180 * x ** 2 + 60 * x
xs_ = np.linspace(0, 1, 200001); spp_max = float((-S5pp(xs_)[xs_ > 0.5]).max())
ghost = {}
for zt in (0.0, 1.0, 3.0):
    Krho0 = DTA * 1.5 * OM0 * H0_SI ** 2 * (1 + zt) ** 3
    rho0 = Krho0 / K_SI
    for Rmpc in (0.1, 1.0, 10.0):
        Rm = Rmpc * 1e3 * KPC
        for lab, frac in (("baryon-sourced", FB), ("universal", 1.0)):
            g0 = frac * Krho0 * (Rm / 2) / 3; u0 = uph(g0, A0["canonical"])
            W0 = Wrem_num(u0, A0["canonical"])
            kg = math.sqrt(rho0 / ((spp_max / H0_SI ** 2) * W0))
            ghost[f"z_ta={zt:g}|R={Rmpc:g}Mpc|{lab}"] = dict(k_g_R=kg * Rm, k_g_Lstar24=kg * 24 * PC, u0_over_a0=u0 / A0["canonical"])
kgR = [v["k_g_R"] for v in ghost.values()]; kgL = [v["k_g_Lstar24"] for v in ghost.values()]
P(f"  O2a-G gate kinetic term -(1/2) s''(theta) W_X (div v)^2, W_X = W_rem(u0): ghost band k > k_g, k_g R = {min(kgR):.3g} ... {max(kgR):.3g}, "
  f"k_g L*(24 pc) = {min(kgL):.3g} ... {max(kgL):.3g}")


def disp_c2(c2v, u0s, a0=1.0):
    ks = np.logspace(-2, 5, 300); ths = np.linspace(0, math.pi / 2, 41); out = {}
    for u0 in u0s:
        KK, TT = np.meshgrid(ks, ths)
        w2 = (c2v + Rp_num(u0, a0)) * np.cos(TT) ** 2 + (c2v + u0 / (a0 - u0)) * np.sin(TT) ** 2 - 1.0 + 0.5 * KK ** 2
        out[u0] = float(w2.min())
    return out


dC = disp_c2(c2max, (0.5, 0.9, 0.99))
for c_ in ("O2a-1",):
    put(c_, "d", False, f"(d0) FAIL: felt by all, sourced by baryons: no action (L-AR), pair self-acceleration {a_cm / a0c:.3f} a0; (d1) FAIL: "
        "deep-law response at zero field is not Lipschitz (N-L); (d2) static QUMOND = two Poisson solves (pass)")
put("O2a-2", "d", False, "(d0) pass (baryons source and feel X); (d1) FAIL: baryon perturbations respond as sqrt(a0 g_N) about FRW (N-L); (d2) pass")
put("O2a-3", "d", False, "(d0) pass; (d1) FAIL (N-L, total-matter source); (d2) pass")
put("O2a-G", "d", False, f"(d0) as O2a-1/3; (d1) the gate removes X at linear order but its kinetic term is a ghost band for k > k_g, k_g R = {min(kgR):.2g} ... "
    f"{max(kgR):.2g} (CFG941 R3theta mechanism with W_X = W_rem)")
put("O2b", "d", False, "(d0) FAIL: sourced by dust, felt by baryons (L-AR); (d1) FAIL: N-L in the dust's field unless gated; (d2) pass")
put("O2c", "d", min(dC.values()) >= -1.0 - 1e-12, f"(d0) pass (CFG938 action); (d1) min omega^2/(K rho0) about O2c static states (u0/a0 = 0.5/0.9/0.99) = "
    f"{', '.join(f'{v:.3f}' for v in dC.values())}: bounded Jeans-type (as CFG941 R1); (d2) pass")
put("O2d1", "d", True, "(d0) pass (action); (d1) second-order Galilean equations, free scalar about FRW (not tested beyond linear order); (d2) pass")
put("O2d2", "d", True, "(d0) pass (dust + gravity); (d1) Vlasov/Euler-Poisson: bounded Jeans growth; (d2) pass")
RES["d"] = dict(ghost=ghost, disp_O2c=dC, spp_max=spp_max)

# ================================================================================================ (e) slip
P("\n==================== (e) SLIP ON CFG847's FIVE SYSTEMS ====================")
eE = {}
for foot in FOOTS:
    a0 = A0[foot]
    for name, Mb, rk_ in SYS847:
        M = Mb * MSUN847; rr_ = rk_ * KPC847
        gn = G_SI * M / rr_ ** 2; g_ = law_g(gn, a0); uu = g_ - gn; vc2 = g_ * rr_
        s_conf = uu / g_
        pr = R_num(uu, a0) * uu / K_SI - Wrem_num(uu, a0); ptt = -Wrem_num(uu, a0)
        s_best_g = 4 * math.pi * G_SI * rr_ * abs(pr) / (C_SI ** 2 * g_)
        s_best_8 = 8 * math.pi * G_SI * rr_ ** 2 * max(abs(pr), abs(ptt)) / (C_SI ** 2 * vc2)
        # O2c static state at c2max
        c2v = c2max; bq_ = gn - (1 - c2v) * a0
        uc = (-bq_ + math.sqrt(bq_ * bq_ + 4 * (2 - c2v) * gn * a0)) / (2 * (2 - c2v)); gc = gn + uc
        Wc = Wrem_num(uc, a0) + c2v * uc * uc / (2 * K_SI); Dc = R_num(uc, a0) + c2v * uc
        prc = -Wc; ptc = -Wc + Dc * uc / K_SI
        s_c_g = 4 * math.pi * G_SI * rr_ * abs(prc) / (C_SI ** 2 * gc)
        s_c_8 = 8 * math.pi * G_SI * rr_ ** 2 * max(abs(prc), abs(ptc)) / (C_SI ** 2 * gc * rr_)
        # O2d2: dispersion-supported phantom, p(r) = int_r^inf rho_ph g dr

        def rho_g(s_):
            x = math.exp(s_); gnx = G_SI * M / x ** 2; ux = uph(gnx, a0)
            dudg = 0.5 * (-1 + (gnx + 2 * a0) / math.sqrt(gnx * gnx + 4 * gnx * a0))
            dr2u = 2 * x * ux + x * x * dudg * (-2 * gnx / x)
            return dr2u / (K_SI * x * x) * law_g(gnx, a0) * x
        pdisp, _ = quad(rho_g, math.log(rr_), math.log(rr_) + 25, limit=400, epsrel=1e-10)
        s_d_g = 4 * math.pi * G_SI * rr_ * pdisp / (C_SI ** 2 * g_)
        s_d_8 = 8 * math.pi * G_SI * rr_ ** 2 * pdisp / (C_SI ** 2 * vc2)
        eE[f"{foot}|{name}"] = dict(conformal=s_conf, best_grad=s_best_g, best_847=s_best_8, O2c_grad=s_c_g, O2c_847=s_c_8, O2d2_grad=s_d_g, O2d2_847=s_d_8)
P(f"  {'system':18s} {'light-blind X':>13s} {'best X s_847':>12s} {'O2c s_847':>10s} {'O2d2 s_grad':>11s} {'O2d2 s_847':>10s}")
for k_, v in eE.items():
    P(f"  {k_:18s} {v['conformal']:13.4f} {v['best_847']:12.3e} {v['O2c_847']:10.3e} {v['O2d2_grad']:11.3e} {v['O2d2_847']:10.3e}")
mx = lambda key: max(v[key] for v in eE.values())
for c_ in ("O2a-1", "O2a-2", "O2a-3", "O2a-G", "O2b", "O2d1"):
    put(c_, "e", False, f"minimal (conformal) light coupling: light misses X, s = u/g up to {mx('conformal'):.3f} (line 1.9e-5); best case (X in both potentials, "
        f"needs an extra disformal/vector sector): worst s_847 {mx('best_847'):.2e}, s_grad {mx('best_grad'):.2e}")
put("O2c", "e", max(mx("O2c_847"), mx("O2c_grad")) <= 1.9e-5, f"on O2c's own static states (c2 = {c2max:.2e}): worst s_847 {mx('O2c_847'):.2e}, "
    f"s_grad {mx('O2c_grad'):.2e} (line 1.9e-5; CFG941 R1 3.28e-5)")
put("O2d2", "e", max(mx("O2d2_847"), mx("O2d2_grad")) <= 1.9e-5, f"dispersion pressure of the phantom-shaped dust: worst s_847 {mx('O2d2_847'):.2e}, "
    f"s_grad {mx('O2d2_grad'):.2e} (line 1.9e-5)")
RES["e"] = eE

# ================================================================================================ (f) class-A limit
P("\n==================== (f) CLASS-A LIMIT (COSMIC SHEAR TRANSFER) ====================")
zs = {}
for foot in FOOTS:
    a0 = A0[foot]; gbt = G_SI * MB_N / RTA_N ** 2
    zs[foot] = (RTA_N ** 2 * uph(gbt, a0) / G_SI) / (6.364 * MB_N)
P(f"  field-supplied phantom inside NGC 3198's r_ta / catchment total mass (6.364 M_b) = {zs['canonical']:.2f} / {zs['alt']:.2f} (class A: zero-sum, 0)")
for c_ in ("O2a-1", "O2a-3", "O2a-G", "O2b"):
    put(c_, "f", False, f"g1 no (dust feels X, not only Newton); g2 no (the X phantom is a net source: {zs['canonical']:.1f} x the catchment mass inside r_ta; "
        "it reads the total field: EFE); g3 no (X on linear modes) [O2a-G: g3 yes]")
put("O2a-2", "f", False, f"g1 yes (dust feels Newton only); g2 no (lensing sees baryons + dust, the phantom is a baryon-only fifth force; net source {zs['canonical']:.1f} x); "
    "g3 no (baryons feel X)")
put("O2c", "f", False, "g1 no (the tether R(u) acts in settled regions); g2 no (equilibrium reads the total dust field); g3 yes only for c2 -> 0 (CFG941 R1)")
put("O2d1", "f", False, "g1 no (Galileon fifth force on dust); g2 no; g3 only for weak coupling")
put("O2d2", "f", False, "g1 yes, g3 yes; g2 only with a selection rule that the local construction lacks: with the catchment rule added it IS class A "
    "(option 3, CFG947), not a local option-2 construction")
RES["f"] = dict(net_source_over_catchment=zs)

# ================================================================================================ (g) excess family and below-law systems
P("\n==================== (g) EXCESS FAMILY AND BELOW-LAW SYSTEMS ====================")
r925f = jload("CFG925_small_reframings_A", "cfg925_results.json")
gE = {}
for foot in FOOTS:
    ob = r925f["observed_dex"][foot]; se = r925f["observed_se_dex"][foot]
    gE[foot] = {k_: dict(dex=ob[k_], f=10 ** ob[k_] - 1, f_lo=10 ** (ob[k_] - se[k_]) - 1, f_hi=10 ** (ob[k_] + se[k_]) - 1) for k_ in ("F0", "F1", "F5", "F2", "F3", "F4")}
    P(f"  [{foot}] dust fraction each fact needs (Newtonian addition, f = 10^D - 1): " +
      ", ".join(f"{k_} {v['dex']:+.3f} dex -> {v['f']:.3f} [{v['f_lo']:.3f}, {v['f_hi']:.3f}]" for k_, v in gE[foot].items()))
r936 = jload("CFG936_below_law_systems", "cfg936_results.json")["routes"]
gB = {}
for foot in FOOTS:
    rr9 = r936[foot]
    gB[foot] = {k_: {c_: dict(rbar=rr9[k_][c_]["stats"]["rbar"], se=rr9[k_][c_]["stats"]["se"], z=rr9[k_][c_]["stats"]["z_mean"],
                             cls=rr9[k_][c_].get("cls")) for c_ in ("T", "U")} for k_ in ("law", "route_i", "route_iii_EFE_contrast")}
    P(f"  [{foot}] CFG936 (read only): bare law T {gB[foot]['law']['T']['rbar']:+.3f} +/- {gB[foot]['law']['T']['se']:.3f}; field law + EFE (route iii) T "
      f"{gB[foot]['route_iii_EFE_contrast']['T']['rbar']:+.3f} +/- {gB[foot]['route_iii_EFE_contrast']['T']['se']:.3f} (z {gB[foot]['route_iii_EFE_contrast']['T']['z']:+.2f}, "
      f"{gB[foot]['route_iii_EFE_contrast']['T']['cls']}), U {gB[foot]['route_iii_EFE_contrast']['U']['cls']}; zero supply (route i) T "
      f"{gB[foot]['route_i']['T']['rbar']:+.3f} +/- {gB[foot]['route_i']['T']['se']:.3f} ({gB[foot]['route_i']['T']['cls']})")
hd = [cC[f"canonical|H1|{rk:g}"]["gdh_over_gbh"] for rk in RHOST]
ex_txt = f"RE-DESCRIBES: dust fractions from {gE['canonical']['F4']['f']:.3f} (SPARC large) to {gE['canonical']['F0']['f']:.2f} (dwarfs) with no derived selector"
for c_ in ("O2a-1", "O2a-2", "O2a-G"):
    put(c_, "g", "FAILS", f"{ex_txt}; below-law: the field acts on every baryonic system, TDGs at route (iii) {gB['canonical']['route_iii_EFE_contrast']['T']['rbar']:+.3f} "
        f"+/- {gB['canonical']['route_iii_EFE_contrast']['T']['se']:.3f} (z {gB['canonical']['route_iii_EFE_contrast']['T']['z']:+.2f}) / alt z "
        f"{gB['alt']['route_iii_EFE_contrast']['T']['z']:+.2f}; DF4 below Newton is unreachable")
put("O2a-3", "g", "FAILS", f"{ex_txt}; below-law: as O2a-1/2, host dust raises g_e only x{1 + min(hd):.2f}-{1 + max(hd):.2f} at 50-250 kpc (TDGs need x29-36)")
for c_ in ("O2b", "O2c", "O2d2"):
    put(c_, "g", "RE-DESCRIBES", f"{ex_txt}; below-law: zero dust -> Newton, route (i) {gB['canonical']['route_i']['T']['cls']} (label not derived, as CFG936)")
put("O2d1", "g", "NOT COMPUTED", "fails (a) structurally; no zero-supply escape for a baryon-sourced field")
RES["g"] = dict(fractions=gE, below_law=gB, host_dust_factor=hd)

# ================================================================================================ CLASSES
P("\n==================== CLASSES (frozen rules, criteria sec. 5) ====================")
CLASSES = {}
for c_ in CONS:
    t = TESTS[c_]
    fails_ae = [k for k in "abcde" if t[k]["pass_"] is not True]
    f_ok = t["f"]["pass_"] is True
    if not fails_ae and f_ok:
        cl = "VIABLE"
    elif not fails_ae:
        cl = "VIABLE-WITH-COST"
    else:
        cl = "NOT VIABLE"
    CLASSES[c_] = dict(cls=cl, fails=[k for k in "abcdef" if t[k]["pass_"] is not True], g=t["g"]["pass_"])
    P(f"  {c_:6s} {cl:17s} fails: {','.join(CLASSES[c_]['fails']) or '-'};  (g) {t['g']['pass_']}")
if any(v["cls"] == "VIABLE" for v in CLASSES.values()):
    OVERALL = "OPTION 2 WORKS"
elif any(v["cls"] == "VIABLE-WITH-COST" for v in CLASSES.values()):
    OVERALL = "CONDITIONAL"
else:
    OVERALL = "NO-GO (theorem T-O2)" if THM else "NO-GO (case by case, no proof)"
P(f"\n  OVERALL: {OVERALL}")
P("  T-O2: L-AR, L-G, D-T', N-L " + ("all pass" if THM else "do NOT all pass") + ": under A1-A4 the deep extra force must be dust mass (L-G), i.e. cold energy IS the "
  "phantom in the deep regime, contradicting option 2; static selection then needs supported dust, whose holding force cancels its self-gravity (D-T').")
RES["tests"] = TESTS; RES["classes"] = CLASSES; RES["overall"] = OVERALL
allchk = all(v["pass"] for v in RES["checks"].values())
P(f"\n  all checks pass: {allchk}; runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
dump()
sys.exit(0 if (allchk and K_ALL) else 1)

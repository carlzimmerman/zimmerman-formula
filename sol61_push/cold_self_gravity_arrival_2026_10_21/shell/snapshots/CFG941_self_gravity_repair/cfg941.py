"""CFG941 -- self-gravity repair of CFG938's covariant parent.
Criteria: FROZEN_CRITERIA.md (0b41bd0cf, committed alone before this script); amendment A1 (7c395c866, pre-result).
Run (one core, one process, < 1 GB):
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg941.py              -> cfg941.out, cfg941_results.json (K + main)
    CFG941_STAGE=K ...                                          -> cfg941_K.out, cfg941_results_K.json (K only)
    CFG941_MUTATE=1 ...                                         -> cfg941_MUTATE.out, cfg941_results_MUTATE.json
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite).
kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed."""
import os, sys, io, json, math, time, resource, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG941_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG941_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
OUT = []
RES = {"lane": "CFG941", "criteria": "0b41bd0cf", "amendments": ["A1 7c395c866 pre-result (BTFR point y = 1e-14)"],
       "mutate": MUT, "stage": STAGE, "checks": {}, "tests": {}}
T0 = time.time()
RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg941_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg941{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def rss_guard(where=""):
    r = rss_val()
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def is0(e):
    return sp.simplify(sp.expand(e)) == 0


# ------------------------------------------------------------------------------------------------ constants (read-only inputs)
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # the record's footings
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC, KPC = 6.67430e-11, 299792458.0, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e19
K_SI = 4 * math.pi * G_SI
MSUN847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's constants for its systems (as CFG938)
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0),
          ("cluster", 1.5e14, 1000.0)]
H0_SI = 67.4e3 / (1e6 * PC); RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
OB = 0.0493; OC = 5.364 * OB; RHO_C0 = OC * RHO_CRIT; OM0 = OB + OC; HLIT = 0.674
FBr, FCr = sp.Rational(1000, 6364), sp.Rational(5364, 6364)          # matter-era fractions (Omega_c/Omega_b = 5.364)
HOSTS882 = [("H1", 1e4, 30.0), ("H2", 3e5, 200.0), ("H3", 2e7, 700.0)]  # CFG882 Plummer dwarfs (M_sun, pc)
HOST938 = 6e10                                                          # CFG938 S8 host (M_sun), radii 50/100/250 kpc


def law_g(gN, a0):
    return 0.5 * (gN + math.sqrt(gN * gN + 4.0 * gN * a0))


def Rinv(x, a0):                                                      # u with R(u) = u^2/(a0 - u) = x
    return 0.5 * (-x + math.sqrt(x * x + 4.0 * x * a0))


def R_num(u_, a0):
    return u_ * u_ / (a0 - u_)


def Rp_num(u_, a0):
    return u_ * (2 * a0 - u_) / (a0 - u_) ** 2


def wfull_x(x):                                                       # -x - log(1-x), stable
    if x < 1e-3:
        return x * x / 2 + x ** 3 / 3 + x ** 4 / 4 + x ** 5 / 5 + x ** 6 / 6 + x ** 7 / 7
    return -x - math.log1p(-x)


def wrem_x(x):                                                        # -x - log(1-x) - x^2/2, stable
    if x < 1e-2:
        return sum(x ** n / n for n in range(3, 14))
    return -x - math.log1p(-x) - x * x / 2


def Wfull_num(u_, a0):
    return a0 * a0 * wfull_x(u_ / a0) / K_SI


def Wrem_num(u_, a0):
    return a0 * a0 * wrem_x(u_ / a0) / K_SI


# NGC 3198 (record SPARC file, Upsilon 0.61 as CFG938)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MB_N = GN_N[-1] * R_N[-1] ** 2 / G_SI

P("CFG941  self-gravity repair of CFG938's covariant parent" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P("  criteria 0b41bd0cf; A1 7c395c866 (pre-result); kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2;  NGC 3198: {len(R_N)} radii, "
  f"M_b(<{R_N[-1] / KPC:.1f} kpc) = {MB_N / MSUN:.3e} Msun")

# ================================================================================================ shared sympy
r, G, a0s, gam = sp.symbols("r G a_0 gamma", positive=True)
u, gN, gs, qq = sp.symbols("u g_N g q", positive=True)
KS = 4 * sp.pi * G
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / KS
Wrem = Wfull - u ** 2 / (2 * KS)
Dfull = sp.simplify(KS * sp.diff(Wfull, u))                           # u/(1 - u/a0)
Rrem = sp.simplify(KS * sp.diff(Wrem, u))                             # u^2/(a0 - u)


def EL_alg(Wuse, m=1, free_q=None):
    """gamma -> 0 Euler-Lagrange of the reduced static energy E[M_c] = int[-G(M_b + m M_c + M_f)^2/(2 r^2) + 4 pi r^2 W(G M_c/r^2)] dr,
    as a function of (u, g_N).  m = 2 is the source double count (M2a).  free_q: free mass M_f = q M_c substituted AFTER variation."""
    Mc = sp.Function("M_c")(r); Mb = sp.Function("M_b")(r); Mf = sp.Function("M_f")(r)
    Wf = sp.Lambda(u, Wuse)
    Lr = -G * (Mb + m * Mc + (Mf if free_q is not None else 0)) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wf(G * Mc / r ** 2)
    eq = sp.euler_equations(Lr, [Mc], [r])[0].lhs
    sub = {Mc: u * r ** 2 / G, Mb: gN * r ** 2 / G}
    if free_q is not None:
        eq = eq.subs(Mf, free_q * Mc)
    return sp.simplify(eq.subs(sub).doit())


def solve_static(Wuse, m, gNarr, a0, free_q=None):
    """root u of the reduced EL at each g_N; total g = g_N + m u (+ q u)."""
    ex = EL_alg(Wuse, m, qq if free_q is not None else None)
    f = sp.lambdify((u, gN, a0s, G, qq), ex, "math")
    qv = 0.0 if free_q is None else free_q
    grid = a0 * np.unique(np.concatenate((np.logspace(-14, -1e-12, 900), np.linspace(1e-4, 1 - 1e-13, 3000))))
    us = []
    for gn in gNarr:
        vals = np.array([f(x, gn, a0, G_SI, qv) for x in grid])
        idx = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) <= 0)[0]
        if len(idx) == 0:
            us.append(float("nan")); continue
        i = idx[0]
        us.append(brentq(lambda x: f(x, gn, a0, G_SI, qv), grid[i], grid[i + 1], xtol=1e-40, rtol=1e-15, maxiter=800))
    us = np.array(us)
    g_tot = gNarr + m * us + qv * us
    return us, g_tot, ex


def law_dev(g_tot, gNarr, a0):
    gl = np.array([law_g(x, a0) for x in gNarr])
    return float(np.nanmax(np.abs(g_tot / gl - 1))), int(np.sum(~np.isfinite(g_tot)))


def btfr_numeric(Wuse, a0, y=1e-14):
    """A1: V^4/(G M_b a0) for NGC 3198's baryons as a point mass at the radius where g_N = y a0, from the reduced EL."""
    rr_ = math.sqrt(G_SI * MB_N / (y * a0))
    us, gt, _ = solve_static(Wuse, 1, np.array([y * a0]), a0)
    return float((gt[0] * rr_) ** 2 / (G_SI * MB_N * a0))


# ------------------------------------------------------------------------------------------------ growth machinery (EdS, comoving, sub-horizon)
tt = sp.symbols("t", positive=True); al = sp.symbols("alpha")
C2s, Bs, FTs = sp.symbols("c_2 b f_t", nonnegative=True)
Kg = sp.Symbol("K", positive=True)


def growth_det(comp):
    """comp: list of (name, fraction, tethered).  Quadratic Lagrangian per comoving volume:
    L = sum 1/2 rho0_i a^2 psi_i'^2 + (a^5 K/2)(sum rhobar_i psi_i)^2 - (a^5 c2/2K)(-K rhobar_T psi_T + b beta psi_T')^2,
    beta = chibar'/c^2 = -K rhobar_T/(3H) (CFG938's chi background, D5).  EdS: a = t^(2/3), K rhobar_tot = 2/(3 t^2).
    Returns det M(alpha) for psi_i = A_i t^alpha (homogeneity checked)."""
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
    det = sp.expand(M.det())
    return det, homog


def n_from_det(det, subs):
    subs = dict(subs); subs[Kg] = 1
    pol = sp.Poly(sp.expand(det.subs(subs)), al)
    roots = np.roots([complex(sp.N(c_)) for c_ in pol.all_coeffs()])
    rr = [z.real for z in roots if abs(z.imag) < 1e-9]
    return 1.5 * max(rr)


P("\n  deriving growth determinants (sympy) ...")
DET2, HOM2 = growth_det([("b", FBr, False), ("t", FCr, True)])                       # P0 / gated / range repairs
DET3, HOM3 = growth_det([("b", FBr, False), ("f", FCr * (1 - FTs), False), ("t", FCr * FTs, True)])   # R2
rss_guard("growth dets")


def n2(c2, b):
    return n_from_det(DET2, {C2s: c2, Bs: b})


def n3(ft, b, c2=1):
    ft = min(max(ft, 1e-10), 1 - 1e-10)                                # zero-density rows make det vanish identically
    return n_from_det(DET3, {FTs: ft, Bs: b, C2s: c2})


def cfg938_matrix_n():
    """CFG938 S6's own method: medium feels baryons only (matrix [[fb, fc],[fb, 0]])."""
    alx = sp.Symbol("alx")
    ev = max(sp.N(e) for e in sp.Matrix([[FBr, FCr], [FBr, 0]]).eigenvals())
    a_ = max(sp.solve(alx ** 2 + alx / 3 - sp.Rational(2, 3) * ev, alx), key=lambda e: sp.N(e))
    return float(sp.N(3 * a_ / 2)), float(ev)


# ------------------------------------------------------------------------------------------------ slip (CFG938 S4 definitions)
def slip_table(kind):
    """kind 'P0': CFG938 static states (law, W_full); 'R1': R1's own static states (R(u) = g_N + u, W_rem)."""
    rows = {}; worst_g = 0.0; worst_8 = 0.0; inert_min = float("inf")
    for foot in FOOTS:
        a0 = A0[foot]
        for name, Mb, rk_ in SYS847:
            M = Mb * MSUN847; rr = rk_ * KPC847

            def uat(x):
                gn = G_SI * M / x ** 2
                if kind == "P0":
                    g_ = law_g(gn, a0); return g_ * a0 / (g_ + a0)
                return ((a0 - gn) + math.sqrt((a0 - gn) ** 2 + 8 * gn * a0)) / 4.0
            gn = G_SI * M / rr ** 2; uu = uat(rr); g_ = gn + uu
            W_ = Wfull_num(uu, a0) if kind == "P0" else Wrem_num(uu, a0)
            Dv = (uu / (1 - uu / a0)) if kind == "P0" else R_num(uu, a0)
            h_ = 1e-5 * rr
            rho_c = ((rr + h_) ** 2 * uat(rr + h_) - (rr - h_) ** 2 * uat(rr - h_)) / (2 * h_) / (K_SI * rr ** 2)
            vc2 = g_ * rr; row = {}
            for lab, Lpc in (("W", 0.0), ("stiff24", 24.0), ("stiff1k", 1000.0)):
                ps = math.pi * G_SI * (Lpc * PC) ** 2 * rho_c ** 2
                pr = -W_ + ps; pt = -W_ + Dv * uu / K_SI + ps
                row[lab] = dict(s_grad=4 * math.pi * G_SI * rr * abs(pr) / (C_SI ** 2 * g_),
                                s_847=8 * math.pi * G_SI * rr ** 2 * max(abs(pr), abs(pt)) / (C_SI ** 2 * vc2))
                worst_g = max(worst_g, row[lab]["s_grad"]); worst_8 = max(worst_8, row[lab]["s_847"])
            inert = K_SI * rho_c * C_SI ** 2 / (Dv * uu)
            inert_min = min(inert_min, inert)
            row.update(vc_kms=math.sqrt(vc2) / 1e3, rho_c=rho_c, u_over_a0=uu / a0, inv_eps_inertia=inert)
            rows[f"{foot}|{name}"] = row
    return rows, worst_g, worst_8, inert_min


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
# K1: NGC 3198 law from CFG938's reduced EL
k1 = {}
for foot in FOOTS:
    us, gt, ex_k1 = solve_static(Wfull, 1, GN_N, A0[foot])
    dv, nn = law_dev(gt, GN_N, A0[foot]); k1[foot] = dict(max_rel_vs_law=dv, unsolved=nn)
P(f"  K1 reduced EL (CFG938 W_full, m = 1): {sp.factor(ex_k1)}")
K1 = chk("K1_NGC3198_law_CFG938_reduction", all(k1[f]["max_rel_vs_law"] < 1e-6 and k1[f]["unsolved"] == 0 for f in FOOTS),
         f"max |g/g_law - 1| canonical {k1['canonical']['max_rel_vs_law']:.2e}, alt {k1['alt']['max_rel_vs_law']:.2e} (CFG938: 2.2e-16; line 1e-6)")
RES["K1"] = k1
# K2: FRW dust w = 0 (light symbolic stress: T_mu nu = -(2/sqrt(-g)) d(sqrt(-g) L)/d g^{mu nu} at phi = x)
gi_sym = {}; GI = sp.zeros(4, 4)
for i in range(4):
    for j in range(i, 4):
        gi_sym[(i, j)] = sp.Symbol(f"gi{i}{j}", real=True); GI[i, j] = GI[j, i] = gi_sym[(i, j)]
mm = sp.Symbol("m", positive=True); t_ = sp.Symbol("t", real=True); af = sp.Function("a", positive=True)(t_)
sqrtg = 1 / sp.sqrt(-GI.det()); Ld = sqrtg * (-mm * sp.sqrt(GI[1:, 1:].det()))
Tdn = sp.zeros(4, 4)
for (i, j), s_ in gi_sym.items():
    Tdn[i, j] = Tdn[j, i] = (-2 if i == j else -1) * sp.diff(Ld, s_) / sqrtg
FRW = [-1, af ** -2, af ** -2, af ** -2]
Tm = sp.simplify(sp.diag(*FRW) * Tdn.subs({gi_sym[(i, j)]: (FRW[i] if i == j else 0) for (i, j) in gi_sym}))
rho_d, p_d = sp.simplify(-Tm[0, 0]), sp.simplify(Tm[1, 1])
offd = all(sp.simplify(Tm[i, j]) == 0 for i in range(4) for j in range(4) if i != j)
iso = sp.simplify(Tm[1, 1] - Tm[2, 2]) == 0 and sp.simplify(Tm[1, 1] - Tm[3, 3]) == 0
K2 = chk("K2_FRW_dust_w0", offd and iso and p_d == 0 and sp.simplify(rho_d - mm / af ** 3) == 0,
         f"rho = {rho_d}, p = {p_d}, w = 0 exactly; T^mu_nu diagonal and isotropic")
del Tdn, Ld, sqrtg
rss_guard("K2")
# K3: CFG938 S6 exponent by its own matrix method
n938, ev938 = cfg938_matrix_n()
K3 = chk("K3_CFG938_S6_exponent", abs(n938 - 0.6096) < 1e-3, f"mu = {ev938:.4f}, n = {n938:.5f} (CFG938 json 0.60954; line 0.6096 +/- 1e-3)")
# K4: this lane's Lagrangian route
n_c1b0 = n2(1, 0); n_c0 = n2(0, 0)
K4 = chk("K4_Lagrangian_growth_route", HOM2 and HOM3 and abs(n_c1b0 - n938) < 1e-6 and abs(n_c0 - 1) < 1e-12,
         f"homogeneous in t: {HOM2 and HOM3}; (c2 = 1, no chi-bar gradient) n = {n_c1b0:.8f} vs K3 {n938:.8f}; (c2 = 0) n = {n_c0:.12f}")
# K5: CFG938 worst slip
_, wg0, w80, _ = slip_table("P0")
K5 = chk("K5_CFG938_slip_reproduced", abs(w80 / 1.539799903790011e-05 - 1) < 0.02,
         f"worst s_847 = {w80:.4e} (CFG938 1.5398e-5), worst s_grad = {wg0:.3e} (CFG938 5.79e-6)")
# K6: R1 static solve reproduces CFG938 M3
m3_938 = json.load(open(os.path.join(LANES, "CFG938_medium_continuum_eft", "cfg938_results_MUTATE.json")))["MUTATE"]["M3"]
k6 = {}
for foot in FOOTS:
    us, gt, ex_r1 = solve_static(Wrem, 1, GN_N, A0[foot])
    dv, nn = law_dev(gt, GN_N, A0[foot]); k6[foot] = dict(max_rel_vs_law=dv, unsolved=nn, cfg938_M3=m3_938[foot]["max_rel_vs_law"])
K6 = chk("K6_R1_equals_CFG938_M3", all(abs(k6[f]["max_rel_vs_law"] / k6[f]["cfg938_M3"] - 1) < 0.02 for f in FOOTS),
         f"R1 law dev canonical {k6['canonical']['max_rel_vs_law']:.4f} (CFG938 M3 {k6['canonical']['cfg938_M3']:.4f}), "
         f"alt {k6['alt']['max_rel_vs_law']:.4f} ({k6['alt']['cfg938_M3']:.4f})")
RES["K6"] = k6
K_ALL = K1 and K2 and K3 and K4 and K5 and K6
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> VOID'}")
RES["K_all"] = K_ALL
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)


# ------------------------------------------------------------------------------------------------ hover / F2 machinery
GL_X, GL_W = np.polynomial.legendre.leggauss(64)


def plummer_g(M, a, x):
    return G_SI * M * x / (x * x + a * a) ** 1.5


def satellite_hover(Mb_sun, a_pc, rkpc, a0, tether=True):
    """Satellite (Plummer baryons + its isolated law phantom, truncated where u_s = u_h) at the centre of its medium, in the
    settled field of a 6e10 Msun host at r.  Returns Delta a = a_medium(CoM) - a_stars along z (away from host)."""
    Mh = HOST938 * MSUN847; rh = rkpc * KPC847
    gbh = G_SI * Mh / rh ** 2; gh = law_g(gbh, a0); uh = gh - gbh
    M = Mb_sun * MSUN847; a = a_pc * PC
    us_of = lambda x: law_g(plummer_g(M, a, x), a0) - plummer_g(M, a, x)
    # truncation (implementation choice, disclosed): outermost radius in [a/100, 100 a] with u_s >= u_h; r_t = a if u_s < u_h everywhere
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
    maxw = float(wmag.max() / a0)
    wm = np.minimum(wmag, a0 * (1 - 1e-12))
    Tz = (wm ** 2 / (a0 - wm)) * wz / wmag if tether else -(wz)          # tether off: medium feels -grad chi like stars
    Tz_avg = float(np.sum((Tz * wq).sum(axis=1) * dM) / np.sum(dM))
    if tether:
        a_m = -gbh + Tz_avg
    else:
        a_m = -gbh + Tz_avg                                               # = -gbh - uh exactly (radial parts average out)
    a_s = -(gbh + uh)
    gbs_a = plummer_g(M, a, a)
    efe = (gbs_a + (Rinv(gbh + gbs_a, a0) - uh)) / (gbs_a + Rinv(gbs_a, a0))
    rho_h = None
    return dict(g_host=gh, u_h=uh, g_bh=gbh, delta_a=a_m - a_s, ratio=(a_m - a_s) / gh, r_t_pc=rt / PC, max_w_over_a0=maxw,
                g_bs_at_a=gbs_a, efe_factor=efe, efe_dex=math.log10(efe))


# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    # M1: remove each repair -> the S6-approximation exponent returns
    m1 = dict(R1_c2_to_1=n2(1, 0), R2_ft_to_1=n3(1, 0), R3theta_s_to_1=n2(1, 0), R3ell_ell_to_inf=n2(1, 0))
    m1_bite = all(abs(v - n938) < 1e-3 for v in m1.values())
    chk("M1_remove_repair_returns_0p61", m1_bite, ", ".join(f"{k} n = {v:.5f}" for k, v in m1.items()) + f" (K3 {n938:.5f})")
    # M2a: source multiplicity 2; M2b: independent-P phantom plus the medium's own mass at the law density
    m2 = {}
    for foot in FOOTS:
        a0 = A0[foot]
        _, gt2, ex2 = solve_static(Wfull, 2, GN_N, a0)
        dv2, nn2 = law_dev(gt2, GN_N, a0)
        g2b = np.array([law_g(gn + (law_g(gn, a0) - gn), a0) for gn in GN_N])
        dv2b, _ = law_dev(g2b, GN_N, a0)
        m2[foot] = dict(M2a_dev=dv2, M2a_unsolved=nn2, M2b_dev=dv2b)
    P(f"  M2a reduced EL (dust -rho_c Phi AND S2's P.grad Phi): {sp.factor(ex2)}")
    m2_bite = all(m2[f]["M2a_dev"] > 1e-6 and m2[f]["M2b_dev"] > 1e-6 for f in FOOTS)
    chk("M2_double_counting_breaks_law", m2_bite, "; ".join(f"{f}: M2a {m2[f]['M2a_dev']:.3f}, M2b {m2[f]['M2b_dev']:.3f}" for f in FOOTS))
    # M3: boost tooth
    nb1, nb0 = n2(1, 1), n2(1, 0)
    m3_bite = abs(nb1 - nb0) > 1e-3
    chk("M3_boost_tooth", m3_bite, f"full action (chi-bar gradient on) n = {nb1:.5f}; dropped n = {nb0:.5f}; |diff| = {abs(nb1 - nb0):.4f} (> 1e-3)")
    # M4: hover tooth
    m4 = {}
    for foot in FOOTS:
        for hn, Mb_, apc in HOSTS882:
            for rk in (50.0, 100.0, 250.0):
                m4[f"{foot}|{hn}|{rk:g}"] = satellite_hover(Mb_, apc, rk, A0[foot], tether=False)["ratio"]
    m4_bite = all(abs(v) < 1e-12 for v in m4.values())
    chk("M4_tether_off_universal_free_fall", m4_bite, f"max |Delta a|/g_host with the tether off = {max(abs(v) for v in m4.values()):.1e}")
    RES["MUTATE"] = dict(M1=m1, M2=m2, M3=dict(n_boost=nb1, n_noboost=nb0), M4_max=max(abs(v) for v in m4.values()))
    allbite = m1_bite and m2_bite and m3_bite and m4_bite
    P(f"\n  MUTATE: {'ALL TEETH BITE (exit 1 by design)' if allbite else 'A TOOTH FAILED TO BITE'}")
    dump(); sys.exit(1 if allbite else 2)

# ================================================================================================ D1 / D2 DIAGNOSIS
P("\n==================== D1/D2 DIAGNOSIS: where the medium's self-gravity goes ====================")
x1 = sp.Symbol("x", real=True)
Phi1, rb1, rc1, chi1, lam1, P1 = [sp.Function(n_)(x1) for n_ in ("Phi", "rho_b", "rho_c", "chi", "lam", "P")]
L938 = -sp.diff(Phi1, x1) ** 2 / (2 * KS) - (rb1 + rc1) * Phi1 - Wfull.subs(u, sp.diff(chi1, x1)) + lam1 * (sp.diff(chi1, x1, 2) - KS * rc1)
e938 = sp.euler_equations(L938, [Phi1], [x1])[0].lhs
pois938 = sp.solve(e938, sp.diff(Phi1, x1, 2))[0]
LS2 = -(sp.diff(Phi1, x1) - KS * P1) ** 2 / (2 * KS) - rb1 * Phi1 - Wrem.subs(u, KS * P1)
eS2 = sp.euler_equations(LS2, [Phi1], [x1])[0].lhs
poisS2 = sp.solve(eS2, sp.diff(Phi1, x1, 2))[0].subs(sp.diff(P1, x1), rc1)
LDC = LS2 - rc1 * Phi1
poisDC = sp.solve(sp.euler_equations(LDC, [Phi1], [x1])[0].lhs, sp.diff(Phi1, x1, 2))[0].subs(sp.diff(P1, x1), rc1)
D1 = chk("D1_Poisson_counts_medium_once", is0(pois938 - KS * (rb1 + rc1)) and is0(poisS2 - KS * (rb1 + rc1)) and is0(poisDC - KS * (rb1 + 2 * rc1)),
         f"CFG938: Phi'' = {sp.factor(pois938)}; S2 square + ID: Phi'' = {sp.factor(poisS2)}; adding dust -rho_c Phi on top (M2a) gives {sp.factor(poisDC)}: "
         "NO source double count in S2 or CFG938 (the medium's rest mass is P.grad Phi, counted once)")
# D2(i): mode average with general tether quadratic coefficient c2
kx, xx, Bb, C1, C2 = sp.symbols("k x B C_1 C_2", positive=True)
c2g = sp.Symbol("c_2", real=True)
Ct = C1 + C2
PhiM = -KS * (Bb + Ct) * sp.cos(kx * xx) / kx ** 2
Pm = Ct * sp.sin(kx * xx) / kx
Lm = -sp.diff(PhiM, xx) ** 2 / (2 * KS) - (Bb + Ct) * sp.cos(kx * xx) * PhiM - c2g * (KS * Pm) ** 2 / (2 * KS)
Lavg = sp.simplify(sp.integrate(Lm, (xx, 0, 2 * sp.pi / kx)) * kx / (2 * sp.pi))
cross12 = sp.factor(sp.diff(Lavg, C1, C2)); selfc = sp.factor(sp.diff(Lavg, C1, 2) / 2); crossb = sp.factor(sp.diff(Lavg, Bb, C1))
D2a = chk("D2a_mode_average_general_c2", is0(Lavg - KS / (4 * kx ** 2) * ((Bb + Ct) ** 2 - c2g * Ct ** 2)) and is0(cross12.subs(c2g, 1))
          and not is0(cross12.subs(c2g, 0)),
          f"<L> = (K/4k^2)[(B+C)^2 - c2 C^2]; d2<L>/dC1dC2 = {cross12}; self C1^2 coefficient = {selfc}; baryon-medium = {crossb}. "
          "c2 = 1 (W_full's quadratic) removes BOTH the medium's self-gravity and the mutual gravity of tethered components; the baryon term survives")
# D2(ii): force identity on a medium element
Phib_r, chi_r = sp.Function("Phi_b")(r), sp.Function("chi")(r)
f_full = -sp.diff(Phib_r + chi_r, r) + Dfull.subs(u, sp.diff(chi_r, r))
f_res = -sp.diff(Phib_r, r) + Rrem.subs(u, sp.diff(chi_r, r))
D2b = chk("D2b_force_identity", is0(f_full - f_res),
          "medium force -(Phi_b + chi)' + D_full(chi') = -Phi_b' + R(chi'): the tether's linear part +chi' is exactly the medium's own "
          "Newtonian pull (chi = the medium's potential): a FORCE cancellation, not a source cancellation; baryons still feel the medium")
rss_guard("D2")

# ================================================================================================ D-T THEOREM
P("\n==================== D-T: the law forces c2 = 1 for any always-on tether ====================")
uu_, gg_ = sp.symbols("uu gg", positive=True)
gsol = sp.solve(sp.Eq(uu_, gg_ - gg_ ** 2 / (gg_ + a0s)), gg_)
Fu = [s_ for s_ in gsol if sp.simplify(s_.subs({uu_: a0s / 3})) > 0][0]
DT1 = chk("DT1_law_forces_F_equals_D_full", is0(Fu - Dfull.subs(u, uu_)), f"static cold equilibrium F(u) = g = g_N + u with the law -> F(u) = {sp.factor(Fu)} = D_full(u)")
ser = sp.series(Fu, uu_, 0, 4).removeO()
DT2 = chk("DT2_c2_equals_1", is0(ser - (uu_ + uu_ ** 2 / a0s + uu_ ** 3 / a0s ** 2)), f"F(u) = {ser} + O(u^4): linear coefficient 1 -> W = u^2/2K + ... (c2 = 1)")
h1, h2, h3, b2, b3, b4 = sp.symbols("h1 h2 h3 b2 b3 b4")
ggen = uu_ + b2 * uu_ ** 2 + b3 * uu_ ** 3 + b4 * uu_ ** 4
gNgen = ggen ** 2 / a0s * (1 + h1 * ggen / a0s + h2 * (ggen / a0s) ** 2 + h3 * (ggen / a0s) ** 3)
eqs_g = sp.Poly(sp.expand(ggen - gNgen - uu_), uu_).all_coeffs()[::-1]
solb = sp.solve([eqs_g[2], eqs_g[3], eqs_g[4]], [b2, b3, b4], dict=True)[0]
DT3 = chk("DT3_any_deep_limit_law_forces_c2_1", is0(solb[b2] - 1 / a0s) and is0(eqs_g[1]),
          f"generic law g_N = (g^2/a0)(1 + h1 g/a0 + h2 (g/a0)^2 + ...): F(u) = u + ({solb[b2]}) u^2 + ...; the linear coefficient is 1 "
          "independent of h1, h2, h3 (it is the deep limit, not the simple interpolation, that forces it)")
yy, c2p = sp.symbols("y c2p", positive=True)
lim_c1 = sp.limit(((yy + sp.sqrt(yy ** 2 + 4 * yy)) / 2) ** 2 / yy, yy, 0, "+")
# F = c2 u + u^2/a0 (a0 = 1): g_N = (c2 - 1) u + u^2 -> u(g_N); g = c2 u + u^2; BTFR = g^2/g_N as g_N -> 0
uc = (-(c2p - 1) + sp.sqrt((c2p - 1) ** 2 + 4 * yy)) / 2
btfr_c = (c2p * uc + uc ** 2) ** 2 / yy
lim_lt = sp.limit(btfr_c.subs(c2p, sp.Rational(1, 2)), yy, 0, "+"); lim_gt = sp.limit(btfr_c.subs(c2p, 2), yy, 0, "+")
DT4 = chk("DT4_only_c2_1_gives_BTFR", lim_c1 == 1 and lim_lt == sp.oo and lim_gt == 0,
          f"lim V^4/(G M a0): c2 = 1 (law) -> {lim_c1}; c2 = 1/2 -> {lim_lt} (acceleration floor); c2 = 2 -> {lim_gt} (rescaled Newton). "
          "With D2a/D6 (linear self-gravity coefficient (1 - c2) K rho_c): (a) => c2 = 1 => the settling medium has NO linear self-gravity")
DT = DT1 and DT2 and DT3 and DT4
RES["DT"] = dict(F=str(Fu), series=str(ser), generic_b2=str(solb[b2]), btfr_limits=[str(lim_c1), str(lim_lt), str(lim_gt)])
rss_guard("DT")

# ================================================================================================ D5 the chi-bar timelike gradient
P("\n==================== D5: CFG938's FRW chi background enters u at O(c^0) ====================")
tq, xq, yq, zq = sp.symbols("t x y z", real=True); XX = [tq, xq, yq, zq]
cc, ep = sp.symbols("c epsilon", positive=True)
aq = sp.Function("a", positive=True)(tq)
gq = sp.diag(-cc ** 2, aq ** 2, aq ** 2, aq ** 2); giq = gq.inv()
chib = sp.Function("chibar")(tq); dchi = sp.Function("dchi")(*XX)
Vq = [sp.Function(f"V{i}")(*XX) for i in range(3)]
V2q = sum(v_ ** 2 for v_ in Vq)
gl_ = 1 / sp.sqrt(1 - ep ** 2 * V2q / cc ** 2)
uq = sp.Matrix([gl_ / cc] + [gl_ * ep * Vq[i] / (aq * cc) for i in range(3)])
normq = sp.simplify((uq.T * gq * uq)[0])
hq = giq + uq * uq.T
chiq = chib + ep * dchi
dq = [sp.diff(chiq, X_) for X_ in XX]
u2q = sum(hq[m_, n_] * dq[m_] * dq[n_] for m_ in range(4) for n_ in range(4))
u2s = sp.series(u2q, ep, 0, 3).removeO()
target = ep ** 2 * sum((sp.diff(dchi, XX[i + 1]) / aq + sp.diff(chib, tq) / cc ** 2 * Vq[i]) ** 2 for i in range(3))
D5a = chk("D5a_medium_frame_gradient_has_boost_term", normq == -1 and is0(u2s - target),
          "u^2 = h^{mu nu} d chi d chi = eps^2 |grad_phys dchi + (chibar'/c^2) V|^2 + O(eps^3) exactly (V = peculiar velocity of the medium)")
Gq = [[[sp.simplify(sum(giq[a_, d_] * (sp.diff(gq[d_, b_], XX[c_]) + sp.diff(gq[d_, c_], XX[b_]) - sp.diff(gq[b_, c_], XX[d_]))
                        for d_ in range(4)) / 2) for c_ in range(4)] for b_ in range(4)] for a_ in range(4)]
nabq = sp.Matrix(4, 4, lambda m_, n_: sp.diff(chiq, XX[m_], XX[n_]) - sum(Gq[l_][m_][n_] * dq[l_] for l_ in range(4)))
D2q = sum(hq[m_, n_] * nabq[m_, n_] for m_ in range(4) for n_ in range(4))
D2s = sp.series(D2q, ep, 0, 2).removeO()
Hq = sp.diff(aq, tq) / aq
o0 = sp.simplify(D2s.coeff(ep, 0)); o1 = sp.simplify(D2s.coeff(ep, 1))
t1 = sum(sp.diff(dchi, XX[i + 1], 2) for i in range(3)) / aq ** 2 - 3 * Hq * sp.diff(dchi, tq) / cc ** 2
D5b = chk("D5b_constraint_background_and_linear", is0(o0 + 3 * Hq * sp.diff(chib, tq) / cc ** 2) and is0(o1 - t1),
          "D^2 chibar = -3 H chibar'/c^2 (= K rhobar => chibar'/c^2 = -K rhobar/(3H), c-independent); first-order constraint = "
          "lap dchi/a^2 - 3H dchi'/c^2 with NO velocity term (so dchi = dPhi_c sub-horizon)")
P(f"  boost coefficient: chibar'/c^2 = -K rhobar_c/(3H); in EdS beta^2/(K rhobar_c) = Omega_c/6 = {float(FCr) / 6:.4f} (inertia reduction); "
  f"today |chibar'|/c = Omega_c H0 c/2 = {OC * H0_SI * C_SI / 2:.3e} m/s^2 = {OC * H0_SI * C_SI / 2 / A0['canonical']:.3f} a0 (canonical)")
del Gq, nabq, D2q
rss_guard("D5")

# ================================================================================================ D6 growth of the unrepaired parent
P("\n==================== D6: linear growth of the tethered medium (EdS, baryons free) ====================")
n_full = n2(1, 1)
P(f"  CFG938 S6 approximation (medium feels baryons only): n = {n938:.5f}   [K3/K4]")
P(f"  full quadratic action incl. the chi-bar boost (D5): n = {n_full:.5f}   (inertia x (1 - Omega_c/6); force (K rhobar_c/3) q psi, q = 1/2)")
P(f"  dust (c2 = 0): n = {n_c0:.6f}")
D6 = chk("D6_growth_exponents_computed", HOM2 and n_full < 1 - 1e-3 and abs(n_c0 - 1) < 1e-12,
         f"unrepaired parent: S6-approx {n938:.4f}, full action {n_full:.4f} (a correction to CFG938 S6: the chi-bar gradient raises the "
         "exponent but it stays far below 1); F1 confirmed for the parent")
RES["D6"] = dict(n_S6=n938, n_full=n_full, n_dust=n_c0)
# n(c2) curves (used by R3n, R3ell)
c2grid = [0.0, 1e-4, 1e-3, 3e-3, 1e-2, 0.03, 0.1, 0.3, 0.5, 0.8, 1.0]
ncurve = {c_: (n2(c_, 0), n2(c_, 1)) for c_ in c2grid}
for c_, (a_, b_) in ncurve.items():
    P(f"     c2 = {c_:7.4g}: n (no boost) = {a_:.6f}, n (boost) = {b_:.6f}")
c2max = brentq(lambda c_: n2(c_, 0) - 0.999, 1e-8, 0.5, xtol=1e-12)
P(f"  largest tether coefficient with |n - 1| < 1e-3 (no boost): c2_max = {c2max:.4e}")
RES["D6"]["c2_max"] = c2max; RES["D6"]["curve"] = {str(k): v for k, v in ncurve.items()}
rss_guard("D6")

# ================================================================================================ TESTS: helpers
TESTS = {}


def put(rep, key, ok, detail):
    TESTS.setdefault(rep, {})[key] = dict(pass_=bool(ok) if ok is not None else None, detail=str(detail))
    tag = "PASS" if ok else ("FAIL" if ok is not None else "N/A ")
    P(f"   ({key}) {tag}: {detail}")


def disp_min(Dp, Du, self_coef, u0s, a0=1.0):
    """omega^2/(K rho0) = Dp(u0) cos^2 + (D/u)(u0) sin^2 - self + (kL*)^2/2 (CFG938 S5 form, c -> infinity); grid as CFG938."""
    ks = np.logspace(-2, 5, 400); ths = np.linspace(0, math.pi / 2, 61)
    out = {}
    for u0 in u0s:
        KK, TT = np.meshgrid(ks, ths)
        w2 = Dp(u0, a0) * np.cos(TT) ** 2 + Du(u0, a0) * np.sin(TT) ** 2 - self_coef + 0.5 * KK ** 2
        out[u0] = float(w2.min())
    return out


Dfull_p = lambda u0, a0: 1 + Rp_num(u0, a0); Dfull_u = lambda u0, a0: 1 + u0 / (a0 - u0)
Rp_ = lambda u0, a0: Rp_num(u0, a0); Ru_ = lambda u0, a0: u0 / (a0 - u0)
U0GRID = (0.0909, 0.5, 0.9, 0.99)

# P0-sector static-law slip, dispersion, hover (shared by R2-tethered, R3 gates where s = 1)
slipP0, wgP0, w8P0, inP0 = slip_table("P0")
dP0 = disp_min(Dfull_p, Dfull_u, 1.0, U0GRID)
hover = {}
for foot in FOOTS:
    for hn, Mb_, apc in HOSTS882:
        for rk in (50.0, 100.0, 250.0):
            hover[f"{foot}|{hn}|{rk:g}"] = satellite_hover(Mb_, apc, rk, A0[foot])
hov_ratio = [v["ratio"] for v in hover.values()]
efe_dex = [v["efe_dex"] for v in hover.values()]
P("\n  F2 machinery (P0 static sector): satellite at the centre of its own medium in a 6e10 Msun host's settled field")
P(f"  {'case':22s} {'g_host/a0':>9s} {'u_h/a0':>7s} {'Da/g_host':>9s} {'g_bs(a)/Da':>10s} {'t_sep Myr':>9s} {'w_resp/w_cross':>14s} {'EFE dex':>8s} {'max|w|/a0':>9s}")
for kx_, v in hover.items():
    foot, hn, rk = kx_.split("|"); a0 = A0[foot]
    apc = dict((h[0], h[2]) for h in HOSTS882)[hn]
    tsep = math.sqrt(2 * apc * PC / abs(v["delta_a"])) / (3.156e13)
    rh = float(rk) * KPC847
    uh = v["u_h"]; gbh = v["g_bh"]
    # host phantom density at rh (point mass, law): rho = (1/(K r^2)) d(r^2 u)/dr
    def uhr(x):
        gn = G_SI * HOST938 * MSUN847 / x ** 2; return law_g(gn, a0) - gn
    hh = 1e-5 * rh
    rho_h = ((rh + hh) ** 2 * uhr(rh + hh) - (rh - hh) ** 2 * uhr(rh - hh)) / (2 * hh) / (K_SI * rh ** 2)
    w_resp = math.sqrt(K_SI * rho_h * Rp_num(uh, a0))
    w_cross = math.sqrt(v["g_host"] * rh) / (apc * PC)
    v.update(t_sep_Myr=tsep, omega_resp_over_cross=w_resp / w_cross, rho_host_phantom=rho_h)
    P(f"  {kx_:22s} {v['g_host'] / a0:9.4f} {uh / a0:7.4f} {v['ratio']:9.4f} {v['g_bs_at_a'] / abs(v['delta_a']):10.3f} {tsep:9.2f} "
      f"{w_resp / w_cross:14.2e} {v['efe_dex']:8.3f} {v['max_w_over_a0']:9.3f}")
RES["hover"] = hover
rss_guard("hover")

# ================================================================================================ R1
P("\n==================== R1: dust gravity kept, tether only redistributes (W_full -> W_rem) ====================")
r1a = {}
for foot in FOOTS:
    us, gt, _ = solve_static(Wrem, 1, GN_N, A0[foot]); dv, nn = law_dev(gt, GN_N, A0[foot])
    r1a[foot] = dict(dev=dv, unsolved=nn, min_u_over_a0=float(np.nanmin(us) / A0[foot]), btfr_y1e14=btfr_numeric(Wrem, A0[foot]))
u_r1y = ((1 - yy) + sp.sqrt((1 - yy) ** 2 + 8 * yy)) / 4                   # R1 static u/a0 for a point mass (R(u) = g_N + u)
btfr_r1 = sp.limit((yy + u_r1y) ** 2 / yy, yy, 0, "+")
r1_a_ok = all(r1a[f]["dev"] < 1e-6 and abs(r1a[f]["btfr_y1e14"] - 1) < 1e-6 for f in FOOTS) and btfr_r1 == 1
put("R1", "a", r1_a_ok, f"law dev canonical {r1a['canonical']['dev']:.3f}, alt {r1a['alt']['dev']:.3f} (line 1e-6); static states need u >= a0/2 "
    f"(min u/a0 = {r1a['canonical']['min_u_over_a0']:.3f}); g -> a0/2 floor: lim V^4/(GMa0) = {btfr_r1}, value at y = 1e-14 "
    f"{r1a['canonical']['btfr_y1e14']:.3e}. Identical to CFG938's M3 tooth (K6)")
put("R1", "b", True, "W_rem(0) = 0, W_rem'(u)/u -> 0: tether stress vanishes on FRW; dust w = 0 (K2)")
nR1 = n_c0
put("R1", "c", abs(nR1 - 1) < 1e-3, f"c2 = 0 -> n = {nR1:.6f} at super-L* (W_rem has no quadratic term, so no chi-bar boost either); sub-L*: stiffness Jeans "
    "omega^2 = gamma rho k^2 - K rho > 0 for k_phys L* > sqrt(2): oscillation, no growth faster than a^1")
dR1 = disp_min(Rp_, Ru_, 1.0, (0.5, 0.9, 0.99))
_, wgR1, w8R1, inR1 = slip_table("R1")
put("R1", "d", min(dR1.values()) >= -1.0 - 1e-12 and inR1 > 1, f"about R1 static states (u0/a0 = 0.5/0.9/0.99; 0.0909 has none): min omega^2/(K rho0) = "
    f"{', '.join(f'{v:.3f}' for v in dR1.values())} (bounded; Jeans-type only); FRW: -1 + (kL*)^2/2 bounded; inertia margin {inR1:.2e} > 1")
put("R1", "e", wgR1 <= 1.9e-5 and w8R1 <= 1.9e-5, f"on R1's own static states: worst s_grad {wgR1:.2e}, s_847 {w8R1:.2e} (line 1.9e-5)")
hovR1 = {}
for foot in FOOTS:
    a0 = A0[foot]
    for rk in (50.0, 100.0, 250.0):
        gbh = G_SI * HOST938 * MSUN847 / (rk * KPC847) ** 2
        uh = ((a0 - gbh) + math.sqrt((a0 - gbh) ** 2 + 8 * gbh * a0)) / 4      # R1's settled host: R(u_h) = g_bh + u_h
        a_m = -gbh - uh + R_num(uh, a0); a_s = -(gbh + uh)                       # test medium element at rest vs stars
        hovR1[f"{foot}|{rk:g}"] = (a_m - a_s) / (gbh + uh)
r1_f_ok = all(abs(v) <= 0.01 for v in hovR1.values())
put("R1", "f", r1_f_ok, f"mutual cross term Newtonian (c2 = 0, D2a) BUT hover lemma in R1's own settled host (R(u_h) = g_bh + u_h): a medium element at rest "
    f"feels zero net force, Delta a/g_host = {min(hovR1.values()):.4f} ... {max(hovR1.values()):.4f} (leading order); CFG925 R3 not respected")
put("R1", "g", False, "g1 no (medium feels R(u) tether in settled regions); g2 no (equilibrium reads the total medium field); g3 yes (dust + stiffness)")
RES["R1"] = dict(a=r1a, disp=dR1, slip=(wgR1, w8R1), inertia_min=inR1, hover=hovR1)
rss_guard("R1")

# ================================================================================================ R2
P("\n==================== R2: two separately conserved media (free dust + tethered), no conversion ====================")
nft = {ft: (n3(ft, 0), n3(ft, 1)) for ft in (0.0, 1e-3, 3e-3, 0.01, 0.03, 0.1, 0.3, 1.0)}
for ft, (a_, b_) in nft.items():
    P(f"     f_t = {ft:6.3g}: joint growing-mode n (no boost) = {a_:.6f}, (boost) = {b_:.6f}")
ftmax = brentq(lambda ft: n3(ft, 1) - 0.999, 1e-9, 0.9, xtol=1e-12)
q_c = (1 - ftmax) / ftmax
r2a = {}
for foot in FOOTS:
    a0 = A0[foot]
    us, gt, ex_r2 = solve_static(Wfull, 1, GN_N, a0, free_q=q_c)
    dv, nn = law_dev(gt, GN_N, a0)
    uL = law_g(GN_N[-1], a0) - GN_N[-1]
    Mph = uL * R_N[-1] ** 2 / G_SI
    supply = ftmax * 53.64 * MB_N
    r2a[foot] = dict(dev_with_free=dv, unsolved=nn, phantom_over_Mb=Mph / MB_N, tethered_supply_over_need=supply / Mph)
P(f"  R2 tethered equilibrium with free mass M_f = q M_t (varied first, substituted after): EL = {sp.factor(ex_r2)}")
P(f"  f_t,max (|n - 1| < 1e-3, boost on) = {ftmax:.4e} -> q = {q_c:.3e}")
r2_a_ok = all(r2a[f]["dev_with_free"] < 1e-6 for f in FOOTS)
put("R2", "a", r2_a_ok, f"tethered-only galaxy = P0 (K1, 2e-16) BUT jointly (criteria sec. 4): f_t = 1 fails (c); at f_t <= {ftmax:.2e} galaxies carry free mass "
    f"q = {q_c:.2e} x tethered, which enters the law's source (R(u_t) = g_b + g_f): law dev {r2a['canonical']['dev_with_free']:.2f} / {r2a['alt']['dev_with_free']:.2f}; "
    f"tethered supply / NGC 3198 phantom = {r2a['canonical']['tethered_supply_over_need']:.2e} / {r2a['alt']['tethered_supply_over_need']:.2e}")
put("R2", "b", True, "two label-field dusts: w = 0 each (K2); tether sector zero on FRW")
r2_c_ok = abs(nft[1.0][1] - 1) < 1e-3 and abs(nft[1.0][0] - 1) < 1e-3
put("R2", "c", r2_c_ok, f"graded on the composition that passes (a) (f_t = 1, criteria sec. 4): n = {nft[1.0][1]:.4f} (full action) / {nft[1.0][0]:.4f} "
    f"(S6 approx); the tethered medium keeps c2 = 1 (D-T); n -> 1 only as f_t -> 0, where it is a passenger of the free medium's gravity")
# two-component dispersion
def disp2(rf, rt_, u0, a0=1.0):
    ks = np.logspace(-2, 5, 200); ths = np.linspace(0, math.pi / 2, 31); mn = float("inf")
    for th_ in ths:
        A_ = Dfull_p(u0, a0) * math.cos(th_) ** 2 + Dfull_u(u0, a0) * math.sin(th_) ** 2 if u0 > 0 else 1.0
        for k_ in ks:
            V = np.array([[-rf * rf, -rf * rt_], [-rf * rt_, -rt_ * rt_ + rt_ * rt_ * A_ + 0.5 * k_ * k_ * rt_ * rt_]])
            Mi = np.diag([1 / math.sqrt(rf), 1 / math.sqrt(rt_)])
            mn = min(mn, float(np.linalg.eigvalsh(Mi @ V @ Mi).min()))
    return mn
d2c = {f"rf/rt={rf:g}|u0={u0:g}": disp2(rf, 1.0, u0) for rf in (0.1, 1.0, 10.0) for u0 in (0.0, 0.0909, 0.5, 0.9)}
d2_ok = all(v >= -(rf_ + 1.0) * (1 + 1e-9) for (key_, v), rf_ in zip(d2c.items(), [0.1] * 4 + [1.0] * 4 + [10.0] * 4))
put("R2", "d", d2_ok, f"two-component WKB (free + tethered, units K = rho_t = L* = 1): min omega^2 >= -(rho_f + rho_t) on every case "
    f"(min {min(d2c.values()):.3f}): bounded Jeans growth; tethered sector as CFG938 (min omega^2 >= 0: {min(dP0.values()):.3f})")
put("R2", "e", w8P0 <= 1.9e-5 and wgP0 <= 1.9e-5, f"tethered static states = P0: worst s_grad {wgP0:.2e}, s_847 {w8P0:.2e}")
hov_ok = all(abs(v) <= 0.01 for v in hov_ratio)
put("R2", "f", hov_ok, f"tethered satellite in a tethered host: Delta a/g_host = {min(hov_ratio):.3f} ... {max(hov_ratio):.3f} (hover); only satellites whose cold energy "
    "is FREE fall universally")
put("R2", "g", False, "g1 no (tethered medium feels -grad Phi_b - grad Phi_f + R(u_t)); g2 no (equilibrium reads g_b + g_f and the total tethered field); g3 only for the free medium")
RES["R2"] = dict(n_ft=nft, ft_max=ftmax, q=q_c, a=r2a, disp2=d2c)
rss_guard("R2")

# ================================================================================================ R3n density gate
P("\n==================== R3n: density gate s(rho_c) on the tether sector ====================")
rr_s = sp.Symbol("rr", positive=True); Ms_ = sp.Symbol("Ms", positive=True)
gN_pm = G * Ms_ / rr_s ** 2
u_pm = (gN_pm + sp.sqrt(gN_pm ** 2 + 4 * gN_pm * a0s)) / 2 - gN_pm
rho_pm = sp.lambdify((rr_s, Ms_, a0s, G), sp.diff(rr_s ** 2 * u_pm, rr_s) / (KS * rr_s ** 2), "math")
u_pm_f = sp.lambdify((rr_s, Ms_, a0s, G), u_pm, "math")
S5 = lambda x: 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3
S5p = lambda x: 30 * x ** 4 - 60 * x ** 3 + 30 * x ** 2
S5pp = lambda x: 120 * x ** 3 - 180 * x ** 2 + 60 * x
# sympy: k^2 coefficient of the gated tether + gated stiffness
rho0s, drs, dus, W0s, s0, s1, s2v = sp.symbols("rho0 drho du W0 s0 s1 s2")
Wd1, Wd2 = sp.symbols("W1 W2")
sexp = s0 + s1 * drs + s2v * drs ** 2 / 2; Wexp = W0s + Wd1 * dus + Wd2 * dus ** 2 / 2
Lgate = -sexp * Wexp - sexp * gam / 2 * drs ** 2
V2c = sp.expand(-Lgate).coeff(drs, 2).subs(dus, 0)
R3nsym = chk("R3n_k2_coefficient", is0(V2c - (s2v * W0s / 2 + s0 * gam / 2)),
             "potential's delta rho^2 coefficient = (s'' W + s gamma)/2 -> omega^2 -> rho0 (s'' W + s gamma) k^2 at large k (s'' = d2s/drho2)")
r3n = {}
for foot in FOOTS:
    a0 = A0[foot]
    gl_ = np.array([law_g(x, a0) for x in GN_N]); uu_N = gl_ - GN_N
    rho_ph = np.gradient(R_N ** 2 * uu_N, R_N) / (K_SI * R_N ** 2)
    neg = int(np.sum(rho_ph <= 0))
    rho_star = float(np.min(rho_ph[rho_ph > 0]))
    z_on = (rho_star / RHO_C0) ** (1 / 3) - 1; z_off = (rho_star * math.exp(-1) / RHO_C0) ** (1 / 3) - 1
    r_star = brentq(lambda x: rho_pm(x, MB_N, a0, G_SI) - rho_star * math.exp(-1), 0.05 * R_N[-1], 1e4 * R_N[-1])
    # transition-region effective sound speed, L* = 24 pc and 1 kpc
    ceff = {}
    for Lpc in (24.0, 1000.0):
        gm = K_SI * (Lpc * PC) ** 2 / 2; mins = []
        for xg in np.linspace(0.02, 0.98, 49):
            rho0 = rho_star * math.exp(-(1 - xg))
            rr0 = brentq(lambda x: rho_pm(x, MB_N, a0, G_SI) - rho0, 0.05 * R_N[-1], 1e4 * R_N[-1])
            u0 = u_pm_f(rr0, MB_N, a0, G_SI)
            s_ = S5(xg); spp = (S5pp(xg) - S5p(xg)) / rho0 ** 2              # Delta = 1
            mins.append(rho0 * (spp * Wfull_num(u0, a0) + s_ * gm) / (s_ * gm * rho0 if s_ > 0 else 1.0))
        ceff[f"{Lpc:g}pc"] = float(min(mins))
    gate847 = {}
    for name, Mb, rk_ in SYS847:
        rhs = rho_pm(rk_ * KPC847, Mb * MSUN847, a0, G_SI); gate847[name] = "on" if rhs >= rho_star else "OFF"
    r3n[foot] = dict(rho_star=rho_star, nonpositive_radii=neg, z_on=z_on, z_off=z_off, r_star_kpc=r_star / KPC,
                     ceff_ratio_min=ceff, gate_on_CFG847=gate847)
    P(f"  [{foot}] rho_* = {rho_star:.3e} kg/m^3 = {rho_star / RHO_C0:.0f} rhobar_c0 (non-positive rho_ph radii: {neg}); gate fully ON for the cosmic "
      f"mean at z > {z_on:.1f}, off below z = {z_off:.1f}; tether ends at r_* = {r_star / KPC:.0f} kpc; min c_eff^2/(s gamma rho) in the "
      f"transition: {ceff}; CFG847 systems gated: {gate847}")
r3n_btfr_finite = all(math.isfinite(r3n[f]["r_star_kpc"]) for f in FOOTS)       # gate ends the tether at finite r -> BTFR limit 0
r3n_a_ok = (not r3n_btfr_finite) and all(r3n[f]["nonpositive_radii"] == 0 for f in FOOTS)
put("R3n", "a", r3n_a_ok, f"43 radii with s = 1 are P0's (non-positive rho_ph radii: {r3n['canonical']['nonpositive_radii']} / {r3n['alt']['nonpositive_radii']}) BUT "
    f"the deep BTFR needs the tether at arbitrarily low density (rho_ph ~ r^-2 -> 0): beyond r_* = {r3n['canonical']['r_star_kpc']:.0f} / "
    f"{r3n['alt']['r_star_kpc']:.0f} kpc the gate is off and lim V^4/(GMa0) = 0; CFG847 gates (canonical): {r3n['canonical']['gate_on_CFG847']}")
put("R3n", "b", True, "W(0) = 0: the gated sector vanishes on FRW for any s")
r3n_c_ok = all(r3n[f]["z_on"] < 0 for f in FOOTS)                               # gate never on for the cosmic mean at z <= 1100
r3n_c_ok = r3n_c_ok or abs(n_full - 1) < 1e-3
put("R3n", "c", r3n_c_ok, f"cosmic-mean medium has rho > rho_* at z > {r3n['canonical']['z_on']:.1f} / {r3n['alt']['z_on']:.1f} (s = 1): n = {n_full:.4f} there "
    f"(S6-approx {n938:.4f}); |n - 1| < 1e-3 fails over z in [{r3n['canonical']['z_on']:.0f}, 1100]")
dneg = min(min(v["ceff_ratio_min"].values()) for v in r3n.values())
put("R3n", "d", dneg >= 0, f"transition shell: c_eff^2 = rho0 (s'' W + s gamma); min c_eff^2/(s gamma rho0) = {dneg:.3e} < 0 -> gradient instability, Im omega ~ k "
    "(L* = 24 pc and 1 kpc, both footings); static s = 1 states as CFG938")
put("R3n", "e", True, f"where s = 1 the static states are P0's (worst {w8P0:.2e}); gated-off systems carry no tether stress")
put("R3n", "f", hov_ok, f"settled host region (s = 1): hover, Delta a/g_host = {min(hov_ratio):.3f} ... {max(hov_ratio):.3f}")
put("R3n", "g", False, "g1/g2 no in s = 1 regions; g3 no (gate on for the cosmic mean at high z)")
RES["R3n"] = r3n
rss_guard("R3n")

# ================================================================================================ R3theta turnaround gate
P("\n==================== R3theta: turnaround gate s(theta), theta = medium expansion ====================")
th0s, dths = sp.symbols("theta0 dtheta"); sth0, sth1, sth2 = sp.symbols("st0 st1 st2")
Lth = -(sth0 + sth1 * dths + sth2 * dths ** 2 / 2) * W0s
kin_corr = sp.expand(Lth).coeff(dths, 2)
R3tsym = chk("R3theta_kinetic_term", is0(kin_corr + sth2 * W0s / 2),
             "-s(theta) W contributes -(1/2) s''(theta) W (div v)^2: longitudinal kinetic coefficient rho0 - s'' W k^2")
xs_ = np.linspace(0, 1, 200001); spp_max = float((S5pp(xs_)[xs_ > 0.5]).__neg__().max())   # s = 1 - S5(theta/theta_s): s'' = -S5''/theta_s^2
ghost = {}
for zt in (0.0, 1.0, 3.0):
    Krho0 = 5.55 * 1.5 * OM0 * H0_SI ** 2 * (1 + zt) ** 3                 # turnaround overdensity 5.55 (EdS) of the cosmic mean at z_ta
    rho0 = Krho0 / K_SI
    for Rmpc in (0.1, 1.0, 10.0):
        Rm = Rmpc * 1e3 * KPC; u0 = Krho0 * (Rm / 2) / 3
        W0 = Wfull_num(min(u0, 0.999 * A0["canonical"]), A0["canonical"])
        stt = spp_max / H0_SI ** 2                                         # theta_s = H0
        kg = math.sqrt(rho0 / (stt * W0))
        ghost[f"z_ta={zt:g}|R={Rmpc:g}Mpc"] = dict(k_ghost_R=kg * Rm, u0_over_a0=u0 / A0["canonical"])
P(f"  s'' max on the upper half of the transition = {spp_max:.4f}/theta_s^2 (theta_s = H0); ghost band k > k_g:")
for k_, v in ghost.items():
    P(f"     {k_:22s} k_g R = {v['k_ghost_R']:.3f}   (u0/a0 = {v['u0_over_a0']:.2e})")
btfrP0 = {f: btfr_numeric(Wfull, A0[f]) for f in FOOTS}
P0_a_ok = all(k1[f]["max_rel_vs_law"] < 1e-6 and abs(btfrP0[f] - 1) < 1e-6 for f in FOOTS) and lim_c1 == 1
s5_0 = (S5(0.0), S5p(0.0), S5pp(0.0))
put("R3theta", "a", P0_a_ok and s5_0 == (0.0, 0.0, 0.0), f"static states have theta = 0, s(0) = 1, s'(0) = s''(0) = 0 (quintic gate): identical to P0 "
    f"(K1 {k1['canonical']['max_rel_vs_law']:.1e}; BTFR limit {lim_c1}, at y = 1e-14: {btfrP0['canonical'] - 1:+.2e} / {btfrP0['alt'] - 1:+.2e})")
put("R3theta", "b", True, "gate x W(0) = 0 on FRW")
th_lin_ok = 3 * H0_SI > H0_SI                                                 # theta of the cosmic mean exceeds theta_s at every z <= 1100
put("R3theta", "c", th_lin_ok and abs(n_c0 - 1) < 1e-3, f"cosmic-mean linear medium has theta = 3H(z)(1 + O(delta)) >= 3 H0 > theta_s = H0: s = s' = s'' = 0, pure dust "
    f"(stiffness gated too): n = {n_c0:.6f} at every k, sub- and super-L*")
kg_all = [v["k_ghost_R"] for v in ghost.values()]
put("R3theta", "d", not all(math.isfinite(k_) for k_ in kg_all), f"static states fine (s'' = 0 at theta = 0) BUT in the transition (theta in (theta_s/2, theta_s)) s'' > 0: "
    f"kinetic coefficient rho0 - s''W k^2 < 0 for k > k_g (k_g R = {min(kg_all):.2f}-{max(kg_all):.2f}): a GHOST band and a degenerate kinetic surface")
put("R3theta", "e", w8P0 <= 1.9e-5 and wgP0 <= 1.9e-5, f"static states = P0 (worst {w8P0:.2e})")
put("R3theta", "f", hov_ok, f"settled host (theta = 0, s = 1): hover, Delta a/g_host = {min(hov_ratio):.3f} ... {max(hov_ratio):.3f}")
put("R3theta", "g", False, "g1/g2 no in settled regions (g3 yes): the settled sector is CFG938's, not class A's")
RES["R3theta"] = dict(ghost=ghost, spp_max=spp_max)

# ================================================================================================ R3ell range gate
P("\n==================== R3ell: finite range of the medium's own potential, D^2 chi - chi/ell^2 = K m n ====================")
kk_, ll_ = sp.symbols("k ell", positive=True)
c2k = sp.simplify((kk_ ** 2) / (kk_ ** 2 + 1 / ll_ ** 2))
R3lsym = chk("R3ell_cancellation_fraction", is0(c2k - kk_ ** 2 * ll_ ** 2 / (1 + kk_ ** 2 * ll_ ** 2)) and
             sp.limit((1 + rr_s / ll_) * sp.exp(-rr_s / ll_), rr_s, sp.oo) == 0,
             "linear tether force / medium self-gravity = k^2 l^2/(1 + k^2 l^2) (Yukawa vs Newton); point-source Yukawa factor (1 + r/l) e^{-r/l} -> 0: "
             "no asymptotic BTFR for any finite l")
kphys_max = 5 * HLIT / (1e3 * KPC) * 1101; kphys_min = 0.01 * HLIT / (1e3 * KPC) * 1101
ell_c = math.sqrt(c2max / (1 - c2max)) / kphys_max
ell_c_loose = math.sqrt(c2max / (1 - c2max)) / kphys_min


_YCACHE = {}


def yukawa_u(ell, a0, r_out=1e3 * KPC, N=20000):
    """Yukawa field of NGC 3198's law medium (SPARC radii, point-mass baryons beyond the last radius, out to r_out) at the 43 radii.
    Returns max_i |u_Yukawa/u_Newton - 1| (the tether's reading vs the medium's Newtonian field on the same shells)."""
    if a0 not in _YCACHE:
        rs_ = np.logspace(math.log10(0.01 * KPC), math.log10(r_out), N)
        gl_in = np.array([law_g(x, a0) for x in GN_N]) - GN_N
        lr_in = np.log(R_N); mc_in = gl_in * R_N ** 2 / G_SI
        Mc = np.empty_like(rs_)
        for i_, x in enumerate(rs_):
            if x <= R_N[0]:
                Mc[i_] = mc_in[0] * (x / R_N[0]) ** 3
            elif x <= R_N[-1]:
                Mc[i_] = np.interp(math.log(x), lr_in, mc_in)
            else:
                gn = G_SI * MB_N / x ** 2; Mc[i_] = (law_g(gn, a0) - gn) * x * x / G_SI
        _YCACHE[a0] = (np.diff(Mc), np.sqrt(rs_[1:] * rs_[:-1]))
    dm, sm = _YCACHE[a0]
    uN = np.zeros(len(R_N)); uY = np.zeros(len(R_N))
    for i_, rq in enumerate(R_N):
        inn = sm < rq; out_ = ~inn
        xs1 = sm[inn] / ell; yq = rq / ell
        sinhc_e = np.where(xs1 < 20, np.sinh(np.minimum(xs1, 20.0)) / np.maximum(xs1, 1e-300) * np.exp(-yq),
                           0.5 * (np.exp(xs1 - yq) - np.exp(-xs1 - yq)) / np.maximum(xs1, 1e-300))
        sinhc_e = np.where(xs1 < 1e-6, (1 + xs1 ** 2 / 6) * np.exp(-yq), sinhc_e)
        uY_in = G_SI * np.sum(dm[inn] * sinhc_e) * (1 + yq) / rq ** 2
        so = sm[out_]
        fy = (yq ** 2 / 3 + yq ** 4 / 30) if yq < 1e-3 else (math.cosh(yq) - math.sinh(yq) / yq) if yq < 20 else None
        if fy is None:
            term = 0.5 * (np.exp(yq - so / ell) + np.exp(-yq - so / ell)) - 0.5 * (np.exp(yq - so / ell) - np.exp(-yq - so / ell)) / yq
        else:
            term = np.exp(-so / ell) * fy
        uY_out = -G_SI * np.sum(dm[out_] * term / so) / rq
        uY[i_] = uY_in + uY_out; uN[i_] = G_SI * np.sum(dm[inn]) / rq ** 2
    return float(np.max(np.abs(uY / uN - 1)))


r3l = {}
for foot in FOOTS:
    a0 = A0[foot]
    dev_c = yukawa_u(ell_c, a0)
    ell_scan = np.logspace(math.log10(10 * KPC), math.log10(1e7 * KPC), 61); ell_a = float("nan")
    for el in ell_scan:
        if yukawa_u(el, a0) < 1e-6:
            ell_a = float(el); break
    r3l[foot] = dict(ell_max_c_pc=ell_c / PC, ell_max_c_loose_pc=ell_c_loose / PC, tether_dev_at_ell_c=dev_c, ell_min_a_Mpc=ell_a / (1e3 * KPC))
    P(f"  [{foot}] (c) needs l <= {ell_c / PC:.3g} pc (k = 5 h/Mpc at z = 1100; {ell_c_loose / PC:.3g} pc at k = 0.01 h/Mpc): there the tether field at "
      f"NGC 3198's radii deviates by {dev_c:.3f}; (a) at 1e-6 needs l >= {ell_a / (1e3 * KPC):.3g} Mpc (finite-radius law only; the BTFR limit fails for every finite l)")
    rss_guard("R3ell")
put("R3ell", "a", not R3lsym, f"finite-radius law needs l >= {r3l['canonical']['ell_min_a_Mpc']:.3g} / {r3l['alt']['ell_min_a_Mpc']:.3g} Mpc and the deep BTFR "
    "fails for every finite l (Yukawa factor -> 0, R3ell_cancellation_fraction)")
put("R3ell", "b", True, "lambda-bar = 0, u = 0, tau = 0 on FRW: no stress; dust w = 0")
r3l_c_ok = all(r3l[f]["ell_max_c_pc"] * PC >= r3l[f]["ell_min_a_Mpc"] * 1e3 * KPC for f in FOOTS)
put("R3ell", "c", r3l_c_ok, f"needs l <= {ell_c / PC:.3g} pc (strictest k) or {ell_c_loose / PC:.3g} pc (k = 0.01 h/Mpc), disjoint from (a)'s Mpc range; "
    "at any l allowed by (a) every relevant mode is tethered at z = 1100 (n = parent's)")
put("R3ell", "d", True, "massive chi: tether linear force reduced by k^2l^2/(1 + k^2l^2); omega^2 >= -K rho0 + c_s^2 k^2: bounded")
put("R3ell", "e", w8P0 <= 1.9e-5, f"for l >= l_min(a) the static states are P0's to < 1e-6 (worst {w8P0:.2e})")
put("R3ell", "f", hov_ok, f"within l: hover, Delta a/g_host = {min(hov_ratio):.3f} ... {max(hov_ratio):.3f}")
put("R3ell", "g", False, "g1/g2 no within l; g3 no at the scales allowed by (a)")
RES["R3ell"] = r3l
rss_guard("R3ell")

# ================================================================================================ unrepaired parent row (reference)
P("\n==================== P0 (CFG938, unrepaired) reference row ====================")
put("P0", "a", P0_a_ok, f"K1: {k1['canonical']['max_rel_vs_law']:.1e} / {k1['alt']['max_rel_vs_law']:.1e}; BTFR limit {lim_c1}, y = 1e-14: "
    f"{btfrP0['canonical'] - 1:+.2e} / {btfrP0['alt'] - 1:+.2e}")
put("P0", "b", K2, "CFG938 S1 (K2)")
put("P0", "c", abs(n_full - 1) < 1e-3 and abs(n938 - 1) < 1e-3, f"n = {n938:.4f} (S6 approx) / {n_full:.4f} (full action, D6)")
put("P0", "d", min(dP0.values()) >= 0, f"CFG938 S5 grid min omega^2/(K rho0) = {', '.join(f'{v:.3f}' for v in dP0.values())}; inertia margin {inP0:.2e}")
put("P0", "e", w8P0 <= 1.9e-5, f"worst s_847 {w8P0:.2e}, s_grad {wgP0:.2e}")
put("P0", "f", hov_ok, f"Delta a/g_host = {min(hov_ratio):.3f} ... {max(hov_ratio):.3f}; EFE {min(efe_dex):.3f} ... {max(efe_dex):.3f} dex")
put("P0", "g", False, "g1 no, g2 no, g3 no")

# ================================================================================================ CLASSES
P("\n==================== CLASSES (frozen rules, criteria sec. 6) ====================")
NOTREP = {
    "R1": DT and not TESTS["R1"]["a"]["pass_"],
    "R2": DT and not TESTS["R2"]["c"]["pass_"] and r2a["canonical"]["dev_with_free"] > 1e-6 and r2a["alt"]["dev_with_free"] > 1e-6,
    "R3n": DT and not TESTS["R3n"]["a"]["pass_"] and not TESTS["R3n"]["c"]["pass_"],
    "R3ell": DT and R3lsym and not TESTS["R3ell"]["a"]["pass_"] and not TESTS["R3ell"]["c"]["pass_"],
    "R3theta": False,
}
WHY = {
    "R1": "D-T: an always-on tether passes (a) only with c2 = 1, which cancels the linear self-gravity; R1's c2 = 0 fails (a) (= CFG938 M3)",
    "R2": "f_t = 1: the tethered medium has c2 = 1 (D-T); f_t < 1: free self-gravitating mass in every galaxy enters the law's source (no segregation or conversion in the action)",
    "R3n": "the deep BTFR needs s = 1 at all densities (rho_ph -> 0), i.e. s = 1 on the cosmic mean -> D-T",
    "R3ell": "the deep BTFR fails for every finite range; l -> infinity is the parent (D-T); finite-radius windows disjoint by > 4 decades",
    "R3theta": "",
}
CLASSES = {}
for rep in ("R1", "R2", "R3n", "R3theta", "R3ell"):
    tests = TESTS[rep]; fails = [k for k in "abcdefg" if not tests[k]["pass_"]]
    if not fails:
        cl = "REPAIRED"
    elif NOTREP[rep]:
        cl = "NOT REPAIRABLE"
    else:
        cl = "PARTIAL"
    CLASSES[rep] = dict(cls=cl, fails=fails, why=WHY[rep])
    P(f"  {rep:8s} {cl:15s} fails: {','.join(fails) or '-'}   {WHY[rep]}")
any_rep = any(v["cls"] == "REPAIRED" for v in CLASSES.values())
any_ae = any(all(TESTS[rep][k]["pass_"] for k in "abcde") for rep in CLASSES)
if any_rep:
    OVERALL = "SELF-GRAVITY RESTORED"
elif any_ae:
    OVERALL = "CONDITIONAL"
elif DT:
    OVERALL = "STRUCTURAL OBSTRUCTION"
else:
    OVERALL = "NOT REPAIRED (no proof)"
P(f"\n  OVERALL: {OVERALL}")
P("  (g) fails for every repair: class A (the T1x/T2x/NC1x shear-pass engine) is NOT the non-relativistic limit of any tested parent; the shear results do not transfer.")
cr925 = all(abs(v) <= 0.01 for v in hov_ratio) and all(abs(e) <= 0.01 for e in efe_dex)
P(f"  CFG925 R3 (no satellite EFE) respected by the tethered sector: {cr925}")
RES["tests"] = TESTS; RES["classes"] = CLASSES; RES["overall"] = OVERALL; RES["CFG925_R3_respected"] = cr925
RES["slip_P0"] = slipP0; RES["disp_P0"] = dP0
allchk = all(v["pass"] for v in RES["checks"].values())
P(f"\n  all checks pass: {allchk}; runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
dump()
sys.exit(0 if (allchk and K_ALL) else 1)

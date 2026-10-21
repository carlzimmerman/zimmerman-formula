"""CFG944 -- curing the ghost of the turnaround-gated tether (CFG941 R3theta).
Criteria: FROZEN_CRITERIA.md (2587be5c7, committed alone before this script).
Run (one core, one process, < 1 GB):
    CFG944_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg944.py   -> cfg944_K.out, cfg944_results_K.json (K only)
    CFG944_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg944.py  -> cfg944_MUTATE.out, cfg944_results_MUTATE.json
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg944.py                  -> cfg944.out, cfg944_results.json (K + main)
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite).
kappa = 1/2 FITTED; footings never pooled; cold energy (no particle species); not theory closed."""
import os, sys, io, json, math, time, resource, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG944_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG944_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
OUT = []
RES = {"lane": "CFG944", "criteria": "2587be5c7", "amendments": [], "mutate": MUT, "stage": STAGE, "checks": {}, "tests": {}}
T0 = time.time()
RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg944_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg944{TAG}.out"), "w").write("\n".join(OUT) + "\n")


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
MPC = 1e3 * KPC
K_SI = 4 * math.pi * G_SI
MSUN847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's constants for its systems (as CFG938/941)
SYS847 = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0),
          ("cluster", 1.5e14, 1000.0)]
H0_SI = 67.4e3 / MPC; RHO_CRIT = 3 * H0_SI ** 2 / (8 * math.pi * G_SI)
OB = 0.0493; OC = 5.364 * OB; OM0 = OB + OC; HLIT = 0.674
FB, FC = 1.0 / 6.364, 5.364 / 6.364
FBr, FCr = sp.Rational(1000, 6364), sp.Rational(5364, 6364)
THETA_S = H0_SI                                                        # CFG941 R3theta: theta_s = H0
C2MAX_941 = None                                                       # set in K3


def law_g(gN, a0):
    return 0.5 * (gN + math.sqrt(gN * gN + 4.0 * gN * a0))


def wfull_x(x):                                                       # -x - log(1-x), stable (x = u/a0 < 1)
    if x < 1e-3:
        return x * x / 2 + x ** 3 / 3 + x ** 4 / 4 + x ** 5 / 5 + x ** 6 / 6 + x ** 7 / 7
    return -x - math.log1p(-x)


def Wfull_num(u_, a0):
    return a0 * a0 * wfull_x(u_ / a0) / K_SI


def D_num(u_, a0):                                                    # K W_full'(u) = u/(1 - u/a0)
    return u_ / (1.0 - u_ / a0)


def Dp_num(u_, a0):                                                   # d D/du = 1/(1 - u/a0)^2
    return 1.0 / (1.0 - u_ / a0) ** 2


def S5(x):
    x = np.clip(x, 0.0, 1.0); return 6 * x ** 5 - 15 * x ** 4 + 10 * x ** 3


def S5pp(x):
    return 120 * x ** 3 - 180 * x ** 2 + 60 * x


# NGC 3198 (record SPARC file, Upsilon 0.61 as CFG938/941)
_d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
R_N = _d[:, 0] * KPC
GN_N = (_d[:, 3] * 1e3 * np.abs(_d[:, 3] * 1e3) + 0.61 * _d[:, 4] * 1e3 * np.abs(_d[:, 4] * 1e3)
        + 0.61 * _d[:, 5] * 1e3 * np.abs(_d[:, 5] * 1e3)) / R_N
MB_N = GN_N[-1] * R_N[-1] ** 2 / G_SI


def ngc_states(a0):
    """the law's u, the phantom (medium) density and W at NGC 3198's 43 radii."""
    gl = np.array([law_g(x, a0) for x in GN_N]); uu = gl - GN_N
    rho = np.gradient(R_N ** 2 * uu, R_N) / (K_SI * R_N ** 2)
    W = np.array([Wfull_num(x, a0) for x in uu])
    return uu, rho, W, gl


P("CFG944  curing the ghost of the turnaround-gated tether (CFG941 R3theta)" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P("  criteria 2587be5c7; kappa = 1/2 FITTED; footings never pooled; cold energy, no particle species; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2;  NGC 3198: {len(R_N)} radii, "
  f"M_b(<{R_N[-1] / KPC:.1f} kpc) = {MB_N / MSUN:.3e} Msun;  theta_s = H0 = {THETA_S:.4e} 1/s")

# ================================================================================================ shared sympy
r, G, a0s, gam = sp.symbols("r G a_0 gamma", positive=True)
u, gN = sp.symbols("u g_N", positive=True)
KS = 4 * sp.pi * G
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / KS


def EL_alg(Wuse):
    """gamma -> 0 Euler-Lagrange of CFG938's reduced static energy E[M_c] = int[-G(M_b + M_c)^2/(2 r^2) + 4 pi r^2 W(G M_c/r^2)] dr."""
    Mc = sp.Function("M_c")(r); Mb = sp.Function("M_b")(r)
    Wf = sp.Lambda(u, Wuse)
    Lr = -G * (Mb + Mc) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wf(G * Mc / r ** 2)
    eq = sp.euler_equations(Lr, [Mc], [r])[0].lhs
    return sp.simplify(eq.subs({Mc: u * r ** 2 / G, Mb: gN * r ** 2 / G}).doit())


def solve_static(gNarr, a0):
    ex = EL_alg(Wfull)
    f = sp.lambdify((u, gN, a0s, G), ex, "math")
    us = []
    for gn in gNarr:
        lo, hi = 1e-300, a0 * (1 - 1e-15)
        us.append(brentq(lambda x: f(x, gn, a0, G_SI), lo, hi, xtol=1e-300, rtol=8.9e-16, maxiter=2000))
    us = np.array(us)
    return us, gNarr + us, ex


# ------------------------------------------------------------------------------------------------ growth machinery (copied from CFG941 cfg941.py growth_det, unchanged)
tt = sp.symbols("t", positive=True); al = sp.symbols("alpha")
C2s, Bs = sp.symbols("c_2 b", nonnegative=True)
Kg = sp.Symbol("K", positive=True)


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


P("\n  deriving the growth determinant (sympy, CFG941 route) ...")
DET2, HOM2 = growth_det([("b", FBr, False), ("t", FCr, True)])


def n2(c2, b):
    return n_from_det(DET2, {C2s: c2, Bs: b})


rss_guard("growth det")

# ------------------------------------------------------------------------------------------------ slip (CFG938 S4 definitions) with an optional vacuum (bag) term B
def slip_worst(bag_of_foot=None, foots=FOOTS):
    """worst s_grad, s_847 over CFG847's five systems (rows W, stiff24, stiff1k) on P0's static states, with p -> p + B.
    bag_of_foot(foot) -> B in J/m^3 (T_mu nu = B g_mu nu: p_r and p_t both shift by +B)."""
    worst_g = 0.0; worst_8 = 0.0; rows = {}
    for foot in foots:
        a0 = A0[foot]; B = 0.0 if bag_of_foot is None else bag_of_foot(foot)
        for name, Mb, rk_ in SYS847:
            M = Mb * MSUN847; rr = rk_ * KPC847

            def uat(x):
                gn = G_SI * M / x ** 2; g_ = law_g(gn, a0); return g_ * a0 / (g_ + a0)
            gn = G_SI * M / rr ** 2; uu = uat(rr); g_ = gn + uu
            W_ = Wfull_num(uu, a0); Dv = D_num(uu, a0)
            h_ = 1e-5 * rr
            rho_c = ((rr + h_) ** 2 * uat(rr + h_) - (rr - h_) ** 2 * uat(rr - h_)) / (2 * h_) / (K_SI * rr ** 2)
            vc2 = g_ * rr; row = {}
            for lab, Lpc in (("W", 0.0), ("stiff24", 24.0), ("stiff1k", 1000.0)):
                ps = math.pi * G_SI * (Lpc * PC) ** 2 * rho_c ** 2
                pr = -W_ + ps + B; pt = -W_ + Dv * uu / K_SI + ps + B
                sg = 4 * math.pi * G_SI * rr * abs(pr) / (C_SI ** 2 * g_)
                s8 = 8 * math.pi * G_SI * rr ** 2 * max(abs(pr), abs(pt)) / (C_SI ** 2 * vc2)
                row[lab] = (sg, s8); worst_g = max(worst_g, sg); worst_8 = max(worst_8, s8)
            rows[f"{foot}|{name}"] = row
    return worst_g, worst_8, rows


def bag_limit(foot):
    """largest bag b (in units a0^2/K of that footing) with every s_grad, s_847 <= 1.9e-5 (bisection)."""
    a0 = A0[foot]
    f = lambda b: max(slip_worst(lambda ft: b * a0 * a0 / K_SI, foots=(foot,))[:2]) - 1.9e-5
    if f(0.0) > 0:
        return 0.0
    return brentq(f, 0.0, 50.0, xtol=1e-12)


# ------------------------------------------------------------------------------------------------ CFG941's ghost grid (T1) and the edge-field variant (T2)
def ghost_grid(a0, spp, edge=False):
    out = {}
    for zt in (0.0, 1.0, 3.0):
        Krho0 = 5.55 * 1.5 * OM0 * H0_SI ** 2 * (1 + zt) ** 3
        rho0 = Krho0 / K_SI
        for Rmpc in (0.1, 1.0, 10.0):
            Rm = Rmpc * MPC
            u0 = Krho0 * Rm / 3 if edge else Krho0 * (Rm / 2) / 3
            uc = min(u0, 0.999 * a0)
            W0 = Wfull_num(uc, a0)
            kg = math.sqrt(rho0 / (spp * W0))
            out[f"z_ta={zt:g}|R={Rmpc:g}Mpc"] = dict(k_ghost_R=kg * Rm, u_over_a0=u0 / a0, W=W0, rho0=rho0, capped=u0 > 0.999 * a0)
    return out


xs_ = np.linspace(0, 1, 200001)
SPP_Q = float((-S5pp(xs_)[xs_ > 0.5]).max())                           # max of -S5'' on the upper half (CFG941: 5.7735)
SPP_MAX = SPP_Q / THETA_S ** 2

# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
k1 = {}
for foot in FOOTS:
    us, gt, ex_k1 = solve_static(GN_N, A0[foot])
    gl = np.array([law_g(x, A0[foot]) for x in GN_N])
    k1[foot] = float(np.max(np.abs(gt / gl - 1)))
P(f"  K1 reduced EL (CFG938 W_full): {sp.factor(ex_k1)}")
K1 = chk("K1_NGC3198_law_P0", all(v < 1e-6 for v in k1.values()),
         f"max |g/g_law - 1| canonical {k1['canonical']:.2e}, alt {k1['alt']:.2e} (CFG938: 2.2e-16; line 1e-6)")
RES["K1"] = k1
yy = sp.Symbol("y", positive=True)
lim_btfr = sp.limit(((yy + sp.sqrt(yy ** 2 + 4 * yy)) / 2) ** 2 / yy, yy, 0, "+")
btfr = {}
for foot in FOOTS:
    a0 = A0[foot]; y = 1e-14
    us, gt, _ = solve_static(np.array([y * a0]), a0)
    btfr[foot] = float(gt[0] ** 2 / (y * a0 * a0))
K2 = chk("K2_deep_BTFR", lim_btfr == 1 and all(abs(v - 1) < 1e-6 for v in btfr.values()),
         f"lim V^4/(G M a0) = {lim_btfr}; at y = 1e-14: canonical {btfr['canonical'] - 1:+.2e}, alt {btfr['alt'] - 1:+.2e} (line 1e-6)")
RES["K2"] = btfr
j941 = json.load(open(os.path.join(LANES, "CFG941_self_gravity_repair", "cfg941_results.json")))
n10, n11, n00 = n2(1, 0), n2(1, 1), n2(0, 0)
C2MAX_941 = brentq(lambda c_: n2(c_, 0) - 0.999, 1e-8, 0.5, xtol=1e-12)
K3 = chk("K3_growth_CFG941_route", HOM2 and abs(n10 - 0.60954) < 1e-5 and abs(n11 - 0.69433) < 1e-5 and abs(n00 - 1) < 1e-12
         and abs(C2MAX_941 / j941["D6"]["c2_max"] - 1) < 0.01,
         f"n(c2=1, no boost) = {n10:.6f} (0.60954), n(c2=1, boost) = {n11:.6f} (0.69433), n(c2=0) = {n00:.12f} (R3theta's linear regime: "
         f"gate off = dust); c2_max = {C2MAX_941:.4e} (CFG941 {j941['D6']['c2_max']:.4e})")
g941 = j941["R3theta"]["ghost"]
T1c = ghost_grid(A0["canonical"], SPP_MAX)
k4dev = max(abs(T1c[k_]["k_ghost_R"] / g941[k_]["k_ghost_R"] - 1) for k_ in g941)
K4 = chk("K4_CFG941_ghost_grid", k4dev < 1e-6 and abs(SPP_Q - 5.7735) < 1e-4,
         f"nine k_g R values reproduced, max rel dev {k4dev:.1e}; s''_max theta_s^2 = {SPP_Q:.5f} (5.7735); "
         f"k_g R range {min(v['k_ghost_R'] for v in T1c.values()):.3f}-{max(v['k_ghost_R'] for v in T1c.values()):.3f}")
wg0, w80, _ = slip_worst()
K5 = chk("K5_CFG938_slip", abs(w80 / 1.539799903790011e-05 - 1) < 0.02, f"worst s_847 = {w80:.4e} (CFG938 1.5398e-5), s_grad = {wg0:.3e}")
# K6 + G1: exact second variation of J F(Jdot/J)
Jq, Jd, J0q, th0, eA, eB, ep = sp.symbols("J Jd J_0 theta_0 dJ dJd epsilon")
Ff = sp.Function("F")
E = Jq * Ff(Jd / Jq)
E2 = sp.diff(E.subs({Jq: J0q + ep * eA, Jd: th0 * J0q + ep * eB}), ep, 2).subs(ep, 0) / 2
Fpp = sp.Subs(sp.Derivative(Ff(sp.Symbol("q")), sp.Symbol("q"), 2), sp.Symbol("q"), th0)
target_G1 = Fpp / (2 * J0q) * (eB - th0 * eA) ** 2
G1_ok = is0(sp.simplify(E2.doit() - target_G1.doit()))
ssym = sp.Function("s"); Wsym = sp.Symbol("W", positive=True)
E2_R3 = sp.diff((Jq * (-ssym(Jd / Jq) * Wsym)).subs({Jq: J0q + ep * eA, Jd: 0 * J0q + ep * eB}), ep, 2).subs(ep, 0) / 2
s2_0 = sp.Subs(sp.Derivative(ssym(sp.Symbol("q")), sp.Symbol("q"), 2), sp.Symbol("q"), 0)
dv = sp.Symbol("divv")
K6 = chk("K6_G1_reproduces_CFG941_kinetic_term", G1_ok and is0(sp.simplify((E2_R3.doit() - (-s2_0 * Wsym / (2 * J0q)) * eB ** 2).doit()))
         and is0(sp.simplify(((-s2_0 * Wsym / (2 * J0q)) * (J0q * dv) ** 2 / J0q - (-s2_0 * Wsym / 2) * dv ** 2).doit())),
         "second variation of J F(Jdot/J) = (F''(theta0)/2J0)(dJdot - theta0 dJ)^2 exactly (G1); at theta0 = 0 with F = -s W and "
         "dJdot = J0 div v it is -(1/2) s''(0) W (div v)^2 per unit volume = CFG941's R3theta_kinetic_term")
K_ALL = K1 and K2 and K3 and K4 and K5 and K6
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> VOID'}")
RES["K_all"] = K_ALL
if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB"); sys.exit(0 if K_ALL else 1)
rss_guard("K")

# ================================================================================================ shared main machinery
# ---- native linear amplitude U(z) (CFG654 A1 primary table; amplitude only)
TAB = np.load(os.path.join(LANES, "CFG654_independent_inputs", "cfg654_ics_tables_cmb.npz"), allow_pickle=False)
h_t = float(TAB["h"]); Om_t = (float(TAB["omega_b"]) + float(TAB["omega_c"])) / h_t ** 2; fc_t = float(TAB["omega_c"]) / (float(TAB["omega_b"]) + float(TAB["omega_c"]))
H0_t = 100e3 * h_t / MPC; zi_t = float(TAB["zi"])
kh_t, Pzi_t = TAB["kh"], TAB["P_zi"]
sel_ = (kh_t >= 0.01) & (kh_t <= 5.0)
I_zi = float(np.trapz(Pzi_t[sel_], kh_t[sel_]) / (2 * math.pi ** 2)) * (MPC / h_t) ** 2          # m^2 (z_i)
I_phi = float(np.trapz(Pzi_t[sel_] / kh_t[sel_] ** 2, kh_t[sel_]) / (2 * math.pi ** 2)) * (MPC / h_t) ** 4   # m^4 (z_i)
lnD_of = lambda lna: float(np.interp(lna, TAB["lna"], TAB["lnD"]))
D_zi = math.exp(lnD_of(-math.log(1 + zi_t)))


def U_of_z(z):
    """1-sigma medium field (m/s^2) of linear perturbations, k in [0.01, 5] h/Mpc (the medium's share f_c; D5 boost omitted)."""
    Dz = math.exp(lnD_of(-math.log(1 + z)))
    return fc_t * 1.5 * H0_t ** 2 * Om_t * (1 + z) ** 2 * math.sqrt(I_zi) * Dz / D_zi


ZG = np.concatenate((np.linspace(0, 10, 101), np.geomspace(10.5, 1100, 400)))
UZ = np.array([U_of_z(z) for z in ZG])
U_MAX = float(UZ.max())

# ---- transition sets T1 (CFG941, u at R/2), T2 (edge field), T3 (NGC 3198 interior)
SETS = {}
for foot in FOOTS:
    a0 = A0[foot]
    uN, rhoN, WN, glN = ngc_states(a0)
    SETS[foot] = dict(T1=ghost_grid(a0, SPP_MAX), T2=ghost_grid(a0, SPP_MAX, edge=True),
                      T3=dict(u=uN, rho=rhoN, W=WN, kg_r=np.sqrt(rhoN / (SPP_MAX * WN)) * R_N))


def Wmax_set(foot, name):
    s_ = SETS[foot][name]
    return float(max(v["W"] for v in s_.values())) if name != "T3" else float(SETS[foot]["T3"]["W"].max())


TESTS = {}


def put(cure, key, ok, detail):
    TESTS.setdefault(cure, {})[key] = dict(pass_=(bool(ok) if ok is not None else None), detail=str(detail))
    tag = "PASS" if ok else ("FAIL" if ok is not None else "N/A ")
    P(f"   ({key}) {tag}: {detail}")


def c4_build(uc, a0, Wg_scale=1.0, sat=True):
    """C4 pieces for a given u_c: h(u), W_g = max_{u <= u_c} (1 - h) W, and F_thth theta_s^2 on a grid."""
    hfun = (lambda uu: S5(np.clip(2 * uu / uc - 1, 0, 1))) if sat else (lambda uu: np.zeros_like(uu))
    ug = np.linspace(0, min(uc, 0.999999 * a0), 4001)
    Wg = float(np.max((1 - hfun(ug)) * np.array([Wfull_num(x, a0) for x in ug])))
    return hfun, Wg * Wg_scale, Wg


def c4_Fthth_min(uc, a0, Wg, hfun, ugrid=None, xgrid=None):
    """min over (x, u) of F_thth theta_s^2 = 60 x (1-x) W_g + S5''(x) (1 - h(u)) W(u); relative to W-scale a0^2/K."""
    xg = np.linspace(1e-4, 1 - 1e-4, 801) if xgrid is None else xgrid
    ug = np.concatenate((np.linspace(0, 0.999 * a0, 1500), a0 * (1 - np.geomspace(1e-3, 1e-9, 60)))) if ugrid is None else ugrid
    Wv = np.array([Wfull_num(x, a0) for x in ug]); hv = hfun(ug)
    F = 60 * xg[:, None] * (1 - xg[:, None]) * Wg + S5pp(xg)[:, None] * ((1 - hv) * Wv)[None, :]
    i, j = np.unravel_index(np.argmin(F), F.shape)
    return float(F.min() / (a0 * a0 / K_SI)), float(xg[i]), float(ug[j] / a0)


def omega2(k, rho0, u0, a0, s0, Fthth, th0, gam_eff, ang=0.0):
    """frozen-coefficient WKB (G3): (rho0 + F k^2) w^2 = rho0 W2_P0(k; s0) - F k^2 theta0^2."""
    W2 = gam_eff * rho0 * k ** 2 + K_SI * rho0 * (s0 * (Dp_num(u0, a0) * math.cos(ang) ** 2 + D_num(u0, a0) / u0 * math.sin(ang) ** 2) - 1)
    return (rho0 * W2 - Fthth * k ** 2 * th0 ** 2) / (rho0 + Fthth * k ** 2)


# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    teeth = {}
    a0 = A0["canonical"]
    # M1: C4 with the cure removed -> R3theta's ghost (F_thth = S5'' W < 0 on the upper half)
    h0 = lambda uu: np.zeros_like(uu)
    m1, _, _ = c4_Fthth_min(0.3 * a0, a0, 0.0, h0)
    teeth["M1_C4_cure_removed"] = (m1 < 0, f"min F_thth theta_s^2 = {m1:.3e} a0^2/K < 0 (ghost back); T1 k_g R finite: "
                                   f"{min(v['k_ghost_R'] for v in T1c.values()):.3f}-{max(v['k_ghost_R'] for v in T1c.values()):.3f}")
    # M1b: C1 with c_theta = 0 -> the same kinetic coefficient rho0 - s'' W k^2
    teeth["M1b_C1_c_theta_zero"] = (all(math.isfinite(v["k_ghost_R"]) for v in T1c.values()), "c_theta = 0: kinetic coefficient rho0 - s''W k^2, k_g finite on all nine T1 states")
    # M2: C1 at half its T1 ghost bound
    cg = SPP_MAX * Wmax_set("canonical", "T1")
    worst = min(0.5 * cg - SPP_MAX * v["W"] for v in T1c.values())
    teeth["M2_C1_below_bound"] = (worst < 0, f"c_theta = c_theta,g/2 = {0.5 * cg:.3e} kg/m: min (c_theta - s''_max W) on T1 = {worst:.3e} < 0 -> ghost band remains")
    # M3: C4 with W_g halved
    uc = 0.3 * a0; hf, Wg, _ = c4_build(uc, a0)
    m3, x3, u3 = c4_Fthth_min(uc, a0, 0.5 * Wg, hf)
    teeth["M3_C4_half_bag"] = (m3 < 0, f"u_c = 0.3 a0, W_g/2: min F_thth theta_s^2 = {m3:.3e} a0^2/K at x = {x3:.3f}, u/a0 = {u3:.3f}")
    # M4: C4 without the u-saturation at its own W_g
    m4, x4, u4 = c4_Fthth_min(uc, a0, Wg, h0)
    teeth["M4_C4_no_saturation"] = (m4 < 0, f"h = 0, W_g kept: min F_thth theta_s^2 = {m4:.3e} a0^2/K at u/a0 = {u4:.4f} (W(u) > W_g)")
    # M5: amplitude tooth -- with U = 0 the C4 window opens (some u_c passes (c-amp) and (e))
    be = bag_limit("canonical")
    ucs = np.linspace(0.02, 0.98, 49) * a0
    ok_u = [x for x in ucs if 5 * c4_build(x, a0)[1] <= be * a0 * a0 / K_SI]
    teeth["M5_amplitude_tooth"] = (len(ok_u) > 0, f"U = 0: (c-amp) trivially passes; (e) admits u_c up to {max(ok_u) / a0 if ok_u else float('nan'):.2f} a0 "
                                   f"(bag 5 W_g <= B_e = {be:.4f} a0^2/K): window OPENS -> (c-amp) is what closes it")
    # M6: Theorem G tooth -- with no static-law constraint at u > 0, B_min = W(0) = 0 <= B_e
    teeth["M6_theoremG_tooth"] = (Wfull_num(0.0, a0) <= be * a0 * a0 / K_SI, f"u* -> 0: B_min = W(0) = 0 <= B_e = {be:.4f} a0^2/K (the bound bites only through (a))")
    for k_, (ok, det) in teeth.items():
        chk(k_, ok, det)
    RES["MUTATE"] = {k_: dict(bites=bool(v[0]), detail=v[1]) for k_, v in teeth.items()}
    allbite = all(v[0] for v in teeth.values())
    P(f"\n  MUTATE: {'ALL TEETH BITE (exit 1 by design)' if allbite else 'A TOOTH FAILED TO BITE'}")
    dump(); sys.exit(1 if allbite else 2)

# ================================================================================================ 1. GHOST RE-DERIVATION
P("\n==================== 1. GHOST RE-DERIVATION (G1-G5) ====================")
chk("G1_rank_one_second_variation", G1_ok, "J F(Jdot/J) is degree-1 homogeneous in (J, Jdot): its Hessian is (F''/J)(-theta, 1)(-theta, 1)^T, "
    "so the second variation is (F''(theta0)/2J0)(dJdot - theta0 dJ)^2 for ANY F(theta) (u held fixed)")
# G2: second-order part of J for one Fourier mode is zero; in general a divergence
q1, q2, q3, Aq, k1s, k2s, k3s, e1, e2, e3 = sp.symbols("q1 q2 q3 A k1 k2 k3 e1 e2 e3", real=True)
qv = [q1, q2, q3]; ph_ = k1s * q1 + k2s * q2 + k3s * q3
xi = [Aq * e * sp.cos(ph_) for e in (e1, e2, e3)]
Jm = sp.Matrix(3, 3, lambda i, j: (1 if i == j else 0) + sp.diff(xi[i], qv[j]))
J2 = sp.expand(sp.series(Jm.det().subs(Aq, ep * Aq), ep, 0, 3).removeO().coeff(ep, 2))
xg = [sp.Function(f"xi{i}")(q1, q2, q3) for i in range(3)]
divx = sum(sp.diff(xg[i], qv[i]) for i in range(3))
J2gen = (divx ** 2 - sum(sp.diff(xg[i], qv[j]) * sp.diff(xg[j], qv[i]) for i in range(3) for j in range(3))) / 2
divform = sum(sp.diff(xg[i] * divx - sum(xg[j] * sp.diff(xg[i], qv[j]) for j in range(3)), qv[i]) for i in range(3)) / 2
chk("G2_single_mode_J2_vanishes", is0(J2) and is0(sp.expand(J2gen - divform)),
    "second-order part of J = det(I + grad xi) is (1/2)[(div xi)^2 - d_i xi_j d_j xi_i] = (1/2) div(xi div xi - xi.grad xi) in general, and "
    "identically 0 for a single plane wave of any polarization -> the longitudinal kinetic coefficient is exactly rho0 + F_thth k^2 "
    "(transverse: rho0); for R3theta F_thth = -s''(theta) W(u): ghost iff s'' W k^2 > rho0")
# G3: frozen-coefficient dispersion about an NGC 3198 transition state (mid radius, theta0 = 0.8 theta_s)
g3 = {}
for foot in FOOTS:
    a0 = A0[foot]; T3 = SETS[foot]["T3"]; i = len(R_N) // 2
    rho0, u0, W0 = float(T3["rho"][i]), float(T3["u"][i]), float(T3["W"][i])
    x0 = 0.8; s0 = 1 - float(S5(x0)); spp0 = -float(S5pp(x0)) / THETA_S ** 2; F = -spp0 * W0
    kg = math.sqrt(rho0 / (spp0 * W0))
    for Lpc in (24.0, 1000.0):
        gm = 2 * math.pi * G_SI * (Lpc * PC) ** 2
        vals = [omega2(kg * (1 + sg_ * 10.0 ** -j), rho0, u0, a0, s0, F, x0 * THETA_S, s0 * gm) for j in range(1, 9) for sg_ in (1, -1)]
        far = omega2(kg * 1e4, rho0, u0, a0, s0, F, x0 * THETA_S, s0 * gm)
        g3[f"{foot}|L*={Lpc:g}pc"] = dict(k_g_r=kg * R_N[i], w2_near=vals, w2_far=far, Krho=K_SI * rho0)
g3_ok = all(min(v["w2_near"]) < -1e5 * v["Krho"] and abs(v["w2_near"][-1]) > 1e5 * abs(v["w2_near"][1]) for v in g3.values())
k_ = list(g3.keys())[0]
chk("G3_degenerate_kinetic_surface", g3_ok,
    f"R3theta at NGC 3198 r = {R_N[len(R_N) // 2] / KPC:.1f} kpc, theta0 = 0.8 theta_s: k_g r = {g3[k_]['k_g_r']:.3e}; "
    f"omega^2/(K rho0) at k = k_g(1 -/+ 1e-1): {g3[k_]['w2_near'][1] / g3[k_]['Krho']:.2e} / {g3[k_]['w2_near'][0] / g3[k_]['Krho']:.2e}; at k_g(1 -/+ 1e-8): "
    f"{g3[k_]['w2_near'][-1] / g3[k_]['Krho']:.2e} / {g3[k_]['w2_near'][-2] / g3[k_]['Krho']:.2e} "
    "(omega^2 ~ C/(k - k_g): -> -infinity as k -> k_g from below, where the inertia rho0 + F k^2 vanishes against the gated-off self-gravity, and "
    "negative-energy oscillation above): omega^2 is NOT bounded below independently of k (the gyroscopic F_thu terms are O(k) and cannot cancel the pole)")
RES["G3"] = g3
P("  G4 = K4 (CFG941 grid reproduced). G5 transition states reached from settled galaxies:")
for foot in FOOTS:
    T3 = SETS[foot]["T3"]
    P(f"   [{foot}] NGC 3198 interior: k_g r = {T3['kg_r'].min():.2e} ... {T3['kg_r'].max():.2e} (all << 1: the ghost band covers every galactic scale); "
      f"u/a0 = {T3['u'].min() / A0[foot]:.3f} ... {T3['u'].max() / A0[foot]:.3f}; T2 (edge field) k_g R = "
      f"{min(v['k_ghost_R'] for v in SETS[foot]['T2'].values()):.3f}-{max(v['k_ghost_R'] for v in SETS[foot]['T2'].values()):.3f}")
G5_ok = all(SETS[f]["T3"]["kg_r"].max() < 1 for f in FOOTS)
chk("G5_galaxy_interior_ghost", G5_ok, "every NGC 3198 radius, perturbed into the convex half of the gate (theta in (theta_s/2, theta_s), i.e. "
    "|div v| ~ 1e-18 1/s, far below galactic rates), carries a ghost band starting at k_g << 1/r")
RES["G5"] = {f: dict(kg_r_min=float(SETS[f]["T3"]["kg_r"].min()), kg_r_max=float(SETS[f]["T3"]["kg_r"].max()),
                     u_over_a0_max=float(SETS[f]["T3"]["u"].max() / A0[f])) for f in FOOTS}
rss_guard("G")

# ================================================================================================ native amplitude
P("\n==================== native linear amplitude U(z) (CFG654 A1 table; amplitude only) ====================")
z_cross = {}
for foot in FOOTS:
    a0 = A0[foot]; uNmax = float(SETS[foot]["T3"]["u"].max())
    zx = float(ZG[np.argmax(UZ >= uNmax)]) if (UZ >= uNmax).any() else float("nan")
    za = float(ZG[np.argmax(UZ >= a0)]) if (UZ >= a0).any() else float("nan")
    z_cross[foot] = dict(z_U_eq_uNmax=zx, z_U_eq_a0=za, U0_over_a0=UZ[0] / a0, U1100_over_a0=U_of_z(1100.0) / a0)
    P(f"   [{foot}] U(0) = {UZ[0] / a0:.4f} a0; U(100) = {U_of_z(100) / a0:.3f} a0; U(1100) = {U_of_z(1100) / a0:.2f} a0; "
      f"U >= u_N,max ({uNmax / a0:.3f} a0) for z >= {zx:.0f}; U >= a0 for z >= {za:.0f}")
chk("AMP_native_table_sane", 0.001 < UZ[0] / A0["canonical"] < 0.05 and np.all(np.diff(UZ[ZG > 20]) > 0),
    f"U(0) = {UZ[0]:.3e} m/s^2 = {UZ[0] / A0['canonical']:.4f} a0 (canonical); U rises monotonically above z = 20 (~(1+z)); "
    f"table h = {h_t:.4f}, Omega_m = {Om_t:.4f}, f_c = {fc_t:.4f}, D(z_i)/D(1) = {D_zi:.5f}")
RES["amplitude"] = dict(U_max_over_a0={f: U_MAX / A0[f] for f in FOOTS}, crossings=z_cross,
                        U_z=[(float(z), float(v)) for z, v in zip(ZG[::25], UZ[::25])])
P(f"  SIDE FLAG (estimate, not graded): P0's always-on tether argument u reaches W_full's wall u = a0 at z >= "
  f"{z_cross['canonical']['z_U_eq_a0']:.0f} / {z_cross['alt']['z_U_eq_a0']:.0f} on typical (1-sigma) points; CFG941's quadratic-action "
  "exponents for P0 assume u << a0. Gated theories avoid the wall only because s = 0 exactly there. CFG938/941 not edited.")

# ================================================================================================ 2. C1: aether-like term, always on
P("\n==================== C1: +(c_theta/2) theta^2, always on ====================")
tq = sp.Symbol("t", real=True); cc, Gs, cth, rho0s = sp.symbols("c G c_theta rho_0", positive=True)
Nf = sp.Function("N", positive=True)(tq); af = sp.Function("a", positive=True)(tq)
Xs = [tq] + list(sp.symbols("x y z", real=True))
gmet = sp.diag(-Nf ** 2 * cc ** 2, af ** 2, af ** 2, af ** 2); gin = gmet.inv()
Gam = [[[sum(gin[a_, d_] * (sp.diff(gmet[d_, b_], Xs[c_]) + sp.diff(gmet[d_, c_], Xs[b_]) - sp.diff(gmet[b_, c_], Xs[d_])) for d_ in range(4)) / 2
         for c_ in range(4)] for b_ in range(4)] for a_ in range(4)]
Ric = sp.zeros(4, 4)
for b_ in range(4):
    for c_ in range(4):
        Ric[b_, c_] = sp.simplify(sum(sp.diff(Gam[a_][b_][c_], Xs[a_]) - sp.diff(Gam[a_][b_][a_], Xs[c_])
                                      + sum(Gam[a_][a_][d_] * Gam[d_][b_][c_] - Gam[a_][c_][d_] * Gam[d_][b_][a_] for d_ in range(4)) for a_ in range(4)))
Rs = sp.simplify(sum(gin[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
sqg = Nf * cc * af ** 3
ad = sp.diff(af, tq)
c1_ibp = is0(sp.simplify(sqg * Rs + 6 * af * ad ** 2 / (Nf * cc) - (6 / cc) * sp.diff(af ** 2 * ad / Nf, tq)))
theta_frw = sp.simplify(sp.diff(sqg * (1 / Nf), tq) / sqg)
As_, Ads_, Ns_ = sp.symbols("A Adot N_l", positive=True)
form_ok = is0(sp.simplify(sqg * (cth / 2) * theta_frw ** 2 - sp.Rational(9, 2) * cth * cc * af * ad ** 2 / Nf))
Lmini = -(3 * cc ** 3 / (8 * sp.pi * Gs)) * As_ * Ads_ ** 2 / Ns_ + sp.Rational(9, 2) * cth * cc * As_ * Ads_ ** 2 / Ns_ - rho0s * cc ** 3 * Ns_
hamc = sp.diff(Lmini, Ns_).subs(Ns_, 1)
Ad_sol = sp.solve(hamc, Ads_)[0]
H2 = sp.simplify(Ad_sol ** 2 / As_ ** 2)
Gcos_ratio = sp.simplify(H2 / (8 * sp.pi * Gs * rho0s / (3 * As_ ** 3)))
c2ae = -8 * sp.pi * Gs * cth / cc ** 2
t0s = sp.Symbol("t_0", positive=True)
Lfun = Lmini.subs({As_: af, Ads_: ad, Ns_: 1})
ELa = sp.euler_equations(Lfun, [af], [tq])[0].lhs
asol = (tq / t0s) ** sp.Rational(2, 3)
rho_needed = sp.solve(sp.Eq(hamc.subs({As_: asol, Ads_: sp.diff(asol, tq)}), 0), rho0s)[0]
ELa_on = sp.simplify(ELa.subs(af, asol).doit().subs(rho0s, rho_needed))
chk("C1_G_cosmo", c1_ibp and form_ok and is0(theta_frw - 3 * ad / (Nf * af)) and is0(Gcos_ratio - 1 / (1 - 12 * sp.pi * Gs * cth / cc ** 2))
    and is0(sp.simplify(1 / (1 + 3 * c2ae / 2) - Gcos_ratio)) and ELa_on == 0,
    f"sqrt(-g) R = -6 a adot^2/(N c) + total derivative; theta_FRW = 3 adot/(N a); Friedmann: H^2 = (8 pi G rho/3) * {sp.factor(Gcos_ratio)} "
    "-> G_cosmo/G_N = 1/(1 - 12 pi G c_theta/c^2) (= Einstein-aether 1/(1 + 3 c2/2) with c2 = -8 pi G c_theta/c^2); the a-equation is solved "
    "by the same dust history (a pure G renormalisation, eps_theta = (9/2) c_theta H^2 tracks H^2); static states have theta = 0, so G_N = G")
P("  (positive kinetic energy for the medium, c_theta > 0, RAISES G_cosmo; 12 pi G c_theta/c^2 -> 1 removes the scale factor's kinetic term)")
c1 = {}
for foot in FOOTS:
    a0 = A0[foot]
    for name in ("T1", "T2", "T3"):
        cg = SPP_MAX * Wmax_set(foot, name)
        c1[f"{foot}|{name}"] = dict(c_theta_g=cg, eps=12 * math.pi * G_SI * cg / C_SI ** 2)


def growth_c1(c_theta, k_hMpc, z_start=1100.0):
    """two-component EdS growth with medium inertia rho_c (1 + r), r = c_theta k_phys^2/rho_c, background G_cosmo = G/eps:
    (1+r) psi_c'' + ((1+r)/2 + r) psi_c' = (3/2) eps (f_b psi_b + f_c psi_c);  psi_b'' + psi_b'/2 = (3/2) eps (f_b psi_b + f_c psi_c)."""
    eps = 1 - 12 * math.pi * G_SI * c_theta / C_SI ** 2
    if eps <= 0:
        return float("-inf"), eps
    kc = k_hMpc * HLIT / MPC
    rho_c0 = FC * eps * RHO_CRIT                                           # EdS-consistent background (favourable to C1)
    r0 = c_theta * kc ** 2 / rho_c0
    n0 = (-0.5 + math.sqrt(0.25 + 6 * eps)) / 2

    def rhs(x, y):
        rr = r0 * math.exp(x); src = 1.5 * eps * (FB * y[0] + FC * y[2])
        return [y[1], src - 0.5 * y[1], y[3], (src - ((1 + rr) / 2 + rr) * y[3]) / (1 + rr)]
    x0 = -math.log(1 + z_start)
    sol = solve_ivp(rhs, (x0, 0.0), [1.0, n0, 1.0, n0], method="LSODA", rtol=1e-10, atol=1e-13, dense_output=True)
    xs = np.linspace(x0, 0.0, 600); yv = sol.sol(xs)
    nloc = yv[3] / yv[2]
    return float(nloc.min()), eps


f_lim = lambda lc: growth_c1(10 ** lc, 5.0)[0] - 0.999
lc_max = brentq(f_lim, 0.0, 22.0, xtol=1e-6)
c_theta_max = 10 ** lc_max
n_at_max_small_k = growth_c1(c_theta_max, 0.01)[0]
P(f"  growth window (c): min_z n >= 0.999 at k = 5 h/Mpc needs c_theta <= {c_theta_max:.3e} kg/m "
  f"(r(z=0, k=5) = {c_theta_max * (5 * HLIT / MPC) ** 2 / (FC * RHO_CRIT):.2e}; G_cosmo shift {12 * math.pi * G_SI * c_theta_max / C_SI ** 2:.1e}); "
  f"at that c_theta, k = 0.01 h/Mpc gives n_min = {n_at_max_small_k:.6f}")
for k_, v in c1.items():
    ng5, eps5 = growth_c1(v["c_theta_g"], 5.0); ng01, _ = growth_c1(v["c_theta_g"], 0.01)
    v.update(n_min_k5=ng5, n_min_k001=ng01, ratio_to_growth_max=v["c_theta_g"] / c_theta_max)
    P(f"   {k_:15s} ghost bound c_theta,g = {v['c_theta_g']:.3e} kg/m (x{v['ratio_to_growth_max']:.2e} the growth maximum); "
      f"12 pi G c_theta/c^2 = {v['eps']:.3e}" + (f" -> G_cosmo/G = {1 / (1 - v['eps']):.4f}" if v['eps'] < 1 else " >= 1: NO Friedmann branch (scale-factor ghost)")
      + f"; n_min(k=5) = {ng5:.4f}, n_min(k=0.01) = {ng01:.4f}")
u_flip = {}
for foot in FOOTS:
    a0 = A0[foot]
    u_flip[foot] = brentq(lambda x: 12 * math.pi * G_SI * SPP_MAX * Wfull_num(x * a0, a0) / C_SI ** 2 - 1, 1e-6, 1 - 1e-12)
P(f"  the T-set ghost bound reaches 12 pi G c_theta/c^2 = 1 (no Friedmann branch) for transition states with u >= {u_flip['canonical']:.4f} a0 "
  f"(canonical), {u_flip['alt']:.4f} a0 (alt)")
uc_cover = {}
for foot in FOOTS:
    a0 = A0[foot]; Wc = c_theta_max / SPP_MAX
    uc_cover[foot] = brentq(lambda x: Wfull_num(x * a0, a0) - Wc, 1e-12, 0.999999) if Wc < Wfull_num(0.999999 * a0, a0) else 1.0
P(f"  at the growth maximum, (d) holds only where W(u) <= c_theta,max/s''_max: u <= {uc_cover['canonical']:.2e} a0 (canonical), "
  f"{uc_cover['alt']:.2e} a0 (alt) -- smaller than every T1 state (u/a0 >= 6.8e-5 / 5.7e-5)")
RES["C1"] = dict(c_theta_growth_max=c_theta_max, sets=c1, u_cover_over_a0=uc_cover, u_flip_over_a0=u_flip)
put("C1", "a", K1 and K2, "static states have theta = 0: (c_theta/2) theta^2 and its first variation vanish -> P0's static law (K1 2.2e-16, BTFR K2)")
put("C1", "b", True, "T^mu_nu isotropic, medium dust w = 0; the cure adds eps_theta = (9/2) c_theta H^2 (a G_cosmo renormalisation, C1_G_cosmo): the cost")
put("C1", "c", c1['canonical|T1']['n_min_k5'] >= 0.999, f"(c) needs c_theta <= {c_theta_max:.2e} kg/m (inertia c_theta k_phys^2 vs rho_c, worst at k = 5 h/Mpc, z = 0); every ghost bound "
    f"on T1-T3 exceeds it by x{min(v['ratio_to_growth_max'] for v in c1.values()):.1e} - x{max(v['ratio_to_growth_max'] for v in c1.values()):.1e}: "
    f"at c_theta,g(T1) n_min(k=5) = {c1['canonical|T1']['n_min_k5']:.3f}")
put("C1", "c-amp", None, "theta-only cure: (c-amp) = (c)")
put("C1", "d", uc_cover['canonical'] >= 1.0 and uc_cover['alt'] >= 1.0, "ghost-free iff c_theta >= s''(theta) W(u) on every transition state; W_full -> infinity as u -> a0, so no finite c_theta is "
    f"global; exact region u <= W^-1(c_theta/s''_max); at the growth maximum it covers u <= {uc_cover['canonical']:.1e} a0, no T1-T3 state")
put("C1", "e", w80 <= 1.9e-5, f"theta = 0 on static states: slip = P0's (worst s_847 {w80:.2e})")
put("C1", "g", False, "settled sector unchanged (P0 + an inert theta^2): g1, g2 fail; see section g")
rss_guard("C1")

# ================================================================================================ 3. C2: gates on non-derivative variables
P("\n==================== C2: gates on non-derivative variables (rho, chi, latch / clock-density) ====================")
rho0c, drs, dus, W0s, s0c, s1c, s2c, Wd1, Wd2 = sp.symbols("rho0 drho du W0 s0 s1 s2 W1 W2")
sexp = s0c + s1c * drs + s2c * drs ** 2 / 2; Wexp = W0s + Wd1 * dus + Wd2 * dus ** 2 / 2
Lgate = -sexp * Wexp - sexp * gam / 2 * drs ** 2
V2c = sp.expand(-Lgate).coeff(drs, 2).subs(dus, 0)
chk("C2i_density_gate_structure", is0(V2c - (s2c * W0s / 2 + s0c * gam / 2)),
    "s(rho) multiplies W: the gate's curvature enters the POTENTIAL, (s'' W + s gamma) drho^2/2 with drho ~ k xi, so c_eff^2 = rho0 (s'' W + s gamma): "
    "the theta-ghost becomes a gradient instability wherever s is concave in rho and W > s gamma/|s''| (W unbounded); same convexity "
    "obstruction in a different variable (a bounded increasing gate saturating at 1 is concave near the top)")
r3n = j941["R3n"]
P(f"   CFG941 R3n (read): r_* = {r3n['canonical']['r_star_kpc']:.0f} / {r3n['alt']['r_star_kpc']:.0f} kpc (BTFR limit 0: (a) FAILS); gate on for the cosmic "
  f"mean at z > {r3n['canonical']['z_on']:.1f} / {r3n['alt']['z_on']:.1f} ((c) FAILS); min c_eff^2/(s gamma rho) = "
  f"{min(min(v['ceff_ratio_min'].values()) for v in r3n.values()):.2e} ((d) FAILS)")
# (ii) chi gate: the chi equation picks up s'(chi) W
xx = sp.Symbol("x", real=True)
chif, lamf, rhof = sp.Function("chi")(xx), sp.Function("lam")(xx), sp.Function("rho")(xx)
sf = sp.Function("s"); Wf_ = sp.Function("W")
Lchi = -sf(chif) * Wf_(sp.diff(chif, xx)) + lamf * (sp.diff(chif, xx, 2) - KS * rhof)
ELchi = sp.euler_equations(Lchi, [chif], [xx])[0].lhs
extra = sp.simplify(sp.diff(Lchi, chif))
extra_in_EL = sp.simplify(ELchi - extra) != ELchi
sigma_phi = fc_t * 1.5 * H0_t ** 2 * Om_t * math.sqrt(I_phi) * math.exp(lnD_of(0.0)) / D_zi
uN_c, rhoN_c, WN_c, glN_c = ngc_states(A0["canonical"])
well = float(np.trapz(glN_c, R_N))
drift = OC * C_SI ** 2 / 2
P(f"   chi: rms linear medium potential today {sigma_phi:.2e} m^2/s^2 = {sigma_phi / C_SI ** 2:.1e} c^2; NGC 3198 well across its radii "
  f"{well:.2e} = {well / C_SI ** 2:.1e} c^2; background drift per Hubble time |chibar'|/H = Omega_c c^2/2 = {drift / C_SI ** 2:.3f} c^2")
chk("C2ii_chi_gate", sp.simplify(extra) != 0 and sigma_phi > well,
    f"s(chi) adds {sp.simplify(extra)} to chi's Euler-Lagrange equation (breaks the static law unless s' = 0 on every static chi; chi's shift "
    f"symmetry is broken); the linear potential ({sigma_phi / C_SI ** 2:.1e} c^2) exceeds the galaxy's whole well ({well / C_SI ** 2:.1e} c^2) and "
    "chibar drifts by 0.13 c^2 per Hubble time: a chi threshold cannot separate collapsed from linear regions (it is a cosmic-epoch switch)")
# (iii) latch via a multiplier
dl_, ds_, dth_, lb_, Fs_, Ft_, Fss, Ftt, Fts = sp.symbols("dlam dsig dth lambar F_s F_t F_ss F_tt F_ts")
Lq = -lb_ * (Fss * ds_ ** 2 / 2 + Fts * ds_ * dth_ + Ftt * dth_ ** 2 / 2) - dl_ * (Fs_ * ds_ + Ft_ * dth_)
Hq = -Lq
Hess = sp.Matrix([[sp.diff(Hq, a_, b_) for b_ in (ds_, dl_)] for a_ in (ds_, dl_)])
tau_ = sp.Symbol("tau"); nfun = sp.Function("n", positive=True)(tau_); sgf = sp.Function("sigma")(tau_); alf = sp.Function("alpha")
ident = sp.simplify(sp.diff(sp.integrate(1 / alf(sp.Symbol("v")), (sp.Symbol("v"), 0, sgf)) + sp.log(nfun), tau_).subs(
    sp.diff(sgf, tau_), alf(sgf) * (-sp.diff(nfun, tau_) / nfun)))
Tt, rhoE = sp.symbols("T rho_E", positive=True)
Y_eds = sp.simplify(KS * (1 / (6 * sp.pi * G * Tt ** 2)) * Tt ** 2)
T_age = 2 / (3 * H0_SI)
YN = K_SI * rhoN_c * T_age ** 2
gm24 = 2 * math.pi * G_SI * (24 * PC) ** 2; gm1k = 2 * math.pi * G_SI * (1000 * PC) ** 2
dY_need = {lab: float(np.sqrt(SPP_Q * WN_c[-1] * K_SI ** 2 * T_age ** 4 / (0.9 * gmv))) for lab, gmv in (("24pc", gm24), ("1kpc", gm1k))}
dY_avail = float(YN.min() - 2.0 / 3.0)
chk("C2iii_latch_and_clock_density", is0(sp.diff(Lq, dth_, 2) + lb_ * Ftt) and is0(Hess.det() + Fs_ ** 2) and is0(ident) and is0(Y_eds - sp.Rational(2, 3))
    and all(v > dY_avail for v in dY_need.values()),
    "latch lambda(u.d sigma - F(theta, sigma)): theta^2 coefficient -lambar F_thth (the ghost returns with a multiplier-set sign) and the "
    "(dsigma, dlambda) Hamiltonian Hessian has det = -F_s^2 < 0 (linear in the multiplier momentum: unbounded); F linear in theta makes "
    "int dsigma/alpha + ln n conserved along the flow, i.e. a density/label gate (R3n/R2). Clock-density Y = K rho T^2 = 2/3 on the EdS mean "
    f"(a good turnaround label) but it is a density gate: deep-BTFR (a) fails as R3n, and drho ~ k makes s_YY W K^2 T^4 rho0 k^2 a gradient term; "
    f"stability needs a transition width dY >= {dY_need['24pc']:.1e} (L* 24 pc) / {dY_need['1kpc']:.1e} (1 kpc) vs the available "
    f"{dY_avail:.1e} (NGC 3198's lowest Y minus 2/3)")
RES["C2"] = dict(sigma_phi_over_c2=sigma_phi / C_SI ** 2, well_over_c2=well / C_SI ** 2, dY_need=dY_need, dY_avail=dY_avail,
                 R3n_from_CFG941={f: dict(r_star_kpc=r3n[f]["r_star_kpc"], z_on=r3n[f]["z_on"]) for f in FOOTS})
for lab, why in (("C2i", "density gate = R3n: (a) FAIL (BTFR, r_* = 73 kpc), (c) FAIL (on at z > 18), (d) FAIL (gradient instability)"),
                 ("C2ii", "chi gate: breaks chi's shift symmetry; static law changed unless s' = 0 on all static chi; cannot separate collapsed from linear"),
                 ("C2iii", "latch: lambar F_thth ghost or a density/label gate; clock-density Y: (a) FAIL (BTFR, as R3n) and (d) FAIL (width x"
                           f"{min(dY_need.values()) / dY_avail:.0e} too small)")):
    put(lab, "class-reason", False, why)
rss_guard("C2")

# ================================================================================================ 4. C3: the gate profile alone
P("\n==================== C3: any gate profile s(theta) ====================")
th1, th2 = 3 * H0_SI, 3 * H0_SI * math.sqrt(OM0) * 1101 ** 1.5
lam_ = th1 / th2
s_lower = (1 - lam_) - C2MAX_941 * lam_
xq = sp.Symbol("x", positive=True); Bq = sp.Symbol("B", positive=True)
sopt = (1 - xq) ** 2
bound_int = sp.integrate(Bq * (1 - xq), (xq, 0, 1))
fam = {}
for name, sfun in (("S3 cubic", lambda x: 1 - (3 * x ** 2 - 2 * x ** 3)), ("S5 quintic (CFG941)", lambda x: 1 - S5(x)),
                   ("S7 septic", lambda x: 1 - (35 * x ** 4 - 84 * x ** 5 + 70 * x ** 6 - 20 * x ** 7)), ("(1-x)^2 optimal", lambda x: (1 - x) ** 2)):
    xg_ = np.linspace(1e-6, 1 - 1e-6, 400001); sv = sfun(xg_); spp_ = np.gradient(np.gradient(sv, xg_), xg_)
    fam[name] = float(spp_[5:-5].max())
wlog = 3 * H0_SI / (math.log(1e6) + math.log(1 / C2MAX_941))
th_m = wlog * math.log(1e6)
xl = np.linspace(-20, 20, 400001); sig = 1 / (1 + np.exp(xl)); sigpp = np.gradient(np.gradient(sig, xl), xl)
fam["logistic (s(0) = 1 - 1e-6, s(3H0) = c2_max)"] = float(sigpp.max()) / wlog ** 2 * (3 * H0_SI) ** 2 / 9
kg_ratio = math.sqrt(SPP_Q / (2.0 / 9.0))
T1opt = {k_: v["k_ghost_R"] * kg_ratio for k_, v in T1c.items()}
chk("C3_concavity_theorem", s_lower > C2MAX_941 and is0(sp.diff(sopt, xq, 2) - 2) and sopt.subs(xq, 0) == 1 and sopt.subs(xq, 1) == 0
    and sp.diff(sopt, xq).subs(xq, 1) == 0 and is0(bound_int - Bq / 2) and all(v > 0 for v in fam.values()),
    f"(i) kinetic coefficient rho0 - s''W k^2 > 0 for all k iff s'' <= 0 wherever W > 0 (G2); (ii) a concave s with s(0) = 1 and |s| <= c2_max at "
    f"theta2 = 3H(1100) >= {th2 / H0_SI:.3e} H0 has s(3H0) >= 1 - lambda(1 + c2_max) = {s_lower:.6f} > c2_max = {C2MAX_941:.2e}: impossible; "
    f"(iii) any C^1 gate from 1 to 0 on [0, theta_s] with s'(theta_s) = 0 has max s'' >= 2/theta_s^2 (s' >= -B(theta_s - theta) => 1 <= B theta_s^2/2), "
    f"attained by (1 - x)^2; max s'' theta_s^2 by family: " + ", ".join(f"{k_} {v:.3f}" for k_, v in fam.items())
    + " (logistic in units (3H0)^2/9 = H0^2): every family is convex somewhere -> ghost")
P(f"   optimal gate at theta_s = 3H0 raises k_g by x{kg_ratio:.3f}: T1 k_g R = {min(T1opt.values()):.2f}-{max(T1opt.values()):.2f}; "
  f"NGC 3198 interior k_g r <= {SETS['canonical']['T3']['kg_r'].max() * kg_ratio:.2e} (still << 1)")
RES["C3"] = dict(theta2_over_H0=th2 / H0_SI, s_lower=s_lower, families=fam, kg_ratio_optimal=kg_ratio, T1_optimal=T1opt)
put("C3", "class-reason", False, "concavity theorem: ghost-free at all k needs s concave where W > 0, incompatible with s(0) = 1 and s ~ 0 on the cosmic "
    "range; bounded s'' only moves k_g (x5.1 at best), it never removes the ghost band")
rss_guard("C3")

# ================================================================================================ 5. C4: u-saturated gate + localized convex theta-term
P("\n==================== C4: u-saturated gate + transition-localized convex theta-term ====================")
xs4, Wgs4, ws4, hs4 = sp.symbols("x W_g W h", real=True)
S5s = 6 * xs4 ** 5 - 15 * xs4 ** 4 + 10 * xs4 ** 3
F4 = 60 * xs4 * (1 - xs4) * Wgs4 + sp.diff(S5s, xs4, 2) * (1 - hs4) * ws4
c4_closed = is0(F4 - 60 * xs4 * (1 - xs4) * (Wgs4 - (2 * xs4 - 1) * (1 - hs4) * ws4))
L0s = sp.integrate(xs4 * 60 * xs4 * (1 - xs4), (xs4, 0, 1))
chk("C4_construction", c4_closed and L0s == 5,
    "F_thth theta_s^2 = 60 x(1-x)[W_g - (2x-1)(1-h(u))W(u)] > 0 on 0 < x < 1 for every u once W_g >= max (1-h)W (|2x-1| < 1); = 0 outside the "
    "transition with no theta-dependence there; bag B0 = L0(0) = int_0^theta_s theta L0'' = 5 W_g; s(0, u) = 1 for all u (static states P0's); "
    "on FRW theta = 3H > theta_s and u = 0: s = h(0) = 0, L0 = 0 (no stress)")
c4 = {}
be = {f: bag_limit(f) for f in FOOTS}
for foot in FOOTS:
    a0 = A0[foot]
    rows = []
    for ucx in np.linspace(0.02, 0.98, 49):
        hf, Wg, _ = c4_build(ucx * a0, a0)
        mF, _, _ = c4_Fthth_min(ucx * a0, a0, Wg, hf)
        rows.append((ucx, Wg / (a0 * a0 / K_SI), mF))
    ue = {}
    for mult in (5.0, 1.4375, 1.0):
        ok = [rw[0] for rw in rows if mult * rw[1] <= be[foot]]
        ue[str(mult)] = max(ok) if ok else 0.0
    xe = brentq(lambda x: float(S5(x)) - C2MAX_941, 1e-6, 0.5)
    u_amp = 2 * U_MAX / (1 + xe) / a0
    c4[foot] = dict(B_e=be[foot], u_e=ue, u_amp=u_amp, x_eps=xe, minF_over_grid=min(rw[2] for rw in rows),
                    rows=[(float(a), float(b), float(c)) for a, b, c in rows[::6]])
    P(f"   [{foot}] slip-allowed bag B_e = {be[foot]:.4f} a0^2/K; (e) admits u_c <= {ue['5.0']:.2f} a0 (frozen profile, B0 = 5 W_g), "
      f"<= {ue['1.4375']:.2f} a0 (minimal profile), <= {ue['1.0']:.2f} a0 (absolute minimum B0 = W_g); (c-amp) needs u_c >= 2 U_max/(1 + x_eps) = "
      f"{u_amp:.1f} a0 (U_max = {U_MAX / a0:.2f} a0); min F_thth over all u_c, x, u in [0, a0): {min(rw[2] for rw in rows):.2e} a0^2/K")
# frozen-coefficient omega^2 lower bound for C4 states
w2min = []
for foot in FOOTS:
    a0 = A0[foot]; T3 = SETS[foot]["T3"]; hf, Wg, _ = c4_build(0.3 * a0, a0)
    for i in range(0, len(R_N), 6):
        rho0, u0 = float(T3["rho"][i]), float(T3["u"][i])
        for x0 in (0.05, 0.25, 0.5, 0.75, 0.95):
            s0 = float(1 - S5(x0) + hf(np.array([u0]))[0] * S5(x0))
            F = (60 * x0 * (1 - x0) * Wg + float(S5pp(x0)) * (1 - float(hf(np.array([u0]))[0])) * Wfull_num(u0, a0)) / THETA_S ** 2
            for ang in (0.0, math.pi / 2):
                ks = np.geomspace(1e-4, 1e8, 400) / R_N[i]
                w2 = min(omega2(kk, rho0, u0, a0, s0, F, x0 * THETA_S, gm24, ang) for kk in ks)
                w2min.append(w2 / max(K_SI * rho0, (x0 * THETA_S) ** 2))
chk("C4_d_bounded_dispersion", min(w2min) >= -1 - 1e-9,
    f"with F_thth >= 0, omega^2 >= -max(K rho0, theta0^2) at every k (a weighted mean of -K rho0 and -theta0^2 plus non-negative terms); sampled "
    f"NGC 3198 states x 5 gate points x 2 angles x k r in [1e-4, 1e8]: min omega^2/max(K rho0, theta0^2) = {min(w2min):.4f} (>= -1)")
RES["C4"] = c4
uamp_min = min(c4[f]["u_amp"] for f in FOOTS)
put("C4", "a", K1 and K2, "s(0, u) = 1 for every u and L0 is linear for theta <= 0 (a total derivative + the constant B0): P0's static law (K1, K2)")
put("C4", "b", float(S5(1.0)) == 1.0 and float(c4_build(0.3 * A0['canonical'], A0['canonical'])[0](np.array([0.0]))[0]) == 0.0, "theta = 3H >= 3H0 > theta_s and u = 0 on FRW: s = h(0) = 0, L0 = 0 -> no added stress; dust w = 0")
put("C4", "c", abs(n00 - 1) < 1e-12, "literal (quadratic action at u = 0): h = 0 below u_c/2, L0'' = 0 for theta >= theta_s -> pure dust, n = 1 (K3, c2 = 0); "
    "the always-on stiffness adds only sub-L* Jeans oscillation (reported, not graded)")
put("C4", "c-amp", uamp_min <= 1.0, f"typical (1-sigma) linear medium fields reach U_max = {U_MAX / A0['canonical']:.1f} a0 at z = 1100 (U >= a0 for z >= "
    f"{z_cross['canonical']['z_U_eq_a0']:.0f}): the saturation switches the tether ON (effective c2 = h(U/u_c) -> 1) and puts its argument beyond W_full's wall "
    f"for every u_c < a0 (needed for a finite bag); (c-amp) needs u_c >= {uamp_min:.1f} a0")
put("C4", "d", all(c4[f]["minF_over_grid"] >= 0 for f in FOOTS), f"kinetic matrix positive definite everywhere (min F_thth {min(c4[f]['minF_over_grid'] for f in FOOTS):.1e} >= 0; "
    "C4_construction); omega^2 bounded below independently of k (C4_d_bounded_dispersion): GLOBAL")
put("C4", "e", min(c4[f]['u_e']['5.0'] for f in FOOTS) > 0, f"for u_c <= {c4['canonical']['u_e']['5.0']:.2f} / {c4['alt']['u_e']['5.0']:.2f} a0 (bag 5 W_g within the slip line)")
put("C4", "g", False, "settled sector (theta <= 0 or u >= u_c) is P0 plus a constant: g1, g2 fail (section g)")
rss_guard("C4")

# ================================================================================================ 6. THEOREM G
P("\n==================== THEOREM G: local L(theta, u) ====================")
fq = sp.Function("f")
ibp = is0(sp.diff(xq * sp.diff(fq(xq), xq) - fq(xq), xq) - xq * sp.diff(fq(xq), xq, 2))
tg = {}
for foot in FOOTS:
    a0 = A0[foot]; uNmax = float(SETS[foot]["T3"]["u"].max())
    ustar = min(uNmax, U_MAX)
    Bmin = Wfull_num(ustar, a0) / (a0 * a0 / K_SI)
    tg[foot] = dict(u_star_over_a0=ustar / a0, B_min=Bmin, B_e=be[foot], ratio=Bmin / be[foot])
    P(f"   [{foot}] u* = min(u_N,max, U_max) = {ustar / a0:.4f} a0 -> B >= W(u*) = {Bmin:.4f} a0^2/K vs slip-allowed B_e = {be[foot]:.4f} a0^2/K "
      f"(x{Bmin / be[foot]:.1f})")
TG = chk("TheoremG", ibp and all(v["B_min"] > v["B_e"] for v in tg.values()) and U_MAX >= max(SETS[f]["T3"]["u"].max() for f in FOOTS),
         "for each u: f_u(theta) = L(theta, u) is convex (d); f_u(0) = -W(u) + L(0,0) (a); f_u = L(., 0) near some cosmic theta_T on the linear "
         "locus (c-amp; U_max >= u_N,max); the tangent line at theta_T gives L(0,0) - T(0) >= W(u). (d/dx)(x f' - f) = x f'' makes "
         "int_0^1 x s'' = 1 for any gate 1 -> 0 with s'(1) = 0, so the bag is >= W for EVERY profile. B >= W(u*) exceeds the slip-allowed bag on both footings: "
         "no local L(theta, u) passes (a), (c-amp), (d) and (e) together (the Solar System, u -> a0, would make the bound infinite)")
RES["TheoremG"] = tg
rss_guard("TG")

# ================================================================================================ 7. (g) class-A limit and F2
P("\n==================== (g) class-A limit, equation by equation (engine code read, not run) ====================")
gtab = [
    ("g1 universal coupling", "every PM particle (cold + baryon tracers) is kicked by -grad phi, del^2 phi ~ (1 + delta) + src (forces())",
     "settled medium (s = 1) feels -grad Phi_b + R(|grad chi|) chi_hat (CFG941 D2b)", False),
    ("g2 phantom input", "s_ph = -div[(nu(|g_b|) - 1) g_b], g_b = f_b x the field of the retained (or condensed) fraction of the PM particle density "
     "over the whole box (QUMOND phantom; neighbours enter g_b through their particles; the extra source src never feeds back)", "equilibrium R(u) = g_N with u the TOTAL tethered field (host and neighbour media enter: hover lemma)", False),
    ("g3 linear regime", "no catchments before turnaround: pure Newtonian cold matter", "theta = 3H > theta_s: s = 0, pure dust (n = 1)", True),
    ("g4 switch", "union of balls (radius x r_ON) around resolved peaks with enclosed mean >= Delta_ta(z), x tidal f_sw, x edge mask: NON-LOCAL",
     "local theta <= 0 (R3theta) [C4 also u >= u_c]: a pointwise flow criterion; no ball, no peak, no cosmic mean", False),
    ("g5 source", "src = e - q s_c (1 + delta): demand e = f_sw max(s_ph - s_c(1+delta), 0) filled by an INSTANTANEOUS shell draw, zero-sum per "
     "catchment/host; particles are not moved", "no extra source: del^2 Phi = K(rho_b + rho_c); the medium itself must move (mass conserved by "
     "continuity; settling needs dissipation, CFG938 sec. 4)", False)]
for name, ca, gt_, ok in gtab:
    P(f"   {name:22s} class A: {ca}")
    P(f"   {'':22s} gated : {gt_}  -> {'MATCH' if ok else 'NO MATCH'}")
g_pass = all(row[3] for row in gtab)
RES["g"] = [dict(item=row[0], class_A=row[1], gated=row[2], match=row[3]) for row in gtab]
P(f"  (g): {'PASS' if g_pass else 'FAIL'} (only g3 matches) -> the T1x/T2x/NC1x shear passes do NOT transfer to the gated theory or any cure here")
P("  F2 (CFG945's lane, not duplicated): every cure leaves the settled sector (theta = 0, s = 1) exactly P0 plus at most a constant, so the hover "
  "lemma and CFG941's Delta a/g_host = 1.02-1.11 are untouched; C4's u-saturation keeps any strong-field satellite medium tethered regardless of its flow")

# ================================================================================================ CLASSES
P("\n==================== CLASSES (frozen rules, criteria sec. 4) ====================")
CL = {}
CL["C1"] = dict(cls="NOT CURABLE" if min(v["ratio_to_growth_max"] for v in c1.values()) > 1 else "REGIONAL",
                why=f"(c) needs c_theta <= {c_theta_max:.1e} kg/m; (d) on T1-T3 needs c_theta >= {min(v['c_theta_g'] for v in c1.values()):.1e} "
                    f"(x{min(v['ratio_to_growth_max'] for v in c1.values()):.0e}); (d) global impossible (W unbounded); for u >= {min(u_flip.values()):.3f} a0 the bound "
                    "also removes the scale factor's kinetic term (12 pi G c_theta/c^2 >= 1)")
CL["C2"] = dict(cls="NOT CURABLE", why="rho: R3n (a, c, d fail); chi: shift symmetry, static law, cannot separate collapsed/linear; latch: "
                                       "lambar F_thth ghost or a density/label gate; clock-density Y: (a) and (d) fail")
CL["C3"] = dict(cls="NOT CURABLE", why="concavity theorem (C3_concavity_theorem); bounded s'' moves k_g by <= x5.1")
c4_window = all(c4[f]["u_amp"] <= c4[f]["u_e"]["5.0"] and c4[f]["u_amp"] < 1.0 for f in FOOTS)
CL["C4"] = dict(cls="NOT CURABLE" if not c4_window else "CURED-WITH-COST",
                why=f"(c-amp) needs u_c >= {uamp_min:.1f} a0 but a finite bag needs u_c < a0 and (e) needs u_c <= {min(c4[f]['u_e']['5.0'] for f in FOOTS):.2f} a0")
for k_, v in CL.items():
    P(f"  {k_}: {v['cls']:12s} {v['why']}")
allnc = all(v["cls"] == "NOT CURABLE" for v in CL.values())
if any(v["cls"] in ("CURED", "CURED-WITH-COST") for v in CL.values()):
    OVERALL = "GHOST CURED"
elif any(v["cls"] == "REGIONAL" for v in CL.values()):
    OVERALL = "CONDITIONAL"
elif allnc and TG:
    OVERALL = "NO CURE"
else:
    OVERALL = "NO CURE FOUND (no proof)"
P(f"\n  OVERALL: {OVERALL}")
RES["tests"] = TESTS; RES["classes"] = CL; RES["overall"] = OVERALL; RES["g_pass"] = g_pass
allchk = all(v["pass"] for v in RES["checks"].values())
P(f"\n  all checks pass: {allchk}; runtime {time.time() - T0:.1f} s; peak RSS {rss_val() / 1e9:.3f} GB")
dump()
sys.exit(0 if (allchk and K_ALL) else 1)

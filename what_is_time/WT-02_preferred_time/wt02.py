"""WT-02 -- what defines "now" in the CFG938 parent?  Preferred foliation / frame, characteristics, L95, frame size, c_T.
Criteria: FROZEN_CRITERIA.md (b85749d1cd, committed alone before this script).
Run (one core, one process, < 1 GB):
    OMP_NUM_THREADS=1 nice -n 10 python3 wt02.py                 -> wt02.out, wt02_results.json
    WT02_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 wt02.py   -> wt02_MUTATE.out, wt02_results_MUTATE.json
MUTATE exits 1 iff every tooth bites (2 otherwise).  Main exits 0 iff every control passes.
kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; no particle species; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib, itertools
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
LANES = os.path.join(REPO, "campaign_fresh_gravity")
MUT = os.environ.get("WT02_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = []; RES = {"lane": "WT-02", "criteria": "b85749d1cd", "mutate": MUT, "checks": {}, "labels": {}}
T0 = time.time(); RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def guard(where):
    if rss() > RSS_LIMIT:
        P(f"RSS GUARD {rss() / 1e9:.2f} GB at {where}; abort"); dump(); sys.exit(3)


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def dump():
    RES["runtime_s"] = round(time.time() - T0, 1); RES["peak_rss_GB"] = round(rss() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"wt02_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"wt02{TAG}.out"), "w").write("\n".join(OUT) + "\n")


# ------------------------------------------------------------------------------------------------ constants / inputs
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                   # read-only: the record's footings
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15
G_SI, C_SI, MSUN, PC = 6.67430e-11, 299792458.0, 1.98847e30, 3.0856775814913673e16
KPC, MPC = 1e3 * PC, 1e6 * PC
K_SI = 4 * math.pi * G_SI
H0 = 67.4e3 / MPC; OMB = 0.0493; OMC = OMB * 5.364; OMM = OMB + OMC; OML = 1 - OMM   # CFG938's declared cosmology
LSTAR = {"24pc": 24 * PC, "1kpc": 1 * KPC}                                           # CFG820 window ends
WS = {"30": 30e3, "370": 370e3, "1000": 1000e3}
RSUN, AU, VEARTH = 6.957e8, 1.495978707e11, 29.78e3
GMSUN = G_SI * MSUN
BOUND = dict(alpha1=3.4e-5, alpha2_weak=1e-7, alpha2_strong=1.6e-9, alpha3=4e-20, cT_lo=-3e-15, cT_hi=7e-16)
H72 = [(1.50e10, 1.67), (3.66e10, 2.07), (6.01e10, 3.44), (9.13e10, 2.77)]           # (M_b [Msun], r_end bound [Mpc])
CFG770_BG = {"canonical": [(2.00e-10, 0.6812), (2.32e-10, 0.7125), (2.64e-10, 0.7382)],
             "alt": [(2.00e-10, 0.6387), (2.32e-10, 0.6722), (2.64e-10, 0.7000)]}  # (g_e, u_e/a0), cfg770.out lines 10-15
R_SUN_GAL = 8.2 * KPC                                                                 # declared (criteria D2)
D_GW = 40 * MPC                                                                       # declared (criteria E3)


def law_g(gN, a0):                      # g_N = g^2/(g + a0)
    return 0.5 * (gN + math.sqrt(gN * gN + 4.0 * gN * a0))


def law_u(gN, a0):                      # medium's own field on the law: u = g - g_N
    return law_g(gN, a0) - gN


def Rrem(u, a0): return u * u / (a0 - u)
def Rp(u, a0): return u * (2 * a0 - u) / (a0 - u) ** 2
def Dfull(u, a0): return u / (1 - u / a0)


P("WT-02  what defines 'now' in the CFG938 parent" + ("   [MUTATE]" if MUT else ""))
P("  criteria b85749d1cd; kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2")

# ================================================================================================ covariant machinery (A1)
x0, x, y, z = sp.symbols("x0 x y z", real=True); XX = [x0, x, y, z]
eps = sp.Symbol("epsilon")
c, Km, Ls, u0 = sp.symbols("c K_m L_s u_0", positive=True)
h = sp.Symbol("h", real=True, nonzero=True)
Dd, Dp, lam0 = sp.symbols("D_d D_p lambda_0", real=True)


def ser2(e):
    e0 = e.subs(eps, 0); d1 = sp.diff(e, eps)
    return sp.expand(e0 + eps * d1.subs(eps, 0) + eps ** 2 * sp.diff(d1, eps).subs(eps, 0) / 2)


def build(case, intrinsic=False, chib_on=True):
    """CFG938 action ingredients to O(eps^2): comoving labels (plane symmetric), u, h, nabla nabla chi, D^2 chi, tau, u^2.
    case: 'frw' (a = exp(h x0), chibar from S1d) | 'static_par' (grad chi along x = along k) | 'static_perp' (along y) |
    'static_zero' (no background gradient).  x0 = c t in the static cases; c = 1 and lengths in c/H in 'frw'."""
    xi = sp.Function("xi")(x0, x); eta = sp.Function("eta")(x0, x)
    dchi = sp.Function("dchi")(x0, x); dlam = sp.Function("dlam")(x0, x); Phi = sp.Function("Phi")(x0, x)
    if case == "frw":
        a = sp.exp(h * x0); g = sp.diag(-1, a ** 2, a ** 2, a ** 2)
        chib = Km / (9 * h ** 2) * sp.exp(-3 * h * x0) if chib_on else 0     # chibar' = -K rho a^-3 /(3 a'/a)  (S1d)
        fields = [xi, eta, dchi, dlam]
    else:
        g = sp.diag(-1, 1, 1, 1)
        chib = {"static_par": u0 * x, "static_perp": u0 * y, "static_zero": 0}[case]
        fields = [xi, eta, dchi, dlam, Phi]
    chi = chib + eps * dchi; lam = eps * dlam
    gi = g.inv(); sqrtg = sp.sqrt(-g.det())
    phis = [x - eps * xi, y - eps * eta, z]
    dphi = [[sp.diff(p_, X) for X in XX] for p_ in phis]
    J = []
    for mu in range(4):
        tot = 0
        for (a_, b_, c_) in itertools.permutations([i for i in range(4) if i != mu], 3):
            lc = sp.LeviCivita(mu, a_, b_, c_)
            for (I, Jx, Kx) in itertools.permutations(range(3), 3):
                tot += lc * sp.LeviCivita(I, Jx, Kx) * dphi[I][a_] * dphi[Jx][b_] * dphi[Kx][c_]
        J.append(tot / (6 * sqrtg))
    J = sp.Matrix(J)
    if (J[0].subs(eps, 0)).subs(x0, 0) < 0:
        J = -J
    J = J.applyfunc(ser2)
    n = ser2(sp.sqrt(-ser2((J.T * g * J)[0])))
    uu = (J / n).applyfunc(ser2); ud = (g * uu).applyfunc(ser2)
    hup = (gi + uu * uu.T).applyfunc(ser2); hdn = (g + ud * ud.T).applyfunc(ser2)
    hmix = (sp.eye(4) + ud * uu.T).applyfunc(ser2)                  # h_mu^alpha
    Gam = [[[ser2(sum(gi[r_, d_] * (sp.diff(g[d_, m_], XX[n_]) + sp.diff(g[d_, n_], XX[m_]) - sp.diff(g[m_, n_], XX[d_]))
                      for d_ in range(4)) / 2) for n_ in range(4)] for m_ in range(4)] for r_ in range(4)]
    dch = [sp.diff(chi, X) for X in XX]
    nab = sp.Matrix(4, 4, lambda m_, n_: ser2(sp.diff(chi, XX[m_], XX[n_]) - sum(Gam[r_][m_][n_] * dch[r_] for r_ in range(4))))
    DD = (hmix * nab * hmix.T).applyfunc(ser2)
    D2 = ser2(sum(hup[m_, n_] * nab[m_, n_] for m_ in range(4) for n_ in range(4)))
    theta = ser2(sum(sp.diff(sqrtg * uu[m_], XX[m_]) for m_ in range(4)) / sqrtg)
    udchi = ser2(sum(uu[m_] * dch[m_] for m_ in range(4)))
    if intrinsic:                                                   # MU3: intrinsic slice Laplacian (theta u.d chi removed)
        D2 = ser2(D2 + theta * udchi)
    tau = (DD - hdn * D2 / 3).applyfunc(ser2)
    tauup = (gi * tau * gi).applyfunc(ser2)
    tt = ser2(sum(tau[m_, n_] * tauup[m_, n_] for m_ in range(4) for n_ in range(4)))
    s = ser2(sum(hup[m_, n_] * dch[m_] * dch[n_] for m_ in range(4) for n_ in range(4)))
    return dict(g=g, sqrtg=sqrtg, n=n, u=uu, D2=D2, tt=tt, s=s, lam=lam, fields=fields, theta=theta, udchi=udchi, chib=chib)


def modes(L2, fields, phase, at):
    eqs = sp.euler_equations(L2, fields, [x0, x])
    amps = sp.symbols(" ".join(f"A{i}" for i in range(len(fields))))
    M = sp.zeros(len(fields), len(fields))
    for i, e in enumerate(eqs):
        ex = e.lhs
        for f_, A_ in zip(fields, amps):
            ex = ex.subs(f_, A_ * sp.exp(phase)).doit()
        ex = sp.expand(sp.powsimp(sp.expand(ex * sp.exp(-phase)))).subs(at)
        ex = sp.expand(sp.simplify(ex))
        for j, A_ in enumerate(amps):
            M[i, j] = sp.expand(ex.coeff(A_))
    return M, eqs


sig, kk, om = sp.symbols("sigma k omega")


def frw_system(intrinsic=False):
    B = build("frw", intrinsic=intrinsic, chib_on=not intrinsic)
    n = B["n"]; sqrtg = B["sqrtg"]
    src = Km * (n - sp.exp(-3 * h * x0)) if intrinsic else Km * n    # MU3 needs the background subtraction (no chibar)
    Lt = sqrtg * (-Km * n - B["s"] / 2 - sp.Rational(3, 8) * Ls ** 2 * B["tt"] + B["lam"] * (B["D2"] - src))
    Le = sp.expand(Lt); L2 = Le.coeff(eps, 2)
    M, eqs = modes(L2, B["fields"], sig * x0 + sp.I * kk * x, {x0: 0})
    return M, L2, B


def static_system(geom, with_lam0=False):
    B = build("static_" + geom)
    n = B["n"]; sqrtg = B["sqrtg"]; s = B["s"]; Phi = B["fields"][-1]
    if geom == "zero":
        KW = s / 2
    else:
        ds = sp.expand(s - u0 ** 2)
        KW = Dd / (2 * u0) * ds + sp.Rational(1, 2) * (Dp - Dd / u0) / (4 * u0 ** 2) * ds ** 2
    lamt = B["lam"] + (lam0 if with_lam0 else 0)
    Lt = (sqrtg * (-c ** 2 * Km * n - eps * Km * n * Phi - KW - sp.Rational(3, 8) * Ls ** 2 * B["tt"] + lamt * (B["D2"] - Km * n))
          - (eps * sp.diff(Phi, x)) ** 2 / 2)
    L2 = sp.expand(Lt).coeff(eps, 2)
    M, eqs = modes(L2, B["fields"], -sp.I * om / c * x0 + sp.I * kk * x, {})
    return M, L2, B


def has_time(Mrow_entry, var):
    return sp.expand(Mrow_entry).has(var)


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
KOK = {}
# ---- K1: NGC 3198 law reduction from the reduced static functional (CFG938 K1)
r_, G_ = sp.symbols("r G", positive=True); uS, gNS, a0S = sp.symbols("u g_N a_0", positive=True)
Wfull_s = (-a0S * uS - a0S ** 2 * sp.log(1 - uS / a0S)) / (4 * sp.pi * G_)
Mc = sp.Function("M_c")(r_); Mb = sp.Function("M_b")(r_)
Lred = -G_ * (Mb + Mc) ** 2 / (2 * r_ ** 2) + 4 * sp.pi * r_ ** 2 * sp.Lambda(uS, Wfull_s)(G_ * Mc / r_ ** 2)
ELr = sp.euler_equations(Lred, [Mc], [r_])[0].lhs.subs({Mc: uS * r_ ** 2 / G_, Mb: gNS * r_ ** 2 / G_}).doit()
fEL = sp.lambdify((uS, gNS, a0S, G_), sp.simplify(ELr), "math")
dat = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
Rr = dat[:, 0] * KPC; Vg, Vd, Vb = dat[:, 3] * 1e3, dat[:, 4] * 1e3, dat[:, 5] * 1e3
gNb = (Vg * np.abs(Vg) + 0.61 * Vd * np.abs(Vd) + 0.61 * Vb * np.abs(Vb)) / Rr
k1 = {}
for f in FOOTS:
    a0 = A0[f]; rel = []
    for gn in gNb:
        uu_ = brentq(lambda q: fEL(q, gn, a0, G_SI), 1e-300, a0 * (1 - 1e-15), xtol=1e-30, rtol=1e-15, maxiter=500)
        rel.append(abs((gn + uu_) / law_g(gn, a0) - 1))
    k1[f] = float(max(rel))
KOK["K1"] = chk("K1_NGC3198_law_reduction", all(v <= 1e-12 for v in k1.values()) and len(gNb) == 43,
                f"N = {len(gNb)}; max|g/g_law - 1| canonical {k1['canonical']:.2e}, alt {k1['alt']:.2e} (line 1e-12; CFG938 2.22e-16)")
guard("K1")
# ---- K2: S1d on FRW
Bf = build("frw")
D2b = sp.simplify(Bf["D2"].coeff(eps, 0))
chib = Bf["chib"]
k2 = sp.simplify(D2b - (-3 * h * sp.diff(chib, x0))) == 0 and sp.simplify(D2b - Km * sp.exp(-3 * h * x0)) == 0
KOK["K2"] = chk("K2_S1d_FRW", k2, f"D^2 chibar = {D2b} = -3 (a'/a) chibar' = K m nbar (homogeneous solution, S1d)")
# ---- K3: S5a from the covariant machinery (c -> infinity, lambda_0 = 0, Newtonian self-gravity on)
k3 = {}
for geom in ("par", "perp"):
    Ms, L2s, Bs = static_system(geom)
    det = sp.factor(Ms.det())
    w2 = sp.symbols("w2")
    detw = sp.expand(det.subs(om, sp.sqrt(w2)))
    roots = sp.solve(detw, w2)
    lim = [sp.simplify(sp.limit(r__, c, sp.oo)) for r__ in roots]
    k3[geom] = dict(M=Ms, roots=roots, lim=lim, L2=L2s, B=Bs)
# expected (Kp = K rho0 = Km, gamma rho0 = Km Ls^2/2; D = u + R, D' = 1 + R')
exp_par = Km * (Dp - 1) + Km * Ls ** 2 * kk ** 2 / 2
exp_perp = Km * (Dd / u0 - 1) + Km * Ls ** 2 * kk ** 2 / 2
okp = any(sp.simplify(l_ - exp_par) == 0 for l_ in k3["par"]["lim"]) and any(sp.simplify(l_) == 0 for l_ in k3["par"]["lim"])
okq = any(sp.simplify(l_ - exp_perp) == 0 for l_ in k3["perp"]["lim"]) and any(sp.simplify(l_) == 0 for l_ in k3["perp"]["lim"])
KOK["K3"] = chk("K3_S5a_reproduced", okp and okq,
                f"k || grad chi: omega^2 -> {[str(l_) for l_ in k3['par']['lim']]}; k perp grad chi: {[str(l_) for l_ in k3['perp']['lim']]} "
                "(= gamma rho0 k^2 + K rho0 R' and + K rho0 R/u with D' = 1 + R', D/u = 1 + R/u; the 0 root is the vortical mode)")
guard("K3")
# ---- K4: Mehler kernel at B -> 0
def g_beta(beta):
    """g(beta) = 4 pi r G_nu(r): in-plane Green function of the rotating-medium constraint, normalised to Poisson."""
    if beta < 1e-12:
        f = lambda t: (4 * math.pi * t) ** -0.5 * math.exp(-1 / (4 * t)) / t
    else:
        def f(t):
            e2 = math.exp(-2 * beta * t)
            if beta * t > 700:
                return 0.0
            sh = 2 * beta * math.exp(-beta * t) / (1 - e2) if beta * t > 1e-8 else 1 / t
            ct = (1 + e2) / (1 - e2) if beta * t > 1e-8 else 1 / (beta * t)
            return sh * math.exp(-(beta / 4) * ct) * (4 * math.pi * t) ** -0.5
    val = quad(lambda lt: f(math.exp(lt)) * math.exp(lt), -14, 70, limit=800, epsabs=0, epsrel=1e-11)[0]
    return val
g0 = g_beta(0.0)
KOK["K4"] = chk("K4_Mehler_Poisson_limit", abs(g0 - 1) < 1e-6, f"g(B -> 0) = {g0:.9f} (line |g - 1| < 1e-6)")
bsm = [1e-11, 1e-9, 1e-7, 1e-5]; Cs = [(1 - g_beta(b_)) / math.sqrt(b_) for b_ in bsm]
P(f"  K4 diagnostic (not a frozen check): 1 - g(beta) = C sqrt(beta) with C = {Cs[0]:.5f}..{Cs[-1]:.5f} for beta = 1e-11..1e-5 "
  "(non-analytic at B = 0: the time kernel has heavy tails; run 2's extra beta = 1e-9 check expected analytic behaviour and is removed, amendment A1)")
RES["K4_sqrt_coefficient"] = Cs
# ---- K5: linearised Ricci for TT; c_T = c with L* = 0 (done in E)
th_k = sp.Symbol("theta_k", real=True)
nvec = sp.Matrix([sp.sin(th_k), 0, sp.cos(th_k)])
e1 = sp.Matrix([sp.cos(th_k), 0, -sp.sin(th_k)]); e2v = sp.Matrix([0, 1, 0])
EP = e1 * e1.T - e2v * e2v.T; EX = e1 * e2v.T + e2v * e1.T
Ap, Ax = sp.symbols("A_p A_x", real=True)
Fw = sp.Function("F")
zeta = (nvec[0] * x + nvec[2] * z)
Hs = (Ap * EP + Ax * EX) * Fw(x0, zeta)
gT = sp.diag(-1, 1, 1, 1)
for i in range(3):
    for j in range(3):
        gT[i + 1, j + 1] += eps * Hs[i, j]
def ricci_lin(gm):
    gim = gm.inv()
    Gm = [[[sum(gim[r__, d_] * (sp.diff(gm[d_, m_], XX[n_]) + sp.diff(gm[d_, n_], XX[m_]) - sp.diff(gm[m_, n_], XX[d_])) for d_ in range(4)) / 2
            for n_ in range(4)] for m_ in range(4)] for r__ in range(4)]
    Gm1 = [[[sp.diff(Gm[r__][m_][n_], eps).subs(eps, 0) for n_ in range(4)] for m_ in range(4)] for r__ in range(4)]
    R1 = sp.zeros(4, 4)
    for m_ in range(4):
        for n_ in range(4):
            R1[m_, n_] = sum(sp.diff(Gm1[r__][m_][n_], XX[r__]) - sp.diff(Gm1[r__][m_][r__], XX[n_]) for r__ in range(4))
    return R1
R1 = ricci_lin(gT)
boxH = sp.Matrix(3, 3, lambda i, j: -sp.diff(Hs[i, j], x0, 2) + sum(sp.diff(Hs[i, j], X, 2) for X in (x, y, z)))
k5a = all(sp.simplify(R1[i + 1, j + 1] + boxH[i, j] / 2) == 0 for i in range(3) for j in range(3))
trT = sp.simplify((Hs).trace()); divT = [sp.simplify(sum(sp.diff(Hs[i, j], [x, y, z][j]) for j in range(3))) for i in range(3)]
KOK["K5"] = chk("K5_TT_linearised_Ricci", k5a and trT == 0 and all(d_ == 0 for d_ in divT), "R^(1)_ij = -(1/2) box h_ij for the TT basis used in E (traceless, transverse)")
guard("K5")
# ---- K6: screened pull from 2 K M/(L*^2 k^4) (IR-regularised)
kq, rq, muq, MM, LL, GG = sp.symbols("k r mu M L G", positive=True)
Kq = 4 * sp.pi * GG
Iint = sp.integrate(sp.sin(kq * rq) / (kq * (kq ** 2 + muq ** 2)), (kq, 0, sp.oo))
Phi_r = -(2 * Kq * MM / LL ** 2) / (2 * sp.pi ** 2 * rq) * Iint
pull = sp.simplify(sp.limit(-sp.diff(Phi_r, rq), muq, 0))
KOK["K6"] = chk("K6_screened_pull_GM_over_Lstar2", sp.simplify(pull + GG * MM / LL ** 2) == 0,
                f"-dPhi_c/dr (mu -> 0) = {pull} : magnitude GM/L*^2 toward the mass (CFG770 K1); Phi_c - Phi_c(0) = GMr/L*^2 => f_c = r^2/L*^2")
# ---- K7: FRW parabolic coefficients vanish as H -> 0
Mf, L2f, Bfrw = frw_system()
cchi = sp.expand(Mf[3, 2]).coeff(sig); clam = sp.expand(Mf[2, 3]).coeff(sig)
KOK["K7"] = chk("K7_FRW_parabolic_coeffs_vanish_at_H0", sp.limit(cchi, h, 0) == 0 and sp.limit(clam, h, 0) == 0,
                f"coefficient of d0 dchi in the chi equation = {cchi}; of d0 dlam in the lambda equation = {clam}; both -> 0 as h -> 0 "
                f"(note: chibar' = -K rho/(3h) itself diverges as h -> 0)")
K_ALL = all(KOK.values()); RES["K_all"] = K_ALL
P(f"  K controls all pass: {K_ALL}")
guard("K")

# ================================================================================================ A. CHARACTERISTICS
P("\n==================== A. CHARACTERISTICS ====================")
A = {}
# ---- A-i / A-ii: static backgrounds -- which fields carry time derivatives?
P("  A-i static medium (Minkowski), plane-symmetric linearisation of the full covariant action; rows = EL equation of "
  "[xi, eta, dchi, dlam, Phi] in the order: medium-long, medium-trans, (chi-variation = lambda eq), (lambda-variation = chi eq), Poisson")
cls_static = {}
for geom in ("par", "perp", "zero"):
    Ms = k3[geom]["M"] if geom in k3 else static_system(geom)[0]
    rows = {"chi_eq (from dlam)": 3, "lambda_eq (from dchi)": 2, "Phi_eq": 4}
    res_g = {}
    for nm, ri in rows.items():
        own = {3: 2, 2: 3, 4: 4}[ri]
        res_g[nm] = "TIME-DERIVATIVE" if has_time(Ms[ri, own], om) else "ELLIPTIC"
    P(f"    grad chi {geom:5s}: chi eq row = {[str(sp.factor(e_)) for e_ in Ms[3, :]]}")
    P(f"                    lambda eq row = {[str(sp.factor(e_)) for e_ in Ms[2, :]]}")
    cls_static[geom] = res_g
    P(f"                    own-field time derivatives: {res_g}")
A["static_classes"] = cls_static
# lambda_0 variant
Ml0, L2l0, _ = static_system("par", with_lam0=True)
l0_chi = has_time(Ml0[3, 2], om); l0_lam = has_time(Ml0[2, 3], om)
detl0 = sp.factor(Ml0.det())
P(f"    lambda_0 != 0 variant (k || grad chi): chi eq own time derivative: {l0_chi}; lambda eq own time derivative: {l0_lam}; det = {detl0}")
A["lambda0_variant"] = dict(chi_time=l0_chi, lam_time=l0_lam, det=str(detl0))
static_elliptic = all(v_ == "ELLIPTIC" for d_ in cls_static.values() for v_ in d_.values()) and not l0_chi and not l0_lam
chk("A_static_chi_lambda_elliptic", static_elliptic, "on static media the chi and lambda equations carry no time derivative of their own field "
    "along u (elliptic, instantaneous on the medium's slices); Phi here is the Newtonian limit of the hyperbolic metric")
# medium speed on static backgrounds: principal part omega^2 -> c_s^2 k^2
cs2_par = sp.limit(k3["par"]["lim"][[i for i, l_ in enumerate(k3["par"]["lim"]) if l_ != 0][0]] / kk ** 2, kk, sp.oo)
P(f"    medium longitudinal principal speed^2 (k -> inf) = {cs2_par}  (= gamma rho0 = c_s^2); vortical roots omega^2 = 0")
# ---- A-ii: NGC 3198 frozen coefficients
P("  A-ii NGC 3198 law state (frozen coefficients, both footings, L* = 24 pc / 1 kpc)")
def u_rho_profile(gN_arr, R_arr, a0):
    u_arr = np.array([law_u(g_, a0) for g_ in gN_arr])
    y_ = R_arr ** 2 * u_arr
    dy = np.gradient(y_, R_arr)
    rho = dy / (K_SI * R_arr ** 2)
    return u_arr, rho
A2 = {}
for f in FOOTS:
    a0 = A0[f]
    u_arr, rho_arr = u_rho_profile(gNb, Rr, a0)
    good = rho_arr > 0
    for lk, Lv in LSTAR.items():
        cs = np.sqrt(np.clip(K_SI * Lv ** 2 / 2 * rho_arr, 0, None))
        inv_eps = K_SI * rho_arr * C_SI ** 2 / (np.array([Dfull(q, a0) for q in u_arr]) * u_arr)
        A2[f"{f}|{lk}"] = dict(cs_max_kms=float(cs.max() / 1e3), cs_over_c_max=float(cs.max() / C_SI), n_rho_pos=int(good.sum()),
                               min_inertia_margin=float(inv_eps[good].min()), max_eps_omega=float((1 / inv_eps[good]).max()))
        P(f"    {f:9s} L*={lk:5s}: max c_s = {cs.max() / 1e3:.3e} km/s (c_s/c = {cs.max() / C_SI:.2e}); rho_c > 0 at {good.sum()}/43 radii; "
          f"min inertia margin rho c^2 K/(D u) = {inv_eps[good].min():.2e}")
A["NGC3198"] = A2
speeds_ok = all(v_["cs_over_c_max"] <= 1 for v_ in A2.values())
# ---- A-iii / A-iv: FRW (expanding / contracting) -- parabolic structure and Hadamard test
P("  A-iii FRW (rows: EL equations of [xi, eta, dchi, dlam]; sigma = growth rate in units of H, k in units of H/c)")
for i in range(4):
    P(f"    row {i}: {[str(sp.factor(Mf[i, j])) for j in range(4)]}")
chi_coef = sp.factor(cchi); lam_coef = sp.factor(clam)
P(f"    chi eq: (-k^2 {'+' if True else ''} ({chi_coef}) sigma) dchi + ... ; lambda eq: (... + ({lam_coef}) sigma) dlam")
detf = sp.factor(Mf.det())
P(f"    det M = {detf}")
A["FRW_rows"] = [[str(sp.factor(Mf[i, j])) for j in range(4)] for i in range(4)]; A["FRW_det"] = str(detf)
# classify the own-field parabolic sign: unsourced chi mode sigma = -k^2/(3h); lambda mode sigma = (k^2 - 9h^2)/(3h)
s_chi = sp.solve(sp.Eq(Mf[3, 2], 0), sig)[0]; s_lam = sp.solve(sp.Eq(Mf[2, 3], 0), sig)[0]
P(f"    unsourced chi mode sigma = {s_chi}; unsourced lambda mode sigma = {s_lam}")
poly_full = sp.Poly(sp.numer(sp.together(detf / sig)), sig)                       # drop the vortical sigma = 0 root
def hadamard(hv, Kmv, Lsv, poly=poly_full, label=""):
    ks = [10 ** p_ for p_ in (2, 3, 4, 5, 6)]
    mp.mp.dps = 80
    mx = []
    cfun = [sp.lambdify((h, Km, Ls, kk), cc, "mpmath") for cc in poly.all_coeffs()]
    for kv in ks:
        cf = [f_(mp.mpf(hv), mp.mpf(Kmv), mp.mpf(Lsv), mp.mpf(kv)) for f_ in cfun]
        while abs(cf[0]) == 0: cf = cf[1:]
        rts = mp.polyroots(cf, maxsteps=800, extraprec=800)
        mx.append(max(float(mp.re(r__)) for r__ in rts))
    slope = math.log(max(mx[-1], 1e-300) / max(mx[-2], 1e-300)) / math.log(10) if mx[-1] > 0 and mx[-2] > 0 else float("nan")
    fires = (mx[-1] / abs(hv) > 1e3) and (1.9 <= slope <= 2.1)
    return ks, mx, slope, fires
def frozen(zv):
    E2 = OMM * (1 + zv) ** 3 + OML
    Omc_z = OMC * (1 + zv) ** 3 / E2
    Hz = H0 * math.sqrt(E2)
    return 1.5 * Omc_z, Hz
HAD = {}
for zv in (0.0, 10.0):
    Kmv, Hz = frozen(zv)
    for lk, Lv in LSTAR.items():
        Lsv = Lv * Hz / C_SI
        for sgn, nm in ((1, "expanding"), (-1, "contracting")):
            ks, mx, slope, fires = hadamard(sgn * 1.0, Kmv, Lsv)
            HAD[f"z{zv:g}|{lk}|{nm}"] = dict(k=ks, maxRe=mx, slope=slope, fires=bool(fires))
            P(f"    z = {zv:4.1f} L*={lk:5s} {nm:11s}: max Re sigma / |H| at k l_H = 1e2..1e6: {[f'{m_:.3e}' for m_ in mx]}; "
              f"slope {slope:.4f}; Hadamard fires: {fires}")
A["Hadamard"] = HAD
ill = all(v_["fires"] for v_ in HAD.values())
# anticipation time for the final-data reading: tau_k = 1/max Re sigma ~ 3H/(c^2 k^2)
TAU = {}
for rr_lab, rr in (("10kpc", 10 * KPC), ("1Mpc", MPC), ("100Mpc", 100 * MPC)):
    kv = 1 / rr
    kl = kv * C_SI / H0
    mxv = float(kl ** 2 / 3)                                       # leading root (checked against the polynomial above)
    TAU[rr_lab] = dict(k_lH=kl, tau_s=1 / (mxv * H0), tau_yr=1 / (mxv * H0) / 3.156e7, light_crossing_yr=rr / C_SI / 3.156e7)
    P(f"    anticipation (final-data reading) at r = {rr_lab:6s}: tau_k = 3H r^2/c^2 = {TAU[rr_lab]['tau_yr']:.3e} yr "
      f"(light crossing {TAU[rr_lab]['light_crossing_yr']:.3e} yr)")
lead = HAD["z0|24pc|expanding"]["maxRe"][-1] / (1e6 ** 2 / 3)
P(f"    check: leading root at k l_H = 1e6 equals k^2/3 to {abs(lead - 1):.2e}")
A["anticipation"] = TAU
LAB_A = []
if static_elliptic: LAB_A.append("MEDIUM CLOCK")
if ill: LAB_A.append("ILL-POSED-IVP")
if not static_elliptic and not ill and speeds_ok: LAB_A.append("NO PREFERRED TIME")
P(f"  (a) labels: {LAB_A}" + ("  | criterion B VIOLATED under the final-data reading of the backward field" if ill else ""))
RES["labels"]["a"] = LAB_A; RES["A"] = {k_: v_ for k_, v_ in A.items()}
guard("A")

# ================================================================================================ B. THE FRAME
P("\n==================== B. THE FRAME ====================")
B_ = {}
# B1 vortical roots: transverse eta rows
vort = all(sp.factor(k3[g_]["M"][1, 1]).has(om) and sp.limit(sp.factor(k3[g_]["M"][1, 1]) / om ** 2, c, sp.oo) != 0 for g_ in ("par",))
P(f"  B1 transverse (eta) row, k || grad chi: {sp.factor(k3['par']['M'][1, 1])} * eta = 0  -> omega^2 = 0 (vortical, frozen-in, positive kinetic coefficient)")
B_["B1_vortical_allowed"] = bool(vort)
# B2 Kelvin with W(u) velocity dependence
vr, vt, rho_s, Uc, cc_ = sp.symbols("v_r v_theta rho U c", positive=True)
Wf = sp.Function("W")
uvel = sp.sqrt(Uc ** 2 + (vr * Uc) ** 2 / cc_ ** 2)
Lkin = rho_s * (vr ** 2 + vt ** 2) / 2 - Wf(uvel)
pi_r = sp.diff(Lkin, vr); pi_t = sp.diff(Lkin, vt)
corr = sp.simplify(rho_s * vr - pi_r)
P(f"  B2 canonical momentum: pi_r = rho v_r - [{corr}] ; pi_theta = {pi_t}")
rr_, th_ = sp.symbols("r theta_p", positive=True)
fr = sp.Function("f")(rr_); vrf = sp.Function("vr")(rr_, th_)
curl_corr = sp.simplify(-sp.diff(fr * vrf, th_) / rr_)          # z-curl of f(r) v_r(r,theta) rhat in polar coordinates
B_["B2_curl_of_correction"] = str(curl_corr)
P(f"  B2 if pi is irrotational, curl(rho v) = curl(f(r) v_r rhat) = {curl_corr}  (f = W'(u) U^2/(u c^2) != 0): vorticity of v forced at relative order eps_omega")
eps_om = {f: max(A2[f"{f}|24pc"]["max_eps_omega"], A2[f"{f}|1kpc"]["max_eps_omega"]) for f in FOOTS}
P(f"  B2 eps_omega = D(u) u/(K rho_c c^2) max on NGC 3198: canonical {eps_om['canonical']:.2e}, alt {eps_om['alt']:.2e}")
B_["B2_eps_omega"] = eps_om
# B3 Frobenius
Om, ct_ = sp.symbols("Omega c", positive=True)
gam = 1 / sp.sqrt(1 - Om ** 2 * (x ** 2 + y ** 2) / ct_ ** 2)
u_dn = [-gam, -gam * Om * y / ct_, gam * Om * x / ct_, 0]           # x0 = c t, flat
def d1form(w_):
    return [[sp.diff(w_[j], XX[i]) - sp.diff(w_[i], XX[j]) for j in range(4)] for i in range(4)]
du_ = d1form(u_dn)
w3 = sp.simplify(u_dn[0] * du_[1][2] + u_dn[1] * du_[2][0] + u_dn[2] * du_[0][1])  # (u ^ du)_{0xy}
P(f"  B3 rigid rotation: (u ^ du)_(t x y) = {sp.simplify(w3)}  (nonzero -> u is not hypersurface-orthogonal: no medium slices)")
B_["B3_frobenius"] = str(w3)
# B4 Hormander bracket and Mehler time kernel
tS = sp.Symbol("t", real=True)
fT = sp.Function("f")(tS, x, y)
vx_, vy_ = -Om * y, Om * x
Xx = lambda F_: sp.diff(F_, x) + vx_ / ct_ ** 2 * sp.diff(F_, tS)
Xy = lambda F_: sp.diff(F_, y) + vy_ / ct_ ** 2 * sp.diff(F_, tS)
br = sp.simplify(Xx(Xy(fT)) - Xy(Xx(fT)))
P(f"  B4 [X_x, X_y] f = {br}  (bracket-generating: the constraint operator is hypoelliptic in (x, y, t), not a family of slice problems)")
B_["B4_bracket"] = str(br)
bgrid = np.concatenate([[0.0], np.logspace(-9, math.log10(400), 260)])
ggrid = np.array([g_beta(b_) for b_ in bgrid])
from scipy.interpolate import interp1d
pgrid = np.sqrt(bgrid)
one_minus = interp1d(pgrid, 1 - ggrid, kind="cubic")
from scipy.special import sici
def Ffrac(Tt):
    """fraction of the time kernel within |t| < T (T in units of 2 Omega r^2/c^2): 1 - (2/pi) int (1-g(beta)) sin(beta T)/beta"""
    pmax = pgrid[-1]; b1 = 1e-2
    vA = quad(lambda p_: float(one_minus(p_)) * 2 * math.sin(p_ * p_ * Tt) / p_ if p_ > 0 else 0.0, 0, math.sqrt(b1), limit=400, epsabs=1e-13)[0]
    vB = quad(lambda b_: float(one_minus(math.sqrt(b_))) / b_, b1, pmax ** 2, weight="sin", wvar=Tt, limit=400)[0]
    tail = math.pi / 2 - sici(pmax ** 2 * Tt)[0]                 # integral_{B}^{inf} sin(beta T)/beta with 1 - g = 1
    return 1 - (2 / math.pi) * (vA + vB + tail)
T50 = brentq(lambda T_: Ffrac(T_) - 0.5, 1e-3, 1e2, xtol=1e-6)
t50_units = 2 * T50                                              # t_50 in units of Omega r^2 / c^2
P(f"  B4 g(beta) at beta = 0.1, 1, 10: {g_beta(0.1):.4f}, {g_beta(1):.4f}, {g_beta(10):.4e}; response before the source = 0.5 (evenness, BY CONSTRUCTION)")
P(f"  B4 half-mass time t_50 = {t50_units:.4f} Omega r^2/c^2")
illus = {}
for f in FOOTS:
    for rk in (10, 20, 30):
        i_ = int(np.argmin(np.abs(Rr - rk * KPC)))
        vobs = dat[i_, 1] * 1e3
        tsec = t50_units * vobs * Rr[i_] / C_SI ** 2
        illus[f"{f}|{rk}kpc"] = dict(v_kms=vobs / 1e3, t50_yr_full_rotation=tsec / 3.156e7, t50_s_eps_omega=tsec * eps_om[f])
P(f"  B4 illustration (hypothetical medium rotating like NGC 3198's stars): t_50 = {illus['canonical|10kpc']['t50_yr_full_rotation']:.1f} / "
  f"{illus['canonical|20kpc']['t50_yr_full_rotation']:.1f} / {illus['canonical|30kpc']['t50_yr_full_rotation']:.1f} yr at 10/20/30 kpc; "
  f"with the B2-forced fraction eps_omega: <= {max(v_['t50_s_eps_omega'] for v_ in illus.values()):.2e} s")
B_["B4_t50_units_Omega_r2_over_c2"] = t50_units; B_["B4_illustration"] = illus
# B5 cosmic clock: exact boost
beta_, chip = sp.symbols("beta chi_p", positive=True)
gb = 1 / sp.sqrt(1 - beta_ ** 2)
uB = sp.Matrix([gb, gb * beta_, 0, 0]); eta_m = sp.diag(-1, 1, 1, 1)
hB = eta_m.inv() + uB * uB.T
dchib = sp.Matrix([-chip, 0, 0, 0])                                # d chibar/dx0 = -|chibar'| (S1d sign)
uv2 = sp.simplify((dchib.T * hB * dchib)[0])
P(f"  B5 medium moving at beta = v/c through the cosmic chibar(x0): h^mn d chibar d chibar = {uv2}  -> u_v = gamma beta |chibar'|")
# frozen-coefficient FRW expansion agrees: s contains (K rho/(3H))^2 (xi_t^2 + eta_t^2)
s_frw = sp.factor(Bfrw["s"].coeff(eps, 2))
P(f"  B5 FRW machinery: u^2 at O(eps^2) = {s_frw}")
clock_rate = OMC * H0 / 2                                           # |chibar_dot|/c^2 = K rho_c/(3H) at z = 0  [1/s]
P(f"  B5 |chibar'| /c = K rho_c c/(3 H0) -> u_v = (Omega_c H0/2) gamma v = {clock_rate:.4e} s^-1 x v")
B_["B5_uv2"] = str(uv2); B_["B5_rate_per_s"] = clock_rate
cosmic_clock = sp.simplify(uv2) != 0
LAB_B = ["NOW = MEDIUM SLICES FOR IRROTATIONAL FLOW ONLY" if vort else "GLOBAL NOW"]
if cosmic_clock: LAB_B.append("COSMIC CLOCK")
LAB_B.append("LAW IN MEDIUM FRAME (by construction)")
P(f"  (b) labels: {LAB_B}")
RES["labels"]["b"] = LAB_B; RES["B"] = B_
guard("B")

# ================================================================================================ C. L95
P("\n==================== C. L95 ====================")
C_ = {}
dchi_f = Bfrw["fields"][2]; dlam_f = Bfrw["fields"][3]
d0chi = sp.Derivative(dchi_f, x0); d0lam = sp.Derivative(dlam_f, x0)
pchi_frw = sp.simplify(sp.diff(L2f, d0chi)); A_frw = sp.simplify(sp.diff(L2f, d0chi, 2)); A_lam = sp.simplify(sp.diff(L2f, d0lam, 2))
Bst = k3["par"]["B"]; L2st = k3["par"]["L2"]
dchi_s = Bst["fields"][2]
pchi_st = sp.simplify(sp.diff(L2st, sp.Derivative(dchi_s, x0)).subs({Bst["fields"][0]: 0, Bst["fields"][1]: 0}).doit())
A_st = sp.simplify(sp.diff(L2st, sp.Derivative(dchi_s, x0), 2))
P(f"  C1 static medium frame (medium unperturbed): p_chi = {pchi_st};  A = d^2L/d(chi_dot)^2 = {A_st}")
P(f"  C1 FRW: p_chi = {pchi_frw};  A = {A_frw};  d^2L/d(lam_dot)^2 = {A_lam}")
P("  C2 FRW Hamiltonian: p_chi + 3 h a^3 dlam = 0 and p_lam = 0 are second class for h != 0 (bracket 3 h a^3); eliminating dlam leaves")
P("     one canonical pair (dchi, p_chi) with H LINEAR in p_chi (A = 0): a first-order (parabolic) pair, unbounded in p_chi.")
P("     At h = 0 the bracket vanishes: p_chi ~ 0 and p_lam ~ 0 are constraints and the pair carries no degree of freedom.")
P("     L95's obstruction A A'/2 = 0 identically on both backgrounds.")
satisfies = (A_st == 0) and (A_frw == 0)
C_.update(p_chi_static=str(pchi_st), A_static=str(A_st), p_chi_frw=str(pchi_frw), A_frw=str(A_frw), dof_jump="0 (theta = 0) -> 1 (theta != 0)")
LAB_C = ["SATISFIES L95" if satisfies else "CONFLICT WITH L95"]
LAB_C.append("EVADES L31/DC-019 alpha_3 horn (premise 'non-dynamical foliation' fails: the frame is the varied medium; alpha_3 = 0 by the "
             "semi-conservative theorem, CFG938 S3b) -- BY CONSTRUCTION")
P(f"  (c) labels: {LAB_C}")
P("      reading: the MOND function sits on a non-propagating field (A = 0) and the foliation is supplied by the medium, as L95 requires;")
P("      L95 is silent on the linear-in-momentum structure that the medium's expansion creates (theta != 0).")
RES["labels"]["c"] = LAB_C; RES["C"] = C_
guard("C")

# ================================================================================================ D. PREFERRED-FRAME SIZE
P("\n==================== D. PREFERRED-FRAME SIZE ====================")
D_ = {}
# D1 relativistic simultaneity of the local medium clock (uniform motion)
kx_, ky_, wv_ = sp.symbols("k_x k_y w", positive=True); cth = sp.Symbol("cos_theta", real=True)
kvec2 = kx_ ** 2 + ky_ ** 2
chi_hat = -1 / kvec2                                               # medium-frame Poisson per (K rho_hat)
phi_hat = -1 / (kvec2 - (kx_ * wv_) ** 2 / cc_ ** 2)                # retarded, source moving along x at w
ratio = sp.simplify(chi_hat / phi_hat)
C2 = sp.simplify((ratio - 1).subs({kx_: sp.Symbol("kk") * cth, ky_: sp.Symbol("kk") * sp.sqrt(1 - cth ** 2)}))
P(f"  D1 chi_hat/Phi_hat = {ratio}  ->  C2(theta) = {C2}  (max |C2| = (w/c)^2; even in w: no alpha_1-type term)")
D_["D1_C2"] = str(C2)
fc_scr = lambda r__, L_: (r__ / L_) ** 2
fc_uns = lambda r__, M_, a0_: a0_ * r__ ** 2 / (G_SI * M_)
TEST = {"solar_surface": (RSUN, MSUN, "alpha2_weak"), "NS_surface": (1e4, 1.4 * MSUN, "alpha2_strong")}
FCMULT = 1.0
D1 = {}
for tn, (rt, Mt, bn) in TEST.items():
    for lk, Lv in LSTAR.items():
        for f in FOOTS:
            fc = 1.0 if MUT else fc_scr(rt, Lv)
            a2 = fc * 1.0                                          # max|C2|/(w/c)^2 = 1
            D1[f"{tn}|{lk}|{f}"] = dict(alpha2_eff=a2, bound=BOUND[bn], ratio=a2 / BOUND[bn], fc_unscreened_context=fc_uns(rt, Mt, A0[f]))
P("  D1 alpha2_eff = f_c(r) (w-independent):")
for k_, v_ in D1.items():
    P(f"    {k_:28s} alpha2_eff = {v_['alpha2_eff']:.3e}  bound {v_['bound']:.1e}  ratio {v_['ratio']:.2e}   (unscreened ceiling f_c = {v_['fc_unscreened_context']:.2e}, context)")
D_["D1"] = D1
# D2 Newtonian Doppler in the Solar System (CFG770 backgrounds; point-mass Galaxy at 8.2 kpc)
def rho_bg(gNe, a0):
    Mg = gNe * R_SUN_GAL ** 2 / G_SI
    def uR(R_): return law_u(G_SI * Mg / R_ ** 2, a0)
    dR = R_SUN_GAL * 1e-4
    dy = ((R_SUN_GAL + dR) ** 2 * uR(R_SUN_GAL + dR) - (R_SUN_GAL - dR) ** 2 * uR(R_SUN_GAL - dR)) / (2 * dR)
    return dy / (K_SI * R_SUN_GAL ** 2)
D2 = {}; bgchk = []
for f in FOOTS:
    a0 = A0[f]
    for (ge, ue_f) in CFG770_BG[f]:
        ue = ue_f * a0; gNe = ge - ue
        bgchk.append(abs(Rrem(ue, a0) / gNe - 1))
        rhoe = rho_bg(gNe, a0)
        for lk, Lv in LSTAR.items():
            cs2 = K_SI * Lv ** 2 / 2 * rhoe
            for rn, rt in (("R_sun", RSUN), ("1AU", AU)):
                kv = 1 / rt
                w2min = cs2 * kv ** 2 + K_SI * rhoe * min(Rp(ue, a0), Rrem(ue, a0) / ue)
                for wl, wv in WS.items():
                    xq = (kv * wv) ** 2 / w2min
                    Fm1 = abs(xq / (1 - xq))
                    fc = 1.0 if MUT else fc_scr(rt, Lv)
                    a2 = Fm1 * fc / (wv / C_SI) ** 2
                    D2[f"{f}|ge{ge:.2e}|{lk}|{rn}|w{wl}"] = dict(x=xq, F_minus_1=Fm1, alpha2_eff=a2, rho_e=rhoe, cs_kms=math.sqrt(cs2) / 1e3)
P(f"  D2 CFG770 background consistency R(u_e)/g_Ne - 1: max {max(bgchk):.2e}")
worst_D2 = {}
for rn, bn in (("R_sun", "alpha2_weak"), ("1AU", "alpha2_weak")):     # frozen text: D2 scored at both E1 radii
    sel = {k_: v_ for k_, v_ in D2.items() if f"|{rn}|" in k_}
    kmax = max(sel, key=lambda k_: sel[k_]["alpha2_eff"])
    worst_D2[rn] = dict(key=kmax, **sel[kmax], bound=BOUND[bn], ratio=sel[kmax]["alpha2_eff"] / BOUND[bn])
    P(f"  D2 worst alpha2_eff at {rn}: {sel[kmax]['alpha2_eff']:.3e} ({kmax}; |F-1| = {sel[kmax]['F_minus_1']:.4f}, x = {sel[kmax]['x']:.3e}, "
      f"c_s = {sel[kmax]['cs_kms']:.3e} km/s); bound {BOUND[bn]:.0e}; ratio {worst_D2[rn]['ratio']:.2e}")
sel1 = {k_: v_ for k_, v_ in D2.items() if "|1AU|" in k_}
P(f"  D2 at 1 AU: |F-1| range {min(v_['F_minus_1'] for v_ in sel1.values()):.4f}-{max(v_['F_minus_1'] for v_ in sel1.values()):.4f}; "
  f"rows >= 10x bound: {[k_ for k_, v_ in sel1.items() if v_['alpha2_eff'] >= 10 * BOUND['alpha2_weak']]}")
# POST HOC (amendment A1; no class weight): compare the observable itself, not alpha2 normalised by the tabulated w
WREF = 370e3; A_spin = BOUND["alpha2_weak"] * (WREF / C_SI) ** 2
PULL_BOUND_1AU = 4.2157e-15 / 0.1152                               # CFG770 T3 (cfg770.out:36): sunward pull bound at 1 AU
ph = {}
for rn, rt in (("R_sun", RSUN), ("1AU", AU)):
    sel = {k_: v_ for k_, v_ in D2.items() if f"|{rn}|" in k_}
    dPhiU = max(v_["F_minus_1"] * (rt / LSTAR[k_.split("|")[2]]) ** 2 for k_, v_ in sel.items())
    da = max(v_["F_minus_1"] * GMSUN / LSTAR[k_.split("|")[2]] ** 2 for k_, v_ in sel.items())
    ph[rn] = dict(dPhi_over_U=dPhiU, A_spin_bound=A_spin, delta_a=da, pull_bound_1AU=PULL_BOUND_1AU)
P(f"  D2 POST HOC (amendment A1, no class weight): solar surface dPhi/U = {ph['R_sun']['dPhi_over_U']:.2e} vs alpha2 1e-7 x (370 km/s/c)^2 = {A_spin:.2e}; "
  f"1 AU frame-dependent pull <= {ph['1AU']['delta_a']:.2e} m/s^2 vs CFG770 T3 sunward-pull bound {PULL_BOUND_1AU:.2e} (ratio {ph['1AU']['delta_a'] / PULL_BOUND_1AU:.2e})")
D_["D2_posthoc_A1"] = ph
D_["D2_solar"] = dict(worst=worst_D2, rho_e_example=list(D2.values())[0]["rho_e"])
# D2 NGC 3198 deep MOND
D2n = {}
for f in FOOTS:
    a0 = A0[f]; u_arr, rho_arr = u_rho_profile(gNb, Rr, a0)
    for lk, Lv in LSTAR.items():
        vc = []; F370 = []
        for i_ in range(len(Rr)):
            if rho_arr[i_] <= 0: continue
            kv = 1 / Rr[i_]
            w2min = K_SI * Lv ** 2 / 2 * rho_arr[i_] * kv ** 2 + K_SI * rho_arr[i_] * min(Rp(u_arr[i_], a0), Rrem(u_arr[i_], a0) / u_arr[i_])
            vc.append(math.sqrt(w2min) / kv)
            out_ = {}
            for wl, wv in WS.items():
                xq = (kv * wv) ** 2 / w2min; out_[wl] = abs(xq / (1 - xq))
            F370.append(out_)
        D2n[f"{f}|{lk}"] = dict(vcrit_kms_min=min(vc) / 1e3, vcrit_kms_max=max(vc) / 1e3,
                               Fm1_w30_median=float(np.median([q["30"] for q in F370])), Fm1_w370_median=float(np.median([q["370"] for q in F370])))
        P(f"  D2 NGC 3198 {f:9s} L*={lk:5s}: v_crit = {min(vc) / 1e3:.1f}-{max(vc) / 1e3:.1f} km/s; median |F-1| at w = 30 / 370 km/s: "
          f"{D2n[f'{f}|{lk}']['Fm1_w30_median']:.3f} / {D2n[f'{f}|{lk}']['Fm1_w370_median']:.3f}  (no record bound)")
D_["D2_NGC3198"] = D2n
# D3 cosmic clock
D3 = {}
for f in FOOTS:
    a0 = A0[f]
    for wl, wv in WS.items():
        gb_ = 1 / math.sqrt(1 - (wv / C_SI) ** 2)
        uv = clock_rate * gb_ * wv
        D3[f"{f}|w{wl}|uv_over_a0"] = uv / a0
P("  D3 u_v/a0 = (Omega_c H0/2) gamma w / a0: " + ", ".join(f"{k_} {v_:.3e}" for k_, v_ in D3.items()))
D3i = {}
for f in FOOTS:
    a0 = A0[f]
    for (ge, ue_f) in CFG770_BG[f]:
        ue = ue_f * a0
        dlnRp = (math.log(Rp(ue * 1.0001, a0)) - math.log(Rp(ue * 0.9999, a0))) / (math.log(1.0001) - math.log(0.9999))
        dlnRu = (math.log(Rrem(ue * 1.0001, a0) / (ue * 1.0001)) - math.log(Rrem(ue * 0.9999, a0) / (ue * 0.9999))) / (math.log(1.0001) - math.log(0.9999))
        MA = max(abs(dlnRp), abs(dlnRu))
        for lk, Lv in LSTAR.items():
            for wl, wv in WS.items():
                uv = clock_rate * wv
                da = (uv / ue) * MA * GMSUN / Lv ** 2
                gE = GMSUN / AU ** 2
                a1 = da / (gE * (wv / C_SI) * (VEARTH / C_SI))
                D3i[f"{f}|ge{ge:.2e}|{lk}|w{wl}"] = dict(M_A=MA, delta_a=da, alpha1_eff=a1, ratio=a1 / BOUND["alpha1"])
kw3 = max(D3i, key=lambda k_: D3i[k_]["alpha1_eff"])
P(f"  D3(i) Solar System worst alpha1_eff = {D3i[kw3]['alpha1_eff']:.3e} ({kw3}; M_A = {D3i[kw3]['M_A']:.2f}; delta_a = {D3i[kw3]['delta_a']:.2e} m/s^2); "
  f"bound 3.4e-5; ratio {D3i[kw3]['ratio']:.2e}")
D3ii = {}
for f in FOOTS:
    a0 = A0[f]
    for bi, (Mb_, rb) in enumerate(H72):
        for wl, wv in WS.items():
            uv = clock_rate * wv
            rx = math.sqrt(G_SI * Mb_ * MSUN * a0) / uv / MPC
            D3ii[f"{f}|bin{bi + 1}|w{wl}"] = dict(r_x_Mpc=rx, bound_Mpc=rb, ratio=rx / rb)
for f in FOOTS:
    P(f"  D3(ii) {f:9s} r_x / r_end-bound per bin (w = 30 / 370 / 1000 km/s): " + "; ".join(
        f"bin{bi + 1} " + "/".join(f"{D3ii[f'{f}|bin{bi + 1}|w{wl}']['ratio']:.2f}" for wl in WS) for bi in range(4)))
D_["D3"] = D3; D_["D3i"] = D3i; D_["D3ii"] = D3ii
# labels for (d)
ratios_strict = [v_["ratio"] for v_ in D1.values()] + [worst_D2["R_sun"]["ratio"], worst_D2["1AU"]["ratio"]] + [v_["ratio"] for v_ in D3i.values()]
r_x_ratios = [v_["ratio"] for v_ in D3ii.values()]
LAB_D = []
excl = any(r_ >= 10 for r_ in ratios_strict) or any(r_ <= 0.1 for r_ in r_x_ratios)
under_reasons = []
if any(0.1 < r_ < 10 for r_ in ratios_strict): under_reasons.append("an alpha_eff within 10x of its bound")
if any(0.1 < r_ < 10 for r_ in r_x_ratios): under_reasons.append("cosmic-clock crossover r_x within 10x of an h72 KiDS r_end bound")
under_reasons.append("D2 on NGC 3198 (MOND-regime Doppler) has no record bound")
under = bool(under_reasons)
P(f"  (d) UNDERDETERMINED reasons: {under_reasons}")
D_["under_reasons"] = under_reasons
if excl: LAB_D.append("EXCLUDED")
if under: LAB_D.append("UNDERDETERMINED")
if all(r_ <= 0.1 for r_ in ratios_strict): LAB_D.append("MEDIUM CLOCK")
if cosmic_clock: LAB_D.append("COSMIC CLOCK")
P(f"  (d) max strict alpha ratio = {max(ratios_strict):.2e}; r_x ratios span {min(r_x_ratios):.2f}-{max(r_x_ratios):.2f}; "
  f"in (0.1, 10): {[k_ for k_, v_ in D3ii.items() if 0.1 < v_['ratio'] < 10]}")
P(f"  (d) labels: {LAB_D}")
RES["labels"]["d"] = LAB_D; RES["D"] = D_
guard("D")

# ================================================================================================ E. c_T
P("\n==================== E. c_T ====================")
E_ = {}
Fp = sp.Symbol("Fp")
# robust route: evaluate on F = cos(x0 - kz zeta) and average via coefficient of k^2
kzs = sp.Symbol("kz", positive=True)
plane = sp.cos(kzs * zeta)
Hpw = (Ap * EP + Ax * EX) * plane
gP = sp.diag(-1, 1, 1, 1)
for i in range(3):
    for j in range(3):
        gP[i + 1, j + 1] += eps * Hpw[i, j]
gPi = gP.inv()
GamP = {}
for i in range(1, 4):
    for j in range(1, 4):
        GamP[(i, j)] = sp.expand(sp.diff(sum(gPi[3, d_] * (sp.diff(gP[d_, i], XX[j]) + sp.diff(gP[d_, j], XX[i]) - sp.diff(gP[i, j], XX[d_]))
                                             for d_ in range(4)) / 2, eps).subs(eps, 0))
trGP = sum(GamP[(i, i)] for i in range(1, 4))
tauP = {(i, j): -u0 * (GamP[(i, j)] - (sp.Rational(1, 3) * trGP if i == j else 0)) for i in range(1, 4) for j in range(1, 4)}
ttq_pw = sp.expand(sum(tauP[k_] ** 2 for k_ in tauP))
P(f"  E1 trace Gamma^z_kk at first order (TT) = {sp.simplify(trGP)}")
grad_pw = sp.expand(sum(sum(sp.diff((Ap * EP + Ax * EX)[i, j] * plane, X) ** 2 for X in (x, y, z)) for i in range(3) for j in range(3)))
# both are proportional to kz^2 sin^2(kz zeta): ratio is the quadratic form q
q_form = sp.simplify(ttq_pw / grad_pw / u0 ** 2)
qpp = sp.simplify(q_form.subs({Ap: 1, Ax: 0})); qxx = sp.simplify(q_form.subs({Ap: 0, Ax: 1}))
qmix = sp.simplify(q_form.subs({Ap: 1, Ax: 1}) * 2 - qpp - qxx)
P(f"  E1 q = Sum(Gamma^z)^2 / Sum(grad h)^2 : plus {qpp}, cross {qxx}, mixing {sp.simplify(qmix)}")
# dispersion: (c^4/16)[(d0 h)^2 - (grad h)^2] - (3 L*^2/8) u0^2 Sum(Gamma^z)^2 -> c_T^2/c^2 = 1 + 6 L*^2 u0^2 q / c^4
CT = sp.simplify(6 * qpp); CTx = sp.simplify(6 * qxx)
qs_num = [float(qpp.subs(th_k, t_)) for t_ in np.linspace(0, math.pi / 2, 7)] + [float(qxx.subs(th_k, t_)) for t_ in np.linspace(0, math.pi / 2, 7)]
Cmax = 6 * max(qs_num); Cmin = 6 * min(qs_num)
P(f"  E1 delta(c_T^2/c^2) = C_T L*^2 u0^2 / c^4 with C_T in [{Cmin:.4f}, {Cmax:.4f}] over angle and polarisation (sign +: superluminal)")
if MUT:
    c13 = 0.01
    dcT_mut = 1 / math.sqrt(1 + c13) - 1
    P(f"  MU1 aether c13 = 0.01: c_T/c - 1 = {dcT_mut:.4e}")
# mass-like terms from W (size at 100 Hz): K W expansion with s = g^zz u0^2
kLIGO = 2 * math.pi * 100 / C_SI
def mass_ratio(u_, a0):
    KWscale = max(Dfull(u_, a0) * u_, (1 + Rp(u_, a0)) * u_ ** 2)
    return KWscale / (C_SI ** 4 / 16 * kLIGO ** 2)
E_["mass_like_ratio_at_wall"] = {f: mass_ratio(A0[f] * 0.999, A0[f]) for f in FOOTS}
P(f"  E1 W mass-like terms relative to the EH k^2 term at 100 Hz (u -> 0.999 a0): canonical {E_['mass_like_ratio_at_wall']['canonical']:.1e}, alt {E_['mass_like_ratio_at_wall']['alt']:.1e}; "
  "constant lambda_0 term is a total derivative (sqrt(-g) g^mn Gamma^z_mn = -d_m(sqrt(-g) g^mz))")
# E2 local worst
E2 = {}
for f in FOOTS:
    for lk, Lv in LSTAR.items():
        E2[f"{f}|{lk}"] = Cmax / 2 * (Lv * A0[f] / C_SI ** 2) ** 2
P("  E2 local worst |c_T/c - 1| at u0 = a0: " + ", ".join(f"{k_} {v_:.3e}" for k_, v_ in E2.items()))
# E3 path model
def int_u2(Mb_, a0):
    GM = G_SI * Mb_ * MSUN
    def integ(lr):
        r__ = math.exp(lr); gN = GM / r__ ** 2
        return law_u(gN, a0) ** 2 * r__
    return quad(integ, math.log(1e-6 * PC), math.log(1e4 * MPC), limit=500)[0]
E3 = {}
for f in FOOTS:
    for Mb_ in (1e11, 1e12):
        I1 = int_u2(Mb_, A0[f]); Itot = 2 * I1
        for lk, Lv in LSTAR.items():
            val = Cmax / 2 * Lv ** 2 * Itot / (C_SI ** 4 * D_GW)
            Lmax = math.sqrt(BOUND["cT_hi"] * 2 * C_SI ** 4 * D_GW / (Cmax * Itot)) / KPC
            E3[f"{f}|Mb{Mb_:.0e}|{lk}"] = dict(int_u2_one_galaxy=I1, dcT=val, Lstar_max_kpc=Lmax)
    Lmax_w = math.sqrt(BOUND["cT_hi"] * 2 * C_SI ** 4 / (Cmax * A0[f] ** 2)) / KPC
    E3[f"{f}|worstcase_Lstar_max_kpc"] = Lmax_w
for k_, v_ in E3.items():
    P(f"  E3 {k_:30s} {v_ if isinstance(v_, float) else ''}" + (f"<c_T/c - 1> = {v_['dcT']:.3e}; L*_max = {v_['Lstar_max_kpc']:.3e} kpc" if isinstance(v_, dict) else " kpc (worst case)"))
if MUT:
    path_vals = [1 / math.sqrt(1 + 0.01) - 1]
else:
    path_vals = [v_["dcT"] for v_ in E3.values() if isinstance(v_, dict)]
path_ok = all(BOUND["cT_lo"] < v_ < BOUND["cT_hi"] for v_ in path_vals)
worst_ok = all(BOUND["cT_lo"] < v_ < BOUND["cT_hi"] for v_ in E2.values())
excl_e = any(not (BOUND["cT_lo"] < v_["dcT"] < BOUND["cT_hi"]) for k_, v_ in E3.items() if isinstance(v_, dict) and "Mb1e+11" in k_) if not MUT else not path_ok
LAB_E = ["EXCLUDED"] if excl_e else (["ROBUST PASS"] if (path_ok and worst_ok) else (["PASS"] if path_ok else ["UNDERDETERMINED"]))
if Cmax != 0 and not MUT:
    LAB_E.append("CFG938 A5 'c_T = c (structural)' CORRECTED: c_T != c inside the medium at O(L*^2 u^2/c^4); a computed bound, not structural")
P(f"  (e) labels: {LAB_E}")
E_.update(C_T_range=[Cmin, Cmax], E2=E2, E3=E3, q_plus=str(qpp), q_cross=str(qxx))
RES["labels"]["e"] = LAB_E; RES["E"] = E_
guard("E")

# ================================================================================================ OVERALL
order = ["EXCLUDED", "CONFLICT WITH L95", "ILL-POSED-IVP", "UNDERDETERMINED", "MEDIUM CLOCK", "NO PREFERRED TIME"]
alllab = [l_ for v_ in RES["labels"].values() for l_ in v_]
head = next((o_ for o_ in order if any(l_.startswith(o_) for l_ in alllab)), "UNDERDETERMINED")
RES["overall"] = dict(headline=head, all=alllab)
# POST HOC reading (amendment A1; no class weight): D2 scored on the observable (solar-surface dPhi/U vs alpha2 x (w_ref/c)^2;
# 1 AU pull vs CFG770 T3), not on alpha2 normalised by the tabulated w at a radius where the solar-spin bound was not measured
if not MUT:
    ph = D_["D2_posthoc_A1"]
    r_ph = [v_["ratio"] for v_ in D1.values()] + [ph["R_sun"]["dPhi_over_U"] / ph["R_sun"]["A_spin_bound"], ph["1AU"]["delta_a"] / ph["1AU"]["pull_bound_1AU"]] + [v_["ratio"] for v_ in D3i.values()]
    LAB_D_ph = []
    if any(r_ >= 10 for r_ in r_ph) or any(r_ <= 0.1 for r_ in r_x_ratios): LAB_D_ph.append("EXCLUDED")
    LAB_D_ph.append("UNDERDETERMINED")
    if all(r_ <= 0.1 for r_ in r_ph): LAB_D_ph.append("MEDIUM CLOCK")
    if cosmic_clock: LAB_D_ph.append("COSMIC CLOCK")
    lab_ph = dict(RES["labels"]); lab_ph["d"] = LAB_D_ph
    all_ph = [l_ for v_ in lab_ph.values() for l_ in v_]
    head_ph = next((o_ for o_ in order if any(l_.startswith(o_) for l_ in all_ph)), "UNDERDETERMINED")
    RES["posthoc_A1"] = dict(d_labels=LAB_D_ph, max_ratio=max(r_ph), headline=head_ph)
P("\n==================== OVERALL ====================")
for k_, v_ in RES["labels"].items():
    P(f"  ({k_}) {v_}")
P(f"  HEADLINE (frozen rule): {head}")
if not MUT:
    P(f"  POST HOC (amendment A1, no class weight): (d) {RES['posthoc_A1']['d_labels']} (max ratio {RES['posthoc_A1']['max_ratio']:.2e}); "
      f"headline {RES['posthoc_A1']['headline']}")

# ================================================================================================ MUTATE
if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    bite = {}
    bite["MU1"] = chk("MU1_aether_c13_flags_GW170817", abs(1 / math.sqrt(1.01) - 1) >= 1e-3 and "EXCLUDED" in LAB_E,
                      f"|c_T/c - 1| = {abs(1 / math.sqrt(1.01) - 1):.3e}; (e) = {LAB_E}")
    bite["MU2"] = chk("MU2_frame_in_metric_sector_excluded", "EXCLUDED" in LAB_D, f"f_c = 1: max alpha ratio = {max(ratios_strict):.2e}; (d) = {LAB_D}")
    Mi, _, _ = frw_system(intrinsic=True)
    cchi_i = sp.expand(Mi[3, 2]).coeff(sig); clam_i = sp.expand(Mi[2, 3]).coeff(sig)
    deti = sp.factor(Mi.det())
    P(f"  MU3 intrinsic Laplacian: chi-eq sigma coefficient {cchi_i}, lambda-eq sigma coefficient {clam_i}; det = {deti}")
    polyi = sp.Poly(sp.numer(sp.together(deti)), sig)
    Kmv, Hz = frozen(0.0)
    _, mxi, sli, firesi = hadamard(1.0, Kmv, LSTAR["24pc"] * Hz / C_SI, poly=polyi)
    P(f"  MU3 Hadamard: max Re sigma = {[f'{m_:.3e}' for m_ in mxi]}; fires: {firesi}")
    bite["MU3"] = chk("MU3_intrinsic_laplacian_removes_ill_posedness", cchi_i == 0 and clam_i == 0 and not firesi,
                      "parabolic coefficients vanish and the Hadamard test does not fire: the A-iii label flips")
    t50_0 = 0.0 if Ffrac(1e-6) > 0.5 - 1e-9 else None
    gz = g_beta(0.0)
    brz = sp.simplify(br.subs(Om, 0))
    bite["MU4"] = chk("MU4_no_vorticity_no_smear", brz == 0 and abs(gz - 1) < 1e-6,
                      f"Omega = 0: bracket = {brz}; g(beta) = g(0) = {gz:.6f} for all nu -> kernel = delta(t), t_50 = 0")
    allb = all(bite.values())
    P(f"\n  MUTATE: {'ALL TEETH BITE (exit 1 by design)' if allb else 'A TOOTH FAILED TO BITE'}")
    dump(); sys.exit(1 if allb else 2)

P(f"\n  runtime {time.time() - T0:.1f} s; peak RSS {rss() / 1e9:.3f} GB")
dump()
sys.exit(0 if K_ALL else 2)

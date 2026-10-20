"""CFG938 -- the cold-energy medium as a relativistic continuum (fluid EFT of comoving label fields).
Criteria: FROZEN_CRITERIA.md (7a0d41e8b, committed alone before this script).
Run (one core, one process, < 1 GB):
    OMP_NUM_THREADS=1 nice -n 10 python3 cfg938.py                      -> cfg938.out, cfg938_results.json (K + main)
    CFG938_STAGE=K ...                                                  -> cfg938_K.out, cfg938_results_K.json (K only)
    CFG938_MUTATE=1 ...                                                 -> cfg938_MUTATE.out, cfg938_results_MUTATE.json
MUTATE exits 1 by design when every tooth bites (2 if a tooth fails to bite).
kappa = 1/2 FITTED; footings never pooled; cold energy's mass required; not theory closed."""
import os, sys, io, json, math, time, resource, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
MUT = os.environ.get("CFG938_MUTATE", "0") == "1"
STAGE = os.environ.get("CFG938_STAGE", "MAIN").upper()
TAG = "_MUTATE" if MUT else ("_K" if STAGE == "K" else "")
OUT = []; RES = {"lane": "CFG938", "criteria": "7a0d41e8b", "mutate": MUT, "stage": STAGE, "checks": {}}
T0 = time.time()
RSS_LIMIT = 1.0e9


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def rss_guard(where=""):
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    r = r if sys.platform == "darwin" else r * 1024                    # bytes on macOS, kB on Linux
    if r > RSS_LIMIT:
        P(f"RSS GUARD: {r / 1e9:.2f} GB > 1 GB at {where}; aborting"); dump(); sys.exit(3)
    return r


def chk(name, ok, detail=""):
    RES["checks"][name] = {"pass": bool(ok), "detail": str(detail)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return bool(ok)


def dump():
    RES["runtime_s"] = round(time.time() - T0, 2); RES["peak_rss_GB"] = round(rss_guard_val() / 1e9, 3)
    json.dump(RES, open(os.path.join(HERE, f"cfg938_results{TAG}.json"), "w"), indent=1, default=str)
    open(os.path.join(HERE, f"cfg938{TAG}.out"), "w").write("\n".join(OUT) + "\n")


def rss_guard_val():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024


def is0(e):
    return sp.simplify(sp.expand(e)) == 0


# ------------------------------------------------------------------------------------------------ constants
sys.path.insert(0, LANES)
with contextlib.redirect_stdout(io.StringIO()):
    import CFG4_common as C4                                          # read-only: the record's footings
A0 = dict(C4.A0); FOOTS = ("canonical", "alt")
G_SI, C_SI, MSUN, PC, KPC = 6.67430e-11, 299792458.0, 1.98847e30, 3.0856775814913673e16, 3.0856775814913673e19
K_SI = 4 * math.pi * G_SI
assert abs(A0["canonical"] - 9.3603e-11) < 1e-15 and abs(A0["alt"] - 1.1312e-10) < 1e-15


def law_g(gN, a0):                                                    # canonical S2 law: g_N = g^2/(g + a0)
    return 0.5 * (gN + math.sqrt(gN * gN + 4.0 * gN * a0))


def Wfull_num(u, a0):                                                 # J/m^3; K W' = u/(1 - u/a0)
    return (-a0 * u - a0 * a0 * math.log1p(-u / a0)) / K_SI


P("CFG938  the cold-energy medium as a relativistic continuum" + ("   [MUTATE]" if MUT else "") + f"   stage={STAGE}")
P("  criteria 7a0d41e8b; kappa = 1/2 FITTED; footings never pooled; not theory closed")
P(f"  footings: canonical a0 = {A0['canonical']:.4e}, alt a0 = {A0['alt']:.4e} m/s^2")

# ================================================================================================ symbols shared
r, G, a0s, Ks, gam, m = sp.symbols("r G a_0 K gamma m", positive=True)
u, gN, gs = sp.symbols("u g_N g", positive=True)
Wfull = (-a0s * u - a0s ** 2 * sp.log(1 - u / a0s)) / (4 * sp.pi * G)            # W_full(u), K = 4 pi G
Wrem = Wfull - u ** 2 / (2 * 4 * sp.pi * G)
Dfull = sp.simplify(4 * sp.pi * G * sp.diff(Wfull, u))                            # u/(1 - u/a0)
Rrem = sp.simplify(4 * sp.pi * G * sp.diff(Wrem, u))                              # u^2/(a0 - u)


# ================================================================================================ REDUCED STATIC FUNCTIONAL
# Static weak-field limit of the continuum action (derivation in DERIVATION.md section 2):
#   L = -|grad Phi|^2/(2K) - (rho_b + rho_c) Phi - W(|grad chi|) - (gamma/2) rho_c^2 + lambda (lap chi - K rho_c).
# With Phi and chi on shell in spherical symmetry (Gauss: chi' = G M_c/r^2 = u), the energy is a functional of the
# medium's enclosed mass M_c(r) (its Lagrangian configuration variable).  'tcoef' scales the tether (M1 sets 0);
# 'Wuse' selects W_full (correct) or W_rem (M3).
def reduced_EL(tcoef, Wuse, with_stiff=True):
    Mc = sp.Function("M_c")(r); Mb = sp.Function("M_b")(r)
    Wfun = sp.Lambda(u, Wuse)
    Lr = (-G * (Mb + tcoef * Mc) ** 2 / (2 * r ** 2) + 4 * sp.pi * r ** 2 * Wfun(G * Mc / r ** 2)
          + (4 * sp.pi * r ** 2 * (gam / 2) * (sp.diff(Mc, r) / (4 * sp.pi * r ** 2)) ** 2 if with_stiff else 0))
    eq = sp.euler_equations(Lr, [Mc], [r])[0].lhs
    return eq, Mc, Mb


def EL_algebraic(tcoef, Wuse):
    """gamma -> 0 Euler-Lagrange expression as a function of (u, g_N) [u = G M_c/r^2, g_N = G M_b/r^2]."""
    eq, Mc, Mb = reduced_EL(tcoef, Wuse, with_stiff=False)
    e = eq.subs({Mc: u * r ** 2 / G, Mb: gN * r ** 2 / G}).doit()
    return sp.simplify(e)


def K1_sparc(tcoef, Wuse, label):
    """NGC 3198 (record SPARC file), Upsilon 0.61; solve the action's EL at every radius; compare with the closed law."""
    ex = EL_algebraic(tcoef, Wuse)
    f = sp.lambdify((u, gN, a0s, G), ex, "math")
    d = np.genfromtxt(os.path.join(REPO, "real_research", "data", "sparc_data", "NGC3198_rotmod.dat"), comments="#")
    R = d[:, 0] * KPC; Vg, Vd, Vb = d[:, 3] * 1e3, d[:, 4] * 1e3, d[:, 5] * 1e3
    gNb = (Vg * np.abs(Vg) + 0.61 * Vd * np.abs(Vd) + 0.61 * Vb * np.abs(Vb)) / R
    out = {}
    for foot in FOOTS:
        a0 = A0[foot]; rel = []; gNt = []
        for gn in gNb:
            lo = 0.5 * a0 if Wuse is Wrem else 0.0                    # M3: R(u) - u >= 0 only for u >= a0/2
            hi = a0 * (1 - 1e-15)
            fl, fh = f(lo + 1e-300, gn, a0, G_SI), f(hi, gn, a0, G_SI)
            if tcoef == 0:                                            # M1: EL = D_full(u) = 0 -> u = 0
                uu = 0.0 if abs(f(0.0 + 1e-300, gn, a0, G_SI)) < 1e-12 * a0 else float("nan")
            elif fl * fh > 0:
                uu = float("nan")
            else:
                uu = brentq(lambda x: f(x, gn, a0, G_SI), lo + 1e-300, hi, xtol=1e-30, rtol=1e-15, maxiter=500)
            g_cp = gn + tcoef * uu
            rel.append(abs(g_cp / law_g(gn, a0) - 1.0)); gNt.append(abs(g_cp / gn - 1.0))
        out[foot] = dict(max_rel_vs_law=float(np.nanmax(rel)), max_rel_vs_newton=float(np.nanmax(gNt)),
                         n=int(len(rel)), nan=int(np.sum(~np.isfinite(rel))))
    P(f"  K1[{label}] EL(gamma->0) = {sp.factor(ex)}")
    for foot in FOOTS:
        o = out[foot]
        P(f"     {foot:9s} N={o['n']}  max|g/g_law - 1| = {o['max_rel_vs_law']:.3e}   max|g/g_N - 1| = {o['max_rel_vs_newton']:.3e}"
          f"   unsolved = {o['nan']}")
    return ex, out


# ================================================================================================ K CONTROLS
P("\n==================== K CONTROLS ====================")
# ---- K2: FRW dust
t_, x_, y_, z_ = sp.symbols("t x y z", real=True); XX = [t_, x_, y_, z_]
af = sp.Function("a", positive=True)(t_)
gi_sym = {}; GI = sp.zeros(4, 4)
for i in range(4):
    for j in range(i, 4):
        gi_sym[(i, j)] = sp.Symbol(f"gi{i}{j}", real=True); GI[i, j] = GI[j, i] = gi_sym[(i, j)]


def stress_from(Lfun):
    """T_{mu nu} = -(2/sqrt(-g)) d(sqrt(-g) L)/d g^{mu nu} at fixed phi^I = x^I (d_mu phi^I = delta), symbolic g^{mu nu}."""
    sqrtg = 1 / sp.sqrt(-GI.det())
    Ld = sqrtg * Lfun(GI)
    T = sp.zeros(4, 4)
    for (i, j), s_ in gi_sym.items():
        dd = sp.diff(Ld, s_)
        T[i, j] = T[j, i] = (-2 if i == j else -1) * dd / sqrtg
    return T


def B_of(GIm):                                                        # B^{IJ} = g^{mu nu} d phi^I d phi^J with phi = x
    return GIm[1:, 1:]


def at_metric(T, diag):
    sub = {gi_sym[(i, j)]: (diag[i] if i == j else 0) for (i, j) in gi_sym}
    Tm = T.subs(sub).doit()
    gimat = sp.diag(*diag)
    return sp.simplify(gimat * Tm)                                    # T^mu_nu = g^{mu a} T_{a nu}


FRW = [-1, af ** -2, af ** -2, af ** -2]
nsym = sp.Symbol("n", positive=True)
Ffun = sp.Function("F")
Tfl = stress_from(lambda GIm: Ffun(sp.sqrt(B_of(GIm).det())))
Tmix_fl = at_metric(Tfl, FRW)
n_frw = sp.simplify(sp.sqrt(B_of(sp.diag(*FRW)).det()))
off = [sp.simplify(Tmix_fl[i, j]) for i in range(4) for j in range(4) if i != j]
iso = sp.simplify(Tmix_fl[1, 1] - Tmix_fl[2, 2]) == 0 and sp.simplify(Tmix_fl[2, 2] - Tmix_fl[3, 3]) == 0
Tdust = stress_from(lambda GIm: -m * sp.sqrt(B_of(GIm).det()))     # F = -m c^2 n (c = 1)
Tmix_d = at_metric(Tdust, FRW)
rho_d = sp.simplify(-Tmix_d[0, 0]); p_d = sp.simplify(Tmix_d[1, 1])
P(f"  FRW (x0 = ct): B^IJ = delta/a^2, n = {n_frw};  fluid T^mu_nu off-diagonal all zero: {all(o == 0 for o in off)}; T^i_i equal: {iso}")
P(f"  dust F = -m c^2 n:  rho = {rho_d}, p = {p_d}, w = {sp.simplify(p_d / rho_d)}")
k2 = chk("K2_FRW_dust_w0", all(o == 0 for o in off) and iso and sp.simplify(p_d) == 0 and sp.simplify(rho_d - m / af ** 3) == 0,
         f"rho = {rho_d}, p = {p_d}, w = 0 exactly; fluid stress diagonal and isotropic")
rss_guard("K2")

# ---- K3: Newtonian limit of sqrt(-g)(-m c^2 n) for a static medium
cc, Phi_s, Psi_s = sp.symbols("c Phi Psi", real=True)
eps = sp.Symbol("epsilon", positive=True)                              # bookkeeping: 1/c^2
Am = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"A{i}{j}", real=True))  # static Jacobian d_i phi^I
gsp = (1 - 2 * Psi_s * eps)                                           # g_ij = (1 - 2 Psi/c^2) delta_ij
n_static = sp.sqrt((Am * Am.T / gsp).det())
sqrtg_static = sp.sqrt(1 + 2 * Phi_s * eps) * gsp ** sp.Rational(3, 2)   # x0 = ct; S = int dt d^3x sqrt(-g) L
Ldust = sqrtg_static * (-m / eps) * n_static                          # -m c^2 n
detA = sp.Symbol("detA", positive=True)
Ldust = Ldust.subs((Am * Am.T).det(), detA ** 2)
Ldust = sp.simplify(Ldust.subs(sp.sqrt((Am * Am.T).det()), detA))
ser = sp.series(sp.simplify(Ldust), eps, 0, 1).removeO()
target = -m * detA / eps - m * detA * Phi_s
k3 = chk("K3_newtonian_limit", is0(ser - target),
         f"sqrt(-g)(-m c^2 n) = {sp.simplify(ser)}  (Psi drops out exactly for a static medium)")
rss_guard("K3")

# ---- K1: SPARC reduction
k1ex, k1out = K1_sparc(1, Wfull, "action: tether on, W_full")
k1_ok = all(k1out[f]["max_rel_vs_law"] < 1e-6 and k1out[f]["nan"] == 0 for f in FOOTS)
_ratio = sp.simplify(k1ex / (Rrem - gN))
k1sym = bool(_ratio.free_symbols == set() and _ratio != 0)
k1 = chk("K1_SPARC_NGC3198_reduction", k1_ok and k1sym,
         f"EL = +/-(R(u) - g_N) symbolically: {k1sym}; max rel dev canonical {k1out['canonical']['max_rel_vs_law']:.2e}, "
         f"alt {k1out['alt']['max_rel_vs_law']:.2e} (line < 1e-6)")
RES["K1"] = k1out
K_ALL = k2 and k3 and k1
P(f"  K controls: {'ALL PASS' if K_ALL else 'FAIL -> VOID'}")
RES["K_all"] = K_ALL

if STAGE == "K" and not MUT:
    dump(); P(f"  runtime {time.time() - T0:.1f} s"); sys.exit(0 if K_ALL else 1)


# ================================================================================================ dispersion (used by S5 and M2)
kk, th, rho0, u0, cl, epsI = sp.symbols("k theta rho_0 u_0 c epsilon_I", positive=True)
Dfun = sp.Lambda(u, Dfull)


def dispersion(gsign=1):
    """Quadratic action about a static medium (WKB, rest frame).  Potential per mode from
    E2 = -(K/2)|drho|^2/k^2 [self-gravity] + (1/2) dchi.Hess(W).dchi [tether] + (gamma/2)|drho|^2 [stiffness],
    drho = -i rho0 k.xi, dchi = -K drho/k^2 (medium-frame constraint).  Kinetic: rest mass + W(u) with
    u^2 = h^{mu nu} d chi d chi = |grad chi|^2 + gamma_L^2 (v.grad chi)^2/c^2."""
    Kk = 4 * sp.pi * G
    zhat = sp.Matrix([0, 0, 1]); khat = sp.Matrix([sp.sin(th), 0, sp.cos(th)])
    Hess = (sp.diff(Dfull, u).subs(u, u0) * zhat * zhat.T + (Dfull / u).subs(u, u0) * (sp.eye(3) - zhat * zhat.T)) / Kk
    drho2_coef = rho0 ** 2 * kk ** 2                                 # |drho|^2 = rho0^2 k^2 |khat.xi|^2
    dchi2 = Kk ** 2 / kk ** 4                                         # |dchi|^2 per |drho|^2
    tether = sp.Rational(1, 2) * (khat.T * Hess * khat)[0] * kk ** 2 * dchi2
    vmode = 2 * drho2_coef * (-(Kk / 2) / kk ** 2 + tether + gsign * gam / 2)     # coefficient of (1/2)|khat.xi|^2 -> V = v khat khat^T
    vmode = sp.simplify(vmode)
    # kinetic: expand W(u) with u^2 = u0^2 + (v_z u0)^2/c^2 (gamma_L -> 1 at O(v^2)); L_kin = 1/2 rho v^2 - (W'(u0) u0/(2c^2)) v_z^2
    vz = sp.Symbol("v_z", real=True)
    Wf = sp.Lambda(u, Wfull)
    ukin = sp.sqrt(u0 ** 2 + (vz * u0) ** 2 / cl ** 2)
    Lkin_W = -sp.series(Wf(ukin), vz, 0, 3).removeO() + Wf(u0)
    inert_z_corr = sp.simplify(-2 * Lkin_W.coeff(vz, 2))              # positive number subtracted from rho0 along z
    Imat = rho0 * sp.eye(3) - inert_z_corr * zhat * zhat.T
    V = vmode * khat * khat.T
    w2 = sp.Symbol("w2")
    charpoly = sp.factor((V - w2 * Imat).det())
    sols = sp.solve(sp.Eq(charpoly, 0), w2)
    w2L = [s_ for s_ in sols if sp.simplify(s_) != 0][0]
    return sp.simplify(vmode), inert_z_corr, sp.simplify(w2L), sols


def w2_numeric(w2L, a0v, u0v, gsign, rho0v=1.0):
    """omega^2 / (K rho0) on a k L* grid, all angles; c -> infinity limit printed separately."""
    f = sp.lambdify((kk, th, u0, a0s, rho0, G, gam, cl), w2L, "numpy")
    Gv = 1.0 / (4 * math.pi); Kv = 1.0                                 # units: K = 1, rho0 = 1 -> omega in sqrt(K rho0)
    Lstar = 1.0; gv = Kv * Lstar ** 2 / 2
    ks = np.logspace(-2, 5, 400); ths = np.linspace(0, math.pi / 2, 61)
    KK, TT = np.meshgrid(ks, ths)
    vals = f(KK, TT, u0v, a0v, rho0v, Gv, gv, 1e30)                 # sign of gamma is inside w2L
    return ks, ths, np.real(vals)


if MUT:
    P("\n==================== MUTATE (each tooth must bite) ====================")
    _, m1 = K1_sparc(0, Wfull, "M1: tether coefficient 0")
    m1_newton = all(m1[f]["max_rel_vs_newton"] < 1e-12 for f in FOOTS)
    m1_bite = m1_newton and not all(m1[f]["max_rel_vs_law"] < 1e-6 for f in FOOTS)
    chk("M1_no_tether_gives_Newton_and_K1_fails", m1_bite,
        f"max|g/g_N - 1| = {max(m1[f]['max_rel_vs_newton'] for f in FOOTS):.1e} (Newtonian); law dev "
        f"{min(m1[f]['max_rel_vs_law'] for f in FOOTS):.3f} > 1e-6")
    _, m3 = K1_sparc(1, Wrem, "M3: W_rem in place of W_full")
    m3_bite = not all(m3[f]["max_rel_vs_law"] < 1e-6 for f in FOOTS)
    chk("M3_Wrem_breaks_reduction", m3_bite, f"law dev canonical {m3['canonical']['max_rel_vs_law']:.3f}, alt {m3['alt']['max_rel_vs_law']:.3f}")
    vm, icorr, w2L_m, _ = dispersion(gsign=-1)
    P(f"  M2 dispersion (gamma -> -gamma): omega^2 = {w2L_m}")
    grow = {}
    for foot in FOOTS:
        a0v = 1.0
        for uf in (0.0909, 0.5, 0.9):
            ks, ths, W2 = w2_numeric(w2L_m, a0v, uf * a0v, -1)
            im = np.sqrt(np.clip(-W2, 0, None)).max(axis=0)           # max over angle at each k
            sel = ks > 100
            slope = float(np.polyfit(np.log(ks[sel]), np.log(im[sel]), 1)[0])
            grow[f"{foot}|u0={uf}"] = dict(min_w2=float(W2.min()), slope_ImOmega_vs_k=slope, Im_at_k1e5=float(im[-1]))
    m2_bite = all(v["min_w2"] < 0 and abs(v["slope_ImOmega_vs_k"] - 1) < 0.01 for v in grow.values())
    for kx, v in grow.items():
        P(f"     {kx:22s} min omega^2/(K rho0) = {v['min_w2']:.3e}; d ln Im(omega)/d ln k = {v['slope_ImOmega_vs_k']:.4f}; "
          f"Im omega(kL*=1e5) = {v['Im_at_k1e5']:.3e} sqrt(K rho0)")
    chk("M2_negative_stiffness_gradient_instability", m2_bite, "omega^2 < 0 at large k with |Im omega| proportional to k (slope 1)")
    RES["MUTATE"] = dict(M1=m1, M3=m3, M2=grow)
    allbite = m1_bite and m2_bite and m3_bite
    P(f"\n  MUTATE: {'ALL TEETH BITE (exit 1 by design)' if allbite else 'A TOOTH FAILED TO BITE'}")
    dump(); sys.exit(1 if allbite else 2)

# ================================================================================================ S1 BACKGROUND
P("\n==================== S1 BACKGROUND (Q1) ====================")
taus = sp.symbols("tau1 tau2 tau3", positive=True)
Fs = sp.Function("Fs")


def solid_L(GIm):
    B = B_of(GIm)
    return Fs((B).trace(), (B * B).trace(), (B * B * B).trace())


Tsol = stress_from(solid_L)
Tmix_s = at_metric(Tsol, FRW)
off_s = all(sp.simplify(Tmix_s[i, j]) == 0 for i in range(4) for j in range(4) if i != j)
iso_s = sp.simplify(Tmix_s[1, 1] - Tmix_s[2, 2]) == 0 and sp.simplify(Tmix_s[1, 1] - Tmix_s[3, 3]) == 0
a1, a2, a3 = [sp.Function(nm, positive=True)(t_) for nm in ("a1", "a2", "a3")]
BI = [-1, a1 ** -2, a2 ** -2, a3 ** -2]
Tfl_BI = at_metric(Tfl, BI); Tsol_BI = at_metric(Tsol, BI)
fl_BI_iso = sp.simplify(Tfl_BI[1, 1] - Tfl_BI[2, 2]) == 0
sol_BI_aniso = sp.simplify(Tsol_BI[1, 1] - Tsol_BI[2, 2])
sol_BI_iso_when_equal = sp.simplify(sol_BI_aniso.subs({a2: a1}).doit()) == 0
chk("S1a_FRW_homogeneous_isotropic_fluid_and_solid", off_s and iso_s and all(o == 0 for o in off) and iso,
    "T^mu_nu diagonal with T^1_1 = T^2_2 = T^3_3 for F(n) and for generic solid F(tr B, tr B^2, tr B^3)")
chk("S1a2_Bianchi_I_contrast", fl_BI_iso and (sol_BI_aniso != 0) and sol_BI_iso_when_equal,
    "anisotropic expansion: fluid stress stays isotropic (always); solid stress anisotropic only if a1 != a2")
# rest frame: J^mu = eps^{mu a b c} eps_IJK d phi d phi d phi /(6 sqrt(-g)) at phi = x on FRW
import itertools
LC4 = sp.LeviCivita
def J_frw():
    dphi = lambda I, al: 1 if al == I + 1 else 0
    sqrtg = af ** 3
    J = []
    for mu in range(4):
        tot = 0
        for al, be, ga in itertools.product(range(4), repeat=3):
            e4 = LC4(mu, al, be, ga)
            if e4 == 0: continue
            for I, Jx, Kx in itertools.permutations(range(3)):
                tot += e4 * LC4(I, Jx, Kx) * dphi(I, al) * dphi(Jx, be) * dphi(Kx, ga)
        J.append(sp.simplify(tot / 6 / sqrtg))
    return J
Jf = J_frw()
uvec = [sp.simplify(j / n_frw) for j in Jf]
chk("S1b_rest_frame_is_cosmic_frame", uvec == [1, 0, 0, 0], f"u^mu = {uvec} (comoving); g_mu nu u^mu u^nu = -1")
chk("S1c_w0", k2, "F = -m c^2 n -> w = 0 (K2)")
# chi sector on FRW: chi = chibar(t); h = g + u u; D_i D_j chi; traceless tidal tensor; constraint
chib = sp.Function("chibar")(t_)
gfrw = sp.diag(-1, af ** 2, af ** 2, af ** 2); gfrw_inv = gfrw.inv()
def christoffel(gm, gim):
    Gam = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a_ in range(4):
        for b_ in range(4):
            for c_ in range(4):
                Gam[a_][b_][c_] = sp.simplify(sum(gim[a_, d_] * (sp.diff(gm[d_, b_], XX[c_]) + sp.diff(gm[d_, c_], XX[b_])
                                                                - sp.diff(gm[b_, c_], XX[d_])) for d_ in range(4)) / 2)
    return Gam
Gm = christoffel(gfrw, gfrw_inv)
uup = sp.Matrix([1, 0, 0, 0]); udn = gfrw * uup
hup = gfrw_inv + uup * uup.T; hmix = sp.eye(4) + uup * udn.T          # h^mu_nu = delta + u^mu u_nu
hdn = gfrw + udn * udn.T
dch = [sp.diff(chib, X_) for X_ in XX]
nabla2 = sp.Matrix(4, 4, lambda a_, b_: sp.diff(chib, XX[a_], XX[b_]) - sum(Gm[c_][a_][b_] * dch[c_] for c_ in range(4)))
DD = sp.simplify(hmix.T * nabla2 * hmix)                               # D_a D_b chi = h_a^c h_b^d nabla_c nabla_d chi
D2 = sp.simplify(sum(hup[a_, b_] * DD[a_, b_] for a_ in range(4) for b_ in range(4)))
tau_tl = sp.simplify(DD - hdn * D2 / 3)
u2chi = sp.simplify(sum(hup[a_, b_] * dch[a_] * dch[b_] for a_ in range(4) for b_ in range(4)))
Hh = sp.diff(af, t_) / af
chk("S1d_tether_sector_vanishes_on_FRW", u2chi == 0 and tau_tl == sp.zeros(4, 4) and is0(D2 + 3 * Hh * sp.diff(chib, t_)),
    f"h^{{mu nu}} d chi d chi = {u2chi}; traceless tidal tensor = 0; D^2 chibar = {D2} -> chibar' = -K rho/(3H) (homogeneous solution exists); P = 0")
RES["S1"] = dict(solid_BI_anisotropy=str(sol_BI_aniso)[:300])
rss_guard("S1")

# ================================================================================================ S2 MATCHING
P("\n==================== S2 MATCHING TO S2 (Q2) ====================")
phis = [sp.Function(f"phi{I}")(*XX) for I in range(3)]
def Jcur(ph, mu):
    tot = 0
    for al, be, ga in itertools.product(range(4), repeat=3):
        e4 = LC4(mu, al, be, ga)
        if e4 == 0: continue
        for I, Jx, Kx in itertools.permutations(range(3)):
            tot += e4 * LC4(I, Jx, Kx) * sp.diff(ph[I], XX[al]) * sp.diff(ph[Jx], XX[be]) * sp.diff(ph[Kx], XX[ga])
    return tot / 6
def Qform(ph, mu, nu):
    tot = 0
    for be, ga in itertools.product(range(4), repeat=2):
        e4 = LC4(mu, nu, be, ga)
        if e4 == 0: continue
        for I, Jx, Kx in itertools.permutations(range(3)):
            tot += e4 * LC4(I, Jx, Kx) * ph[I] * sp.diff(ph[Jx], XX[be]) * sp.diff(ph[Kx], XX[ga])
    return tot / 6
Qm = [[Qform(phis, mu, nu) for nu in range(4)] for mu in range(4)]
twoform_ok = all(sp.expand(Jcur(phis, mu) - sum(sp.diff(Qm[mu][nu], XX[nu]) for nu in range(4))) == 0 for mu in range(4))
J0_det = sp.expand(Jcur(phis, 0) - sp.Matrix(3, 3, lambda I, i: sp.diff(phis[I], XX[i + 1])).det()) == 0
Pvec = [Qm[0][i + 1] - XX[i + 1] / 3 for i in range(3)]                # P^i (units m nbar = 1)
divP = sum(sp.diff(Pvec[i], XX[i + 1]) for i in range(3))
divP_ok = sp.expand(divP - (Jcur(phis, 0) - 1)) == 0
jcur = [Jcur(phis, i + 1) for i in range(3)]
cont_ok = sp.expand(sum(sp.diff(sp.diff(Pvec[i], t_) + jcur[i], XX[i + 1]) for i in range(3))) == 0
chk("S2a_P_is_electric_part_of_current_2form", twoform_ok and J0_det and divP_ok and cont_ok,
    "J^mu = d_nu Q^{mu nu}, Q = (1/6) eps eps phi dphi dphi; J^0 = det(d_i phi^I); P^i = m(Q^{0i} - nbar x^i/3): "
    "div P = rho - rhobar EXACT (nonlinear), d_t P + j divergence-free (d_t P_L = -j_L exact)")
rss_guard("S2a")
# linear order: phi = x - e xi(x) -> P = -rhobar xi + (divergence-free)
ee = sp.Symbol("e")
xis = [sp.Function(f"xi{i}")(x_, y_, z_) for i in range(3)]
phlin = [XX[i + 1] - ee * xis[i] for i in range(3)]
Plin = [sp.series(Qform(phlin, 0, i + 1) - XX[i + 1] / 3, ee, 0, 2).removeO().coeff(ee, 1) for i in range(3)]
lin_ok = sp.expand(sum(sp.diff(Plin[i] + xis[i], XX[i + 1]) for i in range(3))) == 0
chk("S2a2_linear_P_minus_rhobar_xi", lin_ok, "P = -rhobar xi + (divergence-free) at linear order, xi = x - phi (sign: div P = +delta rho)")
# tether = minimal coupling; S2 square expansion
drho, PhiF = sp.Function("drho")(x_, y_, z_), sp.Function("Phi")(x_, y_, z_)
Pf = [sp.Function(f"P{i}")(x_, y_, z_) for i in range(3)]
divPf = sum(sp.diff(Pf[i], XX[i + 1]) for i in range(3))
tether_id = sp.expand(-divPf * PhiF - (sum(Pf[i] * sp.diff(PhiF, XX[i + 1]) for i in range(3))
                                         - sum(sp.diff(Pf[i] * PhiF, XX[i + 1]) for i in range(3)))) == 0
Kk = 4 * sp.pi * G
gradPhi = [sp.Symbol(f"dPhi{i}", real=True) for i in range(3)]; Pc = [sp.Symbol(f"Pc{i}", real=True) for i in range(3)]
uK = Kk * sp.sqrt(sum(p ** 2 for p in Pc))
sq = -sum((gradPhi[i] - Kk * Pc[i]) ** 2 for i in range(3)) / (2 * Kk) - Wrem.subs(u, uK)
ex = -sum(gp ** 2 for gp in gradPhi) / (2 * Kk) + sum(Pc[i] * gradPhi[i] for i in range(3)) - Wfull.subs(u, uK)
square_ok = is0(sq - ex)
chk("S2b_tether_is_minimal_gravitational_coupling", tether_id and square_ok and k3,
    "-delta rho_c Phi = P.grad Phi - div(P Phi) with div P = delta rho_c; -|grad Phi - KP|^2/2K - W_rem = "
    "-|grad Phi|^2/2K + P.grad Phi - W_full; the medium's rest-mass coupling gives -rho Phi (K3): FORCED")
chk("S2b2_W_identities", is0(Dfull - u / (1 - u / a0s)) and is0(Rrem - u ** 2 / (a0s - u)) and is0(Dfull - u - Rrem),
    "K W_full' = u/(1 - u/a0), K W_rem' = u^2/(a0 - u), D_full = u + R")
# W is not a strain function and not a local function of d phi
lam_ = sp.Symbol("lambda", positive=True)
phc = [XX[i + 1] / lam_ for i in range(3)]
Pc_ = [sp.simplify(Qform(phc, 0, i + 1) - XX[i + 1] / 3) for i in range(3)]
Bc = sp.simplify(sp.Matrix(3, 3, lambda I, J: sum(sp.diff(phc[I], XX[i + 1]) * sp.diff(phc[J], XX[i + 1]) for i in range(3))))
P2c = sp.simplify(sum(p ** 2 for p in Pc_))
strain_ok = Bc == sp.eye(3) / lam_ ** 2 and sp.simplify(sp.diff(P2c, x_)) != 0
rho_a, R_, Dl = sp.symbols("rho_a R Delta", positive=True)
u_prof1 = G * (4 * sp.pi / 3) * rho_a * R_ ** 3 / R_ ** 2
u_prof2 = G * ((4 * sp.pi / 3) * rho_a * R_ ** 3 + (4 * sp.pi / 3) * Dl * (R_ / 2) ** 3) / R_ ** 2
nonlocal_ok = sp.simplify(u_prof2 - u_prof1) != 0
chk("S2c_W_not_a_strain_or_local_function", strain_ok and nonlocal_ok,
    f"uniform compression phi = x/lambda: B = delta/lambda^2 everywhere but |P|^2 = {P2c} grows with position; "
    f"two profiles identical near R with different interiors: u differs by {sp.simplify(u_prof2 - u_prof1)} -> u is an "
    "enclosed-mass (nonlocal) quantity; a local covariant W(K|P|) needs an extra structure")
# chi: medium-frame potential; Gauss
Mf = sp.Function("M")(r)
chip = G * Mf / r ** 2
gauss_ok = is0(sp.diff(r ** 2 * chip, r) / r ** 2 - 4 * sp.pi * G * sp.diff(Mf, r) / (4 * sp.pi * r ** 2))
chk("S2c2_chi_constraint_gives_u", gauss_ok, "D^2 chi = K rho_c (medium frame) -> chi' = G M_c(<r)/r^2 = u = K|P_L| (Gauss)")
# stiffness identities
chf = sp.Function("chi")(r)
tot_ok = is0(r ** 2 * ((sp.diff(chf, r, 2) ** 2 + 2 * sp.diff(chf, r) ** 2 / r ** 2) - (sp.diff(chf, r, 2) + 2 * sp.diff(chf, r) / r) ** 2)
             + sp.diff(2 * r * sp.diff(chf, r) ** 2, r))
ch3 = sp.Function("chi3")(x_, y_, z_)
hess3 = sp.Matrix(3, 3, lambda i, j: sp.diff(ch3, XX[i + 1], XX[j + 1])); lap3 = hess3.trace()
gen_ok = sp.expand(sum(hess3[i, j] ** 2 for i in range(3) for j in range(3)) - lap3 ** 2
                   - sum(sp.diff(sp.diff(ch3, XX[j + 1]) * hess3[i, j], XX[i + 1]) for i in range(3) for j in range(3))
                   + sum(sp.diff(sp.diff(ch3, XX[j + 1]) * lap3, XX[j + 1]) for j in range(3))) == 0
chk("S2d_stiffness_is_density_squared", tot_ok and gen_ok,
    "|d_i d_j chi|^2 = (lap chi)^2 + divergence (3-D, exact); with K P_L = grad chi: (gamma/2)|grad P_L|^2 = (gamma/2) delta rho_c^2 "
    "+ divergence; traceless form (3 gamma/4K^2) tau^2 gives the same (2/3 factor absorbed)")
eqs, Mc_, Mb_ = reduced_EL(1, Wfull, True)
expected = (-G * (Mb_ + Mc_) / r ** 2 + Dfull.subs(u, G * Mc_ / r ** 2)
            - gam * sp.diff(sp.diff(Mc_, r) / (4 * sp.pi * r ** 2), r))
stiffEL_ok = is0(eqs - expected)
chk("S2d2_static_equation_with_stiffness", stiffEL_ok,
    "EL: D_full(u) = g + gamma d rho_c/dr, i.e. R(u) = g_N + gamma rho_c' (stiffness = pressure p = (gamma/2) rho_c^2 = pi G L*^2 rho_c^2; "
    "rho_c' < 0 pushes u below the law: screening)")
# early universe: local EoS version
H0 = 67.4e3 / (1e6 * PC); rho_crit = 3 * H0 ** 2 / (8 * math.pi * G_SI)
Ob = 0.0493; Oc = 5.364 * Ob; rho_c0 = Oc * rho_crit
a_rad = 7.5657e-16; T_cmb = 2.7255; Neff = 3.046
rho_r0 = a_rad * T_cmb ** 4 / C_SI ** 2 * (1 + 7 / 8 * (4 / 11) ** (4 / 3) * Neff)
bbn = {}
for Lpc in (24.0, 1000.0):
    Ls = Lpc * PC
    coef = math.pi * G_SI * Ls ** 2 * rho_c0 ** 2 / (rho_r0 * C_SI ** 2)      # eps_stiff/eps_rad = coef (1+z)^2
    w_rec = math.pi * G_SI * Ls ** 2 * rho_c0 * 1101 ** 3 / C_SI ** 2
    z10 = math.sqrt(0.1 / coef) - 1
    bbn[f"{Lpc:g}pc"] = dict(ratio_at_zBBN=coef * (4e8 + 1) ** 2, w_at_recombination=w_rec, z_where_10pct_of_radiation=z10,
                             w_today=math.pi * G_SI * Ls ** 2 * rho_c0 / C_SI ** 2)
for kx, v in bbn.items():
    P(f"  local EoS p = pi G L*^2 rho_c^2, L* = {kx}: eps_stiff/eps_rad(z=4e8) = {v['ratio_at_zBBN']:.2e}; reaches 10% of radiation at "
      f"z = {v['z_where_10pct_of_radiation']:.2e}; w(z=1100) = {v['w_at_recombination']:.2e}; w(0) = {v['w_today']:.2e}")
chk("S2d3_local_stiffness_EoS_early_universe", True,
    "computed (a result, not a pass line): the LOCAL covariant stiffness is a stiff EoS; EXCLUDED at BBN for the whole L* window "
    "if the medium exists then (ratio >> 0.1); the chi-tidal (traceless) form vanishes on FRW (S1d) and has no background")
RES["S2"] = dict(early_universe_local_EoS=bbn)
rss_guard("S2")

# ================================================================================================ S3 CONSERVATION
P("\n==================== S3 CONSERVATION AND SETTLING (Q3) ====================")
# (a) static stress of the tether sector by metric variation (N = 1, spatial metric h^{ij} symbolic)
hs = {}; Hm = sp.zeros(3, 3)
for i in range(3):
    for j in range(i, 3):
        hs[(i, j)] = sp.Symbol(f"h{i}{j}", real=True); Hm[i, j] = Hm[j, i] = hs[(i, j)]
cx = [sp.Symbol(f"c{i}", real=True) for i in range(3)]; lx = [sp.Symbol(f"l{i}", real=True) for i in range(3)]
Wg = sp.Function("W")
uu_h = sp.sqrt(sum(Hm[i, j] * cx[i] * cx[j] for i in range(3) for j in range(3)))
sqh = 1 / sp.sqrt(Hm.det())
Lh = -Wg(uu_h) - sum(Hm[i, j] * lx[i] * cx[j] for i in range(3) for j in range(3))   # lambda D^2 chi integrated by parts
Tvar = sp.zeros(3, 3)
for (i, j), s_ in hs.items():
    Tvar[i, j] = Tvar[j, i] = (-2 if i == j else -1) * sp.diff(sqh * Lh, s_) / sqh
Tvar = Tvar.subs({hs[(i, j)]: (1 if i == j else 0) for (i, j) in hs}).doit()
u_flat = sp.sqrt(sum(c_ ** 2 for c_ in cx))
Wp = sp.Subs(sp.Derivative(Wg(sp.Symbol("s_")), sp.Symbol("s_")), sp.Symbol("s_"), u_flat).doit()
Tform = sp.Matrix(3, 3, lambda i, j: Wp / u_flat * cx[i] * cx[j] - (1 if i == j else 0) * Wg(u_flat)
                  + lx[i] * cx[j] + lx[j] * cx[i] - (1 if i == j else 0) * sum(lx[k_] * cx[k_] for k_ in range(3)))
tvar_ok = all(sp.simplify(sp.expand(Tvar[i, j] - Tform[i, j]).doit()) == 0 for i in range(3) for j in range(3))
chk("S3a_tether_sector_stress_by_metric_variation", tvar_ok,
    "T_ij = (W'/u) d_i chi d_j chi - delta_ij W + 2 d_(i lambda d_j) chi - delta_ij grad lambda.grad chi")
# (b) divergence identity, generic 3-D fields: on the chi shell, d_j T_ij = rho_c d_i(K lambda) = -(force density on the medium)
chi3, lam3 = sp.Function("chi")(x_, y_, z_), sp.Function("lam")(x_, y_, z_)
fs = sp.Function("f")
grad = lambda F_: [sp.diff(F_, XX[i + 1]) for i in range(3)]
gc, gl = grad(chi3), grad(lam3); s2 = sum(q ** 2 for q in gc)
fp = sp.diff(fs(s2), chi3) if False else None
Ss = sp.Symbol("S")
fprime = sp.Subs(sp.Derivative(fs(Ss), Ss), Ss, s2).doit()
T3 = [[2 * fprime * gc[i] * gc[j] - (1 if i == j else 0) * fs(s2) + gl[i] * gc[j] + gl[j] * gc[i]
       - (1 if i == j else 0) * sum(gl[k_] * gc[k_] for k_ in range(3)) for j in range(3)] for i in range(3)]
divT = [sum(sp.diff(T3[i][j], XX[j + 1]) for j in range(3)) for i in range(3)]
chi_eq = sum(sp.diff(2 * fprime * gc[j], XX[j + 1]) for j in range(3)) + sum(sp.diff(gl[j], XX[j + 1]) for j in range(3))
lapchi = sum(sp.diff(gc[j], XX[j + 1]) for j in range(3))
div_ok = all(sp.simplify(sp.expand((divT[i] - gc[i] * chi_eq - gl[i] * lapchi).doit())) == 0 for i in range(3))
chk("S3b_momentum_balance_identity", div_ok,
    "d_j T_ij = d_i chi [div(W' grad chi/|grad chi|) + lap lambda] + d_i lambda lap chi  ->  on shell = rho_c d_i(K lambda) = "
    "-(tether force density on the medium): medium + tether + gravity conserve momentum")
rss_guard("S3b")
# (c) on-shell radial stress = CFG660's field-aligned stress
Kk = 4 * sp.pi * G
gN_law = gs ** 2 / (gs + a0s); u_law = sp.simplify(gs - gN_law)
W_on = Wfull.subs(u, u_law)
p_par = -W_on; p_perp = -W_on + gs * u_law / Kk
c660_1 = is0(sp.diff(p_par, gs) - (gs / Kk) * (sp.diff(gN_law, gs) - 1))
c660_2 = is0(p_perp - p_par - gs * (gs - gN_law) / Kk)
ser660 = sp.series(p_par, gs, 0, 4).removeO()
c660_3 = is0(ser660 - (-gs ** 2 / (8 * sp.pi * G) + gs ** 3 / (6 * sp.pi * G * a0s)))
uf_ = sp.Function("u")(r)
pr_ = -Wfull.subs(u, uf_); pt_ = -Wfull.subs(u, uf_) + Dfull.subs(u, uf_) * uf_ / Kk
rho_ph = (sp.diff(uf_, r) + 2 * uf_ / r) / Kk
bal_ok = is0(sp.diff(pr_, r) + 2 * (pr_ - pt_) / r + rho_ph * Dfull.subs(u, uf_))
chk("S3c_static_stress_equals_CFG660_Pi", c660_1 and c660_2 and c660_3 and bal_ok,
    f"p_r = -W_full(u), p_t = p_r + D(u) u/K; on the law: dP_par/dg = (g/K)(dg_N/dg - 1), P_perp - P_par = g(g - g_N)/K, "
    f"deep P_par = {ser660}; radial balance p_r' + 2(p_r - p_t)/r = -rho_c g. CFG660's stress is the derived stress of this action")
# (d) the record's two-sided drift as the linearised force of this action
dd_ = sp.Symbol("delta")
uL = sp.Symbol("u_L", positive=True)
force = (Dfull - (gN + u)).subs(u, uL + dd_)                             # outward force per mass, gamma = 0
force_lin = sp.series(force.subs(gN, Rrem.subs(u, uL)), dd_, 0, 2).removeO()
drift_ok = is0(force_lin - sp.diff(Rrem, u).subs(u, uL) * dd_)
chk("S3d_drift_is_linearised_tether_force", drift_ok,
    "f = D(u) - g = R(u) - g_N ~ R'(u_L)(u - u_L) = R'(u_L)(g - g_law): same direction as CFG638/CFG544 v_s = alpha tau (g - g_law); "
    "an overdamped limit needs a drag (mobility tau_d: alpha tau = tau_d R'(u_L)), which the ideal action does not contain")
# (e) overdamped gradient flow of this action's energy (code units G = a0 = 1, Hernquist baryons M = 1, a = 0.5)
def shell_flow(N=300, dM=0.02, rs=0.5, r_edge=10.0, nstep=40000, every=500):
    from scipy.integrate import quad
    Kc = 4 * math.pi; ab = 0.5
    Mb = lambda rr: rr * rr / (rr + ab) ** 2
    Wc = lambda uu: (-uu - math.log1p(-uu)) / Kc
    def uLaw(rr):
        gg = law_g(Mb(rr) / rr ** 2, 1.0); return gg / (gg + 1.0)
    Minit = lambda rr: uLaw(rr) * rr * rr + dM * (1 - math.exp(-(rr / rs) ** 3))
    Mt = Minit(r_edge); mk = Mt / N
    rk = np.array([brentq(lambda rr: Minit(rr) - (k_ + 1.0) * mk * (1 - 1e-12), 1e-8, r_edge) for k_ in range(N)])   # M_c just outside shell k = M_init(r_k)
    def energies(rk):
        rs_ = np.sort(rk); Eg = 0.0; Ew = 0.0
        edges = np.concatenate(([0.0], rs_))
        for k_ in range(N + 1):
            lo = edges[k_]; hi = rs_[k_] if k_ < N else np.inf; Mc = k_ * mk
            Eg += -quad(lambda rr: (Mb(rr) + Mc) ** 2 / (2 * rr * rr) if rr > 0 else 0.0, lo, hi, limit=200, epsabs=1e-13, epsrel=1e-12)[0]
            if Mc > 0:
                Ew += quad(lambda rr: 4 * math.pi * rr * rr * Wc(Mc / rr ** 2), lo, hi, limit=200, epsabs=1e-13, epsrel=1e-12)[0]
        return Eg, Ew
    def forces(rk):
        order = np.argsort(rk); rs_ = rk[order]
        Mm = np.arange(N) * mk; Mp = Mm + mk
        gbar = (Mb(rs_) + Mm + mk / 2) / rs_ ** 2
        up, um = Mp / rs_ ** 2, Mm / rs_ ** 2
        if np.any(up >= 1): return None, order
        Wp_ = (-up - np.log1p(-up)) / Kc; Wm_ = (-um - np.log1p(-um)) / Kc
        F = -mk * gbar + 4 * math.pi * rs_ ** 2 * (Wp_ - Wm_)
        out = np.empty(N); out[order] = F
        return out, order
    assert forces(rk)[0] is not None, "initial state hits the wall u >= a0"
    rec = []; E0 = energies(rk); rec.append((0.0,) + E0); tt = 0.0
    for st in range(1, nstep + 1):
        F, order = forces(rk)
        v = F / mk
        # time step limited by the shells' own curvature dF_k/dr_k (run 1 used only the relative-displacement limit: explicit Euler
        # went unstable on the stiff shells near the wall and E rose by up to 7e-8 per record; fixed before any class was recorded)
        rs_ = rk[order]; Mm = np.arange(N) * mk; Mp = Mm + mk; up, um = Mp / rs_ ** 2, Mm / rs_ ** 2
        Wp_ = (-up - np.log1p(-up)) / Kc; Wm_ = (-um - np.log1p(-um)) / Kc
        dWp, dWm = up / (1 - up) / Kc, um / (1 - um) / Kc
        dMb = 2 * rs_ * ab / (rs_ + ab) ** 3
        curv = (-mk * (dMb / rs_ ** 2 - 2 * (Mb(rs_) + Mm + mk / 2) / rs_ ** 3) + 8 * math.pi * rs_ * (Wp_ - Wm_)
                + 4 * math.pi * rs_ ** 2 * (-2 / rs_) * (dWp * up - dWm * um))
        dt = min(1e-3 * np.min(rk / np.maximum(np.abs(v), 1e-300)), 0.5 * np.min(mk / np.maximum(np.abs(curv), 1e-300)))
        trial = rk + v * dt
        while forces(trial)[0] is None:
            dt *= 0.5; trial = rk + v * dt
        rk = trial; tt += dt
        if st % every == 0:
            rec.append((tt,) + energies(rk)); rss_guard("shell_flow")
    rec = np.array(rec)
    return rec, dict(N=N, dM=dM, rs=rs, r_edge=r_edge, nstep=nstep)
rec, cfgflow = shell_flow()
Etot = rec[:, 1] + rec[:, 2]
mono = bool(np.all(np.diff(Etot) <= 1e-12 * np.abs(Etot).max()))
dEg, dEw = rec[-1, 1] - rec[0, 1], rec[-1, 2] - rec[0, 2]
P(f"  overdamped flow ({cfgflow}): records {len(rec)}; E_total monotone non-increasing: {mono}")
P(f"     Delta E_grav = {dEg:+.4e} (CFG932's 'drift work', >0 = energy against gravity)   Delta E_W = {dEw:+.4e}   "
  f"heat = -(sum) = {-(dEg + dEw):+.4e}   [code units G = a0 = M_b = 1]")
chk("S3e_settling_energy_books_close_with_tether_energy", mono and dEg > 0 and dEw < -dEg,
    "pushing a central surplus out raises the gravitational energy (CFG932's injection) but releases more tether energy W; "
    "total potential energy falls, the difference is dissipated (heat). BY CONSTRUCTION for a gradient flow; the content is that "
    "CFG932's books omit E_W")
RES["S3"] = dict(flow=dict(cfg=cfgflow, dE_grav=dEg, dE_W=dEw, heat=-(dEg + dEw), monotone=mono))
rss_guard("S3")

# ================================================================================================ S4 SLIP
P("\n==================== S4 LENSING AND SLIP (Q4) ====================")
SYS = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0), ("cluster", 1.5e14, 1000.0)]
MSUN847, KPC847 = 1.989e30, 3.0857e19                                  # CFG847's own constants for its systems
slip = {}; worst_grad = 0.0; worst_847 = 0.0
for foot in FOOTS:
    a0 = A0[foot]
    P(f"  [{foot}] {'system':9s} {'v_c km/s':>8s} {'s_grad(W)':>10s} {'s_847(W)':>10s} {'s_grad(+stiff 1kpc)':>20s} {'s_847(+stiff 1kpc)':>19s}"
      f" {'1/eps_inertia':>14s}")
    for name, Mb, rk_ in SYS:
        M = Mb * MSUN847; rr = rk_ * KPC847
        def uat(x):
            g_ = law_g(G_SI * M / x ** 2, a0); return g_ * a0 / (g_ + a0)
        g_ = law_g(G_SI * M / rr ** 2, a0); uu_ = uat(rr); W_ = Wfull_num(uu_, a0)
        h_ = 1e-5 * rr
        rho_c = ((rr + h_) ** 2 * uat(rr + h_) - (rr - h_) ** 2 * uat(rr - h_)) / (2 * h_) / (K_SI * rr ** 2)
        vc2 = g_ * rr
        row = {}
        for lab, Lpc in (("W", 0.0), ("stiff24", 24.0), ("stiff1k", 1000.0)):
            ps = math.pi * G_SI * (Lpc * PC) ** 2 * rho_c ** 2
            pr = -W_ + ps; pt = -W_ + g_ * uu_ / K_SI + ps
            row[lab] = dict(s_grad=4 * math.pi * G_SI * rr * abs(pr) / (C_SI ** 2 * g_),
                            s_847=8 * math.pi * G_SI * rr ** 2 * max(abs(pr), abs(pt)) / (C_SI ** 2 * vc2))
        inert = K_SI * rho_c * C_SI ** 2 / (g_ * uu_)                    # 1/eps: rho_c c^2 / (D u / K), D = g on the law
        row.update(vc_kms=math.sqrt(vc2) / 1e3, rho_c=rho_c, inv_eps_inertia=inert)
        slip[f"{foot}|{name}"] = row
        worst_grad = max(worst_grad, max(row[l]["s_grad"] for l in ("W", "stiff24", "stiff1k")))
        worst_847 = max(worst_847, max(row[l]["s_847"] for l in ("W", "stiff24", "stiff1k")))
        P(f"           {name:9s} {row['vc_kms']:8.1f} {row['W']['s_grad']:10.2e} {row['W']['s_847']:10.2e} {row['stiff1k']['s_grad']:20.2e}"
          f" {row['stiff1k']['s_847']:19.2e} {inert:14.2e}")
P(f"  worst s_grad = {worst_grad:.2e}; worst s_847 = {worst_847:.2e}  (CFG847 largest 1.9e-5; class line 1e-2). Lensing/dynamics "
  "mass mismatch = s_grad/2. The medium is cold here (no dispersion term).")
chk("S4_slip_within_CFG847_bound", worst_grad <= 1.9e-5 and worst_847 <= 1.9e-5,
    f"anisotropic stress is present (p_r - p_t = -g u/K, the field-aligned stress) but s <= {max(worst_grad, worst_847):.1e}")
RES["S4"] = dict(rows=slip, worst_grad=worst_grad, worst_847=worst_847)
rss_guard("S4")

# ================================================================================================ S5 WELL-POSEDNESS
P("\n==================== S5 WELL-POSEDNESS (Q5) ====================")
vmode, icorr, w2L, sols = dispersion(gsign=1)
P(f"  potential per mode v(k) = {sp.factor(vmode)}")
P(f"  inertia: rho0 delta_ij - {icorr} z_i z_j   (= D(u0) u0/(K c^2) along grad chi)")
P(f"  omega^2 (longitudinal) = {w2L};  other two roots: {[s_ for s_ in sols if sp.simplify(s_) == 0]}")
w2_cinf = sp.simplify(sp.limit(w2L, cl, sp.oo))
target_w2 = rho0 * (4 * sp.pi * G * (sp.diff(Rrem, u).subs(u, u0) * sp.cos(th) ** 2 + (Rrem / u).subs(u, u0) * sp.sin(th) ** 2) + gam * kk ** 2)
disp_ok = is0(w2_cinf - target_w2)
Rp_fact = sp.factor(sp.diff(Rrem, u)); Ru_fact = sp.factor(Rrem / u)
P(f"  c -> infinity: omega^2 = rho0 [K (R'(u0) cos^2 + (R(u0)/u0) sin^2) + gamma k^2];  R' = {Rp_fact},  R/u = {Ru_fact}")
chk("S5a_dispersion_relation", disp_ok, "omega^2 = c_s^2 k^2 + K rho0 [R'(u0) cos^2 theta + (R(u0)/u0) sin^2 theta], c_s^2 = gamma rho0; "
    "self-gravity (-K rho0) cancelled and over-cancelled by the tether; transverse (vortical) roots omega^2 = 0")
wp = {}
for uf in (0.0909, 0.5, 0.9, 0.99):
    ks, ths, W2 = w2_numeric(w2L, 1.0, uf, 1)
    wp[f"u0/a0={uf}"] = dict(min_w2=float(W2.min()), max_Im=float(np.sqrt(np.clip(-W2, 0, None)).max()))
    P(f"     u0/a0 = {uf:6.4f}: min omega^2/(K rho0) over kL* in [1e-2, 1e5], theta in [0, pi/2] = {W2.min():.4e}; max Im omega = "
      f"{wp[f'u0/a0={uf}']['max_Im']:.1e}")
chk("S5b_no_gradient_instability_bounded_growth", all(v["min_w2"] >= 0 and v["max_Im"] == 0 for v in wp.values()),
    "omega^2 >= 0 for every k and angle (gamma > 0, 0 <= u0 < a0): no growth at all, versus CFG660's growth proportional to sqrt(k)")
inert_ok = all(v["inv_eps_inertia"] > 1 for v in slip.values())
P(f"  inertia condition rho_c c^2 > D(u) u / K on CFG847's systems: min margin 1/eps = {min(v['inv_eps_inertia'] for v in slip.values()):.2e}")
chk("S5c_positive_inertia_condition", inert_ok,
    "kinetic matrix positive iff rho_c c^2 > D(u) u/K (the tether stress); margin ~ c^2/v^2 on the law; screened regions "
    "(u ~ K rho_c r/3) need only r < 3c/sqrt(K rho_c). CONDITION, not automatic")
# non-propagation of chi, lambda in the medium rest frame (flat): no time derivatives
cht = sp.Function("chit")(*XX)
hflat = sp.diag(0, 1, 1, 1)
u2t = sum(hflat[a_, b_] * sp.diff(cht, XX[a_]) * sp.diff(cht, XX[b_]) for a_ in range(4) for b_ in range(4))
D2t = sum(hflat[a_, b_] * sp.diff(cht, XX[a_], XX[b_]) for a_ in range(4) for b_ in range(4))
noprop = not u2t.has(sp.Derivative(cht, t_)) and not D2t.has(sp.Derivative(cht, t_, 2))
chk("S5d_chi_lambda_non_propagating", noprop,
    "in the medium rest frame the chi/lambda sector has no time derivatives: constraints (elliptic, instantaneous in that frame); "
    "propagating dof = medium (1 longitudinal at c_s, 2 vortical at 0) + graviton (2)")
RES["S5"] = dict(w2=str(w2L), grid=wp)
rss_guard("S5")

# ================================================================================================ S6 LINEAR GROWTH (D2 flag)
P("\n==================== S6 LINEAR GROWTH FLAG (D2) ====================")
al = sp.Symbol("alpha"); mu_ = sp.Symbol("mu")
fb = 1 / (1 + sp.Rational(5364, 1000)); fc = sp.Rational(5364, 1000) / (1 + sp.Rational(5364, 1000))
def growth(Mx):
    ev = max(sp.N(e) for e in Mx.eigenvals())
    a_ = max(sp.solve(al ** 2 + al / 3 - sp.Rational(2, 3) * ev, al), key=lambda e: sp.N(e))
    return float(ev), float(sp.N(a_)), float(sp.N(3 * a_ / 2))
ev_id, at_id, aa_id = growth(sp.Matrix([[fb, fc], [fb, 0]]))
ev_A, at_A, aa_A = growth(sp.Matrix([[fb, fc], [fb, fc]]))
P(f"  matter era, Omega_c/Omega_b = 5.364, baryons free (post recombination):")
P(f"     this parent (tethered medium feels baryon gravity only, CFG888): mu = {ev_id:.4f}, delta ~ t^{at_id:.4f} ~ a^{aa_id:.4f}")
P(f"     record's class-A engine (Newtonian cold gravity, used by CFG650/T2x): mu = {ev_A:.4f}, delta ~ a^{aa_A:.4f}")
chk("S6_growth_flag_computed", abs(aa_A - 1) < 1e-9 and aa_id < 1,
    "a result, not a pass line: the covariant parent of S2 + ID suppresses linear growth of the tethered medium; the record's growth "
    "pass (T2x, class A) does NOT transfer to this parent. Before recombination the medium would follow photon-locked baryons only")
RES["S6"] = dict(mu_parent=ev_id, exp_a_parent=aa_id, mu_classA=ev_A, exp_a_classA=aa_A)

# ================================================================================================ S8 TETHERED-TETHERED GRAVITY
P("\n==================== S8 TETHERED-TETHERED GRAVITY (structural consequence, found while scoring C1) ====================")
kx_, xx_, Bb, C1s, C2s = sp.symbols("k x B C_1 C_2", positive=True)
Kk = 4 * sp.pi * G
# 1-D longitudinal modes: rho_b = B cos kx; two tethered components (e.g. satellite and host) C_1 cos kx, C_2 cos kx
Ctot = C1s + C2s
PhiM = -Kk * (Bb + Ctot) * sp.cos(kx_ * xx_) / kx_ ** 2               # Poisson with all mass
Pm = Ctot * sp.sin(kx_ * xx_) / kx_                                    # div P = delta rho_c (both components)
Lid = -(sp.diff(PhiM, xx_) - Kk * Pm) ** 2 / (2 * Kk) - Bb * sp.cos(kx_ * xx_) * PhiM
Lnw = -sp.diff(PhiM, xx_) ** 2 / (2 * Kk) - (Bb + Ctot) * sp.cos(kx_ * xx_) * PhiM
avg = lambda e: sp.simplify(sp.integrate(e, (xx_, 0, 2 * sp.pi / kx_)) * kx_ / (2 * sp.pi))
Lid_a, Lnw_a = avg(Lid), avg(Lnw)
cross_id = sp.simplify(sp.diff(Lid_a, C1s, C2s)); cross_nw = sp.simplify(sp.diff(Lnw_a, C1s, C2s))
cross_b = sp.simplify(sp.diff(Lid_a, Bb, C1s))
P(f"  <L>_ID = {sp.factor(Lid_a)}   (Newtonian: {sp.factor(Lnw_a)})")
chk("S8a_no_gravity_between_tethered_components", cross_id == 0 and cross_nw != 0 and cross_b != 0,
    f"d2<L>/dC1 dC2 = {cross_id} (Newtonian {cross_nw}); baryon-medium term kept ({cross_b}). Astra's C^2 cancellation (audit sec. 4) "
    "extends to cross terms: tethered medium feels baryons (+ residual R) but NOT the gravity of any tethered medium; baryons and "
    "light feel all of it")
gext = {}
for foot in FOOTS:
    a0 = A0[foot]
    for rkpc in (50.0, 100.0, 250.0):
        rr = rkpc * KPC847; gN_ = G_SI * 6e10 * MSUN847 / rr ** 2; g_ = law_g(gN_, a0); uc = g_ - gN_
        gext[f"{foot}|{rkpc:g}kpc"] = dict(g_total=g_, g_host_medium=uc, ratio_to_a0=uc / a0, residual_R=uc ** 2 / (a0 - uc))
        P(f"  [{foot}] MW-like host (6e10 Msun) at {rkpc:5.0f} kpc: host-medium field {uc:.2e} m/s^2 = {uc / a0:.3f} a0 acts on a satellite's "
          f"stars, not on its tethered medium; residual R(u_host) = {uc ** 2 / (a0 - uc):.2e}")
chk("S8b_differential_free_fall_flag", True,
    "a result, not a pass line: CL-AR's premise (universal coupling) holds for fields of baryons but not for fields of tethered medium; "
    "a satellite's stars and its tethered medium fall differently by ~ the host-medium field (0.03-0.17 a0 for a 6e10 Msun host at 50-250 kpc, both footings). "
    "Not scored against a CFG678 gate; tension with CFG925 R3 (no satellite EFE) is UNTESTED and needs its own lane")
RES["S8"] = dict(L_ID=str(Lid_a), L_Newton=str(Lnw_a), host_medium_field=gext)
rss_guard("S8")

# ================================================================================================ S7 SCORECARD AND CLASS
P("\n==================== S7 CFG678 SCORECARD (Q6) ====================")
SC = [
 ("A1", "no ghost; 2nd-order eqs", "CONDITIONAL", "positive inertia iff rho_c c^2 > D(u)u/K (S5c; margin ~c^2/v^2); medium eqs 2nd order; "
  "chi/lambda auxiliary; chi-tidal stiffness makes the chi constraint 4th order in space (no higher time derivatives)"),
 ("A2", "strongly hyperbolic", "CONDITIONAL", "Euler + c_s^2 = gamma rho > 0 symmetric hyperbolic; tether/gravity are order-0 (elliptic) terms; "
  "omega^2 >= 0 (S5b). Needs gamma > 0 and the A1 inequality; CFG292's khronon line does not apply"),
 ("A3", "nonlinear local WP", "UNTESTED", "not proved; single-stream EFT ends at shell crossing (CFG939's domain)"),
 ("A4", "strong coupling", "UNTESTED", "not computed (classical lane); dust-like c_s << c lowers the phonon EFT cutoff"),
 ("A5", "GW at c", "PASS", "Einstein-Hilbert unmodified; medium and chi sector couple through g and u^mu only, no curvature couplings: c_T = c (structural)"),
 ("A6", "BH exteriors", "UNTESTED", "no BH computation"),
 ("A7", "radiative stability", "DECLARED", "CFG320"),
 ("B1", "switch from variation", "UNTESTED", "no switch term; law acts on every tethered element; S4 untethering not derived"),
 ("B2", "a0-Lambda tie", "UNTESTED", "a0 is a constant inside W; kappa = 1/2 FITTED"),
 ("B3", "well-posed cold sector, lenses like mass", "CONDITIONAL", "linear well-posed (S5) under gamma > 0 + inertia inequality; T_00 = rho_c c^2 "
  "(lenses like mass, slip <= 1.9e-5, S4); one metric; static stress = CFG660 Pi (S3c) now derived from an action. Conditions: extra "
  "non-propagating chi/lambda; spherical/longitudinal matching only; single stream"),
 ("C1", "Cassini", "CONDITIONAL", "static spherical sector = S2 (inherits CFG770); the quadrupole (non-spherical) sector is not identical "
  "to S2 (fluid has no transverse P). Uniform fields of BARYONS free-fall out (CL-AR holds); fields of TETHERED MEDIUM do not act on "
  "tethered medium (S8a): differential free fall, a flag beyond CFG678's gates"),
 ("C2", "SPARC RAR", "PASS", "the static spherical limit IS the law (K1: 2.2e-16 on NGC 3198); CFG4 rms 0.1003/0.0991 <= 0.110"),
 ("C3", "early types 50-100 kpc", "FAIL", "inherits the law's CFG529 failure (same static predictions)"),
 ("C4", "cluster lensing 8-40'", "NOT DECIDED", "CFG680 amplitude not frozen for the law (as CFG678)"),
 ("D1", "zero-field nonlinear dependence", "UNTESTED", "not run; tether sector vanishes identically on FRW (S1d)"),
 ("D2", "growth vs raw KiDS/DES", "UNTESTED", f"frozen CFG596 line not run; FLAG: tethered medium has no linear self-gravity, delta ~ a^{aa_id:.2f} "
  "vs the class-A engine a^1 (S6); T2x pass used class A and does not transfer"),
 ("D3", "flat a0(z)", "PENDING", "constant a0 in W gives flat a0; sealed tests 2026-11-06 / 2026-11-28"),
 ("E1", "kappa from the action", "DECLARED", "kappa = 1/2 FITTED"),
 ("E2", "quantum completion", "DECLARED", "-"),
 ("E3", "SM structure", "DECLARED", "-"),
]
for gid, gname, st, src in SC:
    P(f"  {gid:3s} {gname:38s} {st:12s} {src}")
RES["scorecard"] = [dict(gate=g_, name=n_, status=s_, source=c_) for g_, n_, s_, c_ in SC]
P1 = RES["checks"]["K1_SPARC_NGC3198_reduction"]["pass"]
P2 = RES["checks"]["S3b_momentum_balance_identity"]["pass"] and RES["checks"]["S3a_tether_sector_stress_by_metric_variation"]["pass"]
P3 = RES["checks"]["S5b_no_gradient_instability_bounded_growth"]["pass"] and RES["checks"]["S5c_positive_inertia_condition"]["pass"]
P4 = RES["checks"]["S1a_FRW_homogeneous_isotropic_fluid_and_solid"]["pass"] and RES["checks"]["S1d_tether_sector_vanishes_on_FRW"]["pass"] and k2
P5 = RES["checks"]["S4_slip_within_CFG847_bound"]["pass"]
conditions = [
 "extra non-propagating fields chi (the medium's own potential, medium-frame constraint D^2 chi = K rho_c) and lambda (multiplier); "
 "u = K|P| is |D chi|, not a strain function (S2c)",
 "gamma > 0 (stiffness sign; M2) and the inertia inequality rho_c c^2 > D(u) u/K (S5c)",
 "stiffness built on chi's traceless tidal tensor (background-free); the local EoS form p = pi G L*^2 rho^2 is excluded at BBN if the medium exists then (S2d3)",
 "S2 reproduced in the longitudinal (curl-free P) sector: exact in spherical symmetry; non-spherical sectors differ from S2 with an independent P",
 "single-stream continuum: valid until shell crossing; the medium-frame constraint needs the medium present everywhere (rho_c > 0)",
]
flags = [
 "D2: the tethered medium has no linear self-gravity (S6): delta ~ a^0.61 vs a^1 for the class-A engine; T2x's pass does not transfer",
 "S8: no gravity between tethered components (any source); a satellite's stars and tethered medium fall differently in a host-medium "
 "field (0.03-0.17 a0 at 50-250 kpc for a 6e10 Msun host): UNTESTED against satellites (CFG925 R3)",
 "C3 FAIL inherited (same static law)",
]
allP = P1 and P2 and P3 and P4 and P5
CLASS = "CONDITIONAL" if allP else "NOT FOUND"
P(f"\n  P1 law {P1} | P2 conservation {P2} | P3 well-posed (conditions) {P3} | P4 background {P4} | P5 slip {P5}")
P(f"  CLASS: {CLASS}")
for c_ in conditions:
    P(f"   - {c_}")
P("  Particle in disguise (CFG723): YES for the mass. F = -m c^2 n is a conserved-number rest-mass dust; its gravitating and inertial "
  "content is that of a cold matter component (one stream). The chi/lambda tether sector is not a particle (no propagating mode).")
RES["class"] = CLASS; RES["conditions"] = conditions; RES["flags"] = flags; RES["P"] = dict(P1=P1, P2=P2, P3=P3, P4=P4, P5=P5)
P("  Flags reported with equal prominence (data/structure, not part of P1-P5):")
for f_ in flags:
    P(f"   ! {f_}")
allchk = all(v["pass"] for v in RES["checks"].values())
P(f"\n  all checks pass: {allchk}; runtime {time.time() - T0:.1f} s; peak RSS {rss_guard_val() / 1e9:.3f} GB")
dump()
sys.exit(0 if (allchk and K_ALL) else 1)

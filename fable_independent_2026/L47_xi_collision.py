#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
L47 -- the coherence-length collision: xi = 0.10/0.15 pc (carried by the theory) vs xi >= 4 pc (L30's solve)
=============================================================================================================
THE COLLISION.  Two things the programme carries at the same time cannot both be right.

  (a) THE STANDING FLOOR.  The deposited theory (PAPER8, DOI 10.5281/zenodo.22667688) fixes the coherence
      length at xi = 0.10 pc canonical / 0.15 pc alt, calls it "theorem-forced", and Amendment 11 of the
      frozen Gaia-DR4 pre-registration computes arm B's registered wide-binary CEILINGS gamma_v = 1.0450 /
      1.0300 AT THOSE FLOORS.
  (b) L30's SOLVE.  Writing the action's own static scalar equation with the coherence operator and solving
      it drives a point source onto the biharmonic cone, giving an enclosed phantom-mass fraction
      M_ph(<r)/M = r^2/(2 xi^2) -- kernel-free, a0-free, mass-free -- and the Pitjev-Pitjeva Saturn bound
      then reads xi >= 4.00 pc, 27x the standing floor.  At 4 pc every DR4 pair is deep inside the healing
      length, which is exactly where the registered prediction lives.

WHAT THIS LANE DOES, in order.

  1  CONTROLS.  Independent machinery, from scratch: an analytic Green's function for the linearised
     carrier equation, verified symbolically; a 3-D FFT solve of the same operator; a nonlinear radial
     Newton BVP solver written in a different variable and a different discretisation from L30's.  These
     reproduce L30's K4 (the biharmonic cone), K5 (the xi -> 0 algebraic carrier law) and K6 (the analytic
     interior prediction over many exact solves), plus g03x's own standing floors from the repository's
     unedited machinery, plus g03d's gate constants, plus L34's shortfall, plus PAPER8's own printed
     screening numbers, plus the registered estimator's published gamma_v.
  2  IS THE CONE AN ARTEFACT OF THE POINT SOURCE?  Six source models -- point, uniform Sun, n = 3
     polytrope, Sun + eight planets, + local ISM, + the Oort-limit local mass density -- solved with the
     same fourth-order equation, phantom mass read at Saturn's orbit against Pitjev-Pitjeva directly.
  3  IS THE STANDING FLOOR BLIND TO THE FOURTH-ORDER OPERATOR?  The three screening laws the repository
     actually uses are rebuilt side by side at the same xi and the same observable, and the factor between
     them is decomposed analytically.
  4  IS xi >= 4 pc RIGHT, on both footings, and does it depend on L30's repair of the kernel?
  5  PROPAGATION TO THE REGISTERED PREDICTION.  gamma_v at the xi the analysis supports, through a
     re-implementation of the registered estimator that is first controlled against g03h's published
     1.032/1.040 and g03y's registered 1.0450/1.0300.
  6  THE DOCUMENTATION CONFLICT.  Which placement of the coherence operator, and which SOURCE for the
     scalar, each of the action document, the deposited paper, the standing-floor scripts and the
     registered gamma_v solver actually uses -- read out of the files themselves.

NOTHING IS WRITTEN INTO THE PRE-REGISTRATION.  This lane reports what an amendment would have to say.

Both a0 footings throughout: 9.3619e-11 (canonical) / 1.1279e-10 (alt).  Checks can fail; a FAIL is a
finding, not a crash.  Nothing in prep_2026/ or in the lead's trees is edited or executed for effect.
"""
import math, os, sys, io, json, time, contextlib, warnings
import numpy as np
import scipy.sparse as sps, scipy.sparse.linalg as spl
warnings.filterwarnings("ignore")

T0 = time.time()
FAILS = []
def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
def rel(p): return os.path.relpath(p, REPO)

# ------------------------------------------------------------------ constants (repository values, cited)
PC   = 3.0857e16
AU   = 1.495978707e11
G    = 6.6743e-11
MSUN = 1.98892e30
GM   = 1.32712440018e20                      # g02_filtered_efe.py / g03d line 21
A0   = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
R_SAT      = 9.54*AU                         # g02_filtered_efe.py line 43 (g03d/L43 use 9.58 AU; both reported)
R_SAT_G03D = 9.58*AU
M_SAT_BOUND = 6.7e-11                        # Pitjev-Pitjeva, in M_sun inside Saturn's orbit
A_SUNWARD  = 0.5*9.36e-11/1278.0             # g02 line 44, the alpha = 1 constant-sunward-acceleration gate
PLANETS = {"Mercury": 0.387*AU, "Venus": 0.723*AU, "Earth": AU, "Mars": 1.524*AU,
           "Jupiter": 5.203*AU, "Saturn": R_SAT, "Uranus": 19.19*AU, "Neptune": 30.07*AU}
PLANET_M = {"Mercury": 1.66e-7, "Venus": 2.447e-6, "Earth": 3.003e-6, "Mars": 3.213e-7,
            "Jupiter": 9.5458e-4, "Saturn": 2.858e-4, "Uranus": 4.366e-5, "Neptune": 5.151e-5}   # M/M_sun
R_SUN = 6.957e8
KAU = 1e3*AU

print("=" * 122)
print("L47 -- the coherence-length collision: the standing 0.10/0.15 pc floor against the action's own "
      "fourth-order equation")
print("=" * 122, flush=True)

# ==================================================================================================
# 0.  THE KERNEL, and the two structures the repository writes for the same scalar
# ==================================================================================================
print("""
0.  THE TWO STRUCTURES.  Everything below turns on ONE fork, so it is stated first, in the repository's
    own words and symbols.

    (i) THE CARRIER STRUCTURE.  PAPER5 section 7, g03x's docstring and L34's control A3 all assert that the
        MOND scalar is sourced by MATTER:            div[ J_Y(Y) grad phi ] = 4 pi G rho ,
        so on a sphere J_Y(g_phi) g_phi = g_N and g_phi = a0 Delta(g_N/a0).  This is the structure in which
        the bounded-boost theorem, the saturation, and L34's "no kernel of the class can screen the Solar
        System" corollary exist at all.  Amendment 11(b) registers arm B in exactly this structure
        ("nu_RAR carried and saturated at its maximum").

    (ii) THE AQUAL STRUCTURE.  g03c / g03d / g03g solve, for the SAME symbol,
        div[ mu(|grad(Phi_0 + psi)|/a0) grad psi ] - xi^2 Laplacian^2 psi = -div[ (mu - 1) grad Phi_0 ] ,
        i.e. psi is the CORRECTION to the Newtonian potential and its source is the (mu - 1)-suppressed
        phantom flux, not the point mass.  g03d's own docstring: "no point source, no screening of Newton".

    For a spherical monopole the two agree EXACTLY at xi = 0 -- that is what "the carried kernel" means, and
    it is why the fork was invisible.  They cannot agree once the fourth-order operator is switched on,
    because in (i) that operator has to fight the FULL point mass and in (ii) only (mu - 1) of it.  At
    Saturn (mu - 1) = C a0 / g_N = 9.3e-7.  That single factor is the whole collision.
""", flush=True)

SS = np.logspace(-9, 9, 900001)
DD = SS*(1.0/(1.0 - np.exp(-np.sqrt(SS))) - 1.0)                 # Delta(s) for nu_RAR, s = g_N/a0
_i = int(np.nanargmax(DD)); C_RAR = float(DD[_i]); S_SAT = float(SS[_i])
S_BR, D_BR = SS[:_i + 1], DD[:_i + 1]                            # the strictly increasing (invertible) branch

def Delta(s):
    """the carried kernel as the repository codes it: nu_RAR below the maximum, flat at C above it."""
    s = np.asarray(s, float)
    return np.where(s > S_SAT, C_RAR, s*(1.0/(1.0 - np.exp(-np.sqrt(np.maximum(s, 1e-300)))) - 1.0))

def Sinv(w):
    """s(Delta): the inverse of Delta on its increasing branch.  Used ONLY where Delta < C, so no
    continuation of the kernel past s_sat is invoked anywhere below -- check K6 certifies this."""
    return np.interp(np.clip(np.asarray(w, float), 0.0, D_BR[-1]), D_BR, S_BR)

def Sigma_par(w):
    """d s / d Delta = 1/Delta'(s) -- the longitudinal stiffness, from the inverse, by finite difference."""
    w = np.clip(np.asarray(w, float), 0.0, D_BR[-1]*(1 - 1e-12))
    h = np.maximum(1e-9*np.maximum(w, 1e-6), 1e-15)
    return np.maximum((Sinv(w + h) - Sinv(w - h))/(2*h), 0.0)

print(f"    carried kernel nu_RAR: C = sup Delta = {C_RAR:.6f} at s_sat = {S_SAT:.4f}; "
      f"C a0 = {C_RAR*A0['canonical']:.4e} (canonical) / {C_RAR*A0['alt']:.4e} (alt) m/s^2")
A_SAT_GATE = {f: G*MSUN*M_SAT_BOUND/R_SAT**2 for f in A0}        # the PP bound as an acceleration at R_Sat
print(f"    gates: Pitjev-Pitjeva M_ph(<Saturn) < {M_SAT_BOUND:.1e} M_sun  ==  "
      f"{A_SAT_GATE['canonical']:.4e} m/s^2 at r = {R_SAT/AU:.2f} AU;  alpha = 1 sunward "
      f"{A_SUNWARD:.4e} m/s^2")

# ==================================================================================================
# 1.  CONTROLS
# ==================================================================================================
print("\n" + "-" * 122)
print("1.  CONTROLS -- independent machinery, then L30's own controls reproduced with it")
print("-" * 122, flush=True)

# ---- 1a  the analytic Green's function of the LINEARISED carrier equation ------------------------
print("""
    1a  THE ANALYTIC GREEN'S FUNCTION.  Linearise the carrier equation about ANY background of stiffness
        Sigma (the galactic field, a cluster, nothing at all):   Sigma grad^2 phi - xi^2 grad^4 phi = 4 pi G rho.
        In Fourier  1/[k^2(Sigma + xi^2 k^2)] = (1/Sigma)[1/k^2 - 1/(k^2 + Sigma/xi^2)], i.e. Coulomb MINUS
        Yukawa of range l = xi/sqrt(Sigma), so for a point mass

            phi(r) = -(GM/Sigma)(1 - e^{-r/l})/r ,      w(r) = |phi'| = (GM/(Sigma r^2))[1 - e^{-r/l}(1 + r/l)]

        and, expanding, w(r -> 0) = GM/(2 xi^2) EXACTLY: the Sigma cancels.  The biharmonic cone is
        therefore not a property of the kernel, of the repair, of a0, or of the external field.""", flush=True)

def cone_shape(x):
    """1 - e^{-x}(1 + x), evaluated stably.  For x << 1 this is x^2/2 - x^3/3 + ... and the direct form
    loses every significant digit to cancellation, so the series is used there."""
    x = np.asarray(x, float)
    return np.where(x < 1e-3,
                    x**2/2 - x**3/3 + x**4/8 - x**5/30,
                    1.0 - np.exp(-np.minimum(x, 700.0))*(1.0 + x))

def w_analytic(r, GMs, Sig, xi):
    l = xi/math.sqrt(Sig); x = np.asarray(r, float)/l
    return GMs/(Sig*np.asarray(r, float)**2)*cone_shape(x)

try:
    import sympy as sy
    _r, _S, _x2, _GMs = sy.symbols("r Sigma xi2 GM", positive=True)
    _l = sy.sqrt(_x2/_S)
    _phi = -(_GMs/_S)*(1 - sy.exp(-_r/_l))/_r
    def lap(f): return sy.simplify(sy.diff(f, _r, 2) + 2*sy.diff(f, _r)/_r)
    _res = sy.simplify(_S*lap(_phi) - _x2*lap(lap(_phi)))
    ok_sym = (sy.simplify(_res) == 0)
    _lim = sy.simplify(sy.limit(sy.diff(_phi, _r), _r, 0))
    ok_lim = sy.simplify(_lim - _GMs/(2*_x2)) == 0
    check("K1a [control] the analytic Green's function satisfies Sigma grad^2 phi - xi^2 grad^4 phi = 0 away "
          "from the source, symbolically and for arbitrary Sigma", bool(ok_sym), f"sympy residual {_res}")
    check("K1b [control] its r -> 0 force limit is GM/(2 xi^2) exactly, with Sigma cancelling -- the "
          "biharmonic cone, derived without any kernel", bool(ok_lim), f"sympy limit {sy.simplify(_lim)}")
except Exception as e:                                                        # sympy optional
    d1 = max(abs(w_analytic(np.array([1e-6*PC]), GM, S, 1.0*PC)[0]/(GM/(2*(1.0*PC)**2)) - 1)
             for S in (0.05, 1.0, 2.55, 100.0))
    check("K1a [control] (sympy unavailable) the analytic Green's function's small-r force equals "
          "GM/(2 xi^2) for four values of Sigma", d1 < 1e-8, f"worst deviation {d1:.2e}; sympy said: {e}")
    check("K1b [control] placeholder for the symbolic PDE residual (sympy unavailable)", False, str(e))

d_sig = [abs(float(w_analytic(np.array([1e-12*PC]), GM, S, 1.0*PC)[0])/(GM/(2*(1.0*PC)**2)) - 1)
         for S in (0.03, 0.3, 3.0, 30.0, 300.0)]
check("K1c [control] the cone GM/(2 xi^2) is independent of the background stiffness Sigma over four "
      "decades (0.03 to 300), so it does not depend on the external field or on which kernel is carried",
      max(d_sig) < 1e-8, f"worst relative spread {max(d_sig):.2e} over Sigma = 0.03 ... 300, evaluated at "
                         f"r = 1e-12 pc; the residual is the leading -2r sqrt(Sigma)/(3 xi) correction, "
                         f"which is what makes the cone the r -> 0 LIMIT rather than a plateau")

# ---- 1b  an independent 3-D FFT solve of the same operator ---------------------------------------
def fft_yukawa_err(Sig, ell, N=160, Lfac=10.0, sigfac=0.06):
    """3-D periodic FFT solve of the LINEAR operator, differenced against xi = 0 so the residual is the
    short-ranged Yukawa and periodic images are exponentially harmless.  Entirely different code path."""
    L = Lfac*ell; h = L/N; GMs = 1.0
    xg = (np.arange(N) - N//2)*h
    X, Y, Z = np.meshgrid(xg, xg, xg, indexing="ij"); R = np.sqrt(X**2 + Y**2 + Z**2)
    sg = sigfac*ell
    rho = (GMs/G)*(2*math.pi*sg**2)**-1.5*np.exp(-R**2/(2*sg**2))
    k = 2*math.pi*np.fft.fftfreq(N, d=h); KX, KY, KZ = np.meshgrid(k, k, k, indexing="ij"); K2 = KX**2 + KY**2 + KZ**2
    F = np.fft.fftn(rho)
    dphi = np.real(np.fft.ifftn(4*math.pi*G*F*(ell**2/(Sig*(1.0 + ell**2*K2)))))
    sel = (R > 8*sg) & (R < 3.5*ell)
    an = (GMs/Sig)*np.exp(-R/ell)/np.maximum(R, 1e-30)
    return float(np.max(np.abs(dphi[sel]/an[sel] - 1.0)))
e_fft = [fft_yukawa_err(S, 1.0) for S in (1.0, 2.55)]
check("K2 [control] an independent 3-D FFT solve of the same linear operator reproduces the analytic "
      "Green's function to better than 5% (discretisation-limited) -- a different dimensionality and a "
      "different code path from any 1-D solver",
      max(e_fft) < 0.05, f"max relative error {max(e_fft):.3e} at Sigma = 1.0 and 2.55, 160^3 box")

# ---- 1c  the nonlinear radial solver: my own variable, my own stencil ----------------------------
print("""
    1c  THE NONLINEAR SOLVER.  The action's static scalar equation with the coherence operator OUTSIDE J,
        in spherical symmetry, integrated once (u = r^2 w, w = |grad phi|):

            J_Y(w) u  -  xi^2 ( u'' - 2 u'/r )  =  G M(<r) .

        Nondimensionalised with r_M = sqrt(GM/a0), x = r/r_M, u_hat = u/(r_M^2 a0), eps = xi/r_M, and using
        J_Y(w) w = a0 S(w_hat) with S the inverse of Delta:

            S(u_hat/x^2) x^2  -  eps^2 ( u_hat_xx - 2 u_hat_x/x )  =  m(x) .

        Solved by NEWTON in u_hat (L30 solved in q = s(w); the Jacobian, the variable and the linearisation
        are therefore different), on a uniform grid in t = ln x with u_hat_xx - 2u_hat_x/x = (u_hat_tt -
        3 u_hat_t)/x^2, boundary conditions u_hat(x_min) = 0 (regularity: this excludes the spurious
        extra-point-mass 1/r^2 branch) and u_hat(x_max) = the algebraic carrier law.  Positive stiffness
        S' = Sigma_par >= 0 makes the linear operator positive definite at every step.""", flush=True)

def solve_carrier(a0, xi, mfun=None, N=4001, xmin=1e-7, xmax=1e5, itmax=200, tol=1e-11, Mfac=1.0):
    """returns (r, w, iterations, convergence norm, max Delta reached / C)."""
    rM = math.sqrt(Mfac*GM/a0); eps = xi/rM
    t = np.linspace(math.log(xmin), math.log(xmax), N); h = t[1] - t[0]; x = np.exp(t)
    m = np.ones_like(x) if mfun is None else np.asarray(mfun(x*rM), float)
    s_alg = m/x**2
    u = x**2*np.minimum(Delta(s_alg), 1.0/(2*eps**2))
    u_out = float(x[-1]**2*Delta(np.array([s_alg[-1]]))[0])
    lam = x**2/eps**2
    d = np.inf
    for it in range(itmax):
        w = np.clip(u/x**2, 0.0, None); S0 = Sinv(w); Sg = Sigma_par(w)
        rhs = lam*(m - (S0 - Sg*w)*x**2)
        a_lo = -(1.0/h**2 + 1.5/h)*np.ones(N)
        a_dg = (2.0/h**2)*np.ones(N) + lam*Sg
        a_up = -(1.0/h**2 - 1.5/h)*np.ones(N)
        a_dg[0] = 1.0; a_up[0] = 0.0; rhs[0] = 0.0
        a_dg[-1] = 1.0; a_lo[-1] = 0.0; rhs[-1] = u_out
        A = sps.diags([a_lo[1:], a_dg, a_up[:-1]], [-1, 0, 1], format="csr")
        un = spl.spsolve(A, rhs)
        d = float(np.max(np.abs(un - u)/(np.abs(u) + 1e-12*np.max(np.abs(u)))))
        u = un
        if d < tol: break
    w = np.clip(u/x**2, 0.0, None)
    return x*rM, w*a0, it, d, float(np.max(w)/C_RAR)

# K3: the pure biharmonic limit -- the kernel switched off entirely (L30's K4, by a different route)
def solve_biharmonic(a0, xi, N=4001, xmin=1e-7, xmax=1e5):
    rM = math.sqrt(GM/a0); eps = xi/rM
    t = np.linspace(math.log(xmin), math.log(xmax), N); h = t[1] - t[0]; x = np.exp(t)
    lam = x**2/eps**2
    rhs = lam*np.ones(N)
    a_lo = -(1.0/h**2 + 1.5/h)*np.ones(N); a_dg = (2.0/h**2)*np.ones(N); a_up = -(1.0/h**2 - 1.5/h)*np.ones(N)
    u_out = x[-1]**2/(2*eps**2)
    a_dg[0] = 1.0; a_up[0] = 0.0; rhs[0] = 0.0
    a_dg[-1] = 1.0; a_lo[-1] = 0.0; rhs[-1] = u_out
    u = spl.spsolve(sps.diags([a_lo[1:], a_dg, a_up[:-1]], [-1, 0, 1], format="csr"), rhs)
    return x*rM, (u/x**2)*a0
rr, ww = solve_biharmonic(A0["canonical"], 0.5*PC)
w0_pred = GM/(2*(0.5*PC)**2)
w0_num = [float(np.interp(rp, rr, ww)) for rp in (R_SAT, 100*AU, 1000*AU)]
check("K3 [control] with the kernel switched off the solver's stencil reproduces the exact biharmonic cone "
      "w = GM/(2 xi^2) at three radii spanning two decades (reproduces L30's K4 with a different variable "
      "and a different discretisation)",
      max(abs(v/w0_pred - 1) for v in w0_num) < 0.01,
      f"worst deviation {100*max(abs(v/w0_pred - 1) for v in w0_num):.4f}% at xi = 0.5 pc")

# K4: xi -> 0 reproduces the algebraic carrier law (L30's K5)
k5 = []
for foot, a0 in A0.items():
    rM = math.sqrt(GM/a0)
    for e in (1e-4, 1e-3, 1e-2):
        r_, w_, it_, d_, _ = solve_carrier(a0, e*rM, xmax=1e4)
        num = float(np.interp(rM, r_, w_)); alg = a0*float(Delta(np.array([1.0]))[0])
        k5.append(abs(num/alg - 1))
check("K4 [control] at xi -> 0 the solver reproduces the algebraic carrier law w = a0 Delta(g_N/a0) at "
      "r = r_M, on both footings and three values of eps = xi/r_M (reproduces L30's K5)",
      max(k5) < 0.01, f"worst deviation {100*max(k5):.4f}% over {len(k5)} solves")

# K5: the analytic interior prediction over many exact solves (L30's K6)
XI_SCAN = np.array([0.05, 0.1, 0.3, 1.0, 2.0, 4.0, 6.0, 10.0, 30.0])*PC
cone_err = []; sat_frac = []; SOLVE = {}
for foot, a0 in A0.items():
    for xi in XI_SCAN:
        r_, w_, it_, d_, mx = solve_carrier(a0, xi)
        wS = float(np.interp(R_SAT, r_, w_))
        pred = min(GM/(2*xi**2), C_RAR*a0)
        cone_err.append(abs(wS/pred - 1)); sat_frac.append(mx)
        SOLVE[(foot, round(xi/PC, 3))] = dict(wS=wS, pred=pred, it=it_, d=d_, maxfrac=mx,
                                              r=r_, w=w_)
check("K5 [control] every one of the exact solves reproduces the analytic interior prediction "
      "min[GM/(2 xi^2), C a0] (reproduces L30's K6, with an independent solver)",
      max(cone_err) < 0.01, f"worst deviation {100*max(cone_err):.4f}% over {len(cone_err)} solves, "
                            f"both footings, xi = 0.05 to 30 pc")
check("K6 [control] no solve above ever enters the saturated branch, so the whole xi floor below is "
      "computed WITHOUT any continuation of the published kernel past s_sat: L30's repair is not what "
      "drives the number",
      max(sat_frac) < 0.999, f"largest Delta reached anywhere in any solve is {max(sat_frac):.4f} C "
                             f"(the plateau is never touched; at xi = 0.05 pc it comes closest)")

# K7: the repository's own filtered-proxy machinery reproduces the STANDING floors
G02 = os.path.join(REPO, "qwen_claude_field_theory/closure_2026/g02_filtered_efe.py")
gg = {"__file__": G02}
_src = open(G02).read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(_src[:_src.index("# ---------------------------------------------------------------- 3. the scans")],
                 "g02head", "exec"), gg)
eN_of, phantom_density, observables = gg["eN_of"], gg["phantom_density"], gg["observables"]
Q2_CEIL_g = gg["Q2_CEIL"]; MSB_g = gg["M_SAT_BOUND"]; ASUN_g = gg["A_SUNWARD"]
RSAT_g = gg["R_SAT"]; PL_g = gg["PLANETS"]; NU_EXP = gg["nu"]

def nu_rar_carried(s):
    s = np.asarray(s, float)
    return np.where(s <= S_SAT, 1.0/(1.0 - np.exp(-np.sqrt(np.maximum(s, 1e-300)))),
                    1.0 + C_RAR/np.maximum(s, 1e-300))

XIS_STD = np.array([0.01, 0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.15, 0.3, 1.0, 4.0])*PC
FIELDS = (("2.00", 2.00e-10), ("2.32", 2.32e-10), ("2.64", 2.64e-10))
def std_gate(nufun, grid=XIS_STD, want_rows=None):
    """g03x's gate, verbatim in structure: unfiltered QUMOND phantom density, ONE Helmholtz output filter."""
    gg["nu"] = nufun; out = {}; rows = {}
    for foot, a0 in A0.items():
        rM = math.sqrt(GM/a0); adm = {}
        for tag, gobs in FIELDS:
            eN = eN_of(gobs, a0)
            for xi in grid:
                r, th, rho = phantom_density(MSUN, 0.0, "gauss", eN, a0, 1e-4*rM, 1e4*rM)
                ob = observables(r, th, rho, xi, "helmholtz", a0)
                Msat = float(np.interp(RSAT_g, r, ob["Menc"]))
                gr = max(abs(float(np.interp(rp, r, ob["g_r"]))) for rp in PL_g.values())
                adm[(tag, xi)] = (abs(ob["Q2"]) < Q2_CEIL_g and Msat < MSB_g and gr < ASUN_g)
                if want_rows is not None and foot == want_rows and tag == "2.32":
                    rows[round(xi/PC, 3)] = (abs(ob["Q2"])/Q2_CEIL_g, Msat/MSB_g, gr/ASUN_g)
        ok = [xi for xi in grid if all(adm[(t, xi)] for t, _ in FIELDS)]
        out[foot] = round(min(ok)/PC, 3) if ok else None
    gg["nu"] = NU_EXP
    return out, rows

std_floor, std_rows = std_gate(nu_rar_carried, want_rows="canonical")
check("K7 [control] the repository's own filtered-proxy machinery (g02_filtered_efe.py imported unedited, "
      "driven exactly as g03x drives it) reproduces the STANDING floors for the carried kernel: 0.10 pc "
      "canonical / 0.15 pc alt -- the floors Amendment 11(b) and PAPER8 both carry",
      std_floor.get("canonical") == 0.1 and std_floor.get("alt") == 0.15, f"{std_floor}")

# K8: the gate constants and L34's shortfall
short = {f: C_RAR*A0[f]/A_SAT_GATE[f] for f in A0}
check("K8 [control] the gate constants rebuilt from g02/g03d's own numbers, and L34's published bare-kernel "
      "shortfall reproduced: 1.400e4x canonical / 1.687e4x alt against the binding Saturn phantom-mass gate",
      abs(short["canonical"]/1.400e4 - 1) < 0.03 and abs(short["alt"]/1.687e4 - 1) < 0.03,
      f"C a0 / gate = {short['canonical']:.3e} (canonical), {short['alt']:.3e} (alt); "
      f"gate {A_SAT_GATE['canonical']:.3e} m/s^2")

# K9: PAPER8's own printed screening numbers
p8_supp = (0.10*PC/R_SAT_G03D)**2
p8_frac = (C_RAR*A0["canonical"]/(1 + p8_supp))/(G*MSUN*M_SAT_BOUND/R_SAT_G03D**2)
check("K9 [control] PAPER8's own Solar-System screening formula, residual C a0 / (1 + (xi/R_Sat)^2) "
      "(L43_assemble_theory.py line 540), reproduces the paper's printed numbers: suppression 4.6e6 and "
      "3.0e-3 of the bound at xi = 0.10 pc",
      abs(p8_supp/4.6e6 - 1) < 0.05 and abs(p8_frac/3.0e-3 - 1) < 0.10,
      f"(xi/R_Sat)^2 = {p8_supp:.3e} (paper 4.6e6); screened/bound = {p8_frac:.3e} (paper 3.0e-3)")

# ==================================================================================================
# 2.  DOES r^2/(2 xi^2) SURVIVE A REALISTIC SOLAR-SYSTEM SOURCE?
# ==================================================================================================
print("\n" + "-" * 122)
print("2.  THE REALISTIC SOURCE -- the same fourth-order equation with six mass models, phantom mass read "
      "at Saturn against Pitjev-Pitjeva")
print("-" * 122, flush=True)

# n = 3 Lane-Emden mass profile, integrated here
from scipy.integrate import solve_ivp
def lane_emden_n3():
    def rhs(z, y): return [y[1], -np.abs(y[0])**3 - 2*y[1]/max(z, 1e-12)]
    sol = solve_ivp(rhs, [1e-8, 7.0], [1.0, 0.0], rtol=1e-10, atol=1e-14, dense_output=True, max_step=0.01)
    z = np.linspace(1e-8, 6.8968, 4000); th = sol.sol(z)[0]; dth = sol.sol(z)[1]
    zz = z[th > 0]; dd = dth[th > 0]
    Mz = -zz**2*dd                                       # proportional to enclosed mass
    return zz/zz[-1], Mz/Mz[-1]
LE_x, LE_m = lane_emden_n3()

RHO_ISM = 2.3e-21                                        # kg m^-3, n_H ~ 1 cm^-3 with helium
RHO_OORT = 0.1*MSUN/PC**3                                # local total (Oort-limit) mass density
R_LOCAL = 10.0*PC                                        # the local backgrounds are truncated here: beyond a
                                                         # few pc the Galaxy is not a uniform sphere centred
                                                         # on the Sun, and an untruncated model would only be
                                                         # testing an unphysical outer boundary condition

def m_point(r):     return np.ones_like(np.asarray(r, float))
def m_ball(r):      r = np.asarray(r, float); return np.clip((r/R_SUN)**3, 0.0, 1.0)
def m_poly(r):      r = np.asarray(r, float); return np.interp(np.clip(r/R_SUN, 0, 1), LE_x, LE_m)
def m_planets(r):
    r = np.asarray(r, float); m = m_poly(r)
    for p, a in PLANETS.items(): m = m + PLANET_M[p]*(r > a)
    return m
def m_ism(r):
    r = np.asarray(r, float); return m_planets(r) + (4*math.pi/3)*np.minimum(r, R_LOCAL)**3*RHO_ISM/MSUN
def m_oort(r):
    r = np.asarray(r, float); return m_planets(r) + (4*math.pi/3)*np.minimum(r, R_LOCAL)**3*RHO_OORT/MSUN
MODELS = [("point mass", m_point), ("uniform ball R_sun", m_ball), ("n = 3 polytrope", m_poly),
          ("+ eight planets", m_planets), ("+ local ISM (1 cm^-3)", m_ism),
          ("+ Oort-limit 0.1 Msun/pc^3", m_oort)]

print(f"      {'source model':30s} {'footing':10s} {'xi [pc]':>8s} {'w(Saturn) [m/s^2]':>18s} "
      f"{'M_ph(<Sat)/M':>13s} {'r^2/(2 xi^2)':>13s} {'ratio':>9s}")
src_dev = []
for nm, mf in MODELS:
    for foot in ("canonical", "alt"):
        a0 = A0[foot]
        for xipc in (4.0,):
            xi = xipc*PC
            r_, w_, it_, d_, mx = solve_carrier(a0, xi, mfun=mf)
            wS = float(np.interp(R_SAT, r_, w_))
            Mph = wS*R_SAT**2/(G*MSUN)
            law = R_SAT**2/(2*xi**2)
            src_dev.append(abs(Mph/law - 1))
            print(f"      {nm:30s} {foot:10s} {xipc:8.2f} {wS:18.5e} {Mph:13.5e} {law:13.5e} "
                  f"{Mph/law:9.5f}", flush=True)
check("R1 the enclosed phantom-mass law M_ph(<r)/M = r^2/(2 xi^2) survives a realistic Solar-System source: "
      "a finite Sun (uniform and n = 3 polytrope), the eight planets, the local interstellar medium and the "
      "full Oort-limit local mass density all leave it unchanged to better than 1%",
      max(src_dev) < 1e-2, f"worst departure from the point-source law over 12 solves is "
                           f"{100*max(src_dev):.3f}% (the Oort-limit background, which genuinely adds mass); "
                           f"the finite-Sun models are indistinguishable from the point mass at "
                           f"{100*max(src_dev[:6]):.3f}%, the leading correction being "
                           f"O((R_sun/R_Sat)^2) = {(R_SUN/R_SAT)**2:.2e}.  Every departure RAISES the "
                           f"phantom mass, so the floor moves up, not down")
print(f"      why: the fourth-order operator inverts to xi^2 grad^2 phi = -Phi_N, so w(r) = "
      f"(1/r^2) int_0^r [-Phi_N(r')] r'^2 dr'/xi^2 -- it responds to the enclosed POTENTIAL, and for any\n"
      f"      mass distribution wholly inside r that is GM/(2 xi^2) up to O((R_source/r)^2).  At Saturn "
      f"(R_sun/R_Sat)^2 = {(R_SUN/R_SAT)**2:.1e} and the ISM inside Saturn's orbit is "
      f"{(4*math.pi/3)*R_SAT**3*RHO_ISM/MSUN:.1e} M_sun.")

# the external field / nearest stars, handled analytically (K1c already shows Sigma cancels)
w_alpha_cen = 2.0*GM/(2*(4.0*PC)**2)
grad_alpha  = w_alpha_cen*(2.0/3.0)*(R_SAT/(1.34*PC))
print(f"      the nearest stars: alpha Cen (2 M_sun at 1.34 pc) contributes its own cone "
      f"{w_alpha_cen:.2e} m/s^2 at the Sun, but it varies by only\n      {grad_alpha:.2e} m/s^2 across "
      f"Saturn's orbit ({grad_alpha/A_SAT_GATE['canonical']:.1e} of the gate), so it is an external field, "
      f"not a monopole inside Saturn's orbit.")

# ==================================================================================================
# 3.  IS THE STANDING FLOOR BLIND TO THE FOURTH-ORDER OPERATOR?
# ==================================================================================================
print("\n" + "-" * 122)
print("3.  THE STANDING FLOOR -- the three screening laws the repository actually uses, side by side on the "
     "same observable")
print("-" * 122, flush=True)

print("""
    Same quantity in every row: the phantom mass inside Saturn's orbit as a fraction of the Pitjev-Pitjeva
    bound, for the CARRIED nu_RAR kernel.

      (A) PAPER8 / L43_assemble_theory.py line 540:  screened = C a0 / (1 + (xi/R_Sat)^2)     [a heuristic]
      (B) g03x / g02_filtered_efe.py, the source of the standing 0.10/0.15 pc floor: the QUMOND phantom
          density of an UNFILTERED point source, passed through ONE Helmholtz output filter of length xi.
          There is no fourth-order operator anywhere in this machinery.                        [a filter]
      (C) the action's own carrier equation with the coherence operator, solved:  w = GM/(2 xi^2).  [a solve]
""", flush=True)

print(f"      {'xi [pc]':>8s} | {'(A) PAPER8 formula':>19s} | {'(B) g03x filtered proxy':>23s} | "
      f"{'(C) fourth-order solve':>22s} | {'C/B':>9s} | {'C/A':>9s}")
ANAT = {}
for xipc in (0.05, 0.10, 0.15, 0.30, 1.0, 4.0):
    a0 = A0["canonical"]
    A_ = (C_RAR*a0/(1 + (xipc*PC/R_SAT)**2))/A_SAT_GATE["canonical"]
    B_ = std_rows.get(round(xipc, 3), (float("nan"),)*3)[1]
    C_ = min(GM/(2*(xipc*PC)**2), C_RAR*a0)/A_SAT_GATE["canonical"]
    ANAT[xipc] = (A_, B_, C_)
    print(f"      {xipc:8.2f} | {A_:19.4e} | {B_:23.4e} | {C_:22.4e} | {C_/B_:9.1f} | {C_/A_:9.3e}")

ratios_CB = [ANAT[x][2]/ANAT[x][1] for x in (0.10, 0.15, 0.30, 1.0) if not math.isnan(ANAT[x][1])]
check("S1 the standing floor's machinery and the action's fourth-order equation give the SAME xi-scaling "
      "(both ~ 1/xi^2) and differ only by a constant factor, so the disagreement is a normalisation, not a "
      "different physical law",
      max(ratios_CB)/min(ratios_CB) < 1.4,
      f"C/B = {[f'{v:.0f}' for v in ratios_CB]} over xi = 0.10 to 1.0 pc, spread "
      f"{max(ratios_CB)/min(ratios_CB):.2f}x; mean {np.mean(ratios_CB):.0f}")

fac_analytic = (GM/R_SAT**2)/(2*C_RAR*A0["canonical"])
check("S2 the factor between PAPER8's screening formula and the fourth-order solve is exactly "
      "g_N(Saturn)/(2 C a0) -- the paper applies the gradient-scale suppression (xi/R_Sat)^2 to the "
      "SATURATED RESIDUAL C a0, while the equation applies it to the FULL NEWTONIAN SOURCE",
      abs((ANAT[0.10][2]/ANAT[0.10][0])/fac_analytic - 1) < 0.02,
      f"measured {ANAT[0.10][2]/ANAT[0.10][0]:.4e} vs g_N(Sat)/(2 C a0) = {fac_analytic:.4e}")

# does the standing gate contain a fourth-order operator at all?
g02_src = open(G02).read()
g03x_src = open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/g03x_nurar_carrier_and_cassini.py")).read()
has_4th = any(tok in (g02_src + g03x_src) for tok in ("Delta^2", "Laplacian^2", "nabla^4", "grad^4", "D2@D2", "biharmon"))
check("S3 the machinery that produced the standing 0.10/0.15 pc floor evaluates the fourth-order coherence "
      "operator at all",
      has_4th,
      "neither g02_filtered_efe.py nor g03x_nurar_carrier_and_cassini.py contains any fourth-order "
      "operator: the screening there is a linear Helmholtz filter applied to the QUMOND phantom DENSITY, "
      "and the scalar's own equation is never solved.  L30's diagnosis is confirmed by reading the files")

# and the one script that DOES solve a fourth-order equation solves the other structure
g03d_src = open(os.path.join(REPO, "qwen_claude_field_theory/closure_2026/g03d_exact_fourth_order_solar.py")).read()
aqual_src = ("-div[ (mu - 1) grad Phi_0 ]" in g03d_src) or ("-div[(mu-1) grad Phi_0]" in g03d_src) \
            or ("no point source" in g03d_src)
supp = C_RAR*A0["canonical"]/(GM/R_SAT**2)
check("S4 the one standing script that DOES solve a fourth-order equation (g03d) applies it to a scalar "
      "that carries the point mass",
      not aqual_src,
      f"g03d's own docstring says the scalar has 'no point source, no screening of Newton': its source is "
      f"-div[(mu-1) grad Phi_0], suppressed at Saturn by (mu - 1) = C a0/g_N = {supp:.2e}.  The fourth-order "
      f"operator there never sees the Sun")

# ==================================================================================================
# 4.  THE FLOOR, BOTH FOOTINGS
# ==================================================================================================
print("\n" + "-" * 122)
print("4.  THE COHERENCE-LENGTH FLOOR the action's own equation forces")
print("-" * 122, flush=True)

xi_saturn = R_SAT/math.sqrt(2*M_SAT_BOUND)
xi_saturn_g03d = R_SAT_G03D/math.sqrt(2*M_SAT_BOUND)
xi_sunward = math.sqrt(GM/(2*A_SUNWARD))
print(f"      M_ph(<r)/M = r^2/(2 xi^2)  =>  Pitjev-Pitjeva  xi >= r_Saturn/sqrt(2 x 6.7e-11) = "
      f"{xi_saturn/PC:.3f} pc   (r_Sat = 9.54 AU; 9.58 AU gives {xi_saturn_g03d/PC:.3f} pc)")
print(f"      constant sunward acceleration GM/(2 xi^2) < {A_SUNWARD:.3e}      =>  xi >= "
      f"{xi_sunward/PC:.3f} pc")
print(f"      Saturn binds by {xi_saturn/xi_sunward:.2f}x.  NEITHER number contains a0, so the two footings "
      f"are identical -- which is itself a check: the standing floor 0.10/0.15 pc DOES differ between "
      f"footings, because\n      it comes from a machinery in which a0 enters.")

floors = {}
for foot, a0 in A0.items():
    adm = None
    for xipc in (0.05, 0.1, 0.3, 1.0, 2.0, 4.0, 6.0, 10.0, 30.0):
        s = SOLVE[(foot, round(xipc, 3))]
        wS = s["wS"]
        Mover = wS*R_SAT**2/(G*MSUN*M_SAT_BOUND)
        grmax = max(float(np.interp(rp, s["r"], s["w"])) for rp in PLANETS.values())
        if Mover < 1.0 and grmax < A_SUNWARD and adm is None: adm = xipc
    floors[foot] = adm
check("F1 the fourth-order carrier equation admits the repository's standing coherence-length floor "
      "(xi <= 0.15 pc)",
      floors["canonical"] is not None and floors["canonical"] <= 0.15,
      f"the smallest admissible tabulated xi is {floors['canonical']} pc (canonical) and {floors['alt']} pc "
      f"(alt); the analytic floor is {xi_saturn/PC:.2f} pc, {xi_saturn/(0.10*PC):.0f}x the canonical "
      f"standing floor and {xi_saturn/(0.15*PC):.0f}x the alt one")
check("F2 the floor xi >= 4.0 pc is the same on both footings, because the biharmonic cone contains "
      "neither a0 nor the kernel",
      floors["canonical"] == floors["alt"] == 4.0,
      f"canonical {floors['canonical']} pc, alt {floors['alt']} pc; analytic {xi_saturn/PC:.3f} pc for both")
check("F3 the 4 pc floor depends on L30's repair of the kernel past its saturation point",
      max(sat_frac) >= 0.999,
      f"it does not: no solve reaches more than {max(sat_frac):.3f} C, the interior sits at "
      f"Delta = {GM/(2*(4.0*PC)**2)/A0['canonical']:.2e} a0 (deep MOND), and the analytic derivation "
      f"(K1a-K1c) uses no kernel at all.  The repair is needed to WRITE the equation, not to get this number")

# the inside-J placement
print("\n      THE OTHER PLACEMENT.  With the operator inside J, as the action and PAPER8 both display it,")
print("      the interior balance is  w = GM/(2 xi^2 J_Y(w))  with J_Y at the screened (deep-MOND) gradient,")
print("      so  w = sqrt(GM a0/2)/xi  and the Saturn bound reads  xi >= r_Sat^2 sqrt(a0/2GM)/6.7e-11.")
xi_in = {}
for foot, a0 in A0.items():
    xi_in[foot] = R_SAT**2*math.sqrt(a0/(2*GM))/M_SAT_BOUND
    w_in = math.sqrt(GM*a0/2)/xi_in[foot]
    JY_true = float(Sinv(np.array([w_in/a0]))[0])/max(w_in/a0, 1e-300)
    print(f"      {foot:10s}: xi >= {xi_in[foot]/PC:.0f} pc; at that floor w = {w_in:.3e} m/s^2 = "
          f"{w_in/a0:.2e} a0, J_Y there = {JY_true:.4e} against the deep-MOND value "
          f"{w_in/a0:.4e} (ratio {JY_true/(w_in/a0):.4f})")
check("F4 the two placements of the coherence operator, which the action document and PAPER8 both call "
      "equivalent, give the same Solar-System floor",
      abs(xi_in["canonical"]/xi_saturn - 1) < 0.5,
      f"inside J: {xi_in['canonical']/PC:.0f} pc canonical / {xi_in['alt']/PC:.0f} pc alt, against "
      f"{xi_saturn/PC:.2f} pc outside J -- factors {xi_in['canonical']/xi_saturn:.0f} and "
      f"{xi_in['alt']/xi_saturn:.0f} apart.  BOTH exceed the standing floor by more than 25x, so the "
      f"collision does not depend on which placement is adopted")

# ==================================================================================================
# 5.  PROPAGATION TO THE REGISTERED PREDICTION
# ==================================================================================================
print("\n" + "-" * 122)
print("5.  ARM B -- the registered wide-binary ceilings recomputed at the xi the analysis supports")
print("-" * 122, flush=True)

print("""
    Inside the healing length the scalar force of each star is the CONSTANT GM_i/(2 xi^2), so for a pair of
    total mass M the relative radial acceleration is  G M/r^2 + G M/(2 xi^2)  and

        gamma_force(r) = 1 + [1 - e^{-x}(1 + x)]/Sigma ,   x = r sqrt(Sigma)/xi   ->   1 + r^2/(2 xi^2)

    independent of the masses, of the orientation, of the external field and of a0.  The largest DR4
    separation, 30 kAU, is r/l = 0.058 at xi = 4 pc, so the fourth-order term dominates the kernel term by
    (l/r)^2 = 300 and the nonlinear external-field machinery of g03g is irrelevant there: superposition of
    the two cones is exact to the second decimal in the correction itself.""", flush=True)

sys.path.insert(0, os.path.join(REPO, "prep_2026", "gaia_dr4_prep"))
import wide_binary_pipeline as P                                     # imported, never edited

SEPS = [3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
def gamma_force_cone(s_m, xi, Sig):
    l = xi/math.sqrt(Sig); x = s_m/l
    return 1.0 + float(cone_shape(np.array([x]))[0])/Sig

def run_estimator(Ms, S, tab, a0):
    """the registered pipeline's own estimator, re-implemented exactly as g03y calls it (g03y's own
    estimator body lives inside its __main__ block and cannot be imported)."""
    rng = np.random.default_rng(20261216)
    def fn(r3d, Mt):
        sk = np.clip(r3d/P.KAU, S[0], S[-1]); m = np.clip(Mt, Ms[0], Ms[-1])
        gl = np.interp(np.log(sk), np.log(S), tab[0]); gh = np.interp(np.log(sk), np.log(S), tab[-1])
        return np.sqrt(np.maximum(gl + (gh - gl)*(m - Ms[0])/(Ms[-1] - Ms[0]), 1e-6))
    pop = P.make_population(1_500_000, rng, dr4=True); logy = np.log10(pop["g_proj"]/a0)
    r3d = np.sqrt(P.G*pop["M_obs"]*P.MSUN/pop["g_true"]); gam = fn(r3d, pop["M_obs"])
    vX = (gam*pop["pmx"] + pop["npmx"])*4.74e3*(pop["d_obs"]/1000.)
    vY = (gam*pop["pmy"] + pop["npmy"])*4.74e3*(pop["d_obs"]/1000.)
    vt = np.hypot(vX, vY)/pop["vc_obs"]; mod = P.model_medians(pop, a0, P.GRID, rng)
    med, sig, cnt = P.bin_medians(logy, vt, boot=300, rng=rng)
    return P.fit_gamma(med, sig, mod, P.GRID)

def load_table(path):
    T = json.load(open(path))["table"]
    Ms = sorted({float(k.split("|")[0]) for k in T})
    S = sorted({s_ for s_ in {float(k.split("|")[1]) for k in T}
                if all(f"{M}|{s_}|{th}" in T for M in Ms for th in (("0.0", "45.0", "90.0") if M == 1.0 else ("0.0", "90.0")))})
    xs = np.array([1.0, math.cos(math.radians(45)), 0.0]); tab = np.zeros((len(Ms), len(S)))
    for i, M in enumerate(Ms):
        for j, s in enumerate(S):
            g0, g90 = T[f"{M}|{s}|0.0"]["gamma"], T[f"{M}|{s}|90.0"]["gamma"]
            if f"{M}|{s}|45.0" in T: g45 = T[f"{M}|{s}|45.0"]["gamma"]
            else:
                r0, r45, r90 = (T[f"1.0|{s}|{th}"]["gamma"] - 1 for th in (0.0, 45.0, 90.0))
                wgt = r45/(r0 + r90) if (r0 + r90) != 0 else 0.5
                g45 = 1 + wgt*((g0 - 1) + (g90 - 1))
            tab[i, j] = -np.trapz(np.array([g0, g45, g90]), xs)
    return np.array(Ms), np.array(S), tab

CL = os.path.join(REPO, "qwen_claude_field_theory/closure_2026")
ctrl0, ctrlB = {}, {}
for foot, a0p in (("canonical", P.A0_CAN), ("alt", P.A0_ALT)):
    f0 = os.path.join(CL, f"g03g_table_{foot}.json")
    if os.path.exists(f0):
        Ms0, S0, tab0 = load_table(f0); ctrl0[foot] = run_estimator(Ms0, S0, tab0, a0p)[0]
    f1 = os.path.join(CL, f"g03y_table_rar_carried_{foot}.json")
    if os.path.exists(f1):
        Ms1, S1, tab1 = load_table(f1); ctrlB[foot] = run_estimator(Ms1, S1, tab1, a0p)[0]
print(f"      estimator control: g03g's original table -> gamma_v = "
      f"{ctrl0.get('canonical', float('nan')):.4f} / {ctrl0.get('alt', float('nan')):.4f}  "
      f"(g03h published 1.032 / 1.040)")
print(f"      estimator control: g03y's rar_carried table -> gamma_v = "
      f"{ctrlB.get('canonical', float('nan')):.4f} / {ctrlB.get('alt', float('nan')):.4f}  "
      f"(Amendment 11(b) registered 1.0450 / 1.0300)")
check("K10 [control] the estimator used below reproduces BOTH published numbers: g03h's 1.032/1.040 from "
      "g03g's original table and Amendment 11(b)'s registered 1.0450/1.0300 from g03y's carried-kernel "
      "table.  Anything reported afterwards is physics, not a re-implementation difference",
      len(ctrl0) == 2 and len(ctrlB) == 2
      and abs(ctrl0["canonical"] - 1.032) < 0.002 and abs(ctrl0["alt"] - 1.040) < 0.002
      and abs(ctrlB["canonical"] - 1.0450) < 0.002 and abs(ctrlB["alt"] - 1.0300) < 0.002,
      f"g03g: {ctrl0.get('canonical', 0):.4f}/{ctrl0.get('alt', 0):.4f}; "
      f"g03y: {ctrlB.get('canonical', 0):.4f}/{ctrlB.get('alt', 0):.4f}")

# the external-field stiffness, for the (2%-level) correction term
GEXT = 1.7784e-10                                                    # g03g's banked 1.9 a0 at a0 = 9.36e-11
SIG_SET = {}
for foot, a0 in A0.items():
    ye = GEXT/a0
    s_e = float(np.interp(ye, S_BR + D_BR, S_BR))                    # y = s + Delta(s), inverted
    d_e = float(Delta(np.array([s_e]))[0])
    SIG_SET[foot] = (s_e/max(d_e, 1e-30), float(Sigma_par(np.array([d_e]))[0]))
print(f"      external-field stiffnesses at y_e = {GEXT/A0['canonical']:.3f} a0: "
      f"Sigma_perp = {SIG_SET['canonical'][0]:.3f}, Sigma_par = {SIG_SET['canonical'][1]:.3f} (canonical); "
      f"{SIG_SET['alt'][0]:.3f} / {SIG_SET['alt'][1]:.3f} (alt)")

XI_CASES = [("Saturn phantom-mass floor", xi_saturn/PC, True),
            ("sunward-gate floor only", xi_sunward/PC, True),
            ("standing floor 0.10 [diagnostic]", 0.10, False),
            ("standing floor 0.15 [diagnostic]", 0.15, False)]
ARMB = {}
print(f"\n      {'case':32s} {'xi [pc]':>8s} {'footing':10s} " +
      " ".join(f"{s:6.0f}k" for s in SEPS) + "   gamma_v (registered estimator)")
for lbl, xipc, supported in XI_CASES:
    for foot, a0p in (("canonical", P.A0_CAN), ("alt", P.A0_ALT)):
        Sig = SIG_SET[foot][0]
        row = [gamma_force_cone(s*KAU, xipc*PC, Sig) for s in SEPS]
        tab = np.vstack([row, row])
        gv, sg, chi2, nb, kap = run_estimator(np.array([1.0, 2.0]), np.array(SEPS), tab, a0p)
        ARMB[(lbl, foot)] = (xipc, gv, sg, row)
        print(f"      {lbl:32s} {xipc:8.3f} {foot:10s} " + " ".join(f"{g:7.5f}" for g in row) +
              f"   {gv:.5f} +/- {sg:.4f}", flush=True)
print("      the last two rows are a LINEAR-RESPONSE DIAGNOSTIC, not a solve: at xi = 0.10-0.15 pc the pair's\n"
      "      own field is not a small perturbation on the external field at 15-30 kAU, so the cone formula\n"
      "      overestimates there.  They are shown only to make the point that the carrier structure does NOT\n"
      "      return 1.0450/1.0300 at those lengths either -- and those lengths are excluded by 1600x anyway.\n"
      "      The first two rows ARE exact: at xi >= 1.38 pc every DR4 separation is deep inside the cone.")

# Sigma-sensitivity of the supported rows
sig_spread = max(abs(gamma_force_cone(20*KAU, xi_saturn, S)/gamma_force_cone(20*KAU, xi_saturn, 2.113) - 1)
                 for S in (1.0, 2.113, 12.92))
print(f"      Sigma-sensitivity at the supported xi: varying the background stiffness from 1.0 to 12.9 "
      f"(Sigma_perp to Sigma_par) moves gamma_force at 20 kAU by {sig_spread:.2e} -- the cone is "
      f"stiffness-free to that order.")

gv_sat = {f: ARMB[("Saturn phantom-mass floor", f)][1] for f in A0}
gv_sun = {f: ARMB[("sunward-gate floor only", f)][1] for f in A0}
gf20_sat = gamma_force_cone(20*KAU, xi_saturn, 2.113) - 1.0
gf20_reg = 1.0450**2 - 1.0
check("B1 Amendment 11(b)'s registered arm-B ceilings, 1.0450 (canonical) / 1.0300 (alt), are still the "
      "right numbers at the coherence length the action's own Solar-System equation supports",
      abs(gv_sat["canonical"] - 1.0450) < 0.005 and abs(gv_sat["alt"] - 1.0300) < 0.005,
      f"at xi = {xi_saturn/PC:.2f} pc the same registered estimator returns gamma_v = "
      f"{gv_sat['canonical']:.4f} (canonical) / {gv_sat['alt']:.4f} (alt), i.e. Newton to the estimator's "
      f"own resolution.  In the force boost, which does not round: {gf20_sat:.3e} at 20 kAU against the "
      f"registered ceiling's {gf20_reg:.3e} -- a factor {gf20_reg/gf20_sat:.0f}")
check("B2 the corrected arm-B prediction still lies strictly between Newton and the registered ceiling, so "
      "the registered ceiling is not FALSIFIED by this -- it is vacuous",
      1.0 <= gv_sat["canonical"] <= 1.0450 and 1.0 <= gv_sat["alt"] <= 1.0300 and gf20_sat > 0,
      f"{gv_sat['canonical']:.4f} <= 1.0450 and {gv_sat['alt']:.4f} <= 1.0300, and the boost is strictly "
      f"positive ({gf20_sat:.2e} at 20 kAU), so nothing registered is violated -- the ceiling is simply "
      f"{gf20_reg/gf20_sat:.0f}x too loose to exclude anything.  On the weaker sunward-only floor "
      f"xi >= {xi_sunward/PC:.2f} pc the ceiling would be {gv_sun['canonical']:.4f} / "
      f"{gv_sun['alt']:.4f}")

SIG_TOT, SIG_FIT = 0.028, 0.019
kill_old = 1.0450 + 3*SIG_TOT
kill_new = {f: gv_sat[f] + 3*SIG_TOT for f in A0}
check("B3 Amendment 11(d)'s decision rule still kills arm B at the right place",
      abs(kill_old - 1.129) < 0.002 and abs(kill_new["canonical"] - 1.129) < 0.005,
      f"the registered kill-from-above threshold is ceiling + 3 sigma_tot = {kill_old:.3f} (the table's "
      f"1.129).  At the supported xi the ceiling is {gv_sat['canonical']:.5f}, so the threshold should be "
      f"{kill_new['canonical']:.3f}: a DR4 value in [{kill_new['canonical']:.3f}, {kill_old:.3f}] would "
      f"kill arm B and the registered table would not say so")

xi_for_ceiling = math.sqrt(20*KAU*20*KAU/(2*(1.0450**2 - 1)))
check("B4 within the carrier structure there exists a coherence length that simultaneously passes the "
      "Solar System and returns the registered ceiling gamma_v = 1.0450",
      xi_for_ceiling >= xi_saturn,
      f"gamma_v = 1.0450 at 20 kAU needs xi = {xi_for_ceiling/PC:.3f} pc, which the same structure excludes "
      f"by {(xi_saturn/xi_for_ceiling)**2:.0f}x on the Saturn phantom mass.  The registered ceiling and "
      f"the Solar-System gate are mutually exclusive INSIDE the carrier structure, separated by a factor "
      f"{xi_saturn/xi_for_ceiling:.0f} in xi")

# ==================================================================================================
# 6.  THE DOCUMENTATION CONFLICT -- placement AND source, read out of the files
# ==================================================================================================
print("\n" + "-" * 122)
print("6.  WHICH EQUATION EACH DOCUMENT AND EACH SCRIPT ACTUALLY USES")
print("-" * 122, flush=True)

def read(p): return open(os.path.join(REPO, p), encoding="utf-8", errors="replace").read()
ACT = read("qwen_claude_field_theory/closure_2026/THE_ACTION_2026-09-05.md")
P8  = read("qwen_claude_field_theory/papers_2026/PAPER8_complete_theory_2026.tex")
G3D = read("qwen_claude_field_theory/closure_2026/g03d_exact_fourth_order_solar.py")
G3G = read("qwen_claude_field_theory/closure_2026/g03g_3d_pair_solver.py")
G3Y = read("qwen_claude_field_theory/closure_2026/g03y_gammav_corrected_floors.py")
L43 = read("fable_independent_2026/L43_assemble_theory.py")
PRG = read("prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md")

DOC = [
    ("THE_ACTION_2026-09-05.md §1", "inside J" if "J( Y + ξ²" in ACT or "J( Y +" in ACT else "?",
     "carrier (AeST coupling 2(2-K_B) J^mu d_mu phi, statically div J = grad^2 Psi)"),
    ("PAPER8 (DOI 22667688) eq. (1)", "inside J" if "Y+\\xi^2" in P8 else "?",
     "carrier (PAPER5 §7's theorem is quoted as the reason xi exists)"),
    ("g03d_exact_fourth_order_solar.py", "outside J (bare xi^2 Delta^2 psi)",
     "AQUAL correction: -div[(mu-1) grad Phi_0], 'no point source'"),
    ("g03g_3d_pair_solver.py  [arm B's solver]", "outside J (bare xi^2 Delta^2 psi)",
     "AQUAL correction: -div[(mu-1) grad Phi_0]"),
    ("g02/g03x  [the standing floor]", "no fourth-order operator at all",
     "QUMOND phantom density + one Helmholtz output filter"),
    ("L43_assemble_theory.py line 540", "no operator: heuristic C a0/(1+(xi/R_Sat)^2)", "n/a"),
    ("L30 / L47 Gate 2", "outside J (bare xi^2 grad^4 phi)", "carrier: 4 pi G rho"),
]
print(f"      {'document / script':44s} {'placement of the coherence operator':38s} source of the scalar")
for a, b, c in DOC: print(f"      {a:44s} {b:38s} {c}")

act_inside = ("ξ² q^{λσ}" in ACT) or ("\\xi^2" in ACT and "J( Y +" in ACT) or ("J( Y + ξ²" in ACT)
p8_inside  = ("Y+\\xi^2\\,q^{\\lambda\\sigma}" in P8) or ("Y+\\xi^2" in P8)
solver_outside = ("xi^2 Delta^2 psi" in G3G) or ("xi**2*box.K2**2" in G3G)
solver_aqual = ("-div[(mu - 1) grad Phi_0]" in G3G) or ("(mu - 1) grad Phi_0" in G3G) or ("mu - 1) grad Phi_0" in G3G)
check("D1 the deposited paper and the action document display the coherence operator INSIDE J",
      act_inside and p8_inside,
      f"THE_ACTION §1: J( Y + xi^2 q^(lambda sigma) q^(mu nu) grad_lambda V_mu grad_sigma V_nu ); "
      f"PAPER8 eq. (1): the same, verbatim.  Both then add that it 'may equivalently sit outside J'")
check("D2 the solver that produced the registered arm-B number uses the SAME placement as the deposited "
      "paper",
      not solver_outside,
      "g03g_3d_pair_solver.py (via g03y) solves 'div[mu grad psi] - xi^2 Delta^2 psi', a bare fourth-order "
      "term with a constant coefficient -- the OUTSIDE-J placement.  The paper displays the inside-J one, "
      "and L30/L47 measure the two placements' Solar-System floors as 4.0 pc and ~590 pc: they are not "
      "interchangeable")
check("D3 the solver that produced the registered arm-B number uses the SAME source for the scalar as the "
      "structure Amendment 11(b) registers ('nu_RAR carried and saturated at its maximum')",
      not solver_aqual,
      "g03g solves the AQUAL correction equation, whose source is -div[(mu-1) grad Phi_0]; the carried "
      "structure the amendment names sources the scalar with 4 pi G rho.  The two agree exactly at xi = 0 "
      "and differ by (mu-1) = C a0/g_N once the fourth-order term is switched on")
amend_names_carrier = "nu_RAR carried and saturated at its maximum" in PRG
amend_names_floor = ("0.10 pc\n> canonical / 0.15 pc alt" in PRG) or ("ξ ≥ 0.10 pc" in PRG)
check("D4 [record] Amendment 11(b) names the carrier structure and the 0.10/0.15 pc floor together, so the "
      "conflict is visible inside a single registered clause",
      amend_names_carrier,
      "Amendment 11(b): 'the coherence operator ξ²|∇⊥V|² inside the kernel; ν_RAR carried and saturated at "
      "its maximum' and 'ξ ≥ 0.10 pc canonical / 0.15 pc alt ... (g03d_exact_fourth_order_solar.py)' -- "
      "the operator is named inside the kernel, the floor is taken from a solve that puts it outside AND "
      "removes the point source")

# ==================================================================================================
# 7.  VERDICT
# ==================================================================================================
print("\n" + "-" * 122)
print("7.  VERDICT -- which coherence length the programme should carry")
print("-" * 122, flush=True)

print(f"""
    In the CARRIER structure -- the one PAPER5's bounded-boost theorem needs, the one L34's screening
    corollary is derived in, the one PAPER8 says is the reason xi exists at all, and the one Amendment
    11(b) names -- the action's own static scalar equation gives

        M_ph(<r)/M = r^2/(2 xi^2)      exactly, for any kernel, any a0, any external field, any mass, and
                                       any realistic Solar-System mass distribution (12 solves, section 2)

    so the Solar System forces  xi >= {xi_saturn/PC:.2f} pc  (Pitjev-Pitjeva) or  xi >= {xi_sunward/PC:.2f} pc
    (the profile-appropriate constant-sunward-acceleration gate alone), on BOTH footings.  The standing
    0.10/0.15 pc comes from a filtered proxy with no fourth-order operator in it, cross-checked against a
    fourth-order solve of the OTHER structure and against a heuristic that suppresses the residual rather
    than the source.  Nothing in the standing chain evaluates the equation the action writes.

    In the AQUAL structure the residual vanishes in the Solar System by itself (PAPER8 §: "only the carrier
    arm needs a coherence length at all"), xi is set by the Cassini QUADRUPOLE at 0.03/0.05 pc, and neither
    the bounded-boost theorem nor arm B's saturation exists.  That is a DIFFERENT theory, not a rescue of
    this one, and it is the theory the registered gamma_v solver actually solves.

    The programme must pick one.  It cannot register arm B as the carrier structure and evaluate its
    coherence length and its wide-binary boost in the AQUAL one.""", flush=True)

verdict_ok = (floors["canonical"] == 4.0 and floors["alt"] == 4.0 and max(sat_frac) < 0.999
              and max(src_dev) < 1e-2 and not has_4th)
check("V1 [verdict] the coherence length the programme should carry, inside the structure it registers, is "
      "xi >= 4.0 pc (Saturn) / 1.38 pc (sunward gate alone) on both footings -- NOT 0.10/0.15 pc",
      verdict_ok,
      f"floors {floors}; no continuation used (max Delta = {max(sat_frac):.3f} C); the law survives six "
      f"source models to {100*max(src_dev):.3f}%; the standing machinery contains no fourth-order operator")
check("V2 [verdict] Amendment 11 needs no correction before DR4",
      abs(gv_sat["canonical"] - 1.0450) < 0.005,
      f"it does: the registered ceilings 1.0450/1.0300 become {gv_sat['canonical']:.5f}/{gv_sat['alt']:.5f} "
      f"at xi = {xi_saturn/PC:.2f} pc (and {gv_sun['canonical']:.5f}/{gv_sun['alt']:.5f} at "
      f"{xi_sunward/PC:.2f} pc), identical on both footings, and the kill-from-above threshold moves from "
      f"1.129 to {kill_new['canonical']:.3f}.  NOT WRITTEN HERE -- reported for the owner")

print(f"""
    WHAT AN AMENDMENT WOULD HAVE TO SAY (text is NOT written into the pre-registration by this lane):

      (i)   Arm B's coherence-length floor, in the carrier structure Amendment 11(b) names, is
            xi >= {xi_saturn/PC:.2f} pc from the Pitjev-Pitjeva Saturn phantom mass and xi >= {xi_sunward/PC:.2f} pc from the
            alpha = 1 sunward gate alone, IDENTICAL on both footings because the biharmonic cone contains
            no a0.  The floors 0.10 pc / 0.15 pc are superseded.
      (ii)  Arm B's ceiling therefore becomes gamma_v <= {1 + 0.5*gf20_sat:.5f} (both footings) on the Saturn gate, or
            gamma_v <= {gv_sun['canonical']:.4f} (both footings) if only the sunward gate is taken.  1.0450 / 1.0300 are
            superseded and must not be scored.  They are not falsified -- the true value stays below them --
            but they are {gf20_reg/gf20_sat:.0f}x too loose in the force boost and no longer exclude anything.
      (iii) Amendment 11(d)'s row "gamma >= 1.129 -> arm B falsified" must move to {kill_new['canonical']:.3f} on the Saturn
            gate ({gv_sun['canonical'] + 3*SIG_TOT:.3f} on the sunward gate).  Amendment 11(e)'s statement that DR4 cannot
            separate arm B from Newton becomes stronger, not weaker: the predicted boost at 20 kAU is
            {gf20_sat:.2e} in force, i.e. {0.5*gf20_sat/SIG_TOT:.4f} sigma_tot in gamma_v, so the wide-binary channel
            stops being a test of arm B at all -- it can only kill it from above.
      (iv)  The row "1.007 - 1.056 -> the arm question is decided for B" is no longer right: at the
            supported xi, a measurement anywhere in that range is 0.2-2.0 sigma_tot ABOVE arm B, not
            consistent with it as its own prediction.
      (v)   PAPER8's parameter table entry "xi >= 0.10 pc canonical / 0.15 pc alt --- theorem-forced" and
            its §"the operator's gradient-scale suppression (xi/R_Sat)^2" need the same correction: the
            suppression applies to the Newtonian source, not to the saturated residual, a factor
            g_N(Saturn)/(2 C a0) = {fac_analytic:.2e}.
      (vi)  The action document's "it may equivalently sit outside J" is false as a statement about the
            Solar System: the two placements' floors are {xi_saturn/PC:.1f} pc and {xi_in['canonical']/PC:.0f} pc.
""", flush=True)

print("\n" + "=" * 122)
print(f"RESULT: {len(FAILS)} FAIL -> {FAILS}" if FAILS else "RESULT: 0 FAIL", f"   ({time.time() - T0:.0f} s)")
print("=" * 122, flush=True)
sys.exit(0)

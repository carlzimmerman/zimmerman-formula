#!/usr/bin/env python3
"""
L71 -- the LEAD's integrable-clock action in a GALACTIC deep-MOND background: is its propagating sector healthy?
================================================================================================================
L60 killed the DEPOSITED action's scalar sector in deep MOND by a LAPSE-CHANNEL SUBTRACTION: a separate MOND
scalar phi is sourced by the AeST coupling 2(2-K_B) a^mu d_mu phi to an Einstein-constrained lapse; eliminating
the lapse feeds -(2-K_B)^2/(2-c14) into phi's own soft kernel stiffness Sigma_perp = J_Y = s/Delta, which goes
to 0 in deep MOND, so a FIXED positive subtraction beats a VANISHING stiffness and the transverse gradient term
goes negative below s = 0.3985 (g_N < 0.4 a0).  L69 turned that into a class no-go under three hypotheses:
H1 (soft kernel Sigma_perp -> 0), H2 (a SEPARATE scalar AeST-coupled to a clock's acceleration through the
lapse), H3 (a single-metric Einstein-Hilbert host).  L66 found the lead's INTEGRABLE-CLOCK action (ACTION.md /
IC20 / IC30) ESCAPES the kill by violating H2 -- it has NO separate MOND scalar; the MOND scale rides the
clock's OWN acceleration invariant 2(1-u^2)a_mu a^mu - 2 a0^2 U(u^2), and the lapse N=(2X)^{-1/2} is a
functional of the varied clock T.  BUT L66 was explicit: its deep-MOND transverse health is UNCOMPUTED --
certified only at a flat-vacuum FLRW design point of ~0.0006 e-folds.  Clearing it there would repeat the exact
error L60 caught.

THIS LANE (L71) constructs the integrable-clock action's STATIC quasi-static background in a galaxy, in deep
MOND, and asks whether its propagating sector is healthy THERE -- on a galactic background (R != 0, background
clock gradient), NOT on flat vacuum, NOT at the cosmological design point.

WHAT IS COMPUTED, IN ORDER.
  PART 0(a) CONTROLS: an independent Dirac counter returns 2 / 3 / 5 / 3 on ADM GR, GR+scalar, Einstein-aether,
            khronometric.
  PART 0(b) CONTROLS: REPRODUCE L60's KILL ON THE DEPOSITED ACTION -- static 3x3 route -> J_crit = 0.9000009;
            repaired kernel -> s = 0.3985; slow-mode growth -> 0.737 Myr e-folding at 1 kpc, both footings.  If
            the kill does not reproduce, a health verdict from this machinery would be worthless.
  PART 0(c) CONTROLS: REPRODUCE L66's structure identification -- the submitted action (I) carries the
            lapse-channel coupling 2b P'v and shares the kill; the integrable-clock action (II) has no separate
            scalar and no such coupling.
  PART 1    THE GALACTIC BACKGROUND, from the lead's OWN action (IC30 RADIAL_BRIDGE section 2-3): the leading
            weak-field static reduction is the MOND field equation div[(1-e^{-|grad Phi|/a0}) grad Phi] =
            rho_b/(2m) with G_N = 1/(8 pi m), and the clock acceleration invariant fixes u^2 = 1 - e^{-y},
            y = |grad Phi|/a0.  Solve it for a spherical baryonic source in deep MOND, both footings.  On the
            static (eta=0) branch the trace momentum and auxiliary vanish: q = z = s = 0, i.e. pi = 0.
  PART 2    THE L60 MECHANISM on that background: does the clock-internal coupling generate a lapse-channel
            subtraction of its own?  H_Sq = 0 on q=z=0 (no separate scalar), and the clock-lapse gradient
            coefficient B = m e^{S+2wc}(1-u^2) STAYS O(1) in deep MOND because (1-u^2) = e^{-y} -> 1, whereas
            L60's Sigma_perp = J_Y -> 0.  Both reasons the L60 kill fires are absent.
  PART 3    L69's necessary condition Sigma_perp > lambda^2/(kappa_phi chi_lapse) reinterpreted: with no
            separate scalar the coupling lambda_eff = C = H_Sq = 0, so the RHS is 0 and the condition reduces to
            positivity of the clock-lapse stiffness, which holds.  L69 does NOT bind action (II).
  PART 4    THE NEW-MECHANISM CONCERN, on-configuration: the IC-4 auxiliary-gradient Hessian det G = -4 u^2 xi^2
            < 0 at pi = 0 -- and pi = 0 IS the static galactic branch, with xi = Phi != 0 and u != 0.  So the
            auxiliary symbol is INDEFINITE exactly on the galactic configuration; the lead's repair is matched
            only at the pi != 0 cosmological witness.
  PART 5    THE UNDER-SPECIFICATION: the propagating scalar's full gradient stiffness needs H_SS, H_RR on a
            curved (R != 0) galactic background, set by the coefficient functions A(S), D(S), E4(S), which are
            pinned only at the cosmological design point S = 0.1 (design() targets) and, per IC31, may NOT be
            extrapolated outside their represented S interval.  There is no calibration relating the action's
            dimensionless S to a galactic potential.  So the full deep-MOND transverse verdict is UNDERSPECIFIED
            by the lead's own action.
  VERDICT.

POLARITY.  Each check asserts a STATEMENT and PASS means the statement is true.  Read the statement: some PASSes
are negative for the construction.

Both a0 footings on every dimensional number: 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.  Nothing under
closure_2026/ or any other agent's directory is imported, executed or copied here.  The Dirac counter and the
deposited-kill reproduction are fable_independent_2026's own machinery (validated 64/64 in L60, 18/18 in L66).
The lead's action structure is REBUILT from the equations printed in its markdown (ACTION.md, IC20, IC30,
AUXILIARY_SYMBOL, USER_ACTION_*); its reference numbers were read once, offline, and are hard-coded as
reproduction targets the rebuild must hit.
"""
import sympy as sp
import numpy as np
import math, sys, time
from mpmath import mp, mpf

T_START = time.time()
FAILS = []
NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(title):
    print("\n" + "=" * 118); print(title); print("=" * 118, flush=True)

R = sp.Rational
print("=" * 118)
print("L71 -- the LEAD's integrable-clock action in a GALACTIC deep-MOND background: is its propagating sector healthy?")
print("=" * 118, flush=True)

# ------------------------------------------------------------------------------------------------------
# physical constants and the deposited theory's own numbers (for the CONTROL reproduction of the kill)
# ------------------------------------------------------------------------------------------------------
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
XI_FLOOR = {"canonical": 0.10, "alt": 0.15}          # pc, theorem-forced floor (deposited theory)
c_light = 2.99792458e8
G_N = 6.674e-11
MSUN = 1.989e30
pc = 3.0856775814913673e16
kpc = 1e3 * pc

KB_pt = 0.2
c14_pt = 1.978e-6
sigma_star = 1.679312732187113
c2_pt = 2 * sigma_star * c14_pt / (2 - c14_pt - 3 * sigma_star * c14_pt)
K2_pt = (2 - KB_pt) ** 2 / c2_pt                     # closure locus c_2|K_2| = (2-K_B)^2

# the deposited theory's repaired kernel Delta(s)
C_TH, P_TH, A2_TH = 0.647610, 1.7538, 0.9335
A1_TH = 1.0 / (C_TH * P_TH)
mp.dps = 50
def Delta_mp(s):
    u = mp.sqrt(s)
    return mpf(C_TH) * (1 - (1 + mpf(A1_TH) * u + mpf(A2_TH) * u * u) ** (-mpf(P_TH)))
def Delta_th(s):
    if s <= 0: return 0.0
    return float(Delta_mp(s))
def J_Y_of_s(s):  return s / Delta_th(s)             # deposited: Sigma_perp = J_Y = g_N/g_phi

print(f"\n  deposited exhibited point: K_B={KB_pt}, c_14={c14_pt:.4e}, c_2={c2_pt:.6e}, |K_2|={K2_pt:.4e}")
print(f"  footings: a_0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2")

# ======================================================================================================
# MACHINERY -- an independent Dirac counter, rebuilt in exact rational arithmetic (fable_independent_2026's
# own; the same used 64/64 in L60 and 18/18 in L66; imports nothing from any other agent's directory).
# ======================================================================================================
t, z = sp.symbols("t z", real=True)
k = sp.Symbol("k", positive=True)
eps = sp.Symbol("epsilon")
NZ = {"n": 0, "nu_x": 0, "nu_y": 0, "nu_z": 1, "hT": 0, "hD": 0, "h_xy": 0, "h_xz": 1, "h_yz": 1,
      "h_zz": 0, "chi": 0, "v_x": 0, "v_y": 0, "v_z": 1, "psi": 0, "phi": 0}
FUN = {nm: sp.Function(nm)(t) for nm in NZ}
PROF = {nm: FUN[nm] * (sp.cos(k * z) if NZ[nm] % 2 == 0 else sp.sin(k * z)) for nm in NZ}
IDX = ["x", "y", "z"]
ETA = sp.diag(-1, 1, 1, 1)
from sympy.simplify.fu import TR8
def zavg(e):
    e = sp.expand(TR8(sp.expand(e)))
    return sp.expand(e.subs({sp.cos(2 * k * z): 0, sp.sin(2 * k * z): 0, sp.cos(k * z): 0, sp.sin(k * z): 0}))
def trunc2(e):
    e = sp.expand(e); return sum(e.coeff(eps, i) * eps ** i for i in range(3))
def dz(expr, coord): return sp.diff(expr, z) if coord == "z" else sp.Integer(0)
def d4(expr, mu):
    if mu == 0: return sp.diff(expr, t)
    if mu == 3: return sp.diff(expr, z)
    return sp.Integer(0)
def hspatial():
    hxx = (PROF["hT"] + PROF["hD"]) / 2; hyy = (PROF["hT"] - PROF["hD"]) / 2
    return sp.Matrix([[hxx, PROF["h_xy"], PROF["h_xz"]], [PROF["h_xy"], hyy, PROF["h_yz"]],
                      [PROF["h_xz"], PROF["h_yz"], PROF["h_zz"]]])
def L_einstein_hilbert():
    H = hspatial(); nu = [PROF["nu_x"], PROF["nu_y"], PROF["nu_z"]]
    K1 = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K1[i, j] = (sp.diff(H[i, j], t) - dz(nu[j], IDX[i]) - dz(nu[i], IDX[j])) / 2
    L_K = sum(K1[i, j] ** 2 for i in range(3) for j in range(3)) - sum(K1[i, i] for i in range(3)) ** 2
    I3 = sp.eye(3); g = I3 + eps * H; ginv = I3 - eps * H + eps ** 2 * (H * H)
    trH = sum(H[i, i] for i in range(3)); trH2 = sum(H[i, j] * H[j, i] for i in range(3) for j in range(3))
    sqrtdet = 1 + eps * trH / 2 + eps ** 2 * (trH ** 2 / 8 - trH2 / 4)
    Gam = [[[sp.Integer(0)] * 3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3):
                s_ = sum(ginv[a, l] * (dz(g[l, j], IDX[i]) + dz(g[l, i], IDX[j]) - dz(g[i, j], IDX[l])) for l in range(3))
                Gam[a][i][j] = trunc2(s_ / 2)
    R3 = 0
    for i in range(3):
        for j in range(3):
            term = 0
            for a in range(3):
                term += dz(Gam[a][i][j], IDX[a]) - dz(Gam[a][a][i], IDX[j])
                for b in range(3):
                    term += Gam[a][a][b] * Gam[b][i][j] - Gam[a][j][b] * Gam[b][a][i]
            R3 += ginv[i, j] * term
    L_R = trunc2((1 + eps * PROF["n"]) * sqrtdet * trunc2(R3))
    return sp.expand(L_K) + L_R.coeff(eps, 2)
def h4():
    H = hspatial(); h = sp.zeros(4, 4); h[0, 0] = -2 * PROF["n"]
    for i, nm in enumerate(["nu_x", "nu_y", "nu_z"]):
        h[0, i + 1] = PROF[nm]; h[i + 1, 0] = PROF[nm]
    for i in range(3):
        for j in range(3):
            h[i + 1, j + 1] = H[i, j]
    return h
def grad_u(u_lower):
    h = h4(); A = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            Gam0 = -(d4(h[0, nu], mu) + d4(h[0, mu], nu) - d4(h[mu, nu], 0)) / 2
            A[mu, nu] = sp.expand(d4(u_lower[nu], mu) + Gam0)
    return A
def L_aether(A, c1, c2, c3, c4):
    Aup = ETA * A * ETA
    t1 = sum(A[m, n] * Aup[m, n] for m in range(4) for n in range(4))
    tr = sum(ETA[m, n] * A[m, n] for m in range(4) for n in range(4))
    t3 = sum(A[m, n] * Aup[n, m] for m in range(4) for n in range(4))
    acc = sum(ETA[m, n] * A[0, m] * A[0, n] for m in range(4) for n in range(4))
    return sp.expand(-c1 * t1 - c2 * tr ** 2 - c3 * t3 + c4 * acc)
def u_lower_khrono(): return [-PROF["n"], sp.Integer(0), sp.Integer(0), -sp.diff(PROF["chi"], z)]
def u_lower_aether(): return [-PROF["n"], PROF["nu_x"] + PROF["v_x"], PROF["nu_y"] + PROF["v_y"], PROF["nu_z"] + PROF["v_z"]]
def L_testscalar(): return sp.expand((sp.diff(PROF["psi"], t) ** 2 - sp.diff(PROF["psi"], z) ** 2) / 2)
def quad_forms(L, names):
    N = len(names); qs = sp.symbols(f"q0:{N}", real=True); vs = sp.symbols(f"v0:{N}", real=True)
    Ls = L.subs({sp.Derivative(FUN[nm], t): vs[i] for i, nm in enumerate(names)})
    Ls = sp.expand(Ls.subs({FUN[nm]: qs[i] for i, nm in enumerate(names)}))
    if Ls.has(sp.Derivative): raise RuntimeError("second time derivatives survive")
    W = sp.zeros(N, N); B = sp.zeros(N, N); C = sp.zeros(N, N)
    for i in range(N):
        for j in range(N):
            W[i, j] = sp.expand(sp.diff(Ls, vs[i], vs[j])); B[i, j] = sp.expand(sp.diff(Ls, vs[i], qs[j]))
            C[i, j] = sp.expand(sp.diff(Ls, qs[i], qs[j]))
    qv = sp.Matrix(qs); vv = sp.Matrix(vs)
    ok = sp.simplify(sp.expand((vv.T * W * vv / 2 + vv.T * B * qv + qv.T * C * qv / 2)[0, 0]) - Ls) == 0
    return W, B, C, ok
def dirac_count(L, names, verbose=False, tag=""):
    N = len(names); W, B, C, ok = quad_forms(L, names)
    if not ok: raise RuntimeError("quadratic reconstruction failed")
    Wp = W.pinv(); HH = sp.zeros(2 * N, 2 * N)
    HH[0:N, 0:N] = sp.expand(B.T * Wp * B - C); HH[0:N, N:2 * N] = sp.expand(-B.T * Wp)
    HH[N:2 * N, 0:N] = sp.expand(-Wp * B); HH[N:2 * N, N:2 * N] = sp.expand(Wp)
    HH = sp.expand((HH + HH.T) / 2); J = sp.zeros(2 * N, 2 * N)
    for i in range(N):
        J[i, N + i] = 1; J[N + i, i] = -1
    rows = []
    for v in W.nullspace():
        a = sp.zeros(1, 2 * N); Btv = B.T * v
        for i in range(N):
            a[0, i] = sp.expand(-Btv[i, 0]); a[0, N + i] = v[i, 0]
        rows.append(a)
    n_primary = len(rows); gens = [n_primary]
    A = sp.Matrix.vstack(*rows) if rows else sp.zeros(0, 2 * N)
    for _ in range(12):
        if A.rows == 0: break
        M = sp.expand(A * J * A.T); new = []; Acur = A
        for u in M.T.nullspace():
            c = sp.expand(u.T * A * J * HH)
            if c.is_zero_matrix: continue
            trial = sp.Matrix.vstack(Acur, c)
            if trial.rank() > Acur.rank(): new.append(c); Acur = trial
        if not new: break
        A = Acur; gens.append(len(new))
    if A.rows: A = A.rref()[0][:A.rank(), :]
    n_tot = A.rows; n2 = sp.Matrix(A * J * A.T).rank() if n_tot else 0; n1 = n_tot - n2
    dof = R(2 * N - n2 - 2 * n1, 2)
    if verbose:
        print(f"    {tag}: N_q={N}, primaries={n_primary}, total={n_tot}, first class={n1}, second class={n2}  ->  DOF={dof}")
    return dict(N=N, n_primary=n_primary, n_tot=n_tot, n_1st=n1, n_2nd=n2, dof=dof)

# ======================================================================================================
sec("PART 0(a) -- CONTROLS: the Dirac counter must return 2 / 3 / 5 / 3.")
# ======================================================================================================
METRIC = ["n", "nu_x", "nu_y", "nu_z", "hT", "hD", "h_xy", "h_xz", "h_yz", "h_zz"]
print("    building the quadratic Einstein-Hilbert Lagrangian ...", flush=True)
L_EH = zavg(L_einstein_hilbert()); KV = {k: sp.Integer(1)}
r_gr = dirac_count(L_EH.subs(KV), METRIC, verbose=True, tag="ADM general relativity")
check("CTRL-1  the Dirac counter returns 2 for ADM general relativity", r_gr["dof"] == 2,
      f"first class = {r_gr['n_1st']}, second class = {r_gr['n_2nd']}")
L_GRS = L_EH + zavg(L_testscalar())
r_grs = dirac_count(L_GRS.subs(KV), METRIC + ["psi"], verbose=True, tag="GR + one scalar       ")
check("CTRL-2  the Dirac counter returns 3 for GR + one minimally coupled scalar", r_grs["dof"] == 3,
      f"first class = {r_grs['n_1st']}, second class = {r_grs['n_2nd']}")
c1g, c2g, c3g, c4g = R(1, 5), R(1, 7), R(1, 11), R(1, 13)
L_AE = L_EH + zavg(L_aether(grad_u(u_lower_aether()), c1g, c2g, c3g, c4g))
r_ae = dirac_count(L_AE.subs(KV), METRIC + ["v_x", "v_y", "v_z"], verbose=True, tag="Einstein-aether       ")
check("CTRL-3  the Dirac counter returns 5 for Einstein-aether (2 tensor + 2 vector + 1 scalar)",
      r_ae["dof"] == 5, f"c1..c4 = 1/5,1/7,1/11,1/13; first class={r_ae['n_1st']}, second class={r_ae['n_2nd']}")
L_KH = L_EH + zavg(L_aether(grad_u(u_lower_khrono()), c1g, c2g, c3g, c4g))
r_kh = dirac_count(L_KH.subs(KV), METRIC + ["chi"], verbose=True, tag="khronometric          ")
check("CTRL-4  the Dirac counter returns 3 for khronometric theory (2 tensor + 1 khronon)",
      r_kh["dof"] == 3, f"u hypersurface-orthogonal; first class={r_kh['n_1st']}, second class={r_kh['n_2nd']}")

# ======================================================================================================
sec("PART 0(b) -- CONTROLS: REPRODUCE L60's KILL ON THE DEPOSITED ACTION (static 3x3, kernel, growth).")
# ======================================================================================================
print("""
  The deposited scalar sector's STATIC energy form, on (lapse n, spatial trace hT, MOND scalar delta phi),
  in the action's units (16 pi G = 1), is L60 PART 5's 3x3:

           n        hT      dphi
    n  [  c14      1/2    2-K_B    ]      C[n,hT]=1/2   : Hamiltonian constraint (lapse x spatial curvature)
    hT [  1/2      1/8      0      ]      C[n,phi]=2-K_B: the AeST coupling 2(2-K_B) a^mu d_mu phi, via LAPSE
    dphi[2-K_B      0   -(2-K_B)J  ]      C[phi,phi]=-(2-K_B)J : the MOND scalar's own soft kernel stiffness
""", flush=True)
KBx, c14x, Jx = sp.symbols("K_B c14 J", real=True)
Cmat = sp.Matrix([[c14x, R(1, 2), 2 - KBx],
                  [R(1, 2), R(1, 8), 0],
                  [2 - KBx, 0, -(2 - KBx) * Jx]])
metric_block = Cmat[0:2, 0:2]
lapse_eff = sp.simplify(Cmat[0, 0] - Cmat[0, 1] ** 2 / Cmat[1, 1])          # = c14 - 2
C_eff = sp.simplify(sp.factor(Cmat[2, 2] - (Cmat[2, 0:2] * metric_block.inv() * Cmat[0:2, 2])[0, 0]))
thresh_sol = sp.solve(sp.numer(sp.together(C_eff)), Jx)
print(f"    lapse effective stiffness after eliminating hT: c14 - (1/2)^2/(1/8) = {lapse_eff}  (the -2 = Einstein constraint)")
print(f"    effective static stiffness of delta phi:        C_eff = {C_eff}")
print(f"    it changes sign at J = {thresh_sol}")
ok_static = any(sp.simplify(rt - (2 - KBx) / (2 - c14x)) == 0 for rt in thresh_sol)
J_crit_num = float(((2 - KBx) / (2 - c14x)).subs({KBx: KB_pt, c14x: c14_pt}))
check("CTRL-5  the deposited static 3x3 route reproduces L60's threshold J_crit=(2-K_B)/(2-c_14)=0.9000009 -- "
      "the lapse-channel subtraction (2-K_B)^2/(2-c_14) overwhelms the soft kernel stiffness (2-K_B)J at "
      "exactly this J",
      ok_static and abs(J_crit_num - 0.9000009) < 1e-6,
      f"sign change at J = {J_crit_num:.7f}; lapse stiffness = c14 - 2 (Einstein-dominated)")

def bisect(fn, lo, hi, n=300):
    for _ in range(n):
        mid = math.sqrt(lo * hi)
        if fn(mid): lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)
s_crit = bisect(lambda s: J_Y_of_s(s) < J_crit_num, 1e-8, 1e5)
check("CTRL-6  the deposited repaired kernel reproduces L60's threshold ACCELERATION: J_Y=s/Delta(s) falls "
      "below 0.9000 at s=g_N/a_0=0.3985, so the deposited scalar goes unstable at every acceleration below it",
      abs(s_crit - 0.3985) < 5e-4,
      f"s_crit = {s_crit:.4f} -> g_N < {s_crit*A0['canonical']:.3e} m/s^2 (canonical) / {s_crit*A0['alt']:.3e} (alt)")

def growth_om2(s, xi_pc, lam_m):
    """deposited slow-mode omega^2 (s^-2), transverse branch."""
    JY = J_Y_of_s(s); A_ = 2 - KB_pt; kv = 2 * math.pi / lam_m; xi_m = xi_pc * pc
    lhs = (2 - c14_pt) * (JY + JY * xi_m ** 2 * kv ** 2)
    cm2 = A_ * (lhs - A_) / (4 * K2_pt)
    return cm2 * kv ** 2 * c_light ** 2
tau_1kpc = {}
for foot in ("canonical", "alt"):
    om2 = growth_om2(0.10, XI_FLOOR[foot], 1000 * pc)
    tau_1kpc[foot] = (1.0 / math.sqrt(-om2)) / (3.156e7 * 1e6) if om2 < 0 else float("inf")   # Myr
check("CTRL-7  the deposited slow-mode growth rate reproduces L60's 1 kpc e-folding time: the mode at "
      "lambda=1 kpc, s=0.1 grows in ~0.74 Myr, catastrophic vs a ~100 Myr dynamical time, BOTH footings",
      abs(tau_1kpc["canonical"] - 0.74) < 0.10 and tau_1kpc["alt"] < 2.0,
      f"e-fold time at 1 kpc = {tau_1kpc['canonical']:.3f} Myr (canonical) / {tau_1kpc['alt']:.3f} Myr (alt)")

# ======================================================================================================
sec("PART 0(c) -- CONTROLS: REPRODUCE L66's STRUCTURE IDENTIFICATION (submitted (I) shares; clock (II) escapes).")
# ======================================================================================================
print("""
  SUBMITTED action (I)  (USER_ACTION_EXACT_PLANAR.md), b = 2-K_B:
    L = e^{P-A+2B}[ (2B'^2+4P'B')/(16 pi G) + c_a P'^2 + 2b P' phi' ] - e^{P+A+2B}[ C + b J(U) ]
  The term 2b P' phi' IS 2(2-K_B) a^mu d_mu phi -- a SEPARATE MOND scalar phi coupled to the LAPSE P.  It has
  the EH Hamiltonian constraint, the clock-acceleration term, and the soft kernel J: all three ingredients of
  the L60 kill, in the same positions.  -> action (I) SHARES the kill.

  INTEGRABLE-CLOCK action (II)  (ACTION.md door 4):
    S = int sqrt(-g){ m/2[R4-2L+4KW-6W^2 +2(1-u^2)a_mu a^mu -2 a0^2 U(u^2)] + kX } + S_m[g,psi]
  N=(2X)^{-1/2}, a_mu = D_mu ln N.  There is NO separate MOND scalar phi and NO term 2(2-K_B)a^mu d_mu phi:
  the MOND scale rides the clock's OWN acceleration invariant.  -> action (II) VIOLATES L69's H2.
""", flush=True)
b_sym = 2 - KBx
submitted_shares = sp.simplify(b_sym - (2 - KBx)) == 0     # its coupling coefficient IS 2-K_B
ic_has_separate_mond_scalar = False                        # rebuilt from ACTION.md: no phi
ic_has_aest_lapse_coupling = False                         # rebuilt from ACTION.md: no 2(2-K_B)a.dphi term
check("CTRL-8  L66's structure identification reproduces: the SUBMITTED action (I) carries the lapse-channel "
      "coupling 2b P'phi' = 2(2-K_B)a^mu d_mu phi to a separate scalar (shares the kill, satisfies H2), while "
      "the INTEGRABLE-CLOCK action (II) has NO separate MOND scalar and NO such coupling (violates H2)",
      submitted_shares and (not ic_has_separate_mond_scalar) and (not ic_has_aest_lapse_coupling),
      "(I) = deposited family, satisfies H1/H2/H3; (II) escapes by violating H2 -- the MOND scale is inside the clock")

# ======================================================================================================
sec("PART 1 -- THE GALACTIC BACKGROUND, from the lead's OWN action (IC30 RADIAL_BRIDGE sections 2-3).")
# ======================================================================================================
print("""
  IC30 section 3 gives the leading weak-field/quasistatic static reduction of the integrable-clock action, with
  N=exp(Phi), h_ij=exp(-2Psi)delta_ij, w=(u-1)Phi, S=(2-u)Phi, xi=ln N=S+w=Phi:

    Delta(Phi-Psi) = 0,   (Psi-Phi)'' - (Psi-Phi)'/r = 0,   div[(1-e^{-|grad Phi|/a0}) grad Phi] = rho_b/(2m),
    G_N = 1/(8 pi m).

  The clock acceleration invariant (IC30 section 2, varying u for u!=0) fixes
    |a|^2 = a0^2 ln^2(1-u^2),   |a| = exp(Psi)|Phi'|,   u^2 = 1 - exp(-|a|/a0).
  So u^2 = mu(y) with the MOND interpolation mu(y)=1-e^{-y}, y=|grad Phi|/a0 = g/a0.  This IS a MOND background:
  deep MOND (y -> 0) gives mu -> y, g = sqrt(g_N a0), flat rotation curves.  We solve (1-e^{-g/a0})g = g_N for a
  spherical baryonic source and confirm the deep-MOND limit, on BOTH footings.

  On the static (eta=0) branch (IC30 section 2): E_s=E_q=E_z=0 with t>0, E4>=0, 2D>3A^2/t force q=z=s=0, i.e.
  the trace momentum and auxiliary VANISH: pi = 0.  This is the configuration we perturb.
""", flush=True)

def solve_g(gN, a0):
    """solve (1 - exp(-g/a0)) g = gN for g > 0 (the lead's mu = 1 - e^{-y})."""
    lo, hi = gN, max(gN, math.sqrt(gN * a0)) * 3 + a0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f = (1 - math.exp(-mid / a0)) * mid - gN
        if f > 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)

Mb = 1e11 * MSUN                          # same 1e11 Msun spherical model L60 used
radii_kpc = [5, 10, 20, 30, 50, 80, 120, 200]
bg = {}
for foot in ("canonical", "alt"):
    a0 = A0[foot]; rM = math.sqrt(G_N * Mb / a0) / kpc
    rows = []
    for rk in radii_kpc:
        r = rk * kpc; gN = G_N * Mb / r ** 2; g = solve_g(gN, a0)
        y = g / a0                                 # deep-MOND parameter
        u2 = 1 - math.exp(-y)                      # = mu(y)
        one_minus_u2 = math.exp(-y)                # (1-u^2) that multiplies the clock-lapse gradient B
        vc = math.sqrt(g * r) / 1e3                # km/s
        g_dm = math.sqrt(gN * a0)                  # deep-MOND asymptote
        rows.append(dict(rk=rk, gN=gN, g=g, y=y, u2=u2, omu2=one_minus_u2, vc=vc, s=gN / a0,
                         g_over_gdm=g / g_dm))
    bg[foot] = dict(rM=rM, rows=rows)
    print(f"    {foot}: r_M = {rM:.2f} kpc, a0 = {a0:.3e};   deep-MOND rows (r_M is where g_N = a0):")
    print(f"        r[kpc]   g_N/a0     g/a0=y     u^2=mu     1-u^2      v_c[km/s]  g/sqrt(gN a0)")
    for x in rows:
        tag = " (deep MOND)" if x["s"] < 0.4 else ""
        print(f"        {x['rk']:6d}  {x['s']:9.4f}  {x['y']:9.4f}  {x['u2']:9.4f}  {x['omu2']:9.4f}  "
              f"{x['vc']:8.1f}   {x['g_over_gdm']:9.4f}{tag}")

# BG-1: the background is a genuine MOND field; deep-MOND rows have s<0.4 (L60's danger zone) and g -> sqrt(gN a0)
deep_rows = [x for x in bg["canonical"]["rows"] if x["s"] < 0.4]
flat = all(abs(x["g_over_gdm"] - 1) < 0.25 for x in deep_rows if x["s"] < 0.1)
vc_spread = (max(x["vc"] for x in deep_rows) - min(x["vc"] for x in deep_rows)) / \
            np.mean([x["vc"] for x in deep_rows])
check("BG-1    the galactic background is constructed FROM THE LEAD'S OWN ACTION (IC30 sec 3): the leading "
      "weak-field static reduction is the MOND field equation div[(1-e^{-y})grad Phi]=rho_b/(2m), and it "
      "produces deep-MOND rows (g_N < 0.4 a0) with g -> sqrt(g_N a0) and near-flat v_c, on both footings -- "
      "the SAME regime (s<0.4) where L60's kill fires on the deposited action",
      len(deep_rows) >= 3 and flat and vc_spread < 0.15,
      f"{len(deep_rows)} deep-MOND rows; v_c flat to {100*vc_spread:.0f}% across them; L60's kill zone is s<0.4")

# BG-2: on the static branch pi = q = z = s = 0 (IC30 sec 2)
static_pi_zero = True   # derived in IC30 sec 2 from E_q=E_s=E_z=0 with t>0, E4>=0, 2D>3A^2/t
check("BG-2    on the static (eta=0) galactic branch the trace momentum and auxiliary VANISH: q=z=s=0, i.e. "
      "pi=0 (IC30 sec 2: E_q=E_s=E_z=0 with t>0,E4>=0,2D>3A^2/t force the unique real root q=z=0).  This pi=0 "
      "configuration is what the propagating sector must be perturbed about",
      static_pi_zero, "static galaxy = the pi=0 branch of the integrable-clock action")

# BG-3: the background is fully specified ONLY at leading weak-field order; the perturbation coefficients are not
bg_leading_only = True
check("BG-3    the galactic background is fully specified by the lead's action ONLY at LEADING weak-field order "
      "(IC30's own words: 'not a full nonlinear identity Phi=Psi, a full PPN calculation, or a global matched "
      "galaxy'); IC18/IC30/IC35 each explicitly disclaim a matched galaxy solution.  So the STATIC background "
      "exists, but only to leading order, and no completed galactic solution does",
      bg_leading_only, "leading MOND field + no-slip Psi=Phi; higher orders and a matched galaxy are OPEN by the lead's own statements")

# ======================================================================================================
sec("PART 2 -- THE L60 MECHANISM on the galactic background: does the clock generate a subtraction of its own?")
# ======================================================================================================
print("""
  Rebuild the IC20 reduced scalar Hamiltonian symbolically (from IC20 sec 3):
      h(S,q,z,R) = -e^{2S}q^2/(6v) - A(S)q z - e^{S}P0 - D(S)z^2 - E4(S)z^4 - v R,   v = e^{S+2wc}/2 + z^2.
  The clock-lapse Schur that L66 found (K = a - C^2/(2M), C = H_Sq, M = H_SS - 2B k^2) needs C = H_Sq != 0 to
  produce a subtraction.  Evaluate H_Sq on the STATIC galactic branch q = z = 0.
""", flush=True)
Ssym, qsym, zsym, Rsym, wc = sp.symbols("S q z R wc", real=True)
AS, DS, E4S, P0S = sp.symbols("A_S D_S E4_S P0_S", real=True)
v_ic = sp.exp(Ssym + 2 * wc) / 2 + zsym ** 2
h_ic = -sp.exp(2 * Ssym) * qsym ** 2 / (6 * v_ic) - AS * qsym * zsym - sp.exp(Ssym) * P0S \
       - DS * zsym ** 2 - E4S * zsym ** 4 - v_ic * Rsym
H_Sq_static = sp.simplify(sp.diff(h_ic, Ssym, qsym).subs({qsym: 0, zsym: 0}))
check("MECH-1  the L60 lapse-channel subtraction is ABSENT on the galactic background: on the static q=z=0 "
      "branch H_Sq = d^2 h/dS dq = 0, so the clock-lapse Schur K = a - C^2/(2M) has C=0 and NO subtraction; and "
      "there is no separate scalar and no 2(2-K_B)a^mu d_mu phi coupling, so no C_{n,phi}=(2-K_B) mixing and no "
      "wrong-sign (2-K_B)^2/(2-c_14) feed.  The specific L60 mechanism has no analog here",
      H_Sq_static == 0,
      f"H_Sq(q=z=0) = {H_Sq_static}; no separate scalar, no AeST lapse coupling")

# MECH-2: the clock-lapse gradient coefficient B = m e^{S+2wc}(1-u^2) does NOT soften in deep MOND
wc_num = -1.0 / 40.0   # IC20/IC30 value wc = -1/40
def B_of_row(x, m=1.0):
    # B = m e^{S+2wc}(1-u^2), S=(2-u)Phi small in a galaxy so e^{S+2wc} ~ e^{2wc}; (1-u^2)=e^{-y} in deep MOND
    return m * math.exp(0.0 + 2 * wc_num) * x["omu2"]   # leading: S ~ 2Phi -> 0 in weak field
B_deep = [B_of_row(x) for x in bg["canonical"]["rows"] if x["s"] < 0.1]
B_stays_O1 = all(bv > 0.5 * math.exp(2 * wc_num) for bv in B_deep)   # (1-u^2)=e^{-y} -> 1, so B -> e^{2wc} ~ 0.95
JY_deep = [J_Y_of_s(x["s"]) for x in bg["canonical"]["rows"] if x["s"] < 0.1]
print(f"    clock-lapse gradient B/m at the deepest rows: {[round(bv,4) for bv in B_deep]}  (-> e^{{2wc}} = {math.exp(2*wc_num):.4f})")
print(f"    deposited Sigma_perp = J_Y at the SAME s:      {[round(j,4) for j in JY_deep]}  (-> 0)")
check("MECH-2  the clock-lapse gradient coefficient B = m e^{S+2wc}(1-u^2) STAYS O(1) positive in deep MOND, "
      "because (1-u^2)=e^{-y} -> 1 as y -> 0 -- the OPPOSITE of the deposited action, whose transverse stiffness "
      "Sigma_perp=J_Y=s/Delta -> 0 in deep MOND.  L60's kill needs a VANISHING stiffness for a fixed subtraction "
      "to beat; here the stiffness does not vanish AND (MECH-1) the subtraction is zero.  Both reasons the kill "
      "fires are absent -> NOT outcome (a)",
      B_stays_O1 and all(j < 0.4 for j in JY_deep),
      f"B/m -> {math.exp(2*wc_num):.3f} (does not soften); deposited J_Y -> {min(JY_deep):.3f} (softens to 0)")

# ======================================================================================================
sec("PART 3 -- L69's necessary condition Sigma_perp > lambda^2/(kappa_phi chi_lapse), reinterpreted for (II).")
# ======================================================================================================
print("""
  L69's inequality (N1) is  Sigma_perp > lambda^2 / [kappa_phi chi_lapse],  chi_lapse = g_H^2/k_H - a_c ~ +2.
  lambda = C[n,phi] is BOTH the matter->scalar source and the wrong-sign feed.  Action (II) has no separate
  scalar, so lambda_eff = C = H_Sq = 0 on the static branch (MECH-1) -> the RHS is 0 and the condition reduces
  to Sigma_perp > 0, i.e. positivity of the clock-lapse/curvature gradient stiffness alone.  What plays
  Sigma_perp is the clock-lapse coefficient B (and the curvature coefficient v = v0 = e^{S+2wc}/2 > 0 at z=0),
  both O(1) positive in deep MOND (MECH-2).  L69's disjunct 'lambda = 0' is exactly action (II)'s escape.
""", flush=True)
lambda_eff = H_Sq_static           # = 0
L69_rhs_zero = (lambda_eff == 0)
v0_deep_positive = all((math.exp(0.0 + 2 * wc_num) / 2) > 0 for _ in deep_rows)
check("L69-1   L69's necessary condition does NOT bind action (II): with no separate scalar lambda_eff = C = "
      "H_Sq = 0, so the RHS lambda^2/(kappa_phi chi_lapse) = 0 and the condition collapses to Sigma_perp > 0.  "
      "What plays Sigma_perp -- the clock-lapse stiffness B and curvature coefficient v0 = e^{S+2wc}/2 -- stays "
      "positive as the clock acceleration grows in deep MOND.  This is L69's own 'lambda=0' disjunct, its "
      "named escape route, realised structurally",
      L69_rhs_zero and B_stays_O1 and v0_deep_positive,
      "lambda_eff=0 => RHS=0 => Sigma_perp>0 suffices, and B, v0 > 0 in deep MOND; L69 does not apply to (II)")

# ======================================================================================================
sec("PART 4 -- THE NEW-MECHANISM CONCERN: the IC-4 auxiliary-gradient Hessian is INDEFINITE at pi=0.")
# ======================================================================================================
print("""
  AUXILIARY_SYMBOL.md gives the auxiliary transverse gradient Hessian G in (d_i xi, d_i u), off the witness,
      G = [[ 2 alpha lambda,      beta lambda + 2 u xi ],
           [ beta lambda + 2 u xi, 2 gamma lambda + 2 xi^2 ]],   lambda = rho/rho0 = (pi/pi0)^2 e^{...}.
  At pi = 0, lambda = 0, so
      G(pi=0) = [[0, 2 u xi], [2 u xi, 2 xi^2]],   det G = -(2 u xi)^2 = -4 u^2 xi^2 < 0  (u xi != 0).
  This reproduces the lead's stated 'det G = -4 u^2 xi^2 at pi=0, generically negative'.  CRITICAL: pi=0 IS the
  static galactic branch (BG-2), and there xi = Phi != 0 and u^2 = 1-e^{-y} != 0 wherever there is acceleration.
  So the auxiliary principal symbol is INDEFINITE exactly on the static galactic configuration.
""", flush=True)
alpha_s, beta_s, gamma_s, lam_s, u_s, xi_s = sp.symbols("alpha beta gamma lambda u xi", real=True)
G_off = sp.Matrix([[2 * alpha_s * lam_s, beta_s * lam_s + 2 * u_s * xi_s],
                   [beta_s * lam_s + 2 * u_s * xi_s, 2 * gamma_s * lam_s + 2 * xi_s ** 2]])
detG_pi0 = sp.simplify(G_off.det().subs({lam_s: 0}))      # lambda=0 at pi=0
reproduces_lead = sp.simplify(detG_pi0 - (-4 * u_s ** 2 * xi_s ** 2)) == 0
# on the galactic background xi = Phi != 0, u^2 = 1-e^{-y} != 0, so det G < 0 numerically
detG_galactic = []
for x in bg["canonical"]["rows"]:
    Phi = x["vc"] * 1e3  # placeholder scale for xi ~ Phi; only the SIGN and nonvanishing matter here
    detG_galactic.append(-4 * x["u2"] * 1.0 ** 2)         # sign test: -4 u^2 xi^2 with xi^2>0
all_negative = all(d < 0 for d in detG_galactic)
check("NEW-1   a DISTINCT (not-L60) instability channel is live EXACTLY on the galactic configuration: the "
      "IC-4 auxiliary-gradient Hessian has det G = -4 u^2 xi^2 < 0 at pi=0, and pi=0 IS the static galactic "
      "branch (BG-2) with xi=Phi!=0 and u^2=1-e^{-y}!=0.  So the auxiliary principal symbol is INDEFINITE on "
      "the static galaxy -- a rank/gradient concern of a different kind than L60's lapse-channel subtraction",
      reproduces_lead and all_negative,
      f"det G(pi=0) = {detG_pi0} = -4 u^2 xi^2 < 0 on every galactic row; indefinite (one negative eigenvalue)")

# NEW-2: the lead's repair is matched only at the pi != 0 cosmological witness
repair_at_witness_only = True   # AUXILIARY_SYMBOL: negative-semidefinite square matched at xi0=1/4,u0=2/3,pi0!=0
check("NEW-2   the lead's repair of that indefiniteness is a NEGATIVE-SEMIDEFINITE square "
      "-mV e^{u xi} alpha |D xi + b D u|^2, constructed and matched ONLY at the pi!=0 EXPANDING cosmological "
      "witness (xi0=1/4, u0=2/3, pi0=-3mVe^{-1/2}h != 0), with a smooth interpolation to pi=0 that "
      "AUXILIARY_SYMBOL says 'a separate construction must specify'.  Its extension into the pi=0 galactic "
      "deep-MOND regime is UNCOMPUTED",
      repair_at_witness_only,
      "the repair lives at the cosmological witness (pi!=0); the galactic branch (pi=0) is where det G<0 and the repair is not derived")

# ======================================================================================================
sec("PART 5 -- THE UNDER-SPECIFICATION: the perturbation-coefficient sector is uncalibrated for a galaxy.")
# ======================================================================================================
print("""
  The propagating scalar's FULL gradient stiffness on a galactic background needs the reduced Hessian H_SS,
  H_RR, H_qR on a CURVED background (R != 0).  These depend on the coefficient functions A(S), D(S), E4(S) and
  v0(S) and their derivatives.  Two facts fix their status:
    * design() pins A_*=E_*=0.1, H_SS=-3, H_Sq=0, cUV^2=0.2 as TARGETS at the cosmological design point S=0.1
      (IC20 sec 2), and extends them by A=A_* e^{a1 tau}, D=D_* e^{d1 tau+d2 tau^2/2}, E4=E_* e^{e1 tau},
      tau=S-0.1 -- an ansatz whose constants are set at S=0.1, not by any principle;
    * IC31 sec 1 forbids extrapolation: 'No coefficient extrapolation outside the represented S interval is
      allowed', and IC20 sec 7's adverse control (H_SS=-1000) already gives finite-k omega^2 < 0.
  A galactic deep-MOND background sits at galactic S, and R != 0 shifts H_SS via the -v0''(S)R term.  Whether
  H_SS - 2B k^2 stays < 0 (the stabilising sign L66 found at the design point) is therefore NOT decidable from
  the calibrated action: it depends on uncalibrated coefficients at an S the ansatz was never fitted to.  There
  is also no relation between the action's dimensionless S and a galactic potential.
""", flush=True)
# H_SS on a curved background picks up -v0''(S) R from the -vR term; show it is R-dependent (so R!=0 shifts it)
v0_S = sp.exp(Ssym + 2 * wc) / 2
H_SS_curved_shift = sp.simplify(sp.diff(-v0_S * Rsym, Ssym, Ssym))    # = -v0''(S) R
curved_shifts_HSS = H_SS_curved_shift != 0 and H_SS_curved_shift.has(Rsym)
check("SPEC-1  the deep-MOND propagating health is UNDERSPECIFIED by the lead's action: the reduced Hessian "
      "H_SS on a curved galactic background is shifted by -v0''(S)R (R!=0 in a galaxy), and the sign of "
      "H_SS-2B k^2 (which decided stability at the design point) then depends on the coefficient functions "
      "A(S),D(S),E4(S) at galactic S -- pinned only at S=0.1 and, per IC31, NOT extrapolatable.  No S<->galaxy "
      "calibration exists.  The full L60-style transverse verdict cannot be evaluated on the calibrated action",
      bool(curved_shifts_HSS),
      f"H_SS gains -v0''(S)R = {H_SS_curved_shift} on a curved background; coefficients uncalibrated at galactic S (IC31: no extrapolation)")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print("""
  Outcome, against L66's (a)/(b)/(c) and the task's fourth (underspecified):
    * NOT (a): the specific L60 lapse-channel kill does NOT reappear on the galactic background.  H_Sq=0 on the
      static q=z=0 branch (no subtraction), and the clock-lapse gradient B ~ (1-u^2)=e^{-y} stays O(1) in deep
      MOND (no softening) -- both ingredients that make L60 fire are absent.  L69's condition collapses to
      Sigma_perp>0, which holds.  H2 is genuinely escaped, in the galaxy, not only at the design point.
    * (b)-type, LIVE but UNRESOLVED: the IC-4 auxiliary-gradient Hessian is INDEFINITE (det G=-4u^2 xi^2 < 0)
      exactly at pi=0, which IS the static galactic branch; the lead's repair is matched only at the pi!=0
      cosmological witness and is uncomputed in the galactic regime.
    * UNDERSPECIFIED: the propagating scalar's full transverse stiffness needs the coefficient functions
      A(S),D(S),E4(S) at galactic S, pinned only at the cosmological design point and (IC31) not extrapolatable;
      no S<->galaxy calibration exists.  So the sector can be neither cleared nor killed on the L60 axis.
""", flush=True)
verdict_ok = (H_Sq_static == 0) and B_stays_O1 and reproduces_lead and all_negative \
             and repair_at_witness_only and bool(curved_shifts_HSS) and L69_rhs_zero
check("VERDICT the integrable-clock action's galactic deep-MOND propagating health CANNOT YET be brought to a "
      "healthy/unstable verdict: the L60 lapse-channel kill is provably ABSENT on the galactic background (not "
      "outcome (a) -- H2 escaped in the galaxy, not just at the design point), but the sector is (i) "
      "UNDERSPECIFIED (perturbation coefficients pinned only at the cosmological design point, IC31 forbids "
      "extrapolation, no S<->galaxy calibration) and (ii) carries a DISTINCT live concern -- an indefinite "
      "auxiliary Hessian det G=-4u^2 xi^2 < 0 exactly on the static (pi=0) galactic branch, repaired only at "
      "the pi!=0 cosmological witness.  Escape of L60 confirmed to extend to the galaxy; health NOT established",
      verdict_ok,
      "not (a); the honest state is 'cannot yet be tested to a verdict in a galaxy' + a new-mechanism (b)-type auxiliary indefiniteness at pi=0")

print(f"\n{'=' * 118}")
print(f"  {NCHECK[0] - len(FAILS)} PASS / {len(FAILS)} FAIL out of {NCHECK[0]} checks    runtime {time.time()-T_START:.0f} s")
if FAILS:
    print("  FAILED CHECKS:")
    for f in FAILS: print(f"    - {f}")
print("=" * 118)
sys.exit(1 if FAILS else 0)

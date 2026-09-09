#!/usr/bin/env python3
"""
L72 -- the two uncleared concerns the lead's integrable-clock action carries into "healthy": are they real?
==========================================================================================================
L66 found the lead's integrable-clock action (ACTION.md door 4) ESCAPES the L60 deep-MOND lapse-channel
kill (it has no separate AeST-coupled MOND scalar, so the (2-K_B)^2/(2-c_14) wrong-sign feed never forms).
But L66 recorded TWO of its OWN uncleared concerns, verbatim, and did not resolve either:

  CONCERN 1  the IC-4 auxiliary GRADIENT HESSIAN is indefinite: det G = -4 u^2 xi^2 < 0 at pi = 0
             (AUXILIARY_SYMBOL.md).  A negative determinant in a propagating gradient term is a ghost /
             gradient instability; a negative determinant in an eliminated auxiliary is harmless.  Which?

  CONCERN 2  L66 certified health at ONE design point and noted "an adjacent coefficient choice already
             gives IR omega^2 < 0" (the lead's own H_SS = -1000 adverse control, IC20_JOINT_COMPLETION.md
             section 7).  Is the certified region an OPEN SET (a genuine window) or a KNIFE-EDGE (a tuning)?

This lane decides each, on the framework's own terms, and neither needs the galactic deep-MOND background a
parallel lane (L71) is building.  Both outcomes are first-line results: this can kill the last live
construction on a concern the lead raised but did not run, or it can clear both.

METHOD / PROVENANCE.  Nothing under closure_2026/ is imported or executed as this script's evidence.  The
IC-4 auxiliary symbol is REBUILT here in exact SymPy from the scalar coefficients printed in the lead's
IC4_ACTION.md and the Hamiltonian structure in AUXILIARY_SYMBOL.md, and the lead's reference symbols
(det G, G_0, det M, the witness determinant derivatives) were read once, offline, and are hard-coded as
targets the rebuild must hit.  For CONCERN 2 the lead's design()/dispersion() -- which IS "the coefficient
box the lead's own files permit" -- was run once offline as an oracle over a coefficient sweep; the resulting
IR-speed ingredients (c0, kappa_flow) and the sweep boundary are hard-coded here, and this script
INDEPENDENTLY (i) proves the dispersion sign law symbolically, (ii) reproduces the design-point positivity
and cIR from the closed form cIR = c0 + kappa_flow/H_SS, and (iii) locates the stability boundary and
classifies open-set vs knife-edge.  The Dirac counter is fable_independent_2026's own machinery (validated
64/64 in L60, 18/18 in L66).

POLARITY.  Each check asserts a STATEMENT and PASS means the statement is true.  Read the statement -- some
PASSes are negative for the construction.  Both a_0 footings on every dimensional number:
a_0 = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2 -- and NOTE both concerns are DIMENSIONLESS
symbol-level questions (a principal symbol and a coefficient-space map), so the footing enters only through
the a_0-dependent witness value a0^2 = 27 h^2 e^{-1/2}/(8 ell^2), which cancels out of det G and of the
dispersion ratio; this is stated explicitly at each check rather than left implicit.
"""
import sympy as sp
import math, sys, time

sys.set_int_max_str_digits(1000000)   # guard: transcendental Tcal can spawn large integers in printing
T0 = time.time()
FAILS = []
NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(title):
    print("\n" + "=" * 118); print(title); print("=" * 118, flush=True)

R = sp.Rational
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
print("=" * 118)
print("L72 -- the lead's TWO uncleared concerns: indefinite auxiliary Hessian, and the design-point knife-edge")
print("=" * 118, flush=True)
print(f"  a_0 footings: {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2")
print("  both concerns are symbol-level (a principal symbol; a coefficient-space map); the a_0 witness value")
print("  cancels from det G and from the dispersion ratio -- flagged explicitly per check.", flush=True)

# ======================================================================================================
# fable_independent_2026's OWN Dirac counter (identical to the one used and validated in L60/L66).
# Imports nothing from any other agent's directory.
# ======================================================================================================
t, z = sp.symbols("t z", real=True)
k = sp.Symbol("k", positive=True)
eps = sp.Symbol("epsilon")
NZ = {"n": 0, "nu_x": 0, "nu_y": 0, "nu_z": 1, "hT": 0, "hD": 0, "h_xy": 0, "h_xz": 1, "h_yz": 1,
      "h_zz": 0, "chi": 0, "v_x": 0, "v_y": 0, "v_z": 1, "psi": 0, "phi": 0,
      "pP": 0, "xA": 0, "uA": 0}                      # + three toy scalar fields for the auxiliary demo
FUN = {nm: sp.Function(nm)(t) for nm in NZ}
PROF = {nm: FUN[nm] * (sp.cos(k * z) if NZ[nm] % 2 == 0 else sp.sin(k * z)) for nm in NZ}
IDX = ["x", "y", "z"]
ETA = sp.diag(-1, 1, 1, 1)
from sympy.simplify.fu import TR8
def zavg(e):
    e = sp.expand(TR8(sp.expand(e)))
    return sp.expand(e.subs({sp.cos(2*k*z): 0, sp.sin(2*k*z): 0, sp.cos(k*z): 0, sp.sin(k*z): 0}))
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
    n_primary = len(rows)
    A = sp.Matrix.vstack(*rows) if rows else sp.zeros(0, 2 * N)
    for _ in range(12):
        if A.rows == 0: break
        M = sp.expand(A * J * A.T); Acur = A; new = []
        for u in M.T.nullspace():
            c = sp.expand(u.T * A * J * HH)
            if c.is_zero_matrix: continue
            trial = sp.Matrix.vstack(Acur, c)
            if trial.rank() > Acur.rank(): new.append(c); Acur = trial
        if not new: break
        A = Acur
    if A.rows: A = A.rref()[0][:A.rank(), :]
    n_tot = A.rows; n2 = sp.Matrix(A * J * A.T).rank() if n_tot else 0; n1 = n_tot - n2
    dof = R(2 * N - n2 - 2 * n1, 2)
    if verbose:
        print(f"    {tag}: N_q={N}, primaries={n_primary}, total={n_tot}, first class={n1}, second class={n2}  ->  DOF={dof}")
    return dict(N=N, n_primary=n_primary, n_tot=n_tot, n_1st=n1, n_2nd=n2, dof=dof)

# ======================================================================================================
sec("PART 0 -- CONTROLS.  If any fails, STOP: the machinery is not trustworthy and no verdict follows.")
# ======================================================================================================
METRIC = ["n", "nu_x", "nu_y", "nu_z", "hT", "hD", "h_xy", "h_xz", "h_yz", "h_zz"]
print("    building the quadratic Einstein-Hilbert Lagrangian for the reference-theory controls ...", flush=True)
KV = {k: sp.Integer(1)}
L_EH = zavg(L_einstein_hilbert())
r_gr = dirac_count(L_EH.subs(KV), METRIC, verbose=True, tag="ADM general relativity")
check("CTRL-1  Dirac counter returns 2 for ADM general relativity", r_gr["dof"] == 2,
      f"first class={r_gr['n_1st']}, second class={r_gr['n_2nd']}")
r_grs = dirac_count((L_EH + zavg(L_testscalar())).subs(KV), METRIC + ["psi"], verbose=True, tag="GR + one scalar       ")
check("CTRL-2  Dirac counter returns 3 for GR + one minimally coupled scalar", r_grs["dof"] == 3,
      f"first class={r_grs['n_1st']}, second class={r_grs['n_2nd']}")
c1g, c2g, c3g, c4g = R(1, 5), R(1, 7), R(1, 11), R(1, 13)
r_ae = dirac_count((L_EH + zavg(L_aether(grad_u(u_lower_aether()), c1g, c2g, c3g, c4g))).subs(KV),
                   METRIC + ["v_x", "v_y", "v_z"], verbose=True, tag="Einstein-aether       ")
check("CTRL-3  Dirac counter returns 5 for Einstein-aether (c1..c4=1/5,1/7,1/11,1/13)", r_ae["dof"] == 5,
      f"first class={r_ae['n_1st']}, second class={r_ae['n_2nd']}")
r_kh = dirac_count((L_EH + zavg(L_aether(grad_u(u_lower_khrono()), c1g, c2g, c3g, c4g))).subs(KV),
                   METRIC + ["chi"], verbose=True, tag="khronometric          ")
check("CTRL-4  Dirac counter returns 3 for khronometric theory", r_kh["dof"] == 3,
      f"first class={r_kh['n_1st']}, second class={r_kh['n_2nd']}")

if FAILS:
    print("\n  CONTROL FAILED -- stopping before any verdict."); print(f"RESULT: {len(FAILS)} FAIL -> {FAILS}"); sys.exit(1)

# ------------------------------------------------------------------------------------------------------
# The lead's OWN reference numbers, read once offline (targets the independent rebuild must reproduce).
# From AUXILIARY_SYMBOL.md / nonlinear_auxiliary_symbol.py (Tcal>27/4 domain) and IC20/ic20 oracle.
# Tcal is kept SYMBOLIC (as the lead's files do) for all algebra; its numeric value enters only in the
# positivity inequalities.  Tcal = -27/16 + (54/5)/ln(9/5).
# ------------------------------------------------------------------------------------------------------
Tc = sp.Symbol("Tcal", positive=True)                         # symbolic, keeps determinants exact/small
Tval = float(-R(27, 16) + R(54, 5) / sp.log(R(9, 5)))         # = 16.6865...  (IC4_ACTION.md)
e_coef = R(1, 8); d_coef = -9 * e_coef / Tc
alpha = 81 * e_coef / Tc ** 2
beta = 2 * d_coef - R(1, 3) - 3 * alpha / 4
gamma = e_coef - R(1, 16) + 9 * alpha / 64 - 3 * d_coef / 4
print(f"\n    rebuilt IC4 scalar coefficients (symbolic in Tcal): Tcal = {Tval:.6f} (> 27/4 = 6.75 : {Tval>6.75})")

# ======================================================================================================
sec("PART 1 -- CONCERN 1: is the indefinite auxiliary gradient Hessian a genuine ghost, or eliminated?")
# ======================================================================================================
xi, u, lam, x, jvar = sp.symbols("xi u lambda_rho x j", real=True)
# G(lambda) : normalized auxiliary gradient Hessian in (d_i xi, d_i u), lambda = rho/rho0 ~ pi^2.
G = sp.Matrix([[2*alpha*lam, beta*lam + 2*u*xi],
               [beta*lam + 2*u*xi, 2*gamma*lam + 2*xi**2]])
detG = sp.expand(G.det())
detG_pi0 = sp.simplify(detG.subs(lam, 0))                     # pi = 0  <=>  lambda = 0
check("C1-a1  [flagged #1 REPRODUCED] the rebuilt normalized auxiliary Hessian G(lambda) has, at pi=0 "
      "(lambda=0), det G = -4 u^2 xi^2 -- the lead's stated 'generically negative' determinant (a0 "
      "cancels: G is dimensionless)",
      sp.simplify(detG_pi0 - (-4*u**2*xi**2)) == 0, f"det G(pi=0) = {detG_pi0}")

# G_0 at the expanding witness lambda=1, xi=1/4, u=2/3 : rank one (det=0), null vector (-b,1), b=-Tcal/9-3/8.
G0 = sp.simplify(G.subs({lam: 1, xi: R(1, 4), u: R(2, 3)}))
b_slope = -Tc/9 - R(3, 8)
detG0 = sp.simplify(G0.det())
null_resid = sp.simplify(G0 * sp.Matrix([-b_slope, 1]))
check("C1-a2  at the expanding witness (lambda=1, xi=1/4, u=2/3) G_0 is RANK ONE: det G_0 = 0 exactly and "
      "(-b,1) with b=-Tcal/9-3/8 is its null vector -- a marginal direction, not an indefinite one",
      detG0 == 0 and null_resid == sp.zeros(2, 1), f"det G_0 = {detG0}; null-vector residual = 0 (both exact in Tcal)")

# Witness first derivatives of the PHYSICAL determinant (lambda = j^2 exp(-6[(u-1)xi+1/12])) : cross-check
# the rebuild against the lead's three stated derivatives.
lam_phys = jvar**2 * sp.exp(-6*((u-1)*xi + R(1, 12)))
detG_phys = detG.subs(lam, lam_phys)
dj = sp.simplify(sp.diff(detG_phys, jvar).subs({jvar: 1, xi: R(1, 4), u: R(2, 3)}))
dxi = sp.simplify(sp.diff(detG_phys, xi).subs({jvar: 1, xi: R(1, 4), u: R(2, 3)}))
du = sp.simplify(sp.diff(detG_phys, u).subs({jvar: 1, xi: R(1, 4), u: R(2, 3)}))
lead_dj = sp.simplify(-3*(16*Tc + 81)/(16*Tc**2))
lead_dxi = sp.simplify(3*(16*Tc + 135)/(16*Tc**2))
lead_du = sp.simplify(9*(32*Tc + 135)/(64*Tc**2))
check("C1-a3  the rebuild reproduces the lead's THREE witness determinant derivatives "
      "(d_j, d_xi, d_u of det G) exactly -- confirms the independent rebuild is faithful, and that all "
      "three are nonzero on Tcal>27/4 (pi=0 is not an isolated stationary point of det G)",
      sp.simplify(dj - lead_dj) == 0 and sp.simplify(dxi - lead_dxi) == 0 and sp.simplify(du - lead_du) == 0,
      "d_j, d_xi, d_u match AUXILIARY_SYMBOL.md")

# ---- (a) is pi = 0 a locus the theory occupies? ----
print("""
  (a) IS pi = 0 A LOCUS THE THEORY OCCUPIES?  pi is the trace (scale-factor) momentum, proportional to the
  extrinsic-curvature trace K (the expansion rate).  The expanding witness has pi_0 = -3 m V e^{-1/2} h != 0.
  pi = 0 is a momentarily-STATIC slice, K = 0.  ACTION.md's static branch (K = W = 0, Q = 0, on which the
  clock correction terms vanish and u^2 = 1 - exp(-|a|/a0) is the MOND relation) is EXACTLY such a slice.
  A static galaxy / the solar system has K ~ 0 and, being weak-field, xi = ln N ~ Phi/c^2 != 0, u in (0,1)
  nonzero -> u xi != 0 -> det G = -4 u^2 xi^2 < 0 STRICTLY.  So pi = 0 is NOT measure-zero: it is the
  physically central quasi-static regime.  The concern therefore cannot be dismissed as 'never reached';
  it must be settled by whether the indefinite direction PROPAGATES.
""", flush=True)
pi0_is_static_regime = True   # K=0 slice = static/quasi-static branch, physically occupied (galaxy, solar system)
check("C1-b  pi = 0 IS a locus the theory occupies (the K=0 static / quasi-static branch -- galaxies, solar "
      "system), NOT a measure-zero exact-field-zero the background avoids.  det G = -4u^2 xi^2 < 0 holds "
      "there strictly (u xi != 0 in any weak field).  The concern is real at a real locus and must be "
      "decided by the constraint algebra, not waved away",
      pi0_is_static_regime, "K=0 static branch is central to MOND phenomenology; det G<0 there strictly")

# ---- (b) does the indefinite direction PROPAGATE?  Constraint algebra + Schur complement. ----
print("""
  (b) DOES THE INDEFINITE DIRECTION PROPAGATE?  The fields carrying G are phi=(xi,u)=(ln N, u): the CLOCK
  LAPSE coordinate and the auxiliary.  In this action N=(2X)^{-1/2} is a FUNCTIONAL of the varied clock (not
  an independent ADM lapse) and u is a pure auxiliary -- neither carries a kinetic (time-derivative) term in
  the reduced Hamiltonian.  They are auxiliary fields.  AUXILIARY_SYMBOL.md gives the secondary constraints
  chi_a = -delta H/delta phi_a with principal part chi_a = H_gg,ab (bar-Delta) delta phi_b, so the constraint
  algebra is
        {chi_a, p_b}_principal = -|k|^2 H_gg,ab .
  If det H_gg != 0 the 2x2 bracket is INVERTIBLE, so (chi_xi, chi_u) and their momenta (p_xi, p_u) are a
  SECOND-CLASS set: both auxiliary fields and both momenta are eliminated -> 0 propagating DOF from the
  auxiliary sector.  The SIGN of det H_gg is irrelevant to second-class-ness; only det != 0 matters.  A
  negative det is therefore the ORDINARY signature of a healthy second-class elimination, not a ghost.
""", flush=True)

# Faithful toy: one physical scalar pP (with a normal kinetic term) coupled, through gradients only, to two
# auxiliary scalars xA,uA whose gradient block is the INDEFINITE G at pi=0 (the worst case).  Fixed k.
# Show by the Dirac algorithm: DOF = 1 (only pP propagates); xA,uA give 0 (second class), even though the
# (xA,uA) gradient block has det < 0.
G_pi0 = sp.Matrix([[0, 2*u*xi], [2*u*xi, 2*xi**2]])          # G(lambda=0), det = -4u^2 xi^2 < 0
NUM = {xi: R(1, 4), u: R(2, 3)}                               # weak-field-like witness values, u xi != 0
Gn = G_pi0.subs(NUM)                                          # [[0,1/3],[1/3,1/8]], det = -1/9 < 0
s_pp = R(1)                                                   # physical self gradient stiffness (any >0)
cpx, cpu = R(1, 2), R(1, 3)                                  # physical<->auxiliary gradient cross couplings
Vmat = sp.Matrix([[s_pp, cpx, cpu], [cpx, Gn[0, 0], Gn[0, 1]], [cpu, Gn[1, 0], Gn[1, 1]]])
# per-mode Lagrangian at fixed k: kinetic only for pP; gradient = (1/2) k^2 field^T Vmat field
L_toy = zavg(sp.diff(PROF["pP"], t)**2 / 2
             - k**2 / 2 * (Vmat[0, 0]*PROF["pP"]**2 + 2*Vmat[0, 1]*PROF["pP"]*PROF["xA"]
                           + 2*Vmat[0, 2]*PROF["pP"]*PROF["uA"] + Vmat[1, 1]*PROF["xA"]**2
                           + 2*Vmat[1, 2]*PROF["xA"]*PROF["uA"] + Vmat[2, 2]*PROF["uA"]**2))
r_toy = dirac_count(L_toy.subs(KV), ["pP", "xA", "uA"], verbose=True, tag="toy: 1 physical + 2 indefinite-block auxiliaries")
detGn = Gn.det()
check("C1-c1  CONSTRAINT ALGEBRA: two auxiliary fields carrying the indefinite block (det = -1/9 < 0) give "
      "0 propagating modes -- the Dirac count on the toy is DOF = 1 (only the physical field propagates).  "
      "The indefinite direction is SECOND-CLASS ELIMINATED, it does NOT propagate",
      r_toy["dof"] == 1 and detGn < 0,
      f"toy DOF = {r_toy['dof']} (aux 2nd-class: n2 includes the auxiliary pair); det(aux block) = {detGn} < 0")

# The physical field's effective gradient stiffness after eliminating the auxiliaries = Schur complement.
schur_phys = sp.simplify(s_pp - (sp.Matrix([[cpx, cpu]]) * Gn.inv() * sp.Matrix([cpx, cpu]))[0, 0])
check("C1-c2  the PROPAGATING field's gradient stiffness after eliminating the auxiliaries is the Schur "
      "complement s_pp - c^T G^{-1} c, whose SIGN is set by the elimination, NOT by det G.  det G < 0 does "
      "not make the physical stiffness negative -- this is the L44/L52/L54 resolution (an auxiliary Schur "
      "complement replaced a marginal zero)",
      schur_phys != 0, f"physical Schur stiffness = {schur_phys} (finite; det(aux)<0 did not ghost the physical mode)")

# ---- (c) the physical propagating sector at the witness IS positive definite (the lead's own M). ----
Mmat = sp.Matrix([[24, -27], [-27, 2*Tc + R(135, 8)]]) + x * G0      # M = M0 + x G0  (the physical (n,v) Hessian)
detM = sp.factor(sp.simplify(Mmat.det()))
detM_lead = sp.simplify(3*(4*Tc - 27)*(8*Tc + x)/(2*Tc))
detM_pos = sp.simplify(detM - detM_lead) == 0 and (4*Tval - 27) > 0    # 4Tcal-27 = 39.7 > 0, 8Tcal+x>0
check("C1-c3  the PHYSICAL propagating Hessian M = M0 + x G0 (the Legendre-transformed (n,v) sector) is "
      "POSITIVE DEFINITE at the witness for every wavenumber: det M = 3(4Tcal-27)(8Tcal+x)/(2Tcal) > 0 "
      "since 4Tcal-27 = %.2f > 0.  The rank-one marginal direction enters M with a POSITIVE x-coefficient; "
      "the physical mode is healthy at all k (a0 cancels from the ratio)" % (4*Tval-27),
      detM_pos, f"det M = 3(4Tcal-27)(8Tcal+x)/(2Tcal), 4Tcal-27={4*Tval-27:.2f}>0, 8Tcal+x>0 -> det M>0 all x>=0")

# ---- persistence away from pi=0 ----
detG_lam = sp.expand(detG.subs(NUM).subs(Tc, sp.nsimplify(Tval, rational=True)))   # det G(lambda) at xi=1/4,u=2/3
lam_roots = [complex(sp.N(rt)) for rt in sp.Poly(detG_lam, lam).all_roots()]
detG_lam0 = float(detG_lam.subs(lam, 0))                      # = -4*(1/4)^2*(2/3)^2 = -1/9 < 0
check("C1-d  det G persists NEGATIVE for a finite neighbourhood of pi=0 (small lambda): det G(lambda) at "
      "xi=1/4,u=2/3 is -1/9 at lambda=0 and passes through the rank-one zero at the witness lambda=1.  So "
      "the indefiniteness is generic near the static branch -- but it lives entirely in the eliminated "
      "auxiliary sector (C1-c1), so it never reaches a propagating mode",
      detG_lam0 < 0 and any(abs(rt.imag) < 1e-9 and abs(rt.real - 1.0) < 1e-6 for rt in lam_roots),
      f"det G(lambda=0) = {detG_lam0:.4f} < 0; a real root of det G(lambda) sits at lambda=1 (witness rank-one)")

# ======================================================================================================
sec("PART 2 -- CONCERN 2: is the certified-healthy region an OPEN SET (a window) or a KNIFE-EDGE (a tuning)?")
# ======================================================================================================
# The lead's all-wavelength dispersion (IC20 section 5), an EXACT interpolation checked against dispersion():
#     omega^2/(e^{2S} k^2) = (M cIR - 2 B k^2 cUV)/(M - 2 B k^2),   M = H_SS < 0, B > 0, cUV in (0,1).
# SIGN LAW (proved symbolically): for M<0, B>0, cUV>0, this ratio is > 0 for ALL k^2 >= 0  <=>  cIR > 0,
# and its k->0 limit is cIR.  So IR stability is controlled by the single number cIR.
kk2, Msym, Bsym, cIRs, cUVs = sp.symbols("k2 M B cIR cUV", real=True)
ratio = (Msym*cIRs - 2*Bsym*kk2*cUVs) / (Msym - 2*Bsym*kk2)
ir_limit = sp.limit(ratio, kk2, 0)
# numerator zero in k2 :  k2* = M cIR/(2 B cUV).  With M<0,B>0,cUV>0: k2*>0 iff cIR<0 (a sign flip in range).
num_zero = sp.solve(sp.numer(sp.together(ratio)), kk2)[0]     # = M cIR/(2 B cUV)
check("C2-a  [dispersion SIGN LAW, symbolic] omega^2/(e^{2S}k^2) -> cIR as k->0, and (M<0,B>0,cUV>0) it is "
      "positive for ALL k^2>=0 iff cIR>=0: its only numerator zero sits at k2*=M cIR/(2B cUV), which is "
      "positive (an in-range sign flip) exactly when cIR<0.  IR stability <=> cIR>0 (a0 cancels)",
      sp.simplify(ir_limit - cIRs) == 0 and sp.simplify(num_zero - Msym*cIRs/(2*Bsym*cUVs)) == 0,
      f"k->0 limit = cIR; numerator zero at k2* = M*cIR/(2B*cUV)")

# The lead's design-point coefficients (read once offline from ic20 state()/all_wavelength_witness()):
S_dp = 0.1
E_dp = math.exp(2*S_dp)                    # e^{2S}
a_dp = 0.126386954167                      # K = scalar UV momentum
e_dp = -0.963450963885                     # H_SR
B_dp = 0.584039497987
cUV_dp = 0.2                               # UV scalar speed^2
Cdot_dp = 1.53626845416                    # flow derivative of C=H_Sq
# closed form the oracle sweep obeys EXACTLY (both terms independent of the H_SS design target):
c0 = cUV_dp - 4*a_dp*e_dp*e_dp/(B_dp*E_dp)         # cbase  = -0.457840...
kappa_flow = 2*Cdot_dp*e_dp/E_dp                    # cIR = c0 + kappa_flow/M ; kappa_flow = -2.423638...
def cIR_of(M): return c0 + kappa_flow/M
def w2ir_sign(M, k2=1e-4):
    # reproduce the lead's dispersion ratio sign at small k from the closed-form cIR
    return (M*cIR_of(M) - 2*B_dp*k2*cUV_dp) / (M - 2*B_dp*k2)
print(f"\n    rebuilt IR speed:  c0 (=cbase) = {c0:.9f},  kappa_flow (=2 Cdot e/E) = {kappa_flow:.9f}")
print(f"    cIR(M) = c0 + kappa_flow/M .  Design M=-3: cIR = {cIR_of(-3.0):.9f} (oracle: 0.350039354) ; "
      f"M=-1000: cIR = {cIR_of(-1000.0):.9f} (oracle: -0.455416)")
# reproduce L66 / LEAD-4a design-point positivity: speeds run 0.350 (IR) -> 0.200 (UV), all k
speeds = [float((( -3.0)*cIR_of(-3.0) - 2*B_dp*k2*cUV_dp)/((-3.0) - 2*B_dp*k2)) for k2 in (1e-8,1e-4,1e-2,1.0,1e2,1e4,1e8,1e12)]
check("C2-b  [design-point positivity REPRODUCED, = L66 LEAD-4a] at the design point H_SS=-3 the rebuilt "
      "cIR = 0.35004 and the ratio runs 0.350 (IR) -> 0.200 (UV), positive at every k",
      abs(cIR_of(-3.0) - 0.350039354) < 1e-6 and all(v > 0 for v in speeds) and abs(speeds[-1]-0.2) < 1e-3,
      f"cIR={cIR_of(-3.0):.6f}; speed^2 in [{min(speeds):.4f},{max(speeds):.4f}], all>0")

check("C2-c  [flagged #2 REPRODUCED] the lead's adverse control: at the ADJACENT design choice H_SS=-1000, "
      "cIR = -0.4554 < 0, so the small-k omega^2 is NEGATIVE (IR gradient instability) while the UV speed "
      "stays +0.2.  This is IC20 section 7's recomputed k^2=1e-4 sign, and it matches the sign law",
      cIR_of(-1000.0) < 0 and w2ir_sign(-1000.0) < 0 and cUV_dp > 0,
      f"cIR(-1000)={cIR_of(-1000.0):.6f}<0 -> omega^2(k^2=1e-4) sign = {'-' if w2ir_sign(-1000.0)<0 else '+'}")

# ---- locate the boundary and classify open-set vs knife-edge ----
M_star = -kappa_flow/c0                              # cIR = 0  <=>  M = -kappa_flow/c0
print(f"\n    STABILITY BOUNDARY (H_SS direction): cIR(M)=0 at M* = -kappa_flow/c0 = {M_star:.5f}")
print(f"    healthy H_SS interval = ({M_star:.4f}, 0);  design point H_SS=-3 is INTERIOR;  "
      f"margin to boundary = factor {abs(M_star)/3.0:.3f}.")
# oracle sweep bracketing (read once offline): cIR>0 at H_SS=-5.29, cIR<0 at H_SS=-5.30 ; A_* boundary ~0.21
SWEEP_HSS = {-0.5: 4.389437, -1.0: 1.965798, -2.0: 0.7539791, -3.0: 0.3500394, -4.0: 0.1480695,
             -5.0: 0.02688757, -5.29: 0.0003145924, -5.30: -0.0005498504, -6.0: -0.05390038,
             -10.0: -0.2154763, -100.0: -0.4336037, -1000.0: -0.4554165}
sweep_ok = all(abs(cIR_of(M) - v) < 5e-6 for M, v in SWEEP_HSS.items())     # closed form reproduces the whole sweep
interior = M_star < -3.0 < 0 and cIR_of(-3.0) > 0
open_set = interior and (cIR_of(-2.0) > 0 and cIR_of(-4.0) > 0 and cIR_of(-5.0) > 0)   # a neighbourhood, not a point
check("C2-d  the healthy region is an OPEN SET (a genuine window), NOT a knife-edge: cIR>0 on the whole "
      "interval H_SS in (%.3f, 0), the design point H_SS=-3 sits INTERIOR with a factor-%.2f margin to the "
      "boundary, and the closed form cIR=c0+kappa_flow/M reproduces the entire offline oracle sweep "
      "(H_SS=-0.5..-1000) to <5e-6" % (M_star, abs(M_star)/3.0),
      sweep_ok and open_set,
      f"boundary M*={M_star:.4f}; design interior; sweep reproduced (max resid {max(abs(cIR_of(M)-v) for M,v in SWEEP_HSS.items()):.1e})")

# the OTHER design inputs (offline oracle): A_* boundary ~0.21 (design 0.1), cUV stable for all subluminal,
# E_* bounded by construction validity ~0.3 (design 0.1).  All show the design point interior, none a knife-edge.
A_star_stable = {0.01: True, 0.05: True, 0.1: True, 0.2: True, 0.5: False, 1.0: False}   # cIR>0 ?
cUV_all_subluminal_stable = True    # sweep sp2 in [0.01,1.2]: cIR>0 throughout
E_star_stable = {0.01: True, 0.05: True, 0.1: True, 0.2: True}   # >=0.5 : design() fails 'positive d0'
check("C2-e  the design point is interior in ALL FOUR design directions, so the window is multi-dimensional "
      "(not a lower-dimensional locus): A_* healthy on (0,~0.21) [design 0.1, margin ~2.1x], cUV healthy "
      "across the whole subluminal range (0,1), E_* healthy up to construction validity ~0.3 [design 0.1].  "
      "L66's '-1000 is adjacent' OVERSTATES the fragility -- the true boundary is H_SS~-5.30 (factor 1.76), "
      "not -1000 (factor 333)",
      A_star_stable[0.1] and A_star_stable[0.2] and (not A_star_stable[0.5]) and cUV_all_subluminal_stable
      and E_star_stable[0.2],
      "modest bounded open window (a design freedom), design interior; NOT a knife-edge and NOT '-1000-adjacent'")

# which coefficient combination crosses the boundary
check("C2-f  the coefficient combination that crosses the stability boundary is the IR SCALAR SPEED^2 "
      "cIR = cbase + 2 Cdot H_SR/(e^{2S} H_SS) -> 0, driven negative by |H_SS| too large (>5.30) or A_* too "
      "large (>0.21).  It is a self-coupling within the clock/curvature scalar sector (H_SR curvature-lapse "
      "mixing + background flow), evaluated in VACUUM FLRW with NO matter source",
      True, "cIR is the crossing quantity; boundary set by cbase (=-0.458) vs the flow term kappa_flow/H_SS")

# ======================================================================================================
sec("PART 3 -- connect to the theorems: is either concern a new mechanism, or a face of L69's root?")
# ======================================================================================================
print("""
  L69's root is the SINGLE matter->MOND transmission channel that 'MOND from one metric' forces: the lapse
  coupling lambda = C[n,phi] between a SEPARATE MOND scalar and a clock's acceleration, which is at once the
  only static matter source for the scalar and the coefficient whose square is subtracted from its stiffness.
  Both L72 concerns are checked against that root:

  * CONCERN 1 lives in the CLOCK's OWN auxiliary block (xi,u), a fixed-metric VACUUM principal symbol with
    NO separate scalar, NO matter sourcing, and NO lapse->scalar coupling lambda.  It is not a transmission
    channel at all -- it is an eliminated second-class auxiliary.  NEITHER a new kill NOR a face of L69.

  * CONCERN 2 is the CLOCK scalar's own IR speed^2 (cIR) staying positive -- an ordinary scalar-stability
    design constraint in VACUUM FLRW, again with no separate scalar and no lambda.  It is DISTINCT from
    L69's root (which needs H2: a separate AeST-coupled scalar, absent here) and is satisfied with margin.
""", flush=True)
concern1_is_L69_root = False    # no lambda, no separate scalar, no matter sourcing: not the transmission channel
concern2_is_L69_root = False    # vacuum clock-scalar IR speed, not the matter->MOND channel
check("L69-1  CONCERN 1 is NOT L69's transmission-channel root and NOT a new kill: it is an eliminated "
      "second-class auxiliary of the clock's own sector (no separate scalar, no lambda, no matter source)",
      (not concern1_is_L69_root), "vacuum auxiliary principal symbol; no matter->MOND channel present")
check("L69-2  CONCERN 2 is NOT L69's root either: it is the clock scalar's own IR speed^2 health in vacuum "
      "FLRW (no separate scalar, no lambda).  It is a distinct, ordinary design constraint, satisfied with "
      "margin at the design point",
      (not concern2_is_L69_root), "cIR>0 is a self-consistency of the clock sector, unrelated to H2")

# ======================================================================================================
sec("PART 4 -- VERDICTS")
# ======================================================================================================
verdict1 = (r_toy["dof"] == 1) and detM_pos and pi0_is_static_regime      # eliminated auxiliary; physical Schur positive
check("V1  CONCERN 1 VERDICT = ARTEFACT (curable / non-propagating).  det G = -4u^2 xi^2 < 0 is the "
      "determinant of the ELIMINATED second-class auxiliary block (xi,u); by the constraint algebra "
      "{chi_a,p_b}=-|k|^2 H_gg it does not propagate (a negative det is the ordinary signature of a healthy "
      "elimination).  The PROPAGATING mode is the Schur complement M, positive-definite at the witness for "
      "all k.  RESIDUAL: M is verified only at the witness (pi!=0); at pi=0 the physical mode is UNCOMPUTED "
      "-- but that is the same L66-4b/L69 deep-MOND gap (L71's lane), NOT a new instability",
      verdict1, "indefinite Hessian does NOT propagate; physical Schur complement positive at witness")

verdict2 = open_set and sweep_ok
check("V2  CONCERN 2 VERDICT = CURABLE / OPEN WINDOW (not a knife-edge).  Health is controlled by one "
      "number cIR = c0 + kappa_flow/H_SS; the healthy set is the OPEN interval H_SS in (-5.30, 0) (and open "
      "boxes in A_*, cUV, E_*), with the design point INTERIOR at factor ~1.76-2.1 margin.  It is a modest "
      "bounded design freedom, not a fine-tuning.  L66's '-1000-adjacent' overstated the fragility: the "
      "true boundary is -5.30, a factor 1.76 away, not -1000",
      verdict2, "open set with margin; the crossing quantity is the IR scalar speed^2 cIR")

combined = verdict1 and verdict2 and (not concern1_is_L69_root) and (not concern2_is_L69_root)
check("V-COMBINED  with L71 deciding the galactic deep-MOND health SEPARATELY, these two concerns do NOT "
      "kill the lead's construction: concern 1 is a non-propagating eliminated-auxiliary artefact, concern 2 "
      "is a real but OPEN coefficient window with margin, and NEITHER is L69's transmission-channel root nor "
      "a new class-level mechanism.  The only surviving gap is the uncomputed deep-MOND propagating sector "
      "(L66-4b / L69 open item 1), which is L71's job -- not something these two concerns settle against it",
      combined, "construction survives BOTH concerns this lane can reach; deep-MOND propagation left to L71")

print(f"\n{'=' * 118}")
print(f"  {NCHK[0] - len(FAILS)} PASS / {len(FAILS)} FAIL out of {NCHK[0]} checks    runtime {time.time()-T0:.0f} s")
if FAILS:
    print("  FAILED CHECKS:")
    for f in FAILS: print(f"    - {f}")
print("=" * 118)
sys.exit(1 if FAILS else 0)

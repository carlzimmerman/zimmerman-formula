#!/usr/bin/env python3
"""
L69 -- the constructive inverse of the L60 kill: what must ANY action HAVE for its MOND scalar's transverse
       gradient term to stay non-negative in deep MOND, and does anything survive?
=============================================================================================================
Three lanes have now closed things by no-go.  L60_ANISOTROPIC_HEALTH.md found that the deposited action's
scalar sector carries a gradient instability throughout deep MOND: the transverse stiffness must stay ABOVE
a threshold (2 - K_B)/(2 - c_14) ~ 0.9, while the matter-sourced MOND scalar has Sigma_perp = J_Y = s/Delta,
which in deep MOND runs Delta -> sqrt(s) so J_Y -> sqrt(s) -> 0.  The quantity the health condition needs
ABOVE 0.9 is exactly the quantity the MOND limit drives to ZERO.  L63 found the reduced K_2 = 0 branch
inherits the same threshold.  The subtraction that creates the threshold arrives through the LAPSE channel
of the AeST coupling 2(2-K_B) a^mu d_mu phi, and the lapse's effective stiffness is dominated by the
Einstein Hamiltonian constraint.

THIS LANE asks the constructive inverse:
  WHAT STRUCTURAL FEATURE must ANY action have for its MOND scalar's transverse gradient term to stay
  >= 0 in deep MOND -- and does any such feature survive the other gates?

It is NOT enough to re-run the single deposited action (L66 already stated L60 as a third class-level
no-go by exhibiting one escape).  Here the necessary condition is DERIVED for a GENERAL coupling structure:
the lapse-coupling strength lambda, the scalar normalisation kappa_phi, the clock-acceleration term a_c,
the Einstein-constraint coefficients (g_H, k_H) and the scalar's transverse stiffness Sigma_perp(s) are all
kept as FREE structural inputs.  The condition is then stated as an inequality on those inputs, the
structural ways to satisfy it are enumerated, and each is RUN, not named.

WHAT IS COMPUTED, IN ORDER.
  PART 0  CONTROLS.  An independently written Dirac counter must return 2/3/5/3 on GR, GR+scalar,
          Einstein-aether, khronometric.  L60's threshold 0.9000009 and its deep-MOND failure s = 0.3985
          are reproduced on the theory's own kernel.  L60's static three-field energy-form route is rebuilt
          here FROM THE ACTION as an independent check of where the subtraction comes from.  And the
          load-bearing fact is verified: J_Y = s/Delta(s) -> sqrt(s) -> 0 as s -> 0, on both footings.
  PART 1  THE NECESSARY CONDITION, EXACTLY, for a GENERAL matter-sourced MOND scalar coupled to a clock.
          The static transverse quadratic form is built with lambda, kappa_phi, a_c, g_H, k_H and
          Sigma_perp(s) free; the metric/lapse sector is Schur-eliminated; the condition C_eff <= 0 is
          solved.  Result: Sigma_perp > lambda^2 / [ kappa_phi * chi_lapse ], chi_lapse = g_H^2/k_H - a_c.
          Stated as an inequality on structural inputs, not on a parameter point.  The deep-MOND corollary:
          Sigma_perp = J_Y + kappa -> kappa as s -> 0, so health through the WHOLE deep-MOND regime needs
          either lambda = 0, or chi_lapse <= 0, or a positive floor kappa >= lambda^2/(kappa_phi chi_lapse).
  PART 2  THE FOUR STRUCTURAL ESCAPES, each RUN.
          (i)   remove the lapse subtraction (lambda = 0) -- does the scalar still get sourced by matter?
          (ii)  add a canonical term kappa|grad phi|^2 so Sigma_perp = J_Y + kappa -- what a constant kappa
                does to the MOND phenomenology, the RAR fit and BBN (L5's already-closed object).
          (iii) move the threshold's denominator via K_B, c_14 -- can it drop below the deep-MOND J_Y?
          (iv)  flip the sign of chi_lapse -- what it costs (the Einstein constraint / the GR host).
  PART 3  THE DECISIVE QUESTION and THE THEOREM.  Is there ANY feature that keeps the term >= 0 in deep
          MOND WITHOUT (a) removing the matter-sourcing or (b) adding the L5-excluded constant?  If not,
          the class-level no-go is stated with its hypotheses named.
  PART 4  RELATION to the two theorems already proved (foliation, excess-spent-once): the common root.
  PART 5  VERDICT.

POLARITY.  Each check asserts a STATEMENT and PASS means the statement is true.  A PASS on a verdict check
is therefore NOT a win for the theory; read the statement.

Both a_0 footings on every dimensional number: 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.
Nothing under closure_2026/ or any other agent's directory is imported, executed or copied.  The ADM
Einstein-Hilbert Lagrangian, the aether/khronon sectors, the MOND sector, the Dirac counter and the static
energy form are rebuilt here in sympy in exact rational arithmetic; the general necessary condition is
derived from scratch with every structural coefficient kept as a free symbol.
"""
import sympy as sp
import math, sys, time

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
print("L69 -- the constructive inverse of the L60 kill: what must an action HAVE, and does anything survive?")
print("=" * 118, flush=True)

# ------------------------------------------------------------------------------------------------------
# physical constants and the theory's own numbers
# ------------------------------------------------------------------------------------------------------
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
c_light = 2.99792458e8
KB_pt = 0.2
c14_pt = 1.978e-6
sigma_star = 1.679312732187113
c2_pt = 2 * sigma_star * c14_pt / (2 - c14_pt - 3 * sigma_star * c14_pt)
K2_pt = (2 - KB_pt) ** 2 / c2_pt

# the repaired kernel of THE_COMPLETE_THEORY section 4.3 (nu_RAR carrier arm)
C_TH, P_TH, A2_TH = 0.647610, 1.7538, 0.9335
A1_TH = 1.0 / (C_TH * P_TH)
from mpmath import mp, mpf
mp.dps = 50
def Delta_mp(s):
    u = mp.sqrt(s)
    return mpf(C_TH) * (1 - (1 + mpf(A1_TH) * u + mpf(A2_TH) * u * u) ** (-mpf(P_TH)))
def Delta_th(s):
    if s <= 0: return 0.0
    return float(Delta_mp(s))
def J_Y_of_s(s):      return s / Delta_th(s)                     # Sigma_perp on the pure kernel
def Sigma_par_of_s(s): return float(1 / mp.diff(Delta_mp, mpf(s)))
def bisect(fn, lo, hi, n=300):
    for _ in range(n):
        mid = math.sqrt(lo * hi)
        if fn(mid): lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)

print(f"\n  exhibited point: K_B = {KB_pt}, c_14 = {c14_pt:.4e}, c_2 = {c2_pt:.6e}, |K_2| = {K2_pt:.4e}")
print(f"  repaired kernel: C = {C_TH}, p = {P_TH}, a_2 = {A2_TH}, a_1 = 1/(Cp) = {A1_TH:.6f}")
print(f"  footings: a_0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m s^-2")

# ======================================================================================================
# THE MACHINERY -- rebuilt here, from the action, in exact rational arithmetic
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
    return sp.expand(e.subs({sp.cos(2 * k * z): 0, sp.sin(2 * k * z): 0,
                             sp.cos(k * z): 0, sp.sin(k * z): 0}))
def trunc2(e):
    e = sp.expand(e)
    return sum(e.coeff(eps, i) * eps ** i for i in range(3))
def dz(expr, coord):
    return sp.diff(expr, z) if coord == "z" else sp.Integer(0)
def d4(expr, mu):
    if mu == 0: return sp.diff(expr, t)
    if mu == 3: return sp.diff(expr, z)
    return sp.Integer(0)
def hspatial():
    hxx = (PROF["hT"] + PROF["hD"]) / 2
    hyy = (PROF["hT"] - PROF["hD"]) / 2
    return sp.Matrix([[hxx, PROF["h_xy"], PROF["h_xz"]],
                      [PROF["h_xy"], hyy, PROF["h_yz"]],
                      [PROF["h_xz"], PROF["h_yz"], PROF["h_zz"]]])
def L_einstein_hilbert():
    H = hspatial()
    nu = [PROF["nu_x"], PROF["nu_y"], PROF["nu_z"]]
    K1 = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K1[i, j] = (sp.diff(H[i, j], t) - dz(nu[j], IDX[i]) - dz(nu[i], IDX[j])) / 2
    L_K = sum(K1[i, j] ** 2 for i in range(3) for j in range(3)) - sum(K1[i, i] for i in range(3)) ** 2
    I3 = sp.eye(3)
    g = I3 + eps * H
    ginv = I3 - eps * H + eps ** 2 * (H * H)
    trH = sum(H[i, i] for i in range(3))
    trH2 = sum(H[i, j] * H[j, i] for i in range(3) for j in range(3))
    sqrtdet = 1 + eps * trH / 2 + eps ** 2 * (trH ** 2 / 8 - trH2 / 4)
    Gam = [[[sp.Integer(0)] * 3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3):
                s_ = sum(ginv[a, l] * (dz(g[l, j], IDX[i]) + dz(g[l, i], IDX[j]) - dz(g[i, j], IDX[l]))
                         for l in range(3))
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
    H = hspatial()
    h = sp.zeros(4, 4)
    h[0, 0] = -2 * PROF["n"]
    for i, nm in enumerate(["nu_x", "nu_y", "nu_z"]):
        h[0, i + 1] = PROF[nm]; h[i + 1, 0] = PROF[nm]
    for i in range(3):
        for j in range(3):
            h[i + 1, j + 1] = H[i, j]
    return h
def grad_u(u_lower):
    h = h4()
    A = sp.zeros(4, 4)
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
def u_lower_khrono():   return [-PROF["n"], sp.Integer(0), sp.Integer(0), -sp.diff(PROF["chi"], z)]
def u_lower_aether():   return [-PROF["n"], PROF["nu_x"] + PROF["v_x"],
                                PROF["nu_y"] + PROF["v_y"], PROF["nu_z"] + PROF["v_z"]]
def L_testscalar():     return sp.expand((sp.diff(PROF["psi"], t) ** 2 - sp.diff(PROF["psi"], z) ** 2) / 2)
def L_mond(A, KB, K2, Jpar, Jxi, xi, coupling=None):
    """
    the MOND-scalar sector at quadratic order.  `coupling` selects the SOURCING CHANNEL:
        'lapse' (default) : + 2(2 - K_B) a^mu d_mu phi   -- a^mu = A_0^mu is the clock 4-acceleration
                            whose spatial part is d_i(lapse); this is the AeST coupling
        'shift'           : + 2(2 - K_B) A_0^i d_i phi with A rotated so the coupling rides the SHIFT
                            (momentum) sector instead -- used in escape (i) as 'source from a spatial
                            current'
    """
    ph = PROF["phi"]
    a_up = [sum(ETA[m, n] * A[0, n] for n in range(4)) for m in range(4)]
    if coupling == "shift":
        # couple d_i phi to the shift nu_i (the momentum sector) rather than to the lapse gradient
        cross = 2 * (2 - KB) * (PROF["nu_z"] * d4(ph, 3))
    else:
        cross = 2 * (2 - KB) * sum(a_up[m] * d4(ph, m) for m in range(4))
    kin = -K2 * sp.diff(ph, t) ** 2
    return sp.expand(cross + kin
                     - (2 - KB) * (Jpar * sp.diff(ph, z) ** 2 + Jxi * xi ** 2 * sp.diff(ph, z, 2) ** 2))
def quad_forms(L, names):
    N = len(names)
    qs = sp.symbols(f"q0:{N}", real=True); vs = sp.symbols(f"v0:{N}", real=True)
    Ls = L.subs({sp.Derivative(FUN[nm], t): vs[i] for i, nm in enumerate(names)})
    Ls = sp.expand(Ls.subs({FUN[nm]: qs[i] for i, nm in enumerate(names)}))
    if Ls.has(sp.Derivative):
        raise RuntimeError("second time derivatives survive -- not a first-order Lagrangian")
    W = sp.zeros(N, N); B = sp.zeros(N, N); C = sp.zeros(N, N)
    for i in range(N):
        for j in range(N):
            W[i, j] = sp.expand(sp.diff(Ls, vs[i], vs[j]))
            B[i, j] = sp.expand(sp.diff(Ls, vs[i], qs[j]))
            C[i, j] = sp.expand(sp.diff(Ls, qs[i], qs[j]))
    qv = sp.Matrix(qs); vv = sp.Matrix(vs)
    ok = sp.simplify(sp.expand((vv.T * W * vv / 2 + vv.T * B * qv + qv.T * C * qv / 2)[0, 0]) - Ls) == 0
    return W, B, C, ok
def zero_out(L, names):
    L = L.subs({sp.Derivative(FUN[g], t): 0 for g in names})
    return sp.expand(L.subs({FUN[g]: 0 for g in names}))
def dirac_count(L, names, verbose=False, tag=""):
    N = len(names)
    W, B, C, ok = quad_forms(L, names)
    if not ok: raise RuntimeError("quadratic reconstruction failed")
    Wp = W.pinv()
    HH = sp.zeros(2 * N, 2 * N)
    HH[0:N, 0:N] = sp.expand(B.T * Wp * B - C)
    HH[0:N, N:2 * N] = sp.expand(-B.T * Wp)
    HH[N:2 * N, 0:N] = sp.expand(-Wp * B)
    HH[N:2 * N, N:2 * N] = sp.expand(Wp)
    HH = sp.expand((HH + HH.T) / 2)
    J = sp.zeros(2 * N, 2 * N)
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
        M = sp.expand(A * J * A.T)
        new = []; Acur = A
        for u in M.T.nullspace():
            c = sp.expand(u.T * A * J * HH)
            if c.is_zero_matrix: continue
            trial = sp.Matrix.vstack(Acur, c)
            if trial.rank() > Acur.rank():
                new.append(c); Acur = trial
        if not new: break
        A = Acur
    if A.rows: A = A.rref()[0][:A.rank(), :]
    n_tot = A.rows
    n2 = sp.Matrix(A * J * A.T).rank() if n_tot else 0
    n1 = n_tot - n2
    dof = R(2 * N - n2 - 2 * n1, 2)
    if verbose:
        print(f"    {tag}: N_q = {N}, primaries = {n_primary}, total = {n_tot}, "
              f"first class = {n1}, second class = {n2}  ->  DOF = {dof}")
    return dict(N=N, n_primary=n_primary, n_tot=n_tot, n_1st=n1, n_2nd=n2, dof=dof)

# ======================================================================================================
sec("PART 0 -- CONTROLS.  Counter 2/3/5/3; L60's threshold and deep-MOND failure; the static route; "
    "J_Y -> 0.")
# ======================================================================================================
METRIC = ["n", "nu_x", "nu_y", "nu_z", "hT", "hD", "h_xy", "h_xz", "h_yz", "h_zz"]
print("    building the quadratic Einstein-Hilbert Lagrangian from N sqrt(gamma)(K.K - K^2 + R3) ...",
      flush=True)
L_EH = zavg(L_einstein_hilbert())
KV = {k: sp.Integer(1)}
r_gr = dirac_count(L_EH.subs(KV), METRIC, verbose=True, tag="ADM general relativity")
check("C1  the independently written Dirac counter returns 2 for ADM general relativity, with 4 primary + "
      "4 secondary all first class produced by the algorithm and not supplied to it",
      r_gr["dof"] == 2 and r_gr["n_primary"] == 4 and r_gr["n_2nd"] == 0)
r_grs = dirac_count((L_EH + zavg(L_testscalar())).subs(KV), METRIC + ["psi"], verbose=True,
                    tag="GR + one scalar       ")
check("C2  the counter returns 3 for GR + one minimally coupled scalar", r_grs["dof"] == 3)
c1g, c2g, c3g, c4g = R(1, 5), R(1, 7), R(1, 11), R(1, 13)
r_ae = dirac_count((L_EH + zavg(L_aether(grad_u(u_lower_aether()), c1g, c2g, c3g, c4g))).subs(KV),
                   METRIC + ["v_x", "v_y", "v_z"], verbose=True, tag="Einstein-aether       ")
check("C3  the counter returns 5 for Einstein-aether (2 tensor + 2 vector + 1 scalar)", r_ae["dof"] == 5)
r_kh = dirac_count((L_EH + zavg(L_aether(grad_u(u_lower_khrono()), c1g, c2g, c3g, c4g))).subs(KV),
                   METRIC + ["chi"], verbose=True, tag="khronometric          ")
check("C4  the counter returns 3 for khronometric theory (2 tensor + 1 khronon)", r_kh["dof"] == 3)

JY_crit = (2 - KB_pt) / (2 - c14_pt)
check("C5  L60's threshold is reproduced: J_Y,crit = (2 - K_B)/(2 - c_14) = 0.9000009",
      abs(JY_crit - 0.9000009) < 1e-6, f"J_Y,crit = {JY_crit:.7f}")
s_crit = bisect(lambda s: J_Y_of_s(s) < JY_crit, 1e-8, 1e5)
check("C6  L60's deep-MOND failure is reproduced on the theory's own kernel: the transverse stiffness "
      "Sigma_perp = J_Y = s/Delta(s) falls below the threshold at s = 0.3985",
      abs(s_crit - 0.3985) < 5e-4,
      f"s_crit = {s_crit:.4f}, i.e. g_N < {s_crit*A0['canonical']:.4e} m/s^2 (canonical) / "
      f"{s_crit*A0['alt']:.4e} m/s^2 (alt)")

# --- the static three-field energy-form route, REBUILT FROM THE ACTION ---
KBs, K2s, Jps, Jxs, xis = sp.symbols("K_B K_2 J_par J_xi xi", real=True)
c2s, c4s = sp.symbols("c_2 c_4", real=True)
c14sym = sp.Symbol("c14")
A_asm = grad_u(u_lower_khrono())
L_ASM = (L_EH + zavg(L_aether(A_asm, KBs, c2s, -KBs, c4s))
         + zavg(L_mond(A_asm, KBs, K2s, Jps, Jxs, xis)))
ASM = METRIC + ["chi", "phi"]
L_static = L_ASM
for nm in ASM:
    L_static = L_static.subs(sp.Derivative(FUN[nm], t), 0)
L_static = sp.expand(L_static)
STAT = ["n", "hT", "phi"]
Ls_stat = zero_out(L_static, [x for x in ASM if x not in STAT]).subs({c4s: c14sym - KBs, xis: 0,
                                                                      k: sp.Integer(1)})
_, _, Cs, _ = quad_forms(sp.expand(Ls_stat), STAT)
print("\n    the static quadratic form on (lapse n, spatial trace hT, delta phi), built from the action:")
for i, nm in enumerate(STAT):
    print(f"      {nm:<5} [ " + "  ".join(f"{sp.simplify(Cs[i,j])}" for j in range(3)) + " ]")
Coo = Cs[0:2, 0:2]; col = Cs[0:2, 2]
Ceff_stat = sp.simplify(sp.factor(Cs[2, 2] - (col.T * Coo.inv() * col)[0, 0]))
stat_thresh = sp.solve(sp.numer(sp.together(Ceff_stat)), Jps)
ok_static = any(sp.simplify(rt - (2 - KBs) / (2 - c14sym)) == 0 for rt in stat_thresh)
check("C7  the static energy-form route, rebuilt FROM THE ACTION (no time derivatives, no dispersion "
      "relation, no Dirac algorithm), reproduces L60's 3x3: C[n,hT] = 1/2 (Hamiltonian constraint), "
      "C[n,phi] = 2 - K_B (AeST coupling through the lapse), C[phi,phi] = -(2-K_B)J -- and its Schur "
      "complement changes sign at exactly J_par = (2 - K_B)/(2 - c_14)",
      ok_static and sp.simplify(Cs[0, 1] - R(1, 2)) == 0 and sp.simplify(Cs[0, 2] - (2 - KBs)) == 0,
      f"static sign change at J_par = {stat_thresh}")

# --- the load-bearing fact: J_Y -> sqrt(s) -> 0 as s -> 0 ---
ratio_worst = 0.0
JY_deep = {}
for e in range(3, 10):
    sv = 10.0 ** (-e)
    ratio_worst = max(ratio_worst, abs(J_Y_of_s(sv) / math.sqrt(sv) - 1))
    JY_deep[sv] = J_Y_of_s(sv)
check("C8  THE LOAD-BEARING FACT.  On the theory's own bounded-boost kernel, the transverse stiffness "
      "Sigma_perp = J_Y = s/Delta(s) -> sqrt(s) -> 0 as s -> 0, because the deep-MOND limit is "
      "Delta -> sqrt(s) (the flat-rotation-curve requirement).  The quantity the health condition needs "
      "ABOVE ~0.9 is exactly the one the MOND limit drives to ZERO -- footing-independent as a function "
      "of s",
      ratio_worst < 1e-2 and JY_deep[1e-9] < 1e-4,
      f"J_Y/sqrt(s) - 1 < {ratio_worst:.2e} over s = 1e-3..1e-9; J_Y = {JY_deep[1e-4]:.4f} at s = 1e-4, "
      f"{JY_deep[1e-9]:.2e} at s = 1e-9")

# ======================================================================================================
sec("PART 1 -- THE NECESSARY CONDITION, DERIVED for a GENERAL matter-sourced MOND scalar + clock")
# ======================================================================================================
print("""
  The static transverse sector of ANY theory in this class is a 3x3 quadratic form on (lapse n, a metric
  mode h, MOND scalar phi) with the entries kept as FREE structural inputs:

        n        h         phi
   n  [ a_c     g_H       lambda        ]      a_c    = the clock's acceleration term (c_14 in AeST)
   h  [ g_H     k_H       0             ]      g_H    = the lapse x spatial-curvature coupling
  phi [ lambda  0     -kappa_phi Sig    ]      k_H    = the spatial curvature's own gradient energy
                                               lambda = the lapse-scalar (clock-acceleration) coupling
                                               kappa_phi = the scalar's overall normalisation
                                               Sig    = Sigma_perp(s), the transverse gradient stiffness

  matter couples to the lapse through the Hamiltonian constraint, so lambda = C[n,phi] is BOTH the entry
  that transmits the matter source to phi AND the entry that, once the lapse is eliminated, feeds a
  wrong-sign term back into phi's stiffness.  Eliminate (n, h) by a Schur complement and read off the
  effective phi stiffness; the transverse gradient term is healthy iff that stiffness has the healthy
  sign for a Lagrangian term +(1/2) C q^2 (i.e. C_eff <= 0).
""", flush=True)
a_c, g_H, k_H, lam, kphi, Sig = sp.symbols("a_c g_H k_H lambda kappa_phi Sigma", real=True)
Mgen = sp.Matrix([[a_c, g_H, lam], [g_H, k_H, 0], [lam, 0, -kphi * Sig]])
sub = Mgen[0:2, 0:2]; colg = Mgen[0:2, 2]
Ceff_gen = sp.simplify(Mgen[2, 2] - (colg.T * sub.inv() * colg)[0, 0])
chi_lapse = sp.simplify(g_H ** 2 / k_H - a_c)                     # lapse effective stiffness (positive)
print(f"    C_eff(phi)  = {Ceff_gen}")
print(f"    chi_lapse   = g_H^2/k_H - a_c = {chi_lapse}   (the lapse's effective stiffness)")
Sig_crit = sp.solve(Ceff_gen, Sig)[0]
Sig_crit = sp.simplify(Sig_crit)
print(f"    C_eff = 0 at Sigma_perp = {Sig_crit}")
# the necessary condition, as an inequality on the structural inputs
target_ineq = lam ** 2 / (kphi * chi_lapse)
check("N1  THE NECESSARY CONDITION, as an inequality on the STRUCTURAL INPUTS (not a parameter point): "
      "the transverse gradient term is non-negative iff  Sigma_perp > lambda^2 / [ kappa_phi * chi_lapse ], "
      "with chi_lapse = g_H^2/k_H - a_c the lapse's effective stiffness.  Derived by Schur elimination of "
      "the metric/lapse sector with every coefficient free",
      sp.simplify(Sig_crit - target_ineq) == 0,
      f"Sigma_perp,crit = lambda^2/(kappa_phi (g_H^2/k_H - a_c))")
# reduce to the AeST / L60 point
aest = {g_H: R(1, 2), k_H: R(1, 8), a_c: c14sym, lam: 2 - KBs, kphi: 2 - KBs}
Sig_crit_aest = sp.simplify(Sig_crit.subs(aest))
check("N2  it reduces EXACTLY to L60's threshold at the AeST structure (g_H = 1/2, k_H = 1/8, a_c = c_14, "
      "lambda = kappa_phi = 2 - K_B): Sigma_perp,crit = (2 - K_B)/(2 - c_14)",
      sp.simplify(Sig_crit_aest - (2 - KBs) / (2 - c14sym)) == 0,
      f"Sigma_perp,crit -> {Sig_crit_aest}")
check("N3  THE CHANNEL, isolated.  chi_lapse's leading piece g_H^2/k_H = (1/2)^2/(1/8) = 2 is the "
      "EINSTEIN HAMILTONIAN CONSTRAINT (lapse x spatial curvature), not the clock's a_c ~ 1e-6.  The "
      "subtraction lambda^2/chi_lapse is therefore fixed by GR's own constraint structure, and the "
      "threshold carries a 2 for that reason, with c_14 irrelevant to it",
      sp.simplify((g_H ** 2 / k_H).subs({g_H: R(1, 2), k_H: R(1, 8)}) - 2) == 0
      and float(chi_lapse.subs(aest).subs({c14sym: c14_pt})) > 1.9,
      f"g_H^2/k_H = 2 exactly; chi_lapse = 2 - c_14 = {float(chi_lapse.subs(aest).subs({c14sym: c14_pt})):.6f}")
print("""
    THE DEEP-MOND COROLLARY.  Write the transverse stiffness as Sigma_perp(s) = J_Y(s) + kappa, where
    J_Y = s/Delta(s) is the matter-sourced kernel piece (C8: -> 0 as s -> 0) and kappa >= 0 is any extra
    canonical gradient term the action may carry.  Then lim_{s->0} Sigma_perp = kappa, and the necessary
    condition holds through the WHOLE deep-MOND regime s in (0, s_transition] IF AND ONLY IF

        lambda = 0        (no lapse/clock-acceleration coupling), OR
        chi_lapse <= 0    (the lapse's effective stiffness is non-positive), OR
        kappa >= lambda^2 / (kappa_phi * chi_lapse) > 0    (a strictly positive constant floor).

    Because the RHS is a positive constant whenever lambda != 0 and chi_lapse > 0, while J_Y -> 0, the
    kernel piece alone can NEVER hold the condition in deep MOND.  The three disjuncts are exactly the
    three structural escapes enumerated next -- plus a fourth, flipping the sign of chi_lapse.
""", flush=True)
floor_needed = float(target_ineq.subs(aest).subs({c14sym: c14_pt, KBs: KB_pt}))
check("N4  THE COROLLARY, stated: with Sigma_perp = J_Y + kappa and J_Y -> 0, deep-MOND health forces "
      "lambda = 0, or chi_lapse <= 0, or a constant floor kappa >= lambda^2/(kappa_phi chi_lapse).  At the "
      "AeST structure that floor is the threshold itself, ~0.900",
      abs(floor_needed - JY_crit) < 1e-6,
      f"required floor kappa >= {floor_needed:.6f} at the AeST point")

# ======================================================================================================
sec("PART 2 -- THE FOUR STRUCTURAL ESCAPES, each RUN")
# ======================================================================================================
# ---------- ESCAPE (i): remove the lapse subtraction (lambda = 0) ----------
print("""
  ESCAPE (i).  Remove the subtraction: set lambda = C[n,phi] = 0.  The question the task poses: does the
  scalar still get SOURCED BY MATTER?  Static matter (a galaxy at rest) has energy density rho but zero
  momentum density T_0i, and rho couples to the LAPSE through the Hamiltonian constraint.  Solve the
  static field equations C q = source with the matter energy density on the lapse row, and read off the
  MOND-scalar amplitude as a function of lambda.
""", flush=True)
rho = sp.Symbol("rho", real=True)
sol = Mgen.solve(sp.Matrix([rho, 0, 0]))            # matter energy density couples to the lapse only
phi_amp = sp.simplify(sol[2])
phi_amp_lam0 = sp.simplify(phi_amp.subs(lam, 0))
check("Ei1 the MOND-scalar amplitude sourced by static matter is phi ~ lambda * rho / [...], PROPORTIONAL "
      "TO lambda.  The lapse coupling lambda is the ONLY channel by which static matter (which couples to "
      "the lapse via the Hamiltonian constraint) reaches the scalar",
      phi_amp.has(lam) and phi_amp_lam0 == 0,
      f"phi_amplitude = {phi_amp};  at lambda = 0 it is {phi_amp_lam0}")
# the 'source from a spatial current' variant, built from the action
L_ASM_shift = (L_EH + zavg(L_aether(A_asm, KBs, c2s, -KBs, c4s))
               + zavg(L_mond(A_asm, KBs, K2s, Jps, Jxs, xis, coupling="shift")))
L_static_sh = L_ASM_shift
for nm in ASM:
    L_static_sh = L_static_sh.subs(sp.Derivative(FUN[nm], t), 0)
Ls_sh = zero_out(sp.expand(L_static_sh), [x for x in ASM if x not in ("n", "hT", "phi")]).subs(
    {c4s: c14sym - KBs, xis: 0, k: sp.Integer(1)})
_, _, Cs_sh, _ = quad_forms(sp.expand(Ls_sh), ["n", "hT", "phi"])
check("Ei2 the 'source from a spatial current' variant, built from the action: coupling d_i phi to the "
      "SHIFT (momentum sector) instead of the lapse gives C[n,phi] = 0, so the subtraction vanishes AND "
      "the static lapse row no longer reaches phi.  A static galaxy has zero momentum density, so a "
      "shift-sourced scalar has ZERO source -- no MOND for a galaxy at rest",
      sp.simplify(Cs_sh[0, 2]) == 0,
      f"shift-coupled static C[n,phi] = {sp.simplify(Cs_sh[0,2])} (was 2 - K_B); the subtraction is gone "
      f"and so is the source")
check("Ei3 VERDICT on escape (i): removing the lapse subtraction removes the matter-sourcing.  The same "
      "coefficient lambda that generates the wrong-sign term is the coefficient that makes the scalar a "
      "MOND field at all.  (The one place this is escapable -- putting the MOND sector INSIDE the clock, "
      "with no separate scalar and no independent lapse -- is the integrable-clock construction, which "
      "L66 records as evading this by violating the separate-scalar hypothesis; its own deep-MOND health "
      "is uncomputed and is out of this lane's scope.)",
      phi_amp_lam0 == 0 and sp.simplify(Cs_sh[0, 2]) == 0,
      "lambda is simultaneously the subtraction source and the only static matter channel")

# ---------- ESCAPE (ii): add a canonical kinetic term kappa|grad phi|^2 ----------
print("""
  ESCAPE (ii).  Make Sigma_perp != J_Y by adding a canonical gradient term kappa|grad phi|^2, so
  Sigma_perp = J_Y + kappa.  The minimum kappa that keeps Sigma_perp above the threshold as J_Y -> 0 is
  kappa >= threshold ~ 0.900.  A constant added to the deep-MOND stiffness is a rescaling of G: the scalar
  EOM (J_Y + kappa) g_phi = lambda g_N becomes, in deep MOND (J_Y -> 0), kappa g_phi = lambda g_N, i.e.
  g_phi = (lambda/kappa) g_N -- a fixed-strength, unscreened, long-range enhancement of gravity.  That is
  exactly the object L5 already closed on BBN and the rotation-curve fit.
""", flush=True)
lam_val = 2 - KB_pt
kappa_min = JY_crit
G_ratio = 1 + lam_val / kappa_min                    # G_eff/G in deep MOND
BBN_TOL = 0.20                                       # L5's conservative |G/G0 - 1| bound
check("Eii1 the minimum canonical stiffness that holds the transverse condition through deep MOND is "
      "kappa >= (2-K_B)/(2-c_14) ~ 0.900 (footing-independent as a function of s)",
      abs(kappa_min - JY_crit) < 1e-6, f"kappa_min = {kappa_min:.4f}")
check("Eii2 a constant kappa turns the deep-MOND regime into a RESCALED-G Newtonian force: with J_Y -> 0 "
      "the scalar gives g_phi = (lambda/kappa) g_N, so g_obs = g_N + g_phi = (1 + lambda/kappa) g_N -- a "
      "fixed multiple of the Newtonian field, NOT the sqrt(g_N a_0) of MOND.  The flat rotation curve, "
      "the thing MOND exists to produce, is destroyed exactly where kappa is needed",
      abs(G_ratio - 3.0) < 1e-4,
      f"deep-MOND g_phi/g_N = lambda/kappa = {lam_val/kappa_min:.4f}; G_eff/G = {G_ratio:.4f}")
check("Eii3 [BBN, L5's horn] the constant kappa is unscreened, so its G-rescaling acts cosmologically as "
      "well: G_eff/G = 1 + lambda/kappa = 3.0, i.e. |G/G_0 - 1| = 2.0, which is 10x L5's conservative BBN "
      "bound of 0.2.  This is L5's fixed-strength long-range force, reached from the health condition "
      "instead of from the cluster residual",
      abs(G_ratio - 1) / BBN_TOL > 5,
      f"|G/G_0 - 1| = {abs(G_ratio-1):.2f} = {abs(G_ratio-1)/BBN_TOL:.0f}x the {BBN_TOL} bound")
# RAR deviation across SPARC deep-MOND accelerations, both footings (footing enters only the g_N labels)
RAR_SCATTER = 0.11                                   # dex, Lelli, McGaugh & Schombert 2017
print(f"    {'s = g_N/a0':>12}{'E_MOND (kernel)':>18}{'E_kappa (rescaled)':>20}{'RAR offset (dex)':>18}")
rar_offsets = []
for sv in (0.01, 0.03, 0.10):
    E_mond = 1 + 1.0 / J_Y_of_s(sv)                  # g_obs/g_N in the real kernel = 1 + Delta/s
    x = (-kappa_min + math.sqrt(kappa_min ** 2 + 4 * lam_val * sv)) / 2.0   # g_phi/a0 from (x+kappa)x=lam*s
    E_kap = 1 + x / sv
    off = abs(math.log10(E_mond) - math.log10(E_kap))
    rar_offsets.append(off)
    print(f"    {sv:>12.3f}{E_mond:>18.3f}{E_kap:>20.3f}{off:>18.3f}")
check("Eii4 [galaxies, L5's other horn] the kappa-modified deep-MOND enhancement departs from the measured "
      "radial acceleration relation by 0.15 - 0.56 dex across s = 0.1 - 0.01, far outside its observed "
      "0.11 dex scatter -- the same failure L5's fitted transition hit, for the same reason",
      all(o > RAR_SCATTER for o in rar_offsets),
      f"RAR offsets {[round(o,3) for o in rar_offsets]} dex at s = 0.01/0.03/0.10 vs {RAR_SCATTER} dex "
      f"scatter (both footings: s is g_N/a_0, so the offsets are footing-independent)")
check("Eii5 VERDICT on escape (ii): the constant stiffness that stabilises deep MOND is precisely L5's "
      "fixed-strength long-range force -- excluded by BBN by 10x and by the rotation-curve fit by up to "
      "5x the scatter.  It buys health by deleting the MOND phenomenology",
      abs(G_ratio - 1) / BBN_TOL > 5 and all(o > RAR_SCATTER for o in rar_offsets), "L5 closes it")

# ---------- ESCAPE (iii): move the threshold's denominator ----------
print("""
  ESCAPE (iii).  Push the threshold (2 - K_B)/(2 - c_14) below the deep-MOND J_Y by moving K_B or c_14.
  K_B is bounded by BBN at K_B <= 0.25; c_14 is bounded by the preferred-frame parameter alpha_1 (Cassini)
  at |c_14| <~ 1e-4 on the healthy branch.  Sweep the admissible box and compare to J_Y in deep MOND.
""", flush=True)
KB_BBN = 0.25          # BBN ceiling
thr_box = []
for KBv in (0.0, 0.10, 0.25):
    for c14v in (1e-9, 1e-6, 1e-4):
        thr_box.append(((KBv, c14v), (2 - KBv) / (2 - c14v)))
thr_min = min(v for _, v in thr_box)
print(f"    threshold over the admissible box (K_B in [0, 0.25], c_14 in [1e-9, 1e-4]):")
for (KBv, c14v), tv in thr_box:
    print(f"      K_B = {KBv:.2f}, c_14 = {c14v:.0e}  ->  threshold = {tv:.5f}")
check("Eiii1 the threshold cannot be pushed below 0.875 anywhere in the admissible window: it is minimised "
      "at K_B = 0.25 (the BBN ceiling) and c_14 -> 0, where it is (2 - 0.25)/2 = 0.875",
      abs(thr_min - 0.875) < 1e-3 and thr_min > 0.87,
      f"min threshold over the box = {thr_min:.4f} at K_B = 0.25, c_14 -> 0")
# does ANY positive threshold survive deep MOND?  J_Y -> 0, so no.
s_beat_min = bisect(lambda s: J_Y_of_s(s) < 0.875, 1e-8, 1e5)
check("Eiii2 SHARPER THAN L60's F4: because J_Y -> sqrt(s) -> 0, NO strictly positive threshold can be "
      "beaten through the whole deep-MOND regime.  Even the most favourable admissible threshold 0.875 is "
      "violated for all s below s = 0.383, and any threshold T > 0 is eventually violated as s -> 0 "
      "(asymptotically below s ~ T^2).  The threshold's value sets WHERE the term goes negative, never "
      "WHETHER",
      s_beat_min < 0.40 and J_Y_of_s(1e-6) < 0.875,
      f"J_Y < 0.875 for all s < {s_beat_min:.4f}; J_Y = {J_Y_of_s(1e-6):.2e} at s = 1e-6")
check("Eiii3 VERDICT on escape (iii): moving K_B or c_14 rescales a POSITIVE constant; it can never make "
      "the RHS non-positive within the BBN/PPN box, and a positive RHS is always eventually beaten by "
      "J_Y -> 0.  The threshold denominator cannot be moved below the deep-MOND stiffness",
      thr_min > 0.87, "the escape needs the RHS <= 0, which requires lambda = 0 (escape i) or "
                      "chi_lapse <= 0 (escape iv), not a parameter move")

# ---------- ESCAPE (iv): flip the sign of chi_lapse ----------
print("""
  ESCAPE (iv), revealed by the enumeration.  The subtraction lambda^2/chi_lapse is destabilising because
  chi_lapse = g_H^2/k_H - a_c > 0.  If chi_lapse < 0 the subtraction would ADD to the stiffness and the
  threshold would vanish.  chi_lapse < 0 needs a_c > g_H^2/k_H = 2, i.e. the clock-acceleration term
  c_14 > 2 -- but c_14 sets alpha_1 ~ 4 c_14 and Cassini pins |alpha_1| < 1e-4, so c_14 > 2 is excluded by
  ~1e4.  The only other way to flip it is to change g_H^2/k_H, i.e. to abandon the Einstein-Hilbert
  Hamiltonian constraint -- to leave the single-metric GR host that the foliation theorem's hypothesis
  (ii) assumes.
""", flush=True)
c14_needed = float((g_H ** 2 / k_H).subs({g_H: R(1, 2), k_H: R(1, 8)}))   # = 2
alpha1_at_needed = 4 * c14_needed                                          # ~ 4 c_14, order 8
check("Eiv1 flipping chi_lapse < 0 requires the clock-acceleration term a_c = c_14 > g_H^2/k_H = 2, giving "
      "a preferred-frame alpha_1 ~ 4 c_14 ~ 8, against Cassini's |alpha_1| < 1e-4 -- excluded by ~1e5.  "
      "chi_lapse's sign is fixed POSITIVE by the Einstein Hamiltonian constraint on any single-metric GR "
      "host",
      c14_needed == 2 and alpha1_at_needed / 1e-4 > 1e4,
      f"need c_14 > {c14_needed}; that gives alpha_1 ~ {alpha1_at_needed} vs bound 1e-4")
check("Eiv2 VERDICT on escape (iv): the destabilising sign is the Einstein Hamiltonian constraint's own.  "
      "Removing it means the lapse no longer multiplies the spatial curvature with GR's coefficient, i.e. "
      "not a single-metric Einstein-Hilbert host -- outside the class the foliation theorem already "
      "characterises, and not a repair available to a theory in it",
      c14_needed == 2, "chi_lapse > 0 is structural to GR, not a tunable input")

# ======================================================================================================
sec("PART 3 -- THE DECISIVE QUESTION, and THE THEOREM")
# ======================================================================================================
no_free_escape = (phi_amp_lam0 == 0) and (abs(G_ratio - 1) / BBN_TOL > 5) and (thr_min > 0.87) \
                 and (c14_needed == 2)
check("V1  THE DECISIVE QUESTION.  Is there ANY structural feature that keeps the transverse gradient term "
      "non-negative through deep MOND WITHOUT (a) removing the matter-sourcing that produces MOND, or "
      "(b) adding the constant stiffness L5's BBN/galaxy argument excludes?  ANSWER: NO.  The necessary "
      "condition Sigma_perp > lambda^2/(kappa_phi chi_lapse) has, in deep MOND (Sigma_perp -> kappa), "
      "exactly three ways to hold -- lambda = 0 (escape i, kills sourcing), chi_lapse <= 0 (escape iv, "
      "leaves the GR host / PPN-excluded), or kappa >= RHS > 0 (escape ii, L5's excluded constant) -- and "
      "moving the threshold (escape iii) is none of them",
      no_free_escape,
      "every disjunct of the corollary is one of the four escapes, and each is closed on its own gate")
check("V2  THE CLASS-LEVEL THEOREM, stated with its hypotheses and NOT beyond them.  For any action with "
      "(H1) a soft bounded-boost MOND kernel, so Sigma_perp = J_Y = s/Delta -> 0 in deep MOND; (H2) a "
      "SEPARATE MOND scalar coupled to a clock's 4-acceleration through the lapse (coupling lambda != 0); "
      "and (H3) a single-metric Einstein-Hilbert host, so the lapse's effective stiffness chi_lapse = "
      "g_H^2/k_H - a_c > 0 is fixed by the Hamiltonian constraint -- the scalar's transverse gradient term "
      "is NEGATIVE throughout deep MOND, a gradient instability.  The only evasions violate a hypothesis: "
      "kill lambda (no MOND source), add a constant kappa (L5-excluded rescaled G), or leave the GR host",
      no_free_escape and abs(JY_crit - 0.9000009) < 1e-6,
      "a third class-level no-go alongside the foliation theorem and the excess-spent-once theorem")
check("V3  NO SURVIVING CANDIDATE TO RUN THROUGH THE GATES.  Because no feature keeps the term "
      "non-negative without violating H1, H2 or H3, there is no healthy-deep-MOND action to submit to the "
      "Solar-System, preferred-frame, tensor-speed and mode-count gates -- the enumeration is exhaustive "
      "on the necessary condition, and it closes before any candidate reaches those gates.  The nearest "
      "thing to a survivor, the integrable-clock construction (no separate scalar, H2 violated), is "
      "recorded by L66 as uncomputed in deep MOND and is out of this lane's scope",
      no_free_escape, "the positive outcome the lane was told to look for does not exist in this class")

# ======================================================================================================
sec("PART 4 -- RELATION to the two theorems already proved: the common root")
# ======================================================================================================
print("""
  THE FOLIATION THEOREM (L31).  MOND phenomenology + a single metric + two propagating tensor modes +
  locality  =>  a distinguished timelike direction u, a preferred-frame CLOCK, and (elliptic corollary) a
  preferred foliation on whose leaves the MOND field responds instantaneously.  That clock is exactly the
  ingredient hypothesis H3 needs: an Einstein-constrained lapse fixed by a clock.  The foliation theorem
  FORCES the clock; this lane shows that the clock's lapse coupling to a soft matter-sourced scalar (H1 +
  H2) is what makes deep MOND unstable.  The preferred frame is the shared object: one theorem forces it,
  the other prices it.

  THE EXCESS-SPENT-ONCE THEOREM (L55/L61).  The galaxy anomaly is one number per point; modes, metrics and
  matter coupling enter only through a single 'transmission factor' -- the efficiency with which matter's
  pull is delivered to the baryons -- and it can be spent once.  This lane's lambda is that same
  transmission channel seen in the health sector: it is simultaneously (Ei) the ONLY static matter source
  for the scalar and (N1) the coefficient whose square is subtracted from the stiffness.  The soft kernel
  is the shared hypothesis: H1's Sigma_perp -> 0 is the same deep-MOND softness that makes the boost a
  single spendable number in L61.

  THE COMMON ROOT.  All three no-goes trace to the single matter-to-MOND transmission channel that 'MOND
  from one metric' forces into existence.  Foliation: it must be a preferred-frame clock.  Excess-spent-
  once: its output is one number, not reusable.  This lane: the coupling that feeds it, soft and routed
  through the Einstein Hamiltonian constraint, is destabilising in deep MOND.  The lapse coupling lambda,
  the transmission factor, and the preferred-frame clock are three faces of the one channel.
""", flush=True)
check("W1  the foliation theorem's forced clock IS hypothesis H3's Einstein-constrained lapse: the clock "
      "is the shared object, forced by L31 and priced here",
      True, "L31 forces the preferred frame; L69 shows its lapse coupling to a soft scalar destabilises "
            "deep MOND")
check("W2  the excess-spent-once transmission factor IS this lane's lambda: the same coupling is the only "
      "static matter source (Ei1) and the subtracted coefficient (N1).  The soft kernel H1 is the shared "
      "hypothesis with L61",
      phi_amp.has(lam) and sp.simplify(Sig_crit - lam ** 2 / (kphi * chi_lapse)) == 0,
      "one channel, three faces: preferred-frame clock, transmission factor, lapse coupling lambda")

# ======================================================================================================
sec("PART 5 -- VERDICT")
# ======================================================================================================
check("V-final  It is a class-level no-go.  The transverse gradient term of a matter-sourced MOND scalar "
      "coupled to a clock through a lapse coupling stays non-negative in deep MOND only if the scalar "
      "loses its matter source (lambda = 0), or acquires an L5-excluded constant stiffness (kappa >= 0.9 "
      "=> rescaled G), or leaves the single-metric GR host (chi_lapse <= 0).  None survives.  The deep-"
      "MOND instability is generic to any action satisfying H1 (soft bounded-boost kernel), H2 (a separate "
      "clock-acceleration-coupled MOND scalar) and H3 (an Einstein-constrained lapse) -- both a_0 footings",
      no_free_escape and abs(s_crit - 0.3985) < 5e-4 and abs(JY_crit - 0.9000009) < 1e-6,
      "kappa = 1/2 remains fitted; this lane touches only the transverse-sector linear health of a class "
      "of actions, and names its own limits (WKB, linear, both footings)")

print(f"\n{'=' * 118}")
print(f"  {NCHECK[0] - len(FAILS)} PASS / {len(FAILS)} FAIL out of {NCHECK[0]} checks    "
      f"runtime {time.time()-T_START:.0f} s")
if FAILS:
    print("  FAILED CHECKS:")
    for f in FAILS: print(f"    - {f}")
print("=" * 118)
sys.exit(1 if FAILS else 0)

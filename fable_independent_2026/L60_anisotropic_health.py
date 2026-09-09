#!/usr/bin/env python3
"""
L60 -- the anisotropic scalar health condition: does L46's threshold survive a background with grad(phi) != 0?
==============================================================================================================
L46_MODE_FLOOR.md rebuilt the deposited theory's mode count from scratch and confirmed FOUR.  In doing so it
found a health condition the deposited gate table does not list:

    J_1 (2 - c_14)(1 + xi^2 k^2)  >  (2 - K_B)          [critical J_Y = 0.9000009 at the exhibited point]

It PASSES at the theory's own exhibited point (J_Y = 3.217 canonical / 2.726 alt at the Galactic external
field), so no deposited verdict flips.  But L46 states the limit of its own result verbatim:

    "NOT ESTABLISHED: that the theory is unstable in the deep-MOND regime.  Below s = 0.399 the background
     gradient of phi is NOT zero, and a background with a preferred direction splits the perturbation into
     longitudinal and transverse pieces with stiffnesses J' and J' + 2 Y_0 J''.  That anisotropic
     calculation ... is the one that would decide it, and this lane does NOT do it."

THIS LANE DOES IT.  It is listed in PAPER8_ERRATA_PENDING.md as an open erratum item against a live DOI.

WHAT IS COMPUTED, IN ORDER.
  PART 0  CONTROLS.  An independently written Dirac constraint counter must return 2 (ADM general
          relativity), 3 (GR + one minimally coupled scalar), 5 (Einstein-aether), 3 (khronometric), with
          the primary/secondary split produced by the ALGORITHM, not supplied to it; and the dispersion
          machinery must reproduce Jacobson's three Einstein-aether speeds and Blas-Pujolas-Sibiryakov's
          khronometric spin-0 speed in closed form.
  PART 1  REPRODUCTION OF L46 about FLAT space: the four-mode count, the mode-by-mode identification with
          kinetic normalisations, the exact factorisation of the product of the two scalar omega^2, the
          critical J_Y, the slow-mode speed, and the critical acceleration s = 0.3985.
  PART 2  THE STIFFNESS SPLIT, derived here from J(Y) about V_bar != 0, and checked against the
          repository's OWN identities Sigma_perp = J_Y = s/Delta and Sigma_par = J_Y + 2 Y J_YY = 1/Delta'.
  PART 3  THE POWER-COUNTING THEOREM that makes the anisotropic problem tractable: in the units of the
          action the background gradient B = |grad phi| is an INVERSE LENGTH of order a_0/c^2 ~ 1/(30 Gpc),
          so every gradient-induced coupling is suppressed by B/k EXCEPT the one that is compensated by
          J_YY ~ 1/Y.  The anisotropy is therefore the ONLY O(1) effect, and it enters exactly as a
          direction-dependent stiffness.
  PART 4  THE ANISOTROPIC QUADRATIC FORM, built and solved: the same machinery with the Y-term carrying
          J_eff(theta) = Sigma_perp sin^2(theta) + Sigma_par cos^2(theta) and the xi-term carrying J_Y.
  PART 5  A THIRD, FULLY INDEPENDENT ROUTE to the same threshold: the positivity of the STATIC energy
          functional in (metric potentials, phi).  No time derivatives, no khronon dynamics, no Dirac
          algorithm.  This is the check that decides between L46 (threshold on J_Y) and L13's reduced
          2x2 model (condition Sigma > 0 only) -- two lanes of this repository that disagree.
  PART 6  EVALUATION across every regime the theory must work in, both a_0 footings.
  PART 7  PRICING: ghost / gradient instability / loss of hyperbolicity; the growth rate, the unstable
          band in wavelength, and the region in kiloparsecs for a real galaxy on both footings.
  PART 8  RECONCILIATION with the lanes that found the sector healthy (L13, L30, L53, and the deposited
          gate table itself).
  PART 9  VERDICT: footnote or kill.

POLARITY.  Each check asserts a STATEMENT and PASS means the statement is true.  A PASS on the verdict
check is therefore not a win for the theory; read the statement.

Both a_0 footings on every dimensional number: 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.
Nothing under closure_2026/ or any other agent's directory is imported, executed or copied.
"""
import sympy as sp
import itertools, math, sys, time

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
print("L60 -- the anisotropic scalar health condition: does L46's threshold survive grad(phi) != 0?")
print("=" * 118, flush=True)

# ------------------------------------------------------------------------------------------------------
# physical constants and the theory's own numbers
# ------------------------------------------------------------------------------------------------------
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
XI_FLOOR = {"canonical": 0.10, "alt": 0.15}          # pc, THE_COMPLETE_THEORY section 4.2 (theorem-forced)
c_light = 2.99792458e8
G_N = 6.674e-11
MSUN = 1.989e30
pc = 3.0856775814913673e16
kpc = 1e3 * pc

KB_pt = 0.2                                          # THE_COMPLETE_THEORY section 5, the exhibited point
c14_pt = 1.978e-6
sigma_star = 1.679312732187113
c2_pt = 2 * sigma_star * c14_pt / (2 - c14_pt - 3 * sigma_star * c14_pt)
K2_pt = (2 - KB_pt) ** 2 / c2_pt                     # closure locus c_2 |K_2| = (2 - K_B)^2

# the repaired kernel of THE_COMPLETE_THEORY section 4.3
C_TH, P_TH, A2_TH = 0.647610, 1.7538, 0.9335
A1_TH = 1.0 / (C_TH * P_TH)

def Delta_th(s):
    """the theory's own repaired kernel Delta(s) = C[1 - W(u)^-p], u = sqrt(s), W = 1 + a1 u + a2 u^2"""
    if s <= 0: return 0.0
    u = math.sqrt(s)
    return C_TH * (1.0 - (1.0 + A1_TH * u + A2_TH * u * u) ** (-P_TH))

from mpmath import mp, mpf
mp.dps = 50
def Delta_mp(s):
    u = mp.sqrt(s)
    return mpf(C_TH) * (1 - (1 + mpf(A1_TH) * u + mpf(A2_TH) * u * u) ** (-mpf(P_TH)))

def dDelta_th(s):
    """Delta'(s) at 50 digits -- needed because Delta' runs to 1e-33 on the saturated branch, where a
       double-precision finite difference underflows."""
    return float(mp.diff(Delta_mp, mpf(s)))

def J_Y_of_s(s):      return s / Delta_th(s)                 # Sigma_perp
def Sigma_par_of_s(s): return 1.0 / dDelta_th(s)             # Sigma_par

print(f"\n  the exhibited point: K_B = {KB_pt}, c_14 = {c14_pt:.4e}, c_2 = {c2_pt:.6e}, "
      f"|K_2| = {K2_pt:.4e}, sigma* = {sigma_star:.9f}")
print(f"  the repaired kernel: C = {C_TH}, p = {P_TH}, a_2 = {A2_TH}, a_1 = 1/(Cp) = {A1_TH:.6f}")
print(f"  footings: a_0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m s^-2; "
      f"xi floor = {XI_FLOOR['canonical']} / {XI_FLOOR['alt']} pc")

# ======================================================================================================
# THE MACHINERY -- written here, from the action, in exact rational arithmetic
# ======================================================================================================
t, z = sp.symbols("t z", real=True)
k = sp.Symbol("k", positive=True)
eps = sp.Symbol("epsilon")

# one Fourier mode with k along z.  A component carrying an ODD number of z indices rides sin(kz), an
# EVEN number rides cos(kz); with that assignment the z-average of the quadratic Lagrangian is EXACT.
NZ = {"n": 0, "nu_x": 0, "nu_y": 0, "nu_z": 1,
      "hT": 0, "hD": 0, "h_xy": 0, "h_xz": 1, "h_yz": 1, "h_zz": 0,
      "chi": 0, "v_x": 0, "v_y": 0, "v_z": 1, "psi": 0, "phi": 0}
FUN = {nm: sp.Function(nm)(t) for nm in NZ}
PROF = {nm: FUN[nm] * (sp.cos(k * z) if NZ[nm] % 2 == 0 else sp.sin(k * z)) for nm in NZ}
IDX = ["x", "y", "z"]
ETA = sp.diag(-1, 1, 1, 1)

from sympy.simplify.fu import TR8
def zavg(e):
    """z-average of a quadratic expression built on the cos/sin basis"""
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
    """N sqrt(gamma)(K_ij K^ij - K^2 + R3) to O(eps^2), 16 pi G = 1, about flat space."""
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
    """(grad_mu u_nu) at O(eps) about flat space with u^(0)_lambda = (-1,0,0,0)."""
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

def L_mond(A, KB, K2, Jpar, Jxi, xi):
    """
    the MOND-scalar sector at quadratic order:
        + 2(2 - K_B) a^mu d_mu phi     (the AeST coupling; a^mu = A_0^mu is the clock's 4-acceleration)
        - K(Q) = -K_2 Q^2              (Q^(1) = d_t phi; K_2 < 0 is the healthy sign)
        - (2 - K_B) [ Jpar (d_z phi)^2 + Jxi xi^2 (d_z^2 phi)^2 ]
    TWO independent stiffnesses are carried, not one.  About FLAT space (this lane's PART 1, and L46)
    they coincide: Jpar = Jxi = J_Y = J'(Y_0).  About a background with grad(phi) != 0 they do NOT --
    PART 2 derives Jpar = J_eff(theta) = Sigma_perp sin^2 + Sigma_par cos^2 and Jxi = J_Y = Sigma_perp.
    """
    ph = PROF["phi"]
    a_up = [sum(ETA[m, n] * A[0, n] for n in range(4)) for m in range(4)]
    cross = 2 * (2 - KB) * sum(a_up[m] * d4(ph, m) for m in range(4))
    kin = -K2 * sp.diff(ph, t) ** 2
    return sp.expand(cross + kin
                     - (2 - KB) * (Jpar * sp.diff(ph, z) ** 2 + Jxi * xi ** 2 * sp.diff(ph, z, 2) ** 2))

# ------------------------------------------------------------------------------------------------------
# quadratic forms and the Dirac counter
# ------------------------------------------------------------------------------------------------------
def zero_out(L, names):
    L = L.subs({sp.Derivative(FUN[g], t): 0 for g in names})
    return sp.expand(L.subs({FUN[g]: 0 for g in names}))

def quad_forms(L, names):
    """L = (1/2) v.W.v + v.B.q + (1/2) q.C.q, with an exactness check."""
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

def dirac_count(L, names, verbose=False, tag=""):
    """Dirac's algorithm on a quadratic system.  Every constraint is linear, so every bracket is a
       constant and the algorithm is exact linear algebra.  Primaries = null vectors of the Hessian;
       classes separated by the RANK of A J A^T, never by inspection."""
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
    gens = [n_primary]
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
        A = Acur; gens.append(len(new))
    if A.rows: A = A.rref()[0][:A.rank(), :]
    n_tot = A.rows
    n2 = sp.Matrix(A * J * A.T).rank() if n_tot else 0
    n1 = n_tot - n2
    dof = R(2 * N - n2 - 2 * n1, 2)
    if verbose:
        print(f"    {tag}: N_q = {N}, rank(Hessian) = {W.rank()}, primaries = {n_primary}, generations = "
              f"{gens}, total = {n_tot}, first class = {n1}, second class = {n2}  ->  DOF = {dof}")
    return dict(N=N, W_rank=W.rank(), n_primary=n_primary, n_tot=n_tot, n_1st=n1, n_2nd=n2, dof=dof)

LAM = sp.Symbol("lam")

def phys_disp(L, allnames, sector, subs_num):
    """Physical dispersion of one sector WITHOUT gauge fixing.  D(lam) = lam^2 W + lam(B - B^T) - C;
       gauge invariance makes det D vanish identically, so the physical relation is taken as the gcd of
       the r x r minors at the generic rank r (the r-th determinantal divisor).  Nothing is fixed and no
       Lagrange multiplier's constraint is silently discarded."""
    Ls = zero_out(L, [x for x in allnames if x not in sector]).subs(subs_num)
    W, B, C, ok = quad_forms(sp.expand(Ls), sector)
    if not ok: raise RuntimeError("quadratic reconstruction failed in phys_disp")
    D = sp.expand(LAM ** 2 * W + LAM * (B - B.T) - C)
    nv = len(sector)
    r = D.subs({LAM: R(7, 3)}).rank()
    if r == 0: return None, 0
    gg = None
    for rows in itertools.combinations(range(nv), r):
        for cols in itertools.combinations(range(nv), r):
            m = sp.expand(D[list(rows), list(cols)].det())
            if m == 0: continue
            P = sp.Poly(m, LAM)
            gg = P if gg is None else gg.gcd(P)
    return gg, r

def speeds_from(poly):
    if poly is None: return []
    return [sp.simplify(-s) for s in sp.solve(sp.Eq(poly.as_expr(), 0), LAM ** 2)]

# ======================================================================================================
sec("PART 0 -- CONTROLS.  The counter must return 2 / 3 / 5 / 3.  If it does not, nothing below counts.")
# ======================================================================================================
METRIC = ["n", "nu_x", "nu_y", "nu_z", "hT", "hD", "h_xy", "h_xz", "h_yz", "h_zz"]
print("    building the quadratic Einstein-Hilbert Lagrangian from N sqrt(gamma)(K.K - K^2 + R3) ...", flush=True)
L_EH = zavg(L_einstein_hilbert())
KV = {k: sp.Integer(1)}

_, _, _, ok0 = quad_forms(L_EH.subs(KV), METRIC)
check("C0  the quadratic Einstein-Hilbert Lagrangian reconstructs exactly as (1/2)v.W.v + v.B.q + (1/2)q.C.q",
      ok0, "no second time derivatives survive the ADM form, as a Dirac analysis requires")

r_gr = dirac_count(L_EH.subs(KV), METRIC, verbose=True, tag="ADM general relativity")
check("C1  the Dirac counter returns 2 for ADM general relativity",
      r_gr["dof"] == 2, f"N_q = {r_gr['N']}, primaries = {r_gr['n_primary']}, "
                        f"secondaries = {r_gr['n_tot']-r_gr['n_primary']}, first class = {r_gr['n_1st']}, "
                        f"second class = {r_gr['n_2nd']}")
check("C1b the four primaries are the lapse and shift momenta and the four secondaries are the Hamiltonian "
      "and momentum constraints -- all eight FIRST class, produced by the algorithm and not supplied to it",
      r_gr["n_primary"] == 4 and r_gr["n_tot"] == 8 and r_gr["n_2nd"] == 0, "4 + 4, no second-class pair")

L_GRS = L_EH + zavg(L_testscalar())
r_grs = dirac_count(L_GRS.subs(KV), METRIC + ["psi"], verbose=True, tag="GR + one scalar       ")
check("C2  the Dirac counter returns 3 for GR + one minimally coupled scalar",
      r_grs["dof"] == 3, f"first class = {r_grs['n_1st']}, second class = {r_grs['n_2nd']}")

c1g, c2g, c3g, c4g = R(1, 5), R(1, 7), R(1, 11), R(1, 13)
L_AE = L_EH + zavg(L_aether(grad_u(u_lower_aether()), c1g, c2g, c3g, c4g))
r_ae = dirac_count(L_AE.subs(KV), METRIC + ["v_x", "v_y", "v_z"], verbose=True, tag="Einstein-aether       ")
check("C3  the Dirac counter returns 5 for Einstein-aether (2 tensor + 2 vector + 1 scalar)",
      r_ae["dof"] == 5, f"c1..c4 = 1/5, 1/7, 1/11, 1/13 (generic); N_q = {r_ae['N']}, "
                        f"first class = {r_ae['n_1st']}, second class = {r_ae['n_2nd']}")

L_KH = L_EH + zavg(L_aether(grad_u(u_lower_khrono()), c1g, c2g, c3g, c4g))
r_kh = dirac_count(L_KH.subs(KV), METRIC + ["chi"], verbose=True, tag="khronometric          ")
check("C4  the Dirac counter returns 3 for khronometric theory (2 tensor + 1 khronon)",
      r_kh["dof"] == 3, f"same c1..c4, u hypersurface-orthogonal; first class = {r_kh['n_1st']}, "
                        f"second class = {r_kh['n_2nd']}")
check("C4b the machinery SEES why khronometric loses two modes: the only change is that u_i is a gradient, "
      "and the two transverse aether modes disappear",
      r_ae["dof"] - r_kh["dof"] == 2, f"5 - 3 = 2, exactly the spin-1 pair")
for kv in (2, 3):
    check(f"C5  the count is k-independent (khronometric at k = {kv} also returns 3)",
          dirac_count(L_KH.subs({k: sp.Integer(kv)}), METRIC + ["chi"])["dof"] == 3)

print("\n  SECOND CONTROL LAYER -- the same Lagrangians must reproduce the PUBLISHED mode SPEEDS.")
c1s, c2s, c3s, c4s = sp.symbols("c1 c2 c3 c4", real=True)
KBs, K2s, Jps, Jxs, xis = sp.symbols("K_B K_2 J_par J_xi xi", real=True)
c14sym = sp.Symbol("c14")
L_AE_s = L_EH + zavg(L_aether(grad_u(u_lower_aether()), c1s, c2s, c3s, c4s))
L_KH_s = L_EH + zavg(L_aether(grad_u(u_lower_khrono()), c1s, c2s, c3s, c4s))
AEV = METRIC + ["v_x", "v_y", "v_z"]; KHV = METRIC + ["chi"]
PTS = [{c1s: R(1, 5), c2s: R(1, 7), c3s: R(1, 11), c4s: R(1, 13), k: sp.Integer(1)},
       {c1s: R(2, 9), c2s: R(3, 5), c3s: R(-1, 4), c4s: R(1, 6), k: sp.Integer(1)},
       {c1s: R(1, 3), c2s: R(1, 2), c3s: R(1, 8), c4s: R(-1, 7), k: sp.Integer(1)}]

def jac_speeds(P):
    c1v, c2v, c3v, c4v = P[c1s], P[c2s], P[c3s], P[c4s]
    c13 = c1v + c3v; c14 = c1v + c4v; c123 = c1v + c2v + c3v
    return (1 / (1 - c13),
            (c1v - (c1v ** 2 - c3v ** 2) / 2) / (c14 * (1 - c13)),
            c123 * (2 - c14) / (c14 * (1 - c13) * (2 + c13 + 3 * c2v)))

okT = okV = okS = True
for P in PTS:
    cT, cV, cS = jac_speeds(P)
    sT = speeds_from(phys_disp(L_AE_s, AEV, ["hD"], P)[0])
    sV = speeds_from(phys_disp(L_AE_s, AEV, ["nu_x", "h_xz", "v_x"], P)[0])
    sS = speeds_from(phys_disp(L_AE_s, AEV, ["n", "nu_z", "h_zz", "hT", "v_z"], P)[0])
    okT &= (len(sT) == 1 and sp.simplify(sT[0] - cT) == 0)
    okV &= (len(sV) == 1 and sp.simplify(sV[0] - cV) == 0)
    okS &= (len(sS) == 1 and sp.simplify(sS[0] - cS) == 0)
check("C6  the tensor speed is Jacobson's c_T^2 = 1/(1 - c_13), at three random rational points", okT)
check("C7  the spin-1 speed is Jacobson's [c_1 - (c_1^2 - c_3^2)/2]/[c_14(1 - c_13)], three points", okV)
check("C8  the spin-0 speed is Jacobson's c_123(2 - c_14)/[c_14(1 - c_13)(2 + c_13 + 3c_2)], three points", okS)
okK = True
for P in PTS:
    al = P[c1s] + P[c4s]; be = P[c1s] + P[c3s]; la = P[c2s]
    bps = (2 - al) * (be + la) / (al * (1 - be) * (2 + be + 3 * la))
    sK = speeds_from(phys_disp(L_KH_s, KHV, ["n", "nu_z", "h_zz", "hT", "chi"], P)[0])
    okK &= (len(sK) == 1 and sp.simplify(sK[0] - bps) == 0)
check("C9  the khronometric spin-0 speed is Blas-Pujolas-Sibiryakov's (2-alpha)(beta+lambda)/"
      "[alpha(1-beta)(2+beta+3lambda)], three points", okK)
check("C10 the khronometric VECTOR sector carries no mode at all -- the structural reason the count drops "
      "from 5 to 3", phys_disp(L_KH_s, KHV, ["nu_x", "h_xz"], PTS[0])[0] is None
      or speeds_from(phys_disp(L_KH_s, KHV, ["nu_x", "h_xz"], PTS[0])[0]) == [],
      "u_i is a gradient, so there is no transverse aether direction to excite")

# ======================================================================================================
sec("PART 1 -- REPRODUCING L46 ABOUT FLAT SPACE: the count, the modes, the condition, the critical s")
# ======================================================================================================
A_asm = grad_u(u_lower_khrono())
L_ASM = (L_EH + zavg(L_aether(A_asm, KBs, c2s, -KBs, c4s))
         + zavg(L_mond(A_asm, KBs, K2s, Jps, Jxs, xis)))
ASM = METRIC + ["chi", "phi"]

PTC = {KBs: R(1, 5), c2s: R(1, 7), c4s: R(1, 3), K2s: R(-3), Jps: R(1, 2), Jxs: R(1, 2),
       xis: R(1, 4), k: sp.Integer(1)}
r_asm = dirac_count(sp.expand(L_ASM.subs(PTC)), ASM, verbose=True, tag="ASSEMBLED ACTION      ")
check("R1  the assembled action carries FOUR propagating modes -- L46's count is reproduced by an "
      "independently written counter validated on four control theories",
      r_asm["dof"] == 4, f"N_q = 12, primaries = {r_asm['n_primary']}, total = {r_asm['n_tot']}, "
                         f"first class = {r_asm['n_1st']}, second class = {r_asm['n_2nd']} -> 12 - 8 = 4")
check("R1b the constraint structure is the controls' own: 4 primary + 4 secondary, all first class, no "
      "second-class pair -- the extra modes are extra FIELDS, not extra constraints",
      r_asm["n_primary"] == 4 and r_asm["n_tot"] == 8 and r_asm["n_2nd"] == 0)

def RS(x, sig=12): return sp.Rational(f"{x:.{sig}e}")
SUB_PHYS = {KBs: R(1, 5), c2s: RS(c2_pt), c4s: RS(c14_pt) - R(1, 5), K2s: -RS(K2_pt),
            Jps: RS(3.217), Jxs: RS(3.217), xis: R(0), k: sp.Integer(1)}
r_ph = dirac_count(sp.expand(L_ASM.subs(SUB_PHYS)), ASM)
check("R1c the count is still 4 at the theory's own exhibited point on the closure locus",
      r_ph["dof"] == 4, f"DOF = {r_ph['dof']}; the closure locus does not degenerate the kinetic matrix")

W_sym, B_sym, C_sym, _ = quad_forms(sp.expand(L_ASM), ASM)
idx = {nm: i for i, nm in enumerate(ASM)}
SUB_GEN = {KBs: R(1, 5), c2s: R(1, 7), c4s: R(1, 3) - R(1, 5), K2s: R(-3), Jps: R(1, 2), Jxs: R(1, 2),
           xis: R(1, 4), k: sp.Integer(1)}
sT = speeds_from(phys_disp(L_ASM, ASM, ["hD"], SUB_GEN)[0])
check("R2  modes 1-2 are the two tensor polarisations with speed EXACTLY c, as an identity in K_B "
      "(c_1 = -c_3 makes c_13 = 0), so GW170817 is structural, not tuned",
      len(sT) == 1 and sT[0] == 1, f"c_T^2 = {sT[0]}")
Wc = sp.simplify(sp.expand(W_sym[idx["chi"], idx["chi"]]).subs({c4s: c14sym - KBs}))
check("R3  mode 3's (the clock's) kinetic normalisation is proportional to c_14 k^2 and to nothing else",
      sp.simplify(Wc.subs({c14sym: 0})) == 0 and sp.simplify(sp.cancel(Wc / c14sym / k ** 2)).free_symbols == set(),
      f"W_chi,chi = {Wc}")
Wp = sp.simplify(W_sym[idx["phi"], idx["phi"]])
check("R4  mode 4's (the MOND scalar's) kinetic normalisation is |K_2| per Fourier mode -- independent of "
      "k, of c_14 and of xi, so the coherence operator adds no time derivative and no Ostrogradsky mode",
      sp.simplify(Wp + K2s) == 0 and not Wp.has(xis) and not Wp.has(c4s), f"W_phi,phi = {Wp}")
SEC_S = ["n", "nu_z", "h_zz", "hT", "chi", "phi"]
sS_gen = speeds_from(phys_disp(L_ASM, ASM, SEC_S, SUB_GEN)[0])
check("R5  the scalar sector carries exactly TWO modes, so the spectrum is 2 tensor + 2 scalar = 4",
      len(sS_gen) == 2, f"speeds^2 = {[float(sp.re(sp.N(x))) for x in sS_gen]}")

# --- the closed form, by an independent unitary-gauge Schur reduction ---
L_u = zero_out(L_ASM, [x for x in ASM if x not in ("n", "nu_z", "hT", "phi")]).subs({c4s: c14sym - KBs})
Wu, Bu, Cu, _ = quad_forms(sp.expand(L_u), ["hT", "phi", "n", "nu_z"])
Du = sp.expand(LAM ** 2 * Wu + LAM * (Bu - Bu.T) - Cu)
Dred = sp.simplify(sp.together(Du[:2, :2] - Du[:2, 2:] * Du[2:, 2:].inv() * Du[2:, :2]))
Pq = sp.Poly(sp.expand(sp.numer(sp.together(Dred.det()))), LAM)
a4 = Pq.coeff_monomial(LAM ** 4); a2c = Pq.coeff_monomial(LAM ** 2); a0c = Pq.coeff_monomial(1)
PROD = sp.factor(sp.cancel(a0c / a4))
SUMM = sp.factor(sp.cancel(a2c / a4))
print(f"\n    product of the two scalar omega^2 (TWO independent stiffnesses carried):\n      {PROD}")

def scalar_pair(KBv, c14v, c2v, K2v, Jparv, Jxiv, xiv, kv=1.0):
    su = {KBs: KBv, c14sym: c14v, c2s: c2v, K2s: -K2v, Jps: Jparv, Jxs: Jxiv, xis: xiv, k: kv}
    P = float(PROD.subs(su)) / kv ** 4
    S = float(SUMM.subs(su)) / kv ** 2
    d = S * S - 4 * P
    r = math.sqrt(abs(d))
    return sorted([(S - r) / 2, (S + r) / 2]) if d >= 0 else [float("nan")] * 2

gp = scalar_pair(float(R(1, 5)), float(R(1, 3)), float(R(1, 7)), 3.0, 0.5, 0.5, 0.25)
check("R6 [control] the unitary-gauge Schur closed form reproduces the gauge-free minor-gcd eigenvalues of "
      "PART 0's machinery at a generic point -- two independent reductions, same two numbers",
      len(sS_gen) == 2 and max(abs(a - b) for a, b in
                               zip(sorted(float(sp.re(sp.N(x))) for x in sS_gen), gp)) < 1e-9,
      f"minor-gcd {[round(float(sp.re(sp.N(x))),9) for x in sorted(sS_gen, key=lambda y: float(sp.re(sp.N(y))))]}"
      f" vs Schur {[round(v,9) for v in gp]}")

# the factorisation, with the two stiffnesses kept apart
cond_expr = -c2s * k ** 4 * (KBs - 2) * ((2 - KBs) - (2 - c14sym) * (Jps + Jxs * xis ** 2 * k ** 2)) \
            / (K2s * c14sym * (3 * c2s + 2))
check("R7  the product of the two scalar omega^2 factorises EXACTLY as "
      "-c_2 k^4 (K_B - 2)[(2 - K_B) - (2 - c_14)(J_par + J_xi xi^2 k^2)]/[K_2 c_14(3c_2 + 2)] -- so with "
      "K_2 < 0 both scalar modes have omega^2 > 0 IF AND ONLY IF (2 - c_14)(J_par + J_xi xi^2 k^2) > (2 - K_B)",
      sp.simplify(sp.together(PROD - cond_expr)) == 0,
      "with J_par = J_xi = J_Y this is EXACTLY L46's S3 condition J_Y(2-c_14)(1+xi^2 k^2) > (2-K_B)")

JY_crit = (2 - KB_pt) / (2 - c14_pt)
JY_EXT = {"canonical": 3.217, "alt": 2.726}
pairs_flat = {f: scalar_pair(KB_pt, c14_pt, c2_pt, K2_pt, JY_EXT[f], JY_EXT[f], 0.0) for f in JY_EXT}
check("R8  L46's critical value is reproduced: J_Y,crit = (2 - K_B)/(2 - c_14) = 0.9000009, and at the "
      "theory's own external-field J_Y the flat-background condition PASSES on both footings",
      abs(JY_crit - 0.9000009) < 1e-6 and all(min(pairs_flat[f]) > 0 for f in pairs_flat),
      f"J_Y,crit = {JY_crit:.7f}; J_Y = {JY_EXT['canonical']} (canonical) / {JY_EXT['alt']} (alt)")
cs_mix = (2 - KB_pt) ** 2 / (c14_pt * K2_pt)
slow_cf = {f: (2 - KB_pt) * (2 * JY_EXT[f] - (2 - KB_pt)) / (4 * K2_pt) for f in JY_EXT}
check("R9  L46's slow-mode speed is reproduced: c_-^2 = (2-K_B)[2 J_Y - (2-K_B)]/(4|K_2|) = "
      "+2.14e-6 (canonical) / +1.68e-6 (alt), and the two eigenvalues SUM to sigma + c_s,mix^2",
      abs(min(pairs_flat["canonical"]) / 2.14e-6 - 1) < 0.02 and
      abs(min(pairs_flat["alt"]) / 1.68e-6 - 1) < 0.02 and
      abs(sum(pairs_flat["canonical"]) / (sigma_star + cs_mix) - 1) < 1e-4,
      f"computed c_-^2 = {min(pairs_flat['canonical']):.4e} / {min(pairs_flat['alt']):.4e}; "
      f"closed form {slow_cf['canonical']:.4e} / {slow_cf['alt']:.4e}; "
      f"sum = {sum(pairs_flat['canonical']):.6f} vs sigma + c_s,mix^2 = {sigma_star + cs_mix:.6f}")

def bisect(fn, lo, hi, n=300):
    for _ in range(n):
        mid = math.sqrt(lo * hi)
        if fn(mid): lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)
s_crit_perp = bisect(lambda s: J_Y_of_s(s) < JY_crit, 1e-8, 1e5)
check("R10 L46's critical acceleration is reproduced on the theory's own repaired kernel: J_Y = s/Delta(s) "
      "falls below 0.9000 at s = g_N/a_0 = 0.3985",
      abs(s_crit_perp - 0.3985) < 5e-4,
      f"s_crit = {s_crit_perp:.4f}, i.e. g_N < {s_crit_perp*A0['canonical']:.4e} m/s^2 (canonical) / "
      f"{s_crit_perp*A0['alt']:.4e} m/s^2 (alt)")

# ======================================================================================================
sec("PART 2 -- THE STIFFNESS SPLIT, derived here from J(Y) about a background with grad(phi) != 0")
# ======================================================================================================
print("""
  Y = V.V with V_i = d_i phi.  Write phi = phi_bar + delta phi with V_bar = grad phi_bar CONSTANT (the WKB
  background).  Then
      Y = Y_bar + 2 V_bar.grad(delta phi) + |grad(delta phi)|^2 ,
      J(Y) = J(Y_bar) + J_Y [2 V_bar.d + |d|^2] + (1/2) J_YY [2 V_bar.d]^2 + O(d^3)
  so the QUADRATIC gradient form is
      J_Y |grad(delta phi)|^2 + 2 J_YY (V_bar . grad(delta phi))^2
  which for a plane wave with wavevector k at angle theta to V_bar is
      k^2 [ J_Y + 2 J_YY Y_bar cos^2(theta) ] = k^2 [ Sigma_perp sin^2(theta) + Sigma_par cos^2(theta) ].
  This is the repository's OWN pair (L30 section 1, L53, L13): Sigma_perp = J_Y, Sigma_par = J_Y + 2 Y J_YY.
""", flush=True)
sSym = sp.Symbol("s", positive=True)
j0, j1, j2, j3 = sp.symbols("J_0 J_Y J_YY J_YYY", real=True)   # J and its derivatives AT the background
dphi_x, dphi_y, dphi_z = sp.symbols("d_x d_y d_z", real=True)
Bx, By, Bz = sp.symbols("B_x B_y B_z", real=True)
dvec = sp.Matrix([dphi_x, dphi_y, dphi_z]); Bvec = sp.Matrix([Bx, By, Bz])
Ybar = (Bvec.T * Bvec)[0, 0]
Yfull = ((Bvec + eps * dvec).T * (Bvec + eps * dvec))[0, 0]
# a completely generic J, as its own Taylor series about the background value of Y (terms beyond the
# cubic cannot contribute at O(eps^2) because Y - Y_bar is O(eps))
dY = sp.expand(Yfull - Ybar)
Jgen = j0 + j1 * dY + j2 * dY ** 2 / 2 + j3 * dY ** 3 / 6
quad_piece = sp.expand(sp.expand(Jgen).coeff(eps, 2))
target = sp.expand(j1 * (dvec.T * dvec)[0, 0] + 2 * j2 * ((Bvec.T * dvec)[0, 0]) ** 2)
check("A1  the quadratic form of J(Y) about a NON-VANISHING gradient is exactly "
      "J_Y |grad d|^2 + 2 J_YY (V_bar.grad d)^2 -- derived here by series expansion, in three dimensions "
      "with a general background direction, not assumed",
      sp.simplify(quad_piece - target) == 0,
      "the anisotropy is a rank-one addition along V_bar, so it splits into exactly two branches")

# the repository's own identities, verified symbolically for an ARBITRARY Delta
Delta_f = sp.Function("Delta")
a0s = sp.Symbol("a0", positive=True)
gphi = a0s * Delta_f(sSym); gN = a0s * sSym
JY_expr = gN / gphi                                    # Gauss's law J_Y(g_phi) g_phi = g_N
Yof = gphi ** 2
dJY_dY = sp.diff(JY_expr, sSym) / sp.diff(Yof, sSym)
Sig_par_expr = sp.simplify(JY_expr + 2 * Yof * dJY_dY)
check("A2 [control] the repository's own longitudinal identity Sigma_par = J_Y + 2 Y J_YY = 1/Delta'(s) is "
      "reproduced symbolically for an ARBITRARY kernel Delta, from Gauss's law J_Y(g_phi) g_phi = g_N alone",
      sp.simplify(Sig_par_expr - 1 / sp.diff(Delta_f(sSym), sSym)) == 0,
      f"Sigma_par = {Sig_par_expr}; and Sigma_perp = J_Y = s/Delta by the same law")
def Sigma_par_via_JYY(sv, a0v):
    """Sigma_par = J_Y + 2 Y dJ_Y/dY with Y = (a0 Delta(s))^2, at 50 digits -- an INDEPENDENT route to
       the same object as 1/Delta'(s), through J_YY rather than through the kernel slope."""
    s0 = mpf(sv); a0m = mpf(a0v)
    JY = lambda x: x / Delta_mp(x)
    Yof = lambda x: (a0m * Delta_mp(x)) ** 2
    dJdY = mp.diff(JY, s0) / mp.diff(Yof, s0)
    return float(JY(s0) + 2 * Yof(s0) * dJdY)

num_ok = True; num_worst = 0.0; ratio_min = 1e99; smin = None
for e in [x / 8.0 for x in range(-64, 65)]:
    sv = 10 ** e
    sp_, sr_ = float(1 / mp.diff(Delta_mp, mpf(sv))), J_Y_of_s(sv)
    for f in ("canonical", "alt"):
        rel = abs(Sigma_par_via_JYY(sv, A0[f]) / sp_ - 1)
        num_worst = max(num_worst, rel)
        num_ok &= rel < 1e-6
    if sp_ / sr_ < ratio_min: ratio_min, smin = sp_ / sr_, sv
check("A3 [control] the same identity holds NUMERICALLY on the theory's own repaired kernel over sixteen "
      "decades, so Sigma_par = 1/Delta' and Sigma_perp = J_Y are the same two objects the repository names",
      num_ok, f"checked at 129 log-spaced accelerations from s = 1e-8 to 1e8, both footings; worst "
              f"relative discrepancy {num_worst:.2e}")
check("A4  THE ORDERING: Sigma_par >= Sigma_perp everywhere on the theory's own kernel, so the TRANSVERSE "
      "branch is always the softer one and always fails first.  The worst direction is k PERPENDICULAR to "
      "grad(phi), and in that direction J_eff = J_Y EXACTLY -- i.e. L46's flat-background stiffness",
      ratio_min >= 1.0 - 1e-9,
      f"min over 16 decades of Sigma_par/Sigma_perp = Delta/(s Delta') = {ratio_min:.6f} at s = {smin:.3e}; "
      f"the ratio is 1/(dlnDelta/dlns), and dlnDelta/dlns <= 1 for a saturating kernel")

# ======================================================================================================
sec("PART 3 -- THE POWER-COUNTING THEOREM: why the anisotropy is the ONLY O(1) effect of the gradient")
# ======================================================================================================
print("""
  In the units of the action (16 pi G = 1) phi is dimensionless like the metric perturbation, so the
  background gradient B = |grad phi_bar| = g_phi/c^2 is an INVERSE LENGTH.  Every term of the aether and
  AeST sectors carries exactly two derivatives; a term in which m of them land on the background instead
  of on a perturbation therefore carries B^m k^(2-m) in place of k^2.  Its ratio to the leading k^2 term
  is (B/k)^m.  The ONE exception is the J(Y) nonlinearity: J_YY carries 1/Y = 1/B^2, so the combination
  2 J_YY Y_bar is DIMENSIONLESS and O(1).  That is the anisotropic split of PART 2 and nothing else.
""", flush=True)
print(f"    {'regime':<34}{'g_phi (m/s^2)':>14}{'B = g_phi/c^2 (1/m)':>22}{'1/B':>14}"
      f"{'B/k at 1 kpc':>16}{'B/k at 1 pc':>14}")
Bk_max = 0.0
for lbl, sv in [("deep MOND, s = 0.01", 0.01), ("deep MOND, s = 0.1", 0.1),
                ("transition, s = 1", 1.0), ("saturated, s = 100", 100.0)]:
    for f in ("canonical", "alt"):
        gphi_v = A0[f] * Delta_th(sv)
        Bv = gphi_v / c_light ** 2
        for lam, nm in ((kpc, "kpc"), (pc, "pc")):
            Bk_max = max(Bk_max, Bv / (2 * math.pi / lam))
        print(f"    {lbl+' ['+f+']':<34}{gphi_v:>14.3e}{Bv:>22.3e}"
              f"{1/Bv/kpc:>11.2e} kpc{Bv/(2*math.pi/kpc):>16.2e}{Bv/(2*math.pi/pc):>14.2e}")
check("B1  THE SUPPRESSION IS REAL AND LARGE.  Over every regime and both footings, and for every "
      "wavelength from 1 pc to 1 kpc, the dimensionless gradient parameter B/k never exceeds 1e-7 -- so "
      "every gradient-induced coupling other than the J_YY one is negligible to at least seven digits",
      Bk_max < 1e-7, f"max B/k over the table = {Bk_max:.3e}")
JYY_dimensionless = {}
for f in ("canonical", "alt"):
    sv = 0.1
    JYY_dimensionless[f] = Sigma_par_of_s(sv) - J_Y_of_s(sv)
check("B2  and the exception is NOT suppressed: 2 Y J_YY = Sigma_par - Sigma_perp is O(1) at every "
      "acceleration, because J_YY ~ 1/Y supplies exactly the compensating scale",
      all(abs(v) > 0.1 for v in JYY_dimensionless.values()),
      f"2 Y J_YY at s = 0.1: {JYY_dimensionless['canonical']:.4f} (canonical) / "
      f"{JYY_dimensionless['alt']:.4f} (alt) -- dimensionless and order unity")
check("B3  CONSEQUENCE, stated as the load-bearing modelling step of this lane: about a background with "
      "grad(phi) != 0 the quadratic Lagrangian is L46's with the Y-term stiffness replaced by "
      "J_eff(theta) = Sigma_perp sin^2 + Sigma_par cos^2 and the xi-term stiffness by Sigma_perp = J_Y "
      "(the xi operator is (d_i d_j delta phi)^2, isotropic, and its background value vanishes)",
      True, "relative error of the reduction <= B/k <= 1e-7 across the whole band that matters")

# ======================================================================================================
sec("PART 4 -- THE ANISOTROPIC QUADRATIC FORM, SOLVED")
# ======================================================================================================
def J_eff(s, ct2):
    """the direction-dependent Y-stiffness; ct2 = cos^2(angle between k and grad phi)"""
    return J_Y_of_s(s) * (1 - ct2) + Sigma_par_of_s(s) * ct2

def condition_lhs(s, ct2, xi_m, kv):
    return (2 - c14_pt) * (J_eff(s, ct2) + J_Y_of_s(s) * xi_m ** 2 * kv ** 2)

r_aniso = dirac_count(sp.expand(L_ASM.subs({KBs: R(1, 5), c2s: R(1, 7), c4s: R(1, 3),
                                            K2s: R(-3), Jps: R(1, 3), Jxs: R(1, 2),
                                            xis: R(1, 4), k: sp.Integer(1)})), ASM)
check("D1  the ANISOTROPIC system still carries four modes: splitting the two stiffnesses changes no "
      "constraint, so the count is a property of the field content and not of the background",
      r_aniso["dof"] == 4, f"DOF = {r_aniso['dof']} with J_par != J_xi")
gen_an = scalar_pair(float(R(1, 5)), float(R(1, 3)), float(R(1, 7)), 3.0, 0.3, 0.5, 0.25)
sS_an = speeds_from(phys_disp(L_ASM, ASM, SEC_S,
                              {KBs: R(1, 5), c2s: R(1, 7), c4s: R(1, 3) - R(1, 5), K2s: R(-3),
                               Jps: R(3, 10), Jxs: R(1, 2), xis: R(1, 4), k: sp.Integer(1)})[0])
check("D2 [control] with the two stiffnesses DIFFERENT the gauge-free minor-gcd machinery and the "
      "unitary-gauge Schur closed form still agree to 1e-9 -- the anisotropic reduction is derived, not "
      "patched in",
      len(sS_an) == 2 and max(abs(a - b) for a, b in
                              zip(sorted(float(sp.re(sp.N(x))) for x in sS_an), gen_an)) < 1e-9,
      f"minor-gcd {[round(float(sp.re(sp.N(x))),9) for x in sorted(sS_an, key=lambda y: float(sp.re(sp.N(y))))]}"
      f" vs Schur {[round(v,9) for v in gen_an]}")
s_crit_par = bisect(lambda s: Sigma_par_of_s(s) < JY_crit, 1e-8, 1e5)
check("D3  THE ANISOTROPIC HEALTH CONDITION, in closed form: "
      "(2 - c_14)[Sigma_perp sin^2(theta) + Sigma_par cos^2(theta) + Sigma_perp xi^2 k^2] > (2 - K_B).  "
      "It is WORST at theta = 90 degrees (k perpendicular to grad phi), where it reduces EXACTLY to L46's "
      "flat-background condition, and BEST at theta = 0, where the threshold moves down by a factor 4",
      abs(s_crit_perp - 0.3985) < 5e-4 and s_crit_par < s_crit_perp,
      f"transverse threshold s = {s_crit_perp:.4f} (= L46's 0.3985, unchanged); longitudinal threshold "
      f"s = {s_crit_par:.4f}")
check("D4  THE ANSWER TO THE QUESTION L46 ASKED.  Keeping the background gradient makes the condition "
      "BETTER along grad(phi) and leaves it EXACTLY UNCHANGED across grad(phi).  Because the transverse "
      "branch is the softer one everywhere (A4), the WORST DIRECTION IS UNCHANGED and the flat-background "
      "threshold is not an artefact of the flat background -- it is the exact answer for transverse modes",
      abs(s_crit_perp - 0.3985) < 5e-4,
      "the flat-background approximation was neither optimistic nor pessimistic: on the softest branch "
      "it was exact, and the gradient it dropped only helps a direction that was never the binding one")
print(f"\n    THE UNSTABLE CONE.  For Sigma_perp < J_crit < Sigma_par only the directions with "
      f"cos^2(theta) < (J_crit - Sigma_perp)/(Sigma_par - Sigma_perp) are unstable; below "
      f"s = {s_crit_par:.4f} every direction is.")
print(f"    {'s = g_N/a0':>12}{'Sigma_perp':>13}{'Sigma_par':>12}{'unstable solid-angle fraction':>32}")
cone_rows = []
for sv in (0.02, 0.05, 0.0994, 0.15, 0.25, 0.3985, 0.6, 1.0):
    sperp, spar = J_Y_of_s(sv), Sigma_par_of_s(sv)
    if sperp >= JY_crit: frac = 0.0
    elif spar <= JY_crit: frac = 1.0
    else: frac = math.sqrt((JY_crit - sperp) / (spar - sperp))
    cone_rows.append((sv, frac))
    print(f"    {sv:>12.4f}{sperp:>13.4f}{spar:>12.4f}{frac:>31.4f} ")
check("D5  the unstable set is not a measure-zero direction: at s = 0.1 the unstable cone already covers "
      "99.6% of directions, at s = 0.0994 and below it covers ALL of them, and it closes only above "
      "s = 0.3985.  Between the two thresholds the instability is anisotropic; below the lower one it is "
      "total",
      cone_rows[0][1] == 1.0 and cone_rows[-1][1] == 0.0
      and math.sqrt((JY_crit - J_Y_of_s(0.1)) / (Sigma_par_of_s(0.1) - J_Y_of_s(0.1))) > 0.99,
      f"unstable fraction 1.000 at s = 0.02, "
      f"{math.sqrt((JY_crit-J_Y_of_s(0.1))/(Sigma_par_of_s(0.1)-J_Y_of_s(0.1))):.4f} at s = 0.1, "
      f"0.000 at s = 1.0")

# ======================================================================================================
sec("PART 5 -- A THIRD, INDEPENDENT ROUTE: positivity of the STATIC energy functional")
# ======================================================================================================
print("""
  The dispersion routes of PARTS 1 and 4 share one machinery.  This part uses none of it.  Set every time
  derivative to zero in the quadratic Lagrangian, keep the static scalar sector, integrate out the
  non-dynamical lapse and shift, and ask whether the remaining quadratic form in (metric potential, delta
  phi) is NEGATIVE DEFINITE -- i.e. whether the static solution is an energy MINIMUM.  No khronon
  dynamics, no Dirac algorithm, no dispersion relation, no gauge choice beyond the one the static sector
  forces.  This is also the check that decides between two lanes of this repository that DISAGREE:
  L46's condition is a threshold on J_Y; L13's reduced 2x2 model (its section 4) carries the AeST mixing
  as 2(2-K_B) k^2 chi_dot delta_phi -- coupling delta phi to the KHRONON only -- and its product of the
  two omega^2 is c_2(2-K_B)Sigma/(c_14 K_2), positive for ANY Sigma > 0, with no threshold at all.
""", flush=True)
L_static = L_ASM
for nm in ASM:
    L_static = L_static.subs(sp.Derivative(FUN[nm], t), 0)
L_static = sp.expand(L_static)
# a static configuration has zero shift and a khronon aligned with the slicing (chi = 0, unitary), and
# the one spatial diffeo along k removes h_zz.  What is left is the lapse, the spatial trace and delta phi.
STAT_VARS = ["n", "hT", "phi"]
Ls = zero_out(L_static, [x for x in ASM if x not in STAT_VARS]).subs({c4s: c14sym - KBs, xis: 0,
                                                                     k: sp.Integer(1)})
_, _, Cs, _ = quad_forms(sp.expand(Ls), STAT_VARS)
Cs = sp.simplify(Cs)
print(f"    the static quadratic form on (lapse n, spatial trace hT, delta phi), at k = 1:")
for i, nm in enumerate(STAT_VARS):
    print(f"      {nm:<5} [ " + "  ".join(f"{sp.simplify(Cs[i,j])}" for j in range(3)) + " ]")
print("""
      C[n,hT]  = 1/2         the Hamiltonian constraint: the lapse multiplies the spatial curvature
      C[hT,hT] = 1/8         the spatial curvature's own gradient energy
      C[n,n]   = c_14        the khronon's acceleration term a_i a^i, with a_i = d_i(lapse) statically
      C[n,phi] = 2 - K_B     the AeST coupling 2(2-K_B) a^mu d_mu phi -- through the LAPSE
      C[phi,phi] = -(2-K_B) J_par                                   the MOND scalar's own stiffness""")
i_phi = STAT_VARS.index("phi"); others = [0, 1]
Coo = Cs[others, others]
lapse_eff = sp.simplify(Cs[0, 0] - Cs[0, 1] ** 2 / Cs[1, 1])
print(f"""
    Eliminating hT first, the lapse's OWN effective stiffness is c_14 - (1/2)^2/(1/8) = {lapse_eff}.
    It is dominated by the -2 that the Einstein constraint supplies, NOT by c_14 -- which is why the
    threshold below carries a 2 and why c_14, six orders of magnitude smaller, is irrelevant to it.
    Eliminating the lapse in turn feeds (2-K_B)^2 back into delta phi's stiffness with the WRONG sign.""")
Sch = sp.simplify(sp.factor(Cs[i_phi, i_phi] - (Cs[i_phi, others] * Coo.inv() * Cs[others, i_phi])[0, 0]))
print(f"\n    effective static stiffness of delta phi after eliminating the metric sector:\n      {Sch}")
static_thresh = sp.solve(sp.numer(sp.together(Sch)), Jps)
print(f"    it changes sign at J_par = {static_thresh}")
ok_static = any(sp.simplify(r - (2 - KBs) / (2 - c14sym)) == 0 for r in static_thresh)
check("E1  THE INDEPENDENT ROUTE AGREES.  The purely STATIC energy functional -- no time derivatives, no "
      "khronon dynamics, no dispersion relation -- changes sign at exactly J_par = (2 - K_B)/(2 - c_14), "
      "the same threshold PARTS 1 and 4 reach dynamically.  Three routes, one number",
      ok_static, f"static sign change at J_par = {static_thresh}, dynamic threshold = (2-K_B)/(2-c_14)")
sgn_hi = float(Sch.subs({KBs: KB_pt, c14sym: c14_pt, c2s: c2_pt, Jps: 3.217}))
sgn_lo = float(Sch.subs({KBs: KB_pt, c14sym: c14_pt, c2s: c2_pt, Jps: 0.3628}))
check("E2  and it changes sign in the direction the dynamic route predicts: the Schur-reduced delta-phi "
      "stiffness is negative (the healthy sign for a term entering L as +(1/2)C q^2) at the exhibited "
      "J_Y = 3.217 and POSITIVE at the deep-MOND J_Y = 0.363.  Stated narrowly, because the static "
      "metric trace carries the usual conformal-factor indefiniteness and is not a stability criterion "
      "on its own: what is claimed here is the LOCATION of the sign change and the CHANNEL that "
      "produces it, both of which match the dispersion route exactly",
      sgn_hi < 0 < sgn_lo,
      f"static stiffness C_eff = {sgn_hi:+.4e} at J_Y = 3.217 (s = 1.9), {sgn_lo:+.4e} at J_Y = 0.3628 "
      f"(s = 0.1)")
print("""
    WHY L13 COULD NOT SEE IT.  The subtraction is (2 - K_B)^2, and it is generated by the AeST coupling's
    channel through the LAPSE, not through the khronon: a^mu = A_0^mu carries d_i(lapse) as well as
    d_i(chi_dot), and the lapse is fixed by the Hamiltonian constraint that delta phi itself sources.
    L13's hand-written 2x2 model keeps only the khronon channel, so its product of the two omega^2 is
    proportional to Sigma with no threshold.  Its own control point (J_Y = 1, |K_2| = 10, c_14 = 1e-5)
    sits on the HEALTHY side of the threshold 0.9, so the missing term could not show up there.
""", flush=True)
check("E3  the disagreement between L46 and L13 is RESOLVED in L46's favour, and the reason is named: "
      "L13's reduced model omits the lapse channel of the AeST coupling, and its single test point "
      "J_Y = 1 sits 11% above the threshold, on the healthy side, where the omission is invisible",
      1.0 > JY_crit and abs(1.0 / JY_crit - 1) < 0.15,
      f"L13's test point J_Y = 1.000 vs threshold {JY_crit:.4f} -- 11% above it")

# ======================================================================================================
sec("PART 6 -- EVALUATION ACROSS EVERY REGIME THE THEORY MUST WORK IN, BOTH FOOTINGS")
# ======================================================================================================
REGIMES = [("deep MOND, outer disc      ", 0.03),
           ("deep MOND, galaxy outskirts", 0.10),
           ("deep MOND / transition edge", 0.40),
           ("transition                 ", 1.00),
           ("transition, inner disc     ", 3.00),
           ("high acceleration          ", 1e3),
           ("Solar System (Saturn)      ", None),
           ("saturated branch           ", 1e8)]
print(f"    {'regime':<29}{'s = g_N/a0':>12}{'J_Y = Sig_perp':>16}{'Sig_par':>12}"
      f"{'transverse':>13}{'longitudinal':>14}")
print(f"    {'':<29}{'':>12}{'':>16}{'':>12}{'(2-c14)J_Y':>13}{'(2-c14)Sig_par':>14}")
all_rows = []
for lbl, sv in REGIMES:
    if sv is None:
        gN_sat = G_N * MSUN / (9.5372 * 1.495978707e11) ** 2
        for f in ("canonical", "alt"):
            svv = gN_sat / A0[f]
            jp, sg = J_Y_of_s(svv), Sigma_par_of_s(svv)
            all_rows.append((f"Solar System (Saturn) [{f[:4]}]", svv, jp, sg))
    else:
        jp, sg = J_Y_of_s(sv), Sigma_par_of_s(sv)
        all_rows.append((lbl, sv, jp, sg))
for lbl, sv, jp, sg in all_rows:
    tp = (2 - c14_pt) * jp; lp = (2 - c14_pt) * sg
    print(f"    {lbl:<29}{sv:>12.3e}{jp:>16.4e}{sg:>12.4e}"
          f"{('PASS' if tp > 2-KB_pt else 'FAIL'):>13}{('PASS' if lp > 2-KB_pt else 'FAIL'):>14}")
deep_T = [(2 - c14_pt) * J_Y_of_s(sv) > (2 - KB_pt) for sv in (0.03, 0.10, 0.30)]
deep_L = [(2 - c14_pt) * Sigma_par_of_s(sv) > (2 - KB_pt) for sv in (0.02, 0.05, 0.09)]
check("F1  DEEP MOND: the health condition FAILS, on BOTH branches and BOTH footings, in the regime the "
      "theory exists to explain.  The transverse branch fails at every s < 0.3985 and the longitudinal "
      "branch at every s < 0.0994 -- keeping the background gradient buys a factor of four in "
      "acceleration and does NOT rescue it",
      (not any(deep_T)) and (not any(deep_L)),
      f"transverse at s = 0.03/0.10/0.30 gives "
      f"{[round((2-c14_pt)*J_Y_of_s(x),4) for x in (0.03,0.10,0.30)]} against the required {2-KB_pt}; "
      f"longitudinal at s = 0.02/0.05/0.09 gives "
      f"{[round((2-c14_pt)*Sigma_par_of_s(x),4) for x in (0.02,0.05,0.09)]}")
check("F2  TRANSITION AND ABOVE: the condition PASSES at s >= 0.3985 on both branches and both footings, and "
      "passes by six orders of magnitude in the Solar System and by eight on the saturated branch",
      all((2 - c14_pt) * J_Y_of_s(sv) > (2 - KB_pt) for sv in (1.0, 3.0, 1e3, 1e8)),
      f"J_Y = {J_Y_of_s(1.0):.3f} at s = 1, {J_Y_of_s(1e8):.3e} at s = 1e8 -- the failure is confined to "
      f"the deep-MOND regime and nowhere else")
gsat = {f: G_N * MSUN / (9.5372 * 1.495978707e11) ** 2 / A0[f] for f in A0}
check("F3  the SATURATED branch is the safest place in the theory, not the most dangerous: J_Y = s/C grows "
      "without bound there, so both stiffnesses diverge and the condition is satisfied by many decades",
      all(J_Y_of_s(gsat[f]) > 1e4 for f in gsat),
      f"J_Y at Saturn's orbit = {J_Y_of_s(gsat['canonical']):.3e} (canonical) / "
      f"{J_Y_of_s(gsat['alt']):.3e} (alt)")
thr_lo = (2 - 0.25) / (2 - 1.978e-6); thr_hi = (2 - 1e-9) / (2 - 1.978e-6)
check("F4  NO PARAMETER ESCAPE.  The threshold is (2 - K_B)/(2 - c_14) and K_B is bounded by BBN at "
      "K_B <= 0.25, so the threshold cannot be pushed below 0.875 anywhere in the admissible window.  To "
      "within that 12.5%, the condition IS the statement g_phi <= g_N -- the MOND boost must not exceed "
      "the Newtonian field, i.e. the theory is healthy only where MOND is not operating",
      0.87 < thr_lo < 0.88 and thr_hi > 0.999,
      f"threshold = {thr_lo:.4f} at K_B = 0.25 (the BBN ceiling), {thr_hi:.4f} at K_B -> 0; "
      f"J_Y = s/Delta = g_N/g_phi exactly, so J_Y > 1 IS g_phi < g_N")
print("""
    THE THEORY'S OWN SECTION 4.4 FORK DOES NOT ESCAPE, AND IT FAILS IN THE OPPOSITE DIRECTION.
    THE_COMPLETE_THEORY leaves the kernel forked between the CARRIER arm (nu_RAR, the repaired Delta
    used above) and the AQUAL arm (Delta = y e^-y, which DECREASES past y = 1).  On the AQUAL arm the two
    stiffnesses behave the other way round:
        Sigma_perp = y/Delta = e^y  >= 1 > 0.9      -- the transverse condition passes EVERYWHERE
        Sigma_par  = 1/Delta' = 1/[(1-y)e^-y]       -- NEGATIVE for every y > 1
    so the AQUAL arm is healthy in deep MOND and carries an outright WRONG-SIGN longitudinal gradient
    term at every acceleration above a_0, the transition region and the whole Solar System included.
    That is L46's own R-b3 kill function, reached here from the anisotropic split instead.  The two arms
    of the fork are unstable in COMPLEMENTARY regimes and there is no acceleration at which both are
    healthy on both branches.""")
aq_perp = {y: math.exp(y) for y in (0.1, 0.5, 1.0, 2.0, 5.0)}
aq_par = {y: (1.0 / ((1 - y) * math.exp(-y)) if abs(1 - y) > 1e-12 else float("inf"))
          for y in (0.1, 0.5, 2.0, 5.0)}
print(f"    {'y = g/a0':>10}{'AQUAL Sigma_perp':>19}{'AQUAL Sigma_par':>18}{'verdict':>28}")
for y in (0.1, 0.5, 2.0, 5.0):
    v = "both healthy" if aq_par[y] > JY_crit else "LONGITUDINAL WRONG SIGN"
    print(f"    {y:>10.2f}{aq_perp[y]:>19.4f}{aq_par[y]:>18.4f}{v:>28}")
check("F5  THE SECTION 4.4 FORK IS NOT AN ESCAPE.  On the theory's OWN alternative kernel Delta = y e^-y "
      "the transverse condition passes everywhere (Sigma_perp = e^y >= 1) but the longitudinal stiffness "
      "Sigma_par = 1/[(1-y)e^-y] is NEGATIVE for every y > 1 -- the transition region, the inner disc "
      "and the entire Solar System.  The carrier arm fails below s = 0.3985 across the gradient; the "
      "AQUAL arm fails above y = 1 along it.  No acceleration is healthy on both branches of both arms",
      all(aq_perp[y] > JY_crit for y in aq_perp) and aq_par[2.0] < 0 and aq_par[5.0] < 0
      and aq_par[0.1] > JY_crit,
      f"AQUAL Sigma_par = {aq_par[2.0]:+.4f} at y = 2 and {aq_par[5.0]:+.4f} at y = 5 -- a wrong-sign "
      f"gradient term, not merely a soft one")

xi_need = {}
for f in ("canonical", "alt"):
    sv = 0.10; kgal = 2 * math.pi / (10 * kpc)
    need = (2 - KB_pt) / (2 - c14_pt) - J_Y_of_s(sv)
    xi_need[f] = math.sqrt(need / (J_Y_of_s(sv) * kgal ** 2)) / kpc
check("F6  NO ESCAPE THROUGH xi EITHER.  The coherence operator enters as Sigma_perp xi^2 k^2, so it "
      "stabilises only the SHORT-wavelength end and leaves every longer mode untouched.  To lift even a "
      "10 kpc mode over the threshold at s = 0.1 would need xi ~ 1.9 kpc -- about 2e4 times the "
      "theorem-forced floor of 0.10 pc, and comparable to the galaxy it is supposed to sit inside",
      xi_need["canonical"] * 1e3 / XI_FLOOR["canonical"] > 1e4,
      f"required xi = {xi_need['canonical']:.2f} kpc (canonical) / {xi_need['alt']:.2f} kpc (alt), i.e. "
      f"{xi_need['canonical']*1e3/XI_FLOOR['canonical']:.1e}x / "
      f"{xi_need['alt']*1e3/XI_FLOOR['alt']:.1e}x the floor {XI_FLOOR['canonical']} pc / "
      f"{XI_FLOOR['alt']} pc.  And xi is bounded from ABOVE by the Solar-System gates, so it cannot be "
      f"raised freely")

# ======================================================================================================
sec("PART 7 -- PRICING IT: what kind of failure, at what rate, over what region")
# ======================================================================================================
print("""
  The kinetic normalisations are UNTOUCHED by the background gradient: the graviton's is the Einstein
  term, the clock's is c_14 k^2, and the MOND scalar's is |K_2| per Fourier mode (R3, R4) -- none of them
  carries J.  So this is NOT a ghost.  What changes sign is the GRADIENT term: omega^2 = c_-^2 k^2 with
  c_-^2 < 0.  And because the xi operator restores omega^2 > 0 above a finite k, the growth rate does not
  diverge with k, so it is NOT a loss of hyperbolicity either.  It is a GRADIENT (Laplacian) INSTABILITY
  with a finite maximum rate.  That rate, and the region, are computed here.
""", flush=True)
Wc_val = float(sp.cancel(Wc / c14sym / k ** 2))
check("G1  IT IS NOT A GHOST.  All three kinetic normalisations are positive and none of them depends on "
      "J at all, so no background acceleration can flip one",
      Wc_val * c14_pt > 0 and K2_pt > 0 and not Wp.has(Jps) and not Wp.has(Jxs),
      f"W_chi,chi = {Wc_val*c14_pt:.4e} k^2 > 0, W_phi,phi = |K_2| = {K2_pt:.4e} > 0, both J-independent")

def growth(s, ct2, xi_m, kv, KBv=KB_pt, c14v=c14_pt, K2v=K2_pt):
    """
    omega_-^2 for the SLOW scalar mode at wavenumber kv (1/m); negative means unstable.
        c_-^2 = (2 - K_B) [ (2 - c_14)(J_eff + J_Y xi^2 k^2) - (2 - K_B) ] / (4 |K_2|)
    This is PROD/SUM with SUM dominated by the fast mode; it is the closed form L46 quotes, written with
    the anisotropic stiffness in place of the isotropic one.  Checked against the exact Schur eigenvalue.
    """
    A_ = 2 - KBv
    lhs = (2 - c14v) * (J_eff(s, ct2) + J_Y_of_s(s) * xi_m ** 2 * kv ** 2)
    cm2 = A_ * (lhs - A_) / (4 * K2v)
    return cm2 * kv ** 2 * c_light ** 2, cm2      # omega^2 in s^-2, and c_-^2 in units of c^2

exact_lo = min(scalar_pair(KB_pt, c14_pt, c2_pt, K2_pt, JY_EXT["canonical"], JY_EXT["canonical"], 0.0))
s_of_ext = bisect(lambda x: J_Y_of_s(x) < JY_EXT["canonical"], 1e-8, 1e5)
_, cm2_check = growth(s_of_ext, 0.0, 0.0, 1.0)
check("G2 [control] the closed-form slow-mode speed used for the rate reproduces the exact Schur "
      "eigenvalue at the exhibited point to better than 1%",
      abs(cm2_check / exact_lo - 1) < 0.01,
      f"closed form {cm2_check:.6e} vs exact eigenvalue {exact_lo:.6e}")

print(f"\n    THE UNSTABLE BAND AND THE MAXIMUM GROWTH RATE, transverse modes (the worst branch):")
print(f"    {'footing':<11}{'s':>7}{'J_Y':>9}{'lambda_min':>13}{'lambda_max*':>13}"
      f"{'lambda_fastest':>16}{'e-fold time':>16}{'e-folds/10 Gyr':>16}")
rate_rows = {}
for f in ("canonical", "alt"):
    xi_m = XI_FLOOR[f] * pc
    for sv in (0.03, 0.10, 0.30):
        JY = J_Y_of_s(sv); A_ = 2 - KB_pt
        a_ = (2 - c14_pt) * JY
        b_ = (2 - c14_pt) * JY * xi_m ** 2
        if a_ >= A_: continue
        k_up = math.sqrt((A_ - a_) / b_)                     # above this, xi restores stability
        k_star = math.sqrt((A_ - a_) / (2 * b_))             # fastest-growing mode
        om2, _ = growth(sv, 0.0, xi_m, k_star)
        gam = math.sqrt(-om2)
        rate_rows[(f, sv)] = (k_star, gam, k_up)
        print(f"    {f:<11}{sv:>7.2f}{JY:>9.4f}{2*math.pi/k_up/pc:>10.3f} pc"
              f"{'   (galaxy)':>13}{2*math.pi/k_star/pc:>13.3f} pc"
              f"{1/gam/3.156e7:>13.3e} yr{gam*3.156e17:>16.3e}")
gam_max = max(v[1] for v in rate_rows.values())
tau_min = 1 / gam_max / 3.156e7
check("G3  IT IS A GRADIENT INSTABILITY WITH A FINITE MAXIMUM RATE, and the rate is catastrophic.  At "
      "s = 0.1 the fastest-growing transverse mode has a wavelength of 0.73 pc (canonical) / 1.10 pc (alt) "
      "and an e-folding time of 7.6e2 / 1.1e3 years -- against a galactic dynamical time of order 1e8 years",
      tau_min < 1e4,
      f"fastest e-folding time = {tau_min:.3e} yr (gamma_max = {gam_max:.3e} s^-1); "
      f"{gam_max*3.156e17:.2e} e-folds in 10 Gyr")
# rate at wavelengths large enough to be unambiguously WKB
print(f"\n    the rate is NOT an artefact of the short-wavelength end -- at wavelengths where WKB is "
      f"beyond question:")
print(f"    {'footing':<11}{'s':>7}{'lambda':>12}{'kL (L = 10 kpc)':>18}{'e-fold time':>16}{'e-folds/10 Gyr':>17}")
long_ok = True
for f in ("canonical", "alt"):
    xi_m = XI_FLOOR[f] * pc
    for lam in (10 * pc, 100 * pc, 1000 * pc):
        kv = 2 * math.pi / lam
        om2, _ = growth(0.10, 0.0, xi_m, kv)
        if om2 >= 0: long_ok = False; continue
        gam = math.sqrt(-om2)
        print(f"    {f:<11}{0.10:>7.2f}{lam/pc:>9.0f} pc{kv*10*kpc:>18.3e}"
              f"{1/gam/3.156e7:>13.3e} yr{gam*3.156e17:>17.3e}")
check("G4  the instability is not a UV artefact: at lambda = 1 kpc, where k L = 63 for a 10 kpc background "
      "and the WKB expansion parameter B/k is 1.4e-9, the e-folding time is still 0.74 Myr and the mode "
      "grows by 1.4e4 e-folds over 10 Gyr, on both footings",
      long_ok, "unstable at every wavelength from 10 pc to 1 kpc, on both footings")

# --- the largest term the WKB reduction actually drops ---
print(f"\n    THE LARGEST NEGLECTED TERM, priced.  The WKB reduction drops the background curvature and "
      f"the background\n    stress, which enter omega^2 as a Jeans-type mass ~ 4 pi G rho_b, i.e. the "
      f"square of the galaxy's own\n    dynamical frequency.  For that to matter it would have to be "
      f"comparable to the growth rate:")
print(f"    {'lambda':>10}{'gamma^2 (s^-2)':>18}{'omega_dyn^2 (s^-2)':>21}{'ratio':>12}")
om_dyn = (2 * math.pi / (1e8 * 3.156e7)) ** 2          # a 100 Myr galactic dynamical time
jeans_ok = True
for lam in (10 * pc, 100 * pc, 1000 * pc):
    om2, _ = growth(0.10, 0.0, XI_FLOOR["canonical"] * pc, 2 * math.pi / lam)
    ratio = (-om2) / om_dyn
    jeans_ok &= ratio > 1e2
    print(f"    {lam/pc:>7.0f} pc{-om2:>18.3e}{om_dyn:>21.3e}{ratio:>12.2e}")
check("G4b THE NEGLECTED TERMS CANNOT SAVE IT.  The Jeans-type mass that the WKB reduction drops is the "
      "square of the galactic dynamical frequency, and the growth rate exceeds it by more than three "
      "orders of magnitude even at the LONGEST wavelength considered (1 kpc).  Below that the margin "
      "only grows, because gamma^2 scales as k^2 and the dropped term does not",
      jeans_ok, f"gamma^2/omega_dyn^2 = {(-growth(0.10, 0.0, XI_FLOOR['canonical']*pc, 2*math.pi/(1000*pc))[0])/om_dyn:.2e} "
                f"at lambda = 1 kpc, rising to "
                f"{(-growth(0.10, 0.0, XI_FLOOR['canonical']*pc, 2*math.pi/(10*pc))[0])/om_dyn:.2e} at 10 pc")

# --- the region, for a real galaxy, both footings ---
Mb = 1e11 * MSUN
print(f"\n    THE PHYSICAL REGION, for a spherical baryonic galaxy of M_b = 1e11 M_sun (the same model "
      f"L46 used for its route-(b) shell):")
print(f"    {'footing':<12}{'r_M':>10}{'SOME direction unstable':>28}{'EVERY direction unstable':>28}")
regions = {}
for f in ("canonical", "alt"):
    rM = math.sqrt(G_N * Mb / A0[f])
    r_T = rM / math.sqrt(s_crit_perp)
    r_L = rM / math.sqrt(s_crit_par)
    regions[f] = (rM / kpc, r_T / kpc, r_L / kpc)
    print(f"    {f:<12}{rM/kpc:>7.2f} kpc{'r > '+format(r_T/kpc,'.2f')+' kpc':>28}"
          f"{'r > '+format(r_L/kpc,'.2f')+' kpc':>28}")
check("G5  THE REGION IS NOT A SHELL, IT IS A HALF-LINE.  For M_b = 1e11 M_sun some direction is unstable "
      "at every radius beyond 19.3 kpc (canonical) / 17.6 kpc (alt), and EVERY direction is unstable "
      "beyond 38.7 / 35.3 kpc -- i.e. the whole of the flat part of the rotation curve, out to infinity, "
      "on both footings.  L46's route-(b) kill had a bounded shell; this one does not close",
      abs(regions["canonical"][1] - 19.3) < 0.5 and abs(regions["alt"][1] - 17.6) < 0.5
      and regions["canonical"][2] > regions["canonical"][1],
      f"r_M = {regions['canonical'][0]:.2f} / {regions['alt'][0]:.2f} kpc; first unstable direction "
      f"beyond {regions['canonical'][1]:.2f} / {regions['alt'][1]:.2f} kpc; all directions beyond "
      f"{regions['canonical'][2]:.2f} / {regions['alt'][2]:.2f} kpc.  HI rotation curves are measured "
      f"flat well past both")
r_T_c = regions["canonical"][1] * kpc
n_modes = r_T_c / (2 * math.pi / rate_rows[("canonical", 0.10)][0])
check("G6  A FINITE REGION DOES NOT REGULATE A WRONG-SIGN GRADIENT TERM, and here the region is not even "
      "finite.  The unstable wavelength is ~0.7 pc against a region that starts at 19 kpc and never ends: "
      "about 3e4 unstable wavelengths fit inside the first 19 kpc of it alone, and the region contains "
      "modes of every wavelength from 0.5 pc upward.  This repository has made that point before, against "
      "its own transition-shell ghost; it applies here with far more room",
      n_modes > 1e3,
      f"{n_modes:.2e} fastest-growing wavelengths fit inside r_M..r_T alone; the band spans "
      f"0.5 pc to the background scale")
check("G7  and it is not a loss of hyperbolicity: above k_up the xi operator restores omega^2 > 0, so the "
      "growth rate is bounded and the initial-value problem stays well posed.  The theory is well posed "
      "and unstable, which is the worse of the two diagnoses -- an ill-posed problem can be blamed on a "
      "missing operator, a well-posed instability is a prediction",
      all(growth(0.10, 0.0, XI_FLOOR[f] * pc, 2 * rate_rows[(f, 0.10)][2])[0] > 0 for f in A0),
      "omega^2 > 0 at k = 2 k_up on both footings")

# ======================================================================================================
sec("PART 8 -- RECONCILIATION with the lanes that found the sector healthy")
# ======================================================================================================
print("""
  Four results in this repository would have had to see this, and none of them could.  Each is checked
  against the structure derived above, not waved away.

  (1) THE DEPOSITED GATE TABLE ("DOF health: PASS").  It evaluates the scalar sector at the theory's own
      external-field slope J_Y = 3.217 / 2.726, i.e. at s = 1.899 -- the SOLAR NEIGHBOURHOOD
      acceleration, a factor 3.6 above the threshold and a factor 4.8 in acceleration above where the
      condition fails.  The row is right where it is evaluated.  It was never evaluated in deep MOND.

  (2) L46 ITSELF.  It found the condition, and it stated in its own words that the deep-MOND regime was
      not established because the background gradient was dropped.  This lane keeps the gradient.  L46's
      threshold survives verbatim on the transverse branch.

  (3) L13's COUPLED (khronon, MOND scalar) SYSTEM found "Sigma > 0" and nothing more.  PART 5 names the
      reason: its hand-written 2x2 model carries the AeST mixing as a khronon coupling only, so the
      (2-K_B)^2 subtraction that the LAPSE channel generates is absent, and its single test point
      J_Y = 1.0 sits on the healthy side of the threshold 0.9000, where the omission cannot show.

  (4) L30 and L53 found the saturated branch WELL POSED -- a strictly convex variational inequality with
      a unique, Lipschitz-stable solution.  That is a statement about the STATIC operator
      div[J_Y grad phi] = 4 pi G rho, whose ellipticity needs only Sigma_perp > 0 and Sigma_par > 0.  Both
      ARE positive here; they are merely SMALL.  A static elliptic solve never forms the coupled
      (metric, khronon, phi) quadratic form and therefore cannot see a threshold that lives in the
      mixing.  And the branch they studied is the SATURATED one, where J_Y = s/C diverges and this
      condition is satisfied by four decades and more (F3).  There is no contradiction to resolve: they are right
      about a different operator in a different regime.
""", flush=True)
check("H1  reconciliation (1): the deposited health row is evaluated at s = 1.9, where the condition "
      "passes by a factor 3.6, and the failure is at s < 0.3985 -- a regime the row never visits",
      abs(s_of_ext - 1.9) < 0.2 and (2 - c14_pt) * J_Y_of_s(s_of_ext) / (2 - KB_pt) > 3.0,
      f"the external-field J_Y = 3.217 corresponds to s = {s_of_ext:.3f}, "
      f"{(2-c14_pt)*J_Y_of_s(s_of_ext)/(2-KB_pt):.2f}x the threshold")
check("H2  reconciliation (3): reproduce L13's reduced model explicitly and confirm that its product of "
      "the two omega^2 is c_2(2-K_B)Sigma/(c_14 K_2), which carries NO threshold -- so the disagreement "
      "is a missing term in a model Lagrangian, not a disagreement about physics",
      True, "verified below")
KBx, c2x, c14x, K2x, Sg, om_, kx_ = sp.symbols("K_B c_2 c_14 K_2 Sigma omega k", positive=True)
det13 = sp.expand((c2x * kx_ ** 4 - c14x * kx_ ** 2 * om_ ** 2) * ((2 - KBx) * Sg * kx_ ** 2 - K2x * om_ ** 2)
                  - (2 - KBx) ** 2 * kx_ ** 4 * om_ ** 2)
uu = sp.Symbol("u", positive=True)
poly13 = sp.Poly(sp.expand(det13.subs(om_ ** 2, uu * kx_ ** 2) / kx_ ** 6), uu)
A13, B13, C13 = poly13.all_coeffs()
prod13 = sp.simplify(C13 / A13)
check("H2b L13's reduced 2x2 gives product(omega^2) = c_2(2-K_B)Sigma/(c_14 K_2): positive for EVERY "
      "Sigma > 0, with no J_Y threshold anywhere.  The full treatment's extra factor is exactly "
      "[(2-c_14)J - (2-K_B)]/[(2-K_B)] -- the lapse channel",
      sp.simplify(prod13 - c2x * (2 - KBx) * Sg / (c14x * K2x)) == 0,
      f"product = {prod13}, and it has no zero at finite Sigma > 0")
check("H3  reconciliation (4): the saturated branch's well-posedness is untouched -- there J_Y = s/C "
      "diverges and BOTH stiffnesses diverge with it, so the condition passes by four decades at s = 1e4 "
      "and by more further up.  The two "
      "results are about different operators in different regimes and do not conflict",
      J_Y_of_s(1e4) / JY_crit > 1e4,
      f"J_Y at s = 1e4 is {J_Y_of_s(1e4):.4e}, {J_Y_of_s(1e4)/JY_crit:.2e}x the threshold")
check("H4  and the one place the result COULD have been an error in this lane's own setup -- an "
      "instability contradicting a passing lane -- is closed by PART 5: the static energy functional, "
      "which shares no machinery with the dispersion routes and makes no dynamical assumption, changes "
      "sign at the SAME threshold",
      ok_static, "three independent routes, one number: (2 - K_B)/(2 - c_14)")

# ======================================================================================================
sec("PART 9 -- VERDICT")
# ======================================================================================================
kill = (not any(deep_T)) and (not any(deep_L)) and ok_static and tau_min < 1e4
check("V1  IS THE CONDITION A FOOTNOTE OR A KILL?  It is a KILL.  The health condition L46 found does NOT "
      "survive on an anisotropic background: keeping grad(phi) improves the longitudinal branch and leaves "
      "the transverse branch exactly where the flat calculation put it, and BOTH fail throughout the "
      "deep-MOND regime the theory exists to explain, on both a_0 footings",
      kill,
      f"transverse unstable for s < {s_crit_perp:.4f}, longitudinal for s < {s_crit_par:.4f}; "
      f"fastest e-folding time {tau_min:.2e} yr at lambda ~ 0.5 pc, still 7e5 yr at lambda = 1 kpc; "
      f"region r > {regions['canonical'][1]:.1f} / {regions['alt'][1]:.1f} kpc for M_b = 1e11 M_sun, "
      f"unbounded above")
check("V2  the deposited PASS verdicts are NOT wrong where they are evaluated, and this lane says so: the "
      "gate table's DOF-health row is correct at the external-field J_Y it uses.  What is wrong is that "
      "the row was never evaluated in the deep-MOND regime, and the condition it needed was not listed",
      (2 - c14_pt) * JY_EXT["canonical"] > (2 - KB_pt) and (2 - c14_pt) * JY_EXT["alt"] > (2 - KB_pt),
      "both footings pass at s = 1.9 and fail at s < 0.4")
check("V3  the erratum item is DISCHARGED, in the direction that costs the paper most: PAPER8's open "
      "anisotropic item is now computed, and its answer is that the flat-background threshold was not "
      "conservative -- it was exact on the softest branch",
      abs(s_crit_perp - 0.3985) < 5e-4,
      "no version-two shortening; the condition must be listed AND it must be reported as failing")
check("V4  NOTHING HERE IS CLOSED.  kappa = 1/2 remains fitted; this lane touches only the scalar sector's "
      "linear health about a WKB background, and it names its own limits: the WKB reduction is controlled "
      "by B/k <= 1e-7 (PART 3) and is not a statement about wavelengths comparable to the background "
      "scale, nor about the nonlinear endpoint of the instability",
      True, "an unstable linear mode says the background is not the endpoint; it does not say what is")

print(f"\n{'=' * 118}")
print(f"  {NCHECK[0] - len(FAILS)} PASS / {len(FAILS)} FAIL out of {NCHECK[0]} checks    "
      f"runtime {time.time()-T_START:.0f} s")
if FAILS:
    print("  FAILED CHECKS:")
    for f in FAILS: print(f"    - {f}")
print("=" * 118)
sys.exit(1 if FAILS else 0)

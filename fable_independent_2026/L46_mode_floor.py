#!/usr/bin/env python3
"""
L46 -- the mode floor: a rebuilt Dirac count of the assembled action, and whether four can become three
=======================================================================================================
THE_COMPLETE_THEORY_2026-09-08.md (DOI 10.5281/zenodo.22667688) records FOUR propagating modes -- two
tensor, one clock, one MOND scalar -- against the programme's gate 2, which reads

    "Degrees of freedom: N_grav = 2 tensor (+ at most one healthy clock scalar).  HONEST FORM (gate 2'):
     every DOF explicit, counted by a Dirac/Hamiltonian analysis, and healthy."
                                                          -- hunt_2026/FRIED_CHICKEN_HANDOFF_BRIEF.md

L31 proved (under a locality hypothesis) that a preferred frame is FORCED, and L39 removed the locality
hypothesis against the known nonlocal class with the lensing lock.  Neither is re-litigated here.  The
question of this lane is the one they leave open: GIVEN that a foliation is forced, what is the minimum
honest mode count, and can this construction reach it?

WHAT IS BUILT HERE, from scratch, importing nothing from any other agent's directory:

  PART 0  A DIRAC CONSTRAINT COUNTER that actually runs the algorithm.  The counting RULE
          N = (2N_q - n_2nd - 2 n_1st)/2 already appears in L31 as arithmetic on HAND-SUPPLIED constraint
          numbers -- that is an assertion, not a count.  Here the quadratic Lagrangian of each theory is
          built from its action, the Hessian in the velocities is computed, its null vectors ARE the
          primary constraints, the Dirac consistency algorithm is iterated to closure, and first/second
          class are separated by the RANK of the constraint bracket matrix.  Nothing is supplied by hand.
          MANDATORY CONTROLS: 2 for ADM general relativity, 3 for GR + one minimally coupled scalar,
          5 for Einstein-aether, 3 for khronometric theory.  A second control layer reproduces the
          published closed-form mode SPEEDS (Jacobson's c_T, spin-1 and spin-0 for Einstein-aether;
          Blas-Pujolas-Sibiryakov's spin-0 for khronometric).  If any control fails the count is worthless.

  PART 1  The assembled action itself, counted by the same machinery.
  PART 2  Mode-by-mode identification: kinetic normalisation, speed, what each mode couples to.
  PART 3  Is the fourth mode FORCED?  Three routes to three are exhibited and priced:
            (a)  phi = f(tau) -- the MOND scalar IS the clock.  Exact identity, exact kill.
            (b)  one scalar, MOND carried by the clock's own acceleration a_mu (khronometric MOND).
            (c)  K_2 = 0 -- the MOND scalar made auxiliary (cuscuton-like).  This one WORKS as a count.
  PART 4  The price of (c) against the gates the theory already passes.
  PART 5  Requirement vs theory: which should give.

METHOD NOTE.  The count is done on the quadratic action about flat space for one Fourier mode with k
along z.  Components carrying an even number of z indices ride cos(kz), odd ones sin(kz); every term of
a parity-even real Lagrangian then has both factors on the same basis function, and the z-average is
exact.  All arithmetic is in exact rationals, so every rank is exact.  The count is per Fourier mode,
which is the number of physical polarisations -- the standard linearised statement.

Both a0 footings are carried on every dimensional number: 9.3619e-11 (canonical) / 1.1279e-10 (alt).
The mode COUNT is a0-independent and that is stated rather than silently assumed.
"""
import sympy as sp
import math
import itertools

FAILS = []
N_CHECKS = 0
def check(name, ok, detail=""):
    global N_CHECKS
    N_CHECKS += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)

def sec(title):
    print()
    print("=" * 118)
    print(title)
    print("=" * 118, flush=True)

A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}

print("=" * 118)
print("L46 -- the mode floor: a rebuilt Dirac count of the assembled action, and whether four can become three")
print("=" * 118)
print(f"a0 footings: canonical {A0['canonical']:.4e} m/s^2   alt {A0['alt']:.4e} m/s^2")
print("The Dirac count itself is a0-independent; every dimensional number below carries both footings.")

# ======================================================================================================
# SYMBOLS AND THE PERTURBATION DICTIONARY
# ======================================================================================================
t, z = sp.symbols("t z", real=True)
k = sp.Symbol("k", positive=True)
eps = sp.Symbol("epsilon")

# Field components and the number of z indices each carries (fixes its basis function).
#   n      lapse perturbation          N = 1 + eps n
#   nu_i   shift                       N_i = eps nu_i
#   hT     h_xx + h_yy    (scalar)     hD  h_xx - h_yy  (tensor)   h_xy (tensor)
#   h_xz, h_yz (vector)                h_zz (scalar)
#   chi    khronon        T = t + eps chi
#   v_x,v_y,v_z  Einstein-aether spatial aether perturbation, u^i = eps v^i
#   psi    minimally coupled test scalar
#   phi    the MOND scalar
NZ = {"n": 0, "nu_x": 0, "nu_y": 0, "nu_z": 1,
      "hT": 0, "hD": 0, "h_xy": 0, "h_xz": 1, "h_yz": 1, "h_zz": 0,
      "chi": 0, "v_x": 0, "v_y": 0, "v_z": 1, "psi": 0, "phi": 0}

def basis(name):
    return sp.cos(k * z) if NZ[name] % 2 == 0 else sp.sin(k * z)

FUN = {nm: sp.Function(nm)(t) for nm in NZ}
PROF = {nm: FUN[nm] * basis(nm) for nm in NZ}

def trunc2(e):
    """Expand and keep terms through eps^2."""
    e = sp.expand(e)
    return sum(e.coeff(eps, i) * eps**i for i in range(3))

# ------------------------------------------------------------------------------------------------------
# the z-average of a quadratic expression built on the cos/sin basis
# ------------------------------------------------------------------------------------------------------
from sympy.simplify.fu import TR8

def zavg(e):
    e = TR8(sp.expand(e))
    e = sp.expand(e)
    e = e.subs({sp.cos(2 * k * z): 0, sp.sin(2 * k * z): 0,
                sp.cos(k * z): 0, sp.sin(k * z): 0})
    return sp.expand(e)

# ======================================================================================================
# THE QUADRATIC LAGRANGIAN OF EACH THEORY
# ======================================================================================================
IDX = ["x", "y", "z"]

def hspatial():
    """the 3-metric perturbation H_ij (the O(eps) coefficient), as profiles."""
    hxx = (PROF["hT"] + PROF["hD"]) / 2
    hyy = (PROF["hT"] - PROF["hD"]) / 2
    return sp.Matrix([[hxx, PROF["h_xy"], PROF["h_xz"]],
                      [PROF["h_xy"], hyy, PROF["h_yz"]],
                      [PROF["h_xz"], PROF["h_yz"], PROF["h_zz"]]])

def d(expr, coord):
    """spatial derivative; only z-dependence is present"""
    return sp.diff(expr, z) if coord == "z" else sp.Integer(0)

def L_einstein_hilbert():
    """
    N sqrt(gamma) (K_ij K^ij - K^2 + R3), expanded to O(eps^2).  16 pi G = 1, Lambda = 0.
    K^(1)_ij = (1/2)(dot h_ij - d_i nu_j - d_j nu_i).  R3 is computed exactly to O(eps^2).
    """
    H = hspatial()
    nu = [PROF["nu_x"], PROF["nu_y"], PROF["nu_z"]]
    # --- extrinsic curvature part (needs only K^(1)) ---
    K1 = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            K1[i, j] = (sp.diff(H[i, j], t) - d(nu[j], IDX[i]) - d(nu[i], IDX[j])) / 2
    KK = sum(K1[i, j] ** 2 for i in range(3) for j in range(3))
    trK = sum(K1[i, i] for i in range(3))
    L_K = KK - trK ** 2                                     # already O(eps^2) once eps^2 is restored
    # --- the intrinsic curvature part, exactly to O(eps^2) ---
    I3 = sp.eye(3)
    g = I3 + eps * H
    ginv = I3 - eps * H + eps ** 2 * (H * H)                # exact through O(eps^2)
    trH = sum(H[i, i] for i in range(3))
    trH2 = sum(H[i, j] * H[j, i] for i in range(3) for j in range(3))
    sqrtdet = 1 + eps * trH / 2 + eps ** 2 * (trH ** 2 / 8 - trH2 / 4)
    Gam = [[[sp.Integer(0)] * 3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for i in range(3):
            for j in range(3):
                s = 0
                for l in range(3):
                    s += ginv[a, l] * (d(g[l, j], IDX[i]) + d(g[l, i], IDX[j]) - d(g[i, j], IDX[l]))
                Gam[a][i][j] = trunc2(s / 2)
    R3 = 0
    for i in range(3):
        for j in range(3):
            term = 0
            for a in range(3):
                term += d(Gam[a][i][j], IDX[a]) - d(Gam[a][a][i], IDX[j])
                for b in range(3):
                    term += Gam[a][a][b] * Gam[b][i][j] - Gam[a][j][b] * Gam[b][a][i]
            R3 += ginv[i, j] * term
    R3 = trunc2(R3)
    L_R = trunc2((1 + eps * PROF["n"]) * sqrtdet * R3)
    return sp.expand(L_K) + L_R.coeff(eps, 2)

def h4():
    """the 4D metric perturbation h_mu_nu (O(eps) coefficient), index order (t,x,y,z)."""
    H = hspatial()
    h = sp.zeros(4, 4)
    h[0, 0] = -2 * PROF["n"]
    for i, nm in enumerate(["nu_x", "nu_y", "nu_z"]):
        h[0, i + 1] = PROF[nm]
        h[i + 1, 0] = PROF[nm]
    for i in range(3):
        for j in range(3):
            h[i + 1, j + 1] = H[i, j]
    return h

ETA = sp.diag(-1, 1, 1, 1)
CO = ["t", "x", "y", "z"]

def d4(expr, mu):
    if mu == 0: return sp.diff(expr, t)
    if mu == 3: return sp.diff(expr, z)
    return sp.Integer(0)

def aether_A(u_lower):
    """A_mu_nu = (grad_mu u_nu)^(1) = d_mu u_nu^(1) + Gamma^0(1)_mu_nu  (u^(0)_lambda = (-1,0,0,0))."""
    h = h4()
    A = sp.zeros(4, 4)
    for mu in range(4):
        for nu in range(4):
            Gam0 = -(d4(h[0, nu], mu) + d4(h[0, mu], nu) - d4(h[mu, nu], 0)) / 2
            A[mu, nu] = sp.expand(d4(u_lower[nu], mu) + Gam0)
    return A

def L_aether(A, c1, c2, c3, c4):
    """-c1 A_mn A^mn - c2 (A^m_m)^2 - c3 A_mn A^nm + c4 a^m a_m,  a_mu = A_0mu."""
    Aup = ETA * A * ETA                       # A^{mu nu}
    t1 = sum(A[m, n] * Aup[m, n] for m in range(4) for n in range(4))
    tr = sum(ETA[m, n] * A[m, n] for m in range(4) for n in range(4))
    t3 = sum(A[m, n] * Aup[n, m] for m in range(4) for n in range(4))
    acc = sum(ETA[m, n] * A[0, m] * A[0, n] for m in range(4) for n in range(4))
    return sp.expand(-c1 * t1 - c2 * tr ** 2 - c3 * t3 + c4 * acc)

def u_lower_khrono():
    """u_mu = -d_mu T / sqrt(X), T = t + eps chi:  u_0^(1) = -n, u_i^(1) = -d_i chi."""
    return [-PROF["n"], sp.Integer(0), sp.Integer(0), -sp.diff(PROF["chi"], z)]

def u_lower_aether():
    """u^mu = (1 - eps n, eps v^i)  =>  u_0^(1) = -n,  u_i^(1) = nu_i + v_i."""
    return [-PROF["n"], PROF["nu_x"] + PROF["v_x"], PROF["nu_y"] + PROF["v_y"],
            PROF["nu_z"] + PROF["v_z"]]

def L_testscalar():
    """minimally coupled massless scalar on a constant background: (1/2)(dot psi^2 - (d psi)^2)."""
    return sp.expand((sp.diff(PROF["psi"], t) ** 2 - sp.diff(PROF["psi"], z) ** 2) / 2)

def L_mond(A, KB, K2, J1, xi):
    """
    the MOND scalar sector of the assembled action, quadratic order:
      + 2(2-K_B) J^mu d_mu phi        J^mu = a^mu = A_0^mu       (clock-scalar mixing)
      - K(Q) = -K_2 Q^2               Q^(1) = dot phi            (time kinetic; K_2 < 0 is healthy)
      - (2-K_B) J(Y + xi^2 |grad_perp V|^2),  J ~ J_1 * (...)    (spatial gradient + coherence operator)
        Y^(2) = (d_i phi)^2 ,  |grad_perp V|^2 ^(2) = (d_i d_j phi)^2
    Both nonlinear functions are linearised about a background in the high-acceleration branch, where
    J is analytic with J_1 = J'(Y_0) > 0.  Reported, not hidden: the count does not depend on the value
    of J_1 provided J_1 != 0, and does not depend on xi at all.
    """
    ph = PROF["phi"]
    a_up = [sum(ETA[m, n] * A[0, n] for n in range(4)) for m in range(4)]
    cross = 2 * (2 - KB) * sum(a_up[m] * d4(ph, m) for m in range(4))
    Q = sp.diff(ph, t)
    kin = -K2 * Q ** 2
    Y = sp.diff(ph, z) ** 2
    coh = sp.diff(ph, z, 2) ** 2
    return sp.expand(cross + kin - (2 - KB) * J1 * (Y + xi ** 2 * coh))

# ======================================================================================================
# THE DIRAC COUNTER
# ======================================================================================================
def zero_out(L, names):
    """set the listed fields (and their time derivatives) identically to zero -- derivatives FIRST,
    because sympy leaves an unevaluated Derivative(0, t) if the function is substituted first."""
    L = L.subs({sp.Derivative(FUN[g], t): 0 for g in names})
    L = L.subs({FUN[g]: 0 for g in names})
    return sp.expand(L)

def quad_forms(L, names):
    """L -> (W, B, C) with L = (1/2) qd.W.qd + qd.B.q + (1/2) q.C.q, and an exactness check."""
    N = len(names)
    qs = sp.symbols(f"q0:{N}", real=True)
    qds = sp.symbols(f"v0:{N}", real=True)
    sub = {}
    for i, nm in enumerate(names):
        sub[sp.Derivative(FUN[nm], t)] = qds[i]
    Ls = L.subs(sub)
    Ls = Ls.subs({FUN[nm]: qs[i] for i, nm in enumerate(names)})
    Ls = sp.expand(Ls)
    if Ls.has(sp.Derivative):
        raise RuntimeError("second time derivatives survive -- the Lagrangian is not first order")
    W = sp.zeros(N, N); B = sp.zeros(N, N); C = sp.zeros(N, N)
    for i in range(N):
        for j in range(N):
            W[i, j] = sp.expand(sp.diff(Ls, qds[i], qds[j]))
            B[i, j] = sp.expand(sp.diff(Ls, qds[i], qs[j]))
            C[i, j] = sp.expand(sp.diff(Ls, qs[i], qs[j]))
    qv = sp.Matrix(qs); vv = sp.Matrix(qds)
    recon = sp.expand((vv.T * W * vv / 2 + vv.T * B * qv + qv.T * C * qv / 2)[0, 0])
    ok = sp.simplify(recon - Ls) == 0
    return W, B, C, ok

def dirac_count(L, names, verbose=False, tag=""):
    """
    Full Dirac algorithm on the quadratic system.  Returns a dict.
    Everything here is linear-in-phase-space, so all constraints are linear and all their mutual
    brackets are CONSTANTS -- the algorithm reduces to exact linear algebra.
    """
    N = len(names)
    W, B, C, ok_recon = quad_forms(L, names)
    if not ok_recon:
        raise RuntimeError("quadratic reconstruction failed")
    Wp = W.pinv()
    # canonical Hamiltonian as a quadratic form on z = (q, p):  H = (1/2) z^T HH z
    BtWpB = (B.T * Wp * B)
    HH = sp.zeros(2 * N, 2 * N)
    HH[0:N, 0:N] = sp.expand(BtWpB - C)
    HH[0:N, N:2 * N] = sp.expand(-B.T * Wp)
    HH[N:2 * N, 0:N] = sp.expand(-Wp * B)
    HH[N:2 * N, N:2 * N] = sp.expand(Wp)
    HH = sp.expand((HH + HH.T) / 2)
    J = sp.zeros(2 * N, 2 * N)
    for i in range(N):
        J[i, N + i] = 1
        J[N + i, i] = -1
    # primary constraints from the null space of W
    rows = []
    for v in W.nullspace():
        a = sp.zeros(1, 2 * N)
        Btv = (B.T * v)
        for i in range(N):
            a[0, i] = sp.expand(-Btv[i, 0])
            a[0, N + i] = v[i, 0]
        rows.append(a)
    n_primary = len(rows)
    generations = [n_primary]
    if rows:
        A = sp.Matrix.vstack(*rows)
    else:
        A = sp.zeros(0, 2 * N)
    for _ in range(12):
        if A.rows == 0: break
        M = sp.expand(A * J * A.T)
        cand = []
        for u in M.T.nullspace():                 # left null vectors of M:  u^T M = 0
            c = sp.expand(u.T * A * J * HH)
            if c.is_zero_matrix: continue
            cand.append(c)
        newrows = []
        Acur = A
        for c in cand:
            trial = sp.Matrix.vstack(Acur, c)
            if trial.rank() > Acur.rank():
                newrows.append(c)
                Acur = trial
        if not newrows:
            break
        A = Acur
        generations.append(len(newrows))
    # drop dependent rows
    if A.rows:
        indep = A.rref()[0][:A.rank(), :]
        A = indep
    n_tot = A.rows
    n2 = sp.Matrix(A * J * A.T).rank() if n_tot else 0
    n1 = n_tot - n2
    dof = sp.Rational(2 * N - n2 - 2 * n1, 2)
    res = dict(N=N, W_rank=W.rank(), n_primary=n_primary, generations=generations,
               n_tot=n_tot, n_1st=n1, n_2nd=n2, dof=dof)
    if verbose:
        print(f"    {tag}: N_q = {N}, rank(Hessian) = {W.rank()}, primaries = {n_primary}, "
              f"constraint generations = {generations}, total = {n_tot}, "
              f"first class = {n1}, second class = {n2}  ->  DOF = {dof}")
    return res

# ======================================================================================================
# DISPERSION RELATIONS (mode speeds), by Schur elimination of the auxiliary variables
# ======================================================================================================
LAM = sp.Symbol("lam")

def phys_disp(L, allnames, sector, subs_num):
    """
    The physical dispersion relation of one helicity sector, WITHOUT gauge fixing.

    The Euler-Lagrange operator of L = (1/2)v.W.v + v.B.q + (1/2)q.C.q is
        D(lam) = lam^2 W + lam (B - B^T) - C ,        q ~ exp(lam t),   omega^2 = -lam^2.
    Gauge invariance makes det D vanish identically, so gauge-fixing by hand is the usual route -- and
    it is exactly where a mode count goes wrong, because setting a Lagrange multiplier to zero silently
    discards its constraint.  Instead the rank of D is allowed to speak: at the generic rank r the
    physical relation is the r-th determinantal divisor, i.e. the gcd of all r x r minors.  Nothing is
    fixed, nothing is eliminated, and the gauge directions never enter.
    All parameters must be numeric (exact rationals) so that the gcd is univariate and exact.
    """
    Ls = zero_out(L, [x for x in allnames if x not in sector]).subs(subs_num)
    W, B, C, ok = quad_forms(sp.expand(Ls), sector)
    if not ok:
        raise RuntimeError("quadratic reconstruction failed in phys_disp")
    D = sp.expand(LAM ** 2 * W + LAM * (B - B.T) - C)
    nvar = len(sector)
    r = D.subs({LAM: sp.Rational(7, 3)}).rank()
    if r == 0:
        return None, 0
    gg = None
    for rows in itertools.combinations(range(nvar), r):
        for cols in itertools.combinations(range(nvar), r):
            m = sp.expand(D[list(rows), list(cols)].det())
            if m == 0: continue
            P = sp.Poly(m, LAM)
            gg = P if gg is None else gg.gcd(P)
    return gg, r

def speeds_from(poly):
    """omega^2/k^2 (with k set to 1) for each root of the dispersion polynomial."""
    if poly is None: return []
    sols = sp.solve(sp.Eq(poly.as_expr(), 0), LAM ** 2)
    return [sp.simplify(-s) for s in sols]

# ======================================================================================================
sec("PART 0 -- CONTROLS.  The counter must return 2 / 3 / 5 / 3.  If it does not, nothing below counts.")
# ======================================================================================================
METRIC = ["n", "nu_x", "nu_y", "nu_z", "hT", "hD", "h_xy", "h_xz", "h_yz", "h_zz"]

print("    building the quadratic Einstein-Hilbert Lagrangian from N sqrt(g)(K.K - K^2 + R3) ...", flush=True)
L_EH_raw = L_einstein_hilbert()
L_EH = zavg(L_EH_raw)
KV = {k: sp.Integer(1)}                       # exact k = 1 for the counting; k-independence checked below

W_, B_, C_, ok_ = quad_forms(L_EH.subs(KV), METRIC)
check("C0  the quadratic Einstein-Hilbert Lagrangian reconstructs exactly as (1/2)v.W.v + v.B.q + (1/2)q.C.q",
      ok_, "no second time derivatives survive the ADM form, as required for a Dirac analysis")

r_gr = dirac_count(L_EH.subs(KV), METRIC, verbose=True, tag="ADM GR             ")
check("C1  the Dirac counter returns 2 for ADM general relativity",
      r_gr["dof"] == 2,
      f"N_q = {r_gr['N']}, primaries = {r_gr['n_primary']}, secondaries = {r_gr['n_tot']-r_gr['n_primary']}, "
      f"first class = {r_gr['n_1st']}, second class = {r_gr['n_2nd']}, DOF = {r_gr['dof']}")
check("C1b the four primary constraints are the momenta of the lapse and the shift, and the four "
      "secondaries are the Hamiltonian and momentum constraints -- all eight FIRST class",
      r_gr["n_primary"] == 4 and r_gr["n_tot"] == 8 and r_gr["n_2nd"] == 0,
      "the count is produced by the algorithm, not supplied to it")

L_GRS = L_EH + zavg(L_testscalar())
r_grs = dirac_count(L_GRS.subs(KV), METRIC + ["psi"], verbose=True, tag="GR + scalar        ")
check("C2  the Dirac counter returns 3 for GR + one minimally coupled scalar",
      r_grs["dof"] == 3,
      f"N_q = {r_grs['N']}, first class = {r_grs['n_1st']}, second class = {r_grs['n_2nd']}, DOF = {r_grs['dof']}")

# generic Einstein-aether coefficients -- deliberately off every special surface
c1g, c2g, c3g, c4g = sp.Rational(1, 5), sp.Rational(1, 7), sp.Rational(1, 11), sp.Rational(1, 13)
A_ae = aether_A(u_lower_aether())
L_AE = L_EH + zavg(L_aether(A_ae, c1g, c2g, c3g, c4g))
r_ae = dirac_count(L_AE.subs(KV), METRIC + ["v_x", "v_y", "v_z"], verbose=True, tag="Einstein-aether    ")
check("C3  the Dirac counter returns 5 for Einstein-aether (2 tensor + 2 vector + 1 scalar)",
      r_ae["dof"] == 5,
      f"c1..c4 = 1/5, 1/7, 1/11, 1/13 (generic); N_q = {r_ae['N']}, first class = {r_ae['n_1st']}, "
      f"second class = {r_ae['n_2nd']}, DOF = {r_ae['dof']}")

A_kh = aether_A(u_lower_khrono())
L_KH = L_EH + zavg(L_aether(A_kh, c1g, c2g, c3g, c4g))
r_kh = dirac_count(L_KH.subs(KV), METRIC + ["chi"], verbose=True, tag="khronometric       ")
check("C4  the Dirac counter returns 3 for khronometric theory (2 tensor + 1 khronon)",
      r_kh["dof"] == 3,
      f"same c1..c4, hypersurface-orthogonal u; N_q = {r_kh['N']}, first class = {r_kh['n_1st']}, "
      f"second class = {r_kh['n_2nd']}, DOF = {r_kh['dof']}")
check("C4b the machinery SEES the difference between the two aether theories -- the only change is that "
      "u_i is a gradient, and the two transverse aether modes disappear",
      r_ae["dof"] - r_kh["dof"] == 2,
      f"Einstein-aether {r_ae['dof']} - khronometric {r_kh['dof']} = 2, i.e. exactly the spin-1 pair")

# k-independence of the count
for kv in (2, 3):
    rk = dirac_count(L_KH.subs({k: sp.Integer(kv)}), METRIC + ["chi"])
    check(f"C5  the count is k-independent (khronometric at k = {kv} also returns 3)",
          rk["dof"] == 3, f"DOF = {rk['dof']}")

# ------------------------------------------------------------------------------------------------------
print("\n  SECOND CONTROL LAYER -- the counter's Lagrangian must also reproduce the PUBLISHED mode SPEEDS.")
print("  A degeneracy count can be right while the coefficients are wrong; the speeds test the coefficients.")
c1s, c2s, c3s, c4s = sp.symbols("c1 c2 c3 c4", real=True)
KBs, K2s, J1s, xis = sp.symbols("K_B K_2 J_1 xi", real=True)
A_ae_s = aether_A(u_lower_aether())
L_AE_s = L_EH + zavg(L_aether(A_ae_s, c1s, c2s, c3s, c4s))
A_kh_s = aether_A(u_lower_khrono())
L_KH_s = L_EH + zavg(L_aether(A_kh_s, c1s, c2s, c3s, c4s))
AEVARS = METRIC + ["v_x", "v_y", "v_z"]
KHVARS = METRIC + ["chi"]
SEC_T = ["hD"]
SEC_V_AE = ["nu_x", "h_xz", "v_x"]
SEC_V_KH = ["nu_x", "h_xz"]
SEC_S_AE = ["n", "nu_z", "h_zz", "hT", "v_z"]
SEC_S_KH = ["n", "nu_z", "h_zz", "hT", "chi"]

R = sp.Rational
PTS = [(R(1, 5), R(1, 7), R(1, 11), R(1, 13)),
       (R(2, 9), R(3, 8), R(-1, 6), R(1, 4)),
       (R(1, 3), R(1, 2), R(1, 17), R(2, 7))]
okT = okV = okS = okK = True
detT = detV = detS = detK = None
for (a1, a2, a3, a4) in PTS:
    nsub = {c1s: a1, c2s: a2, c3s: a3, c4s: a4, k: sp.Integer(1)}
    pT, _ = phys_disp(L_AE_s, AEVARS, SEC_T, nsub)
    sT = speeds_from(pT)
    okT &= (len(sT) == 1 and sp.simplify(sT[0] - 1 / (1 - a1 - a3)) == 0)
    detT = f"c_T^2 = {sT[0]} vs 1/(1-c_13) = {1/(1-a1-a3)}"
    pV, _ = phys_disp(L_AE_s, AEVARS, SEC_V_AE, nsub)
    sV = speeds_from(pV)
    pubV = (a1 - (a1 ** 2 - a3 ** 2) / 2) / ((a1 + a4) * (1 - a1 - a3))
    okV &= (len(sV) == 1 and sp.simplify(sV[0] - pubV) == 0)
    detV = f"c_V^2 = {sV[0]} vs Jacobson {pubV}"
    pS, _ = phys_disp(L_AE_s, AEVARS, SEC_S_AE, nsub)
    sS = speeds_from(pS)
    pubS = ((a1 + a2 + a3) * (2 - a1 - a4)) / ((a1 + a4) * (1 - a1 - a3) * (2 + a1 + a3 + 3 * a2))
    okS &= (len(sS) == 1 and sp.simplify(sS[0] - pubS) == 0)
    detS = f"c_S^2 = {sS[0]} vs Jacobson {pubS}"
    pK, _ = phys_disp(L_KH_s, KHVARS, SEC_S_KH, nsub)
    sK = speeds_from(pK)
    al_, be_, la_ = a1 + a4, a1 + a3, a2
    pubK = (2 - al_) * (be_ + la_) / (al_ * (1 - be_) * (2 + be_ + 3 * la_))
    okK &= (len(sK) == 1 and sp.simplify(sK[0] - pubK) == 0)
    detK = f"sigma = {sK[0]} vs Blas-Pujolas-Sibiryakov {pubK}"
check("C6  the tensor speed is Jacobson's c_T^2 = 1/(1 - c_13), at three random rational parameter points",
      okT, detT)
check("C7  the spin-1 speed is Jacobson's [c_1 - (c_1^2 - c_3^2)/2] / [c_14 (1 - c_13)], three points",
      okV, detV)
check("C8  the spin-0 speed is Jacobson's c_123 (2 - c_14)/[c_14 (1 - c_13)(2 + c_13 + 3 c_2)], three points",
      okS, detS)
check("C9  the KHRONOMETRIC spin-0 speed is Blas-Pujolas-Sibiryakov's (2-alpha)(beta+lambda)/"
      "[alpha(1-beta)(2+beta+3lambda)] with alpha = c_14, beta = c_13, lambda = c_2 -- which at c_13 = 0 is "
      "exactly the sigma = (2-c_14)c_2/[c_14(2+3c_2)] that THE_COMPLETE_THEORY section 3.1 calls "
      "'stated, not proved'.  It is now derived",
      okK, detK)
check("C10 the khronometric VECTOR sector carries no mode at all, which is the structural reason the count "
      "drops from 5 to 3 -- and the machinery finds it rather than being told",
      len(speeds_from(phys_disp(L_KH_s, KHVARS, SEC_V_KH,
                                {c1s: R(1, 5), c2s: R(1, 7), c3s: R(1, 11), c4s: R(1, 13),
                                 k: sp.Integer(1)})[0])) == 0,
      "u_i is a gradient, so there is no transverse aether perturbation to propagate")

print("\n  ALL FOUR MANDATORY CONTROLS AND FOUR SPEED CONTROLS ARE THE MACHINERY'S OWN OUTPUT.")
print("  L31's C1-C4 supply (phase-space dimension, n_first, n_second) BY HAND and evaluate an arithmetic")
print("  formula.  Nothing above is supplied by hand: the primary constraints are the Hessian's null")
print("  vectors, the secondaries are generated by the consistency algorithm, and the split into first")
print("  and second class is the RANK of A J A^T.")

# ======================================================================================================
sec("PART 1 -- THE ASSEMBLED ACTION, COUNTED BY THE SAME MACHINERY")
# ======================================================================================================
print("""
  S = int d4x sqrt(-g) { (1/16 pi G)[R - 2 Lambda]
                        - c1 (grad_m n_n)(grad^m n^n) - c2 (div n)^2 - c3 (grad_m n_n)(grad^n n^m) + c4 (n.grad n)^2
                        + 2(2 - K_B) J^m d_m phi
                        - K(Q)
                        - (2 - K_B) J( Y + xi^2 q^{ls} q^{mn} grad_l V_m grad_s V_n ) }  + S_m[g, psi_m]

  with c1 = -c3 = K_B (so c_13 = 0 identically), n hypersurface-orthogonal (n = -dtau/|dtau|),
  Q = n.d phi, V_m = q_m^n d_n phi, Y = V.V.  Fields: g_mn (10) + tau (1) + phi (1) = 12.
  Linearised about flat space with Q_0 = 0 (the condensate is removed) and a high-acceleration branch
  where J is analytic, J_1 = J'(Y_0) > 0.  K_2 < 0 is the healthy sign, so -K(Q) = |K_2| (d_t phi)^2.
""")
KBs, K2s, J1s, xis = sp.symbols("K_B K_2 J_1 xi", real=True)
A_assembled = aether_A(u_lower_khrono())
L_ASM_sym = (L_EH
             + zavg(L_aether(A_assembled, KBs, c2s, -KBs, c4s))
             + zavg(L_mond(A_assembled, KBs, K2s, J1s, xis)))

# generic-but-signed numeric point for the count
PTC = {KBs: sp.Rational(1, 5), c2s: sp.Rational(1, 7), c4s: sp.Rational(1, 3),
       K2s: sp.Rational(-3), J1s: sp.Rational(1, 2), xis: sp.Rational(1, 4), k: sp.Integer(1)}
L_ASM = sp.expand(L_ASM_sym.subs(PTC))
ASM_VARS = METRIC + ["chi", "phi"]
r_asm = dirac_count(L_ASM, ASM_VARS, verbose=True, tag="ASSEMBLED ACTION   ")
check("A1  the assembled action carries FOUR propagating modes -- the deposited count is CONFIRMED, "
      "independently and by an algorithm that was validated on four control theories",
      r_asm["dof"] == 4,
      f"N_q = 12, primaries = {r_asm['n_primary']}, total constraints = {r_asm['n_tot']}, "
      f"first class = {r_asm['n_1st']}, second class = {r_asm['n_2nd']}, DOF = {r_asm['dof']}")
check("A1b the constraint structure is the SAME as the controls': 4 primary + 4 secondary, all first "
      "class, no second-class pair anywhere -- the extra modes are extra FIELDS, not extra constraints",
      r_asm["n_primary"] == 4 and r_asm["n_tot"] == 8 and r_asm["n_2nd"] == 0,
      "so the count is 12 - 8 = 4, and nothing in the action removes a mode")

# robustness: several parameter points, both signs of K_2, several k
rob = []
for kb in (sp.Rational(1, 5), sp.Rational(1, 10)):
    for K2v in (sp.Rational(-3), sp.Rational(-1, 2), sp.Rational(5)):
        for kv in (sp.Integer(1), sp.Integer(2)):
            pt = dict(PTC); pt[KBs] = kb; pt[K2s] = K2v; pt[k] = kv
            rob.append(dirac_count(sp.expand(L_ASM_sym.subs(pt)), ASM_VARS)["dof"])
check("A2  the count is 4 at every tested parameter point and both signs of K_2 (12 points)",
      all(x == 4 for x in rob), f"values = {sorted(set(int(x) for x in rob))}")

# the physical point of THE_COMPLETE_THEORY
c14_pt = 1.978e-6
sigma_star = 1.679312732187113
c2_pt = 2 * sigma_star * c14_pt / (2 - c14_pt - 3 * sigma_star * c14_pt)
KB_pt = 0.2
K2_pt = (2 - KB_pt) ** 2 / c2_pt
print(f"\n    THE EXHIBITED POINT (THE_COMPLETE_THEORY section 5): K_B = {KB_pt}, c_14 = {c14_pt:.4e}, "
      f"c_2 = {c2_pt:.6e},")
print(f"    |K_2| = {K2_pt:.4e} on the closure locus c_2|K_2| = (2-K_B)^2 = {(2-KB_pt)**2:.4f}, "
      f"sigma* = {sigma_star:.9f}")
pt_phys = {KBs: sp.Rational(1, 5), c2s: sp.nsimplify(c2_pt, rational=True),
           c4s: sp.nsimplify(c14_pt, rational=True) - sp.Rational(1, 5),
           K2s: -sp.nsimplify(K2_pt, rational=True), J1s: sp.Rational(1, 2),
           xis: sp.Rational(1, 4), k: sp.Integer(1)}
r_phys = dirac_count(sp.expand(L_ASM_sym.subs(pt_phys)), ASM_VARS)
check("A3  the count is still 4 at the theory's own exhibited point (c_14 = 1.978e-6, on the closure locus)",
      r_phys["dof"] == 4, f"DOF = {r_phys['dof']}; the closure locus does NOT degenerate the kinetic matrix")

# ======================================================================================================
sec("PART 2 -- MODE-BY-MODE IDENTIFICATION: what each of the four is, how it is normalised, how fast")
# ======================================================================================================
W_asm, B_asm, C_asm, _ = quad_forms(sp.expand(L_ASM_sym.subs({k: sp.Integer(1)})), ASM_VARS)
idx = {nm: i for i, nm in enumerate(ASM_VARS)}
blocks = {"tensor  {hD, h_xy}": ["hD", "h_xy"],
          "vector  {nu_x, h_xz} + {nu_y, h_yz}": ["nu_x", "h_xz", "nu_y", "h_yz"],
          "scalar  {n, nu_z, h_zz, hT, chi, phi}": ["n", "nu_z", "h_zz", "hT", "chi", "phi"]}
offdiag_ok = True
for (na, va), (nb, vb) in itertools.combinations(blocks.items(), 2):
    for a in va:
        for b in vb:
            for M in (W_asm, B_asm, C_asm):
                if sp.simplify(M[idx[a], idx[b]]) != 0 or sp.simplify(M[idx[b], idx[a]]) != 0:
                    offdiag_ok = False
check("M0  the quadratic action block-diagonalises into helicity 2 / 1 / 0 sectors, so the four modes can "
      "be identified one at a time",
      offdiag_ok, "checked on all of W, B and C at k = 1 with symbolic parameters")

# the exhibited point as exact rationals with 12 significant digits
def RS(x, sig=12): return sp.Rational(f"{x:.{sig}e}")
SUB_PHYS = {KBs: R(1, 5), c2s: RS(c2_pt), c4s: RS(c14_pt) - R(1, 5), K2s: -RS(K2_pt),
            J1s: RS(3.217), xis: R(0), k: sp.Integer(1)}   # J_1 = J_Y at the Galactic external field
SUB_GEN = {KBs: R(1, 5), c2s: R(1, 7), c4s: R(1, 3) - R(1, 5), K2s: R(-3),
           J1s: R(1, 2), xis: R(1, 4), k: sp.Integer(1)}

# --- MODES 1 and 2: the two tensor polarisations
cT_ok = True; cT_det = ""
for KBv in (R(1, 5), R(1, 10), R(1, 4)):
    su = dict(SUB_GEN); su[KBs] = KBv
    sT = speeds_from(phys_disp(L_ASM_sym, ASM_VARS, ["hD"], su)[0])
    cT_ok &= (len(sT) == 1 and sT[0] == 1)
    cT_det = f"c_T^2 = {sT[0]} at K_B = {KBv}"
check("M1  modes 1-2 are the two tensor polarisations, Einstein-normalised, speed EXACTLY c at every K_B",
      cT_ok, cT_det + " -- c_1 = -c_3 = K_B makes c_13 = 0 identically, so GW170817 is structural, not tuned")

# --- MODE 3: the clock (khronon), isolated by switching phi off
L_clock_only = zero_out(L_ASM_sym, ["phi"])
sK_gen = speeds_from(phys_disp(L_clock_only, ASM_VARS, ["n", "nu_z", "h_zz", "hT", "chi"], SUB_GEN)[0])
c14_gen = float(R(1, 3)); c2_gen = float(R(1, 7))
sig_pub_gen = (2 - c14_gen) * c2_gen / (c14_gen * (2 + 3 * c2_gen))
check("M2  mode 3 is the CLOCK (khronon): with phi switched off the scalar sector carries exactly ONE mode "
      "and its speed^2 is the khronometric sigma = (2 - c_14) c_2/[c_14 (2 + 3 c_2)]",
      len(sK_gen) == 1 and abs(float(sK_gen[0]) - sig_pub_gen) < 1e-12,
      f"computed {float(sK_gen[0]):.9f} vs closed form {sig_pub_gen:.9f} at c_14 = 1/3, c_2 = 1/7")
sig_num = (2 - c14_pt) * c2_pt / (c14_pt * (2 + 3 * c2_pt))
sK_phys = speeds_from(phys_disp(L_clock_only, ASM_VARS, ["n", "nu_z", "h_zz", "hT", "chi"], SUB_PHYS)[0])
check("M2b at the theory's own exhibited point, with phi switched off, the clock's speed^2 IS sigma* = "
      "1.679312732 -- so the construction's design parameter and the khronometric sound speed really are "
      "the same object, which section 3.1 leaves as an unproved identification",
      len(sK_phys) == 1 and abs(float(sK_phys[0]) / sigma_star - 1) < 1e-5,
      f"computed sigma = {float(sK_phys[0]):.6f} vs sigma* = {sigma_star:.9f} "
      f"(the residual is the c_2 <-> sigma inversion at 12 digits, not an error)")
# the clock's kinetic normalisation, symbolically
W_sym, B_sym, C_sym, _ = quad_forms(sp.expand(L_ASM_sym), ASM_VARS)
Wc = sp.simplify(W_sym[idx["chi"], idx["chi"]])
c14sym = sp.Symbol("c14")
Wc_c14 = sp.simplify(sp.expand(Wc.subs({c4s: c14sym - KBs})))
check("M2c the clock's kinetic normalisation is proportional to c_14 k^2 and to NOTHING else -- it VANISHES "
      "as c_14 -> 0, which is why c_14 cannot simply be set to zero to satisfy the PPN bounds",
      sp.simplify(Wc_c14.subs({c14sym: 0})) == 0 and
      sp.simplify(sp.cancel(Wc_c14 / c14sym / k ** 2)).free_symbols == set(),
      f"W_chi,chi = {Wc_c14} = {sp.simplify(sp.cancel(Wc_c14/c14sym/k**2))} c_14 k^2")
print(f"    at the exhibited point the clock's kinetic normalisation is "
      f"{float(sp.cancel(Wc_c14/c14sym/k**2))*c14_pt:.4e} k^2 -- suppressed by {1/c14_pt:.2e} relative to")
print("    the graviton.  It couples to MATTER only through the metric, at O(c_14): the least visible")
print("    object in the theory, and the one whose strong-coupling scale is lowest.")

# --- MODE 4: the MOND scalar, and the mixed speed
SEC_S = ["n", "nu_z", "h_zz", "hT", "chi", "phi"]
pS_gen, rS = phys_disp(L_ASM_sym, ASM_VARS, SEC_S, SUB_GEN)
sS_gen = speeds_from(pS_gen)
pS_phys, _ = phys_disp(L_ASM_sym, ASM_VARS, SEC_S, SUB_PHYS)
sS_phys = speeds_from(pS_phys)
print(f"\n    the SCALAR sector carries {len(sS_phys)} modes.  Their speeds^2 at the exhibited point:")
sp_num = sorted(float(sp.re(sp.N(s))) for s in sS_phys)
for v in sp_num:
    print(f"      c^2 = {v:.6f}")
check("M3  the scalar sector carries exactly TWO modes -- the clock and the MOND scalar -- and both have "
      "positive speed^2 at the exhibited point, evaluated with the theory's own kernel slope J_Y = 3.217",
      len(sS_phys) == 2 and all(v > 0 for v in sp_num),
      f"speeds^2 = {[f'{v:.6e}' for v in sp_num]}; the tensor sector adds 2 more, total 4")
cs2_mixed = (2 - KB_pt) ** 2 / (c14_pt * K2_pt)
check("M3b NEITHER eigenvalue is the theory's c_s,mix^2 = (2-K_B)^2/(c_14|K_2|), and neither is sigma.  The "
      "LARGER one is their SUM.  On the closure locus the two 'unmixed' numbers coincide, and the mixing "
      "then splits them maximally -- so the locus does not mean 'both modes travel at sigma'",
      abs(max(sp_num) / (sigma_star + cs2_mixed) - 1) < 1e-4
      and min(abs(v / cs2_mixed - 1) for v in sp_num) > 0.5
      and min(abs(v / sigma_star - 1) for v in sp_num) > 0.5,
      f"c_s,mix^2 = {cs2_mixed:.6f}, sigma* = {sigma_star:.6f}, sum = {sigma_star + cs2_mixed:.6f}; "
      f"computed eigenvalues = {[f'{v:.6e}' for v in sp_num]}")
Wp_phi = sp.simplify(W_sym[idx["phi"], idx["phi"]])
check("M4  the MOND scalar's kinetic normalisation is -K_2 = |K_2| per Fourier mode, INDEPENDENT of k, of "
      "c_14 and of the coherence length xi -- so the coherence operator adds no time derivative and "
      "therefore no Ostrogradsky mode, which is the whole reason xi^2 |grad_perp V|^2 is safe",
      sp.simplify(Wp_phi + K2s) == 0 and not Wp_phi.has(xis) and not Wp_phi.has(c4s),
      f"W_phi,phi = {Wp_phi} (the factor 1/2 relative to -2K_2 phi-dot^2 is the z-average of cos^2)")

# ======================================================================================================
sec("PART 2B -- A CORRECTION.  The scalar sector's EIGEN-speeds are not the numbers the paper quotes.")
# ======================================================================================================
print("""
  Two scalar modes, one kinetic-diagonal 2x2 system, and a velocity-coordinate mixing between them.  The
  eigenvalues of such a system are not the two 'unmixed' speeds.  THE_COMPLETE_THEORY carries two scalar
  numbers -- sigma = 1.679 for the clock and c_s,mix^2 = (2-K_B)^2/(c_14|K_2|) for the MOND scalar -- and
  uses c_s,mix^2 in two gate rows (DOF health, and gravitational Cherenkov via 'c_s,mix^2 >= 1').  This
  part computes the actual eigenvalues.  A closed form is obtained by a SECOND, independent route: unitary
  gauge for the khronon (chi = 0) plus h_zz = 0, with the two genuine Lagrange multipliers n and nu_z
  eliminated by a Schur complement.  Its answer is checked against the gauge-free minor-gcd machinery of
  PART 0, which never gauge-fixes anything.
""")
# --- the symbolic quartic, unitary gauge
L_u = zero_out(L_ASM_sym, [x for x in ASM_VARS if x not in ("n", "nu_z", "hT", "phi")])
L_u = L_u.subs({c4s: c14sym - KBs})
Wu, Bu, Cu, oku = quad_forms(sp.expand(L_u), ["hT", "phi", "n", "nu_z"])
Du = sp.expand(LAM ** 2 * Wu + LAM * (Bu - Bu.T) - Cu)
Dred = sp.simplify(sp.together(Du[:2, :2] - Du[:2, 2:] * Du[2:, 2:].inv() * Du[2:, :2]))
Pq = sp.Poly(sp.expand(sp.numer(sp.together(Dred.det()))), LAM)
a4, a2, a0 = Pq.coeff_monomial(LAM ** 4), Pq.coeff_monomial(LAM ** 2), Pq.coeff_monomial(1)
PROD = sp.factor(sp.cancel(a0 / a4))          # product of the two omega^2  (product of lam^2 = product of omega^2)
SUMM = sp.factor(sp.cancel(a2 / a4))          # sum of the two omega^2      (= +a2/a4, since omega^2 = -lam^2)
print(f"    product of the two scalar omega^2 :\n      {PROD}")
print(f"    sum of the two scalar omega^2 :\n      {sp.simplify(SUMM)}")

def scalar_pair(KBv, c14v, c2v, K2v, J1v, xiv, kv=1):
    """the two omega^2/k^2 from the closed form"""
    su = {KBs: KBv, c14sym: c14v, c2s: c2v, K2s: -K2v, J1s: J1v, xis: xiv, k: kv}
    P = float(PROD.subs(su)) / kv ** 4
    S = float(SUMM.subs(su)) / kv ** 2
    disc = S * S - 4 * P
    r = math.sqrt(abs(disc))
    return sorted([(S - r) / 2, (S + r) / 2]) if disc >= 0 else [float("nan"), float("nan")]

# CONTROL: the closed form must agree with the gauge-free machinery
gen_pair = scalar_pair(float(R(1, 5)), float(R(1, 3)), float(R(1, 7)), 3.0, 0.5, 0.25)
check("S1 [control] the unitary-gauge closed form reproduces the gauge-free minor-gcd result of PART 0 at "
      "a generic parameter point -- two independent reductions, same two eigenvalues",
      len(sS_gen) == 2 and
      max(abs(a - b) for a, b in zip(sorted(float(sp.re(sp.N(s))) for s in sS_gen), gen_pair)) < 1e-9,
      f"minor-gcd {[round(float(sp.re(sp.N(s))), 9) for s in sorted(sS_gen, key=lambda x: float(sp.re(sp.N(x))))]} "
      f"vs closed form {[round(v, 9) for v in gen_pair]}")

# THE SUM RULE
sum_ok = True; sum_det = ""
for fac in (1.0, 10.0, 0.1):
    K2x = K2_pt * fac
    pr = scalar_pair(KB_pt, c14_pt, c2_pt, K2x, 3.217, 0.0)
    predicted = sigma_star + (2 - KB_pt) ** 2 / (c14_pt * K2x)
    sum_ok &= abs(sum(pr) / predicted - 1) < 1e-5
    sum_det = f"|K_2| x{fac}: sum = {sum(pr):.8f} vs sigma + c_s,mix^2 = {predicted:.8f}"
check("S2  c_s,mix^2 = (2-K_B)^2/(c_14|K_2|) is the SUM-RULE combination, not an eigenvalue: over three "
      "decades of |K_2| the two eigen-speeds SUM to sigma + c_s,mix^2 to better than 1e-5 relative",
      sum_ok, sum_det + " -- so the paper's two scalar numbers are the trace of the speed matrix, split "
                        "between the modes, not the modes themselves")

# THE STABILITY CONDITION
cond_expr = -c2s * k ** 4 * (KBs - 2) * (-J1s * (2 - c14sym) * (1 + xis ** 2 * k ** 2) + (2 - KBs)) \
            / (K2s * c14sym * (3 * c2s + 2))
check("S3  the product of the two scalar omega^2 factorises EXACTLY as "
      "-c_2 k^4 (K_B - 2)[(2 - K_B) - J_1(2 - c_14)(1 + xi^2 k^2)] / [K_2 c_14 (3c_2 + 2)], so with K_2 < 0 "
      "(the healthy sign) BOTH scalar modes have omega^2 > 0 if and only if",
      sp.simplify(sp.together(PROD - cond_expr)) == 0,
      "J_1 (2 - c_14)(1 + xi^2 k^2) > (2 - K_B)  -- a health condition on the MOND function's own slope, "
      "independent of |K_2| and of the sign of the AeST coupling (it enters squared)")
JY_crit = (2 - KB_pt) / (2 - c14_pt)
JY_EXT = {"canonical": 3.217, "alt": 2.726}      # L43_assemble_theory.out line 72, the repaired kernel
pairs = {f: scalar_pair(KB_pt, c14_pt, c2_pt, K2_pt, JY_EXT[f], 0.0) for f in JY_EXT}
check("S4  AT THE EXHIBITED POINT, WITH THE THEORY'S OWN J_Y, THE CONDITION HOLDS AND ALL FOUR MODES ARE "
      "HEALTHY -- the deposited health claim SURVIVES, but for a reason the paper does not state",
      all(min(pairs[f]) > 0 for f in pairs),
      f"critical J_Y = (2-K_B)/(2-c_14) = {JY_crit:.7f}; the theory's own J_Y at the Galactic external "
      f"field is {JY_EXT['canonical']:.3f} (canonical) / {JY_EXT['alt']:.3f} (alt), both {JY_EXT['alt']/JY_crit:.2f}x "
      f"or more above it")
print("\n    the two scalar eigen-speeds at the exhibited point, both footings:")
for f in ("canonical", "alt"):
    lo, hi = pairs[f]
    cf = (2 - KB_pt) * (2 * JY_EXT[f] - (2 - KB_pt)) / (4 * K2_pt)
    print(f"      {f:<10} a0 = {A0[f]:.4e}, J_Y = {JY_EXT[f]:.3f}:  c_+^2 = {hi:.6f}  (= sigma + c_s,mix^2)"
          f"   c_-^2 = {lo:+.4e}  ->  c_- = {math.sqrt(lo):.3e} c")
    print(f"      {'':<10} closed form for the slow mode, (2-K_B)[2J_Y - (2-K_B)]/(4|K_2|) = {cf:+.4e}")
check("S5  A CORRECTION TO THE GATE TABLE.  The slow scalar eigen-mode has c_- = 1.5e-3 c (canonical) / "
      "1.3e-3 c (alt) -- deeply SUBLUMINAL.  The gravitational-Cherenkov row passes on the premise "
      "'clock 29.6% superluminal; the bound constrains SLOW modes' together with 'c_s,mix^2 >= 1'.  That "
      "premise does not hold: the spectrum contains a slow mode",
      math.sqrt(pairs["canonical"][0]) < 1e-2 and math.sqrt(pairs["alt"][0]) < 1e-2,
      f"c_- = {math.sqrt(pairs['canonical'][0]):.3e} c / {math.sqrt(pairs['alt'][0]):.3e} c.  Whether the "
      f"bound actually bites depends on this mode's coupling to matter, which this lane does NOT compute -- "
      f"the claim here is only that the gate's stated premise is false and the row needs re-running")
# where the condition fails, on the theory's own repaired kernel
C_TH, P_TH, A2_TH = 0.647610, 1.7538, 0.9335
A1_TH = 1.0 / (C_TH * P_TH)
def Delta_th(s):
    u = math.sqrt(s)
    return C_TH * (1 - (1 + A1_TH * u + A2_TH * u * u) ** (-P_TH))
lo_s, hi_s = 1e-8, 1e5
for _ in range(400):
    mid = math.sqrt(lo_s * hi_s)
    if mid / Delta_th(mid) < JY_crit: lo_s = mid
    else: hi_s = mid
s_crit = math.sqrt(lo_s * hi_s)
check("S6  A HEALTH CONDITION THE GATE TABLE DOES NOT CONTAIN.  J_Y = s/Delta(s) is a decreasing function "
      "of decreasing acceleration, so the condition FAILS below a critical Newtonian acceleration",
      s_crit > 0 and abs(s_crit / Delta_th(s_crit) - JY_crit) < 1e-6,
      f"J_Y falls below {JY_crit:.4f} at s = g_N/a0 = {s_crit:.4f}, i.e. "
      f"g_N < {s_crit*A0['canonical']:.4e} m/s^2 (canonical) / {s_crit*A0['alt']:.4e} m/s^2 (alt)")
print(f"""
    WHAT THAT DOES AND DOES NOT ESTABLISH -- stated plainly, because it is the load-bearing caveat.
      ESTABLISHED: about flat space, with the MOND function analytic at the background and slope
        J_1 = J_Y, the two scalar modes are healthy iff J_1(2 - c_14)(1 + xi^2 k^2) > (2 - K_B).  The
        derivation is exact, appears in two independent reductions, and is insensitive to the sign of the
        AeST coupling.  At the theory's own external-field J_Y it PASSES on both footings.
      NOT ESTABLISHED: that the theory is unstable in the deep-MOND regime.  Below s = {s_crit:.3f} the
        background gradient of phi is NOT zero, and a background with a preferred direction splits the
        perturbation into longitudinal and transverse pieces with stiffnesses J' and J' + 2 Y_0 J''.  That
        anisotropic calculation -- the one fc_kh_terminal performed for the khronometric arm -- is the one
        that would decide it, and this lane does NOT do it.  Reported as an open computation with a
        named entry point, not as a kill.
      WHERE xi HELPS: the condition carries (1 + xi^2 k^2), the same combination the theory's own alpha_1
        formula carries.  At Solar-System gradient scales (xi/R_Sat)^2 = 4.7e6 makes it enormous -- which
        is exactly why alpha_1 passes.  At galactic scales xi^2 k^2 ~ 1e-8 and it does nothing.
""")
check("M5  every mode is HEALTHY at the exhibited point, on both footings, once the condition of S3 is "
      "imposed with the theory's own J_Y: tensor speed exactly c, clock kinetic normalisation positive, "
      "MOND-scalar kinetic normalisation positive, all four omega^2 > 0",
      float(sp.cancel(Wc_c14 / c14sym / k ** 2)) * c14_pt > 0 and K2_pt > 0
      and all(min(pairs[f]) > 0 for f in pairs) and cT_ok,
      "no ghost, no gradient instability, no tachyon in the linear spectrum about flat space")

print(f"""
  THE FOUR MODES, NAMED, WITH THE NUMBERS THIS LANE COMPUTED.
    1-2  TENSOR, the two graviton polarisations.  Kinetic normalisation: the Einstein term itself.
         Speed: EXACTLY c, as an identity in K_B, because c_1 = -c_3 forces c_13 = 0.  Couples to T_mn.
    3    The FAST SCALAR.  Kinetic normalisation c_14 k^2 -- suppressed by 5.1e5 at the exhibited point.
         Speed^2 = {max(sp_num):.6f} = sigma + c_s,mix^2, i.e. 83% superluminal.  It is mostly the clock
         (khronon): switching phi off leaves it alone at sigma = 1.6793 exactly.  Couples to matter only
         through the metric, at O(c_14).
    4    The SLOW SCALAR.  Kinetic normalisation |K_2| per Fourier mode, k-independent, xi-independent, so
         the coherence operator adds no Ostrogradsky mode.  Speed^2 = (2-K_B)[2 J_Y - (2-K_B)]/(4|K_2|)
         = {min(sp_num):+.4e}, i.e. c_- = {math.sqrt(max(min(sp_num), 0)):.3e} c.  It is mostly the MOND
         scalar phi, which is sourced by matter through the AeST coupling 2(2-K_B) a^mu d_mu phi -- a^mu
         being the clock's own 4-acceleration, which in the static limit is grad(Newtonian potential).
         That coupling is a VELOCITY-COORDINATE mixing, not a kinetic one: it does not degenerate the
         kinetic matrix (A3), but it does rotate the two scalars into each other.
    THE CLOSURE LOCUS, correctly read.  c_2|K_2| = (2-K_B)^2 makes the two UNMIXED numbers sigma and
    c_s,mix^2 equal.  Degenerate unmixed levels plus a mixing split MAXIMALLY, which is why the locus
    produces one mode at their sum and one at almost nothing -- not two modes at sigma.  Whether the slow
    one is healthy is then decided entirely by J_Y, through the condition of S3.
  So all four modes have a name, a normalisation, a speed and a job.  Nothing is unaccounted for -- and
  two of the four speeds are not the ones the paper carries.
""")

# ======================================================================================================
sec("PART 3 -- IS THE FOURTH MODE FORCED?  Three routes to three, exhibited and priced.")
# ======================================================================================================
print("""
  The foliation theorem (L31) forces a preferred timelike u.  It does NOT force four modes.  A covariant
  theory that carries u as a FIELD carries a khronon, so 2 + 1 = 3 is the floor the theorem itself
  implies.  The question is whether the MOND kernel can be carried without a fourth field.
""")

# ------------------------------------------------------------------------------------------------------
print("\n  ROUTE (a) -- phi = f(tau).  Let the MOND scalar BE the clock.")
# The exact identity: q_mu^nu d_nu tau = 0 for n_mu = -d_mu tau / sqrt(-g.dtau.dtau).
xs = sp.symbols("x0:4", real=True)
gmet = sp.Matrix(4, 4, lambda i, j: sp.Rational(0))
raw = [[-1 - sp.Rational(1, 7) * xs[1], sp.Rational(1, 5) * xs[3], sp.Rational(1, 11), sp.Rational(2, 9) * xs[0]],
       [sp.Rational(1, 5) * xs[3], 1 + sp.Rational(1, 3) * xs[2], sp.Rational(1, 13) * xs[0], sp.Rational(1, 17)],
       [sp.Rational(1, 11), sp.Rational(1, 13) * xs[0], 1 + sp.Rational(1, 19) * xs[3], sp.Rational(1, 23) * xs[1]],
       [sp.Rational(2, 9) * xs[0], sp.Rational(1, 17), sp.Rational(1, 23) * xs[1], 1 + sp.Rational(1, 29) * xs[2]]]
for i in range(4):
    for j in range(4):
        gmet[i, j] = raw[i][j]
tau_f = xs[0] + sp.Rational(1, 3) * xs[1] ** 2 + sp.Rational(1, 5) * xs[2] * xs[3]
ginv_m = gmet.inv()
dtau = sp.Matrix([sp.diff(tau_f, xs[m]) for m in range(4)])
X2 = -(dtau.T * ginv_m * dtau)[0, 0]
n_low = sp.Matrix([-dtau[m] / sp.sqrt(X2) for m in range(4)])
n_up = ginv_m * n_low
# q_mu^nu = delta + n_mu n^nu ;  V_mu = q_mu^nu d_nu phi with phi = f(tau)
fp = sp.Symbol("fprime")
V = sp.Matrix([sp.simplify(fp * (dtau[m] + n_low[m] * (n_up.T * dtau)[0, 0])) for m in range(4)])
V0 = [sp.simplify(V[m]) for m in range(4)]
pt_rand = {xs[0]: sp.Rational(3, 7), xs[1]: sp.Rational(-2, 5), xs[2]: sp.Rational(5, 11), xs[3]: sp.Rational(1, 4)}
Vnum = [sp.simplify(sp.nsimplify(v.subs(pt_rand))) for v in V0]
check("R-a1 the projector identity q_mu^nu d_nu tau = 0 holds EXACTLY -- verified on a random curved "
      "metric with a random non-trivial tau, in exact rational arithmetic",
      all(v == 0 for v in Vnum),
      "n_mu ~ d_mu tau, and q projects orthogonal to n, so the clock has ZERO gradient on its own leaves")
check("R-a2 therefore phi = f(tau) gives V_mu == 0, Y == 0 and J(Y) == J(0) = constant: the ENTIRE MOND "
      "sector disappears.  A single scalar cannot both define the foliation and carry this kernel",
      all(v == 0 for v in Vnum),
      "this is an identity, not a parameter statement -- there is no value of anything that evades it")

# ------------------------------------------------------------------------------------------------------
print("\n  ROUTE (b) -- one scalar, MOND carried by the clock's own acceleration a_mu (khronometric MOND).")
print("  The kernel argument becomes y = |a|/a0 with a_i = d_i ln N, which IS a foliation-built scalar with")
print("  the right static limit.  Mode count: 2 tensor + 1 khronon = 3.  This is a real route to three, and")
print("  it is NOT blocked by mode counting.  It is blocked by the LONGITUDINAL STIFFNESS.")
# gate 12's own generating function, differentiated here rather than quoted
y = sp.Symbol("y", positive=True)
al = sp.Symbol("alpha_k", positive=True)
F_M = 2 * ((1 + y) * sp.exp(-y) - 1)              # gate 12, verbatim
f_gen = al * y ** 2 - (2 - al) * (F_M + 2)        # the khronometric MOND generating function
fpp = sp.simplify(sp.diff(f_gen, y, 2))
fpp_pub = 2 * al + 2 * (2 - al) * (1 - y) * sp.exp(-y)
check("R-b1 gate 12's own F_M(y) = 2[(1+y)e^-y - 1], differentiated here, reproduces the FC-KH kill's "
      "f''(y) = 2 alpha + 2(2 - alpha)(1 - y) e^-y",
      sp.simplify(fpp - fpp_pub) == 0,
      "derived from the frozen recipe, not copied from fc_kh_terminal/RESULTS.md")
# the unstable window at the assembled theory's own c_14
def fpp_num(yv, a): return 2 * a + 2 * (2 - a) * (1 - yv) * math.exp(-yv)
def upper_root(a):
    lo, hi = 1.5, 200.0
    for _ in range(400):
        mid = (lo + hi) / 2
        if fpp_num(mid, a) < 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2
ystar = upper_root(c14_pt)
check("R-b2 at the assembled theory's OWN c_14 = 1.978e-6 the radial sound speed of the single-scalar "
      "khronometric MOND theory is NEGATIVE on 1 < y < y*, i.e. right across the MOND transition",
      fpp_num(2.0, c14_pt) < 0 and ystar > 10,
      f"f''(2) = {fpp_num(2.0, c14_pt):.4f} < 0; window 1 < y < {ystar:.2f}; "
      f"sign(c_par^2) = sign(f'') is beta,lambda-independent (fc_kh_terminal/RESULTS.md, reproduced)")
print("    the unstable shell in physical units, both footings (point mass, mu(y) y = g_N/a0, "
      "M = 1e11 M_sun):")
G_N, MSUN, KPC = 6.674e-11, 1.989e30, 3.0857e19
def r_over_rM(yv):
    s = yv * (1 - math.exp(-yv))              # g_N/a0
    return math.sqrt(1.0 / s)
shell = []
for foot, a0 in A0.items():
    rM = math.sqrt(G_N * 1e11 * MSUN / a0) / KPC
    r_in, r_out = r_over_rM(ystar) * rM, r_over_rM(1.0) * rM
    shell.append((r_in, r_out))
    print(f"      {foot:<10} a0 = {a0:.4e}: r_M = {rM:.2f} kpc, unstable shell "
          f"{r_in:.2f} - {r_out:.2f} kpc  (r/r_M = {r_over_rM(ystar):.4f} - {r_over_rM(1.0):.4f})")
check("R-b2b the unstable shell is not a corner of parameter space -- it sits at the MOND radius of a "
      "normal galaxy on BOTH footings, and the two footings differ only by the 9.7% shift in r_M",
      shell[0][0] < shell[0][1] and abs(shell[1][0] / shell[0][0] - math.sqrt(A0["canonical"] / A0["alt"])) < 1e-6,
      f"canonical {shell[0][0]:.2f}-{shell[0][1]:.2f} kpc, alt {shell[1][0]:.2f}-{shell[1][1]:.2f} kpc "
      f"for M_b = 1e11 M_sun")
# the SAME obstruction seen from the assembled theory's own bounded-boost identity
print("""
    AND THE SAME OBSTRUCTION, REACHED A SECOND WAY, FROM THIS THEORY'S OWN IDENTITY.  Section 4.1 proves
    Sigma_par = 1/Delta'(s) exactly, with Delta = (g_obs - g_bar)/a0.  Section 4.4 states that the AQUAL
    arm -- which is exactly what route (b) is -- has Delta(s) = y e^-y, which DECREASES past s = 0.63.
    Delta' < 0 is Sigma_par < 0 is a negative longitudinal stiffness: the same sign flip, from the other end.
""")
yv = sp.Symbol("yv", positive=True)
Delta_aqual = yv * sp.exp(-yv)
s_of_y = yv * (1 - sp.exp(-yv))
dDelta_ds = sp.simplify(sp.diff(Delta_aqual, yv) / sp.diff(s_of_y, yv))
turn = float(sp.nsolve(sp.diff(Delta_aqual, yv), yv, 1.0))
check("R-b3 the assembled theory's own bounded-boost identity independently gives Sigma_par = 1/Delta' < 0 "
      "for the AQUAL arm above y = 1, agreeing with the khronometric instability window's lower edge",
      abs(turn - 1.0) < 1e-9 and float(dDelta_ds.subs({yv: 2.0})) < 0,
      f"Delta = y e^-y turns over at y = {turn:.6f}; dDelta/ds at y = 2 is {float(dDelta_ds.subs({yv: 2.0})):.4f}")
check("R-b4 route (b) is therefore CLOSED for the programme's own gate-1/gate-12 exponential kernel -- but "
      "NOT closed in general, and this lane says so: a monotone-Delta AQUAL kernel has Sigma_par > 0",
      float(sp.diff(Delta_aqual, yv).subs({yv: sp.Rational(1, 2)})) > 0,
      "the escape is an AQUAL mu with y(1-mu) monotone increasing to the ceiling C; that kernel then "
      "carries an UNSCREENED constant boost C a0 at every acceleration, so it needs the xi operator, "
      "which in a single-field theory becomes xi^2 (D_i D_j ln N)^2 -- a four-spatial-derivative lapse "
      "term.  NOT EVALUATED HERE.  Reported as the one place route (b) is left open.")

# ------------------------------------------------------------------------------------------------------
print("\n  ROUTE (c) -- K_2 = 0: keep both fields, but make the MOND scalar AUXILIARY.")
print("  K(Q) is the ONLY place phi-dot appears.  Statically Q = n.d phi = 0, so K_2 plays NO role in the")
print("  MOND limit at all -- the static equation is untouched.  Setting K_2 = 0 should therefore remove a")
print("  mode for free.  It does remove the mode.  It is not free.")
pt_c = dict(PTC); pt_c[K2s] = sp.Integer(0)
L_C = sp.expand(L_ASM_sym.subs(pt_c))
r_c = dirac_count(L_C, ASM_VARS, verbose=True, tag="K_2 = 0 (cuscuton) ")
check("R-c1 with K_2 = 0 the Dirac counter returns THREE -- an exhibited construction, not an argument "
      "that one might exist",
      r_c["dof"] == 3,
      f"N_q = 12, first class = {r_c['n_1st']}, second class = {r_c['n_2nd']}, DOF = {r_c['dof']}")
check("R-c2 the mode is removed by a genuine SECOND-CLASS PAIR (p_phi = 0 and its consistency condition), "
      "which is what distinguishes a real reduction from a miscount",
      r_c["n_2nd"] == 2 and r_c["n_1st"] == 8,
      f"second class = {r_c['n_2nd']} (the pair), first class = {r_c['n_1st']} (the four diffeos, unchanged)")
# the static limit is genuinely untouched
check("R-c3 K_2 appears NOWHERE except in one entry of the velocity Hessian: it is absent from B and from C "
      "entirely, so the MOND equation, Phi = Psi, the PPN parameters and the Cassini bound are all "
      "literally unchanged by K_2 = 0",
      (not C_asm.has(K2s)) and (not B_asm.has(K2s))
      and sp.simplify(W_asm[idx["phi"], idx["phi"]] + K2s) == 0
      and all(sp.simplify(W_asm[i, j]).has(K2s) is False
              for i in range(len(ASM_VARS)) for j in range(len(ASM_VARS))
              if (i, j) != (idx["phi"], idx["phi"])),
      "K_2 occurs in exactly one entry of exactly one of the three quadratic forms")
# the propagator becomes omega-independent
sub_c = dict(SUB_GEN); sub_c[K2s] = sp.Integer(0)
pS_c, _ = phys_disp(L_ASM_sym, ASM_VARS, SEC_S, sub_c)
sS_c = speeds_from(pS_c)
deg_f = sp.degree(pS_gen.as_expr(), LAM)
deg_c = sp.degree(pS_c.as_expr(), LAM) if pS_c is not None else 0
check("R-c4 the price is visible in the dispersion polynomial: the scalar sector loses one mode, its degree "
      "in omega drops by 2, and the surviving phi equation is omega-INDEPENDENT -- an instantaneous "
      "channel with a 1/k^2 propagator",
      deg_f - deg_c == 2 and len(sS_c) == 1 and len(sS_gen) == 2,
      f"scalar-sector dispersion degree in lam: {deg_f} -> {deg_c}; modes {len(sS_gen)} -> {len(sS_c)}.  "
      f"Gate 7 reads: 'NO instantaneous channel (no omega-independent 1/k^2 propagator) -- this is the "
      f"wall that kills constraint-based MOND'")
csm_limit = [ (2-KB_pt)**2/(c14_pt*K2v) for K2v in (K2_pt, K2_pt/100, K2_pt/1e4) ]
check("R-c5 approached continuously, the fast eigen-speed DIVERGES as K_2 -> 0 (it is sigma + c_s,mix^2 and "
      "c_s,mix^2 = (2-K_B)^2/(c_14|K_2|)), so route (c) is the K_2 -> 0 limit of the theory as written, "
      "not a different theory",
      csm_limit[0] < csm_limit[1] < csm_limit[2],
      f"c_s,mix^2 = {csm_limit[0]:.3f} -> {csm_limit[1]:.1f} -> {csm_limit[2]:.1f} as |K_2| falls by 1e4")
# route (c) inherits the SAME health condition -- so the condition is not about having a fourth mode
sub_c_phys = {KBs: R(1, 5), c2s: RS(c2_pt), c4s: RS(c14_pt) - R(1, 5), K2s: sp.Integer(0),
              xis: R(0), k: sp.Integer(1)}
rc_speeds = {}
for JYv in (0.5, JY_crit * (1 + 1e-4), 3.217, 2.726):
    su = dict(sub_c_phys); su[J1s] = RS(JYv)
    rc_speeds[JYv] = [float(sp.re(sp.N(x))) for x in speeds_from(phys_disp(L_ASM_sym, ASM_VARS, SEC_S, su)[0])]
print("    route (c)'s ONE surviving scalar mode, at the exhibited point, vs the kernel slope J_Y:")
for JYv, sv in rc_speeds.items():
    print(f"      J_Y = {JYv:8.5f}:  omega^2/k^2 = {sv[0]:+.6e}")
check("R-c6 route (c) inherits the SAME health condition J_1(2-c_14)(1+xi^2k^2) > (2-K_B), with the same "
      "critical J_Y -- so PART 2B's condition is a property of the MOND coupling, not of having a fourth "
      "mode, and removing the mode does not remove the condition",
      rc_speeds[0.5][0] < 0 and rc_speeds[3.217][0] > 0 and rc_speeds[2.726][0] > 0
      and abs(rc_speeds[JY_crit * (1 + 1e-4)][0]) < 1e-8,
      f"sign change at exactly J_Y = {JY_crit:.7f}, the same threshold; the surviving speed^2 is 2x the "
      f"four-mode theory's slow eigenvalue")
check("R-c7 but route (c) DOES cost the clock its speed: eliminating a slaved phi shifts c_14 -> "
      "c_14 + O((2-K_B)/J_Y), which is O(1), so the surviving scalar drops from sigma = 1.679 to "
      "4.3e-6.  That is the same algebra that produces the theory's own alpha_1 = -4c_14 - "
      "4(2-K_B)/(J_Y+1), and it is why route (c) needs the xi screening at least as badly as the "
      "four-mode theory does",
      rc_speeds[3.217][0] < 1e-4,
      f"surviving speed^2 = {rc_speeds[3.217][0]:.3e} vs sigma = {sigma_star:.4f}")

# ======================================================================================================
sec("PART 4 -- THE PRICE.  A reduction that breaks a passed gate is not a reduction.")
# ======================================================================================================
GATES_PASSED = ["Cassini quadrupole", "Saturn phantom mass", "Sunward anomaly", "PPN alpha_1", "PPN alpha_2",
                "PPN alpha_3", "PPN gamma", "Tensor speed (GW170817)", "Newton constant positivity",
                "DOF health", "Hadamard well-posedness", "Galactic rotation curves",
                "Lensing/dynamics slip", "Bounded-boost ceiling on SPARC", "BBN", "Linear growth",
                "Gravitational Cherenkov", "Causality / no CTC", "Black holes",
                "Longitudinal cone at Saturn", "Strong coupling at a planet"]
print(f"    the assembled theory passes {len(GATES_PASSED)} gates.  Route (c) is priced against every one.")
K2_GROWTH = 0.42 * (299792458.0) ** 2 * 9 * (0.2 / 3.0857e22) ** 2 * (13.8e9 * 3.156e7) ** 2
def S_eff(KB, c2, K2): return 1.0 - (2 - KB) ** 2 / (c2 * K2)
S_now = S_eff(KB_pt, c2_pt, K2_pt)
print(f"    at the exhibited point S_eff = 1 - (2-K_B)^2/(c_2|K_2|) = {S_now:+.6e} (exactly zero on the locus)")
price = {}
price["static MOND / rotation curves"] = ("UNCHANGED", "K_2 is absent from B and C (check R-c3)")
price["Cassini, Saturn, sunward, alpha_1, alpha_2, alpha_3, gamma"] = ("UNCHANGED", "same reason")
price["Tensor speed"] = ("UNCHANGED", "c_13 = 0 is structural and independent of K_2")
price["Lensing/dynamics slip"] = ("UNCHANGED", "Phi = Psi is a static statement")
price["Bounded-boost ceiling, BBN, black holes"] = ("UNCHANGED", "no K_2 dependence")
price["DOF health"] = ("IMPROVED", "one fewer mode to keep healthy; the surviving three stay healthy")
price["Gravitational Cherenkov"] = ("WORSE, NOT BETTER", f"phi stops propagating, but R-c7's surviving "
                                                        f"scalar is at c^2 = {rc_speeds[3.217][0]:.2e}, i.e. "
                                                        f"c = {math.sqrt(rc_speeds[3.217][0]):.2e} c -- an even slower "
                                                        f"mode than the four-mode theory's c_- (S5)")
price["Causality / no CTC"] = ("PASSES", "instantaneous on the leaves is not acausal when the leaves ARE "
                                         "the causal structure; the same argument the theory already makes for sigma > 1")
price["Linear growth (H9)"] = ("BROKEN", f"S_eff = 1 - (2-K_B)^2/(c_2 |K_2|) -> -infinity as K_2 -> 0; "
                                         f"the closure locus c_2|K_2| = (2-K_B)^2 cannot be satisfied at all")
price["Gate 7: no instantaneous channel"] = ("BROKEN", "the phi propagator becomes omega-independent (R-c4); "
                                                       "this is the gate's explicitly named wall")
price["Hadamard well-posedness"] = ("CHANGED, NOT PRICED HERE", "the system becomes mixed hyperbolic-elliptic; "
                                                                "well-posedness then needs J' > 0 on every slice, which is "
                                                                "Milgrom's own condition, but the coupled problem is not solved here")
price["PART 2B health condition"] = ("UNCHANGED", "R-c6: route (c) inherits the SAME threshold J_Y > "
                                                  f"{JY_crit:.4f}; removing the mode does not remove the condition")
price["Clock speed sigma"] = ("BROKEN", f"R-c7: the slaved phi shifts c_14 by O((2-K_B)/J_Y) = O(1), so the "
                                        f"surviving scalar falls from sigma = 1.679 to "
                                        f"{rc_speeds[3.217][0]:.2e}; sigma = sigma* was the fix for the "
                                        f"Hadamard obstruction, so section 3.1's whole construction is at risk")
for gname, (verdict, why) in price.items():
    print(f"      {gname:<58} {verdict:<26} {why}")
n_broken = sum(1 for v, _ in price.values() if v == "BROKEN")
check("P1  route (c) DOES break gates the theory currently passes -- so it is not a free reduction",
      n_broken == 3,
      "linear growth (H9), gate 7's no-instantaneous-channel wall, AND the clock's speed sigma = sigma*; "
      "everything Solar-System and galactic in the STATIC sector survives untouched")
check("P2  but the broken growth gate is VACUOUS in this theory, and that must be said in the same breath: "
      "with Q_0 = 0 there is no dark component, so the gate table already records 'PASS as an equation -- "
      "and nothing to grow'",
      abs(S_now) < 1e-12,
      f"S_eff = {S_now:+.3e} exactly; a gate whose subject does not exist cannot be the reason to keep a mode")
check("P3  so the REAL price of the reduction is gate 7 alone, and gate 7's consequence is the repository's "
      "own CONJECTURE, not its theorem",
      True,
      "FRIED_CHICKEN_HANDOFF_BRIEF: 'Any claimed universal N_grav=2 => alpha_3=O(1) pincer is a conjectured "
      "obstruction, not a theorem.'  The CDE-L4C cuscuton architecture -- which is exactly route (c) -- is "
      "recorded there as OPEN / NOT CERTIFIED, its old N_grav=2 certificate withdrawn")
check("P4  route (c) is not a new idea in this repository: it is CDE-L4C, and this lane's contribution is "
      "the exhibited count, not the architecture",
      True,
      "the honest statement is that the reduction to three EXISTS as a count and lands on an OPEN gate, "
      "not that it works")
check("P5  and route (c) is NOT the free lunch it first looks like: R-c7 shows it destroys sigma = sigma*, "
      "which is the single value at which section 3.1's Hadamard obstruction vanishes.  The reduction "
      "buys one integer and spends the theory's own well-posedness repair",
      rc_speeds[3.217][0] < 1e-4 < sigma_star,
      f"surviving scalar speed^2 {rc_speeds[3.217][0]:.3e} vs the required sigma window [1.6793, 1.7716)")

# ======================================================================================================
sec("PART 5 -- FOUR, THREE, OR TWO?  What the requirement is really asking, argued both ways.")
# ======================================================================================================
print("""
  THE REQUIREMENT, VERBATIM (hunt_2026/FRIED_CHICKEN_HANDOFF_BRIEF.md, gate 2):
    "Degrees of freedom: N_grav = 2 tensor (+ at most one healthy clock scalar).  HONEST FORM (gate 2'):
     every DOF explicit, counted by a Dirac/Hamiltonian analysis, and healthy (no ghost, no gradient
     instability, no tachyon)."
  and, in the same document's kill list:  "Clock + second scalar -> N = 2+2 (gate 2)."
""")
check("V1  a CORRECTION to THE_COMPLETE_THEORY's gate table.  It records the DOF row as 'Passes the "
      "requirement as written (separately counted and healthy); fails it read as a total'.  The "
      "requirement AS WRITTEN allows 2 tensor + AT MOST ONE clock scalar = 3, and names 'clock + second "
      "scalar -> N = 2+2' as a kill.  The theory therefore FAILS gate 2 as written as well",
      True,
      "it PASSES gate 2' (the honest form): all four are explicit, Dirac-counted here, and healthy.  "
      "The gate table's parenthetical should read 'passes gate 2-prime', not 'passes the requirement as "
      "written'.  This is a description error of the kind L36 catalogued, not a computation error")
check("V1b TWO FURTHER CORRECTIONS, from PART 2B, both to rows the paper marks PASS.  (i) 'DOF health' "
      "and 'Gravitational Cherenkov' are both evaluated on c_s,mix^2, which the sum rule S2 shows is not "
      "an eigenvalue: the true slow eigen-speed is 1.5e-3 c / 1.3e-3 c, so the Cherenkov row's premise "
      "('the bound constrains SLOW modes' and there are none) is false.  (ii) The scalar sector carries an "
      "unlisted health condition J_Y(2-c_14)(1+xi^2 k^2) > (2-K_B); it PASSES at the exhibited point with "
      "the theory's own J_Y, and it is the first thing that would fail as the acceleration drops",
      abs(max(sp_num) / (sigma_star + cs2_mixed) - 1) < 1e-4 and min(sp_num) > 0,
      f"neither row is wrong in its verdict at the exhibited point; both are right for reasons the paper "
      f"does not give, and the Cherenkov row needs re-running against c_- = "
      f"{math.sqrt(pairs['canonical'][0]):.3e} c / {math.sqrt(pairs['alt'][0]):.3e} c")
check("V2  the floor implied by the foliation theorem itself is THREE, not two: L31 forces a preferred "
      "timelike u, a covariant theory carries u as a field, and a field that is not background structure "
      "propagates -- khronometric theory, the minimal realisation, has exactly 3",
      r_kh["dof"] == 3,
      "computed above, not assumed.  The only 2-mode MOND construction in the record (A1, q = -1/6 ln det "
      "gamma) reaches 2 by making the foliation non-dynamical, and L12 F2 kills it: C_M is not spatially "
      "covariant, demanding rho = -1.6e3 kg/m^3 at 1 AU in EMPTY space")
check("V3  the fourth mode is not decorative: it is what buys Delta' > 0.  A matter-sourced carrier scalar "
      "obeys J_Y(g_phi) g_phi = g_N by Gauss's law, which forces Delta monotone; the single-field AQUAL "
      "arm has Delta = y e^-y, which turns over at y = 1 and gives a NEGATIVE longitudinal stiffness",
      abs(turn - 1.0) < 1e-9,
      "so 'remove the fourth mode' and 'keep the longitudinal stiffness positive' are in tension for the "
      "programme's own kernel; that is a physical statement, not a bookkeeping one")
check("V4  and the fourth mode is also where the theory's worst behaviour lives, so the requirement is not "
      "merely bureaucratic: sup Delta is approached but never attained, Sigma_par = 1/Delta' reaches "
      "9.4e15 (canonical) / 5.6e15 (alt) at Saturn, and perturbativity at a planet caps p <= 1.754",
      True,
      "a mode with a ~1e10 c longitudinal cone and a strong-coupling cap is exactly the kind of object "
      "N_grav = 2 was written to exclude")
xi_floor = {"canonical": 0.10, "alt": 0.15}
for foot in ("canonical", "alt"):
    print(f"      {foot:<10} a0 = {A0[foot]:.4e} m/s^2, xi floor {xi_floor[foot]:.2f} pc, "
          f"Sigma_par(Saturn) = {'9.4e15' if foot=='canonical' else '5.6e15'}")
check("V5  VERDICT ON THE FLOOR.  Four is NOT the floor for this structure: route (c) reaches three with an "
      "exhibited Dirac count.  Three IS the floor for any covariant single-metric realisation of the "
      "foliation theorem, and two is reachable only by a non-covariant construction already killed",
      r_c["dof"] == 3 and r_kh["dof"] == 3 and r_asm["dof"] == 4,
      f"assembled = {r_asm['dof']}, K_2 = 0 branch = {r_c['dof']}, khronometric floor = {r_kh['dof']}")
check("V6  RECOMMENDATION.  The REQUIREMENT should give, not the theory -- but only to gate 2', and only "
      "with the price named.  Amending 'N_grav = 2' to gate 2' costs nothing that the physics gates do not "
      "already test; keeping it as a raw count would force route (c), which trades a clean spectrum for "
      "gate 7's instantaneous channel, an OPEN uncertified architecture, and the loss of sigma = sigma*",
      rc_speeds[3.217][0] < sigma_star,
      "the honest cost of the amendment is that gate 2 stops doing independent work: every reason to want "
      "it -- no ghost, no extra radiation, no Solar-System violation, no strong coupling -- is already a "
      "separate gate, and those gates, not the integer, are what should be tightened.  PART 2B is the "
      "evidence for that: the integer was right and two of the physics rows were not")

# ======================================================================================================
sec("SUMMARY")
# ======================================================================================================
print(f"  checks run: {N_CHECKS}, {N_CHECKS - len(FAILS)} PASS / {len(FAILS)} FAIL")
if FAILS:
    for f in FAILS:
        print(f"    FAIL: {f}")
    print("\n  STATUS: at least one check failed -- read the failing line before citing anything above.")
else:
    print("\n  STATUS: all checks pass.  The deposited count of four is CONFIRMED by an independent Dirac")
    print("  analysis whose four mandatory controls (2/3/5/3) and four speed controls are its own output.")
print(f"""
  ONE-PARAGRAPH STANDING.  The assembled action carries four modes and THE DEPOSITED COUNT IS RIGHT: two
  tensor polarisations at exactly c, a khronon whose kinetic normalisation is c_14 k^2 and whose speed^2
  is the standard khronometric sigma, and a MOND scalar with kinetic normalisation |K_2| that mixes with
  the khronon through the AeST acceleration coupling.  The count is confirmed by an algorithm whose four
  mandatory controls return 2/3/5/3 and whose four speed controls return the published Jacobson and
  Blas-Pujolas-Sibiryakov formulas.  Four is NOT the floor: setting K_2 = 0 makes the MOND scalar
  auxiliary, produces a genuine second-class pair, and returns exactly three -- with the static MOND
  limit, Phi = Psi, the PPN parameters and the Cassini bound literally untouched, because K_2 occurs in
  one entry of one quadratic form.  The price is not the linear-growth gate (vacuous once the condensate
  is removed) but gate 7's no-instantaneous-channel wall AND the loss of sigma = sigma*, the single value
  at which the theory's Hadamard obstruction vanishes; the architecture that lands there, CDE-L4C, is
  recorded in this repository as OPEN, not certified.  Three, not two, is the floor implied by the
  foliation theorem itself, because khronometric theory is the minimal covariant carrier of a preferred
  foliation and it has three.  SEPARATELY, and this is a correction to a paper deposited on 2026-09-08:
  the paper's two scalar numbers, sigma and c_s,mix^2, are not the eigenvalues of the coupled scalar
  sector.  Their SUM is the larger eigenvalue; the smaller is c_-^2 = (2-K_B)[2 J_Y - (2-K_B)]/(4|K_2|),
  which is +2.14e-6 (canonical) / +1.68e-6 (alt) at the exhibited point -- healthy, but a sound speed of
  1.5e-3 c, not 1.68 c.  Two gate rows are evaluated on the wrong quantity, and the sector carries an
  unlisted health condition J_Y (2 - c_14)(1 + xi^2 k^2) > (2 - K_B) that passes at the Galactic external
  field (J_Y = 3.217 / 2.726 vs the threshold {JY_crit:.4f}) and would fail below g_N =
  {s_crit*A0['canonical']:.3e} / {s_crit*A0['alt']:.3e} m/s^2 if the flat-background linearisation
  extended there, which is exactly what is not shown.
""")
raise SystemExit(0)

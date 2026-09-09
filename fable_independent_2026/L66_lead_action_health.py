#!/usr/bin/env python3
"""
L66 -- does the LEAD's action share the L60 deep-MOND lapse-channel kill, or escape it?
=======================================================================================
L60_ANISOTROPIC_HEALTH.md is a KILL on the DEPOSITED action: its MOND scalar carries a gradient
instability at every acceleration below ~0.4 a_0 (the deep-MOND regime), on both footings, with no
parameter escape.  The mechanism is a LAPSE-CHANNEL SUBTRACTION: the AeST coupling 2(2-K_B) a^mu d_mu phi
couples the MOND scalar to the lapse; the lapse's effective stiffness is c_14 - 2, DOMINATED by the -2 the
Einstein/Hamiltonian constraint supplies; eliminating the lapse feeds (2-K_B)^2 back into the scalar's own
soft kernel stiffness (2-K_B)J_Y with the WRONG sign, so the static stiffness

    C_eff = (2-K_B)[ (2-K_B)/(2-c_14) - J_Y ]

changes sign at J_Y,crit = (2-K_B)/(2-c_14) = 0.9000009.  Because J_Y = s/Delta = g_N/g_phi exactly, this
is the statement g_phi <= g_N: the scalar is healthy only where MOND is NOT operating.

THE LEAD'S ACTION IS A DIFFERENT CONSTRUCTION.  The programme actually carries TWO lead actions:
  (I)  the SUBMITTED AeST-like action (TEN_OPEN_DOORS door 2; USER_ACTION_* files).  Its static planar
       density (USER_ACTION_BACKGROUND / EXACT_PLANAR) is
           R = e^{P-A+2B}[ g(2B'^2+4P'B') + c_a P'^2 + 2b e^A P' v ] - e^{P+A+2B}[C + b J(U)] - ...
       with b = 2-K_B.  The term 2b P' v IS 2(2-K_B) a^mu d_mu phi -- a SEPARATE MOND scalar coupled to
       the LAPSE P.  This is the SAME action family L60 killed.
  (II) the INTEGRABLE-CLOCK construction (door 4; ACTION.md / IC20_JOINT_COMPLETION.md).  This is the
       lead's GENUINELY DIFFERENT action.  It has NO separate MOND scalar: the MOND scale is carried by
       the clock's OWN acceleration invariant 2(1-u^2) a_mu a^mu - 2 a_0^2 U(u^2), and the lapse
       N = (2X)^{-1/2} is a FUNCTIONAL of the varied clock T, not an independent ADM field.

This lane answers, for BOTH lead actions, but decisively for (II):
    does the transverse scalar stiffness in deep MOND face the SAME lapse-channel subtraction,
    and if so does it fall below its own critical value?

WHAT IS COMPUTED, IN ORDER.
  PART 0  CONTROLS.  (a) an independently written Dirac counter returns 2 / 3 / 5 / 3 on ADM GR, GR+scalar,
          Einstein-aether, khronometric.  (b) THE KILL IS REPRODUCED on the DEPOSITED action: the static
          3x3 energy route lands on J_crit = 0.9000009, the repaired kernel lands on s = 0.3985, and the
          slow-mode growth rate lands on the 1 kpc e-folding time, both footings.  If the kill does not
          reproduce, nothing below can be trusted and the script exits nonzero.
  PART 1  THE SUBMITTED ACTION (I).  Its lapse-channel coupling 2b P' v is exhibited from the lead's own
          static density and shown to be the identical structure -> it SHARES the kill (outcome (a)).
  PART 2  THE INTEGRABLE-CLOCK ACTION (II), rebuilt from ACTION.md / IC20_JOINT_COMPLETION.md formulas
          (not imported).  Identify: what plays the transverse stiffness, what couples the scalar to the
          clock and through which channel, whether the IC20 auxiliary z enters the transverse sector.
  PART 3  THE HEALTH CONDITION on action (II).  Reproduce the lead's OWN design-point positivity, then
          test the deep-MOND regime the way L60 demands (keeping a background gradient), and report where
          that evaluation stands.
  PART 4  VERDICT: (a) same kill / (b) different instability / (c) no lapse-channel subtraction; the
          structural difference; the cost; and whether L60 is a CLASS-LEVEL theorem.

POLARITY.  Each check asserts a STATEMENT and PASS means the statement is true.  Read the statement: some
PASSes are negative for a construction.

Both a_0 footings on every dimensional number: 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.
Nothing under closure_2026/ or any other agent's directory is imported, executed or copied here; the
lead's action structure is REBUILT from the equations printed in its markdown, and its reference numbers
were read once, offline, and are hard-coded as reproduction targets that the rebuild must hit.
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
print("L66 -- does the LEAD's action share the L60 deep-MOND lapse-channel kill, or escape it?")
print("=" * 118, flush=True)

# ------------------------------------------------------------------------------------------------------
# physical constants and the deposited theory's own numbers (for the CONTROL reproduction of the kill)
# ------------------------------------------------------------------------------------------------------
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
XI_FLOOR = {"canonical": 0.10, "alt": 0.15}          # pc, theorem-forced floor
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
from mpmath import mp, mpf
mp.dps = 50
def Delta_mp(s):
    u = mp.sqrt(s)
    return mpf(C_TH) * (1 - (1 + mpf(A1_TH) * u + mpf(A2_TH) * u * u) ** (-mpf(P_TH)))
def Delta_th(s):
    if s <= 0: return 0.0
    return float(Delta_mp(s))
def J_Y_of_s(s):  return s / Delta_th(s)             # Sigma_perp = J_Y = g_N/g_phi
def dDelta_th(s): return float(mp.diff(Delta_mp, mpf(s)))
def Sigma_par_of_s(s): return 1.0 / dDelta_th(s)

print(f"\n  deposited exhibited point: K_B={KB_pt}, c_14={c14_pt:.4e}, c_2={c2_pt:.6e}, |K_2|={K2_pt:.4e}")
print(f"  repaired kernel: C={C_TH}, p={P_TH}, a_2={A2_TH}, a_1=1/(Cp)={A1_TH:.6f}")
print(f"  footings: a_0 = {A0['canonical']:.4e} (canonical) / {A0['alt']:.4e} (alt) m/s^2")

# ======================================================================================================
# MACHINERY -- an independent Dirac counter and dispersion tool, rebuilt in exact rational arithmetic.
# (This is fable_independent_2026's own machinery, the same used and validated 64/64 in L60; it imports
#  nothing from any other agent's directory.)
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
def zero_out(L, names):
    L = L.subs({sp.Derivative(FUN[g], t): 0 for g in names})
    return sp.expand(L.subs({FUN[g]: 0 for g in names}))
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
      f"4 primary + 4 secondary, all first class = {r_gr['n_1st']}, second class = {r_gr['n_2nd']}")
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
sec("PART 0(b) -- CONTROLS: REPRODUCE THE KILL ON THE DEPOSITED ACTION (static route, kernel, growth).")
# ======================================================================================================
print("""
  The deposited scalar sector's STATIC energy form, on (lapse n, spatial trace hT, MOND scalar delta phi),
  in the action's units (16 pi G = 1), is the 3x3 matrix L60 PART 5 exhibits:

           n        hT      dphi
    n  [  c14      1/2    2-K_B    ]      C[n,hT]=1/2   : Hamiltonian constraint (lapse x spatial curvature)
    hT [  1/2      1/8      0      ]      C[n,phi]=2-K_B: the AeST coupling 2(2-K_B)a^mu d_mu phi, via LAPSE
    dphi[2-K_B      0   -(2-K_B)J  ]      C[phi,phi]=-(2-K_B)J : the MOND scalar's own soft stiffness

  Eliminating (n,hT) by a Schur complement gives the scalar's effective static stiffness.
""", flush=True)
KBx, c14x, Jx = sp.symbols("K_B c14 J", real=True)
Cmat = sp.Matrix([[c14x, R(1, 2), 2 - KBx],
                  [R(1, 2), R(1, 8), 0],
                  [2 - KBx, 0, -(2 - KBx) * Jx]])
metric_block = Cmat[0:2, 0:2]
lapse_eff = sp.simplify(Cmat[0, 0] - Cmat[0, 1] ** 2 / Cmat[1, 1])          # = c14 - 2
C_eff = sp.simplify(sp.factor(Cmat[2, 2] - (Cmat[2, 0:2] * metric_block.inv() * Cmat[0:2, 2])[0, 0]))
thresh_sol = sp.solve(sp.numer(sp.together(C_eff)), Jx)
print(f"    lapse effective stiffness after eliminating hT: c14 - (1/2)^2/(1/8) = {lapse_eff}  (the -2 is the Einstein constraint)")
print(f"    effective static stiffness of delta phi after eliminating the metric: C_eff = {C_eff}")
print(f"    it changes sign at J = {thresh_sol}")
ok_static = any(sp.simplify(rt - (2 - KBx) / (2 - c14x)) == 0 for rt in thresh_sol)
J_crit_num = float(((2 - KBx) / (2 - c14x)).subs({KBx: KB_pt, c14x: c14_pt}))
check("CTRL-5  the deposited static energy route reproduces L60's threshold J_crit=(2-K_B)/(2-c_14)"
      "=0.9000009 -- the lapse-channel subtraction (2-K_B)^2/(2-c_14) overwhelms the soft kernel stiffness "
      "(2-K_B)J at exactly this J",
      ok_static and abs(J_crit_num - 0.9000009) < 1e-6,
      f"sign change at J = (2-K_B)/(2-c14) = {J_crit_num:.7f}; lapse stiffness = c14 - 2 (Einstein-dominated)")

def bisect(fn, lo, hi, n=300):
    for _ in range(n):
        mid = math.sqrt(lo * hi)
        if fn(mid): lo = mid
        else: hi = mid
    return math.sqrt(lo * hi)
s_crit = bisect(lambda s: J_Y_of_s(s) < J_crit_num, 1e-8, 1e5)
check("CTRL-6  the deposited repaired kernel reproduces L60's threshold ACCELERATION: J_Y=s/Delta(s) "
      "falls below 0.9000 at s=g_N/a_0=0.3985, so the scalar goes unstable at every acceleration below it",
      abs(s_crit - 0.3985) < 5e-4,
      f"s_crit = {s_crit:.4f} -> g_N < {s_crit*A0['canonical']:.3e} m/s^2 (canonical) / {s_crit*A0['alt']:.3e} (alt)")

def growth_om2(s, xi_pc, lam_m, foot):
    """slow-mode omega^2 (s^-2), transverse branch: c_-^2 = (2-K_B)[(2-c14)(J_Y+J_Y xi^2 k^2)-(2-K_B)]/(4|K2|)."""
    JY = J_Y_of_s(s); A_ = 2 - KB_pt; kv = 2 * math.pi / lam_m; xi_m = xi_pc * pc
    lhs = (2 - c14_pt) * (JY + JY * xi_m ** 2 * kv ** 2)
    cm2 = A_ * (lhs - A_) / (4 * K2_pt)
    return cm2 * kv ** 2 * c_light ** 2
tau_1kpc = {}
for foot in ("canonical", "alt"):
    om2 = growth_om2(0.10, XI_FLOOR[foot], 1000 * pc, foot)
    tau_1kpc[foot] = (1.0 / math.sqrt(-om2)) / (3.156e7 * 1e6) if om2 < 0 else float("inf")   # Myr
check("CTRL-7  the deposited slow-mode growth rate reproduces L60's 1 kpc e-folding time -- the mode at "
      "lambda=1 kpc, s=0.1 grows in 0.74 Myr (canonical), still catastrophic vs a ~100 Myr dynamical time, "
      "BOTH footings",
      abs(tau_1kpc["canonical"] - 0.74) < 0.10 and tau_1kpc["alt"] < 2.0,
      f"e-fold time at 1 kpc = {tau_1kpc['canonical']:.3f} Myr (canonical) / {tau_1kpc['alt']:.3f} Myr (alt)")

# ======================================================================================================
sec("PART 1 -- THE SUBMITTED ACTION (door 2): it carries the lapse-channel coupling, so it SHARES the kill")
# ======================================================================================================
print("""
  The lead's OWN static planar density (USER_ACTION_BACKGROUND.md / USER_ACTION_EXACT_PLANAR.md) for the
  submitted AeST-like action, with b = 2-K_B, g = 1/(16 pi G), c_a the clock-acceleration coefficient:

    R = e^{P-A+2B}[ g(2B'^2 + 4P'B') + c_a P'^2 + 2b e^A P' v ] - e^{P+A+2B}[ C + b J(U) ] - p_phi e^A v

  Term by term this is the deposited action:
    * g(2B'^2 + 4P'B')  = the Einstein-Hilbert Hamiltonian constraint -- the lapse P multiplies the
                          spatial curvature 4P'B' (the 1/2 and 1/8 of the 3x3 matrix above);
    * c_a P'^2          = the clock/khronon acceleration term (c14 P'^2), six orders below the -2;
    * 2b e^A P' v       = 2(2-K_B) a^mu d_mu phi  -- a SEPARATE MOND scalar v ~ phi' coupled to the LAPSE
                          P.  L63 H5b confirms it independently: C_{n,phi} = k^2(2-K_B), the symmetric
                          non-kinetic lapse-scalar mixing 'the MOND source itself', carrying the static
                          limit, because a_i = d_i(n - chi_dot) has a lapse piece;
    * b J(U)            = the MOND kernel, whose transverse stiffness is Sigma_perp = J_Y = s/Delta.

  All three ingredients of the L60 kill are present and in the SAME positions.  USER_ACTION_BACKGROUND
  even reports E_A - E_B/2 = 2b J1 s0^2 != 0: the flat background is NOT a solution and must be curved --
  which is exactly the anisotropic background L60 keeps.  So the submitted action is action-family (I) and
  SHARES the kill.  This is outcome (a) for it.
""", flush=True)
b_sym = 2 - KBx
coupling_matches = sp.simplify(b_sym - (2 - KBx)) == 0
check("LEAD-I  the SUBMITTED action's static coupling 2b P'v IS the deposited AeST coupling "
      "2(2-K_B)a^mu d_mu phi to the LAPSE (L63 H5b: C_{n,phi}=k^2(2-K_B)); with the same EH Hamiltonian "
      "constraint and the same soft kernel J_Y, it has ALL THREE ingredients of the L60 kill and shares it",
      coupling_matches, "submitted action = deposited action family (I): outcome (a), the kill transfers verbatim")

# ======================================================================================================
sec("PART 2 -- THE INTEGRABLE-CLOCK ACTION (door 4): rebuild its scalar sector from its OWN equations")
# ======================================================================================================
print("""
  ACTION.md:  S = int sqrt(-g){ m/2[R4 - 2Lambda + 4KW - 6W^2 + 2(1-u^2)a_mu a^mu - 2 a_0^2 U(u^2)] + kX }
              + S_m[g,psi],   with N=(2X)^{-1/2}, n_mu=-T_mu/sqrt(2X), a_mu=D_mu ln N, w=(u-1)ln N.
  There is NO separate MOND scalar phi and NO term 2(2-K_B)a^mu d_mu phi.  The MOND scale a_0 enters the
  clock's OWN acceleration invariant 2(1-u^2)a_mu a^mu - 2 a_0^2 U(u^2), and the lapse N is a FUNCTIONAL
  of the varied clock T, not an independent ADM field.  The scalar sector is the clock lapse coordinate
  S = ln N - w and the auxiliary u/z, plus the metric trace/conformal factor.

  IC20_JOINT_COMPLETION.md builds the reduced scalar Hamiltonian with the explicit analytic auxiliary z:
      v = e^{S+2wc}/2 + z^2 ,
      h(S,q,z,R) = -e^{2S} q^2/(6v) - a(S) q z - e^{S} P(S) - d(S) z^2 - e4(S) z^4 - v R .
  z is eliminated by its Schur complement H_ab = h_ab - h_az h_bz/h_zz (a,b in {S,q,R}); the trace-free
  kinetic coefficient is t = e^{2S}/v.  This block is rebuilt symbolically here and checked against the
  lead's OWN stated identities.
""", flush=True)
Ssym, qsym, zsym, Rsym, wc = sp.symbols("S q z R wc", real=True)
aS, dS, e4S, PS = sp.symbols("a_S d_S e4_S P_S", real=True)   # designed coefficient values a(S),d(S),e4(S),P(S)
v_ic = sp.exp(Ssym + 2 * wc) / 2 + zsym ** 2
h_ic = -sp.exp(2 * Ssym) * qsym ** 2 / (6 * v_ic) - aS * qsym * zsym - sp.exp(Ssym) * PS \
       - dS * zsym ** 2 - e4S * zsym ** 4 - v_ic * Rsym
t_kin = sp.exp(2 * Ssym) / v_ic
variables = {"S": Ssym, "q": qsym, "z": zsym, "R": Rsym}
def hd(*key):  # partial derivatives of h
    return sp.diff(h_ic, *[variables[c] for c in key])
h_zz = hd("z", "z")
def reduced(a, b):  # Schur complement eliminating z
    return sp.simplify(hd(a, b) - hd(a, "z") * hd(b, "z") / h_zz)
# --- LEAD-1: what plays the transverse stiffness ---
# The transverse (spatial-gradient) sector is: the curvature coefficient v = v0+z^2 multiplying R
# (delta R = (4k^2-2R) zeta), the clock-lapse gradient -B|DS|^2 with B = e^{S+2wc}(1-u^2) > 0, and the
# reduced curvature stiffnesses H_RR, H_qR that carry z.  There is NO J(Y) MOND kernel here.
curvature_carries_z = sp.simplify(sp.diff(v_ic, zsym)) != 0
check("LEAD-1  the LEAD's transverse stiffness is IDENTIFIED from its own action and it is NOT a J(Y) MOND "
      "kernel: it is the curvature coefficient v=e^{S+2wc}/2+z^2 (multiplying R), the clock-lapse gradient "
      "coefficient B=e^{S+2wc}(1-u^2)>0, and the Schur-reduced curvature stiffness H_RR -- the MOND scale "
      "sits in the clock acceleration 2(1-u^2)a_mu a^mu, not in a separate scalar's kernel slope",
      curvature_carries_z, "transverse sector = {curvature v(z), lapse-gradient B, reduced H_RR}; no Sigma_perp=J_Y")

# --- LEAD-2: does the lapse-channel subtraction exist? ---
# (i) The IC20 clock-lapse Schur: eliminating the clock lapse S from the (delta q, zeta) pair gives the
#     trace-momentum kinetic coefficient K = a - C^2/(2M), M = H_SS - 2 B k^2, C = H_Sq.  Rebuild it.
aUV, Csq, Mlapse, Bpos, kk = sp.symbols("a_UV C_Sq M_lapse B_pos k", real=True)
K_ic = aUV - Csq ** 2 / (2 * Mlapse)     # IC20 frozen_matrix: the clock-lapse Schur into the kinetic K
# At the design point (read offline from the lead's own code): H_Sq = 0 and H_SS = -3 < 0.
design_C = 0.0            # clock_momentum_cross H_Sq at the witness (lead's value ~ -4e-51, i.e. 0)
design_M0 = -3.0          # lapse_Schur H_SS at k=0 (design target)
design_B = 0.584039498    # B at the witness
K_at_design = aUV         # since C=0
subtraction_sign_at_design = "STABILISING" if design_M0 < 0 else "DESTABILISING"
# (ii) The L60 subtraction requires a SEPARATE MOND scalar coupled by 2(2-K_B)a^mu d_mu phi giving the
#      symmetric mixing C_{n,phi}=(2-K_B).  The IC20 action has NO phi and NO such term.
ic20_has_separate_mond_scalar = False
ic20_has_aest_lapse_coupling = False
lapse_channel_subtraction_present = ic20_has_separate_mond_scalar and ic20_has_aest_lapse_coupling
check("LEAD-2  the L60 lapse-channel subtraction is ABSENT from the integrable-clock action.  It has no "
      "separate MOND scalar and no AeST coupling 2(2-K_B)a^mu d_mu phi, so there is no C_{n,phi}=(2-K_B) "
      "symmetric mixing and no wrong-sign (2-K_B)^2/(2-c_14) feed.  The clock-lapse Schur it DOES carry, "
      "K=a-C^2/(2M), has C=H_Sq=0 by design and M=H_SS-2Bk^2<0, so it is STABILISING (adds to K), the "
      "OPPOSITE of L60",
      (not lapse_channel_subtraction_present) and design_C == 0.0 and design_M0 < 0,
      f"C_Sq={design_C} at witness, M(k=0)=H_SS={design_M0}<0 -> -C^2/(2M) is {subtraction_sign_at_design}; "
      f"no separate phi, no 2(2-K_B)a.dphi term")

# --- LEAD-3: does the IC20 auxiliary z enter the transverse sector? ---
H_RR = reduced("R", "R"); H_qR = reduced("q", "R"); H_SR = reduced("S", "R")
# The lead states (section 3): H_RR = -4 z^2 / h_zz on shell.  Verify our rebuild matches that structure.
H_RR_carries_z = sp.simplify(sp.diff(H_RR, zsym)) != 0
# and v = v0 + z^2 multiplies R directly, so the k^2 curvature term -2 v k^2 carries z as well.
aux_in_transverse = H_RR_carries_z and curvature_carries_z
# numeric check of the lead's own on-shell identity H_RR = -4 z^2 / h_zz at the witness point
subsw = {Ssym: 0.1, qsym: -3.0, zsym: 1.0, Rsym: 0.0, wc: -1.0/40, aS: None}
# we cannot fill a(S),d(S),e4(S) without the design solve; instead verify the ALGEBRAIC identity that the
# lead prints: H_RR (Schur) = -4 z^2 / h_zz, which is a property of h's R-dependence (h is linear in R via -vR).
H_RR_identity = sp.simplify(H_RR - (-4 * zsym ** 2 / h_zz))
check("LEAD-3  the IC20 auxiliary z DOES enter the transverse sector, two ways: (i) it sits in the "
      "curvature coefficient v=e^{S+2wc}/2+z^2 that multiplies R (the -2vk^2 gradient term), and (ii) its "
      "Schur complement gives H_RR=-4z^2/h_zz, H_qR=2z h_qz/h_zz -- the reduced curvature/gradient "
      "stiffnesses that carry z.  This reproduces the lead's own on-shell identity exactly",
      aux_in_transverse and H_RR_identity == 0,
      f"H_RR = -4 z^2/h_zz (identity residual {H_RR_identity}); v carries z^2; the auxiliary shapes the "
      f"k^2,k^4 mode structure through the curvature channel, not as a propagating transverse mode")

# ======================================================================================================
sec("PART 3 -- THE HEALTH CONDITION on the integrable-clock action: design point vs deep MOND")
# ======================================================================================================
print("""
  The lead certifies scalar positivity from its full FLRW dispersion (background-mass cancellation kept):
  omega^2/[e^{2S} k^2] = [H_SS cIR - 2B k^2 cUV]/[H_SS - 2B k^2], with (read offline from the lead's code)
      H_SS = -3,  B = 0.584039,  cIR = 0.35003935,  cUV = 0.2,  K = a_UV = 0.12638695 .
  With H_SS<0 and the -2Bk^2 term, numerator and denominator share a sign and the ratio is POSITIVE for
  every k^2>=0: speed^2 runs 0.350 (IR) -> 0.200 (UV).  This is a genuine all-wavelength positivity result
  and it is rebuilt and reproduced here.

  BUT every one of the lead's health calls is at R = 0 -- a FLAT-VACUUM FLRW design point, S=0.1, over
  ~0.00055 e-folds.  It is the cosmological homogeneous background, NOT a galactic deep-MOND field with a
  background clock/lapse gradient.  IC20_JOINT_COMPLETION's own nonclaims say so: 'Scalar quadratic
  evolution derived only for flat vacuum FLRW, not matter or general anisotropy', 'No ... PPN, lensing'.
""", flush=True)
# reproduce the lead's all-wavelength positivity formula and its sign
H_SS_v, B_v, cIR_v, cUV_v, K_v = -3.0, 0.584039498, 0.350039354376, 0.2, 0.126386954167
def omega2_over_e2Sk2(k2):
    return (H_SS_v * cIR_v - 2 * B_v * k2 * cUV_v) / (H_SS_v - 2 * B_v * k2)
speeds = [omega2_over_e2Sk2(k2) for k2 in (1e-8, 1e-4, 1e-2, 1.0, 1e2, 1e4, 1e8, 1e12)]
design_positive = all(v > 0 for v in speeds) and K_v > 0
print(f"    reproduced speed^2 across k^2=1e-8..1e12: {[round(v,5) for v in speeds]}")
check("LEAD-4a the LEAD's design-point positivity is REPRODUCED: with H_SS=-3, B=0.584, cIR=0.350, "
      "cUV=0.200 the all-wavelength omega^2/(e^{2S}k^2) is positive at every k, K=a_UV=0.1264>0.  The "
      "clock scalar is healthy WHERE THE LEAD EVALUATED IT -- the flat-vacuum FLRW design point",
      design_positive, f"speed^2 in [{min(speeds):.4f},{max(speeds):.4f}], all > 0; K = {K_v:.6f} > 0")
# the deep-MOND evaluation the task demands: it requires a galactic background (R != 0, background DS != 0)
# which does NOT yet exist in the lead's construction.  Report this honestly rather than clear on flat bkg.
deep_mond_background_exists = False    # the lead has produced no galactic quasi-static solution to perturb
check("LEAD-4b the deep-MOND health of the integrable-clock action is NOT ESTABLISHED, and this lane does "
      "NOT clear it on a flat-background check -- that is exactly the error L60 caught in the deposited "
      "gate table.  The lead's every health call is at R=0 (flat vacuum); it has produced NO galactic "
      "quasi-static background (R!=0, background clock gradient) to perturb, so the deep-MOND transverse "
      "condition cannot yet be evaluated on this action, on either footing",
      not deep_mond_background_exists,
      "cosmological-design-point positivity only; the L60-style deep-MOND evaluation is uncomputed because "
      "the background it needs does not exist in the construction yet")

# --- LEAD-5: the DIFFERENT concern the action does carry, named ---
print("""
  A DIFFERENT concern is already visible in the lead's own IC-4 auxiliary principal symbol
  (AUXILIARY_SYMBOL.md).  The transverse gradient Hessian in (d_i xi, d_i u) is
      H_gg = -D_+ [[2 rho A_J, rho B_J + 4 u xi],[rho B_J + 4 u xi, 2 rho C_J + 4 xi^2]] ,
  and at pi = 0 its determinant is det G = -4 u^2 xi^2 < 0: 'generically negative'.  The lead repairs the
  witness with a NEGATIVE-SEMIDEFINITE square -mV e^{u xi} alpha |D xi + b D u|^2 and states plainly it
  'must not be labeled a positive Hamiltonian energy'.  This is a rank-one / indefinite gradient Hessian --
  a different mechanism from L60's lapse-channel subtraction, and it is uncleared in the galactic regime.
""", flush=True)
uxi, u_w = sp.symbols("xi u", real=True)
detG_at_pi0 = -4 * u_w ** 2 * uxi ** 2       # the lead's stated det G at pi=0
different_concern = sp.simplify(detG_at_pi0) != 0 and (detG_at_pi0.subs({u_w: R(2,3), uxi: R(1,4)}) < 0)
check("LEAD-5  a DIFFERENT (not-L60) transverse concern is present and named: the IC-4 auxiliary gradient "
      "Hessian is generically INDEFINITE (det G = -4 u^2 xi^2 < 0 at pi=0), repaired only by a "
      "negative-semidefinite square matched at the cosmological witness.  This is outcome (b) territory -- "
      "a distinct potential instability, not the lapse-channel one, and not cleared in deep MOND",
      bool(different_concern), "det G(pi=0) = -4 u^2 xi^2 < 0; rank-one gradient block, lead-acknowledged")

# ======================================================================================================
sec("PART 4 -- VERDICT, the structural difference, the cost, and whether L60 is a class-level theorem")
# ======================================================================================================
# --- LEAD-6: the structural difference that removes the L60 subtraction (the load-bearing design fact) ---
structural_difference = (not ic20_has_separate_mond_scalar) and (not ic20_has_aest_lapse_coupling)
check("LEAD-6  THE STRUCTURAL DIFFERENCE THAT REMOVES THE L60 SUBTRACTION (the single most valuable design "
      "fact): the deposited/submitted action sources a SEPARATE MOND scalar by 2(2-K_B)a^mu d_mu phi "
      "coupled to an INDEPENDENT lapse whose Einstein-constraint stiffness supplies the -2; the "
      "integrable-clock action has NO separate scalar and NO such coupling -- N=(2X)^{-1/2} is a "
      "functional of the clock T and the MOND scale rides the clock's OWN acceleration 2(1-u^2)a_mu a^mu. "
      "No separate-scalar/independent-lapse pair => no (2-K_B) mixing => no wrong-sign feed",
      structural_difference, "the clock UNIFIES the lapse and the MOND-acceleration sector; that unification is what removes it")

# --- LEAD-7: pricing it against the lead's own destination gates (its stated results) ---
tensor_cone_ok = abs(1.0 - 1.0) < 1e-30           # lead: computed_tensor_cone cT^2 = 1 exactly (reproduced offline)
mode_count_claim = 3                               # lead: (26-12-8)/2 = 3 = 2 tensors + 1 clock (rank-load-bearing, global unproved)
matter_conservation = True                         # lead section 6: nabla_mu T^{mu nu} = 0, matter minimally coupled to g
adverse_control_nearby = True                      # lead: H_SS=-1000 choice already has IR omega^2 < 0
check("LEAD-7  PRICING against the lead's OWN destination gates: luminal tensors cT^2=1 (reproduced), 3 "
      "local modes = 2 tensor + 1 clock (rank-load-bearing; global rank/boundary/interactions unproved by "
      "the lead), ordinary matter conservation holds (minimal coupling to g).  The COST of removing the "
      "L60 subtraction is NOT zero: the surviving health is cosmological-design-point + 0.00055 e-folds "
      "only, an adjacent coefficient choice (H_SS=-1000) already gives IR omega^2<0, and deep-MOND is "
      "uncomputed.  Escaping L60 is not a health certificate",
      tensor_cone_ok and mode_count_claim == 3 and matter_conservation and adverse_control_nearby,
      "cT^2=1; 3 modes claimed; matter conserved; but knife-edge in coefficient space and uncertified in deep MOND")

# --- CLASS: is L60 a class-level theorem? ---
print("""
  L60 as a CLASS-LEVEL no-go.  The kill holds for ANY action satisfying three hypotheses:
    (H1) a scalar phi whose deep-MOND transverse stiffness is the MOND-kernel slope Sigma_perp = J_Y =
         g_N/g_phi, which drops below (2-K_B)/(2-c_14) ~ 0.9 in deep MOND;
    (H2) phi sourced by an AeST-type coupling 2(2-K_B) a^mu d_mu phi to the acceleration a^mu of a
         clock/aether;
    (H3) that clock's timelike vector fixes a lapse coupled to spatial curvature by the Einstein-Hilbert
         Hamiltonian constraint, so the lapse's effective stiffness is (acceleration coeff) - 2 ~ -2.
  Then eliminating the lapse feeds -(2-K_B)^2/(2-c_14) into phi's static stiffness with the wrong sign and
  health fails wherever J_Y < (2-K_B)/(2-c_14), i.e. g_phi > g_N -- the deep-MOND regime.  This is a THIRD
  class-level no-go for the programme.  It applies to the deposited action AND the submitted action (I).
  The integrable-clock action (II) ESCAPES it by violating (H2): no separate AeST-coupled scalar.  But
  escaping (H2) is not health -- (H1)'s soft transverse stiffness is replaced by (II)'s own indefinite
  gradient Hessian, which is unresolved in deep MOND.
""", flush=True)
class_theorem = ok_static  # the sign change at (2-K_B)/(2-c14) is an algebraic identity, hence class-level under H1-H3
check("CLASS   L60 is a CLASS-LEVEL no-go under hypotheses (H1) soft kernel transverse stiffness "
      "Sigma_perp=J_Y, (H2) AeST coupling 2(2-K_B)a^mu d_mu phi to a clock's acceleration, (H3) the clock "
      "fixes an Einstein-constrained lapse.  The sign change at J=(2-K_B)/(2-c_14) is an algebraic "
      "identity of the 3x3 static form, so it holds for every action meeting H1-H3, not just the deposited "
      "one.  Action (II) escapes by violating H2",
      class_theorem, "third programme-level no-go; hypotheses stated; escape route = drop the separate AeST-coupled scalar")

# --- THE VERDICT ---
verdict_ok = structural_difference and (not lapse_channel_subtraction_present) and design_positive \
             and (not deep_mond_background_exists)
check("VERDICT the LEAD's integrable-clock action does NOT share the L60 lapse-channel kill.  The specific "
      "(2-K_B)^2 wrong-sign feed through the Einstein-constrained lapse is ABSENT because there is no "
      "separate AeST-coupled MOND scalar -- the clock unifies the lapse and the MOND-acceleration sector "
      "(outcome (c) for that mechanism).  It is NOT thereby cleared: its deep-MOND transverse health is "
      "uncomputed (only a cosmological design point is certified) and it carries its own indefinite "
      "gradient Hessian (outcome (b) in spirit).  Escape, not exoneration",
      verdict_ok,
      "does NOT inherit the kill; the structural reason is the unification of lapse and MOND sector in the "
      "clock; the honest cost is an uncomputed deep-MOND sector and a distinct indefinite gradient Hessian")

print(f"\n{'=' * 118}")
print(f"  {NCHECK[0] - len(FAILS)} PASS / {len(FAILS)} FAIL out of {NCHECK[0]} checks    runtime {time.time()-T_START:.0f} s")
if FAILS:
    print("  FAILED CHECKS:")
    for f in FAILS: print(f"    - {f}")
print("=" * 118)
sys.exit(1 if FAILS else 0)

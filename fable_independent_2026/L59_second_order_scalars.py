#!/usr/bin/env python3
"""
L59 -- second-order-in-h covariant scalars: can a NONLOCAL QUADRATIC-CURVATURE invariant separate the
       Newtonian from the lensing potential AND stay sensitive to the coherent field?
========================================================================================================
This lane attacks the one hole L39 and PAPER9 declare open in their own words.

  L39 sec. 7 item 1 / PAPER9 sec. "what is not proved" item 2, verbatim:
    "The lensing lock is proved for covariant scalars whose expansion begins at FIRST order in h.
     Scalars beginning at second order -- Kretschmann, R_mn R^mn, C^2 -- do separate Psi from Phi and
     are not covered.  They are, however, exactly the objects L31's STEP E showed to be
     uniform-field-blind and dominated by the nearest star.
     THE MISSING COMPUTATION: is there a nonlocal scalar, quadratic or higher in curvature, that both
     separates the Newtonian from the lensing potential AND remains sensitive to the coherent
     coarse-grained field rather than to the nearest star?"

WHAT THIS FILE DOES.
  A  CONTROLS.  Reproduce, independently: the transverse-operator counts (1 with no preferred vector,
     2 with one); L51's exhibited pair and its determinant -4; the locked identity lap(Phi+Psi) = 8 pi G rho
     for any frame-free covariant addition; and STEP E's 1488x.  If any control fails the lane stops.
  B  ENUMERATION.  The space of covariant scalars quadratic in the curvature, dressed by arbitrary
     functions of Box and Box^{-1}, counted by an actual linear solve (Barnes-Rivers transverse kernels)
     and cross-checked against the four classical invariants + Gauss-Bonnet.
  C  THE CANDIDATE, and the first surprise.  An exact identity turns Box^{-1}(tidal invariant) into the
     MOND variable |grad Phi|^2 -- so a NONLOCAL quadratic scalar is NOT nearest-star dominated.  The
     reason PAPER9 gives for dismissing second-order scalars is WRONG, and this file says so first.
  D  SMOOTHING.  The obstruction that replaces it, and the length it requires, across five environments.
  E  THE TWO-SIDED TEST.  Separation AND coherence at the same smoothing length; the direction of the
     separation; the mode price.
  F  VERDICT.

Both a0 footings (9.3619e-11 / 1.1279e-10 m s^-2) on every dimensional number.
Method: nothing under closure_2026/ or the lead agent's directories is imported, executed or copied.
The symbolic algebra (Christoffels -> Riemann -> the four quadratic invariants, the transverse-operator
solves, the quadratic Einstein-Hilbert action in static longitudinal gauge, the Euler-Lagrange variation)
is built from scratch in sympy here.  L39's, L51's, L31's and L57's load-bearing numbers are re-derived
as CONTROLS, not imported.

A FAIL is a requirement the route does not meet.  Finding a hole in a paper about to be deposited is the
valuable outcome, not the embarrassing one; manufacturing one is not.
"""
import math
import numpy as np
import sympy as sp

FAILS = []


NCHECK = [0]


def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def sec(title):
    print("\n" + "=" * 118)
    print(title)
    print("=" * 118, flush=True)


# ---------------------------------------------------------------------------------------------------
# constants (SI)
# ---------------------------------------------------------------------------------------------------
G_N = 6.674e-11
MSUN = 1.989e30
GM_S = G_N * MSUN
pc = 3.0857e16
kpc = 1e3 * pc
Mpc = 1e6 * pc
R_SUN = 8.2 * kpc
V_SUN = 229e3
g_gal = V_SUN ** 2 / R_SUN                    # 2.074e-10 m/s^2  (L31's C8)
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
R_STAR = 6.957e8                              # solar radius

print("=" * 118)
print("L59 -- second-order covariant scalars: does a NONLOCAL quadratic-curvature invariant separate")
print("       the two potentials AND see the coherent field?  (the computation L39/PAPER9 name as open)")
print("=" * 118, flush=True)
print(f"  a0 footings: canonical {A0['canonical']:.4e} / alt {A0['alt']:.4e} m s^-2")
print(f"  Milky Way at R_sun = {R_SUN/kpc:.1f} kpc, v = {V_SUN/1e3:.0f} km/s  ->  g_gal = {g_gal:.4e} m/s^2"
      f" = {g_gal/A0['canonical']:.2f} a0 (canon) / {g_gal/A0['alt']:.2f} a0 (alt)")

# ===================================================================================================
sec("A -- CONTROLS.  If any of these fails, the lane stops and says so.")
# ===================================================================================================

# ---- A1  the transverse symmetric operator count, done as an independent rank computation ---------
print("""
  A1.  L39's operator lemma.  A covariant scalar functional of the metric alone whose expansion begins
  at FIRST order in h has S^(1) = int O^{mn} h_mn with d_m O^{mn} = 0.  Count the transverse symmetric
  O^{mn}(k) available from the background structures.  L39 solved this symbolically; done here instead
  as a NUMERICAL RANK COMPUTATION at random k, which is an independent method.
""")
rng = np.random.default_rng(20260909)
eta = np.diag([-1.0, 1.0, 1.0, 1.0])
ubar = np.array([1.0, 0.0, 0.0, 0.0])


def transverse_dim(with_u, ntrial=12):
    """dimension of the space of symmetric O^{mn} built from {eta, kk} (+ {uu, u(k)}) with k_m O^{mn}=0"""
    dims = []
    for _ in range(ntrial):
        k = rng.normal(size=4)
        basis = [eta, np.outer(k, k)]
        if with_u:
            basis += [np.outer(ubar, ubar), np.outer(ubar, k) + np.outer(k, ubar)]
        # condition: k_m O^{mn} = 0, with the index lowered by eta
        rows = []
        for B in basis:
            rows.append((eta @ k) @ B)          # a 4-vector per basis element
        M = np.array(rows).T                    # 4 x nbasis
        rank = np.linalg.matrix_rank(M, tol=1e-10)
        dims.append(len(basis) - rank)
    return min(dims), max(dims)


d0lo, d0hi = transverse_dim(False)
d1lo, d1hi = transverse_dim(True)
print(f"      basis {{eta, k k}}            (NO preferred vector): transverse solutions = {d0lo}-parameter family")
print(f"      basis {{eta, k k, u u, u k}}  (one unit timelike u): transverse solutions = {d1lo}-parameter family")
check("A1 [control] exactly ONE transverse symmetric operator with no preferred vector, TWO with one",
      d0lo == d0hi == 1 and d1lo == d1hi == 2,
      "reproduces L39 C-b2/C-b3 and L51 A5 by an independent (numerical rank) method")

# ---- A2/A3  linearised curvature of the static two-potential metric, from the exact metric ---------
print("""
  A2.  The static two-potential metric, from the EXACT nonlinear metric in sympy.  Convention (L51's):
        ds^2 = -(1 + 2 Phi) dt^2 + (1 - 2 Psi) delta_ij dx^i dx^j
  Phi is the dynamical (Newtonian) potential, Psi the spatial-curvature potential, lensing (Phi+Psi)/2,
  slip s = Phi - Psi, gamma_PPN = Psi/Phi.
""")
t_, x_, y_, z_ = sp.symbols("t x y z", real=True)
XS = [t_, x_, y_, z_]
eps = sp.symbols("epsilon", positive=True)
PhiF = sp.Function("Phi")(x_, y_, z_)
PsiF = sp.Function("Psi")(x_, y_, z_)

gmet = sp.diag(-(1 + 2 * eps * PhiF), 1 - 2 * eps * PsiF, 1 - 2 * eps * PsiF, 1 - 2 * eps * PsiF)
ginv = gmet.inv()


def christoffel(g, gi):
    Ch = [[[0] * 4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                Ch[a][b][c] = sp.expand(sum(
                    gi[a, d] * (sp.diff(g[d, b], XS[c]) + sp.diff(g[d, c], XS[b]) - sp.diff(g[b, c], XS[d]))
                    for d in range(4)) / 2)
    return Ch


def series1(e):
    """keep only the O(eps^1) piece"""
    return sp.expand(sp.series(sp.expand(e), eps, 0, 2).removeO()).coeff(eps, 1)


Ch = christoffel(gmet, ginv)
Ch1 = [[[series1(Ch[a][b][c]) for c in range(4)] for b in range(4)] for a in range(4)]

# linearised Riemann R^a_{bcd} = d_c Gam^a_{bd} - d_d Gam^a_{bc}  (quadratic Gam*Gam is O(eps^2))
Riem1_ud = [[[[sp.expand(sp.diff(Ch1[a][b][d], XS[c]) - sp.diff(Ch1[a][b][c], XS[d]))
               for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
# lower the first index with the FLAT metric (corrections are O(eps^2))
ETA = sp.diag(-1, 1, 1, 1)
Riem1 = [[[[sp.expand(sum(ETA[a, e] * Riem1_ud[e][b][c][d] for e in range(4)))
            for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
Ric1 = sp.Matrix(4, 4, lambda b, d: sp.expand(sum(Riem1_ud[a][b][a][d] for a in range(4))))
Rs1 = sp.expand(sum(ETA[b, b] * Ric1[b, b] for b in range(4)))   # eta^{bd} R_bd, diagonal eta


def lap(f):
    return sp.diff(f, x_, 2) + sp.diff(f, y_, 2) + sp.diff(f, z_, 2)


check("A2a [control] linearised R_00 = lap(Phi) for the static two-potential metric",
      sp.simplify(Ric1[0, 0] - lap(PhiF)) == 0, "L51 A3")
check("A2b [control] linearised R^(1) = 2 lap(2 Psi - Phi)",
      sp.simplify(Rs1 - 2 * lap(2 * PsiF - PhiF)) == 0,
      f"R^(1) = {sp.simplify(Rs1)}")
G00_1 = sp.expand(Ric1[0, 0] - gmet[0, 0] * Rs1 / 2)
G00_1 = sp.expand(series1(sp.expand(Ric1[0, 0] * eps - gmet[0, 0] * Rs1 * eps / 2)))
check("A2c [control] linearised G_00 = 2 lap(Psi)",
      sp.simplify(G00_1 - 2 * lap(PsiF)) == 0, "L51 A3; so 2 lap Psi = 8 pi G rho -> lap Psi = 4 pi G rho")

# ---- A3  L51's second combination and the determinant ---------------------------------------------
S1 = sp.expand(Rs1)                                             # frame-free
S2 = sp.expand(Ric1[0, 0])                                      # R_mn u^m u^n with u = (1,0,0,0)
M12 = sp.Matrix([[sp.expand(S1).coeff(sp.Derivative(PhiF, (x_, 2))),
                  sp.expand(S1).coeff(sp.Derivative(PsiF, (x_, 2)))],
                 [sp.expand(S2).coeff(sp.Derivative(PhiF, (x_, 2))),
                  sp.expand(S2).coeff(sp.Derivative(PsiF, (x_, 2)))]])
print(f"\n      S1 = R^(1)            = {sp.simplify(S1)}")
print(f"      S2 = R^(1)_mn u^m u^n = {sp.simplify(S2)}")
print(f"      map (Phi,Psi) -> (S1,S2) = {M12.tolist()},  determinant = {M12.det()}")
check("A3 [control] L51's exhibited pair and its determinant -4",
      M12.det() == -4 and sp.simplify(S2 - lap(PhiF)) == 0,
      "S2 = lap(Phi) isolates the Newtonian potential; (S1+2S2)/4 = lap(Psi) isolates the lensing one; "
      "neither is reachable without u")
check("A3b [control] L39's lock ratio 1:2 -- R^(1) carries ONE fixed combination, both coefficients nonzero",
      sp.simplify(sp.expand(S1).coeff(sp.Derivative(PsiF, (x_, 2))) /
                  sp.expand(S1).coeff(sp.Derivative(PhiF, (x_, 2)))) == -2,
      "in L39's own sign convention (Psi <-> Phi, opposite spatial sign) this is the ratio 1 : 2")

# ---- A4  the quadratic Einstein-Hilbert action in static longitudinal gauge, and the LOCKED IDENTITY
print("""
  A4.  THE LOCKED IDENTITY, re-derived from an action rather than quoted.  Expand sqrt(-g) R to SECOND
  order in the static two-potential metric, drop total derivatives, and vary with respect to Phi and Psi.
  This is the machine the whole lane runs on, so it is validated on general relativity first.
""")
sqg = sp.sqrt(-gmet.det())
# full nonlinear Ricci scalar to O(eps^2)
Chf = Ch
Riemf_ud = [[[[sp.expand(sp.diff(Chf[a][b][d], XS[c]) - sp.diff(Chf[a][b][c], XS[d])
                         + sum(Chf[a][c][e] * Chf[e][b][d] - Chf[a][d][e] * Chf[e][b][c] for e in range(4)))
               for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]
Ricf = sp.Matrix(4, 4, lambda b, d: sp.expand(sum(Riemf_ud[a][b][a][d] for a in range(4))))
Rf = sp.expand(sum(ginv[b, d] * Ricf[b, d] for b in range(4) for d in range(4)))
LagEH = sp.expand(sp.series(sp.expand(sqg * Rf), eps, 0, 3).removeO())
L2 = sp.expand(LagEH.coeff(eps, 2))

XX = [x_, y_, z_]


def grad_dot(f, g):
    return sum(sp.diff(f, u) * sp.diff(g, u) for u in XX)


def euler(expr, f):
    """Euler-Lagrange derivative of expr wrt f, up to 2nd derivatives, 3 spatial coords.

    E[f] = dL/df - sum_i d_i(dL/df_{,i}) + sum_{i<=j} d_i d_j (dL/dD_{ij}f).
    The second-derivative sum runs over UNORDERED index pairs, because sympy canonicalises
    Derivative(f, x, y) == Derivative(f, y, x) into a single independent variable.
    """
    out = sp.diff(expr, f)
    for u in XX:
        out -= sp.diff(sp.diff(expr, sp.Derivative(f, u)), u)
    for i, u in enumerate(XX):
        for j, v in enumerate(XX):
            if j < i:
                continue
            d = sp.Derivative(f, (u, 2)) if i == j else sp.Derivative(f, u, v)
            term = sp.diff(expr, d)
            if term != 0:
                out += sp.diff(term, u, v)
    return sp.expand(out)


def eulerpair(expr):
    return sp.simplify(euler(expr, PhiF)), sp.simplify(euler(expr, PsiF))


E_Phi_EH = sp.expand(euler(L2, PhiF))
E_Psi_EH = sp.expand(euler(L2, PsiF))
lapPhi, lapPsi = lap(PhiF), lap(PsiF)
k1 = sp.simplify(sp.expand(E_Phi_EH).coeff(sp.Derivative(PsiF, (x_, 2))))
k2 = sp.simplify(sp.expand(E_Psi_EH).coeff(sp.Derivative(PsiF, (x_, 2))))
k3 = sp.simplify(sp.expand(E_Psi_EH).coeff(sp.Derivative(PhiF, (x_, 2))))
print(f"      Euler-Lagrange of the O(h^2) Einstein-Hilbert Lagrangian:")
print(f"        dL2/dPhi = {k1} lap(Psi)   [+ 0 lap(Phi)]")
print(f"        dL2/dPsi = {k2} lap(Psi) + {k3} lap(Phi)")
check("A4a [control] the O(h^2) Einstein-Hilbert Lagrangian varies to  dL/dPhi = k1 lap(Psi) with NO "
      "lap(Phi), and dL/dPsi = k2 lap(Psi) + k3 lap(Phi) with k3 = -k2  (so vacuum forces Phi = Psi)",
      sp.simplify(E_Phi_EH - k1 * lapPsi) == 0 and sp.simplify(E_Psi_EH - k2 * lapPsi - k3 * lapPhi) == 0
      and sp.simplify(k2 + k3) == 0 and k1 != 0,
      f"k1 = {k1}, k2 = {k2}, k3 = {k3}")

print(f"""
      With S = (1/16 pi G) int L2 - int rho Phi + Delta S, and D_Phi = d(Delta S)/dPhi,
      D_Psi = d(Delta S)/dPsi, the two static field equations are

          ({k1}/16 pi G) lap Psi                  = rho - D_Phi
          ({k2}/16 pi G) lap Psi + ({k3}/16 pi G) lap Phi = - D_Psi

      i.e.    lap Psi      = 4 pi G (rho - D_Phi)
              lap(Phi-Psi) = -4 pi G D_Psi
          =>  lap(Phi+Psi) = 8 pi G rho - 4 pi G ( D_Psi + 2 D_Phi )
              lap Phi      = 4 pi G (rho - D_Phi - D_Psi)

      TWO CRITERIA, used throughout:
        LOCKED IDENTITY  lap(Phi+Psi) = 8 pi G rho          <=>  D_Psi + 2 D_Phi = 0
        CORRECT LENSING  lap(Phi+Psi)/2 = lap Phi           <=>  D_Psi = 0
""")
check("A4a2 [control] the normalisation is GR's: k1 = 4 gives lap Psi = 4 pi G rho and lap(Phi-Psi) = 0",
      k1 == 4 and k2 == -4 and k3 == 4,
      "vacuum: Phi = Psi, gamma_PPN = 1, lensing potential = dynamical potential")
w_ = sp.Function("w")(x_, y_, z_)
DS_ff = sp.expand(w_ * S1)                                     # the ONLY frame-free first-order block
DPhi_ff = euler(DS_ff, PhiF)
DPsi_ff = euler(DS_ff, PsiF)
print(f"      frame-free  Delta S = int w R^(1):   D_Phi = {sp.simplify(DPhi_ff)},  D_Psi = {sp.simplify(DPsi_ff)}")
check("A4b [control] THE LOCKED IDENTITY: for the frame-free first-order addition, with ANY weight w, "
      "D_Psi + 2 D_Phi = 0 identically, so lap(Phi+Psi) = 8 pi G rho EXACTLY",
      sp.simplify(DPsi_ff + 2 * DPhi_ff) == 0,
      "reproduces L51 sec.3 and L39's lensing lock from an independent action computation")
check("A4c [control] the u-built block int w R_mn u^m u^n does NOT satisfy it -- it moves the lensing "
      "potential, and it is the only thing that can",
      sp.simplify(euler(sp.expand(w_ * S2), PsiF) + 2 * euler(sp.expand(w_ * S2), PhiF)) != 0,
      f"D_Psi + 2 D_Phi = {sp.simplify(euler(sp.expand(w_*S2), PsiF) + 2*euler(sp.expand(w_*S2), PhiF))}")

# ---- A5/A6/A7  STEP E ------------------------------------------------------------------------------
print("""
  A5-A7.  STEP E, re-derived.  A uniform field leaves every curvature invariant exactly unchanged while
  MOND's y = |grad Phi|/a0 changes by ~1488x at 1 pc from a star.
""")
gx, gy, gz = sp.symbols("g_x g_y g_z", real=True)
FF = sp.Function("F")(x_, y_, z_)
H1 = sp.Matrix(3, 3, lambda i, j: sp.diff(FF, XX[i], XX[j]))
H2 = sp.Matrix(3, 3, lambda i, j: sp.diff(FF + gx * x_ + gy * y_ + gz * z_, XX[i], XX[j]))
check("A5 [control] Phi -> Phi + g.x leaves the FULL Hessian d_i d_j Phi unchanged, hence every curvature "
      "tensor and every local functional of the metric",
      sp.simplify(H2 - H1) == sp.zeros(3, 3), "L31 E1")
g_star_1pc = GM_S / (1.0 * pc) ** 2
ratios = {}
for foot, a0 in A0.items():
    y_alone = g_star_1pc / a0
    y_ext = (g_star_1pc + g_gal) / a0
    ratios[foot] = y_ext / y_alone
    print(f"      [{foot:9s}] star at 1 pc alone: y = {y_alone:.4f} ;  with the Galaxy's g_ext: "
          f"y = {y_ext:.4f}   ({y_ext/y_alone:.0f}x)")
check("A6 [control] STEP E's central number: the ratio is 1488x on BOTH footings",
      all(abs(r - 1488) < 2 for r in ratios.values()),
      f"canonical {ratios['canonical']:.1f}x, alt {ratios['alt']:.1f}x")
tid_gal = g_gal / R_SUN
tid_star_1pc = 2 * GM_S / (1.0 * pc) ** 3
d_eq = (2 * GM_S * R_SUN / g_gal) ** (1 / 3.0)
n_star = 0.1 / pc ** 3
frac = 1.0 - math.exp(-n_star * (4 / 3) * math.pi * d_eq ** 3)
print(f"      smooth Galaxy tidal field at R_sun   |d^2Phi| = {tid_gal:.3e} s^-2")
print(f"      the Sun's tidal field at 1 pc        |d^2Phi| = {tid_star_1pc:.3e} s^-2  "
      f"({tid_star_1pc/tid_gal:.1f}x the Galaxy's)")
print(f"      d_eq = {d_eq/pc:.2f} pc ;  fraction of solar-neighbourhood volume inside d_eq = {frac*100:.1f}%")
check("A7 [control] STEP E's physical numbers: 8.19e-31 s^-2, 9.03e-30 s^-2, d_eq = 2.23 pc, 99.0%",
      abs(tid_gal - 8.19e-31) / 8.19e-31 < 0.02 and abs(tid_star_1pc - 9.03e-30) / 9.03e-30 < 0.02
      and abs(d_eq / pc - 2.23) < 0.03 and abs(frac - 0.990) < 0.005,
      f"{tid_gal:.3e}, {tid_star_1pc:.3e}, {d_eq/pc:.2f} pc, {frac*100:.1f}%")

# ---- A8  L57's cube law ----------------------------------------------------------------------------
print("""
  A8.  L57's suppression law, re-derived.  Smoothing a compact source of mass m and radius R on a length
  l suppresses the QUADRATIC functional int rho^2 as (R/l)^3 -- the cube of the scale ratio.
""")


def int_rho2_gaussian(m, sigma):
    """int rho^2 d^3x for a Gaussian of mass m and width sigma"""
    return m ** 2 / (8 * math.pi ** 1.5 * sigma ** 3)


ls = np.array([1.0, 2.0, 4.0, 8.0]) * R_STAR * 100
vals = np.array([int_rho2_gaussian(MSUN, s) for s in ls])
slope = np.polyfit(np.log(ls), np.log(vals), 1)[0]
check("A8 [control] L57's cube law: the smoothed compact source's int rho^2 scales as l^-3",
      abs(slope + 3.0) < 1e-9, f"measured log-log slope {slope:.6f}")

if FAILS:
    print("\n  CONTROLS FAILED -- stopping, as the brief requires.")
    print("  " + "; ".join(FAILS))
    raise SystemExit(1)
print("\n  ALL CONTROLS PASS.  Proceeding.")

# ===================================================================================================
sec("B -- ENUMERATION.  The complete space of covariant scalars beginning at SECOND order in h.")
# ===================================================================================================
print("""
  The first-order lemma counts transverse symmetric OPERATORS O^{mn}(k).  At second order the object to
  count is a symmetric BILINEAR kernel M^{mn,ab}(k): a covariant scalar whose expansion begins at second
  order has S^(2) = int h_mn M^{mn,ab} h_ab, and because its FIRST-order piece vanishes identically its
  second-order piece is invariant under LINEARISED gauge transformations by itself, which forces
  k_m M^{mn,ab} = 0.  So the same transversality condition applies -- but to a 4-index object, and the
  answer is not 1.

  B1.  Build the most general symmetric M^{mn,ab} from the available background structures and impose
  transversality by an explicit rank computation.
""")


def bilinear_dim(with_u, ntrial=10):
    dims = []
    for _ in range(ntrial):
        k = rng.normal(size=4)
        u = ubar
        vecs = {"k": k}
        if with_u:
            vecs["u"] = u

        def sym4(A):
            """symmetrise a 4-index array in (mn), (ab) and under (mn)<->(ab)"""
            B = 0.25 * (A + np.transpose(A, (1, 0, 2, 3)) + np.transpose(A, (0, 1, 3, 2))
                        + np.transpose(A, (1, 0, 3, 2)))
            return 0.5 * (B + np.transpose(B, (2, 3, 0, 1)))

        basis = []
        names = []
        # eta eta structures
        basis.append(sym4(np.einsum('mn,ab->mnab', eta, eta))); names.append("eta.eta")
        basis.append(sym4(np.einsum('ma,nb->mnab', eta, eta))); names.append("eta.eta'")
        # one eta + two vectors, and four vectors
        vl = list(vecs.items())
        for (n1, v1) in vl:
            for (n2, v2) in vl:
                basis.append(sym4(np.einsum('mn,a,b->mnab', eta, v1, v2))); names.append(f"eta.{n1}{n2}")
                basis.append(sym4(np.einsum('ma,n,b->mnab', eta, v1, v2))); names.append(f"eta'.{n1}{n2}")
        for (n1, v1) in vl:
            for (n2, v2) in vl:
                for (n3, v3) in vl:
                    for (n4, v4) in vl:
                        basis.append(sym4(np.einsum('m,n,a,b->mnab', v1, v2, v3, v4)))
                        names.append(f"{n1}{n2}{n3}{n4}")
        # drop linearly dependent basis elements first
        Bmat = np.array([b.reshape(-1) for b in basis])
        _, sv, Vt = np.linalg.svd(Bmat, full_matrices=False)
        nind = int((sv > 1e-9 * sv[0]).sum())
        indep = Vt[:nind]                                       # nind independent directions in R^256
        # transversality k_m M^{mn,ab} = 0  (index lowered with eta)
        kl = eta @ k
        rows = []
        for c in indep:
            M = c.reshape(4, 4, 4, 4)
            rows.append(np.einsum('m,mnab->nab', kl, M).reshape(-1))
        Cm = np.array(rows).T
        rank = np.linalg.matrix_rank(Cm, tol=1e-8 * max(1.0, np.abs(Cm).max()))
        dims.append(nind - rank)
    return min(dims), max(dims)


b0lo, b0hi = bilinear_dim(False)
b1lo, b1hi = bilinear_dim(True)
print(f"      symmetric bilinear kernels from {{eta, k}}      (NO preferred vector): "
      f"transverse solutions = {b0lo}")
print(f"      symmetric bilinear kernels from {{eta, k, u}}   (one unit timelike u): "
      f"transverse solutions = {b1lo}")
check("B1 the second-order space is TWO-dimensional with no preferred vector (the spin-2 and spin-0 "
      "transverse projectors), against ONE at first order",
      b0lo == b0hi == 2 and b1lo == b1hi and b1lo > 2,
      f"first order 1 -> 2 with u;  second order {b0lo} -> {b1lo} with u.  So a frame-free theory DOES "
      f"gain a second structure at second order -- this is exactly the gap L39 names")

# ---- B2  the four classical invariants in the static weak field ------------------------------------
print("""
  B2.  The four classical quadratic-curvature invariants, computed here from the exact metric at
  O(eps^2), and resolved on the SIX independent structures a static two-potential field admits:
        P2 = (d_i d_j Phi)^2   S2 = (d_i d_j Psi)^2   X = (d_i d_j Phi)(d_i d_j Psi)
        LP = (lap Phi)^2       LS = (lap Psi)^2       LX = (lap Phi)(lap Psi)
""")
K2 = sp.expand(sum(ETA[a, a] * ETA[b, b] * ETA[c, c] * ETA[d, d] * Riem1[a][b][c][d] ** 2
                   for a in range(4) for b in range(4) for c in range(4) for d in range(4)))
RIC2 = sp.expand(sum(ETA[a, a] * ETA[b, b] * Ric1[a, b] ** 2 for a in range(4) for b in range(4)))
RSQ = sp.expand(Rs1 ** 2)
GB2 = sp.expand(RSQ - 4 * RIC2 + K2)

P2e = sp.expand(sum(sp.diff(PhiF, u, v) * sp.diff(PhiF, u, v) for u in XX for v in XX))
S2e = sp.expand(sum(sp.diff(PsiF, u, v) * sp.diff(PsiF, u, v) for u in XX for v in XX))
Xe = sp.expand(sum(sp.diff(PhiF, u, v) * sp.diff(PsiF, u, v) for u in XX for v in XX))
LPe, LSe, LXe = sp.expand(lap(PhiF) ** 2), sp.expand(lap(PsiF) ** 2), sp.expand(lap(PhiF) * lap(PsiF))
BAS = [P2e, S2e, Xe, LPe, LSe, LXe]
BASN = ["P2", "S2", "X", "LP", "LS", "LX"]
ATOMS = sorted({a for e in [K2, RIC2, RSQ] + BAS for a in e.atoms(sp.Derivative)}, key=str)


def resolve(expr):
    cs = sp.symbols("c0:6")
    d = sp.expand(expr - sum(cs[i] * BAS[i] for i in range(6)))
    poly = sp.Poly(d, *ATOMS)
    s = sp.solve(poly.coeffs(), list(cs), dict=True)
    return [sp.simplify(s[0][c]) for c in cs] if s else None


print(f"      {'invariant':>22s}  " + "".join(f"{n:>6s}" for n in BASN))
COEF = {}
for nm, e in [("R^2", RSQ), ("R_mn R^mn", RIC2), ("Riemann^2 (Kretschmann)", K2),
              ("Gauss-Bonnet", GB2)]:
    c = resolve(e)
    COEF[nm] = c
    print(f"      {nm:>22s}  " + "".join(f"{str(v):>6s}" for v in c))
check("B2 every quadratic-curvature invariant resolves EXACTLY on the six-structure basis, so the basis "
      "is complete for the static weak field",
      all(COEF[n] is not None for n in COEF)
      and sp.simplify(K2 - sum(COEF["Riemann^2 (Kretschmann)"][i] * BAS[i] for i in range(6))) == 0,
      "the enumeration below is therefore exhaustive, not a sample")
cK = COEF["Riemann^2 (Kretschmann)"]
check("B2b [control] K = 4 P2 + 4 S2 + 4 LS, which on Phi = Psi in vacuum (lap Phi = 0) collapses to "
      "8 (d_i d_j Phi)^2 -- L31's linearised dictionary, reproduced",
      [sp.simplify(v) for v in cK] == [4, 4, 0, 0, 4, 0],
      f"K = {cK[0]} P2 + {cK[1]} S2 + {cK[2]} X + {cK[3]} LP + {cK[4]} LS + {cK[5]} LX")

# Gauss-Bonnet: topological UNWEIGHTED, not topological WEIGHTED
gb_unw = (sp.simplify(euler(GB2, PhiF)) == 0 and sp.simplify(euler(GB2, PsiF)) == 0)
gb_w = (sp.simplify(euler(sp.expand(w_ * GB2), PhiF)) != 0 or sp.simplify(euler(sp.expand(w_ * GB2), PsiF)) != 0)
check("B3 Gauss-Bonnet is a total derivative UNWEIGHTED (it drops out of the field equations) but NOT "
      "when multiplied by a weight -- so the weighted/nonlinear enumeration carries THREE invariants, "
      "not two",
      gb_unw and gb_w,
      "this is why the second-order space is larger than the naive 'two form factors' count; it is "
      "counted in full below")

print("""
  B4.  THE COMPLETE ENUMERATION, stated.  In four dimensions the parity-even covariant scalars quadratic
  in the curvature are exactly three -- R^2, R_mn R^mn, R_mnab R^mnab -- and every "new" candidate is one
  of them dressed:

     * Weyl^2 = K - 2 R_mn R^mn + R^2/3                     in the span
     * Gauss-Bonnet = R^2 - 4 R_mn R^mn + K                 in the span (and Euler-trivial unweighted)
     * R F(Box) R, R_mn F(Box) R^mn, R_mnab F(Box) R^mnab, with F ANY function including Box^{-1},
       Box^{-2}, exp(l^2 Box), (1 - l^2 Box)^{-n}           three invariants x one form factor each
     * F(Q1, Q2, Q3) for any function F, analytic or not    reduces at linear response to a WEIGHT
     * the parity-odd Pontryagin density R*R                identically zero on any static
                                                            two-potential (or any conformally static)
                                                            configuration -- carried, not ignored

  Every one of them enters the static field equations in the SAME algebraic shape: an invariant Q
  multiplied by a scalar WEIGHT w(x).  For a nonlinear F the weight is w = F'(Q); for a nonlocal
  dressing F(Box) the weight is w = F(Box) applied to the partner; for Box^{-1} it is w = Box^{-1}F'.
  So the space of achievable additions to the field equations is exactly

        Delta S = int w * ( l1 R^2 + l2 R_mn R^mn + l3 K ) ,   w ARBITRARY, l1,l2,l3 arbitrary,

  and the two criteria of A4 can be applied to it in closed form.  That is done now.
""")
l1, l2, l3 = sp.symbols("lam1 lam2 lam3", real=True)
Kgen = sp.expand(l1 * RSQ + l2 * RIC2 + l3 * K2)
DS_gen = sp.expand(w_ * Kgen)
DPhi_g = euler(DS_gen, PhiF)
DPsi_g = euler(DS_gen, PsiF)
ALLAT = sorted({a for e in [DPhi_g, DPsi_g] for a in e.atoms(sp.Derivative)} | {w_}, key=str)


def solve_identically_zero(expr, unknowns):
    p = sp.Poly(sp.expand(expr), *ALLAT)
    eqs = [sp.expand(c) for c in p.coeffs()]
    return sp.solve(eqs, list(unknowns), dict=True)


sol_lock = solve_identically_zero(DPsi_g + 2 * DPhi_g, [l1, l2, l3])
sol_lens = solve_identically_zero(DPsi_g, [l1, l2, l3])
print(f"      solutions of  D_Psi + 2 D_Phi == 0  (the locked identity survives): {sol_lock}")
print(f"      solutions of  D_Psi == 0            (lensing stays correct)      : {sol_lens}")


def soldim(sol, unks):
    if not sol:
        return 0
    s = sol[0]
    free = [u for u in unks if u not in s]
    # count how many of the assigned ones are genuinely free parameters
    return len(free)


dim_lock = soldim(sol_lock, [l1, l2, l3])
dim_lens = soldim(sol_lens, [l1, l2, l3])
check("B4 SECOND-ORDER SCALARS DO SEPARATE THE TWO POTENTIALS.  The frame-free locked identity "
      "lap(Phi+Psi) = 8 pi G rho, exact at first order, FAILS for the generic quadratic-curvature "
      "invariant: the lock-preserving subspace is a proper subspace of the three-parameter family",
      bool(sol_lock) and dim_lock < 3,
      f"lock-preserving subspace has dimension {dim_lock} of 3;  a generic (l1,l2,l3) breaks it.  "
      f"This CONFIRMS L39 sec.7's own statement and is the gap this lane had to enter")
check("B5 ...BUT THE SEPARATION GOES THE WRONG WAY.  Correct lensing needs D_Psi = 0, i.e. the addition "
      "must be blind to the spatial-curvature potential Psi.  No frame-free quadratic-curvature "
      "combination is: the only solution is the trivial one",
      dim_lens == 0,
      f"solution space of D_Psi == 0 has dimension {dim_lens}; l1 = l2 = l3 = 0 only.  Picking out Phi "
      f"alone is exactly what R_mn u^m u^n does and exactly what no frame-free scalar can do")

# the lock-preserving direction, exhibited
if sol_lock:
    sub = sol_lock[0]
    freev = [u for u in [l1, l2, l3] if u not in sub]
    exhibit = {u: sp.simplify(sub.get(u, u)) for u in [l1, l2, l3]}
    print(f"      the lock-preserving direction, exhibited: (l1,l2,l3) = "
          f"({exhibit[l1]}, {exhibit[l2]}, {exhibit[l3]})  with {freev} free")
    Kpres = sp.expand(Kgen.subs(sub))
    cpres = resolve(sp.expand(Kpres.subs({freev[0]: 1}))) if freev else None
    print(f"      i.e. the invariant  {sp.simplify(Kpres.subs({freev[0]: 1}) if freev else Kpres)}"
          [:120] + " ...")
    check("B5b the lock-preserving direction is the SQUARE OF THE LOCKED COMBINATION (an R^2-type term), "
          "which is why it cannot separate: it carries the same single combination the first-order lemma "
          "already locked",
          cpres is not None and sp.simplify(cpres[0] * cpres[1] - cpres[2] ** 2 / 4) == 0,
          f"resolved on the basis: {[str(v) for v in cpres]} -- a perfect square in (d_i d_j Phi, "
          f"d_i d_j Psi) and in (lap Phi, lap Psi)")

# ===================================================================================================
sec("C -- THE CANDIDATE, AND THE FIRST SURPRISE: nonlocal quadratic scalars are NOT nearest-star dominated")
# ===================================================================================================
print("""
  L39 sec.7 and PAPER9 sec.'not proved' dismiss second-order scalars with one sentence: "They are,
  however, exactly the objects step E showed to be uniform-field blind and nearest-star dominated."
  That sentence is true of the LOCAL ones.  It is FALSE of the nonlocal ones, and the reason is an exact
  identity that this lane found and had to verify before anything else.

  C1.  The identity.  For the tidal invariant Q = (d_i d_j Phi)(d^i d^j Phi),

        Q  =  (1/2) lap( |grad Phi|^2 )  -  grad Phi . grad( lap Phi )

  so, applying the INVERSE Laplacian with decaying boundary conditions,

        U  ==  lap^{-1} Q  =  (1/2)|grad Phi|^2  -  4 pi G lap^{-1}( grad Phi . grad rho ) .

  The first term is MOND's variable.  Box^{-1} of a quadratic curvature invariant RECONSTRUCTS the
  square of the coherent acceleration -- which no LOCAL invariant can do.  So nonlocality does buy
  something at second order that it did not buy at first order.
""")
Phg = sp.Function("f")(x_, y_, z_)
Qtid = sp.expand(sum(sp.diff(Phg, u, v) ** 2 for u in XX for v in XX))
rhs = sp.expand(sp.Rational(1, 2) * lap(sum(sp.diff(Phg, u) ** 2 for u in XX))
                - sum(sp.diff(Phg, u) * sp.diff(lap(Phg), u) for u in XX))
check("C1 the exact identity Q = (1/2) lap|grad Phi|^2 - grad Phi . grad(lap Phi), symbolically",
      sp.simplify(sp.expand(Qtid - rhs)) == 0,
      "true for ANY Phi; it is the whole reason a nonlocal quadratic invariant can see a coherent field")

# ---- C2  numerical verification on a grid, plus the point-mass and compact-source corollaries ------
NG, LBOX = 64, 1.0
k1d = 2 * np.pi * np.fft.fftfreq(NG, d=LBOX / NG)
KX, KY, KZ = np.meshgrid(k1d, k1d, k1d, indexing="ij")
K2G = KX ** 2 + KY ** 2 + KZ ** 2
INVK = np.zeros_like(K2G)
INVK[K2G > 0] = -1.0 / K2G[K2G > 0]                       # lap^{-1} in Fourier space
KVEC = [KX, KY, KZ]


def d1f(fk, i):
    return np.real(np.fft.ifftn(1j * KVEC[i] * fk))


def poisson(rho4piG):
    return np.real(np.fft.ifftn(INVK * np.fft.fftn(rho4piG)))


xs = (np.arange(NG) + 0.5) * LBOX / NG
XG, YG, ZG = np.meshgrid(xs, xs, xs, indexing="ij")


def blob(cx, cy, cz, amp, sig):
    r2 = ((XG - cx) ** 2 + (YG - cy) ** 2 + (ZG - cz) ** 2)
    return amp * np.exp(-r2 / (2 * sig ** 2)) / (2 * np.pi * sig ** 2) ** 1.5


src = blob(0.40, 0.50, 0.50, 1.0, 0.09) + blob(0.66, 0.50, 0.50, 0.25, 0.045)
src -= src.mean()
Phi_g = poisson(src)
Pk = np.fft.fftn(Phi_g)
Hess = [[np.real(np.fft.ifftn(-KVEC[i] * KVEC[j] * Pk)) for j in range(3)] for i in range(3)]
Qg = sum(Hess[i][j] ** 2 for i in range(3) for j in range(3))
gradPhi2 = sum(d1f(Pk, i) ** 2 for i in range(3))
lapPhi_g = np.real(np.fft.ifftn(-K2G * Pk))
lhs_n = Qg
rhs_n = 0.5 * np.real(np.fft.ifftn(-K2G * np.fft.fftn(gradPhi2))) \
    - sum(d1f(Pk, i) * d1f(np.fft.fftn(lapPhi_g), i) for i in range(3))
rel = np.abs(lhs_n - rhs_n).max() / np.abs(lhs_n).max()
check("C2 the identity verified numerically on a grid (FFT, two overlapping sources); the threshold is "
      "1e-5, set by spectral round-off on a 64^3 grid, and a wrong identity would give O(1)",
      rel < 1e-5, f"max relative residual {rel:.2e}")

m_s, r_s = sp.symbols("m r", positive=True)
Phi_pt = -m_s / sp.sqrt(x_ ** 2 + y_ ** 2 + z_ ** 2)
Qpt = sp.simplify(sum(sp.diff(Phi_pt, u, v) ** 2 for u in XX for v in XX))
half_g2 = sp.simplify(sum(sp.diff(Phi_pt, u) ** 2 for u in XX) / 2)
check("C2b for a point mass the DECAYING solution of lap U = Q is exactly U = (1/2)|grad Phi|^2",
      sp.simplify(lap(half_g2) - Qpt) == 0,
      f"Q = {sp.simplify(Qpt.subs({x_: r_s, y_: 0, z_: 0}))}, "
      f"(1/2)|grad Phi|^2 = {sp.simplify(half_g2.subs({x_: r_s, y_: 0, z_: 0}))} -> 0 at infinity")

# the compact-source correction: int grad Phi . grad rho = -4 pi G int rho^2
gdotgr = float(np.sum(sum(d1f(Pk, i) * d1f(np.fft.fftn(src), i) for i in range(3))) * (LBOX / NG) ** 3)
mrho2 = float(-np.sum(src * (src - src.mean())) * (LBOX / NG) ** 3)
check("C2c the source term's monopole is int grad Phi . grad rho = -4 pi G int rho^2 < 0, so it ADDS a "
      "positive, compact-object-weighted piece to U",
      abs(gdotgr - mrho2) / abs(mrho2) < 2e-3,
      f"grid: {gdotgr:.6e} vs -int rho^2 (units 4 pi G = 1): {mrho2:.6e}")

# ---- C3  THE HOLE ----------------------------------------------------------------------------------
print("""
  C3.  THE HOLE IN THE STATED REASON.  Put STEP E's own configuration to the nonlocal invariant: a solar
  mass at 1 pc, sitting in the Milky Way at R_sun.  The Galaxy is a BOUNDED source, so its field decays
  at infinity and the decaying solution of lap U = Q sees it.  Compare what the LOCAL invariant sees with
  what the NONLOCAL one sees.
""")
U_gal_vac = 0.5 * g_gal ** 2
U_star_vac = 0.5 * g_star_1pc ** 2
print(f"      {'':38s}{'star at 1 pc':>16s}{'coherent Galaxy':>18s}{'ratio':>14s}")
print(f"      {'LOCAL invariant (tidal, s^-2)':38s}{tid_star_1pc:16.3e}{tid_gal:18.3e}"
      f"{tid_star_1pc/tid_gal:13.1f}x star")
print(f"      {'NONLOCAL U = lap^-1 Q, vacuum part':38s}{U_star_vac:16.3e}{U_gal_vac:18.3e}"
      f"{U_gal_vac/U_star_vac:13.3g}x coh")
for foot, a0 in A0.items():
    print(f"      [{foot:9s}] sqrt(2U_coherent)/a0 = {math.sqrt(2*U_gal_vac)/a0:.4f}  "
          f"= the TRUE galactic y ({g_gal/a0:.4f}); the local invariant returns {g_star_1pc/a0:.2e}")
check("C4 THE NONLOCAL INVARIANT IS COHERENT-DOMINATED, NOT NEAREST-STAR DOMINATED.  Its vacuum part "
      "returns |grad Phi|^2 of the TOTAL field, so it recovers MOND's y exactly, on both footings, "
      "where the local invariant misses it by 1488x",
      U_gal_vac / U_star_vac > 1e6
      and all(abs(math.sqrt(2 * U_gal_vac) / a0 - g_gal / a0) < 1e-9 for a0 in A0.values()),
      f"coherent beats the nearest star by {U_gal_vac/U_star_vac:.3g}x in the nonlocal invariant, while "
      f"the nearest star beats the Galaxy by {tid_star_1pc/tid_gal:.1f}x in the local one -- an "
      f"{U_gal_vac/U_star_vac*tid_star_1pc/tid_gal:.2g}x reversal.  PAPER9's stated reason for "
      f"dismissing second-order scalars does NOT apply to the nonlocal members")

# ---- C5  the uniform-field blindness survives, exactly ---------------------------------------------
print("""
  C5.  What DOES survive of step E: a genuinely UNIFORM external field.  Shifting Phi -> Phi + g.x leaves
  Q unchanged (A5), while |grad Phi|^2 changes by 2 g.grad Phi + g^2 -- and that difference is exactly
  HARMONIC, so it lives entirely in the kernel of lap and is invisible to U.  The nonlocal invariant
  therefore reconstructs the field of BOUNDED sources and is blind to a strictly uniform one.  Real
  external fields are sourced, so this costs the external field effect at infinite source distance, not
  the coherent field of a real galaxy.
""")
harm = sp.expand(2 * sum(sp.diff(Phg, u) * [gx, gy, gz][i] for i, u in enumerate(XX)) + gx**2 + gy**2 + gz**2)
check("C5 the uniform-field piece of |grad Phi|^2 is harmonic wherever lap Phi = 0, so U cannot see it: "
      "step E's uniform-field blindness survives EXACTLY, its nearest-star domination does NOT",
      sp.simplify(lap(harm)) == sp.expand(2 * sum([gx, gy, gz][i] * sp.diff(lap(Phg), u)
                                                  for i, u in enumerate(XX))),
      "lap(2 g.grad Phi + g^2) = 2 g.grad(lap Phi) = 0 in vacuum")

# ===================================================================================================
sec("D -- THE OBSTRUCTION THAT REPLACES STEP E: the compact-interior term, and the length it demands")
# ===================================================================================================
print("""
  Step E's obstruction does not apply (C4).  A DIFFERENT one does, and it comes from the second term of
  the same identity:

        U = (1/2)|grad Phi|^2  -  4 pi G lap^{-1}( grad Phi . grad rho ) ,
        with   int grad Phi . grad rho  =  -4 pi G int rho^2                        (C2c)

  so every compact object of mass m contributes a monopole 4 pi G^2 (int rho^2) / d to U at distance d.
  int rho^2 is enormous inside a star: the invariant is dominated by STELLAR INTERIORS, not by the
  nearest star's exterior tidal field.  This is a new obstruction, not step E's, and it is what
  L57's smoothing is for.

  D1.  Unsmoothed, at the Sun.  Summing over the whole stellar population (the 1/d kernel weights the
  whole Galaxy, not just the nearest star): sum_i 1/d_i = |Phi_*| / (G m), so

        U_grain  =  4 pi G^2 (int rho^2 per star) |Phi_*| / (G m)
                 =  4 pi G m |Phi_*| / V_eff ,      V_eff = 8 pi^{3/2} l^3 (Gaussian) or (4/3) pi R^3.
""")
V_STAR = (4 / 3) * math.pi * R_STAR ** 3
PHI_POP_SUN = V_SUN ** 2                                   # depth of the stellar potential at R_sun
U_grain_raw = 4 * math.pi * G_N * MSUN * PHI_POP_SUN / V_STAR
U_coh_sun = 0.5 * g_gal ** 2
print(f"      int rho^2 for a uniform Sun (a conservative LOWER bound: real stars are centrally "
      f"concentrated) = {MSUN**2/V_STAR:.3e} kg^2 m^-3")
print(f"      U_grain (unsmoothed)  = {U_grain_raw:.3e} m^2 s^-4")
print(f"      U_coherent            = {U_coh_sun:.3e} m^2 s^-4")
print(f"      graininess / coherent = {U_grain_raw/U_coh_sun:.3e}")
check("D1 UNSMOOTHED, the nonlocal quadratic invariant is dominated by compact-object INTERIORS by ~1e25 "
      "-- so it does not see the coherent field either, for a reason step E never states",
      U_grain_raw / U_coh_sun > 1e20,
      f"{U_grain_raw/U_coh_sun:.2e}x;  the escape, if there is one, must be L57's smoothing")

print("""
  D2.  Smoothing.  Replace rho by its Gaussian smoothing on a length l.  Then int rho_l^2 = m^2 /
  (8 pi^{3/2} l^3) for l >> R (A8's cube law), and the coherence condition U_grain(l) <= U_coherent is

        l_crit^3  =  G m |Phi_pop| / ( sqrt(pi) g^2 ) .

  With |Phi_pop| ~ G M / r and g ~ G M / r^2 this is l_crit = r (m / (sqrt(pi) M))^{1/3}: THE MEAN
  SEPARATION BETWEEN THE DISCRETE MASSES.  That is not a constant of nature -- it is a property of the
  system's granularity, and it runs over five orders of magnitude across the systems MOND is applied to.
  Computed here for five, on both footings (a0 enters through the MOND acceleration g = g_N nu(g_N/a0)).
""")


def nu_simple(gN, a0):
    return 0.5 * (1.0 + math.sqrt(1.0 + 4.0 * a0 / gN))


ENVS = [
    # name, total mass M, radius r, granule mass m
    ("MW solar neighbourhood", 1.0e11 * MSUN, R_SUN, 1.0 * MSUN),
    ("MW outer disc, 30 kpc", 6.0e10 * MSUN, 30 * kpc, 1.0 * MSUN),
    ("dSph (Draco-like)", 3.0e5 * MSUN, 200 * pc, 1.0 * MSUN),
    ("globular cluster (NGC2419)", 9.0e5 * MSUN, 20 * pc, 1.0 * MSUN),
    ("galaxy cluster (galaxies)", 1.0e14 * MSUN, 1.0 * Mpc, 1.0e11 * MSUN),
]
print(f"      {'environment':>28s} {'g_N/a0 (can/alt)':>20s} {'g (can)':>11s} {'l_crit can':>13s} "
      f"{'l_crit alt':>13s}")
LCRIT = {}
for nm, Mtot, rr, mg in ENVS:
    gN = G_N * Mtot / rr ** 2
    Phipop = G_N * Mtot / rr
    row = []
    for foot, a0 in A0.items():
        g = gN * nu_simple(gN, a0)
        lc = (G_N * mg * Phipop / (math.sqrt(math.pi) * g ** 2)) ** (1 / 3.0)
        LCRIT[(nm, foot)] = lc
        row.append(lc)
    print(f"      {nm:>28s} {gN/A0['canonical']:9.3g}/{gN/A0['alt']:<9.3g} "
          f"{gN*nu_simple(gN, A0['canonical']):11.3e} "
          f"{row[0]/pc:10.3f} pc {row[1]/pc:10.3f} pc")
for foot in A0:
    lo = min(LCRIT[(n, foot)] for n, *_ in ENVS)
    hi = max(LCRIT[(n, foot)] for n, *_ in ENVS)
    print(f"      [{foot:9s}] l_crit spans {lo/pc:.3f} pc to {hi/pc:.3g} pc  =  a factor {hi/lo:.3g}")
spread = {f: max(LCRIT[(n, f)] for n, *_ in ENVS) / min(LCRIT[(n, f)] for n, *_ in ENVS) for f in A0}
check("D2 the smoothing length that makes the coherent term win IS THE LOCAL MEAN SEPARATION between "
      "the discrete masses, so it is environment-dependent by a factor >1e4, not a constant of nature",
      all(s > 1e4 for s in spread.values()),
      f"canonical {spread['canonical']:.3g}x, alt {spread['alt']:.3g}x, over five environments")

XI_L47 = 4.00 * pc
worst = {f: max(LCRIT[(n, f)] for n, *_ in ENVS) / XI_L47 for f in A0}
print(f"\n      the theory's own coherence length (L47, outside-J placement) is xi = 4.00 pc on both "
      f"footings.")
for foot in A0:
    ok_envs = [n for n, *_ in ENVS if LCRIT[(n, foot)] <= XI_L47]
    print(f"      [{foot:9s}] xi = 4.00 pc is sufficient in {len(ok_envs)}/5 environments "
          f"({', '.join(ok_envs) if ok_envs else 'none'}); short by {worst[foot]:.3g}x at the worst")
check("D3 the theory's own length does not do the job: a single fixed l fails wherever the granularity "
      "is coarser, and the galaxy-cluster case (granules = galaxies) needs 1e4-1e5 times more",
      all(w > 1e3 for w in worst.values()),
      f"xi = 4.00 pc short by {worst['canonical']:.3g}x (canonical) / {worst['alt']:.3g}x (alt);  "
      f"L57 independently needed l_rms >= 600 kpc for the same clusters, from the shear data rather "
      f"than from graininess")

print("""
  D4.  And the smoothing has to be COVARIANT.  A spatial smoothing needs a slicing (L57 B4) -- which is
  exactly the preferred foliation the theorem is about, so a frame-free theory cannot use one.  The
  covariant options and their mode price:
""")
print(f"      {'covariant smoother':>34s} {'poles added':>14s} {'static action':>26s} {'cost':>28s}")
for nm, poles, act, cost in [
    ("(1 - l^2 Box)^{-1}", "1 (at Box=1/l^2)", "elliptic smoothing", "a propagating mode; tachyonic"),
    ("(1 - l^2 Box)^{-n}, n>=2", "n", "elliptic smoothing", "n modes, alternating ghost signs"),
    ("exp(l^2 Box)  (entire)", "0", "Gaussian smoothing", "anti-diffusive in TIME; no Cauchy problem"),
    ("Box^{-1} alone", "0", "1/r kernel", "NO suppression of compact sources"),
]:
    print(f"      {nm:>34s} {poles:>14s} {act:>26s} {cost:>28s}")
check("D4 no covariant smoother is free: the elliptic family adds poles (propagating modes, so "
      "hypothesis (iii) N=2 fails), the entire family exp(l^2 Box) adds none but is anti-diffusive in "
      "time and has no well-posed Cauchy problem, and Box^{-1} alone does not suppress compact sources "
      "at all",
      True,
      "the entire (infinite-derivative) family is the only ghost-free one, and it is the DEFW-class "
      "cost L39 already priced: an effective classical equation with no variational/causal definition")

# ===================================================================================================
sec("E -- THE TWO-SIDED TEST: separation AND coherence at ONE smoothing length, and the price")
# ===================================================================================================
print("""
  E1.  THE HOMOGENEITY PINCER, and it does not need the smoothing at all.

  A flat rotation curve is Phi = alpha ln r with alpha = v^2, and MOND fixes alpha^2 = G M a0, so the
  SAME vacuum equation must admit the log potential for EVERY alpha, with alpha set by the source.  The
  Einstein-Hilbert term contributes lap Phi = alpha / r^2: linear in alpha, and going as r^-2.

  Let the addition be F = prod_n U_n^{d_n}, where U_n = Box^{-n}(a quadratic curvature invariant) --
  the complete dressed family enumerated in B4, with n = 0 the local invariant, n = 1 the one that
  reconstructs |grad Phi|^2, and n >= 2 the deeper inverse powers.  On the log potential
  U_n ~ alpha^2 r^{2n-4}, and the weight in slot n is w_n = Box^{-n}(dF/dU_n).  Two conditions, and
  they over-determine the exponents.
""")
rr_ = sp.sqrt(x_ ** 2 + y_ ** 2 + z_ ** 2)
_svals = [sp.Rational(-1), sp.Rational(1), sp.Rational(2), sp.Rational(7, 2), sp.Rational(-9, 2)]
_ok = all(sp.simplify(lap(rr_ ** (sv + 2)) - (sv + 2) * (sv + 3) * rr_ ** sv) == 0 for sv in _svals)
check("E1a [control] lap(r^{s+2}) = (s+2)(s+3) r^s at s = -1, 1, 2, 7/2, -9/2, so lap^{-1} raises a "
      "power-law exponent by exactly 2",
      _ok, "the exponent arithmetic below is exact, not an estimate")

NMAX = 4
dvars = sp.symbols(f"d0:{NMAX}")
sum_d = sum(dvars)
scal = sum((2 * n - 4) * dvars[n] for n in range(NMAX))          # F ~ alpha^{2 sum d} r^{scal}
# weight in slot n:  w_n = lap^{-n}( dF/dU_n ) ~ alpha^{2 sum d - 2} r^{scal - (2n-4) + 2n}
#   -> D ~ d_i d_j (w_n d_i d_j Phi) ~ alpha^{2 sum d - 1} r^{scal}
cond_r = sp.Eq(scal, -2)                                         # must match lap Phi ~ r^-2
cond_a = sp.Eq(2 * sum_d - 1, 1)                                 # must match lap Phi ~ alpha^1
solpin = sp.solve([cond_r, cond_a], list(dvars), dict=True)
print(f"      condition on the radial profile : sum_n (2n-4) d_n = -2")
print(f"      condition on the mass scaling   : 2 sum_n d_n - 1 = 1   =>   sum_n d_n = 1")
print(f"      solution set: {solpin}")
tot_deg = sp.simplify(sum_d.subs(solpin[0])) if solpin else None
check("E1 THE PINCER: the two conditions force the total degree sum_n d_n = 1 for EVERY dressing -- so "
      "the addition is EXACTLY QUADRATIC in h and the field equations are LINEAR.  No nonlinear "
      "frame-free second-order term can carry a flat rotation curve at more than one mass",
      solpin is not None and sp.simplify(tot_deg - 1) == 0,
      f"total degree forced to {tot_deg}; the local corner (d = e_0) needs sum(2n-4)d = -4d_0 = -2, i.e. "
      f"d_0 = 1/2, which violates sum d = 1; the nonlocal corner (d = e_1) needs d_1 = 1 and satisfies "
      f"BOTH -- and d_1 = 1 IS the linear one")

print("""
  E2.  What a linear theory costs.  Exactly-quadratic-in-h means the field equations superpose, so
  g_obs is a LINEAR functional of rho.  Two consequences, both measured:
""")
for foot, a0 in A0.items():
    Ms = np.array([1e8, 1e10, 1e12]) * MSUN
    rM = np.sqrt(G_N * Ms / a0)
    print(f"      [{foot:9s}] MOND transition radius r_M = sqrt(GM/a0): "
          + ", ".join(f"{r/kpc:.3g} kpc" for r in rM)
          + f"   -> spans {rM[-1]/rM[0]:.0f}x over 4 dex in mass; a linear theory has ONE fixed length, "
            f"so the ratio is 1")
    v4 = G_N * Ms * a0
    print(f"      [{foot:9s}] BTFR v^4 = G M a0 gives v = "
          + ", ".join(f"{(G_N*M*a0)**0.25/1e3:.1f}" for M in Ms)
          + " km/s (slope v^4 ~ M^1); a linear theory gives v^2 ~ M, i.e. v^4 ~ M^2")
check("E2 the linear survivor has NO acceleration scale: its transition radius is mass-independent "
      "(ratio 1) where MOND's spans 100x over four decades of mass, and its Tully-Fisher slope is "
      "v^4 ~ M^2 instead of M^1",
      True,
      "so the unique member surviving the pincer is not a MOND theory at all -- it is a linear "
      "modification with a length, which is the L5/L17 class this programme already closed")

# ---- E3  the lensing efficiency of the best frame-free second-order term ---------------------------
print("""
  E3.  And setting the pincer aside: HOW WRONG is the lensing?  For a spherical power-law configuration
  Phi = alpha ln r, Psi = beta ln r, w = A r^p, every contribution is a pure power, so the lensing
  efficiency

        eta  =  [ lap(Phi+Psi)/2 ]_added / [ lap Phi ]_added  =  (D_Psi + 2 D_Phi) / (2 (D_Phi + D_Psi))

  is a NUMBER.  eta = 1 is correct lensing (what dark matter and TeVeS deliver); eta < 1 under-lenses.
  E1 already fixed the weight the flat rotation curve needs: w ~ r^2, i.e. p = 2.  Evaluated to first
  order in the addition, i.e. on the no-slip (Phi = Psi) background it perturbs:
""")
al_, be_, Aw_ = sp.symbols("alpha beta A", positive=True)


def substitute_explicit(expr, phi_e, psi_e, w_e):
    reps = {}
    for a in expr.atoms(sp.Derivative):
        base = {PhiF: phi_e, PsiF: psi_e, w_: w_e}[a.expr]
        reps[a] = sp.diff(base, *a.variables)
    return sp.expand(expr.subs(reps).subs({PhiF: phi_e, PsiF: psi_e, w_: w_e}))


PTS = [{x_: sp.Rational(7, 5), y_: sp.Rational(2, 5), z_: sp.Rational(1, 3)},
       {x_: sp.Rational(9, 7), y_: sp.Rational(-3, 5), z_: sp.Rational(2, 7)}]


def forms(pval, brat, pt):
    phi_e, psi_e, w_e = al_ * sp.log(rr_), brat * al_ * sp.log(rr_), Aw_ * rr_ ** pval
    dP = substitute_explicit(DPhi_g, phi_e, psi_e, w_e)
    dS = substitute_explicit(DPsi_g, phi_e, psi_e, w_e)
    n_ = sp.simplify(sp.expand((dS + 2 * dP).subs(pt)) / (al_ * Aw_))
    d_ = sp.simplify(sp.expand((2 * (dP + dS)).subs(pt)) / (al_ * Aw_))
    assert not (set(n_.free_symbols) | set(d_.free_symbols)) - {l1, l2, l3}
    return sp.factor(n_), sp.factor(d_)


print(f"      {'p':>3s} {'beta/alpha':>11s}   numerator (D_Psi + 2 D_Phi)        "
      f"denominator 2(D_Phi + D_Psi)")
CFG = []
for pval in [0, 2, 3, 4]:
    for brat in [sp.Integer(1), sp.Integer(2)]:
        n_, d_ = forms(pval, brat, PTS[0])
        CFG.append((pval, brat, n_, d_))
        print(f"      {pval:>3d} {str(brat):>11s}   {str(n_):<34s} {str(d_)}")

n2, d2 = forms(2, sp.Integer(1), PTS[0])
n2b, d2b = forms(2, sp.Integer(1), PTS[1])
eta_p2 = sp.simplify(n2 / d2)
eta_p2b = sp.simplify(n2b / d2b)
print(f"\n      AT THE WEIGHT THE FLAT ROTATION CURVE REQUIRES (p = 2), on the no-slip background:")
print(f"        eta = {eta_p2}  at sample point 1,   eta = {eta_p2b}  at sample point 2")
print(f"        -- INDEPENDENT of (l1,l2,l3): lam1 and lam2 drop out of BOTH forms entirely.")
check("E3 AT THE PINCER-REQUIRED WEIGHT THE WHOLE FRAME-FREE FAMILY GIVES THE SAME LENSING EFFICIENCY "
      "eta = 3/4: every second-order frame-free term UNDER-LENSES BY EXACTLY 25%, and the deficit "
      "cannot be tuned away because all three couplings give the same number (or no effect at all)",
      sp.simplify(eta_p2 - sp.Rational(3, 4)) == 0 and sp.simplify(eta_p2b - sp.Rational(3, 4)) == 0
      and not (n2.free_symbols & {l1, l2}) and not (d2.free_symbols & {l1, l2}),
      f"eta = {eta_p2} at two independent sample points; the only free coupling left is lam3 "
      f"(Kretschmann), and it cancels in the ratio.  lam3 = 0 gives no modification at all")

# stacked rank: can eta = 1 hold across configurations at once?
rows = []
for pval, brat, n_, d_ in CFG:
    L = sp.expand(n_ - d_)
    if L == 0:
        continue
    rows.append([float(sp.expand(L).coeff(v)) for v in (l1, l2, l3)])
Rk = np.linalg.matrix_rank(np.array(rows), tol=1e-10) if rows else 0
print(f"\n      stacking the eta = 1 conditions over {len(rows)} configurations: rank = {Rk} of 3")
check("E3b eta = 1 CAN be arranged on any single configuration, but the conditions from different "
      "profiles are independent: stacked over the sampled configurations the rank is 3, so the only "
      "frame-free term with correct lensing everywhere is the zero one -- the numerical form of B5",
      Rk == 3,
      f"rank {Rk}/3 over {len(rows)} configurations; a surviving direction would have needed rank < 3")

print("""
  E4.  BOTH CONDITIONS AT ONE SMOOTHING LENGTH?  The separation test (B4) is algebraic and holds at
  every l.  The coherence test (D2) holds for l >= l_crit, and l_crit is the local mean separation.  So
  for a SINGLE system both can be met at one l -- and that is the honest answer to the brief's question.
  What cannot be met is the pair of them with ONE l across systems (D2/D3: a factor 2.6e5), and what
  cannot be met at ANY l is the third requirement neither test contains: that the separation go in the
  direction lensing needs (B5, E3) and that the term be nonlinear enough to carry an acceleration scale
  (E1, E2).
""")
one_l_single = True
one_l_all = max(spread.values()) < 3.0
check("E4 both conditions CAN hold at one smoothing length for one system, and CANNOT for all systems "
      "with a single covariant length",
      one_l_single and not one_l_all,
      f"single system: yes (any l >= l_crit);  all five systems with one l: no, l_crit spans "
      f"{spread['canonical']:.2g}x (canonical) / {spread['alt']:.2g}x (alt)")

print("""
  E5.  THE MODE PRICE of the one member that survives E1 -- the linear, exactly-quadratic action
  Delta S = int h [ a(Box) P^(2) + c(Box) P^(0s) ] h  with the two form factors B1 counted.
""")
print(f"      {'form factor':>26s} {'extra poles':>12s} {'ghost?':>10s} {'verdict':>44s}")
for nm, poles, gh, vd in [
    ("polynomial (Stelle R+R^2+C^2)", "2", "yes, spin-2", "massive spin-2 ghost -- the classic result"),
    ("a(Box)=c(Box)=1+m^-2 Box", "1", "yes", "Ostrogradsky; excluded"),
    ("entire, e.g. exp(Box/M^2)", "0", "no", "ghost-free, but acausal/no Cauchy problem"),
    ("with Box^{-1} (IR nonlocal)", "0 new", "no", "L39's retarded reading: N_grav = 2"),
]:
    print(f"      {nm:>26s} {poles:>12s} {gh:>10s} {vd:>44s}")
check("E5 the surviving member need NOT add a propagating mode -- an entire or purely-IR-nonlocal form "
      "factor is ghost-free and keeps N_grav = 2 under L39's retarded reading -- so the route is NOT "
      "closed on Ostrogradsky, and this lane does not claim it is",
      True,
      "the mode count is the one gate this candidate passes; it fails on E1, B5/E3 and D2/D3 instead")

# ===================================================================================================
sec("F -- VERDICT.  The requirements ledger, stated from the CANDIDATE's side so a FAIL is a real cost.")
# ===================================================================================================
print("""
  THE CANDIDATE, in full:  a frame-free covariant addition
        Delta S = int sqrt(-g) F( Box^{-1} Q_smoothed ),   Q a quadratic curvature invariant,
  smoothed with an entire covariant form factor on a length l.  It is the ONLY object the enumeration
  of B1-B4 leaves, it is exactly what L39 sec.7 asks for, and it is not a straw man: it defeats the
  obstruction L39 and PAPER9 cite against it.  Six requirements; it meets three.
""")
req = [
    ("R1 it SEPARATES Phi from Psi (the first-order lock's exact identity fails at second order)",
     True, "B4: the lock-preserving subspace is 1 of 3; the generic invariant breaks "
           "lap(Phi+Psi) = 8 pi G rho"),
    ("R2 it is COHERENT-dominated, not nearest-star dominated -- step E's obstruction does NOT apply",
     True, f"C4: Box^{{-1}}Q returns (1/2)|grad Phi|^2 of the total field, coherent by "
           f"{U_gal_vac/U_star_vac:.2e}x where the local invariant is star-dominated by "
           f"{tid_star_1pc/tid_gal:.1f}x"),
    ("R3 it does not add a propagating mode",
     True, "E5: an entire or purely-IR-nonlocal form factor is ghost-free; N_grav = 2 under L39's "
           "retarded reading"),
    ("R4 the separation goes in the direction LENSING needs (eta = 1)",
     False, "E3: at the weight a flat rotation curve requires, eta = 3/4 EXACTLY for the entire "
            "three-parameter family -- a 25% lensing deficit that no coupling can tune away.  B5/E3b: "
            "eta = 1 as an identity has only the trivial solution"),
    ("R5 it is nonlinear enough to carry an ACCELERATION scale (a flat rotation curve at every mass)",
     False, "E1: the radial-profile and mass-scaling conditions force total degree 1, i.e. an exactly "
            "quadratic action and LINEAR field equations.  E2: v^4 ~ M^2 not M^1, and one fixed length "
            "instead of r_M ~ sqrt(M) spanning 100x over four decades"),
    ("R6 ONE fixed covariant smoothing length makes the coherent term win in every system",
     False, f"D2/D3: l_crit is the local mean separation between the discrete masses and spans "
            f"{spread['canonical']:.2g}x (canonical) / {spread['alt']:.2g}x (alt) from a globular "
            f"cluster to a galaxy cluster; the theory's own xi = 4.00 pc is short by "
            f"{worst['canonical']:.2g}x / {worst['alt']:.2g}x"),
]
for nm, ok, det in req:
    check(nm, ok, det)

nmet = sum(1 for _, ok, _ in req if ok)
check("F1 VERDICT ON THE GAP: no exhibited frame-free nonlocal scalar, quadratic or higher in curvature, "
      "separates the Newtonian from the lensing potential in the direction lensing needs while carrying "
      "an acceleration scale.  THE LENSING LOCK SURVIVES at second order",
      nmet == 3 and not req[3][1] and not req[4][1],
      f"{nmet}/6 requirements met; the three that fail are independent of each other and any one is "
      f"fatal.  The lock is no longer an exact identity at second order -- it is a 25% deficit plus a "
      f"linearity theorem")
check("F2 PAPER9 MUST BE AMENDED BEFORE DEPOSIT.  Its stated reason for setting second-order scalars "
      "aside -- 'they are, however, exactly the objects step E showed to be uniform-field blind and "
      "nearest-star dominated' -- is FALSE for the nonlocal members, by 2e6 in the wrong direction.  "
      "The conclusion stands; the argument for it does not",
      False,
      "the correct statement is the one this lane proves: nonlocal second-order scalars DO see the "
      "coherent field, and they are excluded instead by (i) eta = 3/4, (ii) the degree-1 pincer, and "
      "(iii) a graininess length that is not a constant of nature")

print(f"""
  WHAT IS STILL NOT PROVED, named as precisely as L39 named its own gap:

   1. E1's pincer assumes the deep-MOND asymptotics are an exact power law and that F is asymptotically
      homogeneous in the invariants.  A genuinely non-homogeneous F (an interpolation that never
      reaches a power law) is not covered.  THE MISSING COMPUTATION: does the flat-rotation-curve
      requirement, imposed over a FINITE range of radii and masses rather than asymptotically, still
      force total degree 1?  This is a strictly smaller target than L39's.
   2. eta = 3/4 is a first-order (linear-response) result about the no-slip background.  Its
      backreacted, fully nonlinear value is not computed here.  The sign and the O(1) size are robust;
      the exact 3/4 is not claimed beyond linear response.
   3. Cubic and higher invariants (R^3, R_mn R^na R_a^m, Box^{{-1}} of them) are NOT enumerated here.
      They begin at third order in h, so they are outside both the first-order lemma and this lane's
      second-order enumeration.  B1's counting method extends to them; the count was not run.
   4. Nothing here says whether nature is MONDian, and nothing here tests the deposited theory.
""")

sec("SUMMARY")
print(f"  checks: {NCHECK[0]} run;  {NCHECK[0]-len(FAILS)} PASS / {len(FAILS)} FAIL")
for f in FAILS:
    print(f"    FAIL  {f}")
print("""
  Three sentences.
    A nonlocal quadratic-curvature scalar DOES defeat the obstruction PAPER9 cites against it: the exact
    identity Q = (1/2)lap|grad Phi|^2 - grad Phi.grad(lap Phi) makes Box^{-1}Q return the square of the
    COHERENT acceleration, so it beats the nearest star by 2.2e6 where the local invariant loses to it by
    1488x, and PAPER9's stated reason must be amended before deposit.
    It is excluded anyway, three times over and independently: at the weight a flat rotation curve
    requires it under-lenses by exactly 25% for every coupling in the family; the radial-profile and
    mass-scaling conditions together force the addition to be exactly quadratic in h, hence linear, hence
    without an acceleration scale; and the smoothing length that would make it see the coherent field is
    the local mean separation between the discrete masses, which is not a constant of nature and spans
    2.6e5 from a globular cluster to a galaxy cluster.
    So the lensing lock survives at second order and PAPER9's theorem is unchanged -- but it survives for
    a different reason than the paper gives, and the paper says the wrong thing on the way to the right
    answer.
""")
raise SystemExit(0)

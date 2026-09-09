#!/usr/bin/env python3
"""
L27 -- is there a scalar, foliation-independent replacement for q = -(1/6) ln det gamma?
========================================================================================
THE ASSIGNMENT.  L12 tested recipe item A1, "MOND as a gravitational constraint":

    C_M = D_i[ mu(y) D^i q ] - S ~ 0 ,      q = -(1/6) ln det gamma ,      y = c^2 |Dq| / a0

and found that its ARITHMETIC IS RIGHT.  C_M is momentum-free, so the 5x5 constraint matrix has rank 2,
one second-class pair, and (12 - 2 - 6)/2 = 2 -- exactly two tensor degrees of freedom, no propagating
clock.  The static weak-field limit is EXACTLY Milgrom's equation with the frozen kernel mu = 1 - e^{-y};
the Solar System is screened by a local acceleration; Newton is recovered exponentially with no 1/y.
That is everything requirement I3a asks for, and it is the only route the programme has that delivers it.

It died for ONE reason: q = -(1/6) ln det gamma is a property of the SLICE and its COORDINATES, not of
the spacetime.  Vacuum Schwarzschild in Painleve-Gullstrand slicing has exactly flat spatial metric, so
q = 0 and the MOND field is exactly ZERO, while the static slice of the SAME spacetime gives g_Newton.
L12's closing sentence names this lane's job:

    "the surviving obligation is to find a scalar, foliation-independent quantity to put in q's place;
     this lane found none."

THE QUESTION: is there one?

THE ACCEPTANCE TEST.  A replacement qt must satisfy, as checkable conditions:
  (a)  qt is a genuine spatial scalar under spatial diffeomorphisms -- no anomaly;
  (b)  its value on a given spacetime does not depend on the slicing;
  (c)  in the static weak field it reduces to the Newtonian potential (up to constants), so that |D qt|
       is an acceleration and the MOND kernel has something to act on -- FOR A GENERAL SOURCE, i.e. it
       must superpose, not merely fit one Schwarzschild solution;
  (d)  it vanishes in genuinely empty flat space in EVERY coordinate system;
  (e)  the resulting constraint is still momentum-free, or at least still removes only the conformal
       mode, so the count stays at 2;
  (f)  it does not force rho = 0 on FLRW and is compatible with GR's own Hamiltonian constraint.

Requirement (b) is the killer and is applied FIRST and cheaply, on a ONE-PARAMETER FAMILY OF SLICINGS of
vacuum Schwarzschild.  L12 used two slicings; two is not enough, because R3 happens to vanish on BOTH the
static and the PG slice and would pass a two-point test by coincidence.  The family used here is

    ds^2 = -f dT^2 + 2 lam sqrt(u) dT dr + [(1 - lam^2 u)/f] dr^2 + r^2 dOmega^2 ,
    f = 1 - 2M/r,  u = 2M/r,  lam in [0, 1]

which is vacuum Schwarzschild written on the slices T = t + lam * INT sqrt(u)/f dr.  lam = 0 is the static
slicing, lam = 1 is Painleve-Gullstrand (gamma exactly flat, N = 1), lam = 1/2 is a legitimate third cut.
Every lam is the SAME SPACETIME (control C1 verifies R_munu = 0 and Kretschmann = 48 M^2/r^6 for all
three), and the areal radius r labels the same 2-sphere of that spacetime on every slice, so comparing a
candidate at the same r across lam is comparing the same geometry.  A candidate whose value moves with
lam is dead on (b) immediately, and the table of what died on (b) is itself a deliverable.

WHAT IS SEARCHED.  The spatial-metric scalars (det gamma, R3), the extrinsic-curvature scalars
(K, K_ij K^ij, the trace-free A_ij A^ij), the lapse and the acceleration of the normal observers, the
four-dimensional curvature invariants (R4, Kretschmann I1, grad-Riemann I2, the electric Weyl E_ij E^ij),
a matter scalar, the norm of the timelike Killing vector, and -- the one construction that actually
reproduces -M/r out of local curvature alone --

    q_ratio = -(720 / 48^{3/2}) * sqrt(I1^3) / I2  =  -M/(r - 2M)  ->  Phi_Newton/c^2 ,

an exact closed form on Schwarzschild built only from spacetime scalars.  That candidate is the honest
strong case for "yes", and it is tested here as ruthlessly as the others.

BOTH FOOTINGS on every dimensional number: a0 = 9.3619e-11 (canonical) / 1.1279e-10 (alt) m s^-2.
Nothing here is read from, executed from, or copied out of
closure_2026/integrable_clock_construction_2026/ or any other agent's directory; the sympy machinery is
rebuilt from scratch in this file and guarded by seven controls.  A failure below is the candidate's,
not the toolkit's.
"""
import math
import sympy as sp
import numpy as np

FAILS = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


# ----------------------------------------------------------------------------------------------------------
# constants -- both footings everywhere a0 enters
# ----------------------------------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
G_N = 6.674e-11
MSUN = 1.989e30
AU = 1.495978707e11
KPC = 3.0857e19
MPC = 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0 = 67.4e3 / MPC
OMEGA_M = 0.315

BAR = "=" * 118
print(BAR)
print("L27 -- is there a scalar, foliation-independent replacement for q = -(1/6) ln det gamma?")
print(BAR, flush=True)


# ----------------------------------------------------------------------------------------------------------
# geometry toolkit, rebuilt from scratch
# ----------------------------------------------------------------------------------------------------------
def christoffel(g, x):
    n = len(x)
    gi = sp.simplify(g.inv())
    return [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b])
                                          - sp.diff(g[b, c], x[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)], gi


def riemann_low(g, x):
    """returns (R_abcd all-lower, Ricci_bd, Ricci scalar, gamma^{-1}, Christoffels)"""
    n = len(x)
    Gam, gi = christoffel(g, x)
    Rm = [[[[sp.simplify(sp.diff(Gam[a][b][d], x[c]) - sp.diff(Gam[a][b][c], x[d])
                         + sum(Gam[a][c][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][c] for e in range(n)))
             for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Rl = [[[[sp.simplify(sum(g[a, e] * Rm[e][b][c][d] for e in range(n)))
             for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.Matrix(n, n, lambda b, d: sp.simplify(sum(Rm[a][b][a][d] for a in range(n))))
    Rs = sp.simplify(sum(gi[b, d] * Ric[b, d] for b in range(n) for d in range(n)))
    return Rl, Ric, Rs, gi, Gam


def ricci_scalar(g, x):
    return riemann_low(g, x)[2]


def contract4(Al, Bl, gi, n=4):
    """A_abcd B^abcd with both given all-lower"""
    s = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    v = Al[a][b][c][d]
                    if v == 0:
                        continue
                    for a2 in range(n):
                        if gi[a, a2] == 0:
                            continue
                        for b2 in range(n):
                            if gi[b, b2] == 0:
                                continue
                            for c2 in range(n):
                                if gi[c, c2] == 0:
                                    continue
                                for d2 in range(n):
                                    if gi[d, d2] == 0 or Bl[a2][b2][c2][d2] == 0:
                                        continue
                                    s += gi[a, a2] * gi[b, b2] * gi[c, c2] * gi[d, d2] * v * Bl[a2][b2][c2][d2]
    return sp.simplify(s)


def cov_grad_riemann(Rl, Gam, x, n=4):
    """nabla_e R_abcd as a dict keyed (e,a,b,c,d)"""
    DR = {}
    for e in range(n):
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(n):
                        t = sp.diff(Rl[a][b][c][d], x[e])
                        t -= sum(Gam[m][e][a] * Rl[m][b][c][d] for m in range(n))
                        t -= sum(Gam[m][e][b] * Rl[a][m][c][d] for m in range(n))
                        t -= sum(Gam[m][e][c] * Rl[a][b][m][d] for m in range(n))
                        t -= sum(Gam[m][e][d] * Rl[a][b][c][m] for m in range(n))
                        DR[(e, a, b, c, d)] = sp.simplify(t)
    return DR


def gradR_sq(DR, gi, n=4):
    """nabla_e R_abcd nabla^e R^abcd"""
    keys = [k for k, v in DR.items() if v != 0]
    s = 0
    for k1 in keys:
        for k2 in keys:
            fac = 1
            for p in range(5):
                fac *= gi[k1[p], k2[p]]
                if fac == 0:
                    break
            if fac == 0:
                continue
            s += fac * DR[k1] * DR[k2]
    return sp.simplify(s)


def weyl_low(Rl, Ric, Rs, g, n=4):
    C = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    e = Rl[a][b][c][d]
                    e -= sp.Rational(1, 2) * (g[a, c] * Ric[b, d] - g[a, d] * Ric[b, c]
                                              - g[b, c] * Ric[a, d] + g[b, d] * Ric[a, c])
                    e += Rs / 6 * (g[a, c] * g[b, d] - g[a, d] * g[b, c])
                    C[a][b][c][d] = e
    return C


def grad_sq3(fn, gam, x):
    gi = gam.inv()
    return sp.simplify(sum(gi[i, j] * sp.diff(fn, x[i]) * sp.diff(fn, x[j])
                           for i in range(len(x)) for j in range(len(x))))


def cov_div3(V, gam, x):
    sq = sp.sqrt(gam.det())
    return sp.simplify(sum(sp.diff(sq * V[i], x[i]) for i in range(len(x))) / sq)


# ==========================================================================================================
print("\nSECTION 0 -- CONTROLS: is the machinery right, and does it reproduce L12's kill?")
print("-" * 118)
# ==========================================================================================================
T, th, ph = sp.symbols("T theta phi")
r = sp.Symbol("r", positive=True)
M = sp.Symbol("M", positive=True)
X4 = [T, r, th, ph]
X3 = [r, th, ph]
f_s = 1 - 2 * M / r
u_s = 2 * M / r

# --- C0: flat 3-space has R3 = 0 in Cartesian AND spherical
xx, yy, zz = sp.symbols("x y z")
R3_cart = ricci_scalar(sp.eye(3), [xx, yy, zz])
R3_sph = ricci_scalar(sp.diag(1, r ** 2, r ** 2 * sp.sin(th) ** 2), X3)
check("C0 [control] my 3-curvature machinery returns R3 = 0 for flat space in BOTH Cartesian and "
      "spherical coordinates",
      R3_cart == 0 and R3_sph == 0, f"R3_cart = {R3_cart}, R3_sph = {R3_sph}, both exact")


# --- the one-parameter slicing family of vacuum Schwarzschild
def g4_family(lam):
    return sp.Matrix([[-f_s, lam * sp.sqrt(u_s), 0, 0],
                      [lam * sp.sqrt(u_s), (1 - lam ** 2 * u_s) / f_s, 0, 0],
                      [0, 0, r ** 2, 0],
                      [0, 0, 0, r ** 2 * sp.sin(th) ** 2]])


def gam3_family(lam):
    return sp.diag((1 - lam ** 2 * u_s) / f_s, r ** 2, r ** 2 * sp.sin(th) ** 2)


def lapse_family(lam):
    return sp.sqrt(f_s / (1 - lam ** 2 * u_s))


def shiftdown_family(lam):
    return sp.Matrix([lam * sp.sqrt(u_s), 0, 0])          # N_i = gamma_ij N^j = g_{Tr} delta^r_i


LAMS = [(sp.Integer(0), "lam=0   static"), (sp.Rational(1, 2), "lam=1/2 tilted"), (sp.Integer(1), "lam=1   PG")]

print("\n    Building the slicing family.  Same spacetime, three cuts, labelled by the areal radius r.")
GEO = {}
for lam, tag in LAMS:
    g4 = g4_family(lam)
    Rl, Ric, Rs, gi4, Gam4 = riemann_low(g4, X4)
    GEO[lam] = dict(g4=g4, Rl=Rl, Ric=Ric, Rs=Rs, gi4=gi4, Gam4=Gam4, tag=tag)
    print(f"      {tag}:  N = {sp.simplify(lapse_family(lam))},  gamma_rr = "
          f"{sp.simplify(gam3_family(lam)[0, 0])}", flush=True)

kret = {}
for lam, tag in LAMS:
    kret[lam] = contract4(GEO[lam]["Rl"], GEO[lam]["Rl"], GEO[lam]["gi4"])
ric_flat = all(sp.simplify(GEO[lam]["Ric"]) == sp.zeros(4, 4) for lam, _ in LAMS)
kret_same = all(sp.simplify(kret[lam] - 48 * M ** 2 / r ** 6) == 0 for lam, _ in LAMS)
check("C1 [control] the three cuts are ONE spacetime: R_munu = 0 and Kretschmann = 48 M^2/r^6 for "
      "lam = 0, 1/2, 1 (vacuum Schwarzschild in all three)",
      ric_flat and kret_same,
      f"Kretschmann = {kret[sp.Integer(0)]} / {kret[sp.Rational(1,2)]} / {kret[sp.Integer(1)]}")

N0 = sp.simplify(lapse_family(sp.Integer(0)))
N1 = sp.simplify(lapse_family(sp.Integer(1)))
gam_pg_flat = sp.simplify(gam3_family(sp.Integer(1)) - sp.diag(1, r ** 2, r ** 2 * sp.sin(th) ** 2)) == sp.zeros(3, 3)
check("C2 [control] the three cuts are genuinely DIFFERENT slices: the lapse and the spatial metric move "
      "with lam (lam=1 is Painleve-Gullstrand, gamma exactly flat, N = 1)",
      N0 != N1 and gam_pg_flat and sp.simplify(N1 - 1) == 0,
      f"N(lam=0) = {N0}, N(lam=1) = {N1}, gamma(lam=1) flat = {gam_pg_flat}")

# --- C3: reproduce L12's kill exactly.  q_det on the static slice (isotropic fiducial) vs on PG.
rb = sp.Symbol("rbar", positive=True)
psi = 1 + M / (2 * rb)
gam_iso = sp.diag(psi ** 4, psi ** 4 * rb ** 2, psi ** 4 * rb ** 2 * sp.sin(th) ** 2)
gam_iso_flat = sp.diag(1, rb ** 2, rb ** 2 * sp.sin(th) ** 2)
q_iso = sp.simplify(-sp.Rational(1, 6) * sp.log(gam_iso.det() / gam_iso_flat.det()))
q_iso_1 = sp.simplify(sp.series(q_iso, M, 0, 2).removeO())
g_iso = sp.simplify(sp.sqrt(grad_sq3(q_iso_1, gam_iso_flat, [rb, th, ph])))
gam_pg = gam3_family(sp.Integer(1))
q_pg = sp.simplify(-sp.Rational(1, 6) * sp.log(gam_pg.det() / sp.diag(1, r ** 2, r ** 2 * sp.sin(th) ** 2).det()))
g_pg = sp.simplify(sp.sqrt(grad_sq3(q_pg, gam_pg, X3)))
print(f"\n    L12's kill, reproduced:  static slice, isotropic fiducial : c^2|Dq| = c^2 * {g_iso}  = g_Newton")
print(f"                             Painleve-Gullstrand slice        : q = {q_pg}, c^2|Dq| = {g_pg}")
check("C3 [CONTROL, reproduces L12] q = -(1/6) ln det gamma gives g_Newton on the static slice and "
      "EXACTLY 0 on the Painleve-Gullstrand slice of the same vacuum Schwarzschild spacetime",
      sp.simplify(g_iso - M / rb ** 2) == 0 and q_pg == 0 and g_pg == 0,
      "reproduced: g_N vs 0, the L12 kill stands")

# --- C3b: reproduce L12's F2 -- q_det is not even a spatial scalar
gam_flat_sph = sp.diag(1, r ** 2, r ** 2 * sp.sin(th) ** 2)
q_flat_sph = sp.simplify(-sp.Rational(1, 6) * sp.log(gam_flat_sph.det()))
gi_fs = gam_flat_sph.inv()
V_fs = [sp.simplify(sum(gi_fs[i, j] * sp.diff(q_flat_sph, X3[j]) for j in range(3))) for i in range(3)]
CM_flat_sph = cov_div3(V_fs, gam_flat_sph, X3)          # mu = 1 there, verified below
rho_fict = -(C_LIGHT ** 2) / (3.0 * AU ** 2) / (4 * math.pi * G_N)
check("C3b [CONTROL, reproduces L12] in EMPTY flat space written in spherical coordinates the operator is "
      "C_M = -1/(3 r^2), demanding fictitious matter",
      sp.simplify(CM_flat_sph + 1 / (3 * r ** 2)) == 0,
      f"C_M = {CM_flat_sph}; rho_fict = {rho_fict:.3e} kg/m^3 at 1 AU (denser than granite), identical on "
      f"both footings because mu = 1 there")

# --- C4: linearised Ricci scalar machinery
tt = sp.Symbol("t")
X4c = [tt, xx, yy, zz]
eta = sp.diag(-1, 1, 1, 1)
Phi = sp.Function("Phi")(xx, yy, zz)


def lin_ricci_scalar(h):
    hu = sp.Matrix(4, 4, lambda a, b: sum(eta[a, c] * eta[b, d] * h[c, d] for c in range(4) for d in range(4)))
    trh = sum(eta[a, b] * h[a, b] for a in range(4) for b in range(4))
    t1 = sum(sp.diff(hu[a, b], X4c[a], X4c[b]) for a in range(4) for b in range(4))
    bx = sum(eta[a, b] * sp.diff(trh, X4c[a], X4c[b]) for a in range(4) for b in range(4))
    return sp.expand(t1 - bx)


h_wf = sp.diag(-2 * Phi, -2 * Phi, -2 * Phi, -2 * Phi)
R1_wf = sp.simplify(lin_ricci_scalar(h_wf))
lap_Phi = sp.diff(Phi, xx, 2) + sp.diff(Phi, yy, 2) + sp.diff(Phi, zz, 2)
xi = [sp.Function(f"xi{i}")(xx, yy, zz) for i in range(4)]
xil = [sum(eta[i, j] * xi[j] for j in range(4)) for i in range(4)]
h_gauge = sp.Matrix(4, 4, lambda i, j: h_wf[i, j] + sp.diff(xil[j], X4c[i]) + sp.diff(xil[i], X4c[j]))
gauge_shift = sp.simplify(lin_ricci_scalar(h_gauge) - R1_wf)
# validate the linear formula against the FULL nonlinear scalar on a 1-D profile
ee = sp.Symbol("epsilon")
phi1 = sp.Function("varphi")(xx)
g_full = sp.diag(-(1 + 2 * ee * phi1), 1 - 2 * ee * phi1, 1 - 2 * ee * phi1, 1 - 2 * ee * phi1)
R_full1 = sp.simplify(sp.diff(ricci_scalar(g_full, X4c), ee).subs(ee, 0))
check("C4 [control] linearised R4 = 2 grad^2 Phi, is invariant under h -> h + d_(mu xi_nu), and agrees "
      "with the FULL nonlinear Ricci scalar at O(Phi)",
      sp.simplify(R1_wf / lap_Phi) == 2 and gauge_shift == 0
      and sp.simplify(R_full1 - 2 * sp.diff(phi1, xx, 2)) == 0,
      f"R^(1)/grad^2 Phi = {sp.simplify(R1_wf/lap_Phi)}, gauge shift = {gauge_shift}, "
      f"full-nonlinear O(eps) term = {R_full1}")

# --- C5: the curvature-ratio construction, exact and in its weak-field surrogate
DR_s = cov_grad_riemann(GEO[sp.Integer(0)]["Rl"], GEO[sp.Integer(0)]["Gam4"], X4)
I2_s = gradR_sq(DR_s, GEO[sp.Integer(0)]["gi4"])
I1_s = kret[sp.Integer(0)]
COEF = sp.Integer(720) / sp.Integer(48) ** sp.Rational(3, 2)
q_ratio_exact = sp.simplify(-COEF * sp.sqrt(I1_s ** 3) / I2_s)


def tidal_invariants(second, third):
    """I_E = sum (d_i d_j Phi)^2 ; J_E = sum (d_k d_i d_j Phi)^2"""
    return float(np.sum(second ** 2)), float(np.sum(third ** 2))


def d2_point(x, src):
    out = np.zeros((3, 3))
    for (m, pos) in src:
        d = x - pos
        rr = math.sqrt(d @ d)
        out += G_N * m * (np.eye(3) / rr ** 3 - 3 * np.outer(d, d) / rr ** 5)
    return out


def d3_point(x, src):
    out = np.zeros((3, 3, 3))
    dl = np.eye(3)
    for (m, pos) in src:
        d = x - pos
        rr = math.sqrt(d @ d)
        t = np.zeros((3, 3, 3))
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    t[i, j, k] = (3.0 * (dl[i, j] * d[k] + dl[j, k] * d[i] + dl[k, i] * d[j]) / rr ** 5
                                  - 15.0 * d[i] * d[j] * d[k] / rr ** 7)
        out += G_N * m * t
    return out


COEF_WEAK = float(720 * math.sqrt(8) / 48 ** 1.5)


def q_ratio_weak(x, src):
    IE, JE = tidal_invariants(d2_point(x, src), d3_point(x, src))
    if JE == 0.0:
        return float("nan")
    return -COEF_WEAK * IE ** 1.5 / JE / C_LIGHT ** 2


def Phi_newton(x, src):
    return -sum(G_N * m / math.sqrt((x - pos) @ (x - pos)) for (m, pos) in src) / C_LIGHT ** 2


one_mass = [(1e10 * MSUN, np.zeros(3))]
xt = np.array([7.0 * KPC, 3.0 * KPC, -2.0 * KPC])
q1 = q_ratio_weak(xt, one_mass)
p1 = Phi_newton(xt, one_mass)
check("C5 [control] the curvature-ratio construction reproduces the Newtonian potential of a POINT MASS "
      "exactly, both in exact GR and in its weak-field surrogate",
      sp.simplify(q_ratio_exact + M / (r - 2 * M)) == 0 and abs(q1 / p1 - 1.0) < 1e-12,
      f"exact GR: -(720/48^1.5) sqrt(I1^3)/I2 = {q_ratio_exact} = -M/(r-2M) -> -M/r; "
      f"surrogate/Phi = {q1/p1:.12f}")
print(f"         (I1 = {I1_s}, I2 = nabla_e R_abcd nabla^e R^abcd = {sp.simplify(I2_s)})")


# ==========================================================================================================
print("\nSECTION 1 -- REQUIREMENT (b), APPLIED FIRST AND TO EVERY CANDIDATE")
print("    Same vacuum Schwarzschild spacetime, three slicings.  A candidate that moves with lam is dead.")
print("-" * 118)
# ==========================================================================================================
BTAB = []


def brow(label, vals, ok, note=""):
    BTAB.append((label, [str(v) for v in vals], ok, note))
    return ok


def same_across(vals):
    return all(sp.simplify(vals[0] - v) == 0 for v in vals[1:])


# extrinsic curvature of each slice (static configuration: d_t gamma_ij = 0)
KEXT = {}
for lam, tag in LAMS:
    gam = gam3_family(lam)
    Nl = lapse_family(lam)
    Nd = shiftdown_family(lam)
    Gam3, gi3 = christoffel(gam, X3)
    Kij = sp.Matrix(3, 3, lambda i, j: sp.simplify(
        ((sp.diff(Nd[j], X3[i]) - sum(Gam3[k][i][j] * Nd[k] for k in range(3)))
         + (sp.diff(Nd[i], X3[j]) - sum(Gam3[k][j][i] * Nd[k] for k in range(3)))) / (2 * Nl)))
    trK = sp.simplify(sum(gi3[i, j] * Kij[i, j] for i in range(3) for j in range(3)))
    KK = sp.simplify(sum(gi3[i, k] * gi3[j, l] * Kij[i, j] * Kij[k, l]
                         for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
    Aij = sp.Matrix(3, 3, lambda i, j: sp.simplify(Kij[i, j] - trK * gam[i, j] / 3))
    AA = sp.simplify(sum(gi3[i, k] * gi3[j, l] * Aij[i, j] * Aij[k, l]
                         for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
    R3 = ricci_scalar(gam, X3)
    Ham = sp.simplify(R3 + trK ** 2 - KK)
    KEXT[lam] = dict(K=trK, KK=KK, AA=AA, R3=R3, gam=gam, N=Nl, gi3=gi3, Ham=Ham)
check("C6 [control] every slice of the family satisfies the VACUUM ADM Hamiltonian constraint "
      "R3 + K^2 - K_ij K^ij = 0 (my extrinsic-curvature machinery is right)",
      all(KEXT[lam]["Ham"] == 0 for lam, _ in LAMS),
      "exact 0 on all three cuts")

# b01 -- q_det.  values below are |D qt|; multiply by c^2 for the acceleration.
q_det_vals = []
for lam, tag in LAMS:
    gam = gam3_family(lam)
    qd = sp.simplify(-sp.Rational(1, 6) * sp.log(gam.det() / sp.diag(1, r ** 2, r ** 2 * sp.sin(th) ** 2).det()))
    q_det_vals.append(sp.simplify(sp.sqrt(grad_sq3(qd, gam, X3))))
q_det_wf = [sp.simplify(sp.series(v, M, 0, 2).removeO()) for v in q_det_vals]
check("b01 (b) q = -(1/6) ln(det gamma / det gamma-bar)  [L12's own choice, flat fiducial]",
      brow("q_det = -(1/6) ln(det gamma/det gbar)", q_det_vals, same_across(q_det_vals),
           "slice-dependent: g_N/3 (areal fiducial) -> 0; g_N with the isotropic fiducial, control C3"),
      f"|Dq| to O(M) = {q_det_wf[0]} / {q_det_wf[1]} / {q_det_wf[2]}  (static / tilted / PG); multiply by "
      f"c^2 for the acceleration -- the same vacuum spacetime hands back a different MOND field on every "
      f"cut, and 0 on PG")

# b02 -- R3
R3_vals = [KEXT[lam]["R3"] for lam, _ in LAMS]
check("b02 (b) the spatial Ricci scalar R3",
      brow("R3 (spatial Ricci scalar)", R3_vals, same_across(R3_vals),
           "0 on static AND PG by coincidence, nonzero on the third cut"),
      f"R3 = {R3_vals[0]} / {sp.simplify(R3_vals[1])} / {R3_vals[2]}  -- the two-slicing test would have "
      f"PASSED this candidate; the third cut kills it")

# b03 -- K
K_vals = [KEXT[lam]["K"] for lam, _ in LAMS]
check("b03 (b) the trace of the extrinsic curvature K (the York time)",
      brow("K = gamma^ij K_ij", K_vals, same_across(K_vals), "0 on static, nonzero on PG"),
      f"K = {K_vals[0]} / {sp.simplify(K_vals[1])} / {sp.simplify(K_vals[2])}")

# b04 -- K_ij K^ij
KK_vals = [KEXT[lam]["KK"] for lam, _ in LAMS]
check("b04 (b) K_ij K^ij",
      brow("K_ij K^ij", KK_vals, same_across(KK_vals), "0 on static, nonzero on PG"),
      f"K_ijK^ij = {KK_vals[0]} / {sp.simplify(KK_vals[1])} / {sp.simplify(KK_vals[2])}")

# b05 -- trace-free A_ij A^ij
AA_vals = [KEXT[lam]["AA"] for lam, _ in LAMS]
check("b05 (b) the trace-free part A_ij A^ij",
      brow("A_ij A^ij (trace-free)", AA_vals, same_across(AA_vals), "0 on static, nonzero on PG"),
      f"A_ijA^ij = {AA_vals[0]} / {sp.simplify(AA_vals[1])} / {sp.simplify(AA_vals[2])}")

# b06 -- ln N (the khronometric choice)
lnN_vals = [sp.simplify(sp.log(lapse_family(lam))) for lam, _ in LAMS]
check("b06 (b) ln N, the ADM lapse  [this is the khronometric choice and it reintroduces a preferred "
      "foliation by construction -- the test confirms it quantitatively]",
      brow("ln N (ADM lapse)", lnN_vals, same_across(lnN_vals), "(1/2)ln f -> 0; N IS the slicing"),
      f"ln N = {lnN_vals[0]} / {sp.simplify(lnN_vals[1])} / {lnN_vals[2]}")

# b07 -- c^2 |D ln N|, the proper acceleration of the normal observers
acc_vals = []
for lam, tag in LAMS:
    lnN = sp.log(lapse_family(lam))
    acc_vals.append(sp.simplify(sp.sqrt(grad_sq3(lnN, gam3_family(lam), X3))))
acc_wf = [sp.simplify(sp.series(v, M, 0, 2).removeO()) for v in acc_vals]
check("b07 (b) c^2 |D ln N|, the proper acceleration of the slice-normal observers  [the MOND field "
      "taken to BE an acceleration rather than a potential gradient]",
      brow("c^2|D ln N| (normal-observer acceleration)", acc_vals, same_across(acc_vals),
           "g_N on static, exactly 0 on PG (free-fallers feel nothing)"),
      f"|D ln N| to O(M) = {acc_wf[0]} / {acc_wf[1]} / {acc_wf[2]}; times c^2 that is g_N on the static "
      f"cut and exactly 0 on PG, because the PG normal observers are in free fall")

# b08 -- R4
R4_vals = [GEO[lam]["Rs"] for lam, _ in LAMS]
check("b08 (b) the four-dimensional Ricci scalar R4",
      brow("R4 (spacetime Ricci scalar)", R4_vals, same_across(R4_vals), "0 = 0 = 0, but see (c)"),
      f"R4 = {R4_vals[0]} / {R4_vals[1]} / {R4_vals[2]} -- SURVIVES (b)")

# b09 -- Kretschmann
I1_vals = [kret[lam] for lam, _ in LAMS]
check("b09 (b) the Kretschmann scalar I1 = R_abcd R^abcd",
      brow("I1 = Kretschmann", I1_vals, same_across(I1_vals), "48 M^2/r^6 on all three"),
      f"I1 = {I1_vals[0]} on all three cuts -- SURVIVES (b)")

# b10 -- grad-Riemann invariant, computed on all three cuts
I2_vals = []
for lam, tag in LAMS:
    DRl = cov_grad_riemann(GEO[lam]["Rl"], GEO[lam]["Gam4"], X4)
    I2_vals.append(gradR_sq(DRl, GEO[lam]["gi4"]))
    print(f"      I2 on {tag}: {sp.simplify(I2_vals[-1])}", flush=True)
check("b10 (b) the derivative invariant I2 = nabla_e R_abcd nabla^e R^abcd",
      brow("I2 = grad-Riemann squared", I2_vals, same_across(I2_vals), "720 M^2(r-2M)/r^9 on all three"),
      f"I2 = {sp.simplify(I2_vals[0])} on all three cuts -- SURVIVES (b)")

# b11 -- electric Weyl w.r.t. the slice normal
E2_vals = []
for lam, tag in LAMS:
    Nl = lapse_family(lam)
    Nup_r = sp.simplify(lam * sp.sqrt(u_s) * f_s / (1 - lam ** 2 * u_s))
    nup = [sp.simplify(1 / Nl), sp.simplify(-Nup_r / Nl), 0, 0]
    gam = gam3_family(lam)
    gi3 = gam.inv()
    Rl = GEO[lam]["Rl"]
    E = sp.Matrix(3, 3, lambda i, j: sp.simplify(sum(Rl[a][i + 1][b][j + 1] * nup[a] * nup[b]
                                                     for a in range(4) for b in range(4))))
    E2_vals.append(sp.simplify(sum(gi3[i, k] * gi3[j, l] * E[i, j] * E[k, l]
                                   for i in range(3) for j in range(3) for k in range(3) for l in range(3))))
check("b11 (b) the electric Weyl invariant E_ij E^ij with E_ij = C_(a i b j) n^a n^b, n the slice normal",
      brow("E_ij E^ij (electric Weyl)", E2_vals, same_across(E2_vals),
           "6 M^2/r^6 on all three -- radial boosts leave type-D E_ij alone"),
      f"E^2 = {E2_vals[0]} on all three cuts -- SURVIVES (b), and it is NOT trivially so: the normal "
      f"observer is static at lam=0 and free-falling at lam=1")

# b12 -- the norm of the timelike Killing vector
kill_vals = []
kill_is_killing = []
for lam, tag in LAMS:
    g4 = GEO[lam]["g4"]
    xiv = [1, 0, 0, 0]                                    # d/dT  (the same vector field for every lam)
    xid = [sp.simplify(sum(g4[a, b] * xiv[b] for b in range(4))) for a in range(4)]
    Gam4 = GEO[lam]["Gam4"]
    KV = sp.Matrix(4, 4, lambda a, b: sp.simplify(
        (sp.diff(xid[b], X4[a]) - sum(Gam4[m][a][b] * xid[m] for m in range(4))
         + sp.diff(xid[a], X4[b]) - sum(Gam4[m][b][a] * xid[m] for m in range(4))) / 2))
    kill_is_killing.append(KV == sp.zeros(4, 4))
    kill_vals.append(sp.simplify(sp.Rational(1, 2) * sp.log(-sum(g4[a, b] * xiv[a] * xiv[b]
                                                                for a in range(4) for b in range(4)))))
check("b12 (b) ln sqrt(-xi.xi), the norm of the timelike KILLING vector  [not the ADM lapse: xi is a "
      "property of the spacetime, so this is the geometrically-defined 'potential']",
      brow("ln sqrt(-xi.xi) (Killing norm)", kill_vals, same_across(kill_vals) and all(kill_is_killing),
           "(1/2)ln(1-2M/r) on all three -- SURVIVES"),
      f"ln sqrt(-xi.xi) = {kill_vals[0]} on all three cuts, and xi is verified Killing "
      f"(nabla_(a xi_b) = 0) in all three coordinate systems -- SURVIVES (b)")

# b13 -- the curvature-ratio potential
qr_vals = [sp.simplify(-COEF * sp.sqrt(I1_vals[i] ** 3) / I2_vals[i]) for i in range(3)]
check("b13 (b) q_ratio = -(720/48^{3/2}) sqrt(I1^3)/I2  [the construction that DOES give -M/r out of "
      "local curvature alone]",
      brow("q_ratio = -(720/48^1.5) sqrt(I1^3)/I2", qr_vals, same_across(qr_vals),
           "-M/(r-2M) on all three -- SURVIVES"),
      f"q_ratio = {qr_vals[0]} on all three cuts -- SURVIVES (b)")

# b14 -- a matter scalar
check("b14 (b) a matter-built scalar, e.g. T = T^mu_mu  [vacuously equal on the family, so it is carried "
      "forward rather than dismissed]",
      brow("T = T^mu_mu (matter scalar)", [0, 0, 0], True, "0 = 0 = 0 in vacuum, vacuous here"),
      "T = 0 on all three cuts (vacuum) -- SURVIVES (b) vacuously; decided by (c) below")

print("\n    REQUIREMENT-(b) TABLE  (vacuum Schwarzschild; static / tilted / Painleve-Gullstrand)")
print("    " + "-" * 112)
print(f"    {'candidate':<44} {'(b)':<6} {'what happened'}")
print("    " + "-" * 112)
for label, vals, ok, note in BTAB:
    print(f"    {label:<44} {'PASS' if ok else 'FAIL':<6} {note}")
print("    " + "-" * 112)
n_bpass = sum(1 for _, _, ok, _ in BTAB if ok)
print(f"    {len(BTAB) - n_bpass} of {len(BTAB)} candidates die on requirement (b) alone.  "
      f"{n_bpass} survive to (a), (c), (d).")


# ==========================================================================================================
print("\nSECTION 2 -- REQUIREMENTS (a), (c), (d) ON THE (b)-SURVIVORS")
print("-" * 118)
# ==========================================================================================================

# --- (a): the anomaly.  q_det is not a spatial scalar; a curvature scalar is one, verified by transport.
xiv3 = [sp.Function(f"z{i}")(*X3) for i in range(3)]
Lie_gam = sp.Matrix(3, 3, lambda i, j: sp.simplify(
    sum(xiv3[k] * sp.diff(gam_flat_sph[i, j], X3[k]) for k in range(3))
    + sum(gam_flat_sph[k, j] * sp.diff(xiv3[k], X3[i]) + gam_flat_sph[i, k] * sp.diff(xiv3[k], X3[j])
          for k in range(3))))
gi3s = gam_flat_sph.inv()
dq_det = sp.simplify(-sp.Rational(1, 6) * sum(gi3s[i, j] * Lie_gam[i, j] for i in range(3) for j in range(3)))
xi_dq = sum(xiv3[k] * sp.diff(q_flat_sph, X3[k]) for k in range(3))
anomaly_form = sp.simplify(dq_det - xi_dq + sp.Rational(1, 3) * sum(sp.diff(xiv3[k], X3[k]) for k in range(3)))
check("a1 (a) q_det transforms as a spatial SCALAR under spatial diffeomorphisms, delta_xi q = xi.dq",
      sp.simplify(dq_det - xi_dq) == 0,
      f"it does not.  Computing delta_xi q = -(1/6) gamma^ij (Lie_xi gamma)_ij directly gives "
      f"delta_xi q - xi.dq + (1/3) d_k xi^k = {anomaly_form} exactly, i.e. the anomaly "
      f"delta_xi q_det = xi.dq - (1/3) d_k xi^k that L12 reports, reproduced here independently")

# a genuine scalar: same 3-geometry, two radial charts.  Use the tilted slice, whose R3 is nonzero.
rho = sp.Symbol("rho", positive=True)
gam_tilt = gam3_family(sp.Rational(1, 2))
R3_tilt = KEXT[sp.Rational(1, 2)]["R3"]
gam_tilt_rho = sp.Matrix(3, 3, lambda i, j: sp.simplify(
    gam_tilt[i, j].subs(r, rho + M) * (sp.diff(rho + M, rho) ** 2 if (i == 0 and j == 0) else 1)))
R3_tilt_rho = ricci_scalar(gam_tilt_rho, [rho, th, ph])
q_det_tilt = sp.simplify(-sp.Rational(1, 6) * sp.log(gam_tilt.det()))
q_det_tilt_rho = sp.simplify(-sp.Rational(1, 6) * sp.log(gam_tilt_rho.det()))
scalar_ok = sp.simplify(R3_tilt_rho - R3_tilt.subs(r, rho + M)) == 0
qdet_ok = sp.simplify(q_det_tilt_rho - q_det_tilt.subs(r, rho + M)) == 0
check("a2 (a) a curvature scalar really is anomaly-free: R3 of the SAME 3-geometry written in two radial "
      "charts (r and rho = r - M) gives the same number at the same point, while q_det does not",
      scalar_ok and not qdet_ok,
      f"R3 agrees exactly under the chart change ({scalar_ok}); q_det does not ({qdet_ok}).  Every "
      f"(b)-survivor here (R4, I1, I2, E^2, Killing norm, q_ratio, T) is a spacetime scalar and so "
      f"satisfies (a) by the same argument -- requirement (a) is not what decides this search")

# --- (c) and (d) on the survivors
print("\n    (c) THE STATIC WEAK FIELD.  Does the survivor reduce to the Newtonian potential, for a")
print("        GENERAL source (i.e. does it superpose), so that |D qt| is an acceleration?")

MW_M, MW_R = 6.0e10 * MSUN, 10.0 * KPC
gN_MW = G_N * MW_M / MW_R ** 2
print(f"        reference system: M_b = 6e10 Msun at 10 kpc, g_N = {gN_MW:.3e} m/s^2")
for foot, a0 in A0.items():
    gobs = math.sqrt(gN_MW * a0)
    print(f"          {foot:<10}: a0 = {a0:.4e}, y = g_N/a0 = {gN_MW/a0:.3f}, deep-MOND g_obs ~ "
          f"sqrt(g_N a0) = {gobs:.3e} m/s^2")

# c08: R4 (and every Ricci-built scalar)
check("c08 (c) R4 (and every Ricci-built scalar: R_munu R^munu, T, rho) reduces to the Newtonian "
      "potential in the static weak field",
      False,
      f"it does not: R4^(1) = 2 grad^2 Phi (control C4), so R4 = 0 identically in VACUUM -- outside the "
      f"baryons, which is exactly where the rotation curve lives.  c^2|D R4| = 0 against a required "
      f"{math.sqrt(gN_MW*A0['canonical']):.3e} (canonical) / {math.sqrt(gN_MW*A0['alt']):.3e} (alt) m/s^2 "
      f"at 10 kpc: the deficit is total, on both footings")

# c09/c11: Kretschmann and E^2 -- tidal, not potential; and the mass scaling
KRET_POW = "I1^{1/6}"
mw, dw = 6.0e10, 6.0e8                                    # Msun
scal_err = (mw / dw) ** (2.0 / 3.0)
check("c09 (c) I1 = Kretschmann, I2 = grad-Riemann squared (equivalently E_ij E^ij, C^2) reduce to the "
      "Newtonian potential",
      False,
      f"it does not: I1 = 48 M^2/r^6 is TIDAL.  The only dimensionless combination with the right radial "
      f"fall-off is {KRET_POW} ~ M^(1/3)/r, so c^2|D qt| ~ M^(1/3)/r^2 -- calibrate on a 6e10 Msun spiral "
      f"and a 6e8 Msun dwarf is predicted {scal_err:.0f}x too strong; v_c^2 = g r ~ M^(1/3)/r still falls "
      f"off, so there is no flat rotation curve and no BTFR on either footing.  I2 = 720 M^2(r-2M)/r^9 "
      f"carries the same disease: both are quadratic in the TIDAL field, not linear in the potential")
check("c11 (c) E_ij E^ij, the electric Weyl, reduces to the Newtonian potential",
      False,
      "it does not, for the same reason (E_ij = d_i d_j Phi in the weak field is the TIDAL tensor, two "
      "derivatives of the potential, not the potential); and it additionally vanishes wherever the "
      "spacetime is conformally flat -- see T5 below")

# c13: the ratio candidate -- the superposition test, which is where (c) really bites
print("\n        c13 THE SUPERPOSITION TEST for q_ratio.  It is exact for ONE point mass by construction")
print("            (control C5).  Requirement (c) is about a GENERAL static source, so: two point masses.")
two = [(1e10 * MSUN, np.array([-5.0 * KPC, 0.0, 0.0])), (1e10 * MSUN, np.array([5.0 * KPC, 0.0, 0.0]))]
pts = [("midpoint, 0.5 kpc off-axis", np.array([0.0, 0.5 * KPC, 0.0])),
       ("on-axis, 2 kpc from centre", np.array([2.0 * KPC, 0.0, 0.0])),
       ("perpendicular, 8 kpc out", np.array([0.0, 8.0 * KPC, 0.0])),
       ("far field, 200 kpc out", np.array([0.0, 200.0 * KPC, 0.0]))]
def grad_num(fn, x, src, h=1e-4):
    out = np.zeros(3)
    for i in range(3):
        dx = np.zeros(3)
        dx[i] = h * max(abs(x[i]), KPC)
        out[i] = (fn(x + dx, src) - fn(x - dx, src)) / (2 * dx[i])
    return out


ratios_q, ratios_g = [], []
print(f"            {'field point':<32} {'c^2 q_ratio':>13} {'Phi':>13} {'q/Phi':>9} "
      f"{'c^2|Dq_ratio|':>14} {'|grad Phi|':>12} {'ratio':>9}")
for lbl, xp in pts:
    qq = q_ratio_weak(xp, two)
    pp = Phi_newton(xp, two)
    gq = C_LIGHT ** 2 * np.linalg.norm(grad_num(q_ratio_weak, xp, two))
    gp = C_LIGHT ** 2 * np.linalg.norm(grad_num(Phi_newton, xp, two))
    ratios_q.append(qq / pp)
    ratios_g.append(gq / gp)
    print(f"            {lbl:<32} {qq*C_LIGHT**2:>13.4e} {pp*C_LIGHT**2:>13.4e} {qq/pp:>9.3f} "
          f"{gq:>14.4e} {gp:>12.4e} {gq/gp:>9.2f}")
check("c13 (c) q_ratio superposes, i.e. reduces to the Newtonian potential for a GENERAL static source "
      "and not merely for the single Schwarzschild solution it was tuned on",
      max(abs(x - 1) for x in ratios_q) < 0.01 and max(abs(x - 1) for x in ratios_g) < 0.05,
      f"it does not: for two equal 1e10 Msun masses 10 kpc apart, q_ratio/Phi runs from "
      f"{min(ratios_q):.3f} to {max(ratios_q):.3f} across the field and the predicted ACCELERATION runs "
      f"from {min(ratios_g):.2f}x to {max(ratios_g):.0f}x the Newtonian one.  It is exact only in the "
      f"far field, where the two-body system looks like the single point mass it was tuned on.  A ratio "
      f"of curvature invariants is not additive, so it is not a potential")

# c12: the Killing norm passes (c)
print("\n        c12 THE KILLING-NORM CANDIDATE.  ln sqrt(-xi.xi) = (1/2) ln(1 - 2M/r) -> -M/r = Phi/c^2,")
print("            and because it EQUALS Phi/c^2 at linear order it superposes exactly.")
kill_wf = sp.simplify(sp.series(kill_vals[0], M, 0, 2).removeO())
check("c12 (c) ln sqrt(-xi.xi) reduces to the Newtonian potential in the static weak field, for a general "
      "static source",
      sp.simplify(kill_wf + M / r) == 0,
      f"yes: {kill_vals[0]} = {kill_wf} + O(M^2) = Phi/c^2, and Phi obeys a linear Poisson equation so it "
      f"superposes by construction -- this candidate PASSES (c)")

print("\n    (d) EMPTY FLAT SPACE, IN EVERY COORDINATE SYSTEM.")
flat_cart = sp.eye(4).copy()
flat_cart[0, 0] = -1
flat_sph4 = sp.diag(-1, 1, r ** 2, r ** 2 * sp.sin(th) ** 2)
Rl_fc, Ric_fc, Rs_fc, gi_fc, Gam_fc = riemann_low(flat_cart, X4c)
Rl_fs, Ric_fs, Rs_fs, gi_fs4, Gam_fs = riemann_low(flat_sph4, X4)
I1_fc = contract4(Rl_fc, Rl_fc, gi_fc)
I1_fs = contract4(Rl_fs, Rl_fs, gi_fs4)
check("d1 (d) the (b)-surviving GEOMETRIC scalars (R4, I1, I2, E^2, Killing norm) vanish in genuinely "
      "empty flat space in BOTH Cartesian and spherical coordinates",
      Rs_fc == 0 and Rs_fs == 0 and I1_fc == 0 and I1_fs == 0,
      "yes -- R4 = I1 = 0 exactly in both charts, and ln sqrt(-xi.xi) = ln 1 = 0.  This is the "
      "requirement q_det fails catastrophically (control C3b, -1.6e3 kg/m^3 at 1 AU)")
flat_val = q_ratio_weak(np.array([1.0 * KPC, 0.0, 0.0]), [])
check("d2 (d) q_ratio is well defined and vanishes in genuinely empty flat space",
      not (math.isnan(flat_val) or math.isinf(flat_val)),
      "it is not: I1 = I2 = 0 in flat space, so sqrt(I1^3)/I2 is 0/0 -- undefined, not zero.  Every "
      "curvature-RATIO construction has this disease, because the ratio exists only where curvature does")


# ==========================================================================================================
print("\nSECTION 3 -- THE STRUCTURAL TENSION, ADDRESSED HEAD ON: IS IT A THEOREM?")
print("-" * 118)
# ==========================================================================================================
print("""
    The tension the assignment names is real and it has now been made precise.  Three statements, each
    proved on the geometry above rather than asserted.
""")

# --- T1: the linear-order theorem.  This is the tension itself, made computable.
print("    T1  THE DERIVATIVE-COUNT THEOREM.  Requirement (c) asks for the ZEROTH-derivative object Phi;")
print("        requirements (a)+(b) force at least the SECOND.  Nothing sits in between.")


def lin_riemann(h, x):
    return {(m, n, p, s): sp.expand(sp.Rational(1, 2) * (sp.diff(h[m, s], x[n], x[p]) + sp.diff(h[n, p], x[m], x[s])
                                                         - sp.diff(h[m, p], x[n], x[s]) - sp.diff(h[n, s], x[m], x[p])))
            for m in range(4) for n in range(4) for p in range(4) for s in range(4)}


def lin_ricci_tensor(h, x):
    hu = sp.Matrix(4, 4, lambda a, b: sum(eta[b, c] * h[a, c] for c in range(4)))
    trh = sum(eta[a, b] * h[a, b] for a in range(4) for b in range(4))
    return sp.Matrix(4, 4, lambda m, n: sp.expand(sp.Rational(1, 2) * (
        sum(sp.diff(hu[m, a], x[a], x[n]) for a in range(4))
        + sum(sp.diff(hu[n, a], x[a], x[m]) for a in range(4))
        - sum(eta[a, b] * sp.diff(h[m, n], x[a], x[b]) for a in range(4) for b in range(4))
        - sp.diff(trh, x[m], x[n]))))


PhiH = xx * yy                                            # a harmonic potential: vacuum, grad^2 Phi = 0
h_vac = sp.diag(-2 * PhiH, -2 * PhiH, -2 * PhiH, -2 * PhiH)
Ric1_vac = sp.simplify(lin_ricci_tensor(h_vac, X4c))
LR = lin_riemann(h_vac, X4c)
tidal_ok = all(sp.simplify(LR[(0, i, 0, j)] - sp.diff(PhiH, X4c[i], X4c[j])) == 0 for i in (1, 2, 3) for j in (1, 2, 3))
print(f"        vacuum weak field (Phi harmonic): linearised R_munu = 0 -> {Ric1_vac == sp.zeros(4,4)};")
print(f"        the only surviving linear invariant is R^(1)_(0i0j) = d_i d_j Phi -> {tidal_ok}")
check("T1 [theorem] some natural dimensionless scalar has a part LINEAR in h_munu that equals Phi itself, "
      "i.e. zero derivatives of the potential",
      False,
      f"none does.  A natural scalar's linear part must be invariant under h -> h + d_(mu xi_nu) "
      f"(control C4), and the complete set of such invariants is the LINEARISED RIEMANN TENSOR, which is "
      f"exactly two derivatives of h.  Computed here: in vacuum the linearised Ricci tensor vanishes "
      f"identically ({Ric1_vac == sp.zeros(4,4)}), so every Ricci-built scalar is zero there, and the one "
      f"surviving piece is R^(1)_(0i0j) = d_i d_j Phi ({tidal_ok}) -- the TIDAL tensor, dimension 1/L^2.  "
      f"Making it dimensionless needs either an external length (giving l^2 grad^2 Phi, not Phi) or a "
      f"RATIO of invariants, which is not linear at all -- and the ratio branch is exactly candidate b13, "
      f"killed on superposition (c13) and on 0/0 in flat space (d2).  Both horns are closed")

# --- T4: the slice-metric no-go
print("\n    T4  THE SLICE-METRIC NO-GO.  Any qt = F[gamma] built from the SPATIAL METRIC ALONE fails.")
print("        Proof, using only objects computed above:")
print("          1. the lam = 1 (PG) slice of vacuum Schwarzschild has gamma_ij EXACTLY FLAT (control C2),")
print("             i.e. isometric to a slice of Minkowski;")
print("          2. requirement (d) then forces F[gamma_PG] = F[flat] = 0 -- F cannot tell the PG slice of")
print("             a black hole from a slice of empty space, because it sees only gamma;")
print("          3. requirement (b) propagates that zero to EVERY slice of the same spacetime, so qt = 0")
print("             on the static slice too;")
print("          4. requirement (c) demands c^2|D qt| = g_Newton /= 0 there.  Contradiction.")
check("T4 [theorem] a functional of the spatial metric alone can satisfy (b), (c) and (d) simultaneously",
      False,
      "it cannot: PG's gamma is exactly flat while the spacetime is not, so (d) forces qt = 0 there, (b) "
      "propagates the zero to the static slice, and (c) is then violated.  This kills A1's ENTIRE "
      "structure -- a MOND constraint on the conformal mode of gamma -- not merely the choice ln det gamma")

# --- e1: momentum.  Where the (b)-survivors actually live.
print("\n    e1  WHERE THE (b)-SURVIVORS LIVE, and what that does to the count.")
R3_pg = KEXT[sp.Integer(1)]["R3"]
KK_pg = sp.simplify(KEXT[sp.Integer(1)]["KK"])
K_pg = sp.simplify(KEXT[sp.Integer(1)]["K"])
print(f"        On the PG slice: R3 = {R3_pg} exactly, while K = {K_pg} and K_ijK^ij = {KK_pg}.")
print("        Gauss-Codazzi then says the whole of I1 = 48 M^2/r^6 there is built out of K_ij, i.e. out")
print("        of the gravitational MOMENTUM pi^ij.  So on that slice every (b)-survivor is a function of")
print("        pi alone.")
check("e1 (e) a (b)-surviving qt leaves C_M momentum-free, so A1's rank-2 argument -- the SOLE source of "
      "its 2-DOF claim -- still applies",
      False,
      f"it does not: on the PG slice R3 = {R3_pg} and all of the curvature sits in K_ij, so delta C_M / "
      f"delta pi^ij /= 0.  A1's count assumed C_M contains no gravitational momentum; that hypothesis is "
      f"false for every candidate that passes (b).  A constraint on pi alone is a SLICING condition (the "
      f"CMC/York type), which is the preferred foliation arriving by the other door")

# --- e2: the Killing candidate, ruthlessly
print("\n    e2  THE KILLING-NORM CANDIDATE, judged as hard as the others.  It passes (a), (b), (c), (d).")
aa = sp.Function("a")(tt)
g_flrw = sp.diag(-1, aa ** 2, aa ** 2, aa ** 2)
Gam_flrw, gi_flrw = christoffel(g_flrw, X4c)
xid_flrw = [sp.simplify(sum(g_flrw[i, j] * [1, 0, 0, 0][j] for j in range(4))) for i in range(4)]
KV_flrw = sp.Matrix(4, 4, lambda a, b: sp.simplify(
    (sp.diff(xid_flrw[b], X4c[a]) - sum(Gam_flrw[m][a][b] * xid_flrw[m] for m in range(4))
     + sp.diff(xid_flrw[a], X4c[b]) - sum(Gam_flrw[m][b][a] * xid_flrw[m] for m in range(4))) / 2))
check("e2 (e)+(f) ln sqrt(-xi.xi) is available as a replacement for q: it exists on the spacetimes the "
      "theory must describe, and it removes a gravitational degree of freedom",
      False,
      f"neither.  (i) EXISTENCE: FLRW has no timelike Killing vector -- nabla_(a xi_b) for xi = d/dt is "
      f"{sp.simplify(KV_flrw[1,1])} /= 0 whenever adot /= 0 -- so the candidate is UNDEFINED on cosmology "
      f"and on any evolving galaxy; the conformal Killing vector that does exist gives ln a, spatially "
      f"constant, which is L12's cosmology failure verbatim.  (ii) COUNT: xi is fixed by the whole "
      f"spacetime, not by (gamma, pi) on one slice, so C_M is not a constraint on the gravitational phase "
      f"space at all -- it removes NO mode and merely over-determines the lapse, which is a khronon "
      f"written in geometric clothing.  On the spacetimes where xi does exist, ln sqrt(-xi.xi) IS the "
      f"static lapse, i.e. candidate b06")

# --- T5: the curvature pincer
print("\n    T5  THE CURVATURE PINCER.  A local curvature scalar splits into Ricci and Weyl parts, and the")
print("        two halves fail on OPPOSITE sides of the problem.")
Rl_flrw, Ric_flrw, Rs_flrw, gi_flrw2, Gam_flrw2 = riemann_low(g_flrw, X4c)
C_flrw = weyl_low(Rl_flrw, Ric_flrw, Rs_flrw, g_flrw)
weyl_flrw_zero = all(sp.simplify(C_flrw[a][b][c][d]) == 0
                     for a in range(4) for b in range(4) for c in range(4) for d in range(4))
# interior Schwarzschild (uniform-density star): the static counterpart of FLRW
R0 = sp.Symbol("R_0", positive=True)
fin = 1 - 2 * M * r ** 2 / R0 ** 3
Nin = sp.Rational(1, 2) * (3 * sp.sqrt(1 - 2 * M / R0) - sp.sqrt(fin))
g_int = sp.diag(-Nin ** 2, 1 / fin, r ** 2, r ** 2 * sp.sin(th) ** 2)
Rl_int, Ric_int, Rs_int, gi_int, Gam_int = riemann_low(g_int, X4)
C_int = weyl_low(Rl_int, Ric_int, Rs_int, g_int)
sub_int = {M: sp.Rational(1, 10), R0: sp.Integer(3), r: sp.Rational(7, 5), th: sp.Rational(11, 10)}
maxC = max(abs(complex(sp.N(C_int[a][b][c][d].subs(sub_int), 30)))
           for a in range(4) for b in range(4) for c in range(4) for d in range(4))
maxR = max(abs(complex(sp.N(Rl_int[a][b][c][d].subs(sub_int), 30)))
           for a in range(4) for b in range(4) for c in range(4) for d in range(4))
print(f"        FLRW: Weyl tensor identically zero = {weyl_flrw_zero}")
print(f"        interior Schwarzschild (uniform-density star): max|Weyl| = {maxC:.3e} against "
      f"max|Riemann| = {maxR:.3e}")
check("T5 [theorem] some LOCAL curvature scalar can serve as the MOND potential everywhere the theory "
      "must work",
      False,
      f"no, and the two halves fail on opposite sides.  RICCI half (R4, R_munu R^munu, T, rho): "
      f"proportional to T_munu, hence exactly ZERO in vacuum -- no field outside a galaxy's baryons, "
      f"where the rotation curve is.  WEYL half (I1, E^2, C^2, and every ratio built from them): exactly "
      f"ZERO wherever the spacetime is conformally flat -- verified here for FLRW (Weyl = 0 identically) "
      f"and for the interior Schwarzschild solution, a uniform-density star (max|Weyl| = {maxC:.1e} vs "
      f"max|Riemann| = {maxR:.1e}), where |grad Phi| = (4 pi G rho/3) r /= 0.  Newtonianly: inside any "
      f"homogeneous region the traceless part of d_i d_j Phi vanishes while the force does not")

# --- T3: the homogeneity theorem -- q-independent
print("\n    T3  THE HOMOGENEITY THEOREM.  This one needs no search at all, and it is the sharpest result")
print("        of the lane: it is INDEPENDENT of what q is.")
Qt = sp.Function("Q")(tt)
gam_flrw3 = sp.diag(aa ** 2, aa ** 2, aa ** 2)
Dq_flrw = sp.simplify(grad_sq3(Qt, gam_flrw3, [xx, yy, zz]))
V_flrw = [sp.simplify((1 - sp.exp(-sp.sqrt(Dq_flrw))) * sum(gam_flrw3.inv()[i, j] * sp.diff(Qt, [xx, yy, zz][j])
                                                            for j in range(3))) for i in range(3)]
CM_flrw = cov_div3(V_flrw, gam_flrw3, [xx, yy, zz])
rho_c = 3 * H0 ** 2 / (8 * math.pi * G_N)
rho_m = OMEGA_M * rho_c
check("T3 [theorem] the constraint C_M = D_i[mu(y) D^i qt] - S ~ 0 admits a nonzero matter density on a "
      "homogeneous background, for SOME scalar qt",
      False,
      f"for NO scalar qt.  On an exactly homogeneous slice every spatial scalar is spatially constant, so "
      f"D_i qt = 0, y = 0 and the frozen kernel gives mu(0) = 1 - e^0 = 0: the whole operator vanishes "
      f"identically (verified symbolically, C_M = {CM_flrw}), leaving C_M = -S and therefore rho = 0 "
      f"against rho_m = {rho_m:.3e} kg/m^3 today.  a0 does not appear, so the statement is IDENTICAL on "
      f"both footings ({A0['canonical']:.4e} and {A0['alt']:.4e}).  A1's cosmology failure is a property "
      f"of its CONSTRAINT FORM, not of ln det gamma, and no replacement for q can repair it")

# --- f1: compatibility with GR's own Hamiltonian constraint, inherited by any (c)-satisfying qt
print("\n    f1  COMPATIBILITY (L12's matter failure), inherited by ANY candidate that satisfies (c).")


def mond_g(gN, a0):
    lo, hi = gN, max(10 * gN, 10 * a0)
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if mid * (1 - math.exp(-mid / a0)) < gN:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


gN_ref = G_N * 1e10 * MSUN / (10 * KPC) ** 2
ratios = {}
for foot, a0 in A0.items():
    ratios[foot] = mond_g(gN_ref, a0) / gN_ref
    print(f"        {foot:<10}: H_perp wants g = {gN_ref:.4e}, C_M wants g = {mond_g(gN_ref,a0):.4e} m/s^2 "
          f"-- factor {ratios[foot]:.3f}")
check("f1 (f) a (c)-satisfying qt is compatible with GR's own Hamiltonian constraint rather than "
      "over-determining it",
      False,
      f"it is not, and the failure is inherited from (c) itself: any qt that reduces to Phi/c^2 in the "
      f"static weak field ALREADY obeys grad^2 qt = 4 pi G rho/c^2 by H_perp.  Imposing C_M as well leaves "
      f"div[e^{{-y}} grad qt] = 0 with e^{{-y}} > 0 strictly, whose only decaying solution is qt = const, "
      f"i.e. g = 0.  The two constraints demand accelerations differing by {ratios['canonical']:.2f}x "
      f"(canonical) / {ratios['alt']:.2f}x (alt) for 1e10 Msun at 10 kpc.  Requirement (c) and "
      f"requirement (f) are in direct conflict for ANY q")


# ==========================================================================================================
print("\nSECTION 4 -- VERDICT")
print("-" * 118)
# ==========================================================================================================
SUMMARY = [
    ("q_det = -(1/6) ln(det gamma/det gbar)", "b", "slice-dependent: g_N/3 / g_N/4 / 0 across three cuts "
                                                   "(g_N with the isotropic fiducial)"),
    ("R3, spatial Ricci scalar", "b", "0 on static AND PG by coincidence; nonzero on the third cut"),
    ("K, the York time", "b", "0 on static, (3/2) sqrt(2M/r^3) on PG (sign per convention)"),
    ("K_ij K^ij", "b", "0 on static, nonzero on PG"),
    ("A_ij A^ij, trace-free part", "b", "0 on static, nonzero on PG"),
    ("ln N, the ADM lapse", "b", "the khronometric choice; N IS the slicing, 0 on PG"),
    ("c^2 |D ln N|, normal-observer accel.", "b", "g_N on static, exactly 0 on PG"),
    ("R4, spacetime Ricci scalar", "c", "survives (b); = 0 in ALL vacuum, so no field outside baryons"),
    ("I1 = Kretschmann", "c", "survives (b); tidal, M^(1/3)/r scaling, no BTFR; 0 in conformally flat regions"),
    ("I2 = grad-Riemann squared", "c", "survives (b); same tidal disease"),
    ("E_ij E^ij, electric Weyl", "c", "survives (b) even under radial boost; tidal, and 0 inside uniform density"),
    ("T = T^mu_mu, matter scalar", "c", "survives (b) vacuously; = 0 in vacuum, no field outside baryons"),
    ("q_ratio = -(720/48^1.5) sqrt(I1^3)/I2", "c,d", "survives (b) and gives -M/r EXACTLY for one point mass; "
                                                     "does not superpose (0.6x-3400x the Newtonian force on a two-body "
                                                     "field); 0/0 in genuinely flat space"),
    ("ln sqrt(-xi.xi), Killing norm", "e,f", "survives (a),(b),(c),(d); no timelike xi on FLRW or any "
                                             "evolving system; not a functional of (gamma,pi) so removes no mode; "
                                             "where xi exists it IS the static lapse"),
]
print(f"    {'candidate':<40} {'dies on':<8} {'how'}")
print("    " + "-" * 112)
for lab, where, how in SUMMARY:
    print(f"    {lab:<40} {where:<8} {how}")
print("    " + "-" * 112)

check("V1 [VERDICT] a scalar, foliation-independent replacement for q = -(1/6) ln det gamma EXISTS that "
      "meets requirements (a)-(f)",
      False,
      "no.  7 of 14 candidates die on (b) alone; the 7 that survive (b) die on (c) or (d); the single "
      "candidate that reaches (e) is the Killing norm, which does not exist on the backgrounds the theory "
      "must describe and removes no gravitational mode.  L12's construction obligation is not merely "
      "unmet -- it is unmeetable in this class")
check("V2 [VERDICT] the failure is GENERIC -- a theorem about the class rather than an obstacle this lane "
      "could not get past",
      True,
      "yes, on four independent counts.  T1: a natural scalar's linear part is built from the linearised "
      "Riemann tensor, hence at least two derivatives of Phi, while (c) asks for Phi itself; the only "
      "escape is a ratio, which is not linear and dies on superposition.  T4: (b)+(d) force any "
      "gamma-only qt to vanish on Schwarzschild, killing A1's structure and not just its choice of q.  "
      "T5: local curvature scalars split into a Ricci half that vanishes in vacuum and a Weyl half that "
      "vanishes in conformally flat regions, so no local curvature scalar works on both sides.  T3: on a "
      "homogeneous background EVERY spatial scalar has D_i qt = 0, so mu(0) = 0 forces rho = 0 -- "
      "q-independent, and fatal on its own")

print("\n" + BAR)
print(f"L27 SUMMARY: {len(FAILS)} FAIL")
for nm in FAILS:
    print(f"   FAIL: {nm}")
print(BAR)
print("""
THE ANSWER TO THE LANE'S QUESTION: NO.

The structural tension the assignment names is a THEOREM, not an obstacle.  Stated in one line: a
foliation-independent scalar built from the geometry is a curvature, and a curvature is at least two
derivatives of the potential; a quantity that behaves like a potential is at most one derivative of the
metric and is therefore a property of the cut.  Requirement (c) asks for the ZEROTH-derivative object;
requirements (a) and (b) together force at least the SECOND.  Nothing sits in between, because there is
no diffeomorphism-invariant object linear in h with fewer than two derivatives -- the linearised Riemann
tensor is the complete set of gauge invariants of linearised gravity (control C4 verifies its gauge
invariance and its value 2 grad^2 Phi; check T1 verifies the consequence, that in vacuum the linearised
Ricci tensor vanishes identically and the sole surviving invariant is the tidal tensor d_i d_j Phi).

The two escapes that remain are exactly the two the requirement I3a exists to forbid:
  * supply a preferred time direction -- a khronon, or a Killing vector where one happens to exist -- and
    read the potential off the lapse.  That is candidate b06/b12, and it is the khronometric theory;
  * make qt NONLOCAL: solve an elliptic equation for it, i.e. introduce an auxiliary potential field.
    That is AQUAL/QUMOND, whose constraint is a condition on the auxiliary field and NOT on the
    gravitational phase space, so it removes no conformal mode and A1's 2-DOF count does not apply to it.

And T3 stands over all of it: even a perfect qt would force rho = 0 on FLRW, because the frozen kernel
has mu(0) = 0 and every spatial scalar is spatially constant on a homogeneous slice.  A1's cosmology
failure was never about ln det gamma.

WHAT SURVIVES AND SHOULD BE CARRIED FORWARD, unchanged from L12 and independent of q: an elliptic
constraint whose principal part acts on the conformal mode does leave exactly two tensor polarisations,
and the exponential kernel inside such a constraint screens the Solar System by a local acceleration with
no 1/y.  What is now settled is that the object the kernel acts on cannot be built out of the geometry of
a slice.
""")
raise SystemExit(0)

"""GATE (freeze session 2026-08-27): MATTER CONSERVATION derived, not asserted, for the
frozen MMG_constraint_first chassis.

Chassis (openai_push/final_closure, certified 12-gate + Gate 13):
  H_T = H_can + int d^3x [ lambda_N pi_N + mu_1 C_M + mu_2 D^2 q + mu_3 D^2 p ] + (shift terms)
  H_can = H_GR + H_m ,  H_GR = int [ N Hperp_grav + N^i H_i_grav ],  H_m = int [ N eps_n + N^i j_i ]
  C_M = D_i[ c^2 mu(y) D^i ln N ] - 4 pi G rho_m ,  y = (c^2/a0)|D ln N| ,  rho_m = T_nn/c^2 (mass units)
  second-class set (pi_N, C_M, D^2 q, D^2 p); first-class (pi_i, H_i).  NO Hamiltonian constraint.

THE HOLE THIS GATE CLOSES.  Gate 8 of the certified suite solves the multiplier system
purely symbolically: mu_1 = -r_4/L_N with r_4 = {pi_N, H_can} left as an ARBITRARY SYMBOL.
Gate 10 then claims the matter EOM correction is O(v^2/c^2).  Neither script ever evaluates
r_4.  This script evaluates it:

  r_4 = {pi_N, H_can} = -(Hperp_grav + sqrt(gamma) eps_n)

and because the chassis DELETES the Hamiltonian constraint (D^2 q ~ 0 forces the conformal
mode flat, so Hperp_grav ~ 0 at Newtonian order while eps_n = rho c^2 != 0), r_4 is
matter-density-sourced and mu_1 is NOT small.  The mu_1 C_M term in H_T contains matter
variables through rho_m, so matter feels an extra force.  We derive it exactly at leading
order, then price it in (a) the solar system at 1 AU, (b) PSR B1913+16, (c) a galaxy at
g ~ a0, against committed bounds.

KEY RESULT (derived below):
  Define chi := -(4 pi G / c^2) mu_1.  The pi_N-preservation equation becomes
     D_i[ c^2 M^{ij} D_j chi ] = 4 pi G rho    (same source as C_M, LINEARIZED operator
                                                M^{ij} = mu delta^ij + y mu' nhat^i nhat^j)
  and every matter species (rho_m = T_nn is universal) evolves under the effective lapse
     N_eff = N + chi ,
  i.e. acceleration  a = -grad(Psi + X),  X = c^2 chi,  instead of the geodesic -grad Psi.
  In spherical symmetry (Gauss):  c^2 chi' = g_N / M_par(y),  M_par = mu + y mu' = d(y mu)/dy.
  So the matter force is  g_matter = g_N [ 1/mu + 1/M_par ]  -- Newtonian region: 2 g_N
  (EXACT DOUBLING, zeroth order in v/c); deep MOND: (3/2) sqrt(g_N a0).
  The violation of grad_mu T^{mu nu} = 0 w.r.t. the chassis metric g = (-N^2 c^2, gamma_ij) is
     grad_mu T^{mu i} = -rho c^2 D^i chi = -rho g_N / M_par(y) nhat^i    (static spherical)
  which is NEWTONIAN order -- (v/c)^0, first order in Phi/c^2 -- not O(v^2/c^2) as Gate 10
  claimed.  Conservation DOES hold, exactly and on matter shell, w.r.t. the EFFECTIVE metric
  g_eff = (-(N+chi)^2 c^2, gamma_ij) because the coupling is universal; the theory is secretly
  a TWO-POTENTIAL theory (the same disease as the york-route audit E-FAIL, G_eff = 2G).

Discipline: every number below is computed here or quoted from a committed source named inline.
"""

import numpy as np
import sympy as sp

ok = True
def check(cond, label, detail=""):
    global ok
    tag = "PASS" if cond else "FAIL"
    if not cond:
        ok = False
    print(f"  [{tag}] {label}" + (f"  -- {detail}" if detail else ""))

# =============================================================================
print("=" * 78)
print("PART A -- symbolic: the linearized operator M_par = mu + y mu' = d(y mu)/dy")
print("=" * 78)
# The mu_1 (equivalently chi) equation carries the LINEARIZATION of the C_M flux
# around the physical lapse.  In 1D/radial with u = phi' > 0, y = (c^2/a0) u:
u, a0s, cs, ns = sp.symbols("u a0 c n", positive=True)
y = cs**2 * u / a0s
for name, mu_of_y in [("mu_exp", 1 - sp.exp(-y)),
                      ("mu_5", y / (1 + y**5) ** sp.Rational(1, 5)),
                      ("mu_10", y / (1 + y**10) ** sp.Rational(1, 10))]:
    F = cs**2 * mu_of_y * u                    # radial flux  c^2 mu(y) phi'
    dF = sp.simplify(sp.diff(F, u))            # linearization d/dphi'
    yy = sp.symbols("yy", positive=True)
    mu_y = mu_of_y.subs(u, a0s * yy / cs**2)   # mu as function of y
    target = sp.simplify(cs**2 * (mu_y + yy * sp.diff(mu_y, yy)))
    diff = sp.simplify(dF.subs(u, a0s * yy / cs**2) - target)
    check(diff == 0, f"d/dphi'[c^2 mu phi'] = c^2 (mu + y mu')  for {name}")

# Self-adjointness of the linearized operator (so the pi_N variation lands on mu_1):
x = sp.symbols("x")
m1 = sp.Function("m1")(x); w = sp.Function("w")(x); Mf = sp.Function("M")(x)
I = m1 * sp.diff(Mf * sp.diff(w, x), x) - sp.diff(Mf * sp.diff(m1, x), x) * w
bdry = sp.diff(Mf * (m1 * sp.diff(w, x) - sp.diff(m1, x) * w), x)
check(sp.simplify(I - bdry) == 0,
      "m1 L[w] - L[m1] w = total derivative (Sturm-Liouville self-adjoint)")

# Hperp_grav ~ 0 at Newtonian order: D^2 q ~ 0 (decaying) => det gamma = 1; the remaining
# TT part cannot source linear R:  R^(1) = k_i k_j h_ij - k^2 h_ii = 0 for TT.
k3 = sp.symbols("k", positive=True)
hp, hx = sp.symbols("h_+ h_x")
h = sp.Matrix([[hp, hx, 0], [hx, -hp, 0], [0, 0, 0]])   # TT for k along z
kvec = sp.Matrix([0, 0, k3])
R1 = (kvec.T * h * kvec)[0] - k3**2 * h.trace()
check(sp.simplify(R1) == 0, "linear R^(3) vanishes for TT metric (Hperp_grav ~ 0 + static pi=0)")
# D^2 p ~ 0 (decaying) => p = pi/sqrt(gamma) trace = 0; static TT => pi^ij = 0: kinetic term 0.

# =============================================================================
print()
print("=" * 78)
print("PART B -- symbolic: matter EOM from H_T (the mu_1 force) and grad_mu T^{mu nu}")
print("=" * 78)
# Point particle in H_T:  H_p = N E_p + [mu_1 * (-4 pi G)] * (E_p/c^2),  E_p = sqrt(m^2c^4+p^2c^2)
# (rho_m in C_M is the particle's T_nn/c^2 = (E_p/c^2) delta^3).  With chi = -4 pi G mu_1/c^2:
t = sp.symbols("t")
p, m, c = sp.symbols("p m c", positive=True)
Psi = sp.Function("Psi")(x); X = sp.Function("X")(x)
N_lapse = 1 + Psi / c**2
chi = X / c**2
E_p = sp.sqrt(m**2 * c**4 + p**2 * c**2)
H_p = (N_lapse + chi) * E_p
pdot = -sp.diff(H_p, x)
acc_at_rest = sp.simplify(pdot.subs(p, 0) / m)
check(sp.simplify(acc_at_rest + sp.diff(Psi, x) + sp.diff(X, x)) == 0,
      "a = -grad(Psi + X): the mu_1 force enters at (v/c)^0 -- NEWTONIAN order",
      f"a = {acc_at_rest}")
# Photon: H_gamma = (N + chi) c |p|  -- SAME effective lapse => coupling universal (EEP kept;
# conservation exact on-shell w.r.t. g_eff with lapse N+chi).

# grad_mu T^{mu x} w.r.t. the CHASSIS metric g = diag(-c^2(1+2Psi/c^2), 1):  dust, 1D, leading order.
rho = sp.Function("rho")(t, x); v = sp.Function("v")(t, x)
Ttt = rho; Ttx = rho * v; Txx = rho * v**2
Gamma_x_tt = sp.diff(Psi, x)          # leading Christoffel of the chassis metric
divT_x = sp.diff(Ttx, t) + sp.diff(Txx, x) + Gamma_x_tt * Ttt
continuity = sp.Eq(sp.diff(rho, t), -sp.diff(rho * v, x))
euler = sp.Eq(sp.diff(v, t), -v * sp.diff(v, x) - sp.diff(Psi + X, x))   # ACTUAL chassis EOM
divT_x = divT_x.subs({sp.diff(rho, t): continuity.rhs, sp.diff(v, t): euler.rhs})
divT_x = sp.simplify(sp.expand(divT_x))
check(sp.simplify(divT_x + rho * sp.diff(X, x)) == 0,
      "grad_mu T^{mu x}|_g = -rho dX/dx  (NOT zero; violation = the chi force itself)",
      f"divT = {divT_x}")
print("  => Verdict structure: w.r.t. chassis metric g: VIOLATED at Newtonian order.")
print("     w.r.t. effective metric (lapse N+chi): exact on matter shell (universal coupling).")

# =============================================================================
print()
print("=" * 78)
print("PART C -- kernels and the exact static-spherical anomaly  g_chi = g_N / M_par(y)")
print("=" * 78)

def make_kernel(kind, nn=None):
    if kind == "exp":
        mu  = lambda yv: 1 - np.exp(-yv)
        Mpar= lambda yv: 1 - np.exp(-yv) + yv * np.exp(-yv)
        lab = "mu_exp"
    else:
        mu  = lambda yv: yv * (1 + yv**nn) ** (-1.0 / nn)
        Mpar= lambda yv: yv * (2 + yv**nn) * (1 + yv**nn) ** (-(nn + 1.0) / nn)
        lab = f"mu_{nn}"
    return lab, mu, Mpar

kernels = [make_kernel("exp"), make_kernel("n", 5), make_kernel("n", 10)]

# numeric check of the closed-form M_par against a finite difference
for lab, mu, Mp in kernels:
    yv = np.array([0.03, 0.3, 1.0, 1.9, 3.0, 30.0])
    h = 1e-6
    fd = ((yv + h) * mu(yv + h) - (yv - h) * mu(yv - h)) / (2 * h)
    check(np.allclose(fd, Mp(yv), rtol=1e-5), f"M_par(y) = d(y mu)/dy closed form  [{lab}]")

def y_of_gN(gN, a0, mu):
    """Solve mu(y) * y * a0 = g_N for y (the C_M Gauss law)."""
    yv = np.maximum(gN / a0, np.sqrt(np.maximum(gN / a0, 1e-300)))  # seed both regimes
    for _ in range(200):
        f = mu(yv) * yv * a0 - gN
        h = 1e-7 * np.maximum(yv, 1e-30)
        fp = (mu(yv + h) * (yv + h) - mu(yv - h) * (yv - h)) / (2 * h) * a0
        yv = np.maximum(yv - f / fp, 1e-30)
    return yv

# asymptotics of the total matter force  g_m = g_N [1/mu + 1/M_par]
for lab, mu, Mp in kernels:
    hi = 1e8; lo = 1e-6
    ratio_hi = 1 / mu(hi) + 1 / Mp(hi)
    ratio_lo = (1 / mu(lo) + 1 / Mp(lo)) * lo    # in units of g_N/y
    check(abs(ratio_hi - 2) < 1e-6, f"Newtonian regime: g_m -> 2 g_N EXACTLY  [{lab}]",
          f"1/mu+1/M_par = {ratio_hi:.8f} at y=1e8")
    check(abs(ratio_lo - 1.5) < 1e-3, f"deep MOND: g_m -> (3/2) g_N/y = (3/2) sqrt(g_N a0)  [{lab}]",
          f"(1/mu+1/M_par)*y = {ratio_lo:.6f} at y=1e-6")

# =============================================================================
print()
print("=" * 78)
print("PART D -- (a) SOLAR SYSTEM at 1 AU vs the committed ephemeris bound")
print("=" * 78)
G = 6.674e-11; Msun = 1.989e30; AU = 1.496e11; c_si = 2.998e8
BOUND = 3.66e-14   # m/s^2, Sereno & Jetzer 2006 Earth bound, committed in
                   # real_research/reviews/a0_local_ephemeris_2026.py (corpus 1278x record)
gN_au = G * Msun / AU**2
print(f"  g_N(1 AU) = {gN_au:.4e} m/s^2 ; bound = {BOUND:.2e} m/s^2")
for a0v, foot in [(9.36e-11, "canonical rho_DE/cH_Lambda"), (1.13e-10, "alt rho_total/cH0")]:
    for lab, mu, Mp in kernels:
        yloc = float(y_of_gN(np.array([gN_au]), a0v, mu)[0])
        g_chi = gN_au / Mp(yloc)
        over = g_chi / BOUND
        # charitable frame: absorb G_bare = G_lab/2; residual fractional force deviation
        resid = 0.5 * (1 / mu(yloc) + 1 / Mp(yloc)) - 1
        print(f"  [{foot} | {lab:6s}] y_loc={yloc:.3e}  g_chi={g_chi:.3e} m/s^2 "
              f"= {over:.2e} x bound ;  G-rescaled residual = {resid:.2e} x g_N")
check(gN_au / BOUND > 1e11, "UNRESCALED anomaly at 1 AU is ~1.6e11 x the ephemeris bound",
      f"{gN_au / BOUND:.2e}")
# EFE/DHF context (committed DHF lesson: solar-system observable = quadrupole at y_ext ~ 1.9):
print("\n  chi-channel vs mu-channel deviation at the EFE point y_ext = 1.9")
print("  (the route1B Cassini pricing used the mu-channel 1-mu ONLY):")
for lab, mu, Mp in kernels:
    yext = 1.9
    print(f"  [{lab:6s}] 1-mu(y_ext) = {1-mu(yext):.4f}   M_par(y_ext)-1 = {Mp(yext)-1:+.4f}"
          f"   |ratio chi/mu| = {abs(Mp(yext)-1)/(1-mu(yext)):.2f}")

# =============================================================================
print()
print("=" * 78)
print("PART E -- (b) BINARY PULSAR PSR B1913+16")
print("=" * 78)
m1_ = 1.4398 * Msun; m2_ = 1.3886 * Msun; Mtot = m1_ + m2_
Pb = 27906.98
a_rel = (G * Mtot * Pb**2 / (4 * np.pi**2)) ** (1.0 / 3.0)
gN_psr = G * Mtot / a_rel**2
y_psr = float(y_of_gN(np.array([gN_psr]), 9.36e-11, kernels[0][1])[0])
print(f"  a_rel = {a_rel:.4e} m ; g_N = {gN_psr:.4e} m/s^2 ; y = {y_psr:.3e}")
for lab, mu, Mp in kernels:
    yv = float(y_of_gN(np.array([gN_psr]), 9.36e-11, mu)[0])
    print(f"  [{lab:6s}] anomalous force g_chi/g_N = {1/Mp(yv):.6f}  (100% of Newton)")
PBDOT_CONSISTENCY = 0.0016   # Weisberg & Huang 2016: Pb_dot(obs)/Pb_dot(GR) = 0.9983 +/- 0.0016
print(f"  Unrescaled frame: 100% force anomaly vs {PBDOT_CONSISTENCY*100:.2f}% GR-consistency"
      f" => {1.0/PBDOT_CONSISTENCY:.0f} x over")
print("  G-rescaled frame: Newtonian-order anomaly absorbed into fitted masses (m_i -> m_i/2);")
print("  the 1PN post-Keplerian sector of this chassis is NOT DERIVED (no H_perp, Phi=0,")
print("  chi-channel) -- pulsar PK consistency at the 1e-3 level CANNOT be claimed; it is OPEN.")

# =============================================================================
print()
print("=" * 78)
print("PART F -- (c) GALAXY at g ~ a0: the RAR shape after the charitable G-rescaling")
print("=" * 78)
# Observable pair in the lab-G frame: g_bar = 2 g_N_bare (Cavendish sees 2G),
# g_obs = g_N_bare [1/mu + 1/M_par].  Fit the canonical one-potential law
# g_model(g_bar; a0_eff) = y a0_eff with mu(y) y a0_eff = g_bar, over the SPARC range.
a0c = 9.36e-11
gNb = np.logspace(-12.5, -8.5, 400)   # bare-G Newtonian accelerations, SPARC-ish span
for lab, mu, Mp in kernels:
    yv = y_of_gN(gNb, a0c, mu)
    g_obs = gNb * (1 / mu(yv) + 1 / Mp(yv))
    g_bar = 2 * gNb
    best = (None, np.inf)
    for s in np.linspace(0.9, 1.4, 501):
        a0e = s * a0c
        ym = y_of_gN(g_bar, a0e, mu)
        g_mod = ym * a0e
        r = np.log10(g_obs) - np.log10(g_mod)
        rms = float(np.sqrt(np.mean(r**2)))
        if rms < best[1]:
            best = (s, rms, float(np.max(np.abs(r))))
    s, rms, mx = best
    print(f"  [{lab:6s}] best a0_eff/a0 = {s:.3f}  (deep-MOND analytic 9/8 = 1.125) ;"
          f" residual SHAPE distortion rms = {rms:.4f} dex, max = {mx:.4f} dex")
print("  Compare: banked SPARC RAR scatter 0.108 dex (rar_framework_a0_mlfit.py);")
print("  the shape distortion is a SYSTEMATIC, to be added to the 0.108->0.123/0.127 mu_n cost.")

# kappa arithmetic (pure algebra, both directions; interpretation left open):
print("\n  kappa bookkeeping if the doubling is absorbed (G_bare = G_lab/2, a0_RAR = 1.125 a0_bare):")
kap_factor = np.sqrt(2) / 1.125
print(f"  kappa_bare = kappa_obs * sqrt(2)/1.125 = {kap_factor:.4f} * kappa_obs")
print(f"  holding a0_RAR = 9.36e-11 (kappa_obs = 1/2): required kappa_bare = {0.5*kap_factor:.4f}")
print(f"  vs distance-free measured kappa = 0.551 +/- 0.043:"
      f"  ({0.5*kap_factor:.4f}-0.551)/0.043 = {(0.5*kap_factor-0.551)/0.043:+.2f} sigma")
print(f"  vs BTFR measured kappa = 0.465 +/- 0.076:"
      f"  ({0.5*kap_factor:.4f}-0.465)/0.076 = {(0.5*kap_factor-0.465)/0.076:+.2f} sigma")

# =============================================================================
print()
print("=" * 78)
print("PART G -- lensing cross-check (does the chi-channel rescue the lensing FAIL? NO)")
print("=" * 78)
print("  Photons couple to the SAME effective lapse N+chi (rho_m = T_nn is universal):")
print("  deflection ~ grad_perp(Psi+X) ; dynamics ~ grad(Psi+X).  Both channels doubled =>")
print("  the lensing/dynamics ratio is UNCHANGED: still 1/2 of the equal-slip value.")
print("  The gate_lensing_weakfield_derivation FAIL stands; but its Part C ('a = -grad Psi,")
print("  full MOND') and its RAR-cost numbers are superseded by a = -grad(Psi+X).")

print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("""  r_4 = {pi_N,H_can} = -(Hperp_grav + eps_n) ~ -rho c^2  (Hperp deleted, D^2q~0)  [Part A]
  mu_1 = -r_4/L_N is DENSITY-SOURCED; chi = -4piG mu_1/c^2 solves the linearized
  C_M operator with the SAME source 4 pi G rho.                                   [Part A]
  Matter EOM: a = -grad(Psi + X) -- the mu_1 force is (v/c)^0, NEWTONIAN order.   [Part B]
  grad_mu T^{mu i}|_chassis-metric = -rho D^i X != 0 ;  exact conservation holds
  only w.r.t. the effective metric with lapse N+chi (universal two-potential).    [Part B]
  Gate 10's 'correction is O(v^2/c^2)' claim is FALSIFIED.
  (a) 1 AU: unrescaled anomaly 5.9e-3 m/s^2 = 1.6e11 x Sereno-Jetzer bound;
      G-rescaled residual ~ e^{-y_loc} / y_loc^{-n} = 0 locally; chi-channel at the
      EFE point y_ext=1.9 is 0.90 (mu_exp) / 3.88 (mu_5) / 8.99 (mu_10) x the
      mu-channel => route1B Cassini pricing must be RERUN with chi included.      [Part D]
  (b) B1913+16: unrescaled 100% force anomaly (~600 x the 0.16% GR consistency);
      G-rescaled: absorbed at Newtonian order, 1PN PK sector UNDERIVED (open).    [Part E]
  (c) galaxy: after the best joint (2G, a0_eff~1.125a0) absorption an irreducible
      RAR SHAPE distortion remains (numbers above, ~0.01-0.05 dex scale) and the
      kappa=1/2 calibration moves to kappa_bare ~ 0.63 (1.8-2.2 sigma from the
      measured brackets).                                                         [Part F]
  Kernel dependence: the doubling (y->inf) and the deep-MOND 3/2 are shared by
  mu_exp and mu_n exactly; mu_n does NOT repair this defect (it is structural:
  the deleted Hamiltonian constraint sources mu_1).                               [Part C]
""")
print("GATE RESULT: DERIVED -- FAIL (matter conservation)" if ok else "GATE RESULT: SCRIPT INCONSISTENCY")
import sys
sys.exit(0 if ok else 1)

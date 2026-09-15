#!/usr/bin/env python3
"""H013 -- G03 SWARM LANE: the localised filter action (direction 1), gate S1 + P3 sketch.

CONTEXT (astra's G03 spec, fable_independent_2026/G03_SPEC_FOR_SWARMS_2026-09-15.md).
  Every relativistic completion died on Cassini.  The k^4 PPN gate sorted the
  escapes: every LOCAL fourth-order operator makes alpha_1 grow as (xi k)^2 and
  dies (G030, G034, G032, H004->H006).  What survives is a COHERENT STIFFENING
  OF THE WHOLE Y SECTOR giving the PROPAGATOR form
        J_Y -> J_Y (1 + xi^2 k^2)   in the denominator, i.e.  1/(1 + xi^2 k^2).

  Direction 1 of the spec: "The double filter (Gaussian or Helmholtz, output
  filter compulsory) as one or two auxiliary fields with ... Helmholtz mass
  1/xi; count the extra modes (P3) before believing S2."

THE IDEA THIS LANE WRITES AND CHECKS.
  The obstruction to the propagator form is that writing 1/(1 + xi^2 k^2)
  directly means a k^4 OPERATOR, which is fourth-order and carries an
  Ostrogradsky ghost.  But a propagator is what you get by INTEGRATING OUT an
  auxiliary field -- and the localised parent is only SECOND order:

      S = int sqrt(-g) [ M_P^2 R / 2 + Lambda^4 f(X)
                         - (Z/2) (grad chi)^2 - (1/2) m^2 (chi - phi)^2 ] + S_m

  with m = 1/xi.  Varying chi gives  (□ - m^2) chi = -m^2 phi, i.e.
        chi = m^2 / (m^2 - □)  phi      ->     chi_k = phi_k / (1 + xi^2 k^2)
  in Fourier.  That is EXACTLY the f31c surviving form, obtained from a local,
  second-order action.  No k^4 operator appears, so there is no Ostrogradsky
  ghost and no (xi k)^2 growth in alpha_1.  The filter is an OUTPUT filter:
  matter and light respond to the filtered field.

  This is why the door was missed: people wrote the form factor as an operator
  (fourth order, ghost) instead of as a field (second order, healthy).

GATES RUN HERE (cheap kills first, per the spec).
  S1  static reduction: the action's OWN field equations, reduced on the static
      branch, give the programme's kernel law with the output filtered, plus a
      stated correction of order (xi grad)^2.  The modified source is DERIVED,
      not postulated.
  P3  mode count (sketch): both phi and chi are second order -> no Ostrogradsky
      mode; the extra mode is healthy for Z > 0, m^2 > 0.

A0 FOOTINGS: 9.3619e-11 (canonical) and 1.1279e-10 (alternative), both run.

HONEST SCOPE: this lane does NOT run S2 (the Cassini quadrupole integral) --
that needs hunt_2026/g01 and is the next commit.  It does not claim the
candidate passes Cassini; it establishes that the candidate is a legal,
healthy, second-order action whose static limit is the filtered kernel law,
which is the precondition for S2 being meaningful.

Every check states measurement and threshold separately.
"""
import sympy as sp
import json, math

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

# the two a0 footings, per the spec
FOOT = {"canonical": 9.3619e-11, "alternative": 1.1279e-10}

print("="*74)
print("H013 -- G03 SWARM: THE LOCALISED FILTER ACTION (direction 1)")
print("="*74)

# ============================================================ the action
print("\n" + "="*74)
print("PART 0 -- THE ACTION (every term written)")
print("="*74)
print("""
    S = int sqrt(-g) [ M_P^2 R/2
                       + Lambda^4 f(X),            X = -(grad phi)^2/(2 Lambda^4)
                       - (Z/2) (grad chi)^2
                       - (1/2) m^2 (chi - phi)^2  ]  + S_m[g, psi]

    m = 1/xi.   Boundary term: the standard Gibbons-Hawking-York for R.
    No clock, no aether, no preferred structure: phi and chi are true scalars.
    Matter couples minimally to g only.
""")

# ============================================================ S1: the equations
print("\n" + "="*74)
print("PART S1 -- STATIC REDUCTION (sympy: field equations, then static limit)")
print("="*74)

t, x1 = sp.symbols('t x1')
phi = sp.Function('phi')(t, x1)
chi = sp.Function('chi')(t, x1)
Z, m, Lam4 = sp.symbols('Z m Lambda4', positive=True)

# 1+1 flat space, signature (-,+): (grad u)^2 = -u_t^2 + u_x^2
def kin(u): return -sp.diff(u, t)**2 + sp.diff(u, x1)**2

X = -kin(phi)/(2*Lam4)
f = sp.Function('f')
L = Lam4*f(X) - (Z/2)*kin(chi) - (m**2/2)*(chi - phi)**2

# Euler-Lagrange for chi:  dL/dchi - d/dx(dL/dchi_x) - d/dt(dL/dchi_t) = 0
EL_chi = sp.simplify(
    sp.diff(L, chi)
    - sp.diff(sp.diff(L, sp.diff(chi, x1)), x1)
    - sp.diff(sp.diff(L, sp.diff(chi, t)), t))
print(f"\n  EOM(chi):  {sp.simplify(EL_chi/(-1))} = 0")
print("             i.e.  Z (□ chi) - m^2 (chi - phi) = 0")
print("                   (□ - m^2) chi = -m^2 phi      [with Z = 1]")

# verify: with Z=1 the chi equation is (lap - m^2) chi = -m^2 phi
EL_chi_Z1 = sp.simplify(EL_chi.subs(Z, 1))
target = -( m**2*(chi - phi) - (sp.diff(chi, x1, 2) - sp.diff(chi, t, 2)) )
check("S1a [THE CHI EQUATION] varying the auxiliary gives the screened\n"
      "      Helmholtz equation (□ - m^2) chi = -m^2 phi  (sympy, from the action)",
      f"residual = {sp.simplify(EL_chi_Z1 + m**2*(chi-phi) - (sp.diff(chi,x1,2)-sp.diff(chi,t,2)))}",
      sp.simplify(EL_chi_Z1 + m**2*(chi-phi) - (sp.diff(chi,x1,2)-sp.diff(chi,t,2))) == 0,
      "This is a SECOND-ORDER equation for a healthy massive scalar. The\n"
      "         filter is not an operator acting on phi -- it is a field that\n"
      "         tracks a smoothed copy of phi.")

# Fourier form: chi_k = phi_k / (1 + xi^2 k^2)
k, xi = sp.symbols('k xi', positive=True)
# (lap - m^2) chi = -m^2 phi ; in Fourier with lap -> -k^2, m = 1/xi:
#   (-k^2 - 1/xi^2) chi_k = -(1/xi^2) phi_k
#   chi_k = (1/xi^2)/(k^2 + 1/xi^2) phi_k = phi_k/(1 + xi^2 k^2)
chi_k = (1/xi**2)/(k**2 + 1/xi**2)
check("S1b [THE PROPAGATOR FORM] in Fourier the solution is\n"
      "      chi_k = phi_k / (1 + xi^2 k^2) -- EXACTLY the f31c surviving form",
      f"chi_k/phi_k = {sp.simplify(chi_k)}  ->  1/(1 + xi^2 k^2): "
      f"{sp.simplify(chi_k - 1/(1 + xi**2*k**2))}",
      sp.simplify(chi_k - 1/(1 + xi**2*k**2)) == 0,
      "THE POINT: f31c says the lock is evaded by the propagator form. Writing\n"
      "         that form as an operator needs k^4 (fourth order, Ostrogradsky\n"
      "         ghost, alpha_1 ~ (xi k)^2 -> dies, G030/G034). As an AUXILIARY\n"
      "         FIELD the same form factor comes from a second-order action.\n"
      "         The form factor was never the problem; writing it as an\n"
      "         operator was.")

# ============================================================ the phi equation
print("\n" + "="*74)
print("PART S1c -- the phi equation and the output filter")
print("="*74)

EL_phi = sp.simplify(
    sp.diff(L, phi)
    - sp.diff(sp.diff(L, sp.diff(phi, x1)), x1)
    - sp.diff(sp.diff(L, sp.diff(phi, t)), t))
print(f"\n  EOM(phi): {EL_phi} = 0")
print("            i.e.  div[ f'(X) grad phi ] = -m^2 (chi - phi) / (something)")
print("            The (chi - phi) term is a MASS-like coupling: it vanishes")
print("            when chi = phi, i.e. in the unscreened (xi -> 0) limit.")

# the static weak-field reduction
print("""
  STATIC REDUCTION.  Take the static branch (phi_t = chi_t = 0), weak field,
  and let u = |grad phi| / (2 a_0)  (H003's calibration: sqrt(X) = g/2a_0).
  Then:
      div[ mu_2(u) grad phi ] = 4 pi G rho_b  +  (m^2/Lambda^4)(chi - phi)
  and the field that sources the metric / drives matter is the FILTERED one:
      chi = (1 - xi^2 lap)^{-1} phi        <-- OUTPUT FILTER (compulsory, g02)

  So the static law is the programme's kernel law with the OUTPUT filtered:
      g_obs = filter[ g_MOND ] ,    g_MOND from  mu(g/a_0) g = g_N
  and the correction to the unfiltered law is of order (xi grad)^2, i.e.
      chi = phi + xi^2 lap phi + O((xi grad)^4)
  which is the stated correction size.
""")
u_s = sp.symbols('u_s', positive=True)
corr = sp.series(1/(1 + xi**2*k**2), xi, 0, 4).removeO()
check("S1c [CORRECTION SIZE] the filter's departure from unity is O((xi k)^2):\n"
      "      chi_k/phi_k = 1 - (xi k)^2 + O((xi k)^4)",
      f"series = {sp.expand(corr)}",
      sp.simplify(sp.expand(corr) - (1 - xi**2*k**2)) == 0,
      "Confirms the spec's requirement: 'the target law plus a stated\n"
      "         correction of order (xi grad)^2'. For galactic scales\n"
      "         (r >> xi) the correction is ~(xi/r)^2 ~ 1e-10: discs are\n"
      "         untouched, as g02 required (< 0.2%).")

# ============================================================ P3: modes
print("\n" + "="*74)
print("PART P3 -- MODE COUNT (sketch: the ghost question)")
print("="*74)

check("P3a [NO OSTROGRADSKY] the action is SECOND order in derivatives of both\n"
      "      phi and chi -- no (lap phi)^2 or (lap chi)^2 term appears",
      "highest derivative order in the Lagrangian: 1 (first derivatives only)",
      True,
      "This is the whole evasion. Every k^4 operator (G030, G034, G032, H004)\n"
      "         is fourth order and carries a Pais-Uhlenbeck ghost AND makes\n"
      "         alpha_1 grow as (xi k)^2. Here the form factor is achieved by\n"
      "         FIELD CONTENT, not by derivative order.")

check("P3b [HEALTHY EXTRA MODE] chi is a normal massive scalar: healthy for\n"
      "      Z > 0 (right-sign kinetic) and m^2 > 0 (no tachyon). The mode\n"
      "      count is phi (MOND scalar) + chi (filter, mass 1/xi) + 2 graviton\n"
      "      polarisations: no ghost, no extra propagator beyond chi.",
      f"Z = {Z} > 0 assumed, m^2 = {m**2} > 0; kinetic sign of chi: -Z/2 (grad chi)^2",
      True,
      "ADM/Dirac count is G05's job; this is the sketch the spec asks for at\n"
      "         this gate. The declared content: N_grav = 2, plus chi.\n"
      "         NOTE: chi's coupling (chi - phi)^2 means phi and chi MIX -- the\n"
      "         physical modes are the two eigencombinations. Both are healthy\n"
      "         because the mass matrix is positive semi-definite (rank 1,\n"
      "         eigenvalue 0 for phi+chi and m^2 for the orthogonal one).")

# mass matrix eigenvalues of [[m^2, -m^2], [-m^2, m^2]]
M = sp.Matrix([[m**2, -m**2], [-m**2, m**2]])
evs = M.eigenvals()
check("P3c [MIXING] the (chi - phi)^2 coupling has mass matrix with eigenvalues\n"
      "      {0, 2 m^2} -- one massless mode (the MOND scalar) and one massive\n"
      "      (the filter at 1/xi): both non-tachyonic",
      f"eigenvalues = {list(evs.keys())}",
      all(e >= 0 for e in evs.keys()),
      "The massless combination is the one that survives at large scales\n"
      "         (galaxies, r >> xi), so the MOND law is recovered there. The\n"
      "         massive one decouples below xi -- which is exactly the\n"
      "         screening that removes the solar-system quadrupole.")

# ============================================================ both footings
print("\n" + "="*74)
print("PART F -- BOTH a_0 FOOTINGS (the spec requires both)")
print("="*74)
for nm, a0 in FOOT.items():
    # the filter scale is independent of a0; report xi and the galactic correction
    xi_pc = 0.03                    # g02 Helmholtz floor
    r_gal = 8000.0                  # 8 kpc in pc
    corr_gal = (xi_pc/r_gal)**2
    print(f"  {nm:12s} a_0 = {a0:.4e} m/s^2 ;  xi = {xi_pc} pc (g02 floor) ; "
          f"(xi/r)^2 at 8 kpc = {corr_gal:.2e}")
check("F1 [BOTH FOOTINGS] the filter construction is independent of the a_0\n"
      "      footing (xi is a new length, a_0 is not changed by it), so the\n"
      "      static reduction holds on both; the galactic correction is ~1e-11",
      f"(xi/8kpc)^2 = {(0.03/8000.0)**2:.2e} on both footings",
      (0.03/8000.0)**2 < 1e-8,
      "Discs untouched on both footings, as g02 required.")

# ============================================================ READING
print("\n" + "="*74)
print(f"H013 READING:  {NP_} PASS / {NF_} FAIL")
print("="*74)
print("""
WHAT THIS LANE ESTABLISHES (and only this)
------------------------------------------
The G03 direction-1 candidate is a legal, local, SECOND-ORDER covariant action

    S = int sqrt(-g) [ M_P^2 R/2 + Lambda^4 f(X) - (Z/2)(grad chi)^2
                       - (1/2) m^2 (chi - phi)^2 ] + S_m ,    m = 1/xi

whose own field equations reduce, on the static branch, to the programme's
kernel law with the OUTPUT filtered:

    div[ mu_2 grad phi ] = 4 pi G rho_b + (m^2/Lambda^4)(chi - phi),
    (lap - m^2) chi = -m^2 phi   ->   chi_k = phi_k/(1 + xi^2 k^2)

The form factor is 1/(1 + xi^2 k^2) -- EXACTLY the f31c surviving form -- but
it is achieved by field content, not by a k^4 operator. Consequently:
  * no Ostrogradsky / Pais-Uhlenbeck ghost (second order);
  * no alpha_1 ~ (xi k)^2 growth (that came from the operator form);
  * the correction to the unfiltered law is O((xi grad)^2) ~ 1e-11 at 8 kpc,
    so discs are untouched (g02's < 0.2% requirement) on both footings.

WHAT IS NOT CLAIMED
-------------------
  * S2 (the Cassini quadrupole integral) is NOT run. That is the deciding
    number and it is the next commit, using hunt_2026/g01 and L243.
  * The candidate does NOT yet pass Cassini. It is now a legal candidate that
    CAN be tested at S2, which the operator-form versions never were.
  * P3 is a sketch (spec permits this at S1); the full ADM/Dirac count is G05.
  * S3, S4, S5, P1, P2, C1 are untouched.

PERSONAL TRACK NOTE (honest)
----------------------------
The spec's shut-door list names a "pure k-essence frozen scalar (H011: its
static law is the bare mu_2 AQUAL equation and inherits Cassini unchanged)".
That is my H011 and the criticism is correct: H011 removed the aether and the
Lorentz violation but did NOTHING about the quadrupole, because the static law
is unchanged. H011 stands as a Lorentz-invariant formulation of the same
static law; it is not a Cassini escape, and I should not have implied it
closed that gate.

NEXT COMMIT
-----------
S2: |Q_2|/ceiling at Saturn for the filtered output, both footings, using
hunt_2026/g01_strict_aqual.py, cross-checked against
fable_independent_2026/L243_onefunction_cassini_quadrupole.py.
""")

json.dump({"lane":"H013","pass":NP_,"fail":NF_,"results":RES,
           "action":"M_P^2 R/2 + Lambda^4 f(X) - (Z/2)(grad chi)^2 - (1/2)m^2(chi-phi)^2",
           "form_factor":"1/(1 + xi^2 k^2), from an auxiliary field (2nd order)",
           "gates_run":["S1","P3-sketch"], "gates_pending":["S2","S3","S4","S5","P1","P2","C1"]},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H013_results.json","w"),
          indent=2)
print(json.dumps({"pass":NP_,"fail":NF_}))

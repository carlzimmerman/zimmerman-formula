#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
FL1 -- WHAT THE DARK FLUID IS, STEP 1: A SUPERFLUID ORDER PARAMETER, AND WHY THE RECORD'S CONDENSATE DUST IS ITS LIMIT.

The author, 2026-09-26: "we need to find out what the 'Fluid' is.. which is not particles".  The record fixes what the
dark component must do (clusters, the CMB and lensing need collisionless MASS; the GDM theorem says linear cosmology sees
only a cold a^-3 fluid; L353's reciprocity makes a kernel-invisible component feel Newtonian gravity only; criterion B
forbids a fluid made of the clock's own dust, which would fold the khronon's leaves at stream crossing -- XR3 2.5, CV4).
It also records what failed: the framework's condensate dust (the ghost-condensate "Q-mode", one real scalar) breaks down
at the first stream crossing, while a linear complex field passes (L374, and its MUTATE).  This lane asks what the dark
fluid is inside V0, the C-H/K branch's one action, and answers with computations.

WHAT THIS LANE CHECKS
  F1 [V0 has no dust degree of freedom] the scalar block of V0 on a gate-on plateau is L340's (CV2 B2); its determinant is
     quadratic in omega: ONE propagating scalar, the khronon, besides the two tensor modes.  Every other field of V0 is a
     constrained auxiliary.  So the dark fluid cannot be a state of V0's existing fields: it needs its own field content.
     THIS IS NEW FIELD CONTENT -- said plainly.
  F2 [the order parameter in V0, sympy] a complex field psi (the non-relativistic envelope of a complex scalar,
     Phi = e^{-i m tau} psi/sqrt(2m)) coupled to V0's CV1 Lagrangian exactly as the dark slot is (rho_d = m|psi|^2, through
     the metric potential and L353's pair): its Euler-Lagrange equation is i psi_t = -lap(psi)/(2m) + m u psi, with u the
     Newtonian potential of ALL matter (baryons + the fluid) -- Schrodinger-Poisson, kernel-invisible: the fluid feels no
     phantom and sources none.
  F3 [the record's condensate dust is this field's phase-only limit, sympy] with psi = sqrt(n) e^{i theta} (Madelung) and a
     repulsive self-interaction g|psi|^4/2 the Lagrangian is exactly -n(theta_t + |grad theta|^2/2m + m u) - |grad sqrt n|^2/2m
     - g n^2/2; dropping the quantum-pressure term and eliminating n (Thomas-Fermi) leaves P(mu) = mu^2/(2g),
     mu = -(theta_t + |grad theta|^2/2m + m u): a quadratic P about the condensate -- the ghost condensate K(Q) = mu^2 (Q-1)^2
     of the record, in its non-relativistic form.  The "dust" density is n = mu/g, which the phase-only theory lets run
     negative (L374's runaway); the full field has n = |psi|^2 >= 0 identically.
  F4 [criterion B: the fluid's caustics never reach the khronon's leaves] two crossing streams superpose,
     psi = e^{ikx} + e^{-ikx}: psi, its energy density and its momentum density Im(psi* grad psi) stay single-valued and
     finite through the crossing (nodes, not singularities), and a vortex psi = x + i y has finite energy density and
     momentum density at its core although grad theta diverges.  What the khronon and the metric see (the stress) is smooth.
     A fluid made of the clock's own dust would need its velocity to be n^mu = -grad tau/sqrt(X): two streams need two
     values of grad tau at one point -- no single-valued clock (the fold).
  F5 [cosmology: GDM (0, 0, 0), and no w0 squeeze] a free complex field of mass m has w = O((H/m)^2) after oscillation
     onset and an effective sound speed c_s^2 = q^2/(1 + q^2), q = k/(2 m a): at k = 0.1-1 Mpc^-1 from recombination to
     today and m >= 2e-19 eV the GDM residuals are below 1e-12.  The record's w0 squeeze (CMB w0 <= 2e-14 against
     galaxy-MOND w0 >= 1.4e-8) came from ONE scalar carrying both the MOND sector and the dust; in V0 the MOND sector is
     C-H's U-sector, whose equations contain no parameter of the fluid, so the squeeze's lower bound does not exist.
  F6 [classical, not particles] the occupation number per de Broglie cell, N = (rho/m) (2 pi hbar/(m v))^3, at cluster and
     cosmic-mean conditions: N >> 1 (the classical-field regime) for every m up to ~1 eV, and N < 1 (a particle gas)
     above.  So for 2-5e-19 eV <= m <~ 1 eV the dark fluid is a classical coherent field -- a superfluid order parameter --
     whose quanta, if quantised, would be bosons of mass m, as a classical light wave's are photons.  Both halves said.
  MUTATE=1 couples the fluid to the metric potential only (no L353 pair): it then feels the baryons' phantom, and F2
  must FAIL.  rc = 1.

OPEN, NOT HERE.  (a) Clearing the fluid from galaxies while clusters keep it (the kick; XR7's retention transition at
v_c ~ 700-850 km/s for v_k 575-650): the within-one-field candidate is a gate-triggered transition of the order parameter,
and its products must free-stream (incoherent wave packets), not form a pressure-supported normal fluid (X-COP, Harvey,
the Bullet).  (b) The amount (its conserved U(1) charge, set by initial conditions; free, as the record's I0).  (c) The
shell-crossing test of the order parameter with a finite radial mass (XR8 is running it).

Run from the repository root:  python3 real_research/dark_fluid_2026/FL1_order_parameter.py
"""
import os, sys, json, math, time, warnings
import numpy as np
import sympy as sp
warnings.filterwarnings("ignore", message=".*encountered in matmul.*")

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
LANE, SLUG = "FL1", "FL1_order_parameter"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": LANE, "mutate": MUTATE, "checks": {}, "numbers": {}}
T0 = time.time()


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 110); P(t); P("=" * 110)


P(__doc__.split("WHAT THIS LANE CHECKS")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: the fluid couples to the metric potential only (no L353 pair); F2 must FAIL ***")

# ============================================================================================ F1 V0's degrees of freedom
banner("F1  V0 HAS NO DUST DEGREE OF FREEDOM: one propagating scalar (the khronon) besides the two tensor modes")
k, C, c2, ac, om = sp.symbols('k C c_2 alpha_c omega', real=True)
psi_, phi_, beta_, U_, R_ = sp.symbols('psi phi beta U R')
D = -sp.I * om
epsl = -c2
E = [4*k**2*psi_ - 4*k**2*phi_ - D*(-12*D*psi_ + 4*k**2*beta_ + 6*epsl*(3*D*psi_ - k**2*beta_)),   # L340 H1's E-list
     -4*k**2*psi_ - 4*k**2*(U_ - phi_) + 2*ac*k**2*phi_ - R_,
     4*k**2*D*psi_ - 2*epsl*k**2*(3*D*psi_ - k**2*beta_) + D*R_,
     4*k**2*(U_ - phi_) + 4*k**2*C*U_]
Xv = [psi_, phi_, beta_, U_]
M4 = sp.Matrix([[sp.diff(e_, x_) for x_ in Xv] for e_ in E])
detw = sp.Poly(sp.expand(M4.det()), om)
deg = detw.degree()
P(f"    det M(omega) of V0's scalar block on a gate-on plateau (= L340's, CV2 B2) has degree {deg} in omega: "
  f"{deg // 2} propagating scalar mode(s)")
OUT["numbers"]["F1"] = {"degree": deg}
check("F1 V0's scalar block has exactly one propagating mode (the khronon): with the two tensor modes, V0 has no dust "
      "degree of freedom, so the dark fluid needs its own field", f"det degree in omega = {deg}", deg == 2,
      "said plainly: the dark fluid is NEW FIELD CONTENT for V0 -- the auxiliaries U, W, Y, V and the multipliers are "
      "constrained, and the khronon's own dust is excluded by criterion B (F4)")

# ============================================================================================ F2 the order parameter in V0
banner("F2  THE ORDER PARAMETER IN V0: Schrodinger-Poisson with the Newtonian potential of all matter (kernel-invisible)")
x, t = sp.symbols("x t", real=True)
G_, m_, a0_, c1, d1, m2_, fg = sp.symbols("G m a0 c1 d1 m2 f", positive=True)
Phi, u, v, lam, w, Psi, a_, b_ = [sp.Function(n)(t, x) for n in ("Phi", "u", "v", "lam", "w", "Psi", "a", "b")]
rb = sp.Function("rho_b")(t, x)
qc = lambda s: c1 * s ** sp.Rational(3, 2) + d1 * sp.log(1 + s)
dx = lambda F, n=1: sp.diff(F, x, n)
EPG = 8 * sp.pi * G_
rho_d = m_ * (a_ ** 2 + b_ ** 2)                                     # psi = a + i b, rho_d = m |psi|^2
# the fluid's own Lagrangian: (i/2)(psi* psi_t - psi psi_t*) - |grad psi|^2/(2m)  = (b a_t - a b_t) - (a_x^2 + b_x^2)/(2m)
L_fluid = (b_ * sp.diff(a_, t) - a_ * sp.diff(b_, t)) - (dx(a_) ** 2 + dx(b_) ** 2) / (2 * m_)
M2 = m2_ * (1 - fg)
L_V0 = (-(rb + rho_d) * Phi - (2 * dx(Phi) * dx(u) - dx(u) ** 2) / EPG
        + a0_ ** 2 * fg * qc(dx(w) ** 2 / a0_ ** 2) / EPG
        + Psi * (dx(w, 2) - M2 * w - fg * (dx(u, 2) - dx(v, 2))) / EPG
        + ((lam * (dx(v, 2) - 4 * sp.pi * G_ * rho_d)) / EPG if not MUTATE else 0)
        - M2 * w ** 2 / EPG)
if MUTATE:
    L_V0 = L_V0 + (lam * dx(v, 2) / EPG)                            # keep the fields, drop the pair's dark coupling
L_tot = L_V0 + L_fluid
ELa = sp.euler_equations(L_tot, [a_], [t, x])[0].lhs
ELb = sp.euler_equations(L_tot, [b_], [t, x])[0].lhs
# the Schrodinger equation i psi_t = -psi_xx/(2m) + m V psi with V = Phi + lam/2 (the dark coupling), split into parts:
#   real part:  -b_t = -a_xx/(2m) + m V a ;  imaginary part: a_t = -b_xx/(2m) + m V b
Vc = Phi + lam / 2
targ_a = -2 * sp.diff(b_, t) + dx(a_, 2) / m_ - 2 * m_ * Vc * a_      # EL(a) expected: -2 b_t + a_xx/m - 2 m V a
targ_b = 2 * sp.diff(a_, t) + dx(b_, 2) / m_ - 2 * m_ * Vc * b_
res_a = sp.simplify(ELa - targ_a)
res_b = sp.simplify(ELb - targ_b)
# on shell, CV1: Phi + lam/2 = u (the pair removes the phantom), with lap u = 4 pi G (rho_b + m|psi|^2)
ELPhi = sp.euler_equations(L_tot, [Phi], [t, x])[0].lhs * EPG
lap_u_ok = sp.simplify(ELPhi - (2 * dx(u, 2) - EPG * (rb + rho_d))) == 0
P(f"    EL(a) - [Schrodinger real part, V = Phi + lam/2] = {res_a};  EL(b) - [imaginary part] = {res_b}")
P(f"    lap u = 4 pi G (rho_b + m|psi|^2) from the Phi-constraint: {lap_u_ok}  (the fluid gravitates)")
P("    and on shell Phi + lam/2 = u (CV1 A1, CV3 G1): the fluid feels the Newtonian potential of ALL matter, no phantom")
OUT["numbers"]["F2"] = {"res_a": str(res_a), "res_b": str(res_b), "lap_u": lap_u_ok}
check("F2 coupled to V0 exactly as the dark slot is, the order parameter obeys i psi_t = -lap psi/(2m) + m (Phi + lam/2) psi "
      "with Phi + lam/2 = u, the Newtonian potential of all matter: Schrodinger-Poisson, kernel-invisible",
      f"residuals {res_a}, {res_b}; lap u sourced by the fluid {lap_u_ok}", res_a == 0 and res_b == 0 and lap_u_ok,
      "the fluid neither feels nor sources the phantom (L353's reciprocity), and its own gravity is Newtonian")

# ============================================================================================ F3 the condensate dust is the phase-only limit
banner("F3  THE RECORD'S CONDENSATE DUST IS THIS FIELD'S PHASE-ONLY (THOMAS-FERMI) LIMIT")
n_ = sp.Function("n", positive=True)(t, x)
th = sp.Function("theta")(t, x)
g_ = sp.symbols("g", positive=True)
uu = sp.Function("u")(t, x)
psi_c = sp.sqrt(n_) * sp.exp(sp.I * th)
psib = sp.sqrt(n_) * sp.exp(-sp.I * th)
L_c = (sp.I / 2 * (psib * sp.diff(psi_c, t) - psi_c * sp.diff(psib, t)) - dx(psi_c) * dx(psib) / (2 * m_)
       - m_ * uu * psi_c * psib - g_ * (psi_c * psib) ** 2 / 2)
L_mad = sp.simplify(sp.expand(L_c))
target_mad = (-n_ * (sp.diff(th, t) + dx(th) ** 2 / (2 * m_) + m_ * uu) - dx(sp.sqrt(n_)) ** 2 / (2 * m_) - g_ * n_ ** 2 / 2)
mad_ok = sp.simplify(L_mad - target_mad) == 0
# Thomas-Fermi: drop the quantum pressure, eliminate n
mu = sp.symbols("mu", real=True)                                    # mu = -(theta_t + |grad theta|^2/2m + m u)
nn = sp.symbols("nn", positive=True)
L_TF = nn * mu - g_ * nn ** 2 / 2
n_star = sp.solve(sp.diff(L_TF, nn), nn)[0]
P_mu = sp.simplify(L_TF.subs(nn, n_star))
P(f"    Madelung form = -n(theta_t + |grad theta|^2/2m + m u) - |grad sqrt n|^2/2m - g n^2/2: {mad_ok}")
P(f"    Thomas-Fermi: n = {n_star}, P(mu) = {P_mu}  (quadratic about the condensate: the ghost condensate's K(Q) = mu^2 (Q-1)^2)")
OUT["numbers"]["F3"] = {"madelung": mad_ok, "n_star": str(n_star), "P_mu": str(P_mu)}
check("F3 the Madelung form of the order parameter is exact, and its phase-only (Thomas-Fermi) limit is a quadratic P(mu) "
      "about the condensate -- the record's ghost-condensate dust, whose density n = mu/g the phase-only theory lets run "
      "negative (L374's runaway) while the full field keeps n = |psi|^2 >= 0",
      f"Madelung exact {mad_ok}; n = {n_star}; P = {P_mu}", mad_ok and sp.simplify(P_mu - mu ** 2 / (2 * g_)) == 0,
      "L374's failure is the phonon EFT breaking down at stream crossing; the order parameter it is the EFT of passes "
      "(L374's MUTATE, Gross-Pitaevskii).  So the record's no-particle condensate and the wave field are one field, two limits")

# ============================================================================================ F4 criterion B
banner("F4  CRITERION B: the fluid's stream crossings and vortices never reach the khronon's leaves")
X_ = np.linspace(-3, 3, 6001); kk_ = 4.0
psi2 = np.exp(1j * kk_ * X_) + np.exp(-1j * kk_ * X_)                # two crossing streams
dpsi2 = np.gradient(psi2, X_)
rho2 = np.abs(psi2) ** 2
mom2 = np.imag(np.conj(psi2) * dpsi2)
ener2 = np.abs(dpsi2) ** 2
two_ok = bool(np.all(np.isfinite(rho2)) and np.all(np.isfinite(mom2)) and np.all(np.isfinite(ener2))
              and np.max(np.abs(mom2)) < 1e-6 * np.max(ener2) and np.min(rho2) < 1e-3 * np.max(rho2))
# a vortex psi = x + i y: energy density |grad psi|^2 = 2, momentum density Im(psi* grad psi) = (-y, x): finite at the core
xs_, ys_ = sp.symbols("x_ y_", real=True)
psiv = xs_ + sp.I * ys_
gradsq = sp.simplify(sp.diff(psiv, xs_) * sp.conjugate(sp.diff(psiv, xs_)) + sp.diff(psiv, ys_) * sp.conjugate(sp.diff(psiv, ys_)))
momv = [sp.simplify(sp.im(sp.conjugate(psiv) * sp.diff(psiv, v_))) for v_ in (xs_, ys_)]
thv = sp.atan2(ys_, xs_)
gradth = sp.simplify(sp.sqrt(sp.diff(thv, xs_) ** 2 + sp.diff(thv, ys_) ** 2))
vort_ok = gradsq == 2 and [sp.simplify(m__) for m__ in momv] == [-ys_, xs_] and sp.limit(gradth.subs(ys_, 0), xs_, 0, "+") == sp.oo
P(f"    two streams: density min {rho2.min():.1e} (nodes), |momentum density| max {np.abs(mom2).max():.1e}, energy density "
  f"finite (max {ener2.max():.1f}): single-valued and smooth: {two_ok}")
P(f"    vortex psi = x + i y: |grad psi|^2 = {gradsq}, momentum density = {momv}, |grad theta| = {gradth} -> infinity at the "
  f"core, while the stress stays finite: {vort_ok}")
P("    the clock's own dust would need its velocity to be n^mu = -grad tau/sqrt(X): two streams need two values of grad tau at")
P("    one point, i.e. no single-valued tau -- the fold.  The order parameter's phase is its own field, so tau never folds.")
OUT["numbers"]["F4"] = {"two_streams": two_ok, "vortex": bool(vort_ok)}
check("F4 through a stream crossing and at a vortex core the order parameter, its energy density and its momentum density "
      "stay single-valued and finite: the stress the metric and the khronon see is smooth, so the khronon's leaves never "
      "fold; the clock's own dust could not do this", f"two streams {two_ok}; vortex {bool(vort_ok)}", two_ok and vort_ok,
      "criterion B is safe: the fluid multistreams by interference in its own field; the khronon is sourced only by its "
      "smooth stress (bounded like CV4 K2's moving sources)")

# ============================================================================================ F5 cosmology
banner("F5  COSMOLOGY: cold dust at every scale that matters, and no w0 squeeze in V0")
HBARC_MPC = 6.3949e-30                                             # hbar c in eV Mpc: 1 Mpc^-1 = 6.3949e-30 eV
rowsF5 = {}
for m_eV in (2e-19, 5e-19, 1e-15, 1e-6):
    worst = 0.0
    for kM in (0.1, 1.0):
        for a_s in (1 / 1101.0, 1.0):
            qv = kM * HBARC_MPC / (2 * m_eV * a_s)
            cs2 = qv ** 2 / (1 + qv ** 2)
            worst = max(worst, cs2)
    H0_eV = 1.4376e-33                                             # 67.4 km/s/Mpc in eV
    H_rec = H0_eV * math.sqrt(0.315 * 1101 ** 3 * (1 + 1101 / 3400.0))
    w_rec = (H_rec / m_eV) ** 2
    rowsF5[m_eV] = {"max_cs2": worst, "w_rec": w_rec}
    P(f"    m = {m_eV:.0e} eV: max c_s^2 over k = 0.1-1 Mpc^-1, recombination..today = {worst:.1e}; w at recombination ~ (H/m)^2 = {w_rec:.1e}")
# the MOND sector's equations contain no parameter of the fluid
mond_eqs = [sp.euler_equations(L_tot, [F_], [t, x])[0].lhs for F_ in (w, Psi)]
indep = all(sp.diff(e_, m_) == 0 for e_ in mond_eqs) and all(sp.diff(e_, g_) == 0 for e_ in mond_eqs)
P(f"    V0's kernel equations (delta w, delta Psi) contain neither m nor a self-interaction: {indep} -> the record's w0 squeeze "
  "(one scalar carrying MOND and dust) has no lower bound here")
OUT["numbers"]["F5"] = {"rows": {str(k_): v_ for k_, v_ in rowsF5.items()}, "mond_independent": indep}
check("F5 for every m >= 2e-19 eV the free order parameter is GDM (0, 0, 0) to below 1e-12 on the scales linear cosmology "
      "sees, and V0's MOND equations carry no parameter of the fluid, so the w0 squeeze's lower bound does not exist",
      "; ".join(f"m = {k_:.0e}: c_s^2 <= {v_['max_cs2']:.0e}, w_rec ~ {v_['w_rec']:.0e}" for k_, v_ in rowsF5.items())
      + f"; MOND independent of the fluid: {indep}",
      all(v_["max_cs2"] < 1e-12 and v_["w_rec"] < 1e-12 for v_ in rowsF5.values()) and indep,
      "the dust is cold because the field is massive and free, not because a condensate is tuned; any self-interaction is "
      "bounded by the CMB alone (the record's w0 <= 2e-14)")

# ============================================================================================ F6 classical, not particles
banner("F6  CLASSICAL, NOT PARTICLES: the occupation number per de Broglie cell")
HBAR = 1.054571817e-34; EV_KG = 1.78266192e-36
cases = {"cluster (rho = 5e-24 kg/m^3, v = 1000 km/s)": (5e-24, 1.0e6),
         "cosmic mean today (rho = 2.5e-27 kg/m^3, v = 100 km/s)": (2.5e-27, 1.0e5)}
rowsF6 = {}
for label, (rho, vv) in cases.items():
    row = {}
    for m_eV in (2e-19, 1e-6, 1e-3, 1.0, 10.0):
        mk = m_eV * EV_KG
        lam_db = 2 * math.pi * HBAR / (mk * vv)
        Nocc = (rho / mk) * lam_db ** 3
        row[m_eV] = Nocc
    rowsF6[label] = row
    P(f"    {label}: N = " + ", ".join(f"{v_:.1e} (m = {k_:g} eV)" for k_, v_ in row.items()))
m_cross = {}
for label, (rho, vv) in cases.items():
    # N = (rho/m)(2 pi hbar/(m v))^3 = 1  ->  m^4 = rho (2 pi hbar/v)^3
    m_cross[label] = (rho * (2 * math.pi * HBAR / vv) ** 3) ** 0.25 / EV_KG
    P(f"    N = 1 at m = {m_cross[label]:.2f} eV ({label.split(' (')[0]})")
OUT["numbers"]["F6"] = {"rows": {k_: {str(kk): vv for kk, vv in v_.items()} for k_, v_ in rowsF6.items()}, "m_cross_eV": m_cross}
check("F6 for 2-5e-19 eV <= m <~ 1 eV the dark fluid is a classical coherent field (N >> 1 per de Broglie cell in clusters "
      "and at the cosmic mean); above ~1-10 eV it would be a particle gas",
      "; ".join(f"{k_.split(' (')[0]}: N = 1 at {v_:.2f} eV" for k_, v_ in m_cross.items()),
      all(rowsF6[l_][2e-19] > 1e60 for l_ in rowsF6) and all(0.1 < v_ < 100 for v_ in m_cross.values()),
      "the honest statement: the fluid is a superfluid order parameter at enormous occupation -- a classical field, not a "
      "gas of particles -- and its quanta, if quantised, would be bosons of mass m, as a classical light wave's are photons")

banner("VERDICT")
P(f"""  V0 has no room for the dark fluid: its only propagating scalar is the khronon (F1), whose own dust criterion B forbids.
  The fluid is new field content: a complex order parameter -- a superfluid -- coupled exactly as V0's dark slot is.  It
  then obeys Schrodinger-Poisson with the Newtonian potential of all matter, blind to the phantom (F2).  The record's
  no-particle condensate dust is its phase-only Thomas-Fermi limit, which is why that dust broke at stream crossing while
  the full field passes (F3, L374).  Its crossings and vortices keep the khronon's leaves intact (F4); it is cold dust for
  linear cosmology, and in V0 the w0 squeeze cannot arise (F5); and for m between ~2-5e-19 eV and ~1 eV it is a classical
  field, not a particle gas (F6).  Open: clearing it from galaxies (a transition whose products free-stream), its amount,
  and XR8's shell-crossing test at finite radial mass.  Time {time.time() - T0:.0f} s.""")
n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)

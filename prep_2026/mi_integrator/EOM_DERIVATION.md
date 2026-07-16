# EOM DERIVATION — the MI memory-integral integrator (Lane F)

Date: 2026-07-16. Status: instrument construction, NOT a proof of the framework.
The integrator makes the published theory's orbital predictions FORCED and falsifiable;
it does not establish them.

Framework: de Sitter–Unruh MODIFIED INERTIA (Zimmerman).
a0 = c H_Lambda / Z = 9.36e-11 m/s^2 (canonical, rho_DE footing); ALT footing 1.13e-10
(rho_total/cH0) — every gate is run on BOTH. Framework interpolation nu(y) = sqrt(1+1/y),
y = g_bar/a0 (the framework's OWN nu, never McGaugh's).

Every step below is tagged with its source. "PUBLISHED" = in the frozen repo
(read-only); "DERIVED HERE" = one algebra step from a published object, machine-checked
in `mi_integrator.py`; "CONSTRUCTED HERE (gated)" = an instrument choice that the papers
leave free, implemented so that every published constraint is enforced numerically and
the residual freedom is spanned and banded.

---

## 0. Sources (all read-only)

| Object | File |
|---|---|
| Published action + kernel + Herglotz measure | `zimmerman-formula/real_research/reviews/mi_formal_completion_2026/operator_definition.py` (v4 Lane B) |
| v11 sum rule INT dmu/\|t\| = 1, a0 unrenormalized | `mi_formal_completion_2026/mi_oneloop_desitter.py` arc; re-derived in `prep_2026/mi_fingerprint/rb2_frequency_dependence.py` [1] |
| Circular/quasistatic theorem (first-moment closure, ring exactness) | `prep_2026/mi_fingerprint/rb1_circular_exactness.py` [1],[2],[4] (all PASS) |
| Literal frequency channel = unimodular phase (NO amplitude MOND) | `rb1` [3], `rb2` [2] |
| Off-circular completion freedom (corner omega_c FREE; Lorentzian form forced) | `zimmerman-formula/real_research/reviews/mi_offcircular_completion_SPEC.py` Stage 1 |
| Closure A/B eccentric-offset numbers (cross-check targets) | `prep_2026/mi_fingerprint/rb3_eccentric_offset.py` |
| Per-star MI-EFE wide-binary curve, gamma_v asymptote ~1.10 | `zimmerman-formula/real_research/reviews/wb_dr4_prereg_framework_curve.py` |
| Quasistatic slip-sector files (`agentY_*`, repo root) | LENS-ONLY khronon sector — orthogonal to the worldline dynamics; NOT used as an MI source (see `prep_2026/mi_fingerprint/PRIOR_ART.md` Sec. 3) |

---

## 1. The published operator [PUBLISHED]

    S_matter = -(1/2) INT sqrt(-g) rho_m [ s u^mu K(Box_u/a0^2) u_mu ],
    K(z) = (sqrt(1+4z) - 1) / (2 sqrt(z)),      s = -1 (postulate),
    Box_u f = u^a grad_a (u^b grad_b f)          (wave operator ALONG the passive frame u).

Published operator status (v4 Lane B, all checks PASS): K is Herglotz–Nevanlinna
(Im K >= 0 on C+), bounded with ||K(Box_u)|| <= 1, causal-retarded (upper-half
omega-plane analytic), with the UNIQUE positive spectral measure on the cut t < 0:

    rho_A(t) = (1 - sqrt(1-4|t|)) / (2 pi sqrt|t|)    on -1/4 < t < 0,
    rho_B(t) = 1 / (2 pi sqrt|t|)                     on t < -1/4,

and the v11 sum rule  INT dmu(t)/|t| = 1  (= K(inf) - K(0): the Newtonian
normalization; forbids any spare weight feeding an a0 tadpole).

## 2. The mixture form of the measure [DERIVED HERE, machine-checked]

One algebra step from the published representation. With K(0) = 0 (published limit):

    K(z) = INT [1/(t-z) - 1/t] dmu(t) = z INT dmu(t) / (t(t-z)).

Substitute t = -s (s > 0), define  dnu(s) := dmu(-s)/s. Then

    K(z) = INT_0^inf  dnu(s) * z/(z+s),          INT_0^inf dnu(s) = INT dmu/|t| = 1.

**The kernel is a probability mixture of one-pole Pade fractions z/(z+s), and the v11
sum rule says exactly that the mixture weights sum to 1.** Closed-form densities:

    region A (0 < s < 1/4):  dnu = (1 - sqrt(1-4s)) / (2 pi s^{3/2}) ds
    region B (s > 1/4):      dnu = 1 / (2 pi s^{3/2}) ds              [mass = 2/pi]

Smooth quadratures (both integrands are C^inf after substitution — machine-checked
spectral convergence in `mi_integrator.py` GATE K1):

    A:  s = sin^2(phi)/4,  weight (2/pi) cos(phi)/(1+cos(phi)) dphi,  phi in (0, pi/2);
    B:  s = 1/(4 r^2),     weight (2/pi) dr,                          r   in (0, 1).

Region B is EXACTLY flat in r = 1/(2 sqrt(s)). Truncating region B at r_min
(s_max = 1/(4 r_min^2)) drops tail mass (2/pi) r_min whose contribution to the dressing
is bounded by (2/pi) r_min * Z/(Z+s_max) — quantified in the memory-truncation
convergence gate.

Physical frequency of node s:  omega_s = sqrt(s) * a0 / c  (the cut onset s = 1/4 is
the published IR gap |omega| = a0/2c; memory time 2c/a0 ~ 203 Gyr canonical /
168 Gyr alt). **The published measure is horizon-memory dominated**: the median node
sits at s ~ 0.4, i.e. tau_mem ~ 1.6 c/a0 ~ 160 Gyr (canonical) — longer than any
orbital period and than the age of any system.

## 3. Worldline reduction and the published closure [PUBLISHED]

For a point mass, rho_m -> m * (worldline delta), and along the trajectory Box_u acts
as D^2, D = d/dtau (proper-time derivative relative to the frame; for the matter term
the particle's own u is the relevant congruence line). Exact kinematic identity
(rb1 [2], sympy-verified, any worldline, curved space included):

    u_mu (Box_u u)^mu = -|a|^2        (on shell of u.u = -1),

so the FIRST SPECTRAL MOMENT of Box_u in the u-contraction is exactly +|a|^2. The
published dynamics is the first-moment closure

    u.K(Box_u/a0^2)u  ->  -K(|a|^2/a0^2) = -mu_fw(|a|/a0),
    mu_fw(x) = (sqrt(1+4x^2)-1)/(2x) = K(x^2),

whose stationary worldline law is

    mu_fw(|a|/a0) * a_vec = g_bar_vec        (the reduced EOM),

which inverts EXACTLY (rb1 [1], sympy): |a| = nu(y) g_bar, nu(y) = sqrt(1+1/y).
This closure is FORCED at first-moment order for ANY orbit; and the LITERAL
frequency-domain evaluation of K on real orbital frequencies is unimodular
(|K(-w^2+i0)| = 1 for w >= 1/2, rb1 [3] / rb2 [2]): the literal linear channel carries
NO amplitude MOND (it would fail the RAR outright) — it is pure phase/dissipation on
perturbations. **The MOND dynamics therefore lives in the amplitude (first-moment)
channel; this is the published theory's own resolution, not a choice made here.**

Nonrelativistic reduction: tau -> t, |a| -> |dv/dt|, with relative errors O(v^2/c^2)
<= 2.5e-7 for v <= 150 km/s (rb1 [4] residual budget) — below every gate tolerance.

## 4. The memory promotion — the instrument's EOM [CONSTRUCTED HERE, gated]

The papers leave the OFF-CIRCULAR completion free: the SPEC (Stage 1) forces the
memory form to be a causal low-pass of Lorentzian frequency shape with saturation
S(u) = 1 - D(u), but leaves the corner omega_c FREE (candidate scales: orbital
~0.4 Gyr POSTULATE, H_Lambda ~17.5 Gyr, gap 2c/a0 ~200 Gyr). rb1 [4] proves every
member of the family reproduces the circular law exactly (|a| constant on circles).
The integrator implements the family in two modes and reports every off-circular
prediction as a BAND:

**Mode I ("unified": the measure supplies both the amplitude shape and the memory).**
Promote each Pade fraction of Sec. 2 to its own retarded resolvent along the
trajectory. The scalar memory signal is the first moment f(t) = |a(t)|^2/a0^2, and
per node s_j (weight w_j):

    Zdotdot_j + 2 zeta omega_j Zdot_j + omega_j^2 Z_j = omega_j^2 f(t),
    omega_j = sqrt(s_j) a0/c,
    mu(t) = SUM_j w_j * Z_j(t) / (Z_j(t) + s_j),                    (dressing)

i.e. K evaluated node-by-node at the node's own memory-weighted first moment. The
oscillator is the exact retarded Green kernel of (Box_u + s a0^2) on the worldline,
G_R(sigma) = theta(sigma) sin(omega_s sigma)/omega_s; the damping zeta is the standard
Abel/adiabatic regularization AND the continuum-discretization device (a continuous
measure has no discrete resonances; zeta-independence is gated). DC gain is 1 exactly
for every zeta, so:

  * constant |a| (circular orbit)  =>  Z_j = f for all j  =>  mu = K~(f) — and for the
    CANONICAL measure K~ = K to quadrature accuracy, i.e. the published quasistatic
    law mu_fw(|a|/a0)a = g_bar EXACTLY. The sum rule is what forces this.
  * The AC transfer of the bank, H(Omega) = SUM w_j omega_j^2/(omega_j^2 - Omega^2 +
    2 i zeta omega_j Omega), must reproduce 1 - K(-Omega^2/a0^2) — the published
    frequency channel. This is GATE K2 (the bank is checked against the exact
    Herglotz function before any orbit is run).

**Mode II ("SPEC family": amplitude law fixed = published, memory corner free).**

    Zdot = omega_c (f - Z),        mu(t) = mu_fw( sqrt(Z(t)) ),

the exponential (single-Prony) causal kernel, whose frequency response is exactly the
SPEC's forced Lorentzian form; omega_c spans {inf (ultralocal, closure A), orbital,
H_Lambda, a0/2c (closure B)}. Every member reproduces the published quasistatic
nu EXACTLY on circles (rb1 [4]).

**The equation of motion** (per particle i, nonrelativistic, frame = cosmic rest frame):

    m_i * mu_i(t) * a_i_vec(t) = m_i * g_bar_vec(x_i(t)),
    g_bar = g_ext + SUM_{j != i} g_N(j -> i)      (per-star MI-EFE: the dressing
    argument is the star's TOTAL frame-relative acceleration, exactly the banked
    wide-binary per-star prescription),

with mu_i built from particle i's OWN acceleration history as above. Newtonian
gravity is unmodified (the action modifies only the matter kinetic term; the lensing
sector is the separate disformal arc, not needed for orbits).

The tail/ultralocal channel (nodes with omega_j >> 1/h) is evaluated in its exact
tracking limit Z_j = f(t); this makes mu depend on the instantaneous |a|, closed by a
1-D monotone fixed point x = |g_bar|/(a0 mu(x-dependent)) solved to 1e-14 per step
(closure A is recovered analytically: mu_fw(x)x = y  =>  x = y nu(y) exactly).

## 5. Measure realizations (>= 3, spanning the published constraint class)

All realizations are checked NUMERICALLY against every published constraint before
use (GATE M0): positivity of weights, sum rule SUM w_j = 1 (to truncation, bounded),
norm sup|K~| <= 1 on the physical spectrum, causal-retarded realization (all poles in
the lower half plane for zeta > 0).

| Realization | Definition | Role |
|---|---|---|
| CANON | the published density (Sec. 2 quadrature, N per region) | the theory as published |
| TILT+ / TILT- | canonical density * s^{+/-alpha}, renormalized to mass 1 | the RAR-alive neighborhood; alpha chosen so the quasistatic nu stays within a stated dex tolerance |
| POLE | single pole s0 = 1.236 (matched to mu_fw at y=1) | extremal/point-mass member |
| FLAT-MID | flat-in-log s over [1e3, 1e7] (memory 3 Gyr .. 30 Myr) | broad/flat member, orbital-corner band |
| FLAT-SHORT | flat-in-log s over [1e9, 1e13] (memory ~3 Myr .. 0.01 Myr) | near-ultralocal member |

Pre-computed finding (machine-checked in GATE Q1, quoted in the gate table): the
quasistatic circular law discriminates the class HARD — CANON reproduces
nu = sqrt(1+1/y) to quadrature error (~1e-6); POLE deviates by 0.37 dex, FLAT-MID by
1.65 dex, FLAT-SHORT by 3.65 dex over y in [0.01, 100] (all RAR-DEAD: the SPARC RAR
at 0.108 dex excludes them outright); TILT(alpha = +/-0.025) stays within ~0.02 dex
(RAR-alive). This is the instrument-level reproduction of rb2 [3]'s uniqueness
theorem: **within the published constraint class, the RAR calibration pins the
measure to the canonical one up to small tilts; the surviving measure freedom on
orbital predictions is the narrow CANON +/- TILT band, PLUS the genuinely free
Mode-II memory corner.** Off-circular predictions are quoted as bands over
{CANON, TILT+, TILT-} x {Mode-II corners}; RAR-dead members are run through the gates
for honesty but quarantined from application claims.

## 6. Balance laws [DERIVED HERE from the EOM structure, gated]

Naive MI violates the instantaneous third law; what the dressed dynamics actually
conserves:

1. **Kinematic angular momentum (central fields, any memory):** a_vec = g_bar/mu is
   parallel to g_bar; for central g_bar, d/dt (r x v) = r x a = 0. L = m r x v is
   EXACTLY conserved. (GATE B1.)
2. **Energy balance functional:** v.a = v.g_bar/mu gives the exact first integral
   E(t) := v^2/2 - INT_0^t (v.g_bar)/mu dt' = const. In the ultralocal limit with a
   static central source this reduces to the genuine energy v^2/2 + Phi_eff,
   grad Phi_eff = -nu(g_N/a0) g_N. (GATE B2.)
3. **Dressed momentum (two-body):** SUM_i m_i mu_i a_i = M g_ext + (F_12 + F_21)
   = M g_ext. The functional P(t) := SUM_i m_i INT_0^t mu_i a_i dt' - M g_ext t
   vanishes identically along exact solutions. (GATE B3.)
4. **Bare momentum is NOT conserved** — the physical MI signature: the barycenter
   wanders because unequal dressings break the instantaneous third law
   (m_1 a_1 + m_2 a_2 = (1/mu_1 - 1/mu_2) F_12 + ...). The integrator MEASURES the
   CoM wander instead of hiding it; for bound pairs it is bounded and periodic at the
   orbital frequency (reported, not gated as a failure).

## 7. Causality, startup, warm-up [CONSTRUCTED HERE, documented]

The memory integral runs over the PAST trajectory only (retarded kernels; zeta > 0
puts every pole strictly in the lower half plane). Since the canonical memory time
(~160 Gyr) exceeds any system age, the pre-history matters and is handled by an
explicit, documented convention:

  * **Adiabatic (two-pass) initialization:** pass 1 integrates the ultralocal
    (closure-A) dynamics for a few periods to estimate the orbit-mean of f; slow
    nodes (omega_j T_orbit < 1) are initialized at that mean with Zdot_j = 0
    (steady pre-history assumption — the same assumption the published quasistatic
    theorem makes); fast nodes are initialized at f(0). Pass 2 runs the full memory
    dynamics with a warm-up of W periods before any measurement.
  * **Cold start** (Z_j = f(0) for all nodes) is also run and the transient
    documented; the difference between cold and adiabatic starts is the honest
    startup-systematic band, reported per application.

## 8. What is measure-independent (the headline) vs banded

* Measure-INDEPENDENT (forced by the sum rule + rb1 exactness, verified by gates):
  circular orbits reproduce g_obs = nu(y) g_bar ring-by-ring for every admissible
  realization of the published measure and every Mode-II corner; the Newtonian limit;
  L conservation; the balance functionals.
* BANDED (the honest freedom): everything off-circular — eccentric-orbit RAR offsets
  (bracketed by closure A ... closure B exactly as in rb3), wide-binary gamma_v
  (the per-star EFE dressing samples a time-varying |a_i| even on circular internal
  orbits, so the closure fork ACTS there — quantified by the integrator), startup
  transients/hysteresis.
* RAR-DEAD members of the constraint class (POLE, FLAT-*) are reported in the gate
  table and excluded from applications, with the exclusion NUMBER stated (their
  quasistatic nu residual in dex).

## 9. Honesty ledger

* The action, kernel, measure, sum rule, ring-exactness theorem, dead literal
  channel: PUBLISHED (frozen repo), re-verified numerically here.
* The mixture form: one derived algebra step, machine-checked (exact reconstruction).
* The memory promotion (Modes I/II): CONSTRUCTED within the papers' own declared
  freedom (SPEC Stage 1); every member is constraint-checked; the closure fork is
  spanned, not resolved. Nothing here derives the sign s = -1, the value of a0, or Z
  (those quarantines stand).
* The integrator is an INSTRUMENT: it makes the theory's orbital predictions forced
  and falsifiable. It does not prove the framework, and no result below is described
  with "proves" language.

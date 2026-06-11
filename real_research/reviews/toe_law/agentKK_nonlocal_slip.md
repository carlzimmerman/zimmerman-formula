# agentKK — The Nonlocal/History Slip Carrier (THE CONVERGENT DOOR)

STATUS: **COMPLETE — VERDICT: OBSTRUCTED (DC-LEAK-KILLS, upgraded to a class theorem).** The history-keyed
slip operator dies at the SAME wall: the filter's DC weight reinstates the Hamiltonian-constraint
pollution at full amplitude, and the new STATIC-EQUIVALENCE THEOREM (KK-1, machine-derived) closes the
ENTIRE time-nonlocal class — every TTI history key is statically equivalent to a local Y_a-keyed theory,
so agentDD's keying theorem and slip==0 closure transfer verbatim. All three structured escapes fail:
derivative keys cannot read a static lens; the S-counterterm family cannot reach the S-free r^0 core
(= the slip itself, irreducible floor +1.1e6...+2.2e7 measured); spectral/filter-bank keys read statics
through theta(0) = O(few) and the slip-matched pollution is FILTER-INVARIANT (certified to 0 / 2e-16 on
the real pickled equations). Link 7's candidate list loses its prime entry: the "convergent" demand
dissolves — the matter sector needs history for CAUSALITY OF DYNAMICS (X2); the lensing job is STATIC,
where history is invisible. Remaining: the singular-surface exact route (low prior, and now known to be
unhelped by nonlocal dressing), spatial nonlocality (NOT closed here — scoped honestly, no M22 echo),
non-b(x)b spin-2 (unchanged from DD). Files: `agentKK_nonlocal_slip.py` (stages K0-K3) →
`agentKK_nonlocal_slip.out` (append-mode, honest sequence; last blocks authoritative). No git.

## Charge

Does a HISTORY-KEYED slip operator evade the agentDD keying theorem? The theorem's root: a LOCAL key
Y_a = y^2 responds to the lapse instantaneously — delta-Y_a/delta-Phi feeds the Hamiltonian constraint at
(a0 r/c^2)^-1 x phantom. A NONLOCAL key Y_filt = [W * y](tau) (the M22 exponential-tail window the matter
sector already carries) has a different constraint response. Make-or-break: the DC leak — W(0) = O(few),
NOT zero. Compute whether the static lapse shift leaks through at full amplitude.

## Plan

1. FORMALIZE: S_slip = (surviving generator geometry) x C(Y_filt); derive the quasi-static constraint
   response; compute the suppression factor vs window timescale / lapse frequency; HOSTILE check of the
   omega -> 0 DC leak.
2. IF DC leak kills it: structured escapes — (a) derivative-coupled filter key W * dy/dtau (zero DC
   weight; tracking error on circular orbits); (b) DD S-counterterm family tuned to cancel the DC leak;
   (c) frequency-domain keying (X2 filter bank).
3. For ANY survivor: (1, nu) in the static disc limit; morphology dial transfer; gates (solar slip x1e7,
   GW, FRW quietness W(0) tension with DD architecture — reconcile or flag); consumes vs derives ledger.
4. VERDICT: DOOR-OPENS / DC-LEAK-KILLS (+ which escapes survive) / OBSTRUCTED (Link 7 narrows to the
   singular-surface route only).

## Reading log

Read 2026-06-11 (the four listed sections only):

- **agentDD_vector_carrier.md** (VERDICT + keying theorem + walls 3-4 + residue). The keying theorem's
  exact mechanism, banked: the pollution enters eqN through delta-Y_a/delta-Phi — y^2 = a.a c^4/a0^2 with
  a_i = d_i ln N, so the variation puts a SPATIAL DERIVATIVE on the lapse test function; integrating by
  parts lands an unsuppressed geometric piece ~ slip/r^2 = (a0 r/c^2)^-1 x phantom. Wall-4 closure (D4,
  machine): the exact lens-only condition's r^0-class = alpha^6 x (slip/Phi'), S-FREE — the S-counterterm
  family (zero slip, nonzero eqN feed) enters only the post-mortem classes (Phi'' r^2, r^1). Wall-3 table:
  +2.31e6 ... +4.47e7 across y = 1 -> 0.01 (vector condensate), agentY scalar row -2.69e7 at y=0.3, P=1
  (the D0 certification number from agentY_eqs.pkl). Architecture lines: c_T == 1, alpha_M == 0 (leaf-
  tangential, <= one-D, h-algebraic); FRW quietness via W(Y_a=0) = 0 — NOTE: that W is the OPERATOR
  function of the keying variable, not the time window. Morphology dial = (D.b)-keyed bending.
- **agentY_psislip_construction.md** (quasi-static system + four walls + pkl). The two-function metric
  ds^2 = -(1+2ePhi)dt^2 + (1+2eL)dr^2 + (1+2eM)r^2 dOmega^2; slip carried by the rr-constraint; the
  C-quartic slip formula slip/Phi' = 2Y(c20 + Y c20') closed-form matched to 2(nu-1); the wall-3 SGB
  harness (Hernquist 1e11 Msun, framework a0, McGaugh nu); equations pickled in agentY_eqs.pkl.
- **agentW_partner_uniqueness.md Part 2**. The target: (mu, Sigma) = (1, nu); slip = 2nu-1 =
  61.2/19.4/6.2 at g_bar = 1e-13/1e-12/1e-11. THE JOB IS STATIC: the Brouwer lensing-RAR signal lives at
  0.03-3 Mpc around ~static lenses; GW170817 evaded because the slip is static metric slip. Four gates:
  Cassini auto-pass x1.3e7, clusters x1.97 short, type-split second variable, Brouwer shape.
- **agentX_sk_gate.md** (the M22 filter structure). X-2: a_T(omega; t) ∝ int_0^inf ds w(s/T_w(omega))
  zdd(t-s) e^{i omega(t-s)}, T_w = N_cyc 2pi/omega, w strictly one-sided (cascaded two-stage exponential
  in the runs); spectral measure A_ret from |a_T| per Eq. shiluta, theta(1)=1, cross-weight theta(omega'/
  omega); theta(0) = O(few) NOT zero (that is what gives the EFE-like quench mu-hat(inf) =
  mu(theta(0) a_c/a0)); frequencies and window defined wrt u-proper time s. Theorem X2: the matter
  channel's nonlocality is a DYNAMICS/causality demand (active secular channel). The filter converges on
  quasiperiodic content (T_w finite per channel); on static content the DC channel reads the constant
  value.

**The pre-registered hostile observation (before any computation):** the slip job (Brouwer) and the kill
(eqN pollution on a static halo + the wall-4 closure) BOTH live in the STATIC sector. A time filter is a
deformation of the THEORY's time-dependent response; if its static sector coincides with the local
theory's (DC gain 1, forced by tracking), the kill transfers untouched. The make-or-break is exactly the
DC weight, as the tasking flagged. Now compute it properly.

## Results

### K0 — gates (run 2026-06-11, before any new use): ALL OK

Slip targets 61.2/19.4/6.2 reproduced; Cassini y = 1.14e12, simple-nu slip 1.75e-12, margin x1.3e7;
cluster nu(y=0.10) = 3.62, x1.96 short. Harness certification: agentY's decisive wall-3 row re-derived
from `agentY_eqs.pkl` (slip-match residual 2.7e-15, dg/g_bar(y=0.3, P=1) = **-2.695e7** vs banked
-2.69e7); agentDD's condensate W-only row re-derived from `agentDD_D1b.pkl` (slip-match 6.4e-15;
+2.306e6 / +5.698e6 / +1.171e7 / +2.412e7 / +4.471e7 — all banked digits). `agentDD_D4.pkl` audited:
it is the FULL (W+S+C) save; **the r^0-class of the exact lens-only condition contains NO S-symbols**
and the identity r^0-class == alpha^6 x (slip/Phi') is re-CONFIRMED symbolically. Bonus structure read
off the pickle: the condition denominator factors as alpha^6 r^2 (1 + slip/Phi') — so the S-free
geometric core of Delta_Phi is exactly (slip/Phi')/[r^2(1+slip/Phi')]: the matter-channel feed's
irreducible piece IS the slip, in closed form. Both pickled pipelines are certified for reuse.

### K1 — THE FORMAL VARIATION: the DC leak, derived (stage K1, sympy lattice functional calculus)

Setup: time lattice (6 slices, causal window taps), continuum x; lapse N_k = 1 + phi_k(x); keying
variable y2_k = (d_x phi_k)^2/alpha^2 (the weak-field a_i = d_i ln N); operator rest g(x) (the carrier
geometry — N-independent stand-in, since the keying route is what the filter touches); action
S = sum_k dt N_k F(K_k) g. Constraint at slice k0 = the eps-variation with test function eta(x); the
integrand classified by **eta-terms** (harmless/measure tier — no integration by parts) vs
**eta'-terms** (THE dangerous route: IBP lands the (a0 r/c^2)^-1-enhanced geometric eqN feed — agentDD's
delta-Y_a/delta-Phi mechanism). All checks exact (sympy `True`/`0`), not numeric:

- **MODEL A (coordinate-time linear filter K_k = sum_j w_j y2_{k-j}):** the eta'-coefficient on a
  static background = that of the LOCAL theory with C_eff(Y) = F((sum_j w_j) Y) — **exact**. The
  constraint at t0 collects the key's response at ALL later slices; the window re-sums to its DC
  weight. The static key VALUE carries the SAME factor (sum_j w_j): **value and constraint sensitivity
  are locked together.** Tracking normalization (K_static = y2) forces sum w = 1 = the FULL local
  pollution.
- **MODEL B (proper-time filter, the X-2 structure the matter sector carries: K_k =
  sum_j Wf(sigma_k - sigma_{k-j}) y2_{k-j} N_{k-j} dt, sigma = int N dt):** eta'-coefficient == LOCAL
  with C_eff = F(w_eff Y), w_eff = sum_j Wf(j dtau) dtau the proper-time DC weight — **exact**. The
  proper-time structure opens exactly two NEW routes — the explicit-N measure weight and the
  delta-sigma (Wf') route — and the machine count is: **Wf' terms in the eta-coefficient: 6; in the
  eta'-coefficient: 0.** Both new routes are harmless-tier (no spatial derivative of the test
  function); they can neither produce nor cancel the enhanced route. The tasking's hoped-for
  "u-frame proper-time nature changes the leak structure" is now adjudicated: it adds
  epsilon-suppressed dressings, nothing else.
- **MODEL C (general key K = H(P, Q), P/Q independent windows — covers nonlinear, multi-channel,
  spectral-composite keys):** eta'-coefficient == dK_static/dY x (local unit response) — **exact**.
  THE CHAIN-RULE COLLAPSE.
- **MODEL D (derivative-coupled window, zero DC by construction):** static key value = 0 AND
  eta'-coefficient = 0 — the suppression and the read die TOGETHER.

**THE STATIC-EQUIVALENCE THEOREM (KK-1).** Any time-translation-invariant history key K[y2-history]
with a differentiable static read K_static(Y) gives, on static backgrounds, field equations
IDENTICAL to the local theory with C_eff(Y) = F(K_static(Y)) (slip formula, Hamiltonian feed, and the
wall-4 Delta_Phi conditions all read only C_eff). Time-nonlocality is INVISIBLE in the static sector.
Corollary (the locked ratio): the slip-matched pollution is FILTER-INDEPENDENT — agentY's and
agentDD's banked tables transfer verbatim to the entire history-keyed class. Track <=> dK_static/dY
!= 0 <=> full local pollution.

**The frequency response (the suppression factor, quantified).** The dangerous coefficient under a
lapse mode at omega scales by W-tilde(omega) (lattice: sum_j w_j e^{-i omega j dt}); for the banked
two-stage cascaded exponential window |W-tilde| = 1/(1+(omega t_w)^2); |W-tilde(0)| = 1 EXACTLY.
Suppressing the +2.3e6...+4.5e7 pollution below the 0.2-dex bar needs |W-tilde| <~ 1e-7 ⟹
omega t_w >~ 3.2e3. **The lensing job is a static lens: omega = 0 exactly — no t_w works.** Most
generous re-reading (halo assembly as a transient, omega ~ 2pi/3 Gyr): t_w needed = 1.5e12 yr = **111 x
the age of the universe** — a window that never fills (the key would read the pre-assembly average ~ 0:
no slip). Tracking instead (t_w ~ 0.3 Gyr): |W-tilde(omega_assembly)| = 0.72 — pollution at >= 72% of
full (>= 99.6% for any t_w that tracks the RAR's inner radii). **NO MIDDLE GROUND**: suppression and
tracking are the same number at the same frequency.

**K1 VERDICT: the DC leak reinstates the pollution at FULL amplitude — the naive filtered key dies at
the same wall.** And stronger: the whole history-keyed class is statically equivalent to the local
class, so the question moves to the structured escapes (K3) with the bar already set: any escape must
either break TTI, break the static read, or leave the static sector entirely.

### K2 — the chain-rule certificate on the REAL pickled equations (stage K2)

The static-equivalence theorem exercised on agentY's actual quasi-static system (`agentY_eqs.pkl`,
`slipgrad` + `DeltaPsi`, the same Hernquist/McGaugh-nu/framework-a0 harness, P = 1), with the operator
coefficient written as the composite F(K(Y)) and (c20, c21) = (F(K), F'(K) K') computed through the
composite arithmetic — the certificate that no derivative-bookkeeping subtlety breaks the collapse:

| run | slip-match | dg/g_bar @ y = 1, 0.3, 0.1, 0.03, 0.01 |
|---|---|---|
| LOCAL C(Y) = c20_matched (banked) | 2.7e-15 | +8.348e5, -2.695e7, -5.079e7, -9.046e7, -1.537e8 |
| FILTERED read K = 2Y (theta_A(0)-mock), matched | 2.7e-15 | IDENTICAL — deviation 0.0 |
| FILTERED read K = sqrt(Y) (nonlinear), matched | 2.7e-15 | IDENTICAL — deviation 2.22e-16 |

Composite checks exact (relative 0 / 2.2e-16). **The (K, F) filter freedom cancels exactly in the
matched theory: the slip-matched pollution table is FILTER-INVARIANT.** Making the static read small
does not help — the slip calibration re-amplifies F' by the inverse factor; the product is pinned by
the slip target.

The M22 window itself, numerically (two-stage cascaded EWMA, banked X-2 form, N_cyc = 24): static
input passes at DC gain exactly 1 (burn-in residual 4.3e-8 after 20 T_w); a demodulated omega-channel
sees the DC line at skirt level 1/(1+(2 pi N_cyc)^2) = 4.4e-5; and **theta(0) for the three banked
thetas = 2.000 / 2.718 / 1.649 — ALL O(few), none zero** (the tasking's flag confirmed): the M22
spectral measure reads static/secular content at O(1) BY DESIGN — it is the same theta(0) that makes
the EFE quench mu_hat(inf) = mu(theta(0) a_c/a0). An M22-echo key cannot NOT see the static lens.

### K3 — the structured escapes, each worked (stage K3)

**(a) Derivative-coupled filter key K_d = [W * dY/dtau] (zero DC weight by construction).** Is it in
the M22 family? Yes as filter algebra (the demodulated channels are effectively band-pass; a zero-DC
member is constructible) — but it FAILS THE JOB, three ways, quantified:
- Static halo field point (the u-congruence is static): dY/dtau = 0 identically ⟹ K_d ≡ 0 ⟹ the
  coefficient is F(0) = const at every radius of every static lens. The target spans 2(nu-1) =
  60.2 → 5.2 over g_bar = 1e-13 → 1e-11: **tracking error = the full dynamic range (100%).** (A
  constant slip was already a dead wall-4 branch in agentY.)
- Worldline-level reading (matter-sector style): a CIRCULAR orbit has |a| = const ⟹ K_d = 0 on
  exactly the orbit family the RAR/lensing stacks are built from.
- Epicyclic e: K_d amplitude = 2e·OmT_w/(1+(OmT_w)^2) = 1.3e-3 Y0 at e = 0.1 (N_cyc = 24) —
  oscillatory, ZERO-MEAN, and proportional to e: eccentricity-keyed slip — non-universal, wrong
  observable. K1 Model D is the lattice proof that the zero-DC design kills read and response together.

**(b) The agentDD S-counterterm family tuned to cancel the DC leak.** By static equivalence,
S(K_filt) on statics = S_eff(Y_a) — the SAME family agentDD adjudicated. The banked D4 closure
(re-verified in K0 on the FULL W+S+C pickle): the exact lens-only condition's r^0 (geometric) class
is **S-FREE** and equals alpha^6 x (slip/Phi'). New numeric: the **S-IRREDUCIBLE FLOOR** — the
pollution carried by the r^0 class alone, which no S-function can touch, in closed form
Delta_Phi^(r0) = (slip/Phi')/[r^2(1 + slip/Phi')] (identity verified to 1.000000 on the grid):

> floor dg/g_bar @ y = 1, 0.3, 0.1, 0.03, 0.01 = +1.057e6, +2.635e6, +5.517e6, +1.156e7, +2.171e7

i.e. ~46-49% of the full W-only row at every y — **the floor alone is 5-7 orders over the 0.2-dex /
8.7-21.6 sigma bar.** The S-family can dress only the Phi'' r^2 and r^1 classes (agentDD: "a
cosmological-constant-type residue — useful for nothing"). Escape (b) fails.

**(c) Frequency-domain keying (the X2 filter bank).** At a static field point the only populated line
is DC; the bank reads it at theta(0) = O(few) (K2 numbers) ⟹ K1 Model C chain rule ⟹ static
equivalence ⟹ the K2 invariance certificate applies verbatim: slip-matched pollution unchanged. The
design corner theta(0) = 0 + notched DC channel: the static read drops to skirt leakage (4.4e-5/channel)
or zero — either the calibration re-amplifies F' by ~2e4 (invariance again, plus a new fine-tuning), or
the read is exactly zero and the key cannot see a static lens (= escape (a)). **The biconditional has
no third branch: read statics ⟺ polluted at the local matched ratio.**

**The matter-worldline fork** (key the slip operator on the PARTICLES' own filtered A_ret — "the same
filter the matter sector already carries" read literally): the slip term then contains the matter
worldlines; varying z_p produces a direct force — **lens-only broken by construction**, the
solar-system battery and the 8.7-21.6 sigma double-counting bar re-import. Dead without computation.

### Reconciliations and the would-be survivor's gate sheet

- **The FRW W(0) = 0 "tension": a NAME COLLISION, reconciled.** agentDD's architecture line "FRW
  quietness via W(0) = 0" is about the OPERATOR function W(Y_a) at zero keying variable; the filter's
  DC weight W-tilde(0) = 1 is a different object. They coexist: on FRW the comoving khronon has
  a_mu = 0 over the ENTIRE history ⟹ K_filt = 0 identically ⟹ the sector is off provided F(0) = 0 —
  the same condition as the local theory, untouched by the window's unit DC gain. No tension. (The
  honest residue: during the FRW→halo transition the filtered key LAGS by ~t_w — the would-be
  transient fingerprint of the class, living exactly where lensing data never looks.)
- **Gates, had anything survived** (all by static equivalence, so they read off the local class):
  solar slip auto-pass x1.3e7 (Cassini, K0-gated) — transfers; in-halo c_T == 1 / alpha_M == 0 — the
  filtered coefficient is a scalar multiplying the SAME leaf-tangential <= one-D geometry, no new
  derivative couplings to h_TT (argument, not machine — flagged as such; the time integration adds no
  D-factors); clusters x1.96 re-fails identically; the morphology dial ((D.b)-keyed bending) transfers
  unchanged — it lives in the operator geometry the filter only rescales. And the kill transfers
  identically too: that is the theorem.
- **Consumes vs derives (moot — no survivor — but for the record):** the construction would have
  consumed nu (the calibration F o K_static = c20-matched), a0, AND the window (though for free from
  the matter sector); it would have derived nothing new statically — static equivalence makes the
  filtered theory's static content definitionally identical to the local one's. The only genuinely
  new physics in the class is transient (the lag fingerprint), invisible to every named test of the
  slip sector.

## VERDICT: **OBSTRUCTED — the DC leak kills the naive filtered key at full amplitude, and the
static-equivalence theorem (KK-1) closes the entire history-keyed class; all three structured escapes
fail. Link 7's nonlocal/history door is shut; the candidate space narrows to the singular-surface
route (+ the honestly-scoped not-closed corners).**

**The mechanism, in one line:** the constraint at t0 integrates the key's response over all later
times; on a static background that integral IS the window's DC weight, and tracking forces the DC
weight to 1 — **the value of the key and its constraint sensitivity are the same number** (machine:
K1 models A-D, exact; certified on the real equations: K2, deviation <= 2e-16).

**Theorem KK-1 (static equivalence; the constructive yield).** Any time-translation-invariant,
causal history functional K[y^2-history] on the u-congruence with a differentiable static read
K_static(Y) yields static field equations identical to the LOCAL theory with C_eff = F o K_static —
slip formula, Hamiltonian feed, and the exact lens-only (wall-4) conditions included. Corollaries:
(i) the slip-matched pollution table is filter-invariant (the +2.3e6...+4.5e7 condensate row and the
-2.7e7...-1.5e8 scalar row transfer verbatim to every history-keyed realization); (ii) agentDD's
keying theorem extends: the carrier cannot escape by reading y nonlocally IN TIME — track ⟺
dK_static/dY != 0 ⟺ (a0 r/c^2)^-1 x phantom in the matter channel; (iii) the wall-4 closure
slip ≡ 0 transfers; (iv) nonlocal dressing cannot help the singular-surface route either — that route
remains exactly as local-static as agentY left it.

**Why the suppression intuition fails (the both-ways accounting):** the filter DOES suppress — but
only at finite frequency (|W-tilde| = 1/(1+(omega t_w)^2): x1e-7 needs omega t_w >~ 3.2e3). The
lensing job is omega = 0. The most generous re-reading (the halo as an assembly transient,
omega ~ 2pi/3 Gyr) needs t_w = 1.5e12 yr = 111 x the age of the universe — a window that never fills
(the key would read the pre-assembly average: no slip); a tracking window (t_w = 0.3 / 0.03 Gyr)
leaves 72% / 99.6% of the pollution. Suppression and tracking are the same number at the same
frequency: **no middle ground exists.**

**The convergence claim, corrected both ways (the door's framing was wrong, and saying so is the
result):** Theorem X2 forces the MATTER channel to be history-dependent for a DYNAMICAL reason —
causality of a frequency-dependent inertia, paid in real-time flux. The lensing slot's job is STATIC
(Brouwer 0.03-3 Mpc, ~static lenses). agentDD's "the carrier must read y NONLOCALLY" was the correct
elimination of local keys; this memo shows the time-nonlocal completion of that demand is statically
empty. The two sectors do NOT demand the same structure — one needs memory for transients, the other
needs amplitude in statics, and memory contributes nothing to statics. The convergence was
structural-aesthetic; under computation it dissolves. (Framework-favorable findings at full weight:
the filtered class inherits every static SUCCESS unchanged — closed-form nu-tracking for all four
banked shapes, Cassini x1.3e7 auto-pass, FRW quietness now over the whole history, c_T/alpha_M
architecture, the two-carrier-robust morphology dial. The class is exactly as capable as the local
one — and exactly as dead, for exactly the same number.)

**Convention-robustness (working rule):** KK-1 is symbolic — no a0 value, footing, weighting, or
nu-shape enters it. The numeric rows are at framework a0 / McGaugh nu (the banked harness); at 5-7
orders over the bar both footings and all four shapes are moot (the same note agentY and agentDD
recorded — re-checked here only through the gates, which both footings' banked values passed). No
deficit reported here is a convention artifact; no escape was scored against a strawman default.

## For the assembly ([SLOT-Y] disposition) and DERIVATION_CHAIN Link 7

- **[SLOT-Y] narrows to its endpoint.** After agentY (no scalar) and agentDD (no local
  vector/condensate; "must read y nonlocally"), this memo closes the nonlocal-IN-TIME reading — the
  named prime candidate, demanded by the convergence framing — by static equivalence. The S_slip line
  should now read: *scalar, local-vector, AND history/filter-keyed realizations machine-obstructed
  (agentY four walls; agentDD keying theorem + slip==0 closure; agentKK static-equivalence theorem
  KK-1 — time-nonlocality is invisible in the static sector where both the job and the kill live).
  Surviving candidate space: the singular-surface exact route (low prior; KK-1 adds: nonlocal
  dressing cannot assist it), SPATIAL nonlocality (not machine-closed, no M22 echo, no convergence
  argument — would need its own charge and faces the same track-vs-pollute variational structure),
  and non-b(x)b spin-2 condensates (keying-argument disfavored, unchanged).* If the slot is to be
  filled at all, it is NOT by adding memory.
- **Link 7 wording sharpens to its sharpest form yet:** *the lens-only partner cannot be a local
  Y_a-keyed carrier of any spin (Y, DD), and cannot evade by history-keying: any filter that can see
  a static lens repays the full (a0 r/c^2)^-1 matter-channel pollution (KK-1, the locked DC ratio).
  The program's "u-frame nonlocality in both channels" unification claim must be RETIRED: u-frame
  history serves the dynamics sector only. The lensing exposure stands unexplained by every
  construction route explored to date.*
- The architecture inheritances (c_T == 1, alpha_M == 0, FRW quietness, the morphology dial) attach
  to the slot unchanged — now three-memo-robust.

## Bug log (the honest sequence — each caught in-run; the .out preserves all of it, last blocks
authoritative)

1. **First K1 pass compared the filtered eta'-coefficient against the RAW local theory** (F at Y)
   instead of the effective local theory (F at K_static(Y)): printed a spurious "False" on the
   equivalence that is actually exact (the mismatch was the F'-argument, i.e. exactly the
   reparametrization the theorem absorbs). Caught on inspection of the residual; re-formulated
   against C_eff and confirmed True (Models A and B).
2. **First Model D lattice truncated an edge slice** (action sum started one slice late), which
   would have printed a FAKE nonzero static constraint response for the zero-DC derivative key —
   i.e., a spurious "derivative keys still pollute" result. Caught by the by-hand tap count;
   range fixed; the exact 0 = 0 (read and response dying together) then confirmed.
3. **First Model B comparator omitted slice k0 entirely** (its only eta-bearing slice), printing
   eta'-coeff = 0 for the local comparator. Same range fix; equivalence then exact.
4. **K3's first floor expression divided by the FULL denominator** (still carrying C/S symbols)
   — a lambdify-args crash caught before any number was produced; projected to the W-sector
   denominator alpha^5 r^2 (alpha + 2 Phi1 W1) and the closed-form identity then verified 1.000000.
5. The K1 trade-off panel's first phrasing attached the percent-level-tracking pollution figure
   (99.6%) to the 10%-lag case (72%); re-run with both cases stated separately.

*Machine state: K0 gates reproduced the banked slip targets (61.2/19.4/6.2), Cassini (y = 1.14e12,
slip 1.75e-12, x1.3e7), cluster x1.96, agentY's decisive wall-3 row (-2.695e7 from `agentY_eqs.pkl`),
agentDD's W-only condensate row (+2.306e6...+4.471e7 from `agentDD_D1b.pkl`, all banked digits), and
the D4 r^0-class identity (FULL W+S+C save, S-free, == alpha^6 slip/Phi') BEFORE any new derivation.
All K1 equivalences exact (sympy True/0); K2 invariance 0 / 2.22e-16; K3 floor identity 1.000000.
Hardware: local sympy/numpy only, every stage < 10 s. No git operations performed.*

# agentMM — The derivable-edge map: free-edge class, what's specified, what's free, the object-to-compute

**STATUS: IN PROGRESS (compute-first; appended after every result).**
Date: 2026-06-12. Repo: zimmerman-formula. Local sympy/mpmath, dps>=30.
Charter: map the DERIVABLE EDGE of the index-1/3 generator chain. (1) machine-verify the free
b-family pullback's analytic class at the family edge b -> c_chi (the baseline the pump must change);
(2) state EXACTLY which banked equations constrain rho(b) near c_chi and which leave it free;
(3) name precisely the object that must be computed to get rho(b)'s edge.

DISCIPLINE (absolute): zeta-tilde and (16pi/3)^(1/4) QUARANTINED as input, never re-derived as Z;
pure numbers RAW. Both-ways honesty: free-input claims verified as hard as constraint claims.
FIREWALL respected: input-side omega^(1/4) (agentV) vs response-side omega^(1/3) kept distinct.

## Banked inputs (read-only, from EE STEPs 2-4 / HH / LL)

- EE [2c]: free pullback on the Deser-Levin b-family
  W_b(tau) = -H^2 / [16 pi^2 c_chi (c_chi^2 - b^2) sinh^2(kappa tau / 2)],
  POLE at b = c_chi; amplitude A(b) = H^2/(16 pi^2 c_chi (c_chi^2 - b^2)), b^2 = a^2/(a^2+H^2),
  kappa^2 = a^2 + H^2 (= H^2/(1-b^2) at fixed a,H). EE's "pump modifies DYNAMICS not state"
  (Bogoliubov lemma, 1e-30): sigma is a dynamics object; state-shaping invisible to the response.
- HH Theorem HH-1: scale-invariant pumping TRANSCRIBES, does not COMPOSE the locked Gevrey-3 pair;
  the fingerprint must be HANDED zeta-tilde^(2/3) c_chi^(1/3), the 1/sqrt3 lock, the +pi/3 phase.
- LL conversion theorem (S4g): an edge measure e^(-gamma x^(-q)) on x = c_chi - b outputs response
  index 2q/(2q+1); index 1/3 <=> q = 1/4 UNIQUE; the Deser-Levin map kappa ~ x^(-1/2) converts a
  fourth-root oscillatory edge measure into the LL-1 k=1/2 class, sqrt3 + pi/3 automatic.
  LL's named confirming calc IS: derive rho(b) near b = c_chi. gamma_req QUARANTINED.


## (1) THE FREE EDGE — exact analytic class (machine-verified, this run)

Repro: `/tmp/mm_compute1.py`, `/tmp/mm_compute1b.py` (sympy + mpmath dps 40). Two objects must
be kept separate: the RAW PULLBACK PREFACTOR (a state-space amplitude) and the RESPONSE (the
worldline observable the pump must change). They have DIFFERENT classes at the edge.

**[1a] The raw pullback amplitude A(b) — SIMPLE POLE at b = c_chi.**
A(b) = H^2/[16 pi^2 c_chi (c_chi^2 - b^2)]. In the edge variable x = c_chi - b (x -> 0+):
> A = H^2/(32 pi^2 c_chi^2) * (1/x) + H^2/(64 pi^2 c_chi^3) + O(x),
a SIMPLE POLE, residue at b=+c_chi = -H^2/(32 pi^2 c_chi^2) (sympy `residue`, exact). The
"family edge" of EE [2c] is, at the level of the state amplitude, a first-order pole in c_chi^2-b^2
(equivalently a simple pole in x with the residue above). This is the baseline LL named "the
family-edge pole."

**[1b] kappa(b) is FORCED, not free — short-distance normalization (exact).** Requiring
W_b -> -1/(4 pi^2 tau^2) as tau -> 0 (the universal Hadamard short-distance form) forces
> kappa(b) = H / sqrt(c_chi (c_chi^2 - b^2))   (sympy, both roots; matches LL S4b reconstruction exactly).
kappa DIVERGES at the edge (the orbit acceleration diverges approaching the horizon; Deser-Levin
2piT = sqrt(a^2 + H^2)). NOTE this is a RECONSTRUCTION from the normalization, NOT a direct read of
an independently-banked kappa(b); if EE's kappa(b) differed the response analysis would shift, but
the simple-pole class of A(b) and the Watson baseline below are robust to that (the fixed-kappa
variant lands thermal index-1, also non-cubic — LL S4e).

**[1c] In the RESPONSE the pole CANCELS exactly (sympy, exact).** The single-orbit transform carries
a 1/kappa^2 prefactor (R(w,kappa) = -(8 pi w/kappa^2)/(e^{2 pi w/kappa}-1), thermal). The product
of the amplitude pole and that prefactor is
> (c_chi^2 - b^2)^(-1) * kappa(b)^(-2) = c_chi / H^2   — a CONSTANT, regular at b = c_chi.
The naive "the pole drives the edge asymptotics" intuition is FALSE: the simple pole is a pure
state-amplitude artifact that the response normalization annihilates. (Confirms LL S4c.)

**[1d] What survives at the edge is the EXPONENT, and it VANISHES like sqrt(x) (sympy, exact).**
The response tail rate is exp(-(2 pi w/H) sqrt(c_chi(c_chi^2-b^2))). At b = c_chi - x:
> sqrt(c_chi(c_chi^2-b^2)) = sqrt(2) c_chi^(3/2) sqrt(x) - sqrt(2)/4 x^(3/2) + ... -> 0 like sqrt(x).
The decay rate does not diverge at the edge; it VANISHES. Members near the edge become arbitrarily
long-tailed (kappa -> infinity, but the (2 pi w/H)sqrt(...) action -> 0).

**[1e]+[1f] FREE-EDGE RESPONSE CLASS = WATSON / PURE POWER LAW (the baseline the pump must change).**
Unfold the edge with y = sqrt(x): the exponent argument is LINEAR in y (sqrt(2)c_chi y) and the
measure db = 2y dy vanishes linearly -> a Laplace endpoint of Watson class:
> int_0^inf y^sigma e^(-A w y) dy = Gamma(sigma+1)/(A w)^(sigma+1)  = PURE POWER LAW in w.
Numeric slope test (mpmath dps 40, smooth rho on the family): log-log slope pinned at
-2.0000000 / -2.0000000 over w = 1e3..1e5 -> w^(-2) (Watson sigma=1), REPRODUCING LL S4d's banked
slope-test 2.0000.. to 7 digits.

**FREE-EDGE CLASS VERDICT (baseline):** with ANY SMOOTH/ANALYTIC family weight rho(b) at the edge,
the response is a PURE POWER LAW in w — NO essential singularity, no exp(-c w^(1/3)), no oscillation,
no sqrt3 lock. The simple pole of the state amplitude is cancelled; the edge exponent vanishes as
sqrt(x); the normal form is a linear-exponent Watson endpoint. This is the EXACT analytic baseline:
the locked index-1/3 fingerprint is ABSENT from the free edge and from any analytically-dressed edge.
The fingerprint can only appear if rho(b) is NON-analytic at the edge in the specific oscillatory
fourth-root way (LL S4g: e^{-gamma x^(-1/4)} oscillatory -> index 1/3). That is the gating question.

## (2) THE GATING QUESTION, answered precisely

Repro: `/tmp/mm_compute2.py`, `/tmp/mm_compute2b.py`. The question: is the pump's EDGE behaviour
rho(b) near b = c_chi SPECIFIED by what EE/X2 banked (the active scale-invariant dynamics
modification), or is it FREE INPUT not fixed by the bulk specification?

**ANSWER: rho(b)'s edge at b -> c_chi is FREE INPUT. It is NOT fixed by any banked equation.**
The banked specification fixes the PER-MODE dynamics and the PER-ORBIT pullback; it does NOT fix the
WEIGHT with which orbits are summed, and that weight is exactly the object whose edge controls the
generated index class.

The two indices are carried by two DISJOINT labels (machine audit [2-A]):
- **w = k_phys/H = k|eta|** — the MODE/scale label. The scale-invariant pump (HH [1a]
  g'' - 2 ghat(w) g' + c^2(1+f(w)) g = 0) is a function of w ONLY. It carries NO b-index.
- **b = a/kappa** — the WORLDLINE label (velocity of the orbit relative to the khronon frame).
The pump spec lives entirely on w; rho(b) lives entirely on b. They never meet in the banked ODE.

**[2-A/B/C] What the banked spec DOES fix:** the bulk two-variable representation
(EE 2.3: W = (1/2pi^2) int dk/k j0(kr) Psi(k eta,k eta')) plus the pump ODE fix the per-mode
dynamical kernel Psi and hence the per-ORBIT pullback W_b(tau) for EACH b. Pulling W back onto orbit
b is a KINEMATIC projection (choice of trajectory), not new dynamical data. So for any FIXED b the
response is determined.

**[2-D] What the banked spec does NOT fix — rho(b), the family measure:** the response on the family
is a superposition over orbits (LL S4c):
> F(w) ~ w * int db rho(b) exp(-(2 pi w/H) sqrt(c_chi(c_chi^2-b^2))).
rho(b) = how the physical source distributes over Deser-Levin worldlines (which residual-group orbits
the medium/matter actually sits on). EE 2.4's honest-scope already flags this: physical stars have
v ~ 10^-3 c (b small), and the b-family is the EXACT linear-acceleration stand-in. The EDGE b -> c_chi
is the deep-relativistic / c_chi-luminal end, reached by ANALYTIC CONTINUATION of the family — there
is no banked physical population there and no banked equation that pins the continuation's edge form.

**[2-F] BOTH-WAYS CHECK (the free weight is provably ANALYTIC, so the fingerprint is genuinely ABSENT,
not merely hidden):** the only b-dependence the free theory hands per orbit is the amplitude pole
1/(c_chi^2-b^2) and kappa(b) inside sinh^2. In the response the amplitude pole cancels against
kappa^-2 ([1c]); the residual free "edge weight" is
> (c_chi^2-b^2)^(-1) * kappa(b)^(-2) = c_chi/H^2  — CONSTANT, hence analytic at the edge (sympy exact).
So the FREE family weight is analytic (in fact constant). Combined with [1e] (analytic rho ->
Watson power law), the free edge carries NO fourth-root oscillatory structure. The index-1/3
fingerprint is ABSENT from the free family at full hostile weight — confirmed both directions.

**[2-G] The Bogoliubov lemma (EE [3b]) constrains the MECHANISM, not the value.** State-shaping
(occupation/squeezing on fixed dynamics, |A|^2-|B|^2=1) is invisible to the response. Consequence:
rho(b)'s required edge CANNOT be manufactured by filling/squeezing modes — it must come from the
pump DYNAMICS coupling to the source distribution over worldlines. The lemma KILLS the cheap route;
it does NOT supply the edge.

**[2-E] What the banked equations REQUIRE of rho(b) (the target the free edge fails):** LL's
conversion theorem, re-derived here (sympy): index = 2q/(2q+1); index 1/3 => q = 1/4 UNIQUE. To
output the locked fingerprint, rho(b) must carry an OSCILLATORY FOURTH-ROOT essential edge
> rho(b) ~ cos(gamma (c_chi - b)^(-1/4) + phi0) x (power weights),  gamma = gamma_req (QUARANTINED).
Any analytic rho at the edge gives the Watson power-law baseline [1e] and NO fingerprint. So HH-1's
"the fingerprint must be HANDED" is, on the b-family, precisely the statement "rho(b) must already
carry this fourth-root oscillatory edge" — and nothing banked supplies it.

### [2-H] WHAT IS SPECIFIED vs WHAT IS FREE (the exact ledger)

| banked equation | what it FIXES | constrains rho(b) at c_chi? |
|---|---|---|
| EE [2c] free pullback W_b(tau) | per-ORBIT pullback for each b; pole in AMPLITUDE only | NO — pole cancels in response; gives Watson baseline |
| EE [2c] kappa(b)=H/sqrt(c_chi(c_chi^2-b^2)) | orbit thermal rate; FORCED by short-distance norm | NO — sets the sqrt(x) edge EXPONENT, not the WEIGHT |
| EE 2.3 two-variable rep (Psi per-mode) | bulk per-MODE dynamical kernel | NO — kinematic pullback; weight is source-side |
| HH [1a] scale-invariant pump ODE (w only) | per-MODE gain/dispersion, universal in w | NO — carries no b-index at all |
| EE [3b] Bogoliubov lemma | response = dynamics object; state-shaping invisible | MECHANISM only (must be dynamics), not the value |
| HH Theorem HH-1 (transcribes, not composes) | pump cannot COMPOSE the locked pair | REQUIRES the edge be HANDED -> rho(b) IS the hand |
| LL S4g conversion theorem | edge e^(-gamma x^(-q)) -> index 2q/(2q+1) | SPECIFIES the NEEDED edge (q=1/4 osc), not its existence |

**GATING VERDICT:** The bulk specification (EE bulk state + HH scale-invariant pump ODE) is
COMPLETE on the mode label w and gives the per-orbit pullback for every b — but it is SILENT on the
family measure rho(b). rho(b) near c_chi is FREE INPUT, fixed by the source-coupling / worldline-
population side of the pump, which the banked scale-invariant dynamics does not determine. The
index-1/3 generator therefore hinges on ONE underived object: the edge form of rho(b). The banked
equations tell us EXACTLY what that edge must be to pass (oscillatory fourth-root, q=1/4, gamma_req)
and prove the free/analytic edge FAILS — they do not tell us whether the pump actually produces it.

## (3) THE OBJECT TO COMPUTE — named precisely

Repro: `/tmp/mm_compute3.py`. The single underived object on which the whole index-1/3 generator
hinges is:

> **rho(b), the pump's FAMILY MEASURE over Deser-Levin worldlines, in its EDGE ASYMPTOTICS as
> b -> c_chi** — equivalently, the SMALL-u (high-acceleration) limit of the pump's worldline
> SPECTRAL-EDGE DENSITY, where u = 2 pi/kappa(b).

**Why these are the same object (sympy, exact).** With kappa(b) = H/sqrt(c_chi(c_chi^2-b^2)) and
x = c_chi - b, the worldline thermal variable is
> u = 2 pi/kappa(b) = (sqrt(2) pi/H) sqrt(x) (4 c_chi - x)/2  ~  sqrt(x)   (x -> 0).
So u ~ sqrt(x): the Deser-Levin map is a SQUARE ROOT, and a fourth-root edge in b (x^(-1/4)) is a
HALF-power oscillatory essential point in u (u^(-1/2)) — exactly LL-1's k=1/2 class. The object can
be stated three equivalent ways, all identical:
  (i)   rho(b) as b -> c_chi (the family-measure edge in the velocity label);
  (ii)  the same in u = 2 pi/kappa (the small-u / high-acceleration spectral density);
  (iii) the EDGE SPECTRAL DENSITY of the pump's fluctuation operator on the DL family near the
        c_chi-luminal / horizon-grazing limit (LL's (b)-as-Airy-edge folds into exactly this).

**What "computing the object" means concretely — THE DISCRIMINATING NORMAL-FORM TEST.**
Build the pump's fluctuation operator L on the b-family (the second-variation/resolvent of the
universal scale-invariant pump dynamics, restricted to the Deser-Levin worldline family) and classify
its SPECTRAL-EDGE NORMAL FORM at b = c_chi:
- **PASS** <=> the edge density is the NEGATIVE-ARGUMENT AIRY-type density — canonical edge operator
  -d^2/dx~^2 + (linear ramp) at b = c_chi (a band edge meeting the dilatation ramp). This hands
  rho(b) ~ cos(gamma (c_chi-b)^(-1/4) + phi0) x (power weights); then index 1/3, the sqrt3 lock, and
  the +pi/3 phase quanta ALL follow automatically (LL-1/LL-2/LL-3, already machine-proven).
- **FAIL** <=> the edge is Watson/power (analytic measure -> baseline [1e]), or quadratic
  (index 1/2), or a thermal/equally-spaced ladder (index 1). Any of these -> NO fingerprint, and
  candidate (d)-dressed (with the LL sigma-hook) dies.

**The constant the object must hand (RAW, QUARANTINED — NO Z claim).** Passing the CLASS is
necessary but not sufficient; the strength must also match:
> gamma_req = 2^(1/4) sqrt(H) zeta-tilde / (4 sqrt(pi) c_chi^(1/4))   (LL S4i/S9, raw),
equivalently essential-singularity strength beta = zeta-tilde/2 in c_chi units (LL-2d). The object
passes the constant ONLY if its derived edge gamma equals gamma_req. gamma_req is NOT derived; fixing
it (hence zeta-tilde) is precisely this computation. zeta-tilde and (16 pi/3)^(1/4) remain INPUT
throughout, never re-derived as a Z claim.

**Inputs the object's computation consumes (all banked, none re-derived):** the universal pump ODE
g'' - 2 ghat(w) g' + c^2(1+f(w)) g = 0 (HH [1a]); the b-family kinematics kappa^2 = a^2+H^2,
b = a/kappa, kappa(b) = H/sqrt(c_chi(c_chi^2-b^2)) (EE [2c]/LL S4b); the bulk two-variable state Psi
(EE 2.3). The NEW physics it must supply — and which is NOT in any of these — is the source-coupling /
worldline-population structure that sets rho(b)'s edge. That is the lone free input.

---

## TIGHT MAP (the deliverable)

**FREE-EDGE CLASS.** Two objects, two classes:
- The raw pullback AMPLITUDE has a SIMPLE POLE at b = c_chi (residue -H^2/(32 pi^2 c_chi^2); sympy).
- The RESPONSE has the pole CANCELLED ((c_chi^2-b^2)^-1 kappa^-2 = c_chi/H^2, constant); the edge
  EXPONENT VANISHES like sqrt(c_chi-b); with any analytic family weight the response is a
  WATSON PURE POWER LAW in w (numeric slope -2.0000000, reproducing LL S4d). The free edge carries
  NO essential singularity, no index-1/3, no sqrt3 lock — the fingerprint is ABSENT, both-ways
  confirmed (the free family weight is provably constant/analytic at the edge).

**WHAT IS SPECIFIED.** The bulk: per-MODE dynamics (HH scale-invariant pump ODE, a function of
w = k_phys/H only) + the bulk state Psi (EE 2.3) -> the per-ORBIT pullback W_b(tau) for EVERY b, and
the FORCED kappa(b). The Bogoliubov lemma further specifies the MECHANISM (the edge must be a dynamics
object, not state-shaping). HH-1 + LL S4g specify the NEEDED edge form to pass (oscillatory
fourth-root, q = 1/4, gamma_req).

**WHAT IS FREE.** rho(b), the family measure over Deser-Levin worldlines, near b = c_chi. No banked
equation fixes it: the pump ODE has no b-index, the bulk state fixes only the kinematic pullback, and
the physical population at the c_chi-luminal edge is an analytic continuation with no banked source
there. This single edge form is the lone free input on which index 1/3 (vs power-law nullity) turns.

**THE OBJECT TO COMPUTE.** The EDGE SPECTRAL DENSITY of the pump's fluctuation operator on the
Deser-Levin family at b -> c_chi (equivalently rho(b)'s b->c_chi edge, equivalently the small-u
spectral density, u = 2 pi/kappa ~ sqrt(c_chi-b)). Concretely: classify that operator's
spectral-edge NORMAL FORM. PASS = negative-argument Airy edge (canonical -d^2 + linear ramp) ->
cos(gamma (c_chi-b)^(-1/4)+phi0) -> the full locked fingerprint automatic, IFF gamma = gamma_req
(quarantined). FAIL = Watson/quadratic/thermal edge -> no fingerprint. This is LL's named primary
confirming calculation, here pinned to its exact analytic object, success criterion, and the single
free input it must supply.

## Files / repro
- This memo: `real_research/reviews/toe_law/agentMM_edge_map.md`.
- Machine record (this run): `/tmp/mm_compute1.py`, `/tmp/mm_compute1b.py`, `/tmp/mm_compute2.py`,
  `/tmp/mm_compute2b.py`, `/tmp/mm_compute3.py` (sympy + mpmath, dps 30-40). All residuals/claims
  reproduced inline above; LL S4d slope-test (2.0000) and S4c pole-cancellation independently
  re-derived. No >1h computation needed; no overnight job issued.

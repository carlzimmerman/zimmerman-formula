# agentEE — Can the khronon medium's own fluctuation spectrum produce sigma_req structurally?

**STATUS: IN PROGRESS — skeleton written, steps executing incrementally.**

Date: 2026-06-11. Relaunch (prior attempt stalled pre-write).

## Target

Link 5's sole remaining derivation. agentV (kernel inversion) pinned the REQUIRED spectral
weight sigma_req:

- fourth-root **essential singularity at the lightcone**,
- **all inverse moments zero**,
- asymptotics sigma(u) ~ u^(-13/8) e^(-zeta u^(-1/4)) cos(zeta u^(-1/4) - pi/8) as u -> 0+,
- dS Kallen-Lehmann **positivity kills every dS-invariant carrier** — the carrier must
  BREAK dS invariance.

agentX (Theorem X2): the medium must be ACTIVE/pumped; the Lambda/dS budget pays.
agentU: the khronon (unit-timelike-gradient scalar, M22 corner) is the named matter-sector
candidate; it has a preferred foliation by construction.

**Scoping question:** does the khronon's own fluctuation spectrum (a) evade V's positivity
no-go via foliation breaking, and (b) live in (or reach) the fourth-root essential-singularity
asymptotic class — or what extra structure is needed?

Coefficient discipline: raw numbers only; zeta = (16pi/3)^(1/4) quarantined as input,
not re-derived; NO Z claims. Framework-favorable territory — hostility to wishful steps
is mandatory.

## STEP 1 — Literature pin: khronon mode functions on dS vs fundamental scalar

**Pinned ids (WebSearch 2026-06-11):**

- **arXiv:1206.1083** — *Khronon inflation* (Creminelli–Noreña–Peña–Simonović, JCAP 2012). The
  scalar mode of the preferred foliation ("khronon") on a de Sitter background with full time
  reparametrization invariance: only two leading operators survive, and **the mode wavefunctions
  have the same form as in MINKOWSKI space** — the (1 + ic_s kη)e^{−ic_s kη} dS dressing of a
  fundamental scalar is absent; perturbations are produced only when the reparametrization
  symmetry breaks. This is the cleanest published statement that the khronon's dS two-point
  structure is NOT the Bunch–Davies family.
- **arXiv:astro-ph/0407437** — Lim, *Can we see Lorentz-violating vector fields in the CMB?*
  (PRD 71, 063504). The aether's scalar (and vector) modes quantized on the preferred foliation
  during inflation: modes labeled by comoving k on the foliation, dispersion ω = c_s k with
  **c_s² a ratio of the aether couplings** (≠ 1 generically), spectra carrying inverse powers of
  c_s. Supporting: **arXiv:1003.1283** (Armendáriz-Picón–Sierra–Garriga, Einstein-aether and
  BPSH/khronon primordial perturbations — same structure in the khronometric limit);
  **arXiv:1309.4778** (aether-inflation perturbations can grow exponentially when the LV scale
  is low — the foliation sector admits non-passive corners, cf. X2's option (b), which agentU's
  gate 1 forbids for us).

**How the khronon's dS mode functions differ from a fundamental scalar's (the answer):**

1. **Mode label and cone.** Modes are plane waves in comoving k ON THE PREFERRED FOLIATION with
   dispersion ω = c_χ k, c_χ² = O(γ/α) ≫ 1 in agentU's generic PPN corner. The singular support
   of W sits on the SOUND cone r = c_χ|Δη|, not the metric lightcone — for c_χ > 1 the
   singularity lies at metrically SPACELIKE separation; on metric-timelike chords (where
   sigma_req lives) the free correlator is real-analytic.
2. **No BD dressing / no Z-dependence.** A fundamental massless dS scalar carries the
   (1 + ikη)e^{−ikη} curvature dressing and (for invariant masses) a Wightman function W(Z) of
   the single dS invariant Z. The khronon's wavefunctions are Minkowski-form (1206.1083): its
   W is a function of (η, η′, r) invariant only under the residual 7-parameter subgroup
   E(3) ⋊ dilatation ⊂ SO(4,1) — i.e. a function of TWO independent invariants (e.g. Z and
   η′/η), not one. The three dS boosts are broken by the foliation.
3. **State + dynamics both break dS.** The adiabatic vacuum on the foliation is not a dS-invariant
   state, and the dynamics (foliation-dependent kinetic term) is not a dS-invariant operator —
   so BOTH hypotheses of the Bros–Moschella decomposition fail, not just the state's.
4. **What survives:** dilatation acts as proper-time translation on comoving worldlines ⟹ the
   worldline pullback is still STATIONARY there (verified in §2 below; the conformal-c_s member
   even stays KMS at H/2π — thermality is again "not what breaks", N1-consistent).

## STEP 2 — The positivity escape: which step of V's KL argument uses dS invariance, and does the khronon evade it?

(pending)

## STEP 3 — Asymptotic class: power-law/analytic cut density vs fourth-root essential singularity

(pending)

## STEP 4 — Verdict

(pending)

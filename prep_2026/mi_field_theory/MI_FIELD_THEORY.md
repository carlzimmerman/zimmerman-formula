# The Modified-Inertia Field Theory — Consolidated Statement

**Carl Zimmerman's de Sitter–Unruh modified-inertia framework, assembled as a single
classical (+1-loop-informed) action.**
Scale: `a0 = cH_Lambda/Z = c^2 sqrt(Lambda/3)/Z`, `Z = sqrt(32π/3) = 5.78881`.
Canonical footing `a0 = 9.36e-11 m/s^2` (ρ_DE / cH_Λ); ALT footing `1.13e-10` (ρ_total / cH0).
**Both footings carried throughout; the verdict is a0-value-independent (structure only).**

This is *the most complete honest MI field-theory statement we can write*. It is **not** a
claim that the theory is complete or proved, **not** a TOE, and **not** an SM bridge (the
2026-06-23 TOE/SM retraction is respected). Every element is flagged DERIVED vs POSTULATED.
The verifier's two corrections are applied throughout (closure off-circular sign relabeled
convention-dependent; nonlocal-B ghost-freedom demoted from a machine-check to an asserted
structural argument; the two tautological script checks fixed — `unification.py:161`,
`wellposed.py:204`).

---

## 1. The single most-complete action

Signature (−+++). One metric `g`, one passive frame `u`, one Lagrange multiplier `λ`, matter `ψ`,
one kernel `K`, one scale `a0`:

```
S[g, u, λ, ψ]  =  S_EH[g]  +  S_u[g,u,λ]  +  S_matter[g,u,ψ; K]  +  S_photon[g̃ = g + B[K] u u]

S_EH     = (c^4/16πG) ∫ √−g  R                         # host gravity UNMODIFIED (2 graviton dof)
S_u      = −∫ √−g (λ/2)(u^μ u_μ + 1)                   # passive unit-timelike frame, NO kinetic term (0 dof)
S_matter = −(1/2) ∫ √−g  ρ_m [ s · u^μ K(□_u/a0^2) u_μ ]   # modified inertia lives in the MATTER kinetic sector
S_photon =  standard Maxwell on the disformal metric  g̃_μν = g_μν + B u_μ u_ν   # lensing (2 photon dof)
```

with
- `K(z) = (√(1+4z) − 1)/(2√z)`, `□_u f = u^a ∇_a(u^b ∇_b f)` (frame-directed d'Alembertian),
- `s = −1` (**POSTULATE** — sets the MOND sign, the dissipation sign, *and* the causality-preserving
  sign of the disformal term simultaneously),
- `λ` fixed on-shell `= −ρ_m s K` (soaks the l=0 frame source; no propagating multiplier),
- `B` fixed by the **same** kernel: `∇B = 4(ν−1) g_bar` with `ν = 1/K` the same interpolation the
  dynamics use — **no new free function, no new propagating dof**.

**Kernel rigor (DERIVED).** `K` is Herglotz–Nevanlinna with a *unique* positive Borel measure:
`ρ_A = (1−√(1−4|t|))/(2π√|t|)` on `−1/4<t<0`, `ρ_B = 1/(2π√|t|)` on `t<−1/4`, additive const
`a = 0.65411`, `‖K‖ ≤ 1`, causal-retarded. Sum rule `∫ dμ(t)/|t| = K(∞)−K(0) = 1` (region-B = 2/π
exact, total = 1 to 1e-8), `K(0)=0` — so `a0` enters *only* through the argument `X = |a|^2/a0^2` and
carries **no counterterm at scale a0** (loop-protected, §4).

**Reduction bridge to phenomenology (DERIVED, first moment only).** The frame-directed operator
reduces on a worldline via the **worldline-general** identity
`u_μ □_u u^μ = −|a|^2` (re-derived three independent ways — flat-general, curved-general symbolic,
concrete static Schwarzschild — needing *only* unit norm `u·u=−1` and metric compatibility `∇g=0`;
NOT circularity, geodesy, or symmetry). Hence `⟨□_u⟩_u = +|a|^2` and
`K(□_u/a0^2) → K(a^2/a0^2) = μ_fw(|a|/a0)`. The circular balance `μ_fw(x)·x = y` inverts *exactly*
(the nested radical collapses, `1+4(y^2+y)=(2y+1)^2`) to `x = y·ν(y)`, giving at every radius
```
g_obs = ν(y) g_bar = √(g_bar^2 + g_bar·a0),   ν(y)=√(1+1/y),   y = g_bar/a0
```
ring residual ~1e-13, both footings. This yields Newton, deep-MOND, BTFR `v^4 = G M a0`, and the
`√2` DC-weight external-field kernel.

**This closure is exact at the FIRST moment and no more.** On the exact helix, `u·(□_u)^n u` matches
`(a^2)^n (u·u)` only at n=1; the n=2 ratio is `1−1/v^2`, which diverges as v→0 — the moment tower is
*uncontrolled*, so the off-circular reduction is genuinely free (this is Gap A, §2).

---

## 2. Which completion gaps CLOSED, which stayed OPEN

### Gap A — closure / ordering map beyond the first moment: **PARTIALLY PINNED, one bracket stays OPEN**

The five structural principles (Herglotz+sum-rule, causal-retardedness, KMS/detailed-balance at
`T_dS`, descent-from-the-action, `c_T=1`/Cassini) act as a decision procedure. **FORCED (re-verified):**
- the *operator/measure/scale* (unique measure by identity theorem; only scale `a0`; DC normalization
  `K(∞)−K(0)=1`);
- the *circular reduction* = ring-exact RAR (both footings);
- the AC/orbital sector passes as **pure phase** `|K(−ω^2+i0)| = 1` — no amplitude MOND from *any*
  orbital frequency; MOND lives only in the DC/secular sector;
- the **corner location = a0**: descent from the well-posed action forces `τ_mem = 2c/a0 = 203/168 Gyr
  > Hubble time` (every bound system has `ω_orbit/ω_c ≫ 1e3`), which **rejects** the Milgrom-1994
  orbital-averaging corner as a non-action scale. *This is the genuine new narrowing over the prior
  off-circular SPEC* — it removes the corner-location freedom among candidate scales.

**RESIDUAL, stated exactly (OPEN):** one reduction-weighting degree of freedom — how the finite
horizon-memory weights orbit *history* — interpolating closure A (instantaneous `|a|`; zero offset,
MG-identical in spherical symmetry, verified to 4e-14) and closure B (history-averaged `⟨|a|^2⟩`;
epicyclic offset with deep-MOND coefficient `−0.326 ε^2` dex, isotropic ensemble `~−0.02 to −0.05`
dex, footing-stable ~10–15%). Equivalently **one free function η(β)** on (eccentricity × anisotropy).

> **VERIFIER CORRECTION (applied).** The closure lane's headline that the off-circular *sign* is
> forced (a "MG-impossible discriminator") is **over-pinned and withdrawn**. The check that produced
> it (`closure_map.py:242-244`) was near-tautological, and an independent concave-RAR Jensen
> construction (`d²g_obs/dg_bar² = −a0^2/[4 g^{3/2}(a0+g)^{3/2}] < 0` everywhere ⇒ average-then-dress
> gives a *positive* offset, +0.001…+0.07 dex on Kepler orbits) yields the **opposite** sign. So the
> off-circular *sign is convention/averaging-order-dependent, NOT forced.* The honest residual is a
> **sign-free bracket that includes zero** — magnitude bounded `[0 … closure-B pattern]`, sign not
> pinned. What *is* forced remains: operator, measure, scale, corner, circular RAR.

**Closes only by** the off-circular dS-Unruh Wightman pullback on a non-uniform worldline (not done;
honest prior: the pole stays at/above `κ = H_Λ` ⇒ the freedom stands) **or** an empirical proxy
(dwarf σ-hysteresis amplitude / cluster η(β) slope) that *measures* the retention. **Falsifier:** a
confirmed frequency-split RAR at fixed `g_bar` (>2 dex in orbital frequency, >1e-7 in ν) kills the
kernel outright — no measure freedom can absorb it.

### Gap B — matter coupling + full T_μν: **CLOSED at the tensor-structure + conservation level**

Matter is **minimally coupled to the single metric `g`** (rods, clocks, and photons ride `g`);
modified inertia is a **universal, WEP-exact (η=0) kinematic-scalar dressing**
`W = s u^μ K(□_u/a0^2) u_μ` of the matter kinetic term — matter feels the kernel through its own
4-acceleration via `X=|a|^2/a0^2`. It is **not** a disformal matter metric (a disformal `g_M=g+C uu`
would drag light — computed Maxwell drag `cosh(3/5)/40 ≠ 0` — double-counting the dynamics). The three
variations:
- `δ/δλ ⇒ u·u = −1`;
- `δ/δu^μ ⇒` frame equation with algebraic source `J_μ = −(ρ s K + λ) u_μ`, strictly **l=0**
  (transverse projection verified zero), soaked by `λ = −ρ s K`; the `K'` (acceleration) terms are
  the l=1 worldline dynamics and **never populate the l=2 traceless shear** — this is the AeST Cassini
  Bianchi lock, satisfied structurally;
- `δ/δg^μν ⇒` closed-form stress tensor
  ```
  T_μν = −ρ s K · u_μ u_ν  +  (1/2) ρ s K · g_μν  +  (ρ s K'(X)/a0^2) · a_μ a_ν
  ```
  Principal (UV, K→1, K'→0) limit: the anisotropic `γ a_μ a_ν` term vanishes ⇒ **isotropic perfect
  fluid ⇒ no gravitational slip (Ψ=Φ)** — AeST's no-slip recovered from modified *inertia* without a
  dynamical aether. The *only* slip/enhancement-capable stress is `γ a_μ a_ν`, nonzero only in the
  MOND/IR (`K'≠0`) — this is the lensing-enhancement piece (Gap C).

**Conservation (DERIVED, verified two ways):** `∇_μ T^μν = 0` on-shell by diffeomorphism invariance —
(i) the generic canonical Noether identity `∂_μ Θ^μ_ν = −(EL)∂_ν φ` holds identically; (ii)
instantiated with the actual MI acceleration kernel the residual is `2.6e-16` at 12 random points. The
unit-norm constraint stays consistent (`u·a=0` ⇒ no drift; frame stays 0-dof). **No inconsistency,
no forced composition-dependence, no Cassini quadrupole forced.** `a0` enters `T_μν` only through `X`
(α, β are a0-free; γ's a0-dependence is exactly `1/a0^2`), unrenormalized by the coupling.

**Residual (OPEN):** the *local* `T_μν` uses the first-moment closure, so the full *nonlocal* `T_μν`
differs off-circles by exactly Gap A; and the exact **IR magnitude + higher multipoles** of the
anisotropic `γ a_μ a_ν` stress (the curved `δS/δg` including the connection piece of `a^μ`) — i.e. the
lensing-enhancement magnitude — coincides with Gap C. Present in the tensor and of the right
(horizon-`a0`) order; magnitude not yet pinned.

### Gap C — unification of dynamics + lensing: **UNIFIES in the minimal-disformal sense; off-spherical inherits Gap A**

One action yields **both** the MI dynamics kernel and lensing — but lensing does *not* emerge from the
dynamics term alone; a **separate photon coupling is structurally forced**. With one metric, putting
the RAR enhancement in `g` and re-solving the *same* MI EOM forces `ν_g = 1` (symbolic solve) — a
genuine double-count obstruction. So lensing must live in a separate coupling, and the **minimal** one
is the disformal photon metric `g̃ = g + B uu` with `B` fixed by the *same* `K` (no new field, no new
dof). **The separate Branch-B elastic medium is NOT required** — and is independently evidence-tilted
to fail Cassini (free shear scalar below `β_crit`, ×1.1–1.8 over ceiling). The unified action strictly
dominates the two-action alternative.

**Constraints re-checked from the action (DERIVED):** `c_T = 1` **exact** (graviton on `g`; `B u_μ u_ν`
has zero spatial ij block in the rest frame — now *genuinely* computed, `wellposed.py:204` fixed);
Cassini **safe** both footings (`|Δγ| ~ a0/2a → ~7.2e-7` canonical / `8.7e-7` alt at Saturn `≪ 2.3e-5`).

**Honest deficits (OPEN):**
1. Off spherical symmetry, lensing inherits Gap A: `curl(ν g_bar)=0` holds spherically but is
   order-unity (`−0.31`) for two point masses, so a *local* `B` is exact only spherically; generically
   `B` is the nonlocal AQUAL potential (`= K(□_u)`), whose gradient `≠ ν g_bar` off-sphere.
   Dynamical-RAR and lensing-RAR coincide **exactly only where the first-moment closure is pinned**
   (spherical/circular) and are **both free off it**. Lensing adds no *new* gap; it inherits Gap A.
2. **Nonlocal-B ghost-freedom is ASSERTED, not machine-verified** (verifier correction; the prior
   `unification.py:161` was a tautological `True is True` check, now removed and demoted to narration).
   The *local* B is genuinely first-order (`maxord=1`, verified) hence trivially Ostrogradsky-free
   given the passive frame; the *nonlocal* B off-sphere is argued ghost-free as an elliptic/AQUAL
   constraint field **at the same open standing as the framework's own nonlocal `K(□_u)`** — a
   structural argument, not a proof.
3. The photon-vs-graviton disformal **timing bound** `∫(B/2)dl` over Mpc line-of-sight is a *separate,
   weaker* constraint than the tensor-speed bound; per-galaxy `dB~1e-16` but the accumulation over
   cosmological baselines is only **order-of-magnitude** satisfied — flagged OPEN, not asserted safe.
4. Full nonlinear coupled `g+u+photon` back-reaction and the metric `T_μν` (Gap B residual) uncomputed.

### Well-posedness of the full coupled system: **CLOSED, conditional on the passive-frame premise**

DOF = **2 graviton + 2 photon + matter**, frame **0 propagating dof** — and the 0-dof *survives the
matter coupling* (new result): the unit-norm 2nd-class Dirac pair `{χ1=u·u+1, χ2=u·π}=2(u·u)`,
`det=4(u·u)^2→4`, is a kinematic bracket independent of the matter momentum; the frame principal symbol
`(u·k)^2→k0^2` is a transport ODE (double root, zero group velocity), so `K(a^2)` dressing cannot
promote `u` to a propagating aether. **Ghost-free:** the local first-moment action is first-order in
every dynamical field (the classic `L(ẍ)` modified-inertia Ostrogradsky trap is evaded because
`a=u·∇u` is a *field gradient*, not a worldline `ẍ`); the nonlocal `K(□_u)` is ghost-free by the
Herglotz single-healthy-pole route (`K'>0` operator-monotone, residue +1, `0<K≤1`). **Bounded below:**
dressed inertia `μ=K ∈ (0,1]` positive; `g̃` Lorentzian iff `B<1` (`B~6–7e-7` both footings ≪1);
`c_T=1` exact. **Hyperbolic:** block-diagonal principal symbol (graviton=GR cone, photon=`g̃` cone for
`B<1`, frame=transport) ⇒ well-posed Cauchy problem (integro-differential, well-posed with retarded
history). **Causal:** photon null cone nested strictly inside `g` iff `B≥0` iff `s=−1` (so `s=−1` is
*also* the causality-preserving sign; `s=+1` gives superluminal/acausal photons). `28+/28 checks`,
exit 0, both footings.

**Conditional / OPEN:** the whole 0-dof + no-ghost verdict **rests on the passive/khronon premise**
(hypersurface-orthogonality) — the load-bearing hinge; a *dynamical* khronon `T` would give `a~∂^2 T`
and reintroduce an Ostrogradsky concern. The fully-nonlinear nonlocal coupled Hamiltonian and global
`B<1` off-spherical are not constructed.

---

## 3. Final DERIVED-vs-POSTULATED ledger

### DERIVED (proven / machine-verified, no knobs)
- **D1** Frame dof = 0 — passive frame, machine-verified curved Dirac closure (2nd-class block det=4,
  no tertiary tower), *survives matter coupling*.
- **D2** No induced aether kinetic term — no-wave-cone symbol `S_n=(−1)^n k_⊥^2 k0^{2n}` all orders.
- **D3** `K(□_u)` Herglotz–Nevanlinna, unique positive measure, `‖K‖≤1`, causal-retarded; sum rule
  `∫dμ/|t|=1` exact, `K(0)=0`.
- **D4** First-moment identity `u·□_u u=−|a|^2` **worldline-general** (unit-norm + metric-compatibility
  only; re-derived three ways, residual 0).
- **D5** Ring-exact RAR `g_obs=ν(y)g_bar=√(g_bar^2+g_bar a0)`, both footings, residual ~1e-13.
- **D6** Newton, deep-MOND, BTFR `v^4=GMa0`, `√2`-DC EFE kernel, ghost-freedom (single healthy pole +1).
- **D7** Causal ghost-free two-point propagator; Källén-Lehmann positivity across the cut; principal
  symbol = GR light-cone.
- **D8** Nonlinear classical stability / principal-symbol well-posedness (`K→1` UV hyperbolicity).
- **D9** MI evades the Cassini quadrupole by ~7 orders (passive-frame reading); the MG limb fails
  +6–14σ (this is *why* the MI reading matters, not a claim MG is the framework).
- **D10** One-loop dS: `a0` **unrenormalized** (no z⁰ tadpole; sum rule exact), linear vertex zero all
  orders (geodesy theorem), **no** transverse `(∇u)^2`, dressed KL+KMS positivity.
- **D11** `a0` additive non-renormalization **all-orders exact** (shift symmetry + unit norm); no
  two-loop transverse aether term at divergence level.
- **D12** One-loop finite parts bounded below (`‖K‖≤1`, `s=−1` confine `M^2∈(0,m^2]`); dS IR regulated
  by the `3H/2` friction gap.
- **D13** Disformal lensing kinematics ghost-free (local B, `maxord=1`), causal, Cassini-safe, `B` from
  the same `K`; `c_T=1` (ij-block genuinely computed zero).
- **D14** Matter coupling WEP-exact (η=0, universal dressing); `∇_μ T^μν=0` on-shell (Noether identity
  + MI-kernel residual 2.6e-16); `T_μν` closed-form, isotropic principal part (no slip).
- **D15** Off-circular corner **forced to a0** (τ_mem > Hubble; Milgrom-1994 orbital corner rejected as
  non-action) — the operator/measure/scale/corner are pinned.

### POSTULATED / FREE / OPEN (named, not tuned away)
- **P1** MOND sign `s=−1` — **POSTULATE** (sets dissipation *and* causality-preserving sign too).
- **P2** `a0`'s **value** `cH_Λ/Z` — **POSTULATE**; `Z`/`κ=1/2` provably **unforceable**
  (ghost-freedom + unitarity + holography); a one-parameter EFT (not zero-parameter, not derived).
- **P3** `a0` footing fork (`9.36e-11` ρ_DE vs `1.13e-10` ρ_total) — both carried; decisive tests
  degenerate between them.
- **P4 (Gap A)** off-circular closure/ordering map — **PARTIALLY PINNED**: operator/measure/scale/corner
  forced; residual is **one sign-free bracket η(β) including zero** (verifier correction — the
  off-circular *sign* is convention-dependent, *not* forced; magnitude bounded `[0…closure-B]`).
- **P5** measure — **PINNED, not free** (Herglotz + RAR calibration ⇒ unique by identity theorem).
- **P6 (Gap B)** full nonlocal `T_μν` — **CLOSED at tensor-structure + conservation**; residual (exact
  IR magnitude/multipoles of the anisotropic term) coincides with Gaps A & C; not walled.
- **P7 (Gap C)** unification — **UNIFIES minimal-disformal**; off-spherical inherits Gap A; nonlocal-B
  ghost-freedom **asserted not verified**; photon-timing LOS bound only order-of-magnitude satisfied.
- **P8** `ρ_m=m^2φ^2` loop proxy; `T_μν`/disformal-ρ_m variant — OPEN/proxy (argued to survive since
  `W_dS=0`, not computed).
- **P9** finite one-loop coefficient (candidate `δν(y)`); higher loops — OPEN. The all-n TT-vertex
  script `mi_oneloop_tt_vertex_all_n.py` has HARD-CODED `True` checks (lines 56, 66) — **do NOT lean
  on it**; TT vertex is CAS-proven only for n=1,2.

---

## 4. Exactly how complete this field theory is — where the frontier sits

**Statics are strong and now more complete than the published v4–v11 arc.** The action is written as a
*single* functional; the frame is provably passive (0 dof, surviving the matter coupling); the kernel
is a rigorous positive-measure Herglotz operator; the RAR is ring-exact and *worldline-derived* (the
first-moment identity re-proven general, not assumed circular); `a0` is loop-protected at 1 and 2 loops
at the divergence level; **matter coupling is now closed at the tensor-structure + conservation level**
(WEP-exact, `∇T=0` verified, single unrenormalized scale); **the dynamics and lensing are now one
action** in the minimal-disformal sense; and the **full coupled system is well-posed** (ghost-free,
bounded-below, hyperbolic, causal) conditional on the passive-frame premise.

**The frontier sits at three named, honest places:**
1. **Gap A — the off-circular closure map (the binding constraint).** One reduction-weighting function
   `η(β)` remains free: operator/measure/scale/corner are pinned, but beyond the first moment the map
   from `K(□_u)` to worldline dynamics is a **sign-free bracket including zero**. This blocks
   predictive off-circular dynamics (dSph σ, eccentric orbits) *and*, through inheritance, off-spherical
   lensing. It closes only via the off-circular Wightman pullback or an empirical retention proxy —
   neither done.
2. **Gap B/C residual — the anisotropic IR stress.** `T_μν` is closed in structure and conservation,
   but the exact magnitude and higher multipoles of the sole slip-capable term `γ a_μ a_ν` (= the
   lensing enhancement) coincide with Gap A and are unpinned.
3. **Two irreducible inputs.** `s=−1` (POSTULATE) and `a0`'s value `cH_Λ/Z` (POSTULATE, `κ=1/2`
   unforceable). Both footings carried.

**Bottom line.** This is a **one-scale effective field theory of the gravitational-inertial sector,
carried to a single sharp named boundary** — a passive-frame, positive-measure, loop-protected action
whose statics, matter coupling, unification, and well-posedness are established, and whose *entire*
remaining off-circular predictivity is gated by one free reduction-weighting function plus two
postulated inputs. It is **not a finished theory, not proved, and not a TOE.** The honest headline: the
MI framework is now a *self-consistent, well-posed, single-action field theory up to one bracketed
closure function and two named postulates* — the most complete honest statement the current evidence
supports.

---

*Backing scripts (all exit 0, in this directory; no hard-coded booleans after the verifier's fixes):*
`rederive_identity.py` (18 checks), `closure_map.py` (22; off-circular sign relabeled convention-
dependent in this doc), `matter_coupling_Tmunu.py` (14), `unification.py` (16, tautology at :161
removed), `wellposed.py` (30, ij-block at :204 now genuinely computed). Provenance to the frozen repo
is traced file:line in `BASELINE_ACTION.md`, `CLOSURE_MAP.md`, `MATTER_COUPLING.md`, `UNIFICATION.md`,
`WELLPOSED.md`, `VERIFY.md`. Frozen-repo published arc: Zenodo concept `21253644`,
`real_research/reviews/mi_formal_completion_2026/`.

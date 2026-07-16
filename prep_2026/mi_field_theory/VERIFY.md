# VERIFY.md — Adversarial verification of the MI field-theory build

Independent adversarial pass over the five deliverable scripts in
`/Users/carlzimmerman/new_physics/prep_2026/mi_field_theory/`. Every load-bearing
claim was re-derived or re-attacked from scratch (not trusted from the banked
consolidation). Both a0 footings (9.36e-11 canonical / 1.13e-10 alt) carried.
Rule honored: a WIN is verified as hard as a DEFICIT; a DEFICIT is verified as
hard as a WIN.

---

## 0. Re-run + hard-coded-check sweep

All five scripts **exit 0**:

| script | exit | checks |
|---|---|---|
| `rederive_identity.py` | 0 | all pass |
| `closure_map.py` | 0 | all pass |
| `matter_coupling_Tmunu.py` | 0 | 14/14 |
| `unification.py` | 0 | 17/17 |
| `wellposed.py` | 0 | 28/28 |

**Two tautological ("hard-coded True") checks found** — the exact failure mode the
task warned about (the prior `mi_oneloop_tt_vertex_all_n.py` hard-coded-True bug):

1. **`unification.py:161` — LOAD-BEARING.**
   ```python
   check("NONLOCAL B: AQUAL potential is an elliptic (spatial) constraint, no d/dt kinetic term",
         True is (a_proxy.has(sp.Derivative)))
   ```
   `a_proxy` was *defined* as `sp.Derivative(Phif(t,xx), xx)`, so
   `a_proxy.has(sp.Derivative)` is **always `True`** → the condition is `True is True`.
   This check verifies **nothing**. It guards the claim that the **nonlocal** disformal
   coefficient B (the one the script itself shows is generically required — see §5) has
   **no time-kinetic term / is Ostrogradsky-free**. That claim is therefore *asserted*,
   not machine-verified.

2. **`wellposed.py:204` — MINOR.**
   ```python
   u_i = [0, 0, 0]
   check("graviton c_T=1 exact: B u_mu u_nu has zero spatial ij block (u_i=0) ...",
         all(ui == 0 for ui in u_i))
   ```
   `u_i` is hand-set to `[0,0,0]`, so `all(ui==0 ...)` is tautological. The underlying
   fact (spatial ij block of `B u_mu u_nu` vanishes) **is** genuinely verified elsewhere
   (`unification.py:176-177`, `sp.simplify(Buu[1,1])==0` etc.), and `u_i=0` in the rest
   frame is definitional — so this one is cosmetic, not load-bearing.

The other **88 check conditions across the five scripts carry genuine
symbolic/numeric expressions** (limits, `sp.simplify(...)==0`, numeric residual
thresholds, eigenvalue counts, random-point evaluations). No other hard-coded booleans.

---

## 1. Identity theorem + first-moment closure — **UPHELD**

Re-derived independently (my own sympy, not the script's): for an **arbitrary** timelike
worldline the off-shell master identity
`d/dtau(u.a) = a.a + u.(Box_u u)` has residual **exactly 0** (pure Leibniz). On the
constraint surface `u.u=-1` ⇒ `u.a=0` ⇒ **`u_mu Box_u u^mu = -|a|^2`**.

- **Inputs = unit norm + metric compatibility ONLY.** Not circularity, not geodesy,
  not periodicity, not any Killing symmetry. Confirmed three ways in the script
  (flat general worldline; general curved `g_ab(x)`; concrete static Schwarzschild
  observer giving `u.Box_u u = M^2/[r^3(2M-r)] = -|a|^2`), and I reproduced the flat
  general-worldline residual = 0 myself. **WORLDLINE-GENERAL, not circular.**
- First-moment closure `K(Box_u/a0^2) → K(|a|^2/a0^2) = mu_fw(|a|/a0)` inverts on
  circular balance to `g_obs = nu(y) g_bar = sqrt(g_bar^2 + g_bar a0)` (ring residual
  ~1e-13, both footings) — verified.
- **Honesty preserved:** the closure is the exact FIRST moment and no more. On the helix
  the n=2 moment ratio is `1 - 1/v^2` (diverges as v→0), so the moment tower does **not**
  collapse and no finite moment-matching pins the off-circular reduction. This is
  correctly reported as the genuine open structure, not papered over.

Verdict: **UPHELD.** The derivational backbone is real and worldline-general.

---

## 2. Closure map — **DOWNGRADED** (headline holds; the off-circular SIGN pin is over-claimed)

**What is genuinely pinned (I re-verified each, independently):**
- Herglotz sum rule `∫dμ/|t| = 1`: region-B share `= 2/pi` exact (sympy), total = 1 to 1e-8.
- `|K(-w^2+i0)| = 1` on the oscillatory branch (pure phase — no amplitude MOND from any
  orbital frequency): `ReK^2+ImK^2 = 1` exactly.
- Corner forced to a0 by action-descent: `tau_mem = 2c/a0 = 203 Gyr (canonical) / 168 Gyr
  (alt) > Hubble time`; every bound system has `omega_orbit/omega_c ≫ 1e3`. This
  genuinely rejects the Milgrom-1994 orbital-averaging corner as a non-action scale — the
  real narrowing over the prior SPEC.

These pins are **real** — the operator, measure, and corner location are pinned. The
lane headline **"PARTIALLY PINNED"** stands.

**Where it smuggles a choice — the off-circular SIGN sub-claim:**
The lane advertises the off-circular offset SIGN and its anisotropy-correlation as
**FORCED and "MG-impossible"** (a clean discriminator). I attacked this hardest and it
does **not** hold at the rigor of the other pins:

- The in-script check (`closure_map.py:242-244`) evaluates
  `coef_signs = [-dlnmu_dlnx(x)*b(2b+1)/2 ...]` and checks they are `< 0`. But
  `dlnmu_dlnx > 0` and `b(2b+1)/2 > 0`, so this is checking that `-[positive]*[positive]`
  is negative — **manifestly true by construction.** The load-bearing physics step, the
  identification of that product with `Delta ln g_obs`, lives only in a **comment**
  (line 239), never derived in code. This is a near-tautological check dressed as a
  verification of the sign.
- I constructed the sign **independently**: the RAR map `g_obs(g_bar) =
  sqrt(g_bar^2 + g_bar·a0)` has `d²g_obs/dg_bar² = -a0²/[4 g^{3/2}(a0+g)^{3/2}] < 0`
  everywhere — **strictly concave.** By Jensen, a legitimate *average-then-dress*
  closure (positive-weight history average of the acceleration, fully admissible under
  the five principles) sits **ABOVE** the pointwise closure — a **POSITIVE** offset
  (confirmed numerically on a Kepler orbit: +0.001 to +0.07 dex, growing with
  eccentricity). This is the **opposite sign** to the lane's asserted negative epicyclic
  coefficient.
- Therefore the off-circular SIGN depends on the **averaging order / which quantity is
  averaged** (`g_bar` vs the self-consistent felt `|a|`), i.e. on a *choice inside the
  admissible family*, not forced by the principles. Positivity of the measure/KMS forbids
  a negative *weight*, but it does **not** fix the sign of the RAR-plane residual.

This is consistent with — and strengthens — the lane's own honest statement that the
magnitude bracket **includes 0** (closure A is MG-identical) and that the residual is
"FREE-bounded." The correct reading is: the residual is **more free than the verdict's
headline suggests** — the SIGN is convention-dependent, so the "MG-impossible clean
discriminator" is a property of one *chosen* endpoint (closure B under one averaging
convention), **not a forced prediction of the theory.**

Verdict: **DOWNGRADED.** Operator/measure/corner pinning **UPHELD**; the
"off-circular sign forced / MG-impossible discriminator" sub-claim **DOWNGRADED** to
"one free reduction-weighting function whose sign is also convention-dependent." The
honest object is a bracket that includes zero **and** both signs at the offset level.

---

## 3. Matter coupling (∇T=0, η=0/WEP, c_T=1) — **UPHELD**

- **∇_μ T^μν = 0:** rests on diffeomorphism invariance. The generic canonical Noether
  identity `d_μ Θ^μ_ν = -(EL) d_ν φ` is verified symbolically for an **arbitrary**
  `L(φ,∂φ)` (residual = 0), and **instantiated** with the actual MI acceleration kernel
  (`L = ½ s ρ K(a.a/a0²)`, `u=(cosh ξ, sinh ξ)`), residual `~1e-16` at 12 random points.
  This is a real verification, not an assertion. Conservation holds on-shell with an
  **l=0 frame source soaked by λ** — no l=2 shear obstruction, so no Cassini Bianchi lock
  is forced. **No inconsistency found.**
- **η=0 (WEP):** the dressing `W = s u^μ K u_μ` multiplies `ρ_m` universally and carries
  no species label; the balance inverts species-independently. Exact WEP. Correct.
- **c_T=1:** structural — MI lives in the matter kinetic sector, the graviton kinetic
  operator is pure `S_EH`. Correct (the disformal photon-sector c_T is a *separate*
  question handled in §4/§5).
- **Honesty preserved:** the full `T_μν = α u u + β g + γ a a` is the **algebraic/leading**
  part. The variation of the Christoffels inside `a^μ = u^b∇_b u^μ` (the connection piece
  of `δ(a.a)/δg`) — i.e. the exact IR magnitude of the anisotropic `γ a_μ a_ν` stress and
  the lensing enhancement — is correctly **flagged OPEN (gap C)**, not smuggled in.

Verdict: **UPHELD.** Cleanest lane. Gap B closed at the tensor-structure + conservation
level; the connection piece honestly reported open.

---

## 4 & 5. Unification (Ostrogradsky) + Well-posedness (dof recount)

### Ostrogradsky audit — **UPHELD for local B, DOWNGRADED for nonlocal B**

- **Local B:** genuinely verified — perturbing the metric potential, the disformal
  `B(a)F²` and matter `K(a²)` Lagrangians contain **only first-order** fluctuations
  (`max d-order = 1`, `unification.py:152`, `wellposed.py:157`). The classic
  modified-inertia `L(ẍ)` Ostrogradsky trap is genuinely evaded because `a = u·∇u` is a
  **field gradient** (d¹), not a worldline `ẍ`. Real result.
- **Nonlocal B — the danger the task named:** the script itself shows (`unification.py:224-228`)
  that off spherical symmetry `curl(ν g_bar) ≠ 0` (order-unity for two point masses), so a
  local B **fails** and B **must** be the nonlocal AQUAL potential — i.e. the nonlocal case
  is the **generic** one, not an edge case. Its Ostrogradsky-freedom is guarded by the
  **tautological check at line 161** (`True is True`, §0). The physical argument (elliptic
  inverse-Laplacian constraint ⇒ no time-kinetic term ⇒ no propagating ghost, at the
  constraint-field standing of the Newtonian potential) is **plausible and probably
  correct**, but it is **asserted, not machine-verified**. This is a real gap in the
  verification, on exactly the field the task flagged as the hazard.

### DOF recount — **UPHELD**

Independent recount: **2 graviton + 2 photon + standard matter + 0 frame.**
- Graviton 2 (pure `S_EH` on g), photon 2 (Maxwell on `g̃`, Lorentzian for B<1) — standard.
- **Frame u = 0 propagating dof** is the load-bearing MI claim and is genuinely verified
  **two independent ways:** (i) the unit-norm 2nd-class Dirac pair `{χ1,χ2}=2(u.u)`,
  `det=4(u.u)²→4`, **survives the matter coupling** — checked with a matter-dressed
  momentum `π = π_free + Q(u)` (the bracket is kinematic, independent of Q); (ii) the
  frame principal symbol `(u.k)²→k0²` has a double root `k0=0`, zero group velocity, no
  spatial wave-cone. Additionally, `S_u` has **no `(∇u)²` kinetic term at all**, so u is
  purely auxiliary — 0 dof is over-determined. **No miscount.** No hidden aether mode.

### Ghost / stability / causality — **UPHELD**

`K∈(0,1]` (positive dressed inertia), `K'>0` (operator-monotone/Herglotz), UV propagator
residue `+1` (single healthy pole), `g̃` Lorentzian iff `B<1` with `B~6-7e-7 ≪ 1` at
galaxy scale (both footings), photon null cone nested in g iff `B≥0` iff `s=-1` (so s=-1
is also the causality-preserving sign). All genuinely checked. No ghost or instability
manufactured or found. The verdict correctly rests on the **passive-frame/khronon
premise** (flagged as the load-bearing hinge: a dynamical khronon would give `a~∂²T`).

### c_T=1 (unification)

Genuinely verified where it counts: `B u_μ u_ν` has zero spatial ij block
(`unification.py:176-177`, real `sp.simplify==0` checks) ⇒ TT graviton sector untouched
⇒ `c_T=1` exact. The **photon** disformal timing over Mpc line-of-sight is correctly
**flagged as an open, only-order-of-magnitude-satisfied bound**, not asserted safe.

Verdict: **Unification DOWNGRADED** (structure + local-B ghost-freedom + c_T=1 + Cassini
all UPHELD; the **generic nonlocal-B Ostrogradsky-freedom is asserted, not verified** —
tautological check at line 161). **Well-posedness UPHELD** (dof recount confirmed, no
ghost/instability/acausality, conditional on the passive-frame hinge as honestly stated).

---

## 6. TOE / SM-drift / "theory completed" language — **CLEAN**

Swept all five `.md` files. **No overclaim found.** The docs explicitly hedge:
`BASELINE_ACTION.md:6` — "**not** a claim that the theory is complete";
`MATTER_COUPLING.md:179` — "closed **at the tensor-structure + conservation level**";
`UNIFICATION.md:124-127` — "**exact where the closure is pinned** ... as complete as the
dynamics sector itself, **and no more**". `s=-1` and a0's value are kept POSTULATED
throughout. No "theory of everything", no "derives the Standard Model", no "proved the
theory". The 2026-06-23 retraction is respected.

---

## Bottom line

| Lane | Verdict |
|---|---|
| Identity + first-moment closure | **UPHELD** (worldline-general, re-derived) |
| Closure map | **DOWNGRADED** — operator/corner pinned; off-circular **sign not forced** (convention-dependent; the sign check is near-tautological, my concave-RAR Jensen construction flips it) |
| Matter coupling (∇T=0, η=0, c_T=1) | **UPHELD** (Noether verified; connection piece honestly open) |
| Unification (Ostrogradsky) | **DOWNGRADED** — local-B genuine; **generic nonlocal-B ghost-freedom asserted, not verified** (tautological check `unification.py:161`) |
| Well-posedness (dof recount) | **UPHELD** (2+2+0+matter confirmed two ways; no ghost/instability; passive-frame hinge honest) |
| TOE / overclaim language | **CLEAN** |

**Two hard-coded/tautological checks must be fixed** for the repo to be honestly
self-verifying: `unification.py:161` (load-bearing — nonlocal-B Ostrogradsky) and
`wellposed.py:204` (cosmetic — c_T=1, fact verified elsewhere). No ghost was manufactured,
no conservation broken, no dof miscounted, no matter coupling that breaks c_T=1, and no
TOE drift. The one genuine over-pinning is the **closure-map off-circular sign** — which,
corrected, makes the theory's residual off-circular freedom honestly *larger* (sign-free),
fully consistent with the framework's own "FREE-bounded" standing. `s=-1` and a0's value
remain postulated; both footings carried.

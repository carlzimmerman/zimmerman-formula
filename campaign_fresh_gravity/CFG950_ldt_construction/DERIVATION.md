# CFG950 DERIVATION: the labelled-domain theory (LDT), written down and tested

**Provenance.**
- Criteria: `FROZEN_CRITERIA.md` (324edbf93, committed alone first).
- Amendment: `AMENDMENT_A1_post_hoc.md` (fb9af871f), **POST HOC**: it concerns only the merger-toy metric f3, and was
  committed alone before the script change.
- Every load-bearing step has a sympy or numeric check in `cfg950.py`; check names are in brackets.

**Settings.**
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled.
- Cold energy, no particle species. Framework-native inputs.
- Not "theory closed". Nothing here says the data favour the framework.

**Notation.** K = 4πG; u = |Dχ|; R(u) = u²/(a₀ − u); D_full(u) = u + R(u) = a₀u/(a₀ − u).

## Class

**Frozen rule, frozen metrics: NOT CONSISTENT AS SPECIFIED.** The only FAIL is test (f)'s toy metric f3. With equal-mass
shells, that metric is pinned at the innermost shell, whose field step is δu₁ ≈ 0.73 at every resolution, so it cannot
converge. A1 shows this with a diagnostic table. No structural statement shows a FAIL generic to LDT, so INCONSISTENT is
not claimed.

**Under the post-hoc amendment A1 (f3 only): LDT CONDITIONAL.**

| test | grade |
|---|---|
| (a), (b), (c), (d), (h), (i) | PASS |
| (e) | CONDITIONAL |
| (f) | PASS (FAIL as frozen) |
| (g) | CONDITIONAL |

The conditions, stated with equal weight:
1. **(e) Energy is not conserved by any dynamical field at label events.** Labelling a galaxy's medium injects 0.17–0.94
   of the system's |E_grav|, and a merger 0.54–0.70 of it. Theorem T-LE shows that bound cold medium cannot pay this from
   its kinetic energy. The books close only through R-E, a declared non-dynamical label-energy scalar. Momentum is
   conserved exactly.
2. **(g)** inherits CFG938's premises: γ > 0, ρc² > Du/K, per-label single stream. Nonlinear well-posedness is unproved.

The label sector is non-local and has no action. It is declared as a cost and is never scored as a pass.

---

## 1. The specification

### 1.1 Fields and the action between label events
**Fields.**
- The metric g.
- Baryons S_b, geodesic.
- The cold medium as populations q = 0, 1, 2, …, each with comoving labels φ_q^I, number density n_q and current
  J_q = n_q u_q. Population q = 0 is unlabelled, untethered dust.
- For each label q ≥ 1, an auxiliary potential χ_q and a multiplier λ_q.

**Action.** With the membership of every element fixed:

  S = ∫√−g [ c⁴R/16πG − Σ_{q≥0} m c² n_q − Σ_{q≥1} ( W_full(u_q) + (3γ/4K²) τ_q:τ_q ) + Σ_{q≥1} λ_q (D_(q)² χ_q − K m n_q) ] + S_b,

with:
- u_q² = h_(q)^{μν}∂_μχ_q∂_νχ_q, using label q's own frame;
- W_full(u) = [−a₀u − a₀² ln(1 − u/a₀)]/K;
- γ = KL*²/2;
- τ_q the traceless medium-frame tidal tensor of χ_q.

This is CFG938's parent with one tether copy per label, i.e. CFG945's H1 written for populations. **No θ appears in the
action [T-G].**

Since every term is diffeomorphism-invariant for fixed membership, ∇_μT^{μν} = 0 holds between events.

### 1.2 Static weak-field equations

| quantity | equation |
|---|---|
| gravity | ∇²Φ = K(ρ_b + Σ_{q≥0} ρ_q) |
| medium potentials | ∇²χ_q = Kρ_q; the constraint is linear, so Σ_q χ_q is the medium's total potential |
| force on a star | −∇Φ |
| force on unlabelled dust | −∇Φ |
| force on label-q medium | f_q = −∇Φ + (D_full(u_q)∇̂χ_q)_L (+ stiffness) = −∇Φ_b − Σ_{p≠q}∇χ_p − ∇χ_0 + (R(u_q)∇̂χ_q)_L |

In the force on label-q medium, the tether's linear part cancels label q's own Newtonian pull (D-T, CFG941) but no other
label's.

**Spherical equilibrium of label q:**

  R(u_q) = g_b + Σ_{p≠q} u_p.

So other labels' media act like baryons for label q. This is CFG945's two-label equation, and reported item R1 follows
from it.

### 1.3 The label sector: rules (i)–(v) (no action; causal; non-local where stated)

| rule | statement | locality |
|---|---|---|
| (i) assignment | **Latch** when the element's own θ = ∇_μu^μ first becomes ≤ 0. **Identity**: the label of labelled medium within L* (24 pc; 1 kpc bracket) whose ball domain contains the element, or the dominant one; if none lies within L*, seed a new label | the trigger is local; the identity is local within L* |
| (ii) merge M-R | Ball domain r_dom,p: the outermost r about p's centroid with ⟨\|τ_p\|⟩(r) ≥ ⟨\|τ_ext\|⟩(r). Label p merges into the dominant external label when r_dom,p = 0, by fractional transfer over τ_m | non-local (centroid, shell averages); instantaneous in the NR limit |
| (iii) source/draw | The phantom is label q's own rest mass. Relocation is the medium's motion under the action plus internal viscosity, with mass and momentum conserved by dynamics | local |
| (iv) satellites, L2 | Keep the label. An element outside its own ball domain re-latches to the largest-mass label whose domain contains it. One-way: only to a larger-mass label | non-local (ball domains) |
| (v) debris | Foreign or unlabelled medium inside a settled galaxy's edge must be ≤ q_max = 3.5e-7 of its medium | a requirement on the rules |

What the rules leave as debris. Every element inside a settled galaxy has latched (it lies in a collapsed, converging
region), and lies in one ball domain. Stripped satellite medium is re-latched to the host. Host medium transiting a
satellite is a uniform background inside it and is part of the host's tidal field (§4). Co-spatial foreign labels remain
only during merger transfers. So the rules give zero debris in settled galaxies. A numerical engine must still keep
q ≤ 3.5e-7, a requirement passed to CFG952.

### 1.4 R-E (declared bookkeeping, not dynamics)
At each event a transferred element receives Δe_L = −(its share of ΔE_W). The scalar e_L is comoving, gravitates as
ρe_L/c², and has no NR dynamics.

### 1.5 Primary formulation and the comparison with (B)
**T-EQ (PASS).** (A)'s settled single label and (B)'s P-S configuration have the same gravitating density, provided B's
edge is the kernel's own supply root (q = 1). The check gives max |g_A/g_B − 1| = 4.4e-16 on NGC 3198 and CFG847's five
systems, both footings, out to r_ON. Statically, LDT-(A) is CFG947's N1 with the kernel's own root.

Dynamically they differ:

| | (A) per-label tether (primary) | (B) per-domain source (CFG947 N1) |
|---|---|---|
| action | yes, between events | none (retarded kernels) |
| phantom | real medium; must settle (dissipation) | instantaneous source; cold particles stay geodesic |
| positivity / edge / zero-sum | automatic (mass conservation) | cap, clip and own-root kernel imposed |
| momentum in relocation | automatic (internal forces) | needs a dipole-consistent draw (T-M; M2 bites) |
| merge | Φ continuous (J_LDT = 0) | own-label phantom recomputed: jump 0.33–0.36 in the toy (M5) |
| satellites | tidal residual 1.6e-5 – 2.0e-3 | 0 at monopole order |
| within-domain self-gravity | none (D-T per label) | the cold dust gravitates; the source is pinned inside the edge |

---

## 2. (a) The law in a single-label galaxy: PASS

**a1** [K1].
- Single-label static EL: −(−a₀g_N + g_N u + u²)/(−a₀ + u) = 0, i.e. R(u) = g_N.
- NGC 3198 (43 radii, Υ = 0.61): max |g/g_law − 1| = 2.2e-16 on both footings.

**a2.** The sympy limit of V⁴/(G M_b a₀) is 1. At y = 1e-14 the numeric value is 1 + 1.0e-7, within 4e-16 of the exact
law's own value.

**a3. The edge.** The label mass is the census catchment cold mass, M_c,q = (1 − f_b) M_ta = 53.6 M_b (engine census,
native Δ_ta(0) = 11.8308). The supply root with the simple kernel is analytic:

  (√(y² + 4y) − y)/(2y) = N  ⇒  y_e = 1/(N(N + 1)),  r_e = r_M √(N(N + 1)).

| | canonical | alt |
|---|---|---|
| r_e (kpc) | 453.9 | 412.9 |
| E7 RAR-kernel edge (kpc) | 454.0 | 413.0 |
| r_ON (kpc) | 1151 | 1151 |

The last radius (44.1 kpc) and the deep points y = 1e-2 / 1e-3 (84 / 265 kpc) are inside.

**θ-latch variant (reported).** With the θ-latch label mass (§3), r_e = 214 / 252 / 290 / 317 / 344 kpc (canonical) for
ε = 0.2 / ⅓ / 0.5 / ⅔ / 0.9. The last radius stays inside. The deep point y = 1e-3 falls outside for ε ≤ ⅓.

**Costs** [K3]:
- Two co-spatial equal labels miss NGC 3198 by 4.12 / 4.61 (floor g → a₀).
- Debris q = 1e-6 already gives 2.6e-6. So q ≤ 3.5e-7 is required.

## 3. (b) FRW, latching and growth: PASS; and the comparison with class A's catchments (T-θ)

**b1.** The unlabelled medium has F = −mc²n on FRW: ρ = c²m/a³, p = 0, so w = 0 and the stress is isotropic.

**b2.** At linear order θ = 3H(1 − fδ/3), so a latch needs δ ≥ 3/f (= 3 in EdS). There are no labels in the linear
regime. For the top-hat, θ = 3 sin η/(B(cos η − 1)²) vanishes at turnaround (η = π), where δ_lin = 1.0624 and
1 + δ = 9π²/16 = 5.5517. The crossing is transversal: θ̇(π) = −3/(8B²) ≠ 0.

**b3.** No tether acts in the linear regime, so n = 1.000000000000. A collapsed label is a point mass that falls
universally in large-scale fields, since external fields do not enter its tether. MUTATE M3 (one global always-on label)
brings back n = 0.69433.

**T-θ (PASS).** For EdS power-law profiles δ̄_i ∝ q^{−3ε}, pre-shell-crossing cycloids give self-similar fronts:

  ∂ln J/∂ln a = 3 + δ d/dδ[2 ln F + ln(F − 3εδF′)],  F = (1 + δ_NL)^{−1/3}.

The θ = 0 front lies inside the turnaround (v = 0, E3-type) front:

| ε | 0.2 | ⅓ | 0.5 | ⅔ | 0.9 |
|---|---|---|---|---|---|
| δ_lin at θ = 0 (turnaround: 1.0624) | 1.237 | 1.296 | 1.333 | 1.352 | 1.368 |
| f_θ = M_θ/M_ta | 0.467 | 0.551 | 0.635 | 0.696 | 0.755 |

f_θ = (δ_θ/δ_ta)^{−1/ε}. It is smallest for the shallowest profiles: in a shallow profile a small lag in δ is a large
lag in Lagrangian radius. The exact top-hat (f_θ = 1) is a degenerate case, not the ε → 0 limit.

**Reading.** A local turnaround latch labels 47–76% of class A's catchment mass. The census label mass is the graded
primary.

## 4. (c) No hover and (i) the satellite data bound: both PASS

**Setup.** CFG882's dwarfs H1–H3 at 50 / 100 / 250 kpc in a 6e10 M⊙ host, both footings, with the L2 ball domain:
r_dom = 1.08–34.2 kpc, r_dom/R = 0.012–0.143.

**(c).**
- The own-label medium falls with its stars: Δa/g_host = 1.57e-5 – 2.03e-3 (tidal residual only; the uniform part is
  exactly 0). Lines: ε_B = 0.3443 / 0.3170, recomputed from the CFG874 replica.
- CFG941's 0.01 line is met.
- 1-Gyr two-body integrations with Δa = the tidal residual keep stars and medium bound in 18/18 cases
  (min P_max/Δa = 182; max separation 9e-4 r_dom).

**(i).**
- The uniform-field EFE on the satellite phantom is exactly 0 dex, against δ_c = 0.0816.
- The tidal term at the scale radius is reported: −0.0002 to −0.0572 dex. The extreme is alt, H2 at 50 kpc. CFG945's
  README quotes the canonical extreme, −0.052; CFG945's JSON has the same −0.0572 for alt.

**Why it works.** Labels are escape E1 of Theorem S (CFG945). MUTATE M1 (one shared label) restores CFG941's hover,
1.0167–1.1067, exactly.

## 5. (d) Slip: PASS
- **Per label** (CFG847's five systems, L* ∈ {0, 24 pc, 1 kpc}): worst s_grad = 5.79e-6, s_847 = 1.540e-5.
- **Satellite inside a host** (summed label stresses, upper bound): 2.7e-8.
- Line: 1.9e-5.

## 6. (e) Conservation through label events: CONDITIONAL

### 6.1 Momentum closes exactly
**Theorem T-P.**
- An event changes membership only; positions and velocities are continuous through it.
- Each epoch's action is translation-invariant.
- Therefore total momentum is continuous at events and conserved between them.

**Check.** The 1-D slab toy has baryons, two labels and dust, with exact pair gravity and a per-label gap-energy tether
whose forces telescope to zero. Through latch, re-latch and merge: |P(t) − P(0)|/Σm|v| ≤ 8.1e-14 (line 1e-12). Each slab
changed label at most twice, and one label remained at the end.

**Contrast.** A prescribed class-A relocation (MUTATE M2: asymmetric draw, ε = 0.3) breaks P_m + Ḋ_s by 13% of Σm|v|. The
symmetric control holds to 6e-17 (CFG947 T-M).

### 6.2 Energy jumps, and why no dynamical field can pay them
**First-order chemical potential** (sympy integrand identity):

  δE_W/δm(x) = Kλ_q(x) = ∫_x^∞ D_full(u_q) dr > 0.

Adding medium to a label switches off its gravity on that label (D-T), so the energy rises.

**T-LE (PASS).** For x < r_e,

  Kλ_q(x) − [Φ(r_ON) − Φ(x)] = GM_c/r_ON + ∫_{r_e}^∞ R(GM_c/r²)dr − GM_b(1/r_e − 1/r_ON) ≡ Δ,

which is independent of x, because R(u) = g_b on the law.
- **NGC 3198:** Δ = 9.34e9 / 9.31e9 m² s⁻² ≈ (97 km/s)². The x-independence holds to 4e-15 over the 43 radii.
- **M_b grid (1e7–1e15 M⊙):**
  - Δ/(G M_b/r_e) = 4.6 → 19.5 (rising to M_b ≈ 3e10), then 17.1 → 1.75 at 1e14 and 2.9 at 1e15 (canonical);
  - alt is 4.1–17.7, 1.5–2.6;
  - Δ > 0 everywhere.
- **Consequence.** Medium falling from rest at r_ON, or on any bound orbit with apocentre ≤ r_ON, cannot pay the
  labelling energy at any point. A latch at turnaround has no kinetic energy at all. So no momentum-conserving,
  energy-conserving latch of bound cold medium exists.

**The jumps** (closed forms: joining inside-out at the final radii gives E_W(final); joining at r_ON gives the label's
exterior E_W beyond r_ON):

| event | canonical | alt |
|---|---|---|
| NGC 3198 label assembly ΔE / \|E_grav\| (\|E_grav\| = 1.27e53 / 1.39e53 J) | 0.188 – 0.939 | 0.172 – 0.940 |
| its medium's own Newtonian self-binding (for scale) | 1.16e53 J | 1.28e53 J |
| concentric merger of two NGC-3198-like labels, 1:1 (outside the wall) | 0.70 \|E_grav,merged\| | 0.70 |
| same, 1:3 | 0.54 | 0.54 |
| instantaneous merge inside the core | **+∞**: u₁ + u₂ ≥ a₀ (the W_full wall) inside the radius enclosing 0.7% (1:1) / 0.05% (1:3) of the medium | same |
| re-latch of a shell at r_dom (H1–H3), per unit mass / (g_host R) | +1.67 … +3.10 | +1.58 … +3.03 |

**The wall.** A merged label cannot hold u ≥ a₀. In Newtonian-regime cores two media therefore cannot be relabelled at
once. M-R must transfer gradually while the tether expels the excess, so the injected energy depends on the path. In the
code-unit merger toy the 1:3 merge jumps by +3.34 = 0.70|E|. The 1:1 discrete merge is +∞ at the centre, because the two
innermost shells coincide (A1.2; the continuum superposition stays at 0.78 a₀).

**R-E cost.**
- max |e_L|/c² = 1.7e-6 / 1.8e-6.
- Post-Newtonian (Bianchi) residual at events ≈ ΔE/(M_c c²) = 2.6e-7 / 2.9e-7.
- R-E closes the books globally. Local conservation still fails at events, because χ_q responds instantaneously.

**Grade: CONDITIONAL** by the frozen rule: momentum closes; energy closes only through R-E; the violation is quantified.
**MUTATE M6:** with the tether removed the labelling jump is exactly 0, so the jumps come from the tether.

## 7. (f) Mergers: FAIL as frozen; PASS under post-hoc A1

**T-T (PASS).** R(u₁) − u₂ = R(u₂) − u₁ ⟺ D_full(u₁) = D_full(u₂). Since D_full′ = a₀²/(a₀ − u)² > 0, this forces u₁ = u₂.
Concentric labels therefore have equal tidal fields at every radius (NGC 3198 two-label residual 2e-15). An element-wise
tidal rule ties and cannot finish a merger. **M-R must be a whole-label rule.** It acts through the ball domain, whose
radius → 0 at a tie or under dominance.

**Toy.** Code units G = a₀ = 1. Concentric Hernquist baryons (b = 2) with M_b2/M_b1 = 1 and ⅓. Each label holds 6 M_b
in its isolated settled law profile. They are superposed and merged at once (M-R fires: tie or dominance at the centre).
Then the overdamped gradient flow of the exact (analytic) shell energy runs.

| | 1:1 | 1:3 |
|---|---|---|
| f1 J_LDT (field jump across the merge) | **0** | **0** |
| class-A-type J_A (own-label phantoms recomputed) | 0.357 | 0.325 |
| f2 flow: distance to the merged equilibrium | 0.258 → 0.0112 (×23) | 0.163 → 0.0064 (×25) |
| f2 rejected steps (energy-monotone step control) | 451 of 6951 | 238 of 3738 |
| heat (from first finite state) / \|E\| | 0.41 / 11.36 | 0.119 / 4.79 |
| f3 frozen: max midpoint dev, all shells, N₀ / 2N₀ | 0.121 / 0.121 | 0.125 / 0.125 → **FAIL** |
| A1 f3-A: exact discrete identity ⟨R⟩_k = g_b(r_k) | ≤ 1.4e-11 | ≤ 1.0e-11 |
| A1 f3-B: resolved-range dev (r ≥ 0.447), N₀ / 2N₀ | 2.60e-3 / 5.87e-4 | 2.50e-3 / 9.08e-4 → **PASS** |
| medium mass | exact | exact |

The gravitational field stars and light feel is continuous through the merge (J = 0), because the phantom is real mass.
The field relaxes over the settling time to the merged law, which is reached with the merged supply root as its edge.
The same total change (J_A) arrives continuously instead of as a jump.

**MUTATE.**
- M4: without M-R the two-label equilibrium misses the law by 1.9 (1:1) / 1.7 (1:3) in the toy, and 4.12 / 4.61 on
  NGC 3198.
- M5: the class-A-type recomputation jumps by 0.36 / 0.32.

## 8. (g) Well-posedness: CONDITIONAL
- **g1 (per label).** ω²/(Kρ₀) = (kL*)²/2 + R′cos²θ + (R/u)sin²θ, with minima 0.100 / 1.000 / 9.000 / 99.000 at
  u₀/a₀ = 0.0909 / 0.5 / 0.9 / 0.99, and Im ω = 0. Inertia margin ≥ 5.9e4 on CFG847's systems.
- **g2.** The action has no θ, so F_θθ = 0 and the kinetic coefficient is ρ₀ [T-G]. CFG944's Theorem G does not apply:
  its hypothesis is a local L(θ, u), and the latch sits outside the action.
- **g3.** Co-located labels interpenetrate. Two-label WKB gives max Im ω/√(K(ρ₁ + ρ₂)) = 0.707 ≤ 1: bounded and
  k-independent. The label field enters only through n_q, so a label front is a material, non-characteristic surface.
- **g4.** Under the one-way rule an element changes label finitely often (at most 2 in the toy), so there is no Zeno
  chattering. The latch is transversal (θ̇ ≠ 0).
- **Premises inherited:** γ > 0, ρc² > Du/K, per-label single stream. Nonlinear well-posedness (A3) is unproved, and
  events make the forces piecewise-smooth in time.

## 9. (h) Forced edge and zero-sum: PASS
- **h1.** M_ph(< r_ON)/M_c,q = 2.02–11.52 > 1 for M_b = 1e7–1e15 on both footings, so the law must end inside the
  catchment. CFG947's T-E table is reproduced (K4: min 1.8466).
- **h2.** Edge per galaxy (simple-kernel supply root; E7 agrees to ≤ 0.12%):

| system | N = M_c/M_b | r_e canonical (kpc) | r_e alt (kpc) | r_ON (kpc) | r_e/r_M |
|---|---|---|---|---|---|
| NGC 3198 | 53.6 | 453.9 | 412.9 | 1151 | 54.1 |
| dwarf 1e7 M⊙ | 53.6 | 6.6 | 6.0 | 69 | 54.1 |
| MW 6e10 M⊙ | 53.6 | 511.8 | 465.5 | 1247 | 54.1 |
| group 1e12 M⊙ | 14.9 | 594.8 | 541.0 | 2080 | 15.4 |
| cluster 1.5e14 M⊙ | 6.0 | 3044 | 2769 | 8138 | 6.4 |

  Over the grid, r_e/r_ON = 0.088–0.513.
- **h3.** 0 / 0 SPARC points beyond their galaxy's r_e (175 galaxies), and none for NGC 3198.
- **h4.** Zero-sum is mass conservation of the labelled medium. It is exact in both toys, and events move no mass.

## 10. Reported (no class weight)
- **R1. Other labels act like baryons for a label's equilibrium.** A satellite's own-domain medium is 41–854 times its
  stars (H1–H3 × 3 radii). A host's law beyond a satellite therefore reads g_b + G M_sat,med/d². The three CFG882 dwarfs
  at 100 kpc carry 1.7e9 M⊙ of own-label medium, 2.8% of a 6e10 M⊙ host's baryons. Class A's E4 reads baryons only.
  This is an LDT-specific prediction (hosts with massive satellite systems carry extra law response), untested here.
- **R2. A label without baryons disperses.** With g_b = 0 the force on labelled medium is +R(u_q)û outward. Pure cold
  minihalos cannot persist as labelled objects.
- **R3. (B)'s costs** (CFG947): no action; cap; deficit clip; own-root kernel; T-M; T-L non-additivity (here J_A
  0.32–0.36).

## 11. CFG678 scorecard (20 gates; CFG678's rules: a prescribed rule scores UNTESTED, never PASS)

| gate | status | source |
|---|---|---|
| A1 ghost / 2nd order | CONDITIONAL | per label CFG938 inertia condition (margin ≥ 5.9e4); no θ in the action (T-G); label sector has no action |
| A2 hyperbolicity | CONDITIONAL | g1 (ω² ≥ 0), g3 (bounded co-located labels); needs γ > 0 |
| A3 nonlinear WP | UNTESTED | not proved; event-driven discontinuities |
| A4 strong coupling | UNTESTED | not computed |
| A5 GW at c | PASS | Einstein–Hilbert unmodified; no curvature couplings (structural) |
| A6 BH exteriors | UNTESTED | none |
| A7 radiative | DECLARED | CFG320 |
| B1 switch from variation | UNTESTED | the switch is the action-less label sector (prescribed); momentum conserved (e1), unlike CFG48's gate; CFG944 Theorem G: no local variational version |
| B2 a₀–Λ tie | UNTESTED | a₀ constant in W; κ = ½ FITTED |
| B3 cold sector | CONDITIONAL | per label CFG938 (well-posed, lenses like mass, slip 1.5e-5); energy closes only through R-E |
| C1 Cassini | CONDITIONAL | inherits CFG938's C1; differential free fall of tethered satellites removed (c) |
| C2 SPARC | PASS | single-label law (a); no point beyond its edge (h3); CFG4 rms 0.1003 / 0.0991 ≤ 0.110 |
| C3 early types | FAIL | inherits CFG529 |
| C4 cluster lensing | NOT DECIDED | as CFG678 |
| D1 zero field | UNTESTED | not run |
| D2 growth | UNTESTED | linear regime dust, n = 1 (b); the CFG596 line needs an LDT PM engine (CFG952); class-A shear passes do not transfer automatically |
| D3 flat a₀(z) | PENDING | sealed tests 2026-11-06 / 2026-11-28 |
| E1–E3 | DECLARED | κ = ½ FITTED |

Against CFG941/945:
- the hover is gone;
- D2's linear flag is gone (dust, n = 1);
- B3/A2 stay CONDITIONAL;
- B1 is not passable in LDT by construction;
- C3 stays FAIL.

## 12. Costs, open items, and what is not claimed

**Costs (all of them).**
1. **A non-local, action-less label sector**:
   - θ-latch;
   - contact inheritance within L*;
   - ball domains, from centroids and shell-averaged tidal strengths;
   - one-way, mass-ordered re-latch;
   - whole-label M-R with fractional transfer over τ_m (a declared time scale);
   - seeding.
2. **Energy is not conserved by any dynamical field at label events** (O(1) of binding energies; T-LE). It is closed only
   by R-E, and local (post-Newtonian) conservation fails at ~3e-7.
3. **Settling needs a dissipative extension** (internal viscosity); its rate is not derived.
4. **Auxiliary fields:** one pair (χ_q, λ_q) per label.
5. **Per-label single stream** and CFG938's conditions.
6. **Single-label galaxies** (debris ≤ 3.5e-7) are enforced only by the rules.
7. **Instant merging is forbidden** wherever the summed field reaches the W_full wall. Merges are gradual, with
   path-dependent energy.
8. **Other labels' media act as baryons** (R1), and baryon-free labels disperse (R2).
9. **θ-latch label masses** are 47–76% of the catchment (smaller edges).

**Open.**
- An LDT PM engine and the D2 test (CFG952).
- Mergers and clusters under LDT (CFG951).
- Whether any label dynamics with an action exists. CFG944's Theorem G excludes the local L(θ, u) class.

**Not claimed:**
- that LDT is viable or complete;
- that labels have local dynamics;
- that κ, a₀, Ω_c/Ω_b or L* are derived;
- that the class-A shear passes transfer;
- any data verdict beyond the framework-native bounds above;
- "theory closed".

## 13. Controls and disclosures

**K controls: 7/7 pass.**

| id | result |
|---|---|
| K1 | NGC 3198 law 2.2e-16 / 2.2e-16 |
| K2 | growth exponents 0.609545 / 0.694330 / 1.000000000000 |
| K3 | CFG945's 18 tidal ε, two-label 4.116 / 4.610, debris 2.617e-6 at q = 1e-6, ε_B 0.3443 / 0.3170, δ_c 0.0816 / 0.0816; all with relative difference 0 |
| K4 | CFG947: T-F bound 1.2114e-6; dust n = 1; T-M identity 6.9e-18 and R/(M_dom g_ref) = π²ε/4; T-E minimum 1.846642 |
| K5 | slip s_847 1.5398e-5 |
| K6 | dispersion minima 0.1000 / 1.0001 / 9.0001 / 99.0000; two-label 0.7071 |
| K7 | CFG941's 18 hover ratios, difference 0 |

**MUTATE: all six teeth bite (exit 1 by design).**

| tooth | result |
|---|---|
| M1 | hover returns, 1.0167 minimum, = CFG941 |
| M2 | prescribed asymmetric draw breaks momentum by 0.13 (control 6e-17) |
| M3 | n = 0.69433 |
| M4 | 4.12 / 4.61, and toy 1.9 / 1.7 |
| M5 | J_A 0.357 / 0.325 |
| M6 | tether off gives labelling jump 0 |

**Disclosures.**
- **A1 (post hoc).** The frozen f3 metric cannot converge (see the amendment). The frozen (f) FAIL and the frozen class
  are reported. The amended metric (a resolution criterion r ≥ √(10 dm), chosen after the diagnostic was seen) is labelled
  post hoc wherever it appears. Under A1 the 1:3 toy's 2N₀ value, 9.1e-4, sits close to its 1e-3 line.
- **Runs.**
  - The first main attempt crashed in T-θ: a sympy abs/DiracDelta artefact from writing (x²)^{−1/3}. It was fixed by
    writing F = (2/9)^{1/3}(1 − cos η)/(η − sin η)^{2/3}, which is exact on (0, 2π), before any test output.
  - The second main run is kept as `cfg950_firstrun_f3frozen.*`. It is identical to the final run except for the A1
    additions and runtimes.
  - The A1 diagnostic was run as a scratch script outside the lane.
  - The final K, MUTATE and main were all run from one script (sha256 61af2e46…).
- **Implementation choices made before the first run (not frozen).**
  - 1-D toy: seed 950, slab masses, L* = 0.25 toy units, re-latch beyond twice the median distance from label 2's
    centroid, events at steps 1500 / 3000 / 4500, box ±20 for the box-dependent 1-D energies (ungraded).
  - Merger toy: N₀ read as 300 shells per unit of M_b1 (300 + 300, 300 + 100), equal shell masses, flow stop at a ×20
    reduction or 300 s.
  - NGC-3198-like second label: baryons scaled with the same radial shape.
  - Merger energy scale: E_grav of the merged settled label.
  - Re-latch: host and satellite chemical potentials, spherical about each centre.
- **Inherited.** The engine census (0.315 × 2.775e11 inside M_ta; the f_ret table) places r_ON and N. The law inside r_e
  does not depend on it.
- **Compute.** One process per stage; peak RSS 0.20 / 0.24 / 0.25 GB (K / MUTATE / main); 2 / 3 / 16 s; nice 10,
  OMP_NUM_THREADS = 1; run beside NC2x. Nothing was downloaded. No other lane's file was edited.

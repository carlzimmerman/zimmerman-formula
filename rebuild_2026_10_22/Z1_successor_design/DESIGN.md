# Z★ = v3s-OC: v3s with an owned, capacity-limited hold (design, CONDITIONAL)

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. No dark-matter particle: the cold sector is one
pressureless medium ("cold energy", a field), not a particle species. This is a design, not a theory: two of its rules
have no action yet. Not "theory closed". Every number below is in `z1_successor_design_results.json` or cited.

## 1. One line

Keep v3s (owner-adopted, 591ec436be) as the law-and-screening chassis. Drop the Blanchet–Skordis K(Q) dust and its free
mass μ_K. Make the cold medium one geodesic (mimetic) dust. Let a bound system's khronon hold place the dust it has
captured at the law's phantom configuration, in that system's own free-fall frame (R2), and only up to the dust it has
(R1). Dust that no bound system owns is free dust.

## 2. The pieces

**Action pieces (variational).**

    S = S_GR[g] + Σ_q S_v3s[τ_q, P_q ; D_q] + S_mim[λ, S] + S_m[g, baryons]

- S_v3s on the domain D_q of owner q: the khronon τ_q (preferred foliation = the owner's rest frame), J = J_x
  (1 + J′ = y/(1+y), so the static limit is AQUAL with μ = x/(1+x)), the covector P_q, β = η = 0, and the switched
  stiffness −(γ_L/2)[max(D·P_q, 0)]² (X3). No K(Q) term: μ_K is removed.
- S_mim = −∫√−g λ (g^{μν}∂_μS∂_νS + 1): mimetic dust, T^{μν} = 2λ u^μu^ν with u = ∂S, pressureless and geodesic.
  It is the Q = 1 khronon of X6 (X-D2). Its abundance is an initial condition, as v3's dust abundance is.

**Rules.**
- **R1 (capacity).** The held density of owner q is drawn from its dust: 0 ≤ D·P_q ≤ ρ_d. The Poisson source is
  ρ_b + ρ_d (held + free), never ρ_b + ρ_d + D·P. In statics this is a two-sided obstacle problem on X3's convex leaf
  functional, so it stays convex and uniquely solvable (the upper obstacle is new; see test Z-T3). The time-dependent
  exchange between held and free dust (instantaneous phase equilibrium with total mass conserved) is POSTULATED:
  **non-variational**.
- **R2 (ownership).** Dust belongs to the smallest gravitationally bound system it is bound to, and is held in that
  system's free-fall frame. Dust bound to no system is unowned and free. Baryonic systems that capture no dust (CFG939's
  derived criterion: they move through the medium faster than their own baryonic escape speed — tidal dwarfs, DF2/DF4,
  globulars formed in a disc, stars, binaries) own none. **Non-variational and non-local.** This is CFG945's per-label
  tether H1 with the labels seeded by boundness.

## 3. Constants (honest count)

| item | v3 / v3s | Z★ | change |
|---|---|---|---|
| κ (a₀) | FITTED | FITTED | same |
| L★ (γ_L = K L★²/2) | FITTED, lower bound | FITTED, lower bound | same |
| cold abundance | FITTED initial condition | FITTED initial condition (adiabatic assumed) | same |
| μ_K | FREE, no allowed value | — | **removed** |
| J_x, switched γ_L form | POSTULATED | POSTULATED | same |
| R1, R2 | — | POSTULATED, zero continuous constants | **added rules** (R2 and R1's dynamics non-variational) |

Continuous constants: 3 (v3: 4). Rules: +2. No new scale enters: the supply radius, the crossing mass and the retention
law below are fixed by κ, the supply ratio and the owner's history.

## 4. How one medium is held in isolated galaxies yet self-binds elsewhere (the U1 mechanism)

The record's obstruction (U1, D-T, D-T′, X-D1): in the khronon family the cold medium is held by the law's own field,
so it is the phantom, weighs nothing in a host, and has no linear self-gravity. Z★ keeps "the held dust is the phantom"
(that is what keeps isolated galaxies on the law) and changes three things:

1. **Held dust is real dust, drawn from a supply (R1).** It is not polarization charge. The phantom in an isolated
   owner is the owner's captured dust, placed by the hold. Total mass = baryons + dust, never more, so there is no
   double count (K5: where supply ≥ demand, g obeys the a₀-line exactly).
2. **The hold acts in the owner's own frame (R2).** A satellite's held dust is internal to the satellite. The unit falls
   at exactly g_host (K6; v3 gives g·M_b/(M_b + M_h)), and the host's uniform field drops out of the satellite's law
   argument: no EFE (K6 illustration with the 1-D aligned EFE formula, which over-suppresses (P4): one foliation turns
   x_int = 0.1 into 0.012 at x_e = 1, −0.92 dex; the owner frame keeps 0.1).
3. **Released dust stays bound.** In Z★ the held phase moves with the owner's foliation normal (the khronon charge
   D·P), so in a static owner it is single-stream and at rest; this is part of R1's postulated phase equilibrium. When
   the owner's baryons leave (gas stripping, winds), the demand drops and the surplus is released at rest, so its energy
   in the owner's well is negative everywhere (K7, both footings, 30 grid points). It collapses and stays: the owner keeps
   M_ph(M_b,orig). Inside the owner and before tidal stripping, Δlog g ≥ ½ log(M_b,orig/M_b,now) (K9). This is the
   opposite of CFG939's tethered medium, which carries dispersion and escapes above f_crit; the held v3s dust carries
   none.

Then:
- **Isolated galaxies** (supply ≥ demand inside): held dust = phantom, law exact (K4, K5). Static limit = v3s.
- **Hosted dwarfs and Coma UDGs**: owners in their own frame (no EFE) that lost their gas on infall. X1's isolated-law
  residuals need lost baryon fractions 0.72 / 0.67 (MW classical), 0.95 / 0.93 (ultra-faints), 0.68 / 0.62 (bright
  M31), 0.95 / 0.93 (M31 others); the isolated LG dwarfs (+0.05 / +0.02) need ≤ 0.21 / 0.09. For the Coma UDGs, CFG948's
  field HI-rich UDG gas fraction 0.81 predicts ≥ +0.361 dex against the observed +0.33 dex over the isolated law
  (`R/S1_v3_hosted_small/README.md:8`, `campaign_fresh_gravity/LEDGER.md:704`).
- **TDGs, DF2/DF4**: capture no dust (CFG939) and cannot carry the host's held dust (U1 T3): Newtonian. Same as U1's
  native pass (+0.055 ± 0.114 dex).
- **Linear cosmology**: nothing is bound, nothing is owned, so the medium is mimetic dust: s(k) = 1 for every k and
  δ ∝ a in EdS (K8; v3 at μ_K = 0 gives s = 0). Growth is GR growth on dust (C2: γ = 0.555), BBN has no stiff partner
  (no K(Q)), and the CMB is the dust limit (Q6's ΛCDM-shaped refit, native H₀ 67.2–68.6). a₀ stays absent at linear order.
- **Clusters**: owners that keep the cosmic baryon share, supply f_s ≈ 5.364. The supply radius is
  r_s = r_M √(f_s(f_s+1)) = 5.84 r_M (exact for a point mass, K5). Excess free dust appears only above the crossing mass
  M_× = 2.7e13 / 4.7e13 M☉ (200ρ_c) or 3.8e14 / 6.8e14 M☉ (18π²ρ̄_m, EdS) (K10). X2's tercile medians sit at or below
  it: total/law inside the owner ≤ 1.04. **So Z★ does not produce the core excess (A_MID 1.88 / 1.89 in T2 / T3): the
  cluster row stays FAIL.** Beyond r_s (0.44 / 0.84 / 1.32 Mpc canonical) the law is truncated: design/law enclosed mass
  at 2 Mpc is 0.24 / 0.44 / 0.68, the direction of X2's OUTER ratios 0.50 / 0.78 / 1.40, possibly too strong for T1.

**What Z★ escapes, and how.** D-T, D-T′ and Theorem G hold for local Lagrangians. Theorem S holds for label-free
tethers. Z★ escapes all four **only through R2**, which is non-local and has no action. That is the price, stated plainly.

## 5. Derivations (sympy, `z1_successor_design.py`)

- **Static owner limit (K4).** Leaf functional (a₀²/4πG) F(|∇ψ|/a₀) + ρ_bψ with F(y) = y²/2 − y + ln(1+y):
  F′(y) = yμ(y), F″ = (y² + 2y)/(1+y)² > 0. Its Euler–Lagrange equation is ∇·[μ(|∇ψ|/a₀)∇ψ] = 4πGρ_b (planar,
  residual 0); the spherical first integral is the a₀-line g_N = g²/(g + a₀) (residual 0); BS24 Eq. 35 with μ_K = 0 is
  the same equation. With R1 inactive (supply ≥ demand) the owner's statics are v3s's, so P4, C6, D7d, D10 and X3's
  static results carry over.
- **Linear kernel (K8).** The NR mimetic Lagrangian L = −ρ(φ̇ + |∇φ|²/2 + Φ) gives Hamilton–Jacobi (geodesic) and
  continuity exactly; with Poisson, a single mode obeys D̈ = 4πGρ̄·s(k)·D with s(k) = 1; in EdS the growing mode is δ ∝ a.
- **Capacity and supply radius (K5), crossing mass (K10), release (K7), retention (K9), fall rate (K6)**: closed forms in
  the script; numbers in the JSON.

## 6. Status of every matrix row (D6)

| row | Z★ status | basis |
|---|---|---|
| R1 GW, pulsars | INHERITED (COND) | v3s tensor sector (C8); owner boundaries not analysed |
| R2 health | OPEN | v3s + X3 inside owners; the upper obstacle (R1) and owner boundaries (R2) untested (Z-T3) |
| R3 SPARC RAR | INHERITED inside r_s | owner statics = v3s (K4); r_s depends on owned supply (Z-T6) |
| R4 MeerKAT, R5 groups | INHERITED | P4 |
| R6 isolated LG dwarfs | INHERITED + PREDICTED | at the law if they kept their gas (lost ≤ 0.21 / 0.09) |
| R7 Cassini | INHERITED | v3s screening (C6, D7d) |
| R8 outer globulars | INHERITED | non-owners in the MW's owner field = v3s with EFE (D10 floor 21.7 / 22.9 pc) |
| R9 wide binaries | PREDICTED Newtonian | non-owners (no capture); same sign as v3s's sealed prediction |
| R10 MW K_z | FAIL (inherited) | owner statics = AQUAL disc (P4, X5) |
| R11 MW outer slope | FAIL (inherited) | S3, X5; a released concentrated component would steepen it (untested) |
| R12 TDGs, DF2/DF4 | PREDICTED Newtonian | no capture (CFG939) + T3; U1's native pass |
| R13 satellites | PREDICTED | own frame (no EFE) + retention ≥ ½ log(M_orig/M_now) (Z-T1) |
| R14 Coma UDGs | PREDICTED | ≥ +0.361 dex from gas fraction 0.81 vs +0.33 observed (Z-T1) |
| R15 cluster cores | **FAIL (predicted)** | total/law ≤ 1.04 at the tercile medians (K10); OUTER truncation untested (Z-T2) |
| R16 linear growth | INHERITED (dust limit) | K8; F3 dust-limit S₈ 0.845 → 0.814, consistent at k ≤ 0.3 h/Mpc |
| R17 BBN | PASS by construction | no K(Q), so no a⁻⁶ partner (Q6's failure source removed) |
| R18 CMB | INHERITED (dust limit) | C2 / Q6 ΛCDM-shaped refit; native H₀ |
| R19 isocurvature | OPEN | adiabatic origin assumed, not derived; Codex's two-field origin fails (X1_seedfree) |
| R20 a₀ tied to Λ | INHERITED | J_x; κ FITTED |
| R21 strong field | INHERITED | P3 inside owners |
| R22 lensing inner, red | INHERITED + PREDICTED | blue as v3s (S2); red above the law by √(M_orig/M_now) (Z-T5) |
| R23 lensing outer | PREDICTED, at risk | law truncated beyond r_s plus a native dust two-halo; the record's catchment edge gave Δχ² +100 (F2: not robust) (Z-T4) |
| R24 cosmic shear | OPEN, at risk | owners reshape galaxy halos; the record's settling rules failed raw KiDS (CFG596, CFG960) (Z-T9) |
| new: Cherenkov | OPEN | v3s's khronon/dust pair moves at ~1e-4 c in the Solar System (P3) while stars move at ~7e-4 c through the Galactic medium; Mistele 2103.16954's constraint on slow matter-coupled modes applies (prov) (Z-T11) |

## 7. Risks, in order

1. **R2 has no action.** It violates the one-action rule (CFG678) and is the only way Z★ escapes D-T, G and S.
   Nothing here builds it; the cheap tests below decide whether it is worth building.
2. **Clusters stay red.** Capacity alone gives ≤ 4 % at the tercile medians.
3. **Supply edge.** Isolated-galaxy outer lensing is truncated beyond r_s. The record's catchment edge failed F2
   (Δχ² +100, not robust); P2's spectroscopic data sit below zero-field v3, which is the truncation's direction.
4. **The owned supply is history-dependent.** With the cosmic ratio 5.364 a 1e8 M☉ dwarf would be truncated at 2.3 kpc
   (MW-like: 55 kpc); SPARC's flat outer curves need f_own ≥ R_last/r_M (≈ 10–50 for dwarfs). Unowned dust grows exactly
   like dust, so a native collapse model can give f_own; until then it is OPEN.
5. **MW disc and slope** fail as in every μ-law theory.
6. **Cosmic shear** could repeat the settling rules' excess power.

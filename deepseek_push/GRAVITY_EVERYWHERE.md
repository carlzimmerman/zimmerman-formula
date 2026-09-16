# GRAVITY EVERYWHERE — the complete theory assembly (the TOE statement)

**Status:** assembly of committed, verified results as of 2026-09-15. Every
number below is a committed artifact of the cited gate; nothing here is new
calculation. The document is the EFT one-pager of the theory: one action, three
regimes, two energy sectors, one open list. The style rule of the programme
applies: nothing "closed" that a gate did not close, nothing "open" that
decides the story but is not named.

The one-line theory:

> Gravity is GR plus one shift-symmetric scalar. The scalar's vacuum value is
> the dark energy; its Noether charge is the dark matter. It modifies no force
> anywhere. It generates a sector, and the sector's equilibria make the RAR,
> the flat curves, the clusters, and the dark-energy scale — one constant, all
> of it.

---

## 1. THE ACTION

### 1.1 The sectors

The action has exactly one new dimensionful constant, a₀ (G031; "one scale,
two sectors, one action, three regimes" — STATE.md). It is the Brown/Schutz
fluid form of G031, with the scalar side at the frozen kinetic term of H011:

    S = (c^4/16 pi G) ∫√-g (R − 2 Λ_geom)                    [GR + the cosmological term]
      − ∫√-g Λ^4 f(K)                                       [the shift-symmetric scalar]
      + S_fluid[J, φ, β, α]                                 [the Noether-charge dust]
      + S_baryons

    S_fluid = ∫√-g [ −ε(n) + J^μ (∂_μ φ + β ∂_μ α) ],   n = √(−J_μ J^μ)

  * **GR is exact.** The scalar enters only algebraically through
    K = −(1/2)(∂φ)²/Λ⁴; there is no derivative coupling, no disformal term, so
    the tensor quadratic action is exactly Einstein–Hilbert and
    **c_T = c identically** (H027 T1; GW170817 satisfied structurally, nothing
    to arrange — contrast AeST).
  * **The cold sector is a Noether charge, not a species.** Varying φ, β, α
    (Lagrange multipliers) gives J^μ_{;μ} = 0 **variationally** — for this
    sector the conserved current IS the shift charge (G028): one conservation
    law, no independent particle number (G031). The sector is barotropic dust,
    ε = mn, p = 0, so T^μν = ρ u^μ u^ν with **w = 0 exactly** (certified
    L192/L193). That charge is the dark matter.
  * **The cosmological term is the theory's own f(0) = −1** (hy4): with
    Λ_geom = 8πGρ_Λ/c² and ρ_Λ = 4a₀²/(Gc²), the Einstein term and the scalar's
    vacuum normalisation are one number (G031 V1/V2: Λ_geom = 32πa₀²/c⁴ exact).

### 1.2 The scalar: frozen, shift-symmetric, Lorentz invariant (H011)

    L = Λ^4 f(K),      K = −(1/2) g^μν ∂_μ φ ∂_ν φ / Λ^4
    f(K) = K − 2 ln(1 + √K) − 2/(1 + √K) + 1,      f'(K) = μ_2(√K)

  * With φ̇ = 0 the gradient is spacelike, so K ≥ 0 automatically and √K is real
    **without a projector — no aether, no vector sector at all** (H011 K1/K2,
    P1–P3): α₁ and α₂ do not exist. The aether was solving a problem the theory
    does not have; the frozen configuration is not a tachyonic point
    (dρ/dK > 0, S3), and c_s² = (u²+3u+2)/(u²+3u+4) ∈ (1/2, 1) — the classic
    spacelike-k-essence failure (loss of hyperbolicity) is absent (H011 S1/S2).
  * φ̇ = 0 is a **confirmed attractor** (G054, 14/14), so "frozen" is the
    theory's own dynamics, not an imposed ansatz.
  * K = 0 sits at the non-analytic point: f(0) = −1, w = −1 exactly
    (H011 C1).

### 1.3 The vacuum term and the seesaw

The vacuum value f(0) = −1 gives p = −Λ⁴, ρ = +Λ⁴, i.e. the dark-energy
density, and the seesaw fixes its scale:

    ρ_Λ   = 4 a₀² / (G c²)     (a₀ = (c/2)√(G ρ_Λ))       [G031 V1, Lemma 1]
    a₀    = Λ² / (2 M_Pl)      (measured: Λ²/2E_Pl = 3.2934e-53 = a₀ ħ/c, H027 T4)
    Ω_Λ   = 32π a₀² / (3 H₀² c²) = 0.6857   (+0.07% of Planck 0.6847; G052, G058 Lean)

Λ = 2.2404 meV; ρ_Λ = 5.8447e-27 kg/m³ (canonical footing a₀ = 9.3619e-11;
alt 1.1279e-10 throughout — every gate ran both footings). **One measured
scale, every sector**: the galaxy scale, the vacuum density, and the virial
temperature of §3.1 are the same constant in disguise (the Z-theorem; G058, 6
Lean theorems, zero sorry). The coincidence problem dissolves by parameter
count.

### 1.4 What the scalar does NOT do — the force-law closure (with proof)

The scalar modifies **no force in any regime**. This is dead-and-proofed, not
assumed (g03_verdict.md; G03_SPEC §3 is the shut door):

> "a pure k-essence 'frozen scalar' (H011: its static law is the bare μ₂ AQUAL
> equation and inherits Cassini unchanged)" — G03_SPEC §3 shut door.

  * The bare μ₂ kernel fails the Park 2026 Cassini ceiling 6.44×/7.63×
    (L243, S0-calibrated). The G03 lane then scanned every surviving
    modification class on the validated instrument — T-B localised (single and
    double filter), whole-sector form factor, field-dependent screening, 44
    solves, both footings, ξ = 0.005–0.1 pc: the ratio **never drops below
    6.18×** (xi = 0 is the best case). The smooth-shell lemma (scan-confirmed):
    an isotropic local screen preserves the l = 2 moment of the μ-transition —
    **the static quadrupole is a property of the kernel's transition, not of
    the completion's UV structure.**
  * The force-law class is therefore closed **with proof**: every local,
    isotropic, or aether-mixed completion dies; the frozen scalar — one member
    of that class — dies **as a force law**.
  * It returns here as what it actually is: the **sector generator**. Its
    Noether charge (1.1) is the mass. The MOND-looking force is not a force
    law; it is the gravity of the equilibrated charge dust (§2.ii). The scalar
    produces the sector; the sector produces the phenomenology; the scalar
    itself never pulls.
  * Strong-field corollaries of §1.1, unchanged by construction (H027 T2/T3):
    black holes carry **no independent scalar hair** (the sourced equation
    div[f′(K)∇φ] = 4πGρ has no integration constant independent of the metric's
    mass parameter) — EHT/LIGO see GR; and compact objects carry the same
    phantom-halo law as galaxies, M_ph/M = r/r_M with r_M = √(GM/a₀)
    (10 M☉: 0.12 pc; 10⁹ M☉: 1.2 kpc) — one law, all scales.

---

## 2. THE THREE REGIMES

The regime is selected by the baryonic acceleration g_N relative to a₀, and —
for the phantom form — by the external field g_ext. The sector's phase is
selected by the same numbers (H032: two states of one charge).

### (i) Strong field — g_N > a₀: Newtonian baryon gravity; the sector is cold dust

  * Baryons dominate; the field is Newtonian. The dark sector does NOT
    equilibrate (nothing does at g ≫ a₀): it is **free dust** — cold,
    collisionless, does not know a₀ (H032 D1).
  * **The Solar System**: the phantom is absent — the local cloud is unbound
    and EFE-capped at 7.4 kAU (G006), so the Sun's field is Newtonian plus
    local dust: **no quadrupole, trivially under the Park ceiling** (the pincer
    is complete: every force-law completion fails Cassini — proven; the
    equilibrium reading predicts Newton there — by construction; g03_verdict).
    The Solar-System-adjacent observable is the wide-binary cloud, mass linear
    in separation, γ_v rising 1.002 → 1.047 to 30 kAU with the 7.4 kAU
    period–separation cap (E6/E7, registered; the DR4 falsifier).
  * The Milky Way in the strong part of its field: v_c(R₀) = 224 km/s against
    the measured 229–235 (G072; within 5% of 232.5).

### (ii) Deep, isolated — g_N < a₀, EFE-free: THE EQUIPARTITION REGIME

Where the well is deep enough and isolated enough, the sector **equilibrates**.
This is the regime the programme derived three independent ways (G046, G056,
Q001) and the one the RAR lives in. The content:

  * **The equipartition** (G03E V1): the phantom mass inside the MOND radius
    equals the baryonic mass **exactly** —

        M_ph(<r_M) = M_b,   max |ratio − 1| = 2.2e-16, every mass, both footings

    and the dark total obeys the universal linear law
    **M_dark(<r)/M_b = r/r_M, exactly**, with r_M = √(GM_b/a₀) (G03E V2's
    corrected reading; the phantom form alone is the capped share, the free
    dust continues past the break).
  * **The triad** (G03G V1/V2): the isothermal profile is selected by flatness
    — v_c ~ r^(2−γ) forces γ = 2 — and one number appears three times:

        σ²/v_flat² = κ = c_s² = 1/2        (G002's defining relation; G038; G03G, exact)

    the density ρ = √(GM_b a₀)/(4πG r²) [G003, coefficient exactly 1], the flat
    curve v_c² = 2σ² = √(GM_b a₀) [BTFR], and the deep RAR g² = a₀ g_N
    [coefficient 1] are one chain (G031 V3–V6, sympy-exact).
  * **The dSph floor** (G03G V3): the predicted internal dispersion
    σ_pred = (GM_b a₀)^{1/4}/√2 sits on the classical dwarfs — 7 dwarfs
    (Draco to Crater II), median log₁₀(pred/obs) = **−0.00**, all inside
    ±0.35 dex. The floor of galaxy dynamics is set by the same constant.
  * **The universal surface density** (G078 = G03E × H033): the phantom sheet's
    mean surface density inside r_M is a pure function of the one scale —

        ⟨Σ_ph⟩(<r_M) = M_b/(π r_M²) = a₀/(πG) = 213.74 M☉/pc²     (alt 257.52)

    to machine precision over six decades of mass (the M_b cancels; H033's
    observed 141.3 sits between a₀/(2πG) and a₀/(πG) — bracketed, prefactor
    convention the honest edge). Locally: ρ_dark(R₀) = 0.0081 M☉/pc³ in the
    measured 0.008–0.015 band; the finite ±1.1 kpc column 17.7 M☉/pc² in the
    15–25 measured band (G076/G078).
  * **The RAR is hydrostatics, not a force law** (G031, the reading): at the
    virial temperature the isothermal equilibrium of the charge dust IS the
    phantom — the RAR is the **equation of state** of the dust, the fluid
    action's stationary point. μ₂ is not a modified force; it is the
    interpolant of the equilibrium's own law, and the G002 closed form is what
    connects this regime to the force regime (G031 V7/V8).
  * **Cassini null** (ii, by construction): no phantom, no transition shell, no
    l = 2 moment, no quadrupole — this regime's prediction at Saturn is Newton
    (g03_verdict; the equilibrium is what is absent in the Solar System).
  * **Lensing = GR times real mass**: the phantom is real mass (the equilibrated
    charge), so light sees the total real mass in Einstein's equation —
    no conformal slip, no lensing-dead scalar (G03E V4; L241's kill applies to
    conformal-only force laws, which this is not).

### (iii) EFE-dominated — g_ext > a₀: the cap, and the free dust takes over

  * The phantom form (the equilibrated share) **caps at the EFE line**:

        r_efe = √(G M_b / g_ext)            (= r_M · (a₀/g_ext); H033)

    For the Milky Way this is the **6.1 kpc break** (G072: computed 6.74 kpc on
    L258's M_b = 7e10 and L240's g_ext = 2.146e-10, +10.5% against the
    registered 6.1 kpc — G003 V6's full-kernel value at M_b = 6.5e10 — two
    theory computations agreeing to 10%; E5).
  * Beyond the break the **free dust takes over**: the outer MW curve stays
    mildly declining, log-slope −0.16, non-Keplerian — the registered handoff
    (G072 V5; G03E V2: the dark total keeps the linear law, the phantom-only
    share saturates at 0.62 M_b — the shortfall IS the free dust's registered
    share, G050/G059).
  * Clusters sit here: the phantom shape survives (G008/G012 slope −1.478 vs
    −1.53, T = 809 km/s) while the amplitude carries the environment order
    parameter — the open item of §4.1. In the deepest-Newtonian interiors
    (Bullet main at g/a₀ ≈ 9) the sector is essentially all free dust:
    collisionless, follows the galaxies, not the gas — the Bullet's observed
    peak-separation, and the reason standard MOND (a force law tied to the
    baryons, hence to the gas) struggles there (H032 D2/D3).

### The regime map, one line per place

| Place | Regime | The sector | Gravity |
|---|---|---|---|
| Solar System, strong sources | (i) + EFE cap | absent (unbound, capped 7.4 kAU) | Newton; Cassini null |
| Wide binaries (2–30 kAU) | (i) cloud | mass linear in separation | Newton + cloud (E6/E7) |
| Galaxies, discs | (i) | free dust | Newtonian discs; R₀ = 224–230 km/s |
| Galaxies, deep (r ≳ r_M) | (ii) | equilibrated phantom + dust | flat: v_c² = 2σ² = √(GM_b a₀) |
| Galaxy outer edge | (iii) | phantom capped, free dust takes over | 6.1 kpc break, log-slope −0.16 |
| Clusters | (iii) | phantom shape + free dust | shape passes; normalization open |
| Black holes | (i) | secondary hair only | GR: c_T = c, Kerr shadows, GR ringdown |
| Cosmology | K = 0 | frozen at the vacuum | w = −1, Ω_Λ = 0.6857 |

---

## 3. THE ENERGY SECTORS

### 3.1 Dark energy — the vacuum value f(0) = −1 of the same scalar

Dark energy is the **zero-mode of the MOND scalar**: the value of f where the
gradient vanishes (H027 T4). Not added to the theory — it is what the function
equals when there is nothing to modify. p = −Λ⁴, ρ = +Λ⁴, **w = −1 exactly**
(no aether, no tuning; H011 C1); the seesaw fixes the scale (§1.3), and
Ω_Λ = 0.6857 sits +0.07% from Planck on the canonical footing (G052 — the alt
footing fails at 0.9953: the honest edge was never hidden; Euclid/CMB-S4
decide).

**How it acts — locally, through the virial scale, not only through
expansion.** The same vacuum value that accelerates the background sets the
temperature every dark sector relaxes to:

    σ² = √(G M_b a₀) / 2        (the Zimmerman temperature; G031 V3, sympy-exact)

The chain is one line: f(0) = −1 fixes ρ_Λ; ρ_Λ fixes a₀ (the seesaw); a₀ sets
the equilibrium temperature of every well; the sector relaxes to it and becomes
the phantom. So the dark energy does not merely push the scale factor — it
**sets the local virial scale** on which cold structure equilibrates. The MW
realization: σ = 119.2 km/s (canonical) / 124.9 (alt) against the observed
~100–120 km/s (G031 V9). One constant, three sectors.

### 3.2 Dark matter — the Noether charge, in two phases

The cold sector is not a particle species; it is the shift-symmetry charge
(G028), and it has two acceleration-selected states (H032 D1):

  * **Equilibrated phantom** (g ≲ a₀, EFE-free): baryon-tied, ρ = √(GM_b a₀)/(4πGr²),
    M_ph(<r_M) = M_b, Σ_ph(<r_M) = a₀/(πG) — all of §2.ii.
  * **Free dust** (g ≫ a₀): collisionless, does not know a₀, follows the
    galaxies not the gas — the Bullet, the cluster share, the Milky Way's outer
    handoff.

This is why 40 years of direct detection found nothing: **there is no particle
to find** (H032). The charged object is the field configuration, not a species.

### 3.3 Neutrinos — no (f04/f06 structural kill, quoted)

The convenience story — "the cold sector is a hot relic" — is dead on its own
internal consistency, not on any external datum:

> "Free-streaming then demands m ≥ 148 eV to spare even the coarsest
> Lyman-alpha scale, and phase space demands m ≤ 93 eV to keep the relic out of
> the dwarfs. No overlap." (f06 A4, the rigorous kill)

  * The conflict is exact, not coincidental: hold Ω fixed at Ω_dm; a relic is
    kept OUT of dwarfs by LOW primordial phase-space density and out of the
    free-streaming problem by HIGH primordial phase-space density — one
    quantity, small and large at once. The window is empty by a factor of 1.6
    (phase space m ≤ 93 eV from the cluster floor ≥ 14.68 eV and the dwarf
    ceiling of 93.3 eV, a factor-6 split — f04 A1).
  * The standard escape — MOND regrows the erased power — is **closed for this
    framework by its own best result**: the bulk-flow null measured β = 0.447
    against ΛCDM's 0.440, where an unprotected MOND kernel requires 0.043–0.047
    — the linear regime is Newtonian, so nothing can regrow the erased power
    (f06 A3).
  * Independent, unchanged: Tremaine–Gunn needs m > 65 eV against m_ν < 0.1 eV
    (650×); the mass budget is short by 206×; free-streaming washes out galaxy
    scales (H027 T5).

The cold sector is a charge, not a species; neutrinos stay hot, subdominant,
and not the dark matter.

---

## 4. THE OPEN LIST — every item with its falsifier

Nothing below is closed or claimed closed. Each item names the measurement
that kills it.

| # | Open item | What it is | Its falsifier |
|---|---|---|---|
| 1 | **The cluster normalization** | The phantom shape passes (G008/G012) but the cluster amplitude carries the environment order parameter (G03E V4); the honest astrophysical normalization — how phantom + free dust compose at g_ext ≫ a₀ — is not derived (as LCDM's concentration–mass relation is not ours to use). | A cluster sample whose dark-mass amplitude and radial profile cannot be produced by phantom (equilibrated share) + free dust (collisionless share) with no fitted normalization — in particular a residual growing inward that the free dust cannot supply, or an amplitude varying with environment faster than the EFE line's reach allows. |
| 2 | **The relaxation/stability gate (G081)** | The equilibrium's formation: does the sector actually relax to the Zimmerman temperature σ² = √(GM_b a₀)/2, and is the isothermal equilibrium stable? The temperature's dynamical origin is the theory's contested rung (K001 N-body relaxes to 0.53 R₀ — no attractor found; PAPER29's audit relabels it POSTULATED; G031 honest edge). | An N-body/stability computation showing the charge dust does not relax to σ² = √(GM_b a₀)/2 from generic initial data, or that the isothermal equilibrium is unstable (a small perturbation grows). This gate decides whether §2.ii is dynamics or ansatz. |
| 3 | **The high-z zero point (G080)** | The BTFR zero point at z ≈ 2.5: the equipartition amplitude scales with M_b at all z — 0.00 dex against the +0.33 dex drift of the competing family (20:1 odds). H026: NOT ESTABLISHED — the baseline is not yet wide enough. | JWST/ALMA measuring a drifting zero point (+0.33 dex class): the phantom amplitude is then not M_b-scaled at high z and the equipartition is a local coincidence. |
| 4 | **The DR4 funnel (G076)** | The vertical-funnel map of the phantom sheet: z_c(R) = a₀/(16πG ρ_b(R)) — 140.63 pc at the solar circle (E2, exact on G024's ρ_b(R₀) = 0.095), the e^{+R/3} flare (z_c(15)/z_c(8.2) = 9.6472 = e^{2.2667}), the box-ν = 2 arithmetic (E1), the 1/√z fall (E4), and the radial 6.1 kpc break (E5). | Gaia DR4 (Dec 2 2026): no 140.6 pc break, ν_layer ≠ 2, a flat or rising box-ν, a smooth NFW-like vertical profile with no surface-density coupling, or no radial break at 6.1 kpc. Any one kills the EOS identification (§2.ii) or the two-component architecture (§2.iii). |
| 5 | **The free-dust phase's microphysics** | The free-dust abundance is not derived (L258 A3; G072 V5's edge); the phase split (phantom vs free) is set by g/a₀ alone (H032), and the free dust is collisionless by construction — but its own equation of state, its sourcing within the EFE-capped regime, and its cluster share are open. | A measured free-dust behavior contradicting collisionless dynamics (e.g. a density signature tied to gas rather than galaxies in a well-resolved merger), a direct-detection claim of a particle (there is no species — 40 years of nulls are the prediction), or LIGO/EHT seeing non-GR ringdowns or shadow deviations (no scalar hair, H027 T2). |

Registered elsewhere and not re-opened here: n = 2 remains the one empirical
premise (all derivation routes closed, G009/G019); the growth raise is in the
registered DESI band and its tension with direct lensing is recorded (G020/G022).

---

## 5. HOW GRAVITY WORKS EVERYWHERE — the ten lines

1. There is one constant, a₀ — the dark-energy density in acceleration units (ρ_Λ = 4a₀²/Gc²).
2. The action is GR plus one shift-symmetric scalar, L = Λ⁴f(K), with f(0) = −1.
3. The scalar modifies no force anywhere; it generates a sector of Noether charge.
4. That charge is the dark matter — a field configuration, not a species.
5. Where the field is strong, the sector is cold collisionless dust and gravity is Newtonian (the Solar System passes Cassini by construction).
6. Where it is deep and isolated, the dust equilibrates to the virial temperature σ² = √(GM_b a₀)/2 set by the vacuum scale; the equilibrium is the phantom.
7. The phantom is real mass: M_dark = M_b·r/r_M, ρ ~ r⁻², σ² = v_flat²/2, Σ = a₀/πG, g² = a₀g_N — the RAR is the sector's equation of state, and lensing is GR on the real total mass.
8. Where the external field dominates, the phantom form caps at r_efe = √(GM_b/g_ext) — the MW's 6.1 kpc break — and free dust carries the outer part.
9. The vacuum value of the same scalar is the dark energy: w = −1, Ω_Λ = 0.6857 from a₀ alone; it acts locally by setting every well's equilibrium temperature.
10. What is still open is named and armed: cluster normalization, the G081 relaxation/stability gate, the high-z zero point (G080), and the DR4 funnel (G076) — with its falsifier in print, decided by Gaia DR4 (Dec 2 2026), DESI, JWST/ALMA and Euclid.
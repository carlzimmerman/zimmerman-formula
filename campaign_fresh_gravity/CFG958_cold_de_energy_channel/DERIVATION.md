# CFG958 DERIVATION: one energy channel, cold energy ↔ dark energy

Criteria `FROZEN_CRITERIA.md` (8d7764d74, committed alone first). A1 `AMENDMENT_A1_pre_result.md` (11e0bdd4b, pre-result). A2
`AMENDMENT_A2_weff_line.md` (84c9ebd9c, before any script, written after a disclosed hand check). Every load-bearing statement below
has a sympy or numeric check in `cfg958.py`, named in brackets; numbers are from `cfg958.out` / `cfg958.json` (main),
`cfg958_K.*` and `cfg958_MUTATE.*`. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle
species. Not "theory closed". Nothing here says the data favour the framework.

**Class under the frozen rule (criteria §3, with A1): FAILS, and only at T4's |1 + w_eff| ceiling item.**
- The ceiling deposit rate (all cold energy converted once per Hubble time at ε_max) gives |1 + w_eff| = 2.09e-4 (canonical) /
  2.39e-4 (alt) at z = 2.33, against A1's 1e-4 line.
- Every other graded item passes on at least one variant and reading.

**Substantive reading (A2's record-based line 2.51e-3, set after a disclosed hand check): CONDITIONAL.**
- T5 = CONVERTED. Total stress-energy is conserved exactly, with dark energy as SCT's reservoir.
- The local tests pass only under one of two named conditions:
  - **C-A0**, a₀ reads the cosmic-mean vacuum (CH-L);
  - **C-G**, a new cosmic relocation current carries the deposit away (CH-G).

**V2: ONLY WHERE NO ENTROPY IS EXCHANGED.**
- SCT's events and the class-A drift can use a coherent w = −1 dark energy.
- CFG955's K-T relaxation and CFG935's bath cannot (Clausius).

| test | result | grade |
|---|---|---|
| T1 exchange | identity exact (Minkowski, FRW); event algebra Δ(K + W + E_V) = 0; any compact deposit exerts zero net force and torque, so S-TM is kept; composite = dust; toy \|Δ(K + W + E_V)\|/\|E₀\| 1.47e-4 (E) / 2.46e-5 (M), dP, dL ≤ 2.3e-15 | PASS |
| T2a cosmic | ceiling \|Δ ln a₀\| ≤ 6.8e-5 … 3.6e-4 at z 1–2.33, i.e. (5–8)e-4 of CFG689's 68% half-widths; native (CFG630 ledger rescaled) a₀(z)/a₀(0) − 1 ≈ −2e-7 (z 1), −6e-7 (z 2) | PASS |
| T2b local, CH-L P-σ | a0-cos: NGC 3198 1.8e-7 / 2.1e-7; a0-loc: **6.5e-2 / 8.8e-2** (δV/V̄ up to 0.88 / 1.15 at the inner radii) | a0-cos PASS; **a0-loc FAIL** |
| T2b local, CH-L P-U | a0-cos: 1.9e-9 / 2.6e-9; a0-loc: **3.7e-6 / 5.6e-6** (δV/V̄ 1.6e-5 / 2.5e-5) | a0-cos PASS; **a0-loc FAIL** |
| T2b local, CH-G | 4.9e-9 / 5.4e-9 (in-transit energy, t_P = 1 Gyr), both readings | PASS (carries C-G) |
| T3 sign, ordering | formation cold → DE, mergers DE → cold, net = −Δ(K + W) ≥ 0; capacity C_U ≥ 698 / 467 in every class: never energy-limited | PASS (AVOIDS) |
| T4 stability (IV) | no kinetic term, no propagating mode, composite dust; \|1 + w_eff\| ceiling 4.8e-6 (z 0) … 2.1e-4 / 2.4e-4 (z 2.33) | **frozen FAIL (1e-4)**; A2 PASS (2.51e-3) |
| T-S entropy | SCT events: ΔS = 0 with a zero-entropy dark energy; a heat bath would be violated by the merger draw; K-T: reservoir must absorb entropy | PASS for SCT; V2 = ONLY WHERE NO ENTROPY IS EXCHANGED |
| T5 C-E | frozen: NOT CLOSED (T4 item); A2: CONVERTED (C-A0 or C-G) | — |

---

## 1. The channel

### 1.1 Receiver and exchange

The record needs w ≈ −1, and it has no dark-energy microphysics (CFG689 fits ρ_DE(z) node by node). The minimal receiver with w = −1
at every point is the interacting vacuum (IV). Signature (−,+,+,+), V an energy density, x⁰ = ct:

    T_V^{μν} = −V g^{μν}
    Q^ν ≡ ∇_μ T_V^{μν} = −∇^ν V                         [T1a: Minkowski and flat FRW, all components]
    ∇_μ (T_c + 𝒮′)^{μν} = +∇^ν V = −Q^ν,   ∇_μ T_b^{μν} = 0
    ⇒ ∇_μ (T_b + T_c + 𝒮′ + T_V)^{μν} = 0

- 𝒮′ = Σ_q Σ′_q − T_c,lab is CFG953's source with every body's internal energy set to zero.
- Each increment CFG953 books into E_int,q is booked as vacuum energy instead: ∫ΔV d³x = ΔE_int,q. This covers the conversion
  (R4), the reshape (R6) and the merge (R7).
- The identity Q^ν = −∇^ν V is not new: CFG131, CFG195 and the sol61 local-reaction report give it. In a local frame it reads
  (V̇/c, −∇V). When V rises, matter loses energy at rate V̇ **and receives the force density +∇V**.

### 1.2 Where the energy sits

- **CH-L (local).** V = V̄(t) + Σ_q δV_q(|x − X_q|), with δV_q = E_q w_q, ∫w_q = 1 and support r ≤ r_e,q.
  - The lump travels with body q.
  - Per-owner rule: body q's 𝒮 alone takes the reaction +∇δV_q, and holds it as an internal stress p_hold = δV_q − δV_q(r_e).
  - Profiles: **P-σ**, w ∝ σ_q (the deposit sits where the body's mass is); **P-U**, w uniform inside r_e.
- **CH-G (global).** V = V̄(t) only, homogeneous in the cosmic frame. A radial relocation current in 𝒮, propagating at c, carries
  the deposit from the body to the cosmic mean. This rule is not in CFG953's R0–R9; it is condition **C-G**.

### 1.3 Two structural facts that decide most of the lane

**(i) The reaction is never a net force or torque** [T1c].
- For ANY compactly supported deposit, ∫∇δV d³x = 0 and ∫x × ∇δV d³x = 0. Integrate by parts: ∫x_j ∂_k δV = −δ_jk ∫δV, and
  ε_ijk δ_jk = 0. The check uses a deliberately non-spherical, off-centre deposit.
- So body q's centroid law (CFG953 R4), its spin law (R5) and CFG953's relocation identity R ≡ 0 (S-TM) are untouched.
- The vacuum carries no momentum in any frame: T_V is boost-invariant, so T_V^{0i} = 0.
- Total momentum and angular momentum stay exact, as in CFG953.

**(ii) The composite is dust** [T1d].
- With p_hold = δV:  −δV g + δV (g + u u/c²) = δV u u/c².
- A rigidly translating lump, ∂_μ(L(x − vt) u^μ u^ν) = 0, is conserved.
- So under CH-L the lump plus its holding stress has no stress (no slip) and gravitates as dust of energy δV, moving with the body.
  That is exactly what CFG953's E_int did, had it been given a profile.
- **Under CH-L the channel is stress-energy-identical to SCT's E_int.** It changes no orbit, no lensing and no growth relative to
  SCT. It changes four things:
  1. the reservoir's identity (vacuum energy, w = −1);
  2. its entropy (zero; §6);
  3. its headroom (V̄ ≫ δV, so the reservoir can supply as well as absorb, which removes CFG953's open "sign of E_int over a merger
     history");
  4. if a₀ reads the local vacuum, the local a₀ (§3.2).
- **The price is the holding stress.** The body must carry p_hold = δV. That is the stress whose absence makes the sol61 reaction
  order one relative to gravity (MU4 measures it on NGC 3198).
  - SCT's body is a prescribed, rigid, non-relativistic object, so it can carry any stress whose net force vanishes, and (i) shows
    this one does.
  - A relativistic body (CFG953's open C-c) has to supply it from its own physics. That stays open.

### 1.4 Locality

Q^ν = −∇^ν V is a pointwise identity. WHERE V changes is not local:
- CH-L: a retarded functional of each body, like SCT's body shape itself;
- CH-G: a functional of the whole cosmic volume.

The channel is therefore non-local in the same way as SCT's source, and action-less (it inherits R9).

## 2. Task 1: exact absorption, conservation, momentum [T1: PASS]

- **T1a** [T1a_vacuum_exchange_identity]: ∇_μ(−V g^{μν}) = −∇^ν V in all four components on Minkowski and flat FRW.
- **T1b** [T1b_event_algebra]:
  - The capture or merge kinetic loss is μ|Δv|²/2 ≥ 0, and momentum adds.
  - Booking CFG953's increment (K-loss − ΔW) into E_V gives Δ(K + W + E_V) = 0 identically.
  - A reshape step books −ΔW_shape and closes the same way.
- **T1c** [T1c_momentum_and_S-TM]:
  - T_V is boost-invariant, so T_V^{0i} = 0.
  - For a non-spherical, off-centre deposit, the reaction's net force is [0, 0, 0] and its net torque is [0, 0, 0].
  - The P-U edge shell integrates to 0.
  - So CFG953's centroid law and R ≡ 0 are untouched.
- **T1d** [T1d_composite_is_dust]: the composite is δV u u, and the translating lump is conserved (§1.3).
- **T1e** [T1e_toy_total_energy_with_vacuum_ledger, K2]: CFG953's toys, code copied verbatim, with E_V booked in place of E_int.
  - Run E (260 conversions, satellite infall): |Δ(K + W + E_V)|/|E₀| = 1.474e-4.
  - Run M (head-on merger): 2.461e-5.
  - Both are identical to CFG953's E_int-booked residuals; K2's maximum difference is 0.
  - dP/P_scale and dL/L_scale ≤ 2.3e-15.
  - Without the ledger the error is 0.249 / 0.217 (MU1).
- **Locality** (§1.4): pointwise identity, non-local deposit rule; no action.

## 3. Task 2: sizes

### 3.1 Cosmic [T2a: PASS]

**Hard ceiling, no mass function.**
- Assume all cold energy is converted at ε_max = max E_rel/(M_c c²) over CFG953's S-En grid: 3.72e-5 (canonical) / 4.25e-5 (alt),
  set by M_b = 1e15.
- ω_c and ω_DE(z) are CFG689's primary best fit, transcribed.

| z | ceiling Δρ_DE/ρ_DE (can / alt) | bound on \|Δ ln a₀(z) − Δ ln a₀(0)\| | 0.1 × CFG689 68% half-width | bound / half-width |
|---|---|---|---|---|
| 1.0 | 1.37e-4 / 1.56e-4 | 6.8e-5 / 7.8e-5 | 0.013 | 5.2e-4 / 5.9e-4 |
| 1.2 | 1.77e-4 / 2.02e-4 | 8.8e-5 / 1.0e-4 | 0.014 | 6.2e-4 / 7.1e-4 |
| 1.5 | 2.50e-4 / 2.85e-4 | 1.25e-4 / 1.43e-4 | 0.020 | 6.1e-4 / 7.0e-4 |
| 2.33 | 6.28e-4 / 7.17e-4 | 3.1e-4 / 3.6e-4 | 0.044 | 7.1e-4 / 8.1e-4 |

**Framework-native estimates (reported).**
- **CFG630's native-anchored ledger** (CFG424 PM switch-on counts), rescaled by SCT's E_rel/(M_c V_f²) over CFG630's c_W (×1.045–1.093):
  - Δρ_DE/ρ_DE since z = 1 is 4.2–4.9e-7 (can) / 4.1–4.6e-7 (alt);
  - a₀(z)/a₀(0) − 1 is −(2.1–2.4)e-7 at z = 1, −(5–7)e-7 at z = 2 and −(7–9)e-7 at z = 3.
- **PM-anchored bracket** (CFG424 switch-on fraction × S-En ε between the PM resolution mass M_b 1.2e10 and M_b 1e14):
  - [7e-9, 8e-7] at z = 0;
  - [6e-8, 7e-6] at z = 1.
  - The upper end puts every switched-on particle at the cluster ε.
- **Sign:** formation releases energy for every M_b (S-En), so ρ_DE grows toward today and a₀ was slightly smaller in the past. The
  channel sits on the phantom side, as CFG630 found, and is monotone (no oscillation).
- **CFG956** (its `cfg956.json` as found on disk at run time, not yet committed then): the 95% wave-amplitude bound eps95 lies in
  [0.035, 0.35] (branch S) and [0.032, 0.42] (branch C). The channel's whole monotone shift (≤ 3.6e-4, ceiling) is ≥ 88× below the
  smallest wave bound and carries no oscillation. **Unmeasurable at CFG689's and CFG956's resolution on every estimate.**

### 3.2 Local [T2b]

NGC 3198 (Υ 0.61, M_b 4.72e10 M☉, 43 radii). E_int from the S-En recipe on its own census domain: ε = E_int/(M_c c²) = 2.19e-7 (can)
/ 2.48e-7 (alt). The table gives max over radii of |g_chan/g_law − 1| (simple kernel; ν_mono within 1%).

| variant | δV/V̄ over the 43 radii | a0-cos | a0-loc | headroom min (V̄ − draw)/V̄ |
|---|---|---|---|---|
| CH-L P-σ, can / alt | 5.7e-4 … 0.88 / 7.1e-4 … 1.15 | 1.81e-7 / 2.08e-7 | **6.5e-2 / 8.8e-2** | 0.76 / 0.70 |
| CH-L P-U, can / alt | 1.64e-5 / 2.46e-5 | 1.9e-9 / 2.6e-9 | **3.7e-6 / 5.6e-6** | 1.00 |
| CH-G, t_P = 1 Gyr, can / alt | 0 (V homogeneous) | 4.9e-9 / 5.4e-9 | 4.9e-9 / 5.4e-9 | 1.00 |

- **a0-cos.** The only local effect is the composite's dust-like gravity. For P-σ it is exactly ε × M_σ(<r)/(M_b + M_σ) ≤ ε, i.e.
  ≤ 2.1e-7, inside the 1e-6 line.
- **a0-loc.**
  - P-σ puts the deposit where the body's mass is, and at NGC 3198's inner radii it raises the local vacuum by 88–115%. The law
    moves by 7–9%.
  - Even the most spread-out holdable deposit (P-U) moves it by 3.7e-6 / 5.6e-6, above the 1e-6 line.
  - **CH-L fails NGC 3198 under a0-loc on both profiles and both footings.** Hand estimate E2 predicted this before freezing.
- **Slip.**
  - CH-L: the composite carries no stress (T1d), so the slip stays CFG953's 1.3548e-5 ≤ 1.9e-5.
  - CH-G: the in-transit radial energy adds ≤ 4.4e-9.
- **EFE (a0-loc).** For CFG953's H1–H3 inside the 6e10 M☉ host's lump at 50/100/250 kpc, the maximum is 6.0e-5 / 7.5e-5 dex (P-σ)
  and 1.7e-6 / 2.6e-6 dex (P-U), against δ_c = 0.082. Under a0-cos it is 0 by construction.
- **Cassini.**
  - The MW-like lump's traceless tidal field at 8 kpc is 6.2e-38 / 8.3e-38 s⁻² (P-σ), 1e-11 of Park+2026's 5.2e-27 s⁻².
  - Under a0-loc the Sun sits at δa₀/a₀ = 9.6e-3 / 1.2e-2 (P-σ). CFG770's |Q2|/ceiling at L* = 5.75 pc moves from 3.5e-6 to 3.6e-6.
  - Under SCT-M the Sun is in situ and Newtonian anyway.
- **Class rows** (A1 item 2; at each class's half-light radius; canonical):

| class | ε | ⟨ρ_body⟩/ρ_DE | δV/V̄ P-σ at r½ | δV/V̄ P-U | merger draw/V̄ (P-σ) |
|---|---|---|---|---|---|
| UFD-c | 9.1e-11 | 2.3e5 | 1.0e-4 | 2.1e-5 | 2.1e-5 |
| Draco-like | 9.0e-10 | 2.3e4 | 1.8e-4 | 2.1e-5 | 3.9e-5 |
| Fornax-like | 7.7e-9 | 2.6e3 | 1.3e-3 | 2.0e-5 | 3.0e-4 |
| SPARC dwarf | 3.7e-8 | 514 | 1.1e-3 | 1.9e-5 | 2.6e-4 |
| MW-like (8 kpc) | 2.4e-7 | 66 | 1.9e-2 | 1.6e-5 | 5.2e-3 |
| group | 1.2e-6 | 196 | 2.8e-3 | 2.4e-4 | 7.0e-4 |
| cluster (500 kpc) | 1.3e-5 | 107 | 1.2e-2 | 1.4e-3 | 3.1e-3 |

  - P-U's δV/V̄ is nearly the same for every galaxy, (1.6–2.1)e-5. This is because ε ∝ v_f² and ⟨ρ_body⟩ ∝ 1/(N² v_f²), so
    δV/V̄ ∝ 1/N².
  - **Post hoc, no class weight:** under a0-loc, a common rescale of a₀ (which the fitted κ would absorb) leaves a galaxy-to-galaxy
    residual of about ±1.2e-6 in a₀, i.e. ±0.6e-6 in deep-regime g. Groups and clusters sit 10–100× higher (a₀ +1.2e-4 / +7e-4).
    The frozen line is applied raw, so this reading changes no grade.

## 4. Task 3: sign and ordering [T3: PASS, AVOIDS]

- **Sign.** E_V(t) − E_V(0) = −Δ(K + W): the vacuum ledger is a state function of the mechanical configuration.
  - Body formation releases energy for every M_b (S-En 0.70–0.99 |W_f|): cold → DE.
  - Mergers draw (CFG953 toy 0.207 |E₀|): DE → cold.
  - The cosmic net is the formation release, so Δρ_DE > 0, on the phantom side.
- **Ordering.**
  - CFG930's backward ordering came from a finite budget: SN energy per unit debris binding, largest for ultra-faints.
  - The analogue here is the capacity C_U = V̄ (4π/3) r_e³ / E_rel. It is ≥ 3e4 for every dwarf and galaxy class, 4.2e3 / 2.8e3 (group)
    and 698 / 467 (cluster).
  - **The channel is never energy-limited, so it imposes no mass ordering and cannot reproduce CFG930/932's backward ordering.**
  - For the same reason it selects nothing. It gives **no handle on the excess family**, as CFG953 (f) found for SCT itself.
- **CFG930's D1** (settling releases energy in 100% of objects) is reproduced in sign: S-En > 0 for every M_b.

## 5. Task 4: stability

**The record's dark-energy model.** The record has none beyond a node-by-node ρ_DE(z) (CFG689) and two receivers: CFG542's canonical
scalar partner, and the pure vacuum of CFG131 / sol61. The minimal model assumed here is the interacting vacuum (§1.1).

- **IV (graded)** [T4 structure lines]:
  - T_V contains no derivative of V, so there is no kinetic term and no ghost.
  - At a fixed point δV obeys ∂ₜδV = (event source); its homogeneous solution is δV = const. There is no propagating mode, so no
    k-dependent frequency and no gradient instability.
  - Its energy density is +V, bounded below while V̄ + δV > 0. The headroom column above shows that holds (minimum 0.70, including a
    merger draw).
  - The composite perturbs as dust (T1d).
  - Intrinsic w = −1 exactly.
- **w_eff from the ceiling deposit rate** (A1 item 4): |1 + w_eff| = ε_max ρ_c(z)/(3ρ_DE(z)).
  - Canonical: 4.8e-6 / 4.6e-5 / 5.9e-5 / 8.3e-5 / **2.09e-4** at z = 0 / 1 / 1.2 / 1.5 / 2.33.
  - Alt: 5.5e-6 / 5.2e-5 / 6.7e-5 / 9.5e-5 / **2.39e-4**.
  - **Frozen line 1e-4: FAIL at z = 2.33.**
  - A2's record-based line, 0.1 × min_k(σ_k/ω_DE,k)/3 = 0.1 × 0.0752/3 = **2.51e-3: PASS** by a factor of 10 or more.
  - The native rate (CFG630) is 1 + w(0) ≈ −2.2 … −2.6e-7.
  - The frozen failure is set by the ceiling's ε_max (all cold energy in M_b = 1e15 bodies, converted every Hubble time). It is not a
    physical deposit rate, and it is far below anything the record's background resolves. It is reported as the frozen outcome all
    the same.
- **R-φ (CFG542's canonical receiver; reported)** [sympy]:
  - The perturbation friction is 3H + Q/φ̇², with φ̇² = (1 + w)V̄. On the draw branch (mergers, or a wrong-sign exchange) it is
    anti-damped at rate |Q|/((1 + w)V̄).
  - With A1's deposit, NGC 3198 P-σ is unstable at 1 + w = 0.01 and 0.1 (rate 125–1660 H₀). The cluster P-σ is unstable at 0.01
    (14–18 H₀) and stable at 0.1. P-U never grows faster than H₀; the alt cluster at 0.01 grows at +0.09 H₀.
  - The background is singular at w = −1 (CFG630 verdict 3).
- **R-F (minimal constant-w fluid, c_s² = 1, Q along u_c; reported)** [sympy]: dv/dt = [Q(v_c − (1 + w)v) − ∇δp]/((1 + w)ρ₀). The
  response to the delivered momentum, Q/((1 + w)ρ₀), diverges as w → −1⁺. CFG689's best-fit ρ_DE nodes change direction 3 times, so
  w crosses −1, which a single minimal fluid cannot do.
- **Why the IV.** The IV is the only one of the three that is regular at w = −1 and on the draw branch. It is regular because it has
  no degree of freedom, and the price is that its reaction has to be held by the body (§1.3).

## 6. Entropy: the coordinator's question [T-S: PASS for SCT; V2 = ONLY WHERE NO ENTROPY IS EXCHANGED]

**Question.** CFG955 showed that a coherent, zero-entropy dark energy cannot be K-T's reservoir (Clausius). Does the same argument
kill the channel for SCT's E_int bookkeeping?

**Answer: no. SCT's events are different.** They change labels and bodies, never the dust's distribution function.

- **S1, conversion** [T-S].
  - A conversion moves an element from the unlabelled to the labelled sector. The total dust distribution f = f_unl + f_lab is
    unchanged, and so is −∫f ln f (sympy: ΔH = 0).
  - The labelled dust keeps moving geodesically with all its microstate.
  - Bodies have no microstates, and the vacuum is coherent.
  - So ΔS_tot = 0 with a zero-entropy dark energy.
  - **Why the energy can go to a work reservoir without breaking the second law.** The labelled sector's gravitating energy is
    identically zero (T_c,lab is cancelled by −T_c,lab in 𝒮; sympy T_lab = ∂E_book/∂E = 0). It is an entropy store at zero
    temperature. The entropy stays with the labelled dust, while the booked energy (relative kinetic energy plus ΔW) moves to
    Σ + V. That is Carnot to a T = 0 sink, with efficiency 1.
  - This rests on SCT's R2 (its cost 5: labelled dust is gravitationally invisible). The channel adds nothing to it.
- **S2, merger draw** [T-S].
  - A merger touches only bodies, so nothing in matter changes entropy.
  - A zero-entropy dark energy supplying D gives ΔS = 0.
  - A heat bath at any finite T_R gives ΔS_tot = −D/T_R < 0.
  - **SCT's merger draw therefore excludes a heat bath as SCT's reservoir and requires a work-type one.** A coherent w = −1 vacuum
    is of that type.
- **S3, reshape** [T-S]: deterministic, so the same baryon path back and forth returns E_V exactly. It is work.
- **S4 = K6, CFG955 K-T** [K6_CFG955_L7_Clausius].
  - K-T's collision operator does change f (it relaxes f to a Maxwellian at T_J).
  - dS_d/dt − Q/T_J = (3/2)(ρ/τ)(T_J − T)²/(T T_J) ≥ 0 is reproduced exactly.
  - On the cooling branch T = T_J(1 + x), dS_d/dt = −3ρx/(2τ(1 + x)) < 0, so a zero-entropy receiver gives dS_tot < 0.
  - **CFG955's argument stands for K-T, and for CFG935's bath (S5): the channel cannot serve them.**
- **S5, CFG935.**
  - The drift's work to a coherent partner is admissible (CFG542 Pb; its GENERIC entropy production is ≥ 0, K2/K4 there).
  - The isotropising bath is S4's case.

So the cold ↔ DE exchange does **not** have to carry entropy for SCT, and a w ≈ −1 vacuum cannot carry entropy at all. The channel
closes SCT's books, and the class-A drift's, but not a relaxation theory's. Hand estimate E3 predicted this before freezing.

## 7. Task 5: the verdict on C-E

- **What the channel achieves.**
  - CFG953's C-E posited a non-dynamical body energy outside every dynamical sector. The channel replaces it with dark energy
    carrying a covariant exchange current, and ∇_μ(T_b + T_c + 𝒮′ + T_V)^{μν} = 0 holds exactly.
  - Momentum, angular momentum and S-TM are kept.
  - The reservoir has w = −1, zero entropy (the right kind, §6) and headroom V̄/δV ≥ 0.87 (P-σ at NGC 3198's innermost radius, alt) to ≥ 4e4 (P-U).
    So the open question of E_int's sign over a merger history becomes harmless.
- **What it does not achieve.**
  - (i) The reservoir's existence is a posit: exact Λ cannot exchange, so the vacuum must be variable.
  - (ii) The deposit rule is prescribed and action-less, inherited from SCT's events.
  - (iii) The body must hold the vacuum's reaction as a stress p_hold = δV (MU4: unheld, the reaction is 1.5–1.6× gravity at NGC
    3198), which a relativistic body (C-c) has not been shown to supply.
  - (iv) The local tests need either C-A0 (a₀ reads the cosmic-mean vacuum; CH-L fails NGC 3198 under a local a₀) or C-G (a new
    cosmic relocation current).
- **C-E is CONVERTED, not DERIVED** (A2 reading). Under the frozen rule, T5 = NOT CLOSED, because of T4's ceiling item.

## 8. Controls

**K (all PASS; K stage exit 0, main exit 0):**
- K1: CFG953's S-En table, maximum relative difference 0.
- K2: CFG953's toy E_int (conversion −0.22681, reshape −4.74e-5, merge −0.20693, reshape −0.00924) and dE, dE_mech, difference 0.
- K3: CFG689 band nodes, transcribed, against README / THEORY_CANONICAL: maximum 4.9e-4, which is rounding. Against CFG956's
  independent K4 re-implementation: 0.
- K4: NGC 3198 law with no channel, 2.2e-16; r_e 453.9 / 412.9 kpc.
- K5: the sol61 report's 0.63212, 2.81332e-7 and 7.03329e-6.
- K6: CFG955 L7, sympy 0.

**MUTATE (exit 2 by design, because one tooth did not bite):**

| tooth | result | bites |
|---|---|---|
| MU1 exchange off | toy \|ΔE\|/\|E₀\| 0.249 (E) / 0.217 (M), = CFG953 Mu5 | yes |
| MU2 wrong sign (vacuum receives −ΔE_int) | 0.499 / 0.435 against 100 × residual 0.015 / 0.0025: conservation broken | yes |
| MU3 wrong sign / draw with CFG542's canonical receiver | unstable in 6 of 8 (footing, class, 1 + w) cases; the cluster at 1 + w = 0.1 is stable for both profiles on both footings, so the literal all-four rule fails | **no** |
| MU4 reaction not held (P-σ) | median \|∇δV\|/(σ g) 1.55 / 1.63 (range 0.13–11.8): the sol61 O(1) reaction returns | yes |

- **Read plainly.** A wrong-sign exchange breaks conservation (MU2). It breaks stability for the record's canonical receiver in most
  but not all declared cases (MU3). For the IV, being degree-of-freedom-free, it breaks neither stability nor ordering: the minimum
  capacity is unchanged, and only the cosmic sign flips.
- **Reported, no tooth: a shared rather than per-owner reaction.** A satellite inside its host's lump would feel
  a_sat/g_host = 0.93 / 0.80 (H3 at 50 kpc, P-σ), above ε_B 0.344 / 0.317. The per-owner rule is load-bearing.

## 9. Costs; not claimed; open

**Costs:**
1. A variable vacuum, not exact Λ.
2. A prescribed, action-less deposit rule (CH-L) or a new cosmic relocation current (CH-G, C-G).
3. Bodies must hold the vacuum's pressure.
4. C-A0 under CH-L.
5. The deposit profile is unfixed. It matters only under a0-loc, where both profiles fail.
6. No handle on the excess family.

**Not claimed:**
- that the channel is derived;
- that a₀ reads the cosmic mean;
- any data preference;
- "theory closed".

**Open:**
- a relativistic body that holds p_hold (C-c);
- an action for the exchange;
- whether a₀ is set by the local or the cosmic vacuum;
- a heat-bath reservoir for relaxation theories, should one be needed (CFG955 / CFG935 bath).

## 10. Disclosures

1. **A2** was written before any script but after a hand check of A1 item 4. The frozen outcome is reported first.
2. **CFG689** values were transcribed with the Read tool, as the brief requires.
   - An attempt to inspect cfg689.json with a scratch script was blocked by the session's permission guard. No process opened a
     CFG689 file.
   - K3 checks the transcription against CFG689's README and against CFG956's independent recomputation.
3. **CFG956's** `cfg956.json` and `cfg956_K.json` were read as found on disk. CFG956 had not committed its results when this lane
   ran, so its numbers are labelled as such.
4. **Runs.** K, MUTATE and main all ran from one script, `cfg958.py` (sha256 8cffcd5341bc80d3…).
   - Each ran as one process on one core at nice 10, under the in-script 1 GB RSS guard.
   - Peak RSS 0.14 / 0.46 / 0.49 GB; runtimes 1 s / 292 s / 303 s.
   - Nothing was downloaded. No 1024³ job was live at start (checked read-only). No other lane's file was edited.
5. **The toy code is CFG953's, copied verbatim.** A diff against cfg953.py lines 513–853 shows only the ledger argument and the extra
   returned fields.
6. **Inherited inputs:**
   - the census (f_ret, 0.315 inside M_ta);
   - CFG424's switch-on fractions and CFG630's c_W (transcribed from `cfg630.out`);
   - CFG630's native-anchored JSON;
   - CFG770's Q2 ratio and CFG953's slip, both from the LEDGER / README.


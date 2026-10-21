# CFG941 DERIVATION: can CFG938's tethered medium also gravitate on itself?

Criteria: `FROZEN_CRITERIA.md` (0b41bd0cf, committed alone first); amendment A1 (7c395c866, pre-result). Every load-bearing step
has a sympy or numeric check in `cfg941.py`; check names are in brackets. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻²,
never pooled. Cold energy, no particle species. Not "theory closed". K = 4πG, u = |Dχ|, R(u) = u²/(a₀ − u), D_full(u) = u + R(u).

**Overall class (frozen rule): STRUCTURAL OBSTRUCTION.** The coefficient that makes the law the medium's static equilibrium is
the same coefficient that removes the medium's linear self-gravity and its gravity on other tethered medium. No repair passes
(a)–(e) together. The only one that restores a¹ growth while keeping the law (the turnaround gate R3θ) carries a ghost. Every
repair fails (f) and (g), so class A (the T1x/T2x/NC1x shear-pass engine) is not the non-relativistic limit of any parent tested
here, and those shear results do not transfer.

---

## 1. Diagnosis of F1

### 1.1 No source double count [D1]
Vary the static Lagrangians in Φ:
- CFG938: L = −|∇Φ|²/2K − (ρ_b + ρ_c)Φ − W_full(|∇χ|) + λ(∇²χ − Kρ_c) gives ∇²Φ = K(ρ_b + ρ_c).
- S2 square form + ID: L = −|∇Φ − KP|²/2K − ρ_bΦ − W_rem(K|P|), ∇·P = ρ_c, gives the same ∇²Φ = K(ρ_b + ρ_c).
- Keeping both the dust coupling −ρ_cΦ and S2's P·∇Φ gives ∇²Φ = K(ρ_b + 2ρ_c). That is the double count; M2a shows it breaks
  the law (deviation 6.4 / 7.2 on NGC 3198).

So the medium's rest mass sources Φ exactly once, in S2 and in CFG938. S2's tether term P·∇Φ *is* the rest-mass coupling
(−δρ_cΦ + divergence); it is not an extra one. The baryons and light feel the medium's full gravity.

### 1.2 What cancels the self-gravity [D2a, D2b]
**Energy.** One Fourier mode, ρ_b = B cos kx and two tethered components C₁, C₂ (C = C₁ + C₂), with a tether whose quadratic part
is c₂u²/2K:

  ⟨L⟩ = (K/4k²)[(B + C)² − c₂C²],  ∂²⟨L⟩/∂C₁∂C₂ = −2πG(c₂ − 1)/k²,  self term −πG(c₂ − 1)/k² per C₁².

W_full = u²/2K + u³/(3Ka₀) + … has c₂ = 1. Its quadratic part (S2's critical quadratic −K|P|²/2) cancels the medium's Newtonian
self-energy and the C₁C₂ mutual term together. The baryon–medium term 2πG/k² survives. CFG938's S8 result is the c₂ = 1 case.

**Force.** With χ the medium's own potential (D²χ = Kρ_c) and Φ = Φ_b + χ:

  f_medium = −∇Φ + D_full(|∇χ|)∇̂χ = −∇Φ_b + R(|∇χ|)∇̂χ.

The tether's linear part, +∇χ, is exactly the medium's own Newtonian pull. **F1 is a force cancellation by the u term of
D_full, not a cancellation of the medium's Poisson source.** Because χ is linear in the total medium density, the same term
removes the pull of any other tethered medium (the cross term behind F2).

### 1.3 Theorem D-T: the law forces c₂ = 1 [DT1–DT4]
Take a cold static medium held by any always-on tether force F(u). Its phantom is its own gravitating mass, so g = g_N + u.
- Equilibrium gives F(u) = g. With the law g_N = g²/(g + a₀), sympy gives F(u) = a₀u/(a₀ − u) = D_full(u) exactly [DT1], and
  F = u + u²/a₀ + u³/a₀² + … [DT2].
- For any law with the deep limit g_N → g²/a₀, i.e. g_N = (g²/a₀)(1 + h₁g/a₀ + h₂(g/a₀)² + …), the series inversion gives
  F = u + u²/a₀ + …, with linear coefficient 1 independent of h₁, h₂, h₃ [DT3]. It is the deep limit that forces c₂ = 1, not
  the simple interpolation.
- Only c₂ = 1 gives the BTFR. For F = c₂u + u²/a₀: lim V⁴/(GMa₀) = 1 at c₂ = 1, ∞ at c₂ = ½ (an acceleration floor), and 0 at
  c₂ = 2 (rescaled Newton) [DT4].

Physically, in the deep regime the medium's own field dominates (u ≈ g ≫ g_N). A cold medium at rest there must be held up
against its own gravity, so the tether's linear term must equal the medium's own field. The linear self-gravity coefficient is
(1 − c₂)Kρ_c (D2a, D6). Hence **(a) ⟹ c₂ = 1 ⟹ no linear self-gravity of the settling medium, and no mutual gravity between
tethered components**, wherever the tether acts with its static-law coefficient. F1 is structural to S2+S3. Any parent that
reduces to S2+S3, CFG938 included, inherits it.

### 1.4 A correction to CFG938's growth exponent [D5a, D5b, D6]
CFG938 puts χ = χ̄(t) on FRW with D²χ̄ = −3Hχ̄̇/c² = Kρ̄ (its S1d). That is a **timelike background gradient**,
χ̄̇/c² = −Kρ̄_c/(3H), which does not depend on c. Its spatial projection vanishes only for a comoving medium. Covariantly, to
second order in the peculiar velocity V and in δχ, sympy gives exactly

  u² = h^{μν}∂_μχ∂_νχ = |∇δχ + (χ̄̇/c²)V|²  [D5a],

while the first-order constraint stays ∇²δχ/a² − 3Hδχ̇/c² = Kδρ_c, with no velocity term [D5b].

So at linear order −W_full(u) ≈ −|∇δχ + βV|²/2K, with β = −Kρ̄_c/(3H). On top of the cancellation this does two things:
- it reduces the medium's inertia by β²/(Kρ̄_c) = Ω_c/6 (0.1405 in the matter era);
- it adds a force (Kρ̄_c/3) q ψ, with q the deceleration parameter (q = ½ in EdS; destabilizing).

CFG938 S6 omitted the term. In EdS with Ω_c/Ω_b = 5.364 and free baryons:

| case | growth exponent n (δ ∝ aⁿ) |
|---|---|
| CFG938 S6 approximation (medium feels baryons only) | 0.60954 (K3, and K4 by this lane's Lagrangian route) |
| full quadratic action including the χ̄ gradient | **0.69433** (an independent eigenvalue check agrees to 1e-15) |
| dust (c₂ = 0) | 1.000000 |

The correction raises the exponent but leaves F1 in place. CFG938's files are not edited. One consequence, flagged and not
pursued: in this parent the χ̄ gradient is a preferred frame for moving medium. Its effect in galaxies is estimated, not
computed here, to be suppressed by about ρ̄_c/ρ_galaxy. Today |χ̄̇|/c = Ω_cH₀c/2 = 0.925 a₀ (canonical). The script prints this number; no claim is made about it.

How fast growth comes back as the tether coefficient is lowered (EdS):

| c₂ | 0 | 1e-3 | 3e-3 | 1e-2 | 0.1 | 0.3 | 1 |
|---|---|---|---|---|---|---|---|
| n (no boost / boost) | 1 / 1 | 0.99957 / 0.99972 | 0.99872 / 0.99915 | 0.9957 / 0.9972 | 0.957 / 0.971 | 0.872 / 0.911 | 0.6095 / 0.6943 |

|n − 1| < 1e-3 needs c₂ ≤ 2.35e-3.

## 2. Hover lemma and F2

**Lemma.** In any static cold tethered equilibrium the net force on medium at rest vanishes, by the equilibrium equation itself.
This is CFG939's flat frozen potential. A satellite's tethered medium inside a host's settled medium therefore feels no host
force to leading order. Only the satellite's own fields act on it, and they average to zero over its centre of mass. The
satellite's stars feel the full host field. So Δa = a_medium − a_stars = u_h + R(u_h) = g_host on the host's law. CFG938's S8
quoted u_h, the host-medium part; the full differential also includes R(u_h) = g_bh.

**Numbers** [main, F2 table]. CFG882's Plummer dwarfs sit at the centre of their own (isolated-law) medium in a 6e10 M⊙ host's
settled field. The second-order centre-of-mass average is computed exactly over the satellite's medium, using 64-point
Gauss–Legendre in angle and 4000 shells.

| | 50 kpc | 100 kpc | 250 kpc |
|---|---|---|---|
| g_host / a₀ (canonical) | 0.208 | 0.099 | 0.039 |
| Δa / g_host (H1–H3, both footings) | 1.017–1.094 | 1.027–1.107 | 1.038–1.080 |
| satellite baryonic pull at its scale radius / Δa | 0.017–0.095 | 0.035–0.196 | 0.090–0.52 |
| time for the stars to leave their medium (one scale radius) | 9–45 Myr | 13–65 Myr | 21–106 Myr |
| ambient medium response rate / satellite crossing rate | 4e-4 – 9e-3 | 1e-4 – 3e-3 | 3e-5 – 8e-4 |
| static on-axis EFE factor of the satellite phantom | −0.41 to −0.73 dex | −0.24 to −0.49 dex | −0.10 to −0.24 dex |

**Reading (an estimate, with the assumptions in §6).**
- Universal free fall fails by about 100% for tethered satellites.
- The satellites' own baryons bind their medium 2–60 times more weakly than the differential, so stars and medium separate
  within about 10–100 Myr.
- The ambient medium re-settles 10²–10⁴·⁵ times more slowly than a satellite crosses itself. A moving satellite therefore
  carries no settled medium.
- Even a static satellite would have its phantom cut by 0.1–0.7 dex by the host's medium field (an EFE).

The record's satellite reading (CFG925 R3) is that satellites already sit above the EFE-free law. **CFG925 R3 is not respected**
by any tethered sector. M4 (tether off) restores universal free fall to 3.5e-16.

## 3. The repairs

### R1: dust gravity kept, tether only redistributes (W_full → W_rem): NOT REPAIRABLE
- **(a) FAIL.** Static states need u ≥ a₀/2. The law deviation is 1.645 / 1.884, identical to CFG938's M3 tooth (K6). There is
  an acceleration floor g → a₀/2; lim V⁴/(GMa₀) = ∞, and the value at y = 1e-14 is 2.5e13.
- **(b) PASS.**
- **(c) PASS.** n = 1 exactly. W_rem has no quadratic term, so there is no χ̄ boost either. Sub-L*: stiffness Jeans
  oscillation for k_phys L* > √2.
- **(d) PASS.** Bounded, Jeans-type only. min ω²/(Kρ₀) = 0 / 8 / 98 about R1 states at u₀/a₀ = 0.5 / 0.9 / 0.99; the 0.0909 grid
  point has no R1 state. Inertia margin 6.2e4.
- **(e) FAIL.** Worst s_847 = 3.28e-5 on R1's own static states.
- **(f) FAIL.** The mutual term becomes Newtonian, but the hover lemma holds in R1's own settled host: Δa/g_host = 1.0000.
- **(g) FAIL.**

**Why NOT REPAIRABLE:** D-T. An always-on tether passes (a) only with c₂ = 1, and c₂ = 1 cancels the linear self-gravity.
"Dust gravity plus a redistribution-only tether" with the law unchanged is impossible. R1 is the c₂ = 0 corner.

### R2: two separately conserved media (free dust + tethered), no conversion: NOT REPAIRABLE
- **(a) FAIL (joint reading, criteria §4).**
  - A galaxy with only tethered medium is P0 (2e-16).
  - Growth needs f_t ≤ 0.0602. Then galaxies form from a mix with q = 15.6 times as much free as tethered mass.
  - The free mass enters the law's source: the tethered equilibrium is R(u_t) = g_b + g_f, varied first and substituted after.
    The law deviation is 74 / 82.
  - Even the most generous catchment (CFG888's 53.64 M_b) supplies only 0.68 / 0.61 of NGC 3198's phantom.
- **(b) PASS.**
- **(c) FAIL.** On the composition that passes (a) (f_t = 1), n = 0.6943 / 0.6095. The tethered medium keeps c₂ = 1.
  n → 1 only as f_t → 0, where the tethered medium rides along on the free medium's gravity.
- **(d) PASS.** Two-component WKB: min ω² ≥ −(ρ_f + ρ_t).
- **(e) PASS.** 1.54e-5.
- **(f) FAIL** for tethered satellites (only free cold energy falls universally).
- **(g) FAIL.**

### R3n: density gate s(ρ_c): NOT REPAIRABLE
- **ρ_\*.** ρ_\* = 1.53e-23 / 1.68e-23 kg m⁻³ = 6771 / 7447 ρ̄_c0. This is the least restrictive value that keeps NGC 3198's 43 radii
  on the law; all ρ_ph there are positive.
- **(a) FAIL.** The law's phantom density falls as r⁻², so the tether ends at r_\* = 73 kpc and lim V⁴/(GMa₀) = 0. CFG847's
  MW-outer, group and cluster systems are gated off.
- **(c) FAIL.** The cosmic mean exceeds ρ_\* at z > 17.9 / 18.5, where n = 0.694.
- **(d) FAIL.** At large k the gate gives c_eff² = ρ₀(s″W + sγ) [R3n_k2_coefficient]. In the upper half of the transition shell
  s″ < 0 and c_eff²/(sγρ₀) reaches −3.4e7 (L* = 24 pc) and −2.0e4 (1 kpc): a gradient instability, Im ω ∝ k.
- **(f), (g) FAIL.**

Why NOT REPAIRABLE: the deep BTFR needs s = 1 at every density down to 0, i.e. on the cosmic mean, which brings D-T back.

### R3θ: turnaround gate s(θ), θ = the medium's expansion (CFG649's switch, made local): PARTIAL (fails d, f, g)
- **(a) PASS.** Static states have θ = 0, and the quintic gate has s = 1, s′ = s″ = 0 there, so they are P0's: 2.2e-16, BTFR
  limit 1, y = 1e-14 value +1.0e-7.
- **(b), (e) PASS.**
- **(c) PASS.** The cosmic-mean medium has θ ≈ 3H ≥ 3H₀ > θ_s = H₀, so the gate and its first two derivatives vanish. The medium
  is pure dust, and n = 1 at every k, sub- and super-L*.
- **(d) FAIL.** −s(θ)W puts −½s″(θ)W(∇·v)² into the Lagrangian [R3theta_kinetic_term]. In the upper half of the transition
  s″ > 0 (up to 5.77/θ_s²), so the longitudinal kinetic coefficient ρ₀ − s″Wk² turns negative for k > k_g. That is a ghost band,
  with a degenerate kinetic surface at k = k_g.
  - For turnaround overdensity 5.55 at z_ta = 0 / 1 / 3 and R = 0.1–10 Mpc: k_g R = 2.19 / 0.77 / 0.23–0.27, i.e. at or above
    the perturbation's own scale.
  - This holds for every θ_s > 0.
- **(f), (g) FAIL.** In settled regions s = 1, so the settled sector is CFG938's: hover.

### R3ℓ: finite range of the medium's own potential (D²χ − χ/ℓ² = Kmn): NOT REPAIRABLE
- The linear tether removes the fraction k²ℓ²/(1 + k²ℓ²) of the self-gravity [R3ell_cancellation_fraction].
- **(c) FAIL.** It needs ℓ ≤ 13.1 pc (k = 5 h/Mpc at z = 1100), or ≤ 6.5 kpc for the largest scale k = 0.01 h/Mpc. At such ℓ the
  tether's reading of NGC 3198's medium is off by more than 100%.
- **(a) FAIL.** The finite-radius law at 1e-6 needs ℓ ≥ 63 Mpc (NGC 3198 medium out to 1 Mpc; scan step ×1.26, so the true
  minimum lies in 50–63 Mpc). The deep BTFR fails for every finite ℓ, since the Yukawa factor goes to 0. The two windows are
  disjoint by 4.0 decades (k = 0.01 h/Mpc) to 6.7 decades (k = 5 h/Mpc).
- **(b), (d), (e) PASS.** **(f), (g) FAIL.**

## 4. (g): class A is not the non-relativistic limit of any parent tested
Class A (CFG541/638; CFG649 R-A1/R-A2; CFG650/CFG654) has four features:
- every cold-energy particle feels −∇Φ with ∇²Φ = K(ρ_b + ρ_c): universal coupling and Newtonian self-gravity;
- the extra source exists only on turnaround balls around resolved peaks (enclosed 1 + δ ≥ Δ_ta(z));
- that source is zero-sum per catchment;
- the phantom is a functional of the catchment's own baryons, so there is no EFE.

Every tethered sector here instead has a medium force −∇Φ_b + R(|∇χ_total|)∇̂χ in settled regions (g1 fails). Its equilibrium
reads the total tethered field, including hosts and neighbours (an EFE), plus any free mass (g2 fails). Class A's switch needs
the cosmic mean density and a ball around a peak, and its own-baryon rule needs one tether per catchment. Neither is a local
covariant structure. A local θ gate gets the linear regime right (g3) but is a ghost. **The T1x / T2x / NC1x shear passes
therefore remain results of the class-A engine. They do not transfer to CFG938's parent or to any repair tested here.**

## 5. Class, and what is not claimed

| repair | class | fails |
|---|---|---|
| R1 (dust gravity, W_rem tether) | NOT REPAIRABLE | a, e, f, g |
| R2 (free + tethered populations) | NOT REPAIRABLE | a, c, f, g |
| R3n (density gate) | NOT REPAIRABLE | a, c, d, f, g |
| R3θ (turnaround gate) | PARTIAL | d, f, g |
| R3ℓ (range gate) | NOT REPAIRABLE | a, c, f, g |
| P0 (CFG938, reference) | — | c, f, g |

**Overall: STRUCTURAL OBSTRUCTION.** No repair passes (a)–(e), and D-T passes its checks.

What remains open (not tested, not claimed):
1. A ghost-free turnaround switch. It would need a new field with its own, probably non-variational (latching) evolution. It
   would still fail (f) and (g) unless the tether also became per-catchment.
2. Leaving the cold static tether altogether, with the settled medium held up by velocity dispersion and gravitating
   universally. In the deep regime the law's phantom density √(GMa₀)/(4πGr²) has the singular-isothermal form with
   σ² = V_f²/2 (the identity CFG888 noted). That would be a different theory, not a repair of this parent.

Not claimed:
- that any repair is a candidate;
- that κ, a₀, Ω_c/Ω_b or L* are derived;
- any data verdict beyond the framework-native statements above.

Not "theory closed".

## 6. Controls and disclosures
- **K.** K1 2.2e-16 (both footings); K2 w = 0; K3 0.60954; K4 the Lagrangian route equals K3 (line 1e-6; equal to the 8 printed
  decimals), and dust gives n = 1 to 1e-12; K5 s_847 1.5398e-5; K6 R1 = CFG938 M3 (1.6445 / 1.8844). All pass.
- **MUTATE.** All bite (exit 1):
  - M1: every repair removed gives 0.60954;
  - M2: double counting breaks the law (M2a 6.4 / 7.2, M2b 1.74 / 1.86);
  - M3: the χ̄ gradient moves n by 0.085;
  - M4: tether off gives Δa = 3.5e-16 g_host.
- **A1 (pre-result, 7c395c866).** The numeric BTFR point was moved from y = 1e-12 to 1e-14. The law's own correction is √y,
  so the frozen point would have failed the exact law by 2.5e-13.
- **Before the first run.** brentq's rtol floor, the K substitution in the growth determinant, zero-density rows at f_t = 0 / 1,
  a loop variable shadowing a sympy symbol, a sinh overflow in an unused branch, and literal test outcomes were all fixed. These
  were code fixes, made before any number existed.
- **First MUTATE attempt.** It crashed at M4: the satellite truncation bracket had no sign change when the satellite's phantom
  never reaches u_h. M1–M3 had already printed the values reported above. The fix (next item) touches only `satellite_hover`.
  K, MUTATE and main were then rerun in that order from one script. One more wording-only edit followed: a printed
  "> 4 decades" became the computed 4.0–6.7, and the ℓ-scan resolution is now printed. All three stages were rerun again from
  the final script (sha256 cf4edd42…); no number changed.
- **Implementation choices (not frozen; disclosed).**
  - The satellite medium is truncated at the outermost radius in [a/100, 100a] where u_s ≥ u_h, or at r_t = a if u_s < u_h
    everywhere.
  - The EFE factor is on the far-side axis, at the Plummer scale radius.
  - R2's joint free-mass model uses the tethered phantom's shape.
  - R3θ's transition example uses the total turnaround density for u₀. Using the excess (4.55/5.55 of it) instead would raise
    k_g by about 22%. The ghost band remains.
  - Δ = 1 and θ_s = H₀, as declared. The Yukawa medium runs out to 1 Mpc.
  - The response rate uses CFG938's kL* ≪ 1 dispersion.
  - λ̄ = 0 is the background choice for χ's multiplier (as CFG938 implicitly).
- **Assumptions of the F2 estimate.** The host is on the law at the satellite's radius; the satellite has a circular-speed orbit;
  there are no tides, no orbit history, no multistream structure of the satellite medium, and no stiffness in the response.
- **Compute.** One process, about 4 s, peak RSS 0.25 GB, run beside NC2x with OMP_NUM_THREADS=1 and nice 10. Nothing was
  downloaded. No other lane's file was edited.

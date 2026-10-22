# A39 — the tensor mass on a P̄ ≠ 0 background: does it break anything?

**Lane:** A39_tensor_mass · **Date:** 2026-10-21 · **Base:** `deepseek_push/DS_FINAL_2026_10_21/BRIEF.md`
**Script:** `a39_checks.py` (21/21 PASS, exit 0, 5.3 s) · **Output:** `a39.out` · **Data:** `a39_results.json`
**Action source (frozen, not re-derived):** `core_open_problems_round2_2026_10_20/03_relativity/report.md` §2, the same action A3 used.

---

## 0. Claim

**The TT mode does acquire a mass off the P̄ = 0 background, the mass is positive (no tachyon), and it is
harmless by 9–11 orders of magnitude.** Expanding `−√g W(u)` to second order in `h^TT` at fixed `P̄`
gives, exactly,

```
m_T² = u²(4−3x)/(1−x)² + 4a₀²[x + ln(1−x)],        x ≡ u/a₀ = K|P̄|/a₀.        (7)
```

The second term is the `√g` coupling of the TT mode to the background energy density `W` — the same
`¼ρ·tr h²` that every fluid contributes and that a cosmological constant does **not** turn into a
graviton mass; it cancels against the second-order expansion of the gravitational sector, which is
exactly Einstein for TT modes here (A3 §3.2: no operator carries two derivatives of `h^TT`), exactly as
the `¼Λ tr h²` of de Sitter cancels. What is left is the P-specific piece

```
m_T² = u²(4−3x)/(1−x)²,       = 4u² at u ≪ a₀,      > 0 for every 0 < x < 1.      (8)
```

A31 check 28 is qualitatively right — the quadratic tensor action is **not** the Einstein one off
`P̄ = 0` — but the number it quotes, `3Kp/8`, is `d²u/dh²`, not the `h²` coefficient of the action, so
it is not a mass (§1). The mass is `m_T ≈ 3×10⁻³⁴ eV` at `u = a₀/2`, a Compton wavelength of tens of
Gigaparsecs,
`8×10⁹` below the GW170817+LIGO graviton bound and `10²⁶` inside the speed bound. `c_T² = 1` survives
unchanged as a statement about the `k²` coefficient.

---

## 1. What A31 check 28 actually computed

`a31_checks.py:254` sets `u_pert = K*p/sqrt(1+h)` and takes `series(u_pert, h, 0, 3).coeff(h,2)`.
That is the second derivative of `u` itself:

```
u = Kp(1 + hc)^{−1/2} = Kp[1 − hc/2 + 3h²c²/8 + O(h³)],                          (1)
```

so the coefficient is `3Kp c²/8` — `3Kp/8` at `c = 1`, exactly as the ledger records (check C1
reproduces it). But `u` has the dimensions of an acceleration and `W` of an energy density: `3Kp/8`
cannot be a mass-squared coefficient. The action coefficient needs `W′(ū)` and `W″(ū)`, and they enter
with *different* coefficients (§2). So the *statement* in A31 (`the Einstein quadratic action holds only
on P̄ = 0`) survives, the *number* does not, and — the point of this lane — the magnitude was never
evaluated. It is negligible.

## 2. Derivation

### 2.1 Background and mode

Static galactic frame, `a = 1`, `N = 1`; `P̄_i = p n_i` with `u = K p` constant over the wave period
(the P-field's own range is `λ = 17 pc`, so a 100 Hz wave is deep in the WKB regime). One TT mode,
`k ‖ z`,

```
h_ij = h cos(kz) ε_ij,   ε = diag(1,−1,0),   tr ε = 0,   ∂_i h^TT_ij = 0.        (2)
```

The inverse metric is `g^ij = δ^ij − h^ij + h^{ik}h_k{}^j + O(h³)`; for this mode it is the exact
`diag((1+hc)^{−1}, (1−hc)^{−1}, 1)`. The `h²` term in `g^ij` is **not** optional: dropping it changes
the answer (mutant `inverse_linear`, 8 checks break).

### 2.2 The expansion of `−√g W(u)`

With `ū = Kp`, `δ ≡ h cos(kz)`, and `q ≡ ε_ij n^i n^j` (for `n ‖ x̂`, `q = 1`):

```
u    = ū(1 + qδ)^{−1/2} = ū[1 − qδ/2 + 3q²δ²/8 + O(δ³)],                         (3)
√g   = (1 − δ²)^{1/2}   = 1 − δ²/2 + O(δ⁴),                                       (4)
W(u)= W + W′δu + ½W″δu²,   W′ = (u/K)/(1−u/a₀),  W″ = 1/[K(1−u/a₀)²].             (5)
```

Collecting `O(h²)` and averaging `⟨cos²⟩ = ½`:

```
L ⊃ [ −√g W ]_{h²} = c h²,   c = ½[ ½W − (3/8)W′ū − (1/8)W″ū² ],                  (6)
m_T² ≡ −16K c = −4KW + 3KW′ū + KW″ū².                                             (7)
```

With `KW′ū = u²/(1−x)` and `KW″ū² = u²/(1−x)²` this is eq. (7) of §0. Checks C2 (symbolic identity)
and C2b (direct second difference of the exact Lagrangian, 1.2×10⁻⁷) verify it; C4 verifies the
general-direction form

```
m_T²(n) = u²[ 4(ε²)_ij n^i n^j/(1−x) + (ε_ij n^i n^j)² x/(1−x)² ] + 4a₀²[x+ln(1−x)].   (9)
```

**The two pieces of (6).** The `½W` term is exactly `√g` acting on the background energy density: an
`h²` coupling of the form `¼ρ tr h²`, i.e. what a cosmological constant contributes. A Λ does not give a
graviton a mass: the TT equation on de Sitter is `ḧ + 3Hḣ + (k²/a²)h = 0` with no `h²` term in the
quadratic action — the `¼Λ tr h²` from `√g` is cancelled by the `H²` terms in the second-order expansion
of `√gR`, which is why de Sitter gravitons are massless. The same cancellation applies here because the
gravitational sector of this action is exactly Einstein for TT modes (A3 §3.2: no operator carries two
derivatives of `h^TT`), so the physical mass is the coefficient of the non-universal part
`W(u) − W(ū)`. That is eq. (8). Check C3 verifies the split exactly (`c_hh − c_shape = W/4`). **A direct
verification of the cancellation needs the second-order expansion of `√gR` on the curved background;
this lane does not do it** (§7), and it is the one premise of the headline number that is not proved
here. It does not matter for the verdict: the literal reading differs by a factor < 2 and is also
positive and also 10¹⁰ below the bound.

If one refuses the cancellation, the literal (7) is the answer; it differs by `−4KW ≈ −2u²` and **the
verdict does not move**: C5 verifies that both (7) and (8) are strictly positive on `0 < x < 1`, and the
table of §3 changes only in the second digit.

### 2.3 Sign, and the two limits

* **No tachyon.** `4 − 3x > 0` for every `x < 1` and `(1−x)² > 0`, so (8) is positive for every
  admissible background; the two terms of (9) are each `≥ 0` (first: `|ε·n|² ≥ 0`; second: `x > 0`).
  Check C5 scans `3×10⁵` points on `(0,1)`; the minimum of (8) is at `x → 0` and is `→ 0⁺`, and the
  literal (7) is positive there too. **No tachyon anywhere.**
* **`u → 0`.** `m_T² = 4u² + O(u³/a₀)` (C6), i.e. it vanishes quadratically, and *exactly* at `P̄ = 0`
  (C7): the cosmological background has `m_T = 0` identically. That is A3's background, so **A3's
  `c_T² = 1` is untouched on the background where it was proved.**
* **The cap.** `W″` diverges as `u → a₀`, so the mass grows without bound near the cap: at
  `u = 0.9a₀`, `m_T = 2.1×10⁻³³ eV`; at `u = 0.99a₀`, `2.1×10⁻³² eV`; the graviton bound would be
  reached only at `u/a₀ = 1 − 1.2×10⁻¹¹` (C17). Since `u < a₀` strictly (the cap is where `g → ∞`),
  the divergence is never reached.

### 2.4 The P field relaxes: the mass is a running mass

`W(u)` depends on `P` only through the single combination `u = K|P|`, so the longitudinal part of `δP`
can absorb the `h`-dependence. Writing `P_i = (p+Y)n_i` and eliminating `Y` (which has the mass
`m_Y² = W″ū²/(p²η) = 2/(L*²(1−x)²)` for `η = γ = KL*²/2`, i.e. `m_Y = √2/(L*(1−x))` — the 17.0 pc of
A22 eq. (9), reproduced in C9),

```
m_T²(ω) = [ m_T²(∞) ω² + m_T²(0) m_Y² ] / (ω² + m_Y²),
m_T²(∞) = u²(4−3x)/(1−x)²,   m_T²(0) = u² x/(1−x).                                (10)
```

C8 verifies that at `ω = 0` the `O(u²)` shape term is cancelled and only `−u³/(8a₀(1−x))` survives;
C10/C11 verify (10) to 10⁻¹³ over eight `(x, ω)` points. Since `m_Y = 3.8×10⁻²⁵ eV` (`ω_Y = 5.7×10⁻¹⁰ s⁻¹`)
and LIGO's `ω = 6.3×10² s⁻¹` gives `ω/ω_Y = 1.1×10¹²`, i.e. `ω²/(ω²+m_Y²) = 1 − 8×10⁻²⁵`: **(8) is the
physical mass at every observable frequency** (even a 1 nHz pulsar-timing wave is at `ω/ω_Y = 11`), and (10) only matters in the statement that there is no
mass gap and no tachyonic pole in the deep IR.

## 3. Numbers

`a₀ = 9.36×10⁻¹¹ m s⁻²`, `L* = 24 pc`, `K = 4πG` (K cancels in `m_T²`; it enters only through
`u = K|P̄|`, so the 4πG/8πG convention moves nothing here). `m_T` from (8):
`E_T = ħ u f(x)/c` with `f(x) = x√(4−3x)/(1−x)`.

| regime | `u/a₀` | `m_T` [eV] | `λ_C = ħc/E_T` | | `m_T/m_Y` |
|---|---|---|---|---|
| cosmological (P̄ = 0, no-aether theorem) | 0 | **0 exactly** | ∞ | | 0 |
| galactic, outer | 0.1 | 4.39×10⁻³⁵ | 1.46×10⁶ Mpc (3.3×10² `c/H₀`) | | 1.05×10⁻¹⁰ |
| galactic | 0.3 | 1.55×10⁻³⁴ | 1.37×10⁵ Mpc (31 `c/H₀`) | | 2.9×10⁻¹⁰ |
| galactic (MOND radius) | 0.5 | 3.25×10⁻³⁴ | 3.94×10⁴ Mpc (8.8 `c/H₀`) | | 4.3×10⁻¹⁰ |
| galactic | 0.7 | 6.61×10⁻³⁴ | 1.38×10⁴ Mpc (3.1 `c/H₀`) | | 5.3×10⁻¹⁰ |
| galactic, near the cap | 0.9 | 2.11×10⁻³³ | 3.37×10³ Mpc (0.76 `c/H₀`) | | 5.6×10⁻¹⁰ |

`c/H₀ = 4.45×10³ Mpc`. Asked for in pc and kpc as well: `λ_C = 3.4×10³ Mpc = 3.4×10⁹ pc = 3.4×10⁶ kpc`
at `x = 0.9`, and `1.5×10⁶ Mpc = 1.5×10¹² pc = 1.5×10⁹ kpc` at `x = 0.1` — every entry is in the
Mpc–Gpc range, which is the point. The Compton wavelength is between 0.76 and 327 Hubble radii: **the
tensor mass is a horizon-scale quantity, not a particle-physics one.** Note the direction: `m_T` *increases* with `u`,
so the outer, lowest-acceleration parts of a galaxy have the *smallest* mass.

## 4. Observational consequences, each as a number

**(i) GW dispersion at LIGO/Virgo frequencies.** A mass term leaves `ω² = k² + m_T²`, so the group
velocity is `c(1 − m_T²c⁴/2E²)`. At 100 Hz, `E = ħω = 4.136×10⁻¹³ eV`:

| `u/a₀` | `(c_gw − c)/c` |
|---|---|
| 0.1 | −5.6×10⁻⁴⁵ |
| 0.5 | −3.1×10⁻⁴³ |
| 0.9 | −1.3×10⁻⁴¹ |

against the GW170817 bound `|c_gw/c − 1| < 1×10⁻¹⁵`: **26 orders of magnitude inside it** (C14). The
arrival-time delay over 40 Mpc is `1.3×10⁻³⁴ s`. The *phase* velocity is superluminal by the same
amount, which is the standard Proca behaviour and not a causality statement.

**(ii) Yukawa cutoff.** The mode decays as `exp(−D/λ_C)` over the path where the mass is switched on. It
is switched on only where `P̄ ≠ 0`: by the no-aether theorem the IGM has `P̄ = 0` and `m_T = 0` exactly,
so the physical path is the ~30 kpc through a halo, giving `1 − exp(−D/λ_C) ≤ 8.9×10⁻⁶` at `x = 0.9`
(C15). Even if one (incorrectly) left the mass on over a whole Gpc the suppression would be 26 % at
`x = 0.9` — still far below the ~20 % distance errors of standard sirens, but that configuration does
not exist in this theory.

**(iii) Graviton mass bound.** `m_g < 1.76×10⁻²³ eV` (GW170817 + LIGO): the theory sits **8.3×10⁹**
below it at `u = 0.9a₀` and `4.0×10¹¹` at `u = 0.1a₀` (C16). In `m²` the margin is `7×10¹⁹`.

**(iv) Lensing.** Unchanged, and for a structural reason rather than a numerical one. `W(u)` contains
neither the lapse nor the shift, and the polarization is traceless, so the mass term has **no scalar
projection** and cannot enter the lapse/shift constraints that determine `Φ` and `Ψ` (C18, first two
columns). The P-sector's background stress — hence the exact slip identity `Π = W′u = u²/[K(1−u/a₀)]`
and `Φ − Ψ = O(ε²)` (A3 §2, A12) — is untouched. The mass term's own back-reaction on the lensing
potentials is `(m_T/E)² ρ_gw/ρ_c ≈ 4×10⁻⁴⁷` (C18). The scalar sound speed `c_s² = γ/η` and the
`γ ≤ η` condition are also untouched: no new operator was added, only a new term in the expansion of an
existing one.

## 5. Verdict

**Harmless. The P̄ ≠ 0 background is not excluded; nothing is excluded.**

* The number: `m_T ≤ 2.1×10⁻³³ eV` at `u = 0.9 a₀` (`4.4×10⁻³⁵ eV` at `u = 0.1 a₀`), i.e. **8.3×10⁹
  below the 1.76×10⁻²³ eV bound**, with a Compton wavelength of 3.4×10³–1.5×10⁶ Mpc, a 100 Hz speed
  deficit of `1.3×10⁻⁴¹` against a `10⁻¹⁵` bound, and a Yukawa suppression of `8.9×10⁻⁶` at worst.
* `m_T² > 0` everywhere: **no tachyon, no gradient instability, no ghost.** The mode is massive and
  stable, and massless exactly where A3 proved it so.
* **`c_T² = 1` survives as a speed statement**: `ω² = k² + m_T²` has `d(ω²)/d(k²) = 1` exactly (C12).
  What fails off `P̄ = 0` is only the stronger sentence "the quadratic tensor action *is* the Einstein
  one". The principal symbol is still exactly luminal; the finite-`k` group velocity is
  `c(1 − 1.3×10⁻⁴¹)` at 100 Hz.
* **A31's correction should be recorded with its magnitude.** Its check 28 establishes the right
  qualitative point with the wrong coefficient (`3Kp/8` is `d²u/dh²`); the mass is `u²(4−3x)/(1−x)²`,
  and it is eleven orders of magnitude below every bound. `FINAL_THEORY.md` §3's parenthetical ("a mass,
  not a speed") is correct in kind and now has a number: `≤ 2.1×10⁻³³ eV`.

## 6. Checks (`a39_checks.py`, 21/21 PASS, 5.3 s)

C0 inverse metric exact to `O(h³)`; C1 `u` expansion, reproduces `3Kp/8`; C2 closed form of (7), C2b
finite-difference confirmation; C3 split into Λ-like volume piece and P-specific shape piece; C4 general
direction and polarization, vanishing for `k ‖ P̄`; C5 positivity on `(0,1)`; C6 `u → 0` limit; C7
`m_T(P̄ = 0) = 0` exactly; C8 static `δP` elimination; C9 `m_Y = √2/L*` (17.0 pc, A22); C10–C11 the
running mass (10); C12 `c_T² = 1` and `v_g = 1 − m_T²/2ω²`; C13 mass table; C14 speed deficit vs
GW170817; C15 Yukawa; C16 graviton-mass bound; C17 the `x` at which the bound would be reached; C18
TT-only, lapse-blind, lensing null; C20 A31's coefficient identified as `d²u/dh²`.
Five mutations (§`MUTATE.md`) each break between 1 and 8 checks.

## 7. What this does not do

* It does not solve the P-sector background. `P̄` is taken constant over the wave period
  (`λ_GW ≪ λ_P = 17 pc`); in a real halo `P̄` is a radial hedgehog, so the "mass" is a spatially
  varying, direction-dependent anisotropic mass — a refractive medium, not a Proca mass. The *maximum*
  over directions is what §3–4 quote.
* It assumes the `√g W(ū)` volume piece cancels against the gravitational sector, as a Λ must. The
  alternative (literal) reading is computed alongside and gives the same verdict.
* It does not compute the `O(h³)` back-reaction, the one-loop running, or the waveform from a real
  source. It does not re-derive `η = γ = KL*²/2`; that is A3 §9.1/A22.
* The sign of the effect at `ω → 0` depends on the `δP` kinetic normalisation (`η`); with `η → 0` the
  mass is the frozen (8) at all frequencies. Either way the number is the same to a factor 2.

## 8. Next

1. Put the same expansion on A22's actual radial hedgehog and get the angular pattern of `m_T` for a GW
   crossing a halo at a given impact parameter — a `10⁻⁴⁰`-level birefringence, unobservable but the
   honest statement of the medium's effect.
2. If a future lane wants a *test*, the only handle is the `u → a₀` divergence: a background within
   `10⁻¹¹` of the cap would be excluded by the graviton bound. That is a statement about the cap, not
   about the mass.

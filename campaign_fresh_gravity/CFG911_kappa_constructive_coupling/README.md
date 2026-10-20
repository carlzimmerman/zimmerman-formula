# CFG911: κ constructive lane. ½ ONLY IN MENUS OR POSITS

> **HYPOTHESIS BUILDING, NOT A DERIVATION.** This lane writes down couplings and asks what each would need and what else
> each would predict. Nothing here derives κ. **κ = ½ is FITTED** (CFG493: κ_Λ = 0.417 ± 0.095, κ_crit = 0.345 ± 0.078). Any
> candidate that "gives ½" below is a conjecture with stated tests. It would count as a derivation only if it passed every
> campaign rule, including the look-elsewhere rule, and none does.

**Bottom line.** No coupling in the nine pre-declared candidates selects κ = ½. ½ appears only as a member of a menu or
through a posit, and each time the cost can be named:

- **N0, premise A as the record states it.** The a₀ sector gets its own metric, with gravitational constant G̃ = 3G/(8π), and
  a₀ is taken as the Schwarzschild surface gravity c²/(2R̃) of that metric's horizon. Two things are inserted here. The ratio
  3/(8π) is premise A itself. The factor ½ comes from the Schwarzschild formula used at a horizon that is not Schwarzschild
  (X7). The de Sitter horizon's real surface gravity gives κ = 1.
- **N5, trace share, a₀² = G|T|/N_d.** ½ comes out only for N_d = d², so only because d = 4. This is the X4 class ("where the
  4 lands is a convention"), and the menu {½, 1, 2} makes the ½ spurious.
- **N8, one-sided flux.** The one natural π-free ¼ found is the hemisphere factor of an isotropic flux. It needs a bath of
  quanta with w = +1/3. The DESI w₀ values exclude that at 11–21σ. The Lorentz-invariant vacuum has zero flux, so it would
  give a₀ = 0.

The minimal π-free coupling that is left is premise A written as an action term: S ⊃ λ[a₀² − ξ G F(T_DE)]. It is a **TRADE**,
with κ² = ξ and ξ free, whichever dark-energy stress F it reads. G-normalisation alone therefore does not give ½: it still needs
a 4 from somewhere.

**What the owner gets: falsifiable targets that do not depend on κ.**
- Which stress the portal reads (energy, potential, pressure, trace or active mass) changes a₀(z) under the DESI DR2 dark energy
  by 0.13–0.25 dex at z = 2.
- The density portal obeys a running law: d ln a₀/d ln a = −(3/2)(1 + w).
- The kinetic portal predicts a strong decline into the past. It is excluded if DESI's phantom crossing is confirmed.
- Making a₀ a dynamical field is silent locally (≤ 4e-11 of a₀ in any system).

Outcome as frozen (§7): **½ ONLY IN MENUS OR POSITS.** Footings never pooled. No de Sitter–Unruh argument. No dark-matter
species. Not theory closed.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (1ff4510ee): hypotheses, the N0–N8 family with variants, grading, data thresholds, checks, MUTATE, hand expectations |
| `cfg911.py` | sympy + numpy, one process, about 1 s, about 120 MB |
| `cfg911.out`, `cfg911_results.json` | normal run: 26/27 checks PASS; the one FAIL is K9, failing as frozen because the frozen expectation was wrong (disclosed below); exit 0 |
| `cfg911_MUTATE.out`, `cfg911_results_MUTATE.json` | `CFG911_MUTATE=1`: M1–M4 all bite, exit 1 by design |

Run from the repo root:

    OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG911_kappa_constructive_coupling/cfg911.py > campaign_fresh_gravity/CFG911_kappa_constructive_coupling/cfg911.out 2>&1
    CFG911_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG911_kappa_constructive_coupling/cfg911.py > campaign_fresh_gravity/CFG911_kappa_constructive_coupling/cfg911_MUTATE.out 2>&1

The script reads three tracked files, read-only:
- `fable_independent_2026/L273_desi_a0z_band.py`: the DESI DR2 w₀w_a fits, the L275 correlations and Ω_m.
- `fable_independent_2026/L273_desi_a0z_band.out`: the cross-checks K9b and K9c.
- `campaign_fresh_gravity/CFG829_lensing_low_g_vs_dwarf_excess/cfg829_results.json`: the KiDS blue-lens amplitudes.

Nothing was downloaded. LEDGER.md, the THEORY_CANONICAL files, CFG894's register and the other lanes were not edited.

## Two structural facts the family is built on (both checked in sympy)

1. **In energy units the law has no explicit c:** a₀ = κ c√(Gρ_DE) = κ√(G ε_DE). A "c-coupling" therefore means the a₀ sector
   reads the dark energy's **stress** (energy density, pressure, trace or flux), not its mass density. That is how c enters
   without a horizon. K15 confirms that {a₀, ε or ρ, c} have no dimensionless group, so a G-free tie needs a new dimensional
   constant (N3).
2. **κ² ∝ G¹, and every Gauss-law normalisation of G carries one π.** This covers Poisson's 4πG, Einstein's 8πG and the
   record's K = 4πG, which is forced by ∇·P = ρ − ρ̄. κ² is therefore π-free only in two cases:
   - G enters bare (premise A, here hypothesis H_A);
   - a geometric 1/π cancels the π.
   The record's own K becomes π-free only when divided by a full solid angle, i.e. for a per-steradian quantity. N8(b),
   a₀² = K·I/c, is π-free without premise A, but it gives κ = 1 and needs a bath that carries flux.

## The family and the grades (frozen §5; `cfg911.out` §A and §G)

| id | coupling (hypothesis) | why π-free | κ² (variants) | free | grade |
|---|---|---|---|---|---|
| N0 | second metric g̃ with G̃; a₀ = surface gravity of its horizon | premise A sets G̃/G = 3/(8π) | (2π/3)G̃/G (Schwarzschild form), (8π/3)G̃/G (de Sitter form); at premise A {¼, 1}; at G̃ = G {2π/3, 8π/3}, which are π-odd | G̃/G | **TRADE** (and X7 for the ½) |
| N1 | λ[a₀² − ξGε] (premise A as an action term; record K532) | G bare | ξ | ξ | **TRADE** |
| N2 | λ[a₀² − ξGF], F ∈ {(ε−p)/2, −p, (ε+p)/2, ε−3p, −(ε+3p)} | G bare | ξ·{1, 1, 0, 4, 2} at w = −1; report-only ξ = 1 gives κ {1, 1, –, 2, √2} | ξ | **TRADE** (×5; the kinetic one is sign-limited, see below) |
| N3 | a₀ from ε and c only | no G | none (no dimensionless group). (a) field scale 1/√V″: 8πλ²n² (Einstein-normalised, π-odd) or λ²n² (G-normalised); (b) ħ length (ħc/ε)^{1/4}; (c) horizon c/H: 8πn²/3 | λ, n | **TRADE**; (b) and (c) EXCLUDED: (b) is ħ-bearing and 5.4 × 10³⁰ × the law's unit; (c) is H-type and π-odd |
| N4 | ε_DE = sF², a₀ = √G·F (one G-normalised field) | G bare | 1/s: s = ½ → 2, s = 1 → 1 | – | **MENU** {√2, 1}, both misses |
| N5 | a₀² = G\|T\|/N_d | G bare | (1 − (d−1)w)/N_d: N_d = d², d, 1 → {¼, 1, 4} | – | **EXCLUDED** (X4) + MENU; the ½ is spurious |
| N6 | N1/N2 with φ dynamical (canonical quintessence) | G bare | ξ | ξ, λ | **TRADE**, locally silent |
| N7 | a₀ = n c²/√A_Λ (record K433, cross-check) | √A carries √(4π) | 2n²/3, so n = 1 gives κ = 0.8165; ½ needs n = √6/4 (K11 reproduces K433) | – | **MISS** |
| N8 | an isotropic bath read by its flux: (a) GΦ₁/c, (b) K·I/c, (b′) KΦ₁/(cΩ/2), (c) KΦ₁/c | hemisphere ¼, per-steradian 1/4π | (a) ¼, (b) 1, (b′) ½, (c) π (π-odd) | – | **EXCLUDED** (w = +1/3) + MENU; the ½ is spurious |

- **Rename test (I4).** At κ_law = 2/5:
  - every ξ portal follows the law, so each is a consistency relation;
  - N4, N5, N7 and N8 do not move, so each outputs its own numbers and fails the comparison with 2/5;
  - N0's output is undefined until G̃/G is fixed.
- **π-weights (I8).** They match the frozen classes.
- **ρ_crit readings (report only).** N4 1.170/0.828; N5 0.414/0.828/1.655; N7 0.676; N8 0.414/0.828/0.585/1.467.

## Second predictions, with numbers (κ-free; `cfg911.out` §D–F)

### 1. Which stress the portal reads changes a₀(z)

a₀(z)/a₀(0) = √(F(z)/F(0)), evaluated under the three DESI DR2 CPL fits. The table gives log₁₀ values in dex, listed as
DESY5 / Pantheon+ / Union3.

| z | ε (canonical S1 reading) | V = (ε−p)/2 (record R16) | −p (stage-17) | trace | active mass | rival a₀ ∝ H(z) |
|---|---|---|---|---|---|---|
| 1.06 | +0.000 / −0.008 / +0.009 | +0.049 / +0.027 / +0.072 | +0.101 / +0.062 / +0.141 | +0.074 / +0.045 / +0.106 | +0.157 / +0.099 / +0.223 | +0.270 / +0.265 / +0.276 |
| 1.42 | −0.024 / −0.027 / −0.019 | +0.031 / +0.013 / +0.051 | +0.088 / +0.052 / +0.127 | +0.059 / +0.032 / +0.088 | +0.148 / +0.091 / +0.213 | +0.355 / +0.350 / +0.360 |
| 2.0 | −0.065 / −0.059 / −0.068 | −0.003 / −0.014 / +0.010 | +0.059 / +0.029 / +0.092 | +0.028 / +0.007 / +0.050 | +0.123 / +0.071 / +0.183 | +0.480 / +0.476 / +0.485 |
| 2.5 | −0.099 / −0.085 / −0.111 | −0.034 / −0.038 / −0.027 | +0.030 / +0.007 / +0.057 | −0.002 / −0.016 / +0.014 | +0.097 / +0.052 / +0.151 | +0.575 / +0.570 / +0.580 |

- **The record already uses three of these readings as if they were the same law.** They are the ε reading (canonical S1,
  PAPER7), the −p reading (stage-17, L273 Part 4) and the V reading (R16). Under DESI the ε and −p readings differ by 0.09–0.17 dex at z = 2.5.
  - K9b reproduces L273's density row exactly.
  - K9c reproduces L273's pressure-law row exactly.
- **The differences are robust to the DESI uncertainty.** With 68% bands (Gaussian in w₀ and w_a, using the L275 correlations),
  every portal minus ε stays positive at z = 2: V +0.03…+0.10, −p +0.06…+0.21, trace +0.04…+0.15, active +0.09…+0.34.
- **This is not testable now** (frozen §6).
  - The spread at z = 1.06 is 0.11–0.21 dex, below the record's honest band of ±0.272 (Jeanneau deep refit). Mapped to Δb, the
    portals sit 0.5–1.3σ from that refit.
  - Splitting the extreme portals at 3σ needs σ(log a₀) ≤ 0.043 dex, about 10%, at z = 2.
  - The sealed ALMA programme (2026-11-06, 2026-11-28) encodes only the flat and ε-tracking branches. The other portals are
    not sealed. Testing them against that release would require sealing them before the data come out, which is the owner's
    call; this lane seals nothing.
- **One near-degeneracy.** At z ≈ 1, the active-mass portal under Union3 (+0.223) sits close to the a₀ ∝ H(z) rival (+0.276).
  The two separate by z = 2.5 (+0.151 against +0.580).

### 2. The a₀–w running law

The density portal gives d ln a₀/d ln a = −(3/2)(1 + w) exactly (K17). So a₀ grows with cosmic time only while the dark energy
is phantom. The other portals add a w_a term.

Today's values, in units of H₀ (DESY5 / Pantheon+ / Union3):

| portal | d ln a₀/d ln a today |
|---|---|
| ε | −0.37 / −0.24 / −0.50 |
| V | −0.62 / −0.41 / −0.83 |
| −p | −0.94 / −0.61 / −1.32 |
| trace | −0.77 / −0.51 / −1.04 |
| active | −1.40 / −0.86 / −2.13 |
| kinetic | +1.36 / +1.67 / +1.14 |

The local drift this implies, a few × 10⁻¹¹ per year, cannot be measured directly. The law is tested through a₀(z).

### 3. The kinetic portal, F = (ε + p)/2

- **For a true Λ (w = −1):** a₀ = 0. This form cannot carry the flat branch.
- **Under DESI's CPL fits:** a₀ → 0 at the phantom crossing, z_c = 0.405 / 0.354 / 0.440, and it is undefined beyond.
- **A canonical scalar cannot cross w = −1.** The representative non-crossing variant is thawing quintessence,
  1 + w = (1 + w₀)a³. It gives a₀ roughly ∝ a^{3/2}:
  - z = 1.06: −0.41 to −0.44 dex, so Δb ≈ +0.38 to +0.41 against the refit's +0.140 ± 0.272 (0.9–1.0σ);
  - KiDS lenses at z_l = 0.25: A = 0.86–0.88, against CFG829's 1.016 ± 0.086 (1.6–1.8σ low, canonical footing) and
    0.928 ± 0.078 (0.6–0.8σ low, alt footing).
- **Verdict under the frozen rule:** not excluded by data, so it is graded TRADE. It becomes excluded if DESI DR3 or Euclid
  confirm the crossing.
- **Data that would decide it:**
  - a lens-redshift split of the galaxy–galaxy lensing RAR (CFG255 found KiDS-1000 underpowered, so KiDS-Legacy or Euclid);
  - the Jeanneau deep subsample with direct gas masses (band about 0.15 dex).

### 4. N6: a dynamical a₀ is locally silent

- **The source.** The galaxy's own field sources φ with the "a₀-charge" q = −a₀∂W_rem/∂a₀|_u. Its limits are g³/(3Ka₀) in the
  deep regime and a₀g/K in the Newtonian regime (K19, K19b).
- **The induced variation,** δ ln a₀ = (Gλ²/2c⁴)∫q/|x − x′| d³x′:

  | system | δ ln a₀ |
  |---|---|
  | Sun, at 1 AU | 7.3e-24 λ² |
  | MW-like galaxy (6e10 M_⊙), at 8 kpc | 4.6e-14 λ² |
  | cluster (1e14 M_⊙), at 1 Mpc | 3.6e-11 λ² |
  | Earth, at its surface | 3.0e-29 λ² |

  The scale of each value is λ² G M a₀/c⁴.
- **The equivalence principle.** The coupling ignores composition, so MICROSCOPE-type tests see nothing.
- **The cosmic back-reaction on the dark energy's slope** is about 3e-8. It is uncertain by a log factor because the
  deep-regime charge grows as (1/3) ln(R_out/r_M).
- **Reading.** There is no fifth-force, equivalence-principle or environment target. The coupling agrees with the record's
  environment slope (−0.010 ± 0.015) and with Cassini, because the local sector is the unchanged stiffened action.

### 5. N8 and N0

- **N8.** The bath needs w = v²/3c² ≥ 0, which is +1/3 at v = c. That lies 19.0 / 21.3 / 11.4σ above the DESI w₀ values, so N8
  is EXCLUDED.
- **N0.** It predicts a horizon in the a₀ sector's metric at R* = c/√(Gρ_Λ) = 15.6 Gpc (the Hubble radius is 4.45 Gpc). GR has
  no horizon there (k05 H1), and no data reach it.

## Checks and MUTATE

**Normal run: 26 of 27 checks pass.**
- K1 (I1): no forbidden literal in the script.
- K2 (I2): 19 symbolic variants.
- K3 (I3): scaling.
- K4 (I4): rename.
- K5 (I5): N0 and N7 hold for every ρ, so each is a posit, not a selection.
- K6 (I6): ρ_crit values printed separately.
- K7 (I7): no ħ.
- K8 and K8b (I8): π-weights.
- K10: CFG829 values.
- K11: K433's √6/4.
- K12: W_rem gives the canonical K W′ = u²/(a₀ − u) and the simple law.
- K13: the hemisphere fraction (¼ for n = 3, 1/π for n = 2).
- K14: classifier controls.
- K4b: k04 consistency.
- K15–K21, all added beyond the frozen K1–K14 list: dimensional null spaces; N3; the running law; portal testability;
  q-limits; N6 silence; N8 exclusion.
- K0, K9b, K9c and K19b: provenance and stability checks.

**MUTATE (`CFG911_MUTATE=1`, exit 1): every control bites.**
- **M1 (8πG → 4πG).** N7's κ² goes 2/3 → 1/3 and N0's natural values halve. The G-bare portals do not move, as designed.
- **M2 (w = −1 → −0.9).** The ξ = 1 menu moves to 0.95 / 0.9 / 0.05 / 3.7 / 1.7. N5 moves to 37/160. N8 does not move.
- **M3 (d = 5).** N5 → 1/5. N7 becomes π^{−1/3}. N8(a) becomes 2/(3π). N4 does not move.
- **M4 (planted ξ := a₀_law²/(Gε), labelled "derived").** It is classed IDENTITY: it follows κ_law to 0.4.

## Disclosures

1. **K9 fails as frozen, because the frozen expectation was wrong.**
   - The frozen text asked for "0.82 at z = 2.5 (DESY5) within 0.01". 0.82 is PAPER7's rounded point value, and it equals the
     Pantheon+ pair (10^−0.085 = 0.822).
   - L273's own check of "DESY5 = 0.82" used a 0.03 tolerance, and its table prints 0.796 for DESY5.
   - The check is kept as frozen and counted as a FAIL. K9b and K9c, added after the freeze, reproduce L273's printed density
     and pressure rows to within 0.0015 dex.
   - The normal run's exit code ignores failures that are flagged as disclosed expectation errors. There is one: K9.
2. **Two development runs went to the scratchpad before the recorded run.** They found:
   - K3 returned NaN for the zero-κ² kinetic row; zero rows are now skipped.
   - The lambdified q-function overflowed to −inf, and K20 wrongly passed on −inf. It was replaced by a stable hand form,
     checked symbolically (K19b), and K20 now requires finite positive values.
   - Spurious BLAS floating-point flags appeared in `multivariate_normal`, as in L273. They are suppressed, and the samples are
     asserted finite.
   - After the recorded run, K9c and a print note on the log-dependence of the back-reaction were added, and both modes were
     rerun. All numbers are identical.
3. **One reading of the frozen grading.** N3's variants are alternative constructions. The candidate's grade is that of its
   least severe surviving variant: TRADE for (a)/(a′). Variants (b) and (c) are EXCLUDED and listed.
4. **Hand expectations against the script.**
   - Thawing kinetic portal: KiDS 1.6–1.8σ / 0.6–0.8σ (hand: about 2σ / 1σ); z = 1.06 at −0.41…−0.44 dex (hand: −0.47, which
     neglected the ε factor).
   - Everything else agrees with the frozen §10.
5. **Approximations.**
   - The Jeanneau Δb mapping uses D = 0.243/log₁₀E(1.06) = 0.927, calibrated on the record's own ALT fork, so it is
     approximate.
   - N6 uses point masses and an O(1) slope λ.
   - The thawing form is leading-order in the matter era.
   - Measured w₀/w_a enter only the second predictions, never κ.
6. **Not run here: p63 (pending).** It covers the four-form and a₀-as-field doors. N4 only checks consistency with k04's
   formula.

## What this means for the κ campaign

- **"The new π-free coupling" is premise A.** As an action term it is a TRADE (κ² = ξ). G-normalisation removes the π but
  not the 4.
- **Every route to an exact ½ found here takes the 4 from one of three places,** each already excluded:
  - a counting of d = 4 (X4);
  - the Schwarzschild form at a non-Schwarzschild horizon (X7);
  - the hemisphere flux of a bath that cannot be dark energy (w = +1/3, excluded at ≥ 11σ).
- **The productive output is the κ-free shape tests (the portal invariant and the running law).** They test the coupling class
  whatever κ is, but they need σ(a₀) at the 10% level at z ≈ 2. That is the same data-side unlock the campaign already lists.
- **Look-elsewhere.** No determinate trial is added (MENU, TRADE and EXCLUDED rows only), so P_LEE is unchanged.

## Proposed register line (not appended by this lane; next free id after K601)

`K602,CFG911,FN,campaign_fresh_gravity/CFG911_kappa_constructive_coupling,"constructive pi-free portals of a dynamical rho_DE (premise A as bimetric horizon / multiplier xi G F[T_DE] for F = eps, V, -p, X, trace, active; G-free tie; canonical field strength; trace share; dynamical quintessence; areal K433; hemispherical flux)",,0.5;1;2;1.414;0.816;0.707;1.772,menu,1,"1/2 ONLY IN MENUS OR POSITS: multiplier portals TRADE (kappa^2 = xi); N0 needs Gtilde/G = 3/8pi + Schwarzschild 1/2 (X7); N5 trace share 1/d (X4); N8 hemisphere 1/4 needs w = +1/3 (excluded 11-21 sigma); N4 menu sqrt2/1; N7 0.816; kappa-free targets: portal a0(z) spread 0.13-0.25 dex at z = 2, running dln a0/dln a = -(3/2)(1+w), kinetic portal excluded if DESI crossing confirmed; N6 locally silent",<this commit>`

κ fitted; not theory closed.

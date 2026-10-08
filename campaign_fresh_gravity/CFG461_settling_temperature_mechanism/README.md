# CFG461: what sets the cold fluid's temperature, σ⁴ = G M_b a₀/4? NO CLASS PASSES

The criteria (`FROZEN_CRITERIA.md`) were committed alone first, in d29266e07. The script is `cfg461_temperature.py` and runs in about 8 s.
- Main run: exit 0, because the controls K1–K4 pass.
- `CFG461_MUTATE=1` (a₀ → 2a₀, and the baryon dependence dropped inside every mechanism): every class and R0 fail G-b. Exit 1, as designed.

κ = ½ is FITTED. Both footings are scored separately. No dark-matter particle is added: the cold fluid's mass is still required, and its amount (Ω_c/Ω_b = 5.364) is an input. This is not "theory closed".

## The question

T13 and CFG472 established that the deep phantom is a singular isothermal sphere (SIS) with σ² = V_f²/2. So "settling" in PAPER45 v2's growth fix comes down to one number per galaxy: what sets the cold fluid's velocity dispersion to σ⁴ = G M_b a₀/4 inside r_edge? The answer must:
- conserve mass;
- respect G9;
- add no constant beyond κ.

## Verdict table (class × gate)

The G-b parts are: σ is an output / the state is an SIS / the amplitude is within 0.1 dex / the scaling (d ln σ⁴/d ln M_b and d ln σ⁴/d ln c) is 1 ± 0.1. A "--" means not scorable.

| class | G-a mass | G-b [out/SIS/amp/scal] | G-c κ only | G-d G9 | G-e | result |
|---|---|---|---|---|---|---|
| C1a Lynden-Bell, Newtonian, E from collapse | PASS | **FAIL** [Y/Y/n/n] | PASS | PASS | PASS | FAIL |
| C1b LB entropy maximum in a box (no baryons) | PASS | **FAIL** [n/n/n/n] | PASS | PASS | PASS | FAIL |
| C2a T10 μ-heat flow, conserved mass, cosmological box | PASS | **FAIL** [Y/Y/n/n] | FAIL (drift = target shape) | PASS | PASS | FAIL |
| C2b law's action (AQUAL/QUMOND) on all real mass + entropy | PASS | **FAIL** [Y/n/n/Y] | PASS | PASS | FAIL (acts on all mass) | FAIL |
| C2c mismatch functional ∫\|g_N[b+c] − g_law[b]\|² | PASS* | FAIL [Y/Y/n/n] | **FAIL** (g_law inserted) | PASS | -- | FAIL |
| C2d tracer in the law's field + Newtonian self-gravity | PASS | **FAIL** [n/n/n/n] | PASS | PASS | -- | FAIL |
| C3a Unruh / de Sitter bath at a₀ | PASS | **FAIL** [Y/n/n/n] | FAIL (particle mass) | PASS | FAIL (everywhere) | FAIL |
| C3b vacuum stress boundary P = a₀²/8πG | PASS | **FAIL** [n/Y/n/n] | PASS | PASS | -- | FAIL |
| C4 cosmological virialisation, z_c = 0 / 1 / 3 | PASS | **FAIL** [Y/Y/n/n] | PASS | PASS | PASS | FAIL |
| C5 Jeans marginality | PASS | **FAIL** [n/Y/n/n] | PASS | PASS | -- | FAIL |
| C6 phonon coupling (Berezhiani–Khoury, fork arm a) | -- | not computed | FAIL | **FAIL** | -- | FAIL by construction |
| R0 RESTATEMENT (control): cosmic share, uniform μ inside the law's r_edge | PASS | [n/Y/**Y/Y**] | FAIL (r_edge is the law's) | PASS | PASS | control: the gate can pass |

\* G-a holds for C2c only if the supply equals M_ph(<r_edge).

## The numbers (dex of σ⁴/σ_t⁴ for M_b = 1e9 / 10^10.5 / 10^11.5; canonical footing, alt in the .out)

| class | dex | d ln σ⁴/d ln M_b | d ln σ⁴/d ln c |
|---|---|---|---|
| C1a = C4, z_c = 1 | −1.02, −0.52, −0.18 | 1.333 | 0 |
| C2a, box r₂₀₀(z = 0) | −1.41, −0.91, −0.57 | 1.333 | 0 |
| C4, z_c = 0 | −1.62, −1.12, −0.78 | 1.333 | 0 |
| C4, z_c = 3 | −0.41, **+0.09**, +0.42 | 1.333 | 0 |
| C2b, a = r_M | +0.22 (all three) | 1.000 | 1.000 |
| C3a, best-case m tuned to the middle galaxy | +1.50, 0.00, −1.00 | 0 | 0 |
| R0 (b + c inside r_edge) | +0.073 (all three) | 1.000 | 1.000 |
| R0, cold-only | −0.075 (all three) | 1.000 | 1.000 |

**Coincidence caught.** C4 at z_c = 3 hits the middle galaxy (+0.09 canonical, +0.005 alt), but it misses the ends by ±0.4 dex and its c-exponent is 0. The scaling part of G-b is what catches it.

## What was found

**1. The c-test: no c-free mechanism can set the temperature.** The target is σ⁴ = G M_b κc√(Gρ_Λ)/4, which is linear in c. Put differently, σ⁴/(G M_b √(Gρ_Λ)) must equal one universal velocity, κc/4 = 37,474 km/s, in every galaxy.

Every mechanism built from Newtonian gravity plus Λ is c-independent, so it has d ln σ⁴/d ln c = 0. That covers violent relaxation, max-entropy states, heat flow in a box, cosmological virialisation and Jeans marginality. So none of them can set the amplitude, whatever its energy or radius bookkeeping.

The Unruh bath fails the same way: σ² = ħa₀/(2πcm) = ħκ√(Gρ_Λ)/(2πm), so c cancels. It also gives one σ for every galaxy. The particle mass it needs runs from 1.7e-27 to 9.4e-29 eV (a 1.25 dex spread), so no single m works.

This is CFG264's Buckingham result (c-free principles cannot fix c-carrying coefficients) applied to the settling temperature. **A G9 mechanism must carry c (that is, a₀) at O(1) on galaxy scales.**

**2. Max entropy does not pick the SIS (C1b, K2).**
- The Emden spiral reproduces Antonov's limit: λ_min = −0.3346 at a density contrast of 708.6.
- At the truncated SIS's own energy, λ = −¼, a cored state (contrast 66) has higher entropy than the SIS: 3.792 against 3.748.
- So, in agreement with Lynden-Bell & Wood (1968), the SIS is the unstable centre of the spiral and not a maximum. This is for the self-gravitating case with no baryons, in a box.

**3. The law applied to all mass is the only c-carrying class that selects σ, and it selects the wrong state (C2b).**
- K3 checks the deep-MOND isothermal sphere: σ⁴ = (4/81) G M a₀ exactly (Milgrom's virial relation).
- With baryons, ν_mono and the cosmic share:
  - σ⁴/σ_t⁴ is +0.19 to +0.29 dex;
  - the slope at 2–5 r_M runs from −1.4 to −3.1, so the state is not an SIS;
  - the far slope is −3.6 to −4.0, so the mass is finite.
- It also double-counts (the record's A12 additive exclusion), and it acts on all cosmic mass, which brings back the growth excess.

**4. The others are restatements or leave σ free.**
- C2c's minimiser is ρ_ph only because g_law is written into the functional.
- C2d: a self-gravitating tracer has no SIS; a non-self-gravitating tracer has slope −V_f²/σ², with σ free.
- C3b: P_edge = a₀²/8πG gives σ⁴ = G M_SIS(<r_cap) a₀/4 for every σ. It turns the BTFR into "the SIS mass inside the a₀-radius equals M_b"; it does not supply that.
- C5: λ_J² = 2π²r² for every σ.

## The single most promising lead, and its exact gap

**The temperature problem is equivalent to an edge condition.**
- A conserved cold fluid that relaxes to the uniform-μ (SIS) state has amplitude μ = M(<R)/(4πR), which is fixed by where the settled region ends.
- With the cosmic share inside, σ⁴ = G M_b a₀/4 holds exactly when the edge sits where the law's boost equals the cosmic matter-to-baryon ratio: ν(g_N/a₀) = Ω_m/Ω_b = 1/f_b.
- That is g_N = ln²(1/(1−f_b)) a₀ = 0.029 a₀, i.e. r_edge = 5.85 r_M, CFG424's edge. The deep form is g_N = f_b² a₀.
- R0 reproduces the target to +0.073 dex (−0.075 for the cold fluid alone), with both exponents exactly 1. MUTATE breaks it (+0.37 dex at the middle galaxy, and the M_b slope goes to 0).

**Why it is not yet a mechanism.** The edge criterion is c-carrying because it contains a₀. That makes it the right kind of object, but here it is read off the law, so it fails G-c. Cosmological boxes (r₂₀₀, or (5/12) R_ta from energy-conserving collapse) scale as M^⅓ and give the ΛCDM-like slope σ⁴ ∝ M^{4/3}.

**Exact remaining gap:**
1. A G9-respecting dynamics that makes settling stop (a no-flux boundary) where the local total field falls to ν(y_e) y_e a₀ ≈ 0.19 a₀ (equivalently g_N ≈ 0.029 a₀), with no new constant. The record's zero-constant carrier of the local total field is the khronon lapse (CFG373 G1). Nothing on the record supplies the boundary dynamics.
2. An energy sink. Post-freeze report (not a verdict input): the virialised fluid must contract from R_vir to r_edge. The factor R_vir/r_edge is 3.5 / 2.0 / 1.3 at z_c = 1 (canonical) for the three masses; at z_c = 3 the massive end needs to expand (0.67). So a gravity-only, collisionless fluid must shed up to a few times its virial binding energy, in a mass-dependent way. The record's sink is the khronon K² channel, which needs CFG381's +1 fluid–khronon coupling.

So the lead costs one constant unless the boundary and the sink come from the same c-carrying field with a derived coupling. That is the open target.

## Controls

- K1 (sympy) PASS: the SIS identities, E = −GM²/(4R), and λ_J² = 2π²r².
- K2 PASS: Antonov −0.3346 at contrast 708.6; the spiral tail is −0.2555 at ξ = 2000 against −¼.
- K3 PASS: 0.04938 against 4/81.
- K4 PASS: R0 meets G-b parts 2–4.

## Disclosures

These changes were made after the first output. None of them moves a verdict.
- One C2b row (a = 0.3 r_M, ρ₀ = 1e-3) was a spurious root at the α → 3 pole of the tail correction (tail fraction 1.0, far slope exactly −3.00). A validity check now rejects it and prints the rejection.
- G-e for C2c, C2d, C3b and C5 was changed from FAIL to "not scorable", because they are static statements with no timescale.
- C2a's "σ is an output" flag was set to Y (the cosmological box is an output) before the first complete run.
- The contraction factors are a labelled post-freeze report.

## Caveats

- Everything is spherical and static. Newtonian dynamics is used except where the law enters.
- C4 is a toy: an Einstein–de Sitter turnaround of a uniform sphere, one component, M_tot = M_b/f_b. The cosmological background is fixed (H₀ = 67.4, Ω_m = 0.315) across both footings.
- C2b uses Hernquist baryons at a = 0.3 and 1 r_M only, and its physical numbers use the median Q of the a = 1 runs.
- C1b has no baryons.
- C3a's m is a declared best case.
- C6 was not computed.
- The kernel is the record's ν_mono (FP1). The edge uses its exponential closed form (they agree to 3e-9 at y = 0.03).
- The c-test treats a₀ = κc√(Gρ_Λ) as the framework states. Under a reading where a₀ is a fundamental constant, the test becomes the a₀-scaling test, which gives the same verdicts (MUTATE).

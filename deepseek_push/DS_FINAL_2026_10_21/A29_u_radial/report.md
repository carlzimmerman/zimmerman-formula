# A29 — the radial structure of u(r): why 0.472 inside and 0.986 outside

## Claim

**u is not a gradient. It sits at 0.29–0.53 out to 1.18 Mpc and then jumps to 1, in the gap between
1.18 and 1.71 Mpc.** Inverting the eight CFG687 radial bins one at a time (new in this lane; A21
only did the three bands) gives u = 0.294 ± 0.125, 0.373 ± 0.107, 0.333 ± 0.050, 0.417 ± 0.065,
0.412 ± 0.044, 0.532 ± 0.054, **1.088 ± 0.209, 0.939 ± 0.106** at R = 0.18 … 2.49 Mpc. A single u
is rejected at χ²/dof = 5.92; a step (u_in, u_out and r_t fitted; bins 0–5 | 6–7) fits at 1.75 and must place the
discontinuity in the gap 1.176–1.711 Mpc. In equation-of-state language (`u = 1+3⟨w⟩`, exact, §1)
the three bands give

| band | range (Mpc) | u | ⟨w⟩ |
|---|---|---|---|
| INNER | 0.150–0.461 | 0.3348 ± 0.0563 | −0.2217 ± 0.0188 |
| MID | 0.461–1.417 | 0.4716 ± 0.0361 | −0.1761 ± 0.0120 |
| OUTER | 1.417–3.0 | 0.9865 ± 0.0984 | −0.0045 ± 0.0328 |

so the inner medium is under **tension** at 12σ from dust and the outer medium **is dust** (0.14σ
from w = 0).

Of the three mechanisms, **(i) relaxation is excluded on the sign of its density scaling** — the
inner medium relaxes 94× faster, so it would become dust *first*; forcing any normalisation makes
u_INNER = 1, excluded at 11.8σ. **(ii) phase space is excluded** — u = 1/2 ⇔ β = 1/2 ⇔ r = r_a, but
the one NFW-motivated choice r_a = r_s = 0.229 Mpc is 4.6× inside the measured crossing
(1.065 Mpc), no single β(r) fits the eight bins (χ²/dof = 4.25 against 1.75, Δχ² = 16.7), and both
normalisations miss by 4.3σ and 11.0σ. **(iii) the splashback boundary survives**:
r_sp = 0.83 r200m = **1.37 r200c = 1.41 Mpc** for the stack (1.31–1.63 across three mass routes),
which is **0.3% from the model-independent caustic at 1.42 Mpc** (steepest
d ln(excess)/d ln R = −2.24) and lies inside the u-step interval, and it predicts the observed mass
ordering of u_OUTER (1.90 → 1.04 → 0.68) with no free parameter beyond the M500–M_gas conversion.

**The asymmetry is the result.** u = 1 outside is *forced by construction*: beyond r_sp the material
has never crossed the shock, is single-stream, has zero velocity dispersion in its own rest frame,
hence w = 0 and u = 1 exactly — and the data give 0.9865 ± 0.0984, 0.14σ away. u = 0.47 inside is
**not derived**: it needs tension (w < 0), which no velocity distribution can supply (any dispersion
gives p ≥ 0, hence u ≥ 1). The inner amplitude is the equation of state of the shocked phase and
remains the A21 premise (P1).

## Derivation

Units c = 1, G = 6.67430e-11, a0 = 9.36e-11 m/s², H0 = 67.4 km/s/Mpc, Ω_m = 0.315, Ω_Λ = 0.685
(enters only through ρ_crit(z)), M_☉ = 1.98847e30, Mpc = 3.0857e22 m. The stack: 318 eRASS1 × KiDS
clusters, median z = 0.2336, median M_gas,500 = 1.1608e13 M_☉, median R500 = 0.7845 Mpc, binned on
the CFG686/687 grid `logspace(0.15, 3.0, 9)` → centres 0.18 … 2.49 Mpc.

**1. The inversion, per bin.** With `P_l` the canonical law's ΔΣ (baryons + phantom, `a0` on), `P_N`
the same model with `a0 = 0` (baryons only) and `D` the measured ΔΣ,

    u(r) = (P_l − P_N)/(D − P_N),   u_band = Σ_j w_j(P_l−P_N)_j / Σ_j w_j(D−P_N)_j,           (1)

which is exactly A21's `u = (A_n−A_l)/(A_l(A_n−1))`, since `A_l = ΣwD/ΣwP_l` and `A_n = ΣwD/ΣwP_N`.
K1: the npz reproduces CFG687's six published band amplitudes to 3.5e-8 relative. K2: MID 0.47157
and OUTER 0.98647 reproduce A21's 0.4716 / 0.9865 to 1e-3, and the INNER band gives
**0.3348 ± 0.0563**, a number A21 never computed.

**2. The equation of state is exact, not fitted.** For `T^μ_ν = ρu^μu_ν + p h^μ_ν` in the static
frame, `T^0_0 = −ρ`, `T^i_i = 3p`, so `T_00 − ½g_00T = (ρ+3p)/2` and

    ∇²Φ = 4πG(ρ+3p),   M_g(<r) = M_c + 3∫p dV,   u = M_g/M_c = 1 + 3⟨w⟩,                      (2)

with `⟨w⟩ ≡ ∫p dV/∫ρ dV` volume-weighted (K5, exact in sympy). Hence

    ⟨w⟩ = (u−1)/3,   σ_⟨w⟩ = σ_u/3,   u = 1/2 ⇔ ⟨w⟩ = −1/6 exactly.                            (3)

K4: `du/dA_l = −0.3039` reproduces σ_u = 0.0361 (A21: 0.03625) and σ_⟨w⟩ = 0.0120. K6: the chain
⟨w⟩ → u → `A_l = A_n/(1+u(A_n−1))` returns the measured amplitude in all three bands with **zero**
residual — algebra, not a fit. K7: MID sits 0.79σ from ⟨w⟩ = −1/6, OUTER 0.14σ from ⟨w⟩ = 0.

**3. The profile is a step.** K8: constant u gives χ²/dof = 5.92 (u = 0.447). K9: u(1.71) − u(1.18)
= +0.557, 2.58σ. K10: a step (three parameters) fits at χ²/dof = 1.75 with u_in = 0.412, u_out = 0.970,
splitting the bins 0–5 | 6–7; r_t cannot be placed inside a bin, so the discontinuity is localised
only to **(1.176, 1.711) Mpc**. K11: splitting OUTER at 2.06 Mpc gives 1.088 ± 0.209 and
0.939 ± 0.106 — both 1σ from 1 and 0.7σ from each other: **no residual structure outside the
transition**. The inner six bins are *not* perfectly flat (0.294 → 0.532, rising by
0.199 ± 0.074 between 0.38 and 1.18 Mpc, 2.7σ); u_in = 0.412 is the fit's compromise, and that
residual is item 1 of "what this does not do".

**4. Mechanism (i), relaxation toward dust — NO-GO on sign.** Any local process whose rate rises
with density has `t_relax = 1/(nσv) ∝ t_dyn/ρ`. At the excess-weighted centres 0.6 and 2.0 Mpc, for
an NFW halo with M200c = 1.49e14 and c = 4.5, ρ(0.6)/ρ(2.0) = 24.1 and t_dyn = 0.71 / 2.78 Gyr, so

    t_relax(0.6)/t_relax(2.0) = 0.0107 — the core relaxes 94x FASTER.                          (4)

Relaxation drives the core to dust first and predicts u_inner > u_outer; the data have
0.335 < 0.987. The data *require* the opposite: to leave the inner band at 0.335 while the outer
reaches 0.986, t_relax must **decrease** outward by a factor 49 (K13), a 3.66-decade discrepancy in
the wrong direction. K14 closes the escape route: normalise the one free amplitude so the outer
band is fully relaxed at t_age = 13.8 Gyr and the inner band comes out at u = 1.000 — excluded at
11.8σ. Relaxation cannot be rescued by its normalisation either.

**5. Mechanism (ii), phase space — NO-GO.** `u = 1/2 ⇔ β = 1/2`, and for Osipkov–Merritt
`β(r) = r²/(r²+r_a²)` that is `r = r_a` exactly. The NFW potential contains one length,
`r_s = r200c/c = 0.229 Mpc`, so the only parameter-free choice puts the crossing at **0.229 Mpc**;
the data cross u = 1/2 at **1.065 Mpc** (log-linear between the 0.81 and 1.18 Mpc bins), a factor
**4.64** away (K15). `r_a` must therefore be fitted, and then:

- fitting `u = A·β(r)` with two free parameters gives χ²/dof = **4.25** (r_a = 0.391 Mpc, A = 0.628)
  against **1.75** for the step (three parameters, since r_t is also fitted) — Δχ² = **16.7** for
  one extra parameter, because the data have a discontinuity no single-scale β produces (K16);
- both normalisations fail in opposite directions: with r_a pinned at the observed crossing, `u = β`
  (radial fraction) is 4.3σ wrong at 0.38 Mpc and `u = 1−β` (isotropic fraction) 11.0σ wrong there
  (K17). `u = 1−β` is the sign the lane's premise literally states, and it predicts u *falling*
  outward: 0.155 at 2.49 Mpc against 0.986 ± 0.098.

**6. Mechanism (iii), the splashback boundary — SURVIVES.** Outside r_sp the medium has never been
shocked: one stream, zero dispersion, `p = 0`, hence `w = 0` and **u = 1 by construction, no
parameter**. Inside it is multi-stream and collisional, and whatever stress it carries is the
framework's cold-sector equation of state. For the stack

    r_sp = 0.83 r200m = (0.83 x 1.647) r200c = 1.367 r200c,                                      (5)

with r200m/r200c = 1.647 the exact NFW value at c = 4.5 for Δ200m = 200 Ω_m ρ_c, and M200c from
M500 via the same NFW at z = 0.2336. Three mass routes give M500 = 0.83 / 1.06 / 1.63e14 →
**r_sp = 1.31 / 1.41 / 1.63 Mpc** (central 1.414); the ±0.06 on `r_sp/r200m` together with the
mass-route spread spans 1.21–1.75. K18: the central value is 0.997 × the boundary (1.4174) — at the upper
edge of the 0.461–1.417 window. K19, with **no** mass estimate: the stacked *excess* D − P_N has its
steepest logarithmic slope, −2.24, between 1.18 and 1.71 Mpc → a caustic at **1.4186 Mpc**. K20:
r_sp is **0.005 Mpc (0.3%, 0.02σ)** from that caustic and inside the u-step interval.

**7. Why the rise is broad.** u is a line-of-sight average: `u_proj(R)` is a projection-weighted mean
of `u_3D(r)` over r ≳ R, so a 3D step at 1.41 Mpc must appear smoothed and displaced outward. That
is why the 8-bin rise spans 1.2–2.5 Mpc instead of one bin, and why the step fit returns
u_in = 0.412 rather than INNER's 0.335.

**8. The mass test (K21, K22).** If the transition is a boundary, `r_sp ∝ M^(1/3)` at fixed z, so a
**fixed metric** annulus is more "inside" for heavy clusters and u_OUTER must *fall* with mass.
Terciles by M_gas (medians 3.69e12 / 1.16e13 / 2.92e13 M_☉) give r_sp = 0.96 / 1.41 / 1.92 Mpc and

    u_OUTER = 1.898 +- 0.812  >  1.042 +- 0.157  >  0.683 +- 0.082                            (6)

against a **zero-parameter** sharp-step prediction 1.000 / 0.985 / 0.817
(Z = +1.1 / +0.4 / −1.6). The ordering is 3/3 and every point is inside 1.7σ. At the fixed radius
1.71 Mpc u is >1 for the low tercile (outside r_sp, unconstrained), 1.25 ± 0.40 in the middle and
0.59 ± 0.08 for the top: the transition radius is mass-dependent, as a boundary must be and a
relaxation time need not be.

## Status

- **Task 1 — NUMERICAL (exact inversion).** ⟨w⟩ = −0.2217 ± 0.0188 (INNER), −0.1761 ± 0.0120
  (MID), −0.0045 ± 0.0328 (OUTER); `u = 1+3⟨w⟩` exact; round trip to A_law residual 0. The inner
  band is under tension at 12σ, the outer band is dust at 0.14σ. `u = 1/2` (⟨w⟩ = −1/6) sits 0.79σ
  from MID — consistent, and not selected.
- **Task 2 (i) — NO-GO(obstruction).** Sign: t_relax ∝ t_dyn/ρ makes the core relax 94× faster.
  Normalisation: fully relaxing the outer band forces u_INNER = 1, excluded at 11.8σ. Both are
  independent of the medium's microphysics.
- **Task 2 (ii) — NO-GO(unpredictive + misfit).** r(β=1/2) = r_a is a free parameter; its
  NFW-motivated value misses by 4.6×; a smooth β(r) is rejected at Δχ² = 16.7; both normalisations
  fail at 4.3σ / 11.0σ.
- **Task 2 (iii) — CONDITIONAL(single-stream ⇒ dust; r_sp = 0.83 r200m).** Survives three
  independent checks (0.3% from the caustic; inside the u-step interval; mass ordering 3/3 with
  max 1.6σ). It explains *why u = 1 outside and where the transition is*; it does **not** explain
  why the inner value is below 1.
- **Task 3 — DECIDABLE prediction.** r_step = 1.10 / 1.39 / 2.00 / 2.99 Mpc at
  M500 = 5e13 / 1e14 / 3e14 / 1e15 M_☉ (K23) — the transition crosses the whole outer band.
- **Task 4 — DECIDABLE falsifier.** See below.

## Checks

`a29_checks.py` — 25 checks, deterministic, stdlib + numpy/scipy/sympy, 1.1 s, no network, reads the
CFG687 per-cluster npz, exit 0 iff all pass; three mutations each break a check group (`MUTATE.md`).

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | the npz IS CFG687 (six amplitudes) | 3.5e-8 rel | <1e-4 |
| K2 | three-band u; MID/OUTER = A21 | 0.3348 / 0.4716 / 0.9865 | ±1e-3 |
| K3 | ⟨w⟩ per band, ordered | −0.2217 / −0.1761 / −0.0045 | ±1e-3 |
| K4 | σ_⟨w⟩ = σ_u/3; σ_u from du/dA_l | 0.0361, 0.0120 | ±2e-3 |
| K5 | (ρ+3p)/2 from T^μ_ν (sympy) | 0 | <1e-25 |
| K6 | ⟨w⟩ → u → A_law round trip | 0 | <1e-10 |
| K7 | u=1/2 ⇔ ⟨w⟩=−1/6; distances | 0.79σ, 0.14σ | <1.5, <1 |
| K8 | constant u rejected | χ²/dof = 5.92 | >4 |
| K9 | the jump across 1.417 Mpc | +0.557 (2.58σ) | >2σ |
| K10 | three-parameter step | χ²/dof 1.75, split 0–5\|6–7 | <2 |
| K11 | OUTER sub-bands are both u=1 | 1.088±0.209, 0.939±0.106 | <1.2σ each |
| K12 | t_relax ratio, inner faster | 0.0107 | <0.1 |
| K13 | required vs predicted ratio | 49 vs 0.0107, 3.66 decades | >2 decades |
| K14 | fully-relaxed-outside ⇒ u_INNER=1 | 1.000 vs 0.335 (11.8σ) | >8σ |
| K15 | r(β=1/2) = r_s vs the data | 0.229 vs 1.065 Mpc (4.6×) | >2× |
| K16 | smooth β(r) rejected vs step | χ²/dof 4.25 vs 1.75, Δχ²=16.7 | >3, Δ>10 |
| K17 | both β normalisations miss | 4.3σ, 11.0σ | >3σ |
| K18 | r_sp vs the MID/OUTER boundary | 1.414 vs 1.4174 (0.997) | within 15% |
| K19 | caustic from the excess slope | −2.24 at 1.4186 Mpc | bin 1.18–1.71 |
| K20 | r_sp vs the u-step and the caustic | 0.005 Mpc (0.02σ), inside | <1.5σ |
| K21 | u_OUTER falls with mass | 1.90>1.04>0.68, max\|Z\|=1.63 | 3/3, <3 |
| K22 | r_sp ∝ M^(1/3) | 1.99×, u(1.71) ordered 3/3 | >1.7, ordered |
| K23 | the prediction's amplitude | 1.10 → 2.99 Mpc | >2.5× |
| K24 | σ_u needed in 1.42–2.5 Mpc | 0.0648 (now 0.0973), N≥717 | 0.02–0.09 |
| K25 | what that band already excludes | 5.0σ from ⟨w⟩=−1/6 | >3σ |

## What this does not do

1. **The inner amplitude is not derived, and the plateau is not flat.** u ≈ 0.33–0.47 needs ⟨w⟩ < 0;
   a velocity distribution can only give p ≥ 0, i.e. u ≥ 1, so tension must come from the cold
   sector's own stress. The missing premise is **(P1′) the shocked phase has
   ⟨w⟩ = −0.18 ± 0.01**, A21's (P1) restated with a radial index. Separately, the inner six bins
   rise by 0.199 ± 0.074 (2.7σ) from 0.38 to 1.18 Mpc; the sharp step does not describe that, and
   neither (i) (wrong sign) nor (ii) (rises too fast inside) accounts for it.
2. **u(r) is a projected, ΔΣ-weighted share, not a 3D volume average.** §7 uses that to explain the
   width of the transition, but no deprojection is performed: the 8-bin profile is `u_proj(R)` and
   the 3D ⟨w⟩(r) is bounded, not measured. This is A21's caveat 1, still open, and now the top item.
3. **r_sp carries an inherited coefficient.** 0.83 r200m (More+2015, ±0.06) × 1.647 (NFW c = 4.5) —
   neither from the theory. Your own conversion should be checked: the first version of this lane
   used r200m/r200c = 1.39 and got r_sp = 1.19 Mpc; the correct 1.647 gives 1.41 Mpc. The ±7%
   coefficient plus the mass-route spread is 1.21–1.75, so the *coincidence* with the caustic is not
   a 0.3%-precision result — only a ~10%-precision one.
4. **The M500–M_gas conversion is a single number (0.11).** The catalogue's own R500 implies
   M500 = 1.63e14, 54% above M_gas/0.11: the input catalogue is internally inconsistent at that
   level. Both routes put r_sp in the window; the tercile predictions shift by up to 5%.
5. **The 2-halo term is not separated.** The outer excess is flat in ΔΣ (13.9 → 14.5 between 1.71
   and 2.49 Mpc), which is also the signature of correlated large-scale structure. "Single-stream
   infall" and "unbound 2-halo material" both give dust and both turn on near r_sp, so the geometry
   survives either reading but the physical label is ambiguous.
6. **Bins are correlated and the covariance is noisy.** 30 patches for 8 bins makes the raw inverse
   ill-conditioned; all fits use the diagonal (conservative for a difference between positively
   correlated neighbours). The full jackknife covariance is stored for re-use. Spherical symmetry
   throughout, no miscentring, no EFE, no deprojection, no per-cluster r_sp: the stack is analysed
   at fixed metric radii with one median mass.

## Next

1. **Deprojection** is now the top item: `u_proj(R) → u_3D(r)` for a two-parameter step, to check
   that the 3D step sits at 1.41 Mpc and to recover the inner rise in 3D.
2. **3×3 grid** (three mass terciles × OUTER split at 2.06 Mpc): the self-similarity test
   `u = U(r/r_sp)` uses data already on disk.
3. **β(r) from simulations** (Uchuu, FLAMINGO, The300) at the stack's mass and z: if β never
   exceeds ~0.7 inside r200c, mechanism (ii) is dead independently of the lensing data.

## Falsifier

**A third band at 1.42–2.5 Mpc** — in this stack that is bins 6+7, i.e. the OUTER band itself, so
the discrimination must come from splitting OUTER at 2.06 Mpc (1.088 ± 0.209 and 0.939 ± 0.106,
both consistent with 1) or from a wider radial range. The required precision:

- (iii) predicts **u = 1.000, ⟨w⟩ = 0.000**, with no residual radial structure.
- (ii), with r_a pinned at the observed u = 1/2 crossing, predicts **u = 0.806, ⟨w⟩ = −0.065**.
- The separation is 0.194 in u. **3σ needs σ_u ≤ 0.0648, i.e. σ_⟨w⟩ ≤ 0.0216**, i.e. **N ≥ 717
  clusters** at the present 318-cluster per-object noise (K24) — a factor 2.3, which eRASS1's full
  sky (~12 000 clusters) crossed with LSST Y1 / UNIONS or DES Y6 supplies.

Present status of that band: u = 0.9865 ± 0.0973, ⟨w⟩ = −0.0045 ± 0.0324 — **5.0σ from ⟨w⟩ = −1/6**
and 5.0σ from u = 1/2 (K25). So the question the third band settles is not "1 or 1/2" but
**"1.00 or 0.81"**, and it settles it at 3σ with 2.3× the clusters. Two sharper variants are
already decided by data on disk:

- **the core**: (i) predicts u → 1 at small r; the INNER band gives 0.335 ± 0.056, excluding it at
  11.8σ. A 0.05–0.15 Mpc band with σ_u ≤ 0.11 would close it for good.
- **the mass scaling**: r_step = 1.10 → 2.99 Mpc over 5e13–1e15 M_☉. Measuring the step in three
  mass bins at fixed z tests (iii) with no new physics, and the present terciles already order
  correctly (1.90 / 1.04 / 0.68, max 1.6σ).
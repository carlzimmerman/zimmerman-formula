# A6 — the four distinctive assets, each as a number and a kill condition

Lane A6, DS_FINAL_2026_10_21. Script: `a6_checks.py` (21 checks, under 1 s, no network),
output `a6.out`, numbers `a6_results.json`, mutation `MUTATE.md`.
Quoted numbers attributed to "the note" are Zenodo 23533323 v1.2 (2026-10-21), an external input.

## Claim

Four things in this framework have no counterpart in any other theory, and each is turned
here into one number plus the observation that would kill it. **(1)** The exact static law
has no positive-mass realisation at a Newtonian null point: for two equal masses the cold
energy density must go **negative in a thin pancake through the saddle**, here
**−89.3× the cosmic mean cold density** at R = 0.2 d for a Milky-Way–M31-like pair (the
note's −89, reproduced), and the column through the saddle is negative, with a missing
depth of **3.529 M_sun/pc²** (the note's 1.9–2.1, same order). **(2)** Within
μ = x/(1+x)^p the exact Newtonian limit forces **p = 1** uniquely; the "smallest constant
anomaly" argument for it is **empty** — p = 1 has the *largest* constant anomaly, a₀,
which is exactly the open strong-field problem. **(3)** The two footings differ by
**1.2073, which is 1/√Ω_Λ = 1.2093** (from Λ and H₀), a 20.7 % band that no internal relation
closes. **(4)** The two laws have capacities **a₀ and a₀/2** and their maximum
circular-speed difference at fixed (M_b, r) is exactly **√(2/√3) − 1 = 7.457 %**, at
g_N = a₀/2 — the note's 7.46 %, verified exactly.

## Derivation

Units c = 1 except where SI is quoted; K = 8πG; y ≡ g_N/a₀.

### 1. The saddle no-go

**1.1 The law.** The note's action gives, on varying P, u² = g_N(a₀ − u) with u ≡ K|P| and
g = g_N + u. Eliminating u: **g_N = g²/(g + a₀)**, i.e. ν(y) = ½(1 + √(1 + 4/y)) (K10).
Two equal point masses ±M at x = ±d/2 give, on the axis, g_N = (16GM/d²)·u/(1−u²)² with
u = x/(d/2): a genuine saddle, and g_N ≪ a₀ over the interior |x| < 0.9·d/2 for any wide pair (it reaches a₀ only within ~0.05 d of each mass).

**1.2 The density, exactly.** With ρ_cold = −∇·(g − g_N)/(4πG) — the convention
∇·g = −4πGρ, in which an isolated galaxy has a *positive* cold halo — and using
∇·g_N = 0 away from the sources,

  ∇·u = (ν′(y)/a₀)·(g_N·T·g_N)/|g_N| ,   T_ij = ∂_i g_N,j  (traceless).

This is algebraic: no grid, no finite differences, no softening. K1 validates it against a
central-difference divergence of u = (ν−1)g_N at six points (max relative error 2.43e−6).
Two independent limits confirm the sign: at r ≫ d the pair tends to a single 2M mass and
ρ_cold → +√(a₀G·2M)/(4πG r²); and on the axis ρ_cold > 0 while in the perpendicular
bisector plane ρ_cold < 0.

**1.3 Geometry.** At R = 0.2 d the negative region is a band of **30.5°** about the
perpendicular plane (half-width 15.3°), i.e. **26.3 %** of the solid angle — a thin
pancake, matching the "about a quarter" of the earlier grid study. Along the pancake the
density diverges as **r^(−1/2)** (|ρ|√r constant to 0.597 % over a decade in r, K7): the
null is a square-root branch point, and the divergence is integrable (M_cold(<r) ∝ r^(5/2)),
so the *mass* is finite while the *density* is unbounded below.

**1.4 The magnitude.** ρ̄_cold ≡ Ω_c ρ_crit = 5.364 Ω_b ρ_crit = 2.254e−27 kg/m³, using
Ω_b h² = 0.02237 and h = 0.674 (external). For M_b = 1.4e11 M_sun each and d = 780 kpc:

  ρ_cold(0.2 d, pancake) = −2.013e−25 kg/m³ = **−89.3 ρ̄_cold**  (note: −89).
                         = +1.138e−24 kg/m³ on the axis.

Sensitivity: −75.5 at M_b = 1e11, −92.5 at 1.5e11, −110.9 at d = 700 kpc (same M_b). The note does not
state M_b or d; −89 sits inside the band spanned by plausible MW/M31 baryonic masses, and
pins M_b ≈ 1.4e11 M_sun at d = 780 kpc.

**1.5 The cluster pair — the one place the note does not close.** For M_b = 1e15 M_sun each:

| d | ρ(0.2d)/ρ̄_cold | negative column [M_sun/pc²] |
|---|---|---|
| 3.0 Mpc (bound) | **−485** | −76.01 |
| 11.78 Mpc (gives −33) | **−33.0** | −19.73 |
| 4.2e12 M_sun, 3 Mpc | **−33.07** | **−5.025** |

So −33 is *not* a cluster-pair number at any bound separation: a 1e15 pair needs
**11.78 Mpc** (unbound, supercluster scale) and then its column is −19.73 M_sun/pc², four
times the quoted 4.6–5.1. The note's two cluster numbers (−33 **and** 4.6–5.1) are jointly
reproduced only by a **group-mass pair, M_b = 4.2e12 M_sun each (a 1e14 halo at
f_b = 0.04) at 3 Mpc**, which gives −33.07 and −5.025 simultaneously (K4b). That is a real
internal inconsistency in the note, and it is the only one found.

**1.6 The column and the net sign — refuted.** Line of sight in the pancake plane (what a
lensing survey measures for a pair separated on the sky), |L| < d:

  negative part **−3.529**, positive part **+1.105**, **net −2.424 M_sun/pc²**.

The magnitude is the note's order (1.9–2.1) but 1.8× larger; the *sign* is not. The note
says the total column is still positive (−0.206 negative part, +0.016 net, ratio −0.078).
In the exact 3-D solution the net passes through zero at **φ = 77.4°** from the pair axis
(net 0.00, negative part −1.525 M_sun/pc²) and is −2.42 at the physical φ = 90°; the quoted
pair is reproduced only within a degree of that zero crossing. It is a line-of-sight
artefact, not a property of the solution. **The law therefore does predict a shallow
negative convergence at the pair midpoint**; what a positive-mass medium cannot do is
supply it. The negative part is stable against the integration length
(−3.529 → −4.039 M_sun/pc² for |L| = 1d → 8d), so the depth is a real number, not a
box artefact.

**1.7 What it forbids.** For every ε > 0 there is a neighbourhood of the null in which
ρ_cold < −ε. A medium of positive rest mass has ρ ≥ 0 everywhere, so **no positive-mass
medium can realise the exact law at a Newtonian null point**: either the medium departs
from the law there (the framework's own escape, via the stiffness term (γ/2)|∇P|², whose
length L_* = 24 pc–1 kpc cuts off the cusp), or the law is not the medium's equilibrium
law. This is a no-go on the *realisation*, not on the law: the law is exact and its
solution is unique; it is the ontology that cannot supply it.

**1.8 What it predicts.** No saddle dip. Where the law demands ρ_cold < 0 the medium
flattens at ρ = 0, so the observed column at the midpoint is *higher* than the law by the
missing depth **3.529 M_sun/pc²** (MW-M31-like) and **5.025** (the geometry that reproduces
the note's cluster numbers). Against Σ_crit ≈ 3000 M_sun/pc² that is Δκ ≈ 1.176e−3.

**1.9 The survey size.** With n_src = 10 arcmin⁻², σ_ε = 0.3, Σ_crit = 3000 and a 1.5′
aperture, σ(ΔΣ) = 107 M_sun/pc² per pair, so a 3σ detection of a 3.529 M_sun/pc² depth
needs **N = 8.28e3 pairs** = **11.8×** a 700-pair stack — the note's "~12×" (K9).
At the note's own depth of 2.0 M_sun/pc² it would be 2.58e4 pairs.

**Status: NO-GO(obstruction), with the numbers NUMERICAL.** The obstruction is proved
(the cusp + positivity); the magnitudes are computed, not fitted.

### 2. The exact law identity

**2.1** g_N = g²/(g+a₀) ⟺ g = (g_N/2)(1 + √(1+4a₀/g_N)) ⟺ ν = ½ + √(4a₀+g_N)/(2√g_N)
⟺ u² = g_N(a₀−u), u = g−g_N. sympy residuals **0 / 0** (K10). The last form is the
physical one: the medium's displacement saturates, u < a₀.

**2.2 Which p?** In μ = x/(1+x)^p (x = g/a₀, y = g_N/a₀ = xμ):
y/x → 1 only for **p = 1**; p < 1 gives ∞, p > 1 gives 0 (K11). The deep-MOND geometric
mean y/x² → 1 holds for *every* p (K12), so it is not the selector; exact Newton is, and it
leaves exactly one member. **p is not free: p = 1.**

**2.3 "Smallest constant anomaly" is empty.** In the wider family μ = x/(1+x^p)^(1/p),
which keeps *both* limits for every p, ν−1 ≈ 1/(p y^p): the constant-anomaly coefficient
lim y(ν−1) is **1 at p = 1 and 0 for p > 1** (K14). So p = 1 has the **largest** constant
anomaly in that family, not the smallest; the minimisation selects p → ∞ (a step function),
not the canonical law. What survives is the *exact* statement: the canonical law's
strong-field residue is a constant **a₀** (coefficient 1), the n = 2 law's is **a₀/2**
(coefficient ½) (K13) — and that a₀ is precisely the 1279× ephemeris problem on the record.
The correct justification of p = 1 is exact Newton plus saturation at one scale, not a
minimisation.

**2.4 The measurable discriminator.** The RAR's logarithmic slope at the knee (y = 1) is
**0.72361** for the canonical law and **0.75000** for the n = 2 law.

**Status: DERIVED (p = 1 unique) + REFUTED ("smallest anomaly").**

### 3. The two footings

**3.1** a₀_alt/a₀_can = 1.13e−10/9.36e−11 = **1.207265** (K15). Both footings are the same
relation a₀ = (c/2)√(Gρ) evaluated at ρ = ρ_Λ or ρ = ρ_crit:
(c/2)√(Gρ_Λ) = 9.3542e−11 vs 9.36e−11 stated; (c/2)√(Gρ_crit) = 1.1312e−10 vs 1.13e−10
stated (K17, both within 0.1 %).

**3.2** Therefore the ratio is exactly √(ρ_crit/ρ_Λ) = **1/√Ω_Λ = 1.20931** (K16); the
0.14 % gap from 1.2073 is the rounding of the two quoted a₀ values. This is the internal
content: **the 20.7 % band is the cosmological matter density**, not a free parameter.

**3.3 Nothing internal fixes which.** The framework's equations contain G, Λ, c, κ and the
baryon/cold densities; the map (ρ_Λ, ρ_crit) → a₀ is two-valued and every other relation is
invariant under the swap. The one candidate link, Λ/a₀² = (π/4)y_t, merely moves the choice
into the turn-off scale y_t. So the footing is an **external** choice, and the theory
predicts a 20.7 % band rather than a point — an asset only if something measures it.

**3.4 What observation decides.** A direct, systematics-controlled measurement of the RAR
knee scale (or the BTFR zero point) at **5 %** separates the footings at **4σ**; at 10 %,
2σ. A measurement of the Solar-System turn-off y_t (via Λ/a₀² = (π/4)y_t) does the same
job from the other end.

**Status: DERIVED (ratio) + OPEN(which footing; one external measurement).**

### 4. The capacity statement

**4.1** lim_{g_N→∞}(g − g_N) = **a₀** for the canonical law and **a₀/2** for the n = 2 law
(K18). This is exact and it is a statement about the *saturation scale* of the medium:
u = K|P| obeys u < a₀ in the first case and u < a₀/2 in the second. The canonical law is
literally the saturation law u² = g_N(a₀ − u); the n = 2 law is u(2g_N + u) = a₀g_N.

**4.2** At fixed baryonic mass and radius V² ∝ g, so ΔV/V = √(g₁/g₂) − 1. Maximising over
y gives a single critical point **y = ½** with g₁/g₂ = 2/√3 exactly, hence

  **max ΔV/V = √(2/√3) − 1 = 0.0745699 = 7.457 %**, at **g_N = a₀/2** (K19, K20).

The number contains no a₀: both footings give the same 7.457 %, and it is a *maximum*, not a
typical value, but the maximum is broad (5.644 % at y = 0.1, 5.610 % at y = 2). The note's 7.46 % is verified
exactly.

**Status: DERIVED (exact).**

## Checks

`a6_checks.py` — 21/21 PASS, exit 0, under 1 s. Full output in `a6.out`.

| id | what it proves | value |
|---|---|---|
| K1 | analytic ∇·u = finite-difference ∇·u (independent sign) | max rel err 2.43e−6 |
| K2 | ρ < 0 in the pancake, > 0 on the axis at R = 0.2d | ratio −0.177 |
| K3 | the −89 number | −89.3 |
| K4 | −33 needs an unbound 1e15 pair | d = 11.78 Mpc |
| K4b | −33 **and** 4.6–5.1 need a group-mass pair | −33.07, −5.025 |
| K5 | missing depth, MW pair | −3.529 M_sun/pc² |
| K6 | net saddle column is **negative** (refutes +0.016) | −2.42 M_sun/pc² |
| K7 | r^(−1/2) cusp at the null | spread 0.597 % |
| K8 | pancake geometry | 26.3 % of solid angle, 30.5° wide |
| K9 | survey size | 8.28e3 pairs = 11.8× |
| K10 | law ⟺ ν ⟺ saturation, sympy | residual 0 |
| K11–K14 | p = 1 forced; geometric mean no selector; anomaly a₀ vs a₀/2; "smallest" refuted | 1 / 1 / ½ / 0 |
| K15–K17 | footing ratio, = 1/√Ω_Λ, both from one relation | 1.207265 / 1.20931 / 9.3542e−11, 1.1312e−10 |
| K18 | capacities | a₀, a₀/2 |
| K19 | max ΔV/V exact | 0.0745699 at y = ½ |
| K20 | maximum is a pure number | grid max 0.074570 at y = 0.500 |

## Kill conditions

1. **Saddle.** A stack of pair midpoints measuring the column at **±3.529 M_sun/pc²**: a
   *negative* detection at the law's depth (−3.529) falsifies the positive-medium premise
   outright; a null at ±1 M_sun/pc² with ~1e5 pairs makes the test unfalsifiable in
   practice. Amplitude scales as M_b^(1/2), so a mass-binned sample tests the *shape*, not
   just the amplitude.
2. **Identity.** The RAR knee slope: 0.7236 (canonical) vs 0.7500 (n = 2). A 2 % measurement
   at g_N ≈ a₀ kills one of them; a slope inconsistent with 0.7236 at 3σ kills p = 1.
3. **Footings.** A 5 % a₀ measurement → 4σ between the footings; a 10 % one → 2σ. Nothing
   internal substitutes for it.
4. **Capacity.** Any galaxy with a 2–3 % circular-speed measurement at g_N ≈ a₀/2 decides
   between the two laws; if no system anywhere shows a >7.457 % difference, one of the two
   laws is excluded, because 7.457 % is the exact maximum.

## What this does not do

- Point masses only. The source cores are singular; a finite-size mass changes ρ inside the
  baryonic radius but not the pancake integral (which converges as r^(−1/2)).
- The stiffness term (γ/2)|∇P|² is **not** solved. It must smooth the cusp inside L_*; the
  column, being an integral of an integrable divergence, is insensitive to that at the few-%
  level, but this is asserted, not computed.
- The note does not define "mean cold density" or the pair masses. I adopt
  ρ̄_cold = Ω_c ρ_crit (the only framework-native mean) and state every (M_b, d); the −89
  reproduction is 15 % sensitive to those choices and the cluster numbers are 100 %
  sensitive to them.
- The survey forecast uses stated, not measured, survey parameters (n_src, σ_ε, Σ_crit) and
  N_pub = 700 as an order-of-magnitude external input; the 11.8× is a scaling, not a
  measurement forecast.
- The line-of-sight convention matters: the quoted −0.206/+0.016 is recovered at φ = 77.4°
  only. The physical φ = 90° gives −2.42.

## Next

1. Re-run §1 with extended baryonic masses (Plummer, 3 kpc core) and the stiffness term, and
   report the residual of the missing depth — this is the only way to turn 3.529 into a
   prediction with an error bar.
2. Do the real ΔΣ stack forecast on a pair catalogue (separation- and mass-binned), including
   the ΛCDM two-halo term, which adds with the *opposite* sign and is the actual systematic.
3. Measure the RAR knee slope on SPARC with a 3-D inclination/velocity budget: 0.7236 vs
   0.7500 is a 3.647 % difference and the cheapest of the four kill conditions to run.
4. For the footings, either quote the 20.7 % band as a prediction everywhere (never pool) or
   find the observation that closes it; there is no third option.

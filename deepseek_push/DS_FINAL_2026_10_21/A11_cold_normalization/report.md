# A11 — the cold-sector normalization from first principles

## Claim

The cold sector has **no free normalization inside the frozen law**. For a spherical system
`g_N = g²/(g+a0)` fixes the enclosed mass ratio at every radius exactly,

    M_ph(<r) / M_b(<r) = ½ [ √(1 + 4/y) − 1 ],      y ≡ g_N(r)/a0,

so the ratio is a *prediction* — a one-parameter function of `y`, with concentration entering only through
the enclosed baryon fraction. At the virial radius the law returns **25.04** for a Milky-Way-like system
and **2.62** for a cluster-like one, a factor **9.57** apart: no single number can be universal.
**5.364 is not a normalization the law requires.** It is exactly the cosmological ratio
`(1−f_b)/f_b = 5.364327`, which equals the law's ratio only at `y = 0.029291`, i.e. at `r = 5.84297 r_M`
or at `r_200` of a `1.76e14 M☉` halo — one point of the family.

The record's `N = 5.364/f_ret` is a **catchment mass budget**, and it enters the theory *only* as the
truncation radius `r_e = r_M√(N(N+1)) ≈ (N+½)r_M` (reproducing the record's `r_M/ln(1+1/N)` to `5.4e-4`).
Given `(f_b, f_ret)` it is arithmetic; `f_ret` is a fitted table; the premise that gives it meaning
(A23, "each system settles the cosmic share of its catchment") is posited, with six failed derivations on
record. **`N ≈ 8` is fitted, not forced.** Two things *are* derived: the scaling
`M_ph/M_b ∝ f_eff^{−1/2} M_v^{−1/6} Δ^{−1/3}`, and the bound `N ≲ r_ta/r_M` (**30.2** at `M_b = 1e13`),
which **excludes the condensed variant N = 53.6** above `M_b ≈ 1.26e13` because its edge leaves the
turnaround ball (`1.412×` outside at `1e14`).

## Derivation

`G = 6.67430e-11`, `a0 = 9.36e-11 m/s²` (canonical footing), `M_☉ = 1.98847e30 kg` (`= GM_☉/G`).

**1. Law and inverse.** `g_N = g²/(g+a0)` is quadratic in `g`; the physical root is

    g = (g_N/2)(1 + √(1 + 4a0/g_N)).                                              (1)

K1: (1) is an exact symbolic identity of the law (residual 0).

**2. Phantom = enclosed mass difference.** Define `M_ph(<r) ≡ r²(g−g_N)/G` and `M_b(<r) ≡ r²g_N/G`.
For spherical symmetry each is the Gauss-law mass of its own field, so `M_ph = M_tot − M_b` and the
volume integral `∫4πr²ρ_ph dr` collapses to the boundary term. *This is why "integrating to the virial
radius" cannot rescale anything, and why the concentration does not enter as a normalization.* K22 does the
integral explicitly (Hernquist, 40 000 shells to `0.30 Mpc`): it returns the boundary term to `1.3e-15`, and
`ρ_ph > 0` everywhere (`min = 3.8e-25 kg/m³`), so a round isolated system has no negative-phantom lobes of
the kind A41 records for the global QUMOND field.

**3. Exact ratio.** Dividing, with `y = g_N/a0`,

    M_ph/M_b = g/g_N − 1 = ½[√(1 + 4/y) − 1] ≡ F(y).                               (3)

K2: exact symbolically and identical to the numeric `F` used by every check (deviation 0).

**4. Limits.** `y→0`: `F → y^{−1/2} − ½` (K3a, `1.3e-9` at `y = 1e-8`). `y→∞`: `F → 1/y` (K3b, `1.0e-6`).

**5. Inverting 5.364.** `F(y) = 5.364327` ⇒ `y* = 4/[(2·5.364327+1)²−1] = 0.029291`, `r*/r_M = 5.84297`
(K4a `0`, K4b `5.842973`). As a halo: `F(f_b a_v/a0) = 5.364327` at `M_v = 1.76e14 M☉` (K4c). **That is
all 5.364 is: the law's ratio at 5.843 MOND radii.**

**6. Concentration.** (3) holds exactly for extended profiles with `y(r) = GM_b(<r)/(a0 r²)`. For
Hernquist, `M_b(<r)/r² = M_b/(r+a)²`, so with `c ≡ r_v/a`, `μ(c) ≡ M_b(<r_v)/M_b = (c/(1+c))²`:

    M_ph/M_b(<r_v) = F(μ r_M²/r_v²),   M_ph/M_b,tot = μ[1 + F(μ r_M²/r_v²)] − 1.    (5)

K19 verifies (5) against the direct `M_tot/M_b − 1` for `c = 7.2 … 247` (worst `1.2e-12`). Because
`F ∝ y^{−1/2}`, the `c`-dependence is `μ^{1/2}` and weak: 32× in `a` moves the MW ratio from `25.53` to
`20.94`. **The ratio is a function of `y` and weakly of `c`; of nothing else.**

**7. The virial radius is not free.** The law fixes `M_tot(<r)`, so `r_v` solves
`r²g(r)/G = (4π/3)Δ_vρ_c r³`. Self-consistent solutions (Hernquist, `Δ_v = 200` wrt `ρ_crit`):

| system | `M_b` | `a` | `r_v` | `M_tot` | `μ(<r_v)` | `M_ph/M_b,tot` | `y_v` | `c` |
|---|---|---|---|---|---|---|---|---|
| MW-like | `6.0e10` | 4 kpc | `0.2455` Mpc | `1.563e12` | `0.968` | **25.04** | `0.00144` | `61.4` |
| cluster-like | `1.4e14` | 250 kpc | `1.6863` Mpc | `5.065e14` | `0.758` | **2.62** | `0.05560` | `6.7` |

`M_b`, `a` are labelled inputs (MW: `M_* 5.5e10 + M_gas 5e9`, `r_h ≈ 5 kpc`; cluster: `M_500 ≈ 1e15`,
`f_b ≈ 0.15`, `r_h ≈ 330 kpc`). K5: spread `9.57`.

**8. Scaling.** With `a_v ≡ GM_v/r_v²` and `f_eff ≡ M_b(<r_v)/M_v`, `y_v = f_eff a_v/a0`, so

    M_ph/M_b ∝ f_eff^{−1/2} M_v^{−1/6} Δ_v^{−1/3} ρ_c^{−1/3}.                      (6)

K6: slope in `M_v` is `−0.167573` (target `−1/6`), in `f_eff` `−0.500000` (target `−½`). At `1e13` the
instantaneous slope is `−0.5266`, because the `−½` offset in `F` is already active — the ratio is *not* a
power law over the observed range.

**9. Where 5.364 comes from.** `5.364327 = (1−f_b)/f_b`, `f_b = 0.02237/0.14237 = 0.157126`
[EXT CFG515 `cfg515_lib.py:15`]. It is `ω_c/ω_b` — universal *as cosmology*, not as a force law. (The
supply is `M_c = (1−f_b)M_ta = 0.843 M_ta`, i.e. `5.364327×` the **retained baryons**, not the catchment.)

**10. The census N.** `N = (1−f_b)/(f_ret f_b) = 5.364327/f_ret`
[EXT CFG953 `FROZEN_CRITERIA.md:102`], with `f_ret` the CFG416 table (`0.10` below `10^12.5`,
`+0.45/decade` to `10^13.5`, `+0.30/decade` capped `0.90`) and `M_ta = M_b h/(f_ret f_b16)`,
`h = 0.674`, `f_b16 = 0.157` [EXT CFG416 via CFG515]. Reproduced: `N = 53.643, 44.125, 14.917, 8.296,
5.960` at `M_b = 3e10 … 1e14`, matching CFG953 `DERIVATION.md` a3 (`53.6, 44.1, 14.9, 8.3`, [EXT]).
`f_ret(1e13) = 0.6466`; `N = 8` needs `f_ret = 0.67054`, 3.6% away (K8b). `N` is not a perfect cube
(`N^{1/3} = 2.024`, K8a), so "8 clumps" is numerology.

**11. N is one equation in two unknowns.** The edge is where the phantom has grown to the supply:

    r_e²(g − g_N)/G = N M_b   ⇒   r_e = r_M√(N(N+1)).                               (7)

K9a: (7) satisfies the supply equation to `1.1e-16`. K7c: the record's `r_M/ln(1+1/N)` is the `N ≫ 1`
expansion of (7), differing by `5.4e-4` at `N = 8.3`. **K17: all `N ∈ [1,30]` (40 values) satisfy (7) at
their own edge** — the law does not pick `N`. (7) is one equation for two unknowns; the second equation is
the mass-budget premise A23.

**12. The census does not match the law, and matches best at 4e12.** Comparing `N` with `F` at the `r_200`
that `N` itself implies:

| `M_b` | `3e10` | `6e10` | `1e11` | `1e12` | `1e13` | `1e14` |
|---|---|---|---|---|---|---|
| `N` | 53.643 | 53.643 | 44.125 | 14.917 | 8.296 | 5.960 |
| `F(y_200)` | 36.82 | 32.75 | 28.15 | 13.30 | 7.37 | 4.38 |
| `N/F` | 1.457 | 1.638 | 1.567 | 1.122 | 1.126 | 1.360 |

The census **never undersupplies** the law; closest approach is `1.072` at `M_b = 4.0e12`
(`log10 = 12.60`), and `1.126` at `1e13`. `N ≈ 8` "works" at `1e13` because that is within 13% of the
point of closest agreement between two unrelated normalizations — not because either is derived.

**13. A bound on N that does bite.** R5 draws the supply from inside the turnaround ball, so `r_e < r_ta`
with `r_ta = (3M_ta/(4πΔ_taΩ_mρ_c))^{1/3}`, `Δ_ta = 11.81` [EXT A26, in units of `Ω_mρ_crit`, matching
CFG527 `M_ta()`]. Hence `N² + N < (r_ta/r_M)²`, i.e. `N ≲ r_ta/r_M` = `148, 114, 53.9, 30.2, 18.4` at
`3e10 … 1e14` (K10). The census variant stays at `r_e/r_ta ≤ 0.393`; the condensed variant (`f_ret = 0.10`,
`N = 53.643`) reaches `1.412` at `1e14` and crosses 1 at `M_b ≈ 1.26e13`. The mechanism is worth naming:
**a low retained fraction forces a large catchment, and the supply edge then leaves the turnaround ball.**
At `1e14` the condensed reading needs `r_e = 20.9` Mpc against `r_ta = 14.8` Mpc, while the census reading
gives `2.49` against `7.11` Mpc. That is why the census's *rising* `f_ret` (`N → 8`) survives at cluster
masses and the floor (`N → 54`) does not.

**14. The cold energy's sound speed is fixed by the record's identity.** With `∇·P = ρ_c − ρ̄_c` and
`γ = 2πG L*²`, the internal energy is a `Γ = 2` polytrope [EXT AG6D Part A], so

    c_s² = 2πG L*² ρ_c,     k_J = √2/L*,     R_TF = πL*/√2.                        (9)

At `Ω_cρ_crit` (`Ω_c = 0.2645` [EXT Planck]) with `L* = 24 pc`: `c_s² = 0.5191` (K11a) — `c_s = 0.72c` —
and `c_s = c` at `L* = 33.311 pc` (K11b). Thus `0.91` of the window (in log) is **superluminal** for the
`P` medium on the minimal assignment `I_eff = 1/ρ_c`; the round-2 mediator evades this only through a free
`f = J_q/(I+J_q) ≥ (c_ac/c)²`. At a galactic density `0.01 M_☉/pc³` the identity needs `L* ≤ 0.0608 pc`
(K12) — **394× below the window.** The `Γ = 2` reading is unavailable inside halos; the pressure must be
switched off there (SCT R2, labelled dust is inert).

**15. The window is a velocity window, and the cutoff is the same length.** `L* = σ_c²/a0` inverts to
`σ_c = √(a0L*)`: `24 pc ↔ 8.33 km/s` (within 1% of the 8.23 km/s thermal value for `10^4 K` gas at `μ = 1.22`, AG6D B7
[EXT]), `1 kpc ↔ 53.74 km/s`. The upper end is also `V_f²/(9a0)` for a `M_b = 6e10` galaxy
(`V_f = (GM_b a0)^{1/4} = 165.2 km/s`, `V_f/3 = 55.08 km/s → L* = 1.050 kpc`, K21): the scan boundary is
where the medium's dispersion reaches a third of the flat speed — `CONDITIONAL(σ_c ≤ V_f/3)`, not a
derivation of the 3. The **cutoff length is the same length**: `λ_J = 2π/k_J = √2πL* = 4.443 L*`
(`106.63 pc` at 24 pc, `4443 pc` at 1 kpc; K13a). But the record's *cosmological* cutoff is a different
object: `k_1/2 = 0.98 Mpc⁻¹` at `L* = 24 pc` [EXT AG6D C1] ⇒ `1.020 Mpc`, `9.6e3×` larger (K13b); and a
free-streaming reading at the same dispersion gives `λ_FS = σ_c·2/(3H0) = 82.35 kpc`, `772×` the Jeans
length (K14). **Three cutoffs from one `L*`, spanning 3.98 dex; only the Jeans one is in the window, and it
is there by construction.**

**16. "Collisionless at galaxies, collisional at clusters" is a no-go twice.**
*(a) Barotropic.* At fixed `Δ` the density is identical for every mass, so for `c_s² = Aρ^α`,
`c_s²/σ_vir² ∝ M^{−2/3}` for **every** `α` (K15a `−0.666667`; K15b spread `2.3e-15` over `α = −3…3`).
Pressure support is always relatively weaker in bigger systems; no `c_s(ρ)` can be negligible in galaxies
and dominant in clusters. *(b) Contact term.* The scattering depth per particle over `t_age` is
`τ = ρ(σ/m)σ_vir t_age ∝ M^{1/3}`; requiring `τ<1` at `1e12` and `τ>1` at `1e15` (10 Gyr) needs
`σ/m ∈ [13.0, 130.2] cm²/g` (K16) against the Bullet scale `< 1 cm²/g` [EXT AG6D, PROVISIONAL] — excluded
by ≥ 13×. The required scale dependence is in neither a contact term nor a barotropic `c_s`.

## Status

- **Task 1 — DERIVED (the ratio) + NO-GO (universality).** `M_ph/M_b = F(y)` exact (3); concentration via
  (5). 5.364 is not universal — it is `(1−f_b)/f_b` and equals `F` only at `r = 5.84297 r_M`
  (`r_200` of `1.76e14 M☉`). The law demands `25.04` (MW-like) and `2.62` (cluster-like).
- **Task 2 — NO-GO(obstruction) with a positive sub-result.** `c_s² = 2πG L*²ρ_c` (9) is superluminal over
  `0.91` of the window at cosmic density and `394×` over the window inside a galaxy; the galaxy/cluster
  split is impossible for a barotropic `c_s` (§16a) and needs `σ/m ≥ 13 cm²/g` for a contact term (§16b).
  The cutoff *is* the window length (`λ_J = 4.443L*`), but the record's `k_1/2` is 4 dex away from it.
- **Task 3 — NUMERICAL / fitted.** `N` is arithmetic in `(f_b, f_ret)`, fitted through `f_ret`,
  underdetermined by the law (K17). `N ≈ 8` needs `f_ret = 0.67054` vs the table's `0.6466` (3.6%).
  The derived bound `N ≲ 30.2` at `1e13` does not select 8, but excludes 54 above `1.26e13`.
- **Task 4 — DECIDABLE.** See **Next**.

## Checks

`a11_checks.py` — 34 checks, deterministic, stdlib + numpy/scipy/sympy, 0.5 s, no network, exit 0 iff all pass.

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | (1) exact inverse of the law (sympy) | 0 | 1e-30 |
| K2 | (3) exact (sympy) and equal to the numeric `F` | 0 | 1e-13 |
| K3 | deep / Newtonian limits | 1.3e-9, 1.0e-6 | 1e-6, 1e-5 |
| K4 | `5.364327 ⇔ y* = 0.029291 ⇔ r/r_M = 5.84297`; `M_v = 1.76e14` | 5.842973 | 5.84297 |
| K5 | non-universality `F_MW/F_cluster` | 9.566 | > 2 |
| K6 | scaling (6) in `M_v` and in `f_eff` | −0.167573, −0.500000 | −1/6, −½ |
| K7 | census `N`; record edge form vs (7) | 8.2958, 53.643, 5.4e-4 | 8.296, 53.643, 2e-3 |
| K8 | `N` not a cube; `f_ret(N=8)` 3.6% off | 0.0244, 0.0357 | > 0.01 |
| K9 | (7) solves the supply equation | 1.1e-16 | 1e-12 |
| K10 | R5: census inside, condensed outside `r_ta` | 0.393, 1.412 | < 1, > 1 |
| K11 | `c_s²(24 pc)`; `L*(c_s=c)` | 0.5191, 33.311 | 0.51908, 33.311 |
| K12 | galactic ceiling on `L*` | 394× below 24 pc | > 100× |
| K13 | `λ_J = √2πL*`; `λ_J/λ_cos` | 106.63 pc, 1.04e-4 | 106.629, < 1e-3 |
| K14 | `λ_FS/λ_J` | 772 | > 100 |
| K15 | barotropic slope `−2/3`, `α`-independent | −0.666667, 2.3e-15 | −2/3, 1e-10 |
| K16 | required `σ/m` lower edge vs Bullet 1 cm²/g | 13.0 | > 10 |
| K17 | all 40 `N ∈ [1,30]` satisfy (7) — law does not fix `N` | 40 | 40 |
| K18 | min `N/F = 1.072` at `log10M_b = 12.60`; `N/F(1e13)` | 1.072, 1.126 | 1.25, 13.0 |
| K19 | (5) vs direct `M_tot/M_b − 1` over `c` | 1.2e-12 | 1e-9 |
| K20 | turnover separation `r_e(53.6)/r_e(8.3)` | 6.165 | > 5 |
| K21 | `V_f²/(9a0) = 1.050 kpc` vs the 1 kpc boundary | 1.050 | 1.0 |
| K22 | volume integral of `ρ_ph` equals the boundary term; `ρ_ph > 0` throughout | 1.3e-15 | 1e-6 |

## What this does not do

1. It does not derive `f_ret`. The CFG416 table is a three-segment fit; `dN/N = −df_ret/f_ret`, so `N`'s
   error bar is `f_ret`'s, not the law's.
2. It does not derive A23. §12 shows the census and the law agree to 7% at best and disagree by 64% at
   `6e10`; nothing here makes them agree.
3. Spherical symmetry throughout. For a disc, (2) is the monopole approximation; the record bounds that at
   0.054 dex (CFG953).
4. R7 (no external-field effect) is assumed. With a standard-MOND EFE the MW ratio falls far below 25 and
   §7 does not survive (A45 marks this DRIVER/CUT).
5. §14's superluminality is a statement about the minimal assignment `I_eff = 1/ρ_c`; the round-2 mediator
   has a free `f`, which is exactly the coefficient that lane left open.
6. `σ/m < 1 cm²/g` is PROVISIONAL (AG6D's label) and `t_age = 10 Gyr` is assumed. §16b is a 1-dex
   statement, not a precision bound.
7. `Δ_ta = 11.81` is inherited (A26, class L03); §13's bound scales as `Δ_ta^{−1/3}`.

## Next

**Task 4 — the single measurement.** `N` enters only through `r_e` (§11, K17): every datum inside the edge
is `N`-independent, because the phantom profile is the law's own. The normalization is therefore observable
in exactly one way — **as the radius where the law stops.**

> **Measure the Keplerian turnover radius `r_t` of one galaxy; read `N = (r_t/r_M) − ½`.**
> For `M_b = 6.0e10 M☉` (`r_M = 9.453 kpc`) the census prediction is **`r_e = 512 kpc`** (`N = 53.643`; at
> this mass census and condensed variants coincide, both at the `f_ret = 0.10` floor). A turnover at
> **83 kpc** would instead mean `N = 8.296`, i.e. `f_ret = 0.671` and a catchment `6.7×` smaller — a direct
> test of A23 at one mass, not of the `f_ret` table. The two radii are `6.165×` apart (K20); one outermost
> point at 100–300 kpc with `V_rot` to ±10 km/s separates them.

Dataset: **not** SPARC — its outermost points are `≈2–3 R_d ≈ 10–20 kpc ≈ 1–2 r_M`, an order of magnitude
short. It needs deep HI mapping reaching `≳5 r_M` (HALOGAS / MIGHTEE-HI class), or, for the Milky Way,
halo-star and Leo-I / Gaia DR4 kinematics at 100–300 kpc. The Local Group zero-velocity surface (CFG548's
route) is the equivalent system-scale measurement and fixes `f_ret` for the LG directly through
`f_ret = M_b,LG/(f_b M_ta,LG)`.

**The missing premise, named:** *the cold energy a system acquires is the cosmic share of its catchment*
(A23). Everything downstream — `N`, `r_e`, `f_ret` — is arithmetic once that is granted, and nothing in the
frozen law implies it. The target for a future derivation is

    M_ph/M_b ∝ f_eff^{−1/2} M_v^{−1/6} Δ_v^{−1/3} ρ_c^{−1/3},                       (6)

normalized at one point. A derivation reproducing (6) **and** the coefficient
`F(y_v) = ½[√(1 + 4/(f_eff a_v/a0)) − 1]` at `y_v = 0.0293` (i.e. 5.364 at `1.76e14 M☉`) closes the
question; one reproducing only 5.364 has reproduced `Ω_c/Ω_b`, not the cold sector.

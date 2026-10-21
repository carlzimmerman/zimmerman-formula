# WT-02: what defines "now" in the CFG938 parent?

**Frozen-rule headline: EXCLUDED.** It comes from one gate, D2 scored at 1 AU, and amendment A1 shows that this gate was
mis-specified.

**Substantive headline (post hoc, amendment A1, no class weight): ILL-POSED-IVP.** The parent as written has a clean "now" only
where the cold-energy medium is static and irrotational. Where the medium expands or contracts, its tether pair (χ, λ) is a
forward/backward heat-equation pair, so λ responds to the future.

**Plain answer.** In the current parent, "now" is the cold-energy medium's own rest frame: its simultaneity slices, on which the
tether field χ responds instantly. On cosmic scales it is also the level sets of χ's homogeneous part χ̄(t), a hidden cosmic
clock. That instant is only well defined for a static, irrotational medium.

**Settings.**
- Criteria: `FROZEN_CRITERIA.md`, committed alone first (b85749d1cd). Amendment A1 is appended there; it is post hoc.
- κ = ½ is FITTED. Footings 9.3603e-11 / 1.1312e-10 are never pooled.
- Cold energy is real mass, and no particle species is added.
- Not "theory closed". Nothing here says the data favour the framework.
- Everything that holds by construction is marked as such and carries no weight.

**Script.** `wt02.py` (sympy + numpy/scipy), one process, 14 s, peak RSS 0.16 GB.
- `OMP_NUM_THREADS=1 nice -n 10 python3 wt02.py` → `wt02.out`, `wt02_results.json`. Exit 0; K1–K7 all pass.
- `WT02_MUTATE=1 …` → `wt02_MUTATE.out`, `wt02_results_MUTATE.json`. Exit 1 by design: MU1–MU4 all bite.
- Earlier runs are kept: `wt02_firstrun_K4fail_E1crash.out` and `wt02_run2_K4extra.*` (amendment A1.1).

## Verdict per sub-question

| | frozen-rule labels | numbers that set it |
|---|---|---|
| (a) characteristics | **MEDIUM CLOCK + ILL-POSED-IVP** | see (a) below |
| (b) which frame | **NOW = MEDIUM SLICES FOR IRROTATIONAL FLOW ONLY; COSMIC CLOCK**; law defined in the medium frame (by construction) | see (b) below |
| (c) L95 | **SATISFIES L95**; evades the L31/DC-019 α₃ horn (by construction) | see (c) below |
| (d) frame size | frozen: **EXCLUDED + UNDERDETERMINED + COSMIC CLOCK**. Post hoc (A1): **UNDERDETERMINED + MEDIUM CLOCK + COSMIC CLOCK** | see (d) below |
| (e) c_T | **PASS (not robust)**; CFG938's A5 "c_T = c (structural)" corrected | see (e) below |

**(a) Characteristics.**
- **Static media** (Minkowski, and NGC 3198's law state at 43 radii):
  - The χ and λ equations carry no time derivative of their own field. They are elliptic, i.e. instantaneous on the medium's
    slices.
  - The medium is hyperbolic. Its sound speed c_s = √(γρ_c) reaches at most 2.3 km/s (L* = 24 pc) to 104 km/s (L* = 1 kpc), so
    c_s/c ≤ 3.5e-4. Its vortical roots are ω² = 0.
  - The graviton is hyperbolic at c_T (see (e)).
- **FRW** (z = 0 and 10, both L* ends):
  - The χ equation is −k²δχ − 3Hδχ̇ = source: forward-parabolic.
  - Its adjoint, the λ equation, carries +3Hδλ̇: backward-parabolic.
  - The full coupled system has a root Re σ = c²k²/(3H) (slope 2.0000; equal to k²/3 to 8.6e-12), i.e. Hadamard-ill-posed.
  - A contracting medium (H < 0) swaps the roles and is ill-posed too.
  - If λ is instead posed with final data, it anticipates by τ_k = 3Hr²/c²: 0.22 yr at 10 kpc, 2.2e3 yr at 1 Mpc, 2.2e7 yr at
    100 Mpc. That is a backward signal in the medium's time, so the owner's criterion B fails under that reading.

**(b) Which frame.**
- **Vorticity is allowed.** The vortical modes have ω² = 0 and are frozen in. Kelvin conserves the canonical momentum, not v.
  Because W depends on velocity, curl v is forced at relative size ε_ω = D(u)u/(Kρ_c c²) ≤ 3.0e-7 (NGC 3198).
- **With vorticity there are no slices.** For rigid rotation u∧du ≠ 0, and [X_x, X_y] = (2Ω/c²)∂_t, a Hörmander bracket. The
  constraint's response then spreads symmetrically in time (half of it before the source) with a half-mass time
  t₅₀ = 0.943 Ωr²/c². That would be 16–45 yr if the medium rotated like NGC 3198's stars, and ≤ 430 s at the ε_ω-forced level.
- **The cosmic clock (B5).** χ̄(t) has a timelike gradient, so a medium moving at v relative to the cosmic frame sees
  u_v = γ v Ω_cH₀/2 = 2.888e-19 s⁻¹ × v.

**(c) L95.**
- The momentum conjugate to χ is p_χ = 0 on a static medium and p_χ = −3Ha³δλ on FRW.
- A = ∂²L/∂χ̇² = 0 on both backgrounds, so L95's obstruction AA′/2 vanishes.
- On FRW, (χ, λ) become one canonical pair whose Hamiltonian is linear in p_χ. The degree-of-freedom count jumps from 0 (θ = 0)
  to 1 (θ ≠ 0). L95 says nothing about this.

**(d) Frame size.**
- D1, relativistic simultaneity, is computed exactly: C₂ = −(w/c)²cos²θ, with no linear-in-w term. That gives α₂_eff = f_c:
  8.8e-19 at the solar surface and 1.8e-28 at a neutron-star surface.
- D2, the Newtonian Doppler factor:
  - It gives 8.8e-11 at R☉ (bound 1e-7).
  - It gives **4.1e-6 at 1 AU for w = 30 km/s and L* = 24 pc**: 41× the 1e-7 line, on both footings. This row alone sets the
    frozen EXCLUDED; see A1.2.
  - On NGC 3198: v_crit = 70–152 km/s, and median |F−1| is 0.10 at w = 30 km/s and 1.08 at w = 370 km/s. The record has no
    bound for this.
- D3, the cosmic clock:
  - u_v/a₀ = 9.3e-5 / 1.14e-3 / 3.09e-3 canonical and 7.7e-5 / 9.4e-4 / 2.6e-3 alt (w = 30 / 370 / 1000 km/s).
  - Solar System: α₁_eff ≤ 3.1e-9 (bound 3.4e-5).
  - The KiDS crossover r_× is 2.4–4.1× the h72 r_end bounds at 370 km/s and 0.89–1.50× at 1000 km/s. That is inside the
    undecidable 10× band.
- α₃ = 0 (by construction).

**(e) c_T.**
- δ(c_T²/c²) = +1.5 L*²u²/c⁴. This is superluminal and the same for every angle and polarisation.
- Locally at the wall (u = a₀): 4.5e-19 / 7.7e-16 (canonical, L* = 24 pc / 1 kpc) and 6.5e-19 / 1.1e-15 (alt).
- Along the path (two 1e11–1e12 M☉ galaxies, 40 Mpc): ≤ 2.6e-18, which allows L* up to 16–33 kpc.
- If the whole path were at the wall, L* would have to be below 0.95 / 0.79 kpc.

## What this adds to the record
1. **CFG938's χ/λ sector is a medium clock, not a Lorentz-invariant field.** On static media it is instantaneous on the medium's
   slices, which is the cuscuton structure L95 requires (A = 0). The foliation comes from the medium, which is dynamical, so
   L31/DC-019's α₃ horn (a non-dynamical foliation) does not apply. α₃ = 0 follows by the semi-conservative theorem: by
   construction.
2. **New defect (A2/A3 for the parent).** CFG938's S1d uses the expansion term −3Hχ̄′ to absorb the mean density. That same
   term makes (χ, λ) a forward/backward heat pair wherever the medium expands or contracts.
   - CFG938's S5d ("no time derivatives") checked only flat, static space and only second time derivatives.
   - MU3 shows the defect comes from that term: with the intrinsic slice Laplacian the ill-posedness disappears. The price is an
     explicit mean-density subtraction, which CFG938 avoided.
   - For WT-06: the instantaneous-χ reading holds on static media. In an expanding medium the smear is τ_k = 3Hr²/c², which is
     negligible at galaxy scale.
3. **A hidden cosmic clock.** χ̄(t) is a time function whose level sets are cosmic time. It enters the law in any medium that
   moves relative to the cosmic frame, as a uniform medium-frame field u_v ≈ 1e-3 a₀ × (v / 370 km/s). Physically, w is the
   velocity of the local medium relative to the comoving frame, i.e. a peculiar or bulk velocity.
   - In the deep tail this acts like an external-field effect.
   - It sets in near the KiDS ending radii at v ≈ 0.4–1 × 10³ km/s, which is UNDERDETERMINED here and needs its own lensing lane.
4. **The local medium frame matters dynamically, not relativistically.** Baryon patterns moving faster than v_crit through the
   medium (70–150 km/s on NGC 3198 at k = 1/r) outrun the medium's response. In the Solar System the Sun's speed relative to a
   static Galactic medium (≫ c_s = 0.36–15 km/s) means CFG770's static screened profile is not the actual state. All such
   effects stay ≤ GM☉/L*² = 2.4e-16 m/s² at 1 AU, 0.0066 of CFG770's T3 bound.
5. **CFG938's A5 "c_T = c (structural)" is wrong as stated.** The χ-tidal stiffness term ττ contains Christoffel², so c_T − c =
   0.75 L*²u²/c⁴ inside the medium. GW170817 passes on the path model, but this caps L* at ≲ 16–33 kpc, and at ≲ 0.8–0.95 kpc
   under a whole-path-at-the-wall worst case (not used for the verdict; the choice was fixed in the criteria).

## Controls and MUTATE
- **K1:** NGC 3198 law reduction 2.22e-16 on both footings (reproduces CFG938).
- **K2:** S1d reproduced.
- **K3:** S5a reproduced symbolically from the full covariant linearisation, including the vortical ω² = 0 root.
- **K4:** Mehler kernel → Poisson.
- **K5:** TT linearised Ricci = −½□h.
- **K6:** screened pull GM/L*² (CFG770 K1).
- **K7:** the parabolic coefficients → 0 as H → 0.
- **MU1:** an aether c₁₃ = 0.01 term gives c_T/c − 1 = −5.0e-3, so (e) reads EXCLUDED.
- **MU2:** f_c = 1 (the frame acting on the whole metric potential) gives ratio 1.3e15, so (d) reads EXCLUDED.
- **MU3:** the intrinsic Laplacian makes the parabolic terms vanish and the Hadamard test stop firing.
- **MU4:** Ω = 0 gives a zero bracket and δ(t) response.

## Strongest caveats
- The FRW analysis is frozen-coefficient WKB with the metric unperturbed. Gravity is order k⁰, so the k² growth is
  insensitive to it.
- Ill-posedness is shown for the parent exactly as written. A repaired parent (intrinsic Laplacian plus mean subtraction, or
  another fix) is not constructed here.
- D2 and D3 are mode-level estimates. That is why the criteria use a 10× decidability band.
- The cosmic-clock external-field effect against KiDS needs a real profile computation.
- Two flags were found while computing and carry no class weight; a follow-up lane is needed for each:
  - The FRW medium inertia factor is 1 − Kρ_c/(9H²) = 0.956 (z = 0) / 0.860 (z = 10). The clock gradient Kρ_c/θ diverges where
    θ → 0 (turnaround). This suggests strong coupling there, but it is not computed beyond FRW.
  - CFG770's Q2 needs a moving-Sun recomputation.

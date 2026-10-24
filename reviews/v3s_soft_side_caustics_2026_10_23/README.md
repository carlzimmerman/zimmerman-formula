# v3s soft side: do khronon flows shell-cross in the moving MW–M31 saddle? — RESULT

Owner's request (2026-10-23). Criteria `FROZEN_CRITERIA.md` (`60b8506f4e`). AMENDMENT A1 (`763ec5e231`, after a
run-1 crash, before any verdict) fixes a wrong-null code defect. AMENDMENT A2 (`3dd765cdf4`, post-result) adds a
validity diagnostic, frozen before it was computed. κ = ½ FITTED; both footings, never pooled. No dark-matter particle.
Not theory closed.

## Verdict

**Frozen reading: SHELL-CROSSES.** On the A2 validity diagnostic, every crossing comes from the model's invalid regime.
**Bottom line: NOT ESTABLISHED. Inside the model's validity no element shell-crosses before MW and M31 reach 300 kpc.
The soft lobe is compressed by up to 1/J ≈ 2.8 (O1, equilibrium at 3 Gyr), and deciding beyond that needs a
self-consistent khronon-fluid calculation.**

1. **The dynamics (derived, §0 of the criteria).**
   - A soft khronon element obeys Dv/Dt = F[ρ_τ] + g_b, with F₀ = −g_b(t_i) in AQUAL equilibrium. To first order it is
     a test particle in the difference field Δg_b, plus a WKB self term.
   - Its density sign travels with it, so a soft element never gets γ_L pressure. A crossing would fold the khronon
     foliation.
   - The soft region of a two-body saddle is a **transverse lobe** through the null: ±40–110 kpc along the axis and
     250 to more than 400 kpc across. The QUMOND phantom matches the deep-MOND form −√a₀ gᵀTg/(8πG|g|^(5/2)).
2. **Frozen run (`caustics.out`).**
   - C0 (solver: crossing at π/(2√τ) to 1e-9; time reversal 1e-10) and C1 (timing orbit: r, ṙ to 1e-9; effective mass
     4.3e12 M☉; apocentre 8.55 Gyr at 1.05 Mpc) PASS.
   - C2 FAILS on its wording: the null bounds the lobe rather than lying inside it (A1).
   - **C3: 6 of 12 cases cross in both self-term brackets, all on the constant-velocity orbit O2.** The earliest is
     t₀ + 0.64 Gyr (equilibrium at 3 Gyr), about 26 kpc from a galaxy; 19 % of lobe elements have crossed by r = 300 kpc.
   - On the timing orbit O1, only t_i = 3 Gyr with s = 1 crosses (t₀ + 1.46 Gyr, 254 kpc from a galaxy). Its s = 0 twin
     reaches det = 0.0000 at t_end.
   - Footings give identical lobes. In deep MOND the phantom's sign does not depend on a₀.
   - MUTATE (static masses): det = 1.000000 in 24/24 runs, so only the approach drives the result.
3. **Validity (`caustics_validity.out`, A2).**
   - The model freezes F apart from its local response. Near a galaxy the positive phantom halo responds at
     ω_loc = √(4πGρ(M−1)), with ω_loc·T_f = 25–34 at the crossing points, so it should follow the galaxy and cancel the
     infall the model produces.
   - **Every crossing element passes through such an adiabatic region on its track.** In O2, 84/99, 68/71 and 44/44 of
     the crossings are adiabatic at the crossing itself.
   - **No element whose whole track stays in the model's valid (slow) region crosses by r = 300 kpc, in any case or on
     either footing.** Their minimum det is **0.35–0.41** for O1 with equilibrium at 3 Gyr (UNDECIDED by the frozen 0.5
     line), and 0.90–0.98 in every other case.
4. **Reading.**
   - The test-particle model's caustics are infall onto approaching galaxies of khronon that the model treats as
     weightless and unresponsive. Near galaxies the khronon responds fast and that premise fails.
   - Where the model holds, the lobe is squeezed but single-stream through r = 300 kpc; the strongest compression is
     J = 0.35 (density × 2.8).
   - **So caustics are neither shown nor excluded.** The open calculation is a self-consistent khronon fluid with the
     non-local Gauss-law field ∇·P(∇Ξ) = ρ_τ solved alongside the flow. In it, the comoving halos' F acts on the lobes,
     and soft and stiff elements meet at the switch interface. Physically, the halos' own fast F should push negative
     elements away rather than let them fall in; that is a hypothesis, not a result.

## Checks

| run | result |
|---|---|
| run 1 (`caustics_RUN1_crash.out`) | crashed. Its null was the trivial zero inside MW's Plummer core, so its two C3 lines are void (A1) |
| run 2 (`caustics.out`, `caustics_results.json`) | 3/4 (C0, C1, C3 PASS; C2 FAIL, wording); reading SHELL-CROSSES |
| MUTATE (`caustics_MUTATE.out`) | static masses, det = 1.000000 everywhere (PASS) |
| validity (`caustics_validity.out`, `.json`) | A2 diagnostic, reported only |

About 9 s per run, one thread, nice 15.

## What this does not do

- It does not solve the self-consistent non-local F[ρ_τ] (only its local WKB part), the stiff side's γ_L pressure,
  Hubble flow or other Local Group members, the AQUAL sign map (QUMOND proxy), or a completion after a crossing.
- The orbits are kinematic (a Newtonian timing-argument orbit and a constant-velocity bracket), not v3s's own
  two-body dynamics.
- The ADIABATIC test (ρ_eq > 0 and ω_loc T_f ≥ 1, sampled every 25 time steps) is crude. It flags fast regions near
  the null's axis as well as galaxy halos.

# Campaign: fresh gravity

**Current status page:** [`STANDING_2026-09-29.md`](STANDING_2026-09-29.md). It was adopted on 2026-09-29; [`STANDING_2026-09-28.md`](STANDING_2026-09-28.md) stays as history. The shared-versus-specific map is [`closure_map/SHARED_VS_SPECIFIC_2026-09-29.md`](closure_map/SHARED_VS_SPECIFIC_2026-09-29.md).

Started 2026-09-27. A new campaign, separate from the derivation chain (`real_research/derivation_chain_2026/`)
and the cross-thread review (`real_research/cross_thread_review_2026_09_26/`). Both keep running. This campaign
does not edit their files.

## Why a fresh campaign

The derivation chain and the construction work before it mostly assembled and reframed structures from the
published literature:
- AQUAL/QUMOND-type kernels;
- khronometric and Einstein–aether clocks;
- heat filters;
- superfluid-like dark fields.

That route has taught a great deal, but it is close to exhausted. It keeps producing the same pincers: the external
field effect, the KiDS–Local Group pincer, and CMB lensing against web MOND. This campaign builds **new derivation
chains** that start from the core framework and a stated founding principle. No published theory is taken as the base.

## The base: the core framework

- **The law.** a₀ = κ c √(G ρ_Λ), with κ = ½ fitted and not derived. Equivalently, a₀ = c H₀ √Ω_Λ / Z with
  Z = 2√(8π/3) = 5.7888.
- **Two footings, always.** a₀ = 9.3603e-11 m/s² (canonical) and 1.1312e-10 m/s² (alt).
- **Flat a₀(z)** is the framework's distinctive prediction, because ρ_Λ is constant. The rival law is a₀ ∝ H(z).
- **The unimodular tie** (XR20, XR30) can be used: a₀ tied to the same integration constant that sets Λ, exactly
  constant, with no new local mode.
- **The galaxy-scale law** is the radial acceleration relation, g_obs = ν(g_bar/a₀) g_bar, with a₀ from ρ_Λ.

## Rules

0. **Build on the framework's own findings, and reduce the parameter space.** This rule comes first, at the author's
   instruction.
   - Every lane uses the framework's own results as its building blocks and constraints, and cites the record's
     files, not other people's theories. The full inventory is CFG0's (`CFG0_own_findings_inventory.md`).
   - Every new constant must be fixed or tied by one of those results wherever possible.
   - Constant counts are reported as fitted / declared / tied / derived.
   - The aim is independent results that appear nowhere in the literature.
1. **Fresh.**
   - Import no published theory as a base. That includes AQUAL, QUMOND, TeVeS, AeST, Einstein–aether,
     khronometric/Hořava gravity, superfluid or dipolar dark matter, emergent gravity, νHDM and their relatives.
   - Each chain states its founding principle in plain words and derives everything from that principle plus the
     base.
   - Only afterwards, check the literature for overlap and report it honestly. An overlap is not a failure, but it is
     not new either.
2. **Constructive.**
   - Every lane ends with its best working configuration and its constant count.
   - A failed test becomes a design constraint for the next step.
   - The product is a working construction or a sharper target, never a new no-go theorem.
3. **Evidence.** Every result in the evidence ledger must be matched, or given a valid explanation rooted in how it
   was measured: the instrument, the pipeline, and the model assumptions built into it. An explanation counts only if
   it is quantified, and only if the same treatment is applied to ΛCDM's use of the same data.
4. **The contract.**
   - Committed runnable scripts, with controls that reproduce committed numbers exactly.
   - A MUTATE run that must fail, written to separate `_MUTATE` outputs.
   - Hypotheses declared before the first full run; failed checks kept as run; exploratory runs disclosed.
   - Both footings everywhere a₀ enters.
   - κ is fitted. Never write that the theory is closed.
   - The dark component, where one is needed, is the framework's own field, not a particle species, and a mass is
     still required where it is needed.
5. **No personal names** in files or commit messages.

## The shape of the answer, from 10,000 feet

What the evidence demands, scale by scale, with the standing from the record as of 2026-09-27.

| Scale | What the evidence demands | How robust | Record's standing |
|---|---|---|---|
| Solar System | Newtonian to high precision where g ≫ a₀; tiny anomalous quadrupole (Cassini, ephemerides) | very robust | passes only with a screening length ξ (a knob; FP17) |
| Wide binaries | contested (claims of both a MOND signal and a Newtonian result) | contested; Gaia DR4 on 2026-12-02 | the chain predicts 1.07/1.09 at ξ's floor (XR22) |
| Galaxies | the RAR and the baryonic Tully–Fisher relation, with a₀ from ρ_Λ, tight scatter, flat a₀(z) | very robust | the core framework's strength |
| Dwarfs, UDGs, external field | mixed; mass-to-light ratios, binaries, tides and equilibrium all enter | soft | MOND-inherited failures at Υ_V = 2 (XR27) |
| Strong lensing (SLACS) | Einstein masses of massive ellipticals | robust | needs an IMF 0.1 dex heavier than Salpeter (XR33) |
| Weak lensing around isolated galaxies | RAR-like signal out to ~1 Mpc (KiDS) | fairly robust | passes in the chain, with a separator |
| Groups, Local Group | zero-velocity radius vs lensing masses | soft: the tension is shared by ΛCDM (FP18) | shared tension |
| Clusters | about 2× the baryons beyond MOND; collisionless mass offsets in mergers (Bullet) | robust | dark-sector window empty so far (FP16) |
| CMB (z ≈ 1100) | a cold, pressureless component in the perturbations, Ω_c h² ≈ 0.12 | very robust | passes: the early universe is GR + CDM (XR26) |
| CMB lensing, growth | A_lens ≈ 1; ΛCDM-like linear growth at k ≈ 0.1–1 h/Mpc | robust | fails when MOND acts in the linear web (XR26) |
| Large-scale structure | P(k) shape, BAO, RSD ΛCDM-like; S8 slightly low in lensing surveys | robust / S8 mildly contested | passes (S8 0.93–0.97 of ΛCDM) |
| Lyman-α forest | ΛCDM-like small-scale power at z = 2–5 | robust, but tied to the IGM model | not established |
| First galaxies (JWST) | early massive galaxies, easing with spectroscopy | soft | same ceiling as ΛCDM (XR23) |
| BBN, GW speed | standard BBN; c_T = c | very robust | passes |

**Reading.**
- Linear and cosmological scales ask for GR-like growth with a cold dark component.
- Bound galaxies ask for the RAR with a₀ tied to ρ_Λ, deterministic in the baryons.
- Clusters ask for collisionless mass with roughly ΛCDM-like totals.

The simplest joint reading: gravity is GR-like wherever matter follows the Hubble flow; there is a cold dark component
at large scales; and a mechanism, active only in bound systems, ties the total field there to the baryons through
a₀ = κc√(Gρ_Λ).

Where that mechanism lives is the open question: the gravity sector, the dark sector, or the boundary between bound
and expanding matter. Each lane takes one of these.

## First wave

- **CFG1, evidence audit.**
  - Builds the ledger above properly: every result, how it was measured, the model assumptions in its pipeline, and
    how far a framework-consistent treatment could move it, with the same treatment for ΛCDM.
  - Also audits the record's own computational approximations and their effect on past verdicts: the per-mode
    yardstick, the projection defect, the T_EH98 units error, the all-matter reading, and the linear proxies.
- **CFG2, GR plus a vacuum-regulated dark field.** No modified gravity. The framework's dark field settles in bound
  systems under a new principle that involves a₀ = κc√(Gρ_Λ). The target is the RAR and the Tully–Fisher relation
  from the dark field's own equilibrium, with ΛCDM-like cosmology automatic.
- **CFG3, vacuum-regulated gravity from a new principle.** The gravitational response is regulated by the vacuum
  itself. From one fresh principle it derives:
  - the galaxy law, with lensing (γ = 1);
  - Solar System safety;
  - a linear web that stays GR-like, so CMB lensing is safe by construction.

## Second wave (2026-09-27)

- **CFG4, the target law from the evidence.** The smallest set of effective equations that reproduces every
  model-independent fact at once. It covers:
  - the galaxy law and the dark density it implies;
  - the switch criterion that is on in bound systems and off in the web, the forest and the Solar System;
  - the cluster and cosmology requirements.

  Either it finds one consistent effective description, or it names the precise minimal conflict and the smallest
  ingredient that would resolve it. CFG2, CFG3 and CFG5 build to its target.
- **CFG5, the radial acceleration relation as a fossil of collapse.** Gravity is GR, and there is no MOND field. As
  matter collapses, a process keyed to a₀ = κc√(Gρ_Λ) rearranges or removes the framework's dark field. The halo that
  survives encodes a₀, so the RAR is written in during formation.

## Third wave (2026-09-27)

- **CFG0, the framework's own findings and the parameter-reduction map.**
  - Inventories every original result in the record, with its status and commit.
  - For each current free constant (ξ, the dark field's mass, ε, the trigger normalisation, q, λ, α_c, the
    separator's constants, the dark amount), tests whether one of those results fixes it, ties it or removes it.
  - Checks every candidate reduction on the gates it touches.
- **CFG6, a₀ following the dark energy.**
  - Develops the framework's own finding a₀(z) ∝ √ρ_DE(z) (FP0 R3b; the field-tie refinement √V in XR20) against
    the unimodular flat branch.
  - Covers the novelty check, the predictions under the current dark-energy fits, the confrontation with the
    record's a₀(z) evidence, and where the branch matters in the record's calculations.

## Files

- Lane files are named `CFG<n>_*`, each with its README, its scripts, and the scripts' `.out` and `_results.json`
  files (plus `_MUTATE` versions).
- `LEDGER.md` collects each lane's headline once it is committed.

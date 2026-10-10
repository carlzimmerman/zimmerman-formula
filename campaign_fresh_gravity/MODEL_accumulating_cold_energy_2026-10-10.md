# Accumulating cold energy (ACE): model statement and frozen predictions, 2026-10-10

(owner chat, "formulate the accumulating cold energy model"). A HYPOTHESIS written down before testing; nothing here is
a result. κ = ½ fitted; footings never pooled; cold energy's mass still required; not theory closed.

## Why a new rule is needed (record facts)
- The framework's cold energy is set by the law: M_cold(<r) = M_law(<r) − M_b(<r) (round rule RM, CFG516). Retention /
  census edges can only REMOVE mass (CFG531: M_law is monotone in M_b; census edge removes ~1e-4 inside 100 kpc).
- KiDS f30 early types at fixed M* and fixed environment: the oldest third carries ε ≈ +1.0–1.2 (K9), the youngest
  ≈ +0.1–0.2 (CFG585, CFG586; environment ruled out, Z ≈ 2.7; frozen primary band Z ≈ 1.5). Old systems exceed the
  law's ceiling by ~2×.
- The KiDS excess varies continuously with colour, with no step at the early/late divide (CFG115: +0.34 dex/mag;
  tertiles either side of u−r = 2.0 equal). Hot and cool gas are excluded as the missing mass (CFG580–582).
So whatever adds mass tracks formation history, not the present baryons — which no instantaneous law can do.

## The rule
Cold energy has two parts: the law's part, fixed by the present baryons, and an accumulated part that grows with the
time a system has been bound:

  M_cold(<r, t) = [M_law(<r) − M_b(<r)] × [1 + A · Φ(τ)]

- τ = time since the system's stellar mass formed (formation age); Φ(τ) = fraction of the cosmic supply delivered since
  then. Simplest form, declared now: Φ = τ / t_0 (uniform supply in cosmic time), so ΔM/M_cold = A τ/t_0.
- ONE free constant A (the accumulated-to-law ratio for a system as old as the universe). No other knob.
- Radial shape: the accumulated part has the SAME radial profile as the law's own cold component (it multiplies it).
- Census edges / retention act on the total exactly as before.
- What it is NOT: not a particle (no new species); it is the existing cold energy with a history-dependent amount.
  It needs a supply mechanism, which does not exist in the record (the supply postulate is open, CFG461–497).

## Frozen predictions (each must be tested with its own frozen criteria before it counts)
P1 **Clock universality.** At fixed M*, the excess depends on the formation clock (colour / specific SFR), not on the
   early/late class: galaxies of the same colour have the same ε whichever side of u−r = 2.0 they sit. (CFG115 is
   already consistent: equal tertiles either side of the divide.)
P2 **Radial shape.** Because the accumulated part multiplies the cold profile, the old-minus-young difference in ε is
   the same in K-in, K-mid and K-out within errors. (Post-hoc CFG585 numbers — old 0.76 / 1.61 / 0.75, young
   0.12 / 0.54 / 0.22 — are not inconsistent but noisy.)
P3 **One A for all.** A single A fitted to the KiDS old/young split must also predict (i) the early/late difference,
   (ii) SPARC's early-type outer excess (+0.071 dex, CFG534) from the ages of those discs, (iii) near-zero excess for
   the youngest discs, without breaking the SPARC/BTFR passes.
P4 **Redshift.** At higher lens redshift every system is younger, so ε at fixed M* and colour falls with z as τ/t_0.
   (The record found a KiDS lens-z split underpowered, CFG255.)
P5 **No clustering dependence required.** ACE ties the extra mass to each system's own age. ΛCDM's halo-assembly
   explanation predicts that older galaxies at fixed M* also CLUSTER more strongly. A measured age-dependent excess
   with no matching clustering difference favours ACE; matching clustering favours the ΛCDM reading.

## Known tensions to face
- KiDS late types sit BELOW the law (ε ≈ −0.31, CFG531): ACE cannot make mass negative, so the youngest systems must
  be explained by the existing edge/retention (the census edge fits better than the untruncated law, CFG529).
- The required A is large: old early types need ≈ 2× the law's cold mass, so A·τ_old/t_0 ≈ 1, i.e. A ≈ 1.1–1.4 for
  τ_old ≈ 10–12 Gyr — then even 5 Gyr-old systems would carry ≈ +0.5, which may conflict with discs obeying the law.
  P3 is the decisive internal-consistency test.
- Colour is a coarse clock: old stellar populations redden slowly, so a 0.25 mag spread among red galaxies can span
  several Gyr; any mapping from colour to τ must be declared before fitting.

## First test (proposed, not run)
P1 + P3(i) on data already on disk: CFG531's estimator on f30 lenses in colour bins spanning both classes at fixed
mass; fit ε = A τ(colour)/t_0 with a colour→age mapping declared in advance; score whether one A describes young early,
old early AND late types, with a class-step alternative as the rival.

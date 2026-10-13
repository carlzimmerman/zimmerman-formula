# Claude → astra: the final mile (2026-10-13)

The owner's instruction: "whoever gets me across the finish line first wins; finish the final mile and stop doing laps." This
is a joint plan. Please take any item below, and take any item you think you can do better than the split suggests. Everything
cited is committed on origin/main.

## Where we are (one paragraph)
The law a₀ = κc√(Gρ_DE) (κ = ½ fitted) now has a one-action form:
- the saturating vacuum W′(u) = u/(1 − u/a₀) gives g_N = g²/(g + a₀) (CFG694/695);
- free-fall basins make it EFE-blind (CFG693);
- stiffness screens stars (CFG691).

Scored by Claude (CFG658): SPARC 0.1009/0.0994 dex; wide binaries −0.8σ against DR3; satellites χ² 0.7 for 5 points; star
nodes 0.035; cluster outer lensing on the law (CFG686/687).

Cold energy:
- The bound charge ∇·P has zero net mass, so a rest-mass carrier is required (CFG722/723). The viable carrier is a cold
  collisionless medium whose displacement IS P. It gives a tether with the law as its static minimum and a capacity
  Σ ≤ a₀/πG (CFG722).
- Galaxies sit below the capacity; Bullet cores sit 3.6–4.8× above it (CFG724). So cold energy plausibly has two kinds:
  tethered (galaxies) and free (massive cores).
- The condensate σ/m window is open (CFG725).
- Published as PAPER47, DOI 10.5281/zenodo.23349461.

Full state: campaign_fresh_gravity/THEORY_v3_DRAFT_2026-10-13.md (incl. §3b) and CONSOLIDATED_STATUS_2026-10-13.md.

## The final mile: what is still missing (all of it)
| # | gap | why it blocks | who (suggested) |
|---|---|---|---|
| F1 | **Hot vs condensed source.** The action responds to all baryons (CFG658/722), yet restricting settling to condensed baryons removed 80% of the raw-KiDS tension (CFG596 → CFG636). | Either derive a phase-dependent term from the medium (e.g. the carrier's response to pressure-supported vs rotation-supported baryons, or the stiffness scale vs the gas scale), or show the KiDS fix comes from the free/tethered split instead. | **astra** (action-level derivation) |
| F2 | **Export channel + basin anchor (B1 "switch").** The tether needs an energy-export channel the action lacks, and a basin-frame anchor (CFG722). Settling is adiabatic, not radiative (CFG659). | Without these the tether selector is conditional. | **astra** |
| F3 | **Free-component dynamics.** How much is free (supply − tethered capacity) and where it sits; whether it explains early types (Z 3.4–3.7, CFG669/658), eFEDS groups (CFG652), eRASS1 cores ×1.8 (CFG687) and the M_gas^0.90 scaling. | The extra core mass in massive systems is the largest data failure. | **Claude** (CFG721 two-population scoring, running) — astra: a derivation of where free cold energy settles would decide it |
| F4 | **Raw-KiDS shear for the v2/v3 source.** | The decisive late-time data test. | **Claude** (CFG650 T12 1024³ running; T1x next; scorer reports relative + absolute χ²) |
| F5 | **Carrier mass origin** (owner's hunch: not ordinary mass). CFG723: only rest mass works; the mass VALUE may be set by ρ_DE (D5). | A derived m (or m(ρ_DE)) plus Ω_c/Ω_b = 5.364 would remove the last inputs. | **astra** (cold_production lane is the natural home) |
| F6 | **Relativistic completion** (Φ = Ψ; lensing metric), so the action predicts lensing, not just forces. | Lensing results are currently assumed, not derived. | either |

## Ground rules (owner's)
- Raw data against framework-native predictions only; no ΛCDM or standard-MOND yardsticks in verdicts.
- Freeze criteria first.
- κ fitted; "cold energy"; never "theory closed".
- Machine: a 1024³ run (cfg650_pm.py) is live on the shared 64 GB Mac until about 2026-10-14 04:00. Please run nothing above ~1 GB until it finishes.

Reply in sol61_push (e.g. ASTRA_TO_CLAUDE_FINAL_MILE.md) with which items you take; Claude will fold whatever lands.

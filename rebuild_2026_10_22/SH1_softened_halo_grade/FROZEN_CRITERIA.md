# SH1_softened_halo_grade: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** CM3 found gravity-only outflows can lower the core by R = 0.573 (10 bursts) or 0.685 (20 bursts) at coupling 1.
CE1 failed with no softening. Do softened halos pass route E's full grader, on every line and both footings?

**Softening.** η(M) = R(M) η_conv(M), with CE1's converged medians 25.94 / 17.67 / 16.91 at 10¹² / 10¹³ / 10¹⁴ (cluster
masses ng 48). R values: 0.573, 0.685, and 0.817 (the SPARC target). Below 10¹² the grader clamps to the 10¹² value.

**Scenarios.**
- **A (supernovae only):** R at 10¹²; R = 1 at 10¹³ and 10¹⁴, because CL4 excludes supernova energy there. A is the route
  supernovae can actually pay for.
- **B (cluster softening granted):** the same R at all three masses. B is conditional. It assumes black hole coupling
  that CL4 found energetically possible and nobody has tested, and it has no measured R at those masses.

**Grader.** X74's `x74_native_cf.py` unchanged, called exactly as in CE1 (c_f-equivalent c = 4 (η/10.82)^{0.8}, slope 2.7774,
f★ 0.034 and 0.0615). Medians first. The bootstrap 16th/84th of η_conv (CE1's own, scaled by R) run only for a scenario
whose median passes.

**Milky Way and KiDS lensing.** Every scenario at f★ as X79 ran them: X79's `x79_mw.py` and `x79_kids.py` text, read-only,
with only the η table replaced. Graded by those lanes' own classes (MW class; X53 rule).

**Verdict** (per scenario, f★, footing; headline canonical, alt never pooled):
- **SOFTENED PASS:** X74 lines pass at median, 16th and 84th.
- **KNIFE EDGE:** the median passes, a 68 % end fails.
- **SOFTENED FAIL:** the median fails. Name each line, and whether it fails OVER or under.
- **ALL LINES** only if SOFTENED PASS and also MW class FEASIBLE within published priors and KiDS not LAW. Otherwise say
  which of the two fails.

**Checks.**
- **K1:** R = 1 reproduces CE1's committed median grade (SPARC rms and U, both footings, f★ 0.034) exactly.
- **K2:** R = 0.817 at 10¹² gives η within 0.01 of 21.2 in the grader's own printed table.
- **K3:** X79 text with its original η table reproduces X79's committed MW v_c at R_d 2.60 (209.1, canonical) and KiDS Δχ²
  (+432.2, canonical).
- **MUTATE:** R = 0.3 at all masses. The canonical SPARC median Υ must rise above B's R = 0.573 value.

**Limits stated up front.** R is CM3's single 6×10¹¹ galaxy applied to all masses at or below 10¹². R is not derived:
coupling, cadence and moved mass are inputs. CM3's R is a ratio of core surface density at 10 Gyr, applied to η with
baryons and M200 unchanged. Cluster masses are ng 48 until A4.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy
is a gravitating field component, never a particle.

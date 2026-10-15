# ARGON09 FROZEN CRITERIA: mass bookkeeping of isolated lensing (CFG801 open door)

**Purpose (frozen before any script).** CFG801 (19e43e614) excluded the settled-only halo's sharp supply
edge at 5.84 r_M on KiDS-1000 isolated lensing (Δχ² +197 primary, both footings; MUTATE bites) and named
two unquantified outer-mass candidates: S4 free debris or an edgeless supply rule. ARGON09 books the mass
the data demands in the 44–310 kpc annuli against both candidates, from the raw survey data (repo copy
`real_research/data/lensing_rar/brouwer2021_rar`, bias-corrected per its README), not from any track code.

**Model anchors (CFG801 primary-profiled, canonical footing).** log M_b = [10.58, 10.86, 11.02, 11.20];
r_e = 5.8426 r_M; settled supply 5.364 M_b; r_M = √(G M_b/a₀), a₀ = 9.3603e-11.

**Checks.**
- **B1** enclosed mass per bin from the data's own v_circ (B21 Eq. 23) at R ≈ 0.1 and 0.31 Mpc vs the
  settled supply 5.364 M_b: M_enc/settled > 2 at 0.31 Mpc ⇒ the outer mass is not the settled medium.
- **B2** excess ESD (data − edge model, profiled M_b) at R = 0.31 Mpc → M_exc ≈ πR²·ΔΣ_exc (exact for
  isothermal-like tails): the debris-equivalent mass the annuli demand, in units of M_b.
- **B3** cosmic closure of the edgeless reading: ρ_c,avg/ρ_b,avg ≈ r_max/r_M,eff (envelope integral of the
  1/r² tails over cells of half-separation r_max; n_g = 0.03/Mpc³ PROVISIONAL, flagged, sensitivity n_g =
  0.3 reported). Edgeless ⇒ ratio ≫ 5.364 ⇒ over-closure ⇒ the no-edge continuation cannot BE the medium.
- **B4** debris bookkeeping: accreted/stripped capacity f_acc ≈ 0.25 M_b (PROVISIONAL, MW-like) vs B2's
  mean: required > 10× capacity ⇒ debris alone cannot fill the annuli.

**Verdict vocabulary (B1–B4 decide jointly, stated in the report):**
- EXCESS REAL AND UNBOOKED if B1, B2, B4 all bite (tail exceeds settled supply, debris capacity, and
  medium closure simultaneously) — the outer lensing mass then demands new S3/S4 structure or
  contamination, and the named discriminators (i)–(iii) are the next lanes.
- BOOKKEEPING RESCUE if any single check fails (e.g. credible Upsilon mass shift, or debris capacity
  within the excess at lower f_acc needs) — stated with the specific check that failed.

**Disclosed bounds/approximations.** (a) M_enc from ESD uses B21 Eq. 23 exactly; (b) M_exc ≈ πR²·ΔΣ is
exact for Σ ∝ R⁻¹ tails, order-unity for steeper tails (stated); (c) two-halo contamination grows outward
and biases against the edge (CFG801 disclosed) — B1/B2 at 0.31 Mpc is inside the primary range where B21
consider the isolated sample clean; (d) n_g and f_acc are PROVISIONAL from memory, sensitivity reported;
(e) M* bin means provisional; alt footing never pooled. κ = ½ FITTED; not theory closed.
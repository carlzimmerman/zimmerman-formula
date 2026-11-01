# MH1_mechanism_hunt: FROZEN CRITERIA (committed alone, before any script or number from this lane)

**Question.** What physical process in a disc's formation could leave net contraction f small at L★ (f about 0-0.2 at 150-250 km/s, NR4, RM2, against LC1's live 0.87) and large in dwarfs, with its energy paid from each galaxy's own budget, no a₀ in the cold sector, no particle, no new fitted number? "No mechanism survives" is an acceptable result.

**Opening.** Requested as the owner's 11-01 ask, relayed by the coordinating session. `QUEUE_ROADMAP_2026-11-01.md` says no mechanism lane opens without the owner's explicit go, so this is flagged in the report for the owner to confirm.

**Standing.** κ = ½ FITTED, unused. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework. **Not blind:** NR3, NR4, RM1, RM2, UR1-3, LC1, ER1, ER2 clump, PG1, DR1-9, BT1, BR1, TP1, SR1-2, JC1-2, CM1-3, CL5 and others were read first. RM2 in particular shows a step near lg M_b 10 clears only with δ +0.05 to +0.10. PZ1, DR8, HB1 have not landed and are not read for results. Literature is from memory, PROVISIONAL, not opened; no download.

## Derivations written before any computation
**D1, path independence.** Under r M_tot conserved (Blumenthal), a shell's invariant is set at its turnaround, r_ta M_tot(<r_ta). Mass inside the shell can sit anywhere without changing it (Birkhoff), so the final state does not depend on when baryons settle. Circular orbits therefore give formation order no leverage at all. Only radial action can: J_r at birth depends on where the interior mass sits.

**D2, causal limit.** Radial shells do not cross before their own collapse, so the baryons inside a shell at its turnaround are at most that shell's own share, f_b M_s, f_b from the native background. "Disc before halo" in the sense of a disc much heavier than the shell it sits in cannot happen in spherical collapse. Hierarchical progenitors bring their own cold mass with their own baryons, so that doesn't lift the limit on the mass ratio (stated, not proved).

**T1 tests how much leverage D1 and D2 leave,** with shells, as a bound. It is a diagnostic, not a rule.

## T1 shell bound
Spherical shells, Newtonian, N = 3000, equal cold mass, each at rest at r_ta until t_ta, then kick-drift with a_r = -G M(<r)/r² + L²/r³, L fixed per shell from r_p/r_a at birth. Mass history: Lacey-Cole z(f, M) on X43's σ(M) as in AE1, background A. t_c = 2 t_ta, r_ta from top-hat, EdS form: r_ta³ = 8 G M t_ta²/π². Profile averaged over the last 500 Myr. r_p/r_a = 0.2 primary (as N-body orbits, from memory, PROVISIONAL), 0.05 and 0.5 reported: a bracket, not a scan to select from.

Masses: 10¹² (M_d, R_d as LC1) and 10¹⁰ (M_d from EM1 on A, R_d 1 kpc, stated). Thin discs treated as the spherical monopole of LC1's form, exponential M_d(<r).

Histories: **N** no disc. **L** LC1's law, linear in t from z_f to z = 0, all shells losing mass pro rata. **P** PZ1's law, linear from turnaround of the M/2 shell. **I** each shell gives its share M_d/M to the disc at its own collapse. **C** the causal extreme: each shell gives f_b at collapse until M_d is reached, then none.

Read: Q = M_c/M_c(N) at 2, 3, 4, 6, 8, 10 R_d. ρ_X = (Q_X − 1)/(Q_L − 1) at 3 R_d.
- **K-T1:** Q_L(3 R_d) at 10¹² within 25 % of LC1's live Q − 1 (0.94) at r_p/r_a 0.2. If not: no T1 label.
- **Label:** **ORDER CAN REACH** if ρ_C × 0.872 ≤ 0.20 at 10¹² at r_p/r_a 0.2 with ρ_C at 10¹⁰ above 0.8; otherwise **ORDER CANNOT REACH, SPHERICAL**. Non-spherical order stays PZ1's. Measured SFH is not fed in: C bounds it. Downsizing's sign is discussed as PROVISIONAL literature only.
- MUTATE: M_d × 2 must move Q_L(3 R_d) − 1 by more than 30 %.

## Two survivors chosen for grading (from reading the record, no number from this lane)
Both run on NR3's path through `rm1n_lib`, NR2 MEDIAN, EM1, read only, own cache.

**MB, missing baryon budget.** EM1 and native fair share together say a galaxy's shells started with cold × (1 + 1/R_nat), not cold × (1 + F_obs). RET1's M_ej requires this gas to have been lifted. The response row omitted that. Rule: in `contract`, F → max(F, 1/R_nat), every path. This is a ceiling, since gas that never entered a shell (preventive, or ejected before the shell's birth) doesn't count. No number added. It does nothing to clusters at fair share.

**VDI0, disc instability of the closed-box gas disc.** Clumps massive enough to feel friction need a gas disc that is Toomre unstable given a dispersion that cannot drop below warm gas's thermal speed. Rule, per SPARC galaxy, using no V_obs: M = 0.5 L₃₆ + 1.33 M_HI, all gas (closed box), scale R_d from SPARC's table; at R = 2 R_d: Σ = M e⁻²/(2π R_d²), V² = G[0.594 M + M₀(R)]/R with M₀ the uncontracted cold mass on the harness, κ = √2 V/R, σ_crit = πGΣ/κ. **Selected if σ_crit > c_s, c_s = 8.2 km/s** (isothermal, T 10⁴ K, μ 1.22, the atomic cooling floor: a physical number, not fitted). Selected: f = 0, the ceiling, energy not counted. Unselected: f = 1. Groups and clusters have no disc: f = 1, which follows from the rule and isn't an extra posit. LITTLE THINGS by the same test with R_d = R/2.2 (R its tabulated radius, stated) and M its M_b.

**VDIE, energy-limited.** As VDI0, but the undoing is limited by what demonstrably reached the centre, per galaxy and per Υ: M_sink = M_bul = max(Υ V_bul² r/G) from the SPARC rotmods. Available energy, perfect delivery as ER2: W = M_sink [∫_{r_f}^{R_HI} G M_tot/r dln r + V_c(R_HI)²/2], M_tot the contracted total, r_f the first observed radius. f from ER1's E(f) = [W(f) − W(1)]/2 = W_avail, with W(f) = −∫G(M_b + M_f) dM_f/r, f ∈ [0, 1], f = 1 where unselected or no bulge.

Reported, not primary: VDI0 + MB; VDI0 with c_s 11.7 km/s (μ 0.6); VDI0 at δ +0.05, FITTED, labelled, because RM2 needs that. Per bin: selected share; median Υ selected vs not. **Delivery ratio** D per bin (no grade): E_cold/E_undo with all baryons through clumps, Toomre mass M_T = π Σ (λ/2)², λ = 2σ_crit²/(GΣ)... with λ = 4π²GΣ/κ² as ER2, one clump's power from Chandrasekhar in the uncontracted cold density at 2 R_d, lnΛ = ln(1 + M(<R)/M_T), X = 1 (B = 0.428), lifetime 300 Myr (PROVISIONAL, from memory), energy E_cold = (M/M_T) × M_T V × F_df/M_T × ... = M × [4πG² M_T ρ_c lnΛ B/V] × t_life; all baryons is a ceiling. D ≥ 1 is necessary, not sufficient.

## Pass lines, the record's
SPARC rms ≤ 0.110 and Υ 0.50-0.80 both backgrounds; |tilt| ≤ 0.15; groups |Z| ≤ 2; |LITTLE THINGS median E| ≤ 0.10. 15 keys and X-COP (|mean| ≤ 0.05, rms ≤ 0.10): this path's cluster block as NR3, which NR4's audit says isn't on gas +0.005; if a row clears the SPARC side, it's rerun on +0.005 before any claim. **Labels per row: SPARC SIDE CLEARS, or FAILS naming gates; CLUSTER BLOCK reported.** Whole-row PASS needs both. For VDI rows the cluster block equals EM1 Blumenthal by construction, X-COP −0.097, so no whole-row pass is possible on this path, and this is stated now.

**Holdouts read, not rerun:** a selected galaxy under VDI0 is UR3's Off row: DiskMass r 1.365 and Milky Way wide priors only, smooth core. So a full f = 0 at L★ is already in tension there. This is not a graded pass line here, and it counts against the rule.

**Lensing tail, forest, early universe:** a late baryonic process cannot change R ≫ R₂₀₀ or z ~ 3 × 10⁴, and neither rule touches BOLTZ1's or the forest's constraints. So the blue tail is not addressed; stated now.

## New predictions, non-SPARC, frozen in form (numbers filled from the run)
- **MB:** at fixed M₂₀₀ and M_b, cold mass inside 8 kpc at MW mass falls by a stated ratio against Blumenthal, computed; and it shrinks to none in systems at fair share. Discriminator: inner cold mass against measured gas in the halo (tSZ, X-ray) at fixed M_b, more retained gas meaning more contraction.
- **VDI0:** cold deficit sets in where σ_crit crosses c_s, about V 100-120 km/s, independent of bulge share; z 1-2 massive clumpy discs already show inner cold deficits, and same-z discs below the threshold don't. Dust-lane transition (from memory, Dalcanton et al. 2004, about 120 km/s, PROVISIONAL) is a check of the threshold. LSBs at V_flat 150-250 below threshold keep full contraction.

## Checks (any failure: no verdict on that block)
K1 EM1 off and Blumenthal through this lane's wrapper against NR3 MEDIAN: |d| ≤ 1e-6 on Υ, rms, tilt, LT, groups Z, or its grid-caused size named as NR4's audit found (then stated). K2 VDI0 with all unselected = EM1 Blumenthal |d| ≤ 1e-6. K3 MB with F_c 0 = EM1 Blumenthal. K4 E(f=1) = 0, E monotone in f. MUTATE, separate output: MB F_c × 2 moves Υ by more than 0.02; selection inverted in VDI0 moves Υ by more than 0.05. No knob scans. One thread, nice 15.

## My expectation on record
T1: ρ_C 0.7-1.0, ORDER CANNOT REACH. MB: Υ 0.38-0.48, tilt worse, FAILS; right idea, wrong mass trend, since F_c − F_obs is larger in dwarfs. VDI0: Υ line and tilt clear or nearly, LT +0.116 FAILS since it doesn't touch dwarfs, selected share near 1 at 150-250; D below 1 at realistic clump mass; holdouts against it. VDIE: Υ near 0.35, since most SPARC spirals at 150-250 carry little or no bulge. Overall: no mechanism survives whole. Probability I'd put now on any row clearing the SPARC side with no fitted number: 0.15.

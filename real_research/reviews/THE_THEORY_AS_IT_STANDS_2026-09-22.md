# The theory of gravity as it stands — synthesis of the week 2026-09-14 → 09-22

**What this is.** About 630 commits from roughly ten agent tracks landed in this repository between 09-14 and 09-22. On 09-22 they were audited against their committed scripts, re-running the load-bearing ones. This page assembles the most coherent theory the record supports. For each part it says whether it is measured, derived, fitted or missing. It also names the gates that would have to fall for this to become a theory of gravity, rather than a law plus an unfinished completion.

**Update, 09-25 (evening): the vacuum gate reopens the switch, the bound-region kernel is built, and the assembled construction passes every gate tested so far** (L357, L359–L361).

- **The switch lives again, with a vacuum-gated threshold** ([L359](../g03_audit_2026/L359_vacuum_gated_switch.py), 4/4; `MUTATE` = no gate, the window closes).
  - The KiDS–forest pincer (L352/L358/L362) applied ONE threshold at two epochs: KiDS at z ≈ 0.25 accepts x_c ≲ 3, the forest at z = 2–3 needs x_c ≳ 7.
  - The fix is to gate the switch variable by the vacuum's share of the expansion: u = x̃ [Ω_Λ(z)/Ω_Λ,0]^p = x̃ (3Λ/(Ω_Λ,0 K²))^p. This is local, and a tensor mode leaves K unperturbed, so L351's c_T = 1 carries over. The threshold becomes x_c,eff(z) = x_c0 E(z)^(2p): low today, high in the matter era.
  - Eight cells (p = 0.5–2, x_c0 = 1.5–2.5) pass three tests together:
    - linear growth (σ₈ = 0.810);
    - KiDS-1000 with L352's Gauss-compensated profile plus 2-halo (Δχ² −1 to −28 against the unswitched model);
    - the forest observable with L347's PM + FGPA (worst deviation 0.2–8.5% against the 10% rule).
  - The ungated control fails the forest at 0.16–0.19.
  - L362's resolution growth (about ×1.2) leaves the p ≥ 1 cells robust (≤ 4%) and p = 0.5 marginal.
- **The bound-region kernel, built from an action** ([L361](../g03_audit_2026/L361_bound_region_kernel.py), 6/6; `MUTATE` = L353's full-baryon unscreened kernel, which fails).
  - It is a region-local QUMOND. Its argument w is sourced only by the baryons inside the gated switch's bound region, and it is screened across the inactive web by M² = m²(1 − f).
  - Euler–Lagrange: in-region baryons feel their own region's phantom plus Newtonian gravity from everything; web gas and the carrier feel Newtonian gravity only. The phantom obeys (∇² − M²)P = ∇·[f(ν−1)∇w] + M²w, so it is Gauss-cancelled at the edge apart from a thin screened layer.
  - KiDS-1000 at the kernel's own field: +0.0 against isolated MOND, where the total-field and baryons-only kernels score +548 and +233.
  - The Sun keeps the Galaxy's field to 4×10⁻¹², so L340 S1 holds and wide binaries keep their EFE.
  - A 2 Mpc inactive gap transmits 9.5×10⁻⁵ of an external field at 1/m = 0.2 Mpc. The only requirement on m is 1/m ≤ 0.5 Mpc.
  - Unlike BK1, nothing inside a region is screened.
- **The carrier** ([L357](../dark_sector_2026/L357_virialization_triggered_carrier.py), 8/8; `MUTATE` = trigger off, V1 and D2 fail).
  - **The plain virialization trigger fails.** As a local trigger that fires in every halo down to 10⁸ M☉, it fails the forest at both slow and fast kicks: T²(k=5) = 0.30–0.64 against the 0.9 floor. Where the forest survives, X-COP overshoots (≥ 1.32).
  - **Relation to L365.** The parallel L365 triggers on the mesh-scale density. It finds a slow-kick window because its unresolved halos never fire, so the two lanes bracket the plain trigger.
  - **Gated by the same vacuum factor (p = 2), the carrier opens a window:** 3 strict cells and 17 alternative. The best decays where x̃ ≥ 2000 today with v_k = 3000 km/s, and passes:
    - the forest (T² ≥ 0.998);
    - S₈ = 0.772;
    - X-COP at 1.08 / 1.13 (canonical / alt);
    - the galaxy gate.
  - **Why it works:** galaxies are measured at x̃ ~ 10⁴–10⁵ while cluster R500 sits at x̃ ~ 200–350, and a cluster that loses its core expands.
  - **The price at z ≈ 2.5:** galaxies there keep carrier outside their cleared cores. The deep-MOND Tully–Fisher zero point shifts +0.8 dex, against 0.00 for the framework alone and +0.33 for ΛCDM, and RC100's inner dark fraction comes out at 0.43 against 0.29 (RC100 is calibration-conditional).
- **The assembled pair on KiDS** ([L360](../g03_audit_2026/L360_assembled_construction_kids.py), 4/4; `MUTATE` = undecayed carrier, 0 of 96 pairs pass).
  - 70 of 96 (switch, carrier) pairs pass (≤ +4 against the unswitched model).
  - The switched phantom stops at each lens's edge, and the carrier's hollowed halo fills the deficit beyond it. An undecayed carrier fails (≥ +232).
  - Example: switch (p = 1, x_c0 = 1.5) with carrier (p = 2, x̃ ≥ 2000, 3000 km/s) scores −23.5 / −16.8.
- **Standing.** One construction now passes, together:
  - linear growth (σ₈ = 0.810);
  - the Lyman-α forest (switch ≤ 4%, carrier strict);
  - S₈ = 0.772;
  - X-COP at 1.08 / 1.13;
  - the galaxy gate;
  - KiDS-1000 at −23.5 / −16.8;
  - GW170817 (c_T = 1);
  - the Solar System (1PN = GR, with the Sun keeping the Galaxy's field).
  
  It is a construction. The two thresholds and the gate exponent are chosen, not derived; the gate's tie to ρ_Λ, which also sets a₀, is suggestive, not derived.
- **Open, in order:**
  1. Gas inside active filaments at z ≲ 1 feels its own deep-MOND field, a force ×8–12 that cuts infall from 17–34 Gyr to 5.5–10 Gyr. The low-z forest and the filament tSZ stacks decide this.
  2. The high-z price: the flagship shift and RC100.
  3. The relativistic embedding of the bound-region kernel.

**Update, 09-25 (later): a kernel-invisible dark component — built, and what it does and does not fix** (L353–L356).

- **It exists** ([L353](../g03_audit_2026/L353_kernel_invisible_dark_component.py), 4/4; Lean `L353_kernel_invisible_certificates`).
  - **The construction:** a subtraction pair, two leafwise auxiliaries (v, λ) with ∇²v = 4πGρ_d, makes the MOND kernel read u − v, the baryonic Newtonian potential.
  - **The resulting field:** the metric carries Newtonian(all) + phantom(baryons), and lensing = dynamics for both species.
  - **What carries over:** L340's boost, tracking and modes are unchanged. The dark field leaks into the kernel only at α_c/2 ≈ 10⁻⁹.
- **Reciprocity fixes the force law** (L353 N2; Lean `response_symmetric`).
  - **The theorem:** a static Lagrangian's species-response matrix is symmetric, so a component the kernel cannot see feels only Newtonian gravity.
  - **Consequence for the record:** L321/L322's "additive" coupling (the carrier feels the baryons' MOND field while its own field is unboosted) has no action. It breaks Newton's third law by r/r_M, a factor 10.5 at 10 r_M.
  - **The price:** a dark-sector equivalence-principle violation wherever the phantom is on. In X-COP clusters the dark component feels 47% (37–53%) less acceleration than the gas.
- **At z = 0 the two live fronts become compatible** ([L354](../dark_sector_2026/L354_carrier_lagrangian_additive_window.py), 3/3). With the carrier's orbits Newtonian, L319's Λ-triggered carrier has a window, including cells that pass the strict thresholds:
  - canonical f_d(0) = 0.8, v_k = 1400 km/s: X-COP 1.13, S₈ 0.773, galaxies +0.02 dex;
  - also canonical 0.9 / 1200 and alt 0.8 / 1400.

  L345's "no window" was for C-H/K's universal coupling.
- **KiDS says the kernel must be blind to the web, not only to dark matter** ([L355](../g03_audit_2026/L355_kernel_invisible_kids.py), 4/4).
  - **Why baryons-only is not enough:** such a kernel still feels the web's baryonic field (e_b ≈ 0.002 a₀; 0.0008 at Brouwer+21's quiet field), while KiDS bounds any external field in the kernel at about 7×10⁻⁵ a₀ (BS2).
  - **The numbers:** the deficit is +233/+241. With the carrier's surviving halo and a bias-like 2-halo it is still +120 to +145, against the +9 fixed before the run.
  - **The control:** with the kernel blind to the web, the same carrier + 2-halo fits KiDS better than isolated MOND (Δχ² −11 to +1), and KiDS then wants 20–30% of a ΛCDM halo.
- **At high redshift kernel-invisibility changes nothing** ([L356](../dark_sector_2026/L356_construction_highz_price.py), 3/3). The carrier's halos must be intact at z ≈ 1–2.5 for the forest.
  - **RC100:** those halos overshoot the dark fraction (0.48–0.58 vs 0.29), and the inverted slope is +0.09 to +0.12 against −0.11 ± 0.06 (calibration-conditional).
  - **The flagship:** the deep-MOND Tully–Fisher zero point moves by +0.8 to +1.0 dex (Moster-calibrated halos), beyond ΛCDM's +0.33.
  - **Reading:** a Λ trigger acts too late. The carrier has to leave halos as they virialize.
- **The dark sector's specification, sharpened:**
  - (1) it must be kernel-invisible and feel Newtonian gravity only, as reciprocity forces (L353);
  - (2) the kernel must be blind to the large-scale field at the ~10⁻⁴ a₀ level. A bound-region kernel would do this: the subtraction pair extended to baryons outside switched-on regions. The open issue is λ's constant mode, which then enters the force at switch edges and must be fixed by boundary conditions;
  - (3) the carrier must be cold and present in the web and the forest, leave galaxy halos at virialization (a local trigger, e.g. on x̃), and be retained in cluster-depth wells (v_k ≈ 1000–1600 km/s).

**Update, 09-25: C-H/K's λ-channel and its switch against three more gates.** Three lanes from this session (L350–L352) and three committed by parallel lanes (KM3, L345, L346).

- **Local gravity holds.** KM3 ([`KM3`](../khronon_momentum_2026/KM3_chk_one_pn.py)) finds C-H/K's Solar-System 1PN metric is GR's. [L351](../g03_audit_2026/L351_switch_gw170817_gate.py) W5 confirms c_T = 1 for C-H/K without the switch: the heat filter's TT terms carry at most one derivative of h.
- **The λ-channel is capped by cosmology** ([L350](../g03_audit_2026/L350_chk_cosmological_G_gate.py), 5/5; `MUTATE` = WMAP-era bound, rc = 1).
  - **Why it applies:** on FRW, C-H/K is low-energy Hořava gravity with λ − 1 = c₂, η = α_c, ξ = 1. The minisuperspace gives G_cos/G_N = (2 − α_c)/(2 + 3c₂), which is exactly Frusciante & Benetti 2020 eq. (9).
  - **The cap:** their Planck 2018 fits put c₂ ≤ 0.6–2.9×10⁻³ (95%, every dataset combination). That is below L340's tracking floor of 7.3×10⁻³ by 2.5–12×.
  - **What survives:** below the cap the phantom still tracks galaxy bodies. Deep-MOND outskirts moving at 300–620 km/s are amplified by up to ~40%, and at the tightest cap the Local Group's outskirts are left behind. KM2's T1 thereby moves into KiDS reach.
  - **Repair (a construction):** −c₂(K − ⟨K⟩_Σ)², a λ-term acting only on the leaf-inhomogeneous part of K. It vanishes on FRW and is L340's term for every k ≠ 0 mode.
- **The switch variable fails GW170817** ([L351](../g03_audit_2026/L351_switch_gw170817_gate.py), 5/5; `MUTATE` = no shear completion, rc = 1).
  - **The mechanism:** x = 9R⁽³⁾/(4K²) puts R⁽³⁾ into the Lagrangian, so gravitational waves are superluminal wherever the switch is turning.
  - **The size:** the integrated advance per switching shell is exactly G M_b/(6c³), whatever the threshold, the switch's shape or H. That is 13.7 h for the Milky Way. GW170817 would have beaten its γ-rays by ≥ 19 h, against 1.74 s observed.
  - **Repair:** x̃ = 9(R⁽³⁾ + σ_ijσ^ij)/(4K²) takes L342's values on FRW, in the linear web and in static systems, and keeps c_T = 1 exactly.
- **Gauss's law: the switch cancels the phantom** ([L352](../g03_audit_2026/L352_switch_gauss_compensation.py), 7/7; `MUTATE` = retained profile, rc = 1).
  - **The theorem:** the phantom is a divergence, so a switch that turns the MOND flux off makes every isolated galaxy weigh exactly its baryons beyond its edge. A negative-mass shell sits at the edge, and it is singular as a static solution.
  - **Withdrawn:** L341 F7 and L342 B4 scored KiDS with the phantom's mass retained beyond the edge, a profile the action cannot produce. BS1 is built on the same model. These are withdrawn as evidence for the switch.
  - **Rescored:** with the realizable profile, L342's x_c = 5 is disfavoured (Δχ² +35/+36 with a free 2-halo term, +214/+225 without). Using the Hamiltonian-constraint switch variable of L346/Lean I26, x_c ≈ 2–3 fits KiDS better than no switch, but only with a bias-like 2-halo term (A ≈ 0.6–1.8).
- **The switch is closed by the forest plus KiDS.** L346 ([`L346`](../g03_audit_2026/L346_switch_forest_gate.py), parallel lane) fails every threshold up to x_c = 7 against its pre-declared band on the matter P(k). The parallel L347 corrects that headline at the level of the forest observable (FGPA 1D flux power): x_c = 5 is borderline (10.8% against a 10% rule) and x_c = 7 passes (7.2%). KiDS with the realizable profile accepts only x_c ≲ 3, and gives Δχ² +35/+36 at x_c = 5 and +101 to +106 at x_c = 7. No threshold serves both. Both sides are quantitative tensions (collisionless PM; linear 2-halo), so the closure holds at that precision.
- **The dark sector** (L345, parallel lane): C-H/K boosts any minimally coupled carrier like baryons, and the Λ-triggered carrier has no window under its coupling. The one internal escape is a carrier–U coupling that tracks the kernel.
- **Where this leaves it:** C-H/K, with the leaf-average λ-term, passes every local gravity gate computed (linear health, tracking, 1PN, c_T) and has no cosmology. The requirement is now sharp:
  - (i) the linear web and the forest-scale IGM at z ≈ 2–3 must stay Newtonian;
  - (ii) the lensing flux around isolated galaxies at 1–3 Mpc at z ≈ 0.25 must be supplied. By Gauss, that means either the MOND flux is on there or real mass is;
  - (iii) whatever supplies (ii) must not be boosted by the kernel.

  No local density switch does (i) and (ii) together. The doors left are a time-triggered threshold (the forest needs x_c ≳ 5–7 at z ≈ 2 (L346/L347), KiDS needs x_c ≲ 3 at z ≈ 0.25) and a dark component invisible to the kernel.

**Update, 09-23 (later): the bound-region switch, [L342](../g03_audit_2026/L342_bound_region_switch.py) (6/6; `MUTATE` = no switch, fails B2).** One scalar of C-H/K's own foliation, x = 9R⁽³⁾/(4K²), turns the MOND sector on only where the preferred leaves curve faster than they expand.
- **Where it is off:** on flat FRW, x = 0, and in the linear web x = (3/2)Ω_mδ. Linear growth returns to ΛCDM, with σ₈ = 0.810 against L341's 18–27.
- **Where it is on:** in a static bound system x = 4πGρ_dyn/H², which is ≥ 600 at every SPARC point and 10⁶ in the Solar neighbourhood. Galaxies, the Solar System and wide binaries are untouched.
- **KiDS-1000 picks the threshold:** x_c ≈ 4–7, the turnaround scale, preferred over no switch by Δχ² ≈ −15 to −19 on both footings; x_c ≥ 15 is excluded. This is a lead: the base fit is poor and 2-halo and external-field terms are not modelled.
- **Prediction:** a lensing truncation at r_t = v_flat/(√x_c H(z)), about 1.1 Mpc for the Milky Way today.
- **What it does not do:** it is a construction with one new number, not a derivation, and the outskirts are bistable. The dark sector is not solved.

**Lean certificates** (algebra only; exit 0, zero `sorry`, axioms {propext, Classical.choice, Quot.sound}), in `fable_independent_2026/lean_2026/`:
- `L330_frozen_density`: the shift cancels in the momentum-constraint divergence, with a λ ≠ 1 control; astra's block lapse is F(1+C)/C.
- `L340_chk_certificates`: static tracking; the khronon mode has ω² > 0 ⇔ C > 0; the negative-lobe inertia bound; |α₂| ≤ c₁₄.
- `L341_frw_certificates`: the CMC stiffness in the Newtonian and static cases; the quartic-floor suppression; the K-floor equals the dS-Unruh floor.
- `L342_switch_certificates`: x = (3/2)Ω_mδ on the linear web and 4πGρ/H² in a static system; the linear web stays off; the truncation radius.

**Update, 09-23: C-H/K fails the FRW gate, [L341](../g03_audit_2026/L341_chk_frw_gate.py).** With the cold fluid the CMB requires, C-H/K's MOND sector boosts the linear field and σ₈ comes out 18–27. Finite tracking does not rescue it.
- **The floor it could use:** the only floor made of its own fields is the clock's expansion K, and κ = K/(3α) = cH/a₀ is exactly the record's dS-Unruh floor. It is healthy in quartic form and returns σ₈ = 0.81.
- **Why that floor fails:** the foliation is CMC-stiff. δK = 0 for every static source, so a galaxy keeps K = 3H₀, and the floor removes MOND from the RAR (SPARC Δχ² > +6500).
- **What is missing:** a variable that knows whether matter has decoupled from the Hubble flow. KiDS-1000 says such a switch cannot sit inside ~0.5 Mpc of a galaxy (Δχ² +105 to +256) and is allowed near ~1 Mpc (Δχ² −11, a lead).
- **Status:** C-H/K stays the only candidate passing the linear gravity gates. It is not a cosmology.

**Update, late 09-22: a candidate completion, [L340](../g03_audit_2026/L340_filtered_khronon_completion.py).** C-H/K is astra's C-H plus the khronon's α-term α_c a² and λ-term −c₂K² (the Blas–Pujolas–Sibiryakov terms, β = 0), with a monotone phantom law. It is the first construction on the record to pass the moving-source gate and the health gates at the orders computed (11/11; see §1, Layer 3). **It is a candidate, not a theory:** nonlinear well-posedness, the full 1PN metric, cosmological perturbations and the dark sector are not computed.

**Verdict on the week itself.** No breakthrough landed in the week's commits. What they leave is:

- a measured law;
- a non-relativistic field theory that works as a description of galaxies;
- a relativistic candidate that is now known to fail a gate the record had not run;
- a dark sector with an exact but unfilled specification.

Two lanes were added on 09-22 to settle points this synthesis depends on: [L330](../g03_audit_2026/L330_moving_source_momentum_gate.py) (the moving-source gate) and [L331](../rc100_audit_2026/L331_rc100_fairness_audit.py) (RC100 fairness).

---

## 0. The standing in five lines

1. **The law stands, with κ measured.** a₀ = κ c√(Gρ_Λ), with κ = 0.465 ± 0.076 (BTFR) or 0.55 ± 0.17 (distance-free), consistent with ½. κ is **not derived**: every route on the record is closed, including KS01, the channel-count capstone (`opus_48_extended_research/kappa_audit_2026`) and postquantum classical gravity (L313–L314, κ = 1.30–1.45).
2. **The non-relativistic field theory stands as a description.** It is QUMOND with the framework's kernel ν_RAR, acting through a heat-kernel filter of length ξ (T-B). It passes Cassini statically and organises galaxies. It does not account for clusters.
3. **There is no relativistic completion.** The one open candidate, astra's C-H, passes its static gates. **New today (L330):** its MOND sector carries no momentum, so the phantom it produces is fixed initial data. The phantom cannot form as a galaxy assembles and cannot follow a galaxy that moves. This holds under either causality criterion.
4. **There is no dark sector.** The CMB needs a cold fluid: baryons alone give a third-to-second peak ratio of 1.192 against 0.992 (L295). The Lyman-α forest, RC100 and KiDS together squeeze out every carrier on the record (L319–L321).
5. **The dated tests are unchanged:**
   - Gaia DR4 on 2026-12-02;
   - the z ≈ 2.5 deep-MOND Tully–Fisher zero point;
   - a blind map-level tSZ score;
   - cluster lensing cores.

---

## 1. The theory, layer by layer

### Layer 1: the scale (MEASURED)

$$a_0=\kappa\,c\sqrt{G\rho_\Lambda}=\frac{cH_\Lambda}{Z}\quad(\kappa=\tfrac12),\qquad Z=\sqrt{32\pi/3}=5.7888$$

- **Footings:** canonical 9.36×10⁻¹¹ m s⁻² from ρ_Λ; alternative 1.13×10⁻¹⁰ from ρ_total. Their ratio is 1.2048 = 1/√Ω_Λ.
- **Deep limit:** v_flat⁴ = G M_b a₀ = ½ c G^{3/2} M_b √ρ_Λ.
- **What is distinctive:** with w = −1, a₀ is flat in cosmic time (under 1% to z = 5). ΛCDM's emergent scale rises by about +0.33 dex by z ≈ 2.5.
- **Z ≡ κ.** Deriving Z is deriving κ; the horizon form c²/(Z R_dS) restates κ = ½.

### Layer 2: the non-relativistic field equations (T-B; C-H's static branch)

$$\nabla^2u=4\pi G\rho_b,\qquad \nabla^2\Phi=4\pi G\rho_b+S^{*}\nabla\!\cdot\!\big[(\nu(|\nabla Su|/a_0)-1)\,\nabla Su\big],$$
$$S=e^{(\xi^2/2)\nabla^2},\qquad \nu(y)=\big[1-e^{-\sqrt y}\big]^{-1}.$$

| What | Status | Where |
|---|---|---|
| Deep RAR, BTFR, M_ph(<r) = M_b r/r_M | IDENTITY (Lean) | `L261` inventory |
| RAR scatter 0.108 dex; vertical force and Eilers slope (f_M = 1.30) | works as a description | STANDING rev. 6; vertical-force front |
| Cassini and the ephemeris, static | passes for ξ ≳ 0.02–0.05 pc. The operator-dependent floors are not reconciled across candidates. | G02, `hunt_2026/f29`, L316 |
| Clusters | **fails**: the kernel leaves 1.65–2.0× the baryons at R500 on real X-COP, and 6.8× inside 400 kpc with ρ ∝ r⁻¹·⁵ | `opus_48 C02`, g04a |
| tSZ outer slope | **NOT PASSED**: −2.48 ± 0.33 against the registered window (−1.7, −0.9) | L317 |
| Dark mass inside r_M (kernel 0.49 vs equipartition 1.00) | cannot be decided on SPARC | L267 |
| Phantom active-mass law | disfavoured at ~4σ on its own terms | L315 |
| The 5.09 keV mass / 2.55 keV line / "the loop is closed" | **do not cite** | L261 |

### Layer 3: the relativistic completion (MISSING)

**What an action must supply:**

- (i) PPN γ = β = 1, α₁ and α₂ inside their bounds, and the Solar-System quadrupole under the Cassini ceiling;
- (ii) lensing = dynamics, **including for time-dependent sources**;
- (iii) no ghost and no gradient instability;
- (iv) c_T = c (GW170817);
- (v) the deep-MOND limit;
- (vi) a phantom that forms and follows matter, i.e. the moving-source gate (L330).

| Candidate | Where it dies |
|---|---|
| AeST / v9 | α₁ = −2(K_B+2), which cannot be tuned away |
| Exponential khronometric MOND | radial gradient instability for a₀ < a < 38a₀ |
| Frozen scalar | ghost (H045) |
| Bimetric | Boulware–Deser ghost |
| Local k⁴ operators | PPN |
| PAPER24/25 disformal clock | GW170817: a 1.8–2.3 yr delay against the observed 1.7 s (CK01; errata deposited) |
| L297 "complete action" (clock chain) | not standing: 3 of 4 checks are literal `True`, the dust is CDM by hand, L306's σ₈ = 1.000000 calls the same function twice, and L294's galaxy exclusion integrates a grid that starts at 30 kpc. Its khronon has one momentum channel (c₂K², λ − 1 ≈ 2.5×10⁻⁵), **not computed** |
| **C-H (astra, G03)** | static T-B ✓. Causality depends on the criterion (L318). **Moving-source gate ✗ (L330)**. α₁, α₂ and c_T have never been computed for C-H. The structural reading is c_T = c, with α's negligible where the filter suppresses the modification. A scratch calculation of the clock's principal symbol (frozen coefficients, O(λ₀), not committed) finds a pole near kξ ≈ 5–7, i.e. linearised Hadamard ill-posedness, wherever sign(C₀) ≠ sign(ρ_ph). That covers negative-phantom lobes, and y > 1 regions for the ν_RAR kernel, including the Sun's neighbourhood. **Scratch lead, needs a committed lane** |

**New today: the momentum pincer (L330).** Every term of C-H's modification is independent of the shift and of every time derivative in the preferred frame. This was verified symbolically for an arbitrary lapse and shift, and astra's FULL_VARIATION states the same thing as G_ni = 8πG T_m,ni. The momentum constraint is therefore GR's with matter momentum alone. Its divergence is ½ ∂_t R⁽³⁾ with every shift term cancelled, so

$$\partial_t\big[R^{(3)}-16\pi G\rho_m\big]=0 .$$

The non-baryonic density that the curvature of the preferred leaves sees is conserved. astra's "integration function F" (ACTION.md) and the conserved δC of FULL_VARIATION §3 are this density. It is the analogue of Mukohyama's "dark matter as an integration constant" (2009): a dust-like density tied to the foliation, not to the baryons.

Consequences:
- A galaxy that assembles from near-uniform initial data forms no phantom in the leaf curvature.
- A phantom present at an initial time stays where it was. Satellites, pairs and cluster members cross their own r_M in 1–50 Myr.
- Either the dynamics is unmodified too, and no MOND is ever generated; or the lapse carries MOND and lensing sees (g_dyn + g_bar)/2. That is about half the phantom, −0.30 to −0.19 dex at KiDS accelerations, whereas KiDS-1000 finds the lensing RAR on the dynamical one.

The same shift-independence is what gives α₁ = α₂ = 0 on the record. The escape routes are all closed or open-but-uncomputed:

| Way to carry the phantom's momentum | Outcome |
|---|---|
| None (shift-independent sector) | frozen phantom (L330) |
| A dynamical QUMOND auxiliary | a ghost (Theorem 8, H045) |
| A vector, or a second metric | the α₁ of AeST, or the c_T of the disformal clock |
| Coupling that vanishes where ν → 1 | **open, and nothing on the record does this** |

**The candidate that passes: C-H/K ([L340](../g03_audit_2026/L340_filtered_khronon_completion.py), 11/11; `MUTATE` = ν_RAR kernel fails A1/H2, rc = 1).**

$$I_{\rm CHK}=I_{\rm CH}+\frac{c^3}{16\pi G}\int d^4x\sqrt{-g}\,\big[\alpha_c\,a_\mu a^\mu-c_2K^2\big],$$

with C-H's kernel built from a **monotone** phantom law ν_mono: ν_RAR below its phantom peak (y = 2.54), then a phantom acceleration that keeps rising slowly.

| Gate | Result |
|---|---|
| Moving source (L330) | **passes**: the λ-channel puts the shift into the momentum constraint. The ω → 0 response is the static MOND solution, and there is no frozen mode. The control c₂ = 0 gives back the Newtonian, frozen answer |
| Tachyon / ghost at leading order | **none**: one extra mode, ω² > 0, positive energy, in both constitutive directions at every y |
| Why the kernel must be monotone | in every momentum channel scanned (243/243 cells), a direction with C < 0 is a ghost or a tachyon. C is the clock's inertia, so momentum couplings cannot fix its sign. This is the record's 08-31 condition (yq)′ ≥ 0, found independently. ν_RAR and μ_exp both violate it |
| Negative-phantom lobes, O(Φ/c²) | the G03 audit's pole is re-derived (D1–D4) and removed by α_c ≥ α_min ~ G\|ρ_ph\|ξ²/c² (10⁻¹⁸ to 10⁻¹³) |
| Static limit | untouched: K = 0 on static slices, so the Cassini floors, the deep-MOND limit and static lensing = dynamics carry over |
| SPARC | Δχ² = −0.8 / +0.5 against ν_RAR (18 bins); the kernel change is ≤ 0.01 dex |
| Solar System | floors equal to ν_RAR's (0.031/0.045 pc canonical). Without the filter the monotone tail is excluded 2×10⁴× over the ephemeris bound: the 08-31 Cassini-vs-ghost pincer, reproduced **and broken by the filter** |
| Window | α_c between 10⁻¹³ and 3.2×10⁻⁹ (α₁ = −4α_c, α₂ ≈ −α_c/2); c₂ between 7.3×10⁻³ (tracking) and 0.067 (BBN); c_T = 1 exactly |
| New prediction | the phantom follows sources slower than c_s = c√(c₂/(C(2+3c₂))), about 10³–10⁴ km/s in halos, and lags faster ones by ~(v/c_s)² |

**FRW gate (L341, 09-23): FAILED as built.** σ₈ = 18–27 with the cold fluid; the K-floor fixes growth but is CMC-stiff and kills galaxies. See the update at the top.

**Not computed:**
- nonlinear well-posedness;
- the full 1PN metric (β_PPN, ζ's);
- cosmological perturbations, where C is singular at zero gradient;
- the dark sector and clusters, which are unchanged and still missing.

Scope: linear, frozen-coefficient, principal order, plus the audit's O(Φ/c²) clock terms with metric mixing dropped.

**Causality (L318).** Under the metric-cone criterion every scalar completion fails. Under the global-time criterion, standard in Lorentz-violating gravity (Babichev–Mukhanov–Vikman 2008; Bruneton 2007; Afshordi–Chung–Geshnizjani 2007), C-H survives causality. It still fails L330.

### Layer 4: cosmology and the dark sector (MISSING; the specification is exact)

**What the fluid must do:**
- at recombination, a cold fluid with Ω ≈ 0.26 (L295);
- cold power in the intergalactic medium at z = 2–3 and k ≈ 5 h/Mpc (the forest);
- cold mass with an r⁻¹·⁵ profile in clusters at z ≈ 0 (g04a);
- **no** cold halo inside galaxies (KiDS; RC100 at z ≈ 1–2.5). The MOND boost double-counts any CDM there, and a carrier must not source the MOND field (L321).

**The pincer, sharpened this week.** The forest and RC100 sample the same epoch at different accelerations: g_N ≈ 10⁻⁵–10⁻² a₀ in forest absorbers against a median g_bar ≈ 1.6 a₀ at R_e. The forest and KiDS sample the same accelerations at different epochs. A carrier therefore needs both a time trigger and a steep acceleration switch.

| Carrier | Status |
|---|---|
| Λ-triggered kicked decay (L319) | first on record to pass the forest and S8 (0.80–0.83); disfavoured at 3.0–3.4σ by RC100's trend (L320); at z = 0 the universal coupling is dead, and the additive coupling is near a window only at v_k ≈ 1500–1800 km/s (L321; L322 in progress) |
| Y-modulated carrier (L290–L309) | not standing (S8 identity, grid artefact). A scratch audit also finds its forest pass is evaluated at s = 0. Inside forest fluctuations the switch gives c_s = 30–110 km/s with pressure/gravity ≫ 1 at k = 5 h/Mpc. **Scratch, needs a committed lane.** |
| Relics, condensates, wave dark matter, the ~11 eV sterile corner | closed (g04f–g04j; f06) |
| Baryons only | CMB fails (L295) |

**RC100, stated fairly (L331).**
- The level of inner dark matter (0.29) is what any MOND on the z = 0 RAR gives: 0.28–0.32 across footings, kernels and a₀ = 1.2×10⁻¹⁰.
- A cored ΛCDM halo (r_c = 2R_e) matches the level (0.28) and the per-galaxy rms (0.168 vs 0.162).
- What survives is the redshift trend. For ΛCDM halos that do not evolve, cored or not, the residual rises at 3.0σ; for the framework it is flat to 0.9σ. The framework itself is 1.8σ from the data's slope.
- Fair wording: *RC100 is consistent with the z = 0 RAR and disfavours non-evolving ΛCDM halos at ~3σ in the trend.* That is one survey, with model-dependent f_DM. The earlier line "the framework alone beats ΛCDM" is withdrawn.

---

## 2. What the week produced, audited

**Stands, positive:**
- L319's carrier (with its RC100 price);
- L320's trend, as reworded by L331;
- L266: read as an emergent ΛCDM scale, a₀ predicts a gas-rich-dwarf BTFR scatter 2.2–2.4× the observed. It is semi-analytic and needs a ΛCDM population before it counts.
- L279: lensing = dynamics, static, leading order;
- field–orbit reciprocity E²(1−2β) = 2 (AQUAL-type theories only; untested on data).

**Stands, negative and useful:**
- κ is not derived: the channel count is 1 for dust (kappa_audit);
- CQ gravity is closed as a phantom source (L313–L314);
- G111 has no attractor; Q009 is exactly marginal;
- there is no linear-order drag (doorJ);
- a universal a₀ must break the strong equivalence principle (L264); L263;
- deepseek's g03_verdict does not close G03 (L316);
- tSZ: not passed (L317);
- the causality fork (L318);
- the phantom law: ~4σ (L315);
- the moving-source gate (L330).

**Refuted or hollow:**
- deepseek PD01–PD22, "κ = ½ derived" (kappa_audit);
- deepseek PD20's wide-binary v⁴ = 2GMa₀: it adds square-root responses and breaks momentum conservation (scratch);
- deepseek G196/G205/G207/G214 (L261);
- hy4 H055/H060: the kernel relabelled as a Lomax distribution (L261; G230 passes 1/5);
- hy4 H016–H031 (L260);
- qwen38 Q007/Q008 read as κ derivations;
- opus_49b/c I14, the "Hardy wall" (doorH);
- opus48 M01/M02, the MUSE reconciliation: a ln/log₁₀ slip, and Ciocan's real per-galaxy data give about 0.01 dex (scratch). **MUSE's rising a₀(z) remains a live threat to the flat law.**
- L297/L306, "linear cosmology closed";
- L311–L312, the phantom law;
- the BH* campaign's a₀(ρ_gas): 6.3×10⁷ times the framework's a₀, a local-density reading already excluded at 13–34σ on SPARC. Its CFJC RFC-0001 still says "within 0.2%" after wave P downgraded it.

**Contradictions to resolve:**
- Wide binaries have three incompatible predictions on the record: γ_v = 1.000 (grok K005, L307), ≥ 2^{1/4} (deepseek PD18/PD20), and the registered Arm A band 1.16–1.23. Only the registered arms (Amendment 11) count.
- L306's σ₈ claim has never been retracted.
- The cluster kernel removes either 48% or 74–89% of the dark mass, depending on which lane you read. This is definitional, but it should be reconciled before either number is quoted.

**Record attributions to fix:**
- L279 (lensing = dynamics), L280 (α₂) and L287 (DOF count) were computed for the khronon + φ host of `THE_ACTION_2026-09-05`, not for C-H, and `CLOCK_WORK_ORDER.md` row C2 conflates the two.
- doorJ's drag result is for the shift-symmetric f(K) scalar, not for C-H.

Items marked *scratch* were checked by this audit in scripts that are not committed. Do not cite them until a lane commits them.

---

## 3. The dated tests (unchanged)

| Test | Framework | Rival | Date or gate |
|---|---|---|---|
| Gaia DR4 wide binaries, γ_v | Arm A 1.1614–1.1814 (canonical) / 1.1917–1.2267 (alt); Arm B covariant ceilings 1.0450 / 1.0300 | Newton 1.000 | **2026-12-02**, rule fixed in Amendment 11 |
| Deep-MOND BTFR zero point at z ≈ 2.5 | 0.00 dex (flat) | ΛCDM-native +0.33 dex | 2–4 clean rotators at ±0.13 dex (one gives only 4:1) |
| tSZ outer slope, blind map-level | isotherm window (−1.7, −0.9) | universal profile | pending (the existing-data score is NOT PASSED) |
| Cluster lensing cores | kernel + cold component | NFW | needs HST |

---

## 4. What a breakthrough would have to be

**Gravity.** An action that carries the phantom's momentum, so that the phantom forms and follows matter, through a shift-dependence that vanishes where ν → 1. It must also:
- avoid a wrong-sign dynamical auxiliary;
- keep the leafwise filter (Cassini);
- keep lensing = dynamics for moving sources;
- keep c_T = c.

The one momentum channel already on the record is L297's khronon (λ − 1 = c₂ ≈ 2.5×10⁻⁵). The first computation is whether it can carry a galaxy's phantom at 100–300 km/s inside the α₁ and α₂ bounds.

**Dark sector.** A cold component with a time trigger and a steep acceleration switch that does not source the MOND field. Next computations:
- the Y-modulated switch evolved inside growing fluctuations, scored against P(k = 5 h/Mpc, z = 3)/P_ΛCDM ≥ 0.9;
- the additive window of L321/L322.

**κ.** Settled as a measured constant of nature. Its precision is limited by the M/L zero point, the absolute gas scale and H₀.

**Gravity, after L340.** C-H/K meets these requirements at the orders computed. The next computations, in order of what they decide:
0. **(L341: FAILED as built; L342: REPAIRED by the switch; 09-25: the switch CLOSED by L346 + L352, its R⁽³⁾ form also by GW170817, L351)** FRW linear growth. The bound-region switch x = 9R⁽³⁾/(4K²) ≥ x_c ≈ 5 restores ΛCDM growth, and KiDS prefers it. What remains open here is the switch's bistability and dynamics;
1. nonlinear well-posedness of the clock + U/W system with the khronon terms;
2. the full 1PN metric (09-25: KM3, the Solar-System 1PN metric is GR's);
3. FRW perturbations, with the zero-gradient singularity of C regularised;
4. a moving-source N-body test of the (v/c_s)² lag.

The closure map's closing statement already applies to rungs 1, 2, 4, 5, 6 and 10. For C-H as written it now applies to rung 3 as well. Rung 3 is open again, for C-H/K (L340), with the four computations above left to run. As it stands, the programme is a galaxy-scale law with a measured constant and, as of L340, one relativistic candidate that survives its linear gates. It is not yet a theory of gravity.

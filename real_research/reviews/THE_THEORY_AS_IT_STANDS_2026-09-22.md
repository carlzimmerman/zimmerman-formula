# The theory of gravity as it stands — synthesis of the week 2026-09-14 → 09-22

**What this is.** About 630 commits from roughly ten agent tracks landed in this repository between 09-14 and 09-22. On 09-22 they were audited against their committed scripts, re-running the load-bearing ones. This page assembles the most coherent theory the record supports. For each part it says whether it is measured, derived, fitted or missing. It also names the gates that would have to fall for this to become a theory of gravity, rather than a law plus an unfinished completion.

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
1. nonlinear well-posedness of the clock + U/W system with the khronon terms;
2. the full 1PN metric;
3. FRW perturbations, with the zero-gradient singularity of C regularised;
4. a moving-source N-body test of the (v/c_s)² lag.

The closure map's closing statement already applies to rungs 1, 2, 4, 5, 6 and 10. For C-H as written it now applies to rung 3 as well. Rung 3 is open again, for C-H/K (L340), with the four computations above left to run. As it stands, the programme is a galaxy-scale law with a measured constant and, as of L340, one relativistic candidate that survives its linear gates. It is not yet a theory of gravity.

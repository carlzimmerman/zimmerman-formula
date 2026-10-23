# K1_braneworld_weyl — frozen criteria (written before any script or number; committed alone with the ledger)

Lane of the 2026-10-22 rebuild (`rebuild_2026_10_22/BRIEF.md`; doors `BRIEF.md` and `BRIEF_E_AUDIT.md` apply).
κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. No dark-matter particle.
Never "theory closed". Never "the data favour the framework".

## The idea under test (the owner's)

"What if cold energy is kind of like a black hole, a dip into another dimension." Mapped (coordinator) to braneworld
gravity: our 4D world is a brane in a 5D bulk; bulk gravity projects onto the brane as the projected Weyl tensor E_μν
(a traceless "Weyl fluid" / "dark radiation" that gravitates without being brane matter). The literal reading (a population
of black holes / compact objects) is treated in one paragraph only (it behaves like particle dark matter; F2 says isolated
galaxies need no extra halo).

Record checked before freezing: `why_4_puzzle/W4_01_untouched_gravity_families/` (DGP only for κ: MENU/TRADE),
`deepseek_push/DS_FINAL_2026_10_21/A34_dimension_route/` (κ = 2/D numerology; D = 5 rotation curves), CFG254 R3
("bubble/brane contact: UNTESTABLE-AS-STATED", a cosmic contact, not E_μν), `real_research/GEMINI_10_IDEAS_REVIEW_2026-06.md`
idea 10 (DGP leakage: hits the same wall). No lane has computed the projected Weyl term for cluster cores, galaxies,
dwarfs, the Solar System or BBN. H2 (AeST μ²Φ dust: wrong shape) and J1 (|Φ| selector, frozen, running) are related and
read only. No braneworld paper is on disk: every literature equation is an EXTERNAL input, cited by arXiv id, flagged
"not verified on disk"; wherever possible its static consequence is re-derived here with sympy.

**Disclosed before freezing (not blind):** back-of-envelope estimates in my head say (i) a P = 0 Weyl fluid tied to the
cosmological dark radiation under the BBN bound is ~10¹¹ too weak for cluster cores, and (ii) its profile tracks |Φ|, the
same shape H2 excluded. The checks below are built to show or refute this with numbers.

## Part A — the brane equations (sympy; DERIVED unless marked)

External input (not verified on disk): the effective 4D equations of Shiromizu, Maeda & Sasaki (arXiv:gr-qc/9910012),
G_μν = −Λ₄g_μν + κ₄²T_μν + κ₅⁴π_μν − E_μν, π_μν quadratic in T_μν (∝ ρ²/λ), E_μν traceless, ∇^μE_μν = κ₅⁴∇^μπ_μν; Maartens'
decomposition of E_μν into U (energy), P (anisotropic stress), Q (flux) (arXiv:gr-qc/0312059; arXiv:1004.3962).

A1. Static spherical metric −e^ν c²dt² + e^λ dr² + r²dΩ²; Weyl fluid ρ_W = U (mass units), p_r = (U + 2P)c²/3,
    p_t = (U − P)c²/3 (traceless). Derive the tt, rr, θθ equations and the Weyl conservation law. Count unknowns
    (ν, λ, U, P) against independent equations (tt, rr, conservation; θθ follows by Bianchi). Expected: one free
    function = the non-closure. Name what fixes it: a bulk solution, or a POSTULATED closure.
A2. Low energy: the brane source of E_μν is π_μν/T_μν ~ ρ/λ_b. With λ_b ≥ (1 TeV)⁴ (EXTERNAL, arXiv:1004.3962, not verified
    on disk) evaluate ρ/λ_b for a cluster core, a galaxy and the solar centre. If ≪ 1, the Weyl amplitude is a bulk
    boundary datum: brane matter does not set it.
A3. Universal slip (any closure, weak field, leading order in Φ/c²): show d M_dyn/dr = 4πr²·2U, d M_lens/dr = 4πr²·(3/2)U,
    d M_λ/dr = 4πr²·U (M_dyn from ν, M_lens from (ν + λ)/2). Lensing/dynamics of the Weyl mass = 3/4.
A4. Closures the literature uses, each solved:
    - **C0, P = 0** (vanishing anisotropic stress): U = U_ref e^{−2(ν − ν_ref)} (Tolman radiation). Linear: δU = −4U_∞ψ/c²,
      ψ = Φ − Φ_ref. Show this is an AeST-type mass term ∇²ψ + μ_W²ψ = 4πGρ with μ_W² = 32πG U_∞/c² (relativistic Jeans
      wavenumber), lensing weight 3/4. C0 is the only closure whose amplitude depends on potential depth.
    - **C1, P = wU** (linear equation of state; Mak & Harko arXiv:gr-qc/0404104; Harko & Cheng galaxy closure, ApJ 636, 8,
      arXiv id recalled as astro-ph/0509576; both not verified on disk): U ∝ r^{−6w/(1+2w)}; flat rotation curves (the HC
      closure) ⇔ w = 1, U ∝ r⁻². Amplitude per object, free.
    - **C2, P = −2U** (tidal charge; Dadhich, Maartens, Papadopoulos & Rezania, "black holes on the brane",
      arXiv:hep-th/0003061, not verified on disk): verify exactly that e^ν = e^{−λ} = 1 − 2GM/(rc²) + Q/r² solves the
      vacuum brane equations with U ∝ Q/r⁴, P = −2U. This is the owner's "black hole / dip" in its exact braneworld form.
    - **B1, bulk-supplied (RS2 linear; Garriga & Tanaka arXiv:hep-th/9911055, not verified on disk):**
      Φ = −GM/r (1 + 2ℓ²/(3r²)), table-top ℓ ≤ 0.1 mm (arXiv:1004.3962, not verified). Not a postulate: the bulk supplies it.
    - **B2, bulk-supplied (DGP, induced gravity):** spherical decoupling-limit equation 3β∇²φ + (r_c²/c²)[(∇²φ)² −
      (∇_i∇_jφ)²] = 8πGρ, Φ = Φ_N + φ/2 (Nicolis & Rattazzi arXiv:hep-th/0404159; Koyama & Silva arXiv:hep-th/0702169;
      not verified on disk). Solve the spherical root with sympy.
A5. FRW: a traceless, conserved, isotropic E_μν is w = 1/3, ρ_W ∝ a⁻⁴ (dark radiation). It cannot be the CDM-like dust that
    growth needs (H1, v4); state whether v4's dust is still required.

**Postulate count (frozen):** C0: closure P = 0 (+1 POSTULATE), LINK static asymptote U_∞ = cosmological dark radiation
(+1 POSTULATE; it is what allows the BBN test), zero point r_ref (+1 RULE), U_∞ (+1 constant, calibrated).
C1: closure w = 1 (+1), normalisation rule (+1), truncation r_ref (+1 RULE), ξ₁ (+1 constant). C2: closure P = −2U per mass
element (+1), Q ∝ mass rule (+1), ℓ_Q (+1 constant). B1, B2: no postulate; constants bounded externally, not calibrated.
Weyl gravity is added to the law's acceleration (A-ADD, +1 POSTULATE for every closure; reason: E_μν is geometry, and it
is traceless, so a trace-sourced scalar would not see it). The law is AQUAL μ = x/(1+x) (spherical root, F1's `g_aqual_sph`).

## Part B — one constant per closure, calibrated on F1 MID only, then predictions with no refit

**Frozen normalisations (one constant each):**
- C0: U_∞ (Weyl density at r_ref). Exact linear boundary-value problem per system, feedback included:
  ψ′ = g_law(r) + 2G m_W/r², m_W′ = 4πr²δU, δU = −4U_∞ψ/c² for r ≤ r_ref, δU = 0 beyond; m_W(r₀) = 0, ψ(r_ref) = 0;
  **r_ref = 3 Mpc** (F1's outer edge and gas truncation). Lensing source 1.5 δU. Reported, not graded: the test-fluid
  version (ψ = law potential, no feedback) and r_ref = 10 Mpc.
- C1 (w = 1, HC isothermal): Weyl dynamical velocity v_W² = ξ₁ √(G M_b a₀) (a fixed fraction of the law's own flat
  velocity; M_b = the system's total baryon mass), ρ_dyn = v_W²/(4πG r²) to r_ref = 3 Mpc, lensing source 0.75 ρ_dyn.
- C2 (tidal charge per mass element): Φ_W(x) = −G ℓ_Q ∫ρ_b(x′)/|x − x′|² d³x′ (each element's Q = −2G dm ℓ_Q/c²);
  dynamics from Φ_W, lensing weight 3/4.

**Calibration (CAL).** F1 PRIMARY exactly: F1's measurement cache (sha256 961ea4fc…e720, read-only copy), AQUAL, native
h 0.672 and 0.686, eRASS1 gas rescaled q^{5/2}, β-model G0, f* = 0.20, data boost, catalogue miscentring, F1's per-band
amplitude statistic and 30-patch jackknife. Solve A_MID = 1 per closure, footing and h. C1 and C2 are linear in their
constant (closed form). C0: smallest U_∞ on a 0.1-dex log bracket U_∞/ρ_crit,0 ∈ [1e-8, 1e12], refined by bisection. CAL
FAILS for a closure if no root exists. (Reported only: CAL with F1's A1 clipped boost.)

**Predictions (each footing at its own constant; graded at the h 0.672 and the h 0.686 calibration; a line passes only
if it passes in both):**
- **O1, F1 OUTER:** |A_OUTER − 1| ≤ 2σ_OUTER AND profile χ² of the bins 3–7 residual stack (30-patch jackknife covariance,
  Hartlap (30−5−2)/29) ≤ 11.07 (H2/J1's line). INNER reported.
- **R1, isolated galaxies:** F2's four profiled L1 lens masses log M_b = 10.36, 10.83, 11.01, 11.18 (Plummer b = 5 kpc,
  AQUAL law, no external field). Ratio ∫ΔΣ_W d ln R / ∫ΔΣ_law d ln R over O1 (0.4–1.1 Mpc) and O2 (1.1–2.6 Mpc).
  PASS iff ≤ 0.14 (2 × F2's σ(A_O2) = 0.07) in both bands for all four masses.
- **R3, dwarf satellites:** E3's per-system CSV (central values; canonical 45 / alt 46). Baseline residual
  r_i = log10(M_dyn,i b_i² / M_pred,i), M_pred = B_scr,L24 × 10^{log M*}/2, b_i the CSV binary ratio. With the closure:
  r_i′ = r_i − log10(1 + M_W,i/M_pred,i), M_W = the closure's dynamical Weyl mass inside r12 = (4/3) R_h (own baryons as a
  Plummer sphere with half-mass radius r12; host = MW or M31 Hernquist 6.0e10 / 1.0e11 M☉, a = 3 kpc, at LVD distance_gc /
  distance_m31; field dwarfs: MW at distance_gc). PASS iff |median r′| ≤ 0.26 dex (2 × E3's 0.13). Otherwise FAIL by the
  median r′ (positive = still short, negative = overshoot).
- **R5, Solar System:** anomalous radial acceleration at Earth / Mars / Saturn vs C6's bounds (8.7e-15 / 1.4e-15 /
  7.0e-15 m/s², `covariant_push_2026_10_22/C6_literal_cassini/c6_literal_cassini.py` line 35). Sun = point mass; Galactic
  part from the MW Hernquist at R₀ = 8.122 kpc. PASS iff all three ratios < 1. Reported: Cassini γ − 1 from the slip
  vs (2.1 ± 2.3)e-5.
- **R4, cosmology:** where the static normalisation is linked to the background (C0's LINK), the calibrated U_∞ is the
  dark-radiation density today: ΔN_eff = Ω_W h²/(x Ω_γ h²), x = (7/8)(4/11)^{4/3}, Ω_γh² = 2.469e-5 (C2), bound
  |ΔN_eff| ≤ 0.30 (A78, read-only). PASS iff within. C1, C2: NOT LINKED (stated). Dust: from A5.
- **Bulk-supplied lines.** B1: fractional cluster excess at r = 0.808 Mpc (MID bin 4 centre) with ℓ = 0.1 mm, vs the
  needed A_MID − 1; FAIL by the ratio. Also the ℓ that would be needed and what it does to the Solar System (5D gravity
  below ℓ). B2: fractional boost δ = (φ′/2)/(GM/r²) at 0.808 Mpc for a cluster (M = 7.0e13 M☉, H2's median baryon mass)
  and a galaxy (10^{10.83} M☉), r_c = c/H₀ (h 0.679), β = 1 and 3. FAIL R2 if δ_cluster < 0.5 × (A_MID − 1); the
  selector sign is δ_cluster/δ_galaxy (> 1 = deep-potential selector).

## Part C — J1

Report, not graded: which closures carry a |Φ| dependence and with what scaling; C0's boost relative to the law at
cluster MID, galaxy O2, a median dwarf and the Sun at the calibrated U_∞; whether the Weyl term supplies a physical
origin for a potential-depth selector. Read J1's committed results (if any) read-only.

## Verdict rule

- **WORKS:** some closure passes CAL, O1, R1, R3, R5 (and R4 where linked) on both footings.
- **PARTIAL:** some closure passes CAL and O1 and at least two of R1, R3, R5, R4-if-linked (state which).
- **FAILS:** no closure reaches PARTIAL, and B1 and B2 both fail R2 (state which requirement and by how much, per closure).
- **UNDECIDED (missing bulk solution):** no closure reaches PARTIAL, but B1 or B2 cannot be evaluated.
The per-object amplitude of C1/C2 (one free constant per system, set by an unknown bulk solution) is a fit, not a
prediction; it is reported as what stays open, never as a pass.

## Checks (script `k1_braneworld_weyl.py`; one line each; exit 0 iff all pass)

- K1: sympy A1: with U = P = 0 the equations reduce to TOV; the θθ equation follows from tt, rr and the conservation law
  (residual 0); unknowns − independent equations = 1.
- K2: sympy A4: P = 0 ⇒ U ∝ e^{−2ν}; P = wU ⇒ U ∝ r^{−6w/(1+2w)} at leading order (w = 1 ⇒ r⁻²); the DMPR metric solves
  the exact vacuum equations with P = −2U, U ∝ Q/r⁴ (residual 0).
- K3: sympy A3 slip coefficients 2, 3/2, 1 (residual 0); and μ_W² = 32πGU_∞/c² from the linearised C0 system.
- K4: sympy A5: ρ_W ∝ a⁻⁴; and (1 + x N_eff)/x reproduces A78's 7.4492 (A78 `a78.out`, read-only) to 1e-4.
- K5: F1 reproduction: cache sha256 matches; the law with F1's own functions reproduces F1's committed PRIMARY A_MID and
  A_OUTER (2 h × 2 footings) to ≤ 1e-6 relative.
- K6: my signed linear projector agrees with F1's projector on the law's (positive) density: band amplitudes within 0.5 %.
- K7: C0 solver: homogeneous solution equals sin(μr)/(μr) to ≤ 1e-4; at μ_W r_ref ≤ 1e-3 the exact BVP equals the
  test-fluid integral to ≤ 1e-3.
- K8: C2 kernel: for a Plummer sphere, Φ_W → −GMℓ/r² at r ≥ 50 b to ≤ 1e-3.
- K9: E3 reproduction from the CSV: median baseline r_i within 0.10 dex of E3's +0.886 (canonical) / +0.846 (alt)
  (central values vs E3's Monte Carlo; the difference is printed).
- `--mutate`: the Weyl radial pressure is dropped from the rr equation (p_r^W → 0): K1 and K3 must FAIL; outputs in
  `*_MUTATE.*`.

Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, single thread, minutes, no downloads, no network. F1's measurement cache
is copied read-only into session scratch (path as argv[1]); nothing of another lane is written.

## AMENDMENT A1 (2026-10-23, PRE-RESULT: before any K1 script was written or run)

- **R3 / K9 baseline.** E3's per-system CSV `M_dyn` is already the binary-corrected median (E3 `build(..., binmode="free")`,
  `e3_dwarf_excess.py` L252 and L302). Applying the CSV `binary_ratio` again would double-correct. So the baseline is
  r_i = log10(M_dyn,i / M_pred,i), with no b_i². Disclosed: while reading the CSV I saw its central medians (0.95 / 0.91 dex
  without b², 0.81 / 0.77 with b²; E3's Monte Carlo gives 0.886 / 0.846). K9's 0.10 dex line is unchanged.
- **K8.** For a Plummer sphere the far-field correction to −GMℓ/r² is not small at 50 b: the r⁻⁵ tail makes the second
  moment log-divergent, ⟨s²⟩_{<r} ≈ 3b²[ln(2r/b) − 4/3], which gives ≈ 1e-3 at r = 50 b (analytic, from the expansion
  K = r⁻²(1 + s²/3r² + …)). K8 is therefore evaluated at r ≥ 100 b (correction ≈ 3e-4); the 50 b value is printed.

## AMENDMENT A2 (2026-10-23, PRE-RESULT, coordinator request after J1 landed in 3d75573e2c; reporting only, no graded line changes)

J1 found that a |Φ| selector calibrated on F1 MID overshoots OUTER (|Φ| is nearly flat across a cluster) and does nothing
for satellites (they sit in shallower host potential than the Sun). Added reports:
- For each closure, the variable the Weyl mass tracks: the potential ψ (C0), a fixed per-object power law (C1), or the
  local baryon density / its gradient (C2: in Fourier space Φ_W,k = −2π²Gℓ_Q ρ_k/k, so ρ_eff = (πℓ_Q/2)(−∇²)^{1/2}ρ_b; to be
  checked with sympy as K2(d), reported only, not a graded check).
- Compactness against F1's needed shape (extra ≈ 1.4–1.8 × gas inside 1 Mpc, ≈ 0 outside, more concentrated than the gas):
  the calibrated Weyl lensing mass over the gas mass inside 0.5, 1, 2, 3 Mpc (median cluster), and the radius holding half
  of the Weyl excess inside 3 Mpc vs the same radius for the gas.
- For satellites, the variable each closure uses (host depth ψ for C0, which J1 showed is the wrong variable; the
  satellite's own baryon mass for C1; the satellite's own baryon structure, ℓ_Q/r12, for C2).

## AMENDMENT A3 (2026-10-23, POST-RESULT: implementation fixes after RUN1; frozen lines and thresholds unchanged)

RUN1 is kept as `*_RUN1.*` (8/9 checks, verdict FAILS, the same per-closure statuses as the final run except C2's R1 line).
1. **K2** failed in RUN1 because the sympy symbol w had no realness assumption, so `dsolve` returned a complex-exponent
   form. w is now declared real. No number changes.
2. **R1 for C2 (a graded line).** The galaxy projection cannot resolve C2's far field. Around a compact galaxy the C2
   effective density is a positive core (scale 2Mℓ/b) plus a negative r⁻⁴ envelope, and their net ΔΣ at 0.4–2.6 Mpc is
   about 1/400 of either part. F1's 2 kpc inner disc and 90-point 2D cumulative integral are not that accurate: RUN1 gave
   −0.16 to −0.55, and adding the inner 1 kpc mass as a point gave −0.5 to −1.8. The line is now graded on the exact
   point-source result ΔΣ_lens = (9/16) M ℓ_Q / R³ (README; corrections O((b/R)² ln) ≤ 1e-3 at R ≥ 80 b), which gives
   +0.04 to +0.13 (PASS). The projector values are still printed. For clusters (no such cancellation) the C2 template is
   checked against the projected-potential method: median ratio 1.000–1.004 in bins 3–7 (10 clusters). This moves C2's
   R1 from FAIL to PASS. C2's verdict is unchanged (it FAILS O1, R3 and R5).
3. **R1, law and C1:** the galaxy's mass inside 1 kpc (RG[0]) is added as a central point (≤ 0.5 % effect on the ratios).
4. **RSS hygiene.** RUN1 peaked at 1.38 GB (ru_maxrss), above the < 1 GB rule, from heap growth in the C0 calibration
   scan. The C0 solver now uses reusable step-major buffers. The final run peaks at 0.85 GB; its numbers are identical to
   the run before this change (all non-memory output lines equal).

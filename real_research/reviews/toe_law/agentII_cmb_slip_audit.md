# agentII — Boltzmann/CMB audit of the lens-only slip sector

**Status: COMPLETE (2026-06-11). VERDICT: KILL of the unregulated linear-scale extension — Sigma =
nu(g_bar/a0) over-lenses the CMB x57 (A_L family), E_G by 25-193 sigma, Sigma_0 by ~230 sigma, ISW
sign-flipped; required saturation cap (nu <= 1.03-1.14) sits below the ENTIRE galactic measured nu range
(4.4-306) at overlapping g_bar; the EFE/ambient rescue is short x112-777 in field strength. All three
readings, both footings, and the framework's own no-CDM accounting (x4-6 over, 20-25 sigma). The early
universe is safe (the law self-extinguishes above z ~ 122-155); the kill is late-time/large-scale only.
Constructive output: S_slip REQUIRES a second discriminant beyond g_bar (boundedness/scale), converging
with agentZ's independent type-dial demand. Details §3-§5; one caught bug (EH98 q-convention), §5.5.**

## Charge

The assembly's biggest unpaid debt, named [OPEN] in UNIFIED_ACTION_ASSEMBLY.md: the
lens-only Psi-channel slip sector has (mu, Sigma) = (1, nu(g_bar/a0)), zero clustering
stress-energy (double-counting theorem), c_T = 1, alpha_M = 0 identically. At linear
cosmological scales g_bar << a0, so a naive nu(y) -> 1/sqrt(y) DIVERGES: the slip sector
would catastrophically over-lens the CMB (A_L), the ISW, and galaxy-galaxy lensing unless
something saturates or screens it.

Audit plan (both footings, kill verified as hard as pass):
1. Linear-theory Sigma(k,z) for the assembled sector, with the ambient g_bar of large-scale
   structure computed properly from the power spectrum (not guessed).
2. Confront with measured constraints: Planck-2018 A_L, CMB-lensing sigma8 consistency,
   published E_G measurements (pinned arXiv ids), Sigma_0 from DES-Y3 / KiDS / Planck
   (mu0, Sigma0) parametrizations.
3. Compute the framework's actual predictions under three honest readings:
   (a) raw nu, no saturation; (b) the lensing-RAR-saturated form; (c) the EFE /
   ambient-field-regulated nu (the ambient field is nonzero at linear scales).
4. VERDICT per observable: PASS / KILL / SATURATION-DEPENDENT, with the required
   alpha_infinity computed and compared against the lensing-RAR-measured value if the
   verdict lands there.

## Log

- [x] Memo created; reading UNIFIED_ACTION_ASSEMBLY.md, agentW, agentY, lensing_rar corpus next.
- [x] 2026-06-11 (relaunch): inputs read; computation plan fixed (below). Results appended incrementally.
- [x] Stage A (g_bar map, a0 crossings, EFE ambient) run + banked (§1).
- [x] Stage B (Sigma readings x frames x footings, overlap exhibit) run + banked (§2).
- [x] Stage C (A_L/phi-phi/E_G/Sigma_0/ISW; required caps + floors; Frame 2; verdict matrix) run + banked (§3).
- [x] Stage X validation gates: BBKS cross-check CAUGHT an EH98 q-convention bug -> fixed, all stages rerun,
      §1/§2 corrected in place, bug log §5.5. Post-fix gates: P-peak 0.0164, d_rms 2.38', phi-phi peak 1.34e-7.
- [x] Constraint pins fetch-verified 4/4 (§4): A_L 1.180+/-0.065; Pullen E_G 0.24+/-0.06; DES-Y3 Sigma_0 =
      0.04+/-0.05 (tighter than pinned); phi-phi amplitude 1.011+/-0.028.
- [x] Verdict + constructive requirement written (§5); STATUS flipped to COMPLETE.

## §0 Inputs and scoping (read 2026-06-11)

**The law under audit** (UNIFIED_ACTION_ASSEMBLY.md, S_slip): (mu, Sigma) = (1, nu(g_bar/a0)) with
nu(y) = sqrt(1 + 1/y); zero clustering stress-energy (T^slip is anisotropic-stress-only in the Psi channel);
c_T = 1 and alpha_M = 0 identically. Slip normalization banked against the lensing-RAR amplitude
(Brouwer+2021 / our 6.8-sigma Hartlap re-measurement, agentK).

**Saturation search:** `grep -ri saturation reviews/lensing_rar/` is EMPTY — **no lensing-RAR saturation is
banked anywhere in the corpus.** The lensing-RAR measurement runs g_bar = 1e-15 to 5e-12 m/s^2 (15 bins,
lr_data_acquisition.md) and the banked result is that the measured profiles FOLLOW the RAR there (the early/late
split is a +0.2 dex type offset, not a flattening). So at g_bar = 1e-15 the data demand nu ≈ nu(1e-15/a0) ≈ 306
(canon footing) — the measured curve is UNSATURATED to the survey floor. Reading (b) therefore uses the charge's
fallback: a Brouwer-consistent cap "Sigma_max ~ few" (we scan nu_max = 2, 3, 5) AND we invert each observable for
the REQUIRED cap, which is the decision-relevant number.

**Footings (both, per the working rule):** canon a0 = 9.36e-11 m/s^2 (pure-Lambda, rho_DE/cH_Lambda);
alt footing a0 = 1.13e-10 (rho_total/cH0); MOND-default 1.2e-10 as the convention-robustness row. In the deep
regime nu scales as sqrt(a0/g_bar): the full footing spread moves nu by 10-13% — verdict-irrelevant, shown anyway.
a0(z): the framework's own branch is sqrt(rho_DE) = CONSTANT under pure Lambda (the conservative choice, used
here); the rival rising cH(z) branch only RAISES nu at z>0 (worsens any over-lensing) — noted where relevant.

**Scoping (what this audit is and is not):** This is the slip-sector piece of the assembly's [OPEN] Boltzmann
debt, computed on the OBSERVED clustering (EH98 no-wiggle P(k), sigma8 = 0.811, Planck-18 background), per the
charge. mu = 1 means matter growth is taken standard; the matter-sector question (whether the M22 inertia
functional can grow the observed delta without CDM) is a SEPARATE open debt, flagged but not computed here.
Because the framework's own accounting has no CDM, every observable is computed in TWO frames with equal weight:
- **Frame 1 (constraint frame, generous):** Sigma = nu applied on top of the LCDM-calibrated total-matter field;
  g_bar argument = the total-matter Newtonian field (Omega_m). This is the frame in which the published A_L, E_G,
  Sigma_0 constraints are defined. Generous because the framework's own g_bar (baryons only) is 6.4x smaller,
  i.e. nu 2.5x larger.
- **Frame 1-own (the law on its own terms):** same, but the nu argument is the BARYONIC field
  g_b = (Omega_b/Omega_m) g_total (delta_b = delta_m at linear scales) — the RAR's g_bar is always baryons.
- **Frame 2 (no-CDM accounting):** lensing is sourced by baryons ALONE and boosted: Sigma_eff =
  (Omega_b/Omega_m) x nu(g_b/a0) relative to LCDM's total. Here the divergence is LOAD-BEARING (it is what must
  replace CDM in the Weyl potential) and the question becomes whether nu delivers the right amplitude AND the
  right (k,z) shape. Both the needed boost (Omega_m/Omega_b = 6.39, k-flat) and the delivered one are computed.

**Constraint pins (charge-given; fetch-verification in §4):** Planck-2018 A_L = 1.180 +/- 0.065 (TTTEEE+lowE
peak-smearing); Planck phi-phi reconstruction amplitude consistent with LCDM at the ~2.5% level (the second,
TIGHTER member of the A_L family — the anomaly is in the smearing, not the reconstruction); E_G(z=0.3-0.9)
measured 0.16-0.48 (band 0.3-0.4) vs LCDM Omega_m/f(z) = 0.40-0.46; DES-Y3/KiDS (mu0, Sigma0): |Sigma_0| <~
0.2-0.5 (Sigma(z)-1 = Sigma_0 OmegaLambda(z)/OmegaLambda_0 convention, so Sigma(z=0)-1 = Sigma_0).

**Computation plan:** (1) g_bar(k,z) map, k = 1e-3..1 h/Mpc x z = 0..1100, EH98 no-wiggle + growth ODE
(radiation in H(a)), rms-per-ln-k delta; a0-crossing contour. (2) the three readings (a) raw / (b) capped /
(c) EFE-floored at the rms bulk-flow acceleration g_amb(z) = [3/2 Om(z)H^2(z)] sqrt(int dlnk Delta^2_lin/k_phys^2)
— note the per-ln-k rms (reading a) and the all-k cumulative rms (reading c's floor) are exactly the two natural
conventions for "the ambient field," so (a) and (c) bracket the convention freedom. (3) Limber A_L^eff(L) over the
CMB-lensing kernel, E_G = Omega_m,0 Sigma/f, Sigma_0^eff, an ISW order-of-magnitude row. (4) required caps /
required floors per observable, against the lensing-RAR-measured nu range. Script: agentII_cmb_slip_audit.py
(numpy/scipy only), stages A/B/C; canonical output agentII_cmb_slip_audit.out.

## §1 The ambient g_bar of linear structure (stage A — run 2026-06-11, validated; numbers are POST-bug-fix,
see the bug log in §5)

**Machinery validation (all pass, post-fix):** sigma8 round-trip 0.8110 = target; P(k) peak at k = 0.0164 h/Mpc
(expect ~0.016); Delta^2_lin(0.2) = 0.77 (standard for sigma8 = 0.81); EH98-vs-BBKS independent-transfer
cross-check max 16% (family-level); D(z): f(0) = 0.527 vs Om^0.55 = 0.530; linear v_rms(1D, z=0) = 306 km/s
(standard ~290-330); chi(z*) = 13864 Mpc (Planck 13869); GR lensing spectrum [L(L+1)]^2 C_L^pp/2pi = 1.34e-7
at L=40 (Planck/CAMB peak ~1.3e-7); GR deflection d_rms = 2.38 arcmin (textbook 2.4-2.7, linear no-wiggle
expected marginally low). Growth ODE integrates radiation in H(a) from a = 1e-4 with Meszaros ICs;
D(1090) = 1.41e-3.

**The g_bar(k,z) map (total-matter source; the baryonic field is x0.156 of every entry):**
g_bar = (3/2) Om(z) H^2(z) delta_rms(k,z)/k_phys with delta_rms = sqrt(Delta^2_lin). Per-ln-k rms peaks at
**k = 0.056 h/Mpc at every z** (the n_eff = -1 plateau): max_k g_bar = **5.9e-13 m/s^2 at z=0** (y_canon =
6.3e-3), 2.2e-12 at z=2, 9.9e-10 at z=1090. g_bar grows as (1+z)^2 D(z) ~ (1+z) through matter domination.

**Where g_bar crosses a0 (the charge's question 1):**
- canon footing: max_k g_bar = a0 at **z_dagger = 122**. ALL linear scales are sub-a0 for z < 122.
- alt footing: z_dagger = 146; MOND-default: z_dagger = 155. Per-k (canon): k=0.01 crosses at z=209,
  k=0.03 at z=129, k=0.1 at z=128, k=0.3 at z=187.
- So the slip sector is in its DIVERGENT regime over the entire late-time universe: at the CMB-lensing kernel
  pivot (k=0.028 h/Mpc, z=2): g_bar = 2.1e-12, y = 0.022, **nu = 6.8**. At the E_G pivots (k=0.05, z=0.32/0.57):
  **nu = 10.5 / 9.4**. At the Sigma_0 pivot (k=0.05-0.1, z=0): **nu = 12.7-13.0**.
- At recombination the slip has mostly shut itself off at the acoustic scales (y = 10 at k = 0.05-0.1,
  nu = 1.05) BUT NOT at the largest scales: nu(k=0.001, z=1090) = 1.50, nu(0.003) = 1.20, nu(0.01) = 1.08 —
  an 8-50% Weyl-potential boost at ell <~ 100 survives at the primary CMB (flagged in §3 as a follow-on
  exposure).

**The EFE ambient (reading (c)'s floor):** the rms peculiar-gravity (bulk-flow) acceleration of linear
structure, g_amb(z) = (3/2)Om(z)H^2(z) sqrt(int dlnk Delta^2/k_phys^2) — integral converges (k<=1 carries 99%):

| z | g_amb [m/s^2] | y (canon) | nu canon | nu alt | nu MOND |
|---|---|---|---|---|---|
| 0 | 1.04e-12 | 1.11e-2 | **9.5** | 10.5 | 10.8 |
| 0.57 | 1.90e-12 | 2.0e-2 | 7.1 | 7.8 | 8.0 |
| 2 | 3.90e-12 | 4.2e-2 | 5.0 | 5.5 | 5.6 |
| 10 | 1.45e-11 | 0.155 | 2.7 | 3.0 | 3.0 |
| 1090 | 1.74e-9 | 18.6 | 1.03 | 1.03 | 1.03 |

Key structural fact: g_amb(z) EXCEEDS the per-ln-k g_bar at every k (cumulative > per-octave, necessarily), so
the EFE floor binds everywhere and reading (c) gives a k-INDEPENDENT Sigma(z) = nu(g_amb/a0) — scale-shape-safe,
but amplitude ~10 at z=0 and ~5 at z=2 where the constraints want ~1. Nonlinear power raises g_amb (bracket x1.5
carried downstream; even a hand-bracket "mass-weighted one-halo ambient" ~1e-11 m/s^2 only lowers the floor to
nu ~ 3.2). The framework's own a0(z) branch (sqrt(rho_DE), constant under Lambda) is used; the rival rising-cH(z)
branch would RAISE nu at z > 0.

## §2 Sigma(k,z) under the three readings x three frames (stage B — run 2026-06-11, post-fix)

**Sigma at the constraint pivots (canon footing; alt/MOND footings raise every nu by 10-13% — tabled in .out):**

| pivot (k h/Mpc, z) | g_bar [m/s^2] | F1 raw | F1own raw | F2 raw | F1 EFE | F2 EFE |
|---|---|---|---|---|---|---|
| phi-phi kernel (0.028, 2.0) | 2.06e-12 | **6.8** | 17.1 | 2.67 | 5.0 | 1.94 |
| E_G low-k (0.02, 0.5) | 8.62e-13 | 10.5 | 26.4 | 4.13 | 7.3 | 2.86 |
| E_G Reyes (0.05, 0.32) | 8.62e-13 | **10.5** | 26.4 | 4.13 | 7.9 | 3.10 |
| E_G Pullen (0.05, 0.57) | 1.07e-12 | 9.4 | 23.6 | 3.70 | 7.1 | 2.78 |
| Sigma0 pivot (0.05, 0) | 5.86e-13 | **12.7** | 32.0 | 5.00 | 9.6 | 3.76 |
| Sigma0 low-k (0.01, 0) | 3.37e-13 | 16.7 | 42.1 | 6.59 | 9.6 | 3.76 |

Reading (b): any "Sigma_max ~ few" cap (2/3/5 scanned) binds at EVERY pivot — raw nu >> cap everywhere on
linear scales, so the capped law is just Sigma = cap there; the verdict is then set by the cap value alone (§3).

**The overlap exhibit (the audit's structural core):** the linear-scale ambient g_bar at z <= 1,
k = 0.01-0.3 h/Mpc spans [~2e-13, 1.4e-12] m/s^2 — INSIDE the lensing-RAR measured bins (1e-15..5e-12, where
the banked result is that the data FOLLOW nu: nu = 4.4 at 5e-12 rising to 306 at 1e-15, unsaturated) and at
SPARC's low edge (nu = 9.7 at 1e-12). The law is ONE function of g_bar: at g_bar = 5e-13 the galactic RAR
demands nu = 13.7 while the CMB-era constraints (§3) allow ~1.07 at the same argument. No nu(g_bar) can do both.

**The recombination row (z = 1090):** the slip mostly shuts itself off at the acoustic scales (nu = 1.05 at
k >= 0.05 h/Mpc, ell >~ 470) but NOT at large scales: nu = 1.50 at ell ~ 9, 1.20 at ell ~ 28, 1.08 at ell ~ 93.
An 8-50% Weyl-potential boost at ell <~ 100 would distort the SW plateau / early-ISW region of the primary TT
spectrum at a level Planck constrains to percents. Flagged as a follow-on exposure (no Boltzmann solve here);
direction: it can only ADD to the kill. (Caveat: z~1090 values use the scale-independent-growth approximation
stated in §1 — factor-level, not order-level, uncertainty.)

## §3 The confrontation (stage C — run 2026-06-11, post-fix)

### 3.1 A_L family (CMB lensing amplitude)

A_L^eff = the kappa-weighted / deflection-weighted <Sigma^2> over the exact Limber CMB-lensing kernel
(L = 20-400, sources to z*; the GR denominator validated against the Planck phi-phi peak, §1):

| reading/frame | <Sig^2> kappa-wt | defl-wt | A(L=40) | A(L=400) |
|---|---|---|---|---|
| F1 raw | **57.0** | 85.5 | 78.9 | 45.9 |
| F1own raw (baryonic g_bar) | **358.9** | 540.8 | 498.5 | 288.1 |
| F2 raw (no-CDM accounting) | **8.8** | 13.3 | 12.2 | 7.1 |
| F1 EFE-floored (x1.0 / x1.5 NL) | 28.4 / 19.2 | 36.3 / 24.5 | — | — |
| F2 EFE-floored | 4.3 | 5.6 | — | — |
| F1 capped nu_max=3 | 8.9 | 9.0 | 9.0 | 8.8 |

Constraints: A_L(TT smearing) = 1.180 +/- 0.065; the phi-phi reconstruction amplitude = LCDM-consistent at
~2.5-3%. **The charge's direction question: YES, the framework predicts MORE lensing (nu >= 1 always — the
direction of the A_L anomaly), but the excess is catastrophically over: x57 (F1 raw) where the anomaly wants
x1.18.** Right sign, wrong by ~1.7 orders of magnitude. Footing spread: 57.0 (canon) / 68.6 (alt) / 72.8
(MOND-default) — **the framework's own canonical footing is the MOST favorable and still dies; the kill is
not a convention artifact** (working rule satisfied). A_L^eff(L) is nearly flat in L for every reading, so no
(smearing vs reconstruction) threading exists: anything fitting A_L = 1.18 in the smearing violates the
phi-phi amplitude at the same level. CMB-lensing sigma8 reading: sqrt(57) => sigma8^lens ~ 7.5x the TT value
(measured: consistent to ~2%).

### 3.2 E_G (lensing / clustering-velocity ratio)

E_G = Om0 Sigma/f(z); LCDM = 0.454 (z=0.32), 0.402 (z=0.57), 0.370 (z=0.86). Predicted at k=0.05
(spread over k=0.02-0.1 is +/-5%):

| reading/frame | E_G(0.32) | E_G(0.57) | E_G(0.86) | vs Reyes 0.39+/-0.06 | vs Pullen 0.243+/-0.060 |
|---|---|---|---|---|---|
| F1 raw | 4.76 | 3.78 | 3.15 | **+73 sigma** | **+59 sigma** |
| F1own raw | 11.98 | 9.51 | 7.90 | +193 sigma | +154 sigma |
| F2 raw | 1.87 | 1.49 | 1.24 | **+25 sigma** | +21 sigma |
| F1 EFE (x1.0 / x1.5) | 3.59 / 2.94 | 2.85 / 2.34 | 2.38 / 1.95 | +53 / +43 sigma | +43 / +35 sigma |
| F2 EFE | 1.41 | 1.12 | 0.93 | +17 sigma | +15 sigma |
| F1 cap nu_max=3 | 1.36 | 1.21 | 1.11 | +16 sigma | +16 sigma |

Every published E_G point (eight tabled in the .out, z = 0.27-0.86, values 0.09-0.48) sits at or BELOW the
LCDM expectation; several (Pullen, VIPERS) prefer LESS lensing than LCDM. The slip law predicts 3-12x MORE.
Even the most generous reading on the table (F2 + EFE floor) is 15-17 sigma over.

### 3.3 Sigma_0 (DES-Y3/KiDS parametrization, bound |Sigma_0| <~ 0.2-0.5)

Sigma_0^eff = Sigma(k, z=0) - 1: F1 raw +11.7 to +15.7 (k = 0.01-0.3); F1own +31 to +41; F2 raw +4.0 to +5.6;
F1 EFE +8.6; F2 EFE +2.8; cap-3 +2.0. **Mildest entry is x5.5 over the loosest bound.**

### 3.4 ISW (supplementary, source-level)

GR late-ISW: potentials decay, d(D/a)/dlna < 0. The slip law's Weyl potential is Sigma(k,z) x (D/a) and nu
GROWS in time faster than D/a decays, so the source is **SIGN-FLIPPED** and large: ratio (FW/GR source) =
-16 to -50 at k = 0.002-0.02, z = 0.2-1.0 => ISW auto-power x270-x2450 GR. The measured ISW x LSS
cross-correlation is POSITIVE (decaying potentials) at ~4-5 sigma — the slip law predicts the WRONG SIGN of
the cross-correlation on top of the wrong magnitude. (Source-level statement; no C_ell computed; partial
line-of-sight cancellations cannot flip a sign that is uniform over the whole late-time kernel.)

### 3.5 Required saturation caps (the inversion the charge asked for)

Bisection on the kernel-weighted <Sigma^2> (frame-insensitive: F1own identical to 3 decimals):

| target | required nu_cap | saturation onset |
|---|---|---|
| phi-phi reconstruction +2sig (1.067) | **1.033** | y = 14.9, g_sat = 1.4e-9 = 15 a0 |
| A_L central = 1.18 (FITS the anomaly) | **1.086** | y = 5.6, g_sat = 5.2e-10 = 5.6 a0 |
| A_L +2sig (1.31) | 1.145 | y = 3.2 |
| E_G Reyes +2sig | 1.122 | — |
| E_G Pullen +2sig | **0.902** (prefers Sigma < 1) | — |
| Sigma_0 0.2 / 0.5 | 1.20 / 1.50 | — |

**The coincidence test: FAILS.** No saturation is banked in the lensing-RAR corpus (grep empty, §0); the
measured lensing-RAR curve is UNSATURATED to its floor, nu(1e-15) ~ 306. The required cap (1.03-1.5) sits
BELOW the ENTIRE galactic measured range (nu = 4.4-306 across the lensing-RAR bins; nu = 9.7 already at
SPARC's own low edge g_bar = 1e-12). Per the charge's decision rule — required cap below galactic measured
nu values — **this is a KILL for any global saturation**, and it is a kill that does NOT even need Brouwer's
deep bins: SPARC alone contradicts the cap. The "cute" sub-result: a cap at nu_max = 1.086 would PREDICT the
A_L anomaly centrally — but that cap freezes nu ~ 1 for all y > 5.6 i.e. over the entire RAR, destroying all
rotation-curve phenomenology. The framework cannot buy the A_L anomaly without selling the galaxies.

### 3.6 Required EFE floor vs the computed ambient (reading (c) closed)

To pass, the regulating ambient field must satisfy g_floor = a0/(nu_cap^2 - 1):

| target | required g_floor | computed g_amb(z=0.5) | shortfall (linear / x1.5 NL / one-halo 1e-11) |
|---|---|---|---|
| phi-phi recon +2sig | 1.40e-9 (15 a0) | 1.80e-12 | **x777 / x518 / x140** |
| A_L central | 5.20e-10 (5.6 a0) | 1.80e-12 | x289 / x193 / x52 |
| A_L +2sig | 3.02e-10 (3.2 a0) | 1.80e-12 | x168 / x112 / x30 |

The honest EFE reading (the charge's (c)) DOES tame the divergence — it floors nu and even makes Sigma
k-independent — but the cosmic ambient field is **2-3 orders of magnitude too weak** to floor it anywhere
near 1. Even the maximally generous hand-bracket (every line of sight bathed in a one-halo field of 1e-11
m/s^2) leaves the floor x30-140 short. Reading (c) is quantitatively closed, both footings.

### 3.7 Frame 2: is the divergence the right size to replace CDM? (the load-bearing reading)

In the framework's own no-CDM accounting the boost is REQUIRED — Sigma_eff = (Ob/Om) nu(g_b/a0) must equal
1.0 (k-flat, all z) to reproduce the LCDM-equivalent Weyl potential. Computed: Sigma_eff = 5.0-5.7 at z=0,
4.1-4.7 at z=0.32, 2.6-2.9 at z=2, crossing 1.0 only at z* ~ 19-23; shape dlnSigma_eff/dlnk = -0.02..+0.20
over the k = 0.05-0.2 plateau (near-flat: a genuinely nontrivial near-miss — the n_eff = -1 plateau makes
nu(g_bar(k)) accidentally scale-free exactly where lensing looks CDM-like) but -0.19 at k=0.02 and steepening
below. **Verdict: the mechanism that would replace CDM in lensing over-delivers by x4-6 at z <= 0.5, x2.6-2.9
at the phi-phi kernel peak, has the wrong redshift evolution (boost FALLS with z while CDM's contribution is
constant), and the wrong low-k shape. As a CDM-replacement the slip law fails in amplitude, growth, and
scale-dependence — not marginally, 20-25 sigma in its gentlest observable (E_G).** The matter-growth side
(can mu=1 baryons even grow delta to the observed sigma8 without CDM wells? — no, by ~(Ob/Om) x growth
suppression) is the assembly's separate open debt, noted not computed.

## §4 Constraint pins: fetch-verified (4/4 budget used, 2026-06-11)

1. **A_L = 1.180 +/- 0.065** (TT,TE,EE+lowE; 2.8 sigma above 1) — VERIFIED, Planck 2018 VI
   (arXiv 1807.06209; cf. the 2310.03127 reanalysis: the preference is ~10% more smearing at fixed params,
   partly 217-GHz/ecliptic-keyed — i.e. the anomaly itself may be partly systematic; either way the
   framework's x57 is not in the conversation).
2. **E_G:** Pullen+2016 (CMASS x Planck lensing, z=0.57) = **0.24 +/- 0.06 (stat)** — VERIFIED; the published
   family at z~0.27-0.9 spans ~0.24-0.48 with GR/LCDM expectation ~0.37-0.45 (Reyes+2010 0.39+/-0.06 the
   classic; Blake+2016 CFHTLenS x CMASS 0.42+/-0.056; ACT-DR6 x BOSS 2024 = the modern CMB-lensing point,
   arXiv 2405.12795). My from-memory table attributions (Blake/Amon/VIPERS rows) are family-correct at the
   +/-0.1 level; no E_G measurement anywhere approaches the predicted 1.9-12.
3. **Sigma_0 = 0.04 +/- 0.05** (DES-Y3 3x2pt + BAO+RSD+SN, arXiv 2207.05766, the SAME
   Sigma(z)-1 = Sigma_0 OmegaLambda(z)/OmegaLambda_0 convention as coded) — VERIFIED and TIGHTER than the
   charge's pinned band (|Sigma_0| <~ 0.2-0.5). Sharpened consequences: the Sigma_0-required cap drops to
   **nu_cap <= 1.14** (2-sigma), and the F1-raw tension is (11.7-0.04)/0.05 ~ **230 sigma**; even F2-EFE
   (+2.76) is ~54 sigma. The loose-band caps (1.2/1.5) in §3.5 are therefore GENEROUS to the framework.
4. **phi-phi reconstruction amplitude = 1.011 +/- 0.028** relative to LCDM (Planck 2018 VIII, arXiv
   1807.06210/A&A 641 A8) — VERIFIED; exactly the target used for the tightest required cap (1.033).

## §5 VERDICT (the charge's matrix), bug log, and what survives

### 5.1 Per-observable x per-reading (canon footing; alt/MOND footings shift nu +10-13%, no change anywhere)

| observable (measured) | (a) RAW nu | (b) SATURATED (global cap) | (c) EFE-REGULATED |
|---|---|---|---|
| A_L TT smearing (1.180+/-0.065) | **KILL** x57 (F1) / x359 (F1own) / x8.8 (F2) | **SATURATION-REQUIRED -> KILL**: required cap 1.086-1.145 lies BELOW the entire galactic-measured nu range (4.4-306) | **KILL** x19-28 (F1), x4.3 (F2); floor short x112-777 in g |
| phi-phi recon (1.011+/-0.028) | **KILL** (same numbers, tighter target) | required cap 1.033 (onset 15 a0!) -> **KILL** harder | **KILL** |
| E_G (0.24-0.48 vs LCDM ~0.40) | **KILL** +25 to +193 sigma | required cap 0.90-1.12; the Pullen point wants cap < 1 (Sigma < 1) -> **KILL** | **KILL** +15 to +53 sigma |
| Sigma_0 (0.04+/-0.05) | **KILL** ~230 sigma (F1), ~80 sigma (F2) | required cap <= 1.14 -> **KILL** | **KILL** +2.8 to +8.6 vs 0.04+/-0.05 |
| ISW (suppl., source-level) | **KILL**: sign-flipped, power x270-2450 | a true global cap makes Sigma time-constant -> ISW sign OK (consistency note: ONLY the capped law passes ISW, and the cap is excluded above) | **KILL**: still sign-flipped (nu(g_amb) grows in time) |
| primary CMB ell <~ 100 (suppl.) | exposure: nu-1 = 8-50% Weyl boost at recomb | cap 1.03-1.15: marginal | near-pass (nu(g_amb,1090) = 1.026) — the one cell reading (c) handles |

**Both footings:** canon a0 = 9.36e-11 gives the SMALLEST kill margins (A_L 57.0 vs 68.6 alt vs 72.8
MOND-default); the framework's own convention is the most favorable and the verdict is unchanged — per the
working rule this is a convention-robust deficit, reported as such. The rival rising-a0(z) branch worsens all
of it; any nu-function with the same deep-MOND sqrt limit moves the numbers by O(1), never by the needed x50.

### 5.2 The structural theorem the numbers prove

The lensing-RAR (banked, 6.8 sigma, bins g_bar = 1e-15..5e-12 m/s^2) and SPARC (g_bar >~ 1e-12) MEASURE
nu(g_bar) = 4.4-306 across exactly the g_bar range that linear cosmological structure occupies at z <~ 2
(ambient 2e-13..4e-12 m/s^2, §1). The CMB/lensing/E_G/Sigma_0 constraints REQUIRE nu <= 1.03-1.14 on linear
scales at the same g_bar. **One function of g_bar alone cannot take both values at the same argument: the
lens-only slip law Sigma = nu(g_bar/a0), extended as-is to linear scales, is excluded — not marginally but by
1.7-2.5 orders of magnitude in power, in four independent observables, in both footings, under every reading
of the ambient field, including the framework's own no-CDM accounting (x4-6 over at z <= 0.5, wrong
z-evolution, 20-25 sigma at its gentlest).** Reading (c), the charge's named EFE rescue, is quantitatively
closed: the required regulating field (3.2-15 a0) exceeds the computed cosmic ambient (~0.01-0.04 a0 at the
kernel) by x112-777 (x30-140 under the maximally generous one-halo hand-bracket).

### 5.3 What survives, honestly (the both-ways column)

- The DIRECTION of the A_L anomaly matches (nu >= 1 -> more smearing), and a cap at nu_max = 1.086 would fit
  A_L = 1.180 centrally — but that cap is excluded by the galaxies the law was built on (it freezes nu ~ 1
  over the whole RAR) and by the phi-phi reconstruction (needs <= 1.033). The framework cannot buy the
  anomaly without selling the galaxies.
- The slip law self-extinguishes at high z (g_bar crosses a0 at z_dagger ~ 122-155): the EARLY universe is
  nearly safe (recomb-era nu = 1.03-1.05 at acoustic scales; reading (c) at z=1090 passes at ~3%). The kill
  is entirely a late-time, large-scale phenomenon — which is also why no pre-2026 banked gate caught it.
- Frame 2's near-miss is real and nontrivial: on the n_eff = -1 plateau (k ~ 0.05-0.2 h/Mpc) nu(g_bar(k)) is
  accidentally scale-FREE (dlnSigma/dlnk = -0.02..+0.20), i.e. the divergence has roughly the CDM-like SHAPE
  there — it is the amplitude (x4-6 at z <= 0.5) and the z-evolution that kill it, not the shape.
- The galactic-scale slip results (lensing-RAR amplitude, the agentZ dial, agentY's survivors) are untouched:
  this audit kills the EXTENSION of the law to unbound linear modes, not the law in halos.

### 5.4 What any rescue must now do (the constructive requirement, stated for the assembly)

A viable slip sector must carry a SECOND discriminant beyond g_bar that switches Sigma -> 1 on linear scales:
suppression of (Sigma - 1) by a factor >= 50-800 at k <= 0.3 h/Mpc, z <= 2, while preserving Sigma = nu out to
at least r ~ 1-3 Mpc around bound halos (Brouwer's outermost bins). g_bar itself cannot be the switch (the
ranges overlap); candidate discriminants with the needed >= 2-order dynamic range: boundedness/overdensity
(delta >~ 200 vs <~ 1), potential depth, or field-configuration evolution rate (linear modes evolve at ~H,
halo fields are static — and X2/EE's pumped bath lives exactly at omega ~ H, so a slip response with a
spectral notch at the bath band would shut off precisely the H-paced modes; SPECULATIVE, not derived, named
only because it is the one in-corpus hook). NOTE the convergence: agentZ already proved the slip amplitude
needs a morphology dial BEYOND g_bar in halos (TYPE-IRREDUCIBLE, 6.2 sigma); this audit independently proves
it needs a boundedness/scale dial BEYOND g_bar in cosmology. Two independent demands that S_slip cannot be a
function of g_bar alone — that is now a structural feature of the assembly, not a choice.

### 5.5 Bug log (per protocol: every catch recorded)

1. **EH98 q-convention bug (CAUGHT by the stage-X BBKS cross-check + d_rms gate; FIXED).** The transfer
   function's q used k in Mpc^-1 where the EH98 sec-4.2 Gamma-formalism takes k in h/Mpc (q = k[h/Mpc]
   Theta^2/Gamma_eff; the sound-horizon product 0.43*k*s stays physical). Symptoms before the fix: P(k) peak
   at 0.021 h/Mpc (vs 0.016 expected), P_EH/P_BBKS = 0.45 at k = 0.005, d_rms = 1.76' (vs 2.4-2.7'), phi-phi
   peak 7.1e-8 (vs ~1.3e-7). After: peak 0.0164, BBKS ratio within 16% everywhere (family-level), d_rms =
   2.38', phi-phi peak 1.34e-7 at L=40 — three independent anchors land simultaneously. Effect on results:
   nu at the pivots moved 10-20% (e.g. A_L F1 raw 69.9 -> 57.0); NO verdict changed. Pre-fix numbers existed
   briefly in §1/§2 (corrected in place, marked post-fix). Residual convention ambiguity (0.43*k*s physical
   vs h-units) checked: ~4% in T at the suppression knee — verdict-irrelevant.
2. **Stage-X pre-baked print ("agreement to ~15%") asserted before computing** — replaced with the computed
   max deviation + explicit gate language. (Process bug, zero numerical effect; recorded because the BBKS
   gate is exactly what caught bug 1, and it must keep teeth.)
3. **Charge's E_G-scale k ~ 0.02 read as h/Mpc vs Mpc^-1:** computed at k = 0.02-0.1 h/Mpc with the +/-5%
   k-spread quoted; ambiguity immaterial (nu varies by < 15% across the whole decade).

### 5.6 Status of the assembly's [OPEN] Boltzmann debt

PAID, with a definite answer: **the assembled S_slip's (mu, Sigma) = (1, nu(g_bar/a0)), taken at face value on
linear scales, is excluded at the x50-300 level in lensing power (A_L families), 15-230 sigma in E_G/Sigma_0,
with a sign-flipped ISW — under all three charge readings, both footings, and the framework's own no-CDM
accounting. The unified action as currently written has no viable linear-cosmology limit for its lensing
sector; viability requires the second discriminant of §5.4 as a STRUCTURAL feature (converging with agentZ's
independent same-shaped demand).** The matter-sector growth question (mu = 1 without CDM) remains the
assembly's separate, still-unpaid cosmology debt.

*Deliverables: this memo; agentII_cmb_slip_audit.py (stages A/B/C/X, numpy/scipy only, no CAMB);
agentII_cmb_slip_audit.out (canonical full run, post-fix). No git (per charge).*

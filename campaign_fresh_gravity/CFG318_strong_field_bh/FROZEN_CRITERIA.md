# CFG318: gate G11 (strong field: black holes, neutron-star structure) for the filtered C-H/K chassis. FROZEN CRITERIA

Lane CFG318. Written and committed before the lane script exists. Verdict words are the recipe's section 6 words
only: PASS, CONDITIONAL, KILL, OPEN. Standing rules: kappa = 1/2 is FITTED; no knob scans and no fitting (alpha_c and
c_2 are read from committed files); nothing here says the theory is closed or that the data favour the framework; the
cold mass the CMB needs is untouched and still required.

## 0. What was read before freezing, and the not-blind statement

Read: recipe sections 1-8 and 11 and the 2026-09-26 user decisions; CFG291, CFG292, CFG294, CFG311, CFG312 READMEs;
CFG291 and CFG311 scripts (window inputs, Barausse-2019 radiative coefficients, the NS sensitivity table).

Literature, through a summarising fetch tool (arXiv abstract pages, ar5iv HTML and the arXiv export API; values are
PROVISIONAL, the summariser is not the table). One fetch of an arXiv PDF URL (Ramos & Barausse) returned binary
content that the tool saved automatically outside the repository; it was not read and nothing below rests on it.
- Barausse, Jacobson & Sotiriou 2011, PRD 83 124043 (arXiv:1104.2889). Static spherical BHs regular at the spin-0
  horizon exist across the explored viable ranges; deviations from Schwarzschild "typically no more than a few
  percent"; universal horizon. Asymptotic series (their eqs. 24-26, EF coordinates, signature +---):
  F = 1 + F1 x + (1/48) c14 F1^3 x^3 + ..., B = 1 + (1/16) c14 F1^2 x^2 - (1/12) c14 F1^3 x^3 + ..., F1 = -r0, x = 1/r;
  G_N = G/(1 - c14/2); r0 = 2 G_N M.
- Blas & Sibiryakov 2011, PRD 84 124043 (arXiv:1110.2195): universal horizon in spherical Horava BHs; no non-standard
  long-range hair.
- Berglund, Bhattacharyya & Mattingly 2012, PRD 85 124019 (arXiv:1202.4497): exact c14 = 0 solution
  e(r) = 1 - r0/r - c13 r_ae^4/r^4, f = 1, (u.chi) = -sqrt(1 - r0/r + (1 - c13) r_ae^4/r^4), (s.chi) = r_ae^2/r^2;
  the spin-0 horizon coincides with the universal horizon at c14 = 0.
- Barausse & Sotiriou 2012/2013, PRL 109 181101 + erratum, and PRD 87 087504 (arXiv:1207.6370, 1212.1334): slowly
  rotating Horava BHs exist (not as Einstein-aether solutions); the khronon keeps its spherical configuration.
- **Ramos & Barausse 2019, PRD 99 024034 (arXiv:1811.07786).** Slowly MOVING BHs at O(v): for generic (alpha, beta,
  lambda) they carry curvature singularities at the spin-0 horizon (or, if made regular there, at the universal
  horizon / lose asymptotic flatness); regular only on the one-dimensional subset alpha = beta = 0, where the khronon is
  stealth, the solution is boosted Schwarzschild and BH sensitivities vanish. The singular result is numerical, at one
  point (alpha, beta, lambda) = (0.02, 0.01, 0.1) (sigma ~ 1e-3 there), plus a boundary-condition count; the authors
  state they did not explore small non-zero alpha, beta. Restated by Franchini, Herrero-Valea & Barausse 2021, PRD
  103 084012 (arXiv:2103.00929): regular slowly moving BHs "require alpha and beta to vanish exactly"; spherical
  collapse forms a regular universal horizon at alpha = beta = 0.
- EHT Sgr A* Paper VI, ApJL 930 L17 (2022) (arXiv:2311.09484) abstract: "image size is within ~10% of the Kerr
  predictions". M87* (ApJL 875 L6; Psaltis et al. PRL 125 141104): the abstracts read give no percentage.
- LVK, GW250114 spectroscopy (arXiv:2509.08099) abstract: the quadrupolar (220) frequency is bounded "within a few
  percent of the GR prediction"; arXiv:2509.08054: modes' frequencies within +-30% of Kerr. GWTC-3 TGR
  (arXiv:2112.06861) abstract: no ringdown number.
- Owen et al. 2025 (arXiv:2503.04916) abstract: "the dipole emission parameter is less than O(10^-4) at 90%
  credibility" (binary inspirals; definition not read: PROVISIONAL).

**Not blind.** Before this file I did exploratory sympy work (scratch, not committed):
- the static spherical reduced action in khronon-adapted ADM variables (N, N^r, gamma_rr) reproduces Schwarzschild +
  any maximal slicing at alpha = beta = 0, and Berglund's exact c14 = 0 family at beta != 0;
- in the K = 0 (multiplier) form the O(alpha) equations reduce to (r^2 q')' = alpha Sigma(r) with a rational
  Sigma; its large-r expansion gives e_3 = -alpha/6 (= BJS's -c14 r0^3/48 at r0 = 2M), and g^rr = e/(e + r e' +
  (alpha/2) r^2 U'^2), whose expansion gives BJS's B coefficients;
- a first number: delta b/b ~ +1.2e-3 alpha at the photon sphere.
The decision rule below was written knowing these, and knowing the Ramos-Barausse result.

## 1. Chassis and map (CFG291's map, reused)

I_CHK = I_CH + (c^3/16 pi G) Int sqrt(-g) [alpha_c a.a - c_2 K^2], beta = 0, mostly-plus signature. Map onto
khronometric/Einstein-aether: alpha = c14 = alpha_c, beta = c13 = 0, lambda = c2 = c_2 (CFG291 C4). Window (L340 P1,
read from `real_research/g03_audit_2026/L340_filtered_khronon_completion_results.json`): alpha_c in [9.624e-14, 3.2e-9],
c_2 in [7.2888e-3, 0.0667]; c_S^2 = c_2(2 - alpha_c)/(alpha_c(2 + 3 c_2)), c_S >= 444 c. Scored grid W: 9 x 9 log grid
over the window (corners included).

## 2. Equations (DERIVED in-lane with sympy; ADOPTED items marked)

- **(D1) Reduced action** (static, spherical, khronon time T, areal r): L = N sqrt(A) r^2 [(1-beta) K.K - (1+lambda) K^2
  + 3R + alpha (N'/N)^2/A], K^r_r = -(V A'/A + 2V')/(2N), K^th_th = -V/(rN), V = N^r, A = gamma_rr. Euler-Lagrange in
  N, V, A (symmetric criticality; the gamma_theta-theta equation follows from the radial-diffeo identity, the khronon
  equation from the metric equations).
- **(D2) O(alpha) static solution.** At alpha = beta = 0 every maximal slicing (K = 0) of Schwarzschild solves D1 for
  any lambda; regularity at the universal horizon fixes C = 3 sqrt(3) M^2/4, r_UH = 3M/2. At O(alpha) the khronon
  equation forces K = O(alpha/lambda), so lambda K = O(alpha) acts as a multiplier mu: the exterior O(alpha) metric
  is the K = 0 multiplier system, lambda-independent, with corrections O(alpha/lambda) <= 4.4e-7 relative. Derived
  objects: Sigma(r), q(r) = Int_r^inf ds s^-2 Int_s^inf Sigma, e(r) = -g_tt = 1 - 2M/r + alpha q(r), g^rr as above.
  Mass normalisation: the 1/r coefficient of e defines r0 = 2 G_N M (BJS); e -> 1 fixes the time unit. The O(alpha)
  khronon-charge shift c1 must drop out of e and g^rr (checked).
- **(D3) Observables** (photons and test bodies follow g: recipe I2).
  - Photon sphere d(e/r^2)/dr = 0; shadow b_c = r_ph/sqrt(e(r_ph)); fractional delta_sh = b_c/(3 sqrt(3) M) - 1.
  - ISCO from e alone (circular-orbit L^2 = r^3 e'/(2e - r e'), d L^2/dr = 0); delta r_ISCO, delta Omega_ISCO.
  - QNM, eikonal (ADOPTED: Cardoso et al. 2009 light-ring correspondence, valid because the tensor cone is g's light
    cone, c_T = 1, CFG292 T1): omega = l Omega_c - i (n + 1/2) lambda_L, Omega_c = sqrt(e)/r at r_ph, lambda_L from
    (dr/dt)^2 = g^rr e (1 - e b_c^2/r^2). Fractional delta f, delta tau.
  - QNM l = 2 test scalar field on the deformed metric, 3rd-order WKB (Iyer & Will 1987): reading only.
  - BH dipole: Barausse 2019's dipole coefficient C (CFG291 coeffs) in the GW band, where the khronon wavelength is
    << xi so the wave-zone factor is 1; B_dip = (5/32) C (s1 - s2)^2.
- **(D4) Neutron stars.** Static star, khronon aligned (V = 0, K = 0), alpha (N'/N)^2 term kept; D1 + perfect fluid
  16 pi N sqrt(A) r^2 p(mu_0/N). Same Read et al. 2009 piecewise polytropes as CFG311 (parameters recalled, as there).
  Mass from the exterior: N^2 -> 1 - r0/r, M = r0 (1 - alpha/2)/2 (G_N). Regularity: N'(0) = 0, A(0) = 1, smooth
  across the surface. CFG311's moving-star khronon equation (r^2 e^{2Phi-Lambda} F')' = 2 e^{2Phi+Lambda} F has no
  singular point (coefficient > 0) on any TOV star: checked.
- **(D5) MOND / heat filter near a BH.** Filter suppression exp(-xi^2 k^2/2) at k = 1/r_ph; the MOND-sector force is
  bounded by h_mono(y_f) a0 for any filtered field y_f (nu_mono reimplemented and matched to L340's committed A1
  numbers); epsilon_MOND = h_mono,max a0 / g(r_ph). For M87* (6.5e9 Msun), Sgr A* (4.0e6 Msun), 10 Msun.

## 3. Bounds used (cited above; PROVISIONAL)

- Shadow: |delta_sh| <= 0.10 (EHT Sgr A* VI). Applies to M87* too: delta_sh is scale-free (a pure number times alpha).
- Ringdown: |delta f_220|, |delta tau_220| <= 0.01, a deliberately strict floor under "a few percent" (GW250114).
- ISCO: no published bound used; reported against 1% as a reading.
- Dipole: B_dip <= 1e-4 (Owen et al. 2025). s_BH is NOT computed in this lane (section 5).
- NS: |delta M_max/M_max| <= 0.01 as a reading (the 2.01 Msun mass is +-0.04).

## 4. Controls (each can fail)

Load-bearing:
- **C1 alpha -> 0:** e = 1 - 2M/r and g^rr = e exactly (Schwarzschild); every derived deviation is proportional to
  alpha; the alpha = beta = 0 maximal-slicing family solves D1 symbolically for symbolic lambda and C.
- **C2 published BH (Berglund et al. 2012):** the c14 = 0 family solves D1 exactly at beta != 0; regularity (double
  root of (u.chi)^2) gives r_UH = 3 r0/4 and r_ae^4 = 27 r0^4/(256 (1 - c13)), checked at c13 = 0, 0.3.
- **C3 published asymptotics (BJS eqs. 24-25):** at O(alpha) the e series has x^3 coefficient -alpha r0^3/48 and the
  EF B series has +alpha r0^2/16 x^2 and +alpha r0^3/12 x^3, exactly (sympy series of the derived solution).
- **C4 Schwarzschild numbers at alpha = 0:** r_ph = 3M, b_c = 3 sqrt(3) M, r_ISCO = 6M, M Omega_c = M lambda_L =
  1/(3 sqrt(3)) to 1e-10; WKB l = 2 scalar n = 0 within 1% of 0.4836 - 0.0968i (recalled).
- **C5 numerics:** q by two quadratures (nested mpmath; closed-form inner integral) agree to 1e-12; the series to
  O(x^8) matches q at r = 50 to 1e-10.
- **C6 injection:** the scorer must flag an injected 20% shadow deviation and a 5% QNM deviation.
- **C7 kernel:** nu_mono reproduces L340's y_p, h_p to 1e-4.
- **C8 NS TOV at alpha = 0** reproduces CFG311's recalled SLy M_max 2.049 within 2%; the centre is regular.

Reading: WKB l = 2 shifts; NS M_max slope; the perturbative near-UH behaviour (q ~ x ln x in the K = 0 form, and
the finite-lambda estimate K_1 ~ (alpha/lambda)/x^2) as a sign of a boundary layer of width ~ M/c_S inside the
Killing horizon.

**MUTATE** (`CFG318_MUTATE=1`, separate `_MUTATE` outputs): alpha = 0.1 (outside the window). It must be flagged; the
run must exit rc = 1. Flags available: the window gate (alpha > 3.2e-9; PPN |alpha2| ~ alpha/2 = 0.05 >> 1.6e-9) and
the observables. Pre-registered expectation: at O(alpha) delta_sh ~ 1e-4, so EHT and ringdown will NOT flag alpha =
0.1; the flag is the window gate. That is reported as found, not hidden.

## 5. Decision rule (frozen)

- **OPEN:** a load-bearing control (C1-C8) fails.
- Dipole scoring: BBH, Delta s = 0 for non-spinning BHs (a vacuum BH's sensitivity is a pure number, independent of
  mass); NS-BH, Delta s = s_NS (CFG311's max over EOS at 1.4 Msun ... 2.01 Msun) with s_BH = 0 (its alpha = beta = 0
  value), and the critical s_crit (B_dip = 1e-4) is reported; a dipole failure would need |s_BH| >= s_crit, which is
  part of the named condition.
- **KILL:** a scored observable (shadow, ringdown, dipole as just defined; NS reading excluded) fails at any W
  point; or a regularity failure of static or slowly moving BHs is DEMONSTRATED at a point
  inside the window, by an in-lane computation or a published computation at such a point, or by a published analytic
  proof covering every alpha > 0 at beta = 0.
- **CONDITIONAL:** every scored observable passes at every W point and the static O(alpha) exterior is regular, but
  the regularity of slowly moving (or rotating) BHs at alpha_c != 0 inside the window is neither established nor
  demonstrated to fail there. The condition is named in the README.
- **PASS (at the stated scope):** all of the above pass AND static and slowly moving BH regularity is established at
  window points (in-lane or published at window alpha).
- **Owner flag:** Ramos & Barausse's boundary-condition count is generic in alpha != 0. If the owner reads it as a
  proof for every alpha > 0, G11 reads KILL for the chassis (which needs alpha_c > 0). This lane does not make that
  call; it reports it.

Every script ends with "N/M checks pass"; main and MUTATE outputs go to separate files.

## 6. What this lane cannot say

- Leading order in alpha_c, beta = 0, alpha/lambda << 1; exterior metric only. The near-UH interior is
  non-perturbative (boundary layer); static existence there rests on BJS's numerics (which did not reach alpha ~ 1e-9).
- No moving-BH computation at alpha != 0; no BH sensitivity computed.
- QNMs: eikonal order for the tensor modes; l = 2 only for a test scalar. The direct khronon coupling of finite-l
  gravitational perturbations is not derived.
- One gate on one chassis. It is not "the theory works".

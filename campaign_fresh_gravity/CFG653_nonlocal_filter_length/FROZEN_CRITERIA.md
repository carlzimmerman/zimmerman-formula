# CFG653 FROZEN CRITERIA: can the filter length of the nonlocal response be DERIVED from the framework?

Committed alone, before any CFG653 script or number exists. kappa = 1/2 FITTED. Both footings
(canonical a0 = 9.3603e-11, alt 1.1312e-10 m/s^2) are scored separately and never pooled. "Cold energy" naming.
No LCDM or standard-MOND yardstick enters a verdict; standard formulations appear only as labelled context.
Not theory closed whatever the outcome.

## 0. The object under test (astra, read as data)

sol61_push/nonlocal_response_2026_10_12 (RESULT.txt, calculate.py): with C = 4 pi G, q = grad Phi,
p(g) = g - B(g) (B the inverse of the law g = F(g_N), the repaired nu_mono kernel) and the componentwise
high-pass filter P_L with Fourier symbol H(k) = 1 - exp(-k^2 L^2 / 2), the stationary equation is

    div { q - P_L[ p(|z|) z/|z| ] } = C rho_b ,   z = P_L q .

It is exactly blind to an added uniform gradient for every L. L is an undetermined input.

Disclosed before any number: in this convention P_L = 1 - (Gaussian smoothing of width L). Hence
L -> infinity gives H = 1 on every non-zero mode, i.e. the LOCAL response (with its external-field effect for any
host at finite distance; only an exactly uniform gradient is removed), and L -> 0 gives H = 0, i.e. NO response
(Newton). The brief's MUTATE wording ("L -> 0 recovers the local response and its EFE; L -> infinity recovers the
exact uniform-gradient insensitivity") is therefore mapped onto what the mathematics gives: M1 and M3 below.
No construction in this family has a local L -> 0 limit; this is stated, not hidden.

## 1. Candidate filter lengths (zero new constants)

- C1  r_M = sqrt(G M_b / a0) of the system (system-dependent).
- C2a c^2 / a0 (universal; footing-dependent).
- C2b l_dS = c / H_Lambda, H_Lambda^2 = 8 pi G rho_Lambda / 3, rho_Lambda from FP0 (universal).
- C3a r_ta: CFG4_target.py's own turnaround radius: where the law's isolated enclosed mass M_b nu(g_N/a0) falls to
      Delta_ta(0) = 11.81 times rho_m (Omega_m = 0.3153, h = 0.6733167, as CFG4 uses). Flagged: rho_m and
      Delta_ta are CFG4's cosmological inputs.
- C3b r_zg: the dark-energy balance radius where the law's acceleration equals (8 pi G rho_Lambda / 3) r
      (law + rho_DE only).
- C4  any length singled out by astra's construction. Declared expectation: none (L enters only through H; the
      construction fixes only the separation ratio k_g/k_e >= 8.43 at b = 0.01, eps = 0.1). C4 is answered by a
      constant-L WINDOW SCAN, L in {1, 3, 10, 30, 100, 300, 1e3, 3e3, 1e4, 1e5, 1e6, 1e7} kpc plus C2a/C2b:
      the set of constant L passing gates (a) and (b) on both footings. If empty: no constant filter length
      passes. If not empty: any L picked inside it is a KNOB unless a framework length lands inside it.

System assignment for C1/C3a/C3b (frozen). PRIMARY: the outermost bound system containing the point (the
record's FG001/CFG24 convention): SPARC galaxy = itself; cluster satellite = the cluster; solar-neighbourhood wide
binary = the Milky Way, with the Local Group reported as a variant. SECONDARY: the object's own system.
If only one assignment passes, the assignment is a choice and the verdict is KNOB.
Masses: SPARC M_b = r^2 g_bar at the last rotmod point (at the profiled Upsilon); satellite M_b = 1.2 M_* (as
CFG478); cluster M_b = f M200 with f in {0.10, 0.20} (both reported; verdict must hold for both); MW M_b = 6e10,
Local Group 2e11 Msun; binary = its own mass (pipeline population).

## 2. Computation

Spherical reimplementation of astra's equation in R^3, exact for spherical sources: the Gaussian filter acts on the
enclosed-"mass" function m = r^2 g through the analytic smoothed-shell enclosed fraction
W(r, a) = 1/2[erfc((a-r)/(L sqrt2)) - erfc((a+r)/(L sqrt2))] - L/(a sqrt(2 pi)) [e^{-(r-a)^2/2L^2} - e^{-(r+a)^2/2L^2}],
on a log grid out to >= 30 L (and >= 1e3 kpc) with the data radii inserted exactly; Newton-Krylov solve.
SPARC discs enter as the spherical-equivalent source m_N = r^2 g_bar (the rotmod statistic's own convention;
L -> infinity reproduces the algebraic law exactly). Beyond the last point m_N is constant; inside the first point
m_N ~ r^3.

## 3. Gates (per candidate, per footing)

(a) RAR. CFG4's statistic exactly (weighted rms of log g_obs - log g_pred, weights (V/eV)^2 clipped at 1 km/s,
    Upsilon_bul = 1.4 Upsilon_disk, one global Upsilon_disk profiled on 0.30-1.20: coarse 0.05 then fine 0.01).
    Local law baseline (must reproduce, K1): nu_mono 0.1003 @ 0.61 canonical, 0.0991 @ 0.57 alt.
    PASS: rms <= local + 0.005 dex and Upsilon in 0.50-0.80; TENSION: <= local + 0.010; FAIL otherwise.
(b) R7, quantitatively at what CFG447/CFG478 constrain.
    (b1) Cluster satellites (CFG478 data, host NFW M200 6e14 c 4, satellites at <R_sat>, r_bg as cm14b):
         residual host field f_res = (P_L q_host)(R)/q_host(R) from filtering the host's total field; satellite
         M_tot = M_b min(B_self(L), B_EFE(f_res g_e)) + ret, where B_self is the satellite's isolated nonlocal boost
         at r_bg and B_EFE is CFG478's exact enclosed-phantom boost with the host field scaled by f_res. The min is
         an OPTIMISTIC combination (it assumes the two suppressions do not compound): a FAIL is robust, a PASS is
         "not excluded at this approximation". PASS: chi^2/5 with p >= 0.01 (CFG478's exclusion threshold) for
         nu_mono on the footing; FAIL: p < 0.01.
    (b2) Wide binaries (CFG447 machinery: the frozen DR4 pipeline imported read-only, sha256 checked; 10 mocks,
         N = 6,210, DR3 noise; seeds 47001-47010; master 1e6): injected velocity boost gamma = sqrt(B) with B
         the enclosed-mass boost of the binary under the candidate: residual MW field g_e,eff = f_res x 1.9 a0
         (the pipeline's banked field) entered as a Newtonian field through the law's inverse, binary self-field
         filtered when L is not >> s (exact spherical nonlocal boost at y = g_true/a0). Recovered gamma_hat vs
         DR3 builder 1.0750 +- 0.0550 (canonical) / 1.0775 +- 0.0512 (alt):
         z <= 2 PASS; 2 < z <= 5 TENSION; z > 5 FAIL (CFG447's own exclusion threshold).
    R7 gate PASS needs (b1) and (b2) PASS (TENSION in b2 alone -> R7 TENSION).
    Context, not a gate: any gamma != 1 changes the sealed DR4 prediction (Amendment 21: exactly Newtonian).
(c) Well-posedness: (c1) variational (Euler-Lagrange of a single functional); (c2) static convexity: the filter
    operator used is self-adjoint, a contraction and annihilates constants (checked numerically, including the
    variable-width form P = 1 - exp(div (L(x)^2/2) grad) needed for system-dependent L); (c3) L fixed by rho_b
    without a free choice (a segmentation rule from the record is allowed but its discontinuity across system
    boundaries is measured: a realistic merger of two equal MW-mass galaxies must not move the outer RAR
    prediction by more than 0.005 dex, else CONDITIONAL); (c4) static-limit causality: the filter's 1%-weight
    radius 3.37 L must lie inside the dark-energy horizon l_dS = c/H_Lambda.
    PASS: c1, c2, c4 and (c3 or CONDITIONAL); FAIL otherwise.

Verdict per candidate: DERIVED-AND-PASSES (framework-only, no choice, a+b+c PASS on both footings) /
FAILS (named gate[s]) / KNOB (passing needs a choice of length, multiplier or assignment).

## 4. Controls and MUTATE

K1 local-law reproduction (above) to 1e-4 dex. K2 the spherical solver against astra's own 3D periodic solver
(calculate.py's functions re-executed read-only in a scratch copy, box 128, N = 64, Gaussian width 2, mass 4 pi,
L = 4 and 8): radial-force relative L2 over 4 <= r <= 12 within 3%. K3 CFG478 reproduction: f_res = 1, B_self = isolated
reproduces CFG478 Q1 nu_mono chi^2 (98.7 / 94.6) to 0.1. K4 CFG447 reproduction: f_res = 0 with unfiltered
self-field gives the EFE-blind recovery pinned at the grid top (>= 1.5) as CFG447.
M1 L = 1e12 kpc: SPARC rms equals the local law to 1e-4 dex; f_res >= 0.999 for both hosts (local EFE back).
M2 L = 1e-6 kpc: SPARC rms equals Newton's to 1e-3 dex; satellite and binary boosts -> 1.
M3 astra's uniform-gradient invariance re-run (3D, external gradient 0.1) at L = 4, 8: residual change <= 1e-9.
MUTATE run (--mutate) executes M1-M3 and writes _MUTATE outputs; it must DETECT (M1, M2 limits reached).

Resources: one process, nice -n 10, <= 2 GB, single-threaded BLAS; no downloads; the running 1024^3 job and its
waiters are not touched.

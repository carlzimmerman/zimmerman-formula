# FROZEN A27: exhaustive dimensional search for the rho_DE tie from LCDM's own quantities

Frozen before any A27 number. Script `scripts/recipe29.py`, output `scripts/recipe29.out`. Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing (one API check only, no candidate graded): colossus peaks.nonLinearMass at z = 0 in the folder cosmology returns about 6.4e12 Msun, falling to about 2.6e9 Msun by z 2.33. Known from A13 and A24: c^2 sqrt(Lambda/3)/2 pi gives kappa_eff 0.461, c H_inf/6 gives 0.482.

## Question
Could a rival "find" a = kappa c sqrt(G rho_DE), kappa = 1/2, just by combining LCDM's own quantities with c and G? How many dimensionally valid accelerations land on the tie by chance, and does any of them survive with a mechanism (G5)?

## Search space (fixed now)
Base cosmology = lib.py: flat, H0 67.4, Om0 0.315, Ob0 0.0493, sigma8 0.811, ns 0.965, no relativistic species in colossus. Constants G 6.674e-11, c 2.998e8, Msun 1.989e30, kpc 3.0857e19 (from lib). Target a_T = 0.5 c sqrt(G rho_DE), rho_DE = Ode0 rho_crit0.

Ingredients, 15 (dimension L, T, M):
- dimensional: H0 (T^-1); Lambda = 8 pi G rho_DE / c^2 (L^-2); rho_L = rho_DE; rho_m0; rho_b0; rho_c0 (each M L^-3); rho_g0 = 4 sigma_SB T_CMB^4 / c^3 with T_CMB 2.7255 K (the T_CMB ingredient; c^p G^q alone cannot make T_CMB dimensionally valid, so it enters through its photon density; neutrinos left out, as in lib); t_age (T); L_H = c/H0 (L); M_* where sigma(M) = 1.686 (colossus peaks.nonLinearMass, Eisenstein-Hu 98, M); V_* = virial velocity of an M_* halo at 200c (L T^-1); g_* = G M_*/R200(M_*)^2, its virial acceleration (L T^-2).
- dimensionless: f_b = Omega_b/Omega_m; sigma_8; n_s.
Products of 1 to 3 distinct ingredients, each exponent in {-2, -3/2, -1, -1/2, 1/2, 1, 3/2, 2}, times c^p G^q with p, q solved for (any rational; no bound). A product is dimensionally valid only if q = M-exponent and the L and T equations agree (equivalently L + T + M exponent sum = -1). Prefactor: one element of P = {1, 2, 1/2, pi, 2 pi, 1/(2 pi), 4 pi, 1/(4 pi), 6, 1/6, sqrt 3, 1/sqrt 3} (12). Sensitivity run (look-elsewhere only, not the primary grade): prefactor = product of any two elements of P (unique values), which contains Milgrom's 1/(2 pi sqrt 3).
Counting: N_expr = every (ingredient set, exponents, prefactor) that is valid; N_val = distinct log10 values rounded to 1e-4 dex; families = distinct functional forms, keyed on (G2 slope, G3 ratios, footing-B slope) rounded to 1e-4.

## Gates
- G1 |log10(a / a_T)| <= 0.05 today, base cosmology (kappa_eff within 0.05 dex of 0.5).
- G2 slope d ln a / d ln rho_DE = 0.50 +- 0.05, varying rho_DE alone by factors 0.8 and 1.25 (both slopes must pass), flat, at fixed physical omega_m = Om0 h^2 and omega_b = Ob0 h^2, fixed T_CMB, n_s. So h^2 = omega_m + f omega_DE, Om0' = omega_m/h'^2. Two footings: A (primary for nothing; reported) sigma8 held fixed at 0.811; B (primary) fixed primordial amplitude: sigma8' set so that sigma at physical radius 8 Mpc/h0 at z = 30 equals the base value (same transfer function in physical k, same matter-era growth). A survivor must pass G2 on footing B; footing A is also reported. M_*, V_*, g_*, t_age, H0, rho_c0, Lambda recomputed in each cosmology.
- G3 a(z)/a(0) inside [0.76,1.03], [0.71,1.12], [0.33,1.21] at z 1, 1.5, 2.33, each ingredient on its own evolution: H(z); Lambda and rho_L constant; rho_m, rho_b (1+z)^3; rho_c = 3 H(z)^2/8 pi G; rho_g (1+z)^4; t_age = age at z; L_H = c/H(z); M_*(z) from nonLinearMass(z); V_*, g_* at 200c of rho_crit(z); sigma_8(z) = sigma_8 D(z) (colossus growth factor, normalised 1 today); f_b, n_s constant.
- G4 one constant across galaxy hosts log M200 11 to 12.5, rms <= 0.1 dex: every candidate is a cosmology-wide number with no host-mass dependence, so G4 passes for all by construction (stated, not a result).
- G5 operative at galaxy radii, judged for each full survivor (G1 + G2B + G3): each dimensional ingredient is mapped to the acceleration its physical field exerts at r = 10 kpc in a disc host: Lambda, rho_L: Lambda c^2 r/3; H0, t_age, L_H: |q0| H0^2 r; rho_m0, rho_b0, rho_c0, rho_g0: background pull (4 pi G/3) rho r (an upper bound, since inside a bound halo the mean background is not a separate field); M_*, V_*, g_*: an M_* halo is present only in hosts of that mass, so operative for disc hosts only if log M_* lies in 11 to 12.5, and then NFW (Diemer19 c) enclosed g at 10 kpc of an M_* halo. G5 passes only if the largest mapped acceleration is >= 0.1 a_T (A13's rule). Dimensionless ingredients carry no field.

## Look-elsewhere (fixed now)
- Observed G1 hits K1 and full hits K123 (G1 + G2B + G3), counted on expressions and on distinct values.
- Chance expectation: slide the target over log offsets delta in [-1.5, +1.5] dex, step 0.01, excluding |delta| < 0.1 (the real window), and count hits on distinct values for each delta. Report mean, 16th and 84th percentiles, for G1 alone and for G1 + G2B + G3 (G2 and G3 do not depend on delta). Poisson tail P(N >= K | mean).
- Reading, fixed now: if the observed full-hit count is within the 84th percentile of the slid counts, or Poisson P > 0.01, the full survivors are numerology (a dense enough lattice hits any 0.1 dex window). Beyond chance would be notable and listed prominently. Same done on the two-element prefactor sensitivity run.
- Non-Lambda survivors: any full survivor whose dimensional ingredients do not include Lambda or rho_L is listed prominently.

## Expected in advance
The enumeration contains the tie itself, (1/2) c sqrt(G rho_L), and Lambda-variants (c^2 sqrt(Lambda) with prefactors; times powers of f_b, n_s, sigma_8). Full survivors are the Lambda / rho_L^(1/2) family dressed with dimensionless constants (n_s and f_b on footing B; sigma_8 terms fail G3 by D(z) and footing B's G2 for odd powers maybe) and they fail G5 (Lambda pull at 10 kpc about 1e-5 a0). G1 hits number in the hundreds or more, at or near the slid expectation, so G1 alone is numerology. H0-only forms fail G2 (slope 0.5 Ode0, about 0.34) and G3; M_* forms fail G3 (M_* falls 3 decades by z 2.33). No non-Lambda full survivor expected; if one appears it is checked by hand before anything is written.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

Two runs, each under a minute, peak RSS 248 MB, single thread. Lines quoted from `scripts/recipe29.out`. The first output is kept as `scripts/recipe29_before_fix.out` (see Deviations); every gate number is identical in both.

Base: c sqrt(G rho_DE) = 1.8727e-10, a_T = 9.3637e-11 (lib A0 9.3625e-11); M_* = 6.36e12 Msun (log 12.80), falling to 3.1e-2, 5.8e-3, 4.2e-4 of that at z 1, 1.5, 2.33. G2 cosmologies: f 0.8 gives h 0.6261, footing-B sigma8 0.7967; f 1.25 gives h 0.7294, sigma8 0.8249 (z = 30 match 1.00000). Checks: Milgrom c^2 sqrt(Lambda/3)/2 pi gives kappa_eff 0.4607 (A13 0.461); (1/2) c sqrt(G rho_L) gives 0.5000.

Counting: 239,800 ingredient-exponent products, 16,632 dimensionally valid; x 12 prefactors = N_expr 199,584, N_val 103,819 distinct values at 1e-4 dex (150,082 at 1e-7), 2,551 functional families; log10(a/a_T) spans -34.5 to +33.1, 65,192 expressions within 1.5 dex. Products alone: G2 footing B passes 671, footing A 966, G3 702, G2B + G3 377.

G1: 2,403 expressions, 817 distinct values (1,643 at 1e-7). Full G1 + G2(B) + G3 (+ G4 by construction): 104 expressions, 63 distinct values (73 at 1e-7); on footing A 76 expressions. Of the 2,403 G1 hits, 174 pass G2B and 149 pass G3.

Look-elsewhere (target slid over 282 offsets, |delta| 0.1 to 1.5 dex):
- G1, frozen 1e-4 distinct: chance mean 782.5 (16-84 % 745-813), observed 817, 9.2 % of offsets reach it: WITHIN CHANCE.
- Full, frozen 1e-4 distinct: chance mean 62.1 (44-80), observed 63, 54 % of offsets reach it: WITHIN CHANCE.
- Fix rows: full at 1e-7 distinct mean 70.8 (50-91), observed 73; full on expressions mean 94.3 (61-123), observed 104: WITHIN CHANCE. G1 on expressions mean 2,153 (1,884-2,369), observed 2,403, 10.3 % of offsets reach it; the script's rule marks it BEYOND CHANCE because the Poisson tail is tiny, but the expressions cluster (slid spread is about 10 times the Poisson width), so the Poisson test does not apply there and the offset fraction (10 %) is the honest number. G1 alone is not the deciding gate.
- Two-element prefactor sensitivity: N_expr 964,656; full hits 217 distinct (mean 201.3, 160-236), 313 at 1e-7 (mean 292.3), 442 expressions (mean 412.0): WITHIN CHANCE.
So the tie's number falls where a lattice this dense lands anyway: numerology, about as many hits as at any other target 0.1 to 1.5 dex away.

Full survivors, G5: all 104 FAIL G5. Lambda and rho_L pull at 10 kpc 1.1e-5 a_T; H0, t_age, L_H Hubble deceleration 8.3e-6 a_T; background density pulls 4e-7 to 8e-6 a_T; M_* (log 12.80) lies outside the disc-host range, and no M_*, V_* or g_* form reaches the full set anyway (g_* forms fail G2B and/or G3).
- 76 survivors are the Lambda / rho_L^(1/2) family (slope exactly 0.500, flat in z) dressed with powers of f_b, n_s, or rho_b/rho_m, H0 L_H, rho_L/rho_c ratios; this includes the tie itself, (1/2) c sqrt(G rho_L), and many exact rewritings of it.
- NON-LAMBDA SURVIVORS, 28 expressions in two families, both on footing B only (0 of them on footing A), both G5 FAIL:
  - F1 = c H0 sigma_8^(3/2) x (prefactor, f_b, n_s powers), 26 expressions (also written c sqrt(G rho_c0) sigma_8^(3/2), c^2/L_H sigma_8^(3/2)); best "1/sqrt3 c G^1/2 rho_c0^1/2 sigma8^3/2 n_s^1/2" kappa_eff 0.5005, "pi c H0 f_b^3/2 sigma8^3/2" 0.4968. Footing-B slopes +0.4500 at f 0.8 (0.450006 by hand: a pass by 6e-6) and +0.4686 at 1.25; footing A +0.330, +0.354 FAIL. a(z)/a(0) 0.846, 0.826, 0.813: H(z) rises while sigma_8 D(z)^(3/2) falls, and inside the wide E5 bands they nearly cancel (diagnostic: 0.89 at z 0.5, 0.81 at z 3 to 4). Diagnostic slopes at other f: 0.438 at f 0.64 (fails), 0.456 at 0.9, 0.464 at 1.1, 0.475 at 1.5625. So F1 sits on the G2 edge and only on the fixed-amplitude footing.
  - F2 = (1/6) c H0^(3/2) t_age^(1/2) sigma_8, 2 expressions, kappa_eff 0.4609 (-0.035 dex); footing B slopes +0.504, +0.529 (footing A 0.424, 0.453 FAIL); a(z)/a(0) 0.946, 1.004, 1.119, rising past the band by z 3 (1.21, 1.35 at z 4, diagnostic).
  Neither has an LCDM process behind it: there is no term in which a halo feels c H0 times the amplitude of fluctuations to the 3/2. They are lattice products that happen to sit inside the bands, and their count is within the slid chance.

## Deviations
1. After the first run, before writing anything: the frozen distinct-value count rounds at 1e-4 dex, which caps a 0.1 dex window at 1,001 values. The two-element sensitivity run sat at the cap (1,001 observed, chance mean 997.8), so its frozen G1 reading is uninformative. Added the same slide on 1e-7 dex distinct values and on raw expression counts; the frozen rows are still printed unchanged. First output kept as `scripts/recipe29_before_fix.out`; all gate counts identical.
2. Added a diagnostic block (finer z grid, more rho_DE factors) to check the non-Lambda families by direct colossus calls. It grades nothing.
3. Expected in advance "no non-Lambda full survivor": wrong. Two non-Lambda families pass G1 to G4, on footing B only, F1 by 6e-6 on the G2 edge; both fail G5 and footing A.
4. G5 explanation strings are built from a Python set, so their order changes between runs; content identical.

Provisional: none from the web; no look-ups used. The Eisenstein-Hu 98 power spectrum, colossus growth, and the fixed-amplitude footing (matching sigma at z 30) are this script's choices.

Verdict: a rival can "find" the tie by dimensional search, as the target itself and its Lambda rewritings, plus two non-Lambda look-alikes on one footing, but the number of hits is what a lattice of 2e5 to 1e6 expressions gives at any target, so this is numerology. No full survivor passes G5: no LCDM process carries any of these scales to galaxy radii. The rho_DE tie stays a hand term on the LCDM side.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

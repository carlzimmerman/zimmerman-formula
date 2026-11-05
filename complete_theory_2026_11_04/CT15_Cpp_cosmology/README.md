# CT15_Cpp_cosmology: C'' FAILS G5 WITH ANY FITTED DUST AMOUNT. Its dust is v3s's khronon, which is not dust at recombination at the mu_K galaxies allow. Max H3/H2 is 0.557 (mu_K 0.03 and 0.1 Mpc^-1, n_s 0.9649), against the window 0.969-0.989. A separate standard dust passes only with omega_x/omega_b 4.98-5.32, and that dust is the record's "CDM under another name"

Criteria `FROZEN_CRITERIA.md` (written first). Script `ct15_cpp_cosmology.py`; numbers `ct15_cpp_cosmology.out` (cited as out:line) and `ct15_cpp_cosmology.json`. The CMB runs use Q6's validated khronon CLASS (sha256 3ccb50b2..., re-checked). Background runs use vanilla classy 3.3.4. 79 runs, 337 s, one thread, peak 0.17 GB. No download. Graded under the owner's follow-up to D1 ("Yes, grade it"), with the dust amount counted as a fitted constant. This is a go to grade, not an adoption. The 2026-11-01 retirement stands. No particle. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## Step 1: C''s linear cosmology (the frozen decision, FROZEN_CRITERIA.md)

**What the dust is.** The dust is v3s's khronon charge, with alpha ≡ 1 (V3_FULL_PICTURE.md §4.1).

**How its perturbations behave.** At linear order the khronon is a fluid with J'(0) = -1, and its self-force kernel is s = a^2 mu_K^2/(k^2 + a^2 mu_K^2) (Q6 D2/D5). It acts as CDM only in the limit mu_K -> infinity. At the mu_K that galaxies allow (< 0.1 Mpc^-1, S4), it is radiation-like until z ≈ 35-78 (V3_FULL_PICTURE.md:108-109). The CMB needs dust by z ≥ 3e4 (V3S_FINAL_VERDICT:234, :492).

**No MOND-sector linear effect.** a0 is absent from linear FRW (Q6 README:28-29). On FRW, L_M = dL_M/drho = 0 (CT13 R6). So the MOND sector adds no linear growth enhancement.

**What phi is.** phi is plain thawing quintessence with c_s^2 = 1 and no Lambda.

**Verdict on the stand-in.** CLASS with standard cold dust is not a faithful stand-in. The correction is to replace the dust's perturbations with the khronon kernel, done here with Q6's LOB build: a dust background with the literal perturbations, the most favourable reading, since the literal K has no radiation era (Q6 finding 1). A fitted amount cannot help, because the phase does not cluster at recombination.

## Step 2: G5 and the background
| Dust model | H3/H2 over omega_x 0-0.48 (n_s 0.9649) | Fitted omega_x | G5 |
|---|---|---|---|
| khronon, mu_K 0.1 Mpc^-1 | 0.527 to 0.556 (out:4) | none reaches 0.979 at any n_s (max 0.565, out:5) | **FAIL** (out:6) |
| khronon, mu_K 0.03 Mpc^-1 | 0.527 to 0.557 (out:8) | none (max 0.566, out:9) | **FAIL** (out:10) |
| khronon, BS cap 10 Mpc^-1 (excluded by S4, reported) | at most 0.678 (out:16) | none | FAIL (out:18) |
| standard dust (not faithful) | 0.527 to 1.531 (out:12) | 0.1192 / 0.1153 / 0.1116 at n_s 0.93 / 0.9649 / 1.0. Ratio 5.32 / 5.15 / 4.98, inside 4.9-5.4 (out:11-14) | passes only as a separate dust |

**Check.** The binary's dust row reproduces CT3's 0.992 (out:2).

**Standard-dust row at n_s 0.9649.**
- Reported checks: H2/H1 is 0.453 against raw 0.451, and the peaks sit at l 222/541/822 against raw 222/533/814 (out:12).
- BAO with phi frozen at w ≈ -1 gives chi2 53.3, a **FAIL** against the 28.3 line (out:22). CT11's Lambda reference reproduces 46.8 (out:19).
- Thawing at w0 = -0.9 gives chi2 11.9, a pass, but only with w0 as a second hand-set constant (out:23).
- SN diagonal chi2 is 694-699 for 1580 SNe (reported only).

## Step 3: growth
- **Khronon dust:** sigma8 is 0.0010 / 0.0005 (S8 0.0014 / 0.0007) at mu_K 0.1 / 0.03 (out:25-26), against raw KiDS S8 ≈ 0.77 (CT3_REPORT.md:47). That is about 3 orders of magnitude short, consistent with X4's R_B of 0.003-0.005. There is no linear MOND enhancement (Step 1), and the nonlinear J_x does not restore growth (L1).
- **Standard dust (not faithful):** S8 is 0.813, a pass (out:27).

## Hand-set constants
- kappa = 1/2. It is unused at linear order.
- omega_x, fitted. It is fitted only where a fit exists, which is the standard-dust row.
- mu_K, bounded above only.
- w0 (V's shape and phi_i).
- L*.
- A_s, tau and YHe are inherited. n_s is bracketed.

## Caveats
- LOB is a hybrid. The literal khronon has no radiation era, so the real C'' does worse.
- The TT ratio comes from diagonal errors and is not a likelihood (CT3).
- The thawing CPL mapping wa = -1.58(1 + w0) is quoted from memory and is provisional.
- Omega_L is the Lambda-shape value from SN, reused for phi.

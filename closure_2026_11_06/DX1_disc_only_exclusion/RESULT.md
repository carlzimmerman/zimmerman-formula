# DX1: disc-only exclusion (exit 3). EVERY DIRECTION DEAD; EVEN A PERFECT EXCLUSION FAILS GB1

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle. The component is cold dark energy (KD1's captured
K(Q) dust).

Order on record:
- ANALYSIS.md and FROZEN_CRITERIA.md (367d5b823a), committed alone before any script.
- Then dx1.py, which writes dx1.json / dx1.out.
- MUTATE twin: dx1_MUTATE.json / dx1_MUTATE.out.

A rerun gives a byte-identical dx1.json. Runtime about 1 s, one thread. GB1 and KD1 are used read-only.

## Labels per direction (derived in ANALYSIS.md)

| Direction | Label | Why |
|---|---|---|
| D1 matter flow vs khronon frame / P | **DEAD** | Matter is minimally coupled (QX17 E5), so kinematics reach the khronon sector only at (v/c)^2 <= 1.1e-5. The Pi_+ / Sigma_+ switches cannot amplify that: their argument is the phantom density, far above zero, and they gate terms <= 1e-10. New couplings either reduce to dead keys (bulk velocity I5, p/rho) or to support (beta_P), which QX22 rules out for early types. The one form that survives QX22, "cold discs only", is local: it acts on a layer of about 0.1 of the volume, while KD1's fluid sits static in a 0.35 pc core. It can remove at most about 0.1, against the factor 13-21 needed |
| D2 angular momentum / vorticity | **DEAD** | The khronon flow is hypersurface-orthogonal, so its vorticity is 0 everywhere. FA1 I2 is killed on both readings (ICM shear 27-130x threshold; ellipticals Z -2.15). j/(rv) is v/sigma, so QX22 applies. A gas-current-only coupling is QX23's cold-gas key, killed in SPARC |
| D3 AC2q off-branch (Sigma < 0) | **DEAD** | It needs negative phantom density below -2X. That happens at external-field saddles, not in discs. On either branch only terms <= 1e-10 change, and AC2q carries no cold component to remove |
| D4 disc formation history | **DEAD** | Contraction pulls the component in (wrong sign). Expulsion needs 5-23 % of all supernova energy put into the component through gravity alone, and the ordering is inverted: gas-poor spheroids had the most feedback and need the component, while gas-rich discs had the least and must lack it. QX23's gas-poor minus gas-rich (+0.053) goes the wrong way. Capture at turnaround is history-blind (KD1 f_cap is identical in every class) |

None was frozen as a candidate. What was frozen is the one cheap question the directions leave: **would a perfect
exclusion help?**

## The oracle bound on GB1 (not a candidate; it reads a class tag)

- **O1:**
  - f = 0 in the disc set: SPARC, KiDS late lenses, the Sun;
  - f = KD1's cosmic capture everywhere else: 4.11100 canonical / 4.11214 alt;
  - all ellipticals are "on", as QX22 requires;
  - uniform b = 1 + f.
- **O2:** O1 with QX26's IMF, b = b_imf (1 + f).

Residual = D - Delta; negative means over-predicted.

| Gate | O1 canonical | O1 alt | O2 canonical | O2 alt |
|---|---|---|---|---|
| G1 SPARC | PASS Z +0.027, rms 0.136 | PASS -0.001, 0.133 | NV; bracket PASS all | NV; bracket PASS all |
| G2 X-COP | **PASS** mean +0.004, rms 0.082 | **PASS** -0.020, 0.086 | NV; bracket PASS all (-0.016 to -0.023) | NV; bracket PASS all |
| G3 groups | FAIL 2/20 (f* 0), 0/20 (f* 1); median -0.02 / -0.20 | FAIL 3/20, 0/20 | NV; bracket FAIL all | NV; bracket FAIL all |
| G4 ellipticals | FAIL -0.368 | FAIL -0.379 | FAIL -0.504 | FAIL -0.512 |
| G5 Coma UDGs | FAIL +0.743 (+2.84 sigma_U) | FAIL +0.702 (+2.68) | FAIL +0.743 | FAIL +0.702 |
| G6 dSph (median - anchor [95 % CI]) | FAIL: bright M31 -0.180 [-0.310, +0.005]; MW classical -0.171 [-0.478, +0.172]; LG field -0.358 [-0.446, -0.221] | FAIL: -0.189 [-0.318, -0.003]; -0.179; -0.367 [-0.451, -0.230] | NV; bracket FAIL all | NV; bracket FAIL all |
| G7 KiDS split | FAIL D_cand +0.382, R -0.224 (-3.50 sigma) | FAIL +0.380, R -0.222 (-3.46) | NV; bracket FAIL all (-4.10 to -4.80 sigma) | NV; bracket FAIL all |
| G8 Solar System | PASS 0.211 | PASS 0.190 | PASS 0.211 | PASS 0.190 |
| G9 CMB lensing + growth | CARRIED PASS (KD1 at mu_K*, chi^2 8.56) | CARRIED PASS | CARRIED | CARRIED |

**Labels.**
- **O1: BOUND FAILS (G3, G4, G5, G6, G7), both footings.**
- **O2: BOUND FAILS (G4, G5); NO VERDICT (G1, G2, G3, G6, G7).** Its brackets read FAIL for G3, G6 and G7.

## What it says

1. **A perfect disc-only exclusion fixes discs and clusters at once.** With exclusion by fiat, the cosmic capture
   share alone puts X-COP on the law's line (+0.004 / -0.020, rms 0.08), with SPARC and the Solar System untouched.
   This is KD1's 4.11 against X-COP's 4.18 / 3.78, now graded. It is the closest any bound in the record has come on
   G2, but it is an oracle. No mechanism delivers it (directions D1-D4 above).
2. **Everything else goes the wrong way, by too much.** The same share over-fills:
   - the ellipticals: -0.37 dex, and -0.50 with the IMF that GB1 needs for them;
   - the groups at f* = 1: -0.20, with 0 of 20 passing;
   - the dSphs: LG field -0.36 with its CI excluding 0, and bright M31 -0.18;
   - the KiDS early lenses: -3.5 sigma.
   It still under-fills the Coma UDGs (+0.70 to +0.74).
3. **So exit 3 cannot close the triangle on its own.** Even after a perfect switch, the amount held must vary about
   100x across the hot classes:
   - ellipticals need 0.86 / 0.77;
   - dSphs 1.3-1.8;
   - groups 0.9-3.5;
   - X-COP 4.2 / 3.8;
   - Coma UDGs 78-86 (KD1's needs).
   A universally captured cold component gives 4.1 to each. Only exit 1 (several causes) could supply that spread, and
   it would have to remove most of the share from ellipticals, groups and dSphs while adding to UDGs.
4. **Classification sensitivity (reported).** If the LG field dwarfs (dIrr-rich) also count as "off":
   - LG field sits at +0.019 / +0.007, back inside;
   - canonical G6 then passes, because bright M31's CI upper end is +0.005;
   - alt G6 still fails (upper end -0.003).
   The bound's label does not change: G3, G4, G5 and G7 fail regardless.

## Checks
- **KA1:** GB1's L0 class means, |d| 4.3e-7 / 4.5e-7 (line 1e-6); UDG 0 / 2.2e-16. PASS.
- **KA2:** O1 at f_on = 0 equals gb1.json L0 on G1-G8, |d| 0. PASS both footings.
- **KA3:** O2 at f_on = 0 equals gb1.json L1, brackets included, |d| 0. PASS both footings.
- **KA4:** KD1's SPARC_f_max is re-derived as 0.325672 / 0.193712, |d| 0. PASS.
- **MUTATE (inverted oracle: the component in discs, none in hot systems):** G1 FAILS on both footings (Z -0.480 /
  -0.500, rms 0.51 / 0.52 against lines 0.146 / 0.143). The bound bites.

## Limits
- **Profile.** Uniform b is KD1's extended diagnostic convention. KD1's own 0.35 pc core over-shoots X-COP (-0.70), so
  a core profile makes every hot row worse.
- **G9 is carried, not re-run.** The argument is that a late, nonlinear disc-only exclusion leaves the linear lensing
  spectrum at L <= 400 unchanged.
- **The oracle's tags are classifications.** The ellipticals are all "on" because QX22 forces it. LG field is
  reported both ways.
- **No mechanism is claimed.** ANALYSIS.md's directions are derived or argued, not field-solved. D1's locality bound
  of about 0.1 is an order of magnitude, not a solve.

Kappa = 1/2 FITTED; not theory closed.

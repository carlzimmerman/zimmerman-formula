# HZ1: a UV completion of action (A)? Gate T3 of the TOE0 battery (2026-11-10)

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Footings canonical (a0 9.3603e-11 m/s^2) and
alt (1.1312e-10 m/s^2), never pooled. The cold component is cold dark energy (the clock's charge), never a particle. Not a
LCDM lane. No data download. Committed alone, before any script or number of this lane.

Parent: `toe_2026_11_10/TOE0_gate_battery/FROZEN_CRITERIA.md` (commit 8a99cb7c34), section 1, gate T3. This file only
tightens T3; nothing here loosens it. The theory graded is action (A) as printed in
`closure_2026_11_06/QX17_covariant_field_equations/RESULT.md` section 0.

Id check: no `HZ1_*` folder exists. `git log --grep=HZ1` finds the name only inside CFG591's commit messages, where "HZ1"
was a mass-conservation check of that lane, not a lane id. This lane is `toe_2026_11_10/HZ1_uv_completion/`, the id the
TOE0 battery reserved. The sibling lane QG1 (gate T2) is not touched.

## R. The record's UV position (quoted, not re-graded)

- June TOE map, `opus_48_extended_research/reviews/TOE_LITERATURE_MAP_2026-06-15.md`, leg (v): "UV-complete AeST host:
  ONLY-COMPATIBLE -> contested". The aether is the IR of non-projectable Horava gravity, "but the renormalizability proof
  is for the projectable branch; the viable host's renormalizability is OPEN".
- `STANDING.md` L350 (the lambda channel, 09-25): Planck-era Horava fits give c2 <= 0.6-2.9e-3 at 95 %.
- `book/31_not_a_theory_of_everything_yet_the_hones.md`: the preferred frame makes the framework an SME background that
  "induces" a gravity-sector coefficient of order 1e-12 from the known a0, "derives" nothing.

All three predate (A). They concern the June AeST-type actions and the C-H/K khronon. None of them writes (A) as a Horava
theory, none asks whether the law's function can sit in a renormalizable action, and none computes the matter-sector
Lorentz violation a UV completion would leak. That is what this lane adds.

## 0. What is computed

**(A) in unitary gauge.** tau = t, lapse N, Q = 1/N, A_i = d_i ln N, P spatial. Read off: lambda (coefficient of K^2
next to K_ij K^ij), beta (extra K_ij K^ij, so c_T^2 = 1/(1 - beta)), xi (R^(3)), and alpha(u) defined by writing the law's
term as (1/4K) alpha a_i a^i, together with its fluctuation values alpha_par = 2 J''(u), alpha_perp = 2 J'(u)/u around a
background u = |A|/a0. Here J(u) = u - ln(1 + u), so (A) at gamma_L = 0 carries + (a0^2/K) J(u) (QX17 K0). Also listed:
the clock term mu_K^2 (1/N - 1)^2/(2K) (a lapse potential: it breaks time reparametrization), the P sector, and every
non-analytic piece of (A).

**Power counting.** Anisotropic scaling [x] = -1, [t] = -z, d = 3. Dimensions: [N] = 0, [N_i] = z - 1, [gamma_ij] = 0,
[K_ij] = z, [a_i] = 1, [R_ij] = 2; the Lagrangian density carries dimension z + d. A coupling's dimension is
(z + d) - (dimension of its operator). The general z = 3 non-projectable potential (every scalar built from R_ij, a_i and
spatial derivatives, of dimension 2, 4 and 6) is listed and each coupling's dimension computed.

**J as a UV term.** Two tests, both computed (sympy):
- J1 analyticity: does J's Taylor series in u = |A|/a0 contain odd powers? An odd power of |A| = (A_i A^i)^(1/2) is not a
  polynomial in A_i, so it cannot be a vertex of a perturbative local action.
- J2 renormalizability: does J's series have non-zero terms of order n >= 7 (coupling dimension 6 - n < 0 at z = 3)?
J is **present in a power-counting renormalizable UV action** only if both answers are no.

**Generation candidates (the flow).** Each is a one-loop determinant of a field whose squared mass (or mass matrix) is a
polynomial in A_i, so the UV action stays local and polynomial. Frozen list:
- G1 the lead's candidate: a real scalar on the 3-d leaves (time-ultralocal, leaf density nu), m^2 = g^2 A_i A^i.
  3-d determinant per leaf, so L_ind = -nu V_3 with V_3 = -|m|^3/(12 pi) per real boson (universal, non-analytic part).
- G2 the fermion version: an 8-component leaf fermion with three anticommuting mass matrices coupled linearly to A_i, so
  |m| = g|A| (checked by building the Clifford matrices); Grassmann sign.
- G3 the pair: G2's fermion plus G1's boson with a bare mass, m_B^2 = m0^2 + g_B^2 A^2, and g_B = 2 g_F (large-A cubic
  cancels).
- G4 a thermal bath: a 4-d boson at temperature T, m^2 = g^2 A^2, the full J_B function (and the fermion J_F).
- G5 the 4-d vacuum (Coleman-Weinberg) determinant, m^2 = g^2 A^2, boson and fermion.
Each candidate's total static Lagrangian is L(A) = -A^2/(2K) (GR on shell psi = Phi) + (1/4K) alpha_t A^2 (tree) + L_ind(A),
and mu(A) = -(K/A) dL/dA (GR alone gives mu = 1; QX17's J gives mu = x/(1+x), x = |A|/a0: known answer KA3).

## 1. Gate T3, as tightened here

**(i) UV action.** PASS needs ONE candidate that passes all four tests below, on both footings, with J not present as a
UV term (J1 or J2 fails) so that it must come from the flow.
- (i-s) sign: the induced |A|^3 term must give an attractive deep regime (its coefficient in L negative, as J's cubic
  -|A|^3/(3 K a0) is). Read from the computed L_ind, not from V.
- (i-m) shape: with the candidate's free parameters fitted (scipy, bounded), max |mu - x/(1+x)| <= 0.1 on 41 log-spaced
  x in [0.01, 100] (T3's number), AND the deep slope d ln mu/d ln x at x = 0.01 within 0.1 of the law's (0.990).
  The slope condition is the tightening: a 0.1 absolute band alone does not test mu proportional to x below x = 0.1.
- (i-c) coefficient: the coupling combination the fit needs, against the natural ceiling nu <= M_Pl
  (1.2209e19 GeV, unreduced), |g| <= 4 pi, N_species <= 1000, temperature T <= M_Pl. Ratio
  R_c = needed / ceiling; pass needs R_c <= 1. Reported as log10 R_c per footing.
- (i-p) power counting: the UV action the candidate adds has every coupling of non-negative dimension at z = 3.
**FAIL** if every candidate fails at least one of (i-s), (i-m), (i-c), (i-p) on either footing, and J1 or J2 shows J
cannot be a UV term. Scope: FAIL covers the candidates stated here; a non-perturbative origin of J (condensate, strong
coupling) is not computed and is listed as untested. **OPEN** if any known answer fails or a numerical step fails.

**(ii) Percolation.** One-loop Lorentz violation in matter from graviton/khronon loops, Pospelov-Shang scaling
(arXiv:1010.5249, PROVISIONAL): the transfer is protected by (M_*/M_P)^2 above the Horava scale M_*. Frozen estimate,
species X:

    delta c_X = C * alpha_LV * (M_* / Mbar_P)^2 / (16 pi^2),      Mbar_P = 2.435e18 GeV (reduced; conservative)

with C scanned over [1e-3, 1e3] (an O(1) loop factor; the scan is wide on purpose) and alpha_LV the khronon's LV strength
on the background: graded with alpha_LV = 2, (A)'s value at A = 0 (the maximum over all backgrounds); reported with
alpha_perp(u) at Earth's surface (u = 9.80665/a0) and at the Sun's Galactic orbit (u = (233 km/s)^2/(8.2 kpc)/a0), and
with the enhanced form alpha_perp/(2 - alpha_par) there. Bounds (Kostelecky-Russell data tables arXiv:0801.0287v19,
Tables S2/S3, maximal two-sided sensitivities, PROVISIONAL, orders of magnitude):
- photon isotropic kappa-tilde_tr <= 1e-20;
- electron c-tilde_TT <= 1e-21; proton c-tilde_TT <= 1e-22;
- neutron, via the boost: an isotropic CMB-frame c seen at beta = 369.82 km/s/c gives c_JK ~ beta^2 c (direction factor
  set to 1, which tightens), and neutron c-tilde_Z <= 1e-29, so c <= 1e-29/beta^2;
- the strictest of these sets M_hi(C) = Mbar_P sqrt(16 pi^2 bound / (C alpha_LV)).
**PASS** if M_hi(C = 1e3) > M_lo (below) on both footings; **FAIL** if M_hi(C = 1e-3) < M_lo; **OPEN** otherwise.
Matter keeps z = 1 (Pospelov-Shang); its dimension-6 LV is then Planck-suppressed and is reported, not graded.

**(iii) The window with gravity's own limits.** M_lo = max of: short-range gravity hbar c/(38.6 um) (Lee et al. 2020,
arXiv:2002.11761, PROVISIONAL; the z = 2 terms act at r ~ 1/M_*); the z = 3 tensor dispersion at f = 100 Hz,
(2 pi hbar f/M_*)^2 <= 1e-15. M_hi additionally capped by: |c_T - 1| <= 1e-15 (GW170817, arXiv:1710.05834) with tree
c_T from beta and the one-loop delta c_T taken from the same estimate as (ii); the UV corrections to the solar-system and
pulsar limits the record passes, (hbar c/(M_* r))^2 at r = 1 AU and r = 10 km, and the one-loop generated beta,
lambda - 1, alpha (same estimate) against |alpha_2^PPN| <= 1.6e-9 (pulsars, PROVISIONAL) and the record's
lambda-channel c2 <= 6e-4 (L350). **PASS** if [M_lo, M_hi] is non-empty for C = 1e3 on both footings; **FAIL** if empty at
C = 1e-3; **OPEN** otherwise.

**T3 label.** PASS only if (i), (ii) and (iii) all PASS. FAIL if any of them FAILS. Otherwise OPEN.

Not part of the label (T2's ground, QG1): the khronon's strong-coupling scale. Reported only: at A = 0 (FRW, voids) the
quadratic gradient term of the lapse vanishes in (A) (alpha = 2 exactly), so perturbation theory there is not controlled;
the window's top must also sit below QG1's Lambda_s.

## 2. Reported, not graded

- **R1:** does the UV fix kappa or the 5.41? For the candidate that gets furthest, write a0 and rho_DE in terms of its UV
  couplings and say whether any relation ties them; the 5.41 is an integration constant of (E3) (R541).
- **R2:** do the z = 3 terms resolve COL1's fold (`fable52_push/COL1_clock_collapse/`) into a standing clock? Compute the
  length where a z = 3 dispersion omega = k^3/M_*^2 balances the infall (v = 100 and 300 km/s) across the window, against
  COL1's fold scale (1e-5 kpc, grid-limited), and state whether the added terms remove energy.

## 3. Known answers (must pass before any graded line is read)

- **KA1 power counting:** the formula [coupling] = (z + d) - [operator] gives [1/kappa^2] = z - d: 0 at z = d = 3
  (Horava's marginal gravitational coupling, arXiv:0901.3775) and 2 at z = 1 (M_P^2); every potential term of the
  projectable z = 3 list has a coupling of dimension >= 0.
- **KA2 BPS IR limit:** from the static weak-field ADM Lagrangian N sqrt(gamma) R^(3) + alpha a^2 (sympy), G_N =
  G/(1 - alpha/2) (Blas-Pujolas-Sibiryakov arXiv:1007.3503, PROVISIONAL); the FRW minisuperspace of R gives lambda = 1
  exactly.
- **KA3 the law:** QX17's + (a0^2/K) J(u) with GR gives mu = x/(1+x) exactly (sympy), so the mu definition is right.
- **KA4 textbook one-loop:** (a) 3-d: (1/2) Int d^3k/(2 pi)^3 ln(k^2 + m^2) with a hard cutoff has non-analytic part
  -m^3/(12 pi) (fit to 1e-6 relative); (b) thermal: the y^(3/2) coefficient of J_B(y) is -pi/6 (Dolan-Jackiw) to 1e-3;
  (c) the 8x8 Clifford fermion: det D = (k^2 + g^2 A^2)^4 at 5 random points to 1e-10.

## 4. MUTATE twins (must bite)

- **M1:** give G2's fermion boson statistics. (i-s) must FAIL for it.
- **M2:** feed the J1/J2 detector an even polynomial of degree 6 in u. It must report "admissible" (else the detector
  is broken).
- **M3:** replace a0 by M_Pl in the coefficient test of G3. (i-c) must PASS, showing the fail is the hierarchy.
- **M4:** drop G3's boson (fermion only). (i-m) must FAIL (no saturation).
- **M5:** set every (ii) bound to 1e-60. The window must be empty and (iii) FAIL.

## 5. Hand expectation (the lead's, unverified, written before any number)

(i) FAILS: J is non-analytic; the leaf determinant has the right sign but misses the coefficient by the a0 hierarchy
(about 30 orders, W3). (ii) a window exists only for M_* far below M_Pl, about 1e9-1e10 GeV. (iii) unclear. Fold: the
z = 3 terms set the caustic's microphysics, not whether a standing clock comes out.

My own pre-run note on the sign: the brief compares V_3 = -|m|^3/(12 pi) with J's cubic -u^3/3. J enters L with a plus
sign and V enters L with a minus sign, so for a boson the two may be opposite. (i-s) settles it from L.

kappa = 1/2 FITTED; not theory closed.

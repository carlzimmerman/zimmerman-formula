# CFG467 FROZEN CRITERIA: the alpha_c axis of the relativistic chassis (C-H/K) and the sign tension

Frozen 2026-10-08, before any CFG467 script exists. Nothing below may be edited after the commit that adds this file;
corrections go in a dated section appended at the end.

Theory only, offline, no downloads. Read-only on every lane named here. kappa = 1/2 is FITTED and plays no role. a0
enters none of the gates below (XC1 A4, CFG291, CFG320 say so), so the two footings (9.36e-11 / 1.13e-10) give
identical intervals; this is printed, not assumed silently. No dark-matter particle is added; the cold fluid's mass is
still required. Nothing here says "theory closed".

## 0. What is being asked, and disclosure

The failure ledger (LEDGER_failure_mechanisms_2026-10-08, rows 4-9) records a clash on the chassis (the ungated filtered
C-H/K khronon of L340: I_CH + c^3/(16 pi G) Int sqrt(-g) [alpha_c a.a - c_2 K^2], beta = 0): well-posedness wants
alpha_c > 0, while fully regular moving black holes exist only at alpha_c = 0. CFG467 maps every committed gate that
depends on alpha_c onto the real alpha_c axis (beta = 0, c_2 in L340's window), with its source lane and kind of
evidence, and decides whether the allowed sets intersect.

**Not blind.** Every source lane was read before this file was written. The expected outcome is anticipated: under the
strict black-hole criterion the allowed set is {0}, while hyperbolicity allows only (0, 2), so the central
intersection is expected to be empty; under the weak black-hole reading the record window is expected to survive. The
rule below is therefore fixed in a form that cannot be tuned after the run: every gate's strict and lenient sets are
written down here, from the record, before computing anything.

## 1. Scope

- Chassis only: beta = 0 (forced by c_T = 1), lambda_K = 1 + c_2, c_2 on the 9-point log grid CFG320 scored
  (`numbers.inputs.c2_scored` of CFG320's results JSON; L340 P1 window [7.289e-3, 0.0667], the leaf-average branch of
  L350 G5). The alpha_c axis is the whole real line; nothing is scanned as a knob, the axis is mapped.
- **Candidate B** has no action. None of these gates is computed for B. The README must say what the result implies
  for B, and say "untested for B".
- The c_2 axis's own problem (L350: the plain-K^2 branch's Planck-era ceilings lie below L340's c2_min) is out of
  scope; it is mentioned, not re-run.

## 2. The gates (allowed sets frozen here; A = shown allowed, X = shown excluded, U = untested, the rest of the line)

Kinds: PROOF = exact symbolic / certified algebra within the source's stated scope; NUM = computed on points or grids;
LIT = an external bound read through a summariser (PROVISIONAL); ARG = an argument or count, not a computation.
c_S^2 = c_2 (2 - alpha)/(alpha (2 + 3 c_2)) (CFG292 T1 at beta = 0).

| ID | gate | source | strict A | lenient A (the stated uncertainty / alternative reading) | X (both, unless noted) | kind |
|---|---|---|---|---|---|---|
| G1 | strong hyperbolicity + criterion B, F2a | CFG292 (T1, COND, C2, C4), CFG294 S1, XC2 B6 | 0 < c_S^2 < inf and alpha != 1/2, i.e. (0, 1/2) U (1/2, 2) | (0, 2): alpha = 1/2 is an F2a gauge artefact (physical lapse coefficient alpha/2 != 0) | (-inf, 0] U [2, inf); {1/2} strict only | PROOF (linear, frozen-coefficient principal symbol) |
| G2 | lapse/U leaf system: ellipticity and UV positivity | CFG294 S4b (joint det = 4 N alpha k^4), CFG329 (lapse coefficient (2C + alpha(1+C))/(1+C)), with C -> 0 at k >> 1/xi (XC1 A3) | alpha > 0 | same | (-inf, 0] | PROOF |
| G3 | F2a lapse kernel with W <= 0, W != 0 | CFG294 S4c, CFG312 (Hardy factor 1/2 - alpha) | alpha < 1/2, alpha != 0 | same | {0} U [1/2, inf) | PROOF (homogeneous class; Hardy sufficient) |
| G4 | strong coupling G8 | XC1 A4 (GSS2018 eq. 15; k = sqrt(alpha) M c_s^(-1/2) for c_s > 1, c_s^(3/2) for c_s < 1; M = 2.435e18 GeV; alpha <= 0 gives k = 0) | k_sc >= 1e3 x 1.3e4 GeV (XC1's gate) | k_sc >= 1.3e4 GeV (the LHC itself) | the complement on the line | NUM from LIT formula, tree level, decoupling limit |
| G5 | negative-phantom-lobe health | L340 H4 | [9.624e-14, inf) (L340 P1's alpha_min, an estimate |lambda0| xi^2/20) | [alpha_bis, inf), alpha_bis = the threshold bisected on L340's own symbol and k grid over the three negative lobes | (-inf, alpha_bis) | PROOF that alpha <= 0 fails (large-k limit of the symbol); NUM edge |
| G6 | PPN alpha2 | L340 P1, CFG291 (exact alpha2 = -alpha(2 alpha lam + alpha - lam)/(lam(alpha - 2)), lam = c_2) | \|alpha2\| <= 1.6e-9 | \|alpha2\| <= 2.4e-7 (CFG291's secondary) | complement | LIT |
| G7 | PPN alpha1 = -4 alpha | CFG291, L340 P1 | \|alpha1\| <= 1.1e-5 (L340, the tightest on record) | -3.5e-5 < alpha1 < 3.3e-5 (Shao & Wex 2012, as CFG291 lists) | complement | LIT |
| G8 | binary-pulsar dipole | CFG291, CFG311 | [9.624e-14, 3.2e-9] (tested, 625/625 under B0-B2; CFG311 discharges the sensitivity condition) | (0, 3.2e-9] (CFG291 C6: the flux vanishes monotonically as alpha -> 0+) | none shown: alpha <= 0 and alpha > 3.2e-9 are U (formula undefined / not scored) | NUM with LIT formulas |
| G9 | cosmological G / BBN | L350 G1, G5 | leaf-average branch: \|G_cos/G_N - 1\| = \|alpha\|/2 < 0.1 | same (the plain branch (2 - alpha)/(2 + 3 c_2) is printed as a reading) | complement | PROOF formula + LIT bound |
| G10 | G_N > 0 (static block G_N = G/(1 - alpha/2)) | L350 G1, CFG320 K4 | alpha < 2 | same | [2, inf) | PROOF |
| G11 | radiative stability G12 | CFG320 | no hierarchy: [9.624e-14, alpha_rs(c_2)] with Lambda_sc(alpha_rs, c_2) = Lambda_HL_max (CFG320 JSON summary, 9.87e8 GeV), clipped to 3.2e-9 | Pospelov-Shang hierarchy granted (M_* <= 9.9e8 GeV): [9.624e-14, 3.2e-9] (81/81 for naturalness and the EFT piece) | strict only: (alpha_rs, 3.2e-9]; the rest U | NUM + LIT |
| G12 | black-hole regularity G11 | CFG318, CFG319 (+ RB2019, FHB2021; Kovachik-Sibiryakov 2023/25 as recorded in the XC README, provisional) | reading S, regular everywhere outside r = 0 including the universal horizon: {0} (CFG319 C1 stealth solution) | reading W, CFG319's option C accepted (regular outside the UH; integrable x^-0.382 gradient singularity on the UH, hidden from all signals): {0} U [9.624e-14, 1e-3] (5 window points + the ladder 1e-7..1e-3) | strict: (0, inf) (count over-determined by one for every alpha > 0, test-khronon limit; NUM at 5 window points + ladder); lenient: none; alpha < 0 is U in both | NUM + ARG (count) + LIT |

**alpha_c-independent (listed, not scored):** Cassini Q2 (CFG357: the khronon sector is not in Q2); CFG312's W itself
(no alpha in W); GW170817 (beta only); L340 tracking (c_2 only); CFG318's exterior observables (shadow, QNM, ISCO pass at
every window alpha and do not flag even alpha = 0.1); PPN gamma, beta (alpha-independent in khronometric theory as a
literature reading; not computed for C-H/K on the record, L340's scope note).

**Reading rows (printed, never scored):** (r1) CFG294's physical velocity-fixed lapse form alpha |k|^2 + W, which for
W < 0 is resonance-free only for alpha <= 0 (CFG294 records the resonance and says F2a, the operator the scheme inverts,
has none); (r2) for alpha < 0, c_2 > 0, CFG319's S22 has no zero outside the UH, so the spin-0-horizon condition
disappears from the count (no existence computed); (r3) the plain-branch BBN interval.

## 3. Decision rule

For each c_2 on the grid, intersect the allowed sets (sympy sets; endpoints exact where the formula is algebraic,
mpmath roots at 50 digits otherwise):
- I_strict(c_2) = intersection of every gate's strict A;
- I_len(c_2) = intersection of every gate's lenient A;
- NX(c_2) = intersection of the complements of every gate's strict X (the "not shown excluded" set).

Verdict (union over the c_2 grid):
- **CONSISTENT** if the union of I_strict is non-empty. Report it, with the binding gate at each edge.
- **TENSION** if the union of I_strict is empty but the union of I_len is non-empty (empty, but within the stated
  uncertainties and alternative readings of the source lanes).
- **INCONSISTENT** if the union of I_len is also empty (empty robustly).

Also reported (not verdicts):
- the S-only robustness: the intersection with G12 held at reading S and every other gate lenient;
- every minimal set of relaxations (strict -> lenient) that opens the intersection, enumerated over all 2^12 subsets;
- the gates that exclude each of the probe points alpha = -1e-9, 0, 1e-15, 1e-13, 1e-11, 3e-9, 1e-6, 0.1, 0.5, 1 (strict);
- the minimal change that would open the intersection, and whether it adds a constant. The candidates are taken from the
  record, not invented: (a) the BH criterion W (owner call, no constant); (b) a UV sector that regularises the universal
  horizon at alpha > 0 (Horava higher-spatial-derivative terms, scale M_*: +1 constant, possibly the same M_* that G11's
  hierarchy names; untested); (c) moving the chassis to alpha <= 0, which needs G1, G2, G4, G5 all changed.

## 4. Controls (load-bearing unless marked; a failed control is reported and kept, never silently fixed)

- **K1** G1's set is derived from CFG292's committed F2a scalar characteristic polynomial (results JSON numbers.T1,
  parsed with sympy, beta = 0): real non-zero roots iff 0 < alpha < 2 at every c_2 > 0 on the grid; and F2a's committed
  lapse coefficient (2 alpha - 1)/4 vanishes only at alpha = 1/2.
- **K2** the G4 formula reproduces XC1's committed minimum k_sc (numbers.A4.min_k_sc_GeV, 8.48e8 GeV) to 1e-6 relative at
  its worst point.
- **K3** the G5 symbol, re-implemented from L340's source, reproduces L340's committed H4 booleans (alpha = 0 and 1e-9, all
  four lobes); and inertia at the grid's top k is negative for alpha = 0 and alpha = -1e-20 in every negative lobe.
- **K4** the G6/G7 formulas reproduce CFG291's committed PPN corners (numbers.PPN.corners) to 1e-6 relative.
- **K5** the G11 Lambda_sc reproduces CFG320's committed Lambda_sc_min and Lambda_sc_max to 1e-6 relative, and its
  sub-window contains exactly CFG320's committed UV_subwindow points (3, at alpha_min, c_2 >= 0.0383).
- **K6** G12's sets are read from CFG319's committed JSON: verdict_inputs.full_regular all False at the five window
  points, optC_admissible all True, C1 passed; the ladder alphas are read from numbers.runs.
- **K7** the set engine on toy sets: (0,1) n {0} = empty; (0,1) n [1/2, 2] = [1/2, 1); ((0,1/2) U (1/2,2)) n [1/2,1] = (1/2, 1].
- **K8 mirror** flipping the sign convention of EVERY gate (alpha -> -alpha) must mirror I_strict, I_len and NX exactly and
  leave the verdict unchanged.
- **K9 footings** a0 is not an input of any gate function (checked by running the gate builder under both footing labels
  and comparing the sets: identical).

## 5. MUTATE (`CFG467_MUTATE=1`)

Flip the sign convention of ONE gate, G1 (alpha -> -alpha, as CFG292's own C4 did): its sets become the mirror images.
Required response: K1 fails (the flipped G1 contradicts CFG292's committed polynomial), so rc = 1; and the run must
show that the intersection logic responds: I_len, computed in the same process with and without the flip, must differ,
and the MUTATE verdict is printed. Outputs go to `*_MUTATE.out` / `*_results_MUTATE.json`, never over the main files.

## 6. Files

`cfg467_alpha_c_axis.py`; `cfg467_alpha_c_axis.out`, `cfg467_results.json`; `cfg467_alpha_c_axis_MUTATE.out`,
`cfg467_results_MUTATE.json`; `README.md` with the interval table. Commit locally; do not push.

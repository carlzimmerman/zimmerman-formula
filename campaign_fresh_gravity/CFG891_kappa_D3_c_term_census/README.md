# CFG891: κ door D3, a census of every place c meets a₀ in the record. π-FREE BUT NOT ½

**Bottom line.** No equation in the record gives exactly κ = ½ unless ½ (or its premise) is written in.

The census found 67 relations in which c meets a₀: 62 frozen plus 5 post-freeze additions. A further 15 rows were checked and
turned out to be a₀-free or c-free. Of the 67:
- **Five π-free rational equalities give exactly ½, and all five carry the target.** They are the canonical
  "ρ_DE c² = 4a₀²/G" (L02), MASTER's "desired identity" (M04), the AeST/HT tie (R01) and the CFG43 fluid cap (R03), which write
  ½ in, and the free-fall radius R* = c/√(Gρ) (R19), whose J = 1 is a forbidden premise.
- **Exactly one π-free determinate value exists without the target.** It is CFG380's S⁴ four-volume reading (R18): the √π of
  Vol^{1/4} cancels Einstein's √(8π) and leaves κ² = 2√6/3, κ = 1.278. That value is irrational, a posit, and a miss.
- **Every H-type value has odd π-weight (7 of 7),** as π-parity requires.
- **Every other route** is an identity, an inequality, a trade (½ only by tuning a free constant), mass-dependent, π-bearing,
  ill-defined or pending.

Frozen outcome: **π-FREE BUT NOT ½** (N_half = N_live = 0, N_pfdet = 1).

What this means for the κ campaign:
- **The record cannot produce exact ½.** A new door would need a π-free coupling, through c, of a dynamical ρ_DE that does not
  pass through Einstein's 8πG. Alternatively it would need a principle that makes c√(Gρ_DE) itself the natural unit, which is
  premise A and is forbidden unless derived.
- **The structural observation in KAPPA_DOORS.md needs one amendment.** π can cancel between sectors (R18), but in the record it
  never cancels to a rational κ².
- **The mutation shows Einstein's 8π is load-bearing.** Remove the portal's π and 8 rows become π-free, none of them at ½.

Standing facts:
- **κ = ½ is FITTED.** CFG493: κ_Λ = 0.417 ± 0.095, κ_crit = 0.345 ± 0.078.
- The footings are never pooled. The classes are identical on ρ_DE and ρ_crit (K6), and no footing number is used.
- No de Sitter–Unruh argument is cited for ½. A04 lists the 2cH_Λ temperature root as an excluded H-type term, off by exactly Z.
- GF2's ½ is the SIS ratio (a755b66ca) and is not counted.
- This lane derives nothing. A census outputs no κ, so P_LEE is unchanged. Not theory closed.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (19571473c): scope, classification scheme, the 70-row term table (77 encoded rows with sub-rows) with hand classes, checks, outcomes, MUTATE |
| `cfg891.py` | sympy + stdlib, one process, about 2 s, under 150 MB |
| `cfg891.out`, `cfg891_results.json` | normal run, 11/11 K checks PASS, exit 0 |
| `cfg891_scan.out` | K9: per-file counts and all 118 lines in the 36 Tier 1 files where an a₀ token and a c-carrier share a line |
| `cfg891_MUTATE.out`, `cfg891_results_MUTATE.json` | `CFG891_MUTATE=1`: M1, M2 and M3 bite, exit 1 by design |

Run from the repo root:

    OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG891_kappa_D3_c_term_census/cfg891.py
    CFG891_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 campaign_fresh_gravity/CFG891_kappa_D3_c_term_census/cfg891.py

The script reads only the 36 Tier 1 text files and the CFG894 register CSV, all read only. Nothing was downloaded, and no
other lane, LEDGER.md, canonical file or register was edited.

## How the census works

**Scope** (frozen §1):
- **Tier 1, the record's own equations,** read from 36 files: the canonical theory files, FRAMEWORK_EQUATIONS, MASTER, the
  cold-energy equations (CFG541/542/638/639/893), the action S2 (CFG694/695/770/807/760/762), black holes and horizons
  (CFG775/778), relativistic ties (CFG187, CFG43, kappa_closure, XR20, p63, the sol61 clock lanes) and lensing/relativistic
  lanes (CFG349/381/380/663/847).
- **Tier 2: 103 register rows.** These are the 67 sol61 puzzle_32pi rows and 36 door starting points.
- **Tier 3:** all 64 half = 1 rows in the register, as a cross-check.

**Classification.** Each relation was written in sympy with π as a tracked symbol. The script then substituted the law
a₀ = κc√(Gρ) and the footing's own Friedmann relation (H² = 8πGρ/3, Λ = 8πGρ/c², R_H = c/H). Each row was classed as:
- DEF or ID if it holds for every κ;
- INEQ if it is an inequality;
- otherwise κ² was solved for and read off as HBAR, TRADE, MASS, or a determinate r·π^k. A determinate value is H-ODD or H-EVEN
  for an H carrier, RHO-PI for a ρ or Λ carrier with k ≠ 0, and PF-RAT or PF-ALG for k = 0.

Each row also carries its provenance (held, posit, target, rejected, pending).

**What would have counted.** N_half (= N_live) counts π-free, ħ-free, determinate, non-identity equalities with κ² = 1/4
exactly whose provenance is not target or pending.

## Results

| class | n | rows |
|---|---|---|
| DEF (the law and its rewritings) | 6 | L01, L03–L07 |
| ID (holds for every κ) | 15 | L08, B01–B05, B07, R16; declared C02, C06, C10, S07, R05, R15, X01 |
| INEQ | 3 | C04 (drift causality); declared C03 (sink bounds), X03 (lensing slip) |
| TRADE (κ swapped for a free constant) | 10 | L09, L10, R02 (normalisations k_H, k_E, κ_K); C05 (α, f); S03 (zero mode w₀); S05, S06 (y_t, L*); R04 (Z/β²); R10 (D, λ); R11 (C_bare) |
| MASS | 2 | A01, A02 (CFG893 R3/R4) |
| ILL / REJ / PEND (declared) | 5 / 2 / 4 | S04, S10, R14, A03, A05 / C07, R13 / S08, R08, R09, M02 |
| H-ODD | 7 | R20a 2.894, R20b 1.447, R20c 0.461 (π⁻¹), R21 2.894, A04 5.789 (rejected); pending R06 1.447, R07 2.894 |
| RHO-PI | 7 | S09a 0.984 (π⁻³), S09b 3.545 (π), R17a/b/c 1.671/1.447/2.894 (π), R20d 4.19 and R20e 8.38 (π²) |
| PF-RAT | 5 | L02, R01, R03, R19, M04: all κ = ½, **all provenance target** (N_wi_half = 5) |
| PF-ALG | 1 | **R18: κ² = 2√6/3, κ = 1.278 (posit, miss)** = N_pfdet |
| NA (checked; no c–a₀ meeting) | 15 | P01, C01, C08, C09, C11, C12, S01, S02, B06, R12, X02, X04, X05, M01, M03 |

**Reading, row group by row group.**

1. **The portal.** P01 (MASTER Supp. C): ρ_DE reaches c-geometry only through G_μν = (8πG/c⁴)T^DE, so as 8πGρ/c². Every
   relation built through H, Λ or a horizon inherits that π.
2. **H-type rows always have odd weight.** a₀ = r·π^m·cH gives κ² = (8/3)r²π^{2m+1}, odd for every integer m (K8, symbolic).
   The seven H-type values are 2.894, 1.447, 0.461, 5.789 and the pending p63 forms. CFG775's whole black-hole and horizon table
   (B01–B05) consists of identities in q = a₀/(cH∞). Their "ratio = 1" posits, report only, give 1.447, 0.362, 1.447, 1.447 and
   2.894, all π-odd.
3. **ρ- and Λ-type rows carry π.** Examples: k01 K5's vacuum reading (κ² = 30/π³ or 4π), CFG380's algebraic Λ-geometry
   coefficients (κ² = 8πC²) and the Newtonian ball (π²).
4. **π-free rows.** The ½ appears π-free only where the unit c√(Gρ) is postulated: R* = c/√(Gρ) (J = 1, premise A), or ½
   written in (L02, M04, R01, R03). The rename test K4 confirms these five restate the law. With the law's κ set to 2/5 each
   one fails. The only π-cancellation without the target, R18, needs a second geometric π (the four-volume of S⁴_Λ), and it
   returns an irrational κ².
5. **Trades.** In these rows ½ is reachable only by tuning:
   - the four-form, at Z/β² = 7.964;
   - CFG807's hand-set turn-off, at y_t = 33.98 (C = 16π);
   - the zero mode, at w₀ = 4;
   - the clock coefficient, whose BBN bound already forces κ < 0.145;
   - H12, which needs α and the locus.
   Each is a TRADE under rule §2. CFG897 (D1) and CFG898 (D2) have since closed the stiffness-vacuum and causality-saturation
   versions on their own terms.
6. **The c-free sector** (S01, S02, C12, M01) is NA, as CFG893's S_λ symmetry requires. So are CFG893's c-free R5 balances,
   which are not listed because they are c-free.

**Values against W_data** (report only, no evidential weight):
- Inside [0.227, 0.607] on ρ_DE: R20c's 0.4607 (the recurring Gibbons–Hawking-as-Unruh reading, an H-type posit, still subject
  to the open RT-17 / RT-19 conflict P4) and the five target rows.
- Every other determinate value lies outside.

**Tier 2 (103 rows).**
- Histogram of the descriptive mapping: CLOSURE 30, TRADE/FREE 29, VOID 9, INEQ 7, OTHER 7, ID/CONDITION 4, PEND 4, MENU 3,
  RHO 2, CONDITIONAL 1, not trials 7.
- The two determinate density routes are K216 (κ 4.1; κ² = 16π/3, π-odd) and K297 (κ 12). Both miss.
- Eleven in-scope half = 1 rows exist (K079, K128, K278, K295, K345, K375, K486, K492, K543, K574, K580). All are void,
  conditional or menu.
- No live candidate.

**Tier 3.** 64 of 64 half = 1 rows in the register carry a void-type verdict. This re-verifies CFG894's "P(flawed | ½) = 1"
from the verdict text.

## What this does to the door list

D3's predicted sentence holds, with one qualifier. Record it as:

> No record equation produces exact κ = ½. In the record, ρ_DE meets a₀ through c only via Einstein's 8πG (π-odd for every H or
> horizon route), via written-in ties, or via the postulated unit c√(Gρ) (premise A / J = 1). The one π-cancellation found
> (CFG380's S⁴ four-volume) gives an irrational κ² = 2√6/3. An exact ½ needs a new π-free c-coupling of a dynamical ρ_DE outside
> Einstein's 8πG, or a derivation of premise A.

- N_live = 0, so no new door is spawned.
- The formal version (a Lean statement) belongs to the 32π chat.
- The remaining doors that could still produce a π-free coupling are D4 (v = c nodal medium, M02 here) and D5 (Festina Lente).
  Both are pending and outside the record's present equations.

## Checks (all PASS in the normal run)

- **K1:** no forbidden constant in the script.
- **K2:** all 32 solved κ² are printed symbolically.
- **K3:** scaling G → λG, ρ → μρ, c → νc (with a₀, H, L*, M and ρ_c scaled consistently) leaves every κ² unchanged. This also
  checks the dimensions of every encoding.
- **K4:** the rename test. All DEF and ID rows still hold at κ_law = 2/5, and all five WI rows fail there.
- **K5:** Z² = 32π/3 at κ = ½ holds for every ρ, and L04 is classed DEF.
- **K6:** identical classes and counts on ρ_crit.
- **K7:** in R21, ħ cancels, giving H-ODD. No HBAR row remains and no un-ratioed ¼ appears.
- **K8:** the generic π-parity holds, and all 7 H-type weights are odd.
- **K9:** all 36 Tier 1 files are cited. 23 of them have hit lines, 118 lines in all.
- **K10:** no live Tier 2 candidate, and Tier 3 is 64/64 voided.
- **K11:** the six planted classifier controls each receive their own class.

## MUTATE (exit 1: every control bites)

- **M1, Einstein's portal π removed** (8π → 8 in H², Λ and k01's 1/16πG). N_pfdet rises from 1 to 8: S09b gives κ = 2; R17a/b/c
  give 8C²; R20a gives 8/3; R20b gives 2/3; R21 and A04 also become π-free. R18 becomes π-bearing (2√6/(3π)). None of the eight
  is ½. The π-parity wall therefore rests on the 8π.
- **M2, a planted live row** (ρ_DE c² = 4a₀²/G with provenance held). N_half goes from 0 to 1, and the outcome flips to EXACT-½
  AVAILABLE.
- **M3, d = 5 under the 8πG_d convention** (H² = (4π/3)Gρ). Every H-type κ² moves, π-weights are unchanged, and N_half and
  N_pfdet are unchanged.
  - The frozen wording "every H-type κ² halves" **FAILS AS FROZEN for R06** (pending p63 C1). There κ² ∝ 1/H², so it doubles.
    This was worked out from the algebra before the first MUTATE run, and the script prints it.
  - S3 note: under the Gauss-law convention the coupling's π-weight is ⌊(d−1)/2⌋, which is odd only at d = 4 among d = 4–6. So
    the parity wall is a d = 4 statement in that convention.

## Disclosures

1. **First run (verdict already printed).** sympy auto-cancelled CFG775's ratio identities (B01–B05) to 0 when they were
   built, so they were classed NA. They are now kept unevaluated (`EQ`). This changed N_c from 57 to 62 and touched neither
   N_pfdet nor N_half.
2. **Post-freeze additions A01–A05,** found by reading the K9 scan lines after run 1 and labelled as such:
   - A01, A02: CFG893 R3/R4, MASS;
   - A03: k01 K3–K4's wrong-sign Λ-free vacuum, ILL;
   - A04: k03's a₀ = 2cH_Λ, H-ODD, rejected;
   - A05: CFG187 C2, ILL.
   None could change N_pfdet or N_half. N_c went from 62 to 67.
3. **One classifier reading.** The frozen order lists H-ODD/H-EVEN before PF. The script classes any k = 0 as PF whatever the
   carrier, as the frozen M1 expectation requires. This never arises in the normal run.
4. **Hand classes that the script overrode:**
   - L09, L10 and R02: these are shape laws with a free normalisation. The script calls them TRADE; the hand table said ID.
   - S03: the zero mode written as ρ_DE c² = w₀a₀²/G is a TRADE (w₀ free). The hand table said ID.
   - C03 and X03: declared INEQ, because they are numeric bounds with no a₀ symbol.
   - R06 and R07: classified from their frozen forms as H-ODD with provenance pending, so not counted.
   No count changes.
5. **Tier 2 mapping refined after the run** (histogram only; the K10 rule is unchanged): word-boundary matching, so that
   "boundary" is not read as BOUND, plus CIRCULAR → VOID and FIT → TRADE.
6. **Evaluation choices.** k01 K5 (S09) is evaluated at K_B = 0, the record's headline value; K_B > 0 makes it a TRADE. L10
   and the event-horizon natural value use the pure-dS R_E = c/H_Λ, because today's R_E needs Ω_m.
7. **Scan count.** The scan regex counts 23 files with hits, against 24 in the pre-freeze exploratory count.
8. **S08 (door D1)** was pending at the freeze and has since run as CFG897: CLOSURE, with κ swapped for L*. That agrees with
   S06's TRADE. It was not re-classified here.

## Proposed register row (not appended by this lane; for the orchestrator)

`K597?,CFG891,AU,campaign_fresh_gravity/CFG891_kappa_D3_c_term_census,"D3 census: every c-a0 relation in the record (67; pi-weight, hbar-weight, class)",,,audit,0,"CENSUS pi-FREE BUT NOT 1/2: N_half 0; 5 pi-free halves all target-written; one pi-free value CFG380 S4 volume kappa^2=2sqrt6/3 (1.278, posit miss); all H-type pi-odd",<this commit>`

Use the next free K id. K595 and K596 are taken by CFG897 and CFG898.

κ fitted; not theory closed.

## Appendix: the full table (rendered from `cfg891_results.json`)

\* = declared class (no symbolic κ form; reason given). "natural" = report-only κ of the posit "ratio = 1".

| id | relation (source) | prov | class | κ² (π-weight) | κ |
|---|---|---|---|---|---|
| L01 | the law (kappa FITTED) | held | DEF |  |  |
| L02 | 'equivalently rho_DE c^2 = 4 a0^2/G (C = 16 pi)': the fitted value restated (rules s2: G rho_L = 4 a0^2) | target | PF-RAT | 1/4 (0) | 0.5000 |
| L03 | Lambda c^4/a0^2 = 8 pi/kappa^2 (32 pi at kappa = 1/2 by choice) | held | DEF |  |  |
| L04 | Z = c H_L/a0 | held | DEF |  |  |
| L05 | q = a0/(c H_inf) | held | DEF |  |  |
| L06 | Lambda l0^2 = 8 pi/kappa^2 | held | DEF |  |  |
| L07 | alt footing a0 = kappa c sqrt(G rho_crit) = kappa sqrt(3/8pi) c H0; CFG833's 1/sqrt(Omega_L) by construction | held | DEF |  |  |
| L08 | a0(z)/a0(0) = sqrt(rho_DE(z)/rho_DE(0)) (flat, tracking, DESI, BH-sourced) | held | ID |  |  |
| L09 | rival a0 proportional to H(z); normalisation k_H fitted | held | TRADE | 8 pi k_H^2/3 [free: k_H] | natural 2.894 |
| L10 | event-horizon branch a0 proportional to c^2/R_E (pure-dS limit R_E = c/H_L; today R_E needs Omega_m) | held | TRADE | 8 pi k_E^2/3 [free: k_E] | natural 2.894 |
| P01 | Einstein equation with T^DE: rho_DE reaches c-geometry only as 8 pi G rho/c^2 | held | NA |  |  |
| C01 | exact-Lambda sink: w = -1 forces Q = 0 (a0-free) | held | NA |  |  |
| C02 | d ln a0/dt = Qbar/(2 eps_DE): an ODE whose integration constant is kappa (CFG893 R2) | held | ID* |  |  |
| C03 | sink bounds: d rho_DE/rho_DE <= 2.2e-6; local d a0/a0 <= 7e-9 if the energy leaves at c (numeric bounds) | held | INEQ* |  |  |
| C04 | drift causality /v_s/ <= c (CFG893 R12) | held | INEQ |  |  |
| C05 | H12: marginal causality at rho* = f rho_DE (added hypothesis) | posit | TRADE | 9.53746371792924 pi f/alpha^2 [free: alpha, f] |  |
| C06 | damped psi wave: c is a propagation speed; a0 enters only through the source d(rho_ph(a0)); no equality relates them | held | ID* |  |  |
| C07 | tau_psi = c/a0: a timescale identification, rejected (unstable; needs kappa > 379 at Delta_loc 1e5) | rejected | REJ* |  |  |
| C08 | tau_psi = 1/H0 (a0-free), rejected | rejected | NA |  |  |
| C09 | dark-energy scalar equation (a0-free) | held | NA |  |  |
| C10 | Cattaneo / damped-wave Hurwitz condition with K = ck/Gamma: c is a propagation speed | held | ID* |  |  |
| C11 | Israel-Stewart closure; characteristics u +- sqrt3 sigma << c (a0-free) | held | NA |  |  |
| C12 | deficit-gated mobility (c-free; CFG893 K7) | held | NA |  |  |
| S01 | S2 field law K W' = u^2/(a0 - u), K = 4 pi G (c-free) | held | NA |  |  |
| S02 | saturation u <= a0 gives Sigma_ph <= a0/(pi G) (c-free) | held | NA |  |  |
| S03 | vacuum zero mode: W_rem -> W_rem + W0 leaves the EL equations unchanged, so rho_DE c^2 = W0 = w0 a0^2/G has w0 free | held | TRADE | 1/w_0 [free: w_0] |  |
| S04 | PAPER42 premise in S2: eps_W = -infinity, eps_Q = +infinity (CFG807 V1) | posit | ILL* |  |  |
| S05 | vacuum with hand-set turn-off, C(y_t) ~ (pi/2) y_t - logs; C = 16 pi at y_t = 33.98 | posit | TRADE | 4 pi/C_yt [free: C_yt] |  |
| S06 | y_t = c^2/(a0 L*): off by x1.7e8 | posit | TRADE | c^2/(G L_star^2 rho_DE y_t^2) [free: L_star, y_t] |  |
| S07 | P-wave speed c_P = sqrt(gamma/I) is free; c_P = c is not in the record; no kappa equation | held | ID* |  |  |
| S08 | covariant completion of the stiffness term on FRW (door D1) | pending | PEND* |  |  |
| S09a | k01 K5: nu_RAR unsaturated-branch constant 4 pi^4/15 as vacuum energy, K_B = 0 (forbidden branch) | posit | RHO-PI | 30/pi^3 (-3) | 0.9836 |
| S09b | k01 K5: exp-carrier constant 2 as vacuum energy, K_B = 0 | posit | RHO-PI | 4 pi (1) | 3.5449 |
| S10 | k02 sequestering average: five orders short | posit | ILL* |  |  |
| B01 | r_M/sqrt(r_s R_H) = 1/sqrt(2q) | held | ID |  | natural 1.447 |
| B02 | tether capacity / horizon surface density = 8q | held | ID |  | natural 0.362 |
| B03 | projected = 2q | held | ID |  | natural 1.447 |
| B04 | BH of surface gravity a0 / horizon mass = 1/(2q) | held | ID |  | natural 1.447 |
| B05 | a0 / dS surface gravity = q | held | ID |  | natural 2.894 |
| B06 | Nariai mass / M_H (a0-free) | held | NA |  |  |
| B07 | CCBH chain a0^2 = kappa^2 c^2 G Xi int psi a^-3 dt: the law with rho_DE identified | held | ID |  |  |
| R01 | AeST/HT tie alpha(Lambda) = kappa sqrt(Lambda/8pi) with kappa = 1/2 written in | target | PF-RAT | 1/4 (0) | 0.5000 |
| R02 | tie to the aether/khronon expansion K = 3H (rival law), kappa_K free | held | TRADE | 24 pi kappa_K^2 [free: kappa_K] | natural 8.683 |
| R03 | fluid cap P_cap = (kappa^2/8pi) rho_L c^2 = a0^2/(8 pi G), kappa = 1/2 written in (also G031) | target | PF-RAT | 1/4 (0) | 0.5000 |
| R04 | four-form: kappa^2 = 2 beta^2/(Z + 2 b beta^2), b = I/(8 pi) (k04 F2; AS651-658) | held | TRADE | 2.0 pi/(pi Zq_over_beta2 + 0.113125) [free: Zq_over_beta2] |  |
| R05 | four-form feedback a0_loc/a0 = 1/(1 + (kappa^2/8pi) F(y)): defines a local a0 for every kappa | held | ID* |  |  |
| R06 | p63 C1: saturated bound charge (unrun) | pending | H-ODD | 2 pi/3 (1) | 1.4472 |
| R07 | p63 C1b: patch bootstrap (unrun) | pending | H-ODD | 8 pi/3 (1) | 2.8944 |
| R08 | p63 C2: flux lattice kappa = kappa1/N (MENU class) | pending | PEND* |  |  |
| R09 | p63 C3: Kaloper-Sorbo hbar audit | pending | PEND* |  |  |
| R10 | canonical clock coefficient; BBN bound C > 1197.9 gives kappa < 0.145 in that construction | held | TRADE | 6 pi (3 lambda_clock - 1)/(D (D + 1)^2) [free: D, lambda_clock] |  |
| R11 | vacuum offset V0: C_bare spans every positive value | held | TRADE | 8 pi/C_bare [free: C_bare] |  |
| R12 | density-length identity r_U^2 Lambda = 16 pi/S* (a0-free) | held | NA |  |  |
| R13 | switch rate Gamma = a0/c (sensitivity only, 0/24 ON): a rate choice, no kappa equation | rejected | REJ* |  |  |
| R14 | alpha = a0/c^2 promoted to a free field switches MOND off (FP5 / XR20 D3) | held | ILL* |  |  |
| R15 | T1e: a matter vacuum moves the observed Lambda but not a0 (tie to the HT constant only) | held | ID* |  |  |
| R16 | evolving-DE tie a0 ~ sqrt(V), V = (rho - p)/2, evaluated at w = -1 | held | ID |  |  |
| R17a | CFG380 Lambda-geometry identification a0 = C c^2 sqrt(Lambda), C = 1/3 (CHOSEN) | posit | RHO-PI | 8 pi/9 (1) | 1.6711 |
| R17b | CFG380 Lambda-geometry identification a0 = C c^2 sqrt(Lambda), C = sqrt(3)/6 (CHOSEN) | posit | RHO-PI | 2 pi/3 (1) | 1.4472 |
| R17c | CFG380 Lambda-geometry identification a0 = C c^2 sqrt(Lambda), C = sqrt(3)/3 (CHOSEN) | posit | RHO-PI | 8 pi/3 (1) | 2.8944 |
| R18 | CFG380 R4: a0 = c^2/Vol(S^4_Lambda)^(1/4) (CHOSEN; closest miss x2.56) | posit | PF-ALG | 2 sqrt(6)/3 (0) | 1.2779 |
| R19 | free-fall surface gravity at R* = c/sqrt(G rho): J = 1 posited (rules s2), no SdS horizon at R* (k05 H1) | target | PF-RAT | 1/4 (0) | 0.5000 |
| R20a | k05 R2: dS horizon surface gravity | posit | H-ODD | 8 pi/3 (1) | 2.8944 |
| R20b | k05 R2: Hubble sphere as its own Schwarzschild radius | posit | H-ODD | 2 pi/3 (1) | 1.4472 |
| R20c | k05 R2 / k03: Gibbons-Hawking as Unruh (the 0.461 form) | posit | H-ODD | 2/(3 pi) (-1) | 0.4607 |
| R20d | k05 R2: Newtonian ball of vacuum at R* | posit | RHO-PI | 16 pi^2/9 (2) | 4.1888 |
| R20e | k05 R2: Newtonian ball with active mass /rho + 3p/ = 2 rho | posit | RHO-PI | 64 pi^2/9 (2) | 8.3776 |
| R21 | T_Unruh(a0) = T_GH (hbar bookkeeping; algebraically R20a) | posit | H-ODD | 8 pi/3 (1) | 2.8944 |
| X01 | weak-field metric with Phi/c^2, Psi/c^2; lensing probes Phi + Psi: c is a unit conversion | held | ID* |  |  |
| X02 | additive non-lensing prescription (c-free) | held | NA |  |  |
| X03 | slip /Phi - Psi//v_c^2 <= 2e-5 from sigma^2/c^2 and the law's field energy W (kappa-free numeric bound) | held | INEQ* |  |  |
| X04 | the response sector must lens (no a0-c relation) | held | NA |  |  |
| X05 | khronon K response ratio (a0-free) | held | NA |  |  |
| M01 | K =? G a0 (c-free) | held | NA |  |  |
| M02 | nodal medium K = q_b^3 v/(2 N m* C^3 h^3) with v = c (door D4); TRADE + hbar expected | pending | PEND* |  |  |
| M03 | carrier charge bound (c = 1 units, a0-free) | held | NA |  |  |
| M04 | 'desired identity' a0 =? (c/2) sqrt(G rho_DE): the target | target | PF-RAT | 1/4 (0) | 0.5000 |
| A01 (post-freeze) | CFG893 R3 (H3): dark energy = accumulated settling energy, eps_DE = rho_DE c^2 = int Q dt (EXCLUDED there) | posit | MASS | c^6 rho_DE^3/(G^3 M^2 rho_c^4 xi^4) |  |
| A02 (post-freeze) | CFG893 R4 (H4): the sink drives a 1% dark-energy evolution (EXCLUDED there) | posit | MASS | c^6 rho_DE^3/(100000000 G^3 M^2 rho_c^4 xi^4) |  |
| A03 (post-freeze) | k01 K3-K4: Lambda-free vacuum with the primitive's zero fixed by an empty Newtonian vacuum: negative sign and 0.4-0.7% of rho_L, so no real kappa | posit | ILL* |  |  |
| A04 (post-freeze) | k03's note: Milgrom 1999's construction read as a0 = 2 c H_L (the temperature root), excluded | rejected | H-ODD | 32 pi/3 (1) | 5.7888 |
| A05 (post-freeze) | CFG187 C2: without the HT multiplier Lambda's equation is local, Lambda ~ Y, so a0 varies in space (closure; the multiplier is what makes the tie global) | held | ILL* |  |  |

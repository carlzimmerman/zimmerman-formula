# SRH1 FROZEN CRITERIA: one history of the settled radius against the forest, rotation curves and galaxy lensing

Committed alone, before any SRH1 script exists and before any SRH1 number is computed. TEST lane, quarantined. Relabels
nothing, adopts nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded
separately, never pooled. Cold dark energy is a gravitating field component; no particle is added anywhere.
kappa = 1/2 FITTED; not theory closed.

**Lane id.** The brief named this lane SR1. That id is taken twice (`rebuild_2026_10_22/SR1_r2_on_sluggs`,
`rebuild_2026_10_22/SR1_star_saturated_response`), so this lane is **SRH1**.

**This family is post hoc.** It was chosen after FRZ1 (forest FAILS, 9916 / 9009) and FZS1 (forest FAILS at R_set = R_fold,
38.7 / 36.7; passes at x 0.5, 0.19 / 0.19) were seen, and after the closure chat's scan from a copy (not a lane: 3.17 / 3.08
at 0.7 R_fold, 13.2 / 12.6 at 0.85). A pass here is not a pass of form B and not a derivation: the joint (the equation
that takes the cold component from falling dust to the settled halo) stays missing. A pass needs an independent re-grade,
and it is not in PAPER72.

## 0. The question, and what was seen before this freeze

Is there one history R_set(z, M_b), with the law's layout inside it and the cold reference's layout outside it, that
passes the forest, the rotation curves at high redshift and today, and galaxy lensing together? Or do the lower limits sit
above the upper limits?

Seen before this freeze: FZS1's criteria, RESULT, `fzs1_hm.py`, `fzs1_forest.py`, `fzs1_forest_canonical.out`, and the scan
copy's `driver.log` (numbers above); FRZ1's `layout`, `set_z`, `halo_basics_z`, `phantom` code; FLD1's RESULT,
`fld1_compare.py` and, from `fld1_compare.json`, the worst ratios at f = 1 (SPARC UGC00128 R_last / R_fold(0) 0.467 /
0.467; RC100 zC 405226 2.2 R_e / R_fold(z) 0.391 / 0.391 and 4 R_e 0.711 / 0.712; no SPARC galaxy outside FLD1's mass grid);
ONE1's RESULT, `one1_kids.py` (sections 1 to 8), its run log (gate PASS / PASS, model R_s 1.003 / 0.847, data 0.811 +- 0.134
/ 0.809 +- 0.133 at 1.6 R_h); PD1's RESULT and `pd1.py` (`sparc`, `kids`, share table); the KiDS lens redshifts in
`lr_lenses.npz` (median 0.31, 5-95 % 0.16-0.43). No SRH1 number of any kind has been computed.

## 1. The family

1. **R_set(z, M_b) = f x R_fold(z, M_b)**, f one constant for every redshift and mass, same footing. R_fold is FZS1's
   `rfold_kpc`: FLD1's primary run files (`runs/hubble_<footing>_M<logMb>_zi10_N2400.json`, 12 masses 6.5 to 12), linear
   in z on each stored series, log R linear in log M_b between table masses, M_b^(1/3) outside 6.5 to 12. Capped at the
   halo's r_ta (FZS1's cap).
2. **The layout is FZS1's rule, unchanged** (FZS1 FROZEN_CRITERIA section 1 item 3): M_S(r) = Bar(r) + s C_B(r) for
   r <= R_set and Bar(r) + C_R(r) for r > R_set, s = C_R(R_set) / C_B(R_set), so the enclosed cold mass at R_set is the
   reference's. C_B is the law's (form-B) cold layout, C_R the cold reference's. R_set = 0 gives the reference; R_set = r_ta
   gives FRZ1's form-B layout.
3. **Primary grid (frozen):** f = 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.90, 1.00, 1.25, 1.50,
   2.00. Comparators (reported, never in the window): f = 0 (reference everywhere) and f = inf (R_set = r_ta).
4. **Extension (reported, never graded):** f(z) = f0 (1 + z)^beta, beta in {-1, -0.5, +0.5}, f0 in {0.5, 0.75, 1.0}: G1
   from the halo model, G2 and G3 from the coverage lines. G4 is run on the tilt only if G4 fails somewhere on the primary
   grid.

## 2. The four gates (each reusing the owning lane's code from its own path, read-only; nothing written in their folders)

**G1 forest, upper limit.** FZS1's pipeline exactly (`fzs1_hm.py` and `fzs1_forest.py`, copied into this folder with only
the case list and output names changed; they execute FRZ1's `frz1_hm.py` / `frz1_forest.py` prefixes unchanged), with
fac = f. The record's forest gate as FZS1 used it: DESI DR1 P1D, 755 points, all twelve bins z 2.2 to 4.4, full covariance,
form B's own CLASS reference. **G1 passes at f iff Delta chi^2 <= 4.** Per-bin values reported.

**G2 high-redshift rotation curves, lower limit.** FLD1's line (b) and inputs (`rc100()`: RC100 six-field table, z 0.6 to
2.5, log M_bar and R_e from the paper). **G2 passes at f iff 2.2 R_e <= f R_fold(z_i, M_i) for all 100 galaxies**, i.e.
f >= max_i 2.2 R_e,i / R_fold(z_i, M_i). The fraction covered at 2.2 R_e and at 4 R_e is reported at every f; the 4 R_e
lower limit is reported, not graded (FLD1 graded 2.2 R_e and reported 4 R_e; RC100's 4 R_e is the sample's maximum stated
extent, not a per-galaxy radius).

**G3 present-day rotation curves, lower limit.** Two lines, in order.
- (a) FLD1's line (a1) and inputs (`sparc()`, M_b = 0.5 L36 + 1.33 M_HI): **all 175 SPARC R_last <= f R_fold(0, M_b)**.
- (b) Only at f where (a) fails: PD1's P2-SPARC code (`sparc()` of `pd1.py`, QX8 fit, M_b from the baryon curve at
  Upsilon 0.5 / 0.7, executed from PD1's prefix) with R_trunc = R_set(0, M_b) and no leftover: inside R_set g = glaw(g_N),
  outside g_N + (glaw - g_N)(R_set) (R_set / R)^2. PD1's frozen line: rms <= 0.0660, |mean| <= 0.05, and the same for the
  massive tail (Vflat >= 250 km/s).
- **G3 passes at f iff (a) holds, or (a) fails and (b) holds.**
- Reported at every f (not graded): the SPARC residual under the family's own layout at z = 0 (inside R_set g = g_N +
  s (glaw - g_N); outside g_N + G C_R(R) / R^2, C_R the NFW reference below), and s at R_set for every galaxy (median,
  5-95 %).

**G4 galaxy lensing (ONE1's KiDS host-free row).** ONE1's machinery: `one1_kids.py` executed from its own path up to its
"# ---------------- primary" marker (data side, estimator, fit, neighbour kernel, unchanged). The own-halo model of each
lens enters ONE1's estimator as ONE1's does, as the law's g times a projected ratio: cell value = glaw(k g_bar) x
DeltaSigma_S(R) / DeltaSigma_inf(R), DeltaSigma_inf ONE1's untruncated law halo. DeltaSigma_S is the projection (cosh
substitution, ONE1's form) of the lens's settled layout at its own z_lens with M_b = k M_gal:
- C_B(r) = min(Mph(r), X M_b) (the law's phantom of a central point M_b, ending at x_t; this is ONE1's counted-once halo and
  FRZ1's galaxy-regime mode B with rem = 0), X = ONE1's X (PD1's share, 59.4861 / 59.5029).
- C_R(r) = X M_b m_nfw(r / r_s) / m_nfw(r_ta / r_s): FRZ1's galaxy-regime reference ("Rb") for the halo with
  M_ta = X M_b / (1 - FB) at z_lens, from FRZ1's `halo_basics_z` (Duffy c(M, z), Delta_ta(z)); radii converted from comoving
  Mpc/h to physical.
- Bar = the central point M_b (ONE1's baryons). FRZ1's uncondensed baryons and its cluster regime are not used (ONE1 uses
  neither); disclosed.
- R_set = f R_fold(z_lens, k M_gal), capped at r_ta; s as in section 1. Total mass (1 + X) M_b, as ONE1's halo.
- Tabulated on a grid in log M_b (7 to 13, step 0.05), z (0 to 0.85, step 0.05) and u = R / r_M (ONE1's UG), trilinear in
  (log M_b, z, log u).
- **Neighbours: ONE1's counted-once halos (share X, ONE1's kernel) for every f**, on a fixed lambda grid of 9 nodes
  (ONE1's 7: 0.773 to 2.164, plus 0.65 and 2.57). Not re-laid out: disclosed as an approximation; the no-neighbour readings
  are reported beside.
- **G4 passes at f iff ONE1's frozen gate holds** at the 1.6 R_h veto, KO1 tie rule, k fitted on the inner window:
  G-K1 |R_s,data - R_s,model| <= 2 sigma for all, late, early; G-K2 profile chi^2 <= 9.49 (all); G-K3 type difference
  <= 2 sigma.
- **Readings reported separately:** "host-free" = the graded gate above. "Pooled" = PD1's P2-KiDS pointwise line on
  Brouwer et al. 2021's isolated-lens mass bins (59 points, all colour types pooled, QX5's loader): |log10(g_model /
  glaw(g_bar))| <= 0.05 at every point, the settled layout at z = 0.31 (the median lens z) with M_b the bin's. Reported,
  not graded (PD1's own law-to-R_t halo fails it; see KA-4c).

**Window.** W(footing) = the primary-grid f at which G1, G2, G3 and G4 all pass.

## 3. Labels (per footing)

- **ONE HISTORY PASSES** iff W is not empty, every known answer passes and every MUTATE arm bites. The interval is the
  smallest and largest passing grid f (edges interpolated between grid points, reported). If W has a gap, the label names it.
- **WINDOW EMPTY** iff W is empty, with known answers and MUTATE as above. The RESULT names the gate pair whose pass sets
  are disjoint and the factor between the upper limit and the lower limit (e.g. G1 needs f <= a, G3 needs f >= b, b / a).
  If one gate fails at every grid f, the label names that gate alone.
- **NO VERDICT** iff a known answer fails, a MUTATE arm does not bite, or a gate cannot be evaluated at a grid f (ONE1's
  fit finds no k crossing, a run does not finish). The RESULT says which gate and why.
- **Qualifier, G4 does not test the history:** printed beside the label if G4's status is the same at every grid f and at
  both comparators (f = 0 and f = inf).
- **Qualifier, amplitude:** printed beside the label if the reported family-layout SPARC reading (G3, reported) fails PD1's
  line at every f inside W: then the law holds inside R_set in shape only.

## 4. Known answers

- **KA-G1:** f = 1 reproduces FZS1's 38.741 / 36.66 (+- 0.01); f = 0.5 its 0.189 / 0.19 (+- 0.01); R_set = r_ta reproduces
  FRZ1's 9916.246 / 9008.690 (FZS1's KA-T, 1e-10 on R_cold); R_set = 0 gives 0 (KA-0). FZS1's own KAs (KA-F, KA-M, KA-Z0,
  FRZ1's KA2 / KA3) re-run inside the copy and pass.
- **KA-G2 / KA-G3:** at f = 1, FLD1's worst ratios (UGC00128 0.467; zC 405226 0.391; 4 R_e 0.711) and counts (175 / 175,
  100 / 100) to 1e-6.
- **KA-G3b:** PD1's `sparc()` with PD1's own share table (z 0) reproduces PD1's P2-SPARC rms 0.0563 / 0.0558 (+- 0.0005),
  and with truncation off PD1's law-only value.
- **KA-G4a:** ONE1's own code, run as ONE1 ran it (its lambda grid, X), reproduces its stored primary: model R_s
  1.003 / 0.847, z -1.14 / -0.23 at 1.6 R_h, gate PASS / PASS (1e-6 relative on R_s).
- **KA-G4b:** this lane's projection applied to ONE1's halo (C = min(Mph, X M_b), no reference) equals ONE1's `dsig(u, X)`
  to 1e-3 at u 0.1 to 1e4.
- **KA-G4c:** ONE1's halo pushed through this lane's table, interpolation and 9-node neighbour grid reproduces KA-G4a's
  model R_s within 0.005 and z within 0.05 for all / late / early, both footings.
- **KA-4c (pooled):** with R_set = inf and s = 1 (the law to R_t, no leftover) the pooled reading reproduces PD1's original
  P2-KiDS count (20 / 59 over, worst -0.635 canonical; 24 / 59, -0.675 alt) within 1 point and 0.01 dex.
- **KA-Z0:** the z = 0 table at f = 1 reproduces FZS1's R_tot 1.0019 / 1.0125 (canonical) and 1.0053 / 1.0389 (alt) at
  k 1 / 3 (+- 1e-4).

## 5. MUTATE (each must bite on both footings)

- **MU1, f = 10:** G1 must fail (Delta chi^2 > 4).
- **MU2, f = 0.05:** G2 or G3 must fail.
- **MU3, the redshift dependence of R_fold reversed.**
  - (a) G1: FZS1's MS2 (R_fold read at the mirror DESI bin, z <-> 6.6 - z) at f = 0.6. Line, FZS1's: canonical
    |R_cold(k 10) - 1| falls by >= 20 % at z 2.2 and rises by >= 20 % at z 4.4. Forest Delta chi^2 reported.
  - (b) G2: R_fold read at 3.1 - z (RC100's range 0.6 to 2.5 mirrored). The G2 lower limit must move by >= 10 %.
- **MU4 (G4 power), the reference outside R_set removed** (halo ends at R_set with its cold mass C_R(R_set); total mass not
  conserved) at f = 0.5: the canonical model R_s (all, 1.6 R_h, with neighbours) must move by >= 0.10.

## 6. Reported, not graded

- At every primary f: the z = 0 redistribution factor R_tot at k 1 / 3 h/Mpc that the weak-lensing amplitude row uses
  (FZS1's z = 0 table), beside CO1's (law to r_ta: canonical 1.0033 / 1.0282, alt 1.0076 / 1.0645) and KL1's quoted line
  (0.982 -> 0.972 at k 1 under its C2 response).
- G4 at f = 0 and f = inf; ONE1's halo; per-type R_s and k at every f; the no-neighbour readings.
- The tilt extension (section 1 item 4).

## 7. What counts against (stated now)

- An empty window.
- A window that exists only with the tilt.
- G4 passing at every f and at both comparators: then lensing does not test the history (the qualifier says so).
- s far from 1 inside the window: the law holds inside R_set in shape, not in amplitude (the amplitude qualifier).
- R_fold is FLD1's law-dominated limit (softened point mass, radial shells, no cold mass in the shells' own gravity). A
  window in f is a window in units of that limit, not of a derived settling radius.
- G1 inherits FRZ1's halo model (Tinker 2008 z-scaling and Duffy c(M, z) from memory, PROVISIONAL; present-day baryon
  shapes; linear 1D projection). G4's neighbours keep ONE1's counted-once halos. G2's 2.2 R_e is a sample mean extent.
- The window, if any, is in a family picked after the forest fails were seen.

## 8. Hand estimates (before any number)

**Mine.**
- G1: upper limit f near 0.72 on both footings (from the closure chat's scan; 0.70 passes, 0.75 likely fails).
- G2: lower limit 0.39 at 2.2 R_e (FLD1's worst); 4 R_e would need about 0.71, at the G1 edge.
- G3: (a) gives f >= 0.47; (b) is not reached inside the window.
- G4: passes at every f and at both comparators, model R_s moving by under 0.1 across the grid: inside 100 kpc the NFW
  reference and the law's phantom enclose similar cold mass (my rough s is 0.95 to 1.05 near R_set ~ 0.5 R_fold), and
  the reference is more concentrated than ONE1's halo farther out, which lowers model R_s toward the data. Lensing does
  not test the history (70 %).
- So: ONE HISTORY PASSES on both footings with a window near 0.5 to 0.70, carrying the "G4 does not test the history"
  qualifier. Pooled pointwise reading fails at every f (outer points beyond r_ta), as PD1's halo did.
- Family-layout SPARC reading: passes inside the window (60 %), since s is near 1 there.
- z = 0 redistribution at f 0.6: R_tot(k 1) near 1.001 canonical, between the reference's 1 and FZS1's 1.0019.

**The closure chat's.** G1 gives f at most about 0.72; G3 gives f at least about 0.47; G2 a lower limit near 0.3 to 0.6;
so a window around 0.5 to 0.7 for the first three; G4 is the unknown and may empty it.

## 9. Files (planned)

- `srh1_hm.py` -> `srh1_hm.json` / `.out`, `srh1_hm_MUTATE.json` (copy of FZS1's with the case list changed).
- `srh1_forest.py` -> `srh1_forest_<footing>.json` / `.out`.
- `srh1_rc.py` -> `srh1_rc.json` / `.out` (G2, G3, MU2, MU3b, KA-G2/G3/G3b, the family-layout SPARC reading).
- `srh1_lens.py` -> `srh1_lens.json` / `.out` (G4, KA-G4a-c, MU4, pooled reading, KA-4c).
- `srh1_grade.py` -> `srh1_grade.json` / `.out` (window and labels).
- Amendments, if any, as `AMENDMENT_An.md`, each committed alone, marked post hoc if any number was seen.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

# CFG860 FROZEN CRITERIA: is the dwarf excess tied to gas lost by STRIPPING? Plus the Earth bound (before any script)

**Why.** CFG846: the low-g excess appears only in gas-poor systems at g_bar ≲ 10⁻¹² m/s². H-EX (the cold share of expelled
baryons becomes free; CFG809) failed on placement (CFG822) and on outflow loss traced by the metallicity deficit (CFG852, NO
SIGNAL with power shown). Metallicity marks only gas blown out by winds. Ram-pressure and tidal stripping by a host remove gas
without a metallicity mark, so CFG852 cannot see that route. This lane separates the routes by environment: stripped satellites,
isolated dwarfs that lost their gas without a host, and isolated dwarfs that kept gas.

**Framework statement (cited, not re-derived).** No channel in the framework turns gas into cold energy: the action conserves
cold mass exactly (CFG793). "Gas loss → cold energy" can only mean a share being set free (H-EX) or a share bound by a rule not
yet on the record.

## Part A — dwarfs: three groups at matched g_bar (graded)

**Sample.** Every LVD dwarf (`real_research/data/dsph/lvd_dwarf_mw.csv`, `lvd_dwarf_m31.csv`, `lvd_dwarf_local_field.csv`) with
a measured `vlos_sigma` (not an upper limit), r_h (`rhalf_sph_physical`, else `rhalf_physical`) and `M_V`, excluding CFG852's
rotating / gas-rich set (LMC, SMC, WLM, NGC 6822, IC 1613, Leo A, Sagittarius dIrr, Pegasus dIrr, M 32).

**Groups** (distances `distance_gc` to the Milky Way and `distance_m31` to M31, kpc; HI from `mass_HI` = detection,
`mass_HI_ul` = upper limit):
- **S, stripped satellites:** within 300 kpc of the MW or M31, and no HI detection (upper limit or no HI entry; MW/M31
  satellites inside ~300 kpc are known to be gas-free apart from the excluded LMC/SMC).
- **I0, isolated gas-free:** ≥ 300 kpc from BOTH the MW and M31, and an HI upper limit only (no detection). An isolated
  dwarf with no HI entry at all cannot be classified and is left out (listed).
- **IG, isolated gas-bearing:** ≥ 300 kpc from both, HI detected.
- **SG, satellites with detected HI** (e.g. NGC 185, NGC 205, LGS 3): reported, not graded.

**Δ (same as CFG852's secondary):** Υ_V = 2, M★ = Υ_V L_V with L_V = 10^{0.4(4.83 − M_V)}; Wolf estimator at
r_1/2 = 4/3 r_h, g_obs = 3σ²/r_1/2; g_bar = G (M★/2) / r_1/2²; Δ = log10 g_obs / (g_bar ν(g_bar/a0)); kernel ν_e
(ν = 1/(1 − e^{−√y})); canonical a0 = 9.3603e-11 m/s² graded, alt a0 = 1.1312e-10 reported (CFG828's values).

**Fit.** Δ = a + b (log10 g_bar + 12.5) + c0 [I0] + cG [IG], unweighted least squares on S ∪ I0 ∪ IG. c0 = isolated
gas-free minus satellites at matched g_bar; cG = isolated gas-bearing minus satellites. Errors: stratified bootstrap
(resample within each group), 2000 draws, seed 860; σ = standard deviation of the draws.

**Classes** (canonical footing; checked in this order):
1. **NOT DIAGNOSTIC** if N(I0) < 4 or N(IG) < 4, or σ(c0) > 0.20 dex or σ(cG) > 0.20 dex. (The rival readings differ by
   ~0.4 dex, the satellite mean over the law; σ ≤ 0.20 resolves that at 2σ.)
2. **OPPOSITE** if c0 ≥ +2σ(c0) or cG ≥ +2σ(cG).
3. **STRIPPING** if c0 ≤ −2σ(c0) and cG ≤ −2σ(cG): isolated dwarfs, with or without gas, sit below the satellites.
4. **GAS LOSS, ANY ROUTE** if |c0| < 2σ(c0) and cG ≤ −2σ(cG): isolated gas-free dwarfs match the satellites; gas-bearing
   ones fall below.
5. **NOT GAS** if |c0| < 2σ(c0) and |cG| < 2σ(cG), and both a + c0 and a + cG exceed 0 by ≥ 2σ (bootstrap): every faint
   dwarf carries the excess, gas or no gas, host or no host.
6. **INCONCLUSIVE** otherwise.

**Reported, not graded:** alt footing; isolation cut 350 and 400 kpc; Υ_SFH from CFG828's rows where a dwarf has one;
gas bracket for IG with g_bar from (M★ + 1.33 M_HI)/2 (all gas inside r_1/2: upper bracket); Antlia B dropped (it orbits
NGC 3109); the fit restricted to log10 g_bar < −11.9; per-group means and members; the SG offset; Cetus and Tucana Δ
cross-checked against CFG838's field values.

**Declared limitations.** Distance-only isolation cannot rule out backsplash systems (dwarfs that passed once through a host).
HI non-detections are upper limits of uneven depth. Faint-system kinematic systematics (binaries, small stellar samples) are
shared by all groups and are not corrected here. The isolated groups are small.

## Part R — isolated red lenses (reported, no new statistic)

Isolated (B21) red lenses lost their gas without being satellites. If the excess required host stripping they would sit on the
law. Read CFG850's committed JSON: A_red and A_blue at `canonical|0.123|0.0` and `alt|0.123|0.0` (with the CFG667 +0.123 dex M★
correction), and print them. Scale caveat stated with the numbers: lensing probes 30–300 kpc, the dwarf dispersions
r_1/2 ≈ 0.1–1 kpc, and CFG851 found no single law across the two.

## Part E — the Earth bound (arithmetic, separate script `cfg860_earth_bound.py`)

Question: can removing gas here (a lab vessel, a plant, Earth's atmosphere) set cold energy free, or make it?
- **E1 conversion:** none; the action conserves cold mass (CFG793, η = 0 exactly). Cited.
- **E2 release bound without stiffness:** the cold share tied to gas sitting in Earth's field is at most f = ν(g/a0) − 1 per
  unit gas mass, g = 9.81 m/s² (Earth's field dominates the gas's own; external-field effect). Reported for the simple kernel
  ν = ½ + √(¼ + 1/y) (most generous: f ≈ a0/g) and for ν_e (f = 1/(e^{√y} − 1); print log10 f analytically, it underflows).
  Both footings.
- **E3 with stiffness:** E2 × (s/L*)², the inner limit of CFG691/CFG740's anomaly/Newton, at L* = 24 pc (CFG820's lower edge,
  which gives the largest value), for s = 1 m (lab vessel), 1 km (plant), 6.371e6 m (Earth radius: the atmosphere).
- **E4 natural loss:** Earth's atmosphere loses hydrogen at roughly 3 kg/s (order of magnitude; literature value, provisional
  look-up, not graded). Freed cold mass per year from E2 and from E3 at s = Earth radius.
- **E5 reference:** 1e-9 kg per kg removed (about the relative resolution of the best mass comparators; reference only).
- **E6:** the 541.664 / 595.463 GHz line (CFG799) stays the only lab-scale test of the cold sector; status cited (archive null,
  kill line not reached).
- **E7 (reported):** the non-canonical hot-gas term of CFG745 (C = k·M_hot, k ≈ 3 fitted at galaxy scale, no mechanism) is a
  tethered amount, not a conversion; with the same (s/L*)² factor at s = 1 m.

**Class:** **NO LAB CHANNEL** if E2 with the simple kernel (the most generous case, no stiffness) is below 1e-9 kg per kg on
both footings; **LAB CHANNEL OPEN** otherwise. Disclosed: the order of magnitude (~1e-11 for E2 simple, ~1e-47 for E3 at 1 m)
was estimated in chat before this freeze. Part E is a bound, not a test against data.

## Controls
- **K1:** for Draco, this script's Δ equals CFG852's `delta_ups2` Δ to 1e-9 (same function, same inputs); the fit with
  c0 = cG = 0 reproduces numpy.polyfit's pooled slope.
- **K2 (Part E):** for y = 1e4, simple-kernel f agrees with 1/y to 1e-3 relative.
- **MUTATE** (separate outputs, `CFG860_MUTATE=1`): (a) −0.4 dex on every I0 and IG Δ → must class STRIPPING; (b) −0.4 dex on
  IG only → must class GAS LOSS, ANY ROUTE. The N and σ gates apply as in the real run; if the real run is NOT DIAGNOSTIC, the
  MUTATE prints the c values only and is recorded as "did not bite by rule".

## Resources
A 1024³ run (NCS0) is live. One process, numpy/scipy only, no downloads, well under 1 GB; `OMP_NUM_THREADS=1`.

κ = ½ fitted; cold energy mass required; not theory closed.

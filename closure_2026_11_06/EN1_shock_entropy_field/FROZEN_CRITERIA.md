# EN1 frozen criteria: a shock-entropy field in the khronon sector, graded on the f table and the GB1 battery

Frozen before any EN1 script or EN1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane
(owner proposal, graded as stated; no substitute idea). No particle of any kind. Both footings, graded separately and
never pooled: canonical a0 = 9.3603e-11 m/s^2 (QX5's 9.360324825027975e-11), Lstar 21.7 pc; alt a0 = 1.1312e-10
m/s^2 (QX5's 1.1312035414413022e-10), Lstar 22.9 pc. No downloads. Compute: one thread, under 1 GB, minutes.

## 0. The owner's proposal

Give the khronon sector a second scalar: an entropy field sourced ONLY by shocks (irreversible heating). The extra
gravitating response is set by the cumulative irreversible heating the matter has suffered, not by a host's present
temperature: near zero in a disc that formed by smooth accretion, large in anything that virialised by merging.

## 1. Field definition (frozen)

**The field.** sigma(x, t) is a scalar carried by the baryon fluid with the dimensions of an adiabat (keV cm^2; the
same units as K = kT n_e^(-2/3)). On the baryon worldlines (four-velocity u^mu),

    u^mu nabla_mu sigma = (sigma / c_v) s_dot_shock,      c_v = (3/2) k_B / (mu m_p),

where s_dot_shock >= 0 is the specific entropy production rate of the gas at shocks only (the Rankine-Hugoniot
jump). It is ZERO under adiabatic compression or expansion (sigma, like the adiabat K = P rho^-gamma, is invariant
there), and radiative cooling does NOT enter (cooling lowers K, never sigma). So sigma is the gas's adiabat with
cooling switched off: the shock record. Before structure formation there are no shocks, so sigma = 0 at the CMB
epoch. This is a dissipative source, so EN1 is a field-equation statement, not an action. It is stated as such.

**Volume field.** sigma lives in space. Any baryon at x (gas or stars) sits in the local sigma(x), which is set by the
gas there. Stars carry no shock entropy of their own: violent relaxation of a collisionless system is not a shock and
is not a source ("sourced ONLY by shocks"). A galaxy embedded in a host's hot gas sees the host's sigma.

**Gravitating response.** rho_x is a pressureless energy density comoving with the baryons. It enters the metric
equation as extra Newtonian mass. The a0 law acts on baryons + rho_x as one source inside the AQUAL operator (the one
declared rule, as KD1 P4): g_pred = g_law(b g_N), b = 1 + M_x(<r)/M_b(<r), F = 1, T = 0 in GB1's interface.
Energy bookkeeping: rho_x grows as sigma grows, so the khronon / dark-energy sector must supply it
(nabla_mu (T_b + T_x + T_khronon)^{mu nu} = 0). That exchange is stated, not modelled, and not graded.

**Two readings, frozen as separate variants (never chosen after the numbers):**
- **V-frac (a fraction per baryon):** rho_x(x) = rho_b(x) g(sigma(x)), rho_b all baryons at x.
  M_x(<r) = integral_0^r g(sigma) dM_b. A UDG's own stars inside Coma's ICM pick up g(sigma_Coma).
- **V-dens (a density per volume):** rho_x(x) = lambda sigma(x), independent of the local baryon density.
  M_x(<r) = integral_0^r lambda sigma 4 pi r'^2 dr'. A UDG inside Coma's ICM sees the ICM's rho_x per volume.

**Functional forms (two at most; each has exactly one dimensionful constant):**
- Form L (linear): V-frac g = sigma / sigma_*; V-dens rho_x = lambda sigma.
- Form S (entropy-like, saturating): V-frac only, g = ln(1 + sigma / sigma_*). (Delta s per baryon is logarithmic in
  the adiabat.) V-dens with form S would need a density scale AND an adiabat scale (two constants), so it is not
  defined.
- So three variants are graded: **V-frac-L, V-frac-S, V-dens-L**.

**Measurable difference from the dead keys (stated before grading).**
- QX13 (virial-shock-heated sector with entropy floor, FAIL under): there the SECTOR itself was the shock-heated fluid,
  and its retained mass was limited by its own hydrostatic atmosphere (h_2 = (15/16) H_sh whatever the upstream
  density; class_bound). EN1 is not a fluid that has to be retained. rho_x is slaved to the BARYONS' measured
  adiabat, so QX13's retention bound does not apply. The measured input is different too: QX13 keyed on the infall
  velocity at r_ta/2 (a potential-depth quantity); EN1 keys on the measured gas K(r).
- QX12 iter_2 (host temperature b = p/rho c^2, a step) and the "host temperature" key: K and T are ordered the same
  way ACROSS classes (cold discs < ellipticals < groups < clusters), so across classes EN1 is not separated from a
  temperature key in what is measurable. They do differ WITHIN a host: T(r) is near flat while K(r) rises steeply
  outward (and falls in cool cores). So the separation EN1 can show lives in the X-COP radial rms (G2), in groups at
  R2500 vs R500 (G3), and in ellipticals (low K at high-ish T). The MUTATE twin (section 6) measures it.

## 2. Measured proxy for sigma per class (data on disk only)

Proxy: sigma = K_meas = kT n_e^(-2/3) (keV cm^2), n_e = rho_gas / (mu_e m_p), mu_e = 1.155 (CFG57's frozen value).
K_meas is the present adiabat = shock record minus cooling. Where the cooling time is shorter than the age (cluster
and group cores, elliptical hot atmospheres) K_meas is a LOWER bound on sigma. Disclosed; it is the only measured
record available.

| Class | Proxy | Source on disk |
|---|---|---|
| X-COP (GB1's 7 clusters x 5 radii) | K(r) = kT(r) n_e(r)^(-2/3). kT(r): X-COP spectroscopic temperature profile, log-interpolated in r/R500 and held at the ends (TX1's T_at rule, X-ray only; projected temperatures, disclosed). n_e(r): rho_gas = (dM_gas/dr) / (4 pi r^2) from the deprojected M_gas profile, derivative taken in log space (np.gradient of ln M on ln r). Below the innermost tabulated radius sigma is held at its innermost value | `_external_data/xcop_thermo_2026_11_02/<name>/spectral_results_<name>.fits` (KT) with `<name>_temperature.fits` (RW_X, R500), sha256 in that directory's SOURCES.txt (downloaded 11-02 for TX1; read-only, untracked); `real_research/data/xcop/<name>/<name>_fgas_profile.fits` (MGAS, RADIUS x R500), `<name>_mstar.fits` (stars, for V-frac's dM_b) |
| Groups (Lovisari+2015, 20) | kT = the global kT_keV at both radii (no profile on disk). n_e at R2500 and R500 from the local power law of M_gas between the two radii: s = ln(Mgas500/Mgas2500)/ln(R500/R2500), rho_gas(r) = s M_gas(r)/(4 pi r^3). Inside, sigma is the power law through the two K values (exponent k), so integral_0^r sigma dM = K(r) M(r) s/(s + k) and integral_0^r sigma 4 pi r'^2 dr' = 4 pi K(r) r^3/(3 + k), evaluated numerically on the same power laws for form S | `real_research/data/lovisari2015_groups.tsv` |
| Ellipticals (Humphrey+2006, 7) | K10 = kT_o n_e,10kpc^(-2/3), uniform sigma = K10 at every graded radius (one measured point per galaxy; disclosed). kT_o = Fukazawa's outer temperature. Stars carry the gas's sigma (volume field). M_b(<r): Humphrey Kroupa stars (GB1's, gas neglected per QX18) | `real_research/data/cfg57_gas_sources/fukazawa2006_table4.tsv` (kTo_keV, ne10_1e-3cm3). Six of the seven are there; NGC 6482 is NOT in Fukazawa's table and no other hot-gas profile for it is on disk, so its proxy is None and the graded G4 cell is NO VERDICT (GB1's rule). Reported, not graded: G4's mean on the six with a proxy. Needed file: an NGC 6482 hot-gas kT and n_e (e.g. Humphrey+2006's own profiles) |
| SPARC discs | sigma = 0 at the measured radii: no X-ray-hot gas in the measured discs; the cold ISM's adiabat (T ~ 1e4 K, n ~ 1 cm^-3: K ~ 1e-3 keV cm^2) is ~1e-5 of the cluster values. A measurement-based reading, not an assumption of the answer. Hot CGM lies outside the measured radii | SPARC rotmod (GB1) |
| Coma UDGs (S1's 9) | NO measured Coma ICM density on disk (S1/CFG948 carry only Coma's beta-model shape: kT 8.6 keV, r_c 276 kpc, beta 0.71, no n_e0). So K_Coma cannot be formed. Row G5 = NO VERDICT. Needed file: a Coma ICM electron-density profile (e.g. a ROSAT/XMM beta-model normalisation n_e0, or a deprojected n_e(r)) covering 0.5-2 Mpc. Reported, not graded: the sigma the frozen coupling would need at each UDG to give f = KD1's 86 / 78, beside the X-COP measured K range | `rebuild_2026_10_22/S1_v3_hosted_small/` (searched); `campaign_fresh_gravity/CFG948_nocapture_vs_udgs/` (searched) |
| dSph satellites (LW1) | no shock-heating measure of the host CGM at the satellites on disk: G6 = NO VERDICT | none |
| KiDS lenses (G7) | no hot-gas measure of the isolated lenses' halos on disk: G7 = NO VERDICT | none |
| Solar System (G8) | sigma = 0 at the planets and the Cassini radius (no shocks in the supersonic solar wind inside 10 AU; owner's reading). Reported only: for V-dens, the sigma that would put the record's 1e-10 Msun ephemeris bound (QX13 / C6P) inside 1 AU | C6P (GB1) |

Missing proxy follows GB1's rule: a gate needing a None feature is NO VERDICT, which counts as not passing. No
bracket is defined for any missing proxy (the record states none), so the bracket reading is "NONE".

## 3. Constants

- Exactly ONE dimensionful constant per variant (sigma_* for V-frac-L and V-frac-S, lambda for V-dens-L), fixed ONCE
  per footing on X-COP: the mean over GB1's 35 X-COP points of M_x(<r)/M_b(<r) equals KD1's uniform f need,
  read from `closure_2026_11_06/KD1_unpinned_kq_dust/kd1.json` footings.<f>.uniform_f_diag.Xcop_f_need
  (4.1785998 canonical, 3.7832575 alt). Form L is linear in its constant (closed form); form S by brentq. Nothing
  else is fitted; no scan.
- Tolerances: GB1's lines, unchanged (GB1 FROZEN_CRITERIA e9464bc8ce section 2): G1 |Z| <= 0.057 and rms <=
  rms(L0)+0.010; G2 |mean| <= 0.05 and rms <= 0.10 (HO1); G3 >= 16/20 within 2 sigma_log for f* 0 AND 1; G4 |mean|
  <= 0.15 (QX18 G7 line); G5 |mean| <= 2 sigma_U (S1); G6 every graded dSph class's CI contains 0 (QX21 T2); G7 |R|
  < 2 sigma_tot (QX21 T1); G8 C6P use <= 1.
- G2's mean is near zero by the X-COP calibration (the calibration sets the mean f, not the mean residual); G2 then
  tests the rms, i.e. the radial shape of K.

## 4. The f table (the owner's) and how each cell is labelled

Predicted f per class = mean over the class's GB1 points of M_x(<r)/M_b(<r) at the fixed constant (groups per f*).
Needed f = KD1's uniform_f_diag (SPARC: f_max). The cell label is the class's GB1 gate status (G1 SPARC, G2 X-COP,
G3 groups, G4 ellipticals, G5 UDGs, G6 dSphs), so the tolerance is GB1's line, not a ratio of f's. "Passes the f
table" needs PASS in every class row on both footings for that variant; NO VERDICT counts as not passing.

## 5. Grading and labels

- GB1's loaders, features and gate functions are executed read-only (as kd1.py does); none of GB1's files is edited.
- Per variant and footing: G1-G8 PASS / FAIL / NO VERDICT. G9 (CMB lensing + growth): sigma = 0 before the first
  shocks, so rho_x = 0 at z 3400 and the CMB side is the record's baryons-only control (QX15: +1.7e5, FAIL). Carried
  as FAIL by construction, not re-run.
- Variant labels: PASSES ALL STATIC GATES (G1-G8 PASS both footings) / FAIL (rows) / NOT GRADABLE (rows), GB1's
  rules.
- Reported, not graded: EN1 + QX26 IMF on the ellipticals (b = b_imf + f_x); X-COP with the SZ temperature beyond the
  X-ray range; the K values per class.

## 6. Known answers and MUTATE

- KA1: with the constant at 0 (no rho_x; the candidate then needs no proxy), every G1-G8 row equals gb1.json's L0
  row (status equal, numbers to 1e-12), and the L0 class means equal QX20's KA dict (qx20.py; GB1's KA20) to 1e-6, per
  footing.
- KA2: the density-derivative check: integral of 4 pi r^2 rho_gas dr from the innermost tabulated radius, plus the
  innermost M_gas, reproduces M_gas at every graded X-COP radius to 1e-2 relative.
- KA3: the six Humphrey ellipticals other than NGC 6482 have a Fukazawa row with kT_o and n_e,10kpc finite; all 20 groups have finite K at
  both radii; every X-COP graded radius has finite K > 0.
- MUTATE twin (en1.py --mutate, separate outputs en1_MUTATE.*): the same three variants with sigma replaced by the
  PRESENT temperature kT (keV; discs 0, ellipticals kT_o, groups global kT, X-COP kT(r)), the constant re-fixed on
  X-COP by the same rule. It must FAIL (at least one G1-G8 row FAIL on either footing). If it does not, the run says
  it does not bite. Also reported: "separates" = some row where the main variant PASSES and its MUTATE twin FAILS.
  If no row separates, the battery cannot tell the shock-entropy key from the dead host-temperature key, and the
  run says so.

## 7. Outputs

en1.py writes en1.json / en1.out; en1.py --mutate writes en1_MUTATE.json / en1_MUTATE.out. RESULT.md gives the f
table (class x footing x variant: predicted, needed, PASS / FAIL / NO VERDICT), the GB1 rows, the constants, KA and
MUTATE, and every disclosure. Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.

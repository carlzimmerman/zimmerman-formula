# DB1_cluster_dark_baryons: frozen criteria, committed alone, before any script or graded number of this lane

**Question.** The law (g_N = g^2/(g + a0), a0 = kappa c sqrt(G rho_DE), kappa = 1/2 FITTED) leaves clusters short. The day's lanes say the missing part is collisionless, rides with the galaxies, is cluster-wide, is absent in discs, and isn't a formula over gas fraction, acceleration, size or temperature. Milgrom's cluster baryonic dark matter (CBDM) fits that description on paper: ordinary baryons in compact cold clouds or dim objects, collisionless, comparable to the hot gas, more concentrated than the gas. Can one fixed-form CBDM component make the law pass the cluster gates without breaking anything else, and can such baryons exist?

**Source.** Milgrom 2008, "Marriage a-la-MOND: baryonic dark matter in galaxy clusters and the cooling flow puzzle". The brief cited arXiv:0801.3133; that abstract page is a different Milgrom paper. The CBDM abstract is at arXiv:0712.4203 (web look-up 2026-11-03, PROVISIONAL, abstract only): CBDM mass for a whole cluster "similar to that in hot gas", more centrally concentrated than the hot gas, dominating the core, form unspecified ("very massive black holes to cool, compact gas clouds"). No radial law and no number beyond "similar" is in the abstract, which is why X2 listed it "not tested (no fixed published form)". The forms below are my fixed readings, not Milgrom's.

Ordinary baryons only; no new particle. kappa = 1/2 FITTED. Footings canonical a0 9.3603e-11 and alt 1.1312e-10, reported apart, never pooled. No LCDM input (no Planck numbers, no LCDM background). The cold sector (cold dark energy) stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework.

**Not blind.** I have read RS1, MB1, UX6, MG1, TM2, FR1, X2, FG1, BK2, RQ3's harness. I know MB1's K (mass on stars, 50x) fails keys 7/15, 8/15 and B24, and KG (6.7x gas on the gas, phantom added linearly) passes X-COP fully, keys 6/15, Bullet FAIL. I know BK2's I5 row passes 15/15 keys in its primary cell and fails the Bullet.

## The rule, all arms
CBDM is ordinary mass. **The law acts on it like any baryon:** g = law(g_gas + g_star + g_cb), with g_cb = G M_cb(<r)/r^2. In maps (Bullet, mergers) the CBDM's Newtonian field is added to the baryon field before the law, and the law's direction is the total's. CBDM attaches to X-ray hot intracluster or intragroup gas only: it is applied for harness samples `cluster`, `group`, `xgroup`, `merger`. Every other sample (SPARC discs, LITTLE THINGS, dwarfs, Milky Way, lensing galaxies, planets, ellipticals `et`, TDGs, UDGs, globulars) returns the law exactly. **Why SPARC is untouched:** its gas is cold HI, not hot gas; the hot coronae of spirals are a separate check below.

## Arms. The whole list; no others without an amendment
| Arm | M_cb(<r) | Fitted | Placement in the Bullet and mergers |
|---|---|---|---|
| **P1, tracer** | lambda M_gas(<r500) M_star(<r)/M_star(<r500): the amount set by the gas, the shape the cluster's collisionless tracer | lambda, one per footing | on the galaxies: field R_j x the subcluster's galaxy field, R_j = lambda M_gas,j / M_star,j (model totals) |
| **P1G, gas-shaped collisionless** | lambda M_gas(<r): a relaxed collisionless component with the gas's radial shape | lambda | on the galaxies, R_j = lambda M_gas,j(<300 kpc) / M_star,j(<300 kpc), both about the subcluster's galaxy centre (the gas as it sat before the collision) |
| **P2, cooling-flow core** (Milgrom's reading) | lambda M_gas(<min(r, r_cool)): the deposit of gas from inside r_cool, left where it cooled | lambda | on the galaxies, R_j = lambda M_gas,j(<r_cool,j) / M_star,j |
| **P3, requirement** (labelled REQUIREMENT) | whatever makes law(g_b + g_cb) equal BK2's I5 row, g_I5 = I5(g_b, a0) [(8 pi/3) g_gas / sqrt(a0 g_b) + (g_star/g_b)^4], I5(x, y) = x / (1 - exp(-sqrt(x/y))): g_cb = g_I5^2/(g_I5 + a0) - g_b, floored at 0 | none here (8 pi/3 was chosen by BK2's search) | on the galaxies, R_j = M_cb,j(<300 kpc)/M_star,j(<300 kpc), M_cb,j from the same rule on the subcluster's own spherical gas and stars about its galaxy centre |

**Inputs, set here.**
- X-COP (7 clusters with `mstar.fits`, 35 rows, the harness's rows): M_star(<r) from the harness's `gs`; M_gas(<r500), M_star(<r500) interpolated in log from the same FITS files at the header R500, as the harness interpolates.
- Keys: the harness's template gas `gg`; tracer shape NFW c_g 2.9 on R200 = 1.5 r500, MB1's key reading, normalised at r500; M_gas(<r500) from `gg` at r500.
- Groups B1 (`group`, no gas on file): gas share f 0.5 at all radii (MB1's), f 0.3 and 0.85 reported only. P1 has no tracer there and reads as P1G.
- Lovisari groups B2 (`xgroup`, one aperture each, measured gas): M_cb = lambda M_gas(<r) at that aperture for P1 and P1G (P1's own normalisation needs r500 gas and isn't on the R2500 call); P3 by its rule.
- r_cool (P2): radius where t_cool = 1/H0, H0 = 70 km/s/Mpc (13.97 Gyr; 7.7 Gyr reported only). t_cool = (3/2)(n_e + n_i) kT / (n_e n_H Lambda), Lambda = 3.0e-27 sqrt(T/K) erg cm^3/s (bremsstrahlung, textbook), n_e from the X-COP MGAS profile's derivative (mu_e 1.17, n_i 0.92 n_e, n_H 0.83 n_e) and T from X-COP's own `_temperature.fits` in `_external_data/xcop_thermo_2026_11_02` (on disk, TX1's files). Systems without a T profile on disk (keys, groups): r_cool = the median of X-COP's r_cool/r500 times r500 [READING]. Groups: P2 not computable (no r500); B1 and B2 read as the law, stated. Bullet: T main 14 keV, sub 6 keV (PROVISIONAL, recalled from Markevitch's Chandra work, not looked up), n_e from UX6's Plummer gas about each galaxy centre.
- Bullet: UX6's `SYS`, `observe`, `run` through RQ3's `bullet_ns`, unedited; the own Bullet row replaces the harness's B28, which can only hand g a magnitude, as MB1 did. MG1 rows: MG1's pair model and table, unedited, with my placement.

**The one fitted number.** lambda per arm per footing, set by X-COP mean B23 = 0 (bisection, |mean| < 1e-4 dex). Train = X-COP only; X-COP sits out of its joint as in MB1 and UX3. Everything else is out of sample. P3 fits nothing.

## Gates and tolerances
Set before this lane, from real errors, and never widened after a result:
- RQ3's `acceptance.py` and `tolerances.json`, unedited (|Z| <= 2 on stat plus the stated systematics; X-COP HSE sys 0.12 dex; keys B4-B18 worst of both h and both f*, B19, B20; groups B1, B2; X-COP B23 |mean| <= 0.05, B24 rms <= 0.10, B25). Run per arm with keys.
- **Own Bullet row:** the harness B28 rule: class not FAIL and both M300 within |Z| <= 2 on UX6's PROVISIONAL sigma.
- **MG1 rows:** dkappa > 0 (lens excess on the galaxy side) at every primary GAL row, both footings; reported as sign only. MG1 said any galaxy-tied mass gets the sign nearly by construction, so a pass here weighs little; a fail weighs a lot.
- **Untouched rows** (SPARC A1-A10, dwarfs, MW, lensing A30, planets, ellipticals): must equal the law's RQ3 values to print precision; any difference is a bug.

## Physical existence, gates fixed now (hand plus `db1_phys.py`, numbers with sources, PROVISIONAL where from memory)
Amounts come from the fitted arms (core mass in 300 kpc and the total). For a cloud of mass m and column Sigma_c = m/(pi a^2):
- **(a) X-ray absorption.** Either the mean excess column through the core is <= 2e20 cm^-2 (Chandra/XMM N_H agreeing with Galactic HI at that level; PROVISIONAL, from memory), or the clouds are grey (N_c >= 1e22, tau(0.5 keV) >> 1) with covering fraction f_c <= 0.10 (a grey cover only lowers the emission measure; 10 % is about the gas-mass systematic).
- **(b) Collisionless in the Bullet.** Sigma_c >= 3 x the ICM column swept in one passage (main-cluster central density from UX6's model, 1 Mpc path), and self-gravity G Sigma_c^2 >= rho_ICM v^2 at v = 4700 km/s.
- **(c) Survival over 1/H0.** Conduction: Sigma_c >= the mass per area evaporated at the saturated heat flux (Cowie and McKee 1977 form, q_sat = 0.4 n_e kT (2kT/pi m_e)^0.5) at T 1e8 K, n_e 3e-3; a factor-100 magnetic suppression reported, moves no label. Collisions: t_coll = Sigma_c/(rho_cb sigma_v) >= 1/H0, rho_cb from the fitted core, sigma_v 1000 km/s.
- **(d) Other limits.** Microlensing: a cloud is compact (a microlens) if Sigma_c > Sigma_cr = c^2/(4 pi G D_eff), D_eff = 1 Gpc; compact objects of 1e-5 to 1e2 Msun at a high fraction of the core mass are excluded by caustic-crossing events (Oguri et al. 2018, arXiv:1710.00148, abstract read 2026-11-03, PROVISIONAL, qualitative: "high fractional mass densities" inconsistent). Gate: compact classes in that range fail if CBDM is > 10 % of the projected core mass (the 10 % is my reading of that literature, PROVISIONAL). Metals: any class made through stars (white dwarfs, neutron stars, stellar black holes) fails if its progenitors' metal yield exceeds the ICM's metals (0.3 solar, PROVISIONAL). Star formation: gas clouds that are Jeans-unstable at the CMB floor would form stars; reported.
- **(e) Baryon budget.** Raw data only: BBN with measured D/H (Cooke et al. 2018, 100 Omega_b h^2 = 2.166, PROVISIONAL, from memory; no Planck). Gate: CBDM over all hot-gas systems where the rule applies must not exceed the baryons not already counted (hand, from published census shares, PROVISIONAL).
- **Report which object classes survive all five:** dense H2 clouds (by Sigma_c window), brown dwarfs, Jupiters, sub-Earth H/He bodies, stellar remnants, massive black holes. A class survives only if a Sigma_c or mass window passes all five.

## Labels, per arm, per footing
- **CBDM WORKS ON PAPER** (P1, P1G, P2): B24, B25 pass, 15/15 keys, B19, B20 pass, own Bullet PASS, B1 and B2 no worse than the law's labels, MG1 sign at every primary GAL row.
- **WORKS AND CAN EXIST:** the above, and at least one object class survives (a)-(e).
- **REQUIREMENT MEETS / MISSES** (P3 only): the same gates; never a pass of a rule.
- **FAILS:** anything else, naming the rows.
- Overall RQ3 reads REJECTED for every arm by construction (law rows elsewhere); "hit" means every RQ3 row passes. I expect none.

## Controls and checks (before any graded number is read; a failed check is NO VERDICT for that arm)
- **K1 known answer:** lambda = 0 through the same code reproduces the law's X-COP mean 0.467-ish, rms (RQ3/DR1: +0.467, 0.476 canonical), groups, Bullet M300 1.11, 0.73 (1e14, canonical), and the law's key Z's (RQ3's cached law keys) to 1e-6.
- **K2:** non-listed samples return the law to 1e-12.
- **K3 planted:** mock X-COP masses made from P1G at lambda 3.0 (canonical): the fit recovers 3.0 within 1 %.
- **K4:** UX6's onBCG control PASS, onGas FAIL (MB1's K4b).
- **K5 rerun byte-identical** for the fast grade.
- **MUTATE twin (must bite):** P1G's Bullet CBDM placed on the gas field (same amount): must read Bullet FAIL with dkappa < 0 at both subclusters, both footings; exit 1 by result. Separate outputs.
- **Label control, same tolerance:** P1 with the X-COP clusters' M_gas500/M_star500 ratios cyclically permuted, lambda refit. If its B24 is within 0.005 of real P1's, the per-cluster amount carries no information: reported AMOUNT NOT INFORMATIVE. In the Bullet, P1 with main and sub ratios swapped, reported.

## Expectation on record
- lambda (P1G) about 3.5-4.5, since KG needed 6.7 with the phantom added linearly and the law boosts CBDM by 1.5-2 at cluster g. Milgrom's "similar to the hot gas" (lambda near 1) is short by about 4 on this law's a0 under HSE (70 %).
- P1G passes X-COP (80 %), fails keys like KG, outer keys over-massed (75 %). P1 fails B24 and keys like K (75 %). P2 fails X-COP B24 (90 %). P3 passes most keys, not all four cells (50 %).
- Bullet sign right for P1, P1G, P3 (90 %, nearly by construction); M300 within 2 sigma for at least one arm (50 %).
- Physical: no class survives cleanly (70 %); dense sub-critical H2 clouds the last window, marginal; compact objects die on microlensing or metals.

## Limits, stated now
Static, spherical in relaxed clusters, Plummer maps in mergers. CBDM velocity structure and equilibrium aren't modelled. X-COP is DISPUTED HSE; keys HSC 1.7; Bullet sigma PROVISIONAL. Physical gates are order-of-magnitude, with PROVISIONAL literature inputs, several from memory and labelled so. No downloads.

Compute: one thread, nice 19, under 1 GB RSS, at most two processes.

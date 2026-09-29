# Lane F -- spacetime dimension as the discriminator for kappa = 1/2 (c = 1)

## Bottom line
1. **Dimension does not single out any of the five readings.** With every d-dependence the physics fixes computed from metrics (Friedmann, Tangherlini, Gauss law, Komar/Tolman, volume law, Euler units), the record's readings, once corrected and completed, extend to seven *different* functions kappa(d) (nine candidates, two pairs coincide), all equal to 1/2 at d = 3 and spreading 0.33 .. 1.00 at d = 4; the derived volume-law reading is an eighth (not 1/2 at d = 3). Any two functions normalised to 1/2 at d = 3 cross there, so the record's "lock at d = 3" is guaranteed by normalisation (36/36 pairs of the nine), not a finding.
2. **What does force d = 3 is independent of kappa**, so it cannot choose a reading: (a) the fixed cubic deep-MOND kernel is flat and conformally invariant only at d = 3; (b) the pi-count of "A Lambda = Euler unit" matches only at D = 4. And (a) is contingent: the conformally invariant deep-MOND kernel in d dimensions (p = d) has flat curves and the dS_(d+1)/conformal-group link in **every** d.
3. **One record item is wrong**: the PD11 "Tolman count d-1" uses rho + d p, but the computed D-dimensional acceleration law has (d-2) rho + d p. The vacuum's count is -2 for every d (numerator) or 2/(d-2) (dust-normalised); the "Tolman lock selects d = 3" (GEOMETRIC_EQUATIONS_SYNTHESIS 3.2) is an artifact of the wrong rule.
4. **The "dim SO(d)" lock is not the content**: Z_d^2 dim SO(d) kappa^2 = 8 pi for ANY kappa (Friedmann, G_00 = dim SO(d) H^2). Z_d^2 = 32 pi/dim SO(d) is Friedmann geometry with kappa = 1/2 imposed in every d.
5. **No d-independent topological form of "A Lambda = 32 pi^2"**: the natural D-dim analogue A Lambda^((d-1)/2) carries pi^(d-1) while the Euler unit carries pi^((d+1)/2); the ratio is (rational) kappa^-(d-1) pi^((d-3)/2), transcendental for every algebraic kappa at D = 6, 8, ....

**Verdict: SHARP NO-GO (scoped) for "dimension as discriminator", plus one correction to the record.** kappa = 1/2 stays FITTED; no derivation is claimed.

## What I did (scripts, all exit 0; 130 checks + 15 in the mutation runner)
Notation: spatial d, spacetime D = d+1, G = G_D the Einstein coupling, R* = c/sqrt(G rho_L) = Z_f(d) L with Z_f = 4 sqrt(pi/(d(d-1))), a0 = kappa c sqrt(G rho_L), Z_d = c H/a0 = Z_f/kappa.

| script | content | checks |
|---|---|---|
| `f01_ddim_ingredients.py` | (i) FRW Ricci computed for d = 2..5; static weak field (linearised Ricci, d = 2..5); Tangherlini-dS explicit metrics d = 3,4,5 + symbolic d | 33/33 |
| `f02_deep_mond_ddim.py` | (ii) Gauss law + algebraic MOND in d dims; analytic and numerical (brentq, mu = x/(1+x)) slopes d = 2..6; p-Laplacian, conformal invariance, scaling, dimensional analysis | 34/34 |
| `f03_volume_law_ddim.py` | (iii) the volume-law elastic reading re-derived symbolically in D dims (steps of arXiv:1611.02269 sec. 1.4, 4) | 19/19 |
| `f04_topological_units_ddim.py` | (iv) Euler densities (brute-force contraction D = 2,4,6), units 4 pi, 32 pi^2, 384 pi^3, 6144 pi^4, Chern units, pi-count of A Lambda^((d-1)/2) | 25/25 |
| `f05_reading_matrix.py` | the five readings + new/corrected ones, dim SO(d) identity, gates E, N, F, P, pairwise crossings | 19/19 |
| `f06_mutations.py` | reruns f01-f05 and 10 one-claim mutants (all caught) | 15/15 |

## Results
**(i) Determined pieces (f01).** Friedmann H^2 = 16 pi G rho/(d(d-1)); acceleration addot/a = -8 pi G ((d-2) rho + d p)/(d(d-1)); de Sitter Lambda = 8 pi G rho_L, H^2 = 2 Lambda/(d(d-1)). Weak field: Phi = (d-2) Psi (so the two static channels have lensing weights 1 : 1/(d-2), equal only at d = 3), lap Phi = 8 pi G (d-2) rho/(d-1), i.e. G_N/G_D = 2(d-2)/(d-1) (0, 1, 4/3 at d = 2, 3, 4). Tangherlini-dS f = 1 - mu/r^(d-2) - H^2 r^2 solves R_mu_nu = (2 Lambda/(d-1)) g_mu_nu; black-hole surface gravity **(d-2)/(2 r_s)**; de Sitter horizon surface gravity **H in every d** (so Gibbons-Hawking/Unruh matching is d-independent); a rho-ball is its own horizon at r = 1/H (not at R*). Reading (3) ("a0 = surface gravity at r_s = R*") therefore gives kappa = (d-2)/2. Controls: naive rho + d p law and d-independent 8 pi/3 both match only at d = 3 (fail at 2, 4, 5).

**(ii) Deep-MOND in d dims (f02).** Gauss law g_N ~ 1/r^(d-1); with the record's kernel (mu -> x): g = sqrt(a0 g_N) ~ r^(-(d-1)/2), v ~ r^((3-d)/4): rising at d = 2 (numerical slope +0.2498), flat at d = 3, falling at d = 4 (-0.2500), d = 5 (-0.5); potential ~ r^((3-d)/2): confining/log for d <= 3, bounded (escape possible) for d > 3. Flat curves need g ~ 1/r, i.e. the deep kernel mu ~ x^(d-2); its field equation is the p-Laplacian with p = d, whose action is conformally invariant iff p = d (inversion check). So "flat" <=> "conformally invariant" <=> p = d in every d; the fixed cubic kernel (p = 3) has all of these only at d = 3, and the Milgrom-type scale invariance (t,x) -> lambda(t,x) then scales mass as lambda^(d-3). The isometry group of dS_(d+1) is the conformal group of R^d for every d (dimension count checked; Milgrom's d = 3 statement of ten generators is arXiv:0810.4065, opened), so a dS/conformal reading of deep-MOND extends to every d with the p = d kernel. d = 2 control: Newtonian g_N ~ 1/r is already flat. **Self-correction:** an earlier draft of this lane claimed dimensional analysis alone singles out d = 3 (v^4 = G M a0); wrong: v = (G M)^(1/(2(d-1))) a0^((d-2)/(2(d-1))) exists for every d (f02 D1-D3). Also the record's slope reading (mu'(0) = N) is defined only for the p = 3 kernel; with flat kernels mu'(0) is 0 at d >= 4.

**(iii) Volume law (f03).** V0 = 4 G L/(D-1); S_DE(r) = (r/L) A(r)/(4G) in every D; S_M = -2 pi M r in every D; displacement premise gives V*/V = (D-1)/(D-2); elastic identity (exterior integral of strain^2 = removed volume) holds in every D; result g_D^2 = a0 g_B (D-3)/((D-2)(D-1)) [matches the paper's printed d-spacetime form, = 1/6 at D = 4] => **Z_V(d) = d(d-1)/(d-2) = 2 dim SO(d)/(d-2)**, 6 at d = 3, 6 at d = 4, 6.67 at d = 5. Different d-dependence from the record's Z_d (which falls with d); kappa_V(3) = 0.4824 (Z = 6, N = 2.07): close to, not equal to, 1/2, and rational Z (no pi). It coincides with the record's Z_d nowhere at integer d (crossings at d = 2.584, 2.820). Steps are Gauss-law/thermodynamic where labelled DETERMINED and heuristic premises where labelled PREMISE in the script; this is not a derivation.

**(iv) Topological units (f04).** Euler density of S^(2n) = (2n)!/L^(2n) (brute force D = 2, 4, 6); integral = (4 pi)^n n! chi: 4 pi, **32 pi^2 (D = 4)**, **384 pi^3 (D = 6)**, 6144 pi^4 (D = 8); Chern-character units (2 pi)^n n!: 8 pi^2 (SU(2) instanton) at D = 4, 48 pi^3, 384 pi^4 (Euler/Chern = 2^n). A Lambda alone has dimension L^(d-3); the only dimensionless combination is A Lambda^((d-1)/2) = Omega_(d-1) (2 pi (d-2)^2/kappa^2)^((d-1)/2), which is 32 pi^2 at d = 3, kappa = 1/2 (control passes; kappa = 1 gives 8 pi^2, fails). Ratio to the Euler unit: 1/(4 kappa^2) (d=3), (9/4) pi/kappa^4 (d=5), (3125/144) pi^2/kappa^6 (d=7). The pi-exponent (d-3)/2 vanishes only at d = 3. Readings at d = 5: 36 pi (kappa = 1/2), 4 pi/9 (kappa = 3/2, class B), 400 pi (fixed Z); never 1; near-misses (e.g. 0.877 at d = 7 for class B) are not evidence. Using G rho instead of Lambda leaves a 1/pi in every odd d including d = 3 (Einstein's 8 pi is the missing pi). The de Sitter horizon itself is one pi short of the unit in every d (thermal period). d = 4 (D = 5) is a control where no Euler unit exists; d = 2 has no horizon.

**The readings (f05), kappa(d) = a0/(c sqrt(G rho_L)):**

| candidate | kappa(d) | d=2 | d=3 | d=4 | d=5 | d=6 | status |
|---|---|---|---|---|---|---|---|
| R1 two channels (count 2) | 1/2 | .500 | .500 | .500 | .500 | .500 | count is 2 in every d (numerator of the computed law); kappa = 1/count is a premise |
| R1w channels weighted 1 : 1/(d-2) | (d-2)/(d-1) | 0 | .500 | .667 | .750 | .800 | not in record; count vs weighted count is undetermined |
| R2 record's Tolman d-1 | 1/(d-1) | 1 | .500 | .333 | .250 | .200 | **mis-generalised** (wrong D-dim active density) |
| R2c D-dim Tolman/Komar, dust-normalised 2/(d-2) | (d-2)/2 | 0 | .500 | 1 | 1.5 | 2 | computed; kappa = 1/count is a premise |
| R3 Tangherlini at r_s = R* | (d-2)/2 | 0 | .500 | 1 | 1.5 | 2 | **same function as R2c**; r_s = R* is a premise |
| R3h horizon Ricci scalar = Lambda/4pi (= R6, kappa = 1/2 in G_N units) | sqrt((d-2)/(2(d-1))) | 0 | .500 | .577 | .612 | .632 | equally natural extension of the same d = 3 fact |
| R4 enthalpy premise | (2/3) d/(d+1) | .444 | .500 | .533 | .556 | .571 | premise (2/3, bath enthalpy; known leak) |
| R5 fixed Z | sqrt(3/(2d(d-1))) | .866 | .500 | .354 | .274 | .224 | premise (a fixed d-independent Z; natural only for a thermal Z = 2 pi, not for this coefficient) |
| RV volume-law (derived, f03) | Z_f (d-2)/(d(d-1)) | 0 | .482 | .341 | .238 | .173 | derived given premises; not 1/2 at d = 3 |

Even the one d = 3 fact "K_Sigma = rho" extends two ways (sectional curvature = G rho gives class B; scalar curvature = Lambda/4 pi gives R3h), and "kappa = 1/2" itself depends on which Newton constant multiplies rho (G_D, G_N = 2(d-2)G_D/(d-1)): the convention-free statement is Z_d = cH/a0 (or a0/(c^2 sqrt Lambda)), and it is different for each row.

**dim SO(d) (f05 S1-S3).** For any kappa(d): Z_d^2 dim SO(d) kappa^2 = 8 pi. The record's Z_d^2 = 32 pi/dim SO(d) is R1; with R3 the same identity reads 32 pi/((d-2)^2 dim SO(d)). dim SO(d) = d(d-1)/2 is the coefficient of H^2 in G_00 and enters every reading identically.

**Gates (all computed):**
- F (flat curves, fixed p = 3 kernel) and P (pi-count vs Euler unit): pass only at d = 3, identically for every reading, hence non-discriminating.
- E (the a0-horizon is a horizon of its own Lambda universe, mass <= Nariai): p06 reproduced at d = 3 (7.52); every reading fails at d = 3; only R2c/R3 pass, and only at d >= 11 (R3: 1.19 at d = 10, 0.40 at d = 11). This anti-selects d = 3.
- N (soft: the MOND transition radius r_M^(d-1) = 8 pi G (d-2) M/((d-1) Omega a0) of a fixed mass stays finite as d -> 2+): only kappa proportional to (d-2) passes (R1w, R2c, R3, RV). It only records which readings inherit the Gauss-law factor (d-2); d is an integer, so this is not a physical requirement.
- Class B is the d-dim form of the record's UV/IR bridge: kappa = (d-2)/2 is exactly r_M^(d-1) = r_s^(d-2) R* with no d-dependent coefficient (kappa = 1/2 gives coefficient d-2). That is a restatement of "r_s = R*", not an explanation of it.

**Which of the five survive?** No hard gate discriminates. R2 (Tolman d-1) does not survive as stated (retracted; its correct forms are R1's numerator and R2c). R3 (= R2c) is the reading whose d-dependence is computed from the D-dim physics with the fewest premises (one: r_s = R*, which has the rival R3h), so "least premised" -- that is bookkeeping, not evidence for 1/2. R1, R4, R5 remain premise-dependent. The physics that forces d = 3 (F, P) is reading-independent.

## Not established
- Any d-dimensional version of the framework itself (kernel, action, ownership); "kappa(d)" here is the d-dependence of a reading of the d = 3 number, so a completion could extend differently. In particular the second-dimension check the README of the parent folder asks for cannot be made against data: the only observational anchor of a0 is d = 3.
- The volume-law chain (f03) inherits the paper's heuristic premises (displacement u = Phi L, strain-to-density map); I re-derived it, I did not justify it.
- Gate N is soft; gate E is the Schwarzschild-Nariai bound only (no rotating/charged case).
- Isomorphism dS_(d+1) ~ conformal group of R^d was checked by generator count (standard fact); Milgrom's d = 3 statement was read in arXiv:0810.4065; the D-dim conformally invariant equation was seen only in a search summary, and I derived the p = d statement myself (f02 B).
- The Unruh temperature a/2 pi is d-independent (standard, quoted); the dS side is computed (f01 C-kdS). This is why a thermal matching would make Z d-independent (Z = 2 pi, R5-type), but the record's coefficient is classical (5.789), not 2 pi.
- Nothing here shows kappa = 1/2 is anything but fitted.

## Verdict
**SHARP NO-GO (scoped)**: spacetime dimension is not a discriminator among the readings of kappa = 1/2; the d = 3 selections that survive scrutiny (flat/conformal cubic kernel, D = 4 pi-count) are kappa-independent, and the first is kernel-conditional. One correction to the record (PD11 Tolman rule). Files: this directory, `f01`-`f06` (.py and .out).

Sources opened: arXiv:1611.02269 (volume-law derivation, printed d-dimensional relations); arXiv:0810.4065 (space-time scale invariance, conformal invariance, dS_4 vs conformal group of R^3).

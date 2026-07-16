# METHOD NOTES — reconstructing Chae (2021) ApJ 921, 104 (arXiv:2109.04745) environmental e_N vectors

Source of quotes: ar5iv HTML of 2109.04745, saved at `data/raw/chae21_ar5iv.html`
(plain text extraction: `data/raw/chae21_fulltext.txt`). All quotes verbatim from Section 2-3.

## 0. Definition of e_N

> "an EFE model that is parameterized by e_N ≡ g_Ne/a_0, where a_0 = 1.2×10^-10 m s^-2
> is the MOND acceleration scale"  (Sec. 2)

So e_N is the environmental **Newtonian** field in units of a0 = 1.2e-10 m/s^2.
(a0 enters ONLY as this unit — no framework numerology here.)

## 1. Catalogs Chae used

> "We use four main catalogues: the 2M++ galaxy catalogue (Lavaux & Hudson, 2011), the MCXC
> galaxy clusters catalogue (Piffaretti et al., 2011), the Karachentsev galaxy catalogue
> (Karachentsev et al., 2018 ...) and the NASA-Sloan Atlas (NSA) ... 2M++ and MCXC are used
> for the approximate all-sky calculation of g_Ne,env (Section 3.1) while MCXC, Karachentsev
> and the NSA are used for the more detailed calculation within the SDSS footprint (Section 3.2)."

**The published Table 3 (our GATE-A target, `chae21_env.csv`) comes from the Sec. 3.2
SDSS-footprint calculation** ("We evaluate g_Ne,env ... at the positions of the SPARC galaxies
for a direct comparison with g_Ne,fit", Sec. 3.2.5).
**We implement the Sec. 3.1 all-sky (2M++ + MCXC) estimator** — NSA (~2.7 GB) and Karachentsev
are skipped; the impact is quantified empirically by GATE-A (see gate_report.md).

## 2. 2M++ treatment (Chae Sec. 3.1)

> "we estimate distances from the galaxy's recession velocity in the rest frame of the Cosmic
> Microwave Background assuming a Hubble constant of H0 = 73 km s^-1 Mpc^-1 (as assumed in SPARC)"

> "We estimate stellar masses assuming a mass-to-light ratio of 0.64 in the K_S band
> (consistent with 0.5 in the Spitzer [3.6] band as assumed in SPARC)"

> "We follow the prescription of Lavaux & Hudson (2011) for relating apparent and absolute
> magnitude. We remove sources with K_S > 11.5 which are preferentially seen in the deeper 6dF
> and SDSS fields and cut the catalogue at 200 Mpc. This leaves 54,483 galaxies out of 69,160 in total."

Lavaux & Hudson (2011) magnitude prescription (their Eq. 1, fetched from ar5iv 1105.6107):
M = m − A_K − k(z) + e(z) − DM(D_L), with k(z) = −2.1 z and e(z) = 0.8 z (Bell et al. 2003).
The catalogued K2M++ magnitude is already extinction/aperture corrected, so we apply only
the k+e terms and the distance modulus.

**Our conventions (flagged as ours where not in Chae):**
- D = Vcmb/73 Mpc (Chae). Distance modulus uses D_L = D(1+z_cmb) [ours; negligible at z<0.05].
- Solar absolute magnitude M_sun(Ks, Vega) = 3.28 [ours; standard 2MASS value. Any error here is a
  GLOBAL multiplicative constant, absorbed by GATE-A's single allowed calibration].
- L_K = 10^(−0.4 (M_Ks − 3.28)) Lsun; M* = 0.64 L_K (Chae).
- Ks ≤ 11.5 and D ≤ 200 Mpc cuts (Chae). ZoA mock galaxies ("zoa" Ref) are KEPT (they are part
  of the catalogue's density field by construction).

## 3. Gas masses (Chae Sec. 3.2.2 — he applied this in the SDSS calc; we port it to 2M++, flagged OURS)

> "From Henriques et al. (2015), the early-type fraction is given by
> f_early ≈ 0.28 log(M*/Msun) − 2.12."
> Late types (Eq. 7): "M_g,cold = 11500 (M*/Msun)^0.54 + 0.07 M*"
> Early types (Eq. 8): "log(M_g,hot/Msun) = 1.47 log(M*/Msun) − 5.414"

Chae assigns types stochastically per Monte Carlo draw; we use the deterministic expectation
M_gas = (1−f_early)·M_cold + f_early·M_hot with f_early clipped to [0,1] [ours]. This is a
switch (`--gas`) so its effect is measurable; default ON.

## 4. MCXC clusters (Chae Sec. 3.1.1)

> "M_X = (10^14 Msun / E(z)) 10^((log(L500/E(z)) − A)/B), where A = 44.44, B = 1.11 and
> E(z) = 0.3(1+z)^3 + 0.7."   (Eq. 3; L500 in erg/s)
> "log(M_MOND/Msun) = C + D log(M_X/Msun), finding C = 3.814 and D = 0.728"  (Eq. 4)
> "M_MOND is a factor of several lower than M500, so it is important not to use M500 directly."

NOTE: the ar5iv text renders E(z) = 0.3(1+z)^3+0.7 (no square root). Standard notation would be
E(z) = sqrt(0.3(1+z)^3+0.7). At MCXC redshifts (z<~0.3 for anything that matters here) the
difference is <5% in M_X; we use the paper text AS WRITTEN (a `--ez-sqrt` switch exists to flip it).
Cluster distance: D = c z / 73 Mpc [ours; Chae does not state it separately — consistent with his
velocity-distance convention. MCXC z is heliocentric; the CMB-frame correction is <~300 km/s].

Interior of clusters (Chae Sec. 3.1.2, math alt-text recovered from ar5iv HTML):
> "In case a test point is a distance d < R_500 [of a cluster we scale the contribution by]
> (d/R_500)^3"
i.e. uniform-density interior: g = G M_MOND d / R500^3. We implement exactly this, with
R500 taken from the MCXC catalogue.

## 5. Vector sum (Chae Sec. 3.1.2)

> "We calculate g_Ne,env by linearly summing the g_Ne values of each of the objects in the
> combined catalogue. For galactic sources — and clusters beyond R_500 — we treat the sources
> as point objects ..."
> "To remove numerical artifacts we exclude source objects within 10 kpc of a test point"

Self-exclusion of the SPARC galaxy itself (Chae Sec. 3.2.5):
> "We exclude from the source catalogue the test galaxy under consideration ... for a SPARC
> galaxy, by using NED to determine if it is in the NSA and an RA/Dec match with tolerance
> 0.1 deg to determine if it is in the Karachentsev catalogue."

We exclude any 2M++ source within 0.1 deg of the SPARC position AND with |D_src − D_SPARC| <
max(3 Mpc, 20% of D) [ours: the distance condition prevents removing genuine background objects].

SPARC test-point positions: VizieR J/AJ/152/157/table1 SIMBAD positions; distances = SPARC
`Dist` column (the distances Chae's SPARC fits use).

## 6. The max-clustering vs no-clustering bracket (Chae Secs. 3.2.1, 3.2.4)

Faint galaxies below the survey limit (his SDSS version):
> "we assume either that the mock galaxies are randomly distributed in space within each distance
> annulus (i.e. unclustered), or that they are satellites of the galaxies included in the NSA so
> that they may be considered coincident with them (i.e. maximum clustering) ...
> For the 'max clustering' method we multiply the mass of each NSA galaxy by the reciprocal of the
> mass fraction calculated above for the corresponding distance bin ... We find this boost to
> g_Ne,env to be ~0.1 dex."

Cosmological missing baryons:
> "baryons in the forms we explicitly model amount to ~Ω_b/8 ... meaning that there are potentially
> ~8× more baryons than we have included so far ... 1) they are completely unclustered (or
> equivalently non-existent) so do not alter g_Ne,env, or 2) they are maximally clustered with the
> structures we model ... causing a uniform increase in the magnitude of the g_Ne,env field by a
> factor of 8."

Empirical check on his published table: log_eN_maxclu − log_eN_noclu ≈ 0.89-0.91 dex ≈ log10(8)
per galaxy — the bracket is dominated by the uniform ×8, plus the small (~0.1 dex) faint-galaxy
clustering boost.

**Our bracket implementation:**
- `noclu` (reconstruction of his no-clustering column): raw visible-catalogue vector sum.
  (His unclustered mock mass adds ~no net vector in an all-sky sum; his footprint-restricted
  version adds mostly noise.)
- `maxclu` (reconstruction of his max-clustering column): each 2M++ galaxy mass multiplied by the
  reciprocal of the K-band luminosity-completeness fraction f(D) at its distance (the direct 2M++
  analog of his "multiply the mass of each NSA galaxy by the reciprocal of the mass fraction ...
  for the corresponding distance bin"), then the whole field ×8 for cosmological missing baryons.
  f(D) = Γ(α+2, L_lim(D)/L*) / Γ(α+2) with the 2MASS K-band Schechter LF of Kochanek et al. (2001):
  M*_K = −23.39 + 5 log h (h = 0.73), α = −1.09 [OURS — Chae used the Li & White (2009) r-band SMF
  with the deeper SDSS limit; our correction is larger because 2M++ (Ks ≤ 11.5) is shallower].

## 7. What we knowingly OMIT (all quantified only through GATE-A residuals)

1. NSA depth (r < 17.6 vs Ks < 11.5): within the SDSS footprint Chae resolves much fainter
   structure; our LF up-weighting restores the mass but pins it to bright 2M++ galaxies.
2. Karachentsev Local Volume catalogue (D < 11 Mpc, complete to M_B ≈ −12).
3. The homogeneous grid outside the SDSS footprint (his Sec. 3.2.3): an isotropic homogeneous
   component contributes ~zero net vector in an all-sky sum; we add none.
4. Monte Carlo scatter model (his e_ columns): we produce point estimates only.
5. His 10 kpc exclusion is implemented; NED-based NSA self-match is replaced by the 0.1-deg +
   distance match above.

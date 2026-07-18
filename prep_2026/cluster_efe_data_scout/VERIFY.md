# VERIFY — cluster-EFE sigma-spread MMU data-availability scout

Adversarial re-run + both-ways audit of the three scout scripts in this dir.
Re-ran 2026-07-17. All three exit 0.

```
inventory_manga.py       EXIT 0   MMU-MaNGA alone ~39 ; MaNGA+SAMI ~202
inventory_membership.py  EXIT 0   MMU-MaNGA ~77 ; MaNGA+SAMI ~172
overlap_power.py         EXIT 0   MMU-MaNGA band 40-77 ; stack 135-237 ; z-table
```

Verdict of the verification: **the NO-GO (MMU-MaNGA alone) and MARGINAL-NEEDS-STACK
(MaNGA+SAMI) findings survive. Neither a GO nor a NO-GO is manufactured. Two
honest tightenings below make the picture slightly MORE pessimistic, not less —
so the go/no-go is unchanged and robust.**

---

## (1) Is the diffuse-carrier count HONEST? (the most likely place a GO is faked)

**HONEST — not inflated; if anything the reliable-sigma count is slightly generous
in the OTHER direction (toward NO-GO).**

The three lanes disagree on the MMU-MaNGA-alone number by ~2x (39 vs 77). Traced:
- `inventory_manga.py` builds it granularly from the mass function
  (977 dwarfs x0.45 in-window + 1538 interm x0.10, x0.55 reliable = 326 diffuse
  all-env; x0.12 rich-cluster = **39**).
- `inventory_membership.py` uses a coarser `f_diffuse=0.18` of the FULL 10,059
  (=1810 in-window), x0.50 reliable x0.10 cluster x0.85 tag = **77**.
- `overlap_power.py` reconciles to a **40-77** band, central ~51.

The 0.18 full-sample diffuse fraction (membership lane) is at the GENEROUS end:
MaNGA is a massive-galaxy survey whose sigma_e distribution peaks ~100-150 km/s;
the genuine sigma 20-70 fraction is closer to 6-15% (the granular manga route gives
5.9% kinematic). So 77 is the optimistic corner, 39 the pessimistic. **Both land
NO-GO for MMU-MaNGA alone (target 300-500).** The 2x spread does NOT flip the
verdict — even the generous 77 gives z_opt=1.24. No manufactured GO.

**Does the M*>~5e8 floor genuinely exclude sigma~20-40 dwarfs? YES, confirmed.**
The MaNGA Primary/Secondary selection floors at log M* ~9 (~1e9); very few objects
below 10^8.5. Faber-Jackson puts sigma~20-40 km/s at roughly M* < 10^9, i.e. the
sparsely-sampled bottom of the mass function. The deepest-MOND carriers (a_in << a0,
sigma 20-40) — which carry the LARGEST D(zone) — are the ones MaNGA has fewest of
AND measures worst. This is the predicted failure mode and it is real.

## (2) Is the CORRECTED magnitude used? (~4-9.5% relational, NOT the old 6-13%)

**YES — all three scripts use the corrected value, explicitly.**
`overlap_power.py` line 158: `sig_rel_lo, sig_rel_hi = 0.040, 0.095`; comment
"USE THIS; supersedes old short-memory 6-13%". Both inventory writeups quote
"~0.3-1.5% ABSOLUTE / ~4-9.5% RELATIONAL D(zone)" at framework-committed E10
tau_mem=203 Gyr. **No slippage back to 6-13%.** (Had they used 6-13%, S/N would be
~1.4x higher and MMU-alone would still be NO-GO — so the correction did not create
the deficit; it is the honest committed number.)

## (3) Does MMU-manga serve resolved sigma, or only spectra? (VERIFIED externally)

**VERIFIED: MMU serves RESOLVED STELLAR SIGMA. sigma_int is recoverable as a 2-D
map with NO re-derivation. GO on kinematics.**
- The MMU manga builder downloads BOTH `DRP LOGCUBE` AND `DAP MAPS
  HYB10-MILESHC-MASTARSSP` (MMU README, confirmed via github).
- The build script keeps ALL maps with NO filtering
  (`example['maps'] = [dict(zip(map_cols, i)) for i in grp['maps']]` — no
  emission-line-only selection), so the standard DR17 DAP `STELLAR_SIGMA`,
  `STELLAR_SIGMA_IVAR`, `STELLAR_SIGMACORR` extensions are carried through.
- So the scripts' `MMU_SERVES_STELLAR_SIGMA = True` is correct. No pPXF
  re-reduction needed → no extra re-derivation systematic on that axis.

**BUT one correction to the reliability floor (tightening, toward NO-GO):** the
scripts cite "DAP robust down to ~20 km/s". Verified: that ~20 km/s figure is the
**EMISSION-line** floor (high-SNR gas kinematics). For **STELLAR** sigma — which is
what this test needs — the instrumental LSF is ~72-76 km/s (1sigma) and reliable
stellar sigma bottoms out near HALF the LSF, ~35-45 km/s, only at high continuum
SNR. So the sigma 20-40 stellar band is essentially all upper limits in MaNGA. The
f_reliable ~0.50-0.55 haircut applied to the full 20-70 window is therefore mildly
GENEROUS; the accessible carriers are really the ~45-70 km/s (higher-a_in) end.
Consequence: the accessible subsample carries a SMALLER true D(zone) than the
4-9.5% quoted for the full diffuse population → S/N is if anything overstated, and
the NO-GO is reinforced. Not a manufactured deficit; a real physical limitation.

## (4) Does the systematic + tidal + projection leave a real signal at that N? (S/N)

**The exploratory "~2-3 sigma" is the OPTIMISTIC CORNER, not the central estimate.**
Re-ran the z-table. The honest MID scenario (D=6.7%, purity 0.52, scatter 0.23,
sys 0.020) gives:
- MMU-MaNGA alone (N~77): z_mid = **0.5**
- MaNGA+SAMI stack (N~237): z_mid = **0.9**
- target N=300: z_mid = **0.9** ; even N=500: z_mid = **1.1**

The 2.0-2.7 numbers appear ONLY in the OPT column, which simultaneously stacks the
best-case signal (9.5%), best purity (0.65), lowest scatter (0.18), and lowest sys
floor (0.012) — a low-probability corner. **The central expectation is z<1
everywhere reachable with public data.** The verdict's "underpowered ~2-2.5 sigma
hint on the stack" is defensible only as a best-case ceiling and should be read as
such; the expected outcome is a non-detection.

Two systematics deserve emphasis (both correctly flagged as "systematics-fragile"):
- **Tidal confound is same-signed** as the first-infall-hotter signal and, in
  ABSOLUTE terms (1-3% residual after the F3 radial-profile separator) is
  comparable to the absolute signal (0.3-1.5%). If F3 separation is imperfect the
  tidal residual can mimic the signal outright. In relational/ln units the signal
  (0.039-0.091) still exceeds the sys floor (0.012-0.030) by 1.3-7x, so it is not
  formally swamped — but the margin rests on the F3 separator working as assumed.
- Limiting-factor diagnostic confirms **STATISTICS-limited at every accessible N**
  (se_stat > 0.020 sys floor until N>~400). Opposite of the SDSS single-fiber
  stack. So more carriers is the lever — and public IFU does not have them.

## (5) DESI BGS z-coverage around the ACTUAL low-z clusters — real or assumed?

**The 854 deg^-2 / ~9.5x deepening is a REAL published sky-average (Hahn+2023).
Its application to the SPECIFIC clusters hosting MaNGA carriers is ASSUMED, but
NON-BINDING.**
The script does not identify the individual z<0.05 clusters that host the ~39-77
MaNGA diffuse carriers and confirm DESI DR1 footprint + BGS depth at each. DESI DR1
covers a large fraction of, but not all of, the SDSS/MaNGA footprint, and very
bright nearby giant-elliptical members can fall out of the BGS bright limit
(fainter dwarf members are fine). HOWEVER: membership tagging for these clusters
does NOT depend on DESI — GalWCat19 (1800 clusters, caustic-ready), HeCS, and Yang
groups already tag them from SDSS. DESI is a deepening bonus, not a requirement. So
the "assumed, not cluster-by-cluster verified" gap does NOT touch the verdict,
because the membership/phase-space side is not the bottleneck either way.

---

## BOTH-WAYS CHECK

**Manufactured GO?** No. The generous lane (0.18 diffuse fraction → 77) still lands
NO-GO. The one axis that could inflate a GO — treating the emission-line 20 km/s
floor as if it applied to stellar sigma — was found and corrected in the pessimistic
direction. Resolved sigma IS served, so that "GO on kinematics" is real, not faked.

**Manufactured NO-GO?** No. The counts (39-77) are fair-to-generous, not
understated. The target (300-500) is reasonable for a 2-3sigma firewalled test given
the systematics. The corrected (lower) 4-9.5% magnitude is the committed value, not
a deficit invented to force failure — the old 6-13% would still give NO-GO for
MMU-alone. Membership infrastructure is honestly credited as ABUNDANT (not
understated to depress the count).

---

## VERDICT (data-availability go/no-go only; MI-class-generic; NOT a physics claim; no "proves")

**CONFIRMED: NO-GO from public MMU data now.**

- **MMU-MaNGA ALONE = NO-GO.** ~40-77 diffuse tagged cluster members (tens). Even
  the best-case z~1.2; central z~0.5. Dies on statistics. Root cause verified and
  real: MaNGA is stellar-mass-limited (floor log M*~9) and field-dominated, so the
  sigma 20-70 (especially 20-45) deep-MOND carriers are both rare and jammed against
  the ~72-76 km/s stellar LSF (upper limits, not values).
- **MaNGA+SAMI public stack = MARGINAL/UNDERPOWERED** (~135-237), and SAMI is public
  but NOT served by MMU — so it fails the literal "assemble from MMU now" framing.
  Central z~0.9; the "~2-2.5sigma" is an optimistic ceiling, expected outcome is a
  non-detection.
- **Resolved stellar sigma IS served by MMU-MaNGA** (DAP MAPS kept in full) — that
  half of the feasibility is genuinely GO; the binding failure is carrier COUNT, not
  data type.

**What is needed (unchanged, endorsed):** (i) ingest SAMI cluster IFU into the
stack; for a clean >3-5sigma bite (ii) a dedicated wide nearby-cluster dwarf-IFU
survey (M* floor to log M~8, resolved stellar sigma reliable well below 45 km/s,
sub-percent systematics) or (iii) ELT/HARMONI-class resolved dwarf kinematics
(~2032). The membership/caustic scaffolding (GalWCat19+HeCS+DESI DR1 BGS) is ready
and slots in once the diffuse-carrier IFU sample exists.

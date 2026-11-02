# MG1_merger_sample: the Bullet's failure of local gas repeats. At the frozen reading 8 of 9 subclusters with lensing able to decide have peaks on galaxies, none on gas, 1 between, in 6 systems. L1, L2 DEAD IN GENERAL on both footings. N1 NOT GENERALISED. N2 sign holds at the primary reading and FAILS at the other reading of an ambiguous criterion. All from published numbers read off the web, PROVISIONAL, on a sample chosen for visible offsets. Not a map-level test

**The count is less firm than 8 of 9 sounds.**
- Reading "s resolved" with the row's lens sigma (primary, A3): GAL 8, BETWEEN 1, of 9. Reading it with s's own error: GAL 7, BETWEEN 2, UNRESOLVED 3, of 12, which is 58 %, under the frozen 2/3, so **N2 reads SIGN FAILS** there. Three of those 12 can't decide anything; dropping them is the primary's logic, but the frozen text didn't say which, and I chose knowing the hand sums (`AMENDMENTS.md`).
- Published errors only: GAL 5, BETWEEN 1, of 6. Assumed errors x 2: GAL 6, BETWEEN 1, UNRESOLVED 2.
- ZwCl 0008 E sits at Z 1.98, and turns BETWEEN with the BCG as tracer. A threshold of 1 sigma: GAL 3, BETWEEN 6.
- **Rows that are GAL with published errors and not at the edge: 4 in 3 systems.** MACS J0025 SE, NW; A56 S; A1758 NE. One of those, A1758 NE, is a ground-based fitted centre.
- With the Bullet in: GAL 10, BETWEEN 1, of 11.

Criteria `FROZEN_CRITERIA.md` (f344a35675), committed alone first. Amendments `AMENDMENTS.md` (8401b58d04). Table `mg1_table.csv`, script `mg1_merger.py`, numbers `mg1_merger.out`, `mg1_results.json`, twin `_MUTATE`. **Not blind.** A description, no action. The cold sector stays retired; nothing here reinstates it. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. No file downloaded on purpose (see Errors).

## Table, PROVISIONAL, kpc. Z = d/sigma, label at 2 sigma
| Subcluster, z | d(lens, gal) | d(lens, gas) | s | Z gal, gas | label | Masses used (M_lens) | Note | Ref |
|---|---|---|---|---|---|---|---|---|
| Bullet main, 0.296 (control) | 0 ± 41 | 209 ± 41 | 209 | 0.0, 5.1 | GAL | 3.5e14 (<300) | UX6 inputs | [Clowe 2006](https://arxiv.org/abs/astro-ph/0608407) |
| Bullet sub (control) | 0 ± 38 | 194 ± 38 | 194 | 0.0, 5.1 | GAL | 2.3e14 | | same |
| MACS J0025 SE, 0.586 | 45 ± 112 | 326 ± 91 | 371 | 0.4, 3.6 | **GAL** | 2.5e14 (<300), gas 2.75e13, stars 2.7e12 | gas split evenly | [Bradac 2008](https://arxiv.org/abs/0806.2320) |
| MACS J0025 NW | 29 ± 94 | 199 ± 57 | 170 | 0.3, 3.5 | **GAL** | 2.6e14, 2.75e13, 1.9e12 | paper: >4 sigma | same |
| A56 S, 0.302 | 7 ± 16 | 104 ± 41 | 111 | 0.4, 2.5 | **GAL** | M200 4.5e14 | offset by subtraction | [A56](https://iopscience.iop.org/article/10.3847/1538-4357/acdb73) |
| A56 N | 87 ± 22 | 337 ± 44 | 424 | 4.0, 7.7 | **BETWEEN** | 2.8e14 | gas PROXY; "tentative" | same |
| CIZA J0107 NE, 0.105 | 21 ± 14 | 160 ± 50* | 160 | 1.5, 3.2 | **GAL** | 2.8e14 | *ASSUMED; UNRESOLVED at x 2 | [2210.12165](https://arxiv.org/abs/2210.12165) |
| CIZA J0107 SW | 27 ± 19 | 160 ± 50* | 160 | 1.4, 3.2 | **GAL** | 3.1e14 | same | same |
| ZwCl 0008 E, 0.104 | 249 ± 126 | 319 ± 52 | 420 | 1.98, 6.1 | **GAL** | 5.73e14 | BCG tracer: BETWEEN | [Golovich 2017](https://arxiv.org/abs/1703.04803) |
| A1758 NE, 0.278 | 128 ± 77 | 408 ± 64 | 408 | 1.7, 6.4 | **GAL** | 5.49e14 | fitted centre, ground | [1605.07595](https://arxiv.org/abs/1605.07595) |
| Musket Ball S, 0.534 | 80 ± 50* | 538 ± 54 | 538 | 1.6, 10 | **GAL** | 3.2e14 | *ASSUMED; gal number via [Wittman's table](https://arxiv.org/abs/1701.05877), which came through scrambled; gas in [Dawson 2012](https://arxiv.org/abs/1110.4391) | |
| A2034 S, 0.112 | 173 ± 76 | 348 ± 99 | 187 | 2.3, 3.5 | BETWEEN, out of primary (s/sigma 1.89) | 2.35e14 | lens **beyond** the BCG from the gas; paper says within 2 sigma | [1808.09449](https://arxiv.org/abs/1808.09449) |
| RM J1508 NE, 0.542 | 145 ± 148 | 37 ± 93 | 182 | 1.0, 0.4 | UNRESOLVED | 5.5e14 | | [2307.10174](https://arxiv.org/abs/2307.10174) |
| RM J1508 SW | 27 ± 50 | 80 ± 62 | 107 | 0.5, 1.3 | UNRESOLVED | 5.2e14 | | same |
| ZwCl 0008 W | 170 ± 131 | 176 ± 129 | 12 | 1.3, 1.4 | UNRESOLVED | 1.21e14 | gas on galaxies | as above |
| A2744 Core, 0.308 | 61 ± 50 | 99 ± 54 | 99 | 1.2, 1.8 | UNRESOLVED | 2.24e14 (<250) | s PROXY; paper gives 17 and 22 arcsec | [Merten 2011](https://arxiv.org/abs/1103.2772) |

Where no gas or star mass is listed: DEFAULT 0.12, 0.02 of M_lens, and M_lens mixes M200 with apertures. Numbers in the table are rounded; `mg1_merger.out` is exact.

### NOT USABLE on the frozen rule: no number on at least one offset. Of the eight systems the lane named, only three reach the primary count
| System | What the paper says | Which way it leans |
|---|---|---|
| **Abell 520** | [Jee 2014](https://arxiv.org/abs/1401.3356): P3' dark peak, 3.94e13 in 150 kpc, M/L 813, better agreement with the strongest X-ray; moved ~1' from J12. [Clowe 2012](https://arxiv.org/abs/1209.2143): no excess at the gas, M/L 114 ± 54 consistent with the rest, under 2.3 sigma against constant M/L. No offsets as numbers from either | **Contested. If Jee is right: a lens peak on gas, against N2 and the one row of the sort local gas wants. If Clowe: follows galaxies.** The four normal peaks follow light in both |
| El Gordo | [Kim 2021](https://arxiv.org/abs/2106.00031): SE X-ray 97 kpc from mass, ~2 sigma; mass "coincide within 1 sigma" with luminosity peaks; 360 kpc, 6.6 sigma from SE galaxy number peak. NW no X-ray clump | galaxies by light, not by number |
| Abell 2744 others | [Jauzac 2016](https://arxiv.org/abs/1606.04527): gas 120 kpc off the core, 80 kpc off N. No galaxy offsets | no read |
| MACS J0717 | [Jauzac 2018](https://arxiv.org/abs/1711.01324): coordinates give lens-gas 41 to 272 kpc by the summariser's arithmetic, against the paper's "almost perfect" for two; "optical counterparts" only. Limousin 2012 (A&A 544, A71) says mass follows light and not gas; only a search snippet read | galaxies, unquantified |
| Abell 754 | [Okabe & Umetsu](https://arxiv.org/abs/astro-ph/0702649): central peak on BCG; E clump off the X-ray clump, opposite its motion, unquantified | galaxies |
| A1758 NW, A2146, A115, A3376 E, A1750, A1914 | Lens, BCG, X-ray all agree within resolution | can't decide |
| A2034 N, A1758 S | One offset only; A1758 S's centre is fixed on the BCG | no read |
| CIZA J2242 | [Jee 2015](https://arxiv.org/abs/1410.2898): lens ~190 kpc off the luminosity peak at both, p 0.08, 0.29; no gas number | **off galaxies, marginal** |
| Musket Ball N | Gas 1.4' ± 0.49', no galaxy number | no read |

### Ensemble, reported, no label
[Harvey 2015](https://arxiv.org/abs/1503.07675), 72 substructures in 30 systems: mean mass-star offset -5.8 ± 8.2 kpc, with a 60 kpc error assumed per star-gas row; a filter pipeline. [Wittman 2018](https://arxiv.org/abs/1701.05877) reworks it, omits many rows, and finds 67 of 72 outside the small-offset regime. A [2026 review](https://arxiv.org/abs/2608.16987) reports it finds an El Gordo peak spurious; only the first 100,000 characters read; no per-merger table in them. This is the fair place to look: per-row Table S1 is what would fix my selection, not read.

## Model read on an isolated pair: sign and position only
| Form | canonical, k fit, 9 primary rows | alt | Verdict |
|---|---|---|---|
| L1 | GAL with dkappa <= 0: 8 of 8, in 6 systems. dkappa > 0 at 0 of 9 | same | **DEAD IN GENERAL**, both footings, both k |
| L2 | same | same | **DEAD IN GENERAL**, both footings, both k |
| N1 | wrong sign at 5 of 8 GAL in 4 systems; +ve at A56 S, CIZA J0107 NE, SW | same | **NOT GENERALISED**, both, both k |
| N2 | dkappa > 0 at 9 of 9, delta > 0.5 at 8 | same | sign: **SIGN HOLDS** primary, published only, assumed x 2; **SIGN FAILS** other reading of s |

Size: L1 dkappa runs -0.07 (A56 S) to -1.05 (ZwCl E), canonical at k fit, on default gas. Gas x 0.5 lifts A56 S to +0.006; that's the only primary row that flips, 7 of 9 still wrong. Gas x 2 worsens all. Bullet pair control: L1 -0.162, -0.113, N2 +0.074, +0.078; UX6's full model has L1 -0.212, -1.158, N2 +0.069, +0.422, so same signs, but the pair badly underestimates the sub's size.

### What it says
- **Local gas.** L1, L2 predict a mass excess at the gas side wherever there's gas apart from galaxies. Published lens peaks don't sit there. The Bullet wasn't special. Solid in sign unless the A520 reading of Jee's generalises.
- **N1** escapes only in rows with small s and small default gas, where the term has little to separate. No evidence for it; it is simply not refuted in general by the pair, and UX6 kills it on the Bullet.
- **Carried memory.** Sign is **nearly by construction** in this model: N2 puts its term about the galaxies, so +ve dkappa at 9 of 9 tests little beyond that. It is an observation about position that any mass moving with the galaxies would also give. This can't separate memory from that, and it says nothing on mass, carrier or mechanism. UX6's main-peak and mass failures stand. Not a pass.
- **Possible cracks for anything galaxy-tied:** A520 P3' if real, A2034 S beyond the BCG, CIZA J2242 off luminosity, ZwCl 0008 E between on the BCG tracer, A56 N. Each marginal or contested.

## Checks
K1 Bullet sign PASS. K2 PASS, 2e-16, 4e-5. K3 PASS. K4 PASS, a weak check: references present, not values right. K5 PASS. K6 PASS, +1.259, -1.391.
**K7 partial.** Second reads: MACS J0025 Table 2 re-read, same; its NW 29 kpc matches Wittman's independently quoted -29 kpc. ZwCl Table 4 re-read, same page, same summariser; abstract also says no significant dark-galaxy offset. A1758 96 (+14/-15) arcsec, abstract, same. A56, CIZA J0107, RM J1508 agree with search snippets. **Not re-read: Musket Ball's 80 kpc, A2034's table.**
**MUTATE:** K2, K3, K6 FAIL as required, exit 1. Rerun byte-identical.

## Files for a map-level test, for approval. Sizes from HEAD requests 2026-11-02, nothing fetched. Target names for each ObsID checked on Chandra's catalogue page
Lens: `https://archive.stsci.edu/pub/hlsp/frontier/{abell2744,macs0717}/models/cats/v4.1/`. Chandra: `https://cxc.cfa.harvard.edu/cdaftp/byobsid/<last digit>/<obsid>/primary/`. HST: `https://archive.stsci.edu/pub/hlsp/frontier/<cluster>/images/hst/<version>/`.

**Abell 2744, smallest full test, 185,100,000 bytes approx with its one mosaic**
| File | Bytes |
|---|---|
| hlsp_frontier_model_abell2744_cats_v4.1_kappa.fits | 16,007,040 |
| hlsp_frontier_model_abell2744_cats_v4.1_readme.txt | 4,051 |
| acisf08477N003_evt2.fits.gz (ObsID 8477) | 14,422,267 |
| acisf07915N003_evt2.fits.gz (7915) | 5,628,670 |
| acisf08557N003_evt2.fits.gz (8557) | 8,747,210 |
| acisf02212N005_evt2.fits.gz (2212) | 7,959,255 |
| hlsp_frontier_hst_acs-60mas-selfcal_abell2744_f814w_v1.0-epoch2_drz.fits (v1.0-epoch2) | 132,330,240 |
| .../catalogs/subaru/hlsp_frontier_subaru_suprimecam_abell2744-astrom_i_v1_cat.txt, optional | 1,681,339 |

**MACS J0717**
| File | Bytes |
|---|---|
| hlsp_frontier_model_macs0717_cats_v4.1_kappa.fits | 4,006,080 |
| hlsp_frontier_model_macs0717_cats_v4.1_readme.txt | 3,240 |
| acisf04200N005_evt2.fits.gz (4200) | 6,652,037 |
| acisf16235N003_evt2.fits.gz (16235) | 6,798,202 |
| acisf16305N003_evt2.fits.gz (16305) | 8,929,398 |
| hlsp_frontier_hst_acs-60mas-selfcal_macs0717_f814w_v1.0-epoch1_drz.fits (v1.0-epoch1) | 100,834,560 |

**X-ray only so far: no public lens map found by me, so they can't run the test yet**
| System | Files | Bytes |
|---|---|---|
| MACS J0025 | acisf10413N004 (10413) 11,225,547; acisf05010N009 (5010) 2,724,533 | 13,950,080 |
| El Gordo | acisf12258N003 8,620,377; acisf14022N002 23,411,236; acisf14023N002 14,818,253 | 46,849,866 |
| Abell 520 | acisf00528N004 1,518,838; acisf04215N004 8,631,037; acisf07703N005 555,367; acisf09424N003 19,215,635; acisf09425N004 19,684,106; acisf09426N003 18,719,089; acisf09430N003 19,391,395 | 87,715,467 |

All `_evt2.fits.gz`. ObsID 7703 is small, may not be worth taking; 11405, which I guessed, is someone else's target, **dropped**. A520's lens needs shear catalogues or a map from the authors; RELICS path for El Gordo returned no listing, unverified either way.

**Sample table:** `https://arxiv.org/e-print/1503.07675`, 4,316,313 bytes, Harvey's source with supplement; a table S1 inside is **unconfirmed**: one search says the supplement lists Figs S1 to S8 only, the paper's text says Table S1. Or the PDF, `https://arxiv.org/pdf/1503.07675`, 2,275,401 bytes. If the table's there, it reaches 72 rows.

HFF kappa is strong-lens dominated, core-limited, and a model; A2744's outer clumps are its weakest part. The test needs a filter choice frozen first.

## Expectation against result
Most usable rows GAL 70 %: yes. Local-gas DEAD IN GENERAL 60 %: yes for L1, L2, no for N1. N2 holds 75 %: at primary. Many rows lacking errors 85 %: most systems named had none at all, more than I guessed. A520 exception in some reading 80 %: qualitatively, not countable.

## Limits, errors, unfinished
- Mixed methods, resolution, apertures; ground and space; strong and weak. Selection toward visible offsets, so **8 of 9 isn't a rate.** Gas peak isn't gas mass centre; one peak isn't the mass map. A lens map is itself a reconstruction, and peak offsets at this S/N are noisy and biased high.
- Isolated pair, static, Plummer, default masses for most rows, a_gas and a_star fixed, projection ignored, no partner. a0 at z = 0, with rows to z 0.59. X-COP's k carried over. No mass grade.
- WebFetch reads through a summariser; several table extractions were called garbled by it. I transcribed through it.
- **A1, A2, A3 written after hand sums.** Script's first run came before the amendments' commit, because of another session's git lock; disclosed in that file. K4 as built is a presence check.
- WebFetch on arXiv 1410.7019 saved a 1.6 MB PDF to the session's tool-results store on its own, outside the repo, unread for its numbers. Not asked for; not used. That paper's peak offsets remain unread. arXiv 2106.00031's PDF and 2608.16987's PDF refused for size.
- A1758's and others' kpc are the summariser's conversions from the papers' arcsec scales. MACS J0717's are its arithmetic.
- Unfinished: A3376, A2163, A3411, PLCK G287 and the 29-relic sample (BCG offsets only: mean 75 ± 14 kpc) not tabulated. Map-level test awaits approval.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

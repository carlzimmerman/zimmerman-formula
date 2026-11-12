# LIT1 RESULT: Milky Way prior art under MOND and modified gravity

2026-11-12. Literature sweep, not a graded lane. Plan frozen first (`SEARCH_PLAN.md`, hash in
`FREEZE_STAMP.txt`, 2026-11-12T20:25:16Z). Every number below is a web look-up and is PROVISIONAL;
each carries its URL. Abstract pages and arXiv HTML were preferred; where a number came from a PDF
the text was extracted locally and read in context. Search engine summaries were used only to find
papers; numbers in the table were read from the paper or its abstract page unless marked
"(secondary)". kappa is not touched.

## Answers

**Q1. Anything since DESI DR2 Results III?** Nothing found. Semantic Scholar lists 0 citations of
2611.05518 (queried 2026-11-12). An arXiv API search of abstracts with "Milky Way" plus mass,
potential, rotation curve or gravity, newest first, shows 27 entries from 2026-11-03 to 2026-11-10;
none mentions MOND or modified gravity, and the only ones on the Milky Way mass are the four DESI
papers themselves (plus 2611.13837, a phase-snail potential paper, not about DESI). An arXiv search
for MOND / Milgromian / modified Newtonian dynamics gives two November 2026 papers (2611.08702 on
clusters, 2611.03770 on early structure), neither on the Milky Way. No critique of the Auriga mock
calibration was found. Caveats: arXiv postings after 2026-11-10 were not seen; INSPIRE's citation
query did not parse and ADS was not queried; Google Scholar not reachable.

**Q2. MOND fits to the Milky Way rotation curve since Gaia DR3; is ~7e10 Msun of stars already in
the literature?** Yes, close to it. Sylos Labini et al. 2023 (ApJ 945, 3; arXiv:2302.01379) fit MOND
(simple nu, a0 = 1.2e-10, no external field, bulge not fitted, disc mass and scale length free) to
Gaia DR3 curves and get Md = 7.79 +/- 0.5 (stat) +/- 0.7 (syst) x 10^10 Msun, Rd = 3.1 kpc (7.24 and
7.97 x 10^10 for the other two samples); they say MOND fits well to 19 kpc and poorly beyond 20 kpc.
Banik and Zhao 2018 (arXiv:1708.03771) state that MOND needs a disc of about 7 x 10^10 Msun (stars
plus gas, citing McGaugh 2016's model) to explain the rotation curve. Oria et al. 2021 use 7.5 x 10^10
baryons (6.37 disc incl. 1.13 gas, 0.7 bulge). Against the claimed Keplerian decline (Jiao et al.
2023, 2.06e11 total; Ou et al. 2023/24, Mvir 1.81e11): Coquery and Blanchard 2025 find standard MOND
cannot reproduce the decline with a standard baryon model; freed, the fit wants a stellar disc of
order 1e11 and a0 < 0.53e-10 (95 per cent). Chan and Law 2023 claim MOND "almost" excluded at more than
5 sigma at 17 to 23 kpc; Wang et al. 2026 claim more than 13 sigma using vertical phase spirals and
say adding an external field makes the outer discrepancy worse; Singh et al. 2026 find MOND
(three nu functions) worse than cored halos. Beordo et al. 2024 find MOND and LambdaCDM statistically
equivalent to 19 kpc. MOG (Moffat et al. 2024) needs Mb ~ 1.3e11 and attributes the excess to
circumgalactic gas. The 2026 review (arXiv:2608.10189) says the external field's effect on the decline
is an open question, not assessed against the Jiao data. None of these papers uses the DESI DR2
halo-star masses.

**Q3. External field at the Milky Way.** Published MOND works adopt 0.01 to 0.03 a0 as the actual
(MOND) external acceleration: Famaey, Bruneton and Zhao 2007, of order a0/100 from the 550 km/s
local escape speed; Wu et al. 2008, 0.01 a0 baseline, in the Sun to Galactic-centre direction,
attributed to the Great Attractor region (H0 x 600 km/s), with 0.03 a0 as an upper limit for a bound
LMC; Banik and Zhao 2018, 0.015 a0 from the Local Group's 630 km/s peculiar velocity, but 0.03 a0 or
more needed to match the escape-speed curve, field taken along the disc axis; Oria et al. 2021 (full
Local Volume QUMOND), Virgo the dominant source and the Milky Way "not under a strong EFE". Chae et al.
2020 give environmental fields for SPARC galaxies with mean 0.033 and range 0.02 to 0.05 (units of
g-dagger), from 2M++ abundance-matched total masses; they give no Milky Way value.

Comparison with the record's 0.01273 (canonical; 0.01054 alt), toward (l, b) = (268.5, +33.0): the
record's value is labelled **Newtonian** e_N and is entered inside nu. Numerically it equals the
literature's estimate of the **actual** acceleration of the Local Group (linear theory from 600 to
630 km/s gives 0.0099 to 0.0104 a0; H0 x v gives 0.011 to 0.012 a0). Under the simple nu, a Newtonian
0.01273 corresponds to an actual field of about 0.119 a0, four to twelve times the published 0.01 to
0.03 a0; conversely the published 0.01 / 0.015 / 0.03 a0 correspond to Newtonian e_N of about 0.0001 /
0.0002 / 0.0009 (arithmetic here, not from a source). The record's reconstruction (2M++, LambdaCDM
bias and growth rate) also measures total-matter gravity. **This convention question is unresolved
here and should be checked**: if the published convention applies, every literature field lies far
inside MWJ1's and PLT1's windows (e_N below 0.0075). Unconfirmed: whether Chae et al. 2020 enter e as
a Newtonian or MOND quantity in their fitting function.

**Q4. Outer Milky Way in MOND, and hot gas.** Escape speed: Famaey et al. 2007 and Wu et al. 2008
(local 544 km/s, LMC bound), Banik and Zhao 2018 (8 to 50 kpc, Williams et al. 2017 data; model
521 km/s locally). External-field truncation: Wu et al. 2008 place the external field's effect at
about 200 kpc for 0.03 a0 and the negative phantom-density zone near 600 kpc for 0.01 a0 (200 kpc for
0.03); Oria et al. 2021 find isolated and EFE rotation curves separate at 150 to 200 kpc and a phantom
mass of 1.39e12 at r200. Streams: Thomas et al. 2017 (Sagittarius N-body in MOND); Koop et al. 2024
(Helmi streams disperse too fast in MOND); satellites: Asencio et al. 2026 (tidal features), and
Lueghausen et al. 2014. Hot gas in the baryon budget: yes, in two MOND works, pointing opposite ways.
Banik and Zhao 2018 include a Plummer corona of 2 to 8e10 Msun and prefer about 2e10 or none (escape
speed). Thomas et al. 2017 need a flattened corona of about 1.5e11 within 100 kpc (2.6e11 total) to
reproduce Sagittarius leading-arm velocities. MOG work (Moffat et al.) also invokes circumgalactic
gas. No published MOND enclosed-mass prediction at 100 to 300 kpc compared with halo-star or
satellite masses was found.

**Q5. Today's five lanes.**

- **NMB1** (line vs NIMBLE curves, passes, low power): not duplicated; no published MOND analysis of
  the DESI DR2 curves. No published number contradicts it. Indirect support only: DESI itself reads
  the Keplerian decline as an artefact (record's DR2REV), which removes the strongest published MOND
  objections (Chan and Law 2023, Coquery and Blanchard 2025, Wang et al. 2026 all rest on the
  decline at 17 to 27 kpc).
- **PLT1** (outer masses; record's field fails the satellite rows beyond 150 kpc): not duplicated.
  The mechanism (an external field truncating the phantom halo near 150 to 200 kpc for strong fields,
  much further out for 0.01 a0) is published (Wu et al. 2008; Oria et al. 2021). Its post hoc pointer
  (a weak field preferred) agrees in direction with Oria et al.'s "not under a strong EFE" and with
  0.01 a0 adoptions; whether it agrees in magnitude depends on the convention issue in Q3.
- **MWJ1** (all data pass at 1.26 to 1.31 x census baryons, 8.4 to 8.75e10): supported in substance
  by published MOND fits needing more than census baryons: Sylos Labini et al. 2023 (7.8e10 disc,
  bulge excluded); Coquery and Blanchard 2025 (about 1e11 stellar disc to fit the decline). The total
  is above Banik and Zhao's "about 7e10" and Oria et al.'s 7.5e10. The "census short by a quarter to a
  third in MOND" statement is in effect prior art; the joint window with DESI and outer data is new.
- **MWG1** (hot gas cannot supply the inner need; it lifts the outer masses): not duplicated. Partly
  supported: Thomas et al. 2017 find a massive corona helps outer (Sagittarius) dynamics in MOND.
  Partly in tension: Banik and Zhao 2018 prefer a corona of 2e10 or less from the escape-speed
  curve at 8 to 50 kpc; MWG1's Miller and Bregman case (3.1e10 within 200 kpc) is near that bound,
  Faerman 2017 (7.7e10) is above it. Different gates; no direct contradiction of MWG1's numbers.
- **MWI1** (needs 7.05 to 7.41e10 stars canonical, 6.36 to 6.73e10 alt): close to duplicated by
  Sylos Labini et al. 2023 (MOND disc 7.79 +/- 0.86e10 combined, 7.24 and 7.97 for other samples,
  without bulge, so their stellar total is higher still). Contradicted in direction by the
  RAR/MOND-based terminal-velocity analysis of McGaugh 2016 (stellar mass 5 to 6e10) and by Banik and
  Zhao's 7e10 including gas (about 5.8e10 stars if gas is 1.2e10). So the literature brackets MWI1:
  the lane's need sits between McGaugh's RAR inventory and Sylos Labini's free MOND fit.

## Sources

| ref | arXiv / URL | number(s) used | note |
|---|---|---|---|
| DESI Collab. 2026, Results III | https://arxiv.org/abs/2611.05518 | submitted 2026-11-03; abstract has no MOND | |
| Semantic Scholar record | https://api.semanticscholar.org/graph/v1/paper/arXiv:2611.05518?fields=title,citationCount,publicationDate | citationCount 0 | queried 2026-11-12 |
| arXiv API, MW mass listing | https://export.arxiv.org/api/query?search_query=abs:%22Milky%20Way%22%20AND%20(abs:mass%20OR%20abs:potential%20OR%20abs:%22rotation%20curve%22%20OR%20abs:gravity)&sortBy=submittedDate&sortOrder=descending&max_results=40 | 27 entries 2026-11-03 to 11-10, none MOND | |
| arXiv API, MOND listing | https://export.arxiv.org/api/query?search_query=abs:MOND%20OR%20abs:%22modified%20Newtonian%20dynamics%22%20OR%20abs:%22Milgromian%22&sortBy=submittedDate&sortOrder=descending&max_results=25 | Nov 2026: 2611.08702, 2611.03770 only | |
| Sylos Labini et al. 2023, ApJ 945, 3 | https://arxiv.org/abs/2302.01379 | MOND Md 7.79 +/- 0.5 stat +/- 0.7 syst e10 (DR3+), 7.24 (DR3), 7.97 (E19); Rd 3.1 kpc; simple nu; a0 1.2e-10; no EFE; bulge not fitted | read from PDF text, Table 5 |
| Banik and Zhao 2018, MNRAS 473, 419 | https://arxiv.org/abs/1708.03771 (HTML https://ar5iv.arxiv.org/html/1708.03771) | EF 0.01 to 0.03 a0 tested, ~0.03 a0 favoured; 0.015 a0 from LG 630 km/s; disc 5.51e10 stars + 1.18e10 gas, no bulge; "~7e10" MOND RC need; corona 2 to 8e10, ~2e10 preferred | |
| Famaey, Bruneton, Zhao 2007, MNRAS 377, L79 | https://arxiv.org/abs/astro-ph/0702275 | EF of order a0/100; v_esc 550 km/s | |
| Wu et al. 2008 | https://ar5iv.labs.arxiv.org/html/0803.0977 | EF 0.01 a0 (Sun to GC direction, Great Attractor, H0 x 600 km/s); 0.03 a0 upper limit; EF effective ~200 kpc at 0.03 a0; negative PDM ~600 / ~200 kpc; baryons Besancon ~7.0e10 | |
| Oria et al. 2021, ApJ | https://ar5iv.labs.arxiv.org/html/2109.10160 | MW baryons 7.5e10 (disc 6.37 incl 1.13 gas, bulge 0.7); PDM(r200) 1.39e12; curves split 150 to 200 kpc; "not under a strong EFE"; Virgo dominant | |
| Chae et al. 2020/21, ApJ | https://ar5iv.labs.arxiv.org/html/2009.11525 | e_env mean 0.033, range 0.02 to 0.05; fitted median 0.052 +/- 0.011 | no MW value |
| Haslbauer, Banik, Kroupa 2020 | https://ar5iv.arxiv.org/html/2009.11292 | 0.055 a0 field around the KBC void | not a MW-specific value (secondary) |
| Thomas et al. 2017, A&A 603, A65 | https://ar5iv.arxiv.org/html/1705.01552 | MW disc 3.52e10, bulge 0.518e10, ISM 1.69e10; corona M(<100 kpc) ~1.5e11, 2.6e11 total | |
| Jiao et al. 2023, A&A 678, A208 | https://arxiv.org/abs/2309.00048 | decline 19 to 26.5 kpc, flat rejected 3 sigma, Mtot 2.06e11 | no MOND in abstract |
| Ou et al. 2023 (2024 journal) | https://arxiv.org/abs/2303.12838 | Mvir 1.81e11, to ~30 kpc | |
| Coquery and Blanchard 2025, A&A 703, A88 | https://arxiv.org/abs/2407.18846 | stellar disc ~1e11; a0 < 0.53e-10 (95%) | nu and EF not in abstract |
| Chan and Law 2023, ApJ 957, 24 | https://arxiv.org/abs/2309.05252 | MOND "almost" ruled out >5 sigma at 17 to 23 kpc | |
| Wang et al. 2026 | https://arxiv.org/html/2605.10857 | MOND disfavoured >13 sigma; EFE worsens it; simple/standard/RAR nu | no total stellar mass quoted |
| Singh et al. 2026, Ap&SS | https://arxiv.org/abs/2605.16994 | MOND (3 nu) worse than cored halos | |
| Beordo et al. 2024, JCAP 12, 024 | https://arxiv.org/abs/2407.12482 | MOND ~ LambdaCDM to 19 kpc | |
| Moffat, Sharron, Toth 2024 (MOG) | https://arxiv.org/abs/2409.17371 | Mb ~ 1.3e11; residual as CGM | (secondary, via search and review) |
| Melchiorri and Ruchika 2026 review | https://arxiv.org/html/2608.10189 | EFE effect on decline "an open question"; Mbar 0.6 to 1.0e11 (Bland-Hawthorn and Gerhard 2016) | |
| McGaugh 2016, ApJ | https://arxiv.org/abs/1511.06387 | RAR-based stellar mass 5 to 6e10 | abstract |
| McGaugh 2018, RNAAS | https://arxiv.org/abs/1808.09435 | stellar mass 6.16 +/- 0.31e10 | whether built on the RAR unconfirmed |
| Koop et al. 2024 | https://arxiv.org/abs/2406.08872 | Helmi stream clumps dissolve ~100 Myr in MOND | listing gist only |
| Asencio et al. 2026 | https://arxiv.org/abs/2607.05502 | satellite tidal features fit MOND | listing gist only |

## Not found or not confirmed

- Any analysis of the DESI DR2 Milky Way mass papers under MOND or modified gravity, or any critique
  of their LambdaCDM-mock calibration (to 2026-11-10 on arXiv; INSPIRE and ADS citation lists not
  obtained).
- A published MOND prediction of M(<100 to 300 kpc) compared with halo-star or satellite masses.
- A MOND fit that uses a Milky Way-specific external field with a stated direction other than Wu et al.
  (Sun to Galactic centre) and Banik and Zhao (disc axis); none matches the record's (268.5, +33.0).
- The interpolating function and external-field treatment inside Coquery and Blanchard 2025 (abstract
  only read), the total stellar mass in Wang et al. 2026, and whether Chae et al. 2020's e is Newtonian.
- The external-field convention question in Q3 (literature 0.01 to 0.03 a0 as actual field versus the
  record's 0.01273 as Newtonian e_N) is flagged, not resolved; hunt h81's code was not read.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

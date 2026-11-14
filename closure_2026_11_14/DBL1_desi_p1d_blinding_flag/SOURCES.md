# DBL1 sources (all read 2026-11-14; nothing saved to disk)

Status words: **SEEN IN TEXT** = the words were returned verbatim from the fetched page or source file (quotes of a few
words below); **PROVISIONAL** = search snippet, a summary, or a negative that rests on a full-page search by the fetch
tool. Caveat for every line: the page-fetch tool passes the page through a small model before answering. Verbatim code
lines and short quotes were asked for and returned; where two independent fetches (rendered docs and raw source) gave
the same lines, that is said. The lead may wish to re-read the four key items (S1, S4, S5, S7) by hand.

## The paper

- **S1. Karaçaylı, Martini, Aguilar et al., "DESI DR1 Lyα 1D power spectrum: The optimal estimator measurement",
  arXiv:2505.07974** (v1 12 May 2025, v2 26 Aug 2025; abstract page and HTML v2, read in two parts covering the whole
  text).
  - SEEN IN TEXT: the only occurrence of any form of "blind" in the whole HTML text is in the Discussion opening: the
    study is called a "cosmologically blind measurement of P1D".
  - PROVISIONAL (paraphrase; the sentence was too long for the tool to quote whole): the reason given is timing; the
    study comes before the cosmological inference phase, so no analysis choice was steered by parameter inference.
  - PROVISIONAL (a negative from a full-text search by the fetch tool): the paper describes no blinding function,
    factor, hidden parameter or unblinding step applied to the P1D values.
  - SEEN IN TEXT, Data Availability: "All data points shown in the figures are available" at
    doi 10.5281/zenodo.16943723.
  - SEEN IN TEXT, amplitude against eBOSS: the DR1 power is "5−15% larger than the eBOSS measurements"; Figure 2
    caption: "in 15% tension with eBOSS results".
- **S2. Companion FFT paper, arXiv:2505.09493 (HTML v2, both parts).** SEEN IN TEXT: "blind" appears only as "a blind
  exploration of four data variations" and "blindly search for potential sources of analysis systematic error", that
  is, systematics tests; no value-level blinding or unblinding step is described. Its data-availability text says the
  figure data are released under DESI's data-management policy.

## The release

- **S3. Zenodo record 10.5281/zenodo.16943723** (v1, published 25 Aug 2025). SEEN IN TEXT: title equal to the paper's;
  "Supplementary material to DESI's publication"; one file `data_points.tar`, 131.6 MB,
  md5 `33d7fc21bfd3d745ed71a0bbe80ca433`, the same checksum as the archive on disk (FILE_FACTS.md). The page does not
  mention blinding, `P1D_BLIND` or `BLINDING` (PROVISIONAL negative).

## The code and the keyword

- **S4. QSOnic continuum fitter (github p-slash/qsonic), `py/qsonic/spectrum.py`, function `Spectrum.set_blinding`**,
  read twice, from the rendered source on qsonic.readthedocs.io and from the raw file on GitHub (master), with the same
  lines. SEEN IN TEXT:
  - the docstring: "Mock, side band and SV analyses are not blinded";
  - the label is set only from the latest observation date of the quasar catalogue: `elif maxlastnight < 20220801:` /
    `Spectrum._blinding = "desi_y1"` (other branches give "none", "desi_m2", "desi_y3", "desi_dr3");
  - its only effects: `Spectrum._fits_colnames[1] = 'DELTA_BLIND'` when the label is not "none", and
    `'BLINDING': Spectrum._blinding,` written as a header keyword.
  - PROVISIONAL (negative from the fetch tool's read of the whole file): no arithmetic on flux, inverse variance,
    continuum or delta depends on the label. The same check found no "blind" at all in `picca_continuum.py`, and in
    `io.py` and `scripts/qsonic_fit.py` only the guard that the label is set and the date look-up.
  - Limit: this is the current master branch, not necessarily the exact version used for DR1.
- **S5. The quadratic estimator (github p-slash/lyspeq).** SEEN IN TEXT in `io/qso_file.cpp`: the reader accepts the
  delta column under either name, `"DELTA"` or `"DELTA_BLIND"`, and reads it the same way. In
  `core/quadratic_estimate.cpp` the estimator names its own output extension `"P1D"` (with `_<iteration>` appended);
  no "blind" in that file, nor in `core/global_numbers.cpp` or `core/one_qso_estimate.cpp` (PROVISIONAL negatives).
  - NOT FOUND: the code that wrote the released file, with its `P1D_BLIND` extension name, its `BLINDING` keyword and
    its `PSMOOTH`, `E_SYST` and `SYSTEMATICS` content. It is neither lyspeq's writer nor picca's
    `pk1d/postproc_pk1d.py` (that file has no "blind" and sets no extension name; PROVISIONAL negative). The
    collaboration's script repository `p-slash/desi-y1-p1d` was listed (file tree only) and holds no obvious writer.
    GitHub code search needs a login and was not used.
- **S6. DESI DR1 Lyman-alpha deltas catalogue page, data.desi.lbl.gov/doc/releases/dr1/vac/lya-deltas/.** SEEN IN TEXT:
  the per-forest header row "BLINDING | none | char[12] | Blinding scheme used" and the extension "EXTNAME =
  DELTA_BLIND". The page does not say what blinding does to the values. So the public DR1 deltas carry the
  `DELTA_BLIND` name while the documented keyword value is "none": the "BLIND" name persists as a label.
- **S7. DESI 2024 IV, Lyman-alpha BAO from DR1, arXiv:2404.03001 (HTML v3, all three parts).** SEEN IN TEXT, Section
  6.1: the team chose "blinding the measured correlation functions"; it "applied an additive correction to the
  measured correlation functions"; Appendix C: the method "only shifts the position of the BAO peak at the level of the
  measured correlation functions", and picca "automatically applied this template to any calculation of the
  correlation function". PROVISIONAL: the appendix does not state in so many words that deltas were left unchanged.
- **S8. DR1 Lyman-alpha correlations catalogue page** (search snippet only): the `BLINDING` field is described as the
  string "specifying the blinding strategy (desi-y1)". PROVISIONAL.
- **S9. Perez-Sanchez et al., "Alcock-Paczynski Blinding Scheme for the Ly-α Forest Analysis", arXiv:2607.07875**
  (abstract page). PROVISIONAL (summary): a later, catalogue-level scheme (a wavelength shift of each forest), tested on
  DR1 among others; it is not the scheme of the DR1 BAO analysis or of the DR1 P1D paper, and its abstract does not
  mention P1D. Listed because it shows that "blinded Y1 catalogues" exist in later work.

## Item 3: numerical check against a published number

Not done. The paper text read here gives the eBOSS comparison only as a range (5 to 15 per cent) and gives no single
power value at a stated z and k. The eBOSS table is not on disk and downloads are not allowed, so the table's amplitude
could not be set against an external published number. The figure-data check in FILE_FACTS.md (Figure 8, exact
to 3e-17) ties the table to the published figure but cannot test a common factor.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.

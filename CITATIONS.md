# Citations

Everyone whose published work — equations, models, methods, data or software — is used by the Python scripts in
this repository, tied to the exact, verified reference and to every script and line that uses it.

**21,118 people** · **3,175 works** · credited in **7,607 scripts** (of
8,141 scanned) and **85 LaTeX paper files** · built 2026-09-28 from commit `c10a155aaf`

| | |
|---|---|
| [People A–Z](citations/people/README.md) | everyone credited — 6,851 with their own page, 14,267 as authors of large collaboration papers |
| [Works](citations/WORKS.md) | every verified reference, most-used first; each work's page lists every script and line |
| [REFERENCES.bib](citations/REFERENCES.bib) | BibTeX for all 3,175 works |
| [By folder](citations/BY_FOLDER.md) | which works each top-level folder uses |
| [Could not verify](citations/UNVERIFIED.md) | 75 broken identifiers, 59 script citations that match no publication, 13 ambiguous ones, 87 unmatched paper-bibliography entries |
| [Corrections](citations/CORRECTIONS.md) | what happened to each of the previous index's 182 names |
| [How it is built](citations/README.md) | scope, evidence, verification, and the one command that rebuilds and checks it |

## How a person gets credited

A script credits a work when it

1. **cites** it — an author–year reference, arXiv id, DOI or ADS bibcode in a comment, docstring or string;
2. **names** its equation, method or model — "Tully–Fisher", "NFW", "Gibbons–Hawking temperature", "AQUAL", "Nelder–Mead";
3. **uses its data** — SPARC, Planck 2018, DESI DR2, Gaia DR3, Pantheon+, eRASS1, CODATA, PDG …;
4. **imports its software** — NumPy, SciPy, SymPy, mpmath, Astropy, CLASS, CAMB …; or
5. **calls a routine that implements its algorithm** — `solve_ivp` (Dormand & Prince 1980), `brentq` (Brent 1973),
   `quad` (QUADPACK), `spearmanr` (Spearman 1904) …;

and the repository's LaTeX papers credit every work in their bibliographies (matched entry by entry).

Every work is checked against its publisher (Crossref / DataCite), arXiv or INSPIRE-HEP record before anyone is
credited; the people credited are that record's authors. References that cannot be verified are never credited —
they are listed in [Could not verify](citations/UNVERIFIED.md) with the script and line, because some of this
repository's scripts were machine-written and a few of their references are garbled or invented.

## Most-used works

| # | work | scripts |
|---:|---|---:|
| 1 | [Harris et al. 2020](citations/works/harris-2020-array-programming-with-numpy.md) — Array programming with NumPy | 5,148 |
| 2 | [Milgrom 1983](citations/works/milgrom-1983-a-modification-of-the-newtonian-dynamics-as-a-po.md) — A modification of the Newtonian dynamics as a possible alternative to the hidden mass hypo | 3,502 |
| 3 | [Milgrom 1983](citations/works/milgrom-1983-a-modification-of-the-newtonian-dynamics-impli.md) — A modification of the Newtonian dynamics - Implications for galaxies | 3,273 |
| 4 | [Milgrom 1983](citations/works/milgrom-1983-a-modification-of-the-newtonian-dynamics-impli-2.md) — A Modification of the Newtonian Dynamics - Implications for Galaxy Systems | 3,273 |
| 5 | [Meurer et al. 2017](citations/works/meurer-2017-sympy-symbolic-computing-in-python.md) — SymPy: symbolic computing in Python | 2,776 |
| 6 | [Newton 1687](citations/works/newton-1687-philosophiae-naturalis-principia-mathematica.md) — Philosophiae Naturalis Principia Mathematica | 1,845 |
| 7 | [Virtanen et al. 2020](citations/works/virtanen-2020-scipy-1-0-fundamental-algorithms-for-scientific.md) — SciPy 1.0: fundamental algorithms for scientific computing in Python | 1,774 |
| 8 | [McGaugh, Lelli & Schombert 2016](citations/works/mcgaugh-2016-radial-acceleration-relation-in-rotationally-sup.md) — Radial Acceleration Relation in Rotationally Supported Galaxies | 1,396 |
| 9 | [Lelli et al. 2017](citations/works/lelli-2017-one-law-to-rule-them-all-the-radial-acceleratio.md) — One Law to Rule Them All: The Radial Acceleration Relation of Galaxies | 1,353 |
| 10 | [Bekenstein & Milgrom 1984](citations/works/bekenstein-1984-does-the-missing-mass-problem-signal-the-breakdo.md) — Does the missing mass problem signal the breakdown of Newtonian gravity? | 1,234 |
| 11 | [Blumenthal et al. 1984](citations/works/blumenthal-1984-formation-of-galaxies-and-large-scale-structure.md) — Formation of galaxies and large-scale structure with cold dark matter | 1,217 |
| 12 | [Peebles 1982](citations/works/peebles-1982-large-scale-background-temperature-and-mass-fluc.md) — Large-scale background temperature and mass fluctuations due to scale-invariant primeval p | 1,217 |
| 13 | [Gauss 1809](citations/works/gauss-1809-theoria-motus-corporum-coelestium-in-sectionibus.md) — Theoria motus corporum coelestium in sectionibus conicis solem ambientium | 1,051 |
| 14 | [Lelli, McGaugh & Schombert 2016](citations/works/lelli-2016-sparc-mass-models-for-175-disk-galaxies-with-sp.md) — SPARC: MASS MODELS FOR 175 DISK GALAXIES WITH SPITZER PHOTOMETRY AND ACCURATE ROTATION CUR | 1,034 |
| 15 | [Friedmann 1922](citations/works/friedmann-1922-uber-die-krummung-des-raumes.md) — Über die Krümmung des Raumes | 896 |
| 16 | [Friedmann 1924](citations/works/friedmann-1924-uber-die-moglichkeit-einer-welt-mit-konstanter-n.md) — Über die Möglichkeit einer Welt mit konstanter negativer Krümmung des Raumes | 896 |
| 17 | [O'Neill 2014](citations/works/oneill-2014-pcg-a-family-of-simple-fast-space-efficient-sta.md) — PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Numb | 789 |
| 18 | [de Sitter 1917](citations/works/de-sitter-1917-on-einsteins-theory-of-gravitation-and-its-astr.md) — On Einstein's Theory of Gravitation and its Astronomical Consequences. Third Paper. | 788 |
| 19 | [Skordis & Złośnik 2021](citations/works/skordis-2021-new-relativistic-theory-for-modified-newtonian-d.md) — New Relativistic Theory for Modified Newtonian Dynamics | 744 |
| 20 | [Johansson & The mpmath development team 2023](citations/works/johansson-2023-mpmath-a-python-library-for-arbitrary-precision.md) — mpmath: a Python library for arbitrary-precision floating-point arithmetic | 714 |
| 21 | [Anderson et al. 1999](citations/works/anderson-1999-lapack-users-guide.md) — LAPACK Users' Guide | 697 |
| 22 | [McGaugh et al. 2000](citations/works/mcgaugh-2000-the-baryonic-tully-fisher-relation.md) — The Baryonic Tully-Fisher Relation | 675 |
| 23 | [Davies 1975](citations/works/davies-1975-scalar-production-in-schwarzschild-and-rindler-m.md) — Scalar production in Schwarzschild and Rindler metrics | 656 |
| 24 | [Fulling 1973](citations/works/fulling-1973-nonuniqueness-of-canonical-field-quantization-in.md) — Nonuniqueness of Canonical Field Quantization in Riemannian Space-Time | 656 |
| 25 | [Unruh 1976](citations/works/unruh-1976-notes-on-black-hole-evaporation.md) — Notes on black-hole evaporation | 656 |

[All 3,175 works →](citations/WORKS.md)

## Most-credited people for the research itself

Counted over the files that cite their work, name their method or use their data (software and numerical-method
credits excluded; authors of large collaboration papers are listed A–Z instead).

| person | files | works |
|---|---:|---:|
| [Mordehai Milgrom](citations/people/milgrom-mordehai.md) | 3,688 | 48 |
| [Stacy S. McGaugh](citations/people/mcgaugh-stacy-s.md) | 2,060 | 47 |
| [James M. Schombert](citations/people/schombert-james-m.md) | 2,030 | 23 |
| [Isaac Newton](citations/people/newton-isaac.md) | 1,859 | 5 |
| [Federico Lelli](citations/people/lelli-federico.md) | 1,812 | 31 |
| [Jacob D. Bekenstein](citations/people/bekenstein-jacob-d.md) | 1,492 | 12 |
| [Marcel S. Pawlowski](citations/people/pawlowski-marcel-s.md) | 1,361 | 9 |
| [Sandra M. Faber](citations/people/faber-sandra-m.md) | 1,235 | 5 |
| [P. J. E. Peebles](citations/people/peebles-p-j-e.md) | 1,219 | 3 |
| [Joel R. Primack](citations/people/primack-joel-r.md) | 1,219 | 4 |
| [George R. Blumenthal](citations/people/blumenthal-george-r.md) | 1,217 | 2 |
| [Martin J. Rees](citations/people/rees-martin-j.md) | 1,217 | 1 |
| [Martin J. White](citations/people/white-martin-j.md) | 947 | 20 |
| [A. Friedmann](citations/people/friedmann-a.md) | 896 | 2 |
| [Simon D. M. White](citations/people/white-simon-d-m.md) | 869 | 19 |
| [Carlos S. Frenk](citations/people/frenk-carlos-s.md) | 833 | 27 |
| [W. de Sitter](citations/people/de-sitter-w.md) | 788 | 1 |
| [Constantinos Skordis](citations/people/skordis-constantinos.md) | 758 | 14 |
| [Tom Złośnik](citations/people/zlosnik-tom.md) | 746 | 8 |
| [R. A. Sunyaev](citations/people/sunyaev-r-a.md) | 725 | 11 |
| [W. J. G. de Blok](citations/people/de-blok-w-j-g.md) | 721 | 11 |
| [Hiranya V. Peiris](citations/people/peiris-hiranya-v.md) | 719 | 8 |
| [David H. Weinberg](citations/people/weinberg-david-h.md) | 713 | 24 |
| [Xiaohui Fan](citations/people/fan-xiaohui.md) | 701 | 35 |
| [Carl Friedrich Gauss](citations/people/gauss-carl-friedrich.md) | 699 | 4 |
| [Benjamin Alan Weaver](citations/people/weaver-benjamin-alan.md) | 698 | 44 |
| [Ofer Lahav](citations/people/lahav-ofer.md) | 688 | 45 |
| [Massimiliano Lattanzi](citations/people/lattanzi-massimiliano.md) | 680 | 15 |
| [G. D. Bothun](citations/people/bothun-g-d.md) | 675 | 1 |
| [P. C. W. Davies](citations/people/davies-p-c-w.md) | 675 | 3 |
| [Stephen A. Fulling](citations/people/fulling-stephen-a.md) | 656 | 1 |
| [W. G. Unruh](citations/people/unruh-w-g.md) | 656 | 1 |
| [Licia Verde](citations/people/verde-licia.md) | 638 | 13 |
| [Sergey E. Koposov](citations/people/koposov-sergey-e.md) | 634 | 31 |
| [John A Peacock](citations/people/peacock-john-a.md) | 611 | 11 |
| [Daniel J. Eisenstein](citations/people/eisenstein-daniel-j.md) | 589 | 31 |
| [Alexandra Walker](citations/people/walker-alexandra.md) | 581 | 3 |
| [Robert N. Cahn](citations/people/cahn-robert-n.md) | 580 | 5 |
| [Uros Seljak](citations/people/seljak-uros.md) | 579 | 7 |
| [Georges Lemaître](citations/people/lemaitre-georges.md) | 578 | 1 |

Software and numerical methods are credited too — most widely: [Ralf Gommers](citations/people/gommers-ralf.md) (5,185), [David Cournapeau](citations/people/cournapeau-david.md) (5,183), [Matthew Brett](citations/people/brett-matthew.md) (5,181), [Charles R. Harris](citations/people/harris-charles-r.md) (5,181), [Robert Kern](citations/people/kern-robert.md) (5,181), [K. Jarrod Millman](citations/people/millman-k-jarrod.md) (5,181), [Travis E. Oliphant](citations/people/oliphant-travis-e.md) (5,181), [Tyler Reddy](citations/people/reddy-tyler.md) (5,181), [Nathaniel J. Smith](citations/people/smith-nathaniel-j.md) (5,181), [Stéfan J. van der Walt](citations/people/van-der-walt-stefan-j.md) (5,181) …

[All 21,118 people →](citations/people/README.md)

# Local source-diagram attribution correction

Date 2026-10-19. Independent source check; frozen author files preserved unchanged.

The statement audited is in sea_lattice/DERIVATION.md, subsection “Which sea contraction was actually seen”: it identifies the second upper drawing in Wang Figure S3 as the product of the two-current vacuum loop and nucleon correlator that is subtracted. The Wang entry of sea_lattice/SOURCE_RECEIPTS.json records visual inspection of these drawings, but supplies no source statement identifying the second drawing with the subtraction.

**Verdict: incomplete, with the smallest missing implication.** Figure S3 does not identify its second drawing as the vacuum-subtraction term. In the primary figure, both drawings have the same two-current closed quark loop, accompanied by different nucleon Wick contractions: the first has uncrossed nucleon propagators and the second has crossed propagators. Its caption calls them two disconnected diagrams computed in the work. A quark-line drawing alone does not identify ensemble factorization or a subtraction.

The vacuum subtraction and surviving ensemble covariance are independently supported by the paragraph immediately following source equation (11), and the supplement's “Contributions from disconnected diagrams” text explicitly says the subtraction is performed. Therefore the correct source statement is:

> Both upper drawings in Figure S3 are same-loop two-current disconnected contractions with different nucleon contractions. The vacuum subtraction is established by the accompanying source text; the second image is not its identifying label.

This correction changes no Table II value, finite-window qualifier, normalization, alpha_ref stripping or raw-Fu slope conversion. It does not make the reported included contractions complete in physical flavor space. No image needs to be used as a positivity statement.

Audited source: X.-H. Wang et al., [arXiv:2310.01168v3](https://arxiv.org/abs/2310.01168v3), 30 August 2024, Figure S3 on supplemental page S4 (PDF page11), visually checked in the retained versioned PDF. The paragraph after equation (11) and the supplement text were checked in its TeX/extracted text.

| Artifact | SHA-256 |
|---|---|
| /private/tmp/fsp007_sea_sources/2310.01168v3.pdf | c216213c240e2a2b01457874a3e0e0f49fc6319623501358923d41ac3a61de4e |
| /private/tmp/fsp007_sea_sources/2310.01168v3/paper.tex | c720c612c117fcb9b2fb45261ef9563d9066fb1cf0179b766f5ec5c7344b292b |
| /private/tmp/fsp007_sea_sources/2310.01168v3/gram_disc1.pdf | 8910f8685dc09e76746cd87ca08b06362e17b137ab3c3a6b87f7bdf712a4c08b |
| /private/tmp/fsp007_sea_sources/2310.01168v3/gram_disc2.pdf | 94a6ec19f6bbfab96e100829520f63cb9080f405f9d52db6cc6cb65f8dcd6701 |
| sea_lattice/DERIVATION.md | a464a9946027f5f1f0c5d16aa4022daf3c368655c1809b44fc6eebf0db26c277 |
| sea_lattice/REPORT.md | 17f530b5460d4603c384c4b3cec2a8ddcc2292b8e650530a56fe547d08c745f7 |
| sea_lattice/SOURCE_RECEIPTS.json | 027f9b288b22946206c7f0346be1ae0e9ae363b8e357be5d94339710b4178f3e |

This note is the review correction. It is not an amendment of the frozen author artifacts.

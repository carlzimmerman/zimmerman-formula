# Primary-source checks after target exposure

The pretarget SOURCE_CHECK.md remains unchanged. After reading the frozen
packets, exact-version cache lookups found their three retained primary
sources. PDFs and extracted texts were read from the ignored cache; no files
were added there. All six SHA-256 values were independently recomputed and
equal the author SOURCE_RECEIPTS.json values.

| Exact source | PDF SHA-256 | Extracted text SHA-256 | Application checked |
|---|---|---|---|
| [Jersak, Lang, Neuhaus, hep-lat/9606013v1](https://arxiv.org/abs/hep-lat/9606013v1) | de457bfac32320b4507e474b7faa8eecf75cd43a338b25889e94915d99041363 | b7625b1601ab0debd1ae11b61b0df5bb1b5c6ba9320fe3f5b739283b11e660dd | Section 2 pp.7-9 distinguishes unprojected SH[N] from projected weighted S[N]; Appendix p.35 gives all five counts with n=N-1. Verified connectivity/count translation. U(1) simulation results do not transfer. |
| [Langelage, Muenster, Philipsen, 0710.0512v2](https://arxiv.org/abs/0710.0512v2) | 7d2d5c1a246f31a91fd07161262ed3ed8a457223144bf22e59bed0f70db05583 | 45f295ee16da553cab2dab797d26e1db557d383c616d3d2ec1e7c0afd2e8d5ce | Equations (2.1)-(2.4),(2.8): Wilson normalization, c0, closed polymer convention, leading beta/18. Equation (2.3) subtracts the vacuum part; target retains it. Its Wilson constant offset is separately accounted for. Verified restricted convention match. |
| [Wakabayashi et al., 2112.06340v2](https://arxiv.org/abs/2112.06340v2) | 87f093390a5d2e84748a992523191196f0ecb1d8558dd96085004391b0b9c275 | c97331f35967e600d60724ae0040b88bdc59f8e0a3bed84a35b4b06dedd7cd8f | Equations (4)-(8) give M=1-kappa B, det M(0)=1 and -Tr B^l/l. Verified algebraic convention. The source's flat Wilson spin trace supplies no curved K_n spin transport. |

Title/authors/version banners in all three cached documents were read. Official
arXiv exact-version metadata was independently opened for 9606013v1 and
2112.06340v2. The 0710.0512v2 metadata request returned a web cache miss; its
cached primary-document title/authors/v2 banner (4 October 2007) and matching
binary/text hashes were available. No unseen source theorem is credited.

The Jersak PDF has a later compilation date in the title block while retaining
the exact arXiv v1 banner. The version is identified by that banner and the
authenticated identifier, not by interpreting the compilation date as a new
submission. No new novelty or source-absence search was made here.

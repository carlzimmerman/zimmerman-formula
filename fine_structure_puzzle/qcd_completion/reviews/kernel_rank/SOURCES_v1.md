# Exact source checks for the kernel/rank audit

Checked 2026-10-18, America/New_York. Full downloaded text stays in `/private/tmp`; no full source is copied into this tracked review. The project-local cache had no exact identifier hit when queried. Source identity alone is not theorem verification.

| Primary source | Exact version | PDF SHA-256 | Text SHA-256 |
|---|---|---|---|
| [Moore, Royston, Van den Bleeken, Parameter counting for singular monopoles on R3](https://arxiv.org/abs/1404.5616v2) | v2, 2016-01-09 | `0ef1ef96b5d9a16bd793c6585f94221222dcf412d51d3e6888f5c0804f8d3ed7` | `9f36550b07678708313deeb2f7e6c1c6a482d1372847d3e6a01e13f2ce5935be` |
| [Kottke, Dimension of monopoles on asymptotically conic 3-manifolds](https://arxiv.org/abs/1310.2974v3) | v3, 2014-10-03; BLMS 47 (2015), 818–834, DOI 10.1112/blms/bdv055 | `98a2652cb0d41cf8e94d7783a88680bc72609762c5e765ae2f2bd1818a22f68b` | `0fb674a911bb4f06d1fc468b6a909560cb0d254a653ced4d97142a7912eae9b7` |
| [Kottke, A Callias-type index theorem with degenerate potentials](https://arxiv.org/abs/1210.3275v5) | v5, 2014-10-03; CPDE 40 (2015), 219–264, DOI 10.1080/03605302.2014.942740 | `da0fae7d829108bc00ace4cfea2d66661edb5e84c3d576088386ef4d8deef6b5` | `43abdd44beabdf550e67d48b13c1502c841380e09e21415300eb8237ea23d6b4` |

## Extracted implications

MRV: pages 16–21, equations (2.19), (2.27), (2.32)–(2.35); pages 30–31, equation (3.49). Their gauge group tends to the identity. Setting the defect set empty, regular SU2 Higgs and magnetic co-root with root pairing two gives complex Weyl kernel count two and real bosonic count four. The partner vanishing argument is explicit. Their neutral continuum treatment invokes Weinberg's asymptotic analysis; the Taubes discussion is an attribution, not an independently checked Taubes theorem here. Thus this paper corroborates the count but is not the sole rigorous-domain leaf used.

Kottke monopoles: Theorem 1.1 and Theorem 4.7 (pages 2 and 16–17), equations (2.8)–(2.16) (pages 6–9). For positive fixed mass, smooth SU2 Bogomolny data on radially compactified Euclidean space, framed weighted index is four times charge; the unframed index is one smaller. The weighted gauge adjoint needs the target isometry and correct commutator prefactor derived in RAW_DERIVATION_v1.md. No claim is made that the printed (2.15) expansion alone equals the project's Coulomb operator.

Kottke general theorem: Definition 2.3 and Theorem 2.4 (pages 16–17), Theorem 3.6 (page 26). The hybrid neutral domain uses b-derivatives; the massive domain uses scattering derivatives. Its Fredholm and nullspace asymptotics results include Sobolev order zero. This fixes the precise domain underlying the index application.

Authentication: versioned arXiv landing pages and downloaded PDF stamps agree. Kottke PDFs/HTML contain compilation-date fields different from the submission date, so the arXiv version and content hash are the identity, not the generated date field. `pdftotext -layout` succeeded for all three PDFs. Mathematical extraction and the smooth no-defect application were checked directly in the exact text. The source-to-Hessian and source-to-rank implications are internal arguments recorded separately.

Weinberg, Phys. Rev. D20 (1979) 936, remains metadata-only in this review. Its publisher text was unavailable to the coordinator; no theorem has been authenticated from that original paper. Taubes, CMP91 (1983) 235–263, DOI 10.1007/BF01211160, was located only as a publisher subscription preview here and is not used as a verified theorem.

No novelty claim is made. The literature scope was exact theorem/domain verification, using arXiv, the source bibliographies, and publisher metadata.

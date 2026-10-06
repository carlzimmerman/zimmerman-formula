# Source and provenance contract

Primary versions and equation locators are recorded in sources.json. Both PDF pages were opened with the web tool on 2026-10-06; Flanagan exact v3 was reopened explicitly. This is a bounded two-paper authentication, not a novelty search. Original PDF bytes were not downloaded: original_pdf_sha256 is deliberately null. Reproducing source authentication requires reopening those exact URLs, not treating metadata as a cached full source.

provenance.json records the actual inspected HEAD and hashes of the two scientific parent reports read during derivation. Parent inputs remain unchanged. The scientific script uses Python3.9.6/SymPy1.14.0, with the bounded outer runner using Python3.13. Runner manifests hash executed files, contract, raw outputs and logs. The report equations supply general-n proofs; the finite ADM symbolic check uses three spatial dimensions.

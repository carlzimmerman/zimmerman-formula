# AX1 / khronon (Blanchet–Marsat): FAIL [G2a] on both footings. The AQUAL static limit gives the same Q2 as AeST: law 2.44–5.15× Hees; β ≥ 2.5 fail E0 at 1.01–1.12× canonical, 1.42–1.47× alt. The preferred-frame question (G2c) stays open and isn't needed for the fail

Criteria `FROZEN_CRITERIA.md` (alone, before this run) + `../common/FROZEN_CRITERIA.md` (fd417eea04). Engine `../common/ax1_engine.py`. Outputs `ax1_khronon.{json,out}`, byte-identical rerun (SHA-256 ed81043e…), twin `ax1_khronon_MUTATE.*` (K1, K2 fail, all QUMOND Q2 = 0, exit 1). Seconds, one thread. **Not blind**; the by-hand expectation came true. κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. The cold sector stays retired. CMB and clusters out of scope, open.

## Result
- Static numbers are identical to `../AeST/README.md`: same AQUAL limit (E2), same candidates. The law fails G2a (2.44–4.55× canonical, 2.85–5.15× alt) and G2b (1.34e4 / 1.62e4×). The turn-off clears G2b but not G2a. Every β member passes G1 and G2b but fails E0.
- G2c O: the record has two branches that disagree (X15's static α1 = −8 against A22's moving-source α1 = α2 = 0), and the literature says only that α1, α2 are the non-GR parameters [PROVISIONAL].
- G3 P [PROVISIONAL]. G4 O: c_T = c needs β_kh = 0 [PROVISIONAL]; health is conditional (C5) and the literal form has saddle growth (H4). G5: a0 by hand.
- **Label: FAIL [G2a for every candidate; G2b for the law] on both footings.**

## Reading
Khronon and AeST share the AQUAL Q2 wall. The record got past that wall only with the stiffness length L★, which is v3s (`../v3s/`).

# T8 — full-corpus fingerprint sweep (all 722 manuscripts, full text)

Closes the honest coverage gap of the campaign: the triage scored all 372
families from abstracts only; full-text reads covered the ~40 score-1+
families. This lane fingerprints **every one of the 722 manuscripts** in
`preprints/` — full TeX (4 MB cap) with pdftotext fallback — for
framework-shaped signatures. Family numbers are not in the dir names, so
9 anchor families (374/360/377/267/269/270/215/221/263) are resolved by
title words (C3c: all found and scanned). Text cache lives in TMPDIR
(untracked, reproducible); scripts and outputs are committed.

Main run: **6/6 PASS, rc 0** (722/722 scanned). MUTATE (decoy fingerprints
33π / 0.0988 / 5.44): **7/7 PASS, rc 0**, F2/F3/F7/F8 hit counts strictly
decrease 10→0, 1→0, 1→0, 6→4 — the declared flip, verified by C4.

## Results

| fingerprint | hits | triage |
|---|---|---|
| F1 kernel 1/(1−e^{−√y}) | **0** | the record kernel appears NOWHERE in the corpus (no Bose-occupancy-at-√y form anywhere) |
| F2 32π | 10 | all incidental theorem coefficients. Physics contacts: (a) Kerr–Newman–Penrose `A ≥ 64π > 32π/15 ≥ 8π|J|` — the only 32π in a gravity manuscript, a geometric-inequality coefficient with no Λ and no acceleration scale (Q1 fail); (b) XY-model critical log-correction `(c_{N+1}−c_N)/(32πℓN)` — denominator of a spin-wave correction (Q1 fail); (c) 8 more: circle-packing bound 32π/3, honeycomb half-period 32π, Penrose-equality area sums 32πm², family-263 outer-electron radius 32π/3·q_ℓ^{−5} (that family's own normalization), planar-XY, etc. |
| F3 √(32π) | 1 | `λ_p(𝓔_{z,R}) ≤ (√(32πe)·R)^p`, Gaussian-regression ellipsoid eigenvalue bound (information theory; the 32π is a sphere-volume constant; √e factor; Q1 fail, no Λ/G/a₀) |
| F4 3-Laplacian with source | **0** | P5 confirmed empty at FULL-TEXT level (agrees with T5's manuscript-level read; nothing beyond the abstract sweep) |
| F5 Gρ_Λ / √(Gρ_Λ) | **0** | the law's raw ingredient appears nowhere |
| F6 a₀ = c√(Gρ_Λ) spellings | **0** | no manuscript writes the law or any c√(Gρ) form |
| F7 0.0997… | 1 | **junk**: the arXiv ID `1610.09970v2` in a bibliography of the entropy-photon-number paper |
| F8 5.36 | 6 | **all junk**: pgfmath atan tables (25.36095), TikZ figure grid (0,5.36,10.72), DOI `10.1515/crll.1985.363.1`, equation cross-reference `Equation~(5.36)`, Laughlin-paper pgfmath table — no physics constant 5.36 anywhere |
| F9 tanh ∧ (a₀/g_N-scale word) | 60 | switch vocabulary only: tanh in pure-math kernels (mixing times, cosh-log Ising free energy, etc.); no tanh(g/g_N) MOND-style interpolant in any manuscript (P6 stays vocabulary-only at full-text level) |
| F10 Bose/Planck occupancy 1/(1−e^{−x}), 1/(e^x−1), frac forms | 122 | ubiquitous as expected (C3b). The kernel ν(y) = 1/(1−e^{−√y}) is the Bose occupation at x = √y; the corpus has 122 plain occupancies, **zero** with the √y argument |

## Honest bottom line

The full-text sweep confirms the abstract triage **mechanism-level**: the
release contains no manuscript that writes the framework's kernel, its field
equation, its law's ingredients (Gρ_Λ), the required amount 5.36, the
switch, or the constant T. The only literal 32π in a gravity paper is the
Kerr–Newman–Penrose bound coefficient 32π/15 — a pure geometric-inequality
constant (no Λ; screen Q1 fails), and 1/√(32π) appears exactly once, inside
an information-theory bound with an extra √e. Nothing FORCES 4, 32π, 5.36 or
κ. The "did you read all 700+?" question now has a definitive answer: yes,
every manuscript's full text has been fingerprinted, and the triage's
zero-scores hold.

Follow-up: none from this sweep. The fingerprint set is reusable as a
per-release gate: any future openai/math batch can be swept with the same
script in minutes.
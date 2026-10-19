# Frozen-source locator correction

Date: 2026-10-19. This note corrects citations only. The completed author
DERIVATION.md, REPORT.md, SOURCES.json and their delivery hashes are preserved.

Exact primary source: H. Makino and H. Suzuki, *Lattice energy-momentum tensor
from the Yang-Mills gradient flow—inclusion of fermion fields*,
[arXiv:1403.4772v5](https://arxiv.org/abs/1403.4772v5), 2015-06-17.

The inspected existing PDF is
`/private/tmp/fsp006-vacuum-sources/makino14034772v5.pdf`, SHA256
`decefa1e7bf7e32a1ad77b55bdbbfb59a788b4e5cbd1e7196da5db8d2a92fcf6`.
Its existing extracted text has SHA256
`2669bab7423a53f4d0dbbe9bb0eda456dfc9fe668e077cbba6fd97d35a81c461`.
Both match the frozen SOURCES.json receipts. The v5 banner and relevant exact
text were inspected; no source refetch or new all-page review is claimed.

| Frozen locator/description | Exact locator in v5 | Result |
|---|---|---|
| DERIVATION.md line 57: master formula `(4.73)` | Section 4.4, `(4.70)`, printed page 23; also identified explicitly in Section 1 | `(4.73)` is the coefficient `c2(t)`, not the EMT master formula. Replace only the master-formula locator with `(4.70)`. |
| REPORT.md line 33: equations `(2.11),(4.73)` support vacuum-subtracted EMT | Definition `(2.10)`, trace anomaly `(2.11)` and its following vacuum-subtraction convention, master formula `(4.70)` | The substantive restriction is supported. The clean precise reference is `(2.10),(2.11),(4.70)` plus Section 1. |
| SOURCES.json exact_locators: `(2.11),(2.12),(4.71),(4.73); Section 4.3` | Section 1; `(2.10),(2.11)`; Section 4.4 `(4.70)`; `(4.68)` and its following qualification; Section 5 `(5.6)` and its surrounding text | `(2.12)` defines the beta function; `(4.71)` is a flowed-operator expectation identity; `(4.73)` gives `c2(t)`. These are real equations but do not replace the missing master-formula locator. |

Section 1 explicitly limits the master formula to EMT insertions separated
from other operators and requires the continuum limit before the small
flow-time limit. The discussion following `(4.68)` permits the equation of
motion only with no other operator at that point. Section 5 repeats the
noncoincidence condition for the simplification `(5.6)`. Thus the report's
physical conclusion survives: the flat vacuum-subtracted separated-insertion
formula does not by itself evaluate an integrated curved-space `Tqq` or
`TqqJJ` response or supply its contact prescription.

Frozen author files implicated:

- DERIVATION.md SHA256 `592a7fb94b58f7fac6541447e3d1bc83dff598c535155f698acb4e97ff45132a`.
- REPORT.md SHA256 `c5066b8a86a4c0b6e0cae3c60c32a719e426479b8221e8c72537bdb2b7c04f49`.
- SOURCES.json SHA256 `626d5c9fb8639f3217c51e6cc48fcebc3c871dd5d7789075c64760d16e7cffec`.

This note supplies an audit correction alongside those artifacts; it neither
rewrites their receipts nor changes their physical or computational evidence.

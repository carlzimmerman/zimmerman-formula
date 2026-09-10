# Targeted source record

Checked 2026-09-10. This is a parameterization and notation check, not a novelty
survey. The repository literature-cache lookup returned no cache. Searches of
project-local filenames and DHOST reports found earlier project calculations,
including `dhost_terminal/exceptional_branch.py`, but no authenticated primary
copy for the selected result. Two version-pinned public arXiv PDFs were then
retained in this directory's ignored local `.research-cache/`. Both extracted
successfully with `pdftotext -layout`; cache verification passed.

## Langlois, Saito, Yamauchi, Noui

“Scalar-tensor theories and modified gravity in the wake of GW170817,”
arXiv:1711.07403v2, revised 2018-11-01, Phys. Rev. D 97, 061501.
[Primary PDF](https://arxiv.org/pdf/1711.07403v2),
[readable equations](https://arxiv.org/html/1711.07403v2).

PDF SHA-256: `03fca70ae81e34ee3cc989f5ae5e5f02ae0ff585516967e2e4914098bf4a0703`.
Equations (1)-(2) define the quadratic operators with source variable
\(Y=g^{\mu\nu}\phi_\mu\phi_\nu\). Equations (5)-(8) state the luminal
degenerate class: \(A_1=A_2=0\), with \(A_4,A_5\) fixed by \(F,A_3\).
Setting \(A_3=0\) gives \(A_4=6F_Y^2/F\), \(A_5=0\).
The project variable is \(X=-Y/2\); therefore \(F_Y=-F_X/2\), and
\(L_4=(\nabla X)^2\), yielding coefficient \(3F_X^2/(2F)\).
The algebraic translation is executable. The source identifies a single scalar
mode for its degenerate class; this task does not reproduce its underlying
Hamiltonian classification. Its screened spherical formulas divide by
\(A_3\) and use additional approximations, so they are not applied here.

## Creminelli, Lewandowski, Tambalo, Vernizzi

“Gravitational Wave Decay into Dark Energy,” arXiv:1809.03484v2,
revised 2018-12-14, JCAP 2018(12)025.
[Primary PDF](https://arxiv.org/pdf/1809.03484v2),
[readable equations](https://arxiv.org/html/1809.03484v2).

PDF SHA-256: `751eb9a7b53dca5530e90902ab559e2d8ece5b363b9a999320894c755b0b8351`.
Equation (72) independently states the selected conformal subclass, using the
same \(Y\) convention as above. The preceding text derives it by an invertible
\(Y\)-dependent conformal metric transformation, with redefined lower-order
functions. Footnote 4 states that the quartic screening mechanism considered
there is absent in this subclass. No screening or decay-rate prediction is
inferred for the present unsolved model.

The precise local invertibility condition used here is derived directly from
\(\widetilde X=X/C(X)\): \(C-XC_X\ne0\). This avoids interpreting the
source's informal comment about linear conformal factors as a ban on the
invertible affine control \(C=1+\lambda X\).

Classification: known family after notation translation. The new work in this
checkpoint is its independently checked static variation and inverse-equation
discriminator. No claim about literature-wide priority is made. Search scope
ends at these two primary versions and the listed local predecessor.

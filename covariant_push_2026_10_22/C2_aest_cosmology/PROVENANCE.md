# C2_aest_cosmology: provenance of owner-approved downloads (2026-10-22)

**Approval.** The owner's words, relayed by the coordinator: "fetch the two AeST papers, the Planck 2018 TE/EE spectra and cobaya
with plik-lite for the native CMB lane".

**Storage.** Each item was fetched into its own new, empty directory under `_external_data/`, outside the repo.
None of the large files is committed.

**Use.** No downloaded code was executed for any number in this lane:
- The paper sources were read as text.
- The data files were read with numpy under `python3 -I`.
- A classifier denied importing cobaya into the analysis Python, so the likelihood formulas were
  reimplemented from cobaya's source, read as text.
- cobaya's own installer (`cobaya-install`) was run once, inside its venv, to fetch the plik-lite and low-ℓ data.

Retrieval times are UTC.

## 1. AeST papers: `_external_data/aest_papers_2026_10_22/`

| file | URL | retrieved | bytes | sha256 |
|---|---|---|---|---|
| 2007.00082.pdf | https://arxiv.org/pdf/2007.00082 | 2026-10-22T22:01Z | 857654 | e2057c92c44fa10d36d9c77f532d610a815591bed2a329c2a39635d7dab34d66 |
| 2007.00082.eprint (gzip tar) | https://arxiv.org/e-print/2007.00082 (served from /src/) | 2026-10-22T22:01Z | 758578 | b65d515e24d3436e0aa37ab1a7c97653814d6b8cddb22710ead88b9d93f795a8 |
| src_2007.00082/newRMONDLett.tex | extracted | — | 41520 | 31bd0abbdc68d8d5b73da3a5e0e1cc078c2a4fbce0e174e2e86704813250871d |
| 2304.05134.pdf | https://arxiv.org/pdf/2304.05134 | 2026-10-22T22:01Z | 802375 | d9a980f283298172bb0c65baba5dadc542dba927df6983c642f6299a5c565b18 |
| 2304.05134.eprint (gzip tar) | https://arxiv.org/e-print/2304.05134 | 2026-10-22T22:01Z | 392218 | d5d365f89e552b591b0d289e98cc2846ff41664f1fce604985ec589ca5eac71e |
| src_2304.05134/main.tex | extracted | — | 84139 | 92ba4d918d6a657e5be009c00ff5a9c38a98edda95a112465fb6cd4e9d04c32c |

Titles and authors were verified from the LaTeX:
- 2007.00082: "New Relativistic Theory for Modified Newtonian Dynamics", C. Skordis and T. Złośnik. The e-print is dated 2021-10-15, the PRL version.
- 2304.05134: "Aether Scalar Tensor (AeST) theory: Quasistatic spherical solutions and their phenomenology", P. Verwayen et al.

## 2. Planck PR3 spectra: `_external_data/planck_pr3_spectra_2026_10_22/` (IRSA mirror of the PLA)

| file | URL | retrieved | bytes | sha256 |
|---|---|---|---|---|
| COM_PowerSpect_CMB-TE-full_R3.01.txt | https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/COM_PowerSpect_CMB-TE-full_R3.01.txt | 2026-10-22T22:02Z | 135731 | 8b2c97d8865ebfdfb2b23c3e6883a39820734b804ba6e353533657b3a2f71425 |
| COM_PowerSpect_CMB-EE-full_R3.01.txt | https://irsa.ipac.caltech.edu/data/Planck/release_3/ancillary-data/cosmoparams/COM_PowerSpect_CMB-EE-full_R3.01.txt | 2026-10-22T22:02Z | 135731 | c865c56fe215e17e45eeed1069ddcd7d13365735f439fd63cc9c9325db97d67f |

Each file has 1996 lines: ℓ, D_ℓ, −dD_ℓ, +dD_ℓ. The errors are diagonal only. These files are not used in any check; they are kept for a later native comparison.

## 3. cobaya: `_external_data/cobaya_2026_10_22/`

- **Code.** `venv/` is a dedicated venv made from the base Python 3.13. It holds `pip install cobaya` from PyPI → **cobaya 3.6.2**, plus 29 packages in total (numpy 2.5.4, scipy 1.18.1). Installed 2026-10-22T22:02Z.
- **Data.** `packages/` was filled by `cobaya-install planck_2018_highl_plik.TTTEEE_lite_native planck_2018_lowl.TT planck_2018_lowl.EE`,
  from the official GitHub releases of `CobayaSampler/planck_native_data`, release v1, at 2026-10-22T22:03Z. Total size 19 MB.
- **Why `_native`.** The owner named "plik-lite"; the `_native` variant is the pure-data form, which needs no clik compile.
  The low-ℓ TT and EE likelihoods are cobaya's native versions (`planck_2018_lowT.zip`, `planck_2018_lowE.zip`).

| file | bytes | sha256 |
|---|---|---|
| planck_2018_pliklite_native/cl_cmb_plik_v22.dat | 37393 | dac0d9d493213e77c940a10a968cf0da3c5730bae60e1356c4cd8bcff96377ff |
| planck_2018_pliklite_native/c_matrix_plik_v22.dat | 3006160 | ad90378c50bd67841764179c90ae6711fa4317c649966ab2b0712143b31e0a32 |
| planck_2018_pliklite_native/bweight.dat | 185925 | 8afcbd8bad769e2de96bacd80177e6543f96b2b406e6c2da1fd0d26718c9e415 |
| planck_2018_pliklite_native/blmin.dat | 16125 | 325b351cbf8f694556bb13e98f285344e8d66811bb8eef18bcdcf1626518719d |
| planck_2018_pliklite_native/blmax.dat | 16125 | c28ade0fa5270c7e87ba07bdcb68aef8783b132b352bfaa36c04d17694ab4014 |
| planck_2018_pliklite_native/plik_lite_v22.dataset | 415 | 0dc7318de1b1b8fe0ad79e6bdb13135eae0190c9678e52a0a4f5120ceafa64ca |
| planck_2018_lowT_native/cov.txt | 1582091 | f3bedefd70c80388a4bda13faffc2cd803e59437216ca842e9df85aaa8c119d4 |
| planck_2018_lowT_native/mu.txt | 6356 | aa2ffbcb2d26c2881553de428aba729422390f3bb04a20b7ee9ea3865aee579f |
| planck_2018_lowT_native/mu_sigma.txt | 6225 | 3c396bb6997c2746f5da0736c3d95eb6c748887e10613e37c481851a4fed6996 |
| planck_2018_lowT_native/cl2x_1.txt | 6225000 | 9c681e02595b14a3a934a32d3cfa93be7fba1968083a59326828834e37ac83b5 |
| planck_2018_lowT_native/cl2x_2.txt | 6341136 | 46714e527337832604f42eade620277910e7cc8d62af0150d2eb2873676ebb05 |
| planck_2018_lowE_native/prob_table.txt | 2187000 | 7efa150e762313f7920b7ae2b4f3cf3c7d3fdaaa6b1ae257b60b2c75279fe7b3 |

**Data classes.**
- plik-lite is foreground-marginalised (Prince & Dunkley compression) and counts as SURVEY-CALIBRATION.
- The low-ℓ products are Planck's PR3 pixel-likelihood compressions.

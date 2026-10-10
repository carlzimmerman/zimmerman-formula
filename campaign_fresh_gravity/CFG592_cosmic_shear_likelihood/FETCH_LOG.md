# CFG592 fetch log

Owner approval in chat, 2026-10-10 ("yes download the KiDS and DES shear data"). Files are stored outside git in `../_external_data/cfg592_work/` (relative to the repository root's parent). No login or bot check was met.

| date (UTC) | URL | bytes | SHA-256 |
|---|---|---|---|
| 2026-10-10 18:04 | https://kids.strw.leidenuniv.nl/DR4/data_files/KiDS1000_cosmic_shear_data_release.tgz | 17283861 | 97729199aeb23238767921f58f36341317aa5251beab99e2575eb35fe78c7bb3 |
| 2026-10-10 18:04 | https://desdr-server.ncsa.illinois.edu/despublic/y3a2_files/datavectors/2pt_NG_final_2ptunblind_02_26_21_wnz_maglim_covupdate.fits | 28287360 | 83efa43f6609ff07248b9c4e411b9ab386ec569cba402364fb21edff456e8b76 |
| 2026-10-10 18:05 | https://raw.githubusercontent.com/KiDS-WL/Cat_to_Obs_K1000_P1/master/data/kids/nofz/SOM_cov_multiplied.asc | 295 | 7a0a36040e065f43131f4a208fbda8f8290868eb9867bd2704a86b00f1cad5f1 |
| 2026-10-10 18:05 | https://raw.githubusercontent.com/joezuntz/cosmosis-standard-library/main/examples/des-y3.ini | 12804 | 3eb12b626e7ad705e7562f219444d0292b9be2cf6d3216afcfc04123f911c233 |
| 2026-10-10 18:05 | https://raw.githubusercontent.com/joezuntz/cosmosis-standard-library/main/examples/des-y3-values.ini | 1377 | d1ff37841b08df28b12693f003cddb2e2c75094d244d884608462b386b133a10 |
| 2026-10-10 18:05 | https://raw.githubusercontent.com/joezuntz/cosmosis-standard-library/main/examples/des-y3-priors.ini | 538 | 1f316d1988fab366862dd4c7c386659e016ddf0e83f630b77028235261894ce9 |
| 2026-10-10 18:05 | https://raw.githubusercontent.com/joezuntz/cosmosis-standard-library/main/examples/des-y3-scale-cuts.ini | 1836 | 92b5f05037cc498614926f5dd4b7723b62f6e0db892d56be0526a6455a2a6a14 |

Total about 45.6 MB (cap 400 MB). Software: pyccl 3.3.6 installed by pip into a virtual environment inside `../_external_data/cfg592_work/venv` (outside the repository; about 20 MB); CAMB 1.6.6 was already installed.

The DES Y3 maglim file is the 3x2pt release; only its xip / xim extensions, the matching covariance block and nz_source are used. The KiDS tarball also holds COSEBIs and band-power files and the published chains; only the ξ± file is used, and the ξ± chain only for the S8 reference value of control C1.

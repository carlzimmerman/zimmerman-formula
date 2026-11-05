# Public ALMA input retrieval

Raw FITS downloads are deliberately excluded from Git; they remain in the original local workspace. This repository saves metadata, source code, derived measurements, numerical results and provenance, not a self-contained copy of the raw observation.

Public product listing:
https://almascience.eso.org/datalink/sync?ID=uid://A001/X2d1f/X33c

Project: 2022.1.01118.S. Product archive:
`2022.1.01118.S_uid___A001_X2d1f_X33c_001_of_001.tar`

Retrieve the public product archive and restore these files into this directory to reproduce the final run:

- `member.uid___A001_X2d1f_X33c.vuds_cosmos_5110377875_sci.spw25.cube.I.pbcor.fits`
- `member.uid___A001_X2d1f_X33c.vuds_cosmos_5110377875_sci.spw25.cube.I.pb.fits.gz`

The exact input hashes are recorded in `../run02/manifest.json`; validate them before re-running. `../contract_v2.json` records software versions and scope. Other locally downloaded spectral windows were not required by that calculation. A fresh checkout cannot validate or rerun the raw-input computation until these files are restored.

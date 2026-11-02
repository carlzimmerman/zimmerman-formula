# ACDM flavored fried chicken version of Galaxy Dnynamics

Working note, v1.0, DOI 10.5281/zenodo.23897582. How exactly LCDM's knobs can reproduce the law on real SPARC baryons, and what each match costs. Rival-flavoured exercise; adopts nothing and reinstates nothing. kappa = 1/2 FITTED; not theory closed.

- `lcdm_fried_chicken.tex` / `.pdf`: the paper. Rebuild: `tectonic lcdm_fried_chicken.tex`. Check: `python3 audit.py`.
- `FROZEN_RECIPE.md`: targets, recipes, Amendments A1 to A3, and the cosmology bug note.
- `scripts/recipe.py`, `recipe2.py`, `recipe3.py`, `recipe4.py`: run from `scripts/`, needs colossus. Outputs are the `.out` files. `recipe2_before_cosmology_fix.out` is the wrong run, kept on record.

Bibliography entries are from memory and were not checked against the journals. Fixing the cosmology bug also corrected `../REDTEAM_LCDM_PRIEST/`.

# Scope and exact prior-work distinction

KT40 `mw/diagnose.py`, `diagnose_hydro_v2.py`, and `force_probe.py` explicitly loop only over `(canonical,1368)` and `(alt,1287)`. The force probe refines those two witnesses at refinements 3–6 and checks potential differences. It does not enumerate all original KT39 primary passes at R=12 kpc,z=.3 kpc.

KT39 `adaptive_1125_001/results.json` supplies the immutable selection: stored all_four primary scores at p=9/8,ell=3kpc, production refinement2, exactly32 canonical and20alternate indices. A separate reconstruction of that criterion must agree with the stored summary. Current new runs do not reselect after seeing local force.

KT42 `mw/filtered_model.py` implements H_h T_h psi with its full volume-weighted transpose; `calculate_v2.py` and `checks_003/results.json` establish prior adjoint/energy/heat/zero-width controls, while `scan_001/results.json` supplies the two-witness refinement3 replay. These files are imported/read only. This task applies that same implementation to52 preselected baryon cells at three widths, rather than claiming a new action or rerunning the original1375-cell population.

`selection.json` pins the old population result and stores every selected index/cell/production score. `novelty_search.json`/`.txt` record a focused KT39/KT40 source/contract search; the broader bounded prior-work audit is in KT41/nonlocal. This is a new specified selection-dependence discriminator in those parent records, not proof of universal repository or scientific novelty.

Frozen values: p=9/8,ell=3kpc,a=0,.0001,.001kpc, refinement3,heat32,rmin=.005kpc,outer multiplier1, original a0,baryons,primary cuts. Signed gz is partial_z Phi atR12,z.3 in (km/s)^2/kpc; gz<0 corresponds to upward/outward acceleration above the midplane. Refinement3 plus32heat steps is a numerical diagnostic. Two witness refinements do not certify every population cell, and this is not an exclusion of all1375 baryon configurations for the filtered action.

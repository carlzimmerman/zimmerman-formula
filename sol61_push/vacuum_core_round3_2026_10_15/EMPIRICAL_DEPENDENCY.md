# CFG801 dependency impact: finite-stock energy minima are not a lensing pass

15 October 2026. Focused read-only reconciliation of shared result commit
`19e43e6148d063a9cb3dc067b6bf293b4a7b838e`, with criteria frozen separately at
`0ff46e53085f64ed937c9a1586e713869fec1c40`. Observed checkout during review:
`7e6b3dd73fa4b0e8200affaf5a3382334331dac3`.
No script was rerun, score recomputed, criterion changed or data product edited.
This note records the result's direct model dependence; it is not an independent
reproduction or full survey/data/profiling audit.

**Direct consequence.** Under CFG801's registered mass/lensing interpretation,
our gamma-zero canonical cutoff with total cold stock 5.364 Mb cannot be
presented as the complete lensing mass of its isolated-galaxy sample. It is the
same settled-only profile classified **EDGE EXCLUDED** in that run. The exact
variational/energetic theorem is unchanged; the proposed physical identification
with the entire observed halo is the dependency that fails the recorded test.

## Exact object match and recorded result

`dynamical_lift/PROOF.md` constructs

    m_c(r)=min{Mb[√(1+4r²/rM²)-1]/2, s Mb},
    rM=√(G Mb/a0),    R/rM=√[s(s+1)].

For s=5.364, R/rM=5.842644606682834. CFG801's frozen object uses precisely
this mass profile, derivative density, inventory and radius, plus a baryon
point mass. Its implementation projects the truncated three-dimensional
density along a finite line of sight. It retains the exterior excess-surface-
density tail; it does **not** set the observed lensing signal to zero outside
R. For projected radii beyond a spherical finite stock, that rest-mass
interpretation gives DeltaSigma=(Mb+Mc)/(pi R_projected²).

The code compares this against the same canonical law continued without a
supply edge. Its registered primary range is projected R<=0.31 Mpc, 8 radii
in each of 4 mass bins, with the full selected covariance. The deciding
comparison profiles one baryonic mass per bin on the same declared grid for
both models. The frozen classification threshold is DeltaChi²>=9.

| Footing and range | Recorded DeltaChi²=edge minus no edge | Registered class |
|---|---:|---|
| Canonical, primary | 197.07283636283003 | EDGE EXCLUDED |
| Alternative, primary | 234.0015218964213 | EDGE EXCLUDED |
| Canonical, all radii | 753.0232395061423 | EDGE EXCLUDED |
| Alternative, all radii | 813.0448157819951 | EDGE EXCLUDED |

The canonical primary edge chi² is 280.9324; the no-edge chi² is 83.8596
for 28 fitted degrees of freedom. The latter is also a poor absolute fit
(reported p about 1.75e-7), so the relative preference is not an observational
pass for the edgeless alternative. The provisional zero-knob masses are
separately reported, not substituted for the primary statistic. The seeded
mutation returns EDGE FAVOURED, as the registered control requires. Footings
remain separate.

## Impact on this round's claims

| Claim/model | What changes after CFG801 |
|---|---|
| Gamma-zero finite-stock KKT/global energetic minimum | No mathematical implication changes: it is still the unique constrained minimum of its declared Newtonian model. Identifying its s=5.364 point-source realization with the sample's entire lensing mass inherits the registered exclusion. Stability cannot establish observational adequacy. |
| General prescribed spherical baryon extension | Its variational proof remains valid. It is not automatically a distinct successful KiDS prediction; its own finite baryon distribution and total lensing response must be specified and evaluated. The exact point-source match above is the direct exclusion. |
| `stiff_halo/` finite-gamma inverse-source witness | Its cold density, baryon profile, stiffness and radius are different constructed inputs. CFG801 did not score that profile, so no numerical exclusion or pass can be assigned to it from this result alone. Its chosen 5.364 ratio does not make it the canonical 5.84 rM template. It remains an existence/energy witness, not an empirically supported galaxy model. |
| `critical_stiff/` and `critical_interface/` dynamical bodies | Their chosen polytropes, density profiles and/or wall differ from the tested dust cutoff. They retain their stated mathematical results but acquire no lensing pass. They do not reproduce the old pressureless galaxy law by construction. |
| S4 debris or another supply/phase rule | Not scored in CFG801: no such outer-density model was supplied. These are possible model changes requiring counted stock, a force/phase prescription and their own registered comparison; no rescue is demonstrated. |

Under the present Newtonian rest-mass gravity convention, nonzero exterior
D flux by itself does not add the missing lensing rest mass: gauge-field
energy is not included in that Poisson source. Invoking its relativistic
stress as extra lensing would require an actual completion and calculation,
not reinterpretation of this run. Likewise an added free component must obey
one common inventory and conservative charge/energy accounting; it cannot
silently duplicate the settled stock.

The original ARGON02 disk/merger-free language is narrower than CFG801's
four mass-binned isolated-galaxy sample. CFG801 explicitly lists clean
merger-free/disk-only selection and unspecified free-debris profiles among
its untested cases. Its result therefore rejects the specified settled-only
whole-lensing-mass interpretation on this sample; it does not exclude every
possible disk, debris, phase or cosmological model. Outer two-halo contamination
and provisional stellar masses are disclosed in the source, with the inner
0.31 Mpc range retained as the primary test. None of these disclosures is used
here to reverse its published classification.

## Pinned source identities and limits of this check

The following tracked bytes all match result commit 19e43e6148d063a9cb3dc067b6bf293b4a7b838e.
Paths under `campaign_fresh_gravity/CFG801_settled_edge_vs_kids/`:

| File | SHA-256 |
|---|---|
| FROZEN_CRITERIA.md | `51fa12bf5325a6bbb2e18a996a676231996f46c3289e571d407426e8e2cd6c68` |
| README.md | `dc13f66c43a58cf27bb3632d4f17c314bea7904da294388d05742b4bd86feea9` |
| cfg801.py | `cad4510cb2ff9854a7d9d3256e6172d74e3e0a79596ddd360c877c4ad20cc845` |
| cfg801_results.json | `d5b978312e856c63aa80cfcf96f7718322cf16464c4ae353d34fb41fc074e3ee` |
| cfg801_results_alt.json | `78a131de2078f787275aaa3a2fc781f966b10b7298df2764bf730334ded70347` |
| cfg801_results_MUTATE.json | `1f6e55a22f96a8795d4914eda8003c07b56ab5bd492c1117d514b3481b1d2058` |

The upstream ARGON02 frozen criteria SHA-256 is
`f19423b9cf42cace5919536601d83646d54d7bdde3e960f65e82b1ddf6f2db65`.
This round's compared proofs are the unchanged
`dynamical_lift/PROOF.md`, SHA-256
`5e34946670364a2563c7c7d9a300e6c281975a1fa3ab0f69f90af10881d51280`, and
`stiff_halo/PROOF.md`, SHA-256
`db363953a1199748c668e71c65911db17992c7e7868f6591bfc36fe43f7e01ca`.

The actual named local data files exist. Their headers confirm ESD and bias
columns and the covariance/bias-product columns read by the script. Current
SHA-256 identities under
`real_research/data/lensing_rar/brouwer2021_rar/` are:

| Input file | SHA-256 |
|---|---|
| Fig-3_Lensing-rotation-curves_Massbin-1.txt | `cd8171d248a5c660701c2fcfb5f39eea01ae57b5b9ec2bae233e5aef77e7d78e` |
| Fig-3_Lensing-rotation-curves_Massbin-2.txt | `279d82e4faee34041221b617f0ce9cfc97966c431616c94608b0983e60421ae7` |
| Fig-3_Lensing-rotation-curves_Massbin-3.txt | `88eca49e85504c1eb6ce11e09edcdda37c0903dd678f2207ed4bca4fa31f7a22` |
| Fig-3_Lensing-rotation-curves_Massbin-4.txt | `05853565ae193347adff22f8aec58c50f80b2e22866fb9c532137c6f198a79e1` |
| Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt | `e2568b34578a4752c4cdc25c23cd38c896ac1c5e0477cce3fe8d7b32e4954445` |

These are review-time data hashes, not a claim that this note authenticated
the survey release or reconstructed the original run environment. This check
did not rerun the projection, certify the coordinate profiler's global optimum,
revalidate the full covariance statistically, or revise the frozen sample and
scores. The focused conclusion is the exact profile dependency and the need
to preserve the recorded empirical failure alongside the new mathematical
energy results.

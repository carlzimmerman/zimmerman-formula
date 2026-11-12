# Stronger density/potential ambiguity: the same portal coefficient also survives

12 November 2026. Independent audit of the coordinator's specialization of the general D/V overlap family. Original `portal_checks.py`, contract and accepted run02 inputs are unchanged. This addendum has its own contract, checking script and validated `fixed_coefficient_run01` provenance.

## Exact construction

Retain the report's flat-late GR-FRW assumptions, constant gG=G_cosm/G_N, independently measured F=h² and Q=q², and separate conservation. Fix **the same** positive C=8πgG/(3κ²) in both the density and canonical-potential portal. Let P,R>0 and choose Aρ>=CR. Set

    Q=P+R u³,
    F=Aρu³+C Q=CP+(Aρ+CR)u³,
    Av=Aρ-CR>=0.

The density reading has

    Xρ=F-Aρu³=C(P+R u³)=C Q,
    Yρ=Xρ-uXρ'/3=CP>0,
    wρ=-P/(P+R u³).

The potential reading has

    Xv=F-Avu³=CP+2CRu³>0,
    Zv=Xv-uXv'/6=CP+CRu³=C Q,
    kinetic=Xv-Zv=CRu³>0,
    Yv=Xv-uXv'/3=CP>0,
    wv=-P/(P+2R u³).

Both w functions evolve strictly with u for R>0, and both branches have negative pressure and positive density. The potential branch is canonical at the homogeneous background level. Its positive kinetic energy permits monotone-field reconstruction on an expanding interval; that is not a demonstration that a chosen a0-coupled action is healthy.

**The measured F,Q and the constant κ/sqrt(gG) are identical.** The difference is an inferred matter amplitude ΔA=CR and a corresponding dust-shaped contribution assigned to the homogeneous sector. The background F itself is exactly the usual constant-plus-dust functional form. Thus even an independent calibration of the portal coefficient cannot generally distinguish density versus potential promotion without an independent constraint on the matter split. This is stronger than saying free coefficients absorb constant-w factors.

The family is already contained in the report's D/V solution at s=0, Cρ=Cv=C. No conflict arises with the report's triple-overlap result: a positive constant pressure coefficient would require

    Cp=[F-uF'/3]/Q=CP/(P+R u³),

which varies. If Cp is required to equal C it fails by CRu³. Only R=0 gives all three equal-coefficient portals together, the vacuum limit.

## What would distinguish it

More precise measurements of the same h and q functions cannot break this exact D/V equivalence. One needs additional physical information that fixes or bounds the matter-versus-sector dust assignment, or sector perturbations interpreted through a specified stable parent theory. Growth/lensing do not automatically measure an unambiguous matter density: their interpretation depends on the same gravitational and stress assumptions, so the proposed extra information must be independently justified. Non-gravitational baryon inventory alone does not necessarily determine the full conserved pressureless amplitude A.

The pressure integral statistic from the report can distinguish this family from a constant-coefficient pressure portal when Q is independently resolved between bins. It remains subject to its finite-interpolation and covariance limitations. No observational discrimination or sample power is claimed here.

## Evidence

`fixed_coefficient_contract.json` froze this analytic family before execution. `fixed_coefficient_checks.py` checks 17 identities/sign properties: both portal equations at equal C, matter split, canonical positive kinetic, evolving w, exact constant-plus-dust background, and pressure incompatibility. All 17 pass in `fixed_coefficient_run01/results.json`; run status is completed and the installed v2 manifest validator passes. The physical parameter condition Aρ>=CR is explicitly external to SymPy's independent positive-symbol assumptions, and is required before asserting Av>=0.

This is a scoped identifiability result, not a new normalization derivation, a claim of healthy coupled gravity, an observational fit or a literature novelty claim. September's inverse-dust ambiguity remains prior work; this is its explicit same-coefficient density/potential specialization.

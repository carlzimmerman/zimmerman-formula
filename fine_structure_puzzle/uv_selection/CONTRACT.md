# FSP-U1: coupled Abelian fixed-point discriminator

Date: 2026-10-18 America/New_York. Input checkpoint: FSP-000, Git `3c01aa2861bf576f4c2d942251eb9d2f89cae108`, dirty baseline.

Question: does a genuinely coupled two-U(1) fixed point fix the physical hypercharge normalization, or only a matrix direction/upper bound once the unknown gravity coefficient, branch choice and symmetry-breaking matching are exposed?

The candidate is the minimal B-L / chi completion in Carone, arXiv:2512.12044v1, published February 2026. It was absent from the old lane-B investigation. The source uses one-loop MSbar matter beta functions and a universal phenomenological gravity contribution `-f_g G` above a step at the Planck scale. These assumptions are tested algebraically here; no full FRG computation is being reproduced.

`assertion_tested`: for exactly the two charge tables specified in `source_equations.json`, independently sum the one-loop charge-trace matrix B; compare the induced matrix flow with the three published triangular-coupling beta functions; find and linearize its full-rank and rank-one fixed points; derive the physical single-photon matching and the coefficient-free top-bottom Yukawa difference. All load-bearing equalities use exact rational/symbolic arithmetic. The general claims about matrix rank and the UV-finite cone also receive a written analytic proof in REPORT.md.

Normalization: `D = d - i q^T G A`, q = (Y,X), canonical vector fields A, `G=[[gY,gt],[0,g]]`, `H=G G^T`, `K=H^-1`. Hypercharge is Q=T3+Y; g1=sqrt(5/3) gY in the source. `F=fhat_g=16 pi^2 f_g>0`, t=ln(mu), and script vector fields are multiplied by 16 pi^2. Fermion weights are 2/3 per Weyl degree of freedom and scalar weights 1/3 per complex degree of freedom, with 3 fermion generations.

Bounds: two models; no parameter search, fitting, or measured alpha input. Rank-one ellipse sampled symbolically by a free slope parameter, with one rational orientation used to check its local characteristic polynomial. The stable scalar family is checked symbolically for c in (0,1). Optional floating values only display exact results.

Outputs cannot establish the existence of an exact quantum-gravity fixed point, its unitarity, the true f_g, convergence of a truncation, realistic scalar breaking/masses, full flavor viability, or alpha(0). A missing FRG coefficient is not a proof that no completion can supply it. A fixed point in the phenomenological matter system is conditional evidence only.

Command: the bounded computation-audit runner launches `python3 fine_structure_puzzle/uv_selection/discriminator.py --output fine_structure_puzzle/uv_selection/run-001/result.json`. The `--mutate` control changes only the source beta-function cross coefficient and should fail its independent charge-trace comparison.

# Independent conformal-cutoff action review

Verdict: accepted as stated for the classical improvement convention, the positive-domain constant common vacuum, its unique global minimum and canonical mass bound. No blocking mathematical error found. The action is not Weyl invariant, its kinetic normalization remains free, and neither a physical observed coefficient nor full relative/clock health is established.

Frozen inputs independently pinned:

- REPORT.md: 3aa76c222fdeb99b82dfe84739179e6abac1237e1a3797edcd9c24fea094ab9e.
- checks.py: 13584e703c7f2c7109c0be380e67f29a163eacc79ecf63e9a12b3b24306654da.

Only this peer note was written; author inputs were not edited.

## Raw trace and action convention

For −(∂φ)²/2−ξRφ²/2, flat improved stress is canonical stress plus ξ(ημν Box−∂μ∂ν)φ². Its trace is −(d−2)(∂φ)²/2+ξ(d−1)Boxφ². On the free massless equation Boxφ=0, Boxφ²=2(∂φ)², so ξc=(d−2)/[4(d−1)] is exactly the required improvement value. This fixes a free scalar's trace convention, not the full two-metric model's symmetry. With φ=fu it indeed gives F=1−ξc(f²/M0)u², as reported. The common multiplier of the interaction is an additional declared action choice, required for the parent's critical leading MOND cancellation. No symmetry argument fixes f²/M0 or the action a0.

The full independent constant-u metric variations give the parent's unchanged Λ=χn a0²A/2, while the scalar's nonminimal curvature variation requires pA=βq, β=2/(d−2). Dropping either metric equation or the curvature part of the scalar equation would change the result. On the exact common sector, the Einstein frame has U=V0A F^-β and Z=f²/F+M0(d−1)q²/(d−2)>0. This reconstruction uses F>0 throughout; no crossing of its zeros is licensed.

## Uniqueness and global minimum

Let α=ξcγ, z=αu². Direct differentiation gives q=−2αu/(1−z), q'=−2α(1+z)/(1−z)². Since pA>0, a root must be on the negative-u half-domain. The log-potential slope tends to −∞ at its left finite F=0 endpoint and is positive at u=0 and on the positive half. Hence it has a negative-u root.

At every root, eliminating α in favor of pA=βq yields

C=(logU)''=pA'+pA²(1+z)/(2βz)>0,

using 0<z<1, β≤1, pA>1, and pA'>−1/4. Thus every root crosses from negative to positive slope. Two distinct roots would require an intervening zero with nonpositive crossing derivative, contradicting the same identity. This is stronger than sample root-finding and does not assume that the slope is globally monotone away equilibria. There is exactly one critical point. At both finite endpoints F^-β diverges while A(exp u) has a strictly positive finite limit; U therefore tends to +∞ at both ends. The unique strict minimum is global on this connected positive-F domain. This is a common canonical potential statement, not a proof of all-sector nonlinear stability or a global cosmological attractor.

Since u<0, T<1 and A(T)<πT/2 gives the stated action-parameter bound Λ/a0²<χnπ/4. Operational Newton/MOND calibration is a separate source problem; no observed a0 is substituted into that inequality.

## Exact canonical mass interval

At fixed ξc, γ=α/ξc. Combining the Jordan kinetic term with the Einstein conformal term gives

Z/M0=γ/(1−z)+(d−1)q²/(d−2)
     =(d−1)q²/[(d−2)z].

A fresh symbolic calculation returned zero residual for this identity. At a root q=pA/β, and m²/HE²=2z pA'/pA²+(1+z)/β; I separately reconstructed and symbolically checked this ratio. Its upper bound is strict because pA'<0 and z<1. Its lower bound follows from

m²/HE²>1/β+z[1/β−1/(2pA²)]>1/β.

Thus (d−2)/2<m²/HE²<d−2 in all stated d≥4. With a stationary potential and constant background scalar, common metric perturbations do not mix linearly into this canonical scalar equation. The scalar has positive kinetic and unit principal speed; mass of order H does not justify a rapid-oscillation cold-fluid claim. No relative modes are thereby diagnosed.

## Frozen radial inverse admission and numerical scope

The stationary equation also gives |u|<3/(4βα)=3(d−1)/(2γ); fresh algebra checked the last factor. For γ=100,d=4 this yields T>exp(−.045). The frozen radial inverse derivative is 1 plus the strictly positive b+yb' term minus 4b(y/T)²/[1+(y/T)²]². For y≥1/3, the negative term is at most b≤1, so the positive term gives strict positivity. For y≤1/3, it is at most 4y^(3/2)/T²; T²>4/(3sqrt3) is sufficient. The γ100 lower bound satisfies it. This proves admission of the fixed-T radial constitutive chart, not the coupled nonminimal scalar/matter source boundary problem. No global radial source is asserted for the other sample roots merely from vacuum stability.

I independently reevaluated all three stored sample roots with 35-digit mpmath integrals over the entire real line, using pA'=Cov(ell,tanh v) rather than the author's finite-window second-derivative integrand. The stationarity residuals were approximately −4.84e−17, −1.22e−13 and 2.07e−13 for γ=4,10,100. A/2 and m²/HE² agree with the displayed table. These are independent numerical corroboration, not interval-certified root proofs; existence/uniqueness are analytic above.

All three current manifest validations independently returned exit 0. Raw records have main 27/27, sign 25/27 with only the two declared prefactor symbolic identities false, and mass 27/28 with only the rapid-cold-mass assertion false. The sign control changes symbolic F only; it is not a full alternate-action cosmology run. The counts do not replace the action and global-minimum arguments.

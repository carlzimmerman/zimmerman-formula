# Independent reconstruction of the two-sided minimizing completion

Primary verdict: **proved as written within the declared local inverse-chart and eliminated-invariant scope**. The two parity constructions have the stated auxiliary costs, and retaining the positive source envelope prevents a C² eliminated invariant action on an open Lorentzian metric-first-jet neighborhood. This does not establish an on-shell physical ghost, rule out a nonsmooth constrained theory, or exhaust possible extra operators. No blocking correction found.

Reviewed at actual HEAD `1db53a670a09a76c023e70784fddc5f351fb8a81`. Only this review is written by the reviewer; author inputs and historical evidence remain unchanged.

## Inspected frozen inputs

- REPORT.md: `601d2679f84c79f5148e09575ee27c4e107b8a5e669393244919ff1c15aaab2e`.
- checks.py: `f82f8f49ab5163f1eed060b99208c540e1a3c4d2030f78994c4fd73c6d8ffb58`.
- contract.json: `587c2e38f8f4c5580de2530b2e04aa6326e5734dfaa62f98ba6c46753e9d38ce`.
- SOURCES.md: `dcceff7103b3ab23ea904ab682e58898d6848cee68a707ee6595232c23e839cc`.
- provenance.json: `e093ae8ab0c4c2fa3be5e5fb42d98462101a21043f1c8c39dbe6bb7d2d10a728`.

Inherited actual-action leaves independently read: covariant_vacuum_dictionary/REPORT.md `66e0b0104c2064a942387a10552d649e371105dfb1fc857b4ebe0422e6de8ef2`; symmetric_external_field/REPORT.md `ad34e20ad62b9a0e2b30ebddf14a5f6025a69053e98915d86bde5486cb2adc94`; tensor parent REPORT.md `912ad06793bb41e3c96819f3f7e72db104b44122b31c17bf48a74770cf848287`; scale-covariant parent REPORT.md `b53ecf9b85e59808cc54174e3f2f92afe3789dad2f3de8d2d2083aa56bc7b52f`. The repaired contraction averages both inverse metrics. The primary g-only contraction is not silently treated as exchange invariant.

## Dependency graph and independent derivation

The positive source input is the actual symmetric radial source dictionary, not the opposite-sign QUMOND map: x=y+2d, d=ye, q_y=2d, M=q+2d²−λT²/2−A_off, and z=x². An inverse chart x_y>0 is an explicit hypothesis. At fixed T,

    M_y = 2d(1+2d_y) = 2d x_y,
    M_z = M_y/(2x x_y) = d/x = 1/2−y/(2x).

The source stationary root is q_T|y=λT. When varying the actual invariant x rather than y, x_T=2y e_T=q_Ty, so

    y_T|x = −q_Ty/x_y,
    M_T|x = q_T−λT,
    M_TT|x = q_TT−λ−q_Ty²/x_y.

The static auxiliary energy curvature is therefore λ−q_TT+q_Ty²/x_y. Directly differentiating q_T=4T∫₀ʸ t³b(t)/(T²+t²)² dt and using stationarity gives

    λ−q_TT = 16T²∫₀ʸ t³b(t)/(T²+t²)³ dt > 0.

This independently proves the strict local minimum on every such source chart, beyond the three numerical examples. It proves neither a global minimum across a chart fold nor the identification of the T=0 boundary with the interior minimizing solution. Near the source origin T~K y^(7/8), K⁴=8/(7λ); direct leading integral differentiation gives q_TT~−3λ. The chain correction q_Ty²/x_y is O(y^(1/4)), so H_T→4λ. Taking the T=0 vacuum axis first instead gives λ. The two limits do not imply a smooth joint Hessian.

Set a_d=√(7λ/8). The inherited analytic source IFT gives x=2√y[1−a_d y^(1/4)+O(√y)]. Its inverse is y=x²/4[1+2a_d√(x/2)+O(x)], hence

    M_eff,z = 1/2−√z/8−a_d z^(3/4)/(4√2)+O(z),
    M_eff,+ = −A_off+z/2−z^(3/2)/12−a_d z^(7/4)/(7√2)+O(z²).

The IFT provides differentiable expansions; differentiating an arbitrary little-o remainder would not suffice. In particular √z M_eff,zz→−1/16. The coefficient −1/12 is fixed by the actual radial response and is independent of λ. This is a scalar-envelope statement on positive z, not a nonspherical physical Newton-field identification.

## Parity constructions with the same potential

Write r=|z|, B=q+2d², R_joint=B−r/2. For the absolute construction M_abs=−A_off+z/2+R_joint(r,T)−λT²/2. Its negative-z expression B(r,T)−r−λT²/2 has exactly the same fixed-r auxiliary derivative and energy Hessian as the source side. It therefore retains the local minimum T_min(r). Eliminating T yields negative-side slope 1−m(r)>1/2. The T=0 axis slopes zero and one remain distinct from the envelope limit 1/2; this construction does not regularize the joint origin.

For the odd remainder with the SAME potential, negative z gives M_odd=−A_off−B(r,T)−λT²/2, with M_T=−q_T−λT<0 at finite r,T>0. Thus the old positive root cannot be inserted as a solution of this action. This is an interior-root obstruction only; it does not exclude a separately defined T=0 boundary. If the entire eliminated remainder is made odd by also flipping the potential, M_T becomes −q_T+λT. The old root returns, but M_TT becomes +H_T and the auxiliary energy has negative curvature. The sign cost is genuine. Arbitrary alternative negative-side functions are not exhausted by these two tests.

## Metric-jet sign and regularity audit

For mean-zero planar TT first-jets with tr(e²)=2, the raw flat coincident-position contraction gives Υ_sym=(v²−w²)/2 and z=(w²−v²)/(4χ_n a₀²). The two Einstein-Hilbert terms give K(v²−w²)/4; interaction z/2 cancels this exactly. On the absolute timelike envelope w=0, the first retained term is

    L_rel = −K|v|³/(48√χ_n a₀)+O(|v|^(7/2)),
    L_vv = −K|v|/(8√χ_n a₀)+O(|v|^(3/2)).

The prescribed odd envelope reverses this leading sign, but is not the stationary envelope of the same-potential odd action. The one-polarization P(X)=sgn(X)|X|^(3/2) comparison indeed has positive P_X, timelike ratio 1/2 and spacelike longitudinal ratio 2. These are coefficient/principal calculations in a restricted truncation. No ADM constraint elimination, admitted background or full bimetric physical dispersion follows from those ratios or from the unfavorable absolute sign. The report retains this restriction correctly. Curved backgrounds also have the tensor parent's lower-derivative curvature terms; this flat coefficient jet is not a de Sitter solution calculation.

For a nonzero null jet v=w>0, D_w z is nonzero. Approaching from the unchanged positive side w=v+ε gives

    √ε ∂w²[−z^(3/2)/12] → −(1/16)[v/(2χ_n a₀²)]^(3/2).

I independently differentiated this expression in an in-memory SymPy calculation, without importing author functions. The next z^(7/4) term is only O(ε^(−1/4)) in its second derivative, so it cannot cancel the ε^(−1/2) divergence. A negative-z choice cannot change this one-sided limit. These are realizable TT metric first-jets, not arbitrary connection arrays. Scaling v=w to arbitrarily small nonzero values places such jets in every open first-jet neighborhood of the origin. Therefore an invariant-only eliminated action retaining this positive envelope cannot be C² on such a neighborhood.

At C=0 itself the remainder is O(||C||³), with gradient O(||C||²); its second Fréchet derivative exists and is zero. That pointwise fact does not give a continuous Hessian on a neighborhood containing nonzero null jets. Similarly T_min~const|z|^(7/8)=O(||C||^(7/4)) has zero first derivative at the zero jet but is not twice differentiable there. The absolute envelope is C¹ across null jets; this must not be confused with joint smoothness of the original (z,T) functional. Extra independent invariants/operators or a restricted admissible jet domain change the premise and are not ruled out by this argument.

## Obligation and computation status

Passed: actual symmetric radial source slope; fixed-invariant auxiliary chain; strict local Hessian; near-zero envelope coefficients; both explicit same-potential parity tests; planar TT normalization/sign; one-sided null-jet obstruction; origin-versus-neighborhood distinction.

Conditional: local inverse chart and admitted auxiliary branch inherited from the source construction. Not addressed: on-shell dynamical admission, complete lapse/shift/metric constraint structure, nonlinear nonsmooth PDE solutions, all-helicity physical health, or a primordial cold-sector interpretation. Out of scope: 32π selection and global novelty.

I independently validated all four current standard manifests against the repository root using the installed computation-audit validator. main_a has 33/33; control_odd_a, control_null_a and control_time_a each have 33/34 with one intended extra false assertion. The controls test retaining the source root in the odd same-potential action, finite null Hessian, and favorable absolute time curvature respectively. The three 60-digit charts verify local finite values and asymptotic coefficients; they are not the universal proof. The universal local sign and regularity conclusions follow from the identities and limits above. No extra author execution or source edits were needed.

The strongest safe result is a source-law obstruction to an ordinary C² eliminated invariant-only completion on an open Lorentzian first-jet neighborhood, together with a constructive absolute local minimum and a precise odd-continuation auxiliary cost. The missing implication is an admitted full constrained dynamical theory; none of the frozen evidence supplies it.

# Independent final radiation-capacity audit

**Primary verdict: proved conditional on the retained same-action quadratic system and the declared radiation-density-square ansatz.** The exact finite-Z clock Schur gain is bounded by the radiation budget; for every fixed eta>0 there are sufficiently small positive fold radiation fractions with an intermediate finite epoch where this operator cannot repair all sufficiently small nonzero-p clock coefficients. The universal family conclusion follows from an analytic dust-limit continuity proof, not a numerical grid.

This audit uses the corrected final deltaF sign and b_r normalization. The authoritative execution generation is `main_c/control_universal_c`; a and b are explicitly superseded. Observed HEAD: `36b9957612c8b422e900874fb053c6baa22456e4`. Inspected final inputs and outputs are pinned below. No author input was edited or executed here; current c manifests were independently hash-validated.

## Actual square, source dictionary and constraints

For the minimally coupled parent radiation scalar `P(Y)=lambda Y²`, the bare density function is `rho_r=3lambda Y²`. Its first variation is

`delta rho_r=4rho_r(s_r−nu)`, `s_r=dot(v_r)−Hv_r`.

The background clock obeys X=q²/2. With `B_rho=dB/d rho_r` and `b_r=4rho_r B_rho/q²`, direct subtraction gives

`deltaF=delta X−B_rho delta rho_r`

`=−q²[(1−b_r)nu+b_r s_r]`.

Thus `Delta L_2=DeltaSigma[(1−b_r)nu+b_r s_r]²`, `DeltaSigma=Zq⁴/2`. The corrected sign matters: the lapse coefficient of the square is not simply DeltaSigma, and its velocity mixing cannot be dropped. The lack of a first-order shift perturbation follows from the homogeneous backgrounds of both scalar kinetic invariants. Consequently the unchanged parent shift relation gives the velocity part `nu=d zetadot`, `d=M/Theta`; dust/radiation velocity-potential terms in that relation contain no time derivative. Define `u=dot(v_r)−d zetadot`. The added velocity square is exactly

`DeltaSigma(d zetadot+b_r u)²`.

The Hv_r normalization and scalar/metric one-derivative terms do not affect this Hessian. No dynamical radiation field is eliminated as an auxiliary in the following Schur test. The density used in B is the declared bare P(Y) function, not a claim that the new interacting radiation stress remains separately minimal off the chosen history; the operator changes its perturbation dynamics. No physical photon or recombination dictionary is supplied.

## Exact finite capacity

Write D=DeltaSigma>0, C=C_r>0 and v=zetadot. The retained two-velocity form is

`A_old v²+C u²+D(dv+b_r u)²`.

Its radiation diagonal is `C+D b_r²>0`. Completing its velocity square gives the exact clock Schur coefficient

`A_new=A_old+D d²C/(C+D b_r²)`.

The gain is strictly increasing in D with derivative `d²C²/(C+D b_r²)²`. If b_r≠0 its supremum is `d²C/b_r²`, attained only in the infinite-D limit. On the upper branch let `A_old(0)=−a`, a>0. Then

`A_new(0)>0 iff D(d²C−a b_r²)>aC`.

A positive finite D therefore exists if and only if `d²C>a b_r²`; its threshold is `D>aC/(d²C−a b_r²)`. Equality of capacities cannot give a positive finite coefficient. At b_r=0 the gain is unbounded and the same threshold reduces to D>a/d². These conclusions concern the nonzero-k constrained system's formal p→0 coefficient, not a separate homogeneous k=0 gauge-sector elimination.

For strict capacity failure with b_r≠0, the supremum is itself negative: `−a+d²C/b_r²<0`. The original positive acceleration contribution proportional to p² cannot cure all sufficiently small nonzero p. Indeed a small-p interval can be chosen uniformly over all positive finite D using this strict negative gap. Whether a physical box or initial spectrum contains those modes is a distinct question. Positive Schur capacity is not full gradient or mode-growth health.

## Correct background conversion

Let x=a_FRW/a_fold, `r=r_fold x^(−4)`, `d_f=1−4r_fold/3`, and h=H/H*. From the retained charge relation

`q proportional to x³(h−1)`, `rho_r proportional to x^(−4)`.

Since B=q²/2,

`b_r=4rho_r q_rho/q=−d ln q/d ln x`

`=−[3+h_ln_x/(h−1)]`.

There is no factor 1/2. This gives early radiation b_r→−1 and early dust-limit b_r→−3/2. Using `Theta=M H*(h−eta)` yields

`d²=1/[H*²(h−eta)²]`, `C_r=12M H*² eta r`,

`a=3M eta(h−1−eta)/(h−eta)²`.

The M cancellation in d² is also essential. The exact dimensionless criterion is therefore

`4r>(h−1−eta)b_r²`.

I reconstructed both corrections from the raw scalar-density and background-current definitions; they are not accepted merely because their numerical verdicts match earlier versions.

## Universal small-radiation family obstruction

At r_fold=0 and any fixed x<1, the upper dust background is the unique t>1 solution

`g_eta(t)=L(t)+eta(t−1)²/2=L(x^(−3))`,

`t=(h−1)/eta`, `L(t)=t−ln t−1`.

Its derivative is `g_eta'(t)=(t−1)(1/t+eta)>0`. For any fixed eta>0 the early dust asymptotic follows directly from the leading quadratic/background density terms:

`h~sqrt(2eta)x^(−3/2)`, `h_ln_x/(h−1)→−3/2`.

Choose a sufficiently small but fixed finite x0<1 so that the dust-limit upper state has `h0>1+eta` and b0≠0. This is possible because b0→−3/2. At this x0, the implicit derivative in h is nonzero, so the upper h and its ln-x derivative depend continuously (locally analytically) on r_fold near zero. Hence b_r also tends to b0. The capacity difference tends to

`4r−(h−1−eta)b_r² -> −(h0−1−eta)b0² <0`.

Continuity yields a strictly negative interval for all sufficiently small positive r_fold. Choose its size below 3/4 to retain positive dust d_f. This proves the quantifier `for every fixed eta>0, there exists a small positive radiation interval and a finite epoch of failure`. It does not require the zero-radiation theory itself to carry a radiation perturbation pair or a uniformly regular designer function B as r_fold→0; only the background h,b_r and the finite-positive-r capacity formula are continued. It also does not claim failure for every radiation fraction.

## Endpoint controls and intermediate nature

For every fixed positive r_fold, the actual sufficiently early branch is radiation dominated:

`h~alpha x^(−2)`, `alpha=sqrt(2eta r_fold)`, `b_r→−1`.

Its capacity ratio behaves as `4r_fold/(alpha x²)→infinity`. Near the fold let s=ln x. The two matched minima give

`h−(1+eta)~−eta sqrt[(9+4r_fold)/(1+eta)] s`

on its upper side s<0. Thus h_ln_x and b_r have finite fold limits, while h−1−eta→0 and r→r_fold>0; capacity holds near the fold. These facts make the small-radiation failure an intermediate-epoch obstruction and prevent endpoint-only acceptance of the proposed operator.

The fixed-eta family claim uses an upper branch with h>1+eta, so Theta is nonzero even for eta>1. It does not assert that the complete later history avoids a Theta crossing outside this upper interval; the original complete cosmological-health scope remains separate.

## Final computation audit and limits

The final corrected script's symbolic Schur, derivative, saturation, threshold and background conversion implement the derived identities. Its 70-digit bisection examples at eta=.5,x=.5 give capacity ratios approximately `.00302410854` for r_fold=.0001 and `9.64432211` for r_fold=.25. The first fails and the second passes the finite-epoch capacity test; neither establishes a full history by sampling. These are not interval certificates and are unnecessary to the universal continuity proof.

I inspected final main_c output (nine implemented assertions pass) and separately validated both main_c and intended-failure control_universal_c manifests against current input/output hashes. Historical a/b records are superseded; their old numeric ratios are not used. Validation certifies recorded execution provenance, not the universal theorem or full gradient stability. No Boltzmann hierarchy, recombination dynamics, source matching, fixed-coupling vacuum adjustment or 32pi selector follows.

- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/radiation_schur_bound/REPORT.md`: `274ca5eb5799b3456648c94ec33463571ef68e4d31e4d67b4d041f8fc0ac8681`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/radiation_schur_bound/checks.py`: `250c1cec31e72c3d767e151494666739831fde91c1710c85d5be8555090aed22`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/radiation_schur_bound/runs/main_c/results.json`: `b504233eabb751c117c2701421154565baecf7a05a470a9b145d6adfa081b46d`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/radiation_schur_bound/runs/main_c/manifest.json`: `856a1f442a98655c5b4b839b55bfe9f950b6c1a9c9787405e7026d66de3195e4`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/radiation_schur_bound/runs/control_universal_c/manifest.json`: `5327b8b07c8a0efe586e98fc7842a798e4914d4ebed376baa8377b5441881bb1`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/perturbations/REPORT.md`: `c5fdf8222e9ea93d13a59255c212a00b39b9911b091495ef4919d96f8d966a15`.
- `sol61_push/recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/radiation_extension/REPORT.md`: `61982a07d83a0a3f672d799a5f4a33b814b35e6816ea97d72414cd24ea0790db`.

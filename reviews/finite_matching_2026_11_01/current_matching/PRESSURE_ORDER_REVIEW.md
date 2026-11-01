# TP03 pressure and order bookkeeping: exposed-input cross-review

**Claim reviewed.** `../pressure.py` combines the full finite vacuum graph result, known heavy-field elimination and actual one-loop angular-current coefficient into the local rotating-phase grand potential through the stated order, then calculates the pressure/IR response with finite root controls. `../ORDER_AND_STATE.md` and `../CURRENT_PULLBACK_AUDIT.md` specify its scope.

**Verdict: correct only after the stated finite-order/local-state restrictions.** I find no missing same-order homogeneous occupied term within the declared expansion and no Legendre-transform or current-normalization error. The finite radial kinetic coefficient is not needed to calculate the homogeneous equation of state. It is needed, together with gradient/current matching, to turn that equation into a complete dynamical action and to assess finite-wavelength modes. The calculation remains a specified weak-coupling, fixed-gauge/subtraction, connected rotating state, rather than a physical halo or an all-orders exclusion.

Prior exposure is material: I authored `current.py` and the earlier native-phase thermodynamic calculations, so this is **not an independent audit of those inputs**. I freshly checked the coordinator's composition, order counting, numerical iterator and current-pullback identity. Independent algebra review of the current graphs is a separate evidence item. No coordinator code or earlier input was changed by this review.

## Grand potential, Legendre transform and subtraction

The retained action uses q=omega² and

    Omega=V-Fq-Jq²/2,
    V=V0+V1+V2_diagrams-(CWa²/Haa+CWb²/Hbb)/2,
    F=F0+deltaF_current-CWb F_b/Hbb,
    J=F_b²/Hbb.

The three heavy terms are the expansion of one square. `pressure.py:48–53` includes each once; the direct current graph result excludes the heavy geometric term, so there is no double counting. Omitting V0 in the numerical evaluator is legitimate here because it is field independent at fixed couplings and the reported energy and pressure are vacuum-subtracted. The reference subtraction at the *scheme's own* zero-charge minimum is consistently used for both quantities.

At fixed omega, stationarity is Vs-Fs q-Js q²/2=0. The code's rationalized positive small-q root is correct under its explicit Vs,Fs/discriminant tests. Put

    N=Omega_ss,
    C=-Omega_omegaomega=2F+6Jq,
    M=Omega_somega=-2omega(Fs+Js q),
    D=epsilon_ss at fixed n=N+M²/C,
    n=-Omega_omega=2omega(F+Jq).

On the stationary branch dn/domega=C+M²/N=C D/N. Hence c_IR²=n N/(omega C D), exactly as implemented at lines67–71. The pressure and energy formulas

    P_ex=Fq+Jq²/2-V+Vvac,
    epsilon_ex=Fq+3Jq²/2+V-Vvac

follow directly from P=-Omega+Vvac and epsilon=Omega+omega n. The direct numerical P(n) check at1.05 is a genuinely different route to the same thermodynamic derivative; its maximum recorded error is about1.4e-6.

For positive C,D,n,omega the N=0 pressure boundary is distinct from D=0 radial instability. A small IR sound speed at that boundary does not imply small w_ex. The driver correctly reports both. A finite radial coefficient can change a gap and the wavelength range of validity, but it does not alter this Legendre transform or rescue a negative thermodynamic susceptibility. An assumed positive radial metric remains an interpretation hypothesis for the ordinary dynamical sound branch.

## Same-order occupied terms

Introduce formal loop order: V1 is one loop, q scales as one loop on the radiatively lifted nonzero-source branch, and the one-loop normal sources are of that same order. Then V2, q deltaF_current, the cross term from CWb times q F_b, and the tree-induced Jq² are all second order. The code retains them all. The one-loop current evaluated after a one-loop heavy displacement would change the energy at third order, as would a one-loop correction to the heavy Hessian in the quadratic displacement term. Cubic heavy-displacement terms are also third order.

The explicit equal-coupling scaling at fixed scaled X and Q²/e is consistent:

    m_tree² proportional to e, F0 proportional to e^(-1),
    V1 proportional to e²/L, V2 proportional to e^4/L²,
    deltaF proportional to e/L, J proportional to e^(-2),
    q proportional to e³/L, L=16pi².

An ordinary one-loop omega^4 graph has coefficient of order1/L times a function of the fixed dimensionless spectrum, so it contributes e^6/L³ here, beyond the retained order. A gapless free-occupation omega^4 term likewise does not become a missing second-order term merely because its threshold is zero; its nonlocal/IR dynamics are nevertheless not controlled by this counting. The document appropriately disclaims a uniform bound over arbitrary fields, momenta or occupations.

The homogeneous commuting phase background has no classical gauge-charge source: for normal diagonal A and B, the gauge moment of the common B phase vanishes. Thus no extra classical nonzero A0/Gauss-law solution was omitted from this invariant rotating ansatz. Other occupied or noncommuting states would be different problems.

Solving the truncated algebraic action exactly resums some higher-order algebraic terms; it is acceptable as the declared finite model, but those terms do not estimate the uncomputed remainder. No all-order accuracy or universal state conclusion follows from that exact algebraic solution.

## Current-pullback scale identity

At fixed retained X, F0=X²+30(hX/lambda)². One-loop running gives

    D1_reduced F0=-2gammaX X²-60gammaB_chiral b².

The actual graph current instead has partial_lnQ deltaF_current=2gammaX X²+60gammaB_component b². The difference is supplied by the computed heavy pullback,

    partial_lnQ deltaF_heavy=-300g²b²/L
       =60(gammaB_chiral-gammaB_component)b².

This agrees with the off-valley component potential CS equation differentiated at fixed raw b, then divided by the raw Hbb and multiplied by F_b. The b-chart normalization is consistent; a canonical mass eigenvalue was not substituted for that raw curvature. At the inherited critical equal-coupling comparator the required combined derivative happens to vanish, so the v2 numerical check correctly normalizes cancellation errors by the sizes of the individual terms. The first normalization-by-zero failure was preserved rather than hidden. Recorded combined residuals are at most5.79e-12 in that normalization. This is a nontrivial composition check, not a proof of a full radial effective action.

## Numerical coverage and current endpoints

The iterator really performs48 pressure cases: two coefficient grids(21,29 Chebyshev nodes), two couplings(.01,.03), four declared compositions, and three actual root stencils(.01,.005,.0025). This improves on the earlier fixed-root derivative-repeat-only check: each root is solved again at each stencil. The full coefficients are checked directly at three off-node positions at both couplings; the largest recorded relative coefficient/scaling error is3.16e-10. These finite checks are not interval certificates.

The interpolation region contains the complete root/stencil range used here. Exact equal-coupling scaling is appropriate at fixed Q²/e and is separately checked at the off-nodes. The baseline one-loop CW function is evaluated at its default scale, while the complete finite functions use the fixed stated Q; the inherited critical relation makes the one-loop explicit scale shift vanish through STr M4=0, so these agree in this model.

At the finest grid/stencil, the fully matched endpoints are:

| e | X/Xmin | w_ex at endpoint | c_IR² at1.2 | c_IR² at1.3 |
|---:|---:|---:|---:|---:|
| .01 | 1.2139437203 | .6141473 | +.0789553 | -.5603835 |
| .03 | 1.2181863885 | .6091668 | +.0981381 | -.4940415 |

All recorded endpoint/sample C and D are positive. The maximum last-two-stencil root change is3.25e-11; changing21 to29 coefficient nodes changes roots by at most3.21e-10. These numbers support the displayed finite-order endpoint stability, not an all-order physical precision claim. The pressure-rich endpoint and later negative sound sign remain finite outcomes of these declared states.

One diagnostic needs a narrow reading: `omega2_over_heavy_mass2` uses the tree singlet mass square2e. It is not the minimum positive mass among every scalar/fermion/SV threshold in the current diagrams. Its tiny value is useful, but does not by itself certify the derivative expansion against all lighter adjoint modes or the gapless sectors. A complete dynamical interpretation would compare the actual relevant thresholds and compute/bound the nonlocal terms; this limitation does not change the homogeneous thermodynamic identities above.

No forced implementation correction was found. The appropriate claim is a complete named finite vacuum/current contribution through the declared order on this local phase state, with independent finite controls, and with the stated higher-order, IR, current-lifetime and gravity obligations left open.

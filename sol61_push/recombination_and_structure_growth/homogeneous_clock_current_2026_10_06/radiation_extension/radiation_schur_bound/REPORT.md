# Exact radiation budget for the density-square clock repair

Base: 36b9957612c8b422e900874fb053c6baa22456e4. This is a root derivation from the parent conserved radiation background and actual quadratic action. It tests the proposed radiation-density square; it does not select 32pi or identify a physical photon interaction.

Let Delta L=Z(rho_r)[X-B(rho_r)]²/2, X=q²/2, rho_r=3lambda Y², and B equal the chosen background X as a function of its monotone radiation density. Put DeltaSigma=Zq⁴/2>0, d=M/Theta, and b_r=4rho_r B'/q². Because delta rho_r=4rho_r(v_r_dot-Hv_r-nu), the added quadratic term is

    DeltaSigma[(1-b_r)nu+b_r(v_r_dot-Hv_r)]².

The square has no shift perturbation at first order, so the actual parent shift equation is unchanged. Retaining only the velocity Hessian after that constraint, define u=v_r_dot-d zeta_dot. The two propagating velocity variables have quadratic form

    A_old zeta_dot²+C_r u²+DeltaSigma(d zeta_dot+b_r u)²,
    C_r=2rho_r>0.

The radiation diagonal C_r+DeltaSigma b_r² is positive. Eliminating its velocity mixing gives the exact clock Schur coefficient

    A_new=A_old+DeltaSigma d² C_r/(C_r+DeltaSigma b_r²).

This is a velocity-Hessian calculation, not algebraic elimination of the dynamical radiation mode. Dust retains its first-order density-momentum pair. For b_r!=0 the added Schur contribution has the finite upper bound d²C_r/b_r², regardless of how large Z becomes. The radiation carries this budget because the interaction changes its velocity mixing as well as the lapse coefficient.

On the upper conserved branch h>1+eta, set a=-A_old(p=0)=3M eta(h-1-eta)/(h-eta)²>0. A positive finite square can make this formal zero-wave-number Schur coefficient positive if and only if

    d² C_r>a b_r²,
    DeltaSigma>a C_r/(d²C_r-a b_r²).

Equality in the first inequality never suffices at finite DeltaSigma. For b_r=0 the same inequalities apply without a finite saturation ceiling. Since A_old(p)=A_old(0)+kappa M p²/[Hstar²(h-eta)²], this is sufficient to lift the coefficient for every finite p, and failure with a strict negative limiting value obstructs sufficiently small nonzero p. It does not establish which modes a finite cosmological box or an EFT admits, nor full gradient stability.

Write x=a_FRW/a_fold, r=r_fold x^-4 and d_f=1-4r_fold/3. The background has q proportional to x³(h-1), rho_r proportional to x^-4. Thus

    b_r=-(3+h_ln_x/(h-1)),
    C_r=12M Hstar² eta r,
    d²=1/[Hstar²(h-eta)²].

The exact capacity criterion becomes

    4r>(h-1-eta)b_r².

It is not automatic. At any fixed upper-branch x where the dust-only limit has b_r!=0, the right side remains strictly positive as r_fold tends to zero, whereas 4r tends to zero. The analytic implicit upper branch is continuous in r_fold at such x: its h derivative is positive away from the fold. Such x exist, since the dust-only early branch has h~sqrt(2eta)x^-3/2 and b_r tends to -3/2. Consequently, for every fixed eta>0, sufficiently small positive radiation fractions give at least one finite epoch where no positive square of this form can repair all sufficiently long wavelength clock coefficients. This is an analytic family obstruction, not a finite grid claim.

Conversely, at every fixed r_fold>0 the radiation-dominated early branch has h~alpha x^-2, alpha=sqrt(2eta r_fold), b_r->-1, and the capacity ratio

    4r/[(h-1-eta)b_r²]~4r_fold/(alpha x²)->infinity.

At the fold h approaches 1+eta with a finite h_ln_x and b_r, so the capacity criterion also holds in a sufficiently small upper-branch neighborhood. For small radiation fractions the obstruction therefore occurs at intermediate epochs, even though the early and fold limits admit a repair. This rules out judging the operator only from those two limits.

checks.py independently verifies the exact Hessian, saturation and threshold algebra. A 70-digit calculation illustrates a finite on-background failure at eta=1/2, r_fold=1/10000, x=1/2; bisection and residuals are recorded. This numerical illustration is not an interval certificate and is not needed for the analytic small-radiation theorem. A companion illustration with r_fold=1/4 at the same epoch passes the capacity condition; it does not prove global health of that history.

This analysis does not test the principal gradient matrix, source matching, vacuum self-adjustment, atomic recombination or free-streaming photons. Those remain separate obligations. The proposed radiation-square author is calculating the full constrained characteristic in a separate sibling folder. The underlying logKGB route extends the Claude-motivated cutoff/clock work already audited in sol61_push; the new square is a proposed extension rather than a result attributed to Claude.

Execution correction: main_a exposed an erroneous extra M in the d² substitution used for the background-dictionary check. Since Theta=M Hstar(h-eta), d² has no M. That check and the displayed dictionary were corrected; the capacity inequality and numerical illustrations are unchanged. main_a/control_universal_a are retained as superseded runs whose input hashes are historical. main_b/control_universal_b use the corrected inputs.

Independent-author correction: the radiation-square raw action exposed a sign error in the displayed deltaF square and a factor of two in b_r=density conversion. The correct deltaF is -q²[(1-b_r)nu+b_r s_r], and b_r=-d ln q/d ln a. The Schur formula and symbolic capacity criterion depend only on b_r² and remain correct; the earlier numerical ratios and limiting constants were four times too large. The analytic family obstruction and the two example verdicts survive. main_b/control_universal_b are superseded; main_c/control_universal_c use corrected final inputs.

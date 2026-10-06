# Independent raw radiation/shear constraint audit

Accepted within the frozen Q=1, n=3 principal-action scope. I reconstructed the fluid/shift completion, three algebraic constraints, evolving time boundary and physical two-mode principal symbol independently before using the author’s check output. There is no blocking algebra correction. This is evidence for a high-frequency gradient instability of the retained arithmetic projected operator on this admitted branch, not a bare-lapse ghost argument or a general finite-momentum health theorem.

## Inspected evidence

Observed author provenance HEAD: `f2c6144f842b9d56b61781d7399e598a1328a726`. Frozen inspected SHA-256:

- REPORT.md: `df1df0faa1a4ff8abdf82cac3e386f79c8f0b1d555a409a378729214c9abbcf2`
- checks.py: `6004f297a23e58eb9cdaa36874055390487f358220516201ad0c04945491ba31`
- contract.json: `8876e2db10077647d8d9916ad448d907a7d20f6627034d8268aea90cbd736a18`
- provenance.json: `c8200c45618d8a94104c0613abd1cc168796ee5f7f8e5423031d5d991791c407`

Also inspected inherited matter, shear-repair and actual FRW reports, with their hashes recorded in the author provenance. The old eta=0 clock response constraint is not an admissible replacement for the new clock row. This peer file is outside execution inputs; no author input was changed.

## Action reconstruction and constraints

With individual Einstein coefficient M=2K, CY² gives rho=3C_r q^4/4, W=C_r q^4 and C_f=3W/2. Its scalar velocity coefficient is positive. The raw visible shift-dependent block is −3M f_g²−2M f_g t_g−eta M t_g²/3−W v t_g. Differentiation gives t_g=−3(f_g+Wv/(2M))/eta; the empty-hat row gives t_h=−3f_h/eta. Completing these squares must precede lapse reduction. The residual shear row sets Dvol=0; setting both spatial shears to zero would instead remove a physical relative row. Clock restoration has the different hatted factor L² P_h pi, consistent with normalized hatted lapse. The common diffeomorphism identity supplies the full clock row only after retaining the shear contribution.

The clean action stated in section 3 follows from the actual fluid boundaries. In particular, the visible cross term becomes −2A Tw n_g because 2C_f=3W: the extra H w and zeta_g terms cancel, rather than leaving another fluid-lapse mixing. Write the auxiliary ordering (n_g,n_h,u). Its coefficient matrix is

C=[[A+B+Gamma,−Gamma,g−Gamma ell], [−Gamma,D+Gamma,j+Gamma ell], [g−Gamma ell,j+Gamma ell,Gamma ell²]].

The displayed report matrix is the same matrix in its (u,n_g,n_h) ordering. Direct variation reconstructs the linear vector and all three rows. The background used for the fixture is genuinely on shell: H²=h²+rho/(3M), Hdot=−W/(2M), L=a³/b³ and H2=Lh. The integration constant for b³ is set with a common choice of integral origin; the a=1,b=2 fixture has H=sqrt(2), rather than an arbitrary frozen H.

## Independently reconstructed principal symbol

Let alpha=g/(g+j), r=j/(g+j), T=gj/(g+j) and s=T/Gamma. The leading spatial auxiliary determinant is −Gamma(g+j)², hence invertible in the positive stated domain. Its solution is u=−alpha chi, n_g=−rY−r(2alpha ell+s)chi, n_h=alpha Y+alpha[(alpha−r)ell+s]chi. Substitution gives the spatial part

−2T chi Y−T(2alpha ell+s)chi².

A fixed-background freeze at this point would give the wrong answer. Integrating −2T chi chi_dot yields +T_dot chi², and the actual background gives T_dot/T=r(H−e)+alpha(2ell+H2). The ell terms cancel. The surviving velocity form is A(w_dot+r chi_dot)²+(B r²+D alpha²)chi_dot², with both coefficients strictly positive. Terms containing undifferentiated w or chi and derivatives of r are lower principal terms.

The gradient matrix has Gww=g e, Gwchi=T e, Gchichi=T[s−r(H−e)−alpha H2]. Under R=w+r chi its off-diagonal term cancels since gr=T. Thus the two physical principal frequencies are P_g/3 and

omega_rel²=−P_g P_h(P_g−P_h)²/[b0(P_g+P_h)(P_h²+P_g²/L²)], b0=3(1−eta)/eta>0.

I obtained the negative square directly from g=M a³ P_g H, j=M a³ P_h H2 and Gamma=M a³(P_g+P_h)/4. It vanishes only when P_g=P_h on this positive domain. For L=1/8, P_h/P_g=1/4 and eta=1/4, c_rel²=−1/5125. Radiation retains c_s²=1/3. This is a physical reduced direction with positive high-k kinetic and negative gradient, not an auxiliary variable’s sign. On a compact interval with strict mismatch, the retained continuum operator admits a high-frequency local growing characteristic whose rate can exceed background rates. A physical EFT cutoff is still required to decide whether that regime is available in an application.

## Finite-k caveat and coefficient discriminator

A separate reconstruction gives the full velocity-plus-auxiliary determinant −A Gamma(B j²+D g²), and therefore det K_reduced=−A Gamma(B j²+D g²)/det C wherever the auxiliary chart is invertible. At small k with ell nonzero, det C starts +Gamma ell²(A+B)D; at large k it starts −Gamma(g+j)². A finite chart rank loss follows by continuity. This does not by itself prove a physical singularity or an IR ghost: the original constrained/canonical system needs a separate analysis there. The report properly avoids promoting the ultraviolet Gram form to all finite k.

For a different positive Gamma with the same high-k scaling, zero relative stiffness requires Gamma_crit=T/(rH+alpha H2)=M a³ P_g P_h/(P_g+P_h). The arithmetic gap is M a³(P_g−P_h)²/[4(P_g+P_h)]. This is a valid algebraic discriminator, not an already admitted changed covariant action. No general-Q or general-n result is pooled into this frozen Q=1 conclusion.

## Bounded records and remaining implications

I independently ran the standard manifest validator on main_b, control_mismatch_b, control_shift_b and control_boundary_b: all four are valid against the current inputs. Main records 28/28; each control records 28/29 with its deliberate rejection assertion. These outputs support exact identities only. The revised shift control inserts the actual old eta=0 row f_g=−Wv/(2M) and tests whether the new shift Euler equation vanishes: its residual −2M eta t/3 correctly rejects the transplantation. It is a row-level mutation, not a newly solved alternative full-action theory. Historical a checks included an unnecessary +1 rejection assertion; that input was archived and superseded by b, not pooled with current evidence. The mathematical verdict above comes from the raw reconstruction, not the check count.

No atomic photon transport, cold material abundance, source/halo matching, all-mode health, finite astrophysical instability timescale or A/32pi selection follows from this audit. The ordinary fluid is an ideal CY² radiation control, not a thermal-photon recombination calculation. The next necessary arrow for this operator is an actual physical cutoff or separately varied repair with its own radiation constraints.

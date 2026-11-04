# AZ24: the nonlinear cusp has a branch-domain constraint

κ = ½ FITTED; not theory closed

**PASS** for the scoped nonlinear constraint derivation; **FAIL** for unrestricted extrapolation of AZ23 into this one-sided cusp; **NO VERDICT** for nonlinear late-time selection; **NOT EVALUABLE** for physical κ. Both canonical and alt have these verdicts. No whole requirement or RQ3 row is earned. Criteria were committed as 5c2a9d48ed before computation.

This calculation attacks the original nonlinear action. It does not append an arbitrary cubic term to the linear Green equation. The result exposes a missing branch of the physical evolution problem, rather than finding b=1.

## Exact plane-symmetric constraints

Use the inherited foliation action with c1=−C1, c2=−C2, C1,C2>0. Set spatial metric gamma_ij=a(t)^2 exp(2ζ) delta_ij, lapse N>0 and shift (v,0,0). In this section x is a spatial coordinate, not the invariant displacement. Define

    T = (H+ζdot−v ζ_x)/N,   w=v_x/N,
    K=3T−w,   Qkin=Kij Kij−K²=−6T²+4Tw,
    R3=a^−2 exp(−2ζ)(−4ζ_xx−2ζ_x²),
    g²=a_i a^i=a^−2 exp(−2ζ)(N_x/N)²,
    I=(−C2 K²+C1 g²)/m².

The exact reduced gravitational action density is B N a³ exp(3ζ)[R3+Qkin+m²F(I)]/2. This is a plane-symmetric sector, not a spherical galaxy solution or a proof about all perturbations.

For zero matter momentum density, shift variation gives

    ∂_x[c2 F'(I)K−2T] − 2ζ_x w = 0.

The second term is a nonlinear connection contribution. Omitting it is a genuine mutation, with residual −2ζ_x v_x/N. With a reference de Sitter boundary (K0=3H, T0=H), define the momentum functional

    E = T−H + integral_from_reference^x ζ_x w dx.

Then the integrated constraint is c2[F'(I)K−F'(I0)K0]=2E. Boundary integration constants must be retained if a de Sitter reference is unavailable. A matter momentum density would add its integral; we have not set it to zero in a general evolving galaxy. For AZ23's infinitesimal comoving probe it vanishes at first order, which is the only order used in the source test below.

The lapse variation gives the independent Hamiltonian constraint

    R3−Qkin+m²F−2c2 F'K²+2c1 F'g²
      + (2c1/sqrt(gamma)) ∂_x[sqrt(gamma) F' gamma^xx N_x/N]
      = 2ρ/B,

where ρ is the matter energy density measured by the foliation normal. This recovers 3H²=m²(2I0 F'0−F0)/2 in vacuum. Neither constraint uses division by F'' or 2−alpha.

## Nonlinear inversion, retaining the free width

On the specified source side, let q=sqrt((I−I0)/xa)>=0 and write A=a_M, with xa=C1 A²/m². The inherited interpolation is

    F'(I)=2/[C1(1+q)],
    F(I)=F0+(4xa/C1)[q−ln(1+q)].

Define J=K0−C1 E/C2. The momentum equation fixes K=J(1+q). Substitution into the invariant yields the exact algebraic equation

    (C1 A²+C2 J²)q² + 2C2 J² q = S,
    S=C1 g²+C2(K0²−J²)
     =C1[g²+2K0 E−(C1/C2)E²].

The left side is strictly increasing for q>0, starts at zero, and tends to infinity. Hence a nonnegative root exists uniquely **if and only if S>=0**. This is a nonlinear admissibility condition, not a numerical stability heuristic. For S>=0 it can be evaluated without cancellation as

    q = S / [C2 J²+sqrt(C2² J⁴+(C1 A²+C2 J²)S)],

with the trivial S=J=0 endpoint defined by q=0. Near the expanding background J>0. The result follows from the original momentum constraint and invariant; it is not the old spherical approximation F'K=constant.

For E=epsilon E1 and g=epsilon g1,

    S = 2C1 K0 epsilon E1 + O(epsilon²).

Thus a generic negative E1 leaves the declared cusp side for sufficiently small positive epsilon. Increasing or selecting A does not repair that sign: A is absent from S.

## The AZ23 source probe does leave that side

AZ23's conserved-source particular solution was ζ_p=Q y³/12, n_p=−ζ_p, y=k_com/(aH), Q>0 at a positive source phase. At first order E=U=ζdot−Hn. Therefore

    E_p = −H Q y³/6 < 0.

The acceleration squared is second order in probe amplitude. At fixed finite time and wavelength, the leading S is consequently negative. At a spatial source maximum its first-order gradient also vanishes. This particular solution of the formal linear system cannot be continued into the specified I>=I0 nonlinear branch. Homogeneous modes can change E; this is not a proof that every initial condition fails, nor that no nonlinear solution exists.

AZ23 remains an exact inverse of its stated **conditional linear operator**. Its physical use now needs an additional restriction: one must establish the branch on which its source and initial data lie. The critical-endpoint record already noted that homogeneous matter explores the opposite side. This calculation extends the issue to the finite-wavelength, time-dependent source and gives its nonlinear domain test.

The inherited source-side formula does not specify the full opposite-side evolution. A regular opposite branch need not have the same limiting scalar kinetic coefficient as the singular source branch. Assuming C=6 there, extending q to a negative square root, or clipping S to zero would each add a physical prescription. None was done. Consequently an arbitrary nonlinear Green-function simulation at this point would not test the declared action.

## Does any endpoint equation select b or κ?

No endpoint selection was found. The exact de Sitter equations use F0 and F'0, while the source width xa remains absent. This common-background statement is weaker than constructing a family of globally healthy sourced cosmologies; no such family is claimed.

For orientation only, if the old MOND source window and tensor Newton calibration were valid, rho_vac=3BH², G=1/(8pi B), and c=1 would give

    κ_conditional=(A/H)sqrt(8pi/3),
    b_conditional=(H/(2A))sqrt(3/(8pi)),
    κ_conditional=1/(2 b_conditional).

This is a dictionary, not a selection equation. A is still an action parameter, not a field with an evolution equation. Nothing derived here sets A/H, makes b flow, or establishes a universal late-time sourced response independent of A. In particular, imposing b=1 would still insert the requested value.

## Evidence, failure preservation and next calculation

`results.json`: **17/17** checks pass, including direct shift/lapse action variations, homogeneous vacuum and zero-source controls, integrated cusp derivative, branch equation, first-order domain, source sign, and two finite Lean witnesses. Both mutations bite. The exact negative-domain rational witness has C1=C2=K0=A=1, E=−1/10, g=0; its equation is (q+1)(221q+21)/100=0, strictly positive for q>=0. These are dimensionless algebra controls, not fitted physical parameters or a scan. Lean checks the finite rational witness only; it does not certify the physical nonlinear PDE or κ.

Initial execution passed 14/17 checks. It exposed two implementation defects: structural substitution missed SymPy's algebraically rearranged derivative argument, and ordered substitution left K0 inside the inserted vacuum expression. `initial_run.py` and `initial_results.json` retain that failure. The repair explicitly proves equality of each derivative argument before substitution and substitutes K0 inside the vacuum expression before insertion. The physics, frozen criteria and tested equations are unchanged. This is a self-review, not an independent audit.

Next required calculation: specify a physically justified opposite-side F and matter evolution, derive the coupled lapse/shift/metric system across the cusp, and test branch crossing and existence before late-time normalization. Choosing that continuation just to land on b=1 is not acceptable. A two-sided mathematical completion could be explored as an explicitly unselected model, but would not supply the missing physical principle by itself. The full late-time question remains open; this lane does not prove impossibility.

All H,B,m,C1,C2,xa, boundary data and any assigned source amplitudes remain unselected/FITTED. No new data, particles, cold component, scan, heavy simulation or push. Reproduce with `python3 astra_goal_2026_11_03/P3/AZ24_nonlinear_cusp_constraints/run.py`.

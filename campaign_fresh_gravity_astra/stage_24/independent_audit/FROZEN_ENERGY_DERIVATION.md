# Independently frozen FGF037 energy-domain test

Derived from task037 and the pinned Q action/crossing/weighted theorem, before any new author/root proof or formula preview. Proof-only; no mathematical computation.

Fix one accepted short interval, rho>0, chi and hence a(x) bounded above/below positive, signed g=phi', signed MOND B=sgn(g)b(|g|,a), B'=C rho. Keep rho and chi unchanged in all tests. The exact phi-dependent energy is E(phi)=int[rho phi+W(|phi'|,a)/C]; the internal-fluid and scale terms are unchanged and finite. This is a fixed-wall, fixed-mass admissible control of the FULL static energy, not a deletion of its matter coupling.

## Exact growth and finite-energy domain

For s>=0, direct square-root inequalities give

    s-a/2 <= b(s,a) <= s,
    s²/2-a s/2 <= W(s,a) <= s²/2,
    s²/4-a²/4 <= W(s,a) <= s²/2.

The second lower bound follows by completing a square. Also W>=0. On a finite interval with bounded a, int W(|v|,a) is finite iff v is L2. Thus for a fixed finite-energy g, finite new field energy is equivalent to psi' in L2. A finite trace or bounded weighted-space representative then puts psi in ordinary H1; with fixed zero outer perturbation values it is H1_0. This is the exact phi-sector finite-energy characterization under the fixed bounded-positive a premise, not a full nonlinear fluid-domain theorem.

Let F_x(z)=W(|z|,a(x)); F_x'(g)=B and F_x''(g)=A. Convexity gives D_x(t)=F_x(g+t)-F_x(g)-Bt>=0; since 0<=F_x''<=1, D_x(t)<=t²/2. At the actual background and any globally AC zero-outer-trace psi with integrable terms,

    int B psi'=-int B'psi=-C int rho psi.

Therefore full energy increment for finite-energy perturbations is int D_x(psi')/C. This is exact cancellation with the interaction, using MOND B', not g'. For a singular direction the same linear integrals exist, but it is only a formal first-variation cancellation; it does not confer finite nonlinear energy.

## One singular weighted direction

Use the reciprocal-A coordinate s(x)=int_left^x 1/A. Choose v(s) smooth compactly supported, with nonzero constant derivative kappa near the central s0, and set psi=v(s(x)). This is a globally AC zero-trace element of V_A. Near zero, psi'=kappa/A~kappa/[a_A sqrt(|x|)], so int A psi'²<infinity but int psi'² diverges logarithmically. No center wall or discontinuity is inserted. For every nonzero epsilon, g+epsilon psi' is not L2 (g is L2), hence the exact field energy is infinite by the growth bounds. psi is bounded, int rho psi is finite, and B psi'~constant*sgn(x)sqrt(|x|) is integrable. Interaction and linear subtractions cannot cancel the positive infinite field energy. xi=eta=0 is legitimate in the full form domain and keeps mass, density positivity and scale fixed. An arbitrarily small multiple of this direction is in any weighted norm ball; consequently no whole weighted neighborhood is a finite-valued nonlinear-energy domain.

## One smooth concentration: beta=1/2

Choose nonzero f in C_c^infinity(-1,1), fixed positive L_ref and potential unit Psi_ref, and dimensionless delta decreasing to zero. Set

    psi_delta(x)=Psi_ref delta^(1/2) f(x/(L_ref delta)).

The support is interior for small delta. It is smooth with zero outer trace, unchanged rho/chi and fixed mass. Its amplitude tends uniformly to zero. Exact derivative and norm scales are

    ||psi_delta'||²_2=(Psi_ref²/L_ref) int f'²,
    ||psi_delta||²_2=Psi_ref² L_ref delta² int f²,
    ||psi_delta'||_infinity=(Psi_ref/L_ref)delta^(-1/2)||f'||_infinity.

Since A(x)~a_A sqrt(|x|), its weighted second variation is

    Q_phi[psi_delta]~[a_A Psi_ref²/(C sqrt(L_ref))]
        delta^(1/2) int sqrt(|y|) f'(y)² dy ->0.

The weighted form norm therefore tends to zero, although the physical unweighted gradient L2 norm stays at a nonzero constant and the gradient maximum diverges. Choosing beta=1/2 isolates a finite nonzero exact energy limit rather than requiring a scan.

Use the direct bound |W(s,a)-s²/2|<=a s/2. On the shrinking support, g=O(sqrt(delta)), t=psi_delta'=O(delta^(-1/2)), so int |t|=O(sqrt(delta)), int |g|=O(delta^(3/2)), int |g t|=O(delta), and int g²=O(delta²). Uniform boundedness of a therefore yields

    int_support W(|g+t|,a) -> (Psi_ref²/(2L_ref)) int f'².

Background W integrates to zero on that shrinking support (indeed O(delta^(5/2))), and the exact matter interaction is O(delta^(3/2)). Equivalently the B t linear term has that order and cancels it exactly. Hence

    E(phi+psi_delta)-E(phi)
       -> [Psi_ref²/(2 C L_ref)] int f'² >0.

Each member has finite smooth energy. Nevertheless the energy is not continuous at the background even when restricted to smooth finite-energy perturbations with the inherited weighted topology. The Taylor remainder after the equilibrium linear term and one-half of Q_phi has the same positive limit. Its ratio to the squared weighted norm diverges like delta^(-1/2). There is not even a local O(||u||_V²) remainder estimate on these smooth controls, much less a uniform o(||u||_V²) Frechet second-order expansion. Ordinary directional second variations along fixed smooth directions remain compatible with this failure of uniformity. The singular weighted direction does not have a finite-valued Gateaux energy variation at nonzero amplitude.

## Exact surviving scope

FGF036's positive closed quadratic form, transmission operator and linear evolution remain valid as a LINEAR theorem. They do not by themselves furnish a finite nonlinear energy neighborhood in that completed topology. In this fixed-rho/chi sector, ordinary H1_0 for phi perturbations is necessary and sufficient for finite exact field energy; naming that stronger space does not prove C2 Frechet differentiability, a nonlinear inverse or nonlinear well-posedness. No instability/ghost claim follows from topology mismatch. Both a0 values, distinct frozen-H/constant-vacuum/actual evolving-H interpretations and Q-only scope are retained; no RAR/M, metric/photon, physical reservoir or empirical transfer is inferred.

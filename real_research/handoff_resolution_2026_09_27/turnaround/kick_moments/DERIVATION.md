# Exact isotropic kick moments within the existing daughter-shell closure

For v=(v_r,v_t,0), speed u=|v|>0, unit vector e=v/u and fixed kick speed k>0, write w=v+k n for uniform n on S². The source escape test is E=|w|²/2+phi>0. Its complement is mu=n.e <= c0=(-2phi-u²-k²)/(2ku). Equality on a circle has zero angular measure. Clip c0 to c in [-1,1]. The surviving fraction is f_b=(1+c)/2; conditional on survival, mu is uniform on [-1,c], and azimuth is uniform independently. Thus

    m1 = E[mu | bound] = (c-1)/2,
    m2 = E[mu² | bound] = (c²-c+1)/3,
    E[n_i | bound] = m1 e_i,
    E[n_i n_j | bound] = A delta_ij + D e_i e_j,
    A=(1-m2)/2, D=(3m2-1)/2.

The two moments needed by the unchanged engine closure are

    E[w_r² | bound] = v_r² + 2 k v_r m1 e_r + k²(A+D e_r²),
    E[w_t1²+w_t2² | bound] = v_t² + 2 k v_t m1 e_t + k²(2A+D e_t²).

For c=1 all directions bind: m1=0 and the kick adds k²/3 radially and 2k²/3 tangentially. For c=-1 the surviving population has zero measure; moments are undefined and the routine returns zero placeholders, which the existing engine ignores when removing the shell. If u=0 or k=0, all directions have the same energy. They all bind when (u²+k²)/2+phi<=0 and all escape otherwise, including the finite-measure E=0 degeneracy treated exactly as in the source. At u=0, the bound moments are k²/3 and 2k²/3. At k=0, they are v_r² and v_t².

No physical coefficient or distribution is fitted. The analytic rule is the infinite-angular-sampling limit of the specified one-step isotropic kick and energy cut. The engine still represents the entire retained distribution by one shell, sets its radial velocity to the old radial sign times sqrt(E[w_r²]), and assigns J=r sqrt(E[w_t²]). Those substitutions are the existing second-moment closure; they do not in general preserve the conditional vector mean, its dispersion separately, or the subsequent phase-space distribution. This work therefore does not turn the shell prescription into exact kinetic evolution.

`control.py` integrates explicit Cartesian kicks using a separate aligned coordinate basis and a 32-node Gauss-Legendre / 64-angle azimuth quadrature. It covers oblique, radial, tangential, all-bound, no-bound, zero-velocity, zero-kick and degenerate zero-energy cases. Main passes14/14. Mutation sets m1=0, leaving fraction and tensor formulas unchanged; exactly the three partial-bound second-moment controls fail (11/14 pass). An initial JSON serialization error for numpy booleans was corrected before these scientific controls and before launching any benchmark; it was not counted as mutation evidence.

`engine_exact.py` is a copied source with only the import, exact sampler replacement and optional trigger cadence (default5) changed; `engine_exact.patch` records every edit. Its historical docstring still describes the old64-direction rule because the copy preserves other source text. The unused RNG initialization remains and makes no draws in the benchmark. All original files are read only.

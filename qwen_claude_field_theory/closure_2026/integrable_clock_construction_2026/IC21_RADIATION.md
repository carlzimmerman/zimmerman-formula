# IC21: explicit radiation coupled to the IC20 action

Base `a5ffa5f3f3ebe592d1c6e63345e2304538628231`, 2026-09-09.
**Full theory OPEN.** No gravitational coefficient is changed in this work.
This advances the matter perturbation gate of the SAME IC20 action, not a
replacement model donating a radiation result. Carl Zimmerman's primordial
clock and vacuum-normalized exponential framework motivate this construction.
The vacuum-scale normalization remains imposed; no new observational fit or
global novelty claim is made.

## 1. Vary an actual matter action

Choose the concrete minimally coupled matter sector

    Sm = integral sqrt(-g) X_sigma²,
    X_sigma=-g^{mu nu} partial_mu sigma partial_nu sigma/2 > 0.

This is an irrotational perfect radiation fluid, NOT a Boltzmann photon gas
with anisotropic stress, not a photon-baryon plasma, and not recombination.
Its scalar equation is nabla_mu(2X_sigma nabla^mu sigma)=0. Its stress is
T_mu_nu=2X_sigma sigma_mu sigma_nu+X_sigma² g_mu_nu. Thus rho=3X_sigma²,
p=X_sigma². The standalone sound speed follows as
P_X/(P_X+2XP_XX)=1/3; it is not assigned to a coupled eigenmode.
Minimal coupling gives the ordinary matter Ward identity on sigma shell.

The constant pin conformal factor cancels from this four-dimensional action.
In barred coordinates with Nbar=exp(S), volume V=exp(3Q) and homogeneous
velocity v_sigma, its Lagrangian is V v_sigma^4/(4Nbar³). Variation gives

    P_sigma=V v_sigma³/Nbar³,
    Hrad=(3/4)Nbar P_sigma^(4/3)/V^(1/3),
    Hrad/V=(3/4)exp(S)j^(4/3)=h_r, j=P_sigma/V>0.

The fixed-momentum gradient coefficient is exp(S)j^(2/3)/2, obtained from
-partial L/partial |Dsigma|² before setting the background gradient to zero.
The background amplitude used in IC20 is Mr=(3/4)P_sigma^(4/3), so its
previous radiation background equations now have this explicit matter action.

The background solves h_S+h_r=0, h_z=0. Preservation and evolution use
the radiation-sourced IC20 equations, NOT the vacuum Sdot, qdot and zdot.

## 2. Matter enters the momentum constraint

Let fields be x=(zeta,delta sigma), and momenta p=(delta q,s), with
delta q=delta pi/V-3q zeta and s=delta P_sigma/V. Their symplectic density is

    V[2 delta q zetadot+s delta sigmadot].

For a scalar mode the spatial momentum constraint solves the trace-free
metric momentum amplitude as -delta q/2+3j delta sigma/4, giving

    |delta pi_TF/V|²=(delta q-3j delta sigma/2)²/6.

Leaving this source out would artificially remove the load-bearing coupling.
Background volume and symplectic terms now leave 2h_r zeta² rather than the
vacuum mass cancellation. These coefficients are derived and symbolically
checked in the script.

## 3. Coupled quadratic Hamiltonian, including lapse elimination

All h derivatives below come from IC20's h after eliminating z by its varied
equation: H_ab=h_ab-h_az h_bz/h_zz. Use the IC20 quantities

    a=t/6+H_qq/2, d=H_qR, C=H_Sq, e=H_SR,
    t=exp(2S)/v, B=m exp(S+2wc)(1-u_clock²),
    beta=exp(S)j^(-2/3)/6, u_r=exp(S)j^(1/3),
    Z=4e k²-4h_r, M=H_SS+h_r-2B k².

Do not confuse u_r with the gravitational auxiliary u_clock. For
H2/V=p^T K p+2p^T L x+x^T W x, first form

    K0=diag(a,beta),
    L0=[[2d k²,-t j/4],[-u_r/2,0]],
    W0=diag(-2v k²+8H_RR k^4+2h_r,
            3t j²/8+exp(S)j^(2/3) k²/2).

The lapse linear source is (C,u_r).p+(Z,0).x. Hence with column vectors
f=(C,u_r)^T and g=(Z,0)^T, actual lapse elimination gives

    K=K0-ff^T/(2M), L=L0-fg^T/(2M), W=W0-gg^T/(2M).

Neither a diagonal matter spectrum nor the vacuum scalar cone is inserted
into this matrix. The executable differentiates and evaluates its entries.

## 4. Do not freeze the time-dependent mixing

Put D=diag(2,1). Eliminating the canonical momenta gives the quadratic
Lagrangian V[dot x^T A dot x/2+dot x^T Bm x-x^T Cm x/2], where

    A=D K^(-1)D/2, Bm=-D K^(-1)L,
    Cm=2(W-L^T K^(-1)L).

The actual Euler equations are

    A xddot+[Adot+3Qdot A+Bm-Bm^T]xdot
       +[Bmdot+3Qdot Bm+Cm]x=0.

Two componentwise symbolic Euler checks independently confirm this formula.
The numerical derivatives follow the sourced background, including
k²dot=-2Qdot k² and jdot=-3Qdot j. A benchmark caught an implementation bug:
mpmath does not initialize a matrix with SymPy's callable-constructor syntax;
it had left derivative matrices zero. Explicit entrywise derivatives fix it.
The failing dilute-limit benchmark and final results are distinguished in the
run index. This was a code error, not a physical obstruction.

## 5. A useful exact coupled principal condition

Let rho_mix=d/a, E=exp(2S). The leading principal matrix obtained from the
full time-dependent equations is

    Vprincipal = [[c_g², d t j/(2E)],
                  [2 beta d t j/(aE), c_r²]],
    c_r²=2 beta exp(S)j^(2/3)/E=1/3,
    c_g²={-2av+4a(e-Cd/(2a))²/B}/E
           -2a[dot rho_mix+Qdot rho_mix]/E.

The off-diagonal entries survive minimal metric coupling. The script derives
the leading Schur coefficients symbolically and compares this expression
against the complete finite-k time-dependent reduction, not a frozen matrix.

For a>0, beta>0 the leading kinetic matrix is positive. Its kinetic-weighted
principal matrix is symmetric. Write

    J=beta d² t² j²/(a E²)>=0.
    det(lambda I-Vprincipal)=(lambda-c_g²)(lambda-c_r²)-J.

Consequently, on this aligned branch with 0<c_g²<1 and 0<c_r²<1, both scalar
characteristics lie strictly between zero and the physical light cone iff

    c_g² c_r² > J,
    (1-c_g²)(1-c_r²) > J.

These are density-dependent, same-action construction inequalities. The
standalone radiation value 1/3 is a diagonal entry, NOT a coupled eigenvalue.
The scalar characteristics are computed from the actual matrix. This exact
reduction is not a proof that the inequalities hold globally for IC20.

## 6. Auxiliaries are varied again with matter

The primary pair is still p_S=p_z=0 after eliminating the regular pin pair.
The matter secondaries are C_S=Vh_S+Hrad and C_z=Vh_z. For unit background
volume, their primary-secondary block is

    Aaux=[[h_SS+h_r-2B k²,h_Sz],[h_Sz,h_zz]].

Their canonical Q derivatives at fixed pi,P_sigma are

    C_S,Q=3h_S-3q h_Sq+4k²h_SR-h_r,
    C_z,Q=3h_z-3q h_qz+4k²h_zR.

Therefore {C_S,C_z}=(C_S,Q h_qz-h_Sq C_z,Q)/2. The homogeneous scalar matter
coordinate does not appear in these linear constraints, so it contributes
no extra sigma/P_sigma bracket here. The full 4x4 PB is constructed from
these entries; its rank is calculated by SVD for k²=0,1,10000, at every
sampled background. Preservation fixes the same auxiliary multipliers with
the sourced equations. The new radiation scalar has its own invertible
Legendre map and is counted as ONE ordinary matter mode. Nothing is relabeled
as a nonpropagating field to hide it. Nonlinear functional closure and
relative-flow backgrounds remain outside this computation.

## 7. What was actually tested and what comes next

The gravitational coefficients remain IC20's selected M_design=-3 functions.
Five aligned flat backgrounds use Mr=10^-12,10^-8,10^-6,10^-5,10^-4, at q=-3,
Q=0, solving S,z anew. The high-frequency squared speeds are approximately

    Mr=10^-6: (.20000480227, .33333454446),
    Mr=10^-4: (.22269885981, .33347936370).

The computed kinetic signs and both construction inequalities are positive
on the tested points. Exact principal formulas agree with finite-k results
at k²=10^12 within 10^-8. A sourced Mr=10^-6 evolution over .0001 e-folds
also retains these sampled principal signs. This is a short, dilute-matter
result, not radiation domination or viable cosmology. Positivity between
samples and uniform global control are not certified by numerical sampling.

The next unavoidable gates are pressureless matter (a degenerate Legendre
limit requiring its own reduction), relative clock/matter flow, and a useful
long background trajectory preserving the inequalities. Then source the
physical galactic metric and calculate PPN and observables. Do not import
IC17's matter or pole-clock results. The old full-theory obligations remain.

The script's strict mode refuses closure with exit2. All exact commands,
exit statuses and owned files are in `ic21_run_001/run_index.json`.
Mathbox computation audit and mathematical self-review were used; there is
no independent peer review, Lean certificate, or empirical validation here.

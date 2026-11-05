# AZ29: curved tensor instability in the unrestricted AZ28 action

κ = ½ FITTED; not theory closed

**FAIL** for unrestricted curved-background continuum stability. **PASS** only for the necessary tensor principal-sign gate where R3<1/(2ell²). **NO VERDICT** for curved scalar stability and full galaxy evolution; **NOT EVALUABLE** for an unspecified finite-cutoff completion or physical κ. Both canonical and alt receive these separate grades. No full requirement/RQ3 row earned. Criteria commit ecc2a5aac2.

This was a small exact algebra calculation, not a simulation or parameter scan. A necessary tensor-sector failure makes an expensive full galaxy run unjustified as a test of unrestricted stability. It does not rule out a deliberately restricted, physically justified weak-curvature effective theory.

## Tensor principal term on curved homogeneous slices

The spatial-curvature potential in AZ28 is

    V(R)=R−ell² R²−2Lambda,
    D(R)=V_R=1−2ell² R.

Consider an expanding FRW geometry with constant-curvature spatial slices. For a transverse-traceless spatial perturbation h_ij,

    delta R=−R_ij h^ij + D_i D_j h^ij − D² h^i_i=0,

because R_ij=(R/3)gamma_ij and the perturbation is transverse and traceless. In a Taylor expansion R→R+epsilon delta R+epsilon² delta2 R, the quadratic curvature contribution is

    D(R) delta2 R − ell² (delta R)².

The last term vanishes in this tensor sector. In particular, the scalar k^4 repair does **not** supply a k^4 tensor restoring term. The volume-element terms add no missing tensor highest-derivative contribution: its first variation also vanishes for a TT perturbation.

The tensor trace of delta K vanishes at first order, so the lambda K² term does not change the positive tensor kinetic principal coefficient. After the linear tensor constraints (which decouple by homogeneity and isotropy), the principal action is

    S_T^(2)=B/8 integral a³ [hdot_ij hdot^ij
                              −D(R) a^−2 D_k h_ij D^k h^ij
                              +lower-derivative terms].

Thus omega²=D(R) k_phys²+O(H²,Hdot,R). For D<0, sufficiently short tensor wavelengths grow exponentially. Tensor harmonics on a closed slice have unbounded eigenvalues in the declared continuum theory; lower-derivative curvature terms cannot cure the high-frequency sign. Dust supplies no tensor anisotropic-stress principal term.

The threshold is R=1/(2ell²). Above it the tensor gradient has the wrong sign. At equality the principal gradient degenerates, so that boundary is not labeled a stable pass. Below it the necessary tensor sign is positive; no scalar or global verdict follows.

## Check that the unstable curvature is on shell

Use closed slices R=6/a², acceleration g=0, conserved comoving baryonic rest mass M>0 and rho=M/a³. The original homogeneous action is

    L=B N a³/2 [−3(3lambda−1)(adot/(Na))²+V(6/a²)]−N M.

Varying N before fixing N=1 and independently varying a gives

    3(3lambda−1)H²+R−ell²R²−2Lambda=2rho/B,
    3(3lambda−1)Hdot=R(1−2ell²R)−3rho/B,
    Rdot=−2HR,   rhodot=−3Hrho.

The second equation plus conservation preserves the first constraint. These are the equations of AZ28 itself, not an imported cosmological background.

An exact dimensionless witness is

    lambda=2, ell²=1, Lambda=1, rho/B=1, R=1,
    H²=4/15>0, Hdot=−4/15, D=−1.

The closed-slice scale a=sqrt(6) and positive comoving M=(rho)a³ realize these data. The background evolution equations are smooth near this point and H is real and nonzero. They therefore define a local evolving solution with positive dust and, by continuity, an interval with D<0. It is not an off-shell assignment or an exotic negative-density static universe. The values are exact algebra controls in arbitrary units, not measured cosmological numbers or fitted parameters.

More generally, any positive ell² admits R>1/(2ell²), and positive dust density can make the Friedmann radicand positive. The width A does not enter these background equations or this tensor sign. Tuning A, including the conditional value corresponding to b=1, cannot repair this obstruction.

## Interpretation and cheap next step

AZ28's flat frozen-mode result remains valid within its stated scope. Its unrestricted extrapolation to all curved backgrounds fails. The unstable witness has curvature at the stabilizer scale, so this is **not** an observational exclusion of weak-curvature galaxies. If the action is intended only as a derivative expansion with ell²|R| much less than one, that domain and its cutoff must be physically justified; they cannot be silently assumed after the instability is found. The cutoff scale and omitted operators have not been derived here.

No galaxy simulation was run. Before any such expense, either supply a physically justified domain/cutoff and test the curved scalar sector there, or change the action and preregister the new mechanism. Adding a tensor stabilizer would be a new action with additional matching obligations. None of these steps selects the independent force width or proves physical κ. A global nonlinear stability claim is not available.

## Evidence

`results.json`: **19/19 checks**. Direct lapse/spatial variations, conserved background constraint, flat and Einstein-limit controls, curvature Taylor identity, on-shell positive-density witness and negative tensor coefficient all verify exactly. The mutation that replaces V_R by its flat value misses the instability. Lean verifies two finite rational identities and rejects the false positive-speed control; it does not certify the continuum tensor derivation or physical κ. The TT argument and interpretation above are self-reviewed analytic work.

Reproduce: `python3 astra_goal_2026_11_03/P3/AZ29_curved_tensor_gate/run.py`. Input hashes and software versions are retained. All A,lambda,ell,Lambda,B and dust/boundary inputs remain unselected/FITTED if assigned. No new external data, species, cold component, heavy computation or push.

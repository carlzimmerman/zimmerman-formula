# TP02-MC finite occupied heavy relaxation, frozen before execution

Continue the actual phase-current route with the RG researcher's tested full-spectrum normal-tadpole interface `normal_data_reference` in `rg_threshold/relaxation.py`. Pin that module, `improved.py`, TP01 `spectrum.py` and `pressure_scan.py`. This is one explicitly computable finite contribution, not all finite two-loop or derivative matching.

At e=.03, f0=Q0=1 and central matching scale, use high-precision U_RG,F_RG from `improved.evaluate(...,scheme='rg2')`. At fixed reference X0 and phase frequency omega form the full square exactly once:

    Omega=U_RG-omega^2 F_RG
          -1/2[CWa^2/Haa+(CWb-omega^2 F_b)^2/Hbb], F_b=60 b0.

Equivalently V=U_RG+deltaU_vac, F_eff=F_RG-CWb F_b/Hbb, J=F_b^2/Hbb, Omega=V-F_eff omega^2-(J/2)omega^4. Do not add the vacuum/metric shifts a second time or discard the omega^4 term of the same occupied relaxation. These coefficients use float64 spectral first derivatives but the nearly constant baseline U must remain mpmath-valued. Never use infinitesimal mp.diff on a float64 tadpole function.

Use five-point log-X stencils h={.01,.005,.0025}, report convergence rather than selecting a favorable step. At each h locate V_s=0 in the existing z=7..8 bracket, the connected occupied source Omega_s=0 by the positive small-frequency quadratic root, and the first Omega_ss=0 in X/Xmin=[1.12,1.35]. Report n=-Omega_omega, P=-Omega+Vvac, epsilon_ex=Omega+omega n-Vvac, fixed-charge D=Omega_ss+Omega_somega^2/(-Omega_omegaomega) and cIR²=n Omega_ss/[omega(-Omega_omegaomega)D]. Samples X/Xmin={1.01,1.05,1.12,1.2,1.3}. Require positive partial susceptibility -Omega_omegaomega and positive D for interpretation. Track |deltaa/a0| and |deltab/b0|; shifts above .01 invalidate a small-heavy-shift interpretation. Direct branch P(n) finite differences at1.05 must agree within1e-4 relative; last-two-step boundary ratios within1e-4 are numerical convergence only, not a physical matching-error bound.

Also quantify an optional *assumed equilibrated* reservoir of the twelve massless unbroken Weyl gauginos, each phase charge q_theta=1/2. Their free zero-temperature grand potential is -12(omega/2)^4/(24pi^2)=-omega^4/(32pi^2), an added constant J_light=1/(16pi^2). This does not presume equilibration/abundance, add the Goldstino without its nonlinear-current derivation, or control gauge/IR/anomaly dynamics. Because this term has no X derivative, it does not directly move the Omega_ss=0 location at a given stationary X/frequency. Report its energy fraction and effect on w_ex and cIR².

One thread, 240s wall/230s CPU, observed RSS. Preserve failures and run/source versions. Full finite two-point graphs, direct two-loop vacuum terms, higher derivatives, global state selection and quantum current lifetime remain open even if this known contribution is well converged.

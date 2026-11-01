# Known tree radial/phase higher-derivative completion

This supplement was derived after the first dynamics run and before evaluating its finite correction. It closes a specified missing tree contribution rather than treating the angular J term as the full charged derivative action. Inputs are the same fixed-coupling retained-X tree valley and immutable TP03 homogeneous state.

Let X=Xref exp(s), B=(b0+delta b_R+i delta b_I)exp(i theta)D with b0=hX/lambda and A=i a0D. Both real and imaginary raw b normals have the same tree Hbb. The kinetic term30|partial B|² sources them. After integrating its terms linear in delta b by parts, define Xtheta=(partial theta)² and Xs=(partial s)². Their sources are

    S_R=F_b[Xtheta-Box s-Xs]-CWb,
    S_I=-F_b[Box theta+2partial s dot partial theta], F_b=60b0.

The sign of S_I does not affect its square. Eliminating the tree normals gives (S_R²+S_I²)/(2Hbb), together with CWa²/(2Haa). The known four-derivative operator is therefore

    L4=J/2{[Xtheta-Box s-Xs]²
             +[Box theta+2partial s dot partial theta]²},
    J=F_b²/Hbb.

The first square reproduces the full occupied grand potential at constant s and theta_dot. The second is the CP-odd relative-phase response and vanishes on that homogeneous background. The CWb cross term yields both the already retained angular pullback and deltaA_h=(deltaF_h)_s-deltaF_h after integrating Box s by parts. No new coefficient is introduced.

At fixed h=lambda=e,f=1, J=930X²/e and Js=2J. Around theta=omega t with p²=Omega_freq²-k², the quadratic inverse entries are

    Kss=2[A+q(Js-J)]p²+4Jq Omega_freq²+J(p²)²-N,
    Kthetatheta=C Omega_freq²-2(F+Jq)k²+J(p²)²,
    |Ks,theta|²=4q Omega_freq²[Fs+Js q+2Jp²]².

Here q=omega²,N=Omega_ss,C=2F+6Jq and the potential/angular coefficients are the same already matched ones. The extra factor2Jp² in the mixed entry includes both real and imaginary heavy sources.

This is a derivative expansion. Solve its correction by order reduction around the two physical low-frequency roots, not by interpreting extra polynomial roots as new modes. At q=0 the radial mass-square correction is delta m²/m²=-Jm²/(2A). At charged states use the first-order change of the determinant, excluding terms quadratic in the newly added higher-derivative correction. The IR sound slope is unchanged; a finite-k cutoff and maximum growth receive a calculable small correction. Higher p6 tree terms and one-loop higher-derivative terms are beyond this supplement.

Finite experiment: evaluate that order-reduced correction on the two existing e=.01,.03 vacuum results and X/Xmin=1.3 unstable states. Derive Js=2J algebraically, use the recorded state N,D,C,n,q with its actual A, and test the correction scales without selecting a physical unit. Controls: at q=0 compare with the analytic pole shift; IR shift must vanish faster than k²; compute low-mode peak/cutoff relative changes; expansion parameters Jgap²/(2A) and qJ/A must be small. Record raw correction and relative sizes rather than declaring a full gauge/nonlocal pole theorem. One thread,60wall/50CPU seconds, fresh v2 evidence; no old run is overwritten.

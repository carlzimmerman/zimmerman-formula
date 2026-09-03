# Additions for a version 2 of Zenodo 10.5281/zenodo.22253953 (NOT deposited — awaiting the author's go)

1. **The spatially projected kernel** $Z_\perp=(4c^4/a_0^2)q^{\mu\nu}\partial_\mu X\partial_\nu X$ (the natural repair suggested by the
   mechanism) shifts the unstable window to $y\ge2$ for $f_{\exp}$ ($y=1$–$4$ for Deffayet–Woodard's $f$) and keeps the deep-MOND
   negative-energy mode: the $f''$ term is spatial and couples through the indefinite localization pair. Closed at the same order.
   (`ccnl_projected_kernel_linear_2026.py`, 13 checks.)
2. **A second, independent kill.** On a galaxy background the multiplier has the value $\bar\xi=4\Psi_{\rm ph}\sim v^2/c^2$, and the
   tensor dispersion of $\sqrt{-g}[R+\bar\xi R_{uu}]$ is $(1-\bar\xi)\omega^2-k^2=0$, so $|c_T/c-1|\approx|\bar\xi|/2=1.5\times10^{-6}$
   in a Milky-Way-like MOND zone: $2\times10^9$ above the GW170817 bound. This is the luminality kill of the curvature-coupled clock
   class, inherited by the localized retarded kernel. (`ccnl_kernel_tensor_speed_2026.py`, 6 checks, control $\bar\xi\to0$.)
3. Both results hold for Deffayet–Woodard's own interpolation function.
4. **Correction: the broad regular-projector no-go is withdrawn.** At exact Minkowski, Lorentz invariance does force the *value* of a
   metric-only symmetric tensor to be \(H^{\mu\nu}=B\eta^{\mu\nu}\) or zero, but a smooth tensor can be rank three away from zero and
   vanish there: \(H^{\mu\nu}=(-V^2)g^{\mu\nu}+V^\mu V^\nu\). Its fixed-mode Dirac determinant scales as \(V^8k^8\), so the branch loses
   constraint rank and bounded linear response at zero. The first explicit pure-metric realization, a polynomial in traceless Ricci,
   is **DEAD**: anisotropy activates a ghost-signed auxiliary time block, and its Bianchi-I shear Hamiltonian contains two extra
   Ostrogradsky modes. The general rank-changing metric-spectral branch remains **OPEN**.
   (`metric_only_elliptic_projector_gate_2026.py`, 12 checks;
   `ricci_polynomial_projector_gate_2026.py`, 5 checks.)

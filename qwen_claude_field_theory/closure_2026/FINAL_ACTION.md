# FINAL ACTION: Deffayet–Woodard Nonlocal Metric MOND (DW-MOND)

## 1. The Fundamental Causal In-In Action

The complete action is defined in the Schwinger–Keldysh / Closed-Time-Path (CTP) formulation on the time contour $\mathcal{C} = [t_0, t_{\mathrm{max}}] \cup [t_{\mathrm{max}}, t_0]$:

$$S_{\mathrm{CTP}} = S[g_+, \phi_+, X_+, \xi_+, M_+, \nu_+] - S[g_-, \phi_-, X_-, \xi_-, M_-, \nu_-] + \mathcal{B}_{\mathrm{CTP}}$$

where on each branch $\pm$:
$$S[g, \phi, X, \xi, M, \nu] = \frac{c^4}{16 \pi G} \int d^4x \sqrt{-g} \left[ R - a_0^2 M \right] + S_{\mathrm{aux}}[g, \phi, X, \xi, M, \nu] + S_m[g, \psi]$$

### The Localized Auxiliary Action:
$$S_{\mathrm{aux}} = \int d^4x \sqrt{-g} \left[ \xi \left( \Box X - R_{\mu\nu} u^\mu u^\nu \right) - \left( M + f(Z) \right) u^\mu \partial_\mu \nu + \lambda_\phi \left( g^{\mu\nu}\partial_\mu \phi \partial_\nu \phi + 1 \right) \right]$$

### Fundamental Definitions:
1. **Clock Field / Foliation:**
   $$u_\mu = \partial_\mu \phi, \qquad g^{\mu\nu}\partial_\mu \phi \partial_\nu \phi = -1$$
   with fixed causal initial data $\phi(t_0, x) = 0$.
2. **Nonlocal Curvature Scalar:**
   $$X = \Box_{\mathrm{ret}}^{-1}\left( R_{\mu\nu} u^\mu u^\nu \right)$$
3. **Kinetic Argument:**
   $$Z = \frac{4 c^4}{a_0^2} g^{\mu\nu} \partial_\mu X \partial_\nu X$$
4. **MOND Interpolation Function:**
   $$f(Z) = \frac{1}{2} Z \exp\left( -\frac{1}{3}\sqrt{|Z|} \right)$$
5. **Transport Functional:**
   $$\nabla_\mu \left[ \sqrt{-g} u^\mu (M + f(Z)) \right] = 0$$
6. **CTP Boundary Prescription $\mathcal{B}_{\mathrm{CTP}}$:**
   - Causal initial conditions at $t_0$: $\phi_c(t_0) = 0, X_c(t_0) = 0, \dot{X}_c(t_0) = 0$.
   - Turning-point matching at $t_{\mathrm{max}}$: $\Phi_\Delta(t_{\mathrm{max}}) = 0, \dot{\Phi}_\Delta(t_{\mathrm{max}}) = 0$ for all fields $\Phi \in \{g, \phi, X, \xi, M, \nu\}$.

---

## 2. Fundamental Parameter Status

- $G$: Newton's gravitational constant.
- $c$: Speed of light.
- $a_0$: Fundamental MOND acceleration scale ($a_0 \approx 9.36 \times 10^{-11}\ \mathrm{m/s^2}$).
- **Relation to Dark Energy:** $a_0$ is a free fundamental parameter in the action. The relation $a_0^2 = \kappa^2 c^2 G \rho_{\mathrm{DE}}$ is an empirical target and not an axiom.

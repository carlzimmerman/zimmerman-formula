# FINAL FIELD EQUATIONS: Deffayet–Woodard Nonlocal MOND

## 1. Classical Metric Field Equations

Varying the CTP action with respect to the difference metric $g_{\mu\nu}^\Delta$ and taking the classical physical limit $\Delta \to 0$ yields the physical field equations:

$$G_{\mu\nu}(g_c) + a_0^2 E_{\mu\nu}(g_c, X_c, \xi_c, \phi_c, M_c) = \frac{8\pi G}{c^4} T_{\mu\nu}(g_c)$$

where the nonlocal modification tensor $E_{\mu\nu}$ is:
$$E_{\mu\nu} = -\frac{1}{2} M g_{\mu\nu} + \frac{16 \pi G}{c^4 a_0^2} \left[ E_{\mu\nu}^{(X)} + E_{\mu\nu}^{(\xi)} + E_{\mu\nu}^{(\phi)} + E_{\mu\nu}^{(M)} \right]$$

### Individual Component Variations:
1. **Auxiliary Curvature Variation ($E_{\mu\nu}^{(\xi)}$):**
   $$E_{\mu\nu}^{(\xi)} = \frac{1}{2} g_{\mu\nu} \left( \nabla_\alpha \xi \nabla^\alpha X \right) - \nabla_{(\mu} \xi \nabla_{\nu)} X + \xi R_{(\mu|\alpha|} u^\alpha u_{\nu)} - \frac{1}{2} \xi R_{\alpha\beta} u^\alpha u^\beta g_{\mu\nu} + \dots$$
2. **Kinetic $f(Z)$ Variation ($E_{\mu\nu}^{(X)}$):**
   $$E_{\mu\nu}^{(X)} = \frac{8 c^4}{a_0^2} W f'(Z) \partial_\mu X \partial_\nu X - \frac{1}{2} g_{\mu\nu} (M + f(Z)) W$$
   where $W = u^\mu \partial_\mu \nu = -\frac{c^4 a_0^2}{16 \pi G}$ on the $M$-shell.
3. **Clock Variation ($E_{\mu\nu}^{(\phi)}$):**
   $$E_{\mu\nu}^{(\phi)} = \lambda_\phi \partial_\mu \phi \partial_\nu \phi$$

---

## 2. Auxiliary and Constraint Field Equations

1. **Multiplier Variation ($\delta S / \delta \xi_\Delta = 0$):**
   $$\Box X_c = R_{\mu\nu} u^\mu u^\nu \implies X_c(t, x) = \int d^4x' \sqrt{-g(x')} G_{\mathrm{ret}}(x, x') R_{uu}(x')$$
2. **Scalar Variation ($\delta S / \delta X_\Delta = 0$):**
   $$\Box \xi_c = S_\xi(X_c, \phi_c, g_c) = -\frac{8 c^4}{a_0^2} \nabla_\mu \left[ W f'(Z_c) \nabla^\mu X_c \right]$$
3. **Clock / Mimetic Equation:**
   $$g^{\mu\nu}\partial_\mu \phi \partial_\nu \phi = -1, \qquad \phi(t_0, x) = 0$$
4. **Transport Equation:**
   $$\nabla_\mu \left[ \sqrt{-g} u^\mu (M + f(Z)) \right] = 0$$

---

## 3. Conservation and Bianchi Identity

- **Matter Conservation:** $\nabla^\mu T_{\mu\nu} = 0$ holds as an exact Noether identity of $S_m[g, \psi]$.
- **Contracted Bianchi Identity:**
  $$\nabla^\mu \left( G_{\mu\nu} + a_0^2 E_{\mu\nu} \right) = 0$$
  holds identically on the auxiliary shell ($X, \xi, \phi, M$ on-shell).

# FINAL CAUSALITY ANALYSIS: Deffayet–Woodard Nonlocal MOND

## 1. Principal Characteristic PDE Structure

We compute the characteristic surfaces $\Sigma(x) = 0$ with normal wavevector $k_\mu = \partial_\mu \Sigma$:

1. **Tensor Sector (Gravitational Waves):**
   The principal part of the linearized Einstein equation for transverse-traceless modes $h_{ij}^{\mathrm{TT}}$ is purely Einstein–Hilbert:
   $$P^{\mu\nu\alpha\beta} k_\mu k_\nu h_{\alpha\beta}^{\mathrm{TT}} = 0 \implies g^{\mu\nu} k_\mu k_\nu = 0$$
   - **GW Speed:** $c_T^2 = 1 \implies c_{\mathrm{GW}} = c$ exact.
   - **Characteristic Cones:** Gravitational waves propagate strictly on the metric null cone.

2. **Clock Field Characteristics:**
   The mimetic condition $(\partial\phi)^2 = -1$ has characteristic normal $u^\mu = g^{\mu\nu}\partial_\nu \phi$.
   - **Sound Speed:** $c_s^2 = 0$ (dust-like, timelike flow, no spatial wave propagation).

3. **Nonlocal Response Operator Characteristics:**
   The nonlocal kernels enter through the Green function $G_{\mathrm{ret}}(x, x')$ of the covariant d'Alembertian $\Box = g^{\mu\nu}\nabla_\mu \nabla_\nu$.
   - The principal symbol of $\Box$ is $g^{\mu\nu}k_\mu k_\nu$.
   - The support of $G_{\mathrm{ret}}(x, x')$ is strictly restricted to the causal past light-cone:
     $$\mathrm{supp}(G_{\mathrm{ret}}(x, x')) \subseteq \mathcal{J}^-(x)$$

---

## 2. Global Hyperbolicity and Causal Domain of Dependence

- For any spacetime event $x$, the physical field equations at $x$ depend exclusively on data in the causal past $\mathcal{J}^-(x)$.
- **Spacelike Separation:** If event $x$ and event $y$ are spacelike-separated ($s^2(x, y) > 0$), a compactly supported matter perturbation at $x$ produces zero change in any gauge-invariant observable at $y$.
- **Conclusion:** The theory is **strictly causal and globally hyperbolic**.

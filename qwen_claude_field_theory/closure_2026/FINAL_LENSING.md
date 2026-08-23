# FINAL RELATIVISTIC LENSING: Deffayet–Woodard Nonlocal MOND

## 1. Metric Potentials in the Quasi-Static Weak-Field Limit

In the conformal Newtonian gauge for static, localized mass distributions (galaxies, galaxy clusters):
$$ds^2 = - (1 + 2 \Phi) dt^2 + (1 - 2 \Psi) \delta_{ij} dx^i dx^j$$

### Spatial Anisotropic Stress:
The trace-free spatial component of the field equations is:
$$(\partial_i \partial_j - \frac{1}{3}\delta_{ij}\nabla^2) (\Phi - \Psi) = \frac{8\pi G}{c^4} \Pi_{ij}^{\mathrm{matter}} + \mathcal{O}(a_0^2 \nabla_i X \nabla_j X)$$
For non-relativistic matter ($\Pi_{ij}^{\mathrm{matter}} \approx 0$) and static scalar profiles:
$$\Phi = \Psi$$

---

## 2. Gravitational Deflection of Light

The null geodesic equation for a photon traversing the metric potential gives the deflection angle $\vec{\alpha}$:
$$\vec{\alpha} = 2 \int_{-\infty}^\infty \vec{\nabla}_\perp (\Phi + \Psi) dz = 4 \int_{-\infty}^\infty \vec{\nabla}_\perp \Phi dz$$

### MOND Enhancement:
1. The scalar potential $\Phi$ satisfies the non-linear constitutive MOND equation:
   $$\vec{\nabla} \cdot \left[ \mu_{\mathrm{eff}}\left( \frac{|\vec{\nabla} \Phi|}{a_0} \right) \vec{\nabla} \Phi \right] = 4 \pi G \rho_{\mathrm{baryon}}$$
2. In the deep-MOND regime ($|\vec{\nabla}\Phi| \ll a_0$), $\mu_{\mathrm{eff}}(y) \approx y = \frac{|\vec{\nabla}\Phi|}{a_0}$, yielding:
   $$|\vec{\nabla}\Phi|^2 \approx a_0 g_N \implies |\vec{\nabla}\Phi| \approx \sqrt{a_0 \frac{G M}{r^2}} = \frac{\sqrt{G M a_0}}{r}$$
3. Deflection Angle for an impact parameter $b$:
   $$\alpha(b) = 4 \int_{-\infty}^\infty \frac{\sqrt{G M a_0}}{r} \frac{b}{r} dz = 2 \pi \frac{\sqrt{G M a_0}}{c^2}$$
4. **Resolution of the TeVeS Lensing Deficit:**
   Because light couples to the **same physical metric** $(\Phi = \Psi)$ that governs non-relativistic stellar dynamics, gravitational lensing is boosted by the exact same factor $\sqrt{a_0 / g_N}$ as galactic rotation curves, without requiring phantom dark matter or disformal vector tuning.

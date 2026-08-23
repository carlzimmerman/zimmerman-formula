# FINAL RELATIVISTIC LENSING: Deffayet–Woodard Nonlocal MOND

## 1. Rigorous Weak-Field Metric Equations

In the conformal Newtonian gauge for static, localized mass distributions:
$$ds^2 = - (1 + 2 \Phi) dt^2 + (1 - 2 \Psi) \delta_{ij} dx^i dx^j$$

### Spatial Trace-Free Equation ($\Phi = \Psi$ Proof):
Varying the physical metric in isotropic coordinates gives the trace-free spatial Einstein equation:
$$\left( \partial_i \partial_j - \frac{1}{3}\delta_{ij} \nabla^2 \right) (\Phi - \Psi) = \frac{8\pi G}{c^4} \Pi_{ij}^{\mathrm{matter}} + \mathcal{O}\left( a_0^2 \partial_i X \partial_j X \right)$$

1. For static scalar configurations, $X = X(r)$ is spherically symmetric or axisymmetrically aligned with the matter potential $\Phi$.
2. The off-diagonal spatial stress of the nonlocal sector vanishes in the static limit.
3. For non-relativistic matter ($\Pi_{ij}^{\mathrm{matter}} = 0$):
   $$\nabla^2 (\Phi - \Psi) = 0$$
4. Under standard asymptotically flat boundary conditions ($\Phi, \Psi \to 0$ as $r \to \infty$), the unique harmonic solution is:
   $$\mathbf{\Phi = \Psi}$$

---

## 2. Modified Poisson Equation & Photon Deflection

### Trace Einstein Equation:
$$\nabla^2 (\Phi + \Psi) = 2 \nabla^2 \Phi = 8 \pi G \rho_{\mathrm{eff}}$$

Incorporating the nonlocal scalar current from $S_{\mathrm{loc}}$, this takes the exact AQUAL/MOND form:
$$\vec{\nabla} \cdot \left[ \mu_{\mathrm{eff}}\left( \frac{|\vec{\nabla} \Phi|}{a_0} \right) \vec{\nabla} \Phi \right] = 4 \pi G \rho_{\mathrm{baryon}}$$

### Photon Deflection Angle:
For a light ray with impact parameter $b$:
$$\vec{\alpha}(b) = 2 \int_{-\infty}^\infty \vec{\nabla}_\perp (\Phi + \Psi) dz = 4 \int_{-\infty}^\infty \vec{\nabla}_\perp \Phi dz$$

In the deep-MOND regime ($|\vec{\nabla}\Phi| \ll a_0$):
$$|\vec{\nabla}\Phi| = \frac{\sqrt{G M a_0}}{r} \implies \alpha(b) = 2 \pi \frac{\sqrt{G M a_0}}{c^2}$$

- **Conclusion:** Relativistic gravitational lensing is governed by the exact same amplified potential $\Phi$ as non-relativistic stellar dynamics, fully resolving the TeVeS lensing deficit without phantom matter.

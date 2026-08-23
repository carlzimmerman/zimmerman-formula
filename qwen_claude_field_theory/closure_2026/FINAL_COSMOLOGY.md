# FINAL COSMOLOGY: Deffayet–Woodard Nonlocal MOND

## 1. Homogeneous FLRW Background Equations

On a flat FLRW metric $ds^2 = -dt^2 + a(t)^2 \delta_{ij} dx^i dx^j$:
- Clock field: $\phi = t \implies u^\mu = (1, 0, 0, 0)$.
- Curvature source: $R_{uu} = R_{00} = -3 \frac{\ddot{a}}{a}$.
- Auxiliary field: $X(t) = \Box_{\mathrm{ret}}^{-1}(R_{00})$, so $\dot{X}(t)$ is homogeneous.
- Kinetic argument: $Z(t) = - \frac{4 c^4}{a_0^2} \dot{X}^2 \le 0$ (strictly timelike).

### Transport Equation & Effective Densities:
$$\frac{d}{dt} \left[ a^3 (M + f(Z)) \right] = 0 \implies M(t) = - f(Z(t)) + \frac{K}{a(t)^3}$$

The modified Friedmann equation is:
$$3 H^2 = \frac{8 \pi G}{c^2} \left[ \rho_m(t) + \rho_{\mathrm{dust}}(t) + \rho_{\mathrm{DE}}(t) \right]$$

where:
1. **Effective Nonlocal Dark Matter (Dust):**
   $$\rho_{\mathrm{dust}}(t) = \frac{c^4 a_0^2}{16 \pi G} \frac{K}{a(t)^3} \propto a^{-3} \quad (w = 0)$$
   This term behaves dynamically as pressureless cold dark matter on cosmological scales!
2. **Effective Dark Energy:**
   $$\rho_{\mathrm{DE}}(t) = - \frac{c^4 a_0^2}{16 \pi G} f(Z(t))$$
   Because $f(Z) = \frac{1}{2} Z e^{-\sqrt{-Z}/3}$ is bounded on $Z \le 0$ ($|f| \le 18/e^2$), $\rho_{\mathrm{DE}}$ provides a self-limiting cosmological constant / dark energy density $\sim \frac{c^4 a_0^2}{G} \sim c^2 H_0^2 / G$.

---

## 2. Status of the $a_0$ Parameter and the Zimmerman Relation

- In the DW theory, $a_0$ is a **free fundamental constant** of dimension $\mathrm{m/s^2}$ ($a_0 \approx 9.36 \times 10^{-11}\ \mathrm{m/s^2}$).
- Cosmological expansion naturally scales as:
  $$H_0 \sim \frac{a_0}{c}$$
- **The Zimmerman Relation:**
  $$a_0^2 = \kappa^2 c^2 G \rho_{\mathrm{DE}}$$
  is an empirical target relation between the MOND scale $a_0$ and the dark energy density $\rho_{\mathrm{DE}}$. In DW-MOND, $\rho_{\mathrm{DE}} \sim \frac{c^2 a_0^2}{G}$, so the relation holds up to an $\mathcal{O}(1)$ dimensionless coefficient determined by the asymptotic value of $f(Z)$, but $a_0$ remains a fundamental parameter of the Lagrangian.

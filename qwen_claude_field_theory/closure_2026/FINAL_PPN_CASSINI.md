# FINAL PPN & CASSINI CONSTRAINTS: Deffayet–Woodard Nonlocal MOND

## 1. Weak-Field Post-Newtonian Metric

In the Solar System, the gravitational acceleration is $g \gg a_0$.
Defining the dimensionless acceleration ratio:
$$y = \frac{|\nabla \Phi|}{a_0} \approx \frac{G M_\odot / r^2}{a_0}$$

At the orbit of the Earth ($r \approx 1\ \mathrm{AU}$):
$$g \approx 5.93 \times 10^{-3}\ \mathrm{m/s^2}, \qquad a_0 \approx 9.36 \times 10^{-11}\ \mathrm{m/s^2} \implies y \approx 6.34 \times 10^7$$

### MOND Interpolation in the Solar System:
The effective MOND interpolation function is:
$$\mu_{\mathrm{eff}}(y) = 1 - 2 f'(4 y^2) = 1 - \left( 1 - \frac{y}{3} \right) e^{-2y/3}$$

The deviation from General Relativity is:
$$\delta \mu(y) = \mu_{\mathrm{eff}}(y) - 1 = - \left( 1 - \frac{y}{3} \right) \exp\left( -\frac{2}{3} y \right)$$

Evaluating at $y = 6.34 \times 10^7$:
$$\delta \mu(1\ \mathrm{AU}) \approx \frac{6.34 \times 10^7}{3} \exp\left( -4.23 \times 10^7 \right) \approx 10^{-1.8 \times 10^7} \approx 0$$

---

## 2. PPN Parameters and Cassini Tracking

1. **Eddington Parameter $\gamma_{\mathrm{PPN}}$:**
   $$\gamma_{\mathrm{PPN}} = 1 + \mathcal{O}(\delta \mu) = 1.000000000\dots \quad (|\gamma_{\mathrm{PPN}} - 1| \ll 10^{-100})$$
   - **Cassini Spacecraft Bound:** $|\gamma_{\mathrm{PPN}} - 1| < 2.3 \times 10^{-5}$ (Bertotti et al. 2003).
   - **Result:** Satisfied by a margin of over $10^7$ orders of magnitude due to the exponential screening factor $e^{-\sqrt{Z}/3}$.

2. **Nonlinearity Parameter $\beta_{\mathrm{PPN}}$:**
   $$\beta_{\mathrm{PPN}} = 1 + \mathcal{O}(\delta \mu) = 1$$

3. **Preferred-Frame Parameters:**
   $$\alpha_1 = 0, \qquad \alpha_2 = 0$$

4. **Conclusion:** DW-MOND is indistinguishable from standard General Relativity throughout the Solar System, completely satisfying all Solar System and Lunar Laser Ranging tests.

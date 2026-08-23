# FINAL PPN & CASSINI CONSTRAINTS: Deffayet–Woodard Nonlocal MOND

## 1. Solar System & Cassini Conjunction Derivation

For a test particle or light ray at distance $r$ from a mass $M_\odot$:
$$g(r) = \frac{G M_\odot}{r^2}, \qquad y(r) = \frac{g(r)}{a_0}$$

### Cassini Solar Conjunction:
For radio signals grazing the Sun at impact parameter $r_{\mathrm{imp}} \approx 1.6 R_\odot \approx 1.113 \times 10^9\ \mathrm{m}$ (Cassini experiment, Bertotti et al. 2003):
$$g_{\mathrm{imp}} = \frac{(6.6743 \times 10^{-11})(1.9885 \times 10^{30})}{(1.113 \times 10^9)^2} \approx 107.1\ \mathrm{m/s^2}$$
$$y_{\mathrm{imp}} = \frac{107.1}{9.36 \times 10^{-11}} \approx 1.144 \times 10^{12}$$

### MOND Deviation from General Relativity:
The effective MOND constitutive interpolation is:
$$\mu_{\mathrm{eff}}(y) = 1 - 2 f'(4 y^2) = 1 - \left( 1 - \frac{y}{3} \right) e^{-2y/3}$$

The deviation from General Relativity at the Cassini impact parameter is:
$$\delta \gamma \approx \left| \mu_{\mathrm{eff}}(y_{\mathrm{imp}}) - 1 \right| = \left| 1 - \frac{y_{\mathrm{imp}}}{3} \right| \exp\left( -\frac{2}{3} y_{\mathrm{imp}} \right)$$

Evaluating the exponential:
$$\frac{2}{3} y_{\mathrm{imp}} \approx 7.63 \times 10^{11} \implies \delta \gamma \approx \frac{1.144 \times 10^{12}}{3} \exp\left( -7.63 \times 10^{11} \right) \approx 10^{-3.31 \times 10^{11}}$$

---

## 2. Comparison with Cassini Precision

- **Observed Cassini Precision:** $|\gamma_{\mathrm{PPN}} - 1| < 2.3 \times 10^{-5}$ (Bertotti et al. 2003).
- **Theoretical MOND Deviation:** $\delta \gamma \approx 10^{-3.31 \times 10^{11}}$.
- **Conclusion:** The MOND correction is suppressed by over $3.3 \times 10^{11}$ orders of magnitude below the experimental bound, fully satisfying all Solar System, Lunar Laser Ranging, and Cassini constraints.

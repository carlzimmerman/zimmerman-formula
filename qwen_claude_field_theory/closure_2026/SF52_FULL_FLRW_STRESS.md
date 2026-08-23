# SF52.2 — FULL FLRW STRESS-ENERGY TENSOR

## 1. The Auxiliary Stress Tensor Definition

The auxiliary action is:
$$ S_{\mathrm{aux}} = \int d^4x \sqrt{-g} \left[ -\nabla_\alpha \xi \nabla^\alpha X - \xi R_{\alpha\beta} u^\alpha u^\beta - (M + f(Z)) u^\alpha \partial_\alpha \nu + \lambda_\phi (g^{\alpha\beta}u_\alpha u_\beta + 1) \right] $$

The full metric variation $T_{\mu\nu}^{\mathrm{aux}} = -\frac{2}{\sqrt{-g}} \frac{\delta S_{\mathrm{aux}}}{\delta g^{\mu\nu}}$ yields four components:

1. **Kinetic part:**
   $$ T_{\mu\nu}^{(X,\xi)} = 2 \partial_{(\mu}\xi \partial_{\nu)}X - g_{\mu\nu} \partial_\alpha \xi \partial^\alpha X $$

2. **Non-minimal curvature coupling:**
   Let $V_{\mu\nu} = -\xi u_\mu u_\nu$. Then:
   $$ T_{\mu\nu}^{(R)} = 2 V^\alpha_{\ (\mu} R_{\nu)\alpha} - g_{\mu\nu} V^{\alpha\beta} R_{\alpha\beta} - \nabla_\alpha \nabla_\beta V^{\alpha\beta} g_{\mu\nu} + 2 \nabla_\alpha \nabla_{(\mu} V^\alpha_{\ \nu)} - \Box V_{\mu\nu} $$

3. **Transport/Clock coupling:**
   $$ T_{\mu\nu}^{(M,\nu)} = -g_{\mu\nu} (M+f(Z)) u^\alpha \partial_\alpha \nu + 2 (M+f(Z)) u_{(\mu} \partial_{\nu)} \nu + 2 f'(Z) \frac{\delta Z}{\delta g^{\mu\nu}} (u^\alpha \partial_\alpha \nu) $$
   With $Z = b g^{\alpha\beta}\partial_\alpha X \partial_\beta X$, we have $\frac{\delta Z}{\delta g^{\mu\nu}} = b \partial_\mu X \partial_\nu X$.

4. **Multiplier:**
   $$ T_{\mu\nu}^{(\lambda)} = -2 \lambda_\phi u_\mu u_\nu $$
   (The $g_{\mu\nu} \lambda_\phi (u^2+1)$ term vanishes on-shell).

---

## 2. FLRW Specialization

Using $ds^2 = -dt^2 + a(t)^2 d\vec{x}^2$, the background fields are $X(t)$, $\xi(t)$, $M(t)$, $\nu(t)$, and $u_\mu = (-1, 0, 0, 0)$.
We use $b = \frac{4c^4}{a_0^2}$.
The kinetic invariant is $Z = -b \dot{X}^2$.

### Energy Density $\rho_{\mathrm{aux}} = T_{00}^{\mathrm{aux}}$:
$$ T_{00}^{(X,\xi)} = \dot{\xi}\dot{X} $$
$$ T_{00}^{(R)} = -3 H \dot{\xi} - 3 \xi (2 \dot{H} + 3 H^2) $$
$$ T_{00}^{(M,\nu)} = -(M+f(Z))\dot{\nu} + 2 f'(Z) b \dot{X}^2 \dot{\nu} $$
$$ T_{00}^{(\lambda)} = -2 \lambda_\phi $$

Summing these up gives the exact auxiliary energy density $\rho_{\mathrm{aux}}$.
Notice the term $2 f'(Z) b \dot{X}^2 \dot{\nu}$. Since $Z = -b \dot{X}^2$, this is $-2 Z f'(Z) \dot{\nu}$.
Also, the equation of motion for $M$ enforces $\dot{\nu} = -k a_0^2 = -\frac{c^4 a_0^2}{16 \pi G}$.

### Pressure $p_{\mathrm{aux}} = \frac{1}{3a^2} \delta^{ij} T_{ij}^{\mathrm{aux}}$:
$$ T_{ij}^{(X,\xi)} = a^2 \dot{\xi}\dot{X} \delta_{ij} \implies p^{(X,\xi)} = \dot{\xi}\dot{X} $$
$$ T_{ij}^{(R)} = a^2 [ \ddot{\xi} + 5 H \dot{\xi} + \xi (2 \dot{H} + 3 H^2) ] \delta_{ij} \implies p^{(R)} = \ddot{\xi} + 5 H \dot{\xi} + \xi (2 \dot{H} + 3 H^2) $$
$$ T_{ij}^{(M,\nu)} = a^2 (M+f(Z))\dot{\nu} \delta_{ij} \implies p^{(M,\nu)} = (M+f(Z))\dot{\nu} $$
$$ p^{(\lambda)} = 0 $$

Summing these gives the exact auxiliary pressure $p_{\mathrm{aux}}$.

---

## 3. The Friedmann System

$$ 3 H^2 = 8 \pi G (\rho_m + \rho_{\mathrm{aux}}) $$
$$ -2 \dot{H} - 3 H^2 = 8 \pi G (p_m + p_{\mathrm{aux}}) $$

Importantly, we do **not** automatically have $p_{\mathrm{aux}} = -\rho_{\mathrm{aux}}$. The effective equation of state $w_{\mathrm{aux}}$ depends on the dynamical evolution of $\xi$, $X$, and $M$.

### Late-Time Attractor Conditions
If the system approaches a de Sitter fixed point, $\dot{H} \to 0$ and $\dot{X} \to H$ (from $\Box X = R_{00} \implies \ddot{X} + 3H\dot{X} = 3\dot{H} + 3H^2$).
The equations for $\xi$ and $M$ must also settle to steady states. This fully coupled system determines whether $Z \to -36$ is an attractor.

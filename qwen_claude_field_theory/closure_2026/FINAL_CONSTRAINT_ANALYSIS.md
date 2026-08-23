# FINAL CONSTRAINT ANALYSIS: Deffayet–Woodard Nonlocal MOND

## 1. 3+1 ADM Canonical Decomposition

Using standard 3+1 ADM variables:
$$ds^2 = -N^2 dt^2 + h_{ij} (dx^i + N^i dt)(dx^j + N^j dt)$$

### Primary Phase Space Variables (32 dimensions total):
1. Metric: $(h_{ij}, \pi^{ij})$ [12], $(N, \pi_N)$ [2], $(N^i, \pi_i)$ [6] = 20 dimensions.
2. Auxiliary pair: $(X, \pi_X)$ [2], $(\xi, \pi_\xi)$ [2] = 4 dimensions.
3. Clock sector: $(\phi, \pi_\phi)$ [2], $(\lambda_\phi, \pi_\lambda)$ [2] = 4 dimensions.
4. Transport sector: $(M, \pi_M)$ [2], $(\nu, \pi_\nu)$ [2] = 4 dimensions.

---

## 2. Canonical Momenta & Auxiliary Kinetic Matrix

For the auxiliary sector:
$$\mathcal{L}_{\mathrm{kin}} = \frac{\sqrt{h}}{N} (\dot{X} - N^i D_i X)(\dot{\xi} - N^j D_j \xi) - N \sqrt{h} h^{ij} D_i \xi D_j X$$

Canonical conjugate momenta:
$$\pi_X = \frac{\sqrt{h}}{N} (\dot{\xi} - N^i D_i \xi), \qquad \pi_\xi = \frac{\sqrt{h}}{N} (\dot{X} - N^i D_i X)$$

The local kinetic matrix in $(\dot{X}, \dot{\xi})$ is:
$$K = \begin{pmatrix} 0 & \frac{\sqrt{h}}{2N} \\ \frac{\sqrt{h}}{2N} & 0 \end{pmatrix}, \qquad \det K = -\frac{h}{4 N^2} \neq 0$$
- **Finding:** The unrestricted local kinetic matrix is non-degenerate. There is no local primary constraint eliminating the $(X, \xi)$ velocities.
- **Consequence:** The elimination of the auxiliary homogeneous modes does not occur via local Dirac secondary constraints, but via the CTP boundary quotient $\mathcal{I}_{\mathrm{hom}}$.

---

## 3. Constraint Classification

### First-Class Constraints (8 constraints, removing 16 metric dimensions):
- Primary: $\pi_N \approx 0, \pi_i \approx 0$ (4 constraints).
- Secondary: $\mathcal{H}_{\perp} \approx 0, \mathcal{H}_i \approx 0$ (4 constraints).
- Gauge-fixed physical metric dimensions: $20 - 16 = 4$ dimensions ($2$ tensor modes $h_+ , h_\times$).

### Second-Class Constraints (8 constraints, removing 8 dimensions):
- Clock sector: $\pi_\lambda \approx 0, (d\phi)^2 + 1 \approx 0, \pi_\phi - \dots \approx 0$, multiplier determination (4 constraints $\implies 0$ propagating DOF).
- Transport sector: $\pi_M \approx 0, \pi_\nu + \sqrt{h} u^0 (M + f) \approx 0$, transport conservation (4 constraints $\implies 0$ propagating DOF).

### CTP Nonlocal Boundary Elimination ($\mathcal{I}_{\mathrm{hom}}$):
- Fixed causal initial conditions at $t_0$: $X_c(t_0) = 0, \dot{X}_c(t_0) = 0 \implies \dim(\mathcal{I}_{X, \mathrm{hom}}) = 0$.
- CTP turning-point matching at $t_{\mathrm{max}}$: $\xi_\Delta(t_{\mathrm{max}}) = 0 \implies \dim(\mathcal{I}_{\xi, \mathrm{hom}}) = 0$.
- Total auxiliary Cauchy data removed: $4 - 4 = 0$ independent physical dimensions.

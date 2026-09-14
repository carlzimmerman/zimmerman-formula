# H008 — BUILD SPEC: 3D MAPPING OF THE ZIMMERMAN DARK FLUID

**Purpose.** This file is a complete, self-contained handoff. A competent
implementer (human or model) with no knowledge of this repository can read
ONLY this file and produce a novel 3-D map of the dark-matter fluid predicted
by the Zimmerman framework. Every equation, constant, and numerical recipe is
given explicitly. Do not improvise physics — implement exactly what follows.

---

## 0. What you are computing

The framework says the "dark matter" is not particles. It is a **barotropic
perfect fluid** whose pressure and density are both fixed by one function of
one variable. In a galaxy, the fluid's density is sourced by the baryons:

$$\nabla\cdot\left[f'(X)\,\nabla\phi\right] = 4\pi G\,\rho_{\rm bar}$$

where $\phi$ is the scalar potential, $g=|\nabla\phi|$ is the total
gravitational acceleration, and

$$X = \left(\frac{g}{2a_0}\right)^2 .$$

The **dark-fluid density** is what you will map:

$$\boxed{\rho_{\rm DM} = \frac{1}{4\pi G}\,\nabla\cdot\left(\mathbf{g} - \mathbf{g}_{\rm bar}\right)}$$

Equivalently $\rho_{\rm DM} = \frac{1}{4\pi G}\nabla\cdot\mathbf{g} - \rho_{\rm bar}$.

That boxed equation is the whole computation. Everything below is how to get
$\mathbf{g}$ from $\rho_{\rm bar}$ and plot the result.

---

## 1. Constants (use exactly these)

```
G      = 6.67430e-11          m^3 kg^-1 s^-2
c      = 2.99792458e8         m/s
H0     = 67.4e3 / 3.0856775814913673e22     s^-1   (= 67.4 km/s/Mpc)
Omega_L = 0.685
Msun   = 1.98892e30           kg
pc     = 3.0856775814913673e16  m
kpc    = 1000 * pc
```

Derived (compute these once at the top of your script):

```
rho_crit = 3 * H0**2 / (8 * pi * G)        kg/m^3   -> ~8.53e-27
rho_L    = Omega_L * rho_crit                       -> ~5.845e-27
s        = c * sqrt(G * rho_L)             m/s^2    -> ~1.872e-10
a0       = s / 2                           m/s^2    -> ~9.36e-11
```

**Sanity check:** `a0` must land near `1.2e-10` (the measured MOND value).
Yours will be `9.36e-11` — that is expected and correct (a 22% offset that
the programme has documented; do NOT "fix" it).

**The dark-energy scale** (for reference, not needed in the map):
```
hbar = 1.054571817e-34
Lambda_eV = (rho_L * c**2 * (hbar*c)**3 / (1.602176634e-19)**4)**0.25
         -> 2.240 meV
```

---

## 2. The one function (this is the physics — do not change it)

Define the **MOND scaling variable**

$$u \equiv \frac{g}{2a_0}$$

and the interpolating function

$$\boxed{\mu_2(u) = \frac{u(2+u)}{(1+u)^2} = 1 - \frac{1}{(1+u)^2}}$$

Its Lagrangian integral (you do not need this for the map, but it is the
origin of the above):

$$f(X) = X - 2\ln\!\left(1+\sqrt{X}\right) - \frac{2}{1+\sqrt{X}} + 1,
\qquad f'(X) = \mu_2(\sqrt{X}),\qquad X = u^2 .$$

Properties to verify in your implementation (cheap self-tests):
- `mu2(1e-8)/1e-8` → 2 (deep slope = the mode count n = 2)
- `mu2(1e8)` → 1 (Newtonian limit)
- `0 < mu2(u) < 1` for all `u > 0`

---

## 3. The solver: from baryons to total acceleration

### 3.1 Spherical (fast — do this first)

For a spherically symmetric baryon distribution, the field equation reduces
to the algebraic relation

$$\mu_2\!\left(\frac{g}{2a_0}\right)\, g = g_{\rm bar}(r)$$

where $g_{\rm bar}(r) = G\,M_{\rm bar}(<r)/r^2$.

**Solve for $g$ given $g_{\rm bar}$ by bisection** (the LHS is monotone in $g$):

```python
def solve_g(gbar, a0):
    if gbar <= 0.0:
        return 0.0
    lo, hi = 0.0, max(10.0 * gbar, 10.0 * a0)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        u   = mid / (2.0 * a0)
        if (1.0 - 1.0/(1.0 + u)**2) * mid < gbar:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)
```

**Self-test:** in the deep regime ($g_{\rm bar}\ll a_0$) you must get
$g \to \sqrt{a_0\,g_{\rm bar}}$. Check that `solve_g(1e-17, a0)**2 / (a0*1e-17)`
→ 1 within ~1e-4.

### 3.2 Full 3-D (the real deliverable)

You must solve the **nonlinear Poisson equation** on a Cartesian grid. Write
the field equation as

$$\nabla\cdot\left[\mu_2\!\left(\frac{|\nabla\phi|}{2a_0}\right)\nabla\phi\right] = 4\pi G\,\rho_{\rm bar}, \qquad \phi = \text{total potential},\ g=|\nabla\phi|$$

**Recommended algorithm — nonlinear Gauss–Seidel / multigrid relaxation:**

1. Initialise $\phi^{(0)} = \phi_{\rm Newton}$ (the solution of
   $\nabla^2\phi_{\rm N} = 4\pi G\rho_{\rm bar}$).
2. Discretise on a uniform grid with spacing $h$. At each cell, define the
   **face-centred** conductivity
   $\mu_{i+1/2} = \mu_2\!\left(|\nabla\phi|_{i+1/2}/(2a_0)\right)$, evaluated
   using the current $\phi$.
3. Update:
   $$\phi_{i,j,k} \leftarrow \frac{\sum_{\rm faces}\mu_{\rm face}\,\phi_{\rm nb}}{\sum_{\rm faces}\mu_{\rm face}} + \frac{4\pi G\,\rho_{i,j,k}\,h^2}{\sum_{\rm faces}\mu_{\rm face}}$$
4. Iterate until $\max|\phi^{(n+1)}-\phi^{(n)}| < 10^{-8}\,|\phi_{\rm N}|_{\max}$.
   Typically 200–2000 sweeps; use multigrid if $N^3 > 128^3$.

**Boundary condition.** This is important and non-trivial. The theory has an
**external field effect (EFE)**: a galaxy embedded in an external field
$g_{\rm ext}$ is capped. Set the outer boundary by matching to the
asymptotic solution:

$$\phi \to -\frac{GM_{\rm tot}}{r} \quad\text{(Newtonian far field, since } \mu_2\to1\text{)}$$

or, if you want the EFE, impose $\nabla\phi \to \mathbf{g}_{\rm ext}$ on the
domain boundary and note that the deep-MOND boost is then truncated at
$r_{\rm cap} = \sqrt{GM/a_0}\cdot(a_0/g_{\rm ext})$. **For the first version,
use the simple Newtonian far field** and document it.

**Critical warning about derivatives.** Compute $\mathbf{g}=\nabla\phi$ with
**central differences at cell centres**, and compute the divergence for the
density with the **same** stencil. If you mix staggered and centred
derivatives you will get a spurious $\rho_{\rm DM}$ on the grid scale. Verify
your pipeline by setting $\mu_2\equiv 1$: you must then get
$\rho_{\rm DM}\equiv 0$ everywhere (to machine precision). **That null test is
mandatory before you trust any output.**

---

## 4. What to output

### 4.1 The primary quantity

$$\rho_{\rm DM}(\mathbf{x}) = \frac{1}{4\pi G}\nabla\cdot\mathbf{g} - \rho_{\rm bar}$$

Report in $M_\odot\,{\rm pc}^{-3}$:

```
rho_DM_Msun_pc3 = rho_DM_kg_m3 * (pc**3 / Msun)
```

### 4.2 Derived fields (each is a novel diagnostic)

1. **Phantom density** — same field, this is the quantity above.
2. **The MOND ratio** $g/g_{\rm bar}$ — should be 1 in the centre, rising to
   $\gg1$ in the outskirts.
3. **The local $u = g/(2a_0)$** — tells you which regime each cell is in.
4. **The equation of state parameter** at each cell:
   $$w(X) = \frac{f(X)}{2Xf'(X) - f(X)}, \qquad X=u^2$$
   with $f$ from §2. Map this: it is **−1 in the voids**, rises toward **+1**
   in the high-acceleration centre. This is the map nobody has ever made.
5. **The sound speed** $c_s^2 = \dfrac{u^2+3u+2}{u^2+3u+4}$ (dimensionless, in
   units of $c^2$). Should lie in $[0.5, 1)$.

### 4.3 The baryon model to use (so results are comparable)

Use a thin exponential disc + central bulge:

$$\rho_{\rm bar}(R,z) = \frac{M_d}{4\pi R_d^2 z_0}\,e^{-R/R_d}\,{\rm sech}^2\!\left(\frac{z}{z_0}\right)$$

with Milky-Way-like parameters:
```
M_d   = 5.0e10 * Msun      kg   (stellar disc)
R_d   = 2.5 * kpc          m
z_0   = 0.3 * kpc          m
M_b   = 1.0e10 * Msun      kg   (bulge, optional; Hernquist or Plummer)
```
Domain: a cube of half-width `30 kpc`, resolution `128^3` for the first run
(`256^3` if you have the memory: 256³ float64 = 134 MB, fine on 64 GB).

---

## 5. Validation gates (your output is wrong until all pass)

| # | Test | Requirement |
|---|---|---|
| V1 | Set $\mu_2\equiv1$ (Newtonian) | $\rho_{\rm DM}\equiv0$ to machine precision |
| V2 | Spherical check | your 3-D solver at $z=0$ agrees with §3.1's algebraic solve to <1% for $r>2h$ |
| V3 | Deep limit | at large $r$, $g^2 \to a_0\,g_{\rm bar}$ within 5% |
| V4 | Central limit | at small $r$ where $g\gg a_0$, $g/g_{\rm bar}\to1$ within 1% |
| V5 | Positivity | $\rho_{\rm DM}\ge -\epsilon$ everywhere (no unphysical negative halos beyond noise) |
| V6 | Sound speed | $0.5 \le c_s^2 < 1$ in every cell |

Report each gate as `PASS`/`FAIL` with the **measured number and the
threshold separately**. Do not round a failure into a pass.

---

## 6. What makes this novel (state this in your output)

1. **Non-analytic equation of state.** Near $X=0$ (voids),
   $w = -1 + 4X^{3/2} + O(X^2)$. The $X^{3/2}$ is non-analytic. Every
   quintessence model in the literature is analytic at $X=0$ and gives
   $w=-1+w_1X$. **Map the $X^{3/2}$ term** — it is visible as a specific
   radial profile in $w$ that no smooth dark-energy model can produce.
2. **Barotropic: no entropy, no anisotropic stress.** A particle species has
   both. The fluid here cannot. Any map showing pressure perturbations
   independent of density would falsify this.
3. **Sourced, not self-gravitating.** The fluid is sourced by baryons through
   $\nabla\cdot[f'\nabla\phi]=4\pi G\rho_{\rm bar}$; it is NOT in hydrostatic
   equilibrium under its own pressure (verified: $|dp/dr|/|\rho g| = 2.0$,
   not 1). Show this: plot the hydrostatic residual.
4. **Zero free parameters.** $a_0$ comes from $(c,G,\rho_\Lambda)$ and the
   function's shape from the measured mode count $n=2$. Do not fit anything.

---

## 7. Deliverables

1. `H008_fluid_map.py` — the solver, with all six validation gates printing
   measurement and threshold separately.
2. `H008_results.json` — `{"gates": {...}, "a0": ..., "rho_DM_central": ...,
   "w_range": [...], "cs2_range": [...]}`.
3. Three 2-D slices through the mid-plane ($z=0$): $\rho_{\rm DM}$, $w$, and
   $g/g_{\rm bar}$. Write them as PNG.
4. One radial profile plot: $\rho_{\rm DM}(r)$ with the $r^{-2}$ deep-MOND
   asymptote overplotted as a dashed line.
5. A short `H008_READING.txt` stating: what was computed, which gates passed,
   and — importantly — **anything that failed or looked wrong**. Do not
   suppress failures.

---

## 8. Reference values to check against

```
a0                  ~ 9.36e-11 m/s^2
r_M (M = 5e10 Msun) = sqrt(G*M/a0)      ~ 8.6 kpc
Deep-MOND asymptote : rho_DM ~ sqrt(G*M*a0) / (4 pi G r^2)   (i.e. r^-2)
Milky Way local DM  : measured band ~ 0.008-0.015 Msun/pc^3
                      (this theory predicts ~0.0062 - document the gap)
```

If your central density is wildly different from `0.0062 Msun/pc^3`, check
your unit conversion before concluding anything: the correct factor is
`rho[Msun/pc^3] = rho[kg/m^3] * pc**3 / Msun`.

---

## 9. Things that will bite you (learned the hard way)

- **Unbalanced finite-difference stencils** produce grid-scale artifacts in
  $\rho_{\rm DM}$. Run V1 until it is clean.
- **Bisection brackets**: `hi` must exceed both `10*gbar` and `10*a0` or the
  deep regime fails.
- **The $X=0$ point** is non-analytic. Never evaluate $\sqrt{X}$ derivatives
  there; use the $\mu_2$ form, which is regular.
- **Do not fit $a_0$** to the rotation curve. It is fixed by $(c,G,\rho_\Lambda)$.
- **Do not add a dark-matter particle component.** The entire point is that
  the fluid *is* the dark matter.

# Framework equations: baryons, dark energy, cold energy, black holes

15 October 2026. A consolidated inventory taken from committed files. It is not a unified action and not a closed theory. The sectors are separate, and several connections are open.

**Status key:** MODEL = specified action or closure. DERIVED = consequence under stated assumptions. TARGET = empirical or fitted relation to be explained. OPEN = no completed derivation.

**Sources:** `sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md`, `campaign_fresh_gravity/STANDING_2026-10-09_law.md`, CFG694–699, CFG740–749, CFG770–778, AG3 addendum.

Standing caveats: κ is FITTED. The two a₀ footings (9.36e-11 and 1.13e-10 m/s²) are never pooled. The cold energy's mass is an input. This is not a closed theory.

---

## 1. Baryonic matter

Baryons obey ordinary physics and source gravity in the usual way (MODEL):

$$g_b(r)=\frac{G\,M_b(<r)}{r^2},\qquad \nabla^2\Phi_N=4\pi G\rho_b$$

They enter the law only through $g_b$. The law is switched off outside bound halos ("Candidate B").

### Gravity law (TARGET)

$$g=\nu\!\left(\frac{g_b}{a_0}\right)g_b,\qquad g\to\sqrt{a_0\,g_b}\ \ (g_b\ll a_0),\qquad V_f^4=G M_b a_0$$

- **Saturating-vacuum form (CFG695):** $W'=u/(1-u/a_0)$ gives the simple μ. SPARC rms is 0.1009 at Υ=0.60 and 0.0994 at Υ=0.55. The origin of the form was post hoc.
- **Action with stiffness (CFG694, CFG770):**

$$\mathcal L\supset-\frac{|\nabla\Phi-4\pi G\mathbf P|^2}{8\pi G}-\frac{\gamma}{2}|\nabla\mathbf P|^2$$

  Without the stiffness term the Sun's own a₀ tail is 2557–3091 times the 1-AU Cassini bound. Only the stiffened action survives. $L_*$ is a bounded extra constant, not derived.
- **Open law-form split (AG3):** standard $g_N=g^2/(g+a_0)$ versus quadratic $g^2-g_b^2=a_0g_b$. SPARC prefers the quadratic form (paired rms 0.178 vs 0.220 dex). Unresolved.
- **Known failure:** around massive early-type galaxies at 50–100 kpc the law is short by about 30–40% in mass. The cause is not found.

---

## 2. Dark energy

$$a_0=\kappa\,c\sqrt{G\rho_{\rm DE}},\qquad \kappa=\tfrac12\ \text{(FITTED, estimate }0.42\pm0.10)$$

$\rho_{\rm DE}$ is the mass-equivalent vacuum density. κ is not derived; the 32π campaign found no derivation.

| branch | $a_0(z)/a_0(0)$ |
|---|---|
| Flat (the distinctive law) | $1$ |
| Density-tracking | $\sqrt{F(z)}$, $F=\rho_{\rm DE}(z)/\rho_{\rm DE0}$ |
| DESI-tracking | CPL, $w_0=-0.838$, $w_a=-0.62$ |
| Rival | $a_0\propto H(z)$ |
| Event horizon | $R_E(0)/R_E(z)$ (Section 4) |

---

## 3. Cold energy

Cold energy is energy carried as rest mass with low pressure. It is not a particle species. Two sectors exist, and their connection is OPEN.

### 3a. Carrier sector (MODEL)

$$\mathcal L_c=\partial_\mu\Phi^*\partial^\mu\Phi+\partial_\mu X^*\partial^\mu X-V_c$$

$$V_c=m^2|\Phi|^2+4m^2|X|^2+\Big|\sqrt{\Delta_c}\,X+\tfrac{g_c}{\sqrt{\Delta_c}}\Phi^2\Big|^2+\lambda_{\rm rep}|\Phi|^4$$

with $M=2m\sqrt{1+u_*^2}$, $\Delta_c=M^2-4m^2$, $\lambda_{\min}=g_c^2/\Delta_c$, $\lambda_{\rm tot}=\lambda_{\min}+\lambda_{\rm rep}$.

Field equations:

$$(\Box+m^2)\Phi+2g_cX\Phi^*+2\lambda_{\rm tot}|\Phi|^2\Phi=0,\qquad(\Box+M^2)X+g_c\Phi^2=0$$

- **Charge bound (DERIVED, isolated classical theory):** the U(1) symmetry $(\Phi,X)\to(e^{i\theta}\Phi,e^{2i\theta}X)$ gives $E\ge m|Q|$.
- **Production:** $\Gamma_c=\dfrac{g_c^2}{8\pi M}\sqrt{1-4m^2/M^2}$, with free-stream $P/\rho=\dfrac{u_*^2}{3(1+u_*^2)}$.
- **Pressure bound (fixed regulator):** $|P|/\rho_E\le b_+d/(1+d)$.
- **Not a cosmological result.** Source epoch, abundance and free streaming are missing.

### 3b. Fluid and field-stress sector (CFG660–699)

- **Fluid form:** Israel–Stewart, with $\eta=p\tau/2\alpha$, $\mathrm{Kn}=\sqrt2/4\alpha$, $\mathrm{Re}=4\alpha$.
- **Law as equilibrium:** the law is the exact equilibrium of field-aligned stress.
- **Tether:** $4\pi G\mathbf P=-g_c$ cancels cold self-gravity (CFG698, CFG743).
- **Relaxation (CFG747):** collisionless cold energy relaxes onto the law within 5 r_M to ≤2% from any start.
- **Abundance:** $\Omega_c\approx5.36\,\Omega_b$ is required, not derived.
- **Open:** a damping channel for settling (CFG744), and orbiting cold energy is unbound (CFG749).

---

## 4. Black holes

There is no black-hole action. What exists is a geometric relation and a set of tests (CFG775, CFG778).

### Geometry: one coincidence

$$q\equiv\frac{a_0}{cH_\infty}=\kappa\sqrt{\tfrac{3}{8\pi}}=0.1727\quad(\kappa=\tfrac12)$$

| relation | from q |
|---|---|
| $r_M=\sqrt{GM/a_0}$ divided by $\sqrt{r_sR_H}$ | $1/\sqrt{2q}$ |
| tether capacity $a_0/\pi G$ divided by horizon surface density | $8q$ |
| BH with surface gravity $a_0$, divided by horizon mass | $1/(2q)$ |
| $a_0$ divided by the de Sitter surface gravity | $q$ |

Each is the single statement $a_0\propto cH_\infty$. No horizon relation fixes q or the cold-energy amount.

### Black holes as the source of dark energy (k=3 coupled BHs)

$$\rho_{\rm DE}(z)=\epsilon\int_z^\infty\psi(z')(1+z')^3\left|\frac{dt}{dz'}\right|dz'$$

- **Amount:** $\epsilon_{\rm req}=3.9$–$4.6$ against a ceiling of about 0.05. Stellar remnants alone are EXCLUDED as the source.
- **Timing:** within 0.017–0.029 dex of DESI, so the shape nearly matches.

### Event-horizon branch (SEALED, sha256 `b9f3e827…`)

$$\frac{a_0(z)}{a_0(0)}=\frac{R_E(0)}{R_E(z)},\qquad R_E(a)=c\,a\int_a^\infty\frac{da'}{a'^2H(a')}$$

Values at z=2 are 1.46 (event horizon), 1.00 (flat), 0.85 (BH k=3).

---

## 5. What decides next

- **ALMA releases:** U4_27928 (2026-11-06) and GS4_24110 (2026-11-28), predictions sealed.
- **Gaia DR4 (2026-12-02):** Milky Way outer slope, K_z map, wide binaries.
- **The early-type failure:** needs an independent lensing survey or old-population σ_z.

Do not cite this as "the data favour the framework" or "theory closed".

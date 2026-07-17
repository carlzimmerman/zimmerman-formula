# The a0-Line: an Exact Identity of the dS-Unruh Modified-Inertia Law, and the Sharpest Available a0 Measurement It Enables

**Lane DERIVE — 2026-07-16.** Scripts in this directory (run order: `identity_uniqueness.py` → `estimator_theory.py` → `bayes_setup.py`; all exit 0 on real SPARC data, read-only from the frozen repo). This is the sharpest available measurement + model comparison **on the framework's own terms** — not a proof of anything, and explicitly **not** a TOE claim.

Framework: modified **inertia**, horizon-derived scale

$$a_0 = \frac{cH_\Lambda}{Z} = \frac{c^2\sqrt{\Lambda/3}}{Z},\qquad Z=\sqrt{\tfrac{32\pi}{3}}=5.78881,\qquad a_0^{\rm canon}=9.355\times10^{-11}\ {\rm m\,s^{-2}}$$

ALT footing ($\rho_{\rm total}/cH_0$): $a_0^{\rm ALT}=1.1305\times10^{-10}$. **Both footings are carried everywhere below.**

---

## 1. The identity (exact, all accelerations)

The framework's own interpolation $g_{\rm obs}=\sqrt{g_{\rm bar}^2+a_0 g_{\rm bar}}$, i.e. $\nu(y)=\sqrt{1+1/y}$ with $y=g_{\rm bar}/a_0$, squares to

$$\boxed{\;g_{\rm obs}^2-g_{\rm bar}^2 \;=\; a_0\,g_{\rm bar}\;}\qquad\text{exactly, at every }y.$$

The MOND excess $E\equiv g_{\rm obs}^2-g_{\rm bar}^2$ is a **straight line through the origin with slope $a_0$** — no deep-MOND selection, no interpolation fit, no approximation. (`identity_uniqueness.py` §A, sympy-verified.)

### Uniqueness (honestly characterized)

Demanding an exactly linear excess, $y^2(\nu^2-1)=\lambda y$ for all $y>0$, is a pointwise algebraic equation — elementary, but exact and exhaustive: the solution family is precisely

$$\nu_\lambda(y)=\sqrt{1+\lambda/y},$$

and $\lambda$ is pure $a_0$-rescaling ($\nu_\lambda(g/a_0)=\nu_1(g/\lambda a_0)$, sympy-verified). Fixing the standard deep-MOND normalization $g_{\rm obs}\to\sqrt{a_0 g_{\rm bar}}$ forces $\lambda=1$. **So $\nu=\sqrt{1+1/y}$ is the unique interpolation with an exactly linear excess, up to the definition of $a_0$ itself.** Every rival $\nu$ bends the line somewhere. (§B.)

### Rival excess formulas (each in its own convention; $\varepsilon(y)\equiv E/(a_0 g_{\rm bar}) = y(\nu^2-1)$)

| $\nu$ | $\varepsilon(y)$ | $y\to0$ | $y\to\infty$ |
|---|---|---|---|
| **framework** $\sqrt{1+1/y}$ | $1$ (exact) | 1 | 1 |
| **McGaugh/RAR-fit** $[1-e^{-\sqrt y}]^{-1}$, $g^\dagger=1.2\times10^{-10}$ | $y(\nu^2-1)$ | 1 | $\sim 2y\,e^{-\sqrt y}\to 0$ (superexponential death) |
| **simple** $\tfrac12+\sqrt{\tfrac14+1/y}$ | $1-\tfrac y2+\tfrac y2\sqrt{1+4/y}$ | 1 | **2** (persistent, slope $2a_0$) |

Separation ratio $R(y)=\varepsilon_{\rm fw}/\varepsilon_{\rm rival}$ (matched scale): $R_{\rm McG}=0.66$–$0.7$ at $y\sim1$–$3$, crosses 1 near $y\approx12$, then $4.0$ at $y=30$, $11.8$ at $y=50$, **$110$ at $y=100$** (the "×100 at $g_{\rm bar}\sim100a_0$" statement — computed, and it survives any choice of $g^\dagger$). Against simple-$\nu$ the ratio saturates at $1/2$: a factor-2 **shape** difference, not a decay — tail *persistence* alone does not separate framework from simple-$\nu$; exact *constancy* of $\varepsilon$ does. (§C–D.)

### Where SPARC actually samples (Q≤2, inc≥30°, $\Upsilon_d=0.70$)

153 galaxies, 3166 points: median $y=0.31$; $N(y>30)=47$, $N(y>50)=16$, $N(y>100)=1$. **The ×100 zone is at the extreme edge of SPARC**; the gas-dominated points live almost entirely at $y\lesssim$ a few. The gas subsample is the *slope* sample; the tail-shape test rides on star-dominated inner points where M/L errors are largest. (§E.)

---

## 2. E1 — the slope estimator and its honest error budget (`estimator_theory.py`)

**Estimator.** WLS through the origin: $\hat a_0=\sum w_iE_ig_i/\sum w_ig_i^2$, ${\rm Var}_{\rm stat}=1/\sum w_ig_i^2$. The prospectus form $\langle E/g_{\rm bar}\rangle$ is the $w\propto1/g^2$ special case.

**A real trap, caught and kept visible:** with $\sigma_E$ evaluated at the *observed* $g_{\rm obs}$, weights correlate with noise ($\mathbb E[w\,\epsilon]<0$, sympy §S1) and the real-data slope collapses to $4.2\times10^{-11}$ — a **×3 artifact, not a framework deficit**. Cure: iterated GLS with model-based errors and an intrinsic-scatter floor $f_{\rm int}\,g^2_{\rm obs,model}$ tuned to $\chi^2/N=1$ ($f_{\rm int}=0.64$).

**Distance scaling, derived exactly (§S2):** $\partial\ln g_{\rm bar}/\partial\ln D=0$ for **every** baryonic component (gas *and* stars — surface density is distance-independent; $M_{\rm gas}=2.36\times10^5 F_{21}D^2$, $r\propto D$), while $\partial\ln g_{\rm obs}/\partial\ln D=-1$. So the gas cut does **not** reduce distance sensitivity — it suppresses $\Upsilon$ only; gas-rich dwarfs (Hubble-flow distances, $\sigma_{\ln D}\approx25\%$) actually carry a *larger* per-galaxy distance term, tamed only because $D$ errors are independent across galaxies while $\Upsilon$ is a global calibration.

**Per-point sensitivities of $a_{0,\rm pt}=E/g_{\rm bar}$ (§S3, all sympy-verified):**

$$\frac{\partial a_{0,\rm pt}}{\partial\ln D}=-2a_0(y{+}1),\quad \frac{\partial a_{0,\rm pt}}{\partial\ln\sin i}=-4a_0(y{+}1),\quad \frac{\partial a_{0,\rm pt}}{\partial v/v}=+4a_0(y{+}1),$$
$$\frac{\partial a_{0,\rm pt}}{\partial\ln\Upsilon}=-\varphi\,a_0(2y{+}1),\qquad \frac{\partial a_{0,\rm pt}}{\partial\ln({\rm gas\ cal})}=-(1{-}\varphi)\,a_0(2y{+}1),$$

with $\varphi$ = stellar share of $g_{\rm bar}$. Every lever arm grows $\propto y$: **the high-$g$ points where rivals separate most are exactly where the estimator is most fragile** (a 10% $\Upsilon$ error at $y=30$ biases $a_{0,\rm pt}$ by $\sim-6a_0$). The a0-line **inherits the full banked RAR $a_0$–$\Upsilon$ degeneracy on star-dominated points** — as the banked wall says.

**Real-SPARC budget** (Q≤2, inc≥30°, $e_V/V<10\%$; $\Upsilon_d=0.70$, $\Upsilon_b=1.4\Upsilon_d$; fiducials: $\sigma_{\ln D}$ by SPARC $f_D$ flag {HF 25%, TRGB/Cep 5%, UMa 10%, SNIa 8%}, $\sigma_i=3°$, $\sigma_{\ln\Upsilon}=0.1$ dex global, gas cal 10% global):

| sample | N (gals) | $\hat a_0$ GLS | median $E/g$ | stat | dist | inc | $\Upsilon$ | gas | estim. | **total** |
|---|---|---|---|---|---|---|---|---|---|---|
| FULL | 2696 (147) | $1.279\times10^{-10}$ | $0.88\times10^{-10}$ | 0.02 | 0.06 | 0.02 | **0.35** | 0.04 | 0.20 | **0.41** (32%) |
| GAS-DOM | 310 (49) | $1.181\times10^{-10}$ | $0.97\times10^{-10}$ | 0.05 | 0.08 | 0.03 | 0.10 | 0.09 | 0.10 | **0.19** (16%) |

(σ columns in $10^{-10}$ m s⁻²; gas-dominated = point-level $V_{\rm gas}^2>\Upsilon_dV_{\rm disk}^2+\Upsilon_bV_{\rm bul}^2$.)

Tensions: FULL $+0.84\sigma$/canon, $+0.36\sigma$/ALT; **GAS $+1.29\sigma$/canon, $+0.27\sigma$/ALT.** Statistical error is negligible — the measurement is systematics-owned.

**The $\Upsilon$ swing (the banked degeneracy, quantified):** over $\Upsilon_d=0.5\to0.8$, FULL $\hat a_0$ swings $1.89\to1.10\times10^{-10}$ (62% — the banked P1 profiling swing $1.76\to0.88$ reproduced in a different metric); GAS swings only $1.36\to1.13\times10^{-10}$ (19%). **The gas cut kills 71% of the $a_0$–$\Upsilon$ degeneracy**; the gas slope is $a_0=(1.1$–$1.4)\times10^{-10}$ across the *entire* physical M/L range.

**The shape test (framework vs McGaugh vs simple, scale AND $\Upsilon$ profiled, common error model):** min-$\chi^2$ 1860.4 / 1858.8 / 1867.5 — **framework-vs-McGaugh is a wash ($|\Delta\chi^2|\approx2$)**; simple-$\nu$ mildly disfavored ($\Delta\chi^2\approx+7$, same direction as the banked log-space 0.108-vs-0.122 dex result). At fixed $\Upsilon=0.7$–$0.8$ the framework beats McGaugh ($\Delta\chi^2\approx-32$ to $-54$); at $\Upsilon=0.5$ it loses — the verdict is $\Upsilon$-assumption-dependent, i.e. **not a discriminator today.** The $y>30$ tail contributes $\Delta\chi^2\sim0.2$ on 15–20 points.

---

## 3. E2 — the inversion: galaxies → Λ (`bayes_setup.py` Part 3)

$$a_0=\frac{c^2\sqrt{\Lambda/3}}{Z}\;\Longleftrightarrow\;\boxed{\;\Lambda=\frac{3Z^2a_0^2}{c^4}\;}$$

Gas-dominated slope → $\Lambda_{\rm pred}=1.74\times10^{-52}$ m⁻² (GLS) / $1.18\times10^{-52}$ (median) vs Planck $1.089\times10^{-52}$: ratio 1.08–1.6, i.e. $+1.45\sigma$ (GLS) / $+0.24\sigma$ (median) at $\sigma_{\ln\Lambda}=2\sigma_{\ln a_0}=0.32$. Rotation curves of gas-rich dwarfs recover the cosmological constant to a factor ~1.1–1.6 across 52 a-priori orders of magnitude. **This is the banked $a_0\sim cH/Z$ coincidence reframed as an inversion — same information content, sharper falsification target** (a future gas slope at $3\times10^{-10}$ would break it).

---

## 4. E3 — the Occam/Bayes factor (`bayes_setup.py` Parts 1–2)

With likelihood Gaussian in $x=\ln a_0$ (width $s$ = total fractional error) and M1 prior log-flat width $W$:

$$B_{01}=\underbrace{\frac{W}{\sqrt{2\pi}\,s}}_{\text{Occam factor}}\;\underbrace{e^{-t^2/2}}_{\text{fit penalty}},\qquad t=\frac{\ln a_0^*-\ln\hat a_0}{\sqrt{s^2+s_{\rm anchor}^2}}$$

(closed form sympy-derived; numeric quadrature agrees to <0.01 ban; Planck anchor width ±1% folded in).

**Headline (gas GLS, log-flat $[10^{-11},10^{-9}]$): $B_{01}=+0.60$ bans (canonical), $+1.04$ bans (ALT).** Sensitivity: 4-decade prior +0.90/+1.34; 1-decade +0.30/+0.74; linear-flat +0.86/+1.29; median-estimator variant +1.04/+0.87. **Canonical-vs-ALT: 0.44 bans toward ALT — under 1 ban, the footing fork is NOT decided** (consistent with the banked 21%-apart non-diagnosticity). The bans are a formalization of *predicted-not-fitted*, not new data; they are capped by the honest systematics — a ×3 error reduction (TRGB distances for the gas dwarfs) would make the same agreement worth ~+1.5–2 bans.

---

## 5. THE HONEST BOTTOM LINE (what each piece adds beyond the banked non-diagnosticity)

The banked wall stands: **the full-sample slope is exactly as $\Upsilon$-degenerate as the RAR** (62% swing over physical M/L, reproduced here in the line metric — the a0-line on all of SPARC is a beautiful reframing, not new information). What is genuinely new, quantified:

1. **The identity itself** — an algebraically special property (unique $\nu$ with exactly linear excess): it converts "fit an interpolation" into "measure one slope," which is what makes items 2–4 possible. Conceptual, zero new bits by itself.
2. **The gas-dominated subsample kills 71% of the $a_0$–$\Upsilon$ degeneracy** — the single-number result: $\hat a_0^{\rm gas}=(0.97$–$1.18)\times10^{-10}\pm16\%$ *regardless of M/L*. But it does **not** kill distance errors ($g_{\rm bar}\propto D^0$ exactly for gas *and* stars; $g_{\rm obs}\propto1/D$ for both), and it lands **between the two footings**: canonical $+1.3\sigma$, ALT $+0.3\sigma$ — mild, non-decisive lean toward ALT; the 21% footing fork survives.
3. **The linearity/tail shape test adds almost nothing today**: framework-vs-McGaugh $\Delta\chi^2\approx2$ with M/L profiled (verdict flips sign across the physical $\Upsilon$ range); the ×100 separation zone ($y\sim100$) contains one SPARC point. It becomes decisive only with $y\gtrsim50$ data carrying M/L-independent masses.
4. **The Occam factor is +0.6–1.0 bans** — positive, prior-robust to within ±0.4 bans, and modest; "substantial", not "decisive", on Jeffreys' scale.

**Solar-system consistency (banked story, restated not rederived):** the persistent $a_0g_{\rm bar}$ excess at high $g$ is galaxy-safe here; in the planetary regime the banked gated-corner mechanism suppresses the excess at planetary orbital frequencies $\Omega\gg\omega_c$, not at galactic $\omega\ll\omega_c$ — so the excess *should* persist in galaxy inner regions (as the identity requires) while remaining Cassini-compatible via the frequency gate. The Cassini Q₂ quadrupole tension inherited by the AeST(=MG) realization is a separate, banked open item and is not touched by this lane.

**Not claimed:** no derivation of $Z$'s value from data, no TOE, no "SPARC pins $9.36\times10^{-11}$", no resolution of the footing fork, no rival-$\nu$ kill.

### Files
- `identity_uniqueness.py` — §A identity, §B uniqueness family, §C rival excesses, §D separation table, §E SPARC sampling census.
- `estimator_theory.py` — S1 WLS + bias trap, S2 distance scaling, S3 sensitivities, S4 budget, S5 $\Upsilon$ swing, S6 shape test. Writes `estimator_results.json`.
- `bayes_setup.py` — evidence closed form + quadrature, prior sensitivity, footing comparison, E2 inversion. Writes `bayes_results.json`.

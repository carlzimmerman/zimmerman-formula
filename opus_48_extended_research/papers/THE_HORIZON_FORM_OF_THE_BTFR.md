# The Horizon Form of the Baryonic Tully–Fisher Law

### The acceleration scale as the de Sitter horizon's surface gravity, the zero-parameter mass law it fixes, and an honest accounting of what that buys

**Carl Zimmerman** — Briar Creek Tech, Charlotte, North Carolina, USA
**Draft:** 2026-09-16. Both footings throughout (canonical $a_0 = 9.3619\times10^{-11}\,\mathrm{m\,s^{-2}}$, alt $1.1279\times10^{-10}$). Every number is a committed, re-runnable artifact of a cited gate.

---

## Abstract

We write the deep-MOND baryonic Tully–Fisher law in a form that carries no acceleration scale explicitly:
$$v_{\rm flat}^4 = \frac{G M_b\,c^2}{Z\,R_{\rm dS}},\qquad Z = 2\sqrt{8\pi/3} = 5.7888,\qquad R_{\rm dS} = \frac{c}{H_0\sqrt{\Omega_\Lambda}}.$$
The right-hand side is the baryon mass times the **surface gravity of the de Sitter horizon**, $\kappa_{\rm dS} = c^2/R_{\rm dS}$, divided by the pure number $Z$. Numerically $\kappa_{\rm dS}/Z = 9.3624\times10^{-11}\,\mathrm{m\,s^{-2}}$, matching the fitted $a_0$ to $+0.0051\%$. We are explicit that this is a **re-expression, not a derivation**: $Z \equiv \kappa^{-1}\cdot(\text{Friedmann bookkeeping})$, so the horizon form contains exactly the physics of the single fitted coefficient $\kappa = \tfrac12$ and not one bit more. What the form does earn is conceptual and testable — it makes every galactic scale a function of $(GM_b, R_{\rm dS})$ with no independent length or acceleration, and it converts the BTFR zero point into a pre-registered geometric target. The zero point is the content: the clean rotation-dominated core of a 542-object, 12-decade sample sits **on** the horizon value ($z = -0.20$), while the full equal-weight ladder sits $+0.26$ dex above it ($z = +6.3$, a registered departure traced to catalogue M/L normalisation, not a kill). Around this scale we state the zero-parameter mass law $M_{\rm dark}(<r)/M_b = r/r_M$ and report its wave-1 test on eight instruments (0.03–0.22 dex). We close with the two liabilities that decide the programme and are **not** resolved here: the coefficient $\kappa=\tfrac12$ is fitted and provably underivable by the candidate action, and the non-relativistic completion faces a Cassini-vs-lensing pincer that the equilibrium reading evades only by an as-yet-unclosed relaxation assumption.

---

## 1. The horizon form

The deep-MOND limit of the baryonic Tully–Fisher relation is $v_{\rm flat}^4 = G M_b a_0$. Substitute the framework's identification of the acceleration scale with the cosmological constant, $a_0 = \kappa\, c\sqrt{G\rho_\Lambda}$ with $\rho_\Lambda = 3 H_0^2\Omega_\Lambda/(8\pi G)$ and $\kappa=\tfrac12$:

$$a_0 = \frac{c^2}{Z R_{\rm dS}} = \frac{\kappa_{\rm dS}}{Z},\qquad \kappa_{\rm dS}\equiv\frac{c^2}{R_{\rm dS}},\qquad R_{\rm dS}=\frac{c}{H_0\sqrt{\Omega_\Lambda}}=1.6583\times10^{26}\,\mathrm{m}=5.37\,\mathrm{Gpc}.$$

Then

$$\boxed{\,v_{\rm flat}^4 = \frac{G M_b\,c^2}{Z R_{\rm dS}}\,}$$

with $\kappa_{\rm dS} = 5.4197\times10^{-10}\,\mathrm{m\,s^{-2}}$ and $\kappa_{\rm dS}/Z = 9.3624\times10^{-11}$. The flat rotation speed of a galaxy is thus fixed by its baryon mass and the horizon radius alone.

### 1.1 What $Z$ is, stated without varnish

$Z$ is **not a second constant**. It is the fitted coefficient in disguise. With $H^2 = 8\pi G\rho/3$ (Friedmann) the ratio $cH/a_0$ is
$$Z^2 = \frac{8\pi}{3\kappa^2}\quad\Longrightarrow\quad \kappa=\tfrac12 \iff Z = \sqrt{32\pi/3} = 2\sqrt{8\pi/3} = 5.7888,$$
verified symbolically on four independent routes (`opus_48_extended_research/reviews/ROUTE{2,4,5}_*`, `FRONTIER5_*`). The $\sqrt{8\pi/3}$ is pure conversion between $H$ and $\rho$; the leading factor is $1/\kappa$. Consequently:

- **"$Z = 5.789$ matches via Friedmann" is a tautology, never a data confirmation** — $H$ cancels for *any* $(\rho,H)$ on the Friedmann relation. The only data content is (i) the *magnitude* of $a_0$ and (ii) *which* density enters ($\rho_\Lambda$, not $\rho_{\rm crit}$; the latter inflates $a_0$ by $1/\sqrt{\Omega_\Lambda}=1.208$).
- The variants $a_0 = cH_\Lambda/Z$ (with $H_\Lambda = H_0\sqrt{\Omega_\Lambda}$), $a_0 = c^2/(ZR_{\rm dS})$, and $a_0 = \kappa_{\rm dS}/Z$ are the **same statement**. A machine-precision check this session: $c^2/(ZR_{\rm dS})$ and $(c/2)\sqrt{G\rho_\Lambda}$ agree at ratio $1.0000000000000002$.
- The often-quoted $cH_0/a_0 = 6.994$ is the *same* $Z$ measured against $H_0$ instead of $H_\Lambda$: $6.994\times\sqrt{0.685} = 5.789$. Not a third number.

**The honest content of §1, then, is a change of variables**: it trades the fitted $a_0$ for the fitted $\kappa$ and exhibits the length that sets the scale as the de Sitter horizon. That reframing is worth making — it is falsifiable through the zero point (§3) and it fixes the coincidence-of-scales question by parameter count — but it derives nothing that $\kappa=\tfrac12$ did not already assume.

### 1.2 Why a horizon *surface gravity* is a natural home for $a_0$

The interpretation is not arbitrary. $a_0\sim c H$ has been noted since Milgrom; the sharpening here is that the *pure-$\Lambda$* rate $H_\Lambda = c\sqrt{\Lambda/3}$, not the instantaneous $H(z)$, is what the identification requires if the zero point is to be flat in cosmic time (the distinctive prediction; §5). The de Sitter horizon at $R_{\rm dS} = c/H_\Lambda$ has surface gravity $\kappa_{\rm dS}=c^2/R_{\rm dS}$, and $a_0$ is that surface gravity reduced by $Z$. We do **not** claim a first-principles $Z$ — see §6.1 — but the geometry is the right geometry: a constant vacuum energy sets a fixed horizon, a fixed horizon sets a fixed surface gravity, and a fixed surface gravity sets a time-independent galactic scale.

---

## 2. The mass law the scale fixes

Given the scale, the framework's galactic content is a one-line mass law with **zero free parameters**:

$$\frac{M_{\rm dark}(<r)}{M_b} = \frac{r}{r_M},\qquad r_M \equiv \sqrt{\frac{G M_b}{a_0}} = \sqrt{\frac{G M_b\,Z R_{\rm dS}}{c^2}}.$$

Its immediate consequences, all definitional given $r_M$ and therefore not themselves predictions but *bookkeeping identities* worth stating once:

- $g(r_M) = a_0$ for every galaxy at every mass ($r_M$ is defined as the radius where baryonic $g = a_0$);
- $M_{\rm dark}(r_M) = M_b$ (equipartition at the MOND radius; Lean-certified, `G090`/`G083`, both compile clean, axioms $\{$propext, Classical.choice, Quot.sound$\}$, zero `sorry`);
- $\sigma^2 = v_{\rm flat}^2/2$ (the isothermal triad, $\kappa = \sigma^2/v_{\rm flat}^2 = c_s^2 = 1/2$; the coefficient $1/2$ is $\kappa$, fitted);
- the mean phantom surface density within $r_M$ is universal, $\langle\Sigma_{\rm ph}\rangle = a_0/(\pi G) = 213.8\,M_\odot\,\mathrm{pc^{-2}}$.

> **Priority, stated plainly.** The universal surface density $a_0/(\pi G)$ is the standard MOND central-surface-density result (Milgrom 2009); Donato et al. (2009) measured $\log_{10}\mu_{0D}=2.15\pm0.05$ against it. It is not novel to this framework and we do not present it as such. What is new is the *combination*: a single fitted coefficient tying the surface density, the BTFR zero point, the isothermal temperature, and the dark-energy density to one horizon scale.

### 2.1 The re-expression table

No galactic constant retains an independent scale; each is a function of $(GM_b, R_{\rm dS}, Z)$:

| quantity | committed form | horizon form | value |
|---|---|---|---|
| $a_0$ | $\kappa c\sqrt{G\rho_\Lambda}$ | $c^2/(ZR_{\rm dS})$ | $9.362\times10^{-11}$ |
| $r_M$ | $\sqrt{GM_b/a_0}$ | $\sqrt{GM_b Z R_{\rm dS}/c^2}$ | $7959\,\mathrm{AU}$ (Sun), $9.84\,\mathrm{kpc}$ ($6.5\!\times\!10^{10}M_\odot$) |
| $\langle\Sigma_{\rm ph}\rangle$ | $a_0/\pi G$ | $c^2/(\pi G Z R_{\rm dS})$ | $213.8\,M_\odot\mathrm{pc^{-2}}$ |
| $\sigma$ (anchor $6.5\!\times\!10^{10}$) | $\sqrt{GM_ba_0}/2$ | $\tfrac12\sqrt{GM_bc^2/(ZR_{\rm dS})}$ | $119.2\,\mathrm{km/s}$ |

Every entry reproduces its committed register to $\le 0.3\%$ (`Z11`, 19/19 numerical checks).

---

## 3. The zero point is the test

Because the horizon form fixes the BTFR *zero point* — not just its slope — it is falsifiable by a single well-measured system. We pre-register the target and report status honestly.

**Target (pre-registered).** The slope-fixed absolute BTFR zero point must sit at $a_0 = c^2/(ZR_{\rm dS}) = 9.3624\times10^{-11}\,\mathrm{m\,s^{-2}}$ to $1\%$ (kill band $[9.270, 9.456]\times10^{-11}$).

**Kill rule (pre-registered).** Any *single well-measured system* — a $z\approx2.5$ JWST BTFR, a clean SPARC-class rotation sample, a GEMS-type group — whose slope-fixed $a_0$ lands $>3\sigma$ off the horizon zero point kills the geometric reading.

**Status, both ways (this is the working rule — verify the departure as hard as the agreement):**

- The **clean rotation-dominated core** (bright dSph + HI + SPARC, $n=104$) sits at $a_0 = 0.976\,a_{0,H}$, $z = -0.20$: **on the horizon value.**
- The **full 542-object, 12-decade equal-weight ladder** sits at $1.81\,a_{0,H}$, $+0.2585$ dex, $z = +8.98$ (stat) / $+6.31$ (stat+sys): a **registered departure.**
- The departure is *not* reported as a confirmation of the theory and *not* as a kill. Its decomposition: $\sim56\%$ is the ATLAS3D internal $M/L_{\rm JAM}$ zero point (a named systematic, not a rotation measurement), the remainder the registered end-populations (cluster $f_b$; UFD dSph disequilibrium). Per-catalogue the pull is entirely at the ends: SPARC $0.66\,a_{0,H}$, HI $1.19$, GEMS $1.33$, GC $1.40$ (all within $\sim1.7\sigma$); ATLAS3D $2.02$ and UFD dSph $7.4$ and clusters $12.2$ carry the offset.

**The decider is a system measured as a system**, not the pooled multi-catalogue ladder. If a clean deep-MOND system confirms the $+0.26$-dex offset, the horizon reading dies; if the offset dissolves under a catalogue-normalisation audit, it stands. Gaia DR4 (Dec 2026), a $z\approx2.3$–$2.9$ lensed rotator, and DESI are the instruments.

---

## 4. Wave-1: the mass law on eight instruments

The mass law of §2 was tested on eight independent instruments, every lane a committed script carrying its own pre-registered verdict including its failures:

| instrument | data | verdict | number |
|---|---|---|---|
| dSph floor | Simon 2019, 34 objects | PASS (V2 FAIL) | median $|\log_{10}({\rm pred}/{\rm obs})| = 0.222$; UFD faint end fails — the boundary |
| SPARC full curves | 35 isolated galaxies, 641 rings | PASS | pooled rms $0.145$ dex, zero parameters |
| Milky Way | Eilers+19 / Ou+24 | 5/5 | $v_c(8.2)$ within 5%; break $6.74$ vs $6.1$ kpc; $\rho_{\rm dark}(R_0)=0.0081$ |
| lensing floor | KiDS-1000 (Brouwer 2021) | 4/5 (V2 FAIL) | mass independence $0.033$ dex; floor$+$free-dust split $-0.355$ dex |
| GC boundary | Baumgardt & Hilker 2018 | 7/7 | crossing at $M=1.2\times10^5 M_\odot$, $r_M/r_h=\eta/2=3.39$ exact |
| cluster triad | X-COP, 12 clusters | 6/11 (FAIL = the finding) | $T_{\rm pred}/T_{\rm obs}=0.28=(\sigma_{\rm pred}/\sigma_{\rm dyn})^2$; amplitude an input |
| sheet/funnel | MW + slab | 4/4 | $z_c(8.2)=140.6$ pc; DR4 fingerprint |
| stability | isothermal mode analysis | 4/4 | $\omega^2=0$ exact, marginal; **local** stability only |

**Corrections carried from the wave-1 audit (`real_research/WAVE1_SUMMARY_AUDIT_2026-09-15.md`), so this paper does not repeat the summaries' overreach:**
- the lensing lane used **one survey** (KiDS), not "KiDS + DES-Y3"; no public DES-Y3/HSC galaxy-galaxy lensing RAR exists;
- the cluster amplitude is an **input**, not a prediction — the triad scales the temperature *formula* across 8 decades but the normalisation is set by free dust;
- the stability lane (`G081`) closes **local linear** stability ($\omega^2=0$ exact, cap-invariant, zero-mode residual $1.8\times10^{-12}$ after the mid-audit fix) but says nothing about **attainment**; whether the dust *relaxes* to $(\sigma^2, r_M)$ is the open half, and a Newtonian dust suite already failed that attractor form (`G035`).

---

## 5. What is distinctive, and what is shared

Set against the bar "made by no other framework," most of the identities above are deep-MOND results or definitions. Being explicit protects the two claims that are genuinely distinctive:

**Distinctive to this framework:**
1. **A flat zero point in cosmic time.** Because the scale is $\rho_\Lambda$ (constant for $w=-1$), not $\rho_{\rm crit}(z)$, the deep-MOND BTFR zero point is predicted flat: $0.00$ dex evolution to $z\approx2.5$, versus $+0.33$ dex for a $\Lambda$CDM-native rising RAR scale. This is the sharp discriminator (pre-registered at $\pm0.13$ dex). *Caution recorded 2026-09-10:* the naive $a_0\propto H(z)$ branch is **not** the distinctive one — it coincides with $\Lambda$CDM's $g^\dagger\sim\sqrt{G\rho_{\rm crit}}\propto H$. The FLAT law is what $\Lambda$CDM cannot mimic.
2. **The EFE break radius** $r_{\rm cap} = (a_0/g_{\rm ext})\,r_M$ — a halo truncation set by environment (`L242`).

**Shared with GR / $\Lambda$CDM / MOND, and not to be sold as distinctive:** $g(r_M)=a_0$, $M_{\rm dark}(r_M)=M_b$, the surface density (Milgrom 2009), the BTFR zero-point amplitude (deep-MOND), $c_T=c$ and no scalar hair (GR and most healthy scalar-tensor theories).

---

## 6. The two liabilities that decide the programme

This paper would be dishonest without them. Neither is resolved here.

### 6.1 The coefficient is fitted and provably underivable by the candidate action

$\kappa=\tfrac12$ is an empirical boundary condition (measured $0.551\pm0.043$ distance-free, $0.465\pm0.076$ BTFR; four candidate coefficients sit inside $2\sigma$). The `kappa_closure` programme (`k01`–`k04`) shows it is **not** derivable from the candidate action: the MOND primitive enters the field equations only through $J'$ and the background only through a normalisation zero mode; the $\Lambda$-free repair gives a vacuum energy of the wrong sign and $220\times$ too small; a sequestering-type global constraint misses by five orders; the four-form promotion makes $a_0\propto\sqrt{G\rho_\Lambda}$ *structural* but leaves $\kappa$ a free ratio. The one coefficient-free alternative, $a_0=c^2/(2\pi L_{\rm dS})$ ($\kappa=0.461$), is below the BTFR mass-budget floor and **exactly degenerate with the $H_0$ tension**. So: the *form* $a_0\propto\sqrt{G\rho_\Lambda}$ is defensible; the *number* $Z=5.789$ is $\kappa=\tfrac12$ restated, and $\kappa=\tfrac12$ is a fit. Its determination is a precision problem ($M/L$ zero point, absolute gas scale, $H_0$), not a theory result of this class. (Published: `kappa_closure`, DOI 10.5281/zenodo.22559892.)

### 6.2 The non-relativistic completion faces a Cassini-vs-lensing pincer

The kernel that reproduces the RAR ($\nu_{\rm RAR}$) has a non-relativistic pincer, both arms now numbers (field-theory arm, `hunt_2026/f23`–`f28`):
- **as modified gravity**, the framework's own kernel gives the Solar System an external-field quadrupole of $6.2$–$6.8\times$ (QUMOND) / $7.7$–$8.8\times$ (exact AQUAL) the Park 2026 Cassini ceiling;
- **as modified inertia**, it is lensing-dead at $\sim20\sigma$;
- no one-argument static law $\mu(g/a_0)$ passes both.

What separates the Sun at $0.1$ pc from a galaxy at $10$ kpc *at the same acceleration* is a **length**, not a second acceleration. The surviving non-relativistic thread is the **coherence-length law**: QUMOND on a Helmholtz-smoothed potential $(1-\xi^2\nabla^2)\tilde\Phi=\Phi_N$, which breaks the Cassini$\leftrightarrow$wide-binary lock at $\xi\approx0.05$ pc (Solar System safe for $\xi\ge0.045$ pc $=$ one solar MOND radius; the pre-registered wide-binary boost survives). $\xi$ is a **new parameter**, not one of the framework's own (which are Gpc), and its candidate local action has four undone calculations (Solar-System solve, PPN, Dirac count, FLRW background). The equilibrium reading of §2/§4 evades Cassini "by construction" (no phantom in the strong field), but only by the attainment assumption §4 flags as open.

---

## 7. Statement

The acceleration scale can be written as the surface gravity of the de Sitter horizon reduced by a pure number, and the galactic mass law that follows is a zero-parameter, eight-instrument-tested description of rotation curves, dwarf dispersions, lensing floors, and the cluster-scale boundary where it fails. This is real and it is narrow. The horizon form is a change of variables that makes the single fitted coefficient a horizon geometry; it does not derive that coefficient, and honesty requires saying so in the same breath as the boxed equation. The programme's fate rests on two things this paper does not settle: whether $\kappa=\tfrac12$ is a number a completed action must return or a boundary condition the data pin, and whether the non-relativistic completion can put a length between the Sun and a galaxy without a phantom the Solar System forbids. The one prediction that is both distinctive and armed — a BTFR zero point flat in cosmic time — is decided not by the pooled ladder that departs today but by a single clean system, and the instruments to measure it are in the field.

---

*All quantities are committed, re-runnable artifacts. Load-bearing gates: `Z11` (horizon form, 19/19), `G070`–`G092` (wave-1 mass law), `G090`/`G083` (Lean), `kappa_closure/k01`–`k04` (coefficient), `hunt_2026/f23`–`f30` (non-relativistic pincer and coherence length). Corrections applied per `real_research/WAVE1_SUMMARY_AUDIT_2026-09-15.md`. Both footings throughout. No claim here is presented as more than its gate earns.*

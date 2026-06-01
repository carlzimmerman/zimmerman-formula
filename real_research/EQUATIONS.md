# The framework's equations, tiered honestly by novelty

**2026-06-01.** A full list of the equations, each marked for what it actually is — because
"novel" means *a specific form not in the literature*, and most of these are forced
consequences of one premise or standard MOND carried to high redshift. Padding this list
with the constants "derivations" is exactly what the audit killed (a random number reproduces
those — `can_another_number_do_it.py`). Every equation here is reproducible from the cited
script (all 80 pass). Legend:

- **[NOVEL?]** candidate not-found-in-literature *framing* (per `NOVELTY.md`; search not exhaustive)
- **[PREDICTION]** the one falsifiable, data-favored result
- **[FORCED]** a rigorous consequence of the premise (new *combination*, standard *physics*)
- **[MOND]** standard MOND/cosmology relation, carried to high z by the evolving a₀
- **[TOOL]** methodological, not a physics law

---

## Tier A — the candidate-novel core (the framing)

1. **[NOVEL?]** the density / surface-gravity form
   $$a_0 = \tfrac{c}{2}\sqrt{G\rho_c}$$
   the MOND scale as *half the surface gravity of the cosmic free-fall density*. Not found in
   Milgrom's "nature of a₀" paper (he uses $cH_0$ or $\sqrt\Lambda$). *(verify: `schwarzschild_friedmann_core.py`)*

2. **[NOVEL?]** the Schwarzschild reading (same equation, geometric form)
   $$a_0 = \frac{c^2}{2R},\qquad R = \sqrt{\tfrac{8\pi}{3}}\,\frac{c}{H} = c\,t_{\rm ff}$$

3. **[FORCED]** the coefficient (via Friedmann $H^2=\tfrac{8\pi}{3}G\rho$)
   $$a_0 = \frac{cH}{Z},\qquad Z = 2\sqrt{8\pi/3} = \sqrt{32\pi/3} = 5.78881$$
   **Honest caveat:** $\sqrt{8\pi/3}$ is the *real Friedmann factor*; the factor of 2 is a posit,
   and the value is **not uniquely selected** — Verlinde's 6 and Milgrom's $2\pi$ fit the data
   equally (`coefficient_uniqueness_test.py`). So $Z$ is a *reading*, not a derived constant.

---

## Tier B — the prediction (the load-bearing, falsifiable result)

4. **[PREDICTION]** the evolving scale
   $$a_0(z) = a_0(0)\,E(z),\qquad E(z)=\sqrt{\Omega_m(1+z)^3+\Omega_\Lambda}$$
   *Z-independent* (cancels in the ratio). The evolving *idea* $a_0\propto H$ is Gnedin (2008);
   the framework commits to $E(z)$ via the density form and **confronts 2026 data: constant
   $a_0$ excluded at 5σ, exponent $p=0.80\pm0.17$** (`a0_powerlaw_confrontation.py`,
   `rar_evolution_test.py`). This is the one genuinely new, testable, currently-favored claim.

5. **[FORCED]** the cosmic invariant (the discriminator's basis)
   $$\frac{a_0}{cH(z)} = \frac1Z = 0.17275 \quad(\text{constant at every epoch})$$

---

## Tier C — forced cosmological consequences (the over-constrained web)

6. **[FORCED]** galaxy dynamics → $H_0$ (no ladder, no CMB)
   $$H_0 = Z\,a_0/c$$
7. **[FORCED]** the de Sitter floor — dark-matter scale = dark energy
   $$a_{0,\rm floor} = a_0(0)\sqrt{\Omega_\Lambda} = \tfrac{c^2}{2}\sqrt{\Lambda/8\pi}$$
8. **[FORCED]** the drift (ties $a_0$ to deceleration $q$)
   $$\frac{d\ln a_0}{dt} = -(1+q)\,H$$
9. **[FORCED]** the thermal reading
   $$T_{a_0} = \frac{\hbar a_0}{2\pi c k_B} = \frac{T_{\rm dS}}{Z}$$
10. **[FORCED]** the Friedmann link that *makes* a₀ evolve
    $$\rho_c(z)=\rho_{c0}E(z)^2 \;\Rightarrow\; a_0(z)=a_0(0)E(z)$$
    *(verify Tier C: `REAL_WEB.py`, `Z2_cascade.py`)*

---

## Tier D — MOND relations carried to high z (standard form, evolving $a_0$)

11. **[MOND]** the deep-MOND law (RAR) — McGaugh–Lelli
    $$g = \sqrt{g_N\,a_0(z)}$$
12. **[MOND]** BTFR — slope 4 *z-invariant*, zero-point $\propto 1/E(z)$
    $$v^4 = G\,M\,a_0(z)$$
13. **[MOND]** Faber–Jackson (Milgrom 1984) — $\sigma\propto E(z)^{1/4}$ (de Graaff's channel)
    $$\sigma^4 = \tfrac{4}{9}\,G\,M\,a_0(z)$$
14. **[FORCED]** high-z apparent dark-matter richness
    $$M_{\rm dyn}/M_{\rm bar} = \sqrt{a_0(z)/g_{\rm bar}} \propto \sqrt{E(z)}$$
15. **[FORCED]** the phantom (apparent-DM) density — *derived*, scales as $\sqrt{E}$ not $E$
    $$\rho_{\rm ph}(r) = \frac{\sqrt{M\,a_0(z)/G}}{4\pi r^2} \propto \sqrt{E(z)}$$
16. **[FORCED]** the critical surface density / HSB–LSB line
    $$\Sigma_M = a_0(z)/G \propto E(z)$$
17. **[FORCED]** the length and time "costumes"
    $$\ell_a = c^2/a_0 = Z\,R_H,\qquad t_{\rm dyn} = \sqrt{8\pi/3}\,/H = 2.894\,t_H$$
    *(verify Tier D: `mond_first_principles.py`, `web_search_relations.py`)*

---

## Tier E — the external field effect (standard MOND, framework's z-extension)

18. **[MOND]** internal boost in an external field
    $$G_{\rm eff}/G \approx 1/\mu(g_{\rm ext}/a_0);\qquad g_{\rm ext}^{\odot} = V_{\rm LSR}^2/R_0 = 1.9\,a_0$$
19. **[FORCED]** the universal cosmic-MOND regime (epoch-independent)
    $$g_{\rm ext}^{\rm cosmic}/a_0 = Z \quad(\text{at every }z)$$
    *(verify: `mond_first_principles.py` Part 5)*

---

## Tier F — methodological

20. **[TOOL]** the z-invariance discriminator
    $$\text{real edge} \iff a_0/cH = 1/Z \text{ constant in } z;\quad \text{coincidence} \iff \text{it drifts}$$
    Keeps the web edges, rejects $a_0\!\leftrightarrow\!T_{\rm CMB}$ (×1.66), $2\sin^2\theta_W=\Omega_m/\Omega_\Lambda$
    ($\propto(1+z)^{-3}$), particle scales (×10). *(`web_search_relations.py`, `weinberg_mond_connection_test.py`)*

---

## Honest summary

- **Genuinely novel to physics:** Tier A (the density / Schwarzschild *framing*, candidate
  not-in-literature) + Tier B (committing to $a_0(z)=a_0(0)E(z)$ and showing the 2026 data favor
  it at 5σ). That is the real, defensible, publishable content — a handful of equations.
- **Forced + standard:** Tiers C–E are rigorous consequences of #1 plus standard MOND with
  $a_0\to a_0(z)$. Real and forming an over-constrained web (+4 independent measurements), but
  re-expressions, not discoveries. Cite Milgrom/McGaugh/Skordis–Złośnik.
- **NOT equations of this framework (proven dead this session):** $\alpha^{-1}=4Z^2+3$ and all
  constants (a random number reproduces them, `can_another_number_do_it.py`); $Z^2=\eta(T^3/Z_2)$
  (category error, `eta_local_bruning_seeley.py`); the 20.6 Gpc topology; the genetic code; the
  dipole $19/6$. These carry ~0 bits and must not be listed as results.

*Verify all: `python real_research/REAL_WEB.py` and the per-equation scripts above; full suite
80/80 pass.*

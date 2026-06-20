# Does the dS-Unruh THERMAL OCCUPATION of the ghost-condensate mode PIN I0 (Omega_dm)? — NO, FREE (head-on, 2026-06-19)

*topic: pin_I0_thermal. Both-ways, quarantine held. Scripts in `gc_consequences/`:
`pin_I0_thermal.py`, `pin_I0_thermal_ADVERSARIAL.py` (both exit 0). Primary literature pulled
verbatim this session: Arkani-Hamed–Creminelli–Mukohyama–Zaldarriaga, "Ghost Inflation",
hep-th/0312100 (JCAP 0404:001, 2004), Eqs 1.3–1.11 — the AUTHORS' OWN de Sitter fluctuation of
the ghost condensate. Plus ACLM 2004 (hep-th/0312099), Skordis–Zlosnik, Verwayen–Skordis–Zlosnik
2024 (the GC mapping).*

## HEADLINE (both ways)

**The thermal route is a NULL — done HEAD-ON this time, not by the banked crude estimate.** The
banked PIN_THE_AMOUNT condition (B) used a radiation-gas `rho~(kT_GH)^4` scaling (WRONG dispersion
for the GC) and a one-quantum-per-horizon guess. This session computed the GH thermal occupation of
the ghost-condensate mode with its OWN `omega^2 = alpha^2 k^4/M^2` dispersion, using the ACLM
authors' own de Sitter result (Ghost Inflation Eq 1.6): the frozen pi-fluctuation amplitude is
`delta_pi_H ~ (H_Lam M^3)^(1/4)` — this IS the fluctuation-dissipation / Gibbons-Hawking occupation
of the k^4 mode at horizon freezing. Mapping it to the induced cold dust gives
`rho_dust ~ H_Lam^(5/2) M^(3/2)` → **Omega_dust ~ 1e-74** at the framework's clustering scale
M~0.04–1 eV — ~74 orders BELOW Omega_dm=0.266. To land 0.26 the thermal route would need
M~3e47 eV (~1e40× the 10 MeV bound — excluded). No dS dimensionless combination (H/M, delta_pi/M,
T_GH/M, 1/Z, (3/8pi)^¼) equals Om_dm/Om_L=0.387 without tuning. **And the decisive structural
reason (new, sharper than the order-of-magnitude miss): the dark-matter amplitude is the MEAN of a
shift-symmetric flat direction (the conserved shift-charge I0); thermal/GH physics is a statement
about the VARIANCE of fluctuations AROUND that mean. No thermodynamic quantity pins the mean of a
flat direction.** The strong prior holds: I0 (Omega_dm) is a FREE integration constant. Quarantine
held; the null is now PROVEN with the correct dispersion, not assumed.

---

## (1) The head-on calculation — what the banked note skipped

The banked DARK_MATTER_ILLUSION / PIN_THE_AMOUNT condition (B) estimated the GH-thermal density two
crude ways — a **radiation gas** `rho ~ (pi^2/30)(kT_GH)^4/(hbar c)^3` and **one quantum per horizon
volume** — both giving `Omega ~ 1e-122` (the dark-ENERGY/CC scale). Correct conclusion (negligible),
but the WRONG physics: a ghost condensate is NOT a relativistic radiation gas; its mode has
`omega^2 = alpha^2 k^4/M^2` (Ghost Inflation Eq 1.4), so its de Sitter fluctuation spectrum and
energy density are completely different from `(kT)^4`. The task demanded the head-on FDT/GH-occupation
of the GC mode. Done here.

**The ACLM authors computed exactly this** (Ghost Inflation hep-th/0312100, the de-Sitter fluctuation
of the very same condensate). Pulled verbatim:
- Lagrangian (Eq 1.3): `S = ∫d^4x [ (1/2) pidot^2 − (alpha^2/2M^2)(∇^2 pi)^2 − (beta/2M^2) pidot(∇pi)^2 + … ]`
- dispersion (Eq 1.4): `omega^2 = alpha^2 k^4/M^2`
- **scaling dimension of pi = 1/4** (Eq 1.5), so the fluctuation at energy E is `delta_pi_E ~ (E M^3)^(1/4)`
- **the frozen (horizon-crossing) fluctuation (Eq 1.6): `delta_pi_H ~ (H M^3)^(1/4)`** — the de Sitter /
  Bunch-Davies (= GH-thermal) amplitude; "much larger than H" but `<< M` (EFT validity `H << M`)
- freezing happens at `k_freeze ~ sqrt(H M/alpha)` (NOT k~H), Eq just below 1.6
- curvature perturbation (Eq 1.8): `delta_rho/rho ~ (H/M)^(5/4)`

`delta_pi_H ~ (H M^3)^(1/4)` IS the Gibbons-Hawking thermal occupation of the GC mode: in de Sitter
the Bunch-Davies vacuum is GH-thermal at `T_GH = H/2pi`, and the mode freezes when Hubble friction
balances the dispersion — the fluctuation-dissipation balance the task asks about. This is the
authors' own, not a relabel.

## (2) The numbers (pin_I0_thermal.py, exit 0)

Framework footing: `H_Lam = 1.81e-18 s^-1`, `hbar H_Lam = 1.19e-33 eV`, `kB T_GH = 1.89e-34 eV`,
M~0.04–1 eV (banked clustering window). Then (Eq 1.6):

| M (eV) | delta_pi_H=(H M^3)^¼ (eV) | delta_pi/M | rho_dust~H^{5/2}M^{3/2} → Omega_dust |
|---|---|---|---|
| 0.04 | 5.3e-10 | 1.3e-8 | **4.0e-74** |
| 0.15 | 1.4e-9 | 9.4e-9 | **7.7e-74** |
| 1.00 | 5.9e-9 | 5.9e-9 | **6.6e-72** |

The induced cold-dust density (velocity-displacement kinetic energy `~(1/2)(H delta_pi)^2`, equiv.
the ACLM `delta_rho/rho~(H/M)^{5/4}` core, equiv. the FDT mode-integral `k_freeze^3 · hbar H`) is
**Omega ~ 1e-74–1e-72 — ~74 orders below Omega_dm=0.266.** Three independent mappings (kinetic
`(H δπ)²`, the curvature `(H/M)^{5/4}`, and the FDT bath `k_fr^3·hbar H`) ALL give `rho~H^{5/2}M^{3/2}`
and the same Omega — they agree. The GH-thermal occupation of the GC mode is a CC-scale ripple, not
the 26% dust.

**Inversion:** to make `Omega_dust=0.266` the thermal route needs `M = (rho_dm/H_Lam^{5/2})^{2/3}
~ 3.4e47 eV` — ~2e48× the clustering scale and ~3e40× the 10 MeV twinkling bound (excluded). The
framework's actual M is ~50 orders too small for the thermal energy to matter.

## (3) No dS dimensionless number hits 0.387 (pin_I0_thermal.py part d)

`Om_dm/Om_L = 0.3879`. Scanned: `H/M ~ 8e-33`, `(H/M)^¼ ~ 9e-9`, `delta_pi/M ~ 9e-9`,
`T_GH/M ~ 1e-33`, `1/Z = 0.173`, `1/Z^2 = 0.030`, `(3/8pi)^¼ = 0.588`, `Om_L = 0.685`. None within
5% of 0.387. The thermal/dispersion ratios are ~1e-9 to 1e-33 (nowhere near); the O(1) geometric
candidates (1/Z, (3/8pi)^¼, Om_L) are the SAME ones the banked PIN_THE_AMOUNT already showed miss.
No zero-tuning combination lands.

## (4) Adversarial both-ways — four pro-PIN moves, all fail (pin_I0_thermal_ADVERSARIAL.py, exit 0)

The "it's a null" verdict tested as hard as a "pins" claim. Four strongest pro-pin moves:

- **ADV-1 (THE strong one): freeze at large EARLY H, redshift the dust a^-3 to today.** Fails three
  ways: (i) EFT validity requires `H_fr << M`, capping `H_fr` at the eV scale; (ii) `a^-3` redshift
  SHRINKS the surviving density, not grows it; (iii) **structural — thermal physics sets the VARIANCE
  `<delta_pi^2>` (a zero-mean Gaussian); redshifting a zero-mean fluctuation stays zero-mean. The
  dark-matter amplitude is the homogeneous MEAN `<Q>-Q0 = I0`, not the variance.** Even maximally
  generous (freeze at H~M~eV), `Omega_dust,0 ~ 1e-72`. Miss by ~70+ orders.
- **ADV-2 (maximal LINEAR energy `rho~M^2·delta(phidot)`, ACLM Eq 1.9):** bigger than quadratic but
  the `H_Lam~1e-33 eV` factor still gives `Omega ~ 1e-31–1e-35`. No landing.
- **ADV-3 (ghost-inflation amplitude `(H/M)^{5/4}`):** at the framework's late H=H_Lam this is
  `~1e-41` — negligible. That mechanism is an EARLY-universe (H~keV) story; the framework's dark
  MATTER is not ghost inflation.
- **ADV-4 (FDT fixed point for the zero mode):** the shift symmetry forbids a potential `V(Q)`, so the
  flat direction has NO stationary mean (random walk, not Ornstein-Uhlenbeck-to-a-fixed-point). The
  EOM is a conservation law `a^3 K'(Q)=I0`; the constant I0 is set by initial data. FDT fixes the
  variance about whatever I0 is; it never pins the flat-direction mean.

**The decisive structural fact (new this session, sharper than the banked order-of-magnitude miss):
I0 is the MEAN of a shift-symmetric flat direction; GH/thermal/FDT physics is a statement about the
VARIANCE of fluctuations around that mean. No thermodynamic quantity pins the mean of a flat
direction.** This is WHY the thermal route can never pin I0 — independent of the (also fatal) ~74-order
magnitude gap.

## (5) sympy confirmation of the orthogonality (pin_I0_thermal.py part f)

`K(Q) = K2(Q−Q0)^2 − 2Lambda` → `K'(Q)=2K2(Q−Q0)` → first integral `a^3 K'(Q)=I0` →
`Q(a)=Q0+I0/(2K2 a^3)` → `rho_dust = Q0 I0/a^3`. sympy: `d rho_dust/dLambda = 0` and
`d rho_dust/d mu = 0` (the additive −2Lambda dark energy and the μ/K2 mass both cancel out of the
dust amplitude). The thermal `delta_pi` rides the fluctuation spectrum about Q0; the conserved I0 is
orthogonal to every bulk dS constant — the field-theory restatement of the banked `drho_dust/dLambda=0`.

## VERDICT (both ways, quarantine held)

**The dS-Unruh thermal occupation of the ghost-condensate mode does NOT pin I0 / Omega_dm.** Computed
head-on with the correct `k^4/M^2` dispersion and the ACLM authors' own de Sitter fluctuation
(`delta_pi_H~(H M^3)^{1/4}`, Ghost Inflation Eq 1.6): the GH-thermal energy density of the GC mode at
the framework's M~0.04–1 eV is `rho~H^{5/2}M^{3/2}` → **Omega ~ 1e-74**, ~74 orders below 0.266; it
reproduces a CC-scale ripple, not the dark-matter amount. Three independent mappings agree; four
adversarial pro-pin moves (early freeze, linear energy, ghost-inflation amplitude, FDT fixed point)
all fail. No dS dimensionless number hits 0.387 without tuning.

**This is the sharpest form of the free-amount result to date.** The banked crude `(kT)^4` estimate
reached the right conclusion by luck (wrong dispersion); this session confirms it rigorously with the
right physics, AND adds the decisive structural reason: **I0 is the mean of a shift-symmetric flat
direction, and no thermal/GH/FDT quantity pins the mean of a flat direction — only initial data
does.** Identical landing to the banked SQRT_LAMBDA_PINS_KQ=NO / PIN_THE_AMOUNT / DSUNRUH_DRIVES_VEV
nulls, now closed in its strongest tested form.

Both-ways: had the thermal occupation landed Omega_dm at a defensible scale it would have been the
zero-parameter dark sector (huge) — it was tested at full rigor and does not. The free-amount concession
is made at full weight, with the correct dispersion and a structural proof, not a reflexive dismissal.
Quarantine held throughout: a0, Z, kappa, I0 never asserted derived.

**Files (absolute):**
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/pin_I0_thermal.py
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/pin_I0_thermal_ADVERSARIAL.py
- /Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/gc_consequences/PIN_I0_THERMAL_VERDICT_2026-06-19.md

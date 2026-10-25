# X47_vacuum_tethered_core_floor: a vacuum-set acceleration floor for cold dark energy cores

Criteria: `FROZEN_CRITERIA.md` (bafcb4754e, committed alone before any script or number). Lane id X47; X46 belongs to a peer.

Standing caveats:
- κ = ½ is FITTED. The two footings (canonical a₀ 9.3603e-11, alt 1.1312e-10 m s⁻²) are never pooled.
- Route E: Newtonian gravity on baryons plus cold dark energy, with the law emergent.
- Cold dark energy is a gravitating w ≈ 0 field component paired with dark energy. It is not matter and not a particle.
- This is not "theory closed". Nothing here says the data favour the framework.

**The owner's question.** "Figure out the tethering of the cold dark energy": what sets where it settles?

**Hypothesis VT.** Cold dark energy stays bound only where its own pull exceeds g_T = ζ c²√Λ. Below that it stays tethered to
the smooth dark-energy background.
- ζ is fixed, not fitted: g_T is the peak self-pull of an a₀/(2πG) Burkert core.
- That peak is **0.254484 a₀**, at x = 0.9634 r₀. At r₀ itself the pull is B(1)/2 = 0.254323 a₀, which is 6.3e-4 lower.
- So g_T = 2.382e-11 m s⁻² (canonical) and 2.879e-11 (alt).
- On the canonical footing a₀ = c²√(Λ/32π), which gives ζ = 0.025381. On the alt footing a₀ is set by ρ_total, so there
  g_T is 0.254484 a₀,alt.

Two readings are graded separately:
- **VT-L (local, primary):** the hypothesis as written. The medium binds at a point iff |∇Φ_c| > g_T there.
- **VT-O (object, reported):** the key is a bound object's peak self-pull, so it never reads the linear field. This reading
  is nonlocal.

## Verdict

- **VT-L: VT FAILS AT growth / data**, on both footings.
- **VT-O: VT-O CONSISTENT (NONLOCAL, mechanism open)**, on both footings.
- **No action is written down**, so neither reading reaches "WITH AN ACTION".

**Step 0 passes.**
- This lane's own Burkert code reproduces X38's four SPARC rows (2 footings × 2 backgrounds) with |Δrms| = 0 and the same
  median Υ.
- B(1)/2 = 0.254323 matches X40b's 0.50865/2.
- The Burkert closed form matches quadrature to 0.

## 2a. The floor is constant Σ, by dimensional analysis

For any profile of fixed shape, g_pk = C · Gρ₀r_s. So "peak self-pull = g_T" is the same statement as "Σ = constant". For
Burkert it reproduces X38's ρ₀r₀ = a₀/(2πG) exactly, by construction. **This is a restatement of X38, not a result.** The
content lies in the choice of ζ, which carries X38's 1/(2π) and κ = ½ (FITTED).

The table below comes from sympy. dM/dx = 4πx²ρ is exact for all five profiles. Σ is in units of Σ_a₀ (106.9 / 129.2 M☉ pc⁻²).

| profile | x_pk | C | ρ₀ r_{1/4} (ρ = ρ₀/4) | Σ_proj(0) | M(<r_pk)/(π r_pk²) |
|---|---|---|---|---|---|
| Burkert | 0.963 | 1.599 | **1.000** | 1.571 | 0.509 |
| pseudo-isothermal | 1.515 | 2.889 | 0.959 | 1.739 | 0.509 |
| Einasto n = 2 | 6.08 | 3.245 | 0.947 | 1.971 | 0.509 |
| Einasto n = 3 | 41.9 | 8.165 | 0.522 | 2.350 | 0.509 |
| Einasto n = 4 | 402 | 28.69 | 0.206 | 2.675 | 0.509 |

- **The mean enclosed density is profile-blind.** M(<r_pk)/(πr_pk²) = g_T/(πG) for every shape; this is an identity.
- **Genuinely cored shapes agree closely.** For Burkert, pseudo-isothermal and Einasto n = 2, the "Donato-convention"
  ρ₀r_{1/4} is 0.95–1.00 Σ_a₀ (0.02 dex). Their central projected Σ is 1.57–1.97 Σ_a₀ (0.10 dex).
- **The steeper Einasto shapes do not.** Einasto n = 3 and 4 peak far out, at x = 42 and 402. Their ρ₀r_{1/4} drops to
  0.52 and 0.21. The floor's Σ is therefore shape-dependent by up to 0.69 dex, and well defined only for genuinely cored halos.

## 2b. SPARC: per-galaxy g(r₀) against g_T

X38 fixes Σ for every galaxy, so its g(r₀) equals B(1)/2 · a₀ in every galaxy by construction. That is not a test.

**The test.** Fit Σ freely per galaxy on the raw rotation curves:
- grid log(Σ/Σ_a₀) from −1.5 to +1.5 in steps of 0.02;
- M200 from EM1's relation (background A, borrowed and not refit);
- X38's saturation rule.

For a Burkert core g(r₀)/g_T = Σ/Σ_a₀.

| footing, Υ | constrained | median log(g(r₀)/g_T) | 16–84 % | half-width | below −0.3 dex | above +0.3 dex |
|---|---|---|---|---|---|---|
| canonical, Υ free | 168/175 | **+0.070** | −0.19, +0.46 | 0.32 | 0.101 | 0.304 |
| canonical, Υ = 0.50 | 172/175 | +0.180 | −0.16, +0.52 | 0.34 | 0.099 | 0.349 |
| alt, Υ free | 168/175 | **−0.020** | −0.27, +0.38 | 0.32 | 0.131 | 0.232 |
| alt, Υ = 0.50 | 172/175 | +0.100 | −0.24, +0.44 | 0.34 | 0.116 | 0.285 |

- **D1, "no core below the floor": PASS on both footings.** Only 10–13 % of galaxies sit more than 0.3 dex below, against
  the frozen limit of 1/3.
- **Centred, but not narrow.** The median sits within 0.07 dex of g_T (Υ free). The spread is ±0.32 dex, not a sharp
  pile-up, and 23–30 % of galaxies sit more than 0.3 dex above the floor. X41's collapse ρr in galaxies is far below the
  floor, so VT expects galaxies to sit at the floor. The spread is therefore either Υ–Σ degeneracy and noise, or real scatter
  that VT does not explain. This lane cannot tell which.
- **D3 (VT-L self-consistency): FAIL.** In every SPARC galaxy, 100 % of X38's halo mass inside R_last has g_h < g_T
  (median 1.0000, min 1.0000). This is analytic: g_T is the halo's own peak pull, so an at-floor core is below threshold at
  every radius but one. Any cored profile also has g → 0 at its centre. **A local threshold therefore tethers both the core's
  centre and its envelope:** VT-L cannot hold a cored halo at all.
- **Context only.**
  - Gentile+2009, as transcribed in `campaign_fresh_gravity/CFG4_galaxy_law.py` (PROVISIONAL): ⟨Σ⟩(<r₀) = 72 (+42/−27)
    M☉ pc⁻², i.e. g(r₀) = 3.15e-11 [1.97e-11, 4.99e-11] m s⁻². That is 1.32 g_T (canonical) and 1.10 g_T (alt), inside
    its range on both footings.
  - Li+2020 Burkert fits, as in the record (`hunt_2026/h5_h95_h58.out`, F25; EXTERNAL fits): median 176.8 M☉ pc⁻²,
    scatter 0.45 dex, i.e. 1.65 / 1.37 g_T.

## 3. Theorem D-T: it does not apply to the bound cores; it returns wherever the tether is on

D-T (CFG941 DERIVATION §1.3) rests on three premises:
1. **(P1)** a cold, static medium held by an always-on tether force F(u);
2. **(P2)** its phantom is its own mass, g = g_N + u;
3. **(P3)** the law (any deep limit g_N → g²/a₀) is imposed as that medium's equilibrium, F(u) = g.

From these, F = D_full and c₂ = 1, and the linear self-gravity coefficient (1 − c₂)Kρ_c vanishes. sympy reproduces DT1:
F = a₀u/(a₀ − u).

**In VT's bound cores, P1 and P3 fail.**
- **P1 fails.** The bound medium is dust held up by its velocity dispersion, ∇(ρσ²) = −ρ∇Φ. No tether force acts on it, so
  c₂ = 0 and its self-gravity is full, Kρ_c.
- **P3 fails.** In route E the law is not imposed galaxy by galaxy; it emerges approximately. X38 reaches rms 0.073–0.080
  against the law's 0.054.
- **This is CFG941's own open item 2:** a settled medium "held up by dispersion" and gravitating universally. Because bound
  medium falls universally, the hover lemma (F2) does not arise.
- **T1: PASS.**

**But in VT's tethered region, D-T's conclusion comes back by definition.** "Tethered to the smooth background" means held at
δ_c ≈ 0 against its own gravity, so the effective linear self-gravity is zero. That is the c₂ = 1 outcome, now imposed by
hand rather than forced by the law. Where the tether switches on therefore decides everything, which is task 4.

## 4. Growth: a local key switches the tether on in the linear field

Method:
- the record's CLASS backgrounds A and B, through EM1's committed block; σ₈ 0.82742 / 0.81715 equals F3 exactly;
- the cold sector's linear rms self-pull per ln k, g_k = 4πGρ̄_c(z) a √Δ²(k, z)/k.

Linear g_k in m s⁻², background A (B agrees to within 7 %):

| z | k 0.01 | 0.03 | 0.1 | 0.3 | 1 | 3 | 10 h/Mpc | cumulative k ≥ 0.01 | max/g_T (canonical) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2.9e-13 | 4.8e-13 | 4.7e-13 | 3.2e-13 | 1.6e-13 | 7.6e-14 | 3.0e-14 | 8.6e-13 | 0.020 |
| 1 | 7.1e-13 | 1.2e-12 | 1.1e-12 | 7.9e-13 | 4.0e-13 | 1.8e-13 | 7.2e-14 | 2.1e-12 | 0.049 |
| 3 | 1.5e-12 | 2.4e-12 | 2.4e-12 | 1.6e-12 | 8.3e-13 | 3.8e-13 | 1.5e-13 | 4.4e-12 | 0.102 |
| 10 | 4.1e-12 | 6.7e-12 | 6.5e-12 | 4.5e-12 | 2.3e-12 | 1.1e-12 | 4.1e-13 | 1.2e-11 | 0.283 |
| 30 | 1.2e-11 | 1.9e-11 | 1.8e-11 | 1.3e-11 | 6.5e-12 | 3.0e-12 | 1.2e-12 | 3.4e-11 | 0.801 |

**G1 (VT-L): FAIL on both footings and both backgrounds.**
- Even ν = 3 peaks reach at most 0.25–0.31 g_T anywhere in k 0.01–10 h/Mpc at z ≤ 3.
- Tracking g_T with a₀(z) on M-DEC raises that only to 0.32–0.40.
- **When the tether switches on in the linear field** (ν = 1, g_k = g_T):
  - canonical: z ≈ 38–63 for k 0.01–0.3 h/Mpc, rising to 112–602 at k 1–10;
  - alt: z ≈ 46–75, and 135–713.
  - For ν = 3 peaks the switch-on is at z ≈ 12–25 (k ≤ 0.3) and 37–260 (k 1–10).
- Below those redshifts a local key holds the cold sector smooth. That loses all of its late linear growth, which σ₈, KiDS
  and the forest need.
- **This is the μ-pincer in acceleration form.** An at-floor galaxy core today has g ≈ g_T, while the linear field at the
  same epoch has g ≈ 0.02 g_T. No local threshold separates "bind in cores" from "grow in the linear field" without first
  tethering the linear field.

**G2 (VT-O): PASS by construction.** The object key never reads the linear field. But collapse itself is sub-threshold.
The cold self-pull at turnaround is only 0.001–0.010 g_T at z = 0 (10¹⁰–10¹³ M☉), and 0.036–0.36 at z = 5. So VT-O must
switch on only after virialisation. That makes it both nonlocal and time-ordered.

## 5. Σ_floor(z), a reported prediction

If a₀ tracks ρ_DE (M-DEC curve, CFG223), the floor scales with it: Σ_floor(z) = Σ_a₀ · a₀(z)/a₀(0), with Burkert ρ₀r₀ in M☉ pc⁻².

| z | a₀(z)/a₀(0) | canonical ρ₀r₀ | canonical g_T (m s⁻²) | alt ρ₀r₀ | alt g_T |
|---|---|---|---|---|---|
| 0 | 1.000 | 106.9 | 2.382e-11 | 129.2 | 2.879e-11 |
| 0.5 | 1.032 | 110.3 | 2.458e-11 | 133.3 | 2.971e-11 |
| 1 | 0.989 | 105.7 | 2.356e-11 | 127.7 | 2.847e-11 |
| 2 | 0.874 | 93.4 | 2.082e-11 | 112.9 | 2.516e-11 |

**Data in the record that could test it:**
- KURVS z ≈ 1.5 discs (CFG140/141; NON-DIAGNOSTIC so far, because the gas is unmeasured);
- the ALMA z 1.2–2 window (CFG570/571; governing plans CFG806/809).

The predicted shift is −0.06 dex at z = 2, and +0.01 dex at z = 0.5. Against SPARC's per-galaxy spread of 0.32 dex, seeing it at 2σ
would take about (2 × 0.32/0.06)² ≈ 110 galaxies at z ≈ 2 (arithmetic on this lane's numbers). The record's high-z samples hold tens, so they **cannot test it as
they stand**. X35's caveat applies: with early dark energy the a₀(z) band differs.

## 6. Mechanism menu (reported only; no action claimed)

| candidate | static limit gives the floor? | linear field (G1 numbers) | Theorem G (CFG944) |
|---|---|---|---|
| **K(Q) threshold in the cold sector's own potential**, ∇·[μ_T(\|∇Φ_c\|/g_T)∇Φ_c] = 4πGρ_c with self-gravity off below g_T | **No.** A cored profile has g → 0 at its centre and g ≤ g_T everywhere at the floor (D3 = 1.000), so the static solution is no core, not a floored core | **Fails:** the linear self-pull is 0.02–0.31 g_T at z ≤ 3, so self-gravity is off and there is no growth | Not needed: G's (c-amp) growth leg fails directly. G's static-law premise does not apply in route E |
| **Phase transition keyed to \|∇Φ_self\|/(c²√Λ), non-latching** | as above | fails as above | as above |
| **Same transition, latching** (once bound, stays bound) | **No floor forms.** The linear field exceeds g_T at z > 38–713 (ν = 1), so the whole cold sector latches into dust early and never re-tethers | passes, because it is plain dust | — |
| **Object-keyed (VT-O):** a bound, virialised object's peak self-pull | yes, by construction | passes, by construction | outside G (nonlocal). It needs bound-object or catchment identification, as in CFG941 (g) and CFG947. No action exists in the record |
| **The law's phantom bound** Σ_ph ≤ a₀/(2πG) (CFG4: exact for P2) | yes, but only if the law is fundamental | — | — |

The last row is the record's known coincidence: in the law-fundamental reading, the floor is a property of the phantom, not of
cold dark energy.

**The local pincer, stated K-independently.**
- A non-latching local threshold tethers the linear field. It also tethers the cores' own centres and envelopes.
- A latching threshold never forms a floor.

**Only an object-level (nonlocal) key survives,** and no action for one is written here.

## Reading

**What VT does.** It is a consistent way to state X38's galaxy floor, and through X43's max() a natural reading of the
floor branch:
- SPARC's free per-galaxy cores centre on g_T to within 0.07 dex, and few sit below it;
- Gentile's PROVISIONAL g(r₀) lies within its own range of g_T;
- D-T does not bind dispersion-supported cores.

**What VT does not do.** It does not answer the owner's question with a local mechanism. Taken literally (VT-L), it fails:
- **growth:** the tether switches on in the linear field at z ≈ 12–700;
- **self-consistency:** an at-floor core is sub-threshold everywhere.

The answer this lane can give: **wherever the tethering lives, it must key on bound objects, not on any local acceleration, density
or expansion invariant.** That puts it in the same class as the record's nonlocal catchment switch. The mechanism is open.

## Checks and MUTATE

- **Checks 5/5:**
  - K0: S0a, X38 SPARC reproduced, |Δ| = 0;
  - K1: S0b, B(1)/2 and Burkert quadrature;
  - K2: sympy dM/dx for 5 profiles;
  - K3: CLASS σ₈ equals F3;
  - K4: peak RSS 0.56 GB.
- **MUTATE** (`X47_MUTATE=1`, arctan sign flipped in B):
  - K0 fails (|Δrms| up to 0.25), K1 fails, and K2 fails;
  - verdict UNDECIDED (step 0), exit 1, as frozen.
- **Disclosed implementation fix:** before the committed MUTATE run, the profile-peak root finder was given a fallback for
  the mutated Burkert, which has no interior peak and first crashed. The main run is unaffected; that branch is unreachable
  there.

## Files and commands

`FROZEN_CRITERIA.md`, `x47_vt_floor.py`, `x47_vt_floor.out` / `_results.json`, `x47_vt_floor_MUTATE.out` / `_results_MUTATE.json`.

    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x47_vt_floor.py                 # exit 0, 5/5, ~11 s, 0.56 GB
    X47_MUTATE=1 PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 x47_vt_floor.py    # exit 1, K0/K1/K2 fail

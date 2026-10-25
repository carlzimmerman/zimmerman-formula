# X47_vacuum_tethered_core_floor: FROZEN CRITERIA (committed alone, before any script or number)

The owner's question: "Figure out the tethering of the cold dark energy." What sets where cold dark energy settles?

Standing: κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m s⁻², never pooled. Cold dark energy is a
gravitating w ≈ 0 clumping field component paired with dark energy; not matter, not a particle. Route E (Newtonian gravity
on baryons + cold dark energy, law emergent) as in EM1 / X38. Framework-native: raw SPARC rotation curves, the record's
own CLASS backgrounds (F3 / EM1), the record's DESI M-DEC a₀(z) curve (CFG223). Literature numbers (Donato+2009,
Gentile+2009, Li+2020 fits) are context only, labelled PROVISIONAL or EXTERNAL, never in a verdict. Not "theory closed".
Nothing here says the data favour the framework. Lane id X47 (X46 is a peer's).

## Hypothesis VT (vacuum-tethered core floor)

Cold dark energy stays bound only where its own pull exceeds g_T = ζ c²√Λ; below it the medium stays tethered to the smooth
dark-energy background. ζ is fixed (not fitted) by g_T = peak self-pull of an a₀/(2πG) Burkert core = (B(1)/2) a₀ at r₀
(peak value used as computed). Two readings are graded separately and never merged:

- **VT-L (local, the hypothesis as literally stated):** at each point the medium is bound/clumping iff |∇Φ_c| > g_T, where
  Φ_c is the cold sector's own potential. This is the PRIMARY reading.
- **VT-O (object):** a bound object's core cannot settle with peak self-pull below g_T; the key is a property of a
  bound object, so it never acts on the linear field. Reported as the fallback reading, flagged NONLOCAL.

## Step 0 (stop rule)

- S0a: re-evaluate X38's SPARC rows (EM1 relation, background A and B, both footings) with this lane's own Burkert code;
  rms must match `x38_sd_halos_results.json` to |Δ| ≤ 1e-6 and median Υ exactly. Fail ⇒ STOP, verdict UNDECIDED.
- S0b: B(1)/2 from the closed form must equal X40b's B(1) = 0.50865 / 2 to 1e-5. Fail ⇒ STOP.

## Task 2a: floor ⇔ Σ (sympy, PYTHONHASHSEED=0)

For Burkert, pseudo-isothermal and Einasto n = 2, 3, 4: closed-form M(x), dM/dx = 4πx²ρ verified symbolically, g(x) =
GM/r², x_pk and g_pk = C_prof · G ρ₀ r_s. Report the Σ implied by g_pk = g_T in three conventions: ρ₀ r_{1/4}
(radius where ρ = ρ₀/4; Burkert's r₀), central projected Σ_proj(0), and mean enclosed M(<r_pk)/(π r_pk²) (= g_T/(πG) for
every profile by identity). Flag in the README that for any fixed-shape family "peak g = g_T" ⇔ "Σ = const" by dimensional
analysis, so the Burkert equivalence is a restatement of X38, not a result.

## Task 2b: SPARC data test (framework-native, non-tautological)

X38 fixes Σ for every galaxy, so its g(r₀) is identical by construction; that distribution is NOT a test and is reported as such.
The test: per-galaxy free Σ (grid log₁₀(Σ/Σ_a₀) ∈ [−1.5, +1.5], step 0.02), EM1 relation (bg A) for M200, X38's saturation
rule, Υ free per galaxy (primary) and Υ = 0.50 pinned (secondary). For a Burkert core g(r₀)/g_T = Σ/Σ_a₀ exactly.
"Constrained" galaxies: best grid value not within 0.1 dex of an edge.

- **D1 (floor):** VT says no core sits below the floor. FAIL on a footing if more than 1/3 of constrained galaxies have
  log₁₀(g(r₀)/g_T) < −0.30 (primary Υ-free variant).
- **D2 (pile-up, reported):** median and 16–84 % of log₁₀(g(r₀)/g_T); "centred" if |median| ≤ 0.15 dex, "narrow" if the
  16–84 half-width ≤ 0.25 dex.
- **D3 (VT-L self-consistency):** fraction of X38's halo mass inside each galaxy's last measured radius that has g_h < g_T
  (the medium VT-L would tether). Reported; VT-L also FAILS data if the median galaxy has > 50 % of that mass below g_T.
- Context only: Gentile+2009 ⟨Σ⟩(<r₀) = 72 (+42/−27) M☉ pc⁻² as transcribed in `CFG4_galaxy_law.py` (PROVISIONAL), and the
  record's Li+2020 Burkert median 176.8 M☉ pc⁻² (`hunt_2026/h5_h95_h58.out`, F25; EXTERNAL fits).

## Task 3: D-T

Read CFG941 DERIVATION §1.3. Name each premise (always-on tether F(u) holding a cold STATIC medium; its phantom is its own
mass with the law imposed as its equilibrium; deep limit). Decide which premise fails in VT's bound cores and in VT's tethered
region. A sympy check reproduces DT1 (F = a₀u/(a₀ − u)) and the self-gravity coefficient (1 − c₂). **T1 PASS** if a premise
provably fails for the bound cores; FAIL if D-T applies to them.

## Task 4: growth (the μ-pincer location)

Record CLASS backgrounds A and B via EM1's committed block (σ₈ check vs F3). Linear rms self-acceleration per ln k of the cold
sector: g_k(z) = 4πG ρ̄_c(z) a(z) √Δ²(k, z) / k (comoving k), with Δ² ∝ D(z)², at k = 0.01, 0.03, 0.1, 0.3, 1, 3, 10 h/Mpc
and z = 0, 0.5, 1, 2, 3, 5, 10, 30; also ν = 3 peaks; also the cumulative rms over k ≥ 0.01 h/Mpc. g_T constant (Λ) and,
reported, g_T(z) ∝ M-DEC to z = 3.

- **G1 (VT-L):** FAIL if the ν = 3 g_k < g_T at any grid k for any z ≤ 3 (the tether would switch on in the linear field
  where σ₈, KiDS and the forest need dust growth). Report z_cross(k) where ν = 1 and ν = 3 g_k = g_T.
- **G2 (VT-O):** PASS by construction (the key never reads the linear field); reported with the label NONLOCAL.
- Reported: self-pull at turnaround (δ = 5.55 × mean) of 10¹⁰–10¹³ M☉ objects at z = 0–5, against g_T.

## Task 5: Σ_floor(z) (reported prediction)

Σ_floor(z) = Σ_a₀ · a₀(z)/a₀(0), M-DEC curve (CFG223), at z = 0.5, 1, 2, both footings, never pooled; also g_T(z). Name the
record's data that could test it. No verdict.

## Task 6: mechanism menu (reported only)

Candidates checked against Theorem G (CFG944) and against this lane's G1 numbers (the μ-pincer analogue). No action is
claimed unless written down with its static limit shown to give the floor.

## Verdict classes (primary = VT-L)

- **VT FAILS AT growth** if G1 fails (primary reading); FAILS AT data if D1 fails, or (VT-L) D3 fails; FAILS AT D-T if T1 fails.
  Several may be listed.
- **VT CONSISTENT** if S0, D1, T1 pass and G1 passes for VT-L.
- **VT CONSISTENT WITH AN ACTION** only if task 6 writes down an action whose static limit gives the floor and passes G1.
- **UNDECIDED** if step 0 fails or footings disagree.
- The VT-O reading gets its own reported class: "VT-O CONSISTENT (NONLOCAL, mechanism open)" if S0, D1, T1 pass, else
  "VT-O FAILS AT …".

## Checks and MUTATE

K0 = S0a; K1 = S0b plus Burkert closed form vs quadrature (1e-6); K2 = sympy dM/dx = 4πx²ρ for all five profiles; K3 = CLASS σ₈
vs F3 (1e-3); K4 = peak RSS < 1 GB. MUTATE (`X47_MUTATE=1`): the arctan sign in B(x) is flipped (as X38's mutate); K0 and K1
must FAIL, exit 1, outputs written with a `_MUTATE` tag. One thread, nice 15, no downloads, nothing outside this folder.

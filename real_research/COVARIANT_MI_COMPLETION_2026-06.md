# The covariant modified-inertia completion — SKEPTIC pass: both candidates HIT-THE-NO-GO at a precise, named obstruction (2026-06-26)

*Independent re-adjudication of the two banked candidate completions (Candidate A = aether/SME modified-inertia action;
Candidate B = dS-Unruh nonlocal modified-inertia action) against the Milgrom-1994 MI no-go + Ostrogradsky + covariance +
the slip⇔Φ lensing no-go. Seven load-bearing checks re-run independently in sympy/mpmath (`/tmp/mi_*.py`). Both ways:
genuine partial structure credited at full weight, the obstruction conceded at full weight, no manufactured action, no
high-priesting. Primaries fetched: Milgrom 2503.07106 (abstract verbatim), AeST 2007.00082, Luo 2026 2602.14515.*

---

## VERDICT: (C) HITS-THE-NO-GO — neither candidate is a surviving covariant, stable, a0-hosting MI completion. The obstruction is now MAPPED EXACTLY (a sharpened trichotomy), which is genuine progress.

This is **not** a defeat dressed up — it is the precise statement of what a completion must evade, and it *tightens* the
banked standing rather than overturning it. The framework's modified-INERTIA matter sector that genuinely survives
(Route E, banked) is NOT either candidate as proposed: Candidate A fails on **stability** (Ostrogradsky), Candidate B
fails on **the source of its kernel** (passivity → anti-MOND) plus the framework's **specific coefficient**. Both
inherit a0's VALUE rather than deriving it (only the √Λ SCALE is forced).

---

## What I verified INDEPENDENTLY (seven sympy/mpmath checks, all reproduce the bank)

| # | Check | Result | Criterion |
|---|---|---|---|
| 1 | Framework gate `mu_fw(x)=(√(1+4x²)−1)/(2x)`: `mu→1` (x→∞), `mu→x` (x→0); `mu(a/a0)·a=g_N` ⇒ `a=√(a0 g_N)`; circular `v⁴=GM a0` | **PASS, sympy-exact** | (b) deep-MOND |
| 2 | `Z=a_dS/a0=√(32π/3)=5.7888=4√(6π)/3`; kinematic dS-Unruh kernels deliver `√(1/3)` (Milgrom-1999 5D) or `2√(1/48)=√(1/12)` (Luo 2026) → ratio `√(8π/3)=2.894`; the `32π=8π·4` gravitational normalization is NEVER seen by a kinematic kernel | **SCALE forced, VALUE not** | (a) a0 from dS |
| 3 | Local gate `−mc²F(\|a\|/a0)`: `d²L/d(ẍ)²=−mc²F''/a0²≠0` for any `F''≠0` ⇒ non-degenerate ⇒ Ostrogradsky; finite truncation `1/(s+s²/M²)` has poles {0,−M²} with residues {**+1, −1**} (the −1 = the ghost) | **FAILS (ghost)** | (c) stability |
| 4 | Entire/branch-cut form factor `exp(p²/M²)/p²`: single pole at `p²=0`, residue **+1**, NO extra poles (exp is entire) | **PASS, but only nonlocal** | (c) stability |
| 5 | Einstein-aether mode speeds in the `c13=0` (c_T=c) corner, witness {c1,c2,c3,c4}={1,1,−1,0}×10⁻³: spin-2/1/0 speeds² = {1, 1, 0.998} > 0 | **Aether KINETIC sector HEALTHY** | (d) GR/SME |
| 6 | Pure-slip traceless shear `T_ij=∂_i∂_j f−⅓δ_ij∇²f`: trace=0 but `div_i T_ij=(2/3)∂_j(∇²f)≠0` ⇒ conservation forces `3δp=−2∇²f≠0` ⇒ sources δΦ | **δΦ=0 forbidden (4-diff)** | (d) lensing |
| 7 | Passive (Ohmic) bath adiabatic inertia shift `δm=(2/π)∫J/ω² dω` is POSITIVE (mass increases) ⇒ wrong sign ⇒ **anti-MOND**; MOND needs an active sign-flipping kernel the cosmos does not supply | **Kernel un-sourceable** | (c)/(a) |

The bank's claims survive hostile re-computation. Nothing flips.

---

## CANDIDATE A (aether/SME modified-inertia action) — FAILS on stability (c). Precise obstruction: Ostrogradsky.

**Form:** `S = S_grav[g] + S_aether[g,u] + S_matter`, with `S_matter = −mc²∫dτ F(|a|/a0)`, `|a|=√(a^μ a_μ)` the
covariant 4-acceleration magnitude, `u^μ` the unit-timelike aether locked to the dS rest frame, and the gate from the
Deser-Levin dS-Unruh temperature `T_eff=(1/2π)√(a²+a_dS²)`.

- **(a) a0 from dS — PARTIAL (scale yes, value no).** `a_dS=cH_Λ=c²√(Λ/3)` is genuine Deser-Levin physics and IS the
  thermal floor the gate sees, so `a0~√Λ` emerges in FORM non-circularly. But `a_dS=Z·a0` with `Z=√(32π/3)≈5.79` — the
  floor is ~5.79× too big; pulling it to `a0` needs the unforced response→inertia coefficient κ (banked
  KAPPA_FORCING_DOOR_CLOSED). The `32π` is a GRAVITATIONAL normalization (`8π` Einstein × 4 horizon) living inside
  `ρ_DE=Λc²/8πG`, invisible to a kinematic kernel. **a0's value is NOT derived.** (check 2)
- **(b) deep-MOND — PASS, sympy-exact.** `a=√(a0 g_N)`, `v⁴=GM a0`, Newtonian `a=g_N` recovered. (check 1)
- **(c) stability — FAILS. THE OBSTRUCTION.** `|a|` is a 2nd proper-time derivative, so `L(x,ẋ,ẍ)` is
  higher-derivative; `d²L/d(ẍ)²=−mc²F''/a0²≠0` for any nontrivial gate ⇒ Ostrogradsky non-degeneracy ⇒ the
  Ostrogradsky Hamiltonian is linear in the conjugate `p1` (coefficient `=ẋ`, unconstrained) ⇒ energy unbounded below
  ⇒ GHOST. Propagator cross-check: residue −1 on the second pole. (check 3) **This is exactly Milgrom's 1994 wall**:
  a local Galilei/Lorentz-invariant MI gate reproducing MOND is excluded; the only stable MI realization is strongly
  time-NONLOCAL. The aether `u^μ` only LABELS the frame — it cannot lower the derivative order of the per-body gate.
- **(d) GR/SME — PASS.** `mu_fw→1` for `g≫a0` (all Solar-System internal accelerations) ⇒ standard GR. Aether kinetic
  sector healthy at `c13=0` (check 5; c_T=c via GW170817). s^TX boost dipole Saturn `8.68e-10` vs INPOP/Cassini
  `~8.3e-9` ⇒ ~9.6× margin, LIVE but PASSING (banked S_TENSOR_SME_COMPONENT_LEDGER).

**Net:** Candidate A WORKS on (a-form)/(b)/(d) but its matter gate is Ostrogradsky-unstable. It does not constitute a new
completion — it re-derives, from the action side, exactly why the framework's MI home must be time-nonlocal (Route E),
NOT an aether vector coupling. **The aether vector provably cannot evade Milgrom-1994: it labels the frame, it does not
lower derivative order.**

## CANDIDATE B (dS-Unruh NONLOCAL modified-inertia action) — FAILS on the kernel's SOURCE and the framework's COEFFICIENT.

**Form:** covariant relativistic point-particle action with a NONLOCAL (entire-exponential / infinite-derivative)
dS-Unruh kinetic factor referred to the cosmic rest frame, `a0²` set by `Λ/3` (Milgrom-1999 5D embedding `a5=√(a²+Λ/3)`;
Luo 2026 `a_bg=√(Λ/48)`).

- **(a) a0 from dS — YES for the SCALE, NO for the framework's VALUE.** Two independent literature constructions
  (Milgrom 1999 astro-ph/9805346; Luo 2026 2602.14515 — fetched, confirmed it is the kinematic dS-Unruh-broadening MI
  interpretation, 11pp, circular-orbit-limited, no CMB attempt) genuinely source `a0~c√Λ` non-circularly. **But** the O(1)
  coefficient is `√(1/3)` or `√(1/12)`, NEVER the framework's `√(1/32π)` (check 2). Same κ/Z wall as A.
- **(b) deep-MOND — YES** (same gate algebra, check 1).
- **(c) stability — PASS, but ONLY in the fully-nonlocal realization.** The entire (branch-cut) form factor has a single
  healthy pole, residue +1, no extra poles (check 4); the FINITE truncation reintroduces the Ostrogradsky ghost
  (check 3). **Nonlocality is what removes the ghost — this is real and survives.** This is the genuine advance the
  banked Route E records.
- **(d) GR/SME — YES** (Newtonian/GR recovery; preferred-frame s^TX consistent).
- **THE OBSTRUCTION — two precise points:**
  1. **The kernel is ADMISSIBLE but UN-SOURCEABLE from the dS vacuum.** The stable nonlocal kernel must be POSTULATED
     (conservative, even). It cannot be DERIVED from the dS-Unruh bath, because a PASSIVE bath gives the WRONG SIGN:
     the adiabatic inertia renormalization of any passive (dissipative) bath is POSITIVE (mass increases) = ANTI-MOND
     (check 7). MOND needs an ACTIVE, frenetic, sign-flipping kernel at `ω~ω_orbit` — and no cosmological source supplies
     it (banked passivity theorem). So the construction is FOUNDED-not-DERIVED.
  2. **Functional-class mismatch (banked MI_KERNEL).** The dS-Unruh memory is an analytic derivative expansion (integer
     powers of `ȧ`, NO `√ȧ`); Milgrom's MOND kernel is a scale-free spectral RATIO-convolution with the non-analyticity
     in the LOCAL magnitude. Different mathematical objects; the kernel SHAPE stays an AeST-class free function inside a
     bounded cone. It also does NOT do the CMB (no Ȳ=0 dust mode; the trilemma's hard corner).

**Net:** Candidate B is the most framework-native route and PARTIALLY SURVIVES (a-scale/b/c-nonlocal/d-form), but FAILS to
(i) supply its kernel from the vacuum non-circularly (passivity → anti-MOND), (ii) deliver the framework's specific
`Z=√(32π/3)`, and (iii) pass the CMB. It is REAL (Route E, literature-backed) but FOUNDED, not DERIVED.

---

## The sharpened obstruction — an EXACT trichotomy, all three horns blocked

A covariant MOND-reproducing modified-inertia completion must be one of:

1. **LOCAL aether/vector MI gate** → **Ostrogradsky ghost** (check 3; `|a|` is 2nd-derivative, `F''≠0` non-degenerate).
   The vector labels the frame but cannot lower derivative order — Milgrom-1994 wall. *(Candidate A.)*
2. **FIELD/modified-gravity MI** (promote the gate's partner to source matter) → a field matter feels is a 5th force, it
   MOVES Φ, and the slip⇔Φ Bianchi lock (check 6) plus the covariant LENSING no-go forbid a Cassini-safe covariant slip
   (`δΦ=0` impossible in any 4-diff class; Route-2 aether-multiplier escape REFUTED by explicit metric variation,
   banked ROUTE2 adversarial). Fails Cassini. *(AeST is here — modified gravity, re-incurs Cassini.)*
3. **NONLOCAL MI** (entire/branch-cut form factor) → the ONLY ghost-free corner (check 4), = the Galley doubled-worldline
   Route E. But it is NOT an aether/SME vector term, and it needs an ACTIVE kernel the passive cosmos does not supply
   (check 7). FOUNDED, not DERIVED; a0's VALUE still inherited; CMB still open. *(Candidate B / Route E.)*

**This trichotomy is the result.** Both candidates land on a blocked horn. The genuine open construction remains the
time-nonlocal Route E — and the precise missing pieces are now named: (i) an active/frenetic kernel source (the cosmos
gives only a passive bath → anti-MOND), (ii) the framework's specific `√(32π/3)` from a kinematic mechanism (the `32π`
is gravitational, unseen by the kinematic kernel), (iii) the CMB DM-mimic (no Ȳ=0 trick for a pure inertia mod).

## What a SURVIVING completion would have to evade (the value of mapping the wall)

1. **Lower the derivative order WITHOUT going nonlocal** — provably impossible for a local gate (Ostrogradsky), so a
   completion MUST be nonlocal (Route-E class). The aether vector route is dead for the *gate* (it can still supply the
   preferred frame the nonlocal kernel needs).
2. **Source an ACTIVE kernel** at `ω~ω_orbit` from the dS vacuum — every passive bath gives anti-MOND (check 7). This is
   the single hardest missing piece and it is a SIGN theorem, not a tuning problem.
3. **Deliver `√(1/32π)` not `√(1/3)`** from a kinematic dS-Unruh mechanism — the `32π` lives in the gravitational
   normalization `ρ_DE=Λc²/8πG`, which a purely kinematic kernel never sees. This is the already-closed κ-forcing wall.
4. **Pass the CMB** without a Ȳ=0 dust mode — the trilemma's hard corner (banked MODIFIED_INERTIA_the_natural_home).

## Both-ways ledger

**CREDITED at full weight (real, survives hostile recompute):** the deep-MOND/Newtonian limits and BTFR (sympy-exact,
check 1); the FORM-emergence of `a0~√Λ` from the dS-Unruh lock (`a_dS=cH_Λ` real Deser-Levin physics, check 2); the
genuine modified-INERTIA / Cassini-safe-by-class structure of the matter coupling; the HEALTHY aether kinetic corner at
c13=0 (check 5); the s^TX/SME pass (~9.6× margin); and — the genuine advance — the NONLOCAL branch-cut form factor being
ghost-free where the local truncation is not (check 4 vs 3). Route E is a real covariant MI MATTER sector.

**CONCEDED at full weight:** the covariant LOCAL aether-MI gate is Ostrogradsky-unstable (check 3); a0's VALUE is NOT
derived (only the scale; one free O(1)=κ/Z, quarantine held); the aether vector provably cannot evade Milgrom-1994 (it
labels the frame, does not lower derivative order); the nonlocal kernel cannot be SOURCED from the dS vacuum
(passivity → anti-MOND, check 7) and its SHAPE stays an AeST-class free function; the CMB DM-mimic is uncured; the
covariant Cassini-safe LENSING partner is forbidden in every 4-diff class (slip⇔Φ, check 6) and the Route-2 aether-escape
was REFUTED by explicit variation.

**Milgrom 2503.07106 cross-check (fetched, abstract verbatim):** his 2025 "linear deep-MOND" modifies BOTH inertia and
gravity, is explicitly NON-relativistic, and he DISOWNS it as a full theory ("I cannot base some acceptable MOND theory
on these models", "important drawbacks ... may make it unacceptable"). It is NOT a covariant MI completion and does not
rescue either candidate. Consistent with the trichotomy.

## One line

Both candidate covariant modified-inertia completions HIT-THE-NO-GO at precise, independently-sympy-confirmed
obstructions — Candidate A (aether/SME local gate) is Ostrogradsky-unstable (the vector labels the frame but cannot lower
the gate's derivative order; check 3, Milgrom-1994 wall), and Candidate B (dS-Unruh nonlocal) survives stability ONLY by
being nonlocal (Route E) but cannot SOURCE its active kernel from the passive dS vacuum (passivity→anti-MOND, check 7),
cannot deliver the framework's `√(32π/3)` from a kinematic mechanism (the `32π` is gravitational, unseen by the kernel;
check 2), and cannot do the CMB — so the result is an EXACT trichotomy (local=ghost / field=modified-gravity-Cassini /
nonlocal=Route-E-needs-an-unsourced-active-kernel), all three horns blocked, which maps precisely what a real completion
must evade. Deep-MOND/BTFR (check 1), the healthy aether kinetic corner (check 5), the ghost-free nonlocal form factor
(check 4), and the s^TX/SME pass are credited at full weight; a0's value is not derived (scale only); quarantine held; no
manufactured action, no high-priesting.

**Scripts (absolute):** `/tmp/mi_skeptic.py` (deep-MOND + Z coefficient), `/tmp/mi_ostro.py` (Ostrogradsky + nonlocal
form factor), `/tmp/mi_aether.py` (aether mode speeds + Bianchi slip⇔Φ), `/tmp/mi_passivity.py` (passivity/anti-MOND).
**Banked refs:** `.../reviews/COVARIANT_LENSING_NOGO_2026-06-17.md`, `.../reviews/COVARIANT_ACTION_STEP2_VERDICT_2026-06-17.md`,
`.../reviews/MI_KERNEL_FROM_DSUNRUH_2026-06-19.md`, `.../reviews/ROUTE2_AETHER_SHEAR_ABSORBING_ADVERSARIAL_VERDICT_2026-06-17.md`,
`real_research/MODIFIED_INERTIA_the_natural_home.md`. **Primaries:** Milgrom 2503.07106, AeST 2007.00082, Luo 2026 2602.14515,
Milgrom 1994 Ann.Phys.229 384.

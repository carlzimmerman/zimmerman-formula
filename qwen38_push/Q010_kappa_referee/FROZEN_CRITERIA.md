# Q010 — FROZEN CRITERIA (committed ALONE, before any re-derivation run)

**Lane:** `qwen38_push/Q010_kappa_referee/` · **Date:** 2026-10-15 · **Track:** qwen38 (closure track)
**Reclassification note:** prepared as AG5 under `argon_push/` in the interactive session; moved
under the qwen track by owner instruction ("push this up under the qwen folder") BEFORE its
first commit. AG3/AG4 handoff references to "AG5" map to this lane. Nothing was ever
committed at the argon path (append-only intact).
**Question (owner request):** the nature of cold energy and dark energy WITHOUT assumptions —
operationalized as: referee the pending GF2 register-upgrade line ("κ=½: DERIVED as the
closure coefficient"), re-derive the whole κ-chain independently, audit every junction with
citation-level precision, and publish the assumption ledger for cold/dark energy.

## Status quo being adjudicated (recon, pre-freeze; updated for the qwen38 track)

- **GF2 (5b173a046, pending referee):** Φ=C ln r [P1 committed] + Poisson ⇒ ρ=C/(4πG)r⁻²
  (γ=2 FORCED) + stationarity/barotropy ⇒ σ²=C/2; κ_dyn := σ²/v_flat² = ½; uniqueness lemma
  (γ=2 unique self-sourced power law); ledger 0/4 entries carry ½; MUTATE γ=2.1 ⇒ κ=0.476.
- **GF1 (web):** κ_germ := a₀/s = 1/n exact (s=n·a₀ committed tie scale); web
  UNDERDETERMINED-BY-ONE-INTEGER (0/6 pins); R3b transport: under **rung 5** (equilibrium
  identification "halo=phantom, coefficient 1" — deepseek_push/THEORY.md L64, carried
  status), γ=2 ⇔ response exponent ½ ⇔ n=2 shape; tie empirical: n_germ = 2.000102±0.0172;
  H1/H2: R1/R2 are reductions, not derivations.
- **Triad identification:** κ = σ²/v_flat² = c_s²(deep) = a₀/s carried in
  THE_HORIZON_FORM_OF_THE_BTFR.md L58 with "the coefficient 1/2 is κ, **fitted**";
  G002 (glm53) one-function chassis derives a₀=s/2, κ=1/n, w=−1 GIVEN the chassis;
  THEORY.md L87: rung 4 was "honest-postulated" pre-GF2.
- **qwen38 track state (this track's own certified material — the dynamical face is already
  multiply derived):**
  - **Q001** (py + lean/Q001_sound_speed_identity.lean): σ_Z² ≡ c_s² ≡ P/ρ_ph = √(GM_ba₀)/2
    — the rung-4 temperature as a CONSTITUTIVE EOS property of the L247 medium (Lean).
  - **Q007** (lean/Q007_triad_half.lean): the ½ AMPLITUDE derived — isothermal hydrostatics
    of the flatness-selected r⁻² profile closes to v_c²=2σ²; with G03E's linear mass law,
    σ²=v_flat²/2 at every r; density and temperature coefficients are ONE identity
    A=σ²/(2πG) (Lean, pure algebra). **Lane-state fact for the J4 audit table:** Q007's
    Python run is a PRESERVED TRACEBACK (assert V1 "density coefficient inconsistent with
    linear mass law") — the Lean certificate stands; the py-lane inconsistency is recorded,
    NOT re-run or repaired here (sibling-track hygiene: read-only).
  - **Q002** (omega_lambda selector), **Q009** (marginal zero mode, Lean) — adjacent
    selector/zero-mode material, cited where relevant.
- **AG1 constraint on P1:** log branch/V1 closure identity SURVIVES the G081 reversal; the
  static ball is ill-posed and A/r² annuli need w<7.44 (AG3: observed median 1.84 ⇒ the
  SIS closure device is realized in the outer annulus regime, not the interior — AG3 K4
  X_ball=0.0025). P1's physical reach is the annulus/deep limit, per GF2 README's own
  graceful-degradation border.
- **ARGON01:** local modulus route to κ CLOSED; C₀-invisibility ⇒ ρ_vac calibration-only.

## Gates (exit 0 iff J1–J3, J5–J7 pass and verdict ∈ {UPHELD-FULL, UPHELD-QUALIFIED})

- **J1 closure re-derivation (independent sympy, no GF2/Q007 import):** ∇²(C ln r) = C/r²;
  Poisson ⇒ ρ = C/(4πG)r⁻²; hydrostatic+barotropic ⇒ σ² = C/2; κ_dyn = ½ exact; numeric
  controls reproduce the REGISTERED values: σ(M_b=6.5e10) = 119.2 km/s, σ(1e11) = 132.76.
- **J2 uniqueness lemma (independent):** (i) defect form: d/dr[∇²(C ln r) − 4πGAr^{−γ}] =
  −4πGA(2−γ)r^{1−γ} — vanishes ∀r iff γ=2; (ii) two-point form: Φ′=γσ²/r (hydrostatic,
  const σ²) + Poisson at r∈{1,2} ⇒ 2^{−γ}=1/4 ⇒ γ=2 (A≠0). Both exact.
- **J3 web re-derivation (independent):** Z²=n²·8π/3; AΛ=8π²n²/c⁴; Ω_Λ=8πn²a₀²/(3H₀²c²);
  cH₀/a₀=n√(8π/(3Ω_Λ)); κ=a₀/s=1/n given s=na₀. Numeric battery reproduces GF1 registers:
  germ ratio 4.000406, Z 5.788810, cH₀/a₀ 6.99465 vs n=2 prediction 6.99430, Ω_Λ 0.685.
- **J4 junction audit (citation-level, the crux):** table of every link in
  κ_dyn=½ → κ_germ=1/n → a₀=c√(Gρ_Λ)/2 with file:line evidence and status ∈
  {DERIVED, TEXTBOOK, POSTULATED-CARRIED, IDENTIFICATION-CARRIED, EMPIRICAL-TIE,
  LEAN-CERTIFIED-TRACK}. Rows MUST include: rung 4 (THEORY.md L87 → GF2/Q001/Q007 status),
  rung 5 (THEORY.md L64), triad line (HORIZON-BTFR L58), G002 κ definition and chassis
  outputs, GF1 R1e/H2, Q007 py-traceback lane-state row. No link may be silently promoted.
- **J5 new relations (zero new assumptions):** capacity–DE relation Σ̄_max = a₀/(πG) =
  κc√(ρ_DE/G)/π (AG4 T5 Lean + S1 tie), numeric at registers (κ=½ ⇒ 213.7 M⊙/pc²);
  G002 V16 zero-mode restatement (DE pinned |c|<0.02, κ/a₀/RAR shift-invariant) —
  recompute the shift-invariance algebra exactly.
- **J6 Lean certificate (qwen38_push/lean/Q010_kappa_closure.lean):** COMPLEMENTARY to
  Q001/Q007 — no restatement of their amplitude/constitutive theorems. New: log-branch
  derivatives (HasDerivAt C·ln and C/x), Laplacian algebra Φ′′+2Φ′/r = C/r², Poisson
  coefficient identity (γ=2 case, cleared), two-point uniqueness γ=2 (via log/rpow
  injectivity), germ identity a₀/s=1/n, capacity–DE cleared identity, shift-invariance
  of the dynamical face under f→f+c (zero-mode algebra). Zero sorry; axioms ⊆ {propext,
  Classical.choice, Quot.sound}; statements sympy-prechecked before typing.
- **J7 mutations:** M1 γ=2.1 ⇒ defect ≠ 0 AND κ moves to 0.476 (reproduces GF2's declared
  MUTATE value 2.38% off ½ — cross-lane mutation control); M2 n=3 ⇒ Z/boundary registers
  break (web is a point not a basin, echoing GF1 R4a); M3 rung-5 removal probe: with the
  identification link dropped, the verdict must degrade to IDENTIFIED (demonstrates the
  qualification is load-bearing).

## Pre-registered verdict vocabulary (exact readings)

- **UPHELD-FULL:** J4 finds the junction κ_dyn=κ_germ DERIVED somewhere in the record
  (a cited derivation deeper than identification).
- **UPHELD-QUALIFIED:** J1–J3 re-derive clean AND the junction is exactly the rung-5
  equilibrium identification + carried triad (postulate/identification status, cited),
  with the empirical integer pin (n=2.000±0.017, three channels + lockstep falsifier)
  standing behind the value. Register line becomes: "κ=½: DERIVED as the closure
  coefficient of the dynamical face (three independent routes: GF2 closure, Q001
  constitutive, Q007 amplitude — the latter two Lean-certified); germ face tied by exact
  κ=1/n web; cross-face identification = rung 5 (carried postulate); value anchored
  empirically at 0.06%."
- **REVERSED:** any of J1–J3 fails to reproduce, or the audit finds the number ½ imported
  into the closure chain (GF2's 0/4 ledger false), or P1's status is weaker than
  committed-certified.
Expected from recon: UPHELD-QUALIFIED. Expectation is NOT a result; the gates decide.

## Kill test (of this lane's conclusion)

A derivation of the rung-5 identification from S2 + a relativistic completion would
upgrade QUALIFIED→FULL (that is §3's relativistic-completion open item — out of scope
here, registered as the door). Falsification of the value: >3σ split between the germ-tie
integer and the slope-channel integer (GF1's registered lockstep falsifier) would break
the web regardless of this referee's algebra verdict.

## Provenance / hygiene

Registers read at runtime (a₀, ρ_Λ, H₀, Ω_Λ from G081_results.json / GF1_results.json);
GF2/GF1/G002/THEORY/HORIZON-BTFR/Q001/Q007 files read-only (sibling-track hygiene — the
Q007 py traceback is recorded, not repaired); nothing outside qwen38_push/ touched except
this lane's own reads; ledger/register edits handed to conductor as proposals only.

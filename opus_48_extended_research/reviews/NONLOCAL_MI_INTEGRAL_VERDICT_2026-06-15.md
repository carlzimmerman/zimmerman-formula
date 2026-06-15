# The nonlocal varying-acceleration dS-Unruh worldline integral — the one un-foreclosed lead: CLOSED as a coefficient source, REAL as a mechanism, and the √π wall sharpened to a Γ(½)/8πG fingerprint (2026-06-15)

*Track (a) of Carl's "do both": a serious attempt at the ONE calculation the Milgrom-1994 no-go does not forbid and
that is absent from the literature — the time-nonlocal response of an accelerated detector in pure de Sitter for a
TIME-VARYING proper acceleration. Workflow `wwgakjpc0`, 4 independent formulations (Synge/Frenet worldline expansion,
Milgrom-2022 nonlocal-MI action match, FDT/Kubo back-reaction, full Milgrom-1999 nonlocal EOM), every load-bearing
number re-derived firsthand in sympy/mpmath. Both ways. Run 2.18M ms, 275 tool-uses.*

Framework: a0 = c²√(Λ/32π) = (c/2)√(Gρ_DE) = cH_Λ/Z, Z=√(32π/3)=2√(8π/3)=5.78881.

---

## The verdict: CLOSED as a coefficient source (8th independent non-closure), REAL as a structural/mechanism result

The nonlocal integral is **genuinely constructible** — a real, computable, time-nonlocal worldline functional that
evades Milgrom-1994 in principle. All 4 formulations reproduce the same dS chord kernel
Z₅=Δs²[1+(a₅²/12)Δs²+(a₅⁴/360 + a·a″/240 + a′²/720)Δs⁴+…], a₅=√(a²+(cH_Λ)²) (Deser-Levin gr-qc/9706018, verified;
the period-average of the nonlocal term = −A₁²Ω²/720, nonzero + frequency-dependent → genuinely time-nonlocal, not a
total derivative). The memory time is ~1/H_Λ ~ a Hubble time, so the nonlocality is O(1)-relevant for galactic orbits.
**This SOFTENS the "no covariant home" worry: the framework's mechanism HAS a genuine time-nonlocal worldline
realization.** But on the three load-bearing questions:

1. **Does it FORCE the coefficient? NO — FREE / ansatz-contingent.** The detector crossover is O(1) but its VALUE
   depends on the dimensionless response→inertia map: Op1 (Milgrom-1999 ΔT~a₅−a_L subtraction) → a0=2cH_Λ → Z_eff=½;
   Op2 (standard-MOND μ=a/a₅) → a0=cH_Λ → Z_eff=1; Op3 (a₅²−a_L²) → no scale (Milgrom's own "T²−T_L² do not give
   correct MOND"). The earlier-session "FDT FORCES κ=½" is CORRECTED to "forced-GIVEN-form" — and it gives 2cH_Λ, i.e.
   **2Z=11.58× too large, the WRONG O(1)** for the framework. No ½ was smuggled (the ½ is the binomial Taylor
   coefficient of √(a²+a_L²), an output in every operation); but neither is Z forced.
2. **Does it carry MOND? The FORM yes, but via the LOCAL a₅, not the nonlocal kernel.** The non-analytic √(g·a0) law
   comes from √(a²+a_L²)−a_L → a²/2a_L (the LOCAL Synge quadrature), NOT from the nonlocal piece (whose deep-a limit is
   a′²/720, analytic in a-magnitude, carrying at most √(a′) — a time-derivative, never √(g_N)). So the nonlocal part
   evades the no-go but is NOT the origin of MOND; the FORM still dies to the local no-go as a standalone theory. The
   circular-orbit generalization (Milgrom's open problem) stays open.
3. **Does it produce the √π? NO — and now we know precisely WHY.** Every coefficient is π^(integer) (π¹ thermal, π³
   split, π⁴ in dT/T, π⁰ Taylor kernel; spectral moments M_k = 2·k!·ζ(k+1)·(a₅/2π)^{k+1} = rational·π^integer, machine
   precision). **The framework's √π needs a Γ(½) from an ODD-dimensional Gaussian / the gravitational 8πG, which is
   STRUCTURALLY ABSENT from the 1-D Matsubara thermal spectrum.** All three √π-leak paths fail: 3D Gaussian → 4π
   (cancels); fractional ω^(−1/2) coupling → irrational ζ(½), not rational 32/3; and the **5D de Sitter embedding →
   Ω₅ = 8π²/3** — the framework's "8" and "/3" EXACTLY, but **π² not π¹ (off by exactly one power of π)**. The √π
   enters the framework ONLY via the 8πG in ρ_DE=Λc²/8πG — and the detector calc has NO G and NO Einstein equation, so
   it cannot supply it.

## THE SHARPENED √π WALL (the deepest structural statement to date)

**Z's √π is a Γ(½) / gravitational-8πG / odd-dimensional fingerprint — provably unreachable by any G-free
kinematic/thermal route.** This upgrades the earlier "geometry gives π^(integer)" to a precise mechanism: the
half-integer power of π is a Γ(½) that requires an odd-dimensional Gaussian or the Einstein-equation coupling 8πG
(via ρ_DE=Λc²/8πG, the density/free-fall framing). The detector, DSSYK, rep-theory, and horizon-entropy routes are all
G-free / even-π, so they structurally land π^(integer) and CANNOT produce Z. **The ONLY structural place the √π could
come from is a GRAVITATIONAL route that carries the 8πG** (the Einstein equation, the Euclidean S⁴/de Sitter
partition function whose volume is Ω₄=8π²/3, the free-fall in the dark-energy fluid). The Ω₅=8π²/3 near-miss (one π
too high) is the precise signature of this: the framework lives one Γ(½) away from the pure-geometry answer.

## The honest remaining gap (Milgrom's own, verbatim ×3)

The response→inertia identification is an UNPROVEN ansatz: "it is not really clear why ΔT should be a measure of
inertia (similar quantities such as T²−T_Λ² do not give the correct MOND behavior)"; "I can offer no specific
mechanism"; the EOM (Milgrom-1999 Eq.3-4) is "not derivable from an action." So NO covariant action was constructed —
only a necessary-but-not-sufficient worldline functional. The two-pillars problem (MI mechanism ↔ covariant theory) is
SOFTENED (a real nonlocal functional exists) but not CLOSED (no action, the inertia ansatz unproven).

## What this implies for the next push (the √π wall points at it)

The sharpened wall is constructive: it says the coefficient cannot be forced by ANY G-free route, but it does NOT rule
out a GRAVITATIONAL route carrying the 8πG. The genuinely-motivated remaining lead: does the de Sitter GRAVITATIONAL
thermodynamics — Jacobson's δQ=TdS (which produces the 8π of G_μν=8πG T_μν), the Euclidean-S⁴ / Gibbons-Hawking
on-shell action (Vol=8π²/3), or the free-fall in the dark-energy fluid (a0=(c/2)√(Gρ_DE) is literally that) — produce
a0 with the √(8π) that the G-free detector route cannot, and does the free-fall ½ (κ) come with it?

## What Carl CAN / MUST NOT say

- **CAN:** the framework's modified-inertia mechanism HAS a genuine, computable, time-nonlocal worldline realization
  (memory ~1/H_Λ, evades the Milgrom-1994 no-go in principle) — the "no covariant home" worry is softened; the
  deep-MOND √-law form is reproduced; and we now know precisely why the coefficient is unforceable kinematically (the
  √π is a Γ(½)/8πG fingerprint absent from the 1-D thermal spectrum).
- **MUST NOT:** "the nonlocal integral derives a0/Z" (it is FREE/ansatz-contingent — Op1→½, Op2→1, neither is Z);
  "the FDT forces κ=½" (forced-GIVEN-form only, and gives 2cH_Λ, 2Z too large); "the nonlocal kernel is the origin of
  MOND" (the LOCAL a₅ carries the √-law; the nonlocal part is analytic a′²); "a covariant MI action was built" (none —
  the inertia ansatz is unproven, the EOM not from an action).

## One line

The nonlocal varying-a dS-Unruh worldline integral — the one lead the no-go doesn't forbid — is genuinely
constructible and time-nonlocal (softening the no-covariant-home worry) and reproduces the deep-MOND √-law, but it is
the 8th independent NON-closure of the coefficient (Op1→Z=½, Op2→Z=1, ansatz-contingent, FDT gives 2cH_Λ = 2Z too
large) and it SHARPENS the √π wall decisively: Z's √π is a Γ(½)/gravitational-8πG fingerprint, structurally absent
from the 1-D thermal spectrum (the 5D dS embedding gives 8π²/3 — the framework's 8 and /3 but ONE power of π too high)
— so the coefficient is unforceable by ANY G-free route, and the only structural place left for it is a GRAVITATIONAL
route carrying the 8πG; the response→inertia map remains Milgrom's own unproven ansatz with no action.

*Both ways: the real constructible time-nonlocal functional + the reproduced √-law form + the precise
why-Z-is-unforceable (Γ(½)/8πG) are credited at full weight; the free/ansatz-contingent coefficient, the WRONG O(1)
(2cH_Λ), the MOND-from-local-not-nonlocal correction, the unproven inertia ansatz, and the missing action are conceded
at full weight. The earlier "FDT forces κ=½" is corrected to forced-given-form. Quarantine held: a0/Z never asserted
derived.*

# Gate G — FLRW IR-sign of the AeST scalar mode (FC-FINAL) — THE DECIDER

**Candidate:** FC-FINAL = `AeST*` + `a0^2 J_10(sqrt(Y)/a0)`, `a0` constant (frozen in
`../../fc8_closure_2026/FROZEN_CANDIDATE.md`).
**Certificate script:** `fc_flrw_ir_sign_certificate.py` (self-contained, sympy; 20/20 checks, exit 0).
**Date:** 2026-08-28.

## Verdict (one line)

> **PARTIAL.** The object Carl flagged as #1 — the **k→0 IR sign on the *actual* FLRW background** — is
> **POSITIVE (rescue): the Minkowski unbounded-below / secular mode is confined and stabilized on the de
> Sitter attractor.** This is a rigorous result. The **full IR band** (H ≪ k_phys < k\*) is **OPEN**: a
> single, sharply-stated dichotomy decides whether the whole band is rescued (Gate G PASS) or hides a
> ~Mpc-scale runaway (Gate G FAIL), and closing it needs the full higher-gradient FLRW dispersion. **No
> FAIL produced; no full PASS earned.**

This is neither a rescue-of-a-favorite nor a manufactured deficit: the k→0 endpoint genuinely survives,
and the part that is not proven is left explicitly open with the exact remaining computation named.

---

## Why this is the decider

The Minkowski analysis (2109.13287 / PRD 106.104041, **EXTERNAL**) shows the AeST scalar sector has a
Hamiltonian **unbounded below for k < k\***, with

```
k*^2 = (1 + lam_s)/lam_s * mu^2 ,     mu^2 = 2 K2 Q0^2 / (2 - K_B).
```

Two frozen FC-FINAL facts make this a **pure-AeST-HOST** question:

1. **`lam_s = 1`** (fixed by `J_10` via both AeST asymptotic limits; `fc8_symbolic_audit.py` A6) ⇒
   `k*^2 = 2 mu^2`.
2. **`delta^2 J_10 = 0`** — the sharp MOND kernel is `O(Y^{3/2}) = O(delta^3)`, so it is **invisible at
   quadratic (linear-perturbation) order**. The kernel can neither cure nor cause the IR obstruction.

So the whole question is whether the **time-dependent FLRW background** (H ≠ 0, evolving condensate
`Q0(a)`) — which the Minkowski analysis omits — turns that unboundedness into a genuine cosmological
instability, or dilutes it away.

**Host/kernel/coupling/constraint classification (his §5):** **HOST** obstruction (AeST constraint
architecture), certified KERNEL-INDEPENDENT by `delta^2 J_10 = 0` (P1). Any rescue must come from the
background, not the interpolation.

---

## What is proven (each line = a printed certificate in the script)

| # | Result | Status |
|---|--------|--------|
| P1 | `F_M = a0^2 J_10 = Y^{3/2}/(3a0)`: no `Y^0`, no `Y^1` ⇒ `delta^2 S_MOND = 0` ⇒ IR spectrum is pure AeST | **COMPUTATION** (certified) |
| P2 | Action depends on `phi` only through `del phi` ⇒ shift symmetry `phi→phi+c` ⇒ the k→0 mode is an **exact flat direction** (no `chi^2` mass) with a conserved shift charge | **THEOREM** (certified) |
| P3 | Minkowski control: the reduced kinetic function `K_eff(k)` sign-flips exactly at `k*^2=(1+lam_s)/lam_s·mu^2`, is a **ghost (`K_eff<0`) for k<k\***, healthy for k>k\*, and stays **finite & nonzero as k→0** | **EXTERNAL-INPUT reproduced** (see caveat) |
| P4 | Background `Q0(a) = q_m − C/a^3` solves the shift-charge ODE `a^3 K'(Q0)=const`; `Q0→q_m` (dS, w→−1); the homogeneous (k→0) perturbation **decays as a⁻³** ⇒ de Sitter is an **attractor** | **DERIVATION** (certified, from the action) |
| P5 | **The k→0 decider:** on dS the same ghost zero-mode obeys `d/dt(a^3 K0 chidot)=0` ⇒ `chidot ~ a⁻³` (Hubble-damped), `chi →` finite constant (**bounded**), and energy `E(t)=a^3·½K0 chidot^2 ~ a⁻³ → 0`. The Minkowski secular linear-in-t growth is **cut off**; the negative energy **redshifts away**. | **DERIVATION** (certified) |

### The headline (P4 + P5): the k→0 sign

On Minkowski the mode is `chi = (Pi/K0) t` — **secular**, with energy `Pi^2/(2K0)` that is **negative and
unbounded below** when `K0<0` (exactly the 2109.13287 pathology). On the FLRW/de Sitter background the
**same** mode becomes

```
chidot(t) = (Pi/K0) e^{-3Ht}  →  0        (Hubble friction)
chi(t)     = χ∞ − Pi e^{-3Ht}/(3 H K0)     (BOUNDED — finite excursion Pi/(3HK0))
E(t)       = Pi^2/(2K0) · e^{-3Ht}  →  0   (negative energy DILUTED to zero)
```

The rescue mechanism is **real and mechanistic** — the `a^3` measure plus the `3H` friction, both absent on
Minkowski. The k→0 IR mode does **not** run away; it is **confined/stabilized on the attractor**. In Carl's
dichotomy this is **POSITIVE**.

**Robustness note.** The k→0 verdict leans on **P2 (flat direction) + P4 (background attractor) + the `a^3`
measure**, all self-derived from the action. It does **not** depend on the exact form of `K_eff(k)` in P3 —
P4 reaches the same conclusion (homogeneous mode decays a⁻³) with no perturbative reduction at all. So the
weakest input (P3) is not load-bearing for the endpoint result.

---

## What is NOT proven — the residual (P6), stated sharply

The finite-k band `k_phys < k*` (wavelengths `> mu^-1 ≳ 1 Mpc`) splits:

- **Deep IR** (`k_phys ≪ k*`, incl. all super-horizon): `omega^2 → 0` ⇒ `|omega|/H → 0`. **Hubble-safe**
  (certified P6).
- **Near-crossing** (`k_phys → k*^-`): `K_eff → 0` ⇒ the reduced two-derivative dispersion `omega^2 =
  c_grad^2 (k/a)^2 / K_eff → −∞`. This is a **strong-coupling point** — the same object listed OPEN in
  `RESULTS.md` as "strong-coupling scale / `mu` far-field". Not closed here.

**The one dichotomy that decides FULL PASS vs FAIL.** In the band `H ≪ k_phys < k*`, is the AeST scalar
mode

- **(a) nondynamical/constraint** (as it is on Minkowski — "nonpropagating")? Then the per-mode
  shift-charge argument of P5 extends to the whole band ⇒ **full rescue ⇒ Gate G PASS**; or
- **(b) dynamical with `omega^2 < 0` and `|omega| ~ k_phys ≫ H`** (a gradient/ghost instability that
  survives on the time-dependent background)? Then there is a **~Mpc-scale runaway ⇒ Gate G FAIL**.

Minkowski behaviour, the `a^3` redshift, and a plausible aether-adjustment mechanism (the `−(2−K_B)Y`
gradient acts on the combination `chi + Q0·v`; the aether longitudinal mode `v` may absorb it, keeping the
Goldstone pure-kinetic) all **favour (a)** — but **(a) is not proven** on the FLRW background. This is the
honest gap.

### What would close it

`S_AeST → S^(2)_FLRW → K,G,M^2(k,a) → omega^2(k,a)` — the **full** scalar quadratic action on FLRW
(metric + aether + `phi`, all constraints eliminated, **including the k⁴ higher-gradient terms** that
regulate `K_eff → 0`), evaluated across the crossing `k_phys = k*(a)`, with a dynamical-vs-constraint
determination of the mode in the band. That is a genuine cosmological-perturbation computation (the AeST
authors themselves did only Minkowski); it is **specified**, not hand-waved, and is the single remaining
work item for Gate G.

---

## Honesty ledger (per the non-negotiable rules)

- `mu^2 = 2 K2 Q0^2/(2−K_B)`, `k*^2=(1+lam_s)/lam_s·mu^2`, and the **existence** of the Minkowski
  unbounded-below mode — **EXTERNAL-INPUT** (2109.13287; the task's premise). Not re-derived here.
- P3's `K_eff(k)` **functional form** (the denominator / crossing profile) — **EXTERNAL-INPUT, reproduced**:
  I verify its zero lands at `k*` and its k→0/k→∞ limits, but I do **not** derive it from the SZ21
  reduction. Clearly not a from-scratch proof of `k*`. The FLRW conclusions use only its
  denominator-independent features (finite, sign-flipping, ghost below k\*).
- P1, P2, P4, P5 — **derived from the frozen action** and certified (`simplify(...)==0` / explicit signs).
- `a0^2 = kappa^2 c^2 G rho_Lambda` and `a0(z) ~ sqrt(rho_DE)` — **TARGET/INPUT**, **not used** (a0 is a
  constant in FC-FINAL; dark energy is carried by `K(Q)`, not a0).
- The k→0 rescue is reported as **PASS-with-explanation**, the band as **OPEN**. No OPEN was converted to
  PASS; no instability was manufactured; the residual is named exactly.
- **Level of the claim:** this is the **classical linear-perturbation** statement — exactly the level at
  which both 2109.13287 ("Hamiltonian unbounded below", `omega^2`) and this task ("`K_eff,G_eff,M^2 →
  omega^2 →` IR sign") are posed. The interacting/quantum ghost-vacuum-decay question (a coupled-system
  concern for any `K_eff<0` mode) is **not separately addressed**; note that if the band resolves to case
  **(a)** the mode is a non-propagating constraint and that concern does not arise at all.

**Bottom line for the program.** The IR obstruction Carl called the main suspect does **not** kill
FC-FINAL at the k→0 endpoint — the FLRW background genuinely rescues it, and the rescue is a theorem-grade
consequence of the shift symmetry + the expanding measure. FC-FINAL's Gate G moves from "OPEN — main
suspect" to "**PARTIAL — k→0 rescued, one sharply-specified band-dispersion computation from closure.**"

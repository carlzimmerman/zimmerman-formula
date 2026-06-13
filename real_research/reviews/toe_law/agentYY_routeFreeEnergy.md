# agentYY — ROUTE 1: the crossed-product FREE ENERGY F(a) along a boost orbit

*agentYY, 2026-06-13. WW's named next calc (the ONLY known route to a derivational upgrade of
a0's SCALE): does the dressed type II_1 observer's crossed-product free energy F(a)=E−T·S_gen
along a boost orbit of proper acceleration a have a genuine thermodynamic EXTREMUM (dF/da=0) or
a transition AT a~cH=H — FORCING the inertial-transition scale from the modular thermodynamics
WITHOUT φ — or is F(a) monotone so the scale stays external (STRUCTURAL CEILING)? Units ħ=c=k_B=1,
so cH=H. Artifact: `agentYY_routeFreeEnergy.py` (sympy+mpmath, all checks PASS). Coefficient
quarantine (q=1/4, Z) held throughout.*

---

## VERDICT: **STRUCTURAL-CEILING-CONFIRMED** — F(a) is MONOTONE, no extremum/transition at a~H.

The crossed-product free energy reproduces the algebraic a~H crossover of the temperature but
does NOT supply a thermodynamic extremum there. The a0 scale stays an EXTERNAL input. WW's honest
prior (likely monotone) is CONFIRMED, on the merits, machine-checked across three physically
distinct energy/entropy assignments plus a general theorem.

---

## BANKED SETUP (cited, not re-derived)
- Modular temperature on a boost orbit of proper accel a (WW machine-verified Tolman identity):
  **T(a)=√(a²+H²)/2π** = Tolman blueshift H/(2π|ξ|) of the GH temperature, |ξ|=H/√(a²+H²).
- Crossed product (Witten 2112.12828, CLPW 2206.10780): dressed generator ĥ=H_mod+q (q≥0 =
  observer clock energy), ρ̂~e^{−βĥ}, β=2π/H in boost time; the +q makes the trace FINITE (type
  II_1). Generalized entropy **S_gen=⟨ĥ⟩/T+S_out** (≡⟨βĥ⟩+S_out+const).

## THE COMPUTATION (3 models + theorem + loophole, all in the .py)

**Model A — literal Witten S_gen=⟨ĥ⟩/T+S_out.** The proper observer energy blueshifts as
E(a)=q₀·B(a), B=1/|ξ|=√(a²+H²)/H, and T(a)=T_GH·B(a) blueshifts by the *same* factor.
⇒ ⟨ĥ⟩/T = E/T is **a-INVARIANT** (the Tolman factor cancels exactly): S_gen=S₀+2πq₀/H.
Hence **F(a)=E−T·S_gen = −T(a)·S₀ = −S₀√(a²+H²)/2π**, with **dF/da=−S₀a/(2π√(a²+H²))**.
**No interior zero** (vanishes only at a=0); F monotone-decreasing. F(0,H,2H,10H)/S₀ =
−0.159, −0.225, −0.356, −1.599.

**Model B — entropy as a frame-invariant pure number** (proper E and T, boost-frame S).
Algebraically collapses to the SAME F=−T·S₀ (the q-energy term and its T-rescaled entropy
contribution cancel identically). Monotone, no stationary point.

**Model C — HOSTILE, the one way to break the cancellation:** give the QFT bath a genuinely
a-dependent thermal entropy at the LOCAL temperature, conformal gas F_gas=−K·T^{n+1} for
arbitrary power n>0. Then dF/da = −[K(n+1)Tⁿ+S₀]·a/(2π√(a²+H²)); the bracket is **>0 for all
a**, so dF/da has the sign of −a: **monotone-decreasing, no interior extremum**, for every n.

**THEOREM (the structural ceiling, why no F is stationary at a~H).** The crossed product fixes
ONE generator (β=2π/H, the boost); the worldline enters ONLY through the Tolman factor, i.e.
ONLY through T(a). Every energy/entropy piece blueshifts by the same 1/|ξ|, so **F(a)=Φ(T(a))**
for some Φ. Then dF/da=Φ′(T)·dT/da, and **dT/da=a/(2π√(a²+H²))>0 for all a>0** (zero only at
a=0). An interior dF/da=0 thus REQUIRES Φ′(T)=0 — a stationary point of the free energy *in
temperature*. But T(a=H)=√2·H/2π is an ordinary interior temperature; H sets the OFFSET inside
√(a²+H²), it does not create a zero of Φ′. To land the extremum at a~H, Φ would have to know H
TWICE (once in T(a), once to place Φ′=0 exactly at T(√2 H/2π)); the crossed product supplies H
only ONCE (the modular offset). **NOT FORCED.**

**Loophole (a turnover via opposite-sign terms)** Φ=A·Tᵖ−C·Tʳ gives Φ′=0 at
T*=(Cr/Ap)^{1/(p−r)} — but T* is set by the FREE coefficients A,C,p,r; demanding T*=T(a=H) is a
by-hand constraint (must input H and tune A/C), NOT algebra-forced. And the crossed product
furnishes no such opposite-sign competing term anyway: E≥0, S≥0, F=E−TS monotone in T (Models
A–C confirm).

## TRANSITION vs EXTREMUM (the central trap, addressed directly)
a~H is the smooth crossover where the two terms inside T=√(a²+H²)/2π (Unruh a/2π vs GH H/2π) are
equal — a feature of T's ALGEBRA (descriptive), reproduced by the structural identity. It is
**NOT a thermodynamic transition of F**: F and all its derivatives are smooth/analytic in a²,
machine-checked — F″ at a/H=0.50/0.99/1.00/1.01/2.00 = −0.114/−0.0571/−0.0563/−0.0554/−0.0142,
no kink, no jump, no latent heat, no dF/da=0. The crossover is not the extremum.

**Full Deser–Levin with c_χ:** T=√(a²+(c_χH)²)/2π has the identical structure; dT/da>0 (zero
only at a=0); the crossover merely relabels to a~c_χH (still an INPUT scale fixed by H and c_χ).
c_χ does not create a zero of Φ′. Verdict unchanged.

## DERIVES SCALE? — NO (structural, not derivational)
The type II_1 free energy **structurally reproduces** the algebraic a~H crossover (it is a
function of T_DL, whose crossover is at a~H by construction). It does **NOT derivationally FORCE**
a~cH: there is no extremum, no transition, no stationary condition that singles out a=H from the
thermodynamics. The scale H remains the external modular offset = an INPUT. This is the WW
structural/derivational boundary, now confirmed SHARPER from the free-energy side.

## QUARANTINE
q=1/4 / Z never asserted. No extremum even lands at a~H, so there was nothing to probe for a
coefficient — the quarantine question never arose. Reported honestly both ways: the prior
(monotone) was the likely outcome and it is what the computation gives, on the merits, robustly
across all reasonable conventions (literal Witten S_gen, invariant-entropy reading, hostile
a-dependent bath, full DL with c_χ).

## STATUS: BANKED — STRUCTURAL CEILING CONFIRMED. F(a)=Φ(T(a)) monotone; dF/da≠0 at any interior
a; a~H is a smooth descriptive crossover, not a thermodynamic extremum/transition. The crossed-
product modular thermodynamics is a FOUNDATION that REPRODUCES the scale algebraically, NOT a
derivation of a0's scale. The only path to a derivational upgrade would need machinery that
supplies H a SECOND time (to place Φ′=0 at a~H) — absent from the type II_1 crossed product.

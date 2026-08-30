# Phase III — Causal Variation / In-In (CTP) Construction

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

Phase II found that the first variation δM is a **nonlocal transport
expression** carrying an **unfixed integration constant** (the homogeneous
solution of the transport PDE, which is constant along each flow line of `U`).
This phase shows how the **in-in / Schwinger–Keldysh / closed-time-path (CTP)**
prescription fixes that constant and makes the variation causal and unique.

---

## 1. The ambiguity to be fixed

The transport PDE for δM (Phase II, eq. ∗∗) is first order along the flow:
```
U^μ ∇_μ (δM) + (∇·U)(δM) = S[g, δg, δU, δZ] .
```
Its general solution is
```
δM = δM_h + δM_p ,
```
where
- `δM_h` is the **homogeneous** solution: constant along each flow line of `U`
  (it is the transported integration constant, i.e. data on a Cauchy surface),
- `δM_p` is a **particular** solution (the forced response to the source `S`).

The frozen action does **not** fix `δM_h`. Two variations δg that differ only in
how they move the Cauchy-surface data give different δM. Hence
`E_{μν} = δM/δg^{μν}` is **not uniquely defined** by the action alone. This is
the central defect the causal prescription must cure.

---

## 2. The CTP / in-in setup

We place the theory on the closed time contour
```
C = [t_0, t_max] (forward, +)  ∪  [t_max, t_0] (backward, -) .
```
Each field `Φ` is doubled to `Φ_±` on the two branches. The CTP action is
```
S_CTP = S[Φ_+] - S[Φ_-] + B_CTP ,
```
with the **boundary prescription** `B_CTP`:
- **Causal initial conditions** at `t_0`: the fields on both branches coincide
  at `t_0` and are set to the physical (retarded) initial data, e.g.
  `Φ_±(t_0) = Φ_phys(t_0)`, `δΦ_±(t_0) = 0`.
- **Turning-point matching** at `t_max`: the two branches coincide at the
  turning point, `Φ_+(t_max) = Φ_-(t_max)`, i.e. the **difference field**
  `Φ_Δ = Φ_+ - Φ_-` vanishes at `t_max`:
  ```
  Φ_Δ(t_max) = 0   for all fields Φ, including M_Δ = M_+ - M_- .
  ```

The **physical** field is the average `Φ_c = (Φ_+ + Φ_-)/2`; the **difference**
field `Φ_Δ` is a bookkeeping device that vanishes at the turning point. The
classical field equation is obtained by varying `S_CTP` with respect to the
**difference** field `Φ_Δ` and taking the physical limit `Φ_Δ → 0`.

---

## 3. How the in-in prescription fixes the integration constant  (decisive)

**DERIVED:** The turning-point condition `M_Δ(t_max) = 0` is precisely the
condition that **fixes the homogeneous part of the variation**.

- The difference field `M_Δ` obeys the same transport PDE as δM (it is the
  variation of M between the two branches):
  ```
  U^μ ∇_μ (M_Δ) + (∇·U)(M_Δ) = S_Δ ,
  ```
  where `S_Δ` is the source built from the branch-difference of δg, δU, δZ.
- The homogeneous part `M_{Δ,h}` is constant along each flow line. The
  turning-point condition `M_Δ(t_max) = 0` forces
  ```
  M_{Δ,h}(t_max) = - M_{Δ,p}(t_max) ,
  ```
  i.e. the homogeneous part is **uniquely determined** by the particular
  solution at the turning point. There is no remaining free constant.

Equivalently, in the physical (single-branch) language, the in-in prescription
selects the **retarded** solution of the transport equation for δM: the
integration constant is chosen so that δM has **no homogeneous (free) component**
at the initial time `t_0` (causal IC) and is fully determined by the source
`S` propagated forward from `t_0`. The advanced/free component is eliminated.

**Consequence:** After the in-in prescription, δM — and hence `E_{μν}` — is a
**unique, causal (retarded) functional** of δg. The ambiguity flagged in Phase
II (item 5) is **resolved** by the CTP boundary prescription.

> **IMPOSED:** The specific choice of IC (retarded, vanishing difference at the
> turning point) is a **manual boundary/initial-condition choice** — it is not
> derivable from the bulk action. This is the standard in-in choice and is
> physically motivated (it selects the retarded, causal response). But it is an
> **input**, not a consequence, of the action.

---

## 4. Causality of the resulting E_{μν}

**DERIVED:** With the in-in prescription, `E_{μν} = δM/δg^{μν}` is built from:
1. the **retarded** Green's function of `Box` (via δΦ, hence δZ), and
2. **retarded transport integrals** along the flow lines of `U` (via δM),
   with the homogeneous part fixed by the turning-point condition.

Both are **causal/retarded** operators. Therefore `E_{μν}` is a **causal
nonlocal tensor**: `E_{μν}(x)` depends on δg only within the **past** of `x`
(with respect to both the metric cone and the `U`-flow). There is no advanced
or acausal dependence. This is the desired causal structure.

**UNKNOWN:** Whether this causal `E_{μν}` is **covariantly conserved** on-shell
(`∇^μ E_{μν} = 0`, the Phase II constraint (C)) is **not yet verified**. This is
the next open question (Phase VII, field equations). Diffeomorphism invariance
of the action (which holds because M is defined by a diffeo-invariant transport
equation) **suggests** conservation on-shell, but for a nonlocal tensor the
proof requires interchanging divergences with retarded Green's functions and
transport integrals, which is nontrivial and is the most likely place for a
failure.

---

## 5. The first-order (transport) nature and the CTP subtlety

The M-sector is a **first-order** (in time) system: the transport equation
`∇_μ[√(-g) U^μ (M+F)] = 0` is first order in the time derivative of M. This is
different from a standard second-order field (like a scalar with a `Box` term).

**DERIVED / caveat:** The standard CTP/in-in doubling is designed for
**second-order** (Hamiltonian) systems, where the turning-point matching of both
the field and its velocity is natural. For a **first-order** transport system,
the "velocity" is not an independent variable — the field M itself is the
single canonical variable, and the turning-point condition `M_Δ(t_max)=0` is the
only (and sufficient) matching condition. The CTP construction is therefore
**well-defined** for the M-sector, but it is a **first-order** CTP, and the
usual "field + conjugate momentum" doubling reduces to just the field doubling.
This is consistent, but it means the M-sector has **half** the usual phase-space
structure: M is a **first-class** (transport) variable, not a second-order
dynamical degree of freedom. This feeds directly into the DOF count (Phase V).

---

## 6. Summary of Phase III results

| # | Result | Status |
|---|--------|--------|
| 1 | The in-in/CTP turning-point condition `M_Δ(t_max)=0` **uniquely fixes** the homogeneous (integration-constant) part of δM. | DERIVED (decisive) |
| 2 | After the prescription, δM and `E_{μν}` are **unique, causal (retarded)** functionals of δg. | DERIVED |
| 3 | The specific IC choice (retarded, vanishing difference at turning point) is an **input**, not derivable from the bulk action. | IMPOSED |
| 4 | `E_{μν}` is a **causal nonlocal tensor** (depends on δg only in the past of x). | DERIVED |
| 5 | Covariant conservation `∇^μ E_{μν}=0` on-shell is **not yet verified** (the key open question for Phase VII). | UNKNOWN |
| 6 | The M-sector is a **first-order** (transport) system; its CTP is a first-order CTP, and M is a transport (first-class) variable, not a second-order DOF. | DERIVED |

**Phase III verdict:** The causal prescription **resolves the integration-
constant ambiguity** of Phase II and makes `E_{μν}` a unique, causal, nonlocal
tensor. The remaining open question is whether this causal `E_{μν}` satisfies
the conservation constraint `∇^μ E_{μν} = 0` on-shell. That is the crux that
Phases IV–VII must settle.

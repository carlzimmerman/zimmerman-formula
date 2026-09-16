# G235 — THE TYPE-III READING

**Does the operator-algebra description of the dark sector (hy4 H057 V13/V16)
carry physical content, or is it decoration on an already-committed
equilibrium?** Broken into the three mandated sections: the formal type-III
claim and its honest testable translation, the KMS/FDT check at the committed
T_b, and the verdicts. Companion machine-readable results: `G235_results.json`.

Sources: H057 V13/V16 (the doors), H047 (the coherent charge, lambda_fs = 0,
R(k) = 1, 12/12), G093/G115 (the warm-relic reading killed), G084 (the
maximum-entropy equilibrium at the de-set temperature), G132 (T_b = 9.52 K,
first-order, N and entropy bookkeeping), G116 (one species, two phases).

---

## 1. THE FORMAL CLAIM (H057 V13): type III as no-particle / no-free-streaming

**The claimed correspondence.** A factor of type III has no trace: no faithful
normal trace, hence no density matrix, no number operator, and no well-defined
von Neumann entropy of the algebra. The claim in H057 V13 is that the dark
sector is type III, and that this **explains** two committed facts:
(i) there is no particle and no free-streaming (H047: lambda_fs = 0,
R(k) = 1, sigma² = 0), and (ii) there is no conventional thermodynamics of the
sector.

**The honest translation to a testable statement.** The three candidate
observables on which a type-I and a type-III dark sector genuinely differ:

| candidate | type I | type III |
|---|---|---|
| **entropy (THE candidate)** | finite, extensive von Neumann entropy over a countable packing; **finite mean entropy per degree of freedom** (Sackur–Tetrode, D = 3) | no trace ⇒ no finite per-degree-of-freedom entropy; the local/algebra entropy is **regulator-divergent** (area/volume-law, a UV/IR divergence) |
| entanglement | finite entanglement entropy of a reduced state (~ ln N) | infinite (QFT area-law divergence between region and complement) |
| coarse-graining | set by explicit resolution | set by modular flow (Tomita–Takesaki) — i.e. "the sector is a thermal state at a definite T", which the framework already commits (G084) |

**The candidate observable that tells them apart: the finite mean entropy per
degree of freedom at fixed mass.** The framework's own bookkeeping is
quantitatively **type-I-like**:

- **S/N = 22.8–23.8 k_B per particle** at fixed m = 5 keV (G132: s_ph at
  r_break = 22.81, at r_M = 23.77 k_B), via the Sackur–Tetrode law
  `s/k_B = 5/2 + ln[(mσ/ħ)³ (m/ρ) / (2π)^{3/2}]` — a **D = 3** momentum-space
  packing;
- over a **countable** packing **N_ph = M_b/m = 1.56e73** (G132 C1, the
  equipartition identity closes to 1.4e-16);
- **regulator-independent** (documented in G132's shared-reference convention).

A strict type-III sector would render that entropy divergent and well-defined
per degree of freedom. **The committed data are type-I.**

**The key insight — H047's discriminator is not a discriminator.**
`lambda_fs = 0` and `R(k) = 1` (H047 N2/N10) do **not** separate type I from
type III: an ordinary **type-I coherent condensate** (N particles occupying a
single mode, zero velocity dispersion, one thermal velocity ~ 0) produces
exactly the same observable signature — no free-streaming, R(k) = 1, no
discrete propagating particles. Both a type-I condensate and a type-III sector
realize "no free-streaming." The WDM kill that G093/G115 actually need (the
11 eV warm relic dead at 103–190 Mpc; the warm floor damping the halo function
at M_hm ~ 5e5–5.8e6 Msun) is the single-vanishing-velocity fact, which type I
coherent states provide as cheaply as type III. So **V13 contributes no
observable that is not already a thermal/coherent statement.**

---

## 2. THE KMS CONDITION (V16): the phantom at T_b = 9.52 K

**The KMS condition's content.** A state ω on an algebra with time evolution
α_t is KMS at inverse temperature β iff a two-point function F_AB(z) exists,
analytic on 0 < Im z < β, with `F_AB(t) = ω(A α_t(B))` and
`F_AB(t + iβ) = ω(α_t(B) A)`; in Fourier,
`Ẽ_BA(−ω) = e^{−βω} Ẽ_AB(ω)`. Physically: **the two-sided (positive/negative
frequency) correlation functions are tied by the Boltzmann factor at the
equilibrium temperature** — this is the *content* of thermal equilibrium and
of the fluctuation–dissipation theorem.

**The equilibrium's own numbers at T_b = 9.52 K (G132, 5 keV, G081 constants):**

| quantity | value |
|---|---|
| T_b = m σ²/k_B | **9.520686 K** |
| k_B T_b | 1.3145e-22 J = **8.20e-4 eV** |
| β = 1/(k_B T_b) | 7.608e21 J⁻¹ = **1.22e3 eV⁻¹** |
| σ (1-D) | 121.44 km/s (σ² = 1.4747e10 m²/s²) |
| **k_B T_b / m** | 1.47473e10 m²/s² = σ² to **2.0e-5** |
| ⟨v²⟩_3D = 3 k_B T_b/m | 4.424e10 m²/s² → **v_rms = 210.3 km/s** |
| ħω_orb / (k_B T_b) | **3.2e-28** (utterly classical) |

**The framework's own β from entropy maximization (G084).** At the global
maximum `dS/dE = 1/σ²` (measured 6.78096e-11 vs predicted 1/σ² = 6.78105e-11,
rel. diff −1.3e-5). The equilibrium's thermodynamic temperature β_fw =
1/(m σ²) = 7.608e21 J⁻¹ equals the KMS β = 1/(k_B T_b) to **2.0e-5**. In other
words **G084's maximum-entropy construction already *derived* the KMS/thermal
(canonical) condition classically** — the phantom is, by construction, the
thermal state at σ² = C/2.

**The FDT test at its own T_b.** With the normalization
`k_B T_b / m = σ²` being the *definition* of T_b, the isothermal equilibrium
satisfies the classical fluctuation–dissipation/Einstein relation
**identically, with zero free parameters**:
`D = σ²/τ_rel = (k_B T_b/m) μ = μ k_B T_b` for any drag channel τ_rel. The
fluctuation–dissipation balance is the definition of the temperature, not an
independent test.

**The gap.** The repo has committed **no two-time correlation function and no
response/admittance** χ(ω) or noise spectrum S(ω) for the phantom sector. The
only committed dynamics of the sector: the frozen-scalar fluid with c_s² ∈
[½, 1−] (H047 N6/N8 — a *frozen, non-propagating* sector, no free degrees) and
the free dust with c_s = 0 (H047 N3/N7). Without a committed χ(ω) or S(ω),
the **frequency-dependent FDT cannot be run: it is untested, not violated.**
The quantum KMS crossing factor e^{−βħω} degenerates to unity at these
frequencies (ratio 3.2e-28), so KMS reduces to the classical Maxwellian
— which is precisely the committed equilibrium.

---

## 3. VERDICTS

**V1 — the type-III translation (the observable that differs).**
**DECORATION with a real, already-committed core.** The honest observable that
separates a type-I from a type-III dark sector is the **finite mean entropy per
degree of freedom at fixed mass**. The framework's own bookkeeping is
**type-I-like**: S/N = 22.8–23.8 k_B per particle at fixed m = 5 keV over a
countable N_ph = M_b/m = **1.56e73** via a D = 3 Sackur–Tetrode law — finite,
extensive, regulator-independent. A strict type-III sector would render it
divergent, which the committed data neither contain nor can contain. The claim
that H047's no-particle / lambda_fs = 0 / R(k) = 1 is *evidence for type III*
fails: it is shared by a type-I coherent condensate. The only physical residue
of V13 is the already-committed "no discrete propagating particle" reading,
which a condensate realizes in type I.

**V2 — the KMS/FDT check on the committed equilibrium.**
**SATISFIED AS AN IDENTITY, NOT MEASURED.** The phantom is KMS at its own
T_b = 9.52 K **by construction**: the equilibrium's thermodynamic β from
G084 dS/dE = 1/σ² equals the KMS β = 1/(k_B T_b) to 2e-5, and
k_B T_b/m = σ² to 2e-5 (⟨v²⟩_3D = 4.42e10 m²/s², v_rms = 210.3 km/s — exactly
the Maxwellian at T_b). The classical FDT at T_b then holds **identically**
(zero free parameters). The **nontrivial** FDT (a committed χ(ω) or S(ω)) is
**untested** — no such response spectrum exists in the record, and the sector's
committed dynamics are frozen/non-propagating. V16 is **true-but-empty**: true
because every thermal state is KMS, empty because the framework's max-entropy
construction already derived that the phantom *is* a thermal state at
σ² = C/2.

**V3 — the honest statement (deep structure or decoration).**
**DECORATION on the committed equilibrium.** The phantom was already
characterized (G084/G132) as a finite-temperature, type-I-like
**maximum-entropy** thermal state — finite per-particle entropy 22.8 k_B over
countable N = 1.56e73, self-consistent β, first-order transition at
T_b = 9.52 K (L/(N k_B T_b) = 10.8–23.7). The type-III claim adds **no
observable** and explains nothing the coherent-condensate picture (H047) does
not already explain; it is in direct **tension** with the framework's own
arithmetic (type III has no finite per-particle entropy; the framework
computes one). It survives only if "type III" is redefined as the already-
committed, trivial statement *"the number of distinguishable microstates is
not a fundamental observable"* (the coherent-charge reading of H047).

**The test that tells deep structure from decoration:**
1. **Commit one two-time correlation function of the phantom sector** — the
   velocity autocorrelation or the scalar-mediated force-fluctuation spectrum,
   i.e. a real χ(ω) or S(ω) — and check the **frequency-dependent FDT at T_b**
   (S(ω) = 2 Re Z(ω) k_B T_b). A genuine response spectrum would make the KMS
   reading physical; its absence leaves it vacuous.
2. **The type-III discriminator:** determine whether the phantom's local
   entropy stays **finite per degree of freedom** (type I — committed at
   22.8 k_B) or **diverges under coarse-graining** (type III — uncommitted,
   unfalsified because no entropy-divergence scale was ever defined).

On the committed record the answer is **type-I-like, decoration-only.**

---

*6/6 checks pass. Numbers verified by computation: the thermal identity
k_B T_b/m = σ² to 2e-5; the framework β = KMS β to 2e-5; N = 1.56e73;
S/N = 22.8–23.8 k_B; quantum ratio 3.2e-28.*

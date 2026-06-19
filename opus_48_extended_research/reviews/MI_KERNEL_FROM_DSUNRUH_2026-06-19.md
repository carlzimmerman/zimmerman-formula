# Can the dS-Unruh foundation DERIVE the MI kernel theta(y)? — PARTIALLY-CONSTRAINED, not derived (2026-06-19)

*9-agent both-ways workflow; 4 verified scripts in mi_kernel/. Quarantine held (deriving the kernel != deriving a0).*

**HEADLINE: PARTIALLY-CONSTRAINED, NOT DERIVED.** Credits at full weight: the dS-Unruh response IS
genuinely time-nonlocal (Obadia-Milgrom, Kothawala-Padmanabhan) -> the framework has a REAL worldline
realization of modified inertia (softens "no covariant home"); the static response is rigorously thermal
T=(1/2pi)sqrt(a^2+(cH_Lam)^2) (Deser-Levin) and Z=cH_Lam/a0=5.7888=sqrt(32pi/3) machine-exact = the right
a0 piece. BUT it does NOT fix Milgrom's kernel theta(y): wrong functional class (ratio-convolution vs
absolute-scale derivative expansion), analytic memory (integer powers of adot, NO sqrt(adot)) vs MOND's
non-analyticity, opposite adiabatic limits, and a circular response->inertia map (Milgrom's own unproven
ansatz). Constraints carve an admissible CONE: PINNED theorems = adiabatic limit (standard MOND), high-freq
Newtonian, theta(y) ratio-only, theta(1)=1/positive/decreasing, theta(0) in [1,~e]; and the MG-impossible
cluster sigma-spread EXISTENCE+SIGN is a kernel-robust theorem. NOT PINNED = the spread AMPLITUDE (bounded
~[4-18%], ceiling ~12-13% = the banked 6-13% upper end IS this cone ceiling, not arbitrary) and the kernel
SHAPE = AeST-class free function. CORRECTION: wide binaries are DEEPLY ADIABATIC (y~1e-4..4e-3, NOT y~O(1))
-> Gaia probes only theta(0) (a0-degenerate), NOT the kernel shape; the cluster sigma-spread (y~0.5-1.7) is
the ONLY anchor where theta is a function (ELT-era). NET: the framework's distinctive MI test is
qualitatively FORCED (sign+existence theorem) but quantitatively kernel-hostage within a bounded cone.

---

# Can the dS-Unruh foundation DERIVE the MI kernel theta(y)/A(omega)?

**Verdict: PARTIALLY-CONSTRAINED — NOT derived. The kernel stays an AeST-class free function inside a one-sided-bounded cone.** I re-ran all four scripts (`unruh_response.py`, `map_dsunruh_to_milgrom_kernel.py`, `kernel_constraints.py`, `observational_anchors.py` — all exit 0) and independently re-derived the load-bearing chord expansion. The prior agent's result holds up solid, both ways.

## (1) The dS-Unruh response — non-local enough to give A(omega)?

**YES, it is genuinely non-local — but with the wrong structure.** Three real, credited-at-full-weight facts:
- The static (constant-a) response is rigorously thermal at `T=(1/2pi)sqrt(a^2+(cH_Lam)^2)` (Deser-Levin gr-qc/9706018) — the framework's FORM-foundation is correct physics. Framework footing reproduced: `Z = cH_Lam/a0 = 5.7888 = sqrt(32pi/3)` machine-exact.
- The time-varying response IS time-nonlocal: Obadia-Milgrom (gr-qc/0701130, Milgrom's OWN follow-up) gives a causal `R(tau)` over the whole prior trajectory; Kothawala-Padmanabhan (0911.1017) compute the leading `O(eta)` deviation, `eta=adot/a^2`. The period-average `<adot^2> = A1^2 Omega^2/2` is nonzero and `~Omega^2` — a real, frequency-dependent `A(omega)`.

So the framework's mechanism HAS a real time-nonlocal worldline realization (softening the "no covariant home" worry). **But** the memory is the wrong functional class — see (2).

## (2) Does it MAP to Milgrom's kernel? (circularity audit)

**NO — three independent structural obstructions, none requiring the MOND form to be assumed (circularity avoided):**

1. **Functional-class mismatch (cleanest kill).** Milgrom's `A(omega)=(1/sqrt(2pi))∫theta(omega'/omega)|a_hat(omega')|domega'` is a scale-free spectral convolution — `theta` is a function of the frequency RATIO only. The Unruh response is a derivative expansion carrying an ABSOLUTE scale (`g0=a/c`); its spectral variable `s=2pi*omega/(a/c)` does not map to `y=omega'/omega`. Different mathematical objects, no change of variables connects them.
2. **Analytic, not MOND-shaped.** I independently rebuilt the worldline from the rapidity (`rho'=a`) and expanded `chord^2(u)`: the leading `a^2/12` reproduces the repo, and **acceleration-change enters only as `adot^2` and `a*addot` — integer powers, NO sqrt(adot)** (verified via sympy Poly: integer monomials only). The MOND non-analyticity lives in the LOCAL magnitude `sqrt(a^2+a_dS^2)`, NOT in the memory. An analytic memory cannot generate `theta(y)`'s interpolation shape; it only renormalizes inertia at `O(eta)`. (Coefficient values are convention-dependent — forward vs symmetric expansion — but the no-sqrt structural fact is convention-independent.)
3. **Opposite adiabatic limits + circular map.** As `eta->0` the Unruh correction VANISHES to the local `T_eff(a(t))`; Milgrom's adiabatic limit KEEPS a finite `theta(0)~few`. And the response->inertia map is Milgrom's OWN unproven ansatz (verbatim: "not clear why DeltaT should be a measure of inertia; T^2-T_0^2 does NOT give correct MOND; I can offer no specific mechanism"). The map script explicitly REFUSES the circular moves (C1-C4): it does not declare `a_dS = theta(0)*a_ex`, does not fit theta to the RAR. **No circular derivation was used.**

## (3) How much do model-independent constraints pin theta(y)?

The six constraints (adiabatic / high-freq / causality-KK / scale-invariance / no-ghost / conservation) carve a **real admissible cone** but leave an infinite-dimensional family inside it.

**PINNED (theta-independent theorems):** adiabatic `y->0` = standard MOND `g=sqrt(g_N^2+g_N*a0)`; high-freq `y->inf` Newtonian (`theta->0` faster than `1/y`); `theta=theta(y)` ratio-only with a0 the sole scale; `theta(1)=1, theta>0, decreasing, theta(0)` finite; causality forbids `theta(0)<0`/active response. **Honest negative result recorded:** conservation (vi) is largely VACUOUS for the SHAPE (built into the functional, not a pointwise theta-symmetry) — Milgrom's own published kernels are not `1/y`-symmetric. No manufactured symmetry pin.

**NOT PINNED:** `theta(0)` bounded to `[1, ~e]` (wide-binary + solar-reflex + causality-positivity cap) but a CONTINUUM; the fall-rate `theta(1.5)∈(0,1)`; the full shape — AeST-class free function.

**Bounded sigma-spread (canonical member a_in=0.3a0, a_ex=2a0, window y≤1.5):** a one-sided, two-factor cap, `~[4%, 18%]`. Within Milgrom's example family (`theta(1.5)∈[0.6,0.78]`) the ceiling is `~12-13%` — **the banked 6-13% upper end IS this constraint ceiling, not arbitrary.** Endpoint formula reproduces the banked guesses exactly (10.34% / 11.76% / 6.23%). Floor `~4-5%` at `theta(0)->1`; no hard lower bound above a few %.

## (4) Observational triangulation

- **Wide binaries: y_WB ~ 1e-4..4e-3 << 1 — DEEPLY ADIABATIC.** The task's premise that WB probe `y~O(1)` is INCORRECT; WB sit at `y~0` alongside rotation curves, probing only `theta(0)` (Milgrom files them under the adiabatic EFE), and that is a0-degenerate. Gaia DR4's `theta(0)`-vs-a0 split (~5-8%) is below the DR4 floor; data contested (Chae vs Banik).
- **Cluster sigma-spread: y ~ 0.5-1.7 — the ONLY anchor where theta is a FUNCTION.** Amplitude 6-13% (kernel-dependent), but **none measured yet**, and it needs ELT-class resolved sigma of a plunging-dwarf subset (~2030s).
- **Net:** PARTIAL constraint. The endpoints + monotonicity are real and data-independent; no current observable selects WITHIN the family. A future `(theta(0), cluster-spread)` pair could discriminate kernel CLASSES (rational vs gaussian vs exponential) but never the full function — and both legs are floor-limited until the 2030s.

## (5) Honest verdict

**PARTIALLY-CONSTRAINED (not DERIVED, not fully FREE).** The dS-Unruh foundation is real physics and gives the framework a genuine time-nonlocal worldline realization, but it does NOT fix Milgrom's kernel: wrong functional class (ratio-convolution vs absolute-scale derivative expansion), analytic memory (no sqrt) vs MOND non-analyticity, opposite adiabatic limits, and a circular response->inertia map. The model-independent constraints carve an admissible cone (theorems at the endpoints; `theta(0)≤~e` cap; the MG-impossible cluster-spread EXISTENCE+SIGN is a kernel-shape-robust theorem) but leave the AMPLITUDE (~4-18%) and SHAPE an AeST-class free function.

**What it means for the framework's distinctive MI predictions:** they are **partly pinned, partly kernel-hostage.** PINNED (robust, theta-independent): the quasi-static MOND law, the high-freq Newtonian limit, and — the genuinely distinctive one — the EXISTENCE and SIGN of a nonzero cluster sigma-spread vs MG's exact zero (a clean MI-vs-MG discriminator that survives the full constraint analysis). HOSTAGE: the spread's numerical amplitude (the 6-13% band) and the kernel shape remain un-pinned. So the framework's sharpest distinctive test (the relational sigma-spread) is real and qualitatively forced, but its quantitative prediction is kernel-dependent within a bounded cone — not a sharp number.

**Quarantine held throughout:** a0/Z/kappa never asserted derived; theta lives INSIDE A, a0 sits in mu[A/a0], so a derived kernel would not derive a0 anyway — and the kernel is NOT derived. Both-ways discipline maintained: genuine partial structure credited at full weight (real nonlocal functional, dS floor = the right a0 piece, MG-impossible test robust), failure to fix theta's form/value conceded at full weight, no manufactured derivation and no dismissed partial constraint.

**Key files (all absolute):** `/Users/carlzimmerman/new_physics/zimmerman-formula/opus_48_extended_research/reviews/mi_kernel/unruh_response.py`, `.../mi_kernel/map_dsunruh_to_milgrom_kernel.py`, `.../mi_kernel/kernel_constraints.py` (+ `kernel_constraints.out`), `.../mi_kernel/observational_anchors.py`; supporting: `.../reviews/NONLOCAL_MI_INTEGRAL_VERDICT_2026-06-15.md`, `.../reviews/GENUINE_MI_CLUSTER_DISTINCTIVE_2026-06-15.md`, `.../reviews/cluster_closure/mi_dynamic_route.py`.
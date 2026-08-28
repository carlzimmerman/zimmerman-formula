# FC-FINAL 4-AC Type-II MMG — SETUP / derivation-scoping

**Task:** lay out the 4-auxiliary-constraint (Type-II MMG) structure faithfully, embed the
frozen MOND kernel `mu_10`, and derive the one load-bearing thing: **which metric potential(s)
the MOND modification sources in the static weak field** — the lapse potential `Psi` (dynamics),
the spatial curvature potential `Phi` (lensing), or both.

**Certificate:** `fc4ac_setup_scaffold.py` → `ALL BOOLEAN CHECKS PASS`, exit 0
(sympy 1.13.1, py 3.13.9; output frozen in `fc4ac_setup_scaffold.out`).
This is a **scoping** document: it states what is DERIVED, what is EXTERNAL-INPUT, and what is
OPEN and hands the decider to the next task. It does **not** claim closure and does **not**
assert `Phi=Psi` or `Phi!=Psi` — it computes the map from the free constraint choice to the slip.

Honesty labels: `THEOREM | DERIVATION | COMPUTATION | EXTERNAL-INPUT | MODEL-ASSUMPTION | OPEN | FAILED`.

---

## 1. The 4-AC Type-II structure (faithful)

**EXTERNAL-INPUT** (De Felice–Mukohyama–Pookkillath, arXiv 2302.02090, "Type-II" minimally-modified
gravity = 4 auxiliary constraints permitting consistent matter coupling from the outset;
Iyonaga–Kobayashi, arXiv 2109.10615 / PRD 104.124020, spatially-covariant MMG with a non-dynamical
scalar ⇒ exactly 2 tensor DOF, `gamma_PPN=1`, `c_T=1`):

Phase space `(gamma_ij, pi^ij ; N, pi_N ; N^i, pi_i)`, dim `12 + 2 + 6 = 20`.
GR reaches 2 DOF with **four first-class** constraints `H_perp + H_i` (+ their spatial-diffeo gauge).
Type-II keeps 2 DOF **without `H_perp`** by adding **four second-class** auxiliary constraints in the
scalar sector, `{S_1, S_2, S_3, S_4}`, whose `4×4` Dirac block `Delta_AB = {S_A, S_B}` is
**non-degenerate** (invertible), and retaining only the first-class spatial-diffeo pair `(pi_i, H_i)`.

Carl's target set (the object under attack):

| Constraint | Content | Sector fixed (static) |
|---|---|---|
| `S_1 = pi_N` | lapse momentum (primary) | `pi_N = 0` |
| `S_2 = C_M^(10)` | **the MOND constraint** (kernel `mu_10`) | one scalar potential |
| `S_3 = C_q` | conformal-factor constraint | the other scalar potential |
| `S_4 = C_p` | conjugate/momentum constraint (`p = pi/sqrt(gamma)`) | trace-`K` momentum → `0` |

**DERIVATION (arithmetic, cert Part 0):** `N_grav = (20 − 2·6 − 4)/2 = 2`. Two tensor gravitons,
`N_scalar = N_vector = 0`. The four second-class constraints remove the lapse pair `(N, pi_N)` and the
conformal scalar pair `(q, p_q)`.

**Committed anchor:** the baseline block has `Pf(Delta) = L_N·K` (`openai_push/final_closure/scripts/
03_dirac_matrix.py`), invertible off the measure-zero `L_N=0 ∧ K=0` locus. **OPEN caveat (committed,
carried forward):** the `{D²q, H_i}` bracket carries `(1/3)D²(D·xi) ≠ 0`; the first-class status of
`H_i` after adding `S_2` was asserted, not computed, in the certified suite — if the E-mode is
physical the 2-DOF count itself is not yet secured (`ppn_mmg_gate_2026.out` Part 0.6).

---

## 2. Where the kernel lives, and the weak-field dictionary

**FROZEN kernel (unchanged):** `mu_10(y) = y/(1+y^10)^(1/10)`, `y = (c²/a0)|D(field)|`,
`mu_10>0`, `mu_10 + y·mu_10' > 0` (strict ellipticity on `y>0`).

**DERIVATION (cert Part 1).** In the static weak field
(`g_00 = −N²c²`, `N = 1 + Psi/c²`; `g_ij = (1−2Phi/c²)δ_ij`):

- `q = (1/6) ln det gamma = −Phi/c² + O(c⁻⁴)` — **the conformal factor `q` IS the curvature potential `Phi`.**
- `ln N = +Psi/c² + O(c⁻⁴)` — **the lapse log `ln N` IS the dynamical potential `Psi`.**

**This is the entire pivot.** `mu_10` is a **one-field elliptic operator**: it sources whichever of
`{Phi, Psi}` its carrier field is. The task's own phrasing — *"`y = (c²/a0)|D q|` **or** `|D ln N|`
per the embedding"* — is exactly the choice of which potential the MOND modification hits.

---

## 3. THE DECIDER — which potential(s) the modification sources

### 3.1 The lapse `Psi` is sourced (DERIVATION, cert Part 2)

With `C_M^(10) = D_i[c² mu_10(y) D^i ln N] − 4πG ρ`, `y=(c²/a0)|D ln N|`, the `c²` factors cancel and
the constraint reduces **exactly** to AQUAL for `Psi`:
```
D_i[ mu_10(|DPsi|/a0) D^i Psi ] = 4πG ρ ,   v_inf^4 = G M a0 ,   slow matter a = −grad Psi .
```
(sympy residual `= 0`; consistent with committed `02_newtonian_limit.py`.) The kernel has **no
`q`-dependence** — so, on its own, **`C_M` sources `Psi` ONLY.** Rotation curves are correct and MOND.

### 3.2 The curvature `Phi` is sourced by `C_q` — and that is a free choice (DERIVATION, cert Part 3)

In the static weak field the four constraints split cleanly: `S_1=pi_N` and `S_4=C_p` kill the
(vanishing) momenta; `S_2=C_M` fixes `Psi`; **`S_3=C_q` fixes `Phi`.** The MOND reach into `Phi`
is therefore whatever `C_q` is built to be. Enumerating the admissible `C_q`:

| # | `C_q` | `Phi` solves | slip `gamma_PPN=Phi/Psi` | status |
|---|---|---|---|---|
| 3a | `D²q` (source-free) | `Phi=0` | `0` at **all** accel. | **LAPSE-ONLY** — the old chassis. `FC_NO_GO` THEOREM. |
| 3b | `D²q − 4πG ρ` (Newton source) | Newtonian `Phi` | `μ(y)`: `≈1` solar, `→0` galactic | regime-split; **fails galaxy lensing** (§4) |
| 3c | `D²(q + ln N)` (**the lock**) | `Phi=Psi` | `1` everywhere | **BOTH** — uncertified; new liabilities (§5) |
| 3d | `D_i[μ D^i q] − 4πG ρ` (matched MOND) | `Phi=Psi=`MOND | `1` everywhere | **BOTH** — uncertified; distinct Dirac block |

All four rows carry sympy certificates. The point: **the answer to "which potentials" is not fixed by
the MOND requirement alone — it is set by `C_q`, which is a design degree of freedom of the 4-AC
structure.** The default (source-free) reproduces the `gamma_PPN=0` disaster; the escape lives in 3c/3d.

---

## 4. Sharpening the no-go's "named escape": the Newtonian-source slip **is `mu(y)`** (DERIVATION, cert Part 4)

`FC_NO_GO.md` names one escape: a `rho`-sourced `q`-constraint `D²q ~ +4πG ρ` (row 3b) *"WOULD source
Phi and restore gamma_PPN=1."* **This is only half true, and the correction matters.**

**THEOREM (spherical, exact by Gauss).** With `Psi` from AQUAL (`mu(y) Psi' = g_N`) and `Phi` from
Newtonian Poisson (`Phi' = g_N`), the gradient slip is
```
Phi'/Psi'  =  g_N / g_MOND  =  mu_10(y) ,     lensing efficiency (Phi'+Psi')/(2 Psi') = (mu_10(y)+1)/2 .
```
- **Newtonian regime** (`y≫1`, `mu→1`): slip `→1`, efficiency `→1` — **fixes Cassini / solar-system γ.**
- **Deep-MOND regime** (`y≪1`, `mu→0`): slip `→0`, efficiency `→1/2` — **the SAME ~20σ M24-KiDS deficit
  as the source-free chassis.**

Numeric point-mass (`M=6×10¹⁰ M_sun`, `a0=9.36e-11`, cert Part 4): slip is `1.000` at `0.1–5 kpc`,
falls to `0.47 / 0.19 / 0.094` at `20 / 50 / 100 kpc` — i.e. it collapses precisely across the
galaxy-lensing radii where the KiDS RAR lives. **So reintroducing `H_perp` with a Newtonian source is
NOT a lensing fix**; it repairs the solar-system end and leaves the galactic end essentially unrepaired.
Only rows 3c/3d (slip `=1` at all `y`) give correct lensing in **both** regimes.

---

## 5. Two contrasts, and the price of the escape

**(a) OLD source-free chassis (`Phi=0`, `gamma_PPN=0`).** `openai_push/final_closure/
gate_lensing_weakfield_derivation.py` derives it twice: the deleted `H_perp` *is* the equation that
sourced `Phi`; with `S_2=D²q` source-free, `q≡0 ⇒ Phi≡0`, light sees half the potential, `M24 KiDS
Δχ² ≈ +403..+498 (~20σ)`, Cassini `~43,000σ`. This is the **LAPSE-ONLY** endpoint the escape must beat.

**(b) Iyonaga–Kobayashi / DFMP locally-trivial (`Phi=Psi` trivially).** Their Type-II constructions get
`gamma_PPN=1` and `c_T=1` — but by **recovering GR locally** (no modification to asymptotically-flat
black holes / the solar system; the modification is effectively cosmological). Their `Phi=Psi` is the
GR one, sourced by `rho` through the retained effective Hamiltonian structure — **there is no `a0`, no
flat rotation curves.** MOND is exactly the opposite requirement: it **must** modify the local galactic
weak field at `a0`. The whole difficulty is grafting a *local elliptic* MOND modification onto the
DFMP scaffold and still landing `gamma_PPN=1`.

**The mechanism by which a non-trivial MOND modification could still give `Phi=Psi`** (rows 3c/3d):
a fourth constraint `C_q` that **locks** `q` to `−ln N` (⇒ `Phi=Psi`) or carries a **MOND-matched
source** on `q`. Committed evidence that this is not empty:
`openai_push/final_closure/gate_fork_S2prime_matter_mondlaw.py` computes the lock `S_2'=D²(q+lnN)` and
finds

- **WIN:** `Phi=Psi` exactly ⇒ `gamma_PPN=1`; and the Dirac block stays invertible,
  `Pf(Delta) = L_N K − E c_M ≠ 0` on the generic branch — the 2-DOF count **plausibly survives**.
- **PRICE (all committed, none cosmetic):**
  1. **OPEN re-certification.** `{pi_N, S_2'} = −D²(·/N) ≠ 0` changes the block; Dirac Gates 3/6/7/8
     (structure, rank, count, no-tertiary) must be re-run — the certificate does **not** transfer.
  2. **New repulsive force.** The lock turns the extra scalar channel `X` into a *hill*: net matter
     force `g = g_Psi[1 − (1−mu)/M_par]`, **repulsive below `y_crit ≈ 1/3`** (mu_10) — a brand-new
     galactic liability introduced by the very fix (`gate_fork` Parts C/D).
  3. **`alpha_3` untouched (§6).**

---

## 6. The parallel obstruction: `alpha_3` is orthogonal to the `Phi/q` sector (EXTERNAL-INPUT, cert Part 5)

**COMPUTATION (committed `ppn_mmg_gate_2026.out` 1.4 / 4.4).** The coefficient of the kinetic-energy
potential `Phi_1` in `g_00` is `1` (MMG) vs `4` (GR): the **elliptic** `C_M` responds
**instantaneously** to the source's kinetic energy ⇒ `alpha_3 = −1` (`2.5×10¹⁹×` the pulsar bound; also
= momentum non-conservation). `alpha_3` is a functional of `C_M` (the `g_00`/lapse sector), with
`d(alpha_3)/d(C_q multiplier) = 0`. **Fixing `Phi` via `C_q` (rows 3c/3d) does not move `alpha_3`.**

Note `alpha_1 = +4` is *linked* to `gamma_PPN`: it is booked from the `g_0i` sector read through a
`gamma=0` dictionary, so restoring `gamma_PPN=1` plausibly relaxes `alpha_1` too. `alpha_3` is **not**
so linked — it is the sharp, separate, `g_00`-sector obstruction. `alpha_3=0` needs either a **retarded**
(non-instantaneous) lapse response, or the DFMP "consistent matter coupling" 4th constraint engineered
to cancel the instantaneous piece — **OPEN**, and the real content of the next task.

---

## 7. Scoping verdict

**Which potential(s) does the MOND modification source? → UNDETERMINED-needs-derivation.**

- **DERIVED:** `mu_10` is a one-field elliptic operator; in `C_M` on `ln N` it **sources the lapse `Psi`**
  (correct dynamics). The curvature `Phi` is fixed by a *separate* constraint `C_q`.
- **DERIVED:** the "which potentials" answer is **set by `C_q`, a free design choice**, not by MOND:
  source-free → `Phi=0` (LAPSE-ONLY, `gamma_PPN=0`); Newton-source → slip `mu(y)` (fixes solar, fails
  galaxies); lock or matched-MOND → `Phi=Psi` (`gamma_PPN=1` everywhere).
- **Therefore the structure ADMITS both `Phi=Psi` and `Phi≠Psi`.** We assert neither. The MOND-specific
  obstruction is *not* an automatic LAPSE-ONLY verdict (unlike the old source-free chassis); it has a
  **named, partially-verified escape** (the lock keeps the Dirac determinant nonzero) — **at a price**:
  (i) a full 2-DOF Dirac re-certification for the changed block `{pi_N, C_q}≠0` (OPEN);
  (ii) a new repulsive matter force below `y_crit≈1/3` that the lock introduces (COMMITTED liability);
  (iii) the sector-orthogonal `alpha_3=−1` that no `C_q` choice repairs (COMMITTED, needs the DFMP
  consistent-matter-coupling machinery to even attempt).

**The DECIDER for the next task (sharp, three-part):** does there exist a single `C_q` (equivalently, a
single choice among the 4 auxiliary constraints carrying the matter density into the `q`/curvature
sector) that **simultaneously** (1) yields `Phi=Psi` at all accelerations, (2) certifies at **exactly**
2 DOF through the full Dirac program with the `{D²q,H_i}` E-mode resolved, and (3) leaves neither a
repulsive galactic force nor `alpha_3≠0`? If the 4-AC algebra forbids (1)∧(2)∧(3) jointly, that is the
MOND-specific NO-GO; if it permits them, FC-FINAL becomes a genuine `gamma_PPN=1` relativistic-MOND
candidate. **Nothing in the committed record yet exhibits such a `C_q`; nothing yet forbids it.**

---

### Provenance
- **This session:** `fc4ac_setup_scaffold.py` (+ `.out`) — the C_q→Phi→slip map, the `slip=mu(y)`
  theorem, the DOF arithmetic, the `alpha_3` orthogonality. All boolean certs pass, exit 0.
- **Committed cross-refs:** `03_dirac_matrix.py` (Pf=L_N·K), `02_newtonian_limit.py` (AQUAL),
  `gate_lensing_weakfield_derivation.py` (source-free `gamma_PPN=0`), `ppn_mmg_gate_2026.py`
  (`alpha_3=−1`, kernel-blind), `gate_fork_S2prime_matter_mondlaw.py` (the lock: `Pf=L_N K−E c_M`,
  repulsive-force liability), `fc_no_go_Hperp_unsources_Phi.py` (source-free THEOREM + named escape),
  `fc_C_laplacian_orthogonality_certificate.py` (k=0 vs k≠0 disjoint support).
- **EXTERNAL:** DFMP arXiv 2302.02090 (Type-II, 4-AC, consistent matter coupling); Iyonaga–Kobayashi
  arXiv 2109.10615 (2-DOF spatially-covariant MMG, `gamma_PPN=1` **with GR recovered locally**).
- **Labelled ASSUMED throughout:** `a0² = κ²c²Gρ_Λ`, `a0(z)~√ρ_DE`, `κ=1/2`, `Z~21` — phenomenological
  input, never derived.

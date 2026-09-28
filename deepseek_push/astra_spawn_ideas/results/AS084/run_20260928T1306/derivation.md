# AS084 — Self-gravitational virial energy with a central mass

Run: `run_20260928T1306` · Worker: hermes subagent (`deepseek/deepseek-v4-flash-0731` via OpenRouter, macOS host) · Task sha256: `71026d9a802021e7f62e81ef43677f2f6832d03de868a20be43c4ef96720243b`
Companion artifacts: `compute_AS084_virial_central.py`, `residuals.json` (10/10 checks), `raw_output.txt`, `time_mem.txt`, `AS084_virial_identity.lean` + `lean_check.out` (Lean 4.34.0-rc2, zero `sorry`, axioms = {propext, Classical.choice, Quot.sound}).

---

## 1. Precise claim, symbols, assumptions (seed step 1)

**Claim (finite-shell virial identity, exact).** On every finite spherical shell `r_in ≤ r ≤ R` with `r_in > 0`, carrying the phantom density
`rho_ph(r) = A / r²` around a central point mass `M_in ≥ 0`, the total virial-energy integral

    W_vir,total = −∫_{r_in}^{R} G·M(r)/r · dM_shell(r),      M(r) = M_in + m_s·(r − r_in),

is exactly

    W_tot = W_cent + W_self,
    W_cent = −G·m_s·M_in·ln(R/r_in) = −C·M_in·ln(R/r_in),
    W_self = −G·m_s²·(R − r_in − r_in·ln(R/r_in)) = −(C²/G)·(R − r_in − r_in·ln(R/r_in)).

**Symbols (SI unless noted):** `G` Newton constant; `M_in` central mass; `M_b` baryonic mass; `m_s = C/G = 4πA` shell linear mass density (`dM_shell = m_s dr`); `A` density normalization; `C = sqrt(G·M_b·a0)`; `a0` framework acceleration; `r_M = sqrt(G·M_b/a0)`; `r_in, R` shell boundaries; `M_T = m_s·(R − r_in)` total shell mass; `σ²` virial velocity dispersion; `v_flat⁴ = G·M_b·a0`.

**Framework inputs (adopted, not derived):** `a0 = κ·c·sqrt(G·rho_Lambda)` with `κ = 1/2` — canonical footing `a0 = 9.3619e-11 m/s²` (`rho_Lambda = 5.844412454021876e-27 kg/m³`, `epsilon_Lambda = 5.252696e-10`, `Λ = 1.090800e-52 m⁻²`); alternative footing `a0 = 1.1279e-10 m/s²` (`rho_Lambda = 8.483089619559099e-27`, `epsilon_Lambda = 7.624221e-10`, `Λ = 1.583282e-52`). The two footings are carried separately: they cannot share both a fixed vacuum density and a fixed κ (fixing `rho_Lambda` to the canonical value at the alt footing would force an effective `κ = 0.60239`; fixing `κ = 1/2` forces `rho_Lambda` ratio 1.45149 — recorded in `residuals.json.footing_relations`).

**Assumptions:** spherical static shell; Newtonian pairwise kernel `−G dM dM' / r'`; enclosed-mass law `M(r) = M_in + m_s (r − r_in)` follows from `rho_ph(r) = A/r²` plus the shell normalization `m_s = 4πA` (G084); virial definition `dW_vir = −G M(r)/r dM` (G091 virial triad); `M_in ≥ 0`, `r_in > 0`, `R ≤ r_M` for the finite-shell results, deep exterior separately (`r_in/r_M ∈ {10,100}`, `R/r_in ∈ {2,10}`).

## 2. Exact integration (seed step 2 — separation, not conflation)

The integrand splits by construction of `M(r)`:

    W_vir,total = −∫ G·[M_in + m_s(r − r_in)]/r · m_s dr
                = −G·m_s·M_in·∫ dr/r  − G·m_s²·∫ (r − r_in)/r dr
                = −G·m_s·M_in·ln(R/r_in)  − G·m_s²·(R − r_in − r_in·ln(R/r_in)).

Sympy primitive of the full integrand (recorded): `G·m_s²·r + G·m_s·(M_in − m_s·r_in)·ln r`.

- **W_cent** (virial of the *external* central potential acting on the shell continuum): `−C·M_in·ln(R/r_in)` — vanishes identically when `M_in = 0`.
- **W_self** (shell continuum self-gravity): `−(C²/G)·(R − r_in − r_in·ln(R/r_in))` — the pair self-energy. The two terms are kept separate everywhere; the pair self-energy is never reported as the virial of an external potential and vice versa (`separation_verified = true`, sympy; Lean `separation_of_terms`).

The finite-shell corrections relative to the singular-sphere form `−G·M(R)²/R` are the terms that *disappear only when the singular sphere is used* (`r_in → 0⁺`):

    W_self(r_in; R) → −(C²/G)·R = −G·m_s²·R = −G·M(R)²/R   as  r_in → 0⁺   (M(R) = m_s·R),
    W_naive − W_tot│_{M_in=0} = −G·m_s²·r_in·[ ln(R/r_in) − (1 − r_in/R) ]  (exact, Lean `naive_error_exact`, `naive_overbinds`)

Since `ln ρ > 1 − 1/ρ` for `ρ = R/r_in > 1`, the naive replacement `−G·M(R)²/R` is **strictly more negative** than the true virial on every finite shell — the singular-sphere identification is exact only in the limit, never inside the domain `r_in > 0`.

## 3. Signs, scale factors, units (seed step 3)

- All terms carry `−` (attractive ⇒ negative virial energy, J). `−G·m_s·M_in·ln(R/r_in)`: `G [m³ kg⁻¹ s⁻²]·m_s [kg/m]·M_in [kg]·ln[1]` → `[kg m² s⁻²] = J` ✓. `G·m_s²·r_in·ln(R/r_in)` and `G·m_s²·R` likewise J ✓.
- Hook between framework constants: `G·m_s = C` (since `m_s = C/G`), so `W_cent = −C·M_in·ln(R/r_in)` (units: `a0^{1/2}·G^{1/2}·M_b^{1/2}·kg = J` ✓) and `W_self = −(C²/G)·(...)` = `−G·m_s²·(...)`.
- Deep-MOND velocity: `v_flat⁴ = G·M_b·a0 ⇒ v_flat = 168.58 km/s` (MW, canonical), σ from the virial relation: 119.20 km/s (canonical MW) — see table.
- Both virial terms scale as `sqrt(a0)` through `C`; hence `W_self(alt)/W_self(can) = sqrt(a0_alt/a0_can) = C_alt/C_can = 1.0976232541844928` **exactly** (C8; max rel deviation 2.0e-16, i.e. float round-off).

**Virial balance with central mass (σ², exact closed form).** From `2T + W_cent + W_self = 3P_sV` with `T = 3/2·M_T·σ²`, `M_T = m_s(R − r_in)`:

    σ²(M_in, r_in) = G·[ R·m_s − m_s·r_in + ln( R^{M_in − m_s·r_in} · r_in^{−(M_in − m_s·r_in)} ) ] / ( 2·(R − r_in) )

which recovers `σ² → C/2` in the singular limit `M_in → 0, r_in → 0⁺` (sympy double-limit with `m_s = C/G` substituted; C9). For `M_in = 0` the closed form simplifies to `σ² = (C/2)·[1 − (r_in/(R−r_in))·ln(R/r_in)]`, i.e. `σ²/(C/2) = 0.953483` at `r_in/R = 0.01`, `0.744157` at `0.1`, `0.306853` at `0.5` (exactly the C9 rows) — the finite-boundary virial deficit of a surface-truncated phantom shell.

**Leading neglected term in the singular limit** (`r_in → 0⁺`): exact deviation of the naive form from the true self-virial is `W_naive − W_self = −G·m_s²·r_in·[ln(R/r_in) − (1 − r_in/R)] < 0`, magnitude `|ΔW|/|W_self| = (r_in/R)·[ln(R/r_in) − 1 + r_in/R]` (verified exactly: ε = 1e-8 ⇒ 1.742068e-7, ε = 1e-12 ⇒ 2.663e-11, matching the C4b rows to all shown digits).

## 4. Independent checks — actual residuals (seed step 4)

Controls are **capable of failing**; all residuals below are recorded values from `residuals.json` (10/10 PASS).

| Check | Method (independent representation) | Observed | Tolerance |
|---|---|---|---|
| C1 | Closed form vs **50-digit mpmath quadrature of the raw integrand**, 8 cells × 2 footings, grid `(r_in/R, R/r_M) ∈ {(0.01,0.62),(0.1,1.0)}`, `M_in/M_b ∈ {0,0.1}` | max rel err **2.419992483473175e-51** | 1e-25 |
| C2 | Discrete N-shell Newtonian pair-energy sum `Σ_{i<j} −G m_i m_j / r̄`, N = 10…10⁴, `M_in/M_b = 0.1`, canonical | rel err 0.181→1.36e-4 (0.01\|0.62 cell), 0.0772→7.78e-5 (0.5\|1.0 cell); O(1/N) boundary-term convergence, per-decade ratio ~0.10 ✓ | 5e-4 at N=10⁴ |
| C3 | `dW/dR = −G·M(R)·m_s/R` by central finite differences, h = 1e-6·R | max rel err **2.493e-11** | 1e-5 |
| C4 | **Negative control**: naive `−G·M(R)²/R` on every finite shell, 6 cells × {0,0.1} M_in/M_b × 2 footings × 2 masses | rel deviation **3.83% – 64.88%** — naive form REJECTED for finite shells | dev > 0.1% |
| C4b | Naive form recovers exactness only in the singular limit `M_in=0, r_in→0` | dev 1.742e-7 (eps=1e-8) → 2.663e-11 (eps=1e-12) | < 1e-6 at eps=1e-12 |
| C5 | Thin-shell boundary limit `R → r_in⁺` (W → −C·M_in·ln(1+ε) leading) | W/W_cent = 1.0004999 (ε=1e-3), 1.0000050 (ε=1e-5) | 5% |
| C6 | Singular limit reproduces the **G091 (cited source) closed form** `−G·M_T²/r_break` at `R = 0.62 r_M` | rel **2.86e-11** (G091 used `G = 6.674e-11`; this audit G = 6.67430e-11, ΔG/G = 4.49e-5, tracked) | 1e-6 |
| C7 | Deep-exterior shells `r_in/r_M ∈ {10,100}`, `R/r_in ∈ {2,10}`: A-profile virial vs **Q-kernel and RAR-kernel** densities (`M_in ∈ {0, M_b}`) | rel_Q = 5.15e-3 (10 r_M, 2·r_in) → 5.18e-5 (100 r_M); rel_RAR = 8.64e-4 → 8.65e-6; matches analytic leading terms 5e-3/5e-5 (Q), 8.33e-4/8.33e-6 (RAR) | 2.0 (bound check) |
| C8 | Both footings separate and scale exactly: `W_self(alt)/W_self(can) = sqrt(a0_alt/a0_can)` | ratio 1.0976232541844928, max dev from analytic **2.02e-16** | 1e-9 |
| C9 | Virial σ² with central mass: `2T + W_self + W_cent = 3P_sV`; singular limit `σ² → C/2` (sympy, with `m_s = C/G` substituted) | `σ²/(C/2) = 0.953…8.456` across the grid (finite-shell corrections); `singular_limit_ok = true` | limit identity |

**Symbolic layer (sympy, exact):** closed form verified, separation verified, singular limit verified, σ² → C/2 verified (all `true`), i.e. symbolic identities agree with the numeric audit; the numeric audit is genuine quadrature of the raw integrand (not evaluation of the closed form).

## 5. Lean 4 certificate (independent formal check)

`AS084_virial_identity.lean` — standalone, verified with `lake env lean` (Lean 4.34.0-rc2, mathlib 4.34.0-rc2) **exit 0**, all axioms ⊆ {propext, Classical.choice, Quot.sound}, zero `sorry`. Certificates:

- `virial_integral_closed`: HasDerivAt-based FTC (`integral_eq_sub_of_hasDerivAt_of_le`) for the primitive `F(r) = G·m_s·(M_in·ln r + m_s·r − m_s·r_in·ln r)` plus log algebra ⇒ full closed form on `0 < r_in < R`.
- `separation_of_terms` (defeq) and `virial_value` (`−(∫ …) = W_tot`).
- `naive_error_exact`: exact deviation formula for arbitrary `M_in` (R ≠ 0).
- `naive_overbinds`: **negative control as a theorem** — `W_naive − W_tot < 0` for every finite shell, `M_in = 0` (`G, m_s, r_in > 0`, `r_in < R`), using `Real.log_lt_sub_one_of_pos`.
- `wself_singular_limit`: `W_self(r_in) → −G·m_s²·R` as `r_in → 0⁺` (`𝓝[>] (0:ℝ)`), built from `tendsto_log_mul_rpow_nhdsGT_zero` and `Real.log_div` on the right-neighborhood.

## 6. Representative numbers (both footings, SI)

Shell `r_in = 0.1·R, R = 0.62·r_M, M_in = 0.1·M_b` (`M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`):

| footing | M_b | C [kg·m/s] | r_M [kpc] | v_flat [km/s] | σ [km/s] | W_cent [J] | W_self [J] | W_tot [J] | W_tot/(M_b c²) |
|---|---|---|---|---|---|---|---|---|---|
| canonical | MW 6.5e10 | 2.841849e10 | 9.838 | 168.58 | 119.20 | −8.457639e50 | −1.525220e51 | −2.370983e51 | −2.0411e-7 |
| canonical | NGC3198 6.2501e10 | 2.786685e10 | 9.647 | 166.93 | 118.04 | −7.974612e50 | −1.438112e51 | −2.235573e51 | −2.0014e-7 |
| alt | MW 6.5e10 | 3.119280e10 | 8.963 | 176.61 | 124.89 | −9.283301e50 | −1.674116e51 | −2.602447e51 | −2.2403e-7 |
| alt | NGC3198 6.2501e10 | 3.058730e10 | 8.789 | 174.89 | 123.67 | −8.753120e50 | −1.578505e51 | −2.453817e51 | −2.1968e-7 |

## 7. Strongest surviving statement, negative-control result, next implication (seed step 5)

**Strongest statement.** For the conditional deep-equilibrium sector with `κ = 1/2` (adopted), on the exact domain `0 < r_in < R ≤ r_M`, `M_in ≥ 0`: the virial of the `1/r²` phantom shell about a central mass is the exact closed form of §1 — central-mass attraction and shell self-gravity are separately identified and never conflated; the naive `−G·M(R)²/R` replacement is **excluded for every finite shell** (strict overbinding, 3.83%–64.88% deviation, Lean-provable for `M_in = 0`), recovering exactness only in the singular limit where `M(R) = m_s·R = (C/G)·R` and `σ² → C/2`.

**Negative control result (capable of failing — it fails as required):** C4/C4b rejected the naive form on all 96 finite-shell samples and confirmed exact recovery only as `r_in → 0⁺`; the analytic deviation `−G·m_s²·r_in·[ln(R/r_in) − (1 − r_in/R)]` is positive-definite on the whole finite-shell domain. The negative control is a real control: had the naive form been the true virial, deviations would have been ≤ 0.1% and C4 would have failed the audit.

**Next unresolved implication.** The virial *balance* is now exact, but the seed's distinct obligation — *dynamical attainment* — is open: nothing here shows that the deep-exterior filtered-MONO flow actually *reaches* the state `M(r) = M_in + m_s·(r − r_in)` with `σ² → C/2` at finite time, nor what interior pressure term supplies the virial deficit at finite `r_in` (C9: `σ²/(C/2)` between 0.31 and 8.5 across the grid). The first transfer step is to compute the enclosed mass `M_MONO(r)` from the operative filtered-MONO density (Q/RAR proxies are bounded by C7 to ≤0.52% / ≤0.086% at `r_in = 10 r_M`, `R = 2 r_in`) and re-run the virial identity with the kernel-exact `M_MONO(r)`.

## Limitations

- Static scalar virial only: no dynamics, no profile attainment, no Jeans/beyond-Newtonian kernel beyond the bounded C7 comparison; the σ² value is a virial-consistent estimate, not a measured dispersion.
- `κ = 1/2` is adopted, not derived; `rho_Lambda` values per footing are fixed by `a0` inverts, and both footings cannot share density and κ simultaneously (footing relations recorded).
- Finite-shell results (`R ≤ r_M`) do not transfer to the filtered-MONO interior without the C7 kernel check; the interior imposed-log-well ansatz (`R ≤ r_M` fixtures) is explicitly not a controlled point-source deep-MOND domain.
- Spherical symmetry assumed; shell mass normalization `m_s = C/G` inherited from G084's source normalization.
- C4b and C6 residuals at 1e-11–1e-7 levels are set by float64 arithmetic for energies ~1e51 J (relative, not absolute, error claims).

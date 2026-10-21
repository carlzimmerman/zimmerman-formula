# CFG953 DERIVATION: the minimal source-changing non-local theory (SCT)

Criteria `FROZEN_CRITERIA.md` (049a0f867, committed alone first). Amendment `AMENDMENT_A1_pre_result.md` (611bb324a, pre-result for the
main stage, committed alone; reported-only addition to (g)). Every load-bearing statement below has a sympy or numeric check in
`cfg953.py`, named in brackets. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle species.
Not "theory closed". Nothing here says the data favour the framework.

**Overall class (frozen rule): SCT CONDITIONAL (SCT-M, the primary).**

| test | (a) | (b) | (c) | (d) | (e) | (f) | (g) |
|---|---|---|---|---|---|---|---|
| SCT-M | PASS | PASS | PASS | PASS | CONDITIONAL (C-E) | PASS | CONDITIONAL (C-DF) |
| SCT-Q | PASS | PASS | PASS | PASS | CONDITIONAL (C-E) | PASS | **FAIL** |

**SCT-M** fails no test, and two tests rest on named conditions:
- **C-E:** energy closes only through a non-dynamical internal energy carried by each phantom body.
- **C-DF:** DF2/DF4 are in-situ debris.

Two further conditions bind its application to real systems: C-MR (the merge rule must act) and C-c (a relativistic finite-c_u body).

**SCT-Q**, which uses the pointwise QUMOND phantom of the own baryons, is **INCONSISTENT**. In-situ systems inherit the host EFE, and
the Lelli+15 tidal dwarfs exclude that: CFG936 route (iii), z −3.48 / −3.79. The source therefore has to be a coarse (monopole)
function of the own baryons, not the pointwise phantom.

---

## 1. The construction

### 1.1 Chassis and what conservation forces

  G_μν = (8πG/c⁴)(T^b + T^c + 𝒮)_μν.

Baryons and all cold dust are geodesic, and the dust has no tether (CFG938's matter sector without W, χ, λ or stiffness). The
Bianchi identity and ∇_μT^b_μν = ∇_μT^c_μν = 0 force ∇_μ𝒮^{μν} = 0 separately. With J_s = ∂·𝒬 (𝒬 antisymmetric) the NR content is
ρ_s = −∇·𝒫 and j_s = ∂ₜ𝒫 + ∇×M, so ∫j_s = Ḋ_s (D_s the 𝒮 dipole). Total momentum P_m + Ḋ_s is conserved iff

  D̈_s = −∫ρ_s ∇Φ_m        (CFG947 T-M),

i.e. the 𝒮 dipole must fall as if its mass felt the matter's field.

### 1.2 Conversion: the source (R2)

  𝒮^{μν} = Σ_q Σ_q^{μν} − T^{μν}_{c,lab}.

- T_{c,lab} is the full stress-energy of the cold dust that carries a domain label. Between label events it is conserved by itself
  (geodesic dust), so ∇_μ𝒮^{μν} = 0 reduces to ∇_μΣ_q^{μν} = 0 for every body.
- Cancelling only the dust's rest mass would leave a part of T_c,lab that is not separately conserved. Covariance therefore forces the
  whole tensor out, including kinetic energy and stress. Consequences:
  - labelled dust is gravitationally inert: it falls, but sources nothing and carries no momentum in the books;
  - its velocity-dispersion pressure, which set CFG947's worst slip (1.63e-5), is gone from the source.
- NR gravitating density: ρ_g = ρ_b + ρ_{c,unl} + Σ_q σ_q. It is non-negative wherever every σ_q ≥ 0 (S-+). There is no draw shell
  of negative weight, so no cap is needed (CFG947 needed the cap; Mu5 there).
- Zero-sum per domain: ∫ρ_s,q = M_c,q − M_c,lab,q = 0, exactly, because a body's mass is its labelled cold mass (S-Z).

In words: at collapse, a system's cold energy changes phase. Its gravitating mass, momentum and energy move into a "phantom body"
whose shape is the law's phantom of the system's own baryons. The dust carrier keeps falling but no longer gravitates.

### 1.3 The body's shape (R3)

**SCT-M (primary).** σ_q is spherical about its own centroid X_q:

  M_σ,q(<r) = min{ r²[g_law(ḡ) − ḡ]/G , M_c,q },   ḡ = G M_b,q(<r)/r²,

with M_b,q(<r) the own-baryon monopole about X_q. The edge r_e is the kernel's own supply root, M_ph(<r_e) = M_c (CFG947 T-E: forced
inside turnaround). For the record's spherical-equivalent rotation-curve convention this is the law exactly inside r_e.

**SCT-Q (variant).** The pointwise QUMOND phantom of the own baryons, carried rigidly, with the spin S_q absorbing torques.

The two coincide for spherical systems. They differ where an in-situ sub-system sits inside a parent:
- SCT-Q's pointwise phantom has a local lump at every concentration of the parent's own baryons, which is the host EFE;
- SCT-M's monopole has none.

### 1.4 Dynamics and the escape from T-M (R4; S-P, S-TM)

The body's centroid momentum P_q = M_c,q V_q obeys dP_q/dt = ∫σ_q g dV between events. A conversion is an inelastic capture:
- M_c → M_c + m;
- X → (M_c X + m x)/(M_c + m);
- P → P + m v;
- S and E_int absorb the internal angular momentum and energy.

**Theorem S-P.**
- The book momentum P = Σ_{b,unl} m v + Σ_q M_c,q V_q is exactly conserved.
- Between events: dP/dt = Σ_{b,unl} m g(x) + Σ_q ∫σ_q g = ∫ρ_g g = 0, since a Poisson field exerts no net force on its own source.
- At events: ΔP = 0 by the capture algebra (sympy).
- Because ∫j_s = Ḋ_s = Σ M_c V_q − Σ_lab m v, P equals the full momentum P_m + ∫j_s: the 2-form current carries exactly the
  labelled dust's momentum with a minus sign.

**Theorem S-TM.**
- Under R4 the relocation term R = D̈_s − ∫ρ_s g vanishes identically: for CFG947's two-blob toy, for any conversion history, and
  in general (sympy).
- The reason: the capture keeps D_s and Ḋ_s continuous, and between events the body's centroid law is the momentum condition
  itself.
- **The price.** The body is centred on the centroid of the dust it converted, not on the baryons. In the two-blob toy it sits at
  εX from the core. The baryons are then re-centred by the baryon–body attraction (a bound two-body mode), and the law holds exactly
  only for δ = 0.
- This is CFG947's way out (ii) ("an independent 𝒮 dipole degree of freedom"), with zero free initial data: X_q and V_q are fixed
  at birth by the converted dust.

**Existence of the stress.** The body's compact stress Π_σ (∇·Π_σ = −σ g + σ A_q, plus the reshaping current) exists iff
∫(−σg + σA_q) = 0, which is R4. It is symmetric iff the body feels no net torque about its centre, which holds for a sphere (S-L).

### 1.5 Angular momentum (R5; S-L)

Gravitational forces between mass elements are central. A spherical body's own field is radial about X_q, so the torque it exerts on
anything about X_q is zero, and by the pair argument so is the torque on it. Its spin S_q therefore changes only at events, where it
absorbs the converted element's angular momentum about the new centroid (sympy: ΔL_tot = 0).

In the 2-form language S_q lives in the magnetic part, j_s ⊃ ∇×M, which carries angular momentum but no density and no net momentum.
Its gravitomagnetic effect is O(v²/c²).

### 1.6 Energy (R6; S-En)

With W = ½∫ρ_g Φ:
- d(K + W)/dt = Σ_q P_σ,q, where P_σ,q = ∫Φ ∂ₜσ_q|_shape is the work done by reshaping;
- conversion and merge events change K + W discontinuously.

No dynamical sector supplies these terms: baryons are geodesic and the body's shape is prescribed. Energy closes only with an
internal energy E_int,q per body: a declared, non-dynamical reservoir that gravitates at 1/c². This is SCT's version of CFG935's
"settling needs an energy sink outside matter".
- SCT has no settling problem: the labelled dust never needs to reach the law profile, because its gravity is already the body's.
- But building the body still moves gravitating mass (§3, S-En), and that energy must go somewhere.

### 1.7 Domains, labels, in-situ systems, merges (R1, R7)

- **Birth.** At first turnaround from the Hubble flow, with baryons present (no RMIN; peaks at L*). Labels are latched.
- **In situ.** A system formed inside a collapsed domain (stars, binaries, clusters, tidal dwarfs, collisional debris) is not a
  domain, and finds no unlabelled dust to convert.
- **Merges.** Bound fraction < ½, or coalescence; inelastic in mass, momentum, spin and E_int.

### 1.8 Causality (R8)

- Every inverse operator is retarded, □_ret⁻¹.
- The shape uses the retarded angle average.
- Body signals and relocation currents propagate at c_u = c.
- The rigid-centroid law is the NR limit (c_u → ∞), valid when r_e/c ≪ t_dyn. For NGC 3198, r_e/c ≈ 1.5 Myr.
- A finite-c_u relativistic body whose limit is R4 is not constructed. That is condition C-c.

### 1.9 No action (R9)

The equations are retarded and non-local. The time-symmetric action form is acausal (Mu6: a precursor of ½), so SCT cannot meet
CFG678's one-action rule together with causality.

---

## 2. Structural results (each with its check)

| id | result |
|---|---|
| S-P [S-P_momentum_event_algebra] | a conversion event leaves D_s, Ḋ_s, P_tot and L_tot unchanged (sympy: [0,0,0] each); the 𝒮 self-force on 40 random signed weights is 1.8e-14 (Poisson symmetry). With R4 between events this gives exact conservation of P = Σ_{b,unl} m v + Σ M_c V |
| S-TM [S-TM_relocation_term_zero] | CFG947's two-blob toy under R4: R = D̈_s − ∫ρ_s g = 0 for any conversion histories m_±(t), blob motion X(t) and body force F(t), including CFG947's draw proportions. E8's prescribed draw gives −ε(M̈_e X + 2Ṁ_e Ẋ) (K6 reproduces π²ε/4). The price: the body's centroid sits at εX, the converted dust's centroid, off the baryonic core |
| S-L [S-L_no_torque_on_spherical_body] | torque on a spherical body about its centre from any mass element = 0 (sympy); the spin absorbs each converted element's internal angular momentum |
| S-Z [S-Z_zero_sum_per_domain] | body mass at the supply root = M_c to 2.0e-15 (NGC 3198, both footings and kernels), so ∫ρ_s,q = 0 |
| S-+ [S-+_body_positive] | simple kernel: dg/dy − 1 > 0 because (y + 2)² − (y² + 4y) = 4; dν/dy = −1/(y^{3/2}√(y + 4)) < 0. ν_mono checked numerically on y ∈ [1e-12, 1e6]. Hence σ ≥ 0 whenever M_b(<r) is non-decreasing (the true monopole always is). NGC 3198's spherical-equivalent m_N is *not* monotone (the record convention's gas term), but M_ph rises at all 43 radii on both footings and kernels, so σ ≥ 0 there |
| S-E [S-E_edge_inside_turnaround] | r_e/r_ON ∈ [0.019, 0.514] for M_b = 1e3–1e15 M⊙, both footings and kernels: the edge lies inside turnaround |
| S-C [S-C_retarded_support] | the retarded response vanishes before r/c; 𝒮 updates propagate at c (R8) |
| S-En [S-En_formation_energy] | building a body from dust spread uniformly over r_ON (baryons fixed) releases E_rel = 0.70–0.99 \|W_f\| (canonical 0.988 at 1e3, 0.961 at 1e6, 0.878 at 1e9, 0.834 at 1e12, 0.701 at 1e15; alt 0.728–0.989), i.e. E_rel ≈ (0.82–1.10) M_c v_f², which is 4.1e-11 – 4.3e-5 of M_c c² (UFDs → clusters). Released for every M_b |

**Reading of S-En.** SCT removes CFG935's settling problem, because labelled dust never has to reach the law profile. It does not
remove the energy: rearranging the gravitating mass from the turnaround sphere into the body releases about one binding energy, and
that energy must go into E_int (R6). This is CFG935's "sink outside matter", now built into the body.

## 3. Tests

### (a) Static law, one domain [PASS]

NGC 3198, 43 radii, Υ = 0.61, spherical-equivalent convention, edge at the kernel's own supply root. N = M_c/M_b = 53.64 (census).
r_e = 453.9 kpc (canonical) / 412.9 kpc (alt).

| footing, kernel | max dev P-S / P-I / P-X | deep y = 1e-2 / 1e-3: dev; V⁴/(G M_b a₀) | y_e (V⁴/(G M_b a₀) there) | law at y = 1e-14 | g/g_law at 2 r_e |
|---|---|---|---|---|---|
| canonical, simple | 2.2e-16 / 2.2e-16 / 2.2e-16 | 0 / 0; 1.1051 / 1.0321 | 3.41e-4 (1.0186) | 1.00000010 | 0.502 |
| canonical, ν_mono | 2.2e-16 (all three) | 0 / 0; 1.1043 / 1.0320 | 3.41e-4 (1.0186) | 1.00000010 | 0.502 |
| alt, simple | 2.2e-16 (all three) | 0 / 2.2e-16; 1.1051 / 1.0321 | 3.41e-4 (1.0186) | 1.00000010 | 0.502 |
| alt, ν_mono | 2.2e-16 (all three) | 2.2e-16 / 1.1e-16; 1.1043 / 1.0320 | 3.41e-4 (1.0186) | 1.00000010 | 0.502 |

**What it shows.**
- **No C-ρ condition.** Labelled dust is inert, so P-S, P-I and P-X agree exactly. Class A (CFG947) exceeded the law wherever the
  dust outnumbered the phantom (P-X 0.83).
- **The kernel's own root makes both kernels exact.** CFG947's N1 failed the simple kernel through E7.
- **The deep BTFR holds to the edge only.** The flat part runs from a few r_M to r_e = (N + ½) r_M. y_e = 1/N² ≈ 3.4e-4, where
  V⁴/(G M_b a₀) = 1.019; beyond, the curve falls as Kepler (0.50 of the law at 2 r_e).
- **What (a) does not show.** For one domain the body *is* the law's phantom by definition. (a) checks the edge, the kernel root and
  the dust's inertness, not physics beyond that.

**a3 (reported, no class weight).**
- **Disc geometry.** For a thin exponential disc, the monopole body against the pointwise law differs by at most 0.016 / 0.039 /
  0.054 dex at y(R_d) = 10 / 1 / 0.1, always *below* the law, and most for low-surface-brightness discs. SCT-M is the record's law
  exactly only in the spherical-equivalent convention used by every parent lane (CFG938–952). A true-monopole SPARC fit has not been
  done here (open).
- **Supply.** N = 53.6 for M_b ≤ 3e10, then 44.1 (1e11), 14.9 (1e12) and 8.3 (1e13). CFG803's lines (3 / 4 primary; 16 / 24 all
  radii) are met to 1e11; at 1e12 only the primary line is met (as CFG947 T-E).

### (b) FRW and growth [PASS]
- Dust: ρ = m/a³, p = 0, isotropic (sympy).
- 𝒮 ≡ 0 on FRW, since Δ_ta(z) ≥ 5.569 > 1 means no domain exists.
- Linear dust exponent n = 1.000000000000.
- Top-hat density rises monotonically to 9π²/16, so no domain is born before turnaround.
- After domains exist, the bodies are free-falling centres of mass. The body gas obeys the dust growth equation, with roots
  {−1, 2/3}, so n = 1. Large-scale growth stays a¹ (CFG947's positive result, kept).

### (c) No hover and no satellite EFE [PASS]

CFG882's H1–H3 at 50/100/250 kpc from the 6e10 M⊙ host. Canonical values; alt maxima in brackets.

| satellite, D | Δa/g_host (tidal) + retardation | δ_eq/a | EFE (dex) | host tidal term (dex, reported) | body edge vs Jacobi (kpc) |
|---|---|---|---|---|---|
| H1 50 | 1.5e-7 + 1.2e-7 | 7.3e-7 | 3.0e-7 | 0.001 | 0.21 / 0.40 |
| H2 50 | 3.2e-5 + 9.8e-8 | 1.9e-4 | 7.6e-5 | 0.006 | 1.17 / 1.25 |
| H3 50 | **2.7e-3** + 2.2e-7 | **7.0e-3** | **2.6e-3** | 0.009 | **9.38 / 5.07** |
| H3 100 | 6.9e-4 | 8.5e-4 | 3.2e-4 | 0.002 | 9.38 / 8.18 |
| H3 250 | 1.1e-4 | 5.2e-5 | 1.9e-5 | 0.000 | 9.38 / 15.2 |
| max (alt) | (2.1e-3) | (5.4e-3) | (2.1e-3) | (0.009) | |

**c1.** max Δa/g_host = 2.7e-3 (canonical) / 2.1e-3 (alt), against ε_B = 0.344 / 0.317.
- The satellite's stars and its body both fall at g_host at monopole order: the body's centroid obeys R4, and by the shell theorem
  only host matter *inside* the body's extent (the host's own smooth body) produces a difference.
- This is CFG947's no-hover result, kept, against CFG941/945's tethered 1.017–1.107 (K2, Mu2).

**c2.** The EFE is 0 by construction: a satellite's body depends on its own baryons only. The equilibrium baryon–body offset driven by
the tidal Δa moves the law at the Plummer radius by at most 2.6e-3 dex, against δ_c = 0.082 (CFG874 via CFG945).

**Reported.** SCT-M's body is rigid and is not tidally truncated. H3's body (9.4 kpc) extends beyond its Jacobi radius at 50 and
100 kpc (5.1 / 8.2 kpc): the satellite keeps all its gravitating cold mass while its stars can be stripped. Bodies cause no dynamical
friction (they are not particles). Both are untested predictions.

### (d) Slip [PASS]

| system | s (worst of s_grad, s_847), canonical / alt |
|---|---|
| CFG847 dwarf | 3.6e-9 / 4.0e-9 |
| MW disc | 2.5e-7 / 2.8e-7 |
| MW outer | 2.9e-7 / 3.1e-7 |
| group | 9.1e-7 / 9.3e-7 |
| cluster | 1.25e-5 / **1.35e-5** |
| NGC 3198 (43 radii) | 3.0e-7 / 3.4e-7 |

The worst value is 1.3548e-5, within the 1.9e-5 line. The body's isotropic stress completion is the only stress left: the labelled
dust's dispersion pressure (CFG947's worst, 1.63e-5, K4) is cancelled with its stress-energy (R2).

### (e) Conservation [CONDITIONAL: momentum PASS, energy through E_int]

**e1 (sympy).** S-P, S-TM and S-L above.

**e3.** The force between two overlapping spherical bodies, computed both ways by adaptive quadrature, is equal and opposite to 1.4e-11.
The bodies were Plummer M_b = 1, a = 1, M_c = 20 and M_b = 0.3, a = 0.5, M_c = 8, at separation 6.

**e2 (N-body toy, criteria §4).**

| run | dP/P_scale | dL/L_scale | \|ΔE_tot\|/\|E₀\| (with E_int) | \|ΔE_mech\|/\|E₀\| (without) | E_int needed |
|---|---|---|---|---|---|
| E, dt 2e-3 (formation 200 + accretion 60 conversions; satellite infall) | 6.6e-16 | 7.9e-16 | 1.47e-4 | 0.249 | conversion −0.227, reshape −4.7e-5 |
| E, dt 1e-3 | 2.3e-15 | 1.3e-15 | 6.97e-5 | 0.239 | conversion −0.226, reshape −4e-4 |
| M (head-on merger), dt 2e-3 | 1.6e-15 | 2.3e-15 | 2.46e-5 | 0.217 | merge −0.207, reshape −0.009 |
| E, Mu3 glued body (MUTATE) | **0.526** | **0.488** | — | 0.248 | not booked |

All values in units of \|E₀\| (E₀ = −29.59 for run E, −75.93 for run M).

**What the toy shows.**
- **Momentum and angular momentum** are conserved to round-off through 260 conversion events, satellite infall and a merger. The
  glued-body mutation (the class-A way: body nailed to its baryons, conversions without momentum transfer) loses 53% of the momentum
  scale.
- **Energy is conserved only with E_int.** Without it the mechanical energy changes by 22–25% of \|E₀\|. With it, the residual is
  integrator error, which halves with dt (1.47e-4 → 6.97e-5).
- **The sign of E_int depends on geometry.**
  - In the toy, the dust cloud (R = 10) lies inside the body's edge (r_e ≈ 20), so building the body *costs* energy (−0.23 \|E₀\|).
  - In real domains r_e < r_ON (S-E), so formation *releases* 0.70–0.99 \|W_f\| (S-En).
  - The merger *costs* energy. Two own-domain bodies merging into the law of the combined baryons weakens gravity: the monopole g at
    r = 5 falls to 0.749 of its pre-merge value, the T-L non-additivity √f + √(1 − f). W therefore rises by 20.7 and E_int pays
    15.7 = 0.207 \|E₀\|, after absorbing the bodies' relative kinetic energy (4.98).
  - So E_int must both absorb and supply O(1) binding energies. Whether it stays non-negative through a merger history is not
    established.
- **The price of S-TM, seen in the toy.**
  - Host A's body was born at the first converted dust element, 4.8 from the baryon centre. It ends 0.70 (dt 2e-3) / 0.69 (dt 1e-3)
    from the baryon centre, in units of the baryons' Plummer a = 1: an undamped baryon–body sloshing mode after anisotropic accretion.
  - Satellite B ends 0.022 from its body (a = 0.1). This is toy granularity: its neighbours are 0.1-mass dust particles.
  - The law holds exactly only when the offset is zero.

**Grade.** Momentum and angular momentum PASS. Energy closes only through E_int, so (e) is CONDITIONAL (C-E), as CFG950's (e) was with
its R-E.

### (f) Dwarfs: the law with no RMIN [PASS]
- Every system with baryons born at turnaround has a domain, whatever its mass (grid 1e3–1e15). CFG947's T-R obstruction is absent.
- For CFG939's classes and H1–H3, with Plummer stars and isotropic Jeans, the edge moves the aperture σ²_los(<R_e) by:

| | UFD-c | UFD-e | Draco-like | Fornax-like | H1 | H2 | H3 |
|---|---|---|---|---|---|---|---|
| canonical (simple) | −0.0004 | **−0.019** | −0.0001 | −0.0000 | −0.0001 | −0.0002 | −0.0000 |
| alt (simple) | −0.0006 | **−0.024** | −0.0002 | −0.0000 | −0.0002 | −0.0003 | −0.0000 |
| r_e/a (canonical) | 4.9 | **1.5** | 6.7 | 18.6 | 7.0 | 5.7 | 13.3 |

- ν_mono gives the same to 1e-4. The maximum, 0.024 dex, is well inside the 0.082 line, and σ ≥ 0 everywhere.
- The SPARC dwarf's rotation point (5 kpc) lies well inside its edge (41.4 / 37.6 kpc).
- **Reported.** In extended UFDs (UFD-e) the law ends at about 1.5 half-light radii.

**Excess family: NO HANDLE.** SCT's prediction for every dwarf, satellite or isolated, is the EFE-free law of its own baryons (0 dex
excess). Nothing in SCT makes a dwarf's gravitating mass exceed the law:
- the body *is* the law's phantom up to the supply edge;
- a stripped satellite keeps M_c but its body follows the law of its remaining baryons.

SCT is no better on the record's dwarf excess than every earlier variant.

### (g) Below-law systems [SCT-M CONDITIONAL; SCT-Q FAIL]

CFG936's data, statistic and primary class rule (K7 reproduces its route (i) and (iii) class-T numbers).

| prediction | footing | T (6 TDGs, dex) | U (DF2 + DF4, ln σ²) |
|---|---|---|---|
| **SCT-M: Newton (no own body, monopole parent)** | canonical | +0.055 ± 0.114 (z +0.48), χ² 1.17/6 → **EXPLAINS** | +0.028 ± 0.539, χ² 0.25/2 → **EXPLAINS** |
| | alt | the same → **EXPLAINS** | the same → **EXPLAINS** |
| SCT-Q: host EFE (route iii) | canonical | −0.381 ± 0.110 (z −3.48), χ² 14.85/6 → **FAILS** | −1.153 ± 0.480 (z −2.40) → FAILS (CFG936 with corners: PARTIAL) |
| | alt | −0.414 ± 0.109 (z −3.79) → **FAILS** | −1.232 ± 0.480 (z −2.57) → FAILS |

- **SCT-M.** In-situ systems (R1) have no own body, and their baryons enter the parent's body only through its monopole, which has no
  local lump. TDGs then come out Newtonian, with no further premise. DF2/DF4 come out Newtonian too if they are in-situ debris (the
  record's reading, CFG933/936/768). A primordial DF2/DF4 would carry its own body and sit on the law, which CFG936 already excludes.
  Hence CONDITIONAL (C-DF).
  - Unlike CFG936's route (i), the zero supply is not a label put on these objects: inside a collapsed parent all cold dust is already
    converted, so there is nothing to capture. This is stronger than CFG939's v_rel > V_esc,b criterion and consistent with it.
  - Coma UDGs (CFG948): Newton is excluded at 5.45σ, so under SCT they must be turnaround-born, with their own body, and sit at the
    law. Ceiling +0.018 ln against +0.76 observed (z +1.63 / +1.43 with systematics): NOT DIAGNOSTIC, as CFG948.
- **SCT-Q.** The Sun's, the binaries' and the TDGs' baryons are their parent's own baryons. The pointwise phantom then has a local,
  EFE-reduced lump at each of them, and the TDG data exclude that. This is the discriminating finding of the lane.

**A1 (reported, no class weight): the parent body's local density inside an in-situ system.**
- At the TDGs (hosts 0.6 L_K at the projected D_p, an upper bound) the orientation-averaged term (4π/3)Gρ_h r raises the Newton
  prediction by +0.018 to +0.099 dex (alt +0.020 to +0.108). r̄ becomes −0.013 ± 0.114 (alt −0.019): still EXPLAINS.
- For DF2 / DF4 it adds +0.074 / +0.165 ln (alt +0.081 / +0.180). r̄ becomes −0.092 ± 0.539: EXPLAINS.
- The TDG errors are 0.15–0.38 dex, so this term is below the data's resolution, but not negligible.

### (h) CFG678 scorecard (reported)

| status | SCT-M | SCT-Q |
|---|---|---|
| PASS | A5 | A5 |
| CONDITIONAL | A1, A2, A6, B3, C1, C2 | A1, A2, A6, B3, C2 |
| FAIL | C3 (inherited, CFG529) | C3 |
| NOT DECIDED | C4 (CFG954) | C1, C4 |
| PENDING | D3 | D3 |
| UNTESTED | A3, A4, B1, B2, D1, D2 | A3, A4, B1, B2, D1, D2 |
| DECLARED | A7, E1–E3 | A7, E1–E3 |

**Notes on the rows.**
- **C2.** SCT-M SPARC rms 0.10033 @ Υ 0.61 / 0.09910 @ 0.57, equal to the local law, with 0 of 3389 points beyond an edge. It is
  CONDITIONAL, not PASS, because the law comes from the prescribed 𝒮 (CFG678: a recipe never PASSes).
- **C1, SCT-M.** The Sun formed in situ, so it has no own body, and the MW body is smooth. The Solar System is Newtonian plus the
  ordinary galactic tide: 4πGρ_σ/3 = 1.3e-31 s⁻² (ρ_σ(8 kpc) = 4.6e-22 kg m⁻³), with no EFE quadrupole.
- **C1, SCT-Q.** The Sun lies inside the pointwise phantom, which gives the QUMOND EFE quadrupole (G01/G02; not recomputed).
- **Wide binaries.** SCT-M: Newtonian, z = −1.36 / −1.51 against the DR3 builder (PASS, \|z\| ≤ 2), agreeing with the sealed DR4
  "exactly Newtonian". SCT-Q: CFG653's QUMOND-EFE values 1.179 / 1.244 (PASS / TENSION).
- **D2.** Linear growth is a¹, but the CFG596 line needs an SCT PM engine and a 1024³ run. The class-A shear passes (T1x / T2x /
  NC1x / NC2x) do not transfer: SCT is not class A's parent.
- **Against CFG950 (LDT).** A6 and C1 move to CONDITIONAL. B1 is still not passable (prescribed label sector), and C3 is still FAIL.

## 4. Clusters (first-order statement only; CFG954 decides)

In SCT-M:
- members keep their whole, rigid bodies until R7 merges them;
- the host's body is the law of the host's own baryons (no cross-sourcing, so no CFG951 inter-label sourcing);
- members' bodies add only as Newtonian mass.

The cluster therefore lies between two CFG951 rows:
- the plain-law row, if every member merges: eRASS1 A_MID 1.91 / 1.75 (Z +7.7 / +6.9), a core deficit, with A_OUTER fine;
- the X-OD row, if members persist: A_OUTER 0.81 / 0.75 (Z −2.7 / −4.0) even with members L2-truncated. SCT-M's members are not
  truncated, so their memory would be at least as large.

So SCT-M does not by itself fix clusters: it either keeps the core deficit or carries merger memory, depending on R7.

**Differences from CFG954's working statement (frozen before this lane), for its amendment if needed:**
- SCT-M has no clip: labelled dust is inert, rather than CFG947's ρ_s = max(ρ_ph − ρ_c, 0).
- Its bodies are rigid and are not truncated at King r_J.
- Its momentum rule is the inelastic body centroid, not carried weights.

## 5. Classes (frozen rule)

| variant | a | b | c | d | e | f | g | class |
|---|---|---|---|---|---|---|---|---|
| SCT-M | PASS | PASS | PASS | PASS | CONDITIONAL | PASS | CONDITIONAL | **SCT CONDITIONAL** (C-E, C-DF) |
| SCT-Q | PASS | PASS | PASS | PASS | CONDITIONAL | PASS | FAIL | **SCT INCONSISTENT** |

**Overall: SCT CONDITIONAL.** The obstruction for SCT-Q is computed: TDGs at z −3.48 / −3.79 below its prediction. To remove it,
SCT-Q would need a rule that takes in-situ sub-systems out of the parent's own-baryon field. That rule would have to separate tidal
dwarfs from stars, which must stay in it; a rule that made every self-bound object a domain would empty a galaxy's own-baryon set
(CFG947 T-R discussion). No such rule is declared here. This is an argument, not a proof that none exists.

**Open conditions for real systems** (not needed for any graded PASS here, listed because they bind applications):
- **C-MR.** Real galaxies are single-domain only if R7 acts (T-L otherwise). CFG952 found CFG947's M-R does not fire in equal-mass
  mergers. R7's coalescence trigger is untested outside this toy.
- **C-c.** No finite-c_u relativistic body with R4 as its limit has been constructed.

## 6. Costs (all of them)

1. **An action-less, retarded, non-local source sector** (R9). No CFG678 gate set by 𝒮 can PASS.
2. **A prescribed label sector:** birth at turnaround from the Hubble flow, latch, the in-situ rule, and the merge rule R7 (B1
   UNTESTED by construction).
3. **Rigid phantom bodies** with charges (mass, centroid, momentum, spin, internal energy). Their initial values are fixed by the
   converted dust, so there are no free initial data, but the body is a non-relativistic idealization (C-c).
4. **E_int, a non-dynamical reservoir.**
   - Formation: it absorbs 0.70–0.99 \|W\| (4e-11 – 4e-5 of M_c c²).
   - Mergers: it supplies about 0.2 \|E\| (toy).
   - It is CFG935's sink outside matter, declared and not derived.
5. **Cold energy changes phase at collapse.** The labelled dust becomes gravitationally invisible: it falls, but sources nothing and
   carries nothing in the books.
6. **Baryon–body offsets after anisotropic accretion** (toy: 0.7 of a disc scale, undamped). The law is exact only at zero offset.
7. **No tidal truncation of bodies and no dynamical friction from them.** A satellite keeps its whole gravitating cold mass.
8. **A monopole source.** It is the law exactly only in the spherical-equivalent convention; true discs fall up to 0.054 dex below
   the pointwise law (LSB end).
9. **The supply N comes from the engine's census** (f_ret table; inherited, flagged). The law inside r_e does not depend on it; the
   edge does.

## 7. What SCT fixes, and what it does not, relative to the record

| issue | record | SCT-M |
|---|---|---|
| satellite hover (D-T, S) | tether: Δa/g_host 1.02–1.11 (CFG941/945) | 0 at monopole order; tidal ≤ 2.7e-3 |
| linear self-gravity, growth | tether: a^0.694 (CFG941) | a¹ |
| T-M (relocation not conservable) | CFG947: π²ε/4; CFG952: positive slaved draw infeasible | R ≡ 0: inelastic body centroid (S-TM); price: offsets |
| T-R (RMIN) | 128/175 SPARC galaxies law-off | no RMIN; every collapsed system with baryons |
| T-X (global phantom EFE) | −0.10 … −0.73 dex | 0 (own baryons only); Mu1 restores it |
| condition C-ρ (dust > phantom) | class A exceeds the law (P-X 0.83) | gone (inert dust) |
| cap / negative density | class A needs the cap (Mu5) | σ ≥ 0, no draw shell |
| inter-label sourcing (CFG951) | LDT: members source the host's law | none (host law from own baryons) |
| energy at events | LDT: R-E label energy (CFG950) | E_int body energy (same status) |
| TDGs / DF2/DF4 | zero supply by label (CFG936) | Newton derived from the in-situ rule (DF2/DF4 conditional on origin) |
| wide binaries, Cassini | QUMOND EFE (CFG653/947) | Newtonian (in situ) |
| dwarf excess | unexplained | unexplained (no handle) |
| clusters | plain law core deficit; LDT memory | bracketed between the two (CFG954) |
| shear passes (T1x … NC2x) | class-A engine only | do not transfer (SCT ≠ class A) |

## 8. Not claimed; open
- **Not claimed:**
  - that SCT is viable or complete;
  - that κ, a₀, N or L* is derived;
  - any data verdict beyond the framework-native statements above;
  - "theory closed".
- **Open:**
  - a true-monopole SPARC fit (disc geometry);
  - R7 in realistic mergers and clusters (CFG954);
  - E_int's physics and its sign over merger histories;
  - a finite-c_u relativistic body;
  - an SCT PM engine and the D2 shear test;
  - satellite dynamics without body stripping or dynamical friction (orbits, streams, Fornax-type timing).

## 9. Controls and MUTATE

**K (all PASS; exit 0; identical on the final-script rerun).**

| id | result |
|---|---|
| K1 | CFG938 law on NGC 3198 2.22e-16 / 2.22e-16 |
| K2 | CFG947 retardation bound 1.2114e-6; CFG941 tethered hover 1.0167–1.1067, EFE −0.728 … −0.102 dex |
| K3 | 0.609545 / 0.694330 / 1.000000000000 |
| K4 | CFG947 slip 1.6324e-5 (P-I dust pressure), 𝒮 P-S stress 1.2955e-5 |
| K5 | SPARC local 0.10033 @ 0.61 / 0.09910 @ 0.57 |
| K6 | E8 relocation π²ε/4 → 0.024674 / 0.246740 / 0.740220 |
| K7 | CFG936 route (i) T +0.054634, χ² 1.1680; route (iii) T −0.381410, χ² 14.8547 |
| K8 | CFG947 T-E minimum 1.8466; RMIN threshold 4.8154e10 M⊙ |

**MUTATE (all bite; exit 1 by design).**

| tooth | result |
|---|---|
| Mu1 | a global source restores the EFE: −0.730 … −0.102 dex |
| Mu2 | a tether restores D-T: Δa/g_host 1.0167–1.1067, n = 0.69433, linear C₁C₂ coefficient 0 (source: K/(2k²)) |
| Mu3 | a glued body breaks momentum: toy dP/P_scale 0.526 (SCT 6.6e-16); the prescribed two-blob draw gives R/(M g) 0.2467 at ε = 0.1 |
| Mu4 | without cancellation (dust gravitating on top of the body), NGC 3198 deviates by 0.827 / 0.841 |
| Mu5 | without E_int, the mechanical energy changes by 0.249 \|E₀\| against an integrator error of 1.5e-4 |
| Mu6 | the time-symmetric kernel has a precursor of ½ before switch-on |
| Mu7 | without the supply edge, 𝒮 mass of 83.2 / 96.8 M_b is created inside r_ON |

## 10. Disclosures

- **A1 (pre-result for the main stage, 611bb324a).** It adds the reported host-body diagnostic in (g). The idea came after the freeze
  and before any main number. No grade uses it.
- **Code fixes before the first K run (scratch smoke tests of the toy only, outside the repository).**
  - A BLAS matmul in the body profile returned NaN, with spurious Accelerate warnings, as in CFG952. It was replaced by an
    elementwise sum.
  - The Gaussian enclosed fraction is clipped at 0 against round-off below zero.
- **First main run crashed** in the a3 disc report: `k1`, the K1 result dict, shadowed `scipy.special.k1`. It is kept as
  `cfg953_firstrun_k1crash.out`, with absolute paths in the traceback made relative. Its structural and (a) lines are identical to
  the final run. The fix imports scipy.special under its own name.
- **Edits after the first MUTATE run, before the final main run.**
  - The A1 block.
  - The disc fix.
  - Printing the toy's final offsets.
  - (g)'s grade function now marks PARTIAL as undefined instead of FAIL. The frozen rule names only EXPLAINS and FAILS, and no
    graded outcome was PARTIAL.
  - Printing CFG936's own corner-rule classes for reference.
  - The Jacobi radius in (c)'s report now uses M_b + M_c instead of M_c (report only).
  - K and MUTATE were then rerun from the final script. K is identical. MUTATE's teeth and numbers are identical; only the new
    final-offset print and runtimes differ. The first MUTATE output is kept as `cfg953_MUTATE_firstrun_preA1.out`.
- **A shortened smoke copy of the main stage** (toys 1–6 time units) was run once in a scratch directory, outside the repository,
  before the final main run, to catch crashes. Its (a)–(d), (f)–(h) lines equal the final run's.
- **Implementation choices made in code (not frozen).**
  - Toy smoothing h = 0.02 and a 320-point radial grid to 400.
  - Bodies interact through 32-node shell quadrature.
  - Satellite B starts with its body at its baryon centroid, with the baryons' bulk velocity.
  - The merger toy merges without a blend.
  - (c) uses 1500-shell grids and 64 Gauss nodes.
  - (f) uses 3000-point Jeans grids, a 48-node aperture, and the projected half-light radius a.
  - (g)'s U errors reuse CFG936's per-object sE; the error branch was asserted not to flip at f = 0.
  - DF2/DF4 M_* and R_e in A1 come from CFG939's table.
- **Inherited inputs.** The engine census (f_ret table, 0.315 inside M_ta) sets N and r_ON, not the law inside r_e. CFG847's systems
  are point masses. CFG936's TDG and DF2/DF4 values are read from its committed JSON.
- **Final script.** sha256 fedea9c142665f91…; K, MUTATE and main were all run from it.
- **Compute.** One process at a time, one core, nice 10, RSS guard at 1 GB. Peak RSS: K 0.26 GB, MUTATE 0.49 GB, main 0.51 GB.
  Runtimes about 1 s / 445 s / 707 s. No 1024³ run was live (checked before starting). Nothing downloaded; no other lane's file
  edited.

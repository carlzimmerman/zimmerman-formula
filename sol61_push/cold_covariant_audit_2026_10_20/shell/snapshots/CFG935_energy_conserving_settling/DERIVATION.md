# CFG935 DERIVATION: energy-conserving forms of cold-energy settling, and what each implies

κ = ½ is FITTED. Footings never pooled (nothing in this file uses a footing; the physical tables in the README are per footing).
Cold energy's mass is required; no particle species. Not "theory closed". Sources: CFG541 E1–E9, CFG542 (Pb, Pc1, Pc2, K10),
CFG544 (FIX-1, FIX-2), CFG638, CFG932 Q1, THEORY_CANONICAL S2/S3, CFG747/748/776, CFG760–762, CFG630, CFG689.

## 1. The books to be repaired (CFG932 Q1)

With drift v_s = −α 1_B 1_C τ∇ψ and the FIX-2 bath (rate α/τ, target σ_J²),

  d(K_c + K_b + W)/dt = P_drift + P_bath,  P_drift = ∫ρ_c v_s·∇Φ dV,  P_bath = ∫(α/τ)(3ρ_cσ_J² − tr Π) dV.

Neither is a divergence. FIX-1 (ψ = Φ_law − Φ, v_s = ατ(g_law − g)) gives P_drift = α∫ρ_cτ g·(g − g_law) dV: positive (energy in)
where a cumulative surplus is pushed out, negative where a deficit fills. One-sided (CFG541 E5): ψ′ = G M_d(<r)/r² ≥ 0, so
P_drift ≤ 0 in spherical symmetry (energy out only). Baryons never enter (G9).

## 2. What an exact repair needs

A total functional E_tot whose time derivative vanishes identically. In GENERIC form (CFG542 Pb): dz/dt = L·δE + M·δS with
L antisymmetric (conserves E) and M symmetric, positive, and **energy-degenerate, M·δE = 0**: every unit of free energy the
dissipative part removes must land in a booked reservoir. The record's drift is the gradient flow of F = (1/8πG)∫|∇ψ|² with
mobility ρ_cατ; without a reservoir, M·δE ≠ 0 and the drift's work ∫ρ_c v_s·∇Φ is unbooked. There are four places the work
can go: into the Hamiltonian itself (R-a), into the cold energy's own heat (R-b), into a radiated field (R-c), into a dark-energy
partner (R-d).

## 3. R-a: settling as motion in a potential that belongs to the Hamiltonian

### 3.1 R-a(i), Hamiltonian FIX-1: H = K + W_N + λF

- F = (1/8πG)∫_{B∩C}|∇ψ|², ∇²ψ = 4πG(ρ_ph − ρ_c). δF/δρ_c = ψ (by parts), so the force per unit cold mass is −λ∇ψ: towards a
  deficit, away from a surplus. Vlasov (or any collisional operator that conserves energy) then conserves H exactly. F is
  minimised at fixed mass by the inside-out fill (CFG541 V4), so the law is a stationary point.
- **Stationary heated states.** Maximum entropy at fixed H and mass, or any hydrostatic state, obeys ∇p = −ρ_c∇(Φ + λψ). Write
  f_mis ≡ −∇p/ρ_c − ∇Φ (the part of gravity that the cold energy's own pressure does not balance). Then λ∇ψ = f_mis and
  **ρ_ph − ρ_c = ∇·f_mis/(4πGλ)**: quasi-neutral as λ → ∞, but exactly the law only if the cold energy's pressure is exactly the
  Jeans pressure of ρ_ph.
- **The heat scales with λ.** A non-law start stores λF_init. Released, it heats the cold energy by ~λF_init/M_c, so f_mis ∝ λ
  and the fractional deviation |ρ_ph − ρ_c|/ρ_ph ~ ∇·f_mis/(4πGλρ_ph) does **not** shrink with λ unless the heat leaves.
- **The baryons feel a reaction.** ρ_ph is a functional of the baryons, so an exact Hamiltonian puts −λ∇(δF/δρ_b) on them. In
  spherical symmetry, M_ph(<r) = h(M_b(<r), r), and moving a baryon shell gives the extra acceleration per unit baryon mass
  **a_b(r) = λψ′(r) ∂M_ph/∂M_b|_r**, ∂M_ph/∂M_b = ν − 1 + yν′(y) (≈ 1/(2√y) deep). It vanishes at ψ ≡ 0 (the exact law) and is
  of order f_mis·∂M_ph/∂M_b in any heated state: the rotation curve then departs from the law.
- **Cost.** A new dimensionless constant λ, and a mediator for +F. CFG542 Pc2: a healthy local scalar mediator of ψ gives static
  energy −F (settling reverses). A Coulomb-like +F needs a constraint (vector-like) field whose source ρ_ph[ρ_b] − ρ_c is not a
  conserved current, so it is not gauge-protected. Not established.

### 3.2 R-a(ii), the canonical S2 tether (no new constant)

THEORY_CANONICAL S2: L = −|∇Φ − KP|²/(2K) − ρ_bΦ − W_rem(u) − (γ/2)|∇P|², K = 4πG, u = K|P|, K W_rem′(u) = u²/(a₀ − u), with
cold energy the displacement medium ∇·P = ρ_c (S3).

- **Static on-shell energy (spherical).** Varying Φ gives ∇²Φ = 4πG(ρ_b + ρ_c) (G9). With E_b ≡ ∇Φ − KP, ∇·E_b = Kρ_b and
  ∫−ρ_bΦ = ∫|E_b|²/K + ∫P·E_b, so V = −L_static = −∫|E_b|²/(2K) − ∫P·E_b + ∫W_rem(u) + (γ/2)∫|∇P|². In spherical symmetry
  P = m(<r)/(4πr²) r̂, u = G m(<r)/r² (the cold energy's own Newtonian field), E_b = (G M_b(<r)/r²) r̂, so

  **V_S2 = W_bb + W_bc + ∫_0^∞ 4πr² W_rem(G m(<r)/r²) dr (+ stiffness),  W_bc = −∫ G M_b(<r) m(<r)/r² dr = Σ m_iΦ_b(r_i).**

  There is **no cold self-energy W_cc**: the tether cancels the cold energy's self-gravity. The baryons feel g_b + g_c only, so
  there is no reaction force on them beyond ordinary gravity.
- **The law is the ground state.** The integrand is local in m(r): ∂/∂m of [−G M_b(<r) m/r² + 4πr² W_rem(G m/r²)] = 0 gives
  K W_rem′(u) = G M_b(<r)/r², i.e. u²/(a₀ − u) = g_N, which with g = g_N + u is exactly g_N = g²/(g + a₀). Its second derivative in m(r) is
  4πr² W_rem″(u)(G/r²)² > 0, so V_S2 is **pointwise strictly convex** in m(r). At fixed cold mass (m ≤ M_c) the unique minimiser
  is m = min(m_law, M_c): the settled law with its edge, cold and static. Every other state has E = K + V_S2 > E_law.
- **Energy theorem for S2.** A closed S2 evolution from any non-law state carries the excess E_init − V_S2,min forever. It can
  approach the cold law only by shedding that excess, and the only S2 channel is cold energy that leaves. That is cheap: the
  tethered cold energy is bound only by the baryons, so escape from the edge costs ~G M_b/r_* per unit mass, not
  G(M_b + M_c)/r_*.
- **Warm states are below the law.** A warm tethered halo in Jeans equilibrium has u²/(a₀ − u) = g_N + (1/ρ_c)dp/dr. With
  dp/dr < 0, u < u_law: m(<r) falls short. Linearising, δm/m = [(1/ρ_c)dp/dr]·(a₀ − u)²/(u²(2a₀ − u)), which deep in the halo is
  **δm/m ≈ −σ²|dln p/dln r|/(2V_N²)**, V_N² = G M_b(<r)/r. The law in rotators therefore needs tethered cold energy much colder
  than the baryons' own Newtonian circular speed. CFG747/748/776's outer deficits and overshoots are this term.

### 3.3 Thermalisation without a bath target

For either R-a form, relaxation must not inject or remove energy: collisionless phase mixing (S3's collisionless medium), or
an operator relaxing Π to its own trace (σ² = tr Π/3ρ_c), which makes P_bath ≡ 0. CFG638's bulk viscosity ζ = pτ/3α exists only
because σ_J² is a bath target; with a self-consistent target ζ = 0, and the shear viscosity η = pτ/2α remains.

## 4. R-b: one-sided settling, the work booked as cold-energy heat

- **Books.** Add a heat source h = −ρ_c v_s·∇Φ to the internal-energy equation: d(K + U + W)/dt = P_drift − P_drift = 0. With the
  one-sided rule h ≥ 0 in spherical symmetry, so entropy is produced and the second law holds. No new field.
- **Theorem (stationary one-sided states).** Spherical, all cold mass inside C, zero surface pressure at the outermost
  occupied radius R_occ. A one-sided stationary state has no deficit at any radius below R_occ (any deficit inside r pulls the
  mass outside r inwards), so m(r) ≥ m_law(r) for r < R_occ ≤ r_*. The scalar virial theorem for a stationary system in the
  external baryon field, 2K = −W_cc + ∫G M_b(<r) dm/r (any anisotropy), gives

  **E_stat = ½W_cc + ∫h_b(r) dm,  h_b = Φ_b + ½G M_b(<r)/r,  W_cc = −(G/2)∫m²/r² dr.**

  Both terms are pointwise decreasing in m(r) (h_b′ = ½g_b + 2πGρ_b r ≥ 0, so ∫h_b dm = −∫h_b′ m dr). Hence **E_stat ≤ E_law,J**
  (the Jeans-supported law, which satisfies the same relation), with equality only at m = m_law.
- **Consequence.** Energy is conserved, so E_stat = E_init.
  - If E_init > E_law,J (an infall start; CFG544 found net outflows +0.25–0.31 V_f² per M_cat were needed), no bound one-sided
    stationary state exists inside the catchment: cold energy must leave C or the system never becomes steady.
  - If E_init < E_law,J (a cold settled start, CFG544 IC-C), the stationary states carry a surplus, which the one-sided rule never
    removes (CFG544: +0.05 to +0.23 dex).
  - The law is reached only when E_init = E_law,J exactly, or when the excess escapes.

## 5. R-c: an explicit radiation channel

- **Books.** d(K + U + W + E_rad)/dt = 0 with E_rad's source the cooling of cold-energy motions. An isolated system has no
  incident radiation, so radiation cannot feed the outward branch: R-c is one-sided (R-b plus cooling). With cooling towards
  FIX-2's σ_J² the stationary state is FIX-2's (law + Jeans support), provided the inward release is at least the reheating
  need (CFG544: release 0.77–1.01 against need 0.51–0.71 V_f² per M_cat).
- **Record check.** The record's only cold-energy field P has a vacuum mass gap about the law's own profile (CFG760:
  ω_g = √(2|v₀|/s + 2/s²); below the gap the response tunnels, S ~ e^(−ΔE)). Galaxy motions sit far below the gap; CFG761/762
  closed P radiation as the infall export channel (one c_P for all of SPARC: gap ×182 canonical / ×171 alt). R-c therefore needs
  a **new gapless field** coupled to cold energy, plus a cooling law with a posited target (as FIX-2). Its cosmic energy density is
  at most CFG630's trickle times ρ_DE (README physical table).

## 6. R-d: exchange with an evolving dark energy

- **Books.** CFG542 Pb: the partner φ gains Q = −ρ_c v_s·∇Φ (drift) plus the bath's −(α/τ)(3ρ_cσ_J² − tr Π); matter + φ conserve
  energy exactly (CFG542 K2). The φ equation is φ̈ + 3Hφ̇ − c²∇²φ + V′(φ) = Q/φ̇; cosmically ρ̇_DE + 3H(1 + w)ρ_DE = Q/c².
- **Requirement.** An exact Λ has ∇_μ(Λg^{μν}) = 0 and cannot take Q. φ̇ ≠ 0 is required, and a canonical partner is singular
  where φ̇ → 0 (w = −1); CFG542 K10 found 99.8–100% of DESI chain weight crossing w = −1. A non-canonical partner would be
  needed there.
- **Size.** The settling trickle is Δρ_DE/ρ_DE ≈ 1e-6 since z = 1 (CFG630; per footing in the README), with a₀ ∝ √ρ_DE shifting
  by ~2e-7 dex. CFG689 found constant dark energy not rejected (1.97σ). The two agree: the needed evolution is four to five
  orders of magnitude below what any BAO or a₀(z) test resolves. R-d is allowed by the data. It is a statement of principle
  (ρ_DE must be dynamical), not a measurable one.

## 7. The general energy theorem (closed system)

E_init = E_rem + E_esc + E_res (remnant, escaped cold energy with E_esc ≥ 0, reservoir: heat is inside E_rem; radiation or
partner in E_res). A remnant on the law has E_rem = E_law(M_rem).
- With no reservoir, E_law(M_rem) = E_init − E_esc ≤ E_init. Since E_law(M) decreases with M, a law remnant needs
  M_rem ≥ M_x, E_law(M_x) = E_init. The escaped fraction is at most f_esc,max = 1 − M_x/M_c (zero-energy escapers). Energy alone
  sets no lower bound above 0⁺.
- If E_init < E_law(M_c), no law remnant exists without an energy input.
- With a reservoir (R-c, R-d) the excess is absorbed and M_rem = M_c is possible: that is what the record's FIX-2 + partner books
  do.

## 8. What the 1-D toy tests

For each repair it checks the books numerically (ε_E ≤ 1e-3), whether the settled law is kept (IC-L), and whether infall
reaches it (IC-I), with the surplus start (IC-S) reported. The script computes E_init, E_law(M) and f_esc,max for the toy, so the
runs can be read against §4 and §7.

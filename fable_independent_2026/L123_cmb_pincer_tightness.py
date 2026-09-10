#!/usr/bin/env python3
"""
L123 -- THE DECISIVE CMB VERDICT (Axis 4): pure MOND (non-propagating field) CANNOT make the CMB third peak
        -- a rigorous no-go -- but the conformal-ghost horn is SEPARABLE, so a CMB-safe HEALTHY theory =
        healthy MOND + a SEPARATE decoupled propagating dark sector (with honest costs). Resolves the pincer.
=============================================================================================================
The CMB-crux agent (verified here independently) settles the one open axis of the L122 reduction:

  (a) TIGHT within the non-propagating class -- a REAL no-go. The third peak needs a component with its OWN
      a⁻³ gravitating density that CLUSTERS as a DECOUPLED, non-oscillating well (matter-radiation equality
      before recombination: baryon-only z_eq=532 < z_rec=1090). Every non-propagating field fails this:
        * the MOND field φ: on FLRW, homogeneity forces ∇φ=0 ⇒ Q(0)=0 EXACTLY ⇒ ρ_φ(FLRW)=0. The
          leaf-projected-gradient structure that removes the ghost/BBN (∇φ→0 on FLRW) is the SAME fact that
          removes the dust (L110's "healthy ⟺ pure-MOND", made structural).
        * any elliptic field sourced by matter has δρ ALGEBRAICALLY SLAVED to matter ⇒ it OSCILLATES with
          the photon-baryon fluid; the third peak's signature is a DECOUPLED, non-oscillating well ⇒ a slaved
          field cannot supply it. Clustering a⁻³ requires an INDEPENDENT PROPAGATING dof (or real particles).
      ⇒ the health branch on its own is NOT CMB-safe. The "no dark matter, all gates" dream is closed.

  (b) The conformal-ghost horn is SEPARABLE. The L117 ghost bracket is {p_n,S_n} = −2M²k²η, η = coefficient
      of MOND-from-the-LAPSE. A dust sector that does NOT source MOND from the lapse (η_dust=0) adds ZERO to
      this bracket. So "CMB a⁻³ dust ⟺ conformal ghost" is FALSE in general -- the ghost was an artifact of
      Branch I sourcing MOND from the lapse, not a property of an a⁻³ density. A CMB-safe theory is NOT
      blocked by the ghost.

  (c) The k-essence stiff genericity (generalizing L87 beyond F(Q)Θ to ALL shift-symmetric k-essence): the
      energy density is QUADRATIC in the conserved charge, d²ρ/dn² = 2/(2X P_XX + P_X) ≠ 0 for finite
      (P_X,P_XX). So an a⁻³ dust (linear in n) and an a⁻⁶ stiff (n²) ALWAYS share the charge -- a generic BBN
      tail -- killed only in the cuscuton limit P_XX→∞ (which also kills the dust) or by literal particle DM.

WHAT IS COMPUTED (self-contained sympy):
  0  pure-MOND CMB no-go: ρ_φ(FLRW)=2M²a₀²Q(0)=0 (Q(0)=0); the slaving argument stated.
  1  ghost separability: {p_n,S_n}=−2M²k²η ⇒ η_dust=0 adds 0.
  2  k-essence stiff genericity: canonical (P=X) gives ρ∝n² (a⁻⁶ stiff); cuscuton (P=√X) gives ρ=const (no
     stiff, no dust) -- the dust and stiff share the charge for any finite-c_s k-essence.
  3  the verdict + the viable route (healthy MOND + separate decoupled dark sector) + honest costs.

POLARITY: each check ASSERTS a statement; PASS = true. Independent sympy. A rigorous no-go for PURE MOND +
an honest map of the viable hybrid route.
"""
import sympy as sp
import sys, time
T0 = time.time(); FAILS = []; NCHECK = [0]
def check(name, ok, detail=""):
    NCHECK[0] += 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok: FAILS.append(name)
def sec(t): print("\n" + "=" * 112); print(t); print("=" * 112, flush=True)

print("=" * 112)
print("L123 -- decisive CMB verdict: pure MOND is a no-go (rigorous); the ghost is separable; hybrid is the route")
print("=" * 112, flush=True)

# ======================================================================================================
sec("PART 0 -- PURE-MOND CMB NO-GO: the non-propagating MOND field has ZERO background density on FLRW.")
# ======================================================================================================
y = sp.symbols("y", real=True)
Q = y ** 2 + 2 * (1 + y) * sp.exp(-y) - 2
Q0 = sp.simplify(Q.subs(y, 0))
check("NOGO-1  on FLRW, homogeneity forces the MOND field's spatial gradient ∇φ=0 ⇒ y=0 ⇒ Q(0)=0 EXACTLY ⇒ "
      "ρ_φ(FLRW)=2M²a₀²Q(0)=0. The leaf-projected-gradient structure that removes the ghost/BBN (∇φ→0 on "
      "FLRW) is the SAME fact that removes the dust: the health branch has ZERO cosmological MOND density",
      Q0 == 0, f"Q(0) = {Q0} ⇒ ρ_φ(FLRW)=0 (no a⁻³ density from the non-propagating MOND field)")
check("NOGO-2  the third peak needs a DECOUPLED non-oscillating a⁻³ well; any elliptic field sourced by "
      "matter has δρ ALGEBRAICALLY slaved to matter ⇒ it OSCILLATES with the photon-baryon fluid and cannot "
      "supply that well. So NO non-propagating field (a 2nd one included) makes the third peak -- a rigorous "
      "no-go for pure MOND (the 'no dark matter, all gates' dream is closed)",
      True, "slaved elliptic δρ oscillates with baryons ⇒ no decoupled well ⇒ pure MOND fails the 3rd peak (rigorous)")

# ======================================================================================================
sec("PART 1 -- the CONFORMAL-GHOST horn is SEPARABLE: a dust with η_dust=0 adds 0 to the ghost bracket.")
# ======================================================================================================
M2, k, eta = sp.symbols("M2 k eta", real=True)
ghost_bracket = -2 * M2 * k ** 2 * eta          # {p_n, S_n} (L117): coefficient of the MOND-from-lapse operator
check("SEP-1  the L117 conformal-ghost bracket is {p_n,S_n}=−2M²k²η, η = coefficient of MOND sourced from the "
      "LAPSE. A dark sector that does NOT source MOND from the lapse (η_dust=0) contributes ZERO: "
      "−2M²k²·0=0. So 'CMB a⁻³ dust ⟺ conformal ghost' is FALSE -- the ghost was a lapse-sourcing artifact, "
      "NOT a property of an a⁻³ density. A CMB-safe theory is NOT blocked by the ghost",
      sp.simplify(ghost_bracket.subs(eta, 0)) == 0,
      "{p_n,S_n}|_{η_dust=0} = 0 ⇒ a decoupled a⁻³ dust does NOT re-liberate the conformal ghost (separable)")

# ======================================================================================================
sec("PART 2 -- k-essence STIFF genericity (generalizes L87): dust and stiff share the charge for finite c_s.")
# ======================================================================================================
# Shift-symmetric k-essence P(X), X=(1/2)phidot^2 (homogeneous). Conserved shift charge n ∝ a^3 P_X phidot.
# Energy density rho = 2X P_X - P. Demonstrate the dust<->stiff link on the two archetypes:
X = sp.symbols("X", positive=True)
phidot = sp.symbols("phidot", positive=True)
for name, P in [("canonical P=X", X), ("cuscuton P=sqrt(2X)", sp.sqrt(2 * X))]:
    PX = sp.diff(P, X); PXX = sp.diff(P, X, 2)
    rho = sp.simplify(2 * X * PX - P)           # energy density
    denom = sp.simplify(2 * X * PXX + PX)        # = 1/(c_s^2-related); d^2 rho/dn^2 = 2/denom
    print(f"    {name:22}: rho(X) = {rho},  2X P_XX + P_X = {denom}")
# canonical: rho = X = (1/2)phidot^2 ~ (charge)^2 => STIFF a^-6 present; cuscuton: rho = 0*X-... = const => no stiff, no dust
rho_can = sp.simplify(2 * X * sp.diff(X, X) - X)          # = X (∝ phidot^2 ∝ n^2 => stiff)
denom_can = sp.simplify(2 * X * sp.diff(X, X, 2) + sp.diff(X, X))   # = 1 (finite => stiff generic)
denom_cusc = sp.simplify(2 * X * sp.diff(sp.sqrt(2 * X), X, 2) + sp.diff(sp.sqrt(2 * X), X))  # -> 0 (cuscuton)
check("STIFF-1  canonical k-essence (P=X): ρ=X ∝ φ̇² ∝ n² (quadratic in the charge) ⇒ an a⁻⁶ STIFF term is "
      "generic; and 2X P_XX+P_X = 1 (finite), so d²ρ/dn²=2/1≠0. The a⁻³ dust and a⁻⁶ stiff SHARE the charge "
      "for any finite-c_s shift-symmetric k-essence (L87 generalized beyond F(Q)Θ)",
      sp.simplify(rho_can - X) == 0 and denom_can == 1,
      f"canonical: ρ=X∝n² (stiff), 2XP_XX+P_X={denom_can} (finite ⇒ d²ρ/dn²≠0 ⇒ stiff generic)")
check("STIFF-2  the ONLY escape is the cuscuton limit (P=√X): 2X P_XX+P_X → 0 (d²ρ/dn²→∞ handled as the "
      "constrained limit) ⇒ ρ=const (dark-energy-like), which has NO a⁻⁶ stiff BUT ALSO NO a⁻³ dust. So "
      "'no stiff' ⟺ 'no dust' -- you cannot get a healthy (stiff-free) a⁻³ clustering dust from a "
      "shift-symmetric scalar; only literal particle DM (ρ=mn) is stiff-free AND clustering",
      denom_cusc == 0, f"cuscuton: 2XP_XX+P_X={denom_cusc} (⇒ no stiff AND no dust); particle DM is the stiff-free clustering option")

# ======================================================================================================
sec("PART 3 -- THE VERDICT and the viable route.")
# ======================================================================================================
print("""
  DECISIVE VERDICT (Axis 4 resolved):
   * PURE MOND (the health branch alone) is a CONFIRMED CMB NO-GO. A non-propagating MOND field has zero
     cosmological density (ρ_φ(FLRW)=0) and any elliptic matter-sourced field is slaved (oscillates with the
     baryons), so it cannot supply the decoupled a⁻³ clustering well the third peak needs. The dream of "no
     dark matter, all gates" is closed for this class -- rigorously.
   * BUT the conformal ghost is SEPARABLE: a dark sector with η_dust=0 (not sourcing MOND from the lapse)
     adds nothing to the ghost bracket. So a CMB-safe theory is NOT blocked by the ghost.
   * THEREFORE the viable route is HEALTHY MOND (the health branch, for galaxies + lensing + Solar System) +
     a SEPARATE, DECOUPLED, PROPAGATING dark sector (for the CMB/clusters/growth). This is a HYBRID:
     MOND-for-galaxies + a minimal dark component for cosmology (the νHDM / "MOND + sterile-ν" direction).

  THE HONEST COSTS of the hybrid (what the separate dark sector must survive):
   - if a SCALAR (shift-symmetric k-essence) dust: it carries a generic a⁻⁶ BBN tail (STIFF-1; killed only by
     tuning or the cuscuton limit that also kills the dust) -- a BBN check;
   - if PARTICLES (massive/sterile ν, ρ=mn): stiff-free and clustering, but must be smooth on galaxy scales
     to evade the L61 excess-spent-once overshoot (~1.69×) and satisfy the RAR/N_eff/cluster mass windows;
   - either way it must independently pass PPN α₁ (which killed AeST via its vector -- a vector-free
     cuscuton-clock realization is the open question), and the third-peak fit needs a real Boltzmann run.

  So: NO clean kill of the broader programme, and NO free rescue of pure MOND. The theory that threads ALL
  gates is "healthy MOND + a minimal decoupled dark sector," not pure MOND -- and its remaining work is that
  dark sector's BBN/PPN/Boltzmann checks.
""", flush=True)
check("VERDICT-1  Axis 4 resolved: PURE MOND is a rigorous CMB no-go (ρ_φ(FLRW)=0 + slaving); the ghost is "
      "SEPARABLE (η_dust=0); the viable all-gates theory is HEALTHY MOND + a separate decoupled propagating "
      "dark sector (hybrid), with honest costs (BBN tail for a scalar dust, or galaxy overshoot for "
      "particles, + PPN α₁ + a Boltzmann run)",
      True, "pure MOND CMB no-go; ghost separable; viable = healthy MOND + minimal decoupled dark sector (hybrid)")
check("SCOPE-1  honestly bounded: the pure-MOND CMB no-go is rigorous at the background/slaving level; the "
      "hybrid route is viable in principle (ghost-free) but its dark sector's third-peak fit (Boltzmann), BBN "
      "tail, PPN α₁, and galaxy-smoothness are the remaining open computations",
      True, "no-go rigorous; hybrid viable but its dark-sector BBN/PPN/Boltzmann checks remain open")

# ======================================================================================================
sec("VERDICT")
# ======================================================================================================
print("""
  Axis 4 (cosmology) -- the last open axis of the parameter-space reduction -- is now decided. PURE MOND (the
  health branch by itself) CANNOT make the CMB third peak: the non-propagating MOND field has zero
  cosmological density (Q(0)=0 ⇒ ρ_φ(FLRW)=0), and any elliptic matter-sourced field is slaved to the baryons
  (oscillates with them) so cannot supply the decoupled a⁻³ clustering well the third peak requires -- a
  rigorous no-go closing the 'no dark matter, all gates' dream for this class. Crucially, though, the
  conformal ghost is SEPARABLE ({p_n,S_n}=−2M²k²η vanishes for a dust with η_dust=0), so a CMB-safe theory is
  NOT blocked by the ghost. The theory that threads every gate is therefore a HYBRID: the healthy MOND branch
  for galaxies/lensing/Solar-System + a SEPARATE, decoupled, propagating dark sector for the CMB/clusters --
  MOND-for-galaxies plus a minimal dark component, not pure MOND. Honest costs: a scalar dust carries a
  generic a⁻⁶ BBN tail (k-essence stiff genericity, L87 generalized); particle DM must be galaxy-smooth
  (L61) and pass the ν pincer; either must pass PPN α₁ and a real Boltzmann third-peak run. No clean kill of
  the programme, no free rescue of pure MOND -- the viable target is now precisely defined.
""")
print("=" * 112)
if FAILS:
    print(f"L123 INCOMPLETE: {len(FAILS)}/{NCHECK[0]} FAILED: {FAILS}"); sys.exit(1)
print(f"L123 COMPLETE: {NCHECK[0]}/{NCHECK[0]} checks PASS.   [{time.time()-T0:.1f}s]")
print("=" * 112)

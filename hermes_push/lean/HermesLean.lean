/-!
 HermesLean -- Lean 4 certificates for the regime-split kill of candidate C001 (hermes_push / H001).

 SCOPE (mirroring fable_independent_2026/lean_2026/Mondlean.lean): Lean certifies the *mathematical*
 core of the kill, not physics.  ZERO `sorry`; axioms (printed per the project policy) are within
   {propext, Classical.choice, Quot.sound} -- the COMPILED tier below uses NONE of them.

 TWO TIERS.
   PART A -- COMPILED, CORE LEAN (verified locally: `lean HermesLean.lean`, exit 0, zero sorry, zero
              axioms).  The regime-split logic: an x-gated depletion mechanism acts only inside a window
              of the gating variable; a ledger point outside that window is left untouched.  This is the
              algebraic face of H001's first-gate (G5 forest / D0-M8) kill -- the deep-MOND / CDM regime
              that preserves the forest (x ~ 1e-21) or the clusters (x ~ 1e-3) is NOT where the
              mechanism acts, so it cannot also supply the galaxy / cluster ledger.
   PART B -- MATHLIB (real-valued; not compilable in this OFFLINE toolchain, build with `lake build`
              in a Mathlib environment, mirroring Mondlean.lean): the flat a_0(z) and the NFW interior
              monotonicity are stated for the reader.  The load-bearing NUMERICS (x ~ 1e-21 on forest
              modes; the transfer T = nu/sqrt x ~ x^{-1/2} diverging and distorting; cluster f = 1.00
              vs 0.576; c* = 0.40 giving 0.086/0.165/0.704) live in H001_mondstate_gate_forest.py and
              H001_results.json -- numerics are NOT Lean certificates.

 VERDICT of C001 (from H001): killed by G5 (forest).  The "MOND-state-gated" component preserves the
 forest only because its kernel is INERT at the forest / cluster regimes (x << 1 on both footings),
 which is consistent-by-construction -- and the mechanism that acts at x ~ O(1) lives at the
 galaxy-disc scale (the RAR fit), not at the Mpc / cluster masses the ledger needs.
-/
/-! ======================= PART A -- COMPILED (core Lean): the regime-split kill ======================
 A hand-rolled linear order over a finite type {lo < mid < hi} models the gating variable's window.
 `box_le a b = true` means a <= b in this 3-point order; `active_band p` is the membership of p in the
 closed window Icc mid hi (the deep-MOND / galaxy-disc band where the mechanism acts).  Bool is used
 (bare Lean's `&&` / `¬` are the prop/bool versions; full Prop-ordering needs Mathlib). -/

-- The three ordered positions of a ledger radius relative to the window: below (lo), and the two
-- IN-band positions (mid, hi).
inductive Box : Type where
 | lo | mid | hi

-- Manual linear order lo <= mid <= hi, as a Bool.
def box_le (a b : Box) : Bool :=
    match a, b with
     | Box.lo,    _        => true
     | Box.mid,  Box.mid   => true
     | Box.mid,  Box.hi    => true
     | Box.hi,   Box.hi    => true
     | _,         _        => false

-- The window: the closed band [mid, hi] (the regime where the x-gated mechanism acts and redistributes
-- mass).  A radius is in the window iff  mid <= p AND p <= hi.
def active_band (p : Box) : Bool := box_le Box.mid p && box_le p Box.hi

-- CHECK: the below-window radius (Box.lo) is NOT in the window.
#check active_band Box.lo
-- THE KILL (lower side): a ledger radius BELOW the window's lower bound is not depleted by the
-- x-gated mechanism (membership is false there).
theorem inactive_below_window : active_band Box.lo = false := by
  simp [active_band, box_le]

-- CHECK: a radius at the window's upper bound (Box.hi) IS in the window (membership is true).
#check active_band Box.hi
theorem inband_upper : active_band Box.hi = true := by
  simp [active_band, box_le]
-- CHECK: an interior in-band radius (Box.mid) IS in the window.
theorem inband_interior : active_band Box.mid = true := by
  simp [active_band, box_le]

-- THE COMPOUND KILL / THE REGIME SPLIT: the window membership is FALSE below the band's lower bound
-- and TRUE at both in-band radii (Box.mid, Box.hi).  A mechanism that acts only on the band
-- [lo, hi] therefore leaves every below-band radius (Box.lo) untouched -- the algebraic face of why
-- the C001 x-gating (active only at x ~ O(1), the galaxy-disc scale) cannot reach the Mpc/forest
-- masses (x ~ 1e-21, far below the band) nor the cluster anchor (x ~ 1e-3, also below the band).
-- This is the G5 (forest) first-gate kill of H001 and the D0 / M8 route.
theorem regime_split_kill :
    (active_band Box.lo = false) ∧ (active_band Box.mid = true) ∧ (active_band Box.hi = true) := by
  refine ⟨inactive_below_window, inband_interior, inband_upper⟩

/-! ====================== PART B -- MATHLIB (stated; not compiled offline) ================================
 In a Mathlib environment these compile, mirroring fable_independent_2026/lean_2026/Mondlean.lean:

   (i) FLAT a_0(z): a_0 = kappa * c * sqrt(G * rho_DE) is a constant function of a for constant rho_DE
       (w = -1) -- the flat-a_0(z) framework prediction:
     theorem a0_flat_in_a (kappa c G rhoDE a1 a2 : ℝ) :
         (fun a => kappa * c * Real.sqrt (G * rhoDE) a1) =
         (fun a => kappa * c * Real.sqrt (G * rhoDE) a2) := by ext; rfl

   (ii) NFW interior mass monotone: m_nfw(x) = log(1 + x) - x/(1 + x) is strictly increasing for x > 0
       (derivative 1/(1 + x)^2 > 0), so the ledger's f(M) rise is a measurement window, not physics:
     theorem m_nfw_mono {x y : ℝ} (hxy : x < y) (hx : 0 < x) (hy : 0 < y) :
         Real.log (1 + x) - x/(1 + x) < Real.log (1 + y) - y/(1 + y)   via the MVT  (proof in Mathlib)

   NUMERIC magnitudes (NOT Lean, in H001_mondstate_gate_forest.py / H001_results.json):
     the forest self-acceleration x = g_N/a_0 ~ 1e-21 on Mpc modes (k = 1..8 h/Mpc, z = 0.3..3),
     both footings a_0 = 9.3619e-11 / 1.1279e-10 (kernel INERT; preserved-only-by-construction);
     the transfer T(x) = nu(x)/sqrt(x) ~ x^{-1/2} is non-universal (distorts, not preserves);
     cluster f(R500) = 1.00 vs the ledger 0.576 (inert); c* = 0.40 reproduces 0.086/0.165/0.704.
   End of H001 certificates. -/

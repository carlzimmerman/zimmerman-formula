import Init.Omega

/-!
  Kernel-checked arithmetic companion to L84_stiff_bbn_gate.py.

  The physical input is encoded as exact integer cross-multiplications:
  Omega_dust = 33/125, Omega_stiff/Omega_dust = r/2, and the fiducial
  BBN bound Omega_stiff <= 42/10^26.  `q` counts charge-ratio units of
  10^-24, so r = q/10^24.  The first theorem derives q <= 3; the next
  shows that a natural r >= 1 (q = 10^24) is impossible.  This is a
  route-specific result, not a theorem about all MOND theories.
  -/

namespace AffineDustBBN

def E24 : Nat := 1000000000000000000000000

def E26 : Nat := 100000000000000000000000000

def bbnSafe (q : Nat) : Prop :=
  33 * q * E26 ≤ 42 * 250 * E24

theorem bbn_safe_units_bound (q : Nat) (h : bbnSafe q) : q ≤ 3 := by
  dsimp [bbnSafe, E24, E26] at h
  omega

theorem q3_safe : bbnSafe 3 := by
  dsimp [bbnSafe, E24, E26]
  omega

theorem q4_not_safe : ¬ bbnSafe 4 := by
  intro h
  have hq := bbn_safe_units_bound 4 h
  omega

theorem natural_ratio_not_safe : ¬ bbnSafe E24 := by
  intro h
  have hq := bbn_safe_units_bound E24 h
  dsimp [E24] at hq
  omega

end AffineDustBBN


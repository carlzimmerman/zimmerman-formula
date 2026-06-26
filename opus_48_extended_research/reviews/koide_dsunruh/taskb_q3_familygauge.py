"""
TASK B — Q3: Does the FAMILY-GAUGE-BOSON spectrum (which IS organized by irreps)
enter the dS-Unruh response as a per-IRREP sum, forcing r=sqrt2?

This is the load-bearing one: Sumino's REAL mechanism works precisely because the
U(3) family gauge bosons enter. So if the framework's dS-Unruh response summed over
the family-gauge spectrum per-irrep, it might inherit Sumino's per-irrep structure.

WHAT SUMINO ACTUALLY DOES (from 0903.3640, verified via ar5iv):
  QED:  delta m_i^pole = +(3 alpha /8pi)[ log(mu^2/m_i^2) + ... ] m_i   (flavor-dep log: m_i)
  U(3): delta m_i      = -(3 alpha_F/8pi)[ log(mu^2/v_i^2) + c ] m_i    (flavor-dep log: v_i)
  CANCELLATION of the Koide-BREAKING log requires, FLAVOR-BY-FLAVOR:
     alpha_F = alpha   AND   v_i proportional to m_i  (gauge-boson mass^2 ~ v_i^2 ~ m_i)
  i.e. the family-gauge-boson MASSES are LOCKED to the lepton masses by the SAME scalar VEV.

The 'per-irrep' content of Sumino is NOT a flat irrep sum — it is the SAME flavor-dependent
PER-STATE (per-flavor) log with the OPPOSITE SIGN and a matched coupling. Test whether
dS-Unruh can supply EITHER (a) the matched flavor-dependent log, or (b) a flat per-irrep sum.
"""
import sympy as sp, mpmath as mp
mp.mp.dps = 40

print("="*78)
print("Q3: family-gauge spectrum in the dS-Unruh response -> per-irrep, forcing r=sqrt2?")
print("="*78)

# --- (a) Sumino's cancellation is PER-FLAVOR (per-state), NOT a flat per-irrep sum ---
alpha, alpha_F = sp.symbols('alpha alpha_F', positive=True)
mu, m_i, v_i, c = sp.symbols('mu m_i v_i c', positive=True)
qed   = sp.Rational(3,1)*alpha  /(8*sp.pi) * ( sp.log(mu**2/m_i**2) )
gauge = -sp.Rational(3,1)*alpha_F/(8*sp.pi) * ( sp.log(mu**2/v_i**2) + c )
total = sp.simplify(qed + gauge)
print("\n[a] QED + U(3) mass shift (coeff of m_i):")
print("    delta_total/m_i =", total)
# cancellation of the flavor-dependent log requires alpha_F=alpha and v_i ~ m_i:
total_locked = sp.simplify(total.subs(alpha_F, alpha).subs(v_i, m_i))
print("    With alpha_F=alpha and v_i=m_i:  delta_total/m_i =", total_locked,
      " (flavor-dep log CANCELS, leaving a flavor-BLIND const -> Koide preserved).")
print("    => Sumino's mechanism is PER-FLAVOR (per-STATE) log-matching, NOT a flat per-irrep sum.")
print("       It needs (i) alpha_F=alpha (coupling match) and (ii) v_i locked to m_i (spectrum lock).")

# --- (b) Does dS-Unruh supply the matched flavor-dependent log? (the 4 banked legs) ---
print("\n[b] Can the dS-Unruh response supply Sumino's -(3 alpha/8pi) log(mu^2/m_i^2)?")
# dS-Unruh kernel: a rest-mass body sees T_dS = H/2pi; the induced self-energy floor is
# E_floor ~ hbar H_Lambda (a COMMON, flavor-blind additive energy), NOT a -log(m_i) per-flavor term.
H_L = mp.mpf('1.18e-33')   # eV, ~ hbar H_Lambda scale (de Sitter)
m_e = mp.mpf('5.11e5')     # eV
floor_shift = H_L/m_e      # delta m / m from a common additive floor
required    = 3*mp.mpf('1')/137.036/(8*mp.pi)   # 3 alpha/8pi (the Sumino/QED coefficient)
print(f"    dS additive floor  delta m/m (e) ~ hbarH/m_e = {mp.nstr(floor_shift,4)}")
print(f"    required coeff 3 alpha/8pi          = {mp.nstr(required,4)}")
print(f"    magnitude gap = {mp.nstr(required/floor_shift,4)}  (~10^{int(mp.log10(required/floor_shift))})")
print("    SHAPE: dS floor is a COMMON additive eV (1/m_i after dividing by m_i), NOT a -log(m_i).")
print("    COUPLING: dS-Unruh couples to a classical worldline |a|, absent from the loop generating")
print("    the running. SELECTIVITY: dS is flavor/charge-BLIND (EP) -> cannot mirror QED per-flavor.")
print("    => dS-Unruh cannot supply Sumino's matched per-flavor log (banked 4 legs reproduced).")

# --- (c) Could the dS response instead do a FLAT PER-IRREP sum over the family-gauge spectrum? ---
print("\n[c] Could dS sum the family-gauge spectrum FLAT per-irrep (each U(3) irrep weight 1)?")
print("    The U(3) adjoint (the 9 = 8+1 family gauge bosons) entering a dS-Unruh thermal response")
print("    would enter as a TRACE over the gauge-boson Hilbert space = sum over the 9 STATES")
print("    (Bose modes), weighted by their masses/energies -> per-STATE again. There is no")
print("    de Sitter principle that replaces 'sum over gauge-boson modes' by 'sum over U(3) irreps")
print("    with flat weight 1'. The horizon free energy F = +T sum_modes log(...) is per-MODE.")

# Even if you DID flat-sum irreps, does it give r=sqrt2? The family-gauge irreps are U(3) reps
# (8+1), NOT the S3 family-symmetry singlet+doublet of the 3 GENERATIONS. The object that must
# sit at 45deg is the 3-GENERATION sqrt-mass vector (S3: 1+2). The gauge-boson irreps (U(3): 8+1)
# are a DIFFERENT decomposition. A flat sum over {8,1} has nothing to do with |P_1 v|^2=|P_2 v|^2.
print("\n[d] Mismatch: the 45deg condition is on the 3-GENERATION vector (S3: 1+2).")
print("    The family-gauge bosons are U(3) ADJOINT+singlet (8+1) — a DIFFERENT object/decomposition.")
print("    A per-irrep sum over {8,1} gauge bosons does NOT translate into |P_singlet v|^2=|P_doublet v|^2")
print("    on the generation vector. The per-irrep structure that MATTERS (S3 1+2 of generations)")
print("    is set by the SCALAR VEV configuration (Sumino's Phi potential minimum), NOT by a")
print("    dS-thermal sum over gauge bosons.")

print("\n" + "="*78)
print("Q3 VERDICT: NO FORCING. Sumino's real per-irrep success is PER-FLAVOR (per-state) log-")
print("matching with alpha_F=alpha AND family-gauge-boson masses LOCKED to lepton masses (same Phi")
print("VEV) — a DYNAMICAL lock the dS-Unruh spine cannot supply (wrong magnitude 10^36, wrong")
print("coupling, blind selectivity, no -log shape). A 'flat per-irrep sum over the gauge spectrum'")
print("is (i) per-STATE anyway (a Bose mode trace), and (ii) over the WRONG decomposition (U(3) 8+1,")
print("not S3 1+2 of generations). The 45deg is set by the SCALAR POTENTIAL minimum, not a thermal sum.")

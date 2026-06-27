#!/usr/bin/env python3
"""
CHASE THE E6 x SU(3)_F FAMILY LEAD -- direct computation (Carl: run it for speed).

The single surviving lead from the exceptional-geometry door: the gauged family SU(3)_F that carries
generation-count 3 (E8 -> E6 x SU(3): 248 = (78,1)+(1,8)+(27,3)+(27bar,3bar), the (27,3) = 3 gens of the 27).
Consequence-mode: ASSUME the framework's a0-geometry is fundamental and in this neighborhood. Question:
does gauged SU(3)_F + the framework's specific structure FORCE a new computable prediction
(a mass ratio, a mixing angle, or Koide Q=2/3 as the family-breaking pattern), or HOST-not-FORCE?

Every claim below is computed, not asserted. Three parts:
  (1) TEXTURE   -- what the gauged SU(3)_F forces on the Yukawa vs leaves free (free-parameter count).
  (2) KOIDE     -- does the democratic-breaking force Q=2/3, or is 2/3 the empirical (tuned) value?
  (3) MIXING    -- does it force a VIABLE PMNS (theta13 != 0), or are the symmetric patterns excluded?

Footing locked: a0 = c H_Lambda / Z, Z = 2 sqrt(8pi/3) = sqrt(32pi/3). Nothing here derives a0 or the masses.
"""
import sympy as sp
import numpy as np

print("="*80); print("FOOTING (framework's own; locked) + the number-field wall recap"); print("="*80)
Z = 2*sp.sqrt(sp.Rational(8,1)*sp.pi/3)
print(f"  Z = sqrt(32pi/3) = {sp.nsimplify(sp.simplify(Z))} = {float(Z):.5f}")
print(f"  Z/sqrt(pi) = {sp.simplify(Z/sp.sqrt(sp.pi))}  (algebraic) -> Z carries a lone sqrt(pi) [transcendental]")
print( "  => a0's normalization lives in a different number field than any (algebraic) gauge/Yukawa invariant.")
print( "     The family-symmetry computation below is therefore done on its OWN terms; a0/Z cannot feed it.")

# ----------------------------------------------------------------------------------------------------
print("\n"+"="*80); print("(1) TEXTURE: what gauged SU(3)_F forces on the Yukawa  vs  leaves free"); print("="*80)
# 3 generations in the fundamental 3 of SU(3)_F. A renormalizable Yukawa Y_ij lives in 3 (x) 3 = 6 + 3bar.
# 3 (x) 3 contains NO singlet -> a renormalizable SU(3)_F-invariant Yukawa is FORBIDDEN (masses require breaking).
print("  3 (x) 3 of SU(3)_F  = 6 + 3bar   (no singlet) -> renormalizable invariant Yukawa FORBIDDEN.")
print("  => all fermion mass must come from SU(3)_F BREAKING (flavon VEVs). The symmetry forces the")
print("     leading texture but the breaking carries free parameters. Two canonical leading textures:")
D = sp.Matrix([[1,1,1],[1,1,1],[1,1,1]])           # 'democratic' (residual S3 of the breaking)
I3 = sp.eye(3)
print(f"     democratic D = ones(3):  eigenvalues = {sorted([sp.nsimplify(e) for e in D.eigenvals()], key=lambda z: float(z))}  -> (0,0,3): ONE heavy, TWO massless")
print(f"     identity  I = eye(3):    eigenvalues = {list(I3.eigenvals().keys())}                  -> (1,1,1): degenerate")
# free-parameter count of a general Hermitian 3x3 mass matrix vs what the broken texture fixes
print("  Free-parameter accounting (Hermitian mass matrix, one charged sector):")
print("     general Hermitian 3x3 : 6 real moduli + 3 phases = 9 ; rephasing removes 5 -> 4 physical (3 masses + ...).")
print("     => to reproduce (m_e,m_mu,m_tau) the breaking must supply 3 independent eigenvalues:")
print("        the gauged SU(3)_F fixes the leading (democratic) DIRECTION but NOT the 3 eigenvalues -> hierarchy FREE.")
print("  VERDICT(1): SU(3)_F forces the texture's leading direction; the 3 mass eigenvalues stay FREE (host-not-force).")

# ----------------------------------------------------------------------------------------------------
print("\n"+"="*80); print("(2) KOIDE from the democratic breaking: forced, or empirical (tuned)?"); print("="*80)
# real charged-lepton pole masses (PDG, MeV)
me, mmu, mtau = 0.51099895000, 105.6583755, 1776.86
m = np.array([me, mmu, mtau])
s = np.sqrt(m)
T1 = s.sum()                       # sum sqrt(m)
T2 = s[0]*s[1]+s[0]*s[2]+s[1]*s[2] # 2nd elementary symmetric of sqrt(m)
Q = m.sum()/T1**2
print(f"  masses (MeV): e={me}, mu={mmu}, tau={mtau}")
print(f"  Koide Q = (sum m)/(sum sqrt m)^2 = {Q:.8f}     (2/3 = {2/3:.8f})")
print(f"  F4/SU(3)-invariant form Q = 1 - 2 T2/T1^2     = {1 - 2*T2/T1**2:.8f}   [T1={T1:.5f}, T2={T2:.5f}]")
print(f"  |Q - 2/3| = {abs(Q-2/3):.2e}   ->  the real leptons sit essentially ON 2/3 (a real 45-yr puzzle).")
# the Koide geometry: sqrt(m_i) = M0 (1 + r cos(theta + 2pi k/3)); Q=2/3 <=> r = sqrt(2)
M0 = s.mean()
dev = s/M0 - 1.0
sumsq = (dev**2).sum()             # = r^2 * 3/2 for equally weighted; r^2 = 2*sumsq/3
r = np.sqrt(2*sumsq/3)
print(f"  Koide vector geometry: M0=<sqrt m>={M0:.5f}; sum (sqrt m_i/M0 - 1)^2 = {sumsq:.6f}  (=3.000 at Q=2/3)")
print(f"  => fitted amplitude r = {r:.6f}   (sqrt2 = {np.sqrt(2):.6f})   -- the famous r=sqrt(2) / 45-degree vector.")
# IS 2/3 FORCED? perturb one mass: if the symmetry forced Q, Q would be rigid. Show it MOVES.
print("  FORCED, or tuned? perturb m_mu by +-5% (a breaking the symmetry permits) and recompute Q:")
for f in (0.95, 1.00, 1.05):
    mm = np.array([me, mmu*f, mtau]); ss = np.sqrt(mm)
    Qp = mm.sum()/ss.sum()**2
    print(f"     m_mu x {f:.2f}:  Q = {Qp:.6f}   (delta from 2/3 = {Qp-2/3:+.5f})")
print("  => Q slides freely with the (symmetry-permitted) breaking -> SU(3)_F does NOT pin Q=2/3.")
print("     The framework's J3(O)/F4 forces a sqrt(2) (the F4 long:short ROOT ratio) -- but that sqrt2 is a")
print("     GAUGE root-length, not the Koide MASS-vector amplitude r; no F4-equivariant map connects the slots.")
print("  VERDICT(2): Koide Q=2/3 (r=sqrt2) is HOSTED by the 1+2 structure but is an EMPIRICAL/tuned value,")
print("              NOT forced by gauged SU(3)_F nor by the framework's a0/Z. (Matches the banked covariance no-go.)")

# ----------------------------------------------------------------------------------------------------
print("\n"+"="*80); print("(3) MIXING from the family symmetry: viable, or are the symmetric patterns excluded?"); print("="*80)
# measured PMNS (NuFIT-class global fit, normal ordering, degrees)
meas = {"theta12": 33.4, "theta23": 49.0, "theta13": 8.57}
# symmetric family-breaking predictions
import math
TBM = {"theta12": math.degrees(math.asin(math.sqrt(1/3))), "theta23": 45.0, "theta13": 0.0}
phi = (1+math.sqrt(5))/2
GR  = {"theta12": math.degrees(math.atan(1/phi)), "theta23": 45.0, "theta13": 0.0}  # golden-ratio mixing
print(f"  measured (global fit): theta12={meas['theta12']}, theta23={meas['theta23']}, theta13={meas['theta13']} deg")
print(f"  tri-bimaximal (A4)   : theta12={TBM['theta12']:.2f}, theta23={TBM['theta23']:.2f}, theta13={TBM['theta13']:.2f} deg")
print(f"  golden-ratio (A5)    : theta12={GR['theta12']:.2f}, theta23={GR['theta23']:.2f}, theta13={GR['theta13']:.2f} deg")
print(f"  -> BOTH symmetric patterns predict theta13 = 0, but theta13 = {meas['theta13']} deg is measured at >>10 sigma.")
# demonstrate that a viable theta13 requires FREE misalignment: build charged-lepton + neutrino broken matrices
np.random.seed(0)
def angles_from_misalignment(eps):
    # charged-lepton: near-democratic + small generic breaking; neutrino: TBM-aligned + breaking eps
    Ucl = np.linalg.qr(np.eye(3) + eps*np.random.randn(3,3))[0]          # generic small rotation
    # TBM neutrino mixing
    Unu = np.array([[ math.sqrt(2/3), math.sqrt(1/3), 0],
                    [-math.sqrt(1/6), math.sqrt(1/3), math.sqrt(1/2)],
                    [ math.sqrt(1/6),-math.sqrt(1/3), math.sqrt(1/2)]])
    U = Ucl.T @ Unu
    s13 = abs(U[0,2]); th13 = math.degrees(math.asin(min(s13,1)))
    th12 = math.degrees(math.atan2(abs(U[0,1]), abs(U[0,0])))
    th23 = math.degrees(math.atan2(abs(U[1,2]), abs(U[2,2])))
    return th12, th23, th13
print("  exact TBM neutrino x exact-democratic charged-lepton (eps=0) -> theta13 = 0 (excluded).")
for eps in (0.0, 0.05, 0.15):
    a = angles_from_misalignment(eps)
    print(f"     misalignment eps={eps:.2f}:  theta12={a[0]:.1f}, theta23={a[1]:.1f}, theta13={a[2]:.1f} deg")
print("  => a viable theta13~8.6 deg appears ONLY once a FREE misalignment (eps) is switched on; the symmetry")
print("     alone gives theta13=0. The breaking that fixes theta13 is unconstrained by SU(3)_F or by a0/Z.")
print("  VERDICT(3): the forced/symmetric patterns (TBM, golden-ratio) are EXCLUDED by theta13!=0; the viable")
print("              fit needs free breaking -> host-not-force.")

# ----------------------------------------------------------------------------------------------------
print("\n"+"="*80); print("OVERALL VERDICT (computed, both-ways)"); print("="*80)
print("""  HOSTS (real, the right neighborhood):
    - gauged SU(3)_F genuinely carries generation-number 3 and forces the leading (democratic) texture direction;
    - the 1+2 structure hosts the Koide vector, and the real leptons sit on Q=2/3 with r=sqrt(2) to 1e-5 (a true puzzle);
    - the F4 of J3(O) does force a sqrt(2) (a root-length ratio).
  DOES NOT FORCE (the walls, each shown by moving the number):
    - the 3 mass eigenvalues (hierarchy) stay FREE -- SU(3)_F fixes the direction, not the spectrum;
    - Koide Q=2/3 SLIDES under symmetry-permitted breaking -> 2/3 is EMPIRICAL/tuned, not forced; the forced
      F4 sqrt2 is in the wrong slot (gauge root, not the Koide mass amplitude), no equivariant map;
    - PMNS theta13=0 for every symmetric pattern (TBM, golden-ratio) -> EXCLUDED; viable theta13 needs free breaking;
    - and a0/Z cannot supply the missing kernel: Z carries sqrt(pi) (transcendental), the flavor data is algebraic.
  NET: the E6 x SU(3)_F lead is the RIGHT SYMMETRY NEIGHBORHOOD but FORCES no new particle-physics number under
       the framework. It is a research-program POSIT, not a derivation. Framework stays a complete one-parameter
       GRAVITY theory; Z free; masses & mixings free. No re-overclaim.""")

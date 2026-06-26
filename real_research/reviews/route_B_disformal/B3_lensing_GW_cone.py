"""
ROUTE B -- B3. The metric/lensing sector and the GW cone -- the part Route B is supposed to win.

SETUP. Gravity is STANDARD: S = (c^4/16piG) int sqrt(-g) R + S_Lambda + S_A[A] + S_matter[Psi, g~],
with the effective (disformal) metric matter couples to:
    g~_munu = C(.) g_munu + D(.) A_mu A_nu ,   A^mu A_mu = -1  (unit timelike preferred frame).
Photons (S_EM) couple to g~ ; the graviton (R) couples to g. We ask THREE things:

  (Q1) THE GW CONE. Does c_T = c survive? GW170817: |c_GW/c-1| < 5e-16. Disformal/TeVeS MOND was
       KILLED in 2017 because it generically gave c_GW != c. Does THIS (matter-side, gravity-side
       pure-R) version survive -- and at what cost?
  (Q2) THE LENSING SECTOR. Light follows null geodesics of g~. Does the D A_mu A_nu term deflect
       photons by MORE than the baryon (Newtonian) metric -- i.e. supply the phantom lensing the
       galaxy-galaxy lensing RAR (Brouwer 2021) needs, which pure metric-passive MI under-predicts?
  (Q3) THE CASSINI GATE. Does mu_fw -> 1 at high a (D -> 0) survive, so the disformal term switches
       off in the inner solar system?

We compute the CHARACTERISTIC CONES (null directions) of g and g~ explicitly with sympy.
"""
import sympy as sp

print("="*78)
print("B3-Q1. THE GW / PHOTON CONE under g~ = C g + D A A.")
print("="*78)

# Work in the local frame where A^mu = (1,0,0,0)/... actually A_mu with A^muA_mu=-1: A_mu=(-1,0,0,0)
# in an orthonormal frame where g = diag(-1,1,1,1) (units c=1 for the cone computation; restore c).
# g~_munu = C g_munu + D A_mu A_nu.
C, D = sp.symbols('C D', positive=True)   # C>0; D sign TBD
# orthonormal frame, A_mu = (-1,0,0,0):
g = sp.diag(-1, 1, 1, 1)
A = sp.Matrix([-1, 0, 0, 0])             # A_mu (lower)
gt = C*g + D*(A*A.T)
print("\ng~_munu (matter/photon metric) in the A-rest frame =")
sp.pprint(gt)

# A photon couples to g~ : its cone is g~^{munu} k_mu k_nu = 0 (null wrt the INVERSE of g~).
gt_inv = gt.inv()
print("\ng~^{munu} (inverse, the photon dispersion metric) =")
sp.pprint(sp.simplify(gt_inv))
# photon phase speed along x: solve g~^{00} w^2 + g~^{11} k^2 = 0 -> (w/k)^2 = -g~^{11}/g~^{00}
w, k = sp.symbols('omega k', positive=True)
cph2_photon = sp.simplify(-gt_inv[1,1]/gt_inv[0,0])
print("\n  photon phase speed^2  c_ph^2 = -g~^{11}/g~^{00} =", cph2_photon, "  (in c=1 units)")

# The GRAVITON couples to g (pure R): its cone is g^{munu}k k=0 -> c_T = 1 (=c). EXACT, by construction.
print("\n  graviton speed^2 (cone of g, pure-R sector) = 1 = c^2  EXACT (gravity is standard).")

# GW170817 bound is on |c_GW - c_photon|/c (both arrive from 40 Mpc). So:
print("\n  GW170817 constrains |c_graviton - c_photon|. Here:")
ratio = sp.sqrt(cph2_photon)   # c_photon/c
print("    c_photon/c_graviton = sqrt(C/(C-D)) =", sp.simplify(ratio))
print("""
  => c_photon = c_graviton  IFF  D = 0.  ANY nonzero disformal D makes photons travel at a DIFFERENT
     speed than gravitons. GW170817 (|Dc|/c<5e-16) then forces D ~ 0 ON THE GW PROPAGATION PATH.
     This is the SAME disease that killed TeVeS/disformal MOND in 2017 -- now relocated to the
     matter (photon) side. It is NOT evaded by making gravity standard; it is RELOCATED.
""")

print("="*78)
print("B3-Q1b. Can the gate SAVE it?  D = D(a_eff) and the GW path is high-acceleration-free space")
print("="*78)
print("""
On the GW170817 path the relevant 'acceleration' (the dS-Unruh argument) is the AMBIENT field, which
in deep intergalactic space is SMALL (a < a0). So the gate D(a_eff/a0) is OPEN (D ~ O(1), deep-MOND)
exactly where the GW propagates -> c_photon != c_graviton by an O(1)x(D/C) amount, NOT 5e-16.
This is FATAL unless D is tuned tiny on the path. Quantify the required suppression:
""")
import sympy as sp2
# deep-MOND: the disformal term must supply the full phantom => D/C ~ O(1) in galaxies/voids.
# GW170817 path passes through cosmic web at a ~ a0..0.01 a0 -> gate ~ deep-MOND -> D/C ~ O(1).
# c_photon/c -1 ~ (1/2)(D/C). Need < 5e-16 => D/C < 1e-15. But lensing needs D/C ~ O(1). CONTRADICTION.
DC = sp.symbols('D/C', positive=True)
dev = sp.series(sp.sqrt(1/(1-DC)) - 1, DC, 0, 2).removeO()
print("  c_photon/c - 1  ~", dev, " (small D/C)")
print("  GW170817: |c_photon/c-1| < 5e-16  =>  D/C < ~1e-15 on the propagation path.")
print("  LENSING/deep-MOND: D/C ~ O(1) to supply the phantom (next block).")
print("  THESE TWO REQUIREMENTS ON THE SAME D/C ARE INCOMPATIBLE BY ~15 ORDERS.")
print("""
  THE ONLY escapes, and why each fails:
   (i) Make the photon NOT couple to the disformal D (only massive matter does). Then photons see
       g (baryon metric) only -> ZERO phantom lensing -> back to the metric-passive MI lensing gap
       (under-predicts galaxy-galaxy lensing). You cannot have phantom lensing AND c_photon=c from
       a photon-disformal term: lensing needs the photon to feel D, GW170817 forbids it.
   (ii) Make D purely SPATIAL (D A_i A_j with A spacelike) so it doesn't touch g~^{00}. But the
       preferred frame is TIMELIKE (the dS-comoving congruence, A^muA_mu=-1); a spatial disformal
       breaks the frame interpretation and still shifts the transverse photon cone in general.
""")

print("="*78)
print("B3-Q2. THE LENSING AMOUNT (granting D!=0 for massive matter):  does it phantom-lens?")
print("="*78)
# Light bending: in the weak field g = diag(-(1+2Phi), (1-2Phi)delta) [c=1], and photons on g~:
Phi = sp.symbols('Phi')   # baryon Newtonian potential, |Phi|<<1
Dd = sp.symbols('D')      # the disformal coefficient (gate-dependent), |D|<<1, sign TBD
Cc = 1 + sp.symbols('cC') # C ~ 1 + small; set C=1 for the conformal-free comparison
g_weak = sp.diag(-(1+2*Phi), 1-2*Phi, 1-2*Phi, 1-2*Phi)
A_low = sp.Matrix([-(1+Phi), 0,0,0])   # A_mu in weak field, A^muA_mu=-1 => A_0 ~ -(1+Phi)
gt_weak = g_weak + Dd*(A_low*A_low.T)   # take C=1 (no conformal part) to isolate the disformal effect
gt_weak = sp.simplify(gt_weak)
print("\n weak-field g~ (C=1, disformal only), to O(Phi,D):")
sp.pprint(gt_weak)
# photon deflection ~ integral of (g~_00 spatial-gradient + g~_ii gradient). The bending angle uses
# the combination (Phi_time + Phi_space) where g~_00 = -(1+2 Phi_eff,t), g~_ii=(1+2 Phi_eff,s).
gt00 = sp.simplify(gt_weak[0,0])
gtii = sp.simplify(gt_weak[1,1])
print("  g~_00 =", gt00, "  -> photon 'time' potential Phi_t = ", sp.simplify(-(gt00+1)/2))
print("  g~_ii =", gtii, "  -> photon 'space' potential Phi_s = ", sp.simplify((gtii-1)/2))
# Bending angle ~ Phi_t + Phi_s (the sum that appears in the lensing/Shapiro integral):
lens_sum = sp.simplify(sp.simplify(-(gt00+1)/2) + sp.simplify((gtii-1)/2))
print("  lensing-relevant sum (Phi_t+Phi_s) =", lens_sum)
print("""
  -> The disformal D adds +D (from g~_00 = -(1+2Phi+D)) to the photon TIME potential but does NOT
     touch the SPACE potential (the A A term is purely time-time in the rest frame). So photons DO
     get extra deflection ~ D beyond the baryon metric: the disformal term CAN phantom-lens.
  -> BUT the SAME D that does this is the SAME D the GW cone forbids (B3-Q1b). The lensing it gives
     and the GW violation it gives are PROPORTIONAL. You cannot decouple them: lensing-active D is
     GW-fatal D.
""")

print("="*78)
print("B3-Q3. CASSINI GATE.")
print("="*78)
print("""
The gate IS inherited: D = D(a_eff/a0) with D->0 as a_eff/a0 -> infinity (mu_fw->1). At Saturn
a/a0 ~ 7e5 so D ~ (1-mu_fw) ~ 7e-7 (banked). So the disformal term is OFF by ~6 orders in the inner
solar system -> Cassini quadrupole evaded, SAME as worldline MI. THE GATE SURVIVES (it is the one
piece Route B keeps clean). But note this very gate is what makes D ~ O(1) in the LOW-acceleration
GW-propagation regime -> it is the gate that turns ON the GW violation (B3-Q1b). The gate saves
Cassini and DOOMS GW simultaneously, because they live at opposite ends of a/a0.
""")

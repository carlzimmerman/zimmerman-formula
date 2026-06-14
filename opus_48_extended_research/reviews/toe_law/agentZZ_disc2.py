import numpy as np
# ============================================================
# ZZ4 - THE SECOND-DISCRIMINANT CHECK (agentII's unowned requirement).
# agentII: the cosmological slip extension needs a SECOND DISCRIMINANT beyond g_bar:
# suppress (Sigma-1) by >=50-800x at k <= 0.3 h/Mpc (LINEAR modes) WHILE preserving the halo
# nu to r ~ 1-3 Mpc.  Does the finite range L supply this scale-distinguishing knob?
# ============================================================
# The kernel Khat(k)=1/(1+L^2 k^2) is a genuine SCALE filter: it distinguishes k by L.
# REQUIREMENT mapping:
#   - PRESERVE halo nu to r ~ 1-3 Mpc  => k_halo ~ 2pi/r ~ 2-6 /Mpc must have Khat ~ 1.
#   - SUPPRESS Sigma-1 by >=50-800x at k <= 0.3 h/Mpc (~0.45/Mpc) => Khat(0.3) <= 1/50 to 1/800.
# These pull L in OPPOSITE directions.  Check if ANY L satisfies both.
print("agentII second-discriminant requirement vs the finite-range kernel:")
print("  need: Khat(k_halo~3/Mpc) ~ 1   AND   Khat(k_lin~0.45/Mpc) <= 1/50 ... 1/800")
print()
hkpc = 0.7
k_lin = 0.3*hkpc        # 0.3 h/Mpc in 1/Mpc
k_halo_lo, k_halo_hi = 2*np.pi/3.0, 2*np.pi/1.0   # r=1-3 Mpc
print(f"  k_lin = {k_lin:.3f}/Mpc ; k_halo (r=1-3 Mpc) = {k_halo_lo:.2f}-{k_halo_hi:.2f}/Mpc")
print()
for L in [0.3, 1.0, 3.0, 10.0, 30.0, 100.0]:
    Kh_lin  = 1/(1+(L*k_lin)**2)
    Kh_halo = 1/(1+(L*k_halo_lo)**2)   # the WORST (lowest-k) halo mode to preserve
    supp_lin = 1/Kh_lin
    print(f"  L={L:6.1f} Mpc: Sigma suppression at k_lin = {supp_lin:7.1f}x ;  halo Khat(r=3Mpc) = {Kh_halo:.4f}")
print()
print("THE CONTRADICTION (decisive):")
print("  To suppress Sigma-1 by >=50x at k_lin=0.21/Mpc needs L^2 k_lin^2 >= 49 -> L >= 33 Mpc.")
print("  But preserving halo nu at r=3 Mpc (k=2.1/Mpc) needs L^2 k_halo^2 << 1 -> L << 0.5 Mpc.")
print("  These differ by ~70x in L.  The SAME monotone low-pass kernel cannot pass k~2 AND")
print("  block k~0.2 -- a low-pass that blocks the SMALLER k necessarily blocks the LARGER k MORE.")
print("  Khat is MONOTONE DECREASING in k: Khat(k_lin) > Khat(k_halo) ALWAYS (k_lin < k_halo).")
# prove monotonicity direction is WRONG:
print()
print("  *** WRONG-WAY MONOTONICITY ***  agentII needs suppression at SMALL k (linear) and")
print("  TRANSPARENCY at LARGE k (halo).  But a finite-range LOW-PASS kernel does the OPPOSITE:")
print("  transparent at small k (Khat->1), suppressing at large k.  The finite range distinguishes")
print("  scales, but in the WRONG DIRECTION for agentII's requirement.")
for L in [3.0, 30.0]:
    a = 1/(1+(L*k_lin)**2); b = 1/(1+(L*k_halo_lo)**2)
    print(f"    L={L}: Khat(k_lin)={a:.4f} > Khat(k_halo)={b:.4f}  -> suppresses HALO not LINEAR. Backwards.")
print()
print("CONCLUSION ZZ4: the finite range IS a scale discriminant, but a finite-range SLIP")
print("operator suppresses the slip at SHORT wavelength (halos) and passes it at LONG wavelength")
print("(linear/cosmological) -- exactly INVERTED from agentII's need (suppress linear, keep halo).")
print("It does NOT supply agentII's second discriminant; it supplies its mirror image.")

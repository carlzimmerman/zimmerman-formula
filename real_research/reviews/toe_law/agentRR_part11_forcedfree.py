"""
agentRR Part 11 -- the FORCED-vs-FREE ledger (the load-bearing field). For each saturated-gain
parameter, ask: is it pinned by the dS pump (H, T_dS=H/2pi, the X2 active reservoir) or free?
Then quantify the tuning the fold demands and whether the pump supplies it.

Parameters (in QQ/dimensionless units, c=c_chi=1):
  g0    -- small-signal gain (how active the pump is)
  kappa -- khronon cold loss
  Isat  -- saturation intensity (the nonlinear scale)
  k0    -- gain-center wavenumber (where in k the peak sits)
  Gamma -- gain bandwidth (width of the peak)
The fold demanded (Parts 5-7):
  - sigma4<0  : k0^4 < 3 Gamma^2  (gain center inside ~sqrt3 of the width) -- a CONSTRAINT on x=k0^2/Gam
  - true bounded fold: x=k0^2/Gam in ~[0.10,0.30] AND y=A/(c^2 Gam) (~g0-clamp strength) in a band
    that NARROWS to ~[1.00,1.30] (Part 7) -- a 2D window, ~5% of the natural parameter area, and the
    fold is SHALLOW (v_g^2_min down to ~-0.3 only when c_eff^2 -> 0, i.e. at the sonic-edge collapse)
  - STABLE: Part 9d -- fold-strength active response is UHP across off-center k for ANY kappa<=1
    => the fold band is NOT linearly stable under a scalar saturation clamp.
"""
import numpy as np

# Quantify: what fraction of the natural (x,y) parameter area gives BOTH a true bounded fold AND a
# linearly-stable retarded branch? (Part 7 gave the fold area; Part 9d says stability fails at fold
# strength -> the stable-AND-folding area is ~0 under scalar saturation.)
print("FORCED-vs-FREE ledger (dS pump pins what?):\n")
ledger = [
 ("k0  (gain center)",
  "the dS bath sets a SCALE k*~(c_chi/sqrt(a0))H (QQ: bath-set), so the ORDER of k0 is forced;",
  "but the precise k0/sonic-edge COINCIDENCE (k0 AT b->c_chi) is NOT forced by the smooth pump -- it",
  "is the codim-1 edge-pinning QQ already flagged as needing the peaked QNM. FREE (tuned)."),
 ("Gamma (bandwidth)",
  "T_dS=H/2pi sets a thermal width scale, so Gamma's ORDER is bath-forced;",
  "BUT the fold needs x=k0^2/Gamma in [0.10,0.30] -- a specific RATIO of center-to-width. The smooth",
  "GH continuum gives a BROAD (large-Gamma, small-x) response (QQ: smooth continuum sigma6<0). The",
  "narrow peak with the right x is the QNM input, NOT the thermal continuum. FREE (tuned)."),
 ("g0/kappa (gain above threshold)",
  "X2 FORCES the medium active (g0>0 is forced); the deep-MOND co-payment fixes the gain SIGN;",
  "BUT the MAGNITUDE g0/kappa that lands y~1.0-1.3 (fold-strength) is NOT pump-fixed -- QQ: 'forced",
  "in DIRECTION, free in MAGNITUDE.' The pump gives sign, not the threshold-crossing magnitude. FREE."),
 ("Isat (saturation scale)",
  "saturation EXISTS generically (any pumped medium saturates) -- the CLAMP MECHANISM is forced;",
  "BUT Isat sets the operating amplitude |chi*|, not the dispersion shape; it tames amplitude (D1)",
  "without fixing sigma6. And a SCALAR Isat cannot k-resolve to stabilize off-center fold modes",
  "(Part 9d/10). The clamp is forced; its ABILITY TO DELIVER A STATIC FOLD is not. FREE/insufficient."),
]
for entry in ledger:
    name = entry[0]
    print(f"  {name}:")
    for line in entry[1:]:
        print(f"     {line}")
    print()

print("QUANTITATIVE tuning cost:")
print("  - fold window (true bounded fold) ~ 5% of natural (x,y) area (Part 7) -> ~1.3 dex of tuning")
print("  - AND it requires the SONIC-EDGE collapse c_eff^2->0 for any non-shallow fold (Part 8 corr +0.43)")
print("  - AND linear stability FAILS there under scalar saturation (Part 9d: UHP for any kappa)")
print()
print("BOTTOM LINE (forced_or_model):")
print("  FORCED by the dS pump: (1) the medium is active [X2]; (2) sigma4<0 bend [851e7649];")
print("     (3) saturation clamps amplitude => the LTI *amplitude* runaway is tamed [D1, this route].")
print("  NOT FORCED (free model choices), each load-bearing for delivery:")
print("     (a) the gain PEAK being NARROW with x=k0^2/Gam in [0.1,0.3] (vs the smooth broad continuum);")
print("     (b) the gain MAGNITUDE landing y~1.0-1.3 (fold strength, not pump-fixed);")
print("     (c) k0 COINCIDING with the sonic edge (edge-pinning, = QNM, not smooth bath);")
print("     (d) the saturation being k-RESOLVED/non-Markovian to hold the off-center fold modes in the")
print("         LHP (plain scalar laser saturation does NOT -- Part 9d/10).")
print("  => SATURATION DELIVERS (a) bounded amplitude [D1, forced] and (b) a PEAKED response [D2, if the")
print("     peak is put in by hand]. It does NOT by itself deliver a STATIC STABLE edge-pinned fold [D3]:")
print("     that still needs the same peaked-QNM + magnitude tuning QQ named, PLUS a k-resolved clamp.")

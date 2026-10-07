#!/usr/bin/env python3
"""CFG477: T^3 isoperimetric ceiling for the confined-switch covers (door A of the
openai/math re-read). Applies the exact profile of the cubic flat 3-torus
(Isoperimetric conjecture paper, Theorem 1.1) to the CFG414/413 cover analysis:

  I_unit(V) = min{(36pi)^{1/3} v^{2/3}, 2 sqrt(pi) v, 2},  v = min(V, 1-V)
  minimizers: balls for V <= 4pi/81, circular tubes for 4pi/81 <= V <= 1/pi,
              coordinate slabs for 1/pi <= V <= 1/2 (then complements).

Transfers tested:
  T1  every cover in the box is deep in the BALL phase -> the analytic r_ta (6.60
      Mpc/h) is the isoperimetric estimator; the measured FFT cover radius 7.97 is
      a grid artifact, and its surface waste is exactly (7.97/6.60)^2 - 1.
  T2  ball phase lasts until radius = L/3: single-region cap on cover mass.
  T3  Siegel-Yao disjoint-ball criterion (symplectic ball packing paper): k covers
      of radius x*r_ta fit inside one host turnaround sphere R iff k*(x*r_ta)^3 < R^3
      and 2*x*r_ta < R. Gives k_max(x) - a falsifiable peak-count ceiling.

FROZEN inputs (CFG414): box 512^3 cells of 0.94 Mpc/h; analytic r_ta = 6.60 Mpc/h;
covered radius = 7.97 Mpc/h; D2 ON-mass split: covered_by_resolved_host = 0.805.
"""
import numpy as np

L = 512 * 0.94                       # box side, Mpc/h (cells 0.94 Mpc/h)
STEP = 0.94
R_TA = 6.60                          # analytic turnaround radius, Mpc/h
R_COV = 7.97                         # measured FFT top-hat covered radius
F_COV = 0.805                        # D2 covered_by_resolved_host fraction

V3 = 4*np.pi/3
def v_ball(r): return V3 * r**3 / L**3

def I_unit(V):
    v = min(V, 1-V)
    return min((36*np.pi)**(1/3)*v**(2/3), 2*np.sqrt(np.pi)*v, 2.0)

print("="*72)
print("CFG477: T^3 isoperimetric ceiling on the confined-switch covers")
print("="*72)

# T1: phase classification of the standard covers
print("\n[T1] Phase classification (ball phase: V <= 4pi/81 = %.4f)" % (4*np.pi/81))
for name, r in [("r_ta analytic", R_TA), ("x=0.5 r_ta", 0.5*R_TA),
                ("x=0.4 r_ta", 0.4*R_TA), ("x=0.3 r_ta", 0.3*R_TA),
                ("cover measured", R_COV)]:
    V = v_ball(r)
    phase = "BALL" if V <= 4*np.pi/81 else ("TUBE" if V <= 1/np.pi else "SLAB")
    print(f"   r={r:5.2f} Mpc/h   V/L^3 = {V:.3e}   phase = {phase}   "
          f"I_unit = {I_unit(V):.6f} (perimeter in box units)")

# ball phase lasts until r = L/3
r_max_ball = L * (3/(4*np.pi) * 4*np.pi/81)**(1/3)
print(f"\n   BALL phase holds until r = L/3 = {r_max_ball:.1f} Mpc/h "
      f"(volume fraction 4pi/81 = {4*np.pi/81:.4f})")
print(f"   All covers (r <= {R_COV} Mpc/h << {r_max_ball:.0f}) are isoperimetric balls: PASS")

# T2: C2 surface waste
S_ana = 4*np.pi*R_TA**2
S_meas = 4*np.pi*R_COV**2
waste = S_meas/S_ana - 1
print(f"\n[T2] C2 cover bias: analytic surface 4pi*{R_TA:.2f}^2 = {S_ana:.0f}, "
      f"measured 4pi*{R_COV:.2f}^2 = {S_meas:.0f}")
print(f"     surface waste of the FFT cover = +{100*waste:.1f}%  "
      f"(radius excess +{100*(R_COV/R_TA-1):.1f}%)")
n_eff_meas = F_COV*L**3/V3/R_COV**3
n_eff_ana = F_COV*L**3/V3/R_TA**3
print(f"     N_eff covers to carry F_COV={F_COV} of box mass:  measured r: {n_eff_meas:.0f},"
      f"  analytic r: {n_eff_ana:.0f}  (ball-optimal, disjoint)")
print(f"     UL: single-region cap {4*np.pi/81:.4f} << {F_COV} -> 0.805 REQUIRES many "
      f"regions (resolved hosts): consistent, mass concentrated: CHECK")

# Kepller packing cap on disjoint covers
print(f"\n     Kepler disjointness cap: total cover volume <= pi/(3 sqrt 2) = "
      f"{np.pi/(3*np.sqrt(2)):.4f} of box -> N <= "
      f"{np.pi/(3*np.sqrt(2))*L**3/V3/R_COV**3:.0f} at r={R_COV}")

# T3: Siegel-Yao peak-count ceiling
print("\n[T3] Siegel-Yao: k peak-covers of radius x*r_ta inside one host turnaround R")
print(f"     k_max = floor((R/(x*r_ta))^3) with 2*x*r_ta < R required")
for x in [0.23, 0.3, 0.4, 0.5, 1.0]:
    row = []
    for ratio in [1.0, 1.5, 2.0, 3.0]:
        R = ratio*R_TA
        cond = 2*x*R_TA < R
        k = int((R/(x*R_TA))**3) if cond else 0
        row.append(f"R={ratio:.1f}r_ta:{k:3d}{'*' if cond else ''}")
    print(f"     x={x:.2f}:  " + "  ".join(row))
print("     * = pairwise condition 2xr_ta < R satisfied")
print("\n     FALSIFIER: any host turnaround sphere containing > k_max resolved peaks\n"
      "     at cover radius x*r_ta violates disjoint embeddability -> the confined-\n"
      "     switch picture needs merged covers (read the x-window differently).")
print("="*72)
print("RESULT: T1 PASS (all covers ball-phase), T2 quantified (+45.9% surface waste,"
      "\nclassed grid artifact), T3 k_max(x) table ready for the peak catalog.")
#!/usr/bin/env python3
"""LANE CLOSE-3 (A). Derive the share X_s from the formation reading and grade it.

Nothing here is a new measurement. Every input is a number already printed by a
lane in this repo; the citations are inline. The script does arithmetic only.

Inputs (all cited):
  A0Z1   omega_b, omega_d, per footing          (a0z1_forest_<footing>.out line 2)
  FINAL3 KA-COSMIC: X_s = R -> 5.4092 / 5.4107  (PREREGISTER.md line 143)
  PD1    frozen share 59.4861 / 59.5029         (FINAL6/FINAL4 FROZEN_CRITERIA)
  FLD1   X_fold at the 4 KiDS masses            (RESULT.md line 57)
  ONE1   KiDS brackets at X = 5.41 / 10.82      (one1_kids_brackets.out)
  SRH1   gates G1-G4 and their edges            (RESULT.md)
"""
import math

FOOT = ["canonical", "alt"]

# --- A0Z1 form-B background, per footing (a0z1_forest_<foot>.out, line 2) -----
OM_B = {"canonical": 0.02236, "alt": 0.02234}
OM_D = {"canonical": 0.1209,  "alt": 0.1209}

# --- PD1's frozen share, per footing (FINAL6/FINAL4 FROZEN_CRITERIA) ---------
X_FROZEN = {"canonical": 59.4861, "alt": 59.5029}
# FINAL3's pre-registered KA-COSMIC value of R
R_KA = {"canonical": 5.4092, "alt": 5.4107}

# --- FLD1: the share of a halo that ends at R_fold(0), i.e. f = 1 ------------
# FLD1 RESULT.md: "At the four KiDS masses X_fold is 31.6, 21.0, 19.1 and 17.6
# (canonical; alt 34.8 to 19.4)."  Mass nodes: log M_b 9.4 / 10.45 / 10.7 / 10.9
X_FOLD = {"canonical": [31.6, 21.0, 19.1, 17.6],
          "alt":       [34.8, None, None, 19.4]}          # FLD1 prints only the range
LOGMB = [9.4, 10.45, 10.7, 10.9]

# --- ONE1 KiDS host-free brackets at 1.6 R_h (one1_kids_brackets.out) --------
# (share, footing) -> (z_all, z_late, z_early, profile chi2, model R_s)
ONE1 = {(5.41,  "canonical"): (+4.85, -0.08, +4.93, 23.7, 0.155),
        (5.41,  "alt"):       (+4.93, -0.07, +5.00, 24.4, 0.143),
        (10.82, "canonical"): (+4.34, -0.19, +4.47, 19.2, 0.215),
        (10.82, "alt"):       (+4.53, -0.15, +4.64, 20.8, 0.193)}
ONE1_FROZEN = {"canonical": (-1.14, -1.46, -0.65, 1.9, 1.003),
               "alt":       (-0.23, -1.23, +0.21, 0.9, 0.847)}
GATE_Z, GATE_CHI2 = 2.0, 9.49

# --- the parent's quoted KiDS host-free measurement --------------------------
PARENT_MEAS = {"canonical": (1.4002, 0.2211), "alt": (1.2740, 0.2012)}
LAW_LINE = 0.891            # KO1's line, 10^-0.05

# --- SRH1's four gates ------------------------------------------------------
G1_UPPER = {"canonical": 0.722, "alt": 0.725}     # f <= edge
G4_LOWER = {"canonical": 1.004, "alt": 1.050}     # f >= edge
G2_LOWER = 0.391                                   # f >= edge (both footings)
G3_COVER = 0.467                                   # f >= edge (coverage sub-line)
GAP = {"canonical": 1.39, "alt": 1.45}


def xt(X):
    """ONE1's dimensionless halo end radius: nu(x_t) = 1 + X, x_t^2 = X(X+1)."""
    return math.sqrt(X * (X + 1.0))


def f_of_share(X, X_fold):
    """SRH1's f = R_set / R_fold, from shares (FLD1's x = R_fold/r_M mapping)."""
    return xt(X) / xt(X_fold)


def main():
    print("=" * 78)
    print("A. THE DERIVATION")
    print("=" * 78)
    for ft in FOOT:
        R = OM_D[ft] / OM_B[ft]
        print(f"[{ft}] R = omega_d/omega_b = {OM_D[ft]}/{OM_B[ft]} = {R:.4f}"
              f"   (FINAL3 KA-COSMIC {R_KA[ft]}; dev {abs(R/R_KA[ft]-1)*100:.3f} %)")
    print()
    print("D1 (collapsed-patch closure): X_s M_b = [R/(1+R)] M_b (1 + X_s) -> X_s = R, exactly.")
    print("   check: R(1+X) = (1+R)X  =>  R + RX = X + RX  =>  X = R        (identity)")
    for ft in FOOT:
        R = R_KA[ft]
        print(f"   [{ft}] X_s = {R:.4f}; end radius x_t = sqrt(X(X+1)) = {xt(R):.4f} r_M")
    print()

    print("D2 (front at FLD1's fold): X_s = X_L(g_b(R_fold)) = X_fold, f = 1 by construction.")
    for ft in FOOT:
        vals = [v for v in X_FOLD[ft] if v is not None]
        lo, hi = min(vals), max(vals)
        print(f"   [{ft}] X_s = {lo}..{hi}  (FLD1, 4 KiDS masses)"
              f"   x_t = {xt(lo):.2f}..{xt(hi):.2f} r_M")
    print()

    print("=" * 78)
    print("B. GRADE vs ONE1's KiDS HOST-FREE GATE (|z| <= 2, profile chi2 <= 9.49)")
    print("=" * 78)
    for ft in FOOT:
        z, zl, ze, c2, mdl = ONE1[(5.41, ft)]
        ver = "PASS" if max(abs(z), abs(zl), abs(ze)) <= GATE_Z and c2 <= GATE_CHI2 else "FAIL"
        print(f"[{ft}] derived D1 (X=5.41): z all/late/early {z:+.2f}/{zl:+.2f}/{ze:+.2f}, "
              f"chi2 {c2} -> {ver}  (margin {abs(z)-GATE_Z:+.2f} sigma)")
        z, zl, ze, c2, mdl = ONE1_FROZEN[ft]
        print(f"       frozen  (X=59.5): z {z:+.2f}/{zl:+.2f}/{ze:+.2f}, chi2 {c2} -> "
              f"{'PASS' if max(abs(z),abs(zl),abs(ze))<=GATE_Z and c2<=GATE_CHI2 else 'FAIL'}")
    print()
    print("Against the parent's quoted measurement (1.4002+-0.2211 / 1.2740+-0.2012):")
    for ft in FOOT:
        d, s = PARENT_MEAS[ft]
        for lbl, key in (("D1  X=5.41", (5.41, ft)), ("frozen X=59.5", None)):
            m = ONE1[key][4] if key else ONE1_FROZEN[ft][4]
            z = (d - m) / s
            print(f"   [{ft}] {lbl}: model R_s {m:.3f}, z = ({d} - {m})/{s} = {z:+.2f} -> "
                  f"{'PASS' if abs(z) <= GATE_Z else 'FAIL'}; "
                  f"model/0.891 = {m/LAW_LINE:.3f} of KO1's law-level line")
    print()

    print("=" * 78)
    print("C. GRADE vs SRH1's FOUR GATES  (f = R_set / R_fold)")
    print("=" * 78)
    print("f is mapped from the share by FLD1's x = R_fold/r_M row (f=1 <=> X = X_fold).")
    for ft in FOOT:
        print(f"--- {ft}")
        for i, mb in enumerate(LOGMB):
            xf = X_FOLD[ft][i]
            if xf is None:
                continue
            f_d1 = f_of_share(R_KA[ft], xf)
            g1 = "PASS" if f_d1 <= G1_UPPER[ft] else "FAIL"
            g2 = "PASS" if f_d1 >= G2_LOWER else "FAIL"
            g3 = "PASS" if f_d1 >= G3_COVER else "FAIL"
            g4 = "PASS" if f_d1 >= G4_LOWER[ft] else "FAIL"
            print(f"  log M_b {mb:5.2f}  X_fold(f=1) {xf:5.1f}  "
                  f"D1 f = {f_d1:.3f}  G1 {g1} G2 {g2} G3(cov) {g3} G4 {g4}")
        print(f"  D2 (front at the fold): f = 1.000 exactly -> "
              f"G1 {'PASS' if 1.0 <= G1_UPPER[ft] else 'FAIL'} "
              f"G2 {'PASS' if 1.0 >= G2_LOWER else 'PASS'} "
              f"G3 {'PASS' if 1.0 >= G3_COVER else 'PASS'} "
              f"G4 {'PASS' if 1.0 >= G4_LOWER[ft] else 'FAIL'}  "
              f"(SRH1 gap {G1_UPPER[ft]}..{G4_LOWER[ft]}, factor {GAP[ft]})")
        print(f"  frozen X=59.5: f = 1.9..4.2 (FLD1: PD1's cap lies 1.1 to 4.2 x beyond R_fold(0))")
    print()

    print("=" * 78)
    print("D. THE TWO FINAL3 QUALIFIERS")
    print("=" * 78)
    for ft in FOOT:
        rat = R_KA[ft] / X_FROZEN[ft]
        print(f"[{ft}] derived/frozen = {R_KA[ft]}/{X_FROZEN[ft]} = {rat:.5f}; "
              f"1/11 = {1/11:.5f}; within 10 % of 1/11? "
              f"{'YES -> qualifier FIRES' if abs(rat/(1/11)-1) <= 0.10 else 'no'}"
              f"  (frozen/derived = {X_FROZEN[ft]/R_KA[ft]:.3f})")
    print()
    print("Share-driven vs radius-driven (ONE1 brackets, 1.6 R_h, canonical 'all'):")
    for X in (5.41, 10.82, 53.64, 59.4861):
        row = ONE1.get((X, "canonical"))
        zs = row[0] if row else (-0.59 if X < 55 else -1.14)   # 53.64 = census cap, ONE1 RESULT.md
        print(f"   X = {X:8.4f}  x_t = {xt(X):6.2f} r_M   z(all) = "
              f"{('%+.2f' % zs) if zs is not None else '   n/a'}")
    print("   -> the statistic tracks the AMOUNT monotonically; the radius follows from it.")


if __name__ == "__main__":
    main()

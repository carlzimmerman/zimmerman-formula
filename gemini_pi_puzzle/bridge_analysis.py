#!/usr/bin/env python3
"""
gemini_pi_puzzle/bridge_analysis.py -- Analysis of the physical bridge between
galaxy acceleration a0 and vacuum curvature Lambda, contrasting the de Sitter horizon
(L_dS^2 * Lambda = 3) with the vacuum Jeans scale ((R*)^2 * Lambda = 8*pi).
"""

import math
import sympy as sp

def main():
    print("=" * 78)
    print("THE PHYSICAL BRIDGE: L_dS^2 * Lambda = 3 vs (R*)^2 * Lambda = 8*pi")
    print("=" * 78)
    
    c, G, Lambda, a0 = sp.symbols('c G Lambda a0', positive=True)
    
    # 1. Cosmological horizon in de Sitter:
    # H^2 = Lambda * c^2 / 3 => L_dS = c / H = sqrt(3 / Lambda)
    L_dS = sp.sqrt(3 / Lambda)
    id_dS = sp.simplify(L_dS**2 * Lambda)
    print(f"1. Kinematic de Sitter horizon: L_dS = sqrt(3/Lambda)")
    print(f"   L_dS^2 * Lambda = {id_dS} (reflects 3 spatial dimensions in expansion)")
    
    # 2. Vacuum gravitational dynamical scale (Jeans scale):
    # rho_Lambda = Lambda * c^2 / (8*pi*G)
    # tau_vac = 1 / sqrt(G * rho_Lambda)
    # R* = c * tau_vac = c / sqrt(G * rho_Lambda)
    rho_L = Lambda * c**2 / (8 * sp.pi * G)
    R_star = c / sp.sqrt(G * rho_L)
    id_star = sp.simplify(R_star**2 * Lambda)
    print(f"\n2. Dynamic vacuum Jeans scale: R* = c / sqrt(G * rho_Lambda)")
    print(f"   (R*)^2 * Lambda = {id_star} (reflects 8*pi in Einstein's field equation)")
    
    # 3. Ratio between the two physical scales:
    ratio_sq = sp.simplify(R_star**2 / L_dS**2)
    print(f"\n3. Ratio of the two scales squared:")
    print(f"   (R* / L_dS)^2 = {ratio_sq} == 8*pi / 3")
    print(f"   R* / L_dS = {float(sp.sqrt(ratio_sq)):.5f}")
    
    # 4. The Bridge Hypothesis:
    # Why would galaxy gravity (a0) be governed by R* instead of L_dS?
    # If a0 is the surface gravity of a horizon at R*:
    # kappa = c^2 / (2 * r_H)
    # Setting r_H = R* gives:
    a0_bridge = sp.simplify(c**2 / (2 * R_star))
    print(f"\n4. If a0 is set by R* (surface gravity kappa = c^2 / (2 * R*)):")
    print(f"   a0 = {a0_bridge} == c^2 * sqrt(Lambda / (32*pi))")
    
    # Contrast with setting r_H = L_dS (the naive de Sitter horizon):
    a0_dS = sp.simplify(c**2 / (2 * L_dS))
    print(f"\n5. If a0 were set by L_dS (surface gravity of de Sitter horizon):")
    print(f"   a0_dS = {a0_dS} == (1/2) * c * H_Lambda == c^2 * sqrt(Lambda / 12)")
    print(f"   Ratio a0_dS / a0 = {float(sp.simplify(a0_dS / a0_bridge)):.5f} == sqrt(8*pi/3) == 2.8944")
    
    # 6. Physical interpretation:
    # Galaxy dynamics does NOT probe the cosmic expansion rate H (which gives 3).
    # Galaxy dynamics probes the local GRAVITATIONAL RESPONSE to vacuum energy density rho_Lambda (which gives 8*pi).
    print("\n" + "=" * 78)
    print("CONCLUSION:")
    print("  r_H^2 * Lambda = 8*pi is NOT the de Sitter horizon (which has L^2 * Lambda = 3).")
    print("  r_H is the vacuum gravitational dynamical scale R* = c / sqrt(G * rho_Lambda).")
    print("  The missing physics is why a galaxy's MOND transition couples to R* with factor 1/2.")
    print("=" * 78)

if __name__ == '__main__':
    main()

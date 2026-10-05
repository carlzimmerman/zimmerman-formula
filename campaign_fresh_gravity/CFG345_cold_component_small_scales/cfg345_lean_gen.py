#!/usr/bin/env python3
"""Generate CFG345_certificate.lean from cfg345_small_scales_results.json (outward rounding to 4 significant figures)."""
import json, math, os
from fractions import Fraction as F
H = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(H, "cfg345_small_scales_results.json")))
Mneed = json.load(open(os.path.join(H, "..", "CFG344_postreion_cold_accretion", "cfg344_accretion_results.json")))["HIST"]["8.0"]["M_cool"]
def up(x):  e = math.floor(math.log10(x)) - 3; return F(math.ceil(x / 10**e)) * F(10) ** e
def dn(x):  e = math.floor(math.log10(x)) - 3; return F(math.floor(x / 10**e)) * F(10) ** e
A = J["wave"]["A_T2"]; B = J["roadS"]["B_eq"]
Alo, Ahi, Blo, Bhi, Mlo, Mhi = dn(A), up(A), dn(B), up(B), dn(Mneed), up(Mneed)
q = lambda f: f"({f.numerator} / {f.denominator} : ℚ)" if f.denominator != 1 else f"({f.numerator} : ℚ)"
L = ["import Mathlib", "",
 "/-! CFG345 certificate. Wave field: M_1/2 = A m22^(-4/3) (HBG, T^2 = 1/2) <= M_need  <=>  m22^4 * M_need^3 >= A^3.",
 f"Road S: M_J(z_eq) = B M^-6 (M in eV) <= M_need  <=>  M^6 * M_need >= B. A = {A:.5e}, B = {B:.5e}, M_need = {Mneed:.5e} Msun,",
 "all rounded outward to 4 significant figures. Values from cfg345_small_scales_results.json and CFG344's JSON. -/", ""]
th = [("wave_floor_2e20_suppresses", f"(200 : ℚ)^4 * {q(Mhi)}^3 < {q(Alo)}^3", "m = 2e-20 eV (record window floor): M_1/2 > M_need"),
      ("wave_228_fails", f"(228 : ℚ)^4 * {q(Mhi)}^3 < {q(Alo)}^3", "m22 = 228 still above M_need"),
      ("wave_229_passes", f"{q(Ahi)}^3 ≤ (229 : ℚ)^4 * {q(Mlo)}^3", "bound: m >= 2.29e-20 eV suffices"),
      ("wave_L383_floor_passes", f"{q(Ahi)}^3 ≤ (2000 : ℚ)^4 * {q(Mlo)}^3", "L383 floor 2e-19 eV passes"),
      ("roadS_gdust_min_suppresses", f"(424 / 100 : ℚ)^6 * {q(Mhi)} < {q(Blo)}", "road S at its G-DUST minimum 4.24 eV suppresses"),
      ("roadS_44eV_passes", f"{q(Bhi)} ≤ (44 : ℚ)^6 * {q(Mlo)}", "road S bound: M >= 44 eV suffices"),
      ("roadS_onset_passes", f"{q(Bhi)} ≤ (3300 : ℚ)^6 * {q(Mlo)}", "the record's own onset requirement 3.3 keV passes")]
for n, s, d in th: L += [f"/-- {d} -/", f"theorem {n} : {s} := by norm_num", ""]
open(os.path.join(H, "CFG345_certificate.lean"), "w").write("\n".join(L))
print("\n".join(L))

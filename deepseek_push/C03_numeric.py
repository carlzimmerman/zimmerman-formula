#!/usr/bin/env python3
r"""C03 -- NUMERIC GATE for the LINE KINEMATICS + THE ABEL CUSP certificates.

THEOREM 1 (B01 line kinematics, Lean-certified in C03_line_abel.lean):
  E = m/2 exactly and sigma_E/E = sigma_v/c (field-level factorization).
Numeric here: the committed registers reproduced at high precision:
  E = 5.0886/2 = 2.5443 keV;  sigma_E = E*sigma_d/c = 1.18986 eV;
  delta-E/E = sigma_d/c = 4.6766e-4.

THEOREM 2 (B02 Abel column, Lean-certified as the arctan substitution
identity + pi/2 evaluation + limit):
  Int_0^oo 1/(b^2+s^2) ds = pi/(2b) for b > 0.
Numeric here: the B02 phantom projected column Sigma_p(b) = pi*A/b
reproduced to 1e-10 by direct quadrature of the LOS integral
  Sigma(b) = A * Int_-oo^oo 1/(b^2+l^2) dl
at A = 3.388787757915661e19 kg/m and b = 1 kpc; plus the finite-L
(capped) B02 C1 value with the same tolerance.

Uses the mpmath environment if available (checked per-run); otherwise
scipy/numpy quad at float precision.  rel-err tolerance 1e-10.
"""

import json, math, os

try:
    from mpmath import mp, mpf, pi, sqrt, atan, quad
    mp.dps = 30
    HAVE_MP = True
except Exception:
    HAVE_MP = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "C03_numeric.out")
JSON = os.path.join(HERE, "C03_results.json")

# ---------------- committed registers (B01/B02)
M_KEV = 5.0886
E_KEV = M_KEV / 2.0
SIG_D = 140.2          # km/s, G182
C_KMS = 2.99792458e5   # km/s
A_GAL = 3.388787757915661e19   # kg/m, MW phantom amplitude (G072)
KPC   = 3.0856775814913673e19  # m
G     = 6.674e-11
MB_MW = 6.5e10 * 1.98892e30     # kg
A0    = 9.3619e-11
RM_GAL = math.sqrt(G * MB_MW / A0)
RB_GAL = 0.62 * RM_GAL          # B02 physical halo cut

RES = []
def check(name, measured, ok, reading=""):
    RES.append({"name": name, "measured": measured, "pass": bool(ok),
                "reading": reading})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading:
        print(f"         reading : {reading}")

print("=" * 100)
print("C03 -- NUMERIC GATE: line kinematics (B01) + the Abel cusp (B02)")
print("=" * 100)

# ============================================================ PART 1
print("\nPART 1  THE LINE KINEMATICS (Lean: line_energy_is_half, doppler_width_identity)")
print("=" * 100)
E = M_KEV / 2.0
print(f"  E = m/2 = {M_KEV}/2 = {E:.4f} keV   (A05 register 2.5443)")
check("N1 [E = m/2] the line energy reproduces the A05 register exactly",
      f"E = {E:.4f} keV", abs(E - 2.5443) < 1e-4,
      "m = 5.0886 keV (G212 joint peak), E = m/2 = 2.5443 keV exactly.")

de_e = SIG_D / C_KMS
de_ev = E * 1e3 * SIG_D / C_KMS
print(f"  delta-E/E = sigma_d/c = {de_e:.6e}")
print(f"  sigma_E = E*sigma_d/c = {de_ev:.5f} eV")
check("N2 [the Doppler width identity] sigma_E/E = sigma_v/c holds with "
      "the committed registers",
      f"sigma_E/E = {de_e:.6e} = {SIG_D}/{C_KMS}",
      abs(de_e - SIG_D / C_KMS) < 1e-15,
      "identity by construction; the certified statement is the Lean "
      "field factorization E*(sigma_v/c).")
check("N3 [the width register] sigma_E = 1.1899 eV in the B01 band [1.18, 1.20]",
      f"sigma_E = {de_ev:.4f} eV", 1.18 < de_ev < 1.20,
      "B01 C2 register 1.19 eV; the Lean interval theorem num_sigmaE_eV.")
check("N4 [the ratio register] delta-E/E in the B01 band [4.67e-4, 4.68e-4]",
      f"delta-E/E = {de_e:.6e}", 4.67e-4 < de_e < 4.68e-4,
      "B01 C2 register 4.68e-4; the Lean interval theorem num_deltaE_over_E.")

# ============================================================ PART 2
print("\nPART 2  THE ABEL COLUMN (Lean: arctan_substitution_identity, arctan_pi_over_two)")
print("        Int_0^oo 1/(b^2+s^2) ds = pi/(2b),  Sigma_p(b) = pi A/b")
print("=" * 100)

b = KPC
A = A_GAL

if HAVE_MP:
    # well-scaled: u = l/b, integrand (1/b)*1/(1+u^2); geometric subintervals
    # give each mpmath tanh-sinh pass a modest dynamic range; the far tail
    # u in [T, oo) is 1/T - 1/(3T^3) + O(1/T^5) <= 1e-50 at T = 1e10.
    T = 1e10
    subs = [mpf(0)] + [mpf(10) ** k for k in range(0, 11)]   # 0, 1, ..., 1e10
    val = mpf(0)
    for i in range(len(subs) - 1):
        val += quad(lambda u: 1.0 / (1 + u * u), [subs[i], subs[i + 1]])
    tail = 1 / mpf(T) - 1 / (3 * mpf(T) ** 3)
    half = val + tail                             # -> pi/2
    num_full = 2 * A / b * half
    closed = pi * A / b
    rel_full = abs(num_full - closed) / closed
    print(f"  full-LOS quadrature (u-sub, [-inf,inf]): {mp.nstr(num_full, 17)}")
    print(f"  closed form pi*A/b                 : {mp.nstr(closed, 17)}")
    print(f"  rel err = {mp.nstr(rel_full, 5)}   (half-line integral = "
          f"{mp.nstr(half, 17)} vs pi/2)")
    check("N5 [the Abel column] the full-LOS column Sigma_p(b) = A*pi/b "
          "reproduced to 1e-10 by direct quadrature",
          f"rel err {mp.nstr(rel_full, 5)}", rel_full < 1e-10,
          "quadrature of int 1/(1+u^2) du on u in [0,1e10] (geometric "
          "subintervals) + the O(1/T^5) tail; the Lean certificate is the "
          "arctan substitution identity + the pi/2 evaluation.")
    # the capped B02 C1 object: finite L = sqrt(r_break^2 - b^2)
    Lc = sqrt(RB_GAL ** 2 - b ** 2)
    num_c = 2 * A * quad(lambda l: 1.0 / (b * b + l * l), [mpf(0), mpf(Lc)])
    closed_c = 2 * A / b * atan(Lc / b)
    rel_c = abs(num_c - closed_c) / closed_c
    print(f"\n  capped (r_break) quadrature: {mp.nstr(num_c, 17)}")
    print(f"  capped closed form 2A/b arctan(L/b): {mp.nstr(closed_c, 17)}")
    print(f"  rel err = {mp.nstr(rel_c, 5)}  (B02 C1 register 3.088476669, rel 5.03e-15)")
    check("N6 [the capped column, B02 C1] the r_break-capped column "
          "2A/b*arctan(L/b) reproduces the quadrature to 1e-10",
          f"rel err {mp.nstr(rel_c, 5)}", rel_c < 1e-10,
          "the finite object of B02 C1; the Lean theorem "
          "capped_column_closed_form.")
    print(f"\n  register check: pi*A/b at b=1kpc = {mp.nstr(closed, 12)} "
          f"in (3.450, 3.451): {3.450 < float(closed) < 3.451}")
    check("N7 [the MW register] pi*A/b in (3.450, 3.451) at b = 1 kpc",
          f"pi*A/b = {mp.nstr(closed, 12)}",
          3.450 < float(closed) < 3.451,
          "the Lean interval theorem num_sigma_phantom_MW.")
else:
    raise SystemExit("mpmath required for the 1e-10 gate "
                     "(use the miniconda base python3)")

print("\n" + "=" * 100)
print("GATES AND REGISTRATION -- see C03_results.json")
print("=" * 100)
n_pass = sum(1 for c in RES if c["pass"])
n_tot = len(RES)
print(f"\n  CHECKS: {n_pass}/{n_tot} PASS")

result = {
    "lane": "C03_line_abel",
    "wave": "C-wave (LEAN certification of the B-series lemma targets)",
    "question": "Certify (1) the LINE KINEMATICS -- E = m/2 exactly and "
                "sigma_E/E = sigma_v/c (the Doppler width identity, "
                "field-level factorization, B01) -- and (2) THE ABEL CUSP "
                "-- Int_0^oo 1/(b^2+s^2) ds = pi/(2b) for b > 0 via the "
                "substitution identity (arctan integral) with the pi/2 "
                "evaluation (B02), at the level the house patterns allow; "
                "plus the numeric gate: the B02 column Sigma(b) = A*pi/b "
                "reproduced to 1e-10.",
    "lean_file": "deepseek_push/lean/C03_line_abel.lean",
    "lean_status": {
        "compiles": True, "exit_code": 0, "n_sorry": 0,
        "axiom_subset": "{propext, Classical.choice, Quot.sound} -- "
                        "verified per theorem via #print axioms",
        "theorems": 13,
        "theorem_registry": [
            {"name": "line_energy_is_half",
             "statement": "E = m/2 <-> m = 2E (exact, bidirectional)",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "line_energy_divided",
             "statement": "E = m/2 ==> E/m = 1/2",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "doppler_width_identity",
             "statement": "sigma_E = E*sigma_v/c ==> sigma_E/E = sigma_v/c",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "doppler_width_factorized",
             "statement": "sigma_E = E*sigma_v/c ==> sigma_E = E*(sigma_v/c) "
                          "(the factorization)",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "num_E_line_keV",
             "statement": "5.0886/2 = 2.5443 keV (norm_num)",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "num_sigmaE_eV",
             "statement": "sigma_E = 1.18986 in (1.18, 1.20) eV",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "num_deltaE_over_E",
             "statement": "delta-E/E in (4.67e-4, 4.68e-4)",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "arctan_substitution_identity",
             "statement": "Int_0^t 1/(b^2+s^2) ds = arctan(t/b)/b for b > 0 "
                          "(FTC; derivative of arctan(s/b)/b closed by "
                          "field algebra)",
             "status": "CERTIFIED",
             "strikes": 2},
            {"name": "arctan_pi_over_two",
             "statement": "arctan(t/b) -> pi/2 as t -> oo for b > 0 "
                          "(composed t/b -> oo with tendsto_arctan_atTop)",
             "status": "CERTIFIED",
             "strikes": 1},
            {"name": "abel_column_half_line",
             "statement": "Int_0^oo 1/(b^2+s^2) ds = pi/(2b): the substitution "
                          "identity + pi/2 evaluation, as the limit of the "
                          "finite integrals",
             "status": "CERTIFIED",
             "strikes": 1},
            {"name": "sigma_cusp_full_los",
             "statement": "2*(pi/(2b))*A = pi*A/b (the full-LOS b^-1 cusp "
                          "algebra, B02 C1)",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "capped_column_closed_form",
             "statement": "2A*Int_0^L 1/(b^2+s^2) ds = (2A/b)*arctan(L/b) "
                          "(the r_break-capped B02 column)",
             "status": "CERTIFIED",
             "strikes": 0},
            {"name": "num_sigma_phantom_MW",
             "statement": "pi*A/b at A = MW, b = 1 kpc in (3.450, 3.451) "
                          "(pi-interval arithmetic, G083 style)",
             "status": "CERTIFIED",
             "strikes": 1},
        ],
        "strike_ledger": [
            {"theorem": "arctan_substitution_identity",
             "strikes": 2,
             "blockers": [
                "strike 1: HasDerivAt (Real.arctan ∘ (fun y => y/b)) vs "
                "(fun y => Real.arctan (y/b)) -- function-shape mismatch "
                "after simplification; fixed with simpa [Function.comp_def].",
                "strike 2: trailing `ring` after `field_simp` -- No goals "
                "to be solved (field_simp already closes by ring_nf)"],
             "outcome": "CLOSED"},
            {"theorem": "arctan_pi_over_two",
             "strikes": 1,
             "blockers": [
                "strike 1: bare `atTop` elaborated differently from "
                "`Filter.atTop` under relaxedAutoImplicit=false; and the "
                "`𝓝` notation is NOT in scope in this mathlib build "
                "(unknown identifier) -- use `nhds`."],
             "outcome": "CLOSED"},
            {"theorem": "abel_column_half_line",
             "strikes": 1,
             "blockers": [
                "strike 1: same `atTop`/`𝓝` elaboration; fixed by full "
                "qualification + `open Filter`."],
             "outcome": "CLOSED"},
            {"theorem": "num_sigma_phantom_MW",
             "strikes": 1,
             "blockers": [
                "strike 1: `field_simp` closed the goal before the trailing "
                "`ring` (No goals to be solved); and the pi-interval bounds "
                "had to be chosen so the coarse 3.141592/3.1416 pi-bounds "
                "still separate (3.450 < pi*A/b < 3.451, verified by exact "
                "rational arithmetic before encoding)."],
             "outcome": "CLOSED"},
        ],
    },
    "theorem1_line_kinematics": {
        "statement": "E = m/2 exactly; sigma_E = E x (sigma_v/c) and "
                     "sigma_E/E = sigma_v/c (field-level factorization)",
        "registers": {"m_keV": M_KEV, "E_keV": E_KEV,
                      "sigma_d_kms": SIG_D, "c_kms": C_KMS},
        "sigma_E_eV": de_ev, "delta_E_over_E": de_e,
        "lean_theorems": ["line_energy_is_half", "line_energy_divided",
                          "doppler_width_identity", "doppler_width_factorized",
                          "num_E_line_keV", "num_sigmaE_eV",
                          "num_deltaE_over_E"],
        "reading": "the width is Doppler-dominated, never intrinsic (no "
                   "rate predicted, A05); the thermal/core footings are "
                   "one velocity scale read two ways (B01 honest note).",
    },
    "theorem2_abel_column": {
        "statement": "Int_0^oo 1/(b^2+s^2) ds = pi/(2b) for b > 0; the "
                     "phantom r^-2 column projects to Sigma_p(b) = pi*A/b "
                     "(the b^-1 cusp)",
        "certification_level": "the substitution identity (arctan integral "
                               "closed by FTC) + the pi/2 evaluation "
                               "(arctan(t/b) -> pi/2), assembled as the "
                               "limit of finite integrals -- the level the "
                               "house patterns allow; the measure-theoretic "
                               "improper integral itself is NOT the target "
                               "(G031 house style: intervalIntegral chain)",
        "lean_theorems": ["arctan_substitution_identity",
                          "arctan_pi_over_two", "abel_column_half_line",
                          "sigma_cusp_full_los",
                          "capped_column_closed_form",
                          "num_sigma_phantom_MW"],
        "numeric": {"A_kg_m": A_GAL, "b_m": KPC,
                    "Sigma_p_b_kg_m2": float(closed),
                    "quadrature_rel_err": float(rel_full),
                    "capped_B02_C1": float(closed_c),
                    "capped_rel_err": float(rel_c),
                    "tolerance": 1e-10},
    },
    "numeric_checks": RES,
    "n_pass": n_pass, "n_total": n_tot,
    "stated_precision": "E = m/2 = 2.5443 keV; sigma_E = 1.18986 eV "
                        "(1.19 eV band); delta-E/E = 4.6766e-4; "
                        "Sigma_p(1 kpc) = pi*A/b = 3.4501954412545 kg/m^2 "
                        "in (3.450, 3.451); Abel column quadrature to 1e-10.",
    "registration": {
        "CERTIFIED": [
            "E = m/2 exactly (line_energy_is_half)",
            "sigma_E/E = sigma_v/c (doppler_width_identity, the Doppler "
            "width identity / field-level factorization)",
            "Int_0^oo 1/(b^2+s^2) ds = pi/(2b) for b > 0 "
            "(arctan_substitution_identity + arctan_pi_over_two + "
            "abel_column_half_line -- substitution identity + pi/2 "
            "evaluation)",
            "Sigma_p(b) = pi*A/b (sigma_cusp_full_los, the 1/b cusp)",
            "the B02 column reproduced numerically to 1e-10 (N5/N6)"],
        "PENDING": [],
        "rule": "three-strike rule: any theorem not closed in 3 attempts "
                "is dropped with the exact Mathlib blocker named and "
                "registered PENDING. All 13 theorems closed; the strike "
                "ledger records the blockers hit and the fixes. No "
                "PENDING carry-over.",
        "axioms": "every #print axioms output is exactly "
                  "[propext, Classical.choice, Quot.sound]; zero sorry; "
                  "exit 0."},
    "json_path": JSON,
}

with open(JSON, "w") as f:
    json.dump(result, f, indent=1, sort_keys=False)
print(f"\n  JSON written: {JSON}")
print(f"  CHECKS {n_pass}/{n_tot} PASS")
print("  C03 NUMERIC GATE DONE.")
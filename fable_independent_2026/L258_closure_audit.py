#!/usr/bin/env python3
"""L258 -- THE "FINISHED PUZZLE" OF 2026-09-14/15, AUDITED ON ITS OWN NUMBERS.

WHAT IS UNDER REVIEW.  Between 2026-09-14 and 09-15 the glm53/qwen38/hy4/grok/deepseek agent tracks
promoted the equilibrium reading of the radial acceleration relation to "a complete theory": the STATE
board (glm53_push/STATE.md) labels every rung of its chain DERIVED, including
    rung 4  -- the dust temperature sigma^2 = sqrt(G M_b a_0)/2, "DERIVED -- 3 independent routes"
              (G046, G056, Q001), which PAPER29 (DOI 10.5281/zenodo.22753165) had labelled POSTULATED;
    rung 9  -- Omega_Lambda = 32 pi a_0^2 / (3 H_0^2 c^2) = 0.6857, "+0.07% of Planck, DERIVED + Lean"
              (G052, G058, Q002), "the dark energy and the MOND scale are ONE measurement";
and names a relativistic completion -- the frozen scalar L = Lambda^4 f(K) (H011/G054/G055) -- whose
referee defence (glm53_push/REFEREE_ATTACKS.md) declares Cassini, lensing and PPN ANSWERED.

This lane tests those four promotions on the tracks' own committed numbers and on this track's own
committed lanes.  It adds nothing to the physics; it asks whether the promotions are earned.  Every
check states the measurement and the threshold separately; a FAIL is a finding; there are no literal-True
conditions; both a_0 footings are carried wherever a dimensional number appears.

PARTS
  A  the Omega_Lambda closure: does the identity return anything that was not fed into a_0?
  B  rung 4: does hydrostatic balance in the scalar's 1/r force FIX the temperature, or ASSUME the profile?
     and what the tracks' own lane outputs say about it (G046's scorecard; the double-count under G046's
     stated rule that the dust sources the same equation)
  C  the completion: Cassini by inheritance (L243), the two mutually exclusive completions cited as one,
     what carries the lensing/cluster/Milky-Way mass, and the uncommitted G062 draft
  D  the Lean inventory (from L258_lean_inventory.py): what compiles, on which axioms, and what the
     certified statements are

INPUTS (all committed, all cited by path): glm53_push/G046_temperature_from_action_results.json,
glm53_push/G003_results.json, glm53_push/G032_horn_a_fixed_congruence.out, hy4_push/H011_results.out,
fable_independent_2026/L243_onefunction_cassini_quadrupole.out, fable_independent_2026/L232_sparc_parameter_free.out,
glm53_push/G062_results.json (uncommitted draft at audit time), fable_independent_2026/L258_lean_inventory.json.
Planck 2018 (TT,TE,EE+lowE+lensing): H_0 = 67.36 +/- 0.54, Omega_Lambda = 0.6847 +/- 0.0073, Omega_b = 0.0493,
Omega_dm = 0.2647 (literature).  McGaugh, Lelli & Schombert 2016 PRL 117 201101: a_0 = 1.20 +/- 0.02 (rand)
+/- 0.24 (syst) e-10 m/s^2 (literature)."""
import os, re, json, math, sys
import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
G, C_LIGHT, MPC, MSUN, KPC, PC = 6.674e-11, 299792458.0, 3.0857e22, 1.989e30, 3.0857e19, 3.0857e16
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
CH, OUT = [], {}
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
def rd(rel):
    p = os.path.join(REPO, rel)
    return open(p).read() if os.path.exists(p) else None
def mu2(u): return 1.0 - (1.0 + u) ** -2
def solve_mu2(gN, a0):
    """g mu_2(g/2a0) = gN, the certified sourced equation (Lean solve_well_posed: strictly monotone)."""
    f = lambda g: g * mu2(g / (2 * a0)) - gN
    return brentq(f, gN, 1e4 * max(gN, a0) + gN)

print("L258 -- the 'finished puzzle' of 2026-09-14/15, audited on its own numbers\n")

# =====================================================================================================
print("=" * 100); print("PART A -- Omega_Lambda 'from a_0 alone' (G052 / G058 / Q002)"); print("=" * 100)
H0_P, OMEGA_L_P, SIG_OMEGA_P, OMEGA_B_P, OMEGA_DM_P = 67.36, 0.6847, 0.0073, 0.0493, 0.2647
def a0_from(omega, h0): return 0.5 * C_LIGHT * (h0 * 1e3 / MPC) * math.sqrt(3 * omega / (8 * math.pi))
def omega_back(a0, h0): return 32 * math.pi * a0 ** 2 / (3 * (h0 * 1e3 / MPC) ** 2 * C_LIGHT ** 2)

print("A1 -- the identity applied to the a_0 that was built from Omega_Lambda")
om, h0, a0s, cs, Gs = sp.symbols('Omega H0 a0 c G', positive=True)
a0_expr = cs / 2 * sp.sqrt(Gs * om * 3 * h0 ** 2 / (8 * sp.pi * Gs))          # a0 = (c/2) sqrt(G rho_Lambda)
resid = sp.simplify(32 * sp.pi * a0_expr ** 2 / (3 * h0 ** 2 * cs ** 2) - om)   # fed back through the G058 identity
print(f"    sympy: 32 pi a0(Omega,H0)^2/(3 H0^2 c^2) - Omega = {resid}")
for (omi, h0i) in [(0.685, 67.4), (0.6847, 67.36)]:
    a0i = a0_from(omi, h0i)
    print(f"    a0 built from Omega_L = {omi}, H0 = {h0i}: {a0i:.5e} m/s^2 (registered canonical 9.3619e-11: {100*(a0i/A0['canonical']-1):+.3f}%)")
om_back = omega_back(A0["canonical"], H0_P)
ratio_rounding = (67.4 / 67.36) ** 2 * (0.685 / 0.6847)
print(f"    Omega_L returned by the identity from the registered a0 and H0 = 67.36: {om_back:.4f} (G052 registers 0.6857)")
print(f"    ratio to Planck 0.6847: {om_back/OMEGA_L_P:.5f};  the ratio of the two roundings (67.4/67.36)^2 x (0.685/0.6847) = {ratio_rounding:.5f}")
OUT["A1"] = dict(sympy_residual=str(resid), omega_back_registered=om_back, rounding_ratio=ratio_rounding)
check("A1 [THE IDENTITY RETURNS ITS OWN INPUT] the registered a_0 is rebuilt from the Planck pair the "
      "programme used (Omega_L = 0.685, H_0 = 67.4); the G058 identity is then applied to it symbolically and "
      "numerically; a symbolic residual of zero AND a numerical return within 0.2% of the input Omega means "
      "the 'derivation' of Omega_Lambda is the inversion of the definition of a_0",
      resid == 0 and abs(a0_from(0.685, 67.4) / A0["canonical"] - 1) < 2e-3 and abs(om_back / 0.685 - 1) < 2e-3,
      f"symbolic residual {resid}; a0(0.685, 67.4) reproduces the registered value to "
      f"{100*(a0_from(0.685,67.4)/A0['canonical']-1):+.3f}%; the identity returns {om_back:.4f}. The advertised "
      f"'+0.07% agreement with Planck' is the ratio {ratio_rounding:.5f} between two roundings of the same Planck "
      f"parameters (H_0 = 67.4 vs 67.36, Omega = 0.685 vs 0.6847), not a prediction. Q002's own closing "
      f"paragraph says the same: 'a_0's canonical value was DERIVED from rho_Lambda in the first place'")

print("\nA2 -- what the identity returns from an a_0 that was NOT built from Omega_Lambda")
l232 = rd("fable_independent_2026/L232_sparc_parameter_free.out") or ""
m = re.search(r"n = 2 the freely fitted scale is ([0-9.]+) times the cosmological one, giving a_0 = ([0-9.e+-]+)", l232)
a0_free = float(m.group(2)) if m else 1.2457e-10
a0_mcg = 1.20e-10
indep = {"L232 free-scale fit at n = 2 (SPARC, M/L fixed 0.5/0.7)": a0_free,
         "McGaugh+2016 RAR fit (nu_RAR, free M/L)": a0_mcg}
worst = 0.0
for name, a in indep.items():
    ob = omega_back(a, H0_P); worst = max(worst, abs(ob / OMEGA_L_P - 1))
    print(f"    {name}: a_0 = {a:.4e} -> Omega_L = {ob:.3f} ({100*(ob/OMEGA_L_P-1):+.0f}% from Planck, {abs(ob-OMEGA_L_P)/SIG_OMEGA_P:.0f} sigma)")
    OUT[f"A2_{name[:12]}"] = dict(a0=a, omega=ob)
band = [omega_back(a0_mcg * (1 - 0.2), H0_P), omega_back(a0_mcg * (1 + 0.2), H0_P)]
print(f"    the RAR's +/-20% systematic on a_0 maps to Omega_L in [{band[0]:.2f}, {band[1]:.2f}] (Omega scales as a_0^2)")
OUT["A2_band"] = band
check("A2 [A GALACTIC a_0 DOES NOT RETURN PLANCK'S Omega_Lambda] the two independent galactic scales on the "
      "record (this track's L232 free-scale fit at the selected integer, and the literature RAR fit) are fed "
      "through the same identity and compared with Planck at G052's own 1% threshold",
      worst < 0.01,
      f"L232's free scale gives Omega_L = {omega_back(a0_free, H0_P):.2f} and the literature value {omega_back(a0_mcg, H0_P):.2f}: "
      f"both exceed 1 (a closed, matter-free universe), {abs(omega_back(a0_free,H0_P)-OMEGA_L_P)/SIG_OMEGA_P:.0f} and "
      f"{abs(omega_back(a0_mcg,H0_P)-OMEGA_L_P)/SIG_OMEGA_P:.0f} sigma from Planck. With the RAR's own +/-20% systematics the "
      f"identity constrains Omega_L to [{band[0]:.2f}, {band[1]:.2f}], a +/-40% statement, not +0.07%. The tie a_0 ~ sqrt(G rho_L) "
      f"at the 20-30% level is the long-known MOND coincidence (Milgrom 1983); nothing sharper is delivered")

print("\nA3 -- the 'selection rule' (Q002) and the 'flatness residual' (G052)")
a0_crit = a0_from(1.0, H0_P)
print(f"    (c/2) sqrt(G rho_crit) = {a0_crit:.4e}; registered alt footing 1.1279e-10 ({100*(a0_crit/A0['alt']-1):+.2f}%) -> identity returns Omega = {omega_back(A0['alt'], H0_P):.4f}")
om_dm_res = 1 - om_back - OMEGA_B_P
print(f"    G052 'flatness residual' Omega_dm = 1 - Omega_L(returned) - Omega_b = {om_dm_res:.4f} vs Planck {OMEGA_DM_P} (registered a_0)")
res_band = {name: 1 - omega_back(a, H0_P) - OMEGA_B_P for name, a in indep.items()}
res_band["McGaugh -20% syst"] = 1 - omega_back(a0_mcg * 0.8, H0_P) - OMEGA_B_P
res_band["McGaugh +20% syst"] = 1 - omega_back(a0_mcg * 1.2, H0_P) - OMEGA_B_P
for k, v in res_band.items(): print(f"    flatness residual with a_0 from {k}: Omega_dm = {v:+.3f}")
OUT["A3"] = dict(a0_crit=a0_crit, omega_alt=omega_back(A0["alt"], H0_P), omega_dm_residual=om_dm_res, residual_band=res_band)
check("A3 [THE 'FLATNESS RESIDUAL' PREDICTS Omega_dm, AND THE ALT-FOOTING 'EXCLUSION' SELECTS SOMETHING] the residual "
      "1 - Omega_L(identity) - Omega_b is evaluated for the registered a_0 and for every galactic a_0 on the record "
      "including the RAR's +/-20% systematic band; the prediction is real only if it stays within 0.03 of Planck's "
      "Omega_dm across that band; the alt footing is rebuilt as (c/2) sqrt(G rho_crit) to see what its 'exclusion' means",
      all(abs(v - OMEGA_DM_P) < 0.03 for v in res_band.values()),
      f"with the registered (fed-back) a_0 the residual is {om_dm_res:.4f}; with any galactic a_0 it runs from "
      f"{min(res_band.values()):+.2f} to {max(res_band.values()):+.2f} -- negative dark matter over most of the RAR's own "
      f"systematic band. The 'prediction' of Omega_dm is Planck's Omega_Lambda fed back. The alt footing is the "
      f"critical-density convention to {100*(a0_crit/A0['alt']-1):+.2f}%, so its identity value {omega_back(A0['alt'],H0_P):.3f} is 1 by "
      f"construction and Q002's '44 sigma exclusion' is the statement rho_crit != rho_Lambda, which selects nothing about "
      f"galaxies. The 'parameter count = 0' of G038/G052 therefore omits the cold-dust abundance (Planck's Omega_dm by "
      f"feedback) and the cluster/Milky-Way dust normalisation (fitted: G059, G003 V5)")

# =====================================================================================================
print("\n" + "=" * 100); print("PART B -- rung 4: is the temperature DERIVED from the equilibrium, or is the profile ASSUMED?"); print("=" * 100)
print("B1 -- hydrostatic balance of an isothermal fluid in the scalar's deep force g = C/r (sympy)")
r, Cc, s2, A = sp.symbols('r C sigma2 A', positive=True)
rho = sp.Function('rho')
sol = sp.dsolve(sp.Eq(sp.diff(rho(r) * s2, r), -rho(r) * Cc / r), rho(r))
print(f"    d(rho sigma^2)/dr = -rho C/r  =>  {sol}")
gam = sp.symbols('gamma', positive=True)
rho_pow = A * r ** (-gam)
resid_pow = sp.simplify(sp.diff(rho_pow * s2, r) + rho_pow * Cc / r)
s2_of_gamma = sp.solve(sp.Eq(resid_pow, 0), s2)
print(f"    a power law rho = A r^-gamma balances iff sigma^2 = {s2_of_gamma} -- for EVERY gamma, with A FREE")
OUT["B1"] = dict(general_solution=str(sol), sigma2_of_gamma=str(s2_of_gamma))
# numerical illustration at the Milky-Way mass, both footings
Mb = 6.5e10 * MSUN
for tag, a0 in A0.items():
    Cv = math.sqrt(G * Mb * a0)
    print(f"    [{tag}] C = sqrt(G M_b a0) = {Cv:.3e} m^2/s^2: sigma^2 = C/2 -> rho ~ r^-2 (the phantom); "
          f"C/3 -> r^-3; 2C/3 -> r^-1.5; every choice is an exact equilibrium ({math.sqrt(Cv/2)/1e3:.1f} / {math.sqrt(Cv/3)/1e3:.1f} / {math.sqrt(2*Cv/3)/1e3:.1f} km/s)")
check("B1 [HYDROSTATIC BALANCE IN A 1/r FORCE DOES NOT FIX THE TEMPERATURE] the balance equation is solved in "
      "general; the temperature is fixed only if the general solution admits a single sigma^2, whereas a "
      "one-parameter family sigma^2 = C/gamma with a free amplitude A means sigma^2 = C/2 is equivalent to "
      "ASSUMING the r^-2 profile (the phantom) rather than deriving it",
      len(s2_of_gamma) == 1 and (gam not in s2_of_gamma[0].free_symbols),
      f"general solution rho = A r^(-C/sigma^2): sigma^2 and A are both integration data. sigma^2 = C/2 <=> gamma = 2 <=> "
      f"'the dust IS the phantom' -- G046 PART 3/4 and G056 V2a ('the log-potential virial 2 sigma^2 = g r') both insert "
      f"gamma = 2 and read the temperature back out. Q001's identity P/rho = C/2 uses L247's matched law, which was "
      f"CONSTRUCTED to yield the phantom and which L247 itself records as leaving the amplitude C free. Three restatements "
      f"of PAPER29's rung 5, not three derivations of rung 4. Verdict of PAPER29 (POSTULATED) stands. [FAIL is the finding]")

print("\nB2 -- G046's own scorecard (the lane STATE cites for 'DERIVED')")
g046 = rd("glm53_push/G046_temperature_from_action_results.json")
if g046:
    d = json.loads(g046); fails = [c["name"][:70] for c in d["checks"] if not c["pass"]]
    print(f"    G046: {d['pass']} PASS / {d['fail']} FAIL; failed: " + "; ".join(fails))
    log = rd("glm53_push/G046_run.log") or ""
    mrm = re.search(r"\[canonical/MW\] a0=[0-9.e-]+: rM=([0-9.]+) kpc.*?rho_ph\(R0\)=([0-9.]+) Msun/pc\^3", log)
    rM_g046, rho_g046 = (float(mrm.group(1)), float(mrm.group(2))) if mrm else (float("nan"), float("nan"))
    rM_true = math.sqrt(G * Mb / A0["canonical"]) / KPC
    rho_true = math.sqrt(G * Mb * A0["canonical"]) / (4 * math.pi * G * (8.2 * KPC) ** 2) / (MSUN / PC ** 3)
    print(f"    G046 prints r_M(MW) = {rM_g046} kpc and rho_ph(R0) = {rho_g046} Msun/pc^3; closed forms give {rM_true:.2f} kpc and {rho_true:.4f} Msun/pc^3 "
          f"(factors {rM_g046/rM_true:.0f} and {rho_g046/rho_true:.0f})")
    OUT["B2"] = dict(g046_pass=d["pass"], g046_fail=d["fail"], rM_print=rM_g046, rM_true=rM_true, rho_print=rho_g046, rho_true=rho_true)
    check("B2 [G046 SUPPORTS ITS 'PROMOTED' VERDICT ON ITS OWN CHECKS] the lane's committed results file is read; "
          "the promotion is supported only if the checks it names as the derivation (V3.2, V4.1, V4.2) and the "
          "numerical confirmation (V2 full sphere) PASS and its dimensional realisation reproduces the master-table "
          "r_M within 1%",
          d["fail"] == 0 and abs(rM_g046 / rM_true - 1) < 0.01,
          f"3 of 11 checks pass; the three 'derivation' checks and the full-sphere integration all FAIL in the lane's own "
          f"output (integrated density deviation 100%, falsifier amplitude 0.000), and its dimensional block is off by "
          f"10^3 in r_M and 10^6 in density (a pc/kpc slip). The log ends 'rung 4 PROMOTED' regardless. STATE.md and "
          f"REFEREE_ATTACKS.md cite this lane as one of the three routes")
else:
    check("B2 [G046 results file present]", False, "glm53_push/G046_temperature_from_action_results.json missing")

print("\nB3 -- the double count, under G046's stated rule that the dust sources the SAME sourced equation")
print("    'the SAME field equation that gives the baryons' MOND force mediates the dust's self-gravity' (G046 V1.1).")
print("    The phantom is rho_ph = C/(4 pi G r^2), M_ph(r) = C r/G, whose Newtonian pull alone is C/r = the deep MOND force.")
rows = {}
for tag, a0 in A0.items():
    Cv = math.sqrt(G * Mb * a0); rM = math.sqrt(G * Mb / a0); vflat = (G * Mb * a0) ** 0.25
    rows[tag] = {}
    for xr in (2.0, 5.0, 10.0):
        rr = xr * rM
        gN_b = G * Mb / rr ** 2; gN_d = Cv / rr
        g_i = solve_mu2(gN_b, a0)                       # (i) MOND response to baryons only
        g_ii = gN_b + gN_d                              # (ii) Newton: baryons + dust (no scalar force on anything)
        g_iii = solve_mu2(gN_b + gN_d, a0)              # (iii) G046's rule: dust sources the same equation
        g_iv = gN_d + g_i                               # (iv) dust Newtonian + baryons scalar-boosted
        v = lambda g: math.sqrt(g * rr) / vflat
        rows[tag][xr] = dict(i=v(g_i), ii=v(g_ii), iii=v(g_iii), iv=v(g_iv))
        print(f"    [{tag}] r = {xr:4.1f} r_M ({rr/KPC:6.1f} kpc): v/v_flat = (i) MOND-only {v(g_i):.3f} | (ii) Newton with the dust {v(g_ii):.3f} | "
              f"(iii) dust as a source of the same equation {v(g_iii):.3f} | (iv) dust Newton + baryons boosted {v(g_iv):.3f}")
OUT["B3"] = rows
w_iii = max(rows[t][5.0]["iii"] for t in A0); w_iv = max(rows[t][5.0]["iv"] for t in A0)
check("B3 [THE EQUILIBRIUM READING WITH THE SCALAR FORCE KEEPS THE OUTER CURVE FLAT] the mu_2 sourced equation is "
      "solved at 2, 5 and 10 r_M for a Milky-Way-mass baryon well with the phantom-density dust included as a "
      "source (G046's rule), and separately with the dust's Newtonian pull added to the baryons' MOND response; "
      "the reading is consistent only if the curve stays within 10% of v_flat out to 5 r_M in at least one of them",
      abs(w_iii - 1) < 0.10 or abs(w_iv - 1) < 0.10,
      f"at 5 r_M the curve is {w_iii:.2f} v_flat under (iii) (rising as (r/r_M)^(1/4): g^2 = a0 g_N with g_N ~ C/r gives "
      f"v^2 ~ sqrt(a0 C r)) and {w_iv:.2f} v_flat under (iv) (2C/r: BTFR mass normalisation off by 4). Only (ii), Newtonian "
      f"gravity with the dust and NO scalar force, is flat -- and (ii) is a cold-dark-matter halo with a prescribed "
      f"profile, in which the scalar does nothing dynamically and the halo amplitude A is free (B1). This is the "
      f"2.7-4.4x double-counting liability (STANDING rev. 6) in closed form; G003's claim that the identification "
      f"'dissolves' it is the opposite of what the equation says")

# =====================================================================================================
print("\n" + "=" * 100); print("PART C -- the completion, and the referee document's answers"); print("=" * 100)
print("C1 -- Cassini, by inheritance")
h011 = rd("hy4_push/H011_results.out") or ""
same_static = ("df/dK = mu_2(sqrt K)" in h011) and ("Same relation as the aether version, same function, same calibration" in h011)
l243 = rd("fable_independent_2026/L243_onefunction_cassini_quadrupole.out") or ""
mc = re.search(r"canonical eta = [0-9.]+: .*?= ([0-9.]+)x ceiling", l243); ma = re.search(r"alt\s+eta = [0-9.]+: .*?= ([0-9.]+)x ceiling", l243)
q_can, q_alt = (float(mc.group(1)) if mc else float("nan")), (float(ma.group(1)) if ma else float("nan"))
print(f"    H011 states the frozen scalar's static law is the same mu_2 AQUAL equation: {same_static}")
print(f"    L243 (exact AQUAL, mu_2): EFE quadrupole = {q_can}x / {q_alt}x the Park 2026 Cassini ceiling (canonical / alt)")
OUT["C1"] = dict(same_static_law=same_static, q_over_ceiling=[q_can, q_alt])
check("C1 [THE FROZEN-SCALAR COMPLETION CLEARS CASSINI] the completion's own lane asserts its static law is the "
      "mu_2 AQUAL equation; the exact-AQUAL Cassini quadrupole of that equation is on the record (L243); the "
      "completion passes only if that quadrupole is below the ceiling on at least one footing",
      same_static and min(q_can, q_alt) < 1.0,
      f"same static law (H011 M1/M2), so the committed {q_can}x/{q_alt}x is inherited unchanged. REFEREE_ATTACKS 1.1 "
      f"answers Cassini with Horn A (G032), a DIFFERENT theory (next check); for the frozen scalar it is an open kill, "
      f"not 'ANSWERED'")

print("\nC2 -- one completion or two?")
g032 = rd("glm53_push/G032_horn_a_fixed_congruence.out") or ""
lv_cost = "explicit local Lorentz violation" in g032
no_lv = re.search(r"Lorentz violation\s*:\s*none", h011) is not None
g043 = rd("glm53_push/G043_mimetic_embedding.out") or ""
not_gauge = "The Lorentz-violation cost does NOT dissolve" in g043
print(f"    G032 Horn A (the PPN answer, alpha_1 = 0 'by architecture'): states its cost as explicit local Lorentz violation: {lv_cost}")
print(f"    H011 frozen scalar (the Lorentz-invariance answer): states 'Lorentz violation: none': {no_lv}; G043: the congruence is not a gauge: {not_gauge}")
OUT["C2"] = dict(hornA_LV_cost=lv_cost, frozen_no_LV=no_lv, congruence_not_gauge=not_gauge)
check("C2 [THE REFEREE DOCUMENT'S PPN ANSWER AND ITS LORENTZ-INVARIANCE ANSWER COME FROM ONE THEORY] the two "
      "committed outputs are read; the answers are compatible only if the theory that delivers alpha_1 = 0 is the "
      "theory that has no preferred frame",
      not (lv_cost and no_lv and not_gauge),
      "Horn A buys alpha_1 = 0 with a fixed congruence that G032 itself calls explicit local Lorentz violation and "
      "G043 proves is not a gauge choice; the frozen scalar has no congruence and therefore no Horn-A PPN result. "
      "REFEREE_ATTACKS 1.1/1.2 cite Horn A for PPN and 4.x/H011 for Lorentz invariance as if they were one completion")

print("\nC3 -- what carries the lensing, the cluster bulk and the Milky Way's dark mass")
g003 = json.loads(rd("glm53_push/G003_results.json") or "{}")
v5 = next((c for c in g003.get("checks", []) if c["name"].startswith("V5")), None)
m17 = re.search(r"a factor (\d+) short", v5["measured"]) if v5 else None
short = int(m17.group(1)) if m17 else None
print(f"    G003 V5 (Milky Way, capped phantom), recorded as PASS: '{v5['measured'] if v5 else 'n/a'}'")
print(f"    REFEREE_ATTACKS 2.1: 'Lensing = GR + the dust'; 2.4: cluster amplitude 'OPEN-HONEST'; G059: no partition closes; L248: cap at 5.8 kpc, lensing bins start at 35 kpc")
OUT["C3"] = dict(mw_factor_short=short)
check("C3 [THE SECTOR THAT CARRIES LENSING, THE CLUSTER BULK AND THE MILKY WAY'S OUTER MASS HAS A DERIVED ABUNDANCE] "
      "the tracks' own outputs are read for the mass the phantom fails to supply and for who supplies it",
      short is not None and short <= 2,
      f"the capped phantom is a factor {short} short in the Milky Way (G003 V5, printed PASS), the cluster residual is "
      f"open (G059), and the weak-lensing signal is carried entirely by 'the dust as ordinary matter' (REFEREE 2.1, L248). "
      f"That dust has Planck's Omega_dm (A3), a fitted cluster normalisation and 94% of the Milky Way's dark mass: it is "
      f"cold dark matter under another name, and the scalar's only remaining job -- the galactic RAR -- double-counts with "
      f"it (B3). The honest description is Lambda-CDM plus a scalar, not a replacement for it")

print("\nC4 -- the uncommitted G062 Milky-Way draft, and the Milky Way on the certified solve")
g062 = rd("glm53_push/G062_results.json")
if g062:
    d = json.loads(g062); sm = d.get("summary", {})
    v0c = next((c["measured"] for c in d["checks"] if c["name"].startswith("V0c")), "")
    v0d = next((c["measured"] for c in d["checks"] if c["name"].startswith("V0d")), "")
    print(f"    G062: {sm.get('pass')} PASS / {sm.get('fail')} FAIL; V0c '{v0c[:80]}'; V0d '{v0d[:70]}'")
    print(f"    G062 'required mass' {d['required_mass']['canonical']['M']:.3e} Msun = {d['required_mass']['canonical']['ratio_mid']:.2f}x the budget -- "
          f"from v_flat = (G M a0)^(1/4), the DEEP-MOND amplitude, applied at R_0 where g_N ~ 1.4 a_0")
    OUT["C4_g062"] = dict(summary=sm, v0c=v0c[:120], v0d=v0d[:120])
for tag, a0 in A0.items():
    R0 = 8.2 * KPC; vs = {}
    for Mb_i in (6.0e10, 6.5e10, 7.0e10, 8.0e10):
        gN = G * Mb_i * MSUN / R0 ** 2; vs[Mb_i] = math.sqrt(solve_mu2(gN, a0) * R0) / 1e3
    print(f"    [{tag}] v_c(R_0 = 8.2 kpc), point-mass mu_2 solve: " + ", ".join(f"M_b = {m/1e10:.1f}e10 -> {v:.0f} km/s" for m, v in vs.items())
          + f"  (g_N/a0 at 6.5e10 = {G*6.5e10*MSUN/R0**2/a0:.2f}; measured 232.5 +/- 5; a disc raises the point-mass value by ~10-15%, L172: 220/225 km/s at 6.7e10)")
    OUT[f"C4_vc_{tag}"] = vs
ok_mw = all(abs(math.sqrt(solve_mu2(G * 7.0e10 * MSUN / (8.2 * KPC) ** 2, a0) * 8.2 * KPC) / 1e3 / 232.5 - 1) < 0.10 for a0 in A0.values())
check("C4 [THE CERTIFIED mu_2 SOLVE PUTS THE MILKY WAY WITHIN 10% OF ITS MEASURED CIRCULAR SPEED FOR THE STANDARD "
      "BARYON BUDGET] the sourced equation is solved at the solar radius for M_b = 7e10 (point mass, both footings) "
      "and compared with 232.5 km/s; G062's 3.4x mass deficit is checked against this",
      ok_mw,
      "the point-mass solve lands within 10% on both footings before the disc correction, so G062's 'required mass "
      "3.4x the budget' is a misuse of the deep-MOND BTFR amplitude at a radius that is not deep MOND. G062 is also "
      "unit-broken (disc/sphere force ratio 10^19, enclosed mass 10^30 'Msun') and fails 15 of its 21 checks: a draft, "
      "not evidence in either direction; it should not be committed as it stands")

# =====================================================================================================
print("\n" + "=" * 100); print("PART D -- the Lean inventory (L258_lean_inventory.py)"); print("=" * 100)
inv = rd("fable_independent_2026/L258_lean_inventory.json")
if inv:
    d = json.loads(inv); tot = d["total"]
    print(f"    {tot['files']} files, {tot['theorems']} theorems; {tot['files_exit0']} files exit 0; "
          f"{tot['theorems_on_nonstandard_axioms']} theorems on non-standard axioms; files with errors: {tot['files_with_errors']}")
    for k, v in d["files"].items():
        if v["n_errors"] or v["theorems_on_nonstandard_axioms"]:
            print(f"      {k}: exit {v['exit']}, {v['n_errors']} errors, on sorryAx: {list(v['theorems_on_nonstandard_axioms'])[:6]}")
    OUT["D"] = tot
    check("D1 [EVERY COMMITTED CERTIFICATE COMPILES ON THE STANDARD AXIOMS] every .lean file in the agent tracks and "
          "this track is compiled against the repository Mathlib with #print axioms on every theorem",
          tot["theorems_on_nonstandard_axioms"] == 0 and not tot["files_with_errors"],
          f"{tot['theorems'] - tot['theorems_on_nonstandard_axioms']} of {tot['theorems']} theorems certify on "
          f"{{propext, Classical.choice, Quot.sound}}; the exceptions are listed above. The glm53/qwen38/hy4/grok/deepseek "
          f"certificates all compile clean. What they certify is algebra: G058's 'one_constant_closure' is the statement "
          f"that rho = 4 a0^2/(G c^2) exists and is unique given a0 (a definition); EQUILIBRIUM_THEORY's identification is "
          f"Milgrom's isothermal-sphere identity; Q001's is P/rho = C/2 for two r^-2 laws. None certifies that any "
          f"equilibrium is reached, stable, or selected -- PAPER29's reading of the word 'certified' stands")
else:
    check("D1 [Lean inventory present]", False, "run fable_independent_2026/L258_lean_inventory.py first")

# =====================================================================================================
n_pass, n = sum(CH), len(CH)
print(f"\nL258 COMPLETE: {n_pass}/{n} checks PASS.")
print("READING: the puzzle is not finished.  Rung 9 (Omega_Lambda 'from a_0') returns the Planck value that built a_0;")
print("rung 4's three 'derivations' each insert the r^-2 profile they claim to derive, and the lane cited for the")
print("promotion fails 8 of its own 11 checks; the completion inherits the Cassini kill through its own static law and")
print("its referee defence splices two incompatible theories; the lensing, cluster and Milky-Way mass is cold dark")
print("matter with a fitted or fed-back abundance.  What STANDS since PAPER29: the honest negatives (G059 partition,")
print("G044 EFE split), the asymmetric-drift channel for the sag (G057, open on sigma_z), the Lean algebra, and this")
print("track's L248/L257 on what lensing does and does not test.  PAPER29's labels are unchanged by the 09-14/15 batch.")
json.dump(dict(pass_count=n_pass, total=n, out=OUT), open(os.path.join(HERE, "L258_results.json"), "w"), indent=1, default=str)
sys.exit(0 if n_pass == n else 1)

#!/usr/bin/env python3
"""CFG195_compare.py -- PHASE 2b: compare CFG195's own saved results with CFG176's committed results JSON (opened only after CFG195's own main and MUTATE runs were saved and hashed).
Row-by-row table; each difference classified NUMBER / MATH / SCOPE / LABEL (frozen classes).  Reads CFG176's results JSON (read-only) and CFG195's own JSONs."""
import json, math, os, numpy as np
from scipy.integrate import solve_ivp, quad
from CFG195_common import Run, find_repo, HERE
run = Run("CFG195_compare", ()); repo = find_repo(); assert repo
L = json.load(open(os.path.join(repo, "campaign_fresh_gravity", "CFG176_dark_energy_flow", "CFG176_de_flow_results.json")))["numbers"]
LM1 = json.load(open(os.path.join(repo, "campaign_fresh_gravity", "CFG176_dark_energy_flow", "CFG176_de_flow_results_MUTATE1.json")))["numbers"]
ld = lambda n: json.load(open(os.path.join(HERE, n)))
D, N, S, Q, F = ld("CFG195_desi_bound_results.json")["numbers"], ld("CFG195_nec_lp_results.json")["numbers"], ld("CFG195_sympy_algebra_results.json")["numbers"], ld("CFG195_q3_q5_numbers_results.json")["numbers"], ld("CFG195_freeform_results.json")["numbers"]
M3 = ld("CFG195_desi_bound_MUTATE3_results.json")["numbers"]
ROWS = []
def row(item, theirs, mine, tol, klass="NUMBER", note="", rel=True):
    t = np.atleast_1d(np.array(theirs, float)); m = np.atleast_1d(np.array(mine, float))
    d = np.abs(m - t) / np.maximum(np.abs(t), 1e-12) if rel else np.abs(m - t)
    ok = bool(np.all(d <= tol)); verdict = "REPRODUCES" if ok else klass
    ROWS.append((item, verdict)); print(f"  {'OK ' if ok else '!! '}{item:62s} CFG176 {np.round(t,5).tolist()}  CFG195 {np.round(m,5).tolist()}  max {'rel' if rel else 'abs'} diff {float(d.max()):.2e}  -> {verdict}" + (f"   [{note}]" if note and not ok else ""))
    return ok
NM = ["DESY5", "Pantheon+", "Union3"]
print("== Q0 controls and Q4 (DESI inputs, the 0.078) ==")
row("R canonical / alt", [L["Q1_table"]["canonical"]["R"], L["Q1_table"]["alt"]["R"]], [D["R"]["canonical"], D["R"]["alt"]], 5e-4)
row("1+w0 97.5th pct", [L["Q4_chains"][n]["onepw0_pct"][4] for n in NM], [D[f"{n}_I2"]["omw0_pct"][4] for n in NM], 3e-3)
row("1+w0 median", [L["Q4_chains"][n]["onepw0_pct"][2] for n in NM], [D[f"{n}_I2"]["omw0_pct"][2] for n in NM], 3e-3)
row("today 3/4(1+w0) 97.5th", [L["Q4_chains"][n]["today_pf_pct"][1] for n in NM], [D[f"{n}_I2"]["today34_975"] for n in NM], 3e-3)
CHd = {n: np.loadtxt(os.path.join(repo, "fable_independent_2026", "data", "desi_dr2_w0wa_thinned", f + ".txt")) for n, f in zip(NM, ("desy5sn", "pantheonplus", "union3"))}
pR = [float(CHd[n][:, 0][0.75 * (1 + CHd[n][:, 1]) >= D["R"]["canonical"]].sum() / CHd[n][:, 0].sum()) for n in NM]
row("p(3(1+w0)/4 >= R) canonical (today's rate alone)", [L["Q4_chains"][n]["p_today_pf_ge_R"]["canonical"] for n in NM], pR, 0.05, note="differences are in the 4th decimal", rel=False)
row("F(k=1/2, isotropic) 97.5th", [L["Q4_chains"][n]["carried_iso_pct"][2] for n in NM], D["I5_table"]["k=1/2 (w_par = w_iso)"], 5e-3)
row("F(k=3/4, perfect fluid) 97.5th   [THE 0.049 / 0.035 / 0.078]", [L["Q4_chains"][n]["carried_pf_pct"][2] for n in NM], [D[f"{n}_F"]["p975"] for n in NM], 5e-3)
row("F(k=3/4) median", [L["Q4_chains"][n]["carried_pf_pct"][0] for n in NM], [D[f"{n}_F"]["p50"] for n in NM], 5e-3)
print("  (crossing) README/CFG6 B5: 0.9998@0.41, 0.9978@0.36, 0.9998@0.44  vs CFG195:", [(round(D[f'{n}_I2']['cross_frac'], 4), round(D[f'{n}_I2']['zcross_med'], 3)) for n in NM], "-> agree at the README's two-decimal rounding; my frozen line demanded 0.36 <= z <= 0.44 unrounded (0.356 and 0.444 miss by 0.004): LABEL/rounding, kept as a FAIL of my own I-3 line")
ROWS.append(("crossing fractions and z_cross (two-decimal)", "REPRODUCES (my unrounded pass line FAILS by 0.004: LABEL)"))
print("\n== thawing best nodes (NEC-respecting healthy field) ==")
lm = [L["Q4_thawing_best_nodes"][n]["carried_pf"] for n in NM]; mm = [D_ if False else Q["I6a"][n]["F34"] for n, D_ in zip(NM, NM)]
row("F(k=3/4), best thawing node", lm, mm, 0.10, klass="LABEL", note="node selection: CFG6 conditions on a 3-d Gaussian in (w0,wa,Omega_m) over an Omega_m x lambda grid; CFG195 uses the best chi^2 node in (w0,wa) at the chain-mean Omega_m on a 20-point lambda grid. Pantheon+ agrees (0.0164 vs 0.0163)")
print("  CFG176 lam:", [L["Q4_thawing_best_nodes"][n]["lam"] for n in NM], " CFG195 lam:", [round(Q["I6a"][n]["lam"], 2) for n in NM])
print("\n== Q1 numbers ==")
row("2R (NEC, w_par)", [L["Q1_table"]["canonical"]["NEC_min_onepw_par"], L["Q1_table"]["alt"]["NEC_min_onepw_par"]], [2 * D["R"]["canonical"], 2 * D["R"]["alt"]], 1e-3)
row("4R/3 (perfect fluid CMB frame)", [L["Q1_table"]["canonical"]["pf_min_onepw_eff"], L["Q1_table"]["alt"]["pf_min_onepw_eff"]], [4 * D["R"]["canonical"] / 3, 4 * D["R"]["alt"] / 3], 1e-3)
Cl = {(r["footing"], r["logM"]): r["C"] for r in L["Q1_compaction"]}
row("C = rho_c/rho_L (8 footing x mass cells)", [Cl[(f, m)] for f in ("canonical", "alt") for m in (9, 10, 11, 12)], [Q["IV4"][f"{f}_{10.0**m:.0e}"][0] for f in ("canonical", "alt") for m in (9, 10, 11, 12)], 1e-3)
row("attraction threshold beta at w=-0.752", L["Q1_attraction_threshold_beta"]["-0.752"], 0.8467, 1e-3, note="CFG195 sympy: (1+b^2)+w(3-b^2)=0")
row("|beta| needed (2 C Omega_L), 1e9..1e12 canonical", [r["beta_needed"] for r in L["Q2_theta_channel_beta_needed"]], [Q["IV4"][f"canonical_{10.0**m:.0e}"][1] for m in (9, 10, 11, 12)], 1e-3)
print("\n== Q2 ==  CFG176 S6 (H^2 = 8 pi G rho/[3(1+beta/2)], beta = c1+3c2+c3, w_flow = w_total) vs CFG195 IV-1: identical (sympy, both); see the CFG195 checks IV-1a..d, IV-2")
ROWS.append(("Q2 minisuperspace factor (1+beta/2)", "REPRODUCES"))
print("\n== Q3-I ==")
q3 = L["Q3_I"]; mq = Q["IV6"]
row("H0 t0, w0", [q3["H0t0"], q3["w"]["0.0"]], [mq["H0t0"], mq["w0"]], 2e-4)
row("CPL fit (w0,wa)", q3["cpl"], mq["cpl"], 1e-3)
row("a0(z)/a0(0) dex at 0.85/1.5/2.5", [q3["dlog_a0"][k] for k in ("0.85", "1.5", "2.5")], [mq["a0dex"][k] for k in ("0.85", "1.5", "2.5")], 2e-3)
row("H(0.5)/H_LCDM - 1", q3["H_over_LCDM"]["0.5"] - 1, mq["H05"], 2e-3)
row("Mahalanobis distance of the model CPL (3 chains)", [q3["chains"][n]["mahal_model"] for n in NM], [36.058, 33.951, 27.476], 1e-3, note="CFG195 numbers read from its .out")
print("\n== Q5 ==")
nf = L["Q5_null_flow"]["canonical"]; row("Omega_null, z_dom (canonical)", [nf["Omega_null0"], nf["z_eq_matter"]], [0.202, 0.542], 3e-3, note="CFG195 numbers from its .out (3 dp)")
pg = L["Q5_PG_linear"]; row("PG cross-term rho_x/rho_L (1e9..1e12)", [abs(r["rho_x_over_rhoL"]) for r in pg], [1233.6, 693.7, 390.1, 219.4], 1e-3)
row("PG cross-term pull/a0", [r["g_cross_over_a0"] for r in pg], [0.0008, 0.0014, 0.0026, 0.0046], 0.08, note="CFG195 numbers rounded to 4 dp")
print("\n== E8/E9 (hand estimates from Phase 1): fraction of each posterior whose TODAY momentum limit reaches R, by bound ==")
for lab, k in (("k=1/2 (w_par = w_iso)", 0.5), ("k=3/4 (perfect fluid)", 0.75), ("k=sqrt3/2 (NEC-only maximum)", math.sqrt(3) / 2)):
    fr = [float(CHd[n][:, 0][k * (1 + CHd[n][:, 1]) >= D["R"]["canonical"]].sum() / CHd[n][:, 0].sum()) for n in NM]
    print(f"  {lab:32s} DESY5 {fr[0]:.4f}  Pantheon+ {fr[1]:.4f}  Union3 {fr[2]:.4f}"); run.num("today_reach_R_" + lab.split()[0], fr)
print("\n== Bianchi I coefficient (reported by CFG176, not scored) ==")
OM, OLb = 0.3111, 0.6889
def solve(Om_):
    E = lambda x: math.sqrt(Om_ * math.exp(-3 * x) + 1 - Om_); s = solve_ivp(lambda x, y: [3 * (1 - Om_) / E(x) - 3 * y[0]], (-12, 0), [0.0], rtol=1e-10, atol=1e-14); return float(s.y[0, -1])
Dh = solve(OM); sig1 = 2 * Dh / 3
Sc = 2 * OLb * quad(lambda a: a * a / math.sqrt(OM / a ** 3 + OLb), 0, 1)[0]
print(f"  CFG195 ODE: D(t0)/H0 = {Dh:.4f} x (p_par - p_perp)/rho; the component sigma_1 = H_x - Hbar = (2/3) D -> {sig1:.4f}; CFG176 coefficient {L['Q4_shear']['coef']:.4f} (their 2 Omega_L int a^2/E da at Om=0.3111 = {Sc:.4f})")
row("Bianchi coefficient sigma_1/H0 per unit Delta (Om=0.3111)", L["Q4_shear"]["coef"], sig1, 2e-3, klass="LABEL", note="my frozen E20 used sigma = D/sqrt3; the coefficient reproduces with sigma_1 = (2/3) D")
print("  CFG176's Delta_req = 1.5(2R - eps_max), eps_max = 97.5th pct of TODAY'S 1+w0 (0.511): the '4-11% anisotropy' closes the TODAY-rate shortfall (2R = 0.586 vs 0.511), NOT the integrated 3.8x shortfall (0.078 vs 0.293): SCOPE (wording in the README's bottom line)")
ROWS.append(("'closing the gap needs a 4-11% anisotropy' (defined against today's rate, not the integrated column)", "SCOPE"))
print("\n== MUTATE cross-check ==")
theirs_dust = [LM1["Q4_chains"][n]["carried_pf_pct"][2] for n in NM]; mine_dust = [0.75 * M3[f"{n}_F"]["p975"] for n in NM]
row("CFG176 MUTATE=1 vs CFG195 M3 (dust inertia): F 97.5th pct at k=3/4-equivalent", theirs_dust, mine_dust, 5e-3)
print("\n== What CFG195 adds, none of which is in CFG176 (classification of the differences of substance) ==")
print(f"  SCOPE  NEC-only maximum of g/e is (sqrt3/2)(1+w_iso) (CFG195 LP: {list(N['II2_ratios'].values())[0]:.5f}), not the perfect-fluid 3/4: the 97.5th pct of F becomes {[round(x,4) for x in D['I5_table']['k=sqrt3/2 (NEC-only maximum, see CFG195_nec_lp)']]} (x1.1547); CFG176's own inequality g/e <= (1+w_par)/2 is true but not sufficient")
print("  SCOPE  the bound assumes a single NEC-respecting component; with a phantom compensator (w_ph >= -2) R is reachable at total 1+w = 0.05 with phantom fraction ~0.29 (CFG195 A6)")
print("  SCOPE  the CPL posterior is phantom (NEC-violating at rest) for 65-71% of cosmic time (CFG195 A4a) and CFG176 clips those epochs to zero; a free-form NEC-respecting rho_DE(z) that mimics the CPL background within 1-2% can carry F_max above R when Omega_m is left free (CFG195 A3), and near R at 2% with Omega_m fixed: tolerance- and parameterisation-dependent")
print("  LABEL  C range 1.13e4-4.77e5 spans both footings, |beta| range printed 1.6e4-4.9e5 is canonical only (both footings: 1.55e4-6.53e5)")
run.num("rows", [{"item": a, "verdict": b} for a, b in ROWS])
nb = sum(1 for _, v in ROWS if v.startswith("REPRODUCES")); print(f"\n{nb}/{len(ROWS)} rows reproduce; others classified above")
run.check("compare: the load-bearing README numbers (F 97.5th, 1+w0, C, Q3-I) reproduce within tolerance", f"{nb}/{len(ROWS)}", all(v.startswith("REPRODUCES") for a, v in ROWS if a.startswith("F(k=3/4, perfect") or a.startswith("1+w0 97.5") or a.startswith("C =") or a.startswith("H0 t0")))
run.finish()

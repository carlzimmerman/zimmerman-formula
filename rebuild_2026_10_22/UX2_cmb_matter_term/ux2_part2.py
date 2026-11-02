#!/usr/bin/env python3
"""UX2 P2a, P2c and the computed rows: required density history from RF5; X-COP and the dwarf/IC-regime nu shift for SZ's published f = x; the hydrostatic
term and K-shape stiffness at the benchmarks' caption parameters; mu at each. Frozen: FROZEN_CRITERIA.md. UX2_MUTATE=1: density exponent -2.9, K1 must fail.
kappa = 1/2 FITTED; footings never pooled; cold sector stays retired; not theory closed."""
import json, math, os, pickle, sys
import numpy as np
MUT = os.environ.get("UX2_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""; EXPO = 2.9 if MUT else 3.0
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO = os.path.dirname(RB)
G = 6.6743e-11; MPC = 3.0857e22; MS = 1.98847e30; C = 299792458.0; OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
A0 = dict(canonical=9.3603e-11, alt=1.1312e-10)
RCH2 = 3 * (1e5 / MPC) ** 2 / (8 * math.pi * G)           # kg/m^3 per h^2
R = dict(mutate=MUT, rho_crit_per_h2_kg_m3=RCH2)
rf = json.load(open(os.path.join(RB, "RF5_growth_native_yardstick", "rf5_results.json")))
win = [k for k, v in rf["cells"].items() if v.get("window_pass")]
P(f"RF5 window cells: {win}")
rows = []
for k in win:
    c = rf["cells"][k]; p = c["params"]; wx, wb, h = p["omega_c"], p["omega_b"], c["h"]; Om = c["Omega_m"]
    Ode = 1 - Om - 2.47e-5 * 1.68 / h ** 2 * 1.0
    rows.append(dict(cell=k, zon=c["zon"], omega_x=wx, omega_b=wb, ratio=wx / wb, h=h, Omega_m=Om, a0_can=c["a0"]["canonical"]["a0_0"], a0_alt=c["a0"]["alt"]["a0_0"], a0z_can=c["a0"]["canonical"]["a0_2.33"], a0z_alt=c["a0"]["alt"]["a0_2.33"], sqrtX=c["sqrtX"]))
R["window_cells"] = rows
wxs = np.array([r["omega_x"] for r in rows]); wbs = np.array([r["omega_b"] for r in rows]); rts = wxs / wbs
wx = float(np.median(wxs)); wb = float(np.median(wbs)); h = float(np.median([r["h"] for r in rows]))
R["omega_x"] = dict(median=wx, lo=float(wxs.min()), hi=float(wxs.max())); R["ratio"] = dict(median=float(np.median(rts)), lo=float(rts.min()), hi=float(rts.max()))
P(f"omega_x median {wx:.5f} [{wxs.min():.5f}, {wxs.max():.5f}] ; omega_b {wb:.5f}; ratio {np.median(rts):.3f} [{rts.min():.3f}, {rts.max():.3f}] (this fit's own output, not an input)")
wg = 2.473e-5; wr = wg * (1 + 3.044 * 7 / 8 * (4 / 11) ** (4 / 3))
zeq = (wx + wb) / wr - 1; R["z_eq_from_fit"] = zeq
hist = []
rhoDE0 = None
for z in (0.0, 0.5, 1.0, 2.33, 10.0, 1059.0, 1090.0, zeq, 3e4, 1e5, 1e6):
    r = wx * RCH2 * (1 + z) ** EXPO; hist.append(dict(z=z, rho_x_kg_m3=r, rho_x_Msun_Mpc3=r * MPC ** 3 / MS, over_rho_b=wx / wb, over_rho_r=wx * (1 + z) ** 3 / (wr * (1 + z) ** 4)))
    P(f"  z {z:>10.1f}: rho_x {r:.4e} kg/m^3, {r * MPC ** 3 / MS:.4e} Msun/Mpc^3, x/radiation {wx / (wr * (1 + z)):.4g}")
R["history"] = hist; R["zeq"] = zeq
# K1: independent arithmetic. rho_c = 1.87834e-26 h^2 kg/m^3 (from CODATA G, 1 Mpc); z = 1090
k1a = abs(RCH2 / 1.8783e-26 - 1); k1b = abs(hist[6]["rho_x_kg_m3"] / (wx * 1.87829e-26 * 1091 ** 3) - 1)
R["K1"] = dict(a=k1a, b=k1b, passed=bool(k1a <= 1e-3 and k1b <= 1e-3)); P(f"K1 rho_c {k1a:.2e} rho(1090) {k1b:.2e} -> {'PASS' if R['K1']['passed'] else 'FAIL'}")
# rho_DE(0), both footings through a0 = kappa c sqrt(G rho_DE); canonical read-off vs alt read-off from RF5
for f in A0:
    rde = (A0[f] / (0.5 * C)) ** 2 / G; R.setdefault("rho_from_footing", {})[f] = rde
    P(f"[{f}] a0 {A0[f]:.4e} -> rho = (a0/(kappa c))^2/G = {rde:.4e} kg/m^3; rho_x(0)/rho = {wx * RCH2 / rde:.4f}; RF5 window a0(0) {min(r['a0_can' if f == 'canonical' else 'a0_alt'] for r in rows):.4e}-{max(r['a0_can' if f == 'canonical' else 'a0_alt'] for r in rows):.4e}, a0(2.33) {min(r['a0z_can' if f == 'canonical' else 'a0z_alt'] for r in rows):.3e}-{max(r['a0z_can' if f == 'canonical' else 'a0z_alt'] for r in rows):.3e}")
# P2c: the size of the matter term relative to baryons in the a0 law's background
P(f"matter term the law's rho_DE assumes: omega_m = {wx + wb:.4f}, baryons {wb:.4f}: non-baryonic share {wx / (wx + wb):.3f}")
cf = os.path.join(REPO, "campaign_fresh_gravity", "CFG689_native_ruler_bao"); cfr = {}
for m in ("", "_B4m", "_B4p", "_B5a", "_B9"):
    d = json.load(open(os.path.join(cf, f"cfg689{m}.json"))); cfr[m or "primary"] = dict(ruler=d["ruler"], cfg={k: v for k, v in d["cfg"].items() if isinstance(v, (int, float, str, bool))})
R["cfg689"] = cfr
# nu family on X-COP: SZ f = x, nu = 1 + 1/sqrt(y), the family's upper envelope; law = simple
_C = pickle.load(open(os.path.join(RB, "SL1_symbolic_law_search", "cache", "sl1_cache.pkl"), "rb")); GE, MSE, MPCE = _C["const"]["GE"], _C["const"]["MSUNE"], _C["const"]["MPCE"]
nu_law = lambda y: 0.5 + np.sqrt(0.25 + 1 / y); nu_sz = lambda y: 1 + 1 / np.sqrt(y)
for f, a0 in A0.items():
    res = {}
    for name, nu in (("law", nu_law), ("SZ_f=x", nu_sz)):
        d = []; ys = []
        for z in _C["xcop"]["canonical"]["rows"]:
            if z["x"] > 0.75: continue
            r = z["r_kpc"] * 1e3 * MPCE / 1e6; Mb = z["Mb_Msun"] * MSE; gN = GE * Mb / r ** 2; y = gN / a0
            d.append(math.log10(z["MHSE_Msun"] / (float(nu(y)) * z["Mb_Msun"]))); ys.append(y)
        d = np.array(d); res[name] = dict(mean=float(d.mean()), rms=float(np.sqrt((d ** 2).mean())), n=len(d), factor=float(10 ** d.mean()), ymed=float(np.median(ys)))
    R.setdefault("xcop", {})[f] = res; P(f"[{f}] X-COP log(M_HSE/M_model): law {res['law']['mean']:+.3f} rms {res['law']['rms']:.3f}; SZ f=x {res['SZ_f=x']['mean']:+.3f} rms {res['SZ_f=x']['rms']:.3f}, factor {res['SZ_f=x']['factor']:.2f}; median y {res['law']['ymed']:.2f}")
# nu ratio by acceleration regime
R["nu_ratio"] = {f"{y:g}": float(nu_sz(y) / nu_law(y)) for y in (0.01, 0.05, 0.1, 0.3, 1.0, 3.0, 10.0)}; P(f"nu_SZ/nu_law by y: {R['nu_ratio']}")
# Benchmarks: mu, stiffness in a static well, and the K-shape's sound speed (SZ21 caption values as C7 read them)
B = {"PC1 Cosh": dict(KB=0.5, Q0=0.1, K2=7.5e3, Z0=1e-9, kpp0=lambda k2: 2 * k2), "PC2 Exp": dict(KB=0.1, Q0=1e-4, K2=9.5e3, Z0=1e-17, kpp0=lambda k2: 4 * k2)}
for n, b in B.items():
    mu2 = b["kpp0"](b["K2"]) * b["Q0"] ** 2 / (2 - b["KB"]); mu = math.sqrt(mu2); sig2 = b["Z0"] / b["Q0"]
    e = dict(mu_quadratic_per_Mpc=mu, mu_inv_Mpc=1 / mu, Z0_over_Q0=sig2, sigma_kms=math.sqrt(sig2) * C / 1e3, Z_at_Psi={})
    for psi in (1e-7, 1e-6, 1e-5): e["Z_at_Psi"][f"{psi:g}"] = b["Q0"] * psi / b["Z0"]
    e["g_physical"] = 1 - b["KB"] / 2; R.setdefault("benchmarks", {})[n] = e; P(f"{n}: mu(quadratic expansion at Z=0) {mu:.4g}/Mpc, mu^-1 {1 / mu:.4g} Mpc; Z0/Q0 {sig2:.1e} -> sqrt {e['sigma_kms']:.3g} km/s; Z=Q0 Psi/Z0 at Psi 1e-7,1e-6,1e-5: {list(e['Z_at_Psi'].values())}; g {e['g_physical']}")
# hydrostatic quadratic branch: rho = mu^2 |Phi|/(4 pi G) against disc scale, at the paper's bound mu^-1 = 1 Mpc
kms2 = 1e6; rhobar = wx * RCH2
for mi in (1.0, 0.1):
    mu_si = 1 / (mi * MPC)
    for V in (50.0, 200.0, 1000.0):
        Phi = 3 * (V * 1e3) ** 2; rho = mu_si ** 2 * Phi / (4 * math.pi * G); M8 = 4 / 3 * math.pi * (8e3 * 3.0857e16) ** 3 * rho / MS
        R.setdefault("hydro", []).append(dict(mu_inv_Mpc=mi, V=V, rho_kg_m3=rho, over_cosmic_mean=rho / rhobar, Msun_pc3=rho * (3.0857e16) ** 3 / MS, M_inside_8kpc=M8))
        P(f"hydrostatic quadratic mu^-1 {mi} Mpc, V {V:.0f} (Phi=3V^2): rho {rho * (3.0857e16) ** 3 / MS:.3e} Msun/pc^3, {rho / rhobar:.1f} x cosmic mean rho_x, inside 8 kpc {M8:.2e} Msun")
json.dump(R, open(os.path.join(HERE, f"ux2_part2{TAG}.json"), "w"), indent=1, sort_keys=True); open(os.path.join(HERE, f"ux2_part2{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if R["K1"]["passed"] else 1)

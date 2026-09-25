"""Deep-MOND IFU forecast (2026-09-25): what one NIRSpec IFU velocity field per verified target can decide.

Inputs are the VERIFIED ledger only (highz_target_ledger_verified_2026.py; every row re-read from its paper).
Three zero-parameter hypotheses for the low-acceleration scale at redshift z (ratio R(z) = a0(z)/a0(0)):
  H-CONST  R = 1                              (a0 a constant; the dark-energy-density reading, w = -1)
  H-LCDM   R = E^{4/3} [c^2/f(c)](z)/[..](0)  (LambdaCDM's emergent halo RAR scale; same law as
                                               a0z_lcdm_native_hypothesis_2026.py, DM14 concentrations,
                                               evaluated at halo masses 1e11 and 1e12 Msun)
  H-HUBBLE R = E(z)                           (a0 = c H(z)/const, the "cosmic coincidence" scaling)
In the deep-MOND limit V^4 = G M_b a0, so log a0 = 4 log V_c - log M_b - log G and the hypotheses
differ by log R(z) at fixed M_b.

CORRECTED 2026-09-25 (same day as the first commit df4373ee8): parts C and D first used that deep-limit formula.
At the gate (y = g_bar/a0 = 0.2-0.3) and at target 1's face-value accelerations it is wrong in both directions
that mattered: it UNDERSTATED the per-object error (0.29 -> 0.43 dex, JWST only) and OVERSTATED the gas a
constant a0 needs (so the first version's "face-value lean against constant a0" is withdrawn). Both parts now
use the full RAR kernel, the intrinsic scatter and the halo-to-halo scatter (numbers as MNRAS v2 S4).

SCOPE / CAVEATS (read before quoting anything):
  * This tests the three HYPOTHESES above, not the framework as a whole. The framework's own z ~ 2.5
    prediction carries the open L189 retained-halo correction (OBSERVING_CASE_A0Z_2026.md, 09-12 note):
    a retained cold halo can shift its zero point by ~+0.2 dex in mass, which would put it between
    H-CONST and H-LCDM. That correction is NOT computed here.
  * Part C is a face-value read of PUBLISHED ground-based kinematics (Keck/OSIRIS, V = Dv/2, not
    inclination-corrected) and is NOT a measurement of a0. It shows what gas mass each hypothesis needs.
  * The error budget in part D is an assumed budget, not an exposure-time-calculator result.
"""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: print(*a, flush=True)
FAILS = []; NCHK = [0]
def check(name, ok, detail=""):
    NCHK[0] += 1
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    if not ok: FAILS.append(name)

G = 6.674e-11; MSUN = 1.989e30; KMS = 1e3
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}          # both footings, always
OM, OL, h = 0.3150, 0.6850, 0.674                      # same as a0z_fork_likelihood_2026.py
E = lambda z: np.sqrt(OM*(1+z)**3 + OL)
fNFW = lambda x: np.log(1+x) - x/(1+x)
def c_DM14(M, z):
    a = 0.520 + (0.905 - 0.520)*np.exp(-0.617*z**1.21); b = -0.101 + 0.026*z
    return 10**(a + b*np.log10(M*h/1e12))
def R_lcdm(z, M):
    c0, cz = c_DM14(M, 0.0), c_DM14(M, z)
    return E(z)**(4/3)*(cz**2/fNFW(cz))/(c0**2/fNFW(c0))

ledger = json.load(open(os.path.join(HERE, "highz_target_ledger_verified_2026_results.json")))
rows = {r["name"]: r for r in ledger["rows"]}
TARGETS = ["OLAS M0717-02064", "A68-C4", "SL2S 0217", "OLAS M1149-00683"]
check("A0 every target is present in the verified ledger", all(t in rows for t in TARGETS))

P("="*100); P("A. hypothesis ratios log10 a0(z)/a0(0) and the deep-MOND velocity factor R^{1/4} at fixed M_b"); P("="*100)
out = {"targets": {}}
for t in TARGETS:
    z = rows[t]["z"]
    hyp = {"H-CONST": 0.0, "H-LCDM(1e11)": np.log10(R_lcdm(z, 1e11)),
           "H-LCDM(1e12)": np.log10(R_lcdm(z, 1e12)), "H-HUBBLE": np.log10(E(z))}
    out["targets"][t] = {"z": z, "log_R": hyp}
    P(f"  {t:18s} z={z:5.3f}  " + "  ".join(f"{k} {v:+.3f} (V x{10**(v/4):.3f})" for k, v in hyp.items()))
zA, zB = rows["OLAS M0717-02064"]["z"], rows["A68-C4"]["z"]
check("A1 H-HUBBLE separates from H-CONST by >= 0.49 dex at both primary targets",
      np.log10(E(zA)) >= 0.49 and np.log10(E(zB)) >= 0.49, f"{np.log10(E(zA)):.3f}, {np.log10(E(zB)):.3f}")
check("A2 H-LCDM lies strictly between H-CONST and H-HUBBLE at both primary targets",
      all(0 < np.log10(R_lcdm(z, M)) < np.log10(E(z)) for z in (zA, zB) for M in (1e11, 1e12)))
check("A3 Halpha (0.65628 um) lands inside G235H/F170LP (1.66-3.05 um) for all four targets",
      all(1.66 < 0.65628*(1+rows[t]["z"]) < 3.05 for t in TARGETS),
      ", ".join(f"{0.65628*(1+rows[t]['z']):.3f}" for t in TARGETS))

P("="*100); P("C. FACE VALUE on published ground-based kinematics, M0717-02064 (NOT a measurement; V not inclination-corrected)"); P("="*100)
# 2026-09-25 CORRECTION (same day): the first version used the deep-limit V^4 = G M_b a0 here. At this galaxy's accelerations
# (y ~ 0.1-1.8) that OVERSTATES the baryonic mass a given hypothesis needs, because the full RAR kernel nu(y) = 1/(1-exp(-sqrt y))
# exceeds the deep-limit 1/sqrt(y). The face-value "lean against a constant a0" of the first version is WITHDRAWN (check C3).
from scipy.optimize import brentq
KPC = 3.086e19
nu_rar = lambda y: 1/(1 - np.exp(-np.sqrt(y)))
def Mb_needed(Vc_kms, R_kpc, a0):
    gobs = (Vc_kms*KMS)**2/(R_kpc*KPC); x = gobs/a0
    y = brentq(lambda y: y*nu_rar(y) - x, 1e-10, 1e6)
    return y*a0*(R_kpc*KPC)**2/G/MSUN, y
r = rows["OLAS M0717-02064"]; Ms = r["Mstar"]; V = r["V"]; s = r["sig"]; z = r["z"]
SFR = {"OLAS M0717-02064": 10**0.65}      # log SFR(Halpha) 0.65 (+0.13/-0.20), Hirtenstein+2019 Table 2, lens-corrected, re-read 2026-09-25
sfr = SFR["OLAS M0717-02064"]; TDEP = (0.2, 1.0)   # Gyr: bracket for z ~ 2 star-forming galaxies
P(f"  published: V = Dv/2 = {V} km/s, sigma_local = {s} km/s, v/sigma = {r['vsig_pub']}, M* = {Ms:.3g} Msun (lens-corrected), mu = {r['mu']}, SFR(Ha) = {sfr:.1f}")
P(f"  full RAR kernel; radius R where V_c is read is not published -> R = 1.5 / 2.5 / 3.5 kpc; deep-limit value in brackets (first version)")
P(f"  {'a0':>9} {'R':>4} {'geometry':>18} | CONST: y  Mgas/M*  t_dep[Gyr] (deep) | HUBBLE: y  Mgas/M*  t_dep[Gyr]")
face = []
for fk, a0 in A0.items():
    for R in (1.5, 2.5, 3.5):
        for gname, (inc, alpha) in (("edge-on, no drift", (90.0, 0.0)), ("i=60, alpha=2", (60.0, 2.0))):
            Vc = np.sqrt((V/np.sin(np.radians(inc)))**2 + alpha*s**2)
            row = {"footing": fk, "R_kpc": R, "geometry": gname, "Vc": Vc}
            for hk, lr in (("CONST", 0.0), ("HUBBLE", np.log10(E(z)))):
                Mb, y = Mb_needed(Vc, R, a0*10**lr)
                Mb_deep = (Vc*KMS)**4/(G*a0*10**lr)/MSUN
                row.update({f"{hk}_y": y, f"{hk}_Mgas_over_Mstar": max(Mb - Ms, 0)/Ms, f"{hk}_tdep_Gyr": max(Mb - Ms, 0)/sfr/1e9,
                            f"{hk}_deep_Mgas_over_Mstar": max(Mb_deep - Ms, 0)/Ms})
            face.append(row)
            P(f"  {a0:9.3g} {R:4.1f} {gname:>18} | {row['CONST_y']:6.2f} {row['CONST_Mgas_over_Mstar']:7.1f} {row['CONST_tdep_Gyr']:8.2f} ({row['CONST_deep_Mgas_over_Mstar']:5.1f})"
              f" | {row['HUBBLE_y']:6.2f} {row['HUBBLE_Mgas_over_Mstar']:7.1f} {row['HUBBLE_tdep_Gyr']:8.2f}")
out["M0717_face_value_full_kernel"] = face
cmin = min(f["CONST_Mgas_over_Mstar"] for f in face); cmax_t = max(f["CONST_tdep_Gyr"] for f in face)
P(f"  M_gas from SFR x t_dep in [{TDEP[0]}, {TDEP[1]}] Gyr: [{sfr*TDEP[0]*1e9/Ms:.1f}, {sfr*TDEP[1]*1e9/Ms:.1f}] x M*")
check("C1 every hypothesis needs a gas-dominated disc: CONST needs M_gas/M* > 5 in every row", cmin > 5, f"min {cmin:.1f}")
check("C2 HUBBLE needs less gas than CONST in every row (the ordering is geometry- and radius-independent)",
      all(f["HUBBLE_Mgas_over_Mstar"] < f["CONST_Mgas_over_Mstar"] for f in face))
check("C3 (correction, against interest) with the full kernel, CONST needs t_dep <= 1.0 Gyr in every row: the published data do NOT disfavour a constant a0",
      cmax_t <= TDEP[1], f"max {cmax_t:.2f} Gyr")
check("C4 (correction) the deep-limit formula of the first version overstated the gas CONST needs by >= 1.4x in every row",
      all(f["CONST_deep_Mgas_over_Mstar"] >= 1.4*f["CONST_Mgas_over_Mstar"] for f in face))
risk = [f for f in face if f["geometry"] == "i=60, alpha=2"]
check("C5 (risk) under CONST at typical geometry the galaxy sits at y > 0.3 at every radius tried: target 1 may FAIL the deep gate",
      all(f["CONST_y"] > 0.3 for f in risk), f"y in [{min(f['CONST_y'] for f in risk):.2f}, {max(f['CONST_y'] for f in risk):.2f}]")
P("  => face value: no lean either way. Inclination, pressure support, radius and gas mass decide it: that is the JWST measurement.")

P("="*100); P("D. per-object precision on log a0 (assumed budget, Monte Carlo) and what N objects decide"); P("="*100)
# 2026-09-25 CORRECTION (same day): the first version used the DEEP-LIMIT estimator log a0 = 4 log V - log M_b, i.e.
# amplifications A_bar = 1, A_obs = 2, and no intrinsic scatter. At the gate (y = g_bar/a0 = 0.2-0.3) the kernel inversion
# a0 = g_bar/y amplifies errors more: d ln a0 = (1 + 1/n) d ln g_bar - (1/n) d ln g_obs, n = d ln nu/d ln y, with the RAR
# kernel nu = 1/(1 - exp(-sqrt y)) (same table as the MNRAS v2 paper_numbers.py S4: y = 0.1 -> A_bar 1.35, A_obs 2.35;
# y = 0.3 -> 1.66, 2.66). The intrinsic RAR scatter (0.034 dex in g_obs) enters x A_obs, and for CONST vs LCDM the
# halo-to-halo concentration scatter moves each object's LCDM expectation by +/-0.132 dex (MNRAS v2, S4). All included now.
rng = np.random.default_rng(20260925)
def n_rar(y):
    r = np.sqrt(y); return -(r/2)*np.exp(-r)/(1 - np.exp(-r))
def sigma_loga0(y, sig_V_fit, sig_i_deg, i0_deg, sig_alpha, sig_logMs, sig_logMgas, fgas, s_over_V=0.6, intr=0.034, n=400000):
    nn = -0.5 if y is None else n_rar(y); A_bar, A_obs = 1 + 1/nn, -1/nn          # A_bar enters with sign (1+1/n) < 0
    i = np.radians(i0_deg + sig_i_deg*rng.standard_normal(n)); i = np.clip(i, np.radians(20), np.radians(89.9))
    Vrot = (1 + sig_V_fit*rng.standard_normal(n))/np.sin(i)*np.sin(np.radians(i0_deg))
    alpha = np.clip(2.7 + sig_alpha*rng.standard_normal(n), 0, None)
    Vc = np.sqrt(Vrot**2 + alpha*s_over_V**2); Vc0 = np.sqrt(1 + 2.7*s_over_V**2)
    Ms = (1 - fgas)*10**(sig_logMs*rng.standard_normal(n)); Mg = fgas*10**(sig_logMgas*rng.standard_normal(n))
    la = A_bar*np.log10(Ms + Mg) + A_obs*(2*np.log10(Vc/Vc0) + (0 if y is None else intr)*rng.standard_normal(n))
    return float(np.std(la)), abs(A_bar), A_obs
BASE_J = dict(sig_V_fit=0.05, sig_i_deg=8, i0_deg=60, sig_alpha=0.7, sig_logMs=0.15, sig_logMgas=0.30, fgas=0.85)
BASE_A = dict(BASE_J, sig_logMgas=0.12)
BASE_B = dict(sig_V_fit=0.04, sig_i_deg=4, i0_deg=60, sig_alpha=0.5, sig_logMs=0.12, sig_logMgas=0.12, fgas=0.85)
BUDGETS = {}
for ylab, y in (("deep limit (first version, UNDERSTATES)", None), ("y = 0.2 (design point)", 0.2), ("y = 0.3 (gate edge)", 0.3)):
    BUDGETS[f"JWST IFU only (KS gas 0.30 dex), {ylab}"] = (y, BASE_J)
    BUDGETS[f"JWST IFU + CO/dust gas 0.12 dex, {ylab}"] = (y, BASE_A)
    BUDGETS[f"JWST IFU + gas 0.12 dex + inclination 4 deg, {ylab}"] = (y, BASE_B)
T3 = ("OLAS M0717-02064", "A68-C4", "SL2S 0217")
dH = {t: np.log10(E(rows[t]["z"])) for t in T3}
dL = {t: np.log10(R_lcdm(rows[t]["z"], 1e11)) for t in T3}
HALO = 0.132
out["budgets"] = {}
for name, (y, b) in BUDGETS.items():
    sg, Ab, Ao = sigma_loga0(y, **b)
    z2H = np.sqrt(sum((dH[t]/sg)**2 for t in T3[:2])); z3H = np.sqrt(sum((dH[t]/sg)**2 for t in T3))
    sL = np.sqrt(sg**2 + HALO**2)
    z2L = np.sqrt(sum((dL[t]/sL)**2 for t in T3[:2])); z3L = np.sqrt(sum((dL[t]/sL)**2 for t in T3))
    N3L = int(np.ceil((3*sL/np.mean(list(dL.values())))**2))
    out["budgets"][name] = {"y": y, "A_bar": Ab, "A_obs": Ao, "sigma_log_a0": sg, "z_CONST_vs_HUBBLE_2obj": z2H, "z_CONST_vs_HUBBLE_3obj": z3H,
                            "z_CONST_vs_LCDM_2obj": z2L, "z_CONST_vs_LCDM_3obj": z3L, "N_for_3sigma_CONST_vs_LCDM": N3L}
    P(f"  {name}  [A_bar {Ab:.2f}, A_obs {Ao:.2f}]\n      sigma(log a0) per object = {sg:.3f} dex | CONST vs HUBBLE: 2 obj {z2H:.1f} sigma, 3 obj {z3H:.1f} sigma"
      f" | CONST vs LCDM (halo scatter incl.): 2 obj {z2L:.1f}, 3 obj {z3L:.1f} sigma | N for 3 sigma CONST vs LCDM: {N3L}")
B = out["budgets"]
J0, J2, J3 = (B[f"JWST IFU only (KS gas 0.30 dex), {l}"] for l in ("deep limit (first version, UNDERSTATES)", "y = 0.2 (design point)", "y = 0.3 (gate edge)"))
A2 = B["JWST IFU + CO/dust gas 0.12 dex, y = 0.2 (design point)"]
check("D1 (correction, against interest) the deep-limit estimator understated the JWST-only error: y = 0.2 sigma exceeds the deep-limit value by > 25%",
      J2["sigma_log_a0"] > 1.25*J0["sigma_log_a0"], f"{J0['sigma_log_a0']:.3f} -> {J2['sigma_log_a0']:.3f}")
check("D2 JWST only, 3 objects at y = 0.2: CONST vs HUBBLE stays BELOW 3 sigma (the first version's '~3 sigma' is withdrawn)",
      J2["z_CONST_vs_HUBBLE_3obj"] < 3, f"{J2['z_CONST_vs_HUBBLE_3obj']:.2f}")
check("D3 JWST only, 3 objects: CONST vs LCDM is below 1.5 sigma at y = 0.2 (no decision on the LCDM question)",
      J2["z_CONST_vs_LCDM_3obj"] < 1.5, f"{J2['z_CONST_vs_LCDM_3obj']:.2f}")
check("D4 a 0.12-dex gas mass brings 3 objects past 3 sigma on CONST vs HUBBLE at y = 0.2",
      A2["z_CONST_vs_HUBBLE_3obj"] > 3, f"{A2['z_CONST_vs_HUBBLE_3obj']:.2f}")
check("D5 the error grows toward the gate edge (y = 0.3 worse than y = 0.2)", J3["sigma_log_a0"] > J2["sigma_log_a0"],
      f"{J2['sigma_log_a0']:.3f} -> {J3['sigma_log_a0']:.3f}")

P("="*100)
P("VERDICT: one NIRSpec IFU velocity field per target delivers the velocity half (rotation gate, inclination, V_c).")
P("The gas mass decides the test. With the full-kernel amplification at the gate, JWST alone gives ~2 sigma on CONST vs HUBBLE")
P("(three objects) and no decision on CONST vs LCDM; a 0.12-dex gas mass lifts CONST vs HUBBLE past 3 sigma. The decisive")
P("CONST-vs-LCDM measurement needs gas masses AND more objects. The framework's own z~2 zero point still carries the open")
P("L189 retained-halo correction (not computed here).")
out["n_checks"] = NCHK[0]; out["fails"] = FAILS
json.dump(out, open(os.path.join(HERE, "a0z_deepmond_ifu_forecast_2026_results.json"), "w"), indent=1, default=float)
P(f"\n{NCHK[0] - len(FAILS)}/{NCHK[0]} checks passed" + ("" if not FAILS else f"; FAILED: {FAILS}"))
raise SystemExit(1 if FAILS else 0)

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
r = rows["OLAS M0717-02064"]; Ms = r["Mstar"]; V = r["V"]; s = r["sig"]; z = r["z"]
P(f"  published: V = Dv/2 = {V} km/s, sigma_local = {s} km/s, v/sigma = {r['vsig_pub']}, M* = {Ms:.3g} Msun (lens-corrected), mu = {r['mu']}")
face = []
for inc in (90.0, 60.0, 45.0):
    for alpha in (0.0, 2.0, 3.36):              # asymmetric drift: V_c^2 = V_rot^2 + alpha sigma^2 (3.36 = exp disc at R_e)
        Vc = np.sqrt((V/np.sin(np.radians(inc)))**2 + alpha*s**2)
        row = {"i": inc, "alpha": alpha, "Vc": Vc}
        for fk, a0 in A0.items():
            for hk, lr in (("CONST", 0.0), ("HUBBLE", np.log10(E(z)))):
                Mb = (Vc*KMS)**4/(G*a0*10**lr)/MSUN
                row[f"{hk}_{fk}_Mgas_over_Mstar"] = max(Mb - Ms, 0.0)/Ms
        face.append(row)
P(f"  {'i':>4} {'alpha':>5} {'V_c':>6} | M_gas/M* needed:  CONST can  CONST alt | HUBBLE can  HUBBLE alt")
for row in face:
    P(f"  {row['i']:4.0f} {row['alpha']:5.2f} {row['Vc']:6.1f} |                 {row['CONST_canonical_Mgas_over_Mstar']:9.1f} {row['CONST_alt_Mgas_over_Mstar']:10.1f} |"
      f" {row['HUBBLE_canonical_Mgas_over_Mstar']:10.1f} {row['HUBBLE_alt_Mgas_over_Mstar']:11.1f}")
lo = min(row["CONST_alt_Mgas_over_Mstar"] for row in face)
loH = min(row["HUBBLE_alt_Mgas_over_Mstar"] for row in face)
P(f"  minimum gas-to-stellar ratio required: H-CONST {lo:.1f} (alt footing, edge-on, no drift); H-HUBBLE {loH:.1f}")
P("  => under every hypothesis this galaxy must be strongly gas-dominated; the GAS MASS, not the velocity, decides it.")
check("C1 H-CONST needs M_gas/M* > 5 even at the most favourable geometry (the target is gas-dominated if a0 is constant)", lo > 5, f"{lo:.1f}")
check("C2 H-HUBBLE needs less gas than H-CONST at every geometry (the ordering is geometry-independent)",
      all(row["HUBBLE_alt_Mgas_over_Mstar"] < row["CONST_alt_Mgas_over_Mstar"] for row in face))
out["M0717_face_value"] = face

P("-"*100)
P("C'. is that gas plausible? Halpha SFR (Hirtenstein+2019 Table 2, lens-corrected, re-read 2026-09-25) x depletion time")
# log SFR(Halpha): M0717-02064 0.65 (+0.13/-0.20), M1149-00683 0.82 (+0.06/-0.07) Msun/yr
SFR = {"OLAS M0717-02064": 10**0.65, "OLAS M1149-00683": 10**0.82}
TDEP = (0.2, 1.0)   # Gyr: bracket for z ~ 2 star-forming galaxies; above-main-sequence systems sit at the short end
tdep_req = {}
for t, sfr in SFR.items():
    rr = rows[t]; Ms_t, V_t, s_t, z_t = rr["Mstar"], rr["V"], rr["sig"], rr["z"]
    Mg_lo, Mg_hi = sfr*TDEP[0]*1e9, sfr*TDEP[1]*1e9
    P(f"  {t}: SFR {sfr:.1f} Msun/yr, sSFR {sfr/Ms_t*1e9:.0f} /Gyr -> M_gas in [{Mg_lo:.2g}, {Mg_hi:.2g}] = [{Mg_lo/Ms_t:.1f}, {Mg_hi/Ms_t:.1f}] x M*")
    tdep_req[t] = {}
    for geom, (inc, alpha) in {"most favourable (i=90, no drift)": (90.0, 0.0), "typical (i=60, alpha=2)": (60.0, 2.0)}.items():
        Vc = np.sqrt((V_t/np.sin(np.radians(inc)))**2 + alpha*s_t**2)
        line = []
        for hk, lr in (("CONST", 0.0), ("LCDM(1e11)", np.log10(R_lcdm(z_t, 1e11))), ("HUBBLE", np.log10(E(z_t)))):
            Mb = (Vc*KMS)**4/(G*A0["alt"]*10**lr)/MSUN      # alt footing = the LESS demanding of the two
            td = max(Mb - Ms_t, 0.0)/sfr/1e9
            tdep_req[t][f"{hk}|{geom}"] = td
            line.append(f"{hk} {td:5.2f} Gyr")
        P(f"     required t_dep, {geom:34s}: " + "   ".join(line))
out["tdep_required_Gyr_alt_footing"] = tdep_req
tf = tdep_req["OLAS M0717-02064"]
check("C3 (both ways) M0717: H-CONST is NOT excluded at face value - at the most favourable geometry it needs t_dep inside the bracket",
      TDEP[0] <= tf["CONST|most favourable (i=90, no drift)"] <= TDEP[1], f"{tf['CONST|most favourable (i=90, no drift)']:.2f} Gyr")
check("C4 (both ways) M0717: at typical geometry H-CONST needs t_dep ABOVE the bracket (a face-value lean against constant a0, geometry-dependent)",
      tf["CONST|typical (i=60, alpha=2)"] > TDEP[1], f"{tf['CONST|typical (i=60, alpha=2)']:.2f} Gyr")
P("  => face value: the published kinematics do not decide it; inclination + pressure support + gas mass do. That is the JWST measurement.")

P("="*100); P("D. per-object precision on log a0 (assumed budget, Monte Carlo) and what N objects decide"); P("="*100)
rng = np.random.default_rng(20260925)
def sigma_loga0(sig_V_fit, sig_i_deg, i0_deg, sig_alpha, sig_logMs, sig_logMgas, fgas, s_over_V=0.6, n=400000):
    i = np.radians(i0_deg + sig_i_deg*rng.standard_normal(n)); i = np.clip(i, np.radians(20), np.radians(89.9))
    Vrot = (1 + sig_V_fit*rng.standard_normal(n))/np.sin(i)*np.sin(np.radians(i0_deg))
    alpha = np.clip(2.7 + sig_alpha*rng.standard_normal(n), 0, None)
    Vc = np.sqrt(Vrot**2 + alpha*s_over_V**2); Vc0 = np.sqrt(1 + 2.7*s_over_V**2)
    Ms = (1 - fgas)*10**(sig_logMs*rng.standard_normal(n)); Mg = fgas*10**(sig_logMgas*rng.standard_normal(n))
    la = 4*np.log10(Vc/Vc0) - np.log10(Ms + Mg)
    return float(np.std(la))
BUDGETS = {
    "JWST IFU only (gas from resolved Halpha + KS inversion, 0.30 dex)": dict(sig_V_fit=0.05, sig_i_deg=8, i0_deg=60, sig_alpha=0.7, sig_logMs=0.15, sig_logMgas=0.30, fgas=0.85),
    "JWST IFU + ALMA/NOEMA gas (0.12 dex)":                              dict(sig_V_fit=0.05, sig_i_deg=8, i0_deg=60, sig_alpha=0.7, sig_logMs=0.15, sig_logMgas=0.12, fgas=0.85),
    "JWST IFU + gas 0.12 dex + inclination to 4 deg":                    dict(sig_V_fit=0.04, sig_i_deg=4, i0_deg=60, sig_alpha=0.5, sig_logMs=0.12, sig_logMgas=0.12, fgas=0.85),
}
dH = {t: np.log10(E(rows[t]["z"])) for t in ("OLAS M0717-02064", "A68-C4")}
dL = {t: np.log10(R_lcdm(rows[t]["z"], 1e11)) for t in dH}
out["budgets"] = {}
for name, b in BUDGETS.items():
    sg = sigma_loga0(**b)
    # two primary targets; separation in units of the combined sigma
    zH = np.sqrt(sum((dH[t]/sg)**2 for t in dH)); zL = np.sqrt(sum((dL[t]/sg)**2 for t in dH))
    N_for_3sig_L = int(np.ceil((3*sg/np.mean(list(dL.values())))**2))
    out["budgets"][name] = {"sigma_log_a0": sg, "z_CONST_vs_HUBBLE_2obj": zH, "z_CONST_vs_LCDM_2obj": zL, "N_for_3sigma_CONST_vs_LCDM": N_for_3sig_L}
    P(f"  {name}\n      sigma(log a0) per object = {sg:.3f} dex | 2 objects: CONST vs HUBBLE {zH:.1f} sigma, CONST vs LCDM {zL:.1f} sigma | N for 3 sigma CONST vs LCDM: {N_for_3sig_L}")
bJ = out["budgets"][list(BUDGETS)[0]]; bA = out["budgets"][list(BUDGETS)[1]]
check("D1 JWST-only budget is gas-limited: sigma(log a0) > 0.25 dex", bJ["sigma_log_a0"] > 0.25, f"{bJ['sigma_log_a0']:.3f}")
check("D2 JWST-only, 2 objects, does NOT reach 3 sigma on CONST vs LCDM (honest ceiling)", bJ["z_CONST_vs_LCDM_2obj"] < 3, f"{bJ['z_CONST_vs_LCDM_2obj']:.2f}")
check("D3 adding a 0.12-dex gas mass tightens sigma(log a0) by > 30%", bA["sigma_log_a0"] < 0.7*bJ["sigma_log_a0"],
      f"{bJ['sigma_log_a0']:.3f} -> {bA['sigma_log_a0']:.3f}")

P("="*100)
P("VERDICT: one NIRSpec IFU velocity field per target delivers the velocity half (rotation gate, inclination, V_c).")
P("The gas mass decides the test. JWST alone gives a first ~2-sigma look at CONST vs HUBBLE and no decision on CONST vs LCDM;")
P("the decisive CONST-vs-LCDM measurement needs a molecular/dust gas mass and more objects. The framework's own z~2 zero point")
P("still carries the open L189 retained-halo correction (not computed here).")
out["n_checks"] = NCHK[0]; out["fails"] = FAILS
json.dump(out, open(os.path.join(HERE, "a0z_deepmond_ifu_forecast_2026_results.json"), "w"), indent=1, default=float)
P(f"\n{NCHK[0] - len(FAILS)}/{NCHK[0]} checks passed" + ("" if not FAILS else f"; FAILED: {FAILS}"))
raise SystemExit(1 if FAILS else 0)

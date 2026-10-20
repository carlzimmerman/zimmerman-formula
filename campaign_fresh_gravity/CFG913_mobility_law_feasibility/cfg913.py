#!/usr/bin/env python3
"""CFG913: is there ONE mobility law alpha(local variables) for the cold-energy drift that satisfies mergers (M), galaxies (G) and
dense dwarf clumps (D) at once?  Criteria: FROZEN_CRITERIA.md (957aaab55, committed alone before this script).

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg913.py
          -> cfg913.out, cfg913_results.json, cfg913_gtests_cache.json   (exit 0)
      CFG913_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg913.py
          -> cfg913_MUTATE.out, cfg913_results_MUTATE.json               (exit 1 when the tooth bites)

Read-only imports: CFG598 cfg598_lib (the P0 drift PDE and MW host; flux step copied verbatim with alpha made per cell),
CFG599 cfg599_lib (merger progenitor profiles).  Read-only data: CFG623 cached alpha = 0 runs; the result JSONs of CFG623, 639,
598, 542, 882, 889 (parts), 877.  Nothing downloaded; no other lane edited.
kappa = 1/2 FITTED; footings never pooled; cold energy is real gravitating mass; no particle species; not theory closed."""
import os, sys, json, math, time, io, contextlib
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG913_MUTATE", "") == "1"; SUF = "_MUTATE" if MUT else ""
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


sys.path.insert(0, os.path.join(LANES, "CFG598_settling_front_partial"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg598_lib as C                                   # noqa: E402  (read-only)
sys.path.insert(0, os.path.join(LANES, "CFG599_merger_stopwatch_v2"))
with contextlib.redirect_stdout(io.StringIO()):
    import cfg599_lib as L599                                # noqa: E402  (read-only)
    import cfg599_sim as S599                                # noqa: E402  (read-only: M_MAIN, M_SUB, epoch(); sets np.seterr to ignore)

T0 = time.time()
# ------------------------------------------------------------------------------------------------ constants and footings
FOOTS = ("can", "alt"); FOOTL = {"can": "canonical", "alt": "alt"}
A0SI = {"can": 9.3603e-11, "alt": 1.1312e-10}
KAPPA = 0.5                                                  # FITTED
G_SI, C_SI, MSUN, KPC = 6.674e-11, 2.99792458e8, 1.989e30, 3.0856775814913673e19
RHOL = {f: A0SI[f] ** 2 / (KAPPA ** 2 * G_SI * C_SI ** 2) / (MSUN / KPC ** 3) for f in FOOTS}   # rho_Lambda, Msun/kpc^3
GK, A0K = C.GK, C.A0K                                        # kpc (km/s)^2/Msun ; (km/s)^2/kpc
TU_MYR = C.TU_GYR * 1000.0                                   # kpc/(km/s) in Myr
KMS_KPCGYR = 1.0227121650537077                              # 1 km/s in kpc/Gyr (CFG597 KMS)
T_D = 12000.0                                                # Myr, retention time (CFG882/889)
LN2 = math.log(2.0)
ALPHA_HI = 1.0                                               # causal max at q -> 1 (CFG542 K9), most favourable to G
ALPHA_M_UNG, ALPHA_M_GAT = 0.03, 0.3                         # lenient merger bounds (exclusive): first node failing on value
ALPHA_G_LO, ALPHA_G_HI = 0.25, 1.0                           # G-allowed constant alpha in (0.25, 1.0]
EPS_FLUCT = 0.01                                             # CFG889's lower tested fluctuation level (skin delta)
PDEV = ("xr", "xg", "xJ", "xq")
VNAME = {"xr": "rho_m/rho_Lambda", "xg": "g/a0", "xJ": "y_J", "xq": "q", "xd": "delta", "xM": "Mach"}
NATURAL = {"xr": 1.0, "xg": 1.0, "xJ": 1.0, "xq": None}
RES = dict(lane="CFG913", criteria="957aaab55", mutate=MUT,
           settings=dict(kappa="1/2 FITTED", footings=A0SI, rho_Lambda_Msun_pc3={f: RHOL[f] * 1e-9 for f in FOOTS},
                         alpha_hi=ALPHA_HI, alpha_M_lenient=dict(ungated=ALPHA_M_UNG, gated=ALPHA_M_GAT),
                         alpha_G=[ALPHA_G_LO, ALPHA_G_HI], T_D_Myr=T_D))
rd = lambda p: json.load(open(os.path.join(LANES, p)))
CACHE_F = os.path.join(HERE, "cfg913_gtests_cache.json")
CACHE = json.load(open(CACHE_F)) if os.path.exists(CACHE_F) else {}

P("CFG913  one mobility law alpha(local variables) for mergers / galaxies / dwarf clumps?  criteria 957aaab55")
P("  kappa = 1/2 FITTED; footings 9.3603e-11 / 1.1312e-10 never pooled; cold energy real mass; not theory closed.")
P(f"  rho_Lambda = a0^2/(kappa^2 G c^2): can {RHOL['can'] * 1e-9:.4e}, alt {RHOL['alt'] * 1e-9:.4e} Msun/pc^3")
P()

# ================================================================================================= 1. K-tests (source bounds)
K = {}
R623 = rd("CFG623_merger_stopwatch_v5/cfg623_results.json")["cells"]
k1 = (all(R623[f"0_{f}"]["status"] == "ALLOWED" for f in FOOTS)
      and all(R623[f"{a}_{f}"]["status"] == "EXCLUDED" for a in ("0.1", "0.3", "inf") for f in FOOTS)
      and abs(R623["0.03_can"]["Z_B"] - 3.12) <= 0.01 and abs(R623["0.03_alt"]["Z_B"] - 2.65) <= 0.01)
K["K-M1"] = dict(pass_=bool(k1), ZB_0={f: R623[f"0_{f}"]["Z_B"] for f in FOOTS}, ZB_003={f: R623[f"0.03_{f}"]["Z_B"] for f in FOOTS},
                 status={c: R623[c]["status"] for c in R623})
P(f"K-M1 CFG623: alpha 0 ALLOWED both (Z_B {R623['0_can']['Z_B']:+.2f}/{R623['0_alt']['Z_B']:+.2f}); 0.1, 0.3, inf EXCLUDED; "
  f"alpha 0.03 Z_B {R623['0.03_can']['Z_B']:+.2f}/{R623['0.03_alt']['Z_B']:+.2f} (> 2 on value) -> ungated value bracket [0, 0.03) "
  f"-> {'PASS' if k1 else 'FAIL'}")
R639 = rd("CFG639_deficit_gated_mobility/cfg639_merger_results.json")
c639 = R639["cells"]
k2 = (R639["allowed_set"] == {"can": ["0"], "alt": ["0", "0.03"]}
      and all(c639[f"0.1_{f}"]["Z_B"] < 2 and c639[f"0.1_{f}"]["Z_H"] < 2 for f in FOOTS)
      and c639["0.3_can"]["Z_B"] >= 2 and abs(R639["B_M1"]["gated_off_frac_window"] - 0.714) <= 1e-3)
K["K-M2"] = dict(pass_=bool(k2), allowed=R639["allowed_set"], ZB_ZH_01={f: [c639[f"0.1_{f}"]["Z_B"], c639[f"0.1_{f}"]["Z_H"]] for f in FOOTS},
                 ZB_03={f: c639[f"0.3_{f}"]["Z_B"] for f in FOOTS}, gated_off=R639["B_M1"]["gated_off_frac_window"])
P(f"K-M2 CFG639 (gate): allowed {R639['allowed_set']}; alpha 0.1 Z_B/Z_H can {c639['0.1_can']['Z_B']:+.2f}/{c639['0.1_can']['Z_H']:+.2f}, "
  f"alt {c639['0.1_alt']['Z_B']:+.2f}/{c639['0.1_alt']['Z_H']:+.2f}; alpha 0.3 Z_B {c639['0.3_can']['Z_B']:+.2f}/{c639['0.3_alt']['Z_B']:+.2f}; "
  f"gated off {R639['B_M1']['gated_off_frac_window']:.3f} -> gated value bracket [0.1, 0.3) -> {'PASS' if k2 else 'FAIL'}")
R598 = rd("CFG598_settling_front_partial/cfg598_results.json")["MW"]
k3 = (abs(R598["P0|can|0.25"]["min_q"] - 0.9842) <= 1e-4 and abs(R598["P0|alt|0.25"]["min_q"] - 0.9849) <= 1e-4
      and abs(R598["P0|can|0.5"]["min_q"] - 0.9928) <= 1e-4 and abs(R598["P0|alt|0.5"]["min_q"] - 0.9930) <= 1e-4
      and not R598["P0|can|0.25"]["i_holds"] and R598["P0|can|0.5"]["i_holds"] and R598["P0|alt|0.5"]["i_holds"])
K["K-G1"] = dict(pass_=bool(k3), min_q={k: R598[k]["min_q"] for k in R598 if k.startswith("P0")})
P(f"K-G1 CFG598 MW P0 min q: alpha 0.25 {R598['P0|can|0.25']['min_q']:.4f}/{R598['P0|alt|0.25']['min_q']:.4f} (fails 0.99), "
  f"0.5 {R598['P0|can|0.5']['min_q']:.4f}/{R598['P0|alt|0.5']['min_q']:.4f} (passes) -> alpha_G in (0.25, 0.5] -> {'PASS' if k3 else 'FAIL'}")
R542 = rd("CFG542_dissipative_action/cfg542_results.json")["K9_dispersion"]
am1, amc = R542["alpha_max_beta1_q1"]["Pb"], R542["alpha_max_beta1_q_cosmic"]["Pb"]
k4 = abs(am1 - 1.0) <= 1e-3 and abs(amc - 1.1864) <= 1e-3
K["K-C"] = dict(pass_=bool(k4), alpha_max_q1=am1, alpha_max_qcosmic=amc)
P(f"K-C  CFG542 causality alpha beta q < 1: alpha_max {am1:.4f} (q = 1), {amc:.4f} (q = 1 - f_b) -> {'PASS' if k4 else 'FAIL'}")
R882 = rd("CFG882_clump_retention_equations/cfg882_results.json")["V1"]
HOSTS882 = ("H1", "H2", "H3")
ac = [R882[f][h]["alpha_c"] for f in R882 for h in HOSTS882]; a50 = [R882[f][h]["alpha50"] for f in R882 for h in HOSTS882]
k5 = abs(max(ac) - 1.37e-3) <= 0.01e-3 and abs(min(a50) - 6.2e-4) <= 0.1e-4 and abs(max(a50) - 1.02e-3) <= 0.01e-3
K["K-D1"] = dict(pass_=bool(k5), alpha_c_max=max(ac), alpha50_range=[min(a50), max(a50)],
                 alpha50_H2={f: R882[f]["H2"]["alpha50"] for f in R882})
P(f"K-D1 CFG882 ungated: alpha_c max {max(ac):.3e}; alpha_50 {min(a50):.2e} .. {max(a50):.2e} -> {'PASS' if k5 else 'FAIL'}")
at50 = {}
for part in ("G1a", "G1b", "G2a", "G2b"):
    pj = rd(f"CFG889_gated_kinetic_stability/parts/part_{part}.json")
    for key, v in pj.items():
        if key.startswith("G|") and key.endswith("|clump"):
            a = float(key.split("|")[3][1:]); at50[key] = a * v["t50"]
k6 = len(at50) == 8 and abs(min(at50.values()) - 105.5) <= 1.0 and abs(max(at50.values()) - 147.5) <= 1.0
ALPHA_D_GAT = min(at50.values()) / T_D
K["K-D2"] = dict(pass_=bool(k6), alpha_t50=at50, alpha_D_gated=[min(at50.values()) / T_D, max(at50.values()) / T_D])
P(f"K-D2 CFG889 gated kinetic: alpha*t50 = {min(at50.values()):.1f} .. {max(at50.values()):.1f} Myr over {len(at50)} cells -> "
  f"alpha_D,gated {min(at50.values()) / T_D:.2e} .. {max(at50.values()) / T_D:.2e} (12 Gyr) -> {'PASS' if k6 else 'FAIL'}")
P()

# ================================================================================================= 2. M region (merger states)
R877 = rd("CFG877_finite_cold_clump/cfg877_results.json")
M_MAIN, M_SUB = S599.M_MAIN, S599.M_SUB                       # 1.5e15, 1.5e14
S_CORE = [0.0, 10.0, 25.0, 50.0, 75.0, 100.0, 150.0, 200.0]; S_WIDE = S_CORE + [250.0, 300.0]
NANG = 8


def merger_states(foot):
    run = rd(f"CFG623_merger_stopwatch_v5/runs/a0_{foot}_v2666.7_eta1.132.json")
    with contextlib.redirect_stdout(io.StringIO()):
        pM = L599.Progenitor599(M_MAIN, foot, cloud=False); pS = L599.Progenitor599(M_SUB, foot, cloud=True)
    km3 = dict(Mph_rel=[abs(pM.Mph_tot / run["Mph_tot"][0] - 1), abs(pS.Mph_tot / run["Mph_tot"][1] - 1)],
               Mb_rel=[abs(pM.Mb / run["Mb"][0] - 1), abs(pS.Mb / run["Mb"][1] - 1)])
    s2M, s2S = pM.jeans_sigma2(pM.rho_ph), pS.jeans_sigma2(pS.rho_ph)
    G, a0 = L599.G, L599.A0[foot]
    D = run["diag"]; tp = run["t_peri"]; t = np.array([d["t"] for d in D])
    pos = lambda i, who, key: np.array(D[i][who][key][:2], float)
    def vel(i, who, key):
        return (pos(i + 2, who, key) - pos(i - 2, who, key)) / (t[i + 2] - t[i - 2])
    win = [i for i in range(2, len(D) - 2) if 0.1 <= t[i] - tp <= 0.6 and np.linalg.norm(pos(i, "sub", "gas") - pos(i, "sub", "gal")) >= 200.0]
    ep = S599.epoch(D, tp)                                   # CFG599/621/623 720-kpc observation epoch (read-only)
    obs_ep = [ep["i_obs"] - 1, ep["i_obs"]]
    rows = []
    for i in sorted(set(win) | set(obs_ep)):
        cen = dict(cS=pos(i, "sub", "cold"), sS=pos(i, "sub", "gal"), gS=pos(i, "sub", "gas"), kS=pos(i, "sub", "cloud_com"),
                   cM=pos(i, "main", "cold"), sM=pos(i, "main", "gal"), gM=pos(i, "main", "gas"))
        vv = dict(cS=vel(i, "sub", "cold"), sS=np.array(D[i]["sub"]["vgal"][:2]), gS=vel(i, "sub", "gas"), kS=vel(i, "sub", "cloud_com"),
                  cM=vel(i, "main", "cold"), sM=np.array(D[i]["main"]["vgal"][:2]), gM=vel(i, "main", "gas"))
        comp = dict(cS=(pS, pS.rho_ph, pS.Mph), sS=(pS, pS.rho_s, pS.Ms), gS=(pS, pS.rho_g, pS.Mg), kS=(pS, pS.rho_cc, pS.Mcc_r),
                    cM=(pM, pM.rho_ph, pM.Mph), sM=(pM, pM.rho_s, pM.Ms), gM=(pM, pM.rho_g, pM.Mg))
        for s in S_WIDE:
            for j in (range(NANG) if s > 0 else [0]):
                th = 2 * math.pi * j / NANG
                Pt = cen["cS"] + s * np.array([math.cos(th), math.sin(th)])
                rho, gvec = {}, np.zeros(2)
                for k, (pp, rr, MM) in comp.items():
                    dv = Pt - cen[k]; dd = max(float(np.linalg.norm(dv)), pp.r[1])   # correction 1: never interpolate onto the r = 0 node
                    rho[k] = float(np.interp(dd, pp.r, rr, right=0.0))
                    gvec += -G * float(np.interp(dd, pp.r, MM)) / dd ** 2 * dv / dd
                rc_ = rho["cS"] + rho["cM"]; rb = rho["sS"] + rho["gS"] + rho["kS"] + rho["sM"] + rho["gM"]; rm = rc_ + rb
                uc = (rho["cS"] * vv["cS"] + rho["cM"] * vv["cM"]) / rc_
                ubB = sum(rho[k] * vv[k] for k in ("sS", "gS", "kS", "sM", "gM")) / rb
                rg = rho["gS"] + rho["kS"] + rho["gM"]
                ubA = sum(rho[k] * vv[k] for k in ("gS", "kS", "gM")) / rg
                dS = max(float(np.linalg.norm(Pt - cen["cS"])), pS.r[1]); dM = max(float(np.linalg.norm(Pt - cen["cM"])), pM.r[1])
                sig2 = (rho["cS"] * float(np.interp(dS, pS.r, s2S)) + rho["cM"] * float(np.interp(dM, pM.r, s2M))) / rc_
                sig = math.sqrt(sig2); tau = 1.0 / math.sqrt(4 * math.pi * G * rm)
                rows.append(dict(i=i, win=i in win, obs=i in obs_ep, t_after=float(t[i] - tp), s=s, xr=rm / RHOL[foot], xg=float(np.linalg.norm(gvec)) / a0,
                                 xJ=sig / (tau * a0), xq=rc_ / rm, xMB=float(np.linalg.norm(uc - ubB)) / sig,
                                 xMA=float(np.linalg.norm(uc - ubA)) / sig, rho_pc3=rm * 1e-9, sig_kms=sig / KMS_KPCGYR,
                                 dvB_kms=float(np.linalg.norm(uc - ubB)) / KMS_KPCGYR, dvA_kms=float(np.linalg.norm(uc - ubA)) / KMS_KPCGYR,
                                 tau_Myr=tau * 1000.0, fgas=rg / rb, rhoc=rc_, j=j,
                                 comp={k: rho[k] for k in rho}))
    obs = dict(speed=float(ep["v_obs_kms"]), dSG=float(ep["dSG_obs"]), t_obs_after_peri=float(ep["t_obs"] - tp))
    return rows, km3, dict(n_epochs=len(win), t_range=[float(t[win[0]] - tp), float(t[win[-1]] - tp)], obs_epochs=obs_ep, obs=obs)


def summarize_rows(rows, smax, keys=("xr", "xg", "xJ", "xq", "xMB", "xMA", "rho_pc3", "sig_kms", "dvB_kms", "dvA_kms", "tau_Myr", "fgas")):
    sel = [r for r in rows if r["s"] <= smax]
    if not sel:
        return None
    return {k: [min(r[k] for r in sel), max(r[k] for r in sel)] for k in keys}


MREG, MINFO, MROWS = {}, {}, {}
for f in FOOTS:
    rows, km3, info = merger_states(f)
    MROWS[f] = rows
    rw = [r for r in rows if r["win"]]
    MREG[f] = dict(core=summarize_rows(rw, 200.0), wide=summarize_rows(rw, 300.0),
                   obs=summarize_rows([r for r in rows if r["obs"]], 200.0))
    # Mach by epoch (min over core points): where does it dip?
    ep = sorted(set(r["t_after"] for r in rw))
    MREG[f]["MachB_min_by_epoch"] = [[e, min(r["xMB"] for r in rw if r["t_after"] == e and r["s"] <= 200.0),
                                      min(r["xMA"] for r in rw if r["t_after"] == e and r["s"] <= 200.0)] for e in ep]
    core = [r for r in rw if r["s"] <= 200.0]; wc = np.array([r["rhoc"] for r in core])
    MREG[f]["frac_Mach_le1"] = dict(B_points=float(np.mean([r["xMB"] <= 1 for r in core])), A_points=float(np.mean([r["xMA"] <= 1 for r in core])),
                                    B_rhoc_weighted=float(np.sum(wc * np.array([r["xMB"] <= 1 for r in core])) / wc.sum()),
                                    A_rhoc_weighted=float(np.sum(wc * np.array([r["xMA"] <= 1 for r in core])) / wc.sum()),
                                    B_by_s={str(sv): float(np.mean([r["xMB"] <= 1 for r in core if r["s"] == sv])) for sv in S_CORE},
                                    A_by_s={str(sv): float(np.mean([r["xMA"] <= 1 for r in core if r["s"] == sv])) for sv in S_CORE})
    MINFO[f] = dict(km3=km3, **info)
okm3 = all(max(MINFO[f]["km3"]["Mph_rel"] + MINFO[f]["km3"]["Mb_rel"]) <= 1e-6 for f in FOOTS) and \
    all(abs(MINFO[f]["obs"]["speed"] - R623[f"0_{f}"]["speed_kms"]) <= 0.1 and abs(MINFO[f]["obs"]["dSG"] - R623[f"0_{f}"]["dSG"]) <= 0.1 for f in FOOTS)
K["K-M3"] = dict(pass_=bool(okm3), info={f: MINFO[f] for f in FOOTS})
P(f"K-M3 merger reconstruction: Progenitor599 Mph_tot/Mb vs cached run rel. diff <= "
  f"{max(max(MINFO[f]['km3']['Mph_rel'] + MINFO[f]['km3']['Mb_rel']) for f in FOOTS):.1e}; observed epoch d_SG "
  f"{MINFO['can']['obs']['dSG']:.2f} kpc (CFG623 {R623['0_can']['dSG']:.2f}), speed {MINFO['can']['obs']['speed']:.1f} km/s "
  f"(CFG623 {R623['0_can']['speed_kms']:.0f}) -> {'PASS' if okm3 else 'FAIL'}")
P()
P("M region: sub cold energy within 200 kpc (core) / 300 kpc (wide) of its peak, window t - t_peri in [0.1, 0.6] Gyr, d_SG >= 200 kpc")
for f in FOOTS:
    m = MREG[f]["core"]; w = MREG[f]["wide"]
    P(f"  [{f}] {MINFO[f]['n_epochs']} epochs ({MINFO[f]['t_range'][0]:.2f}-{MINFO[f]['t_range'][1]:.2f} Gyr after pericentre)")
    P(f"     rho_m {m['rho_pc3'][0]:.2e} .. {m['rho_pc3'][1]:.2e} Msun/pc^3 (x_rho {m['xr'][0]:.3g} .. {m['xr'][1]:.3g}); "
      f"tau {m['tau_Myr'][0]:.0f} .. {m['tau_Myr'][1]:.0f} Myr; sigma_J {m['sig_kms'][0]:.0f} .. {m['sig_kms'][1]:.0f} km/s")
    P(f"     g/a0 {m['xg'][0]:.3f} .. {m['xg'][1]:.3f}; y_J {m['xJ'][0]:.3f} .. {m['xJ'][1]:.3f}; q {m['xq'][0]:.3f} .. {m['xq'][1]:.3f}")
    P(f"     |u_c - u_b| frame B (all baryons) {m['dvB_kms'][0]:.0f} .. {m['dvB_kms'][1]:.0f} km/s -> Mach_B {m['xMB'][0]:.3f} .. {m['xMB'][1]:.3f}; "
      f"frame A (gas) {m['dvA_kms'][0]:.0f} .. {m['dvA_kms'][1]:.0f} km/s -> Mach_A {m['xMA'][0]:.3f} .. {m['xMA'][1]:.3f}; gas share of local baryons "
      f"{m['fgas'][0]:.2f} .. {m['fgas'][1]:.2f}")
    o_ = MREG[f]["obs"]
    P(f"     wide: rho_m min {w['rho_pc3'][0]:.2e}, Mach_B min {w['xMB'][0]:.3f}, Mach_A min {w['xMA'][0]:.3f}; Bullet observation epochs (report, "
      f"core): Mach_B {o_['xMB'][0]:.3f} .. {o_['xMB'][1]:.3f}, Mach_A {o_['xMA'][0]:.3f} .. {o_['xMA'][1]:.3f}, rho_m {o_['rho_pc3'][0]:.2e} .. "
      f"{o_['rho_pc3'][1]:.2e}")
    fr = MREG[f]["frac_Mach_le1"]
    P(f"     share of M-core states with Mach <= 1 (report): frame B {fr['B_points']:.2f} of points ({fr['B_rhoc_weighted']:.2f} rho_c-weighted), "
      f"frame A {fr['A_points']:.2f} ({fr['A_rhoc_weighted']:.2f}); by radius s (B): "
      + ", ".join(f"{float(k):g} kpc {v:.2f}" for k, v in fr["B_by_s"].items()) + "; (A): "
      + ", ".join(f"{float(k):g} kpc {v:.2f}" for k, v in fr["A_by_s"].items()))
    bad = [e for e in MREG[f]["MachB_min_by_epoch"] if e[1] <= 1.0]
    P(f"     epochs with min Mach_B <= 1: {len(bad)} of {len(MREG[f]['MachB_min_by_epoch'])}"
      + (f" (t - t_peri {bad[0][0]:.2f} .. {bad[-1][0]:.2f} Gyr)" if bad else ""))
P("  delta (logic, CFG639 B-M1): gate-open merger cold states (delta in (0, 1]) exist: "
  f"{1 - R639['B_M1']['gated_off_frac_window']:.3f} of settle steps in the pericentre window")
RES["M_region"] = MREG; RES["M_info"] = MINFO
P()

# ================================================================================================= 3. D region (clump states)
nu_e = lambda y: 1.0 / (-np.expm1(-np.sqrt(np.maximum(y, 1e-300))))


def clump_states(foot, dscale=1.0):
    r = np.geomspace(1e-3, 20.0, 6000)
    Mb0, a = 3e5, 0.2                                        # H2 (CFG882 HOSTS)
    Mb = Mb0 * r ** 3 / (r ** 2 + a ** 2) ** 1.5
    rhob = 3 * Mb0 * a ** 2 / (4 * math.pi * (r ** 2 + a ** 2) ** 2.5)
    a0 = A0K[foot]
    Mph = (nu_e(GK * Mb / (r ** 2 * a0)) - 1.0) * Mb
    rhoph = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
    cl = R877[FOOTL[foot]]; Vx, Mcl, rcl = cl["Vx"], cl["Mcl_Msun"], 0.104
    Mxu = Vx ** 2 * r ** 3 / (GK * (r ** 2 + rcl ** 2)); Mx = np.minimum(Mxu, Mcl)
    rhox = np.where(Mxu < Mcl, Vx ** 2 / GK * (r ** 2 + 3 * rcl ** 2) / (4 * math.pi * (r ** 2 + rcl ** 2) ** 2), 0.0)
    rcap = brentq(lambda x: Vx ** 2 * x ** 3 / (GK * (x ** 2 + rcl ** 2)) - Mcl, 1e-3, 5.0)
    r50 = brentq(lambda x: Vx ** 2 * x ** 3 / (GK * (x ** 2 + rcl ** 2)) - 0.5 * Mcl, 1e-3, 5.0)
    rhoc = rhoph + rhox; rhom = rhob + rhoc
    g = GK * (Mb + Mph + Mx) / r ** 2
    f_ = rhoc * g; I = np.zeros_like(r)
    I[:-1] = np.cumsum((0.5 * (f_[1:] + f_[:-1]) * np.diff(r))[::-1])[::-1]
    sig2 = I / rhoc
    rhoc_s, rhom_s = rhoc * dscale, rhom * dscale            # MUTATE C/D: densities scaled; tau and alpha_D,loc follow
    tau = 1.0 / np.sqrt(4 * math.pi * GK * rhom_s)
    st = dict(r=r, xr=rhom_s / RHOL[foot], xg=g / a0, xJ=np.sqrt(sig2) / (tau * a0), xq=rhoc_s / rhom_s, xd=1.0 - rhoc / rhoph,
              rho_pc3=rhom_s * 1e-9, tau_Myr=tau * TU_MYR, sig_kms=np.sqrt(sig2))
    st["aDloc"] = LN2 * st["tau_Myr"] / (st["xq"] * T_D)
    return st, dict(rcap_pc=rcap * 1e3, r50_pc=r50 * 1e3, Mcl=Mcl)


def dsumm(st, rmax):
    s = st["r"] <= rmax
    out = {k: [float(st[k][s].min()), float(st[k][s].max())] for k in ("xr", "xg", "xJ", "xq", "xd", "rho_pc3", "tau_Myr", "sig_kms", "aDloc")}
    return out


def d_region(dscale=1.0):
    reg = {}
    for f in FOOTS:
        st, info = clump_states(f, dscale)
        reg[f] = dict(cons=dsumm(st, 0.45), len=dsumm(st, info["r50_pc"] * 1e-3), info=info)
        reg[f]["_st"] = st
    return reg


DREG = d_region()
kd4 = abs(DREG["can"]["info"]["rcap_pc"] - 237) <= 2 and abs(DREG["alt"]["info"]["rcap_pc"] - 205) <= 2
K["K-D4"] = dict(pass_=bool(kd4), rcap_pc={f: DREG[f]["info"]["rcap_pc"] for f in FOOTS})
P(f"K-D4 clump profile reaches M_cl at {DREG['can']['info']['rcap_pc']:.1f} / {DREG['alt']['info']['rcap_pc']:.1f} pc (CFG877 README:48-49: "
  f"237 / 205) -> {'PASS' if kd4 else 'FAIL'}")
kd3 = {}
for f in FOOTS:
    st = DREG[f]["_st"]; i = int(np.searchsorted(st["r"], DREG[f]["info"]["rcap_pc"] * 1e-3)) - 1
    kd3[f] = dict(aDloc_rcap=float(st["aDloc"][i]), alpha50_H2=R882[FOOTL[f]]["H2"]["alpha50"],
                  ratio=float(st["aDloc"][i] / R882[FOOTL[f]]["H2"]["alpha50"]))
okd3 = all(1 / 1.5 <= kd3[f]["ratio"] <= 1.5 for f in FOOTS)
K["K-D3"] = dict(pass_=bool(okd3), **kd3)
P(f"K-D3 alpha_D,loc at the cap radius (uniform alpha) {kd3['can']['aDloc_rcap']:.2e} / {kd3['alt']['aDloc_rcap']:.2e} vs CFG882 H2 alpha_50 "
  f"{kd3['can']['alpha50_H2']:.2e} / {kd3['alt']['alpha50_H2']:.2e} (ratio {kd3['can']['ratio']:.2f} / {kd3['alt']['ratio']:.2f}; within x1.5) "
  f"-> {'PASS' if okd3 else 'FAIL'}")
P()
P("D region: CFG877 capped clump on H2 + H2's law-settled halo; conservative r <= 450 pc, lenient r <= r_50")
for f in FOOTS:
    for nm in ("cons", "len"):
        d = DREG[f][nm]
        P(f"  [{f} {nm:4s}] rho_m {d['rho_pc3'][0]:.2e} .. {d['rho_pc3'][1]:.2e} Msun/pc^3 (x_rho {d['xr'][0]:.3g} .. {d['xr'][1]:.3g}); "
          f"tau {d['tau_Myr'][0]:.1f} .. {d['tau_Myr'][1]:.1f} Myr; g/a0 {d['xg'][0]:.3f} .. {d['xg'][1]:.3f}; y_J {d['xJ'][0]:.3f} .. {d['xJ'][1]:.3f}; "
          f"q {d['xq'][0]:.3f} .. {d['xq'][1]:.3f}; delta {d['xd'][0]:.2f} .. {d['xd'][1]:.2f}; sigma_J {d['sig_kms'][0]:.1f} .. {d['sig_kms'][1]:.1f} km/s; "
          f"alpha_D,loc {d['aDloc'][0]:.2e} .. {d['aDloc'][1]:.2e}")
    P(f"  [{f}] cap {DREG[f]['info']['rcap_pc']:.0f} pc, r_50 {DREG[f]['info']['r50_pc']:.0f} pc; Mach = 0 (equilibrium); "
      f"skin delta = 0 +- fluctuations (CFG889 tested eps 0.01-0.1)")
RES["D_region"] = {f: {k: v for k, v in DREG[f].items() if k != "_st"} for f in FOOTS}
P()

# ================================================================================================= 4. G: the P0 PDE with per-cell alpha
HB = dict(xr=np.linspace(-4, 10, 141), xg=np.linspace(-5, 3, 161), xJ=np.linspace(-5, 3, 161), xq=np.linspace(0, 1, 101),
          xd=np.linspace(-5, 1, 121))


def law_factor(law, st):
    F = np.ones_like(st["xr"])
    if law["kind"] in ("step", "smooth"):
        x = st[law["var"]]; xs = law["xstar"]
        if law["kind"] == "step":
            F = (x < xs).astype(float) if law["orient"] == "dec" else (x > xs).astype(float)
        else:
            z = np.clip(x / xs, 0.0, None)
            fm = {"rat1": lambda z: 1 / (1 + z), "rat2": lambda z: 1 / (1 + z * z), "exp": lambda z: np.exp(-z)}[law["form"]](z)
            F = fm if law["orient"] == "dec" else 1.0 - fm
    if law.get("gate"):
        F = F * (st["xd"] > 0)
    return F


class LawRun(C.Run):
    def __init__(self, host, foot, law, N=300, record=False):
        super().__init__(host, foot, "P0", N=N)
        self.law, self.foot, self.record = law, foot, record
        self.dr = np.diff(self.rf)
        self.hist = {k: np.zeros(len(HB[k]) - 1) for k in HB} if record else None
        self.trivial = law["kind"] == "const" and not law.get("gate")

    def state(self, m):
        rho_c = m / self.V; rho_m = rho_c + self.rhob
        with np.errstate(divide="ignore", invalid="ignore"):
            xq = np.where(rho_m > 0, rho_c / rho_m, 0.0)
            rph = self.mph / self.V
            xd = np.where(rph > 0, 1.0 - rho_c / np.where(rph > 0, rph, 1.0), np.where(rho_c > 0, -1e30, 0.0))
            Mbc = 0.5 * (self.Mbf[:-1] + self.Mbf[1:]); Mcc = np.cumsum(m) - 0.5 * m
            g = GK * (Mbc + Mcc) / self.rc ** 2
            itg = rho_c * g * self.dr
            S = np.cumsum(itg[::-1])[::-1] - 0.5 * itg
            sig2 = np.where(rho_c > 0, S / np.where(rho_c > 0, rho_c, 1.0), 0.0)
            xJ = np.sqrt(np.maximum(sig2, 0.0)) * np.sqrt(4 * math.pi * GK * rho_m) / self.a0
        return dict(xr=rho_m / RHOL[self.foot], xg=g / self.a0, xJ=xJ, xq=xq, xd=xd)

    def flux_step(self, m, alpha, rta, dtmax):
        """cfg598_lib.Run.flux_step copied verbatim, with alpha -> alpha * F(state) per cell (donor cell for the face flux)."""
        N, V, A, rf = self.N, self.V, self.A, self.rf
        cellB = rf[:-1] < rta
        rho = m / V
        d = np.where(cellB, np.maximum(self.mph / V - rho, 0.0), 0.0)
        Md = np.concatenate([[0.0], np.cumsum(d * V)])
        dpsi = GK * Md / rf ** 2
        live = m > self.thr
        tau = np.where(live, 1.0 / np.sqrt(4 * math.pi * GK * np.maximum(rho + self.rhob, 1e-300)), 0.0)
        st = self.state(m) if (self.record or not self.trivial) else None
        aarr = alpha * (np.ones(N) if self.trivial else law_factor(self.law, st))
        don = slice(1, N)
        ok = live[don] & cellB[don]
        v = aarr[don] * tau[don] * dpsi[1:N]
        flux = rho[don] * v * A[1:N]
        with np.errstate(divide="ignore", over="ignore", invalid="ignore"):
            dtc = np.where(ok & (v > 0), 0.4 * V[don] / np.maximum(A[1:N] * v, 1e-300), np.inf).min()
        sel = live & cellB
        gam = float((4 * math.pi * GK * rho * tau * aarr)[sel].max()) if sel.any() else 0.0
        dt = min(dtc, 0.2 / gam if gam > 0 else np.inf, dtmax)
        tr = np.where(ok, np.minimum(flux * dt, m[don]), 0.0)
        tr = np.where(ok & (m[don] - tr < self.thr[don]) & (tr > 0), m[don], tr)
        if self.record:
            w = tr > 0
            if w.any():
                for k in HB:
                    x = st[k][1:N][w]
                    x = np.log10(np.maximum(x, 1e-300)) if k in ("xr", "xg", "xJ") else (np.clip(x, -5, 1) if k == "xd" else x)
                    self.hist[k] += np.histogram(np.clip(x, HB[k][0], HB[k][-1] - 1e-12), HB[k], weights=tr[w])[0]
        m = m.copy(); m[1:] -= tr; m[:-1] += tr
        sig = ok & (m[don] >= 1e-3 * self.mph[don])
        vm = float(np.max(np.where(sig, v, 0.0))) if sig.any() else 0.0
        return m, dt, vm


with contextlib.redirect_stdout(io.StringIO()):
    HMW = C.Host(None, mw=True)


def lawkey(law, foot):
    return json.dumps(dict(law, foot=foot), sort_keys=True)


def gtest(law, foot, record=False):
    key = lawkey(law, foot)
    if key in CACHE and not record:
        return CACHE[key], None
    t = time.time()
    R = LawRun(HMW, foot, law, N=300, record=record)
    o = R.run(law["alpha_hi"])
    R.set_baryons(HMW.X_ta(o["t"]))
    with np.errstate(divide="ignore", invalid="ignore"):
        q = np.where(R.mph > 0, o["m"] / R.mph, np.inf)
    sel = R.rf[1:] <= 30.0
    minq = float(np.min(q[sel][R.mph[sel] > 0])); mc = float(o["m"][sel].sum() / R.mph[sel].sum())
    res = dict(min_q=minq, Mc_over_Mph=mc, settled=minq >= 0.99, overfilled=mc - 1 > 0.01, pass_=bool(minq >= 0.99 and mc - 1 <= 0.01),
               n=int(o["n"]), hit_cap=bool(o["hit_cap"]), mass_err=float(o["mass_err"]), runtime_s=time.time() - t)
    CACHE[key] = res
    json.dump(CACHE, open(CACHE_F, "w"), indent=0, sort_keys=True)
    return res, (R if record else None)


def both(law):
    r = {f: gtest(law, f)[0] for f in FOOTS}
    return r, all(r[f]["pass_"] for f in FOOTS)


def lawstr(law):
    if law["kind"] == "const":
        s = f"const alpha {law['alpha_hi']:g}"
    elif law["kind"] == "step":
        s = f"step {VNAME[law['var']]} {'<' if law['orient'] == 'dec' else '>'} {law['xstar']:.4g}, alpha_hi {law['alpha_hi']:g}"
    else:
        s = f"{law['form']} {law['orient']} {VNAME[law['var']]} x*={law['xstar']:.4g}, alpha_hi {law['alpha_hi']:g}"
    return s + (" x gate" if law.get("gate") else "")


def gline(law, r):
    return (f"    {lawstr(law)}: " + "; ".join(f"{f} min q {r[f]['min_q']:.4f} Mc/Mph {r[f]['Mc_over_Mph']:.4f} "
                                             f"{'PASS' if r[f]['pass_'] else 'FAIL'}" for f in FOOTS))


CONST = lambda a: dict(kind="const", alpha_hi=a, gate=False)

# ---- GT0 controls (K-G2) and the recorded G distribution at alpha = 0.5
P("G: CFG598 P0 MW drift PDE, N = 300, run to t0; pass iff CFG598 (i): min q >= 0.99 for r <= 30 kpc and M_c/M_ph(<30) - 1 <= 0.01")
kg2 = {}; GDIST = {}
for f in FOOTS:
    for a in (0.25, 0.5, 1.0):
        if a == 0.5 and not MUT:
            r, R = gtest(CONST(a), f, record=True)
            h = R.hist; GDIST[f] = {}
            for k in HB:
                c = np.cumsum(h[k]); c = c / c[-1]; mid = 0.5 * (HB[k][1:] + HB[k][:-1])
                qs = {p: float(np.interp(p, c, mid)) for p in (0.01, 0.05, 0.5, 0.95, 0.99)}
                if k in ("xr", "xg", "xJ"):
                    qs = {p: 10 ** v for p, v in qs.items()}
                GDIST[f][k] = qs
        else:
            r = gtest(CONST(a), f)[0]
        ref = R598[f"P0|{f}|{a:g}"]
        kg2[f"{f}|{a:g}"] = dict(min_q=r["min_q"], ref=ref["min_q"], Mc=r["Mc_over_Mph"], refMc=ref["Mc_over_Mph"],
                                 rel=max(abs(r["min_q"] / ref["min_q"] - 1), abs(r["Mc_over_Mph"] / ref["Mc_over_Mph"] - 1)))
okg2 = all(v["rel"] <= 1e-9 for v in kg2.values())
K["K-G2"] = dict(pass_=bool(okg2), runs=kg2)
P(f"K-G2 G-test code with F = 1 vs CFG598 MW P0 (alpha 0.25, 0.5, 1; both footings): max rel. diff "
  f"{max(v['rel'] for v in kg2.values()):.1e} -> {'PASS' if okg2 else 'FAIL'}")
if not MUT:
    P("  G region (flux-weighted donor states at alpha = 0.5; 1% / 50% / 99% quantiles; Mach = 0 in P0):")
    for f in FOOTS:
        g = GDIST[f]
        P(f"   [{f}] x_rho {g['xr'][0.01]:.3g} / {g['xr'][0.5]:.3g} / {g['xr'][0.99]:.3g} (rho_m {g['xr'][0.01] * RHOL[f] * 1e-9:.2e} .. "
          f"{g['xr'][0.99] * RHOL[f] * 1e-9:.2e} Msun/pc^3); g/a0 {g['xg'][0.01]:.3g} / {g['xg'][0.5]:.3g} / {g['xg'][0.99]:.3g}; "
          f"y_J {g['xJ'][0.01]:.3g} / {g['xJ'][0.5]:.3g} / {g['xJ'][0.99]:.3g}; q {g['xq'][0.01]:.3f} / {g['xq'][0.5]:.3f} / {g['xq'][0.99]:.3f}; "
          f"delta {g['xd'][0.01]:.2f} / {g['xd'][0.5]:.2f} / {g['xd'][0.99]:.2f}")
    RES["G_distribution"] = GDIST
    # G-inf (report only): free-fall Mach in the settled MW at t0
    GINF = {}
    for f in FOOTS:
        R0 = C.Run(HMW, f, "P0", N=300); R0.set_baryons(1.0)
        rf = R0.rf; Mt = R0.Mbf + (R0.Mphf - R0.Mphf[0]); gf = GK * Mt / rf ** 2
        rph = R0.mph / R0.V; gc = np.sqrt(gf[1:] * gf[:-1]); dr = np.diff(rf)
        Phi = np.concatenate([np.cumsum((gc * dr)[::-1])[::-1], [0.0]])
        vff = np.sqrt(2 * Phi[:-1])
        itg = rph * gc * dr; S = np.cumsum(itg[::-1])[::-1] - 0.5 * itg
        sJ = np.sqrt(np.where(rph > 0, S / np.where(rph > 0, rph, 1), 0))
        s = (R0.rc >= 10.0) & (R0.rc <= 0.9 * HMW.rta0) & (sJ > 0)
        mff = vff[s] / sJ[s]
        GINF[f] = dict(min=float(mff.min()), median=float(np.median(mff)), max=float(mff.max()), rta_kpc=HMW.rta0)
        P(f"   [{f}] G-inf (report only): free-fall Mach v_ff/sigma_J over 10 kpc .. 0.9 r_ta = {mff.min():.2f} / {np.median(mff):.2f} / "
          f"{mff.max():.2f} (min / median / max); r_ta {HMW.rta0:.0f} kpc")
    RES["G_inf"] = GINF
    p2 = {f: R598[f"P2|{f}|{a}"]["Mc_over_Mph"] for f in FOOTS for a in ("0.5",)}
    P(f"   CFG598 P2 (infall placement) MW: OVERFILLED at every alpha (M_c/M_ph(<30) {R598['P2|can|0']['Mc_over_Mph']:.2f} / "
      f"{R598['P2|alt|0']['Mc_over_Mph']:.2f} at alpha 0) -- the galaxy outcome if a Mach factor defers settling to post-collapse")
P()


if MUT and os.path.exists(os.path.join(HERE, "cfg913_results.json")):
    RES["G_distribution"] = {f: {k: {float(p): v for p, v in d.items()} for k, d in g.items()}
                             for f, g in json.load(open(os.path.join(HERE, "cfg913_results.json")))["G_distribution"].items()}

# ================================================================================================= 5. edges, G-tests, verdicts
def edges(MR, DR):
    E = {}
    for f in FOOTS:
        E[f] = {}
        for v in PDEV:
            E[f][v] = dict(M_core=MR[f]["core"][v], M_wide=MR[f]["wide"][v], D_cons=DR[f]["cons"][v], D_len=DR[f]["len"][v])
    return E


def step(v, orient, xs, ahi=ALPHA_HI, gate=False):
    return dict(kind="step", var=v, orient=orient, xstar=float(xs), alpha_hi=ahi, gate=gate)


def smooth_density_consts(DR, f, which):
    """R3: largest x* (most G-favourable) with alpha_hi F(x_rho/x*) <= alpha_D,loc at every D state; also the literal edge value."""
    st = DR[f]["_st"]; rmax = 0.45 if which == "cons" else DR[f]["info"]["r50_pc"] * 1e-3
    s = st["r"] <= rmax; x = st["xr"][s]; aD = st["aDloc"][s]
    out = {}
    for form in ("rat1", "rat2", "exp"):
        a = np.minimum(aD / ALPHA_HI, 0.999999)
        if form == "rat1":
            xs = x / (1 / a - 1)
        elif form == "rat2":
            xs = x / np.sqrt(1 / a - 1)
        else:
            xs = x / np.log(1 / a)
        ie = int(np.argmin(x))
        out[form] = dict(xstar=float(xs.min()), xstar_edge=float(xs[ie]), binding_at_edge=bool(np.isclose(xs.min(), xs[ie], rtol=1e-12)))
    return out


def verdicts(MR, DR, tag, run_tests=True):
    """the whole decision procedure of FROZEN_CRITERIA section 5; returns a dict (and prints)."""
    E = edges(MR, DR); V = dict(edges=E, gtests={}, pairwise={}, classes={})
    P(f"=== {tag}: edges (per footing) ===")
    for f in FOOTS:
        P(f"  [{f}] " + "; ".join(f"{VNAME[v]}: M {E[f][v]['M_core'][0]:.3g}..{E[f][v]['M_core'][1]:.3g}, D {E[f][v]['D_cons'][0]:.3g}.."
                                   f"{E[f][v]['D_cons'][1]:.3g} (len {E[f][v]['D_len'][0]:.3g}..)" for v in PDEV))
    # ---- GT1: pairwise step tests
    P(f"--- GT1 single-variable steps at the M-core and D-conservative edges (alpha_hi {ALPHA_HI:g}) ---")
    pw = {}
    for v in PDEV:
        for orient in ("dec", "inc"):
            for edge in ("M_core", "D_cons"):
                res = {}
                for f in FOOTS:
                    xs = E[f][v][edge][0] if orient == "dec" else E[f][v][edge][1]
                    res[f] = gtest(step(v, orient, xs), f)[0]
                ok = all(res[f]["pass_"] for f in FOOTS)
                law_c = step(v, orient, E["can"][v][edge][0 if orient == "dec" else 1])
                P(f"  [{edge:6s}] " + gline(law_c, res).strip() + (f"  (alt x* {E['alt'][v][edge][0 if orient == 'dec' else 1]:.4g})"))
                pw[(v, orient, edge)] = ok
                V["gtests"][f"GT1|{v}|{orient}|{edge}"] = dict(res=res, pass_=ok)
    # ---- GT2: density at the D-lenient edge (alpha_hi 1, 0.5) and D-cons with alpha_hi 0.5
    P("--- GT2 decreasing density step at the D-lenient edge (alpha_hi 1.0, 0.5) and at the D-conservative edge (alpha_hi 0.5) ---")
    gt2 = {}
    for edge, ahi in (("D_len", 1.0), ("D_len", 0.5), ("D_cons", 0.5)):
        res = {f: gtest(step("xr", "dec", E[f]["xr"][edge][0], ahi), f)[0] for f in FOOTS}
        ok = all(res[f]["pass_"] for f in FOOTS); gt2[(edge, ahi)] = ok
        P(f"  [{edge:6s}] " + gline(step("xr", "dec", E["can"]["xr"][edge][0], ahi), res).strip())
        V["gtests"][f"GT2|{edge}|{ahi:g}"] = dict(res=res, pass_=ok)
    gt2[("D_cons", 1.0)] = pw[("xr", "dec", "D_cons")]
    # ---- GT3: smooth density forms with R3 constants
    P("--- GT3 smooth decreasing density forms, x* from the D bound (R3), alpha_hi 1.0 ---")
    gt3 = {}
    for which in ("cons", "len"):
        for form in ("rat1", "rat2", "exp"):
            res = {}; xsd = {}
            for f in FOOTS:
                cst = smooth_density_consts(DR, f, which)[form]; xsd[f] = cst
                res[f] = gtest(dict(kind="smooth", var="xr", orient="dec", form=form, xstar=cst["xstar"], alpha_hi=ALPHA_HI, gate=False), f)[0]
            ok = all(res[f]["pass_"] for f in FOOTS)
            # M check: alpha at M states (lowest density -> largest alpha) must be < alpha_M (ungated lenient)
            mfac = {f: ALPHA_HI * {"rat1": 1 / (1 + MR[f]["core"]["xr"][0] / xsd[f]["xstar"]),
                                   "rat2": 1 / (1 + (MR[f]["core"]["xr"][0] / xsd[f]["xstar"]) ** 2),
                                   "exp": math.exp(-MR[f]["core"]["xr"][0] / xsd[f]["xstar"])}[form] for f in FOOTS}
            gt3[(which, form)] = dict(G=ok, xstar={f: xsd[f] for f in FOOTS}, alpha_at_M_min_density=mfac,
                                      M_ok=all(mfac[f] < ALPHA_M_UNG for f in FOOTS))
            P(f"  [D_{which:4s}] " + gline(dict(kind="smooth", var="xr", orient="dec", form=form, xstar=xsd["can"]["xstar"], alpha_hi=ALPHA_HI),
                                            res).strip() + f"  | x* binding at D edge: {xsd['can']['binding_at_edge']}/{xsd['alt']['binding_at_edge']}; "
              f"alpha at the lowest-density M state {mfac['can']:.3f}/{mfac['alt']:.3f} (needs < {ALPHA_M_UNG})")
            V["gtests"][f"GT3|{which}|{form}"] = dict(res=res, **gt3[(which, form)])
    # ---- GT5: gate (report only)
    P("--- GT5 (report only, R5): the gate in the P0 PDE ---")
    for nm5 in ("gate_const", "gate_xr_Dcons"):
        res = {}
        for f in FOOTS:
            L_ = dict(kind="const", alpha_hi=ALPHA_HI, gate=True) if nm5 == "gate_const" else step("xr", "dec", E[f]["xr"]["D_cons"][0], gate=True)
            res[f] = gtest(L_, f)[0]
        L_ = dict(kind="const", alpha_hi=ALPHA_HI, gate=True) if nm5 == "gate_const" else step("xr", "dec", E["can"]["xr"]["D_cons"][0], gate=True)
        P("  " + gline(L_, res).strip())
        V["gtests"]["GT5|" + nm5] = dict(res=res, pass_=all(res[f]["pass_"] for f in FOOTS))

    # ---- R1 pairwise separability
    gq = RES.get("G_distribution") or {}
    MB = {f: MR[f]["core"]["xMB"] for f in FOOTS}; MA = {f: MR[f]["core"]["xMA"] for f in FOOTS}
    sepMG = {v: any(pw[(v, o, "M_core")] for o in ("dec", "inc")) for v in PDEV}
    sepDG = {v: any(pw[(v, o, "D_cons")] for o in ("dec", "inc")) for v in PDEV}
    sepDG_len = dict(sepDG); sepDG_len["xr"] = sepDG["xr"] or gt2[("D_len", 1.0)]
    sepMG["xM"] = all(MB[f][0] > 0 for f in FOOTS); sepDG["xM"] = False; sepDG_len["xM"] = False
    sepMG_A = all(MA[f][0] > 0 for f in FOOTS)
    gdl = min(gq[f]["xd"][0.01] for f in FOOTS) if gq else -1.0
    sepMG["xd"] = False                                       # gate-open merger states delta in (0, 1] overlap G's settling delta
    sepDG["xd"] = gdl > EPS_FLUCT; sepDG_len["xd"] = sepDG["xd"]
    nat_MG = all(MB[f][0] > 1.0 for f in FOOTS); nat_MG_A = all(MA[f][0] > 1.0 for f in FOOTS)
    V["pairwise"] = dict(MG=sepMG, DG=sepDG, DG_lenient=sepDG_len, MG_Mach_frameA=sepMG_A, Mach_natural_MG_B=nat_MG,
                         Mach_natural_MG_A=nat_MG_A, G_delta_q01=gdl, Mach_B_min=MB, Mach_A_min=MA)
    P("--- R1 pairwise separability (any function of ONE variable) ---")
    for v in PDEV + ("xM", "xd"):
        P(f"  {VNAME[v]:18s} M|G: {'SEPARABLE' if sepMG[v] else 'not separable'}"
          + (f" (frame B min Mach {MB['can'][0]:.3f}/{MB['alt'][0]:.3f}; frame A {MA['can'][0]:.3f}/{MA['alt'][0]:.3f})" if v == "xM" else "")
          + f"   D|G: {'SEPARABLE' if sepDG[v] else 'not separable'}" + (" (lenient D: SEPARABLE)" if sepDG_len[v] and not sepDG[v] else ""))
    P(f"  delta: G's flux-weighted 1% quantile {gdl:.3f} (D skin at 0 + eps {EPS_FLUCT}); gate-open merger states delta in (0, 1] overlap G")

    # ---- classes
    CL = {}
    # C0 constant
    CL["C0 constant alpha"] = dict(label="INFEASIBLE IN THE DECLARED CLASS",
                                   obstruction=f"M-G: alpha < {ALPHA_M_UNG} vs G alpha in ({ALPHA_G_LO}, {ALPHA_G_HI}]; D-G: alpha <= "
                                               f"{max(ac):.2e} (CFG882) vs G")
    # C1 gate
    CL["C1 gate alpha*1[delta>0]"] = dict(label="INFEASIBLE IN THE DECLARED CLASS",
                                          obstruction=f"D-G: gated kinetic alpha <= {ALPHA_D_GAT:.2e} (CFG889) vs G > {ALPHA_G_LO}; M-G NOT "
                                                      f"ESTABLISHED at node resolution (lenient gated M < {ALPHA_M_GAT} overlaps G > {ALPHA_G_LO}); "
                                                      "G for gate laws UNDETERMINED (CFG639 Part A NOT DIAGNOSTIC)")
    # C2 steps (PDE variables)
    for v in PDEV:
        for orient in ("dec", "inc"):
            eM, eD = pw[(v, orient, "M_core")], pw[(v, orient, "D_cons")]
            # M u D edge = the stricter edge: decreasing -> min, increasing -> max; its G-test is one of the two runs
            strict = {}
            for f in FOOTS:
                xm = E[f][v]["M_core"][0 if orient == "dec" else 1]; xd_ = E[f][v]["D_cons"][0 if orient == "dec" else 1]
                strict[f] = "M_core" if ((xm <= xd_) if orient == "dec" else (xm >= xd_)) else "D_cons"
            feas = all(gtest(step(v, orient, E[f][v][strict[f]][0 if orient == "dec" else 1]), f)[0]["pass_"] for f in FOOTS)
            if feas:
                lab = "FEASIBLE WITH ONE NEW CONSTANT"; obs = f"{VNAME[v]}_* (threshold)"
                nat = NATURAL[v]
                if nat is not None and all((nat <= E[f][v][strict[f]][0]) if orient == "dec" else (nat >= E[f][v][strict[f]][1]) for f in FOOTS):
                    if all(gtest(step(v, orient, nat), f)[0]["pass_"] for f in FOOTS):
                        lab = "FEASIBLE WITH NO NEW CONSTANT"
            else:
                lab = "INFEASIBLE IN THE DECLARED CLASS"
                blk = [p for p, ok in (("M-G", eM), ("D-G", eD)) if not ok]
                obs = f"{', '.join(blk) if blk else 'M and D edges jointly'} not separable in {VNAME[v]} ({orient})"
            CL[f"C2 step {VNAME[v]} {orient}"] = dict(label=lab, obstruction=obs, edge_tests=dict(M=eM, D=eD))
    CL["C2 step Mach"] = dict(label="INFEASIBLE IN THE DECLARED CLASS", obstruction="D-G: clump and P0 galaxy both at Mach = 0")
    CL["C2 step delta"] = dict(label="INFEASIBLE IN THE DECLARED CLASS",
                               obstruction="M-G: gate-open merger states (delta in (0,1], CFG639 B-M1) overlap settling delta; D-G: gate fails "
                                           "kinetically (CFG889)")
    # C3 smooth single-variable
    for which in ("cons",):
        for form in ("rat1", "rat2", "exp"):
            g3 = gt3[(which, form)]
            if g3["M_ok"] and g3["G"]:
                lab, obs = "FEASIBLE WITH ONE NEW CONSTANT", "rho_* (scale)"
            else:
                lab = "INFEASIBLE IN THE DECLARED CLASS"
                obs = "; ".join(x for x, bad in ((f"M-G: alpha at merger densities {g3['alpha_at_M_min_density']['can']:.2f} >= {ALPHA_M_UNG}",
                                                   not g3["M_ok"]), ("D-G: G-test fails at the D-bound scale", not g3["G"])) if bad)
            CL[f"C3 {form} density (D-{which})"] = dict(label=lab, obstruction=obs)
    # C3 natural-scale smooth forms in g/a0, y_J, Mach (x* = 1): D and M checked analytically
    for v in ("xg", "xJ"):
        for form in ("rat1", "rat2", "exp"):
            for orient in ("dec", "inc"):
                fz = lambda z: {"rat1": 1 / (1 + z), "rat2": 1 / (1 + z * z), "exp": math.exp(-z)}[form]
                F = (lambda z: fz(z)) if orient == "dec" else (lambda z: 1 - fz(z))
                okD = all(max(ALPHA_HI * F(x) / a for x, a in zip(DR[f]["_st"][v][DR[f]["_st"]["r"] <= 0.45],
                                                                  DR[f]["_st"]["aDloc"][DR[f]["_st"]["r"] <= 0.45])) <= 1.0 for f in FOOTS)
                okM = all(ALPHA_HI * max(F(MR[f]["core"][v][0]), F(MR[f]["core"][v][1])) < ALPHA_M_UNG for f in FOOTS)
                CL[f"C3 {form} {orient} {VNAME[v]} (x*=1)"] = dict(
                    label="INFEASIBLE IN THE DECLARED CLASS" if not (okD and okM) else "NEEDS G-TEST",
                    obstruction=", ".join(x for x, bad in (("D (alpha above alpha_D,loc at clump states)", not okD),
                                                           ("M (alpha >= alpha_M at merger states)", not okM)) if bad))
    for form in ("rat1", "rat2", "exp"):
        CL[f"C3 {form} Mach (x*=1)"] = dict(label="INFEASIBLE IN THE DECLARED CLASS", obstruction="D: Mach = 0 in the clump gives alpha_hi")
    # C4 products
    CL["C4a gate x Mach step"] = dict(label="INFEASIBLE IN THE DECLARED CLASS",
                                      obstruction="D: clump skin has Mach = 0 and delta > 0 fluctuations; gated erosion alpha*t50 = 105-148 Myr (CFG889)")
    # C4b Mach step x density step
    Gcons1, Glen1, Gcons05, Glen05 = gt2[("D_cons", 1.0)], gt2[("D_len", 1.0)], gt2[("D_cons", 0.5)], gt2[("D_len", 0.5)]
    MachB, MachA = nat_MG, nat_MG_A
    base_q = ["CONDITIONAL-P0"] + ([] if MachB else ["CONDITIONAL-FRAME"])
    quals = list(base_q)
    if (MachB or MachA) and (Gcons1 or Glen1):
        if not Gcons1:
            quals.append("CONDITIONAL-D-LENIENT")
        tested = []
        for f in FOOTS:
            pts = [("M_core", E[f]["xr"]["M_core"][0]), ("D_cons", E[f]["xr"]["D_cons"][0]), ("D_len", E[f]["xr"]["D_len"][0])]
            okp = [(nm, x) for nm, x in pts if gtest(step("xr", "dec", x), f)[0]["pass_"]]
            tested.append(min(x for nm, x in okp) if okp else None)
        edge = "D_cons" if Gcons1 else "D_len"
        rng = {f: [tested[i], E[f]["xr"][edge][0]] for i, f in enumerate(FOOTS)}
        CL["C4b Mach step (1) x density step"] = dict(
            label="FEASIBLE WITH ONE NEW CONSTANT", qualifiers=quals,
            constant="rho_* (density threshold, x_rho = rho_m/rho_Lambda)",
            admissible_x_rho={f: rng[f] for f in FOOTS},
            admissible_rho_Msun_pc3={f: [rng[f][0] * RHOL[f] * 1e-9 if rng[f][0] else None, rng[f][1] * RHOL[f] * 1e-9] for f in FOOTS},
            alpha_hi_tested={"1.0": dict(D_cons=Gcons1, D_len=Glen1), "0.5": dict(D_cons=Gcons05, D_len=Glen05)},
            obstruction="")
    else:
        CL["C4b Mach step (1) x density step"] = dict(
            label="INFEASIBLE IN THE DECLARED CLASS",
            obstruction=", ".join(x for x, bad in ((f"M: Mach <= 1 at some merger states (frame B min {MB['can'][0]:.2f}/{MB['alt'][0]:.2f}, "
                                                    f"frame A {MA['can'][0]:.2f}/{MA['alt'][0]:.2f})", not (MachB or MachA)),
                                                   ("D-G: G-test fails with rho_* at the D edge (conservative and lenient)", not (Gcons1 or Glen1))) if bad))
    # C4c gate x density step: M gate-open states below the D edge get alpha_hi
    mbelow = all(MR[f]["core"]["xr"][0] < E[f]["xr"]["D_cons"][0] for f in FOOTS)
    CL["C4c gate x density step"] = dict(
        label="INFEASIBLE IN THE DECLARED CLASS" if (mbelow and ALPHA_HI >= ALPHA_M_GAT) else "SEE NOTES",
        obstruction=f"M-G: gate-open merger states lie below rho_* (min merger x_rho {MR['can']['core']['xr'][0]:.3g} < D edge "
                    f"{E['can']['xr']['D_cons'][0]:.3g}) and get alpha_hi >= 0.5 > gated lenient {ALPHA_M_GAT}; D also gated kinetic (CFG889)")
    # C4d Mach step x other C2 steps that separate D from G
    for v in ("xg", "xJ", "xq"):
        okv = sepDG[v]
        CL[f"C4d Mach step x {VNAME[v]} step"] = dict(
            label=("FEASIBLE WITH ONE NEW CONSTANT" if (okv and (MachB or MachA)) else "INFEASIBLE IN THE DECLARED CLASS"),
            qualifiers=list(base_q) if (okv and (MachB or MachA)) else [],
            obstruction="" if (okv and (MachB or MachA)) else (f"D-G not separable in {VNAME[v]}" if not okv else "M: Mach <= 1 at some merger states"))
    # C5 smooth Mach x smooth density
    for n in (1, 2):
        okM5 = {fr: all(ALPHA_HI / (1 + MB[f][0] ** n) < ALPHA_M_UNG for f in FOOTS) for fr in ("B",)}
        okM5A = all(ALPHA_HI / (1 + MA[f][0] ** n) < ALPHA_M_UNG for f in FOOTS)
        for form in ("rat1", "rat2", "exp"):
            g3 = gt3[("cons", form)]
            ok = (okM5["B"] or okM5A) and g3["G"]
            CL[f"C5 1/(1+Mach^{n}) x {form} density"] = dict(
                label="FEASIBLE WITH ONE NEW CONSTANT" if ok else "INFEASIBLE IN THE DECLARED CLASS",
                qualifiers=(["CONDITIONAL-P0"] + ([] if okM5["B"] else ["CONDITIONAL-FRAME"])) if ok else [],
                obstruction="" if ok else ", ".join(x for x, bad in (
                    (f"M: alpha_hi/(1+Mach_min^{n}) = {ALPHA_HI / (1 + MB['can'][0] ** n):.3f}/{ALPHA_HI / (1 + MB['alt'][0] ** n):.3f} (B) >= "
                     f"{ALPHA_M_UNG}", not (okM5['B'] or okM5A)), ("D-G: smooth density G-test fails", not g3["G"])) if bad))
    V["classes"] = CL
    # ---- overall
    rank = {"FEASIBLE WITH NO NEW CONSTANT": 0, "FEASIBLE WITH ONE NEW CONSTANT": 1, "UNDETERMINED": 2, "NEEDS G-TEST": 2,
            "SEE NOTES": 3, "INFEASIBLE IN THE DECLARED CLASS": 4}
    best = min(rank[c["label"]] for c in CL.values())
    feas = [k for k, c in CL.items() if rank[c["label"]] == best]
    if best <= 1:
        overall = CL[feas[0]]["label"]
        qset = sorted(set(q for k in feas for q in CL[k].get("qualifiers", [])))
        # a feasible class without a qualifier beats one with
        clean = [k for k in feas if not CL[k].get("qualifiers")]
        overall_q = [] if clean else sorted(set.intersection(*[set(CL[k].get("qualifiers", [])) for k in feas]))
    else:
        overall = "INFEASIBLE IN THE DECLARED CLASSES"; overall_q = []
    MGs = [v for v in sepMG if sepMG[v]]; DGs = [v for v in sepDG if sepDG[v]]; DGl = [v for v in sepDG_len if sepDG_len[v]]
    inter = sorted(set(MGs) & set(DGs))
    if inter:
        minimal = [[v] for v in inter]
    elif MGs and DGs:
        minimal = [[a, b] for a in MGs for b in DGs]
    else:
        minimal = []
    V["overall"] = dict(label=overall, qualifiers=overall_q, feasible_classes=feas if best <= 1 else [],
                        M_G_separators=MGs, D_G_separators=DGs, D_G_separators_lenient=DGl, minimal_variable_sets=minimal)
    P(f"--- classes ({tag}) ---")
    for k, c in CL.items():
        extra = ""
        if c.get("qualifiers"):
            extra += " [" + ", ".join(c["qualifiers"]) + "]"
        if c.get("admissible_rho_Msun_pc3"):
            extra += " rho_* in " + "; ".join(f"{f} [{(c['admissible_rho_Msun_pc3'][f][0] or float('nan')):.3g}, "
                                             f"{c['admissible_rho_Msun_pc3'][f][1]:.3g}] Msun/pc^3" for f in FOOTS)
        P(f"  {k:42s} {c['label']}{extra}" + (f" -- {c['obstruction']}" if c.get("obstruction") else ""))
    P(f"OVERALL ({tag}): {overall}" + (f" [{', '.join(overall_q)}]" if overall_q else "")
      + (f"; feasible classes: {', '.join(feas)}" if best <= 1 else ""))
    P(f"  M-G separators: {[VNAME[v] for v in MGs] or 'none'}; D-G separators: {[VNAME[v] for v in DGs] or 'none'}"
      f" (lenient D: {[VNAME[v] for v in DGl] or 'none'}); minimal variable set(s): "
      f"{[[VNAME[v] for v in s] for s in minimal] or 'none in the declared variables'}")
    return V


VMAIN = verdicts(MREG, DREG, "MAIN")


def jclean(o):
    if isinstance(o, dict):
        return {(k if isinstance(k, str) else ("|".join(map(str, k)) if isinstance(k, tuple) else str(k))): jclean(v)
                for k, v in o.items() if k != "_st"}
    if isinstance(o, (list, tuple)):
        return [jclean(x) for x in o]
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return o


RES["K"] = K; RES["K_all_pass"] = all(v["pass_"] for v in K.values())
RES["main"] = VMAIN
P()
P("K summary: " + ", ".join(f"{k} {'PASS' if v['pass_'] else 'FAIL'}" for k, v in K.items()))

# ================================================================================================= 6. MUTATE
# ================================================================================================= 5b. POST-HOC diagnostics (report only)
# Added after the first full run had been seen (disclosed in the README). No class weight; the frozen verdicts above are unchanged.
def gprofile(law, foot):
    R = LawRun(HMW, foot, law, N=300)
    o = R.run(law["alpha_hi"]); R.set_baryons(HMW.X_ta(o["t"]))
    m = o["m"]
    with np.errstate(divide="ignore", invalid="ignore"):
        q = np.where(R.mph > 0, m / R.mph, np.inf)
    sel = (R.rf[1:] <= 30.0) & (R.mph > 0)
    i = int(np.argmin(np.where(sel, q, np.inf))); j = int(np.argmax(np.where(sel, q, -np.inf)))
    st = R.state(m); fz = law_factor(law, st) == 0
    rfz = float(R.rc[fz & (R.rc <= 30.0)].max()) if (fz & (R.rc <= 30.0)).any() else 0.0
    return dict(min_q=float(q[i]), r_min_q_kpc=float(R.rc[i]), rhoph_over_rhob_at_min=float((R.mph[i] / R.V[i]) / max(R.rhob[i], 1e-300)),
                max_q=float(q[j]), r_max_q_kpc=float(R.rc[j]), r_frozen_max_kpc=rfz,
                Mc_over_Mph_30=float(m[R.rf[1:] <= 30.0].sum() / R.mph[R.rf[1:] <= 30.0].sum()),
                Mph_inside_rfrozen_over_Mph30=float(R.mph[R.rc <= rfz].sum() / R.mph[R.rf[1:] <= 30.0].sum()) if rfz > 0 else 0.0)


PH = {}
if not MUT:
    P()
    P("=== POST-HOC diagnostics (report only; added after the first full run; no class weight) ===")
    P("PH1 merger core states with Mach <= 1: where they sit and which baryons dominate locally")
    PH["PH1"] = {}
    for f in FOOTS:
        core = [r for r in MROWS[f] if r["win"] and r["s"] <= 200.0]
        lowA = [r for r in core if r["xMA"] <= 1]; lowB = [r for r in core if r["xMB"] <= 1]
        domA = {}
        for r in lowA:
            c = r["comp"]; k = max(("gS", "kS", "gM"), key=lambda z: c[z]); domA[k] = domA.get(k, 0) + 1
        fstarB = float(np.median([(r["comp"]["sS"] + r["comp"]["sM"]) / (r["comp"]["sS"] + r["comp"]["sM"] + r["comp"]["gS"] + r["comp"]["kS"]
                                                                          + r["comp"]["gM"]) for r in lowB])) if lowB else None
        epA = sorted(set(round(r["t_after"], 3) for r in lowA))
        PH["PH1"][f] = dict(n_core=len(core), n_lowA=len(lowA), lowA_s=sorted(set(r["s"] for r in lowA)), lowA_epochs=epA,
                            lowA_dominant_gas=domA, n_lowB=len(lowB), lowB_median_star_share=fstarB)
        P(f"  [{f}] frame A: {len(lowA)} of {len(core)} core states, at s = {sorted(set(r['s'] for r in lowA))} kpc, epochs "
          f"{epA[:3]}..{epA[-3:] if epA else ''} Gyr; dominant local gas there {domA} (gS sub gas, kS cool-core cloud, gM main gas)")
        P(f"  [{f}] frame B: {len(lowB)} of {len(core)} core states; median star share of local baryons there {fstarB:.2f}"
          " (the sub's stars co-move with its cold energy)")
    P("PH2 decreasing density step (alpha_hi 1): where the MW misses the frozen (i) rule")
    PH["PH2"] = {}
    for edge in ("D_len", "D_cons"):
        for f in FOOTS:
            x = VMAIN["edges"][f]["xr"][edge][0]
            d = gprofile(step("xr", "dec", x), f); PH["PH2"][f"{edge}|{f}"] = d
            P(f"  [{edge} {f}] rho_* {x * RHOL[f] * 1e-9:.3g} Msun/pc^3: frozen (alpha = 0) out to r = {d['r_frozen_max_kpc']:.2f} kpc "
              f"(holding {d['Mph_inside_rfrozen_over_Mph30']:.3f} of M_ph(<30)); min q {d['min_q']:.4f} at r = {d['r_min_q_kpc']:.2f} kpc "
              f"(rho_ph/rho_b there {d['rhoph_over_rhob_at_min']:.3f}); max q {d['max_q']:.2f} at r = {d['r_max_q_kpc']:.2f} kpc; "
              f"M_c/M_ph(<30) {d['Mc_over_Mph_30']:.3f}")
    P("PH2b decreasing y_J step at the M-core edge (alpha_hi 1): the transport-weighted G states lie below it (99% quantile), yet the MW fails")
    for f in FOOTS:
        x = VMAIN["edges"][f]["xJ"]["M_core"][0]
        d = gprofile(step("xJ", "dec", x), f); PH["PH2"][f"yJ_M_core|{f}"] = d
        P(f"  [{f}] y_J* {x:.3f}: frozen out to r = {d['r_frozen_max_kpc']:.2f} kpc (holding {d['Mph_inside_rfrozen_over_Mph30']:.3f} of M_ph(<30)); "
          f"min q {d['min_q']:.4f} at r = {d['r_min_q_kpc']:.2f} kpc; max q {d['max_q']:.2f} at r = {d['r_max_q_kpc']:.2f} kpc; "
          f"M_c/M_ph(<30) {d['Mc_over_Mph_30']:.3f}")
    RES["post_hoc"] = PH

bite = None
if MUT:
    P()
    P("=== MUTATE: one constraint's local conditions perturbed by an order of magnitude ===")
    MUTS = {}
    import copy
    for nm, kind, s in (("MUT-A merger Mach / 10", "M", 0.1), ("MUT-B merger Mach x 10", "M", 10.0),
                        ("MUT-C clump density x 10", "D", 10.0), ("MUT-D clump density / 10", "D", 0.1)):
        if kind == "M":
            MR2 = copy.deepcopy(MREG)
            for f in FOOTS:
                for reg in ("core", "wide", "obs"):
                    for k in ("xMB", "xMA"):
                        MR2[f][reg][k] = [x * s for x in MR2[f][reg][k]]
            V2 = verdicts(MR2, DREG, nm)
        else:
            DR2 = d_region(s)
            V2 = verdicts(MREG, DR2, nm)
        changed = (V2["overall"]["label"] != VMAIN["overall"]["label"]
                   or V2["overall"]["minimal_variable_sets"] != VMAIN["overall"]["minimal_variable_sets"])
        ctab = sorted(k for k in VMAIN["classes"] if V2["classes"].get(k, {}).get("label") != VMAIN["classes"][k]["label"])
        MUTS[nm] = dict(overall=V2["overall"], changed=changed, class_changes=ctab)
        P(f"  -> {nm}: overall {V2['overall']['label']} (main {VMAIN['overall']['label']}); minimal set "
          f"{V2['overall']['minimal_variable_sets']} (main {VMAIN['overall']['minimal_variable_sets']}); "
          f"{'CHANGED' if changed else 'unchanged'}; class-table changes: {ctab or 'none'}")
        P()
    bite = any(v["changed"] for v in MUTS.values())
    RES["MUTATE"] = dict(runs=MUTS, bites=bite)
    P(f"MUTATE tooth (overall label or minimal set changes in at least one run): {'BITES' if bite else 'DOES NOT BITE'}")
    # POST-HOC positive control of the decision logic (added after the first MUTATE run had been designed around single
    # perturbations; no verdict weight): remove BOTH obstructions at once -- merger Mach x 100 and clump densities x 100.
    P()
    P("POST-HOC positive control (no verdict weight): merger Mach x 100 AND clump densities x 100 together")
    MR3 = copy.deepcopy(MREG)
    for f in FOOTS:
        for reg in ("core", "wide", "obs"):
            for k in ("xMB", "xMA"):
                MR3[f][reg][k] = [x * 100.0 for x in MR3[f][reg][k]]
    V3 = verdicts(MR3, d_region(100.0), "POSITIVE CONTROL (post hoc)")
    RES["post_hoc_positive_control"] = dict(overall=V3["overall"], C4b=V3["classes"]["C4b Mach step (1) x density step"])

RES["wall_s"] = time.time() - T0
P(f"\nwall {RES['wall_s']:.0f} s")
json.dump(jclean(RES), open(os.path.join(HERE, f"cfg913_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg913{SUF}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (MUT and bite) else 0)

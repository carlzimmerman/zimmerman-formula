#!/usr/bin/env python3
"""HC1 post-freeze REPORTED readings (never graded; disclosed in RESULT.md):
  R1 KiDS isolated lensing, absolute: the fermion's predicted offset over the law vs the data's offset, per colour, K1 bins.
  R2 dSph classes inside a host fermion sea: MW / M31 solved with HC1's rule (Hernquist baryons, declared here), sea
     density at d = 50, 100, 200 kpc added to each satellite's own solve; G6 re-run with GB1's g_dsph.
  python3 hc1_report.py -> hc1_report.json / .out. EXPERIMENT; adopts nothing; no-particle rule lifted for HC1 only.
kappa = 1/2 FITTED; not theory closed."""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); src = open(os.path.join(HERE, "hc1.py")).read()
cut = src.index("RES = dict(tag=TAG"); sys.argv = [sys.argv[0]]; NSH = {"__file__": os.path.join(HERE, "hc1.py"), "__name__": "hc1_lib"}
exec(compile(src[:cut], "hc1_lib", "exec"), NSH)
np = NSH["np"]; NS = NSH["NS"]; FM = NSH["FM"]; G = NSH["G"]; MS = NSH["MS"]; KPC = NSH["KPC"]; glaw = NSH["glaw"]
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
RES = {}
HOSTS = {"MW": (6.0e10, 3.0, ("MW classical", "MW ultra-faint")), "M31": (1.0e11, 4.0, ("bright M31", "M31 others"))}   # Msun, Hernquist a kpc (declared readings)
for f, a0 in NSH["A0"].items():
    B = NSH["build_B"](f, a0); NSH["attach"](B, f, a0); R = {}
    # R1 KiDS absolute
    Ee, Ll = B["K"]; K1 = NS["K1"]; gk = NS["gk"]; out = {}
    for lab, fts, gob in (("early", Ee, NS["Ek"]), ("late", Ll, NS["Lk"])):
        obs = [math.log10(4 * NS["GPC"] * gob[i] * NS["PC"] / glaw(gk[i], a0)) for i in K1]
        pred = [NSH["TOT"](f, a0)(ft)["delta"] for ft in fts]
        out[lab] = dict(obs_minus_law_mean=float(np.mean(obs)), fermion_delta_mean=float(np.mean(pred)), residual_mean=float(np.mean(obs) - np.mean(pred)), per_bin_delta=[round(x, 3) for x in pred], per_bin_obs=[round(x, 3) for x in obs])
    R["KiDS_absolute"] = out
    P(f"[{f}] R1 KiDS isolated, K1 bins: early obs-law {out['early']['obs_minus_law_mean']:+.3f}, fermion predicts {out['early']['fermion_delta_mean']:+.3f} (residual {out['early']['residual_mean']:+.3f}); "
      f"late obs-law {out['late']['obs_minus_law_mean']:+.3f}, fermion {out['late']['fermion_delta_mean']:+.3f} (residual {out['late']['residual_mean']:+.3f}); per-bin fermion Delta early {out['early']['per_bin_delta']}")
    # R2 host sea
    sea = {}
    for h, (Mb, a, cls) in HOSTS.items():
        Mt = Mb * MS; aa = a * KPC; rg = NSH["grid"](1e-3 * aa, Mt, 400 * KPC); Mbr = Mt * (rg / (rg + aa)) ** 2
        s = FM.solve(rg, Mbr, rg[-1], 10 * aa, NSH["R_FAIR"] * Mt, NSH["M_EV"], a0, gf=2.0, iters=300, G_=G)
        rho = {str(d): float(np.interp(math.log(d * KPC), np.log(rg), s["rho"][0] if s["rho"].ndim > 1 else s["rho"])) for d in (50, 100, 200)}
        sea[h] = dict(rho_kg_m3=rho, rho_Msun_pc3={k: v / (MS / NS["PC"] ** 3) for k, v in rho.items()}, sigma_kms=float(s["sigma"]) / 1e3, conv=bool(s["conv"]), cls=cls)
    R["host_sea"] = sea; P(f"[{f}] R2 host fermion sea, Msun/pc^3 at 50/100/200 kpc: " + "; ".join(f"{h} {[round(v, 6) for v in sea[h]['rho_Msun_pc3'].values()]} (sigma {sea[h]['sigma_kms']:.0f} km/s)" for h in sea))
    own = {id(p): p["feat"]["Mf"] for c_ in B["D"].values() for p in c_}
    R["G6_with_sea"] = {}
    for d in ("50", "100", "200"):
        for c_, pts in B["D"].items():
            rho = next((sea[h]["rho_kg_m3"][d] for h in sea if c_ in sea[h]["cls"]), 0.0)
            for p in pts:
                if own[id(p)] is not None: p["feat"]["Mf"] = own[id(p)] + 4 * math.pi / 3 * rho * p["feat"]["r"] ** 3
        ok, num = NS["g_dsph"](NSH["TOT"](f, a0), B, a0)
        R["G6_with_sea"][d] = dict(ok=bool(ok), classes={k: dict(med=v["median_minus_anchor"], ci=v["ci"]) for k, v in num.items() if v["graded"]})
        P(f"[{f}] R2 G6 with the host sea at d {d} kpc: {'PASS' if ok else 'FAIL'}; " + "; ".join(f"{k} {v['med']:+.3f} [{v['ci'][0]:+.3f},{v['ci'][1]:+.3f}]" for k, v in R["G6_with_sea"][d]["classes"].items()))
    RES[f] = R
P("REPORTED only, post-freeze; never graded. EXPERIMENT; adopts nothing; no-particle rule lifted for HC1 only. kappa = 1/2 FITTED; not theory closed.")
json.dump(RES, open(os.path.join(HERE, "hc1_report.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "hc1_report.out"), "w").write("\n".join(OUT) + "\n")

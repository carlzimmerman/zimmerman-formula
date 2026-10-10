"""CFG582: cool-CGM escape scoring. Criteria: FROZEN_CRITERIA.md (f9da6e77d). Inputs transcribed from source TeX (below)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
F = {"canonical": 0.8, "alt": 0.55}
# Zahedy et al. 2019 (COS-LRG II, arXiv:1809.05115, source TeX): "Within d<160 kpc from LRGs, we estimate a total cool
# gas mass of M_cool = 1.5^{+0.7}_{-0.3} x 10^10 Msun"; sample median log M* = 11.2 +- 0.2 (same TeX, citing Paper I).
meas = [dict(name="COS-LRG (Zahedy+19 II)", quiescent=True, logM=11.2, R=160.0, central=1.5e10, up=0.7e10, lo=0.3e10)]
out = []
for m in meas:
    s = (100.0 / m["R"]) if m["R"] > 100 else 1.0                    # frozen: M proportional to r beyond 100 kpc
    c100, g100 = m["central"] * s, (m["central"] + m["up"]) * s
    Ms = 10 ** m["logM"]
    req = {k: f * Ms for k, f in F.items()}; req108 = {k: f * 10 ** 10.8 for k, f in F.items()}
    ruled = all(g100 < req[k] for k in F); viable = c100 >= req["alt"]
    call = "RULED OUT" if ruled else ("VIABLE" if viable else "UNDETERMINED")
    r = dict(m, M100_central=c100, M100_generous=g100, required=req, required_at_10p8=req108, call=call,
             frac_of_Mstar_generous=g100 / Ms, shortfall_factor_alt=req["alt"] / g100)
    out.append(r)
    print(f"{m['name']}: M_cool(<100 kpc) central {c100:.2e}, generous {g100:.2e} Msun ({g100 / Ms:.3f} M*); "
          f"required {req['canonical']:.2e} / {req['alt']:.2e} (log M* {m['logM']}); at log M* 10.8: {req108['canonical']:.2e} / {req108['alt']:.2e} "
          f"-> {call} (short by x{req['alt'] / g100:.1f} for alt)")
overall = "RULED OUT" if all(r["call"] == "RULED OUT" for r in out) else ("VIABLE" if any(r["call"] == "VIABLE" for r in out) else "UNDETERMINED")
print(f"VERDICT: COOL-GAS ESCAPE {overall}  (qualifying measurements: {len(out)})")
print("context (not scored): COS-LRG extrapolated to d<500 kpc ~4e10 Msun (0.25 M*), still < 0.55 M*; "
      "Werk+14 COS-Halos (mostly star-forming) > 6.5e10 within R_vir; Afruni+19 is a model (cool gas within 160 kpc ~1% of 2.5e11).")
json.dump(dict(verdict=overall, measurements=out), open(os.path.join(HERE, "cfg582_results.json"), "w"), indent=1)

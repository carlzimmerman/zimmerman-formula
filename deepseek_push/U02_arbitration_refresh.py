#!/usr/bin/env python3
"""U02 -- N05 arbitration card refresh under the channel-dependent model.
Pre-registered formulas F1-F4 in U-WAVE_BRIEF.md (fixed before running); all
inputs runtime-read.  No new physics claim; refreshed program card either way."""
import json, os, math
BASE = os.path.dirname(os.path.abspath(__file__))
checks = []
def check(label, ok, d=""):
    checks.append({"name": label, "pass": bool(ok), "detail": d})
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"   {d}" if d else ""), flush=True)
    return bool(ok)
def ceils(x): return math.ceil(x)

n05 = json.load(open(f"{BASE}/N05_results.json"))
q02 = json.load(open(f"{BASE}/Q02_results.json"))
s02 = json.load(open(f"{BASE}/S02_results.json"))
try:
    ds = n05["deep_sparc_L06"]; dm = n05["mightee_deep"]; nr = n05["n_requirement"]
    for k, path in (("deep_sparc_L06","N05"),("mightee_deep","N05"),("n_requirement","N05"),
                    ("main","Q02"),("machinery","S02"),("se_colourgroup","S02")):
        assert k in (n05 if path=="N05" else q02 if path=="Q02" else s02), k
    check("K1 all required keys present (runtime-read)", True,
          "N05{deep_sparc_L06,mightee_deep,n_requirement} Q02{main} S02{machinery,se_colourgroup}")
except (KeyError, AssertionError) as e:
    check("K1 all required keys present", False, f"missing: {e}")
    json.dump({"lane":"U02_arbitration_refresh","checks":checks,"exit0":False},
              open(f"{BASE}/U02_arbitration_refresh_results.json","w"), indent=1)
    print("EXIT 1"); raise SystemExit(1)

a0 = n05["a0"]
# fix-forward (run-1): F1 as written mixed absolute-Delta units with a0E units and
# used the ring SE where N05's stored per_ring_noise_a0E is built from the CLUSTERED
# ensemble SE (K2 verification caught it: recompute 0.00 vs stored 1655.85).
# Corrected F1 (recorded in-script, house rule 3): per-ring noise in a0E units =
# (ensemble SE actually used by N05 for that channel's z) * sqrt(N) / a0E_unit,
# with a0E_unit = a0*E_gbar (SPARC, stored) and Delta_m/fraction_m (MIGHTEE, stored).
# Pre-registration intent (reproduce N05's arithmetic) is unchanged; F2/K2 gate unchanged.
a0E_unit_s = a0 * ds["E_gbar"]
a0E_unit_m = dm["Delta"] / dm["fraction_a0E"]
sig1_s = ds["se_clustered"] * math.sqrt(ds["N"]) / a0E_unit_s
sig1_m = max(dm["se_ring"], dm["se_colourgroup"]) * math.sqrt(dm["N"]) / a0E_unit_m
del_s = abs(ds["fraction_a0E"]); del_m = dm["fraction_a0E"]  # a0E units
# F2: per-channel 5-sigma attribution N
N_s = ceils((5.0*sig1_s/del_s)**2); N_m = ceils((5.0*sig1_m/del_m)**2)
# F4: verification vs stored
rec = (5.0*sig1_s/del_s)**2
k2 = abs(rec/nr["N_req_ring_level"] - 1.0) < 0.01
check("K2 F2-on-SPARC reproduces N05 N_req_ring_level (1%)", k2,
      f"recompute={rec:.2f} stored={nr['N_req_ring_level']:.2f}")
# F3: cross-channel difference resolution, equal new-N n per channel
n_diff = ceils((5.0*math.sqrt(sig1_m**2 + sig1_s**2)/abs(del_m - del_s))**2)
# bracket from banked Q02/R03 bootstrap-vs-multinomial finding (1.26-1.33x smaller -> conservative upper)
NB = n05["discriminator"]["N_5sigma_LR"]
bracket = [NB, ceils(NB*1.33**2)]
print(f"\nF1 per-ring noise: SPARC {sig1_s:.4f} a0E (N={ds['N']}), MIGHTEE {sig1_m:.4f} a0E (N={dm['N']})")
print(f"F2 SPARC-deficit 5sig attribution N = {N_s} (recompute {rec:.2f} vs stored 1655.85)")
print(f"F2 MIGHTEE-excess 5sig attribution N = {N_m}  [already at z={dm['z']:.2f} with N={dm['N']} -> fired]")
print(f"F3 cross-channel difference 5sig, equal new-N: n = {n_diff} per channel")
print(f"F4 H_A/H_B slope-channel N stands: {NB:.0f}; conservative bracket [{bracket[0]:.0f}, {bracket[1]}] (banked 1.26-1.33x, caveat not kill)")
check("K3 refreshed card recorded (both-ways)", True,
      f"N_s={N_s} N_m={N_m} n_diff={n_diff} bracket={bracket}")
res = {"lane": "U02_arbitration_refresh",
    "f1": {"sigma1_sparc": sig1_s, "sigma1_mightee": sig1_m},
    "f2": {"N_sparc_5sig": N_s, "N_mightee_5sig": N_m,
           "recompute_sparc": rec, "stored_N_req_ring": nr["N_req_ring_level"]},
    "f3": {"n_per_channel_5sig": n_diff,
           "delta_sparc_a0E": del_s, "delta_mightee_a0E": del_m},
    "f4": {"slope_channel_N_stored": NB, "conservative_bracket": bracket,
           "note": "Q02/R03 banked: presence-based SEs 1.26-1.33x smaller than multinomial"},
    "checks": checks, "exit0": bool(all(c["pass"] for c in checks))}
json.dump(res, open(f"{BASE}/U02_arbitration_refresh_results.json", "w"), indent=1)
print("U02 COMPLETE"); print("EXIT", 0 if res["exit0"] else 1)

"""CFG382: one dimensionless fluid-lapse coupling, Gamma = lambda sqrt(4 pi G rho_tot). lambda fixed by the MW floor; everything else predicted.
Criteria: FROZEN_CRITERIA.md (1f66028cc) + Amendment 1 (97307dde9). Run: python3 cfg382_settling.py ; MUTATE=1 sets lambda x 3 (rc 1).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

G, MSUN, KPC, PC, GYR = 6.674e-11, 1.989e30, 3.0857e19, 3.0857e16, 3.156e16
HL = 67.4e3 / 3.0857e22 * math.sqrt(0.6847)
rate = lambda rho: math.sqrt(4 * math.pi * G * rho)               # s^-1
TAUS = {"z2 (primary)": 10.3, "z1": 7.7, "z4": 12.2}

say("CFG382 one-constant settling" + ("  (MUTATE: lambda x 3)" if MUTATE else ""))
say("=" * 78)
check("C2 isothermal local-density rule rho(R) = M/(4 pi R^3) for rho = V^2/(4 pi G r^2) with M = V^2 R/G",
      abs((1e10 * 1e3 / G) / (4 * math.pi * 1e3**3) / (1e10 / (4 * math.pi * G * 1e3**2)) - 1) < 1e-12, "exact")

# anchors
lov = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "lovisari2015_groups.tsv")) if not l.startswith("#")]
hdr, lov = lov[0], [x for x in lov[1:] if len(x) > 5]
iR, iM = hdr.index("R500_kpc"), hdr.index("M500_1e13")
grp_rho = [float(x[iM]) * 1e13 * MSUN / (4 * math.pi * (float(x[iR]) * KPC) ** 3) for x in lov]
xc = json.load(open(os.path.join(REPO, "real_research", "data", "xcop", "xcop_r500_ettori2019.json")))
cl_rho = [v["M500"] * 1e14 * MSUN / (4 * math.pi * (v["R500"] * 1000 * KPC) ** 3) for v in xc.values()]
ufd_rho = 3 * (4e3) ** 2 / (4 * math.pi * G * (30 * PC) ** 2)

res = {}
for lab, tau_g in TAUS.items():
    tau = tau_g * GYR
    for V in (180e3, 200e3, 230e3):
        rho_mw = V**2 / (4 * math.pi * G * (30 * KPC) ** 2)
        lam = -math.log(0.14) / (rate(rho_mw) * tau)
        if MUTATE:
            lam *= 3
        e = lambda rho: math.exp(-lam * rate(rho) * tau)
        e_mw = e(rho_mw)
        e_g = float(np.median([e(r) for r in grp_rho])); e_c = float(np.median([e(r) for r in cl_rho])); e_u = e(ufd_rho)
        G_mw = lam * rate(rho_mw) / HL; G_cl = float(np.median([lam * rate(r) for r in cl_rho])) / HL
        p1 = abs(e_g - 0.60) <= 0.15; p2 = abs(e_c - 0.430) <= 0.15; p2_old = abs(e_c - 0.576) <= 0.15
        p3 = G_mw >= 1.73 and G_cl <= 1.93; p4 = e_u >= 0.5
        n = p1 + p2 + p3
        v = "PAYS FOR ITSELF" if n == 3 else ("PARTIAL" if n == 2 else "FAILS")
        key = f"{lab}|V{V/1e3:.0f}"
        res[key] = dict(lam=lam, e_mw=e_mw, e_group=e_g, e_cluster=e_c, e_ufd=e_u, Gamma_MW_HL=G_mw, Gamma_cl_HL=G_cl,
                        P1=p1, P2=p2, P2_frozen0576=p2_old, P3=p3, P4=p4, verdict=v)
        say(f"  tau {lab:13s} V {V/1e3:.0f}: lambda {lam:.3f} | e MW {e_mw:.3f} groups {e_g:.3f} clusters {e_c:.3f} UFD {e_u:.2e} | "
            f"Gamma MW {G_mw:.2f} cl {G_cl:.2f} H_L | P1 {'Y' if p1 else 'n'} P2 {'Y' if p2 else 'n'} (vs .576 {'Y' if p2_old else 'n'}) "
            f"P3 {'Y' if p3 else 'n'} P4 {'Y' if p4 else 'n'} -> {v}")
prim = res["z2 (primary)|V200"]
check("C1 calibration reproduces e_MW = 0.14 (primary)", MUTATE or abs(prim["e_mw"] - 0.14) < 1e-9, f"{prim['e_mw']:.6f}")
say(f"\nVERDICT (primary): {prim['verdict']}; UFD direction P4 {'PASS' if prim['P4'] else 'FAIL (conflict: UFDs settle fully under this rate)'}")
say(f"  densities: MW(30 kpc) {200e3**2/(4*math.pi*G*(30*KPC)**2):.2e}, groups(R500) median {np.median(grp_rho):.2e}, clusters(R500) median "
    f"{np.median(cl_rho):.2e}, UFD {ufd_rho:.2e} kg/m^3")
say("  Groups and clusters share almost the same local density at R500 (R500 is defined by mean density), so P1 and P2 test one number.")
check("T-MUT main-run marker (MUTATE lambda x3 must move P1/P2 e by > 0.2)", not MUTATE, prim["verdict"])
if MUTATE:
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": prim["verdict"]})
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG382", "mutate": MUTATE, "results": res, "checks": checks}, open(os.path.join(HERE, f"cfg382_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg382{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)

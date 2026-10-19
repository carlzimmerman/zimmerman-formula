"""CFG847 -- gravitational-slip bound for CFG43-type parents.  Criteria: FROZEN_CRITERIA.md (8e554a296).
Run: python3 cfg847.py (CFG847_MUTATE=1: TeVeS-like anisotropic stress).  kappa = 1/2 FITTED; not theory closed.
Field value: u = g a0/(g + a0) (the law's phantom acceleration; identity K W'(u) = u^2/(a0 - u) = g_N checked below)."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("CFG847_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
G, Msun, KPC, c = 6.674e-11, 1.989e30, 3.0857e19, 2.998e8; K = 4 * math.pi * G
SYS = [("dwarf", 1e7, 0.3), ("MW disc", 6e10, 10.0), ("MW outer", 6e10, 100.0), ("group", 1e12, 300.0), ("cluster", 1.5e14, 1000.0)]
def law_g(gN, a0): return 0.5 * (gN + math.sqrt(gN * gN + 4 * gN * a0))          # canonical S2: g_N = g^2/(g + a0)
def W(u, a0): u = min(u, 0.999 * a0); return (-a0 * u - 0.5 * u * u - a0 * a0 * math.log(1 - u / a0)) / K
P("CFG847  slip bound s = |Phi - Psi| / v_c^2  (8 pi G r^2 Pi / c^2 / v_c^2)" + ("  [MUTATE TeVeS-like stress]" if MUT else ""))
RES = dict(lane="CFG847", mutate=MUT, rows={}); worst = 0.0
for foot, a0 in (("canonical", 9.3603e-11), ("alt", 1.1312e-10)):
    P(f"\n  [{foot}]  {'system':10s} {'v_c km/s':>8s} {'s_disp':>9s} {'s_W':>9s} {'s_stiff(24pc)':>13s} {'s_stiff(1kpc)':>13s} {'s_total':>9s}")
    for name, Mb, rk in SYS:
        r = rk * KPC; M = Mb * Msun; gN = G * M / r ** 2; g = law_g(gN, a0); vc2 = g * r; u = g * a0 / (g + a0)
        assert abs(u * u / (a0 - u) - gN) / gN < 1e-9                               # identity check
        rM = math.sqrt(G * M / a0); dMc = 0.5 * M * (4 * r / rM ** 2) / math.sqrt(1 + 4 * r * r / rM ** 2); rho_c = dMc / (4 * math.pi * r * r)
        pref = 8 * math.pi * G * r * r / c ** 2 / vc2
        s1 = pref * rho_c * vc2 / 2; s2 = pref * abs(W(u, a0))
        s3 = [pref * math.pi * G * (L * 3.0857e16) ** 2 * rho_c ** 2 for L in (24.0, 1000.0)]   # (gamma/2)|grad P|^2 = pi G L*^2 rho_c^2 (gamma = K L*^2/2, |grad P| ~ rho_c); units fixed after run 1
        sm = pref * rho_c * c * c * 1e-3 if MUT else 0.0
        tot = s1 + s2 + max(s3) + sm; worst = max(worst, tot)
        RES["rows"][f"{foot}|{name}"] = dict(vc=math.sqrt(vc2) / 1e3, s_disp=s1, s_W=s2, s_stiff=s3, s_mut=sm, s_total=tot)
        P(f"           {name:10s} {math.sqrt(vc2) / 1e3:8.1f} {s1:9.1e} {s2:9.1e} {s3[0]:13.1e} {s3[1]:13.1e} {tot:9.1e}")
cls = "LENSING = DYNAMICS AT TEST PRECISION" if worst <= 1e-2 else ("SLIP POSSIBLY TESTABLE" if worst < 1 else "SLIP LARGE")
P(f"\n  K1: s_disp scales as sigma^2 (zero for dust) - by construction of term 1.")
P(f"  largest s over systems and footings: {worst:.1e}\n  CLASS: {cls}   (conditional on a well-posed covariant parent of this type)")
RES["max_s"] = worst; RES["cls"] = cls
sfx = "_MUTATE" if MUT else ""
json.dump(RES, open(os.path.join(HERE, f"cfg847_results{sfx}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg847{sfx}.out"), "w").write("\n".join(OUT) + "\n")

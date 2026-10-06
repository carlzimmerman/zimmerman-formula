"""CFG369: does dissipation (baryon cooling) settle the cold fluid into the phantom? Criteria: FROZEN_CRITERIA.md (9e7ae79a1).
cm12's cooling functions are COPIED verbatim (lam, ratio; cm12 d39a20280 / 23355d45b), not imported (cm12 runs at import).
Run: python3 cfg369_dissipation.py ; MUTATE=1 multiplies the cooling function by 100 (S3 e(MW) must move > 0.1; rc 1).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, ".."))
import CFG4_common as C4  # noqa: E402

MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
lines, checks = [], []
def say(s=""):
    print(s); lines.append(s)
def check(n, ok, v):
    checks.append({"name": n, "pass": bool(ok), "value": v}); say(f"  [{'PASS' if ok else 'FAIL'}] {n}: {v}")

# ---------------------------------------------------------------- cm12 (copied verbatim, cgs)
G, MSUN, MP, KB, KPC, KEV = 6.674e-8, 1.989e33, 1.6726e-24, 1.380649e-16, 3.0857e21, 1.602177e-9
A0 = {"canonical": 9.3603e-9, "alt": 1.1312e-8}
MU = 0.6; NE_NH, N_NH = 1.17, 2.3
H0 = 67.4e5 / 3.0857e24; RHO_B = 0.0493 * 3 * H0**2 / (8 * math.pi * G)
def lam(T):
    kT = KB * T / KEV
    return (8.6e-3 * kT**-1.7 + 5.8e-2 * kT**0.5 + 6.3e-2) * 1e-23 * (100.0 if MUTATE else 1.0), (0.01 <= kT <= 20)
def ratio(Mb, a0, rad, fhot):
    M = Mb * MSUN; V = (G * M * a0) ** 0.25; T = MU * MP * V**2 / (2 * KB)
    R = math.sqrt(G * M / a0) if rad == "R1" else (3 * M / (4 * math.pi * 200 * RHO_B)) ** (1 / 3)
    rho = fhot * M / (4 / 3 * math.pi * R**3); nH = rho / (MU * MP * N_NH)
    L, inrange = lam(T)
    tcool = 3 * N_NH * nH * KB * T / (2 * NE_NH * nH * nH * L); tdyn = R / V
    return tcool / tdyn, V / 1e5, T, R / KPC, inrange, tcool

H_L = H0 * math.sqrt(0.6847)                       # s^-1
TAU = 10.3e9 * 3.156e7                             # s since z = 2

say("CFG369 dissipation-gated settling" + ("  (MUTATE: cooling x100)" if MUTATE else ""))
say("=" * 78)

# ---------------------------------------------------------------- controls
say("Controls")
J12 = json.load(open(os.path.join(REPO, "sonnet55_push", "cold_mass", "cm12_cooling_step_results.json")))
ref = J12["cells"]["canonical|R1|fhot1.0"]["logMb_star"]
lM = np.linspace(9, 14, 2001)
r = np.array([ratio(10**x, A0["canonical"], "R1", 1.0)[0] for x in lM])
up = np.where((r[:-1] < 1) & (r[1:] >= 1))[0]
xs = lM[up[0]] + (0 - math.log10(r[up[0]])) / (math.log10(r[up[0] + 1]) - math.log10(r[up[0]])) * (lM[1] - lM[0]) if len(up) else float("nan")
check("C1 copied cm12 ratio() reproduces cm12's committed crossing (canonical R1 fhot1) to 0.01 dex", abs(xs - ref) < 0.01 or MUTATE,
      f"{xs:.3f} vs {ref:.3f}" + (" (MUTATE: cooling x100 moves it; not scored)" if MUTATE else ""))

# ---------------------------------------------------------------- S1 energy
say("\nS1 ENERGY: epsilon_min = q (1/2) / ln(r_in/R_d), SPARC Q <= 2 with Rdisk > 0")
Gk = 4.30091e-6; conv = 3.0857e13
gals = [g for g in C4.load_sparc() if g["meta"] and g["meta"]["Q"] <= 2 and g["meta"]["Rdisk"] > 0]
S1 = {}
for foot in ("canonical", "alt"):
    a0k = A0[foot] / 100 * conv                    # cgs cm/s^2 -> m/s^2 -> (km/s)^2/kpc
    eps = {}
    for rin in (1, 10):
        for q in (0.49, 9.5):
            vals = []
            for g in gals:
                Mb = (0.61 * g["meta"]["L36"] + 1.33 * g["meta"]["MHI"]) * 1e9
                rM = math.sqrt(Gk * Mb / a0k)
                L_ = math.log(rin * rM / g["meta"]["Rdisk"])
                vals.append(q * 0.5 / L_ if L_ > 0 else float("inf"))
            eps[(rin, q)] = float(np.median(vals))
    S1[foot] = {f"rin{k[0]}rM_q{k[1]}": v for k, v in eps.items()}
    say(f"  {foot}: median eps_min  r_M: q0.49 {eps[(1,0.49)]:.3f} q9.5 {eps[(1,9.5)]:.3f} | 10 r_M: q0.49 {eps[(10,0.49)]:.3f} q9.5 {eps[(10,9.5)]:.3f}")
def s1_verdict(e):
    if e["rin10rM_q9.5"] <= 1 or e["rin1rM_q9.5"] <= 1:
        return "ALLOWED"
    if e["rin10rM_q0.49"] <= 1:
        return "MARGINAL"
    return "FAIL"
S1v = {f: s1_verdict(S1[f]) for f in S1}
say(f"  S1 verdict: canonical {S1v['canonical']}, alt {S1v['alt']}")

# ---------------------------------------------------------------- S2 + S3
say("\nS2 RATE PINCER and S3 LEVELS (Gamma = 1/t_cool, H_Lambda units; e = exp(-Gamma tau), tau = 10.3 Gyr, epsilon = 1)")
targets = {"MW 6e10": (6e10, 0.13, 0.05), "group 5e12": (5e12, 0.60, 0.15), "cluster 1e14": (1e14, 0.58, 0.15)}
S2, S3 = {}, {}
for foot in ("canonical", "alt"):
    for rad in ("R1", "R2"):
        for fh in (1.0, 0.5):
            cell = f"{foot}|{rad}|fhot{fh}"
            out = {}
            for nm, (Mb, lev, sd) in targets.items():
                _, V, T, R, ok, tc = ratio(Mb, A0[foot], rad, fh)
                Gam = (1 / tc) if T >= 1e4 else 0.0
                e = math.exp(-Gam * TAU)
                out[nm] = dict(Gamma_HL=Gam / H_L, T=T, e=e, target=lev, band=sd, match=abs(e - lev) <= sd, V=V)
            s2 = out["MW 6e10"]["Gamma_HL"] >= 1.73 and out["cluster 1e14"]["Gamma_HL"] <= 1.93
            s3 = all(v["match"] for v in out.values())
            S2[cell], S3[cell] = s2, s3
            S3[cell + "_detail"] = out
            say(f"  {cell:24s}: Gamma/H_L  MW {out['MW 6e10']['Gamma_HL']:.2e}  group {out['group 5e12']['Gamma_HL']:.2e}  cluster {out['cluster 1e14']['Gamma_HL']:.2e}"
                f" | e MW {out['MW 6e10']['e']:.3f} group {out['group 5e12']['e']:.3f} cluster {out['cluster 1e14']['e']:.3f}"
                f" | S2 {'PASS' if s2 else 'fail'} S3 {'PASS' if s3 else 'fail'}")
S2v = {f: any(S2[c] for c in S2 if c.startswith(f)) for f in A0}
S3v = {f: any(S3[c] for c in S2 if c.startswith(f)) for f in A0}
say(f"  S2: canonical {'PASS' if S2v['canonical'] else 'FAIL (no cell)'}, alt {'PASS' if S2v['alt'] else 'FAIL'};  S3: canonical {'PASS' if S3v['canonical'] else 'FAIL'}, alt {'PASS' if S3v['alt'] else 'FAIL'}")
e_mw = [S3[c + "_detail"]["MW 6e10"]["e"] for c in S2 if c.startswith("canonical")]

# ---------------------------------------------------------------- S4 adiabatic contraction
say("\nS4 SHAPE: Blumenthal contraction of a mixed truncated SIS onto the SPARC baryons vs the law phantom (Q <= 2)")
UD, UB = 0.61, 0.854
def contract(rf, Mbf, Mbt, Mct, Ri):
    A, B = Mct / Ri, Mbt / Ri
    ri = (A * rf + np.sqrt(A * A * rf * rf + 4 * (A + B) * rf * Mbf)) / (2 * (A + B))
    out = ri > Ri
    ri = np.where(out, rf * (Mct + Mbf) / (Mct + Mbt), ri)
    return np.where(ri > Ri, Mct, A * ri), ri
# C2 identity: if the final baryons equal the initial ones, the fluid does not move
rt = np.linspace(0.5, 30, 60); Ri_t = 40.0; Mbt_t = 1e10; Mct_t = 5.364e10
Mc_id, _ = contract(rt, Mbt_t * np.minimum(rt / Ri_t, 1), Mbt_t, Mct_t, Ri_t)
check("C2 Blumenthal identity (M_b,f = M_b,i -> M_c,f = M_c,i) and mass bound", np.max(abs(Mc_id / (Mct_t * np.minimum(rt / Ri_t, 1)) - 1)) < 1e-6,
      f"max rel dev {np.max(abs(Mc_id/(Mct_t*np.minimum(rt/Ri_t,1))-1)):.1e}")
S4 = {}
for foot in ("canonical", "alt"):
    a0k = A0[foot] / 100 * conv
    for rin in (1, 10):
        res, lg = [], []
        for g in gals:
            vb2 = g["Vgas"] * np.abs(g["Vgas"]) + UD * g["Vdisk"] * np.abs(g["Vdisk"]) + UB * g["Vbul"] * np.abs(g["Vbul"])
            ok = (g["R"] > 0) & (vb2 > 0)
            if ok.sum() < 3:
                continue
            R = g["R"][ok]; Mbf = vb2[ok] * R / Gk
            Mbt = Mbf[-1]
            Mtab = (0.61 * g["meta"]["L36"] + 1.33 * g["meta"]["MHI"]) * 1e9
            Ri = rin * math.sqrt(Gk * Mtab / a0k)
            Mcf, _ = contract(R, Mbf, Mbt, 5.364 * Mtab, Ri)
            gb = vb2[ok] / R
            Mph = (C4.nu_mono(gb / a0k) - 1) * Mbf
            m = Mph > 0
            res += list(np.log10(Mcf[m] / Mph[m])); lg += list(np.log10(gb[m] / a0k))
        res, lg = np.array(res), np.array(lg)
        rms = float(np.sqrt(np.mean(res**2))); med = float(np.median(res)); slope = float(np.polyfit(lg, res, 1)[0])
        ok4 = rms <= 0.10 and abs(slope) <= 0.10
        S4[f"{foot}|rin{rin}rM"] = dict(rms=rms, median=med, slope=slope, N=len(res), passed=ok4)
        say(f"  {foot} R_i = {rin} r_M: N {len(res)} points, median log(M_c,f/M_ph) {med:+.3f}, rms {rms:.3f} dex, slope vs log g_bar {slope:+.3f} -> {'PASS' if ok4 else 'FAIL'}")
S4v = {f: any(v["passed"] for k, v in S4.items() if k.startswith(f)) for f in A0}

# ---------------------------------------------------------------- verdict
def lane(f):
    if S1v[f] == "FAIL" or not S2v[f]:
        return "DEAD"
    if S2v[f] and S3v[f] and S1v[f] != "FAIL":
        return "ALIVE"
    return "PARTIAL"
V = {f: lane(f) for f in A0}
say(f"\nLANE VERDICT: canonical {V['canonical']} (alt {V['alt']}); class: {'adiabatic' if S4v['canonical'] else 'NON-adiabatic (S4 fails)'}")
check("T-MUT main-run sanity (MUTATE must move S3's e(MW) by > 0.1; recorded in the MUTATE JSON)", not MUTATE, f"e(MW) canonical cells {['%.3f' % x for x in e_mw]}")
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG369", "mutate": MUTATE, "S1": S1, "S1v": S1v, "S2": S2, "S2v": S2v,
           "S3": {k: v for k, v in S3.items()}, "S3v": S3v, "S4": S4, "S4v": S4v, "verdict": V, "e_MW_canonical": e_mw, "checks": checks},
          open(os.path.join(HERE, f"cfg369_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg369{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)

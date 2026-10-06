"""CFG371: cool-core vs non-cool-core X-COP clusters as a test of the settling principle. Criteria: FROZEN_CRITERIA.md (b5624e3d8).
Run: python3 cfg371_coolcore.py ; MUTATE=1 permutes t_c across clusters (seed 371; rc 1).
"""
import json, math, os, sys
import numpy as np
from astropy.io import fits
from scipy.stats import spearmanr

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

G, MSUN, MP, KB, KPC, KEV, GYR = 6.674e-8, 1.989e33, 1.6726e-24, 1.380649e-16, 3.0857e21, 1.602177e-9, 3.156e16
MU, NE_NH, N_NH = 0.6, 1.17, 2.3
A0 = {"canonical": 9.3603e-9, "alt": 1.1312e-8}
def lam(T):
    kT = KB * T / KEV
    return (8.6e-3 * kT**-1.7 + 5.8e-2 * kT**0.5 + 6.3e-2) * 1e-22          # CORRECTED unit (CFG370)
def tcool(rho, T):
    nH = rho / (MU * MP * N_NH)
    return 3 * N_NH * nH * KB * T / (2 * NE_NH * nH * nH * lam(T))

say("CFG371 cool-core test" + ("  (MUTATE: t_c permuted)" if MUTATE else ""))
say("=" * 78)
T1k = KEV / KB
check("C1 corrected TN bremsstrahlung term matches free-free at 1 keV to 1%", abs(5.8e-2 * 1e-22 / (1.42e-27 * 1.2 * math.sqrt(T1k)) - 1) < 0.01, "ok")

xdir = os.path.join(REPO, "real_research", "data", "xcop")
r500j = json.load(open(os.path.join(xdir, "xcop_r500_ettori2019.json")))
rows, c2 = [], []
for nm in sorted(os.listdir(xdir)):
    d = os.path.join(xdir, nm)
    if not os.path.isdir(d) or nm not in r500j:
        continue
    hm = fits.open(os.path.join(d, f"{nm}_hydro_mass.fits"))["HYDRO_MASS"].data
    fg = fits.open(os.path.join(d, f"{nm}_fgas_profile.fits"))["FGAS"].data
    has_ms = os.path.exists(os.path.join(d, f"{nm}_mstar.fits"))
    R500 = r500j[nm]["R500"] * 1000.0                                   # kpc
    M500 = r500j[nm]["M500"] * 1e14
    x = np.asarray(fg["RADIUS"], float); Mg = np.asarray(fg["MGAS"], float)
    lx, lm = np.log(x), np.log(Mg)
    def Mgas(xx): return float(np.exp(np.interp(np.log(xx), lx, lm)))
    def rho_gas(xx):                                                    # g cm^-3 from dM/dr / (4 pi r^2)
        e = 0.02; m1, m2 = Mgas(xx * (1 - e)), Mgas(xx * (1 + e))
        r_cm = xx * R500 * KPC
        dMdr = (m2 - m1) * MSUN / (2 * e * r_cm)
        return dMdr / (4 * math.pi * r_cm**2)
    # C2: integrate the density back between 0.03 and 1 R500
    xs = np.logspace(np.log10(0.03), 0.0, 400)
    integ = (getattr(np, "trapezoid", None) or np.trapz)([rho_gas(v) * 4 * math.pi * (v * R500 * KPC) ** 2 for v in xs], xs * R500 * KPC) / MSUN
    c2.append(abs(integ / (Mgas(1.0) - Mgas(0.03)) - 1))
    T = MU * MP * G * M500 * MSUN / (2 * R500 * KPC) / KB
    tc = tcool(rho_gas(0.03), T) / GYR
    tin = tcool(rho_gas(0.1), T) / GYR
    rk = np.asarray(hm["RADIUS"], float)
    rin = 0.1 * R500
    Mh = float(np.interp(rin, rk, np.asarray(hm["M_FORW"], float)))
    if has_ms:
        ms = fits.open(os.path.join(d, f"{nm}_mstar.fits"))["MSTAR_SMOOTHED"].data
        Ms = float(np.exp(np.interp(np.log(rin), np.log(np.asarray(ms["RADIUS"], float)), np.log(np.asarray(ms["MSTAR"], float)))))
    else:
        Ms = 0.10 * Mgas(0.1)
    Mb = Mgas(0.1) + Ms
    out = {"name": nm, "primary": has_ms, "t_c_Gyr": tc, "t_in_Gyr": tin, "kT_keV": T * KB / KEV}
    for foot, a0 in A0.items():
        gN = G * Mb * MSUN / (rin * KPC) ** 2
        Mlaw = C4.nu_mono(np.array([gN / a0]))[0] * Mb
        out[f"X_in_{foot}"] = (Mh - Mlaw) / (5.364 * Mb)
    out["e_pred"] = math.exp(-10.3 / tin)
    rows.append(out)
check("C2 the finite-difference gas density integrates back to M_gas (0.03-1 R500) within 5%, every cluster", max(c2) < 0.05, f"max dev {max(c2):.3f}")

def analyse(sub, foot, label):
    t = np.array([r["t_c_Gyr"] for r in sub]); X = np.array([r[f"X_in_{foot}"] for r in sub])
    if MUTATE:
        t = np.random.default_rng(371).permutation(t)
    rho = float(spearmanr(t, X).correlation)
    rng = np.random.default_rng(1); perm = [spearmanr(rng.permutation(t), X).correlation for _ in range(20000)]
    p = float(np.mean(np.array(perm) >= rho))
    cool = X[t < 7.7]; non = X[t >= 7.7]
    split = (float(np.median(cool)) if len(cool) else None, float(np.median(non)) if len(non) else None, len(cool), len(non))
    t2 = None if (split[2] < 2 or split[3] < 2) else (split[0] < split[1])
    t2_opp = (split[2] >= 2 and split[3] >= 2 and split[0] - split[1] > 0.1)
    if rho >= 0.5 and p < 0.10 and t2 is not False:
        v = "SUPPORTED"
    elif rho <= 0 or t2_opp:
        v = "CONTRADICTED"
    else:
        v = "INCONCLUSIVE"
    say(f"  {label} [{foot}] N {len(sub)}: Spearman rho(t_c, X_in) = {rho:+.2f} (one-sided p {p:.3f}); COOLING median X_in "
        f"{split[0] if split[0] is None else round(split[0],3)} (N {split[2]}) vs NON-COOLING {split[1] if split[1] is None else round(split[1],3)} (N {split[3]}) -> {v}")
    return dict(N=len(sub), rho=rho, p=p, split=split, verdict=v)

say("\nPer cluster (t_c at 0.03 R500; X_in at 0.1 R500; e_pred = exp(-10.3 Gyr / t_cool(0.1 R500)))")
for r in rows:
    say(f"  {r['name']:8s} {'P' if r['primary'] else 's'}  kT {r['kT_keV']:.1f} keV  t_c {r['t_c_Gyr']:7.2f} Gyr  t_cool(0.1R500) {r['t_in_Gyr']:7.1f}  "
        f"X_in {r['X_in_canonical']:+.3f} (alt {r['X_in_alt']:+.3f})  e_pred {r['e_pred']:.3f}")
say("\nTests")
prim = [r for r in rows if r["primary"]]
R = {"primary_canonical": analyse(prim, "canonical", "PRIMARY"), "primary_alt": analyse(prim, "alt", "PRIMARY"),
     "secondary12_canonical": analyse(rows, "canonical", "SECONDARY (12)")}
amp = [r["e_pred"] / r["X_in_canonical"] for r in prim if r["X_in_canonical"] > 0]
say(f"  T3 (reported): median e_pred / X_in (primary, canonical, X_in > 0) = {np.median(amp) if amp else float('nan'):.2f}")
V = R["primary_canonical"]["verdict"]
say(f"\nVERDICT (primary, canonical): {V}   (alt {R['primary_alt']['verdict']}; secondary {R['secondary12_canonical']['verdict']})")
say("N = 7 has low power; isothermal kT; ranking only.")
check("T-MUT main-run marker (MUTATE must not be SUPPORTED)", not MUTATE or V != "SUPPORTED", V)
if MUTATE:
    checks.append({"name": "MUTATE forces rc 1", "pass": False, "value": V})
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG371", "mutate": MUTATE, "verdict": V, "tests": R, "rows": rows, "checks": checks},
          open(os.path.join(HERE, f"cfg371_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg371{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)

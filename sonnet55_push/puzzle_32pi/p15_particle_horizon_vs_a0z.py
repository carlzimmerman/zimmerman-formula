"""p15: test the particle-horizon reading of A Lambda = 32 pi^2 (p14) against the a0(z) values already in the record.

Law PH (parameter-free): a0(z) = c^2 / (2 R_p(z)), R_p = proper particle horizon at the epoch (Planck 2018, as p14).
Compared in the record's units s* = a0 / 9.3603e-11 with FLAT (s* = 1) and the rival a0 ~ H(z) (s* = H/H0).
POST-HOC: the law was formed after the data were seen (p14, this session); no frozen criteria. Not a verdict on the framework.

Data (read from committed files, nothing re-fitted):
  primary  = CFG303 native (LCDM-free) RC100 sample-B quartiles + CRISTAL R_out primary   (2d9bdc1b9)
  secondary = the committed CFG223/228/229 chart points (LCDM-halo baryon inputs for RC100/CRISTAL)
  KiDS lens-z halves (CFG255): A = +0.060 +- 0.038 dex in g_obs (deep MOND: A = 0.5 dlog a0)
  extra bounds: CFG270 KMOS3D pooled PT1 s* <= 2.44 at z 2.228 (exists only with the hand-added pressure term)
Each record point is calibration-limited (lever -2.5 to -4.8 dex per dex of baryon mass); the 'bands' give s* for baryons
shifted by -0.3/-0.15/+0.15/+0.3 dex, used here for the shift that would put each native point on PH.

Run: python3 p15_particle_horizon_vs_a0z.py   |   MUTATE=1: PH replaced by FLAT (check A must fail)
"""
import csv, json, os, sys
import numpy as np
from scipy.integrate import quad

MUTATE = os.environ.get("MUTATE") == "1"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CFG = os.path.join(ROOT, "campaign_fresh_gravity")
c = 2.99792458e8; Mpc = 3.0857e22; A0 = 9.3603e-11
H0 = 67.66e3 / Mpc; Om = 0.3111; Or = 9.0e-5; OL = 1 - Om - Or
H = lambda a: H0 * np.sqrt(Or / a**4 + Om / a**3 + OL)
Rp = lambda z: quad(lambda x: c / (x * x * H(x)), 1e-12, 1 / (1 + z), limit=500)[0] / (1 + z)
PH = (lambda z: 1.0) if MUTATE else (lambda z: c * c / (2 * Rp(z)) / A0)
HZ = lambda z: H(1 / (1 + z)) / H0
res = []
def check(n, ok): res.append(bool(ok)); print(("PASS  " if ok else "FAIL  ") + n)
inn = lambda lo, hi, s: lo <= s <= hi

J = json.load(open(os.path.join(CFG, "CFG303_lcdm_free_inputs", "cfg303_rc100_cristal_LCDMFREE_results.json")))["points"]
prim = [("RC100 B " + q, J["RC100"]["B " + q]) for q in ("Q1", "Q2", "Q3", "Q4")]
prim.append(("CRISTAL R_out native", J["CRISTAL"]["R_out native, six, outermost data marker (primary)"]))
print(f"PH today: s* = {PH(0):.3f} (a0 = {PH(0)*A0:.3g})\n")
print("PRIMARY (native baryons): 95% interval vs each law; shift = baryon change (dex) that would put the point on PH")
print(f"{'point':22s} {'z':>5s} {'s*':>6s} {'95%':>15s} {'PH':>6s} {'H(z)':>6s}  in95: FLAT  H(z)  PH   shift")
nprim = {"FLAT": 0, "H(z)": 0, "PH": 0}
for name, p in prim:
    z = p["z_med"]; s = p["s"]; lo, hi = p["lo95"], p["hi95"]; sp_, sh = PH(z), HZ(z)
    f = {"FLAT": inn(lo, hi, 1.0), "H(z)": inn(lo, hi, sh), "PH": inn(lo, hi, sp_)}
    for k in f: nprim[k] += f[k]
    shift = "n/a"
    if "bands" in p and not p.get("unbounded"):
        offs = [-0.3, -0.15, 0.0, 0.15]; ss = [p["bands"]["-0.3"], p["bands"]["-0.15"], s, p["bands"]["0.15"]]
        shift = ("beyond -0.30 (band edge)" if sp_ > ss[0] else
                 f"{np.interp(np.log10(sp_), np.log10(ss[::-1]), offs[::-1]):+.2f}")
    sd = "no root" if p.get("unbounded") else f"{s:6.3f}"
    print(f"{name:22s} {z:5.2f} {sd:>6s} [{lo:6.3f},{hi:6.3f}] {sp_:6.2f} {sh:6.2f}  {str(f['FLAT']):5s} {str(f['H(z)']):5s} {str(f['PH']):5s} {shift}")
# the record's own pull method (log10 difference over sd_log) reproduces the stored H(z) pull
q1 = J["RC100"]["B Q1"]
check("0 method: our log10 pull reproduces the stored H(z) pull of RC100 B Q1",
      abs((np.log10(q1["s"]) - np.log10(HZ(q1["z_med"]))) / q1["sd_log"] - q1["expected"]["H(z)"]["pull"]) < 0.02)

print("\nSECONDARY (committed chart points, LCDM-halo baryons where noted in the record)")
sec = {"FLAT": 0, "H(z)": 0, "PH": 0}; nsec = 0
for r in csv.DictReader(open(os.path.join(CFG, "CHART_a0z_combined_2026-09-30", "chart_a0z_points.csv"))):
    if r["no_root"] == "1": continue
    z = float(r["z"]); s = float(r["s_star"]); lo, hi = float(r["stat95_lo"]), float(r["stat95_hi"]); nsec += 1
    f = {"FLAT": inn(lo, hi, 1.0), "H(z)": inn(lo, hi, HZ(z)), "PH": inn(lo, hi, PH(z))}
    for k in f: sec[k] += f[k]
    print(f"{r['object']:22s} {z:5.2f} {s:6.2f} [{lo:6.2f},{hi:7.2f}] PH {PH(z):6.2f}  in95: FLAT {f['FLAT']!s:5s} H(z) {f['H(z)']!s:5s} PH {f['PH']!s:5s}")
print(f"secondary counts inside 95% (of {nsec}): {sec}")

kA, kS = 0.059475, 0.038339
aPH = 0.5 * np.log10(PH(0.372) / PH(0.236)); aH = 0.5 * np.log10(HZ(0.372) / HZ(0.236))
print(f"\nKiDS halves (z 0.236/0.372): data A {kA:+.3f} +- {kS:.3f}; PH {aPH:+.3f} ({(kA-aPH)/kS:+.1f} sig), H(z) {aH:+.3f} ({(kA-aH)/kS:+.1f}), FLAT +0.000 ({kA/kS:+.1f})")
print(f"KMOS3D PT1 bound s* <= 2.44 at z 2.228: PH {PH(2.228):.2f}, H(z) {HZ(2.228):.2f}")

print()
check(f"A primary (native) points: PH inside the 95% interval for {nprim['PH']} of 5, FLAT {nprim['FLAT']}, H(z) {nprim['H(z)']}; PH fails at least 3",
      5 - nprim["PH"] >= 3)
check(f"B secondary points: PH inside 95% for {sec['PH']} of {nsec} vs FLAT {sec['FLAT']} (PH fewer than FLAT)", sec["PH"] < sec["FLAT"])
check("C KiDS halves cannot tell PH from FLAT (both within 2 sigma)", abs((kA - aPH) / kS) < 2 and abs(kA / kS) < 2)
check("D PH sits above the KMOS3D PT1 bound and above H(z) everywhere z>0", PH(2.228) > 2.44 and all(PH(z) > HZ(z) for z in (0.5, 1, 2, 3, 5)))
print(f"\n{sum(res)}/{len(res)} pass" + ("  (MUTATE)" if MUTATE else ""))
sys.exit(0 if all(res) else 1)

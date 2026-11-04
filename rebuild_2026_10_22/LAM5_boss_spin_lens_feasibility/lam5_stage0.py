"""LAM5 stage 0 (criteria a5617b4742): aggregate counts of BOSS galaxy spectra by S/N, fibre coverage c = 1"/R_e and
gas-poor flag, from SkyServer DR17 in 10-degree RA strips. No spectra downloaded. Run: python3 -I lam5_stage0.py.
kappa = 1/2 FITTED; not theory closed."""
import os, json, time, urllib.parse, urllib.request, collections
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = []
URL = "https://skyserver.sdss.org/dr17/SkyServerWS/SearchTools/SqlSearch"
def P(s=""): print(s, flush=True); OUT.append(s)
Q = """SELECT sn, cb, gp, COUNT(*) AS n FROM (SELECT
 CASE WHEN s.snMedian >= 20 THEN 2 WHEN s.snMedian >= 10 THEN 1 ELSE 0 END AS sn,
 CASE WHEN p.deVRad_r <= 0 OR p.deVAB_r <= 0 THEN -1
      WHEN 1.0 / (p.deVRad_r * SQRT(p.deVAB_r)) >= 1.0 THEN 3
      WHEN 1.0 / (p.deVRad_r * SQRT(p.deVAB_r)) >= 0.5 THEN 2
      WHEN 1.0 / (p.deVRad_r * SQRT(p.deVAB_r)) >= 0.3 THEN 1 ELSE 0 END AS cb,
 CASE WHEN e.specObjID IS NULL THEN -1 WHEN e.EW_Ha_6562 < 3 THEN 1 ELSE 0 END AS gp
 FROM SpecObj s JOIN PhotoObj p ON p.objID = s.bestObjID LEFT JOIN emissionLinesPort e ON e.specObjID = s.specObjID
 WHERE s.class = 'GALAXY' AND s.zWarning = 0 AND s.instrument = 'BOSS' AND s.z BETWEEN 0.15 AND 0.55
   AND s.velDisp >= 100 AND s.velDispErr < 0.1 * s.velDisp AND s.ra >= {lo} AND s.ra < {hi}) t GROUP BY sn, cb, gp"""
C = collections.Counter()
for lo in range(0, 360, 10):
    for t in range(4):
        try:
            b = urllib.request.urlopen(URL + "?" + urllib.parse.urlencode({"cmd": Q.format(lo=lo, hi=lo + 10), "format": "csv"}), timeout=600).read().decode()
            rows = [l.split(",") for l in b.strip().splitlines()[2:] if l]
            for sn, cb, gp, n in rows: C[(int(sn), int(cb), int(gp))] += int(n)
            break
        except Exception as e: print(f"  strip {lo} try {t}: {e}", flush=True); time.sleep(10 * (t + 1))
    else: raise SystemExit(f"strip {lo} failed")
cnt = lambda sn, cmin, gp=(1,): sum(n for (a, c, g), n in C.items() if a >= sn and c >= cmin and g in gp)
P(f"BOSS galaxies 0.15 <= z <= 0.55, zWarning 0, velDisp >= 100, err < 10 %: {sum(C.values())}")
P(f"  no Portsmouth match: {sum(n for k, n in C.items() if k[2] == -1)}; bad R_e: {sum(n for k, n in C.items() if k[1] == -1)}")
for sn, nm in ((2, "S/N >= 20"), (1, "S/N >= 10"), (0, "any S/N")):
    P(f"  {nm}: all {sum(n for k, n in C.items() if k[0] >= sn)}, gas-poor {cnt(sn, 0)}, gas-poor c >= 0.3 {cnt(sn, 1)}, c >= 0.5 {cnt(sn, 2)}, c >= 1.0 {cnt(sn, 3)}")
N = cnt(2, 2); f1 = N >= 42000
P(f"F1 gas-poor, S/N >= 20, c >= 0.5: N {N} (>= 42,000): {'PASS' if f1 else 'FAIL'}")
lab = "STAGE 0 PASS" if f1 else "NOT FEASIBLE"; P(f"LABEL: {lab}")
open(os.path.join(HERE, "lam5_stage0.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(lane="LAM5", stage=0, counts={str(k): v for k, v in sorted(C.items())}, F1=dict(n=N, pass_=bool(f1)), label=lab),
          open(os.path.join(HERE, "lam5_stage0.json"), "w"), indent=1)

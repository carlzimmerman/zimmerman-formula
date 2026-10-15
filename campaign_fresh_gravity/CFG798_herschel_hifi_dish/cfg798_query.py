"""CFG798 -- query the public ESA Herschel Science Archive (TAP) for HIFI observations covering 541.7 / 595.5 GHz.
Criteria: FROZEN_CRITERIA.md.  Network: one small TAP query (metadata only, no spectra).  Python stdlib only.
Run: python3 cfg798_query.py  -> cfg798_matches.csv, cfg798_query.out
Notes: HSA 'duration' is in MILLISECONDS (checked against start/end times: 1342250735 1.942e7 -> 5.39 h).
Coverage: target in archive LSB/USB sky range, or 4<=|nu-LO|<=8 GHz, or (spectral scans) LO range overlapping
[nu-8,nu-4] U [nu+4,nu+8].  Spectral-scan time fraction at the target = overlap / LO span (accounting, see README).
Tier A = FSwitch / LoadChop WITHOUT sky reference ('noRef'); Tier B = everything else (frozen switching rule).
"""
import csv, io, os, urllib.parse, urllib.request
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TAP = "https://archives.esac.esa.int/hsa/whsa-tap-server/tap/sync"
Q = ("select o.observation_id, o.target_name, o.duration, o.is_public, o.obsstate, o.start_time, o.proposal_id, "
     "m.band, m.lofreq, m.lofrqmin, m.lofrqmax, m.lfreqmin, m.lfreqmax, m.ufreqmin, m.ufreqmax, m.obs_mode, "
     "om.observing_mode_name, m.vframe, m.freq_thr from hsa.metadata_expert_panels m "
     "join hsa.v_active_observation o on o.observation_oid=m.observation_oid "
     "join hsa.observing_mode om on om.observing_mode_oid=m.observing_mode_oid where m.band in ('1a','1b')")
TARGETS = {"541.7": 541.7, "595.5": 595.5}
OUT = []


def P(s=""):
    print(s, flush=True); OUT.append(str(s))


def fl(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


data = urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=Q)).encode()
txt = urllib.request.urlopen(urllib.request.Request(TAP, data=data), timeout=300).read().decode()
rows = list(csv.DictReader(io.StringIO(txt)))
P(f"CFG798 HSA query: {len(rows)} active HIFI band-1a/1b observations")


def coverage(r, nu):
    """time fraction of the observation with nu in a sideband (0 = not covered)."""
    l1, l2 = fl(r["lofrqmin"]), fl(r["lofrqmax"])
    if l1 is not None and l2 is not None and l2 - l1 > 1.0:          # spectral scan
        ov = sum(max(0.0, min(l2, b) - max(l1, a)) for a, b in ((nu - 8, nu - 4), (nu + 4, nu + 8)))
        return ov / (l2 - l1)
    for a, b in (("lfreqmin", "lfreqmax"), ("ufreqmin", "ufreqmax")):
        if fl(r[a]) is not None and fl(r[b]) is not None and fl(r[a]) <= nu <= fl(r[b]):
            return 1.0
    lo = fl(r["lofreq"])
    return 1.0 if lo is not None and 4.0 <= abs(nu - lo) <= 8.0 else 0.0


def tier(r):
    s = (r["obs_mode"] + " " + r["observing_mode_name"]).lower()
    return "A" if ("noref" in s and ("fswitch" in s or "frequency switch" in s or "loadchop" in s or "load chop" in s)) else "B"


matches = []
for key, nu in TARGETS.items():
    for r in rows:
        f = coverage(r, nu)
        if f <= 0 or r["is_public"] != "true" or "Eng" in r["observing_mode_name"]:
            continue
        dur_h = float(r["duration"]) / 3.6e6
        matches.append(dict(target_GHz=key, observation_id=r["observation_id"], target_name=r["target_name"],
                            band=r["band"], mode=r["observing_mode_name"], obs_mode=r["obs_mode"], tier=tier(r),
                            lofreq=r["lofreq"], lofrqmin=r["lofrqmin"], lofrqmax=r["lofrqmax"],
                            start_time=r["start_time"], duration_h=round(dur_h, 4), cover_frac=round(f, 4),
                            t_int_h=round(0.5 * dur_h * f, 4)))
cols = list(matches[0].keys())
with open(os.path.join(HERE, "cfg798_matches.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(matches)

for key in TARGETS:
    m = [x for x in matches if x["target_GHz"] == key]
    P(f"\n  {key} GHz: {len(m)} public science observations cover it")
    agg = defaultdict(lambda: [0, 0.0, 0.0])
    for x in m:
        a = agg[(x["tier"], x["mode"])]; a[0] += 1; a[1] += x["duration_h"]; a[2] += x["t_int_h"]
    for (t, mode), (n, d, ti) in sorted(agg.items()):
        P(f"    tier {t}  {mode:30s} n={n:3d}  archive {d:7.2f} h  integration-at-target {ti:7.2f} h")
    for t in "AB":
        P(f"    TIER {t} total integration at {key} GHz: {sum(x['t_int_h'] for x in m if x['tier'] == t):.2f} h "
          f"({sum(1 for x in m if x['tier'] == t)} obs)")

# report only (frozen): the +-1% window (nu ∝ sqrt(a0)); any sideband/LO-window overlap, archive hours
P("\n  REPORT ONLY: +-1% window (a scan, not the verdict)")
for key, nu in TARGETS.items():
    lo_w, hi_w = 0.99 * nu, 1.01 * nu
    n, d = 0, 0.0
    for r in rows:
        if r["is_public"] != "true" or "Eng" in r["observing_mode_name"]:
            continue
        hit = False
        for a, b in (("lfreqmin", "lfreqmax"), ("ufreqmin", "ufreqmax")):
            if fl(r[a]) is not None and fl(r[b]) is not None and fl(r[a]) <= hi_w and fl(r[b]) >= lo_w:
                hit = True
        if hit:
            n += 1; d += float(r["duration"]) / 3.6e6
    P(f"    {key} GHz window [{lo_w:.1f}, {hi_w:.1f}]: {n} public obs touch it, archive {d:.1f} h (no coverage fraction)")
open(os.path.join(HERE, "cfg798_query.out"), "w").write("\n".join(OUT) + "\n")

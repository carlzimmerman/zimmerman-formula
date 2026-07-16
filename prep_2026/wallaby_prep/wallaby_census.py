#!/usr/bin/env python3
"""
WALLABY PUBLIC-RELEASE CENSUS + PER-SIDE CAPACITY STATEMENT (Door 5 prep)
=========================================================================
Counts, LIVE from the CADC CAOM2 TAP service (anonymous, public), what the
WALLABY pilot releases actually contain today:
  (a) sources with a SoFiA moment-1 velocity field (_mom1.fits)  -> per-side
      extraction possible IF a tilted-ring geometry exists,
  (b) galaxies with a released WKAPP kinematic model (_AvgMod.txt geometry),
  (c) the overlap = galaxies per-side-capable RIGHT NOW with released
      geometries (perside_extractor.py consumes exactly these two products).

Compares against the banked directional-EFE sample-size requirements
(zimmerman-formula/real_research/reviews/directional_efe_2026/confrontation.out):
  N ~ 1,157  (canonical a0 = 9.36e-11, max-clustering e_N, AQUAL-vs-BranchB w=0.304)
  N ~ 1,424  (alt a0 = 1.13e-10, max-clustering e_N)     [both footings carried]
  N ~ 192-3,057 for the AQUAL-amplitude band (laneB_FEASIBILITY.md)
and the full-survey projection printed in Deg et al. 2022 (PASA 39, e059,
Discussion): ~20% WKAPP modelling success on PDR1 -> ~40,000 kinematic models
projected over the full ~210,000-detection survey, "likely higher than 10%"
(>= ~21,000) as the conservative floor.

Falls back to the cached CSV (census_cache.json, written on every live run)
if the TAP service is unreachable, and says so.  exit 0 either way.
"""
import json, os, re, sys, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "census_cache.json")
TAP = "https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/argus/sync"

Q_ARTIFACTS = """
SELECT Artifact.uri FROM caom2.Artifact AS Artifact
JOIN caom2.Plane AS Plane ON Artifact.planeID=Plane.planeID
JOIN caom2.Observation AS Observation ON Plane.obsID=Observation.obsID
WHERE Observation.collection='WALLABY'
AND (Artifact.uri LIKE '%AvgMod.txt' OR Artifact.uri LIKE '%mom1.fits')
"""

JRE = re.compile(r"(J\d{6}[+-]\d{6})")


def tap_query(adql):
    url = TAP + "?" + urllib.parse.urlencode(
        {"LANG": "ADQL", "FORMAT": "csv", "QUERY": " ".join(adql.split())})
    with urllib.request.urlopen(url, timeout=180) as r:
        return r.read().decode()


def main():
    live = True
    try:
        csv_txt = tap_query(Q_ARTIFACTS)
        rows = [l for l in csv_txt.splitlines()[1:] if l.strip()]
        cache = {"source": "LIVE CADC TAP", "uris": rows}
        with open(CACHE, "w") as f:
            json.dump(cache, f)
    except Exception as e:
        live = False
        if not os.path.exists(CACHE):
            print(f"TAP unreachable ({e}) and no cache -> cannot census. "
                  f"Re-run with network.")
            return 0
        cache = json.load(open(CACHE))
        rows = cache["uris"]
        print(f"[warn] TAP unreachable ({e}); using cached census "
              f"(source={cache['source']})")

    kin, mom = set(), set()
    for uri in rows:
        m = JRE.search(uri)
        if not m:
            continue
        (kin if uri.endswith("AvgMod.txt") else mom).add(m.group(1))
    both = kin & mom

    print("=" * 76)
    print("WALLABY PUBLIC RELEASES -- what exists NOW (%s)" %
          ("live CADC query" if live else "cached"))
    print("=" * 76)
    print("""
  Releases (documented 2026-07-16):
   - Pilot DR1 (2022-11-15): ~600 HI sources, 3 fields (Hydra, Norma, NGC 4636)
       + WKAPP kinematic models for 109/592 detections (Deg+2022, PASA 39 e059,
       arXiv:2211.07333).  Products per modelled source (Deg+22 Table 3):
       _AvgMod.txt geometry+RC, _ModRotCurve/_ModSurfDens/_ModGeometry.fits,
       _ProcData/_ModCube/_DiffCube/_FullRes*.fits cubelets, _DiagnosticPlot.png.
       Rotation curves are AZIMUTHALLY-AVERAGED flat-disk ONLY -- WKAPP releases
       NO per-side (approaching/receding) split.  Per-side must be re-derived
       from the released velocity fields (this pipeline).
   - Pilot DR2 (2024-09-23): ~1800 HI sources at 30'' (NGC 4808, NGC 5044, Vela
       + re-releases), 80 galaxies at 12'' high-res, kinematic models for >120
       detections (Murugeshan+2024, arXiv:2409.13130).
   - Every catalogued source ships SoFiA products incl. the 2D moment-1
       velocity field (_mom1.fits, barycentric Hz) -- small (20-400 KB) and
       individually downloadable, anonymous:
         https://ws.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/raven/files/cadc:WALLABY/<file>
       (also CASDA: https://data.csiro.au, and CANFAR TAP as queried here).
   - 3KIDNAS (successor pipeline): ~400 models across PDR1+PDR2 announced
       (WALLABY newsletter 21, 2025), upload to CADC/CASDA pending the release
       paper -- NOT yet in the public CAOM2 census below.
""")
    print("  Measured from the CADC archive (distinct J-name galaxies):")
    print(f"    sources with a mom1 velocity field : {len(mom):5d}")
    print(f"    galaxies with WKAPP geometry       : {len(kin):5d}")
    print(f"    PER-SIDE-CAPABLE NOW (both)        : {len(both):5d}")
    print()
    print("  Capacity vs the banked directional-EFE requirement")
    print("  (directional_efe_2026/confrontation.out, both a0 footings):")
    for label, n_req in [
        ("AQUAL-band floor (4%, laneB)               ", 192),
        ("N target, canonical a0=9.36e-11 (w=0.304)  ", 1157),
        ("N target, alt a0=1.13e-10 (w=0.304)        ", 1424),
        ("AQUAL-band ceiling (1%, laneB)             ", 3057),
    ]:
        frac = len(both) / n_req
        print(f"    {label}: N={n_req:5d}  -> in hand {frac:5.1%}")
    print(f"""
  Honest statement:
    - NOW: {len(both)} per-side-capable galaxies with released geometries
      ({len(both)}/1157 = {len(both)/1157:.0%} of the canonical-footing target;
      {len(both)}/192 = {len(both)/192:.0%} of the most favorable AQUAL-floor case).
      The in-hand release CANNOT reach the 3-sigma AQUAL-vs-BranchB target on
      either a0 footing; it CAN begin to probe the 4%-AQUAL floor if per-side
      systematics stay below the 0.092 lopsidedness scatter.
    - Un-modelled sources ({len(mom) - len(both)} more mom1 fields) need a
      geometry before per-side extraction; 3KIDNAS (~400 models) will raise
      the capable count by ~{max(0, 400 - len(both))} when public.
    - FULL SURVEY: ~210,000 detections; Deg+22's own projection = kinematic
      models for ~40,000 galaxies (20% success) with a >10% floor (~21,000).
      Even the floor exceeds every banked N target (1157/1424/3057) by >6x --
      the scale-up path is real, but it is YEARS out, not months.
    - The OTHER missing ingredient (g_ext DIRECTION, reconstructable from
      2M++/MCXC/NSA per Chae+2021 sec. 3) is unaffected by WALLABY and still
      must be built (banked: laneB_FEASIBILITY.md).
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())

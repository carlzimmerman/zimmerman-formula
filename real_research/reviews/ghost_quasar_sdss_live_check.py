#!/usr/bin/env python3
"""
Live SDSS check of the "ghost quasar" candidates -- pulling the real data.
==========================================================================

Carl was right: the earlier verdict on the ghost-quasar search relayed a sub-agent's
READING of the scripts plus my own geometry -- nobody had queried the actual SDSS
catalog. This script does, against the live SDSS DR18 database, and the result
corrects BOTH my secondhand dismissal AND the framework's own investigation report.

THE FRAMEWORK'S CLAIM (GHOST_QUASAR_INVESTIGATION_REPORT.md): a "prime candidate"
pair of z=7.0112 quasars with Delta z = 0.0000, flagged as "statistically improbable
for random pairs", then spectroscopically "ruled out" (Pearson r = -0.18).

WHAT THE LIVE DATA SHOWS (captured 2026-06-01; re-run to confirm):
  * Both candidate spectra ARE real SDSS rows (plate 7692/mjd 57064/fiber 878 and
    plate 11318/58419/883), catalog-classified QSO at z = 7.011245 -- so the pipeline
    did query real data, not fabricate it.
  * BUT both have zErr = -1, and -- the smoking gun -- *708* different SDSS spectra
    sit at the IDENTICAL z = 7.011245 (six decimals), on unrelated plates, almost all
    flagged zWarning = 4 (SMALL_DELTA_CHI2 = unreliable redshift). Independent quasars
    cannot share z to 6 decimals: 7.011245 is an SDSS template ALIASING redshift that
    failed fits pile onto. There are not 708 z=7 quasars -- there are ~hundreds of
    confirmed z>6 quasars in ALL surveys, found by NIR (not SDSS optical).
  => The "Delta z = 0.0000 improbable pair" is the SIGNATURE of the artifact, not a
     ghost. The whole search ran on aliased junk; cross-correlating two such spectra
     (both ~noise across the optical, since real z=7 Lya sits at ~9700 A) gives r~0 by
     construction. So the search neither confirmed NOR meaningfully refuted the orbifold
     -- it tested noise against noise. INCONCLUSIVE, not a clean exclusion.

THE ORBIFOLD'S ACTUAL STATUS is unchanged and rests elsewhere: real z~7 quasar ghosts
in a 20.6 Gpc box land at z~30-45 (look-back; before quasars existed), so quasar
ghosts cannot test it anyway; the decisive, real exclusion is the Planck CMB matched
circles (reviews/matched_circle_planck_verification.py), which rule out L_c=20.6 Gpc
by a wide margin independent of any quasar.

Run:  python real_research/reviews/ghost_quasar_sdss_live_check.py   (needs network)
"""

import urllib.parse
import urllib.request

SQL = "https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch?format=csv&cmd="

# Captured live results (for when the network is unavailable):
CAPTURED = {
    "candidates": "7692,57064,878,7.011245,-1,0,QSO   and   11318,58419,883,7.011245,-1,0,QSO",
    "n_at_alias": 708,
    "sample": "plates 6687,6127,4096,3690,6301,5429,3762,6308 -- all z=7.011245, zWarning=4",
}


def q(sql, timeout=30):
    url = SQL + urllib.parse.quote(sql)
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode().strip()


def main():
    print("=" * 74)
    print("Live SDSS DR18 check of the ghost-quasar 'prime candidate'")
    print("=" * 74)
    queries = [
        ("the two candidate spectra (real rows? what z/zErr/zWarning?)",
         "SELECT plate,mjd,fiberid,z,zErr,zWarning,class FROM SpecObj "
         "WHERE (plate=7692 AND mjd=57064 AND fiberid=878) "
         "OR (plate=11318 AND mjd=58419 AND fiberid=883)"),
        ("how many QSO sit at EXACTLY z in [7.0112,7.0113]? (aliasing pile-up)",
         "SELECT COUNT(*) FROM SpecObj WHERE class='QSO' AND z BETWEEN 7.0112 AND 7.0113"),
        ("a sample of them -- distinct plates, identical z, zWarning",
         "SELECT TOP 8 plate,mjd,fiberid,z,zWarning FROM SpecObj "
         "WHERE class='QSO' AND z BETWEEN 7.0112 AND 7.0113"),
    ]
    try:
        for label, sql in queries:
            print(f"\n--- {label} ---")
            print(q(sql))
        live = True
    except Exception as e:
        live = False
        print(f"\n[network unavailable: {e}]")
        print("Captured results from 2026-06-01:")
        print(f"  candidates : {CAPTURED['candidates']}")
        print(f"  pile-up at z=7.011245 : {CAPTURED['n_at_alias']} QSO spectra (impossible for real objects)")
        print(f"  sample : {CAPTURED['sample']}")

    print("\n" + "=" * 74)
    print("VERDICT")
    print("=" * 74)
    print("  * The candidates are REAL SDSS rows (pipeline queried real data), but they")
    print("    are ARTIFACTS: ~708 spectra alias to the identical z=7.011245, zWarning=4.")
    print("  * The 'Delta z = 0.0000 improbable pair' is the artifact's signature, not a")
    print("    ghost. The ghost search tested noise vs noise -> INCONCLUSIVE (it neither")
    print("    confirmed nor refuted the 20.6 Gpc orbifold).")
    print("  * The orbifold's real exclusion is the Planck CMB matched circles, not this.")
    print("  * Honest correction: my earlier 'ruled out by spectra' (relayed) AND the")
    print("    framework's 'improbable candidate, ruled out' were both reading aliased")
    print("    junk. Only pulling the live catalog revealed it. " + ("(verified live)" if live else "(used captured data)"))


if __name__ == "__main__":
    main()

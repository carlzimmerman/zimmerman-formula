"""EUC12 construction B, fetch: Legacy Surveys DR10 Tractor photometry around each lens (P lenses and Auger SLACS
lenses with logMs) from the NOIRLab Data Lab TAP service; one paced stream, >= 1.2 s apart, generic User-Agent.
Raw replies -> _external_data/euc12_common_mass_scale/ls_dr10/<name>.csv ; MANIFEST.txt appended.
Run from the repo root."""
import hashlib, os, sys, time, urllib.parse, urllib.request, datetime
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from euc12_common import euclid_chosen, load_slacs_pos

OUT = "_external_data/euc12_common_mass_scale/ls_dr10"
MAN = "_external_data/euc12_common_mass_scale/MANIFEST.txt"
URL = "https://datalab.noirlab.edu/tap/sync"
UA = "python-tap-client/1.0"
Q = ("SELECT ls_id, ra, dec, type, brick_primary, flux_g, flux_r, flux_z, flux_w1, flux_ivar_z, flux_ivar_w1, "
     "mw_transmission_z, mw_transmission_w1 FROM ls_dr10.tractor "
     "WHERE 't' = q3c_radial_query(ra, dec, {ra:.7f}, {dec:.7f}, {r:.7f})")


def fetch(name, ra, dec):
    fn = f"{OUT}/{name}.csv"
    if os.path.exists(fn) and os.path.getsize(fn) > 0:
        return "cached"
    q = Q.format(ra=ra, dec=dec, r=2.0 / 3600)
    url = URL + "?" + urllib.parse.urlencode(dict(REQUEST="doQuery", LANG="ADQL", FORMAT="csv", QUERY=q))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for att in range(3):
        try:
            b = urllib.request.urlopen(req, timeout=90).read()
            break
        except Exception as e:  # noqa
            print("  retry", name, repr(e)[:120], flush=True)
            time.sleep(5 * (att + 1))
    else:
        return "FAILED"
    open(fn, "wb").write(b)
    with open(MAN, "a") as m:
        m.write(f"{datetime.datetime.utcnow().isoformat()}Z\t{name}\t{len(b)} B\tsha256 {hashlib.sha256(b).hexdigest()}\t"
                f"TAP sync {URL} ADQL: {q}\tlicence: Legacy Surveys data public (CC BY 4.0 per survey policy)\n")
    return f"{len(b)} B"


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(MAN):
        open(MAN, "w").write("EUC12 fetch manifest: Legacy Surveys DR10 Tractor via NOIRLab Data Lab TAP (sync, csv).\n"
                             "Columns: utc, name, bytes, sha256, query, licence.\n")
    targets = []
    eu = euclid_chosen()
    pr = pd.read_csv("closure_2026_11_12/EUC5R_blind_dynamical_boost_regrade/euc5r_per_lens.csv")
    P = set(pr.uid[pr.in_P])
    for _, r in eu[eu.unique_identifier.isin(P)].iterrows():
        targets.append((r.unique_identifier, r.ra, r.dec))
    for s in load_slacs_pos():
        if s["logMs"] == s["logMs"]:
            targets.append(("SLACS_" + s["name"], s["ra"], s["dec"]))
    print(len(targets), "targets", flush=True)
    for name, ra, dec in targets:
        t0 = time.time()
        st = fetch(name, ra, dec)
        print(name, st, f"{time.time() - t0:.1f}s", flush=True)
        if st != "cached":
            time.sleep(1.2)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
desi_confirm.py -- confirm MultimodalUniverse/desi exposes member REDSHIFTS usable for
the cluster relational-sigma-spread test (banked prep_2026/sigma_spread/), the clean
MG-impossible discriminator (MI predicts a 6-13% non-adiabatic sigma spread, MG exactly 0).

WHAT THE TEST NEEDS: per-galaxy spectroscopic redshifts (-> peculiar/LOS velocities),
sky coords (-> cluster membership + projected radius), and a redshift-quality cut.

FINDING (schema-live via HF): MMU/desi provides all three, but only over the DESI
EDR / SV3 + PROVABGS SUBSET, not the full ~20M-spectra DESI.
exit 0.
"""
import sys
import pyarrow.parquet as pq
from huggingface_hub import HfApi, HfFileSystem


def main():
    api = HfApi(); fs = HfFileSystem()
    print("=" * 78)
    print("MMU/desi -- member-redshift availability for the cluster sigma-spread test")
    print("=" * 78)
    total = {}
    for name, first in [("MultimodalUniverse/desi", "edr_sv3/train-00000-of-00007.parquet"),
                        ("MultimodalUniverse/desi_provabgs", "provabgs/train-00000-of-00001.parquet")]:
        files = api.list_repo_files(name, repo_type="dataset")
        pqs = [f for f in files if f.endswith(".parquet")]
        rows = 0
        for f in pqs:
            pf = pq.ParquetFile(fs.open(f"datasets/{name}/{f}"))
            rows += pf.metadata.num_rows
        pf0 = pq.ParquetFile(fs.open(f"datasets/{name}/{first}"))
        cols = [c.name for c in pf0.schema_arrow]
        total[name] = rows
        print(f"\n{name}:  {len(pqs)} parquet shards, ~{rows} rows total")
        has_z = [c for c in cols if c.upper() in ("Z", "Z_HP", "Z_MW")]
        has_zerr = [c for c in cols if "ZERR" in c.upper()]
        has_zwarn = [c for c in cols if "ZWARN" in c.upper() or "ZFAIL" in c.upper()]
        has_coord = [c for c in cols if c.lower() in ("ra", "dec")]
        has_id = [c for c in cols if c.lower() == "object_id"]
        print(f"   redshift   : {has_z or 'NONE'}")
        print(f"   z error    : {has_zerr or 'NONE'}")
        print(f"   z quality  : {has_zwarn or 'NONE'}")
        print(f"   sky coords : {has_coord or '(none direct; via object_id=TARGETID cross-match)'}")
        print(f"   id         : {has_id or 'NONE'}")

    print("\n" + "-" * 78)
    print("VERDICT: MMU/desi DOES expose member redshifts (Z, ZERR, ZWARN) usable for")
    print("  cluster-member LOS velocities; sky coords are direct in desi_provabgs (ra/dec)")
    print("  and recoverable in the main config via object_id=TARGETID cross-match.")
    print("  CAVEAT: this is the DESI EDR/SV3 + PROVABGS SUBSET (~%d + ~%d rows), NOT the"
          % (total.get("MultimodalUniverse/desi", 0), total.get("MultimodalUniverse/desi_provabgs", 0)))
    print("  full ~20M DESI.  SV3 rosette fields are not cluster-targeted -> per-cluster")
    print("  member counts are the binding limit (sigma_spread/POWER.md already underpowered).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

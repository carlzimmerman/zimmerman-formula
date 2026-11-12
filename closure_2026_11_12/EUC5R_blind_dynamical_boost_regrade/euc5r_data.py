"""EUC5R data access: ECLIPSE samples P and S (EUC1 section 2, recomputed here), A1.1 spectrum list."""
import numpy as np
import pandas as pd

ED = "_external_data/euclid_dr1_eclipse"
KEY = f"{ED}/eclipse_dr1_catalogue_key_v20261103.csv"
OBJ = f"{ED}/ECLIPSE_object_catalogue.csv"
MATCH = "closure_2026_11_12/EUC2_desi_source_hunt/euc2_matches.csv"
DESI_DIR = f"{ED}/desi_spectra"
SLACS_DIR = f"{ED}/slacs_sdss_spectra"


def samples():
    k = pd.read_csv(KEY, low_memory=False)
    o = pd.read_csv(OBJ, low_memory=False)[["Unique_Identifier", "large_system_warning", "desi_deflector_specz"]]
    o = o.rename(columns={"Unique_Identifier": "unique_identifier"})
    d = k.merge(o, on="unique_identifier", how="left")
    base = d.lens_model_success.astype(bool) & d.final_sample.astype(bool) & (d.large_system_warning == False)
    valid = ((d.eclipse_effective_einstein_radius > 0) & (d.eclipse_effective_radius > 0) &
             (d.eclipse_sersic_index >= 0.6) & (d.eclipse_sersic_index <= 10) & (d.eclipse_median_phz > 0) &
             (d.eclipse_log_survived_mass_med > 0))
    d["in_P"] = base & valid & (d.lens_grade == "A")
    d["in_S"] = base & valid & d.lens_grade.isin(["A", "B"])
    d["base_A_removed"] = base & (d.lens_grade == "A") & ~valid
    return d


def spectra_list(cat):
    """A1.1: flagged rows, and extension rows whose DESI redshift (warning 0) lies inside photo-z 70% +- 0.1."""
    m = pd.read_csv(MATCH)
    c = cat.set_index("unique_identifier")
    rows = []
    for _, r in m.iterrows():
        u = r.unique_identifier
        if u not in c.index:
            continue
        cr = c.loc[u]
        if bool(r.flagged):
            zdef, kind = float(r.desi_deflector_specz), "flagged"
        else:
            ok = (r.zwarn == 0) and (cr.eclipse_min70_phz - 0.1 <= r.z_desi <= cr.eclipse_max70_phz + 0.1)
            if not ok:
                continue
            zdef, kind = float(r.z_desi), "extension"
        rows.append(dict(unique_identifier=u, sparcl_id=r.sparcl_id, specprimary=bool(r.specprimary), kind=kind,
                         z_def=zdef, z_desi=float(r.z_desi), zwarn=int(r.zwarn), spectype=r.spectype,
                         in_P=bool(cr.in_P), in_S=bool(cr.in_S)))
    return pd.DataFrame(rows)

"""EUC12 shared helpers: Euclid chosen spectra (EUC5R's rule), Auger SLACS table with positions."""
import os, sys
import numpy as np
import pandas as pd

ROOT_EUC5R = "closure_2026_11_12/EUC5R_blind_dynamical_boost_regrade"
MATCH = "closure_2026_11_12/EUC2_desi_source_hunt/euc2_matches.csv"
SLACS = "real_research/data/slacs_auger2009_lenses.tsv"
KEY = "_external_data/euclid_dr1_eclipse/eclipse_dr1_catalogue_key_v20261103.csv"


def euclid_chosen():
    """EUC5R's chosen spectrum per S lens (primary, else smaller error among status ok), with TARGETID."""
    df = pd.read_csv(f"{ROOT_EUC5R}/euc5r_desi_fits.csv")
    out = []
    for u, g in df.groupby("unique_identifier"):
        pr = g[g.specprimary]
        if len(pr):
            out.append(pr.iloc[0])
        else:
            gg = g[g.status == "ok"]
            out.append((gg if len(gg) else g).sort_values("err").iloc[0])
    ch = pd.DataFrame(out)
    m = pd.read_csv(MATCH)[["sparcl_id", "targetid", "survey", "program", "z_desi"]].drop_duplicates("sparcl_id")
    ch = ch.merge(m, on="sparcl_id", how="left", suffixes=("", "_m"))
    k = pd.read_csv(KEY, usecols=["unique_identifier", "ra", "dec"])
    ch = ch.merge(k, on="unique_identifier", how="left")
    return ch


def _sexa(s, ra):
    p = [float(x) for x in s.split()]
    sg = -1.0 if s.strip().startswith("-") else 1.0
    v = abs(p[0]) + p[1] / 60 + p[2] / 3600
    return v * 15.0 if ra else sg * v


def load_slacs_pos():
    lines = open(SLACS, encoding="latin-1").read().splitlines()
    hi = [i for i, l in enumerate(lines) if l.startswith("recno")][0]
    hdr = lines[hi].split("\t")
    col = {c: i for i, c in enumerate(hdr)}
    out = []
    for l in lines[hi + 3:]:
        if not l.strip() or l.startswith("#"):
            continue
        r = l.split("\t")
        if len(r) < len(hdr):
            continue

        def f(k):
            try:
                return float(r[col[k]].strip())
            except ValueError:
                return float("nan")
        out.append(dict(name=r[col["SDSS"]].strip(), zl=f("zlens"), zs=f("zsrc"), sig=f("sigma"), esig=f("e_sigma"),
                        RE=f("RE"), ReV=f("Re(V)"), ReI=f("Re(I)"), logMs=f("logMs"), logMc=f("logMc"),
                        ra=_sexa(r[col["RAJ2000"]], True), dec=_sexa(r[col["DEJ2000"]], False)))
    return out
